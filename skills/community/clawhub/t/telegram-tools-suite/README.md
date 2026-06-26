# Telegram Tools Suite | Telegram工具集
> Telegram (Telethon) keyword monitoring and group search toolkit. This repository provides the **Python package `tg_monitor_kit`**, command line **`tg-monitor` / `python -m tg_monitor_kit`**, and **OpenClaw Skill**. All time and scheduled tasks are based on **Beijing Time**.
>
> Telegram（Telethon）关键词监控与群搜索工具包。本仓库提供 **Python 包 `tg_monitor_kit`**、命令行 **`tg-monitor` / `python -m tg_monitor_kit`**，以及 **OpenClaw Skill**。时间与定时任务均以**北京时间**为准。

Quick Start | 快速入口: Install with `pip install -e .`; CLI help `python -m tg_monitor_kit --help` or `tg-monitor --help`.
快速入口：安装 `pip install -e .`；CLI 帮助 `python -m tg_monitor_kit --help` 或 `tg-monitor --help`。

## Installation & Configuration | 安装与配置
1. Install dependencies (choose one): | 安装依赖（任选其一）：
   - `pip install -e .` (Recommended, execute in project root directory) | `pip install -e .`（推荐，在项目根目录执行）
   - Or `pip install -r requirements.txt` then add `src` to `PYTHONPATH` (Not recommended) | 或 `pip install -r requirements.txt` 后把 `src` 加入 `PYTHONPATH`（不推荐）
2. Copy `.env.example` to `.env`, fill in `TELEGRAM_API_ID`, `TELEGRAM_API_HASH`; fill in `TELEGRAM_PHONE` as needed (for login). | 复制 `.env.example` 为 `.env`，填写 `TELEGRAM_API_ID`、`TELEGRAM_API_HASH`；按需填写 `TELEGRAM_PHONE`（登录用）。
3. Session file: by default generated under `userdata/` in project root (name determined by `TELEGRAM_SESSION_NAME`). **Do not** delete the in-use `.session` file. | 会话文件：默认在项目根目录 `userdata/` 下生成（名称由 `TELEGRAM_SESSION_NAME` 决定）。**勿**删除正在使用的 `.session` 文件。

## First Run (Step by Step) | 首次运行步骤（必看）
1. Install | 安装：
   - `pip install -e .`
2. Get API credentials | 获取 API 凭据：
   - 打开 <https://my.telegram.org>
   - 使用手机号登录
   - 进入 `API development tools`
   - 创建应用后拿到 `api_id` 与 `api_hash`
3. Configure `.env` | 配置：
   - 必填：`TELEGRAM_API_ID`、`TELEGRAM_API_HASH`
   - 建议填：`TELEGRAM_PHONE`（如 `+8613xxxxxxxxx`）
4. Request code hash | 请求验证码 hash：
   - `python3 -m tg_monitor_kit auth`
   - 成功时输出：`SENT_CODE_SUCCESS:<phone_code_hash>`
5. Wait user code and login | 等待用户提供验证码并登录：
   - 设置 `TG_CODE`（短信验证码）
   - 设置 `TG_PHONE_CODE_HASH`（上一步输出）
   - 运行 `python3 -m tg_monitor_kit login`
   - 成功时输出：`LOGIN_SUCCESS`
6. Verify account | 验证账号：
   - `python3 -m tg_monitor_kit groups`
7. Start business command | 启动业务命令：
   - 监控：`python3 -m tg_monitor_kit monitor`
   - 搜索：`python3 -m tg_monitor_kit search`
  - 加群（单轮）：`ENABLE_HIGH_RISK_OPERATIONS=true python3 -m tg_monitor_kit join --once`
  - 定时群发：`ENABLE_HIGH_RISK_OPERATIONS=true python3 -m tg_monitor_kit send-schedule`

## Command List (Recommended) | 命令一览（推荐）
Execute in the project root directory (if `pip install -e .` is installed, you can directly use `tg-monitor`; otherwise use `PYTHONPATH=src python3 -m tg_monitor_kit`): | 在项目根目录执行（已 `pip install -e .` 时可直接用 `tg-monitor`；否则使用 `PYTHONPATH=src python3 -m tg_monitor_kit`）：

