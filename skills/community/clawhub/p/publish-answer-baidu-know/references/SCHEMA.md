# 数据存储与数据管理展示规范

本文是 skill 本地 SQLite 与匠厂宿主「数据管理」页面展示契约的**权威说明**。
实现上的 DDL 与默认中文元数据种子见 `scripts/db/display_metadata.py`；`scripts/db/connection.py` 的 `init_db()` 会一并初始化。

## 职责边界

| 层级 | 负责内容 |
|------|----------|
| **技能（本仓库）** | `SKILL.md.name` 中文技能名；英文物理表/字段名；`_jiangchang_*` 中文展示元数据；`CREATE TABLE` 字段物理顺序 |
| **宿主（匠厂）** | 读取元数据与 PRAGMA 顺序并展示；不猜测业务语义、不按英文字段名重排 |

SQLite **没有**可靠的 `COMMENT ON TABLE/COLUMN`；SQL 文件里的 `-- 注释` 也不会成为可查询结构。
因此中文展示名称必须写入元数据表；字段顺序必须写在 `CREATE TABLE` 的列定义顺序中（`PRAGMA table_info` 的 `cid`）。

> **禁止**新技能使用宿主的旧版 `_schema_meta` 表。仅 `_jiangchang_tables` / `_jiangchang_columns` 为正式契约。

## 技能名称（SKILL.md）

```yaml
---
name: 中文业务名称
description: 中文技能说明
metadata:
  openclaw:
    slug: english-kebab-slug
---
```

- `name`：用户可见的中文业务名称（可含品牌，如 `GEO 文章生成`、`1688 联系人采集`）。
- `description`：能力说明，不是技能名称。
- `metadata.openclaw.slug`：机器标识，kebab-case 英文；目录名与默认数据库文件名使用 slug。slug 语义规范见 [`../development/NAMING.md`](../development/NAMING.md)；本文件仅描述数据库与 kebab-case 格式。
- 复制模板后不得将 `your-skill-slug`、`My Skill` 等占位内容作为正式技能发布名称。

## 数据库路径与命名

```text
{JIANGCHANG_DATA_ROOT}/{JIANGCHANG_USER_ID}/{skill-slug}/{skill-slug}.db
```

- 数据库文件：英文 slug，例如 `scrape-contacts.db`、`account-manager.db`（默认 `{skill-slug}.db`）。
- 业务表、字段：**英文 snake_case** 物理名，例如 `task_logs`、`created_at`。
- **禁止**用中文作为 SQLite 真实表名或字段名。

## 元数据表（宿主兼容）

宿主读取字段（与 `jiangchang` `metadata-resolver.ts` 一致）：

### `_jiangchang_tables`

| 字段 | 必填 | 说明 |
|------|------|------|
| `table_name` | 是 | 物理表名 |
| `display_name` | 是 | 中文表名（用户可见） |
| `description` | 否 | 表说明 |
| `sort_order` | 否 | 宿主目录排序；与字段顺序无关 |
| `visible` | 是 | `1` 展示 / `0` 隐藏 |
| `readonly` | 是 | `1` 只读 / `0` 可写（业务语义） |

### `_jiangchang_columns`

| 字段 | 必填 | 说明 |
|------|------|------|
| `table_name` | 是 | 物理表名 |
| `column_name` | 是 | 物理字段名 |
| `display_name` | 是 | 中文字段名（用户可见） |
| `description` | 否 | 字段说明 |
| `display_order` | 否 | **遗留兼容字段；模板写入时固定 NULL，重复初始化会清理历史非空值，不得用于调整展示顺序** |
| `visible` | 是 | 是否展示 |
| `searchable` | 是 | 是否可搜索 |
| `editable` | 是 | 是否可编辑（与宿主权限结合） |
| `display_type` | 否 | 如 `text` / `textarea` / `datetime_unix_seconds`（标准时间字段见下文） |
| `options_json` | 否 | 枚举选项 JSON |

这两张表是**数据字典**，不是业务数据；宿主不会把它们当作普通业务表展示。

写入应**幂等**（`INSERT … ON CONFLICT DO UPDATE`），数据库升级时同步维护元数据。

## 业务字段物理顺序

用户在「数据管理」中看到的列顺序 = `CREATE TABLE` 定义顺序 = `PRAGMA table_info` 的 `cid` 顺序。
**宿主不会**按英文字段名、`display_order` 或语义规则重排。

