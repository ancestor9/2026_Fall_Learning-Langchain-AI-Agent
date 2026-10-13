################################################
### Minimal FastAPI + Gradio Example
### https://www.gradio.app/docs/gradio/mount_gradio_app
################################################
from fastapi import FastAPI
import gradio as gr
app = FastAPI()
@app.get("/")
def read_main():
    return {"message": "This is your main app"}

io = gr.Interface(lambda x: "Hello, " + x + "!", "textbox", "textbox")
app = gr.mount_gradio_app(app, io, path="/gradio")

## # 실행 방법: uvicorn gradio_from_swagger:app --reload    
# Gradio UI는 http://http://127.0.0.1:8000/gradio 에서 접근 가능

################################################
### Original FastAPI Example (commented out)
################################################

# from fastapi import FastAPI 
# from pydantic import BaseModel
# from typing import Optional

# class Item(BaseModel):
#     name: str
#     description: Optional[str] = None
#     price: float
#     tax: Optional[float] = None

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str | None = None):
#     return {"item_id": item_id, "q": q}

# @app.post("/items2/{item_id}")
# def create_item2(item_id: int, item: Item):
#     return {"item_id": item_id, "item": item}



# #######################################
# ### FastAPI + Gradio Integration Example
# #######################################
# from fastapi import FastAPI
# import gradio as gr
# import json
# from typing import Optional

# # 1. FastAPI 애플리케이션 초기화
# app = FastAPI(
#     title="FastAPI with Gradio UI",
#     description="Gradio is mounted to provide an interactive UI for selected endpoints."
# )

# # 2. FastAPI 엔드포인트 정의 (기존 코드 유지)

# @app.get("/")
# def read_root():
#     """루트 경로. 간단한 상태 확인용."""
#     return {"Hello": "World"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
#     """특정 item_id와 선택적 쿼리(q)를 반환하는 엔드포인트."""
#     return {"item_id": item_id, "q": q}

# # 3. Gradio 인터페이스에 연결할 파이썬 함수 정의
# # 이 함수는 FastAPI 엔드포인트의 비즈니스 로직을 모방하거나, 
# # 필요한 경우 직접 FastAPI의 엔드포인트를 호출하도록 구성할 수 있습니다.
# # 여기서는 엔드포인트 로직을 직접 구현합니다.
# def gradio_read_item(item_id: int, q: Optional[str]):
#     """
#     Gradio를 통해 노출할 'read_item' 로직.
#     Gradio는 함수를 실행하고 그 결과를 출력합니다.
#     출력은 JSON 문자열로 포맷팅하여 Gradio의 'json' 출력 타입에 맞춥니다.
#     """
#     result = {"item_id": item_id, "q": q}
#     # Gradio의 'json' 컴포넌트를 사용하기 위해 JSON 문자열로 반환합니다.
#     return json.dumps(result, indent=2, ensure_ascii=False)

# # 4. Gradio 인터페이스 생성
# # FastAPI의 /items/{item_id} 엔드포인트를 위한 사용자 인터페이스를 정의합니다.
# item_interface = gr.Interface(
#     fn=gradio_read_item,
#     inputs=[
#         gr.Number(
#             label="Item ID (정수)", 
#             value=101, 
#             interactive=True,
#             info="조회할 아이템의 ID를 입력하세요. (예: 1, 100)"
#         ),
#         gr.Textbox(
#             label="Query Parameter 'q' (선택)", 
#             placeholder="선택적 쿼리 문자열을 입력하세요.",
#             info="FastAPI의 'q' 파라미터에 해당합니다."
#         )
#     ],
#     outputs=gr.JSON(label="API 응답 결과"),
#     title="🔍 Item 조회 API (Gradio UI)",
#     description="FastAPI의 `/items/{item_id}` 엔드포인트를 테스트하는 Gradio 인터페이스입니다. 입력 값을 변경하고 'Submit'을 눌러보세요."
# )

# # 5. Gradio 애플리케이션을 FastAPI 앱에 마운트
# # Gradio UI는 /gradio_ui 경로에서 접근할 수 있습니다.
# app = gr.mount_gradio_app(app, item_interface, path="/gradio_ui")

# # 실행 방법:
# # uvicorn gradio_from_swagger:app --reload
# #
# # FastAPI 문서 (Swagger UI)는 http://127.0.0.1:8000/docs 에서 접근 가능합니다. (Gradio로 대체하지 않은 경우)
# # Gradio UI는 http://127.0.0.1:8000/gradio_ui 에서 접근 가능합니다.

