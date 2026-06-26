---
name: setup-openviking-remote
description: >
  Install and configure the OpenViking long-term memory plugin for OpenClaw via natural conversation.
  Covers the full lifecycle: environment check, plugin install, remote-mode config, health verification, and gateway activation.
  Trigger when the user says any of: "install OpenViking", "set up memory", "configure memory plugin",
  "帮我装 OpenViking", "配置记忆插件", "安装记忆功能", "connect to OpenViking server",
  or shares a link/URL containing this skill.
  The user does NOT need to know any CLI commands — the agent handles everything.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - node
        - openclaw
        - curl
    emoji: "🦣"
    homepage: "https://github.com/volcengine/OpenViking"
tags:
  - install
  - setup
  - memory
  - openviking
---

# Setup OpenViking Remote — Agent Installation Skill

You are about to help a user install and configure the OpenViking memory plugin for OpenClaw.
The user does NOT know how to use a terminal. You will collect information through conversation, then run all commands yourself using your shell/terminal tool.

**Read this entire document before starting. Follow every step in order. Do NOT skip steps.**

---

## STEP 0: Detect Language

If the user's message is in Chinese, respond in Chinese throughout.
If in English, respond in English throughout.
All example messages below are given in both languages — use the matching one.

---

## STEP 1: Detect Operating System

Run this command silently (do NOT show it to the user):

```bash
uname -s 2>/dev/null || echo WINDOWS
```

- If output contains `Darwin` → this is **macOS**. Set `OS=mac`.
- If output contains `Linux` → this is **Linux**. Set `OS=linux`.
- If output is `WINDOWS` or the command fails → this is **Windows**. Set `OS=windows`.

Remember the OS for later steps. Do NOT tell the user about this step.

---

## STEP 2: Check Prerequisites

Run these commands silently:

```bash
node -v
openclaw --version
```

**If `node` is not found:**
Tell the user:
> (CN) 你的系统没有安装 Node.js。OpenClaw 和 OpenViking 插件需要 Node.js >= 22。请先安装 Node.js，然后再来找我。
> (EN) Node.js is not installed. OpenClaw requires Node.js >= 22. Please install it first.

**Stop here. Do NOT continue.**

**If `openclaw` is not found:**
Tell the user:
> (CN) 你的系统没有安装 OpenClaw。请先安装 OpenClaw >= 2026.3.7，然后再来找我。
> (EN) OpenClaw is not installed. Please install OpenClaw >= 2026.3.7 first.

**Stop here. Do NOT continue.**

**If both exist:** proceed silently to Step 3.

---

## STEP 3: Greet and Explain

Send this message to the user:

> (CN) 好的，我来帮你配置 OpenViking 长期记忆功能！配置好之后，我会自动记住我们对话中的重要信息，下次聊天也能回忆起来。
>
> 我需要你提供以下信息（如果不确定，可以问你的管理员要）：
> 1. **OpenViking 服务地址** — 比如 `https://ov.example.com` 或 `http://192.168.1.100:1933`
> 2. **API Key** — 用于身份验证（如果服务没有开认证，可以留空）
> 3. **Agent 标识** — 你希望我在 OpenViking 里叫什么名字？（留空我就用 `default`）
>
> 先告诉我服务地址吧？

> (EN) I'll set up OpenViking long-term memory for you! Once configured, I'll automatically remember important information from our conversations and recall it in future chats.
>
> I need 3 pieces of information (ask your admin if unsure):
> 1. **OpenViking server URL** — e.g. `https://ov.example.com` or `http://192.168.1.100:1933`
> 2. **API Key** — for authentication (leave blank if no auth)
> 3. **Agent identifier** — what should I call myself in OpenViking? (blank = `default`)
>
> What's the server URL?

---

## STEP 4: Collect Information

Collect these 3 values from the user one by one, through natural conversation. Be patient. If the user gives multiple values at once, parse them all.

### 4a. Endpoint (REQUIRED)

The user must provide this. Validate format:
- Must start with `http://` or `https://`
- Must not end with `/health` or `/api` (strip trailing path if present)
- Strip any trailing `/`

If the user gives something like `ov.example.com` without protocol, prepend `https://`.

If the user says they don't know, suggest they ask their admin. Do NOT make up a URL.

Store as `ENDPOINT`.

