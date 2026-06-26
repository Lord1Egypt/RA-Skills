---
name: wechat-auto-reply
description: "Monitor WeChat for new messages from specific contacts and auto-reply. Supports macOS (Peekaboo CLI) and Windows (PeekabooWin). Requires Peekaboo CLI on macOS or PeekabooWin on Windows."
description_zh: "监控微信指定联系人的新消息并自动回复。支持 macOS (Peekaboo CLI) 和 Windows (PeekabooWin)。智能等待，已回复检测。"
description_en: "Monitor WeChat for new messages from specific contacts and auto-reply. Cross-platform: macOS + Windows."
---

# WeChat Auto Reply (Cross-Platform v5)

Monitor WeChat for new messages from **any specified contact** and auto-reply.
Supports **macOS** (Peekaboo CLI) and **Windows** (PeekabooWin).

---

## Prerequisites

### macOS (Apple Silicon / Intel)

1. **Peekaboo CLI** installed:
   ```bash
   brew install steipete/peekaboo/peekaboo
   ```
2. **Permissions granted**: Screen Recording + Accessibility
   ```bash
   peekaboo permissions
   ```
3. **WeChat** running and visible on screen

### Windows (10 / 11)

1. **Node.js 22+** installed: https://nodejs.org
   ```powershell
   node --version   # 确认 >= v22.0.0
   ```
2. **PeekabooWin** installed:
   ```powershell
   git clone https://github.com/FelixKruger/PeekabooWin
   cd PeekabooWin
   npm install
   npm test
   ```
3. **Set environment variable** (告诉脚本 PeekabooWin 在哪里):
   ```powershell
   # 临时设置（当前 PowerShell 窗口有效）
   $env:PEEKABOO_WIN_DIR = "C:\Users\<你的用户名>\PeekabooWin"

   # 永久设置（推荐）
   [System.Environment]::SetEnvironmentVariable("PEEKABOO_WIN_DIR", "C:\Users\<你的用户名>\PeekabooWin", "User")
   ```
4. **WeChat** (微信) running and **visible on screen** (不能最小化)
5. **Windows permissions**:
   - 部分操作可能需要以管理员身份运行 PowerShell
   - 确保微信窗口未被"专注助手"屏蔽

### Python

- **Python 3.7+** (macOS 和 Windows 均需要)
- 脚本仅使用标准库，无需额外 pip 安装

---

## Quick Start

### Step 0: Platform Detection & Prerequisite Check

When the user invokes this skill for the first time, **always** run the prerequisite check first. Do NOT start monitoring until all prerequisites are confirmed.

**Run these checks using Bash tool:**

```bash
# 1. Detect platform
echo "PLATFORM: $(uname -s 2>/dev/null || echo Windows)"

# 2. Check Python
python3 --version 2>/dev/null || python --version 2>/dev/null
```

#### If macOS (`Darwin`):

```bash
# Check Peekaboo CLI
which peekaboo && peekaboo version

# Check permissions
peekaboo permissions
```

**If Peekaboo NOT found**, show this message to the user:

> **Peekaboo CLI 未安装，请先执行以下命令：**
> ```bash
> brew install steipete/peekaboo/peekaboo
> ```
> 安装后还需要授予权限：
> 1. 打开 **系统设置 → 隐私与安全 → 屏幕录制** → 勾选 Peekaboo
> 2. 打开 **系统设置 → 隐私与安全 → 辅助功能** → 勾选 Peekaboo
>
> 安装完成后对我说"监控 XX 的微信"即可。

**If permissions NOT granted**, show:

> **权限未完全授予，请打开以下设置：**
> 1. 系统设置 → 隐私与安全 → 屏幕录制 → 勾选 Peekaboo
> 2. 系统设置 → 隐私与安全 → 辅助功能 → 勾选 Peekaboo
>
> 授权后重新运行 `peekaboo permissions` 确认。

#### If Windows:

