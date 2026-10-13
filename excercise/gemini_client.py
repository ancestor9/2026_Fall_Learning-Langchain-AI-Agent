# gemini_client.py

import os
from google import genai
from dotenv import load_dotenv

# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()

# Gemini 클라이언트를 초기화합니다.
# 클라이언트는 환경 변수 GEMINI_API_KEY에서 자동으로 API 키를 가져옵니다.
client = genai.Client()

# 사용할 모델을 정의합니다.
MODEL_NAME = "gemini-2.5-flash"

async def generate_gemini_response(prompt: str) -> str:
    """
    주어진 프롬프트에 대해 Gemini API를 호출하고 응답 텍스트를 반환합니다.
    """
    try:
        # 모델의 generate_content 메서드를 사용하여 응답을 생성합니다.
        response = client.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"Gemini API 호출 중 오류 발생: {e}")
        return "죄송합니다. AI 응답을 생성하는 데 문제가 발생했습니다."

# (선택 사항) 대화 기록을 유지하려면 'client.chats'를 사용하거나 
# FastAPI의 세션 관리 기능을 사용하여 history를 관리해야 합니다.
# 이 최소 예제에서는 각 요청을 독립적으로 처리합니다.