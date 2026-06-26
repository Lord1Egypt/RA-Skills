# 📕 小红书热榜日报 - Xiaohongshu Hot Daily

> 自动抓取小红书热门笔记，支持AI摘要和多渠道推送

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![ClawHub](https://img.shields.io/badge/ClawHub-Available-brightgreen)](https://clawhub.ai)

## ✨ 功能特性

- 📊 自动抓取小红书热门笔记 Top 30
- 🤖 AI 智能分类摘要
- 📱 多渠道推送（Telegram/微信/邮件）
- 📈 数据统计（点赞/收藏/评论）

## 🚀 快速开始

### 安装

```bash
npx clawhub@latest install xiaohongshu-hot-daily
```

### 使用

```bash
# 获取今日热门 Top 10
python3 fetch_hot.py --top 10

# 生成摘要并导出
python3 fetch_hot.py --summary --output hot.json
```

## 💰 定价

- **免费版**：每日 Top 10，基础数据
- **Pro版（49元）**：Top 30 + AI摘要 + 多渠道推送

## 📄 许可证

MIT License - 小天🦞
