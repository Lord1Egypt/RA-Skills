from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from typing import Optional

from .dag import TaskDAG
from .node import TCCNode


def _human_time(iso: str) -> str:
    try:
        then = datetime.fromisoformat(iso)
        now = datetime.now(timezone.utc)
        delta = now - then
        seconds = int(delta.total_seconds())
        if seconds < 60:
            return "just now"
        if seconds < 3600:
            return f"{seconds // 60} minutes ago"
        if seconds < 86400:
            return f"{seconds // 3600} hours ago"
        days = seconds // 86400
        if days == 1:
            return "yesterday"
        if days < 7:
            return f"{days} days ago"
        if days < 30:
            return f"{days // 7} weeks ago"
        if days < 365:
            return f"{days // 30} months ago"
        return f"{days // 365} years ago"
    except Exception:
        return iso


class SessionReconciler:
    def start_session(
        self,
        dag: TaskDAG,
        n_recent: int = 10,
        search_query: str | None = None,
        n_search: int = 5,
    ) -> dict:
        session_id = uuid.uuid4().hex[:12]
        tip = dag.tip()
        is_fresh = tip is None

        if is_fresh:
            summary = "No history yet. Starting fresh."
        else:
            summary = self._build_summary(
                dag,
                tip,
                n_recent=n_recent,
                search_query=search_query,
                n_search=n_search,
            )

        dag.append(
            event="session start",
            actor="system",
            session_id=session_id,
            node_type="milestone",
            session_key=f"agent:raven:{session_id}",
            subtype="start",
            status="running",
        )

        return {
            "session_id": session_id,
            "summary": summary,
            "tip": tip,
            "is_fresh": is_fresh,
        }

    def _build_summary(
        self,
        dag: TaskDAG,
        tip: TCCNode,
        n_recent: int = 10,
        search_query: str | None = None,
        n_search: int = 5,
    ) -> str:
        recent = dag.recent(n_recent)
        lines = [f"Last active: {_human_time(tip.timestamp)}", "", "Recent events:"]
        for node in recent[:7]:
            lines.append(f"  [{node.actor}] {node.event} ({_human_time(node.timestamp)})")
            if node.result_summary:
                lines.append(f"    → {node.result_summary}")
            elif node.summary:
                lines.append(f"    → {node.summary}")

        for node in recent:
            if node.open_threads:
                try:
                    threads = json.loads(node.open_threads)
                except json.JSONDecodeError:
                    continue
                if isinstance(threads, list) and threads:
                    lines.append("")
                    lines.append(f"Open threads: {', '.join(str(t) for t in threads)}")
                    break

        semantic_nodes = []
        if search_query and dag._store.is_vec_enabled:
            semantic_nodes = dag._store.search(search_query, n=n_search)
            recent_hashes = {n.hash for n in recent}
            semantic_nodes = [n for n in semantic_nodes if n.hash not in recent_hashes]

        if semantic_nodes:
            lines.append("")
            lines.append("Relevant historical context:")
            for node in semantic_nodes:
                lines.append(f"  [{node.actor}] {node.event}")

        return "\n".join(lines)

    def end_session(self, dag: TaskDAG, session_id: str, notes: str = "") -> Optional[TCCNode]:
        session_nodes = dag.since(session_id)
        if not session_nodes:
            return None
        return dag.append(
            event="session end",
            actor="system",
            session_id=session_id,
            node_type="milestone",
            session_key=f"agent:raven:{session_id}",
            subtype="end",
            summary=notes[:1000] if notes else None,
            status="done",
        )

    def record_event(
        self,
        dag: TaskDAG,
        session_id: str,
        event: str,
        actor: str,
        status: str = "done",
        node_type: str | None = None,
        session_key: str | None = None,
        subtype: str | None = None,
        result_summary: str | None = None,
        tool_name: str | None = None,
        transcript_ref: str | None = None,
    ) -> TCCNode:
        resolved_node_type = node_type or ("milestone" if actor == "system" else "action")
        if dag.tip() is None:
            return dag.root(event, actor, session_id)
        return dag.append(
            event=event,
            actor=actor,
            session_id=session_id,
            status=status,
            node_type=resolved_node_type,
            session_key=session_key or f"agent:raven:{session_id}",
            subtype=subtype,
            result_summary=result_summary,
            tool_name=tool_name,
            transcript_ref=transcript_ref,
        )

    def record_note(self, dag: TaskDAG, session_id: str, note: str) -> TCCNode:
        return dag.append(
            event=note[:120],
            actor="agent",
            session_id=session_id,
            node_type="decided",
            session_key=f"agent:raven:{session_id}",
            content=note[:500],
            trigger="explicit",
            status="done",
        )

    def record_tool_call(
        self,
        dag: TaskDAG,
        session_id: str,
        tool: str,
        params: dict,
        result: dict,
        status: str = "done",
    ) -> TCCNode:
        return self.record_event(
            dag,
            session_id,
            event=f"{tool} called",
            actor="tool",
            status=status,
            tool_name=tool,
            result_summary=str(result)[:200],
        )
