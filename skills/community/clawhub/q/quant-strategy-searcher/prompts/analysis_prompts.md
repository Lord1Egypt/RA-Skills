# 个股分析提示词模板

## 基本面分析

```
请对股票 {stock_code} ({stock_name}) 进行基本面分析：

财务数据：
{financial_data}

分析要点：
1. 盈利能力：ROE、毛利率、净利率趋势
2. 成长性：营收增长率、净利润增长率
3. 估值水平：PE、PB、PS 与行业对比
4. 偿债能力：资产负债率、流动比率
5. 运营效率：存货周转率、应收账款周转率

输出格式：每项给出评分（1-10分）和简要说明。
```

## 技术面分析

```
请对股票 {stock_code} ({stock_name}) 进行技术面分析：

行情数据：
{market_data}

分析要点：
1. 趋势判断：MA5/MA10/MA20/MA60 均线排列
2. 量价关系：成交量与价格变化配合
3. 技术形态：支撑位、压力位、突破/回调
4. 技术指标：RSI、MACD、KDJ 信号
5. 短期/中期/长期走势预判

输出格式：每项给出评分（1-10分）和综合判断。
```

## 资金面分析

```
请对股票 {stock_code} ({stock_name}) 进行资金面分析：

资金流向数据：
{capital_flow_data}

分析要点：
1. 主力资金净流入/流出趋势
2. 北向资金持仓变化
3. 大单/中单/小单资金分布
4. 融资融券余额变化
5. 资金面综合评级

输出格式：每项给出评分（1-10分）和简要说明。
```

## 情绪面分析

```
请对股票 {stock_code} ({stock_name}) 进行情绪面分析：

相关新闻与舆情：
{news_data}

分析要点：
1. 近期舆情整体倾向（正面/中性/负面）
2. 行业热点与政策影响
3. 机构研报观点汇总
4. 市场情绪指标（换手率、波动率）
5. 情绪面综合判断

输出格式：每项给出评分（1-10分）和简要说明。
```

## 深度财报分析

```
请对股票 {stock_code} ({stock_name}) 进行深度财报分析：

多期财务指标数据（最近 {periods_analyzed} 期）：
{financial_deep_data}

### 分析框架（广度 × 深度 × 可信度）

**广度要求**：必须覆盖以下 5 个维度
1. 🏆 盈利能力：ROE、ROA、毛利率、净利率、营业利润率
2. 📈 成长性：营收增长率、净利润增长率、总资产增长率
3. 🛡️ 偿债能力：资产负债率、流动比率、速动比率
4. 💰 现金流质量：经营现金流/营收比率、现金流覆盖程度
5. ⚙️ 运营效率：总资产周转率、存货周转率、应收账款周转率

**深度要求**：
- 每个维度给出具体数值和历史趋势（↑改善 / ↓恶化 / →持平）
- 分析数据背后的业务含义（为什么增长/下滑）
- 跨维度关联分析（如：营收增长但现金流恶化 => 应收款激增）
- 与行业平均水平的对比判断

**可信度要求**：
- 标注数据完整性（多少指标有数据 / 总共多少指标）
- 给出分析置信度（高/中/低/无）
- 对数据缺失的维度明确说明
- 区分"确定结论"和"推测判断"

### 输出格式

请按以下 JSON 结构输出分析结果：

```json
{
  "composite_score": <1-10>,
  "confidence": "high|medium|low",
  "data_completeness": <0-1>,
  "dimensions": {
    "profitability": {
      "score": <1-10>,
      "assessment": "分析结论",
      "indicators": [
        {"name": "ROE", "value": 15.2, "trend": "↑", "assessment": "优秀，连续3年提升"}
      ],
      "risk_warning": "潜在风险说明"
    }
  },
  "cross_dimension_analysis": "跨维度综合判断",
  "risk_factors": ["风险1", "风险2"],
  "credibility_note": "可信度说明"
}
```
```

## 深度新闻舆论分析

