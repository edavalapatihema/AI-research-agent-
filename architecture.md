                          +----------------------+
                          |      User Query      |
                          +----------+-----------+
                                     |
                                     v
                        +--------------------------+
                        |    LangGraph Workflow    |
                        |   Autonomous Agent Loop  |
                        +-----------+--------------+
                                    |
                    +---------------+----------------+
                    |                                |
                    v                                v
           +----------------+              +-------------------+
           |  Web Search    |              | Internal Knowledge |
           |  (DuckDuckGo)  |              |   Vector Store     |
           +--------+-------+              +---------+----------+
                    |                                |
                    v                                |
           +--------------------+                    |
           |   Web Documents    |                    |
           |   (Scraped HTML)   |                    |
           +---------+----------+                    |
                     |                               |
                     v                               v
           +--------------------+        +---------------------------+
           |   Text Processing  |        |   Vector Retrieval        |
           |   BeautifulSoup    |        |   (Top-K Similarity)      |
           +----------+---------+        +-------------+-------------+
                      |                                  |
                      v                                  v
               +-------------+                 +--------------------+
               | Embeddings  |                 |  LLM (Gemini)      |
               | HuggingFace |                 |  Answer Generation |
               +------+------+                 +---------+----------+
                      |                                  |
                      v                                  v
                +-----------+                   +-------------------+
                | ChromaDB  |                   |  Self Reflection  |
                | Vector DB |                   |   Score Answer    |
                +-----+-----+                   +---------+---------+
                      |                                   |
                      +-----------------------------------+
                                      |
                               If score < 8
                                 Research Again
