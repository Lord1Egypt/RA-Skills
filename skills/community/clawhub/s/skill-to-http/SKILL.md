---
name: skill-to-http
description: >
  Expose installed agent Skills as HTTP(S) REST API services. Runs a persistent FastAPI
  server that auto-generates an API endpoint per Skill, with sync/async execution, webhook
  callbacks, and a multi-engine sub-agent executor (OpenClaw / Claude Code / Codex CLI /
  LLM fallback). Ships a bilingual (EN/ZH) web management console. HTTP by default
  (zero-friction), optional HTTPS with self-signed SAN certificates for production.
  Use when you need to serve Skills over HTTP, call Skills remotely, or expose Skill
  capabilities to external systems.
---

# skill-to-http

- **Version**: 1.0.2
- **License**: MIT
- **Author**: Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)
- **Repository**: https://github.com/Songhonglei/html-tool-suite (skill dir: `skills/skill-to-http`)

> **依赖**：Python 3.10+；`pip install fastapi uvicorn cryptography pydantic starlette`；
> 系统命令 `python3` / `openssl` / `curl`；可选 `pip install claude_agent_sdk`（Claude Code 执行器）。
> 所有 `SKILL_HTTP_*` / `OPENCLAW_*` 环境变量均为可选覆盖项，无一强制。

将已安装的 agent Skill 暴露为 HTTP/HTTPS REST API 服务。

> ## ⚠️ 安全须知（部署前必读）
>
> 本 skill 会启动一个常驻服务，把你**本机已安装的 agent Skill 暴露成可远程调用的 HTTP 接口**——被暴露的 Skill 可能拥有文件、shell、网络、凭证等本机能力。请务必理解以下风险边界：
>
> - **暴露即扩大攻击面**：任何能访问该端口的调用方，都能触发被暴露 Skill 的执行。`expose_skills: ["*"]` / `--expose-skill "*"` 会一次性开放**全部**已安装 Skill，仅建议在你完全掌控的隔离环境使用；生产/共享环境请改用白名单并对有副作用的 Skill 配置 `deny_skills`。
> - **默认 HTTP 不加密**：默认模式下 `X-API-Key`、请求 prompt、Skill 输出均**明文传输**。仅在 `localhost` 或可信内网可接受；跨主机 / 生产环境务必启用 HTTPS。
> - **务必设置鉴权与绑定**：非本机访问时必须配置 API Key，并谨慎对待 `0.0.0.0` 监听。管理控制台可启停服务、改配置、续证书，API Key 泄露等同交出服务控制权。
> - **执行即时且不二次确认**：执行器默认「立即执行、不询问」。对发邮件 / 删数据等高风险 Skill，请在其 frontmatter 设 `requires_confirmation: true`。
>
> 一句话：**这是一个把本机能力对外开放的工具，请当作暴露内部服务来对待，而非零风险的便捷封装。**

## 快速开始

```bash
# 安装依赖
cd /path/to/skill-to-http
pip install -r requirements.txt

# 进入 scripts/ 目录并启动（必须，否则会报 ModuleNotFoundError）
cd scripts
python3 server.py
```

首次启动会触发 init wizard，引导完成 8 步配置（含 TLS / API Key / 暴露范围 / 反向黑名单），
配置文件落到 `<workspace>/.skill-to-http/config.json`（OpenClaw 环境）或 `~/.skill-to-http/config.json`（兜底）。

**Agent 环境一行启动**（跳过向导用默认模板）：
```bash
python3 server.py --non-interactive --expose-skill "*"
```

**服务管理：**
```bash
python3 server.py status   # 查看运行状态和访问地址
python3 server.py stop     # 优雅停止（等待运行中的 job 完成）
python3 server.py restart  # 重启服务
```

启动后浏览器访问 API 文档：`http://localhost:8080/docs`（默认 HTTP 模式，零门槛）。

## HTTP / HTTPS

**默认 HTTP 模式（零门槛跑通）**：TLS 默认关闭，调用方直接 curl 即可（含 `X-API-Key` header）。监听 0.0.0.0 时启动会 warning 提示跨主机推荐启用 HTTPS。

**按需切回 HTTPS** 三步：

```bash
python3 scripts/gen_cert.py --san auto    # 1. 生成自签证书
# 2. 编辑 config.json 把 tls_enabled 改 true
python3 scripts/server.py restart         # 3. 重启
# 或一键：python3 server.py upgrade-to-https
```

