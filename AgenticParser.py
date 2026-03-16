import chromadb
import requests
from bs4 import BeautifulSoup
from typing import TypedDict, Annotated, List
from urllib.parse import urlparse

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.tools import Tool
from langchain_community.tools import DuckDuckGoSearchResults

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import create_react_agent

from llama_index.core import VectorStoreIndex, StorageContext, Document
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.langchain import LangChainLLM


class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], "history"]
    research_steps: int
    is_complete: bool


langchain_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key="AIzaSyAAKd_muxbkMA1B9DUDiOzmTw1PhQC9Jhw"
)

llm = LangChainLLM(langchain_llm)

embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db_client = chromadb.PersistentClient(path="./chroma_db")
collection = db_client.get_or_create_collection("enterprise_hybrid_kb")

vector_store = ChromaVectorStore(chroma_collection=collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_vector_store(
    vector_store=vector_store,
    storage_context=storage_context,
    embed_model=embed_model
)

vector_retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=5
)

retriever_engine = RetrieverQueryEngine.from_args(
    retriever=vector_retriever,
    llm=llm
)


def fetch_clean_text(url: str):
    try:
        r = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.text, "html.parser")
        for s in soup(["script", "style"]):
            s.extract()
        text = soup.get_text(separator=" ", strip=True)
        return text[:15000]
    except:
        return None


search_tool_raw = DuckDuckGoSearchResults()


def web_search(query: str):
    return search_tool_raw.run(query)


def ingest_web(query: str):
    results = search_tool_raw.run(query)
    if isinstance(results, str):
        return "No ingestion performed."
    for item in results:
        url = item.get("link")
        if not url:
            continue
        text = fetch_clean_text(url)
        if text and len(text) > 500:
            doc = Document(
                text=text,
                metadata={"source": urlparse(url).netloc}
            )
            index.insert(doc)
    return "Web documents ingested into vector store."


def rag_query(query: str):
    response = retriever_engine.query(query)
    return str(response)


tools = [
    Tool(
        name="web_search",
        func=web_search,
        description="Search the web for up-to-date information."
    ),
    Tool(
        name="ingest_web_documents",
        func=ingest_web,
        description="Fetch and store web documents into internal knowledge base."
    ),
    Tool(
        name="internal_knowledge_base",
        func=rag_query,
        description="Retrieve grounded information from indexed documents."
    )
]


system_prompt = """
You are an autonomous research agent.
Use tools strategically.
Ingest new information when necessary before answering.
"""


agent = create_react_agent(
    model=langchain_llm,
    tools=tools,
    state_modifier=system_prompt
)


def researcher(state: AgentState):
    result = agent.invoke({"messages": state["messages"]})
    response = AIMessage(content=result["messages"][-1].content)
    return {
        "messages": state["messages"] + [response],
        "research_steps": state["research_steps"] + 1
    }


def self_reflection(state: AgentState):
    answer = state["messages"][-1].content
    critique_prompt = f"""
Evaluate the following answer for completeness,
grounding, and factual consistency.
Score from 1 to 10.
Only output the number.

Answer:
{answer}
"""
    score_response = langchain_llm.invoke([HumanMessage(content=critique_prompt)])
    try:
        score = int("".join(filter(str.isdigit, score_response.content)))
    except:
        score = 0
    return {
        "messages": state["messages"],
        "research_steps": state["research_steps"],
        "is_complete": score >= 8 or state["research_steps"] >= 3
    }


workflow = StateGraph(AgentState)
workflow.add_node("researcher", researcher)
workflow.add_node("self_reflection", self_reflection)
workflow.add_edge(START, "researcher")
workflow.add_edge("researcher", "self_reflection")
workflow.add_conditional_edges(
    "self_reflection",
    lambda state: END if state["is_complete"] else "researcher"
)

app = workflow.compile()


if __name__ == "__main__":
    print("Autonomous Research Agent Started")
    print("Type 'exit' or 'quit' to stop.\n")
    while True:
        query = input("Enter your query:\n")
        if query.lower() in ["exit", "quit", "stop"]:
            print("Shutting down agent.")
            break
        result = app.invoke({
            "messages": [HumanMessage(content=query)],
            "research_steps": 0,
            "is_complete": False
        })
        print("\nAnswer:\n")
        print(result["messages"][-1].content)
        print("\n" + "=" * 60 + "\n")
