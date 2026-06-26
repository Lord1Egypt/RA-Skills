#!/usr/bin/env python3
"""
xiaozhi-esp32 MCP Server - 简化版
只保留run_agent全能工具 + WebSocket实时推送
"""

import asyncio
import json
import subprocess
import shlex
import os
import sys
import uuid
import yaml
import re
from aiohttp import web
from datetime import datetime
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "openclaw-mcp"
TOKEN_FILE = CONFIG_DIR / "token"
TASKS_DIR = CONFIG_DIR / "tasks"
CONFIG_FILE = Path(__file__).parent.parent / "config.yaml"

# Maximum message length to prevent abuse
MAX_MESSAGE_LENGTH = 2000

def load_config():
    """Load configuration from config.yaml"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            return yaml.safe_load(f) or {}
    return {}

def get_target_session():
    """Get target session from config or return empty"""
    config = load_config()
    return config.get("target_session", "")

def sanitize_message(message: str) -> str:
    """Sanitize message to prevent command injection and abuse"""
    if not isinstance(message, str):
        raise ValueError("Message must be a string")
    
    # Limit length
    if len(message) > MAX_MESSAGE_LENGTH:
        message = message[:MAX_MESSAGE_LENGTH]
    
    # Remove control characters except newline and tab
    message = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', message)
    
    return message.strip()

def get_token():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    TASKS_DIR.mkdir(parents=True, exist_ok=True)
    if TOKEN_FILE.exists():
        return TOKEN_FILE.read_text().strip()
    token = os.urandom(24).hex()
    TOKEN_FILE.write_text(token)
    print(f"Token: {token}", file=sys.stderr)
    return token

def verify_token(request):
    url_token = request.query.get("token", "")
    if url_token and url_token == get_token():
        return True
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header[7:] == get_token()
    return False

class TaskManager:
    def __init__(self):
        self.tasks = {}

    def create_task(self, name: str, params: dict) -> str:
        task_id = str(uuid.uuid4())[:8]
        self.tasks[task_id] = {
            "id": task_id,
            "name": name,
            "params": params,
            "status": "pending",
            "result": None,
            "error": None,
            "created_at": datetime.now().isoformat()
        }
        return task_id

    def update_task(self, task_id: str, status: str, result=None, error=None, summary=None):
        if task_id in self.tasks:
            self.tasks[task_id].update({
                "status": status,
                "result": result,
                "error": error,
                "updated_at": datetime.now().isoformat()
            })
            if summary:
                self.tasks[task_id]["summary"] = summary

    def get_task(self, task_id: str) -> dict:
        return self.tasks.get(task_id)

    def list_tasks(self, limit=10):
        return sorted(self.tasks.values(), key=lambda x: x.get("updated_at", ""), reverse=True)[:limit]

task_manager = TaskManager()

class OpenClawMCPServer:
    def __init__(self):
        self.name = "openclaw"
        self.version = "2.0.0"
        self.token = get_token()
        self.ws_clients = set()

    async def handle_call_tool(self, name: str, arguments: dict) -> str:
        if name == "run_agent":
            return await self.run_agent(arguments)
        elif name == "get_task":
            return self.get_task_tool(arguments)
        elif name == "list_tasks":
            return self.list_tasks_tool(arguments)
        else:
            return json.dumps({"error": f"Unknown tool: {name}. Use run_agent for all tasks."})

    async def run_agent(self, args: dict) -> str:
        message = args.get("message", "")
        if not message:
            return json.dumps({"error": "message required"})

        task_id = task_manager.create_task("run_agent", args)
        async_mode = args.get("async", True)

        if async_mode:
            asyncio.create_task(self._run_agent_background(task_id, message))
            return json.dumps({
                "async": True,
                "task_id": task_id,
                "status": "pending",
                "ws_endpoint": "/ws",
                "message": "任务已提交，结果将通过WebSocket推送"
            }, ensure_ascii=False)
        else:
            result = await self._run_agent_background(task_id, message)
            return result

    async def _run_agent_background(self, task_id: str, message: str):
        task_manager.update_task(task_id, "running")
        try:
            # Sanitize message to prevent injection
            safe_message = sanitize_message(message)
            
            # Build command safely using list (no shell=True)
            # 正确顺序: openclaw agent --to SESSION --message MSG --deliver
            cmd = ['timeout', '180', 'openclaw', 'agent']
            
            # Get target session from config if available
            target_session = get_target_session()
            if target_session:
                # Validate target_session format (basic check)
                if re.match(r'^[a-z]+:[a-z0-9]+:[A-Za-z0-9]+$', target_session):
                    cmd.extend(['--to', target_session])
            
            cmd.extend(['--message', safe_message, '--deliver'])
            
            # Run without shell=True for security
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=200)
            output = result.stdout.strip()
            summary = self.summarize_for_voice(output)
            task_manager.update_task(task_id, "completed", result=output, summary=summary)

            if self.ws_clients:
                await self.notify_task_completed(task_id, summary)

            return json.dumps({
                "async": False,
                "task_id": task_id,
                "status": "completed",
                "result": output,
                "summary": summary
            }, ensure_ascii=False)
        except Exception as e:
            task_manager.update_task(task_id, "failed", error=str(e))
            if self.ws_clients:
                await self.notify_task_completed(task_id, f"错误: {str(e)}")
            return json.dumps({
                "async": False,
                "task_id": task_id,
                "status": "failed",
                "error": str(e)
            }, ensure_ascii=False)

    def summarize_for_voice(self, text: str, max_length: int = 140) -> str:
        if len(text) <= max_length:
            return text

        # 优先提取结论
        conclusion_keywords = ["运行正常", "成功", "完成", "就绪", "无异常", "正常", "✅"]
        lines = text.strip().split("\n")
        last_line = lines[-1].strip() if lines else ""
        
        for kw in conclusion_keywords:
            if kw in last_line and len(last_line) < max_length:
                return last_line

        # 查找待确认事项
        action_items = []
        action_keywords = ["需要补充", "需要确认", "待确认", "需要您", "请提供", "请确认", "缺少"]
        for keyword in action_keywords:
            if keyword in text:
                idx = text.find(keyword)
                remaining = text[idx:]
                for line in remaining.split("\n")[1:]:
                    line = line.strip()
                    if not line:
                        continue
                    if " - " in line:
                        point = line.split(" - ")[0].strip()
                        if point and len(point) < 15:
                            action_items.append(point)
                if action_items:
                    break

        first_para = text.split("\n\n")[0] if "\n\n" in text else text[:60]
        if len(first_para) > 60:
            first_para = first_para[:60] + "..."

        if action_items:
            items_str = "、".join(action_items[:3])
            summary = f"{first_para} 另外需确认{items_str}等。"
        else:
            summary = first_para

        if len(summary) < max_length - 20:
            summary += " 详情请查看Channel或邮件。"

        return summary[:max_length]

    async def notify_task_completed(self, task_id: str, result: str):
        message = {
            "type": "task_completed",
            "task_id": task_id,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        disconnected = []
        for ws in list(self.ws_clients):
            try:
                await ws.send_json(message)
            except:
                disconnected.append(ws)
        for ws in disconnected:
            self.ws_clients.discard(ws)

    def get_task_tool(self, args: dict) -> str:
        task_id = args.get("task_id", "")
        task = task_manager.get_task(task_id)
        if not task:
            return json.dumps({"error": f"Task not found: {task_id}"})
        return json.dumps(task, ensure_ascii=False)

    def list_tasks_tool(self, args: dict) -> str:
        limit = args.get("limit", 10)
        tasks = task_manager.list_tasks(limit)
        return json.dumps({"tasks": tasks}, ensure_ascii=False)

    async def handle_websocket(self, request):
        if not verify_token(request):
            ws = web.WebSocketResponse()
            await ws.prepare(request)
            await ws.close(code=4001, message=b"Unauthorized")
            return ws

        ws = web.WebSocketResponse()
        await ws.prepare(request)
        self.ws_clients.add(ws)
        client_id = str(uuid.uuid4())[:8]
        print(f"[WS] 客户端连接: {client_id}, 总数: {len(self.ws_clients)}", file=sys.stderr)

        try:
            async for msg in ws:
                if msg.type == web.WSMsgType.TEXT:
                    try:
                        data = json.loads(msg.data)
                        if data.get("type") == "ping":
                            await ws.send_json({"type": "pong"})
                    except:
                        pass
        finally:
            self.ws_clients.discard(ws)
            print(f"[WS] 客户端断开: {client_id}", file=sys.stderr)
        return ws

    async def handle_http_post(self, request):
        if not verify_token(request):
            return web.json_response({"error": "Unauthorized"}, status=401)

        try:
            request_obj = await request.json()
            if request_obj.get("method") == "tools/call":
                result = await self.handle_call_tool(
                    request_obj["params"]["name"],
                    request_obj["params"].get("arguments", {})
                )
                response = {"jsonrpc": "2.0", "id": request_obj.get("id"),
                    "result": {"content": [{"type": "text", "text": result}]}}
            else:
                response = {"jsonrpc": "2.0", "id": request_obj.get("id"), "result": {}}
            return web.json_response(response)
        except Exception as e:
            return web.json_response({"error": str(e)})

    async def handle_index(self, request):
        return web.json_response({
            "name": self.name,
            "version": self.version,
            "description": "xiaozhi-esp32 MCP Server - 简化版",
            "auth": "Bearer Token required",
            "endpoints": {"http": "/mcp", "websocket": "/ws"},
            "tools": ["run_agent", "get_task", "list_tasks"]
        })

    async def run_http(self, host="0.0.0.0", port=9000):
        app = web.Application()
        app.router.add_get('/', self.handle_index)
        app.router.add_post('/mcp', self.handle_http_post)
        app.router.add_get('/ws', self.handle_websocket)

        print(f"Server: http://{host}:{port}", file=sys.stderr)
        print(f"WebSocket: ws://{host}:{port}/ws", file=sys.stderr)
        print(f"Token: {self.token}", file=sys.stderr)

        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host, port)
        await site.start()

async def main():
    server = OpenClawMCPServer()
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9000
    await server.run_http(port=port)
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())