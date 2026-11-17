---
name: skill-to-http-flash
description: >
  把单个 Skill 编译成独立 HTTP REST API 微服务（v2.0 subprocess 直执行）。当用户说「skill 暴露成
  HTTP 接口」「flash 一个 skill」「skill 起 API 服务」「skill 输入输出结构化」「standalone 跑 skill」
  「skill-to-http-flash」时使用。JSON → Python 入口 → 统一 envelope（success/exit_code/data|output/stderr）。
  毫秒冷启，运行期不依赖 Gateway/LLM，多 agent runtime 通用（OpenClaw/Claude Code/Cursor）。默认 HTTP，按需 HTTPS。
---

# skill-to-http-flash v2.0

- **Version**: 2.0.4
- **License**: MIT
- **Author**: Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)
- **Repository**: https://github.com/Songhonglei/skill-to-http-flash

> **依赖**：Python 3.10+；`pip install fastapi uvicorn cryptography pydantic jsonschema`；可选 `openssl`（HTTPS）。

> **定位**：subprocess 直执行 + standalone。"把 Skill 脚本变成稳定 REST API"的微服务工厂。

```
POST /run  →  subprocess.run(["python3", "scripts/main.py", "--foo", "x", ...])
            →  envelope { success / exit_code / elapsed_ms / data | output / stderr / truncated }
```

不依赖 Gateway，运行期不调 LLM，不走 sessions_spawn。秒级冷启，100% 复现，零 LLM 漂移。

> ℹ️ **关于 LLM**：**运行期（/run 执行 skill）完全不碰 LLM**，100% subprocess 确定性。
> 仅在 `create` / `recreate` **生成期**，会*可选*用 LLM 从 SKILL.md 自动提取入参 schema——
> 未配置 LLM（默认）时走启发式 fallback（空 schema + `additionalProperties: true`），
> 生成后可手动编辑 `params.json`。即：**跑起来零 LLM，生成时 LLM 只是锦上添花**。

---

## v1 → v2 重大变更速览

| 维度 | v1.x | v2.0 |
|---|---|---|
| 执行方式 | sessions_spawn 调 OpenClaw agent + LLM | **subprocess 直调 skill 的 Python 入口** |
| 依赖 Gateway | ✅ 必须 | ❌ 不需要 |
| 入参 | 自由 message 字段（LLM 解读） | **JSON Schema 校验 + 长 flag CLI 映射** |
| 出参 | 自由文本 | **统一 envelope，自适应 JSON 解析（A）或文本（B）** |
| 截断 | 无明确阈值 | **同步 512 KB 截断 + 异步不截断** |
| skill-to-http 依赖 | 静默自动安装 | **完全移除，自带 `_cert.py`** |
| standalone | 部分支持 | **一等公民设计目标**（`--skill-dir`/`--data-dir` + env 覆盖）|
| 默认超时 | 120s | **60s**（同步）|

**v2.0 不兼容 v1 老 project**。已有的 v1 project 必须 `flash.py remove` 后重新 `create`。详见 `references/migration-from-v1.md`。

---

## 前置条件

- **Python 3.10+**
- Skill 的入口必须是 **`.py` 文件**（v2.0 不支持 shell entry，因为 shell 难校验参数）
- 推荐 skill 的入口用 `argparse` 长 flag（自动映射 `{"foo": "x"}` → `--foo x`）

**不再需要**：OpenClaw Gateway / 运行期 LLM。（生成期可选 LLM 提参，未配置走 fallback，见上方说明。）

---

## SKILL.md frontmatter 约定（推荐）

让被 flash 的 skill 在 frontmatter 显式声明入口：

```yaml
---
name: my-skill
version: 1.0.0
description: ...
flash:
  entry: scripts/main.py        # 相对 skill 目录
  interpreter: python3          # 可选，默认 python3
---
```

**找不到 `flash.entry` 时**，flash 按以下顺序扫 7 个候选位置（首个命中为准）：

1. `scripts/<skill-name>.py`
2. `scripts/cli.py`
3. `scripts/main.py`
4. `scripts/run.py`
5. `<skill-name>.py`（skill 根目录）
6. `main.py`（skill 根目录）
7. `cli.py`（skill 根目录）

都找不到 → 直接报错并打印 frontmatter patch 建议，引导用户加 `flash.entry`。

> ⚠️ 找到 `.sh` 入口也会报错 — v2.0 只支持 `.py`。包一层 `subprocess.run(["bash", ...])` 的 Python launcher 即可。

---

## 快速开始（OpenClaw 环境）

