# YouTube OpenClaw 监控系统

自动搜索 YouTube 视频、获取字幕、生成中文摘要，并推送到 Telegram。

## 使用场景

- 监控特定关键词的 YouTube 新视频
- 自动获取视频字幕并生成中文摘要
- 定时推送新视频报告到 Telegram

## 触发指令

- "YouTube 监控"
- "搜索 OpenClaw 视频"
- "检查 YouTube 更新"

## 前置要求

1. 安装依赖：`npm install https-proxy-agent`
2. 配置环境变量：
   - `TRANSCRIPT_API_KEY`：从 transcriptapi.com 获取 API Key
   - `TELEGRAM_USER_ID`：你的 Telegram 用户 ID

## 配置示例

```bash
export TRANSCRIPT_API_KEY="your-api-key"
export TELEGRAM_USER_ID="your-user-id"
node scripts/youtube-openclaw-monitor.js
```

## 配合 Cron 使用

设置每日早上 9 点自动执行：

```bash
0 9 * * * cd /path/to/workspace && node scripts/youtube-openclaw-monitor.js
```

## 输出

- 字幕文件：`youtube-summaries/YYYY-MM-DD-VIDEOID.md`
- 报告文件：`youtube-summaries/latest-report.md`