init wizard 也会询问是否启用 HTTPS（默认 `none` 走 HTTP；选 `self-signed` 或 `imported` 才启）。

### 证书路径

证书自动放到统一目录：

| 探测顺序 | 路径 | 适用场景 |
|---|---|---|
| 1 | `$OPENCLAW_HTTP_ROOT` 环境变量 | Docker/K8s 显式指定 |
| 2 | `<workspace>/.http/certs/` | OpenClaw 环境（跟 PVC 持久化，**推荐默认**）|
| 3 | `~/.http/certs/` | 非 OpenClaw 环境兜底 |

与 `skill-to-http-flash` / `agent-easy-http` 共用同一根目录（详见 `references/tls-auth-standard.md`）。

```bash
# 已有 HTTP 服务 → 一键升级到 HTTPS
python3 server.py upgrade-to-https

# 证书管理
python3 server.py cert --cert-action info     # 查看 SAN / 到期
python3 server.py cert --cert-action renew    # 强制续期（嗅探本机 IP）
python3 server.py cert --cert-action import --cert-src /your/cert.pem --key-src /your/key.pem
```

公网部署 / Let's Encrypt 配方见 `references/https-deployment.md`。

## 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--port` | 监听端口 | 读 `config.port` → 自动选择 (8080→8090→3000→5000→随机) |
| `--host` | 监听地址 | 读 `config.listen_host` → `0.0.0.0` |
| `--https` | 强制启用 HTTPS（即使 config.tls_enabled=false 也启用） | 读 `config.tls_enabled` |
| `--cert` | HTTPS 证书路径 | 读 `config.cert_path` → `<HTTP_ROOT>/certs/server.crt` |
| `--key` | HTTPS 私钥路径 | 读 `config.key_path` → `<HTTP_ROOT>/certs/server.key` |
| `--skill-dir` | Skill 目录（可重复） | 默认扫描 `<workspace>/skills` + `/app/skills` |
| `--data-dir` | params 数据目录 | 读 `config.data_dir` → `<workspace>/.skill-to-http/data` |
| `--executor` | 强制执行器 | auto |
| `--api-key` | API Key 认证密钥（⚠️ 命令行传入会在进程列表可见，建议改用 `config.json` 或 `SKILL_HTTP_API_KEY` 环境变量） | — |
| `--expose-skill` | 暴露的 Skill（可重复，支持 *） | — |
| `--max-concurrent` | 最大并发执行数（0=不限） | 0 |
| `--max-request-size` | 请求体大小限制（MB） | 1 |
| `--no-docs` | 禁用 /docs 和 /redoc 接口（配置了 api_key 时建议开启） | false |

> **优先级**：命令行 > 环境变量 > config.json > 内置默认值。所有 config.json 字段都能被命令行/环境变量覆盖；
> 反过来 init wizard 写入 config.json 的 `tls_enabled` / `listen_host` / `port` / `deny_skills` 也都会被 server 读取生效。

## 环境变量

| 变量 | 说明 |
|------|------|
| `SKILL_HTTP_HOST` | 监听地址（与 `config.listen_host` 等价） |
| `SKILL_HTTP_PORT` | 监听端口（与 `config.port` 等价） |
| `SKILL_HTTP_HTTPS` | 设为 "1" 启用 HTTPS（与 `config.tls_enabled` 等价） |
| `SKILL_HTTP_CERT` | HTTPS 证书路径 |
| `SKILL_HTTP_KEY` | HTTPS 私钥路径 |
| `SKILL_HTTP_DENY_SKILLS` | 逗号分隔的反向黑名单（与 `config.deny_skills` 等价） |
| `SKILL_TO_HTTP_DATA_DIR` | params 数据目录 |
| `OPENCLAW_HTTP_ROOT` | TLS 证书 / API Key 持久化根目录（默认 `<workspace>/.http/`） |
| `OPENCLAW_API_URL` | OpenClaw Gateway 地址（优先读 `~/.openclaw/openclaw.json` 的 `gateway.port`，若未配置则 fallback `http://localhost:18789`） |
| `OPENCLAW_GATEWAY_TOKEN` | Gateway Bearer Token（优先读 `~/.openclaw/openclaw.json` 的 `gateway.auth.token`） |
| `OPENCLAW_AGENT_ID` | OpenClaw agent ID，CLI 路径使用（默认 `zhima`） |
| `SKILL_HTTP_API_KEY` | API Key 认证密钥 |
| `SKILL_HTTP_EXPOSE_SKILLS` | 逗号分隔的白名单（如 "skill-a,skill-b" 或 "*"） |
| `SKILL_HTTP_MAX_CONCURRENT` | 最大并发执行数 |
| `SKILL_HTTP_SKILL_DIRS` | 逗号分隔的 Skill 目录列表 |
| `SKILL_HTTP_EXECUTOR` | 强制指定执行器（auto/openclaw/cc/codex/llm） |