| Subcommand | Description | 说明 |
|--------|--------|------|
| `monitor` | Whitelist group keyword monitoring, hit notification, 18:00 daily Excel summary | 白名单群关键词监控、命中推送、每日 18:00 Excel 汇总 |
| `search` | Keyword-based supergroup search, scheduled daily, export to configured directory | 关键词搜超级群、按配置定时、导出到可配置目录 |
| `join` | Batch join groups from list file; requires `ENABLE_HIGH_RISK_OPERATIONS=true`. Persistent mode additionally requires `TG_ENABLE_PERSISTENT_JOIN=true` | 从清单文件批量加群；需先设置 `ENABLE_HIGH_RISK_OPERATIONS=true`。长驻模式还需 `TG_ENABLE_PERSISTENT_JOIN=true` |
| `send-schedule` | Multi-task scheduled message sending by JSON config file; requires `ENABLE_HIGH_RISK_OPERATIONS=true` | 通过 JSON 配置执行多任务定时群发；需先设置 `ENABLE_HIGH_RISK_OPERATIONS=true` |
| `groups` | List joined groups/channels | 列出已加入群/频道 |
| `members --group "group name"` | Group member list | 群成员列表 |
| `history --group "group name" [--limit N]` | Recent messages | 最近消息 |
| `account-info` | Current account information | 当前账号信息 |
| `auth` | Request SMS verification code when not logged in (requires `TELEGRAM_PHONE`) | 未登录时请求短信验证码（需 `TELEGRAM_PHONE`） |
| `login` | Complete login using environment variables `TG_CODE`, `TG_PHONE_CODE_HASH` | 使用环境变量 `TG_CODE`、`TG_PHONE_CODE_HASH` 完成登录 |

Examples | 示例：
```bash
cd "/path/to/Telegram-Tools-Suite"
python3 -m tg_monitor_kit groups
tg-monitor monitor
# Or if not installed as editable: PYTHONPATH=src python3 -m tg_monitor_kit monitor
# 或未安装 editable 时：PYTHONPATH=src python3 -m tg_monitor_kit monitor
```

## Code Organization | 代码组织
- `src/tg_monitor_kit/monitoring/`：群监控入口（CLI `monitor` 使用）
- `src/tg_monitor_kit/search/`：群搜索入口（CLI `search` 使用）
- `src/tg_monitor_kit/join/`：批量加群入口（CLI `join` 使用）
- `src/tg_monitor_kit/send/`：定时群发入口（CLI `send-schedule` 使用）
- `src/tg_monitor_kit/tools/`：查询类工具命令（`account-info` / `members` / `history`）

## Command Input Matrix | 命令与用户输入要求
| Command | Need user input? | Input source | 说明 |
|--------|------------------|-------------|------|
| `auth` | Yes | `.env` / env `TELEGRAM_PHONE` | 请求短信验证码，返回 `phone_code_hash` |
| `login` | Yes | env `TG_CODE` + `TG_PHONE_CODE_HASH` | 完成登录 |
| `groups` | No | - | 查看已加入群 |
| `account-info` | No | - | 查看账号信息 |
| `members --group` | Yes | CLI 参数 `--group` | 群名需与 Telegram 中一致 |
| `history --group --limit` | Yes | CLI 参数 | `--limit` 默认 100 |
| `monitor` | Yes | `config/target_groups.txt` | 文件为空会拒绝启动 |
| `search` | Yes | `config/group_search_keywords.txt` / `config/group_search.json` | 关键词和定时参数可配置 |
| `join [--once]` | Yes | `join_targets.txt` / env `TG_JOIN_LIST_FILE` | 每行一个目标，支持链接/用户名 |
| `send-schedule` | Yes | `config/scheduled_tasks.json` | 仅支持 JSON 多任务配置；`interval_hours` 不小于 0.5；任务数最多 20 |

