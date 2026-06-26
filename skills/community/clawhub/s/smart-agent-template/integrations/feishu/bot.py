#!/usr/bin/env python3
"""
飞书 Bot 主程序
基于 smart-agent-template 的多渠道 Agent 通信实现

架构：事件订阅模式（与 Telegram 轮询模式不同）
飞书通过 HTTP 回调推送事件，Bot 需要提供一个公网可访问的 Webhook URL
"""

import json
import logging
import sys
import hashlib
import hmac
import base64
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import config
from handlers import FeishuMessageHandlers

# 导入 Telegram 的 AI 适配器（复用）
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'telegram'))
from ai_adapter import create_ai_adapter

import asyncio

# 配置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# 全局 handlers 实例（HTTP server 回调需要）
_handlers: FeishuMessageHandlers = None


def verify_feishu_signature(timestamp: str, nonce: str, encrypt_key: str, body: str, signature: str) -> bool:
    """验证飞书请求签名"""
    if not encrypt_key:
        return True  # 未配置加密则跳过验证
    
    content = timestamp + nonce + encrypt_key + body
    sig = hashlib.sha256(content.encode()).hexdigest()
    return sig == signature


class FeishuWebhookHandler(BaseHTTPRequestHandler):
    """飞书 Webhook 处理器"""
    
    def log_message(self, format, *args):
        logger.info(format % args)
    
    def do_POST(self):
        try:
            # 读取请求体
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            
            # 验证签名
            timestamp = self.headers.get('X-Lark-Request-Timestamp', '')
            nonce = self.headers.get('X-Lark-Request-Nonce', '')
            signature = self.headers.get('X-Lark-Signature', '')
            
            if config.feishu.encrypt_key:
                if not verify_feishu_signature(
                    timestamp, nonce, config.feishu.encrypt_key, body, signature
                ):
                    self._send_response(401, {"error": "Invalid signature"})
                    return
            
            # 解析事件
            event_data = json.loads(body)
            
            # 处理 URL 验证挑战（飞书订阅验证）
            if event_data.get('type') == 'url_verification':
                challenge = event_data.get('challenge', '')
                token = event_data.get('token', '')
                
                if token != config.feishu.verification_token:
                    self._send_response(401, {"error": "Invalid token"})
                    return
                
                self._send_response(200, {"challenge": challenge})
                return
            
            # 处理消息事件
            event_type = event_data.get('header', {}).get('event_type', '')
            
            if event_type == 'im.message.receive_v1':
                # 异步处理消息
                response = asyncio.run(_handlers.handle_message(event_data))
                
                # 获取回复目标
                message = event_data.get('event', {}).get('message', {})
                chat_id = message.get('chat_id', '')
                
                # 发送回复
                self._send_feishu_message(chat_id, response.get('text', ''))
                self._send_response(200, {"code": 0, "msg": "ok"})
            else:
                logger.info(f"Unhandled event type: {event_type}")
                self._send_response(200, {"code": 0, "msg": "ok"})
                
        except json.JSONDecodeError:
            self._send_response(400, {"error": "Invalid JSON"})
        except Exception as e:
            logger.error(f"Error handling request: {e}", exc_info=True)
            self._send_response(500, {"error": "Internal error"})
    
    def _send_response(self, status_code: int, data: dict):
        """发送 HTTP 响应"""
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)
    
    def _send_feishu_message(self, chat_id: str, text: str):
        """调用飞书 API 发送消息"""
        try:
            import urllib.request
            
            # 获取 access token
            token_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
            token_data = json.dumps({
                "app_id": config.feishu.app_id,
                "app_secret": config.feishu.app_secret
            }).encode('utf-8')
            
            token_req = urllib.request.Request(
                token_url,
                data=token_data,
                headers={'Content-Type': 'application/json; charset=utf-8'}
            )
            with urllib.request.urlopen(token_req) as resp:
                token_result = json.loads(resp.read())
            
            access_token = token_result.get('tenant_access_token', '')
            if not access_token:
                logger.error("Failed to get access token")
                return
            
            # 发送消息
            msg_url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
            msg_data = json.dumps({
                "receive_id": chat_id,
                "content": json.dumps({"text": text}),
                "msg_type": "text"
            }).encode('utf-8')
            
            msg_req = urllib.request.Request(
                msg_url,
                data=msg_data,
                headers={
                    'Content-Type': 'application/json; charset=utf-8',
                    'Authorization': f'Bearer {access_token}'
                }
            )
            with urllib.request.urlopen(msg_req) as resp:
                result = json.loads(resp.read())
            
            if result.get('code') != 0:
                logger.error(f"Failed to send message: {result}")
            else:
                logger.info(f"Message sent to chat {chat_id}")
                
        except Exception as e:
            logger.error(f"Error sending Feishu message: {e}", exc_info=True)


def main():
    global _handlers
    
    print("=" * 60)
    print("🚀 Smart Agent 飞书 Bot")
    print("=" * 60)
    
    # 验证配置
    try:
        config.validate()
        print(f"✅ 配置验证通过")
        print(f"🔑 App ID: {config.feishu.app_id}")
        print(f"🤖 AI Engine: {config.ai.engine}")
        print(f"📦 Model: {config.ai.model}")
    except ValueError as e:
        print(f"❌ 配置错误: {e}")
        print("\n请检查环境变量配置:")
        print("  - FEISHU_APP_ID")
        print("  - FEISHU_APP_SECRET")
        print("  - FEISHU_VERIFICATION_TOKEN")
        print("  - FEISHU_ENCRYPT_KEY (可选)")
        print("  - AI_ENGINE (openai/claude/deepseek/ollama)")
        print("  - <ENGINE>_API_KEY (如果需要)")
        sys.exit(1)
    
    # 创建 AI 适配器
    try:
        ai_adapter = create_ai_adapter(
            engine=config.ai.engine,
            api_key=config.ai.api_key,
            model=config.ai.model,
            base_url=config.ai.base_url
        )
        print(f"✅ AI 适配器创建成功")
    except Exception as e:
        print(f"❌ AI 适配器创建失败: {e}")
        sys.exit(1)
    
    # 创建消息处理器
    _handlers = FeishuMessageHandlers(ai_adapter, storage_dir="./data/memory")
    
    # 启动 HTTP 服务器
    server = HTTPServer(('0.0.0.0', config.feishu.port), FeishuWebhookHandler)
    
    print("=" * 60)
    print(f"✅ 飞书 Bot 已启动")
    print(f"🌐 监听端口: {config.feishu.port}")
    print(f"📡 Webhook URL: http://your-domain.com:{config.feishu.port}/")
    print(f"   （需要配置到飞书开放平台 → 事件订阅 → 请求 URL）")
    print(f"   （本地开发可用 ngrok: ngrok http {config.feishu.port}）")
    print("按 Ctrl+C 停止")
    print("=" * 60)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n⏹️  Bot 已停止")
        server.shutdown()


if __name__ == '__main__':
    main()
