# main.py

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn

# 로직 모듈 임포트
from gemini_client import generate_gemini_response 

app = FastAPI()

# 프론트엔드에서 보낼 메시지 구조를 정의합니다.
class ChatRequest(BaseModel):
    message: str

# 1. 루트 엔드포인트: 챗봇 HTML 페이지 제공
@app.get("/", response_class=HTMLResponse)
async def get_root():
    """index.html 파일의 내용을 반환합니다."""
    # 실제 파일 경로를 사용하거나, 이처럼 인라인 HTML을 사용합니다.
    # 최소 코드를 위해 인라인 HTML을 사용합니다.
    return HTML_CONTENT

# 2. API 엔드포인트: 챗봇 응답 생성
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    사용자 메시지를 받아 Gemini API로 전달하고 응답을 반환합니다.
    """
    user_message = request.message
    
    # gemini_client 모듈의 함수를 호출하여 AI 응답을 얻습니다.
    ai_response = await generate_gemini_response(user_message)
    
    # 응답을 JSON 형식으로 반환합니다.
    return {"response": ai_response}

# FastAPI 실행을 위한 HTML_CONTENT 변수
HTML_CONTENT = """
<!DOCTYPE html>
<html>
<head>
    <title>Gemini Chatbot (FastAPI)</title>
    <style>
        body { font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background-color: #f0f0f0; }
        #chat-container { width: 400px; padding: 20px; border: 1px solid #ccc; border-radius: 8px; background-color: white; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        #messages { list-style: none; padding: 0; margin-bottom: 10px; height: 300px; overflow-y: scroll; border: 1px solid #eee; padding: 10px; border-radius: 4px; }
        .user-msg { text-align: right; color: blue; }
        .ai-msg { text-align: left; color: green; }
        #chat-form { display: flex; }
        #messageInput { flex-grow: 1; padding: 8px; border: 1px solid #ccc; border-radius: 4px; margin-right: 5px; }
        #sendButton { padding: 8px 15px; border: none; background-color: #007bff; color: white; border-radius: 4px; cursor: pointer; }
    </style>
</head>
<body>
    <div id="chat-container">
        <h1>Gemini Chatbot</h1>
        <ul id="messages"></ul>
        <form id="chat-form">
            <input type="text" id="messageInput" placeholder="메시지를 입력하세요" required>
            <button type="submit" id="sendButton">전송</button>
        </form>
    </div>

    <script>
        const chatForm = document.getElementById('chat-form');
        const messageInput = document.getElementById('messageInput');
        const messagesContainer = document.getElementById('messages');
        const sendButton = document.getElementById('sendButton');

        // 메시지를 채팅창에 추가하는 함수
        function addMessage(sender, text) {
            const li = document.createElement('li');
            li.textContent = `${sender}: ${text}`;
            li.className = sender === 'User' ? 'user-msg' : 'ai-msg';
            messagesContainer.appendChild(li);
            messagesContainer.scrollTop = messagesContainer.scrollHeight; // 스크롤을 맨 아래로
        }

        chatForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const userMessage = messageInput.value.trim();

            if (userMessage === "") return;

            addMessage('User', userMessage);
            messageInput.value = '';
            sendButton.disabled = true; // 버튼 비활성화 (로딩 표시)
            sendButton.textContent = '...';

            try {
                // FastAPI 백엔드에 POST 요청을 보냅니다.
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message: userMessage })
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }

                const data = await response.json();
                addMessage('AI', data.response); // AI 응답 추가

            } catch (error) {
                console.error('Error fetching chat response:', error);
                addMessage('System', '오류가 발생했습니다. 서버를 확인해주세요.');
            } finally {
                sendButton.disabled = false; // 버튼 다시 활성화
                sendButton.textContent = '전송';
            }
        });

        // 시작 메시지
        addMessage('System', '챗봇이 준비되었습니다. 질문해주세요!');
    </script>
</body>
</html>
"""

# if __name__ == "__main__":
#     # 개발용 서버 실행 (터미널에서 uvicorn main:app --reload 으로 실행하는 것을 권장)
#     # uvicorn.run(app, host="0.0.0.0", port=8000)