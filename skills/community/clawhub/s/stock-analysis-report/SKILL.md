---

name: stock-analysis
description: |
  A股市场分析与个股深度分析技能。支持基本面（财务指标/估值分位）、资金面（主力资金/DDX/DDY/DDZ）、技术面（均线/乖离率/量比）、筹码分布、舆情情报（新闻/研报/公告）等多维度分析，输出结构化评分与操作建议。

Triggers: "分析股票", "个股分析", "市场分析", "A股分析", "stock analysis", "analyze stock", "market analysis", "股票评分", "买卖建议", "涨停分析"

Does NOT trigger:

- 简单的股价查询（无需深度分析）
- 港股/美股/非A股市场分析
- 基金/债券/期货分析

Output: 结构化分析报告（评分0-100、操作方向、买卖点位、风险提示、检查清单）
version: 1.0.9
license: MIT-0
metadata:
  openclaw:
    requires:
      env:
        - LLM_API_KEY
        - LLM_BASE_URL
        - LLM_MODEL
      bins:
        - python3
    optional:
      env:
        - MX_APIKEY
        - SERPAPI_KEY
        - TAVILY_KEY
        - BRAVE_KEY
        - BOCHA_KEY
        - BIAS_THRESHOLD
        - NEWS_MAX_AGE_DAYS
        - ENABLE_CHIP
        - LOG_LEVEL
    primaryEnv: LLM_API_KEY
    emoji: "📈"
    install:
      - kind: uv
        command: pip install -r requirements.txt

---

# A股股票市场分析 Skill

## 功能

### 个股分析

输入股票代码，输出结构化分析结果：

- **基本面**：净利润、营收、ROE、毛利率、资产负债率、机构持股比例、盈利预测
- **估值**：PE(TTM)、PB、历史分位
- **资金面**：主力资金流向（超大单/大单/中单/小单净额）、DDX/DDY/DDZ 指标
- **技术面**：MA5/MA10/MA20/MA60 均线、多头排列、乖离率、量比
- **筹码分布**：获利比例、平均成本、集中度
- **舆情情报**：妙想金融资讯（新闻/研报/公告，LLM 分析）+ 多引擎新闻搜索
- **实时行情**：当前价、涨跌幅、成交量、换手率
- **分析结论**：评分 + 操作方向 + 买卖点位 + 检查清单 + 风险提示

### 市场分析

每日 A 股市场复盘：

- 主要指数（上证/深证/创业板）
- 涨跌统计（涨跌家数、涨停跌停数）
- 板块排名（领涨/领跌 Top5）
- 市场情绪判断 + 操作建议

## 使用方式

### 生成分析报告（推荐）

```bash
# 个股分析报告 → 保存到 reports/{代码}_{日期}.md
python3 {baseDir}/scripts/report.py stock 600519

# 市场分析报告 → 保存到 reports/market_{日期}.md
python3 {baseDir}/scripts/report.py market

# 同时输出 JSON
python3 {baseDir}/scripts/report.py stock 600519 --json

# 自定义输出目录
python3 {baseDir}/scripts/report.py stock 600519 -o ./my-reports
```

### JSON 输出

```bash
python3 {baseDir}/scripts/analyze_stock.py 600519
python3 {baseDir}/scripts/analyze_market.py
```

### Handler 调用

```python
from src.index import handler
result = await handler({"mode": "stock", "code": "600519"})
result = await handler({"mode": "market"})
result = await handler({"mode": "stock", "code": "600519", "save": True})
result = await handler({"mode": "stock", "code": "600519", "save": True, "output_dir": "./reports"})
```

## 输入格式

| 字段          | 类型      | 必填            | 说明                            |
| ----------- | ------- | ------------- | ----------------------------- |
| mode        | string  | 是             | "stock" 或 "market"            |
| code        | string  | mode=stock时必填 | A股股票代码，如 "600519"             |
| save        | boolean | 否             | 是否保存 Markdown 报告到 reports/ 目录 |
| output_dir | string  | 否             | 自定义报告输出目录（需 save=true）        |

## 输出格式

### 个股分析结果

```json
{
  "stock_code": "600519",
  "stock_name": "贵州茅台",
  "core_conclusion": "一句话核心结论",
  "score": 75,
  "action": "买入/观望/卖出",
  "trend": "看多/震荡/看空",
  "buy_price": 1800.0,
  "stop_loss_price": 1700.0,
  "target_price": 2000.0,
  "checklist": [{"condition": "...", "status": "✅/❌", "detail": "..."}],
  "risk_alerts": ["风险1", "风险2"],
  "positive_catalysts": ["利好1"],
  "strategy": "买卖策略建议",
  "stock_info": {"code": "600519", "name": "贵州茅台", "industry": "白酒", "market_cap": 2200000000000},
  "realtime": {"price": 1800.0, "change_pct": 1.5, "turnover_rate": 0.8},
  "tech": {"ma5": 1780.0, "ma10": 1760.0, "ma20": 1740.0, "ma60": 1700.0, "is_bullish_alignment": true, "bias": 2.1, "volume_ratio": 1.2},
  "chip": {"profit_ratio": 75.0, "avg_cost": 1720.0, "concentration": 12.5},
  "capital_flow": {"super_large_net": 500000000, "large_net": 200000000, "ddx": 0.26, "ddy": 0.15, "ddz": 5.3},
  "valuation": {"pe_ttm": 28.5, "pb": 8.2, "pe_percentile": 45.0, "pb_percentile": 30.0},
  "financial": {"net_profit": 55000000000, "revenue": 120000000000, "roe": 30.5, "gross_margin": 91.2, "debt_ratio": 25.3, "institution_holding_pct": 65.0},
  "news": [{"title": "...", "snippet": "资讯摘要", "date": "2025-01-15", "source": "中泰证券·研报·买入", "info_type": "report"}],
  "raw_report": "LLM完整分析报告(Markdown)",
  "disclaimer": "仅供参考，不构成投资建议"
}
```

