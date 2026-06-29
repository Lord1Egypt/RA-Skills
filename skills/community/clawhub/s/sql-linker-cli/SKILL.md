---
name: sql-linker-cli
description: "SQL-Linker CLI: Multi-DB CRUD (MySQL/PostgreSQL/SQLite) with bootstrap config generation, credential management (encrypted password via OS env + cloud dbpw_key), cloud audit sync to https://sqllinker.agentpower.hk.cn, and API key introspection. Per-invocation --approve flag for credential gate."
version: "2.0.3"
requires:
  python_packages:
    - mysql-connector-python  # MySQL support
    - psycopg2               # PostgreSQL support
    - pyyaml                 # Config file parsing
    - pywin32                # Windows DPAPI password decryption (optional)
permissions:
  - environment:read       # Read DB credentials from OS environment variables
  - environment:write      # Write encrypted password to user-scope environment (set_env.ps1/sh)
  - file:read              # Read config.yaml, audit_config.json, table dictionaries
  - file:write             # Write bootstrap config files, audit logs to database
  - network:outbound       # Cloud audit sync to sqllinker.agentpower.hk.cn; API key introspection
---

> **Important / 重要提示：** All `scripts/` paths are relative to this skill directory.
> Run CLI: `cd {skill_dir}/scripts/service_layer && python main.py --help`

***

## sql-linker-cli vs sql-linker

### 中文

**sql-linker-cli** 是 **sql-linker** 的安全增强版，两者主要区别如下：

| 对比项 | sql-linker | sql-linker-cli |
|-------|-----------|----------------|
| **dbpw_key 存储** | 本地存储在 `config.yaml` 中 | **云端管理**，通过 API Key 自动拉取 |
| **凭证密钥隔离** | 本地存储，OpenClaw 可能读取 | **本地与云端隔离**，密钥不在本地 |
| **凭证审批闸门** | 可选配置 | 默认开启，敏感操作需显式授权 |
| **使用场景** | 本地开发、快速原型 | **生产环境推荐**，安全优先 |
| **API Key 管理** | 无 | 云端统一管理，支持 Key 轮换 |
| **审计同步** | 本地 | 云端统一审计 |

**安全优势：**
- `dbpw_key` 不再存储在本地，即使 OpenClaw agent 能读取配置文件，也无法获取数据库密码
- 凭证审批闸门（`--approve`）确保每次敏感操作都有显式授权记录
- 云端统一管理 API Key，支持 Key 轮换和撤销

