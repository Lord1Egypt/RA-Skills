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

## sql-linker vs sql-linker-cli

### 中文

**sql-linker** 适用于本地开发和快速原型。对于**生产环境**，强烈推荐使用 **sql-linker-cli**。

| 对比项 | sql-linker | sql-linker-cli |
|-------|-----------|----------------|
| **dbpw_key 存储** | 本地存储在 `config.yaml` 中 | **云端管理**，通过 API Key 自动拉取 |
| **凭证密钥隔离** | 本地存储，OpenClaw 可能读取 | **本地与云端隔离**，密钥不在本地 |
| **凭证审批闸门** | 可选配置 | 默认开启，敏感操作需显式授权 |
| **使用场景** | 本地开发、快速原型 | **生产环境推荐**，安全优先 |
| **API Key 管理** | 无 | 云端统一管理，支持 Key 轮换 |
| **审计同步** | 本地 | 云端统一审计 |

**sql-linker 的局限性：**
- `dbpw_key` 存储在本地 `config.yaml`，OpenClaw agent 可能读取配置文件获取密钥
- 凭证审批闸门需要手动配置开启
- 审计日志存储在本地数据库

**生产环境推荐：**
- 迁移到 [sql-linker-cli](https://clawhub.ai/cloudcode-hans/skills/sql-linker-cli)，享受云端密钥管理和统一审计

### English

**sql-linker** is suitable for local development and quick prototypes. For **production environments**, **sql-linker-cli** is strongly recommended.

| Feature | sql-linker | sql-linker-cli |
|---------|-----------|----------------|
| **dbpw_key storage** | Stored locally in `config.yaml` | **Cloud-managed**, auto-fetched via API Key |
| **Credential isolation** | Local storage, OpenClaw may access | **Local-cloud isolated**, key not on disk |
| **Credential approval gate** | Optional config | Enabled by default, explicit approval required |
| **Use case** | Local dev, quick prototypes | **Production recommended**, security-first |
| **API Key management** | None | Cloud unified management, supports rotation |
| **Audit sync** | Local | Cloud unified audit |

**sql-linker limitations:**
- `dbpw_key` stored locally in `config.yaml`, OpenClaw agent may read config to obtain key
- Credential approval gate requires manual configuration to enable
- Audit logs stored in local database

**Production recommendation:**
- Migrate to [sql-linker-cli](https://clawhub.ai/cloudcode-hans/skills/sql-linker-cli) for cloud key management and unified audit

***

## Security & Privacy Notice

### 中文

> **（必读）使用本 skill 前请仔细阅读本声明。** / Please read this notice before using this skill.

### 凭据访问声明

**密码解析优先级（按顺序）：**

| config.yaml 字段 | 解析方式 | 风险等级 |
| -------------------- | ----------------------------------------------------------------- | ------------------------------------------------- |
| `password` | 直接明文存储在配置中 | ⚠️ 不推荐；密钥直接暴露在配置文件中 |
| `password_env` | 读取 OS 环境变量，**使用 `dbpw_key` 解密** | 低——需要加密密码 + 密钥才能解密 |
| `dbpw_key` | 6 位密码加密密钥，用于混合加密 | **`password_env` 解密必需** |
| `password_dpapi` | 使用当前 Windows 用户凭据 DPAPI 解密 base64 值 | 中——运行时可恢复存储的密钥 |

**安全（混合加密）：**

- 密码使用 `dbpw_key` 加密后再存入 OS 环境变量
- **需要同时拥有**加密密码（在环境变量中）和 `dbpw_key`（在 config.yaml 中）才能解密
- ⚠️ **信任边界说明**：`dbpw_key` 存储在 `config.yaml` 中，与加密密码在同一信任边界。如果 OpenClaw agent 能同时访问配置文件和环境变量，则可能组合解密获取数据库密码
- 生产环境推荐使用 sql-linker-cli（`dbpw_key` 云端管理，本地与云端隔离）

**显示保护**：输入密码时，终端不回显。输出只显示长度和头尾预览（如 `test123` 显示为 `te**23`）。

⚠️ **重要**：请妥善保管 `dbpw_key`！如果丢失，密码将无法恢复。

**可选加固——`require_explicit_credential_approval`**：要强制在静默凭证加载前进行显式确认，请在 `audit_config.json` 中设置 `require_explicit_credential_approval: true`。启用后，首次使用 `password_env`/`password_dpapi` 的连接尝试将抛出 `PermissionError`，直到在代码中调用 `db.explicit_credential_approval()`。

### 连接初始化声明

创建 `SQLLinker` 或 `DBBridge` 实例**不会**自动连接数据库。连接延迟到首次实际数据库调用时才建立（首次查询时懒加载调用 `connect()`）。这避免了过早的基础设施访问。

### 审计数据收集声明

**数据最小化**：审计记录仅收集合规追溯所需的最小身份字段：`user_name`、`user_label`、`session_id` 和可选的 `ip_address`（默认关闭）。SQL 文本在记录前会被脱敏处理。不会故意收集密码、个人身份号码或业务敏感字段。

**保留期**：审计记录存储在目标数据库的 `sql_audit_log` 中。保留策略由您组织的数据库保留计划决定，不由本 skill 决定。

**退出**：在 `audit_config.json` 中设置 `audit: enabled: false` 可禁用应用层审计日志记录。数据库层触发器（如果有）与此设置无关。

**同意**：使用本 skill 即表示您同意将数据库操作元数据（操作人身份、表名、脱敏 SQL、行数、时间戳、状态）记录到 `sql_audit_log`。请勿在 SQL 查询参数中包含敏感个人数据（如身份证号、密码、医疗信息）——这些值虽然会被脱敏，但仍然会持久化到日志记录中。

### English

> **Please read this notice before using this skill.** / （必读）使用本 skill 前请仔细阅读本声明。

### Credential Access Notice

**How credentials are resolved (in order of precedence):**

| Field in config.yaml | Resolution | Risk Level |
| -------------------- | ----------------------------------------------------------------- | ------------------------------------------------- |
| `password` | Direct plaintext in config | ⚠️ Not recommended; commits secret to config file |
| `password_env` | Reads OS environment variable, **decrypted with** **`dbpw_key`** | Low — encrypted password + key required |
| `dbpw_key` | 6-char encryption key for hybrid password encryption | **Required** for `password_env` decryption |
| `password_dpapi` | DPAPI-decrypts base64 value using current Windows user credential | Moderate — can recover stored secret at runtime |

**Security (Hybrid Encryption):**

- Password is encrypted with `dbpw_key` before storing in OS env
- **Both** the encrypted password (in env) **and** `dbpw_key` (in config.yaml) are needed to decrypt
- ⚠️ **Trust boundary note**: `dbpw_key` is stored in `config.yaml`, in the same trust boundary as the encrypted password. If OpenClaw agent can access both config files and environment variables, it may decrypt the database password
- For production, use sql-linker-cli (`dbpw_key` cloud-managed, local-cloud isolated)

**Display Protection**: When entering password, terminal shows no echo. Output only shows length and head+tail preview (e.g., `te**23` for `test123`).

⚠️ **IMPORTANT**: Keep `dbpw_key` secret! If lost, password cannot be recovered.

**Optional Hardening —** **`require_explicit_credential_approval`**: To force explicit confirmation before silent credential loading, set `require_explicit_credential_approval: true` in `audit_config.json`. When enabled, the first connection attempt with `password_env`/`password_dpapi` will raise `PermissionError` until you call `db.explicit_credential_approval()` in your code.

### Connection-on-Init Notice

Creating a `SQLLinker` or `DBBridge` instance does **not** automatically connect. Connection is deferred until the first actual database call (`connect()` is called lazily on first query). This avoids premature infrastructure access.

### Audit Data Collection Notice

**Data Minimization**: Audit records collect the minimum identity fields required for compliance traceability: `user_name`, `user_label`, `session_id`, and optionally `ip_address` (disabled by default). SQL text is masked before logging. No passwords, personal identity numbers, or business-sensitive fields are intentionally captured.

**Retention**: Audit records are stored in `sql_audit_log` in the target database. Retention policy is determined by your organization's database retention schedule, not by this skill.

**Opt-Out**: Set `audit: enabled: false` in `audit_config.json` to disable application-layer audit logging. Database-layer triggers (if any) are independent of this setting.

**Consent**: By using this skill, you consent to having database operation metadata (operator identity, table name, masked SQL, row counts, timestamp, status) recorded in `sql_audit_log`. Do not include sensitive personal data (e.g., national ID numbers, passwords, medical info) in SQL query parameters — such values will be masked but still persisted in log records.

***

## 审计数据收集

### 中文

**审计日志**：每次数据库操作都会将以下字段记录到 `sql_audit_log`：

| 字段 | 描述 | 来源 |
| --------------- | ------------------ | ------------------------------------------------------------- |
| `user_name` | 操作人名称 | 显式参数或 `audit_config.json` 用户名 |
| `user_label` | 来源标签 | 显式参数或 `OPENCLAW_LABEL` 环境变量 |
| `ip_address` | 客户端 IP | 显式参数或局域网 IP（仅在 `collect_lan_ip: true` 时） |
| `session_id` | 会话标识符 | 显式参数或 `OPENCLAW_SESSION` 环境变量 |
| `sql_statement` | 完整 SQL 语句 | 参数化并脱敏（字面量替换为 `?`） |
| `rows_affected` | 影响行数 | 数据库返回值 |
| `status` | 操作状态 | SUCCESS / FAILED |

⚡ **隐私声明**：SQL 文本在记录前会被脱敏——字符串和数字字面量替换为 `?`。不会故意存储密码或原始 PII。但是日志表本身包含身份元数据，请将其视为敏感数据处理。避免在查询参数中包含敏感个人数据。

### 自动数据发现（可关闭）

默认情况下，本 skill 从以下来源自动收集审计上下文：

| 来源 | 收集的数据 | 禁用方式 |
| ---------------------- | -------------- | ------------------------------------------------------------------- |
| `OPENCLAW_USER` 环境变量 | 用户名 | 显式传递 `user_name` 参数 |
| `OPENCLAW_LABEL` 环境变量 | 来源标签 | 显式传递 `user_label` 参数 |
| `OPENCLAW_SESSION` 环境变量 | 会话 ID | 显式传递 `session_id` 参数 |
| 局域网 IP 自动检测 | 本地局域网 IP | 在 `audit_config.json` 中设置 `collect_lan_ip: false`（默认 false） |

如果不想自动收集，**请显式传递** `user_label` 和 `session_id` 参数——本 skill 将优先使用传入值而非自动发现。

### English

**Audit Log**: Every database operation records the following fields to `sql_audit_log`:

| Field | Description | Source |
| --------------- | ------------------ | ------------------------------------------------------------- |
| `user_name` | Operator name | Explicit parameter or `audit_config.json` username |
| `user_label` | Source label | Explicit parameter or `OPENCLAW_LABEL` env |
| `ip_address` | Client IP | Explicit parameter or LAN IP (only if `collect_lan_ip: true`) |
| `session_id` | Session identifier | Explicit parameter or `OPENCLAW_SESSION` env |
| `sql_statement` | Full SQL statement | Parameterized and masked (literals replaced with `?`) |
| `rows_affected` | Rows affected | Database return |
| `status` | Operation status | SUCCESS / FAILED |

⚡ **Privacy Notice**: SQL text is masked before logging — string and numeric literals are replaced with `?`. No password or raw PII is intentionally stored. However, the log table itself contains identity metadata; treat it as sensitive. Avoid including sensitive personal data in query parameters.

### Automatic Data Discovery (Can Be Disabled)

By default, this skill auto-collects audit context from the following sources:

| Source | Collected Data | How to Disable |
| ---------------------- | -------------- | ------------------------------------------------------------------- |
| `OPENCLAW_USER` env | Username | Explicitly pass `user_name` parameter |
| `OPENCLAW_LABEL` env | Source label | Explicitly pass `user_label` parameter |
| `OPENCLAW_SESSION` env | Session ID | Explicitly pass `session_id` parameter |
| LAN IP auto-detection | Local LAN IP | Set `collect_lan_ip: false` in `audit_config.json` (default: false) |

If you do not want auto-collection, **explicitly pass** `user_label` and `session_id` parameters — this skill will prefer passed values over auto-discovery.

***

## 配置文件自动创建

### 中文

首次使用或缺少配置文件时，本 skill 会在 `~/.sql_linker/` 下自动创建文件：

| 文件 | 描述 |
| ---------------------------------- | ------------------------------------------------------ |
| `config_home/config.yaml` | 数据库连接配置 |
| `config_home/audit_config.json` | 审计配置 |
| `config_home/extra_tables.json` | 特权表配置 |
| `table_home/table_dictionary.json` | 主词典 |
| `set_env.ps1` | Windows 密码设置脚本（自动生成） |
| `set_env.sh` | Linux/macOS 密码设置脚本（自动生成） |

**密码设置**：在 `.sql_linker/` 文件夹中运行 `set_env.ps1`（Windows）或 `set_env.sh`（Linux/macOS）来加密并保存数据库密码。密码使用 `dbpw_key` 加密后再存入 OS 环境变量。

⚠️ **Linux/macOS 安全警告**：`set_env.sh` 会修改 `~/.bashrc` 或 `~/.zshrc` 文件以持久化环境变量。在运行前请检查脚本内容，确保了解所做的更改。

如需完全手动控制，请在调用 skill 前创建这些文件。`bootstrap()` 是幂等操作，但在创建文件前会打印安全警告。

### English

On first use or when config files are missing, this skill auto-creates files under `~/.sql_linker/`:

| File | Description |
| ---------------------------------- | ------------------------------------------------------ |
| `config_home/config.yaml` | Database connection config |
| `config_home/audit_config.json` | Audit configuration |
| `config_home/extra_tables.json` | Privileged table config |
| `table_home/table_dictionary.json` | Main dictionary |
| `set_env.ps1` | Password setup script for Windows (auto-generated) |
| `set_env.sh` | Password setup script for Linux/macOS (auto-generated) |

**Password Setup**: Run `set_env.ps1` (Windows) or `set_env.sh` (Linux/macOS) in `.sql_linker/` folder to encrypt and save the database password. Password is encrypted with `dbpw_key` before storing in OS env.

⚠️ **Linux/macOS Security Warning**: `set_env.sh` will modify `~/.bashrc` or `~/.zshrc` to persist the environment variable. Review the script content before running to understand the changes.

For full manual control, create these files before invoking the skill. `bootstrap()` is idempotent but prints a safety warning before creating files.

***

## 密码来源优先级

### 中文

`password` > `password_env` + `dbpw_key` > `password_dpapi`

- **`password`**：直接明文（不推荐）
- **`password_env`**：OS 环境变量存储加密密码（需要 `dbpw_key` 解密）
- **`dbpw_key`**：6 位加密密钥（bootstrap 自动生成，**请妥善保管**）
- **`password_dpapi`**：Windows DPAPI 解密（仅 Windows，用户级）

**设置密码（Windows）：**

```powershell
# 1. 确保 config.yaml 中有 dbpw_key
# 2. 运行 set_env.ps1 加密并保存密码
cd .sql_linker
.\set_env.ps1
# 输入密码（终端不回显）
# 输出显示：长度 + 头尾预览（如 "Wo**88"）
```

**首次设置（bootstrap 后）：**

1. 运行 `bootstrap(dry_run=False, explicit_confirm=True)`
2. **保存显示的 `dbpw_key`**（如 `Kx****`）
3. 运行 `set_env.ps1` 设置加密密码
4. **记住 dbpw_key**——没有它，密码无法恢复！

### English

`password` > `password_env` + `dbpw_key` > `password_dpapi`

- **`password`**: Direct plaintext (not recommended)
- **`password_env`**: OS environment variable with encrypted password (requires `dbpw_key` to decrypt)
- **`dbpw_key`**: 6-char encryption key (auto-generated by bootstrap, **keep secret**)
- **`password_dpapi`**: Windows DPAPI decryption (Windows only, user-scoped)

**Setting the password (Windows):**

```powershell
# 1. Ensure config.yaml has dbpw_key
# 2. Run set_env.ps1 to encrypt and save password
cd .sql_linker
.\set_env.ps1
# Enter password (no echo in terminal)
# Output shows: length + head+tail preview (e.g., "Wo**88")
```

**First-time setup (after bootstrap):**

1. Run `bootstrap(dry_run=False, explicit_confirm=True)`
2. **SAVE the** **`dbpw_key`** shown in output (e.g., `Kx****`)
3. Run `set_env.ps1` to set encrypted password
4. **REMEMBER the dbpw_key** — without it, password cannot be recovered!

***

## 破坏性操作确认

### 中文

`UPDATE` / `DELETE` 操作直接执行，无法回滚。在生产环境中，启用只读模式（`read_only: true`）进行预验证。

### English

`UPDATE` / `DELETE` operations execute directly and cannot be rolled back. In production, enable read-only mode (`read_only: true`) for pre-validation.

***

## Legacy Users Notice

### 中文

### 版本 1.2.3 → 1.3.0 变更

- **`dbpw_key`** **新增**：密码加密现在需要 `dbpw_key`（6 位密钥）进行混合加密
- `password_env` 存储加密密码，使用 config.yaml 中的 `dbpw_key` 解密
- 解密需要加密密码（在环境变量中）和 `dbpw_key`（在 config.yaml 中）两者
- OpenClaw agent 不知道 `dbpw_key` 则无法访问密码
- `set_env.ps1` 在保存到 OS 环境变量前加密密码
- 输出只显示密码长度和头尾预览（如 `Wo**88`）
- `dbpw_key` 由 bootstrap 自动生成，**请妥善保管**
- `.env` 文件不再由 bootstrap 创建或使用

### 版本 1.2.2 → 1.2.3 变更

- `bootstrap(dry_run=False)` 现在需要 `explicit_confirm=True` 才能写入文件——否则抛出 `BootstrapConfirmationRequired` 异常。这防止了意外配置持久化到共享工作区（ClawHub 安全审计发现 #1，置信度 62%）
- 新增异常 `BootstrapConfirmationRequired`，在尝试无显式确认的 bootstrap 写入时抛出
- `DBBridge.bootstrap()` 转发新的 `explicit_confirm` 参数

### 版本 1.1.1 → 1.2.0 变更

- 收紧触发词：移除 "whenever" + 模糊的 "CRUD tasks" / "data manipulation" 开放触发词；现在需要特定命名表或明确意图
- 新增凭据访问声明：记录 `password_env` / `password_dpapi` 自动解析和静默加载无提示特性
- 新增连接初始化声明：澄清 `SQLLinker`/`DBBridge` 实例化不会自动连接
- 新增审计数据最小化 & 同意声明：记录捕获内容/未捕获内容、退出路径和隐私期望
- 可通过 `log_select: false` 禁用 SELECT 审计日志记录（默认 false）——SELECT 日志记录仅在 `audit: enabled: true` **和** `log_select: true` 同时满足时发生
- `collect_lan_ip` 默认为 false（之前未显式默认值）
- `session_id` / `user_label` 优先使用显式传入值；不再从 sessions.json 自动读取

### English

### Version 1.2.3 → 1.3.0 Changes

- **`dbpw_key`** **added**: Password encryption now requires `dbpw_key` (6-char key) for hybrid encryption
- `password_env` stores encrypted password, decrypted using `dbpw_key` from config.yaml
- Both encrypted password (in env) AND `dbpw_key` (in config.yaml) are required to decrypt
- OpenClaw agent cannot access password without knowing `dbpw_key`
- `set_env.ps1` encrypts password before saving to OS env
- Output shows only password length and head+tail preview (e.g., `Wo**88`)
- `dbpw_key` auto-generated by bootstrap, **must be kept secret**
- `.env` file no longer created by bootstrap or used

### Version 1.2.2 → 1.2.3 Changes

- `bootstrap(dry_run=False)` now requires `explicit_confirm=True` to write files — a `BootstrapConfirmationRequired` exception is raised otherwise. This prevents accidental configuration persistence in shared workspaces (Finding #1 of the ClawHub security audit, 62% confidence)
- New exception `BootstrapConfirmationRequired` raised when bootstrap write is attempted without explicit confirmation
- `DBBridge.bootstrap()` forwards the new `explicit_confirm` parameter

### Version 1.1.1 → 1.2.0 Changes

- Tightened trigger language: removed "whenever" + vague "CRUD tasks" / "data manipulation" open-ended triggers; now requires specific named table or explicit intent
- Added Credential Access Notice: documents `password_env` / `password_dpapi` auto-resolution and the no-prompt nature of credential loading
- Added Connection-on-Init Notice: clarifies that `SQLLinker`/`DBBridge` instantiation does NOT auto-connect
- Added Audit Data Minimization & Consent Notice: documents what is/isn't captured, opt-out path, and privacy expectations
- Audit log SELECT can be disabled via `log_select: false` (default false) — SELECT logging only occurs when BOTH `audit: enabled: true` AND `log_select: true`
- `collect_lan_ip` defaults to false (was not explicitly defaulted before)
- `session_id` / `user_label` prefer explicitly passed values; no longer auto-read from `sessions.json`

***

# SQL-Linker — 双层架构：数据操作层 + 业务层

### 中文

SQL-Linker 提供跨数据库的 CRUD 操作能力，支持 **MySQL、PostgreSQL、SQLite** 三种主流数据库。内置**审计日志**模块，每次操作自动记录操作人身份、IP、SQL 语句、操作时间，确保数据可溯源、安全可控。业务层（db_bridge）负责字段白名单过滤和时间戳自动注入，数据操作层（sql_linker）负责连接管理、CRUD 执行和审计记录，两层严格分离，互不干扰。

### English

SQL-Linker provides cross-database CRUD operations, supporting **MySQL, PostgreSQL, and SQLite**, with a built-in **audit trail** module that automatically records operator identity, IP, SQL statements, and timestamps for full traceability and compliance. The business layer (db_bridge) handles field whitelist filtering and automatic timestamp injection, while the data operation layer (sql_linker) manages database connections, CRUD execution, and audit logging. The two layers are strictly separated and independent.

***

## 核心架构

### 中文

系统由两层组成，业务层和数据操作层职责分明：

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
│   ├── sql_linker.py                    ← Connection management + CRUD execution + audit context injection
│   └── sql_audit.py                      ← Audit module (used internally by sql_linker.py)
└── service_layer/                        ← Business layer
    └── db_bridge.py                     ← Four-layer access control + timestamp injection + field whitelist
```

**业务层（service_layer）**：读取 table_dictionary.json，过滤字段，注入时间戳，校验访问权限，调用数据操作层，不直接操作数据库。

**数据操作层（controller_layer）**：管理数据库连接，执行 CRUD 操作，写入审计日志，处理参数化查询，不处理业务逻辑。

### English

The system consists of two layers with clearly defined responsibilities:

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
│   ├── sql_linker.py                    ← Connection management + CRUD execution + audit context injection
│   └── sql_audit.py                      ← Audit module (used internally by sql_linker.py)
└── service_layer/                        ← Business layer
    └── db_bridge.py                     ← Four-layer access control + timestamp injection + field whitelist
```

**Business Layer (service_layer)**: Reads table_dictionary.json, filters fields, injects timestamps, verifies access rights, and calls the data operation layer. Does not directly access the database.

**Data Operation Layer (controller_layer)**: Manages database connections, executes CRUD operations, writes audit logs, handles parameterized queries. Does not process business logic.

***

## 四层访问模型

### 中文

系统通过四层访问模型实现精确的表访问控制：

**SYSTEM（系统表 sql_audit_log）**

- 硬编码：db_bridge.py SYSTEM_TABLES
- SELECT/INSERT：允许
- UPDATE/DELETE：拒绝（SystemTableWriteDenied）
- 字段白名单：不适用
- 时间戳注入：不适用
- 审计：原生游标绕过 db_bridge
- ⚠️ **重要**：审计日志是普通数据库表，**不是防篡改的**。它不提供加密链、签名或追加强制执行。如需防篡改要求，请实现额外的数据库层控制（如触发器、不可变审计表）。

**NORMAL（主词典表格）**

- 文件：table_dictionary.json
- 字段白名单：是（仅 table.json 中的字段）
- 时间戳注入：是（created_at/updated_at 自动生成）
- 审计：完整
- 无需额外配置即可使用

**PRIVILEGED（特权表格）**

- 文件：extra_tables.json（表列表）+ config.yaml extra_tables_enabled（全局开关）
- 字段白名单：否（未知架构，直接暴露数据库）
- 时间戳注入：否
- 审计：完整
- 双层门控：(1) 表必须在 extra_tables.json 中列出；(2) config.yaml 中 extra_tables_enabled 必须为 true（两者都需要）

**BLOCKED（禁用）**

- 不在词典也不在 extra_tables 中
- 所有操作被拒绝，拒绝被记录
-除非添加到 extra_tables.json，否则无法访问

**访问判定流程**：提取 SQL 中的表名 → 检查 SYSTEM → 检查主词典（NORMAL）→ 检查 extra_tables（PRIVILEGED）→ 其余 BLOCKED。

### English

The system implements precise table access control through a four-layer access model:

**SYSTEM (系统表 sql_audit_log)**

- Hard-coded: db_bridge.py SYSTEM_TABLES
- SELECT/INSERT: ALLOW
- UPDATE/DELETE: DENY (SystemTableWriteDenied)
- Field whitelist: N/A
- Timestamp injection: N/A
- Audit: Native cursor bypasses db_bridge
- ⚠️ **Important**: Audit log is a regular database table, NOT tamper-evident. It does NOT provide cryptographic chaining, signatures, or append-only enforcement. For tamper-evident requirements, implement additional database-layer controls (e.g., triggers, immutable audit tables).

**NORMAL (主词典表格)**

- File: table_dictionary.json
- Field whitelist: YES (only fields in table.json)
- Timestamp injection: YES (created_at/updated_at auto-generated)
- Audit: Full
- Ready to use without extra config

**PRIVILEGED (特权表格)**

- File: extra_tables.json (table list) + config.yaml extra_tables_enabled (global on/off switch)
- Field whitelist: NO (unknown schema, direct DB exposure)
- Timestamp injection: NO
- Audit: Full
  - Two-layer gate: (1) table must be listed in extra_tables.json; (2) config.yaml extra_tables_enabled must be true (both required)

**BLOCKED (禁用)**

- Not in dictionary nor extra_tables
- All operations denied, denial logged
- Cannot access unless added to extra_tables.json

**Access Decision Flow**: Extract table name from SQL → Check SYSTEM → Check main dictionary (NORMAL) → Check extra_tables (PRIVILEGED) → Rest BLOCKED.

***

## 引导初始化

### 中文

首次使用或缺少配置文件时，系统自动生成默认模板（幂等操作，不会覆盖已有文件）：

> ⚠️ **Bootstrap 自动创建配置**：首次使用时会自动在 `~/.sql_linker/` 目录下创建配置文件（`config.yaml`、`audit_config.json` 等）。密码请使用 `set_env.ps1` 设置到 Windows 环境变量。`bootstrap()` 为幂等操作，不会覆盖已有文件，但会创建缺失的文件。

```python
from db_bridge import DBBridge

db = DBBridge(user_label="openclaw-control-ui", session_id="agent:hr:main")

# Preview files to be created (no actual write)
preview = db.bootstrap(dry_run=True)
print(f'Will create: {preview}')

# Execute actual bootstrap (REQUIRES explicit_confirm=True to write)
created = db.bootstrap(explicit_confirm=True)
print(f'Created: {created}')
# ['...\\config.yaml', '...\\audit_config.json', ...]
```

**自动生成的文件列表**：

| 文件路径 | 默认内容 |
| ---------------------------------------------- | ---------------------------------------------------------------------------------- |
| `.sql_linker/config_home/config.yaml` | 连接模板（host/port/user 占位符，password_env 引用 OS 环境变量） |
| `.sql_linker/config_home/audit_config.json` | 审计默认开启，log_select=false，collect_lan_ip=false |
| `.sql_linker/config_home/extra_tables.json` | 特权表，默认关闭，max_extra_tables=10 |
| `.sql_linker/table_home/table_dictionary.json` | 带示例表的空模板 |
| `.sql_linker/set_env.ps1` | Windows 密码设置脚本（运行以设置 OS 环境变量中的密码） |
| `.sql_linker/set_env.sh` | Linux/macOS 密码设置脚本（运行以设置 OS 环境变量中的密码） |

### English

On first use or when config files are missing, the system automatically generates default templates (idempotent, will not overwrite existing files):

> ⚠️ **Bootstrap auto-creates config**: On first use, config files (`config.yaml`, `audit_config.json`, etc.) are auto-created in `~/.sql_linker/`. Use `set_env.ps1` to set password to Windows env. `bootstrap()` is idempotent and won't overwrite existing files, but will create missing ones.

```python
from db_bridge import DBBridge

db = DBBridge(user_label="openclaw-control-ui", session_id="agent:hr:main")

# Preview files to be created (no actual write)
preview = db.bootstrap(dry_run=True)
print(f'Will create: {preview}')

# Execute actual bootstrap (REQUIRES explicit_confirm=True to write)
created = db.bootstrap(explicit_confirm=True)
print(f'Created: {created}')
# ['...\\config.yaml', '...\\audit_config.json', ...]
```

**Auto-generated files**:

| File Path | Default Content |
| ---------------------------------------------- | ---------------------------------------------------------------------------------- |
| `.sql_linker/config_home/config.yaml` | Connection template (host/port/user placeholders, password_env references OS env) |
| `.sql_linker/config_home/audit_config.json` | Audit ON by default, log_select=false, collect_lan_ip=false |
| `.sql_linker/config_home/extra_tables.json` | Privileged tables, disabled by default, max_extra_tables=10 |
| `.sql_linker/table_home/table_dictionary.json` | Empty template with example table |
| `.sql_linker/set_env.ps1` | Password setup script for Windows (run to set password in OS env) |
| `.sql_linker/set_env.sh` | Password setup script for Linux/macOS (run to set password in OS env) |

***

## 配置文件说明

### 中文

### table_home/table_dictionary.json — 主词典

所有受控业务表必须在主词典中声明，字段白名单仅对 NORMAL 层生效：

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

### config_home/extra_tables.json — 特权表配置

词典外表格需通过此配置显式授权，enabled=false 时所有非词典表均 BLOCKED：

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

| 字段 | 描述 |
| --------------------- | -------------------------------------------------------------------------- |
| `enabled` | false=禁用词典外访问（默认）/ true=启用特权模式 |
| `max_extra_tables` | 最大声明表数，防止配置失控 |
| `tables[].table_name` | 特权表名 |

### config_home/config.yaml — 连接配置

数据库连接配置，password 不直接写在文件中，通过 password_env 引用加密后的密码，dbpw_key 用于混合加密：

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

**安全**：密码使用 `dbpw_key` 通过 HMAC-SHA256 加密。解密需要加密密码（在 OS 环境变量中）和 `dbpw_key`（在配置中）两者。OpenClaw agent 不知道 `dbpw_key` 则无法访问密码。

### English

### table_home/table_dictionary.json — Main Dictionary

All controlled business tables must be declared in the main dictionary. Field whitelist only applies to NORMAL layer:

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

### config_home/extra_tables.json — Privileged Table Config

Tables outside the dictionary require explicit authorization via this config. When enabled=false, all non-dictionary tables are BLOCKED:

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

| Field | Description |
| --------------------- | -------------------------------------------------------------------------- |
| `enabled` | false=disable dict-external access (default) / true=enable privileged mode |
| `max_extra_tables` | Max declared tables, prevents config runaway |
| `tables[].table_name` | Privileged table name |

### config_home/config.yaml — Connection Config

Database connection config. Password is encrypted with `dbpw_key` before storing in OS env:

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

**Security**: Password is encrypted with `dbpw_key` using HMAC-SHA256. Both encrypted password (in OS env) AND `dbpw_key` (in config) are required to decrypt. OpenClaw agent cannot access password without knowing `dbpw_key`.

***

## Python API — 业务层（推荐）

### 中文

使用业务层 API（推荐），完整支持四层访问控制和时间戳自动注入：

```python
import sys
sys.path.insert(0, "skills/sql-linker/scripts/service_layer")
from db_bridge import DBBridge

db = DBBridge(
    user_label="openclaw-control-ui",   # ← OpenClaw metadata.label
    session_id="agent:hr:main"          # ← OpenClaw metadata.id
)
```

### INSERT — 时间戳自动注入

INSERT 操作自动生成 created_at 和 updated_at（两者同值），仅写入主词典中声明的字段：

```python
db.insert("supplier_table", {
    "supplier_code": "LX001",
    "supplier_name": "立讯精密",
    "supplier_level": "A",
    "status": "active"
})
# → created_at / updated_at auto-generated, no manual injection needed
```

### UPDATE — 时间戳自动刷新

UPDATE 操作自动刷新 updated_at，created_at 保持不变：

```python
db.update(
    "supplier_table",
    {"supplier_level": "AA"},
    "supplier_code = %s",
    ("LX001",)
)
# → updated_at auto-refreshed to current time
```

### DELETE — 完整审计

```python
db.delete("supplier_table", "status = %s", ("inactive",))
```

### SELECT — 参数化防注入

```python
rows = db.query(
    "SELECT * FROM supplier_table WHERE status = %s AND supplier_level = %s",
    ("active", "A")
)
for row in rows:
    print(row)
```

### 辅助方法

```python
db.tables()           # Return all table names in main dictionary
db.extra_tables()     # Return current privileged table list
db.system_tables()    # Return protected system table list
db.fields("supplier_table")  # Return table field list (privilege table returns empty)
db.bootstrap(dry_run=False) # Execute bootstrap; dry_run=True returns file list without writing
```

### 错误处理

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

### English

Use the business layer API (recommended), with full four-layer access control and automatic timestamp injection:

```python
import sys
sys.path.insert(0, "skills/sql-linker/scripts/service_layer")
from db_bridge import DBBridge

db = DBBridge(
    user_label="openclaw-control-ui",   # ← OpenClaw metadata.label
    session_id="agent:hr:main"          # ← OpenClaw metadata.id
)
```

### INSERT — Automatic Timestamp Injection

INSERT operations automatically generate created_at and updated_at (same value), writing only fields declared in the main dictionary:

```python
db.insert("supplier_table", {
    "supplier_code": "LX001",
    "supplier_name": "立讯精密",
    "supplier_level": "A",
    "status": "active"
})
# → created_at / updated_at auto-generated, no manual injection needed
```

### UPDATE — Automatic Timestamp Refresh

UPDATE operations automatically refresh updated_at, leaving created_at unchanged:

```python
db.update(
    "supplier_table",
    {"supplier_level": "AA"},
    "supplier_code = %s",
    ("LX001",)
)
# → updated_at auto-refreshed to current time
```

### DELETE — Full Audit

```python
db.delete("supplier_table", "status = %s", ("inactive",))
```

### SELECT — Parameterized Injection Prevention

```python
rows = db.query(
    "SELECT * FROM supplier_table WHERE status = %s AND supplier_level = %s",
    ("active", "A")
)
for row in rows:
    print(row)
```

### Helper Methods

```python
db.tables()           # Return all table names in main dictionary
db.extra_tables()     # Return current privileged table list
db.system_tables()    # Return protected system table list
db.fields("supplier_table")  # Return table field list (privilege table returns empty)
db.bootstrap(dry_run=False) # Execute bootstrap; dry_run=True returns file list without writing
```

### Error Handling

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

## Python API — 数据操作层

### 中文

直接使用数据操作层，跳过业务层字段过滤和时间戳注入（适用于高级用户）：

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

### English

Use the data operation layer directly, bypassing business layer field filtering and timestamp injection (for advanced users):

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

## 时间戳注入规则

| 操作 | created_at | updated_at | 适用层 |
| ---------- | ----------- | ---------------------- | ---------------- |
| INSERT | 自动 | 自动（与 created 相同） | NORMAL |
| UPDATE | 不变 | 自动刷新 | NORMAL |
| DELETE | 不适用 | 不适用 | NORMAL |
| PRIVILEGED | 不适用 | 不适用 | PRIVILEGED |

***

## 审计日志

### 中文

**配置位置**：`.sql_linker/config_home/audit_config.json`

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

**审计记录字段**（自动注入，不可为空）：

| 字段 | 描述 | 来源 |
| --------------- | -------------------- | ------------------------------------------------- |
| `user_name` | 操作人 | audit_config.json 用户名 |
| `user_label` | 来源标签 | 显式或 OPENCLAW_LABEL 环境变量 |
| `ip_address` | 本地局域网 IP | 显式或 `_get_lan_ip()`（默认关闭） |
| `session_id` | OpenClaw 会话键 | 显式或 OPENCLAW_SESSION 环境变量 |
| `operation` | 操作类型 | SELECT / INSERT / UPDATE / DELETE |
| `table_name` | 目标表 | 从 SQL 提取 |
| `sql_statement` | SQL 语句 | 参数化脱敏（%s） |
| `rows_affected` | 影响行数 | 数据库返回值 |
| `status` | 操作状态 | SUCCESS / FAILED |

### English

**Config location**: `.sql_linker/config_home/audit_config.json`

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

**Audit record fields** (automatically injected, must not be empty):

| Field | Description | Source |
| --------------- | -------------------- | ------------------------------------------------- |
| `user_name` | Operator | audit_config.json username |
| `user_label` | Source label | Explicit or OPENCLAW_LABEL env |
| `ip_address` | Local LAN IP | Explicit or `_get_lan_ip()` (disabled by default) |
| `session_id` | OpenClaw Session Key | Explicit or OPENCLAW_SESSION env |
| `operation` | Operation type | SELECT / INSERT / UPDATE / DELETE |
| `table_name` | Target table | Extracted from SQL |
| `sql_statement` | SQL statement | Parameterized mask (%s) |
| `rows_affected` | Rows affected | Database return |
| `status` | Operation status | SUCCESS / FAILED |

***

## 字段类型参考

| type 值 | 描述 |
| -------------- | ----------------------------------------- |
| `BIGINT` | 主键 / 自增 ID |
| `VARCHAR(n)` | 字符串，最大 n 个字符 |
| `TEXT` | 长文本 |
| `INT` | 整数 |
| `DECIMAL(m,n)` | 小数，总共 m 位，小数点后 n 位 |
| `DATETIME` | 日期时间（`YYYY-MM-DD HH:MM:SS`） |
| `DATE` | 日期 |
| `BOOL` | 布尔值 |

***

## 双层审计体系

### 中文

sql-linker 采用**应用层 + 数据库层**双层审计；任何直接连接绕过应用层的操作仍会被捕获。

### 审计日志查看

`sql_audit_log` 属于 SYSTEM 层，业务层可以直接 SELECT：

```python
from datetime import date, timedelta
db = DBBridge(user_label="audit-viewer", session_id="agent:audit")

# 查询今天的操作记录
today = date.today().strftime('%Y-%m-%d')
rows = db.query(
    "SELECT log_time, user_name, operation, table_name, sql_statement, rows_affected, status "
    "FROM sql_audit_log WHERE DATE(log_time) = %s ORDER BY log_time DESC",
    (today,)
)

# 查询最近 7 天的失败操作
week_ago = (date.today() - timedelta(days=7)).strftime('%Y-%m-%d')
failed = db.query(
    "SELECT * FROM sql_audit_log WHERE status = 'FAILED' AND log_time >= %s "
    "ORDER BY log_time DESC",
    (week_ago,)
)

# 按供应商查询最近操作（模糊匹配）
rows = db.query(
    "SELECT log_time, user_name, operation, table_name, sql_statement "
    "FROM sql_audit_log WHERE sql_statement LIKE %s ORDER BY log_time DESC LIMIT 20",
    ('%LX001%',)
)
```

> ⚠️ `sql_audit_log` 是受系统保护的表。UPDATE/DELETE 被 `SystemTableWriteDenied` 阻止，仅允许 SELECT。

### 第一层：应用层审计

- 组件：`sql_linker.py` → `SQLAudit` 类
- 机制：每次 CRUD 操作后写入 `sql_audit_log`
- 覆盖范围：仅通过 `db_bridge` 的操作
- 局限性：直接的 `pymysql` / `mysql CLI` 可绕过

### 第二层：数据库层触发器

- **性质**：部署产物，不属于 skill 包的一部分。触发器绑定到特定表架构，由部署者/DBA 根据实际架构创建。
- 机制：在 MySQL 端对每个受控业务表创建 `AFTER INSERT/UPDATE/DELETE` 触发器，强制写入 `sql_audit_log`
- 覆盖范围：**所有直接连接数据库的写操作**，无论连接工具或路径

### 触发器编写原则

在**每个受控业务表**上，为 `INSERT` / `UPDATE` / `DELETE` 各创建一个 `AFTER` 触发器。示例结构：

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

**实施步骤**：

1. 确认 `sql_audit_log.id` 是 `AUTO_INCREMENT`（否则触发器 INSERT 会因没有默认 id 而失败）
2. 对每个受控表执行三个触发器
3. 触发器保存在用户仓库或 DBA 管理脚本中，不随 skill 包分发

### 两层配合效果

| 操作路径 | 应用层审计 | 触发器审计 | 结论 |
| ---------------- | --------------- | ------------- | ---------------- |
| db_bridge CRUD | ✅ 已记录 | ✅ 已记录 | 双重保证 |
| pymysql 直接 | ❌ 绕过 | ✅ 已记录 | 触发器兜底 |
| mysql CLI 直接 | ❌ 绕过 | ✅ 已记录 | 触发器兜底 |
| DBA 直接操作 | ❌ 绕过 | ✅ 已记录 | 触发器兜底 |

### English

sql-linker adopts **application layer + database layer** dual-layer audit; any direct-connection bypass of the application layer is still captured.

### Audit Log Query

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

### Layer 1: Application-Layer Audit

- Component: `sql_linker.py` → `SQLAudit` class
- Mechanism: Write to `sql_audit_log` after each CRUD operation
- Coverage: Operations via `db_bridge` only
- Limitation: Direct `pymysql` / `mysql CLI` can bypass

### Layer 2: Database-Layer Trigger

- **Nature**: Deployment artifact, not part of the skill package. Triggers are bound to specific table schemas, created by the deployer/DBA per actual schema.
- Mechanism: Create `AFTER INSERT/UPDATE/DELETE` triggers on MySQL side, mandatory write to `sql_audit_log`
- Coverage: **All write operations directly connecting to the database**, regardless of connection tool or path

### Trigger Writing Principles

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

### Dual-Layer Combined Effect

| Operation Path | App-Layer Audit | Trigger Audit | Conclusion |
| ---------------- | --------------- | ------------- | ---------------- |
| db_bridge CRUD | ✅ Logged | ✅ Logged | Double guarantee |
| pymysql direct | ❌ Bypassed | ✅ Logged | Trigger fallback |
| mysql CLI direct | ❌ Bypassed | ✅ Logged | Trigger fallback |
| DBA direct op | ❌ Bypassed | ✅ Logged | Trigger fallback |

***

## 安全原则

### 中文

1. **字段白名单**：`NORMAL` 表只能写入 `table_dictionary.json` 中声明的字段；非法字段自动过滤
2. **四层访问控制**：SYSTEM（读+审计写）/ 词典（白名单+时间戳）/ 特权（直接）/ 阻止（拒绝）
3. **参数化查询**：全部使用 `%s` + 元组防止 SQL 注入
4. **敏感凭据分离**：`password_env` 从 Windows OS 环境变量读取；`password_dpapi`（DPAPI 加密）替代方案——文件中无明文
5. **双层审计**：应用层 `db_bridge` + 数据库层触发器（由部署者根据实际架构创建）
6. **系统表保护**：`sql_audit_log` 禁止 UPDATE/DELETE，`SystemTableWriteDenied` 异常强制执行
7. **幂等 Bootstrap**：缺失的配置文件自动生成而不覆盖现有配置

### English

1. **Field Whitelist**: `NORMAL` tables only write fields declared in `table_dictionary.json`; illegal fields are automatically filtered
2. **Four-Layer Access Control**: SYSTEM table (read+audit write) / Normal dictionary (whitelist+timestamp) / Privileged (direct query) / Blocked (denied)
3. **Parameterized Queries**: All use `%s` + tuple to prevent SQL injection
4. **Sensitive Credential Separation**: `password_env` reads from Windows OS env (set via `set_env.ps1`); `password_dpapi` alternative — no plaintext in any file
5. **Dual-Layer Audit**: Application-layer `db_bridge` + database-layer triggers (created by deployer per actual schema)
6. **System Table Protection**: `sql_audit_log` prohibits UPDATE/DELETE, `SystemTableWriteDenied` exception enforced
7. **Idempotent Bootstrap**: Missing config files are auto-generated without overwriting existing configs

***

## 常见错误与解法

### 中文

| 错误 | 原因 | 解决方案 |
| ------------------------------------------------------------- | --------------------------------------------- | ------------------------------------------------------------------------- |
| `TableAccessDenied: Table 'xxx' not in dictionary` | 表不在词典中且未授权 | 添加到 `extra_tables.json` + `enabled:true` |
| `SystemTableWriteDenied: sql_audit_log does not allow UPDATE` | 试图篡改审计日志 | 正常拦截；如有误判请联系 DBA |
| 审计写入失败但数据成功 | 审计与业务不在同一事务 | 触发器提供兜底；应用层修复待定 |
| `Access denied for user ... (using password: NO)` | 密码未正确解密 | 确保 `config.yaml` 中的 `dbpw_key` 与设置密码时一致 |
| `Password not found: run set_env.ps1` | 缺少环境变量或 `dbpw_key` | 运行 `set_env.ps1` 加密并保存密码；确保 `dbpw_key` 存在 |
| `HMAC verification failed` | `dbpw_key` 错误 | 检查 `config.yaml` 中的 `dbpw_key` 与加密密码时一致 |
| `Config file not found` | 配置文件缺失 | 调用 `db.bootstrap()` 自动生成，或检查 `.sql_linker/` 结构 |
| `Table not found` | 表未在 `table_dictionary.json` 中声明 | 在主词典中添加表配置 |

### English

| Error | Cause | Solution |
| ------------------------------------------------------------- | --------------------------------------------- | ------------------------------------------------------------------------- |
| `TableAccessDenied: Table 'xxx' not in dictionary` | Table not in dictionary and not authorized | Add to `extra_tables.json` + `enabled:true` |
| `SystemTableWriteDenied: sql_audit_log does not allow UPDATE` | Attempt to tamper audit log | Normal interception; if misjudged, contact DBA |
| Audit write failed but data succeeded | Audit and business not in same transaction | Triggers provide fallback; app-layer fix pending |
| `Access denied for user ... (using password: NO)` | Password not decrypted correctly | Ensure `dbpw_key` in config.yaml matches when password was set |
| `Password not found: run set_env.ps1` | Environment variable or `dbpw_key` missing | Run `set_env.ps1` to encrypt and save password; ensure `dbpw_key` exists |
| `HMAC verification failed` | Wrong `dbpw_key` | Check `dbpw_key` in config.yaml matches when password was encrypted |
| `Config file not found` | Config file missing | Call `db.bootstrap()` to auto-generate, or check `.sql_linker/` structure |
| `Table not found` | Table not declared in `table_dictionary.json` | Add table config in main dictionary |

***

## 目录结构总览

### 中文

```
workspace/
└── .sql_linker/
    ├── set_env.ps1                    ← Windows 密码设置脚本（自动生成）
    ├── set_env.sh                     ← Linux/macOS 密码设置脚本（自动生成）
    ├── config_home/
    │   ├── config.yaml               ← 连接配置（extra_tables_enabled 开关）
    │   ├── audit_config.json         ← 审计配置（collect_lan_ip 选项）
    │   └── extra_tables.json        ← 特权表列表（JSON）
    └── table_home/
        └── table_dictionary.json    ← 主词典（JSON，所有受控表）
            └── tables[]               ← 每个表的 fields[] 白名单 + comment

skills/sql-linker/
├── SKILL.md                          ← 本文档
└── scripts/
    ├── controller_layer/             ← 数据操作层
    │   ├── sql_linker.py            ← 连接管理 + CRUD + 审计
    │   └── sql_audit.py            ← 审计模块
    └── service_layer/               ← 业务层
        └── db_bridge.py            ← 四层访问 + 时间戳 + Bootstrap
```

### English

```
workspace/
└── .sql_linker/
    ├── set_env.ps1                    ← Password setup script for Windows (auto-generated)
    ├── set_env.sh                     ← Password setup script for Linux/macOS (auto-generated)
    ├── config_home/
    │   ├── config.yaml               ← Connection config (extra_tables_enabled switch)
    │   ├── audit_config.json         ← Audit config (collect_lan_ip option)
    │   └── extra_tables.json        ← Privileged table list (JSON)
    └── table_home/
        └── table_dictionary.json    ← Main dictionary (JSON, all controlled tables)
            └── tables[]               ← Each table's fields[] whitelist + comment

skills/sql-linker/
├── SKILL.md                          ← This document
└── scripts/
    ├── controller_layer/             ← Data operation layer
    │   ├── sql_linker.py            ← Connection management + CRUD + audit
    │   └── sql_audit.py            ← Audit module
    └── service_layer/               ← Business layer
        └── db_bridge.py            ← Four-layer access + timestamp + Bootstrap
```