推荐顺序（可按业务裁剪，但已有字段应遵守相对位置）：

```text
1. 主键 id
2. 关联标识与核心业务字段
3. 普通业务字段
4. 状态、结果、错误等辅助字段
5. created_at（如有）
6. updated_at（如有）

## 标准时间字段（新技能统一规范）

新技能业务表若需要时间审计字段，**统一**采用 Unix **秒级**时间戳，不要使用毫秒时间戳、ISO 字符串或 SQLite 文本 datetime。

| 项目 | 规范 |
|------|------|
| 物理字段 | `created_at INTEGER`、`updated_at INTEGER` |
| 存储格式 | Unix 秒级整数 |
| 展示元数据 `display_type` | `datetime_unix_seconds` |
| 中文名 | `created_at` → **创建时间**；`updated_at` → **更新时间** |
| 用户编辑 | `editable = 0`（系统字段，宿主只展示格式化结果，不写回字符串） |
| 字段顺序 | 位于业务字段末尾：`… → created_at → updated_at` |
| 排序 | **不使用** `display_order`；顺序仅来自 `PRAGMA table_info` |

### 自动生成与维护

- **created_at**：`INTEGER NOT NULL DEFAULT (unixepoch())`；插入时可省略，由数据库生成。
- **updated_at**：`INTEGER NOT NULL DEFAULT (unixepoch())`；插入时同样可省略。
- **updated_at 更新**：模板默认表 `task_logs` 通过 SQLite trigger `{table}_set_updated_at` 在业务字段更新后自动刷新；若技能所有 UPDATE 都经过统一 repository，也可在 repository 层设置 `updated_at = unixepoch()`，**不要**叠加两套机制。

实现参考：

- DDL 与 trigger：`scripts/db/connection.py`、`scripts/db/timestamp_columns.py`
- 中文元数据种子：`scripts/db/display_metadata.py`
- 自检：`scripts/db/display_metadata_validator.py`

宿主（匠厂）只负责把 `display_type = datetime_unix_seconds` 格式化为 `YYYY-MM-DD HH:mm:ss` 展示，**不修改**数据库原始值。

> `datetime_unix_milliseconds`、`datetime_iso` 是宿主兼容能力，**不是**新技能模板推荐标准。

### 模板默认：`task_logs`

物理定义（权威顺序）：

```sql
CREATE TABLE IF NOT EXISTS task_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_type TEXT NOT NULL,
    target_id TEXT,
    input_id TEXT,
    input_title TEXT,
    status TEXT NOT NULL,
    error_msg TEXT,
    result_summary TEXT,
    created_at INTEGER NOT NULL DEFAULT (unixepoch()),
    updated_at INTEGER NOT NULL DEFAULT (unixepoch())
);
```

插入时可省略 `created_at`、`updated_at`；`updated_at` 在 UPDATE 时由 trigger `task_logs_set_updated_at` 自动维护（见 `scripts/db/timestamp_columns.py`）。

对应中文展示（由 `init_db()` 写入元数据表）：

| 物理字段 | 中文名 |
|----------|--------|
| id | 编号 |
| task_type | 任务类型 |
| target_id | 目标编号 |
| input_id | 输入编号 |
| input_title | 输入标题 |
| status | 状态 |
| error_msg | 错误信息 |
| result_summary | 结果摘要 |
| created_at | 创建时间（`display_type = datetime_unix_seconds`，不可编辑） |
| updated_at | 更新时间（`display_type = datetime_unix_seconds`，不可编辑） |

表中文名：**任务日志**。

禁止事项：

- 不要把 `created_at` 放在第一列；
- 不要把 `id` 随意放在中间；
- 不要指望宿主按英文字段名排序；
- 若需调整历史表字段顺序，应通过规范迁移**重建表**，而不是在宿主侧配置掩盖。

复合主键或特殊表结构，请在本文档或技能自有 SCHEMA 补充中说明例外。

### 业务表：`answer_publish_records`

百度知道回答发布记录表。记录每次发布的幂等键、账号、问题 URL、回答文稿路径、发布状态与平台反馈。

物理定义（权威顺序）：

```sql
CREATE TABLE IF NOT EXISTS answer_publish_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    idempotency_key TEXT,
    account_id TEXT NOT NULL,
    question_url TEXT NOT NULL,
    answer_path TEXT NOT NULL,
    status TEXT NOT NULL,
    platform_message TEXT,
    published_at INTEGER,
    created_at INTEGER NOT NULL DEFAULT (unixepoch()),
    updated_at INTEGER NOT NULL DEFAULT (unixepoch())
);
```

幂等索引（部分唯一索引，仅对非 NULL 的 idempotency_key 生效）：

```sql
CREATE UNIQUE INDEX IF NOT EXISTS idx_answer_publish_idempotency
ON answer_publish_records(idempotency_key)
WHERE idempotency_key IS NOT NULL;
```

对应中文展示（由 `init_db()` 写入元数据表）：

| 物理字段 | 中文名 | 说明 |
|----------|--------|------|
| id | 编号 | 发布记录唯一编号 |
| idempotency_key | 幂等键 | 调用方传入的幂等键，同一键不会重复发布 |
| account_id | 账号编号 | 使用的百度知道账号编号 |
| question_url | 问题链接 | 百度知道问题页 URL |
| answer_path | 回答文稿路径 | 本地回答文稿文件路径 |
| status | 发布状态 | `success` / `pending_review` / `failed` |
| platform_message | 平台反馈 | 百度知道返回的提示信息 |
| published_at | 提交时间 | 回答提交到百度知道的时间（Unix 秒级，`display_type = datetime_unix_seconds`） |
| created_at | 创建时间 | 记录创建时间（Unix 秒级，自动生成，不可编辑） |
| updated_at | 更新时间 | 记录最后更新时间（Unix 秒级，自动维护，不可编辑） |

表中文名：**回答发布记录**。

字段顺序说明：

- `id` 主键在首列；
- `idempotency_key` 紧随 `id`，便于人工核对幂等命中；
- 业务字段（`account_id` / `question_url` / `answer_path`）按「账号 → 问题 → 文稿」业务因果顺序排列；
- `status` / `platform_message` / `published_at` 为结果字段，位于业务字段之后；
- `created_at` / `updated_at` 位于末尾，由 trigger 自动维护。

`updated_at` 在 UPDATE 时由 trigger `answer_publish_records_set_updated_at` 自动维护（见 `scripts/db/timestamp_columns.py`）。

实现参考：

- DDL：`scripts/db/connection.py` 的 `init_db()`
- 中文元数据种子：`scripts/db/display_metadata.py` 的 `seed_answer_publish_records_display_metadata()`
- 仓储层：`scripts/db/answer_publish_records_repository.py`

## 中文命名质量

- 使用普通用户能理解的业务用语：`task_logs` → **任务日志**，`error_msg` → **错误信息**。
- 禁止：`Task Logs`、`input编号`、`errormsg`、直接把物理名当 `display_name`。
- 不宜向用户暴露的实现细节（如 `payload_json`、`selector`）应设 `visible = 0` 或给出可理解中文名。

## 元数据同步规则

1. 新增用户可见业务表 → 同步 `_jiangchang_tables`。
2. 新增用户可见字段 → 同步 `_jiangchang_columns`。
3. 删除/重命名表或字段 → 同步清理或迁移元数据。
4. 初始化脚本必须幂等。
5. 元数据中的表、字段必须在库中真实存在；可见项不得缺少中文 `display_name`。

## 不同业务的 `task_logs` 映射

| 业务场景 | task_type | target_id | input_id |
|----------|-----------|-----------|----------|
| 发布类 | publish | 账号 ID | 内容 ID |
| 工资代发 | disburse | 付款账户 | 批次 ID |
| 对账 | reconcile | 银行/平台 | 对账批次 ID |
| 发票验真 | verify | 税务地区 | 发票批次 ID |

业务特有字段优先放入 `result_summary`（JSON 字符串），避免随意加列；若确需新列，必须同步元数据并保持合理物理顺序。

## 开发自检

- `init_db()` 后运行 `tests/test_display_metadata.py`。
- 复制为真实技能后，使用 `scripts/db/display_metadata_validator.py` 中的校验函数检查 SKILL 名称、slug 与元数据完整性。

## 模板原则

- 模板不做复杂历史迁移框架；新 skill 从当前 schema 起步。
- 元数据 DDL 与 `task_logs` 中文种子以 `scripts/db/display_metadata.py` 为单一权威来源。
