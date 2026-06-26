---
name: Telegram Tools Suite
description: >
  Telegram 自动化工具包（群监控、群搜索、批量加群、定时发送）。
  运行时会生成敏感会话文件并包含可选长驻任务；默认启用风险保护，需显式确认后才可执行高风险动作。

requiredEnv:
  - name: TELEGRAM_API_ID
    description: Telegram API ID（来自 https://my.telegram.org）
    required: true
  - name: TELEGRAM_API_HASH
    description: Telegram API Hash（高敏感）
    required: true
  - name: TELEGRAM_PHONE
    description: Telegram 账号手机号（国际格式）
    required: true

optionalEnv:
  - name: ENABLE_HIGH_RISK_OPERATIONS
    description: 高风险总开关（join/send-schedule 需设为 true 才可运行）
    required: false
    default: "false"
  - name: TELEGRAM_SESSION_NAME
    description: 会话文件名（默认 tg_monitor_session）
    required: false
  - name: TELEGRAM_PROXY_HTTP_HOST
    description: Telegram 代理地址（默认 127.0.0.1）
    required: false
  - name: TELEGRAM_PROXY_HTTP_PORT
    description: Telegram 代理端口（默认 1087）
    required: false

  - name: TG_CODE
    description: 登录短信验证码（auth 后）
    required: false
  - name: TG_PHONE_CODE_HASH
    description: 登录验证码哈希（auth 输出）
    required: false

  - name: TG_PROJECT_ROOT
    description: 项目根目录覆盖（用于定位配置文件）
    required: false
  - name: TG_MONITOR_WEB_OUTPUT_DIR
    description: 网页脚本输出目录
    required: false

  - name: TG_TARGET_GROUPS_FILE
    description: 监控群白名单文件路径
    required: false
  - name: TG_KEYWORDS_FILE
    description: 监控关键词文件路径（默认 config/keywords.txt）
    required: false
  - name: TG_MONITOR_REGEX_RULES_FILE
    description: 监控正则规则文件路径
    required: false

  - name: TG_GROUP_SEARCH_KEYWORDS_FILE
    description: 群搜索关键词文件路径
    required: false
  - name: TG_GROUP_SEARCH_SETTINGS_FILE
    description: 群搜索配置文件路径
    required: false

  - name: TG_JOIN_LIST_FILE
    description: 批量加群目标文件路径
    required: false
  - name: TG_ENABLE_PERSISTENT_JOIN
    description: 是否开启 join 长驻模式（默认关闭；需 true）
    required: false
  - name: TG_JOIN_DELAY_SEC
    description: 加群间隔秒数（最小 1800）
    required: false
  - name: TG_MAX_JOINS_PER_RUN
    description: 单轮最多加群数量（最大 20）
    required: false

---

# Telegram Tools Suite

> ⚠️ 【重要安全&运行提示 安装前必读】
> 1. 敏感文件生成：技能运行时会在`userdata/`目录生成`*.session`会话文件（包含Telegram登录认证状态），并使用`.env`配置文件，均为高敏感信息，已默认加入`.gitignore`/`.clawignore`禁止提交到代码仓库/发布，请勿手动分享这些文件。
> 2. 持久运行说明：`monitor`（群监控）、`search`（群搜索）、`join`（批量加群定时模式）均为长时间运行的长驻任务，启动后会持续在后台运行直至手动终止。
> 3. 配置生效规则：所有配置文件（.env、config目录下的关键词/规则/配置文件）修改后，都需要重启对应的运行任务才会生效，修改配置不会影响正在运行的任务。
> 4. 合规使用提示：本工具仅用于合法的Telegram群组自动化管理用途，禁止用于发送垃圾信息、骚扰用户、批量爬取用户信息等违反Telegram服务条款和当地法律法规的行为。建议使用独立测试账号运行，避免主账号被平台封禁。所有配置需用户自行填写，工具无内置默认发送目标、消息内容或爬取规则。
> 4. 默认风险保护：`join` 与 `send-schedule` 均需先设置 `ENABLE_HIGH_RISK_OPERATIONS=true` 才可运行；其中 `join` 长驻模式还需额外设置 `TG_ENABLE_PERSISTENT_JOIN=true`。定时群发由 `send-schedule` 子命令执行，并按 `config/scheduled_tasks.json` 的限制进行校验。

## Instructions

### 🔹 前置说明
本技能为Telegram自动化工具，使用前需提前申请Telegram官方API凭证，需配置3项必填信息：`TELEGRAM_API_ID`、`TELEGRAM_API_HASH`、绑定手机号（国际格式）。

