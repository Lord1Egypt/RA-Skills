---
name: ptrade-strategy
description: |
  国金 PTRADE 量化平台策略生成技能。根据用户需求，
  生成可在 PTRADE 平台运行�?Python 量化交易策略代码�?
  触发关键词：PTRADE、ptrade、量化策略、量化交易、生成策略、写策略代码�?
metadata:
  openclaw:
    emoji: "📈"
---

# PTRADE 量化策略生成 Skill

## 概述

�Skill 从知识库「国金量化」中读取 PTRADE API 文档，为用户生成或修改可在 PTRADE 平台运行的量化交易策略代码

**⚠️ 核心API说明：PTRADE 使用 `get_price()` 全局函数获取K线数据，不是 `security.get_bars()`**

---

## 一、策略必备函数（必写）

```python
initialize(context)               # 初始化（必写�?
handle_data(context, data)       # 行情/交易主函数（必写�?
before_trading_start(context, data)   # 盘前运行
after_trading_end(context, data)      # 盘后运行
tick_data(context, data)         # Tick 级别处理
on_order_response(context, order_list)  # 委托回调
on_trade_response(context, trade_list)  # 成交回调
```

---

## 二、设置类 API

```python
set_universe(security_list)       # 设置股票�?
set_benchmark(sids)              # 设置基准指数
set_commission(commission_ratio, min_commission, type)  # 设置佣金
set_fixed_slippage(fixedslippage)  # 设置固定滑点
set_slippage(slippage)           # 设置滑点比例
set_volume_ratio(volume_ratio)   # 设置成交量限制比�?
set_limit_mode(limit_mode)        # 设置涨跌停模�?
set_yesterday_position(poslist)   # 设置昨日持仓
set_parameters(**kwargs)          # 设置策略参数
set_email_info(email_address, smtp_code, email_subject)  # 设置邮件
```

---

## 三、定时或周期 API

```python
run_daily(context, func, time='9:31')    # 每日定时执行
run_interval(context, func, seconds=10) # 间隔执行（秒�?
```

---

## 四、获取信息类 API

### 4.1 基础信息

```python
get_trading_day(day)             # 获取第N个交易日
get_all_trades_days(date=None)   # 获取所有交易日
get_trade_days(start_date=None, end_date=None, count=None)  # 获取日期范围交易�?
get_trading_day_by_date(query_date, day=0)  # 按日期查询交易日
```

### 4.2 市场信息

```python
get_market_list()                # 获取市场列表
get_market_detail(finance_mic)   # 获取市场详情
```

### 4.3 行情信息

```python
# 获取历史K线（核心API�?
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

# 涨跌停股�?
get_trend_data(date=None, stocks=None, market=None)
```

### 4.4 证券信息

```python
get_stock_name(stocks)           # 获取股票名称
get_stock_info(stocks, field=None)  # 获取股票基本信息
get_stock_status(stocks, query_type='ST', query_date=None)  # 获取股票状�?
get_underlying_code(symbols)    # 获取正股代码
get_stock_exrights(stock_code, date=None)  # 获取复权因子
get_stock_blocks(stock_code)     # 获取股票所属板�?
get_index_stocks(index_code, date)  # 获取指数成分�?
get_industry_stocks(industry_code)  # 获取行业成分�?
get_fundamentals(security, table, fields=None, date=None, start_year=None, end_year=None, report_types=None, merge_type=None, is_dataframe=False)  # 财务数据
get_Ashares(date=None)           # 获取全部A�?
get_etf_list()                   # 获取ETF列表
get_etf_info(etf_code)           # 获取ETF信息
get_etf_stock_list(etf_code)     # 获取ETF成分�?
get_etf_stock_info(etf_code, security)  # 获取ETF成分股信�?
get_ipo_stocks()                 # 获取今日可申购新�?
get_cb_list()                    # 获取可转债列�?
get_cb_info()                    # 获取可转债信�?
get_reits_list(date=None)        # 获取REITs列表
```

---

## 五、交易API

### 5.1 股票交易

```python
order(security, amount, limit_price=None)        # 限价委托
order_target(security, amount, limit_price=None) # 目标仓位
order_value(security, value, limit_price=None)   # 目标市�?
order_target_value(security, value, limit_price=None)  # 目标市�?
order_market(security, amount, market_type, limit_price=None)  # 市价委托
ipo_stocks_order(submarket_type=None, black_stocks=None)  # 新股申购
after_trading_order(security, amount, entrust_price)  # 盘后委托
after_trading_cancel_order(order_param)  # 盘后撤单
etf_basket_order(etf_code, amount, price_style=None, position=True, info=None)  # ETF篮子委托
etf_purchase_redemption(etf_code, amount, limit_price=None)  # ETF申购赎回
```

### 5.2 公共交易

```python
order_tick(sid, amount, priceGear='1', limit_price=None)  # 逐笔委托
cancel_order(order_param)           # 撤单
cancel_order_ex(order_param)        # 增强撤单
debt_to_stock_order(security, amount)  # 转债转�?
```

### 5.3 融资融券

```python
margin_trade(security, amount, limit_price=None, market_type=None)  # 融资融券
margincash_open(security, amount, limit_price=None, market_type=None, cash_group=None)  # 融资开�?
margincash_close(security, amount, limit_price=None, market_type=None, cash_group=None)  # 融资平仓
margincash_direct_refund(value, cash_group=None)  # 融资直接还款
marginsec_open(security, amount, limit_price=None, cash_group=None)  # 融券开�?
marginsec_close(security, amount, limit_price=None, market_type=None)  # 融券平仓
marginsec_direct_refund(security, amount, cash_group=None)  # 融券直接还券
```

### 5.4 期货