## API 接口

### GET /health
健康检查。
- **未认证或 API Key 未配置时**：仅返回 `{"status": "ok"}`
- **认证通过时**：返回完整信息（executor、skills_count、active_jobs）

### GET /skills
列出所有已注册 Skill（含参数 schema）。

### GET /skills/{name}
获取单个 Skill 的元信息。

### POST /skills/{name}/run
同步执行 Skill，等待完成后返回结果。

请求体：
```json
{
  "message": "任务描述",
  "params": {},
  "timeout_seconds": 120,
  "webhook_url": null
}
```

### POST /skills/{name}/run/async
异步执行 Skill，立即返回 job_id，通过 webhook 回调或轮询获取结果。

**Webhook 回调安全：**
- `webhook_url` 提交时校验：仅允许 http/https，拒绝回环（localhost/127.x）与链路本地（169.254.x）地址，防 SSRF
- 回调请求默认携带 HMAC 签名 header：`X-Callback-Sig`（HMAC-SHA256(secret, "{job_id}.{ts}")）+ `X-Callback-Ts`
- secret 自动生成并持久化在 `<HTTP_ROOT>/secrets/skill-to-http.hmac`；接收方可用 `tls_auth.verify_callback_signature` 验签（含 ±300s 防重放窗口）
- 不需要签名时在 config.json 设 `callback_auth_enabled: false`
- 回调失败自动退避重试 1 次

### GET /jobs/{job_id}
查询异步任务的执行状态和结果。

### POST /admin/reload
重新扫描并注册所有 Skill（无需重启服务）。

## 执行引擎

服务自动检测当前环境并使用最优执行方式：

优先级：**openclaw > cc（SDK）> claude_cli > codex > llm**

1. **OpenClaw** - 在 OpenClaw 会话中通过 sessions_spawn API 创建 sub-agent
   - 完整工具访问（browser、exec、memory 等）
   - 自动检测：`OPENCLAW_SESSION` 环境变量 **或** Gateway `/api/health` 可达（优先读 `~/.openclaw/openclaw.json` 端口配置，fallback 18789）
2. **Claude Code SDK** - 使用 `claude_agent_sdk.query()` 异步执行（**最快**）
   - 前提：`pip install claude_agent_sdk`（CC 内置，无需手动安装；独立环境安装见下。国内网络建议用清华镜像）
   - 完整工具访问（CC 内置工具集）；支持 asyncio 原生并发（多 skill 同时跑）
   - 启动开销 ~0.5s（Python import），无额外进程启动
   - 💡 天然没有 workspace context（AGENTS.md/SOUL.md/MEMORY.md），只接收 SKILL.md + prompt
3. **Claude CLI** - 通过 `claude --print --bare` 执行（**次快**）
   - 前提：`npm install -g @anthropic-ai/claude-code` 且 `claude` 在 PATH 中
   - 工具能力来自 claude CLI 自带工具（bash/read/write/search 等）
   - 启动开销 ~2.5-3s，比 openclaw CLI 快 ~1.5-2s；无 Gateway 限制
   - `--bare` 模式跳过所有插件和 hooks，最轻量启动
   - 💡 天然没有 workspace context，只接收 SKILL.md + prompt
4. **Codex CLI** - 通过 subprocess 调用 `codex --approval-mode full-auto`
   - 前提：`npm install -g @anthropic-ai/codex` 且 CLI 在 PATH 中
   - 完整工具访问（Codex 内置工具集）
   - 💡 Codex 天然没有 workspace context，只接收 SKILL.md + prompt
