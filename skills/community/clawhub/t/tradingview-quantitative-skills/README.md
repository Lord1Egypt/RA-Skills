# TradingView Quantitative Investment Analysis Skill

[English](README.md) | [简体中文](README.zh.md)

[![Install with skills](https://img.shields.io/badge/install-skills-blue)](https://skills.sh/hypier/tradingview-quantitative-skills/tradingview-quantitative)
[![GitHub](https://img.shields.io/github/stars/hypier/tradingview-quantitative-skills?style=social)](https://github.com/hypier/tradingview-quantitative-skills)

Professional quantitative investment analysis system based on TradingView data providing intelligent stock screening, technical pattern recognition, market review, risk management, and event-driven analysis.

## Installation

Install this skill with one command:

```bash
npx skills add hypier/tradingview-quantitative-skills
```

## Features

- ✅ **Smart Stock Screening** - Multi-factor comprehensive scoring, dual filtering of technical + fundamental aspects
- 📊 **Technical Pattern Recognition** - Automatically identify classic patterns, provide confidence assessment and trading strategies
- 📈 **Market Review** - Track hot sectors, capital flows, discover investment opportunities
- 🛡️ **Risk Management** - Position suggestions, stop-loss/take-profit, volatility analysis
- 📰 **Event-Driven Analysis** - Track earnings, policies, news, analyze market impact
- 🔍 **Deep Individual Stock Analysis** - Multi-timeframe technical analysis + fundamentals + news comprehensive evaluation
- 💰 **Fundamental Screening** - High dividend, low valuation, profitability screening
- 🔄 **Sector Rotation** - Identify strong sectors and rotation trends

## Quick Start

### 1. Configure MCP Server

Add TradingView MCP server to Cursor or Claude Desktop configuration file:

**Configuration file paths**:
- **macOS/Linux**: `~/Library/Application Support/Cursor/mcp_config.json`
- **Windows**: `%APPDATA%\Cursor\mcp_config.json`

> **📖 Security Notice**: Please read [SECURITY.md](SECURITY.md) for important information about API key management and data privacy.

#### Method 1: Use RapidAPI (Recommended, Ready to Use)

Visit https://rapidapi.com/hypier/api/tradingview-data1 to apply for a free API Key, then configure:

> **⚠️ SECURITY WARNING**: Never commit your real API key to version control. Keep your API key secure and private. The example below uses a placeholder that you must replace with your actual key.

```json
{
  "mcpServers": {
    "RapidAPI Hub - TradingView Data": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.rapidapi.com",
        "--header",
        "x-api-host: tradingview-data1.p.rapidapi.com",
        "--header",
        "x-api-key: <YOUR_RAPIDAPI_KEY_HERE>"
      ]
    }
  }
}
```

**Configuration Steps**:
1. Visit https://rapidapi.com/hypier/api/tradingview-data1
2. Register/login to RapidAPI account
3. Subscribe to free plan (Free tier)
4. Copy your API Key
5. Replace `<YOUR_RAPIDAPI_KEY_HERE>` in the configuration above with your actual API key
6. Restart Cursor/Claude Desktop

#### Method 2: Use Self-Built JWT Token Service

If you already have a RapidAPI Key, you can use a self-built JWT Token service:

**Step 1**: Generate JWT Token

> **⚠️ SECURITY WARNING**: Replace `<YOUR_RAPIDAPI_KEY_HERE>` with your actual API key. Never share or commit your API key.

```bash
curl --request POST \
  --url https://tradingview-data1.p.rapidapi.com/api/mcp/generate \
  --header 'Content-Type: application/json' \
  --header 'x-rapidapi-host: tradingview-data1.p.rapidapi.com' \
  --header 'x-rapidapi-key: <YOUR_RAPIDAPI_KEY_HERE>' \
  --data '{}'
```

**Step 2**: Configure the returned JWT Token to MCP

> **⚠️ SECURITY WARNING**: Replace `<YOUR_JWT_TOKEN_HERE>` with the actual JWT token from Step 1. Never commit tokens to version control.

```json
{
  "mcpServers": {
    "tradingview": {
      "type": "streamable-http",
      "url": "https://mcp.example-mcp-server.com/mcp",
      "headers": {
        "Authorization": "Bearer <YOUR_JWT_TOKEN_HERE>",
        "Accept": "application/json, text/event-stream"
      }
    }
  }
}
```


#### Recommended Configuration

For most users, **Method 1 (RapidAPI) is recommended** because:
- ✅ No need to manually manage token expiration
- ✅ Simple configuration, one-time setup permanent validity
- ✅ Free quota sufficient for personal use
- ✅ Automatic authentication and retry handling

### 2. Verify Installation

After restart, enter in conversation:

```
Please call tradingview_get_metadata to get the list of supported markets
```

If it returns the market list (america, china, japan, etc.), the configuration is successful.

### 3. Start Using

Just ask questions in natural language, for example:

- "Help me select strong stocks from China A-shares"
- "Analyze the technical patterns of BTC/USDT"
- "How is the China A-share market today?"
- "I have 100k capital, want to buy a certain stock, how much should I buy?"
- "Generate today's China financial news briefing"

## Usage Examples

### Smart Stock Screening

```
Help me select stocks from China A-share technology sector that meet the following conditions:
- Technical: RSI 30-70, MACD golden cross
- Fundamental: PE < 30, ROE > 15%
- Market cap: above 5 billion
```

### Individual Stock Analysis

```
Deep analysis of Puyuan Information (688118), including:
- Multi-timeframe technical analysis
- Fundamental data
- Recent news
- Buy recommendations and risk warnings
```

### Market Review

```
How is the China A-share market today? Analyze hot sectors and investment opportunities
```

### Risk Management

```
I have 100k capital, want to buy Puyuan Information, how much should I buy?
Give me position suggestions, stop-loss/take-profit levels and risk-reward ratio
```

## Supported Markets

- 🇨🇳 **China A-shares** - SSE, SZSE, BSE
- 🇺🇸 **United States** - NYSE, NASDAQ
- 🇭🇰 **Hong Kong** - HKEX
- 🇯🇵 **Japan** - TSE
- 🇰🇷 **South Korea** - KRX
- 🪙 **Cryptocurrency** - Binance, Coinbase, OKX, etc.
- 💱 **Forex** - Major currency pairs
- 📦 **Futures** - Commodity, index futures

For complete market list, see `references/api-documentation.md`.

## Frequently Asked Questions

### Q: What to do if prompted "MCP server not found"?

**A**: Check the following points:
1. Confirm `mcp_config.json` path is correct
2. Confirm `tradingview-mcp-server` is correctly built (run `npm run build`)
3. Confirm paths in configuration file use absolute paths
4. Restart Windsurf/Claude Desktop

### Q: What to do if authentication fails?

**A**: 
1. Confirm TradingView account password is correct
2. Confirm account has logged into TradingView website (first time requires web login)
3. If using two-factor authentication, may need app-specific password

### Q: How to get China A-share data?

**A**: 
```
# First get market codes
tradingview_get_metadata(type='markets')

# Use market_code='china' to get A-share data
tradingview_get_leaderboard(
  asset_type='stocks', 
  tab='gainers',
  market_code='china'
)
```

### Q: Which technical indicators are supported?

**A**: When calling `tradingview_get_ta`, set `include_indicators=true` to get:
- Trend indicators: SMA, EMA, MACD, ADX
- Momentum indicators: RSI, Stoch, CCI, Williams %R
- Volume indicators: Volume, MFI
- Support resistance: Pivot Points, Fibonacci
- Others: ATR, Beta, Bollinger Bands

### Q: How to get historical K-line data?

**A**:
```
tradingview_get_price(
  symbol='SSE:600519',    # Exchange:Code
  timeframe='D',          # 1/5/15/30/60/240/D/W/M
  range=120               # Max 500 K-lines
)
```

### Q: Which languages are supported for news data?

**A**: Supports 19 languages, commonly used are:
- `zh-Hans` - Simplified Chinese
- `en` - English
- `ja` - Japanese
- `ko` - Korean

Complete list: `tradingview_get_metadata(type='languages')`

## Directory Structure

```
tradingview-quantitative-skills/
├── README.md                    # This file - User guide
├── SKILL.md                     # AI skill description (for AI)
├── SECURITY.md                  # Security policy and best practices
├── .gitignore                   # Git ignore patterns for sensitive files
├── references/                  # Reference materials
│   ├── api-documentation.md     # Complete API documentation and metadata dictionary
│   ├── mcp-tools-guide.md       # MCP tools usage guide
│   ├── technical-analysis.md    # Technical analysis methodology
│   ├── pattern-library.md       # Pattern recognition library
│   ├── risk-management.md       # Risk management methods
│   └── china-a-stock-examples.md # China A-share practical cases
└── workflows/                   # Workflows (15 total)
    ├── smart-screening.md       # Smart stock screening
    ├── pattern-recognition.md   # Pattern recognition
    ├── market-review.md         # Market review
    ├── risk-assessment.md       # Risk assessment
    ├── event-analysis.md        # Event analysis
    ├── deep-stock-analysis.md   # Deep individual stock analysis
    ├── fundamental-screening.md # Fundamental screening
    ├── sector-rotation.md       # Sector rotation
    └── ...                      # Other workflows
```

## Advanced Usage

### Custom Screening Criteria

Refer to `workflows/smart-screening.md` and `workflows/fundamental-screening.md`, you can combine:
- Technical indicator screening (RSI, MACD, ADX, etc.)
- Fundamental screening (PE, PB, ROE, dividend yield, etc.)
- Market cap, volume screening
- Industry sector screening

### Multi-Market Comparative Analysis

```
Compare today's financial news from China, US, and Japan, analyze market differences
```

### Portfolio Strategy Backtesting

Combining historical K-line data and technical indicators, simple strategy validation can be performed.

## Technical Support

- **API Documentation**: `references/api-documentation.md`
- **Tools Guide**: `references/mcp-tools-guide.md`
- **Practical Cases**: `references/us-stock-examples.md`

## Disclaimer

This tool is for learning and research purposes only and does not constitute any investment advice. Investing involves risks; enter the market cautiously. Any investment decisions made using this tool are at your own risk.

## License

MIT License