```powershell
# Check Node.js version (must be >= 22)
node --version

# Check PEEKABOO_WIN_DIR environment variable
echo $env:PEEKABOO_WIN_DIR

# Check PeekabooWin exists
if (Test-Path "$env:PEEKABOO_WIN_DIR\bin\peekaboo-win.js") { echo "PeekabooWin: FOUND" } else { echo "PeekabooWin: NOT FOUND" }

# Verify PeekabooWin works
node "$env:PEEKABOO_WIN_DIR\bin\peekaboo-win.js" --help 2>$null
```

**If Node.js NOT found or version < 22**, show this message:

> **Node.js 未安装或版本过低，请按以下步骤操作：**
>
> **第 1 步：安装 Node.js 22+**
> 1. 打开 https://nodejs.org
> 2. 下载 **22.x.x LTS** 版本（不要下载 20.x 或更低）
> 3. 运行安装程序，一路点击"Next"完成安装
> 4. 安装完成后，**重新打开 PowerShell**，运行 `node --version` 确认版本 >= v22.0.0
>
> 安装完成后对我说"监控 XX 的微信"即可。

**If Node.js OK but PeekabooWin NOT found**, show this message:

> **PeekabooWin 未安装，请按以下步骤操作：**
>
> **第 2 步：安装 PeekabooWin**
> 1. 打开 PowerShell，运行：
>    ```powershell
>    cd C:\
>    git clone https://github.com/FelixKruger/PeekabooWin
>    cd PeekabooWin
>    npm install
>    npm test
>    ```
> 2. 等待 `npm test` 全部通过（表示安装成功）
>
> **第 3 步：设置环境变量**
> ```powershell
> [System.Environment]::SetEnvironmentVariable("PEEKABOO_WIN_DIR", "C:\PeekabooWin", "User")
> ```
> 设置后必须**重新打开 PowerShell** 才能生效。
>
> 全部完成后对我说"监控 XX 的微信"即可。

**If PeekabooWin found but `node --help` fails**, show:

> **PeekabooWin 已安装但运行异常，请检查：**
> 1. Node.js 版本是否 >= 22：`node --version`
> 2. 在 PeekabooWin 目录重新安装依赖：`cd C:\PeekabooWin && npm install`
> 3. 确认没有安全软件拦截

#### All Prerequisites Met

Once all checks pass, proceed to Step 1 below.

---

### Step 1: Ask User for Contact & Style

1. Ask user: "Which contact to monitor?" (required - no default)
2. Ask user: "Reply style/tone?" (default: friendly, match user personality)
3. Take screenshot using the appropriate engine
4. Read screenshot to identify current chat state
5. Start monitor script with --contact parameter (background)
6. Set up automation for auto-reply polling

**Example**: User says "监控 mini 的微信"

### macOS:
- Contact = "mini"
- Start monitor: `python3 scripts/wechat_monitor.py --contact mini --interval 600`
- Screenshot: `peekaboo image --mode window --app 微信 --retina --path /tmp/wechat_mon/latest.png`

### Windows:
- Contact = "mini"
- Start monitor: `python scripts/wechat_monitor.py --contact mini --interval 600`
- Screenshot: `node <PEEKABOO_WIN_DIR>/bin/peekaboo-win.js screen capture --output <TEMP>\wechat_mon\latest.png`

---

## Core Workflow

### Step 1: Check Contact & Current State

**macOS:**
```bash
peekaboo list apps --json | grep 微信
peekaboo image --mode window --app 微信 --retina --path /tmp/wechat_mon/latest.png
```

**Windows:**
```powershell
node <PEEKABOO_WIN_DIR>\bin\peekaboo-win.js app list
node <PEEKABOO_WIN_DIR>\bin\peekaboo-win.js screen capture --output %TEMP%\wechat_mon\latest.png
```

Read the screenshot to:
- Identify the current chat contact
- Check for unread messages (red badge on avatar)
- Note existing messages in the conversation

### Step 2: Reply to a Message

#### macOS (Peekaboo CLI)

