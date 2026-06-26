"""
migrate.py - 数据库迁移工具

处理 schema 变更：新增表、新增列、索引变更、数据迁移。

用法:
    python3 migrate.py status          # 查看当前版本和待迁移
    python3 migrate.py upgrade         # 升级到最新版本
    python3 migrate.py upgrade --to 3  # 升级到指定版本
    python3 migrate.py rollback        # 回滚到上一版本
    python3 migrate.py create "描述"   # 创建新迁移脚本

迁移脚本存放在 registry/migrations/ 目录，按版本号命名：
    001_initial.sql
    002_add_vector_sync.sql
    003_add_agent_permissions.sql
"""

from __future__ import annotations

import os
import sys
import sqlite3
import json
import hashlib
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

MIGRATIONS_DIR = Path(__file__).parent / "registry" / "migrations"


class MigrationManager:
    """数据库迁移管理器"""

    def __init__(self, db_path: str = None):
        self.db_path = db_path or str(Path(__file__).parent / "memory.db")
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._ensure_migration_table()

    def _ensure_migration_table(self):
        """创建迁移记录表"""
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS _migrations (
                version INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                applied_at INTEGER NOT NULL DEFAULT (strftime('%s','now')),
                checksum TEXT NOT NULL,
                duration_ms INTEGER DEFAULT 0
            );
        """)
        self.conn.commit()

    def get_current_version(self) -> int:
        """获取当前数据库版本"""
        row = self.conn.execute(
            "SELECT MAX(version) as v FROM _migrations"
        ).fetchone()
        return row["v"] if row and row["v"] else 0

    def get_applied_migrations(self) -> list[dict]:
        """获取已应用的迁移列表"""
        rows = self.conn.execute(
            "SELECT * FROM _migrations ORDER BY version"
        ).fetchall()
        return [dict(r) for r in rows]

    def get_pending_migrations(self) -> list[dict]:
        """获取待应用的迁移"""
        current = self.get_current_version()
        available = self._scan_migration_files()
        return [m for m in available if m["version"] > current]

    def _scan_migration_files(self) -> list[dict]:
        """扫描迁移脚本文件"""
        if not MIGRATIONS_DIR.exists():
            MIGRATIONS_DIR.mkdir(parents=True, exist_ok=True)
            return []

        migrations = []
        for f in sorted(MIGRATIONS_DIR.glob("*.sql")):
            name = f.stem  # e.g., "001_initial"
            parts = name.split("_", 1)
            if len(parts) == 2 and parts[0].isdigit():
                version = int(parts[0])
                content = f.read_text(encoding="utf-8")
                checksum = hashlib.md5(content.encode()).hexdigest()[:12]
                migrations.append({
                    "version": version,
                    "name": parts[1],
                    "filename": f.name,
                    "checksum": checksum,
                    "content": content,
                })
        return sorted(migrations, key=lambda m: m["version"])

    def upgrade(self, target_version: int = None) -> dict:
        """
        升级数据库到指定版本（默认最新）。

        返回: {"from": int, "to": int, "applied": int, "errors": list}
        """
        current = self.get_current_version()
        available = self._scan_migration_files()
        pending = [m for m in available if m["version"] > current]

        if target_version:
            pending = [m for m in pending if m["version"] <= target_version]

        if not pending:
            return {"from": current, "to": current, "applied": 0, "errors": []}

        applied = 0
        errors = []

        for migration in pending:
            try:
                import time
                start = time.time()

                # 执行迁移 SQL
                self.conn.executescript(migration["content"])

                # 记录
                duration_ms = int((time.time() - start) * 1000)
                self.conn.execute(
                    "INSERT INTO _migrations (version, name, checksum, duration_ms) VALUES (?, ?, ?, ?)",
                    (migration["version"], migration["name"], migration["checksum"], duration_ms),
                )
                self.conn.commit()

                applied += 1
                logger.info(f"✅ 迁移 {migration['version']:03d}_{migration['name']} ({duration_ms}ms)")

            except Exception as e:
                error_msg = f"迁移 {migration['version']} 失败: {e}"
                logger.error(error_msg)
                errors.append(error_msg)
                self.conn.rollback()
                break  # 停止后续迁移

        new_version = self.get_current_version()
        return {"from": current, "to": new_version, "applied": applied, "errors": errors}

    def status(self) -> dict:
        """获取迁移状态"""
        current = self.get_current_version()
        applied = self.get_applied_migrations()
        pending = self.get_pending_migrations()

        return {
            "current_version": current,
            "applied_count": len(applied),
            "pending_count": len(pending),
            "applied": applied,
            "pending": [{"version": m["version"], "name": m["name"]} for m in pending],
        }

    def create(self, description: str) -> str:
        """创建新的迁移脚本模板"""
        current = self.get_current_version()
        next_version = current + 1

        slug = description.lower().replace(" ", "_")[:40]
        filename = f"{next_version:03d}_{slug}.sql"
        filepath = MIGRATIONS_DIR / filename

        MIGRATIONS_DIR.mkdir(parents=True, exist_ok=True)

        template = f"""-- Migration {next_version:03d}: {description}
-- Created: {datetime.now().strftime('%Y-%m-%d %H:%M')}

-- 在此写入迁移 SQL
-- 示例：
-- ALTER TABLE memories ADD COLUMN new_field TEXT DEFAULT '';
-- CREATE INDEX IF NOT EXISTS idx_memories_new ON memories(new_field);

-- 回滚 SQL（放在注释中，手动执行）：
-- ALTER TABLE memories DROP COLUMN new_field;
"""

        filepath.write_text(template, encoding="utf-8")
        logger.info(f"创建迁移脚本: {filepath}")
        return str(filepath)

    def close(self):
        self.conn.close()


def main():
    import argparse
    from logging_config import configure_logging
    configure_logging(level="INFO", fmt="%(message)s")

    parser = argparse.ArgumentParser(description="数据库迁移工具")
    parser.add_argument("command", choices=["status", "upgrade", "rollback", "create"],
                        help="迁移命令")
    parser.add_argument("--to", type=int, help="目标版本 (upgrade)")
    parser.add_argument("--db", type=str, help="数据库路径")
    parser.add_argument("description", nargs="?", help="迁移描述 (create)")

    args = parser.parse_args()
    mgr = MigrationManager(db_path=args.db)

    try:
        if args.command == "status":
            s = mgr.status()
            logger.info(f"当前版本: {s['current_version']}")
            logger.info(f"已应用: {s['applied_count']} 个迁移")
            if s["pending"]:
                logger.info(f"待应用: {s['pending_count']} 个迁移")
                for m in s["pending"]:
                    logger.info(f"  - {m['version']:03d}_{m['name']}")
            else:
                logger.info("无待应用迁移")

        elif args.command == "upgrade":
            result = mgr.upgrade(target_version=args.to)
            logger.info(f"升级完成: v{result['from']} → v{result['to']} ({result['applied']} 个迁移)")
            if result["errors"]:
                logger.error("错误:")
                for e in result["errors"]:
                    logger.error(f"  ❌ {e}")

        elif args.command == "create":
            if not args.description:
                logger.error("错误: 请提供迁移描述")
                sys.exit(1)
            path = mgr.create(args.description)
            logger.info(f"已创建: {path}")

    finally:
        mgr.close()


if __name__ == "__main__":
    main()