```
请对股票 {stock_code} ({stock_name}) 进行深度新闻舆论分析：

多渠道新闻数据（共 {total_articles} 条，来源 {unique_sources} 个）：
{news_data}

情感分布：正面 {pos_count} / 中性 {neu_count} / 负面 {neg_count}
舆情趋势：{trend_direction}

### 分析框架

**广度要求**：
1. 覆盖多个新闻来源渠道（财经媒体、官方公告、行业报道、社区讨论）
2. 识别不同维度的舆情热点（业绩、行业、政策、管理层、股东等）
3. 区分信息来源类型（官方披露、权威媒体、自媒体、社区）

**深度要求**：
1. 逐条分析关键新闻的影响程度和持续性
2. 识别舆情演变的时序脉络（事件起因 → 发酵 → 高潮 → 回落）
3. 分析不同来源之间的信息一致性（是否存在矛盾或误导）
4. 区分短期情绪冲击和长期基本面影响

**可信度要求**：
1. 标注每条关键信息的来源可信度（根据权威性评级）
2. 区分"事实"和"观点"
3. 对信息不充分的情况明确说明
4. 给出整体分析置信度

### 输出格式

```json
{
  "composite_score": <1-10>,
  "confidence": "high|medium|low",
  "total_articles_analyzed": <数量>,
  "sentiment_summary": {
    "overall": "正面|中性|负面",
    "distribution": {"positive": N, "neutral": N, "negative": N},
    "trend": "向好|平稳|恶化",
    "key_drivers": ["主要驱动因素1", "主要驱动因素2"]
  },
  "key_articles": [
    {
      "title": "新闻标题",
      "source": "来源",
      "source_credibility": 0.85,
      "sentiment": "positive|neutral|negative",
      "impact": "high|medium|low",
      "analysis": "影响分析"
    }
  ],
  "hot_topics": ["主题1", "主题2"],
  "risk_alert": "需要警惕的舆情风险",
  "credibility_note": "可信度说明"
}
```
```

## 招股说明书分析

```
请对股票 {stock_code} ({stock_name}) 进行招股说明书分析：

（如该股为近期上市新股，需重点分析其招股说明书）
如已有历史财务数据，则结合上市前后财报进行对比分析。

### 分析框架

**广度要求**：
1. 📋 公司基本面：主营业务、商业模式、行业定位
2. 🏭 行业分析：市场规模、竞争格局、进入壁垒
3. ⚠️ 风险因素：招股书披露的主要风险
4. 💹 财务分析：上市前后财务数据对比
5. 🏛️ 募集资金用途：资金投向及预期效益
6. 👥 管理层评估：核心团队背景与经验

**深度要求**：
1. 商业模式的可复制性和护城河分析
2. 募集资金项目的可行性及预期回报
3. 与可比公司的优劣势对比
4. 上市后业绩兑现情况（如有历史数据）
5. 特殊条款分析（如对赌协议、锁定期等）

**可信度要求**：
1. 区分招股书披露信息和第三方独立分析
2. 标注信息来源
3. 对不确定的预测性信息明确提示

### 输出格式

```json
{
  "has_prospectus_data": true|false,
  "confidence": "high|medium|low|none",
  "business_analysis": {
    "main_business": "主营业务描述",
    "business_model": "商业模式分析",
    "competitive_advantage": "竞争优势分析"
  },
  "industry_analysis": {
    "market_size": "市场规模",
    "competitive_landscape": "竞争格局",
    "market_position": "市场地位"
  },
  "financial_analysis": {
    "pre_ipo_trend": "上市前财务趋势",
    "post_ipo_performance": "上市后业绩表现",
    "key_metrics_comparison": "关键指标对比"
  },
  "risk_assessment": {
    "key_risks": ["主要风险"],
    "overall_risk_level": "高|中|低"
  },
  "use_of_proceeds": "募集资金用途分析",
  "credibility_note": "可信度说明"
}
```
```

## 分析可信度评分标准

各维度分析的可信度评级标准：

| 等级 | 财报分析 | 新闻舆情分析 | 招股书分析 |
|------|---------|------------|-----------|
| **high** | ≥75%指标有数据，≥3期数据 | ≥10条新闻，平均可信度≥0.7 | 有完整招股书及上市后≥2期财报 |
| **medium** | ≥50%指标有数据，≥2期数据 | ≥5条新闻，平均可信度≥0.5 | 有招股书摘要或部分财务数据 |
| **low** | 部分指标有数据 | ≥1条新闻 | 仅有碎片化信息 |
| **none** | 无可用数据 | 无可用数据 | 无可用数据 |

## 综合评分模板

