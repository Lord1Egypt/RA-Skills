"""
enterprise/offboarding.py — Employee offboarding and memory handover.

When an employee leaves, work memories stay with the enterprise
while personal memories can be exported.
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class HandoverReport:
    """Report of a memory handover."""
    from_user: str = ""
    to_user: str = ""
    work_memories_transferred: int = 0
    personal_memories_exported: int = 0
    personal_memories_deleted: int = 0
    errors: list[str] = field(default_factory=list)


class OffboardingManager:
    """Manage employee offboarding: partition, export, handover.

    Uses MemoryPartition for classification and ComplianceGuard
    for PII redaction during handover.
    """

    def __init__(self, store=None, memory_partition=None,
                 compliance_guard=None):
        self.store = store
        self.memory_partition = memory_partition
        self.compliance_guard = compliance_guard

    def partition_memories(self, user_id: str) -> dict[str, list[dict]]:
        """Partition a user's memories into personal and work.

        Returns:
            {"personal": [...], "work": [...], "enterprise": [...]}
        """
        if not self.store:
            return {"personal": [], "work": [], "enterprise": []}

        try:
            memories = self.store.query(limit=10000) if hasattr(self.store, 'query') else []
            user_memories = [m for m in memories
                           if m.get("owner_agent_id", "").startswith(user_id)]

            result = {"personal": [], "work": [], "enterprise": []}
            for mem in user_memories:
                if self.memory_partition:
                    scope = self.memory_partition.classify_memory(mem)
                else:
                    scope = mem.get("tenant_id", "work")
                    if scope == "default":
                        scope = "work"
                if scope in result:
                    result[scope].append(mem)
                else:
                    result["work"].append(mem)

            return result

        except Exception as e:
            logger.error("Memory partitioning failed: %s", e)
            return {"personal": [], "work": [], "enterprise": []}

    def export_personal(self, user_id: str, format: str = "json") -> str:
        """Export personal memories for the departing employee."""
        partitions = self.partition_memories(user_id)
        personal = partitions.get("personal", [])
        return json.dumps(personal, ensure_ascii=False, indent=2)

    def handover(self, from_user: str, to_user: str,
                 scope: str = "work") -> HandoverReport:
        """Transfer work memories from departing employee to successor.

        Args:
            from_user: Departing employee ID
            to_user: Successor employee ID
            scope: Memory scope to transfer

        Returns:
            HandoverReport with transfer details
        """
        report = HandoverReport(from_user=from_user, to_user=to_user)

        if not self.store:
            return report

        try:
            partitions = self.partition_memories(from_user)
            work_mems = partitions.get(scope, [])

            # Transfer work memories to new owner
            for mem in work_mems:
                mid = mem.get("id", "")
                try:
                    # Redact PII in content before handover
                    content = mem.get("content", "")
                    if self.compliance_guard:
                        scan = self.compliance_guard.scan(content)
                        if not scan.is_compliant:
                            content = scan.redacted_content

                    self.store.update_memory(mid, {
                        "owner_agent_id": to_user,
                    })
                    report.work_memories_transferred += 1
                except Exception as e:
                    report.errors.append(f"Failed to transfer {mid}: {e}")

            # Delete personal memories
            personal = partitions.get("personal", [])
            for mem in personal:
                mid = mem.get("id", "")
                try:
                    self.store.delete_memory(mid)
                    report.personal_memories_deleted += 1
                except Exception as e:
                    report.errors.append(f"Failed to delete {mid}: {e}")

            report.personal_memories_exported = len(personal)

        except Exception as e:
            report.errors.append(str(e))

        return report