### 4b. API Key (OPTIONAL)

Ask:
> (CN) API Key 是什么？如果服务没有认证要求，直接说"没有"或"空"就行。
> (EN) What's the API Key? Say "none" or "skip" if the server has no authentication.

If user says "没有"/"空"/"none"/"skip"/"no"/empty → set `API_KEY` to empty string.
Otherwise store whatever they give as `API_KEY`.

### 4c. Agent ID (OPTIONAL)

Ask:
> (CN) 你希望这个 Agent 在 OpenViking 里叫什么名字？直接回车或说"默认"就用 `default`。
> (EN) What should this agent be called in OpenViking? Press enter or say "default" to use `default`.

If user says "默认"/"default"/empty → set `AGENT_ID` to `default`.
Otherwise store their answer as `AGENT_ID`.

---

## STEP 5: Validate Connection

Tell the user you're checking the connection, then run:

> (CN) 好，让我先测试一下能不能连上你的 OpenViking 服务...
> (EN) Let me test the connection to your OpenViking server...

Run this command:

**If OS=windows:**
```powershell
Invoke-WebRequest -Uri "ENDPOINT/health" -TimeoutSec 10 -UseBasicParsing | Select-Object -ExpandProperty StatusCode
```

**If OS=mac or OS=linux:**
```bash
curl -sS -o /dev/null -w "%{http_code}" --connect-timeout 10 "ENDPOINT/health"
```

Replace `ENDPOINT` with the actual value.

**If the result is `200`:**
Tell the user:
> (CN) ✅ 连接成功！服务正常运行。
> (EN) ✅ Connection successful! Server is running.

Proceed to Step 6.

**If the result is `401` or `403`:**
Tell the user:
> (CN) ❌ 服务器返回了认证错误（401/403）。请确认你的 API Key 是否正确。
> (EN) ❌ Server returned auth error (401/403). Please check your API Key.

Go back to Step 4b and ask for the API Key again.

**If the result is anything else, or the command fails/times out:**
Tell the user:
> (CN) ❌ 无法连接到 ENDPOINT。可能的原因：
> - 服务地址输入有误
> - 服务还没有启动
> - 网络不通（防火墙、VPN 等）
>
> 请检查后告诉我正确的地址，或者确认服务已启动。
> (EN) ❌ Cannot connect to ENDPOINT. Possible causes:
> - Wrong URL
> - Server not running
> - Network issue (firewall, VPN, etc.)
>
> Please verify and give me the correct URL, or confirm the server is running.

Go back to Step 4a and ask for the endpoint again. Do NOT proceed until the health check passes.

---

## STEP 6: Install Plugin

Tell the user:
> (CN) 连接没问题，现在开始安装插件...
> (EN) Connection verified, installing the plugin now...

Run this command:

```bash
openclaw plugins install clawhub:@openclaw/openviking
```

**If the command succeeds (exit code 0):**
Proceed to Step 7.

**If the output contains "already installed" or similar:**
That's fine, proceed to Step 7.

**If the command fails:**
Tell the user the error and suggest:
> (CN) 插件安装失败。请检查网络连接。如果问题持续，尝试手动运行这个命令：`openclaw plugins install clawhub:@openclaw/openviking`
> (EN) Plugin installation failed. Check your network. If the issue persists, try running: `openclaw plugins install clawhub:@openclaw/openviking`

**Stop here. Do NOT continue until the plugin is installed.**

---

## STEP 7: Configure Plugin

Run these commands one by one. **Each command must succeed before running the next one.**

### 7a. Set mode to remote
```bash
openclaw config set plugins.entries.openviking.config.mode remote
```

### 7b. Set the endpoint
```bash
openclaw config set plugins.entries.openviking.config.baseUrl ENDPOINT
```
Replace `ENDPOINT` with the actual URL (e.g. `https://ov.example.com`).

### 7c. Set API Key (ONLY if API_KEY is not empty)
```bash
openclaw config set plugins.entries.openviking.config.apiKey API_KEY
```
Replace `API_KEY` with the actual key.

**If API_KEY is empty, SKIP this command entirely. Do NOT run it with an empty value.**

### 7d. Set Agent ID
```bash
openclaw config set plugins.entries.openviking.config.agentId AGENT_ID
```
Replace `AGENT_ID` with the actual value (e.g. `default`).

