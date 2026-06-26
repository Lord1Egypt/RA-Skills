#!/usr/bin/env python3
"""
OpenClaw Homepage Plugin - 简化版
直接通过 HTTP API 调用 Gateway
"""

import os
import yaml
import logging
import json
import requests
from pathlib import Path
from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CONFIG_PATH = Path.home() / ".openclaw" / "homepage" / "config.yaml"
DATA_DIR = Path.home() / ".openclaw" / "homepage" / "data"
SESSION_EXPIRE_HOURS = 24

DATA_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="OpenClaw Homepage Plugin")

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    reply: str
    session_id: str
    timestamp: str

def load_config():
    if not CONFIG_PATH.exists():
        raise HTTPException(status_code=500, detail=f"配置文件不存在")
    with open(CONFIG_PATH, 'r') as f:
        return yaml.safe_load(f)

def get_session_history(session_id):
    session_file = DATA_DIR / f"{session_id}.json"
    if session_file.exists():
        with open(session_file, 'r') as f:
            data = json.load(f)
            timestamp = datetime.fromisoformat(data.get('timestamp', '2000-01-01'))
            if datetime.now() - timestamp > timedelta(hours=SESSION_EXPIRE_HOURS):
                return []
            return data.get('messages', [])
    return []

def save_session_history(session_id, messages):
    session_file = DATA_DIR / f"{session_id}.json"
    with open(session_file, 'w') as f:
        json.dump({'messages': messages, 'timestamp': datetime.now().isoformat()}, f)

def call_agent(message: str, history: list, config: dict, session_id: str) -> str:
    """通过 Gateway WS API 调用 Agent"""
    agent_config = config.get('agent', {})
    agent_id = agent_config.get('id', 'main')
    gateway_url = agent_config.get('url', 'http://localhost:18789').replace('http', 'ws')
    gateway_token = agent_config.get('api_key', '')
    
    # 构建上下文
    context = ""
    for msg in history[-5:]:
        role = msg.get('role', 'user')
        content = msg.get('content', '')
        context += f"{role}: {content}\n"
    
    full_message = f"{context}\n用户: {message}" if context else message
    
    # 使用 Gateway 的 WebSocket API
    import websocket
    
    ws_url = f"{gateway_url}/agent/{agent_id}?token={gateway_token}"
    logger.info(f"连接: {ws_url}")
    
    try:
        ws = websocket.create_connection(ws_url, timeout=30)
        
        # 发送消息
        ws.send(json.dumps({
            "message": full_message,
            "sessionId": f"homepage-{session_id[:32]}"
        }))
        
        # 接收响应
        response = ws.recv()
        ws.close()
        
        data = json.loads(response)
        payloads = data.get('result', {}).get('payloads', [])
        if payloads:
            return payloads[0].get('text', '获取回复失败')
        return data.get('reply', data.get('message', '获取回复失败'))
        
    except Exception as e:
        logger.error(f"WebSocket 错误: {e}")
        return f"服务错误: {str(e)[:100]}"

@app.get("/homepage/health")
async def health_check():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

@app.post("/homepage/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, authorization: Optional[str] = Header(None)):
    config = load_config()
    expected_key = config.get('security', {}).get('api_key', '')
    
    if expected_key and authorization:
        token = authorization.replace('Bearer ', '')
        if token != expected_key:
            raise HTTPException(status_code=401, detail="无效的 API Key")
    
    history = get_session_history(request.session_id)
    history.append({"role": "user", "content": request.message})
    
    reply = call_agent(request.message, history, config, request.session_id)
    
    history.append({"role": "assistant", "content": reply})
    save_session_history(request.session_id, history)
    
    return ChatResponse(reply=reply, session_id=request.session_id, timestamp=datetime.now().isoformat())

@app.get("/homepage/sessions")
async def list_sessions():
    sessions = []
    for f in DATA_DIR.glob("*.json"):
        with open(f) as fp:
            data = json.load(fp)
            sessions.append({
                "session_id": f.stem,
                "message_count": len(data.get('messages', [])),
                "last_active": data.get('timestamp', '')
            })
    return {"sessions": sessions}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
