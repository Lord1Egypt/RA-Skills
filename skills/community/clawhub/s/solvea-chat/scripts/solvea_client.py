"""Solvea Chat API 客户端（流式接口）"""
import logging
import os
import sys
import uuid
import json
from pathlib import Path

import httpx

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent / ".env", override=False)
except ImportError:
    pass


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        print(f"Error: environment variable {name} is not set", file=sys.stderr)
        print(f"  → copy .env.example to .env and fill in the values", file=sys.stderr)
        sys.exit(1)
    return value


_SOLVEA_BASE_URL_DEFAULT = "https://apps.voc.ai"


class SolveaClient:
    def __init__(self):
        self.base_url = os.getenv("SOLVEA_BASE_URL", _SOLVEA_BASE_URL_DEFAULT)
        self.api_key = _require_env("SOLVEA_API_KEY")
        self.agent_id = int(_require_env("SOLVEA_AGENT_ID"))
        self.headers = {
            "Content-Type": "application/json",
            "X-Token": self.api_key,
        }

    def chat(self, message: str, chat_id: str | None = None) -> dict:
        """
        发送消息，收集 SSE 流式响应后返回完整结果。
        chat_id 不传则自动生成新会话。

        SSE 格式：
          isEnd:false → data.data 是字符串（流式片段，忽略）
          isEnd:true  → data.data 是对象，含 chatId / content / type

        返回: {"chatId": str, "content": str, "type": str, "handoff": bool}
        """
        request_id = chat_id or str(uuid.uuid4())

        url = f"{self.base_url}/api_v2/intelli/plg/transcript/{request_id}/stream"
        body = {
            "chatId": request_id,
            "option": {"personaId": self.agent_id},
            "touchPoint": "LIVE_CHAT",
            "messages": [
                {
                    "role": "user",
                    "content": message,
                    "id": str(uuid.uuid4()),
                }
            ],
        }

        final_data = {}

        logging.debug("api request url: %s", url)
        logging.debug("api request body: %s", json.dumps(body, ensure_ascii=False))

        with httpx.stream("POST", url, json=body, headers=self.headers, timeout=60) as resp:
            resp.raise_for_status()
            for line in resp.iter_lines():
                line = line.strip()
                if not line or not line.startswith("data:"):
                    continue
                raw = line[len("data:"):].strip()
                try:
                    event = json.loads(raw)
                except json.JSONDecodeError:
                    continue

                # 只取最终事件（isEnd:true），其中 data 是完整响应对象
                if event.get("isEnd") is True:
                    inner = event.get("data", {})
                    if isinstance(inner, dict):
                        final_data = inner
                    break

        return {
            # 优先用服务端返回的 chatId，用于后续会话
            "chatId": final_data.get("chatId") or request_id,
            "content": final_data.get("content", ""),
            "type": final_data.get("type", ""),
            "handoff": final_data.get("handoff", False),
        }
