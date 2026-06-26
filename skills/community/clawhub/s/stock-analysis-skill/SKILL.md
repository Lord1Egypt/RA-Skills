# 📈 Stock Analysis Skill

**Intelligent Stock Analysis System for OpenClaw**

[![Version 2.0.1](https://img.shields.io/badge/version-2.0.1-green.svg)](https://github.com/leohuang8688/stock_analysis_skill)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

---

## 🆕 Latest Update (v2.0.1)

- ✅ **Alpha Vantage Integration** - US stocks fallback
- ✅ **Free Tier** - Daily close price (500 requests/day)
- ✅ **Auto Fallback** - Yahoo Finance → Alpha Vantage

---

## 🔐 Required Environment Variables

**Required:**

| Variable | Description | Required | How to Get |
|----------|-------------|----------|------------|
| `STOCK_LIST` | Stock codes to analyze (comma-separated) | ✅ Yes | Your stock list |

**Optional but Recommended:**

| Variable | Description | Required | How to Get | Free Tier |
|----------|-------------|----------|------------|-----------|
| `TAVILY_API_KEY` | Tavily Search API key (news sentiment) | ⚠️ Optional | https://tavily.com/ | 100 searches/day |
| `ALPHA_VANTAGE_API_KEY` | Alpha Vantage API key (US stocks fallback) | ⚠️ Optional | https://www.alphavantage.co/ | 500 requests/day |
| `TUSHARE_TOKEN` | Tushare Pro token (A-share backup) | ⚠️ Optional | https://tushare.pro/ | Requires credits |

**Optional Configuration:**

| Variable | Description | Default |
|----------|-------------|---------|
| `BIAS_THRESHOLD` | Deviation threshold (%) | 5.0 |
| `NEWS_MAX_AGE_DAYS` | News age limit (days) | 3 |

**Notes:**
- Without `TAVILY_API_KEY`: News sentiment analysis will be disabled
- Without `ALPHA_VANTAGE_API_KEY`: US stocks may fail during Yahoo Finance rate limits
- Without `TUSHARE_TOKEN`: A-share fallback to efinance only

---

## ✨ Features

- 🌏 **Multi-Market Support** - A-shares, H-shares, US stocks
- 📊 **Real-Time Quotes** - Live market data
- 📈 **Technical Analysis** - MA, RSI, MACD, trend analysis
- 📰 **News Sentiment Analysis** - Real-time news search with Tavily API
- 🤖 **AI Decision Dashboard** - Intelligent buy/sell/hold recommendations
- 📱 **Multi-Channel Notifications** - Uses OpenClaw's built-in messaging
- ⏰ **Scheduled Analysis** - Automated daily analysis
- 🎯 **Precise Price Points** - Exact entry, target, and stop-loss prices
- 🔄 **Multi-Source Fallback** - Automatic data source switching

### 📊 Data Source Hierarchy

| Market | Primary | Fallback | Status |
|--------|---------|----------|--------|
| **A-shares** | AkShare | efinance ✅ | ✅ Real-time |
| **HK stocks** | Yahoo Finance | - | ⚠️ Rate limit |
| **US stocks** | Yahoo Finance | Alpha Vantage ✅ | ✅ Daily close |

### 📰 News Sentiment Features

- **Real-time News Search** - Powered by Tavily Search API
- **Sentiment Scoring** - Positive/Negative/Neutral analysis
- **Keyword Analysis** - Detects bullish/bearish keywords
- **News Count** - Number of relevant news articles
- **Integration** - Sentiment affects buy/sell recommendations

---

## 🚀 Quick Start

### Installation

```bash
cd ~/.openclaw/workspace/skills/stock_analysis_skill

# Install dependencies
pip3 install -r requirements.txt
```

### Configuration

**Step 1: Copy environment template**

```bash
cp .env.example .env
```

**Step 2: Edit .env file**

```bash
nano .env
```

**Step 3: Add your API keys**

```bash
# Required: Your stock list
STOCK_LIST=600519,hk00700,AAPL,TSLA

# Recommended: Tavily API (news sentiment)
# Get free key: https://tavily.com/
TAVILY_API_KEY=your_tavily_key_here

# Recommended: Alpha Vantage (US stocks fallback)
# Get free key: https://www.alphavantage.co/support/#api-key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here

# Optional: Tushare Pro token (A-share backup)
# Get token: https://tushare.pro/
TUSHARE_TOKEN=your_tushare_token_here

# Optional: Analysis settings
BIAS_THRESHOLD=5.0
NEWS_MAX_AGE_DAYS=3
```

### Basic Usage

```python
from src.analyzer import analyze_stocks

# Analyze single stock
result = analyze_stocks(['600519'])
print(result)

# Analyze multiple stocks
result = analyze_stocks(['600519', 'hk00700', 'AAPL', 'TSLA'])
print(result)
```

---

## 📊 Analysis Features

### Multi-Market Support

- **A-shares**: Shanghai and Shenzhen stocks (600519, 000001, etc.)
- **H-shares**: Hong Kong stocks (hk00700, hk09988, etc.)
- **US stocks**: NASDAQ, NYSE stocks (AAPL, TSLA, etc.)
- **US indices**: SPX, DJI, IXIC

### Technical Indicators

- **Moving Averages**: MA5, MA10, MA20, MA60
- **Trend Detection**: Bullish, Bearish, Neutral
- **Momentum**: RSI, MACD
- **Support/Resistance**: Key price levels

### Decision Dashboard

Each analysis includes:

- **Recommendation**: BUY / SELL / HOLD
- **Action**: 🟢 Buy / 🟡 Hold / 🔴 Sell
- **Score**: 0-100 confidence score
- **Current Price**: Real-time price
- **Target Price**: Profit-taking level
- **Stop Loss**: Risk management level
- **Confidence**: High / Medium / Low
- **Reasoning**: Clear explanation

---

## 📁 Project Structure

```
stock_analysis_skill/
├── src/
│   └── analyzer.py         # Main analysis engine
├── .env.example            # Environment variables template
├── requirements.txt        # Python dependencies
├── SKILL.md                # This file
└── README.md               # Documentation
```

---

## 🎯 Use Cases

### 1. Daily Portfolio Review

```python
# Analyze your portfolio daily
stocks = ['600519', 'hk00700', 'AAPL', 'TSLA']
result = analyze_stocks(stocks)
```

### 2. Market Overview

```python
# Analyze market indices
indices = ['SPX', 'DJI', 'IXIC']
result = analyze_stocks(indices)
```

### 3. Sector Analysis

```python
# Analyze tech sector
tech_stocks = ['AAPL', 'MSFT', 'GOOGL', 'NVDA']
result = analyze_stocks(tech_stocks)
```

---

## ⚙️ Configuration

### Environment Variables

```bash
# Stock list (comma-separated)
STOCK_LIST=600519,hk00700,AAPL,TSLA

# News search API (optional)
TAVILY_API_KEY=your_tavily_key

# Analysis settings
BIAS_THRESHOLD=5.0  # Deviation threshold (%)
NEWS_MAX_AGE_DAYS=3  # News age limit (days)
```

---

## 📝 Output Format

### Example Report

```
📊 股票智能分析报告

分析时间：2026-03-19 18:00
分析股票数：3
==================================================

🟢 买入 600519
当前价格：1850.50
涨跌幅：+2.35%
建议：BUY
目标价：2035.55
止损价：1757.98
置信度：high
理由：技术趋势：bullish, 涨跌幅：2.35%, 舆情：positive (0.75)
新闻：5 条相关新闻，正面情绪主导
--------------------------------------------------

🟡 观望 hk00700
当前价格：420.60
涨跌幅：-0.85%
建议：HOLD
目标价：378.54
止损价：441.63
置信度：medium
理由：技术趋势：neutral, 涨跌幅：-0.85%, 舆情：neutral (0.50)
新闻：3 条相关新闻，情绪中性
--------------------------------------------------

🔴 卖出 AAPL
当前价格：175.30
涨跌幅：-1.25%
建议：SELL
目标价：157.77
止损价：184.07
置信度：high
理由：技术趋势：bearish, 涨跌幅：-1.25%, 舆情：negative (0.30)
新闻：7 条相关新闻，负面情绪主导
--------------------------------------------------

⚠️ 免责声明：本报告仅供参考，不构成投资建议。
```

---

## ⚠️ Limitations

### Data Sources

- **A-shares**: AkShare (free, may have delays)
- **H-shares**: Yahoo Finance (free, 15-min delay)
- **US stocks**: Yahoo Finance (free, real-time for most)

### Analysis Accuracy

- Technical analysis is rule-based
- News sentiment requires API configuration
- AI recommendations use scoring system

---

## 💰 Pricing

### Free Data Sources

- **AkShare**: Free A-share data
- **Yahoo Finance**: Free US/HK data
- **Basic Analysis**: Free

### Optional Paid APIs

- **Tavily**: News search (free tier: 100 searches/day)

---

## 📞 Support

- **GitHub Issues**: https://github.com/leohuang8688/stock_analysis_skill/issues
- **Documentation**: See README.md

---

## 📄 License

MIT License - See LICENSE file for details.

---

## 👨‍💻 Author

**PocketAI for Leo** - OpenClaw Community

- GitHub: [@leohuang8688](https://github.com/leohuang8688)
- Contact: claw@pocketai.sg

---

**Happy Investing! 📈**

---

*Last Updated: 2026-03-19*  
*Version: 1.0.0*

---

---

# 📈 股票分析技能

**OpenClaw 智能股票分析系统**

---

## 🔐 环境变量配置

| 变量 | 说明 | 必需 |
|------|------|------|
| `STOCK_LIST` | 要分析的股票代码（逗号分隔） | ✅ 是 |
| `TAVILY_API_KEY` | Tavily Search API 密钥（新闻搜索） | ⚠️ 可选 |
| `BIAS_THRESHOLD` | 乖离率阈值 (%) | ⚠️ 可选 |
| `NEWS_MAX_AGE_DAYS` | 新闻时效上限 (天) | ⚠️ 可选 |

---

## ✨ 功能特性

- 🌏 **多市场支持** - A 股、港股、美股
- 📊 **实时行情** - 实时市场数据
- 📈 **技术分析** - 均线、RSI、MACD、趋势分析
- 📰 **新闻舆情** - 实时新闻和情绪分析
- 🤖 **AI 决策仪表盘** - 智能买入/卖出/持有建议
- 📱 **多渠道推送** - 使用 OpenClaw 内置消息功能
- ⏰ **定时分析** - 自动化每日分析
- 🎯 **精确点位** - 精确的买入、目标、止损价格

---

## 🚀 快速开始

### 安装

```bash
cd ~/.openclaw/workspace/skills/stock_analysis_skill

# 安装依赖
pip3 install -r requirements.txt
```

### 配置

```bash
# 复制示例 .env 文件
cp .env.example .env

# 编辑 .env 并添加 API 密钥
nano .env
```

### 基本使用

```python
from src.analyzer import analyze_stocks

# 分析单只股票
result = analyze_stocks(['600519'])
print(result)

# 分析多只股票
result = analyze_stocks(['600519', 'hk00700', 'AAPL', 'TSLA'])
print(result)
```

---

## 📊 分析功能

### 多市场支持

- **A 股** - 上海和深圳股票（600519, 000001 等）
- **港股** - 香港股票（hk00700, hk09988 等）
- **美股** - NASDAQ、NYSE 股票（AAPL, TSLA 等）
- **美股指数** - SPX, DJI, IXIC

### 技术指标

- **移动平均线** - MA5、MA10、MA20、MA60
- **趋势检测** - 牛市、熊市、中性
- **动量** - RSI、MACD
- **支撑/阻力** - 关键价格位

### 决策仪表盘

每次分析包含：

- **建议** - 买入 / 卖出 / 持有
- **操作** - 🟢 买入 / 🟡 持有 / 🔴 卖出
- **评分** - 0-100 置信度评分
- **当前价格** - 实时价格
- **目标价** - 获利了结位
- **止损价** - 风险管理位
- **置信度** - 高 / 中 / 低
- **理由** - 清晰解释

---

## 📁 项目结构

```
stock_analysis_skill/
├── src/
│   └── analyzer.py         # 主分析引擎
├── .env.example            # 环境变量模板
├── requirements.txt        # Python 依赖
├── SKILL.md                # 本文件
└── README.md               # 使用文档
```

---

## 🎯 使用案例

### 1. 每日投资组合审查

```python
# 每天分析你的投资组合
stocks = ['600519', 'hk00700', 'AAPL', 'TSLA']
result = analyze_stocks(stocks)
```

### 2. 市场概览

```python
# 分析市场指数
indices = ['SPX', 'DJI', 'IXIC']
result = analyze_stocks(indices)
```

### 3. 行业分析

```python
# 分析科技行业
tech_stocks = ['AAPL', 'MSFT', 'GOOGL', 'NVDA']
result = analyze_stocks(tech_stocks)
```

---

## ⚙️ 配置

### 环境变量

```bash
# 股票列表（逗号分隔）
STOCK_LIST=600519,hk00700,AAPL,TSLA

# 新闻搜索 API（可选）
TAVILY_API_KEY=your_tavily_key

# 分析设置
BIAS_THRESHOLD=5.0  # 乖离率阈值 (%)
NEWS_MAX_AGE_DAYS=3  # 新闻时效上限 (天)
```

---

## 📝 输出格式

### 示例报告

```
📊 股票智能分析报告

分析时间：2026-03-19 18:00
分析股票数：3
==================================================

🟢 买入 600519
当前价格：1850.50
涨跌幅：+2.35%
建议：BUY
目标价：2035.55
止损价：1757.98
置信度：high
理由：技术趋势：bullish, 涨跌幅：2.35%
--------------------------------------------------

🟡 观望 hk00700
当前价格：420.60
涨跌幅：-0.85%
建议：HOLD
目标价：378.54
止损价：441.63
置信度：medium
理由：技术趋势：neutral, 涨跌幅：-0.85%
--------------------------------------------------

⚠️ 免责声明：本报告仅供参考，不构成投资建议。
```

---

## ⚠️ 限制说明

### 数据来源

- **A 股** - AkShare（免费，可能有延迟）
- **港股** - Yahoo Finance（免费，15 分钟延迟）
- **美股** - Yahoo Finance（免费，大部分实时）

### 分析准确性

- 技术分析基于规则
- 新闻舆情需要 API 配置
- AI 建议使用评分系统

---

## 💰 定价

### 免费数据源

- **AkShare** - 免费 A 股数据
- **Yahoo Finance** - 免费美/港数据
- **基础分析** - 免费

### 可选付费 API

- **Tavily** - 新闻搜索（免费层：100 次/天）

---

## 📞 支持

- **GitHub Issues**: https://github.com/leohuang8688/stock_analysis_skill/issues
- **文档**: 详见 README.md

---

## 📄 许可证

MIT License - 详见 LICENSE 文件。

---

## 👨‍💻 作者

**PocketAI for Leo** - OpenClaw Community

- GitHub: [@leohuang8688](https://github.com/leohuang8688)
- 联系方式：claw@pocketai.sg

---

**Happy Investing! 📈**

---

*最后更新：* 2026-03-19  
*版本：* 1.0.0
