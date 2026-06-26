# TA Radar API — 私有化部署指南

本文档面向希望自行部署 TA Radar API 的技术用户。

---

## 目录

1. [项目结构](#项目结构)
2. [依赖安装](#依赖安装)
3. [核心源码 api/index.js](#核心源码)
4. [配置文件](#配置文件)
5. [本地调试](#本地调试)
6. [Vercel 部署](#vercel-部署)
7. [更换 API Endpoint](#更换-api-endpoint)

---

## 项目结构

```
your-project/
├── api/
│   └── index.js        ← 核心逻辑（单文件，无需其他模块）
├── package.json
└── vercel.json
```

---

## 依赖安装

```bash
npm init -y
npm install axios technicalindicators
npm install -g vercel   # 如未安装 Vercel CLI
```

**package.json 关键内容：**

```json
{
  "name": "ta-radar-api",
  "version": "1.0.0",
  "dependencies": {
    "axios": "^1.7.2",
    "technicalindicators": "^3.1.0"
  },
  "engines": {
    "node": ">=18.x"
  }
}
```

---

## 核心源码

**api/index.js 功能模块说明：**

### 输入解析层

| 函数 | 职责 |
|---|---|
| `inferInterval(query)` | 正则匹配关键词推断 K 线级别，默认 4h |
| `extractAddress(query)` | 提取 0x 开头的 42 位合约地址 |
| `resolveSymbolFromAddress(address)` | 调用 DexScreener API 解析合约 → Ticker |
| `extractTicker(query)` | 清除地址后提取首个 2~10 字母数字 Ticker |

### 数据拉取层

| 函数 | 职责 |
|---|---|
| `fetchKlines(symbol, interval)` | 请求币安 `/api/v3/klines`，返回收盘价数组 |

**币安接口容错：**
- 4xx 响应 → 返回 `{ notListed: true, message: "..." }` 专属提示
- 网络超时 → 抛出错误，由主处理器捕获返回 500

### 指标计算层

使用 `technicalindicators` 库，均取结果数组最后一个元素（最新 K 线）：

```javascript
// EMA
EMA.calculate({ period: 20, values: closes })

// RSI
RSI.calculate({ period: 14, values: closes })

// MACD
MACD.calculate({
  fastPeriod: 12, slowPeriod: 26, signalPeriod: 9,
  values: closes,
  SimpleMAOscillator: false,
  SimpleMASignal: false
})

// Bollinger Bands
BollingerBands.calculate({ period: 20, values: closes, stdDev: 2 })
```

### 信号解读层

| 函数 | 返回格式 |
|---|---|
| `signalEMA(ema20, ema50, lastClose)` | `{ label: "偏多/偏空/中性...", desc: "..." }` |
| `signalRSI(rsi)` | 同上，含超买（≥70）/ 超卖（≤30）判断 |
| `signalMACD(macd)` | 基于 MACD线 vs 信号线 及 柱状图正负 |
| `signalBoll(boll, lastClose)` | 基于价格相对上/中/下轨位置 |

### 报告生成层

`buildSummary()` — 统计多空信号数量，生成综合研判段落，输出关键支撑/阻力/中轴三个价位。

`buildMarkdown()` — 拼装完整 Markdown 报告，包含核心数据面板表格 + 综合趋势研判 + 免责声明。

**文风硬性约束（写死在逻辑中）：**
- 禁止比喻和夸张修辞
- 禁止双引号
- 只使用平实交易术语（支撑位、多空博弈、下行通道等）

---

## 配置文件

**vercel.json：**

```json
{
  "version": 2,
  "builds": [{ "src": "api/index.js", "use": "@vercel/node" }],
  "routes": [
    { "src": "/api/(.*)", "dest": "/api/index.js" },
    { "src": "/(.*)", "dest": "/api/index.js" }
  ]
}
```

---

## 本地调试

```bash
vercel dev
# 访问 http://localhost:3000/api?query=SOL%204H分析
```

---

## Vercel 部署

```bash
vercel          # 首次部署，跟随引导绑定账号
vercel --prod   # 推送到生产环境
```

部署成功后，Vercel 会提供一个类似 `https://your-project-name.vercel.app` 的域名。

---

## 更换 API Endpoint

部署完成后，需要更新 Skill 中的 API 地址。在 SKILL.md 中找到：

```
https://ta-radar.vercel.app/api?query={用户原始输入}
```

替换为你自己的域名：

```
https://your-project-name.vercel.app/api?query={用户原始输入}
```

---

## 调用示例与返回结构

**请求：**
```
GET /api?query=SOL%20短线分析
```

**成功返回：**
```json
{
  "success": true,
  "symbol": "SOL",
  "binanceSymbol": "SOLUSDT",
  "interval": "1h",
  "notListed": false,
  "indicators": {
    "price": 148.32,
    "ema20": 147.81,
    "ema50": 145.20,
    "rsi": 58.4,
    "macd": { "macdLine": 0.42, "signal": 0.31, "histogram": 0.11 },
    "boll": { "upper": 152.10, "middle": 147.50, "lower": 142.90 }
  },
  "signals": {
    "ema": "偏多",
    "rsi": "偏多",
    "macd": "偏多",
    "boll": "中轨上方偏多"
  },
  "markdown": "## 📊 全维度技术面雷达 | SOL/USDT · 1H\n..."
}
```

**未上币安返回：**
```json
{
  "success": true,
  "notListed": true,
  "markdown": "⚠️ 侦测到该代币暂未上线币安主流交易区..."
}
```

**错误返回：**
```json
{
  "success": false,
  "error": "具体错误原因描述"
}
```
