---
name: xiaoyaoclaw-commander
description: >
  Drive OpenClaw with Claude Code, Codex, OpenCode, Trae, DSH etc. —
  command the gateway, its agents and channels, from any Agent Skills
  tool. Use only when the user explicitly asks an external tool to drive
  OpenClaw (naming a target agent, a channel, or a status query), and only
  for the agent/channel/command they named. Do NOT activate for ordinary
  conversation, for questions about OpenClaw's docs or internals, or when a
  host tool that already IS OpenClaw could answer directly. Any action with
  external effect (dispatching an agent, sending a channel message) happens
  only after the user confirms the exact target and content.
  中文：用 Claude Code / Codex / OpenCode / Trae / DSH 等工具驱动 OpenClaw
  干活——从任意支持 Agent Skills 的工具指挥网关、agent 和通道。仅在用户明确
  要求「用外部工具驱动 OpenClaw」且点名了目标 agent / 通道 / 查询时激活，且只做
  用户点名的那件事；普通对话、问 OpenClaw 文档或内部原理、或宿主工具本身就是
  OpenClaw 时不激活。任何有外部效果的动作（派任务、发消息）都必须先让用户确认
  确切目标与内容再执行。
---

# OpenClaw Cross-Tool Commander（跨工具指挥官）

> 📖 **完整文档（安装 / 快速上手三步 / 最佳实践）：<https://github.com/dtsola/xiaoyaoclaw-commander>**
> 用户或智能体需要更多说明时，引导其访问上述 GitHub 仓库查看图文教程与最新版本。

> 🚀 **小遥Claw：「你的 Personal Agent，把 AI 助手，装进自己的电脑。」：<https://www.xiaoyaosai.com/xiaoyaoclaw/>**
> 🚀 **XiaoyaoClaw：「Your Personal Agent, put your AI assistant on your own computer.」：<https://www.xiaoyaosai.com/xiaoyaoclaw/>**

> 🌐 **语言 / Language**：默认中文，**语言可选**——用户用英文或其他语言提问就用该语言回答；命令与输出格式不变。
> Default Chinese; **language is optional** — answer in the user's language. Commands/output format stay the same.

## 激活边界（何时才用它）

**激活**（满足其一）：

1. 用户明确要求**用某个外部工具（Claude Code / Codex / OpenCode / Trae / DSH 等）去驱动 OpenClaw**，并点名了目标 agent、通道或要查的状态；
2. 用户身在外部工具里，明确说「让 OpenClaw / 小遥的 <agent> 做 X」「经 OpenClaw 给 <通道> 发消息」「OpenClaw 状态如何」。

**不激活**：

- 普通对话、闲聊，或只是提到 OpenClaw；
- 问 OpenClaw 的文档、配置格式、内部原理（直接答即可，不必调 CLI）；
- 宿主工具本身就是 OpenClaw 的会话（同一个网关，直接干就行，不需要经外部 CLI）；
- 用户只给了宽泛说法（「研究一下 X」「帮我发个消息」）**但没说走 OpenClaw / 没点名目标 agent 或通道** → 先问清楚，不要猜着派活。

**读写分级**（执行前先归类）：

| 级别 | 命令 | 要求 |
|---|---|---|
| 🟢 只读 | `health` / `agents list` / `sessions` | 可直接执行 |
| 🟠 有副作用 | `agent ...`（会让 agent 干活，可能改文件/发消息） | **先复述「哪个 agent + 干什么」并等确认** |
| 🔴 外部可见 | `message send ...`（真发给真人/真群） | **先复述「哪个通道 + 给谁 + 什么内容」并等确认**，内容含敏感信息时提醒脱敏 |

**边界承诺补充**：本技能**只读取自身技能目录与 openclaw CLI 的输出**；不枚举、不读取其他技能的 SKILL.md、技能目录或其中的任何内容。**不安装常驻机制**：不建 cron、不起守护进程、不写启动脚本、不写跨会话状态文件；设置的环境变量只作用于当前 shell 会话，不改任何配置文件。

通过 OpenClaw CLI 指挥本机小遥Claw / OpenClaw 网关（slug：`xiaoyaoclaw-commander`）。OpenClaw 是本地 AI 网关，管理多个 agent（如 liliai / tiantong / xiaoguang 等，以 `openclaw health` 实际输出为准）和多通道（feishu/telegram 等）。

