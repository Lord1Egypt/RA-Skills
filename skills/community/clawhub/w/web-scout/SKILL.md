---
name: web-scout
description: 给 AI Agent 一键装上全网采集能力。基于 Agent Reach，支持 Twitter/X、Reddit、YouTube、B站、小红书、抖音、GitHub、LinkedIn、Boss直聘、RSS、全网搜索等平台。一条命令安装，零 API 费用。
version: 1.0.0
metadata:
  openclaw:
    requires:
      tools: [exec]
    optional:
      tools: [web_fetch]
---

# Web Scout — AI Agent 全网采集工具箱

基于 [Agent Reach](https://github.com/Panniantong/Agent-Reach) 封装，让你的 AI Agent 一键获得全网信息采集能力。

## 支持平台

| 平台 | 工具 | 免费 | 需要配置 |
|------|------|------|---------|
| 🌐 网页 | Jina Reader | ✅ | 无 |
| 📺 YouTube | yt-dlp | ✅ | 无 |
| 📺 B站 | yt-dlp | ✅ | 服务器需代理 |
| 📡 RSS | feedparser | ✅ | 无 |
| 🔍 全网搜索 | Exa (MCP) | ✅ | 自动配置 |
| 📦 GitHub | gh CLI | ✅ | 需登录 |
| 🐦 Twitter/X | xreach (bird) | ✅ | 需 Cookie |
| 📖 Reddit | JSON API + Exa | ✅ | 服务器需代理 |
| 📕 小红书 | xiaohongshu-mcp | ✅ | 需 Docker + Cookie |
| 🎵 抖音 | douyin-mcp-server | ✅ | 需 MCP 服务 |
| 💼 LinkedIn | linkedin-mcp | ✅ | 需浏览器登录 |
| 🏢 Boss直聘 | mcp-bosszp | ✅ | 需扫码登录 |

## 安装

### 第一步：安装 Agent Reach CLI

```bash
pip install https://github.com/Panniantong/agent-reach/archive/main.zip
```

### 第二步：自动安装依赖

默认模式（自动安装所有依赖）：
```bash
agent-reach install --env=auto
```

安全模式（只检查不安装，适合生产环境）：
```bash
agent-reach install --env=auto --safe
```

预览模式（只看会做什么）：
```bash
agent-reach install --env=auto --dry-run
```

### 第三步：检查状态

```bash
agent-reach doctor
```

### 第四步：按需配置平台

需要 Cookie 的平台建议使用小号，避免封号风险。

Cookie 导出方法：浏览器登录平台 → 安装 [Cookie-Editor](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) 插件 → Export → Header String → 发给 Agent。

配置 Twitter：
```bash
agent-reach configure twitter-cookies "COOKIE_STRING"
```

配置代理（服务器访问 Reddit/B站）：
```bash
agent-reach configure proxy http://user:pass@ip:port
```

配置小红书（需要 Docker）：
```bash
docker run -d --name xiaohongshu-mcp -p 18060:18060 xpzouying/xiaohongshu-mcp
mcporter config add xiaohongshu http://localhost:18060/mcp
```

## 常用命令速查

### 读网页
```bash
curl -s "https://r.jina.ai/URL"
```

### 搜索 Twitter/X
```bash
xreach search "关键词" --json
```

### YouTube/B站 字幕提取
```bash
yt-dlp --dump-json "VIDEO_URL"           # 视频信息
yt-dlp --write-sub --skip-download "URL"  # 提取字幕
```

### 全网搜索（Exa）
```bash
mcporter call 'exa.search(query: "关键词", numResults: 10)'
```

### GitHub
```bash
gh repo view owner/repo        # 查看仓库
gh search repos "关键词"        # 搜索仓库
gh issue list -R owner/repo    # 查看 Issue
```

### RSS
```bash
python3 -c "import feedparser; f=feedparser.parse('RSS_URL'); [print(e.title) for e in f.entries[:10]]"
```

### 小红书
```bash
mcporter call 'xiaohongshu.search_feeds(keyword: "关键词")'
mcporter call 'xiaohongshu.get_feed_detail(note_id: "ID")'
```

### 抖音
```bash
mcporter call 'douyin.parse_douyin_video_info(share_link: "分享链接")'
```

### Reddit
```bash
mcporter call 'exa.search(query: "site:reddit.com 关键词")'
```

## 维护

检查更新：
```bash
agent-reach check-update
```

升级：
```bash
pip install --upgrade https://github.com/Panniantong/agent-reach/archive/main.zip
```

健康检查（适合定时任务）：
```bash
agent-reach watch
```

卸载：
```bash
agent-reach uninstall        # 完整卸载
agent-reach uninstall --keep-config  # 保留配置
pip uninstall agent-reach    # 卸载 Python 包
```

## 安全说明

- Cookie 只存本地 `~/.agent-reach/config.yaml`，文件权限 600
- 代码完全开源，可审查
- 需要 Cookie 的平台（Twitter、小红书）建议用小号
- 支持 `--safe` 和 `--dry-run` 模式

## 致谢

基于 [Agent Reach](https://github.com/Panniantong/Agent-Reach) by Panniantong，MIT 协议。
