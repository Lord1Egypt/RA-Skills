---
name: telegram-checkin
description: 使用 agent-browser 对 Telegram 机器人进行自动签到。当用户提到"签到"、"Telegram 机器人自动操作"、"OKEmbyBot"、"Telegram Web 自动化"、"Telegram 按钮点击"时触发。使用持久化 Chrome Profile 保存 cookies，关掉再开无需重新登录。
---

# Telegram 机器人自动签到 Skill

## 功能概述

使用 `agent-browser` 对 Telegram Web 上的机器人（以 OkEmbyBot 为例）进行自动化签到操作。自动处理：
- **Cookie 持久化**（使用 Chrome Profile，关掉浏览器再打开无需重新扫码登录）
- 点击内联键盘按钮
- 等待并验证签到结果

## 核心原理

**重要**：必须用 `--profile` 而不是 `--session-name`！
- `--session-name`：agent-browser 自己管理的 session 文件，**无法保存 httpOnly cookies**（Telegram 用的就是 httpOnly cookies）
- `--profile`：使用 Chrome 原生用户数据目录，cookies 会正确保存，**关掉再开无需重新登录**

## 前置条件

### 1. 安装 agent-browser

```bash
npm install -g agent-browser
# 或
brew install agent-browser
# 或
cargo install agent-browser
```

首次使用需要安装 Chrome：
```bash
agent-browser install
```

### 2. 创建持久化 Profile

首次使用时手动扫码登录一次，之后 cookies 会自动持久化到 Profile 目录：

```bash
# 创建 Profile 目录
mkdir -p ~/.chrome-profiles/telegram-web

# 打开浏览器（带 --headed 显示窗口）
agent-browser --profile ~/.chrome-profiles/telegram-web --headed open https://web.telegram.org

# ... 扫码登录一次 ...

# 之后关掉再开，cookie 会自动保持，无需重新登录
```

## 工作流程

### 标准签到流程

```bash
# Step 1: 打开 Telegram Web
agent-browser --profile ~/.chrome-profiles/telegram-web open https://web.telegram.org

# Step 2: 等待页面加载
sleep 3

# Step 3: 获取页面元素引用
agent-browser --profile ~/.chrome-profiles/telegram-web snapshot -i

# Step 4: 点击 OkEmbyBot 进入聊天
# 在 snapshot 输出中找到 OkEmbyBot 的 link ref，点击它

# Step 5: 等待机器人回复出现内联按钮
sleep 3

# Step 6: 获取最新元素，找到签到按钮
agent-browser --profile ~/.chrome-profiles/telegram-web snapshot -i
# 在输出中找 "🎯 签到" 按钮（通常是列表中最后一个）

# Step 7: 点击签到按钮
agent-browser --profile ~/.chrome-profiles/telegram-web click e28  # 最后一个签到按钮

# Step 8: 等待结果并截图验证
sleep 5
agent-browser --profile ~/.chrome-profiles/telegram-web screenshot /tmp/checkin-result.png
```

### 查找签到按钮的方法

```bash
agent-browser --profile ~/.chrome-profiles/telegram-web snapshot -i 2>&1 | grep "签到"
```

输出示例：
```
- button "🎯 签到" [ref=e14]
- button "🎯 签到" [ref=e17]
- button "🎯 签到" [ref=e20]
- button "🎯 签到" [ref=e25]
- button "🎯 签到" [ref=e28]
```

**注意**：页面上可能有多个签到按钮（来自不同消息）。通常最后一个（e28）是最新的，点击它。

### 验证签到结果

签到成功后，机器人会发送类似：
```
🎉 签到成功 | 10 OK币
💴 当前持有 | 158 OK币
⏳ 签到日期 | 2026-04-15
```

截图并用 image 工具分析即可确认。

## Watchdog 自动守护（必做）

Watchdog 是一个后台守护进程，**开机自动启动**，负责在浏览器意外退出时自动重启。这样 Telegram 浏览器就相当于"永远在后台运行"，关掉也会自动打开。

### 安装 Watchdog

