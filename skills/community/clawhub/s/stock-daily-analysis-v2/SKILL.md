---
name: stock-daily-analysis
description: LLM驱动的每日股票分析系统完整版 v2.1。支持A股/港股/美股智能分析、决策仪表盘、大盘复盘、板块分析、Agent问股、多渠道推送。提供技术面+基本面综合分析。触发词：股票分析、分析股票、每日分析、大盘复盘、板块分析、问股。
---

# Daily Stock Analysis v2.1 (完整集成版)

基于 LLM 的 A/H/美股智能分析 Skill，为 OpenClaw 提供全面的股票分析能力。

## 🎯 项目定位

本项目是 [ZhuLinsen/daily_stock_analysis](https://github.com/ZhuLinsen/daily_stock_analysis) 的 **OpenClaw Skill 完整集成版**。

### v2.1 更新内容

- ✅ 添加飞书卡片消息推送
- ✅ 添加并发批量分析 (`analyze_stocks_concurrent`)
- ✅ 添加 `daily_push()` 每日定时推送函数
- ✅ 添加 Markdown 报告格式生成
- ✅ 优化错误处理

### 功能对比

| 功能 | v1.x | v2.0 | v2.1 |
|------|------|------|------|
| 技术面分析 | ✅ | ✅ | ✅ |
| 基本面分析 | ❌ | ✅ | ✅ |
| 大盘复盘 | ❌ | ✅ | ✅ |
| 板块分析 | ❌ | ✅ | ✅ |
| Agent 问股 | ❌ | ✅ | ✅ |
| 多渠道推送 | ❌ | ⚙️ | ✅ |
| 并发分析 | ❌ | ❌ | ✅ |
| 飞书卡片 | ❌ | ❌ | ✅ |

## 🚀 快速开始

### 安装

```bash
# 依赖安装
pip3 install akshare pandas numpy requests openai yfinance

# 配置
cp config.example.json config.json
# 编辑 config.json 填入你的 API Key
```

### 基本使用

```python
from scripts.analyzer_v2 import (
    analyze_stock,              # 股票分析(含基本面)
    analyze_stocks,            # 批量分析(串行)
    analyze_stocks_concurrent, # 批量分析(并发)
    market_review,             # 大盘复盘
    sector_analysis,           # 板块分析
    agent_query,               # Agent问股
    push_report,               # 推送报告
    daily_push                 # 每日推送
)

# 分析单只股票
result = analyze_stock('600519')

# 并发批量分析 (推荐)
results = analyze_stocks_concurrent(['600519', '000858', '601318'], max_workers=5)

# 大盘复盘
cn_market = market_review('cn')

# 板块分析
sectors = sector_analysis()

# Agent问股
answer = agent_query("推荐新能源股票")

# 每日定时推送 (配合 Cron 使用)
daily_push()
```

### 命令行使用

```bash
# 分析股票
python -m scripts.analyzer_v2 analyze 600519 AAPL

# 并发分析 (更快)
python -m scripts.analyzer_v2 concurrent 600519 000858 601318

# 大盘复盘
python -m scripts.analyzer_v2 review cn
python -m scripts.analyzer_v2 review both

# 板块分析
python -m scripts.analyzer_v2 sector

# Agent 问股
python -m scripts.analyzer_v2 agent 推荐银行股

# 每日推送
python -m scripts.analyzer_v2 push
```

## 📊 功能特性

| 功能 | 状态 | 说明 |
|------|------|------|
| A股分析 | ✅ | 支持个股、ETF |
| 港股分析 | ✅ | 支持港股通标的 |
| 美股分析 | ✅ | 支持主流美股、指数 |
| 技术面分析 | ✅ | MA/MACD/RSI/乖离率/量能 |
| 基本面分析 | ✅ | 估值、机构持仓、资金流向 |
| AI 决策建议 | ✅ | DeepSeek/Gemini |
| 大盘复盘 | ✅ | A股/美股指数、涨跌统计 |
| 板块分析 | ✅ | 行业/概念板块涨跌榜 |
| Agent 问股 | ✅ | 策略问答、股票推荐 |
| 飞书推送 | ✅ | 卡片消息格式 |
| 企业微信 | ✅ | Markdown 格式 |
| Telegram | ✅ | Markdown 格式 |
| Discord | ✅ | 文本格式 |
| 邮件 | ✅ | SMTP 发送 |

## 🏗️ 项目结构

```
stock-daily-analysis/
├── SKILL.md                 # OpenClaw Skill 定义
├── README.md                # 项目文档
├── LICENSE                  # MIT 许可证
├── config.example.json      # 配置示例
├── config.json              # 用户配置 (gitignore)
├── requirements.txt         # Python 依赖
└── scripts/
    ├── analyzer_v2.py       # 主入口 (v2.1)
    ├── analyzer.py          # 主入口 (基础版)
    ├── data_fetcher.py     # 数据获取
    ├── market_data_bridge.py # market-data skill 桥接
    ├── trend_analyzer.py   # 技术分析引擎
    ├── ai_analyzer.py     # AI 分析模块
    ├── fundamental.py      # 基本面分析
    ├── market.py          # 大盘复盘
    ├── sector.py          # 板块分析
    ├── agent.py           # Agent 问股
    └── notifier.py        # 报告输出/推送
```

## 🔧 配置说明

### 完整配置示例

```json
{
  "ai": {
    "provider": "openai",
    "api_key": "sk-your-deepseek-key",
    "base_url": "https://api.deepseek.com/v1",
    "model": "deepseek-chat"
  },
  "data": {
    "days": 60,
    "realtime_enabled": true
  },
  "fundamental": {
    "enabled": true,
    "tushare_token": ""
  },
  "stock_list": "600519,000858,601318,600036",
  "push": {
    "enabled": true,
    "feishu_webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
  }
}
```

### 推送渠道配置

| 渠道 | 配置项 | 说明 |
|------|--------|------|
| 飞书 | `feishu_webhook` | 卡片消息，更美观 |
| 企业微信 | `wechat_webhook` | Markdown 格式 |
| Telegram | `telegram_token` + `telegram_chat_id` | 需要 Bot Token |
| Discord | `discord_webhook` | Webhook URL |
| 邮件 | `email_sender` + `email_password` + `email_receivers` | 支持 QQ 邮箱 |

## 📈 返回数据格式

```python
{
    'code': '600519',
    'name': '贵州茅台',
    'market': 'cn',
    'technical_indicators': {
        'trend_status': '强势多头',
        'signal_score': 75,
        'buy_signal': '买入'
    },
    'fundamental': {
        'valuation': {'pe': '25.3', 'pb': '5.2'},
        'capital_flow': {'main_inflow': '3.2亿'}
    },
    'ai_analysis': {
        'sentiment_score': 75,
        'operation_advice': '买入',
        'confidence_level': '高',
        'target_price': '1550',
        'stop_loss': '1420'
    }
}
```

## 💬 Agent 问股

内置策略:
- `bull_trend` - 多头趋势
- `golden_cross` - 均线金叉
- `breakout` - 突破新高
- `value` - 价值投资
- `momentum` - 动量策略

示例问题:
- "推荐银行股"
- "分析一下茅台"
- "什么是均线金叉策略"
- "帮我选一只新能源股票"

## ⏰ 定时任务 (Cron)

配合 OpenClaw Cron 使用：

```python
# 每天 18:00 执行分析并推送
cron job add --schedule "cron:0 18 * * 1-5" \
  --payload '{"kind":"agentTurn","message":"执行 daily_push()"}'
```

## ⚠️ 免责声明

本项目仅供学习研究使用，不构成任何投资建议。股市有风险，投资需谨慎。

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- 数据来源：[akshare](https://github.com/akfamily/akshare)
- 灵感来源：[ZhuLinsen/daily_stock_analysis](https://github.com/ZhuLinsen/daily_stock_analysis)
- 平台支持：[OpenClaw](https://openclaw.ai)

---

**Made with ❤️ for OpenClaw**