**迁移指南：**
- 从 sql-linker 迁移到 sql-linker-cli，只需在 [官网](https://sqllinker.agentpower.hk.cn/) 创建 API Key 并填入 `audit_config.json`

### English

**sql-linker-cli** is the **security-enhanced version** of **sql-linker**. Key differences:

| Feature | sql-linker | sql-linker-cli |
|---------|-----------|----------------|
| **dbpw_key storage** | Stored locally in `config.yaml` | **Cloud-managed**, auto-fetched via API Key |
| **Credential isolation** | Local storage, OpenClaw may access | **Local-cloud isolated**, key not on disk |
| **Credential approval gate** | Optional config | Enabled by default, explicit approval required |
| **Use case** | Local dev, quick prototypes | **Production recommended**, security-first |
| **API Key management** | None | Cloud unified management, supports rotation |
| **Audit sync** | Local | Cloud unified audit |

**Security advantages:**
- `dbpw_key` is no longer stored locally; even if OpenClaw reads config files, it cannot obtain the database password
- Credential approval gate (`--approve`) ensures every sensitive operation has explicit authorization
- Cloud unified API Key management supports rotation and revocation

**Migration guide:**
- Migrating from sql-linker to sql-linker-cli: just create an API Key at [portal](https://sqllinker.agentpower.hk.cn/) and fill it into `audit_config.json`

***

## API Key 获取官网

### 中文

> **官方门户：** <https://sqllinker.agentpower.hk.cn/>
>
> 这是获取和管理 **API Key** 的唯一官方地址。所有 `cloud_api_key`、`dbpw_key`、agent 绑定和审计日志查询都在此处。
>
> **获取步骤：**
>
> 1. 打开 <https://sqllinker.agentpower.hk.cn/> 并登录
> 2. 进入 **API Keys** 管理页面
> 3. 点击 **Create** 创建新 key，填写 **agent name**（这个 name 会出现在审计日志的 username 字段里）
> 4. 创建后**立即复制** API Key（格式：`slk_xxxxxxxxxxxxxxx`），关闭对话框就再也看不到完整值
>
> **拿到 API Key 后**：把它填进 `.sql_linker/config_home/audit_config.json` 的 `cloud_api_key` 字段，然后运行 `python main.py apikey status` 验证。

### English

> **Official Portal:** <https://sqllinker.agentpower.hk.cn/>
>
> This is the **only official portal** to obtain and manage API Keys. All `cloud_api_key`, `dbpw_key`, agent binding, and audit log query live here.
>
> **Steps:**
>
> 1. Open <https://sqllinker.agentpower.hk.cn/> and log in
> 2. Go to **API Keys** management page
> 3. Click **Create** to create a new key, fill in **agent name** (this name will appear in audit log `username` field)
> 4. **Copy immediately** after creation (format: `slk_xxxxxxxxxxxxxxx`) — dialog closes and full value is unrecoverable
>
> **After getting the key**: Fill it into `cloud_api_key` field in `.sql_linker/config_home/audit_config.json`, then run `python main.py apikey status` to verify.

***

## Security & Privacy Notice

> **⚠️  Security Disclosures / 安全声明**
>
> This skill has the following security-relevant behaviors that operators should be aware of:
>
> 1. **Cloud Audit Telemetry**: INSERT/UPDATE/DELETE operations automatically transmit SQL metadata (masked), user context, and operation details to `https://sqllinker.agentpower.hk.cn`. This is not optional for write operations.
>
> 2. **Credential Access**: `password_env` reads from OS environment variables; `dbpw_key` is fetched from the cloud API when using cloud-managed credentials.
>
> 3. **Bootstrap File Creation**: `bootstrap` command creates config files in `.sql_linker/` directory. `set_env.ps1/sh` generate encrypted credentials for OS environment variables (user-scope). User must manually add export line to shell config for persistence.
>
> 4. **Arbitrary SQL**: The `query` command accepts any SQL text (not limited to SELECT). Use parameterized queries to prevent injection.

### 中文

### 凭据安全

| config.yaml 字段                   | 解析方式                    | 安全性       |
| -------------------------------- | ----------------------- | --------- |
| `password`                       | 直接明文存储在配置中              | ⚠️ 不推荐    |
| `password_env` + `dbpw_key` (云端) | OS 环境变量存储，用 6 位密钥云端拉取解密 | ✅ 推荐      |
| `password_dpapi`                 | Windows DPAPI 解密        | 仅 Windows |

密码使用 `dbpw_key`（6 位密钥，HMAC-SHA256）加密后存入 OS 环境变量。`dbpw_key` 通过 API Key 从云端自动拉取，**不要本地存储**。

### 云端管理的数据库加密码

配置 `cloud_api_key` 后，`dbpw_key` 从 `https://sqllinker.agentpower.hk.cn/api/user/api-keys/by-key` 接口拉取（需要网络）。

### 云端审计

写操作（INSERT/UPDATE/DELETE）通过 API Key 自动同步到 `https://sqllinker.agentpower.hk.cn/api/audit/logs`。

### 凭证审批闸门

当 `audit.require_explicit_credential_approval=true` 时，**每一次** 静默凭证访问都必须显式授权：

- **Python API**: 在 `db.connect()` 前调用 `db.explicit_credential_approval(approved=True)`
- **CLI**: 每次调用传 `--approve` 参数

该 flag 仅本次调用有效——不进配置、不继承。每次敏感操作都会在 shell history 留痕。

### English

### Credential Security

| Field in `config.yaml`              | Resolution                                            | Security           |
| ----------------------------------- | ----------------------------------------------------- | ------------------ |
| `password`                          | Direct plaintext in config                            | ⚠️ Not recommended |
| `password_env` + `dbpw_key` (cloud) | OS env variable, decrypted with 6-char key from cloud | ✅ Recommended      |
| `password_dpapi`                    | Windows DPAPI decryption                              | Windows only       |

Password is encrypted with `dbpw_key` (6-char key, HMAC-SHA256) before storing in OS environment variable. The `dbpw_key` is fetched automatically from cloud via your API Key — **never store it locally**.

### Cloud-Managed dbpw\_key

When `cloud_api_key` is configured, `dbpw_key` is fetched from `https://sqllinker.agentpower.hk.cn/api/user/api-keys/by-key` (requires network).

### Cloud Audit

Write operations (INSERT/UPDATE/DELETE) are auto-synced to `https://sqllinker.agentpower.hk.cn/api/audit/logs` via API Key.

### Credential Approval Gate

When `audit.require_explicit_credential_approval=true`, **every** silent-credential operation must be explicitly approved:

- **Python API**: call `db.explicit_credential_approval(approved=True)` before `db.connect()`
- **CLI**: pass `--approve` flag on each invocation

This flag is per-invocation only — it is NOT stored in config and NOT inherited. This leaves an audit trail in shell history for every sensitive operation.

***

# SQL-Linker CLI

### 中文

跨数据库 CRUD + 云端审计。支持 **MySQL、PostgreSQL、SQLite**。所有写操作同步到 `https://sqllinker.agentpower.hk.cn`。

## 快速开始

### 1. 获取 API Key

见本文档顶部的 [API Key 获取官网](#-api-key-获取官网)。

### 2. 初始化配置

```bash
cd scripts/service_layer
python main.py bootstrap
```

生成以下文件：

- `.sql_linker/config_home/config.yaml` — 数据库连接配置
- `.sql_menu/config_home/audit_config.json` — 审计 + 云端配置（URL 已预填）
- `.sql_linker/config_home/extra_tables.json` — 特权表
- `.sql_linker/table_home/table_dictionary.json` — 主字典
- `.sql_linker/set_env.ps1` / `set_env.sh` — 密码设置脚本

初始化后编辑 `.sql_linker/config_home/audit_config.json`，把 `slk_your_api_key_here` 替换成真实 API Key。

### 3. 设置密码

**Windows:**

```powershell
cd .sql_linker
.\set_env.ps1
# 输入密码（不回显）
```

**Linux/macOS:**

```bash
cd .sql_linker
bash set_env.sh
```

### 4. 验证

```bash
# 验证 API Key 有效性（无需连库）
python main.py apikey status

# 列出表（需要连库）
python main.py tables

# 查看连接配置
python main.py config
```

### 5. 使用 CLI

```bash
# 查询
python main.py query "SELECT * FROM users WHERE status = %s" --params '["active"]'

# 插入（闸门开启时需传 --approve）
python main.py insert users --data '{"name": "test", "email": "test@example.com"}' --approve

# 更新
python main.py update users --data '{"status": "active"}' --where "id = 1" --approve

# 删除
python main.py delete users --where "id = 1" --approve

# 从 JSON 文件（避免 shell 转义）
python main.py insert users --file data.json --approve
```

### English

Cross-database CRUD with cloud audit. Supports **MySQL, PostgreSQL, SQLite**. All write operations sync to `https://sqllinker.agentpower.hk.cn`.

## Quick Start

### 1. Get API Key

See [API Key Official Portal](#-api-key-获取官网) at the top of this document.

### 2. Bootstrap Configuration

```bash
cd scripts/service_layer
python main.py bootstrap
```

Creates:

- `.sql_linker/config_home/config.yaml` — DB connection config
- `.sql_linker/config_home/audit_config.json` — Audit + cloud config (URL pre-filled)
- `.sql_linker/config_home/extra_tables.json` — Privileged tables
- `.sql_linker/table_home/table_dictionary.json` — Main dictionary
- `.sql_linker/set_env.ps1` / `set_env.sh` — Password setup scripts

After bootstrap, edit `.sql_linker/config_home/audit_config.json` and replace `slk_your_api_key_here` with your real API key.

### 3. Set Password

**Windows:**

```powershell
cd .sql_linker
.\set_env.ps1
# Enter password (no echo)
```

**Linux/macOS:**

```bash
cd .sql_linker
bash set_env.sh
```

### 4. Verify Setup

```bash
# Check API key is valid (no DB connection needed)
python main.py apikey status

# List tables (uses DB connection)
python main.py tables

# Inspect connection
python main.py config
```

### 5. Use CLI

```bash
# Query
python main.py query "SELECT * FROM users WHERE status = %s" --params '["active"]'

# Insert (audit-gated; pass --approve when gate enabled)
python main.py insert users --data '{"name": "test", "email": "test@example.com"}' --approve

# Update
python main.py update users --data '{"status": "active"}' --where "id = 1" --approve

# Delete
python main.py delete users --where "id = 1" --approve

# From JSON file (avoids shell escaping)
python main.py insert users --file data.json --approve
```

***

## Commands

### 中文

| 命令              | 用途                        | 审计 | 需要 `--approve` |
| --------------- | ------------------------- | -- | -------------- |
| `bootstrap`     | 生成配置文件                    | 否  | 否              |
| `query`         | SELECT 查询                 | 否  | 闸门开启时          |
| `insert`        | INSERT 插入                 | 是  | 闸门开启时          |
| `update`        | UPDATE 更新                 | 是  | 闸门开启时          |
| `delete`        | DELETE 删除                 | 是  | 闸门开启时          |
| `tables`        | 列出表 + 显示字段                | 否  | 闸门开启时          |
| `config`        | 显示本地配置                    | 否  | 否              |
| `apikey status` | 云端 Key introspection（不连库） | 否  | 否              |

### `apikey status` - API Key 状态查询

从云端拉取当前 API Key 的元数据：

```
[API Key Status]
  status     : OK
  agent_name : 客服
  key_name   : test3
  key_id     : 5
  key_masked : slk_rs6p...GvBY
  dbpw_key   : 6 chars (value hidden)
```

- 不连数据库
- 不需要凭证审批（不走静默路径）
- 用于验证 key 有效性、排错审计归属、确认 dbpw\_key 云端同步
- 退出码: 0=OK, 1=未配置, 2=云端不可达, 3=意外错误

### `--approve` 参数

当 `audit_config.json` 中 `require_explicit_credential_approval=true` 时，每个会触库的 CLI 调用都需要显式授权：

```bash
# 不传 --approve：被闸门拦下
python main.py insert users --data '{...}'
# → [ERROR] Silent credential access requires explicit approval.

# 传 --approve：放行
python main.py insert users --data '{...}' --approve
```

**重要约束：**

- `--approve` 仅本次调用有效，不进配置、不进环境变量
- shell history 会留痕——这是审计痕迹
- 不要把 `--approve` 写进 shell alias，会破坏审计痕迹
- `--approve` 不会改变审计内容，只授权凭证访问

### English

| Command         | Purpose                             | Audit | Needs `--approve`     |
| --------------- | ----------------------------------- | ----- | --------------------- |
| `bootstrap`     | Generate config files               | No    | No                    |
| `query`         | SELECT                              | No    | Yes (if gate enabled) |
| `insert`        | INSERT                              | Yes   | Yes (if gate enabled) |
| `update`        | UPDATE                              | Yes   | Yes (if gate enabled) |
| `delete`        | DELETE                              | Yes   | Yes (if gate enabled) |
| `tables`        | List tables + show fields           | No    | Yes (if gate enabled) |
| `config`        | Show local configuration            | No    | No                    |
| `apikey status` | Cloud API key introspection (no DB) | No    | No                    |

### `apikey status`

Shows current API key metadata fetched from `https://sqllinker.agentpower.hk.cn`:

```
[API Key Status]
  status     : OK
  agent_name : 客服
  key_name   : test3
  key_id     : 5
  key_masked : slk_rs6p...GvBY
  dbpw_key   : 6 chars (value hidden)
```

- Does NOT connect to the database
- Does NOT require credential approval (no silent-credential path)
- Useful for verifying key validity, debugging audit attribution, checking dbpw\_key cloud sync
- Exit codes: 0=OK, 1=not configured, 2=cloud unreachable, 3=unexpected error

### `--approve` Flag

When `audit.require_explicit_credential_approval=true` in `audit_config.json`, every CLI invocation that touches the database needs explicit approval:

```bash
# Without --approve — blocked at credential gate
python main.py insert users --data '{...}'
# → [ERROR] Silent credential access requires explicit approval.

# With --approve — proceeds
python main.py insert users --data '{...}' --approve
```

**Important constraints:**

- `--approve` is **per-invocation only**. Not stored in config. Not inherited from environment.
- This leaves a trace in shell history for every sensitive operation.
- Do NOT alias `python main.py` to include `--approve` — that defeats the audit trail.
- `--approve` does NOT change what gets audited; it only authorizes the credential access that triggers the audit.

***

## Four-Layer Access Model

### 中文

| 层级             | 来源                         | SELECT | INSERT | UPDATE | DELETE |
| -------------- | -------------------------- | ------ | ------ | ------ | ------ |
| **SYSTEM**     | sql\_audit\_log 审计日志表      | ✅      | ✅      | ❌      | ❌      |
| **NORMAL**     | table\_dictionary.json 主字典 | ✅      | ✅      | ✅      | ✅      |
| **PRIVILEGED** | extra\_tables.json 特权表     | ✅      | ✅      | ✅      | ✅      |
| **BLOCKED**    | 黑名单                        | ❌      | ❌      | ❌      | ❌      |

### English

| Layer          | Source                  | SELECT | INSERT | UPDATE | DELETE |
| -------------- | ----------------------- | ------ | ------ | ------ | ------ |
| **SYSTEM**     | `sql_audit_log`         | ✅      | ✅      | ❌      | ❌      |
| **NORMAL**     | `table_dictionary.json` | ✅      | ✅      | ✅      | ✅      |
| **PRIVILEGED** | `extra_tables.json`     | ✅      | ✅      | ✅      | ✅      |
| **BLOCKED**    | —                       | ❌      | ❌      | ❌      | ❌      |

***

## Configuration

### 中文

### config\_home/config.yaml

```yaml
type: mysql                      # 数据库类型: mysql/postgres/sqlite
host: 127.0.0.1                  # 主机地址
port: 3306                       # 端口号
database: db_dev                 # 数据库名
user: admin                      # 用户名
password_env: mysql_pw           # OS 环境变量键（存储加密密码）
read_only: false                 # 只读模式（默认安全）
max_rows: 1000                   # 最大返回行数
timeout: 30                       # 连接超时（秒）
extra_tables_enabled: false      # 特权表开关（默认关闭）
```

### config\_home/audit\_config.json

```json
{
  "username": "CLI",                                    // 用户标识名
  "cloud_audit_url": "https://sqllinker.agentpower.hk.cn/api/audit/logs",  // 云端审计地址
  "cloud_api_key": "slk_xxxxxxxxxxxxxxx",               // API 密钥
  "audit": {
    "enabled": true,                                    // 审计开关
    "log_table": "sql_audit_log",                       // 审计日志表名
    "log_select": false,                                // SELECT 是否记录
    "mask_values": true,                                 // 敏感值脱敏
    "collect_lan_ip": false,                            // 收集局域网IP
    "require_explicit_credential_approval": false        // 凭证审批闸门
  }
}
```

新装默认 `cloud_audit_url` 为新域名，老用户配置继续工作。

### table\_home/table\_dictionary.json

表和字段白名单，只能写入声明过的字段。bootstrap 模板见 `scripts/service_layer/main.py`。

### English

### config\_home/config.yaml

```yaml
type: mysql                      # Database type: mysql/postgres/sqlite
host: 127.0.0.1                  # Host address
port: 3306                       # Port number
database: db_dev                 # Database name
user: admin                      # Username
password_env: mysql_pw           # OS env key (stores encrypted password)
read_only: false                 # Read-only mode (safe by default)
max_rows: 1000                   # Maximum rows returned
timeout: 30                       # Connection timeout (seconds)
extra_tables_enabled: false      # Privileged table gate (off by default)
```

### config\_home/audit\_config.json

```json
{
  "username": "CLI",                                    // User identifier
  "cloud_audit_url": "https://sqllinker.agentpower.hk.cn/api/audit/logs",  // Cloud audit endpoint
  "cloud_api_key": "slk_xxxxxxxxxxxxxxx",               // API Key
  "audit": {
    "enabled": true,                                    // Audit enabled
    "log_table": "sql_audit_log",                       // Audit log table name
    "log_select": false,                                // Log SELECT queries
    "mask_values": true,                                // Mask sensitive values
    "collect_lan_ip": false,                            // Collect LAN IP
    "require_explicit_credential_approval": false        // Require credential approval gate
  }
}
```

New installs default to new domain URL. Existing installs continue to work.

### table\_home/table\_dictionary.json

Whitelist of tables and fields. Only declared fields can be written. Bootstrap template in `scripts/service_layer/main.py`.

***

## Python API

### 中文

```python
import sys
sys.path.insert(0, "scripts/service_layer")
from db_bridge import DBBridge

# 方式一：构造时直接传授权
db = DBBridge(user_label="myagent", session_id="main", approved=True)
db.require_cloud_api_key()
db.connect()
rows = db.query("SELECT * FROM users WHERE status = %s", ("active",))

# 方式二：显式调用授权（推荐）
db = DBBridge(user_label="myagent", session_id="main")
db.require_cloud_api_key()
db.explicit_credential_approval(approved=True)  # 闸门开启时必须
db.connect()

# 云端 introspection（无需连库，直接使用 SQLLinker）
import sys
sys.path.insert(0, "scripts/controller_layer")
from sql_linker import SQLLinker
linker = SQLLinker()
info = linker.fetch_api_key_info()  # 返回非敏感元数据: agent_name, key_name, id, key_masked
print(info["agent_name"], info["key_name"])
```

### English

```python
import sys
sys.path.insert(0, "scripts/service_layer")
from db_bridge import DBBridge

# Option 1: Pass approval in constructor
db = DBBridge(user_label="myagent", session_id="main", approved=True)
db.require_cloud_api_key()
db.connect()
rows = db.query("SELECT * FROM users WHERE status = %s", ("active",))

# Option 2: Call explicit approval (recommended)
db = DBBridge(user_label="myagent", session_id="main")
db.require_cloud_api_key()
db.explicit_credential_approval(approved=True)  # Required when gate is enabled
db.connect()

# Cloud introspection (no DB needed, use SQLLinker directly)
import sys
sys.path.insert(0, "scripts/controller_layer")
from sql_linker import SQLLinker
linker = SQLLinker()
info = linker.fetch_api_key_info()  # Returns non-sensitive metadata: agent_name, key_name, id, key_masked
print(info["agent_name"], info["key_name"])
```

***

## Common Errors

### 中文

| 错误                                                       | 原因                                     | 解决方案                                                                       |
| -------------------------------------------------------- | -------------------------------------- | -------------------------------------------------------------------------- |
| `Silent credential access requires explicit approval...` | 闸门开启且未授权                               | 重新传 `--approve` (CLI) 或调用 `db.explicit_credential_approval(True)` (Python) |
| `cloud_api_key is not configured`                        | audit\_config.json 中缺少 cloud\_api\_key | 从官网获取并填入                                                                   |
| `Cloud unreachable: Network error...`                    | 无法连接云端                                 | 检查网络；确认 cloud\_audit\_url 以 /api/audit/logs 结尾                             |
| `Password not found`                                     | OS 环境变量未设置                             | 运行 set\_env.ps1 / set\_env.sh                                              |
| `HMAC verification failed`                               | 密钥错误或环境变量损坏                            | 重新连接拉取密钥；用 apikey status 检查 Key 有效性                                        |
| `TableAccessDenied`                                      | 表不在字典中                                 | 加入 extra\_tables.json（enabled:true）或 table\_dictionary.json                |
| `SystemTableWriteDenied`                                 | 试图修改审计日志表                              | 正常保护，不要直接修改 sql\_audit\_log                                                |

### English

| Error                                                    | Cause                       | Solution                                                                               |
| -------------------------------------------------------- | --------------------------- | -------------------------------------------------------------------------------------- |
| `Silent credential access requires explicit approval...` | Gate enabled, no approval   | Re-run with `--approve` (CLI) or call `db.explicit_credential_approval(True)` (Python) |
| `cloud_api_key is not configured`                        | Missing in config           | Get from portal and fill in                                                            |
| `Cloud unreachable: Network error...`                    | Cannot reach cloud          | Check network; verify URL ends with `/api/audit/logs`                                  |
| `Password not found`                                     | Env variable not set        | Run `set_env.ps1` / `set_env.sh`                                                       |
| `HMAC verification failed`                               | Wrong key or corrupted env  | Re-connect to fetch key; check with `apikey status`                                    |
| `TableAccessDenied`                                      | Table not in dictionary     | Add to `extra_tables.json` (enabled:true) or `table_dictionary.json`                   |
| `SystemTableWriteDenied`                                 | Attempt to modify audit log | Normal protection                                                                      |

***

## Directory Structure

### 中文

```
sql-linker-cli/                        # 技能根目录
├── SKILL.md                           # 本文档
├── _meta.json                         # 元数据（版本、发布信息）
├── scripts/
│   ├── controller_layer/              # 数据操作层
│   │   ├── sql_linker.py             # 连接 + CRUD + 云端审计 + 密钥获取
│   │   └── sql_audit.py              # 审计模块
│   └── service_layer/                # 业务层
│       ├── db_bridge.py              # 访问控制 + 时间戳
│       └── main.py                   # CLI 入口点

workspace/
└── .sql_linker/                      # 配置根目录（bootstrap 创建）
    ├── config_home/
    │   ├── config.yaml                # 数据库连接配置
    │   ├── audit_config.json          # 审计 + 云端配置
    │   └── extra_tables.json          # 特权表
    ├── table_home/
    │   └── table_dictionary.json     # 主字典
    ├── set_env.ps1                   # 密码设置脚本（Windows）
    └── set_env.sh                    # 密码设置脚本（Linux/macOS）
```

### English

```
sql-linker-cli/                        # Skill root directory
├── SKILL.md                           # This document
├── _meta.json                         # Metadata (version, publish info)
├── scripts/
│   ├── controller_layer/              # Data operation layer
│   │   ├── sql_linker.py             # Connection + CRUD + cloud audit + key fetch
│   │   └── sql_audit.py             # Audit module
│   └── service_layer/                # Business layer
│       ├── db_bridge.py              # Access control + timestamp
│       └── main.py                   # CLI entry point

workspace/
└── .sql_linker/                      # Config root (created by bootstrap)
    ├── config_home/
    │   ├── config.yaml               # DB connection config
    │   ├── audit_config.json         # Audit + cloud config
    │   └── extra_tables.json         # Privileged tables
    ├── table_home/
    │   └── table_dictionary.json    # Main dictionary
    ├── set_env.ps1                  # Password setup (Windows)
    └── set_env.sh                   # Password setup (Linux/macOS)
```

