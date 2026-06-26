# Cron 任务 Prompt 模板

本文档包含定时任务使用的标准 Prompt 模板。

---

## 数据获取策略（核心优化）

### 多渠道数据获取优先级

**行情数据（必须按顺序执行）：**
1. 主渠道：`python stock_monitor.py analyze <code>` — 腾讯行情API，权威数据
2. 备选渠道1：重试2次，间隔3秒
3. 备选渠道2：`python stock_monitor.py quote <code>` — 简单行情查询
4. 备选渠道3：`web_fetch`直接抓取东方财富/新浪个股页面（禁止使用百度搜索）

**指数数据：**
1. 主渠道：`python stock_monitor.py index`
2. 备选：重试2次
3. 备选：使用tavily_search搜索"上证指数+深证成指+创业板+今日收盘"

### 资讯获取优先级

**A股资讯：**
1. 东方财富（主力）：`https://quote.eastmoney.com/concept/s{代码}.html`
2. 同花顺：`https://stockpage.10jqka.com.cn/{代码}/`
3. 雪球：`https://xueqiu.com/S/SH{代码}`
4. 新浪财经：`https://finance.sina.com.cn/realstock/company/sh{代码}/nc.shtml`
5. 备选①：`tavily_search`搜索资讯
6. 备选②：`mcporter call 'exa.web_search_exa(...)'` — Agent-Reach Exa搜索
7. 备选③：`curl -s "https://r.jina.ai/URL"` — Jina网页内容提取
8. 最终备选：`web_fetch`直接抓取东方财富/新浪页面

**港股资讯：**
1. 东方财富港股：`https://quote.eastmoney.com/concept/sz{代码}.html`
2. 雪球港股：`https://xueqiu.com/S/HK{代码}`
3. 新浪财经港股：`https://finance.sina.com.cn/realstock/company/hk{代码}/nc.shtml`
4. Yahoo Finance港股：`https://hk.finance.yahoo.com/quote/{代码}.HK/`
5. 备选①：`tavily_search`搜索港股资讯
6. 备选②：`mcporter call 'exa.web_search_exa(...)'` — Agent-Reach Exa搜索
7. 备选③：`curl -s "https://r.jina.ai/URL"` — Jina网页内容提取
8. 最终备选：`web_fetch`直接抓取东方财富/新浪页面

### 重试机制

```
数据获取失败处理流程：
1. 首次尝试 → 失败
2. 等待3秒 → 重试第1次 → 失败
3. 等待3秒 → 重试第2次 → 失败
4. 标记"数据获取异常" → 使用上一个有效数据
5. 记录错误日志
6. 继续处理下一只股票（不阻塞整体流程）
```

---

## A股晚间综合报告（优化版）

