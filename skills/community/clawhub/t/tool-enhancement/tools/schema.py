#!/usr/bin/env python3
"""
工具系统标准化模块

提供统一工具接口、Schema 验证、权限控制
参考 Claude Code 的工具系统设计
"""

from __future__ import annotations

import json
import asyncio
from typing import Any, Dict, List, Optional, Callable, Set, Union
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import hashlib

try:
    from jsonschema import validate, ValidationError
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False

try:
    from colorama import Fore, init
    init(autoreset=True)
except ImportError:
    class Fore:
        CYAN = GREEN = RED = YELLOW = BLUE = MAGENTA = ""


class ToolCapability(Enum):
    """工具能力"""
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    NETWORK = "network"
    FS_READ = "fs:read"
    FS_WRITE = "fs:write"
    FS_DELETE = "fs:delete"


@dataclass
class ToolResult:
    """工具执行结果"""
    success: bool
    data: Any = None
    error: Optional[str] = None
    execution_time: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ToolDefinition:
    """工具定义"""
    name: str
    description: str
    input_schema: Dict[str, Any] = field(default_factory=dict)
    output_schema: Dict[str, Any] = field(default_factory=dict)
    capabilities: Set[ToolCapability] = field(default_factory=set)
    rate_limit: int = 60  # 每分钟调用次数
    timeout: float = 30.0
    tags: List[str] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)
    version: str = "1.0.0"
    author: str = "unknown"
    deprecated: bool = False
    deprecation_message: Optional[str] = None


