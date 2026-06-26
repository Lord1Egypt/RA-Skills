---
name: simulated-trading
description: 全功能模拟交易系统。创建投资组合、下单买入卖出、撤单、撮合成交、管理行情数据、计算净值与组合绩效（收益率、波动率、夏普比率、最大回撤）。支持东方财富实时行情自动刷新。Use when user wants to simulate stock/fund trading, create paper trading portfolios, place/cancel orders, match orders, calculate NAV, analyze portfolio performance, or run backtesting scenarios. 触发场景：(1) 查看我的账户/持仓/组合 (2) 模拟买卖股票/ETF (3) 下单交易 (4) 查看净值收益 (5) 模拟炒股/模拟交易 (6) 投资组合管理 (7) 交易回测。
---

# 模拟交易系统 Simulated Trading

## 快速开始

所有脚本在 `scripts/` 目录下，使用前会自动初始化数据库（SQLite，路径可设 `SIMTRADE_DB_PATH` 环境变量，默认 `~/.openclaw/workspace/data/simulated-trading.db`）。

完整数据库表结构见 [references/schema.md](references/schema.md)。

## 工作流

模拟交易的标准操作流程：

1. **创建组合** → `portfolio.py create`
2. **录入行情** → `market_data.py update/batch`（或使用自动刷新）
3. **下单交易** → `order.py place`
4. **撮合挂单** → `matching.py`
5. **记录净值** → `performance.py snapshot`
6. **分析绩效** → `performance.py perf`

---

## 一、组合管理 `portfolio.py`

> 🔄 **自动刷新行情：** `show` 命令默认会从东方财富 API 拉取持仓标的的实时价格，确保显示的盈亏基于最新行情。如需使用数据库缓存价格，添加 `--no-refresh` 参数。

```bash
# 创建组合
python scripts/portfolio.py create <名称> <初始资金> [描述]

# 列出所有组合
python scripts/portfolio.py list

# 查看组合详情（含持仓、挂单、近期成交）— 默认自动刷新实时价格
python scripts/portfolio.py show <组合ID>

# 查看组合详情（使用数据库缓存价格，不刷新）
python scripts/portfolio.py show <组合ID> --no-refresh

# 删除组合
python scripts/portfolio.py delete <组合ID>

# 入金
python scripts/portfolio.py deposit <组合ID> <金额>

# 出金
python scripts/portfolio.py withdraw <组合ID> <金额>
```

---

## 二、行情管理 `market_data.py`

> ⚠️ **先录行情，再下单。市价单和撮合都必须有行情数据。**

```bash
# 更新单个标的价格
python scripts/market_data.py update <代码> <价格> [名称]

# 批量更新（JSON 数组字符串）
python scripts/market_data.py batch '[{"symbol":"000001","price":12.5,"name":"平安银行"}]'

# 查询某个标的价格
python scripts/market_data.py price <代码>

# 列出所有行情
python scripts/market_data.py list [搜索关键词]

# 删除行情
python scripts/market_data.py delete <代码>
```

---

## 三、订单管理 `order.py`

```bash
# 下单（限价单）
python scripts/order.py place <组合ID> <代码> <buy|sell> limit <数量> <价格> [名称]

# 下单（市价单，立即按行情成交）
python scripts/order.py place <组合ID> <代码> <buy|sell> market <数量>

# 撤单
python scripts/order.py cancel <订单ID>

# 查询订单
python scripts/order.py query [组合ID] [status]

# 查看订单详情（含成交记录）
python scripts/order.py show <订单ID>
```

---

## 四、撮合引擎 `matching.py`

撮合规则：价格优先、时间优先。限价买单在行情价 <= 限价时成交；限价卖单在行情价 >= 限价时成交。成交价均以行情价为准。

```bash
# 撮合所有待成交订单
python scripts/matching.py

# 撮合指定组合的待成交订单
python scripts/matching.py <组合ID>
```

---

## 五、净值与绩效 `performance.py`

> 🔄 **自动刷新行情：** `nav`、`snapshot`、`perf` 命令默认会从东方财富 API 拉取持仓标的的实时价格。如需使用数据库缓存价格，添加 `--no-refresh` 参数。

```bash
# 即时计算当前净值（不存库）— 默认自动刷新实时价格
python scripts/performance.py nav <组合ID> [日期]

# 记录净值快照（存入 nav_history 表）— 默认自动刷新
python scripts/performance.py snapshot <组合ID> [日期]

# 绩效分析报告 — 默认自动刷新
python scripts/performance.py perf <组合ID> [开始日期] [结束日期]

# 以上三个命令均支持 --no-refresh 跳过自动刷新
python scripts/performance.py nav <组合ID> --no-refresh

# 查看净值历史（不涉及行情，无需刷新）
python scripts/performance.py history <组合ID> [条数]
```

### 绩效指标说明

| 指标 | 说明 |
|---|---|
| total_return_pct | 区间总收益率 |
| annualized_return_pct | 年化收益率（假设 252 交易日/年） |
| annualized_volatility_pct | 年化波动率 |
| sharpe_ratio | 夏普比率（无风险利率 2%） |
| max_drawdown_pct | 最大回撤 |
| win_rate_pct | 日胜率 |

---

## 典型使用示例

```bash
# 1. 创建 10 万初始资金的组合
python scripts/portfolio.py create "我的策略" 100000 "量化策略v1"
# → 返回 PTFxxxxxxxx

# 2. 录入行情
python scripts/market_data.py batch '[{"symbol":"000001","price":12.5,"name":"平安银行"},{"symbol":"600519","price":1680,"name":"贵州茅台"}]'

# 3. 限价买入
python scripts/order.py place PTFxxxx 000001 buy limit 1000 12.0 平安银行
# → 挂单中，需撮合或等行情达到

# 4. 市价买入
python scripts/order.py place PTFxxxx 600519 buy market 100
# → 立即按 1680 成交

# 5. 撮合所有挂单
python scripts/matching.py

# 6. 记录净值快照
python scripts/performance.py snapshot PTFxxxx

# 7. 查看绩效
python scripts/performance.py perf PTFxxxx
```

## 六、实时行情刷新 `refresh_prices.py`

独立的行情刷新工具，自动从东方财富妙想 API 获取实时价格（回退方案：东方财富直连 API）。`portfolio.py show` 和 `performance.py nav/snapshot/perf` 已内置自动调用，通常无需手动执行。

> 🔑 需要 `EM_API_KEY` 环境变量（或写入 `~/.bashrc`）。脚本会自动从 bashrc 读取。

```bash
# 刷新指定组合所有持仓的实时价格
python scripts/refresh_prices.py portfolio <组合ID>

# 刷新指定标的列表的实时价格（逗号分隔）
python scripts/refresh_prices.py symbols <代码1,代码2,...>
```

**所有脚本输出均为 JSON 格式，可直接解析。**
