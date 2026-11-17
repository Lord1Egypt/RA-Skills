---
name: 小果量化交易Ptrade全能助手
version: 2.1.0
author: 小果
contact: 微信 xg_quant
description: |
  小果量化交易Ptrade全能助手基于 Ptrade 量化交易平台的一站式策略辅助工具。
  支持策略回测参数配置、Python 策略代码自动生成、交易日志深度分析、
  实盘交易信号指导、绩效归因与风险评估。
triggers:
  - "小果量化"
  - "Ptrade"
  - "双均线策略"
  - "金叉死叉"
  - "量化回测"
  - "Ptrade 策略"
  - "金叉买入"
  - "死叉卖出"
  - "Ptrade 代码"
platform: Ptrade (恒生电子)
category: 量化交易策略开发
tags:
  - 量化交易
  - Ptrade
  - 双均线策略
  - 回测系统
  - 策略开发
  - 风险管理
---
# 小果量化交易Ptrade全能助手

> 作者：小果（微信：xg_quant）  
> 版本：2.1.0  
> 适用平台：Ptrade 量化交易终端（恒生电子）  
> 适用策略：趋势跟踪、双均线、金叉死叉、多因子、网格、动量轮动等

---

## 一、功能概述

本技能帮助用户在 **Ptrade 量化交易终端** 上高效完成从策略设计、代码编写、回测验证到实盘上线的全流程工作。  
核心覆盖以下场景：

- ✅ **策略脚本生成**：基于用户需求自动生成 Ptrade 可运行的 Python 策略代码
- ✅ **回测参数配置**：引导设置标的、周期、手续费、滑点、资金管理等关键参数
- ✅ **回测结果分析**：解读收益率、夏普比率、最大回撤、胜率、盈亏比等核心指标
- ✅ **交易日志分析**：逐笔分析成交记录，定位亏损原因，优化交易逻辑
- ✅ **实盘交易指导**：提供仓位管理建议、止盈止损设置、风险预警提示
- ✅ **策略优化建议**：基于回测数据给出参数调优、过滤条件增强等专业建议

---

## 二、双均线策略（金叉死叉）快速上手

### 2.1 策略逻辑
- **金叉买入**：短期均线（如 MA5）上穿长期均线（如 MA20），产生买入信号
- **死叉卖出**：短期均线下穿长期均线，产生卖出信号
- **可选增强**：可叠加成交量过滤、RSI 过滤、大盘择时等条件

### 2.2 Ptrade 策略代码模板（Python）

```python
# ============================================================
# 小果量化 - Ptrade 双均线策略模板
# 作者：小果（微信：xg_quant）
# 版本：2.0
# 适用周期：日线 / 30分钟 / 60分钟
# ============================================================

def initialize(context):
    # 设置标的
    g.stock = '510300.SS'  # 沪深300ETF
    g.short_ma = 5         # 短期均线周期
    g.long_ma = 20         # 长期均线周期
    g.position_pct = 0.95  # 仓位比例
    g.stop_loss_pct = 0.05 # 止损比例（5%）
    g.take_profit_pct = 0.10 # 止盈比例（10%）
    
    # 定时任务：每日开盘后执行
    run_daily(main_strategy, time='09:35')
    # 每日收盘前检查止损止盈
    run_daily(check_stop, time='14:55')

def main_strategy(context):
    # 获取历史收盘价
    close_prices = history_bars(g.stock, g.long_ma + 5, '1d', 'close')
    if len(close_prices) < g.long_ma + 1:
        return
    
    # 计算均线
    ma_short = close_prices[-g.short_ma:].mean()
    ma_long = close_prices[-g.long_ma:].mean()
    
    # 当前持仓
    current_position = context.portfolio.positions[g.stock].quantity
    current_price = get_current_data()[g.stock].last_price
    
    # ===== 金叉买入（无持仓时） =====
    if ma_short > ma_long and current_position == 0:
        cash = context.portfolio.cash * g.position_pct
        order_value(g.stock, cash)
        log.info(f'金叉买入 {g.stock}，金额：{cash:.2f}，价格：{current_price:.3f}')
        # 记录买入价格用于止损止盈
        g.entry_price = current_price
    
    # ===== 死叉卖出（有持仓时） =====
    elif ma_short < ma_long and current_position > 0:
        order_target(g.stock, 0)
        log.info(f'死叉卖出 {g.stock}，价格：{current_price:.3f}')

def check_stop(context):
    """止损止盈检查"""
    current_position = context.portfolio.positions[g.stock].quantity
    if current_position == 0:
        return
    
    current_price = get_current_data()[g.stock].last_price
    if not hasattr(g, 'entry_price'):
        return
    
    # 止损
    if current_price < g.entry_price * (1 - g.stop_loss_pct):
        order_target(g.stock, 0)
        log.warning(f'止损触发，卖出 {g.stock}，价格：{current_price:.3f}')
    
    # 止盈
    elif current_price > g.entry_price * (1 + g.take_profit_pct):
        order_target(g.stock, 0)
        log.info(f'止盈触发，卖出 {g.stock}，价格：{current_price:.3f}')
## 二、使用步骤（四步走）

### 步骤1：新建策略
1. 登录 Ptrade 终端，点击左上角 **“策略”** 图标
2. 点击 **“添加策略”**，选择业务类型为 **“股票”**
3. 填写策略名称，例如：`小果双均线策略`
4. 点击 **“确定”**，系统会自动生成一个默认策略模板

### 步骤2：编写策略代码
1. 在策略编辑器中，**删除**默认模板的所有代码
2. 复制 `scripts/dual_ma_strategy.py` 中的完整代码粘贴进去
3. 点击 **“保存”**（快捷键：Ctrl+S）

### 步骤3：配置回测参数
1. 点击 **“新建回测”** 按钮
2. 填写以下参数：
   - **开始时间**：例如 `2023-01-01`
   - **结束时间**：例如 `2023-12-31`
   - **回测资金**：`1000000`（100万元）
   - **回测基准**：`000300.SS`（沪深300指数）
   - **回测频率**：选择 **“日线”**（分钟级别可选）
3. 点击 **“保存”** 按钮
4. 点击 **“回测”** 按钮，系统开始运行回测

### 步骤4：分析回测结果
回测完成后，查看以下面板：
- **策略评价指标**：策略收益、基准收益、Alpha比率、Beta比率、夏普比率、索提诺比率
- **收益曲线**：对比策略收益与基准收益的走势
- **交易日志**：查看每次买卖的详细信息（时间、价格、数量）
- **每日盈亏**：查看每日的盈亏明细

## 三、策略逻辑详解

### 核心逻辑
买入条件：五日均线（MA5）上穿十日均线（MA10）
卖出条件：五日均线（MA5）下穿十日均线（MA10）

### 交易标的
- **股票代码**：`60.SS`（电子）
- **股票池设置**：`set_universe(g.security)`

### 资金管理
- 买入时：**全仓买入**（使用全部可用现金）
- 卖出时：**全部卖出**（清空该股票持仓）

### 代码结构说明
| 函数 | 是否必选 | 执行时机 | 作用 |
|------|----------|----------|------|
| `initialize(context)` | 必选 | 策略启动时（仅1次） | 初始化股票池、全局变量、参数 |
| `handle_data(context, data)` | 必选 | 每分钟/每天执行 | 交易逻辑判断、下单操作 |

## 四、注意事项

### 回测注意事项
1. **股票池设置**：`set_universe()` 必须在 `initialize()` 中调用，否则 `get_history()` 无法获取数据
2. **停牌处理**：停牌日成交量为0，复盘后价格可能跳空，策略需增加过滤条件
3. **滑点设置**：建议设置 `set_slippage(0.001)` 使回测更贴近实盘
4. **佣金设置**：建议设置 `set_commission(0.0003, 5.0)` 模拟真实交易成本
5. **最小交易单位**：股票最小下单100股，可转债最小10张
6. **回测频率**：日线级别在 `15:00` 执行，分钟级别在 `9:31~15:00` 每分钟执行

### 实盘注意事项
1. **交易时间**：股票交易时间为 `9:30~15:00`，建议使用 `run_daily()` 定时执行
2. **涨跌停限制**：涨停无法买入，跌停无法卖出，下单前需判断涨停价和跌停价
3. **资金管理**：不建议全仓买入，建议分批建仓（如每次买入总资金的20%）
4. **日志记录**：使用 `log.info()` 记录关键操作，便于排查问题
5. **行情快照**：`get_snapshot(security)` 仅支持交易模块，回测中不可用

## 五、常见问题解答

### Q1：为什么回测结果显示没有交易？
**可能原因**：
- 股票池设置错误（`set_universe()` 未调用或参数错误）
- 均线周期过大，回测时间太短，没有产生金叉信号
- 股票停牌导致无法交易

**解决方法**：
- 检查 `g.security` 是否正确，确保股票代码格式为 `600570.SS`
- 缩小均线周期（如 MA5/MA10 → MA3/MA5）
- 延长回测时间（至少1年以上）

### Q2：为什么日志报错“股票不在股票池中”？
**原因**：`order()` 函数中指定的股票不在 `set_universe()` 设置的股票池中

**解决方法**：确保 `order(security, amount)` 中的 `security` 与 `set_universe()` 中的股票代码一致

### Q3：如何切换成其他股票？
**修改方法**：在 `initialize()` 函数中修改 `g.security` 的值为其他股票代码
```python
g.security = '0001.SZ'  # 改为银行
## 一、策略必备函数（必写）

```python
initialize(context)                          # 初始化（必写）
handle_data(context, data)                   # 行情/交易主函数（必写）
before_trading_start(context, data)          # 盘前运行
after_trading_end(context, data)             # 盘后运行
tick_data(context, data)                     # Tick 级别处理
on_order_response(context, order_list)       # 委托回调
on_trade_response(context, trade_list)       # 成交回调
```

> `handle_data` 的第二个参数 `data` 为当根 K 线数据，可不使用但建议保留签名。

---

## 二、生成策略工作流（模型必须遵循）

1. **澄清需求**：确认策略类型（择时 / 选股 / 套利 / 事件驱动）、标的范围、周期、风控要求。
2. **锁定 API**：只使用本文件列出的 PTRADE 全局函数；严禁 `security.xxx` / `trade.xxx` / `get_json()` 等 QMT 写法。
3. **选择 / 套用模板**：优先使用下方「策略模板」，或在其基础上修改。
4. **代码生成**：输出完整的 `initialize` + `handle_data`，参数用模块级常量定义，便于在 PTRADE 界面调整。
5. **自检**：生成的代码必须通过 `scripts/validate_strategy.py` 检查（无 QMT API、含 initialize/handle_data）。
6. **运行说明**：附 PTRADE 平台导入 / 回测 / 实盘步骤。

---

## 三、PTRADE 关键约定（必读，否则策略无法运行）

- **全局函数**：`get_price`、`get_history`、`get_positions`、`get_position`、`get_index_stocks`、`get_fundamentals`、`order` 等均为**全局函数**，直接调用，不要当成对象方法。
- **`g` 全局对象**：用 `g.xxx = yyy` 在 `initialize` 中保存自定义状态，在 `handle_data` 中读取。`g` 在 PTRADE 中已预定义。
- **`context` 对象**：`context.portfolio.cash`、`context.portfolio.total_value`、`context.portfolio.positions`、`context.blotter.current_dt`。
- **下单 `order(security, amount, limit_price=None)`**：`amount > 0` 买入，`amount < 0` 卖出；`limit_price=None` 表示市价。每笔数量须为 **100 的整数倍**（1 手 = 100 股）。
- **T+1**：A 股当日买入不可当日卖出，卖出请用 `position.enable_amount`（可用持仓）。
- **行情返回**：`get_price(..., fields=[...], count=N)` 返回 pandas DataFrame，列名为字段名；取数组用 `df["close"].values`。
- **回测撮合**：默认以开盘价成交；使用最新价需订阅实时行情。

---

## 四、设置类 API

```python
set_universe(security_list)                      # 设置股票池
set_benchmark(sids)                              # 设置基准指数
set_commission(commission_ratio, min_commission, type)  # 设置佣金
set_fixed_slippage(fixedslippage)                # 设置固定滑点
set_slippage(slippage)                           # 设置滑点比例
set_volume_ratio(volume_ratio)                   # 设置成交量限制比例
set_limit_mode(limit_mode)                       # 设置涨跌停模式
set_yesterday_position(poslist)                  # 设置昨日持仓
set_parameters(**kwargs)                         # 设置策略参数
set_email_info(email_address, smtp_code, email_subject)  # 设置邮件
```

---

## 五、定时或周期 API

```python
run_daily(context, func, time='9:31')     # 每日定时执行
run_interval(context, func, seconds=10)   # 间隔执行（秒）
```

---

## 六、获取信息类 API

### 6.1 交易日

```python
get_trading_day(day)                          # 获取第N个交易日
get_all_trades_days(date=None)                # 获取所有交易日
get_trade_days(start_date=None, end_date=None, count=None)  # 获取日期范围交易日
get_trading_day_by_date(query_date, day=0)    # 按日期查询交易日
```

### 6.2 市场信息

```python
get_market_list()                             # 获取市场列表
get_market_detail(finance_mic)                # 获取市场详情
```

### 6.3 行情信息

```python
# 获取历史K线（核心API）
get_history(count, frequency, field, security_list, fq=None, include=False, fill='nan', is_dict=False)
get_price(security, start_date=None, end_date=None, frequency='1d', fields=None, fq=None, count=None, is_dict=False)

# 个股委托/成交明细
get_individual_entrust(stocks=None, data_count=50, start_pos=0, search_direction=1, is_dict=False)
get_individual_transaction(stocks=None, data_count=50, start_pos=0, search_direction=1, is_dict=False)

# Tick数据
get_tick_direction(symbols=None, query_date=0, start_pos=0, search_direction=1, data_count=50, is_dict=False)

# 板块排序
get_sort_msg(sort_type_grp=None, sort_field_name=None, sort_type=1, data_count=100)

# 五档行情
get_gear_price(sids)

# 快照行情
get_snapshot(security)

# 涨跌停股票
get_trend_data(date=None, stocks=None, market=None)
```

### 6.4 证券信息

```python
get_stock_name(stocks)                        # 获取股票名称
get_stock_info(stocks, field=None)            # 获取股票基本信息
get_stock_status(stocks, query_type='ST', query_date=None)  # 获取股票状态
get_underlying_code(symbols)                  # 获取正股代码
get_stock_exrights(stock_code, date=None)     # 获取复权因子
get_stock_blocks(stock_code)                  # 获取股票所属板块
get_index_stocks(index_code, date)            # 获取指数成分股
get_industry_stocks(industry_code)            # 获取行业成分股
get_fundamentals(security, table, fields=None, date=None, start_year=None, end_year=None, report_types=None, merge_type=None, is_dataframe=False)  # 财务数据
get_Ashares(date=None)                        # 获取全部A股
get_etf_list()                                # 获取ETF列表
get_etf_info(etf_code)                        # 获取ETF信息
get_etf_stock_list(etf_code)                  # 获取ETF成分股
get_etf_stock_info(etf_code, security)        # 获取ETF成分股信息
get_ipo_stocks()                              # 获取今日可申购新股
get_cb_list()                                 # 获取可转债列表
get_cb_info()                                 # 获取可转债信息
get_reits_list(date=None)                     # 获取REITs列表
```

---

## 七、交易 API

### 7.1 股票交易

```python
order(security, amount, limit_price=None)                  # 限价/市价委托（正买负卖）
order_target(security, amount, limit_price=None)           # 目标仓位
order_value(security, value, limit_price=None)             # 目标市值
order_target_value(security, value, limit_price=None)      # 目标市值
order_market(security, amount, market_type, limit_price=None)  # 市价委托
ipo_stocks_order(submarket_type=None, black_stocks=None)   # 新股申购
after_trading_order(security, amount, entrust_price)       # 盘后委托
after_trading_cancel_order(order_param)                    # 盘后撤单
etf_basket_order(etf_code, amount, price_style=None, position=True, info=None)  # ETF篮子委托
etf_purchase_redemption(etf_code, amount, limit_price=None) # ETF申购赎回
```

### 7.2 公共交易

```python
order_tick(sid, amount, priceGear='1', limit_price=None)   # 逐笔委托
cancel_order(order_param)                                  # 撤单
cancel_order_ex(order_param)                               # 增强撤单
debt_to_stock_order(security, amount)                      # 转债转股
```

### 7.3 融资融券

```python
margin_trade(security, amount, limit_price=None, market_type=None)       # 融资融券
margincash_open(security, amount, limit_price=None, market_type=None, cash_group=None)   # 融资开仓
margincash_close(security, amount, limit_price=None, market_type=None, cash_group=None)  # 融资平仓
margincash_direct_refund(value, cash_group=None)                       # 融资直接还款
marginsec_open(security, amount, limit_price=None, cash_group=None)    # 融券开仓
marginsec_close(security, amount, limit_price=None, market_type=None)  # 融券平仓
marginsec_direct_refund(security, amount, cash_group=None)            # 融券直接还券
```

### 7.4 期货

```python
buy_open(contract, amount, limit_price=None)        # 期货开多
sell_close(contract, amount, limit_price=None, close_today=False)  # 期货平多
sell_open(contract, amount, limit_price=None)       # 期货开空
buy_close(contract, amount, limit_price=None, close_today=False)    # 期货平空
```

---

## 八、查询持仓/订单/成交

```python
get_position(security)              # 获取单只股票持仓
get_positions()                     # 获取所有持仓
get_open_orders(security=None)      # 获取未成交订单
get_order(order_id)                 # 获取订单详情
get_orders(security=None)           # 获取订单列表
get_all_orders(security=None)       # 获取所有订单
get_trades()                        # 获取成交记录
get_deliver(start_date, end_date)   # 获取交割单
get_fundjour(start_date, end_date)  # 获取资金流水
get_lucky_info(start_date, end_date) # 获取中签信息
```

---

## 九、计算/指标 API

```python
get_MACD(close, short=12, long=26, m=9)
get_KDJ(high, low, close, n=9, m1=3, m2=3)
get_RSI(close, n=6)
get_CCI(high, low, close, n=14)
```

---

## 十、其他工具 API

```python
log.debug/info/warning/error/critical()   # 日志输出
is_trade()                                # 是否交易时间
check_limit(security, query_date=None)    # 检查涨跌停
send_email(...)                           # 发送邮件
send_qywx(...)                            # 发送企业微信
permission_test(account=None, end_date=None)  # 权限测试
create_dir(user_path)                     # 创建目录
get_frequency()                           # 获取K线周期
get_business_type()                       # 获取业务类型
get_current_kline_count()                 # 获取当前K线根数
filter_stock_by_status(stocks, filter_type=["ST","HALT","DELISTING"], query_date=None)  # 按状态过滤
check_strategy(strategy_content=None, strategy_path=None)  # 检查策略
fund_transfer(trans_direction, occur_balance, exchange_type="1")  # 资金划转
market_fund_transfer(exchange_type, occur_balance)            # 市场间资金划转
get_research_path()                       # 获取研究模块路径
get_trade_name()                          # 获取交易账户名称
get_user_name(login_account=True)         # 获取用户名称
```

---

## 十一、数据结构（对象）

```python
# g 全局对象（在 initialize 中使用 g.xxx = yyy 赋值）
g = {}  # 自定义全局变量（PTRADE 已预定义，可直接 g.xxx = yyy）

# Context 上下文
context.portfolio            # 资产对象
context.portfolio.cash      # 可用现金
context.portfolio.total_value  # 总资产
context.portfolio.positions # 持仓dict
context.blotter.current_dt  # 当前时间

# BarData K线数据（DataFrame 列）
# open, close, high, low, volume, price, preclose, high_limit, low_limit

# Portfolio 资产对象
context.portfolio.cash           # 可用现金
context.portfolio.total_value     # 总资金
context.portfolio.positions       # 持仓字典 {股票代码: Position}

# Position 持仓对象
position.security           # 证券代码
position.total_amount        # 总持仓数量
position.enable_amount       # 可用持仓（T+1）
position.cost_basis          # 成本
position.avg_cost            # 平均成本

# Order 订单对象
order.id                     # 订单ID
order.dt                     # 委托时间
order.limit_price            # 委托价格
order.amount                 # 委托数量
order.filled                 # 已成交数量
order.status                 # 订单状态
```

---

## 十二、数据字典（状态常量）

```python
# 委托状态(order.status)
0   # 未报
1   # 待报
2   # 已报
3   # 已报待撤
4   # 部成待撤
5   # 部撤
6   # 已撤
7   # 部成
8   # 已成
9   # 废单

# 交易状态(trade_status)
START     # 开盘
PRETR     # 盘前
OCALL     # 集合竞价
TRADE     # 交易
HALT      # 停牌
SUSP      # 暂停
BREAK     # 熔断
POSTR     # 盘后
ENDTR     # 收盘
STOPT     # 停牌
DELISTED  # 退市

# 买卖方向
entrust_bs: 1  # 买
entrust_bs: 2  # 卖

business_direction: 0  # 买
business_direction: 1  # 卖

# frequency 参数频率
"1d"   # 日线
"1m"   # 1分钟
"5m"   # 5分钟
"15m"  # 15分钟
"30m"  # 30分钟
"60m"  # 60分钟
```

---

## 十三、策略模板

### 模板 1：日线双均线策略（金叉买入 / 死叉卖出，含止损止盈）

```python
import numpy as np

SECURITY    = "000001.XSHG"
SHORT_WIN   = 5
LONG_WIN    = 20
TRADE_UNIT  = 100          # 1手=100股
PERIOD      = "1d"
STOP_LOSS   = 0.05         # 止损 5%
TAKE_PROFIT = 0.15         # 止盈 15%

def initialize(context):
    g.security = SECURITY
    g.short_win = SHORT_WIN
    g.long_win = LONG_WIN
    g.buy_price = None
    set_benchmark("000300.XSHG")
    set_universe([SECURITY])
    set_commission(0.00025, 5.0)
    set_slippage(0.002)
    log.info("双均线策略启动 | 标的=%s" % SECURITY)

def handle_data(context, data):
    sym = g.security
    df = get_price(sym, frequency=PERIOD, fields=["close"], count=g.long_win + 5)
    if df is None or len(df) < g.long_win:
        return
    close = df["close"].values.astype(float)
    short_ma = float(np.mean(close[-g.short_win:]))
    long_ma  = float(np.mean(close[-g.long_win:]))
    prev_short = float(np.mean(close[-g.short_win-1:-1]))
    prev_long  = float(np.mean(close[-g.long_win-1:-1]))
    price = float(close[-1])

    pos = get_position(sym)
    holding = int(pos.total_amount) if pos else 0

    # 止损止盈（优先）
    if holding > 0 and g.buy_price:
        pnl = (price - g.buy_price) / g.buy_price
        if pnl <= -STOP_LOSS or pnl >= TAKE_PROFIT:
            order(sym, -holding)
            g.buy_price = None
            return

    gold = (prev_short <= prev_long) and (short_ma > long_ma)
    dead = (prev_short >= prev_long) and (short_ma < long_ma)

    if gold and holding == 0:
        order(sym, TRADE_UNIT)
        g.buy_price = price
        log.info("金叉买入 %s @ %.2f" % (sym, price))
    elif dead and holding > 0:
        order(sym, -holding)
        g.buy_price = None
        log.info("死叉卖出 %s @ %.2f" % (sym, price))
```

> 完整可运行文件见 `templates/dual_ma_strategy.py`。

### 模板 2：布林带策略

```python
import numpy as np

SECURITY = "000001.XSHG"
BOLL_PERIOD = 20
BOLL_STD = 2.0

def initialize(context):
    set_benchmark("000300.XSHG")
    set_universe([SECURITY])

def handle_data(context, data):
    sym = SECURITY
    df = get_price(sym, frequency="1d", fields=["close"], count=BOLL_PERIOD + 5)
    close = df["close"].values.astype(float)
    current = float(close[-1])
    period = close[-BOLL_PERIOD:]
    boll_mid = np.mean(period)
    boll_std = np.std(period, ddof=1)
    upper = boll_mid + BOLL_STD * boll_std
    lower = boll_mid - BOLL_STD * boll_std
    if current <= lower:
        order(sym, 100)
    elif current >= upper:
        pos = get_position(sym)
        holding = int(pos.total_amount) if pos else 0
        if holding > 0:
            order(sym, -holding)
```

### 模板 3：止损止盈策略（修复版，注意 iloc[-1] 取最新价）

```python
STOP_LOSS = 0.05    # 止损5%
TAKE_PROFIT = 0.15  # 止盈15%

def handle_data(context, data):
    sym = "000001.XSHG"
    pos = get_position(sym)
    if pos and pos.total_amount > 0:
        df = get_price(sym, frequency="1d", fields=["close"], count=1)
        current = float(df["close"].iloc[-1])   # 取最新一根，勿用 iloc[-0]
        cost = float(pos.cost_basis)
        profit = (current - cost) / cost
        if profit <= -STOP_LOSS:
            order(sym, -int(pos.enable_amount))  # 止损（用可用持仓）
        elif profit >= TAKE_PROFIT:
            order(sym, -int(pos.enable_amount))  # 止盈
```

### 模板 4（新增）：网格交易策略

```python
SECURITY = "000001.XSHG"
GRID_PCT = 0.02        # 每格间距 2%
UNIT     = 100

def initialize(context):
    g.security = SECURITY
    g.base = None
    set_universe([SECURITY])
    set_benchmark("000300.XSHG")

def handle_data(context, data):
    sym = g.security
    df = get_price(sym, frequency="1d", fields=["close"], count=2)
    price = float(df["close"].values[-1])
    if g.base is None:
        g.base = price
        return
    step = g.base * GRID_PCT
    if price <= g.base - step:
        order(sym, UNIT); g.base = price
        log.info("网格买入 %s @ %.2f" % (sym, price))
    elif price >= g.base + step:
        pos = get_position(sym)
        holding = int(pos.total_amount) if pos else 0
        if holding >= UNIT:
            order(sym, -UNIT); g.base = price
            log.info("网格卖出 %s @ %.2f" % (sym, price))
```

### 模板 5（新增）：二八轮动（沪深300 / 中证500 动量）

```python
IDX_A = "000300.XSHG"   # 沪深300
IDX_B = "000905.XSHG"   # 中证500
LOOKBACK = 20

def initialize(context):
    g.idx = [IDX_A, IDX_B]
    set_universe(g.idx)

def _ret(sym):
    df = get_price(sym, frequency="1d", fields=["close"], count=LOOKBACK)
    c = df["close"].values.astype(float)
    return (c[-1] / c[0]) - 1

def handle_data(context, data):
    ra, rb = _ret(IDX_A), _ret(IDX_B)
    winner = IDX_A if ra >= rb else IDX_B
    for pos in get_positions():
        if pos.security != winner and pos.total_amount > 0:
            order(pos.security, -int(pos.total_amount))
    pos = get_position(winner)
    if (pos is None) or (pos.total_amount == 0):
        order(winner, 100)
        log.info("轮动买入 %s (300收益=%.2f%%, 500收益=%.2f%%)" % (winner, ra*100, rb*100))
```

### 模板 6（新增）：ETF 定投策略

```python
ETF = "510300.XSHG"    # 沪深300ETF
PERIOD_DAYS = 5        # 每5个交易日定投一次
UNIT = 100

def initialize(context):
    g.etf = ETF
    g.cnt = 0
    set_universe([ETF])

def handle_data(context, data):
    g.cnt += 1
    if g.cnt % PERIOD_DAYS != 0:
        return
    order(g.etf, UNIT)
    log.info("定投买入 %s %d 股" % (g.etf, UNIT))
```

### 模板 7（新增）：多标的等权组合（因子选股）

> 完整文件见 `templates/factor_strategy.py`。核心：每月从指数成分股按估值因子选股、等权配置。

```python
import numpy as np

INDEX = "000300.XSHG"
N_HOLD = 10
FACTOR = "PE"

def initialize(context):
    g.index = INDEX
    g.n = N_HOLD
    g.factor = FACTOR
    g.day = 0
    set_benchmark(INDEX)
    set_universe(get_index_stocks(INDEX))

def handle_data(context, data):
    g.day += 1
    if g.day % 20 != 0:
        return
    stocks = get_index_stocks(g.index)
    scores = {}
    for s in stocks:
        try:
            fd = get_fundamentals(s, "valuation", fields=[g.factor])
            if hasattr(fd, "empty") and not fd.empty:
                v = float(fd[g.factor].iloc[-1])
                if v > 0:
                    scores[s] = v
        except Exception as e:
            log.warning("财务数据获取失败 %s: %s" % (s, e))
    target = [s for s, _ in sorted(scores.items(), key=lambda x: x[1])[:g.n]]
    for pos in get_positions():
        if pos.security not in target and pos.total_amount > 0:
            order(pos.security, -int(pos.total_amount))
    for s in target:
        pos = get_position(s)
        if (pos is None) or (pos.total_amount == 0):
            order(s, 100)
```

---

## 十四、风控与最佳实践

- **必须设置股票池**：`set_universe(...)` 决定 `handle_data` 能拿到的数据范围。
- **数量取整到 100**：`order` 的 amount 必须是 100 的整数倍，否则委托会被拒。
- **T+1 卖出约束**：卖出数量不要超过 `position.enable_amount`。
- **ST / 退市过滤**：上线前用 `filter_stock_by_status(stocks, filter_type=["ST","HALT","DELISTING"])` 剔除风险标的。
- **先回测再实盘**：用 `check_strategy(strategy_path=...)` 做静态检查；在 PTRADE 回测通过后再开启实盘。
- **日志而非打印**：用 `log.info(...)` 而非 `print(...)`，便于在 PTRADE 日志面板查看。
- **全局函数陷阱**：再一次强调 —— PTRADE 没有 `security.get_bars` / `trade.open_long` / `get_json`，误用会直接运行失败。

---

## 十五、在 PTRADE 平台运行步骤

1. 打开 PTRADE → 策略研究 → 新建策略
2. 粘贴生成的代码 → 保存（Ctrl+S）
3. 回测：设置时间范围与初始资金，查看收益 / 回撤
4. 参数优化：调整模块级常量（如 SHORT_WIN / LONG_WIN）
5. 实盘：订阅实时行情，开启自动执行

---

## 十六、离线校验（新增）

仓库附带 `scripts/validate_strategy.py`，可在本地（非 PTRADE 环境）快速检查生成的策略是否误用了 QMT API：

```bash
python scripts/validate_strategy.py your_strategy.py
```

校验项：是否包含 `initialize` / `handle_data`、是否出现 `security.get_bars` / `trade.open_long` / `get_json` 等禁用写法、是否使用 PTRADE 全局函数。
# 交易带们参考

"""
策略名称：
三因子日线交易策略
运行周期:
日线
策略流程：
盘前将中小板成分股中st、停牌、退市的股票过滤得到股票池
盘中：
1、获取市场风险溢价、市值因子、账面市值比因子三因子数据，
2、分组差值做线性回归处理，最终得到得分，选择得分高的标的调仓买入
3、每15天换仓一次
注意事项：
策略中调用的order_target_value接口的使用有场景限制，回测可以正常使用，交易谨慎使用。
回测场景下撮合是引擎计算的，因此成交之后持仓信息的更新是瞬时的，但交易场景下信息的更新依赖于柜台数据
的返回，无法做到瞬时同步，可能造成重复下单。详细原因请看帮助文档。
"""
# 导入函数库
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels import regression
from decimal import Decimal


# 初始化此策略
def initialize(context):
    g.factor_params_info = {
        'total_shareholder_equity': ['balance_statement', 'total_shareholder_equity'],
        'roe': ['profit_ability', 'roe']
    }
    set_params()  # 设置策参数
    set_variables()  # 设置中间变量
    if not is_trade():
        set_backtest()  # 设置回测条件


# 设置策参数
def set_params():
    g.tc = 15  # 调仓频率
    g.yb = 63  # 样本长度
    g.N = 10  # 持仓数目
    g.NoF = 3  # 三因子模型


# 设置中间变量
def set_variables():
    g.t = 0  # 记录连续回测天数
    g.rf = 0.04  # 无风险利率
    g.if_trade = False  # 当天是否交易


# 设置回测条件
def set_backtest():
    set_limit_mode('UNLIMITED')


# 每天盘前处理
def before_trading_start(context, data):
    g.current_date = context.blotter.current_dt.strftime("%Y%m%d")
    # 2005-06-01前回测由于数据不足，不执行。
    if g.current_date < '20050601':
        g.trade_flag = False
    else:
        g.trade_flag = True

    g.rf = 0.04
    g.all_stocks = get_index_stocks('000300.XBHS', g.current_date)

    if g.t % g.tc == 0:
        # 每隔g.tc天，交易一次
        g.if_trade = True
        # 将ST、停牌、退市三种状态的股票剔除当日的股票池
        g.all_stocks = filter_stock_by_status(g.all_stocks, filter_type=["ST", "HALT", "DELISTING"], query_date=None)
    g.t += 1


# 每天交易时要做的事情
def handle_data(context, data):
    if not g.trade_flag:
        return

    if g.if_trade:
        df_scores = get_scores(g.all_stocks, str(get_trading_day(-63)), str(get_trading_day(-1)), g.rf)
        # 为每个持仓股票分配资金
        # 依打分排序，当前需要持仓的股票
        if df_scores.empty:
            stock_sort = list()
        else:
            stock_sort = df_scores.sort_values('score')['code'].tolist()
        # 把涨停状态的股票剔除
        up_limit_stock = get_limit_stock(stock_sort)['up_limit']
        # stock_sort = list(set(stock_sort)-set(up_limit_stock))
        stock_sort = [stock for stock in stock_sort if stock not in up_limit_stock]
        position_list = get_position_list(context)
        # 持仓中跌停的股票不做卖出
        limit_info = get_limit_stock(position_list)
        hold_down_limit_stock = limit_info['down_limit']
        log.info('持仓跌停股：%s' % hold_down_limit_stock)
        position_list = get_position_list(context)
        # 持仓中除了不处于前g.N且跌停不能卖的股票进行卖出
        sell_stocks = list(set(position_list) - set(stock_sort[:g.N]) - set(hold_down_limit_stock))
        # 对不在换仓列表中且飞跌停股的股票进行卖出操作
        order_stock_sell(sell_stocks)
        # 获取仍在持仓中的股票
        position_list = get_position_list(context)
        # 获取调仓买入的股票
        buy_stocks = [stock for stock in stock_sort if stock not in position_list][:(g.N - len(position_list))]
        # 仓位动态平衡的股票
        balance_stocks = list(set(buy_stocks + position_list) - set(hold_down_limit_stock))
        every_stock = context.portfolio.portfolio_value / g.N
        order_stock_balance(balance_stocks, every_stock)
        order_stock_balance(balance_stocks, every_stock)
    g.if_trade = False


# 不在换仓目标中且没有跌停的股票进行清仓操作
def order_stock_sell(sell_stocks):
    # 对于不需要持仓的股票，全仓卖出
    for stock in sell_stocks:
        order_target_value(stock, 0)


# 非跌停的换仓目标股进行仓位再平衡
def order_stock_balance(balance_stocks, every_stock):
    for stock in balance_stocks:
        order_target_value(stock, every_stock)


# 获取综合得分
def get_scores(stocks, begin, end, rf):
    try:
        length = len(stocks)
        market_cap_df = get_fundamentals(stocks, 'valuation', fields='total_value', date=begin)
        market_cap_df.dropna(inplace=True)
        if market_cap_df.empty:
            print('获取市值数据失败，股票因子评分失败')
            return pd.DataFrame()
        total_shareholder_equity_df = get_factor_values(stocks, 'total_shareholder_equity', begin, g.factor_params_info)
        total_shareholder_equity_df.dropna(inplace=True)
        if total_shareholder_equity_df.empty:
            print('获取total_shareholder_equity财务数据失败，股票因子评分失败')
            return pd.DataFrame()
        roe_df = get_factor_values(stocks, 'roe', begin, g.factor_params_info)
        roe_df.dropna(inplace=True)
        if roe_df.empty:
            print('获取roe财务数据失败，股票因子评分失败')
            return pd.DataFrame()
        df_all = pd.concat([market_cap_df, total_shareholder_equity_df, roe_df], axis=1)
        df_all.dropna(inplace=True)
        df_all['BTM'] = df_all['total_shareholder_equity'] / df_all['total_value']
        df_all = df_all.reset_index()
        S = df_all.sort_values('total_value')['index'][:int(length / 3)]
        B = df_all.sort_values('total_value')['index'][length - int(length / 3):]
        L = df_all.sort_values('BTM')['index'][:int(length / 3)]
        H = df_all.sort_values('BTM')['index'][length - int(length / 3):]
        W = df_all.sort_values('roe')['index'][:int(length / 3)]
        R = df_all.sort_values('roe')['index'][length - int(length / 3):]

        close_data = get_price(stocks, begin, end, fields='close', frequency='1d', is_dict=True)

        close_df = pd.DataFrame()
        for stock_code, stock_data in close_data.items():
            date_info = pd.to_datetime(stock_data['datetime'], format='%Y%m%d')
            close_info = stock_data['close']
            close_df[stock_code] = pd.Series(close_info, index=date_info)
        close_df.sort_index(inplace=True)
        df = np.diff(np.log(close_df), axis=0) + 0 * close_df[1:]
        SMB = df[S].T.sum() / len(S) - df[B].T.sum() / len(B)
        HML = df[H].T.sum() / len(H) - df[L].T.sum() / len(L)
        RMW = df[R].T.sum() / len(R) - df[W].T.sum() / len(W)
        dp = get_price('000300.XSHG', begin, end, '1d')['close']
        if len(dp)-len(df)>1:
            log.info('历史行情数据缺失，股票因子评分失败')
            return pd.DataFrame()
        RM = np.diff(np.log(dp)) - rf / 252
        X = pd.DataFrame({"RM": RM, "SMB": SMB, "HML": HML, "RMW": RMW})
        factor_flag = ["RM", "SMB", "HML", "RMW"][:g.NoF]
        X = X[factor_flag]
        t_scores = [0.0] * length
        for i in range(length):
            t_stock = stocks[i]
            t_r = linreg(X, df[t_stock] - rf / 252, len(factor_flag))
            t_scores[i] = t_r[0]
        scores = pd.DataFrame({'code': stocks, 'score': t_scores})
        df_scores = scores.sort_values(by='score')
        return df_scores
    except:
        print('股票因子评分失败，请检查数据')
        return pd.DataFrame()


# 获取因子值
def get_factor_values(stock_list, factor, date, factor_params_info):
    """
    获取因子值方法
    入参：
    1、股票池：stock_list
    2、因子名称：factor
    3、计算日期：date
    4、因子数据获取需要维护的信息（因子名称、表名、字段名）
    """
    data = get_fundamentals(stock_list, table=factor_params_info[factor][0], fields=factor_params_info[factor][1],
                            date=date, is_dataframe=True)
    factor_info = {}
    for stock in stock_list.copy():
        if stock not in data.index:
            continue
        factor_info[stock] = data.loc[stock, factor_params_info[factor][1]]
    if factor_info == {}:
        return pd.DataFrame()
    factor_df = pd.DataFrame.from_dict(factor_info, orient='index')
    factor_df.columns = [factor_params_info[factor][1]]
    return factor_df


# 线性回归
def linreg(x, y, columns=3):
    x = sm.add_constant(np.array(x))
    y = np.array(y)
    if len(y) > 1:
        results = regression.linear_model.OLS(y, x).fit()
        return results.params
    else:
        return [float("nan")] * (columns + 1)


# 保留小数点两位
def replace(x):
    x = Decimal(x)
    x = float(str(round(x, 2)))
    return x


# 生成昨日持仓股票列表
def get_position_list(context):
    return [
        position.sid
        for position in context.portfolio.positions.values()
        if position.amount != 0
    ]


# 日级别回测获取持仓中不能卖出的股票(涨停就不卖出)
def get_limit_stock(stock_list):
    out_info = {'up_limit': [], 'down_limit': []}
    for stock in stock_list:
        limit_status = check_limit(stock)[stock]
        if limit_status == 1:
            out_info['up_limit'].append(stock)
        elif limit_status == -1:
            out_info['down_limit'].append(stock)
    return out_info
################################
"""
策略名称：
指数增强日线交易策略
策略流程：
盘前：
1、将沪深300成分股中st、停牌、退市的股票过滤得到股票池
2、示例用roe作为单因子选出排名第一档的股票作为目标股票池
盘中：
1、财报调仓日或者固定间隔调仓日通过线性规划的方法进行调仓，以图实现增强效果
注意事项：
策略中调用的order_target、order_target_value接口的使用有场景限制，回测可以正常使用，交易谨慎使用。
回测场景下撮合是引擎计算的，因此成交之后持仓信息的更新是瞬时的，但交易场景下信息的更新依赖于柜台数据
的返回，无法做到瞬时同步，可能造成重复下单。详细原因请看帮助文档。
"""
import pandas as pd
import numpy as np
import statsmodels.api as sm
import math
from decimal import Decimal
import datetime
from datetime import date as justdate
from scipy.optimize import minimize


# 初始化
def initialize(context):
    g.factor = 'roe'
    g.factor_params_info = {'roe': ['profit_ability', 'roe', False],  # 净资产收益率,最后布尔值为排序方式
                            'operating_revenue_grow': ['growth_ability', 'operating_revenue_grow_rate', False],  # 营收增速
                            'net_profit_grow': ['growth_ability', 'np_parent_company_cut_yoy', False],  # 扣非净利润增速
                            }
    set_params()  # 设置策参数
    set_variables()  # 设置中间变量
    is_trade_flag = is_trade()
    if is_trade_flag:
        pass
    else:
        set_backtest()  # 设置回测条件


# 设置策参数
def set_params():
    g.percent = 0.10
    g.est_interval = 80  # 记录优化区间，使用二次规划根据这个区间最优化权重
    g.lamda = 0
    g.hold_days = 60
    g.max_hold_num = 20  # 最大持仓的股票
    g.run_days = 0
    g.benchmark = '000300.SS'
    # 财报季度调仓所依据的指定日期
    g.finance_update_date_list = ['0401', '0801', '1001']


# 设置中间变量
def set_variables():
    g.init_screen = True
    g.is_update_stocks = False


# 设置回测条件
def set_backtest():
    set_limit_mode('UNLIMITED')  # 回测撮合不限制成交量


# 盘前处理
def before_trading_start(context, data):
    g.current_date = context.blotter.current_dt.strftime('%Y%m%d')
    # 2008-01-01前回测由于数据不足，不执行。
    if g.current_date < '20080101':
        g.trade_flag = False
    else:
        g.trade_flag = True
    if not g.trade_flag:
        return
    g.everyStock = 0
    if is_pub_date(g.current_date):  # 财报调仓日
        g.stocks = create_stocks()
        g.is_update_stocks = True
    elif g.init_screen:
        '''初始化一个组合，这一小段代码只会用一次'''
        g.stocks = create_stocks()
        g.is_update_stocks = True
        g.init_screen = False  # 将Flag置为False，保证下次不再运行


# 每天交易时要做的事情
def handle_data(context, data):
    if not g.trade_flag:
        return
    # 如果到公告日更新了调仓
    if g.is_update_stocks:
        stock_sort = g.stocks
        log.info('初始日或调仓日股票池')
        log.info(stock_sort)
        if not stock_sort:
            return
        previous_date = get_trading_day(-1)
        # 通过二次规划确定权重
        weight = get_weights(stock_sort, previous_date)
        stock_weight = dict(zip(stock_sort, weight))
        stocks = stock_sort
        current_hold_set = set(context.portfolio.positions.keys())
        if set(stocks) != current_hold_set:
            need_buy = set(stocks).difference(current_hold_set)
            need_sell = current_hold_set.difference(stocks)
            current_stocks = set(stocks).difference(need_buy)
            try:
                for stock in need_sell:
                    order_target(stock, 0)
                for stock in need_buy:
                    order_value(stock, context.portfolio.portfolio_value * stock_weight[stock])
                for stock in current_stocks:
                    order_target_value(stock, context.portfolio.portfolio_value * stock_weight[stock])
            except:
                pass
        g.is_update_stocks = False
        g.run_days = 0

    elif g.run_days % g.hold_days == 0:
        stocks = g.stocks
        log.info('非调仓日股票池')
        log.info(stocks)
        if not stocks:
            return
        '''这里的权重通过二次规划确定'''
        weight = get_weights(stocks, context.previous_date)
        stock_weight = dict(zip(stocks, weight))
        try:
            for stock in stocks:
                order_target_value(stock, context.portfolio.portfolio_value * stock_weight[stock])
        except:
            pass
    if context.portfolio.cash > 0:
        # 如果可用资金大于0，说明没有全仓，就是撮合单的时候出问题，所以需要重新买入，这时候重新全仓买入几个ETF
        log.info('尝试把剩余资金用完，买入ETF')
        cash = context.portfolio.cash
        order_value('510300.SS', cash / 10 * 4)
        order_value('510330.SS', cash / 10 * 3)
        order_value('510500.SS', cash / 10 * 3)
    g.run_days += 1


# 建立股票池
def create_stocks():
    g.all_stocks = get_index_stocks('000300.XBHS', g.current_date)
    for stock in g.all_stocks.copy():
        if stock[:3] == '688':
            g.all_stocks.remove(stock)
    # 将ST、停牌、退市三种状态的股票剔除当日的股票池
    g.all_stocks = filter_stock_by_status(g.all_stocks, filter_type=["ST", "HALT", "DELISTING"], query_date=None)
    return get_stocks(g.all_stocks, str(get_trading_day(-1)), g.factor)


# 获取拟持仓股票池
def get_stocks(stocks, date, factor):
    sort_type = g.factor_params_info[factor][-1]
    df = get_factor_values(stocks, factor, date, g.factor_params_info)
    df.dropna(inplace=True)
    if df.empty:
        print('%s数据获取失败，选股失败' % factor)
        return list()
    # 3倍标准差去极值
    df = winsorize(df, factor, std=3, have_negative=True)
    # z标准化
    df = standardize(df, factor, ty=2)
    # 市值中性化
    market_cap_df = get_fundamentals(stocks, 'valuation', fields='total_value', date=date)
    market_cap_df = market_cap_df[['total_value']]
    market_cap_df.dropna(inplace=True)
    if market_cap_df.empty:
        print('市值数据获取失败，选股失败')
        return list()
    df = neutralization(df, factor, market_cap_df)
    df = df.sort_values(by=factor, ascending=sort_type)
    return list(df.head(int(len(df) * g.percent)).index)


# 获取因子值
def get_factor_values(stock_list, factor, date, factor_params_info):
    """
    获取因子值方法
    入参：
    1、股票池：stock_list
    2、因子名称：factor
    3、计算日期：date
    4、因子数据获取需要维护的信息（因子名称、表名、字段名）
    """
    data = get_fundamentals(stock_list, table=factor_params_info[factor][0], fields=factor_params_info[factor][1],
                            date=date, is_dataframe=True)
    factor_info = {}
    for stock in stock_list.copy():
        if stock not in data.index:
            continue
        factor_info[stock] = data.loc[stock, factor_params_info[factor][1]]
    if factor_info == {}:
        return pd.DataFrame()
    factor_df = pd.DataFrame.from_dict(factor_info, orient='index')
    factor_df.columns = [factor_params_info[factor][1]]
    return factor_df


# 使用二次规划确定权重  
def get_weights(stocks, date):
    date = date.strftime('%Y-%m-%d')
    start_date = get_trading_day(-(g.est_interval + 1)).strftime('%Y-%m-%d')
    price_data = get_price(stocks, start_date=start_date, end_date=date, frequency='daily',
                           fields=['close'], is_dict=True)
    
    close_df = pd.DataFrame()
    for stock_code, stock_data in price_data.items():
        date_info = pd.to_datetime(stock_data['datetime'], format='%Y%m%d')
        close_info = stock_data['close']
        close_df[stock_code] = pd.Series(close_info, index=date_info)
    close_df.sort_index(inplace=True)    

    code_list = list(close_df.columns)
    df_list = []
    for stock in code_list:
        df = close_df[[stock]]
        df['change'] = 0 
        df['change'] = df[stock] / df[stock].shift(1) - 1
        df[stock] = df['change']
        df = df[[stock]]
        df.fillna(0, inplace=True)
        df_list.append(df)

    result = pd.concat(df_list, axis=1)
    index_price = get_price(g.benchmark, start_date=start_date, end_date=date, frequency='daily',
                            fields=['close'], is_dict=False)
    index_r = index_price.pct_change()
    index_r.fillna(0, inplace=True)
    weight = calculate_weight(np.array(result), np.array(index_r))
    return weight


def calculate_weight(train_returns, target_returns):
    length = len(train_returns.T)

    # 定义二次线性规划目标函数
    def objective(weights):
        return np.sum((np.dot(train_returns, weights) - target_returns) ** 2)

    # 定义约束条件
    constraints = [{'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1},
                   {'type': 'ineq', 'fun': lambda weights: 0.2 - np.max(weights)}
                   ]
    # 定义权重的取值范围（可以设置最小权重和最大权重区间）
    min_weight = (1 / length) * 0.2  # 最小权重
    max_weight = (1 / length) * 5  # 最大权重
    bounds = [(min_weight, max_weight)] * train_returns.shape[1]
    # 初始化权重
    initial_weights = np.ones(train_returns.shape[1]) / train_returns.shape[1]
    # 最小化目标函数，求解权重
    result = minimize(objective, initial_weights, constraints=constraints, bounds=bounds)
    # 输出结果
    test_weights = result.x
    # print("测试集投资权重：", test_weights)
    return test_weights


# 保留小数点两位
def replace(x):
    x = Decimal(x)
    x = float(str(round(x, 2)))
    return x


# 去极值函数（3倍标准差去极值）
def winsorize(factor_data, factor, std=3, have_negative=True):
    """
    去极值函数
    factor:以股票code为index，因子值为value的Series
    std为几倍的标准差，have_negative 为布尔值，是否包括负值
    输出Series
    """
    r = factor_data[factor]
    if not have_negative:
        r = r[r >= 0]
    # 取极值
    edge_up = r.mean() + std * r.std()
    edge_low = r.mean() - std * r.std()
    r[r > edge_up] = edge_up
    r[r < edge_low] = edge_low
    r = pd.DataFrame(r)
    return r


# z－score标准化函数：
def standardize(factor_data, factor, ty=2):
    """
    s为Series数据
    ty为标准化类型:1 MinMax,2 Standard,3 maxabs
    """
    temp = factor_data[factor]
    re = 0
    if int(ty) == 1:
        re = (temp - temp.min()) / (temp.max() - temp.min())
    elif ty == 2:
        re = (temp - temp.mean()) / temp.std()
    elif ty == 3:
        re = temp / 10 ** np.ceil(np.log10(temp.abs().max()))
    return pd.DataFrame(re)


# 市值中性化函数
def neutralization(data_factor, factor, data_market_cap):
    data_market_cap['total_value2'] = 0
    data_market_cap['total_value2'] = data_market_cap['total_value'].apply(lambda a: math.log(a))
    df = pd.concat([data_factor, data_market_cap], axis=1, join='inner')
    y = df[factor]
    x = df['total_value2']
    result = sm.OLS(y, x).fit()
    result = pd.DataFrame(result.resid)
    result.columns = [factor]
    return result


# 判断当天时间是不是出财报的下一天时间
def is_pub_date(current_date):
    cur_year = current_date[:4]
    trade_dates = []
    # 按季度选股，在4.30、8.31、10.31三个时间日重新根据财务报表选择股票
    for date in g.finance_update_date_list:
        trade_dates.append(get_trading_day_by_date(cur_year+date, day=0))
    if current_date in trade_dates:
        return True
    return False
######################################
"""
策略名称：
AROON指标策略
注意事项：
策略中调用的order_target接口的使用有场景限制，回测可以正常使用，交易谨慎使用。
回测场景下撮合是引擎计算的，因此成交之后持仓信息的更新是瞬时的，但交易场景下信息的更新依赖于柜台数据
的返回，无法做到瞬时同步，可能造成重复下单。详细原因请看帮助文档。
"""
import talib as ta


# 初始化
def initialize(context):
    g.stock = "000333.SZ"
    g.period = 20


# 每个交易日处理
def before_trading_start(context, data):
    current_date = context.blotter.current_dt.strftime('%Y-%m-%d')
    # 2013-10-01前回测由于数据不足，不执行。
    if current_date < '2013-10-01':
        g.trade_flag = False
    else:
        g.trade_flag = True


def handle_data(context, data):
    if not g.trade_flag:
        return
    log.info(g.stock + '当前持仓' + str(get_position(g.stock).amount))
    high = get_history(g.period * 2, frequency='1d', field='high', security_list=g.stock, fq='pre', is_dict=True)
    low = get_history(g.period * 2, frequency='1d', field='low', security_list=g.stock, fq='pre', is_dict=True)
    # 通过talib库计算AROON指标值   
    aroon_down, aroon_up = ta.AROON(high[g.stock]['high'], low[g.stock]['low'], g.period)
    aroon = aroon_up - aroon_down
    signal = 0
    if aroon_up[-2] < 70 <= aroon_up[-1] and aroon[-1] > 0:
        signal += 1
    if aroon_down[-2] < 70 <= aroon_down[-1] and aroon[-1] < 0:
        signal += -1
    if aroon_up[-2] > 50 >= aroon_up[-1] and aroon[-1] < 0:
        signal += -1
    if aroon_down[-2] > 50 >= aroon_down[-1] and aroon[-1] > 0:
        signal += 1
    if signal > 0 and get_position(g.stock).amount == 0:
        order_value(g.stock, context.portfolio.cash)
    if signal < 0 < get_position(g.stock).amount:
        order_target(g.stock, 0)
########################################
"""
策略名称：
单因子日线交易策略
策略流程：
盘前将中小板成分股中st、停牌、退市的股票过滤得到股票池
盘中：
1、通过极值处理、标准化处理、市值中性化处理
2、因子排序获得股票池
3、动态平衡仓位
注意事项：
策略中调用的order_target_value接口的使用有场景限制，回测可以正常使用，交易谨慎使用。
回测场景下撮合是引擎计算的，因此成交之后持仓信息的更新是瞬时的，但交易场景下信息的更新依赖于柜台数据
的返回，无法做到瞬时同步，可能造成重复下单。详细原因请看帮助文档。
"""
import pandas as pd
import numpy as np
import statsmodels.api as sm
import math
from decimal import Decimal


# 初始化处理
def initialize(context):
    g.factor = 'roe'
    g.factor_params_info = {
        'roe': ['profit_ability', 'roe', False],  # 净资产收益率,最后布尔值为排序方式
        'operating_revenue_grow_rate': ['growth_ability', 'operating_revenue_grow_rate', False],
        # 营收增速
        'np_parent_company_cut_yoy': ['growth_ability', 'np_parent_company_cut_yoy', False],
        # 扣非净利润增速
    }
    # 初始化此策略
    set_params()  # 设置策参数
    set_variables()  # 设置中间变量
    if not is_trade():
        set_backtest()  # 设置回测条件


# 设置策参数
def set_params():
    g.tc = 15  # 调仓频率
    g.yb = 63  # 样本长度
    g.N = 20  # 持仓数目
    g.NoF = 3  # 三因子模型
    g.percent = 0.10


# 设置中间变量
def set_variables():
    g.days = 0  # 记录连续回测天数
    g.rf = 0.04  # 无风险利率
    g.is_trade = False  # 当天是否交易
    g.every_stock = 0


# 设置回测条件
def set_backtest():
    set_limit_mode('UNLIMITED')


# 盘前处理
def before_trading_start(context, data):
    g.current_date = context.blotter.current_dt.strftime("%Y%m%d")
    # g.all_stocks = get_index_stocks('000906.XBHS', g.current_date)
    g.all_stocks = get_index_stocks('000300.XBHS', g.current_date)
    if g.days % g.tc == 0:
        # 每g.tc天，交易一次行
        g.is_trade = True
        # 将ST、停牌、退市三种状态的股票剔除当日的股票池
        g.all_stocks = filter_stock_by_status(g.all_stocks, filter_type=["ST", "HALT", "DELISTING"], query_date=None)
    g.days += 1


# 每天交易时要做的事情
def handle_data(context, data):
    if g.is_trade:
        stock_sort = get_stocks(g.all_stocks, str(get_trading_day(-1)), g.factor)
        # 把涨停状态的股票剔除
        up_limit_stock = get_limit_stock(context, stock_sort)['up_limit']
        stock_sort = [stock for stock in stock_sort if stock not in up_limit_stock]
        position_list = get_position_list(context)
        # 持仓中跌停的股票不做卖出
        limit_info = get_limit_stock(context, position_list)
        hold_down_limit_stock = limit_info['down_limit']
        log.info('持仓跌停股：%s' % hold_down_limit_stock)
        # 持仓中除了不处于前g.N且跌停不能卖的股票进行卖出
        sell_stocks = list(set(position_list) - set(stock_sort[:g.N]) - set(hold_down_limit_stock))
        # 对不在换仓列表中且飞跌停股的股票进行卖出操作
        order_stock_sell(context, data, sell_stocks)
        # 获取仍在持仓中的股票
        position_list = get_position_list(context)
        # 获取调仓买入的股票
        buy_stocks = [stock for stock in stock_sort if stock not in position_list][:(g.N - len(position_list))]
        # 仓位动态平衡的股票
        balance_stocks = list(set(buy_stocks + position_list) - set(hold_down_limit_stock))
        log.info('balance_stocks%s' % len(balance_stocks))
        g.every_stock = context.portfolio.portfolio_value / g.N
        log.info('g.every_stock%s' % g.every_stock)
        order_stock_balance(context, data, balance_stocks)
        order_stock_balance(context, data, balance_stocks)
    g.is_trade = False


# 不在换仓目标中且没有跌停的股票进行清仓操作
def order_stock_sell(context, data, sell_stocks):
    # 对于不需要持仓的股票，全仓卖出
    for stock in sell_stocks:
        stock_sell = stock
        order_target_value(stock_sell, 0)


# 非跌停的换仓目标股进行仓位再平衡
def order_stock_balance(context, data, balance_stocks):
    for stock in balance_stocks:
        order_target_value(stock, g.every_stock)


# 获取拟持仓股票池
def get_stocks(stocks, date, factor):
    sort_type = g.factor_params_info[factor][-1]
    df = get_factor_values(stocks, factor, date, g.factor_params_info)
    df.dropna(inplace=True)
    if df.empty:
        print('%s数据获取失败，选股失败' % factor)
        return list()
    # 3倍标准差去极值
    df = winsorize(df, factor, std=3, have_negative=True)
    # z标准化
    df = standardize(df, factor, ty=2)
    # 市值中性化
    market_cap_df = get_fundamentals(stocks, 'valuation', fields='total_value', date=date)
    market_cap_df.dropna(inplace=True)
    if market_cap_df.empty:
        print('市值数据获取失败，选股失败')
        return list()
    market_cap_df = market_cap_df[['total_value']]
    # 中性化处理
    df = neutralization(df, factor, market_cap_df)
    df = df.sort_values(by=factor, ascending=sort_type)
    return list(df.head(int(len(df) * g.percent)).index)


# 获取因子值
def get_factor_values(stock_list, factor, date, factor_params_info):
    """
    获取因子值方法
    入参：
    1、股票池：stock_list
    2、因子名称：factor
    3、计算日期：date
    4、因子数据获取需要维护的信息（因子名称、表名、字段名）
    """
    data = get_fundamentals(stock_list, table=factor_params_info[factor][0], fields=factor_params_info[factor][1],
                            date=date, is_dataframe=True)
    factor_info = {}
    for stock in stock_list.copy():
        if stock not in data.index:
            continue
        factor_info[stock] = data.loc[stock, factor_params_info[factor][1]]
    if factor_info == {}:
        return pd.DataFrame()
    factor_df = pd.DataFrame.from_dict(factor_info, orient='index')
    factor_df.columns = [factor_params_info[factor][1]]
    return factor_df


# 保留小数点两位
def replace(x):
    x = Decimal(x)
    x = float(str(round(x, 2)))
    return x


# 生成昨日持仓股票列表
def get_position_list(context):
    position_last_list = [
        position.sid
        for position in context.portfolio.positions.values()
        if position.amount != 0
    ]
    return position_last_list


# 日级别回测获取持仓中不能卖出的股票(涨停就不卖出)
def get_limit_stock(context, stock_list):
    out_info = {'up_limit': [], 'down_limit': []}
    for stock in stock_list:
        limit_status = check_limit(stock)[stock]
        if limit_status == 1:
            out_info['up_limit'].append(stock)
        elif limit_status == -1:
            out_info['down_limit'].append(stock)
    return out_info


# 去极值函数（3倍标准差去极值）
def winsorize(factor_data, factor, std=3, have_negative=True):
    """
    去极值函数
    factor:以股票code为index，因子值为value的Series
    std为几倍的标准差，have_negative 为布尔值，是否包括负值
    输出Series
    """
    r = factor_data[factor]
    if not have_negative:
        r = r[r >= 0]
    # 取极值
    edge_up = r.mean() + std * r.std()
    edge_low = r.mean() - std * r.std()
    r[r > edge_up] = edge_up
    r[r < edge_low] = edge_low
    r = pd.DataFrame(r)
    return r


# z－score标准化函数：
def standardize(factor_data, factor, ty=2):
    """
    s为Series数据
    ty为标准化类型:1 MinMax,2 Standard,3 maxabs
    """
    temp = factor_data[factor]
    re = 0
    if int(ty) == 1:
        re = (temp - temp.min()) / (temp.max() - temp.min())
    elif ty == 2:
        re = (temp - temp.mean()) / temp.std()
    elif ty == 3:
        re = temp / 10 ** np.ceil(np.log10(temp.abs().max()))
    return pd.DataFrame(re)


# 市值中性化函数
def neutralization(data_factor, factor, data_market_cap):
    data_market_cap['total_value2'] = 0
    data_market_cap['total_value2'] = data_market_cap['total_value'].apply(lambda a: math.log(a))
    df = pd.concat([data_factor, data_market_cap], axis=1, join='inner')
    y = df[factor]
    x = df['total_value2']
    result = sm.OLS(y, x).fit()
    result = pd.DataFrame(result.resid)
    result.columns = [g.factor]
    return result
##########################################
"""
策略名称：
二八轮动策略
运行周期:
日线
策略流程：
策略通过计算沪深300、中证500的阶段动量数据，来决定持有沪深300ETF还是中证500ETF还是货币基金
持有至少10天
注意事项：
策略中调用的order_target接口的使用有场景限制，回测可以正常使用，交易谨慎使用。
回测场景下撮合是引擎计算的，因此成交之后持仓信息的更新是瞬时的，但交易场景下信息的更新依赖于柜台数据
的返回，无法做到瞬时同步，可能造成重复下单。详细原因请看帮助文档。
"""


# 初始化
def initialize(context):
    set_params()
    g.signal = 0
    g.open_date = get_trading_day(-40)
    # 基金池: 沪深300，中证500，货币基金
    g.fund_list = ['000300.SS', '510300.SS',
                   '000905.SS', '510500.SS',
                   '511880.SS', '511880.SS']

    if not is_trade():
        set_backtest()  # 设置回测条件


# 设置策略参数
def set_params():
    g.N = 20  # N日涨幅
    g.holding_days = 10  # 至少持有天数（交易日）
    g.rise_threshold = 0  # 涨幅阈值


# 设置回测条件
def set_backtest():
    set_limit_mode('UNLIMITED')
    set_commission(commission_ratio=0.00015, min_commission=5.0)


def before_trading_start(context, data):
    current_date = context.blotter.current_dt.strftime('%Y%m%d')
    # 2005-05-01前回测由于数据不足，不执行。
    if current_date < '20050501':
        g.trade_flag = False
    else:
        g.trade_flag = True


# 盘中处理
def handle_data(context, data):
    if not g.trade_flag:
        return
    # 产生信号并交易
    g.signal = create_signal(g.fund_list, g.N, g.rise_threshold)
    trade(context, g.signal, g.fund_list, g.holding_days)
    return


# 交易函数
def trade(context, signal, security_round_list, holding_days):
    security_round_num = int(len(security_round_list) / 2)  # 轮动组数
    pre_trading_date = get_trading_day(-holding_days - 1)
    days = (g.open_date - pre_trading_date).days
    if days > 0:
        return
    hold = set(context.portfolio.positions.keys())
    if signal == 0:  # 买货币基金
        to_buy = {security_round_list[(security_round_num - 1) * 2 + 1]}
    else:
        to_buy = {security_round_list[(signal - 1) * 2 + 1]}
    sell = hold - to_buy
    buy = to_buy - hold
    if sell:
        order_target(list(sell)[0], 0)
    if buy:
        target_value = context.portfolio.cash
        order_value(list(buy)[0], target_value)
        g.open_date = context.current_dt.date()
    return


# 产生信号，返回signal
def create_signal(fund_list, num, rise_threshold):
    price_rise = [0, 0, 0, 0]
    max_rise_index = 0  # 涨幅最大的指数
    price_rise_max = -999999  # 价格涨幅
    security_round_num = int(len(fund_list) / 2)  # 轮动组数
    # 货币基金不参与计算信号
    for i in range(security_round_num - 1):
        stock = fund_list[i * 2]
        his_data = get_history(num + 1, frequency='1d', field='close', security_list=stock, fq=None,
                               include=False, is_dict=True)
        price_rise[i] = his_data[stock]['close'][-1] / his_data[stock]['close'][-num - 1] - 1  # N日涨幅
        if price_rise[i] > price_rise_max:
            max_rise_index = i
            price_rise_max = price_rise[i]
    if price_rise[max_rise_index] > rise_threshold:
        signal = max_rise_index + 1
    else:
        signal = security_round_num
    return signal
###########################################
"""
策略名称：
阳线策略
注意事项：
策略中调用的order_target、order_target_value接口的使用有场景限制，回测可以正常使用，交易谨慎使用。
回测场景下撮合是引擎计算的，因此成交之后持仓信息的更新是瞬时的，但交易场景下信息的更新依赖于柜台数据
的返回，无法做到瞬时同步，可能造成重复下单。详细原因请看帮助文档。
"""
import numpy as np
from decimal import Decimal


def initialize(context):
    if is_trade():
        log.info('-----trade-------')
    else:
        set_fixed_slippage(0.0)
        set_slippage(slippage=0.01)
        set_limit_mode('UNLIMITED')
    g.before_start = False
    # 持仓数量
    g.hold_num = 10


def before_trading_start(context, data):
    g.current_date = context.blotter.current_dt.strftime("%Y%m%d")
    # 持仓股昨日最低价容器
    g.holds_pre_low_price = {}
    # 今日开盘价容器
    g.open_price_info = {}
    # 昨日持仓股
    g.position_list = []
    # 获取全市场股票，选最近10个交易日K线，判断个股形态：最近的一个阴K线之后没有阳线结构，符合形态且当天没有停牌的就加入股票池
    g.stock_list = get_Ashares()

    his_data_info = get_history(10, frequency='1d', field=['open', 'close', 'volume'],
                                security_list=g.stock_list, fq=None, include=False, is_dict=True)
    halt_status = get_stock_status(g.stock_list, 'HALT')
    g.buy_stocks = []
    for stock in g.stock_list.copy():
        # 停牌的过滤
        if halt_status[stock]:
            continue
        his_data = his_data_info[stock]
        his_data = np.array(list(filter(volume_filter, his_data)))
        if len(his_data) < 2:
            continue
        yinx_flag = False
        yangx_flag = False
        is_true = False
        for stock_data in reversed(his_data):
            if stock_data['close'] < stock_data['open']:
                yinx_flag = True
            if stock_data['close'] > stock_data['open']:
                yangx_flag = True
            if yinx_flag and not yangx_flag:
                is_true = True
                break
            if not yinx_flag and yangx_flag:
                is_true = False
                break
        if is_true:
            g.buy_stocks.append(stock)
    g.before_start = True
    g.first_handledata = False
    total_value = context.portfolio.portfolio_value
    g.cash = total_value / g.hold_num

    # 对持仓进行数据载入
    g.position_list = position_last_close_init(context)
    log.info(('盘前查询持仓股:', g.position_list))
    log.info(len(g.position_list))
    # 判断持仓股是否停牌，停牌的标的当日不做交易判断
    halt_status = get_stock_status(g.position_list, 'HALT')
    pre_low_data = get_history(1, '1d', 'low', security_list=g.position_list, fq='dypre', is_dict=True)
    for stock in g.position_list.copy():
        # 停牌的过滤
        if halt_status[stock]:
            g.position_list.remove(stock)
            continue
        # 非停牌持仓股获取昨日最低价
        g.holds_pre_low_price[stock] = pre_low_data[stock]['low'][0]


def handle_data(context, data):
    # 确保盘前处理已完成
    if not g.before_start:
        return
    g.K_num = get_current_kline_count()
    # 第一分钟处理
    if not g.first_handledata:
        # 回测场景持仓股及拟买股票池赋值开盘价
        if not is_trade():
            for stock in g.buy_stocks:
                g.open_price_info[stock] = data[stock].open
            for stock in g.position_list:
                g.open_price_info[stock] = data[stock].open
        g.first_handledata = True

    # 14:45之前持仓股如果符合最新价小于昨日最低价条件清仓
    if g.K_num < 225:
        if is_trade():
            for stock in g.position_list.copy():
                snapshot = get_snapshot(stock)
                if snapshot[stock]['last_px'] < g.holds_pre_low_price[stock]:
                    order_target(stock, 0)
                    g.position_list.remove(stock)
        else:
            for stock in g.position_list.copy():
                if data[stock].close < g.holds_pre_low_price[stock]:
                    order_target(stock, 0)
                    g.position_list.remove(stock)

    # 14:45分对非涨停状态的个股进行清仓
    if g.K_num == 225:
        for stock in g.position_list.copy():
            stock_flag = check_limit(stock)[stock]
            if stock_flag != 1:
                order_target(stock, 0)
                g.position_list.remove(stock)

    # 14:50分进行买入,校验当日实体阳线K线
    if g.K_num == 230:
        hold_list = position_last_close_init(context)
        if is_trade():
            count = 0
            for stock in g.buy_stocks:
                if count + len(hold_list) < g.hold_num and stock not in hold_list:
                    snapshot = get_snapshot(stock)
                    if snapshot[stock]['last_px'] > g.open_price_info[stock]:
                        order_target_value(stock, g.cash)
                        count += 1
        else:
            count = 0
            for stock in g.buy_stocks:
                if count + len(hold_list) < g.hold_num and stock not in hold_list:
                    if data[stock].close > g.open_price_info[stock]:
                        order_target_value(stock, g.cash)
                        count += 1


# 生成持仓股票列表
def position_last_close_init(context):
    position_last_list = []
    for stock in context.portfolio.positions:
        if context.portfolio.positions[stock].amount != 0:
            position_last_list.append(stock)
    return position_last_list


# 保留小数点两位
def replace(x):
    x = Decimal(x)
    x = float(str(round(x, 2)))
    return x


# 按成交量筛选停牌的数据
def volume_filter(data):
    if data['volume'] > 0:
        return data
#####################################################
"""
策略名称：
猛犸策略
注意事项：
策略中调用的order_target接口的使用有场景限制，回测可以正常使用，交易谨慎使用。
回测场景下撮合是引擎计算的，因此成交之后持仓信息的更新是瞬时的，但交易场景下信息的更新依赖于柜台数据
的返回，无法做到瞬时同步，可能造成重复下单。详细原因请看帮助文档。
"""
import random


def initialize(context):
    # 交易标的列表（该股票池中的代码仅作为demo演示，非投资建议）
    context.universe = [
        '002131.SZ',
        '002736.SZ',
        '600804.SS',
        '000001.SZ',
        '600376.SS',
        '600104.SS',
        '000630.SZ',
        '002065.SZ',
        '601166.SS',
        '600875.SS',
        '000555.SZ',
        '601939.SS',
        '600999.SS',
    ]
    g.daycount = 0
    g.holdstocks = []


def handle_data(context, data):
    # 最大持仓股票支数
    maxhold = 5
    totalsize = len(context.universe)
    # 取得当前的现金
    cash = context.portfolio.cash
    g.daycount = g.daycount + 1

    if len(g.holdstocks) == 0:  # 初始状态
        count = maxhold
        singlemoney = cash / maxhold

        while count > 0:
            buystock = context.universe[random.randint(0, totalsize - 1)]
            if buystock not in g.holdstocks:
                g.holdstocks.append(buystock)
                # 用所有 singlemoney 买入股票
                log.info('buystock=' + buystock)
                log.info('singlemoney=' + str(singlemoney))
                order_value(buystock, singlemoney)
                # 记录这次买入
                # log.info("Buying %s" % (buystock))
                log.info("Buying %s" % buystock)
                count = count - 1
                log.info('count=' + str(count))

    elif g.daycount % 5 == 1:  # 5 days change

        log.info('g.daycount=' + str(g.daycount))
        # 选择过去7天表现最差的股票卖出
        weakstock = ''
        weak_returns = 10000
        his_data_info = get_history(7, '1d', field=['price', 'volume'], security_list=context.universe,
                                    fq='pre', include=False, is_dict=True)
        halt_status = get_stock_status(context.universe, 'HALT')
        for stock in g.holdstocks:
            his_data = his_data_info[stock]
            # 当日停牌跳过
            if halt_status[stock]:
                continue
            if his_data.size == 0:
                continue
            startprice = his_data['price'][0]
            endprice = his_data['price'][-1]

            cur_returns = endprice / startprice - 1
            # 遍历记录涨幅最小的股票
            if cur_returns < weak_returns:
                weak_returns = cur_returns
                weakstock = stock
        if weakstock == '':
            weakstock = g.holdstocks[0]
        sellstock = weakstock
        log.info('weakstock=' + weakstock)
        g.holdstocks.remove(weakstock)
        # 卖出所有股票,使这只股票的最终持有量为0
        order_target(sellstock, 0)
        # 记录这次卖出
        log.info("selling %s" % sellstock)

        while True:
            buystock = context.universe[random.randint(0, totalsize - 1)]
            if buystock not in g.holdstocks and buystock != sellstock:
                g.holdstocks.append(buystock)
                # 用所有 cash 买入股票
                log.info('buystock=' + buystock)
                log.info('cash=' + str(cash))
                order_value(buystock, cash)
                # 记录这次买入
                log.info("Buying %s" % buystock)
                break
#############################################
"""
策略名称：
协整配对策略
注意事项：
策略中调用的order_target、order_target_value接口的使用有场景限制，回测可以正常使用，交易谨慎使用。
回测场景下撮合是引擎计算的，因此成交之后持仓信息的更新是瞬时的，但交易场景下信息的更新依赖于柜台数据
的返回，无法做到瞬时同步，可能造成重复下单。详细原因请看帮助文档。
"""
import numpy as np


# 初始化函数，设定基准等等
def initialize(context):
    set_params()
    set_variables()
    set_backtest()


# ---代码块1. 设置参数
def set_params():
    # 股票1
    g.security1 = '601398.SS'
    # 股票2
    g.security2 = '601988.SS'
    # 基准
    g.benchmark = '601988.SS'
    # 回归系数
    g.regression_ratio = 0.9938
    # 股票1默认仓位
    g.p = 0.5
    # 股票2默认仓位
    g.q = 0.5
    # 算z-score天数
    g.test_days = 120
    # 
    g.days_count = 0
    # 
    g.benchmarkStart = 0
    #
    g.portfolioStart = 0


# ---代码块2. 设置变量
def set_variables():
    # 现在状态
    g.state = 'empty'


# ---代码块3. 设置回测
def set_backtest():
    # 设置基准
    set_benchmark(g.benchmark)


def before_trading_start(context, data):
    current_date = context.blotter.current_dt.strftime('%Y-%m-%d')
    # 2006-11-01前回测由于数据不足，不执行。
    if current_date < '2006-11-01':
        g.trade_flag = False
    else:
        g.trade_flag = True


# 每个单位时间(如果按天回测,则每天调用一次,如果按分钟,则每分钟调用一次)调用一次
def handle_data(context, data):
    if not g.trade_flag:
        return
    g.days_count += 1
    log.info('day:' + str(g.days_count))
    # z值检验流程
    # 获取两支股票历史价格
    prices1 = get_history(g.test_days, '1d', 'close', g.security1, is_dict=True)[g.security1]['close']
    prices2 = get_history(g.test_days, '1d', 'close', g.security2, is_dict=True)[g.security2]['close']

    # 根据回归比例算它们的平稳序列 a.X-Y,
    stable_series = g.regression_ratio * prices1 - prices2
    # 算均值
    series_mean = np.mean(stable_series)
    # 算标准差
    sigma = np.std(stable_series)
    # 算序列现值离均值差距多少
    diff = stable_series[-1] - series_mean
    # 返回z值
    z_score = diff / sigma
    # log.info('z_score='+str(z_score))
    new_state = get_signal(z_score)
    # log.info(new_state)
    # 调仓
    change_positions(new_state, context)


# ---代码块5.获取信号
# 返回新的状态，是一个string
def get_signal(z_score):
    if z_score > 1:
        # 状态为全仓第二支
        return 'buy2'
    # 如果小于负标准差
    if z_score < -1:
        # 状态为全仓第一支
        return 'buy1'
    # 如果在正负标准差之间
    if -1 <= z_score <= 1:
        # 如果差大于0
        if z_score >= 0:
            # 在均值上面
            return 'side1'
        # 反之
        else:
            # 在均值下面
            return 'side2'


# ---代码块6.根据信号调换仓位
# 输入是目标状态，输入为一个string
def change_positions(new_state, context):
    # 总值产价值
    total_value = context.portfolio.portfolio_value
    # 如果新状态是全仓股票1
    if new_state == 'buy1':
        # 全卖股票2
        order_target(g.security2, 0)
        # 全买股票1
        order_value(g.security1, total_value)
        # 旧状态更改
        g.state = 'buy1'
    # 如果新状态是全仓股票2
    if new_state == 'buy2':
        # 全卖股票1
        order_target(g.security1, 0)
        # 全买股票2
        order_value(g.security2, total_value)
        # 旧状态更改
        g.state = 'buy2'
    # 如果处于全仓一股票状态，但是z-score交叉0点
    if (g.state == 'buy1' and new_state == 'side1') or (g.state == 'buy2' and new_state == 'side2'):
        # 按照p,q值将股票仓位调整为默认值
        order_target_value(g.security1, g.p * total_value)
        order_target_value(g.security2, g.q * total_value)
        # 代码里重复两遍因为要先卖后买，而我们没有特地确定哪个先哪个后
        order_target_value(g.security1, g.p * total_value)
        order_target_value(g.security2, g.q * total_value)
        # 状态改为‘平’
        g.state = 'even'
################################################
"""
策略名称：
双均线策略
注意事项：
策略中调用的order_target接口的使用有场景限制，回测可以正常使用，交易谨慎使用。
回测场景下撮合是引擎计算的，因此成交之后持仓信息的更新是瞬时的，但交易场景下信息的更新依赖于柜台数据
的返回，无法做到瞬时同步，可能造成重复下单。详细原因请看帮助文档。
"""
import numpy as np


def initialize(context):
    # 初始化此策略
    g.security = '600570.SS'


def before_trading_start(context, data):
    h = get_history(20, '1d', field=['close', 'volume'], security_list=g.security,
                    fq='dypre', include=False, is_dict=True)
    g.close_data = h[g.security]['close']


# 当五日均线高于十日均线时买入，当五日均线低于十日均线时卖出
def handle_data(context, data):
    # 获取历史日K线数据
    current_price = data[g.security].close
    # 合成最新K线序列
    close_data = np.concatenate((g.close_data, np.array(list([current_price]))), axis=0)
    # 获取5日、10日均线
    ma5 = get_ma(close_data, 5)
    ma10 = get_ma(close_data, 10)
    # 得到当前资金余额
    cash = context.portfolio.cash
    # 如果当前有余额，并且五日均线大于十日均线
    if ma5 > ma10 and get_position(g.security).amount == 0:
        # 用所有 cash 买入股票
        order_value(g.security, cash)
        # 记录这次买入
        log.info("Buying %s" % g.security)

    # 如果五日均线小于十日均线，并且目前有头寸
    elif ma5 < ma10 and get_position(g.security).enable_amount > 0:
        # 全部卖出
        order_target(g.security, 0)
        # 记录这次卖出
        log.info("Selling %s" % g.security)


# 获取MA函数
def get_ma(close_array, num):
    ma = close_array[-num:].mean()
    return round(ma, 2)
####################################################
"""
策略名称：
单标的日内交易策略
运行周期:
分钟
策略流程：
盘中10点后每隔5分钟进行一次RSI短周期与长周期多空共振的判断，决定做正T还是反T；
盘中再按照盈利比例进行头寸恢复或者收盘前清算头寸恢复
注意事项：
策略中调用的order_target接口的使用有场景限制，回测可以正常使用，交易谨慎使用。
回测场景下撮合是引擎计算的，因此成交之后持仓信息的更新是瞬时的，但交易场景下信息的更新依赖于柜台数据
的返回，无法做到瞬时同步，可能造成重复下单。详细原因请看帮助文档。
"""
# 导入函数库

import numpy as np


# 初始化此策略
def initialize(context):
    # 设置我们要操作的股票池, 这里我们只操作一支股票
    g.ini_buy_flag = False  # 买底仓开关
    g.amount = 100  # 1份标准交易头寸
    g.rate = 1  # 做T涨跌幅，1就是1%
    g.L = 50  # 长周期RSI阈值
    g.S = 80  # 短周期RSI阈值
    g.security = '510500.SS'
    if not is_trade():
        set_limit_mode('UNLIMITED')


# 盘前处理
def before_trading_start(context, data):
    g.B_T_flag = False  # 做正T开关（先买后卖）
    g.S_T_flag = False  # 做反T开关（先卖后买）
    g.first_buy_flag = False
    g.second_buy_flag = False
    g.handle_data_flag = True
    current_date = context.blotter.current_dt.strftime('%Y-%m-%d')
    # 2013-04-01前510500.SS回测由于数据不足，不执行。可按照标的更改允许回测时间
    if current_date < '2013-04-01':
        g.trade_flag = False
    else:
        g.trade_flag = True


# 盘中处理
def handle_data(context, data):
    if not g.trade_flag:
        return
    # 盘中交易开关（一天只做一次T）
    if not g.handle_data_flag:
        return
    k_num = get_current_kline_count()
    if not g.ini_buy_flag:
        order(g.security, g.amount)
        g.ini_buy_flag = True
        g.handle_data_flag = False
    if k_num <= 30:
        return
    # 每个5分钟整点进行做T判断
    if k_num % 5 == 0:
        # 获取5分钟K线数据
        h = get_history(100, '5m', field=['close', 'volume'], security_list=g.security,
                        fq='dypre', include=True, is_dict=True)
        close_array_5m = h[g.security]['close']
        # 合成15分钟K线数据
        h = get_history(100, '15m', field=['close', 'volume'], security_list=g.security,
                        fq='dypre', include=False, is_dict=True)
        close_array_15m = h[g.security]['close']
        current_price = data[g.security].close
        close_array_15m = np.concatenate((close_array_15m, np.array(list([current_price]))), axis=0)
        if close_array_5m.ndim != 0 and close_array_15m.ndim != 0:
            # 获取5分钟、15分钟RSI
            rsi_5m = get_rsi(close_array_5m, 11)[-1]
            rsi_15m = get_rsi(close_array_15m, 11)[-1]
            # 做T条件判断
            if rsi_15m > g.L and rsi_5m > g.S:
                if get_position(g.security).enable_amount == g.amount and not g.B_T_flag:
                    order_id = order(g.security, g.amount)
                    if order_id is not None:
                        log.info('日内看多做正T')
                        g.B_T_flag = True
                        g.B_T_cost = data[g.security].price
            if rsi_15m < 100 - g.L and rsi_5m < 100 - g.S:
                if get_position(g.security).enable_amount == g.amount and not g.S_T_flag:
                    order_id = order(g.security, -g.amount)
                    if order_id is not None:
                        log.info('日内看空做反T')
                        g.S_T_flag = True
                        g.S_T_cost = data[g.security].price
    if g.B_T_flag:
        if data[g.security].price >= g.B_T_cost * (1 + g.rate / 100):
            order_id = order(g.security, -g.amount)
            if order_id is not None:
                log.info('做正T后恢复头寸')
                g.B_T_flag = False
    if g.S_T_flag:
        if data[g.security].price <= g.S_T_cost * (1 - g.rate / 100):
            order_id = order(g.security, g.amount)
            if order_id is not None:
                log.info('做反T后恢复头寸')
                g.S_T_flag = False
    # 收盘前多次尝试将持仓恢复到开盘持有量
    if k_num >= 238:
        log.info('收盘前多次尝试将持仓恢复到开盘持有量')
        order_id = order_target(g.security, g.amount)
        if order_id is not None:
            log.info('收盘清算')


# 获取RSI数据
def get_rsi(array_list, periods=14):
    length = len(array_list)
    rsi_values = [np.nan] * length
    if length <= periods:
        return rsi_values
    up_avg = 0
    down_avg = 0

    first_t = array_list[:periods + 1]
    for i in range(1, len(first_t)):
        if first_t[i] >= first_t[i - 1]:
            up_avg += first_t[i] - first_t[i - 1]
        else:
            down_avg += first_t[i - 1] - first_t[i]
    up_avg = up_avg / periods
    down_avg = down_avg / periods
    rs = up_avg / down_avg
    rsi_values[periods] = 100 - 100 / (1 + rs)

    for j in range(periods + 1, length):
        if array_list[j] >= array_list[j - 1]:
            up = array_list[j] - array_list[j - 1]
            down = 0
        else:
            up = 0
            down = array_list[j - 1] - array_list[j]
        up_avg = (up_avg * (periods - 1) + up) / periods
        down_avg = (down_avg * (periods - 1) + down) / periods
        rs = up_avg / down_avg
        rsi_values[j] = 100 - 100 / (1 + rs)
    return rsi_values
##############################################
# ============================================================
# 双动量ETF轮动策略 — PTrade 版本
# 策略逻辑：
#   1. 绝对动量过滤：只选过去N日收益 > 0 的ETF
#   2. 相对动量排序：N日动量加权得分排名
#   3. 波动率加权：根据近期波动率调整仓位
#   4. ATR跟踪止损 + 冷却期风控
#   5. 防御模式：全部过滤时切换防御型ETF或空仓
# ============================================================
# 【回测设置】
#   频率：分钟级别
#   起始时间：自定义
#   基准：510300.SS (沪深300ETF)
#   成交比例：建议 ≥ 0.5（回测撮合设置）
# ============================================================

import numpy as np
import math
import pandas as pd
from datetime import datetime, date, timedelta

# ==================== 策略参数 ====================
class Params:
    # ── 基础配置 ──
    CAPITAL_RATIO = 1.00              # 资金隔离比例（总资产×10%）
    HOLDINGS_NUM = 2                   # 持仓ETF数量
    MOMENTUM_LOOKBACK = 20             # 动量回看天数
    SHORT_LOOKBACK = 5                 # 短期动量回看天数
    VOL_LOOKBACK = 20                  # 波动率计算回看天数

    # ── 绝对动量门槛 ──
    ABS_MOM_MIN_RETURN = -0.05          # 过去N日收益率阈值（-0.05=允许轻微回撤，只排除暴跌ETF）

    #     ── 排名加权 ──
    # 综合得分 = 年化收益 × R²（与七星高照相同的加权对数回归动量评分）
    VOL_PENALTY_WEIGHT = 0.0           # 波动惩罚权重（0=关闭，匹配七星高照纯动量评分）

    # ── 风控 ──
    MIN_MONEY = 5000                   # 最小交易金额
    USE_TRAILING_STOP = True           # 启用跟踪止损
    TRAILING_STOP_ATR_MULT = 3.0       # 止损线 = 最高价 - N倍ATR
    ATR_PERIOD = 14                    # ATR计算周期
    COOLDOWN_DAYS = 3                  # 止损后冷却天数

    # ── 成交量过滤 ──
    ENABLE_VOLUME_FILTER = True        # 启用成交量过滤
    VOLUME_RATIO_THRESHOLD = 4.0       # 当日量/均值量 < 阈值（放宽，只排除极端放量）

    # ── 防御模式 ──
    DEFENSIVE_ETF = "511880.SS"        # 银华日利（货币ETF）
    SAFE_HAVEN_ETF = "511010.SS"       # 国债ETF

    # ── 基准 ──
    BENCHMARK = "510300.SS"            # 沪深300ETF


# ==================== 候选ETF池 ====================
ETF_POOL = [
    # ── A股宽基 ──
    "510300.SS",   # 沪深300ETF
    "510500.SS",   # 中证500ETF
    "510050.SS",   # 上证50ETF
    "159915.SZ",   # 创业板ETF
    "588080.SS",   # 科创板50ETF
    "512100.SS",   # 中证1000ETF
    "563300.SS",   # 中证2000ETF

    # ── 行业/风格ETF ──
    "512890.SS",   # 红利低波ETF
    "512040.SS",   # 国信价值ETF

    # ── 跨境ETF ──
    "513100.SS",   # 纳指ETF
    "159509.SZ",   # 纳指科技ETF
    "513500.SS",   # 标普500ETF
    "513030.SS",   # 德国ETF
    "513520.SS",   # 日经ETF
    "513310.SS",   # 中韩芯片ETF

    # ── 港股ETF ──
    "513130.SS",   # 恒生科技ETF
    "159920.SZ",   # 恒生ETF
    "513690.SS",   # 恒生高股息ETF

    # ── 商品ETF ──
    "518880.SS",   # 黄金ETF
    "159985.SZ",   # 豆粕ETF
    "159981.SZ",   # 能源化工ETF

    # ── 债券/防御ETF ──
    "511010.SS",   # 国债ETF
    "511220.SS",   # 城投债ETF
    "511380.SS",   # 可转债ETF
    "511880.SS",   # 银华日利
]


# ==================== 初始化函数 ====================
def initialize(context):
    """策略初始化"""
    # ── 资金隔离 ──
    g.capital_allocation_ratio = Params.CAPITAL_RATIO
    g.my_positions = {}                       # 自有持仓账本 {code: {amount, total_cost, cost_basis, entry_date}}
    g.etf_name_memory = {}                    # ETF名称缓存
    g.__initialized = False                   # 防止重复初始化

    # ── 回测专用 ──
    if not is_trade():
        set_slippage(slippage=0.0001)
        set_commission(commission_ratio=0.0001, min_commission=5.0, type="ETF")

    set_benchmark(Params.BENCHMARK)

    # ── 状态变量 ──
    g.target_etfs = []                        # 今日目标ETF列表
    g.cooldown_end_date = None                # 冷却期结束日
    g.position_highs = {}                     # 持仓最高价（ATR跟踪用）
    g.atr_cache = {}                          # ATR日缓存
    g.last_ranked_date = None                 # 上次排名日期

    # ── 设置股票池 ──
    all_etfs = list(set(ETF_POOL))
    set_universe(all_etfs)

    # ── 定时任务 ──
    run_daily(context, check_positions, time='09:10')           # 盘前同步+日志
    run_daily(context, etf_sell_trade, time='10:30')            # 卖出（早盘稳定后）

    # 分钟级风控（10:00~14:30 每隔一段时间检查）
    for t in ['10:00', '11:00', '13:15', '14:00', '14:30']:
        run_daily(context, trailing_stop_check, time=t)

    log.info("=" * 60)
    log.info("双动量ETF轮动策略 初始化完成")
    log.info(f"持仓数量: {Params.HOLDINGS_NUM}只, 动量回看: {Params.MOMENTUM_LOOKBACK}天")
    log.info(f"资金比例: {Params.CAPITAL_RATIO*100:.0f}%, 止损: {'开启' if Params.USE_TRAILING_STOP else '关闭'}")
    log.info(f"防御ETF: {Params.DEFENSIVE_ETF}, 避险ETF: {Params.SAFE_HAVEN_ETF}")
    log.info("=" * 60)


# ==================== 行情工具函数 ====================
def get_etf_name(security):
    """获取ETF名称（带缓存）"""
    try:
        if security in g.etf_name_memory:
            return g.etf_name_memory[security]
        names = get_stock_name(security)
        name = names.get(security, security) if isinstance(names, dict) else security
        g.etf_name_memory[security] = name
        return name
    except:
        return security


def get_current_price(context, security):
    """获取当前价格（回测用get_history，实盘用get_snapshot）"""
    try:
        if is_trade():
            snapshot = get_snapshot(security)
            if snapshot and security in snapshot:
                price = snapshot[security].get('last_px', 0)
                if price and price > 0:
                    return float(price), True
            return 0, False
        else:
            hist = get_history(1, '1d', 'close', security_list=security, fq='pre', include=True)
            if hist is not None and len(hist) > 0:
                price = hist['close'].values[-1]
                if price > 0:
                    return float(price), True
            return 0, False
    except Exception as e:
        log.warning(f"获取{security}当前价格失败: {e}")
        return 0, False


def is_paused(context, security):
    """判断是否停牌"""
    try:
        # 优先用成交量判断（回测/实盘均兼容）
        hist = get_history(1, '1d', 'volume', security_list=security, fq='pre', include=True)
        if hist is not None and len(hist) > 0:
            vol = hist['volume'].values[-1]
            if vol == 0 or str(vol) == 'nan':
                return True
        # 实盘用快照辅助
        if is_trade():
            snapshot = get_snapshot(security)
            if snapshot and security in snapshot:
                status = snapshot[security].get('trade_status', 'TRADE')
                return status in ['HALT', 'SUSP', 'STOPT']
        return False
    except:
        return False


def get_extreme_limits(context, security):
    """获取涨跌停价"""
    try:
        if is_trade():
            ss = get_snapshot(security)
            if ss and security in ss:
                return ss[security].get('up_px', 0), ss[security].get('down_px', 0), True
        else:
            hist = get_history(1, '1d', ['high_limit', 'low_limit'], security_list=security,
                               fq='pre', include=True)
            if hist is not None and len(hist) > 0:
                return (hist['high_limit'].values[-1] if 'high_limit' in hist.columns else 0,
                        hist['low_limit'].values[-1] if 'low_limit' in hist.columns else 0, True)
        return 0, 0, False
    except:
        return 0, 0, False


# ==================== 动量计算引擎 ====================
def calc_momentum_score(price_series):
    """
    计算动量综合得分：
    score = 年化收益 × R² × (1 - vol_penalty)
    用加权对数回归拟合趋势线，R²衡量趋势可信度
    """
    n = len(price_series)
    if n < 5:
        return 0, 0, 0, 0

    log_prices = np.log(price_series)
    x = np.arange(n)
    weights = np.linspace(0.5, 1.5, n)  # 近期权重更高

    # 加权线性回归
    w_sum = np.sum(weights)
    wx_mean = np.sum(weights * x) / w_sum
    wy_mean = np.sum(weights * log_prices) / w_sum
    numerator = np.sum(weights * (x - wx_mean) * (log_prices - wy_mean))
    denominator = np.sum(weights * (x - wx_mean) ** 2)
    slope = numerator / denominator if denominator != 0 else 0
    intercept = wy_mean - slope * wx_mean

    # 年化收益
    ann_return = math.exp(slope * 250) - 1

    # R²
    y_pred = slope * x + intercept
    ss_res = np.sum(weights * (log_prices - y_pred) ** 2)
    ss_tot = np.sum(weights * (log_prices - np.average(log_prices, weights=weights)) ** 2)
    r_sq = 1 - ss_res / ss_tot if ss_tot > 0 else 0

    # 波动率
    daily_returns = np.diff(log_prices)
    annual_vol = np.std(daily_returns) * math.sqrt(250) if len(daily_returns) > 1 else 1

    # 综合得分
    vol_penalty = 1.0 / (1.0 + Params.VOL_PENALTY_WEIGHT * annual_vol)
    score = ann_return * max(r_sq, 0) * vol_penalty

    return score, ann_return, r_sq, annual_vol


def get_atr(security, period, context):
    """计算ATR（Average True Range）"""
    try:
        hist = get_history(period + 1, '1d', ['high', 'low', 'close'],
                           security_list=security, fq='pre', include=False)
        if hist is None or len(hist) < period + 1:
            return 0, False

        h = hist['high'].values
        l = hist['low'].values
        c = hist['close'].values

        tr = np.zeros(len(h))
        for i in range(1, len(h)):
            tr[i] = max(h[i] - l[i], abs(h[i] - c[i-1]), abs(l[i] - c[i-1]))

        atr = np.mean(tr[-period:])
        return float(atr), True
    except Exception as e:
        log.debug(f"ATR计算失败 {security}: {e}")
        return 0, False


def get_today_volume(context, security):
    """获取今日成交量"""
    try:
        if is_trade():
            kv = get_history(240, '1m', 'volume', security_list=security, fq='pre', include=False)
            return kv['volume'].sum() if kv is not None and not kv.empty else 0
        else:
            kv = get_history(1, '1d', 'volume', security_list=security, fq='pre', include=True)
            return kv['volume'].values[-1] if kv is not None and not kv.empty else 0
    except:
        return 0


# ==================== ETF排名与筛选 ====================
def rank_etfs(context):
    """对ETF池进行双动量排名"""
    pool = list(ETF_POOL)
    today = context.current_dt.date()

    # 停牌过滤
    active = [e for e in pool if not is_paused(context, e)]
    if not active:
        log.info("今日无可交易ETF")
        return []

    # 批量获取历史数据
    lookback = max(Params.MOMENTUM_LOOKBACK, Params.VOL_LOOKBACK, Params.ATR_PERIOD) + 10
    try:
        bulk_hist = get_history(lookback, '1d',
                                ['close', 'high', 'low', 'volume'],
                                security_list=active, fq='pre', include=False)
    except Exception as e:
        log.warning(f"批量获取历史数据失败: {e}")
        return []

    if bulk_hist is None or bulk_hist.empty:
        return []

    # 逐个计算排名分
    ranked = []
    for etf in active:
        try:
            name = get_etf_name(etf)
            price, ok = get_current_price(context, etf)
            if not ok or price <= 0:
                log.debug(f"{etf} {name} 无有效价格，跳过")
                continue

            # 提取该ETF的历史数据
            if 'code' in bulk_hist.columns:
                phist = bulk_hist[bulk_hist['code'] == etf]
            else:
                phist = bulk_hist

            if phist is None or len(phist) < Params.MOMENTUM_LOOKBACK:
                log.debug(f"{etf} {name} 数据不足{Params.MOMENTUM_LOOKBACK}天，跳过")
                continue

            close_arr = np.array(phist['close'].values[-Params.MOMENTUM_LOOKBACK-1:])
            close_arr = np.append(close_arr, price)

            # ── 绝对动量过滤 ──
            abs_return = close_arr[-1] / close_arr[-Params.MOMENTUM_LOOKBACK-1] - 1
            if abs_return <= Params.ABS_MOM_MIN_RETURN:
                log.debug(f"{etf} {name} 绝对动量 {abs_return*100:.1f}% ≤ {Params.ABS_MOM_MIN_RETURN*100:.0f}%，过滤")
                continue

            # ── 短期动量 ──
            if len(close_arr) >= Params.SHORT_LOOKBACK + 1:
                short_ret = close_arr[-1] / close_arr[-(Params.SHORT_LOOKBACK+1)] - 1
            else:
                short_ret = 0

            # ── 成交量过滤 ──
            if Params.ENABLE_VOLUME_FILTER:
                avg_vol = np.mean(phist['volume'].values[-20:]) if len(phist) >= 20 else 0
                today_vol = get_today_volume(context, etf)
                if avg_vol > 0 and today_vol > 0:
                    vol_ratio = today_vol / avg_vol
                    if vol_ratio > Params.VOLUME_RATIO_THRESHOLD:
                        log.debug(f"{etf} {name} 放量{vol_ratio:.1f}倍>{Params.VOLUME_RATIO_THRESHOLD}，过滤")
                        continue

            # ── 综合得分 ──
            score, ann_ret, r_sq, vol = calc_momentum_score(close_arr)

            ranked.append({
                'etf': etf,
                'name': name,
                'score': score,
                'ann_ret': ann_ret,
                'r_squared': r_sq,
                'volatility': vol,
                'short_ret': short_ret,
                'price': price,
            })
        except Exception as e:
            log.debug(f"计算{etf}排名出错: {e}")
            continue

    # 按得分降序排序
    ranked.sort(key=lambda x: x['score'], reverse=True)
    return ranked


# ==================== 风控模块 ====================
def is_in_cooldown(context):
    """是否处于冷却期"""
    if g.cooldown_end_date is None:
        return False
    return context.current_dt.date() < g.cooldown_end_date


def enter_cooldown(context, reason):
    """进入冷却期"""
    g.cooldown_end_date = context.current_dt.date() + timedelta(days=Params.COOLDOWN_DAYS)
    log.info(f"⛔ 进入冷却期（{reason}），持续到 {g.cooldown_end_date}")


def exit_cooldown_if_ended(context):
    """如果冷却期结束则退出"""
    if g.cooldown_end_date and context.current_dt.date() >= g.cooldown_end_date:
        g.cooldown_end_date = None
        g.position_highs = {}
        log.info("✅ 冷却期结束，恢复交易")


def trailing_stop_check(context):
    """ATR跟踪止损检查（分钟级）"""
    if not Params.USE_TRAILING_STOP:
        return
    if is_in_cooldown(context):
        return

    for sec in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions.get(sec, None)
        if not pos or pos.amount <= 0:
            continue
        # 防御ETF不止损
        if sec in [Params.DEFENSIVE_ETF, Params.SAFE_HAVEN_ETF]:
            continue

        current_price, ok = get_current_price(context, sec)
        if not ok or current_price <= 0:
            continue

        # 计算ATR
        atr, ok_atr = get_atr(sec, Params.ATR_PERIOD, context)
        if not ok_atr or atr <= 0:
            continue

        # 更新最高价
        if sec not in g.position_highs:
            g.position_highs[sec] = current_price
        else:
            g.position_highs[sec] = max(g.position_highs[sec], current_price)

        # 止损线
        stop_price = g.position_highs[sec] - Params.TRAILING_STOP_ATR_MULT * atr

        if current_price <= stop_price:
            name = get_etf_name(sec)
            log.info(f"🛑 ATR跟踪止损: {sec} {name}, "
                     f"当前价{current_price:.3f} ≤ 止损价{stop_price:.3f}, "
                     f"最高{g.position_highs[sec]:.3f}, ATR={atr:.4f}")
            if smart_order(sec, 0, context):
                g.position_highs.pop(sec, None)
                enter_cooldown(context, f"{name} ATR跟踪止损")


# ==================== 资金隔离工具 ====================
def get_my_capital(context):
    """本策略可用资金 = 总资产 × 分配比例"""
    return context.portfolio.portfolio_value * g.capital_allocation_ratio


def sync_my_ledger(context):
    """每日同步账本与真实持仓，修正前日回测/撮合偏差"""
    ledger = g.my_positions
    pool_set = set(ETF_POOL)

    # 以真实持仓覆盖账本
    for sec in context.portfolio.positions:
        pos = context.portfolio.positions[sec]
        if sec not in pool_set or pos.amount <= 0:
            continue
        cost = getattr(pos, 'cost_basis', 0) or getattr(pos, 'avg_cost', 0) or 0
        if cost <= 0:
            p, ok = get_current_price(context, sec)
            if ok and p > 0:
                cost = p
        if cost <= 0:
            cost = 0.0001
        ledger[sec] = {
            'amount': int(pos.amount),
            'total_cost': round(int(pos.amount) * cost, 2),
            'cost_basis': round(cost, 4),
            'entry_date': context.current_dt.strftime('%Y-%m-%d'),
        }

    # 删除真实持仓中已不存在的
    for sec in list(ledger.keys()):
        if sec not in pool_set:
            continue
        pos = context.portfolio.positions.get(sec, None)
        if pos is None or pos.amount <= 0:
            del ledger[sec]


def update_my_ledger(context, code, amount, price):
    """更新自有账本"""
    ledger = g.my_positions
    if amount > 0:  # 买入
        if code in ledger:
            old = ledger[code]
            new_amt = old['amount'] + amount
            new_cost = old['total_cost'] + amount * price
            old['amount'] = new_amt
            old['total_cost'] = new_cost
            old['cost_basis'] = round(new_cost / new_amt, 4)
        else:
            ledger[code] = {
                'amount': amount,
                'total_cost': round(amount * price, 2),
                'cost_basis': round(price, 4),
                'entry_date': context.current_dt.strftime('%Y-%m-%d'),
            }
    else:  # 卖出
        sell_amt = abs(amount)
        if code in ledger:
            entry = ledger[code]
            entry['total_cost'] -= sell_amt * entry['cost_basis']
            entry['amount'] -= sell_amt
            if entry['amount'] <= 0:
                del ledger[code]


# ==================== 智能下单函数 ====================
def smart_order(security, target_value, context):
    """
    智能下单：停牌/涨跌停/最小金额/T+1保护，使用限价单
    返回 True 如果下单成功
    """
    try:
        name = get_etf_name(security)

        if is_paused(context, security):
            log.debug(f"{security} {name} 停牌，跳过")
            return False

        price, ok = get_current_price(context, security)
        if not ok or price <= 0:
            return False

        high_lim, low_lim, _ = get_extreme_limits(context, security)

        target_amount = int(target_value / price)
        target_amount = (target_amount // 100) * 100
        if target_amount <= 0 and target_value > 0:
            target_amount = 100  # 至少买1手

        # 使用自有账本判断当前持仓量，避免回测实际持仓延迟导致 diff 计算错误
        ledger_amt = g.my_positions.get(security, {}).get('amount', 0)
        cur_pos = context.portfolio.positions.get(security, None)
        cur_amount = ledger_amt
        diff = target_amount - cur_amount

        # 涨停不买 / 跌停不卖
        if diff > 0 and high_lim > 0 and price >= high_lim:
            log.debug(f"{security} {name} 涨停，跳过买入")
            return False
        if diff < 0 and low_lim > 0 and price <= low_lim:
            log.debug(f"{security} {name} 跌停，跳过卖出")
            return False

        # 最小金额检查（仅买入）
        trade_val = abs(diff) * price
        if diff > 0 and 0 < trade_val < Params.MIN_MONEY:
            log.debug(f"{security} {name} 买入金额{trade_val:.0f}<{Params.MIN_MONEY}，跳过")
            return False

        # T+1 可卖数量限制
        if diff < 0 and cur_pos:
            closeable = int(cur_pos.enable_amount)
            if closeable == 0:
                log.debug(f"{security} {name} 今日买入不可卖")
                return False
            diff = -min(abs(diff), closeable)

        if diff == 0:
            return False

        limit_price = round(price, 3)

        # 记录下单前持仓
        before_amt = int(cur_pos.amount) if cur_pos else 0

        order_id = order(security, diff, limit_price=limit_price)
        if not order_id:
            log.warning(f"下单失败: {security} {name} 数量{diff}")
            return False

        # 获取实际成交数量
        actual_filled = None
        try:
            order_info = get_order(order_id)
            if order_info and len(order_info) > 0:
                o = order_info[0]
                actual_filled = int(o.filled if hasattr(o, 'filled') else o.get('filled', 0))
        except:
            pass

        # get_order失败时用持仓变化估算
        if actual_filled is None or actual_filled <= 0:
            try:
                after_pos = context.portfolio.positions.get(security, None)
                after_amt = int(after_pos.amount) if after_pos else 0
                actual_filled = abs(after_amt - before_amt)
            except:
                pass

        # 回测撮合延迟：get_order 和持仓变化都返回0时，乐观假设订单将被撮合
        # 避免账本因撮合延迟而持续失真（盘前 sync_my_ledger 会修正残留偏差）
        optimistic = False
        if actual_filled is None or actual_filled <= 0:
            actual_filled = abs(diff)
            optimistic = True

        # 更新账本
        actual_amount = actual_filled if diff > 0 else -actual_filled
        if actual_filled > 0:
            update_my_ledger(context, security, actual_amount, price)
            if diff > 0:
                tag = "预估成交" if optimistic else "成交"
                log.info(f"📥 买入 {security} {name} 委托{diff} {tag}{actual_filled} 价格{price:.3f}")
                g.position_highs[security] = price
            else:
                tag = "预估成交" if optimistic else "成交"
                log.info(f"📤 卖出 {security} {name} 委托{-diff} {tag}{actual_filled} 价格{price:.3f}")
        else:
            log.info(f"⚠️ {security} {name} 订单未成交")

        return True

    except Exception as e:
        log.warning(f"智能下单 {security} 出错: {e}")
        return False


# ==================== 交易逻辑 ====================
def check_positions(context):
    """盘前：同步账本 + 日志"""
    sync_my_ledger(context)

    for sec in context.portfolio.positions:
        pos = context.portfolio.positions[sec]
        if pos.amount > 0:
            name = get_etf_name(sec)
            cp, _ = get_current_price(context, sec)
            pnl_pct = (cp / pos.cost_basis - 1) * 100 if pos.cost_basis > 0 else 0
            log.info(f"📊 {sec} {name}: 持仓{pos.amount}股, "
                     f"成本{pos.cost_basis:.3f}, 现价{cp:.3f}, 盈亏{pnl_pct:+.2f}%")


def etf_sell_trade(context):
    """卖出不在目标名单的持仓"""
    log.info("=" * 40)
    log.info("【卖出阶段】")

    exit_cooldown_if_ended(context)

    if is_in_cooldown(context):
        log.info(f"冷却期中，跳过卖出，冷却至 {g.cooldown_end_date}")
        # 冷却期也清仓（只留防御ETF）
        for sec in list(context.portfolio.positions.keys()):
            if sec not in [Params.DEFENSIVE_ETF, Params.SAFE_HAVEN_ETF]:
                smart_order(sec, 0, context)
        log.info("=" * 40)
        return

    # 获取排名
    ranked = rank_etfs(context)

    # 确定目标ETF
    target_list = []
    for r in ranked[:Params.HOLDINGS_NUM]:
        target_list.append(r['etf'])

    # 无目标时切防御
    if not target_list:
        log.info("无符合条件的ETF，切换防御模式")
        target_list = [Params.DEFENSIVE_ETF]

    g.target_etfs = target_list
    target_set = set(target_list)

    log.info(f"今日目标ETF: {[f'{e} {get_etf_name(e)}' for e in target_list]}")

    # 卖出不在目标中的持仓
    for sec in list(context.portfolio.positions.keys()):
        if sec not in target_set:
            pos = context.portfolio.positions.get(sec, None)
            if pos and pos.amount > 0:
                if smart_order(sec, 0, context):
                    log.info(f"📤 清仓(不在目标): {sec} {get_etf_name(sec)}")

    log.info("=" * 40)

    # 同时进行买入（卖和买同一时间，等待下一分钟买入执行）
    # 这里采用 sell -> buy_next_minute 模式（需要两个 run_daily）
    # 为简化，直接在卖出后立即买入
    etf_buy_execute(context)


def etf_buy_execute(context):
    """买入执行逻辑"""
    log.info("【买入阶段】")

    if is_in_cooldown(context):
        log.info("冷却期中，不买入")
        log.info("=" * 40)
        return

    target_etfs = getattr(g, 'target_etfs', [])
    if not target_etfs:
        log.info("无目标ETF")
        log.info("=" * 40)
        return

    # 资金隔离
    my_cap = get_my_capital(context)

    # 计算账本已持仓市值
    held_val = 0.0
    for code, entry in list(g.my_positions.items()):
        if entry['amount'] > 0:
            p, ok = get_current_price(context, code)
            if ok:
                held_val += entry['amount'] * p

    remaining = my_cap - held_val
    if remaining < Params.MIN_MONEY:
        log.info(f"剩余配额 {remaining:.0f} < {Params.MIN_MONEY}，不买入")
        log.info("=" * 40)
        return

    # 等权分配
    need_buy = [e for e in target_etfs if e not in g.my_positions or g.my_positions[e]['amount'] == 0]
    if not need_buy:
        # 都在目标中，只调仓
        need_buy = target_etfs

    per_etf = remaining / max(len(need_buy), 1)

    log.info(f"资金配额: 总{my_cap:.0f}, 已持仓{held_val:.0f}, 剩余{remaining:.0f}, 每只{per_etf:.0f}")

    for etf in need_buy:
        # 计算当前持仓市值
        cur_val = 0
        if etf in g.my_positions and g.my_positions[etf]['amount'] > 0:
            cp, ok = get_current_price(context, etf)
            if ok:
                cur_val = g.my_positions[etf]['amount'] * cp

        target_val = per_etf + cur_val
        if abs(target_val - cur_val) < Params.MIN_MONEY:
            continue

        if smart_order(etf, target_val, context):
            log.info(f"📦 调仓: {etf} {get_etf_name(etf)} 目标市值{target_val:.0f}")

    log.info("=" * 40)


# ==================== 必需的 handle_data ====================
def handle_data(context, data):
    """PTrade必需函数，策略使用run_daily调度，此函数保持为空"""
    pass
##############################################################
# 七星高照ETF轮动策略-PTrade版本
# 原始策略来源：聚宽
# 转换说明：已适配PTrade平台API，支持回测和交易

import numpy as np
import math

def initialize(context):
    """
    初始化函数
    """
    # ==================== 实盘交易设置 ====================
    
    # 回测专用设置（仅在回测环境执行）
    if not is_trade():
        # 设置滑点（PTrade使用set_slippage）
        set_slippage(slippage=0.0002)
        
        # 设置交易成本：ETF交易成本较低
        set_commission(commission_ratio=0.0002, min_commission=5.0, type="ETF")
    
    log.info("增强版策略初始化完成！")
    
    # 设置参考基准（代码尾缀转换：XSHE改为SZ）
    set_benchmark("161226.SZ")
    
    # ==================== ETF池设置 ====================
    g.etf_pool = [
        # 大宗商品ETF（代码尾缀转换：XSHG改为SS，XSHE改为SZ）
        "518880.SS",  # 黄金ETF
        "159985.SZ",  # 豆粕ETF（跟踪豆粕期货价格）
        "501018.SS",  # 南方原油（投资原油相关资产）
        "161226.SZ",  # 白银LOF
        # 国际ETF
        "511010.SS",  # 国债
        "513100.SS",  # 纳指ETF
        # 中国ETF
        "159915.SZ",  # 创业板ETF
        # 债券ETF
        "511220.SS",  # 城投债ETF
    ]
    
    # 大ETF池（备用）
    g.etf_pool_bak = [
        # 大宗商品ETF
        "518880.SS",  # 黄金ETF
        "159980.SZ",  # 有色ETF（跟踪有色金属板块）
        "159985.SZ",  # 豆粕ETF（跟踪豆粕期货价格）
        "501018.SS",  # 南方原油（投资原油相关资产）
        "161226.SZ",  # 白银LOF
        "159981.SZ",  # 能源化工ETF
        # 国际ETF
        "513100.SS",  # 纳指ETF
        "159509.SZ",  # 纳指科技ETF
        "513290.SS",  # 纳指生物ETF
        "513500.SS",  # 标普500ETF
        "159529.SZ",  # 标普消费
        "513400.SS",  # 道琼斯ETF
        "513520.SS",  # 日经225ETF
        "513030.SS",  # 德国30ETF
        "513080.SS",  # 法国ETF
        "513310.SS",  # 中韩半导体ETF
        "513730.SS",  # 东南亚ETF
        # 香港ETF
        "159792.SZ",  # 港股互联ETF
        "513130.SS",  # 恒生科技
        "513050.SS",  # 中概互联网ETF
        "159920.SZ",  # 恒生ETF
        "513690.SS",  # 港股红利
        # 指数ETF
        "510300.SS",  # 沪深300ETF
        "510500.SS",  # 中证500ETF
        "510050.SS",  # 上证50ETF
        "510210.SS",  # 上证ETF
        "159915.SZ",  # 创业板ETF
        "588080.SS",  # 科创50
        "512100.SS",  # 中证1000ETF
        "563360.SS",  # A500-ETF
        "563300.SS",  # 中证2000ETF
        # 风格ETF
        "512890.SS",  # 红利低波ETF
        "159967.SZ",  # 创业板成长ETF
        "512040.SS",  # 价值ETF
        "159201.SZ",  # 自由现金流ETF
        # 债券ETF
        "511380.SS",  # 可转债ETF
        "511010.SS",  # 国债ETF
        "511220.SS",  # 城投债ETF
    ]
    
    # g.etf_pool = g.etf_pool_bak  # 启用完整大池
    
    # ==================== 核心策略参数 ====================
    # 动量计算参数
    g.lookback_days = 25  # 长期动量计算周期
    g.holdings_num = 1    # 持仓ETF数量
    g.defensive_etf = "511010.SS"  # 防御性ETF（货币ETF）
    g.min_money = 5000  # 最小交易金额
    g.max_order_amount = 1000000  # 单笔最大委托数量（券商限制，通常为100万股）
    
    # 风险控制参数
    g.stop_loss = 0.95    # 固定百分比止损线（下跌5%止损）
    g.loss = 0.97   # 近3日跌幅止损线
    
    # 得分阈值
    g.min_score_threshold = 0  # 最低得分阈值
    g.max_score_threshold = 500.0  # 最高得分阈值
    
    # ==================== 成交量过滤参数 ====================
    g.enable_volume_check = True  # 是否启用成交量过滤
    g.volume_lookback = 5  # 成交量历史参考天数
    g.volume_threshold = 2  # 放量阈值（大于设定值视为放量）
    g.volume_return_limit = 1  # 年化收益率过滤：当高于该值，则启用成交量过滤
    
    # ==================== 新增：均线过滤参数 ====================
    g.enable_ma_filter = False  # 是否启用均线过滤
    g.ma_filter_days = 20  # 均线过滤天数
    
    # ==================== 原有：短期动量过滤参数 ====================
    g.use_short_momentum_filter = True  # 是否启用短期动量过滤
    g.short_lookback_days = 10  # 短期动量计算周期
    g.short_momentum_threshold = 0.0  # 短期动量阈值
    
    # ==================== 原有：ATR动态止损参数 ====================
    g.use_atr_stop_loss = True  # 是否启用ATR动态止损
    g.atr_period = 14  # ATR计算周期
    g.atr_multiplier = 2  # ATR倍数
    g.atr_trailing_stop = False  # 是否使用跟踪止损
    g.atr_exclude_defensive = True  # 防御ETF是否豁免ATR止损
    
    # ==================== 原有：RSI过滤参数 ====================
    g.use_rsi_filter = True  # 是否启用RSI过滤
    g.rsi_period = 6  # RSI计算周期
    g.rsi_lookback_days = 1  # 检查RSI的历史天数
    g.rsi_threshold = 98  # RSI阈值
    
    # ==================== 持仓管理 ====================
    g.positions = {}  # 记录持仓
    g.position_highs = {}  # 记录持仓期间的最高价
    g.position_stop_prices = {}  # 记录持仓的ATR止损价
    
    # 设置股票池（将所有可能交易的ETF加入）
    all_etfs = list(set(g.etf_pool + [g.defensive_etf]))
    set_universe(all_etfs)
    
    # ==================== 交易调度 ====================
    # 每天开盘后检查持仓
    run_daily(context, check_positions, time='09:10')
    # 每天开盘后检查ATR动态止损
    run_daily(context, check_atr_stop_loss, time='10:31')
    # 执行卖出操作
    run_daily(context, etf_sell_trade, time='10:45')
    # 执行买入操作
    run_daily(context, etf_buy_trade, time='14:00')
    
    log.info("策略参数初始化完成:")
    log.info("- ETF池大小: %s 只ETF" % len(g.etf_pool))
    log.info("- 动量周期: %s 天" % g.lookback_days)
    log.info("- 持仓数量: %s 只" % g.holdings_num)
    log.info("- 成交量过滤: %s" % ("启用" if g.enable_volume_check else "禁用"))
    log.info("- 均线过滤: %s" % ("启用" if g.enable_ma_filter else "禁用"))
    log.info("- RSI过滤: %s" % ("启用" if g.use_rsi_filter else "禁用"))
    log.info("- ATR止损: %s" % ("启用" if g.use_atr_stop_loss else "禁用"))
    log.info("- 防御ETF: %s" % g.defensive_etf)

# ==================== 统一的价格获取函数 ====================
def get_current_price(context, security):
    """
    统一的价格获取函数，自动适配回测和交易环境
    返回：(当前价格, 是否成功)
    """
    try:
        if is_trade():
            # 交易环境使用get_snapshot
            snapshot = get_snapshot(security)
            if snapshot and security in snapshot:
                current_price = snapshot[security].get('last_px', 0)
                if current_price > 0:
                    return current_price, True
            return 0, False
        else:
            # 回测环境使用get_history，include=True包含当前周期
            hist = get_history(1, '1d', 'close', security_list=security, 
                            fq='pre', include=True)
            if hist is not None and len(hist) > 0:
                current_price = hist['close'].values[-1]
                if current_price > 0:
                    return current_price, True
            return 0, False
    except Exception as e:
        log.warning("获取%s当前价格失败: %s" % (security, str(e)))
        return 0, False

def get_current_prices_batch(context, securities):
    """
    批量获取多个标的的当前价格
    返回：字典 {security: price}
    """
    result = {}
    try:
        if is_trade():
            # 交易环境批量获取快照
            snapshot = get_snapshot(securities)
            if snapshot:
                for security in securities:
                    if security in snapshot:
                        price = snapshot[security].get('last_px', 0)
                        if price > 0:
                            result[security] = price
        else:
            # 回测环境批量获取历史数据
            hist = get_history(1, '1d', 'close', security_list=securities,
                            fq='pre', include=True)
            if hist is not None and len(hist) > 0:
                for security in securities:
                    try:
                        price_data = hist.query('code in ["%s"]' % security)['close']
                        if len(price_data) > 0:
                            price = price_data.values[-1]
                            if price > 0:
                                result[security] = price
                    except:
                        continue
        
        return result
    except Exception as e:
        log.warning("批量获取价格失败: %s" % str(e))
        return result

def get_trade_status(context, security):
    """
    获取标的交易状态
    返回：(状态字符串, 涨停价, 跌停价)
    """
    try:
        if is_trade():
            # 交易环境使用get_snapshot
            snapshot = get_snapshot(security)
            if snapshot and security in snapshot:
                info = snapshot[security]
                status = info.get('trade_status', 'TRADE')
                high_limit = info.get('up_px', 0)
                low_limit = info.get('down_px', 0)
                return status, high_limit, low_limit
            return 'UNKNOWN', 0, 0
        else:
            # 回测环境使用get_history获取涨跌停价
            hist = get_history(1, '1d', ['close', 'high_limit', 'low_limit'], 
                            security_list=security, fq='pre', include=True)
            if hist is not None and len(hist) > 0:
                close_price = hist['close'].values[-1]
                high_limit = hist['high_limit'].values[-1] if 'high_limit' in hist.columns else 0
                low_limit = hist['low_limit'].values[-1] if 'low_limit' in hist.columns else 0
                
                # 回测中默认认为可交易
                status = 'TRADE'
                
                # 检查是否停牌（成交量为0）
                vol_hist = get_history(1, '1d', 'volume', security_list=security,
                                    fq='pre', include=True)
                if vol_hist is not None and len(vol_hist) > 0:
                    volume = vol_hist['volume'].values[-1]
                    if volume == 0:
                        status = 'HALT'
                
                return status, high_limit, low_limit
            return 'UNKNOWN', 0, 0
    except Exception as e:
        log.warning("获取%s交易状态失败: %s" % (security, str(e)))
        return 'UNKNOWN', 0, 0

# ============ 持仓检查 ===============
def check_positions(context):
    """每日开盘后检查持仓状态"""
    try:
        positions = context.portfolio.positions
        if not positions:
            log.info("当前无持仓")
            return
        
        # 获取持仓列表
        position_list = list(positions.keys())
        
        for security in positions:
            position = positions[security]
            if position.amount > 0:
                security_name = get_stock_name(security).get(security, security)
                current_price = position.last_sale_price
                
                # 检查停牌状态
                trade_status, high_limit, low_limit = get_trade_status(context, security)
                if trade_status in ['HALT', 'SUSP', 'STOPT']:
                    log.info("警告 %s %s 今日停牌" % (security, security_name))
                
                log.info("持仓检查: %s %s, 数量: %s, 成本: %.3f, 当前价: %.3f" % 
                        (security, security_name, position.amount, position.cost_basis, current_price))
    except Exception as e:
        log.warning("检查持仓时出错: %s" % str(e))

# ==================== 卖出函数 ====================
def etf_sell_trade(context):
    """
    卖出函数
    功能：卖出不符合条件的持仓
    """
    log.info("========== 卖出操作开始 ==========")
    
    # 获取当前持仓
    current_positions = list(context.portfolio.positions.keys())
    
    # 如果没有持仓，直接返回
    if not current_positions:
        log.info("当前无持仓，无需卖出")
        return
    
    # 获取符合条件的ETF排名
    ranked_etfs = get_ranked_etfs(context)
    
    # ========== 构建目标ETF列表（最多g.holdings_num只） ==========
    target_etfs = []
    for metrics in ranked_etfs:
        if len(target_etfs) >= g.holdings_num:
            break
        if metrics['score'] >= g.min_score_threshold:
            target_etfs.append(metrics['etf'])
        else:
            break
    
    # ========== 如果无合格标的，尝试使用防御ETF ==========
    if not target_etfs:
        defensive_etf_available = check_defensive_etf_available(context)
        if defensive_etf_available:
            target_etfs = [g.defensive_etf]
    
    target_etfs_set = set(target_etfs)
    
    # ========== 卖出不在目标列表中的持仓 ==========
    for security in current_positions:
        # 只处理ETF池中的标的或防御ETF
        if (security in g.etf_pool or security == g.defensive_etf) and security not in target_etfs_set:
            position = context.portfolio.positions[security]
            if position.amount > 0:
                success = smart_order_target_value(security, 0, context)
                if success:
                    security_name = get_stock_name(security).get(security, security)
                    log.info("卖出不在目标列表的持仓: %s %s" % (security, security_name))
                    
                    # 清除相关记录
                    if security in g.position_highs:
                        del g.position_highs[security]
                    if security in g.position_stop_prices:
                        del g.position_stop_prices[security]
    
    # ========== 检查并执行固定止损 ==========
    for security in list(context.portfolio.positions.keys()):
        if security in g.etf_pool:
            position = context.portfolio.positions[security]
            if position.amount > 0:
                current_price = position.last_sale_price
                cost_price = position.cost_basis
                
                if current_price <= cost_price * g.stop_loss:
                    success = smart_order_target_value(security, 0, context)
                    if success:
                        security_name = get_stock_name(security).get(security, security)
                        loss_percent = (current_price / cost_price - 1) * 100
                        log.info("固定百分比止损卖出: %s %s，亏损: %.2f%%" % 
                                (security, security_name, loss_percent))
                        
                        # 清除记录
                        if security in g.position_highs:
                            del g.position_highs[security]
                        if security in g.position_stop_prices:
                            del g.position_stop_prices[security]
    
    log.info("========== 卖出操作完成 ==========")

# ==================== 获取ETF排名函数 ====================
def get_ranked_etfs(context):
    """
    获取符合条件的ETF排名
    返回结果：应用所有过滤条件，返回满足条件的ETF列表，按得分降序
    """
    etf_metrics = []
    
    # 可选：先进行均线过滤（减少计算量）
    filtered_pool = g.etf_pool
    
    for etf in filtered_pool:
        # ========== 停牌过滤 ==========
        trade_status, high_limit, low_limit = get_trade_status(context, etf)
        if trade_status in ['HALT', 'SUSP', 'STOPT']:
            log.info("%s: 今日停牌，跳过计算" % etf)
            continue
        
        metrics = calculate_momentum_metrics(context, etf)
        if metrics is not None:
            # 过滤掉得分异常的ETF
            if 0 < metrics['score'] < g.max_score_threshold:
                etf_metrics.append(metrics)
            else:
                log.info("警告 %s 得分不满足要求！" % etf)
    
    # 按得分降序排序
    etf_metrics.sort(key=lambda x: x['score'], reverse=True)
    return etf_metrics

# ==================== 动量指标计算函数 ====================
def calculate_momentum_metrics(context, etf):
    """
    计算ETF的动量指标，整合所有过滤条件
    返回包含各项指标和过滤结果的字典
    """
    try:
        # 获取历史价格数据
        lookback = max(g.lookback_days, g.short_lookback_days, 
                    g.rsi_period + g.rsi_lookback_days) + 20
        
        # PTrade使用get_history获取历史数据
        prices_df = get_history(lookback, '1d', ['close', 'high', 'low', 'volume'], 
                            security_list=etf, fq='pre', include=True)
        
        if prices_df is None or len(prices_df) < g.lookback_days:
            log.info("%s: 历史数据不足，跳过计算" % etf)
            return None
        
        # 提取收盘价、最高价、最低价和成交量
        close_prices = prices_df['close'].values
        high_prices = prices_df['high'].values
        low_prices = prices_df['low'].values
        volumes = prices_df['volume'].values
        
        # 最后一个数据点是当前价格
        current_price = close_prices[-1]
        if current_price == 0:
            log.info("%s: 当前价格为0，跳过计算" % etf)
            return None
        
        # 使用包含当前价格的完整序列
        price_series = close_prices
        
        # ========== 成交量过滤检查 ==========
        if g.enable_volume_check and len(price_series) > g.lookback_days and len(volumes) > g.volume_lookback:
            volume_ratio = check_volume_surge(volumes, g.volume_lookback, g.volume_threshold)
            if volume_ratio is not None:
                volume_annualized = get_annualized_returns(price_series, g.lookback_days)
                if volume_annualized > g.volume_return_limit:
                    log.info("%s: 成交量放大%.2f倍且折合年化收益%.2f超过设置值%s，属于'高位放量'，过滤掉" % 
                            (etf, volume_ratio, volume_annualized, g.volume_return_limit))
                    return None
        
        # ========== RSI过滤检查 ==========
        rsi_filter_pass = True
        current_rsi = 0
        max_rsi = 0
        
        if g.use_rsi_filter and len(price_series) >= g.rsi_period + g.rsi_lookback_days:
            rsi_values = calculate_rsi(price_series, g.rsi_period)
            
            if len(rsi_values) >= g.rsi_lookback_days:
                recent_rsi = rsi_values[-g.rsi_lookback_days:]
                rsi_ever_above_threshold = np.any(recent_rsi > g.rsi_threshold)
                
                # 检查当前价格是否在MA5之下
                if len(price_series) >= 5:
                    ma5 = np.mean(price_series[-5:])
                    current_below_ma5 = current_price < ma5
                else:
                    current_below_ma5 = True
                
                if rsi_ever_above_threshold and current_below_ma5:
                    rsi_filter_pass = False
                    max_rsi = np.max(recent_rsi)
                    current_rsi = recent_rsi[-1] if len(recent_rsi) > 0 else 0
                    log.info("RSI过滤: %s 近%s日RSI曾达%.1f，当前价%.3f<MA5，当前RSI=%.1f" % 
                            (etf, g.rsi_lookback_days, max_rsi, current_price, current_rsi))
                else:
                    max_rsi = np.max(recent_rsi) if len(recent_rsi) > 0 else 0
                    current_rsi = recent_rsi[-1] if len(recent_rsi) > 0 else 0
        
        if not rsi_filter_pass:
            return None
        
        # ========== 短期动量计算 ==========
        if len(price_series) >= g.short_lookback_days + 1:
            short_return = price_series[-1] / price_series[-(g.short_lookback_days + 1)] - 1
            short_annualized = (1 + short_return) ** (250.0 / g.short_lookback_days) - 1
        else:
            short_return = 0
            short_annualized = 0
        
        # ========== 短期动量过滤 ==========
        if g.use_short_momentum_filter and short_annualized < g.short_momentum_threshold:
            log.info("%s: 短期动量%.4f < 阈值%.4f，过滤掉" % 
                    (etf, short_annualized, g.short_momentum_threshold))
            return None
        
        # ========== 长期动量计算（加权回归） ==========
        recent_price_series = price_series[-(g.lookback_days + 1):]
        y = np.log(recent_price_series)
        x = np.arange(len(y))
        weights = np.linspace(1, 2, len(y))
        
        # 计算年化收益率
        slope, intercept = np.polyfit(x, y, 1, w=weights)
        annualized_returns = math.exp(slope * 250) - 1
        
        # 计算R²（拟合优度）
        ss_res = np.sum(weights * (y - (slope * x + intercept)) ** 2)
        ss_tot = np.sum(weights * (y - np.mean(y)) ** 2)
        r_squared = 1 - ss_res / ss_tot if ss_tot != 0 else 0
        
        # 综合得分 = 年化收益率 * 趋势稳定性
        score = annualized_returns * r_squared
        
        # ========== 短期风控过滤 ==========
        if len(price_series) >= 4:
            day1_ratio = price_series[-1] / price_series[-2]
            day2_ratio = price_series[-2] / price_series[-3]
            day3_ratio = price_series[-3] / price_series[-4]
            
            if min(day1_ratio, day2_ratio, day3_ratio) < g.loss:
                score = 0
                log.info("警告 %s 近3日有单日跌幅超设定值，已排除" % etf)
        
        return {
            'etf': etf,
            'annualized_returns': annualized_returns,
            'r_squared': r_squared,
            'score': score,
            'slope': slope,
            'current_price': current_price,
            'short_return': short_return,
            'short_annualized': short_annualized,
            'short_momentum_pass': short_return >= g.short_momentum_threshold,
            'rsi_filter_pass': rsi_filter_pass,
            'current_rsi': current_rsi,
            'max_recent_rsi': max_rsi,
        }
        
    except Exception as e:
        log.warning("计算%s动量指标时出错: %s" % (etf, str(e)))
        return None

# ==================== 成交量检查函数 ====================
def check_volume_surge(volumes, lookback_days, threshold):
    """
    检查成交量是否放量
    volumes: 成交量数组（已包含当日数据）
    lookback_days: 历史参考天数
    threshold: 放量阈值
    返回：如果放量返回比值，否则返回None
    """
    if len(volumes) < lookback_days + 1:
        return None
    
    # 当日成交量
    current_volume = volumes[-1]
    
    # 历史平均成交量（不包括当日）
    historical_volumes = volumes[-(lookback_days + 1):-1]
    avg_volume = np.mean(historical_volumes)
    
    if avg_volume == 0:
        return None
    
    volume_ratio = current_volume / avg_volume
    
    if volume_ratio > threshold:
        return volume_ratio
    else:
        return None

# ==================== 均线过滤函数 ====================
def filter_below_ma(context, stocks, days=None):
    """
    过滤掉当前价格小于N日均价的股票/ETF
    返回过滤后的标的列表（仅保留当前价 >= N日均价的标的）
    """
    if days is None:
        days = g.ma_filter_days
    
    if not stocks:
        return []
    
    filtered = []
    
    for stock in stocks:
        try:
            # 获取N日历史收盘价数据（包含当前价格）
            hist = get_history(days, "1d", "close", 
                            security_list=stock, fq='pre', include=True)
            
            if hist is None or len(hist) < days:
                log.info("%s: 历史数据不足%s天，跳过过滤" % (stock, days))
                continue
            
            close_prices = hist['close'].values
            
            # 计算N日均价（包含当前价格）
            ma_n = np.mean(close_prices)
            
            # 获取当前价格（数组最后一个元素）
            current_price = close_prices[-1]
            
            # 保留当前价 >= N日均价的标的
            if current_price >= ma_n:
                filtered.append(stock)
                log.info("%s: 通过%s日均线过滤，当前价 %.2f >= 均线 %.2f" % 
                        (stock, days, current_price, ma_n))
            else:
                log.info("%s: 未通过%s日均线过滤，当前价 %.2f < 均线 %.2f" % 
                        (stock, days, current_price, ma_n))
                
        except Exception as e:
            log.warning("计算%s %s日均价失败: %s" % (stock, days, str(e)))
            continue
    
    return filtered

# ==================== ATR计算函数 ====================
def calculate_atr(security, period=14):
    """
    计算ATR（平均真实波幅）指标
    """
    try:
        needed_days = period + 20
        hist_data = get_history(needed_days, '1d', ['high', 'low', 'close'],
                            security_list=security, fq='pre', include=True)
        
        if hist_data is None or len(hist_data) < period + 1:
            return 0, [], False, "数据不足%s天" % (period + 1)
        
        high_prices = hist_data['high'].values
        low_prices = hist_data['low'].values
        close_prices = hist_data['close'].values
        
        tr_values = np.zeros(len(high_prices))
        for i in range(1, len(high_prices)):
            tr1 = high_prices[i] - low_prices[i]
            tr2 = abs(high_prices[i] - close_prices[i-1])
            tr3 = abs(low_prices[i] - close_prices[i-1])
            tr_values[i] = max(tr1, tr2, tr3)
        
        atr_values = np.zeros(len(tr_values))
        for i in range(period, len(tr_values)):
            atr_values[i] = np.mean(tr_values[i-period+1:i+1])
        
        current_atr = atr_values[-1] if len(atr_values) > 0 else 0
        valid_atr = atr_values[period:] if len(atr_values) > period else atr_values
        
        return current_atr, valid_atr, True, "计算成功"
    
    except Exception as e:
        log.warning("计算%s ATR时出错: %s" % (security, str(e)))
        return 0, [], False, "计算出错:%s" % str(e)

# ==================== RSI计算函数 ====================
def calculate_rsi(prices, period=6):
    """
    计算RSI指标
    """
    if len(prices) < period + 1:
        return []
    
    deltas = np.diff(prices)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    
    avg_gains = np.zeros_like(prices)
    avg_losses = np.zeros_like(prices)
    avg_gains[period] = np.mean(gains[:period])
    avg_losses[period] = np.mean(losses[:period])
    
    rsi_values = np.zeros(len(prices))
    rsi_values[:period] = 50
    
    for i in range(period + 1, len(prices)):
        avg_gains[i] = (avg_gains[i-1] * (period - 1) + gains[i-1]) / period
        avg_losses[i] = (avg_losses[i-1] * (period - 1) + losses[i-1]) / period
        
        if avg_losses[i] == 0:
            rsi_values[i] = 100
        else:
            rs = avg_gains[i] / avg_losses[i]
            rsi_values[i] = 100 - (100 / (1 + rs))
    
    return rsi_values[period:]

# ==================== 计算年化收益 ====================
def get_annualized_returns(price_series, lookback_days):
    """
    计算年化收益率
    """
    # 使用最后lookback_days+1天的数据
    recent_price_series = price_series[-(lookback_days + 1):]
    y = np.log(recent_price_series)
    x = np.arange(len(y))
    weights = np.linspace(1, 2, len(y))  # 加权回归，近期权重更高
    
    # 计算年化收益率
    slope, intercept = np.polyfit(x, y, 1, w=weights)
    annualized_returns = math.exp(slope * 250) - 1
    return annualized_returns

# ==================== 买入函数 ====================
def etf_buy_trade(context):
    """
    买入函数
    功能：买入符合条件的ETF
    """
    log.info("========== 买入操作开始 ==========")
    
    # 获取符合条件的ETF排名
    ranked_etfs = get_ranked_etfs(context)
    
    # 记录所有ETF的指标（用于调试）
    if ranked_etfs:
        log.info("=== 符合条件的ETF指标 ===")
        for i, metrics in enumerate(ranked_etfs[:5]):  # 只显示前5名
            if i >= 5:
                break
            etf_name = get_stock_name(metrics['etf']).get(metrics['etf'], metrics['etf'])
            log.info("%s %s: 得分=%.4f, 年化=%.4f, R²=%.4f, 短期动量=%.4f, RSI=%.1f" % 
                    (metrics['etf'], etf_name, metrics['score'], metrics['annualized_returns'], 
                    metrics['r_squared'], metrics['short_return'], metrics['current_rsi']))
    
    # ========== 选择前g.holdings_num只合格ETF ==========
    target_etfs = []
    for metrics in ranked_etfs:
        if len(target_etfs) >= g.holdings_num:
            break
        if metrics['score'] >= g.min_score_threshold:
            target_etfs.append(metrics['etf'])
        else:
            break
    
    # 如果没有合格标的，尝试使用防御ETF
    if not target_etfs:
        if check_defensive_etf_available(context):
            target_etfs = [g.defensive_etf]
            log.info("进入防御模式，选择防御ETF: %s %s" % 
                    (g.defensive_etf, get_stock_name(g.defensive_etf).get(g.defensive_etf, g.defensive_etf)))
        else:
            log.info("进入空仓模式，无符合条件的ETF且防御ETF不可用")
            return
    else:
        # 显示选中的ETF
        selected_info = []
        for etf in target_etfs:
            etf_name = get_stock_name(etf).get(etf, etf)
            selected_info.append("%s %s" % (etf, etf_name))
        log.info("选择前%s名ETF: %s" % (len(target_etfs), ', '.join(selected_info)))
    
    # ========== 检查是否有其他非目标持仓未清空 ==========
    current_positions = list(context.portfolio.positions.keys())
    current_etf_positions = [pos for pos in current_positions if pos in g.etf_pool or pos == g.defensive_etf]
    other_positions = [pos for pos in current_etf_positions if pos not in target_etfs]
    
    if other_positions:
        for pos in other_positions:
            position = context.portfolio.positions[pos]
            if position.amount > 0:
                pos_name = get_stock_name(pos).get(pos, pos)
                log.info("警告 尚有其他持仓 %s 未卖出，等待卖出完成后再买入新标的" % pos_name)
                return
    
    # ========== 等权重分配资金 ==========
    # 交易环境使用可用资金，回测环境使用总资产
    if is_trade():
        # 实盘：使用可用资金 + 现有持仓市值
        available_cash = context.portfolio.cash
        current_positions_value = 0
        
        # 计算目标ETF中已有持仓的市值
        for etf in target_etfs:
            if etf in context.portfolio.positions:
                pos = context.portfolio.positions[etf]
                current_positions_value += pos.amount * pos.last_sale_price
        
        total_available = available_cash + current_positions_value
        target_value_per_etf = total_available / len(target_etfs)
        
        log.info("实盘资金分配 - 可用资金: %.2f, 目标持仓市值: %.2f, 总可用: %.2f, 单ETF目标: %.2f" % 
                (available_cash, current_positions_value, total_available, target_value_per_etf))
    else:
        # 回测：使用总资产
        total_value = context.portfolio.portfolio_value
        target_value_per_etf = total_value / len(target_etfs)
        log.info("回测资金分配 - 总资产: %.2f, 单ETF目标: %.2f" % 
                (total_value, target_value_per_etf))
    
    # 对每个目标ETF下单
    for etf in target_etfs:
        success = smart_order_target_value(etf, target_value_per_etf, context)
        if success:
            etf_name = get_stock_name(etf).get(etf, etf)
            # 判断是买入还是调仓
            current_pos = context.portfolio.positions.get(etf)
            current_val = 0
            if current_pos:
                current_val = current_pos.amount * current_pos.last_sale_price
            action = "调仓" if current_val > 0 else "买入"
            log.info("%s: %s %s，目标金额: %.2f" % (action, etf, etf_name, target_value_per_etf))
    
    log.info("========== 买入操作完成 ==========")

# ==================== 辅助函数 ====================
def check_defensive_etf_available(context):
    """检查防御ETF是否可交易"""
    defensive_etf = g.defensive_etf
    
    try:
        if is_trade():
            # 交易环境使用get_snapshot
            snapshot = get_snapshot(defensive_etf)
            
            if not snapshot or defensive_etf not in snapshot:
                log.info("防御性ETF %s 无行情数据" % defensive_etf)
                return False
            
            etf_info = snapshot[defensive_etf]
            trade_status = etf_info.get('trade_status', 'TRADE')
            
            if trade_status in ['HALT', 'SUSP', 'STOPT']:
                log.info("防御性ETF %s 今日停牌" % defensive_etf)
                return False
            
            last_px = etf_info.get('last_px', 0)
            high_limit = etf_info.get('up_px', 0)
            low_limit = etf_info.get('down_px', 0)
            
            if last_px >= high_limit and high_limit > 0:
                log.info("防御性ETF %s 当前涨停" % defensive_etf)
                return False
            
            if last_px <= low_limit and low_limit > 0:
                log.info("防御性ETF %s 当前跌停" % defensive_etf)
                return False
        else:
            # 回测环境简单检查数据可用性
            hist = get_history(1, '1d', ['close', 'volume'], 
                            security_list=defensive_etf, fq='pre', include=True)
            if hist is None or len(hist) == 0:
                log.info("防御性ETF %s 无历史数据" % defensive_etf)
                return False
            
            volume = hist['volume'].values[-1]
            if volume == 0:
                log.info("防御性ETF %s 停牌" % defensive_etf)
                return False
        
        return True
        
    except Exception as e:
        log.warning("检查防御ETF可用性时出错: %s" % str(e))
        return False

def smart_order_target_value(security, target_value, context):
    """
    智能下单函数，兼容回测和交易环境
    """
    try:
        # 获取交易状态和限价信息
        trade_status, high_limit, low_limit = get_trade_status(context, security)
        
        # 检查标的是否停牌
        if trade_status in ['HALT', 'SUSP', 'STOPT']:
            security_name = get_stock_name(security).get(security, security)
            log.info("%s %s: 今日停牌，跳过交易" % (security, security_name))
            return False
        
        # 获取当前价格
        current_price, price_success = get_current_price(context, security)
        if not price_success or current_price == 0:
            security_name = get_stock_name(security).get(security, security)
            log.info("%s %s: 无法获取当前价格，跳过交易" % (security, security_name))
            return False
        
        # 检查涨停（买入时）
        if target_value > 0 and high_limit > 0:
            if current_price >= high_limit:
                security_name = get_stock_name(security).get(security, security)
                log.info("%s %s: 当前涨停，跳过买入" % (security, security_name))
                return False
        
        # 检查跌停（卖出时）
        if target_value == 0 and low_limit > 0:
            if current_price <= low_limit:
                security_name = get_stock_name(security).get(security, security)
                log.info("%s %s: 当前跌停，跳过卖出" % (security, security_name))
                return False
        
        # 计算目标数量
        target_amount = int(target_value / current_price)
        
        # 对于ETF，按100股整数倍调整
        target_amount = (target_amount // 100) * 100
        if target_amount <= 0 and target_value > 0:
            target_amount = 100
        
        # 限制单笔最大委托数量（避免超过券商限制）
        if target_amount > g.max_order_amount:
            log.warning("%s: 计算的目标数量%s超过单笔最大限额%s，调整为最大限额" % 
                    (security, target_amount, g.max_order_amount))
            target_amount = g.max_order_amount
        
        # 获取当前持仓
        current_position = context.portfolio.positions.get(security, None)
        current_amount = current_position.amount if current_position else 0
        
        # 计算需要调整的数量
        amount_diff = target_amount - current_amount
        
        # 限制单次调整数量（避免超过券商限制）
        if abs(amount_diff) > g.max_order_amount:
            if amount_diff > 0:
                log.warning("%s: 需买入数量%s超过单笔限额%s，本次先买入%s股" % 
                        (security, amount_diff, g.max_order_amount, g.max_order_amount))
                amount_diff = g.max_order_amount
            else:
                log.warning("%s: 需卖出数量%s超过单笔限额%s，本次先卖出%s股" % 
                        (security, abs(amount_diff), g.max_order_amount, g.max_order_amount))
                amount_diff = -g.max_order_amount
        
        # 检查最小交易金额
        trade_value = abs(amount_diff) * current_price
        if 0 < trade_value < g.min_money:
            security_name = get_stock_name(security).get(security, security)
            log.info("%s %s: 交易金额%.2f小于最小交易额%s，跳过交易" % 
                    (security, security_name, trade_value, g.min_money))
            return False
        
        # 检查T+1限制（卖出操作）
        if amount_diff < 0:
            closeable_amount = current_position.enable_amount if current_position else 0
            if closeable_amount == 0:
                security_name = get_stock_name(security).get(security, security)
                log.info("%s %s: 当天买入不可卖出(T+1)" % (security, security_name))
                return False
            amount_diff = -min(abs(amount_diff), closeable_amount)
        
        # 执行下单
        if amount_diff != 0:
            # 使用限价单，价格设置为当前价格的小数精度（ETF为3位小数）
            limit_price = round(current_price, 3)
            order_result = order(security, amount_diff, limit_price=limit_price)
            
            if order_result:
                # 更新持仓记录
                g.positions[security] = target_amount
                
                # 如果买入操作，初始化最高价记录和ATR止损价
                if amount_diff > 0 and security in g.etf_pool:
                    g.position_highs[security] = current_price
                    
                    # 计算ATR止损价
                    if g.use_atr_stop_loss and not (g.atr_exclude_defensive and security == g.defensive_etf):
                        current_atr, atr_list, success, msg = calculate_atr(security, g.atr_period)
                        if success:
                            if g.atr_trailing_stop:
                                g.position_stop_prices[security] = current_price - g.atr_multiplier * current_atr
                            else:
                                g.position_stop_prices[security] = current_price - g.atr_multiplier * current_atr
                
                security_name = get_stock_name(security).get(security, security)
                if amount_diff > 0:
                    log.info("买入 %s %s，数量: %s，价格: %.3f" % 
                            (security, security_name, amount_diff, current_price))
                else:
                    log.info("卖出 %s %s，数量: %s，价格: %.3f" % 
                            (security, security_name, abs(amount_diff), current_price))
                return True
            else:
                security_name = get_stock_name(security).get(security, security)
                log.warning("下单失败: %s %s，数量: %s" % (security, security_name, amount_diff))
                return False
        
        return False
        
    except Exception as e:
        log.warning("智能下单%s时出错: %s" % (security, str(e)))
        return False

def check_atr_stop_loss(context):
    """
    检查并执行ATR动态止损
    """
    if not g.use_atr_stop_loss:
        return
    
    try:
        positions_list = list(context.portfolio.positions.keys())
        if not positions_list:
            return
        
        # 批量获取当前价格
        current_prices = get_current_prices_batch(context, positions_list)
        
        for security in positions_list:
            if security not in g.etf_pool:
                continue
            
            position = context.portfolio.positions[security]
            if position.amount <= 0:
                continue
            
            # 防御ETF豁免检查
            if g.atr_exclude_defensive and security == g.defensive_etf:
                continue
            
            try:
                # 获取当前价格
                if security not in current_prices:
                    continue
                
                current_price = current_prices[security]
                if current_price == 0:
                    continue
                
                cost_price = position.cost_basis
                
                # 计算当前ATR值
                current_atr, atr_values, success, atr_info = calculate_atr(security, g.atr_period)
                
                if not success:
                    continue
                
                # 更新持仓期间的最高价
                if security not in g.position_highs:
                    g.position_highs[security] = current_price
                else:
                    g.position_highs[security] = max(g.position_highs[security], current_price)
                
                position_high = g.position_highs[security]
                
                # 计算ATR止损价
                if g.atr_trailing_stop:
                    atr_stop_price = position_high - g.atr_multiplier * current_atr
                else:
                    atr_stop_price = cost_price - g.atr_multiplier * current_atr
                
                g.position_stop_prices[security] = atr_stop_price
                
                # 检查是否触发ATR止损
                if current_price <= atr_stop_price:
                    success = smart_order_target_value(security, 0, context)
                    if success:
                        security_name = get_stock_name(security).get(security, security)
                        loss_percent = (current_price / cost_price - 1) * 100
                        atr_stop_type = "跟踪" if g.atr_trailing_stop else "固定"
                        log.info("ATR动态止损(%s)卖出: %s %s，亏损: %.2f%%" % 
                                (atr_stop_type, security, security_name, loss_percent))
                        
                        # 清除记录
                        if security in g.position_highs:
                            del g.position_highs[security]
                        if security in g.position_stop_prices:
                            del g.position_stop_prices[security]
            
            except Exception as e:
                log.warning("检查%s ATR止损时出错: %s" % (security, str(e)))
                
    except Exception as e:
        log.warning("ATR止损检查整体出错: %s" % str(e))

# ==================== 必需的handle_data函数 ====================
def handle_data(context, data):
    """
    PTrade必需的handle_data函数
    由于策略使用run_daily定时执行，这里保持为空即可
    """
    pass
#############################################################
def initialize(context):
    # 长白山股票代码
    g.security = '603099.SS'
    set_universe(g.security)
    # 用于标记是否已在当年4-5月买入
    g.bought_this_year = False
    # 记录当前年份，用于判断新一年的开始
    g.current_year = None
    log.info('=== 策略初始化完成 ===')
    log.info('标的股票: %s (长白山)' % g.security)
    log.info('策略逻辑: 4-5月底价买入，价格突破60元卖出')

def before_trading_start(context, data):
    # 获取当前日期
    current_date = context.blotter.current_dt
    current_month = current_date.month
    current_year = current_date.year
    
    # 如果跨年了，重置买入标记
    if g.current_year != current_year:
        g.current_year = current_year
        g.bought_this_year = False
        log.info('=== 新年份 %d 开始，重置买入标记 ===' % current_year)
    
    # 每日盘前信息
    position = get_position(g.security)
    log.info('【盘前状态】日期: %s, 当前持仓: %d股, 今年是否已买入: %s, 当前月份: %d月' 
            % (current_date.strftime('%Y-%m-%d'), position.amount, g.bought_this_year, current_month))

def handle_data(context, data):
    security = g.security
    current_date = context.blotter.current_dt
    current_month = current_date.month
    
    # 获取当前持仓
    position = get_position(security)
    current_amount = position.amount
    
    # 获取当前价格（收盘价和最高价）
    current_price = data[security].close
    high_price = data[security].high
    
    # 获取账户信息
    cash = context.portfolio.cash
    portfolio_value = context.portfolio.portfolio_value
    
    # 输出每日基本运行状态（确认策略在运行）
    log.info('--- 策略运行 %s ---' % current_date.strftime('%Y-%m-%d'))
    
    # 卖出逻辑：盘中最高价 > 60元，立刻全部卖出（最高优先级）
    if current_amount > 0 and high_price > 60:
        order_target(security, 0)
        log.info('>>> 【卖出信号】盘中最高价突破60元，立刻卖出全部持仓 | 最高价: %.2f元, 收盘价: %.2f元, 持仓: %d股' 
                % (high_price, current_price, current_amount))
        return
    
    # 持仓监控：显示当前持仓状态
    if current_amount > 0:
        cost_basis = position.cost_basis
        pnl_ratio = (current_price - cost_basis) / cost_basis * 100 if cost_basis > 0 else 0
        log.info('【持仓中】收盘价: %.2f元, 成本: %.2f元, 盈亏: %.2f%%, 持仓: %d股, 等待突破60元' 
                % (current_price, cost_basis, pnl_ratio, current_amount))
    
    # 买入逻辑：仅在4-5月执行
    if current_month in [4, 5] and not g.bought_this_year and current_amount == 0:
        # 获取过去30天的历史价格，找到底价区域
        try:
            history = get_history(30, '1d', 'close', security, fq='pre', include=False)
            if len(history) > 0:
                # 计算30天最低价和平均价
                min_price = history['close'].min()
                avg_price = history['close'].mean()
                
                # 底价买入策略：当前价格接近最低价（在最低价上浮5%范围内）
                threshold_price = min_price * 1.05
                
                log.info('【4-5月买入窗口】当前价格: %.2f元, 30日最低: %.2f元, 买入阈值: %.2f元, 30日均价: %.2f元' 
                        % (current_price, min_price, threshold_price, avg_price))
                
                if current_price <= threshold_price:
                    # 使用80%的可用资金买入
                    buy_value = cash * 1.0
                    if buy_value > 0:
                        order_value(security, buy_value)
                        g.bought_this_year = True
                        expected_shares = int(buy_value / current_price / 100) * 100
                        log.info('>>> 【买入信号】底价区域买入 | 价格: %.2f元, 预计买入: %d股, 金额: %.2f元' 
                                % (current_price, expected_shares, buy_value))
                    else:
                        log.info('资金不足，无法买入')
                else:
                    price_diff_ratio = (current_price - threshold_price) / threshold_price * 100
                    log.info('价格高于买入阈值 %.2f%%，等待价格回落' % price_diff_ratio)
        except Exception as e:
            log.error('获取历史数据失败: %s' % str(e))
    elif current_month not in [4, 5] and current_amount == 0:
        # 非4-5月且无持仓，显示等待状态
        if current_month in [1, 2, 3]:
            log.info('【等待买入窗口】当前%d月，等待进入4-5月买入窗口，价格: %.2f元' % (current_month, current_price))
        elif current_month in [6, 7, 8, 9, 10, 11, 12]:
            log.info('【非交易窗口】当前%d月，价格: %.2f元，等待明年4-5月' % (current_month, current_price))
    elif g.bought_this_year and current_amount == 0:
        # 今年已经买入过但现在没有持仓（已卖出），不再买入
        log.info('【本年已完成交易】今年已买入并卖出，等待下一年，当前价格: %.2f元' % current_price)
    
    # 最后输出账户总览
    log.info('账户总资产: %.2f元, 可用资金: %.2f元, 持仓市值: %.2f元' 
            % (portfolio_value, cash, position.amount * current_price if position.amount > 0 else 0))
###################################################
'''
#策略名称：PTRADE股票双低三因子策略（版权所有不得转卖或转赠）
#升级说明：在A级策略“股票双低轮动策略”的基础上增加了回调因子，寻找调整过后的双低个股。同时加入了
时序因子，在历史数据小微盘股表现不佳的月份选择空仓。经过优化后策略收益率有较大提升，最大回撤也有所减小。

# 特别注意：本策略日频调仓，实盘和回测时请在周期频率选项处选择 "每日"！！！每天调仓时间为14：50左右（根据券商不同有细微差别）
# 再次重申：本策略日频调仓，实盘和回测时请在周期频率选项处选择 "每日"！！！
#——————————————————
'''

#v2：前后3因子一致版

import pandas as pd
import numpy as np

# 初始化
def initialize(context):
    set_universe([])
    g.enable_market_sentiment = True  # 情绪监控开关 （默认True开启）
    g.use_index_stocks = False        # 股票池开关设置True=使用指数成分股，False=使用全市场A股  
    g.enable_financial_filter = True  # 是否开启财务指标筛选（True打开）
    g.enable_688 = True               # 是否允许科创板标的（True允许）
    g.clear_period = False            # 空仓期初始化 
    g.index = "399303.SZ"             # 成分股指数 (默认国证2000）
    g.buy_stock_count = 10             # 最大持有股票数量
    g.pervalue = 20000                # 单次买入金额
    g.screen_stock_count = 70         # 盘前筛选股票数量（情绪监控池）
    g.fall_days = 30                  # 回调因子计算周期（天）
    g.price_line = 2.2             # 股价下限
    g.turnover_threshold = 1     # 换手率下限%
    g.float_line = 6 * 100000000   # 市值下限
    g.market_cap_weight = 1      # 市值因子权重系数
    g.fallback_weight = 1        # 回调因子权重系数
    if not is_trade():
        set_backtest()  # 设置回测条件
    
    # 情绪监控设置
    g.down_ratio_threshold = 0.51   # 下跌家数超过时清仓
    g.hi_ratio = 0.95              # 极端情绪阈值，默认下跌家数超95%时恢复买入
    g.holdings = set()
    g.pause_buy = False      # 暂停买入标志
    
# 设置回测条件
def set_backtest():
    set_limit_mode("UNLIMITED")
    set_commission(commission_ratio=0.00015, min_commission=5.0, type="stock")


# 盘前处理
def before_trading_start(context, data):
    g.pre_position_list = list(g.holdings)
    g.pause_buy = False
    
    # ===== 空仓期检查 =====
    current_date = context.current_dt.date()
    g.clear_period = False
    
    # 检查是否在空仓期
    if (current_date.month == 12 and current_date.day >= 15) or \
       (current_date.month in (1, 2) and (current_date.month == 1 or current_date.day <= 5)):
        g.clear_period = True
 #       log.info("当前日期 %s 处于空仓期 ，停止选股并准备清仓" % current_date)
        g.trade_stocks = []
        set_universe([])
        return  # 直接返回，跳过后续选股逻辑    
        
    if g.use_index_stocks:
        g.stock_list = get_index_stocks(g.index)
    else:
        g.stock_list = get_Ashares() 
    
    stock_list_tmp = filter_stock_by_status(g.stock_list, filter_type=["ST", "HALT", "DELISTING","DELISTING_SORTING"], query_date=None)
    if not g.enable_688:
        stock_list_tmp = [s for s in stock_list_tmp if not s.startswith('688')]
    
    
    if g.enable_financial_filter:
        log.info("开始财务筛选，当前候选数量：%d" % len(stock_list_tmp))
        current_year = context.previous_date.year
        years_needed = [current_year - 1, current_year - 2]
        df_income = get_fundamentals(stock_list_tmp, 'income_statement', fields=['net_profit'],
                                     start_year=str(years_needed[1]), end_year=str(years_needed[0]),
                                     report_types='4', date_type='end')
        valid_stocks = []
        if not df_income.empty:
            grouped = df_income.groupby('secu_code')['net_profit'].agg(
                lambda x: x.count() >= 2 and not (x < 0).all()
            )
            valid_stocks = grouped[grouped].index.tolist()
        stock_list_tmp = [stock for stock in stock_list_tmp if stock in valid_stocks]
        log.info("净利润筛选后数量：%d" % len(stock_list_tmp))
    else:
        log.info("已关闭财务筛选，跳过净利润及ROE检查")

    # 获取估值数据
    fields = ["total_value", "a_floats", "float_value", "turnover_rate"]
    df = get_fundamentals(stock_list_tmp, "valuation", fields=fields, date=context.previous_date)
    
    df['turnover_rate'] = df['turnover_rate'].astype(float)
    df['price'] = df['float_value'] / df['a_floats']
    df = df[
        (df['price'] > g.price_line) & 
        (df['float_value'] > g.float_line) &
        (df['turnover_rate'] >= g.turnover_threshold)
    ].sort_values(by='float_value').head(400)
    
    stock_list_tmp = df.index.tolist()
    set_universe(stock_list_tmp)
    
    # === 新增：计算回调幅度 ===
    # 获取历史收盘价数据
    close_data = get_history(g.fall_days+1, '1d', ['close'], stock_list_tmp, fq='pre', is_dict=True)
      
    # 计算每只股票的回调幅度
    fallback_pct = {}
    for stock in stock_list_tmp:
        if stock in close_data:
            closes = close_data[stock]['close']
            if len(closes) >= 2:  # 确保有足够数据
                start_price = closes[0]   # g.fall_days天前的收盘价
                end_price = closes[-1]    # 最近交易日收盘价
                fallback = (start_price - end_price) / start_price
                fallback_pct[stock] = fallback
            else:
                fallback_pct[stock] = 0  # 数据不足设为0
        else:
            fallback_pct[stock] = 0
    
    # 将回调幅度加入DataFrame
    df['fallback'] = pd.Series(fallback_pct)
    
    # === 修改：三因子排序 ===
    df['市值排名'] = df['float_value'].rank()
    df['股价排名'] = df['price'].rank()
    df['回调排名'] = df['fallback'].rank(ascending=False)  # 回调幅度越大排名越小
    df['综合排名'] = (
        df['市值排名'] * g.market_cap_weight + 
        df['股价排名'] * 1 +  # 保持原股价权重为1
        df['回调排名'] * g.fallback_weight
    )
    df = df.sort_values(by='综合排名').head(g.screen_stock_count)
    
    g.trade_stocks = df.index.tolist()
    g.df = df
    
    # === 修改：日志增加回调幅度信息 ===
    if not df.empty:
        min_price = df['price'].min()
        max_price = df['price'].max()
        avg_price = df['price'].mean()
        min_float_value = df['float_value'].min()
        max_float_value = df['float_value'].max()
        avg_float_value = df['float_value'].mean()
        min_fallback = df['fallback'].min() * 100  # 转换为百分比
        max_fallback = df['fallback'].max() * 100
        avg_fallback = df['fallback'].mean() * 100
        stock_count = len(df)
        
        log.info(f"[盘前筛选] 共筛选股票 {stock_count} 只 | "
                f"股价范围 {min_price:.2f}-{max_price:.2f} 元 | "
                f"流通市值 {min_float_value/100000000:.2f}-{max_float_value/100000000:.2f} 亿 | "
                f"回调幅度 {min_fallback:.2f}%-{max_fallback:.2f}%")
    else:
        log.warning("[盘前筛选] 未筛选出符合条件的股票，请检查筛选参数！")


# 盘中处理
def handle_data(context, data):
    # 空仓期处理
    if g.clear_period:
        # 清空所有持仓
        for stock in list(context.portfolio.positions):
            order_target_value(stock, 0)
        return  # 跳过后续交易逻辑    
    
    if g.enable_market_sentiment:
        # 获取实时涨跌家数
        down_ratio, decline_count, valid_count = get_realtime_down_ratio(context, data, g.trade_stocks)
        log.info("[情绪监控] 当前下跌比例：{:.2%} (下跌家数：{}，统计家数：{})".format(down_ratio, decline_count, valid_count))

        # 风控判断
        if g.hi_ratio > down_ratio > g.down_ratio_threshold:
            log.warning("[情绪监控] 触发下跌家数阈值，执行清仓")
            clear_all_positions(context)
            return  # 终止后续交易
    else:
        log.info("[情绪监控] 当前市场情绪监控已关闭")   
    buy_stocks = get_trade_stocks(context, data)
    log.info("buy_stocks:%s" % buy_stocks)
    trade(context, buy_stocks)

def get_realtime_down_ratio(context, data, stock_list):
    """通过data对象计算下跌比例"""
    if not stock_list:
        return 0.0
    
    decline_count = 0
    valid_count = 0
    
    for stock in stock_list:
        # 确保股票在数据中且价格有效
        if stock in data and data[stock].price > 0 and data[stock].preclose > 0:
            if data[stock].price < data[stock].preclose:
                decline_count += 1
            valid_count += 1
    
    down_ratio = decline_count / valid_count if valid_count > 0 else 0.0
    return down_ratio, decline_count, valid_count

def clear_all_positions(context):
    """清空所有持仓"""
    for stock in list(g.holdings):
        order_target(stock, 0)
        log.info("清仓: %s" % stock)
    g.holdings.clear()

# 交易函数
def trade(context, buy_stocks):
    # 卖出不在买入列表中的持仓
    for stock in list(g.holdings):
        if stock not in buy_stocks:
            order_target_value(stock, 0)
            g.holdings.remove(stock)
            log.info("sell:%s" % stock)
    
    # 买入新标的，使用固定金额
    for stock in buy_stocks:
        if stock not in g.holdings and len(g.holdings) < g.buy_stock_count:
            order_value(stock, g.pervalue)
            g.holdings.add(stock)
            log.info("buy:%s" % stock)


# 获取买入股票池（涨停股不参与换仓）
def get_trade_stocks(context, data):
    hold_up_limit_stock = [stock.replace("XSHG", "SS").replace("XSHE", "SZ") 
                          for stock in g.pre_position_list 
                          if check_limit(stock)[stock] == 1] # 获取持仓中涨停的标的
    df = g.df
    if df.empty:
        return hold_up_limit_stock
    df["code"] = df.index
    # 计算当前流通市值和实时股价
    df["curr_float_value"] = df.apply(lambda x: x["a_floats"] * data[x["code"]].price, axis=1)
    df["curr_price"] = df.apply(lambda x: data[x["code"]].price, axis=1)
    
    # 过滤无效数据
    df = df[(df["curr_float_value"] > 0) & (df["curr_price"] > g.price_line)]
    
    # 三因子排序（与盘前逻辑一致）
    df['市值排名'] = df['curr_float_value'].rank()
    df['股价排名'] = df['curr_price'].rank()
    # 使用盘前计算好的回调幅度（因为盘中无法重新计算）
    df['回调排名'] = df['fallback'].rank(ascending=False)
    df['综合排名'] = (
        df['市值排名'] * g.market_cap_weight + 
        df['股价排名'] * 1 + 
        df['回调排名'] * g.fallback_weight
    )
    
    # 按综合排名排序
    stocks = df.sort_values(by="综合排名").index.tolist()
    
    # 计算本次可买入数量
    count = g.buy_stock_count - len(hold_up_limit_stock)
    check_out_lists = stocks[:count]
    check_out_lists = check_out_lists + hold_up_limit_stock
    return check_out_lists
####################################################
# 导入必要的库
import pandas as pd

# 初始化函数
def initialize(context):
    # 全局变量设置
    g.index = '399101.XBHS'  # 中小板综指数
    g.buy_stock_count = 3    # 持仓股票数量
    g.screen_stock_count = 15 # 筛选股票数量
    
    # 财务数据筛选阈值
    g.roe_threshold = 0.15   # ROE > 15%
    g.roa_threshold = 0.10   # ROA > 10%
    g.revenue_threshold = 1e8 # 营业收入 > 1亿元
    g.profit_threshold = 0    # 净利润 > 0
    g.market_cap_min = 5      # 市值下限（亿元）
    g.market_cap_max = 50     # 市值上限（亿元）
    
    # 风控参数
    g.stoploss_limit = 0.88   # 个股止损阈值
    g.HV_ratio = 0.9          # 异常放量检测比例
    
    # 设置股票池
    g.security = get_index_stocks(g.index)
    set_universe(g.security)
    
    # 设置定时任务 - 修正：run_daily需要3个参数
    run_daily(context, before_trading_start, time='9:00')
    run_daily(context, handle_data, time='10:00')
    
    # 如果需要更多定时任务，可以添加
    run_daily(context, check_stoploss_daily, time='14:30')
    run_daily(context, print_position_info, time='15:00')

# 盘前处理函数
def before_trading_start(context, data):
    """
    盘前处理函数，接受2个参数
    """
    log.info(f"盘前处理开始: {context.blotter.current_dt}")
    
    # 获取指数成分股
    stocks = get_index_stocks(g.index)
    
    # 过滤ST、停牌、退市股票
    stocks = filter_stock_by_status(stocks, filter_type=["ST", "HALT", "DELISTING"])
    
    # 获取财务数据并进行筛选
    g.target_list = filter_by_fundamentals(context, stocks)
    
    # 按流通市值排序，选择小市值股票
    if g.target_list:
        # 获取流通市值数据
        df = get_fundamentals(g.target_list, "valuation", 
                              fields=["float_value"], 
                              date=context.previous_date,
                              is_dataframe=True)
        
        if df is not None and not df.empty:
            df = df.sort_values(by="float_value", ascending=True)
            g.target_list = df.index.tolist()[:g.screen_stock_count]
    
    log.info(f"今日目标股票列表: {g.target_list}")

# 财务数据筛选函数
def filter_by_fundamentals(context, stocks):
    """
    基于财务数据筛选股票
    """
    if not stocks:
        return []
    
    try:
        # 获取当前日期
        current_date = context.blotter.current_dt.strftime('%Y%m%d')
        
        # 获取盈利能力数据
        df_profit = get_fundamentals(stocks, "profit_ability",
                                     fields=["roe", "roa"],
                                     date=current_date,
                                     is_dataframe=True)
        
        # 获取利润表数据
        df_income = get_fundamentals(stocks, "income_statement",
                                     fields=["net_profit", "operating_revenue"],
                                     date=current_date,
                                     is_dataframe=True)
        
        # 获取估值数据
        df_val = get_fundamentals(stocks, "valuation",
                                  fields=["total_value"],
                                  date=current_date,
                                  is_dataframe=True)
        
        if df_profit is None or df_income is None or df_val is None:
            return []
        
        # 合并数据
        df = df_profit.merge(df_income, left_index=True, right_index=True, how='inner')
        df = df.merge(df_val, left_index=True, right_index=True, how='inner')
        
        # 转换为数值类型
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # 市值转为亿元
        df['total_value'] = df['total_value'] / 1e8
        
        # 应用筛选条件
        mask = (
            (df['roe'] > g.roe_threshold) &
            (df['roa'] > g.roa_threshold) &
            (df['net_profit'] > g.profit_threshold) &
            (df['operating_revenue'] > g.revenue_threshold) &
            (df['total_value'] >= g.market_cap_min) &
            (df['total_value'] <= g.market_cap_max)
        )
        
        filtered_stocks = df[mask].index.tolist()
        log.info(f"财务数据筛选后股票数量: {len(filtered_stocks)}")
        return filtered_stocks
        
    except Exception as e:
        log.error(f"财务数据筛选异常: {e}")
        return []

# 盘中交易处理函数
def handle_data(context, data):
    """
    盘中交易处理函数
    """
    log.info(f"盘中交易处理: {context.blotter.current_dt}")
    
    # 检查持仓股票的止损条件
    check_stoploss(context, data)
    
    # 检查异常放量
    check_high_volume(context, data)
    
    # 获取当前持仓
    current_positions = list(context.portfolio.positions.keys())
    
    # 卖出不在目标列表中的股票（涨停股除外）
    for stock in current_positions:
        if stock not in g.target_list:
            # 检查是否涨停
            if not is_limit_up(stock, data):
                order_target_value(stock, 0)
                log.info(f"卖出不在目标列表的股票: {stock}")
    
    # 买入目标股票
    if g.target_list:
        # 计算可用资金
        available_cash = context.portfolio.cash
        
        # 计算每只股票分配的资金
        buy_count = min(g.buy_stock_count - len(current_positions), len(g.target_list))
        if buy_count > 0 and available_cash > 0:
            value_per_stock = available_cash / buy_count
            
            for stock in g.target_list[:buy_count]:
                if stock not in current_positions:
                    order_target_value(stock, value_per_stock)
                    log.info(f"买入财务数据良好的小市值股票: {stock}")

# 止损检查函数
def check_stoploss(context, data):
    for stock, position in context.portfolio.positions.items():
        avg_cost = position.cost_basis
        if avg_cost <= 0:
            continue
            
        # 获取当前价格
        current_price = data[stock].price if stock in data else position.last_sale_price
        
        if current_price < avg_cost * g.stoploss_limit:
            order_target_value(stock, 0)
            log.info(f"触发止损，卖出股票: {stock} (成本: {avg_cost:.2f}, 现价: {current_price:.2f})")

# 每日止损检查函数（独立定时任务）
def check_stoploss_daily(context):
    """
    每日固定时间检查止损
    """
    log.info("执行每日止损检查")
    
    # 获取当前持仓
    positions = get_positions()
    
    for stock, position in positions.items():
        avg_cost = position.cost_basis
        if avg_cost <= 0:
            continue
            
        # 获取当前价格
        snapshot = get_snapshot(stock)
        if snapshot and stock in snapshot:
            current_price = snapshot[stock].get("last_px", 0)
            
            if current_price > 0 and current_price < avg_cost * g.stoploss_limit:
                order_target_value(stock, 0)
                log.info(f"每日止损检查：卖出股票: {stock}")

# 异常放量检查函数
def check_high_volume(context, data):
    for stock in context.portfolio.positions.keys():
        try:
            # 获取历史成交量
            hist_data = get_history(120, '1d', 'volume', 
                                    security_list=[stock], 
                                    fq='pre')
            
            if hist_data is not None and not hist_data.empty:
                # 获取当日成交量
                if stock in data:
                    cur_volume = data[stock].volume
                    hist_max = hist_data.max().values
                    
                    # 检查是否异常放量
                    if cur_volume > g.HV_ratio * hist_max:
                        order_target_value(stock, 0)
                        log.info(f"检测到异常放量，卖出股票: {stock}")
        except Exception as e:
            log.error(f"检查异常放量时出错: {e}")

# 涨停检查函数
def is_limit_up(stock, data):
    """
    检查股票是否涨停
    """
    if stock not in data:
        return False
    
    try:
        # 获取最新价格和涨停价
        current_data = data[stock]
        last_close = current_data.pre_close
        current_price = current_data.price
        
        if last_close <= 0:
            return False
        
        # 计算涨停价（考虑不同板块的涨跌幅限制）
        if stock.startswith('68') or stock.startswith('3'):
            limit_rate = 0.2  # 科创板和创业板
        else:
            limit_rate = 0.1  # 主板
        
        limit_price = last_close * (1 + limit_rate)
        
        # 考虑价格精度
        if stock.endswith('.SS') or stock.endswith('.SZ'):
            # 股票价格精度为小数点后2位
            limit_price = round(limit_price, 2)
        
        return current_price >= limit_price * 0.999  # 考虑微小误差
        
    except Exception as e:
        log.error(f"检查涨停时出错: {e}")
        return False

# 持仓信息打印函数
def print_position_info(context):
    """
    打印持仓信息
    """
    log.info("=" * 50)
    log.info(f"持仓信息 - {context.blotter.current_dt}")
    log.info(f"总资产: {context.portfolio.portfolio_value:.2f}")
    log.info(f"可用资金: {context.portfolio.cash:.2f}")
    
    positions = get_positions()
    if positions:
        for stock, position in positions.items():
            log.info(f"股票: {stock}, 持仓: {position.amount}, 市值: {position.market_value:.2f}, "
                    f"成本: {position.cost_basis:.2f}, 盈亏: {position.pnl:.2f}")
    else:
        log.info("当前无持仓")
    log.info("=" * 50)
#####################################################
"""
MACD金叉plus流通小市值选股策略（PTrade国金版）
适配实盘+增强风控
核心优化：连续回撤保护、双止盈、市价买入、大盘过滤
"""

def initialize(context):
    """初始化函数，回测/实盘仅执行1次"""
    # ========== 基础配置 ==========
    # 设置基准指数为沪深300
    set_benchmark('000300.SS')  # PTrade使用.SS后缀
    
    # 设置滑点（回测专用，实盘无效）
    if not is_trade():
        set_slippage(slippage=0.001)  # 0.1%滑点
        # 设置交易成本（回测专用）
        set_commission(commission_ratio=0.0003, min_commission=5.0)
    
    # ========== 原策略核心参数 ==========
    g.stop_loss = -0.07  # 止损阈值：亏损7%
    g.max_stocks = 3  # 最多持有3只
    g.stock_list = []  # 选股结果存储
    
    # MACD参数（经典12,26,9）
    g.macd_short = 12
    g.macd_long = 26
    g.macd_signal = 9

    # ========== 实盘优化新增参数 ==========
    g.take_profit_base = 0.15  # 保底止盈：盈利15%
    g.take_profit_target = 0.3  # 目标止盈：盈利30%
    g.max_loss_streak = 2  # 最大连续亏损轮数
    g.loss_streak = 0  # 连续亏损轮数计数
    g.strategy_pause = False  # 策略暂停标记
    g.last_batch_profit = 0  # 上一轮调仓盈亏
    g.index_filter = '000300.SS'  # 大盘过滤标的：沪深300
    g.index_ma_period = 20  # 大盘过滤周期：20日线
    g.take_profit_half_done = {}  # 记录是否已执行过半止盈
    
    # 初始化周几标记（用于模拟run_weekly）
    g.last_select_weekday = -1  # 上次选股的星期几
    g.last_trade_weekday = -1  # 上次交易的星期几
    
    # 设置股票池（初始为空，后续动态更新）
    set_universe([])
    
    log.info("策略初始化完成")


def before_trading_start(context, data):
    """每日盘前运行：执行选股逻辑（周二盘前执行，使用周一收盘数据）"""
    # 获取当前是星期几（1=周一, 2=周二, ..., 5=周五）
    current_weekday = context.blotter.current_dt.isoweekday()
    current_date = context.blotter.current_dt.strftime('%Y-%m-%d')
    
    # 周二盘前执行选股（相当于周一收盘后选股）
    if current_weekday == 2 and g.last_select_weekday != 2:
        log.info(f"========== {current_date} 周二盘前选股 ==========")
        get_stock_list(context)
        g.last_select_weekday = 2


def handle_data(context, data):
    """盘中运行：执行交易逻辑（周二开盘交易）+ 止盈止损检查"""
    # 获取当前是星期几
    current_weekday = context.blotter.current_dt.isoweekday()
    current_time = context.blotter.current_dt
    current_date = current_time.strftime('%Y-%m-%d')
    current_hour = current_time.hour
    current_minute = current_time.minute
    
    # ========== 周二开盘交易（仅执行一次）==========
    # 判断是否为周二且是开盘后第一分钟
    is_opening_time = False
    if not is_trade():  # 回测场景：9:31分
        is_opening_time = (current_hour == 9 and current_minute == 31)
    else:  # 实盘场景：9:30分
        is_opening_time = (current_hour == 9 and current_minute == 30)
    
    if current_weekday == 2 and is_opening_time and g.last_trade_weekday != 2:
        log.info(f"========== {current_date} 周二开盘交易 ==========")
        trade(context)
        g.last_trade_weekday = 2
        # 重置半止盈状态（新调仓周期开始）
        g.take_profit_half_done = {}
    
    # 每日重置周几标记（避免一周内重复执行）
    if current_weekday != 2:
        g.last_trade_weekday = -1
        g.last_select_weekday = -1
    
    # ========== 盘中止盈止损检查（每分钟执行）==========
    check_stop_loss_and_take_profit(context, data)


def get_stock_list(context):
    """选股函数：MACD金叉+小市值+大盘过滤+连续亏损保护"""
    # 1. 策略暂停判断
    if g.strategy_pause:
        log.info("策略暂停：连续亏损达标/大盘破位，本周不选股")
        g.strategy_pause = False  # 暂停一周后自动恢复
        g.stock_list = []
        set_universe([])
        return
    
    # 2. 大盘过滤：沪深300跌破20日线，暂停选股
    try:
        current_date = context.blotter.current_dt.strftime('%Y%m%d')
        # 获取沪深300最近21天数据（计算20日均线需要20+1天）
        index_data = get_history(
            count=g.index_ma_period + 1,
            frequency='1d',
            field='close',
            security_list=g.index_filter,
            fq=None,
            include=False
        )
        
        if len(index_data) >= g.index_ma_period:
            # 计算20日均线
            close_values = index_data['close'].values
            ma20 = close_values[-g.index_ma_period:].mean()
            current_close = close_values[-1]
            
            if current_close < ma20:
                log.info(f"沪深300跌破20日线，本周不选股（收盘价：{current_close:.2f}, 20日线：{ma20:.2f}）")
                g.stock_list = []
                set_universe([])
                return
    except Exception as e:
        log.error(f"大盘过滤出错：{e}")
    
    # 3. 获取所有A股
    current_date = context.blotter.current_dt.strftime('%Y%m%d')
    all_stocks = get_Ashares(date=current_date)
    
    # 过滤科创板(688开头)、北交所(8/4开头)
    all_stocks = [stock for stock in all_stocks 
                if not (stock.startswith('688') or stock.startswith('8') or stock.startswith('4'))]
    
    # 过滤次新股（上市不满1年）
    all_stocks = filter_new_stock(context, all_stocks)
    
    # 过滤ST股票
    all_stocks = filter_st_stock(all_stocks)
    
    # 过滤停牌股票
    all_stocks = paused_filter(context, all_stocks)
    
    log.info(f"过滤后剩余股票数量：{len(all_stocks)}")
    
    # 4. MACD金叉筛选
    candidates = []  # 技术面达标池
    for stock in all_stocks:
        try:
            # 获取过去30天日线数据（确保MACD计算准确）
            df = get_history(
                count=30,
                frequency='1d',
                field=['close', 'high', 'low'],
                security_list=stock,
                fq='pre',  # 前复权
                include=False
            )
            
            if len(df) < 30:  # 数据不足跳过
                continue
            
            # 获取收盘价数组
            close_array = df['close'].values
            
            # 过滤过度炒作：过去10天涨停≤3次
            if len(close_array) >= 10:
                last_10_close = close_array[-10:]
                last_10_pre = close_array[-11:-1]
                limit_up_count = ((last_10_close / last_10_pre - 1) >= 0.099).sum()
                if limit_up_count > 3:
                    continue
            
            # 计算MACD
            # EMA短周期
            ema_short = calculate_ema(close_array, g.macd_short)
            # EMA长周期
            ema_long = calculate_ema(close_array, g.macd_long)
            # DIF
            dif = ema_short - ema_long
            # DEA（DIF的EMA）
            dea = calculate_ema(dif, g.macd_signal)
            
            # 判断MACD金叉：昨日DIF<DEA，今日DIF>DEA
            if len(dif) >= 2 and len(dea) >= 2:
                if dif[-2] < dea[-2] and dif[-1] > dea[-1]:
                    candidates.append(stock)
                    
        except Exception as e:
            # 出错则跳过该股票
            pass
    
    log.info(f"技术面筛选：MACD金叉股票数量 = {len(candidates)}")
    
    if not candidates:  # 无金叉标的
        g.stock_list = []
        set_universe([])
        return
    
    # 5. 基本面筛选：流通市值从小到大选3只
    # 【修复点】字段名改为 float_value（A股流通市值）
    try:
        final_stocks_data = get_fundamentals(
            candidates,
            'valuation',
            fields=['float_value'],  # 修正：使用正确的字段名
            date=current_date
        )
        
        if final_stocks_data is not None and not final_stocks_data.empty:
            # 按流通市值升序排序，取前3只
            final_stocks_data_sorted = final_stocks_data.sort_values('float_value')
            final_stocks = final_stocks_data_sorted.index.tolist()[:g.max_stocks]
            
            log.info(f"基本面筛选：市值最小的{g.max_stocks}只股票")
            log.info(final_stocks)
            g.stock_list = final_stocks
            set_universe(final_stocks)
        else:
            log.info("获取估值数据失败，本周不选股")
            g.stock_list = []
            set_universe([])
    except Exception as e:
        log.error(f"基本面筛选出错：{e}")
        g.stock_list = []
        set_universe([])


def trade(context):
    """每周二开盘交易：调仓+批次盈亏统计"""
    final_stocks = g.stock_list
    
    if not final_stocks:
        log.info("无选股结果，本周不调仓")
        # 但要清仓旧持仓
        for stock in list(context.portfolio.positions.keys()):
            log.info(f"清仓旧持仓: {stock}")
            order_target(stock, 0)
        return
    
    # 记录调仓前总资产（用于计算本批次盈亏）
    pre_total_asset = context.portfolio.portfolio_value
    
    # 执行调仓
    adjust_positions(context, final_stocks)
    
    # 记录调仓后总资产
    post_total_asset = context.portfolio.portfolio_value
    g.last_batch_profit = post_total_asset - pre_total_asset
    log.info(f"调仓完成，调仓前资产：{pre_total_asset:.2f}，调仓后资产：{post_total_asset:.2f}")


def adjust_positions(context, final_stocks):
    """调仓核心：等权分配，市价单买入"""
    if not final_stocks:
        # 无选股结果，清仓所有持仓
        for stock in list(context.portfolio.positions.keys()):
            log.info(f"无新选股，清仓旧持仓: {stock}")
            order_target(stock, 0)
        return
    
    # 1. 计算每只股票的目标持仓金额
    total_value = context.portfolio.portfolio_value
    # 等权分配，预留2%现金应对手续费和价格波动
    target_value_per_stock = total_value * 0.98 / len(final_stocks)
    log.info(f"开始调仓，总资产: {total_value:.2f}, 每只股票目标金额: {target_value_per_stock:.2f}")
    
    # 2. 卖旧：清仓不在新选股列表中的股票
    for stock in list(context.portfolio.positions.keys()):
        if stock not in final_stocks:
            log.info(f"卖出旧持仓: {stock}")
            order_target(stock, 0)
    
    # 3. 买新：为新选股列表中的每只股票设置目标金额
    for stock in final_stocks:
        try:
            # PTrade使用order_target_value进行等金额买入
            # 实盘场景：不传limit_price时，系统会用最新价报单
            # 回测场景：自动按回测价格成交
            log.info(f"为 {stock} 设置目标金额 {target_value_per_stock:.2f}，市价买入")
            order_target_value(stock, target_value_per_stock)
        except Exception as e:
            log.error(f"买入 {stock} 失败：{e}")


def check_stop_loss_and_take_profit(context, data):
    """盘中止盈止损：止损7% + 保底止盈15% + 目标止盈30% + 连续亏损统计"""
    # 无持仓，不检查
    positions = context.portfolio.positions
    if not positions:
        return
    
    # 遍历持仓个股
    current_profit = 0  # 本批次当前总盈亏
    
    for stock in list(positions.keys()):
        try:
            position = positions[stock]
            
            # 获取当前价格
            if is_trade():
                # 实盘：使用get_snapshot获取最新价
                snapshot = get_snapshot(stock)
                if snapshot and stock in snapshot:
                    current_price = snapshot[stock].get('last_px', 0)
                else:
                    continue
            else:
                # 回测：使用data对象
                current_price = data[stock].price
            
            # 计算盈亏比
            cost_price = position.cost_basis
            if cost_price <= 0:
                continue
            
            profit_loss = (current_price - cost_price) / cost_price
            single_profit = (current_price - cost_price) * position.amount
            current_profit += single_profit
            
            # 1. 止损：亏损7%清仓
            if profit_loss <= g.stop_loss:
                log.info(f"触发止损: {stock}, 盈亏比: {profit_loss * 100:.2f}%, 清仓")
                order_target(stock, 0)
                # 重置半止盈状态
                if stock in g.take_profit_half_done:
                    del g.take_profit_half_done[stock]
                continue
            
            # 2. 目标止盈：盈利30%，全部清仓
            if profit_loss >= g.take_profit_target:
                log.info(f"触发目标止盈（30%）：{stock}, 盈亏比 {profit_loss * 100:.2f}%, 全部清仓")
                order_target(stock, 0)
                # 重置半止盈状态
                if stock in g.take_profit_half_done:
                    del g.take_profit_half_done[stock]
                continue
            
            # 3. 保底止盈：盈利15%，且尚未执行过半止盈，则清仓一半
            if profit_loss >= g.take_profit_base and stock not in g.take_profit_half_done:
                log.info(f"触发保底止盈（15%）：{stock}, 盈亏比 {profit_loss * 100:.2f}%, 清仓一半")
                target_amount = int(position.amount / 2)
                order_target(stock, target_amount)
                # 标记为已执行过半止盈
                g.take_profit_half_done[stock] = True
                
        except Exception as e:
            log.error(f"处理 {stock} 止盈止损时出错：{e}")
    
    # 4. 批次盈亏统计+连续亏损判断（持仓全部清空时触发）
    if not context.portfolio.positions:
        g.last_batch_profit = current_profit
        
        if g.last_batch_profit < 0:  # 本批次亏损
            g.loss_streak += 1
            log.info(f"本批次亏损 {abs(g.last_batch_profit):.2f} 元，连续亏损 {g.loss_streak} 轮")
            
            if g.loss_streak >= g.max_loss_streak:
                log.info(f"连续亏损 {g.max_loss_streak} 轮，触发策略暂停1周")
                g.strategy_pause = True
                g.loss_streak = 0
        else:  # 本批次盈利
            if g.last_batch_profit > 0:
                log.info(f"本批次盈利 {g.last_batch_profit:.2f} 元，连续亏损计数重置为0")
            g.loss_streak = 0
        
        # 重置半止盈状态
        g.take_profit_half_done = {}


def after_trading_end(context, data):
    """盘后运行：输出持仓情况"""
    # 输出当日持仓情况
    if context.portfolio.positions:
        log.info(f"========== 盘后持仓情况 ==========")
        for stock, position in context.portfolio.positions.items():
            profit_loss = (position.last_sale_price - position.cost_basis) / position.cost_basis
            log.info(f"{stock}: 持仓 {position.amount} 股, 成本 {position.cost_basis:.2f}, "
                    f"现价 {position.last_sale_price:.2f}, 盈亏比 {profit_loss * 100:.2f}%")
    else:
        log.info("当前无持仓")


# ========== 辅助函数 ==========

def calculate_ema(data, period):
    """计算EMA指数移动平均"""
    import numpy as np
    ema = np.zeros(len(data))
    # EMA的平滑系数
    multiplier = 2.0 / (period + 1)
    
    # 第一个EMA值用SMA
    ema[0] = data[0]
    
    # 后续EMA递推计算
    for i in range(1, len(data)):
        ema[i] = (data[i] - ema[i-1]) * multiplier + ema[i-1]
    
    return ema


def paused_filter(context, security_list):
    """过滤停牌股票"""
    # 回测场景：使用get_stock_status
    if not is_trade():
        try:
            halt_status = get_stock_status(security_list, 'HALT')
            if halt_status:
                return [stock for stock in security_list if halt_status.get(stock) is not True]
            return security_list
        except:
            return security_list
    
    # 实盘场景：使用get_snapshot判断交易状态
    try:
        snapshot = get_snapshot(security_list)
        if snapshot:
            return [stock for stock in security_list 
                    if stock in snapshot and snapshot[stock].get('trade_status') not in ['HALT', 'SUSP', 'STOPT', 'DELISTED']]
        return security_list
    except:
        return security_list


def filter_st_stock(stock_list):
    """过滤ST/*ST/退市股"""
    try:
        # 使用PTrade的get_stock_status判断ST状态
        st_status = get_stock_status(stock_list, 'ST')
        if st_status:
            # 过滤掉ST股票
            filtered = [stock for stock in stock_list if st_status.get(stock) is not True]
            return filtered
        return stock_list
    except Exception as e:
        log.error(f"过滤ST股票出错：{e}")
        return stock_list


def filter_new_stock(context, stock_list):
    """过滤上市不满1年次新股"""
    try:
        import datetime
        current_date = context.blotter.current_dt.date()
        filtered = []
        
        for stock in stock_list:
            # 获取股票基础信息
            stock_info = get_stock_info(stock, field=['listed_date'])
            if stock_info and stock in stock_info:
                listed_date_str = stock_info[stock].get('listed_date')
                if listed_date_str:
                    # 转换上市日期字符串为日期对象
                    listed_date = datetime.datetime.strptime(listed_date_str, '%Y-%m-%d').date()
                    # 判断是否上市超过375天（约1年）
                    if (current_date - listed_date).days > 375:
                        filtered.append(stock)
        
        return filtered
    except Exception as e:
        log.error(f"过滤次新股出错：{e}")
        return stock_list
#################################
# -*- coding: utf-8 -*-

from __future__ import print_function
from datetime import datetime, timedelta
import pandas as pd

# --- 全局参数设置 ---
g = {
    'take_profit': 0.3,          # 止盈比例：30%
    'stop_loss': -0.07,          # 止损比例：-7%
    'max_stocks': 3,             # 最大持仓数量
    'benchmark': '000300.SH'     # 基准指数：沪深300
}

# --- 策略初始化 ---
def initialize(context):
    """
    策略初始化函数，在回测或实时交易开始时运行一次。
    """
    # 设置基准
    set_benchmark('000300.SS')
    
    # 定义定时任务
    # 每日10:30执行选股和交易逻辑
    # context 参数必须在第一个位置
    run_daily(context, select_and_trade, time='10:30') 
    
    # 每日收盘后执行止盈止损检查
    # 在 initialize 函数中
    run_daily(context, check_stop_loss_and_take_profit, time='15:00')
    
    log.info("策略初始化完成")


# --- 核心逻辑函数 ---

def select_and_trade(context):
    """
    选股并执行交易的核心函数。
    """
    log.info("开始执行选股逻辑...")
    
    # 1. 获取初始股票池
    # 在 select_and_trade 函数中
    
    # 在 select_and_trade 函数中
    # 在 select_and_trade 函数中

    # 1. 分别获取上交所和深交所的股票列表
    all_stocks = get_index_stocks('000985.SS')
    
    
    # 2. 应用一系列过滤器
    filtered_stocks = all_stocks
    filtered_stocks = filter_kcb_bse_stock(filtered_stocks)
    filtered_stocks = filter_st_stock(context, filtered_stocks)
    filtered_stocks = filter_new_stock(context, filtered_stocks)
    filtered_stocks = filter_paused_stock(context, filtered_stocks)
    
    log.info(f"基础过滤后剩余股票: {len(filtered_stocks)} 只")
    
    # 3. 技术指标筛选
    candidates = []
    for stock in filtered_stocks:
        try:
            # 获取过去20天的日线数据以计算指标
            hist_data = attribute_history(stock, 20, '1d', ['open', 'close', 'high', 'low', 'pre_close'], df=True)
            if len(hist_data) < 20:
                continue
            
            # 检查过去10天涨停次数
            limit_up_count = ((hist_data['close'] / hist_data['pre_close'] - 1) >= 0.099).sum()
            if limit_up_count > 3:
                continue
            
            # 计算布林带指标
            ma20 = hist_data['close'].mean()
            std20 = hist_data['close'].std()
            up_band = ma20 + 2 * std20
            down_band = ma20 - 2 * std20
            
            # 获取昨天和今天的价格
            t1_close = hist_data['close'][-2]
            current_price = get_ticks(stock, end_dt=context.current_dt, fields=['time', 'price'], count=1)[0]['price']
            
            # 布林带条件：今日股价跌破下轨，昨日收盘价在中下轨之间
            boll_condition = (current_price < down_band) and (t1_close > down_band)
            
            # 计算MACD指标
            ema_short = hist_data['close'].ewm(span=12, adjust=False).mean()
            ema_long = hist_data['close'].ewm(span=26, adjust=False).mean()
            dif = ema_short - ema_long
            dea = dif.ewm(span=9, adjust=False).mean()
            
            # MACD金叉条件
            macd_gold_cross = (dif.iloc[-2] < dea.iloc[-2]) and (dif.iloc[-1] > dea.iloc[-1])
            
            if boll_condition and macd_gold_cross:
                candidates.append(stock)
        except Exception as e:
            log.warn(f"处理股票 {stock} 时出错: {e}")
    
    log.info(f"技术指标筛选后剩余股票: {len(candidates)} 只")
    
    # 4. 按流通市值排序，选择市值最小的N只
    if not candidates:
        log.warn("未选出任何符合条件的股票，清仓所有持仓。")
        adjust_positions(context, [])
        return
        
    # 获取候选股票的最新基本面数据
    q = query(
        fundamentals.valuation.code,
        fundamentals.valuation.circulating_market_cap
    ).filter(
        fundamentals.valuation.code.in_(candidates)
    ).order_by(
        fundamentals.valuation.circulating_market_cap.asc()
    ).limit(g['max_stocks'])
    
    fund_data = get_fundamentals(q)
    final_stocks = fund_data['code'].tolist()
    
    log.info(f"最终选定股票: {final_stocks}")
    
    # 5. 调整持仓
    adjust_positions(context, final_stocks)


def adjust_positions(context, final_stocks):
    """
    根据选股结果调整持仓。
    """
    current_positions = list(context.portfolio.positions.keys())
    
    # 卖出持仓中不在最终列表的股票
    for stock in current_positions:
        if stock not in final_stocks:
            log.info(f"卖出股票: {stock}")
            order_target(stock, 0)
    
    # 买入新选出的股票，等权分配资金
    if not final_stocks:
        return
        
    # 计算每只股票的目标权重
    target_weight = 1.0 / len(final_stocks)
    
    # 获取当前可用资金
    available_cash = context.portfolio.cash
    
    # 获取当前总资产
    total_value = context.portfolio.total_value
    
    for stock in final_stocks:
        # 计算目标持仓价值
        target_value = total_value * target_weight
        # 计算当前持仓价值
        current_value = context.portfolio.positions.get(stock, 0).total_amount
        
        if target_value > current_value:
            # 需要买入
            order_value(stock, target_value - current_value)
            log.info(f"买入股票: {stock}, 目标价值: {target_value:.2f}")
        # 如果目标价值小于等于当前价值，不执行操作，以避免频繁交易


def check_stop_loss_and_take_profit(context):
    """
    检查持仓股票是否达到止盈止损条件。
    """
    log.info("开始执行止盈止损检查...")
    for stock in context.portfolio.positions:
        position = context.portfolio.positions[stock]
        # 获取持仓成本价
        cost_price = position.avg_cost
        # 获取当前最新价
        current_price = get_ticks(stock, end_dt=context.current_dt, fields=['price'], count=1)[0]['price']
        
        # 计算盈亏比例
        profit_loss_ratio = (current_price - cost_price) / cost_price
        
        # 检查止盈条件
        if profit_loss_ratio >= g['take_profit']:
            log.info(f"触发止盈: {stock}, 盈亏比: {profit_loss_ratio:.2%}, 清仓。")
            order_target(stock, 0)
        # 检查止损条件
        elif profit_loss_ratio <= g['stop_loss']:
            log.info(f"触发止损: {stock}, 盈亏比: {profit_loss_ratio:.2%}, 清仓。")
            order_target(stock, 0)


# --- 辅助过滤函数 ---

def filter_kcb_bse_stock(stock_list):
    """过滤科创板和北交所股票"""
    return [stock for stock in stock_list if not (stock.startswith('688') or stock.startswith('8') or stock.startswith('4'))]

def filter_st_stock(context, stock_list):
    """过滤ST、*ST及退市股票"""
    current_data = get_current_data()
    return [stock for stock in stock_list if not (
        current_data[stock].is_st or 
        'ST' in current_data[stock].name or 
        '*' in current_data[stock].name or 
        '退' in current_data[stock].name
    )]

def filter_new_stock(context, stock_list):
    """过滤上市不满一年的次新股"""
    # 获取上一个交易日
    yesterday = context.previous_date
    return [stock for stock in stock_list if (yesterday - get_security_info(stock).start_date) >= timedelta(days=365)]

def filter_paused_stock(context, stock_list):
    """过滤停牌股票"""
    current_data = get_current_data()
    return [stock for stock in stock_list if not current_data[stock].paused]
##########################################
"""
MACD+布林策略 (适配Ptrade平台)
策略逻辑：MACD金叉 + 布林带下轨反转 + 小市值选股
"""

# 1. [修改] 导入Ptrade的API库，替换聚宽的 jqdata
from ptrade import *
import pandas as pd
import numpy as np

def initialize(context):
    """
    初始化函数
    """
    # [修改] 设置基准指数，Ptrade使用 '000300.SS'
    set_benchmark('000300.SS')
    
    # [修改] 日志级别设置，Ptrade使用 log.setLevel()
    # 可选级别: log.DEBUG, log.INFO, log.WARN, log.ERROR, log.CRITICAL
    log.setLevel(log.INFO)
    
    # [修改] 定时任务，Ptrade的时间格式为 'HH:MM'
    run_daily(select_and_trade, time='10:30')
    
    # [修改] 定时任务，Ptrade中没有 'every_bar'，使用 '1m' 模拟，实现分钟级监控
    run_daily(check_stop_loss_and_take_profit, time='1m')

    # 全局变量定义
    g.take_profit = 0.3      # 止盈：盈利30%
    g.stop_loss = -0.07      # 止损：跌幅7%
    g.max_stocks = 3         # 最多持有股票数
    # 布林带参数
    g.boll_window = 20
    g.boll_std = 2

def select_and_trade(context):
    """
    每日10:30选股并调整持仓
    """
    # [修改] 获取所有A股，Ptrade使用 get_instruments()
    all_stocks = get_instruments('stock', date=context.now)
    # 过滤科创板(688)和北交所(8,4)
    all_stocks = [stock for stock in all_stocks if not (stock.startswith('688') or stock.startswith('8') or stock.startswith('4'))]
    
    # 应用过滤函数
    all_stocks = filter_new_stock(context, all_stocks)
    all_stocks = filter_st_stock(context, all_stocks) # [修改] 函数签名增加context
    all_stocks = paused_filter(context, all_stocks)
    
    candidates = []
    # [修改] Ptrade的get_price一次性获取所有股票数据，效率更高
    # 计算技术指标需要至少21天数据
    price_df = get_price(all_stocks, count=21, end_date=context.now, frequency='daily', fields=['open', 'close', 'high', 'low', 'pre_close'])

    for stock in all_stocks:
        try:
            # 从DataFrame中提取单只股票的数据
            df = price_df[price_df['code'] == stock]
            if len(df) < 21:
                continue
            
            # 检查过去10天涨停次数
            limit_up_count = ((df['close'] / df['pre_close'] - 1) >= 0.099).sum()
            if limit_up_count > 3:
                continue
            
            # 计算布林带
            df['ma20'] = df['close'].rolling(window=g.boll_window).mean()
            df['std'] = df['close'].rolling(window=g.boll_window).std()
            df['up'] = df['ma20'] + g.boll_std * df['std']
            df['down'] = df['ma20'] - g.boll_std * df['std']
            
            # 获取昨天和今天的数据点
            t1_data = df.iloc[-2] # T-1 天
            current_price = get_ticks(stock, count=1, fields='last_price')[stock]['last_price']
            
            # 布林带反转条件：昨收在中轨上，今开在中轨下
            boli_true = current_price < t1_data['down'] and t1_data['close'] > t1_data['down']
            if not boli_true:
                continue

            # 计算MACD
            short_window = 12
            long_window = 26
            signal_window = 9
            df['ema_short'] = df['close'].ewm(span=short_window, adjust=False).mean()
            df['ema_long'] = df['close'].ewm(span=long_window, adjust=False).mean()
            df['dif'] = df['ema_short'] - df['ema_long']
            df['dea'] = df['dif'].ewm(span=signal_window, adjust=False).mean()

            # 判断MACD金叉 (T-1日死叉，T日金叉)
            if df['dif'].iloc[-2] < df['dea'].iloc[-2] and df['dif'].iloc[-1] > df['dea'].iloc[-1]:
                candidates.append(stock)
        except Exception as e:
            log.error(f"处理股票 {stock} 时出错: {e}")
            
    log.info(f"------------金叉选股 全股----------- {candidates}")
    
    if not candidates:
        log.info("没有选出符合条件的股票，清空所有持仓。")
        for stock in context.portfolio.positions:
            order_target(stock, 0)
        return

    # [修改] 获取基本面数据，Ptrade的 get_fundamentals 用法不同
    q = query(
        fundamentals.valuation.code,
        fundamentals.valuation.circulating_market_cap
    ).filter(
        fundamentals.valuation.code.in_(candidates)
    ).order_by(
        fundamentals.valuation.circulating_market_cap.asc()
    ).limit(g.max_stocks)
    
    final_stocks_df = get_fundamentals(q, date=context.now)
    final_stocks = final_stocks_df['code'].tolist()
    
    log.info(f"------------选3只市值最小----------- {final_stocks}")

    # 调整持仓
    adjust_positions(context, final_stocks)

def adjust_positions(context, final_stocks):
    """
    调整持仓到选定股票
    """
    # [修改] 获取当前持仓，Ptrade的结构略有不同
    current_positions = [position.sid for position in context.portfolio.positions.values() if position.total_amount > 0]

    # 卖出不在选股列表中的股票
    for stock in current_positions:
        if stock not in final_stocks:
            order_target(stock, 0)

    # 平均分配资金到新选定的股票
    # [修改] 计算可用资金时，需要考虑已下单但未成交的部分
    available_cash = context.portfolio.cash
    if final_stocks:
        # 计算需要买入的新股票数量
        new_stocks_to_buy = [stock for stock in final_stocks if stock not in current_positions]
        if new_stocks_to_buy:
            weight = 1.0 / len(final_stocks)
            total_value_to_allocate = context.portfolio.total_value * weight
            
            for stock in new_stocks_to_buy:
                # 计算目标市值，避免超买
                current_value = context.portfolio.positions.get(stock, 0)
                if current_value:
                    current_value = current_value.total_amount * current_value.last_price
                target_value = total_value_to_allocate - current_value
                if target_value > 0:
                    order_target_value(stock, total_value_to_allocate)

def check_stop_loss_and_take_profit(context):
    """
    检查持仓股票是否达到止盈止损条件
    """
    # [修改] 遍历持仓的方式
    positions = context.portfolio.positions
    for stock, position in positions.items():
        if position.total_amount <= 0:
            continue
            
        # [修改] 获取当前价格，Ptrade使用 get_ticks 或 get_price
        current_price = get_ticks(stock, count=1, fields='last_price')[stock]['last_price']
        cost_price = position.avg_cost
        profit_loss = (current_price - cost_price) / cost_price

        # 止盈条件
        if profit_loss >= g.take_profit:
            log.info(f"止盈触发: {stock}, 收益率: {profit_loss:.2%}")
            order_target(stock, 0)

        # 止损条件
        if profit_loss <= g.stop_loss:
            log.info(f"止损触发: {stock}, 收益率: {profit_loss:.2%}")
            order_target(stock, 0)

## [修改] 过滤函数的适配
def paused_filter(context, security_list):
    """过滤停牌股票"""
    # [修改] Ptrade没有直接获取停牌状态的函数，用get_price判断
    # 这是一个常用的替代方法
    current_prices = get_price(security_list, count=1, end_date=context.now, frequency='daily', fields='close')
    return [stock for stock in security_list if not current_prices[current_prices['code'] == stock]['close'].isna().any()]
    
def filter_st_stock(context, stock_list):
    """过滤ST及退市风险股票"""
    # [修改] Ptrade通过 get_instruments 获取详细信息
    instruments_info = get_instruments(stock_list, date=context.now, fields=['listed_date', 'name'])
    return [info['code'] for info in instruments_info if 
            'ST' not in info['name'] and 
            '*' not in info['name'] and 
            '退' not in info['name']]

def filter_new_stock(context, stock_list):
    """过滤次新股（上市不足375天）"""
    # [修改] Ptrade通过 get_instruments 获取上市日期
    instruments_info = get_instruments(stock_list, date=context.now, fields=['listed_date'])
    yesterday = context.now.date() - datetime.timedelta(days=1)
    return [info['code'] for info in instruments_info if 
            (yesterday - pd.to_datetime(info['listed_date']).date()).days >= 375]
###################################################
#导入函数库 3.11版本  #0406
import numpy as np
import pandas as pd
import time
import pickle
import ast
from datetime import datetime
from datetime import timedelta
import json

NOTEBOOK_PATH=''
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('expand_frame_repr', False)

def initialize(context):
    # 设定基准为沪深300指数
    set_benchmark('000300.SS')
    NOTEBOOK_PATH = get_research_path()#+'xsz/'#'/home/fly/notebook/'
    #g.risk_idx = "399101.XBHS"         #'000985.XBHS'中证全指、'399101.XBHS'中小综指
    g.risk_idx = "000985.XBHS"
    #g.risk_idx = "399006.XBHS"         #"399006.XBHS" 创业板指
    #g.risk_idx= '516860.XBHS'
    
    # 策略基础配置和状态变量
    g.no_trading_today_signal = True  # 当天是否执行空仓（资金再平衡）操作
    g.pass_april = True               # 是否在04月或01月期间执行空仓策略
    g.run_stoploss = True              # 是否启用止损策略
    # 持仓和调仓记录
    g.hold_list = []                 # 当前持仓股票代码列表
    g.yesterday_HL_list = []         # 昨日涨停的股票列表（收盘价等于涨停价）
    g.target_list = []               # 本次调仓候选股票列表
    g.not_buy_again = []             # 当天已买入的股票列表，避免重复下单
    # 策略交易及风控的参数
    g.stock_num =10               # 每次调仓目标持仓股票数量
    g.up_price = 40                # 股票价格上限过滤条件（排除股价超过此值的股票）
    g.reason_to_sell = ''            # 记录卖出原因（例如：'limitup' 涨停破板 或 'stoploss' 止损）
    g.stoploss_strategy = 3          # 止损策略：1-个股止损；2-大盘止损；3-联合止损策略
    g.stoploss_limit = 0.88          # 个股止损阀值（成本价 × 0.92） 0.88
    g.stoploss_market = 0.97         # 大盘止损参数（若整体跌幅过大则触发卖出）
    g.totalcash = 50000             #策略使用总资金
    
    g.HV_control = False             # 是否启用成交量异常检测
    g.HV_duration = 120              # 检查成交量时参考的历史天数
    g.HV_ratio = 0.9                 # 当天成交量超过历史最高成交量的比例（如0.9即90%）
    
    # 僵尸因子：市值排名rolling过滤参数
    g.enable_rank_filter = False      # 是否启用市值排名rolling过滤
    g.rank_threshold = 2            # 市值排名rolling均值阈值
    g.rank_rolling_days = 30         # rolling窗口天数，只算交易日
    
    # 周线MACD因子
    g.enable_macd_filter = False       # 是否启用周线MACD因子
    
    # 5日/10日量比因子
    g.enable_volume_ratio_filter = True   # 是否启用量比因子
    g.volume_ratio_threshold = 1.0        # 量比阈值
    g.volume_ratio_boost_positions = 8     # 量比优秀股票往前提升的位置数
    
    #代码转换需要加的全局变量
    g.trading_signal = True  # 是否为可交易日
    g.count = 1 #记录交易日
    g.trade_count = 0 #记录交易日
    g.up_tardeday = ''
    
    g.get_finiance = True
    g.start_year = ""
    g.end_year = ""
    
    g.zt = {}
    #清空财务数据表
    #df = pd.DataFrame(columns=['code', 'np_parent_company_owners', 'net_profit', 'operating_revenue','publ_date','end_date','secu_abbr'])
    #df.to_csv('\\finance_data\\output.csv', index=False)
    #持久化，尝试启动pickle文件
    
    if not is_trade():# 如果是回测，则强制初始化count=1和firstcount=0的文件
        with open(NOTEBOOK_PATH+'count.pkl','wb') as f:
            pickle.dump(1,f,-1)
        with open(NOTEBOOK_PATH+'firstcount.pkl','wb') as f:
            pickle.dump(0,f,-1)
    try:# 从文件中读取count和firstcount的值
        with open(NOTEBOOK_PATH+'count.pkl','rb') as f:
            g.count = pickle.load(f)
            log.info("策略重启初始化,从文件中读取本策略当前交易日: %s" % (g.count)) 
        with open(NOTEBOOK_PATH+'firstcount.pkl','rb') as f:
            g.trade_count = pickle.load(f)
            log.info("策略重启初始化,从文件中读取本策略运行第%s个交易日" % (g.trade_count)) 
    except Exception as e:
        log.error("读取count和firstcount文件失败: %s" % (e))
    
    # 设置交易运行时间
    run_daily(context, update_counters, time='9:00')
    run_daily(context, print_position_info, time='9:00')
    # run_daily(context, save_data_local, time='9:00')
    # run_daily(context, prepare, time='9:05')#gai0:这里改到before_trading_start
    
    # 上午交易任务
    run_daily(context, sell_stocks, time='10:00')
    run_daily(context, weekly_adjustment, time='10:30')
    # 下午交易任务
    run_daily(context, trade_afternoon, time='14:30')
    run_daily(context, close_account, time='14:50')
    # 策略维护
    run_daily(context, record_counters, time='14:55')
    # run_daily(context, print_position_info_weekend, time='15:10')
    # if is_trade():#实盘模式增加
    #     run_daily(context, save_data_local, time='15:00')
    if not is_trade():
        set_limit_mode('UNLIMITED')
          
# 1、开盘前准备工作
#@维护周内计数(g.count)和总计数(g.trade_count)
def update_counters(context):
    """
    更新维护周内计数(g.count)和总计数(g.trade_count)
    如果经过假期，或者策略中断，重置g.count为1，否则g.count++
    g.trade_count++
    """
    today = context.blotter.current_dt
    weekdays = today.weekday()+1 #weekday()返回0-6，所以要+1
    current_date = str(get_trading_day()) #返回格式'2025-06-06'
    date_time = datetime.strptime(current_date, "%Y-%m-%d")
    days = 0
    if g.up_tardeday !='':
        date_time_pre = datetime.strptime(g.up_tardeday, "%Y-%m-%d")
        days = (date_time-date_time_pre).days
    else:#策略首次启动或中断后重启，需要重置count计数
        g.count = 1

    if days >1 or weekdays == 1:#距离上次执行超过1天（说明跨周末或假期），或者今天是周一
        g.count = 1
    else:
        if days != 0:
            g.count += 1
    g.up_tardeday = current_date
    g.trade_count += 1

#@打印每只持仓股票的数据。
def print_position_info(context):
    """
    打印每只持仓股票的数据。
    """
    positions = [position.sid for position in context.portfolio.positions.values() if position.amount != 0]
    log.info(f"{'='*50}")
    log.info(f"          {context.blotter.current_dt.strftime('%Y-%m-%d')} 持仓总结")
    log.info(f"{'='*50}")
    if len(positions)==0:
        log.info(f"                    空")
    else:
        for stock in positions:
            position = get_position(stock)
            price = position.last_sale_price
            avg_cost = position.cost_basis
            ret = 100 * (price / avg_cost - 1)
            value = position.amount
            amount = position.amount * price
            print(f"股票: {stock} | 成本价: {avg_cost:.2f} | 现价: {price:.2f} | 涨跌幅: {ret:.2f}% | 市值: {amount:.2f} | 持仓数: {value:.0f}")
    log.info(f"{'='*50}")
    return
def before_trading_start(context, data):
    prepare(context)
#@ 初始化g.zt={}, g.hold_list持仓股票列表, g.yesterday_HL_list昨日涨停持仓, g.no_trading_today_signal空仓日
def prepare(context):
    """
    1、初始化涨停板追踪字典g.zt={}
    2、更新持仓列表g.hold_list：刷新当前实际持仓股票清单
    3、识别涨停股票g.yesterday_HL_list：找出昨日收盘时处于涨停状态的持仓股票
    4、判断交易状态g.no_trading_today_signal：确定当日是否为资金再平衡的空仓日
    """
    g.zt = {}
    # 从当前持仓中提取股票代码，更新持仓列表
    g.hold_list = [position.sid for position in context.portfolio.positions.values() if position.amount != 0]
    if g.hold_list != []:
        # 获取持仓股票昨日数据（包括收盘价、涨停价、跌停价）
        p = get_history(1, frequency="1d", field=['low','open','close','high_limit','volume'], security_list=g.hold_list, fq='dypre', include=False)#gai0：这里pre改成dypre，不影响结果，因为只是判断涨停与否
        up_limit_list = list(p[p['close'] == p['high_limit']]['code'])
        g.yesterday_HL_list = up_limit_list
    else:
        g.yesterday_HL_list = []
    # 根据当前日期判断是否为空仓日（例如04月或01月时资金再平衡）
    g.no_trading_today_signal = today_is_between(context)


# 2、上午交易任务
#@止盈与止损操作
def sell_stocks(context):
    """
    止盈与止损操作：
    根据策略（1: 个股止损；2: 大盘止损；3: 联合策略）判断是否执行卖出操作。
    """
    if g.run_stoploss:
        current_positions = [position.sid for position in context.portfolio.positions.values() if position.amount != 0]
        if g.stoploss_strategy == 1:# 个股止盈或止损判断
            for stock in current_positions:
                position = get_position(stock)
                price = position.last_sale_price
                avg_cost = position.cost_basis
                if price >= avg_cost * 2:
                    close_position(context,stock)
                    log.info(f"股票{stock}清仓，个股止盈。")
                elif price < avg_cost * g.stoploss_limit and price > 0 :
                    close_position(context,stock)
                    log.info(f"股票{stock}清仓，个股止损。")
                    g.reason_to_sell = 'stoploss'
        elif g.stoploss_strategy == 2:# 大盘止损判断，若整体市场跌幅过大则平仓所有股票
            last_trade_day = str(get_trading_day(-1))
            last_trade_day = last_trade_day.replace('-','')
            stock_df = get_price(security=get_index_stocks(g.risk_idx,last_trade_day)
                        ,end_date=last_trade_day, frequency='daily'
                        ,fields=['close', 'open'], count=1)
            # 计算成分股平均涨跌，即指数涨跌幅
            down_ratio = (stock_df['close'] / stock_df['open']).mean()
            if down_ratio <= g.stoploss_market:
                g.reason_to_sell = 'stoploss'
                log.info(f"市场风险（平均跌幅 {down_ratio:.2%}），准备清仓...")
                for stock in current_positions:
                    close_position(context,stock)
                    log.info(f"股票{stock}清仓，大盘止损。")
                
        elif g.stoploss_strategy == 3:# 联合止损策略：结合大盘和个股判断
            last_trade_day = str(get_trading_day(-1))
            last_trade_day = last_trade_day.replace('-','')
            stock_df = get_price(security=get_index_stocks(g.risk_idx,last_trade_day)
                        ,end_date=last_trade_day, frequency='daily'
                        ,fields=['close', 'open'],count=1)#gai:fq从None改成dypre，不影响结果
            # #gai：当天跌幅过大就清仓，不要算昨天的。效果有提升，但是回测太慢
            # stock_list = get_index_stocks('399101.XBHS',last_trade_day)
            # stock_df = get_history(1,'1d',['open'],stock_list,include=True)
            # latest_close = get_history(1, '1m', 'close', stock_list, include=True)
            # stock_df = stock_df.merge(latest_close[['code', 'close']], on='code', how='left')
            # 计算成分股平均涨跌，即指数涨跌幅
            down_ratio = (stock_df['close'] / stock_df['open']).mean()
            if down_ratio <= g.stoploss_market:
                g.reason_to_sell = 'stoploss'
                log.info(f"市场风险（平均跌幅 {down_ratio:.2%}），准备清仓...")
                for stock in current_positions:
                    position = get_position(stock)
                    price = position.last_sale_price
                    avg_cost = position.cost_basis
                    close_position(context,stock)
                    log.critical(f"股票{stock}清仓，大盘止损，持仓收益率{price/avg_cost-1:.2%}。")
            else:
                for stock in current_positions:
                    position = get_position(stock)
                    price = position.last_sale_price
                    avg_cost = position.cost_basis
                    if price < avg_cost * g.stoploss_limit and price > 0:
                        close_position(context,stock)
                        log.critical(f"股票{stock}清仓，个股止损，持仓收益率{price/avg_cost-1:.2%}。")
                        g.reason_to_sell = 'stoploss'
#@每周调仓策略
def weekly_adjustment(context):
    """
    每周调仓策略：
    如果非空仓日，先选股得到目标股票列表，再卖出当前持仓中不在目标列表且昨日未涨停的股票，
    最后买入目标股票，同时记录当天买入情况避免重复下单。

    时机控制：只在策略启动日或每周第2天执行调仓
    智能卖出：保护昨日涨停股票，避免错失涨停后续收益
    资金管理：先卖后买，确保资金合理分配
    实盘适配：为实盘交易增加延时处理
    """
    if not g.no_trading_today_signal:
        log.info(f"当前第{g.trade_count}个交易日，周{g.count}")
        if g.trade_count == 1 or g.count == 2:#策略首次运行，或者每周第2天
            log.info(f"每周调仓，开始...")
            g.not_buy_again = []  # 重置当天已买入记录
            g.target_list = get_stock_list(context)
            # 取目标持仓数以内的股票作为调仓目标
            target_list = g.target_list[:g.stock_num]
            log.info(f"每周调仓目标股票: {target_list}")
            log.info(f"每周调仓，先卖出不在目标中的股票...")
            # 遍历当前持仓，若股票不在目标列表且非昨日涨停，则执行卖出操作
            for stock in g.hold_list:
                position = get_position(stock)
                price = position.last_sale_price
                avg_cost = position.cost_basis
                if stock not in target_list and stock not in g.yesterday_HL_list:
                    log.critical(f"股票{stock}不在调仓目标中，清仓，持仓收益率{price/avg_cost-1:.2%}。")
                    close_position(context,stock)
                else:
                    log.info(f"股票{stock}仍在调仓目标中，继续持有，持仓收益率{price/avg_cost-1:.2%}。")
            if is_trade():
                time.sleep(30)
            log.info(f"每周调仓，买入目标中还未持仓的股票...")
            buy_security(context, target_list)# 对目标股票执行买入操作
            if is_trade():
                time.sleep(30)
            # 更新当天已买入记录，防止重复买入
            check_hold_list = [position.sid for position in context.portfolio.positions.values() if position.amount != 0]
            for stock in check_hold_list:
                if stock not in g.not_buy_again:
                    g.not_buy_again.append(stock)
##@获取市值最小的2*g.stock_num只股票
def get_stock_list(context):
    '''
    股票池：g.risk_idx
    进行过滤
    先选出市值最小的50只股票，再根据市值排名rolling均值进行二次筛选，最后选出市值最小的2 * g.stock_num作为候选池
    '''
    final_list = []
    MKT_index = g.risk_idx #'399101.XBHS'#中小综指
    current_time = context.blotter.current_dt - timedelta(days=1)
    cur_formatted_time = current_time.strftime("%Y%m%d")
    initial_list = filter_stocks(context, get_index_stocks(MKT_index,cur_formatted_time))

    circulating_market_cap_df = get_float_value(context,initial_list)
    if not circulating_market_cap_df.empty:
        sort_df = circulating_market_cap_df.sort_values(by='total_value', ascending=True)#排序
        initial_list = list(sort_df.index)
        final_list = initial_list[:50]  # 限制数据规模，防止一次处理数据过大
        
        # 僵尸因子：按市值排名rolling均值过滤
        if g.enable_rank_filter:
            final_list = filter_by_market_cap_rank_rolling(context, final_list, 
                                                         threshold=g.rank_threshold, 
                                                         rolling_days=g.rank_rolling_days)
        
        # 5日/10日量比因子：筛选量比>=阈值的股票
        if g.enable_volume_ratio_filter:
            final_list = filter_by_volume_ratio(context, final_list, g.volume_ratio_threshold)
        
        # 周线MACD因子：筛选上周MACD>0的股票
        if g.enable_macd_filter:
            final_list = filter_by_weekly_macd(context, final_list)
        
        #hold_list = [position.sid for position in context.portfolio.positions.values() if position.amount != 0]
        # 取前2倍目标持仓股票数作为候选池
        final_list = final_list[:2 * g.stock_num]
        log.info(f"初选候选股票: {final_list}")
    return final_list
##@ 过滤股票
def filter_stocks(context, stock_list):
    """
    过滤以下股票：
    1、过滤停牌、退市、ST等有风险的股票
    2、只保留主板
    3、过滤未持仓的涨跌停股票
    4、过滤上市时间不足375天的次新股
    5、过滤名称中包含退市标识的股票
    """
    today = context.blotter.current_dt
    today_str = str(today.strftime("%Y%m%d"))
    yesterday = context.blotter.current_dt - timedelta(days=1)
    yesterday_str = yesterday.strftime("%Y%m%d")
    position_list = [position.sid for position in context.portfolio.positions.values() if position.amount != 0]
    filtered_stocks = []
    halt_status_today = get_stock_status(stock_list, 'HALT',today_str)
    halt_status_yesterday = get_stock_status(stock_list, 'HALT',yesterday_str)
    delisting_status = get_stock_status(stock_list, 'DELISTING',today_str)
    st_status = get_stock_status(stock_list, 'ST',today_str)
    #获取股票信息
    stock_infos = get_stock_info(stock_list, ['stock_name','listed_date','de_listed_date'])
    last_trade_day = get_trading_day(-1)
    for stock in stock_list:
        if is_trade():#gai0：这里改为is_trade()，回测有未来函数
            if '退' in stock_infos[stock]['stock_name'] or 'ST' in stock_infos[stock]['stock_name']: #gai0:这里加上名字st
                continue
        if halt_status_yesterday[stock]:
            continue
        if halt_status_today[stock]:  # 停牌
            continue
        if st_status[stock]:  # ST
            continue
        if delisting_status[stock]:  # 退市
            continue
        # if not (stock.startswith('00') or stock.startswith('60')):  # 非主板
        #     continue
        # if stock.startswith('00') or stock.startswith('60'):  # 主板剔除
        #     continue
        if not (stock in position_list or check_limit(stock)[stock]==0):  # 涨跌停 #gai0：这里看文档，有未来函数，原来是check_limit(stock)[stock]
            continue
        if 'listed_date' in stock_infos[stock]:# 过滤上市天数少于375天的股票
            listed_date_str = stock_infos[stock]['listed_date']
            listed_date = datetime.strptime(listed_date_str, '%Y-%m-%d')
            if (last_trade_day-listed_date.date()).days<375:
                continue
        else:
            continue
        filtered_stocks.append(stock)
    return filtered_stocks
##@ 僵尸因子：按市值排名rolling均值过滤股票
def filter_by_market_cap_rank_rolling(context, stock_list, threshold, rolling_days):
    """
    根据市值排名rolling均值过滤股票
    参数:
        stock_list: 待过滤的股票代码列表
        threshold: 市值排名rolling均值阈值，小于此值的股票将被剔除
        rolling_days: rolling窗口天数，默认20个交易日（约一个月）
    返回:
        过滤后的股票代码列表
    """
    if not stock_list:
        return stock_list
    
    filtered_stocks = []
    
    try:
        trading_days = []
        for i in range(rolling_days, 0, -1):# 获取过去rolling_days个交易日的日期
            trade_day = get_trading_day(-i)
            trading_days.append(str(trade_day).replace('-',''))
        
        # # 获取昨日指数成分股作为排名基准池
        # yesterday = context.blotter.current_dt - timedelta(days=1)
        # yesterday_formatted_time = yesterday.strftime("%Y%m%d")
        # index_stocks = get_index_stocks(MKT_index, yesterday_formatted_time)
        
        # 创建DataFrame存储每只股票每天的排名：行是股票，列是交易日
        stock_rankings_df = pd.DataFrame(index=stock_list)
        
        for trade_day in trading_days:
            try:
                daily_market_cap = get_total_value_bydate(context,stock_list,trade_day)# 获取该日期的市值数据
                if not daily_market_cap.empty:
                    # 直接计算市值排名（市值越小，排名数字越小）
                    daily_market_cap['rank'] = daily_market_cap['total_value'].rank(method='min', na_option='keep')
                    # stock_rankings_df有但daily_market_cap没有的填NaN，反之舍弃
                    stock_rankings_df[trade_day] = daily_market_cap['rank'].reindex(stock_rankings_df.index)
                else:
                    log.error(f"获取{trade_day}日市值数据为空")
            except Exception as e:
                log.error(f"计算{trade_day}日市值排名失败: {e}")
        
        # 检查是否有有效的交易日数据
        total_trading_days = len(stock_rankings_df.columns)
        if total_trading_days == 0:
            log.error("没有获取到任何有效的交易日数据，返回原股票列表")
            return stock_list
            
        valid_days_count = stock_rankings_df.count(axis=1)  # 每行非NaN值的数量
        avg_ranks = stock_rankings_df.mean(axis=1)  # 每行的平均值（自动忽略NaN）
        # 数据充足的股票（有效数据>=一半交易日）
        min_required_days = max(1, total_trading_days // 2)  # 至少需要1天数据
        sufficient_data_mask = valid_days_count >= min_required_days
        sufficient_data_stocks = stock_rankings_df.index[sufficient_data_mask]
        # 在数据充足的股票中，筛选平均排名>=阈值的股票
        qualified_mask = avg_ranks[sufficient_data_mask] >= threshold
        qualified_stocks = sufficient_data_stocks[qualified_mask]
        # 数据不足的股票（保守保留）
        insufficient_data_stocks = stock_rankings_df.index[~sufficient_data_mask]
        # 合并结果
        filtered_stocks = list(qualified_stocks) + list(insufficient_data_stocks)
        
        # 日志输出
        for stock in sufficient_data_stocks:
            avg_rank = avg_ranks[stock]
            log.debug(f"股票{stock}排名: {stock_rankings_df.loc[stock]}")
            if avg_rank >= threshold:
                log.info(f"股票{stock}平均排名{avg_rank:.1f}，通过筛选（排名≥{threshold}）")
            else:
                log.info(f"股票{stock}平均排名{avg_rank:.1f}，被剔除（排名<{threshold}，市值排名过于靠前）")
        for stock in insufficient_data_stocks:
            valid_days = valid_days_count[stock]
            log.info(f"股票{stock}数据不足（有效数据{valid_days}天），保留")
        log.info(f"市值排名rolling过滤：原有{len(stock_list)}只股票，过滤后{len(filtered_stocks)}只股票")
    
    except Exception as e:
        log.error(f"市值排名rolling过滤失败: {e}，返回原股票列表")
        return stock_list
    
    return filtered_stocks
##@ 5日/10日量比因子：筛选量比>=阈值的股票
def filter_by_volume_ratio(context, stock_list, threshold):
    """
    根据5日/10日量比调整股票排序，量比>=阈值的股票在原顺序基础上往前提升指定位置
    参数:
        stock_list: 待过滤的股票代码列表
        threshold: 量比阈值，大于等于此值的股票将往前提升位置
    返回:
        调整排序后的股票代码列表
    """
    if not stock_list:
        return stock_list
    volume_boost_stocks = set()# 记录量比>=阈值的股票
    try:
        volume_data = get_history(20, '1d', 'volume', security_list=stock_list, fq='dypre', include=False, fill='pre')
        for stock in stock_list:
            try:
                stock_volume_data = volume_data[volume_data['code'] == stock]
                stock_volume_data = stock_volume_data[stock_volume_data['volume'] > 0]  # 过滤掉成交量为0的数据
                if len(stock_volume_data) < 10:
                    log.debug(f"股票{stock}有效成交量数据不足({len(stock_volume_data)}天)，保持原位置")
                    continue
                volumes = stock_volume_data['volume'].values
                avg_volume_5d = np.mean(volumes[-5:])# 计算5日平均成交量（最近5天）
                avg_volume_10d = np.mean(volumes[-10:])# 计算10日平均成交量（最近10天）
                
                if avg_volume_10d > 0:
                    volume_ratio = avg_volume_5d / avg_volume_10d# 计算量比
                    if volume_ratio >= threshold:
                        volume_boost_stocks.add(stock)
                        log.info(f"股票{stock}量比={volume_ratio:.2f}，将往前提{g.volume_ratio_boost_positions}位（≥{threshold}）")
                else:
                    log.debug(f"股票{stock}10日均量为0，保持原位置")
            except Exception as e:
                log.error(f"计算股票{stock}的量比失败: {e}，保持原位置")
                continue
        
        # 对原列表进行位置调整：量比>=阈值的股票往前提5位
        result_list = stock_list.copy()
        # 从后往前处理，避免索引变化的影响
        i = len(result_list) - 1
        while i>=0:
            stock = result_list[i]
            if stock in volume_boost_stocks:
                # 计算新位置：往前提升指定位置数，但不能超过索引0
                new_position = max(0, i - g.volume_ratio_boost_positions)
                # 移除股票并插入到新位置
                removed_stock = result_list.pop(i)
                result_list.insert(new_position, removed_stock)
                volume_boost_stocks.remove(stock)
            else:
                i = i-1
        # log.info(f"量比调整：原有{len(stock_list)}只股票，{len(volume_boost_stocks)}只股票量比>={threshold}往前提{g.volume_ratio_boost_positions}位")
        log.info(f"量比调整前股票列表：{stock_list}")
        log.info(f"量比调整后股票列表：{result_list}")
        return result_list
        
    except Exception as e:
        log.error(f"量比排序调整失败: {e}，返回原股票列表")
        return stock_list

##@ 周线MACD因子：筛选周线MACD>0的股票
def filter_by_weekly_macd(context, stock_list):
    """
    根据周线MACD指标过滤股票，筛选出周线MACD>0的股票
    参数:
        stock_list: 待过滤的股票代码列表
    返回:
        过滤后的股票代码列表
    """
    if not stock_list:
        return stock_list
    good_stocks = []
    other_stocks = []
    try:
        # 一次性获取所有股票的周线数据
        weekly_data = get_history(36, '1w', 'close', security_list=stock_list, fq='dypre', include=False, fill='pre')
        if weekly_data.empty:
            log.warning(f"无法获取股票的周线数据: {stock_list}")
            return stock_list
        # 获取最新1分钟数据作为本周当前价格
        current_data = get_history(1, '1m', 'close', security_list=stock_list, fq='dypre', include=True)
        for stock in stock_list:# 对每只股票计算MACD
            try:
                stock_data = weekly_data[weekly_data['code'] == stock]
                close_prices = stock_data['close'].values
                
                current_stock_data = current_data[current_data['code'] == stock]
                if not current_stock_data.empty:
                    current_close = current_stock_data['close'].values[0]
                    close_prices = np.append(close_prices, current_close)
                macdDIF_data, macdDEA_data, macd_data = get_MACD(close_prices, 12, 26, 9)
                latest_macd = macd_data[-1]
                if latest_macd > 0:
                    good_stocks.append(stock)
                    log.info(f"股票{stock}周线MACD={latest_macd:.4f}>0，位置提前")
                else:
                    other_stocks.append(stock)
            except Exception as e:
                log.error(f"计算股票{stock}的MACD失败: {e}")
                other_stocks.append(stock)
                continue
        filtered_stocks = good_stocks + other_stocks
        log.info(f"周线MACD过滤：原有{len(stock_list)}只股票，符合标准的有{len(good_stocks)}只排序提前")
    except Exception as e:
        log.error(f"周线MACD过滤失败: {e}，返回原股票列表")
        return stock_list
    return filtered_stocks
    

#@3、下午交易任务：检查是否有因为涨停破板触发的卖出信号；检查账户中是否需要补仓。
def trade_afternoon(context):
    """
    下午交易任务：
    1. 检查是否有因为涨停破板触发的卖出信号；
    2. 如启用了成交量监控，则检测是否有异常成交量；
    3. 检查账户中是否需要补仓。
    """
    if not g.no_trading_today_signal:
        check_continue_limitup(context)
        if g.HV_control:
            check_high_volume(context)
        rebalance_positions(context)    
##@检查昨日处于涨停状态的股票在今天下午是否继续涨停，如没有继续涨停则卖出该股票
def check_continue_limitup(context):
    """
    检查昨日处于涨停状态的股票在当前是否继续涨停。
    如没有继续涨停，则立即卖出该股票，并记录卖出原因为 "limitup"。
    """
    now_time = context.blotter.current_dt
    if g.yesterday_HL_list:
        for stock in g.yesterday_HL_list:
            position = get_position(stock)
            price = position.last_sale_price
            avg_cost = position.cost_basis
            if check_limit(stock)[stock] != 1:#gai0：这里看文档，有未来函数，原来是check_limit(stock)[stock]
                log.critical(f"股票{stock}昨日涨停今日没有继续涨停，触发卖出操作，持仓收益率{price/avg_cost-1:.2%}。")
                close_position(context,stock)
                g.reason_to_sell = 'limitup'
            else:
                log.critical(f"股票{stock}昨日涨停，今日仍维持涨停状态，持仓收益率{price/avg_cost-1:.2%}。")                
##@检查账户中是否因没有继续涨停卖出而需要补仓。
def rebalance_positions(context):
    """
    检查账户资金与持仓数量：
    如果因涨停破板卖出导致持仓不足，则从目标股票中筛选未买入股票，进行补仓操作。
    """
    if g.reason_to_sell == 'limitup':
        g.hold_list = [position.sid for position in context.portfolio.positions.values() if position.amount != 0]
        if len(g.hold_list) < g.stock_num:
            target_list = filter_not_buy_again(g.target_list)
            target_list = target_list[:min(g.stock_num, len(target_list))]
            log.info(f"检测到补仓需求，可用资金 {round(context.portfolio.cash, 2)}，候选补仓股票: {target_list}")
            buy_security(context, target_list)
        g.reason_to_sell = ''
    else:
        log.info("未检测到涨停破板卖出事件，不进行补仓买入。")   
##@过滤在g.not_buy_again中的股票，也就是当天买入后有持仓的股票
def filter_not_buy_again(stock_list):
    """
    过滤掉当日已买入的股票，避免重复下单
    参数:
        stock_list: 待过滤的股票代码列表
    返回:
        未买入的股票代码列表
    """
    return [stock for stock in stock_list if stock not in g.not_buy_again]
#@如果当天是空仓日，清仓所有股票
def close_account(context):
    """
    清仓操作：若当天为空仓日，则平仓所有持仓股票
    """
    if g.no_trading_today_signal:
        if g.hold_list:
            for stock in g.hold_list:
                position = get_position(stock)
                price = position.last_sale_price
                avg_cost = position.cost_basis
                close_position(context,stock)
                log.info(f"股票{stock}清仓，空仓日，持仓收益率{price/avg_cost-1:.2%}。")


# 4、收盘前后维护策略
#@持久化记录count和firstcount
def record_counters(context):
    with open(NOTEBOOK_PATH+'count.pkl','wb') as f:
        pickle.dump(g.count,f,-1)
    with open(NOTEBOOK_PATH+'firstcount.pkl','wb') as f:
        pickle.dump(g.trade_count,f,-1)  
#@如果是周五，打印所有持仓信息
def print_position_info_weekend(context):
    """
    每周五打印当前持仓详细信息，包括股票代码、成本价、现价、涨跌幅、持仓股数和市值
    """
    today = context.blotter.current_dt
    weekdays = today.weekday()+1
    if weekdays == 5:
        position_list = [position.sid for position in context.portfolio.positions.values() if position.amount != 0]
        log.info(f"{'='*50}")
        log.info(f"          {context.blotter.current_dt.strftime('%Y-%m-%d')} 周末持仓总结")
        log.info(f"{'='*50}")
        if len(position_list) == 0:
            log.info(f"                    空")
        else:
            for stock in position_list:
                position = get_position(stock)
                price = position.last_sale_price
                avg_cost = position.cost_basis
                ret = 100 * (price / avg_cost - 1)
                value = position.amount
                amount = position.amount * price
                print(f"股票: {stock} | 成本价: {avg_cost:.2f} | 现价: {price:.2f} | 涨跌幅: {ret:.2f}% | 市值: {amount:.2f} | 持仓数: {value:.0f}")
        log.info(f"{'='*50}")


# 5、工具函数
#@判断今天是否是要空仓跳过的月份
def today_is_between(context):
    # 判断当前日期是否为资金再平衡（空仓）日，通常在04月或01月期间执行空仓操作
    today_str = context.blotter.current_dt.strftime('%m-%d')
    if g.pass_april:
        if ('04-01' <= today_str <= '04-30') or ('01-01' <= today_str <= '01-31'):
            return True
        else:
            return False
    else:
        return False    
#@获取市值数据函数
def get_float_value(context,stocks):
    """
    获取总市值、流通市值、总股本
    """
    df = pd.DataFrame()
    count = 0
    while count<=10:
        count +=1
        if df.empty:
            try:
                last_trade_day = str(get_trading_day(-1))
                last_trade_day = last_trade_day.replace('-','')
                df = get_fundamentals(stocks, 'valuation', fields=['total_value','float_value','total_shares'], date=last_trade_day)
                if not df.empty:
                    log.info("获取流通市值第: %s次, 获取成功" % (count))
                    break 
            except:
                log.info("获取流通市值第: %s次, 获取不成功，正在重新获取" % (count))
                time.sleep(1)
    return df
#@僵尸因子：获取指定日期的总市值
def get_total_value_bydate(context,stocks,query_date):
    """
    获取指定日期的总市值
    """
    df = pd.DataFrame()
    count = 0
    while count<=10:
        count +=1
        if df.empty:
            try:
                df = get_fundamentals(stocks, 'valuation', fields=['total_value'], date=query_date)
                if not df.empty:
                    break
                    # log.info("获取日期%s的流通市值第: %s次, 获取成功" % (query_date,count)) 
            except:
                log.info("获取日期%s的流通市值第: %s次, 获取不成功，正在重新获取" % (query_date,count))
                time.sleep(1)
    return df

# 6、交易相关底层函数
#@清仓指定股票
def close_position(context,stock):
    """
    指定股票清仓
    """
    last_prices = get_last_price(stock)
    limitprice = round(last_prices*0.985,2)
    if limitprice>0:
        position = get_position(stock)
        vol = position.amount
        if not is_trade():# 回测
            order(stock, -vol)
        else: #实盘
            if (stock.startswith('6') or stock.startswith('5')):#最优五档即时成交剩余转限价
                order_market(stock, -vol, 1, limitprice)
            else:#对手方最优价格
                order_market(stock, -vol, 0,limitprice)# gai:这里类型应该改为限价单，保证成交
    else:
        log.error(f"股票{stock}清仓失败，价格为0。")
#@对target_list中没有持仓的股票执行买入，下单资金均摊分配到每个未持仓的股票
def buy_security(context, target_list):
    """
    买入操作：对target_list中没有持仓的股票执行买入，下单资金均摊分配到每个未持仓的股票
    """
    position_list = [position.sid for position in context.portfolio.positions.values() if position.amount > 0]
    position_count = len(position_list)
    target_num = len(target_list)
    log.info(f"目标数 {target_num}，当前持仓数 {position_count}")
    if target_num > position_count:
        try:
            value = g.totalcash / target_num  #每只股票购买资金，策略资金除以策略持仓股票个数
        except ZeroDivisionError as e:
            log.error(f"资金分摊时除零错误: {e}")
            return
        log.info(f"目标股票列表:{target_list}")
        for stock in target_list:
            if stock not in g.zt:#gai:回测g.zt始终为空
                position_list = [position.sid for position in context.portfolio.positions.values() if position.amount > 0]
                log.info(f"准备检查股票{stock},当前持仓数{len(position_list)}")
                position = get_position(stock)
                total_amount = position.amount
                log.info(f"股票{stock},当前持仓{total_amount},可用资金{g.totalcash *(1-position_count/ target_num):.2f}，计划买入均摊市值 {value:.2f}")
                if total_amount == 0 and context.portfolio.cash>=value:# 当前持仓为0，且可用资金>=计划买入均摊市值
                    if open_position(context,stock,value):
                        log.info(f"股票{stock}买入，分配资金 {value:.2f}")
                        g.not_buy_again.append(stock)
                        if is_trade():
                            time.sleep(5)
                        if len(position_list) == target_num:
                            break
#@买入指定股票相应数量
def open_position(context,stock,vol):
    '''
    买入stock金额vol
    '''
    last_prices = get_last_price(stock)
    if last_prices<g.up_price and last_prices>3:
        limitprice = round(last_prices*1.005,2)
        if limitprice>0:
            if not is_trade():
                order_target_value(stock, vol)
            else:
                amount = int(vol / last_prices/100)*100
                avaliable_cash = context.portfolio.cash
                amount = int((amount * 0.9)/100)*100#gai:这里待优化
                if avaliable_cash < amount*limitprice*0.9:
                    amount = int(avaliable_cash*0.9/limitprice/100)*100
                if (stock.startswith('6') or stock.startswith('5')):#最优五档即时成交剩余转限价
                    order_market(stock, amount, 1, limitprice)
                else:#对手方最优价格
                    order_market(stock, amount, 0, limitprice)#gai:深市不支持1，只能02345
            return True
    else:
        return False
    return False
#@获取股票的最新价格:回测和实盘方法不同
def get_last_price(stock):
    '''
    获取股票的最新价格
    '''
    last_prices_panle = get_history(1, '1m', 'close', [stock], fq='dypre', include=True)
    last_prices = 0
    if not is_trade():
        last_prices = last_prices_panle.loc[last_prices_panle['code'] == stock, 'close'].values[0]
    else:
        snapshot = get_snapshot(stock)
        last_prices = snapshot[stock]['last_px']
    return last_prices
#@获取股票是否涨跌停：回测和实盘方法不同
def my_check_limit(stock):
    '''
    获取股票是否涨跌停
    2：触板涨停(已经是涨停价格，但还有卖盘)(仅支持交易研究查询当日)；
    1：涨停；
    0：既不涨停也不跌停；
    -1：跌停；
    -2：触板跌停(已经是跌停价格，但还有买盘)(仅支持交易研究查询当日)；
    '''
    if is_trade():#实盘
        return check_limit(stock)[stock]
    else:#回测
        last_price = get_last_price(stock)
        day_info = get_history(1, '1d', ['high_limit','low_limit'], [stock], fq='dypre', include=True)
        high_limit = day_info.iloc[0]['high_limit']
        low_limit = day_info.iloc[0]['low_limit']
        if last_price == 0  or high_limit == 0 or low_limit == 0 or pd.isna(high_limit) or pd.isna(low_limit) or pd.isna(last_price):
            log.error(f'股票{stock}价格异常，无法获取涨跌停状态, last_price:{last_price},high_limit:{high_limit},low_limit:{low_limit}')
            return 0
        
        if last_price == high_limit:#涨停
            return 1
        elif last_price == low_limit:#跌停
            return -1
        elif last_price > high_limit or last_price < low_limit:#价格超过涨跌停限制
            log.error(f'股票{stock}价格超过涨跌停限制，无法获取涨跌停状态, last_price:{last_price},high_limit:{high_limit},low_limit:{low_limit}')
            return 0
        else:#既不涨停也不跌停
            return 0
                   
# 7、没用到
"""
# 切分list
def split_list(input_list, chunk_size):
    '''
    将一个大列表按指定大小分割成多个小的子列表，用于批量处理数据和规避API调用限制。
    '''
    return [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]
def check_high_volume(context):
    '''
    检查持仓股票当日成交量是否异常放量：
    如果当日成交量大于过去 HV_duration 天内最大成交量的 HV_ratio 倍，则视为异常，执行卖出操作。
    '''
    hold_list = [position.sid for position in context.portfolio.positions.values() if position.enable_amount > 0]
    if len(hold_list)>0:
        halt_status = get_stock_status(hold_list, 'HALT')
        for stock in hold_list:
            if halt_status[stock]:#gai0：这里错了，delisting_status改为halt_status
                continue
            if check_limit(stock)[stock] == 1:
                continue
            his1d = get_history(g.HV_duration, '1d', 'volume', security_list=stock, fq='pre')#fq方式不影响成交量
            #获取当天成交量
            today_str = context.blotter.current_dt.strftime('%Y%m%d')+'093000'
            today_str_time = datetime.strptime(today_str, '%Y%m%d%H%M%S')
            diff_minues = int((context.blotter.current_dt-today_str_time).total_seconds() // 60)
            his1m = get_history(diff_minues, '1m', 'volume', security_list=stock, fq='pre')
            #当天的成交量
            cur_volume = sum(list(his1m))
            his_volume_list = list(his1d)
            if cur_volume > g.HV_ratio * his_volume_list.max():
                log.info(f"检测到股票{stock} 出现异常放量，执行卖出操作。")
                close_position(context,stock)
#保存财报到本地
def save_data_local(context):
    '''
    获取、更新和维护股票财务报表的本地缓存数据库
    回测：年份变化才更新一次
    实盘：startyear为启动年份-1，endyear为当前年份，每天更新  #gai：这里改一下更新频率？策略中断启动年份怎么办？是否不要这么频繁更新？
    归属母公司所有者的净利润、净利润、营业收入、公告日期、截止日期、股票简称
    '''
    MKT_index = g.risk_idx #'399101.XBHS'#中小综指
    current_time = context.blotter.current_dt - timedelta(days=1)
    
    cur_formatted_time = current_time.strftime("%Y%m%d")
    
    startyear = "2005"
    isadjust = False
    if not is_trade():
        #if g.get_finiance:
        today = context.blotter.current_dt
        current_date = str(today.strftime("%Y%m%d"))
        startyear = str(today.year-1)
        endyear = str(today.year)
        #endyear = str(current_time.year)
        #g.get_finiance = False
        if endyear != g.end_year:
            isadjust = True
    else:
        if g.get_finiance:
            today = context.blotter.current_dt
            current_date = str(today.strftime("%Y%m%d"))
            startyear = str(today.year-1)
            g.get_finiance = False
        endyear = str(current_time.year)
        isadjust = True
    #财报截止年份更新才会重新获取数据
    if isadjust:
        log.info("开始补充财报数据...") 
        initial_list = get_index_stocks(MKT_index,cur_formatted_time)
        initial_list = filter_stocks(context, initial_list)#gai0：未来函数，名字带退的
        df = pd.DataFrame(columns=['code', 'np_parent_company_owners', 'net_profit', 'operating_revenue','publ_date','end_date','secu_abbr'])
        #每秒不得调用超过100次（单次最大调用量是500条数据）
        #initial_list = initial_list[:5]
        chunked_lists = split_list(initial_list, 400)
        try:
            df_csv = pd.read_csv(NOTEBOOK_PATH+'finance_data.csv')
        except:
            df.to_csv(NOTEBOOK_PATH+'finance_data.csv', index=False)
        df_csv = pd.read_csv(NOTEBOOK_PATH+'finance_data.csv')
        for stocklist in chunked_lists:
            #time.sleep(1)
            print(startyear,endyear)
            df1 = get_fundamentals(stocklist, 'income_statement', fields=['np_parent_company_owners','net_profit','operating_revenue'], start_year=startyear, end_year=endyear)   
            df_single_index = df1.reset_index()
            for index, row in df_single_index.iterrows():
                #print(f"索引: {index}:{row}")
                new_row = {'code':row['secu_code'], 'np_parent_company_owners':row['np_parent_company_owners'], 'net_profit':row['net_profit'], 'operating_revenue':row['operating_revenue'],'publ_date':row['publ_date'],'end_date':row['end_date'],'secu_abbr':row['secu_abbr']}
                df_csv.loc[len(df_csv)] = new_row
        #df.to_csv("ss.csv")
        # 删除重复数据
        df_unique = df_csv.drop_duplicates()
        df_unique = df_unique.sort_values(by=['code', 'end_date'], ascending=[True, True])
        #sorted_df = df_csv.sort_values(by='end_date', ascending=True)
        df_unique.to_csv(NOTEBOOK_PATH+'finance_data.csv', index=False)
        log.info("当前财报表有 %s 条记录" % (len(df_unique))) 
        
    #跟新获取数据起始年份
    g.start_year = startyear
    g.end_year = endyear
    #log.info("当前财报起止年份: %s - %s" % (g.start_year,g.end_year))
#获取营业总收入数据函数
def get_income_by_csv(context,stocks):
    '''
    从本地CSV文件中提取股票的最新财务报表数据，如果最新是一季报直接使用，否则使用相比上一份财报的环比增长
    '''
    today = context.blotter.current_dt
    df = pd.DataFrame(columns=['code', 'np_parent_company_owners', 'net_profit', 'operating_revenue','publ_date','end_date','secu_abbr'])
    df_one = pd.DataFrame(columns=['code', 'np_parent_company_owners', 'net_profit', 'operating_revenue','publ_date','end_date','secu_abbr'])
    df_pre = pd.DataFrame(columns=['code', 'np_parent_company_owners', 'net_profit', 'operating_revenue','publ_date','end_date','secu_abbr'])
    #读取本地财报数据
    df_finance = pd.read_csv(NOTEBOOK_PATH+'finance_data.csv')
    #筛选财报
    for stock in stocks:
        df_finance['publ_date'] = pd.to_datetime(df_finance['publ_date'])  # 将日期列转换为日期时间格式
        # 筛选日期早于当前日期的数据
        filtered_df1 = df_finance[df_finance['publ_date'] < today]
        #print("-------1--------")
        #print(filtered_df1)
        filtered_df = filtered_df1.loc[(filtered_df1['code'] == stock)]
        #print("-------2--------")
        #print(filtered_df)
        if len(filtered_df)>1:
            #一季报
            if filtered_df.iloc[-1]['end_date'][5:].replace("-", "") == "0331":
                new_row = {'code': filtered_df.iloc[-1]['code'], 'np_parent_company_owners': filtered_df.iloc[-1]['np_parent_company_owners'], 'net_profit': filtered_df.iloc[-1]['net_profit'], 'operating_revenue': filtered_df.iloc[-1]['operating_revenue'],'publ_date':  filtered_df.iloc[-1]['publ_date'],'end_date':  filtered_df.iloc[-1]['end_date'],'secu_abbr':  filtered_df.iloc[-1]['secu_abbr']}
                df_one.loc[len(df_one)] = new_row
            #其他季报
        else:
                new_row = {'code': filtered_df.iloc[-1]['code'], 'np_parent_company_owners': filtered_df.iloc[-1]['np_parent_company_owners'], 'net_profit': filtered_df.iloc[-1]['net_profit'], 'operating_revenue': filtered_df.iloc[-1]['operating_revenue'],'publ_date':  filtered_df.iloc[-1]['publ_date'],'end_date':  filtered_df.iloc[-1]['end_date'],'secu_abbr':  filtered_df.iloc[-1]['secu_abbr']}
                df.loc[len(df)] = new_row
                new_row = {'code': filtered_df.iloc[-2]['code'], 'np_parent_company_owners': filtered_df.iloc[-2]['np_parent_company_owners'], 'net_profit': filtered_df.iloc[-2]['net_profit'], 'operating_revenue': filtered_df.iloc[-2]['operating_revenue'],'publ_date':  filtered_df.iloc[-2]['publ_date'],'end_date':  filtered_df.iloc[-2]['end_date'],'secu_abbr':  filtered_df.iloc[-2]['secu_abbr']}
                df_pre.loc[len(df_pre)] = new_row
    #处理数据
    df.set_index('code', inplace=True)
    df_pre.set_index('code', inplace=True)
    df_one.set_index('code', inplace=True)
    df.drop('publ_date', axis=1, inplace=True)
    df_pre.drop('publ_date', axis=1, inplace=True)
    df_one.drop('publ_date', axis=1, inplace=True)
    df.drop('end_date', axis=1, inplace=True)
    df_pre.drop('end_date', axis=1, inplace=True)
    df_one.drop('end_date', axis=1, inplace=True)     
    df.drop('secu_abbr', axis=1, inplace=True)
    df_pre.drop('secu_abbr', axis=1, inplace=True)
    df_one.drop('secu_abbr', axis=1, inplace=True)  
    merged_df = None
    if len(df_one)>0:
        merged_df = df_one
    if len(df)>0 and len(df_pre)>0:
        #print('---yy---')
        #print(df - df_pre)
        merged_df = pd.concat([merged_df, df - df_pre], ignore_index=False)
    return merged_df
"""

# 8、实盘增加
# 炸板卖出
'''
def tick_data(context,data):#gai：回测没有运行这个函数
    """
    实盘增加：炸板卖出
    """
    log.info("tick_data")
    hold_list = [position.sid for position in context.portfolio.positions.values() if position.amount != 0]
    if len(hold_list)>0:
        for stock in hold_list:
            position = get_position(stock)
            ava = position.amount
            if ava>0:
                #最新价
                current_price = ast.literal_eval(data[stock]['tick']['bid_grp'][0])[1][0]
                #最高价
                high_price = data[stock]['tick']['high_px'][0]
                #涨停价
                highlimit_price = data[stock]['tick']['up_px'][0]
                #卖一价
                m1_price = ast.literal_eval(data[stock]['tick']['offer_grp'][0])[1][0]
                log.info("%s,卖一价%s" % (stock,m1_price))
                if current_price>=highlimit_price and m1_price == 0:
                    if stock not in g.zt:
                        g.zt[stock]=context.blotter.current_dt
                        log.info("%s监控到已经封板,最新价%s,卖一价%s" % (stock,current_price,m1_price)) 
                if current_price<highlimit_price and stock in g.zt:
                    #炸板卖出
                    close_position(context,stock)
                    log.info("%s炸板卖出,最新价%s" % (stock,current_price)) 
'''
########################################################
#逐鹿，0703改买入委托方式为限价单
#导入函数库 3.11版本  #0406
import numpy as np
import pandas as pd
import time
import pickle
import ast
from datetime import datetime
from datetime import timedelta
import json

NOTEBOOK_PATH=''
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('expand_frame_repr', False)

def initialize(context):
    # 设定基准为沪深300指数
    set_benchmark('000300.SS')
    NOTEBOOK_PATH = get_research_path()#+'xsz/'#'/home/fly/notebook/'
    g.risk_idx = "000985.XBHS"         #'000985.XBHS'中证全指、'399101.XBHS'中小综指
    # 策略基础配置和状态变量
    g.no_trading_today_signal = False  # 当天是否执行空仓（资金再平衡）操作
    g.pass_april = True                # 是否在04月或01月期间执行空仓策略
    g.run_stoploss = True              # 是否启用止损策略
    # 持仓和调仓记录
    g.hold_list = []                 # 当前持仓股票代码列表
    g.yesterday_HL_list = []         # 昨日涨停的股票列表（收盘价等于涨停价）
    g.target_list = []               # 本次调仓候选股票列表
    g.not_buy_again = []             # 当天已买入的股票列表，避免重复下单
    # 策略交易及风控的参数
    g.stock_num = 10                  # 每次调仓目标持仓股票数量
    g.up_price = 100.0               # 股票价格上限过滤条件（排除股价超过此值的股票）
    g.reason_to_sell = ''            # 记录卖出原因（例如：'limitup' 涨停破板 或 'stoploss' 止损）
    g.stoploss_strategy = 3          # 止损策略：1-个股止损；2-大盘止损；3-联合止损策略
    g.stoploss_limit = 0.94          # 个股止损阀值（成本价 × 0.92） 0.88
    g.stoploss_market = 0.97         # 大盘止损参数（若整体跌幅过大则触发卖出）

    g.HV_control = False             # 是否启用成交量异常检测
    g.HV_duration = 120              # 检查成交量时参考的历史天数
    g.HV_ratio = 0.9                 # 当天成交量超过历史最高成交量的比例（如0.9即90%）
    
    # 僵尸因子：市值排名rolling过滤参数
    g.enable_rank_filter = False      # 是否启用市值排名rolling过滤
    g.rank_threshold = 2            # 市值排名rolling均值阈值
    g.rank_rolling_days = 30         # rolling窗口天数，只算交易日
    
    # 周线MACD因子
    g.enable_macd_filter = False       # 是否启用周线MACD因子
    
    # 5日/10日量比因子
    g.enable_volume_ratio_filter = True   # 是否启用量比因子
    g.volume_ratio_threshold = 1.0        # 量比阈值
    g.volume_ratio_boost_positions = 8     # 量比优秀股票往前提升的位置数
    
    #代码转换需要加的全局变量
    g.trading_signal = True  # 是否为可交易日
    g.count = 1 #记录交易日
    g.trade_count = 0 #记录交易日
    g.up_tardeday = ''
    
    g.get_finiance = True
    g.start_year = ""
    g.end_year = ""
    
    g.zt = {}
    #清空财务数据表
    #df = pd.DataFrame(columns=['code', 'np_parent_company_owners', 'net_profit', 'operating_revenue','publ_date','end_date','secu_abbr'])
    #df.to_csv('\\finance_data\\output.csv', index=False)
    #持久化，尝试启动pickle文件
    
    if not is_trade():# 如果是回测，则强制初始化count=1和firstcount=0的文件
        with open(NOTEBOOK_PATH+'count.pkl','wb') as f:
            pickle.dump(1,f,-1)
        with open(NOTEBOOK_PATH+'firstcount.pkl','wb') as f:
            pickle.dump(0,f,-1)
    try:# 从文件中读取count和firstcount的值
        with open(NOTEBOOK_PATH+'count.pkl','rb') as f:
            g.count = pickle.load(f)
            log.info("策略重启初始化,从文件中读取本策略当前交易日: %s" % (g.count)) 
        with open(NOTEBOOK_PATH+'firstcount.pkl','rb') as f:
            g.trade_count = pickle.load(f)
            log.info("策略重启初始化,从文件中读取本策略运行第%s个交易日" % (g.trade_count)) 
    except Exception as e:
        log.error("读取count和firstcount文件失败: %s" % (e))
    
    # 设置交易运行时间
    run_daily(context, update_counters, time='9:00')
    run_daily(context, print_position_info, time='9:00')
    # run_daily(context, save_data_local, time='9:00')
    # run_daily(context, prepare, time='9:05')#gai0:这里改到before_trading_start
    
    # 上午交易任务
    run_daily(context, sell_stocks, time='10:00')
    run_daily(context, weekly_adjustment, time='10:30')
    # 下午交易任务
    run_daily(context, trade_afternoon, time='14:30')
    run_daily(context, close_account, time='14:50')
    # 策略维护
    run_daily(context, record_counters, time='14:55')
    # run_daily(context, print_position_info_weekend, time='15:10')
    # if is_trade():#实盘模式增加
    #     run_daily(context, save_data_local, time='15:00')
    if not is_trade():
        set_limit_mode('UNLIMITED')
    
# 1、开盘前准备工作
#@维护周内计数(g.count)和总计数(g.trade_count)
def update_counters(context):
    """
    更新维护周内计数(g.count)和总计数(g.trade_count)
    如果经过假期，或者策略中断，重置g.count为1，否则g.count++
    g.trade_count++
    """
    today = context.blotter.current_dt
    weekdays = today.weekday()+1 #weekday()返回0-6，所以要+1
    current_date = str(get_trading_day()) #返回格式'2025-06-06'
    date_time = datetime.strptime(current_date, "%Y-%m-%d")
    days = 0
    if g.up_tardeday !='':
        date_time_pre = datetime.strptime(g.up_tardeday, "%Y-%m-%d")
        days = (date_time-date_time_pre).days
    else:#策略首次启动或中断后重启，需要重置count计数
        g.count = 1

    if days >1 or weekdays == 1:#距离上次执行超过1天（说明跨周末或假期），或者今天是周一
        g.count = 1
    else:
        if days != 0:
            g.count += 1
    g.up_tardeday = current_date
    g.trade_count += 1

#@打印每只持仓股票的数据。
def print_position_info(context):
    """
    打印每只持仓股票的数据。
    """
    positions = [position.sid for position in context.portfolio.positions.values() if position.amount != 0]
    log.info(f"{'='*50}")
    log.info(f"          {context.blotter.current_dt.strftime('%Y-%m-%d')} 持仓总结")
    log.info(f"{'='*50}")
    if len(positions)==0:
        log.info(f"                    空")
    else:
        for stock in positions:
            position = get_position(stock)
            price = position.last_sale_price
            avg_cost = position.cost_basis
            ret = 100 * (price / avg_cost - 1)
            value = position.amount
            amount = position.amount * price
            print(f"股票: {stock} | 成本价: {avg_cost:.2f} | 现价: {price:.2f} | 涨跌幅: {ret:.2f}% | 市值: {amount:.2f} | 持仓数: {value:.0f}")
    log.info(f"{'='*50}")
    return
def before_trading_start(context, data):
    prepare(context)
#@ 初始化g.zt={}, g.hold_list持仓股票列表, g.yesterday_HL_list昨日涨停持仓, g.no_trading_today_signal空仓日
def prepare(context):
    """
    1、初始化涨停板追踪字典g.zt={}
    2、更新持仓列表g.hold_list：刷新当前实际持仓股票清单
    3、识别涨停股票g.yesterday_HL_list：找出昨日收盘时处于涨停状态的持仓股票
    4、判断交易状态g.no_trading_today_signal：确定当日是否为资金再平衡的空仓日
    """
    g.zt = {}
    # 从当前持仓中提取股票代码，更新持仓列表
    g.hold_list = [position.sid for position in context.portfolio.positions.values() if position.amount != 0]
    if g.hold_list != []:
        # 获取持仓股票昨日数据（包括收盘价、涨停价、跌停价）
        p = get_history(1, frequency="1d", field=['low','open','close','high_limit','volume'], security_list=g.hold_list, fq='dypre', include=False)#gai0：这里pre改成dypre，不影响结果，因为只是判断涨停与否
        up_limit_list = list(p[p['close'] == p['high_limit']]['code'])
        g.yesterday_HL_list = up_limit_list
    else:
        g.yesterday_HL_list = []
    # 根据当前日期判断是否为空仓日（例如04月或01月时资金再平衡）
    g.no_trading_today_signal = today_is_between(context)


# 2、上午交易任务
#@止盈与止损操作
def sell_stocks(context):
    """
    止盈与止损操作：
    根据策略（1: 个股止损；2: 大盘止损；3: 联合策略）判断是否执行卖出操作。
    """
    if g.run_stoploss:
        current_positions = [position.sid for position in context.portfolio.positions.values() if position.amount != 0]
        if g.stoploss_strategy == 1:# 个股止盈或止损判断
            for stock in current_positions:
                position = get_position(stock)
                price = position.last_sale_price
                avg_cost = position.cost_basis
                if price >= avg_cost * 2:
                    close_position(context,stock)
                    log.info(f"股票{stock}清仓，个股止盈。")
                elif price < avg_cost * g.stoploss_limit and price > 0 :
                    close_position(context,stock)
                    log.info(f"股票{stock}清仓，个股止损。")
                    g.reason_to_sell = 'stoploss'
        elif g.stoploss_strategy == 2:# 大盘止损判断，若整体市场跌幅过大则平仓所有股票
            last_trade_day = str(get_trading_day(-1))
            last_trade_day = last_trade_day.replace('-','')
            stock_df = get_price(security=get_index_stocks('399101.XBHS',last_trade_day)
                        ,end_date=last_trade_day, frequency='daily'
                        ,fields=['close', 'open'], count=1)
            # 计算成分股平均涨跌，即指数涨跌幅
            down_ratio = (stock_df['close'] / stock_df['open']).mean()
            if down_ratio <= g.stoploss_market:
                g.reason_to_sell = 'stoploss'
                log.info(f"市场风险（平均跌幅 {down_ratio:.2%}），准备清仓...")
                for stock in current_positions:
                    close_position(context,stock)
                    log.info(f"股票{stock}清仓，大盘止损。")
                
        elif g.stoploss_strategy == 3:# 联合止损策略：结合大盘和个股判断
            last_trade_day = str(get_trading_day(-1))
            last_trade_day = last_trade_day.replace('-','')
            stock_df = get_price(security=get_index_stocks('399101.XBHS',last_trade_day)
                        ,end_date=last_trade_day, frequency='daily'
                        ,fields=['close', 'open'],count=1)#gai:fq从None改成dypre，不影响结果
            # #gai：当天跌幅过大就清仓，不要算昨天的。效果有提升，但是回测太慢
            # stock_list = get_index_stocks('399101.XBHS',last_trade_day)
            # stock_df = get_history(1,'1d',['open'],stock_list,include=True)
            # latest_close = get_history(1, '1m', 'close', stock_list, include=True)
            # stock_df = stock_df.merge(latest_close[['code', 'close']], on='code', how='left')
            # 计算成分股平均涨跌，即指数涨跌幅
            down_ratio = (stock_df['close'] / stock_df['open']).mean()
            if down_ratio <= g.stoploss_market:
                g.reason_to_sell = 'stoploss'
                log.info(f"市场风险（平均跌幅 {down_ratio:.2%}），准备清仓...")
                for stock in current_positions:
                    position = get_position(stock)
                    price = position.last_sale_price
                    avg_cost = position.cost_basis
                    close_position(context,stock)
                    log.critical(f"股票{stock}清仓，大盘止损，持仓收益率{price/avg_cost-1:.2%}。")
            else:
                for stock in current_positions:
                    position = get_position(stock)
                    price = position.last_sale_price
                    avg_cost = position.cost_basis
                    if price < avg_cost * g.stoploss_limit and price > 0:
                        close_position(context,stock)
                        log.critical(f"股票{stock}清仓，个股止损，持仓收益率{price/avg_cost-1:.2%}。")
                        g.reason_to_sell = 'stoploss'
#@每周调仓策略
def weekly_adjustment(context):
    """
    每周调仓策略：
    如果非空仓日，先选股得到目标股票列表，再卖出当前持仓中不在目标列表且昨日未涨停的股票，
    最后买入目标股票，同时记录当天买入情况避免重复下单。

    时机控制：只在策略启动日或每周第2天执行调仓
    智能卖出：保护昨日涨停股票，避免错失涨停后续收益
    资金管理：先卖后买，确保资金合理分配
    实盘适配：为实盘交易增加延时处理
    """
    if not g.no_trading_today_signal:
        log.info(f"当前第{g.trade_count}个交易日，周{g.count}")
        if g.trade_count == 1 or g.count == 2:#策略首次运行，或者每周第2天
            log.info(f"每周调仓，开始...")
            g.not_buy_again = []  # 重置当天已买入记录
            g.target_list = get_stock_list(context)
            # 取目标持仓数以内的股票作为调仓目标
            target_list = g.target_list[:g.stock_num]
            log.info(f"每周调仓目标股票: {target_list}")
            log.info(f"每周调仓，先卖出不在目标中的股票...")
            # 遍历当前持仓，若股票不在目标列表且非昨日涨停，则执行卖出操作
            for stock in g.hold_list:
                position = get_position(stock)
                price = position.last_sale_price
                avg_cost = position.cost_basis
                if stock not in target_list and stock not in g.yesterday_HL_list:
                    log.critical(f"股票{stock}不在调仓目标中，清仓，持仓收益率{price/avg_cost-1:.2%}。")
                    close_position(context,stock)
                else:
                    log.info(f"股票{stock}仍在调仓目标中，继续持有，持仓收益率{price/avg_cost-1:.2%}。")
            if is_trade():
                time.sleep(30)
            log.info(f"每周调仓，买入目标中还未持仓的股票...")
            buy_security(context, target_list)# 对目标股票执行买入操作
            if is_trade():
                time.sleep(30)
            # 更新当天已买入记录，防止重复买入
            check_hold_list = [position.sid for position in context.portfolio.positions.values() if position.amount != 0]
            for stock in check_hold_list:
                if stock not in g.not_buy_again:
                    g.not_buy_again.append(stock)
##@获取市值最小的2*g.stock_num只股票
def get_stock_list(context):
    '''
    股票池：g.risk_idx
    进行过滤
    先选出市值最小的50只股票，再根据市值排名rolling均值进行二次筛选，最后选出市值最小的2 * g.stock_num作为候选池
    '''
    final_list = []
    MKT_index = g.risk_idx #'399101.XBHS'#中小综指
    current_time = context.blotter.current_dt - timedelta(days=1)
    cur_formatted_time = current_time.strftime("%Y%m%d")
    initial_list = filter_stocks(context, get_index_stocks(MKT_index,cur_formatted_time))

    circulating_market_cap_df = get_float_value(context,initial_list)
    if not circulating_market_cap_df.empty:
        sort_df = circulating_market_cap_df.sort_values(by='total_value', ascending=True)#排序
        initial_list = list(sort_df.index)
        final_list = initial_list[:50]  # 限制数据规模，防止一次处理数据过大
        
        # 僵尸因子：按市值排名rolling均值过滤
        if g.enable_rank_filter:
            final_list = filter_by_market_cap_rank_rolling(context, final_list, 
                                                         threshold=g.rank_threshold, 
                                                         rolling_days=g.rank_rolling_days)
        
        # 5日/10日量比因子：筛选量比>=阈值的股票
        if g.enable_volume_ratio_filter:
            final_list = filter_by_volume_ratio(context, final_list, g.volume_ratio_threshold)
        
        # 周线MACD因子：筛选上周MACD>0的股票
        if g.enable_macd_filter:
            final_list = filter_by_weekly_macd(context, final_list)
        
        #hold_list = [position.sid for position in context.portfolio.positions.values() if position.amount != 0]
        # 取前2倍目标持仓股票数作为候选池
        final_list = final_list[:2 * g.stock_num]
        log.info(f"初选候选股票: {final_list}")
    return final_list
##@ 过滤股票
def filter_stocks(context, stock_list):
    """
    过滤以下股票：
    1、过滤停牌、退市、ST等有风险的股票
    2、只保留主板
    3、过滤未持仓的涨跌停股票
    4、过滤上市时间不足375天的次新股
    5、过滤名称中包含退市标识的股票
    """
    today = context.blotter.current_dt
    today_str = str(today.strftime("%Y%m%d"))
    yesterday = context.blotter.current_dt - timedelta(days=1)
    yesterday_str = yesterday.strftime("%Y%m%d")
    position_list = [position.sid for position in context.portfolio.positions.values() if position.amount != 0]
    filtered_stocks = []
    halt_status_today = get_stock_status(stock_list, 'HALT',today_str)
    halt_status_yesterday = get_stock_status(stock_list, 'HALT',yesterday_str)
    delisting_status = get_stock_status(stock_list, 'DELISTING',today_str)
    st_status = get_stock_status(stock_list, 'ST',today_str)
    #获取股票信息
    stock_infos = get_stock_info(stock_list, ['stock_name','listed_date','de_listed_date'])
    last_trade_day = get_trading_day(-1)
    for stock in stock_list:
        if is_trade():#gai0：这里改为is_trade()，回测有未来函数
            if '退' in stock_infos[stock]['stock_name'] or 'ST' in stock_infos[stock]['stock_name']: #gai0:这里加上名字st
                continue
        if halt_status_yesterday[stock]:
            continue
        if halt_status_today[stock]:  # 停牌
            continue
        if st_status[stock]:  # ST
            continue
        if delisting_status[stock]:  # 退市
            continue
        # if not (stock.startswith('00') or stock.startswith('60')):  # 非主板
        #     continue
        # if stock.startswith('00') or stock.startswith('60'):  # 主板剔除
        #     continue
        if not (stock in position_list or check_limit(stock)[stock]==0):  # 涨跌停 #gai0：这里看文档，有未来函数，原来是check_limit(stock)[stock]
            continue
        if 'listed_date' in stock_infos[stock]:# 过滤上市天数少于375天的股票
            listed_date_str = stock_infos[stock]['listed_date']
            listed_date = datetime.strptime(listed_date_str, '%Y-%m-%d')
            if (last_trade_day-listed_date.date()).days<375:
                continue
        else:
            continue
        filtered_stocks.append(stock)
    return filtered_stocks
##@ 僵尸因子：按市值排名rolling均值过滤股票
def filter_by_market_cap_rank_rolling(context, stock_list, threshold, rolling_days):
    """
    根据市值排名rolling均值过滤股票
    参数:
        stock_list: 待过滤的股票代码列表
        threshold: 市值排名rolling均值阈值，小于此值的股票将被剔除
        rolling_days: rolling窗口天数，默认20个交易日（约一个月）
    返回:
        过滤后的股票代码列表
    """
    if not stock_list:
        return stock_list
    
    filtered_stocks = []
    
    try:
        trading_days = []
        for i in range(rolling_days, 0, -1):# 获取过去rolling_days个交易日的日期
            trade_day = get_trading_day(-i)
            trading_days.append(str(trade_day).replace('-',''))
        
        # # 获取昨日指数成分股作为排名基准池
        # yesterday = context.blotter.current_dt - timedelta(days=1)
        # yesterday_formatted_time = yesterday.strftime("%Y%m%d")
        # index_stocks = get_index_stocks(MKT_index, yesterday_formatted_time)
        
        # 创建DataFrame存储每只股票每天的排名：行是股票，列是交易日
        stock_rankings_df = pd.DataFrame(index=stock_list)
        
        for trade_day in trading_days:
            try:
                daily_market_cap = get_total_value_bydate(context,stock_list,trade_day)# 获取该日期的市值数据
                if not daily_market_cap.empty:
                    # 直接计算市值排名（市值越小，排名数字越小）
                    daily_market_cap['rank'] = daily_market_cap['total_value'].rank(method='min', na_option='keep')
                    # stock_rankings_df有但daily_market_cap没有的填NaN，反之舍弃
                    stock_rankings_df[trade_day] = daily_market_cap['rank'].reindex(stock_rankings_df.index)
                else:
                    log.error(f"获取{trade_day}日市值数据为空")
            except Exception as e:
                log.error(f"计算{trade_day}日市值排名失败: {e}")
        
        # 检查是否有有效的交易日数据
        total_trading_days = len(stock_rankings_df.columns)
        if total_trading_days == 0:
            log.error("没有获取到任何有效的交易日数据，返回原股票列表")
            return stock_list
            
        valid_days_count = stock_rankings_df.count(axis=1)  # 每行非NaN值的数量
        avg_ranks = stock_rankings_df.mean(axis=1)  # 每行的平均值（自动忽略NaN）
        # 数据充足的股票（有效数据>=一半交易日）
        min_required_days = max(1, total_trading_days // 2)  # 至少需要1天数据
        sufficient_data_mask = valid_days_count >= min_required_days
        sufficient_data_stocks = stock_rankings_df.index[sufficient_data_mask]
        # 在数据充足的股票中，筛选平均排名>=阈值的股票
        qualified_mask = avg_ranks[sufficient_data_mask] >= threshold
        qualified_stocks = sufficient_data_stocks[qualified_mask]
        # 数据不足的股票（保守保留）
        insufficient_data_stocks = stock_rankings_df.index[~sufficient_data_mask]
        # 合并结果
        filtered_stocks = list(qualified_stocks) + list(insufficient_data_stocks)
        
        # 日志输出
        for stock in sufficient_data_stocks:
            avg_rank = avg_ranks[stock]
            log.debug(f"股票{stock}排名: {stock_rankings_df.loc[stock]}")
            if avg_rank >= threshold:
                log.info(f"股票{stock}平均排名{avg_rank:.1f}，通过筛选（排名≥{threshold}）")
            else:
                log.info(f"股票{stock}平均排名{avg_rank:.1f}，被剔除（排名<{threshold}，市值排名过于靠前）")
        for stock in insufficient_data_stocks:
            valid_days = valid_days_count[stock]
            log.info(f"股票{stock}数据不足（有效数据{valid_days}天），保留")
        log.info(f"市值排名rolling过滤：原有{len(stock_list)}只股票，过滤后{len(filtered_stocks)}只股票")
    
    except Exception as e:
        log.error(f"市值排名rolling过滤失败: {e}，返回原股票列表")
        return stock_list
    
    return filtered_stocks
##@ 5日/10日量比因子：筛选量比>=阈值的股票
def filter_by_volume_ratio(context, stock_list, threshold):
    """
    根据5日/10日量比调整股票排序，量比>=阈值的股票在原顺序基础上往前提升指定位置
    参数:
        stock_list: 待过滤的股票代码列表
        threshold: 量比阈值，大于等于此值的股票将往前提升位置
    返回:
        调整排序后的股票代码列表
    """
    if not stock_list:
        return stock_list
    volume_boost_stocks = set()# 记录量比>=阈值的股票
    try:
        volume_data = get_history(20, '1d', 'volume', security_list=stock_list, fq='dypre', include=False, fill='pre')
        for stock in stock_list:
            try:
                stock_volume_data = volume_data[volume_data['code'] == stock]
                stock_volume_data = stock_volume_data[stock_volume_data['volume'] > 0]  # 过滤掉成交量为0的数据
                if len(stock_volume_data) < 10:
                    log.debug(f"股票{stock}有效成交量数据不足({len(stock_volume_data)}天)，保持原位置")
                    continue
                volumes = stock_volume_data['volume'].values
                avg_volume_5d = np.mean(volumes[-5:])# 计算5日平均成交量（最近5天）
                avg_volume_10d = np.mean(volumes[-10:])# 计算10日平均成交量（最近10天）
                
                if avg_volume_10d > 0:
                    volume_ratio = avg_volume_5d / avg_volume_10d# 计算量比
                    if volume_ratio >= threshold:
                        volume_boost_stocks.add(stock)
                        log.info(f"股票{stock}量比={volume_ratio:.2f}，将往前提{g.volume_ratio_boost_positions}位（≥{threshold}）")
                else:
                    log.debug(f"股票{stock}10日均量为0，保持原位置")
            except Exception as e:
                log.error(f"计算股票{stock}的量比失败: {e}，保持原位置")
                continue
        
        # 对原列表进行位置调整：量比>=阈值的股票往前提5位
        result_list = stock_list.copy()
        # 从后往前处理，避免索引变化的影响
        i = len(result_list) - 1
        while i>=0:
            stock = result_list[i]
            if stock in volume_boost_stocks:
                # 计算新位置：往前提升指定位置数，但不能超过索引0
                new_position = max(0, i - g.volume_ratio_boost_positions)
                # 移除股票并插入到新位置
                removed_stock = result_list.pop(i)
                result_list.insert(new_position, removed_stock)
                volume_boost_stocks.remove(stock)
            else:
                i = i-1
        # log.info(f"量比调整：原有{len(stock_list)}只股票，{len(volume_boost_stocks)}只股票量比>={threshold}往前提{g.volume_ratio_boost_positions}位")
        log.info(f"量比调整前股票列表：{stock_list}")
        log.info(f"量比调整后股票列表：{result_list}")
        return result_list
        
    except Exception as e:
        log.error(f"量比排序调整失败: {e}，返回原股票列表")
        return stock_list

##@ 周线MACD因子：筛选周线MACD>0的股票
def filter_by_weekly_macd(context, stock_list):
    """
    根据周线MACD指标过滤股票，筛选出周线MACD>0的股票
    参数:
        stock_list: 待过滤的股票代码列表
    返回:
        过滤后的股票代码列表
    """
    if not stock_list:
        return stock_list
    good_stocks = []
    other_stocks = []
    try:
        # 一次性获取所有股票的周线数据
        weekly_data = get_history(36, '1w', 'close', security_list=stock_list, fq='dypre', include=False, fill='pre')
        if weekly_data.empty:
            log.warning(f"无法获取股票的周线数据: {stock_list}")
            return stock_list
        # 获取最新1分钟数据作为本周当前价格
        current_data = get_history(1, '1m', 'close', security_list=stock_list, fq='dypre', include=True)
        for stock in stock_list:# 对每只股票计算MACD
            try:
                stock_data = weekly_data[weekly_data['code'] == stock]
                close_prices = stock_data['close'].values
                
                current_stock_data = current_data[current_data['code'] == stock]
                if not current_stock_data.empty:
                    current_close = current_stock_data['close'].values[0]
                    close_prices = np.append(close_prices, current_close)
                macdDIF_data, macdDEA_data, macd_data = get_MACD(close_prices, 12, 26, 9)
                latest_macd = macd_data[-1]
                if latest_macd > 0:
                    good_stocks.append(stock)
                    log.info(f"股票{stock}周线MACD={latest_macd:.4f}>0，位置提前")
                else:
                    other_stocks.append(stock)
            except Exception as e:
                log.error(f"计算股票{stock}的MACD失败: {e}")
                other_stocks.append(stock)
                continue
        filtered_stocks = good_stocks + other_stocks
        log.info(f"周线MACD过滤：原有{len(stock_list)}只股票，符合标准的有{len(good_stocks)}只排序提前")
    except Exception as e:
        log.error(f"周线MACD过滤失败: {e}，返回原股票列表")
        return stock_list
    return filtered_stocks
    

#@3、下午交易任务：检查是否有因为涨停破板触发的卖出信号；检查账户中是否需要补仓。
def trade_afternoon(context):
    """
    下午交易任务：
    1. 检查是否有因为涨停破板触发的卖出信号；
    2. 如启用了成交量监控，则检测是否有异常成交量；
    3. 检查账户中是否需要补仓。
    """
    if not g.no_trading_today_signal:
        check_continue_limitup(context)
        if g.HV_control:
            check_high_volume(context)
        rebalance_positions(context)    
##@检查昨日处于涨停状态的股票在今天下午是否继续涨停，如没有继续涨停则卖出该股票
def check_continue_limitup(context):
    """
    检查昨日处于涨停状态的股票在当前是否继续涨停。
    如没有继续涨停，则立即卖出该股票，并记录卖出原因为 "limitup"。
    """
    now_time = context.blotter.current_dt
    if g.yesterday_HL_list:
        for stock in g.yesterday_HL_list:
            position = get_position(stock)
            price = position.last_sale_price
            avg_cost = position.cost_basis
            if check_limit(stock)[stock] != 1:#gai0：这里看文档，有未来函数，原来是check_limit(stock)[stock]
                log.critical(f"股票{stock}昨日涨停今日没有继续涨停，触发卖出操作，持仓收益率{price/avg_cost-1:.2%}。")
                close_position(context,stock)
                g.reason_to_sell = 'limitup'
            else:
                log.critical(f"股票{stock}昨日涨停，今日仍维持涨停状态，持仓收益率{price/avg_cost-1:.2%}。")                
##@检查账户中是否因没有继续涨停卖出而需要补仓。
def rebalance_positions(context):
    """
    检查账户资金与持仓数量：
    如果因涨停破板卖出导致持仓不足，则从目标股票中筛选未买入股票，进行补仓操作。
    """
    if g.reason_to_sell == 'limitup':
        g.hold_list = [position.sid for position in context.portfolio.positions.values() if position.amount != 0]
        if len(g.hold_list) < g.stock_num:
            target_list = filter_not_buy_again(g.target_list)
            target_list = target_list[:min(g.stock_num, len(target_list))]
            log.info(f"检测到补仓需求，可用资金 {round(context.portfolio.cash, 2)}，候选补仓股票: {target_list}")
            buy_security(context, target_list)
        g.reason_to_sell = ''
    else:
        log.info("未检测到涨停破板卖出事件，不进行补仓买入。")   
##@过滤在g.not_buy_again中的股票，也就是当天买入后有持仓的股票
def filter_not_buy_again(stock_list):
    """
    过滤掉当日已买入的股票，避免重复下单
    参数:
        stock_list: 待过滤的股票代码列表
    返回:
        未买入的股票代码列表
    """
    return [stock for stock in stock_list if stock not in g.not_buy_again]
#@如果当天是空仓日，清仓所有股票
def close_account(context):
    """
    清仓操作：若当天为空仓日，则平仓所有持仓股票
    """
    if g.no_trading_today_signal:
        if g.hold_list:
            for stock in g.hold_list:
                position = get_position(stock)
                price = position.last_sale_price
                avg_cost = position.cost_basis
                close_position(context,stock)
                log.info(f"股票{stock}清仓，空仓日，持仓收益率{price/avg_cost-1:.2%}。")


# 4、收盘前后维护策略
#@持久化记录count和firstcount
def record_counters(context):
    with open(NOTEBOOK_PATH+'count.pkl','wb') as f:
        pickle.dump(g.count,f,-1)
    with open(NOTEBOOK_PATH+'firstcount.pkl','wb') as f:
        pickle.dump(g.trade_count,f,-1)  
#@如果是周五，打印所有持仓信息
def print_position_info_weekend(context):
    """
    每周五打印当前持仓详细信息，包括股票代码、成本价、现价、涨跌幅、持仓股数和市值
    """
    today = context.blotter.current_dt
    weekdays = today.weekday()+1
    if weekdays == 5:
        position_list = [position.sid for position in context.portfolio.positions.values() if position.amount != 0]
        log.info(f"{'='*50}")
        log.info(f"          {context.blotter.current_dt.strftime('%Y-%m-%d')} 周末持仓总结")
        log.info(f"{'='*50}")
        if len(position_list) == 0:
            log.info(f"                    空")
        else:
            for stock in position_list:
                position = get_position(stock)
                price = position.last_sale_price
                avg_cost = position.cost_basis
                ret = 100 * (price / avg_cost - 1)
                value = position.amount
                amount = position.amount * price
                print(f"股票: {stock} | 成本价: {avg_cost:.2f} | 现价: {price:.2f} | 涨跌幅: {ret:.2f}% | 市值: {amount:.2f} | 持仓数: {value:.0f}")
        log.info(f"{'='*50}")


# 5、工具函数
#@判断今天是否是要空仓跳过的月份
def today_is_between(context):
    # 判断当前日期是否为资金再平衡（空仓）日，通常在04月或01月期间执行空仓操作
    today_str = context.blotter.current_dt.strftime('%m-%d')
    if g.pass_april:
        if ('04-01' <= today_str <= '04-30') or ('01-01' <= today_str <= '01-31'):
            return True
        else:
            return False
    else:
        return False    
#@获取市值数据函数
def get_float_value(context,stocks):
    """
    获取总市值、流通市值、总股本
    """
    df = pd.DataFrame()
    count = 0
    while count<=10:
        count +=1
        if df.empty:
            try:
                last_trade_day = str(get_trading_day(-1))
                last_trade_day = last_trade_day.replace('-','')
                df = get_fundamentals(stocks, 'valuation', fields=['total_value','float_value','total_shares'], date=last_trade_day)
                if not df.empty:
                    log.info("获取流通市值第: %s次, 获取成功" % (count))
                    break 
            except:
                log.info("获取流通市值第: %s次, 获取不成功，正在重新获取" % (count))
                time.sleep(1)
    return df
#@僵尸因子：获取指定日期的总市值
def get_total_value_bydate(context,stocks,query_date):
    """
    获取指定日期的总市值
    """
    df = pd.DataFrame()
    count = 0
    while count<=10:
        count +=1
        if df.empty:
            try:
                df = get_fundamentals(stocks, 'valuation', fields=['total_value'], date=query_date)
                if not df.empty:
                    break
                    # log.info("获取日期%s的流通市值第: %s次, 获取成功" % (query_date,count)) 
            except:
                log.info("获取日期%s的流通市值第: %s次, 获取不成功，正在重新获取" % (query_date,count))
                time.sleep(1)
    return df

# 6、交易相关底层函数
#@清仓指定股票
def close_position(context,stock):
    """
    指定股票清仓
    """
    last_prices = get_last_price(stock)
    limitprice = round(last_prices*0.985,2)
    if limitprice>0:
        position = get_position(stock)
        vol = position.amount
        if not is_trade():# 回测
            order(stock, -vol)
        else: #实盘
            if (stock.startswith('6') or stock.startswith('5')):#最优五档即时成交剩余转限价
                order_market(stock, -vol, 1, limitprice)
            else:#对手方最优价格
                order_market(stock, -vol, 0,limitprice)# gai:这里类型应该改为限价单，保证成交
    else:
        log.error(f"股票{stock}清仓失败，价格为0。")
#@对target_list中没有持仓的股票执行买入，下单资金均摊分配到每个未持仓的股票
def buy_security(context, target_list):
    """
    买入操作：对target_list中没有持仓的股票执行买入，下单资金均摊分配到每个未持仓的股票
    """
    position_list = [position.sid for position in context.portfolio.positions.values() if position.amount > 0]
    position_count = len(position_list)
    target_num = len(target_list)
    log.info(f"目标数 {target_num}，当前持仓数 {position_count}")
    if target_num > position_count:
        try:
            value = context.portfolio.cash / (target_num - position_count)
        except ZeroDivisionError as e:
            log.error(f"资金分摊时除零错误: {e}")
            return
        log.info(f"目标股票列表:{target_list}")
        for stock in target_list:
            if stock not in g.zt:#gai:回测g.zt始终为空
                position_list = [position.sid for position in context.portfolio.positions.values() if position.amount > 0]
                log.info(f"准备检查股票{stock},当前持仓数{len(position_list)}")
                position = get_position(stock)
                total_amount = position.amount
                log.info(f"股票{stock},当前持仓{total_amount},可用资金{context.portfolio.cash:.2f}，计划买入均摊市值 {value:.2f}")
                if total_amount == 0 and context.portfolio.cash>=value:# 当前持仓为0，且可用资金>=计划买入均摊市值
                    if open_position(context,stock,value):
                        log.info(f"股票{stock}买入，分配资金 {value:.2f}")
                        g.not_buy_again.append(stock)
                        if is_trade():
                            time.sleep(5)
                        if len(position_list) == target_num:
                            break
#@买入指定股票相应数量
def open_position(context,stock,vol):
    '''
    买入stock金额vol
    '''
    last_prices = get_last_price(stock)
    limitprice = round(last_prices*1.015,2)
    if limitprice>0:
     
        order_value(stock, vol)
      
        return True
    return False

#@获取股票的最新价格:回测和实盘方法不同
def get_last_price(stock):
    '''
    获取股票的最新价格
    '''
    last_prices_panle = get_history(1, '1m', 'close', [stock], fq='dypre', include=True)
    last_prices = 0
    if not is_trade():
        last_prices = last_prices_panle.loc[last_prices_panle['code'] == stock, 'close'].values[0]
    else:
        snapshot = get_snapshot(stock)
        last_prices = snapshot[stock]['last_px']
    return last_prices
#@获取股票是否涨跌停：回测和实盘方法不同
def my_check_limit(stock):
    '''
    获取股票是否涨跌停
    2：触板涨停(已经是涨停价格，但还有卖盘)(仅支持交易研究查询当日)；
    1：涨停；
    0：既不涨停也不跌停；
    -1：跌停；
    -2：触板跌停(已经是跌停价格，但还有买盘)(仅支持交易研究查询当日)；
    '''
    if is_trade():#实盘
        return check_limit(stock)[stock]
    else:#回测
        last_price = get_last_price(stock)
        day_info = get_history(1, '1d', ['high_limit','low_limit'], [stock], fq='dypre', include=True)
        high_limit = day_info.iloc[0]['high_limit']
        low_limit = day_info.iloc[0]['low_limit']
        if last_price == 0  or high_limit == 0 or low_limit == 0 or pd.isna(high_limit) or pd.isna(low_limit) or pd.isna(last_price):
            log.error(f'股票{stock}价格异常，无法获取涨跌停状态, last_price:{last_price},high_limit:{high_limit},low_limit:{low_limit}')
            return 0
        
        if last_price == high_limit:#涨停
            return 1
        elif last_price == low_limit:#跌停
            return -1
        elif last_price > high_limit or last_price < low_limit:#价格超过涨跌停限制
            log.error(f'股票{stock}价格超过涨跌停限制，无法获取涨跌停状态, last_price:{last_price},high_limit:{high_limit},low_limit:{low_limit}')
            return 0
        else:#既不涨停也不跌停
            return 0
###############################################
'''
索普量化逆回购
作者:索普量化
微信:xms_quants1
时间:20251017
'''
import math
import pandas as pd
def initialize(context):
    # 初始化策略
    #一天期的深圳逆回购标的
    g.stock='131810.SZ'
    #保留的资金，避免新股，可转债等申购
    g.cash=0
    print('开始运行逆回购策略*********************')
    run_daily(context, func=run_reverse_repurchase, time='10:30')
def run_reverse_repurchase(context):
    '''
    逆回购函数
    '''
    current_dt=context.blotter.current_dt
    current_dt=current_dt.strftime('%Y-%m-%d')
    account=get_xg_account(context)
    if account.shape[0]>0:
        cash=account['可用金额'].tolist()[-1]
        print('可以金额****************',cash)
        cash=cash-g.cash
        #逆回购最低1000元10张一手
        if cash>=1000:
            amount = int(cash/1000)*10
            if amount>=10:
                #全部逆回购卖出
                order(g.stock, -1*amount)
                print(current_dt,'逆回购回购成功')
            else:
                print(current_dt,'逆回购回购失败，低于最低数量')
        else:
           print(current_dt,'逆回购回购失败，低于最低金额')
    else:
        print(current_dt,'逆回购回购失败，没有金额')
def get_xg_account(context):
    '''
    获取小果账户数据
    '''
    df=pd.DataFrame()
    df['可用金额']=[context.portfolio.cash]
    df['总资产']=[context.portfolio.portfolio_value]
    df['持仓价值']=[context.portfolio.positions_value]
    df['已使用现金']=[context.portfolio.capital_used]
    df['当前收益比例']=[context.portfolio.returns]
    df['初始账户总资产']=[context.portfolio.pnl]
    df['开始时间']=[context.portfolio.start_date]
    return df
def get_xg_position(context):
    '''
    获取小果持股数据
    '''
    data=pd.DataFrame()
    positions=context.portfolio.positions
    stock_list=list(set(positions.keys()))
    print('持股数量{}'.format(len(stock_list)))
    for stock in stock_list:
        df=pd.DataFrame()
        df['证券代码']=[positions[stock].sid]
        df['可用数量']=[positions[stock].enable_amount]
        df['持有数量']=[positions[stock].amount]
        df['最新价']=[positions[stock].last_sale_price ]
        df['成本价']=[positions[stock].cost_basis ]
        df['今日买入']=[positions[stock].today_amount ]
        df['持股类型']=[positions[stock].business_type  ]
        data=pd.concat([data,df],ignore_index=True)
    '''
    if data.shape[0]>0:
        if g.is_del=='是':
            print('开始策略隔离**********')
            data['隔离']=data['证券代码'].apply(lambda x: '是' if x in g.stock_list else '不是')
            data=data[data['隔离']=='是']
        else:
            print('不开启策略隔离*********')
    '''
    return data
def get_xg_order(context):
    '''
    获取小果委托数据
    '''
    orders=get_orders()
    print("委托数量{}".format(len(orders)))
    data=pd.DataFrame()
    if len(orders)>0:
        for ors in orders:
            df=pd.DataFrame()
            df['订单号']=[ors.id]
            df['订单产生时间']=[ors.dt]
            df['指定价格']=[ors.limit ]
            df['证券代码']=[ors.symbol ]
            df['委托数量']=[ors.amount ]
            df['订单生成时间']=[ors.created ]
            df['成交数量']=[ors.filled ]
            df['委托编号']=[ors.entrust_no]
            df['盘口档位']=[ors.priceGear ]
            df['订单状态']=[ors.status ]
            data=pd.concat([data,df],ignore_index=True)
        
    else:
        data=data
    return data
def get_xg_position_on(context,security=''):
    ''''
    获取单股的持股情况
    '''
    pos=get_positions(security=security)
    df=pd.DataFrame()
    if len(pos)>0:
        df['证券代码']=[pos[security].sid]
        df['可以数量']=[pos[security].enable_amount]
        df['持有数量']=[pos[security].amount]
        df['最新价']=[pos[security].last_sale_price ]
        df['成本价']=[pos[security].cost_basis ]
        df['今日买入']=[pos[security].today_amount ]
        df['持股类型']=[pos[security].business_type  ]
    else:
        df=df
    return df
#########################################
"""
策略名称：
两融双均线策略
运行周期:
日线
==============================================================================
备注：该demo仅支持交易使用
"""
import numpy as np


def initialize(context):
    # 融资融券策略
    # 初始化此策略
    # 设置我们要操作的股票池, 这里我们只操作一支股票
    g.security = '600570.SS'
    # 默认买入股数
    g.amount = 1000
    if not is_trade():
        log.info('两融demo策略无法在回测场景使用')



def before_trading_start(context, data):
    if not is_trade():
        return
    h = get_history(20, '1d', field=['close', 'volume'], security_list=g.security,
                    fq='dypre', include=False, is_dict=True)
    g.close_data = h[g.security]['close']


def handle_data(context, data):
    if not is_trade():
        return
    security = g.security
    # 获取历史日K线数据
    current_price = data[security].close
    # 合成最新K线序列
    close_data = np.concatenate((g.close_data, np.array(list([current_price]))), axis=0)
    # 获取5日、10日均线
    ma5 = get_ma(close_data, 5)
    ma10 = get_ma(close_data, 10)

    # 如果五日均线大于十日均线，进行买入
    if ma5 > ma10:
        # 获取最大可融资数量
        amount = get_margincash_open_amount(security).get(security)
        log.info('最大可融资买入的数量:%s' % amount)
        # 可融资买入最大股数超过目标买入股数则用融资买入方式买入标的
        if amount >= g.amount:
            margincash_open(security, g.amount)
            log.info('融资买入全部')
        # 可融资买入最大股数小于目标买入股数但大于零则用先用融资买入方式买入部分，剩余部分用担保品交易方式进行买入
        elif g.amount > amount > 0:
            margincash_open(security, amount)
            log.info('融资买入部分')
            margin_trade(security, g.amount - amount)
            log.info('担保品买入部分')
        elif amount == 0:
            margin_trade(security, g.amount)
            log.info('担保品买入全部')
        g.flag = False

    # 如果五日均线小于十日均线，进行卖出
    else:
        hold_amount = get_position(security).enable_amount
        if hold_amount > 0:
            # 获取标的卖券还款最大可卖数量
            amount = get_margincash_close_amount(security).get(security)
            log.info('最大可卖券还款卖出的数量:%s' % amount)
            # 如果卖券还款最大数量不小于持仓数量，则进行卖券还款操作
            if amount >= hold_amount:
                margincash_close(security, -amount)
                log.info('卖券还款卖出全部')
            # 如果卖券还款最大数量小于持仓数量，则先进行部分数量的卖券还款操作，剩余通过担保品交易卖出
            elif hold_amount > amount > 0:
                margincash_close(security, -amount)
                log.info('卖券还款卖出部分')
                margin_trade(security, -(hold_amount - amount))
                log.info('担保品卖出部分')
            # 如果卖券还款最大数量为零，则持仓部分用担保品方式卖出
            elif amount == 0:
                margin_trade(security, -hold_amount)
                log.info('担保品卖出全部')


# 获取MA函数
def get_ma(close_array, num):
    ma = close_array[-num:].mean()
    return round(ma, 2)
######################################
"""
策略名称：
期货日内交易策略
运行周期:
分钟
策略流程：
盘中每隔5分钟进行一次RSI短周期与长周期多空共振的判断，决定做开多头仓还是空头仓；
盘中再按照盈利比例进行头寸平仓或者收盘前清算头寸平仓
==============================================================================
备注：该demo仅支持回测场景使用，如在交易场景使用，需要将主力合约代码，如"IF888.CCFX"
替换为当前交易日正处理上市状态的合约代码
"""
# 导入函数库
import numpy as np


# 初始化此策略
def initialize(context):
    # 设置我们要操作的股票池, 这里我们只操作一支股票
    g.ini_buy_flag = False  # 买底仓开关
    g.amount = 1  # 1份标准交易头寸
    g.rate = 0.5  # 做T涨跌幅，1就是1%
    g.L = 50  # 长周期RSI阈值
    g.S = 80  # 短周期RSI阈值
    g.target = 'IF'  # 设置交易标的
    g.security = g.target + '888.CCFX'  # 设置主力合约
    log.info(g.security)
    if not is_trade():
        set_limit_mode('UNLIMITED')
        set_margin_rate(g.target, 0.15)


# 盘前处理
def before_trading_start(context, data):
    g.count = 0
    g.B_T_flag = False  # 做正T开关（先买后卖）
    g.S_T_flag = False  # 做反T开关（先卖后买）
    g.first_buy_flag = False
    g.second_buy_flag = False
    g.trade_flag = True


# 盘中处理
def handle_data(context, data):
    g.count += 1
    k_num = g.count
    if k_num <= 5:
        return
    # 每个5分钟整点进行做T判断
    if k_num % 1 == 0:
        # 获取5分钟K线数据
        h = get_history(100, '1m', field=['close', 'volume'], security_list=g.security,
                        fq=None, include=True, is_dict=True)
        close_array_m = h[g.security]['close']
        # 获取5分钟K线数据
        h = get_history(100, '5m', field=['close', 'volume'], security_list=g.security,
                        fq=None, include=True, is_dict=True)
        close_array_5m = h[g.security]['close']

        if close_array_m.ndim != 0 and close_array_5m.ndim != 0:
            # 获取5分钟、15分钟RSI
            rsi_m = get_rsi(close_array_m, 11)[-1]
            rsi_5m = get_rsi(close_array_5m, 11)[-1]
            # 做T条件判断
            if rsi_5m > g.L and rsi_m > g.S:
                if get_position(g.security).long_amount == 0 and not g.B_T_flag:
                    order_id = buy_open(g.security, g.amount)
                    if order_id is not None:
                        log.info('日内看多开多头仓')
                        log.info('========================')
                        g.B_T_flag = True
                        g.B_T_cost = data[g.security].price
            if rsi_5m < 100 - g.L and rsi_m < 100 - g.S:
                if get_position(g.security).short_amount == 0 and not g.S_T_flag:
                    order_id = sell_open(g.security, g.amount)
                    if order_id is not None:
                        log.info('日内看空开空头仓')
                        log.info('========================')
                        log.info(get_positions())
                        g.S_T_flag = True
                        g.S_T_cost = data[g.security].price
    if g.B_T_flag:
        if data[g.security].price >= g.B_T_cost * (1 + g.rate / 100):
            order_id = sell_close(g.security, 1)
            if order_id is not None:
                log.info('多头仓做T后多头仓平仓')
                log.info('------------------------')
                g.B_T_flag = False
    if g.S_T_flag:
        if data[g.security].price <= g.S_T_cost * (1 - g.rate / 100):
            order_id = buy_close(g.security, 1)
            if order_id is not None:
                log.info('空头仓做T后空头仓平仓')
                log.info('------------------------')
                g.S_T_flag = False
    # 收盘前多次尝试将持仓恢复到开盘持有量
    if k_num == 238:
        log.info('收盘前尝试将持仓恢复到开盘持有量')
        long_pos = get_long_position_list(context)
        short_pos = get_short_position_list(context)
        if long_pos:
            order_id = sell_close(g.security, 1)
            if order_id is not None:
                log.info('收盘多头仓清算')
        if short_pos:
            order_id = buy_close(g.security, 1)
            if order_id is not None:
                log.info('收盘空头仓清算')


# 获取RSI数据
def get_rsi(array_list, periods=14):
    length = len(array_list)
    rsi_values = [np.nan] * length
    if length <= periods:
        return rsi_values
    up_avg = 0
    down_avg = 0

    first_t = array_list[:periods + 1]
    for i in range(1, len(first_t)):
        if first_t[i] >= first_t[i - 1]:
            up_avg += first_t[i] - first_t[i - 1]
        else:
            down_avg += first_t[i - 1] - first_t[i]
    up_avg = up_avg / periods
    down_avg = down_avg / periods
    rs = up_avg / down_avg
    rsi_values[periods] = 100 - 100 / (1 + rs)

    for j in range(periods + 1, length):
        if array_list[j] >= array_list[j - 1]:
            up = array_list[j] - array_list[j - 1]
            down = 0
        else:
            up = 0
            down = array_list[j - 1] - array_list[j]
        up_avg = (up_avg * (periods - 1) + up) / periods
        down_avg = (down_avg * (periods - 1) + down) / periods
        rs = up_avg / down_avg
        rsi_values[j] = 100 - 100 / (1 + rs)
    return rsi_values


# 生成持仓股票列表
def get_long_position_list(context):
    position_list = []
    for code in context.portfolio.positions:
        if context.portfolio.positions[code].long_amount != 0:
            position_list.append(code)
    return position_list


# 生成持仓股票列表
def get_short_position_list(context):
    position_list = []
    for code in context.portfolio.positions:
        if context.portfolio.positions[code].short_amount != 0:
            position_list.append(code)
    return position_list
######################################
"""
策略名称：
期货双均线策略
运行周期:
日线
==============================================================================
备注：该demo仅支持回测场景使用，如在交易场景使用，需要将主力合约代码，如"IF888.CCFX"
替换为当前交易日正处理上市状态的合约代码
"""
import numpy as np


def initialize(context):
    g.target = 'IF'  # 设置交易标的
    # 设置主力合约
    g.security = g.target + '888.CCFX'
    g.amount = 1
    if not is_trade():
        set_limit_mode('UNLIMITED')
        set_margin_rate(g.target, 0.15)


def before_trading_start(context, data):
    h = get_history(20, '1d', field=['close', 'volume'], security_list=g.security,
                    fq='dypre', include=False, is_dict=True)
    g.close_data = h[g.security]['close']


# 当五日均线高于十日均线时开多仓、平空仓，当五日均线低于十日均线时开空仓、平多仓
def handle_data(context, data):
    # 获取历史日K线数据
    current_price = data[g.security].close
    # 合成最新K线序列
    close_data = np.concatenate((g.close_data, np.array(list([current_price]))), axis=0)
    # 获取5日、10日均线
    ma5 = get_ma(close_data, 5)
    ma10 = get_ma(close_data, 10)
    # 五日均线大于十日均线
    if ma5 > ma10:
        if get_position(g.security).long_amount == 0:
            # 开一份多头仓
            order_id = buy_open(g.security, g.amount)
            log.info("开多头仓 %s" % g.security)
        if get_position(g.security).short_amount != 0:
            # 平一份空头仓
            order_id = buy_close(g.security, g.amount)
            log.info("平空头仓 %s" % g.security)

    # 五日均线小于十日均线
    elif ma5 < ma10:
        if get_position(g.security).short_amount == 0:
            # 开一份空头仓
            order_id = sell_open(g.security, g.amount)
            log.info("开空仓 %s" % g.security)
        if get_position(g.security).long_amount != 0:
            # 平一份多头仓
            order_id = sell_close(g.security, g.amount)
            log.info("平多仓 %s" % g.security)


# 获取MA函数
def get_ma(close_array, num):
    ma = close_array[-num:].mean()
    return round(ma, 2)
###########################################
# -*- coding: utf-8 -*-
"""
=============================================================================
小果量化交易 - 回测启动脚本（配置参数 + 完整策略）
=============================================================================
使用说明：
1. 登录 Ptrade 终端，点击“策略” → “新建策略”
2. 复制本文件全部代码到策略编辑器中
3. 修改“回测参数配置”部分的参数
4. 点击“保存”，然后点击“回测”运行
5. 查看回测结果（评价指标、收益曲线、交易日志）
=============================================================================
"""

import numpy as np
import pandas as pd


def initialize(context):
    """
    =============================================================================
    初始化函数（必选）
    =============================================================================
    该函数只在策略启动时运行一次，用于：
    1. 设置股票池
    2. 初始化全局变量
    3. 配置回测参数（佣金、滑点等）
    =============================================================================
    """
    # ========== 回测参数配置（用户可修改） ==========
    # 建议回测参数：
    #   - 起始资金：1,000,000 元以上
    #   - 回测时间：至少1年以上（如2023-01-01 ~ 2023-12-31）
    #   - 回测频率：日线（推荐）或分钟线
    #   - 基准指数：沪深300（000300.SS）
    # ==============================================
    
    # 1. 设置股票池（修改为你的股票代码）
    g.security = '600570.SS'  # 示例：恒生电子
    # g.security = ['600570.SS', '000001.SZ']  # 多只股票示例
    set_universe(g.security)
    
    # 2. 设置回测基准（可选，默认沪深300）
    # 基准用于计算 Alpha、Beta、夏普比率等指标
    set_benchmark('000300.SS')
    
    # 3. 设置佣金费率（可选，默认万分之三，最低5元）
    # 股票佣金 = 成交金额 × 佣金费率（最低5元）
    # ETF/LOF佣金 = 成交金额 × 万分之八
    set_commission(commission_ratio=0.0003, min_commission=5.0)
    
    # 4. 设置滑点（可选，默认0.1%）
    # 滑点 = 委托价格 × 滑点比例 / 2
    # 例如：买入10元股票，滑点0.1%，实际成交价 = 10 + 10×0.001/2 = 10.005
    set_slippage(slippage=0.1)
    
    # 5. 设置固定滑点（可选，与set_slippage二选一）
    # set_fixed_slippage(fixedslippage=0.02)
    
    # 6. 设置成交比例（可选，默认0.25）
    # 单笔最大成交数量 = 本周期市场可成交总量 × 成交比例
    set_volume_ratio(volume_ratio=0.25)
    
    # 7. 设置成交数量限制模式（可选，默认'LIMIT'）
    # 'LIMIT'：限制成交数量，'UNLIMITED'：不限制
    set_limit_mode(limit_mode='LIMIT')
    
    # 8. 初始化全局变量
    g.ma_short = 5      # 短期均线周期
    g.ma_long = 10       # 长期均线周期
    g.is_bought = False  # 买入标记
    g.trade_count = 0    # 交易次数
    
    # 9. 日志输出
    log.info("=" * 50)
    log.info("小果量化交易 - 回测启动")
    log.info("股票池: %s" % g.security)
    log.info("均线参数: MA%d / MA%d" % (g.ma_short, g.ma_long))
    log.info("回测基准: 000300.SS（沪深300）")
    log.info("佣金费率: 万分之三（最低5元）")
    log.info("滑点比例: 0.1%%")
    log.info("成交比例: 0.25")
    log.info("=" * 50)


def handle_data(context, data):
    """
    =============================================================================
    盘中处理函数（必选）
    =============================================================================
    该函数在交易时间内按指定的周期频率运行。
    
    日线级别：每天执行一次（15:00）
    分钟级别：每分钟执行一次（9:31~15:00）
    =============================================================================
    """
    security = g.security
    
    # 1. 获取历史数据
    df = get_history(
        count=g.ma_long + 5,
        frequency='1d',
        field='close',
        security_list=security,
        fq=None,
        include=False
    )
    
    # 2. 检查数据是否足够
    if df is None or len(df) < g.ma_long:
        log.warning("历史数据不足")
        return
    
    # 3. 计算均线
    close_prices = df['close'].values
    ma_short = close_prices[-g.ma_short:].mean()
    ma_long = close_prices[-g.ma_long:].mean()
    
    # 4. 获取当前价格和资金
    current_price = data[security]['close']
    cash = context.portfolio.cash
    position = get_position(security)
    position_amount = 0 if position is None else position.amount
    
    # 5. 交易逻辑
    # 买入条件：金叉 + 未买入 + 有资金
    if ma_short > ma_long and not g.is_bought and cash > 0:
        order_id = order_value(security, cash)
        g.is_bought = True
        g.trade_count += 1
        log.info("【买入】MA%d(%.2f) > MA%d(%.2f), 价格: %.2f, 金额: %.2f" % 
                 (g.ma_short, ma_short, g.ma_long, ma_long, current_price, cash))
    
    # 卖出条件：死叉 + 已买入 + 有持仓
    elif ma_short < ma_long and g.is_bought and position_amount > 0:
        order_id = order_target(security, 0)
        g.is_bought = False
        g.trade_count += 1
        log.info("【卖出】MA%d(%.2f) < MA%d(%.2f), 价格: %.2f, 数量: %d" % 
                 (g.ma_short, ma_short, g.ma_long, ma_long, current_price, position_amount))
    
    # 6. 记录变量
    record(stock_price=current_price)
    record(ma5=ma_short)
    record(ma10=ma_long)


def before_trading_start(context, data):
    """
    =============================================================================
    盘前处理函数（可选）
    =============================================================================
    回测中每个交易日 8:30 执行
    =============================================================================
    """
    log.info("盘前 - 交易日: %s" % context.blotter.current_dt)


def after_trading_end(context, data):
    """
    =============================================================================
    盘后处理函数（可选）
    =============================================================================
    回测中每天交易结束后执行
    =============================================================================
    """
    log.info("盘后 - 总资产: %.2f, 可用资金: %.2f, 收益率: %.2f%%" % 
             (context.portfolio.portfolio_value, 
              context.portfolio.cash,
              context.portfolio.returns * 100))
# 全部接口
'''
新建策略
开始回测和交易前需要先新建策略，点击下图中左上角标识进行策略添加。可以选择不同的业务类型(比如股票)，然后给策略设定一个名称，添加成功后可以在默认策略模板基础上进行策略编写。



新建回测
策略添加完成后就可以开始进行回测操作了。回测之前需要对开始时间、结束时间、回测资金、回测基准、回测频率几个要素进行设定，设定完毕后点击保存。然后再点击回测按键，系统就会开始运行回测，回测的评价指标、收益曲线、日志都会在界面中展现。



新建交易
交易界面点击新增按键进行新增交易操作，策略方案中的对象为所有策略列表中的策略，给本次交易设定名称并点击确定后系统就开始运行交易了。



交易开始运行后，可以实时看到总资产和可用资金情况，同时可以在交易列表查询交易状态。



交易开始运行后，可以点击交易详情，查看策略评价指标、交易明细、持仓明细、交易日志。



策略运行周期
回测支持日线级别、分钟级别运行，详见handle_data方法。

交易支持日线级别、分钟级别、tick级别运行，日线级别和分钟级别详见handle_data方法，tick级别运行详见run_interval和tick_data方法。

频率：日线级别

当选择日线频率时，回测和交易都是每天运行一次，回测运行时间为每个交易日的15:00，交易运行时间为尾盘固定时间(允许券商可配)，默认为14:50分。

频率：分钟级别

当选择分钟频率时，回测和交易都是每分钟运行一次，运行时间为每根分钟K线结束。

频率：tick级别

当选择tick频率时，交易最小频率可以达到3秒运行一次。

策略运行时间
盘前运行:

9:30分钟之前为盘前运行时间，交易环境支持运行在run_daily中指定交易时间(如time='09:15')运行的函数；回测环境和交易环境支持运行before_trading_start函数

盘中运行:

9:31(回测)/9:30(交易)~15:00分钟为盘中运行时间，分钟级别回测环境和交易环境支持运行在run_daily中指定交易时间(如time='14:30')运行的函数；回测环境和交易环境支持运行handle_data函数；交易环境支持运行run_interval函数和tick_data函数

盘后运行:

15:30分钟为盘后运行时间，回测环境和交易环境支持运行after_trading_end函数(该函数为定时运行)；15:00之后交易环境支持运行在run_daily中指定交易时间(如time='15:10')运行的函数

交易策略委托下单时间
使用order系列接口进行股票委托下单，将直接报单到柜台。

回测支持业务类型
目前所支持的业务类型:

1.普通股票买卖(单位：股)。

2.可转债买卖(单位：张，T+0)。

3.融资融券担保品买卖(单位：股)。

4.期货投机类型交易(单位：手，T+0)。

5.LOF基金买卖(单位：股)。

6.ETF基金买卖(单位：股)。

交易支持业务类型
目前所支持的业务类型:

1.普通股票买卖(单位：股)。

2.可转债买卖(具体单位请咨询券商，T+0)。

3.融资融券交易(单位：股)。

4.ETF申赎、套利(单位：份)。

5.国债逆回购(单位：份)。

6.期货投机类型交易(单位：手，T+0)。

7.LOF基金买卖(单位：股)。

8.ETF基金买卖(单位：股)。

交易标的对应最小价差
1.股票买卖(最小价差：0.01)。

2.可转债买卖(最小价差：0.001)。

3.LOF买卖(最小价差：0.001)。

4.ETF买卖(最小价差：0.001)。

5.国债逆回购(最小价差：0.005)。

6.股指期货投机类型交易(最小价差：0.2)。

7.国债期货投机类型交易(最小价差：0.005)。

开始写策略
简单但是完整的策略
先来看一个简单但是完整的策略:

def initialize(context):
    set_universe('600570.SS')

def handle_data(context, data):
    pass
一个完整策略只需要两步:

set_universe: 设置股票池，上面的例子中，只操作一支股票: '600570.SS'，恒生电子。所有的操作只能对股票池的标的进行。
实现一个函数: handle_data。
这是一个完整的策略，但是我们没有任何交易，下面我们来添加一些交易

添加一些交易
def initialize(context):
    g.security = '600570.SS'
    # 是否创建订单标识
    g.flag = False
    set_universe(g.security)

def handle_data(context, data):
    if not g.flag:
        order(g.security, 1000)
        g.flag = True
在这个策略里，当创建订单标识为False，也即尚未创建过订单时，买入1000股'600570.SS'，具体的下单API请看order函数。这里我们进行了交易，但只是没有经过条件判断的委托下达。

实用的策略
下面我们来看一个真正实用的策略

在这个策略里，我们会根据历史价格做出判断:

如果上一时间点价格高出五天平均价1%，则全仓买入
如果上一时间点价格低于五天平均价，则清仓卖出
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def handle_data(context, data):
    security = g.security
    sid = g.security

    # 获取过去五天的历史价格
    df = get_history(5, '1d', 'close', security, fq=None, include=False)

    # 获取过去五天的平均价格
    average_price = round(df['close'][-5:].mean(), 3)

    # 获取上一时间点价格
    current_price = data[sid]['close']

    # 获取当前的现金
    cash = context.portfolio.cash

    # 如果上一时间点价格高出五天平均价1%, 则全仓买入
    if current_price > 1.01*average_price:
        # 用所有 cash 买入股票
        order_value(g.security, cash)
        log.info('buy %s' % g.security)
    # 如果上一时间点价格低于五天平均价, 则清仓卖出
    elif current_price < average_price and get_position(security).amount > 0:
        # 卖出所有股票,使这只股票的最终持有量为0
        order_target(g.security, 0)
        log.info('sell %s' % g.security)
模拟盘和实盘注意事项
关于持久化
为什么要做持久化处理
服务器异常、策略优化等诸多场景，都会使得正在进行的模拟盘和实盘策略存在中断后再重启的需求，但是一旦交易中止后，策略中存储在内存中的全局变量就清空了，因此通过持久化处理为量化交易保驾护航必不可少。

量化框架持久化处理
使用pickle模块保存股票池、账户信息、订单信息、全局变量g定义的变量等内容。

注意事项：

框架会在before_trading_start(隔日开始)、handle_data、after_trading_end事件后触发持久化信息更新及保存操作。
券商升级/环境重启后恢复交易时，框架会先执行策略initialize函数再执行持久化信息恢复操作。 如果持久化信息保存有策略定义的全局对象g中的变量，将会以持久化信息中的变量覆盖掉initialize函数中初始化的该变量。
全局变量g中不能被序列化的变量将不会被保存。您可在initialize中初始化该变量时名字以'__'开头。
涉及到IO(打开的文件，实例化的类对象等)的对象是不能被序列化的。
全局变量g中以'__'开头的变量为私有变量，持久化时将不会被保存。
示例
class Test(object):
    count = 5

    def print_info(self):
        self.count += 1
        log.info("a" * self.count)


def initialize(context):
    g.security = "600570.SS"
    set_universe(g.security)
    # 初始化无法被序列化类对象，并赋值为私有变量，落地持久化信息时跳过保存该变量
    g.__test_class = Test()

def handle_data(context, data):
    # 调用私有变量中定义的方法
    g.__test_class.print_info()
策略中持久化处理方法
使用pickle模块保存 g 对象(全局变量)。

示例
import pickle
from collections import defaultdict
'''
持仓N日后卖出，仓龄变量每日pickle进行保存，重启策略后可以保证逻辑连贯
'''
def initialize(context):
    g.notebook_path = get_research_path()
    #尝试启动pickle文件
    try:
        with open(g.notebook_path+'hold_days.pkl','rb') as f:
            g.hold_days = pickle.load(f)
    #定义空的全局字典变量
    except:
        g.hold_days = defaultdict(list)
    g.security = '600570.SS'
    set_universe(g.security)

# 仓龄增加一天
def before_trading_start(context, data):
    if g.hold_days:
        g.hold_days[g.security] += 1

# 每天将存储仓龄的字典对象进行pickle保存
def handle_data(context, data):
    if g.security not in list(context.portfolio.positions.keys()) and g.security not in g.hold_days:
        order(g.security, 100)
        g.hold_days[g.security] = 1
    if g.hold_days:
        if g.hold_days[g.security] > 5:
            order(g.security, -100)
            del g.hold_days[g.security]
    with open(g.notebook_path+'hold_days.pkl','wb') as f:
        pickle.dump(g.hold_days,f,-1)
策略中支持的代码尾缀
市场品种	尾缀全称	尾缀简称
上海市场证券	XSHG	SS
深圳市场证券	XSHE	SZ
指数	XBHS	
中金所期货	CCFX	
关于异常处理
为什么要做异常处理
交易场景数据缺失等原因会导致策略运行过程中常规的处理出现语法错误，导致策略终止，所以需要做一些异常处理的保护。以下是一些基本的处理方法介绍。

示例
try:
    # 尝试执行的代码
    print(a)
except:
    # 如果在try块执行异常
    # 则执行except块代码
    a = 1
    print(a)
try:
    # 尝试执行的代码
    print(a)
except Exception as e:
    # 使用as关键字可以获取异常的实例
    print("出现异常，error为: %s" % e)
    a = 1
    print(a)
try:
    a = 1
    print(a)
except:
    print(a)
else:
    # 如果try块成功执行，没有引发异常，可以选择性地添加一个else块。
    print('执行正常')
try:
    a = 1
    print(a)
except:
    print(a)
finally:
    # 无论是否发生异常，finally块中的代码都将被执行。这可以用来执行一些清理工作，比如关闭文件或释放资源。
    print('执行完毕')
关于限价交易的价格
可转债、ETF、LOF的价格是小数点三位。

股票的价格是小数点两位。

股指期货的价格是小数点一位。

用户在使用限价单委托（如order()入参limit_price）和市价委托保护限价（order_market()入参limit_price）的场景时务必要对入参价格的小数点位数进行处理，否则会导致委托失败。

策略引擎简介
业务流程框架
ptrade量化引擎以事件触发为基础，通过初始化事件(initialize)、盘前事件(before_trading_start)、盘中事件(handle_data)、盘后事件(after_trading_end)来完成每个交易日的策略任务。

initialize和handle_data是一个允许运行策略的最基础结构，也就是必选项，before_trading_start和after_trading_end是可以按需运行的。

handle_data仅满足日线和分钟级别的盘中处理，tick级别的盘中处理则需要通过tick_data或者run_interval来实现。

ptrade还支持委托主推事件(on_order_response)、交易主推事件(on_trade_response)，可以通过委托和成交的信息来处理策略逻辑，是tick级的一个补充。

除了以上的一些事件以外，ptrade也支持通过定时任务来运行策略逻辑，可以通过run_daily接口实现。



initialize(必选)
initialize(context)
使用场景
该函数仅在回测、交易模块可用

接口说明
该函数用于初始化一些全局变量，是策略运行的唯二必须定义函数之一。

注意事项：

该函数只会在回测和交易启动的时候运行一次。
可调用接口
set_universe(回测/交易)	set_benchmark(回测/交易)	set_commission(回测)	set_fixed_slippage(回测)	set_slippage(回测)
set_volume_ratio(回测)	set_limit_mode(回测)	set_yesterday_position(回测)	set_parameters(回测/交易)	run_daily(回测/交易)
run_interval(交易)	convert_position_from_csv(回测)	get_user_name(回测/交易)	get_research_path(回测/交易)	get_trade_name(交易)
set_future_commission(回测(期货))	set_margin_rate(回测(期货))	log(回测/交易)	is_trade(回测/交易)	permission_test(交易)
create_dir(研究/回测/交易)	get_frequency(回测/交易)	get_business_type(回测/交易)	set_email_info(交易)
参数
context: Context对象，存放有当前的账户及持仓信息；

返回
None

示例
def initialize(context):
    #g为全局对象
    g.security = '600570.SS'
    set_universe(g.security)

def handle_data(context, data):
    order('600570.SS',100)
before_trading_start(可选)
before_trading_start(context, data)
使用场景
该函数仅在回测、交易模块可用

接口说明
该函数在每天开始交易前被调用一次，用于添加每天都要初始化的信息，如无盘前初始化需求，该函数可以在策略中不做定义。

注意事项：

在回测中，该函数在每个回测交易日8:30分执行。
在交易中，该函数在开启交易时立即执行，从隔日开始每天9:10分(默认)执行。
当在9:10前开启交易时，受行情未更新原因在该函数内调用实时行情接口会导致数据有误。 可通过在该函数内sleep至9:10分或调用实时行情接口改为run_daily执行等方式进行避免。
可调用接口
set_parameters(回测/交易)	get_trading_day(回测/交易)	get_all_trades_days(研究/回测/交易)	get_trade_days(研究/回测/交易)	get_trading_day_by_date(研究/回测/交易)
get_market_list(研究/回测/交易)	get_market_detail(研究/回测/交易)	get_history(研究/回测/交易)	get_price(研究/回测/交易)	get_individual_entrust(交易)
get_individual_transaction(交易)	get_tick_direction(交易)	get_sort_msg(交易)	get_underlying_code(交易)	get_etf_info(交易)
get_etf_stock_info(交易)	get_gear_price(交易)	get_snapshot(交易)	get_cb_info(研究/交易)	get_trend_data(研究/回测/交易)
get_stock_name(研究/回测/交易)	get_stock_info(研究/回测/交易)	get_stock_status(研究/回测/交易)	get_stock_exrights(研究/回测/交易)	get_stock_blocks(研究/回测/交易)
get_index_stocks(研究/回测/交易)	get_etf_stock_list(交易)	get_industry_stocks(研究/回测/交易)	get_fundamentals(研究/回测/交易)	get_Ashares(研究/回测/交易)
get_etf_list(交易)	get_ipo_stocks(交易)	get_position(回测/交易)	get_positions(回测/交易)	get_all_positions(交易)
get_trades_file(回测)	get_deliver(交易)	get_fundjour(交易)	get_lucky_info(交易)	order(回测/交易)
order_target(回测/交易)	order_value(回测/交易)	order_target_value(回测/交易)	order_market(交易)	ipo_stocks_order(交易)
etf_basket_order(交易)	etf_purchase_redemption(交易)	cancel_order(回测/交易)	cancel_order_ex(交易)	debt_to_stock_order(交易)
get_open_orders(回测/交易)	get_order(回测/交易)	get_orders(回测/交易)	get_all_orders(交易)	get_trades(回测/交易)
margin_trade(回测/交易)	margincash_open(交易)	margincash_close(交易)	margincash_direct_refund(交易)	marginsec_open(交易)
marginsec_close(交易)	marginsec_direct_refund(交易)	get_margincash_stocks(交易)	get_marginsec_stocks(交易)	get_margin_contract(交易)
get_margin_contractreal(交易)	get_margin_asset(交易)	get_assure_security_list(交易)	get_margincash_open_amount(交易)	get_margincash_close_amount(交易)
get_marginsec_open_amount(交易)	get_marginsec_close_amount(交易)	get_margin_entrans_amount(交易)	get_enslo_security_info(交易)	buy_open(回测/交易(期货))
sell_close(回测/交易(期货))	sell_open(回测/交易(期货))	buy_close(回测/交易(期货))	get_margin_rate(回测(期货))	get_instruments(回测/交易(期货))
get_dominant_contract(研究/回测/交易(期货))
get_MACD(回测/交易)	get_KDJ(回测/交易)	get_RSI(回测/交易)	get_CCI(回测/交易)
log(回测/交易)	check_limit(回测/交易)	send_email(交易)	send_qywx(交易)	permission_test(交易)
create_dir(研究/回测/交易)	filter_stock_by_status(研究/回测/交易)	get_cb_list(交易)	get_reits_list(研究/回测/交易)	get_crdt_fund(交易)
fund_transfer(交易)	market_fund_transfer(交易)
参数
context: Context对象，存放有当前的账户及持仓信息；

data：保留字段暂无数据；

返回
None

示例
def initialize(context):
    #g为全局变量
    g.security = '600570.SS'
    set_universe(g.security)

def before_trading_start(context, data):
    log.info(g.security)

def handle_data(context, data):
    order('600570.SS',100)
handle_data(必选)
handle_data(context, data)
使用场景
该函数仅在回测、交易模块可用

接口说明
该函数在交易时间内按指定的周期频率运行，是用于处理策略交易的主要模块，根据策略保存时的周期参数分为每分钟运行和每天运行，是策略运行的唯二必须定义函数之一。

注意事项：

该函数每个单位周期执行一次
如果是日线级别策略，每天执行一次。股票回测场景下，在15:00执行；股票交易场景下，执行时间为券商实际配置时间。
如果是分钟级别策略，每分钟执行一次，股票回测场景下，执行时间为9:31 -- 15:00，股票交易场景下，执行时间为9:30 -- 14:59。
回测与交易中，handle_data函数不会在非交易日触发(如回测或交易起始日期为2015年12月21日，则策略在2016年1月1日-3日时， handle_data不会运行，4日继续运行)。
可调用接口
set_parameters(回测/交易)	get_trading_day(回测/交易)	get_all_trades_days(研究/回测/交易)	get_trade_days(研究/回测/交易)	get_trading_day_by_date(研究/回测/交易)
get_history(研究/回测/交易)	get_price(研究/回测/交易)	get_individual_entrust(交易)	get_individual_transaction(交易)	get_tick_direction(交易)
get_sort_msg(交易)	get_underlying_code(交易)	get_etf_info(交易)	get_etf_stock_info(交易)	get_gear_price(交易)
get_snapshot(交易)	get_cb_info(研究/交易)	get_trend_data(研究/回测/交易)	get_stock_name(研究/回测/交易)	get_stock_info(研究/回测/交易)
get_stock_status(研究/回测/交易)	get_stock_exrights(研究/回测/交易)	get_stock_blocks(研究/回测/交易)	get_index_stocks(研究/回测/交易)	get_etf_stock_list(交易)
get_industry_stocks(研究/回测/交易)	get_fundamentals(研究/回测/交易)	get_Ashares(研究/回测/交易)	get_etf_list(交易)	get_ipo_stocks(交易)
get_cb_list(交易)	get_reits_list(研究/回测/交易)	get_position(回测/交易)	get_positions(回测/交易)	get_all_positions(交易)
order(回测/交易)	order_target(回测/交易)	order_value(回测/交易)	order_target_value(回测/交易)	order_market(交易)
ipo_stocks_order(交易)	after_trading_order(交易)	after_trading_cancel_order(交易)	etf_basket_order(交易)	etf_purchase_redemption(交易)
cancel_order(回测/交易)	cancel_order_ex(交易)	debt_to_stock_order(交易)	get_open_orders(回测/交易)	get_order(回测/交易)
get_orders(回测/交易)	get_all_orders(交易)	get_trades(回测/交易)	margin_trade(回测/交易)	margincash_open(交易)
margincash_close(交易)	margincash_direct_refund(交易)	marginsec_open(交易)	marginsec_close(交易)	marginsec_direct_refund(交易)
get_margin_contract(交易)	get_margin_contractreal(交易)	get_margin_asset(交易)	get_assure_security_list(交易)	get_margincash_open_amount(交易)
get_margincash_close_amount(交易)	get_marginsec_open_amount(交易)	get_marginsec_close_amount(交易)	get_margin_entrans_amount(交易)	get_enslo_security_info(交易)
buy_open(回测/交易(期货))	sell_close(回测/交易(期货))	sell_open(回测/交易(期货))	buy_close(回测/交易(期货))
get_MACD(回测/交易)	get_KDJ(回测/交易)	get_RSI(回测/交易)	get_CCI(回测/交易)	log(回测/交易)
check_limit(回测/交易)	send_email(交易)	send_qywx(交易)	create_dir(研究/回测/交易)	get_current_kline_count(研究/回测/交易)
get_dominant_contract(研究/回测/交易(期货))	get_crdt_fund(交易)	fund_transfer(交易)	market_fund_transfer(交易)
参数
context: Context对象，存放有当前的账户及持仓信息；

data：是一个类对象，实现了类似字典的通过key获取value的方法，可以通过股票代码获取代码对应的BarData对象，对象中包含当前周期(日线策略是当天，分钟策略是当前分钟)的数据；

注意：为了加速，data中的数据只包含股票池中所订阅标的的信息，可使用data[security]的方式来获取当前周期对应的标的信息；

返回
None

示例
def initialize(context):
    #g为全局变量
    g.security = '600570.SS'
    set_universe(g.security)

def handle_data(context, data):
    # 通过data对象获取股票当前周期最新价
    current_price = data[g.security].price
    # 用当前最新价委托下单
    order('600570.SS', 100, limit_price=current_price)
after_trading_end(可选)
after_trading_end(context, data)
使用场景
该函数仅在回测、交易模块可用

接口说明
该函数会在每天交易结束之后调用，用于处理每天收盘后的操作，如无盘后处理需求，该函数可以在策略中不做定义。

注意事项：

该函数只会执行一次
该函数执行时间为由券商配置决定，一般为15:30。
可调用接口
set_parameters(回测/交易)	get_trading_day(回测/交易)	get_all_trades_days(研究/回测/交易)	get_trade_days(研究/回测/交易)	get_trading_day_by_date(研究/回测/交易)
get_market_list(研究/回测/交易)	get_market_detail(研究/回测/交易)	get_history(研究/回测/交易)	get_price(研究/回测/交易)	get_individual_entrust(交易)
get_individual_transaction(交易)	get_tick_direction(交易)	get_sort_msg(交易)	get_underlying_code(交易)	get_etf_info(交易)
get_etf_stock_info(交易)	get_gear_price(交易)	get_snapshot(交易)	get_cb_info(研究/交易)	get_trend_data(研究/回测/交易)
get_stock_name(研究/回测/交易)	get_stock_info(研究/回测/交易)	get_stock_status(研究/回测/交易)	get_stock_exrights(研究/回测/交易)	get_stock_blocks(研究/回测/交易)
get_index_stocks(研究/回测/交易)	get_etf_stock_list(交易)	get_industry_stocks(研究/回测/交易)	get_fundamentals(研究/回测/交易)	get_Ashares(研究/回测/交易)
get_etf_list(交易)	get_ipo_stocks(交易)	get_position(回测/交易)	get_positions(回测/交易)	get_all_positions(交易)
get_trades_file(回测)	get_deliver(交易)	get_fundjour(交易)	get_lucky_info(交易)	order(回测/交易)
order_target(回测/交易)	order_value(回测/交易)	order_target_value(回测/交易)	order_market(交易)	ipo_stocks_order(交易)
etf_basket_order(交易)	etf_purchase_redemption(交易)	cancel_order(回测/交易)	cancel_order_ex(交易)	debt_to_stock_order(交易)
get_open_orders(回测/交易)	get_order(回测/交易)	get_orders(回测/交易)	get_all_orders(交易)	get_trades(回测/交易)
margin_trade(回测/交易)	margincash_open(交易)	margincash_close(交易)	margincash_direct_refund(交易)	marginsec_open(交易)
marginsec_close(交易)	marginsec_direct_refund(交易)	get_margincash_stocks(交易)	get_marginsec_stocks(交易)	get_margin_contract(交易)
get_margin_contractreal(交易)	get_margin_asset(交易)	get_assure_security_list(交易)	get_margincash_open_amount(交易)	get_margincash_close_amount(交易)
get_marginsec_open_amount(交易)	get_marginsec_close_amount(交易)	get_margin_entrans_amount(交易)	get_enslo_security_info(交易)	buy_open(回测/交易(期货))
sell_close(回测/交易(期货))	sell_open(回测/交易(期货))	buy_close(回测/交易(期货))	get_margin_rate(回测(期货))	get_instruments(回测/交易(期货))
get_dominant_contract(研究/回测/交易(期货))
get_MACD(回测/交易)	get_KDJ(回测/交易)	get_RSI(回测/交易)	get_CCI(回测/交易)
log(回测/交易)	check_limit(回测/交易)	send_email(交易)	send_qywx(交易)	permission_test(交易)
create_dir(研究/回测/交易)	filter_stock_by_status(研究/回测/交易)	get_cb_list(交易)	get_reits_list(研究/回测/交易)	after_trading_order(交易)
after_trading_cancel_order(交易)	get_crdt_fund(交易)	fund_transfer(交易)	market_fund_transfer(交易)
参数
context: Context对象，存放有当前的账户及持仓信息；

data：保留字段暂无数据；

返回
None

示例
def initialize(context):
    #g为全局变量
    g.security = '600570.SS'
    set_universe(g.security)

def handle_data(context, data):
    order('600570.SS',100)

def after_trading_end(context, data):
    log.info(g.security)
tick_data(可选)
tick_data(context, data)
使用场景
该函数仅交易模块可用

接口说明
该函数可以用于处理tick级别策略的交易逻辑，每隔3秒执行一次，如无tick处理需求，该函数可以在策略中不做定义。

注意事项：

该函数执行时间为9:30 -- 14:59。
该函数中的data和handle_data函数中的data是不一样的，请勿混肴。
参数data中包含的逐笔委托，逐笔成交数据需开通level2行情才能获取到数据，否则对应数据返回None。
参数data中的tick数据取自get_snapshot()并转换为DataFrame格式， 如要更快速的获取快照强烈建议直接使用get_snapshot()获取。
当调用set_parameters()并设置tick_data_no_l2="1"时， 参数data中将不包含逐笔委托、逐笔成交字段，当券商有l2行情时配置该参数可提升data取速；
当策略执行时间超过3s时，将会丢弃中间堵塞的tick_data。
在收盘后，将会清空队列中未执行的tick_data。
参数data中包含的逐笔委托，逐笔成交数据正常返回DataFrame格式，异常时返回None。
可调用接口
set_parameters(回测/交易)	get_trading_day(回测/交易)	get_all_trades_days(研究/回测/交易)	get_trade_days(研究/回测/交易)	get_trading_day_by_date(研究/回测/交易)
get_history(研究/回测/交易)	get_price(研究/回测/交易)	get_individual_entrust(交易)	get_individual_transaction(交易)	get_tick_direction(交易)
get_sort_msg(交易)	get_underlying_code(交易)	get_etf_info(交易)	get_etf_stock_info(交易)	get_gear_price(交易)
get_snapshot(交易)	get_cb_info(研究/交易)	get_trend_data(研究/回测/交易)	get_stock_name(研究/回测/交易)	get_stock_info(研究/回测/交易)
get_stock_status(研究/回测/交易)	get_stock_exrights(研究/回测/交易)	get_stock_blocks(研究/回测/交易)	get_index_stocks(研究/回测/交易)	get_etf_stock_list(交易)
get_industry_stocks(研究/回测/交易)	get_fundamentals(研究/回测/交易)	get_Ashares(研究/回测/交易)	get_etf_list(交易)	get_ipo_stocks(交易)
get_cb_list(交易)	get_reits_list(研究/回测/交易)	get_position(回测/交易)	get_positions(回测/交易)	get_all_positions(交易)
order(回测/交易)	order_target(回测/交易)	order_value(回测/交易)	order_target_value(回测/交易)	order_market(交易)
ipo_stocks_order(交易)	after_trading_order(交易)	after_trading_cancel_order(交易)	etf_basket_order(交易)	etf_purchase_redemption(交易)
cancel_order(回测/交易)	cancel_order_ex(交易)	debt_to_stock_order(交易)	get_open_orders(回测/交易)	get_order(回测/交易)
get_orders(回测/交易)	get_all_orders(交易)	get_trades(回测/交易)	margin_trade(回测/交易)	margincash_open(交易)
margincash_close(交易)	margincash_direct_refund(交易)	marginsec_open(交易)	marginsec_close(交易)	marginsec_direct_refund(交易)
get_margin_contract(交易)	get_margin_contractreal(交易)	get_margin_asset(交易)	get_assure_security_list(交易)	get_margincash_open_amount(交易)
get_margincash_close_amount(交易)	get_marginsec_open_amount(交易)	get_marginsec_close_amount(交易)	get_margin_entrans_amount(交易)	get_enslo_security_info(交易)
buy_open(回测/交易(期货))	sell_close(回测/交易(期货))	sell_open(回测/交易(期货))	buy_close(回测/交易(期货))
get_MACD(回测/交易)	get_KDJ(回测/交易)	get_RSI(回测/交易)	get_CCI(回测/交易)	log(回测/交易)
check_limit(回测/交易)	send_email(交易)	send_qywx(交易)	create_dir(研究/回测/交易)	order_tick(交易)
get_dominant_contract(研究/回测/交易(期货))	get_crdt_fund(交易)	fund_transfer(交易)	market_fund_transfer(交易)
参数
context: Context对象，存放有当前的账户及持仓信息；

data: 一个字典(dict)，key为对应的标的代码(如：'600570.SS')，value为一个字典(dict)，包含order(逐笔委托)、tick(当前tick数据)、transaction(逐笔成交)三项

结构如下：

{'股票代码':
    {
        'order(最近一条逐笔委托)':DataFrame/None,
        'tick(当前tick数据)':DataFrame,
        'transaction(最近一条逐笔成交)':DataFrame/None,
    }
}
每项具体介绍：

order - 逐笔委托对应DataFrame包含字段：
    business_time：时间戳毫秒级
    hq_px：价格
    business_amount：委托量
    order_no：委托编号
    business_direction：成交方向
    trans_kind：委托类型
tick - tick数据对应DataFrame包含字段：
    amount：持仓量(期货字段,股票返回0)；
    bid_grp：买档位，dict类型，内容如：{1:[42.71,200,0],2:[42.74,200,0],3:[42.75,700,...，以档位为Key，以list为Value，每个Value包含：委托价格、委托数量和委托笔数；
    business_amount：成交数量；
    business_amount_in：内盘成交量；
    business_amount_out：外盘成交量；
    business_balance：成交金额；
    business_count：成交笔数；
    circulation_amount：流通股本；
    current_amount：最近成交量(现手)；
    down_px：跌停价格；
    end_trade_date：最后交易日；
    entrust_diff：委差；
    entrust_rate：委比；
    high_px：最高价；
    hsTimeStamp：时间戳，格式为YYYYMMDDHHMISS，如20170711141612，表示2017年7月11日14时16分12秒的tick数据信息；
    last_px：最新成交价；
    low_px：最低价；
    offer_grp：卖档位，dict类型，内容如：{1:[42.71,200,0],2:[42.74,200,0],3:[42.75,700,...，以档位为Key，以list为Value，每个Value包含：委托价格、委托数量和委托笔数；
    open_px：今开盘价；
    pb_rate：市净率；
    pe_rate：动态市盈率；
    preclose_px：昨收价；
    prev_settlement：昨结算(期货字段,股票返回0.0)；
    px_change_rate: 涨跌幅；
    settlement：结算价(期货字段,股票返回0.0)；
    start_trade_date：首个交易日；
    tick_size：最小报价单位；
    total_bid_turnover: 委买金额；
    total_bidqty: 委买量；
    total_offer_turnover: 委卖金额；
    total_offerqty: 委卖量；
    trade_mins：交易时间，距离开盘已过交易时间，如100则表示每日240分钟交易时间中的第100分钟；
    trade_status：交易状态；
    turnover_ratio：换手率；
    up_px：涨停价格；
    vol_ratio：量比；
    wavg_px：加权平均价；
transaction - 逐笔成交对应DataFrame包含字段：
    business_time：时间戳毫秒级；
    hq_px：价格；
    business_amount：成交量；
    trade_index：成交编号；
    business_direction：成交方向；
    buy_no: 叫买方编号；
    sell_no: 叫卖方编号；
    trans_flag: 成交标记；
    trans_identify_am: 盘后逐笔成交序号标识；
    channel_num: 成交通道信息；
返回

None

示例
import ast
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def tick_data(context,data):
    # 获取买一价
    security = g.security
    current_price = ast.literal_eval(data[security]['tick']['bid_grp'][0])[1][0]
    log.info(current_price)
    # 获取买二价
    # current_price = ast.literal_eval(data[security]['tick']['bid_grp'][0])[2][0]
    # 获取买三量
    # current_amount = ast.literal_eval(data[security]['tick']['bid_grp'][0])[3][1]
    # 获取tick最高价
    # current_high_price = data[security]['tick']['high_px'][0]
    # 获取最近一笔逐笔成交的成交量
    # transaction = data[security]["transaction"]
    # business_amount = list(transaction["business_amount"])
    # if len(business_amount) > 0:
    #     log.info("最近一笔逐笔成交的成交量：%s" % business_amount[0])
    # 获取最近一笔逐笔委托的委托类型
    # order = data[security]["order"]
    # trans_kind = list(order["trans_kind"])
    # if len(trans_kind) > 0:
    #     log.info("最近一笔逐笔委托的委托类型：%s" % trans_kind[0])
    if current_price > 38.19:
        # 按买一档价格下单
        order_tick(security, 100, 1)

def handle_data(context, data):
    pass
on_order_response(可选)-委托主推
on_order_response(context, order_list)
使用场景
该函数仅在交易模块可用，对接jz_ufx不支持该函数

接口说明
该函数会在委托主推回调时响应，比引擎、get_order()和get_orders()函数更新Order状态的速度更快，适合对速度要求比较高的策略。

注意事项：

目前可接收股票、可转债、ETF、LOF、期货代码的主推数据。
当接到策略外交易产生的主推时(需券商配置默认不推送)，由于没有对应的Order对象，主推信息中order_id字段赋值为""。
当主推先于委托应答返回时，由于无法根据entrust_no匹配对应的Order对象，主推信息中order_id字段赋值为""。
当在主推里调用委托接口时，需要进行判断处理避免无限迭代循环问题。
当券商配置接收策略外交易产生的主推且策略调用set_parameters()并设置receive_other_response="1"时， 策略中将接收非本交易产生的主推。
当策略调用set_parameters()并设置receive_cancel_response="1"， 策略接收到撤单成交主推时，主推信息中的order_id为买入或卖出委托Order对象的order_id，entrust_no为撤单委托的委托编号。
撤单委托主推信息中成交数量均处理为正数。
可调用委托接口
set_parameters(回测/交易)	get_history(研究/回测/交易)	get_price(研究/回测/交易)	get_individual_entrust(交易)	get_individual_transaction(交易)
get_tick_direction(交易)	get_sort_msg(交易)	get_underlying_code(交易)	get_etf_info(交易)	get_etf_stock_info(交易)
get_gear_price(交易)	get_snapshot(交易)	get_cb_info(研究/交易)	get_trend_data(研究/回测/交易)	get_stock_name(研究/回测/交易)
get_stock_info(研究/回测/交易)	get_stock_status(研究/回测/交易)	get_stock_exrights(研究/回测/交易)	get_stock_blocks(研究/回测/交易)	get_index_stocks(研究/回测/交易)
get_etf_stock_list(交易)	get_industry_stocks(研究/回测/交易)	get_fundamentals(研究/回测/交易)	get_Ashares(研究/回测/交易)	get_etf_list(交易)
get_ipo_stocks(交易)	get_cb_list(交易)	get_reits_list(研究/回测/交易)	get_position(回测/交易)	get_positions(回测/交易)
get_all_positions(交易)	order(回测/交易)	order_target(回测/交易)	order_value(回测/交易)	order_target_value(回测/交易)
order_market(交易)	ipo_stocks_order(交易)	after_trading_order(交易)	after_trading_cancel_order(交易)	etf_basket_order(交易)
etf_purchase_redemption(交易)	cancel_order(回测/交易)	cancel_order_ex(交易)	debt_to_stock_order(交易)	get_open_orders(回测/交易)
get_order(回测/交易)	get_orders(回测/交易)	get_all_orders(交易)	get_trades(回测/交易)	margin_trade(回测/交易)
margincash_open(交易)	margincash_close(交易)	margincash_direct_refund(交易)	marginsec_open(交易)	marginsec_close(交易)
marginsec_direct_refund(交易)	get_margin_contract(交易)	get_margin_contractreal(交易)	get_margin_asset(交易)	get_assure_security_list(交易)
get_margincash_open_amount(交易)	get_margincash_close_amount(交易)	get_marginsec_open_amount(交易)	get_marginsec_close_amount(交易)	get_margin_entrans_amount(交易)
get_enslo_security_info(交易)	buy_open(回测/交易(期货))	sell_close(回测/交易(期货))	sell_open(回测/交易(期货))	buy_close(回测/交易(期货))
get_MACD(回测/交易)	get_KDJ(回测/交易)	get_RSI(回测/交易)	get_CCI(回测/交易)
log(回测/交易)	check_limit(回测/交易)	send_email(交易)	send_qywx(交易)	create_dir(研究/回测/交易)
get_dominant_contract(研究/回测/交易(期货))	get_crdt_fund(交易)	fund_transfer(交易)	market_fund_transfer(交易)
参数
context: Context对象，存放有当前的账户及持仓信息；

order_list：一个列表，当前委托单发生变化时，发生变化的委托单列表。委托单以字典形式展现，内容包括：'entrust_no'(委托编号), 'error_info'(错误信息), 'order_time'(委托时间), 'stock_code'(股票代码), 'amount'(委托数量), 'price'(委托价格), 'business_amount'(成交数量), 'status'(委托状态), 'entrust_type'(委托类别), 'entrust_prop'(委托属性), 'order_id'(Order对象编号)；

返回
None

接收到的主推格式如下:
本交易委托产生的主推：[{'price': 32.82, 'status': '2', 'amount': 1100, 'order_id': '0e27467920464390aa10a7a53da4d49a', 'stock_code': '600570.SS', 'order_time': '2022-09-21 14:38:35', 'business_amount': 0.0, 'entrust_type': '0', 'entrust_no': '700104', 'error_info': '', 'entrust_prop': '0'}]
本交易撤单产生的主推：[{'price': 32.82, 'status': '2', 'amount': 1100, 'order_id': '0e27467920464390aa10a7a53da4d49a', 'stock_code': '600570.SS', 'order_time': '2022-09-21 14:38:37', 'business_amount': 0.0, 'entrust_type': '2', 'entrust_no': '700105', 'error_info': '', 'entrust_prop': '0'}]
非本交易委托产生的主推：[{'price': 32.82, 'status': '2', 'amount': 1100, 'order_id': '', 'stock_code': '600570.SS', 'order_time': '2022-09-21 14:41:19', 'business_amount': 0.0, 'entrust_type': '0', 'entrust_no': '700106', 'error_info': '', 'entrust_prop': '0'}]
非本交易撤单产生的主推：[{'price': 32.82, 'status': '2', 'amount': 1100, 'order_id': '', 'stock_code': '600570.SS', 'order_time': '2022-09-21 14:41:30', 'business_amount': 0.0, 'entrust_type': '2', 'entrust_no': '700107', 'error_info': '', 'entrust_prop': '0'}]
示例
def initialize(context):
    g.security = ['600570.SS','002416.SZ']
    set_universe(g.security)
    g.flag = 0

def on_order_response(context, order_list):
    log.info(order_list)
    if(g.flag==0):
        order('600570.SS', 100)
        g.flag = 1
    else:
        log.info("end")

def handle_data(context, data):
    order('600570.SS', 100)
on_trade_response(可选)-成交主推
on_trade_response(context, trade_list)
使用场景
该函数仅在交易模块可用

接口说明
该函数会在成交主推回调时响应，比引擎和get_trades()函数更新Order状态的速度更快，适合对速度要求比较高的策略。

注意事项：

目前可接收股票、可转债、ETF、LOF、期货代码的主推数据。
当接到策略外交易产生的主推时(需券商配置默认不推送)，由于没有对应的Order对象，主推信息中order_id字段赋值为""。
当主推先于委托应答返回时，由于无法根据entrust_no匹配对应的Order对象，主推信息中order_id字段赋值为""。
当在主推里调用委托接口时，需要进行判断处理避免无限迭代循环问题。
当券商配置接收策略外交易产生的主推且策略调用set_parameters()并设置receive_other_response="1"时， 策略中将接收非本交易产生的主推。
当策略调用set_parameters()并设置receive_cancel_response="1"， 策略接收到撤单成交主推时，主推信息中的order_id为买入或卖出委托Order对象的order_id，entrust_no为撤单委托的委托编号。
撤单成交主推信息中成交数量均处理为正数。
withdraw_no(撤单原委托号)仅在撤单成交主推信息中才有对应值，在委托成交主推中该字段赋'0'默认值。
撤单成交主推信息中entrust_no在异构柜台情况下与withdraw_no一致，因此策略中请勿将该字段作为撤单成交主推信息的关联字段。
可调用委托接口
set_parameters(回测/交易)	get_history(研究/回测/交易)	get_price(研究/回测/交易)	get_individual_entrust(交易)	get_individual_transaction(交易)
get_tick_direction(交易)	get_sort_msg(交易)	get_underlying_code(交易)	get_etf_info(交易)	get_etf_stock_info(交易)
get_gear_price(交易)	get_snapshot(交易)	get_cb_info(研究/交易)	get_trend_data(研究/回测/交易)	get_stock_name(研究/回测/交易)
get_stock_info(研究/回测/交易)	get_stock_status(研究/回测/交易)	get_stock_exrights(研究/回测/交易)	get_stock_blocks(研究/回测/交易)	get_index_stocks(研究/回测/交易)
get_etf_stock_list(交易)	get_industry_stocks(研究/回测/交易)	get_fundamentals(研究/回测/交易)	get_Ashares(研究/回测/交易)	get_etf_list(交易)
get_ipo_stocks(交易)	get_cb_list(交易)	get_reits_list(研究/回测/交易)	get_position(回测/交易)	get_positions(回测/交易)
get_all_positions(交易)	order(回测/交易)	order_target(回测/交易)	order_value(回测/交易)	order_target_value(回测/交易)
order_market(交易)	ipo_stocks_order(交易)	after_trading_order(交易)	after_trading_cancel_order(交易)	etf_basket_order(交易)
etf_purchase_redemption(交易)	cancel_order(回测/交易)	cancel_order_ex(交易)	debt_to_stock_order(交易)	get_open_orders(回测/交易)
get_order(回测/交易)	get_orders(回测/交易)	get_all_orders(交易)	get_trades(回测/交易)	margin_trade(回测/交易)
margincash_open(交易)	margincash_close(交易)	margincash_direct_refund(交易)	marginsec_open(交易)	marginsec_close(交易)
marginsec_direct_refund(交易)	get_margin_contract(交易)	get_margin_contractreal(交易)	get_margin_asset(交易)	get_assure_security_list(交易)
get_margincash_open_amount(交易)	get_margincash_close_amount(交易)	get_marginsec_open_amount(交易)	get_marginsec_close_amount(交易)	get_margin_entrans_amount(交易)
get_enslo_security_info(交易)	buy_open(回测/交易(期货))	sell_close(回测/交易(期货))	sell_open(回测/交易(期货))	buy_close(回测/交易(期货))
get_MACD(回测/交易)	get_KDJ(回测/交易)	get_RSI(回测/交易)	get_CCI(回测/交易)
log(回测/交易)	check_limit(回测/交易)	send_email(交易)	send_qywx(交易)	create_dir(研究/回测/交易)
get_dominant_contract(研究/回测/交易(期货))	get_crdt_fund(交易)	fund_transfer(交易)	market_fund_transfer(交易)
参数
context: Context对象，存放有当前的账户及持仓信息；

trade_list：一个列表，当前成交单发生变化时，发生变化的成交单列表。成交单以字典形式展现，内容包括：'entrust_no'(委托编号)，'business_time'(成交时间)，'stock_code'(股票代码)，'entrust_bs'(委托方向)，'business_amount'(成交数量)，'business_price'(成交价格)，'business_balance'(成交额)，'business_id'(成交编号)，'status',(委托状态)(对接jz_ufx、ctp期货柜台该字段为空)，'order_id'(Order对象编号)，'cancel_info'(废单原因)，'withdraw_no'(撤单原委托号)，'real_type' (成交类型编号)，'real_status'(成交状态编号)；

返回
None

接收到的主推格式如下:
本交易委托产生的主推：[{'order_id': '0e27467920464390aa10a7a53da4d49a', 'entrust_bs': '1', 'status': '7', 'business_id': '58', 'withdraw_no': '0', 'business_time': '2022-09-21 14:38:11', 'stock_code': '600570.SS', 'business_balance': 32820.0, 'business_price': 32.82, 'business_amount': 1000, 'entrust_no': '700104', 'cancel_info': ' ', 'real_type': '0', 'real_status': '0'}]
本交易撤单产生的主推：[{'order_id': '0e27467920464390aa10a7a53da4d49a', 'entrust_bs': '1', 'status': '5', 'business_id': '0', 'withdraw_no': '700104', 'business_time': '2022-09-21 14:38:13', 'stock_code': '600570.SS', 'business_balance': -3282.0, 'business_price': 32.82, 'business_amount': 100, 'entrust_no': '700105', 'cancel_info': ' ', 'real_type': '2', 'real_status': '0'}]
非本交易委托产生的主推：[{'order_id': '', 'entrust_bs': '1', 'status': '7', 'business_id': '59', 'withdraw_no': '0', 'business_time': '2022-09-21 14:40:56', 'stock_code': '600570.SS', 'business_balance': 32820.0, 'business_price': 32.82, 'business_amount': 1000, 'entrust_no': '700106', 'cancel_info': ' ', 'real_type': '0', 'real_status': '0'}]
非本交易撤单产生的主推：[{'order_id': '', 'entrust_bs': '1', 'status': '7', 'business_id': '0', 'withdraw_no': '700106', 'business_time': '2022-09-21 14:41:06', 'stock_code': '600570.SS', 'business_balance': 0.0, 'business_price': 32.82, 'business_amount': 0, 'entrust_no': '700107', 'cancel_info': '交易主机繁忙', 'real_type': '2', 'real_status': '0'}]
示例
def initialize(context):
    g.security = ['600570.SS','002416.SZ']
    set_universe(g.security)
    g.flag = 0

def on_trade_response(context, trade_list):
    log.info(trade_list)
    if(g.flag==0):
        order('600570.SS', 100)
        g.flag = 1
    else:
        log.info("end")

def handle_data(context, data):
    order('600570.SS', 100)
策略API介绍
设置函数
set_universe-设置股票池
set_universe(security_list)
使用场景
该函数仅在回测、交易模块可用

接口说明
该函数用于设置或者更新此策略要操作的股票池。

注意事项：

股票策略中，该函数只用于设定get_history函数的默认security_list入参，除此之外并无其他用处，因此为非必须设定的函数。
参数
security_list: 股票列表，支持单支或者多支股票(list[str]/str)

返回
None

示例
def initialize(context):
    g.security = ['600570.SS','600571.SS']
    # 将g.security中的股票设置为股票池
    set_universe(g.security)

def handle_data(context, data):
    # 获取初始化设定的股票池行情数据
    his = get_history(5, '1d', 'close', security_list=None)
set_benchmark-设置基准
set_benchmark(sids)
使用场景
该函数仅在回测、交易模块可用

接口说明
该函数用于设置策略的比较基准，前端展现的策略评价指标都基于此处设置的基准标的。

注意事项：

此函数只能在initialize使用。
回测时若用该函数设置了某个基准指数，那么该基准指数会替代终端页面开启回测时所设定的基准。
参数
sids：股票/指数/ETF代码(str)

默认设置
如果不做基准设置，默认选定沪深300指数(000300.SS)的每日价格作为判断策略好坏和一系列风险值计算的基准。如果要指定其他股票/指数/ETF的价格作为基准，就需要使用set_benchmark。

返回
None

示例
def initialize(context):
    g.security = '000001.SZ'
    set_universe(g.security)
    #将上证50(000016.SS)设置为参考基准
    set_benchmark('000016.SS')

def handle_data(context, data):
    order('000001.SZ',100)
set_commission-设置佣金费率
set_commission(commission_ratio=0.0003, min_commission=5.0, type="STOCK")
使用场景
该函数仅在回测模块可用

接口说明
该函数用于设置佣金费率。

注意事项：

关于回测手续费计算：手续费=佣金费+经手费+印花税。
佣金费=佣金费率*交易总金额(若佣金费计算后小于设置的最低佣金，则佣金费取最小佣金)。
经手费=经手费率(万分之0.487)*交易总金额。
印花税=印花税率(千分之1)*交易总金额，仅卖出时收。
参数
commission_ratio：佣金费率，默认股票每笔交易的佣金费率是万分之三，ETF基金、LOF基金每笔交易的佣金费率是万分之八。(float)

min_commission：最低交易佣金，默认每笔交易最低扣5元佣金。(float)

type：交易类型，不传参默认为STOCK(目前只支持STOCK, ETF, LOF)。(string)

返回
None

示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)
    #将佣金费率设置为万分之三，将最低手续费设置为3元
    set_commission(commission_ratio =0.0003, min_commission=3.0)

def handle_data(context, data):
    pass
set_fixed_slippage-设置固定滑点
set_fixed_slippage(fixedslippage=0.0)
使用场景
该函数仅在回测模块可用

接口说明
该函数用于设置固定滑点，滑点在真实交易场景是不可避免的，因此回测中设置合理的滑点有利于让回测逼近真实场景。

注意事项：

滑点如果不足交易品种的最小价差，将不会生效。举例：沪深300期指IF的最小差价是0.2，如果固定滑点设置为0.3，单边为0.15，不足0.2，滑点设置无效。
参数
fixedslippage：固定滑点，委托价格与最后的成交价格的价差设置，这个价差是一个固定的值(比如0.02元，撮合成交时委托价格±0.01元)。最终的成交价格=委托价格±float(fixedslippage)/2。

返回
None

示例
def initialize(context):
    g.security = "600570.SS"
    set_universe(g.security)
    # 将滑点设置为固定的0.2元，即原本买入交易的成交价为10元，则设置之后成交价将变成10.1元
    set_fixed_slippage(fixedslippage=0.2)

def handle_data(context, data):
    pass
set_slippage-设置滑点
set_slippage(slippage=0.001)
使用场景
该函数仅在回测模块可用

接口说明
该函数用于设置滑点比例，滑点在真实交易场景是不可避免的，因此回测中设置合理的滑点有利于让回测逼近真实场景。

注意事项：

无

参数
slippage：滑点比例，委托价格与最后的成交价格的价差设置，这个价差是当时价格的一个百分比(比如设置0.002时，撮合成交时委托价格±当前周期价格*0.001)。最终成交价格=委托价格±委托价格*float(slippage)/2。

返回
None

示例
def initialize(context):
    g.security = "600570.SS"
    set_universe(g.security)
    # 将滑点设置为0.002
    set_slippage(slippage=0.002)

def handle_data(context, data):
    pass
set_volume_ratio-设置成交比例
set_volume_ratio(volume_ratio=0.25)
使用场景
该函数仅在回测模块可用

接口说明
该函数用于设置回测中单笔委托的成交比例，使得盘口流动性方面的设置尽量逼近真实交易场景。

注意事项：

假如委托下单数量大于成交比例计算后的数量，系统会按成交比例计算后的数量撮合，差额部分委托数量不会继续挂单。
参数
volume_ratio：设置成交比例，默认0.25，即指本周期最大成交数量为本周期市场可成交总量的四分之一(float)

返回
None

示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)
    #将最大成交数量设置为本周期可成交总量的二分之一
    set_volume_ratio(volume_ratio = 0.5)

def handle_data(context, data):
    pass
set_limit_mode-设置成交数量限制模式
set_limit_mode(limit_mode='LIMIT')
使用场景
该函数仅在回测模块可用

接口说明
该函数用于设置回测的成交数量限制模式。对于月度调仓等低频策略，对流动性冲击不是很敏感，不做成交量限制可以让回测更加便捷。

注意事项：

不做限制之后实际撮合成交量是可以大于该时间段的实际成交总量。
参数
limit_mode：设置成交数量限制模式，即指回测撮合交易时对成交数量是否做限制进行控制(str)

默认为限制，入参'LIMIT'，不做限制则入参'UNLIMITED'

返回
None

示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)
    #回测中不限制成交数量
    set_limit_mode('UNLIMITED')

def handle_data(context, data):
    pass
set_yesterday_position - 设置底仓
set_yesterday_position(poslist)
使用场景
该函数仅在回测模块可用

接口说明
该函数用于设置回测的初始底仓。

注意事项：

该函数会使策略初始化运行就创建出持仓对象，里面包含了设置的持仓信息。
该函数仅支持在股票、两融回测中设置底仓。
参数
poslist：list类型数据，该list中是字典类型的元素，参数不能为空(list[dict[str:str],...])；

数据格式及参数字段如下：

[{
    'sid':标的代码,
    'amount':持仓数量,
    'enable_amount':可用数量,
    'cost_basis':每股的持仓成本价格,
}]
参数也可通过csv文件的形式传入，参考接口convert_position_from_csv

返回
None

示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)
    # 设置底仓
    pos={}
    pos['sid'] = "600570.SS"
    pos['amount'] = "1000"
    pos['enable_amount'] = "600"
    pos['cost_basis'] = "55"
    set_yesterday_position([pos])

def handle_data(context, data):
    #卖出100股
    order(g.security, -100)
set_parameters - 设置策略配置参数
set_parameters(**kwargs)
使用场景
该函数仅在交易模块可用

接口说明
该函数用于设置策略中的配置参数。

注意事项：

该函数入参格式必须为a=b样式。
not_restart_trade、server_restart_not_do_before两个入参必须在initialize模块中设置。
not_restart_trade入参配置说明(交易场景务必了解)：
服务器环境重启拉起交易时，initialize和before_trading_start函数会被重复调用，请务必检查策略编写逻辑：
避免在这两个函数中设置无法被系统持久化保存的变量，变量一旦被初始化会导致策略逻辑异常。
避免在这两个函数中调用委托接口，造成重复委托。
您可将not_restart_trade入参设置为1，在交易时间段避免重复执行的问题，交易时间段默认为09:00-11:30、13:00-15:30，实际以券商的配置为准。
server_restart_not_do_before入参配置说明(交易场景务必了解)：
服务器环境重启拉起交易时，before_trading_start函数默认会被调用，为了避免重复调用带来的一系列问题(同上)，您可将server_restart_not_do_before入参设置为"1"，即一个交易日内before_trading_start函数仅调用一次。
如果想要取消已经设置的配置参数，需要再次调用该接口并传入xxx(具体配置项)="0"。
支持的参数
holiday_not_do_before：交易中节假日是否执行before_trading_start。0，执行(缺省)；1，不执行。

tick_data_no_l2：tick_data中data是否包含order和transaction。0，包含(缺省)；1，不包含。

receive_other_response：策略中是否接收非本交易产生的主推。0，不接收(缺省)；1，接收。

receive_cancel_response：策略中是否接收撤单委托产生的主推。0，不接收(缺省)；1，接收。

individual_data_in_dict：策略中调用get_individual_entrust/transaction返回的数据类型。0，Panel(缺省)；1，dict。

tick_direction_in_dict：策略中调用get_tick_direction返回的数据类型。0，OrderedDict(缺省)；1，dict。

not_restart_trade：交易时间段若服务器重启，是否自动执行重新拉起本交易。0，执行(缺省)；1，不执行。

server_restart_not_do_before：若服务器重启导致重拉交易，是否重复执行before_trading_start函数。0，执行(缺省)；1，不执行。

返回
None

示例
def initialize(context):
    # 初始化策略
    g.security = "600570.SS"
    set_universe(g.security)
    # 设置非交易日不执行before_trading_start
    # 设置tick_data中data不包含order和transaction
    # 设置接收非本交易产生的主推
    # 设置接收撤单委托产生的主推
    # 设置交易时间段服务器重启不再拉起本交易
    # 设置服务器重启重拉交易时不再执行before_trading_start函数
    set_parameters(holiday_not_do_before="1", tick_data_no_l2="1", receive_other_response="1",
                   receive_cancel_response="1", not_restart_trade="1", server_restart_not_do_before="1")
    # 取消交易时间段服务器重启不再拉起本交易设置
    # 取消服务器重启重拉交易时不再执行before_trading_start函数设置
    set_parameters(not_restart_trade="0", server_restart_not_do_before="0")

def before_trading_start(context, data):
    log.info("do before_trading_start")
    # 取消非交易日不执行before_trading_start设置
    # 取消tick_data中data不包含order和transaction设置
    # 取消接收非本交易产生的主推设置
    # 取消接收撤单委托产生的主推设置
    set_parameters(holiday_not_do_before="0", tick_data_no_l2="0", receive_other_response="0",
                   receive_cancel_response="0")

def on_order_response(context, order_list):
    log.info("委托主推：%s" % order_list)

def on_trade_response(context, trade_list):
    log.info("成交主推：%s" % trade_list)

def handle_data(context, data):
    pass
set_email_info-设置邮件信息
set_email_info(email_address, smtp_code, email_subject)
使用场景
该函数仅在交易模块可用

接口说明
该函数用于设置邮件信息，当交易报错终止时会发送提示邮件。

注意事项：

如要使用该函数，需咨询券商当前环境是否支持发送邮件。
当前仅支持设置QQ邮箱地址。
参数
email_address(str)：邮箱地址(发送方与接收方一致)。

smtp_code(str)：邮箱SMTP授权码。

email_subject(str)：邮件主题。

返回
返回设置是否成功True/False(bool)。

示例
def initialize(context):
    g.security = "600570.SS"
    set_universe(g.security)
    # 设置邮件信息
    set_email_info("2222@qq.com", "AABB", "【PTrade量化-策略交易异常终止提醒】")

def before_trading_start(context, data):
    raise BaseException("test send error email")

def handle_data(context, data):
    pass
定时周期性函数
run_daily-按日周期处理
run_daily(context, func, time='9:31')
使用场景
该函数仅在回测、交易模块可用

接口说明
该函数用于以日为单位周期性运行指定函数，可对运行触发时间进行指定。

注意事项：

该函数只能在初始化阶段initialize函数中调用。
该函数可以在initialize中多次调用，以实现多个定时任务。 但需要注意的是交易中定时任务线程数限制为5且累计的任务不执行，即run_daily和run_interval累计调用超过5次时， 将会因堵塞导致部分定时任务不触发。
股票策略回测中，当回测周期为分钟时，time的取值指定在09:31~11:30与13:00~15:00之间，当回测周期为日时， 无论设定值是多少都只会在15:00执行；交易中不受此时间限制。
参数
context: Context对象，存放有当前的账户及持仓信息(Context)；

func：自定义函数名称，此函数必须以context作为参数(Callable[[Context], None])；

time：指定周期运行具体触发运行时间点，默认为9:31分(str)，交易场景可设置范围：00:00~23:59。

返回
None

示例
# 定义一个财务数据获取函数，每天执行一次
def initialize(context):
    run_daily(context, get_finance)
    g.security = '600570.SS'
    set_universe(g.security)

def get_finance(context):
    re = get_fundamentals(g.security,'balance_statement','total_assets')
    log.info(re)

def handle_data(context, data):
    pass
run_interval - 按设定周期处理
run_interval(context, func, seconds=10, interval_timer_ranges="")
使用场景
该函数仅在交易模块可用

接口说明
该函数用于以设定时间间隔(单位为秒)周期性运行指定函数，可对运行触发时间间隔进行指定。

注意事项：

该函数只能在初始化阶段initialize函数中调用。
可通过 interval_timer_ranges 参数设置运行的时间段。
该函数可以在initialize中多次调用，以实现多个定时任务。但需要注意的是交易中定时任务线程数限制为5且累计的任务不执行，即run_daily和run_interval累计调用超过5次时， 将会因堵塞导致部分定时任务不触发。
最小运行时间间隔seconds的设置规则：期货策略为1秒（用户设置值若小于1秒，系统仍当做1秒处理），股票等其他类型策略为3秒。
参数
context: Context对象，存放有当前的账户及持仓信息(Context)；

func：自定义函数名称，此函数必须以context作为参数(Callable[[Context], None])；

seconds：设定时间间隔(单位为秒)，取值为正整数(int)。

interval_timer_ranges：用于设置指定函数运行的时间范围(str)。

每个时间段使用 HH:MM-HH:MM 格式，多个时间段之间用英文逗号分隔。例如："09:15-11:30,13:00-15:00"表示从上午9点15分到11点半和下午1点到3点的时间范围。
当前时间大于等于时间段范围的开始时间、小于时间段范围的结束时间时触发 run_interval 内设置的函数。
时间是以24小时制表示的，确保统一格式。
如果未定义此参数，系统将默认使用券商配置时间范围进行处理。
如果时间段在数据更新范围外，可能会导致获取到未更新的历史数据，建议设置当前业务可交易的时间范围。
返回
None

示例
# 定义一个周期处理函数，每10秒执行一次
def initialize(context):
    # 设置 interval_handle 函数在9:15~11:30与13:00~15:00时间段内执行
    run_interval(context, interval_handle, seconds=10, interval_timer_ranges="09:15-11:30,13:00-15:00")
    g.security = "600570.SS"
    set_universe(g.security)

def interval_handle(context):
    snapshot = get_snapshot(g.security)
    log.info(snapshot)

def handle_data(context, data):
    pass
获取信息函数
获取基础信息
get_trading_day - 获取交易日期
get_trading_day(day)
使用场景
该函数在研究、回测、交易模块可用

接口说明
该函数用于获取当前时间数天前或数天后的交易日期。

注意事项：

默认情况下，回测中当前时间为策略中调用该接口的回测日日期(context.blotter.current_dt)。
默认情况下，研究中当前时间为调用当天日期。
默认情况下，交易中当前时间为调用当天日期。
参数
day：表示天数，正的为数天后，负的为数天前，day取0表示获取当前交易日，如果当前日期为非交易日则返回上一交易日的日期。day默认取值为0，不建议获取交易所还未公布的交易日期(int)；

返回
date：datetime.date日期对象

示例
def initialize(context):
    g.security = ['600670.SS', '000001.SZ']
    set_universe(g.security)

def handle_data(context, data):
    # 获取后一天的交易日期
    next_trading_date = get_trading_day(1)
    log.info(next_trading_date)
    # 获取前一天的交易日期
    previous_trading_date = get_trading_day(-1)
    log.info(previous_trading_date)
get_all_trades_days - 获取全部交易日期
get_all_trades_days(date=None)
使用场景
该函数在研究、回测、交易模块可用

接口说明
该函数用于获取某个日期之前的所有交易日日期。

注意事项：

默认情况下，回测中date为策略中调用该接口的回测日日期(context.blotter.current_dt)。
默认情况下，研究中date为调用当天日期。
默认情况下，交易中date为调用当天日期。
该接口返回的最早的交易日日期为："2005-01-04"。
参数
date：如'2016-02-13'或'20160213'

返回
一个包含所有交易日的numpy.ndarray

示例
def initialize(context):
    # 获取当前回测日期之前的所有交易日
    all_trades_days = get_all_trades_days()
    log.info(all_trades_days)
    all_trades_days_date = get_all_trades_days('20150312')
    log.info(all_trades_days_date)
    g.security = ['600570.SS', '000001.SZ']
    set_universe(g.security)

def handle_data(context, data):
    pass
get_trade_days - 获取指定范围交易日期
get_trade_days(start_date=None, end_date=None, count=None)
使用场景
该函数在研究、回测、交易模块可用

接口说明
该函数用于获取指定范围交易日期。

注意事项：

默认情况下，回测中end_date为策略中调用该接口的回测日日期(context.blotter.current_dt)。
默认情况下，研究中end_date为调用当天日期。
默认情况下，交易中end_date为调用当天日期。
参数
start_date：开始日期，与count二选一，不可同时使用。如'2016-02-13'或'20160213',开始日期最早不超过1990年(str)；

end_date：结束日期，如'2016-02-13'或'20160213'。如果输入的结束日期大于今年则至多返回截止到今年的数据(str)；

count：数量，与start_date二选一，不可同时使用，必须大于0。表示获取end_date往前的count个交易日，包含end_date当天。count建议不大于3000，即返回数据的开始日期不早于1990年(int)；

返回
一个包含指定范围交易日的numpy.ndarray

示例
def initialize(context):
    # 获取指定范围内交易日
    trade_days = get_trade_days('2016-01-01', '2016-02-01')
    log.info(trade_days)
    g.security = ['600570.SS', '000001.SZ']
    set_universe(g.security)

def handle_data(context, data):
    # 获取回测日期往前10天的所有交易日，包含历史回测日期
    trading_days = get_trade_days(count=10)
    log.info(trading_days)
get_trading_day_by_date - 按日期获取指定交易日
get_trading_day_by_date(query_date, day=0)
使用场景
该函数在研究、回测、交易模块可用

接口说明
该函数用于根据输入日期获取指定的交易日。

注意事项：

query_date为必传入参。
该函数主要使用场景：按固定自然日调仓。
参数
query_date：查询日期,如"20230213"(str)；

day：表示天数，正的为数天后，负的为数天前，day取0表示获取当前交易日，如果当前日期为非交易日则返回下一交易日的日期。day默认取值为0(int)；

返回
date：交易日日期(str)

示例
def initialize(context):
    g.security = ['600570.SS', '000001.SZ']
    set_universe(g.security)

def handle_data(context, data):
    current_date = context.blotter.current_dt.strftime('%Y-%m-%d')
    trading_date = get_trading_day_by_date("20230501", 0)
    if trading_date == current_date:
        log.info("今日是5月1日之后首个交易日")
获取市场信息
get_market_list-获取市场列表
get_market_list()
使用场景
该函数在研究、回测、交易模块可用

接口说明
该函数用于返回当前市场列表目录。

注意事项：

回测和交易中仅限before_trading_start和after_trading_end中使用。
参数
无

返回
返回pandas.DataFrame对象，返回字段包括:


finance_mic - 市场编码(str:str)

finance_name - 市场名称(str:str)

示例
get_market_list()
如返回：


finance_mic	finance_name
1	SS	上海证券交易所
2	SZ	深圳证券交易所
3	CSI	中证指数
4	XBHS	沪深板块
get_market_detail-获取市场详细信息
get_market_detail(finance_mic)
使用场景
该函数在研究、回测、交易模块可用

接口说明
该函数用于返回市场编码对应的详细信息。

注意事项：

回测和交易中仅限before_trading_start和after_trading_end中使用。
仅支持get_market_list接口所返回的四个市场数据。
参数
finance_mic: 市场代码，相关市场编码参考get_market_list返回信息(str)。

返回
返回市场详细信息，类型为pandas.DataFrame对象，返回字段包括：

产品代码: prod_code(str:str)

产品名称: prod_name(str:str)

类型代码: hq_type_code(str:str)

时间规则: trade_time_rule(str:numpy.int64)

返回如下:

      hq_type_code prod_code prod_name  trade_time_rule
0              MRI    000001      上证指数                0
1              MRI    000002      Ａ股指数                0
2              MRI    000003      Ｂ股指数                0
3              MRI    000004      工业指数                0
4              MRI    000005      商业指数                0
5              MRI    000006      地产指数                0
6              MRI    000007      公用指数                0
7              MRI    000008      综合指数                0
示例
# 获取上海证券交易所相关信息 'XSHG'/'SS'
get_market_detail('XSHG')
获取行情信息
get_history - 获取历史行情
get_history(count, frequency='1d', field='close', security_list=None, fq=None, include=False, fill='nan', is_dict=False)
使用场景
该函数仅在回测、交易、研究模块可用

接口说明
该接口用于获取最近N条历史行情K线数据。支持多股票、多行情字段获取。

注意事项：

该接口只能获取2005年后的数据。
针对停牌场景，我们没有跳过停牌的日期，无论对单只股票还是多只股票进行调用，时间轴均为二级市场交易日日历， 停牌时使用停牌前的数据填充，成交量为0，日K线可使用成交量为0的逻辑进行停牌日过滤。
证监会行业、聚源行业、概念板块、地域板块所对应标的的行情数据为非标准的交易所下发数据，是由数据源自行按照成分股分类规则进行计算的，存在与三方数据源不一致的情况。如用户需要在策略中使用，应自行评估该数据的合理性。
该接口与get_price接口不支持多线程同时调用，即在run_daily或run_interval等函数中不要与handle_data等框架模块同一时刻调用get_history或get_price接口，否则会偶现获取数据为空的现象

参数
count： K线数量，大于0，返回指定数量的K线行情；必填参数；入参类型：int；

frequency：K线周期，现有支持1分钟线(1m)、5分钟线(5m)、15分钟线(15m)、30分钟线(30m)、60分钟线(60m)、120分钟线(120m)、日线(1d)、周线(1w/weekly)、月线(mo/monthly)、季度线(1q/quarter)和年线(1y/yearly)频率的数据；选填参数，默认为'1d'；入参类型：str；


field：指明数据结果集中所支持输出的行情字段；选填参数，默认为['open','high','low','close','volume','money','price']；入参类型：list[str,str]或str；输出字段包括：

open -- 开盘价，字段返回类型：numpy.float64；
high -- 最高价，字段返回类型：numpy.float64；
low --最低价，字段返回类型：numpy.float64；
close -- 收盘价，字段返回类型：numpy.float64；
volume -- 交易量，字段返回类型：numpy.float64；
money -- 交易金额，字段返回类型：numpy.float64；
price -- 最新价，字段返回类型：numpy.float64；
is_open -- 是否开盘，字段返回类型：numpy.int64(仅日线返回)；
preclose -- 昨收盘价，字段返回类型：numpy.float64(仅日线返回)；
high_limit -- 涨停价，字段返回类型：numpy.float64(仅日线返回)；
low_limit -- 跌停价，字段返回类型：numpy.float64(仅日线返回)；
unlimited -- 判断查询日是否是无涨跌停限制(1:该日无涨跌停限制;0:该日不是无涨跌停限制)，字段返回类型：numpy.int64(仅日线返回)；
security_list：要获取数据的股票列表；选填参数，None表示在上下文中的universe中选中的所有股票；入参类型：list[str,str]或str；

fq：数据复权选项，支持包括，pre-前复权，post-后复权，dypre-动态前复权，None-不复权；选填参数，默认为None；入参类型：str；

include：是否包含当前周期，True -包含，False-不包含；选填参数，默认为False；入参类型：bool；

fill：行情获取不到某一时刻的分钟数据时，是否用上一分钟的数据进行填充该时刻数据，'pre'-用上一分钟数据填充，'nan'-NaN进行填充(仅交易有效)；选填参数，默认为'nan'；入参类型：str；

is_dict：返回是否是字典(dict)格式{str: array()}，True -是，False-不是；选填参数，默认为False；返回为字典格式取数速度相对较快；入参类型：bool；

返回
dict类型
正常返回dict类型数据，异常时返回None(NoneType)。

OrderedDict([(股票代码(str), array([日期时间(numpy.int64), 开盘价(numpy.float64), 最高价(numpy.float64), 最低价(numpy.float64), 收盘价(numpy.float64), 成交量(numpy.float64), 成交额(numpy.float64), 最新价(numpy.float64)]]))])

OrderedDict([('000001.SZ', array([(202309220931, 11.03, 11.08, 11.03, 11.07, 2289400.0, 25302018.0, 11.07),... ]))])

非dict类型
(python3.5、python3.11版本均支持)第一种返回数据：
当获取单支股票(单只股票必须为字符串类型security_list='600570.SS'，不能用security_list=['600570.SS'])的时候，无论行情字段field入参单个或多个，返回的都是pandas.DataFrame对象，行索引是datetime.datetime对象，列索引是行情字段,为str类型。比如：

如果当前时间是2017-04-18，get_history(5, '1d', 'open', '600570.SS', fq=None, include=False)将返回：

open
2017-04-11	40.30
2017-04-12	40.08
2017-04-13	40.03
2017-04-14	40.04
2017-04-17	39.90
(仅python3.11版本支持)第二种返回数据：
当获取多支股票(多只股票必须为list类型，特殊情况：当list只有一个股票时仍然当做多股票处理，比如security_list=['600570.SS'])的时候，无论行情字段field入参是单个还是多个，返回的是pandas.DataFrame对象，行索引是datetime.datetime对象，列索引是股票代码code和取的字段,为str类型。比如：

如果当前时间是2017-04-18，get_history(5, '1d', 'open', ['600570.SS','600571.SS'], fq=None, include=False)将返回：

code	open
2017-04-11	600570.SS	40.30
2017-04-12	600570.SS	40.08
2017-04-13	600570.SS	40.03
2017-04-14	600570.SS	40.04
2017-04-17	600570.SS	39.90
2017-04-11	600571.SS	17.81
2017-04-12	600571.SS	17.56
2017-04-13	600571.SS	17.42
2017-04-14	600571.SS	17.40
2017-04-17	600571.SS	17.49
假如要对获取查询多只代码种某单只代码或多只代码的数据，可以通过x.query('code in ["xxxxxx.SS"]')的方法获取。

比如:

dataframe_info = get_history(2, frequency='1d', field=['open','close'], security_list=['600570.SS', '600571.SS'], fq=None, include=False)

则获取600570.SS的数据为：df = dataframe_info.query('code in ["600570.SS"]')

(仅python3.5版本支持)第三种返回数据：
当获取多支股票(多只股票必须为list类型，特殊情况：当list只有一个股票时仍然当做多股票处理，比如security_list=['600570.SS'])的时候，如果行情字段field入参为单个，返回的是pandas.DataFrame对象，行索引是datetime.datetime对象，列索引是股票代码的编号,为str类型。比如：

如果当前时间是2017-04-18，get_history(5, '1d', 'open', ['600570.SS','600571.SS'], fq=None, include=False)将返回：

600570.SS	600571.SS
2017-04-11	40.30	17.81
2017-04-12	40.08	17.56
2017-04-13	40.03	17.42
2017-04-14	40.04	17.40
2017-04-17	39.90	17.49
(仅python3.5版本支持)第四种返回数据：
当获取多支股票(多只股票必须为list类型，特殊情况：当list只有一个股票时仍然当做多股票处理，比如security_list=['600570.SS'])的时候，如果行情字段field入参为多个，则返回pandas.Panel对象，items索引是行情字段(如'open'、'close'等)，里面是很多pandas.DataFrame对象，每个pandas.DataFrame的行索引是datetime.datetime对象， 列索引是股票代码,为str类型，比如:

如果当前时间是2015-01-07，get_history(2, frequency='1d', field=['open','close'], security_list=['600570.SS', '600571.SS'], fq=None, include=False)['open']将返回:

600570.SS	600571.SS
2015-01-05	54.77	26.93
2015-01-06	51.00	25.83
假如要对panel索引中的对象进行转换，比如将items索引由行情字段转换成股票代码，可以通过panel_info = panel_info.swapaxes("minor_axis", "items")的方法转换。

比如:

panel_info = get_history(2, frequency='1d', field=['open','close'], security_list=['600570.SS', '600571.SS'], fq=None, include=False)

按默认索引：df = panel_info['open']

对默认索引做转换：panel_info = panel_info.swapaxes("minor_axis", "items")

转换之后的索引：df = panel_info['600570.SS']

示例
def initialize(context):
    g.security = ['600570.SS', '000001.SZ']
    set_universe(g.security)

def before_trading_start(context, data):
    # 获取农业版块过去10天的每日收盘价
    industry_info = get_history(10, frequency="1d", field="close", security_list="A01000.XBHS")
    log.info(industry_info)

def handle_data(context, data):
    # 股票池中全部股票过去5天的每日收盘价
    his = get_history(5, '1d', 'close', security_list=g.security)
    log.info('股票池中全部股票过去5天的每日收盘价')
    log.info(his)

    # 获取600570(恒生电子)过去5天的每天收盘价,
    # 一个pd.Series对象, index是datatime
    log.info('获取600570(恒生电子)过去5天的每天收盘价')
    his_ss = his.query('code in ["600570.SS"]')['close']
    log.info(his_ss)

    # 获取600570(恒生电子)昨天(数组最后一项)的收盘价
    log.info('获取600570(恒生电子)昨天的收盘价')
    log.info(his_ss[-1])

    # 获取每一列的平均值
    log.info('获取600570(恒生电子)每一列的平均值')
    log.info(his_ss.mean())

    # 获取股票池中全部股票的过去10分钟的成交量
    his1 = get_history(10, '1m', 'volume')
    log.info('获取股票池中全部股票的过去10分钟的成交量')
    log.info(his1)

    # 获取恒生电子的过去5天的每天的收盘价
    his2 = get_history(5, '1d', 'close', security_list='600570.SS')
    log.info('获取恒生电子的过去5天的每天的收盘价')
    log.info(his2)

    # 获取恒生电子的过去5天的每天的后复权收盘价
    his3 = get_history(5, '1d', 'close', security_list='600570.SS', fq='post')
    log.info('获取恒生电子的过去5天的每天的后复权收盘价')
    log.info(his3)

    # 获取恒生电子的过去5周的每周的收盘价
    his4 = get_history(5, '1w', 'close', security_list='600570.SS')
    log.info('获取恒生电子的过去5周的每周的收盘价')
    log.info(his4)

    # 获取多只股票的开盘价和收盘价数据
    dataframe_info = get_history(2, frequency='1d', field=['open','close'], security_list=g.security)
    open_df = dataframe_info[['code', 'open']]
    log.info('获所有股票的取开盘价数据')
    log.info(open_df)
    df = open_df.query('code in ["600570.SS"]')['open']
    log.info('仅获取恒生电子的开盘价数据')
    log.info(df)
get_price - 获取历史数据
get_price(security, start_date=None, end_date=None, frequency='1d', fields=None, fq=None, count=None, is_dict=False)
使用场景
该函数在研究、回测、交易模块可用

接口说明
该接口用于获取指定日期前N条的历史行情K线数据或者指定时间段内的历史行情K线数据。支持多股票、多行情字段获取。

注意事项：

start_date与count必须且只能选择输入一个，不能同时输入或者同时都不输入。
针对停牌场景，我们没有跳过停牌的日期，无论对单只股票还是多只股票进行调用，时间轴均为二级市场交易日日历， 停牌时使用停牌前的数据填充，成交量为0，日K线可使用成交量为0的逻辑进行停牌日过滤。
数据返回内容不包括当天数据。
count只针对'daily', 'weekly', 'monthly', 'quarter', 'yearly', '1d', '1m', '5m', '15m', '30m', '60m', '120m', '1w', 'mo', '1q', '1y'频率有效，并且输入日期的类型需与频率对应。
'weekly', '1w', 'monthly', 'mo', 'quarter', '1q', 'yearly', '1y'频率不支持start_date和end_date组合的入参， 只支持end_date和count组合的入参形式。
返回的周线数据是由日线数据进行合成。
该接口只能获取2005年后的数据。
证监会行业、聚源行业、概念板块、地域板块所对应标的的行情数据为非标准的交易所下发数据，是由数据源自行按照成分股分类规则进行计算的，存在与三方数据源不一致的情况。如用户需要在策略中使用，应自行评估该数据的合理性。
该接口与get_history接口不支持多线程同时调用，即在run_daily或run_interval等函数中不要与handle_data等框架模块同一时刻调用get_history或get_price接口，否则会偶现获取数据为空的现象。
参数
security：一支股票代码或者一个股票代码的list(list[str]/str)

start_date：开始时间，默认为空，回测中输入请小于回测日期，交易、研究中输入请小于当前日期，且均小于等于end_date。传入格式仅支持：YYYYmmdd、YYYY-mm-dd、YYYY-mm-dd HH:MM、YYYYmmddHHMM，如'20150601'、'2015-06-01'、'2015-06-01 10:00'、'201506011000'(str)；

end_date：结束时间，默认为空，回测中输入请小于回测日期，交易、研究中输入请小于当前日期。传入格式仅支持：YYYYmmdd、YYYY-mm-dd、YYYY-mm-dd HH:MM、YYYYmmddHHMM，如'20150601'、'2015-06-01'、'2015-06-01 14:00'、'201506011400'(str)；

frequency： 单位时间长度，现有支持1分钟线(1m)、5分钟线(5m)、15分钟线(15m)、30分钟线(30m)、60分钟线(60m)、120分钟线(120m)、日线(1d)、周线(1w/weekly)、月线(mo/monthly)、季度线(1q/quarter)和年线(1y/yearly)频率数据(str)；


fields：指明数据结果集中所支持输出字段(list[str]/str)，输出字段包括 ：

open -- 开盘价(numpy.float64)；
high -- 最高价(numpy.float64)；
low --最低价(numpy.float64)；
close -- 收盘价(numpy.float64)；
volume -- 交易量(numpy.float64)；
money -- 交易金额(numpy.float64)；
price -- 最新价(numpy.float64)；
is_open -- 是否开盘(numpy.int64)(仅日线返回)；
preclose -- 昨收盘价(numpy.float64)(仅日线返回)；
high_limit -- 涨停价(numpy.float64)(仅日线返回)；
low_limit -- 跌停价(numpy.float64)(仅日线返回)；
unlimited -- 判断查询日是否无涨跌停限制(1：该日无涨跌停限制；0：该日有涨跌停限制)(numpy.int64)(仅日线返回)；
fq：数据复权选项，支持包括，pre-前复权，post-后复权，dypre-动态前复权，None-不复权(str)；

count：大于0，不能与start_date同时输入，获取end_date前count根的数据，不支持除天('daily'/'1d')、分钟('1m')、5分钟线('5m')、15分钟线('15m')、30分钟线('30m')、60分钟线('60m')、120分钟线('120m')、周('weekly'/'1w')、('monthly'/'mo')、('quarter'/'1q')和('yearly'/'1y')以外的其它频率(int)；

is_dict：返回是否是字典(dict)格式{str: array()}，True -是，False-不是；选填参数，默认为False；返回为字典格式取数速度相对较快，入参类型：bool；

返回
dict类型
正常返回dict类型数据，异常时返回None(NoneType)。

OrderedDict([(股票代码(str), array([日期时间(numpy.int64), 开盘价(numpy.float64), 最高价(numpy.float64), 最低价(numpy.float64), 收盘价(numpy.float64), 成交量(numpy.float64), 成交额(numpy.float64), 最新价(numpy.float64)]]))])

OrderedDict([('600570.SS', array([(201706010931, 37.1, 37.14, 37.05, 37.09, 128200.0, 4756263.0, 37.09),...]))])

非dict类型
get_price对于多股票和多字段不同场景下获取返回数据的规则与get_history一致，如下：

(python3.5、python3.11版本均支持)第一种返回数据：

当获取单支股票(单只股票必须为字符串类型security='600570.SS'，不能用security=['600570.SS'])和单个或多个字段的时候，返回的是pandas.DataFrame对象，行索引是datetime.datetime对象，列索引是行情字段，为str类型。

例如，输入为get_price(security='600570.SS',start_date='20170201',end_date='20170213',frequency='1d')时，将返回：


                 open	high	 low    close	 volume	         money	       price is_open  preclose high_limit low_limit unlimited
2017-02-03	44.47	44.50	43.58	43.90	4418325.0	193895820.0	43.90	1	44.26	48.69	  39.83 	0
2017-02-06	43.91	44.30	43.66	44.10	4428487.0	194979290.0	44.10	1	43.90	48.29	  39.51 	0
2017-02-07	44.05	44.07	43.34	43.52	5649251.0	246776480.0	43.52	1	44.10	48.51	  39.69 	0
2017-02-08	43.59	44.78	43.53	44.59	12570233.0	557883600.0	44.59	1	43.52	47.87	  39.17 	0
2017-02-09	44.74	45.28	44.39	44.74	9240223.0	413875390.0	44.74	1	44.59	49.05	  40.13 	0
2017-02-10	44.80	44.98	44.41	44.62	8097465.0	361757300.0	44.62	1	44.74	49.21	  40.27 	0
2017-02-13	44.32	45.98	44.02	44.89	14931596.0	672360490.0	44.89	1	44.62	49.08	  40.16 	0
(仅python3.11版本支持)第二种返回数据：
当获取多支股票(多只股票必须为list类型，特殊情况：当list只有一个股票时仍然当做多股票处理，比如security=['600570.SS'])时候，返回的是pandas.DataFrame对象，行索引是datetime.datetime对象，列索引是股票代码code和取的字段，为str类型。

例如，输入为get_price(['600570.SS'], start_date='20170201', end_date='20170213', frequency='1d', fields='open')时，将返回：


              code     open
2017-02-03  600570.SS  44.47
2017-02-06  600570.SS  43.91
2017-02-07  600570.SS  44.05
2017-02-08  600570.SS  43.59
2017-02-09  600570.SS  44.74
2017-02-10  600570.SS  44.80
2017-02-13  600570.SS  44.32
例如，输入为get_price(['600570.SS','600571.SS'], start_date='20170201', end_date='20170213', frequency='1d', fields=['open','close'])[['code', 'open']]时，将返回：


               code    open
2017-02-03  600570.SS  44.47
2017-02-06  600570.SS  43.91
2017-02-07  600570.SS  44.05
2017-02-08  600570.SS  43.59
2017-02-09  600570.SS  44.74
2017-02-10  600570.SS  44.80
2017-02-13  600570.SS  44.32
2017-02-03  600571.SS  19.36
2017-02-06  600571.SS  19.00
2017-02-07  600571.SS  19.27
2017-02-08  600571.SS  19.10
2017-02-09  600571.SS  19.47
2017-02-10  600571.SS  19.57
2017-02-13  600571.SS  19.22
假如要对获取查询多只代码种某单只代码或多只代码的数据，可以通过x.query('code in ["xxxxxx.SS"]')的方法获取。

(仅python3.5版本支持)第三种返回数据：
当获取多支股票(多只股票必须为list类型，特殊情况：当list只有一个股票时仍然当做多股票处理，比如security=['600570.SS'])和单个字段的时候，返回的是pandas.DataFrame对象，行索引是datetime.datetime对象，列索引是股票代码的编号，为str类型。

例如，输入为get_price(['600570.SS'], start_date='20170201', end_date='20170213', frequency='1d', fields='open')时，将返回：


              600570.SS
2017-02-03      44.47
2017-02-06      43.91
2017-02-07      44.05
2017-02-08      43.59
2017-02-09      44.74
2017-02-10      44.80
2017-02-13      44.32
(仅python3.5版本支持)第四种返回数据：
如果是获取多支股票(多只股票必须为list类型，特殊情况：当list只有一个股票时仍然当做多股票处理，比如security=['600570.SS'])和多个字段，则返回pandas.Panel对象，items索引是行情字段，为str类型(如'open'、'close'等)，里面是很多pandas.DataFrame对象，每个pandas.DataFrame的行索引是datetime.datetime对象， 列索引是股票代码，为str类型。

例如，输入为get_price(['600570.SS','600571.SS'], start_date='20170201', end_date='20170213', frequency='1d', fields=['open','close'])['open']时，将返回：


             600570.SS   600571.SS
2017-02-03    44.47        19.36
2017-02-06    43.91        19.00
2017-02-07    44.05        19.27
2017-02-08    43.59        19.10
2017-02-09    44.74        19.47
2017-02-10    44.80        19.57
2017-02-13    44.32        19.22
假如要对panel索引中的对象进行转换，比如将items索引由行情字段转换成股票代码，可以通过panel_info = panel_info.swapaxes("minor_axis", "items")的方法转换。

示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def handle_data(context, data):
    # 获得600570.SS(恒生电子)的2015年01月的天数据，只获取open字段
    price_open = get_price('600570.SS', start_date='20150101', end_date='20150131', frequency='1d')['open']
    log.info(price_open)
    # 获取指定结束日期前count天到结束日期的所有开盘数据
    # price_open = get_price('600570.SS', end_date='20150131', frequency='daily', count=10)['open']
    # log.info(price_open)
    # 获取股票指定结束时间前count分钟到指定结束时间的所有数据
    # stock_info = get_price('600570.SS', end_date='2015-01-31 10:00', frequency='1m', count=10)
    # log.info(stock_info)
    # 获取指定结束日期前count周到结束日期所在周的所有开盘数据
    # week_open = get_price('600570.SS', end_date='20150131', frequency='1w', count=10)['open']
    # log.info(week_open)

    # 获取多只股票
    # 获取沪深300的2015年1月的天数据，返回一个[pandas.DataFrame]
    security_list = get_index_stocks('000300.XBHS', '20150101')
    price = get_price(security_list, start_date='20150101', end_date='20150131')
    log.info(price)
    # 获取某股票开盘价，行索引是[datetime.datetime]对象，列索引是行情字段

    price_open = price.query('code in [@security_list[0]]')['open']
    log.info(price_open)

    # 获取农业版块指定结束日期前count天到结束日期的数据
    industry_info = get_price("A01000.XBHS", end_date="20210315", frequency="daily", count=10)
    log.info(industry_info)
get_individual_entrust- 获取逐笔委托行情
get_individual_entrust(stocks=None, data_count=50, start_pos=0, search_direction=1, is_dict=False)
使用场景
该函数在交易模块可用

接口说明
该接口用于获取当日逐笔委托行情数据。

注意事项：

沪深市场都有逐笔委托数据。
逐笔委托，逐笔成交数据需开通level2行情才能获取到数据，否则无数据返回。
当策略入参is_dict为True时返回的数据类型为dict，返回dict类型数据的速度比(python3.11版本支持)DataFrame,(python3.5版本支持)Panel类型数据有大幅提升。
参数
stocks: 默认为当前股票池中代码列表(list[str])；

data_count: 数据条数，默认为50，最大为200(int)；

start_pos: 起始位置，默认为0(int)；

search_direction: 搜索方向(1向前，2向后)，默认为1(int)；

is_dict: 返回类型（False-(python3.11版本支持)DataFrame,(python3.5版本支持)Panel; True-dict），默认为False；

返回
dict类型
正常返回dict类型数据，异常时返回None(NoneType)。

返回的数据格式如下：

{股票代码(str): [[时间戳毫秒级(int), 价格(float), 委托数量(int), 委托编号(int), 委托方向(int)], ...], "fields": ["business_time", "hq_px", "business_amount", "order_no", "business_direction", "trans_kind"]}

{"600570.SS": [[20220913105747848, 36.16, 700, 5383145, 0, 4], ...], "fields": ["business_time", "hq_px", "business_amount", "order_no", "business_direction", "trans_kind"]}

非dict类型
默认返回(python3.11版本支持)DataFrame,(python3.5版本支持)Panel类型，入参is_dict为True时返回dict类型。

1.(仅python3.11版本支持)DataFrame类型类型，异常时返回None(NoneType)
输出字段如下所示：

code: 代码(str)；
business_time: 时间戳毫秒级(int)；
hq_px: 价格(float)；
business_amount: 委托数量(int)；
order_no: 委托编号(int)；
business_direction: 成交方向(int)；
trans_kind: 委托类型(int)；
2.(仅python3.5版本支持)正常返回Pandas.panel对象，异常时返回None(NoneType)
Items axis: 股票代码列表(str)；

Major_axis axis: 数据索引为自然数列(DataFrame)；

Minor_axis axis: 包含以下信息：

business_time: 时间戳毫秒级(str:numpy.int64)；
hq_px: 价格(str:numpy.int64)；
business_amount: 委托数量(str:numpy.int64)；
order_no: 委托编号(str:numpy.int64)；
business_direction: 成交方向(str:numpy.int64)；
trans_kind: 委托类型(str:numpy.int64)；
示例
def initialize(context):
    g.security = "000001.SZ"
    set_universe(g.security)

def before_trading_start(context, data):
    g.flag = False

def handle_data(context, data):
    if not g.flag:
        # 获取当前股票池逐笔委托数据
        entrust = get_individual_entrust()
        log.info(entrust)
        # 获取指定股票列表逐笔委托数据
        entrust = get_individual_entrust(["000002.SZ", "000032.SZ"])
        log.info(entrust)
        # 获取委托量
        if entrust is not None:
            business_amount = entrust.query('code in ["000002.SZ"]')["business_amount"]
            log.info("逐笔数据的委托量为：%s" % business_amount)

        # 返回字典类型数据
        entrust = get_individual_entrust([g.security], is_dict=True)
        log.info("逐笔委托数据为：%s" % entrust)
        g.flag = True
get_individual_transaction - 获取逐笔成交行情
get_individual_transaction(stocks=None, data_count=50, start_pos=0, search_direction=1, is_dict=False)
使用场景
该函数在交易模块可用

接口说明
该接口用于获取当日逐笔成交行情数据。

注意事项：

沪深市场都有逐笔成交数据。
逐笔委托，逐笔成交数据需开通level2行情才能获取到数据，否则无数据返回。
当策略入参is_dict为True时返回的数据类型为dict，返回dict类型数据的速度比(python3.11版本支持)DataFrame,(python3.5版本支持)Panel类型数据有大幅提升。
参数
stocks: 默认为当前股票池中代码列表(list[str])；

data_count: 数据条数，默认为50，最大为200(int)；

start_pos: 起始位置，默认为0(int)；

search_direction: 搜索方向(1向前，2向后)，默认为1(int)；

is_dict: 返回类型（False-(python3.11版本支持)DataFrame,(python3.5版本支持)Panel; True-dict），默认为False；

返回
dict类型
正常返回dict类型数据，异常时返回None(NoneType)。

返回的数据格式如下：

{股票代码(str): [[时间戳毫秒级(int), 价格(float), 成交数量(int), 成交编号(int), 成交方向(int), 叫买方编号(int), 叫卖方编号(int), 成交标记(int), 盘后逐笔成交序号标识(int), 成交通道信息(int)], ...], "fields": ["business_time", "hq_px", "business_amount", "trade_index", "business_direction", "buy_no", "sell_no", "trans_flag", 'trans_identify_am", "channel_num"]}

{"600570.SS": [[20220913111141472, 36.47, 100, 3286989, 1, 5807243, 5804930, 0, 0, 2], ...], "fields": ["business_time", "hq_px", "business_amount", "trade_index", "business_direction", "buy_no", "sell_no", "trans_flag", 'trans_identify_am", "channel_num"]}

非dict类型
默认返回(python3.11版本支持)DataFrame,(python3.5版本支持)Panel类型，入参is_dict为True时返回dict类型。

1.(仅python3.11版本支持)DataFrame类型类型，异常时返回None(NoneType)
输出字段如下所示：

code: 代码(str)；
business_time: 时间戳毫秒级(int)；
hq_px: 价格(float)；
business_amount: 成交数量(int)；
trade_index: 成交编号(int)；
business_direction: 成交方向(int)；
buy_no: 叫买方编号(int)；
sell_no: 叫卖方编号(int)；
trans_flag: 成交标记(int)；
trans_identify_am: 盘后逐笔成交序号标识(int)；
channel_num: 成交通道信息(int)；
2.(仅python3.5版本支持)正常返回Pandas.panel对象，异常时返回None(NoneType)
Items axis: 股票代码列表(str)；

Major_axis axis: 数据索引为自然数列(DataFrame)；

Minor_axis axis: 包含以下信息：

business_time: 时间戳毫秒级(str:numpy.int64)；
hq_px: 价格(str:numpy.float64)；
business_amount: 成交数量(str:numpy.int64)；
trade_index: 成交编号(str:numpy.int64)；
business_direction: 成交方向(str:numpy.int64)；
buy_no: 叫买方编号(str:numpy.int64)；
sell_no: 叫卖方编号(str:numpy.int64)；
trans_flag: 成交标记(str:numpy.int64)；
trans_identify_am: 盘后逐笔成交序号标识(str:numpy.int64)；
channel_num: 成交通道信息(str:numpy.int64)；
示例
def initialize(context):
    g.security = "000001.SZ"
    set_universe(g.security)

def before_trading_start(context, data):
    g.flag = False

def handle_data(context, data):
    if not g.flag:
        # 获取当前股票池逐笔成交数据
        transaction = get_individual_transaction()
        log.info(transaction)
        # 获取指定股票列表逐笔成交数据
        transaction = get_individual_transaction(["000002.SZ", "000032.SZ"])
        log.info(transaction)
        # 获取成交量
        if transaction is not None:
            business_amount = transaction.query('code in ["000002.SZ"]')["business_amount"]
            log.info("逐笔数据的成交量为：%s" % business_amount)

        # 返回字典类型数据
        transaction = get_individual_transaction([g.security], is_dict=True)
        log.info("逐笔成交数据为：%s" % transaction)
        g.flag = True
get_tick_direction- 获取分时成交行情
get_tick_direction(symbols=None, query_date=0, start_pos=0, search_direction=1, data_count=50, is_dict=False)
使用场景
该函数在交易模块可用

接口说明
该接口用于获取当日分时成交行情数据。

注意事项：

沪深市场都有分时成交数据。
当策略入参is_dict为True时返回的数据类型为dict，返回dict类型数据的速度比OrderedDict类型数据有提升。
参数
symbols: 单只标的代码(str)或代码列表(list[str])；

query_date: 查询日期，默认为0，返回当日日期数据(目前行情只支持查询当日的数据，格式为YYYYMMDD)(int)；

start_pos: 起始位置，默认为0(int)；

search_direction: 搜索方向(1向前，2向后)，默认为1(int)；

data_count: 数据条数，默认为50，最大为200(int)；

is_dict: 返回类型（False-OrderedDict; True-dict），默认为False；

返回
入参is_dict为True时返回dict类型，为False(默认)时返回OrderedDict类型。

dict类型
返回的数据格式如下：

{股票代码(str): [[时间戳毫秒级(int), 价格(float), 价格(int), 成交数量(int), 成交金额(int), 成交笔数(int), 成交方向(int), 持仓量(int), 分笔关联的逐笔开始序号(int), 分笔关联的逐笔结束序号(int)], ...], "fields": ["time_stamp", "hq_px", "hq_px64", "business_amount", "business_balance", "business_count", "business_direction", "amount", "start_index", "end_index"]}

{"600570.SS": [[20220915132138000, 36.18, 0, 2600, 94062, 6, 1, 0, 0, 0], "fields": ["time_stamp", "hq_px", "hq_px64", "business_amount", "business_balance", "business_count", "business_direction", "amount", "start_index", "end_index"]}

OrderedDict类型
返回结果字段介绍：

time_stamp: 时间戳毫秒级(int)；
hq_px: 价格(float)；
hq_px64: 价格(int)(行情暂不支持，返回均为0)；
business_amount: 成交数量(int)；
business_balance: 成交金额(int)；
business_count: 成交笔数(int)；
business_direction: 成交方向(int)；
amount: 持仓量(int)(行情暂不支持，返回均为0)；
start_index: 分笔关联的逐笔开始序号(int)(行情暂不支持，返回均为0)；
end_index: 分笔关联的逐笔结束序号(int)(行情暂不支持，返回均为0)；
示例
def initialize(context):
    g.security = "600570.SS"
    set_universe(g.security)

def handle_data(context, data):
    # 获取分时成交数据
    direction_data = get_tick_direction([g.security])
    log.info(direction_data)
    # 获取成交量
    business_amount = direction_data[g.security]["business_amount"]
    log.info("分时成交的成交量为：%s" % business_amount)

    # 返回字典类型数据
    # 获取字典类型分时成交数据
    direction_data = get_tick_direction([g.security], is_dict=True)
    log.info(direction_data)
get_sort_msg - 获取板块、行业的快照信息
get_sort_msg(sort_type_grp=None, sort_field_name=None, sort_type=1, data_count=100)
使用场景
该函数在交易模块可用

接口说明
该接口用于获取板块、行业的快照信息(可按指定字段进行排序展示)。

注意事项：

证监会行业、聚源行业、概念板块、地域板块所对应标的的行情数据为非标准的交易所下发数据，是由数据源自行按照成分股分类规则进行计算的，存在与三方数据源不一致的情况。如用户需要在策略中使用，应自行评估该数据的合理性

参数
sort_type_grp: 板块或行业的代码(list[str]/str)；(暂时只支持XBHS.DY地域、XBHS.GN概念、XBHS.ZJHHY证监会行业、XBHS.ZS指数、XBHS.HY行业等)

sort_field_name: 需要排序的字段(str)；该字段支持输入的参数如下：

preclose_px: 昨日收盘价；
open_px: 今日开盘价；
last_px: 最新价；
high_px: 最高价；
low_px: 最低价；
wavg_px: 加权平均价；
business_amount: 总成交量；
business_balance: 总成交额；
px_change: 涨跌额；
amplitude: 振幅；
px_change_rate: 涨跌幅；
circulation_amount: 流通股本；
total_shares: 总股本；
market_value: 市值；
circulation_value: 流通市值；
vol_ratio: 量比；
rise_count: 上涨家数；
fall_count: 下跌家数；
sort_type: 排序方式，默认降序(0:升序，1:降序)(int)；

data_count: 数据条数，默认为100，最大为10000(int)；

返回
正常返回一个List列表，里面包含板块、行业代码的涨幅排名信息(list[dict{str:str,...},...])，

返回每个代码的信息包含以下字段内容：

prod_code: 行业代码(str:str)；
prod_name: 行业名称(str:str)；
hq_type_code: 行业板块代码(str:str)；
time_stamp: 时间戳毫秒级(str:int)；
trade_mins: 交易分钟数(str:int)；
trade_status: 交易状态(str:str)；
preclose_px: 昨日收盘价(str:float)；
open_px: 今日开盘价(str:float)；
last_px: 最新价(str:float)；
high_px: 最高价(str:float)；
low_px: 最低价(str:float)；
wavg_px: 加权平均价(str:float)；
business_amount: 总成交量(str:int)；
business_balance: 总成交额(str:int)；
px_change: 涨跌额(str:float)；
amplitude: 振幅(str:int)；
px_change_rate: 涨跌幅(str:float)；
circulation_amount: 流通股本(str:int)；
total_shares: 总股本(str:int)；
market_value: 市值(str:int)；
circulation_value: 流通市值(str:int)；
vol_ratio: 量比(str:float)；
shares_per_hand: 每手股数(str:int)；
rise_count: 上涨家数(str:int)；
fall_count: 下跌家数(str:int)；
member_count: 成员个数(str:int)；
rise_first_grp: 领涨股票(其包含以下五个字段)(str:list[dict{str:int,str:str,str:str,str:float,str:float},...])；
prod_code: 股票代码(str:str)；
prod_name: 证券名称(str:str)；
hq_type_code: 类型代码(str:str)；
last_px: 最新价(str:float)；
px_change_rate: 涨跌幅(str:float)；
fall_first_grp: 领跌股票(其包含以下五个字段)(str:list[dict{str:int,str:str,str:str,str:float,str:float},...])；
prod_code: 股票代码(str:str)；
prod_name: 证券名称(str:str)；
hq_type_code: 类型代码(str:str)；
last_px: 最新价(str:float)；
px_change_rate: 涨跌幅(str:float)；
示例
def initialize(context):
    g.security = '000001.SZ'
    set_universe(g.security)

def handle_data(context, data):
    #获取XBHS.DY板块按preclose_px字段排序的排名信息
    sort_data = get_sort_msg(sort_type_grp='XBHS.DY', sort_field_name='preclose_px', sort_type=1, data_count=100)
    log.info(sort_data)
    #获取sort_data排序第一条代码的数据
    sort_data_first = sort_data[0]
    log.info(sort_data_first)
get_gear_price - 获取指定代码的档位行情价格
get_gear_price(sids)
使用场景
该函数仅在交易模块可用

接口说明
该接口用于获取指定代码的档位行情价格。

注意事项：

获取实时行情快照失败时返回档位内容为空dict({"bid_grp": {}, "offer_grp": {}})。
若无L2行情时，委托笔数字段返回0。
参数
sids：股票代码(list[str]/str)；

返回
包含以下信息(dict[str:dict[int:list[float,int,int],...],...])：

bid_grp:委买档位(str:dict[int:list[float,int,int],...])；
offer_grp:委卖档位(str:dict[int:list[float,int,int],...])；
单只代码返回：
{'bid_grp': {1: [价格, 委托量,委托笔数], 2: [价格, 委托量,委托笔数], 3: [价格, 委托量,委托笔数], 4: [价格, 委托量,委托笔数], 5: [价格, 委托量,委托笔数]},
 'offer_grp': {1: [价格, 委托量,委托笔数], 2: [价格, 委托量,委托笔数], 3: [价格, 委托量,委托笔数], 4: [价格, 委托量,委托笔数], 5: [价格, 委托量,委托笔数]}}
多只代码返回：
{代码：{'bid_grp': {1: [价格, 委托量,委托笔数], 2: [价格, 委托量,委托笔数], 3: [价格, 委托量,委托笔数], 4: [价格, 委托量,委托笔数], 5: [价格, 委托量,委托笔数]},
 'offer_grp': {1: [价格, 委托量,委托笔数], 2: [价格, 委托量,委托笔数], 3: [价格, 委托量,委托笔数], 4: [价格, 委托量,委托笔数], 5: [价格, 委托量,委托笔数]}}
}
示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def handle_data(context, data):
    #获取600570.SS当前档位行情
    gear_price = get_gear_price('600570.SS')
    log.info(gear_price)
    #获取600571.SS当前档位行情
    gear_price = get_gear_price('600571.SS')
    log.info(gear_price)
get_snapshot - 取行情快照
get_snapshot(security)
使用场景
该函数仅在交易模块可用

接口说明
该接口用于获取实时行情快照。

注意事项：

证监会行业、聚源行业、概念板块、地域板块所对应标的的行情数据为非标准的交易所下发数据，是由数据源自行按照成分股分类规则进行计算的，存在与三方数据源不一致的情况。如用户需要在策略中使用，应自行评估该数据的合理性

参数
security： 单只股票代码或者多只股票代码组成的列表，必填字段(list[str]/str)；

返回
正常返回一个dict类型数据，包含每只股票代码的行情快照信息，其中key为股票代码，value为对应的快照信息。异常返回空dict，如{}(dict[str:dict[...]])

快照包含以下信息：

amount:持仓量(str:int)(期货字段,股票返回0)；
bid_grp:委买档位(第一档包含委托队列(仅L2支持))(str:dict[int:list[float,int,int,{int:int,...}],int:list[float,int,int]...])；
business_amount:总成交量(str:int)；
business_amount_in:内盘成交量(str:int)；
business_amount_out:外盘成交量(str:int)；
business_balance:总成交额(str:float)；
business_count:成交笔数(str:int)
circulation_amount:流通股本(str:int)；
current_amount:最近成交量(现手)(str:int)；
down_px:跌停价格(str:float)；
end_trade_date:最后交易日(str:str)
entrust_diff:委差(str:float)；
entrust_rate:委比(str:float)；
high_px:最高价(str:float)；
hsTimeStamp:时间戳(str:float)；
last_px:最新成交价(str:float)；
low_px:最低价(str:float)；
offer_grp:委卖档位(第一档包含委托队列(仅L2支持))(str:dict[int:list[float,int,int,{int:int,...}],int:list[float,int,int]...])；
open_px:今开盘价(str:float)；
pb_rate:市净率(str:float)；
pe_rate:动态市盈率(str:float)；
preclose_px:昨收价(str:float)；
prev_settlement:昨结算(str:float)(期货字段,股票返回0.0)；
px_change_rate:涨跌幅(str:float)；
settlement:结算价(str:float)(期货字段,股票返回0.0)
start_trade_date:首个交易日(str:float)
tick_size:最小报价单位(str:float)
total_bid_turnover:委买金额(str:int)；
total_bidqty:委买量(str:int)；
total_offer_turnover:委卖金额(str:int)
total_offerqty:委卖量(str:int)；
trade_mins:交易分钟数(str:int)
trade_status:交易状态(str:str)；
turnover_ratio:换手率(str:int)；
up_px:涨停价格(str:float)；
vol_ratio:量比(str:float)；
wavg_px:加权平均价(str:float)；
iopv:基金份额参考净值(str:float)；
字段备注:

bid_grp -- 委买档位，{'bid_grp': {1: [价格, 委托量,委托笔数,委托对列{}], 2: [价格, 委托量,委托笔数], 3: [价格, 委托量,委托笔数], 4: [价格, 委托量,委托笔数], 5: [价格, 委托量,委托笔数]}} ；
offer_grp -- 委卖档位，{'offer_grp': {1: [价格, 委托量,委托笔数,委托对列{}], 2: [价格, 委托量,委托笔数], 3: [价格, 委托量,委托笔数], 4: [价格, 委托量,委托笔数], 5: [价格, 委托量,委托笔数]}} ；
total_bid_turnover/total_offer_turnover,委买金额/委卖金额主推数据(tick数据中)不支持(值为0)，仅在线请求中支持；
返回如下:

{'600570.SS': {'offer_grp': {1: [44.47, 3300, 0, {}], 2: [44.48, 2800, 0], 3: [44.49, 3900, 0], 4: [44.5, 17300, 0], 5: [44.51, 1600, 0]}, 'open_px': 44.91, 'pe_rate': 4294573.83, 'pb_rate': 11.42, 'entrust_diff': -100.0, 'entrust_rate': -0.2092, 'total_bidqty': 18900, 'preclose_px': 45.2, 'total_offer_turnover': 0, 'business_amount_out': 2600706, 'px_change_rate': -1.62, 'turnover_ratio': 0.0042, 'total_bid_turnover': 0, 'vol_ratio': 1.12, 'hsTimeStamp': 20220622102358580, 'amount': 0, 'prev_settlement': 0.0, 'circulation_amount': 1461560480, 'low_px': 44.31, 'down_px': 40.68, 'bid_grp': {1: [44.45, 600, 0, {}], 2: [44.44, 600, 0], 3: [44.43, 8300, 0], 4: [44.42, 9200, 0], 5: [44.41, 200, 0]}, 'business_balance': 274847503.0, 'business_amount': 6161800, 'business_amount_in': 3561094, 'last_px': 44.47, 'total_offerqty': 28900, 'up_px': 49.72, 'wavg_px': 44.6, 'high_px': 45.05, 'trade_status': 'TRADE', 'iopv': '0.0'}}
示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def handle_data(context, data):
    # 行情快照
    snapshot = get_snapshot(g.security)
    log.info(snapshot)
get_trend_data - 获取集中竞价期间代码数据
get_trend_data(date=None, stocks=None, market=None)
使用场景
该函数在研究、回测、交易模块可用

接口说明
获取集中竞价期间代码数据。

注意事项：

不传参数时，默认返回当日XSHE,XSHG市场所有代码的数据。
stocks和market不能同时入参。
获取失败时返回空dict{}

参数
date：日期(格式为：YYYYmmdd)(str)；

stocks：股票代码(str/list[str])；

market：市场(str/list[str])

返回
正常返回一个dict类型数据，包含每只代码的信息

包含以下信息：

time_stamp:时间戳(int)；
hq_px:价格(float)；
wavg_px:加权价格(float)；
business_amount:总成交量(int)；
business_balance:总成交额(int)；
amount:持仓量(int)；
示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def handle_data(context, data):
    trend_data = get_trend_data(stocks='600570.SS')
    log.info(trend_data)
    trend_data = get_trend_data("20230308")
    log.info(trend_data['600570.SS'])
    trend_data = get_trend_data(market=["XSHG", "XSHE"])
    log.info(trend_data['600570.SS'])
获取证券信息
get_stock_name - 获取证券名称
get_stock_name(stocks)
使用场景
该函数在研究、回测、交易模块可用

接口说明
该接口可获取股票、可转债、ETF等名称。

注意事项：

交易场景下，默认每个交易日的09:07分~09:09之间完成当天数据的更新，因此在9:10分之后正常情况是可以获取到当天更新的数据的，比如当日新股的基础信息。如果当日未更新，新股返回空dict
参数
stocks：证券代码(list[str]/str)；

返回
证券名称字典，dict类型，key为证券代码，value为证券名称(dict[str:str])。当没有查询到相关数据或者输入有误时value为None(NoneType)；

{'600570.SS': '恒生电子'}
示例
def initialize(context):
    g.security = ['600570.SS', '600571.SS']
    set_universe(g.security)

def handle_data(context, data):
    #获取600570.SS股票名称
    stock_name = get_stock_name(g.security[0])
    log.info(stock_name)
    #获取股票池所有的证券名称
    stock_names = get_stock_name(g.security)
    log.info(stock_names)
get_stock_info - 获取证券基础信息
get_stock_info(stocks, field=None)
使用场景
该函数在研究、回测、交易模块可用

接口说明
该接口可获取股票、可转债、ETF等基础信息。

注意事项：

field不做入参时默认只返回stock_name字段。
参数
stocks：证券代码(list[str]/str)；

field：指明数据结果集中所支持输出字段(list[str]/str)，输出字段包括 ：

stock_name -- 证券代码对应公司名(str:str)；
listed_date -- 证券上市日期(str:str)；
de_listed_date -- 证券退市日期，若未退市，返回2900-01-01(str:str)；
返回
嵌套dict类型，包含内容为field中指定内容，若field=None，返回证券基础信息仅包含对应公司名(dict[str:dict[str:str,...],...])

{'600570.SS': {'stock_name': '恒生电子', 'listed_date': '2003-12-16', 'de_listed_date': '2900-01-01'}}
示例
def initialize(context):
    g.security = ['600570.SS', '600571.SS']
    set_universe(g.security)

def handle_data(context, data):
    #获取单支证券的基础信息
    stock_info = get_stock_info(g.security[0])
    log.info(stock_info)
    #获取多支证券的基础信息
    stock_infos = get_stock_info(g.security, ['stock_name','listed_date','de_listed_date'])
    log.info(stock_infos)
get_stock_status - 获取证券状态信息
get_stock_status(stocks, query_type='ST', query_date=None)
使用场景
该函数在研究、回测、交易模块可用

接口说明
该接口用于获取指定日期证券的ST、停牌、退市等属性。

注意事项：

无

参数
stocks: 例如 ['000001.SZ','000003.SZ']。该字段必须输入，否则返回None(list[str]/str)；

query_type: 支持以下四种类型属性的查询，默认为'ST'(str)；

具体支持输入的字段包括 ：

'ST' - 查询是否属于ST证券
'HALT' - 查询是否停牌
'DELISTING' - 查询是否退市
'DELISTING_SORTING' - 查询是否退市整理期(只支持交易场景下查询当日数据，查询历史返回空字典)
query_date: 格式为YYYYmmdd，默认为None,表示当前日期(回测为回测当前周期，研究与交易则取系统当前时间)(str)；

返回
返回dict类型，每支证券对应的值为True或False(dict[str:bool,...])。当没有查询到相关数据或者输入有误时返回None(NoneType)；

{'600570': None}
示例
def initialize(context):
    g.security = ['600397.SS', '600701.SS', '000001.SZ']
    set_universe(g.security)

def handle_data(context, data):
    stocks_list = g.security
    filter_stocks = []
    # 判断证券是否为ST、停牌或者退市
    st_status = get_stock_status(stocks_list, 'ST')
    # 将不是ST的证券筛选出来
    for i in stocks_list:
        if st_status[i] is not True:
            filter_stocks.append(i)
    # 获取证券停牌信息
    # halt_status = get_stock_status(stocks_list, 'HALT')
    # 获取指定日期的对应属性
    # halt_status = get_stock_status(stocks_list, 'HALT', '20180312')
    # 获取证券退市信息
    # delist_status = get_stock_status(stocks_list, 'DELISTING')
    log.info('筛选不是ST的证券列表: %s' % filter_stocks)
get_underlying_code - 获取证券的关联代码
get_underlying_code(symbols)
使用场景
该函数在交易模块可用

接口说明
该接口用于获取证券的关联代码。

注意事项：

无

参数
symbols: 需要查询的代码(str/list)

返回
正常返回一个dict字典，里面包含需要查询的证券，关联类型和关联代码(dict{str:[int,str],...})，

返回每个代码的信息包含以下字段内容：

underlying_type: 关联类型(int)；
underlying_code: 关联代码(str)；
示例
def initialize(context):
    g.security = '000001.SZ'
    set_universe(g.security)

def handle_data(context, data):
    #获取110063.SS的关联的代码信息
    underlying_code_info = get_underlying_code("110063.SS")
    log.info(underlying_code_info)
    #获取110063.SS的正股代码
    underlying_code = underlying_code_info["110063.SS"][1]
    log.info(underlying_code)
get_stock_exrights - 获取证券除权除息信息
get_stock_exrights(stock_code, date=None)
使用场景
该函数在研究、回测、交易模块可用

接口说明
该接口用于获取证券除权除息信息。

注意事项：

无

参数
stock_code; str类型, 证券代码(str)；

date: 查询该日期的除权除息信息，默认获取该证券历史上所有除权除息信息，e.g. '20180228'/20180228/datetime.date(2018,2,28)(str/int/datetime.date)

返回
输入日期若没有除权除息信息则返回None(NoneType),有相关数据则返回pandas.DataFrame类型数据

例如输入get_stock_exrights('600570.SS')，返回


         allotted_ps   rationed_ps   rationed_px   bonus_ps   exer_forward_a   exer_forward_b   exer_backward_a   exer_backward_b
date
20040604  0.0          0.0           0.0           0.43       0.046077         -1.433            1.000000         0.430
20050601  0.5          0.0           0.0           0.20       0.046077         -1.413            1.500000         0.630
20050809  0.4          0.0           0.0           0.00       0.069115         -1.404            2.100000         0.630
20060601  0.4          0.0           0.0           0.11       0.096762         -1.404            2.940000         0.861
20070423  0.3          0.0           0.0           0.10       0.135466         -1.394            3.822000         1.155
20080528  0.6          0.0           0.0           0.07       0.176106         -1.380            6.115200         1.422
20090423  0.5          0.0           0.0           0.10       0.281770         -1.368            9.172799         2.034
20100510  0.4          0.0           0.0           0.05       0.422654         -1.340            12.841919        2.492
20110517  0.0          0.0           0.0           0.05       0.591716         -1.318            12.841919        3.134
20120618  0.0          0.0           0.0           0.08       0.591716         -1.289            12.841919        4.162
20130514  0.0          0.0           0.0           0.10       0.591716         -1.242            12.841919        5.446
20140523  0.0          0.0           0.0           0.16       0.591716         -1.182            12.841919        7.501
20150529  0.0          0.0           0.0           0.18       0.591716         -1.088            12.841919        9.812
20160530  0.0          0.0           0.0           0.26       0.591716         -0.981            12.841919        13.151
20170510  0.0          0.0           0.0           0.10       0.591716         -0.827            12.841919        14.435
20180524  0.0          0.0           0.0           0.29       0.591716         -0.768            12.841919        18.159
20190515  0.3          0.0           0.0           0.32       0.591716         -0.597            16.694494        22.269
20200605  0.3          0.0           0.0           0.53       0.769231         -0.407            21.702843        31.117
返回结果字段介绍：

date -- 日期(索引列，类型为int64)；
allotted_ps -- 每股送股(str:numpy.float64)；
rationed_ps -- 每股配股(str:numpy.float64)；
rationed_px -- 配股价(str:numpy.float64)；
bonus_ps -- 每股分红(str:numpy.float64)；
exer_forward_a -- 前复权除权因子A；用于计算前复权价格(前复权价格=A*价格+B)(str:numpy.float64)
exer_forward_b -- 前复权除权因子B；用于计算前复权价格(前复权价格=A*价格+B)(str:numpy.float64)
exer_backward_a -- 后复权除权因子A；用于计算后复权价格(后复权价格=A*价格+B)(str:numpy.float64)
exer_backward_b -- 后复权除权因子B；用于计算后复权价格(后复权价格=A*价格+B)(str:numpy.float64)
示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def handle_data(context, data):
    stock_exrights = get_stock_exrights(g.security)
    log.info('the stock exrights info of security %s:\n%s' % (g.security, stock_exrights))
get_stock_blocks - 获取证券所属板块信息
get_stock_blocks(stock_code)
使用场景
该函数在研究、回测、交易模块可用

接口说明
该接口用于获取证券所属板块。

注意事项：

该函数获取的是当下的数据，因此回测不能取到真正匹配回测日期的数据，注意未来函数。
已退市证券无法成功获取数据，接口会返回None。
聚源行业、概念板块、地域板块的成分股分类规则由数据源决定，存在与三方数据源不一致的情况。如用户需要在策略中使用，应自行评估该数据的合理性
参数
stock_code: 证券代码(str)；

返回
获取成功返回dict类型，包含所属行业、板块等详细信息(dict[str:list[list[str,str],...],...])，获取失败返回None(NoneType)。返回数据如：

{
'HGT': [['HGTHGT.XBHK', '沪股通']],
'HY': [['710200.XBHS', '计算机应用']],
'DY': [['DY1172.XBHS', '浙江板块']],
'ZJHHY': [['I65000.XBHS', '软件和信息技术服务业']],
'GN': [['003596.XBHS', '融资融券'], ['003631.XBHS', '转融券标的'], ['003637.XBHS', '互联网金融'], ['003665.XBHS', '电商概念'], ['003707.XBHS', '沪股通'], ['003718.XBHS', '证金持股'], ['003800.XBHS', '人工智能'], ['003830.XBHS', '区块链'], ['031027.XBHS', 'MSCI概念'], ['B10003.XBHS', '蚂蚁金服概念']]
}
示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def handle_data(context, data):
    blocks = get_stock_blocks(g.security)
    log.info('security %s in these blocks:\n%s' % (g.security, blocks))
get_index_stocks- 获取指数成分股
get_index_stocks(index_code,date)
使用场景
该函数在研究、回测、交易模块可用

接口说明
该接口用于获取一个指数在平台可交易的成分股列表，指数列表

注意事项：

在回测中，date不入参默认取当前回测周期所属历史日期。
在研究中，date不入参默认取的是当前日期。
在交易中，date不入参默认取的是当前日期。
参数
index_code：指数代码，如沪深300：000300.SS或000300.XBHS(str)

date：日期，输入形式必须为'YYYYMMDD'，如'20170620'，不输入默认为当前日期(str)；

返回
返回股票代码的list(list[str,...])。

['000001.SZ', '000002.SZ', '000063.SZ', '000069.SZ', '000100.SZ', '000157.SZ', '000425.SZ', '000538.SZ', '000568.SZ', '000625.SZ', '000651.SZ', '000725.SZ', '000728.SZ', '000768.SZ', '000776.SZ',
 '000783.SZ', '000786.SZ', ..., '603338.SS', '603939.SS', '603233.SS', '600426.SS', '688126.SS', '600079.SS', '600521.SS', '600143.SS', '000800.SZ'] 
示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def before_trading_start(context, data):
    # 获取当前所有沪深300的股票
    g.stocks = get_index_stocks('000300.XBHS')
    log.info(g.stocks)
    # 获取2016年6月20日所有沪深300的股票, 设为股票池
    g.stocks = get_index_stocks('000300.XBHS','20160620')
    set_universe(g.stocks)
    log.info(g.stocks)

def handle_data(context, data):
    pass
get_industry_stocks- 获取行业成份股
get_industry_stocks(industry_code)
使用场景
该函数在研究、回测、交易模块可用

接口说明
该接口用于获取一个行业的所有股票，行业列表

注意事项：

该函数获取的是当下的数据，因此回测不能取到真正匹配回测日期的数据，注意未来函数。
聚源行业、概念板块、地域板块的成分股分类规则由数据源决定，存在与三方数据源不一致的情况。如用户需要在策略中使用，应自行评估该数据的合理性
参数
industry_code: 行业编码，尾缀必须是.XBHS 如农业股：A01000.XBHS(str)

返回
返回股票代码的list(list[str,...])

['300970.SZ', '300087.SZ', '300972.SZ', '002772.SZ', '000998.SZ', '002041.SZ', '600598.SS', '600371.SS', '600506.SS', '300511.SZ', '600359.SS', '600354.SS', '601118.SS', '600540.SS', '300189.SZ',
 '600313.SS', '600108.SS'] 
示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def before_trading_start(context, data):
    # 获取农业的股票, 设为股票池
    stocks = get_industry_stocks('A01000.XBHS')
    set_universe(stocks)
    log.info(stocks)

def handle_data(context, data):
    pass
get_fundamentals-获取财务数据
get_fundamentals(security, table, fields = None, date = None, start_year = None, end_year = None, report_types = None, merge_type = None, is_dataframe = False)
使用场景
该函数可在研究、回测、交易模块使用

接口说明
该接口用于获取财务三大报表数据、日频估值数据、各项财务能力指标数据。

注意事项：

growth_ability（成长能力指标）、profit_ability（盈利能力指标）、eps（每股指标）、operating_ability（营运能力指标）、debt_paying_ability（偿债能力指标）五张表的数据非pit类型数据（即:按日期请求返回最近发布的财务数据）。
非pit类型数据在一个财报期范围内按日期请求数据时，假如某股票并未发布该期财报，将无法获取到财务数据。
如以下情况：
get_fundamentals('600570.SS','eps',date='20240301')
2024-01-01~2024-03-31为2023年年报的披露期，但实际上恒生电子年报披露日期为2024-03-19，date按20240301请求时，会判断为此次请求的是2023年年报，但实际未发布，因此会返回None。
建议用户输入年份范围内对应季度获取财务数据，但需注意未来数据的影响。实际操作可以参考单因子策略demo获取数据的方法。
科创板存托凭证(九号公司:689009.SS)没有财务报表披露信息。
参数
为保持各表接口统一，输入字段略有不同，具体可参见 财务数据的API接口说明

security：一支股票代码或者多只股票代码组成的list(list[str])

table：财务数据表名，输入具体表名可查询对应表中信息(str)

表名	包含内容
valuation	估值数据
balance_statement	资产负债表
income_statement	利润表
cashflow_statement	现金流量表
growth_ability	成长能力指标
profit_ability	盈利能力指标
eps	每股指标
operating_ability	营运能力指标
debt_paying_ability	偿债能力指标
fields：指明数据结果集中所需输出业务字段，支持多个业务字段输出(list类型)，如fields=['settlement_provi', 'client_provi'](list[str])；输出具体字段请参考 财务数据的API接口说明

date：查询日期，按日期查询模式，返回查询日期之前对应的财务数据，输入形式如'20170620'；支持datetime.date时间格式输入，不能与start_year与end_year同时作用；支持按日期查询模式，不传入date时默认取回测日期的上一个交易日数据(str)；

start_year：查询开始年份，按年份查询模式，返回输入年份范围内对应的财务数据，如'2015'，start_year与end_year必须同时输入，且不能与date同时作用(str)

end_year：查询截止年份，按年份查询模式，返回输入年份范围内对应的财务数据，如'2015'，start_year与end_year必须同时输入，且不能与date同时作用(str)

report_types：财报类型；如果为年份查询模式(start_year/end_year)，不输入report_types返回当年可查询到的全部类型财报；如果为日期查询模式(date)，不输入report_types返回距离指定日期最近一份财报(str)。

'1':表示获取一季度财报
'2':表示获取半年报
'3':表示获取截止到三季度财报
'4':表示获取年度财报
(已废弃)date_type：数据参考时间设置，该参数只适用于按日期查询模式(date参数模式)(int) ：

(已废弃)date_type不传或传入date_type = None，返回发布日期(publ_date)在查询日期(date)之前指定财报类型数据(report_types)，若未指定财报类型(report_types)则默认为离查询日期(date)最近季度的数据，数据未公布用NAN填充
(已废弃)date_type传入1，返回会计周期(end_date)在查询日期(date)之前指定财报类型数据(report_types)，若未指定财报类型(report_types)则默认为查询日期(date)最近季度会计周期的数据，数据未公布用NAN填充
merge_type：数据更新设置；相关财务数据信息会不断进行修正更新，为了避免未来数据影响，可以通过参数获取原始发布或最新发布数据信息；只有部分表包含此字段(int) ：

merge_type不传或传入merge_type = None，获取首次发布的数据，即使实际数据发生变化，也只返回原样数据信息；回测场景为避免未来数据建议使用此模式
merge_type传入1，获取已发布财报数据的更新数据，更新数据范围包括但不限于相关日期数据，研究场景或交易场景建议使用此模式，但需要指定报告期，否则会获取到历史最近一期有过更新情况的财报数据(不一定是最近一个财报期)
is_dataframe：True-返回DataFrame格式;False-返回pandas.Panel格式(默认,仅python3.5的按年份查询模式有效)。

注意：

date字段与start_year/end_year不能同时输入，否则按日期查询模式(date参数模式)
当date和start_year/end_year相关数据都不传入时，默认为按日期查询模式(date参数模式)，研究和回测中date取值有所不同：在研究中，date取的是当前日期；回测中取回测日期的上一个交易日数据
fields不传入的情况下，date必须传入，否则会报错。正确调用示例：get_fundamentals('600570.XSHG', 'balance_statement', date='2018-06-01')
返回
返回值形式根据输入参数类型不同而有所区分：

1.(python3.11、python3.5版本均支持)按日期查询模式(date参数模式)返回数据类型为pandas.DataFrame类型，索引为股票代码，如get_fundamentals('600000.SS','balance_statement',date='20161201')将返回：

secu_abbr	end_date	publ_date	total_assets	……	total_liability
600000.SS	浦发银行	2016-09-30	2016-10-29	5.56e+12	......	5.20e+12
2.(python3.11版本支持)按年份查询模式(start_year/end_year参数模式)返回数据类型为pandas.DataFrame类型，索引为股票代码(secu_code)和对应会计日期(end_date)。

3.(python3.5版本支持)按年份查询模式(start_year/end_year参数模式)返回数据类型为pandas.Panel类型，索引为股票代码，其中包含的DataFrame索引为返回股票对应会计日期(end_date)，如get_fundamentals(['600000.SS', '600570.SS', '000002.SZ'], 'balance_statement', start_year='2016', end_year='2016')将返回：




示例
import time
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def before_trading_start(context, data):
     # 假设取4000股*10年一季报数据为4万条，之后再取中报又是4万条，因为规则要求每秒不得调用超过100次(单次最大调用量是500条数据)，调用过程就需要sleep1秒，防止流控触发。
     funda_data = get_fundamentals(g.security, 'balance_statement', fields = 'total_assets', start_year='2011', end_year='2020', report_types = '1')
     time.sleep(1)
     funda_data = get_fundamentals(g.security, 'balance_statement', fields = 'total_assets', start_year='2010', end_year='2020', report_types = '2')
def handle_data(context, data):
     # 获取股票池
     stocks = get_index_stocks('000906.XBHS')
     # 指定股票池
     stocks = ['600000.SS','600570.SS']

     # 获取数据的两种模式
     # 1. 按日期查询模式(默认以发布日期为参考时间)：返回输入日期之前对应的财务数据
     # 在回测中获取单一股票中对应回测日期资产负债表中资产总计(total_assets)数据
     #(回测中date默认获取回测日期，无需传入date，除非在回测中获取指定某个日期的数据，日期格式如”20160628”)
     get_fundamentals('600000.SS', 'balance_statement', 'total_assets')

     # 获取股票池中对应上市公司在2016年6月28日之前发布的最近季度(即2016年一季度)
     # 的资产负债表中资产总计(total_assets)数据，如果到查询日期为止一季度数据还,未发布则所有数据用Nan填充
     get_fundamentals(stocks, 'balance_statement', 'total_assets','20160628')

     # 获取股票池中对应上市公司在2016年6月28日最近会计周期(即20160331)的资产负
     # 债表中资产总计(total_assets)数据，如果未查到相关数据则用Nan填充
     get_fundamentals(stocks, 'balance_statement', 'total_assets','20160628', date_type=1)

     # 获取股票池中对应上市公司发布日期在2016年6月28日之前，年度(即2015年年报)
     # 资产负债表中资产总计(total_assets)数据，如果到查询日期为止还未发布则所有数据用Nan填充
     get_fundamentals(stocks, 'balance_statement', 'total_assets', '20160628', report_types='4')

     # 获取股票池中对应上市公司2016年6月28日最近季度资产负债表中对应fields字段数据
     fields =['sold_buyback_secu_proceeds','specific_account_payable']
     get_fundamentals(stocks, 'balance_statement', fields,'20160628',)

     # 获取股票池中对应上市公司2016年6月28日最近季度资产负债表中对应fields字段最新数据，
     # 如果最近更新日期(发布日期)在2016年6月28日之后则无法获取对应数据
     fields =['sold_buyback_secu_proceeds','specific_account_payable']
     get_fundamentals(stocks, 'balance_statement', fields,'20160628',merge_type=1)

     # 2. 按年份查询模式：返回输入年份范围内对应季度的财务数据
     # 获取公司浦发银行(600000.SS)从2013年至2015年第一季度资产负债表中资产总计(total_assets)数据
     get_fundamentals('600000.SS','balance_statement','total_assets',start_year='2013',end_year='2015', report_types='1')

     # 获取股票池中对应上市公司从2013年至2015年年度资产负债表中对应fields字段数据
     fields =['sold_buyback_secu_proceeds','specific_account_payable']
     get_fundamentals(stocks,'balance_statement',fields,start_year='2013',end_year='2015', report_types='4')
get_Ashares - 获取指定日期A股代码列表
get_Ashares(date=None)
使用场景
该函数在研究、回测、交易模块可用

接口说明
该接口用于获取指定日期沪深市场的所有A股代码列表

注意事项：

在回测中，date不入参默认取回测日期，默认值会随着回测日期变化而变化，等于context.blotter.current_dt。
在研究中，date不入参默认取当天日期。
在交易中，date不入参默认取当天日期。
参数
date：格式为YYYYmmdd

返回
股票代码列表，list类型(list[str,...])

['000001.SZ', '000002.SZ', '000004.SZ', '000005.SZ', '000006.SZ', '000007.SZ', '000008.SZ', '000009.SZ', '000010.SZ', '000011.SZ', '000012.SZ', '000014.SZ', '000016.SZ', '000017.SZ', '000018.SZ', '000019.SZ',
 '000020.SZ', '000021.SZ', '000023.SZ', '000024.SZ', '000025.SZ', '000026.SZ', '000027.SZ',..., '603128.SS', '603167.SS', '603333.SS', '603366.SS', '603399.SS', '603766.SS', '603993.SS'] 
示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def handle_data(context, data):
    #沪深A股代码
    ashares = get_Ashares()
    log.info('%s A股数量为%s' % (context.blotter.current_dt,len(ashares)))
    ashares = get_Ashares('20130512')
    log.info('20130512 A股数量为%s'%len(ashares))
get_etf_list - 获取ETF代码
get_etf_list()
使用场景
该函数仅支持PTrade客户端可用、仅在股票交易模块可用，对接jz_ufx、ATP、云订柜台不支持该函数

接口说明
该接口用于获取柜台返回的ETF代码列表

注意事项：

无

返回
正常返回一个list类型对象，包含所有ETF代码。异常返回空list，如[](list[str,...])。

['510010.SS', '510020.SS', '510030.SS', '510050.SS', '510060.SS', '510180.SS', '510300.SS', '510310.SS', '510330.SS', '511800.SS', '511810.SS', '511820.SS', '511830.SS', '511880.SS', '511990.SS', '512010.SS',
 '512510.SS', '159001.SZ', '159003.SZ', '159005.SZ', '159901.SZ', '159903.SZ', '159905.SZ', '159906.SZ', '159909.SZ', '159910.SZ', '159919.SZ', '159923.SZ', '159923.SZ', '159924.SZ', '159925.SZ', '159927.SZ',
 '159928.SZ', '159929.SZ']
示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def handle_data(context, data):
    #ETF代码列表
    etf_code_list = get_etf_list()
    log.info('ETF列表为%s' % etf_code_list)
get_etf_info - 获取ETF信息
get_etf_info(etf_code)
使用场景
该函数仅支持PTrade客户端可用、仅在股票交易模块可用，对接jz_ufx、ATP、云订柜台不支持该函数

接口说明
该接口用于获取单支或者多支ETF的信息。

注意事项：

无

参数
etf_code : 单支ETF代码或者一个ETF代码的list，必传参数(list[str]/str)

返回
正常返回一个dict类型字段，包含每只ETF信息，key为ETF代码，values为包含etf信息的dict。异常返回空dict，如{}(dict[str:dict[...]])

返回结果字段介绍：

etf_redemption_code -- 申赎代码(str:str)；
publish -- 是否需要发布IOPV(str:int)；
report_unit -- 最小申购、赎回单位(str:int)；
cash_balance -- 现金差额(str:float)；
max_cash_ratio -- 现金替代比例上限(str:float)；
pre_cash_component -- T-1日申购基准单位现金余额(str:float)；
nav_percu -- T-1日申购基准单位净值(str:float)；
nav_pre -- T-1日基金单位净值(str:float)；
allot_max -- 申购上限(str:float)；
redeem_max -- 赎回上限(str:float)；
字段备注:

publish -- 是否需要发布IOPV，1是需要发布，0是不需要发布；
返回如下:

{'510020.SS': {'nav_percu': 206601.39, 'redeem_max': 0.0, 'nav_pre': 0.207, 'report_unit': 1000000, 'max_cash_ratio': 0.4,
                'cash_balance': -813.75, 'etf_redemption_code': '510021', 'pre_cash_component': 598.39, 'allot_max': 0.0, 'publish': 1}}
示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def handle_data(context, data):
    #ETF信息
    etf_info = get_etf_info('510020.SS')
    log.info(etf_info)
    etfs_info = get_etf_info(['510020.SS','510050.SS'])
    log.info(etfs_info)
get_etf_stock_list - 获取ETF成分券列表
get_etf_stock_list(etf_code)
使用场景
该函数仅支持PTrade客户端可用、仅在股票交易模块可用，对接jz_ufx、ATP、云订柜台不支持该函数

接口说明
该接口用于获取目标ETF的成分券列表

注意事项：

无

参数
etf_code : 单支ETF代码，必传参数(str)

返回
正常返回一个list类型字段，包含每只etf代码所对应的成分股。异常返回空list，如[](list[str,...])

['600000.SS', '600010.SS', '600016.SS'] 
示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def before_trading_start(context, data):
    #ETF成分券列表
    stock_list = get_etf_stock_list('510020.SS')
    log.info(stock_list)

def handle_data(context, data):
    pass
get_etf_stock_info - 获取ETF成分券信息
get_etf_stock_info(etf_code,security)
使用场景
该函数仅支持PTrade客户端可用、仅在股票交易模块可用，对接jz_ufx、ATP、云订柜台不支持该函数

接口说明
该接口用于获取ETF成分券信息。

注意事项：

无

参数
etf_code : 单支ETF代码，必传参数(str)

security : 单只股票代码或者一个由多只股票代码组成的列表，必传参数(list[str]/str)

返回
正常返回一个dict类型字段，包含每只etf代码中成分股的信息。异常返回空dict，如{}(dict[str:dict[...]])

返回结果字段介绍：

code_num -- 成分券数量(str:float)；
cash_replace_flag -- 现金替代标志(str:str)；
replace_ratio -- 保证金率(溢价比率)，允许现金替代标的此字段有效(str:float)；
replace_balance -- 替代金额,必须现金替代标的此字段有效(str:float)；
is_open -- 停牌标志，0-停牌，1-非停牌(str:int)；
返回如下:

{'600000.SS': {'cash_replace_flag': '1', 'replace_ratio': 0.1, 'is_open': 1, 'code_num': 4700.0, 'replace_balance': 0.0}}
示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def handle_data(context, data):
    #ETF成分券信息
    stock_info = get_etf_stock_info('510050.SS','600000.SS')
    log.info(stock_info)
    stocks_info = get_etf_stock_info('510050.SS',['600000.SS','600036.SS'])
    log.info(stocks_info)
get_ipo_stocks - 获取当日IPO申购标的
get_ipo_stocks()
使用场景
该函数仅支持Ptrade客户端可用、仅在股票交易模块可用，对接jz_ufx不支持该函数

接口说明
该接口用于获取当日IPO申购标的信息

注意事项：

无

返回
正常返回一个dict类型对象，key为各个分类市场，value为市场对应的申购代码列表。异常返回空dict，如{}({str:[],str:[],...})。分类市场明细如下：

上证普通代码；
上证科创板代码；
深证普通代码；
深证创业板代码；
可转债代码；
{'深证普通代码': ['002952.SZ', '072318.SZ'], '深证创业板代码': ['300765.SZ'], '上证普通代码': ['732116.SS', '732136.SS', '732367.SS', '732378.SS', '732380.SS', '732616.SS', '780086.SS', '780211.SS', '780860.SS', '718001.SS', '783012.SS', '783127.SS'], '可转债代码': ['718001.SS', '783012.SS', '783127.SS', '072318.SZ'], '上证科创板代码': ['787006.SS']}
示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def handle_data(context, data):
    # 当日可转债IPO申购标的
    ipo_stocks = get_ipo_stocks().get('可转债代码')
    log.info('可转债IPO申购标的列表为%s' % ipo_stocks)
get_cb_list-获取可转债市场代码表
get_cb_list()
使用场景
该函数仅在交易模块可用

接口说明
返回当前可转债市场的所有代码列表(包含停牌代码)。

注意事项：

为减小对行情服务压力，该函数在交易模块中同一分钟内多次调用返回当前分钟首次查询的缓存数据。
参数
无

返回
返回当前可转债市场的所有代码列表(包含停牌代码)(list)。失败则返回空列表[]。

示例
def initialize(context):
    g.security = "600570.SS"
    set_universe(g.security)
    run_daily(context, get_trade_cb_list, "9:25")


def before_trading_start(context, data):
    # 每日清空，避免取到昨日市场代码表
    g.trade_cb_list = []


def handle_data(context, data):
    pass


# 获取当天可交易的可转债代码列表
def get_trade_cb_list(context):
    cb_list = get_cb_list()
    cb_snapshot = get_snapshot(cb_list)
    # 代码有行情快照并且交易状态不在暂停交易、停盘、长期停盘、退市状态的判定为可交易代码
    g.trade_cb_list = [cb_code for cb_code in cb_list if
                       cb_snapshot.get(cb_code, {}).get("trade_status") not in
                       [None, "HALT", "SUSP", "STOPT", "DELISTED"]]
    log.info("当天可交易的可转债代码列表为：%s" % g.trade_cb_list)
get_cb_info - 获取可转债基础信息
get_cb_info()
使用场景
该函数仅在研究、交易模块可用

接口说明
获取可转债基础信息。

注意事项：

获取失败时返回空DataFrame。
此API依靠可转债基础数据权限，使用前请与券商确认是否有此权限，无权限时调用返回空DataFrame。
参数
无

返回
正常返回一个DataFrame类型数据，包含每只可转债的信息

包含以下信息：

bond_code:可转债代码(str)；
bond_name:可转债名称(str)；
stock_code:股票代码(str)；
stock_name:股票名称(str)；
list_date:上市日期(str)；
premium_rate:溢价率(float)；
convert_date:转股起始日(str)；
maturity_date:到期日(str)；
convert_rate:转股比例(float)；
convert_price:转股价格(float)；
convert_value:转股价值(float)；
示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def handle_data(context, data):
    df = get_cb_info()
    log.info(df)
get_reits_list - 获取基础设施公募REITs基金代码列表
get_reits_list(date=None)
使用场景
该函数在研究、回测、交易模块可用

接口说明
该接口用于获取指定日期沪深市场的所有公募REITs基金代码列表

注意事项：

在回测中，date不入参默认取回测日期，默认值会随着回测日期变化而变化，等于context.blotter.current_dt。
在研究中，date不入参默认取当天日期。
在交易中，date不入参默认取当天日期。
参数
date：格式为YYYYmmdd

返回
公募REITs基金代码列表，list类型(list[str,...])

['180101.SZ', '180102.SZ', '180103.SZ', '180201.SZ', '180202.SZ', '180301.SZ', '180401.SZ', '180501.SZ', '180801.SZ', '508000.SS', '508001.SS', '508006.SS', '508008.SS', '508009.SS', '508018.SS', '508021.SS',
'508027.SS', '508028.SS', '508056.SS', '508058.SS', '508066.SS', '508068.SS', '508077.SS', '508088.SS', '508096.SS', '508098.SS', '508099.SS'] 
示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def handle_data(context, data):
    # 公募REITs基金代码
    ashares = get_reits_list()
    log.info('%s 公募REITs基金数量为%s' % (context.blotter.current_dt,len(ashares)))
    ashares = get_reits_list('20230403')
    log.info('20230403 公募REITs基金数量为%s'%len(ashares))
获取其他信息
get_position - 获取单只标的持仓信息
get_position(security)
使用场景
该函数仅在回测、交易模块可用

接口说明
该接口用于获取某个标的持仓信息详情。

注意事项：

无

参数
security：标的代码，如'600570.SS'。

支持品种：

股票
ETF
LOF
期货
返回
返回一个Position对象(Position)。

<Position {'business_type': 'stock', 'short_amount': 0, 'contract_multiplier': 1, 'short_pnl': 0, 'delivery_date': None, 'today_short_amount': 0, 'last_sale_price': 118.7, 'sid': '600570.SS',
'enable_amount': 100, 'margin_rate': 1, 'amount': 200, 'long_amount': 0, 'short_cost_basis': 0, 'today_long_amount': 0, 'cost_basis': 117.9, 'long_pnl': 0, 'long_cost_basis': 0}>
示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def handle_data(context, data):
    position = get_position(g.security)
    log.info(position)
get_positions - 获取多只标的持仓信息
get_positions(security)
使用场景
该函数仅在回测、交易模块可用

接口说明
该接口用于获取多个标的的持仓信息详情。

注意事项：

无

参数
security：标的代码，可以是一个列表，不传时默认为获取所有持仓(list[str]/str)；

支持品种：

股票
ETF
LOF
期货
返回
返回一个数据字典，键为股票代码，值为Position对象(dict[str:Position])，如下：

注意：四位尾缀或者两位尾缀代码皆可作为键取到返回的数据字典值，如'600570.XSHG'或者'600570.SS'。

{'600570.XSHG': <Position {'business_type': 'stock', 'short_amount': 0, 'contract_multiplier': 1, 'short_pnl': 0, 'delivery_date': None, 'today_short_amount': 0, 'last_sale_price': 118.7, 'sid': '600570.SS',
'enable_amount': 100, 'margin_rate': 1, 'amount': 200, 'long_amount': 0, 'short_cost_basis': 0, 'today_long_amount': 0, 'cost_basis': 117.9, 'long_pnl': 0, 'long_cost_basis': 0}>}
示例
def initialize(context):
    g.security = ['600570.SS','600000.SS']
    set_universe(g.security)

def handle_data(context, data):
    log.info(get_positions('600570.SS'))
    log.info(get_positions(g.security))
    log.info(get_positions())
get_all_positions - 获取全部持仓信息
get_all_positions()
使用场景
该函数仅在交易模块可用

接口说明
该接口用于获取当前账户的持仓信息详情。

注意事项：

因不同柜台返回的字段存在差异，当该接口返回的字段不在返回字段描述中时请咨询券商人员。
不同柜台返回的字段值类型不一致，比如不同柜台返回的enable_amount类型有可能为str/float/int，需要策略中对此做兼容。
该接口返回当前账户所有的持仓信息，包含国债逆回购产生的新标准券、打新中签尚未上市等量化不支持标的的持仓。
为减小对柜台压力，该函数返回的是缓存的账户定时同步持仓查询数据。
参数
无。

返回
返回一个列表，包含不同标的字典类型的持仓信息。不同交易类型返回不同字段的持仓信息。

[{'position_str': '0111900000000001926516100010000000000A027483621600010', 'fund_account': '19265161', 'exchange_type': '1', 'stock_account': 'A027483621', 'stock_code': '600010', 'stock_name': '包钢股份', 'stock_type': '0', 'current_amount': 8300.0, 'enable_amount': 0.0, 'last_price': 1.86, 'cost_price': 1.862, 'keep_cost_price': 1.862, 'income_balance': -18.22, 'hand_flag': '0', 'market_value': 15438.0, 'av_buy_price': 0.0, 'av_income_balance': 0.0, 'client_id': '19265161', 'cost_balance': 15443.25, 'hold_amount': 0.0, 'uncome_buy_amount': 0.0, 'uncome_sell_amount': 0.0, 'entrust_sell_amount': 0.0, 'real_buy_amount': 8300.0, 'real_sell_amount': 0.0, 'asset_price': 1.86, 'delist_flag': '0', 'delist_date': 0, 'par_value': 1.0, 'income_balance_nofare': -5.25, 'frozen_amount': 0.0, 'profit_ratio': -0.11, 'sub_stock_type': '!', 'stbtrans_type': ' ', 'stb_layer_flag': ' ', 'av_cost_price': 1.861, 'income_flag': ' ', 'real_sell_balance': 0.0, 'real_buy_balance': 15443.25, 'sum_buy_amount': 0.0, 'sum_buy_balance': 0.0, 'sum_sell_amount': 0.0, 'sum_sell_balance': 0.0, 'correct_amount': 0.0, 'stbtrans_flag': ' ', 'stock_name_long': '包钢股份', 'pre_dr_price': 1.86, 'close_price': 1.86, 'hold_cost_price': 1.861, 'comb_hold_flag': '0', 'store_unit': 1},]
                            
股票
    exchange_type  交易类别
    stock_code  证券代码
    stock_name  证券名称
    stock_type  证券类别
    hold_amount  持有数量
    current_amount  当前数量
    enable_amount  可用数量
    real_buy_amount  回报买入数量
    real_sell_amount  回报卖出数量
    uncome_buy_amount  未回买入数量
    uncome_sell_amount  未回卖出数量
    entrust_sell_amount  委托卖出数量
    last_price  最新价
    cost_price  成本价
    keep_cost_price  保本价
    income_balance  盈亏金额
    market_value  证券市值
    av_buy_price  买入均价
    av_income_balance  实现盈亏
    cost_balance  持仓成本
    delist_flag  退市标志
    delist_date  退市日期
    income_balance_nofare  无费用盈亏
    frozen_amount  冻结数量
    profit_ratio  盈亏比例(%)
    asset_price  市值价
    av_cost_price  摊薄成本价
融资融券
    exchange_type  交易类别
    stock_code  证券代码
    stock_name  证券名称
    current_amount  当前数量
    hold_amount  持有数量
    enable_amount  可用数量
    last_price  最新价
    cost_price  成本价
    income_balance  盈亏金额
    income_balance_nofare  无费用盈亏
    market_value  证券市值
    av_buy_price  买入均价
    av_income_balance  实现盈亏
    cost_balance  持仓成本
    uncome_buy_amount  未回买入数量
    uncome_sell_amount  未回卖出数量
    entrust_sell_amount  委托卖出数量
    real_buy_amount  回报买入数量
    real_sell_amount  回报卖出数量
    asset_price  市值价
    assure_ratio  担保折算率
    profit_ratio  盈亏比例(%)
    sum_buy_amount  累计买入数量
    sum_buy_balance  累计买入金额
    sum_sell_amount  累计卖出数量
    sum_sell_balance  累计卖出金额
    real_buy_balance  回报买入金额
    real_sell_balance  回报卖出金额
    av_cost_price  摊薄成本价
期货
    futu_exch_type  交易类别
    futu_code  合约代码
    entrust_bs  委托方向
    begin_amount  期初数量
    enable_amount  可用数量
    real_enable_amount  当日开仓可用数量
    hold_income_float  持仓浮动盈亏
    hold_income  期货盯市盈亏
    hold_margin  持仓保证金
    average_price  平均价
    average_hold_price  持仓均价
    tas_average_hold_price  TAS持仓均价
    futu_last_price  最新价格
    hedge_type  投机/套保类型
    real_amount  成交数量
    real_open_balance  回报开仓金额
    old_open_balance  老仓持仓成交额
    real_current_amount  今总持仓
    old_current_amount  老仓持仓数量
    tas_current_amount  TAS持仓数量
    combinable_amount  可组合持仓数量
字段备注
delist_date：默认为0。
示例
def initialize(context):
    g.security = "600570.SS"
    set_universe(g.security)

def before_trading_start(context, data):
    g.flag = False

def handle_data(context, data):
    if not g.flag:
        # 打印当前账户全部持仓
        log.info(get_all_positions())
        g.flag = True
get_trades_file - 获取对账数据文件
get_trades_file(save_path='')
使用场景
该函数仅在回测模块可用

接口说明
该接口用于获取对账数据文件

注意事项：

文件目录的命名需要遵守如下规则：
长度不能超过256个字符。
名称中不能出下如下字符：:?,@#$&();\"\'<>`~!%^*
参数
save_path：导出对账数据存储的路径， 默认在notebook的根目录下(str)；

返回
成功返回导出文件的路径(str)，失败返回None(NoneType)；

导出数据格式的说明:
交易数据文件的组织格式为csv文件，表头信息为：
订单编号，成交编号，委托编号，标的代码，交易类型，成交数量，成交价，成交金额，交易费用，交易时间，对应的表头字段为：
[order_id,trading_id,entrust_id,security_code,order_type,volume,price,total_money,trading_fee, trade_time]
注意：

order_id列中可能出现如下几种取值：

1、M000000，通过外部系统委托的成交数据；

2、类似a6fbc145958843cc86639b23fbcfdc4c的字符串，通过平台委托的成交数据；

3、H000000，引入对账数据接口前的版本产生的交易数据；

示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def handle_data(context, data):
    # 委托
    order_obj = order(g.security, 100)
    log.info('订单编号为：%s'% order_obj)

def after_trading_end(context, data):
    # 获取对账数据，存放到默认目录
    data_path = get_trades_file()
    log.info(data_path)

    # 获取对账数据，存放到notebook下的指定目录
    user_data_path = get_trades_file('user_data/data')
    log.info(user_data_path)
convert_position_from_csv - 获取设置底仓的参数列表(股票)
convert_position_from_csv(path)
使用场景
该函数仅在回测模块可用

接口说明
该接口用于从csv文件中获取设置底仓的参数列表

注意事项：

文件目录的命名需要遵守如下规则：
长度不能超过256个字符。
名称中不能出下如下字符：:?,@#$&();\"\'<>`~!%^*
参数
path: csv文件对应路径及文件名(需要在研究中上传该文件)(str)；

csv文件内容格式要求如下:

sid,enable_amount,amount,cost_basis
600570.SS,10000,10000,45
sid: 标的代码(str)；
amount: 持仓数量(str)；
enable_amount: 可用数量(str)；
cost_basis: 每股的持仓成本价格(str)：
返回
用于设置底仓的参数列表，该list中是字典类型的元素；

返回一个list，该list中是一个字典类型的元素(list[dict[str:str],...])，如：

[{
    'sid':标的代码,
    'amount':持仓数量,
    'enable_amount':可用数量,
    'cost_basis':每股的持仓成本价格,
}]
示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)
    # 设置底仓
    poslist= convert_position_from_csv("Poslist.csv")
    set_yesterday_position(poslist)

def handle_data(context, data):
    # 卖出100股
    order(g.security, -100)
get_user_name - 获取登录终端的资金账号
get_user_name(login_account=True)
使用场景
该函数仅在回测、交易模块可用

接口说明
该接口用于获取登录终端的账号

注意事项：

回测中无论是否传入login_account参数均返回登录终端的资金账号。
交易中login_account参数不传或传入True时返回登录终端的资金账号。
交易中login_account参数传入False时返回当前策略绑定账号，如两融交易返回对应信用账号。
参数
login_account(bool)：默认返回登录终端的资金账号，交易中传入False时返回当前策略绑定账号；

返回
返回登录终端的资金账号/当前策略绑定账号(str)或者None。如果查询成功返回登录终端的资金账号/当前交易策略绑定账号(str)，失败则返回None(NoneType)。

示例
def initialize(context):
    g.security = "600570.SS"
    set_universe(g.security)
    g.current_id = get_user_name(False)

def before_trading_start(context, data):
    g.flag = False

def handle_data(context, data):
    # 账号为234567890且当日未委托过，担保品买卖100股
    if g.current_id == "234567890" and not g.flag:
        margin_trade(g.security, 100)
        g.flag = True
get_deliver - 获取历史交割单信息
get_deliver(start_date, end_date)
使用场景
该函数仅在交易模块使用；仅支持before_trading_start和after_trading_end阶段调用，对接ATP柜台不支持该函数

接口说明
该接口用来获取账户历史交割单信息。

注意事项：

开始日期start_date和结束日期end_date为必传字段。
仅支持查询上一个交易日(包含)之前的交割单信息。
因不同柜台返回的字段存在差异，因此接口返回的为柜台原数据，使用时请根据实际柜台信息做字段解析。
该接口仅支持查询普通股票账户(非两融)。
参数
start_date: 开始日期，输入形式仅支持"YYYYmmdd"，如'20170620'；

end_date: 结束日期，输入形式仅支持"YYYYmmdd"，如'20170620'；

返回
返回一个list类型对象(list[dict,...])，包含一个或N个dict，每个dict为一条交割单信息，其中包含柜台返回的字段信息，失败则返回[]。

[{'entrust_way': '7', 'exchange_fare': 0.04, 'post_balance': 3539128.83, 'stock_account': '0010110920', 'exchange_farex': 0.0, 'fare0': 0.5, 'report_milltime': 110400187, 'business_balance': 2987.0, 'exchange_fare5': 0.0, 'fare_remark': '内部:.5( | ,费用类别:9999)', 'client_id': '10110920', 'uncome_flag': '0', 'exchange_fare0': 0.03, 'exchange_fare2': 0.0, 'fare1': 0.0, 'init_date': 20210811, 'stock_code': '162605', 'occur_amount': 1000.0, 'report_time': 110400, 'entrust_bs': '1', 'seat_no': '123456', 'business_id': '0110351000000242', 'business_amount': 1000.0, 'business_time': 110351, 'fund_account': '10110920', 'begin_issueno': ' ', 'post_amount': 1000.0, 'correct_amount': 0.0, 'money_type': '0', 'client_name': '客户10110920', 'business_type': '0', 'business_flag': 4002, 'clear_balance': -2987.5, 'exchange_fare1': 0.0, 'date_back': 20210811, 'branch_no': 1011, 'serial_no': 153, 'occur_balance': -2987.5, 'stock_name': '景顺鼎益', 'curr_time': 173028, 'exchange_fare4': 0.0, 'brokerage': 0.0, 'business_name': '证券买入', 'order_id': 'F04Z', 'business_times': 1, 'entrust_date': 20210811, 'remark': '证券买入;uft节点:31;', 'exchange_fare6': 0.0, 'standard_fare0': 0.5, 'exchange_fare3': 0.01, 'farex': 0.0, 'clear_fare0': 0.46, 'entrust_no': '38', 'profit': 0.0, 'exchange_type': '2', 'fare2': 0.0, 'business_no': 181, 'stock_type': 'L', 'fare3': 0.0, 'business_status': '0', 'business_price': 2.987, 'position_str': '020210811010110000000153', 'stock_name_long': '景顺鼎益LOF', 'report_no': '38', 'correct_balance': 0.0, 'exchange_rate': 0.0}] 
示例
def initialize(context):
    g.security = "600570.SS"
    set_universe(g.security)

def before_trading_start(context, data):
    h = get_deliver('20210101', '20211117')
    log.info(h)

def handle_data(context, data):
    pass
get_fundjour - 获取历史资金流水信息
get_fundjour(start_date, end_date)
使用场景
该函数仅在交易模块使用；仅支持before_trading_start和after_trading_end阶段调用，对接jz_ufx、ATP、云订柜台不支持该函数

接口说明
该接口用来获取账户历史资金流水信息。

注意事项：

开始日期start_date和结束日期end_date为必传字段。
仅支持查询上一个交易日(包含)之前的资金流水信息。
因不同柜台返回的字段存在差异，因此接口返回的为柜台原数据，使用时请根据实际柜台信息做字段解析。
该接口仅支持查询普通股票账户(非两融)。
参数
start_date: 开始日期，输入形式仅支持"YYYYmmdd"，如'20170620'；

end_date: 结束日期，输入形式仅支持"YYYYmmdd"，如'20170620'；

返回
返回一个list类型对象(list[dict,...])，包含一个或N个dict，每个dict为一条资金流水，其中包含柜台返回的字段信息，失败则返回[]。

[{'post_balance': 3260341.36, 'init_date': 20210104, 'asset_prop': '0', 'serial_no': 1, 'business_flag': 4002, 'occur_balance': -10598.21, 'exchange_type': '0', 'stock_name': ' ', 'business_date': 20210104, 'business_price': 0.0, 'bank_no': '0', 'occur_amount': 0.0, 'remark': '证券买入,恒生电子,100股,价格105.93', 'stock_account': ' ', 'money_type': '0', 'fund_account': '10110920', 'position_str': '20210104010110000000001', 'bank_name': '内部银行', 'business_name': '证券买入', 'stock_code': ' ', 'curr_date': 20210104, 'entrust_bs': ' ', 'business_time': 171730}] 
示例
def initialize(context):
    g.security = "600570.SS"
    set_universe(g.security)

def before_trading_start(context, data):
    h = get_fundjour('20210101', '20211117')
    log.info(h)

def handle_data(context, data):
    pass
get_research_path - 获取研究路径
get_research_path()
使用场景
该函数可在回测、交易模块使用

接口说明
该接口用于获取研究界面根目录路径。

注意事项：

无

参数
无

返回
返回一个字符串类型对象(str)

示例
def initialize(context):
    g.security = "600570.SS"
    set_universe(g.security)
    path = get_research_path()

def handle_data(context, data):
    pass
get_trade_name - 获取交易名称
get_trade_name()
使用场景
该函数仅在交易模块使用

接口说明
该接口用于获取当前交易的名称。

注意事项：

当获取失败时，返回空字符串。
参数
无

返回
当前交易名称(str)。

示例
def initialize(context):
    g.security = "600570.SS"
    set_universe(g.security)

def handle_data(context, data):
    name = get_trade_name()
get_lucky_info - 获取历史中签信息
get_lucky_info(start_date, end_date)
使用场景
该函数仅在交易模块使用，对接jz_ufx不支持该函数

接口说明
该接口用于获取指定时间范围内的中签信息。

注意事项：

为减小对柜台压力，该函数在股票交易模块中同一分钟内多次调用返回当前分钟首次查询的缓存数据。
参数
start_date：开始日期(str)，输入形式仅支持"YYYYmmdd"，如"20220928"。

end_date：结束日期(str)，输入形式仅支持"YYYYmmdd"，如"20220929"。

返回
正常返回一个列表套字典数据，异常或无中签信息时返回一个空列表。

返回的数据格式如下：

[{'stock_code': 证券代码(str), 'occur_amount': 发生数量(float), 'business_price': 成交价格(float), 'stock_name': 证券名称(str), 'init_date': 交易日期(int)}, ...]

[{'stock_code': '371002.SZ', 'occur_amount': 10.0, 'business_price': 100.0, 'stock_name': '崧盛发债', 'init_date': 20220928}, ...]

示例
def initialize(context):
    # 初始化策略
    g.security = "600570.SS"
    set_universe(g.security)

def before_trading_start(context, data):
    pre_date = str(get_trading_day(-1)).replace("-", "")
    current_date = context.blotter.current_dt.strftime("%Y%m%d")
    # 获取上一交易日至今天中签信息
    lucky_info = get_lucky_info(pre_date, current_date)
    log.info(lucky_info)

def handle_data(context, data):
    pass
交易相关函数
注意：代码精度位为3位小数的类型(后台已保护为3位)，如ETF、国债；代码精度为2位小数类型，需要在传参时限制价格参数的精度，如股票。

股票交易函数
order-按数量买卖
order(security, amount, limit_price=None)
使用场景
该函数仅在回测、交易模块可用

接口说明
该接口用于买卖指定数量为amount的股票，同时支持国债逆回购

注意事项：

支持交易场景的逆回购交易。委托方向为卖出(amount必须为负数)，逆回购最小申购金额为1000元(10张)，因此本接口amount入参应大于等于10(10张)，否则会导致委托失败。
回测场景，amount有最小下单数量校验，股票、ETF、LOF：100股，可转债：10张；交易场景接口不做amount校验，直接报柜台。
交易场景如果limit_price字段不入参，系统会默认用行情快照数据最新价报单，假如行情快照获取失败会导致委托失败，系统会在日志中增加提醒。
由于下述原因，回测中实际买入或者卖出的股票数量有时候可能与委托设置的不一样，针对上述内容调整，系统会在日志中增加警告信息：
根据委托买入数量与价格经计算后的资金数量，大于当前可用资金。
委托卖出数量大于当前可用持仓数量。
每次交易股票时取整100股，交易可转债时取整10张，但是卖出所有股票时不受此限制。
股票停牌、股票未上市或者退市、股票不存在。
回测中每天结束时会取消所有未完成交易。
参数
security: 股票代码(str)；

amount: 交易数量，正数表示买入，负数表示卖出(int)；

limit_price：买卖限价(float)；

返回
Order对象中的id或者None。如果创建订单成功，则返回Order对象的id(str)，失败则返回None(NoneType)。

示例
def initialize(context):
    g.security = ['600570.SS', '000001.SZ']
    set_universe(g.security)

def handle_data(context, data):
    #以系统最新价委托
    order('600570.SS', 100)
    # 逆回购1000元
    order('131810.SZ', -10)
    #以39块价格下一个限价单
    order('600570.SS', 100, limit_price=39)
order_target - 指定目标数量买卖
order_target(security, amount, limit_price=None)
使用场景
该函数仅在回测、交易模块可用

接口说明
该接口用于买卖股票，直到股票最终数量达到指定的amount

注意事项：

该函数不支持逆回购交易。
该函数在委托股票时取整100股，委托可转债时取整10张。
交易场景如果limit_price字段不入参，系统会默认用行情快照数据最新价报单，假如行情快照获取失败会导致委托失败，系统会在日志中增加提醒。
该接口的使用有场景限制，回测可以正常使用，交易谨慎使用。回测场景下撮合是引擎计算的，因此成交之后持仓信息的更新是瞬时的，但交易场景下信息的更新依赖于柜台数据的返回，无法做到瞬时同步，可能造成重复下单。具体原因如下：
柜台返回持仓数据体现当日变化(由柜台配置决定)：交易场景中持仓信息同步有时滞，一般在6秒左右，假如在这6秒之内连续下单两笔或更多order_target委托，由于持仓数量不会瞬时更新，会造成重复下单。
柜台返回持仓数据体现当日变化(由柜台配置决定)：第一笔委托未完全成交，如果不对第一笔做撤单再次order_target相同的委托目标数量，引擎不会计算包括在途的总委托数量，也会造成重复下单。
柜台返回持仓数据不体现当日变化(由柜台配置决定)：这种情况下持仓数量只会一天同步一次，必然会造成重复下单。
针对以上几种情况，假如要在交易场景使用该接口，首先要确定券商柜台的配置，是否实时更新持仓情况，其次需要增加订单和持仓同步的管理，来配合order_target使用。
参数
security: 股票代码(str)；

amount: 期望的最终数量(int)；

limit_price：买卖限价(float)；

返回
Order对象中的id或者None。如果创建订单成功，则返回Order对象的id(str)，失败则返回None(NoneType)。

示例
def initialize(context):
    g.security = ['600570.SS', '000001.SZ']
    set_universe(g.security)

def handle_data(context, data):
    #买卖恒生电子股票数量到100股
    order_target('600570.SS', 100)
    #卖出恒生电子所有股票
    if data['600570.SS']['close'] > 39:
        order_target('600570.SS', 0)
order_value - 指定目标价值买卖
order_value(security, value, limit_price=None)
使用场景
该函数仅在回测、交易模块可用

接口说明
该接口用于买卖指定价值为value的股票

注意事项：

该函数不支持逆回购交易。
该函数在委托股票时取整100股，委托可转债时取整10张。
交易场景如果limit_price字段不入参，系统会默认用行情快照数据最新价报单，假如行情快照获取失败会导致委托失败，系统会在日志中增加提醒。
参数
security：股票代码(str)；

value：股票价值(float)

limit_price：买卖限价(float)

返回
Order对象中的id或者None。如果创建订单成功，则返回Order对象的id(str)，失败则返回None(NoneType)。

示例
def initialize(context):
    g.security = ['600570.SS', '000001.SZ']
    set_universe(g.security)

def handle_data(context, data):
    #买入价值为10000元的恒生电子股票
    order_value('600570.SS', 10000)

    if data['600570.SS']['close'] > 39:
        #卖出价值为10000元的恒生电子股票
        order_value('600570.SS', -10000)
order_target_value - 指定持仓市值买卖
order_target_value(security, value, limit_price=None)
使用场景
该函数仅在回测、交易模块可用

接口说明
该接口用于调整股票持仓市值到value价值

注意事项：

该函数不支持逆回购交易。
该函数在委托股票时取整100股，委托可转债时取整10张。
交易场景如果limit_price字段不入参，系统会默认用行情快照数据最新价报单，假如行情快照获取失败会导致委托失败， 系统会在日志中增加提醒。
该接口的使用有场景限制，回测可以正常使用，交易谨慎使用。回测场景下撮合是引擎计算的，因此成交之后持仓信息的更新是瞬时的，但交易场景下信息的更新依赖于柜台数据的返回，无法做到瞬时同步，可能造成重复下单。具体原因如下：
柜台返回持仓数据体现当日变化(由柜台配置决定)：交易场景中持仓信息同步有时滞，一般在6秒左右，假如在这6秒之内连续下单两笔或更多order_target_value委托，由于持仓市值不会瞬时更新，会造成重复下单。
柜台返回持仓数据体现当日变化(由柜台配置决定)：第一笔委托未完全成交，如果不对第一笔做撤单再次order_target_value相同的委托目标金额，引擎不会计算包括在途的总委托数量，也会造成重复下单。
柜台返回持仓数据不体现当日变化(由柜台配置决定)：这种情况下持仓金额只会一天同步一次，必然会造成重复下单。
针对以上几种情况，假如要在交易场景使用该接口，首先要确定券商柜台的配置，是否实时更新持仓情况，其次需要增加订单和持仓同步的管理，来配合order_target_value使用。

参数
security: 股票代码(str)；

value: 期望的股票最终价值(float)；

limit_price：买卖限价(float)；

返回
Order对象中的id或者None。如果创建订单成功，则返回Order对象的id(str)，失败则返回None(NoneType)。

示例
def initialize(context):
    g.security = ['600570.SS', '000001.SZ']
    set_universe(g.security)

def handle_data(context, data):
    #买卖股票到指定价值
    order_target_value('600570.SS', 10000)

    #卖出当前所有恒生电子的股票
    if data['600570.SS']['close'] > 39:
        order_target_value('600570.SS', 0)
order_market - 按市价进行委托
order_market(security, amount, market_type, limit_price=None)
使用场景
该函数仅在交易模块可用

接口说明
该接口用于使用多种市价类型进行委托

注意事项：

支持逆回购交易。委托方向为卖出(amount必须为负数)，逆回购最小申购金额为1000元(10张)，因此本接口amount入参应大于等于10(10张)，否则会导致委托失败。
不支持可转债交易。
该函数中market_type是必传字段，如不传入参数会出现报错。
该函数委托上证股票时limit_price是必传字段，如不传入参数会出现报错。
参数
security：股票代码(str)；

amount：交易数量(int)，正数表示买入，负数表示卖出；

market_type：市价委托类型(int)，上证股票支持参数0、1、2、4，深证股票支持参数0、2、3、4、5，必传参数；

limit_price：保护限价(float)，委托上证股票时必传参数；

返回
Order对象中的id或者None。如果创建订单成功，则返回Order对象的id(str)，失败则返回None(NoneType)。

示例
def initialize(context):
    g.security = "600570.SS"
    set_universe(g.security)

def before_trading_start(context, data):
    g.flag = False

def handle_data(context, data):
    if not g.flag:
        # 以35保护限价按对手方最优价格买入100股
        order_market(g.security, 100, 0, 35)
        # 以35保护限价按最优五档即时成交剩余转限价买入100股
        order_market(g.security, 100, 1, 35)
        # 以35保护限价按本方最优价格买入100股
        order_market(g.security, 100, 2, 35)
        # 以35保护限价按最优五档即时成交剩余撤销买入100股
        order_market(g.security, 100, 4, 35)

        # 按对手方最优价格买入100股
        order_market("000001.SZ", 100, 0)
        # 按本方最优价格买入100股
        order_market("000001.SZ", 100, 2)
        # 按即时成交剩余撤销买入100股
        order_market("000001.SZ", 100, 3)
        # 按最优五档即时成交剩余撤销买入100股
        order_market("000001.SZ", 100, 4)
        # 按全额成交或撤单买入100股
        order_market("000001.SZ", 100, 5)
        g.flag = True
ipo_stocks_order - 新股一键申购
ipo_stocks_order(submarket_type=None, black_stocks=None)
使用场景
该函数仅在交易模块可用，对接jz_ufx不支持该函数

接口说明
该接口用于一键申购当日全部新股

注意事项：

申购黑名单的股票代码必须为申购代码，代码可以是6位数(不带尾缀)，也可以带尾缀入参,比如：black_stocks='787001'或black_stocks='787001.SS'。
参数
submarket_type：申购代码所属市场，不传时默认申购全部新股(int)；

black_stocks：黑名单股票，可以是单个股票或者股票列表，传入的黑名单股票将不做申购，不传时默认申购全部新股(str/list)；

返回
返回dict类型，包含委托代码、委托编号、委托状态(委托失败为0，委托成功为1)、委托数量等信息(dict[str:dict[str:str,str:int,str:float],...])

{'732116.SS': {'entrust_no': '205001', 'entrust_status': 1, 'redemption_amount': 1000}, '732100.SS': {'entrust_no': '205002', 'entrust_status': 1, 'redemption_amount': 2000}}
                            
示例
import time
def initialize(context):
    g.security = "600570.SS"
    set_universe(g.security)
    g.flag = False

def before_trading_start(context, data):
    g.flag = False

def handle_data(context, data):
    if not g.flag:
        # 上证普通代码
        log.info("申购上证普通代码：")
        ipo_stocks_order(submarket_type=0)
        time.sleep(5)
        # 上证科创板代码
        log.info("申购上证科创板代码：")
        ipo_stocks_order(submarket_type=1)
        time.sleep(5)
        # 深证普通代码
        log.info("申购深证普通代码：")
        ipo_stocks_order(submarket_type=2)
        time.sleep(5)
        # 深证创业板代码
        log.info("申购深证创业板代码：")
        ipo_stocks_order(submarket_type=3)
        time.sleep(5)
        # 可转债代码
        log.info("申购可转债代码：")
        ipo_stocks_order(submarket_type=4)
        time.sleep(5)
        g.flag = True
after_trading_order - 盘后固定价委托(股票)
after_trading_order(security, amount, entrust_price)
使用场景
该函数仅支持PTrade客户端可用、仅在股票交易模块可用，对接ATP柜台不支持该函数

接口说明
该接口用于盘后固定价委托申报

注意事项：

entrust_price为必传字段。
参数
security: 股票代码(str)；

amount: 交易数量，正数表示买入，负数表示卖出(int)；

entrust_price：买卖限价(float)；

返回
Order对象中的id或者None。如果创建订单成功，则返回Order对象的id(str)，失败则返回None(NoneType)。

示例
def initialize(context):
    g.security = "300001.SZ"
    set_universe(g.security)
    # 15:00-15:30期间使用run_daily进行盘后固定价委托
    run_daily(context, order_test, time="15:15")
    g.flag = False

def order_test(context):
    snapshot = get_snapshot(g.security)
    if snapshot is not None:
        last_px = snapshot[g.security].get("last_px", 0)
        if last_px > 0:
            after_trading_order(g.security, 200, float(last_px))

def handle_data(context, data):
    if not g.flag:
        snapshot = get_snapshot(g.security)
        if snapshot is not None:
            last_px = snapshot[g.security].get("last_px", 0)
            if last_px > 0:
                after_trading_order(g.security, 200, float(last_px))
                g.flag = True
after_trading_cancel_order - 盘后固定价委托撤单(股票)
after_trading_cancel_order(order_param)
使用场景
该函数仅支持PTrade客户端可用、仅在股票交易模块可用，对接ATP柜台不支持该函数

接口说明
该接口用于盘后固定价委托取消订单，根据Order对象或order_id取消订单。

注意事项：

无

参数
order_param: Order对象或者order_id(Order/str)

返回
None(NoneType)

示例
import time

def initialize(context):
    g.security = "300001.SZ"
    set_universe(g.security)
    # 15:00-15:30期间使用run_daily进行盘后固定价委托、盘后固定价委托撤单
    run_daily(context, order_test, time="15:15")
    g.flag = False

def order_test(context):
    snapshot = get_snapshot(g.security)
    if snapshot is not None:
        last_px = snapshot[g.security].get("last_px", 0)
        if last_px > 0:
            order_id = after_trading_order(g.security, 200, float(last_px))
            time.sleep(5)
            after_trading_cancel_order(order_id)


def handle_data(context, data):
    if not g.flag:
        snapshot = get_snapshot(g.security)
        if snapshot is not None:
            last_px = snapshot[g.security].get("last_px", 0)
            if last_px > 0:
                order_id = after_trading_order(g.security, 200, float(last_px))
                time.sleep(5)
                after_trading_cancel_order(order_id)
                g.flag = True
etf_basket_order - ETF成分券篮子下单
etf_basket_order(etf_code ,amount, price_style=None, position=True, info=None)
使用场景
该函数仅支持PTrade客户端可用、仅在股票交易模块可用，对接jz_ufx、ATP、云订柜台不支持该函数

接口说明
该接口用于ETF成分券篮子下单。

注意事项：

无

参数
etf_code : 单支ETF代码，必传参数(str)

amount : 下单篮子份数, 正数表示买入, 负数表示卖出，必传参数(int)

price_style : 设定委托价位，可传入’B1’、’B2’、’B3’、’B4’、’B5’、’S1’、’S2’、’S3’、’S4’、’S5’、’new’，分别为买一~买五、卖一~卖五、最新价，默认为最新价(str)

position : 取值True和False，仅在篮子买入时使用。申购是否使用持仓替代，True为使用，该情况下篮子股票买入时使用已有的持仓部分；False为不使用。默认使用持仓替代(bool)

info : dict类型，成份股信息。key为成分股代码，values为dict类型，包含的成分股信息字段作为key(Mapping[str, Mapping[str, Union[int, float]]]):

cash_replace_flag -- 设定现金替代标志，1为替代，0为不替代，仅允许替代状态的标的传入有效，否则无效，如不传入info或不传入该字段信息系统默认为成分股不做现金替代
position_replace_flag -- 设定持仓替代标志，1为替代，0为不替代，如不传入info或不传入该字段信息按position参数的设定进行计算
limit_price -- 设定委托价格，如不传入info或不传入该字段信息按price_style参数的设定进行计算
返回
创建订单成功，正常返回一个dict类型字段， key为股票代码，values为Order对象的id，失败则返回空dict，如{}(dict[str:str]))

{'600010.SS': '34e6733d26c14056b2096cafdec253b2', '600028.SS': '4299f7ad527842dd89f2a04cef48b935', '600030.SS': '1729b80b107d408d882a39814fef667d', '600031.SS': 'c17f28961d1248f0b914c62f2e44cd13', '600036.SS': 'ea7274a4e06349308f552d60181bbec8', '600048.SS': 'bd69c204a653483e975d2914c5fe5705', '600104.SS': 'ac8a890df68c453fb93333e19f58be91', '600111.SS': '9c9c5f604c2d43d396c811189699f072'}
                            
示例
def initialize(context):
    g.security = get_Ashares()
    set_universe(g.security)

def handle_data(context, data):
    #ETF成分券篮子下单
    etf_basket_order('510050.SS' ,1, price_style='S3',position=True)
    stock_info = {'600000.SS':{'cash_replace_flag':1,'position_replace_flag':1,'limit_price':12}}
    etf_basket_order('510050.SS' ,1, price_style='S2',position=False, info=stock_info)
etf_purchase_redemption - ETF基金申赎接口
etf_purchase_redemption(etf_code,amount,limit_price=None)
使用场景
该函数仅支持PTrade客户端可用、仅在股票交易模块可用，对接jz_ufx、ATP、云订柜台不支持该函数

接口说明
该接口用于单只ETF基金申赎。

注意事项：

无

参数
etf_code : 单支ETF代码，必传参数(str)

amount : 基金申赎数量, 正数表示申购, 负数表示赎回(int)

返回
创建订单成功，则返回Order对象的id(str)，失败则返回None(NoneType)。

示例
def initialize(context):
    g.security = '510050.SS'
    set_universe(g.security)

def handle_data(context, data):
    #ETF申购
    etf_purchase_redemption('510050.SS',900000)
    #ETF赎回
    etf_purchase_redemption('510050.SS',-900000,limit_price = 2.9995)
公共交易函数
order_tick - tick行情触发买卖
order_tick(sid, amount, priceGear='1', limit_price=None)
使用场景
该函数仅在交易模块可用

接口说明
该接口用于在tick_data模块中进行买卖股票下单，可设定价格档位进行委托。

注意事项：

该函数只能在tick_data模块中使用。
参数
sid：股票代码(str)；

amount：交易数量，正数表示买入，负数表示卖出(int)

priceGear：盘口档位，level1:1~5买档/-1~-5卖档，level2:1~10买档/-1~-10卖档(str)

limit_price：买卖限价，当输入参数中也包含priceGear时，下单价格以limit_price为主(float)；

返回
返回一个委托流水编号(str)

示例
import ast
def initialize(context):
    g.security = "600570.SS"
    set_universe(g.security)

def tick_data(context,data):
    security = g.security
    current_price = ast.literal_eval(data[security]['tick']['bid_grp'][0])[1][0]
    if current_price > 56 and current_price < 57:
        # 以买一档下单
        order_tick(g.security, -100, "1")
        # 以卖二档下单
        order_tick(g.security, 100, "-2")
        # 以指定价格下单
        order_tick(g.security, 100, limit_price=56.5)

def handle_data(context, data):
    pass
cancel_order - 撤单
cancel_order(order_param)
使用场景
该函数仅在回测、交易模块可用

接口说明
该接口用于取消订单，根据Order对象或order_id取消订单。

注意事项：

无

参数
order_param: Order对象或者order_id(Order/str)

返回
None(NoneType)

示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def handle_data(context, data):
    _id = order(g.security, 100)

    cancel_order(_id)
    log.info(get_order(_id))
cancel_order_ex - 撤单
cancel_order_ex(order_param)
使用场景
该函数仅在交易模块可用

接口说明
该接口用于取消订单，根据get_all_orders返回列表中的单个字典取消订单。

注意事项：

该函数仅可撤get_all_orders函数返回的可撤状态订单。
账户多个交易运行时调用该函数会撤销其他交易产生的订单，可能对其他正在运行的交易策略产生影响。
参数
order_param: get_all_orders函数返回列表的单个字典(dict)

返回
None(NoneType)

示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)
    g.count = 0

def handle_data(context, data):
    if g.count == 0:
        log.info("当日全部订单为：%s" % get_all_orders())
        # 遍历账户当日全部订单，对已报、部成状态订单进行撤单操作
        for _order in get_all_orders():
            if _order['status'] in ['2', '7']:
                cancel_order_ex(_order)
    if g.count == 1:
        # 查看撤单是否成功
        log.info("当日全部订单为：%s" % get_all_orders())
    g.count += 1
debt_to_stock_order - 债转股委托
debt_to_stock_order(security, amount)
使用场景
该函数仅在交易模块可用

接口说明
该接口用于可转债转股操作。

注意事项：

无

参数
security: 可转债代码(str)

amount: 委托数量(int)

返回
Order对象中的id或者None。如果创建订单成功，则返回Order对象的id(str)，失败则返回None(NoneType)。

示例
def initialize(context):
    g.security = "600570.SS"
    set_universe(g.security)

def before_trading_start(context, data):
    g.count = 0

def handle_data(context, data):
    if g.count == 0:
        # 对持仓内的国贸转债进行转股操作
        debt_to_stock_order("110033.SS", -1000)
        g.count += 1
    # 查看委托状态
    log.info(get_orders())
    g.count += 1
get_open_orders - 获取未完成订单
get_open_orders(security=None)
使用场景
该函数仅在回测、交易模块可用

接口说明
该接口用于获取当天所有未完成的订单，或按条件获取指定未完成的订单。

注意事项：

该接口仅支持获取本策略内的订单
未完成的状态(status(str))包括以下类型:
'0' -- "未报"
'1' -- "待报"
'2' -- "已报"
'3' -- "已报待撤"
'4' -- "部成待撤"
'7' -- "部成"
参数
security：标的代码，如'600570.SS'，不传时默认为获取所有未成交订单(str)；

返回
返回一个list，该list中包含多个Order对象(list[Order,...])。

[<Order {'id': '52e6a3f8a2b7468e92258c52dfcb6d42', 'dt': datetime.datetime(2025, 2, 21, 11, 25, 1, 229575), 'priceGear': 0, 'limit': 34.1, 'symbol': '600570.XSHG', 'amount': 1000, 'created': datetime.datetime(2025, 2, 21, 11, 25, 1, 229575), 'filled': 0, 'status': '2', 'entrust_no': '3596', 'cancel_entrust_no': None}>]
                            
示例
def initialize(context):
    g.security = ['600570.SS', '000001.SZ']
    set_universe(g.security)

def handle_data(context, data):
    for _sec in g.security:
        _id = order(_sec, 100, limit_price = 30)
    # 当运行周期为分钟则可获取本周期及之前所有未完成的订单
    dict_list = get_open_orders()
    log.info(dict_list)

# 当运行周期为天，可在after_trading_end中调用此函数获取当天未完成的订单
def after_trading_end(context, data):
    dict_list = get_open_orders()
    log.info(dict_list)
get_order - 获取指定订单
get_order(order_id)
使用场景
该函数仅在回测、交易模块可用

接口说明
该接口用于获取指定编号订单。

注意事项：

无

获取指定编号订单。

参数
order_id：订单编号(str)

返回
返回一个list，该list中只包含一个Order对象(list[Order])。

[<Order {'id': '52e6a3f8a2b7468e92258c52dfcb6d42', 'dt': datetime.datetime(2025, 2, 21, 11, 25, 1, 229575), 'priceGear': 0, 'limit': 34.1, 'symbol': '600570.XSHG', 'amount': 1000, 'created': datetime.datetime(2025, 2, 21, 11, 25, 1, 229575), 'filled': 0, 'status': '2', 'entrust_no': '3596', 'cancel_entrust_no': None}>]
                            
示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def handle_data(context, data):
    order_id = order(g.security, 100)
    current_order = get_order(order_id)
    log.info(current_order)
get_orders - 获取全部订单
get_orders(security=None)
使用场景
该函数仅在回测、交易模块可用

接口说明
该接口用于获取策略内所有订单，或按条件获取指定订单。

注意事项：

无

参数
security：标的代码，如'600570.SS'，不传时默认为获取所有订单(str)；

返回
返回一个list，该list中包含多个Order对象(list[Order,...])。

[<Order {'id': '52e6a3f8a2b7468e92258c52dfcb6d42', 'dt': datetime.datetime(2025, 2, 21, 11, 25, 1, 229575), 'priceGear': 0, 'limit': 34.1, 'symbol': '600570.XSHG', 'amount': 1000, 'created': datetime.datetime(2025, 2, 21, 11, 25, 1, 229575), 'filled': 0, 'status': '2', 'entrust_no': '3596', 'cancel_entrust_no': None}>]
                            
示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def handle_data(context, data):
    _id = order(g.security, 100)

    order_obj = get_orders()
    log.info(order_obj)
get_all_orders - 获取账户当日全部订单
get_all_orders(security=None)
使用场景
该函数仅在交易模块可用

接口说明
该接口用于获取账户当日所有订单(包含非本交易的订单记录)，或按条件获取指定代码的订单。

注意事项：

该函数返回账户当日在柜台的全部委托记录，不能查询策略中待报、未报状态的委托。
该函数返回的可撤委托仅可通过cancel_order_ex函数进行撤单，且非本交易的委托进行撤单仅可通过本函数查询委托状态更新。
股票、两融业务返回的amount字段区分正负值，卖出为负数；期货业务返回的amount字段不区分正负值，均为正数。
参数
security：标的代码，如'600570.SS'，不传时默认为获取所有订单(str)；

返回
返回一个list，该list中包含多条订单记录(list[dict, ...])：

股票、两融返回如下：

[{'symbol': , 'entrust_no': , 'amount': , 'entrust_bs': , 'price': , 'status': , 'filled_amount': , 'entrust_time': }, ...]

期货返回如下：

[{'symbol': , 'entrust_no': , 'amount': , 'entrust_bs': , 'price': , 'status': , 'filled_amount': , 'entrust_time': , 'futures_direction': }, ...]

symbol： 股票代码(str)
entrust_no： 委托编号(str)
amount： 委托数量(int)
entrust_bs： 委托方向(int)；
price： 委托价格(float)
status： 委托状态(str)；
filled_amount： 成交数量(int)
entrust_time： 委托时间(str)
futures_direction： 期货开平仓类型，期货专用(str)
示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def handle_data(context, data):
    # 获取账户当日委托600570代码的全部订单
    log.info('当日委托600570代码的全部订单：%s' % get_all_orders(g.security))
    # 获取账户当日全部订单
    log.info('当日全部订单：%s' % get_all_orders())
get_trades - 获取当日成交订单
get_trades()
使用场景
该函数仅在回测、交易模块可用

接口说明
该接口用于获取策略内当日已成交订单详情。

注意事项：

为减小对柜台压力，该函数在股票交易模块中同一分钟内多次调用返回当前分钟首次查询的缓存数据。
该接口会返回当日截止到当前时间段内的成交数据。
一个订单编号会对应一笔或多笔成交记录。
不同品种返回字段不同。
股票标的代码尾缀为四位，上证为XSHG，深圳为XSHE，如需对应到代码请做代码尾缀兼容。
获取国债逆回购成交详情时，成交价格字段实际为回购利率。
参数
无

返回
返回数据：

一个订单编号一笔成交：{'订单编号': [[]]} (dict{str: list[list[]]})

一个订单编号多笔成交：{'订单编号': [[], [], ...]} (dict{str: list[list[], list[], ...]})

股票返回字段：{'订单编号': [[成交编号, 委托编号, 标的代码, 买卖类型, 成交数量, 成交价格, 成交金额, 成交时间]]}

期货返回字段：{'订单编号': [[成交编号, 委托编号, 标的代码, 买卖类型, 开平仓类型, 成交数量, 成交价格, 成交金额, 成交时间]]}

成交编号：str类型
委托编号：str类型
标的代码：str类型
买卖类型：str类型
开平仓类型：开仓、平仓、平今仓，仅支持衍生品业务，str类型
成交数量：float类型
成交价格：float类型
成交金额：float类型
成交时间：YYYY-mm-dd HH:MM:SS格式，str类型
示例如下(股票)：

{'ba6a80d9746347a99c050b29069807c7': [['5001', '700001', '600570.XSHG', '买', 100000.0, 86.60, 8660000.0, '2021-08-15 09:32:00']]}
示例
def initialize(context):
    # 初始化策略
    g.security = "600570.SS"
    set_universe(g.security)

def before_trading_start(context, data):
    g.count = 0

def handle_data(context, data):
    if g.count == 0:
        # 按照回购利率1.76委托国债逆回购
        order("204001.SS", -1000, 1.76)
        g.count += 1
    log.info(get_trades())
融资融券专用函数
融资融券交易类函数
margin_trade - 担保品买卖
margin_trade(security, amount, limit_price=None, market_type=None)
使用场景
该函数仅支持PTrade客户端可用，仅在两融回测、两融交易模块可用。

接口说明
该接口用于担保品买卖。

注意事项：

限价和市价委托类型都不传时默认取当前最新价进行限价委托，限价和市价委托类型都传入时以limit_price为委托限价进行市价委托。
当market_type传入且委托上证股票时，limit_price为保护限价字段，必传字段。
参数
security：股票代码(str)；

amount：交易数量(int)，正数表示买入，负数表示卖出；

limit_price：买卖限价/保护限价(float)；

market_type：市价委托类型(int)，上证股票支持参数0、1、2、4，深证股票支持参数0、2、3、4、5；

返回
Order对象中的id或者None。如果创建订单成功，则返回Order对象的id(str)，失败则返回None(NoneType)。

示例
def initialize(context):
    g.security = "600570.SS"
    set_universe(g.security)

def before_trading_start(context, data):
    g.flag = False

def handle_data(context, data):
    if not g.flag:
        # 以系统最新价委托
        margin_trade(g.security, 100)
        # 以46块价格下一个限价单
        margin_trade(g.security, 100, limit_price=46)

        # 以46保护限价按最优五档即时成交剩余转限价买入100股
        margin_trade(g.security, 100, limit_price=46, market_type=1)
        # 按全额成交或撤单买入100股
        margin_trade("000001.SZ", 100, market_type=5)
        g.flag = True
margincash_open - 融资买入
margincash_open(security, amount, limit_price=None, market_type=None, cash_group=None)
使用场景
该函数仅支持PTrade客户端可用，仅在两融交易模块可用。

接口说明
该接口用于融资买入。

注意事项：

限价和市价委托类型都不传时默认取当前最新价进行限价委托，限价和市价委托类型都传入时以limit_price为委托限价进行市价委托。
当market_type传入且委托上证股票时，limit_price为保护限价字段，必传字段。
参数
security：股票代码(str)；

amount：交易数量，输入正数(int)；

limit_price：买卖限价(float)；

market_type：市价委托类型(int)，上证股票支持参数0、1、2、4，深证股票支持参数0、2、3、4、5；

cash_group：两融头寸性质(int)，1为普通头寸，2为专项头寸，该字段不入参默认表示普通头寸；

返回
Order对象中的id或者None。如果创建订单成功，则返回Order对象的id(str)，失败则返回None(NoneType)。

示例
def initialize(context):
    g.security = "600570.SS"
    set_universe(g.security)

def before_trading_start(context, data):
    g.flag = False

def handle_data(context, data):
    if not g.flag:
        # 以系统最新价委托
        margincash_open(g.security, 100)
        # 以46块价格下一个限价单
        margincash_open(g.security, 100, limit_price=46)

        # 以46保护限价按最优五档即时成交剩余转限价买入100股
        margincash_open(g.security, 100, limit_price=46, market_type=1)
        # 按全额成交或撤单买入100股
        margincash_open("000001.SZ", 100, market_type=5)
        g.flag = True
margincash_close - 卖券还款
margincash_close(security, amount, limit_price=None, market_type=None, cash_group=None)
使用场景
该函数仅支持PTrade客户端可用，仅在两融交易模块可用。

接口说明
该接口用于卖券还款。

注意事项：

限价和市价委托类型都不传时默认取当前最新价进行限价委托，限价和市价委托类型都传入时以limit_price为委托限价进行市价委托。
当market_type传入且委托上证股票时，limit_price为保护限价字段，必传字段。
参数
security：股票代码(str)；

amount：交易数量，输入正数(int)；

limit_price：买卖限价(float)；

market_type：市价委托类型(int)，上证股票支持参数0、1、2、4，深证股票支持参数0、2、3、4、5；

cash_group：两融头寸性质(int)，1为普通头寸，2为专项头寸，该字段不入参默认表示普通头寸；

返回
Order对象中的id或者None。如果创建订单成功，则返回Order对象的id(str)，失败则返回None(NoneType)。

示例
def initialize(context):
    g.security = "600570.SS"
    set_universe(g.security)

def before_trading_start(context, data):
    g.flag = False

def handle_data(context, data):
    if not g.flag:
        # 以系统最新价委托
        margincash_close(g.security, 100)
        # 以46块价格下一个限价单
        margincash_close(g.security, 100, limit_price=46)

        # 以46保护限价按最优五档即时成交剩余转限价卖100股还款
        margincash_close(g.security, 100, limit_price=46, market_type=1)
        # 按全额成交或撤单卖100股还款
        margincash_close("000001.SZ", 100, market_type=5)
        g.flag = True
margincash_direct_refund - 直接还款
margincash_direct_refund(value, cash_group=None)
使用场景
该函数仅支持PTrade客户端可用，仅在两融交易模块可用。

接口说明
该接口用于直接还款。

注意事项：

无

参数
value：还款金额(float)；

cash_group：两融头寸性质(int)，1为普通头寸，2为专项头寸，该字段不入参默认表示普通头寸；

返回
None

示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def handle_data(context, data):
    # 获取负债总额
    fin_compact_balance = get_margin_asset().get('fin_compact_balance')
    # 还款
    margincash_direct_refund(fin_compact_balance)
marginsec_open - 融券卖出
marginsec_open(security, amount, limit_price=None, cash_group=None)
使用场景
该函数仅支持PTrade客户端可用，仅在两融交易模块可用。

接口说明
该接口用于融券卖出。

注意事项：

无

参数
security：股票代码(str)；

amount：交易数量，输入正数(int)；

limit_price：买卖限价(float)；

cash_group：两融头寸性质(int)，1为普通头寸，2为专项头寸，该字段不入参默认表示普通头寸；

返回
Order对象中的id或者None。如果创建订单成功，则返回Order对象的id(str)，失败则返回None(NoneType)。

示例
def initialize(context):
    g.security = '600030.SS'
    set_universe(g.security)

def handle_data(context, data):
    security = g.security
    # 融券卖出100股
    marginsec_open(security, 100)
marginsec_close - 买券还券
marginsec_close(security, amount, limit_price=None, market_type=None, cash_group=None)
使用场景
该函数仅支持PTrade客户端可用，仅在两融交易模块可用。

接口说明
该接口用于买券还券。

注意事项：

限价和市价委托类型都不传时默认取当前最新价进行限价委托，限价和市价委托类型都传入时以limit_price为委托限价进行市价委托。
当market_type传入且委托上证股票时，limit_price为保护限价字段，必传字段。
参数
security：股票代码(str)；

amount：交易数量，输入正数(int)；

limit_price：买卖限价(float)；

market_type：市价委托类型(int)，上证股票支持参数0、1、2、4，深证股票支持参数0、2、3、4、5；

cash_group：两融头寸性质(int)，1为普通头寸，2为专项头寸，该字段不入参默认表示普通头寸；

返回
Order对象中的id或者None。如果创建订单成功，则返回Order对象的id(str)，失败则返回None(NoneType)。

示例
def initialize(context):
    g.security = "600030.SS"
    set_universe(g.security)

def before_trading_start(context, data):
    g.flag = False

def handle_data(context, data):
    if not g.flag:
        # 以系统最新价委托
        marginsec_close(g.security, 100)
        # 以46块价格下一个限价单
        marginsec_close(g.security, 100, limit_price=46)

        # 以46保护限价按最优五档即时成交剩余转限价买100股还券
        marginsec_close(g.security, 100, limit_price=46, market_type=1)
        # 按全额成交或撤单买100股还券
        marginsec_close("000001.SZ", 100, market_type=5)
        g.flag = True
marginsec_direct_refund - 直接还券
marginsec_direct_refund(security, amount, cash_group=None)
使用场景
该函数仅支持PTrade客户端可用，仅在两融交易模块可用。

接口说明
该接口用于直接还券。

注意事项：

无

参数
security：股票代码(str)；

amount：交易数量，输入正数(int)；

cash_group：两融头寸性质(int)，1为普通头寸，2为专项头寸，该字段不入参默认表示普通头寸；

返回
None

示例
def initialize(context):
    g.security = '600030.SS'
    set_universe(g.security)

def handle_data(context, data):
    security = g.security
    #买100股
    marginsec_direct_refund(security, 100)
融资融券查询类函数
get_margincash_stocks - 获取融资标的列表
get_margincash_stocks()
使用场景
该函数仅支持PTrade客户端可用，仅在两融交易模块可用，对接顶点HTS柜台暂不支持该函数。

接口说明
该接口用于获取融资标的。

注意事项：

无

参数
无

返回
返回上交所、深交所最近一次披露的的可融资标的列表的list(list[str,...])

['000002.SZ', '000519.SZ', '600570.SS', '600519.SS']
示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def handle_data(context, data):
    # 获取最新的融资标的列表
    margincash_stocks = get_margincash_stocks()
    log.info(margincash_stocks)
get_marginsec_stocks - 获取融券标的列表
get_marginsec_stocks()
使用场景
该函数仅支持PTrade客户端可用，仅在两融交易模块可用，对接顶点HTS柜台暂不支持该函数。

接口说明
该接口用于获取融券标的。

注意事项：

无

参数
无

返回
返回上交所、深交所最近一次披露的的可融券标的列表的list(list[str,...])

['000002.SZ', '000519.SZ', '600570.SS', '600519.SS']
示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def handle_data(context, data):
    # 获取最新的融券标的列表
    marginsec_stocks = get_marginsec_stocks()
    log.info(marginsec_stocks)
get_margin_contract - 合约查询
get_margin_contract(compact_source=None)
使用场景
该函数仅支持PTrade客户端可用，仅在两融交易模块可用。

接口说明
该接口用于合约查询。

注意事项：

无

参数
compact_source：合约来源(int)，0为普通头寸，1为专项头寸，该字段不入参默认表示普通头寸；

返回
正常返回一个DataFrame类型字段，columns为每个合约所包含的信息(相应字段无数据时返回None)，异常返回None(NoneType)

合约包含以下信息：

open_date:开户日期(str:int)；
compact_id:合约编号(str:str)；
stock_code:证券代码(str:str)；
entrust_no:委托编号(str:str)；
entrust_price:委托价格(str:float)；
entrust_amount:委托数量(str:float)；
business_amount:成交数量(str:float)；
business_balance:成交金额(str:float)；
compact_type:合约类别(str:str)；
compact_source:合约来源(str:str)；
compact_status:合约状态(str:str)；
repaid_interest:已还利息(str:float)；
repaid_amount:已还数量(str:float)；
repaid_balance:已还金额(str:float)；
used_bail_balance:已用保证金(str:float)；
ret_end_date:归还截止日(str:int)；
date_clear:清算日期(str:int)；
fin_income:融资合约盈亏(str:float)；
slo_income:融券合约盈亏(str:float)；
total_debit:负债总额(str:float)；
compact_interest:合约利息金额(str:float)；
real_compact_interest:日间实时利息金额(str:float)；
real_compact_balance:日间实时合约金额(str:float)；
real_compact_amount:日间实时合约数量(str:float)；

    open_date   compact_id   stock_code   ...   real_compact_balance   real_compact_amount
0   20250218   20250131234567   600570.SS   ...   103235.31   2800
1   20250219   20250131232321   000002.SZ   ...	  532581.10   72130
2   20250220   20250131232131   600519.SS   ...	  444000.00   300
示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def handle_data(context, data):
    # 获取最新合约
    df = get_margin_contract()
    log.info(df)
get_margin_contractreal - 实时合约流水查询
get_margin_contractreal()
使用场景
该函数仅支持PTrade客户端可用，仅在两融交易模块可用，对接金证集中，金证快订、云订柜台暂不支持该函数。

接口说明
该接口用于实时合约流水查询。

注意事项：

无

参数
无

返回
正常返回一个DataFrame类型字段，columns为每个合约所包含的信息(相应字段无数据时返回None)，异常返回None

实时合约流水包含以下信息：

init_date:交易日期(str:int)；
compact_id:合约编号(str:str)；
client_id:客户编号(str:str)；
money_type:币种类别(str:str)；
exchange_type:交易类别，仅包含1和2(str:str)；
entrust_no:委托编号(str:str)；
compact_type:合约类别(str:str)；
stock_code:证券代码(str:str)；
business_flag:业务标志(str:int)；
occur_balance:发生金额(str:float)；
post_balance:后资金额(str:float)；
occur_amount:发生数量(str:float)；
post_amount:后证券额(str:float)；
occur_fare:发生费用(str:float)；
post_fare:后余费用(str:float)；
occur_interest:发生利息(str:float)；
post_interest:后余利息(str:float)；
remark:备注(str:str)；

    init_date   compact_id   client_id   ...   post_interest   remark
0   20250218   20250131234567   339200779   ...	  58.2   利息
1   20250219   20250131232321   339200779   ...	  61.3   利息
2   20250220   20250131232131   339200779   ...	  77.1   利息
示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def handle_data(context, data):
    # 获取实时流水
    df = get_margin_contractreal()
    log.info(df)
get_margin_asset - 信用资产查询
get_margin_asset()
使用场景
该函数仅支持PTrade客户端可用，仅在两融交易模块可用。

接口说明
该接口用于信用资产查询。

注意事项：

无

参数
无

返回
正常返回一个dict类型字段，包含所有信用资产信息。异常返回空dict，如{}(dict[str:float,...])

信用资产包含以下信息(相应字段无数据时返回None)：

assure_asset:担保资产(str:float)；
total_debit:负债总额(str:float)；
enable_bail_balance:可用保证金(str:float)；
assure_enbuy_balance:买担保品可用资金(str:float)；
fin_enrepaid_balance:现金还款可用资金(str:float)；
fin_max_quota:融资额度上限(str:float)；
fin_enable_quota:融资可用额度(str:float)；
fin_used_quota:融资已用额度(str:float)；
fin_compact_balance:融资合约金额(str:float)；
fin_compact_fare:融资合约费用(str:float)；
fin_compact_interest:融资合约利息(str:float)；
slo_enable_quota:融券可用额度(str:float)；
slo_compact_fare:融券合约费用(str:float)；
slo_compact_interest:融券合约利息(str:float)；
{'slo_compact_fare': 0.0, 'assure_asset': 22647586233.8, 'fin_compact_interest': 0.0, 'fin_used_quota': 424057.23, 'slo_compact_interest': 0.59, 'fin_enable_quota': 575942.77, 'assure_enbuy_balance': 15796927.64, 'fin_enrepaid_balance': 15796927.64, 'total_debit': 288878.59, 'fin_compact_fare': 0.0, 'slo_enable_quota': 751589.0, 'enable_bail_balance': 16638502122.05, 'fin_max_quota': 1000000.0, 'fin_compact_balance': 156078.0}
                            
示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def handle_data(context, data):
    # 获取信用账户资产信息
    margin_asset = get_margin_asset()
    log.info(margin_asset)
get_assure_security_list - 担保券查询
get_assure_security_list()
使用场景
该函数仅支持PTrade客户端可用，仅在两融交易模块可用，对接顶点HTS柜台暂不支持该函数。

接口说明
该接口用于担保券查询。

注意事项：

无

参数
无

返回
返回上交所、深交所最近一次披露的担保券列表的list(list[str,...])

['000002.SZ', '000519.SZ', '600570.SS', '600519.SS']
                            
示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def handle_data(context, data):
    # 获取最新的担保券列表
    assure_security = get_assure_security_list()
    log.info(assure_security)
get_margincash_open_amount - 融资标的最大可买数量查询
get_margincash_open_amount(security, price=None, cash_group=None)
使用场景
该函数仅支持PTrade客户端可用，仅在两融交易模块可用。

接口说明
该接口用于融资标的最大可买数量查询。

注意事项：

无

参数
security：股票代码(str)；

price：限定价格(float)；

cash_group：两融头寸性质(int)，1为普通头寸，2为专项头寸，该字段不入参默认表示普通头寸；

返回
正常返回一个dict类型对象，key为股票代码，values为最大数量。异常返回空dict，如{}(dict[str:int])

{'600570.SS': 1900}
示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def handle_data(context, data):
    security = g.security
    # 查询恒生电子最大可融资买入数量
    margincash_open_dict = get_margincash_open_amount(security)
    if margincash_open_dict is not None:
        log.info(margincash_open_dict.get(security))
get_margincash_close_amount - 卖券还款标的最大可卖数量查询
get_margincash_close_amount(security, price=None, cash_group=None)
使用场景
该函数仅支持PTrade客户端可用，仅在两融交易模块可用。

接口说明
该接口用于卖券还款标的最大可卖数量查询。

注意事项：

无

参数
security：股票代码(str)；

price：限定价格(float)；

cash_group：两融头寸性质(int)，1为普通头寸，2为专项头寸，该字段不入参默认表示普通头寸；

返回
正常返回一个dict类型对象，key为股票代码，values为最大数量。异常返回空dict，如{}(dict[str:int])

{'600570.SS': 1500}
示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def handle_data(context, data):
    security = g.security
    # 查询恒生电子最大可卖券还款数量
    margincash_close_dict = get_margincash_close_amount(security)
    if margincash_close_dict is not None:
        log.info(margincash_close_dict.get(security))
get_marginsec_open_amount - 融券标的最大可卖数量查询
get_marginsec_open_amount(security, price=None, cash_group=None)
使用场景
该函数仅支持PTrade客户端可用，仅在两融交易模块可用。

接口说明
该接口用于融券标的最大可卖数量查询。

注意事项：

无

参数
security：股票代码(str)；

price：限定价格(float)；

cash_group：两融头寸性质(int)，1为普通头寸，2为专项头寸，该字段不入参默认表示普通头寸；

返回
正常返回一个dict类型对象，key为股票代码，values为最大数量。异常返回空dict，如{}(dict[str:int])

{'600570.SS': 2500}
示例
def initialize(context):
    g.security = '600030.SS'
    set_universe(g.security)

def handle_data(context, data):
    security = g.security
    # 查询中信证券最大可融券卖出数量
    marginsec_open_dict = get_marginsec_open_amount(security)
    if marginsec_open_dict is not None:
        log.info(marginsec_open_dict.get(security))
get_marginsec_close_amount - 买券还券标的最大可买数量查询
get_marginsec_close_amount(security, price=None, cash_group=None)
使用场景
该函数仅支持PTrade客户端可用，仅在两融交易模块可用。

接口说明
该接口用于买券还券标的最大可买数量查询。

注意事项：

无

参数
security：股票代码(str)；

price：限定价格(float)；

cash_group：两融头寸性质(int)，1为普通头寸，2为专项头寸，该字段不入参默认表示普通头寸；

返回
正常返回一个dict类型对象，key为股票代码，values为最大数量。异常返回空dict，如{}(dict[str:int])

{'600570.SS': 3000}
示例
def initialize(context):
    g.security = '600030.SS'
    set_universe(g.security)

def handle_data(context, data):
    security = g.security
    # 查询中信证券最大可买券还券数量
    marginsec_close_dict = get_marginsec_close_amount(security)
    if marginsec_close_dict is not None:
        log.info(marginsec_close_dict.get(security))
get_margin_entrans_amount - 现券还券数量查询
get_margin_entrans_amount(security, cash_group=None)
使用场景
该函数仅支持PTrade客户端可用，仅在两融交易模块可用。

接口说明
该接口用于现券还券数量查询。

注意事项：

无

参数
security：股票代码(str)；

cash_group：两融头寸性质(int)，1为普通头寸，2为专项头寸，该字段不入参默认表示普通头寸；

返回
正常返回一个dict类型对象，key为股票代码，values为最大数量。异常返回空dict，如{}(dict[str:int])

{'600570.SS': 1300}
示例
def initialize(context):
    g.security = '600030.SS'
    set_universe(g.security)

def handle_data(context, data):
    security = g.security
    # 查询中信证券最大可现券还券数量
    margin_entrans_dict = get_margin_entrans_amount(security)
    if margin_entrans_dict is not None:
        log.info(margin_entrans_dict.get(security))
get_enslo_security_info - 融券信息查询
get_enslo_security_info(cash_group=None)
使用场景
该函数仅支持PTrade客户端可用，仅在两融交易模块可用。

接口说明
该接口用于获取融券信息。

注意事项：

无

参数
cash_group：两融头寸性质(int)，1为普通头寸，2为专项头寸，该字段不入参默认表示普通头寸；

返回
正常返回一个dict类型对象，key为股票代码，values为dict，包含返回的相关字段信息，如(dict[{}, {}])。异常返回None(NoneType)。

包含以下信息(相应字段无数据时返回None)：

exchange_type: 交易类别， 仅包含1和2(str)；
slo_ratio: 融券保证金比例(float)；
enable_amount: 可用数量(int)；
real_buy_amount: 回报买入数量(int)；
real_sell_amount: 回报卖出数量(int)；
slo_status: 融券状态，包括"0":正常，"1":暂停，"2":作废(str)；
cashgroup_prop: 两融头寸性质，包括"1":普通，"2":专项(str)；
{'688001.SS': {'slo_status': '0', 'real_buy_amount': 0, 'cashgroup_prop': '1', 'enable_amount': 100000000000000, 'slo_ratio': 0.6, 'real_sell_amount': 0, 'exchange_type': '1'}, '010303.SS': {'slo_status': '0', 'real_buy_amount': 0, 'cashgroup_prop': '1', 'enable_amount': 100000000000000, 'slo_ratio': 0.6, 'real_sell_amount': 0, 'exchange_type': '1'}, '810004': {'slo_status': '0', 'real_buy_amount': 0, 'cashgroup_prop': '1', 'enable_amount': 10000, 'slo_ratio': 0.6, 'real_sell_amount': 0, 'exchange_type': '9'}}
                            
示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def handle_data(context, data):
    # 获取最新的融券信息
    h = get_enslo_security_info()
    log.info(h)
get_crdt_fund - 可融资金信息查询
get_crdt_fund(cash_group=None)
使用场景
该函数仅支持PTrade客户端可用，仅在两融交易模块可用。

接口说明
该接口用于获取可融资金信息查询。

注意事项：

无

参数
cash_group：两融头寸性质(int)，1为普通头寸，2为专项头寸，该字段不入参默认表示普通头寸；

返回
正常返回一个dict类型对象，key为股票代码，values为dict，包含返回的相关字段信息，如(dict[{}, {}])。异常返回None(NoneType)。

包含以下信息(相应字段无数据时返回None)：

enable_balance: 可用资金(float)；
real_buy_balance: 回报买入金额(float)；
real_sell_balance: 回报卖出金额(float)；
{'enable_balance': 68258.96, 'real_sell_balance': 446720.12, 'real_buy_balance': 491809.45}
                            
示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def handle_data(context, data):
    # 获取可融资金信息
    h = get_crdt_fund()
    log.info(h)
期货专用函数
期货交易类函数
buy_open - 多开
buy_open(contract, amount, limit_price=None)
使用场景
该函数仅在回测、交易模块可用

接口说明
买入开仓

注意：

不同期货品种每一跳的价格变动都不一样，limit_price入参的时候要参考对应品种的价格变动规则，如limit_price不做入参则会以交易的行情快照最新价或者回测的分钟最新价进行报单；

根据交易所规则，每天结束时会取消所有未完成交易；

参数
contract：期货合约代码；

amount：交易数量，正数；

limit_price：买卖限价；

返回
Order对象中的id或者None。如果创建订单成功，则返回Order对象的id(str)，失败则返回None(NoneType)。

示例
def initialize(context):
    g.security = ['IF2312.CCFX']
    set_universe(g.security)

def handle_data(context, data):
    #买入开仓
    buy_open('IF2312.CCFX', 1)
sell_close - 多平
sell_close(contract, amount, limit_price=None, close_today=False)
使用场景
该函数仅在回测、交易模块可用

接口说明
卖出平仓

注意：

不同期货品种每一跳的价格变动都不一样，limit_price入参的时候要参考对应品种的价格变动规则，如limit_price不做入参则会以交易的行情快照最新价或者回测的分钟最新价进行报单；

根据交易所规则，每天结束时会取消所有未完成交易；

参数
contract：期货合约代码；

amount：交易数量，正数；

limit_price：买卖限价；

close_today：平仓方式。close_today=False为优先平昨仓，不足部分再平今仓；close_today=True为仅平今仓，委托数量若大于今仓系统会调整为今仓数量。close_today=True仅对上海期货交易所生效，其他交易所无需入参close_today字段，若设置为True系统会警告，并强行转换为close_today=False。

返回
Order对象中的id或者None。如果创建订单成功，则返回Order对象的id(str)，失败则返回None(NoneType)。

示例
def initialize(context):
    g.security = ['IF2312.CCFX']
    set_universe(g.security)

def handle_data(context, data):
    #卖出平仓
    sell_close('IF2312.CCFX', 1)
sell_open - 空开
sell_open(contract, amount, limit_price=None)
使用场景
该函数仅在回测、交易模块可用

接口说明
卖出开仓

注意：

不同期货品种每一跳的价格变动都不一样，limit_price入参的时候要参考对应品种的价格变动规则，如limit_price不做入参则会以交易的行情快照最新价或者回测的分钟最新价进行报单；

根据交易所规则，每天结束时会取消所有未完成交易；

参数
contract：期货合约代码；

amount：交易数量，正数；

limit_price：买卖限价；

返回
Order对象中的id或者None。如果创建订单成功，则返回Order对象的id(str)，失败则返回None(NoneType)。

示例
def initialize(context):
    g.security = ['IF2312.CCFX']
    set_universe(g.security)

def handle_data(context, data):
    #卖出开仓
    sell_open('IF2312.CCFX', 1)
buy_close - 空平
buy_close(contract, amount, limit_price=None, close_today=False)
使用场景
该函数仅在回测、交易模块可用

接口说明
买入平仓

注意：

不同期货品种每一跳的价格变动都不一样，limit_price入参的时候要参考对应品种的价格变动规则，如limit_price不做入参则会以交易的行情快照最新价或者回测的分钟最新价进行报单；

根据交易所规则，每天结束时会取消所有未完成交易；

参数
contract：期货合约代码；

amount：交易数量，正数；

limit_price：买卖限价；

close_today：平仓方式。close_today=False为优先平昨仓，不足部分再平今仓；close_today=True为仅平今仓，委托数量若大于今仓系统会调整为今仓数量。close_today=True仅对上海期货交易所生效，其他交易所无需入参close_today字段，若设置为True系统会警告，并强行转换为close_today=False。

返回
Order对象中的id或者None。如果创建订单成功，则返回Order对象的id(str)，失败则返回None(NoneType)。

示例
def initialize(context):
    g.security = ['IF2312.CCFX']
    set_universe(g.security)

def handle_data(context, data):
    #买入平仓
    buy_close('IF2312.CCFX', 1)
期货查询类函数
get_margin_rate- 获取用户设置的保证金比例
get_margin_rate(transaction_code)
使用场景
该函数仅在回测模块可用

接口说明
获取用户设置的保证金比例

注意事项：

无

参数
transaction_code：期货合约的交易代码，str类型，如沪铜2112("CU2112")的交易代码为"CU"；

返回
用户设置的保证金比例，float浮点型数据，默认返回交易所设定的保证金比例；

示例
def initialize(context):
    g.security = "IF2312.CCFX"
    set_universe(g.security)
    # 设置沪深300指数的保证金比例为8%
    set_margin_rate("IF", 0.08)

def before_trading_start(context, data):
    # 获取沪深300指数的保证金比例
    margin_rate = get_margin_rate("IF")
    log.info(margin_rate)
    # 获取5年期国债的保证金比例
    margin_rate = get_margin_rate("TF")
    log.info(margin_rate)

def handle_data(context, data):
    pass
get_instruments- 获取合约信息
get_instruments(contract)
使用场景
该函数仅在回测、交易模块可用

接口说明
获取合约的上市的具体信息

注意事项：

期货实盘模块中，由于行情源的限制，涨跌幅目前暂无法提供。
此API依靠期货资料详情数据权限，使用前请与券商确认是否有此权限，无权限时调用返回空dict。
参数
contract：字符串，期货的合约代码，str类型；

返回
FutureParams对象，dict类型，key为字段名，value为字段值，主要返回的字段为:

contract_code -- 合约代码，str类型；
contract_name -- 合约名称，str类型；
exchange -- 交易所：大商所、郑商所、上期所、中金所，str类型；
trade_unit -- 交易单位，int类型；
contract_multiplier -- 合约乘数，float类型；
delivery_date -- 交割日期，str类型；
listing_date -- 上市日期，str类型；
trade_code -- 交易代码，str类型；
margin_rate -- 保证金比例，float类型；
changepct_limit -- 每日涨跌幅度，str类型(连续合约为空值)；
littlest_changeunit -- 最小变动价位，str类型(连续合约为空值)；
示例
def initialize(context):
    g.security = ["IF2312.CCFX"]
    set_universe(g.security)

def before_trading_start(context, data):
    # 获取股票池代码合约信息
    for security in g.security:
        info = get_instruments(security)
        log.info(info)

def handle_data(context, data):
    pass
get_dominant_contract- 获取主力合约代码
get_dominant_contract(contract, date=None)
使用场景
该函数在研究、回测、交易模块可用

接口说明
获取连续合约的主力合约代码

注意事项：

此API依靠期货主力合约与对应月合约数据权限，使用前请与券商确认是否有此权限，无权限时调用返回空dict。
参数
contract：字符串，期货的连续合约代码，str类型；

date：查询日期，不入参默认为当前日期，入参查询历史日期时支持datetime类型和str类型(仅支持'YYYY-mm-dd'和'YYYYmmdd'格式)；

返回
期货连续合约对应的主力合约相关信息，dict类型，key为主力合约，value为dict类型，包含以下字段；

corr_month_code -- 主力合约代码，str类型；
trade_date -- 交易日期，str类型，如:"2024-02-01"；
month_contract_name -- 主力合约名称，str类型；
示例
def initialize(context):
    g.security = "IF2312.CCFX"
    set_universe(g.security)

def handle_data(context, data):
    # 获取2023年1月3日的IF主力合约代码
    main_code_info = get_dominant_contract("IF888.CCFX",date='2023-01-03')
    log.info(main_code_info)
    # 获取当前交易日的IF主力合约代码
    main_code = get_dominant_contract("IF888.CCFX")["IF888.CCFX"]['corr_month_code']
    log.info(main_code)
期货设置类函数
set_future_commission - 设置期货手续费
set_future_commission(transaction_code, commission)
使用场景
该函数仅在回测模块可用

接口说明
设置期货手续费，手续费是按照交易代码进行设置的

注意事项：

期货回测的手续费分为按交易金额比例收取和按交易手数收取两种方式，当前支持的股指期货是按金额比例收取的，国债期货是按手数收取的。
参数
transaction_code：期货合约的交易代码，str类型，如沪铜2112("CU2112")的交易代码为"CU"；

commission：手续费，浮点型，设置说明：

当交易时的手续费是按手数收取时，则这里应当设置为每手收取的金额，例如：将期货的手续费设置为2元/手，此处应填写2；
当交易时的手续费是按总成交额收取时，则这里应当设置为总成交额的比例，例如：将期货的手续费费率设置为0.4/万，此处应填写0.00004；
返回
None

示例
def initialize(context):
    g.security = "IF2312.CCFX"
    set_universe(g.security)
    # 设置沪深300指数的手续费，0.4/万
    set_future_commission("IF", 0.00004)

def handle_data(context, data):
    # 买入指数2312
    buy_open(g.security, 2)
set_margin_rate - 设置期货保证金比例
set_margin_rate(transaction_code, margin_rate)
使用场景
该函数仅在回测模块可用

接口说明
设置期货收取的保证金比例，保证金比例是按照交易代码进行设置的

注意事项：

无

参数
transaction_code：期货合约的交易代码，str类型，如沪铜2112("CU2112")的交易代码为"CU"；

margin_rate：保证金比例，浮点型，将对应期货的保证金比例设置为5%则输入0.05；

返回
None

示例
def initialize(context):
    g.security = "IF2312.CCFX"
    set_universe(g.security)
    # 设置沪深300指数收取的保证金比例设置为5%
    set_margin_rate("IF", 0.05)

def handle_data(context, data):
    # 买入指数2312
    buy_open(g.security, 10)
计算函数
技术指标计算函数
get_MACD - 异同移动平均线
get_MACD(close, short=12, long=26, m=9)
使用场景
该函数仅在回测、交易模块可用

接口说明
获取异同移动平均线MACD指标的计算结果

注意事项：

无

参数
close：价格的时间序列数据, numpy.ndarray类型；

short: 短周期, int类型；

long: 长周期, int类型；

m: 移动平均线的周期, int类型；

返回
MACD指标dif值的时间序列, numpy.ndarray类型

MACD指标dea值的时间序列, numpy.ndarray类型

MACD指标macd值的时间序列, numpy.ndarray类型

示例
def initialize(context):
    g.security = "600570.XSHG"
    set_universe(g.security)

def handle_data(context, data):
    h = get_history(100, '1d', ['close','high','low'], security_list=g.security)
    close_data = h['close'].values
    macdDIF_data, macdDEA_data, macd_data = get_MACD(close_data, 12, 26, 9)
    dif = macdDIF_data[-1]
    dea = macdDEA_data[-1]
    macd = macd_data[-1]
get_KDJ - 随机指标
get_KDJ(high, low, close, n=9, m1=3, m2=3)
使用场景
该函数仅在回测、交易模块可用

接口说明
获取KDJ指标的计算结果，KDJ指标（随机指标）是一种动量指标，主要用于识别金融资产（如股票、期货等）的超买超卖状态、潜在趋势转折点及价格波动强度。它由三条曲线组成：K线（快速线）、D线（慢速线）和J线（方向敏感线），通过价格波动的统计计算反映市场短期动能。

注意事项：

无

参数
high：最高价的时间序列数据, numpy.ndarray类型；

low：最低价的时间序列数据, numpy.ndarray类型；

close：收盘价的时间序列数据, numpy.ndarray类型；

n: 周期参数，用来计算未成熟随机值（RSV）的周期长度（RSV是计算KDJ的过程变量），决定指标对价格波动的敏感度。周期越短（如N=5），指标反应越灵敏；周期越长（如N=14），信号越平滑但可能滞后。默认为9天, int类型；

m1: K值的平滑周期，对RSV进行指数移动平均（EMA）处理，进一步平滑K值曲线，默认为3天, int类型；

m2: D值的平滑周期，对RSV进行指数移动平均（EMA）处理，进一步平滑D值曲线，默认为3天, int类型；

返回
KDJ指标k值的时间序列, numpy.ndarray类型

KDJ指标d值的时间序列, numpy.ndarray类型

KDJ指标j值的时间序列, numpy.ndarray类型

示例
def initialize(context):
    g.security = "600570.XSHG"
    set_universe(g.security)

def handle_data(context, data):
    h = get_history(100, '1d', ['close','high','low'], security_list=g.security)
    high_data = h['high'].values
    low_data = h['low'].values
    close_data = h['close'].values
    k_data, d_data, j_data = get_KDJ(high_data, low_data, close_data, 9, 3, 3)
    k = k_data[-1]
    d = d_data[-1]
    j = j_data[-1]
get_RSI - 相对强弱指标
get_RSI(close, n=6)
使用场景
该函数仅在回测、交易模块可用

接口说明
获取相对强弱指标RSI指标的计算结果

注意事项：

无

参数
close：价格的时间序列数据, numpy.ndarray类型；

n: 周期, int类型；

返回
RSI指标rsi值的时间序列, numpy.ndarray类型

示例
def initialize(context):
    g.security = "600570.XSHG"
    set_universe(g.security)

def handle_data(context, data):
    h = get_history(100, '1d', ['close','high','low'], security_list=g.security)
    close_data = h['close'].values
    rsi_data = get_RSI(close_data, 6)
    rsi = rsi_data[-1]
get_CCI - 顺势指标
get_CCI(close, n=14)
使用场景
该函数仅在回测、交易模块可用

接口说明
获取顺势指标CCI指标的计算结果

注意事项：

无

参数
high：最高价的时间序列数据, numpy.ndarray类型；

low：最低价的时间序列数据, numpy.ndarray类型；

close：收盘价的时间序列数据, numpy.ndarray类型；

n: 周期, int类型；

返回
CCI指标cci值的时间序列, numpy.ndarray类型

示例
def initialize(context):
    g.security = "600570.XSHG"
    set_universe(g.security)

def handle_data(context, data):
    h = get_history(100, '1d', ['close','high','low'], security_list=g.security)
    high_data = h['high'].values
    low_data = h['low'].values
    close_data = h['close'].values
    cci_data = get_CCI(high_data, low_data, close_data, 14)
    cci = cci_data[-1]
其他函数
log-日志记录
log(content)
使用场景
该函数仅在回测、交易模块可用。

接口说明
该接口用于打印日志。

支持如下场景的日志记录：

log.debug("debug")
log.info("info")
log.warning("warning")
log.error("error")
log.critical("critical")
与python的logging模块用法一致

注意事项：

无

参数
参数可以是字符串、对象等。

返回
None

示例
# 打印出一个格式化后的字符串
g.security='600570.SS'
log.info("Selling %s, amount=%s" % (g.security, 10000)) 
is_trade-业务代码场景判断
is_trade()
使用场景
该函数仅在回测、交易模块可用。

接口说明
该接口用于提供业务代码执行场景判断依据，明确标识当前业务代码运行场景为回测还是交易。因部分函数仅限回测或交易场景使用，该函数可以协助区分对应场景，以便限制函数可以在一套策略代码同时兼容回测与交易场景。

注意事项：

无

参数
无

返回
布尔类型，当前代码在交易中运行返回True，当前代码在回测中运行返回False(bool)。

示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def handle_data(context, data):
    _id = order(g.security, 100)

    if is_trade():
        log.info("当前运行场景：交易")
    else:
        log.info("当前运行场景：回测")
check_limit - 代码涨跌停状态判断
check_limit(security, query_date=None)
使用场景
该函数在研究、回测、交易模块可用。

接口说明
该接口用于标识股票的涨跌停情况。

注意事项：

入参的query_date仅支持YYYYmmdd格式的传参，当query_date入参为None或传入当日日期时，返回的结果是以实时最新价判断涨跌停状态；当query_date入参为历史交易日期，则均以交易日收盘价判断涨跌停状态。
参数
security：单只股票代码或者多只股票代码组成的列表，必填字段(list[str]/str)；

query_date：查询日期，查询指定日期股票代码的涨跌停状态，回测不传默认是回测当日时间，交易和研究不传默认是执行当日时间，非必填字段(str)；

返回
正常返回一个dict类型数据，包含每只股票代码的涨停状态。多只股票代码查询时其中部分股票代码查询异常则该代码返回既不涨停也不跌停状态0。(dict[str:int])

涨跌停状态说明：

2：触板涨停(已经是涨停价格，但还有卖盘)(仅支持交易研究查询当日)；
1：涨停；
0：既不涨停也不跌停；
-1：跌停；
-2：触板跌停(已经是跌停价格，但还有买盘)(仅支持交易研究查询当日)；
示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def handle_data(context, data):
    # 代码涨跌停状态
    stock_flag = check_limit(g.security)[g.security]
    log.info(stock_flag)
send_email - 发送邮箱信息
send_email(send_email_info, get_email_info, smtp_code, info='', path='', subject='')
使用场景
该函数仅在交易模块可用。

接口说明
该接口用于通过QQ邮箱发送邮件内容。

注意事项：

该接口需要服务端连通外网，是否开通由所在券商决定。
是否允许发送附件(即path参数)，由所在券商的配置管理决定。
邮件中接受到的附件为文件名而非附件路径。
参数
send_email_info：发送方的邮箱地址，必填字段，如:50xxx00@qq.com(str)；

get_email_info：接收方的邮箱地址，必填字段，如:[50xxx00@qq.com, 1xxx10@126.com](list[str]/str)；

smtp_code：邮箱的smtp授权码，注意，不是邮箱密码，必填字段(str)；

info：发送内容，选填字段，默认空字符串(str)；

path：附件路径，选填字段，如:get_research_path() + 'stock.csv'，默认空字符串(str)；

subject：邮件主题，默认空字符串(str)；

返回
None

示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def handle_data(context, data):
    #发送文字信息
    send_email('53xxxxxx7@qq.com', ['53xxxxx7@qq.com', 'Kxxxxn@126.com'], 'phfxxxxxxxxxxcd', info='今天的股票池信息')
send_qywx - 发送企业微信信息
send_qywx(corp_id, secret, agent_id, info='', path='', toparty='', touser= '', totag= '')
使用场景
该函数仅在交易模块可用。

接口说明
该接口用于通过企业微信发送内容，使用方法请查看 企业微信功能使用手册。

注意事项：

该接口需要服务端连通外网，是否开通由所在券商决定。
是否允许发送文件(即path参数)，由所在券商的配置管理决定。
企业微信不能同时发送文字和文件，当同时入参info和path的时候，默认发送文件。
企业微信接受到的文件为文件名而非文件路径。
2022年6月20日之后创建的应用由于需要配置企业可信ip(企业微信官方升级)导致企业微信功能不可用，该日期之前创建的应用仍可以正常使用。
参数
corp_id：企业ID，必填字段(str)；

secret：企业微信应用的密码，必填字段(str)；

agent_id：企业微信应用的ID，必填字段(str)；

info：发送内容，选填字段，默认空字符串(str)；

path：发送文件，选填字段，如:get_research_path() + 'stock.csv'，默认空字符串(str)；

toparty：发送对象为部门，选填字段，默认空字符串(str)，多个对象之间用 '|' 符号分割；

touser：发送内容为个人，选填字段，默认空字符串(str)，多个对象之间用 '|' 符号分割；

totag：发送内容为分组，选填字段，默认空字符串(str)，多个对象之间用 '|' 符号分割；

注意：toparty、touser、totag如果都不传入，接口默认发送至应用中设定的第一个toparty

返回
None

示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def handle_data(context, data):
    #发送文字信息
    send_qywx('wwxxxxxxxxxxxxf9', 'hixxxxxxxxxxxxxxxxxxxBX8', '10xxxx3', info='已触发委托买入', toparty='1|2')
permission_test-权限校验
permission_test(account=None, end_date=None)
使用场景
该函数仅在交易模块可用

接口说明
该接口用于账号和有效期的权限校验，用户可以在接口中入参指定账号和指定有效期截止日，策略运行时会校验运行策略的账户与指定账户是否相符，以及运行当日日期是否超过指定的有效期截止日，任一条件校验失败，接口都会返回False，两者同时校验成功则返回True。校验失败会在策略日志中提示原因。

注意事项：

如果需要使用授权模式下载功能，不要在接口中入参，策略编码时候直接调用permission_test()，授权工具会把需要授权的账号和有效期信息放到策略文件中。
该函数仅在initialize、before_trading_start、after_trading_end模块中支持调用。
参数
account：授权账号，选填字段，如果不填就代表不需要验证账号(str)；

end_date：授权有效期截止日，选题字段，如果不填就代表不需要验证有效期(str)，日期格式必须为'YYYYmmdd'的8位日期格式，如'20200101'；

返回
布尔类型，校验成功返回True，校验失败返回False(bool)。

示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)
def handle_data(context, data):
    pass
def after_trading_end(context, data):
    # 需要用授权模式下载功能的情况下不用入参
    flag = permission_test()
    if not flag:
        raise RuntimeError('授权不通过，终止程序，抛出异常')
    # 不需要用授权模式下载功能的情况下通过入参来进行授权校验
    flag = permission_test(account='10110922',end_date='20220101')
    if not flag:
        raise RuntimeError('授权不通过，终止程序，抛出异常')
create_dir-创建文件路径
create_dir(user_path)
使用场景
该函数在研究、回测、交易模块可用

接口说明
由于PTrade量化引擎禁用了os模块，因此用户无法在策略中通过编写代码实现子目录创建。用户可以通过此接口来创建文件的子目录路径。

注意事项：

创建文件的根路径为研究界面根路径。
参数
user_path(str)：待创建目录相对路径，必传字段。

比如user_path='download'，会在研究界面生成download的目录；

比如user_path='download/2022'，会在研究界面生成download/2022的目录；

返回
是否创建成功(True/False)(bool)。

示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)
    # 在研究界面创建600570.SS目录
    create_dir(g.security)
def handle_data(context, data):
    pass
get_frequency-获取当前业务代码的周期
get_frequency()
使用场景
该函数在回测、交易模块可用

接口说明
该接口用于返回当前业务代码的周期，如在周期为分钟的情况下执行回测或交易，该函数返回minute；在周期为每日的情况下执行回测或交易，该函数返回daily。

注意事项：

无

参数
无

返回
周期为分钟返回minute，周期为每日返回daily(str)

示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)
    log.info(get_frequency())
def handle_data(context, data):
    pass
get_business_type - 获取当前策略的业务类型
get_business_type()
使用场景
该函数在回测、交易模块可用

接口说明
该接口用于返回当前策略的业务类型。

注意事项：

无

参数
无

返回
策略业务类型(str)：

stock -- 股票
rzrq -- 融资融券
future -- 期货
示例
def initialize(context):
    # 初始化策略
    g.security = "600570.SS"
    set_universe(g.security)


def before_trading_start(context, data):
    g.flag = False
    g.business_type = get_business_type()
    log.info("当前策略的业务类型为：%s" % g.business_type)


def handle_data(context, data):
    if g.flag is False:
        if g.business_type == "stock":
            order("600570.SS", 100)
        elif g.business_type == "future":
            buy_open("IF2309.CCFX", 1, 3816.0)
        g.flag = True
get_current_kline_count-获取股票业务当前时间的分钟bar数量
get_current_kline_count()
使用场景
该函数在回测、交易、研究模块可用

接口说明
该接口获取当前时间股票的k线根数。

注意事项：

回测中返回回测日当前时间的分钟bar数量。
研究中返回最新交易日当前时间的分钟bar数量，非交易日执行均返回0。
交易中返回最新交易日当前时间的分钟bar数量。
参数
无

返回
当前时间的分钟bar数量(int)

示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)
def handle_data(context, data):
    log.info(get_current_kline_count())
filter_stock_by_status-过滤指定状态的股票代码
filter_stock_by_status(stocks, filter_type=["ST", "HALT", "DELISTING"], query_date=None)
使用场景
该函数在回测、交易、研究模块可用

接口说明
该接口用于过滤指定状态的股票代码。

注意事项：

仅支持before_trading_start模块调用

参数
stocks: 例如 ['000001.SZ','000003.SZ']。该字段必须输入。(list[str]/str)；

filter_type: 支持以下四种类型属性的过滤条件，默认为["ST", "HALT", "DELISTING"](str/list)

具体支持输入的字段包括 ：

'ST' - 查询是否属于ST股票
'HALT' - 查询是否停牌
'DELISTING' - 查询是否退市
'DELISTING_SORTING' - 查询是否退市整理期(只过滤交易当日数据)
query_date: 格式为YYYYmmdd，默认为None,表示当前日期(回测为回测当前周期，研究与交易则取系统当前时间)(str)；

返回
股票列表（该列表已剔除符合任一指定状态的标的）(list)

示例
def initialize(context):
    g.security = ['123002.SZ',"688500.SS","000001.SZ", "603997.SS", '123181.SZ']
    set_universe(g.security)

def before_trading_start(context, data):
    filter_stock = filter_stock_by_status(g.security, ["ST", "HALT", "DELISTING"])
    log.info(filter_stock)

def handle_data(context, data):
    pass
check_strategy-检查策略内容
check_strategy(strategy_content=None, strategy_path=None)
使用场景
该函数在研究模块可用

接口说明
该接口用于检查策略内容是否涉及升级过程中变动的API和Python库。

注意事项：

每次版本升级后应当将使用的策略内容统一检查一遍。
strategy_content和strategy_path都传入时仅对strategy_content入参内容进行检查。
如果传入strategy_path，需要将对应策略文件上传至研究，且必须是utf-8编码的文本文件。
如果日志打印策略内容涉及升级过程变动，需根据告警信息参考API接口说明调整策略内容。
参数
strategy_content: 策略内容(str)。

strategy_path: 策略路径(str)。

返回
策略内容涉及升级过程中变动的API和Python库信息(list)。

接收到的数据如下：
{
"api_change_list": [
    "margincash_open",
    "get_history",
    "get_fundamentals",
    "get_etf_info",
    "get_individual_transaction",
    "get_individual_transcation",
    "check_limit",
    "get_price",
    "get_snapshot",
    "on_trade_response",
    "set_parameters",
    "set_yesterday_position",
    "marginsec_open",
    "order_market",
    "margin_trade",
    "get_user_name",
    "debt_to_stock_order",
    "get_instruments",
    "get_margincash_open_amount",
    "get_all_orders",
    "run_interval",
    "get_trades",
    "margincash_close",
    "marginsec_close",
    "get_margin_assert",
    "ipo_stocks_order",
    "get_enslo_security_info",
    "get_hks_unit_amount",
    "get_individual_entrust",
    "get_tick_direction",
    "get_margin_contractreal",
    "get_gear_price",
    "get_stock_status"],
"package_change_list": [
    "walrus",
    "keras",
    "pykalman",
    "arch",
    "cvxopt",
    "pulp"]，
}
                        
示例
check_strategy(strategy_content="""
import arch
import cvxopt
import keras
import pulp
import pykalman
import tensorflow
import walrus


def initialize(context):
    g.security = "600570.SS"
    set_universe(g.security)
    pos={}
    pos["sid"] = "600570.SS"
    pos["amount"] = "1000"
    pos["enable_amount"] = "600"
    pos["cost_basis"] = "55"
    set_yesterday_position([pos])
    run_interval(context, interval_handle, seconds=10)


def interval_handle(context):
    pass


def before_trading_start(context, data):
    get_history(100, frequency="1d", field=["close"], security_list=g.security)
    get_fundamentals(g.security, "balance_statement", "total_assets")
    get_etf_info("510020.SS")
    get_individual_transaction()
    get_individual_transcation()
    check_limit(g.security)
    get_price(g.security, start_date="20150101", end_date="20150131", frequency="1d")
    get_snapshot(g.security)
    set_parameters(holiday_not_do_before="1")
    get_user_name(False)
    get_instruments(g.security)
    get_all_orders()
    get_trades()
    get_margin_assert()
    get_enslo_security_info()
    get_hks_unit_amount("02899.XHKG-SS", "1")
    get_individual_entrust()
    get_tick_direction([g.security])
    get_margin_contractreal()
    get_gear_price(g.security)
    get_stock_status([g.security], "ST")


def on_trade_response(context, trade_list):
    pass


def handle_data(context, data):
    margincash_open(g.security, 100)
    marginsec_open(g.security, 100)
    order_market(g.security, 100, 0, 35)
    margin_trade(g.security, 100)
    get_margincash_open_amount(g.security)
    debt_to_stock_order("110033.SS", -1000)
    margincash_close(g.security, 100)
    marginsec_close(g.security, 100)
    ipo_stocks_order(submarket_type=0)
""")
check_strategy(strategy_path="./strategy.txt")
fund_transfer-资金调拨
fund_transfer(trans_direction, occur_balance, exchange_type="1")
使用场景
该函数仅在股票交易模块可用

接口说明
用于UF20柜台与极速柜台、UF20柜台与极速柜台双中心资金调拨。

注意事项：


如要使用该函数，需咨询券商当前柜台是否支持。
当前仅支持UF20柜台与ATP柜台、UF20柜台与ATP柜台双中心资金调拨。
如果是UF20与ATP柜台，exchange_type可不传。
如果是UF20与ATP柜台双中心，exchange_type为必传字段。
参数
trans_direction(str)：调拨方向，0为转入极速、1为转出极速。

occur_balance(float)：发生金额(单位：元，最小精度：0.01元)。

exchange_type(str)：交易类别，1为上海、2为深圳。

返回
返回调拨是否成功True/False(bool)。

示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def before_trading_start(context, data):
    # 转出深A极速柜台100000元
    fund_transfer('1', 100000, exchange_type='2')

def handle_data(context, data):
            pass
market_fund_transfer-市场间资金调拨
market_fund_transfer(exchange_type, occur_balance)
使用场景
该函数仅在股票交易模块可用

接口说明
用于极速柜台双中心之间资金调拨。

注意事项：


如要使用该函数，需咨询券商当前柜台是否支持。
当前仅支持ATP柜台双中心之间资金调拨。
参数
exchange_type(str)：交易类别，1为上海、2为深圳。

occur_balance(float)：发生金额(单位：元，最小精度：0.01元)。

返回
返回调拨是否成功True/False(bool)。

示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def before_trading_start(context, data):
    # 转入沪A极速柜台100000元
    market_fund_transfer('1', 100000)

def handle_data(context, data):
    pass
公共资源
对象
g - 全局对象
使用场景
该对象仅支持回测、交易模块。

对象说明
全局对象g，用于存储用户的各类可被不同函数(包括自定义函数)调用的全局数据,如：

g.security = None #股票池
注意事项：

无

示例
def initialize(context):
    g.security = "600570.SS"
    g.count = 1
    g.flag = 0
    set_universe(g.security)

def handle_data(context, data):
    log.info(g.security)
    log.info(g.count)
    log.info(g.flag)
Context - 上下文对象
使用场景
该对象仅支持回测、交易模块。

对象说明
类型为业务上下文对象

注意事项：

对象内的portfolio数据更新周期详见Portfolio对象对象注意事项说明。
内容
capital_base -- 起始资金
previous_date -- 前一个交易日
sim_params -- SimulationParameters对象
    capital_base -- 起始资金
    data_frequency -- 数据频率
portfolio -- 账户信息，可参考Portfolio对象
initialized -- 是否执行初始化
slippage -- 滑点，VolumeShareSlippage对象
    volume_limit -- 成交限量
    price_impact -- 价格影响力
commission -- 佣金费用，Commission对象
    tax—印花税费率
    cost—佣金费率
    min_trade_cost—最小佣金
blotter -- Blotter对象(记录)
    current_dt -- 当前单位时间的开始时间，datetime.datetime对象(北京时间)
recorded_vars -- 收益曲线值
示例
def initialize(context):
    g.security = ['600570.SS', '000001.SZ']
    set_universe(g.security)

def handle_data(context, data):
    # 获得当前回测相关时间
    pre_date = context.previous_date
    log.info(pre_date)
    year = context.blotter.current_dt.year
    log.info(year)
    month = context.blotter.current_dt.month
    log.info(month)
    day = context.blotter.current_dt.day
    log.info(day)
    hour = context.blotter.current_dt.hour
    log.info(hour)
    minute = context.blotter.current_dt.minute
    log.info(minute)
    second = context.blotter.current_dt.second
    log.info(second)
    # 获取"年-月-日"格式
    date = context.blotter.current_dt.strftime("%Y-%m-%d")
    log.info(date)
    # 获取周几
    weekday = context.blotter.current_dt.isoweekday()
    log.info(weekday)
BarData - K线数据对象
使用场景
该对象仅支持回测、交易模块。

对象说明
一个单位时间内代码的K线数据，是一个类对象。

注意事项：

preclose、high_limit、low_limit、unlimited在分钟频率中均填充为0.0。
当前周期内首次调用会在线获取该代码K线数据，当前周期重复调用时将会返回首次调用缓存的该代码K线数据。
基本属性
以下属性也能通过get_history()/get_price()获取到

symbol 标的代码
name 代码名称
dt 当前周期时间
is_open 停牌标志，0-停牌，1-非停牌
open 当前周期开盘价
close 当前周期收盘价
price 当前周期最新价
low 当前周期最低价
high 当前周期最高价
volume 当前周期成交量
money 当前周期成交额
preclose 昨收盘价(仅日线返回)
high_limit 涨停价(仅日线返回)
low_limit 跌停价(仅日线返回)
unlimited 是否无涨跌停限制(仅日线返回)
datetime 当前周期时间
示例
def initialize(context):
    g.security = "600570.SS"
    set_universe(g.security)


def before_trading_start(context, data):
    g.flag = False


def handle_data(context, data):
    if not g.flag:
        # 打印代码BarData对象
        log.info(data[g.security])
        # 打印标的代码
        log.info(data[g.security].symbol)
        # 打印代码名称
        log.info(data[g.security].name)
        # 打印当前周期时间
        log.info(data[g.security].dt)
        # 打印当前周期是否开盘
        log.info(data[g.security].is_open)
        # 打印当前周期开盘价
        log.info(data[g.security].open)
        # 打印当前周期收盘价
        log.info(data[g.security].close)
        # 打印当前周期最新价
        log.info(data[g.security].price)
        # 打印当前周期最低价
        log.info(data[g.security].low)
        # 打印当前周期最高价
        log.info(data[g.security].high)
        # 打印当前周期成交量
        log.info(data[g.security].volume)
        # 打印当前周期成交额
        log.info(data[g.security].money)
        # 打印昨收盘价(仅日线返回)
        log.info(data[g.security].preclose)
        # 打印涨停价(仅日线返回)
        log.info(data[g.security].high_limit)
        # 打印跌停价(仅日线返回)
        log.info(data[g.security].low_limit)
        # 打印是否无涨跌停限制(仅日线返回)
        log.info(data[g.security].unlimited)
        # 打印当前周期时间
        log.info(data[g.security].datetime)
        g.flag = True
Portfolio - 资产对象
使用场景
该对象仅支持回测、交易模块。

对象说明
对象数据包含账户当前的资金，标的信息，即所有标的操作仓位的信息汇总

注意事项：

交易中对象内的数据更新周期默认为6s(具体配置需咨询所在券商)，即上一次账户资金、委托、持仓查询并更新到对象中后，间隔6s发起下一次查询。数据更新时间范围为before_trading_start-after_trading_end。
内容
股票账户返回
     cash 当前可用资金(不包含冻结资金)
     positions 当前持有的标的(包含不可卖出的标的)，dict类型，key是标的代码，value是Position对象
     portfolio_value 当前持有的标的和现金的总价值
     positions_value 持仓价值
     capital_used 已使用的现金
     returns 当前的收益比例, 相对于初始资金
     pnl 当前账户总资产-初始账户总资产
     start_date 开始时间
期货账户返回：
     cash 当前可用资金(不包含冻结资金)
     positions 当前持有的标的(包含不可卖出的标的)，dict类型，key是标的代码，value是Position对象
     portfolio_value 当前持有的保证金和现金的总价值
     positions_value 持仓价值
     returns 当前的收益比例, 相对于初始资金
     pnl 当前账户总资产-初始账户总资产
     start_date 开始时间
     margin 保证金
示例
def initialize(context):
    g.security = "600570.SS"
    set_universe([g.security])

def handle_data(context, data):
    log.info(context.portfolio.portfolio_value)
Position - 持仓对象
使用场景
该对象仅支持回测、交易模块。

对象说明
持有的某个标的的信息。

注意事项：

期货业务持仓把单个合约的持仓分为了多头仓(long)、空头仓(short)。
交易中对象内的数据更新周期默认为6s(具体配置需咨询所在券商)，即上一次账户资金、委托、持仓查询并更新到对象中后，间隔6s发起下一次查询。数据更新时间范围为before_trading_start-after_trading_end。
交易场景下，持仓信息是每6秒与柜台同步后更新的，update_time字段记录了最近的更新时间，格式为："%Y-%m-%d %H:%M:%S"。回测场景返回None。
内容
股票账户返回
     sid 标的代码
     enable_amount 可用数量
     amount 总持仓数量
     last_sale_price 最新价格
     cost_basis 持仓成本价格
     today_amount 今日开仓数量
     business_type 持仓类型
     update_time 持仓更新时间
期货账户返回：
     sid 标的代码
     short_enable_amount 空头仓可用数量
     long_enable_amount 多头仓可用数量
     today_short_amount 空头仓今仓数量
     today_long_amount 多头仓今仓数量
     long_cost_basis 多头仓持仓成本
     short_cost_basis 空头仓持仓成本
     long_amount 多头仓总持仓量
     short_amount 空头仓总持仓量
     long_pnl 多头仓浮动盈亏
     short_pnl 空头仓浮动盈亏
     amount 总持仓数量
     enable_amount 可用数量
     last_sale_price 最新价格
     business_type 持仓类型
     delivery_date 交割日，期货使用
     margin 持仓保证金
     contract_multiplier 合约乘数
     update_time 持仓更新时间
示例
def initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)

def handle_data(context, data):
    order(g.security,1000)
    position = get_position(g.security)
    log.info(position)
Order - 委托对象
使用场景
该对象仅支持回测、交易模块。

对象说明
买卖订单信息

注意事项：

回测中entrust_no、cancel_entrust_no字段值为None。
交易中对象内的数据更新分为两种同时进行：1.数据周期默认为6s(具体配置需咨询所在券商)，即上一次账户资金、委托、持仓查询并更新到对象中后，间隔6s发起下一次查询。数据更新时间范围为before_trading_start-after_trading_end。2.后台接收到主推数据时会更新对象内成交数量、委托状态、持仓成本价等信息。
交易中对原委托进行撤单时，cancel_entrust_no字段值填充撤单委托编号。
交易中期货(对接UFT柜台)对原委托进行撤单时，撤单委托编号等于原委托编号。
内容
股票账户返回
    id -- 订单号
    dt -- 订单产生时间，datetime.datetime类型
    limit -- 指定价格
    symbol -- 标的代码(备注：标的代码尾缀为四位，上证为XSHG，深圳为XSHE，如需对应到代码请做代码尾缀兼容)
    amount -- 下单数量，买入是正数，卖出是负数
    created -- 订单生成时间，datetime.datetime类型
    filled -- 成交数量，买入时为正数，卖出时为负数
    entrust_no -- 委托编号
    cancel_entrust_no -- 撤单委托编号
    priceGear -- 盘口档位
    status -- 委托状态     
期货账户返回：
    id -- 订单号
    dt -- 订单产生时间，datetime.datetime类型
    limit -- 指定价格
    symbol -- 标的代码
    amount -- 下单数量，正数
    created -- 订单生成时间，datetime.datetime类型
    side -- 多空仓标志(str类型，long：多头仓，short：空头仓)
    action -- 开平仓方向(str类型，open：开仓，close：平仓)
    entrust_direction -- 买卖方向(str类型，buy：买入，sell：卖出)
    filled -- 成交数量，正数
    entrust_no -- 委托编号
    cancel_entrust_no -- 撤单委托编号
    priceGear -- 盘口档位
    status -- 委托状态     
示例
def initialize(context):
    g.security = "600570.SS"
    set_universe(g.security)

def handle_data(context, data):
    order(g.security, 100)
    log.info(get_orders())
数据字典
status -- 委托状态
"0" -- 未报
"1" -- 待报
"2" -- 已报
"3" -- 已报待撤
"4" -- 部成待撤
"5" -- 部撤
"6" -- 已撤
"7" -- 部成
"8" -- 已成
"9" -- 废单
"+" -- 已受理
"-" -- 已确认
"C" -- 正报
"V" -- 已确认
entrust_type -- 委托类别
"0" -- 委托
"2" -- 撤单
"4" -- 确认
"6" -- 信用融资
"7" -- 信用融券
"9" -- 信用交易
entrust_prop -- 委托属性
"0" -- 买卖
"1" -- 配股
"3" -- 申购
"4" -- 回购
"7" -- 转股
"9" -- 股息
"N" -- ETF申赎
"Q" -- 对手方最优价格
"R" -- 最优五档即时成交剩余转限价
"S" -- 本方最优价格
"T" -- 即时成交剩余撤销
"U" -- 最优五档即时成交剩余撤销
"V" -- 全成交或撤销
"b" -- 定价委托
"c" -- 确认委托
"d" -- 限价委托
"HKN" -- 港股订单申报
"HKO" -- 零股订单申报
business_direction -- 成交方向
0 -- 卖
1 -- 买
2 -- 借入
3 -- 出借
trans_kind -- 委托类型
深圳市场
1 -- 市价委托
2 -- 限价委托
3 -- 本方最优
上海市场
4 -- 增加订单
5 -- 删除订单
trade_status -- 交易状态
"START" -- 市场启动(初始化之后，集合竞价前)
"PRETR" -- 盘前
"OCALL" -- 开始集合竞价
"TRADE" -- 交易(连续撮合)
"HALT" -- 暂停交易
"SUSP" -- 停盘
"BREAK" -- 休市
"POSTR" -- 盘后
"ENDTR" -- 交易结束
"STOPT" -- 长期停盘，停盘n天，n>=1
"DELISTED" -- 退市
"POSMT" -- 盘后交易
"PCALL" -- 盘后集合竞价
"INIT" -- 盘后固定价格启动前
"ENDPT" -- 盘后固定价格闭市阶段
"POSSP " -- 盘后固定价格停牌
trans_flag -- 成交标记
0 -- 普通成交
1 -- 撤单成交
trans_identify_am -- 盘后逐笔成交序号标识
0 -- 盘中
1 -- 盘后
entrust_bs -- 委托方向
"1" -- 买
"2" -- 卖
cash_replace_flag -- 现金替代标志
"0" -- 禁止替代
"1" -- 允许替代
"2" -- 必须替代
"3" -- 非沪市退补现金替代
"4" -- 非沪市必须现金替代
"5" -- 非沪深退补现金替代
"6" -- 非沪深必须现金替代
exchange_type/futu_exch_type -- 交易类别
"0" -- 资金
"1" -- 上海
"2" -- 深圳
"9" -- 特转A
"A" -- 特转B
"D" -- 沪Ｂ
"G" -- 沪港通
"H" -- 深Ｂ
"Q" -- 青岛产权
"S" -- 深港通
"T" -- 场外OTC市场
"U" -- 转融通
"J" -- 金华基金
"K" -- 香港市场
"X" -- 固定收益
"F1" -- 郑州交易所
"F2" -- 大连交易所
"F3" -- 上海交易所
"F4" -- 金融交易所
"F5" -- 能源交易所
"Z1" -- 业务受理
"R" -- H股全流通
delist_flag -- 退市标志
"0" -- 正常
"1" -- 退市
hedge_type -- 投机/套保类型
"0" -- 投机
"1" -- 套保
"2" -- 套利
"3" -- 做市商
"4" -- 备兑
"0" -- 权利方
"1" -- 义务方
"2" -- 备兑方
"C" -- 看涨期权
"P" -- 看跌期权
market_type -- 市价委托类型
0 -- 对手方最优价格
1 -- 最优五档即时成交剩余转限价
2 -- 本方最优价格
3 -- 即时成交剩余撤销
4 -- 最优五档即时成交剩余撤销
5 -- 全额成交或撤单
submarket_type -- 申购代码所属市场
0 -- 上证普通代码
1 -- 上证科创板代码
2 -- 深证普通代码
3 -- 深证创业板代码
4 -- 可转债代码
cash_group -- 两融头寸性质
0 -- 核心头寸
1 -- 普通业务头寸
2 -- 专项业务头寸
compact_type -- 合约类别
"0" -- 融资
"1" -- 融券
"2" -- 其他负债
compact_status -- 合约状态
"0" -- 开仓未归还
"1" -- 部分归还
"2" -- 合约已过期
"3" -- 客户自行归还
"4" -- 手工了结
"5" -- 未形成负债
underlying_type -- 关联类型
0 -- A股
1 -- B股
2 -- H股
3 -- 期货
4 -- 期权
5 -- 港股-认购
6 -- 港股-认沽
7 -- 港股-牛证
8 -- 港股-熊证
9 -- 港股-界内证
10 -- 英股关联关系
11 -- 美股关联代码
12 -- 股本认股权证认购证
13 -- 股本认股权证认沽证
14 -- 可转债关联关系正向-正股关联可转债
15 -- 可转债关联关系反向-可转债关联正股
real_type -- 成交类型
"0" -- 买卖
"1" -- 查询
"2" -- 撤单
"6" -- 融资
"7" -- 融券
"8" -- 平仓
"9" -- 信用
"G" -- 期权强制平仓
real_status -- 成交状态
"0" -- 成交
"2" -- 废单
"4" -- 确认
策略示例
策略示例

常见问题
使用本平台受阻，可参考常见问题说明

支持的三方库
Python3.5支持的三方库

Python3.11支持的三方库

三方库变动
类名/函数名	Python3.5实现	Python3.11实现	说明
Numpy	numpy.linalg.lstsq	def lstsq(a, b, rcond=-1):	def lstsq(a, b, rcond="warn"):	参数默认值改变
Pandas	pandas.concat	def concat(objs, axis=0, join='outer', join_axes=None, ignore_index=False, keys=None, levels=None, names=None, verify_integrity=False, sort=None, copy=True):	def concat(objs:Iterable[NDFrame]|Mapping[HashableT, NDFrame], axis:Axis=0, join:str="outer", ignore_index:bool=False, keys=None, levels=None, names=None, verify_integrity:bool=False, sort:bool=False, copy:bool=True)->DataFrame|Series:	弃用join_axes参数
pandas.DatetimeIndex	def __new__(cls, data=None, freq=None, start=None, end=None, periods=None, tz=None, normalize=False, closed=None, ambiguous='raise', dayfirst=False, yearfirst=False, dtype=None, copy=False, name=None, verify_integrity=True):	def __new__(cls, data=None, freq:str|BaseOffset|lib.NoDefault=lib.no_default, tz=None, normalize:bool=False, closed=None, ambiguous="raise", dayfirst:bool=False, yearfirst:bool=False, dtype:Dtype|None=None, copy:bool=False, name:Hashable=None)->DatetimeIndex:	弃用start参数
pandas.DataFrame.append	def append(self, other, ignore_index=False, verify_integrity=False, sort=None):	def append(self, other, ignore_index:bool=False, verify_integrity:bool=False, sort:bool=False)->DataFrame:	参数默认值改变
pandas.DataFrame.apply	def apply(self, func, axis=0, broadcast=None, raw=False, reduce=None, result_type=None, args=(), **kwds):	def apply(self, func:AggFuncType, axis:Axis=0, raw:bool=False, result_type:Literal["expand", "reduce", "broadcast"]|None=None, args=(), **kwargs):	弃用broadcast参数
pandas.DataFrame.astype	def astype(self, dtype, copy=True, errors='raise', **kwargs):	def astype(self:NDFrameT, dtype, copy:bool_t=True, errors:IgnoreRaise="raise")->NDFrameT:	不再支持以kwargs方式传入额外入参
pandas.DataFrame.quantile	def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation='linear'):	def quantile(self, q:float|AnyArrayLike|Sequence[float]=0.5, axis:Axis=0, numeric_only:bool|lib.NoDefault=no_default, interpolation:QuantileInterpolation="linear", method:Literal["single", "table"]="single")->Series|DataFrame:	参数默认值改变
pandas.DataFrame.replace	def replace(self, to_replace=None, value=None, inplace=False, limit=None, regex=False, method='pad'):	def replace(self, to_replace=None, value=lib.no_default, inplace:bool=False, limit:int|None=None, regex:bool=False, method:Literal["pad", "ffill", "bfill"]|lib.NoDefault=lib.no_default)->DataFrame|None:	参数默认值改变
pandas.DataFrame.resample	def resample(self, rule, how=None, axis=0, fill_method=None, closed=None, label=None, convention='start', kind=None, loffset=None, limit=None, base=0, on=None, level=None):	def resample(self, rule, axis:Axis=0, closed:str|None=None, label:str|None=None, convention:str="start", kind:str|None=None, loffset=None, base:int|None=None, on:Level=None, level:Level=None, origin:str|TimestampConvertibleTypes="start_day", offset:TimedeltaConvertibleTypes|None=None, group_keys:bool|lib.NoDefault=no_default, )->Resampler:	弃用how参数
pandas.DataFrame.sort_index	def sort_index(self, axis=0, level=None, ascending=True, inplace=False, kind='quicksort', na_position='last', sort_remaining=True, by=None):	def sort_index(self, axis:Axis=0, level:IndexLabel=None, ascending:bool|Sequence[bool]=True, inplace:bool=False, kind:SortKind="quicksort", na_position:NaPosition="last", sort_remaining:bool=True, ignore_index:bool=False, key:IndexKeyFunc=None)->DataFrame|None:	弃用by参数
pandas.DataFrame.to_csv	def to_csv(self, path_or_buf=None, sep=",", "", na_rep='', float_format=None, columns=None, header=True, index=True, index_label=None, mode='w', encoding=None, compression=None, quoting=None, quotechar='"', line_terminator='\n', chunksize=None, tupleize_cols=None, date_format=None, doublequote=True, escapechar=None, decimal='.'):	def to_csv(self, path_or_buf:FilePath|WriteBuffer[bytes]|WriteBuffer[str]|None=None, sep:str=",", na_rep:str="", float_format:str|Callable|None=None, columns:Sequence[Hashable]|None=None, header:bool_t|list[str]=True, index:bool_t=True, index_label:IndexLabel|None=None, mode:str="w", encoding:str|None=None, compression:CompressionOptions="infer", quoting:int|None=None, quotechar:str='"', lineterminator:str|None=None, chunksize:int|None=None, date_format:str|None=None, doublequote:bool_t=True, escapechar:str|None=None, decimal:str=".", errors:str="strict", storage_options:StorageOptions=None)->str|None:	参数默认值改变
pandas.DataFrame.to_excel	def to_excel(self, excel_writer, sheet_name='Sheet1', na_rep='', float_format=None, columns=None, header=True, index=True, index_label=None, startrow=0, startcol=0, engine=None, merge_cells=True, encoding=None, inf_rep='inf', verbose=True, freeze_panes=None):	def to_excel(self, excel_writer, sheet_name:str="Sheet1", na_rep:str="", float_format:str|None=None, columns:Sequence[Hashable]|None=None, header:Sequence[Hashable]|bool_t=True, index:bool_t=True, index_label:IndexLabel=None, startrow:int=0, startcol:int=0, engine:str|None=None, merge_cells:bool_t=True, encoding:lib.NoDefault=lib.no_default, inf_rep:str="inf", verbose:lib.NoDefault=lib.no_default, freeze_panes:tuple[int, int]|None=None, storage_options:StorageOptions=None)->None:	参数默认值改变
pandas.DataFrame.to_html	def to_html(self, buf=None, columns=None, col_space=None, header=True, index=True, na_rep='NaN', formatters=None, float_format=None, sparsify=None, index_names=True, justify=None, bold_rows=True, classes=None, escape=True, max_rows=None, max_cols=None, show_dimensions=False, notebook=False, decimal='.', border=None, table_id=None):	def to_html(self, buf:FilePath|WriteBuffer[str]|None=None, columns:Sequence[Level]|None=None, col_space:ColspaceArgType|None=None, header:bool|Sequence[str]=True, index:bool=True, na_rep:str="NaN", formatters:FormattersType|None=None, float_format:FloatFormatType|None=None, sparsify:bool|None=None, index_names:bool=True, justify:str|None=None, max_rows:int|None=None, max_cols:int|None=None, show_dimensions:bool|str=False, decimal:str=".", bold_rows:bool=True, classes:str|list|tuple|None=None, escape:bool=True, notebook:bool=False, border:int|bool|None=None, table_id:str|None=None, render_links:bool=False, encoding:str|None=None)->str|None:	参数顺序改变
pandas.DataFrame.to_json	def to_json(self, path_or_buf=None, orient=None, date_format=None, double_precision=10, force_ascii=True, date_unit='ms', default_handler=None, lines=False, compression=None, index=True):	def to_json(self, path_or_buf:FilePath|WriteBuffer[bytes]|WriteBuffer[str]|None=None, orient:str|None=None, date_format:str|None=None, double_precision:int=10, force_ascii:bool_t=True, date_unit:str="ms", default_handler:Callable[[Any], JSONSerializable]|None=None, lines:bool_t=False, compression:CompressionOptions="infer", index:bool_t=True, indent:int|None=None, storage_options:StorageOptions=None)->str|None:	参数默认值改变
pandas.DataFrame.to_records	def to_records(self, index=True, convert_datetime64=None):	def to_records(self, index:bool=True, column_dtypes=None, index_dtypes=None)->np.recarray:	弃用convert_datetime64参数
pandas.DataFrame.to_string	def to_string(self, buf=None, columns=None, col_space=None, header=True, index=True, na_rep='NaN', formatters=None, float_format=None, sparsify=None, index_names=True, justify=None, line_width=None, max_rows=None, max_cols=None, show_dimensions=False):	def to_string(self, buf:FilePath|WriteBuffer[str]|None=None, columns:Sequence[str]|None=None, col_space:int|list[int]|dict[Hashable, int]|None=None, header:bool|Sequence[str]=True, index:bool=True, na_rep:str="NaN", formatters:fmt.FormattersType|None=None, float_format:fmt.FloatFormatType|None=None, sparsify:bool|None=None, index_names:bool=True, justify:str|None=None, max_rows:int|None=None, max_cols:int|None=None, show_dimensions:bool=False, decimal:str=".", line_width:int|None=None, min_rows:int|None=None, max_colwidth:int|None=None, encoding:str|None=None)->str|None:	参数顺序改变
pandas.DataFrame.update	def update(self, other, join='left', overwrite=True, filter_func=None, raise_conflict=False):	def update(self, other, join:str="left", overwrite:bool=True, filter_func=None, errors:str="ignore")->None:	弃用raise_conflict参数
pandas.Panel	def __init__(self, data=None, items=None, major_axis=None, minor_axis=None, copy=False, dtype=None):		在pandas(0.25.0)版本已弃用
pandas.read_excel	def read_excel(io, sheet_name=0, header=0, names=None, index_col=None, usecols=None, squeeze=False, dtype=None, engine=None, converters=None, true_values=None, false_values=None, skiprows=None, nrows=None, na_values=None, parse_dates=False, date_parser=None, thousands=None, comment=None, skipfooter=0, convert_float=True, **kwds):	def read_excel(io, sheet_name:str|int|list[IntStrT]|None=0, header:int|Sequence[int]|None=0, names:list[str]|None=None, index_col:int|Sequence[int]|None=None, usecols:int|str|Sequence[int]|Sequence[str]|Callable[[str], bool]|None=None, squeeze:bool|None=None, dtype:DtypeArg|None=None, engine:Literal["xlrd", "openpyxl", "odf", "pyxlsb"]|None=None, converters:dict[str, Callable]|dict[int, Callable]|None=None, true_values:Iterable[Hashable]|None=None, false_values:Iterable[Hashable]|None=None, skiprows:Sequence[int]|int|Callable[[int], object]|None=None, nrows:int|None=None, na_values=None, keep_def ault_na:bool=True, na_filter:bool=True, verbose:bool=False, parse_dates:list|dict|bool=False, date_parser:Callable|None=None, thousands:str|None=None, decimal:str=".", comment:str|None=None, skipfooter:int=0, convert_float:bool|None=None, mangle_dupe_cols:bool=True, storage_options:StorageOptions=None)->DataFrame|dict[IntStrT, DataFrame]:	参数默认值改变
pandas.read_json	def read_json(path_or_buf=None, orient=None, typ='frame', dtype=True, convert_axes=True, convert_dates=True, keep_def ault_dates=True, numpy=False, precise_float=False, date_unit=None, encoding=None, lines=False, chunksize=None, compression='infer'):	def read_json(path_or_buf:FilePath|ReadBuffer[str]|ReadBuffer[bytes], orient:str|None=None, typ:Literal["frame", "series"]="frame", dtype:DtypeArg|None=None, convert_axes=None, convert_dates:bool|list[str]=True, keep_def ault_dates:bool=True, numpy:bool=False, precise_float:bool=False, date_unit:str|None=None, encoding:str|None=None, encoding_errors:str|None="strict", lines:bool=False, chunksize:int|None=None, compression:CompressionOptions="infer", nrows:int|None=None, storage_options:StorageOptions=None)->DataFrame|Series|JsonReader:	参数默认值改变
pandas.testing.assert_frame_equal	def assert_frame_equal(left, right, check_dtype=True, check_index_type='equiv', check_column_type='equiv', check_frame_type=True, check_less_precise=False, check_names=True, by_blocks=False, check_exact=False, check_datetimelike_compat=False, check_categorical=True, check_like=False, obj='DataFrame'):	def assert_frame_equal(left, right, check_dtype:bool|Literal["equiv"]=True, check_index_type:bool|Literal["equiv"]="equiv", check_column_type="equiv", check_frame_type=True, check_less_precise=no_default, check_names=True, by_blocks=False, check_exact=False, check_datetimelike_compat=False, check_categorical=True, check_like=False, check_freq=True, check_flags=True, rtol=1.0e-5, atol=1.0e-8, obj="DataFrame")->None:	参数默认值改变
pandas.to_datetime	def to_datetime(arg, errors='raise', dayfirst=False, yearfirst=False, utc=None, box=True, format=None, exact=True, unit=None, infer_datetime_format=False, origin='unix', cache=False):	def to_datetime(arg:DatetimeScalarOrArrayConvertible|DictConvertible, errors:DateTimeErrorChoices="raise", dayfirst:bool=False, yearfirst:bool=False, utc:bool|None=None, format:str|None=None, exact:bool=True, unit:str|None=None, infer_datetime_format:bool=False, origin="unix", cache:bool=True)->DatetimeIndex|Series|DatetimeScalar|NaTType|None:	弃用box参数
pandas.to_pickle	def to_pickle(obj, path, compression='infer', protocol=pkl.HIGHEST_PROTOCOL):	def to_pickle(obj:Any, filepath_or_buffer:FilePath|WriteBuffer[bytes], compression:CompressionOptions="infer", protocol:int=pickle.HIGHEST_PROTOCOL, storage_options:StorageOptions=None) -> None:	protocol表示二进制数据序列化协议，Python3.5默认使用4版本协议，Python3.11默认使用5版本协议。使用5版本协议保存的pickle文件将无法在Python3.5版本读取。
接口版本变动
变动版本	变动内容
PTrade1.0-QTV202401.05.032	
run_interval()新增支持interval_timer_ranges(设置指定函数运行的时间范围)入参；
PTrade1.0-QTV202401.05.031	
Python3.5新增三方库：gmssl==3.2.2，psycopg2-binary==2.8.6
Python3.11新增三方库：gmssl==3.2.2，psycopg2-binary==2.9.11
PTrade1.0-QTV202401.05.030	
新增get_fundamentalsbalance_statement表返回字段增加contract_liability、total_fixed_asset、t_constru_in_process字段，income_statement表返回字段增加r_and_d字段；
PTrade1.0-QTV202401.05.021	
get_market_list()仅返回系统支持的四个市场；
get_market_detail()仅支持入参系统支持的四个市场；
Python3.11新增三方库：dtaidistance==2.3.13
PTrade1.0-QTV202401.05.013	
get_price()接口中的fq字段新增支持dypre-动态前复权；
get_price()接口异常返回空字典改为返回值为None；
PTrade1.0-QTV202401.05.011	
Python3.11升级三方库：sxsc-tushare==1.2.11-->sxsc-tushare==20240927
Python3.5升级三方库：sxsc-tushare==1.2.11-->sxsc-tushare==20240927
PTrade1.0-QTV202401.05.008	
Portfolio期货返回字段删除capital_used，增加margin；
PTrade1.0-QTV202401.05.000	
Python3.11升级三方库：bs4==0.0.1-->bs4==0.0.2
Python3.11升级三方库：gensim==4.3.0-->gensim==4.3.3
Python3.11升级三方库：jax==0.4.13-->jax==0.4.18
Python3.11升级三方库：jaxlib==0.4.13-->jaxlib==0.4.18
Python3.11升级三方库：line_profiler==4.0.2-->line_profiler==4.1.3
Python3.11升级三方库：qdldl==0.1.7.post0-->qdldl==0.1.7.post4
Python3.11升级三方库：TA-Lib==0.4.25-->TA-Lib==0.4.31
Python3.11新增三方库：asyncache==0.3.1, fastapi==0.100.0, h11==0.14.0, pydantic==1.10.7, starlette==0.27.0, uvicorn==0.30.6, baostock==0.8.9
Python3.5新增三方库：baostock==0.8.9
股票Position对象展示字段新增update_time(持仓更新时间)；
新增 成交类型字典；
新增 成交状态字典；
PTrade1.0-QTV202401.04.000	
新增fund_transfer()资金调拨；
新增market_fund_transfer()市场间资金调拨；
新增set_email_info()设置邮件信息；
on_trade_response()新增返回real_type: 成交类型、real_status: 成交状态两个字段；
run_interval()seconds最小运行间隔时间的设置规则修改为期货最小1秒，股票等其他业务最小3秒；
create_dir()出参None修改为是否创建成功(True/False)；
Python3.5新增三方库：walrus==0.9.3
PTrade1.0-QTV202401.02.000	
margincash_open()字段cash_group不入参修改为默认表示普通头寸；
margincash_close()增加cash_group字段入参；
margincash_direct_refund()增加cash_group字段入参；
marginsec_open()字段cash_group不入参修改为默认表示普通头寸；
marginsec_direct_refund()增加cash_group字段入参；
get_margincash_open_amount()字段cash_group不入参修改为默认表示普通头寸；
get_margincash_close_amount()增加cash_group字段入参；
get_marginsec_open_amount()字段cash_group不入参修改为默认表示普通头寸；
get_marginsec_close_amount()增加cash_group字段入参；
get_margin_entrans_amount()增加cash_group字段入参；
get_enslo_security_info()增加cash_group字段入参；
get_crdt_fund()增加get_crdt_fund接口；
get_margin_contract()新增compact_source合约来源字段入参和返回；
Python3.5新增三方库：memory-profiler==0.61.0, psutil==5.9.5
PTrade1.0-QTV202401.01.000	
set_parameters()新增入参not_restart_trade、server_restart_not_do_before；
委托属性()新增字段:"4"-回购；
PTrade1.0-QTV202401.00.000	
get_margin_contract()entrust_no委托编号字段返回类型改为str类型；
get_margin_contractreal()entrust_no委托编号字段返回类型改为str类型；
get_deliver()返回字段entrust_no,report_no类型由int改为str；
set_benchmark()入参字段security改为sids；
新增check_strategy()检查策略内容；
新增get_dominant_contract()获取期货主力合约；
Python3.5新增三方库：flameprof==0.4, pypinyin==0.50.0
Python3.11新增三方库：pypinyin==0.50.0
PTrade1.0-QTV202301.03.000	
弃用get_individual_transcation()；
弃用get_margin_assert()；
check_limit()新增支持在研究和回测模块使用；
ipo_stocks_order()入参market_type修改为submarket_type；
get_enslo_security_info()出参market_type修改为exchange_type；
get_etf_info()返回参数pre_cash_componet修改为pre_cash_component；
get_fundamentals()入参date(查询日期)新增支持datetime.date类型、新增支持is_dataframe(是否返回DataFrame类型)入参、弃用date_type入参；
get_hks_unit_amount()入参entrust_type修改为trade_type；
set_parameters()不再支持individual_data_in_dict、tick_direction_in_dict入参；
get_individual_entrust()、get_individual_transaction()和get_tick_direction()新增支持is_dict(是否返回字典类型数据)入参；
get_margin_contractreal()出参market_type修改为exchange_type；
get_gear_price()不再支持在回测中调用；
get_stock_status()入参query_type(查询类型)新增支持查询DELISTING_SORTING(是否退市整理期)类型；
get_trades()在期货回测场景下新增返回开平仓类型字段；
新增filter_stock_by_status()过滤指定状态的股票代码；
新增get_current_kline_count()获取股票业务当前时间的分钟bar数量；
新增get_trading_day_by_date()按日期获取指定交易日；
股票Position对象展示字段新增today_amount(今日开仓数量)；
新增三方库：walrus==0.9.3, gqdata==0.1.5, mplfinance==0.12.10b0
新增支持Python3.11版本，可通过终端右上角选择Python版本；
由于Pandas库0.25.0版本后不再支持Panel类型，在Python3.11版本环境中get_fundamentals()按年份查询模式、get_history()、get_individual_entrust()、get_individual_transaction()和get_price()默认返回DataFrame类型；
PTrade1.0-QTV202301.02.000	
get_snapshot()不再返回close_px(今日收盘)、avg_px(均价)字段；
get_price()、get_history()获取日K线新增返回is_open字段；
删除三方库：arch==3.2, cvxopt==1.1.8
新增三方库：PuLP==2.7.0
研究新增支持get_history()获取历史行情；
新增get_business_type()获取当前策略的业务类型；
新增get_ipo_stocks()获取当日IPO申购标的；
PTrade1.0-QTV202301.01.000	
委托流程调整，交易模式中非交易时间段内调用两融、盘后固定价等API产生的委托直接发送柜台进行处理；
Order对象展示字段新增cancel_entrust_no(撤单委托编号)；
期货Position对象去除margin_rate(保证金比例)字段，增加margin(持仓保证金)字段；
run_interval()入参seconds(最小执行周期)由最小3s修改为最小0.1s限制；
get_trades()返回数据中的委托编号字段数据类型统一由int修改为str，成交时间字段格式统一为YYYY-mm-dd HH:MM:SS；
order_market()新增返回order_id(Order订单编号)字段；
margincash_close()、marginsec_close()新增支持market_type(市价委托类型)入参；
get_price()、get_history()新增支持is_dict(是否返回字典类型数据入参)；
新增get_margin_asset()信用资产查询，后续版本将弃用get_margin_assert()；
新增get_individual_transaction()获取逐笔成交行情，后续版本将弃用get_individual_transcation()；
新增get_reits_list()获取基础设施公募REITs基金代码列表；
PTrade1.0-QTV202301.00.000	
get_margincash_open_amount()新增支持cash_group(两融头寸性质)入参；
get_all_orders()新增返回entrust_time(委托时间)字段；
get_open_orders()改成引擎每天收盘后清空对应的未完成订单列表；
新增get_cb_info()获取可转债基础信息；
新增get_enslo_security_info()融券信息查询；
新增get_trend_data()获取集中竞价期间的代码数据；
PBOXQT1.0V202202.03.000	
get_user_name()新增支持login_account(返回当前交易类型对应账号)入参；
debt_to_stock_order()债转股委托新增支持在两融交易中调用；
get_instruments()新增返回changepct_limit (每日涨跌幅度)、littlest_changeunit (最小变动价位)字段；
order_market()和margin_trade()做市价委托上证股票时，limit_price(保护限价)为必传字段；
send_email()单个交易中每分钟调用次数做限制，一分钟最多发送一次；
新增三方库：pykalman==0.9.5
新增get_all_positions()获取全部持仓；
新增get_lucky_info()获取历史中签信息；
新增get_future_main_code()获取主力合约代码；
PBOXQT1.0V202202.02.000	
get_price()、get_history()新增支持获取期货数据；
get_snapshot()新增返回iopv(基金份额参考净值)字段；
handle_data(context, data)中data对象帮助描述由SecurityUnitData修改为BarData，BarData对象新增返回dt(当前周期时间)、preclose(昨收盘价(仅日线返回))、high_limit(涨停价(仅日线返回))、low_limit(跌停价(仅日线返回))、unlimited(是否无涨跌停限制(仅日线返回))字段，字段描述详见接口说明；BarData对象中dt(当前周期时间)字段值由UTC时间修改为北京时间；
on_trade_response()新增返回withdraw_no(撤单原委托号)、cancel_info(废单原因)字段；返回字段值中entrust_no(委托编号)、withdraw_no(撤单原委托号)统一转为str类型；
set_parameters()新增支持individual_data_in_dict(get_individual_entrust()、get_individual_transaction()获取逐笔数据API返回字典类型)、tick_direction_in_dict(get_tick_direction()获取分时成交数据API返回字典类型)参数；
set_yesterday_position()新增支持设置ETF、LOF类型的底仓；
margincash_open()、marginsec_open()新增cash_group(两融头寸性质)入参；
order_market()和margin_trade()做市价委托上证股票时，limit_price(保护限价)为必传字段。
get_index_stocks()由支持多个指数查询修改为仅支持单个指数查询
由于Keras库2.3.1版本与TensorFlow库不兼容，需要降版本：Keras==2.3.1-->Keras==2.2.4。
新增get_frequency()获取当前业务代码的周期；
新增get_underlying_code() 获取代码关联的代码；
PBOXQT1.0V202202.01.000	
委托流程调整，交易模式中非交易时间段内产生的委托直接发送柜台进行处理；
优化tick_data触发逻辑：当策略执行时间超过3s时，将会丢弃中间堵塞的tick_data；在收盘后，将会清空队列中未执行的tick_data；
tick_data中参数data里的快照数据修改为从get_snapshot()中获取，详见注意事项；
修复get_individual_entrust()和get_individual_transaction()中stocks入参代码数量大于50只时返回数据缺失问题；
run_interval()和run_daily()中新增支持get_sort_msg()调用；
get_snapshot()新增返回business_amount_in(内盘成交量)、business_amount_out(外盘成交量)字段；
on_trade_response()新增接收撤单委托的成交主推，详见接口说明注意事项；
get_snapshot()新增返回avg_px(均价)、business_count(成交笔数)、close_px(今收价)、end_trade_date(最后交易日、settlement(结算价)、start_trade_date(首个交易日)、tick_size(最小报价单位)、trade_mins(交易分钟数)字段，去除prod_code(证券代码)字段说明；
新增open_prepared()备兑开仓；
新增close_prepared()备兑平仓；
新增option_exercise()行权；
新增set_parameters()设置策略配置参数，支持的参数详见接口说明；
PBOXQT1.0V202202.00.000	
log新增支持DEBUG级别日志记录；
get_price()、get_history()新增返回preclose(昨收盘价)、high_limit(涨停价)、low_limit(跌停价)、unlimited(是否无涨跌停限制)字段；
get_snapshot()新增返回total_bidqty(委买量)、total_offerqty(委卖量)、total_bid_turnover(委买金额)、total_offer_turnover(委卖金额)字段；
on_trade_response()新增返回order_id(Order订单编号)字段；
当接到策略外交易产生的主推时(需券商配置默认不推送)，由于没有对应的Order对象，on_order_response()、on_trade_response()中order_id字段赋值为""；
tick_data中可调用接口完善；
弃用set_close_position_type()(设置期货平仓方式)、get_close_position_type()(获取期货平仓方式)API接口；
期货Position对象中删除close_position_type(平仓方式)字段；
sell_close()、buy_close()新增close_today(平仓方式)入参；
run_daily()、run_interval()可以在initialize中多次调用，累计不可超过5次，详见接口说明注意事项；
新增get_MACD()异同移动平均线；
新增get_KDJ()随机指标；
新增get_RSI()相对强弱指标；
新增get_CCI()顺势指标；
新增create_dir()创建文件目录路径；
PBOXQT1.0V202201.02.000	
get_snapshot新增issue_date字段说明；
PBOXQT1.0V202201.01.000	
修复委托状态类型不一致问题，get_orders()、get_all_orders()以及Order对象中的委托状态字段数据类型从int统一为str；
新增get_trade_name()获取交易名称；
tick_data中可调用接口完善；
研究中get_stock_name()、get_stock_info()新增支持获取可转债、ETF、LOF品种；
get_history()新增fill(填充类型)入参；
get_price()、get_history()新增支持：5分钟(5m)、15分钟(15m)、30分钟(30m)、60分钟(60m)、120分钟(120m)频率行情获取；
PBOXQT1.0V202201.00.000	
get_individual_transaction()新增返回buy_no(叫买方编号)、sell_no(叫卖方编号)、trans_flag(成交标记)、trans_identify_am(盘后逐笔成交序号标识)、channel_num(成交通道信息)字段；
get_margin_contract()新增返回compact_interest(合约利息金额)、real_compact_interest(日间实时利息金额)、real_compact_balance(日间实时合约金额)、real_compact_amount(日间实时合约数量)字段；
get_price()、get_history()新增支持：1月(mo)、1季度(1q)、1年(1y)频率行情获取；
set_commission()中type字段新增支持传入"LOF"类型；
get_individual_entrust()和get_individual_transaction()返回内容中hq_px字段值缩小1000倍，返回为真实价格；
set_commission()增加type=“LOF”类型基金费率设置的功能；
新增支持期货日盘回测功能、期货日盘交易功能(对接UFT柜台)，期货API接口详见量化帮助文档期货专用函数模块；
新增get_tick_direction()获取分时成交行情；
新增get_sort_msg()获取版块、行业的涨幅排名；
新增permission_test()权限校验；
PBOXQT1.0V202101.09.000	
get_market_detail()限制仅before_trading_start和after_trading_end中使用；
get_market_list()限制仅before_trading_start和after_trading_end中使用；
get_snapshot()新增返回hsTimeStamp(快照时间戳)字段；对接L2行情买卖一档新增返回委托队列；
ipo_stocks_order()新增black_stocks(新股/债黑名单)入参；
on_order_response()新增返回error_info(错误信息)字段；
PBOXQT1.0V202101.08.000	
initialize对部分API接口调用进行限制，仅initialize可调用接口说明中的API可在initialize函数内使用；
before_trading_start和after_trading_end对两融委托API接口调用进行限制；
修复仅单笔成交订单时调用get_trades()返回格式有误问题；
修复交易场景中获取当日K线14:58、14:59分价格为0的问题；
send_email()发送邮件信息新增path(附件路径)、subject(邮件主题)入参；
新增get_cb_list()获取可转债列表；
新增get_deliver()获取历史交割单信息；
新增get_fundjour()获取历史资金流水信息；
新增get_research_path()获取研究路径；
get_market_detail()新增支持在回测、交易场景中调用；
PBOXQT1.0V202101.07.000	
get_snapshot()新增wavg_px(加权平均价)、px_change_rate(涨跌幅)出参；
可转债回测业务新增支持T+0；
新增支持融资融券回测业务，融资融券专用函数中暂只支持margin_trade()接口；
PBOXQT1.0V202101.06.000	
新增get_user_name()API接口，用于获取登录终端的资金账号；
研究中get_price()新增支持获取周线数据；
get_snapshot()新增支持获取XBHS行业版块市场数据；
send_qywx()新增toparty(发送对象为部门)、touser(发送内容为个人)、totag(发送内容为分组)入参；
PBOXQT1.0V202101.05.000	
信用账户支持ipo_stocks_order()接口调用；
由于行情源返回信息不包含，get_fundamentals()获取growth_ability、profit_ability、eps、operating_ability、debt_paying_ability表不再返回company_type字段；
由于上交所债券业务规则变更，调用debt_to_stock_order()接口对上海市场可转债进行转股操作时需传入可转债代码，不再传入转股代码；
PBOXQT1.0V202101.04.000	
修复get_all_orders()获取特定委托状态报错问题，status字段返回数据类型从int改为str；
on_order_response()、on_trade_response()支持获取非本策略交易的主推信息(需券商配置默认不推送)，且on_order_response推送非本策略交易的主推信息时不包含order_id字段；
相关功能优化；
PBOXQT1.0V202101.03.000	
on_order_response()主推信息中新增entrust_type、entrust_prop字段；
修复信用交易接口兼容问题；
get_price()、get_history()支持周频(1w)行情获取；
由于行情源不再更新维护，get_fundamentals()接口去除share_change表；
'''
############################### 策略例子
'''
策略示例
股票策略示例
集合竞价追涨停策略
策略说明
设置股票池，每天9:23分运行集合竞价处理函数：如果最新价不小于涨停价则买入

示例
def initialize(context):
    # 初始化此策略
    # 设置股票池, 这里我们只操作一支股票
    g.security = '600570.SS'
    set_universe(g.security)
    #每天9:23分运行集合竞价处理函数
    run_daily(context, aggregate_auction_func, time='9:23')

def aggregate_auction_func(context):
    stock = g.security
    # 获取最新价
    snapshot = get_snapshot(stock)
    price = snapshot[stock]['last_px']
    # 获取涨停价
    up_limit = snapshot[stock]['up_px']
    # 如果最新价不小于涨停价则买入
    if float(price) >= float(up_limit):
        order(g.security, 100, limit_price=up_limit)

def handle_data(context, data):
    pass
tick级别均线策略
策略说明
设置股票池，盘前准备历史数据，每3秒钟触发一次：首先用最新的tick行情数据计算五日均线和十日均线，然后进行比较：当五日均线高于十日均线时买入，当五日均线低于十日均线时卖出

示例
def initialize(context):
    # 初始化此策略
    # 设置股票池, 这里我们只操作一支股票
    g.security = '600570.SS'
    set_universe(g.security)
    # 每3秒运行一次主函数
    run_interval(context, func, seconds=3)

# 盘前准备历史数据
def before_trading_start(context, data):
    history = get_history(10, '1d', 'close', g.security, fq='pre', include=False)
    g.close_array = history['close'].values

# 当五日均线高于十日均线时买入，当五日均线低于十日均线时卖出
def func(context):

    stock = g.security

    # 获取最新价
    snapshot = get_snapshot(stock)
    price = snapshot[stock]['last_px']

    # 获取五日均线价格
    days = 5
    ma5 = get_MA_day(stock, days, g.close_array[-4:], price)
    # 获取十日均线价格
    days = 10
    ma10 = get_MA_day(stock, days, g.close_array[-9:], price)

    # 获取当前资金余额
    cash = context.portfolio.cash

    # 如果当前有余额，并且五日均线大于十日均线则买入
    if ma5 > ma10:
        # 用所有 cash 买入股票
        order_value(stock, cash)
        # 记录这次买入
        log.info("Buying %s" % (stock))

    # 如果五日均线小于十日均线，并且目前有头寸，则全部卖出
    elif ma5 < ma10 and get_position(stock).amount > 0:
        # 全部卖出
        order_target(stock, 0)
        # 记录这次卖出
        log.info("Selling %s" % (stock))

# 计算实时均线函数
def get_MA_day(stock,days,close_array,current_price):
    close_sum = close_array[-(days-1):].sum()
    MA = (current_price + close_sum)/days
    return MA

def handle_data(context, data):
    pass
双均线策略
策略说明
设置股票池，每个handle_data周期进行如下判断处理：当五日均线高于十日均线时买入，当五日均线低于十日均线时卖出

示例
def initialize(context):
    # 初始化此策略
    # 设置股票池, 这里我们只操作一支股票
    g.security = '600570.SS'
    set_universe(g.security)

# 当五日均线高于十日均线时买入，当五日均线低于十日均线时卖出
def handle_data(context, data):
    security = g.security

    # 获取十日历史价格
    df = get_history(10, '1d', 'close', security, fq=None, include=False)

    # 获取五日均线价格
    ma5 = round(df['close'][-5:].mean(), 3)

    # 获取十日均线价格
    ma10 = round(df['close'][-10:].mean(), 3)

    # 获取昨天收盘价
    price = data[security]['close']

    # 获取当前资金余额
    cash = context.portfolio.cash

    # 如果当前有余额，并且五日均线大于十日均线
    if ma5 > ma10:
        # 用所有 cash 买入股票
        order_value(security, cash)
        # 记录这次买入
        log.info("Buying %s" % (security))

    # 如果五日均线小于十日均线，并且目前有头寸
    elif ma5 < ma10 and get_position(security).amount > 0:
        # 全部卖出
        order_target(security, 0)
        # 记录这次卖出
        log.info("Selling %s" % (security))
macd策略
策略说明
用历史日K线数据计算MACD指标，以计算结果进行买入卖出交易。

示例
"""
macd强势金叉买入、macd弱势死叉卖出
"""
def initialize(context):
    g.hold_num = 10

def before_trading_start(context, data):
    # 获取沪深300股票
    g.security_list = get_index_stocks('000300.SS')
    g.close_data_dict = {}
    # 获取K线数据
    history = get_history(100, frequency='1d', field=["close"], security_list=g.security_list, fq='dypre',
                             include=False, is_dict=True)
    for stock in g.security_list:
        close_data = history[stock]['close']
        g.close_data_dict[stock] = close_data
    g.every_value = context.portfolio.portfolio_value / g.hold_num

def handle_data(context, data):

    for security in g.security_list:
        close_data = g.close_data_dict[security]
        macdDIF_data, macdDEA_data, macd_data = get_MACD(close_data, 12, 26, 9)
        DIF = macdDIF_data[-1]
        DEA = macdDEA_data[-1]
        macd_current = macd_data[-1]
        macd_pre = macd_data[-2]

        # 获取当前价格
        current_price = data[security].price
        # 获取当前的现金
        position = context.portfolio.positions
        # DIF、DEA均为正，macd金叉，买入信号参考
        if position[security].amount == 0:
            if DIF > 0 and DEA > 0 and macd_pre < 0 and macd_current >= 0:
                if context.portfolio.cash < g.every_value*0.8:
                    continue

                # 以市单价买入股票，日回测时即是开盘价
                order_target_value(security, g.every_value)
                # 记录这次买入
                log.info("Buying %s" % (security))
        else:
            # DIF、DEA均为负，macd死叉，卖出信号参考
            if DIF < 0 and DEA < 0 and macd_pre >= 0 and macd_current < 0:
                # 卖出所有股票,使这只股票的最终持有量为0
                order_target(security, 0)
                # 记录这次卖出
                log.info("Selling %s" % (security))
两融策略示例
融资融券双均线策略
策略说明
设置标的池，每个handle_data周期进行如下判断处理：当五日均线高于十日均线时买入，当五日均线低于十日均线时卖出。其中买入卖出所调用的API为融资融券业务专用API。

示例
def initialize(context):
    # 初始化策略
    # 设置股票池, 这里我们只操作一支股票
    g.security = "600570.SS"
    set_universe(g.security)

def before_trading_start(context, data):
    # 买入标识
    g.order_buy_flag = False
    # 卖出标识
    g.order_sell_flag = False

# 当五日均线高于十日均线时买入，当五日均线低于十日均线时卖出
def handle_data(context, data):
    # 获取十日历史价格
    df = get_history(10, "1d", "close", g.security, fq=None, include=False)
    # 获取五日均线价格
    ma5 = round(df["close"][-5:].mean(), 3)
    # 获取十日均线价格
    ma10 = round(df["close"][-10:].mean(), 3)
    # 获取昨天收盘价
    price = data[g.security]["close"]
    # 如果五日均线大于十日均线
    if ma5 > ma10:
        if not g.order_buy_flag:
            # 获取最大可融资数量
            amount = get_margincash_open_amount(g.security).get(g.security)
            # 进行融资买入操作
            margincash_open(g.security, amount)
            # 记录这次操作
            log.info("Buying %s Amount %s" % (g.security, amount))
            # 当日已融资买入
            g.order_buy_flag = True

    # 如果五日均线小于十日均线，并且目前有头寸
    elif ma5 < ma10 and get_position(g.security).amount > 0:
        if not g.order_sell_flag:
            # 获取标的卖券还款最大可卖数量
            amount = get_margincash_close_amount(g.security).get(g.security)
            # 进行卖券还款操作
            margincash_close(g.security, -amount)
            # 记录这次操作
            log.info("Selling %s Amount %s" % (g.security, amount))
            # 当日已卖券还款
            g.order_sell_flag = True
'''
# 财务数据的API接口说明
valuation-估值数据
接口说明
get_fundamentals(security, 'valuation', fields=None, date=None)
注意事项：

一、该接口只支持按天查询模式，返回查询日期对应股票相关数据。查询此表不支持输入的参数有：start_year, end_year, report_types, date_type, merge_type。

二、换手率（turnover_rate）和滚动股息率（dividend_ratio）两个字段数据源返回的是带%的字符串。比如turnover_rate：20%，用户需要自行转换成0.2的float格式。

关于date字段的说明

场景一：date字段不入参。回测中默认是获取context.blotter.current_dt交易日收盘后更新的数据，因此会产生未来函数，交易和研究会返回当日数据，若在盘中时间由于数据未更新将返回字段为NAN的数据，因此建议获取最新数据的场景都使用date参数入参上一个交易日日期。

场景二：date字段入参日期。回测和交易中若date为非交易日，将返回字段为NAN的数据；研究中若date为非交易日，将返回往前最近一个交易日的数据，注意回测和交易中是可以取到未来的数据，需要规避。


               turnover_rate     pb    total_value   trading_day    pe_dynamic
secu_code
600570.SS         4.20%        11.89   3.748224e+10   2018-04-24      163.38
000001.SZ         0.86%         0.91   2.036411e+11   2018-04-24        7.72
示例
# 获取股票池
stocks = get_index_stocks('000906.XBHS')
# 指定股票池
stocks = ['600570.SS','000001.SZ']

# 获取估值数据，默认会返回context.blotter.current_dt前一交易日的数据(在实际生活中，我们只能看到前一交易日的估值数据)。仅在回测中返回前一交易日的估值数据，在研究和交易中返回当前时间的估值数据。
get_fundamentals(stocks, 'valuation')

#获取股票池中对应上市公司2018年04月10日前一交易日的市净率
get_fundamentals(stocks, 'valuation', date = '20180410', fields = 'pb')

# 获取股票池中对应上市公司2018年04月24日前一交易日的A股总市值(元)、动态市盈率、换手率和市净率数据
get_fundamentals(stocks, 'valuation', date = '2018-04-24', fields = ['total_value', 'pe_dynamic', 'turnover_rate', 'pb'])
表数据具体字段
估值数据 - valuation
字段名称	字段类型	字段说明	属性
trading_day	str	交易日期	固定返回
total_value	float	A股总市值(元)	固定返回
float_value	float	A股流通市值(元)	自选返回
naps	float	每股净资产/(元/股)	自选返回
pcf	float	市现率	自选返回
secu_abbr	str	证券简称	自选返回
secu_code	str	证券代码	固定返回
ps	float	市销率PS	自选返回
ps_ttm	float	市销率PS(TTM)	自选返回
pe_ttm	float	市盈率PE(TTM)	自选返回
a_shares	float	A股股本	自选返回
a_floats	float	可流通A股	自选返回
pe_dynamic	float	动态市盈率	自选返回
pe_static	float	静态市盈率	自选返回
b_floats	float	可流通B股	自选返回
b_shares	float	B股股本	自选返回
h_shares	float	H股股本	自选返回
total_shares	float	总股本	自选返回
turnover_rate	float	换手率	自选返回
dividend_ratio	float	滚动股息率	自选返回
pb	float	市净率	自选返回
roe	float	净资产收益率	自选返回
balance_statement-资产负债表
接口说明
get_fundamentals(security, 'balance_statement',fields, date = None, start_year = None, end_year = None, report_types = None, date_type = None, merge_type = None)

               company_type   publ_date   secu_abbr    total_assets
end_date
2013-03-31            1       2013-04-19   恒生电子     1.76795e+09
2014-03-31            1       2014-04-29   恒生电子     2.20999e+09
2015-03-31            1       2015-04-25   恒生电子     3.09674e+09
示例
# 获取数据的两种模式
# 1. 按日期查询模式（默认以发布日期为参考时间）：返回输入日期之前对应的财务数据
# 在回测中获取单一股票中对应回测日期资产负债表中资产总计（total_assets）数据
get_fundamentals('600570.SS','balance_statement','total_assets','20160628')

# 2. 按年份查询模式：返回输入年份范围内对应季度的财务数据
# 获取恒生电子(600570.SS)从2013年至2015年第一季度资产负债表中资产总计
#（total_assets）数据
get_fundamentals('600570.SS','balance_statement','total_assets',start_year='2013',end_year='2015', report_types='1')
表数据具体字段
资产负债表 - balance_statement
字段名称	字段类型	字段说明
secu_code	str	股票代码
secu_abbr	str	股票简称
company_type	str	公司类型
end_date	str	截止日期
publ_date	str	公告日期
settlement_provi	numpy.float64	结算备付金
client_provi	numpy.float64	客户备付金
deposit_in_interbank	numpy.float64	存放同业款项
r_metal	numpy.float64	贵金属
lend_capital	numpy.float64	拆出资金
derivative_assets	numpy.float64	衍生金融资产
bought_sellback_assets	numpy.float64	买入返售金融资产
loan_and_advance	numpy.float64	发放贷款和垫款
insurance_receivables	numpy.float64	应收保费
receivable_subrogation_fee	numpy.float64	应收代位追偿款
reinsurance_receivables	numpy.float64	应收分保账款
receivable_unearned_r	numpy.float64	应收分保未到期责任准备金
receivable_claims_r	numpy.float64	应收分保未决赔款准备金
receivable_life_r	numpy.float64	应收分保寿险责任准备金
receivable_lt_health_r	numpy.float64	应收分保长期健康险责任准备金
insurer_impawn_loan	numpy.float64	保户质押贷款
fixed_deposit	numpy.float64	定期存款
refundable_capital_deposit	numpy.float64	存出资本保证金
refundable_deposit	numpy.float64	存出保证金
independence_account_assets	numpy.float64	独立账户资产
other_assets	numpy.float64	其他资产
borrowing_from_centralbank	numpy.float64	向中央银行借款
deposit_of_interbank	numpy.float64	同业及其他金融机构存放款项
borrowing_capital	numpy.float64	拆入资金
derivative_liability	numpy.float64	衍生金融负债
sold_buyback_secu_proceeds	numpy.float64	卖出回购金融资产款
deposit	numpy.float64	吸收存款
proxy_secu_proceeds	numpy.float64	代理买卖证券款
sub_issue_secu_proceeds	numpy.float64	代理承销证券款
deposits_received	numpy.float64	存入保证金
advance_insurance	numpy.float64	预收保费
commission_payable	numpy.float64	应付手续费及佣金
reinsurance_payables	numpy.float64	应付分保账款
compensation_payable	numpy.float64	应付赔付款
policy_dividend_payable	numpy.float64	应付保单红利
insurer_deposit_investment	numpy.float64	保户储金及投资款
unearned_premium_reserve	numpy.float64	未到期责任准备金
outstanding_claim_reserve	numpy.float64	未决赔款准备金
life_insurance_reserve	numpy.float64	寿险责任准备金
lt_health_insurance_lr	numpy.float64	长期健康险责任准备金
independence_liability	numpy.float64	独立账户负债
other_liability	numpy.float64	其他负债
cash_equivalents	numpy.float64	货币资金
client_deposit	numpy.float64	客户资金存款
trading_assets	numpy.float64	交易性金融资产
bill_receivable	numpy.float64	应收票据
dividend_receivable	numpy.float64	应收股利
interest_receivable	numpy.float64	应收利息
account_receivable	numpy.float64	应收账款
other_receivable	numpy.float64	其他应收款
advance_payment	numpy.float64	预付款项
inventories	numpy.float64	存货
non_current_asset_in_one_year	numpy.float64	一年内到期的非流动资产
other_current_assets	numpy.float64	其他流动资产
total_current_assets	numpy.float64	流动资产合计
shortterm_loan	numpy.float64	短期借款
impawned_loan	numpy.float64	质押借款
trading_liability	numpy.float64	交易性金融负债
notes_payable	numpy.float64	应付票据
accounts_payable	numpy.float64	应付账款
advance_receipts	numpy.float64	预收款项
salaries_payable	numpy.float64	应付职工薪酬
dividend_payable	numpy.float64	应付股利
taxs_payable	numpy.float64	应交税费
interest_payable	numpy.float64	应付利息
other_payable	numpy.float64	其他应付款
non_current_liability_in_one_year	numpy.float64	一年内到期的非流动负债
other_current_liability	numpy.float64	其他流动负债
total_current_liability	numpy.float64	流动负债合计
hold_for_sale_assets	numpy.float64	可供出售金融资产
hold_to_maturity_investments	numpy.float64	持有至到期投资
investment_property	numpy.float64	投资性房地产
longterm_equity_invest	numpy.float64	长期股权投资
longterm_receivable_account	numpy.float64	长期应收款
fixed_assets	numpy.float64	固定资产
construction_materials	numpy.float64	工程物资
constru_in_process	numpy.float64	在建工程
fixed_assets_liquidation	numpy.float64	固定资产清理
biological_assets	numpy.float64	生产性生物资产
oil_gas_assets	numpy.float64	油气资产
intangible_assets	numpy.float64	无形资产
seat_costs	numpy.float64	交易席位费
development_expenditure	numpy.float64	开发支出
good_will	numpy.float64	商誉
long_deferred_expense	numpy.float64	长期待摊费用
deferred_tax_assets	numpy.float64	递延所得税资产
other_non_current_assets	numpy.float64	其他非流动资产
total_non_current_assets	numpy.float64	非流动资产合计
longterm_loan	numpy.float64	长期借款
bonds_payable	numpy.float64	应付债券
longterm_account_payable	numpy.float64	长期应付款
long_salaries_pay	numpy.float64	长期应付职工薪酬
specific_account_payable	numpy.float64	专项应付款
estimate_liability	numpy.float64	预计负债
deferred_tax_liability	numpy.float64	递延所得税负债
long_defer_income	numpy.float64	长期递延收益
other_non_current_liability	numpy.float64	其他非流动负债
total_non_current_liability	numpy.float64	非流动负债合计
paidin_capital	numpy.float64	实收资本（或股本）
other_equityinstruments	numpy.float64	其他权益工具
capital_reserve_fund	numpy.float64	资本公积
surplus_reserve_fund	numpy.float64	盈余公积
retained_profit	numpy.float64	未分配利润
treasury_stock	numpy.float64	减：库存股
other_composite_income	numpy.float64	其他综合收益
ordinary_risk_reserve_fund	numpy.float64	一般风险准备
foreign_currency_report_conv_diff	numpy.float64	外币报表折算差额
specific_reserves	numpy.float64	专项储备
se_without_mi	numpy.float64	归属母公司股东权益合计
minority_interests	numpy.float64	少数股东权益
total_shareholder_equity	numpy.float64	所有者权益合计
total_liability_and_equity	numpy.float64	负债和权益总计
total_assets	numpy.float64	资产总计
total_liability	numpy.float64	负债总计
contract_liability	numpy.float64	合同负债
total_fixed_asset	numpy.float64	固定资产合计
t_constru_in_process	numpy.float64	在建工程合计
income_statement-利润表
接口说明
get_fundamentals(security, 'income_statement',fields, date = None, start_year = None, end_year = None, report_types = None, date_type = None, merge_type = None)

                company_type   net_profit   publ_date      secu_abbr
end_date
2013-03-31            1        3.71658e+07  2013-04-19      恒生电子
2014-03-31            1        5.38395e+07  2014-04-29      恒生电子
2015-03-31            1           7.22e+07  2015-04-25      恒生电子
示例
# 获取数据的两种模式
# 1. 按日期查询模式（默认以发布日期为参考时间）：返回输入日期之前对应的财务数据
# 在回测中获取单一股票中对应回测日期第一季度利润表中净利润（net_profit）数据
get_fundamentals('600570.SS','income_statement','net_profit','20160628')

# 2. 按年份查询模式：返回输入年份范围内对应季度的财务数据
# 获取恒生电子(600570.SS)从2013年至2015年第一季度利润表中净利润（net_profit）# 数据
get_fundamentals('600570.SS','income_statement','net_profit',start_year='2013',end_year='2015', report_types='1')
表数据具体字段
利润表 - income_statement
字段名称	字段类型	字段说明
secu_code	str	股票代码
secu_abbr	str	股票简称
company_type	str	公司类型
end_date	str	截止日期
publ_date	str	公告日期
basic_eps	numpy.float64	基本每股收益
diluted_eps	numpy.float64	稀释每股收益
net_profit	numpy.float64	净利润
np_parent_company_owners	numpy.float64	归属于母公司所有者的净利润
minority_profit	numpy.float64	少数股东损益
total_operating_cost	numpy.float64	营业总成本
operating_payout	numpy.float64	营业支出
refunded_premiums	numpy.float64	退保金
compensation_expense	numpy.float64	赔付支出
amortization_expense	numpy.float64	减:摊回赔付支出
premium_reserve	numpy.float64	提取保险责任准备金
amortization_premium_reserve	numpy.float64	减:摊回保险责任准备金
policy_dividend_payout	numpy.float64	保单红利支出
reinsurance_cost	numpy.float64	分保费用
amortization_reinsurance_cost	numpy.float64	减:摊回分保费用
insurance_commission_expense	numpy.float64	保险手续费及佣金支出
other_operating_cost	numpy.float64	其他营业成本
operating_cost	numpy.float64	营业成本
operating_tax_surcharges	numpy.float64	营业税金及附加
operating_expense	numpy.float64	销售费用
administration_expense	numpy.float64	管理费用
financial_expense	numpy.float64	财务费用
asset_impairment_loss	numpy.float64	资产减值损失
operating_profit	numpy.float64	营业利润
non_operating_income	numpy.float64	加：营业收入
non_operating_expense	numpy.float64	减：营业外支出
non_current_assetss_deal_loss	numpy.float64	其中：非流动资产处置净损失
total_operating_revenue	numpy.float64	营业总收入
operating_revenue	numpy.float64	营业收入
net_interest_income	numpy.float64	利息净收入
interest_income	numpy.float64	其中：利息收入
interest_expense	numpy.float64	其中:利息支出
net_commission_income	numpy.float64	手续费及佣金净收入
commission_income	numpy.float64	其中：手续费及佣金收入
commission_expense	numpy.float64	其中：手续费及佣金支出
net_proxy_secu_income	numpy.float64	其中：代理买卖证券业务净收入
net_subissue_secu_income	numpy.float64	其中：证券承销业务净收入
net_trust_income	numpy.float64	其中:受托客户资产管理业务净收入
premiums_earned	numpy.float64	已赚保费
premiums_income	numpy.float64	保险业务收入
reinsurance_income	numpy.float64	其中：分保费收入
reinsurance	numpy.float64	减：分出保费
unearned_premium_reserve	numpy.float64	提取未到期责任准备金
other_operating_revenue	numpy.float64	其他营业收入
other_net_revenue	numpy.float64	非营业性收入
fair_value_change_income	numpy.float64	公允价值变动净收益
invest_income	numpy.float64	投资净收益
invest_income_associates	numpy.float64	其中:对联营合营企业的投资收益
exchange_income	numpy.float64	汇兑收益
total_profit	numpy.float64	利润总额
income_tax_cost	numpy.float64	减：所得税费用
total_composite_income	numpy.float64	综合收益总额
ci_parent_company_owners	numpy.float64	归属于母公司所有者的综合收益总额
ci_minority_owners	numpy.float64	归属于少数股东的综合收益总额
r_and_d	numpy.float64	研发费用
cashflow_statement-现金流量表
接口说明
get_fundamentals(security,'cashflow_statement',fields, date = None, start_year = None, end_year = None, report_types = None, date_type = None, merge_type = None)

               company_type invest_cash_paid   publ_date      secu_abbr
end_date
2013-03-31            1        5.271e+08       2013-04-19      恒生电子
2014-03-31            1       3.9488e+08       2014-04-29      恒生电子
2015-03-31            1      9.92432e+08       2015-04-25      恒生电子
示例
# 获取数据的两种模式
# 1. 按日期查询模式（默认以发布日期为参考时间）：返回输入日期之前对应的财务数据
# 在回测中获取单一股票中对应回测日期第一季度现金流量表中投资支付的现金
#（invest_cash_paid）数据
get_fundamentals('600570.SS','cashflow_statement','invest_cash_paid','20160628')

# 2. 按年份查询模式：返回输入年份范围内对应季度的财务数据
# 获取恒生电子(600570.SS)从2013年至2015年第一季度现金流量表中投资支付的现金#（invest_cash_paid）数据
get_fundamentals('600570.SS','cashflow_statement','invest_cash_paid',start_year='2013',end_year='2015', report_types='1')
表数据具体字段
现金流量表 - cashflow_statement
字段名称	字段类型	字段说明
secu_code	str	股票代码
secu_abbr	str	股票简称
company_type	str	公司类型
end_date	str	截止日期
publ_date	str	公告日期
goods_sale_service_render_cash	numpy.float64	销售商品、提供劳务收到的现金
tax_levy_refund	numpy.float64	收到的税费返还
net_deposit_increase	numpy.float64	客户存款和同业存放款项净增加额
net_borrowing_from_central_bank	numpy.float64	向中央银行借款净增加额
net_borrowing_from_finance_co	numpy.float64	向其他金融机构拆入资金净增加额
interest_and_commission_cashin	numpy.float64	收取利息、手续费及佣金的现金
net_deal_trading_assets	numpy.float64	处置交易性金融资产净增加额
net_buyback	numpy.float64	回购业务资金净增加额
net_original_insurance_cash	numpy.float64	收到原保险合同保费取得的现金
net_reinsurance_cash	numpy.float64	收到再保业务现金净额
net_insurer_deposit_investment	numpy.float64	保户储金及投资款净增加额
other_cashin_related_operate	numpy.float64	收到其他与经营活动有关的现金
subtotal_operate_cash_inflow	numpy.float64	经营活动现金流入小计
goods_and_services_cash_paid	numpy.float64	购买商品、接受劳务支付的现金
staff_behalf_paid	numpy.float64	支付给职工以及为职工支付的现金
all_taxes_paid	numpy.float64	支付的各项税费
net_loan_and_advance_increase	numpy.float64	客户贷款及垫款净增加额
net_deposit_in_cb_and_ib	numpy.float64	存放中央银行和同业款项净增加额
net_lend_capital	numpy.float64	拆出资金净增加额
commission_cash_paid	numpy.float64	支付手续费及佣金的现金
original_compensation_paid	numpy.float64	支付原保险合同赔付款项的现金
net_cash_for_reinsurance	numpy.float64	支付再保业务现金净额
policy_dividend_cash_paid	numpy.float64	支付保单红利的现金
other_operate_cash_paid	numpy.float64	支付其他与经营活动有关的现金
subtotal_operate_cash_outflow	numpy.float64	经营活动现金流出小计
net_operate_cash_flow	numpy.float64	经营活动产生的现金流量净额
invest_withdrawal_cash	numpy.float64	收回投资收到的现金
invest_proceeds	numpy.float64	取得投资收益收到的现金
fix_intan_other_asset_dispo_cash	numpy.float64	处置固定资产、无形资产和其他长期资产收回的现金净额
net_cash_deal_sub_company	numpy.float64	处置子公司及其他营业单位收到的现金净额
other_cash_from_invest_act	numpy.float64	收到其他与投资活动有关的现金
subtotal_invest_cash_inflow	numpy.float64	投资活动现金流入小计
fix_intan_other_asset_acqui_cash	numpy.float64	购建固定资产、无形资产和其他长期资产支付的现金
invest_cash_paid	numpy.float64	投资支付的现金
net_cash_from_sub_company	numpy.float64	取得子公司及其他营业单位支付的现金净额
impawned_loan_net_increase	numpy.float64	质押贷款净增加额
other_cash_to_invest_act	numpy.float64	支付其他与投资活动有关的现金
subtotal_invest_cash_outflow	numpy.float64	投资活动现金流出小计
net_invest_cash_flow	numpy.float64	投资活动产生的现金流量净额
cash_from_invest	numpy.float64	吸收投资收到的现金
cash_from_bonds_issue	numpy.float64	发行债券收到的现金
cash_from_borrowing	numpy.float64	取得借款收到的现金
other_finance_act_cash	numpy.float64	收到其他与筹资活动有关的现金
subtotal_finance_cash_inflow	numpy.float64	筹资活动现金流入小计
borrowing_repayment	numpy.float64	偿还债务支付的现金
dividend_interest_payment	numpy.float64	分配股利、利润或偿付利息支付的现金
other_finance_act_payment	numpy.float64	支付其他与筹资活动有关的现金
subtotal_finance_cash_outflow	numpy.float64	筹资活动现金流出小计
net_finance_cash_flow	numpy.float64	筹资活动产生的现金流量净额
exchan_rate_change_effect	numpy.float64	汇率变动对现金及现金等价物的影响
cash_equivalent_increase	numpy.float64	现金及现金等价物净增加额
begin_period_cash	numpy.float64	加：期初现金及现金等价物余额
end_period_cash_equivalent	numpy.float64	期末现金及现金等价物余额
net_profit	numpy.float64	净利润
minority_profit	numpy.float64	加:少数股东损益
assets_depreciation_reserves	numpy.float64	加:资产减值准备
fixed_asset_depreciation	numpy.float64	固定资产折旧
intangible_asset_amortization	numpy.float64	收无形资产摊销
deferred_expense_amort	numpy.float64	长期待摊费用摊销
deferred_expense_decreased	numpy.float64	待摊费用减少(减:增加)
accrued_expense_added	numpy.float64	预提费用增加(减:减少)
fix_intanther_asset_dispo_loss	numpy.float64	处置固定资产、无形资产和其他长期资产的损失
fixed_asset_scrap_loss	numpy.float64	固定资产报废损失
loss_from_fair_value_changes	numpy.float64	公允价值变动损失
financial_expense	numpy.float64	财务费用
invest_loss	numpy.float64	投资损失
defered_tax_asset_decrease	numpy.float64	递延所得税资产减少
defered_tax_liability_increase	numpy.float64	递延所得税负债增加
inventory_decrease	numpy.float64	存货的减少
operate_receivable_decrease	numpy.float64	经营性应收项目的减少
operate_payable_increase	numpy.float64	经营性应付项目的增加
others	numpy.float64	其他
net_operate_cash_flow_notes	numpy.float64	经营活动产生的现金流量净额
debt_to_captical	numpy.float64	债务转为资本
cbs_expiring_within_one_year	numpy.float64	一年内到期的可转换公司债券
fixed_assets_finance_leases	numpy.float64	融资租入固定资产
cash_at_end_of_year	numpy.float64	现金的期末余额
cash_at_beginning_of_year	numpy.float64	减:现金的期初余额
cash_equivalents_at_end_of_year	numpy.float64	加:现金等价物的期末余额
cash_equivalents_at_beginning	numpy.float64	减:现金等价物的期初余额
net_incr_in_cash_and_equivalents	numpy.float64	现金及现金等价物净增加额
growth_ability-成长能力
接口说明
get_fundamentals(security,'growth_ability',fields, date = None, start_year = None, end_year = None, report_types = None, date_type = None)

               oper_profit_grow_rate   publ_date      secu_abbr
end_date
2013-03-31               124.705       2013-04-19      恒生电子
2014-03-31                9.1946       2014-04-29      恒生电子
2015-03-31               14.2251       2015-04-25      恒生电子
注意: 获取此表中数据，不支持输入的参数有：merge_type

示例
# 获取数据的两种模式
# 1. 按日期查询模式（默认以发布日期为参考时间）：返回输入日期之前对应的财务数据
# 在回测中获取单一股票中对应回测日期第一季度成长能力指标中营业利润同比增长
#（oper_profit_grow_rate）数据
get_fundamentals('600570.SS','growth_ability','oper_profit_grow_rate','20160628')

# 2. 按年份查询模式：返回输入年份范围内对应季度的财务数据
# 获取恒生电子(600570.SS)从2013年至2015年第一季度成长能力指标中营业利润同比# 增长（oper_profit_grow_rate）数据
get_fundamentals('600570.SS','growth_ability','oper_profit_grow_rate',start_year='2013',end_year='2015', report_types='1')
表数据具体字段
成长能力- growth_ability
字段名称	字段类型	字段说明	属性
secu_code	str	股票代码	固定返回
secu_abbr	str	股票简称	固定返回
publ_date	str	公告日期	固定返回
end_date	str	截止日期	固定返回
basic_eps_yoy	numpy.float64	基本每股收益同比增长（%）	自选返回
diluted_eps_yoy	numpy.float64	稀释每股收益同比增长（%）	自选返回
operating_revenue_grow_rate	numpy.float64	营业收入同比增长（%）	自选返回
np_parent_company_yoy	numpy.float64	归属母公司股东的净利润同比增长（%）	自选返回
net_operate_cash_flow_yoy	numpy.float64	经营活动产生的现金流量净额同比增长（%）	自选返回
oper_profit_grow_rate	numpy.float64	营业利润同比增长（%）	自选返回
total_profit_grow_rate	numpy.float64	利润总额同比增长（%）	自选返回
eps_grow_rate_ytd	numpy.float64	每股净资产相对年初增长率（%）	自选返回
se_without_mi_grow_rate_ytd	numpy.float64	归属母公司股东的权益相对年初增长率（%）	自选返回
ta_grow_rate_ytd	numpy.float64	资产总计相对年初增长率（%)	自选返回
np_parent_company_cut_yoy	numpy.float64	归属母公司股东的净利润(扣除)同比增长（%）	自选返回
avg_np_yoy_past_five_year	numpy.float64	过去五年同期归属母公司净利润平均增幅（%）	自选返回
oper_cash_ps_grow_rate	numpy.float64	每股经营活动产生的现金流量净额同比增长（%）	自选返回
naor_yoy	numpy.float64	净资产收益率(摊薄)同比增（%）	自选返回
net_asset_grow_rate	numpy.float64	净资产同比增长（%）	自选返回
total_asset_grow_rate	numpy.float64	总资产同比增长（%）	自选返回
sustainable_grow_rate	numpy.float64	可持续增长率（%）	自选返回
net_profit_grow_rate	numpy.float64	净利润同比增长（%）	自选返回
profit_ability-盈利能力
接口说明
get_fundamentals(security,'profit_ability',fields, date = None, start_year = None, end_year = None, report_types = None, date_type = None)

             publ_date     roe     secu_abbr
end_date
2013-03-31  2013-04-19  2.8127      恒生电子
2014-03-31  2014-04-29  3.3056      恒生电子
2015-03-31  2015-04-25  3.4869      恒生电子
注意: 获取此表中数据，不支持输入的参数有：merge_type

示例
# 获取数据的两种模式
# 1. 按日期查询模式（默认以发布日期为参考时间）：返回输入日期之前对应的财务数据
# 在回测中获取单一股票中对应回测日期第一季度盈利能力指标中净资产收益率（roe）数据
get_fundamentals('600570.SS','profit_ability','roe','20160628')

# 2. 按年份查询模式：返回输入年份范围内对应季度的财务数据
# 获取恒生电子(600570.SS)从2013年至2015年第一季度盈利能力指标中净资产收益率
#（roe）数据
get_fundamentals('600570.SS','profit_ability','roe',start_year='2013',end_year='2015',report_types='1')
表数据具体字段
盈利能力- profit_ability
字段名称	字段类型	字段说明	属性
secu_code	str	股票代码	固定返回
secu_abbr	str	股票简称	固定返回
publ_date	str	公告日期	固定返回
end_date	str	截止日期	固定返回
roe_avg	numpy.float64	净资产收益率%平均计算值（%）	自选返回
roe_weighted	numpy.float64	净资产收益率%加权公布值（%）	自选返回
roe	numpy.float64	净资产收益率%摊薄公布值（%）	自选返回
roe_cut	numpy.float64	净资产收益率%扣除摊薄（%）	自选返回
roe_cut_weighted	numpy.float64	净资产收益率%扣除加权（%）	自选返回
roe_ttm	numpy.float64	净资产收益率_TTM（%）	自选返回
roa_ebit	numpy.float64	总资产报酬率（%）	自选返回
roa_ebit_ttm	numpy.float64	总资产报酬率_TTM（%）	自选返回
roa	numpy.float64	总资产净利率（%）	自选返回
roa_ttm	numpy.float64	总资产净利率_TTM（%）	自选返回
roic	numpy.float64	投入资本回报率（%）	自选返回
net_profit_ratio	numpy.float64	销售净利率（%）	自选返回
net_profit_ratio_ttm	numpy.float64	销售净利率_TTM（%）	自选返回
gross_income_ratio	numpy.float64	销售毛利率（%）	自选返回
gross_income_ratio_ttm	numpy.float64	销售毛利率_TTM（%）	自选返回
sales_cost_ratio	numpy.float64	销售成本率（%）	自选返回
period_costs_rate	numpy.float64	销售期间费用率（%）	自选返回
period_costs_rate_ttm	numpy.float64	销售期间的费用率_TTM（%）	自选返回
np_to_tor	numpy.float64	净利润／营业总收入（%）	自选返回
np_to_tor_ttm	numpy.float64	净利润／营业总收入_TTM（%）	自选返回
operating_profit_to_tor	numpy.float64	营业利润／营业总收入（%）	自选返回
operating_profit_to_tor_ttm	numpy.float64	营业利润／营业总收入_TTM（%）	自选返回
ebit_to_tor	numpy.float64	息税前利润／营业总收入（%）	自选返回
ebit_to_tor_ttm	numpy.float64	息税前利润／营业总收入_TTM（%）	自选返回
t_operating_cost_to_tor	numpy.float64	营业总成本／营业总收入（%）	自选返回
t_operating_cost_to_tor_ttm	numpy.float64	营业总成本／营业总收入_TTM（%）	自选返回
operating_expense_rate	numpy.float64	销售费用／营业总收入（%）	自选返回
operating_expense_rate_ttm	numpy.float64	销售费用／营业总收入_TTM（%）	自选返回
admini_expense_rate	numpy.float64	管理费用／营业总收入（%）	自选返回
admini_expense_rate_ttm	numpy.float64	管理费用／营业总收入_TTM（%）	自选返回
financial_expense_rate	numpy.float64	财务费用／营业总收入（%）	自选返回
financial_expense_rate_ttm	numpy.float64	财务费用／营业总收入_TTM（%）	自选返回
asset_impa_loss_to_tor	numpy.float64	资产减值损失／营业总收入（%）	自选返回
asset_impa_loss_to_tor_ttm	numpy.float64	资产减值损失／营业总收入_TTM（%）	自选返回
net_profit	numpy.float64	归属母公司净利润（元）	自选返回
net_profit_cut	numpy.float64	扣除非经常性损益后的净利润（元）	自选返回
ebit	numpy.float64	息税前利润（元）	自选返回
ebitda	numpy.float64	息税折旧摊销前利润（元）	自选返回
operating_profit_ratio	numpy.float64	营业利润率（%）	自选返回
total_profit_cost_ratio	numpy.float64	成本费用利润率	自选返回
eps-每股指标
接口说明
get_fundamentals(security,'eps',fields, date = None, start_year = None, end_year = None, report_types = None, date_type = None)
注意: 获取此表中数据，不支持输入的参数有：merge_type


           basic_eps   publ_date      secu_abbr
end_date
2013-03-31      0.06   2013-04-19      恒生电子
2014-03-31      0.09   2014-04-29      恒生电子
2015-03-31      0.11   2015-04-25      恒生电子
示例
# 获取数据的两种模式
# 1. 按日期查询模式（默认以发布日期为参考时间）：返回输入日期之前对应的财务数据
# 在回测中获取单一股票中对应回测日期第一季度每股指标中基本每股收益（basic_eps）# 数据
get_fundamentals('600570.SS','eps','basic_eps','20160628')

# 2. 按年份查询模式：返回输入年份范围内对应季度的财务数据
# 获取恒生电子(600570.SS)从2013年至2015年第一季度每股指标中基本每股收益
#（basic_eps）数据
get_fundamentals('600570.SS','eps','basic_eps',start_year='2013',end_year='2015',report_types='1')
表数据具体字段
每股指标-eps
字段名称	字段类型	字段说明	属性
secu_code	str	股票代码	固定返回
secu_abbr	str	股票简称	固定返回
publ_date	str	公告日期	固定返回
end_date	str	截止日期	固定返回
basic_eps	numpy.float64	基本每股收益（元/股）	自选返回
diluted_eps	numpy.float64	稀释每股收益（元/股）	自选返回
eps	numpy.float64	每股收益_期末股本摊薄（元/股）	自选返回
eps_ttm	numpy.float64	每股收益_TTM（元/股）	自选返回
naps	numpy.float64	每股净资产（元/股）	自选返回
total_operating_revenue_ps	numpy.float64	每股营业总收入（元/股）	自选返回
main_income_ps	numpy.float64	每股营业收入（元/股）	自选返回
operating_revenue_ps_ttm	numpy.float64	每股营业收入_TTM（元/股）	自选返回
oper_profit_ps	numpy.float64	每股营业利润（元/股）	自选返回
ebitps	numpy.float64	每股息税前利润（元/股）	自选返回
capital_surplus_fund_ps	numpy.float64	每股资本公积金（元/股）	自选返回
surplus_reserve_fund_ps	numpy.float64	每股盈余公积（元/股）	自选返回
accumulation_fund_ps	numpy.float64	每股公积金（元/股）	自选返回
undivided_profit	numpy.float64	每股未分配利润（元/股）	自选返回
retained_earnings_ps	numpy.float64	每股留存收益（元/股）	自选返回
net_operate_cash_flow_ps	numpy.float64	每股经营活动产生的现金流量净额（元/股）	自选返回
net_operate_cash_flow_ps_ttm	numpy.float64	每股经营活动产生的现金流量净额_TTM（元/股）	自选返回
cash_flow_ps	numpy.float64	每股现金流量净额（元/股）	自选返回
cash_flow_ps_ttm	numpy.float64	每股现金流量净额_TTM（元/股）	自选返回
enterprise_fcf_ps	numpy.float64	每股企业自由现金流量（元/股）	自选返回
shareholder_fcf_ps	numpy.float64	每股股东自由现金流量（元/股）	自选返回
operating_ability-营运能力
接口说明
get_fundamentals(security,'operating_ability',fields, date = None, start_year = None, end_year = None, report_types = None, date_type = None)
注意: 获取此表中数据，不支持输入的参数有：merge_type


           current_assets_turnover_rate   publ_date     secu_abbr
end_date
2013-03-31                       0.1803   2013-04-19     恒生电子
2014-03-31                       0.1518   2014-04-29     恒生电子
2015-03-31                       0.1568   2015-04-25     恒生电子
示例
# 获取数据的两种模式
# 1. 按日期查询模式（默认以发布日期为参考时间）：返回输入日期之前对应的财务数据
# 在回测中获取单一股票中对应回测日期第一季度营运能力指标中流动资产周转率
#（current_assets_turnover_rate）数据
get_fundamentals('600570.SS','operating_ability','current_assets_turnover_rate','20160628')

# 2. 按年份查询模式：返回输入年份范围内对应季度的财务数据
# 获取恒生电子(600570.SS)从2013年至2015年第一季度营运能力指标中流动资产周转# 率（current_assets_turnover_rate）数据
get_fundamentals('600570.SS','operating_ability','current_assets_turnover_rate',start_year='2013',end_year='2015', report_types='1')
表数据具体字段
营运能力- operating_ability
字段名称	字段类型	字段说明	属性
secu_code	str	股票代码	固定返回
secu_abbr	str	股票简称	固定返回
publ_date	str	公告日期	固定返回
end_date	str	截止日期	固定返回
oper_cycle	numpy.float64	营业周期（天/次）	自选返回
inventory_turnover_rate	numpy.float64	存货周转率（次）	自选返回
inventory_turnover_days	numpy.float64	存货周转天数（天/次）	自选返回
accounts_receivables_turnover_rate	numpy.float64	应收账款周转率（次）	自选返回
accounts_receivables_turnover_days	numpy.float64	应收账款周转天数（天/次）	自选返回
accounts_payables_turnover_rate	numpy.float64	应付账款周转率（次）	自选返回
accounts_payables_turnover_days	numpy.float64	应付账款周转天数（天/次）	自选返回
current_assets_turnover_rate	numpy.float64	流动资产周转率（次）	自选返回
fixed_asset_turnover_rate	numpy.float64	固定资产周转率（次）	自选返回
equity_turnover_rate	numpy.float64	股东权益周转率（次）	自选返回
total_asset_turnover_rate	numpy.float64	总资产周转率（次）	自选返回
debt_paying_ability-偿债能力
接口说明
get_fundamentals(security,'debt_paying_ability',fields, date = None, start_year = None, end_year = None, report_types = None, date_type = None)
注意: 获取此表中数据，不支持输入的参数有：merge_type


           current_ratio   publ_date      secu_abbr
end_date
2013-03-31        3.4234   2013-04-19      恒生电子
2014-03-31        3.4941   2014-04-29      恒生电子
2015-03-31        1.8332   2015-04-25      恒生电子
示例
# 获取数据的两种模式
# 1. 按日期查询模式（默认以发布日期为参考时间）：返回输入日期之前对应的财务数据
# 在回测中获取单一股票中对应回测日期第一季度偿债能力指标中流动比率（current_ratio）
# 数据
get_fundamentals('600570.SS','debt_paying_ability','current_ratio','20160628')

# 2. 按年份查询模式：返回输入年份范围内对应季度的财务数据
# 获取恒生电子(600570.SS)从2013年至2015年第一季度偿债能力指标中流动比率
#（current_ratio）数据
get_fundamentals('600570.SS','debt_paying_ability','current_ratio',start_year='2013',end_year='2015', report_types='1')
表数据具体字段
偿债能力- debt_paying_ability
字段名称	字段类型	字段说明	属性
secu_code	str	股票代码	固定返回
secu_abbr	str	股票简称	固定返回
publ_date	str	公告日期	固定返回
end_date	str	截止日期	固定返回
current_ratio	numpy.float64	流动比率	自选返回
quick_ratio	numpy.float64	速动比率	自选返回
super_quick_ratio	numpy.float64	超速动比率	自选返回
debt_equity_ratio	numpy.float64	产权比率（%）	自选返回
sewmi_to_total_liability	numpy.float64	归属母公司股东的权益／负债合计（%）	自选返回
sewmi_to_interest_bear_debt	numpy.float64	归属母公司股东的权益／带息债务（%）	自选返回
debt_tangible_equity_ratio	numpy.float64	有形净值债务率（%）	自选返回
tangible_a_to_interest_bear_debt	numpy.float64	有形净值／带息债务（%）	自选返回
tangible_a_to_net_debt	numpy.float64	有形净值／净债务（%）	自选返回
ebitda_to_t_liability	numpy.float64	息税折旧摊销前利润／负债合计	自选返回
nocf_to_t_liability	numpy.float64	经营活动产生现金流量净额/负债合计	自选返回
nocf_to_interest_bear_debt	numpy.float64	经营活动产生现金流量净额/带息债务	自选返回
nocf_to_current_liability	numpy.float64	经营活动产生现金流量净额/流动负债	自选返回
nocf_to_net_debt	numpy.float64	经营活动产生现金流量净额/净债务	自选返回
interest_cover	numpy.float64	利息保障倍数（倍）	自选返回
long_debt_to_working_capital	numpy.float64	长期负债与营运资金比率	自选返回
opercashinto_current_debt	numpy.float64	现金流动负债比	自选返回
############################################
# 标准指数编号
提供数据源最新的标准指数编号，具体调用方法可以参考API文档。

(温馨提示：鉴于内容太多, 可使用Ctrl + F进行搜索)

指数编号
序号	prod_code	prod_name
1	000001	上证指数
2	000002	Ａ股指数
3	000003	Ｂ股指数
4	000004	工业指数
5	000005	商业指数
6	000006	地产指数
7	000007	公用指数
8	000008	综合指数
9	000009	上证380
10	000010	上证180
11	000011	基金指数
12	000012	国债指数
13	000015	红利指数
14	000016	上证50
15	000017	新综指
16	000018	180金融
17	000019	治理指数
18	000020	中型综指
19	000021	180治理
20	000022	沪公司债
21	000025	180基建
22	000026	180资源
23	000027	180运输
24	000028	180成长
25	000029	180价值
26	000030	180R成长
27	000031	180R价值
28	000032	上证能源
29	000033	上证材料
30	000034	上证工业
31	000035	上证可选
32	000036	上证消费
33	000037	上证医药
34	000038	上证金融
35	000039	上证信息
36	000040	上证电信
37	000041	上证公用
38	000042	上证央企
39	000043	超大盘
40	000044	上证中盘
41	000045	上证小盘
42	000046	上证中小
43	000047	上证全指
44	000048	责任指数
45	000049	上证民企
46	000050	50等权
47	000051	180等权
48	000052	50基本
49	000053	180基本
50	000054	上证海外
51	000055	上证地企
52	000056	上证国企
53	000057	全指成长
54	000058	全指价值
55	000059	全R成长
56	000060	全R价值
57	000061	沪企债30
58	000062	上证沪企
59	000063	上证周期
60	000064	非周期
61	000065	上证龙头
62	000066	上证商品
63	000067	上证新兴
64	000068	上证资源
65	000069	消费80
66	000070	能源等权
67	000071	材料等权
68	000072	工业等权
69	000073	可选等权
70	000074	消费等权
71	000075	医药等权
72	000076	金融等权
73	000077	信息等权
74	000078	电信等权
75	000079	公用等权
76	000090	上证流通
77	000091	沪财中小
78	000092	资源50
79	000093	180分层
80	000094	上证上游
81	000095	上证中游
82	000096	上证下游
83	000097	高端装备
84	000098	上证F200
85	000099	上证F300
86	000100	上证F500
87	000101	5年信用
88	000102	沪投资品
89	000103	沪消费品
90	000104	380能源
91	000105	380材料
92	000106	380工业
93	000107	380可选
94	000108	380消费
95	000109	380医药
96	000110	380金融
97	000111	380信息
98	000112	380电信
99	000113	380公用
100	000114	持续产业
101	000115	380等权
102	000116	信用100
103	000117	380成长
104	000118	380价值
105	000119	380R成长
106	000120	380R价值
107	000121	医药主题
108	000122	农业主题
109	000123	180动态
110	000125	180稳定
111	000126	消费50
112	000128	380基本
113	000129	180波动
114	000130	380波动
115	000131	上证高新
116	000132	上证100
117	000133	上证150
118	000134	上证银行
119	000135	180高贝
120	000136	180低贝
121	000137	380高贝
122	000138	380低贝
123	000139	上证转债
124	000141	380动态
125	000142	380稳定
126	000145	优势资源
127	000146	优势制造
128	000147	优势消费
129	000148	消费领先
130	000149	180红利
131	000150	380红利
132	000151	上国红利
133	000152	上央红利
134	000153	上民红利
135	000155	市值百强
136	000158	上证环保
137	000159	沪股通
138	000160	沪新丝路
139	000161	沪中国造
140	000162	沪互联+
141	000170	50AH优选
142	000300	沪深300
143	000510	中证A500
144	000680	科创综指
145	000681	科创价格
146	000682	科创信息
147	000683	科创生物
148	000685	科创芯片
149	000687	科创高装
150	000688	科创50
151	000689	科创材料
152	000690	科创成长
153	000691	科创ESG
154	000692	科创新能
155	000693	科创机械
156	000695	科长三角
157	000697	科大湾区
158	000698	科创100
159	000699	科创200
160	000802	500沪市
161	000814	细分医药
162	000819	有色金属
163	000823	800有色
164	000827	中证环保
165	000847	腾讯济安
166	000849	300非银
167	000851	百发100
168	000852	中证1000
169	000853	CSSW丝路
170	000854	500原料
171	000855	央视500
172	000856	500工业
173	000857	500医药
174	000858	500信息
175	000860	结构调整
176	000863	CS精准医
177	000865	上海国企
178	000867	港中小企
179	000869	HK银行
180	000888	上证收益
181	000891	新兴综指
182	000901	小康指数
183	000903	中证A100
184	000905	中证500
185	000906	中证800
186	000913	300医药
187	000914	300金融
188	000928	中证能源
189	000932	中证消费
190	000933	中证医药
191	000934	中证金融
192	000935	中证信息
193	000974	800金融
194	000982	500等权
195	000986	全指能源
196	000987	全指材料
197	000989	全指可选
198	000991	全指医药
199	000992	全指金融
200	000993	全指信息
201	395001	主板Ａ股
202	395002	主板Ｂ股
203	395004	创业板
204	395005	主板DR
205	395006	创业板DR
206	395011	封闭基金
207	395012	ＬＯＦｓ
208	395013	ＥＴＦｓ
209	395015	REITS
210	395032	债券回购
211	395033	债券现货
212	395034	ABS
213	395041	股票权证
214	395099	总 成 交
215	399001	深证成指
216	399002	深成指R
217	399003	成份Ｂ指
218	399004	深证100R
219	399005	中小100
220	399006	创业板指
221	399007	深证300
222	399008	中小300
223	399009	深证200
224	399010	深证700
225	399011	深证1000
226	399012	创业300
227	399013	深市精选
228	399015	中小创新
229	399016	深证创新
230	399017	SME创新
231	399018	创业创新
232	399019	创业200
233	399020	创业小盘
234	399030	碳科技30
235	399050	创新引擎
236	399060	碳科技60
237	399088	深创100
238	399100	新指数
239	399101	中小综指
240	399102	创业板综
241	399103	乐富指数
242	399106	深证综指
243	399107	深证Ａ指
244	399108	深证Ｂ指
245	399231	农林指数
246	399232	采矿指数
247	399233	制造指数
248	399234	水电指数
249	399235	建筑指数
250	399236	批零指数
251	399237	运输指数
252	399239	IT指数
253	399240	金融指数
254	399241	地产指数
255	399242	商务指数
256	399243	科研指数
257	399244	公共指数
258	399248	文化指数
259	399258	绿色低碳
260	399259	创业低碳
261	399260	先进制造
262	399261	创业制造
263	399262	数字经济
264	399263	创业数字
265	399264	创业软件
266	399265	创新药械
267	399266	创新能源
268	399267	专精特新
269	399268	深小巨人
270	399269	创质量
271	399274	深新基建
272	399275	创医药
273	399276	创科技
274	399277	公共健康
275	399278	长江100
276	399279	云科技50
277	399280	生物50
278	399281	电子50
279	399282	大数据50
280	399283	机器人50
281	399284	AI 50
282	399285	物联网50
283	399286	区块链50
284	399289	碳中和债
285	399290	深转交债
286	399291	创精选88
287	399292	民企发展
288	399293	创业大盘
289	399294	中小创Q
290	399295	创价值
291	399296	创成长
292	399297	新浪100
293	399298	深信中高
294	399299	深信中低
295	399300	沪深300
296	399301	深信用债
297	399302	深公司债
298	399303	国证2000
299	399306	深证ETF
300	399307	深证转债
301	399310	国证A50
302	399311	国证1000
303	399312	国证300
304	399313	巨潮100
305	399314	巨潮大盘
306	399315	巨潮中盘
307	399316	巨潮小盘
308	399317	国证Ａ指
309	399318	国证Ｂ指
310	399319	资源优势
311	399320	国证服务
312	399321	国证红利
313	399322	国证治理
314	399324	深证红利
315	399326	成长40
316	399328	深证治理
317	399330	深证100
318	399333	中小100R
319	399335	深证央企
320	399337	深证民营
321	399339	深证科技
322	399341	深证责任
323	399344	深证300R
324	399346	深证成长
325	399348	深证价值
326	399350	皖江30
327	399351	创新示范
328	399352	深企综指
329	399353	国证物流
330	399354	分析师指数
331	399355	长三角
332	399356	珠三角
333	399357	环渤海
334	399358	国证环保
335	399359	国证基建
336	399360	新硬件
337	399361	在线消费
338	399362	民企100
339	399363	国证算力
340	399364	消费100
341	399365	国证粮食
342	399366	能源金属
343	399367	1000地产
344	399368	国证军工
345	399369	国证责任
346	399370	国证成长
347	399371	国证价值
348	399372	大盘成长
349	399373	大盘价值
350	399374	中盘成长
351	399375	中盘价值
352	399376	小盘成长
353	399377	小盘价值
354	399378	ESG 300
355	399379	国证基金
356	399380	国证ETF
357	399381	1000能源
358	399382	1000材料
359	399383	1000工业
360	399384	1000可选
361	399385	1000消费
362	399386	1000医药
363	399387	1000金融
364	399388	1000信息
365	399389	国证通信
366	399390	1000公用
367	399391	投资时钟
368	399392	国证新兴
369	399393	国证地产
370	399394	国证医药
371	399395	国证有色
372	399396	国证食品
373	399397	国证文化
374	399398	绩效指数
375	399399	中经GDP
376	399400	大中盘
377	399401	中小盘
378	399402	周期100
379	399403	防御100
380	399405	大盘高贝
381	399406	中盘低波
382	399407	中盘高贝
383	399408	小盘低波
384	399409	小盘高贝
385	399410	苏州率先
386	399411	红利100
387	399412	国证新能
388	399413	国证转债
389	399415	I100
390	399416	I300
391	399417	新能源车
392	399418	数据要素
393	399419	国证高铁
394	399420	国证保证
395	399422	中关村A
396	399423	中关村50
397	399428	国证定增
398	399429	新丝路
399	399431	国证银行
400	399432	智能汽车
401	399433	国证交运
402	399434	数字传媒
403	399435	国证农牧
404	399436	绿色煤炭
405	399437	证券龙头
406	399438	绿色电力
407	399439	国证油气
408	399440	国证钢铁
409	399441	生物医药
410	399481	企债指数
411	399550	央视50
412	399551	央视创新
413	399552	央视成长
414	399553	央视回报
415	399554	央视治理
416	399555	央视责任
417	399556	央视生态
418	399557	央视文化
419	399602	中小成长
420	399604	中小价值
421	399606	创业板R
422	399608	科技100
423	399610	TMT50
424	399611	中创100R
425	399612	中创100
426	399613	深证能源
427	399614	深证材料
428	399615	深证工业
429	399616	深证可选
430	399617	深证消费
431	399618	深证医药
432	399619	深证金融
433	399620	深证信息
434	399621	深证电信
435	399622	深证公用
436	399623	中小基础
437	399624	中创400
438	399625	中创500
439	399626	中创成长
440	399627	中创价值
441	399628	700成长
442	399629	700价值
443	399630	1000成长
444	399631	1000价值
445	399632	深100EW
446	399633	深300EW
447	399634	中小等权
448	399635	创业板EW
449	399636	深证装备
450	399637	深证地产
451	399638	深证环保
452	399639	深证大宗
453	399640	创业基础
454	399641	深证新兴
455	399642	中小新兴
456	399643	创业新兴
457	399644	深证时钟
458	399645	100低波
459	399646	深消费50
460	399647	深医药50
461	399648	深证GDP
462	399649	中小红利
463	399650	中小治理
464	399651	中小责任
465	399652	中创高新
466	399653	深证龙头
467	399654	深证文化
468	399655	深证绩效
469	399656	100绩效
470	399657	300绩效
471	399658	中小绩效
472	399659	深成指EW
473	399660	中创EW
474	399661	深证低波
475	399662	深证高贝
476	399663	中小低波
477	399664	中小高贝
478	399665	中创低波
479	399666	中创高贝
480	399667	创业成长
481	399668	创业板V
482	399669	深证农业
483	399670	深周期50
484	399671	深防御50
485	399672	深红利50
486	399673	创业板50
487	399674	深A医药
488	399675	深互联网
489	399676	深医药EW
490	399677	深互联EW
491	399678	深次新股
492	399679	深证200R
493	399680	深成能源
494	399681	深成材料
495	399682	深成工业
496	399683	深成可选
497	399684	深成消费
498	399685	深成医药
499	399686	深成金融
500	399687	深成信息
501	399688	深成电信
502	399689	深成公用
503	399692	创业低波
504	399693	安防产业
505	399694	创业高贝
506	399695	深证节能
507	399696	深证创投
508	399697	中关村60
509	399698	优势成长
510	399699	金融科技
511	399701	深证F60
512	399702	深证F120
513	399703	深证F200
514	399704	深证上游
515	399705	深证中游
516	399706	深证下游
517	399707	CSSW证券
518	399750	深主板50
519	399802	500深市
520	399803	工业4.0
521	399804	中证体育
522	399805	互联金融
523	399806	环境治理
524	399807	高铁产业
525	399808	中证新能
526	399809	保险主题
527	399810	CSSW传媒
528	399811	CSSW电子
529	399812	养老产业
530	399813	中证国安
531	399814	大农业
532	399850	深证50
533	399852	中证1000
534	399901	小康指数
535	399903	中证100
536	399905	中证 500
537	399913	300 医药
538	399914	300 金融
539	399928	中证能源
540	399932	中证消费
541	399933	中证医药
542	399934	中证金融
543	399935	中证信息
544	399959	军工指数
545	399965	800地产
546	399966	800非银
547	399967	中证军工
548	399970	移动互联
549	399971	中证传媒
550	399972	300深市
551	399973	中证国防
552	399974	国企改革
553	399975	证券公司
554	399976	CS新能车
555	399982	500等权
556	399983	地产等权
557	399986	中证银行
558	399987	中证酒
559	399989	中证医疗
560	399990	煤炭等权
561	399991	一带一路
562	399992	CSWD并购
563	399993	CSWD生科
564	399994	信息安全
565	399995	基建工程
566	399996	智能家居
567	399997	中证白酒
568	399998	中证煤炭
569	970070	CNTAI50
570	980001	湾创100
571	980015	疫苗生科
572	980016	医疗健康
573	980017	国证芯片
574	980018	卫星通信
575	980022	CNIROBOT
576	980023	南山50
577	980027	CNINEB
578	980028	龙头家电
579	980030	消费电子
580	980032	新能电池
581	980035	化肥农药
582	980068	蓝色100
583	980076	通用航空
584	980092	CNIFCF
585	988006	CNTHKD
586	988007	CNTUSD
587	988106	CNTTRHKD
588	988107	CNTTRUSD
##########################################################
# 行业数据
提供行业板块信息。

(温馨提示：鉴于内容太多, 可使用Ctrl + F进行搜索)

证监会行业编号
序号	指数代码	指数名称
1	A00000	农、林、牧、渔业
2	A01000	农业
3	A02000	林业
4	A03000	畜牧业
5	A04000	渔业
6	A05000	农、林、牧、渔服务业
7	B00000	采矿业
8	B06000	煤炭开采和洗选业
9	B07000	石油和天然气开采业
10	B08000	黑色金属矿采选业
11	B09000	有色金属矿采选业
12	B10000	非金属矿采选业
13	B11000	开采辅助活动
14	C00000	制造业
15	C13000	农副食品加工业
16	C14000	食品制造业
17	C15000	酒、饮料和精制茶制造业
18	C17000	纺织业
19	C18000	纺织服装、服饰业
20	C19000	皮革、毛皮、羽毛及其制品和制鞋
21	C20000	木材加工和木、竹、藤、棕、草制
22	C21000	家具制造业
23	C22000	造纸和纸制品业
24	C23000	印刷和记录媒介复制业
25	C24000	文教、工美、体育和娱乐用品制造
26	C25000	石油加工、炼焦和核燃料加工业
27	C26000	化学原料和化学制品制造业
28	C27000	医药制造业
29	C28000	化学纤维制造业
30	C29000	橡胶和塑料制品业
31	C30000	非金属矿物制品业
32	C31000	黑色金属冶炼和压延加工业
33	C32000	有色金属冶炼和压延加工业
34	C33000	金属制品业
35	C34000	通用设备制造业
36	C35000	专用设备制造业
37	C36000	汽车制造业
38	C37000	铁路、船舶、航空航天和其他运输
39	C38000	电气机械和器材制造业
40	C39000	计算机、通信和其他电子设备制造
41	C40000	仪器仪表制造业
42	C41000	其他制造业
43	C42000	废弃资源综合利用业
44	C43000	金属制品、机械和设备修理业
45	D00000	电力、热力、燃气及水生产和供应
46	D44000	电力、热力生产和供应业
47	D45000	燃气生产和供应业
48	D46000	水的生产和供应业
49	E00000	建筑业
50	E47000	房屋建筑业
51	E48000	土木工程建筑业
52	E49000	建筑安装业
53	E50000	建筑装饰和其他建筑业
54	F00000	批发和零售业
55	F51000	批发业
56	F52000	零售业
57	G00000	交通运输、仓储和邮政业
58	G53000	铁路运输业
59	G54000	道路运输业
60	G55000	水上运输业
61	G56000	航空运输业
62	G58000	装卸搬运和运输代理业
63	G59000	仓储业
64	G60000	邮政业
65	H00000	住宿和餐饮业
66	H61000	住宿业
67	H62000	餐饮业
68	I00000	信息传输、软件和信息技术服务业
69	I63000	电信、广播电视和卫星传输服务
70	I64000	互联网和相关服务
71	I65000	软件和信息技术服务业
72	J00000	金融业
73	J66000	货币金融服务
74	J67000	资本市场服务
75	J68000	保险业
76	J69000	其他金融业
77	K00000	房地产业
78	K70000	房地产业
79	L00000	租赁和商务服务业
80	L71000	租赁业
81	L72000	商务服务业
82	M00000	科学研究和技术服务业
83	M73000	研究和试验发展
84	M74000	专业技术服务业
85	M75000	科技推广和应用服务业
86	N00000	水利、环境和公共设施管理业
87	N77000	生态保护和环境治理业
88	N78000	公共设施管理业
89	O00000	居民服务、修理和其他服务业
90	O80000	机动车、电子产品和日用产品修理
91	P00000	教育
92	P82000	教育
93	Q00000	卫生和社会工作
94	Q83000	卫生
95	R00000	文化、体育和娱乐业
96	R85000	新闻和出版业
97	R86000	广播、电视、电影和影视录音制作
98	R87000	文化艺术业
99	R88000	体育
100	S00000	综合
101	S90000	综合
聚源行业分类
序号	指数代码	指数名称
1	110000	农林牧渔
2	110100	种植业
3	110200	渔业
4	110300	林业Ⅱ
5	110400	饲料
6	110500	农产品加工
7	110700	养殖业
8	110800	动物保健Ⅱ
9	110900	农业综合Ⅱ
10	220000	基础化工
11	220200	化学原料
12	220300	化学制品
13	220400	化学纤维
14	220500	塑料
15	220600	橡胶
16	220800	农化制品
17	220900	非金属材料Ⅱ
18	230000	钢铁
19	230300	冶钢原料
20	230400	普钢
21	230500	特钢Ⅱ
22	240000	有色金属
23	240200	金属新材料
24	240300	工业金属
25	240400	贵金属
26	240500	小金属
27	240600	能源金属
28	270000	电子
29	270100	半导体
30	270200	元件
31	270300	光学光电子
32	270400	其他电子Ⅱ
33	270500	消费电子
34	270600	电子化学品Ⅱ
35	280000	汽车
36	280200	汽车零部件
37	280300	汽车服务
38	280400	摩托车及其他
39	280500	乘用车
40	280600	商用车
41	330000	家用电器
42	330100	白色家电
43	330200	黑色家电
44	330300	小家电
45	330400	厨卫电器
46	330500	照明设备Ⅱ
47	330600	家电零部件Ⅱ
48	330700	其他家电Ⅱ
49	340000	食品饮料
50	340400	食品加工
51	340500	白酒Ⅱ
52	340600	非白酒
53	340700	饮料乳品
54	340800	休闲食品
55	340900	调味发酵品Ⅱ
56	350000	纺织服饰
57	350100	纺织制造
58	350200	服装家纺
59	350300	饰品
60	360000	轻工制造
61	360100	造纸
62	360200	包装印刷
63	360300	家居用品
64	360500	文娱用品
65	370000	医药生物
66	370100	化学制药
67	370200	中药Ⅱ
68	370300	生物制品
69	370400	医药商业
70	370500	医疗器械
71	370600	医疗服务
72	410000	公用事业
73	410100	电力
74	410300	燃气Ⅱ
75	420000	交通运输
76	420800	物流
77	420900	铁路公路
78	421000	航空机场
79	421100	航运港口
80	430000	房地产
81	430100	房地产开发
82	430300	房地产服务
83	450000	商贸零售
84	450200	贸易Ⅱ
85	450300	一般零售
86	450400	专业连锁Ⅱ
87	450600	互联网电商
88	450700	旅游零售Ⅱ
89	460000	社会服务
90	460600	体育Ⅱ
91	460800	专业服务
92	460900	酒店餐饮
93	461000	旅游及景区
94	461100	教育
95	480000	银行
96	480200	国有大型银行Ⅱ
97	480300	股份制银行Ⅱ
98	480400	城商行Ⅱ
99	480500	农商行Ⅱ
100	490000	非银金融
101	490100	证券Ⅱ
102	490200	保险Ⅱ
103	490300	多元金融
104	510000	综合
105	510100	综合Ⅱ
106	610000	建筑材料
107	610100	水泥
108	610200	玻璃玻纤
109	610300	装修建材
110	620000	建筑装饰
111	620100	房屋建设Ⅱ
112	620200	装修装饰Ⅱ
113	620300	基础建设
114	620400	专业工程
115	620600	工程咨询服务Ⅱ
116	630000	电力设备
117	630100	电机Ⅱ
118	630300	其他电源设备Ⅱ
119	630500	光伏设备
120	630600	风电设备
121	630700	电池
122	630800	电网设备
123	640000	机械设备
124	640100	通用设备
125	640200	专用设备
126	640500	轨交设备Ⅱ
127	640600	工程机械
128	640700	自动化设备
129	650000	国防军工
130	650100	航天装备Ⅱ
131	650200	航空装备Ⅱ
132	650300	地面兵装Ⅱ
133	650400	航海装备Ⅱ
134	650500	军工电子Ⅱ
135	710000	计算机
136	710100	计算机设备
137	710300	IT服务Ⅱ
138	710400	软件开发
139	720000	传媒
140	720400	游戏Ⅱ
141	720500	广告营销
142	720600	影视院线
143	720700	数字媒体
144	720900	出版
145	721000	电视广播Ⅱ
146	730000	通信
147	730100	通信服务
148	730200	通信设备
149	740000	煤炭
150	740100	煤炭开采
151	740200	焦炭Ⅱ
152	750000	石油石化
153	750100	油气开采Ⅱ
154	750200	油服工程
155	750300	炼化及贸易
156	760000	环保
157	760100	环境治理
158	760200	环保设备Ⅱ
159	770000	美容护理
160	770100	个护用品
161	770200	化妆品
162	770300	医疗美容
地域类
提供地域板块信息

地域板块信息
序号	指数代码	指数名称
1	DY1145	上海板块
2	DY1146	黑龙江
3	DY1147	新疆板块
4	DY1148	吉林板块
5	DY1149	安徽板块
6	DY1150	北京板块
7	DY1151	福建板块
8	DY1152	甘肃板块
9	DY1153	广东板块
10	DY1154	广西板块
11	DY1155	河北板块
12	DY1156	河南板块
13	DY1157	湖北板块
14	DY1158	湖南板块
15	DY1159	江苏板块
16	DY1160	江西板块
17	DY1161	辽宁板块
18	DY1162	宁夏板块
19	DY1163	青海板块
20	DY1164	山东板块
21	DY1165	陕西板块
22	DY1166	天津板块
23	DY1167	山西板块
24	DY1169	四川板块
25	DY1170	重庆板块
26	DY1171	云南板块
27	DY1172	浙江板块
28	DY1173	贵州板块
29	DY1174	西藏板块
30	DY1175	内蒙古
31	DY1176	海南板块
概念类
提供概念板块信息

概念板块
序号	指数代码	指数名称
1	000014	地下管网
2	000019	足球概念
3	000021	大飞机
4	002486	文化传媒概念
5	003490	军工
6	003491	高校
7	003492	煤化工概念
8	003494	节能环保
9	003498	AB股
10	003499	AH股
11	003501	新股与次新股
12	003505	中字头
13	003506	创投
14	003509	网络游戏
15	003511	ST概念
16	003514	参股券商
17	003519	稀缺资源
18	003523	新材料
19	003547	黄金概念
20	003548	生物疫苗
21	003554	物联网
22	003574	锂电池概念
23	003577	核电概念
24	003578	稀土永磁
25	003579	云计算
26	003580	LED概念
27	003581	智能电网
28	003583	触摸屏概念
29	003588	太阳能概念
30	003592	铁路基建
31	003596	融资融券
32	003597	水利建设
33	003598	IPV6
34	003600	参股新三板
35	003601	海工装备
36	003603	页岩气
37	003605	金融改革
38	003606	油气设备服务
39	003608	PM2.5
40	003614	食品安全
41	003617	石墨烯
42	003619	3D打印
43	003622	地热能
44	003625	通用航空
45	003628	智慧城市
46	003629	北斗导航
47	003631	转融券标的
48	003632	土地流转
49	003634	大数据
50	003637	互联网金融
51	003640	机器人概念
52	003641	智能穿戴
53	003642	手游概念
54	003643	上海自贸区
55	003644	特斯拉
56	003652	参股民营银行
57	003653	养老概念
58	003655	网络安全
59	003656	智能电视
60	003660	民营医院
61	003662	在线教育
62	003663	油改概念
63	003665	电商概念
64	003666	苹果概念
65	003667	安防概念
66	003668	医疗器械概念
67	003669	生态农业
68	003671	彩票概念
69	003672	上海国资改革
70	003674	蓝宝石
71	003675	病毒防治
72	003677	粤港澳自贸区
73	003679	超导概念
74	003680	智能家居
75	003682	燃料电池概念
76	003683	国企改革
77	003684	京津冀一体化
78	003685	举牌概念
79	003689	阿里概念
80	003690	氟化工概念
81	003693	基因测序
82	003696	国产软件
83	003699	全息技术
84	003700	充电桩
85	003703	超级电容
86	003704	无人机
87	003707	沪股通
88	003708	体育产业
89	003710	量子通信
90	003711	券商
91	003712	一带一路
92	003714	5G概念
93	003715	航母概念
94	003718	证金持股
95	003721	PPP模式
96	003722	虚拟现实（VR）
97	003723	高送转
98	003724	海绵城市
99	003800	人工智能
100	003801	增强现实（AR）
101	003802	无人驾驶
102	003803	股权转让
103	003804	深股通
104	003805	钛白粉概念
105	003808	军民融合
106	003810	工业4.0
107	003813	雄安新区
108	003830	区块链
109	003840	OLED
110	003870	单抗概念
111	003881	3D玻璃
112	003882	猪肉
113	003891	芯片概念
114	003900	新能源车
115	003920	车联网(车路协同)
116	003940	网红直播
117	003950	草甘膦
118	003960	无线充电
119	003980	债转股
120	003990	快递物流
121	010001	养鸡
122	010004	固废处理
123	010005	光伏概念
124	010011	尾气治理
125	010012	污水处理
126	011037	靶材
127	011294	工业大麻
128	011304	人造肉
129	011309	烟草
130	011311	垃圾分类
131	011327	农业种植
132	011335	转基因
133	011341	HJT/HIT电池
134	011358	水产品
135	011388	电子烟
136	011406	碳交易
137	011411	碳中和
138	011412	BIPV概念(光伏建筑一体化)
139	011424	储能概念
140	011432	农药概念
141	011433	兽药
142	011437	绿色电力
143	020003	黄酒概念
144	020006	葡萄酒概念
145	020007	乳业
146	021038	装配式建筑
147	021044	腾讯概念
148	021046	啤酒概念
149	021282	百度概念
150	021291	华为概念
151	021295	信托概念
152	021306	华为海思概念
153	021346	华为HMS
154	021349	食品饮料概念
155	021363	今日头条概念
156	021386	银行概念
157	021387	保险概念
158	021391	代糖(甜味剂)
159	021402	拼多多概念
160	021419	预制菜
161	030016	摘帽
162	031027	MSCI概念
163	031028	白马股
164	031030	超级品牌
165	031034	养老金持股
166	031283	昨日涨停
167	031317	上证50
168	031320	分拆上市预期
169	031352	含可转债
170	031356	影视传媒
171	031364	钢铁概念
172	031384	爱奇艺概念
173	031390	国家大基金持股
174	031398	昨日连板
175	031401	快手概念
176	031413	NFT文交所
177	031425	专精特新
178	031429	参股三板精选层
179	031430	北交所概念
180	040002	禽流感
181	041006	血液制品概念
182	041272	工业互联网
183	041299	电力物联网
184	041302	超级真菌
185	041322	VPN
186	041334	煤炭概念
187	041343	WIFI6
188	041354	数据中心
189	041366	病毒检测
190	050001	铜概念
191	050002	铝概念
192	050005	镍概念
193	050007	白银概念
194	050011	钴概念
195	050012	钨概念
196	050013	钼概念
197	051360	RCS富媒体通信
198	051365	有色金属概念
199	051403	钛
200	051418	盐湖提锂
201	051428	硅锰
202	051434	锂矿
203	051438	磷酸铁锂
204	060002	万达私有化
205	060004	节能照明
206	060006	汽车电子概念
207	060015	移动支付
208	060018	微信小程序
209	060107	有机硅类
210	060109	粘胶短纤
211	061029	无人零售
212	061035	人脸识别
213	061045	石墨电极
214	061047	小米概念
215	061271	富士康概念
216	061273	独角兽概念
217	061274	分散染料
218	061276	知识产权保护
219	061277	数字中国
220	061278	无人银行
221	061287	进口博览会
222	061297	边缘计算
223	061315	磷化工
224	061321	数字货币
225	061361	纺织服装概念
226	061368	化妆品概念
227	061378	机器视觉
228	061392	可降解塑料
229	061408	PVC
230	061409	甲醇
231	061410	PTA
232	061431	元宇宙
233	070001	杭州亚运会
234	070002	网约车
235	070004	电子发票
236	070005	跨境电商概念
237	070006	冷链物流
238	070007	物流电商平台
239	070009	共享单车
240	071024	新零售
241	071281	短视频
242	071359	C2M概念
243	071377	免税店概念
244	071380	地摊经济
245	071405	社区团购
246	080001	水泥概念
247	080002	玻璃概念
248	081275	宁德时代概念
249	081301	透明工厂
250	081355	家居概念
251	081376	精装修
252	081407	固态电池
253	081420	钠离子电池
254	081426	工业母机
255	081440	换电概念
256	090002	波罗的海干散货指数(BDI)
257	091353	航运概念
258	100015	集成电路概念
259	101284	PCB概念
260	101292	柔性屏
261	101296	超高清视频
262	101307	国产操作系统
263	101308	沪伦通
264	101316	光刻机
265	101329	胎压监测
266	101330	汽车零部件概念
267	101331	MiniLED
268	101332	3D摄像头
269	101333	传感器
270	101337	远程办公
271	101344	氮化镓
272	101345	被动元件概念
273	101347	广电系
274	101370	造纸概念
275	101374	包装印刷概念
276	101375	轮胎概念
277	101379	碳基半导体
278	101382	EDA设计软件
279	101383	汽车整车概念
280	101385	中芯国际概念
281	101394	碳化硅
282	101395	金刚石
283	101396	第三代半导体
284	101399	快充概念
285	101400	蔚来汽车概念
286	101414	激光雷达
287	101423	华为鸿蒙
288	101439	IGBT
289	110003	高铁
290	110006	智能医疗
291	110007	智慧停车
292	111040	智能音箱
293	111041	智能交通
294	111042	语音技术
295	111300	数字孪生
296	111314	ETC
297	111326	无线耳机
298	111350	基建
299	111367	REITs
300	111369	港口概念
301	111371	西部大开发
302	111372	工程机械概念
303	111373	电梯概念
304	120001	家用电器概念
305	121348	旅游概念
306	121381	盲盒
307	121422	宠物经济
308	130002	职业教育
309	131031	维生素
310	131362	创新药
311	140001	供应链金融
312	150001	新疆振兴
313	150002	振兴东北
314	170004	生物质能
315	171021	可燃冰
316	171036	燃料乙醇
317	171303	氢能源
318	181024	特色小镇
319	181032	杭州湾大湾区
320	181305	长三角一体化
321	181319	深圳特区
322	191421	三胎概念
323	200001	农村电商
324	200002	农机
325	201270	乡村振兴
326	220002	电子竞技
327	221279	马彩概念
328	231340	医疗信息化
329	231357	呼吸机
330	231435	培育钻石
331	250003	生物医药
332	250004	医药电商
333	251286	疫苗检测溯源
334	251310	青蒿素
335	251323	医疗美容概念
336	251325	中药概念
337	251328	眼科医疗
338	251336	口罩
339	251338	体外诊断概念
340	251339	消毒液
341	251389	长寿药NMN
342	251393	脑科学(脑机接口)
343	251415	辅助生殖
344	251441	CRO
345	252001	新冠检测
346	260001	天然气
347	270002	特钢概念
348	280001	东盟自贸区
349	280002	福建自贸区
350	280004	天津自贸区
351	280005	西安自贸区
352	281404	RCEP概念
353	311023	房地产开发概念
354	311031	房屋租赁
355	B10003	蚂蚁金服概念
356	B10004	白糖
357	B20001	白酒概念
358	B20002	期货概念
359	B50002	健康中国
360	B70001	电力改革
361	B70007	深圳国资改革
362	C10003	风电概念
363	C10006	特高压
364	D10003	棉花
365	D70001	O2O概念
366	GN0004	肝炎概念
367	GN0227	恒大集团概念
368	GN0230	河南国企改革
369	GN2002	虚拟数字人
370	GN2004	新冠药物
371	GN2005	民爆概念
372	GN2006	东数西算/算力
373	GN2007	土壤修复
374	GN2008	智慧灯杆
375	GN2009	PVDF概念
376	GN2010	工业气体
377	GN2011	在线旅游
378	GN2012	低价股
379	GN2013	动力电池回收
380	GN2014	抽水蓄能
381	GN2015	壳资源概念
382	GN2016	刀片电池
383	GN2017	液态金属
384	GN2018	华为汽车
385	GN2019	数据安全
386	GN2020	抖音概念
387	GN2021	共享经济
388	GN2022	云游戏
389	GN2023	互联网医疗
390	GN2024	海南自贸区
391	GN2025	参股保险
392	GN2026	主题公园
393	GN2027	虚拟电厂
394	GN2028	牙科医疗
395	GN2029	汽车芯片
396	GN2030	电子纸
397	GN2031	MicroLED
398	GN2032	华为昇腾
399	GN2033	国资云概念
400	GN2034	数字乡村
401	GN2035	智慧政务
402	GN2036	阿尔茨海默概念
403	GN2037	幽门螺杆菌概念
404	GN2038	仿制药一致性评价
405	GN2039	动物疫苗
406	GN2040	独家药品概念
407	GN2041	EDR概念
408	GN2042	肝素
409	GN2043	信创
410	GN2044	医废处理
411	GN2045	UWB
412	GN2046	磁悬浮
413	GN2047	茅指数
414	GN2048	碳纤维概念
415	GN2049	中俄贸易
416	GN2050	横琴新区
417	GN2051	汽车拆解
418	GN2052	环氧丙烷概念
419	GN2053	物业管理概念
420	GN2054	CIPS概念
421	GN2055	净水概念
422	GN2056	核污染防治
423	GN2057	托育服务
424	GN2058	电子身份证
425	GN2059	新冠抗原检测
426	GN2060	应急产业
427	GN2061	金属回收
428	GN2062	气溶胶检测
429	GN2063	化肥
430	GN2064	铅锌概念
431	GN2065	俄乌冲突概念
432	GN2066	建筑节能概念
433	GN2067	低辐射玻璃
434	GN2068	家庭医生
435	GN2069	6G
436	GN2070	华为鲲鹏
437	GN2071	数字经济
438	GN2073	玉米
439	GN2074	人民币升值受益
440	GN2075	人民币贬值受益
441	GN2076	外贸受益
442	GN2077	油价相关
443	GN2081	中船系
444	GN2082	金融科技
445	GN2083	大基金二期
446	GN2084	统一大市场
447	GN2085	挖掘机
448	GN2086	仪器仪表概念
449	GN2087	化学原料概念
450	GN2088	大豆
451	GN2089	纳米银
452	GN2090	世界杯
453	GN2091	纳入富时罗素
454	GN2092	高低压设备概念
455	GN2093	航空运输概念
456	GN2094	机场概念
457	GN2095	长三角自贸区
458	GN2096	征信
459	GN2097	中非合作
460	GN2098	卫星互联网
461	GN2099	铁矿石概念
462	GN2100	动漫概念
463	GN2101	GDR
464	GN2102	标普道琼斯中国
465	GN2103	大消费
466	GN2104	大央企重组
467	GN2105	中概股回归
468	GN2106	头盔
469	GN2107	智能手表
470	GN2108	钢结构概念
471	GN2109	高速公路概念
472	GN2110	轨道交通
473	GN2111	干细胞
474	GN2112	抗癌
475	GN2113	医保
476	GN2114	光刻胶
477	GN2116	半导体产业
478	GN2117	毫米波
479	GN2118	太赫兹
480	GN2119	手机产业
481	GN2120	消费电子产业
482	GN2121	消费电子代工
483	GN2122	航空发动机
484	GN2123	航天装备概念
485	GN2124	存储器
486	GN2125	涉矿
487	GN2126	生物科技
488	GN2127	双百企业
489	GN2128	中国建材集团
490	GN2129	户外用品（露营）
491	GN2130	新型城镇化建设
492	GN2131	噪音防治
493	GN2132	核酸采样亭
494	GN2133	千金藤素
495	GN2134	方舱医院
496	GN2135	猴痘
497	GN2136	军工集团
498	GN2137	超超临界发电
499	GN2138	高价股
500	GN2139	股权激励
501	GN2141	社保重仓
502	GN2142	破净股
503	GN2143	昨日触板
504	GN2144	比亚迪概念
505	GN2145	F5G
506	GN2146	汽车热管理
507	GN2147	eSIM
508	GN2148	DRG/DIP
509	GN2150	电子车牌
510	GN2151	黑龙江自贸区
511	GN2152	两轮车
512	GN2153	华为欧拉
513	GN2154	粮食概念
514	GN2155	租售同权
515	GN2156	小金属概念
516	GN2157	汽车压铸一体化
517	GN2158	麒麟电池
518	GN2159	钙钛矿电池
519	GN2160	QFII重仓
520	GN2161	26一季报预增
521	GN2162	钒电池
522	GN2163	光伏高速公路
523	GN2164	TOPCon电池
524	GN2165	减速器
525	GN2166	先进封装(Chiplet)
526	GN2167	热泵
527	GN2168	光热发电
528	GN2169	26一季报业绩反转
529	GN2170	昨日首板
530	GN2171	供销社
531	GN2172	气凝胶
532	GN2173	Web3.0
533	GN2174	高压氧舱
534	GN2175	高血压
535	GN2176	广东自贸区
536	GN2177	河南自贸区
537	GN2179	筹码集中100
538	GN2180	参股基金
539	GN2181	园林
540	GN2182	篮球
541	GN2183	虹膜识别
542	GN2184	指纹识别
543	GN2185	手势识别
544	GN2186	生物识别
545	GN2187	精准医疗
546	GN2188	工业自动化
547	GN2189	MCU芯片
548	GN2190	光通信
549	GN2191	重卡
550	GN2192	汽车销售
551	GN2193	醋酸
552	GN2194	液氯
553	GN2195	互联网保险
554	GN2196	AIGC
555	GN2197	复合集流体(PET铜箔)
556	GN2198	人造太阳
557	GN2199	抗病毒面料
558	GN2200	数据要素
559	GN2201	熊去氧胆酸
560	GN2202	PLC概念
561	GN2203	POE胶膜
562	GN2204	第四代半导体
563	GN2205	非酒精性脂肪性肝炎(NASH)
564	GN2206	血氧仪
565	GN2207	轮边电机
566	GN2208	电子后视镜
567	GN2209	成飞概念
568	GN2210	ChatGPT
569	GN2211	共封装光模块(CPO）
570	GN2212	数字水印
571	GN2213	毫米波雷达
572	GN2214	时空大数据
573	GN2215	ERP概念
574	GN2216	行业龙头
575	GN2217	流感
576	GN2218	MLOps概念
577	GN2221	交换机
578	GN2222	AI算力芯片
579	GN2223	服务器
580	GN2224	液冷概念
581	GN2225	中特估
582	GN2226	MR头显
583	GN2228	人工智能大模型
584	GN2229	掌纹识别
585	GN2231	英伟达概念
586	GN2232	空间计算
587	GN2233	富勒烯
588	GN2234	算力租赁
589	GN2235	裸眼3D
590	GN2236	光芯片
591	GN2237	颗粒硅
592	GN2238	人形机器人
593	GN2239	振荡器
594	GN2240	高商誉
595	GN2241	轮毂电机
596	GN2242	空心杯电机
597	GN2243	数据确权
598	GN2244	线控底盘
599	GN2245	锗镓概念
600	GN2246	智能汽车
601	GN2247	小鹏概念
602	GN2248	医疗耗材概念
603	GN2249	机器人执行器概念
604	GN2250	减肥药
605	GN2251	SPD(医疗供应链管理)
606	GN2252	保健品概念
607	GN2253	BC电池
608	GN2254	华为星闪概念
609	GN2255	HEPS概念
610	GN2256	C股(上市次日至五日)
611	GN2257	新型工业化
612	GN2258	细胞免疫治疗
613	GN2259	科创企业同股不同权
614	GN2260	科创企业同股同权
615	GN2261	林业碳汇
616	GN2262	激光
617	GN2263	液冷超充
618	GN2264	教育信息化
619	GN2265	纳米压印
620	GN2266	华为算力
621	GN2267	新疆自贸区
622	GN2268	智能座舱
623	GN2269	短剧/互动游戏
624	GN2270	AI-PIN
625	GN2271	小米汽车
626	GN2272	高带宽存储器HBM
627	GN2273	冰雪概念
628	GN2274	顺周期
629	GN2275	自主可控
630	GN2276	微软合作伙伴
631	GN2277	荣耀手机
632	GN2278	华为汽车股权合作
633	GN2279	希音合作商
634	GN2281	Gemini多模态
635	GN2282	微盘股概念
636	GN2283	元梦之星
637	GN2284	PEEK材料
638	GN2285	合成生物
639	GN2286	可控核聚变
640	GN2287	AIPC
641	GN2288	飞行汽车(eVTOL)
642	GN2289	高股息100
643	GN2290	Sora概念(文生视频)
644	GN2291	SRAM(静态随机存取存储器)
645	GN2292	新质生产力
646	GN2293	AI手机
647	GN2294	低空经济
648	GN2295	磁电存储(MED)
649	GN2296	铜缆高速连接器
650	GN2297	Kimi概念
651	GN2298	AI语料
652	GN2299	5.5G
653	GN2300	通感一体化
654	GN2301	秘塔AI
655	GN2302	军工信息化
656	GN2303	量子计算
657	GN2304	出海50
658	GN2305	玻璃基板封装
659	GN2306	商业航天
660	GN2307	科特估
661	GN2308	科创板做市股
662	GN2309	北交所上市企业
663	GN2310	财税改革
664	GN2311	巴黎奥运会概念
665	GN2312	骨科材料
666	GN2313	AI眼镜
667	GN2314	房屋检测
668	GN2315	一汽系
669	GN2316	中兵系
670	GN2317	中电科系
671	GN2318	中航系
672	GN2319	休闲食品概念
673	GN2320	军工央企
674	GN2321	有色(镁)
675	GN2322	液流电池
676	GN2323	半导体材料概念
677	GN2324	电信运营
678	GN2325	电子签名
679	GN2326	肿瘤治疗
680	GN2327	航天系
681	GN2328	半导体设备概念
682	GN2329	地理信息
683	GN2330	家用护理
684	GN2331	家禽
685	GN2332	有色(钒)
686	GN2333	超硬材料
687	GN2334	有色(锆)
688	GN2335	超级计算机
689	GN2336	有色(锑)
690	GN2337	高端合金
691	GN2338	化债(AMC)
692	GN2339	回购增持再贷款
693	GN2340	并购重组
694	GN2341	智谱AI
695	GN2342	华为盘古
696	GN2343	AI应用
697	GN2344	文创玩具(谷子经济)
698	GN2345	芬太尼概念
699	GN2346	证券IT
700	GN2347	AI编程
701	GN2348	汽车检测
702	GN2349	首发经济
703	GN2350	豆包概念
704	GN2351	消费精选
705	GN2352	微信小店
706	GN2353	小红书概念
707	GN2354	AI智能体
708	GN2355	DeepSeek概念股
709	GN2356	AI医疗概念
710	GN2357	腾讯云概念
711	GN2358	华为手机
712	GN2359	蜜雪冰城概念
713	GN2360	宇树科技概念
714	GN2361	算力一体机
715	GN2362	Manus概念
716	GN2363	深海科技
717	GN2364	有色(铋)
718	GN2365	口含烟
719	GN2366	虚拟机器人
720	GN2367	敦煌网概念
721	GN2368	离境退税概念
722	GN2369	TMT
723	GN2370	磁悬浮压缩机
724	GN2371	中科院系
725	GN2372	智能制造
726	GN2373	无人物流车
727	GN2374	RWA
728	GN2375	旧改
729	GN2376	稳定币概念
730	GN2377	智元机器人
731	GN2378	雅鲁藏布江水电站
732	GN2379	盾构机
733	GN2380	驱蚊概念股
734	GN2381	26一季报预减
735	GN2382	反内卷
736	GN2383	磷化铟晶片
737	GN2384	无人战机
738	GN2385	主营聚乙烯
739	GN2386	新质战斗力
740	GN2387	中核工业集团
741	GN2388	大盘股
742	GN2389	中盘股
743	GN2390	小盘股
744	GN2391	龙头股
745	GN2392	甲骨文概念
746	GN2393	模拟芯片
747	GN2394	电子鼻
748	GN2395	服务消费
749	GN2396	摩尔线程概念
750	GN2397	博通概念
751	GN2398	华为机器人
752	GN2399	防护服
753	GN2400	印巴冲突概念
754	GN2401	垃圾发电
755	GN2402	有色(锡)
756	GN2403	汇金持股
757	GN2404	央企央资
758	GN2405	政府控股
759	GN2406	化工化纤出口
760	GN2407	深地经济
761	GN2408	湖北国企改革
762	GN2409	固液电池
763	GN2410	钍基熔盐堆
764	GN2411	黑神话概念
765	GN2412	谷歌概念
766	GN2413	陕西国企改革
767	GN2414	太空算力
768	GN2415	SpaceX概念
769	GN2416	燃气轮机
770	GN2417	电子特气
771	GN2418	AI营销
772	GN2419	AMD概念
773	GN2420	尼帕病毒
774	GN2421	太空光伏
775	GN2422	电子布
776	GN2423	昨日高振幅
777	GN2424	昨日高换手
778	GN2425	红利破净
779	GN2426	红利股
780	GN2427	微利股
781	GN2428	周期股
782	GN2429	价值股
783	GN2430	HALO
784	GN2431	OpenClaw概念
785	GN2432	航海装备概念
786	GN2433	IT服务概念
787	GN2434	词元概念
788	GN2435	光纤概念
789	GN2436	算电协同
790	GN2437	双氧水概念
791	GN2438	CPU概念
792	GN2439	陶瓷基板
793	GN2440	煤矿安全
##############################################
# 常见问题
关于量化平台部署
关于量化环境
PTrade客户端为本地运行，但量化模块为云端部署方式，客户端通过http或https方式链接云服务器。

关于策略安全
客户策略部署在券商服务器，策略文件加密存储。利用Docker容器技术，隔离多账号运行空间，有效分配各用户账号运行环境，保证策略运行环境与资源使用的独立性。

Mac是否支持
Mac目前不支持，只能在Windows环境下。

关于付费
云纪网络提供的仿真环境目前为免费使用，包括所有数据、回测资源、模拟交易资源。券商部署环境以券商发布的使用条件为准。

关于程序语言
PTrade量化目前仅支持Python语言编程。

关于Python版本
目前支持Python3.11.4。

关于数据
数据种类
在研究、回测、交易模块均可调用2005年以来的历史财务数据以及历史行情数据，包含分钟、日线、周线不同周期数据。交易场景还支持tick级别行情快照数据。数据支持股票、可转债、指数等多品种。

关于数据读写
研究环境可以存放文件，根目录路径为'/home/fly/notebook/'，可通过get_research_path接口获取。回测和交易中均可以通过该路径进行策略中的读写等操作，从而实现数据的保存和读取。

关于本地数据
由于PTrade为云端部署，策略中是无法与本地路径进行直接交互的。

关于行情数据除复权
PTrade行情数据支持不复权、前复权、后复权、动态前复权四种取历史行情数据的方法，但要注意的是回测中回测引擎撮合的价格是不复权的，因此可以通过除权因子进行价格除权处理。

关于level2数据
云纪网络的仿真环境不提供level2数据，券商环境是否提供，由所在券商决定。

关于研究
研究环境资源
目前单个的客户研究环境资源没有上限。

文件传输限制
单个文件手动上传下载目前限制单个文件数据大小不超过50M。

关于定时上传功能
定时上传功能可以实现研究环境自动从本地路径读取文件，但上传次数是有限制的（具体由券商配置决定），因此仍不能支持高频的策略中调用本地数据场景。

定时上传功能目前限制单个文件数据大小不超过50M。

上传文件夹
暂时不支持文件夹上传，文件需要逐个上传。

关于回测
回测与研究有什么区别
研究环境更侧重于数据的清洗、处理、建模、画图、debug 调试等，类似于本地的Python 编程，无法调用诸如order下单，账户资产等等与交易相关的函数。回测环境则更适用于完成完整的交易策略搭建、参数调优、历史收益回测等，更贴近交易。一般的，研究环境适用于对程序有调试需求，需要知道每一步程序执行的结果的用户，而回测则更适用于想知道策略在历史时间段内的收益如何，以便对策略参数甚至是构建思想进行调优的用户。

回测个数
目前支持同时进行5个回测。

回测的速度
PTrade量化中部分接口为在线调用接口，调用速度会受瞬时网络情况影响，比如get_fundamentals、get_Ashares，回测中按实际需求尽量少频次地调用这类在线调用接口。另外分钟级别策略中如果用到日频的历史数据，在before_trading_start模块处理一次就可以，这样可以提升回测的速度。

关于回测周期
目前回测只支持分钟和日线周期的回测。

关于调试功能
量化分步调试功能可以帮助开发者更高效地debug策略代码。该功能在回测模块中，支持调用堆栈查询、变量监视、本地变量查询功能。





关于性能分析
性能分析功能会对运行结果做分析，包括语句的触发次数和耗时情况，能够帮助用户快速地做策略性能优化。







关于离线回测
PTrade量化平台目前不支持离线回测，回测期间必须保障客户端打开。

关于策略上传和下载
PTrade量化平台所创建的策略是可以加密下载和上传的，我们利用AES/DES加密技术对文件流进行加密处理，随机生成盐值进行干扰混淆，保障上传与下载安全私密性。该功能的用途在于支持同一策略在不同账户上实现隐藏代码地进行模拟交易。

操作方法：

一、选定策略，点鼠标右键，选择下载，然后将策略保存到指定路径，下载的文件为zip格式，下载后不要做解压。 可以对该zip文件做重命名也可以不做处理，对于上传没有影响。



二、点击交易中的上传策略。 上传的策略我们可以在回测的策略列表中查询到，策略名称跟下载时候的策略名称保持一致，假如与原策略列表中出现重名，也不会报错。上传策略不允许修改策略名称，且不允许修改策略代码。上传的策略不可以做回测，仅能用来开启交易。



回测撮合是否受真实成交限制
回测提供了两种成交撮合方式，通过set_limit_mode接口控制，一种是按初始化设定的分钟成交量比例进行成交撮合，另一种是不受分钟成交量限制。前者可以较为真实地反映流动性对策略的影响，后者比较适合低频调仓策略，比如基本面月频调仓策略之类。

获取每次回测代码
在回测记录中找到目标回测记录，在‘操作’栏中点击详情按钮获得回测代码。



关于模拟交易
模拟交易个数
默认允许同时运行5个交易，具体以券商配置为准。

交易过程可以客户端离线吗
交易在服务器上运行，因此客户端关闭或掉线并不影响策略运行。

不同交易的账户管理
所有运行的模拟交易或实盘交易都共享一个账户（资金、持仓无法隔离），暂不支持子账户交易系统。

交易开启的时间
交易在任何时间都可以开启，开启后会立刻运行initialize和before_trading_start（如果策略中定义的话），要注意的是：开盘前开启交易，before_trading_start肯定会先于handle_data开启；但开盘期间开启交易，before_trading_start和handle_data可能会同时运行，策略逻辑防止混乱。

策略中模块的运行顺序
交易中before_trading_start、handle_data、tick_data、run_interval都是独立的线程，当交易开启之后，每个线程都会启动，理论上没有先后顺序关系。因此建议在策略中设置强制顺序的控制系统，比如运行完before_trading_start后打开handle_data的运行开关，运行完handle_data后打开tick_data或者run_interval的运行开关。

重启功能
重启功能和新建交易本质上是一样的，会重新创建交易id，原策略中的内存变量如果不做保存会清除。

回测与交易代码兼容
由于交易中支持tick数据以及市价单下单，因此大多数情况下回测和交易在代码设计上会有不同。为了减少代码维护的难度，PTrade量化提供了is_trade接口。通过该接口，用户可以在一套代码中兼容回测和交易两种逻辑。

关于模拟交易的稳定性
常见的影响交易稳定性的因素来自以下几方面：

1、历史行情K线数据服务器更新异常。这种情况往往可以通过比较入参的K线数量、实际返回数据框的长度、时间戳index去重后的返回数据框的长度来做判断（看三者是否保持一致）。

2、实时行情数据获取失败。实时行情源的推送并不能保证一直稳定，因此需要做数据保护：比如

def initialize(context):
    # 初始化此策略
    # 设置我们要操作的股票池, 这里我们只操作一支股票
    g.security = ['600570.SS','600571.SS']
    set_universe(g.security)
    #每3秒运行一次主函数
    run_interval(context, func, seconds=3)
    
def func(context):
    for stock in g.security:
        #获取最新价
        snapshot = get_snapshot(stock)
        # 非空判断
        if snapshot[stock]:
            # 字段数据做保护
            price = snapshot[stock].get('last_px', 0)
            if price == 0:
                log.info((stock,'该股在本tick行情数据异常，不进行判断'))
                continue
            order(stock, 100, limit_price=price)

def handle_data(context, data):
    pass
3、财务数据获取失败。财务数据接口是在线向数据源调用的接口，瞬时调用量过大或者其他导致网络堵塞的原因都有可能使得获取失败，因此建议加入重连机制做保护（可参考单因子demo）。

4、服务器环境异常。这种情况是用户主观不能控制的，但可以通过持久化处理，让策略在短暂停止后，重新拉起并保持原有的策略逻辑连贯（可参考持久化说明）。

关于模拟交易的账户数据更新频率
模拟交易和实盘交易的账户数据同步理论上是6秒一次，包括资金、持仓、订单状态、撤单状态等。因此用户需要自建一定的中间变量做过度，防止重复交易或者重复判断。

tick_data和run_interval的关系
tick_data和run_interval都可以实现tick级别周期策略，tick_data固定3秒一个间隔，run_interval可以随意设置运行间隔时间，最小间隔3秒，数据源也都是行情快照数据，因此可以选择其一进行策略设计。

关于实盘交易
如何开通实盘
向开展PTrade量化业务的所在券商进行申请。

实盘与模拟交易区别
模拟交易和实盘交易在数据获取的机制上是一致的，只是成交撮合机制不同。

关于委托
实时行情获取失败导致委托失败
限价委托接口包括order、order_target、order_value、order_target_value，如果不入参限价字段limit_price，引擎会默认以将行情最新价报单要，碰到行情异常快照数据推送为空的时候，下单会失败形成废单，日志中会有提醒，可以通过废单逻辑判断来进行二次委托。

委托数量校验
委托接口有委托数量校验，如果数量不是整数，会下单失败返回None。

集合竞价下单
已支持，参考集合竞价demo。

委托状态如何监控
get_orders接口可以获取当日本策略的所有订单信息（6秒同步更新），交易模块还可调用on_trade_response接口获取成交回报主推。

手动委托单策略中能否撤单
通过get_all_orders接口获取账户当日全部订单，再结合cancel_order_ex撤单接口，可以对手动委托单进行撤单。

关于三方库
查询支持的三方库
研究中输入 !pip list 即可查询到目前PTrade所支持的所有三方库及其版本。

三方库更新
目前暂不支持用户对三方库的自主更新。

其他
关于调用自有包
策略中不支持调包，也不支持跨策略调用函数，因此一个策略只能在一个文件中实现。

关于连接自己的数据库
因合规要求，目前不支持对本地数据库读写。可以在研究环境上传db文件，通过Python自带库包sqlite进行数据库读写操作。

如何将信号推送给自己
可通过邮件、企业微信接口实现，因该业务需要开通外网，实际看券商环境是否支持。

关于OS
os模块目前无法使用。

关于快速地获取最新价
在回测中建议用data[stock].price（注意这种方法取到的是不复权数据），交易中用get_snapshot接口获取行情快照的最新价。

关于日线策略运行时间
回测中是15:00执行；交易中默认设置是14:50分，具体看所在券商的配置。

关于get_history中的include参数
get_history中的include参数默认为False，如果设置为True，则返回包含当前周期的数据。日线周期（或以上级别）策略的回测场景设置include参数为True获取当日数据，可以使得回测更加快速便捷，其他场景建议谨慎使用该参数。

关于基准设置
基准支持设置为指数/个股/ETF，可参阅set_benchmark。

策略里如何实现跨周期处理
可以通过run_interval和handle_data相结合实现，根据策略逻辑进行编写。

关于requests
目前不能使用requests。

关于批量委托性能
策略发起委托到柜台接收的速度，测试结果：300笔委托耗时2秒。