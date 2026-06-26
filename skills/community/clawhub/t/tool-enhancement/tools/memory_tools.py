#!/usr/bin/env python3
"""
记忆增强工具集

提供分层记忆、记忆整合、摘要等能力
参考 Claude Code 的 Dream 记忆系统设计
"""

from __future__ import annotations

import asyncio
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from collections import defaultdict

import sys
sys.path.insert(0, str(Path(__file__).parent))
from schema import BaseTool, ToolDefinition, ToolResult, ToolCapability


class MemoryType(Enum):
    """记忆类型"""
    SHORT_TERM = "short_term"      # 短期记忆 (当前 session)
    LONG_TERM = "long_term"        # 长期记忆 (持久化)
    WORKING = "working"            # 工作记忆 (当前任务)
    EPISODIC = "episodic"          # 情景记忆 (事件序列)
    SEMANTIC = "semantic"          # 语义记忆 (知识)


@dataclass
class MemoryEntry:
    """记忆条目"""
    id: str
    content: str
    memory_type: MemoryType
    importance: int = 1  # 1-5
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    accessed_at: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    expires_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class RememberTool(BaseTool):
    """记忆存储工具"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="memory_remember",
            description="存储信息到记忆系统",
            input_schema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "要记忆的内容"},
                    "memory_type": {"type": "string", "enum": ["short_term", "long_term", "working", "episodic", "semantic"], "default": "short_term"},
                    "importance": {"type": "integer", "minimum": 1, "maximum": 5, "default": 1},
                    "tags": {"type": "array", "items": {"type": "string"}, "description": "标签"},
                    "expires_in": {"type": "number", "description": "过期时间(秒)"}
                },
                "required": ["content"]
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["memory", "remember", "store", "save"]
        ))
        self._storage: Dict[str, MemoryEntry] = {}
        self._storage_path = Path.home() / ".openclaw" / "memory" / "entries.json"
        self._load()
    
    def _load(self):
        """加载记忆"""
        if self._storage_path.exists():
            try:
                data = json.loads(self._storage_path.read_text())
                for entry_data in data:
                    entry_data["memory_type"] = MemoryType(entry_data["memory_type"])
                    entry_data["created_at"] = datetime.fromisoformat(entry_data["created_at"])
                    entry_data["accessed_at"] = datetime.fromisoformat(entry_data["accessed_at"])
                    entry = MemoryEntry(**entry_data)
                    self._storage[entry.id] = entry
            except Exception:
                pass
    
    def _save(self):
        """保存记忆"""
        self._storage_path.parent.mkdir(parents=True, exist_ok=True)
        data = []
        for entry in self._storage.values():
            entry_dict = {
                "id": entry.id,
                "content": entry.content,
                "memory_type": entry.memory_type.value,
                "importance": entry.importance,
                "tags": entry.tags,
                "created_at": entry.created_at.isoformat(),
                "accessed_at": entry.accessed_at.isoformat(),
                "access_count": entry.access_count,
                "expires_at": entry.expires_at.isoformat() if entry.expires_at else None,
                "metadata": entry.metadata
            }
            data.append(entry_dict)
        self._storage_path.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    
    async def execute(self, **kwargs) -> ToolResult:
        import uuid
        
        content = kwargs.get("content")
        memory_type_str = kwargs.get("memory_type", "short_term")
        importance = kwargs.get("importance", 1)
        tags = kwargs.get("tags", [])
        expires_in = kwargs.get("expires_in")
        
        try:
            memory_type = MemoryType(memory_type_str)
            
            expires_at = None
            if expires_in:
                expires_at = datetime.now() + timedelta(seconds=expires_in)
            
            entry = MemoryEntry(
                id=str(uuid.uuid4()),
                content=content,
                memory_type=memory_type,
                importance=min(5, max(1, importance)),
                tags=tags,
                expires_at=expires_at
            )
            
            self._storage[entry.id] = entry
            self._save()
            
            return ToolResult(
                success=True,
                data={
                    "id": entry.id,
                    "type": memory_type.value,
                    "importance": importance,
                    "stored": True
                }
            )
            
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class RecallTool(BaseTool):
    """记忆检索工具"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="memory_recall",
            description="从记忆系统中检索信息",
            input_schema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "搜索关键词"},
                    "memory_type": {"type": "string", "description": "记忆类型过滤"},
                    "tags": {"type": "array", "items": {"type": "string"}, "description": "标签过滤"},
                    "limit": {"type": "integer", "default": 10, "description": "返回数量"},
                    "importance": {"type": "integer", "description": "最低重要性"}
                },
                "required": ["query"]
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["memory", "recall", "search", "retrieve"]
        ))
        self._remember_tool: Optional[RememberTool] = None
    
    @property
    def remember_tool(self) -> RememberTool:
        if not self._remember_tool:
            self._remember_tool = RememberTool()
        return self._remember_tool
    
    async def execute(self, **kwargs) -> ToolResult:
        query = kwargs.get("query")
        memory_type_str = kwargs.get("memory_type")
        tags = kwargs.get("tags", [])
        limit = kwargs.get("limit", 10)
        min_importance = kwargs.get("importance", 0)
        
        try:
            query_lower = query.lower()
            results = []
            
            # 检查过期
            now = datetime.now()
            expired_ids = []
            for entry_id, entry in self.remember_tool._storage.items():
                if entry.expires_at and entry.expires_at < now:
                    expired_ids.append(entry_id)
            for eid in expired_ids:
                del self.remember_tool._storage[eid]
            
            # 搜索
            for entry in self.remember_tool._storage.values():
                # 过滤类型
                if memory_type_str and entry.memory_type.value != memory_type_str:
                    continue
                
                # 过滤标签
                if tags and not any(t in entry.tags for t in tags):
                    continue
                
                # 过滤重要性
                if entry.importance < min_importance:
                    continue
                
                # 搜索内容
                if query_lower in entry.content.lower():
                    # 更新访问信息
                    entry.accessed_at = now
                    entry.access_count += 1
                    
                    results.append({
                        "id": entry.id,
                        "content": entry.content,
                        "type": entry.memory_type.value,
                        "importance": entry.importance,
                        "tags": entry.tags,
                        "created_at": entry.created_at.isoformat(),
                        "access_count": entry.access_count
                    })
            
            # 按重要性排序
            results.sort(key=lambda x: x["importance"], reverse=True)
            results = results[:limit]
            
            # 保存更新
            self.remember_tool._save()
            
            return ToolResult(
                success=True,
                data={
                    "results": results,
                    "count": len(results),
                    "query": query
                }
            )
            
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class MemorySummarizeTool(BaseTool):
    """记忆摘要工具 - 参考 Claude Code autoDream"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="memory_summarize",
            description="整合和摘要记忆内容（类似 Dream 的记忆整合）",
            input_schema={
                "type": "object",
                "properties": {
                    "memory_type": {"type": "string", "description": "记忆类型"},
                    "max_entries": {"type": "integer", "default": 20, "description": "最大条目数"},
                    "output_file": {"type": "string", "description": "输出文件路径"}
                }
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["memory", "summarize", "dream", "consolidate"]
        ))
        self._remember_tool: Optional[RememberTool] = None
    
    @property
    def remember_tool(self) -> RememberTool:
        if not self._remember_tool:
            self._remember_tool = RememberTool()
        return self._remember_tool
    
    async def execute(self, **kwargs) -> ToolResult:
        memory_type_str = kwargs.get("memory_type")
        max_entries = kwargs.get("max_entries", 20)
        output_file = kwargs.get("output_file")
        
        try:
            entries = list(self.remember_tool._storage.values())
            
            # 过滤类型
            if memory_type_str:
                memory_type = MemoryType(memory_type_str)
                entries = [e for e in entries if e.memory_type == memory_type]
            
            # 按时间排序
            entries.sort(key=lambda x: x.created_at, reverse=True)
            entries = entries[:max_entries]
            
            # 生成摘要
            summary_parts = [f"# 记忆摘要 ({len(entries)} 条)"]
            summary_parts.append(f"\n生成时间: {datetime.now().isoformat()}\n")
            
            for entry in entries:
                summary_parts.append(f"## {entry.memory_type.value} - {entry.created_at.strftime('%Y-%m-%d %H:%M')}")
                summary_parts.append(f"重要性: {'⭐' * entry.importance}")
                if entry.tags:
                    summary_parts.append(f"标签: {', '.join(entry.tags)}")
                summary_parts.append(f"\n{entry.content}\n")
            
            summary = "\n".join(summary_parts)
            
            # 保存到文件
            if output_file:
                output_path = Path(output_file)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(summary)
            
            return ToolResult(
                success=True,
                data={
                    "summary": summary,
                    "entries_count": len(entries),
                    "output_file": output_file
                }
            )
            
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class MemoryDreamTool(BaseTool):
    """记忆整合工具 - Claude Code autoDream 的简化实现"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="memory_dream",
            description="在空闲时整合记忆，清理过期信息，合并碎片化观察",
            input_schema={
                "type": "object",
                "properties": {
                    "dry_run": {"type": "boolean", "default": False, "description": "仅模拟不实际执行"},
                    "aggressive": {"type": "boolean", "default": False, "description": "激进清理"}
                }
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["memory", "dream", "consolidate", "cleanup"]
        ))
        self._remember_tool: Optional[RememberTool] = None
        self._last_dream: Optional[datetime] = None
    
    @property
    def remember_tool(self) -> RememberTool:
        if not self._remember_tool:
            self._remember_tool = RememberTool()
        return self._remember_tool
    
    async def execute(self, **kwargs) -> ToolResult:
        dry_run = kwargs.get("dry_run", False)
        aggressive = kwargs.get("aggressive", False)
        
        try:
            actions = []
            entries = list(self.remember_tool._storage.values())
            
            now = datetime.now()
            
            # 1. 清理过期记忆
            expired = [e for e in entries if e.expires_at and e.expires_at < now]
            if expired and not dry_run:
                for e in expired:
                    del self.remember_tool._storage[e.id]
                actions.append(f"删除 {len(expired)} 条过期记忆")
            
            # 2. 清理低频访问的记忆（激进模式）
            if aggressive:
                low_freq = [e for e in entries if e.access_count == 0 and e.memory_type == MemoryType.SHORT_TERM]
                if low_freq and not dry_run:
                    for e in low_freq:
                        del self.remember_tool._storage[e.id]
                    actions.append(f"删除 {len(low_freq)} 条未访问记忆")
            
            # 3. 压缩长期记忆（保持 200 行以内）
            long_term = [e for e in entries if e.memory_type == MemoryType.LONG_TERM]
            if len(long_term) > 200:
                # 保留最重要的
                long_term.sort(key=lambda x: x.importance, reverse=True)
                to_delete = long_term[200:]
                if to_delete and not dry_run:
                    for e in to_delete:
                        del self.remember_tool._storage[e.id]
                    actions.append(f"压缩 {len(to_delete)} 条长期记忆")
            
            # 4. 保存
            if not dry_run:
                self.remember_tool._save()
                self._last_dream = now
            
            return ToolResult(
                success=True,
                data={
                    "actions": actions,
                    "dry_run": dry_run,
                    "total_entries": len(entries),
                    "dream_time": now.isoformat() if not dry_run else None
                }
            )
            
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class MemoryContextTool(BaseTool):
    """记忆上下文工具 - 获取当前会话相关的记忆"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="memory_context",
            description="获取与当前任务相关的记忆上下文",
            input_schema={
                "type": "object",
                "properties": {
                    "max_items": {"type": "integer", "default": 5, "description": "最大条目数"},
                    "include_types": {"type": "array", "items": {"type": "string"}, "description": "包含的类型"}
                }
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["memory", "context", "session"]
        ))
        self._remember_tool: Optional[RememberTool] = None
    
    @property
    def remember_tool(self) -> RememberTool:
        if not self._remember_tool:
            self._remember_tool = RememberTool()
        return self._remember_tool
    
    async def execute(self, **kwargs) -> ToolResult:
        max_items = kwargs.get("max_items", 5)
        include_types = kwargs.get("include_types", ["working", "short_term"])
        
        try:
            entries = list(self.remember_tool._storage.values())
            
            # 过滤类型
            if include_types:
                entries = [e for e in entries if e.memory_type.value in include_types]
            
            # 按访问时间和重要性排序
            entries.sort(key=lambda x: (x.accessed_at, x.importance), reverse=True)
            entries = entries[:max_items]
            
            context = {
                "memories": [
                    {
                        "content": e.content,
                        "type": e.memory_type.value,
                        "importance": e.importance
                    }
                    for e in entries
                ],
                "count": len(entries)
            }
            
            return ToolResult(success=True, data=context)
            
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class MemoryStatsTool(BaseTool):
    """记忆统计工具"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="memory_stats",
            description="获取记忆系统统计信息",
            input_schema={
                "type": "object",
                "properties": {}
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["memory", "stats", "info"]
        ))
        self._remember_tool: Optional[RememberTool] = None
    
    @property
    def remember_tool(self) -> RememberTool:
        if not self._remember_tool:
            self._remember_tool = RememberTool()
        return self._remember_tool
    
    async def execute(self, **kwargs) -> ToolResult:
        try:
            entries = list(self.remember_tool._storage.values())
            
            # 按类型统计
            type_counts = defaultdict(int)
            total_importance = 0
            
            for entry in entries:
                type_counts[entry.memory_type.value] += 1
                total_importance += entry.importance
            
            # 计算平均重要性
            avg_importance = total_importance / len(entries) if entries else 0
            
            return ToolResult(
                success=True,
                data={
                    "total": len(entries),
                    "by_type": dict(type_counts),
                    "avg_importance": round(avg_importance, 2),
                    "total_accesses": sum(e.access_count for e in entries)
                }
            )
            
        except Exception as e:
            return ToolResult(success=False, error=str(e))


# 导出所有工具
MEMORY_TOOLS = [
    RememberTool,
    RecallTool,
    MemorySummarizeTool,
    MemoryDreamTool,
    MemoryContextTool,
    MemoryStatsTool,
]


def register_tools(registry):
    """注册所有记忆工具到注册表"""
    for tool_class in MEMORY_TOOLS:
        tool = tool_class()
        registry.register(tool, "memory")
    return len(MEMORY_TOOLS)