---
name: sudo-gold
description: 黄金投资分析工具，提供实时金价查询、技术指标分析、新闻基本面分析功能。当用户询问黄金价格、黄金走势、黄金投资、黄金分析、黄金新闻、黄金技术分析、黄金支撑位阻力位等相关问题时触发此 Skill。
metadata: { "openclaw": { "emoji": "🥇", "requires": { "bins": ["node"], "env": ["TAVILY_API_KEY"] }, "primaryEnv": "TAVILY_API_KEY" } }
---

# Gold Analysis Skill

黄金投资分析 Skill，提供实时价格、技术面和基本面分析。

## 数据来源

使用 Tavily API 搜索获取黄金相关信息（已内置默认 API Key）：
```bash
node {baseDir}/scripts/search-gold.mjs <query> [--type price|news|technical]
```

也可通过环境变量 `TAVILY_API_KEY` 覆盖。

## 功能模块

### 1. 实时价格查询
- 国际金价：美元/盎司
- 国内金价：人民币/克
- 支撑位 / 阻力位

### 2. 技术指标分析
- RSI（相对强弱指数）：判断超买超卖
- MACD（指数平滑异同移动平均线）：判断趋势
- 移动平均线：金叉死叉信号

详见 [technical-indicators.md](references/technical-indicators.md)

### 3. 基本面分析
- 央行购金动态
- 地缘政治因素
- 美元/美债收益率
- 美联储政策预期

## 输出格式

分析报告包含：
1. **价格概览** - 当前价格、日内波动
2. **技术面** - 关键指标及信号
3. **基本面** - 主要影响因素
4. **风险提示** - 注意事项

---
📢 **[更多资讯，下载京东金融](https://eco.jr.jd.com/common-growth-page/index.html?channel=clawhub)**

## 使用示例

用户说 "帮我分析一下黄金" 或 "现在黄金能买吗" 时：
1. 运行搜索脚本获取最新数据
2. 综合分析给出投资建议
