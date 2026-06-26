# YouTube OpenClaw 监控系统

自动搜索 YouTube 视频、获取字幕、生成中文摘要，并推送到 Telegram。

## 功能

- 搜索指定关键词的 YouTube 视频
- 获取视频字幕/转录
- 生成中文摘要（3个核心要点）
- 自动推送到 Telegram

## 准备工作

### 1. 安装依赖

```bash
cd scripts
npm install https-proxy-agent
```

### 2. 配置环境变量

创建 `.env` 文件或设置系统环境变量：

```bash
# 必填：Transcript API Key（从 transcriptapi.com 获取）
export TRANSCRIPT_API_KEY="your-api-key-here"

# 必填：你的 Telegram User ID
export TELEGRAM_USER_ID="your-telegram-user-id"

# 可选：代理配置（如果需要）
export HTTPS_PROXY="http://127.0.0.1:7890"
```

### 3. 配置 Cron 定时任务

```bash
# 每天早上 9 点执行
0 9 * * * cd /path/to/workspace && node scripts/youtube-openclaw-monitor.js >> /path/to/workspace/logs/youtube-monitor.log 2>&1
```

## 运行

```bash
node youtube-openclaw-monitor.js
```

## 输出

- 字幕文件保存在 `../youtube-summaries/` 目录
- 格式：`YYYY-MM-DD-VIDEOID.md`
- 最新报告：`../youtube-summaries/latest-report.md`

## 依赖

- Node.js 18+
- https-proxy-agent
- OpenClaw（用于 Telegram 消息发送）

## 配合 OpenClaw 使用

该脚本设计用于配合 OpenClaw 的定时任务功能，可以：

1. 设置每日定时执行
2. 自动将报告发送到你的 Telegram
3. 结合 OpenClaw 的 AI 能力进行翻译和摘要