### 🔹 安装后引导&首次运行流程（按顺序执行）
1. **安装依赖**：执行 `pip install -e .`
2. **获取API凭证**：打开 <https://my.telegram.org>，用Telegram绑定手机号登录，进入「API development tools」创建应用，获得`api_id`和`api_hash`
3. **配置环境变量**：复制`.env.example`为`.env`，填入3项必填信息：`TELEGRAM_API_ID`、`TELEGRAM_API_HASH`、`TELEGRAM_PHONE`（国际格式，如`+8613xxxxxxxxx`）
4. **请求验证码**：执行 `python3 -m tg_monitor_kit auth`，记录输出的`SENT_CODE_SUCCESS:<phone_code_hash>`中的hash值
5. **完成登录**：设置环境变量`TG_CODE`（收到的短信验证码）、`TG_PHONE_CODE_HASH`（上一步获取的hash），执行`python3 -m tg_monitor_kit login`，输出`LOGIN_SUCCESS`即为登录成功
6. **连通性验证**：执行 `python3 -m tg_monitor_kit groups`，输出账号下的群组列表代表功能正常可用

### 🔹 多群定时发送功能使用说明
支持同时给多个群发送不同内容、设置不同发送间隔，配置方法：
1. 在本地自行创建：`config/scheduled_tasks.json`
2. 在 `scheduled_tasks.json` 中填写任务：
   - `name`：任务备注名，方便识别
   - `target_group_id`：目标群组ID（可以从`groups`命令输出中获取）
   - `message`：要发送的消息内容
   - `interval_hours`：发送间隔（小时，建议不小于1小时，避免被平台判定为垃圾消息）
3. 启动定时任务：`ENABLE_HIGH_RISK_OPERATIONS=true python3 -m tg_monitor_kit send-schedule`
> ⚠️ 防封号提示：建议不同群的消息内容不要完全一致，发送间隔不要低于30分钟，避免被Telegram判定为垃圾消息导致账号封禁。
> ⚠️ 校验限制：`interval_hours` 必须 `>= 0.5`，任务总数最多 20 个。


### Runtime Config Files (运行前按需编辑)

- 本技能发布包默认不包含 `config/` 目录内容；请在本地自行创建所需配置文件。
- 监控：创建 `config/target_groups.txt`、`config/keywords.txt`、`config/monitor_regex_rules.json`。
- 搜索：创建 `config/group_search_keywords.txt`、`config/group_search.json`。
- 定时群发：创建 `config/scheduled_tasks.json`。
- 批量加群：创建 `join_targets.txt`（或使用 `TG_JOIN_LIST_FILE` 指定路径）。

### Command Guide (命令入口)

- `python3 -m tg_monitor_kit groups`：列出已加入群/频道（无需额外参数）。
- `python3 -m tg_monitor_kit account-info`：查看当前账号信息（无需额外参数）。
- `python3 -m tg_monitor_kit members --group "群名称"`：导出指定群成员（需要群名）。
- `python3 -m tg_monitor_kit history --group "群名称" --limit 100`：导出指定群最近消息（需要群名；`--limit` 可选）。
- `python3 -m tg_monitor_kit monitor`：关键词监控（长驻）。
- `python3 -m tg_monitor_kit search`：群搜索（长驻，按配置定时）。
- `ENABLE_HIGH_RISK_OPERATIONS=true python3 -m tg_monitor_kit join --once`：批量加群（单轮）。
- `ENABLE_HIGH_RISK_OPERATIONS=true TG_ENABLE_PERSISTENT_JOIN=true python3 -m tg_monitor_kit join`：批量加群（长驻定时，默认关闭）。
- `ENABLE_HIGH_RISK_OPERATIONS=true python3 -m tg_monitor_kit send-schedule`：按 `config/scheduled_tasks.json` 执行定时群发（长驻）。

### 停止长驻任务
- 前台运行：按 `Ctrl+C` 终止。
- 后台运行：结束对应 Python 进程。

## Rules

- 严禁在对话或日志中输出 `TELEGRAM_API_HASH`、短信验证码、`.session` 文件内容。
- `monitor`、`search`、`join`、`send-schedule` 属于长驻任务，运行时会基于主会话复制临时会话副本；如遇异常退出仍可能触发 `database is locked`，请先结束残留进程后重试。
- 所有定时相关行为按北京时间（UTC+8）理解与配置。
- 在提供任何 Telegram 凭证前，必须先确认技能请求来源可信；发布方来源未知时，建议在一次性容器/隔离环境运行并使用测试账号。
- 批量加群存在风控风险，需由使用者自行确认目标与频率合规。

## Examples

### 示例 1：首次登录
输入：用户已填写 `.env`，需要首次登录。  
执行：先 `python3 -m tg_monitor_kit auth`，再设置 `TG_CODE`、`TG_PHONE_CODE_HASH`，再 `python3 -m tg_monitor_kit login`。  
输出：`LOGIN_SUCCESS`。

### 示例 2：开启监控
输入：用户已在 `config/target_groups.txt` 填写群名。  
执行：`python3 -m tg_monitor_kit monitor`。  
输出：控制台显示监控启动信息，命中关键词后推送通知。

### 示例 3：批量加群单轮执行
输入：用户已准备 `join_targets.txt`。  
执行：`ENABLE_HIGH_RISK_OPERATIONS=true python3 -m tg_monitor_kit join --once`。  
输出：返回成功/已在群/失败统计。
