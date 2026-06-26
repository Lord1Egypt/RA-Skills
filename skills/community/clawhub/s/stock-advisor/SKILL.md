---
name: stock-advisor
description: 你的私人 AI 投顾。提供 A 股个股深度多维分析、持仓管理。
metadata.clawdbot:
  version: 1.0.0
  author: Antigravity
  files:
    - scripts/*
    - data/*
requires.env:
  - STOCK_ADVISOR_API_URL: "Stock Advisor Pro API 地址 (例如: http://localhost:8000 或 https://api.daas.ai)"
  - STOCK_ADVISOR_API_KEY: "您的 DaaS 订阅密钥 (API Key)"
---

# Stock Advisor Pro

你的私人 AI 投资顾问，专为 A 股打造。本插件提供个股深度扫描、持仓管理、行情实时监控及个性化投资建议。

## 主要功能

- **深度扫描**：多维评分（基本面、资金面、技术面、情绪面）+ AI 深度解读。
- **持仓管理**：记录你的 A 股持仓，分析盈亏。
- **隐私保护**：所有持仓和预警数据均保存在本地，绝不上云。

## 🌐 外部端点 (External Endpoints)

本插件需要连接到 Stock Advisor Pro API 后端。
- **默认地址**: `http://localhost:8000`
- **环境变量**: `STOCK_ADVISOR_API_URL`

## 🛡️ 安全与隐私 (Security & Privacy)

- **本地优先**: 所有持仓数据仅保存在本地 `data/portfolio.json`。
- **无追踪**: 插件不会收集或上传任何个人交易行为数据。
- **信任声明**: 本插件遵循 OpenClaw 安全规范，所有脚本逻辑透明可查。

## 使用命令

### 1. 个股分析
帮我分析个股的当前状态和潜在风险。
- `uv run {baseDir}/scripts/scan.py <股票代码>`

### 2. 持仓管理
查看或管理你的本地持仓。
- `uv run {baseDir}/scripts/portfolio.py show` - 查看当前持仓
- `uv run {baseDir}/scripts/portfolio.py add <代码> --cost <单价> --quantity <股数>` - 添加持仓
- `uv run {baseDir}/scripts/portfolio.py remove <代码>` - 删除持仓
