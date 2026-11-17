"""匠厂数据管理展示元数据（_jiangchang_tables / _jiangchang_columns）。

SQLite 无原生表/字段 COMMENT；中文展示名称通过这两张元数据表提供给宿主「数据管理」页面。
字段在界面上的顺序由 CREATE TABLE / PRAGMA table_info(cid) 决定，**不**使用 display_order 排序。
"""

from __future__ import annotations

from typing import Iterable

# 宿主会隐藏这些表，不作为业务表展示（见 jiangchang electron/data-management/types.ts）
INTERNAL_METADATA_TABLES = frozenset({"_jiangchang_tables", "_jiangchang_columns"})
LEGACY_METADATA_TABLES = frozenset({"_schema_meta"})
METADATA_TABLES = INTERNAL_METADATA_TABLES | LEGACY_METADATA_TABLES

TASK_LOGS_TABLE = "task_logs"
ANSWER_PUBLISH_RECORDS_TABLE = "answer_publish_records"
DATETIME_UNIX_SECONDS = "datetime_unix_seconds"
STANDARD_TIMESTAMP_COLUMNS = frozenset({"created_at", "updated_at"})

_JIANGCHANG_TABLES_DDL = """
CREATE TABLE IF NOT EXISTS _jiangchang_tables (
    table_name TEXT PRIMARY KEY,
    display_name TEXT NOT NULL,
    description TEXT,
    sort_order INTEGER,
    visible INTEGER NOT NULL DEFAULT 1,
    readonly INTEGER NOT NULL DEFAULT 0
)
"""

_JIANGCHANG_COLUMNS_DDL = """
CREATE TABLE IF NOT EXISTS _jiangchang_columns (
    table_name TEXT NOT NULL,
    column_name TEXT NOT NULL,
    display_name TEXT NOT NULL,
    description TEXT,
    display_order INTEGER,
    visible INTEGER NOT NULL DEFAULT 1,
    searchable INTEGER NOT NULL DEFAULT 1,
    editable INTEGER NOT NULL DEFAULT 1,
    display_type TEXT,
    options_json TEXT,
    PRIMARY KEY (table_name, column_name)
)
"""

TASK_LOGS_TABLE_METADATA = {
    "table_name": TASK_LOGS_TABLE,
    "display_name": "任务日志",
    "description": "记录技能任务的执行状态和结果",
    "visible": 1,
    "readonly": 0,
}

TASK_LOGS_COLUMN_METADATA: tuple[dict[str, object], ...] = (
    {"column_name": "id", "display_name": "编号", "description": "任务日志唯一编号", "visible": 1, "searchable": 1, "editable": 0},
    {"column_name": "task_type", "display_name": "任务类型", "description": "任务的业务类型", "visible": 1, "searchable": 1, "editable": 1},
    {"column_name": "target_id", "display_name": "目标编号", "description": "任务目标对象编号", "visible": 1, "searchable": 1, "editable": 1},
    {"column_name": "input_id", "display_name": "输入编号", "description": "输入对象编号", "visible": 1, "searchable": 1, "editable": 1},
    {"column_name": "input_title", "display_name": "输入标题", "description": "输入对象标题", "visible": 1, "searchable": 1, "editable": 1},
    {"column_name": "status", "display_name": "状态", "description": "任务当前状态", "visible": 1, "searchable": 1, "editable": 1},
    {"column_name": "error_msg", "display_name": "错误信息", "description": "任务失败时的错误说明", "visible": 1, "searchable": 1, "editable": 1},
    {"column_name": "result_summary", "display_name": "结果摘要", "description": "任务执行结果摘要", "visible": 1, "searchable": 1, "editable": 1},
    {
        "column_name": "created_at",
        "display_name": "创建时间",
        "description": "记录创建时间（Unix 秒级时间戳，数据库自动生成）",
        "visible": 1,
        "searchable": 0,
        "editable": 0,
        "display_type": DATETIME_UNIX_SECONDS,
    },
    {
        "column_name": "updated_at",
        "display_name": "更新时间",
        "description": "记录最后更新时间（Unix 秒级时间戳，自动维护）",
        "visible": 1,
        "searchable": 0,
        "editable": 0,
        "display_type": DATETIME_UNIX_SECONDS,
    },
)

ANSWER_PUBLISH_RECORDS_TABLE_METADATA = {
    "table_name": ANSWER_PUBLISH_RECORDS_TABLE,
    "display_name": "回答发布记录",
    "description": "记录每次在百度知道发布回答的账号、问题、文稿与最终状态",
    "visible": 1,
    "readonly": 0,
}

