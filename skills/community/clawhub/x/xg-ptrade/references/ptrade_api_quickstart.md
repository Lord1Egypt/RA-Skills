# Ptrade API 快速入门手册

## 一、策略生命周期函数

### 必选函数

#### 1. initialize(context) - 初始化函数
| 属性 | 说明 |
|------|------|
| 执行时机 | 策略启动时运行一次 |
| 作用 | 初始化股票池、全局变量、参数配置 |
| 是否必选 | **必选** |
| 可用模块 | 回测、交易 |

**示例代码：**
```python
def initialize(context):
    g.security = '600570.SS'  # 设置股票池
    set_universe(g.security)
    g.ma_short = 5  # 设置均线参数
2. handle_data(context, data) - 盘中处理函数
表格属性说明执行时机每分钟/每天执行一次作用交易逻辑判断、下单操作是否必选必选可用模块回测、交易 
示例代码：
pythondef handle_data(context, data):
    # 获取当前价格
    current_price = data[g.security]['close']
    # 获取可用资金
    cash = context.portfolio.cash
    # 买入操作
    if 条件:
        order_value(g.security, cash)
可选函数
表格函数名执行时机作用可用模块before_trading_start(context, data)每天开盘前（8:30/9:10）盘前初始化 回测、交易after_trading_end(context, data)每天收盘后（15:30）盘后处理回测、交易tick_data(context, data)每3秒执行一次（9:30~14:59）Tick级别交易仅交易on_order_response(context, order_list)委托主推回调时 实时处理委托仅交易on_trade_response(context, trade_list)成交主推回调时 实时处理成交仅交易

二、设置函数
表格函数名参数说明可用模块set_universe(security_list)股票代码列表设置股票池 回测、交易set_benchmark(sid)基准代码设置比较基准（默认沪深300） 回测、交易 set_commission(ratio, min, type)费率、最低佣金、类型 设置佣金费率 仅回测set_slippage(slippage)滑点比例 设置滑点（默认0.1%） 仅回测set_fixed_slippage(fixedslippage)固定滑点 设置固定滑点 仅回测set_volume_ratio(volume_ratio)成交比例 设置单笔成交比例（默认0.25） 仅回测set_limit_mode(limit_mode)'LIMIT'/'UNLIMITED'设置成交数量限制模式 仅回测set_yesterday_position(poslist)持仓列表 设置回测初始底仓仅回测

三、定时周期性函数
1. run_daily(context, func, time='9:31')

作用：按日周期运行指定函数
可用模块：回测、交易
注意事项：

只能在 initialize 中调用
可以多次设定，实现多个定时任务
回测分钟级策略：time 取值在 09:31~11:30 与 13:00~15:00
交易场景：time 可设置范围 00:00~23:59

示例：
pythondef initialize(context):
    run_daily(context, my_func, time='14:50')

def my_func(context):
    log.info("定时任务执行")
2. run_interval(context, func, seconds=10)

作用：按设定时间间隔运行指定函数
可用模块：仅交易
注意事项：

只能在 initialize 中调用
最小时间间隔为 3 秒
可以多次设定，会以多个线程并行运行

示例：
pythondef initialize(context):
    run_interval(context, my_func, seconds=10)

def my_func(context):
    log.info("周期任务执行")

四、行情获取函数
1. get_history(count, frequency, field, security_list, fq, include, fill)

作用：获取最近N条历史行情K线数据
可用模块：回测、交易
支持频率：1m、5m、15m、30m、60m、120m、1d、1w、mo、1q、1y
支持字段：open、high、low、close、volume、money、price、preclose、high_limit、low_limit

示例：
python# 获取5日收盘价
df = get_history(5, '1d', 'close', '600570.SS')
# 获取前复权数据
df = get_history(5, '1d', 'close', '600570.SS', fq='pre')
2. get_price(security, start_date, end_date, frequency, fields, fq, count)

作用：获取指定时间段的历史行情数据
可用模块：研究、回测、交易
注意事项：start_date 与 count 必须二选一

示例：
python# 获取指定时间段的日线数据
df = get_price('600570.SS', start_date='20230101', end_date='20231231')
# 获取最近10天的数据
df = get_price('600570.SS', end_date='20231231', count=10)
3. get_snapshot(security)

作用：获取实时行情快照
可用模块：仅交易

返回字段：
表格字段说明last_px最新成交价open_px今开盘价 high_px最高价low_px最低价preclose_px昨收价 up_px涨停价格down_px跌停价格trade_status交易状态 

五、交易函数
基本交易函数
表格函数名参数说明可用模块order(security, amount, price)代码、数量、价格按数量买卖回测、交易order_target(security, amount, price)代码、目标数量、价格调整到目标持仓数量回测、交易order_value(security, value, price)代码、价值、价格按金额买卖回测、交易order_target_value(security, value, price)代码、目标市值、价格调整到目标持仓市值回测、交易cancel_order(order_id)订单ID撤单回测、交易
交易场景专用函数
表格函数名说明可用模块order_market(security, amount, market_type)市价委托仅交易ipo_stocks_order(market_type)新股一键申购仅交易order_tick(security, amount, direction)Tick级别下单（仅tick_data中使用） 仅交易

六、持仓查询函数
表格函数名参数说明get_position(security)股票代码获取单只股票持仓get_positions(security)股票代码列表获取多只股票持仓 get_order(order_id)订单ID获取单个订单get_orders(security)股票代码获取所有订单get_open_orders(security)股票代码获取未成交订单get_trades(security)股票代码获取成交记录

七、股票信息函数
表格函数名参数说明get_stock_name(stocks)股票代码获取股票名称 get_stock_info(stocks, field)股票代码、字段获取股票基础信息 get_stock_status(stocks, query_type, date)代码、类型、日期获取ST/停牌/退市状态 get_stock_blocks(stock_code)股票代码获取股票所属板块 get_index_stocks(index_code, date)指数代码、日期 获取指数成分股 get_industry_stocks(industry_code)行业代码获取行业成分股 

八、财务数据函数
get_fundamentals(security, table, fields, date, ...)

作用：获取财务三大报表数据、估值数据、财务能力指标
可用模块：研究、回测、交易

支持的表名：
表格表名说明valuation估值数据balance_statement资产负债表income_statement利润表cashflow_statement现金流量表growth_ability成长能力指标profit_ability盈利能力指标eps每股指标operating_ability营运能力指标 debt_paying_ability偿债能力指标

九、常用代码模板
模板1：基础双均线策略
pythondef initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)
    g.ma_short = 5
    g.ma_long = 10
    g.is_bought = False

def handle_data(context, data):
    security = g.security
    df = get_history(10, '1d', 'close', security)
    if df is None or len(df) < 10:
        return
    close_prices = df['close'].values
    ma_short = close_prices[-g.ma_short:].mean()
    ma_long = close_prices[-g.ma_long:].mean()
    cash = context.portfolio.cash
    position = get_position(security)
    pos_amount = 0 if position is None else position.amount
    
    if ma_short > ma_long and not g.is_bought and cash > 0:
        order_value(security, cash)
        g.is_bought = True
    elif ma_short < ma_long and g.is_bought and pos_amount > 0:
        order_target(security, 0)
        g.is_bought = False
模板2：定时获取财务数据
pythondef initialize(context):
    g.security = '600570.SS'
    set_universe(g.security)
    run_daily(context, get_finance_data, time='14:50')

def get_finance_data(context):
    data = get_fundamentals(g.security, 'balance_statement', 'total_assets')
    log.info("资产总计: %s" % data)

def handle_data(context, data):
    pass

十、常见错误与解决方法
表格错误信息原因解决方法"股票不在股票池中"股票未在set_universe中设置添加股票到set_universe() "最小下单数量不足"股票<100股，可转债<10张增加下单数量"行情数据获取失败"股票停牌或行情服务异常检查股票状态，稍后重试"资金不足"买入金额超过可用资金检查资金余额，降低买入金额"持仓不足"卖出数量超过持仓数量检查持仓数量，使用order_target卖出"策略中的函数未定义"缺少initialize或handle_data 添加必选函数

---

### 6. references/strategy_notes.md（策略说明与注意事项）

```markdown
# 双均线策略说明与注意事项