```python
buy_open(contract, amount, limit_price=None)      # 期货开�?
sell_close(contract, amount, limit_price=None, close_today=False)  # 期货平多
sell_open(contract, amount, limit_price=None)    # 期货开�?
buy_close(contract, amount, limit_price=None, close_today=False)  # 期货平空
```

---

## 六、查询持仓/订单/成交

```python
get_position(security)             # 获取单只股票持仓
get_positions(security)           # 获取指定股票持仓
get_all_positions()               # 获取所有持�?
get_open_orders(security=None)    # 获取未成交订�?
get_order(order_id)               # 获取订单详情
get_orders(security=None)         # 获取订单列表
get_all_orders(security=None)     # 获取所有订�?
get_trades()                      # 获取成交记录
get_deliver(start_date, end_date) # 获取交割�?
get_fundjour(start_date, end_date) # 获取资金流水
get_lucky_info(start_date, end_date)  # 获取中签信息
```

---

## 七、计算/指标 API

```python
get_MACD(close, short=12, long=26, m=9)
get_KDJ(high, low, close, n=9, m1=3, m2=3)
get_RSI(close, n=6)
get_CCI(high, low, close, n=14)
```

---

## 八、其他工具API

```python
log.debug/info/warning/error/critical()  # 日志输出
is_trade()                    # 是否交易时间
check_limit(security, query_date=None)  # 检查涨跌停
send_email(...)               # 发送邮件
send_qywx(...)                # 发送企业微信
permission_test(account=None, end_date=None)  # 权限测试
create_dir(user_path)         # 创建目录
get_frequency()              # 获取K线周期
get_business_type()          # 获取业务类型
get_current_kline_count()    # 获取当前K线根
filter_stock_by_status(stocks, filter_type=["ST","HALT","DELISTING"], query_date=None)  # 按状态过滤
check_strategy(strategy_content=None, strategy_path=None)  # 检查策略
fund_transfer(trans_direction, occur_balance, exchange_type="1")  # 资金划转
market_fund_transfer(exchange_type, occur_balance)  # 市场间资金划转
get_research_path()          # 获取研究模块路径
get_trade_name()             # 获取交易账户名称
get_user_name(login_account=True)  # 获取用户名称
```

---

## 九、全部数据结构（对象）

```python
# g 全局对象（在 initialize 中使用）
g = {}  # 自定义全局变量

# Context 上下问
context.portfolio           # 资产对象
context.portfolio.cash      # 可用现金
context.portfolio.total_value  # 总资产
context.portfolio.positions # 持仓dict
context.blotter.current_dt  # 当前时间

# BarData K线数�?
# DataFrame 列：open, close, high, low, volume, price, preclose, high_limit, low_limit

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

## 十、数据字典（状态常量）

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

## 策略模板

### 模板 1：日线双均线策略

```python
import numpy as np

SECURITY = "000001.XSHG"
SHORT_WIN = 5
LONG_WIN = 20

def initialize(context):
    set_benchmark("000300.XSHG")
    set_universe([SECURITY])
    set_commission(0.00025, 5.0)
    set_slippage(0.002)
    log.info(f"双均线策略| 标的={SECURITY}")

def handle_data(context):
    sym = SECURITY
    
    # 获取K�?
    df = get_price(sym, frequency="1d", fields=["close"], count=LONG_WIN + 5)
    close = df["close"].values
    
    short_ma = np.mean(close[-SHORT_WIN:])
    long_ma = np.mean(close[-LONG_WIN:])
    
    # 金叉买入
    if short_ma > long_ma and close[-2] <= close[-3] * 0.995:
        order(sym, 100, 0)
    
    # 死叉卖出
    if short_ma < long_ma:
        order(sym, -100, 0)
```

### 模板 2：布林带策略

```python
import numpy as np

SECURITY = "000001.XSHG"
BOLL_PERIOD = 20
BOLL_STD = 2.0

def initialize(context):
    set_benchmark("000300.XSHG")
    set_universe([SECURITY])

def handle_data(context):
    sym = SECURITY
    df = get_price(sym, frequency="1d", fields=["close"], count=BOLL_PERIOD + 5)
    close = df["close"].values
    current = float(close[-1])
    
    period = close[-BOLL_PERIOD:]
    boll_mid = np.mean(period)
    boll_std = np.std(period, ddof=1)
    upper = boll_mid + BOLL_STD * boll_std
    lower = boll_mid - BOLL_STD * boll_std
    
    if current <= lower:
        order(sym, 100, 0)  # 低吸
    elif current >= upper:
        order(sym, -100, 0)  # 高抛
```

### 模板 3：止损止盈策�?

```python
STOP_LOSS = 0.05   # 止损5%
TAKE_PROFIT = 0.15  # 止盈15%

def handle_data(context):
    sym = "000001.XSHG"
    pos = context.portfolio.positions.get(sym)
    
    if pos and pos.total_amount > 0:
        df = get_price(sym, frequency="1d", fields=["close"], count=1)
        current = float(df["close"].iloc[-0])
        cost = float(pos.cost_basis)
        profit = (current - cost) / cost
        
        if profit <= -STOP_LOSS:
            order(sym, -int(pos.enable_amount), 0)  # 止损
        elif profit >= TAKE_PROFIT:
            order(sym, -int(pos.enable_amount), 0)  # 止盈
```

---

## 生成策略流程

1. **理解需求：确认策略类型（选股/择时/套利/事件驱动�?
2. **确认 API**：严格使用本 skill 中的函数
3. **套用模板**：从上方模板库选择或自行编制
4. **代码生成**：输出完整的 `initialize` + `handle_data` 代码
5. **说明要点**：附PTRADE 平台运行说明

