"""Supabase REST-based LangGraph Checkpointer.

Persists graph state via Supabase PostgREST API — no direct Postgres connection needed.
Survives Railway redeploys (data in Supabase, not ephemeral filesystem).
"""

import json
import logging
from typing import Any, Iterator, Optional, Sequence

from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.base import (
    BaseCheckpointSaver,
    ChannelVersions,
    Checkpoint,
    CheckpointMetadata,
    CheckpointTuple,
    PendingWrite,
)

log = logging.getLogger("supabase_checkpointer")


class SupabaseCheckpointer(BaseCheckpointSaver):
    """LangGraph checkpointer backed by Supabase REST API."""

    def __init__(self, client):
        super().__init__()
        self.client = client

    def put(
        self,
        config: RunnableConfig,
        checkpoint: Checkpoint,
        metadata: CheckpointMetadata,
        new_versions: ChannelVersions,
    ) -> RunnableConfig:
        thread_id = config["configurable"]["thread_id"]
        checkpoint_ns = config["configurable"].get("checkpoint_ns", "")
        checkpoint_id = checkpoint["id"]
        parent_id = config["configurable"].get("checkpoint_id")

        row = {
            "thread_id": thread_id,
            "checkpoint_ns": checkpoint_ns,
            "checkpoint_id": checkpoint_id,
            "parent_checkpoint_id": parent_id,
            "type": "json",
            "checkpoint": self._serialize(checkpoint),
            "metadata": self._serialize(metadata),
        }

        try:
            self.client.table("langgraph_checkpoints").upsert(row).execute()
        except Exception as e:
            log.error(f"Failed to save checkpoint: {e}")

        return {
            "configurable": {
                "thread_id": thread_id,
                "checkpoint_ns": checkpoint_ns,
                "checkpoint_id": checkpoint_id,
            }
        }

    def put_writes(
        self,
        config: RunnableConfig,
        writes: Sequence[tuple[str, Any]],
        task_id: str,
    ) -> None:
        thread_id = config["configurable"]["thread_id"]
        checkpoint_ns = config["configurable"].get("checkpoint_ns", "")
        checkpoint_id = config["configurable"]["checkpoint_id"]

        rows = []
        for idx, (channel, value) in enumerate(writes):
            rows.append({
                "thread_id": thread_id,
                "checkpoint_ns": checkpoint_ns,
                "checkpoint_id": checkpoint_id,
                "task_id": task_id,
                "idx": idx,
                "channel": channel,
                "type": "json",
                "blob": self._serialize(value),
            })

        if rows:
            try:
                self.client.table("langgraph_writes").upsert(rows).execute()
            except Exception as e:
                log.error(f"Failed to save writes: {e}")

    def get_tuple(self, config: RunnableConfig) -> Optional[CheckpointTuple]:
        thread_id = config["configurable"]["thread_id"]
        checkpoint_ns = config["configurable"].get("checkpoint_ns", "")
        checkpoint_id = config["configurable"].get("checkpoint_id")

        try:
            query = (
                self.client.table("langgraph_checkpoints")
                .select("*")
                .eq("thread_id", thread_id)
                .eq("checkpoint_ns", checkpoint_ns)
            )
            if checkpoint_id:
                query = query.eq("checkpoint_id", checkpoint_id)
            else:
                query = query.order("created_at", desc=True).limit(1)

            result = query.execute()

            if not result.data:
                return None

            row = result.data[0]
            checkpoint = self._deserialize(row["checkpoint"])
            metadata = self._deserialize(row.get("metadata", "{}"))

            parent_config = None
            if row.get("parent_checkpoint_id"):
                parent_config = {
                    "configurable": {
                        "thread_id": thread_id,
                        "checkpoint_ns": checkpoint_ns,
                        "checkpoint_id": row["parent_checkpoint_id"],
                    }
                }

            # Fetch pending writes
            writes_result = (
                self.client.table("langgraph_writes")
                .select("*")
                .eq("thread_id", thread_id)
                .eq("checkpoint_ns", checkpoint_ns)
                .eq("checkpoint_id", row["checkpoint_id"])
                .order("idx")
                .execute()
            )

            pending_writes = []
            for w in writes_result.data or []:
                pending_writes.append(
                    (w["task_id"], w["channel"], self._deserialize(w.get("blob")))
                )

            return CheckpointTuple(
                config={
                    "configurable": {
                        "thread_id": thread_id,
                        "checkpoint_ns": checkpoint_ns,
                        "checkpoint_id": row["checkpoint_id"],
                    }
                },
                checkpoint=checkpoint,
                metadata=metadata,
                parent_config=parent_config,
                pending_writes=pending_writes,
            )
        except Exception as e:
            log.error(f"Failed to get checkpoint: {e}")
            return None

    def list(
        self,
        config: Optional[RunnableConfig],
        *,
        filter: Optional[dict[str, Any]] = None,
        before: Optional[RunnableConfig] = None,
        limit: Optional[int] = None,
    ) -> Iterator[CheckpointTuple]:
        if not config:
            return

        thread_id = config["configurable"]["thread_id"]
        checkpoint_ns = config["configurable"].get("checkpoint_ns", "")

        try:
            query = (
                self.client.table("langgraph_checkpoints")
                .select("*")
                .eq("thread_id", thread_id)
                .eq("checkpoint_ns", checkpoint_ns)
                .order("created_at", desc=True)
            )

            if before:
                before_id = before["configurable"].get("checkpoint_id")
                if before_id:
                    query = query.lt("checkpoint_id", before_id)

            if limit:
                query = query.limit(limit)

            result = query.execute()

            for row in result.data or []:
                checkpoint = self._deserialize(row["checkpoint"])
                metadata = self._deserialize(row.get("metadata", "{}"))

                parent_config = None
                if row.get("parent_checkpoint_id"):
                    parent_config = {
                        "configurable": {
                            "thread_id": thread_id,
                            "checkpoint_ns": checkpoint_ns,
                            "checkpoint_id": row["parent_checkpoint_id"],
                        }
                    }

                yield CheckpointTuple(
                    config={
                        "configurable": {
                            "thread_id": thread_id,
                            "checkpoint_ns": checkpoint_ns,
                            "checkpoint_id": row["checkpoint_id"],
                        }
                    },
                    checkpoint=checkpoint,
                    metadata=metadata,
                    parent_config=parent_config,
                )
        except Exception as e:
            log.error(f"Failed to list checkpoints: {e}")

    @staticmethod
    def _serialize(obj: Any) -> Any:
        """Serialize to JSON-safe format for Supabase JSONB columns."""
        if obj is None:
            return None
        if isinstance(obj, (dict, list)):
            return json.loads(json.dumps(obj, default=str))
        return json.loads(json.dumps(obj, default=str))

    @staticmethod
    def _deserialize(data: Any) -> Any:
        """Deserialize from Supabase JSONB."""
        if data is None:
            return {}
        if isinstance(data, str):
            try:
                return json.loads(data)
            except (json.JSONDecodeError, TypeError):
                return data
        return data