## 一、策略概述

### 策略名称
**小果量化双均线策略**

### 策略原理
双均线策略是最经典的量化交易策略之一，基于**移动平均线**的金叉死叉信号进行交易。

- **金叉（买入信号）**：短期均线上穿长期均线，表示上涨趋势开始
- **死叉（卖出信号）**：短期均线下穿长期均线，表示下跌趋势开始

### 策略参数
| 参数 | 默认值 | 说明 |
|------|--------|------|
| 短期均线周期 | 5 | 5日均线（MA5） |
| 长期均线周期 | 10 | 10日均线（MA10） |
| 交易标的 | 600570.SS | 恒生电子 |
| 买入方式 | 全仓买入 | 使用全部可用现金 |
| 卖出方式 | 全部卖出 | 清空该股票持仓 |

---

## 二、回测注意事项

### 2.1 回测参数设置
| 参数 | 建议值 | 说明 |
|------|--------|------|
| 起始资金 | 1,000,000元以上 | 避免资金不足导致无法买入 |
| 回测时间 | 至少1年 | 确保有足够的数据产生交易信号 |
| 回测频率 | 日线 | 双均线策略适合日线级别 |
| 回测基准 | 沪深300（000300.SS） | 用于计算Alpha、Beta等指标 |

### 2.2 佣金和滑点
| 参数 | 默认值 | 建议值 | 说明 |
|------|--------|--------|------|
| 佣金费率 | 万分之三 | 万分之三 | 最低5元 |
| 滑点比例 | 0.1% | 0.1%~0.2% | 模拟真实交易成本 |
| 成交比例 | 0.25 | 0.25 | 单笔最大成交比例 |