### 市场分析结果

```json
{
  "date": "2025-01-15",
  "core_conclusion": "一句话核心结论",
  "indices": [{"name": "上证指数", "close": 3200.0, "change_pct": 0.5}],
  "statistics": {"up_count": 3000, "down_count": 1500, "limit_up_count": 50},
  "top_sectors": [{"name": "半导体", "change_pct": 3.2}],
  "bottom_sectors": [{"name": "房地产", "change_pct": -1.5}],
  "sentiment": "偏多/中性/偏空",
  "strategy": "操作建议",
  "raw_report": "LLM完整复盘报告(Markdown)"
}
```

## 数据源

### 推荐配置：妙想金融

配置 `MX_APIKEY` 后，妙想金融自动成为行情数据、财务/资金/估值、资讯搜索的**最高优先级数据源**，覆盖能力最全、数据质量最高。推荐优先配置。

👉 前往 [妙想 Skills 页面](https://dl.dfcfs.com/m/itc4) 获取 API Key

### 行情数据

三级自动容灾，并行竞争 + 超时控制：

| 优先级 | 数据源          | 覆盖能力              | 需要 Key        |
| --- | ------------ | ----------------- | ------------- |
| 0   | **妙想金融**     | 行情 + 财务 + 资金 + 估值 | ✅ `MX_APIKEY` |
| 1   | **Efinance** | 行情 + 板块 + 市场统计    | ❌             |
| 2   | **AkShare**  | 行情 + 筹码 + 板块      | ❌             |

- 配置 `MX_APIKEY` 后妙想自动成为最高优先级；未配置时从 Efinance 开始
- 所有数据源**并行请求**，按优先级取第一个有效结果；日K线取行数最多的结果
- 单数据源超时 10 秒自动降级，任一数据源异常不影响整体分析

### 资讯搜索

五级自动容灾，串行降级：

| 优先级 | 搜索引擎     | 返回内容                   | 需要 Key          |
| --- | -------- | ---------------------- | --------------- |
| 0   | **妙想搜索** | 完整正文 + 新闻/研报/公告 + 机构评级 | ✅ `MX_APIKEY`   |
| 1   | SerpAPI  | snippet                | ✅ `SERPAPI_KEY` |
| 2   | Tavily   | snippet                | ✅ `TAVILY_KEY`  |
| 3   | Brave    | snippet                | ✅ `BRAVE_KEY`   |
| 4   | Bocha    | snippet                | ✅ `BOCHA_KEY`   |

- 妙想搜索返回完整正文，直传 LLM 进行分析；其他引擎仅返回 snippet
- 研报类型含机构名称和评级（如"中泰证券·研报·买入"），LLM 可据此参考机构观点

详见 references/data-sources.md。

## 性能特性

- **并行数据采集**：个股分析的 7 个数据维度（日K线、实时行情、筹码、资金、估值、财务、资讯）并行获取，总耗时取决于最慢的单项
- **并行数据源竞争**：同一数据维度在多个数据源间并行请求，按优先级取第一个有效结果
- **超时保护**：单数据源请求超时 10 秒自动降级，避免阻塞
- **资讯正文直传**：妙想资讯返回完整正文，直传 LLM 在最终分析时一并阅读，保留完整投资信息

## 环境变量

| 变量            | 必填 | 说明                                               |
| -------------- | -- | ------------------------------------------------ |
| LLM_API_KEY    | 是  | LLM API Key                                      |
| LLM_BASE_URL   | 是  | OpenAI 兼容 API 地址                                 |
| LLM_MODEL      | 是  | 模型名称                                             |
| MX_APIKEY      | 否  | 妙想金融 API Key（[前往获取](https://dl.dfcfs.com/m/itc4)），配置后自动成为行情数据 + 财务/资金/估值 + 资讯搜索第一优先级 |
| SERPAPI_KEY    | 否  | SerpAPI 搜索 Key                                   |
| TAVILY_KEY     | 否  | Tavily 搜索 Key                                    |
| BRAVE_KEY      | 否  | Brave 搜索 Key                                     |
| BOCHA_KEY      | 否  | 博查搜索 Key                                         |

## 注意事项

- Efinance / AkShare 为免费接口，无需注册；妙想金融需配置 `MX_APIKEY`
- 分析结果仅供参考，不构成投资建议

