#!/usr/bin/env python3
"""
终端 UI 工具集

提供进度条、加载动画、表格、树形展示等终端 UI 能力
参考 Claude Code 的 Ink/React 终端 UI 设计
"""

from __future__ import annotations

import asyncio
import sys
import time
import itertools
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field
from pathlib import Path

import sys as _sys
_sys.path.insert(0, str(Path(__file__).parent))
from schema import BaseTool, ToolDefinition, ToolResult, ToolCapability


class SpinnerTool(BaseTool):
    """加载动画工具"""
    
    FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="ui_spinner",
            description="显示加载动画",
            input_schema={
                "type": "object",
                "properties": {
                    "message": {"type": "string", "default": "加载中...", "description": "显示消息"},
                    "frames": {"type": "integer", "default": 10, "description": "动画帧数"},
                    "duration": {"type": "number", "default": 3, "description": "持续时间(秒)"}
                }
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["ui", "spinner", "loading", "animation"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        message = kwargs.get("message", "加载中...")
        frames = kwargs.get("frames", 10)
        duration = kwargs.get("duration", 3)
        
        try:
            start_time = time.time()
            frame_index = 0
            
            # 模拟动画
            while time.time() - start_time < duration:
                frame = self.FRAMES[frame_index % len(self.FRAMES)]
                sys.stdout.write(f"\r{frame} {message}")
                sys.stdout.flush()
                await asyncio.sleep(0.1)
                frame_index += 1
            
            sys.stdout.write("\r" + " " * (len(message) + 10) + "\r")
            sys.stdout.flush()
            
            return ToolResult(
                success=True,
                data={
                    "message": message,
                    "duration": duration,
                    "frames_shown": frame_index
                }
            )
            
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class ProgressBarTool(BaseTool):
    """进度条工具"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="ui_progress",
            description="显示进度条",
            input_schema={
                "type": "object",
                "properties": {
                    "current": {"type": "integer", "description": "当前进度"},
                    "total": {"type": "integer", "description": "总数"},
                    "message": {"type": "string", "default": "进度", "description": "显示消息"},
                    "width": {"type": "integer", "default": 30, "description": "进度条宽度"}
                },
                "required": ["current", "total"]
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["ui", "progress", "bar"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        current = kwargs.get("current", 0)
        total = kwargs.get("total", 100)
        message = kwargs.get("message", "进度")
        width = kwargs.get("width", 30)
        
        try:
            # 计算进度
            percent = min(100, max(0, (current / total) * 100))
            filled = int(width * current / total) if total > 0 else 0
            empty = width - filled
            
            # 构建进度条
            bar = "█" * filled + "░" * empty
            text = f"{message}: [{bar}] {percent:.1f}%"
            
            return ToolResult(
                success=True,
                data={
                    "text": text,
                    "percent": percent,
                    "current": current,
                    "total": total,
                    "bar": bar
                }
            )
            
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class TableTool(BaseTool):
    """表格工具"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="ui_table",
            description="生成表格",
            input_schema={
                "type": "object",
                "properties": {
                    "headers": {"type": "array", "items": {"type": "string"}, "description": "表头"},
                    "rows": {"type": "array", "items": {"type": "array", "items": {"type": "string"}}, "description": "数据行"},
                    "style": {"type": "string", "enum": ["simple", "grid", "pipe"], "default": "simple"}
                },
                "required": ["headers", "rows"]
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["ui", "table", "grid"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        headers = kwargs.get("headers", [])
        rows = kwargs.get("rows", [])
        style = kwargs.get("style", "simple")
        
        try:
            if not headers:
                return ToolResult(success=False, error="需要表头")
            
            # 计算列宽
            col_widths = [len(h) for h in headers]
            for row in rows:
                for i, cell in enumerate(row):
                    if i < len(col_widths):
                        col_widths[i] = max(col_widths[i], len(str(cell)))
            
            # 构建表格
            lines = []
            
            if style == "simple":
                # 表头
                header_line = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
                lines.append(header_line)
                lines.append("-" * len(header_line))
                
                # 数据行
                for row in rows:
                    row_line = " | ".join(str(cell).ljust(col_widths[i]) if i < len(row) else "" 
                                          for i, cell in enumerate(row))
                    lines.append(row_line)
            
            elif style == "grid":
                # 带边框的表格
                separator = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
                
                lines.append(separator)
                header_line = "|" + "|".join(f" {h.ljust(col_widths[i])} " for i, h in enumerate(headers)) + "|"
                lines.append(header_line)
                lines.append(separator)
                
                for row in rows:
                    row_line = "|" + "|".join(f" {str(cell).ljust(col_widths[i])} " if i < len(row) else " " * (col_widths[i] + 2)
                                             for i, cell in enumerate(row)) + "|"
                    lines.append(row_line)
                
                lines.append(separator)
            
            elif style == "pipe":
                # Markdown 风格
                header_line = "| " + " | ".join(headers) + " |"
                lines.append(header_line)
                lines.append("|" + "|".join("---" for _ in headers) + "|")
                
                for row in rows:
                    row_line = "| " + " | ".join(str(cell) for cell in row) + " |"
                    lines.append(row_line)
            
            table = "\n".join(lines)
            
            return ToolResult(
                success=True,
                data={
                    "table": table,
                    "headers": headers,
                    "rows": rows,
                    "row_count": len(rows)
                }
            )
            
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class TreeTool(BaseTool):
    """树形展示工具"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="ui_tree",
            description="生成树形结构",
            input_schema={
                "type": "object",
                "properties": {
                    "data": {"type": "object", "description": "树形数据 (嵌套字典)"},
                    "root": {"type": "string", "default": "root", "description": "根节点名称"},
                    "max_depth": {"type": "integer", "default": 5, "description": "最大深度"}
                },
                "required": ["data"]
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["ui", "tree", "hierarchy"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        data = kwargs.get("data", {})
        root = kwargs.get("root", "root")
        max_depth = kwargs.get("max_depth", 5)
        
        try:
            def build_tree(node, prefix="", is_last=True, depth=0):
                if depth > max_depth:
                    return []
                
                lines = []
                connector = "└── " if is_last else "├── "
                lines.append(prefix + connector + str(node.get("name", "node")))
                
                children = node.get("children", [])
                for i, child in enumerate(children):
                    extension = "    " if is_last else "│   "
                    lines.extend(build_tree(child, prefix + extension, i == len(children) - 1, depth + 1))
                
                return lines
            
            tree_lines = [root]
            if data:
                children = data.get("children", [])
                for i, child in enumerate(children):
                    tree_lines.extend(build_tree(child, "", i == len(children) - 1, 1))
            
            tree = "\n".join(tree_lines)
            
            return ToolResult(
                success=True,
                data={
                    "tree": tree,
                    "node_count": len(data.get("children", []))
                }
            )
            
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class MarkdownRenderTool(BaseTool):
    """Markdown 渲染工具 - 简化版"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="ui_markdown",
            description="渲染 Markdown 为终端文本",
            input_schema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "Markdown 内容"},
                    "style": {"type": "string", "enum": ["plain", "colored"], "default": "plain"}
                },
                "required": ["content"]
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["ui", "markdown", "render"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        content = kwargs.get("content", "")
        style = kwargs.get("style", "plain")
        
        try:
            lines = content.split("\n")
            result = []
            
            for line in lines:
                # 标题
                if line.startswith("### "):
                    result.append(f"\033[1;34m{line[4:]}\033[0m")
                elif line.startswith("## "):
                    result.append(f"\033[1;33m{line[3:]}\033[0m")
                elif line.startswith("# "):
                    result.append(f"\033[1;32m{line[2:]}\033[0m")
                # 粗体
                elif "**" in line:
                    line = line.replace("**", "\033[1m", 2)
                    line = line.replace("**", "\033[0m", 1)
                    result.append(line)
                # 列表
                elif line.startswith("- ") or line.startswith("* "):
                    result.append(f"  • {line[2:]}")
                # 链接（简化）
                elif "[" in line and "]" in line:
                    # 移除链接标记
                    import re
                    line = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', line)
                    result.append(line)
                else:
                    result.append(line)
            
            return ToolResult(
                success=True,
                data={
                    "rendered": "\n".join(result),
                    "original": content,
                    "lines": len(lines)
                }
            )
            
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class StatusTool(BaseTool):
    """状态显示工具"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="ui_status",
            description="显示状态信息（成功/警告/错误/信息）",
            input_schema={
                "type": "object",
                "properties": {
                    "message": {"type": "string", "description": "消息内容"},
                    "status": {"type": "string", "enum": ["success", "error", "warning", "info"], "default": "info"},
                    "icon": {"type": "boolean", "default": True, "description": "显示图标"}
                },
                "required": ["message"]
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["ui", "status", "message", "alert"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        message = kwargs.get("message", "")
        status = kwargs.get("status", "info")
        show_icon = kwargs.get("icon", True)
        
        icons = {
            "success": "✅",
            "error": "❌",
            "warning": "⚠️",
            "info": "ℹ️"
        }
        
        icon = icons.get(status, "") if show_icon else ""
        output = f"{icon} {message}".strip()
        
        return ToolResult(
            success=True,
            data={
                "output": output,
                "status": status,
                "message": message
            }
        )


class ConfirmTool(BaseTool):
    """确认对话框工具"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="ui_confirm",
            description="显示确认提示",
            input_schema={
                "type": "object",
                "properties": {
                    "message": {"type": "string", "description": "确认消息"},
                    "default": {"type": "boolean", "default": False, "description": "默认选项"}
                },
                "required": ["message"]
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["ui", "confirm", "prompt"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        message = kwargs.get("message", "确认?")
        default = kwargs.get("default", False)
        
        default_str = "Y/n" if default else "y/N"
        prompt = f"{message} ({default_str}): "
        
        # 注意：这里简化了，实际需要 TTY 输入
        return ToolResult(
            success=True,
            data={
                "message": message,
                "prompt": prompt,
                "note": "需要 TTY 输入，实际使用需配合终端"
            }
        )


class MenuTool(BaseTool):
    """菜单工具"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="ui_menu",
            description="显示菜单选项",
            input_schema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "菜单标题"},
                    "options": {"type": "array", "items": {"type": "string"}, "description": "选项列表"},
                    "multi": {"type": "boolean", "default": False, "description": "多选"}
                },
                "required": ["title", "options"]
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["ui", "menu", "select"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        title = kwargs.get("title", "请选择")
        options = kwargs.get("options", [])
        multi = kwargs.get("multi", False)
        
        try:
            lines = [f"\033[1;36m{title}\033[0m", ""]
            
            for i, option in enumerate(options, 1):
                lines.append(f"  {i}. {option}")
            
            menu = "\n".join(lines)
            
            return ToolResult(
                success=True,
                data={
                    "menu": menu,
                    "options": options,
                    "count": len(options),
                    "multi": multi
                }
            )
            
        except Exception as e:
            return ToolResult(success=False, error=str(e))


# 导出所有工具
UI_TOOLS = [
    SpinnerTool,
    ProgressBarTool,
    TableTool,
    TreeTool,
    MarkdownRenderTool,
    StatusTool,
    ConfirmTool,
    MenuTool,
]


def register_tools(registry):
    """注册所有 UI 工具到注册表"""
    for tool_class in UI_TOOLS:
        tool = tool_class()
        registry.register(tool, "ui")
    return len(UI_TOOLS)