### 2.3 停牌处理
- 停牌日成交量为0
- 复盘后价格可能跳空（开盘价与停牌前收盘价差距大）
- 建议在策略中增加停牌判断逻辑

### 2.4 数据限制
- 只能获取2005年后的数据
- 分钟线数据只支持当天查询
- 财务数据有获取频率限制（每秒不超过100次）

---

## 三、实盘交易注意事项

### 3.1 交易时间
| 时间段 | 说明 |
|--------|------|
| 9:15~9:25 | 集合竞价（可下单，9:30统一报单） |
| 9:30~11:30 | 上午连续交易 |
| 11:30~13:00 | 午间休市 |
| 13:00~15:00 | 下午连续交易 |
| 15:00~15:30 | 盘后固定价交易 |

### 3.2 涨跌停限制
- 股票涨停时无法买入，跌停时无法卖出
- 下单前应使用 `get_snapshot()` 获取涨停价和跌停价
- 涨停价 = 昨收价 × 1.10（普通股票）
- 跌停价 = 昨收价 × 0.90（普通股票）

### 3.3 资金管理建议
- **不要全仓买入**：建议分批建仓，每次买入总资金的20%~30%
- **设置止损**：建议设置5%~10%的止损线
- **控制仓位**：单只股票持仓不超过总资金的50%

### 3.4 日志记录
- 使用 `log.info()` 记录关键操作
- 记录每次买卖的时间、价格、数量
- 记录账户资金变化和持仓变化

---

## 四、策略优化方向

### 4.1 增加过滤条件
| 优化方向 | 说明 | 实现方式 |
|----------|------|----------|
| 成交量过滤 | 放量突破时买入，缩量上涨时谨慎 | 比较当前成交量与均量 |
| 趋势过滤 | 只在上升趋势中做多 | 使用200日均线判断趋势方向 |
| 波动率过滤 | 波动率过高时避免交易 | 使用ATR指标衡量波动率 |

### 4.2 增加风险管理
| 风险控制 | 说明 | 实现方式 |
|----------|------|----------|
| 止损止盈 | 固定比例止损止盈 | 持仓亏损5%止损，盈利10%止盈 |
| 移动止损 | 跟随趋势调整止损线 | 使用布林带或ATR设置动态止损 |
| 仓位管理 | 根据市场情况调整仓位 | 市场好时加仓，差时减仓 |

