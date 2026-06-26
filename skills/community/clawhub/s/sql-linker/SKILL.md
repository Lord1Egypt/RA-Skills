---
name: sql-linker
version: "1.3.0"
description: "Use this skill when you need to query, insert, update, or delete records in the configured MySQL/PostgreSQL/SQLite database and you know the target table name and approximate schema. Triggers include: (1) explicitly requesting a SELECT/INSERT/UPDATE/DELETE on a named table; (2) asking for a specific record by ID or a specific filter; (3) requesting audit log review for sql_audit_log; (4) explicitly asking to bootstrap or inspect the sql-linker configuration. Do NOT trigger on generic "database", "查数据库", "SQL", or "CRUD" without a specific target table or intent."
requires:
  python_packages:
    - mysql-connector-python  # MySQL support
    - pymysql                # MySQL support (alternative)
    - psycopg2               # PostgreSQL support
    - pyyaml                 # Config file parsing
    - pywin32                # Windows DPAPI password decryption (optional; without this, password_dpapi is unavailable)
---

> **Important:** All `scripts/` paths are relative to this skill directory.
> Run with: `cd {skill_dir} && python scripts/...` or use the `cwd` parameter.

***

## ⚠️ Security & Privacy Notice / 安全与隐私声明

> **Please read this notice before using this skill. / （必读）使用本 skill 前请仔细阅读本声明。**

### ⚠️ Credential Access Notice / 凭据访问声明

**How credentials are resolved (in order of precedence):**

| Field in config.yaml | Resolution                                                        | Risk Level                                        |
| -------------------- | ----------------------------------------------------------------- | ------------------------------------------------- |
| `password`           | Direct plaintext in config                                        | ⚠️ Not recommended; commits secret to config file |
| `password_env`       | Reads OS environment variable, **decrypted with** **`dbpw_key`**  | Low — encrypted password + key required           |
| `dbpw_key`           | 6-char encryption key for hybrid password encryption              | **Required** for `password_env` decryption        |
| `password_dpapi`     | DPAPI-decrypts base64 value using current Windows user credential | Moderate — can recover stored secret at runtime   |

> **Security (Hybrid Encryption)**:
>
> - Password is encrypted with `dbpw_key` before storing in OS env
> - **Both** the encrypted password (in env) **and** `dbpw_key` (in config.yaml) are needed to decrypt
> - Even if env is leaked, password cannot be recovered without `dbpw_key`
> - OpenClaw agent cannot access password without knowing `dbpw_key`

> **Display Protection**: When entering password, terminal shows no echo. Output only shows length and head+tail preview (e.g., `te**23` for `test123`).

> ⚠️ **IMPORTANT**: Keep `dbpw_key` secret! If lost, password cannot be recovered.

> **Optional Hardening —** **`require_explicit_credential_approval`**: To force explicit confirmation before silent credential loading, set `require_explicit_credential_approval: true` in `audit_config.json`. When enabled, the first connection attempt with `password_env`/`password_dpapi` will raise `PermissionError` until you call `db.explicit_credential_approval()` in your code.

### ⚠️ Connection-on-Init Notice / 连接初始化声明

Creating a `SQLLinker` or `DBBridge` instance does **not** automatically connect. Connection is deferred until the first actual database call (`connect()` is called lazily on first query). This avoids premature infrastructure access.

### ⚠️ Audit Data Collection Notice / 审计数据收集声明

> **Data Minimization**: Audit records collect the minimum identity fields required for compliance traceability: `user_name`, `user_label`, `session_id`, and optionally `ip_address` (disabled by default). SQL text is masked before logging. No passwords, personal identity numbers, or business-sensitive fields are intentionally captured.
>
> **Retention**: Audit records are stored in `sql_audit_log` in the target database. Retention policy is determined by your organization's database retention schedule, not by this skill.
>
> **Opt-Out**: Set `audit: enabled: false` in `audit_config.json` to disable application-layer audit logging. Database-layer triggers (if any) are independent of this setting.
>
> **Consent**: By using this skill, you consent to having database operation metadata (operator identity, table name, masked SQL, row counts, timestamp, status) recorded in `sql_audit_log`. Do not include sensitive personal data (e.g., national ID numbers, passwords, medical info) in SQL query parameters — such values will be masked but still persisted in log records.

### Audit Data Collection / 审计数据收集