```bash
# 1. Switch to WeChat
peekaboo app switch --to 微信

# 2. Click input box (coords may vary by window position)
peekaboo click --coords 900,780 --app 微信

# 3. Type the message
peekaboo type "你的回复内容" --app 微信

# 4. Send using type --return (NOT press --key return)
peekaboo type "" --app 微信 --return
```

> **IMPORTANT**: `peekaboo press --key return` does NOT reliably trigger WeChat send.
> Always use `peekaboo type "" --app 微信 --return` to send.

#### Windows (PeekabooWin)

```powershell
# 1. Switch to WeChat
node <PEEKABOO_WIN_DIR>\bin\peekaboo-win.js app switch --name "微信"

# 2. Click input box (use label or coordinates)
node <PEEKABOO_WIN_DIR>\bin\peekaboo-win.js click --on "100,200"
# 或者用 label 点击:
# node <PEEKABOO_WIN_DIR>\bin\peekaboo-win.js click --on "消息输入框" --snapshot latest

# 3. Type the message
node <PEEKABOO_WIN_DIR>\bin\peekaboo-win.js type --text "你的回复内容"

# 4. Send using press Enter
node <PEEKABOO_WIN_DIR>\bin\peekaboo-win.js press --keys "Enter"
```

> **Windows 注意**: PeekabooWin 支持 `--on "label"` 模式通过标签点击 UI 元素，比坐标点击更可靠。
> 建议先用 `peekaboo-win see --mode window --title "微信"` 确认可点击的元素标签。

### Step 3: Verify Send

**macOS:**
```bash
peekaboo image --mode window --app 微信 --retina --path /tmp/wechat_mon/verify.png
```

**Windows:**
```powershell
node <PEEKABOO_WIN_DIR>\bin\peekaboo-win.js screen capture --output %TEMP%\wechat_mon\verify.png
```

Read the verify screenshot to confirm the message appears as a green bubble.

### Step 4: Start Background Monitoring

**macOS:**
```bash
nohup python3 scripts/wechat_monitor.py \
  --contact "联系人名称" \
  --interval 600 \
  --threshold 1000 \
  > /tmp/wechat_mon/monitor.log 2>&1 &
```

**Windows (PowerShell):**
```powershell
Start-Process -NoNewWindow python -ArgumentList "scripts/wechat_monitor.py --contact `"联系人名称`" --interval 600 --threshold 1000" -RedirectStandardOutput "$env:TEMP\wechat_mon\monitor.log" -RedirectStandardError "$env:TEMP\wechat_mon\monitor_err.log"
```

**Important**:
- Contact name must match exactly as it appears in WeChat
- Can run multiple monitors for different contacts (use different --workdir and --pending)
- `--engine auto` (default) will auto-detect macOS vs Windows

### Step 5: Set Up Auto-Reply Automation

Create a recurring automation (every 30s) that:

**macOS Automation Prompt Template:**
```
检查 /tmp/wechat_pending.txt 是否存在。
IF EXISTS:
  1. 读取 pending 文件获取 CONTACT 和 DETECTED 时间
  2. 如果距离 DETECTED 时间 < 10分钟: 结束（继续等待）
  3. 如果 >= 10分钟: 重新截图，分析是否已回复
     - 已回复(绿色气泡): 删除 pending，不回复
     - 未回复(白色气泡): 生成回复并发送
     发送命令:
       peekaboo app switch --to 微信
       peekaboo click --coords 900,780 --app 微信
       peekaboo type "[回复]" --app 微信
       peekaboo type "" --app 微信 --return
IF NOT EXISTS:
  什么都不做
```

**Windows Automation Prompt Template:**
```
检查 %TEMP%\wechat_pending.txt 是否存在。
IF EXISTS:
  1. 读取 pending 文件获取 CONTACT 和 DETECTED 时间
  2. 如果距离 DETECTED 时间 < 10分钟: 结束（继续等待）
  3. 如果 >= 10分钟: 重新截图，分析是否已回复
     - 已回复(绿色气泡): 删除 pending，不回复
     - 未回复(白色气泡): 生成回复并发送
     发送命令(替换 <PEEKABOO_WIN_DIR>):
       node <PEEKABOO_WIN_DIR>\bin\peekaboo-win.js app switch --name "微信"
       node <PEEKABOO_WIN_DIR>\bin\peekaboo-win.js type --text "[回复]"
       node <PEEKABOO_WIN_DIR>\bin\peekaboo-win.js press --keys "Enter"