```bash
cd ~/.openclaw/workspace/skills/skill-to-http-flash/scripts

# 1. 创建 flash 项目
python3 flash.py create --skill <skill-name>
#   → 解析入口、提参数 schema、交互确认端口/超时/TLS
#   → 生成到 <workspace>/.skill-to-http-flash/services/<skill-name>-api/

# 2. 启动
cd <workspace>/.skill-to-http-flash/services/<skill-name>-api
pip install -r requirements.txt
python3 server.py start

# 3. 调用
curl -X POST http://127.0.0.1:7780/run \
  -H 'content-type: application/json' \
  -d '{"foo": "bar"}'
```

---

## Standalone 用法（非 OpenClaw 环境）

任何能跑 Python 的机器都能用，**完全不依赖 ~/.openclaw**。它本质是"把带 argparse 的 Python 脚本编译成 REST API"，与具体 agent runtime 无关——不 import 任何 agent SDK，不调 Gateway / LLM / sessions_spawn。

**多 agent 开箱即用**：默认自动探测以下 skill 目录（首个命中为准），OpenClaw / Claude Code / Cursor 用户无需手设 env：

```
~/.openclaw/workspace/skills/   # OpenClaw
~/.claude/skills/               # Claude Code
~/.cursor/skills/               # Cursor
~/.config/skills/               # 通用 XDG
./skills/                       # 项目本地
/app/skills/                    # 容器挂载
```

自定义目录（其它 runtime 或非标准布局）：

```bash
# 方式 A：环境变量
export FLASH_SKILL_DIR=/your/path/to/skills
export FLASH_DATA_DIR=/your/path/to/flash-data
python3 flash.py create --skill my-skill

# 方式 B：CLI flag（每条命令带上）
python3 flash.py \
  --skill-dir /your/path/to/skills \
  --data-dir /your/path/to/flash-data \
  create --skill my-skill
```

> 生成的 `server.py` 完全自包含，可 scp 到任何机器裸跑（只需 `pip install -r requirements.txt`），与本 skill / 任何 agent runtime 解耦。

完整 standalone 指南：`references/standalone-usage.md`

---

## 入参映射规则（JSON → CLI 长 flag）

| 请求 JSON | 转成 argv |
|---|---|
| `{"foo": "x"}` | `--foo x` |
| `{"foo_bar": 10}` | `--foo-bar 10`（下划线 → 横杠）|
| `{"verbose": true}` | `--verbose`（flag style）|
| `{"verbose": false}` | （不传，约定脚本默认就是 false）|
| `{"verbose": null}` | （不传）|
| `{"tags": ["a","b"]}` | `--tags a --tags b`（重复 flag）|
| `{"meta": {"k":"v"}}` | `--meta '{"k":"v"}'`（嵌套对象序列化为 JSON 字符串）|

**安全**：字段名走白名单 `[a-z][a-z0-9_]*`（防 `--foo;rm -rf /`），argv 走 list 不拼 shell。

---

## 响应 envelope

```json
{
  "success": true | false,        // exit_code == 0
  "exit_code": 0 | n,              // subprocess 返回码
  "elapsed_ms": 240,
  "data": <object|array|primitive> | null,  // stdout 是合法 JSON 时（模式 A）
  "output": "<string>" | null,              // stdout 不是 JSON 时（模式 B）
  "stderr": "<string>" | null,              // 仅 success=false 时透出
  "stderr_truncated": true,                  // 仅 stderr 被截断时（success=false 路径）
  "truncated": true,                         // 仅同步 + stdout >512KB 时
  "hint": "Output exceeded 512KB. Use POST /run/async + GET /jobs/<id> for full output."  // 仅 truncated=true 时
}
```

**`data` 和 `output` 互斥**——任意时刻只有一个有值。

### 自适应 JSON 解析

- stdout 是合法 JSON → 走 `data` 字段（**模式 A**，客户端可结构化访问）
- 否则 → 走 `output` 字段（**模式 B**，原始文本）
- 脚本零改动：原来啥样还啥样

### 错误类型

| 错误码 | HTTP | 触发场景 |
|---|---|---|
| `validation_failed` | 400 | JSON Schema / 字段名白名单校验失败 |
| `entry_not_found` | 500 | 入口文件不存在或不是 .py |
| `spawn_failed` | 500 | subprocess 启动失败（interpreter not in PATH 等）|
| `timeout` | 408 | 超过 timeout_seconds |
| `rate_limited` | 429 | /run/async 并发 >20 |
| `internal_error` | 500 | 未预期异常（兜底）|
| _exit_code != 0_ | **200** | 业务执行失败（脚本"运行了但失败"），envelope.success=false + stderr 透出 |

