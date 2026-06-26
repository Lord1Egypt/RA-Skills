# 🔥 微博热搜日报 - Weibo Hot Daily

> 自动抓取微博热搜榜，支持AI摘要和多渠道推送

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![ClawHub](https://img.shields.io/badge/ClawHub-Available-brightgreen)](https://clawhub.ai)

## ✨ 功能特性

- 📊 自动抓取微博热搜榜 Top 50
- 🤖 AI 智能分类摘要
- 📱 多渠道推送（Telegram/微信/邮件）
- ⏰ 定时执行（每日自动更新）
- 📈 数据统计（热度值/排名变化）

## 🚀 快速开始

### 安装

```bash
npx clawhub@latest install weibo-hot-daily
```

### 使用

```bash
# 获取今日热搜 Top 10
python3 fetch_hot.py --top 10

# 获取完整 Top 50
python3 fetch_hot.py --top 50

# 生成摘要并导出
python3 fetch_hot.py --summary --output hot.json
```

## 📊 输出示例

```
#1 太原火灾已致1死25伤
   [HOT] 118.2万 | [CAT] 社会
   [LINK] https://s.weibo.com/weibo?q=...
```

## 💰 定价

- **免费版**：每日 Top 10，基础数据
- **Pro版（49元）**：Top 50 + AI摘要 + 多渠道推送

## 📄 许可证

MIT License - 小天🦞