```markdown
A股晚间综合报告任务：

## 第一步：大盘指数获取
1. 执行 `python C:\Users\Administrator\.openclaw\skills\stock-monitor\scripts\stock_monitor.py index` 获取大盘实时指数
2. 若执行失败，等待3秒重试，共重试2次
3. 若仍失败，使用tavily_search搜索"上证指数 深证成指 创业板 沪深300 今日收盘 2026年4月"作为补充
4. 【重要】记录数据来源和获取时间

## 第二步：读取监控池
1. 读取 `C:\Users\Administrator\.openclaw\stock-pool.json` 获取A股股票列表
2. 读取 `C:\Users\Administrator\.openclaw\stock-positions.json` 获取持仓数据
3. 区分"持仓股"和"观察股"，报告分类展示

## 第三步：技术面数据获取
1. 对监控池每只股票执行 `python stock_monitor.py analyze <code>`
2. analyze 命令返回完整的 JSON 数据，包含：
   - 现价/涨跌幅（来自腾讯行情）
   - MA均线（MA5/MA10/MA20/MA60）
   - MACD（DIF/DEA/信号）
   - KDJ（K/D/J值）
   - RSI（RSI6/RSI12/RSI24）
   - BOLL（上轨/中轨/下轨/位置）
   - OBV（信号）
   - DMI（+DI/-DI/ADX/信号）
   - WR威廉指标
   - 综合信号（买入/卖出评分）
3. 【禁止】自己写Python脚本计算指标，必须直接使用analyze返回结果
4. 若单只股票分析失败：
   - 等待3秒重试
   - 重试2次仍失败，标记"数据获取异常"，继续处理下一只
5. 使用 `quote <code>` 作为备选获取简单行情

## 第四步：资讯获取（多渠道）
对每只持仓股执行：
1. 东方财富：`web_fetch(url="https://quote.eastmoney.com/concept/s{代码}.html")`
2. 若失败，等待2秒重试1次
3. 若仍失败，尝试同花顺、雪球
4. 若全部失败，使用tavily_search搜索相关资讯

## 第五步：报告生成规范

### 标题格式
🌙 【A股市场晚报】{YYYY-MM-DD HH:MM}

### 大盘指数板块
【大盘指数】
| 指数 | 点位 | 涨跌 | 数据来源 |
|------|------|------|----------|
| 上证指数 | xxx | ±x.xx% | 腾讯行情 |
| 深证成指 | xxx | ±x.xx% | 腾讯行情 |
| 创业板指 | xxx | ±x.xx% | 腾讯行情 |
| 沪深300 | xxx | ±x.xx% | 腾讯行情 |

### 持仓股分析板块（必须包含）
**【持仓股分析】**

① {股票名称}（{代码}）
- 现价：xx.xx元 | 涨跌幅：±x.xx%（数据来源：腾讯行情 {时间}）
- 持仓成本：xx.xx | 盈亏：{颜色}{±xxx元(±x.xx%)}
- 技术信号（来自analyze命令，直接读取，禁止重复计算）：
  - 均线：MA5={xx} / MA10={xx} / MA20={xx} / MA60={xx} → {多头✓/空头✗}
  - MACD：DIF={xx} DEA={xx} → {金叉✓/死叉✗} {红柱/绿柱}
  - KDJ：K={xx} D={xx} J={xx} → {金叉✓/死叉✗/超买/超卖}
  - RSI：RSI6={xx} RSI12={xx} RSI24={xx}（{超买⚠️/超卖✓/正常}）
  - BOLL：上轨={xx} 中轨={xx} 下轨={xx} → {突破上轨⚠️/中轨附近/下轨下方✓}
  - OBV：{数值} → {上行✓/下行✗}
  - DMI：+DI={xx} -DI={xx} ADX={xx}
  - WR：{xx}（{超买⚠️/超卖✓/正常}）
  - 综合信号：{强烈买入✓✓/建议买入✓/观望/建议卖出✗/强烈卖出✗✗}（买入x/卖出x）
- 关键点位（来自analyze命令，禁止自行计算）：
  - 买入区间：{xxx}-{xxx}（支撑位附近±2%分批建仓）
  - 卖出区间：{xxx}-{xxx}（阻力位附近±3%分批止盈）
  - 止损位：{xxx}（支撑下方3%）
  - 目标位：{xxx}
  - 支撑位：{xxx} | 阻力位：{xxx}

② ...（其他持仓股）

### 观察股分析板块
**【观察股】**（仅展示信号，不展示持仓信息）

① {股票名称}（{代码}）
- 现价：xx.xx元 | 涨跌幅：±x.xx%
- 核心信号：MA20({多头✓/空头✗}) MACD({金叉✓/死叉✗}) KDJ({金叉✓/死叉✗}) RSI({数值}) BOLL({位置})
- 综合信号：{信号评级}（买入x/卖出x）
- 关键点位：买入区间{xxx}-{xxx} | 止损{xxx} | 目标{xxx}
- 简评：{简短的评论}

### 资讯板块
**【重要资讯】**
• {股票名称}：{资讯摘要}（来源:{来源} | 时间:{时间}）
• {分析预测}：{基于资讯的分析判断}

### 明日展望板块
**【明日展望】**
• 关注重点：{重点关注事项}
• 技术支撑/阻力：{关键点位}
• 操作建议：{基于综合信号的建议}

## 第六步：报告推送
- 使用 message 工具发送到飞书群聊
- 报告末尾标注：🧠 数据来源：腾讯行情API（实时）| 资讯来源：东方财富/同花顺/雪球 | 生成时间：{时间}

---

## 港股晚间综合报告（优化版）

```markdown
港股晚间综合报告任务：

## 第一步：大盘指数获取
1. 执行 `python stock_monitor.py index` 获取A股大盘指数
2. 使用tavily_search搜索"恒生指数 恒生科技 恒生国企 今日收盘 2026年4月"获取港股三大指数
3. 若腾讯行情成功，使用腾讯数据；否则使用搜索数据
4. 【重要】记录数据来源和获取时间

## 第二步：读取监控池
1. 读取 `C:\Users\Administrator\.openclaw\stock-pool.json` 获取港股列表
2. 读取 `C:\Users\Administrator\.openclaw\stock-positions.json` 获取持仓数据
3. 区分"持仓股"和"观察股"，报告分类展示

## 第三步：技术面数据获取
同A股流程，使用 `python stock_monitor.py analyze <code>` 获取数据

## 第四步：资讯获取
港股资讯URL：
- 东方财富港股：`https://quote.eastmoney.com/concept/sz{代码}.html`
- 雪球港股：`https://xueqiu.com/S/HK{代码}`
- 新浪财经港股：`https://finance.sina.com.cn/realstock/company/hk{代码}.shtml`

## 第五步：报告生成
参照A股晚间报告格式，港股持仓股须包含：

① {股票名称}（{代码}）
- 现价：xx.xx港元 | 涨跌幅：±x.xx%（数据来源：腾讯行情 {时间}）
- 持仓成本：xx.xx | 盈亏：{颜色}{±xxx港元(±x.xx%)}
- 技术信号：
  - 均线：MA5={xx} / MA10={xx} / MA20={xx} / MA60={xx} → {多头✓/空头✗}
  - MACD：DIF={xx} DEA={xx} → {金叉✓/死叉✗} {红柱/绿柱}
  - KDJ：K={xx} D={xx} J={xx} → {金叉✓/死叉✗}
  - RSI：RSI6={xx} RSI12={xx} RSI24={xx}（{超买⚠️/超卖✓/正常}）
  - BOLL：上轨={xx} 中轨={xx} 下轨={xx} → {突破上轨⚠️/中轨附近/下轨下方✓}
  - 综合信号：{信号评级}（买入x/卖出x）