### 4.3 引入技术指标组合
| 指标 | 说明 | 用法 |
|------|------|------|
| MACD | 趋势跟踪指标 | MACD金叉+均线金叉双重确认 |
| RSI | 超买超卖指标 | RSI<30为超卖买入信号 |
| 布林带 | 波动率指标 | 价格触及下轨时买入 |

### 4.4 多股票组合
- 选择5~10只相关性低的股票
- 每个股票分配相同权重
- 降低单只股票风险

---

## 五、常见问题解答

### Q1：为什么回测结果很好，实盘却亏损？
**可能原因**：
1. 回测未考虑滑点、佣金等交易成本
2. 回测假设立即成交，实盘有延迟
3. 市场环境变化（趋势变为震荡）

**解决建议**：
1. 回测时设置合理的滑点和佣金
2. 使用分钟线回测更接近实盘
3. 增加策略适应不同市场环境的机制

### Q2：如何避免虚假信号？
**解决方法**：
1. 增加成交量确认（放量突破更可靠）
2. 使用更大周期的均线过滤（如MA20作为趋势判断）
3. 等待收盘价确认（避免盘中假突破）

### Q3：如何在策略中处理停牌？
**解决方法**：
```python
def handle_data(context, data):
    # 获取股票状态
    status = get_stock_status([g.security], 'HALT')
    if status.get(g.security) is True:
        log.info("股票停牌，跳过交易")
        return
    # 正常交易逻辑
Q4：如何获取多只股票的数据？
解决方法：
python# 设置多只股票
g.security = ['600570.SS', '000001.SZ', '000002.SZ']
set_universe(g.security)

# 获取历史数据
df = get_history(5, '1d', 'close', security_list=g.security)

六、策略代码优化建议
6.1 代码结构优化
python# 不好的写法：所有逻辑都在handle_data中
def handle_data(context, data):
    # 100行代码...

# 好的写法：拆分函数
def handle_data(context, data):
    if not should_trade(context, data):
        return
    signal = generate_signal(context, data)
    execute_trade(context, signal)

def should_trade(context, data):
    # 检查是否应该交易
    pass

def generate_signal(context, data):
    # 生成交易信号
    pass

def execute_trade(context, signal):
    # 执行交易
    pass
6.2 错误处理优化
python# 不好的写法：没有错误处理
df = get_history(5, '1d', 'close', '600570.SS')
ma5 = df['close'].mean()

# 好的写法：增加错误处理
try:
    df = get_history(5, '1d', 'close', '600570.SS')
    if df is None or len(df) < 5:
        log.warning("数据不足")
        return
    ma5 = df['close'].mean()
except Exception as e:
    log.error("获取数据时出错: %s" % str(e))
    return
6.3 日志管理优化
python# 不好的写法：日志过多
log.info("当前价格: " + str(price))
log.info("当前MA5: " + str(ma5))
log.info("当前MA10: " + str(ma10))

# 好的写法：格式化日志
log.info("当前价格: %.2f, MA5: %.2f, MA10: %.2f" % (price, ma5, ma10))

七、策略性能评估指标
回测评价指标
表格指标说明理想值策略收益策略的总收益率越高越好基准收益基准指数的收益率对比参考Alpha比率超额收益正数越好Beta比率市场风险敞口0.5~1.5夏普比率风险调整后收益>1为优秀最大回撤最大亏损幅度越小越好胜率盈利交易占比>50%为佳
实盘监控指标
表格指标说明监控频率持仓盈亏未实现盈亏每日累计盈亏已实现盈亏每日可用资金可交易资金实时持仓比例仓位占比实时

---

### 7. assets/backtest_config.json（回测参数模板）

```json
{
  "策略名称": "小果双均线策略",
  "策略版本": "1.0.0",
  "创建时间": "2026-08-14",
  
  "业务配置": {
    "业务类型": "股票",
    "交易标的": ["600570.SS"],
    "股票池说明": "单只股票：600570.SS（恒生电子）"
  },
  
  "回测参数": {
    "开始时间": "2023-01-01",
    "结束时间": "2023-12-31",
    "初始资金": 1000000,
    "回测基准": "000300.SS",
    "回测频率": "日线",
    "频率说明": "支持：日线、分钟线（1m/5m/15m/30m/60m）"
  },
  
  "交易成本": {
    "佣金费率": 0.0003,
    "最低佣金": 5.0,
    "佣金类型": "STOCK",
    "滑点比例": 0.1,
    "滑点说明": "百分比，0.1表示0.1%",
    "成交比例": 0.25,
    "成交限制模式": "LIMIT"
  },
  
  "策略参数": {
    "短期均线周期": 5,
    "长期均线周期": 10,
    "买入方式": "全仓买入",
    "卖出方式": "全部卖出",
    "参数说明": {
      "ma_short": "5日均线，短期趋势判断",
      "ma_long": "10日均线，中期趋势判断",
      "买入条件": "MA5上穿MA10（金叉）",
      "卖出条件": "MA5下穿MA10（死叉）"
    }
  },
  
  "风险控制": {
    "止损比例": 0.05,
    "止盈比例": 0.10,
    "最大持仓比例": 0.50,
    "单只股票最大仓位": 0.30,
    "说明": "止损5%，止盈10%，单只股票不超过总资产30%"
  },
  
  "日志配置": {
    "日志级别": "INFO",
    "日志输出": "控制台+文件",
    "日志说明": "支持级别：DEBUG < INFO < WARNING < ERROR < CRITICAL"
  },
  
  "优化建议": {
    "方向1": "增加成交量过滤条件",
    "方向2": "增加趋势过滤（使用200日均线判断大趋势）",
    "方向3": "增加止损止盈逻辑",
    "方向4": "多股票组合降低风险"
  },
  
  "注意事项": [
    "1. 回测只能获取2005年后的数据",
    "2. 股票最小下单100股，可转债最小10张",
    "3. 停牌日成交量为0，复盘后可能跳空",
    "4. 实盘交易注意涨跌停限制",
    "5. 财务数据每秒调用不超过100次"
  ]
}