ANSWER_PUBLISH_RECORDS_COLUMN_METADATA: tuple[dict[str, object], ...] = (
    {"column_name": "id", "display_name": "编号", "description": "发布记录唯一编号", "visible": 1, "searchable": 1, "editable": 0},
    {"column_name": "idempotency_key", "display_name": "幂等键", "description": "调用方传入的幂等键，同一键不会重复发布", "visible": 1, "searchable": 1, "editable": 0},
    {"column_name": "account_id", "display_name": "账号编号", "description": "使用的百度知道账号编号", "visible": 1, "searchable": 1, "editable": 0},
    {"column_name": "question_url", "display_name": "问题链接", "description": "百度知道问题页 URL", "visible": 1, "searchable": 1, "editable": 0},
    {"column_name": "answer_path", "display_name": "回答文稿路径", "description": "本地回答文稿文件路径", "visible": 1, "searchable": 1, "editable": 0},
    {"column_name": "status", "display_name": "发布状态", "description": "success / pending_review / failed", "visible": 1, "searchable": 1, "editable": 0},
    {"column_name": "platform_message", "display_name": "平台反馈", "description": "百度知道返回的提示信息", "visible": 1, "searchable": 1, "editable": 0},
    {"column_name": "published_at", "display_name": "提交时间", "description": "回答提交到百度知道的时间（Unix 秒级时间戳）", "visible": 1, "searchable": 0, "editable": 0, "display_type": DATETIME_UNIX_SECONDS},
    {
        "column_name": "created_at",
        "display_name": "创建时间",
        "description": "记录创建时间（Unix 秒级时间戳，数据库自动生成）",
        "visible": 1,
        "searchable": 0,
        "editable": 0,
        "display_type": DATETIME_UNIX_SECONDS,
    },
    {
        "column_name": "updated_at",
        "display_name": "更新时间",
        "description": "记录最后更新时间（Unix 秒级时间戳，自动维护）",
        "visible": 1,
        "searchable": 0,
        "editable": 0,
        "display_type": DATETIME_UNIX_SECONDS,
    },
)


def init_display_metadata_tables(cursor) -> None:
    cursor.execute(_JIANGCHANG_TABLES_DDL)
    cursor.execute(_JIANGCHANG_COLUMNS_DDL)


def upsert_table_metadata(cursor, *, table_name: str, display_name: str, description: str | None = None, visible: int = 1, readonly: int = 0) -> None:
    cursor.execute(
        """
        INSERT INTO _jiangchang_tables (table_name, display_name, description, visible, readonly)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(table_name) DO UPDATE SET
            display_name = excluded.display_name,
            description = excluded.description,
            visible = excluded.visible,
            readonly = excluded.readonly
        """,
        (table_name, display_name, description, visible, readonly),
    )


def upsert_column_metadata(
    cursor,
    *,
    table_name: str,
    column_name: str,
    display_name: str,
    description: str | None = None,
    visible: int = 1,
    searchable: int = 1,
    editable: int = 1,
    display_type: str | None = None,
) -> None:
    # display_order 保留为 NULL：宿主按 PRAGMA table_info cid 展示字段，不读 display_order。
    cursor.execute(
        """
        INSERT INTO _jiangchang_columns (
            table_name, column_name, display_name, description,
            display_order, visible, searchable, editable, display_type
        )
        VALUES (?, ?, ?, ?, NULL, ?, ?, ?, ?)
        ON CONFLICT(table_name, column_name) DO UPDATE SET
            display_name = excluded.display_name,
            description = excluded.description,
            display_order = NULL,
            visible = excluded.visible,
            searchable = excluded.searchable,
            editable = excluded.editable,
            display_type = excluded.display_type
        """,
        (table_name, column_name, display_name, description, visible, searchable, editable, display_type),
    )


def seed_task_logs_display_metadata(cursor) -> None:
    meta = TASK_LOGS_TABLE_METADATA
    upsert_table_metadata(
        cursor,
        table_name=str(meta["table_name"]),
        display_name=str(meta["display_name"]),
        description=str(meta["description"]) if meta.get("description") else None,
        visible=int(meta["visible"]),
        readonly=int(meta["readonly"]),
    )
    for column in TASK_LOGS_COLUMN_METADATA:
        upsert_column_metadata(
            cursor,
            table_name=TASK_LOGS_TABLE,
            column_name=str(column["column_name"]),
            display_name=str(column["display_name"]),
            description=str(column["description"]) if column.get("description") else None,
            visible=int(column["visible"]),
            searchable=int(column["searchable"]),
            editable=int(column["editable"]),
            display_type=str(column["display_type"]) if column.get("display_type") else None,
        )


def seed_answer_publish_records_display_metadata(cursor) -> None:
    meta = ANSWER_PUBLISH_RECORDS_TABLE_METADATA
    upsert_table_metadata(
        cursor,
        table_name=str(meta["table_name"]),
        display_name=str(meta["display_name"]),
        description=str(meta["description"]) if meta.get("description") else None,
        visible=int(meta["visible"]),
        readonly=int(meta["readonly"]),
    )
    for column in ANSWER_PUBLISH_RECORDS_COLUMN_METADATA:
        upsert_column_metadata(
            cursor,
            table_name=ANSWER_PUBLISH_RECORDS_TABLE,
            column_name=str(column["column_name"]),
            display_name=str(column["display_name"]),
            description=str(column["description"]) if column.get("description") else None,
            visible=int(column["visible"]),
            searchable=int(column["searchable"]),
            editable=int(column["editable"]),
            display_type=str(column["display_type"]) if column.get("display_type") else None,
        )


def init_display_metadata(cursor) -> None:
    init_display_metadata_tables(cursor)
    seed_task_logs_display_metadata(cursor)
    seed_answer_publish_records_display_metadata(cursor)


def iter_user_tables(cursor) -> Iterable[str]:
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
    )
    for (name,) in cursor.fetchall():
        if name in METADATA_TABLES:
            continue
        yield str(name)


def _quote_identifier(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def list_physical_column_names(cursor, table_name: str) -> list[str]:
    cursor.execute(f"PRAGMA table_info({_quote_identifier(table_name)})")
    rows = cursor.fetchall()
    rows.sort(key=lambda row: int(row[0]))
    return [str(row[1]) for row in rows]
