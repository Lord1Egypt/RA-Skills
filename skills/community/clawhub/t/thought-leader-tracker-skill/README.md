# Thought Leader Tracker

自动收集思想领袖的播客、访谈和 YouTube 视频内容，生成 Markdown 日报。

## 功能特性

- ✅ 支持多平台：YouTube、Apple Podcasts、Spotify
- ✅ 预设 6 位思想领袖：Boris Cherny、李飞飞、Elen Verna、Peter Steinberger、Dan Koe、Demis Hassabis
- ✅ 支持自定义添加新人物
- ✅ 自动生成 Markdown 日报（标题、链接、发布时间、内容概要、核心观点）
- ✅ 共性观点分析：识别 2 人及以上的共同主题
- ✅ 支持近 7 天和近 30 天两种时间范围

## 快速开始

```bash
# 收集最近 7 天的内容
~/.openclaw/skills/thought-leader-tracker/thought-leader-tracker.sh collect

# 收集最近 30 天的内容
~/.openclaw/skills/thought-leader-tracker/thought-leader-tracker.sh collect 30

# 查看已追踪的思想领袖
~/.openclaw/skills/thought-leader-tracker/thought-leader-tracker.sh list

# 添加新人物（交互式）
~/.openclaw/skills/thought-leader-tracker/thought-leader-tracker.sh add-person
```

## 配置文件

编辑 `config.json` 自定义：

```json
{
  "thoughtLeaders": [
    {
      "name": "新人物名称",
      "keywords": ["关键词 1", "关键词 2"],
      "platforms": ["youtube", "apple-podcasts", "spotify"]
    }
  ]
}
```

## 输出示例

报告保存在 `daily-logs/` 目录，格式如下：

```markdown
# Thought Leader Daily Report

**Date:** 2026-03-26
**Time Range:** Last 7 days

## 🔍 Common Themes
- **AI** - Mentioned by: 李飞飞，Demis Hassabis

## 👤 Boris Cherny
### Podcast Title
- **Platform:** Apple Podcasts
- **Published:** 2026-03-20
- **Link:** https://...
- **Summary:** ...
- **Key Points:**
  - 要点 1
  - 要点 2
```

## 自动化

设置每日定时任务（crontab）：

```bash
# 每天早上 8 点运行
0 8 * * * ~/.openclaw/skills/thought-leader-tracker/thought-leader-tracker.sh collect 7
```

## 依赖

- Node.js（运行收集脚本）
- jq（可选，用于美化输出）

## 注意事项

- YouTube 和 Spotify API 需要配置认证密钥才能获取完整数据
- 当前实现使用公开 API（iTunes Search）作为演示
- 生产环境建议配置 `YOUTUBE_API_KEY` 环境变量
