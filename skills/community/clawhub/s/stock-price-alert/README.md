# Stock Price Alert

股价异动实时提醒，支持行情接口、邮件和 Sonos 语音播报。

## 简介

监控持仓股票价格异动，当涨跌幅或价格突破阈值时自动发出邮件和/或 Sonos 语音播报提醒。支持自定义持仓列表、告警规则和通知方式。

## 功能特性

- 📈 涨跌幅阈值告警
- 💰 价格突破上下限告警
- 📧 邮件实时提醒
- 🔊 Sonos 语音播报
- 🔄 可配置轮询间隔
- 🔌 可替换行情数据源

## 快速开始

1. 复制 `scripts/config.example.json` 为 `scripts/config.json`，填入持仓和规则
2. 设置环境变量 `ALPHAVANTAGE_API_KEY`（或其他数据源 Key）
3. 按需配置 SMTP 和 Sonos
4. 运行 `bash scripts/stock_alert.sh`

## 详细文档

请参阅 [SKILL.md](SKILL.md) 获取完整文档。

## 许可证

本项目采用 CC BY-NC-SA 4.0 许可证。