class BaseTool(ABC):
    """工具基类"""
    
    def __init__(self, definition: ToolDefinition):
        self.definition = definition
        self._call_count = 0
        self._last_call: Optional[datetime] = None
    
    @property
    def name(self) -> str:
        return self.definition.name
    
    @property
    def description(self) -> str:
        return self.definition.description
    
    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        """执行工具"""
        pass
    
    def validate_input(self, params: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """验证输入参数"""
        if not HAS_JSONSCHEMA:
            return True, None
        
        try:
            validate(instance=params, schema=self.definition.input_schema)
            return True, None
        except ValidationError as e:
            return False, str(e.message)
    
    def check_rate_limit(self) -> bool:
        """检查速率限制"""
        now = datetime.now()
        
        if self._last_call:
            elapsed = (now - self._last_call).total_seconds()
            if elapsed < 60:  # 1分钟内
                if self._call_count >= self.definition.rate_limit:
                    return False
            else:
                self._call_count = 0
        
        self._call_count += 1
        self._last_call = now
        return True
    
    def get_metadata(self) -> Dict[str, Any]:
        """获取工具元数据"""
        return {
            "name": self.name,
            "description": self.description,
            "version": self.definition.version,
            "author": self.definition.author,
            "capabilities": [c.value for c in self.definition.capabilities],
            "tags": self.definition.tags,
            "deprecated": self.definition.deprecated
        }


class ToolRegistry:
    """工具注册表"""
    
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        self._categories: Dict[str, List[str]] = {}
        self._hooks: Dict[str, List[Callable]] = {
            "before_execute": [],
            "after_execute": [],
            "on_error": []
        }
    
    def register(self, tool: BaseTool, category: str = "default") -> None:
        """注册工具"""
        if tool.name in self._tools:
            raise ValueError(f"工具已存在: {tool.name}")
        
        self._tools[tool.name] = tool
        
        if category not in self._categories:
            self._categories[category] = []
        self._categories[category].append(tool.name)
        
        print(f"{Fore.GREEN}✓ 注册工具: {tool.name} ({category}){Fore.RESET}")
    
    def unregister(self, name: str) -> bool:
        """注销工具"""
        if name not in self._tools:
            return False
        
        del self._tools[name]
        
        for category in self._categories:
            if name in self._categories[category]:
                self._categories[category].remove(name)
        
        return True
    
    def get(self, name: str) -> Optional[BaseTool]:
        """获取工具"""
        return self._tools.get(name)
    
    def list_all(self) -> List[str]:
        """列出所有工具"""
        return list(self._tools.keys())
    
    def list_by_category(self, category: str) -> List[str]:
        """按分类列出"""
        return self._categories.get(category, [])
    
    def search(self, query: str) -> List[str]:
        """搜索工具"""
        query = query.lower()
        results = []
        
        for name, tool in self._tools.items():
            if (query in name.lower() or 
                query in tool.description.lower() or
                any(query in tag.lower() for tag in tool.definition.tags)):
                results.append(name)
        
        return results
    
    def get_by_capability(self, capability: ToolCapability) -> List[str]:
        """按能力查找"""
        results = []
        
        for name, tool in self._tools.items():
            if capability in tool.definition.capabilities:
                results.append(name)
        
        return results
    
    def add_hook(self, event: str, callback: Callable) -> None:
        """添加钩子"""
        if event in self._hooks:
            self._hooks[event].append(callback)
    
    async def execute(self, tool_name: str, **kwargs) -> ToolResult:
        """执行工具"""
        import time
        start_time = time.time()
        
        tool = self.get(tool_name)
        if not tool:
            return ToolResult(
                success=False,
                error=f"工具不存在: {tool_name}"
            )
        
        # 检查废弃
        if tool.definition.deprecated:
            print(f"{Fore.YELLOW}⚠ 工具已废弃: {name}{Fore.RESET}")
            if tool.definition.deprecation_message:
                print(f"   {tool.definition.deprecation_message}")
        
        # 速率限制检查
        if not tool.check_rate_limit():
            return ToolResult(
                success=False,
                error="速率限制超出"
            )
        
        # 输入验证
        valid, error_msg = tool.validate_input(kwargs)
        if not valid:
            return ToolResult(
                success=False,
                error=f"输入验证失败: {error_msg}"
            )
        
        # 执行前钩子
        for hook in self._hooks["before_execute"]:
            try:
                await hook(tool, kwargs)
            except Exception as e:
                print(f"{Fore.YELLOW}⚠ Hook 失败: {e}{Fore.RESET}")
        
        # 执行
        try:
            result = await tool.execute(**kwargs)
            result.execution_time = time.time() - start_time
            
            # 执行后钩子
            for hook in self._hooks["after_execute"]:
                try:
                    await hook(tool, result)
                except Exception as e:
                    print(f"{Fore.YELLOW}⚠ Hook 失败: {e}{Fore.RESET}")
            
            return result
            
        except Exception as e:
            # 错误钩子
            for hook in self._hooks["on_error"]:
                try:
                    await hook(tool, e)
                except Exception:
                    pass
            
            return ToolResult(
                success=False,
                error=str(e),
                execution_time=time.time() - start_time
            )


# ============ 示例工具 ============

class FileReadTool(BaseTool):
    """文件读取工具"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="file_read",
            description="读取文件内容",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "文件路径"},
                    "encoding": {"type": "string", "default": "utf-8"},
                    "limit": {"type": "integer", "description": "限制行数"}
                },
                "required": ["path"]
            },
            capabilities={ToolCapability.FS_READ},
            tags=["file", "read", "io"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        path = kwargs.get("path")
        encoding = kwargs.get("encoding", "utf-8")
        limit = kwargs.get("limit")
        
        try:
            with open(path, "r", encoding=encoding) as f:
                content = f.read() if limit is None else "".join(f.readlines()[:limit])
            
            return ToolResult(success=True, data=content)
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class WebRequestTool(BaseTool):
    """网络请求工具"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="web_request",
            description="发起 HTTP 请求",
            input_schema={
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "请求 URL"},
                    "method": {"type": "string", "default": "GET", "enum": ["GET", "POST"]},
                    "headers": {"type": "object"},
                    "body": {"type": "string"}
                },
                "required": ["url"]
            },
            capabilities={ToolCapability.NETWORK},
            tags=["network", "http", "api"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        import urllib.request
        import urllib.error
        
        url = kwargs.get("url")
        method = kwargs.get("method", "GET")
        headers = kwargs.get("headers", {})
        body = kwargs.get("body")
        
        try:
            req = urllib.request.Request(url, method=method, headers=headers)
            if body:
                req.data = body.encode()
            
            with urllib.request.urlopen(req, timeout=30) as response:
                return ToolResult(
                    success=True,
                    data={
                        "status": response.status,
                        "body": response.read().decode(),
                        "headers": dict(response.headers)
                    }
                )
        except urllib.error.URLError as e:
            return ToolResult(success=False, error=str(e))
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class CalculatorTool(BaseTool):
    """计算器工具"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="calculator",
            description="数学计算",
            input_schema={
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "数学表达式"}
                },
                "required": ["expression"]
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["math", "calculator"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        expression = kwargs.get("expression")
        
        try:
            # 安全计算（只允许基本运算）
            allowed_chars = set("0123456789+-*/.() ")
            if not all(c in allowed_chars for c in expression):
                return ToolResult(success=False, error="包含不允许的字符")
            
            result = eval(expression)  # 注意：生产环境应该用 ast 解析
            return ToolResult(success=True, data=result)
        except Exception as e:
            return ToolResult(success=False, error=str(e))


# ============ 使用示例 ============

async def example():
    """示例"""
    print(f"{Fore.CYAN}=== 工具系统标准化示例 ==={Fore.RESET}\n")
    
    # 创建注册表
    registry = ToolRegistry()
    
    # 注册工具
    print("1. 注册工具:")
    registry.register(FileReadTool(), "file")
    registry.register(WebRequestTool(), "network")
    registry.register(CalculatorTool(), "utility")
    
    # 列出工具
    print("\n2. 所有工具:")
    for name in registry.list_all():
        tool = registry.get(name)
        print(f"   - {name}: {tool.description}")
    
    # 按分类列出
    print("\n3. 文件工具:")
    for name in registry.list_by_category("file"):
        print(f"   - {name}")
    
    # 搜索
    print("\n4. 搜索 'file':")
    for name in registry.search("file"):
        print(f"   - {name}")
    
    # 执行工具
    print("\n5. 执行工具:")
    
    # 计算器
    result = await registry.execute("calculator", expression="2+3*4")
    print(f"   计算 2+3*4 = {result.data}")
    
    # 读取文件
    result = await registry.execute("file_read", path="/etc/hostname")
    if result.success:
        print(f"   读取主机名: {result.data.strip()}")
    else:
        print(f"   读取失败: {result.error}")
    
    # 工具元数据
    print("\n6. 工具元数据:")
    tool = registry.get("calculator")
    meta = tool.get_metadata()
    for key, value in meta.items():
        print(f"   {key}: {value}")
    
    print(f"\n{Fore.GREEN}✓ 工具系统标准化示例完成!{Fore.RESET}")


if __name__ == "__main__":
    asyncio.run(example())