## Keyword Monitoring (monitor) — Feature Summary | 关键词监控（monitor）— 功能摘要
- Listen to whitelist groups from `config/target_groups.txt` (or env `TG_TARGET_GROUPS_FILE`); monitor will not start when the list is empty. | 监听白名单群来自 `config/target_groups.txt`（或环境变量 `TG_TARGET_GROUPS_FILE`）；名单为空时监控不会启动。
- Keyword rules are loaded from `config/monitor_regex_rules.json` (or env `TG_MONITOR_REGEX_RULES_FILE`), and plain keywords are loaded from `config/keywords.txt` (or env `TG_KEYWORDS_FILE`); `SPAM_SKIP_PATTERNS` filters some spam templates. | 正则规则从 `config/monitor_regex_rules.json`（或环境变量 `TG_MONITOR_REGEX_RULES_FILE`）读取，普通关键词从 `config/keywords.txt`（或环境变量 `TG_KEYWORDS_FILE`）读取；`SPAM_SKIP_PATTERNS` 过滤部分垃圾模板。
- Print to console after hit, and push to `NOTIFY_TARGET` (default `me`). | 命中后控制台打印，并向 `NOTIFY_TARGET`（默认 `me`）推送。
- Export `daily_excel_summary/YYYY-MM-DD_监控汇总.xlsx` at 18:00 Beijing time daily (relative to **project root**). | 每日北京时间 18:00 导出 `daily_excel_summary/YYYY-MM-DD_监控汇总.xlsx`（相对**项目根**）。

### Pre-run Check | 运行前检查
- Available session file exists; proxy is reachable (default `127.0.0.1:1087`, configured by `TELEGRAM_PROXY_HTTP_*`). | 已存在可用会话文件；代理可达（默认 `127.0.0.1:1087`，由 `TELEGRAM_PROXY_HTTP_*` 配置）。
- `telethon` and `openpyxl` are installed. | 已安装 `telethon`、`openpyxl`。

### Session File Description | 会话文件说明
- `*.session`: Login state SQLite, must be retained. | `*.session`：登录态 SQLite，须保留。
- `*.session-journal`: SQLite log, paired with `.session`; may exist temporarily after abnormal exit. | `*.session-journal`：SQLite 日志，与 `.session` 成套；异常退出后可能短暂存在。

### Verification Steps | 验证步骤
1. Log like "Telegram monitoring service has started" appears after startup. | 启动后出现「Telegram 监控服务已启动」类日志。
2. Send a message containing keywords in the whitelist group. | 在白名单群发送含关键词消息。
3. "Keyword monitoring notification" print appears in the terminal. | 终端出现「关键词监控通知」打印。

### Startup Failure Troubleshooting | 启动失败排查
1. Long time no connection: Check proxy and network. | 长时间未连接：查代理与网络。
2. `database is locked`: Long-running commands now use isolated temporary session copies. If lock errors still appear (usually after abnormal exits), stop stale Python processes and retry. | `database is locked`：长驻命令已改为临时会话副本隔离；若仍出现锁冲突（多见于异常退出后），请先结束残留 Python 进程再重试。
3. `tg_monitor.lock`: Reject the second instance when there is already a monitoring instance; you can manually delete the lock file after abnormal exit (confirm no process is occupied). `join` uses `tg_join_from_list.lock`. | `tg_monitor.lock`：已有监控实例时拒绝第二实例；异常退出可手动删除锁文件（确认无进程占用）。`join` 使用 `tg_join_from_list.lock`。
4. `file is not a database`: Back up and delete the damaged `.session` / journal, then `auth` → `login`. | `file is not a database`：备份并删除损坏的 `.session` / journal，再 `auth` → `login`。

## Group Search (search) — Feature Summary | 群搜索（search）— 功能摘要
- Keyword list is read from `config/group_search_keywords.txt` (or env `TG_GROUP_SEARCH_KEYWORDS_FILE`). | 关键词从 `config/group_search_keywords.txt` 读取（或环境变量 `TG_GROUP_SEARCH_KEYWORDS_FILE`）。
- Schedule/search/output parameters are read from `config/group_search.json` (or env `TG_GROUP_SEARCH_SETTINGS_FILE`). | 定时/搜索/导出参数从 `config/group_search.json` 读取（或环境变量 `TG_GROUP_SEARCH_SETTINGS_FILE`）。
- Uses isolated temporary session copies at runtime, reducing lock contention with other long-running commands. | 运行时使用独立临时会话副本，降低与其它长驻命令的会话锁冲突。

