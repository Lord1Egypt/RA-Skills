# 典型使用场景示例

> 说明：以下示例均为**只读查询**场景，不执行买卖或资金类操作；回答末尾需附带风险提示。公开信息补充能力仅用于辅助佐证，不替代平台内数据工具。

## 场景一：个股快速诊断

**用户提问**：「帮我看看贵州茅台现在怎么样」

**推荐工作流**：
1. `get_stock_basic_info(stock_code="600519.SH")` → 获取公司基本面
2. `get_stock_price(stock_code="600519.SH")` → 获取最新行情
3. `get_financial_indicator(stock_code="600519.SH")` → 获取关键财务指标
4. `get_financial_news_cls(limit=5)` → 获取近期相关新闻

**输出要点**：
- 当前股价、涨跌幅、成交量
- 核心财务指标（ROE、EPS、PE）
- 近期重要新闻/公告
- 风险提示

---

## 场景二：策略集市浏览

**用户提问**：「智选大师有什么好的策略推荐？」

**推荐工作流**：
1. `search_strategy_market(sort_by="rating", sort_order="DESC", limit=5)` → 获取高评分策略
2. `get_strategy_safe_profile(strategy_id="xxx")` → 获取策略概览
3. `get_backtest_summary(strategy_id="xxx")` → 获取回测表现
4. `get_strategy_subscription_info(strategy_id="xxx")` → 查询订阅信息

**输出要点**：
- 策略名称、投资理念、风格特征
- 年化收益、最大回撤、夏普比率
- 订阅价格和剩余名额
- ⚠️ 不展开内部参数细节

---

## 场景三：量化因子选股

**用户提问**：「帮我选一些低估值高成长的股票」

**推荐工作流**：
1. `get_available_factors()` → 展示可用因子
2. `get_common_factor_strategies()` → 推荐匹配的策略模板
3. `select_stocks_by_factors(factors=[...])` → 执行选股
4. `compare_stocks(stock_codes=[...])` → 对比前几名

**输出要点**：
- 选股逻辑解释（低PE + 高营收增速）
- 筛选结果列表（代码、名称、关键因子值）
- 因子含义科普
- 风险提示：因子选股是量化工具，不保证收益

---

## 场景四：市场全景速览

**用户提问**：「今天大盘怎么样？有什么热点？」

**推荐工作流**：
1. `get_index_price(index_code="000001.SH")` → 上证指数
2. `get_index_price(index_code="399001.SZ")` → 深证成指
3. `get_index_price(index_code="399006.SZ")` → 创业板指
4. `get_db_financial_news_today()` → 今日新闻聚合
5. `get_db_xueqiu_articles_today()` → 雪球热议

**输出要点**：
- 三大指数涨跌幅
- 今日市场热点主题
- 舆情情绪倾向
- 明日交易日确认

---

## 场景五：财务深度对比

**用户提问**：「对比一下茅台和五粮液的财务状况」

**推荐工作流**：
1. `get_income_statement(stock_code="600519.SH")` → 茅台利润表
2. `get_income_statement(stock_code="000858.SZ")` → 五粮液利润表
3. `get_financial_indicator(stock_code="600519.SH")` → 茅台指标
4. `get_financial_indicator(stock_code="000858.SZ")` → 五粮液指标
5. `compare_stocks(stock_codes=["600519.SH", "000858.SZ"])` → 因子对比

**输出要点**：
- 营收、净利润、毛利率对比
- ROE、EPS、PE估值对比
- 现金流健康度
- 各自优劣势分析

---

## 场景六：走势图表生成

**用户提问**：「画一下宁德时代最近3个月的走势图」

**推荐工作流**：
1. `get_stock_basic_info(stock_code="300750.SZ")` → 确认股票信息
2. `get_historical_stock_data(stock_code="300750.SZ", start_date="20251210", end_date="20260310")`
3. `plot_stock_chart(stock_code="300750.SZ")` → 生成K线图

---

## 场景七：交易日查询

**用户提问**：「下周一是交易日吗？」

**推荐工作流**：
1. `get_trade_calendar(start_date="20260310", end_date="20260316")` → 查询本周交易日

---

## 场景八：平台功能了解

**用户提问**：「智选大师是什么平台？有什么功能？」

**推荐工作流**：
1. `get_platform_info()` → 获取主题列表
2. `get_platform_info(topic="平台概述")` → 获取详细介绍
3. `get_platform_info(topic="核心功能模块")` → 获取功能说明

---

## 场景九：错误恢复与参数修正

**用户提问**：「帮我查一下茅台的数据」（未提供标准代码）

**推荐工作流**：
1. 识别"茅台"→ 转换为 `600519.SH`
2. `get_stock_price(stock_code="600519.SH")` → 获取行情
3. 若工具返回错误（如连接超时）→ 等待5秒后重试
4. 若参数错误（如代码不存在）→ 提示用户确认代码，尝试模糊匹配

**异常处理要点**：
- 工具超时：重试1次，仍失败告知用户"数据源暂时不可用，请稍后再试"
- 空数据返回：检查是否为退市股/新股/非交易日，给出明确解释
- 代码格式错误：自动纠正（如 `600519` → `600519.SH`），并告知用户标准格式

---

## 场景十：策略详细咨询（含边界处理）

**用户提问**：「我想了解某策略的具体内部参数」

**推荐工作流**：
1. `search_strategy_market(keyword="用户描述")` → 定位策略
2. `get_strategy_safe_profile(strategy_id="xxx")` → 获取安全概览
3. `get_strategy_performance(strategy_id="xxx")` → 展示绩效数据
4. ⚠️ **拒绝** 调用内部受限工具获取未公开细节

**输出要点**：
- 策略投资理念、风格特征、适合人群
- 历史绩效（年化收益、夏普比率、最大回撤）
- 礼貌拒绝内部参数请求："策略的具体因子权重和阈值属于商业机密，无法提供。我可以为您介绍策略的投资理念和历史表现。"

---

## 通用注意事项

1. **代码标准化**：用户说"茅台"时，需转换为 `600519.SH`
2. **日期处理**：用户说"最近"默认30天，"过去一年"为365天
3. **多工具协同**：复杂问题应组合2-4个工具，但避免一次调用过多
4. **错误恢复**：工具调用失败时调整参数重试，引导用户缩小查询范围
5. **免责声明**：每次分析结束必须附带风险提示

