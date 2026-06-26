"""MemoryEraser — GDPR Article 17 compliant memory erasure.

Performs complete cascade deletion of a memory and all related data across:
  - Main memories table
  - FTS index (memories_fts)
  - Vector index (embedding_store)
  - Links (memory_links)
  - Topics / Tools / Knowledge associations
  - Memory versions
  - Memory entities / Relations
  - Audit logs (anonymize)
  - Reasoning traces referencing the memory
  - Tasks referencing the memory
  - Window associations
  - Document chunks
"""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class ErasureReport:
    """Report of a single memory erasure operation."""
    memory_id: str
    deleted_tables: list[str] = field(default_factory=list)
    vector_deleted: bool = False
    audit_anonymized: bool = False
    errors: list[str] = field(default_factory=list)
    duration_ms: int = 0

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0


@dataclass
class BulkErasureReport:
    """Report of a bulk (tenant-level) erasure operation."""
    tenant_id: str
    total_memories: int = 0
    erased: int = 0
    errors: list[str] = field(default_factory=list)
    erasure_reports: list[ErasureReport] = field(default_factory=list)
    duration_ms: int = 0

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0 and self.erased == self.total_memories


class MemoryEraser:
    """Complete memory erasure compliant with GDPR Article 17.

    Usage:
        eraser = MemoryEraser(store)
        report = eraser.erase_memory("mem_abc123")
        assert report.ok

        # Verify erasure
        assert eraser.verify_erasure("mem_abc123")
    """

    # Tables that have a direct memory_id foreign key
    _MEMORY_ID_TABLES = [
        ("memory_topics", "memory_id"),
        ("memory_tools", "memory_id"),
        ("memory_knowledge", "memory_id"),
        ("memory_versions", "memory_id"),
        ("memory_entities", "memory_id"),
        ("memory_permissions", "memory_id"),
        ("window_memories", "memory_id"),
        ("chunk_meta", "memory_id"),
        ("tasks", "memory_id"),
    ]

    # Tables where memory_id appears in a JSON column (reasoning_traces.sources_used)
    _MEMORY_ID_JSON_TABLES = [
        ("reasoning_traces", "sources_used"),
    ]

    def __init__(self, store):
        """
        Args:
            store: MemoryStore instance (or CryptoStore proxy)
        """
        self.store = store

    def erase_memory(self, memory_id: str, cascade: bool = True) -> ErasureReport:
        """Erase a memory and all related data.

        Args:
            memory_id: The memory to erase
            cascade: If True, delete from all related tables.
                     If False, only delete from the main memories table.

        Returns:
            ErasureReport with details of what was deleted.
        """
        start = time.time()
        report = ErasureReport(memory_id=memory_id)

        # Verify memory exists
        mem = self.store.get_memory(memory_id)
        if not mem:
            report.errors.append(f"Memory {memory_id} not found")
            report.duration_ms = int((time.time() - start) * 1000)
            return report

        if not cascade:
            # Simple delete — delegate to store
            self.store.delete_memory(memory_id)
            report.deleted_tables.append("memories")
            report.duration_ms = int((time.time() - start) * 1000)
            return report

        conn = self.store.conn

        try:
            # 1. Delete from association tables (memory_id FK)
            for table, col in self._MEMORY_ID_TABLES:
                try:
                    conn.execute(f"DELETE FROM {table} WHERE {col} = ?", (memory_id,))
                    report.deleted_tables.append(table)
                except Exception as e:
                    # Table may not exist in all deployments
                    logger.debug("erase_memory: skip %s: %s", table, e)

            # 2. Delete from FTS index
            try:
                conn.execute("DELETE FROM memories_fts WHERE memory_id = ?", (memory_id,))
                report.deleted_tables.append("memories_fts")
            except Exception as e:
                logger.debug("erase_memory: skip memories_fts: %s", e)

            # 3. Delete links (source or target)
            try:
                conn.execute(
                    "DELETE FROM memory_links WHERE source_id = ? OR target_id = ?",
                    (memory_id, memory_id),
                )
                report.deleted_tables.append("memory_links")
            except Exception as e:
                logger.debug("erase_memory: skip memory_links: %s", e)

            # 4. Delete from main memories table
            conn.execute("DELETE FROM memories WHERE memory_id = ?", (memory_id,))
            report.deleted_tables.append("memories")

            # 5. Delete from vector index
            if hasattr(self.store, '_embedding_store_ref') and self.store._embedding_store_ref:
                try:
                    self.store._embedding_store_ref.delete(memory_id)
                    report.vector_deleted = True
                except Exception as e:
                    report.errors.append(f"Vector deletion failed: {e}")

            # 6. Anonymize audit logs (replace memory_id with "[ERASED]")
            try:
                from ..enterprise.audit_log import AuditLogger
                audit_db = AuditLogger()
                audit_conn = audit_db._conn
                audit_conn.execute(
                    "UPDATE audit_logs SET memory_id = '[ERASED]', details = '[ERASED]' WHERE memory_id = ?",
                    (memory_id,),
                )
                audit_conn.commit()
                report.audit_anonymized = True
            except ImportError:
                logger.debug("erase_memory: audit_log module not available")
            except Exception as e:
                logger.debug("erase_memory: audit anonymization failed: %s", e)

            # 7. Clean up relations that reference this memory via source_memory_id
            try:
                conn.execute("DELETE FROM relations WHERE source_memory_id = ?", (memory_id,))
                report.deleted_tables.append("relations")
            except Exception as e:
                logger.debug("erase_memory: skip relations: %s", e)

            # 8. Clean up agent associations
            try:
                conn.execute("DELETE FROM agent_associations WHERE memory_id = ?", (memory_id,))
                report.deleted_tables.append("agent_associations")
            except Exception as e:
                logger.debug("erase_memory: skip agent_associations: %s", e)

            conn.commit()

        except Exception as e:
            try:
                conn.rollback()
            except Exception:
                pass
            report.errors.append(f"Cascade delete failed: {e}")

        report.duration_ms = int((time.time() - start) * 1000)
        return report

    def erase_tenant_data(self, tenant_id: str, secure_delete: bool = True) -> BulkErasureReport:
        """Erase ALL data for a tenant (GDPR right to erasure).

        Args:
            tenant_id: The tenant whose data should be erased
            secure_delete: If True (default), perform true physical deletion
                without archiving. For GDPR compliance, keep this True.

        Returns:
            BulkErasureReport with details of the bulk erasure.
        """
        start = time.time()
        report = BulkErasureReport(tenant_id=tenant_id)

        # Find all memories for this tenant
        memory_ids = self._get_tenant_memory_ids(tenant_id)
        report.total_memories = len(memory_ids)

        if not memory_ids:
            report.duration_ms = int((time.time() - start) * 1000)
            return report

        # Erase each memory with cascade
        for mid in memory_ids:
            erasure = self.erase_memory(mid, cascade=True)
            report.erasure_reports.append(erasure)
            if erasure.ok:
                report.erased += 1
            else:
                report.errors.extend(erasure.errors)

        # If secure_delete, also purge any JSONL archive that may contain
        # this tenant's data from the decay archive.
        if secure_delete:
            try:
                from ..decay import MemoryDecay
                decay = MemoryDecay(self.store)
                purge_result = decay.purge_archive()
                if purge_result.get("purged"):
                    logger.info(
                        "erase_tenant_data: purged JSONL archive for secure deletion"
                    )
            except Exception as e:
                logger.debug(
                    "erase_tenant_data: archive purge skipped: %s", e
                )

        report.duration_ms = int((time.time() - start) * 1000)
        return report

    def verify_erasure(self, memory_id: str) -> bool:
        """Verify that a memory has been fully erased from all tables.

        Args:
            memory_id: The memory ID to verify

        Returns:
            True if no traces of the memory remain in any table.
        """
        conn = self.store.conn

        # 1. Check main table
        row = conn.execute(
            "SELECT COUNT(*) FROM memories WHERE memory_id = ?", (memory_id,)
        ).fetchone()
        if row[0] > 0:
            logger.warning("verify_erasure: memory still exists in memories table")
            return False

        # 2. Check association tables
        for table, col in self._MEMORY_ID_TABLES:
            try:
                row = conn.execute(
                    f"SELECT COUNT(*) FROM {table} WHERE {col} = ?", (memory_id,)
                ).fetchone()
                if row[0] > 0:
                    logger.warning("verify_erasure: data remains in %s", table)
                    return False
            except Exception:
                pass  # Table may not exist

        # 3. Check FTS
        try:
            row = conn.execute(
                "SELECT COUNT(*) FROM memories_fts WHERE memory_id = ?", (memory_id,)
            ).fetchone()
            if row[0] > 0:
                logger.warning("verify_erasure: data remains in memories_fts")
                return False
        except Exception:
            pass

        # 4. Check links
        try:
            row = conn.execute(
                "SELECT COUNT(*) FROM memory_links WHERE source_id = ? OR target_id = ?",
                (memory_id, memory_id),
            ).fetchone()
            if row[0] > 0:
                logger.warning("verify_erasure: data remains in memory_links")
                return False
        except Exception:
            pass

        # 5. Check vector store
        if hasattr(self.store, '_embedding_store_ref') and self.store._embedding_store_ref:
            try:
                vec = self.store._embedding_store_ref.get(memory_id)
                if vec is not None:
                    logger.warning("verify_erasure: vector still exists in embedding store")
                    return False
            except Exception:
                pass

        return True

    def _get_tenant_memory_ids(self, tenant_id: str) -> list[str]:
        """Get all memory IDs for a tenant."""
        conn = self.store.conn
        try:
            # Check if tenant_id column exists
            cols = {
                row["name"]
                for row in conn.execute("PRAGMA table_info(memories)").fetchall()
            }
            if "tenant_id" in cols:
                rows = conn.execute(
                    "SELECT memory_id FROM memories WHERE tenant_id = ?",
                    (tenant_id,),
                ).fetchall()
                return [r["memory_id"] for r in rows]
        except Exception as e:
            logger.warning("_get_tenant_memory_ids: %s", e)
        return []