## Batch Group Joining (join) — Feature Summary | 批量加群（join）— 功能摘要
- Place the list file **`join_targets.txt`** in the project root (or specify the absolute path or path relative to the project root through the environment variable **`TG_JOIN_LIST_FILE`**), one target per line: public group `@username` / `username`, `https://t.me/username`, `https://t.me/+invitation hash`, `https://t.me/joinchat/...`, etc. Empty lines and lines starting with `#` are ignored; duplicate targets are deduplicated. | 在项目根放置清单文件 **`join_targets.txt`**（或通过环境变量 **`TG_JOIN_LIST_FILE`** 指定绝对路径或相对项目根的路径），每行一个目标：公开群 `@username` / `username`、`https://t.me/username`、`https://t.me/+邀请哈希`、`https://t.me/joinchat/...` 等。空行与 `#` 开头行忽略；同一目标会去重。
- Persistent mode is disabled by default. Set `ENABLE_HIGH_RISK_OPERATIONS=true TG_ENABLE_PERSISTENT_JOIN=true` to enable scheduled looping. | 长驻模式默认关闭。需显式设置 `ENABLE_HIGH_RISK_OPERATIONS=true TG_ENABLE_PERSISTENT_JOIN=true` 才会按计划循环执行。
- Hard limits: join interval must be >= 30 minutes, and joins per round must be <= 20; startup is rejected when violated. | 硬限制：加群间隔必须 >= 30 分钟，且每轮加群数 <= 20；超限会拒绝启动。
- After each round, push success/already in group/failure statistics to favorites (`NOTIFY_TARGET = me`). It will automatically wait and retry when encountering `FloodWait`. | 每轮结束后向收藏夹（`NOTIFY_TARGET = me`）推送成功/已在群/失败统计。遇 `FloodWait` 会自动等待后重试。
- **Risk Control**: Batch joining groups may trigger Telegram rate limiting or violate terms of service, please control the list content and frequency by yourself; invalid invitation links, requiring administrator review, full group capacity, etc. will be recorded as failures. | **风控**：批量加群

## Scheduled Messaging (send-schedule) — Feature Summary | 定时群发（send-schedule）— 功能摘要
- Task source is fixed to `config/scheduled_tasks.json`, with top-level key `tasks` as an array. | 任务来源固定为 `config/scheduled_tasks.json`，顶层键为 `tasks` 数组。
- Required fields per task: `name`, `target_group_id`, `message`, `interval_hours`. | 单任务必填字段：`name`、`target_group_id`、`message`、`interval_hours`。
- Limits: `interval_hours >= 0.5`, and total tasks per run <= 20. | 限制：`interval_hours >= 0.5`，单次启动最多 20 个任务。
- Scheduler runs independently from `monitor`, and logs all trigger times in Beijing time. | 调度进程与 `monitor` 独立运行，触发日志统一按北京时间输出。
- Start command: `ENABLE_HIGH_RISK_OPERATIONS=true python3 -m tg_monitor_kit send-schedule`. | 启动命令：`ENABLE_HIGH_RISK_OPERATIONS=true python3 -m tg_monitor_kit send-schedule`。

## High-Risk Safeguards | 高风险能力保护
- `join` 与 `send-schedule` 均要求显式设置 `ENABLE_HIGH_RISK_OPERATIONS=true` 才可运行。 | Both `join` and `send-schedule` require explicit `ENABLE_HIGH_RISK_OPERATIONS=true`.
- `join` 默认仅允许单轮模式（`--once`）；长驻模式还需设置 `TG_ENABLE_PERSISTENT_JOIN=true`。 | `join` is one-shot by default; persistent mode additionally requires `TG_ENABLE_PERSISTENT_JOIN=true`.
- `send-schedule` 使用 `config/scheduled_tasks.json`；`interval_hours` 不能小于 0.5，且任务数不能超过 20。 | `send-schedule` reads `config/scheduled_tasks.json`; `interval_hours` must be >= 0.5 and tasks <= 20.

## Stop Long-Running Tasks | 如何停止长驻任务
- 前台运行：按 `Ctrl+C`。 | Foreground run: press `Ctrl+C`.
- 后台运行：结束对应 Python 进程。 | Background run: terminate the corresponding Python process.