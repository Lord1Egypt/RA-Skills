from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from typing import Optional

from .node import TCCNode
from .store import DAGError, NodeNotFoundError, TCCStore


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class TaskDAG:
    def __init__(self, store: TCCStore):
        self._store = store
        self._store._on_status_update = self._on_status_update
        self._index: dict[str, TCCNode] = {}
        self._parents: dict[str, list[str]] = {}
        self._tip_hash: Optional[str] = None
        self._branches: dict[str, str] = {}  # branch_id -> tip_hash
        self._load()

    def _load(self):
        nodes = self._store.load_all()
        for n in nodes:
            self._index[n.hash] = n
            self._parents[n.hash] = self._store.get_parents(n.hash)
        self._tip_hash = self._store.get_meta("tip_hash")
        self._branches = self._store.get_all_branches()

    def _save_node(self, node: TCCNode, parent_hashes: list[str]) -> None:
        self._store.save_node(node, parent_hashes)
        self._index[node.hash] = node
        self._parents[node.hash] = parent_hashes

    def _on_status_update(self, hash: str, status: str) -> None:
        if hash in self._index:
            old = self._index[hash]
            updated = TCCNode(
                hash=old.hash,
                node_type=old.node_type,
                timestamp=old.timestamp,
                actor=old.actor,
                session_key=old.session_key,
                session_id=old.session_id,
                event=old.event,
                status=status,
                branch_id=old.branch_id,
                transcript_ref=old.transcript_ref,
                tool_name=old.tool_name,
                tool_args_hash=old.tool_args_hash,
                duration_ms=old.duration_ms,
                result_summary=old.result_summary,
                file_path=old.file_path,
                content=old.content,
                trigger=old.trigger,
                subtype=old.subtype,
                summary=old.summary,
                open_threads=old.open_threads,
                token_count=old.token_count,
            )
            self._index[hash] = updated
        self._auto_merge_check()

    def root(self, event: str, actor: str, session_id: str) -> TCCNode:
        if self._tip_hash is not None:
            raise DAGError("Root already exists")
        node = TCCNode.create(
            node_type="action",
            timestamp=_now(),
            event=event,
            actor=actor,
            status="done",
            session_key=f"agent:raven:{session_id}",
            session_id=session_id,
            branch_id="main",
        )
        self._save_node(node, [])
        self._tip_hash = node.hash
        self._store.set_meta("tip_hash", node.hash)
        self._store.set_meta("root_hash", node.hash)
        return node

    def append(
        self,
        event: str,
        actor: str,
        session_id: str,
        parent_hash: Optional[str] = None,
        status: str = "done",
        node_type: str = "action",
        session_key: str | None = None,
        tool_name: str | None = None,
        result_summary: str | None = None,
        transcript_ref: str | None = None,
        subtype: str | None = None,
        summary: str | None = None,
        content: str | None = None,
        trigger: str | None = None,
        open_threads: str | None = None,
        duration_ms: int | None = None,
        token_count: int | None = None,
        file_path: str | None = None,
    ) -> TCCNode:
        parent = parent_hash or self._tip_hash
        if parent and parent not in self._index:
            raise NodeNotFoundError(f"Parent {parent} not found")
        parent_hashes = [parent] if parent else []
        node = TCCNode.create(
            node_type=node_type,
            timestamp=_now(),
            event=event,
            actor=actor,
            status=status,
            session_key=session_key or f"agent:raven:{session_id}",
            session_id=session_id,
            branch_id="main",
            transcript_ref=transcript_ref,
            tool_name=tool_name,
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
        self._save_node(node, parent_hashes)
        self._tip_hash = node.hash
        self._store.set_meta("tip_hash", node.hash)
        return node

    def branch(
        self,
        from_hash: str,
        event: str,
        actor: str,
        session_id: str,
        status: str = "running",
        node_type: str = "action",
        session_key: str | None = None,
        tool_name: str | None = None,
        transcript_ref: str | None = None,
        result_summary: str | None = None,
    ) -> tuple[TCCNode, str]:
        if from_hash not in self._index:
            raise NodeNotFoundError(f"Node {from_hash} not found")
        branch_id = uuid.uuid4().hex[:8]
        while branch_id == "main" or branch_id in self._branches:
            branch_id = uuid.uuid4().hex[:8]
        parent_hashes = [from_hash]
        node = TCCNode.create(
            node_type=node_type,
            timestamp=_now(),
            event=event,
            actor=actor,
            status=status,
            session_key=session_key or f"agent:raven:{session_id}",
            session_id=session_id,
            branch_id=branch_id,
            transcript_ref=transcript_ref,
            tool_name=tool_name,
            result_summary=result_summary,
        )
        self._save_node(node, parent_hashes)
        self._branches[branch_id] = node.hash
        self._store.set_branch_tip(branch_id, node.hash)
        return node, branch_id

    def branch_from_tip(self, session_id: str) -> str:
        if not self._tip_hash:
            raise DAGError("Cannot branch from empty DAG")
        branch_id = uuid.uuid4().hex[:8]
        while branch_id == "main" or branch_id in self._branches:
            branch_id = uuid.uuid4().hex[:8]
        self._branches[branch_id] = self._tip_hash
        self._store.set_branch_tip(branch_id, self._tip_hash)
        return branch_id

    def merge(
        self,
        branch_hashes: list[str],
        event: str = "merged parallel branches",
        session_id: str = "system",
    ) -> TCCNode:
        for h in branch_hashes:
            if h not in self._index:
                raise NodeNotFoundError(f"Branch tip {h} not found")

        all_parents = list(dict.fromkeys(([self._tip_hash] if self._tip_hash else []) + branch_hashes))

        merge_node = TCCNode.create(
            node_type="milestone",
            timestamp=_now(),
            event=event,
            actor="system",
            status="done",
            session_key=f"agent:raven:{session_id}",
            session_id=session_id,
            branch_id="main",
            subtype="merge",
        )
        self._save_node(merge_node, all_parents)
        self._tip_hash = merge_node.hash
        self._store.set_meta("tip_hash", merge_node.hash)

        for bid in list(self._branches.keys()):
            if self._branches[bid] in branch_hashes:
                self._store.mark_branch_merged(bid)
                del self._branches[bid]

        return merge_node

    def update_status(self, hash: str, status: str) -> None:
        self._store.update_status(hash, status)

    def _auto_merge_check(self) -> Optional[TCCNode]:
        if not self._branches:
            return None

        branch_tips = {bid: self._index.get(h) for bid, h in self._branches.items()}

        for tip_node in branch_tips.values():
            if tip_node is None:
                return None
            if tip_node.status not in ("done", "failed"):
                return None

        branch_tip_hashes = list(self._branches.values())
        branch_events = [self._index[h].event for h in branch_tip_hashes if h in self._index]
        merge_event = f"merged: {', '.join(branch_events)}"
        session_id = next((self._index[h].session_id for h in branch_tip_hashes if h in self._index), "system")

        all_parents = list(dict.fromkeys(([self._tip_hash] if self._tip_hash else []) + branch_tip_hashes))

        merge_node = TCCNode.create(
            node_type="milestone",
            timestamp=_now(),
            event=merge_event,
            actor="system",
            status="done",
            session_key=f"agent:raven:{session_id}",
            session_id=session_id,
            branch_id="main",
            subtype="merge",
        )
        self._save_node(merge_node, all_parents)
        self._tip_hash = merge_node.hash
        self._store.set_meta("tip_hash", merge_node.hash)

        for bid in list(self._branches.keys()):
            self._store.mark_branch_merged(bid)
        self._branches.clear()

        return merge_node

    def rollback(self, n: int = 1) -> TCCNode:
        if not self._tip_hash:
            raise DAGError("Empty DAG, cannot rollback")
        current = self._index[self._tip_hash]
        for i in range(n):
            parents = self._parents.get(current.hash, [])
            if not parents:
                raise DAGError(f"Cannot rollback {n} hops, only {i} available")
            current = self._index[parents[0]]
        self._tip_hash = current.hash
        self._store.set_meta("tip_hash", current.hash)

        stale = []
        for bid, tip_hash in self._branches.items():
            if not self.is_ancestor_of_tip(tip_hash):
                stale.append(bid)
        for bid in stale:
            self._store.mark_branch_merged(bid)
            del self._branches[bid]

        return current

    def tip(self) -> Optional[TCCNode]:
        if not self._tip_hash:
            return None
        return self._index.get(self._tip_hash)

    def get(self, hash: str) -> TCCNode:
        if hash not in self._index:
            raise NodeNotFoundError(f"Node {hash} not found")
        return self._index[hash]

    def recent(self, n: int = 10) -> list[TCCNode]:
        if not self._tip_hash:
            return []
        result = []
        seen = set()
        frontier = [self._index[self._tip_hash]] if self._tip_hash in self._index else []
        while frontier and len(result) < n:
            frontier.sort(key=lambda node: node.timestamp, reverse=True)
            current = frontier.pop(0)
            if current.hash in seen:
                continue
            seen.add(current.hash)
            result.append(current)
            for ph in self._parents.get(current.hash, []):
                if ph in self._index and ph not in seen:
                    frontier.append(self._index[ph])
        return result

    def since(self, session_id: str) -> list[TCCNode]:
        return [n for n in self._index.values() if n.session_id == session_id]

    def path(self, from_hash: str, to_hash: str) -> list[TCCNode]:
        if from_hash not in self._index or to_hash not in self._index:
            return []
        from collections import deque

        queue = deque([[from_hash]])
        visited = {from_hash}
        while queue:
            path = queue.popleft()
            node = self._index[path[-1]]
            if node.hash == to_hash:
                return [self._index[h] for h in path]
            for child in self._get_children(node.hash):
                if child not in visited:
                    visited.add(child)
                    queue.append(path + [child])
        return []

    def _get_children(self, hash: str) -> list[str]:
        return self._store.get_children(hash)

    def is_ancestor_of_tip(self, hash: str) -> bool:
        if not self._tip_hash:
            return False
        visited = set()
        stack = [self._tip_hash]
        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)
            if current == hash:
                return True
            for parent_hash in self._parents.get(current, []):
                if parent_hash not in visited:
                    stack.append(parent_hash)
        return False

    def summary(self, n: int = 10) -> str:
        tip = self.tip()
        if tip is None:
            return "No history yet."

        recent = self.recent(n)
        lines = [f"Last active: {self._human_time(tip.timestamp)}", "", "Recent events:"]
        for node in recent:
            lines.append(f"  [{node.actor}] {node.event} ({self._human_time(node.timestamp)})")
            if node.result_summary:
                lines.append(f"    → {node.result_summary}")
            elif node.subtype:
                lines.append(f"    → subtype: {node.subtype}")

        open_threads: list[str] = []
        for node in recent:
            if node.node_type == "milestone" and node.open_threads:
                try:
                    parsed = json.loads(node.open_threads)
                    if isinstance(parsed, list):
                        open_threads = [str(item) for item in parsed]
                        break
                except json.JSONDecodeError:
                    continue

        if open_threads:
            lines.append("")
            lines.append(f"Open threads: {', '.join(open_threads)}")

        return "\n".join(lines)

    @staticmethod
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
