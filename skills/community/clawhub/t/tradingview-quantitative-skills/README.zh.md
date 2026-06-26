# TradingView 量化投资分析技能

[English](README.md) | [简体中文](README.zh.md)

[![Install with skills](https://img.shields.io/badge/install-skills-blue)](https://skills.sh/hypier/tradingview-quantitative-skills/tradingview-quantitative)
[![GitHub](https://img.shields.io/github/stars/hypier/tradingview-quantitative-skills?style=social)](https://github.com/hypier/tradingview-quantitative-skills)

基于 TradingView 数据的专业量化投资分析系统，提供智能选股、技术形态识别、市场复盘、风险管理、事件驱动分析等功能。

## 安装

一键安装此技能：

```bash
npx skills add hypier/tradingview-quantitative-skills
```

## 功能特性

- ✅ **智能选股** - 多因子综合评分，技术面+基本面双重筛选
- 📊 **技术形态识别** - 自动识别经典形态，提供置信度评估和交易策略
- 📈 **市场复盘** - 追踪热点板块、资金流向，发现投资机会
- 🛡️ **风险管理** - 仓位建议、止损止盈、波动率分析
- 📰 **事件驱动分析** - 追踪财报、政策、新闻，分析市场影响
- 🔍 **个股深度分析** - 多时间框架技术分析 + 基本面 + 新闻综合评估
- 💰 **基本面筛选** - 高股息、低估值、盈利能力筛选
- 🔄 **板块轮动** - 识别强势板块和轮动趋势

## 快速开始

### 1. 配置 MCP Server

将 TradingView MCP server 添加到 Cursor 或 Claude Desktop 配置文件：

**配置文件路径**：
- **macOS/Linux**: `~/Library/Application Support/Cursor/mcp_config.json`
- **Windows**: `%APPDATA%\\Cursor\\mcp_config.json`

> **📖 安全提示**：请阅读 [SECURITY.md](SECURITY.md) 了解 API 密钥管理和数据隐私的重要信息。

#### 方法一：使用 RapidAPI（推荐，开箱即用）

访问 https://rapidapi.com/hypier/api/tradingview-data1 申请免费 API Key，然后配置：

> **⚠️ 安全警告**：切勿将真实的 API 密钥提交到版本控制系统。请妥善保管您的 API 密钥。下面的示例使用占位符，您必须将其替换为实际的密钥。

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

**配置步骤**：
1. 访问 https://rapidapi.com/hypier/api/tradingview-data1
2. 注册/登录 RapidAPI 账号
3. 订阅免费计划（Free tier）
4. 复制你的 API Key
5. 将上面配置中的 `<YOUR_RAPIDAPI_KEY_HERE>` 替换为你的实际 API 密钥
6. 重启 Cursor/Claude Desktop

#### 方法二：使用自建 JWT Token 服务

如果你已有 RapidAPI Key，可以使用自建 JWT Token 服务：

**步骤 1**：生成 JWT Token

> **⚠️ 安全警告**：将 `<YOUR_RAPIDAPI_KEY_HERE>` 替换为你的实际 API 密钥。切勿分享或提交你的 API 密钥。

```bash
curl --request POST \
  --url https://tradingview-data1.p.rapidapi.com/api/mcp/generate \
  --header 'Content-Type: application/json' \
  --header 'x-rapidapi-host: tradingview-data1.p.rapidapi.com' \
  --header 'x-rapidapi-key: <YOUR_RAPIDAPI_KEY_HERE>' \
  --data '{}'
```

**步骤 2**：将返回的 JWT Token 配置到 MCP

> **⚠️ 安全警告**：将 `<YOUR_JWT_TOKEN_HERE>` 替换为步骤 1 返回的实际 JWT token。切勿将 token 提交到版本控制系统。

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


#### 推荐配置

对于大多数用户，**推荐使用方法一（RapidAPI）**，因为：
- ✅ 无需手动管理 token 过期
- ✅ 配置简单，一次配置永久有效
- ✅ 免费额度足够个人使用
- ✅ 自动处理认证和重试

### 2. 验证安装

重启后，在对话中输入：

```
请调用 tradingview_get_metadata 获取支持的市场列表
```

如果返回市场列表（america, china, japan 等），说明配置成功。

### 3. 开始使用

直接用自然语言提问即可，例如：

- "帮我从 A 股科技板块中筛选强势股"
- "分析 BTC/USDT 的技术形态"
- "今天 A 股市场怎么样？"
- "我有 10 万资金，想买某只股票，应该买多少？"
- "生成今日中国财经新闻简报"

## 使用示例

### 智能选股

```
帮我从 A 股科技板块中筛选符合以下条件的股票：
- 技术面：RSI 30-70，MACD 金叉
- 基本面：PE < 30，ROE > 15%
- 市值：50 亿以上
```

### 个股分析

```
深度分析普元信息（688118），包括：
- 多时间框架技术分析
- 基本面数据
- 近期新闻
- 买入建议和风险提示
```

### 市场复盘

```
今天 A 股市场怎么样？分析热点板块和投资机会
```

### 风险管理

```
我有 10 万资金，想买普元信息，应该买多少？
给我仓位建议、止损止盈位和风险收益比
```

## 支持的市场

- 🇨🇳 **中国 A 股** - 上交所、深交所、北交所
- 🇺🇸 **美国** - 纽交所、纳斯达克
- 🇭🇰 **香港** - 港交所
- 🇯🇵 **日本** - 东京证券交易所
- 🇰🇷 **韩国** - 韩国交易所
- 🪙 **加密货币** - Binance、Coinbase、OKX 等
- 💱 **外汇** - 主要货币对
- 📦 **期货** - 商品、指数期货

完整市场列表见 `references/api-documentation.md`。

## 常见问题

### Q: 提示"找不到 MCP server"怎么办？

**A**: 检查以下几点：
1. 确认 `mcp_config.json` 路径正确
2. 确认 `tradingview-mcp-server` 已正确构建（运行 `npm run build`）
3. 确认配置文件中的路径使用绝对路径
4. 重启 Windsurf/Claude Desktop

### Q: 认证失败怎么办？

**A**:
1. 确认 TradingView 账号密码正确
2. 确认账号已登录过 TradingView 网站（首次需要网页登录）
3. 如果使用了两步验证，可能需要应用专用密码

### Q: 如何获取 A 股数据？

**A**:
```
# 先获取市场代码
tradingview_get_metadata(type='markets')

# 使用 market_code='china' 获取 A 股数据
tradingview_get_leaderboard(
  asset_type='stocks',
  tab='gainers',
  market_code='china'
)
```

### Q: 支持哪些技术指标？

**A**: 调用 `tradingview_get_ta` 时设置 `include_indicators=true` 可获取：
- 趋势指标：SMA、EMA、MACD、ADX
- 动量指标：RSI、Stoch、CCI、Williams %R
- 成交量指标：Volume、MFI
- 支撑阻力：Pivot Points、Fibonacci
- 其他：ATR、Beta、Bollinger Bands

### Q: 如何获取历史 K 线数据？

**A**:
```
tradingview_get_price(
  symbol='SSE:600519',    # 交易所:代码
  timeframe='D',          # 1/5/15/30/60/240/D/W/M
  range=120               # 最多 500 根 K 线
)
```

### Q: 新闻数据支持哪些语言？

**A**: 支持 19 种语言，常用的有：
- `zh-Hans` - 简体中文
- `en` - 英语
- `ja` - 日语
- `ko` - 韩语

完整列表：`tradingview_get_metadata(type='languages')`

## 目录结构

```
tradingview-quantitative-skills/
├── README.md                    # 本文件 - 用户指南
├── README.zh.md                 # 中文版用户指南
├── SKILL.md                     # AI 技能描述（给 AI 看的）
├── SECURITY.md                  # 安全策略和最佳实践
├── .gitignore                   # Git 忽略敏感文件的模式
├── references/                  # 参考资料
│   ├── api-documentation.md     # 完整 API 文档和元数据字典
│   ├── mcp-tools-guide.md       # MCP 工具使用指南
│   ├── technical-analysis.md    # 技术分析方法论
│   ├── pattern-library.md       # 形态识别库
│   ├── risk-management.md       # 风险管理方法
│   └── china-a-stock-examples.md # A 股实战案例
└── workflows/                   # 工作流（共 15 个）
    ├── smart-screening.md       # 智能选股
    ├── pattern-recognition.md   # 形态识别
    ├── market-review.md         # 市场复盘
    ├── risk-assessment.md       # 风险评估
    ├── event-analysis.md        # 事件分析
    ├── deep-stock-analysis.md   # 个股深度分析
    ├── fundamental-screening.md # 基本面筛选
    ├── sector-rotation.md       # 板块轮动
    └── ...                      # 其他工作流
```

## 高级用法

### 自定义筛选条件

参考 `workflows/smart-screening.md` 和 `workflows/fundamental-screening.md`，可以组合：
- 技术指标筛选（RSI、MACD、ADX 等）
- 基本面筛选（PE、PB、ROE、股息率等）
- 市值、成交量筛选
- 行业板块筛选

### 多市场对比分析

```
对比今日中美日三国财经新闻，分析市场差异
```

### 组合策略回测

结合历史 K 线数据和技术指标，可以进行简单的策略验证。

## 技术支持

- **API 文档**: `references/api-documentation.md`
- **工具指南**: `references/mcp-tools-guide.md`
- **实战案例**: `references/china-a-stock-examples.md`

## 免责声明

本工具仅供学习研究使用，不构成任何投资建议。投资有风险，入市需谨慎。使用本工具进行的任何投资决策，风险自负。

## 许可证

MIT License
