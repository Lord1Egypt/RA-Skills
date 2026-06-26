# 📈 Stock Analysis Skill

**Intelligent Stock Analysis System for OpenClaw**

[![Version 2.0.1](https://img.shields.io/badge/version-2.0.1-green.svg)](https://github.com/leohuang8688/stock_analysis_skill)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

---

## 🆕 Latest Update (v2.0.1)

- ✅ **Alpha Vantage Integration** - US stocks fallback data source
- ✅ **Free Tier** - Daily close price data (500 requests/day)
- ✅ **Auto Fallback** - Yahoo Finance → Alpha Vantage
- ✅ **API Key Configured** - Ready to use

---

## ✨ Features

- 🌏 **Multi-Market Support** - A-shares, H-shares, US stocks
- 📊 **Real-Time Quotes** - Live market data
- 📈 **Technical Analysis** - MA, RSI, MACD, trend analysis
- 📰 **News Sentiment** - Real-time news and sentiment analysis
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

---

## 🚀 Quick Start

### Installation

```bash
cd ~/.openclaw/workspace/skills/stock_analysis_skill

# Install dependencies
pip3 install -r requirements.txt
```

### Configuration

```bash
# Copy example .env file
cp .env.example .env

# Edit .env and add your API keys
nano .env
```

**Required API Keys:**

```bash
# Tavily API (News sentiment analysis)
# Get from: https://tavily.com/
# Free tier: 100 searches/day
TAVILY_API_KEY=your_tavily_key

# Alpha Vantage API (US stocks fallback)
# Get from: https://www.alphavantage.co/
# Free tier: 500 requests/day
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key

# Tushare Token (Optional: A-share backup)
# Get from: https://tushare.pro/
TUSHARE_TOKEN=your_tushare_token
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

### CLI Usage

```bash
# Analyze single stock
python3 src/analyzer.py 600519

# Analyze multiple stocks
python3 src/analyzer.py 600519,hk00700,AAPL,TSLA
```

---

## 📊 Analysis Features

### Real-Time Quotes

- **A-shares**: Shanghai and Shenzhen stocks
- **H-shares**: Hong Kong stocks
- **US stocks**: NASDAQ, NYSE stocks
- **US indices**: SPX, DJI, IXIC

### Technical Analysis

- **Moving Averages**: MA5, MA10, MA20, MA60
- **Trend Detection**: Bullish, Bearish, Neutral
- **Momentum Indicators**: RSI, MACD
- **Support/Resistance**: Key price levels

### Decision Dashboard

Each stock analysis includes:

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
# Analyze your portfolio every day
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
# Analyze stocks in a specific sector
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

### Decision Dashboard Example

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

🔴 卖出 AAPL
当前价格：175.30
涨跌幅：-1.25%
建议：SELL
目标价：157.77
止损价：184.07
置信度：high
理由：技术趋势：bearish, 涨跌幅：-1.25%
--------------------------------------------------

⚠️ 免责声明：本报告仅供参考，不构成投资建议。股市有风险，投资需谨慎。
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
- AI recommendations use simple scoring (can be enhanced with LLM)

---

## 💰 Pricing

### Free Data Sources

- **AkShare**: Free A-share data
- **Yahoo Finance**: Free US/HK data (with delays)
- **Basic Analysis**: Free

### Optional Paid APIs

- **Tavily**: News search (free tier: 100 searches/day)
- **Premium Data**: Real-time quotes (varies by provider)

---

## 📞 Support

- **GitHub Issues**: https://github.com/leohuang8688/stock_analysis_skill/issues
- **Documentation**: See README.md for detailed guide

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

### CLI 使用

```bash
# 分析单只股票
python3 src/analyzer.py 600519

# 分析多只股票
python3 src/analyzer.py 600519,hk00700,AAPL,TSLA
```

---

## 📊 分析功能

### 实时行情

- **A 股** - 上海和深圳股票
- **港股** - 香港股票
- **美股** - NASDAQ、NYSE 股票
- **美股指数** - SPX、DJI、IXIC

### 技术分析

- **移动平均线** - MA5、MA10、MA20、MA60
- **趋势检测** - 牛市、熊市、中性
- **动量指标** - RSI、MACD
- **支撑/阻力** - 关键价格位

### 决策仪表盘

每只股票分析包含：

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
# 分析特定行业的股票
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

### 决策仪表盘示例

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

🔴 卖出 AAPL
当前价格：175.30
涨跌幅：-1.25%
建议：SELL
目标价：157.77
止损价：184.07
置信度：high
理由：技术趋势：bearish, 涨跌幅：-1.25%
--------------------------------------------------

⚠️ 免责声明：本报告仅供参考，不构成投资建议。股市有风险，投资需谨慎。
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
- AI 建议使用简单评分（可用 LLM 增强）

---

## 💰 定价

### 免费数据源

- **AkShare** - 免费 A 股数据
- **Yahoo Finance** - 免费美/港数据（有延迟）
- **基础分析** - 免费

### 可选付费 API

- **Tavily** - 新闻搜索（免费层：100 次/天）
- **高级数据** - 实时行情（因供应商而异）

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
