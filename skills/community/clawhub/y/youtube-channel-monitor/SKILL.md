---
name: youtube-channel-monitor
description: |
  YouTube 频道订阅+自动摘要+Telegraph 发布工具。用于：
  1. 定时监控指定 YouTube 频道的新视频
  2. 提取视频字幕（支持中英双语）
  3. 生成可读性强的中文专栏文章
  4. 自动发布到 Telegraph 并推送到 Telegram 频道
  
  触发场景：
  - 用户想订阅 YouTube 频道并自动获取更新
  - 需要将 YouTube 视频内容转化为文字摘要
  - 希望用 Telegraph 格式接收长内容
---

# YouTube 频道监控

定时检查频道更新，自动生成 Telegraph 文章推送。

## 快速开始

### 订阅新频道

直接发送 YouTube 频道链接给我，格式支持：
- `https://www.youtube.com/@username`
- `https://www.youtube.com/channel/CHANNEL_ID`

### 查看订阅列表

```bash
cat ~/.openclaw/workspace/youtube-channels.json
```

### 手动检查更新

```bash
python3 ~/.openclaw/workspace/skills/youtube-channel-monitor/scripts/youtube-monitor.py
```

## 配置说明

配置文件位于 `~/.openclaw/workspace/youtube-channels.json`：

```json
[
  {"url": "https://www.youtube.com/channel/xxx", "name": "频道名称"}
]
```

### 参数设置

在脚本中可调整：
- `MAX_SUBTITLE_RETRIES = 3` - 字幕检查重试次数
- `PROXY` - HTTP 代理地址
- `TELEGRAM_CHANNEL` - 推送目标频道

## 工作流程

1. 每小时检查订阅频道的最新视频
2. 首次发现新视频时尝试获取字幕
3. 如果无字幕，等待下次检查再试（最多3次）
4. 获得字幕后：
   - 中文字幕：直接生成摘要
   - 英文字幕：自动翻译成中文
5. 使用 humanize-ai-text 去 AI 味
6. 发布到 Telegraph
7. 推送到 Telegram 频道

## 依赖

- `yt-dlp` - 视频信息获取
- `youtube-transcript-api` - 字幕提取
- `requests` - HTTP 请求
- 本地代理 (Clash 7897) - 用于访问 YouTube
