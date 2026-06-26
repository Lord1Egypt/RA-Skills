"""
decay.py - 记忆衰减管理器
基于重要度 × 时间的自动衰减、压缩、归档、物理删除
"""

from __future__ import annotations

import time
import json
import os
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class MemoryDecay:
    """
    记忆衰减策略：

    高优先 (high):    永不自动衰减，人工审查
    中优先 (medium):  90天后衰减为摘要，180天后归档，730天后物理删除
    低优先 (low):     7天衰减，30天压缩为摘要，90天归档，365天物理删除
    """

    # 衰减策略配置
    POLICIES = {
        "high": {
            "review_days": 0,       # 不自动审查
            "decay_days": 0,        # 不衰减
            "archive_days": 0,      # 不自动归档
            "delete_days": 0,       # 不自动删除
        },
        "medium": {
            "review_days": 90,      # 90天后标记待审查
            "decay_days": 180,      # 180天后衰减为摘要
            "archive_days": 365,    # 365天后归档
            "delete_days": 730,     # 730天后物理删除
        },
        "low": {
            "review_days": 7,       # 7天后标记待审查
            "decay_days": 30,       # 30天后衰减为摘要
            "archive_days": 90,     # 90天后归档
            "delete_days": 365,     # 365天后物理删除
        },
    }

    def __init__(self, store, encoder=None, embedding_store=None):
        self.store = store
        self.encoder = encoder
        # Fix (Issue): 接受 embedding_store 引用，用于归档/删除时同步清理向量
        self._embedding_store = embedding_store
        # 归档目录
        self._archive_dir = str(Path(store.db_path).parent / "archive")
        self._archive_file = os.path.join(self._archive_dir, "archived_memories.jsonl")

    def compute_decay_score(self, memory: dict) -> dict:
        """
        计算单条记忆的衰减分数。

        返回: {
            "memory_id": str,
            "importance": str,
            "age_days": int,
            "decay_score": float,      # 0.0 ~ 1.0，1.0=完全新鲜
            "status": str,             # fresh / aging / review / decay / archive / delete
            "next_action": str,
        }
        """
        now = time.time()
        time_ts = memory.get("time_ts", now)
        age_seconds = now - time_ts
        age_days = age_seconds / 86400

        importance = memory.get("importance", "medium")
        policy = self.POLICIES.get(importance, self.POLICIES["medium"])

        # 计算衰减分数
        if policy["decay_days"] == 0:
            decay_score = 1.0
        else:
            decay_score = max(0.0, 1.0 - age_days / policy["decay_days"])

        # 判断状态（按优先级从高到低）
        if policy["delete_days"] and age_days >= policy["delete_days"]:
            status = "delete"
            next_action = "物理删除"
        elif policy["archive_days"] and age_days >= policy["archive_days"]:
            status = "archive"
            next_action = "归档"
        elif policy["decay_days"] and age_days >= policy["decay_days"]:
            status = "decay"
            next_action = "压缩为摘要"
        elif policy["review_days"] and age_days >= policy["review_days"]:
            status = "review"
            next_action = "标记审查"
        else:
            status = "fresh" if age_days < 1 else "aging"
            next_action = "无"

        return {
            "memory_id": memory.get("memory_id", ""),
            "importance": importance,
            "age_days": round(age_days, 1),
            "decay_score": round(decay_score, 4),
            "status": status,
            "next_action": next_action,
        }

    def analyze_all(self, limit: int = 500) -> dict:
        """
        分析所有记忆的衰减状态。

        返回: {
            "total": int,
            "by_status": {"fresh": n, "aging": n, ...},
            "by_importance": {"high": n, "medium": n, "low": n},
            "needs_action": [decay_score dicts],
            "summary": str,
        }
        """
        memories = self.store.query(limit=limit)
        analyses = [self.compute_decay_score(m) for m in memories]

        by_status = {}
        by_importance = {}
        needs_action = []

        for a in analyses:
            by_status[a["status"]] = by_status.get(a["status"], 0) + 1
            by_importance[a["importance"]] = by_importance.get(a["importance"], 0) + 1
            if a["status"] in ("review", "decay", "archive", "delete"):
                needs_action.append(a)

        summary_parts = []
        for status, count in sorted(by_status.items()):
            icon = {"fresh": "🟢", "aging": "🟡", "review": "👀", "decay": "📦",
                    "archive": "🗄️", "delete": "🗑️"}.get(status, "❓")
            summary_parts.append(f"{icon}{status}={count}")

        return {
            "total": len(analyses),
            "by_status": by_status,
            "by_importance": by_importance,
            "needs_action": needs_action,
            "summary": " | ".join(summary_parts),
        }

    def get_decay_weight(self, memory: dict) -> float:
        """获取记忆的衰减权重，用于检索排序。"""
        result = self.compute_decay_score(memory)
        return result["decay_score"]

    def apply_decay_to_recall(self, memories: list[dict]) -> list[dict]:
        """给检索结果附加衰减权重信息。"""
        for mem in memories:
            decay = self.compute_decay_score(mem)
            mem["_decay_score"] = decay["decay_score"]
            mem["_decay_status"] = decay["status"]
            mem["_age_days"] = decay["age_days"]
        return memories

    # ── 真正的遗忘动作 ─────────────────────────────────

    def archive_memories(self, importance: str = None, dry_run: bool = False) -> dict:
        """
        归档到期记忆：导出到 JSONL 文件，然后从 SQLite 删除。

        归档条件：status == "archive"
        high 重要度永不归档。

        返回: {"archived": int, "file": str, "dry_run": bool}
        """
        now = int(time.time())
        memories = self.store.query(importance=importance, limit=1000)

        to_archive = []
        for mem in memories:
            decay = self.compute_decay_score(mem)
            if decay["status"] == "archive":
                to_archive.append(mem)

        if not to_archive:
            return {"archived": 0, "file": self._archive_file, "dry_run": dry_run}

        if dry_run:
            return {"archived": len(to_archive), "file": self._archive_file, "dry_run": True}

        # 写入归档文件
        os.makedirs(self._archive_dir, exist_ok=True)
        archived_ids = []
        with open(self._archive_file, "a", encoding="utf-8") as f:
            for mem in to_archive:
                record = {
                    "memory_id": mem["memory_id"],
                    "content": mem.get("content", ""),
                    "importance": mem.get("importance", ""),
                    "nature_id": mem.get("nature_id", ""),
                    "time_ts": mem.get("time_ts", 0),
                    "person_id": mem.get("person_id", ""),
                    "archived_at": now,
                    "reason": "auto_archive_by_decay",
                }
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
                archived_ids.append(mem["memory_id"])

        # 从 SQLite 物理删除
        for mid in archived_ids:
            try:
                # 先删除关联记录
                self.store.conn.execute(
                    "DELETE FROM memory_topics WHERE memory_id = ?", (mid,)
                )
                self.store.conn.execute(
                    "DELETE FROM memory_tools WHERE memory_id = ?", (mid,)
                )
                self.store.conn.execute(
                    "DELETE FROM memory_knowledge WHERE memory_id = ?", (mid,)
                )
                self.store.conn.execute(
                    "DELETE FROM memory_links WHERE source_id = ? OR target_id = ?", (mid, mid)
                )
                self.store.conn.execute(
                    "DELETE FROM memories WHERE memory_id = ?", (mid,)
                )
            except Exception as e:
                logger.warning("decay: %s", e)

        self.store.conn.commit()

        # 同步清理 FTS
        if hasattr(self.store, '_has_fts') and self.store._has_fts:
            for mid in archived_ids:
                try:
                    self.store.conn.execute(
                        "DELETE FROM memories_fts WHERE memory_id = ?", (mid,)
                    )
                except Exception as e:
                    logger.warning("decay: %s", e)
            self.store.conn.commit()

        # 清理向量库
        if self._embedding_store:
            for mid in archived_ids:
                try:
                    self._embedding_store.delete(mid)
                except Exception as e:
                    logger.warning("decay: %s", e)

        logger.info(f"🗄️ 归档完成: {len(archived_ids)} 条记忆 → {self._archive_file}")
        return {"archived": len(archived_ids), "file": self._archive_file, "dry_run": False}

    def delete_expired(self, importance: str = None, dry_run: bool = False,
                       secure_delete: bool = False) -> dict:
        """
        物理删除到期记忆（status == "delete"）。

        Args:
            importance: 仅删除指定重要度的记忆
            dry_run: True 则只分析不写入
            secure_delete: If True, skip JSONL archiving and perform true
                physical deletion without retaining sensitive data in the
                archive file.  Use this for GDPR-compliant erasure where
                the data subject requests complete removal.
                If False (default, backward compatible), archive to JSONL
                before deletion but log a warning about retained PII.

        Returns: {"deleted": int, "dry_run": bool, "secure_delete": bool}
        """
        memories = self.store.query(importance=importance, limit=1000)

        to_delete = []
        for mem in memories:
            decay = self.compute_decay_score(mem)
            if decay["status"] == "delete":
                to_delete.append(mem)

        if not to_delete:
            return {"deleted": 0, "dry_run": dry_run, "secure_delete": secure_delete}

        if dry_run:
            return {"deleted": len(to_delete), "dry_run": True, "secure_delete": secure_delete}

        # ⚠️ WARNING: Physical deletion is irreversible. Data will be permanently lost.
        logger.warning(
            "SECURITY NOTICE: About to physically delete %d expired memories. "
            "This action is IRREVERSIBLE. Data will be permanently lost. "
            "Use dry_run=True to preview before deletion.",
            len(to_delete),
        )

        deleted_ids = []

        if secure_delete:
            # Secure delete: skip JSONL archiving entirely.
            # Sensitive data is NOT retained anywhere after deletion.
            logger.info(
                "Secure delete mode: %d memories will be physically deleted "
                "WITHOUT JSONL archiving (GDPR-compliant full erasure).",
                len(to_delete),
            )
            deleted_ids = [mem["memory_id"] for mem in to_delete]
        else:
            # Default (backward compatible): archive to JSONL before deletion.
            # WARNING: JSONL archive retains sensitive data (including PII).
            # For GDPR compliance, use secure_delete=True instead.
            logger.warning(
                "Deleting %d memories with JSONL archiving. "
                "Archived data retains sensitive content. "
                "For GDPR-compliant erasure, use secure_delete=True.",
                len(to_delete),
            )
            os.makedirs(self._archive_dir, exist_ok=True)
            with open(self._archive_file, "a", encoding="utf-8") as f:
                for mem in to_delete:
                    record = {
                        "memory_id": mem["memory_id"],
                        "content": mem.get("content", ""),
                        "importance": mem.get("importance", ""),
                        "nature_id": mem.get("nature_id", ""),
                        "time_ts": mem.get("time_ts", 0),
                        "person_id": mem.get("person_id", ""),
                        "deleted_at": int(time.time()),
                        "reason": "auto_delete_by_decay",
                    }
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")
                    deleted_ids.append(mem["memory_id"])

        # 物理删除
        for mid in deleted_ids:
            try:
                self.store.conn.execute("DELETE FROM memory_topics WHERE memory_id = ?", (mid,))
                self.store.conn.execute("DELETE FROM memory_tools WHERE memory_id = ?", (mid,))
                self.store.conn.execute("DELETE FROM memory_knowledge WHERE memory_id = ?", (mid,))
                self.store.conn.execute("DELETE FROM memory_links WHERE source_id = ? OR target_id = ?", (mid, mid))
                self.store.conn.execute("DELETE FROM memories WHERE memory_id = ?", (mid,))
            except Exception as e:
                logger.warning("decay: %s", e)

        self.store.conn.commit()

        # 清理 FTS
        if hasattr(self.store, '_has_fts') and self.store._has_fts:
            for mid in deleted_ids:
                try:
                    self.store.conn.execute("DELETE FROM memories_fts WHERE memory_id = ?", (mid,))
                except Exception as e:
                    logger.warning("decay: %s", e)
            self.store.conn.commit()

        # 清理向量库
        if self._embedding_store:
            for mid in deleted_ids:
                try:
                    self._embedding_store.delete(mid)
                except Exception as e:
                    logger.warning("decay: %s", e)

        mode_label = "secure" if secure_delete else "archived"
        logger.info(
            "Physical delete complete: %d memories (%s mode)",
            len(deleted_ids), mode_label,
        )
        return {"deleted": len(deleted_ids), "dry_run": False, "secure_delete": secure_delete}

    def full_cleanup(self, dry_run: bool = False, secure_delete: bool = False) -> dict:
        """
        执行完整的清理流程：归档 → 删除。

        Args:
            dry_run: True 则只分析不写入
            secure_delete: If True, skip JSONL archiving during deletion.
                For GDPR compliance, use secure_delete=True.

        返回: {"archived": int, "deleted": int}
        """
        archive_result = self.archive_memories(dry_run=dry_run)
        delete_result = self.delete_expired(dry_run=dry_run, secure_delete=secure_delete)

        return {
            "archived": archive_result["archived"],
            "deleted": delete_result["deleted"],
            "dry_run": dry_run,
            "secure_delete": secure_delete,
        }

    def purge_archive(self, archive_path: str | None = None) -> dict:
        """Securely delete the JSONL archive file.

        This removes all archived memory data from disk.  Use this when
        GDPR-compliant full erasure is required and the archive file
        contains sensitive data that must not be retained.

        The deletion is performed by overwriting the file with zeros
        before removing it, to reduce the chance of data recovery.

        Args:
            archive_path: Path to the archive file to purge.
                Defaults to the standard ``archived_memories.jsonl``.

        Returns:
            {"purged": bool, "path": str, "error": str}
            ``purged`` is True only if the file existed and was
            successfully removed.
        """
        target = archive_path or self._archive_file

        if not os.path.exists(target):
            return {"purged": False, "path": target, "error": "file does not exist"}

        try:
            # Overwrite with zeros before deletion to reduce recovery risk
            file_size = os.path.getsize(target)
            with open(target, "wb") as f:
                f.write(b"\x00" * file_size)
                f.flush()
                os.fsync(f.fileno())

            os.unlink(target)
            logger.info("purge_archive: securely deleted %s", target)
            return {"purged": True, "path": target, "error": ""}
        except Exception as e:
            logger.warning("purge_archive: failed to delete %s: %s", target, e)
            return {"purged": False, "path": target, "error": str(e)}

    def generate_report(self, output_path: str = None) -> str:
        """
        生成衰减分析报告 Markdown。
        """
        analysis = self.analyze_all()
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

        lines = [
            "# 📊 记忆衰减分析报告",
            "",
            f"**生成时间**: {now_str}",
            f"**总记忆数**: {analysis['total']}",
            "",
            "## 状态分布",
            "",
        ]

        status_icons = {"fresh": "🟢", "aging": "🟡", "review": "👀", "decay": "📦", "archive": "🗄️"}
        for status in ("fresh", "aging", "review", "decay", "archive"):
            count = analysis["by_status"].get(status, 0)
            if count:
                icon = status_icons.get(status, "❓")
                lines.append(f"- {icon} **{status}**: {count} 条")

        lines.append("")
        lines.append("## 重要度分布")
        lines.append("")
        imp_icons = {"high": "⚡", "medium": "", "low": "🔻"}
        for imp in ("high", "medium", "low"):
            count = analysis["by_importance"].get(imp, 0)
            if count:
                icon = imp_icons.get(imp, "")
                lines.append(f"- {icon} **{imp}**: {count} 条")

        if analysis["needs_action"]:
            lines.append("")
            lines.append("## ⚠️ 需要处理")
            lines.append("")
            lines.append("| 状态 | 重要度 | 天数 | 记忆 ID | 下一步 |")
            lines.append("|------|--------|------|---------|--------|")
            for item in analysis["needs_action"][:20]:
                icon = status_icons.get(item["status"], "")
                lines.append(
                    f"| {icon} {item['status']} | {item['importance']} | {item['age_days']}d | "
                    f"`{item['memory_id'][:20]}...` | {item['next_action']} |"
                )

        lines.append("")
        lines.append(f"**摘要**: {analysis['summary']}")
        lines.append("")
        lines.append("---")
        lines.append("_由 Agent Memory Decay 系统自动生成_")

        report = "\n".join(lines)

        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(report)

        return report
