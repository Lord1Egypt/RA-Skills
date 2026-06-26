# quotedance-market - 全球市场投研情报官

专业的全球市场投研日报技能，提供结构化、有思考维度的市场分析。

---

## 🎯 核心能力

### 数据源融合

- **美股行情**：Yahoo Finance（道指、纳指、标普500及重点个股）
- **A股行情**：quotedance-service（主要指数、自选股）
- **期货行情**：quotedance-service（黄金、原油、螺纹钢、豆粕等）
- **A股板块榜**：quotedance-service（涨跌幅Top N）
- **专业资讯**：Bloomberg、Reuters、华尔街见闻、金十数据（最优质最实时）

### 智能输出风格

- **交易日日报**：市场数据 + 热点主题 + 投资机会 + 风险提醒
- **周末休整日**：本周回顾 + 下周前瞻 + 风险雷达 + 思考题
- **自动切换**：根据日期自动选择日报或周末版本

---

## ⚙️ 配置文件

`skills/quotedance-market/config.json`

```json
{
  "serviceUrl": "https://quotedance.api.gapgap.cc",
  "apiKey": "",
  "watchlist": {
    "us": ["^DJI", "^IXIC", "^GSPC", "AAPL", "NVDA", "TSLA"],
    "cn": ["000001", "399001", "399006"],
    "futures": ["M2605", "RB2605", "AU0", "SC0"]
  },
  "defaults": {
    "plateTopCount": 10,
    "opportunityCount": 5,
    "newsCount": 10
  },
  "network": {
    "useProxy": true,
    "proxyUrl": "",
    "timeoutMs": 25000,
    "requestRetries": 2,
    "enableCurlFallback": true
  }
}
```

---

## 📋 报告结构

### 交易日版本

```
📈 市场情报日报 | 日期
├── 全球市场状态
│   ├── 美股/港股/A股
│   └── 期货（黄金、原油）
├── 今日热点主题
│   ├── AI & 科技
│   ├── 宏观政策
│   └── 地缘风险
├── 投资机会（3-5个）
├── 风险提醒
└── 操作策略建议
```

### 周末版本

```
📈 市场情报日报 | 日期
├── 周期: 周末休整日
├── 全球市场状态
├── 本周回顾
├── 🔥 本周热点主题
├── 📅 下周关键节点（日历表）
├── ⚠️ 风险雷达（高/中风险）
├── 💭 周末思考题
├── 📝 操作策略建议
└── 🎉 今日小彩蛋
```

---

## 🚀 使用方式

### 命令行执行

```bash
cd ~/.openclaw/workspace-quotedance

# 默认生成今日市场情报
node skills/quotedance-market/scripts/market-scan.js

# 强制刷新数据
node skills/quotedance-market/scripts/market-scan.js --refresh

# 输出网络诊断信息（代理、重试、超时配置）
node skills/quotedance-market/scripts/market-scan.js --net-debug
```

### Agent 触发条件

当用户说以下内容时，自动调用本技能：

- "市场日报"、"市场情报"
- "今日市场"、"市场简报"
- "生成市场报告"
- "整理市场信息"
- "早报"、"晚报"

---

## 📊 数据获取逻辑

### 1. 行情数据

- **美股**：Yahoo Finance API
- **A股/期货**：quotedance-service API
- **板块榜**：`/quotes/plate-top-info`

### 2. 资讯数据

**优先级排序（最优质最实时）：**

1. **Bloomberg** - 全球金融快讯
2. **Reuters** - 国际新闻
3. **华尔街见闻** - 中文专业财经
4. **金十数据** - 实时快讯
5. **CoinDesk** - 加密货币专业
6. **The Block** - Web3深度

**不再使用：** 用户订阅源（RSS聚合）

---

## 💡 输出特点

### 专业性

- 数据来源明确标注
- 风险分级（高/中/低）
- 节点重要性标记（⭐ 数量）

### 前瞻性

- 下周关键事件日历
- 风险雷达提前预警
- 周末思考题引导复盘

### 可读性

- 表格化数据展示
- Emoji图示增强识别
- 分段清晰，重点突出

---

## 🔧 实现细节

### 目录结构

```
skills/quotedance-market/
├── SKILL.md                # 本文件
├── config.json             # 配置
├── scripts/
│   └── market-scan.js      # 主脚本
└── memory/
    ├── market-YYYY-MM-DD.json # 历史快照
    └── source-cache.json      # 资讯源缓存
```

### 核心函数

- `fetchUsMarkets()` - 美股行情（Yahoo）
- `fetchQuotedanceQuotes()` - A股/期货（quotedance）
- `fetchPlateLeaders()` - 板块榜
- `fetchProfessionalNews()` - 专业资讯源
- `generateWeekdayReport()` - 交易日报告
- `generateWeekendReport()` - 周末报告
- `analyzeOpportunities()` - 识别投资机会

---

## ⚠️ 注意事项

1. **Yahoo Finance 在中国大陆被墙**，可能获取失败
2. **资讯源可能超时或限制**，脚本会降级处理
3. **周末版本**更注重前瞻性，交易日版本更注重实时性
4. 所有数据仅供参考，不构成投资建议

---

**维护者**: Alpha (quotedance agent)  
**最后更新**: 2026-03-14
