"""标准时间字段：Unix 秒级时间戳、默认值与 updated_at 自动维护。"""

from __future__ import annotations

STANDARD_TIMESTAMP_COLUMNS = frozenset({"created_at", "updated_at"})
DATETIME_UNIX_SECONDS = "datetime_unix_seconds"
TASK_LOGS_UPDATED_AT_TRIGGER = "task_logs_set_updated_at"
ANSWER_PUBLISH_RECORDS_UPDATED_AT_TRIGGER = "answer_publish_records_set_updated_at"

_TASK_LOGS_UPDATED_AT_TRIGGER_DDL = f"""
CREATE TRIGGER IF NOT EXISTS {TASK_LOGS_UPDATED_AT_TRIGGER}
AFTER UPDATE ON task_logs
FOR EACH ROW
BEGIN
    UPDATE task_logs
    SET updated_at = unixepoch()
    WHERE id = NEW.id AND updated_at = OLD.updated_at;
END
"""

_ANSWER_PUBLISH_RECORDS_UPDATED_AT_TRIGGER_DDL = f"""
CREATE TRIGGER IF NOT EXISTS {ANSWER_PUBLISH_RECORDS_UPDATED_AT_TRIGGER}
AFTER UPDATE ON answer_publish_records
FOR EACH ROW
BEGIN
    UPDATE answer_publish_records
    SET updated_at = unixepoch()
    WHERE id = NEW.id AND updated_at = OLD.updated_at;
END
"""


def init_task_logs_timestamp_maintenance(cursor) -> None:
    """幂等创建 task_logs.updated_at 自动维护 trigger。"""
    cursor.execute(_TASK_LOGS_UPDATED_AT_TRIGGER_DDL)


def init_answer_publish_records_timestamp_maintenance(cursor) -> None:
    """幂等创建 answer_publish_records.updated_at 自动维护 trigger。"""
    cursor.execute(_ANSWER_PUBLISH_RECORDS_UPDATED_AT_TRIGGER_DDL)


def has_updated_at_trigger(cursor, table_name: str) -> bool:
    trigger_name = f"{table_name}_set_updated_at"
    cursor.execute(
        """
        SELECT 1 FROM sqlite_master
        WHERE type = 'trigger' AND name = ? AND tbl_name = ?
        LIMIT 1
        """,
        (trigger_name, table_name),
    )
    return cursor.fetchone() is not None
