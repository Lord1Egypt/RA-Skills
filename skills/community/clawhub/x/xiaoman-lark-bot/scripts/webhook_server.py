#!/usr/bin/env python3
"""
飞书 Webhook 消息接收服务
用法: python3 webhook_server.py
环境变量:
  LARK_APP_SECRET - 飞书应用密钥（用于签名验证）
  LARK_WEBHOOK_PORT - 服务端口（默认 19800）
"""
import os
import json
import hmac
import hashlib
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

APP_SECRET = os.environ.get("LARK_APP_SECRET", "")
PORT = int(os.environ.get("LARK_WEBHOOK_PORT", "19800"))

def verify_signature(timestamp, nonce, signature):
    """验证飞书签名"""
    if not APP_SECRET:
        return True  # 未配置密钥时跳过验证
    
    string = f"{timestamp}{nonce}{APP_SECRET}"
    expected = hashlib.sha1(string.encode()).hexdigest()
    return hmac.compare_digest(expected, signature)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """健康检查"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok"}).encode())
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode()
        
        try:
            data = json.loads(body)
        except:
            data = {}
        
        # 验证签名
        timestamp = self.headers.get('X-Lark-Request-Timestamp', '')
        nonce = self.headers.get('X-Lark-Request-Nonce', '')
        signature = self.headers.get('X-Lark-Signature', '')
        
        if not verify_signature(timestamp, nonce, signature):
            self.send_response(401)
            self.end_headers()
            self.wfile.write(json.dumps({"error": "invalid signature"}).encode())
            return
        
        # 处理不同类型的事件
        event_type = data.get("type")
        
        if event_type == "url_verification":
            # 验证 URL 有效性
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "challenge": data.get("challenge")
            }).encode())
            return
        
        if event_type == "event_callback":
            event = data.get("event", {})
            msg_type = event.get("msg_type")
            
            if msg_type == "text":
                # 处理文本消息
                message = event.get("message", {})
                text = message.get("text", {})
                content = text.get("content", "").strip()
                sender_id = message.get("sender_id", {}).get("user_id", "unknown")
                
                print(f"[收到消息] 用户 {sender_id}: {content}")
                
                # TODO: 在这里处理消息逻辑
                # 例如：调用 AI 处理并回复
                # self.reply_message(sender_id, "收到消息")
            
            elif msg_type == "image":
                # 处理图片消息
                print(f"[收到图片消息]")
            
            elif msg_type == "card":
                # 处理卡片消息
                print(f"[收到卡片消息]")
        
        # 响应成功
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "received"}).encode())
    
    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {format % args}")

def main():
    server = HTTPServer(('', PORT), Handler)
    print(f"🦉 Lark Webhook 服务启动于端口 {PORT}")
    print(f"   APP_SECRET: {'已配置' if APP_SECRET else '未配置'}")
    print(f"   按 Ctrl+C 停止")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n停止服务")
        server.shutdown()

if __name__ == '__main__':
    main()