IF NOT EXISTS:
  什么都不做
```

Use `automation_update` tool with:
- `scheduleType: recurring`
- `rrule: RRULE:FREQ=SECONDLY;INTERVAL=30`
- `prompt`: (the template above, filled with actual contact)

---

## Sending Rules

1. **Only reply to the target contact** — never reply to other people's messages
2. **Match user personality** — use the user's real voice, not robotic language
3. **Reference current activity truthfully** — what is the user actually doing right now?
4. **Be warm but natural** — no excessive emojis, no corporate tone

---

## Input Box Coordinates / Labels

### macOS
The input box coordinates depend on WeChat window position. Default: `900,780`

```bash
peekaboo see --app 微信 --annotate --path /tmp/wechat_coords.png
```

### Windows
PeekabooWin supports label-based clicking (recommended) or coordinate clicking:

```powershell
# 推荐: 先查看微信窗口有哪些可点击元素
node <PEEKABOO_WIN_DIR>\bin\peekaboo-win.js see --mode window --title "微信"

# 然后用 label 点击
node <PEEKABOO_WIN_DIR>\bin\peekaboo-win.js click --on "消息" --title "微信"

# 或用坐标点击
node <PEEKABOO_WIN_DIR>\bin\peekaboo-win.js mouse click --x 900 --y 780
```

---

## Platform Differences Summary

| Feature | macOS (Peekaboo) | Windows (PeekabooWin) |
|---------|-----------------|----------------------|
| Install | `brew install steipete/peekaboo/peekaboo` | `git clone` + `npm install` |
| Screenshot | `peekaboo image --mode window --app 微信` | `peekaboo-win screen capture` |
| Click | `peekaboo click --coords X,Y --app 微信` | `peekaboo-win click --on "label"` or `mouse click --x --y` |
| Type | `peekaboo type "text" --app 微信` | `peekaboo-win type --text "text"` |
| Send | `peekaboo type "" --app 微信 --return` | `peekaboo-win press --keys "Enter"` |
| App switch | `peekaboo app switch --to 微信` | `peekaboo-win app switch --name "微信"` |
| Temp dir | `/tmp/wechat_mon/` | `%TEMP%\wechat_mon\` |
| Pending file | `/tmp/wechat_pending.txt` | `%TEMP%\wechat_pending.txt` |

---

## Troubleshooting

| Problem | macOS Fix | Windows Fix |
|---------|-----------|-------------|
| 截图失败 | 检查权限: `peekaboo permissions` | 检查 Node.js 版本 >= 22 |
| 消息未发送 | 用 `type "" --return` | 用 `press --keys "Enter"` |
| 检测不到变化 | 降低 `--threshold` 到 800 | 降低 `--threshold` 到 800 |
| PeekabooWin 找不到 | - | 设置 `PEEKABOO_WIN_DIR` 环境变量 |
| 微信窗口不可见 | `peekaboo app unhide --app 微信` | 确保 WeChat 未最小化 |
| 自动化不触发 | 检查 automation 是否 ACTIVE | 检查 automation 是否 ACTIVE |

---

## Stopping

**macOS:**
```bash
kill $(pgrep -f wechat_monitor.py)
automation_update --mode delete --id <automation-id>
rm -rf /tmp/wechat_mon /tmp/wechat_pending.txt
```

**Windows (PowerShell):**
```powershell
Stop-Process -Name python -Force -ErrorAction SilentlyContinue
# 删除 automation (在 WorkBuddy 中操作)
Remove-Item -Recurse -Force "$env:TEMP\wechat_mon"
Remove-Item -Force "$env:TEMP\wechat_pending.txt"
```