```
请根据以下各维度评分，给出股票 {stock_code} ({stock_name}) 的综合投资建议：

### 基础评分
基本面评分：{fundamental_score}/10
技术面评分：{technical_score}/10
资金面评分：{capital_flow_score}/10
情绪面评分：{sentiment_score}/10

### 深度分析评分（财报 + 舆情）
深度财报评分：{financial_deep_score}/10 (可信度: {financial_confidence})
深度舆情评分：{news_deep_score}/10 (可信度: {news_confidence})

### 分析可信度总览
- 财报分析数据完整度：{data_completeness}
- 舆情分析来源覆盖：{source_coverage}
- 整体分析置信度：{overall_confidence}

### 输出要求
1. 综合评分（加权平均，满分10分）
2. 投资建议：买入（≥8）/ 持有（5-7）/ 观察（3-4）/ 规避（≤2）
3. 核心逻辑（2-3句话总结推荐理由）
4. 广度说明（覆盖了哪些分析维度）
5. 深度说明（每个维度的分析深度和关键发现）
6. 可信度评估（数据来源、指标完整率、分析置信度）
7. 风险提示（列举该股当前主要风险因素，区分确定性和可能性）
```

## 用户交互追问模板

当用户看完初始分析后，可能会追问更深层的问题。以下是对不同追问类型的处理指南：

### 财报追问

```
用户提问：{question}
股票：{stock_code} ({stock_name})
当前已知的深度财报数据：
{financial_deep_data}

可能的追问方向及应提供的回复策略：

1. **"为什么ROE/净利率下滑了？"**
   - 调用 `query_engine.query_financial(stock_code, question, financial_deep_data)`
   - 分析方向：对比多期趋势 → 拆解杜邦分析（净利率×周转率×杠杆） → 找出驱动因素
   - 需要包含：各期具体数值、趋势方向、业务原因推测

2. **"现金流为什么这么差？"**
   - 调用 `query_engine.query_financial(stock_code, question, financial_deep_data)`
   - 分析方向：每股经营现金流 vs 每股收益对比 → 应收账款/存货变化 → 资本开支
   - 可调用 `query_engine.query_financial_timeline(stock_code, periods=8)` 查看更多期数据

3. **"负债率高不高？有风险吗？"**
   - 调用 `query_engine.query_financial(stock_code, question, financial_deep_data)`
   - 分析方向：资产负债率结构 → 流动比率/速动比率 → 有息负债 vs 无息负债
   - 引用源数据报告期和原始值

4. **"这个增长能持续吗？"**
   - 调用 `query_engine.query_financial(stock_code, question, financial_deep_data)`
   - 分析方向：多期增长率趋势 → 营收 vs 利润增长匹配度 → 行业增速对比
   - 需要区分"一次性因素"和"结构性因素"

5. **"能看看过去8期的财务数据走势吗？"**
   - 调用 `query_engine.query_financial_timeline(stock_code, periods=8)`
   - 按时间倒序列出各期关键指标，标记趋势转折点

回复要求：
- 每一条结论都必须引用源数据（报告期、原始值、数据商）
- 区分"数据事实"和"推测判断"
- 提供可验证的数据源链接
- 不确定之处需要明确说明

### 新闻舆情追问

```
用户提问：{question}
股票：{stock_code} ({stock_name})
当前已知的舆情数据：
{news_deep_data}

可能的追问方向及应提供的回复策略：

1. **"有哪些负面新闻？具体什么情况？"**
   - 调用 `query_engine.query_news(stock_code, question, news_deep_data)`
   - 从 `categorized_articles.negative` 获取所有负面新闻
   - 按时间列出每条负面新闻：标题、日期、原文链接、内容摘要
   - 分析每条负面新闻的影响程度和时效性

2. **"最近发生了哪些大事？按时间线梳理一下"**
   - 调用 `query_engine.query_news(stock_code, question, news_deep_data)`  
   - 从 `timeline` 获取完整时间线（按日期倒序排列）
   - 格式：日期 | 事件标题 | 情感标签 | 原文链接 | 内容摘要
   - 如果事件较多，按周/月分组

3. **"市场整体情绪怎么样？"**
   - 从 `sentiment_summary` 获取综合情感结论
   - 展示情感分布（正面/中性/负面数量和占比）
   - 展示来源可信度分析
   - 引用热点主题和高影响力事件

4. **"这篇关于质押的新闻具体说了什么？"**
   - 从 `timeline` 中找到该新闻
   - 提取完整的内容摘要
   - 提供原文链接供用户点击验证
   - 分析该事件的影响和背景

5. **"行业层面有什么动态？"**
   - 从 `hot_topics` 和 `timeline` 中筛选行业相关新闻
   - 分析行业政策、竞争格局变化
   - 结合公司基本面分析影响

回复要求：
- 每条新闻都必须包含：标题、日期、来源、原文链接、内容摘要
- 情感分析结论要引用具体的 `sentiment_summary`
- 提供完整的舆情时间线概览
- 区分"已确认事件"和"市场传闻"
```
