#!/usr/bin/env python3
"""
工具注册表发现模块

自动发现可用工具、分类、版本管理
"""

import json
import importlib
import inspect
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

try:
    from colorama import Fore, init
    init(autoreset=True)
except ImportError:
    class Fore:
        CYAN = GREEN = RED = YELLOW = BLUE = ""


class ToolCategory(Enum):
    """工具分类"""
    FILE = "file"              # 文件操作
    SEARCH = "search"          # 搜索
    EXECUTE = "execute"        # 执行命令
    WEB = "web"                # 网络请求
    CODE = "code"              # 代码相关
    DATA = "data"              # 数据处理
    AI = "ai"                  # AI 能力
    UTILITY = "utility"        # 工具类
    CUSTOM = "custom"          # 自定义


@dataclass
class ToolDescriptor:
    """工具描述符"""
    name: str
    description: str
    category: ToolCategory
    version: str
    author: str
    tags: List[str] = field(default_factory=list)
    input_schema: Dict[str, Any] = field(default_factory=dict)
    output_schema: Dict[str, Any] = field(default_factory=dict)
    capabilities: List[str] = field(default_factory=list)
    registered_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        """转为字典"""
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category.value,
            "version": self.version,
            "author": self.author,
            "tags": self.tags,
            "input_schema": self.input_schema,
            "output_schema": self.output_schema,
            "capabilities": self.capabilities,
            "registered_at": self.registered_at.isoformat()
        }


@dataclass
class ToolVersion:
    """工具版本"""
    version: str
    released_at: datetime
    changelog: str
    breaking: bool = False


class ToolRegistry:
    """工具注册表"""
    
    def __init__(self, storage_path: Path = None):
        self.storage_path = storage_path or Path.home() / ".openclaw" / "tools"
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.tools: Dict[str, ToolDescriptor] = {}
        self.tool_implementations: Dict[str, Callable] = {}
        self.tool_versions: Dict[str, List[ToolVersion]] = {}
        
        self._load_index()
    
    def _load_index(self):
        """加载索引"""
        index_file = self.storage_path / "index.json"
        if index_file.exists():
            try:
                data = json.loads(index_file.read_text())
                for tool_data in data.get("tools", []):
                    tool_data["category"] = ToolCategory(tool_data["category"])
                    tool_data["registered_at"] = datetime.fromisoformat(
                        tool_data["registered_at"]
                    )
                    tool = ToolDescriptor(**tool_data)
                    self.tools[tool.name] = tool
            except Exception:
                pass
    
    def _save_index(self):
        """保存索引"""
        data = {
            "tools": [t.to_dict() for t in self.tools.values()]
        }
        index_file = self.storage_path / "index.json"
        index_file.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    
    def register(
        self,
        name: str,
        description: str,
        category: ToolCategory,
        handler: Callable,
        version: str = "1.0.0",
        author: str = "unknown",
        tags: List[str] = None,
        input_schema: Dict = None,
        output_schema: Dict = None,
        capabilities: List[str] = None
    ) -> ToolDescriptor:
        """注册工具"""
        descriptor = ToolDescriptor(
            name=name,
            description=description,
            category=category,
            version=version,
            author=author,
            tags=tags or [],
            input_schema=input_schema or {},
            output_schema=output_schema or {},
            capabilities=capabilities or []
        )
        
        self.tools[name] = descriptor
        self.tool_implementations[name] = handler
        self._save_index()
        
        print(f"{Fore.GREEN}✓ 注册工具: {name} v{version}{Fore.RESET}")
        return descriptor
    
    def unregister(self, name: str) -> bool:
        """注销工具"""
        if name in self.tools:
            del self.tools[name]
            if name in self.tool_implementations:
                del self.tool_implementations[name]
            self._save_index()
            return True
        return False
    
    def get(self, name: str) -> Optional[ToolDescriptor]:
        """获取工具"""
        return self.tools.get(name)
    
    def get_handler(self, name: str) -> Optional[Callable]:
        """获取工具处理器"""
        return self.tool_implementations.get(name)
    
    def list_all(self) -> List[ToolDescriptor]:
        """列出所有工具"""
        return list(self.tools.values())
    
    def list_by_category(self, category: ToolCategory) -> List[ToolDescriptor]:
        """按分类列出"""
        return [t for t in self.tools.values() if t.category == category]
    
    def search(self, query: str) -> List[ToolDescriptor]:
        """搜索工具"""
        query = query.lower()
        results = []
        
        for tool in self.tools.values():
            if (query in tool.name.lower() or
                query in tool.description.lower() or
                any(query in tag.lower() for tag in tool.tags)):
                results.append(tool)
        
        return results
    
    def has_tool(self, name: str) -> bool:
        """检查工具是否存在"""
        return name in self.tools
    
    def execute(self, name: str, **kwargs) -> Any:
        """执行工具"""
        handler = self.get_handler(name)
        if not handler:
            raise ValueError(f"工具不存在: {name}")
        
        return handler(**kwargs)
    
    async def execute_async(self, name: str, **kwargs) -> Any:
        """异步执行工具"""
        handler = self.get_handler(name)
        if not handler:
            raise ValueError(f"工具不存在: {name}")
        
        if inspect.iscoroutinefunction(handler):
            return await handler(**kwargs)
        return handler(**kwargs)