```bash
# 创建 plist（如果还没有）
cat > ~/Library/LaunchAgents/ai.openclaw.agent-browser-watchdog.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>ai.openclaw.agent-browser-watchdog</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/Users/zq/.openclaw/scripts/agent-browser-watchdog.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/agent-browser-watchdog.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/agent-browser-watchdog.log</string>
</dict>
</plist>
EOF

# 加载服务（开机自启）
launchctl load ~/Library/LaunchAgents/ai.openclaw.agent-browser-watchdog.plist

# 立即启动（不等下次开机）
launchctl start ai.openclaw.agent-browser-watchdog
```

### Watchdog 脚本内容

Watchdog 脚本位于 `~/.openclaw/scripts/agent-browser-watchdog.sh`，内容如下（已预设好，无需修改）：

```bash
#!/bin/bash
# agent-browser watchdog
# 自动检测 agent-browser 进程，关闭后自动重启

BROWSER_URL="${AGENT_BROWSER_URL:-https://web.telegram.org}"
CHROME_PROFILE="${AGENT_BROWSER_CHROME_PROFILE:-~/.chrome-profiles/telegram-web}"
CHECK_INTERVAL=30  # 每30秒检查一次

LOG_FILE="/tmp/agent-browser-watchdog.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

is_daemon_running() {
    pgrep -f "agent-browser-darwin" > /dev/null 2>&1
}

start_browser() {
    log "启动 agent-browser daemon..."
    agent-browser --profile "$CHROME_PROFILE" open "$BROWSER_URL" > /dev/null 2>&1 &
    sleep 3
    log "agent-browser 已启动 (Profile: $CHROME_PROFILE)"
}

log "=== Watchdog 启动 ==="
log "Profile: $CHROME_PROFILE"
log "URL: $BROWSER_URL"

while true; do
    if ! is_daemon_running; then
        log "检测到 daemon 未运行，正在重启..."
        start_browser
    else
        log "Daemon 运行正常"
    fi
    sleep $CHECK_INTERVAL
done
```

### 常用命令

```bash
# 停止 Watchdog（不再自动重启）
launchctl unload ~/Library/LaunchAgents/ai.openclaw.agent-browser-watchdog.plist

# 重新启动 Watchdog
launchctl unload ~/Library/LaunchAgents/ai.openclaw.agent-browser-watchdog.plist
launchctl load ~/Library/LaunchAgents/ai.openclaw.agent-browser-watchdog.plist

# 查看 Watchdog 日志
tail -f /tmp/agent-browser-watchdog.log

# 手动关掉浏览器（Watchdog 会在 30 秒内自动重启）
agent-browser close
```

### 工作原理

```
开机 → launchd 启动 Watchdog → 每 30 秒检查 daemon
                                         ↓
                              daemon 挂了？
                              是 → 重启 daemon → Chrome 自动打开
                              否 → 继续等待
```

## 故障排除

### 浏览器窗口没显示

用 `--headed` 参数打开窗口：
```bash
agent-browser --profile ~/.chrome-profiles/telegram-web --headed open https://web.telegram.org
```

### 需要重新登录

删除 Profile 目录后重新扫码：
```bash
rm -rf ~/.chrome-profiles/telegram-web
agent-browser --profile ~/.chrome-profiles/telegram-web --headed open https://web.telegram.org
# 重新扫码登录
```

### "daemon already running" 警告

这是正常的——agent-browser 的 daemon 是持久化的。如果想用新参数重启，先关掉：
```bash
agent-browser close  # 关掉浏览器窗口
pkill -f "agent-browser-darwin"  # 关掉 daemon（如需完全重置）
```

### 找不到签到按钮

1. 等待更长时间让页面加载：`sleep 5`
2. 先点击进入 OkEmbyBot 聊天窗口再操作
3. 滚动页面到底部让按钮可见

滚动示例：
```bash
agent-browser evaluate "
const el = document.querySelector('.message-list-container');
if (el) el.scrollTop = el.scrollHeight;
"
```

## Profile 管理

### 查看 Profile 目录
```bash
ls -la ~/.chrome-profiles/telegram-web/
```

### Profile 备份（可选）
```bash
# 备份整个 Profile（包含 cookies）
cp -r ~/.chrome-profiles/telegram-web ~/chrome-profiles-telegram-web-backup

# 恢复
cp -r ~/chrome-profiles-telegram-web-backup ~/.chrome-profiles/telegram-web
```
