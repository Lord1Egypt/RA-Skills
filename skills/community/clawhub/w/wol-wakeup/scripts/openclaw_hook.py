#!/usr/bin/env python3
"""
OpenClaw Internal Hook 服务 - 工作流引擎集成
接收 OpenClaw inbound 消息，优先匹配工作流，未匹配则放行给 AI

用法:
    python3 openclaw_hook.py [--port 8765] [--token <token>]
"""

import json
import sys
import os
import hashlib
import hmac
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import threading
import time

# 添加脚本目录到路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from message_handler import handle_message, check_timeouts
from workflow_engine import engine

# 配置
DEFAULT_PORT = 8765
DEFAULT_TOKEN = None  # 从环境变量或命令行参数读取
HOOK_LOG_FILE = SCRIPT_DIR.parent / "hook.log"

class HookLogger:
    """简单的文件日志"""
    def __init__(self, log_file):
        self.log_file = log_file
    
    def log(self, level, message):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        line = f"[{timestamp}] [{level}] {message}\n"
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(line)
    
    def info(self, message):
        self.log('INFO', message)
    
    def error(self, message):
        self.log('ERROR', message)
    
    def debug(self, message):
        self.log('DEBUG', message)

logger = HookLogger(HOOK_LOG_FILE)


def verify_token(token, request_token):
    """验证请求 token"""
    if not token:
        return True  # 未配置 token 时跳过验证
    return hmac.compare_digest(token, request_token)


class HookHandler(BaseHTTPRequestHandler):
    """HTTP Hook 处理器"""
    
    def log_message(self, format, *args):
        """覆盖默认日志，使用自定义 logger"""
        logger.info(f"HTTP: {format % args}")
    
    def send_json_response(self, status_code, data):
        """发送 JSON 响应"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def do_POST(self):
        """处理 POST 请求"""
        # 验证路径
        if urlparse(self.path).path != '/hook':
            self.send_json_response(404, {'error': 'Not found'})
            return
        
        # 验证 token
        auth_header = self.headers.get('Authorization', '')
        request_token = auth_header.replace('Bearer ', '') if auth_header.startswith('Bearer ') else ''
        
        if not verify_token(DEFAULT_TOKEN, request_token):
            self.send_json_response(401, {'error': 'Unauthorized'})
            logger.error('Token verification failed')
            return
        
        # 读取请求体
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            self.send_json_response(400, {'error': 'Empty request body'})
            return
        
        try:
            body = self.rfile.read(content_length)
            request_data = json.loads(body.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            self.send_json_response(400, {'error': f'Invalid JSON: {str(e)}'})
            logger.error(f'Invalid request body: {e}')
            return
        
        # 处理 inbound 消息
        self.handle_inbound_message(request_data)
    
    def handle_inbound_message(self, request_data):
        """处理 inbound 消息"""
        logger.info(f"Received inbound message: {json.dumps(request_data, ensure_ascii=False)[:200]}")
        
        # 提取消息内容
        event_type = request_data.get('event', 'inbound_message')
        if event_type != 'inbound_message':
            # 非 inbound 消息，放行
            self.send_json_response(200, {'handled': False, 'reason': 'Not an inbound message event'})
            return
        
        text = request_data.get('text', '')
        from_user = request_data.get('from', 'unknown')
        channel = request_data.get('channel', 'unknown')
        
        if not text:
            self.send_json_response(200, {'handled': False, 'reason': 'Empty message text'})
            return
        
        # 使用 from_user 作为 session ID
        session_id = from_user
        
        logger.info(f"Processing message from {from_user} on {channel}: '{text[:50]}...'")
        
        try:
            # 调用工作流引擎处理消息
            response = handle_message(text, session_id)
            
            if response:
                # 工作流已处理，返回响应
                logger.info(f"Workflow handled message, response: {response[:100]}...")
                self.send_json_response(200, {
                    'handled': True,
                    'response': response,
                    'workflow_type': 'wol',
                })
            else:
                # 工作流未匹配，放行给 AI
                logger.debug(f"Message not matched by workflow, passing to AI")
                self.send_json_response(200, {
                    'handled': False,
                    'reason': 'No workflow matched',
                })
        
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            # 出错时放行给 AI，避免阻塞消息
            self.send_json_response(200, {
                'handled': False,
                'reason': f'Error: {str(e)}',
            })
    
    def do_GET(self):
        """处理 GET 请求（健康检查）"""
        if urlparse(self.path).path == '/health':
            self.send_json_response(200, {
                'status': 'healthy',
                'active_sessions': len(engine.list_active_sessions()),
            })
        else:
            self.send_json_response(404, {'error': 'Not found'})


def periodic_timeout_check():
    """定期检查并清理超时会话"""
    while True:
        time.sleep(30)  # 每 30 秒检查一次
        try:
            timed_out = check_timeouts()
            if timed_out:
                logger.info(f"Cleaned up {len(timed_out)} timed-out sessions: {timed_out}")
        except Exception as e:
            logger.error(f"Error in timeout check: {e}")


def start_server(port, token):
    """启动 HTTP 服务器"""
    global DEFAULT_TOKEN
    DEFAULT_TOKEN = token
    
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, HookHandler)
    
    logger.info(f"Starting OpenClaw Hook Server on http://127.0.0.1:{port}")
    if token:
        logger.info("Token authentication enabled")
    else:
        logger.warning("WARNING: No token configured, authentication disabled!")
    
    # 启动超时检查线程
    timeout_thread = threading.Thread(target=periodic_timeout_check, daemon=True)
    timeout_thread.start()
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Server shutting down...")
        httpd.shutdown()


def generate_secure_token():
    """生成安全的随机 token"""
    return hashlib.sha256(os.urandom(32)).hexdigest()


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='OpenClaw Internal Hook Server')
    parser.add_argument('--port', type=int, default=DEFAULT_PORT, help=f'Port to listen on (default: {DEFAULT_PORT})')
    parser.add_argument('--token', type=str, default=None, help='Authentication token (default: env HOOK_TOKEN or None)')
    parser.add_argument('--generate-token', action='store_true', help='Generate and print a secure token')
    
    args = parser.parse_args()
    
    if args.generate_token:
        token = generate_secure_token()
        print(f"Generated secure token: {token}")
        print(f"\nAdd this to your openclaw.json:")
        print(json.dumps({
            "hooks": {
                "enabled": True,
                "token": token,
                "internal": {
                    "enabled": True,
                    "endpoint": f"http://127.0.0.1:{args.port}/hook"
                }
            }
        }, indent=2))
        return
    
    # 从环境变量获取 token（如果命令行未指定）
    token = args.token or os.environ.get('HOOK_TOKEN')
    
    # 确保日志目录存在
    HOOK_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    logger.info("=" * 60)
    logger.info("OpenClaw WorkFlow Hook Server")
    logger.info("=" * 60)
    
    start_server(args.port, token)


if __name__ == '__main__':
    main()
