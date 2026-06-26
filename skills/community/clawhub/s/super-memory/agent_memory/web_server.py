#!/usr/bin/env python3
from __future__ import annotations
"""
web_server.py - Agent Memory System Web 服务器

提供 Web 界面和 API 接口，支持：
1. 知识库投喂（文件上传）
2. 格式转换
3. LLM 对话
4. 记忆管理
5. 实时状态监控

启动：
    python web_server.py
    # 访问 http://localhost:8080
"""

import os
import sys
import json
import logging
import hmac
import threading
import time
import urllib.parse
import asyncio
from collections import defaultdict
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
from datetime import datetime

# 添加项目根目录到 Python 路径
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_DIR)

from openclaw_plugin.knowledge_feeder import KnowledgeFeeder, FeederChatWindow
from openclaw_plugin.format_converter import FormatConverter, ConversionManager
from .memory_system import AgentMemory
from .cli import _check_model_server
from .async_manager import get_async_manager, process_file_async, llm_call_async
from .permission_manager import get_permission_manager, PERMISSIONS, DEFAULT_ROLES
from monitoring import get_monitoring_system
from .summarizer import get_summarizer
from .personalization import get_personalization_manager
from plugin_system import get_plugin_system  # deprecated — compatibility shim, will be removed in v12
from .llm_client import LLMClient

# 配置日志
from .logging_config import configure_logging
configure_logging(level="INFO", fmt="detailed")
logger = logging.getLogger(__name__)

_MAX_REQUEST_SIZE = 10 * 1024 * 1024  # 10MB 单请求上限