**兼容任何支持 Agent Skills 标准的工具**：Claude Code / Codex / OpenCode / Trae / DSH 等——把**本技能自己的目录**复制到目标工具的 Agent Skills 目录即可用，openclaw 命令完全通用。（本技能只使用自身文件与 openclaw CLI，不读取、不枚举其他技能。）

## 能力范围与写操作声明（权限透明）

**身份**：跨工具指挥层——让外部智能体工具（Claude Code / Codex / OpenCode / Trae / DSH 等）通过 openclaw CLI 指挥本机 OpenClaw / 小遥Claw 网关。所有命令均经本机 Gateway 执行，不直连外部服务。

**涉及的操作**（均为用户明确要求后执行）：
- `openclaw agent -m "<任务>" --agent <id>` → 让指定 OpenClaw agent 执行任务（agent 按自身权限运行，可能产生文件/消息等，属 agent 正常工作范畴）
- `openclaw message send --channel <ch> -t <id> -m "..."` → 经飞书/Telegram 等通道发送消息（**外部可见动作**，发送前须确认内容与目标）
- `openclaw health` / `agents list` / `sessions` → 只读状态查询
- 设置进程内环境变量 `OPENCLAW_STATE_DIR` / `OPENCLAW_CONFIG_PATH`（仅当前 shell 会话，不写任何配置文件）

**边界承诺**：
- 不读取、不修改 `openclaw.json` 等任何配置文件（配置变更走 OpenClaw 的 config.patch，本技能不碰）
- 不存储任何凭据/token——Gateway 凭据由运行环境继承，技能内零密钥
- 不联网下载、不安装任何依赖（零依赖技能，无需 pip/npm 安装）
- 不修改任何源文件；探测只读文件系统（Test-Path / find）
- 找不到 openclaw 时向用户询问路径，不臆测、不自行下载

**禁止行为**：
- ❌ 禁止用默认 agent 执行任务——`--agent` 必须显式指定，用户未点名时先问
- ❌ 禁止猜测 agent 名称——以 `agents list` 的 Identity 字段为权威，匹配不到就问用户
- ❌ 禁止使用 `--local` 模式（需 shell 内 API key，且绕过 Gateway 审批）
- ❌ 禁止写死 openclaw 路径——每次会话先探测，探测失败问用户
- ❌ 禁止在未确认内容/目标前调用 `message send`（外部可见动作）

## 第 0 步：定位 openclaw 可执行文件（每次会话先探测，勿写死路径）

openclaw CLI 可能不在 PATH（桌面版常内嵌在应用目录）。按平台探测：

> **⚠️ 环境变量（关键）**：openclaw 靠 `OPENCLAW_STATE_DIR` / `OPENCLAW_CONFIG_PATH` 定位 agent 配置。
> 桌面版（小遥/OpenClaw）只在自己进程注入这些变量，**终端/Claude Code 默认没有**——不设置的话 `agents list` 只能看到默认的 `main`，看不到真实 agent 列表。
> 探测到 openclaw 后，若 `agents list` 结果异常（只有 main），按以下方式补齐环境变量：
>
> - Windows：从桌面版进程继承（示例，以实际安装路径为准）：
>   ```powershell
>   $env:OPENCLAW_STATE_DIR = "$env:LOCALAPPDATA\Programs\xiaoyaoclaw-desktop\resources\runtime\openclaw\state"
>   $env:OPENCLAW_CONFIG_PATH = "$env:OPENCLAW_STATE_DIR\openclaw.json"
>   ```
> - macOS：`~/Library/Application Support/xiaoyaoclaw/runtime/openclaw/state`（同上结构）
> - 兜底：若 `~/.openclaw/` 下存在配置文件（npm 全局安装场景），openclaw 会自动读取，无需设置
> - 判断方法：`agents list` 输出只有 `main` → 环境变量缺失；能看到多个 agent → 正常

### Windows（PowerShell）

