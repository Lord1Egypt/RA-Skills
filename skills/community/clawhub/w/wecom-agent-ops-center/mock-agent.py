#!/usr/bin/env python3
"""
Mock Agent — 用于端到端测试
启动：python3 mock-agent.py
端口：3001
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import datetime

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 兼容 self.path 可能被代理改成完整 URL 的情况
        path = self.path.split('?')[0]
        # 如果是完整 URL（如 http://127.0.0.1:3001/chat），提取路径部分
        if '://' in path:
            from urllib.parse import urlparse
            path = urlparse(path).path or '/'
        print(f'[MockAgent] POST {self.path} → 解析路径: {path}')

        if path == '/chat':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))
            user_msg = data.get('content', '')[:100]

            print(f'[MockAgent] 收到消息: {user_msg}')

            reply = {
                'content': (
                    '✅ Mock Agent 已收到你的消息！\n\n'
                    f'你发送的内容：{user_msg or "[空内容]"}\n\n'
                    f'当前时间：{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\n'
                    '（这是模拟回复，真实 Agent 会返回 AI 生成的内容）'
                ),
                'msg_type': 'text',
            }

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(reply, ensure_ascii=False).encode('utf-8'))
            print(f'[MockAgent] 已回复')
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Not found', 'path': self.path}).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def log_message(self, format, *args):
        pass  # 禁用默认日志

if __name__ == '__main__':
    server = HTTPServer(('127.0.0.1', 3001), Handler)
    print('[MockAgent] 启动成功，监听 http://127.0.0.1:3001/chat')
    print('[MockAgent] 等待 Connector 调用...')
    server.serve_forever()