8. assets/strategy_template.py（策略模板文件 - 可复用框架）
python# -*- coding: utf-8 -*-
"""
=============================================================================
Ptrade 策略模板 - 小果量化交易
=============================================================================
功能：提供可复用的策略基础框架，用户只需修改"用户自定义区域"即可快速创建新策略
适用平台：Ptrade 量化交易终端（回测 + 实盘交易）
创建时间：2026-08-14
=============================================================================

【使用说明】
1. 复制本文件到 Ptrade 策略编辑器
2. 修改"用户自定义区域"的代码
3. 点击"保存"并运行回测或交易

【模板结构】
- 第一部分：用户自定义区域（修改这里）
- 第二部分：策略核心逻辑（不需修改）
- 第三部分：可选扩展函数（按需添加）
- 第四部分：工具函数（按需使用）
=============================================================================
"""

import numpy as np
import pandas as pd

# =============================================================================
# 第一部分：用户自定义区域（请修改以下参数）
# =============================================================================

# 策略参数配置
STRATEGY_CONFIG = {
    # 股票池设置
    'stock_pool': ['600570.SS'],  # 股票代码列表，格式：['600570.SS', '000001.SZ']
    
    # 均线参数
    'ma_short': 5,    # 短期均线周期
    'ma_long': 10,    # 长期均线周期
    
    # 交易参数
    'buy_type': 'full',  # 买入方式：'full'（全仓）, 'fixed'（固定金额）, 'ratio'（比例）
    'buy_value': 10000,  # 固定买入金额（buy_type='fixed'时生效）
    'buy_ratio': 0.2,    # 买入比例（buy_type='ratio'时生效）
    
    # 风险控制
    'stop_loss': 0.05,   # 止损比例（5%）
    'take_profit': 0.10, # 止盈比例（10%）
    
    # 日志配置
    'log_level': 'INFO',  # 日志级别：DEBUG, INFO, WARNING, ERROR
}

# =============================================================================
# 第二部分：策略核心逻辑（不需修改）
# =============================================================================