5. **LLM Fallback** - 直接调用 LLM API，SKILL.md 作为 system prompt
   - 前提：`config.json` 中配置 `llm.api_key`
   - ⚠️ **能力限制**：纯文本生成，**无法调用任何工具**（browser/exec/memory 等均不可用）。依赖工具的 Skill（如 IM 发送、日历、文档编辑类）在此模式下会失败或返回无意义结果。仅适合自包含的分析/总结类 Skill。
   - ⚠️ **安全提示**：会将 SKILL.md 内容发送到外部 LLM API，请确保 SKILL.md 不含内部地址、凭据或敏感信息。

**各环境推荐配置：**

| 部署环境 | 推荐 executor | 启动开销 | 备注 |
|---------|:---:|:---:|------|
| OpenClaw（本项目原生环境） | `openclaw` | ~5s | 自动检测，无需配置 |
| Claude Code SDK 可用 | `cc` | ~0.5s | 最快，asyncio 并发 |
| 仅有 claude CLI | `claude_cli` | ~2.5s | 无 Gateway 限制 |
| Codex CLI 环境 | `codex` | ~3s | CI/CD 流水线 |
| 纯独立服务器 | `llm` | — | 配置 `llm.api_key`，仅限无工具 Skill |

### 非 OpenClaw 环境部署指南

**CC 环境（Claude Code SDK，最快）：**
```bash
# 前提：claude_agent_sdk 在 Python path 中
# 检测方式：importlib.util.find_spec('claude_agent_sdk')

# 安装（独立环境，非 CC 内置环境）：
# 国内网络建议使用清华镜像（包体积 ~71MB，直连 PyPI 容易超时）
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple claude_agent_sdk
# 或指定版本 + 镜像：
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple 'claude_agent_sdk>=0.0.9'

# 验证安装：
python3 -c "import claude_agent_sdk; print(hasattr(claude_agent_sdk, 'query'))"

# 启动服务
cd scripts && python server.py --executor cc --non-interactive

# 特点：
# - asyncio 原生并发，多个 skill 可同时执行
# - 启动开销 ~0.5s（Python import），无额外进程
# - 通过 claude_agent_sdk.query() 执行，SDK 内部管理工具权限
# - 没有 workspace context（MEMORY/SOUL 等），只传 SKILL.md + prompt
```

**Claude CLI 环境（次快，无 Gateway 限制）：**
```bash
# 前提：claude CLI 在 PATH 中
# 检测方式：shutil.which('claude')

# 安装：
npm install -g @anthropic-ai/claude-code

# 验证安装：
claude --version

# 启动服务
cd scripts && python server.py --executor claude_cli --non-interactive

# 特点：
# - 使用 claude --print --bare，跳过所有插件，启动 ~2.5s
# - 不经过 OpenClaw Gateway，无 sessions_spawn 限制
# - 支持多进程并发
# - 没有 workspace context，只传 SKILL.md + prompt
# - 限制：不支持 OpenClaw 专属工具（browser/memory/cron 等）
```

**Codex 环境：**
```bash
# 前提：codex CLI 在 PATH 中（npm install -g @anthropic-ai/codex）
# 检测方式：shutil.which('codex')

# 启动服务
cd scripts && python server.py --executor codex --non-interactive

# 特点：
# - 通过 subprocess stdin 传入 prompt，--approval-mode full-auto 非交互
# - 适用于 CI/CD 流水线或 Codex 开发环境
```

**LLM Fallback 环境（纯服务器）：**
```bash
# 前提：config.json 中配置 llm.api_key + llm.base_url + llm.model

# 启动服务
cd scripts && python server.py --executor llm --non-interactive

# 特点：
# - 直接调 OpenAI 兼容 API，SKILL.md 作为 system prompt
# - ⚠️ 无法调用任何工具（browser/exec/memory 不可用）
# - 仅限自包含的分析/总结类 Skill
```

## 配置

