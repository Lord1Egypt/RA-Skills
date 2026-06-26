#!/usr/bin/env python3
"""
统一工具注册器

自动发现并注册所有工具模块
"""

import sys
from pathlib import Path

# 添加 tools 目录到路径
TOOLS_DIR = Path(__file__).parent
sys.path.insert(0, str(TOOLS_DIR))

# 导入 schema 模块的基础类
from schema import ToolRegistry, BaseTool


# 全局注册表实例
_registry = None
_loaded = False


def get_registry() -> ToolRegistry:
    """获取全局注册表"""
    global _registry
    if _registry is None:
        _registry = ToolRegistry()
    return _registry


def load_all_tools() -> int:
    """加载所有工具模块"""
    global _loaded
    
    # 如果已经加载过，直接返回
    registry = get_registry()
    if _loaded and len(registry.list_all()) > 0:
        return len(registry.list_all())
    
    total = 0
    
    # 工具模块列表
    tool_modules = [
        ("file_tools", "FILE_TOOLS"),
        ("exec_tools", "EXEC_TOOLS"),
        ("git_tools", "GIT_TOOLS"),
        ("web_tools", "WEB_TOOLS"),
        ("mcp_tools", "MCP_TOOLS"),
        ("agent_tools", "AGENT_TOOLS"),
        ("memory_tools", "MEMORY_TOOLS"),
        ("ui_tools", "UI_TOOLS"),
        ("session_tools", "SESSION_TOOLS"),  # 新增：会话协作工具
    ]
    
    for module_name, var_name in tool_modules:
        try:
            module = __import__(module_name, fromlist=[var_name])
            tool_classes = getattr(module, var_name, [])
            
            if tool_classes:
                for tool_class in tool_classes:
                    try:
                        tool = tool_class()
                        registry.register(tool, module_name.replace("_tools", ""))
                    except Exception:
                        pass
                
                total += len(tool_classes)
        except Exception:
            pass
    
    _loaded = True
    return total


async def test_tools():
    """测试工具"""
    load_all_tools()
    registry = get_registry()
    
    print(f"\n已加载 {len(registry.list_all())} 个工具\n")
    
    # 测试几个关键工具
    test_cases = [
        ("file_read", {"path": "/etc/hostname"}),
        ("system_info", {}),
    ]
    
    for tool_name, params in test_cases:
        result = await registry.execute(tool_name, **params)
        status = "✓" if result.success else "✗"
        print(f"{status} {tool_name}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_tools())