def initialize(context):
    """
    =============================================================================
    初始化函数（必选）
    =============================================================================
    该函数只在策略启动时运行一次，用于初始化全局变量和参数配置。
    =============================================================================
    """
    # 1. 加载策略配置
    g.config = STRATEGY_CONFIG.copy()
    
    # 2. 设置股票池
    g.security = g.config['stock_pool']
    set_universe(g.security)
    
    # 3. 初始化全局变量
    g.is_bought = False      # 买入标记
    g.trade_count = 0        # 交易次数
    g.buy_price = 0.0        # 买入价格（用于计算止损止盈）
    g.ma_short = g.config['ma_short']  # 短期均线周期
    g.ma_long = g.config['ma_long']    # 长期均线周期
    
    # 4. 日志输出
    log.info("=" * 60)
    log.info("小果量化交易 - 策略启动")
    log.info("股票池: %s" % g.security)
    log.info("均线参数: MA%d / MA%d" % (g.ma_short, g.ma_long))
    log.info("买入方式: %s" % g.config['buy_type'])
    log.info("止损比例: %.1f%%, 止盈比例: %.1f%%" % 
             (g.config['stop_loss'] * 100, g.config['take_profit'] * 100))
    log.info("=" * 60)

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
    # 1. 检查是否应该交易
    if not should_trade(context, data):
        return
    
    # 2. 生成交易信号
    signal = generate_signal(context, data)
    
    # 3. 执行交易
    if signal is not None:
        execute_trade(context, data, signal)

def should_trade(context, data):
    """
    =============================================================================
    检查是否应该交易
    =============================================================================
    返回：True=可以交易，False=跳过本次交易
    =============================================================================
    """
    # 获取当前标的
    security = g.security[0] if isinstance(g.security, list) else g.security
    
    # 检查数据是否有效
    if security not in data:
        log.warning("股票 %s 不在当前数据中" % security)
        return False
    
    # 获取当前价格
    current_price = data[security]['close']
    if current_price is None or current_price <= 0:
        return False
    
    return True

def generate_signal(context, data):
    """
    =============================================================================
    生成交易信号
    =============================================================================
    返回：dict 或 None
        {'type': 'buy'/'sell', 'price': 价格, 'reason': '原因'}
    =============================================================================
    """
    security = g.security[0] if isinstance(g.security, list) else g.security
    
    # 1. 获取历史数据
    df = get_history(
        count=g.ma_long + 5,
        frequency='1d',
        field='close',
        security_list=security,
        fq=None,
        include=False
    )
    
    # 检查数据是否足够
    if df is None or len(df) < g.ma_long:
        log.warning("历史数据不足，当前数据长度: %d" % (0 if df is None else len(df)))
        return None
    
    # 2. 计算均线
    close_prices = df['close'].values
    ma_short = close_prices[-g.ma_short:].mean()
    ma_long = close_prices[-g.ma_long:].mean()
    
    # 3. 获取当前价格和持仓
    current_price = data[security]['close']
    position = get_position(security)
    position_amount = 0 if position is None else position.amount
    cash = context.portfolio.cash
    
    # 4. 买入信号判断
    # 金叉买入：短期均线上穿长期均线
    if ma_short > ma_long and not g.is_bought and cash > 0:
        return {
            'type': 'buy',
            'price': current_price,
            'reason': '金叉买入 - MA%d(%.2f) > MA%d(%.2f)' % 
                     (g.ma_short, ma_short, g.ma_long, ma_long)
        }
    
    # 5. 卖出信号判断
    # 死叉卖出：短期均线下穿长期均线
    if ma_short < ma_long and g.is_bought and position_amount > 0:
        return {
            'type': 'sell',
            'price': current_price,
            'reason': '死叉卖出 - MA%d(%.2f) < MA%d(%.2f)' % 
                     (g.ma_short, ma_short, g.ma_long, ma_long)
        }
    
    # 6. 止损止盈判断
    if g.is_bought and position_amount > 0:
        # 计算盈亏比例
        cost_price = position.cost_basis if position else 0
        if cost_price > 0:
            profit_ratio = (current_price - cost_price) / cost_price
            
            # 止损
            if profit_ratio <= -g.config['stop_loss']:
                return {
                    'type': 'sell',
                    'price': current_price,
                    'reason': '止损卖出 - 亏损%.2f%%' % (profit_ratio * 100)
                }
            
            # 止盈
            if profit_ratio >= g.config['take_profit']:
                return {
                    'type': 'sell',
                    'price': current_price,
                    'reason': '止盈卖出 - 盈利%.2f%%' % (profit_ratio * 100)
                }
    
    return None