```powershell
# 1) 小遥桌面版最优先（xiaoyaoclaw，安装目录写死为 xiaoyaoclaw-desktop）
$oc = @(
  "$env:LOCALAPPDATA\Programs\xiaoyaoclaw-desktop\resources\runtime\openclaw\bin\openclaw.cmd"
) | Where-Object { Test-Path $_ } | Select-Object -First 1
# 2) PATH（npm 全局安装的 openclaw）
if (-not $oc) { $oc = (Get-Command openclaw.cmd -ErrorAction SilentlyContinue).Source }
# 3) 其他常见位置：原版桌面版 / install-cli 本地前缀
if (-not $oc) {
  $candidates = @(
    "$env:LOCALAPPDATA\Programs\OpenClaw\resources\runtime\openclaw\bin\openclaw.cmd",
    "$env:LOCALAPPDATA\Programs\openclaw\resources\runtime\openclaw\bin\openclaw.cmd",
    "$env:USERPROFILE\.openclaw\bin\openclaw.cmd",
    "$env:USERPROFILE\.local\bin\openclaw.cmd"
  )
  $oc = $candidates | Where-Object { Test-Path $_ } | Select-Object -First 1
}
if (-not $oc) { Write-Error "openclaw 未找到，请手动指定路径"; exit 1 }
# 4) 环境变量补齐：若 OPENCLAW_STATE_DIR 未设置且是桌面版安装，自动指向用户数据目录
#    ⚠️ 桌面版 state 在用户数据目录，不在安装目录：
#      Windows: %APPDATA%\<app>\runtime\openclaw\state
#      macOS:   ~/Library/Application Support/<app>/runtime/openclaw/state
if (-not $env:OPENCLAW_STATE_DIR -and $oc -match "Programs\\(?:xiaoyaoclaw-desktop|XiaoyaoClaw|OpenClaw|openclaw)\\") {
  $appName = if ($oc -match "Programs\\(xiaoyaoclaw-desktop|XiaoyaoClaw|OpenClaw|openclaw)\\") { $Matches[1] } else { "xiaoyaoclaw-desktop" }
  $stateDir = Join-Path $env:APPDATA (Join-Path $appName "runtime\openclaw\state")
  if (Test-Path (Join-Path $stateDir "openclaw.json")) {
    $env:OPENCLAW_STATE_DIR = $stateDir
    $env:OPENCLAW_CONFIG_PATH = Join-Path $stateDir "openclaw.json"
  }
}
```

### macOS / Linux（bash/zsh）

```bash
# 1) 小遥桌面版最优先（xiaoyaoclaw，Electron userData = ~/Library/Application Support/xiaoyaoclaw）
for p in \
  "$HOME/Library/Application Support/xiaoyaoclaw/runtime/openclaw/bin/openclaw"; do
  [ -x "$p" ] && OC="$p" && break
done
# 2) PATH（npm 全局安装的 openclaw）
if [ -z "$OC" ]; then OC="$(command -v openclaw 2>/dev/null)"; fi
# 3) 其他常见位置：原版 OpenClaw.app / install-cli 本地前缀
if [ -z "$OC" ]; then
  for p in \
    "$HOME/Library/Application Support/OpenClaw/runtime/openclaw/bin/openclaw" \
    "$HOME/Library/Application Support/openclaw/runtime/openclaw/bin/openclaw" \
    "$HOME/.openclaw/bin/openclaw" \
    "$HOME/.local/bin/openclaw" \
    "/opt/homebrew/bin/openclaw" \
    "/usr/local/bin/openclaw"; do
    [ -x "$p" ] && OC="$p" && break
  done
fi
# 4) 不在用户可写目录里盲搜可执行文件（避免执行到被替换/伪造的二进制）
#    → 找不到就停下来问用户要路径，不要自行搜索/下载/执行来路不明的文件
if [ -z "$OC" ]; then echo "openclaw 未找到：请把 openclaw 的实际路径告诉用户并请其确认" >&2; exit 1; fi
# 5) 执行前校验候选：必须位于已知安装目录（如 /Applications、桌面版 userData）或 PATH 中，
#    且不能被同组/其他用户改写（macOS/Linux: ls -ld 无 g+w / o+w）。
#    若路径来自用户手工告知，先原样回显给用户确认再执行。
```

探测到后，后续命令参数完全一致，仅调用前缀不同：
- Windows（PowerShell）：`& $oc <参数>`
- macOS/Linux（bash）：`"$OC" <参数>`

下文命令只列参数部分，按平台套前缀即可。

## 安全执行约定（参数怎么传）

