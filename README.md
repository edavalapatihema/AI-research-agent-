# AI-research-agent-
Autonomous AI research agent using LangGraph, RAG, and ChromaDB.  The system searches the web, ingests documents into a vector database,  retrieves knowledge using embeddings, and improves answers using a self-reflection loop.


Autonomous Research Agent built with LangGraph, LangChain, and LlamaIndex.

The agent can search the web, ingest documents into a Chroma vector database, 
retrieve information using Retrieval-Augmented Generation (RAG), and evaluate 
its own responses using a self-reflection scoring mechanism.

Key features:
• Web search using DuckDuckGo
• Web document ingestion pipeline
• Persistent vector database using ChromaDB
• HuggingFace embeddings for semantic search
• Gemini LLM for reasoning and response generation
• Self-reflective research loop for improved answers

This project demonstrates how agentic workflows can combine web retrieval, 
vector databases, and LLM reasoning to build autonomous research systems.


## Overview

This project implements an agentic AI workflow capable of:

Searching the web

Extracting relevant information

Storing documents in a vector database

Retrieving knowledge using embeddings

Generating answers with an LLM

Evaluating the response quality

Iterating research if needed

The system demonstrates how autonomous agents can combine web search, RAG, and reasoning loops to build intelligent research systems.

## Features

Autonomous AI research loop
Web search integration
Web document ingestion pipeline
Persistent vector knowledge base
Retrieval-Augmented Generation (RAG)
Self-reflection answer scoring
Modular LangGraph workflow
Semantic search with embeddings

## Tech Stack
Component	Technology
LLM	Google Gemini
Agent Framework	LangGraph
LLM Framework	LangChain
RAG Framework	LlamaIndex
Vector Database	ChromaDB
Embeddings	HuggingFace
Web Search	DuckDuckGo
Web Scraping	BeautifulSoup
Language	Python

## Project Architecture
User Query
    │
    ▼
LangGraph Agent Workflow
    │
    ▼
ReAct Reasoning
    │
    ├── Web Search Tool
    │       │
    │       ▼
    │   Fetch Web Pages
    │
    ├── Web Document Ingestion
    │       │
    │       ▼
    │   Clean Text (BeautifulSoup)
    │
    ▼
Embeddings (HuggingFace)
    │
    ▼
Chroma Vector Database
    │
    ▼
Retriever (Top-K Similarity)
    │
    ▼
LLM (Gemini)
    │
    ▼
Answer Generation
    │
    ▼
Self Reflection
    │
    ├── Score ≥ 8 → Return Answer
    └── Score < 8 → Research Again

 ## Installation
1 Clone Repository

2 Create Virtual Environment
python -m venv venv

Activate environment
Linux / Mac
source venv/bin/activate
Windows
venv\Scripts\activate

3 Install Dependencies
pip install -r requirements.txt

## Environment Setup
Create .env file:

GOOGLE_API_KEY=your_google_api_key
 copy the template:
cp .env.example .env

 ## Running the Project
Start the agent:
python AgenticParser.py

Example output:
Autonomous Research Agent Started
Type 'exit' or 'quit' to stop.

Example query:
Enter your query:
What is Retrieval Augmented Generation?

Response:
Answer:
RAG (Retrieval Augmented Generation) is a method where...

## Tools Used by the Agent
Web Search

Searches the internet for current information.
web_search(query)
## Web Document Ingestion
Downloads web pages and stores them in the vector database.
ingest_web_documents(query)
## Internal Knowledge Base
Retrieves information using vector similarity search.
internal_knowledge_base(query)

## RAG Pipeline
Web search retrieves URLs
Pages scraped using BeautifulSoup
Clean text extracted
Documents embedded using HuggingFace embeddings
Stored in Chroma vector database
Retriever selects top relevant chunks
LLM generates grounded answers

## Embedding model used:

sentence-transformers/all-MiniLM-L6-v2
Self Reflection Mechanism

After generating an answer, the agent evaluates its quality.
## self Reflection Mechanisam 
Score range:
1 – 10
Evaluation criteria:
completeness
factual accuracy
grounding in retrieved knowledge
If score is below threshold, the agent performs additional research iterations.
Maximum research attempts: 3

## Example Workflow

User query:
Explain large language models
Agent process:
Web search
Document ingestion
Vector embedding
Retrieval
LLM reasoning
Self-evaluation
Final answer

## Security Notes

Do not commit API keys
Use environment variables
Validate web sources before ingestion

## Future Improvements

Possible enhancements:
Document chunking for better retrieval
Metadata filtering
Streaming responses
Multi-agent collaboration
FastAPI API interface
Web dashboard UI

## License
MIT License

## Contributing
Contributions are welcome.
1 Fork the repository
2 Create a feature branch
3 Submit a pull request
