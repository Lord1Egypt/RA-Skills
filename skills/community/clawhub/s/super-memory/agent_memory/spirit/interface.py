from __future__ import annotations

import logging
import re
import uuid
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger(__name__)

# Generate UUID-based boundary markers to prevent forgery
_BOUNDARY_UUID = uuid.uuid4().hex[:12]
MEMORY_REPORT_OPEN = f"[MEMORY_REPORT:{_BOUNDARY_UUID}]"
MEMORY_REPORT_CLOSE = f"[/MEMORY_REPORT:{_BOUNDARY_UUID}]"


@dataclass
class WrappedOutput:
    content: str = ""
    confidence: float = 0.0
    source_count: int = 0
    unverified: bool = False
    truncated: bool = False

    def to_string(self) -> str:
        wrapped = f"{MEMORY_REPORT_OPEN}\n{self.content}\n{MEMORY_REPORT_CLOSE}\n"
        wrapped += f"[META:{_BOUNDARY_UUID} confidence={self.confidence:.2f}, sources={self.source_count}, unverified={self.unverified}]"
        if self.truncated:
            wrapped += "\n[TRUNCATED: output exceeded token limit]"
        return wrapped


class SpiritInterface:
    """The ONLY channel between Spirit and core memory engines.

    Dual-LLM Safety Protocol:
    - All outputs are wrapped in UUID-based [MEMORY_REPORT:UUID]...[/MEMORY_REPORT:UUID] markers
    - All outputs include [META:UUID ...] with confidence and source count
    - Unverified content is marked [UNVERIFIED]
    - Token limit enforced (default 500 tokens)
    - UUID-based markers prevent forgery of boundary markers
    """

    READ_OPS = frozenset({
        'recall', 'get_stats', 'get_memories_by_date', 'get_health_status',
        'get_memory', 'get_memories', 'count', 'get_storage_stats',
        'check_integrity', 'get_maintain_stats', 'get_state_distribution',
        'build_self_profile', 'reflect_on_recall', 'should_explore',
        'get_emotion_pattern', 'get_decision_analysis', 'query_awareness',
        'search', 'get_linked', 'get_memory_versions',
    })

    WRITE_OPS = frozenset({
        'merge_memories', 'archive_memories', 'correct_memory', 'create_summary',
        'maintain', 'delete_memory', 'update_memory', 'insert_link',
    })

    MAX_OUTPUT_TOKENS = 500
    _TOKEN_CHARS_RATIO = 2.5

    def __init__(self, store, recall_engine, maintain_engine, cognition_engine, embedding_store):
        self._store = store
        self._recall_engine = recall_engine
        self._maintain_engine = maintain_engine
        self._cognition_engine = cognition_engine
        self._embedding_store = embedding_store

        self._last_confidence: float = 0.0
        self._last_source_count: int = 0
        self._last_unverified: bool = False

    def read(self, operation: str, **kwargs) -> WrappedOutput:
        if operation not in self.READ_OPS:
            return WrappedOutput(
                content=f"[ERROR] Unknown read operation: {operation}",
                confidence=0.0,
                unverified=True,
            )

        self._last_confidence = 0.0
        self._last_source_count = 0
        self._last_unverified = False

        try:
            target = self._resolve_target(operation)
            if target is None:
                return WrappedOutput(
                    content=f"[ERROR] No engine available for: {operation}",
                    confidence=0.0,
                    unverified=True,
                )

            method = getattr(target, operation, None)
            if method is None:
                return WrappedOutput(
                    content=f"[ERROR] Operation not found: {operation}",
                    confidence=0.0,
                    unverified=True,
                )

            raw_result = method(**kwargs)
            content = self._serialize_result(raw_result)
            self._assess_confidence(operation, raw_result)

            content = self._enforce_token_limit(content)
            return WrappedOutput(
                content=content,
                confidence=self._last_confidence,
                source_count=self._last_source_count,
                unverified=self._last_unverified,
            )

        except Exception as e:
            logger.error("SpiritInterface.read(%s): %s", operation, e)
            return WrappedOutput(
                content=f"[ERROR] Read operation failed: {e}",
                confidence=0.0,
                unverified=True,
            )

    def write(self, operation: str, confirm: bool = False, **kwargs) -> WrappedOutput:
        if operation not in self.WRITE_OPS:
            return WrappedOutput(
                content=f"[ERROR] Unknown write operation: {operation}",
                confidence=0.0,
                unverified=True,
            )

        if not confirm:
            return self._preview(operation, **kwargs)

        return self._execute_write(operation, **kwargs)

    def recall(self, query: str = None, keyword: str = None, limit: int = 20, **kwargs) -> WrappedOutput:
        return self.read('recall', query=query, keyword=keyword, limit=limit, **kwargs)

    def query_awareness(self, topic: str) -> WrappedOutput:
        if not self._recall_engine:
            return WrappedOutput(content="[ERROR] No recall engine", confidence=0.0, unverified=True)

        try:
            result = self._recall_engine.recall(query=topic, limit=10, assess_awareness=True)
            awareness = getattr(result, 'awareness', None)
            if awareness is None:
                awareness_dict = {}
            else:
                awareness_dict = awareness.to_dict() if hasattr(awareness, 'to_dict') else {}

            self._last_confidence = awareness_dict.get('confidence', 0.0)
            self._last_source_count = result.total if hasattr(result, 'total') else 0
            self._last_unverified = awareness_dict.get('status', '') in ('no_knowledge', 'low_relevance')

            content = self._serialize_result(awareness_dict)
            content = self._enforce_token_limit(content)
            return WrappedOutput(
                content=content,
                confidence=self._last_confidence,
                source_count=self._last_source_count,
                unverified=self._last_unverified,
            )
        except Exception as e:
            logger.error("SpiritInterface.query_awareness: %s", e)
            return WrappedOutput(content=f"[ERROR] {e}", confidence=0.0, unverified=True)

    def get_stats(self) -> WrappedOutput:
        parts = {}
        if self._store:
            try:
                parts['storage'] = self._store.get_storage_stats()
            except Exception as e:
                parts['storage'] = f"[ERROR: {e}]"
        if self._recall_engine:
            try:
                parts['recall'] = self._recall_engine.get_stats()
            except Exception as e:
                parts['recall'] = f"[ERROR: {e}]"
        if self._maintain_engine:
            try:
                parts['maintain'] = self._maintain_engine.get_maintain_stats()
            except Exception as e:
                parts['maintain'] = f"[ERROR: {e}]"

        self._last_confidence = 1.0
        self._last_source_count = len(parts)
        self._last_unverified = False

        content = self._serialize_result(parts)
        content = self._enforce_token_limit(content)
        return WrappedOutput(
            content=content,
            confidence=self._last_confidence,
            source_count=self._last_source_count,
            unverified=self._last_unverified,
        )

    def _resolve_target(self, operation: str):
        _STORE_OPS = {'get_memory', 'get_memories', 'count', 'get_storage_stats',
                       'check_integrity', 'get_linked', 'get_memory_versions',
                       'get_memories_by_date', 'query'}
        _RECALL_OPS = {'recall', 'get_stats'}
        _MAINTAIN_OPS = {'get_maintain_stats', 'get_state_distribution', 'get_health_status'}
        _COGNITION_OPS = {'build_self_profile', 'reflect_on_recall', 'should_explore',
                          'get_emotion_pattern', 'get_decision_analysis'}
        _EMBEDDING_OPS = {'search'}

        if operation in _STORE_OPS:
            return self._store
        if operation in _RECALL_OPS:
            return self._recall_engine
        if operation in _MAINTAIN_OPS:
            return self._maintain_engine
        if operation in _COGNITION_OPS:
            return self._cognition_engine
        if operation in _EMBEDDING_OPS:
            return self._embedding_store
        return None

    def _preview(self, operation: str, **kwargs) -> WrappedOutput:
        preview_info = {
            'operation': operation,
            'status': 'PREVIEW',
            'message': f'Will execute write operation: {operation}',
            'kwargs_keys': list(kwargs.keys()),
        }

        if operation == 'maintain' and self._maintain_engine:
            try:
                dry_result = self._maintain_engine.maintain(
                    operations=kwargs.get('operations', ['all']),
                    dry_run=True,
                    agent_id=kwargs.get('agent_id'),
                )
                preview_info['dry_run_result'] = dry_result
            except Exception as e:
                preview_info['dry_run_error'] = str(e)

        if operation == 'delete_memory' and self._store:
            mid = kwargs.get('memory_id', '')
            mem = self._store.get_memory(mid) if mid else None
            if mem:
                preview_info['target_content_preview'] = mem.get('content', '')[:100]
                preview_info['target_importance'] = mem.get('importance', '')

        content = self._serialize_result(preview_info)
        return WrappedOutput(
            content=content,
            confidence=0.5,
            source_count=0,
            unverified=False,
        )

    def _execute_write(self, operation: str, **kwargs) -> WrappedOutput:
        try:
            target = self._resolve_write_target(operation)
            if target is None:
                return WrappedOutput(
                    content=f"[ERROR] No engine for write: {operation}",
                    confidence=0.0,
                    unverified=True,
                )

            method = getattr(target, operation, None)
            if method is None:
                return WrappedOutput(
                    content=f"[ERROR] Write method not found: {operation}",
                    confidence=0.0,
                    unverified=True,
                )

            raw_result = method(**kwargs)
            content = self._serialize_result(raw_result)

            self._last_confidence = 1.0
            self._last_source_count = 1
            self._last_unverified = False

            content = self._enforce_token_limit(content)
            return WrappedOutput(
                content=content,
                confidence=self._last_confidence,
                source_count=self._last_source_count,
                unverified=self._last_unverified,
            )

        except Exception as e:
            logger.error("SpiritInterface.write(%s): %s", operation, e)
            return WrappedOutput(
                content=f"[ERROR] Write operation failed: {e}",
                confidence=0.0,
                unverified=True,
            )

    def _resolve_write_target(self, operation: str):
        _STORE_WRITES = {'delete_memory', 'update_memory', 'insert_link'}
        _MAINTAIN_WRITES = {'maintain', 'merge_memories', 'archive_memories', 'correct_memory', 'create_summary'}

        if operation in _STORE_WRITES:
            return self._store
        if operation in _MAINTAIN_WRITES:
            return self._maintain_engine
        return None

    def _assess_confidence(self, operation: str, result):
        if result is None:
            self._last_confidence = 0.0
            self._last_unverified = True
            return

        if operation == 'recall':
            total = getattr(result, 'total', 0) if hasattr(result, 'total') else 0
            self._last_source_count = total
            awareness = getattr(result, 'awareness', None) if hasattr(result, 'awareness') else None
            if awareness:
                self._last_confidence = getattr(awareness, 'confidence', 0.0)
                status = getattr(awareness, 'status', '')
                self._last_unverified = status in ('no_knowledge', 'low_relevance', 'low_confidence')
            else:
                self._last_confidence = min(1.0, total / 10.0) if total > 0 else 0.0
                self._last_unverified = total == 0
        elif operation == 'search':
            if isinstance(result, list):
                self._last_source_count = len(result)
                self._last_confidence = min(1.0, len(result) / 5.0) if result else 0.0
                self._last_unverified = len(result) == 0
        elif operation in ('get_stats', 'get_maintain_stats', 'get_storage_stats'):
            self._last_confidence = 1.0
            self._last_unverified = False
            if isinstance(result, dict):
                self._last_source_count = len(result)
        else:
            self._last_confidence = 0.7
            self._last_unverified = False

    def _enforce_token_limit(self, text: str) -> str:
        if not text:
            return text

        max_chars = int(self.MAX_OUTPUT_TOKENS * self._TOKEN_CHARS_RATIO)
        if len(text) <= max_chars:
            return text

        truncated = text[:max_chars]
        last_newline = truncated.rfind('\n')
        if last_newline > max_chars * 0.5:
            truncated = truncated[:last_newline]

        return truncated + "\n...[truncated]"

    def _serialize_result(self, result) -> str:
        if result is None:
            return "[EMPTY]"
        if isinstance(result, str):
            return result
        if isinstance(result, (int, float, bool)):
            return str(result)
        if isinstance(result, dict):
            return self._dict_to_readable(result)
        if isinstance(result, list):
            if not result:
                return "[EMPTY LIST]"
            if isinstance(result[0], dict):
                lines = []
                for i, item in enumerate(result[:20]):
                    lines.append(self._dict_to_readable(item, indent=1))
                if len(result) > 20:
                    lines.append(f"  ... and {len(result) - 20} more")
                return "\n".join(lines)
            return "\n".join(str(item) for item in result[:30])
        if hasattr(result, 'to_dict'):
            return self._dict_to_readable(result.to_dict())
        return str(result)

    def _dict_to_readable(self, d: dict, indent: int = 0) -> str:
        prefix = "  " * indent
        lines = []
        for key, value in d.items():
            if isinstance(value, dict):
                lines.append(f"{prefix}{key}:")
                lines.append(self._dict_to_readable(value, indent + 1))
            elif isinstance(value, list):
                if not value:
                    lines.append(f"{prefix}{key}: []")
                elif isinstance(value[0], dict):
                    lines.append(f"{prefix}{key}: [{len(value)} items]")
                else:
                    preview = ", ".join(str(v) for v in value[:5])
                    if len(value) > 5:
                        preview += f" ... (+{len(value) - 5})"
                    lines.append(f"{prefix}{key}: [{preview}]")
            else:
                val_str = str(value)
                if len(val_str) > 120:
                    val_str = val_str[:120] + "..."
                lines.append(f"{prefix}{key}: {val_str}")
        return "\n".join(lines)