- 关键点位：
  - 买入区间：{xxx}-{xxx}（支撑位附近±2%分批建仓）
  - 卖出区间：{xxx}-{xxx}（阻力位附近±3%分批止盈）
  - 止损位：{xxx}（支撑下方3%）
  - 目标位：{xxx}
  - 支撑位：{xxx} | 阻力位：{xxx}

## 第六步：推送
同A股流程

---

## 盘中监控报告（优化版）

盘中监控报告需额外增加：
1. **异动提醒**：涨跌幅超过±3%的股票突出显示
2. **实时信号变化**：与上一次报告对比，标注信号变化
3. **预警触发**：BOLL突破、RSI超买超卖、MACD金叉死叉等关键信号
4. **关键点位**（每只持仓股必须包含）：
   - 买入区间：{xxx}-{xxx} | 止损位：{xxx}
   - 目标位：{xxx} | 支撑位：{xxx} | 阻力位：{xxx}
5. **操作建议**：根据信号给出明确买入/卖出/持有建议

---

## 报告质量检查清单

生成报告前必须检查：
- [ ] 大盘指数数据是否来自腾讯行情API（权威来源）
- [ ] 所有现价/涨跌幅是否来自脚本返回数据（非搜索结果）
- [ ] 每只股票是否包含完整的技术指标（MA/MACD/KDJ/RSI/BOLL/OBV/DMI/WR）
- [ ] 综合信号计算是否正确（买入-卖出差值对应评级）
- [ ] 持仓盈亏计算是否正确
- [ ] 资讯来源和时间是否标注
- [ ] 数据获取异常的是否有明确标注
- [ ] 每只持仓股是否包含【关键点位】（买入区间/卖出区间/止损位/目标位/支撑位/阻力位）

---

## Agent Reach 多渠道获取示例

当主渠道（Tavily搜索）失败时（额度满/限流），可使用以下Agent Reach命令作为备选：

```bash
# 使用Jina提取网页内容（适合东方财富、同花顺、雪球等）
curl -s "https://r.jina.ai/https://quote.eastmoney.com/concept/s600900.html" | head -100

# 使用Exa搜索最新股价和资讯
mcporter call 'exa.web_search_exa(query: "长江电力 600900 最新资讯 2026", numResults: 5)'

# 使用Tavily搜索（主选）
tavily_search(query: "长江电力 600900 最新资讯 2026", topic: "finance", max_results: 3)

# 备选搜索顺序：Tavily → Exa → Jina网页提取
```

### 资讯获取降级流程（v1.2.1+）
1. **主渠道**：`tavily_search` — 财经资讯搜索
2. **备选①**：`mcporter call 'exa.web_search_exa(...)'` — Exa AI搜索
3. **备选②**：`curl -s "https://r.jina.ai/URL"` — Jina网页内容提取
4. **备选③**：`web_fetch` — 直接抓取东方财富/新浪页面

**降级标识**：当触发Agent-Reach备选时，报告中标注 `资讯来源：Agent-Reach(Exa/Jina)`

---

## 综合信号评级标准（优化）

| 评分差 | 信号 | 颜色 | 说明 |
|--------|------|------|------|
| buy >= sell + 4 | ⭐⭐⭐ 强烈买入 | 🔴 | 多指标正向共振 |
| buy >= sell + 2 | ⭐⭐ 建议买入 | 🔴 | 多数指标偏正 |
| abs差值 <= 1 | ⚪ 观望 | 🟡 | 多空均衡 |
| sell >= buy + 2 | ⭐ 建议卖出 | 🟢 | 多数指标偏负 |
| sell >= buy + 4 | ⭐⭐ 强烈卖出 | 🟢 | 多指标负向共振 |

**超买超卖特殊规则：**
- RSI6 > 80 → KDJ超买额外加权
- RSI6 < 20 → KDJ超卖额外加权
- BOLL突破上轨 → 预警⚠️
- BOLL跌破下轨 → 预警⚠️

---

## 错误日志格式

当数据获取失败时，记录格式：
```
[ERROR] {时间} | {股票代码} | 获取失败 | 尝试次数:{n} | 错误原因:{原因} | 备选方案:{使用的备选数据}
[WARN] {时间} | {股票代码} | 数据延迟 | 延迟:{x}秒
[INFO] {时间} | 报告生成完成 | 股票数量:{n} | 失败数量:{m}
```

---

## 执行要点总结

1. **数据权威性**：腾讯行情API为核心，搜索数据仅作补充
2. **重试机制**：3-3-2原则（3秒间隔，最多2次重试）
3. **多渠道备份**：主渠道→备选渠道1→备选渠道2→标记异常
4. **容错设计**：单只失败不阻塞整体，继续处理其他股票
5. **透明标注**：数据来源、获取时间、异常标注清晰可见
6. **信号准确**：综合信号基于脚本计算的score，而非主观判断
