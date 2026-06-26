#!/usr/bin/env python3
"""
文件操作工具集

提供完整的文件操作能力：读、写、编辑、删除、搜索、复制、移动
参考 Claude Code 工具系统设计
"""

from __future__ import annotations

import os
import shutil
import glob as glob_module
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field

# 复用 schema.py 的基础类
import sys
sys.path.insert(0, str(Path(__file__).parent))
from schema import BaseTool, ToolDefinition, ToolResult, ToolCapability


class FileReadTool(BaseTool):
    """文件读取工具 - 增强版"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="file_read",
            description="读取文件内容，支持编码选择和行数限制",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "文件路径"},
                    "encoding": {"type": "string", "default": "utf-8", "description": "文件编码"},
                    "limit": {"type": "integer", "description": "限制读取行数"},
                    "offset": {"type": "integer", "description": "起始行号"},
                    "tail": {"type": "boolean", "default": False, "description": "从文件末尾读取"}
                },
                "required": ["path"]
            },
            capabilities={ToolCapability.FS_READ},
            tags=["file", "read", "io"],
            examples=[
                "读取配置文件: path='/etc/config.conf'",
                "读取前10行: path='/tmp/log.txt', limit=10"
            ]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        path = kwargs.get("path")
        encoding = kwargs.get("encoding", "utf-8")
        limit = kwargs.get("limit")
        offset = kwargs.get("offset", 0)
        tail = kwargs.get("tail", False)
        
        try:
            with open(path, "r", encoding=encoding) as f:
                lines = f.readlines()
            
            if tail:
                lines = lines[-limit:] if limit else lines
            
            if offset > 0:
                lines = lines[offset:]
            
            if limit:
                lines = lines[:limit]
            
            content = "".join(lines)
            
            return ToolResult(
                success=True,
                data={
                    "content": content,
                    "lines": len(lines),
                    "path": path
                },
                metadata={"offset": offset, "limit": limit}
            )
        except FileNotFoundError:
            return ToolResult(success=False, error=f"文件不存在: {path}")
        except PermissionError:
            return ToolResult(success=False, error=f"权限不足: {path}")
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class FileWriteTool(BaseTool):
    """文件写入工具"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="file_write",
            description="写入内容到文件，支持创建和覆盖",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "文件路径"},
                    "content": {"type": "string", "description": "写入内容"},
                    "encoding": {"type": "string", "default": "utf-8"},
                    "append": {"type": "boolean", "default": False, "description": "追加模式"}
                },
                "required": ["path", "content"]
            },
            capabilities={ToolCapability.FS_WRITE},
            tags=["file", "write", "io"],
            examples=["写入配置: path='/tmp/config.conf', content='key=value'"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        path = kwargs.get("path")
        content = kwargs.get("content")
        encoding = kwargs.get("encoding", "utf-8")
        append = kwargs.get("append", False)
        
        try:
            mode = "a" if append else "w"
            
            # 确保目录存在
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, mode, encoding=encoding) as f:
                f.write(content)
            
            return ToolResult(
                success=True,
                data={
                    "path": path,
                    "bytes_written": len(content.encode(encoding)),
                    "mode": "append" if append else "write"
                }
            )
        except PermissionError:
            return ToolResult(success=False, error=f"权限不足: {path}")
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class FileEditTool(BaseTool):
    """文件编辑工具 - 支持正则表达式替换"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="file_edit",
            description="编辑文件内容，支持精确替换和正则替换",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "文件路径"},
                    "old": {"type": "string", "description": "要替换的内容"},
                    "new": {"type": "string", "description": "替换后的内容"},
                    "regex": {"type": "boolean", "default": False, "description": "是否使用正则"},
                    "global": {"type": "boolean", "default": False, "description": "全局替换"}
                },
                "required": ["path", "old", "new"]
            },
            capabilities={ToolCapability.FS_WRITE},
            tags=["file", "edit", "replace"],
            examples=["替换文本: path='/tmp/file.txt', old='old', new='new'"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        import re
        
        path = kwargs.get("path")
        old_text = kwargs.get("old")
        new_text = kwargs.get("new")
        use_regex = kwargs.get("regex", False)
        global_replace = kwargs.get("global", False)
        
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            if use_regex:
                pattern = re.compile(old_text, re.MULTILINE)
                new_content = pattern.sub(new_text, content if global_replace else new_text, count=0 if global_replace else 1)
                replacements = len(pattern.findall(content)) if global_replace else (1 if pattern.search(content) else 0)
            else:
                if global_replace:
                    new_content = content.replace(old_text, new_text)
                    replacements = content.count(old_text)
                else:
                    new_content = content.replace(old_text, new_text, 1)
                    replacements = 1 if old_text in content else 0
            
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            
            return ToolResult(
                success=True,
                data={
                    "path": path,
                    "replacements": replacements,
                    "old_length": len(old_text),
                    "new_length": len(new_text)
                }
            )
        except FileNotFoundError:
            return ToolResult(success=False, error=f"文件不存在: {path}")
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class FileDeleteTool(BaseTool):
    """文件删除工具"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="file_delete",
            description="删除文件或目录",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "文件路径"},
                    "recursive": {"type": "boolean", "default": False, "description": "递归删除目录"}
                },
                "required": ["path"]
            },
            capabilities={ToolCapability.FS_DELETE},
            tags=["file", "delete", "remove"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        path = kwargs.get("path")
        recursive = kwargs.get("recursive", False)
        
        try:
            p = Path(path)
            
            if not p.exists():
                return ToolResult(success=False, error=f"路径不存在: {path}")
            
            if p.is_file():
                p.unlink()
            elif p.is_dir():
                if recursive:
                    shutil.rmtree(p)
                else:
                    p.rmdir()
            
            return ToolResult(
                success=True,
                data={"path": path, "deleted": True}
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class FileGlobTool(BaseTool):
    """文件搜索工具 - Glob 模式"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="file_glob",
            description="使用 glob 模式搜索文件",
            input_schema={
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": "Glob 模式"},
                    "root": {"type": "string", "description": "搜索根目录"},
                    "recursive": {"type": "boolean", "default": True, "description": "递归搜索"},
                    "files_only": {"type": "boolean", "default": True, "description": "只返回文件"}
                },
                "required": ["pattern"]
            },
            capabilities={ToolCapability.FS_READ},
            tags=["file", "glob", "search", "find"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        pattern = kwargs.get("pattern")
        root = kwargs.get("root", ".")
        recursive = kwargs.get("recursive", True)
        files_only = kwargs.get("files_only", True)
        
        try:
            root_path = Path(root)
            if not root_path.exists():
                return ToolResult(success=False, error=f"目录不存在: {root}")
            
            # 构建 glob 模式
            if recursive:
                glob_pattern = "**/" + pattern.lstrip("/")
            else:
                glob_pattern = pattern.lstrip("/")
            
            matches = list(root_path.glob(glob_pattern))
            
            if files_only:
                matches = [m for m in matches if m.is_file()]
            
            results = [str(m.absolute()) for m in matches[:100]]  # 限制100个
            
            return ToolResult(
                success=True,
                data={
                    "matches": results,
                    "count": len(results),
                    "pattern": pattern
                }
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class FileCopyTool(BaseTool):
    """文件复制工具"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="file_copy",
            description="复制文件或目录",
            input_schema={
                "type": "object",
                "properties": {
                    "src": {"type": "string", "description": "源路径"},
                    "dst": {"type": "string", "description": "目标路径"},
                    "overwrite": {"type": "boolean", "default": False}
                },
                "required": ["src", "dst"]
            },
            capabilities={ToolCapability.FS_WRITE},
            tags=["file", "copy", "cp"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        src = kwargs.get("src")
        dst = kwargs.get("dst")
        overwrite = kwargs.get("overwrite", False)
        
        try:
            src_path = Path(src)
            dst_path = Path(dst)
            
            if not src_path.exists():
                return ToolResult(success=False, error=f"源路径不存在: {src}")
            
            if dst_path.exists() and not overwrite:
                return ToolResult(success=False, error=f"目标已存在: {dst}")
            
            if src_path.is_file():
                shutil.copy2(src, dst)
            else:
                if dst_path.exists() and overwrite:
                    shutil.rmtree(dst_path)
                shutil.copytree(src, dst)
            
            return ToolResult(
                success=True,
                data={"src": src, "dst": dst, "copied": True}
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class FileMoveTool(BaseTool):
    """文件移动工具"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="file_move",
            description="移动文件或目录",
            input_schema={
                "type": "object",
                "properties": {
                    "src": {"type": "string", "description": "源路径"},
                    "dst": {"type": "string", "description": "目标路径"},
                    "overwrite": {"type": "boolean", "default": False}
                },
                "required": ["src", "dst"]
            },
            capabilities={ToolCapability.FS_WRITE, ToolCapability.FS_DELETE},
            tags=["file", "move", "mv", "rename"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        src = kwargs.get("src")
        dst = kwargs.get("dst")
        overwrite = kwargs.get("overwrite", False)
        
        try:
            src_path = Path(src)
            dst_path = Path(dst)
            
            if not src_path.exists():
                return ToolResult(success=False, error=f"源路径不存在: {src}")
            
            if dst_path.exists() and not overwrite:
                return ToolResult(success=False, error=f"目标已存在: {dst}")
            
            if dst_path.exists():
                dst_path.unlink()
            
            shutil.move(src, dst)
            
            return ToolResult(
                success=True,
                data={"src": src, "dst": dst, "moved": True}
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class FileInfoTool(BaseTool):
    """文件信息工具"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="file_info",
            description="获取文件或目录的详细信息",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "文件路径"},
                    "stat": {"type": "boolean", "default": True, "description": "获取文件状态"}
                },
                "required": ["path"]
            },
            capabilities={ToolCapability.FS_READ},
            tags=["file", "info", "stat", "metadata"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        path = kwargs.get("path")
        get_stat = kwargs.get("stat", True)
        
        try:
            p = Path(path)
            
            if not p.exists():
                return ToolResult(success=False, error=f"路径不存在: {path}")
            
            info = {
                "path": str(p.absolute()),
                "name": p.name,
                "is_file": p.is_file(),
                "is_dir": p.is_dir(),
                "is_symlink": p.is_symlink(),
                "suffix": p.suffix,
                "stem": p.stem,
            }
            
            if get_stat:
                stat = p.stat()
                info.update({
                    "size": stat.st_size,
                    "size_human": self._human_size(stat.st_size),
                    "created": stat.st_ctime,
                    "modified": stat.st_mtime,
                    "accessed": stat.st_atime,
                    "mode": oct(stat.st_mode),
                })
            
            return ToolResult(success=True, data=info)
        except Exception as e:
            return ToolResult(success=False, error=str(e))
    
    @staticmethod
    def _human_size(size: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}PB"


class FileListTool(BaseTool):
    """目录列表工具"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="file_list",
            description="列出目录内容",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "目录路径"},
                    "all": {"type": "boolean", "default": False, "description": "显示隐藏文件"},
                    "recursive": {"type": "boolean", "default": False, "description": "递归列出"}
                },
                "required": ["path"]
            },
            capabilities={ToolCapability.FS_READ},
            tags=["file", "list", "ls", "directory"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        path = kwargs.get("path")
        show_all = kwargs.get("all", False)
        recursive = kwargs.get("recursive", False)
        
        try:
            p = Path(path)
            
            if not p.exists():
                return ToolResult(success=False, error=f"目录不存在: {path}")
            
            if not p.is_dir():
                return ToolResult(success=False, error=f"不是目录: {path}")
            
            results = []
            
            if recursive:
                for item in p.rglob("*"):
                    if not show_all and item.name.startswith("."):
                        continue
                    results.append({
                        "path": str(item.relative_to(p)),
                        "type": "dir" if item.is_dir() else "file",
                        "name": item.name
                    })
            else:
                for item in p.iterdir():
                    if not show_all and item.name.startswith("."):
                        continue
                    results.append({
                        "name": item.name,
                        "type": "dir" if item.is_dir() else "file"
                    })
            
            return ToolResult(
                success=True,
                data={
                    "entries": results[:100],  # 限制100个
                    "count": len(results),
                    "path": str(p.absolute())
                }
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e))


# 导出所有工具
FILE_TOOLS = [
    FileReadTool,
    FileWriteTool,
    FileEditTool,
    FileDeleteTool,
    FileGlobTool,
    FileCopyTool,
    FileMoveTool,
    FileInfoTool,
    FileListTool,
]


def register_tools(registry):
    """注册所有文件工具到注册表"""
    for tool_class in FILE_TOOLS:
        tool = tool_class()
        registry.register(tool, "file")
    return len(FILE_TOOLS)