设计原则：**业务失败用 envelope 表达，HTTP 状态码只表达框架问题**。

---

## 路由

| Method | Path | 说明 |
|---|---|---|
| GET | `/` | HTML 引导页 |
| GET | `/health` | probe entry 文件 + interpreter 在 PATH |
| GET | `/schema` | 入参 JSON Schema + entry / interpreter |
| GET | `/docs` | FastAPI Swagger UI |
| POST | `/run` | **同步**执行，默认 60s 超时，512KB 截断 |
| POST | `/run/async` | **异步**执行，立即返回 job_id，**不截断** |
| GET | `/jobs/{id}` | 轮询异步任务（内存 + JSONL fallback）|

---

## 异步任务（不截断 + 持久化）

```bash
# 提交
JOB=$(curl -s -X POST http://127.0.0.1:7780/run/async \
  -H 'content-type: application/json' -d '{"big_query": true}')
JOB_ID=$(echo "$JOB" | jq -r .job_id)

# 轮询
curl http://127.0.0.1:7780/jobs/$JOB_ID
# {"job_id":"...","status":"completed","result":{...完整 envelope...}}
```

- **不截断**：异步任务保留完整 stdout（>512KB 也不切）
- **内存（快查，1h TTL）+ JSONL 持久化（重启不丢）**
- **并发上限 20**：`{"status": "failed", "error_type": "rate_limited"}` 429
- **logrotate**：JSONL 单文件 >10MB 切到 `.1` ~ `.7`，保留 7 份
- **导出 SQLite**：`python3 flash.py jobs-export-sqlite --skill <name>`

---

## CLI 命令清单

```bash
# 创建项目（首次/新 skill）
python3 flash.py create --skill <name> [--output <dir>]

# 列出所有项目
python3 flash.py list

# 删除（默认保留生成的代码，加 --delete-files 一并删）
python3 flash.py remove --skill <name> [--delete-files]

# Skill 升级后重新生成（保留端口/超时/TLS 配置，只刷 server.py 和 params.json）
python3 flash.py recreate --skill <name> [--yes] [--diff]

# 证书管理（HTTPS 模式）
python3 flash.py cert --skill <name> --cert-action info | renew | import \
    [--cert-src <crt> --key-src <key>]

# 异步 job 历史导出 SQLite
python3 flash.py jobs-export-sqlite --skill <name>

# 生成 systemd unit（宿主机自启）
python3 flash.py systemd --skill <name> [--user] [--output <path>] [--restart-sec 5]

# Standalone：所有命令都支持 --skill-dir / --data-dir 全局 flag
python3 flash.py --skill-dir /path/to/skills --data-dir /path/to/data create --skill <name>
```

---

## 持久化目录（K8s Pod 容器友好）

| 数据 | 默认位置 | 环境变量覆盖 |
|---|---|---|
| **flash 项目数据**（projects.json / jobs.jsonl / PID）| `<workspace>/.skill-to-http-flash/` | `FLASH_DATA_DIR`、`OPENCLAW_FLASH_DATA_DIR` |
| **证书 / API Key** | `<workspace>/.http/` | `OPENCLAW_HTTP_ROOT` |
| **Skill 搜索路径** | `~/.openclaw/workspace/skills/`、`~/.claude/skills/`、`~/.cursor/skills/`、`~/.config/skills/`、`./skills/`、`/app/skills/` | `FLASH_SKILL_DIR` |

兜底（非 OpenClaw 环境）：`~/.skill-to-http-flash/`、`~/.http/`

> ⚠️ K8s Pod：`~/` 下非 workspace 目录可能不挂 PVC，重启丢密钥/证书/历史。默认存 workspace 内能规避（PVC 一定持久化）。

---

## TLS / HTTPS

**默认 HTTP**（零门槛跑通）。create 时可选启用 HTTPS（自签 SAN 证书）。

```bash
# create 时启用
python3 flash.py create --skill foo
# Enable HTTPS? [y/N]: y

# 已有 project 切换
python3 flash.py recreate --skill foo --tls-enabled
python3 flash.py recreate --skill foo --no-tls

# 运行时临时切换（不重生代码）
FLASH_TLS_ENABLED=1 python3 server.py start

# 导入公司颁发的正式证书
python3 flash.py cert --skill foo --cert-action import \
    --cert-src server.crt --key-src server.key
```

证书路径：`<HTTP_ROOT>/certs/flash-<skill>/server.{crt,key}`，自动 SAN 嗅探本机 IP，有效期 365 天。

