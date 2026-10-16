# Code 실습 내용
        - Agent.ipynb: AI Agent의 기본 구조 및 동작 방식
        - Gemini API Get_started.ipynb: Gemini API 연동 설정 및 기초 활용
        - Langchain_rag_geminiAPI.ipynb: LangChain 프레임워크와 Gemini API를 결합하여 RAG(검색 증강 생성) 시스템을 구현
        - RAG_supabase.ipynb: Supabase의 pgvector(Vector DB)를 활용하여 벡터 검색 기반 RAG를 구현
        - Real_Time_Websearch.ipynb: 실시간 웹 검색 기능을 LLM과 연동하여 최신 정보를 검색 및 생성
        - gemini_client.py: Gemini API 호출 및 통신 로직을 전담하는 파이썬 클라이언트 모듈
        - gemini_gradio.ipynb: Gemini 모델과 Gradio 웹 UI를 연동하여 대화형 인터페이스를 구성
        - gemini_main.py: Gemini 기반 애플리케이션의 핵심 로직을 실행
        - gemini_pydantic.ipynb: Pydantic 라이브러리를 활용하여 Gemini의 응답을 구조화된 데이터(Structured Output)로 파싱
        - gemini_pydantic_more_robust.ipynb: 예외 처리 및 유효성 검증을 강화하여 안정적인 Pydantic 데이터 파싱을 구현
        - getting_started_with_google_colab_ai.ipynb: Google Colab 환경에서 Colab AI 및 Gemini API 사용
        - google_file_search.ipynb: Google 파일 검색 API를 활용하여 문서 검색 및 RAG 연동
        - gradio_from_swagger.py: Swagger API 명세를 기반으로 Gradio 웹 UI를 생성하고 연동
        - llm_graph_db.ipynb: LLM과 Graph DB(Neo4j 등)를 연동하여 지식 그래프 기반 검색 및 RAG를 구현


# Multi-Database 기반 LLM Application 개발 프로젝트 
- 수업 중에 끝나면 A+ & 마지막 기말시험 면제(마지막 수업 안 들어도 됨)

## 1. 과제 개요

- PDF, TXT, CSV 형태의 다양한 데이터를 수집하고 전처리하여 클라우드 기반 데이터베이스에 저장하는 LLM Application을 개발한다.
- RDB, Vector DB, Graph DB를 각각 구축하고 데이터의 특성과 사용자 질문의 유형에 따라 적절한 데이터베이스를 선택하여 검색하는 Multi-Database RAG 시스템을 구현한다.
- 사용자의 질문을 LLM이 분석하여 적절한 데이터베이스를 Routing하고, 해당 데이터베이스에서 검색한 결과를 다시 LLM에 전달하여 자연어 형태의 최종 답변을 생성하도록 구현한다.
- 최종적으로 Streamlit(or Gradio) 기반의 Web Application을 구현하여 사용자가 직접 질문하고 결과를 확인할 수 있도록 한다(선택사항).
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
-       Question → Routing → DB Selection → Retrieval → LLM Answer

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
                    Streamlit Web App (Gradio) ---- Optional 
