#!/usr/bin/env python3
"""
网页工具集

提供 HTTP 请求、网页抓取、搜索等能力
参考 Claude Code 的网页工具设计
"""

from __future__ import annotations

import asyncio
import urllib.request
import urllib.parse
import urllib.error
import json
import re
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from schema import BaseTool, ToolDefinition, ToolResult, ToolCapability


class HttpRequestTool(BaseTool):
    """HTTP 请求工具 - 增强版"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="http_request",
            description="发起 HTTP 请求，支持 GET/POST/PUT/DELETE",
            input_schema={
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "请求 URL"},
                    "method": {"type": "string", "enum": ["GET", "POST", "PUT", "DELETE", "PATCH"], "default": "GET"},
                    "headers": {"type": "object", "description": "请求头"},
                    "data": {"type": "object", "description": "请求数据 (JSON)"},
                    "form": {"type": "object", "description": "表单数据"},
                    "timeout": {"type": "number", "default": 30},
                    "follow_redirects": {"type": "boolean", "default": True}
                },
                "required": ["url"]
            },
            capabilities={ToolCapability.NETWORK},
            tags=["http", "request", "api", "network"],
            examples=[
                "GET请求: url='https://api.github.com'",
                "POST请求: url='https://api.example.com', data={'key': 'value'}"
            ]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        url = kwargs.get("url")
        method = kwargs.get("method", "GET")
        headers = kwargs.get("headers", {})
        data = kwargs.get("data")
        form = kwargs.get("form")
        timeout = kwargs.get("timeout", 30)
        follow_redirects = kwargs.get("follow_redirects", True)
        
        try:
            # 构建请求
            req = urllib.request.Request(url, method=method)
            
            # 添加默认头
            req.add_header("User-Agent", "OpenClaw-Tool/1.0")
            
            # 添加自定义头
            for key, value in headers.items():
                req.add_header(key, value)
            
            # 处理请求体
            if data:
                req.data = json.dumps(data).encode("utf-8")
                if "Content-Type" not in headers:
                    req.add_header("Content-Type", "application/json")
            elif form:
                form_data = urllib.parse.urlencode(form).encode("utf-8")
                req.data = form_data
                if "Content-Type" not in headers:
                    req.add_header("Content-Type", "application/x-www-form-urlencoded")
            
            # 处理重定向
            if not follow_redirects:
                import http.cookiejar
                class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
                    def redirect_request(self, req, fp, code, msg, headers, newurl):
                        return None
                opener = urllib.request.build_opener(NoRedirectHandler)
            else:
                opener = urllib.request.build_opener()
            
            # 发送请求
            with opener.open(req, timeout=timeout) as response:
                body = response.read().decode("utf-8", errors="replace")
                
                # 尝试解析 JSON
                try:
                    json_data = json.loads(body)
                    body = json_data
                except:
                    pass
                
                return ToolResult(
                    success=True,
                    data={
                        "status": response.status,
                        "status_text": response.reason,
                        "headers": dict(response.headers),
                        "body": body,
                        "url": response.url
                    }
                )
                
        except urllib.error.HTTPError as e:
            return ToolResult(
                success=False,
                error=f"HTTP {e.code}: {e.reason}"
            )
        except urllib.error.URLError as e:
            return ToolResult(success=False, error=f"请求失败: {e.reason}")
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class WebFetchTool(BaseTool):
    """网页抓取工具"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="web_fetch",
            description="抓取网页内容并提取文本",
            input_schema={
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "网页 URL"},
                    "extract": {"type": "string", "enum": ["text", "html", "markdown", "json"], "default": "text"},
                    "selector": {"type": "string", "description": "CSS 选择器"},
                    "timeout": {"type": "number", "default": 30}
                },
                "required": ["url"]
            },
            capabilities={ToolCapability.NETWORK},
            tags=["web", "fetch", "scrape", "crawl"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        url = kwargs.get("url")
        extract = kwargs.get("extract", "text")
        selector = kwargs.get("selector")
        timeout = kwargs.get("timeout", 30)
        
        try:
            req = urllib.request.Request(url)
            req.add_header("User-Agent", "Mozilla/5.0 (compatible; OpenClaw/1.0)")
            
            with urllib.request.urlopen(req, timeout=timeout) as response:
                html = response.read().decode("utf-8", errors="replace")
            
            if extract == "html":
                return ToolResult(success=True, data={"html": html, "url": url})
            
            # 简单提取文本（移除脚本和样式）
            text = html
            # 移除脚本
            text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
            # 移除样式
            text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
            # 移除 HTML 标签
            text = re.sub(r'<[^>]+>', '', text)
            # 清理空白
            text = re.sub(r'\s+', ' ', text).strip()
            
            if extract == "text":
                return ToolResult(success=True, data={"text": text, "url": url})
            
            # 如果需要 CSS 选择器（简化版）
            if selector:
                # 简单实现：查找包含选择器的元素
                pattern = re.compile(rf'<[^>]+{re.escape(selector)}[^>]*>(.*?)</[^>]+>', re.DOTALL)
                matches = pattern.findall(html)
                text = " ".join(matches)[:5000]  # 限制长度
            
            return ToolResult(
                success=True,
                data={
                    "text": text[:10000],  # 限制长度
                    "url": url,
                    "length": len(text)
                }
            )
            
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class WebSearchTool(BaseTool):
    """网页搜索工具"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="web_search",
            description="搜索网页内容",
            input_schema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "搜索关键词"},
                    "engine": {"type": "string", "enum": ["duckduckgo", "bing", "google"], "default": "duckduckgo"},
                    "limit": {"type": "integer", "default": 10, "description": "结果数量"}
                },
                "required": ["query"]
            },
            capabilities={ToolCapability.NETWORK},
            tags=["web", "search", "google", "duckduckgo"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        query = kwargs.get("query")
        engine = kwargs.get("engine", "duckduckgo")
        limit = kwargs.get("limit", 10)
        
        try:
            # 使用 DuckDuckGo HTML 版本
            if engine == "duckduckgo":
                url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
                req = urllib.request.Request(url)
                req.add_header("User-Agent", "Mozilla/5.0")
                
                with urllib.request.urlopen(req, timeout=30) as response:
                    html = response.read().decode("utf-8", errors="replace")
                
                # 解析结果
                results = []
                # 简单正则匹配
                result_pattern = re.compile(r'<a class="result__a" href="([^"]+)"[^>]*>([^<]+)</a>')
                snippet_pattern = re.compile(r'<a class="result__snippet"[^>]*>([^<]+)</a>')
                
                for match in result_pattern.finditer(html)[:limit]:
                    url = match.group(1)
                    title = match.group(2)
                    # 获取对应的 snippet
                    snippet_match = snippet_pattern.search(html[match.start():match.end() + 200])
                    snippet = snippet_match.group(1) if snippet_match else ""
                    
                    results.append({
                        "title": title,
                        "url": url,
                        "snippet": snippet[:200]
                    })
                
                return ToolResult(
                    success=True,
                    data={
                        "results": results,
                        "count": len(results),
                        "query": query,
                        "engine": engine
                    }
                )
            
            else:
                return ToolResult(success=False, error=f"不支持的搜索引擎: {engine}")
                
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class ApiRequestTool(BaseTool):
    """API 请求工具 - 带认证支持"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="api_request",
            description="发起 API 请求，支持多种认证方式",
            input_schema={
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "API URL"},
                    "method": {"type": "string", "default": "GET"},
                    "auth": {"type": "object", "description": "认证信息"},
                    "params": {"type": "object", "description": "URL 参数"},
                    "headers": {"type": "object", "description": "请求头"},
                    "body": {"type": "object", "description": "请求体"},
                    "timeout": {"type": "number", "default": 30}
                },
                "required": ["url"]
            },
            capabilities={ToolCapability.NETWORK},
            tags=["api", "rest", "auth", "oauth"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        url = kwargs.get("url")
        method = kwargs.get("method", "GET")
        auth = kwargs.get("auth", {})
        params = kwargs.get("params", {})
        headers = kwargs.get("headers", {})
        body = kwargs.get("body")
        timeout = kwargs.get("timeout", 30)
        
        try:
            # 添加 URL 参数
            if params:
                url += "?" + urllib.parse.urlencode(params)
            
            # 构建请求
            req = urllib.request.Request(url, method=method)
            req.add_header("User-Agent", "OpenClaw-Tool/1.0")
            req.add_header("Accept", "application/json")
            
            # 添加认证
            auth_type = auth.get("type", "")
            if auth_type == "bearer":
                token = auth.get("token", "")
                req.add_header("Authorization", f"Bearer {token}")
            elif auth_type == "basic":
                import base64
                username = auth.get("username", "")
                password = auth.get("password", "")
                credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
                req.add_header("Authorization", f"Basic {credentials}")
            elif auth_type == "api_key":
                key_name = auth.get("key_name", "X-API-Key")
                key_value = auth.get("key_value", "")
                req.add_header(key_name, key_value)
            
            # 添加自定义头
            for key, value in headers.items():
                req.add_header(key, value)
            
            # 添加请求体
            if body:
                req.data = json.dumps(body).encode("utf-8")
                req.add_header("Content-Type", "application/json")
            
            # 发送请求
            with urllib.request.urlopen(req, timeout=timeout) as response:
                content = response.read()
                content_type = response.headers.get("Content-Type", "")
                
                if "json" in content_type:
                    data = json.loads(content.decode("utf-8"))
                else:
                    data = content.decode("utf-8", errors="replace")
                
                return ToolResult(
                    success=True,
                    data={
                        "status": response.status,
                        "data": data,
                        "headers": dict(response.headers)
                    }
                )
                
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class UrlParseTool(BaseTool):
    """URL 解析工具"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="url_parse",
            description="解析和操作 URL",
            input_schema={
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "URL"},
                    "action": {"type": "string", "enum": ["parse", "build", "encode", "decode"], "default": "parse"}
                },
                "required": ["url"]
            },
            capabilities={ToolCapability.NETWORK},
            tags=["url", "parse", "encode", "decode"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        url = kwargs.get("url")
        action = kwargs.get("action", "parse")
        
        try:
            if action == "parse":
                parsed = urllib.parse.urlparse(url)
                return ToolResult(
                    success=True,
                    data={
                        "scheme": parsed.scheme,
                        "netloc": parsed.netloc,
                        "hostname": parsed.hostname,
                        "port": parsed.port,
                        "path": parsed.path,
                        "params": urllib.parse.parse_qs(parsed.query),
                        "fragment": parsed.fragment
                    }
                )
            
            elif action == "encode":
                return ToolResult(
                    success=True,
                    data={"encoded": urllib.parse.quote(url)}
                )
            
            elif action == "decode":
                return ToolResult(
                    success=True,
                    data={"decoded": urllib.parse.unquote(url)}
                )
            
            elif action == "build":
                # 需要提供各部分
                return ToolResult(
                    success=False,
                    error="build 需要提供 scheme, netloc, path 等参数"
                )
            
        except Exception as e:
            return ToolResult(success=False, error=str(e))


# 导出所有工具
WEB_TOOLS = [
    HttpRequestTool,
    WebFetchTool,
    WebSearchTool,
    ApiRequestTool,
    UrlParseTool,
]


def register_tools(registry):
    """注册所有网页工具到注册表"""
    for tool_class in WEB_TOOLS:
        tool = tool_class()
        registry.register(tool, "web")
    return len(WEB_TOOLS)