def execute_trade(context, data, signal):
    """
    =============================================================================
    执行交易
    =============================================================================
    参数：
        signal: 交易信号 dict
            {'type': 'buy'/'sell', 'price': 价格, 'reason': '原因'}
    =============================================================================
    """
    security = g.security[0] if isinstance(g.security, list) else g.security
    
    if signal['type'] == 'buy':
        # 计算买入金额
        buy_type = g.config['buy_type']
        cash = context.portfolio.cash
        
        if buy_type == 'full':
            buy_value = cash  # 全仓买入
        elif buy_type == 'fixed':
            buy_value = min(g.config['buy_value'], cash)  # 固定金额
        elif buy_type == 'ratio':
            buy_value = cash * g.config['buy_ratio']  # 比例买入
        else:
            buy_value = cash
        
        # 执行买入
        order_id = order_value(security, buy_value)
        g.is_bought = True
        g.trade_count += 1
        g.buy_price = signal['price']
        
        log.info("【买入执行】%s" % signal['reason'])
        log.info("买入价格: %.2f, 买入金额: %.2f" % (signal['price'], buy_value))
        log.info("订单编号: %s" % order_id)
        
    elif signal['type'] == 'sell':
        # 执行卖出（全部卖出）
        position = get_position(security)
        if position and position.amount > 0:
            order_id = order_target(security, 0)
            g.is_bought = False
            g.trade_count += 1
            
            log.info("【卖出执行】%s" % signal['reason'])
            log.info("卖出价格: %.2f, 卖出数量: %d" % (signal['price'], position.amount))
            log.info("订单编号: %s" % order_id)
    
    # 记录变量
    record(stock_price=signal['price'])

# =============================================================================
# 第三部分：可选扩展函数（按需添加）
# =============================================================================

def before_trading_start(context, data):
    """
    =============================================================================
    盘前处理函数（可选）
    =============================================================================
    回测中每个交易日 8:30 执行
    交易中每天 9:10（默认）执行
    =============================================================================
    """
    log.info("盘前准备 - 交易日: %s" % context.blotter.current_dt)

def after_trading_end(context, data):
    """
    =============================================================================
    盘后处理函数（可选）
    =============================================================================
    每天交易结束后执行，默认 15:30
    =============================================================================
    """
    log.info("=" * 60)
    log.info("【盘后总结】")
    log.info("总资产: %.2f" % context.portfolio.portfolio_value)
    log.info("可用资金: %.2f" % context.portfolio.cash)
    log.info("持仓市值: %.2f" % context.portfolio.positions_value)
    log.info("累计收益率: %.2f%%" % (context.portfolio.returns * 100))
    log.info("累计交易次数: %d" % g.trade_count)
    log.info("=" * 60)

# =============================================================================
# 第四部分：工具函数（按需使用）
# =============================================================================

def print_portfolio_summary(context):
    """
    打印账户持仓摘要
    """
    log.info("=" * 40)
    log.info("【账户摘要】")
    log.info("总资产: %.2f" % context.portfolio.portfolio_value)
    log.info("可用资金: %.2f" % context.portfolio.cash)
    log.info("持仓市值: %.2f" % context.portfolio.positions_value)
    log.info("累计收益率: %.2f%%" % (context.portfolio.returns * 100))
    log.info("=" * 40)

def get_stock_status_info(stock_code):
    """
    获取股票状态信息
    """
    try:
        result = {}
        st_status = get_stock_status([stock_code], 'ST')
        halt_status = get_stock_status([stock_code], 'HALT')
        delist_status = get_stock_status([stock_code], 'DELISTING')
        
        result['is_st'] = st_status.get(stock_code, False) if st_status else False
        result['is_halt'] = halt_status.get(stock_code, False) if halt_status else False
        result['is_delisting'] = delist_status.get(stock_code, False) if delist_status else False
        
        return result
    except Exception as e:
        log.error("获取股票状态时出错: %s" % str(e))
        return None