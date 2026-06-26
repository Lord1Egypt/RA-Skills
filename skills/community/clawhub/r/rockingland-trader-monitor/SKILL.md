---
name: xiaohongshu-trader-monitor
description: Xiaohongshu (RedNote) user post keyword monitoring and WeChat notification. Use when the user needs to (1) monitor a specific Xiaohongshu user's latest posts for keywords in titles, (2) get notified via WeChat when target keywords appear in new posts, (3) set up automated periodic checks for a Xiaohongshu trader/seller's updates, or (4) configure keyword-based alerts for Xiaohongshu content. Triggers on phrases like "小红书监测", "远行商人", "帖子监控", "关键词提醒", "xiaohongshu monitor".
---

# Xiaohongshu Trader Monitor

监测指定小红书用户的最新帖子，标题含关键词时自动推送到微信。

## ⚠️ 使用前配置（必须）

本 skill 需要你填入自己的认证信息才能运行。打开 `scripts/xhs_trader_monitor.py`，修改**用户配置区**（文件顶部）：

### 1. 微信推送目标 ID

获取你的 openclaw-weixin 用户 ID：
```bash
openclaw message list-accounts --channel openclaw-weixin
```

将 `TARGET_ID` 替换为你的 ID，格式为 `xxx@im.wechat`。

### 2. 小红书目标用户信息

**USER_ID**：目标用户主页 URL 中的 ID
- 格式：`https://www.xiaohongshu.com/user/profile/USER_ID`
- 从分享链接或搜索结果中获取

**USER_XSEC**：xsec_token（认证令牌）
- 从目标用户任意帖子的 feed 数据中提取 `xsecToken`
- 或运行 `mcp-call.sh user_profile` 后从返回数据中获取

### 3. 监测关键词

在 `KEYWORDS` 列表中配置你要监测的关键词：
```python
KEYWORDS = ["棱镜球", "炫彩蛋", "同乘蛋", "祝福项坠"]
```

### 4. Cookies 登录

将已登录小红书的浏览器 cookies 导出为 JSON 数组，保存到 `cookies.json`：
```json
[
  {"name": "a1", "value": "...", "domain": ".xiaohongshu.com", "path": "/"},
  {"name": "web_session", "value": "...", "domain": ".xiaohongshu.com", "path": "/"}
```

放置路径（按优先级）：
1. `~/cookies.json`
2. `~/.xiaohongshu/cookies.json`
3. 环境变量 `XHS_COOKIES_SRC` 指定的路径

> ⚠️ 首次登录可通过 `mcp-call.sh get_login_qrcode` 获取二维码扫码登录，但当前环境多被风控，推荐直接导出 cookies。

## Quick Start

### 安装依赖

```bash
# 1. 安装 xiaohongshu-mcp 二进制
# 从 GitHub Releases 下载对应平台文件：
# https://github.com/xpzouying/xiaohongshu-mcp/releases
mkdir -p ~/.local/bin
mv xiaohongshu-mcp-linux-amd64 ~/.local/bin/xiaohongshu-mcp
mv xiaohongshu-login-linux-amd64 ~/.local/bin/xiaohongshu-login
chmod +x ~/.local/bin/xiaohongshu-*

# 2. 安装系统依赖
apt-get install -y jq xvfb

# 3. 检查依赖
./scripts/install-check.sh
```

### 配置并运行

1. 编辑 `scripts/xhs_trader_monitor.py` 填入你的配置
2. 运行监测：
```bash
cd scripts/
python3 xhs_trader_monitor.py
```

### 配置定时任务

```
5 8,12,16,20 * * * /usr/bin/python3 /path/to/xiaohongshu-trader-monitor/scripts/xhs_trader_monitor.py >> /path/to/logs/xhs_trader.log 2>&1
```

## How It Works

1. **启动 MCP**：自动启动 xiaohongshu-mcp 服务（含 Xvfb 虚拟显示）
2. **获取帖子**：调用 `user_profile` 获取目标用户主页最新帖子
3. **关键词匹配**：检查最近 5 条帖子标题是否含配置的关键词
4. **日期过滤**：只检查**今天**发布的帖子（MM.DD 前缀匹配）
5. **去重推送**：已通知过的帖子 ID 不会重复推送
6. **微信通知**：命中关键词时推送消息到微信
7. **关闭 MCP**：监测完成后自动关闭服务

## Resources

### scripts/
- `xhs_trader_monitor.py` — 核心监测脚本（需配置用户信息）
- `start-mcp.sh` — 启动 MCP 服务（自动管理 Xvfb）
- `stop-mcp.sh` — 停止 MCP 服务
- `mcp-call.sh` — 通用 MCP 调用脚本
- `install-check.sh` — 依赖检查

### references/
- `trader_rules.md` — 完整配置指南、故障排查、消息模板

## Files

| File | Purpose |
|------|---------|
| `scripts/xhs_trader_monitor.py` | Core monitoring script (requires user config) |
| `scripts/start-mcp.sh` | Start MCP service with Xvfb |
| `scripts/stop-mcp.sh` | Stop MCP service |
| `scripts/mcp-call.sh` | Generic MCP tool caller |
| `scripts/install-check.sh` | Dependency checker |
| `references/trader_rules.md` | Configuration guide and troubleshooting |
| `cookies.json` | Login cookies (user-provided, not included) |
| `xhs_trader_state.json` | Notification state (auto-generated) |
