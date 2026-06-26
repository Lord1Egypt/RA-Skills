# Prana 封装技能（共享包）

本目录为从 Prana 封装下载的**轻量技能包**：不含业务实现代码，含 **`SKILL.md`**、**`skill.yaml`**、**`package.json`**（供 Node 脚本依赖）与双语言薄客户端。`SKILL.md` / `skill.yaml` **不**展示 `skill_key`、`original_skill_key` 等标识；服务端打包时会将封装元数据 **写入** `scripts/prana_skill_client.py`（`_ENCAPSULATION_EMBEDDED`）与 **`scripts/prana_skill_client.js`**（`ENCAPSULATION_EMBEDDED`），可由渠道或 AI 任选 **Python 3** 或 **Node.js 18+** 运行。

## 目录说明

封装包**包含** 根目录 **`skill.yaml`**（OpenClaw / Claw Hub 等入口描述，与 `SKILL.md` 配套）。

| 文件/目录 | 说明 |
|-----------|------|
| `SKILL.md` | frontmatter 主要含 `name`、`description` 及可选 `input_format` 等；**不含** `skill_key` / `original_skill_key` / `encapsulation_target` |
| `skill.yaml` | OpenClaw 清单：`entryPoint` 默认 Python；`prana_runners` 列出 Node 脚本路径；**不含**业务 skill_key 字段 |
| `scripts/prana_skill_client.py` | Python 入口（无业务逻辑）；已注入 `_ENCAPSULATION_EMBEDDED` |
| `scripts/prana_skill_client.js` | Node 入口（ES Module，与 Python 行为对齐）；已注入 `ENCAPSULATION_EMBEDDED`；需先在包根目录 **`npm install`** |
| `package.json` | Node 依赖声明（当前含 `yaml`，用于解析 `SKILL.md` frontmatter） |
| `config/api_key.txt` | 凭证（单行 `pk:sk` 或粘贴接口 JSON）；可由 `GET /api/v1/api-keys` 手工填入，或由薄客户端自动拉取并写入本文件；接口须带 **`target_system`**，仅 **prana** 使用 `account_id`（见 `config_api_key.txt`） |

**调用远端**时使用脚本内 **`original_skill_key`**（Python `_ENCAPSULATION_EMBEDDED` / Node `ENCAPSULATION_EMBEDDED`，两脚本一致）。元数据中的公开包 id 仍可经下载接口查询。

## `skill.yaml` 说明（不是 `SKILL.yaml`）

根目录文件名为**小写** **`skill.yaml`**，由 **Prana 服务端在封装时自动生成**（调用 `/api/skill/encapsulate/run` 或 `/download` 打入 tar.gz），**无需、也不应**手工编写。

| 项目 | 说明 |
|------|------|
| **作用** | 给 OpenClaw / Claw Hub 等读的**技能清单**：名称、版本、`entryPoint`（Python）；`prana_runners` 供选用 Node |
| **生成来源** | 基于源技能目录的 `SKILL.md`（名称、描述、`trigger`→keywords、`license` 等）+ 当前**上线版本号** |
| **主要字段** | `name`、`version`、`description`、`entryPoint`、`prana_runners` 等（不含业务 skill_key；见脚本内嵌） |
| **可选** | 若源 `SKILL.md` frontmatter 有 `trigger`，会写入 `triggers.keywords` |
| **与 `SKILL.md` 分工** | 文档用 frontmatter；运行时 **`agent-run` 的 `skill_key` 取自 Python/Node 任一脚本内嵌** |

## 快速开始

1. **获取 API Key**（首次无本地凭证时）  
   调用 `GET /api/v1/api-keys`。  
   **必带 / 建议带**查询参数 **`target_system`**（与封装平台一致，与脚本内 `encapsulation_target` 一致；**未传时服务端按 prana 处理**）。  
   - **仅当 `target_system=prana` 时**才使用 **`account_id`**；Claw Hub、`claw_hub` 等其它平台**不要传** `account_id`（服务端会忽略误传）。  
   - **沙盒（Prana）**：环境变量 **`ACCOUNT_ID`** 有值时，薄客户端仅在平台为 **prana** 时自动附加 `account_id`。  

   示例（Prana + 已有账户）：

   ```bash
   curl -sS "${NEXT_PUBLIC_URL}/api/v1/api-keys?target_system=prana&account_id=${ACCOUNT_ID}"
   ```

   示例（非 Prana，勿带 account_id）：

   ```bash
   curl -sS "${NEXT_PUBLIC_URL}/api/v1/api-keys?target_system=claw_hub"
   ```

   也可用环境变量 **`ENCAPSULATION_TARGET`**（或 `SKILL_ENCAPSULATION_TARGET`）覆盖包内平台标识。  

   **自动落盘**：Python / Node 任一脚本在拉取成功后会默认写入 **`config/api_key.txt`**（可用 `PRANA_SKILL_SKIP_WRITE_API_KEY=1` 关闭）。

   响应示例：

   ```json
   {
     "code": 200,
     "message": "success",
     "data": {
       "api_key": {
         "public_key": "pk_...",
         "secret_key": "sk_..."
       }
     }
   }
   ```

   将 **`data.api_key`** 中的 `public_key`、`secret_key` 写入 **`config/api_key.txt`**：  
   单行 `public_key:secret_key`（一个英文冒号）；或把接口完整 JSON **粘贴进同一文件**（多行亦可，脚本会解析）。