**Audit Log**: Every database operation records the following fields to `sql_audit_log`:

| Field           | Description        | Source                                                        |
| --------------- | ------------------ | ------------------------------------------------------------- |
| `user_name`     | Operator name      | Explicit parameter or `audit_config.json` username            |
| `user_label`    | Source label       | Explicit parameter or `OPENCLAW_LABEL` env                    |
| `ip_address`    | Client IP          | Explicit parameter or LAN IP (only if `collect_lan_ip: true`) |
| `session_id`    | Session identifier | Explicit parameter or `OPENCLAW_SESSION` env                  |
| `sql_statement` | Full SQL statement | Parameterized and masked (literals replaced with `?`)         |
| `rows_affected` | Rows affected      | Database return                                               |
| `status`        | Operation status   | SUCCESS / FAILED                                              |

⚡ **Privacy Notice**: SQL text is masked before logging — string and numeric literals are replaced with `?`. No password or raw PII is intentionally stored. However, the log table itself contains identity metadata; treat it as sensitive. Avoid including sensitive personal data in query parameters.

### Automatic Data Discovery (Can Be Disabled) / 自动数据发现（可关闭）

By default, this skill auto-collects audit context from the following sources:

| Source                 | Collected Data | How to Disable                                                      |
| ---------------------- | -------------- | ------------------------------------------------------------------- |
| `OPENCLAW_USER` env    | Username       | Explicitly pass `user_name` parameter                               |
| `OPENCLAW_LABEL` env   | Source label   | Explicitly pass `user_label` parameter                              |
| `OPENCLAW_SESSION` env | Session ID     | Explicitly pass `session_id` parameter                              |
| LAN IP auto-detection  | Local LAN IP   | Set `collect_lan_ip: false` in `audit_config.json` (default: false) |

If you do not want auto-collection, **explicitly pass** `user_label` and `session_id` parameters — this skill will prefer passed values over auto-discovery.

### Automatic Config File Creation / 配置文件自动创建

On first use or when config files are missing, this skill auto-creates files under `~/.sql_linker/`:

| File                               | Description                                            |
| ---------------------------------- | ------------------------------------------------------ |
| `config_home/config.yaml`          | Database connection config                             |
| `config_home/audit_config.json`    | Audit configuration                                    |
| `config_home/extra_tables.json`    | Privileged table config                                |
| `table_home/table_dictionary.json` | Main dictionary                                        |
| `set_env.ps1`                      | Password setup script for Windows (auto-generated)     |
| `set_env.sh`                       | Password setup script for Linux/macOS (auto-generated) |

> **Password Setup**: Run `set_env.ps1` (Windows) or `set_env.sh` (Linux/macOS) in `.sql_linker/` folder to encrypt and save the database password. Password is encrypted with `dbpw_key` before storing in OS env.

For full manual control, create these files before invoking the skill. `bootstrap()` is idempotent but prints a safety warning before creating files.

### Password Precedence / 密码来源优先级

`password` > `password_env` + `dbpw_key` > `password_dpapi`

- **`password`**: Direct plaintext (not recommended)
- **`password_env`**: OS environment variable with encrypted password (requires `dbpw_key` to decrypt)
- **`dbpw_key`**: 6-char encryption key (auto-generated by bootstrap, **keep secret**)
- **`password_dpapi`**: Windows DPAPI decryption (Windows only, user-scoped)

**Setting the password (Windows)**:

```powershell
# 1. Ensure config.yaml has dbpw_key
# 2. Run set_env.ps1 to encrypt and save password
cd .sql_linker
.\set_env.ps1
# Enter password (no echo in terminal)
# Output shows: length + head+tail preview (e.g., "Wo**88")
```

**First-time setup (after bootstrap)**:

1. Run `bootstrap(dry_run=False, explicit_confirm=True)`
2. **SAVE the** **`dbpw_key`** shown in output (e.g., `Kx****`)
3. Run `set_env.ps1` to set encrypted password
4. **REMEMBER the dbpw\_key** — without it, password cannot be recovered!

### Destructive Operations / 破坏性操作确认

`UPDATE` / `DELETE` operations execute directly and cannot be rolled back. In production, enable read-only mode (`read_only: true`) for pre-validation.

***

## Legacy Users Notice / 旧版用户请注意

**Version 1.2.3 → 1.3.0 Changes**:

- **`dbpw_key`** **added**: Password encryption now requires `dbpw_key` (6-char key) for hybrid encryption
- `password_env` stores encrypted password, decrypted using `dbpw_key` from config.yaml
- Both encrypted password (in env) AND `dbpw_key` (in config.yaml) are required to decrypt
- OpenClaw agent cannot access password without knowing `dbpw_key`
- `set_env.ps1` encrypts password before saving to OS env
- Output shows only password length and head+tail preview (e.g., `Wo**88`)
- `dbpw_key` auto-generated by bootstrap, **must be kept secret**
- `.env` file no longer created by bootstrap or used

**Version 1.2.2 → 1.2.3 Changes**:

- `bootstrap(dry_run=False)` now requires `explicit_confirm=True` to write files — a `BootstrapConfirmationRequired` exception is raised otherwise. This prevents accidental configuration persistence in shared workspaces (Finding #1 of the ClawHub security audit, 62% confidence)
- New exception `BootstrapConfirmationRequired` raised when bootstrap write is attempted without explicit confirmation
- `DBBridge.bootstrap()` forwards the new `explicit_confirm` parameter

**Version 1.1.1 → 1.2.0 Changes**:

- Tightened trigger language: removed "whenever" + vague "CRUD tasks" / "data manipulation" open-ended triggers; now requires specific named table or explicit intent
- Added Credential Access Notice: documents `password_env` / `password_dpapi` auto-resolution and the no-prompt nature of credential loading
- Added Connection-on-Init Notice: clarifies that `SQLLinker`/`DBBridge` instantiation does NOT auto-connect
- Added Audit Data Minimization & Consent Notice: documents what is/isn't captured, opt-out path, and privacy expectations
- Audit log SELECT can be disabled via `log_select: false` (default false) — SELECT logging only occurs when BOTH `audit: enabled: true` AND `log_select: true`
- `collect_lan_ip` defaults to false (was not explicitly defaulted before)
- `session_id` / `user_label` prefer explicitly passed values; no longer auto-read from `sessions.json`

***

# SQL-Linker — 双层架构：数据操作层 + 业务层 / Data Ops + Business Layer

***

## Overview / 概述

(中文) SQL-Linker 提供跨数据库的 CRUD 操作能力，支持 **MySQL、PostgreSQL、SQLite** 三种主流数据库。内置**审计日志**模块，每次操作自动记录操作人身份、IP、SQL 语句、操作时间，确保数据可溯源、安全可控。业务层（db\_bridge）负责字段白名单过滤和时间戳自动注入，数据操作层（sql\_linker）负责连接管理、CRUD 执行和审计记录，两层严格分离，互不干扰。

(English) SQL-Linker provides cross-database CRUD operations, supporting **MySQL, PostgreSQL, and SQLite**, with a built-in **audit trail** module that automatically records operator identity, IP, SQL statements, and timestamps for full traceability and compliance. The business layer (db\_bridge) handles field whitelist filtering and automatic timestamp injection, while the data operation layer (sql\_linker) manages database connections, CRUD execution, and audit logging. The two layers are strictly separated and independent.

***

## Core Architecture / 核心架构

(中文) 系统由两层组成，业务层和数据操作层职责分明：

(English) The system consists of two layers with clearly defined responsibilities:

```
workspace/
└── .sql_linker/                          ← Config root
    ├── config_home/
    │   ├── config.yaml                   ← DB connection config
    │   ├── audit_config.json             ← Audit config
    │   └── extra_tables.json             ← Privileged table config (JSON)
    └── table_home/
        └── table_dictionary.json         ← Main dictionary (JSON, all controlled tables)

skills/sql-linker/scripts/
├── controller_layer/                      ← Data operation layer
│   ├── sql_linker.py                     ← Connection management + CRUD execution + audit context injection
│   └── sql_audit.py                       ← Audit module (used internally by sql_linker.py)
└── service_layer/                        ← Business layer
    └── db_bridge.py                      ← Four-layer access control + timestamp injection + field whitelist
```

(中文) **业务层（service\_layer）**：读取 table\_dictionary.json，过滤字段，注入时间戳，校验访问权限，调用数据操作层，不直接操作数据库。

(English) **Business Layer (service\_layer)**: Reads table\_dictionary.json, filters fields, injects timestamps, verifies access rights, and calls the data operation layer. Does not directly access the database.

(中文) **数据操作层（controller\_layer）**：管理数据库连接，执行 CRUD 操作，写入审计日志，处理参数化查询，不处理业务逻辑。

(English) **Data Operation Layer (controller\_layer)**: Manages database connections, executes CRUD operations, writes audit logs, handles parameterized queries. Does not process business logic.

***

## Four-Layer Access Model / 四层访问模型

(中文) 系统通过四层访问模型实现精确的表访问控制：

(English) The system implements precise table access control through a four-layer access model:

***

**SYSTEM (系统表 sql\_audit\_log)**

- Hard-coded: db\_bridge.py SYSTEM\_TABLES
- SELECT/INSERT: ALLOW
- UPDATE/DELETE: DENY (SystemTableWriteDenied)
- Field whitelist: N/A
- Timestamp injection: N/A
- Audit: Native cursor bypasses db\_bridge
- ⚠️ **Important**: Audit log is a regular database table, NOT tamper-evident. It does NOT provide cryptographic chaining, signatures, or append-only enforcement. For tamper-evident requirements, implement additional database-layer controls (e.g., triggers, immutable audit tables).

***

***

**NORMAL (主词典表格)**

- File: table\_dictionary.json
- Field whitelist: YES (only fields in table.json)
- Timestamp injection: YES (created\_at/updated\_at auto-generated)
- Audit: Full
- Ready to use without extra config

***

***

**PRIVILEGED (特权表格)**

- File: extra\_tables.json (table list) + config.yaml extra\_tables\_enabled (global on/off switch)
- Field whitelist: NO (unknown schema, direct DB exposure)
- Timestamp injection: NO
- Audit: Full
  - Two-layer gate: (1) table must be listed in extra\_tables.json; (2) config.yaml extra\_tables\_enabled must be true (both required)

***

***

**BLOCKED (禁用)**

- Not in dictionary nor extra\_tables
- All operations denied, denial logged
- Cannot access unless added to extra\_tables.json

(中文) **访问判定流程**：提取 SQL 中的表名 → 检查 SYSTEM → 检查主词典（NORMAL）→ 检查 extra\_tables（PRIVILEGED）→ 其余 BLOCKED。

## (English) **Access Decision Flow**: Extract table name from SQL → Check SYSTEM → Check main dictionary (NORMAL) → Check extra\_tables (PRIVILEGED) → Rest BLOCKED.

***

## Bootstrap / 引导初始化

(中文) 首次使用或缺少配置文件时，系统自动生成默认模板（幂等操作，不会覆盖已有文件）：

(English) On first use or when config files are missing, the system automatically generates default templates (idempotent, will not overwrite existing files):

> ⚠️ **Bootstrap 自动创建配置**：首次使用时会自动在 `~/.sql_linker/` 目录下创建配置文件（`config.yaml`、`audit_config.json` 等）。密码请使用 `set_env.ps1` 设置到 Windows 环境变量。`bootstrap()` 为幂等操作，不会覆盖已有文件，但会创建缺失的文件。

```python
from db_bridge import DBBridge

db = DBBridge(user_label="openclaw-control-ui", session_id="agent:hr:main")

# Preview files to be created (no actual write)
preview = db.bootstrap(dry_run=True)
print(f'Will create: {preview}')

# Execute actual bootstrap
created = db.bootstrap()
print(f'Created: {created}')
# ['...\\config.yaml', '...\\audit_config.json', ...]
```

(中文) **自动生成的文件列表**：

(English) **Auto-generated files**:

| File Path                                      | Default Content                                                                    |
| ---------------------------------------------- | ---------------------------------------------------------------------------------- |
| `.sql_linker/config_home/config.yaml`          | Connection template (host/port/user placeholders, password\_env references OS env) |
| `.sql_linker/config_home/audit_config.json`    | Audit ON by default, log\_select=false, collect\_lan\_ip=false                     |
| `.sql_linker/config_home/extra_tables.json`    | Privileged tables, disabled by default, max\_extra\_tables=10                      |
| `.sql_linker/table_home/table_dictionary.json` | Empty template with example table                                                  |
| `.sql_linker/set_env.ps1`                      | Password setup script for Windows (run to set password in OS env)                  |
| `.sql_linker/set_env.sh`                       | Password setup script for Linux/macOS (run to set password in OS env)              |

***

## Config Files / 配置文件说明

### `table_home/table_dictionary.json` — Main Dictionary / 主词典

(中文) 所有受控业务表必须在主词典中声明，字段白名单仅对 NORMAL 层生效：

(English) All controlled business tables must be declared in the main dictionary. Field whitelist only applies to NORMAL layer:

```json
{
  "version": 1,
  "tables": [
    {
      "table_name": "supplier_table",
      "comment": "供应商信息表",
      "fields": [
        { "name": "id",            "type": "BIGINT",       "pk": true,  "auto": true  },
        { "name": "supplier_code", "type": "VARCHAR(32)",  "pk": false, "auto": false },
        { "name": "supplier_name", "type": "VARCHAR(128)", "pk": false, "auto": false },
        { "name": "short_name",    "type": "VARCHAR(64)",  "pk": false, "auto": false },
        { "name": "supplier_level","type": "VARCHAR(16)",  "pk": false, "auto": false },
        { "name": "contact_person","type": "VARCHAR(64)",  "pk": false, "auto": false },
        { "name": "contact_phone", "type": "VARCHAR(32)",  "pk": false, "auto": false },
        { "name": "contact_email", "type": "VARCHAR(128)", "pk": false, "auto": false },
        { "name": "status",        "type": "VARCHAR(16)",  "pk": false, "auto": false },
        { "name": "created_at",    "type": "DATETIME",     "pk": false, "auto": false },
        { "name": "updated_at",   "type": "DATETIME",     "pk": false, "auto": false }
      ]
    }
  ]
}
```

### `config_home/extra_tables.json` — Privileged Table Config / 特权表配置

(中文) 词典外表格需通过此配置显式授权，enabled=false 时所有非词典表均 BLOCKED：

(English) Tables outside the dictionary require explicit authorization via this config. When enabled=false, all non-dictionary tables are BLOCKED:

```json
{
  "version": 1,
  "enabled": false,
  "max_extra_tables": 10,
  "tables": [
    { "table_name": "employee_table" },
    { "table_name": "payroll_table" }
  ]
}
```

| Field                 | Description                                                                |
| --------------------- | -------------------------------------------------------------------------- |
| `enabled`             | false=disable dict-external access (default) / true=enable privileged mode |
| `max_extra_tables`    | Max declared tables, prevents config runaway                               |
| `tables[].table_name` | Privileged table name                                                      |

### `config_home/config.yaml` — Connection Config / 连接配置

(中文) 数据库连接配置，password 不直接写在文件中，通过 password\_env 引用加密后的密码，dbpw\_key 用于混合加密：

(English) Database connection config. Password is encrypted with `dbpw_key` before storing in OS env:

```yaml
type: mysql
host: 127.0.0.1
port: 3306
database: db_dev
user: admin
password_env: mysql_pw           # OS env key (stores encrypted password)
dbpw_key: Kx9mT2                 # 6-char encryption key (KEEP SECRET!)
# password_dpapi: AQAAANCMnd8BFdERjHoAwE/Cl+sBAAAA...   # DPAPI-encrypted password (optional)
read_only: false
max_rows: 1000
timeout: 30
extra_tables_enabled: false
```

> **Security**: Password is encrypted with `dbpw_key` using HMAC-SHA256. Both encrypted password (in OS env) AND `dbpw_key` (in config) are required to decrypt. OpenClaw agent cannot access password without knowing `dbpw_key`.

***

## Python API — Business Layer (Recommended) / Python API — 业务层（推荐）

(中文) 使用业务层 API（推荐），完整支持四层访问控制和时间戳自动注入：

(English) Use the business layer API (recommended), with full four-layer access control and automatic timestamp injection:

```python
import sys
sys.path.insert(0, "skills/sql-linker/scripts/service_layer")
from db_bridge import DBBridge

db = DBBridge(
    user_label="openclaw-control-ui",   # ← OpenClaw metadata.label
    session_id="agent:hr:main"          # ← OpenClaw metadata.id
)
```

### INSERT — Automatic Timestamp Injection / 时间戳自动注入

(中文) INSERT 操作自动生成 created\_at 和 updated\_at（两者同值），仅写入主词典中声明的字段：

(English) INSERT operations automatically generate created\_at and updated\_at (same value), writing only fields declared in the main dictionary:

```python
db.insert("supplier_table", {
    "supplier_code": "LX001",
    "supplier_name": "立讯精密",
    "supplier_level": "A",
    "status": "active"
})
# → created_at / updated_at auto-generated, no manual injection needed
```

### UPDATE — Automatic Timestamp Refresh / 时间戳自动刷新

(中文) UPDATE 操作自动刷新 updated\_at，created\_at 保持不变：

(English) UPDATE operations automatically refresh updated\_at, leaving created\_at unchanged:

```python
db.update(
    "supplier_table",
    {"supplier_level": "AA"},
    "supplier_code = %s",
    ("LX001",)
)
# → updated_at auto-refreshed to current time
```

### DELETE — Full Audit / 完整审计

```python
db.delete("supplier_table", "status = %s", ("inactive",))
```

### SELECT — Parameterized Injection Prevention / 参数化防注入

```python
rows = db.query(
    "SELECT * FROM supplier_table WHERE status = %s AND supplier_level = %s",
    ("active", "A")
)
for row in rows:
    print(row)
```

### Helper Methods / 辅助方法

```python
db.tables()           # Return all table names in main dictionary
db.extra_tables()     # Return current privileged table list
db.system_tables()    # Return protected system table list
db.fields("supplier_table")  # Return table field list (privilege table returns empty)
db.bootstrap(dry_run=False) # Execute bootstrap; dry_run=True returns file list without writing
```

### Error Handling / 错误处理

```python
from db_bridge import TableAccessDenied, SystemTableWriteDenied

try:
    db.query("SELECT * FROM unknown_table LIMIT 1")
except TableAccessDenied as e:
    print("Access denied:", e)

try:
    db.update("sql_audit_log", {"status": "tampered"}, "id = %s", (1,))
except SystemTableWriteDenied as e:
    print("System table write denied:", e)
```

***

## Python API — Data Operation Layer / Python API — 数据操作层

(中文) 直接使用数据操作层，跳过业务层字段过滤和时间戳注入（适用于高级用户）：

(English) Use the data operation layer directly, bypassing business layer field filtering and timestamp injection (for advanced users):

```python
import sys
sys.path.insert(0, "skills/sql-linker/scripts/controller_layer")
from sql_linker import SQLLinker

linker = SQLLinker()
linker.connect()
# Explicit audit context (preferred over auto-discovery)
linker.set_user_context(user_name="HR", user_label="openclaw-control-ui",
                        ip_address="", session_id="agent:hr:main")
```

***

## Timestamp Logic / 时间戳注入规则

| Operation  | created\_at | updated\_at            | Applicable Layer |
| ---------- | ----------- | ---------------------- | ---------------- |
| INSERT     | Auto        | Auto (same as created) | NORMAL           |
| UPDATE     | Unchanged   | Auto-refresh           | NORMAL           |
| DELETE     | N/A         | N/A                    | NORMAL           |
| PRIVILEGED | N/A         | N/A                    | PRIVILEGED       |

***

## Audit Trail / 审计日志

(中文) **配置位置**：`.sql_linker/config_home/audit_config.json`

(English) **Config location**: `.sql_linker/config_home/audit_config.json`

```json
{
  "username": "HR",
  "audit": {
    "enabled": true,
    "log_table": "sql_audit_log",
    "log_select": false,
    "mask_values": true,
    "collect_lan_ip": false
  }
}
```

(中文) **审计记录字段**（自动注入，不可为空）：

(English) **Audit record fields** (automatically injected, must not be empty):

| Field           | Description          | Source                                            |
| --------------- | -------------------- | ------------------------------------------------- |
| `user_name`     | Operator             | audit\_config.json username                       |
| `user_label`    | Source label         | Explicit or OPENCLAW\_LABEL env                   |
| `ip_address`    | Local LAN IP         | Explicit or `_get_lan_ip()` (disabled by default) |
| `session_id`    | OpenClaw Session Key | Explicit or OPENCLAW\_SESSION env                 |
| `operation`     | Operation type       | SELECT / INSERT / UPDATE / DELETE                 |
| `table_name`    | Target table         | Extracted from SQL                                |
| `sql_statement` | SQL statement        | Parameterized mask (%s)                           |
| `rows_affected` | Rows affected        | Database return                                   |
| `status`        | Operation status     | SUCCESS / FAILED                                  |

***

## Field Type Reference / 字段类型参考

| type value     | Description                               |
| -------------- | ----------------------------------------- |
| `BIGINT`       | Primary key / auto-increment ID           |
| `VARCHAR(n)`   | String, max n characters                  |
| `TEXT`         | Long text                                 |
| `INT`          | Integer                                   |
| `DECIMAL(m,n)` | Decimal, m total digits, n decimal places |
| `DATETIME`     | Date time (`YYYY-MM-DD HH:MM:SS`)         |
| `DATE`         | Date                                      |
| `BOOL`         | Boolean                                   |

***

## Dual-Layer Audit / 双层审计体系

sql-linker adopts **application layer + database layer** dual-layer audit; any direct-connection bypass of the application layer is still captured.

### Audit Log Query / 审计日志查看

`sql_audit_log` is in SYSTEM layer, business layer can SELECT directly:

```python
from datetime import date, timedelta
db = DBBridge(user_label="audit-viewer", session_id="agent:audit")

# Query today's operation records
today = date.today().strftime('%Y-%m-%d')
rows = db.query(
    "SELECT log_time, user_name, operation, table_name, sql_statement, rows_affected, status "
    "FROM sql_audit_log WHERE DATE(log_time) = %s ORDER BY log_time DESC",
    (today,)
)

# Query failed operations in last 7 days
week_ago = (date.today() - timedelta(days=7)).strftime('%Y-%m-%d')
failed = db.query(
    "SELECT * FROM sql_audit_log WHERE status = 'FAILED' AND log_time >= %s "
    "ORDER BY log_time DESC",
    (week_ago,)
)

# Query recent operations for a supplier (fuzzy match)
rows = db.query(
    "SELECT log_time, user_name, operation, table_name, sql_statement "
    "FROM sql_audit_log WHERE sql_statement LIKE %s ORDER BY log_time DESC LIMIT 20",
    ('%LX001%',)
)
```

> ⚠️ `sql_audit_log` is a system-protected table. UPDATE/DELETE blocked by `SystemTableWriteDenied`. Only SELECT is allowed.

### Layer 1: Application-Layer Audit / 第一层：应用层审计

- Component: `sql_linker.py` → `SQLAudit` class
- Mechanism: Write to `sql_audit_log` after each CRUD operation
- Coverage: Operations via `db_bridge` only
- Limitation: Direct `pymysql` / `mysql CLI` can bypass

### Layer 2: Database-Layer Trigger / 第二层：数据库层触发器

- **Nature**: Deployment artifact, not part of the skill package. Triggers are bound to specific table schemas, created by the deployer/DBA per actual schema.
- Mechanism: Create `AFTER INSERT/UPDATE/DELETE` triggers on MySQL side, mandatory write to `sql_audit_log`
- Coverage: **All write operations directly connecting to the database**, regardless of connection tool or path

### Trigger Writing Principles / 触发器编写原则

On **each controlled business table**, create one `AFTER` trigger each for `INSERT` / `UPDATE` / `DELETE`. Example structure:

```sql
-- Example using supplier_capa (same for other tables)
CREATE TRIGGER trg_<table>_ai
AFTER INSERT ON <table>
FOR EACH ROW
BEGIN
  INSERT INTO sql_audit_log
    (log_time, user_name, user_label, ip_address, session_id,
     db_type, operation, table_name, sql_statement, rows_affected, status, error_msg)
  VALUES
    (NOW(), CURRENT_USER(), 'DB_TRIGGER', 'internal', 'DB_TRIGGER',
     'mysql', 'INSERT', '<table>',
     CONCAT('INSERT id=', NEW.id, ' supplier_code=', NEW.supplier_code),
     1, 'SUCCESS', NULL);
END;
```

**Implementation Steps**:

1. Confirm `sql_audit_log.id` is `AUTO_INCREMENT` (otherwise trigger INSERT fails due to no default id)
2. Execute three triggers for each controlled table
3. Triggers saved in user repository or DBA management scripts, not distributed with the skill package

### Dual-Layer Combined Effect / 两层配合效果

| Operation Path   | App-Layer Audit | Trigger Audit | Conclusion       |
| ---------------- | --------------- | ------------- | ---------------- |
| db\_bridge CRUD  | ✅ Logged        | ✅ Logged      | Double guarantee |
| pymysql direct   | ❌ Bypassed      | ✅ Logged      | Trigger fallback |
| mysql CLI direct | ❌ Bypassed      | ✅ Logged      | Trigger fallback |
| DBA direct op    | ❌ Bypassed      | ✅ Logged      | Trigger fallback |

***

## Security Principles / 安全原则

(中文)

1. **Field Whitelist**: `NORMAL` tables only write fields declared in `table_dictionary.json`; illegal fields auto-filter
2. **Four-Layer Access Control**: SYSTEM (read+audit write) / dict (whitelist+timestamp) / privileged (direct) / blocked (deny)
3. **Parameterized Queries**: All use `%s` + tuple to prevent SQL injection
4. **Sensitive Credential Separation**: `password_env` reads from Windows OS env; `password_dpapi` (DPAPI encrypted) alternative — no plaintext in files
5. **Dual-Layer Audit**: Application-layer `db_bridge` + database-layer triggers (created by deployer per actual schema)
6. **System Table Protection**: `sql_audit_log` prohibits UPDATE/DELETE, `SystemTableWriteDenied` exception enforced
7. **Idempotent Bootstrap**: Missing config files auto-generated without overwriting existing configs

(English)

1. **Field Whitelist**: `NORMAL` tables only write fields declared in `table_dictionary.json`; illegal fields are automatically filtered
2. **Four-Layer Access Control**: SYSTEM table (read+audit write) / Normal dictionary (whitelist+timestamp) / Privileged (direct query) / Blocked (denied)
3. **Parameterized Queries**: All use `%s` + tuple to prevent SQL injection
4. **Sensitive Credential Separation**: `password_env` reads from Windows OS env (set via `set_env.ps1`); `password_dpapi` alternative — no plaintext in any file
5. **Dual-Layer Audit**: Application-layer `db_bridge` + database-layer triggers (created by deployer per actual schema)
6. **System Table Protection**: `sql_audit_log` prohibits UPDATE/DELETE, `SystemTableWriteDenied` exception enforced
7. **Idempotent Bootstrap**: Missing config files are auto-generated without overwriting existing configs

***

## Common Errors and Solutions / 常见错误与解法

| Error                                                         | Cause                                         | Solution                                                                  |
| ------------------------------------------------------------- | --------------------------------------------- | ------------------------------------------------------------------------- |
| `TableAccessDenied: Table 'xxx' not in dictionary`            | Table not in dictionary and not authorized    | Add to `extra_tables.json` + `enabled:true`                               |
| `SystemTableWriteDenied: sql_audit_log does not allow UPDATE` | Attempt to tamper audit log                   | Normal interception; if misjudged, contact DBA                            |
| Audit write failed but data succeeded                         | Audit and business not in same transaction    | Triggers provide fallback; app-layer fix pending                          |
| `Access denied for user ... (using password: NO)`             | Password not decrypted correctly              | Ensure `dbpw_key` in config.yaml matches when password was set            |
| `Password not found: run set_env.ps1`                         | Environment variable or `dbpw_key` missing    | Run `set_env.ps1` to encrypt and save password; ensure `dbpw_key` exists  |
| `HMAC verification failed`                                    | Wrong `dbpw_key`                              | Check `dbpw_key` in config.yaml matches when password was encrypted       |
| `Config file not found`                                       | Config file missing                           | Call `db.bootstrap()` to auto-generate, or check `.sql_linker/` structure |
| `Table not found`                                             | Table not declared in `table_dictionary.json` | Add table config in main dictionary                                       |

***

## Directory Structure Overview / 目录结构总览

```
workspace/
└── .sql_linker/
    ├── set_env.ps1                    ← Password setup script for Windows (auto-generated)
    ├── set_env.sh                     ← Password setup script for Linux/macOS (auto-generated)
    ├── config_home/
    │   ├── config.yaml                 ← Connection config (extra_tables_enabled switch)
    │   ├── audit_config.json           ← Audit config (collect_lan_ip option)
    │   └── extra_tables.json           ← Privileged table list (JSON)
    └── table_home/
        └── table_dictionary.json       ← Main dictionary (JSON, all controlled tables)
            └── tables[]                 ← Each table's fields[] whitelist + comment

skills/sql-linker/
├── SKILL.md                           ← This document
└── scripts/
    ├── controller_layer/               ← Data operation layer
    │   ├── sql_linker.py              ← Connection management + CRUD + audit
    │   └── sql_audit.py               ← Audit module
    └── service_layer/                  ← Business layer
        └── db_bridge.py               ← Four-layer access + timestamp + Bootstrap
```