class SimpleRateLimiter:
    """Simple in-memory rate limiter for web server."""

    def __init__(self, max_requests=100, window_seconds=60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests = defaultdict(list)

    def is_allowed(self, key: str) -> bool:
        now = time.time()
        # Clean old entries
        self._requests[key] = [
            t for t in self._requests[key]
            if now - t < self.window_seconds
        ]
        if len(self._requests[key]) >= self.max_requests:
            return False
        self._requests[key].append(now)
        return True


_rate_limiter = SimpleRateLimiter()


def _validate_file_path(path_str: str, allowed_dirs: list = None) -> 'pathlib.Path':
    import pathlib
    if not path_str:
        raise ValueError("Empty path")
    if '\0' in path_str:
        raise ValueError("Null byte in path")
    parsed = pathlib.PurePosixPath(path_str) if '/' in path_str else pathlib.PureWindowsPath(path_str)
    if parsed.is_absolute():
        raise ValueError(f"Absolute paths not allowed: {path_str}")
    resolved = pathlib.Path(path_str).resolve()
    if '..' in pathlib.PurePosixPath(path_str).parts and '..' in pathlib.PureWindowsPath(path_str).parts:
        raise ValueError(f"Path traversal detected: {path_str}")
    if allowed_dirs:
        cwd = pathlib.Path.cwd()
        allowed_resolved = [cwd / d for d in allowed_dirs]
        if not any(str(resolved).startswith(str(a.resolve())) for a in allowed_resolved):
            raise ValueError(f"Path outside allowed directories: {path_str}")
    return resolved


# 加载配置
def load_config():
    """加载配置文件"""
    config_file = os.path.join(PROJECT_DIR, "config.json")
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
    return {}

config = load_config()

# 全局实例
feeder = None
converter = None
memory_system = None
chat_window = None
async_manager = None
permission_manager = None
monitoring_system = None
summarizer = None
personalization_manager = None
plugin_system = None





class RequestHandler(BaseHTTPRequestHandler):
    """HTTP 请求处理器（支持 API Key 认证）"""

    # 静态文件路径和健康检查端点不需要认证
    _AUTH_EXEMPT_PATHS = {"/", "/styles.css", "/app.js", "/api/status"}
    _RATE_LIMIT_EXEMPT_PATHS = {"/", "/styles.css", "/app.js", "/api/status"}

    def _check_rate_limit(self):
        """Check rate limit for the client. Returns True if allowed, False if rate limited."""
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        if path in self._RATE_LIMIT_EXEMPT_PATHS:
            return True
        client_key = self.client_address[0] if self.client_address else "unknown"
        if not _rate_limiter.is_allowed(client_key):
            error_body = json.dumps({"error": "请求过于频繁", "message": "速率限制已超出，请稍后重试。"}).encode('utf-8')
            self.send_response(429)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.send_header('Content-length', len(error_body))
            self.end_headers()
            self.wfile.write(error_body)
            return False
        return True

    def _check_api_key(self):
        """检查 API Key 认证。

        从请求头 X-API-Key 或 URL 参数 api_key 获取密钥。
        如果环境变量 AGENT_MEMORY_API_KEY 已设置，则所有请求必须携带正确的 API Key。
        如果未设置 AGENT_MEMORY_API_KEY，则跳过认证（开发模式）。

        Returns:
            True 表示认证通过或无需认证，False 表示认证失败（已发送 401 响应）。
        """
        expected_key = os.environ.get("AGENT_MEMORY_API_KEY", "")
        if not expected_key:
            # 未设置 API Key → 开发模式，跳过认证
            return True

        # 从请求头获取
        provided_key = self.headers.get("X-API-Key", "")

        if hmac.compare_digest(provided_key, expected_key):
            return True

        # 认证失败：返回 401 JSON 响应
        error_body = json.dumps({"error": "未授权", "message": "API Key 无效或缺失"}).encode('utf-8')
        self.send_response(401)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Content-length', len(error_body))
        self.end_headers()
        self.wfile.write(error_body)

        client_ip = self.client_address[0] if self.client_address else "?"
        logger.warning(f"API Key 认证失败: client={client_ip} path={self.path}")
        return False

    def do_GET(self):
        """处理 GET 请求"""
        if not self._check_rate_limit():
            return

        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path

        # 静态文件和状态端点豁免认证
        if path in self._AUTH_EXEMPT_PATHS:
            pass  # 继续处理，不检查认证
        elif not self._check_api_key():
            return

        if path == "/":
            self.send_static_file("index.html")
        elif path == "/styles.css":
            self.send_static_file("styles.css")
        elif path == "/app.js":
            self.send_static_file("app.js")
        elif path == "/api/status":
            self.handle_status()
        elif path == "/api/stats":
            self.handle_stats()
        elif path == "/api/conversions":
            self.handle_conversions()
        elif path == "/api/tools":
            self.handle_tools()
        elif path == "/api/monitoring/system":
            self.handle_monitoring_system()
        elif path == "/api/monitoring/health":
            self.handle_monitoring_health()
        elif path == "/api/monitoring/metrics":
            self.handle_monitoring_metrics()
        elif path == "/api/monitoring/alerts":
            self.handle_monitoring_alerts()
        elif path == "/api/monitoring/summary":
            self.handle_monitoring_summary()
        elif path == "/api/summary":
            self.handle_summary()
        elif path == "/api/personalization/settings":
            self.handle_personalization_settings()
        elif path == "/api/personalization/interface":
            self.handle_personalization_interface()
        elif path == "/api/personalization/system":
            self.handle_personalization_system()
        elif path == "/api/personalization/search":
            self.handle_personalization_search()
        elif path == "/api/personalization/memory":
            self.handle_personalization_memory()
        elif path == "/api/personalization/notifications":
            self.handle_personalization_notifications()
        elif path == "/api/personalization/llm":
            self.handle_personalization_llm()
        elif path == "/api/plugins":
            self.handle_plugins_list()
        elif path == "/api/plugins/info":
            self.handle_plugin_info()
        elif path == "/api/plugins/execute":
            self.handle_plugin_execute()
        elif path == "/api/plugins/config":
            self.handle_plugin_config()
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        """处理 POST 请求"""
        if not self._check_rate_limit():
            return

        if not self._check_api_key():
            return

        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > _MAX_REQUEST_SIZE:
            self.send_error(413, "Request Entity Too Large")
            return

        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path

        if path == "/api/feed":
            self.handle_feed()
        elif path == "/api/convert":
            self.handle_convert()
        elif path == "/api/chat":
            self.handle_chat()
        elif path == "/api/memory":
            self.handle_memory()
        elif path == "/api/export":
            self.handle_export()
        elif path == "/api/tool":
            self.handle_tool()
        else:
            self.send_error(404, "Not Found")

    def send_static_file(self, filename):
        """发送静态文件"""
        filename = os.path.basename(filename)
        file_path = os.path.join(PROJECT_DIR, "web", filename)
        real_path = os.path.realpath(file_path)
        web_dir = os.path.realpath(os.path.join(PROJECT_DIR, "web"))
        if not real_path.startswith(web_dir):
            self.send_error(403, "Forbidden")
            return
        if not os.path.exists(file_path):
            self.send_error(404, "File Not Found")
            return

        try:
            with open(file_path, 'rb') as f:
                content = f.read()

            self.send_response(200)
            if filename.endswith('.html'):
                self.send_header('Content-type', 'text/html')
            elif filename.endswith('.css'):
                self.send_header('Content-type', 'text/css')
            elif filename.endswith('.js'):
                self.send_header('Content-type', 'application/javascript')
            self.send_header('Content-length', len(content))
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            logger.error(f"Internal error: {e}", exc_info=True); self.send_error(500, "Internal Server Error")

    def handle_status(self):
        """处理状态请求"""
        llm_available = os.environ.get("OPENAI_API_KEY") is not None
        stats = feeder.get_statistics() if feeder else {}

        response = {
            "status": "ok",
            "llm_available": llm_available,
            "stats": stats,
            "timestamp": datetime.now().isoformat()
        }

        self.send_json_response(response)

    def handle_stats(self):
        """处理统计请求"""
        if not feeder:
            self.send_error(500, "Feeder not initialized")
            return

        stats = feeder.get_statistics()
        self.send_json_response({"status": "ok", "data": stats})

    def handle_conversions(self):
        """处理转换格式请求"""
        if not converter:
            self.send_error(500, "Converter not initialized")
            return

        conversions = converter.get_supported_conversions()
        formatted = []
        for from_format, to_format in conversions:
            formatted.append({
                "from": from_format.value,
                "to": to_format.value
            })

        self.send_json_response({"status": "ok", "data": formatted})

    def handle_feed(self):
        """处理文件投喂"""
        if not feeder:
            self.send_error(500, "Feeder not initialized")
            return

        try:
            # 检查是否是文件上传（multipart/form-data）
            content_type = self.headers.get('Content-Type', '')
            if 'multipart/form-data' in content_type:
                # 处理文件上传
                import cgi
                import tempfile
                import os
                import zipfile

                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )

                if 'file' not in form:
                    self.send_error(400, "No file uploaded")
                    return

                fileitem = form['file']
                if not fileitem.file:
                    self.send_error(400, "Empty file")
                    return

                # 保存上传的文件到临时目录
                temp_dir = tempfile.mkdtemp()
                safe_filename = os.path.basename(fileitem.filename)
                temp_path = os.path.join(temp_dir, safe_filename)

                with open(temp_path, 'wb') as f:
                    f.write(fileitem.file.read())

                results = []

                # 如果是压缩包，解压并处理
                if temp_path.endswith('.zip'):
                    extract_dir = os.path.join(temp_dir, 'extracted')
                    os.makedirs(extract_dir)

                    try:
                        with zipfile.ZipFile(temp_path, 'r') as zip_ref:
                            _MAX_ZIP_ENTRIES = 1000
                            _MAX_ZIP_TOTAL_SIZE = 50 * 1024 * 1024
                            if len(zip_ref.infolist()) > _MAX_ZIP_ENTRIES:
                                self.send_error(413, "Too many files in zip")
                                return
                            total_size = sum(i.file_size for i in zip_ref.infolist())
                            if total_size > _MAX_ZIP_TOTAL_SIZE:
                                self.send_error(413, "Zip contents too large")
                                return
                            for info in zip_ref.infolist():
                                if info.filename.startswith('/') or '..' in info.filename:
                                    continue
                                zip_ref.extract(info, extract_dir)

                        # 处理解压的文件
                        for root, dirs, files in os.walk(extract_dir):
                            for file in files:
                                file_path = os.path.join(root, file)
                                try:
                                    result = feeder.feed_file(file_path)
                                    results.append({
                                        "file": file,
                                        "success": result.success,
                                        "message": result.message if hasattr(result, 'message') else str(result)
                                    })
                                except Exception as e:
                                    results.append({
                                        "file": file,
                                        "success": False,
                                        "message": str(e)
                                    })
                    except zipfile.BadZipFile:
                        self.send_error(400, "Invalid zip file")
                        return
                else:
                    # 非压缩包文件直接处理
                    result = feeder.feed_file(temp_path)
                    results.append({
                        "file": fileitem.filename,
                        "success": result.success,
                        "message": result.message if hasattr(result, 'message') else str(result)
                    })

                # 清理临时文件
                import shutil
                shutil.rmtree(temp_dir)

                self.send_json_response({
                    "status": "ok",
                    "data": {
                        "message": f"成功处理 {len(results)} 个文件",
                        "files": results
                    }
                })
                return
            else:
                # 处理 JSON 格式的投喂
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data)

                if data.get('type') == 'text':
                    result = feeder.feed_text(data.get('content', ''))
                elif data.get('type') == 'url':
                    result = feeder.feed_url(data.get('url', ''))
                else:
                    self.send_error(400, "Invalid feed type")
                    return

                self.send_json_response({
                    "status": "ok" if result.success else "error",
                    "data": {
                        "content_type": result.content_type.value,
                        "original_length": result.original_length,
                        "purified_length": result.purified_length,
                        "content": result.content[:200] + "..." if len(result.content) > 200 else result.content,
                        "error": result.error
                    }
                })

        except Exception as e:
            logger.error(f"Internal error: {e}", exc_info=True); self.send_error(500, "Internal Server Error")

    def handle_convert(self):
        """处理格式转换"""
        if not feeder:
            self.send_error(500, "Feeder not initialized")
            return

        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            input_path = data.get('input')
            output_path = data.get('output')

            if not input_path or not output_path:
                self.send_error(400, "Missing input or output path")
                return

            try:
                input_path = str(_validate_file_path(input_path, allowed_dirs=['data', 'uploads', 'examples']))
                output_path = str(_validate_file_path(output_path, allowed_dirs=['data', 'uploads', 'output']))
            except ValueError as e:
                self.send_error(400, f"Invalid path: {e}")
                return

            result = feeder.convert_format(input_path, output_path)

            self.send_json_response({
                "status": "ok" if result.success else "error",
                "data": {
                    "input_format": result.input_format.value,
                    "output_format": result.output_format.value,
                    "input_file": result.input_file,
                    "output_file": result.output_file,
                    "conversion_time": result.conversion_time,
                    "error": result.error
                }
            })

        except Exception as e:
            logger.error(f"Internal error: {e}", exc_info=True); self.send_error(500, "Internal Server Error")

    def handle_chat(self):
        """处理 LLM 对话"""
        if not chat_window:
            self.send_error(500, "Chat window not initialized")
            return

        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            message = data.get('message')
            if not message:
                self.send_error(400, "Missing message")
                return

            response = chat_window.chat(message)

            self.send_json_response({
                "status": "ok",
                "data": {
                    "content": response['content'],
                    "type": response['type']
                }
            })

        except Exception as e:
            logger.error(f"Internal error: {e}", exc_info=True); self.send_error(500, "Internal Server Error")

    def handle_memory(self):
        """处理记忆管理"""
        if not memory_system:
            self.send_error(500, "Memory system not initialized")
            return

        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            action = data.get('action')

            if action == 'add':
                result = memory_system.remember(
                    content=data.get('content', ''),
                    importance="medium",
                    topics=["user"]
                )
                success = result.get("memory_result", {}).get("written", False)
                self.send_json_response({
                    "status": "ok" if success else "error",
                    "data": {"success": success}
                })

            elif action == 'search':
                results = memory_system.recall(
                    query=data.get('query', ''),
                    top_k=5
                )
                self.send_json_response({
                    "status": "ok",
                    "data": results
                })

            else:
                self.send_error(400, "Invalid action")

        except Exception as e:
            logger.error(f"Internal error: {e}", exc_info=True); self.send_error(500, "Internal Server Error")

    def handle_export(self):
        """处理导出请求"""
        if not feeder:
            self.send_error(500, "Feeder not initialized")
            return

        try:
            md_content = feeder.export_as_markdown()
            export_path = os.path.join(PROJECT_DIR, f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
            with open(export_path, 'w', encoding='utf-8') as f:
                f.write(md_content)

            self.send_json_response({
                "status": "ok",
                "data": {"export_path": export_path}
            })

        except Exception as e:
            logger.error(f"Internal error: {e}", exc_info=True); self.send_error(500, "Internal Server Error")

    def handle_tools(self):
        """处理工具列表请求"""
        tools = [
            {
                "category": "核心记忆",
                "tools": [
                    {"id": "remember", "name": "写入记忆", "description": "向记忆系统写入新内容", "hint": "用于记录重要信息、决策、经验等"},
                    {"id": "recall", "name": "检索记忆", "description": "根据关键词检索记忆", "hint": "快速找到相关的记忆内容"},
                    {"id": "context", "name": "组装上下文", "description": "为对话组装相关记忆", "hint": "为当前对话提供相关背景信息"},
                    {"id": "stats", "name": "查看统计", "description": "查看记忆系统统计信息", "hint": "了解记忆系统的整体状态"},
                    {"id": "maintain", "name": "执行维护", "description": "执行记忆系统维护", "hint": "清理重复、修复矛盾、分析衰减"},
                    {"id": "compress", "name": "压缩记忆", "description": "压缩记忆内容", "hint": "减少存储空间使用"},
                    {"id": "graph", "name": "生成图谱", "description": "生成记忆关系图谱", "hint": "可视化记忆之间的关联关系"},
                    {"id": "export", "name": "导出记忆", "description": "导出记忆为 Markdown", "hint": "将记忆内容导出为可读格式"}
                ]
            },
            {
                "category": "格式转换",
                "tools": [
                    {"id": "convert", "name": "格式转换", "description": "转换文件格式", "hint": "支持 PDF、Word、Excel 等格式转换"}
                ]
            },
            {
                "category": "记忆蒸馏",
                "tools": [
                    {"id": "distill", "name": "执行蒸馏", "description": "执行记忆蒸馏", "hint": "将零散记忆提炼为结构化知识"},
                    {"id": "encyclopedia", "name": "个人百科", "description": "查看个人百科", "hint": "浏览提炼后的知识库"},
                    {"id": "entities", "name": "知识实体", "description": "查看知识实体", "hint": "查看系统识别的知识实体"},
                    {"id": "topic-summaries", "name": "主题摘要", "hint": "查看各个主题的摘要信息", "description": "查看主题摘要"}
                ]
            },
            {
                "category": "时间旅行",
                "tools": [
                    {"id": "snapshot", "name": "创建快照", "description": "创建记忆快照", "hint": "保存特定时间点的记忆状态"},
                    {"id": "snapshots", "name": "列出快照", "description": "列出所有快照", "hint": "查看所有已创建的快照"},
                    {"id": "diff", "name": "对比差异", "description": "对比两个时间点的差异", "hint": "了解一段时间内的记忆变化"},
                    {"id": "blame", "name": "追溯来源", "description": "追溯记忆来源", "hint": "了解记忆的产生和演变过程"}
                ]
            },
            {
                "category": "自我系统",
                "tools": [
                    {"id": "self", "name": "自我状态", "description": "查看自我状态仪表盘", "hint": "了解 Agent 的当前状态和情绪"},
                    {"id": "mood", "name": "内在状态", "description": "查看内在状态", "hint": "详细了解 Agent 的情绪和动机状态"},
                    {"id": "gaps", "name": "知识空白", "description": "查看知识空白", "hint": "发现需要探索的知识领域"},
                    {"id": "reflect", "name": "自我反思", "description": "查看自我反思历史", "hint": "查看 Agent 的自我反思记录"},
                    {"id": "confidence", "name": "置信度", "description": "查看置信度历史", "hint": "了解 Agent 对不同主题的置信度"}
                ]
            },
            {
                "category": "数字孪生",
                "tools": [
                    {"id": "persona", "name": "人格画像", "description": "构建数字孪生人格画像", "hint": "生成 Agent 的人格特征画像"},
                    {"id": "roles", "name": "角色管理", "description": "管理角色模板", "hint": "创建和管理不同的角色模板"},
                    {"id": "whoami", "name": "我是谁", "description": "第一人称自我叙述", "hint": "查看 Agent 的自我认知"},
                    {"id": "identity", "name": "身份画像", "description": "查看身份画像", "hint": "详细了解 Agent 的身份特征"}
                ]
            }
        ]
        
        self.send_json_response({"status": "ok", "data": tools})

    def handle_tool(self):
        """处理工具执行请求"""
        if not memory_system:
            self.send_error(500, "Memory system not initialized")
            return

        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            tool_id = data.get('tool_id')
            params = data.get('params', {})

            if not tool_id:
                self.send_error(400, "Missing tool_id")
                return

            # 执行工具
            result = self._execute_tool(tool_id, params)

            self.send_json_response({
                "status": "ok" if result.get('success', True) else "error",
                "data": result
            })

        except Exception as e:
            logger.error(f"Internal error: {e}", exc_info=True); self.send_error(500, "Internal Server Error")

    def _execute_tool(self, tool_id, params):
        """执行工具"""
        try:
            if tool_id == "remember":
                result = memory_system.remember(
                    content=params.get('content', ''),
                    importance=params.get('importance', 'medium'),
                    topics=params.get('topics', None),
                    nature=params.get('nature', None),
                    force=params.get('force', False)
                )
                return {"success": result.get('written', False), "data": result}

            elif tool_id == "recall":
                result = memory_system.recall(
                    query=params.get('query', ''),
                    topic=params.get('topic', None),
                    importance=params.get('importance', None),
                    significance=params.get('significance', None),
                    limit=params.get('limit', 10)
                )
                return {"success": True, "data": result}

            elif tool_id == "context":
                ctx = memory_system.build_context(
                    query=params.get('query', ''),
                    max_tokens=params.get('max_tokens', 1500),
                    style=params.get('style', 'structured')
                )
                return {"success": True, "data": {"context": ctx}}

            elif tool_id == "stats":
                stats = memory_system.get_stats()
                return {"success": True, "data": stats}

            elif tool_id == "maintain":
                results = {}
                dedup_result = memory_system.deduplicate()
                results["dedup"] = {
                    "scanned": dedup_result.get("total_scanned", 0),
                    "found": dedup_result.get("duplicates_found", 0),
                }
                heal_result = memory_system.self_heal()
                results["self_heal"] = {
                    "contradictions": len(heal_result.get("contradictions", [])),
                    "outdated": len(heal_result.get("outdated", [])),
                    "healed": heal_result.get("importance_healed", 0),
                    "total": heal_result.get("total_issues", 0),
                }
                decay_result = memory_system.analyze_decay()
                results["decay"] = {
                    "total": decay_result.get("total", 0),
                    "needs_action": len(decay_result.get("needs_action", [])),
                    "summary": decay_result.get("summary", ""),
                }
                return {"success": True, "data": results}

            elif tool_id == "distill":
                result = memory_system.distill(force=params.get('force', False))
                return {"success": True, "data": result}

            elif tool_id == "encyclopedia":
                if params.get('export'):
                    try:
                        export_path = str(_validate_file_path(params['export'], allowed_dirs=['data', 'output']))
                    except ValueError as e:
                        return {"success": False, "error": f"无效的导出路径: {e}"}
                    path = memory_system.export_encyclopedia(export_path)
                    return {"success": True, "data": {"exported": path}}
                elif params.get('search'):
                    results = memory_system.search_encyclopedia(params['search'])
                    return {"success": True, "data": results}
                else:
                    entries = memory_system.get_encyclopedia(category=params.get('category'))
                    return {"success": True, "data": entries}

            elif tool_id == "self":
                # 简化的自我状态
                state = memory_system.motivation.state
                profile = memory_system.narrative.build_identity_profile()
                gaps = memory_system.motivation.detect_knowledge_gaps()
                
                return {
                    "success": True,
                    "data": {
                        "mood": state.mood_summary,
                        "emoji": state.mood_emoji,
                        "profile": profile,
                        "gaps": gaps[:3],
                        "state": state.to_dict()
                    }
                }

            elif tool_id == "persona":
                profile = memory_system.build_persona()
                return {"success": True, "data": profile}

            elif tool_id == "whoami":
                whoami = memory_system.narrative.whoami()
                return {"success": True, "data": {"narrative": whoami}}

            elif tool_id == "identity":
                identity = memory_system.narrative.build_identity_profile()
                return {"success": True, "data": identity}

            elif tool_id == "roles":
                roles = memory_system.list_roles()
                return {"success": True, "data": roles}

            elif tool_id == "convert":
                input_file = params.get('input')
                output_file = params.get('output')
                if not input_file or not output_file:
                    return {"success": False, "error": "缺少输入或输出文件路径"}
                try:
                    input_file = str(_validate_file_path(input_file, allowed_dirs=['data', 'uploads', 'examples']))
                    output_file = str(_validate_file_path(output_file, allowed_dirs=['data', 'uploads', 'output']))
                except ValueError as e:
                    return {"success": False, "error": f"无效路径: {e}"}
                result = converter.convert(input_file, output_file)
                return {"success": True, "data": result}

            elif tool_id == "snapshot":
                name = params.get('name', f'snapshot_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
                result = memory_system.take_snapshot(name)
                return {"success": True, "data": result}

            elif tool_id == "snapshots":
                snapshots = memory_system.list_snapshots()
                return {"success": True, "data": snapshots}

            elif tool_id == "diff":
                snapshot1 = params.get('snapshot1')
                snapshot2 = params.get('snapshot2')
                if not snapshot1 or not snapshot2:
                    return {"success": False, "error": "缺少快照ID"}
                result = memory_system.diff_memories(from_snapshot=snapshot1, to_snapshot=snapshot2)
                return {"success": True, "data": result}

            elif tool_id == "blame":
                memory_id = params.get('memory_id')
                if not memory_id:
                    return {"success": False, "error": "缺少记忆ID"}
                result = memory_system.blame_memory(memory_id)
                return {"success": True, "data": result}

            elif tool_id == "compress":
                result = memory_system.compress()
                return {"success": True, "data": result}

            elif tool_id == "graph":
                result = memory_system.generate_graph()
                return {"success": True, "data": result}

            elif tool_id == "export":
                path = memory_system.export_encyclopedia()
                return {"success": True, "data": {"exported": path}}

            elif tool_id == "entities":
                category = params.get('category')
                # 使用百科搜索作为替代
                entities = memory_system.search_encyclopedia(category or "")
                return {"success": True, "data": entities}

            elif tool_id == "topic-summaries":
                # 使用百科条目作为替代
                summaries = memory_system.get_encyclopedia()
                return {"success": True, "data": summaries}

            elif tool_id == "mood":
                state = memory_system.motivation.state
                return {"success": True, "data": state.to_dict()}

            elif tool_id == "gaps":
                gaps = memory_system.motivation.detect_knowledge_gaps()
                return {"success": True, "data": gaps}

            elif tool_id == "reflect":
                # 使用元认知引擎的反思功能作为替代
                result = memory_system.meta_recall(query="自我反思")
                return {"success": True, "data": result.get("reflections", [])}

            elif tool_id == "confidence":
                # 使用自我模型的统计信息作为替代
                stats = memory_system.self_model.get_stats()
                return {"success": True, "data": stats}

            else:
                return {"success": False, "error": f"工具未实现: {tool_id}"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def send_json_response(self, data):
        """发送 JSON 响应"""
        json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Content-length', len(json_data))
        self.end_headers()
        self.wfile.write(json_data)

    def handle_monitoring_system(self):
        """处理系统状态监控请求"""
        global monitoring_system
        if not monitoring_system:
            self.send_error(500, "Monitoring system not initialized")
            return

        try:
            system_status = monitoring_system.get_system_status()
            self.send_json_response({"status": "ok", "data": system_status})
        except Exception as e:
            logger.error(f"Internal error: {e}", exc_info=True); self.send_error(500, "Internal Server Error")

    def handle_monitoring_health(self):
        """处理健康状态监控请求"""
        global monitoring_system
        if not monitoring_system:
            self.send_error(500, "Monitoring system not initialized")
            return

        try:
            health_status = monitoring_system.check_health()
            self.send_json_response({"status": "ok", "data": health_status})
        except Exception as e:
            logger.error(f"Internal error: {e}", exc_info=True); self.send_error(500, "Internal Server Error")

    def handle_monitoring_metrics(self):
        """处理性能指标监控请求"""
        global monitoring_system
        if not monitoring_system:
            self.send_error(500, "Monitoring system not initialized")
            return

        try:
            metrics = monitoring_system.get_metrics()
            self.send_json_response({"status": "ok", "data": metrics})
        except Exception as e:
            logger.error(f"Internal error: {e}", exc_info=True); self.send_error(500, "Internal Server Error")

    def handle_monitoring_alerts(self):
        """处理异常警报监控请求"""
        global monitoring_system
        if not monitoring_system:
            self.send_error(500, "Monitoring system not initialized")
            return

        try:
            alerts = monitoring_system.get_alerts()
            self.send_json_response({"status": "ok", "data": alerts})
        except Exception as e:
            logger.error(f"Internal error: {e}", exc_info=True); self.send_error(500, "Internal Server Error")

    def handle_monitoring_summary(self):
        """处理监控摘要请求"""
        global monitoring_system
        if not monitoring_system:
            self.send_error(500, "Monitoring system not initialized")
            return

        try:
            summary = monitoring_system.get_summary()
            self.send_json_response({"status": "ok", "data": summary})
        except Exception as e:
            logger.error(f"Internal error: {e}", exc_info=True); self.send_error(500, "Internal Server Error")

    def handle_summary(self):
        """处理摘要生成请求"""
        global summarizer
        if not summarizer:
            self.send_error(500, "Summarizer not initialized")
            return

        try:
            # 获取查询参数
            parsed_path = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_path.query)
            text = query_params.get('text', [''])[0]
            max_length = int(query_params.get('max_length', ['200'])[0])
            min_length = int(query_params.get('min_length', ['50'])[0])
            summary_type = query_params.get('type', ['general'])[0]
            language = query_params.get('language', ['zh'])[0]

            if not text:
                self.send_error(400, "Missing text parameter")
                return

            # 生成摘要
            summary = summarizer.summarize(text, max_length, min_length, summary_type, language)
            
            # 获取统计信息
            stats = summarizer.get_summary_stats(text, summary)

            self.send_json_response({"status": "ok", "data": {"summary": summary, "stats": stats}})
        except Exception as e:
            logger.error(f"Internal error: {e}", exc_info=True); self.send_error(500, "Internal Server Error")

    def handle_personalization_settings(self):
        """处理个性化设置请求"""
        global personalization_manager
        if not personalization_manager:
            self.send_error(500, "PersonalizationManager not initialized")
            return

        try:
            if self.command == "GET":
                # 获取查询参数
                parsed_path = urllib.parse.urlparse(self.path)
                query_params = urllib.parse.parse_qs(parsed_path.query)
                user_id = query_params.get('user_id', ['default'])[0]
                
                # 获取设置
                settings = personalization_manager.get_settings(user_id)
                self.send_json_response({"status": "ok", "data": settings})
            elif self.command == "POST":
                # 读取请求体
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data)
                
                user_id = data.get('user_id', 'default')
                settings = data.get('settings', {})
                
                # 更新设置
                success = personalization_manager.update_settings(settings, user_id)
                self.send_json_response({"status": "ok" if success else "error", "data": {"updated": success}})
            else:
                self.send_error(405, "Method Not Allowed")
        except Exception as e:
            logger.error(f"Internal error: {e}", exc_info=True); self.send_error(500, "Internal Server Error")

    def handle_personalization_interface(self):
        """处理界面设置请求"""
        global personalization_manager
        if not personalization_manager:
            self.send_error(500, "PersonalizationManager not initialized")
            return

        try:
            if self.command == "GET":
                # 获取查询参数
                parsed_path = urllib.parse.urlparse(self.path)
                query_params = urllib.parse.parse_qs(parsed_path.query)
                user_id = query_params.get('user_id', ['default'])[0]
                
                # 获取界面设置
                settings = personalization_manager.get_interface_settings(user_id)
                self.send_json_response({"status": "ok", "data": settings})
            elif self.command == "POST":
                # 读取请求体
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data)
                
                user_id = data.get('user_id', 'default')
                settings = data.get('settings', {})
                
                # 更新界面设置
                success = personalization_manager.update_interface_settings(settings, user_id)
                self.send_json_response({"status": "ok" if success else "error", "data": {"updated": success}})
            else:
                self.send_error(405, "Method Not Allowed")
        except Exception as e:
            logger.error(f"Internal error: {e}", exc_info=True); self.send_error(500, "Internal Server Error")

    def handle_personalization_system(self):
        """处理系统设置请求"""
        global personalization_manager
        if not personalization_manager:
            self.send_error(500, "PersonalizationManager not initialized")
            return

        try:
            if self.command == "GET":
                # 获取查询参数
                parsed_path = urllib.parse.urlparse(self.path)
                query_params = urllib.parse.parse_qs(parsed_path.query)
                user_id = query_params.get('user_id', ['default'])[0]
                
                # 获取系统设置
                settings = personalization_manager.get_system_settings(user_id)
                self.send_json_response({"status": "ok", "data": settings})
            elif self.command == "POST":
                # 读取请求体
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data)
                
                user_id = data.get('user_id', 'default')
                settings = data.get('settings', {})
                
                # 更新系统设置
                success = personalization_manager.update_system_settings(settings, user_id)
                self.send_json_response({"status": "ok" if success else "error", "data": {"updated": success}})
            else:
                self.send_error(405, "Method Not Allowed")
        except Exception as e:
            logger.error(f"Internal error: {e}", exc_info=True); self.send_error(500, "Internal Server Error")

    def handle_personalization_search(self):
        """处理搜索设置请求"""
        global personalization_manager
        if not personalization_manager:
            self.send_error(500, "PersonalizationManager not initialized")
            return

        try:
            if self.command == "GET":
                # 获取查询参数
                parsed_path = urllib.parse.urlparse(self.path)
                query_params = urllib.parse.parse_qs(parsed_path.query)
                user_id = query_params.get('user_id', ['default'])[0]
                
                # 获取搜索设置
                settings = personalization_manager.get_search_settings(user_id)
                self.send_json_response({"status": "ok", "data": settings})
            elif self.command == "POST":
                # 读取请求体
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data)
                
                user_id = data.get('user_id', 'default')
                settings = data.get('settings', {})
                
                # 更新搜索设置
                success = personalization_manager.update_search_settings(settings, user_id)
                self.send_json_response({"status": "ok" if success else "error", "data": {"updated": success}})
            else:
                self.send_error(405, "Method Not Allowed")
        except Exception as e:
            logger.error(f"Internal error: {e}", exc_info=True); self.send_error(500, "Internal Server Error")

    def handle_personalization_memory(self):
        """处理记忆设置请求"""
        global personalization_manager
        if not personalization_manager:
            self.send_error(500, "PersonalizationManager not initialized")
            return

        try:
            if self.command == "GET":
                # 获取查询参数
                parsed_path = urllib.parse.urlparse(self.path)
                query_params = urllib.parse.parse_qs(parsed_path.query)
                user_id = query_params.get('user_id', ['default'])[0]
                
                # 获取记忆设置
                settings = personalization_manager.get_memory_settings(user_id)
                self.send_json_response({"status": "ok", "data": settings})
            elif self.command == "POST":
                # 读取请求体
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data)
                
                user_id = data.get('user_id', 'default')
                settings = data.get('settings', {})
                
                # 更新记忆设置
                success = personalization_manager.update_memory_settings(settings, user_id)
                self.send_json_response({"status": "ok" if success else "error", "data": {"updated": success}})
            else:
                self.send_error(405, "Method Not Allowed")
        except Exception as e:
            logger.error(f"Internal error: {e}", exc_info=True); self.send_error(500, "Internal Server Error")

    def handle_personalization_notifications(self):
        """处理通知设置请求"""
        global personalization_manager
        if not personalization_manager:
            self.send_error(500, "PersonalizationManager not initialized")
            return

        try:
            if self.command == "GET":
                # 获取查询参数
                parsed_path = urllib.parse.urlparse(self.path)
                query_params = urllib.parse.parse_qs(parsed_path.query)
                user_id = query_params.get('user_id', ['default'])[0]
                
                # 获取通知设置
                settings = personalization_manager.get_notification_settings(user_id)
                self.send_json_response({"status": "ok", "data": settings})
            elif self.command == "POST":
                # 读取请求体
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data)
                
                user_id = data.get('user_id', 'default')
                settings = data.get('settings', {})
                
                # 更新通知设置
                success = personalization_manager.update_notification_settings(settings, user_id)
                self.send_json_response({"status": "ok" if success else "error", "data": {"updated": success}})
            else:
                self.send_error(405, "Method Not Allowed")
        except Exception as e:
            logger.error(f"Internal error: {e}", exc_info=True); self.send_error(500, "Internal Server Error")

    def handle_personalization_llm(self):
        """处理LLM设置请求"""
        global personalization_manager
        if not personalization_manager:
            self.send_error(500, "PersonalizationManager not initialized")
            return

        try:
            if self.command == "GET":
                # 获取查询参数
                parsed_path = urllib.parse.urlparse(self.path)
                query_params = urllib.parse.parse_qs(parsed_path.query)
                user_id = query_params.get('user_id', ['default'])[0]
                
                # 获取LLM设置
                settings = personalization_manager.get_llm_settings(user_id)
                self.send_json_response({"status": "ok", "data": settings})
            elif self.command == "POST":
                # 读取请求体
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data)
                
                user_id = data.get('user_id', 'default')
                settings = data.get('settings', {})
                
                # 更新LLM设置
                success = personalization_manager.update_llm_settings(settings, user_id)
                self.send_json_response({"status": "ok" if success else "error", "data": {"updated": success}})
            else:
                self.send_error(405, "Method Not Allowed")
        except Exception as e:
            logger.error(f"Internal error: {e}", exc_info=True); self.send_error(500, "Internal Server Error")

    def handle_plugins_list(self):
        """处理插件列表请求"""
        global plugin_system
        if not plugin_system:
            self.send_error(500, "PluginSystem not initialized")
            return

        try:
            # 列出所有插件
            plugins = plugin_system.list_plugins()
            self.send_json_response({"status": "ok", "data": plugins})
        except Exception as e:
            logger.error(f"Internal error: {e}", exc_info=True); self.send_error(500, "Internal Server Error")

    def handle_plugin_info(self):
        """处理插件信息请求"""
        global plugin_system
        if not plugin_system:
            self.send_error(500, "PluginSystem not initialized")
            return

        try:
            # 获取查询参数
            parsed_path = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_path.query)
            plugin_name = query_params.get('name', [''])[0]
            
            if not plugin_name:
                self.send_error(400, "Missing plugin name parameter")
                return

            # 获取插件信息
            info = plugin_system.get_plugin_info(plugin_name)
            if info:
                self.send_json_response({"status": "ok", "data": info})
            else:
                self.send_error(404, f"Plugin {plugin_name} not found")
        except Exception as e:
            logger.error(f"Internal error: {e}", exc_info=True); self.send_error(500, "Internal Server Error")

    def handle_plugin_execute(self):
        """处理插件执行请求"""
        global plugin_system
        if not plugin_system:
            self.send_error(500, "PluginSystem not initialized")
            return

        try:
            if self.command == "POST":
                # 读取请求体
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data)
                
                plugin_name = data.get('plugin', '')
                method = data.get('method', '')
                args = data.get('args', [])
                kwargs = data.get('kwargs', {})
                
                if not plugin_name or not method:
                    self.send_error(400, "Missing plugin or method parameter")
                    return

                # 执行插件方法
                result = plugin_system.execute_plugin(plugin_name, method, *args, **kwargs)
                self.send_json_response({"status": "ok", "data": result})
            else:
                self.send_error(405, "Method Not Allowed")
        except Exception as e:
            logger.error(f"Internal error: {e}", exc_info=True); self.send_error(500, "Internal Server Error")

    def handle_plugin_config(self):
        """处理插件配置请求"""
        global plugin_system
        if not plugin_system:
            self.send_error(500, "PluginSystem not initialized")
            return

        try:
            if self.command == "GET":
                # 获取查询参数
                parsed_path = urllib.parse.urlparse(self.path)
                query_params = urllib.parse.parse_qs(parsed_path.query)
                plugin_name = query_params.get('name', [''])[0]
                
                if not plugin_name:
                    self.send_error(400, "Missing plugin name parameter")
                    return

                # 获取插件配置
                config = plugin_system.get_plugin_config(plugin_name)
                if config is not None:
                    self.send_json_response({"status": "ok", "data": config})
                else:
                    self.send_error(404, f"Plugin {plugin_name} not found")
            elif self.command == "POST":
                # 读取请求体
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data)
                
                plugin_name = data.get('plugin', '')
                config = data.get('config', {})
                
                if not plugin_name:
                    self.send_error(400, "Missing plugin parameter")
                    return

                # 更新插件配置
                success = plugin_system.set_plugin_config(plugin_name, config)
                self.send_json_response({"status": "ok" if success else "error", "data": {"updated": success}})
            else:
                self.send_error(405, "Method Not Allowed")
        except Exception as e:
            logger.error(f"Internal error: {e}", exc_info=True); self.send_error(500, "Internal Server Error")

    def log_message(self, format, *args):
        """自定义日志格式"""
        logger.info(f"{self.client_address[0]} - [{datetime.now().isoformat()}] {format % args}")