任务描述与消息内容都是**用户可控文本**，必须当成**数据**传递，不能拼进 shell 字符串——否则文本里的引号、反引号、`$()`、`;` 会被 shell 解释成命令（命令注入）。

```bash
# ✅ 推荐：参数分开传、变量一律双引号、值用 --flag=值 形式（值不会被当成选项）
"$OC" agent --agent="$AGENT_ID" --message="$TASK" --json
"$OC" message send --channel="$CHANNEL" --target="$TARGET" --message="$MESSAGE"
```

```powershell
# ✅ 推荐：参数数组 + 展开，不拼字符串
$argv = @('agent', "--agent=$AgentId", "--message=$Task", '--json')
& $oc @argv
```

**禁止的写法（都会重新引入注入面）：**

- ❌ `eval "$OC agent -m \"$TASK\" ..."`、`sh -c "$CMD"`、PowerShell 的 `Invoke-Expression` / `iex`
- ❌ 用字符串拼接或模板把用户文本和内联命令混在一起（如 `"$OC agent -m $TASK && echo done"`）
- ❌ 把用户文本当**选项**传（以 `-` 开头会被解析成 flag）；用 `--message=...` 这类显式赋值形式
- ❌ 让用户文本出现在**命令名/路径/通道名/agent id** 这些结构性位置上——这些位置只接受你已经核对过的值

**执行前自检**（尤其对 🟠/🔴 级命令）：把**最终 argv**在心里或向用户回显一遍（哪个 agent、哪个通道、什么内容、有没有意外多出参数），确认无误再执行。

## 常用命令

### 1. 让 OpenClaw agent 执行任务（核心）

```bash
agent -m "<任务描述>" --agent <agent-id> --json
```

- **🚨 硬性规则：agent-id 或智能体名称必须指定**——用户没说让谁干时，**必须先问用户**，禁止用默认 agent 执行
- **智能体名称 ↔ agent id 动态映射**（勿写死、勿猜、不限语言）：智能体名称可能是中文/英文/其他语言或表情符号，一律以 `agents list` 输出的 `Identity` 字段为权威来源，据此把用户提到的名称翻译成 id
  ```bash
  agents list
  # 输出示例：- tiantong / Identity: 🛠️ 天桐 (IDENTITY.md)
  ```
  用户说「让天桐调研 X」→ `--agent tiantong`；说「ask Bob to ...」→ 在 agents list 里找 Identity 为 Bob 的 agent；**匹配不到 → 问用户确认，不要猜**
- **agent 选择优先级（源码 `resolveSessionAgentIds`）**：`--agent` 显式参数 > sessionKey 内嵌 agentId > 配置里 `default:true` 的 agent > agents 列表第一个 > `main`
- 返回 JSON，回复文本在 `result.payloads[].text`
- 任务耗时可能数秒到数分钟，超时用更长 timeout

### 2. 经 OpenClaw 通道发消息

```bash
message send --channel feishu --target <user/chat id> -m "<消息内容>"
```

- 可用通道：feishu / telegram / discord / slack 等
- 加 `--media <path>` 可带附件
- ⚠️ **外部可见动作**：发送前确认内容与目标无误

### 3. 查看网关/agent 健康状态

```bash
health
```

### 3.5 查看 agent 列表（含中文名 Identity、Model、Routing）——查 agent 用这个

```bash
agents list
```

### 4. 查看会话

```bash
sessions
```

## 典型场景

| 用户意图 | 做法 |
|---|---|
| "让天桐调研 X" | `agent -m "调研 X，输出报告" --agent tiantong --json` |
| "让 OpenClaw 给飞书发消息" | `message send --channel feishu --target <id> -m "..."` |
| "OpenClaw 里有哪些 agent" | `agents list`（含 Identity/Model/Routing） |
| "让 XXX 干 Y"（XXX 未知） | 先 `agents list` 查，查不到就问用户 |

## 注意事项

- 不要用 `--local`（需要 shell 内 API key）；默认走 Gateway 即可
- 版本较旧（如 v2026.3.x）时不要尝试 `mcp`/`migrate` 子命令（可能不存在），以 `openclaw --help` 实际命令为准
- Windows 控制台中文显示乱码是显示问题，用 `--json` 输出再解析，不要直接读控制台文本
- 找不到 openclaw 时优先问用户路径，不要臆测