通常不用手动建：首次启动 init wizard 会自动写入 `<workspace>/.skill-to-http/config.json`（OpenClaw 环境）
或 `~/.skill-to-http/config.json`（非 OpenClaw 环境）。需要手改时，可参考 `assets/config.example.json`：
- `executor` - 执行器选择（auto/openclaw/cc/codex/llm）
- `api_key` - API Key 认证密钥
- `expose_skills` - 白名单（如 `["skill-a", "skill-b"]` 或 `["*"]`）
- `max_concurrent` - 最大并发执行数（0=不限）
- `max_request_size_mb` - 请求体大小限制（MB）
- `disable_docs_without_auth` - 配置了 api_key 时是否自动关闭 /docs
- `skill_dirs` - Skill 扫描目录列表（示例路径，需根据实际环境修改）
- `data_dir` - params 存储目录
- `llm.base_url` - LLM API 地址
- `llm.api_key` - API Key（支持 `${ENV_VAR}` 引用环境变量）
- `llm.model` - 模型名称

## 目录说明

```
skill-to-http/
├── SKILL.md                  # 本文件
├── CHANGELOG.md              # 版本历史
├── README.md                 # 项目说明
├── requirements.txt          # Python 依赖
├── scripts/
│   ├── server.py             # FastAPI 主服务入口
│   ├── skill_runner.py       # 多环境执行引擎
│   ├── skill_registry.py     # Skill 扫描与注册
│   ├── params_generator.py   # 自动生成 params.json
│   ├── history_store.py      # SQLite Job 历史持久化
│   ├── context_meta.py       # OpenClaw context_level 扫描
│   ├── dep_scanner.py        # Skill 依赖自动扫描
│   ├── speed_mode.py         # 极速模式管理
│   ├── doctor.py             # 自检工具（环境/依赖/配置/Skills/TLS/运行时）
│   ├── tls_auth.py           # TLS+API Key+HMAC 鉴权模板（与 agent-easy-http 对齐）
│   ├── gen_cert.py           # 自签证书生成 + cert info/renew/import 子命令
│   ├── init_wizard.py        # 首次运行初始化向导（含非交互模式）
│   ├── _paths.py             # 持久化路径统一收口（workspace 内 .skill-to-http/）
│   ├── console.py            # 管理控制台后端（独立进程）
│   ├── console_ui/           # 管理控制台前端静态资源
│   └── start-console.sh      # 控制台启动脚本（独立进程管理）
├── references/
│   ├── tls-auth-standard.md  # HTTP 类 skill TLS+API Key+HMAC 统一规范（跨 skill 共享）
│   ├── https-deployment.md   # HTTPS 部署指南（内网/导入证书/Let's Encrypt）
│   └── params-schema.md      # params.json schema 规范（自定义入参 schema 时阅读）
└── assets/
    └── config.example.json   # 配置模板（首次启动会被 init wizard 覆盖）
```

### references 加载时机

| 文件 | 何时阅读 |
|------|---------|
| `tls-auth-standard.md` | 跨 HTTP skill 设计 / 改造鉴权层时；理解 `<HTTP_ROOT>` 目录约定 |
| `https-deployment.md` | 配置 HTTPS、导入公司 CA 证书、Let's Encrypt 公网部署 |
| `params-schema.md` | 自定义某个 skill 的 `params.json`（覆盖自动生成结果）时 |

## 历史记录

当 `history_store` 可用时（依赖 SQLite，无需额外安装），服务会自动持久化每条异步 job 的执行记录，并注册以下额外端点：

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/history` | 查询历史记录（支持 `?skill=xxx&limit=50&offset=0`） |
| GET | `/history/stats` | 每个 Skill 的执行次数统计 |
| GET | `/history/{job_id}` | 查询单条历史（job 内存过期后仍可查） |
| DELETE | `/history` | 清理旧记录（`?retention_days=7`，默认 7 天） |

服务启动后会注册一个后台线程，每 24 小时自动清理 7 天前的历史记录。

> **注意**：`GET /history` 是持久化历史；`GET /jobs/{job_id}` 是内存内状态（1 小时过期）。两者互为补充。

## 管理控制台

管理控制台是一个独立的 Web 服务（`console.py`），提供可视化的 Skill 管理、Job 历史、日志查看和服务启停界面。**界面支持中英双语一键切换**（顶栏 🌐 按钮，自动跟随浏览器语言，选择持久化到 localStorage）。

```bash
# 在 scripts/ 目录下启动控制台（独立于主服务）
cd scripts
python console.py
# 默认监听 http://0.0.0.0:9000（本机 + 内网可访问）
# 仅本机访问：python console.py start --host 127.0.0.1
# 推荐后台启动（脱离进程组 + 就绪探测）：bash start-console.sh
```

控制台默认监听 `0.0.0.0:9000`（局域网内可访问），访问 `http://localhost:9000` 打开 Web 界面。
`/api/*` 路由受保护：配置了 `api_key` 时校验 `X-API-Key`；未配置时按 Origin 白名单（localhost + 本机 LAN IP）做 CSRF 防护。

