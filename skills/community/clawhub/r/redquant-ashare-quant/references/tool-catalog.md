# RedQuant MCP 工具目录（46 个对外工具）

完整的工具清单与参数说明，按功能分类。所有工具通过 MCP 协议调用。

当前对外暴露 **46 个只读 MCP 工具**，分为 **12 类能力**。少量内部实现类能力未纳入公开目录，不计入本目录。

---

## 一、股票行情（4个）

| 工具名 | 功能 | 关键参数 |
|--------|------|----------|
| `get_stock_price` | 获取股票最新价格和基本行情 | `stock_code`: 股票代码或名称 |
| `get_historical_stock_data` | 获取历史K线数据 | `stock_code`, `start_date`(YYYYMMDD), `end_date`(YYYYMMDD) |
| `get_multiple_stocks_data` | 批量获取多只股票数据 | `stock_codes`: 股票代码列表（≤50只） |
| `get_stock_basic_info` | 获取股票基本信息（名称、行业、上市日期） | `stock_code`: 股票代码或名称 |

## 二、财务数据（7个）

| 工具名 | 功能 | 关键参数 |
|--------|------|----------|
| `get_financial_indicator` | 获取财务指标数据（ROE/EPS/PE等） | `stock_code`, `report_period`(YYYYMMDD) |
| `get_income_statement` | 获取利润表 | `stock_code`, `period` |
| `get_balance_sheet` | 获取资产负债表 | `stock_code`, `period` |
| `get_cashflow_statement` | 获取现金流量表 | `stock_code`, `period` |
| `get_latest_financial_data` | 实时决策场景：获取最新公告财务数据 | `stock_code` |
| `get_financial_data_by_period` | 历史对比场景：同比环比分析 | `stock_code`, `periods` |
| `get_financial_data_with_price` | 事件驱动场景：财报公告后股价联动 | `stock_code`, `period` |

## 三、指数与行业（4个）

| 工具名 | 功能 | 关键参数 |
|--------|------|----------|
| `get_index_price` | 获取指数最新行情 | `index_code`: 指数代码 |
| `get_index_constituents` | 获取指数成分股列表 | `index_code`: 指数代码 |
| `get_industry_classification` | 获取行业分类体系 | 无必填参数 |
| `get_industry_constituents` | 获取指定行业的成分股 | `industry_name`: 行业名称 |

## 四、新闻舆情（5个）

| 工具名 | 功能 | 关键参数 |
|--------|------|----------|
| `get_financial_news_cls` | 获取财联社实时新闻 | `limit`: 返回数量 |
| `get_financial_news_tonghuashun` | 获取同花顺7×24资讯 | `limit`: 返回数量 |
| `get_financial_news_sina` | 获取新浪财经新闻 | `limit`: 返回数量 |
| `get_db_financial_news_today` | 获取今日财经新闻（数据库聚合） | 无必填参数 |
| `get_db_xueqiu_articles_today` | 获取雪球热门文章 | 无必填参数 |

## 五、交易日历（1个）

| 工具名 | 功能 | 关键参数 |
|--------|------|----------|
| `get_trade_calendar` | 查询交易日历（交易日/休市日） | `start_date`, `end_date` |

## 六、量化因子（2个）

| 工具名 | 功能 | 关键参数 |
|--------|------|----------|
| `get_factor_data` | 获取股票因子数据 | `stock_code`, `factor_name` |
| `query_available_factors` | 查询系统支持的所有因子 | 无必填参数 |

## 七、联网搜索与图表（2个）

| 工具名 | 功能 | 关键参数 |
|--------|------|----------|
| `web_search` | 补充公开信息来源 | `query`: 搜索关键词 |
| `plot_stock_chart` | 生成股票K线/走势图表 | `stock_code`, `chart_type` |

## 八、策略集市与平台（5个）

| 工具名 | 功能 | 关键参数 |
|--------|------|----------|
| `search_strategy_market` | 搜索策略集市中的量化策略 | `category`, `min_rating`, `sort_by`, `limit` |
| `get_strategy_subscription_info` | 获取策略订阅信息（价格/名额） | `strategy_id` |
| `get_platform_info` | 获取智选大师平台功能介绍 | `topic`: 主题名称（可选） |
| `list_strategies` | 列出所有可用策略 | 无必填参数 |
| `get_strategy_prompts` | 获取策略场景提示词 | 无必填参数 |

## 九、策略分析与展示（5个）

| 工具名 | 功能 | 关键参数 |
|--------|------|----------|
| `get_strategy_performance` | 获取策略绩效时间序列 | `strategy_id` |
| `get_sim_nav` | 获取策略模拟净值 | `strategy_id` |
| `get_backtest_summary` | 获取回测汇总指标 | `strategy_id` |
| `get_strategy_safe_profile` | 获取策略安全档案（面向用户） | `strategy_id` |
| `get_strategy_product_brief` | 生成基金化的策略产品说明 | `strategy_id` |

## 十、策略说明生成（3个）

| 工具名 | 功能 | 关键参数 |
|--------|------|----------|
| `get_strategy_safe_profile_from_config` | 基于策略定义生成安全描述 | `strategy_id` |
| `generate_strategy_product_brief_from_config` | 基于策略定义生成产品简介文案 | `strategy_id` |
| `generate_strategy_support_answer_from_config` | 基于策略定义生成客服答复 | `strategy_id`, `question` |

## 十一、智能选股（6个）

| 工具名 | 功能 | 关键参数 |
|--------|------|----------|
| `select_stocks_by_factors` | 基于因子条件智能选股 | `factors`: 因子条件列表 |
| `get_stock_factors` | 获取单只股票的因子数据 | `stock_code` |
| `get_stock_factor_history` | 获取股票因子历史数据 | `stock_code`, `factor_name` |
| `compare_stocks` | 对比多只股票的因子 | `stock_codes`: 股票列表 |
| `get_available_factors` | 获取可用因子清单 | 无必填参数 |
| `get_common_factor_strategies` | 获取常见选股策略模板 | 无必填参数 |

## 十二、LLM集成优化（2个）

| 工具名 | 功能 | 关键参数 |
|--------|------|----------|
| `process_query_with_optimization` | 使用语义路由优化处理查询 | `query`: 用户查询文本 |
| `get_llm_integration_stats` | 获取LLM集成性能统计 | 无参数 |

---

## 说明

公开目录仅保留面向普通用户开放的工具；内部实现类能力不会在此展示。

## 查询限制速查

| 限制项 | 上限 |
|--------|------|
| 单次查询股票数 | 50只 |
| 日期跨度 | 3年（1095天） |
| 单次返回记录数 | 1000条 |
| 新闻查询条数 | 100条 |
| 最早查询日期 | 2010-01-01 |