def initialize_components():
    """初始化组件"""
    global feeder, converter, memory_system, chat_window, async_manager, permission_manager, monitoring_system, summarizer, personalization_manager, plugin_system

    try:
        logger.info("Initializing components...")
        
        # 暂时跳过模型服务器初始化，先测试基本功能
        # logger.info("Initializing model server...")
        # _check_model_server()
        # logger.info("Model server initialized successfully")

        logger.info("Initializing KnowledgeFeeder...")
        # 初始化组件
        feeder = KnowledgeFeeder()
        logger.info("KnowledgeFeeder initialized successfully")

        logger.info("Initializing FormatConverter...")
        converter = FormatConverter()
        logger.info("FormatConverter initialized successfully")

        # 暂时跳过 AgentMemory 初始化，先测试基本功能
        # logger.info("Initializing AgentMemory...")
        # memory_system = AgentMemory()
        # logger.info("AgentMemory initialized successfully")
        memory_system = None
        
        # 初始化异步管理器
        logger.info("Initializing AsyncManager...")
        async_manager = get_async_manager()
        import asyncio
        asyncio.run(async_manager.start())
        logger.info("AsyncManager initialized successfully")
        
        # 初始化权限管理器
        logger.info("Initializing PermissionManager...")
        permission_manager = get_permission_manager()
        logger.info("PermissionManager initialized successfully")
        
        # 初始化监控系统
        logger.info("Initializing MonitoringSystem...")
        monitoring_system = get_monitoring_system()
        monitoring_system.start()
        logger.info("MonitoringSystem initialized successfully")
        
        # 初始化摘要生成器
        logger.info("Initializing Summarizer...")
        summarizer = get_summarizer()
        logger.info("Summarizer initialized successfully")
        
        # 初始化个性化设置管理器
        logger.info("Initializing PersonalizationManager...")
        personalization_manager = get_personalization_manager()
        logger.info("PersonalizationManager initialized successfully")
        
        # 初始化插件系统
        logger.info("Initializing PluginSystem...")
        plugin_system = get_plugin_system()
        logger.info("PluginSystem initialized successfully")
        
        # 初始化 LLM 客户端
        logger.info("Initializing LLMClient...")
        llm_client = LLMClient(config)
        logger.info(f"LLMClient initialized successfully, available: {llm_client.is_available()}")
        
        def llm_fn(messages):
            return llm_client.chat(messages)
        
        chat_window = FeederChatWindow(knowledge_feeder=feeder, llm_fn=llm_fn if llm_client.is_available() else None)
        logger.info("FeederChatWindow initialized successfully")

        logger.info("Components initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing components: {e}")
        import traceback
        traceback.print_exc()
        raise


def start_server(host='127.0.0.1', port=None):
    """启动 Web 服务器（默认仅本地访问）"""
    if port is None:
        port = int(os.environ.get("AGENT_MEMORY_WEB_PORT", "8080"))
    if host not in ('127.0.0.1', 'localhost', '::1'):
        logger.warning(f"⚠️ Web server binding to {host} — ensure API Key is set for server.py")
    server_address = (host, port)
    httpd = HTTPServer(server_address, RequestHandler)
    logger.info(f"Starting web server on http://{host}:{port}")
    httpd.serve_forever()


def create_web_directory():
    """创建 Web 目录"""
    web_dir = os.path.join(PROJECT_DIR, "web")
    if not os.path.exists(web_dir):
        os.makedirs(web_dir)
        logger.info(f"Created web directory: {web_dir}")


def main():
    """主函数"""
    # 创建 Web 目录
    create_web_directory()

    # 初始化组件
    initialize_components()

    # 启动 Web 服务器
    start_server()


if __name__ == "__main__":
    main()