### 7e. Activate the context engine slot
```bash
openclaw config set plugins.slots.contextEngine openviking
```

If ANY of these commands fail, tell the user the specific error and stop.

---

## STEP 8: Source Environment and Restart Gateway

### 8a. Source environment file (if it exists)

**If OS=windows:**
Check if the file exists first:
```powershell
Test-Path "$HOME/.openclaw/openviking.env.ps1"
```
If it exists, run:
```powershell
. "$HOME/.openclaw/openviking.env.ps1"
```

**If OS=mac or OS=linux:**
Check if the file exists first:
```bash
test -f ~/.openclaw/openviking.env && source ~/.openclaw/openviking.env
```

If the env file does not exist, that's OK for remote mode. Skip and continue.

### 8b. Restart gateway

```bash
openclaw gateway restart
```

If `gateway restart` fails, try:
```bash
openclaw gateway --force
```

If both fail, tell the user:
> (CN) Gateway 重启失败。请手动运行 `openclaw gateway restart`。
> (EN) Gateway restart failed. Please manually run `openclaw gateway restart`.

Wait 3 seconds after restart before proceeding to verification.

---

## STEP 9: Verify Installation

Run:
```bash
openclaw config get plugins.slots.contextEngine
```

**If output is `openviking`:**
Installation is successful! Tell the user:

> (CN) 🎉 全部搞定！OpenViking 记忆插件已经安装并配置完成。
>
> 从现在开始，我会：
> - **自动记忆**：对话中的重要信息会被自动保存
> - **自动回忆**：回复前会自动搜索相关记忆
> - **跨会话**：下次聊天也能记住之前的内容
>
> 你可以试着说"记住我的邮箱是 xxx@example.com"来测试一下！

> (EN) 🎉 All done! OpenViking memory plugin is installed and configured.
>
> From now on, I will:
> - **Auto-remember**: Important info from conversations is saved automatically
> - **Auto-recall**: Relevant memories are searched before each response
> - **Cross-session**: I'll remember things from previous chats
>
> Try saying "Remember my email is xxx@example.com" to test it!

**If output is NOT `openviking`:**
Tell the user:
> (CN) ⚠️ 插件似乎没有正确激活。让我检查一下日志...
> (EN) ⚠️ Plugin doesn't seem to be activated correctly. Let me check the logs...

Then run:
```bash
openclaw logs 2>&1 | tail -20
```

Show the last 20 lines of logs to the user and suggest they contact support.

---

## ERROR RECOVERY REFERENCE

Use this table if you encounter errors at any step:

| Error Message | Likely Cause | Fix |
|---------------|-------------|-----|
| `command not found: openclaw` | OpenClaw not installed | Ask user to install OpenClaw first |
| `command not found: node` | Node.js not installed | Ask user to install Node.js >= 22 |
| `ECONNREFUSED` or `connection refused` | Server not running | Ask user to verify server is running |
| `ETIMEDOUT` or `timeout` | Network issue | Ask user to check firewall/VPN/URL |
| `401 Unauthorized` | Wrong API Key | Ask user to re-enter API Key |
| `403 Forbidden` | API Key lacks permissions | Ask user to check permissions with admin |
| `404 Not Found` on /health | Wrong URL or old server version | Ask user to verify URL |
| `ENOTFOUND` or `DNS` error | Invalid domain name | Ask user to check the URL |
| `plugins install` fails with network error | npm/ClawHub unreachable | Ask user to check internet connection |
| `config set` returns error | OpenClaw config locked or corrupted | Ask user to run `openclaw config check` |
| Gateway won't start | Port conflict or other process | Run `openclaw logs` and share with user |

---

## IMPORTANT RULES

1. **NEVER ask the user to run commands themselves.** You run everything.
2. **NEVER skip the health check (Step 5).** If the server is unreachable, do NOT proceed.
3. **NEVER proceed past a failed step.** Fix or report every error before moving on.
4. **ALWAYS use the exact commands shown.** Do not improvise or combine commands.
5. **ALWAYS replace placeholders** (`ENDPOINT`, `API_KEY`, `AGENT_ID`) with actual values before running commands.
6. **If a step is marked as "proceed silently"**, do NOT show the command or its output to the user unless there is an error.
7. **Be encouraging and patient.** The user may not understand technical terms. Explain in simple words.