---

## 鉴权

可选 API Key（`X-API-Key` header，与 skill-to-http / agent-easy-http 对齐）：

```bash
# 启用方式
FLASH_API_KEY=mysecret python3 server.py start          # env
echo -n "mysecret" > <HTTP_ROOT>/secrets/api-keys/flash-<skill>.key  # 文件（0600）

# 调用
curl -H 'X-API-Key: mysecret' http://...:7780/run -d '{...}'
```

未设置不做认证（仅适合内网受信测试）。公网部署请走前置反代 + 公认证书。

---

## CORS

默认 `Access-Control-Allow-Origin: *`（无 credentials）。收紧：

```bash
FLASH_CORS_ALLOW_ORIGINS="https://your-tool.com,https://other.com" python3 server.py start
```

---

## 生成的项目结构

```
output/<skill-name>-api/
├── server.py           # 独立 FastAPI 服务（~1150 行）
├── params.json         # 入参 schema
├── requirements.txt    # fastapi / uvicorn / cryptography / pydantic / jsonschema
├── start.sh            # 后台启动
├── stop.sh             # 停止
├── restart.sh          # 重启
└── README.md           # 接口文档
```

`server.py` 完全自包含（内嵌 cert / job store / argv builder / envelope），可 scp 到任何机器跑。

---

## 与 skill-to-http 的关系（更新）

| 维度 | skill-to-http | skill-to-http-flash v2.0 |
|---|---|---|
| 服务模型 | 多 Skill 统一网关 | **单 Skill 独立 subprocess 微服务** |
| Schema | 运行时动态（LLM 生成） | **生成时固化（JSON Schema 校验）** |
| 执行引擎 | sessions_spawn + LLM | **subprocess.run() 直调** |
| 启动延迟 | 30s+ (LLM 链路) | **<2s** |
| 复现性 | LLM 漂移 | **100% 确定性** |
| 依赖 | Gateway + LLM | **无外部依赖** |

flash v2.0 **不再依赖 skill-to-http**（v1.x 自动安装逻辑已删除）。

---

## 参考文档

- `references/migration-from-v1.md` — v1 用户如何 recreate
- `references/standalone-usage.md` — 非 OpenClaw 环境完整使用指南

---

## 适用场景

- **HTML 工具站**通过 fetch 调 skill 拿结构化数据
- **CI/CD pipeline** 步骤里 curl skill 当成"可复用脚本服务"
- **跨服务调用**：服务 A 想调服务 B 的某个 skill
- **本地脚本快速变 REST API**：argparse 写好后立即变 HTTP 接口

---

## 不适用场景（v2.0 第一版边界）

- ❌ 入口是 shell `.sh`（包一层 Python launcher）
- ❌ 需要 LLM 自然语言"理解后取数"（用 skill-to-http 或 agent-easy-http）
- ❌ stdout 包含人交互式 UI（如 TUI）
- ❌ 需要长连接 / SSE / WebSocket

---

## Changelog

### v2.0.3
- **文档**：README 改为 runtime-中立表述，OpenClaw / Claude Code / Cursor / standalone 平等对待（此前 Install 表偏 OpenClaw）

### v2.0.2
- **多 agent 兼容**：skill 目录探测新增 Claude Code (`~/.claude/skills`) / Cursor (`~/.cursor/skills`) / 通用 XDG (`~/.config/skills`) / 项目本地 (`./skills`) 兜底，非 OpenClaw runtime 开箱即用无需手设 env
- **文档一致性修复**：明确「运行期零 LLM、生成期可选 LLM 提参（未配置走 fallback）」，消除「不调 LLM」与 create 期 schema 提取仍调 LLM 的表述冲突
- **优雅退出修复**：生成的 `server.py` lifespan 退出不再 `os._exit(0)`（原会绕过 atexit/finally/日志 flush，可能截断 JSONL 落盘），改为让 uvicorn 自然走完关闭流程
- **安全加固**：API Key 校验改用 `hmac.compare_digest` 恒定时间比较（防 timing attack）；401 响应不再回显 header 名
- **健壮性**：`flash.py list` 的 stale 判断异常捕获从冗余的 `(OSError, Exception)` 收敛为 `(OSError, ValueError, JSONDecodeError)`
- **新增可配置项**：异步并发上限支持 `FLASH_MAX_ASYNC` env 覆盖（默认 20）

### v2.0.1
- PVC 持久化路径、TLS/鉴权/CORS、异步 job store、SQLite 导出等（详见正文）