class ToolDiscovery:
    """工具自动发现"""
    
    def __init__(self, registry: ToolRegistry = None):
        self.registry = registry or ToolRegistry()
        self.discover_paths = [
            Path.home() / ".openclaw" / "tools",
            Path.cwd() / "tools",
        ]
    
    def add_search_path(self, path: Path):
        """添加搜索路径"""
        if path not in self.discover_paths:
            self.discover_paths.append(path)
    
    def discover_from_directory(self, directory: Path) -> List[ToolDescriptor]:
        """从目录发现工具"""
        discovered = []
        
        if not directory.exists():
            return discovered
        
        for py_file in directory.glob("*.py"):
            if py_file.name.startswith("_"):
                continue
            
            try:
                # 动态导入模块
                module_name = py_file.stem
                spec = importlib.util.spec_from_file_location(module_name, py_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # 查找工具注册函数
                if hasattr(module, "register_tools"):
                    tools = module.register_tools(self.registry)
                    discovered.extend(tools if isinstance(tools, list) else [tools])
                    
            except Exception as e:
                print(f"{Fore.YELLOW}⚠ 发现工具失败 {py_file}: {e}{Fore.RESET}")
        
        return discovered
    
    def discover_all(self) -> List[ToolDescriptor]:
        """从所有路径发现工具"""
        all_tools = []
        
        for path in self.discover_paths:
            tools = self.discover_from_directory(path)
            all_tools.extend(tools)
            if tools:
                print(f"{Fore.CYAN}从 {path} 发现 {len(tools)} 个工具{Fore.RESET}")
        
        return all_tools
    
    def auto_discover(self) -> int:
        """自动发现并注册"""
        tools = self.discover_all()
        print(f"{Fore.GREEN}✓ 自动发现 {len(tools)} 个工具{Fore.RESET}")
        return len(tools)


# ============ 使用示例 ============

def example():
    """示例"""
    print(f"{Fore.CYAN}=== 工具注册表示例 ==={Fore.RESET}\n")
    
    # 创建注册表
    registry = ToolRegistry()
    
    # 注册工具
    print("1. 注册工具:")
    
    def read_file_handler(path: str, lines: int = None) -> str:
        """读取文件"""
        with open(path, 'r') as f:
            content = f.read() if lines is None else ''.join(f.readlines()[:lines])
        return content
    
    registry.register(
        name="read_file",
        description="读取文件内容",
        category=ToolCategory.FILE,
        handler=read_file_handler,
        version="1.0.0",
        author="openclaw",
        tags=["file", "read", "io"],
        input_schema={
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "文件路径"},
                "lines": {"type": "integer", "description": "读取行数"}
            },
            "required": ["path"]
        },
        capabilities=["read"]
    )
    
    # 列出工具
    print("\n2. 所有工具:")
    for tool in registry.list_all():
        print(f"   - {tool.name} ({tool.category.value}): {tool.description}")
    
    # 搜索工具
    print("\n3. 搜索 'file':")
    results = registry.search("file")
    for tool in results:
        print(f"   - {tool.name}")
    
    # 执行工具
    print("\n4. 执行工具:")
    # 注意：这里会尝试读取实际文件，可能失败
    try:
        result = registry.execute("read_file", path="/etc/hostname")
        print(f"   结果: {result.strip()}")
    except Exception as e:
        print(f"   执行结果: {e}")
    
    # 工具发现
    print("\n5. 工具发现:")
    discovery = ToolDiscovery(registry)
    count = discovery.auto_discover()
    print(f"   共发现: {count} 个工具")
    
    print(f"\n{Fore.GREEN}✓ 工具注册表示例完成!{Fore.RESET}")


if __name__ == "__main__":
    example()