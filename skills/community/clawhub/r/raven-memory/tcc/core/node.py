from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class TCCNode:
    hash: str
    node_type: str
    timestamp: str
    actor: str
    session_key: str
    session_id: str
    event: str
    status: str
    branch_id: str
    transcript_ref: str | None = None
    tool_name: str | None = None
    tool_args_hash: str | None = None
    duration_ms: int | None = None
    result_summary: str | None = None
    file_path: str | None = None
    content: str | None = None
    trigger: str | None = None
    subtype: str | None = None
    summary: str | None = None
    open_threads: str | None = None
    token_count: int | None = None

    @staticmethod
    def _truncate(value: str | None, max_len: int) -> str | None:
        if value is None or len(value) <= max_len:
            return value
        return value[:max_len] + "…"

    @staticmethod
    def compute_hash(
        timestamp: str,
        session_id: str,
        event: str,
        node_type: str,
    ) -> str:
        content = f"{timestamp}{session_id}{event}{node_type}"
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    @classmethod
    def create(
        cls,
        node_type: str,
        timestamp: str,
        actor: str,
        session_key: str,
        session_id: str,
        event: str,
        status: str,
        branch_id: str = "main",
        transcript_ref: str | None = None,
        tool_name: str | None = None,
        tool_args_hash: str | None = None,
        duration_ms: int | None = None,
        result_summary: str | None = None,
        file_path: str | None = None,
        content: str | None = None,
        trigger: str | None = None,
        subtype: str | None = None,
        summary: str | None = None,
        open_threads: str | None = None,
        token_count: int | None = None,
        **_: Any,
    ) -> "TCCNode":
        event = cls._truncate(event, 120) or ""
        result_summary = cls._truncate(result_summary, 200)
        content = cls._truncate(content, 500)
        summary = cls._truncate(summary, 1000)

        h = cls.compute_hash(
            timestamp=timestamp,
            session_id=session_id,
            event=event,
            node_type=node_type,
        )
        return cls(
            hash=h,
            node_type=node_type,
            timestamp=timestamp,
            actor=actor,
            session_key=session_key,
            session_id=session_id,
            event=event,
            status=status,
            branch_id=branch_id,
            transcript_ref=transcript_ref,
            tool_name=tool_name,
            tool_args_hash=tool_args_hash,
            duration_ms=duration_ms,
            result_summary=result_summary,
            file_path=file_path,
            content=content,
            trigger=trigger,
            subtype=subtype,
            summary=summary,
            open_threads=open_threads,
            token_count=token_count,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "hash": self.hash,
            "node_type": self.node_type,
            "timestamp": self.timestamp,
            "actor": self.actor,
            "session_key": self.session_key,
            "session_id": self.session_id,
            "event": self.event,
            "status": self.status,
            "branch_id": self.branch_id,
            "transcript_ref": self.transcript_ref,
            "tool_name": self.tool_name,
            "tool_args_hash": self.tool_args_hash,
            "duration_ms": self.duration_ms,
            "result_summary": self.result_summary,
            "file_path": self.file_path,
            "content": self.content,
            "trigger": self.trigger,
            "subtype": self.subtype,
            "summary": self.summary,
            "open_threads": self.open_threads,
            "token_count": self.token_count,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "TCCNode":
        return cls(
            hash=payload["hash"],
            node_type=payload["node_type"],
            timestamp=payload["timestamp"],
            actor=payload["actor"],
            session_key=payload["session_key"],
            session_id=payload["session_id"],
            event=payload["event"],
            status=payload["status"],
            branch_id=payload.get("branch_id", "main"),
            transcript_ref=payload.get("transcript_ref"),
            tool_name=payload.get("tool_name"),
            tool_args_hash=payload.get("tool_args_hash"),
            duration_ms=payload.get("duration_ms"),
            result_summary=payload.get("result_summary"),
            file_path=payload.get("file_path"),
            content=payload.get("content"),
            trigger=payload.get("trigger"),
            subtype=payload.get("subtype"),
            summary=payload.get("summary"),
            open_threads=payload.get("open_threads"),
            token_count=payload.get("token_count"),
        )
