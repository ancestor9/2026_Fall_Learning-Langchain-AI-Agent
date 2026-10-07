# Multi-Database 기반 LLM Application 개발 프로젝트

## 1. 과제 개요

- PDF, TXT, CSV 형태의 다양한 데이터를 수집하고 전처리하여 클라우드 기반 데이터베이스에 저장하는 LLM Application을 개발한다.
- RDB, Vector DB, Graph DB를 각각 구축하고 데이터의 특성과 사용자 질문의 유형에 따라 적절한 데이터베이스를 선택하여 검색하는 Multi-Database RAG 시스템을 구현한다.
- 사용자의 질문을 LLM이 분석하여 적절한 데이터베이스를 Routing하고, 해당 데이터베이스에서 검색한 결과를 다시 LLM에 전달하여 자연어 형태의 최종 답변을 생성하도록 구현한다.
- 최종적으로 Streamlit 기반의 Web Application을 구현하여 사용자가 직접 질문하고 결과를 확인할 수 있도록 한다.
### Question → Routing → DB Selection → Retrieval → LLM Answer
---

# 2. 과제 목표

- LLM Application의 전체적인 데이터 처리 및 검색 구조를 이해한다.
- PDF, TXT, CSV 등 서로 다른 형태의 데이터를 Loading하고 전처리하는 방법을 학습한다.
- 문서를 Chunk 단위로 분할하고 Embedding Vector로 변환하는 과정을 이해한다.
-       chunk_size = 300
        chunk_size = 500
        chunk_size = 1000
- PostgreSQL 기반 RDB와 Vector DB(Supabase PostgreSQL의 pgvector)의 차이 및 활용 방법을 이해한다.
-       Document --> Chunk --> Embedding --> 384 dimensional vector --> Supabase pgvector
- Graph DB를 이용하여 데이터 간의 관계를 표현하고 검색하는 방법을 학습한다.
- 사용자의 자연어 질문을 분석하여 적절한 데이터베이스를 선택하는 LLM Router를 구현한다.
- Retrieval 결과를 LLM에 전달하여 근거 기반의 답변을 생성하는 RAG 구조를 구현한다.
- 최종적으로 실제 서비스 형태의 LLM Application을 설계하고 구현한다.

---

# 3. 전체 시스템 구성
## Embedding Model
- HuggingFace의 all-MiniLM-L6-v2 모델을 사용한다.
- 문서와 사용자 질문을 동일한 Embedding Model로 변환하여 Embedding Vector는 384차원으로 구성한다.


전체 시스템은 다음과 같은 구조로 구현한다.

```text
                    PDF / TXT / CSV
                           │
                           ▼
                   Document Loading
                           │
                           ▼
                       Chunking
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
           RDB Index   Vector Index  Graph Index
              │            │            │
              ▼            ▼            ▼
          PostgreSQL    pgvector       Neo4j
              │            │            │
              └────────────┼────────────┘
                           │
                           ▼
                    User Question
                           │
                           ▼
                      LLM Router
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
             RDB        Vector DB     Graph DB
              │            │            │
              ▼            ▼            ▼
          SQL Search   Similarity     Cypher
                           Search       Search
              │            │            │
              └────────────┼────────────┘
                           ▼
                    Retrieved Context
                           │
                           ▼
                      LLM Generation
                           │
                           ▼
                     Final Answer
                           │
                           ▼
                    Streamlit Web App
