"""
GDPR 合规管理器 v0.5.0
========================
提供数据最小化、用户同意、数据导出/删除、保留期限、审计日志等能力。

核心功能：
  - 数据导出：export_all_data() → 导出全部个人数据（JSON）
  - 数据删除：purge_all_data() → 删除本地+请求服务端删除
  - 保留期限：clean_expired_data() → 自动清理过期数据
  - 审计日志：log_operation() → 记录数据操作轨迹

Usage:
    gdpr = GDPRManager(store, identity_mgr)
    gdpr.export_all_data("export.json")
    gdpr.purge_all_data(notify_server=True)
"""

import json
import logging
import os
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

DEFAULT_RETENTION_DAYS = 180  # 服务端数据默认保留 180 天
AUDIT_LOG_TABLE = "audit_log"


class GDPRManager:
    """GDPR 合规管理器"""

    def __init__(self, store=None, identity_mgr=None):
        """
        Args:
            store: DataStore 实例（本地 SQLite）
            identity_mgr: IdentityManager 实例
        """
        self.store = store
        self.identity = identity_mgr
        self._ensure_audit_table()

    def _ensure_audit_table(self):
        """确保审计日志表存在"""
        if not self.store:
            return
        try:
            conn = self.store._conn
            conn.execute(f"""
                CREATE TABLE IF NOT EXISTS {AUDIT_LOG_TABLE} (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_id    TEXT,
                    operation   TEXT NOT NULL,
                    target      TEXT,
                    details     TEXT,
                    operator    TEXT DEFAULT 'user',
                    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
                )
            """)
            conn.execute(f"""
                CREATE INDEX IF NOT EXISTS idx_audit_time
                ON {AUDIT_LOG_TABLE}(created_at)
            """)
            conn.commit()
        except Exception as e:
            logger.warning(f"审计表创建失败: {e}")

    # ──────── 审计日志 ────────

    def log_operation(self, operation: str, target: str = "", details: str = "", operator: str = "user"):
        """记录数据操作到审计日志"""
        if not self.store:
            return
        try:
            agent_id = self.identity.agent_id if self.identity else ""
            self.store._conn.execute(
                f"INSERT INTO {AUDIT_LOG_TABLE} (agent_id, operation, target, details, operator) VALUES (?,?,?,?,?)",
                (agent_id, operation, target, details, operator),
            )
            self.store._conn.commit()
        except Exception as e:
            logger.warning(f"审计日志写入失败: {e}")

    def get_audit_log(self, limit: int = 100) -> List[Dict]:
        """查询审计日志"""
        if not self.store:
            return []
        rows = self.store._conn.execute(
            f"SELECT * FROM {AUDIT_LOG_TABLE} ORDER BY created_at DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]

    # ──────── 数据导出 ────────

    def export_all_data(self, output_path: str = None) -> Dict[str, Any]:
        """
        导出该 Agent 的全部个人数据（GDPR 数据可携权）
        
        Returns:
            包含所有个人数据的字典
        """
        self.log_operation("data_export", "all", "用户请求导出全部数据")

        agent_id = self.identity.agent_id if self.identity else ""
        export_data = {
            "export_version": "1.0",
            "exported_at": datetime.now().isoformat(),
            "agent_id": agent_id,
            "sections": {},
        }

        if self.store:
            conn = self.store._conn

            # 运行记录
            runs = conn.execute(
                "SELECT * FROM skill_runs WHERE agent_id = ? ORDER BY start_time DESC",
                (agent_id,),
            ).fetchall()
            export_data["sections"]["skill_runs"] = [dict(r) for r in runs]

            # 聚合指标
            metrics = conn.execute(
                "SELECT * FROM skill_metrics WHERE agent_id = ? ORDER BY date DESC",
                (agent_id,),
            ).fetchall()
            export_data["sections"]["skill_metrics"] = [dict(r) for r in metrics]

            # 隐性反馈
            feedback = conn.execute(
                "SELECT * FROM implicit_feedback WHERE agent_id = ? ORDER BY created_at DESC",
                (agent_id,),
            ).fetchall()
            export_data["sections"]["implicit_feedback"] = [dict(r) for r in feedback]

            # 旧版反馈
            old_feedback = conn.execute(
                "SELECT * FROM user_feedback WHERE agent_id = ? ORDER BY created_at DESC",
                (agent_id,),
            ).fetchall()
            export_data["sections"]["user_feedback"] = [dict(r) for r in old_feedback]

            # 审计日志
            audit = conn.execute(
                f"SELECT * FROM {AUDIT_LOG_TABLE} WHERE agent_id = ? ORDER BY created_at DESC",
                (agent_id,),
            ).fetchall()
            export_data["sections"]["audit_log"] = [dict(r) for r in audit]

        # 身份配置（脱敏）
        if self.identity:
            export_data["sections"]["config"] = self.identity.get_config()

        # 统计
        export_data["summary"] = {
            table: len(records)
            for table, records in export_data["sections"].items()
        }

        if output_path:
            os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2, default=str)
            logger.info(f"数据已导出到: {output_path}")

        return export_data

    # ──────── 数据删除 ────────

    def purge_all_data(self, notify_server: bool = True, server_url: str = None) -> Dict[str, Any]:
        """
        删除该 Agent 的全部本地数据（GDPR 被遗忘权）
        
        Args:
            notify_server: 是否请求服务端也删除数据
            server_url: 服务端 URL
        """
        self.log_operation("data_purge", "all", "用户请求删除全部数据")
        result = {"local": {}, "server": None}

        agent_id = self.identity.agent_id if self.identity else ""

        if self.store:
            conn = self.store._conn
            tables_to_clean = ["skill_runs", "skill_metrics", "implicit_feedback", "user_feedback"]

            for table in tables_to_clean:
                try:
                    cursor = conn.execute(
                        f"DELETE FROM {table} WHERE agent_id = ?", (agent_id,)
                    )
                    result["local"][table] = cursor.rowcount
                except Exception as e:
                    result["local"][table] = f"error: {e}"

            conn.commit()
            logger.info(f"本地数据已清除: {result['local']}")

        # 请求服务端删除
        if notify_server and server_url:
            result["server"] = self._request_server_delete(server_url, agent_id)

        # 清除安全存储
        if self.identity and self.identity._secure_store:
            try:
                self.identity._secure_store.delete_credential("api_key")
                self.identity._secure_store.delete_credential("agent_id")
                result["local"]["secure_store"] = "cleared"
            except Exception:
                pass

        return result

    def _request_server_delete(self, server_url: str, agent_id: str) -> Dict:
        """请求服务端删除该 Agent 的全部数据"""
        try:
            import requests
            api_key = self.identity.api_key if self.identity else ""
            resp = requests.post(
                f"{server_url}/api/agent/delete-data",
                headers={
                    "X-Agent-ID": agent_id,
                    "X-Agent-Token": api_key or "",
                },
                json={"agent_id": agent_id, "reason": "gdpr_purge"},
                timeout=15,
            )
            return resp.json()
        except Exception as e:
            return {"error": str(e)}

    # ──────── 数据保留期限 ────────

    def clean_expired_data(self, retention_days: int = DEFAULT_RETENTION_DAYS) -> Dict[str, int]:
        """清理超过保留期限的数据"""
        if not self.store:
            return {}

        cutoff = (datetime.now() - timedelta(days=retention_days)).isoformat()
        self.log_operation("data_cleanup", "expired", f"清理 {retention_days} 天前的数据")

        conn = self.store._conn
        result = {}

        for table, time_col in [
            ("skill_runs", "start_time"),
            ("skill_metrics", "date"),
            ("implicit_feedback", "created_at"),
            ("user_feedback", "created_at"),
        ]:
            try:
                cursor = conn.execute(f"DELETE FROM {table} WHERE {time_col} < ?", (cutoff,))
                result[table] = cursor.rowcount
            except Exception as e:
                result[table] = 0
                logger.warning(f"清理 {table} 失败: {e}")

        conn.commit()
        return result

    # ──────── 用户同意管理 ────────

    def show_consent_prompt(self) -> str:
        """生成数据收集声明文本"""
        return """
╔══════════════════════════════════════════════════════╗
║           Skills Monitor 数据收集声明                  ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║  为提供 Skills 诊断和评估服务，我们会收集以下数据：     ║
║                                                      ║
║  📊 运行数据：Skill 调用次数、成功率、响应时间         ║
║  📈 评分数据：5 因子评分指标、趋势分析                ║
║  🔒 健康度：诊断报告的聚合健康度评分                  ║
║                                                      ║
║  我们 不会 收集：                                     ║
║  ❌ Skill 的输入/输出内容                             ║
║  ❌ 您的文件路径、个人信息                            ║
║  ❌ 大模型的对话内容                                  ║
║                                                      ║
║  您的权利：                                           ║
║  📤 随时导出全部数据：skills-monitor export            ║
║  🗑️  随时删除全部数据：skills-monitor purge            ║
║  ⏸️  随时停止数据收集：skills-monitor config --no-collect║
║                                                      ║
╚══════════════════════════════════════════════════════╝
"""