2. **调用技能**（任选 Python 或 Node）

   脚本请求 `POST /api/claw/agent-run` 与（必要时）`POST /api/claw/agent-result` 时，会在请求头加入 **`x-api-key: public_key:secret_key`**（**body 不传 `api_key`**）。  
   - **agent-run** body：`skill_key`（= **脚本内嵌 `original_skill_key`**）、`question`（由 frontmatter 参数说明与用户消息组装）、`thread_id`、`request_id`。  
   - **agent-result** body：仅 `request_id`。  
   `request_id` 不在 `content` 字符串内。

   **Python：**

   ```bash
   export NEXT_PUBLIC_URL=https://你的-prana-域名   # 可选，有默认值时请按文档修改
   python3 scripts/prana_skill_client.py -m "用户说的话或任务描述" -t ""
   ```

   **Node（需先安装依赖）：**

   ```bash
   cd /path/to/技能包根目录
   npm install
   export NEXT_PUBLIC_URL=https://你的-prana-域名   # 可选
   node scripts/prana_skill_client.js -m "用户说的话或任务描述" -t ""
   ```

   第二轮起传入上次响应中的 `thread_id`（若接口返回）：`-t <thread_id>`。

   **长任务与网络异常**：两脚本行为一致——先请求 `POST /api/claw/agent-run`；若超时、连接失败、网关/服务端错误（5xx、408、504），或 **running 但响应非合法 JSON**，会改查 `POST /api/claw/agent-result`。**首次查询前会等待 120 秒，之后若 `data.status` 仍为 `running`，则每隔 120 秒再查一次**，直至结束或达上限（默认 20 次）。可用 `PRANA_AGENT_RESULT_POLL_INTERVAL_SEC`、`PRANA_AGENT_RESULT_POLL_MAX_ATTEMPTS` 调整。成功经此路径返回的 JSON 会带 `_recovered_via: "agent-result"`。

3. **环境变量**（可选）

   - `NEXT_PUBLIC_URL`：Prana API 根 URL  
   - `ENCAPSULATION_TARGET` / `SKILL_ENCAPSULATION_TARGET`：拉取 key 时的 `target_system`（覆盖脚本内嵌 / 旧版 `SKILL.md`）  
   - `ACCOUNT_ID` / `PRANA_ACCOUNT_ID`：仅 **platform=prana** 时参与 GET `/api/v1/api-keys`  
   - `PRANA_SKILL_SKIP_WRITE_API_KEY=1`：拉 key 成功不写 `api_key.txt`  
   - `PRANA_SKILL_PUBLIC_KEY` + `PRANA_SKILL_SECRET_KEY`：优先于配置文件  
   - `PRANA_SKILL_API_KEY`：整段 JSON，或单行 `public_key:secret_key`  
   - `PRANA_AGENT_RESULT_POLL_INTERVAL_SEC`：改查 `agent-result` 时的间隔秒数（默认 `120`）  
   - `PRANA_AGENT_RESULT_POLL_MAX_ATTEMPTS`：最多轮询次数（默认 `20`）

## 与渠道的集成

各渠道 LLM（Cursor、OpenClaw 等）应在运行本技能时：

1. 检查本地是否已配置 `public_key`/`secret_key`；若无则 `GET /api/v1/api-keys`（带合适 **`target_system`**；仅 Prana 带 `account_id`）再写入 **`api_key.txt`**，或依赖薄客户端自动拉取并写 `api_key.txt`。  
2. 根据环境调用 **`prana_skill_client.py`** 或 **`prana_skill_client.js`**（后者需先 `npm install`），将用户消息作为 `-m` 传入，维护 `thread_id` 实现多轮对话。  
3. 若返回付费链接（HTTP 402 等），按文档引导用户完成支付后重试。

## 安全说明

- 勿将 `config/api_key.txt` 提交到公开 Git 仓库。  
- 本包内**不包含**专业技能实现脚本，知识产权保留在 Prana 服务端。