**控制台 API 端点（`http://<host>:9000`）：**

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/status` | 服务运行状态（端口/executor/uptime/活跃 job 数）|
| POST | `/api/service/start` | 启动主服务 |
| POST | `/api/service/stop` | 停止主服务 |
| POST | `/api/service/reload` | 热重载 Skill 注册 |
| GET | `/api/skills` | Skill 列表（含 context_level/exposed 状态）|
| POST | `/api/skills/{name}/expose` | 暴露 Skill |
| POST | `/api/skills/{name}/hide` | 隐藏 Skill |
| POST | `/api/skills/{name}/run` | 同步执行（测试用）|
| GET | `/api/jobs` | Job 历史列表（来自 history.db）|
| GET | `/api/jobs/{job_id}` | 单条 Job 详情 |
| GET | `/api/metrics` | 执行统计（调用次数/成功率/p50/p95 延迟）|
| GET | `/api/logs` | 服务日志（最后 100 行）|
| GET | `/api/doctor` | 运行环境诊断扫描 |
| POST | `/api/doctor/fix` | 自动修复可修复项 |
| GET | `/api/speed_mode/status` | 极速模式状态 |
| POST | `/api/speed_mode/enable` | 启用极速模式（SSE 流式进度）|
| POST | `/api/speed_mode/disable` | 禁用极速模式 |

**注意事项：**
- 控制台的 `api_key` 认证在**启动时**从 `config.json` 一次性读取，修改 `config.json` 后需重启控制台才生效
- 控制台不应暴露到公网，仅供本机或内网受信环境使用
- 控制台可直接触发主服务的启动/停止，请确保访问来源受控

## 异步任务说明

- 异步 job 保留时间为 **1 小时**，超时后自动清理
- `GET /jobs/{job_id}` 返回 404 说明 job 已过期清理
- 建议大任务使用 `webhook_url` 回调，而非长时间轮询
- `GET /health`（认证后）会返回 `job_ttl_seconds: 3600`

## 安全说明

- **CORS**：主服务默认 `Access-Control-Allow-Origin: *`（不带 credentials），内网部署时注意只对受信来源开放，或配置反向代理限制来源
- **API Key 传递**：避免通过 `--api-key` 命令行参数传入（进程列表可见），推荐使用 `config.json` 中的 `api_key` 字段或 `SKILL_HTTP_API_KEY` 环境变量
- **控制台**：默认监听 `0.0.0.0:9000`（内网可达）。不要将其反代到公网；如只需本机使用请加 `--host 127.0.0.1`
- **params 缓存**：`params.json` 由 LLM 自动生成后缓存在 `<workspace>/.skill-to-http/data/params/`（OpenClaw 环境）或 `~/.skill-to-http/data/params/`（兜底）。更新 SKILL.md 后若需重新生成，删对应目录的 `params.json` 并调用 `POST /admin/reload` 即可

## Docker 部署

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
WORKDIR /app/scripts
# 注意：executor=llm 无法调用工具（browser/exec/memory 等均不可用）
# 只适合自包含的分析/总结类 Skill；依赖工具的 Skill 需改为 openclaw/cc/codex
ENV SKILL_HTTP_EXPOSE_SKILLS=* \
    SKILL_HTTP_EXECUTOR=llm \
    SKILL_HTTP_MAX_CONCURRENT=5
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')"
CMD ["python", "server.py", "--non-interactive"]
```

```bash
# 构建与运行
docker build -t skill-to-http .
docker run -d \
  -p 8080:8080 \
  -v ~/.skill-to-http:/root/.skill-to-http \
  -v ~/.http:/root/.http \
  -e SKILL_HTTP_API_KEY=your-secret-key \
  -e SKILL_HTTP_EXPOSE_SKILLS="work-summary,data-report" \
  -e OPENAI_API_KEY=sk-xxx \
  skill-to-http
```

## Changelog

See [CHANGELOG.md](CHANGELOG.md).
