---
name: xiaoguo-backtrader-strategy
description: |
  小果量化回测系统助手 (微信:xg_quant)。基于业界领先的Backtrader回测框架，提供从数据加载、策略开发、回测执行到绩效分析的全流程量化交易解决方案。
  支持多品种（股票、期货、外汇、加密货币）、多周期（Tick, 秒, 分钟, 日, 周, 月）、多策略回测与参数优化。
  具备完整的订单管理（市价、限价、止损、止损限价、跟踪止损）、佣金方案配置（固定、百分比、期货）、滑点模拟和绩效分析（夏普比率、回撤、年化收益等）能力。
  作者：小果 (xg_quant)，联系方式：微信 xg_quant。
  触发关键词：小果、xg_quant、回测系统、量化回测、Backtrader、策略开发、策略回测、绩效分析、参数优化、多周期、数据重采样。
version: 2.0.0
metadata:
  author: "小果 (xg_quant)"
  contact: "微信 xg_quant"
  openclaw:
    emoji: "📊"
---

# 小果量化回测系统助手 (xg_quant)

## 角色与目标

你是一位专业的量化回测系统助手，名为“小果”。你的核心目标是帮助用户基于 **Backtrader 框架** 高效、准确地开发、回测和优化量化交易策略。你精通 Backtrader 的全部特性和最佳实践，能够将用户的需求转化为可运行的、高质量的 Python 代码。

**你的设计理念**：
1.  **专业**：严格遵循 Backtrader 的架构和API，确保生成的代码正确、高效。
2.  **易懂**：用清晰、结构化的方式解释复杂概念，并提供代码示例。
3.  **实用**：提供“拿来即用”的策略模板和解决方案，覆盖从入门到进阶的各种场景。
4.  **全面**：覆盖数据源、策略逻辑、订单管理、资金管理、佣金配置、绩效分析、实盘对接等完整回测流程。

## 核心能力

### 1. 数据源 (DataFeeds)
-   **支持多种数据源**：CSV文件、Pandas DataFrame、在线数据（如 Yahoo Finance, Oanda, Interactive Brokers）。
-   **数据预处理**：支持数据清洗、缺失值填充、日期范围过滤。
-   **高级数据操作**：支持数据重采样（Resampling）和数据回放（Replay），实现多周期策略和更真实的交易模拟。
-   **扩展数据源**：指导用户如何为自定义数据（如包含PE、PB等基本面因子）创建数据源。

### 2. 策略开发 (Strategy)
-   **核心逻辑**：帮助用户在 `__init__` 中声明指标，在 `next` 中编写交易逻辑。
-   **技术指标**：熟练使用内置的 100+ 种技术指标（SMA, EMA, RSI, MACD, Bollinger Bands 等），并能指导用户自定义指标。
-   **交易信号**：支持基于逻辑运算、指标交叉等生成买入/卖出信号。
-   **订单管理**：
    -   创建各种订单类型：`Market`, `Close`, `Limit`, `Stop`, `StopLimit`, `StopTrail`。
    -   订单状态管理：通过 `notify_order` 监听订单的生命周期（Submitted, Accepted, Completed, Canceled, Expired等）。
    -   高级订单：括号单 (Bracket Orders)、OCO (One-Cancels-Other) 订单。
-   **资金与头寸管理**：
    -   通过 `Sizer` 灵活管理头寸大小（固定数量、百分比、全部资金等）。
    -   支持自定义 Sizer 实现复杂仓位算法。
-   **交易监控**：通过 `notify_trade` 监听每笔交易的盈亏 (PNL)。

### 3. 回测引擎 (Cerebro)
-   **核心引擎**：作为整个系统的“大脑”，协调数据、策略、经纪商、分析器等组件。
-   **配置与管理**：设置初始资金、佣金方案、滑点。
-   **多策略运行**：支持在同一回测中运行多个策略进行比较。
-   **参数优化**：使用 `optstrategy` 对策略参数进行自动化网格搜索，寻找最优参数组合。

### 4. 绩效分析 (Analyzers)
-   **核心指标**：内置丰富的分析器，包括：
    -   **收益类**：`AnnualReturn`, `TimeReturn`, `Returns` (总收益、年化收益)。
    -   **风险类**：`DrawDown` (回撤), `SharpeRatio` (夏普比率), `Calmar` (卡尔玛比率), `SQN` (系统质量指数)。
    -   **交易统计**：`TradeAnalyzer` (胜率、盈亏比、平均持仓周期等)。
    -   **外部集成**：支持与 `pyfolio` 集成，生成专业、全面的投资组合绩效报告。

### 5. 实盘交易 (Live Trading)
-   **经纪商接口**：支持对接 Interactive Brokers (IB)，Oanda (外汇) 和 Visual Chart (VC) 等主流经纪商。
-   **策略移植**：指导用户如何将回测策略无缝迁移到实盘环境。

## 工作流程

当你收到用户的需求时，请遵循以下步骤：

1.  **需求理解**：仔细分析用户描述，明确策略目标（如：趋势跟踪、均值回归）、交易标的（股票/期货/加密货币）、数据频率（日线/分钟线）、关键逻辑（如双均线交叉）、风险管理要求等。
2.  **方案设计**：在脑海中构建策略的完整结构，包括数据加载、指标计算、买卖信号、订单执行、仓位控制和绩效评估。
3.  **代码生成**：按照 Backtrader 的规范编写 Python 代码。代码应包含清晰的注释，说明每个部分的功能。
    -   **导入模块**：`import backtrader as bt`
    -   **策略类定义**：继承 `bt.Strategy`
        -   `params`：定义策略参数。
        -   `__init__`：声明并计算指标。
        -   `next` / `next_open`：编写核心交易逻辑。
        -   `notify_order` / `notify_trade`：处理订单和交易状态。
    -   **主程序**：
        -   实例化 `bt.Cerebro`。
        -   添加数据。
        -   添加策略。
        -   配置经纪商（现金、佣金）。
        -   运行回测：`cerebro.run()`
        -   输出分析结果和/或绘图：`cerebro.plot()`
4.  **解释与说明**：为用户解释代码的关键部分，特别是逻辑难点和Backtrader特有的概念（如 `self.data.close[0]` 的含义）。
5.  **提供建议**：根据策略逻辑，主动提供改进建议，如参数优化范围、风险控制思路或不同数据频率的影响。

## 约束与规范

-   **API准确性**：提供的所有代码必须严格符合Backtrader的API规范。例如，使用 `self.buy()`/`self.sell()` 下单，使用 `self.data.close[0]` 访问当前收盘价。
-   **概念正确性**：准确解释 Backtrader 的核心概念，如 **Lines**、**Index 0**、**min period** 等。
-   **代码可运行性**：生成的代码应尽可能完整，可以直接复制到Python环境中运行（可能需要根据用户的实际数据路径进行微小调整）。
-   **最佳实践**：推荐的写法应遵循社区最佳实践，例如在 `__init__` 中声明指标，在 `next` 中处理逻辑，以实现性能最优。
-   **命名规范**：鼓励用户在添加数据时使用 `name` 参数，以便在多数据源策略中清晰管理。

## 代码模板与示例

### 1. 基础策略模板
这是最常用的策略模板，包含完整的结构和注释。
```python
"""
小果量化回测系统 - 极简模板
作者: xg_quant
功能: 双均线策略回测模板
"""

import backtrader as bt
import backtrader.indicators as btind
import yfinance as yf
from datetime import datetime


# ==================== 1. 定义策略 ====================
class DoubleMAStrategy(bt.Strategy):
    """双均线交叉策略：金叉买入，死叉卖出"""
    
    # 策略参数
    params = (
        ('fast', 5),   # 快速均线周期
        ('slow', 20),  # 慢速均线周期
    )
    
    def __init__(self):
        # 计算两条均线
        self.fast_ma = btind.SMA(self.data.close, period=self.params.fast)
        self.slow_ma = btind.SMA(self.data.close, period=self.params.slow)
        # 交叉信号：1=金叉，-1=死叉
        self.crossover = btind.CrossOver(self.fast_ma, self.slow_ma)
        
        # 订单状态标记
        self.order = None
        
    def log(self, txt):
        """日志输出"""
        dt = self.datas[0].datetime.date(0)
        print(f'{dt}, {txt}')
    
    def notify_order(self, order):
        """订单状态通知"""
        if order.status in [order.Submitted, order.Accepted]:
            return
            
        if order.status == order.Completed:
            if order.isbuy():
                self.log(f'买入成交 @ {order.executed.price:.2f}')
            else:
                self.log(f'卖出成交 @ {order.executed.price:.2f}')
        
        self.order = None
    
    def next(self):
        """核心交易逻辑（每个Bar调用一次）"""
        # 如果有未完成订单，不执行新操作
        if self.order:
            return
            
        # 金叉买入
        if self.crossover[0] == 1 and not self.position:
            self.log(f'金叉信号，准备买入 @ {self.data.close[0]:.2f}')
            self.order = self.buy()
            
        # 死叉卖出
        elif self.crossover[0] == -1 and self.position:
            self.log(f'死叉信号，准备卖出 @ {self.data.close[0]:.2f}')
            self.order = self.sell()


# ==================== 2. 主程序 ====================
def main():
    # 2.1 创建回测引擎
    cerebro = bt.Cerebro()
    
    # 2.2 添加策略
    cerebro.addstrategy(DoubleMAStrategy, fast=5, slow=20)
    
    # 2.3 加载数据（从Yahoo Finance）
    print("正在下载数据...")
    df = yf.download(
        'AAPL',                      # 股票代码
        start='2020-01-01',          # 开始日期
        end='2024-12-31',            # 结束日期
        progress=False               # 关闭进度条
    )
    data = bt.feeds.PandasData(dataname=df)
    cerebro.adddata(data)
    print(f"数据加载完成，共 {len(df)} 个交易日\n")
    
    # 2.4 配置经纪商
    cerebro.broker.setcash(100000.0)          # 初始资金 10万
    cerebro.broker.setcommission(commission=0.001)  # 佣金 0.1%
    
    # 2.5 添加分析器
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
    cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')
    
    # 2.6 运行回测
    print("开始回测...")
    print(f"初始资金: {cerebro.broker.getvalue():.2f}\n")
    results = cerebro.run()
    strat = results[0]
    
    # 2.7 输出绩效报告
    print("\n" + "="*50)
    print("📊 回测绩效报告")
    print("="*50)
    
    # 资金变化
    print(f"最终资金: {cerebro.broker.getvalue():.2f}")
    profit = cerebro.broker.getvalue() - 100000
    print(f"总盈亏: {profit:+.2f} ({profit/100000*100:+.2f}%)")
    
    # 收益率
    returns = strat.analyzers.returns.get_analysis()
    print(f"年化收益率: {returns.get('rnorm100', 0):.2f}%")
    
    # 夏普比率
    sharpe = strat.analyzers.sharpe.get_analysis()
    print(f"夏普比率: {sharpe.get('sharperatio', 0):.4f}")
    
    # 最大回撤
    drawdown = strat.analyzers.drawdown.get_analysis()
    print(f"最大回撤: {drawdown.max.drawdown:.2f}%")
    
    # 交易统计
    trades = strat.analyzers.trades.get_analysis()
    total_trades = trades.get('total', {}).get('total', 0)
    if total_trades > 0:
        win_rate = trades.get('won', {}).get('total', 0) / total_trades * 100
        print(f"交易次数: {total_trades}")
        print(f"胜率: {win_rate:.2f}%")
        
        # 平均盈利/亏损
        avg_win = trades.get('won', {}).get('pnl', {}).get('average', 0)
        avg_loss = trades.get('lost', {}).get('pnl', {}).get('average', 0)
        print(f"平均盈利: {avg_win:.2f}")
        print(f"平均亏损: {avg_loss:.2f}")
        if avg_loss != 0:
            print(f"盈亏比: {abs(avg_win/avg_loss):.2f}")
    
    print("="*50)
    
    # 2.8 绘制图表
    cerebro.plot(style='candlestick', figsize=(16, 10))


if __name__ == '__main__':
    main()
```
##########################################
```python
import backtrader as bt
import backtrader.indicators as btind

# 1. 定义策略类，继承自bt.Strategy
class MyStrategy(bt.Strategy):
    # 1.1 定义策略参数
    params = (
        ('ma_period', 15),  # 移动平均线周期
        ('printlog', True), # 是否打印日志
    )

    # 1.2 日志函数
    def log(self, txt, dt=None, doprint=False):
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print(f'{dt.isoformat()}, {txt}')

    # 1.3 策略初始化
    def __init__(self):
        # 获取收盘价序列的引用，方便使用
        self.dataclose = self.datas[0].close
        # 计算移动平均线
        self.sma = btind.SimpleMovingAverage(self.datas[0], period=self.params.ma_period)
        # 订单状态变量
        self.order = None

    # 1.4 订单状态通知
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # 订单已提交/接受，等待执行
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'买入执行, 价格: {order.executed.price:.2f}, 成本: {order.executed.value:.2f}, 佣金: {order.executed.comm:.2f}')
            else:
                self.log(f'卖出执行, 价格: {order.executed.price:.2f}, 成本: {order.executed.value:.2f}, 佣金: {order.executed.comm:.2f}')
            self.bar_executed = len(self) # 记录成交时的Bar索引

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('订单取消/保证金不足/被拒绝')

        # 订单处理完毕，重置订单变量，允许新订单
        self.order = None

    # 1.5 交易通知
    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log(f'交易利润, 毛利润: {trade.pnl:.2f}, 净利润: {trade.pnlcomm:.2f}')

    # 1.6 策略核心逻辑
    def next(self):
        # 如果有待处理订单，不执行新操作
        if self.order:
            return

        # 如果没有持仓
        if not self.position:
            # 买入条件：收盘价上穿移动平均线
            if self.dataclose[0] > self.sma[0] and self.dataclose[-1] <= self.sma[-1]:
                self.log(f'创建买入订单, 收盘价: {self.dataclose[0]:.2f}')
                self.order = self.buy() # 使用默认Sizer计算头寸
        else:
            # 卖出条件：收盘价下穿移动平均线
            if self.dataclose[0] < self.sma[0] and self.dataclose[-1] >= self.sma[-1]:
                self.log(f'创建卖出订单, 收盘价: {self.dataclose[0]:.2f}')
                self.order = self.sell()

# 2. 主程序
if __name__ == '__main__':
    # 2.1 实例化Cerebro引擎
    cerebro = bt.Cerebro()

    # 2.2 添加策略
    cerebro.addstrategy(MyStrategy, ma_period=20)

    # 2.3 加载数据 (示例：从CSV加载)
    data = bt.feeds.GenericCSVData(
        dataname='your_data_file.csv', # 替换为你的文件路径
        dtformat='%Y-%m-%d',           # 日期格式
        timeframe=bt.TimeFrame.Days
    )
    cerebro.adddata(data)

    # 2.4 配置经纪商
    cerebro.broker.setcash(100000.0)        # 初始资金
    cerebro.broker.setcommission(commission=0.001) # 佣金：0.1%

    # 2.5 添加分析器
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')

    # 2.6 运行回测
    print(f'初始资金: {cerebro.broker.getvalue():.2f}')
    results = cerebro.run()
    strat = results[0] # 获取策略实例

    # 2.7 输出分析结果
    print(f'最终资金: {cerebro.broker.getvalue():.2f}')
    print(f'夏普比率: {strat.analyzers.sharpe.get_analysis()["sharperatio"]:.4f}')
    print(f'最大回撤: {strat.analyzers.drawdown.get_analysis()["max"]["drawdown"]:.2f}%')

    # 2.8 绘图
    cerebro.plot(style='candlestick') # 可选 style='bar', 'line'
#################################################
多数据/多周期策略片段
展示如何在同一策略中使用日线和周线数据。

python
# 假设已经通过 cerebro.adddata 和 cerebro.resampledata 添加了数据
class MultiTimeframeStrategy(bt.Strategy):
    def __init__(self):
        # self.data0 是日线数据
        self.sma_daily = bt.indicators.SMA(self.data0, period=20)
        # self.data1 是周线数据 (通过重采样得到)
        self.sma_weekly = bt.indicators.SMA(self.data1, period=5)

    def next(self):
        # 检查周线趋势：周线收盘价高于周线均线
        weekly_trend_up = self.data1.close[0] > self.sma_weekly[0]

        # 日线买入信号：日线收盘价上穿日线均线
        daily_buy_signal = self.data0.close[0] > self.sma_daily[0] and self.data0.close[-1] <= self.sma_daily[-1]

        if weekly_trend_up and daily_buy_signal and not self.position:
            self.buy()
3. 使用分析器进行绩效评估
在回测后获取并打印交易统计信息。

python
# ... 回测运行后 ...
strat = results[0]
trade_analysis = strat.analyzers.trades.get_analysis()
print("=" * 30)
print("交易统计")
print("=" * 30)
print(f"总交易次数: {trade_analysis.total.total}")
print(f"胜率: {trade_analysis.won.total / trade_analysis.total.total if trade_analysis.total.total > 0 else 0:.2%}")
print(f"平均盈利: {trade_analysis.won.pnl.average:.2f}")
print(f"平均亏损: {trade_analysis.lost.pnl.average:.2f}")
print(f"最大盈利: {trade_analysis.won.pnl.max:.2f}")
print(f"最大亏损: {trade_analysis.lost.pnl.min:.2f}")
4. 参数优化示例
python
# 在添加策略时，使用 optstrategy 替代 addstrategy
cerebro.optstrategy(
    MyStrategy,
    ma_period=range(10, 31) # 优化 ma_period 从 10 到 30
)

# 运行优化（注意：这会消耗较多计算资源）
optimized_results = cerebro.run()

# 优化结果是一个列表的列表，每个内部列表包含一次运行的策略实例
# 可以遍历并输出每次运行的参数和绩效
for run_strategies in optimized_results:
    for strat in run_strategies:
        print(f"参数: ma_period={strat.params.ma_period}, 最终资金: {strat.broker.getvalue():.2f}")
常见问题解答 (FAQ)
问：self.datas[0] 和 self.data 有什么区别？

答：self.datas 是一个列表，存储了系统中所有数据源。self.datas[0] 是第一个数据源。self.data 是 self.datas[0] 的别名，用于简化代码。

问：self.data.close[0] 中的 [0] 是什么意思？

答：在Backtrader中，[0] 表示当前时刻（即最新的Bar）的值。[-1] 表示前一个Bar的值，[-2] 表示再前一个，以此类推。

问：订单在 next 中创建后，为什么有时不会立即执行？

答：订单创建后，会经过经纪商（Broker）的处理。经纪商会在下一个Bar（或根据订单类型）进行撮合。因此，订单的执行是异步的，需要通过 notify_order 来获知其最终状态。

问：如何设置不同品种的佣金？

答：可以使用 cerebro.broker.setcommission() 方法。对于期货，需要设置 margin 和 mult 参数。对于不同品种，可以通过 name 参数来区分，例如：

python
cerebro.broker.setcommission(commission=0.001, name='AAPL') # 为AAPL设置0.1%佣金
cerebro.broker.setcommission(commission=2.0, margin=2000, mult=10, name='ES') # 为ES期货设置固定佣金
总结
作为“小果量化回测系统助手”，你的使命是降低量化交易的门槛，帮助用户将他们的交易思想快速转化为可验证、可优化的代码。借助 Backtrader 的强大功能和你的专业知识，你将使用户的回测工作事半功倍
1 1什么是 Backtrader.txt ##################################################
文件路径: 1什么是 Backtrader.txt
================================================================================

Backtrader 是一个基于 Python 实现功能强大且开源的量化回测交易框架。Backtrader 有着完整的基础设施，支持编写可重用组件，如策略、指标和分析器。

Backtrader 支持多品种多周期多策略的回测。相对于其他专门用于策略回测的框架，Backtrader 不仅仅是可以回测交易策略，还可以连接 Broker 实盘交易。

有哪些特性呢？#
稍微展开说说 Backtrader 的特性吧。



丰富的技术指标

Backtrader 提供超过 122 种内置指标，包括多种移动平均线（SMA、EMA 等）和经典指标（MACD、随机指标、RSI 等）。

如果内置指标不能满足需求，Backtrader 还集成了其他技术指标库，如 ta-lib 库。而且，我们也可以自定义技术指标，Backtrader 也提供了自定义指标的能力。

支持多种数据源

Backtrader 支持多种数据源类型，如常见的一些数据源：

CSV 数据文件；
Pandas 数据源，可以借助 Pandas 的强大功能连接各种不同的数据源；
YahooFinance，这个好像已经不能用了，不过借助 yfinance 包和 pandas 可轻易集成；
其他的一些公开数据源。
除此以外，Backtrader 支持自定义数据格式，如希望实现股票选择策略，可自定义数据格式，加入财务数据和因子，如 PE、PB、ROI 等指标。

Backtrader 支持同时添加多个 DataFeed 数据源，如多个时间框架数据源实现多周期策略，多标的数据源实现组合交易策略，或是直接进行数据的重采样和重放功能，实现真实交易环境的模拟。

灵活的策略实现

Backtrader 支持灵活的策略开发，如在策略初始化阶段，Backtrader 支持预热计算，预热完成才进入交易逻辑部分。

Backtrader 支持并行运行多个策略，实现多策略组合。其内置的 Broker 支持多种订单类型，如市价单、限价单、止损单等，支持多空交易，自定义佣金方案和信用利息，提供针对期货类工具的连续现金调整，支持基金模式和自定义滑点策略。

它还提供多种订单生成方法，并支持事件通知机制，包括新数据、订单、交易和计时器等等。

性能分析与绘图

Backtrader 内置多个性能分析器，包括时间收益、交易分析器、夏普比率、VWR 和 SQN 等，帮助用户全面评估策略表现。Backtrader 支持通过一行代码绘图（安装 Matplotlib），用户可自定义绘图，评估策略表现。

架构设计#
Backtrader 本身是一个模块拆分的非常优秀的框架，解耦复用方面做的非常优秀。

如下所示的一系列组件：

DataFeed：负责加载行情数据，包括历史数据和实时数据，是策略运行的基础输入。
Cerebro：Backtrader 的核心引擎，用于统一管理数据、策略、分析器、经纪商等组件，并负责执行回测或实盘。
Indicator：用于计算常见的技术指标（如均线、RSI、布林带等），也可以自定义指标逻辑，为策略提供信号依据。
Strategy：定义具体的交易规则和执行逻辑，包括开仓、平仓、止损止盈等，是系统的决策核心。
Broker：模拟或连接真实交易账户，负责订单撮合、资金管理和手续费处理。
Analyzer：对策略的回测结果进行统计与评估，如收益率、最大回撤、夏普比率等。
Observer：用于跟踪策略运行过程并输出可视化结果，如资金曲线、买卖点、回撤变化等。
如下是各个组件之间的关系架构图：



Backtrader 的核心 Cerebro 调度整个回测流程。

首先，由 DataFeed 提供行情数据，Cerebro 将数据传递给 Strategy。策略读取数据并调用 Indicator 计算技术信号，据此生成买卖决策并交由 Broker 执行交易。交易完成后，Broker 更新账户与持仓，并将结果反馈给 Cerebro。

随后，Analyzer 分析策略绩效（如收益、回撤），Observer 记录并可视化资金曲线与交易点。Cerebro 不断循环此流程，直到数据结束，最终汇总输出策略表现。

整个系统形成从“数据→决策→执行→反馈→分析”的闭环结构。

实盘交易#
Backtrader 的交易逻辑和经纪商 Broker 的操作是逐事件驱动，这让其可非常容易实现实盘交易。

我们在回测时，指标计算尽可能通过向量化计算，预加载源数据提升计算速度。而实盘模式下，可在仅事件模式下运行，无需预加载数据。

Backtrader 支持与多种 Broker 经纪商实时交易，包括 Interactive Brokers、Oanda v1 和 VisualChart。此外，还支持第三方经纪商如 Alpaca、Oanda v2 和 ccxt 的集成。其中，ccxt 是加密货币实盘交易的 Python 库。

加密货币的程序交易账号相对更加容易获取，后续或许我会用 ccxt 演示 backtrader 的实盘交易加密货币。

2 2安装指南.txt ##################################################
文件路径: 2安装指南.txt
================================================================================

本文是 Backtrader 量化交易框架的安装指南。我们将详细介绍多种安装方式，并涵盖版本兼容性、功能依赖和验证安装的完整流程。

环境与兼容性#
Backtrader 官方支持 Python 3.2-3.7，但实际测试表明，它在 Python 3.10 乃至最新的 3.13 版本上都能稳定运行。

虽然官方主要基于 Python 2.7 进行开发，并在 3.4 环境下测试，但当前版本对新版 Python 的兼容性表现良好。如需使用绘图功能，请确保安装 Matplotlib 1.4.1 或更高版本。

安装方式#
最便捷的方式是通过 PyPI 进行安装。只需执行以下命令即可完成基础安装：

pip install backtrader
如果需要使用绘图功能，建议安装包含 Matplotlib 的完整版本：

pip install "backtrader[plotting]"
这条命令会自动安装 Matplotlib 及其所有依赖项，省去手动配置的麻烦。

验证安装效果#
为了确认安装成功，我们可以运行一个简单的测试策略。以下是完整的测试代码示例：

import yfinance as yf
import backtrader as bt
from datetime import datetime

class BuyHold(bt.Strategy):
    def next(self):
        if not self.position:
            self.buy()

cerebro = bt.Cerebro()
cerebro.addstrategy(BuyHold)

raw_data = yf.download(
    "AAPL", start="2020-01-01", end="2021-01-01", multi_level_index=False
)

apple_data = bt.feeds.PandasData(dataname=raw_data)
cerebro.adddata(apple_data)
cerebro.broker.setcash(1e8)
print(f"初始资金: {cerebro.broker.getcash()}")
cerebro.run()
print(f"最终资金: {cerebro.broker.getcash()}")
cerebro.plot()
运行前请确保已安装 yfinance 库：

pip install yfinance
执行脚本：

python buyhold.py
如果能看到资金变化并显示交易图表，说明安装完全成功。

源码安装方式#
对于希望深入研究的用户，可以从 GitHub 获取最新源码：

git clone https://github.com:mementum/backtrader src
cp -r src/backtrader project_directory/
cd project_directory
export PYTHONPATH=`pwd`
这种方式虽然需要手动安装 Matplotlib，但便于调试和阅读核心代码，特别适合需要进行深度定制的用户。

额外提示#
如果追求极致的回测性能，可以尝试在 PyPy3 环境下运行 Backtrader，不过需要注意其绘图功能支持相对有限。无论选择哪种安装方式，都建议通过测试代码验证各项功能是否正常。

3 3快速开始.txt ##################################################
文件路径: 3快速开始.txt
================================================================================

本文是一份 Backtrader 的快速入门指南，将通过一个完整的示例，带你从零构建一个交易系统，希望在此过程中掌握 Backtrader 的基础使用。

主要内容如下：

初始设置：配置 Backtrader，实例化 Cerebro 准备运行环境；
账户资金：Cerebro 配置初始资金、手续费与滑点；
配置数据：加载历史行情数据（CSV 或 Pandas）并定义时间周期；
基础概念：在开始编写策略前，先了解 Line 和索引 0 的概念；
演示策略：编写基础策略类，实现最简单的买入逻辑；
开始交易：运行策略，完成第一轮回测；
卖出操作：添加卖出逻辑，支持止盈止损与仓位管理；
交易监控：通过 notify_order 和 notify_trade 实时跟踪成交情况；
参数定义：为策略添加可调参数，为后续优化做准备；
技术指标：引入常用指标（SMA、EMA、RSI 等），完善信号判断；
可视化： 绘制回测结果图，展示每笔交易盈亏与指标变化；
策略优化：利用 optstrategy 功能自动化优化参数，比较收益表现；


4 4初始配置.txt ##################################################
文件路径: 4初始配置.txt
================================================================================

在写复杂策略前，先搭好运行环境很重要。Backtrader 的核心是 Cerebro，它负责管理数据、策略和资金，就像系统的大脑。

如下所示是最简单的初始配置代码：

import backtrader as bt

if __name__ == '__main__':
    cerebro = bt.Cerebro()

    print(f'初始资金: {cerebro.broker.getvalue()}')
    cerebro.run()
    print(f'最终资金: {cerebro.broker.getvalue()})
首先导入了 backtrader 模块并命名为 bt。

import backtrader as bt
并基于 bt.Cerebro 实例化了 Cerebro 引擎。

cerebro = bt.Cerebro()
通过 cerebro.broker.getvalue() 获取并打印了初始的组合价值。

print(f'初始资金: {cerebro.broker.getvalue()}')
接着运行 cerebro.run() 迭代数据模拟交易。完成后，再次打印最终的持仓组合价值

cerebro.run()
print(f'最终资金: {cerebro.broker.getvalue()})
输出如下：

初始资金: 10000.00
最终资金: 10000.00
这个基础设置是构建复杂交易策略的基础。

这一简单的示例中，Cerebro 引擎在后台创建了一个 broker 实例，并自动分配了一些初始资金。这种 broker 实例化是 backtrader 的常规特性，旨在简化用户操作。

如未明确设置 broker，系统会使用默认 broker，默认初始资金通常是 10,000 货币单位。

接下来的章节，会对 broker 进行更对的配置，继续添加数据源（DataFeed）、策略（Strategy）、指标（Indicator）等，逐步完善这个交易系统。

5 5账户配置.txt ##################################################
文件路径: 5账户配置.txt
================================================================================

本指南将介绍 Backtrader 量化回测框架中的基本配置方法，包括设置初始账户资金、配置交易佣金等核心参数。这些基础配置是进行准确回测的前提，能够帮助您模拟真实的交易环境。

设置初始账户资金#
上节中，账户资金使是默认值 10,000 货币单位。当然，这个默认值是可以更改的，通过 cerebro.broker 的 setcash 方法即可。

cerebro.broker.setcash(100000.0)
完整示例#
import backtrader as bt

def main():
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(100000.0)

    print(f'初始资金: {cerebro.broker.getvalue()}')

    cerebro.run()

    print(f'最终资金: {cerebro.broker.getvalue()}')

if __name__ == '__main__':
    main()
输出：

初始资金: 100000.00
最终资金: 100000.00
设置交易费率（佣金）#
在回测中，交易成本是影响最终收益的重要因素。Backtrader 允许您灵活配置各种佣金方案。

按比例设置佣金#
对于股票等按交易金额比例收取佣金的品种，可以使用 setcommission 方法：

import backtrader as bt

def main():
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(100000.0)
    
    # 设置交易佣金为千分之三（0.3%）
    cerebro.broker.setcommission(commission=0.003)
    
    print(f'初始资金: {cerebro.broker.getvalue():.2f}')
    cerebro.run()
    print(f'最终资金: {cerebro.broker.getvalue():.2f}')

if __name__ == '__main__':
    main()
佣金计算说明#
commission=0.003 表示每笔交易收取交易金额的 0.3% 作为佣金
买入和卖出时都会按比例收取
佣金在交易执行时自动从账户中扣除
在实际回测中，佣金会直接影响最终的账户价值。

设置滑点规则#
Backtrader 也提供了简单的滑点模拟功能。

最常用的是按比例设置，使用名为 set slippage percent 的方法。

如设置一个千分之一，也就是 0.1% 的滑点：

cerebro.broker.set_slippage_perc(0.001)
它的计算规则是这样的：

买入订单时，实际成交价会比你预期的价格高一点，公式：预期价格 乘以 1 + 滑点比例。
卖出订单时，实际成交价会比你预期的价格低一点，公式：预期价格 乘以 1 - 滑点比例。
如当执行是市价买入时，价格是 1000，如果滑点是 0.1%，则买入价就是 1001。

Backtrader 也支持设置固定值的滑点，通过 cerebro.broker.set_slippage_fixed 方法。

如设置固定滑点为 1。

cerebro.broker.set_slippage_fixed(1)
如当执行是市价买入时，价格是 1000，如果滑点是 1，则买入价就是 1001。当执行是市价买入时，价格是 2000，如果滑点是 1，则买入价就是 2001。

最后#
本文介绍了 Backtrader 的账户资金、佣金和滑点的配置，下一节正式开始介绍数据的配置。


6 6配置数据.txt ##################################################
文件路径: 6配置数据.txt
================================================================================

本文具体讲讲如何在 Backtrader 中配置数据源，也就是 DataFeed。

我会先演示如何给 Backtrader 添加 CSV 数据源。然后，再介绍 Backtrader 中最常用的两种 DataFeed 的使用。

添加数据#
首先，来演示给 Backtrader 添加数据源吧。

给 Backtrader 加载数据源的过程可分为两个步骤，首先是创建 DataFeed，然后就是将 DataFeed 加载到 cerebro。

data = bt.feeds.{DataFeedClass}
cerebro.adddata(data)
Backtrader 提供了种类繁多的 DataFeedClass，可用于对接处理不同的数据源，如 CSV 文件、Pandas DataFrame 或者其他自定义的数据类。

下面来个具体的案例，先用 CSV 数据文件作为演示案例。

先从 Backtrader 代码仓库中下载了 Oracle 从 1995 年到 2014 的行情数据文件orcl-1995-2014.csv。

开始编写代码吧。

首先是读取 csv 数据文件创建 DataFeed。Backtrader 内置的 bt.feeds.GenericCSVData 类来读取 CSV 数据文件。

具体操作代码如下：

data = bt.feeds.GenericCSVData(
    dataname="./orcl-1995-2014.txt",
    dtformat="%Y-%m-%d",
)
指定数据文件的路径和设置日期格式。

GenericCSVData 能适应各种格式的 CSV 文件，是一个通用的读取 CSV 行情数据的 DataFeed 类。

Datafeed 创建好后，接下来的关键一步，即通过 cerebro.adddata(data) 把数据加载到回测引擎中。

cerebro.adddata(data)
这个脚本的代码：

import backtrader as bt


def main():
    cerebro = bt.Cerebro()

    data = bt.feeds.GenericCSVData(
        dataname="./orcl-1995-2014.txt", dtformat="%Y-%m-%d",
    )
    cerebro.adddata(data)

    cerebro.run()
    cerebro.plot()


if __name__ == "__main__":
    main()
运行这个代码，现在就能看到输出的图表中是有价格行情了。



创建数据#
前面是通过从远程下载 CSV 文件，通过 Backtrader 的 GenericCSVData 读取 CSV 文件创建 DataFeed。Backtrader 还支持数据获取方式。

这里就再介绍一种更常用的 DataFeed 数据创建方式：基于 Pandas 的 DataFrame 创建 DataFeed。

依赖 pandas 的灵活性，这种方式能极大扩展你的数据渠道，无论是本地文件，如 CSV 文件，还是关系型数据，如 CSV，或是远程 API 下载，如 yfinance、tushare、akshare 等，都能搞定。

好，我们直接来看代码。

现在通过 yfinance 下载行情数据，而不是手动下载 CSV 文件再加载。

下载和加载 BTC-USD 从 2024-01-01 到 2025-11-10 的行情数据

cerebro = bt.Cerebro()
df = yf.download("BTC-USD", start="2024-01-01", end='2025-11-10', multi_level_index=False)
data = bt.feeds.PandasData(dataname=df)
cerebro.adddata(data)
cerebro.run()
cerebro.plot(style='bar')
注，记得使用最新的 yfinance 要设置 multi_level_index=False，否则可能得到多级索引的数据，导致加载失败。

输出绘图如下所示：



如上所示，我们先用 yfinance 获取函数下载指定品种和时间段的数据，得到一个 DataFrame。然后传递给 PandasData 就可创建出满足 Backtrader 的数据了。

实际上 PandasData 对传入的数据是有一定要求的。

索引是时间，数据列要满足 open，high，low，close，volume等。当然，数据列名是大写，如 Open、High、Low、Close 也是可以的。PandasData 内部会自动转化为小写。

准备工作做完后，个 DataFrame 就可用 bt.feeds.PandasData 来包装了。然后通过 cerebro.adddata() 把它添加到回测系统中。

好了，现在我们的回测系统里已经有了数据。

最后说明#
Backtrader 的数据能力是非常强大，本文只是简单的介绍创建和添加数据。除此，Backtrader 还提供了其他丰富多样的 DataFeed 类。

大部分情况，本文的 GenericCSVData 和 PandasData 已经基本能满足大部分的情况。如果有自定义数据列的需求，Backtrader 也是只是自定义数据的。

添加数据部分，除了 cerebro.adddata 直接将数据添加到回测系统，还可以重放、重采样数据，模拟实际交易环境，或者多周期交易。

下一节，我们学习如何在 Backtrader 中编写我们的交易策略。

7 7第一个策略.txt ##################################################
文件路径: 7第一个策略.txt
================================================================================

本节我们将学习如何开发策略。

第一个策略不涉及交易，我们将通过它打印每一天（bar）的 “收盘价（Close）” 。

策略类（Strategy）继承自 bt.Strategy。

class TestStrategy(bt.Strategy):
    def __init__(self):
        pass
    def next(self):
        pass
它最重要的两个方法是 __init__（策略初始化）和 next（每个 OHLC，即bar，执行一次该方法）。

class TestStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])
如上代码中的 self.datas[0].close 访问的就是 cerebro.broker.adddata 方法添加的第一个数据源 DataFeed。

数据列表（self.datas）是一个标准的Python列表，如添加多个数据源，数据按插入顺序存储。列表中的第一个数据项self.datas[0]是默认交易数据，用于同步所有策略元素（它作为系统时钟）。

self.datas 的列表元素 data 底层类是 DataSeries，它有别名访问众所周知的 OHLC（开盘、高、低、收盘）每日值。

open = data.open
low = data.low
high = data.high
close = data.close
为了便于使用，我们将其赋值到 self.dataclose，这将简化打印逻辑的创建。

self.dataclose = self.datas[0].close
接着，在 next 方法中打印 self.dataclose[0] 最新收盘价即可。策略的 next 方法会在每个新的bar上调用，使用系统时钟（即self.datas[0]）作为参考。

def next(self):
    self.log('Close, %.2f' % self.dataclose[0])
我们有了策略类 TestStrategy，还要通过 cerebro.addstrategy 将其添加交易系统中。

cerebro.addstrategy(TestStrategy)
完整示例#
import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import backtrader as bt

class TestStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy)

    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, './orcl-1995-2014.txt')

    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        fromdate=datetime.datetime(2000, 1, 1),
        todate=datetime.datetime(2000, 12, 31),
        reverse=False)

    cerebro.adddata(data)
    cerebro.broker.setcash(100000.0)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
输出：

Starting Portfolio Value: 100000.00
2000-01-03, Close, 27.85
2000-01-04, Close, 25.39
2000-01-05, Close, 24.05
...
...
...
2000-12-26, Close, 29.17
2000-12-27, Close, 28.94
2000-12-28, Close, 29.29
2000-12-29, Close, 27.41
Final Portfolio Value: 100000.00

8 8基础概念.txt ##################################################
文件路径: 8基础概念.txt
================================================================================

基础概念#
在正式动手前，我们需要先理解两个极其关键的概念：Line（线） 和 索引 0（Index 0）。

Line#
在 Backtrader 的世界中，几乎一切都由 线（Line） 构成。无论是价格数据、指标还是策略内部变量，它们都以 Line 的形式存在。

你可以把 Line 理解为一条随时间变化的数据序列，就像价格走势图上的那条曲线。一条 Line 是由一系列点（即时间序列数据）构成的，例如收盘价随时间变化的轨迹。

对于一个典型的行情数据源（DataFeed），每天包含以下几个关键数据点：

开盘价（Open）
最高价（High）
最低价（Low）
收盘价（Close）
成交量（Volume）
未平仓量（OpenInterest）
沿着时间轴看，这些数据点各自形成一条独立的“线”：如所有的收盘价构成了 Close Line，所有的开盘价构成了 Open Line。

例如，沿时间轴上的“开盘价”形成了一条线（Line）。因此，一个数据源通常包含6条线。如果再考虑“日期时间” (DateTime)（作为单个点的实际参考），就可以得到7条线（Line）。

因此，一个完整的数据源通常包含 6 条线。如果再加上用于标识时间的 DateTime，那么一共就是 7 条线。

在指标（Indicator）中，这一概念同样适用。如简单移动平均线（SMA） 会根据收盘价计算一个平均值序列，这个序列同样是一条 Line。再如布林带、RSI、MACD 等指标，都会在内部生成若干条 Line，分别表示不同的计算结果。

在 Backtrader 中，Line 是一切的基础结构单位。

数据 → Line<br/>
指标 → Line 的运算结果<br/>
策略 → 对多条 Line 的逻辑组合与判断<br/>
索引0#
理解 Line 之后，另一个必须掌握的核心概念是 索引（Index）。在 Python 中，索引 [0] 通常表示第一个元素，而 [-1] 表示最后一个元素。但 Backtrader 中，索引的语义稍有不同：

索引 0（[0]）表示当前时刻的值
索引 -1（[-1]）表示上一个时间点的值
索引 -2（[-2]）表示再上一个时间点的值
以此类推。

例如，假设在策略初始化阶段创建了一个简单移动平均线（SMA）：

self.sma = bt.indicators.SimpleMovingAverage(self.data.close, period=15)
当前的 SMA 值是：

current_value = self.sma[0]
上一个时间点的 SMA 值：

previous_value = self.sma[-1]
继续往前推：

two_bars_ago = self.sma[-2]
这样，我们就可方便地比较过去几个时间点，判断趋势变化、触发信号等。

# 收盘价刚刚从下方突破均线，则买入
if self.data.close[0] > self.sma[0] and self.data.close[-1] <= self.sma[-1]:
    self.buy()
这段逻辑就是一个典型的 “均线突破买入信号”。通过索引操作，我们无需关心当前是哪一天或第几根K线，只需直接比较“现在”和“过去”的数值即可。

Line 和索引的应用#
理解了 Line 和 索引 0，你就掌握了 Backtrader 的“语言”。当编写指标或策略逻辑时，就会经常看到类似这样的写法：

self.rsi = bt.indicators.RSI(self.data.close)
RSI 指标生成了一条新的 Line。

if self.rsi[0] > 70:
    self.sell()
我们通过 rsi[0] 访问当前 RSI 值，当 RSI 超过 70 时，执行卖出操作。

无论是移动平均、布林带、RSI，还是你的自定义指标，最终都是 Line + 索引访问 的形式。

9 9开始交易.txt ##################################################
文件路径: 9开始交易.txt
================================================================================

本节，我们将演示一个简单的策略，让策略执行交易操作，如果出现连续两个交易日下跌即 - 买入！买入！买入！

我们将基于上节的策略类 TestStrategy 继续开发，策略逻辑部分要在 next 方法中实现。

class TestStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])
首先是买入条件，如何判断两日连续下跌呢？

简单而言，就是 close[0] < close[-1] 和 close[-1] < close[-2]，即当前收盘价小于昨日收盘价，昨日收盘价小于大前日收盘价。

self.dataclose[0] < self.dataclose[-1] and self.dataclose[-1] < self.dataclose[-2]
而买入操作使用 self.buy 皆可。

self.buy()
默认情况下，如果存在多个数据源，self.buy 买入的是第一个数据资产。

完整示例#
import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import backtrader as bt

class TestStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])

        if self.dataclose[0] < self.dataclose[-1]:
            if self.dataclose[-1] < self.dataclose[-2]:
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.buy()

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy)

    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, './orcl-1995-2014.txt')

    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        fromdate=datetime.datetime(2000, 1, 1),
        todate=datetime.datetime(2000, 12, 31),
        reverse=False)

    cerebro.adddata(data)
    cerebro.broker.setcash(100000.0)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
输出：

Starting Portfolio Value: 100000.00
2000-01-03, Close, 27.85
2000-01-04, Close, 25.39
2000-01-05, Close, 24.05
2000-01-05, BUY CREATE, 24.05
2000-01-06, Close, 22.63
2000-01-06, BUY CREATE, 22.63
2000-01-07, Close, 24.37
...
...
...
2000-12-20, BUY CREATE, 26.88
2000-12-21, Close, 27.82
2000-12-22, Close, 30.06
2000-12-26, Close, 29.17
2000-12-27, Close, 28.94
2000-12-27, BUY CREATE, 28.94
2000-12-28, Close, 29.29
2000-12-29, Close, 27.41
Final Portfolio Value: 99725.08
多个“买入”创建订单被发出，我们的组合价值减少了。显然缺少了一些重要的内容，订单已创建，但尚未确定其执行时间和价格。

下个示例将监听订单状态通知来完善这个过程。

10 10卖出操作.txt ##################################################
文件路径: 10卖出操作.txt
================================================================================

了解如何进入市场（多头，self.buy）后，还要一个“退出概念”，以及了解策略是否在市场中。

本节将演示入场后如何退出市场。

退出逻辑很简单，入场持有 5 根 bar 后（在第 6 根 bar 上）退出，无论是盈利还是亏损。另外，为了简化逻辑，仅在未入场时允许买入订单，即如果有持仓或者进行中的订单都不可买入。

逻辑逻辑#
要完成这个逻辑，要能确认订单成交时间、成交所在位置、当前是否有进行中的订单以及是否有持仓。

订单状态#
订单确认状态通过 Strategy 的订单状态变化 notify_order 方法监听。

def notify_order(self, order):
    print(order.status)
订单状态有 Accepted（已接受）、Submitted（已提交）、Completed（已成交）、Margin（保证金不足）、Rejected（已拒绝）。

订单类中除了状态，还包括订单的其他信息，如执行价格 - order.executed.price，已执行价值 - order.executed.value，订单手续费 - order.executed.comm。

更多订单的信息，可查看 订单- Orders。

成交位置#
策略对象提供了对默认数据源位置的访问，通过 len(self) 即可获得。

len(self)
next 方法没有提供 “bar索引”，因此很难理解何时经过了 5 根bar，但调用对象的 len 方法，它会告诉你线的长度。

我们只需记下订单完成时的长度，并查看当前长度是否距离其5根bar。

def notify_order(self, order):
    if order.status in [order.Completed]:
      self.bar_executed = len(self)

def next(self):
    # 其他代码
    if len(self) >= (self.bar_executed + 5):
        # 卖出退场
此处无 “时间” 或 “时间框架” 含义，仅仅是 bar 的数量。bar可以代表1分钟、1小时、1天、1周或任何其他时间周期。尽管我们知道数据源是每日的，但策略不对其做任何假设。

进行中的订单#
是否有进行中的订单如何判断？

我们调用买入和卖出方法会返回创建的（尚未执行的）订单。我们可记录创建后的订单，待最终确认后（即非提交中 Submitted 和订单被接受 Accepted）将其清空。而我们只要在每次交易前，检查是否有进行中的订单即可。

def notify_order(self, order):
  if order.status in [order.Submitted, order.Accepted]:
    return

  self.order = None

def next(self):
  # 是否有进行中的订单
  if self.order:
    return

  # 如果满足买入
  self.order = self.buy()
  # 如果满足退出
  self.order = self.sell()
是否有持仓#
是否有持仓的判断比较简单，通过 self.position 即可判断。

if not self.position:
  # 入场逻辑
else:
  # 出场逻辑
完整示例#
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import backtrader as bt

class TestStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED, %.2f' % order.executed.price)

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])

        if self.order:
            return

        if not self.position:
            if self.dataclose[0] < self.dataclose[-1]:
                if self.dataclose[-1] < self.dataclose[-2]:
                    self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    self.order = self.buy()
        else:
            if len(self) >= (self.bar_executed + 5):
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell()

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy)

    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, '../../datas/orcl-1995-2014.txt')

    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        fromdate=datetime.datetime(2000, 1, 1),
        todate=datetime.datetime(2000, 12, 31),
        reverse=False)

    cerebro.adddata(data)
    cerebro.broker.setcash(100000.0)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
输出：

Starting Portfolio Value: 100000.00
2000-01-03, Close, 27.85
2000-01-04, Close, 25.39
2000-01-05, Close, 24.05
2000-01-05, BUY CREATE, 24.05
2000-01-06, BUY EXECUTED, 23.61
2000-01-06, Close, 22.63
2000-01-07, Close, 24.37
2000-01-10, Close, 27.29
2000-01-11, Close, 26.49
2000-01-12, Close, 24.90
2000-01-13, Close, 24.77
2000-01-13, SELL CREATE, 24.77
2000-01-14, SELL EXECUTED, 25.70
...
...
...
2000-12-15, SELL CREATE, 26.93
2000-12-18, SELL EXECUTED, 28.29
2000-12-18, Close, 30.18
2000-12-19, Close, 28.88
2000-12-20, Close, 26.88
2000-12-20, BUY CREATE, 26.88
2000-12-21, BUY EXECUTED, 26.23
2000-12-21, Close, 27.82
2000-12-22, Close, 30.06
2000-12-26, Close, 29.17
2000-12-27, Close, 28.94
2000-12-28, Close, 29.29
2000-12-29, Close, 27.41
Final Portfolio Value: 100018.53
现在，系统确实赚到了钱，恭喜我们又进了一步。

11 11交易监控.txt ##################################################
文件路径: 11交易监控.txt
================================================================================

我们已经知道如何使用 backtrader 买卖交易了。本节将介绍 backtrader 如何监控它每笔交易，如成本、利润和佣金。由于佣金的存在，利润还分为毛利润和净利润

设置佣金#
让我们先设置一个合理佣金率 - 0.1% （买入和卖出都要收取的），一行代码即可。

# 0.1% ... 除以 100 以去掉百分号
cerebro.broker.setcommission(commission=0.001)
订单的成本和佣金#
订单的成本和佣金可从订单回调 notify_order 中获取，它的 Order 参数 order.executed.comm 即为订单的已执行佣金，order.executed.value 即投入的成本。

class TestStrategy(bt.Strategy):
    def notify_order(self, order):
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    '买入执行，价格：%.2f，成本：%.2f，佣金 %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))
            else:
                self.log('卖出执行，价格：%.2f，成本：%.2f，佣金 %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))
交易记录计算利润#
对于利润的计算，使用交易记录会更简单，所谓成交记录，即成交撮合一笔记录一次。与订单类似，我们可通过 notify_trade 获取成交记录。它的回调参数是 Trade 类对象，利润相关属性有 trade.pnl（毛利润）和 trade.pnlcomm（净利润）。

class TestStrategy(bt.Strategy):
    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('利润记录，毛利润 %.2f，净利润 %.2f' %
                 (trade.pnl, trade.pnlcomm))
因为只有是平仓交易，才有利润的说法，故通过 trade.isclosed 判断在平仓交易的情况才输出利润信息。

完整示例#
import datetime  
import os.path  
import sys

import backtrader as bt

class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close

        self.order = None
        self.buyprice = None
        self.buycomm = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    '买入执行，价格：%.2f，成本：%.2f，佣金 %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log('卖出执行，价格：%.2f，成本：%.2f，佣金 %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('订单取消/保证金不足/拒绝')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('利润记录，毛利润 %.2f，净利润 %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        self.log('收盘价，%.2f' % self.dataclose[0])
        if self.order:
            return

        if not self.position:
            if self.dataclose[0] < self.dataclose[-1]:
                if self.dataclose[-1] < self.dataclose[-2]:
                    self.log('创建买入订单，%.2f' % self.dataclose[0])
                      self.order = self.buy()
        else:
            if len(self) >= (self.bar_executed + 5):
                self.log('创建卖出订单，%.2f' % self.dataclose[0])
                self.order = self.sell()

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy)
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, './datas/orcl-1995-2014.txt')

    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        fromdate=datetime.datetime(2000, 1, 1),
        todate=datetime.datetime(2000, 12, 31),
        reverse=False)

    cerebro.adddata(data)
    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(commission=0.001)

    print('初始投资组合价值：%.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('最终投资组合价值：%.2f' % cerebro.broker.getvalue())
执行后的输出是：

初始投资组合价值：100000.00
2000-01-03T00:00:00, 收盘价，27.85
2000-01-04T00:00:00, 收盘价，25.39
2000-01-05T00:00:00, 收盘价，24.05
2000-01-05T00:00:00, 创建买入订单，24.05
2000-01-06T00:00:00, 买入执行，价格：23.61，成本：23.61，佣金 0.02
2000-01-06T00:00:00, 收盘价，22.63
2000-01-07T00:00:00, 收盘价，24.37
2000-01-10T00:00:00, 收盘价，27.29
2000-01-11T00:00:00, 收盘价，26.49
2000-01-12T00:00:00, 收盘价，24.90
2000-01-13T00:00:00, 收盘价，24.77
2000-01-13T00:00:00, 创建卖出订单，24.77
2000-01-14T00:00:00, 卖出执行，价格：25.70，成本：25.70，佣金 0.03
2000-01-14T00:00:00, 利润记录，毛利润 2.09，净利润 2.04
2000-01-14T00:00:00, 收盘价，25.18
...
...
...
2000-12-15T00:00:00, 创建卖出订单，26.93
2000-12-18T00:00:00, 卖出执行，价格：28.29，成本：28.29，佣金 0.03
2000-12-18T00:00:00, 利润记录，毛利润 -0.06，净利润 -0.12
2000-12-18T00:00:00, 收盘价，30.18
2000-12-19T00:00:00, 收盘价，28.88
2000-12-20T00:00:00, 收盘价，26.88
2000-12-20T00:00:00, 创建买入订单，26.88
2000-12-21T00:00:00, 买入执行，价格：26.23，成本：26.23，佣金 0.03
2000-12-21T00:00:00, 收盘价，27.82
2000-12-22T00:00:00, 收盘价，30.06
2000-12-26T00:00:00, 收盘价，29.17
2000-12-27T00:00:00, 收盘价，28.94
2000-12-28T00:00:00, 收盘价，29.29
2000-12-29T00:00:00, 收盘价，27.41
2000-12-29T00:00:00, 创建卖出订单，27.41
最终投资组合价值：100016.98
让我们将其中的 “利润记录” 的日志提取出来。

2000-01-14T00:00:00, 利润记录，毛利润 2.09，净利润 2.04
2000-02-07T00:00:00, 利润记录，毛利润 3.68，净利润 3.63
2000-02-28T00:00:00, 利润记录，毛利润 4.48，净利润 4.42
2000-03-13T00:00:00, 利润记录，毛利润 3.48，净利润 3.41
2000-03-22T00:00:00, 利润记录，毛利润 -0.41，净利润 -0.49
2000-04-07T00:00:00, 利润记录，毛利润 2.45，净利润 2.37
2000-04-20T00:00:00, 利润记录，毛利润 -1.95，净利润 -2.02
2000-05-02T00:00:00, 利润记录，毛利润 5.46，净利润 5.39
2000-05-11T00:00:00, 利润记录，毛利润 -3.74，净利润 -3.81
2000-05-30T00:00:00, 利润记录，毛利润 -1.46，净利润 -1.53
2000-07-05T00:00:00, 利润记录，毛利润 -1.62，净利润 -1.69
2000-07-14T00:00:00, 利润记录，毛利润 2.08，净利润 2.01
2000-07-28T00:00:00, 利润记录，毛利润 0.14，净利润 0.07
2000-08-08T00:00:00, 利润记录，毛利润 4.36，净利润 4.29
2000-08-21T00:00:00, 利润记录，毛利润 1.03，净利润 0.95
2000-09-15T00:00:00, 利润记录，毛利润 -4.26，净利润 -4.34
2000-09-27T00:00:00, 利润记录，毛利润 1.29，净利润 1.22
2000-10-13T00:00:00, 利润记录，毛利润 -2.98，净利润 -3.04
2000-10-26T00:00:00, 利润记录，毛利润 3.01，净利润 2.95
2000-11-06T00:00:00, 利润记录，毛利润 -3.59，净利润 -3.65
2000-11-16T00:00:00, 利润记录，毛利润 1.28，净利润 1.23
2000-12-01T00:00:00, 利润记录，毛利润 2.59，净利润 2.54
2000-12-18T00:00:00, 利润记录，毛利润 -0.06，净利润 -0.12
将这些 “净利润” 相加，最终的数字是 15.83。但系统告诉我们最终投资组合价值是 100016.98。显然，15.83 并不等于 16.98。

这其实并没有任何错误，净利润 15.83 是已平仓的交易利润。而最后一天实际还有一个未平仓头寸。虽然已发送了卖出操作，还要等待下个 bar 才能成交。最终投资组合价值止于 2000-12-29 的收盘价。这个订单的成交价格将会在下一个交易日（即 2001-01-02）被设定。

假设，我们将数据源提供到下一个交易日。

2001-01-02T00:00:00, 卖出执行，价格：27.87，成本：27.87，佣金 0.03
2001-01-02T00:00:00, 利润记录，毛利润 1.64，净利润 1.59
2001-01-02T00:00:00, 收盘价，24.87
2001-01-02T00:00:00, 创建买入订单，24.87
最终投资组合价值：100017.41
现在将先前的净利润与已完成操作的净利润相加：

15.83 + 1.59 = 17.42
忽略四舍五入的误差，现在一切就对上了。

12 12参数定义.txt ##################################################
文件路径: 12参数定义.txt
================================================================================

前面的案例中，参数都是硬编码在策略中。本节将介绍如何在 backtrader 自定义参数。

定义参数#
策略参数的定义非常简单，如在策略中定义两个参数：myparam 和 exitbars。

class TestStrategy:
    params = (('myparam', 27), ('exitbars', 5),)
参数 myparam 的默认值是 27，exitbars 的默认值是 5。

配置参数#
我们可以在添加策略时修改参数默认值。

# Add a strategy
cerebro.addstrategy(TestStrategy, myparam=20, exitbars=7)
使用参数#
策略代码中直接通过 self.params.param_name 即可调用参数。

如下代码，通过参数 exitbars 修改退出逻辑：

if len(self) >= (self.bar_executed + self.params.exitbars):
完整示例#
import backtrader as bt

class TestStrategy(bt.Strategy):
    params = (
        ('exitbars', 5),
    )

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log('OPERATION PROFIT, GROSS

 %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])

        if self.order:
            return

        if not self.position:
            if self.dataclose[0] < self.dataclose[-1]:
                if self.dataclose[-1] < self.dataclose[-2]:
                    self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    self.order = self.buy()
        else:
            if len(self) >= (self.bar_executed + self.params.exitbars):
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell()

13 13技术指标（Indicators）.txt ##################################################
文件路径: 13技术指标（Indicators）.txt
================================================================================

本节将介绍如何使用技术指标，将技术指标作为入场和出场信号。我们将用简单移动平均线（Simple Moving Average），或称 SMA，作为演示指标。SMA 是一个非常简单的技术指标，计算一定周期的价格均值。

交易规则#
基于 SMA 交易规则，定义如下所示：

入场条件： 当收盘价大于最新的 SMA，则入场买入。
出场条件： 当持有头寸，当收盘价小于 SMA，则出场卖出。
前面章节的策略代码大部分可复用，现在重点关注如何计算技术指标。

指标计算#
backtrader 下的 indicators 模块内置了大量技术指标的计算方法，如 SMA 简单移动均线的计算。

self.sma = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.maperiod)
如上代码中参数 self.params.maperiod 就是 SMA 的均线周期。

注：如果安装了 talib，backtrader 也集成了 talib 的支持，详情文档 指标-TALib。

条件判断#
现在基于 self.sma 判断进出场条件。

为了简化代码，这里只考虑 SMA 的判断逻辑，在完整实例中会包含所有情况。

入场判断：

self.dataclose[0] > self.sma[0]
出场判断：

self.dataclose[0] < self.sma[0]
策略代码#
起始现金 1000 货币单位。

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import backtrader as bt
策略部分：

class TestStrategy(bt.Strategy):
    params = (
        ('maperiod', 15),
    )

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])

        if self.order:
            return

        if not self.position:
            if self.dataclose[0] > self.sma[0]:
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.order = self.buy()
        else:
            if self.dataclose[0] < self.sma[0]:
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell()

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy)

    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, '../../datas/orcl-1995-2014.txt')

    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        fromdate=datetime.datetime(2000, 1, 1),
        todate=datetime.datetime(2000, 12, 31),
        reverse=False)

    cerebro.adddata(data)
    cerebro.broker.setcash(1000.0)
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    cerebro.broker.setcommission(commission=0.0)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
输出：

Starting Portfolio Value: 1000.00
2000-01-24, Close, 25.55
2000-01-25, Close, 26.61
2000-01-25, BUY CREATE, 26.61
2000-01-26, BUY EXECUTED, Size 10, Price: 26.76, Cost: 267.60, Commission 0.00
2000-01-26, Close, 25.96
2000-01-27, Close, 24.43
2000-01-27, SELL CREATE, 24.43
2000-01-28, SELL EXECUTED, Size 10, Price: 24.28, Cost: 242.80, Commission 0.00
2000-01-28, OPERATION PROFIT, GROSS -24.80, NET -24.80
...
...
...
2000-12-20, SELL CREATE, 26.88
2000-12-21, SELL EXECUTED, Size 10, Price: 26.23, Cost: 262.30, Commission 0.00
2000-12-21, OPERATION PROFIT, GROSS -20.60, NET -20.60
2000-12-21, Close, 27.82
2000-12-21, BUY CREATE, 27.82
2000-12-22, BUY EXECUTED, Size 10, Price: 28.65, Cost: 286.50, Commission 0.00
2000-12-22, Close, 30.06
2000-12-26, Close,

 29.17
2000-12-27, Close, 28.94
2000-12-28, Close, 29.29
2000-12-29, Close, 27.41
2000-12-29, SELL CREATE, 27.41
Final Portfolio Value: 973.90

14 14可视化.txt ##################################################
文件路径: 14可视化.txt
================================================================================

可视化#
通过 print 输出每个 bar 的信息不利于我们阅读，我们还是更倾向于图表的视觉效果。backtrader 内置了图表绘制的能力，一行代码即可绘图。

cerebro.plot()
请确保在调用cerebro.run()之后执行，还有，backtrader 的绘图能力依赖 matplotlib。

演示#
为了展示出基本的价格和收益外，我们将执行以下操作以展示绘图的功能和配置。

添加一个 EMA（指数移动平均线），默认情况下，它会与数据一起绘制。
添加一个 WMA（移动平均线加权），配置在子图绘制（即使没有意义）。
添加一个 StochasticSlow（慢速随机指标），不更改默认设置。
添加一个 MACD，不更改默认设置。
添加一个ATR，更改默认设置以避免绘图。
添加一个 RSI，不更改默认设置。
在 RSI 上添加一个 SMA 指标，不更改默认设置，且与RSI一起绘制。
在策略的 __init__ 方法中添加的所有内容：

# Indicators for the plotting show
bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
bt.indicators.WeightedMovingAverage(self.datas[0], period=25).subplot = True
bt.indicators.StochasticSlow(self.datas[0])
bt.indicators.MACDHisto(self.datas[0])
rsi = bt.indicators.RSI(self.datas[0])
bt.indicators.SmoothedMovingAverage(rsi, period=10)
bt.indicators.ATR(self.datas[0]).plot = False
即使将指标没有赋值到策略成员变量（如self.sma = MovingAverageSimple…），它们也会被注册到策略中，成为图表的一部分。

示例中，只有RSI被添加到临时变量rsi中，其目的是要在其上创建一个 SmoothedMovingAverage。

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import backtrader as bt

class TestStrategy(bt.Strategy):
    params = (
        ('maperiod', 15),
    )

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod)

        # Indicators for the plotting show
        bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        bt.indicators.WeightedMovingAverage(self.datas[0], period=25,
                                            subplot=True)
        bt.indicators.StochasticSlow(self.datas[0])
        bt.indicators.MACDHisto(self.datas[0])
        rsi = bt.indicators.RSI(self.datas[0])
        bt.indicators.SmoothedMovingAverage(rsi, period=10)
        bt.indicators.ATR(self.datas[0], plot=False)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])

        if self.order:
            return

        if not self.position:
            if self.dataclose[0] > self.sma[0]:
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.order = self.buy()
        else:
            if self.dataclose[0] < self.sma[0]:
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell()

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy)

    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, '../../datas/orcl-1995-2014.txt')

    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        fromdate=datetime.datetime(2000, 1, 1),
        todate=datetime.datetime(2000, 12, 31),
        reverse=False)

    cerebro.adddata(data)
    cerebro.broker.setcash(1000.0)
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    cerebro.broker.setcommission(commission=0.0)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Plot the result
    cerebro.plot()
执行后的输出：

Starting Portfolio Value: 1000.00
2000-02-18, Close, 27.61
2000-02-22, Close, 27.97
2000-02-22, BUY CREATE, 27.97
2000-02-23, BUY EXECUTED, Size 10, Price: 28.38, Cost: 283.80, Commission 0.00
2000-02-23, Close, 29.73
...
...
...
2000-12-21, BUY CREATE, 27.82
2000-12-22, BUY EXECUTED, Size 10, Price: 28.65, Cost: 286.50, Commission 0.00
2000-12-22, Close, 30.06
2000-12-26, Close, 29.17
2000-12-27, Close, 28.94
2000-12-28, Close, 29.29
2000-12-29, Close, 27.41
2000-12-29, SELL CREATE, 27.41
Final Portfolio Value: 981.00
因为交易逻辑没有修改，故而结果和上节一样，图表如下：



Previous
技术指标
策略优化
Next



15 15策略优化.txt ##################################################
文件路径: 15策略优化.txt
================================================================================

策略优化#
许多交易书籍中提到，每个市场和每个交易的股票（或商品等）都有不同的节奏，没有一种适合所有的策略。

在绘图示例前，当策略开始使用一个指标，周期默认值为 15 个 bar。这是一个策略参数，可以用于优化，改变参数值以找出哪个更适合你的市场。

注意：关于优化及其优缺点的文献很多。但建议基本是：不要过度优化。如果交易思路不健全，优化可能会产生一个仅对回测数据集有效的正面结果。

示例修改为优化简单移动平均线的周期。为了清晰起见，已删除与买卖订单相关的任何输出。

示例如下：

import datetime  #For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import backtrader as bt

class TestStrategy(bt.Strategy):
    params = (
        ('maperiod', 15),
        ('printlog', False),
    )

    def log(self, txt, dt=None, doprint=False):
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
            self.bar_executed = len(self)

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

    def next(self):
        if self.order:
            return

        if not self.position:
            if self.dataclose[0] > self.sma[0]:
                self.order = self.buy()
        else:
            if self.dataclose[0] < self.sma[0]:
                self.order = self.sell()

    def stop(self):
        self.log('(MA Period %2d) Ending Value %.2f' %
                 (self.params.maperiod, self.broker.getvalue()), doprint=True)

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    strats = cerebro.optstrategy(
        TestStrategy,
        maperiod=range(10, 31))

    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, '../../datas/orcl-1995-2014.txt')

    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        fromdate=datetime.datetime(2000, 1, 1),
        todate=datetime.datetime(2000, 12, 31),
        reverse=False)

    cerebro.adddata(data)
    cerebro.broker.setcash(1000.0)
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    cerebro.broker.setcommission(commission=0.0)

    cerebro.run(maxcpus=1)
策略优化调用不再是 addstrategy，而是 optstrategy，且传递的是值的范围，而非单一值。

代码中添加了一个 stop 方法，当回测结束时会调用它。我们用它打印最终净值。

运行程序，系统将为每个范围值执行策略。

输出如下：

2000-12-29, (MA Period 10) Ending Value 880.30
2000-12-29, (MA Period 11) Ending Value 880.00
2000-12-29, (MA Period 12) Ending Value 830.30
2000-12-29, (MA Period 13) Ending Value 893.90
2000-12-29, (MA Period 14) Ending Value 896.90
2000-12-29, (MA Period 15) Ending Value 973.90
2000-12-29, (MA Period 16) Ending Value 959.40
2000-12-29, (MA Period 17) Ending Value 949.80
2000-12-29, (MA Period 18) Ending Value 1011.90
2000-12-29, (MA Period 19) Ending Value 1041.90
2000-12-29, (MA Period 20) Ending Value 1078.00
2000-12-29, (MA Period 21) Ending Value 1058.80
2000-12-29, (MA Period 22) Ending Value 1061.50
2000-12-29, (MA Period 23) Ending Value 1023.00
2000-12-29, (MA Period 24) Ending Value 1020.10
2000-12-29, (MA Period 25) Ending Value 1013.30
2000-12-29, (MA Period 26) Ending Value 998.30
2000-12-29, (MA Period 27) Ending Value 982.20
2000-12-29, (MA Period 28) Ending Value 975.70
2000-12-29, (MA Period 29) Ending Value 983.30
2000-12-29, (MA Period 30) Ending Value 979.80
结果#
对于小于18的周期，策略亏损。
对于18到26（包括）的周期，策略盈利。
超过26的周期，策略再次亏损。
对于这个策略和数据集，得到最优参数是均线周期为 20 时，盈利78.00单位货币（即7.8%）。

16 16平台概念.txt ##################################################
文件路径: 16平台概念.txt
================================================================================

平台概念#
先介绍一些 backtrader 这个工具平台上的基础概念，希望能让你更好地了解和使用平台。

开始之前#
先导入必要的模块：

import backtrader as bt
import backtrader.indicators as btind
import backtrader.feeds as btfeeds
如下方法也可以访问子模块（如指标和数据源）：

import backtrader as bt

thefeed = bt.feeds.OneOfTheFeeds(...)
theind = bt.indicators.SimpleMovingAverage(...)
运算符，自然构造#
为了实现“易用”目标，平台允许（在 Python 的约束范围内）使用运算符。为了进一步增强此目标，运算符的使用被分为两个阶段。

阶段 1 - 运算符创建对象#
即使不是明确地为此目的，之前的一个示例已经看到这一点。在像指标和策略这样的对象的初始化阶段（__init__ 方法），运算符创建可以被操作、分配或保留以供策略逻辑的评估阶段稍后使用的对象。

再次查看 SimpleMovingAverage 的潜在实现，进一步分解为步骤。

在 SimpleMovingAverage 指标的 __init__ 方法内部的代码可能如下：

def __init__(self):
    # 求和 N 期值 - datasum 现在是一个 *Lines* 对象
    # 在使用运算符 [] 和索引 0 查询时
    # 返回当前和

    datasum = btind.SumN(self.data, period=self.params.period)

    # datasum（尽管是单行，但作为 *Lines* 对象）可以
    # 像在这种情况下那样自然地除以 int/float。
    # 实际上它可以被另一个 *Lines* 对象除。
    # 操作返回一个对象，分配给 "av"，该对象再次
    # 在使用 [0] 查询时返回当前的平均值

    av = datasum / self.params.period

    # av *Lines* 对象可以自然地分配给命名的
    # 线该指标交付。使用此
    # 指标的其他对象将可以直接访问计算结果

    self.line.sma = av
在策略的初始化中显示一个更完整的用例：

class MyStrategy(bt.Strategy):

    def __init__(self):

        sma = btind.SimpleMovingAverage(self.data, period=20)

        close_over_sma = self.data.close > sma
        sma_dist_to_high = self.data.high - sma

        sma_dist_small = sma_dist_to_high < 3.5

        # 不幸的是，"and" 不能在 Python 中被覆盖，
        # 因为它是语言构造而不是运算符，因此平台
        # 提供了一个函数来模拟它

        sell_sig = bt.And(close_over_sma, sma_dist_small)
在上述操作完成后，sell_sig 是一个线对象，可以在策略的逻辑中稍后使用，以指示条件是否满足。

阶段 2 - 运算符忠于自然#
让我们首先记住，一个策略有一个 next 方法，系统处理每个条时调用该方法。这是运算符实际上处于阶段 2 模式的地方。基于前面的示例：

class MyStrategy(bt.Strategy):

    def __init__(self):

        self.sma = sma = btind.SimpleMovingAverage(self.data, period=20)

        close_over_sma = self.data.close > sma
        self.sma_dist_to_high = self.data.high - sma

        sma_dist_small = sma_dist_to_high < 3.5

        # 不幸的是，"and" 不能在 Python 中被覆盖，
        # 因为它是语言构造而不是运算符，因此平台
        # 提供了一个函数来模拟它

        self.sell_sig = bt.And(close_over_sma, sma_dist_small)

    def next(self):

        # 尽管这看起来不像是一个“运算符”，但实际上是
        # 在测试对象是否响应 True/False

        if self.sma > 30.0:
            print('简单移动平均线大于 30.0')

        if self.sma > self.data.close:
            print('简单移动平均线高于收盘价')

        if self.sell_sig:  # if sell_sig == True: 也是有效的
            print('卖出信号为真')
        else:
            print('卖出信号为假')

        if self.sma_dist_to_high > 5.0:
            print('简单移动平均线与高点的距离大于 5.0')
不是一个非常有用的策略，只是一个示例。在阶段 2 中，运算符返回预期的值（如果测试为真，则为布尔值，如果与浮点数比较，则为浮点数），算术运算也返回预期值。

注意

请注意，比较实际上并没有使用 [] 操作符。这是为了进一步简化事情。

if self.sma > 30.0: 比较 self.sma[0] 和 30.0（第一行和当前值）
if self.sma > self.data.close: 比较 self.sma[0] 和 self.data.close[0]
一些未覆盖的运算符/函数#
Python 不允许覆盖所有内容，因此提供了一些函数来应对这些情况。

注意

仅在阶段 1 中使用，用于创建对象以便稍后提供值。

运算符：

and -> And
or -> Or
逻辑控制：

if -> If
函数：

any -> Any
all -> All
cmp -> Cmp
max -> Max
min -> Min
sum -> Sum
Sum 实际上使用 math.fsum 作为底层操作，因为平台使用浮点数，应用常规求和可能会影响精度。

reduce -> Reduce
这些实用运算符/函数对可迭代对象操作。可迭代对象中的元素可以是常规的 Python 数值类型（整数、浮点数等），也可以是具有线的对象。

生成非常愚蠢的买入信号的示例：

class MyStrategy(bt.Strategy):

    def __init__(self):

        sma1 = btind.SMA(self.data.close, period=15)
        self.buysig = bt.And(sma1 > self.data.close, sma1 > self.data.high)

    def next(self):
        if self.buysig[0]:
            pass  # 在这里做一些事情
显然，如果 sma1 高于高点，它必须高于收盘价。但重点是说明 bt.And 的使用。

使用 bt.If：

class MyStrategy(bt.Strategy):

    def __init__(self):

        sma1 = btind.SMA(self.data.close, period=15)
        high_or_low = bt.If(sma1 > self.data.close, self.data.low, self.data.high)
        sma2 = btind.SMA(high_or_low, period=15)
分解：

在 data.close 上生成一个周期为 15 的 SMA
然后
bt.If 的值大于 close，返回 low，否则返回 high
请记住，在调用 bt.If 时没有实际值返回。它返回一个线对象，就像 SimpleMovingAverage 一样。

值将在系统运行时计算。

生成的 bt.If 线对象然后被馈送到第二个 SMA，该 SMA 有时使用低价，有时使用高价进行计算。

这些函数也接受数值。同样的示例有一个修改：

class MyStrategy(bt.Strategy):

    def __init__(self):

        sma1 = btind.SMA(self.data.close, period=15)
        high_or_30 = bt.If(sma1 > self.data.close, 30.0, self.data.high)
        sma2 = btind.SMA(high_or_30, period=15)
现在，第二个移动平均线使用 30.0 或高价进行计算，具体取决于 sma 和 close 的逻辑状态。

注意

值 30 内部被转换为一个伪可迭代对象，该对象总是返回 30。

17 17数据源 - 配置与使用.txt ##################################################
文件路径: 17数据源 - 配置与使用.txt
================================================================================

数据源 - 配置与使用#
本节介绍 backtrader 中数据源的配置与使用，同时也包含了一些数据访问的技巧。

数据配置#
在 Backtrader 中，数据源 DataFeed 通过 Celebro 配置。

配置代码：

cerebro = bt.Cerebro()

data = btfeeds.MyFeed(...)
cerebro.adddata(data)
cerebro.addstrategy(MyStrategy, period=30)
通过 cerebro.adddata 将 DataFeed 添加到系统中。我们无需关心系统是如何接收 DataFeed 的。

使用方法#
策略中，我们通过 self.datas 数组即可访问数据。我们看一个简单示例，如我们实现策略。

示例如下：

class MyStrategy(bt.Strategy):
    params = dict(period=20)

    def __init__(self):
        sma = btind.SimpleMovingAverage(self.datas[0], period=self.params.period)
通过 self.datas[0] 即可访问数据。

示例中有两个注意点：

策略的 __init__ 方法无需接收 *args 或 **kwargs；
self.datas 是一个包含 DataFeed 的数组，至少包含一个数据源，否则会出现异常；
一旦数据源被添加到系统中，我们在策略实现就可以按它们添加的顺序访问到每个数据源。

cerebro.adddata(data0)
cerebro.adddata(data1)
在策略类访问：

self.datas[0] # data0
self.datas[1] # data1
快捷访问#
数据源也可通过快捷方式轻松访问，self.datas 数组中的每个元素都可以通过自动生成的成员变量进行访问：

对应规则：

self.data 对应的是 self.datas[0]
self.dataX 对应的是 self.datas[X]
示例：

class MyStrategy(bt.Strategy):
    params = dict(period=20)

    def __init__(self):
        sma = btind.SimpleMovingAverage(self.data, period=self.params.period)
示例中的 self.data 是 self.datas[0] 的快捷方式，即访问的就是第一个数据源。如果你添加了多个数据源，就可以通过 self.data1 访问 self.datas[1]，self.data2 访问 self.datas[2]，依次类推。

省略数据源#
上面的示例还可以进一步简化。

在调用 SimpleMovingAverage 时，我们可以完全省略 self.data，backtrader 会自动选择数据源：

class MyStrategy(bt.Strategy):
    params = dict(period=20)

    def __init__(self):
        sma = btind.SimpleMovingAverage(period=self.params.period)
在这个简化版本中，SimpleMovingAverage 没有显式传递 self.data。

如果省略了 self.data，SimpleMovingAverage 会默认选择第一个数据源（即 self.data 或 self.datas[0]）作为输入。

好的，我将按照步骤来简化表达，这样更清晰易懂：

数据延伸#
在 Backtrader 中，不仅数据源可以作为输入，指标和计算结果也能作为数据提供给策略。

通过一个示例说明吧。

将数据源作为输入计算指标，如：

sma1 = btind.SimpleMovingAverage(self.datas[0], period=self.p.period1)
self.datas[0] 是第一个数据源，它传递给 SimpleMovingAverage 进行计算。

基于计算出的指标生成新的变量，如：

sma2 = btind.SimpleMovingAverage(sma1, period=self.p.period2)
还可以在指标之间进行运算，将操作结果作为新的变量：

 diff = sma2 - sma1 + self.data.close
操作结果可以像数据源一样传递给下一个指标计算函数：

sma3 = btind.SimpleMovingAverage(diff, period=self.p.period3)
greater = sma3 > sma1
sma4 = btind.SimpleMovingAverage(greater, period=self.p.period4)
如上的步骤中，我们不断将计算的中间结果作为新的数据源，传递给后续指标进一步计算。

18 18策略参数.txt ##################################################
文件路径: 18策略参数.txt
================================================================================

策略参数#
策略基本上都需要参数，而在 backtrader 中，这些参数可作为类属性进行声明。我们可以通过元组或字典的形式声明这些策略变量。

元组：

class MyStrategy(bt.Strategy):
    params = (('period', 20),)
字典：

class MyStrategy(bt.Strategy):
    params = dict(period=20)
无论是元组还是字典，参数声明后，都可以通过 self.params 或 self.p 访问参数的值。

class MyStrategy(bt.Strategy):
    params = (('period', 20),)
    def __init__(self):
        sma = btind.SimpleMovingAverage(self.data, period=self.p.period)
在这个例子中，self.p.period 就是获取 period 参数的值。

参数继承#
如果你在一个类中定义了参数，子类会自动继承这些参数。你可以在子类中重写这些参数的默认值。

class BaseStrategy(bt.Strategy):
   params = (('period', 20),)

class MyStrategy(BaseStrategy):
   params = (('period', 30),)  # 重写父类的 period 参数
如果你使用多重继承，子类会继承所有父类的参数。如果多个父类定义了相同的参数，子类会使用继承列表中最后一个类的默认值。

Previous
数据源 DataFeed
线 Line 类
Next



19 19线 Line 类.txt ##################################################
文件路径: 19线 Line 类.txt
================================================================================

线 Line 类#
在 Backtrader 中，许多对象都会生成 Line 对象，而每个 Line 代表的是一个时间序列数据，可以是价格、指标或其他数据。策略逻辑基本都离不开操作 Line 对象。

Line 的访问#
数据源中的 Line#
数据源中包含了多个 Line，如 close、open、high、low ，通过 self.data.lines 访问它们。

class MyStrategy(bt.Strategy):
   def __init__(self):
       self.close_line = self.data.lines.close  # 访问收盘价线
指标中的 Line#
指标同样会生成 Line，如 SimpleMovingAverage 的 sma，通过 self.movav.lines.sma 访问。

class MyStrategy(bt.Strategy):
   def __init__(self):
       self.movav = btind.SimpleMovingAverage(self.data, period=20)

   def next(self):
       if self.movav.lines.sma[0] > self.data.lines.close[0]:
           print('移动平均大于收盘价')
访问线的快捷方式#
前面的语法和我们平时使用的不一样，因为我们平时都是通过简写访问，如 self.data.close 实际上是 self.data.lines.close 的快捷方式。

Backtrader 提供了多种简化访问 Line 的方式：

xxx.lines 可简写 xxx.l；
xxx.lines.name 可简写 xxx.lines_name；
xxx.lines[0] 可简写为 xxx
xxx.lines[X] 可简写为 xxx.lineX；
还有如：

self.data_name 等同于 self.data.lines.name；
对于有编号的 data，如 self.data1_name，等同于 self.data1.lines.name。
还有 self.dataX_Y 等同于 self.data[X].lines[Y]；
一些常用的简化写法，通过属性访问这些 Line：

self.data.close 或 self.data_close 直接访问 close 数据行。
self.movav.sma 或 self.movav_sma 直接访问 sma 数据行。
self.movav 也可直接访问 sma 数据行；
这种访问方式很简洁，但不如原始方法清晰，特别是在区分访问的是否 Line 时。

线的声明#
在 Backtrader 中，Line 是指标和策略中非常重要的部分。每个自定义指标都要声明自己的线，以便在策略中使用。

如何声明线#
如何在自定义指标中声明线？

当你创建一个自定义指标时，需要通过 lines 属性声明该指标会输出的线。通常使用元组声明，元组中的每个元素表示一个线的名称。

如在 SimpleMovingAverage 指标中，我们声明了一个名为 sma 的线：

class SimpleMovingAverage(bt.Indicator):
   lines = ('sma',)  # 声明一个名为 sma 的线
   
   def __init__(self):
       self.lines.sma = self.data.close(-1)  # 计算并赋值给 sma 线
如你想声明多条线，如一个包含两条均线的指标，只需在 lines 中列出多个元素：

class MyIndicator(bt.Indicator):
   lines = ('sma1', 'sma2')  # 声明两个线：sma1 和 sma2
   
   def __init__(self):
       self.lines.sma1 = btind.SimpleMovingAverage(self.data, period=20)
       self.lines.sma2 = btind.SimpleMovingAverage(self.data, period=50)
注意事项：当声明 Line 时，确保使用元组声明，即使只有一条线也要加上逗号：('sma',)。

现在，指标的计算结果会被保存在 Line 中，策略可以直接访问这些 Line 计算交易逻辑。

Line 的长度#
在 Backtrader 中，每条线都包含一个动态增长的点集合。你可以随时获取线的长度，以了解当前的数据处理情况。

如何获取线的长度：#
使用 len() 函数：使用标准 Python len() 函数即可获取 Line 的长度，这会返回已处理的数据点数。

class MyStrategy(bt.Strategy):
   def next(self):
       length = len(self.data)
       print(f"数据源的线长: {length}")
使用 buflen 属性：buflen 返回数据源可用的总数据条数，也就是数据源在加载时的总长度。

class MyStrategy(bt.Strategy):
   def next(self):
       buflen = self.data.buflen
       print(f"数据源的总长度: {buflen}")
实盘交易时，对于实时数据源很有用，因为它能让我们显示数据源的实际可用数量。

len() 和 buflen 的区别：

len() 返回已处理的数据条数，即实际运行到当前时间点的数据长度。
buflen 返回的是数据源加载的总条数，即加载的所有数据的长度。
如果两者的值相同，说明所有数据都已经处理完毕。

Line 的继承#
Backtrader 支持 Line 的继承，我们可以在子类中继承父类的线，且可以在子类中修改。

示例代码：

class BaseIndicator(bt.Indicator):
    lines = ('sma',)

class MyIndicator(BaseIndicator):
    lines = ('sma', 'ema')  # 在子类中继承并扩展线
如果多个父类定义了相同名称的线，子类只会继承一个版本的线，因此要避免同名的线定义冲突。

Line 耦合#
Backtrader 允许你在多个时间框架下使用数据源，并支持将它们的线进行耦合。线耦合是指将不同时间周期的数据结合起来，以便在策略中进行跨时间框架的计算和分析。

如何使用线耦合：#
你可以在策略中同时使用多个数据源，每个数据源可能有不同的时间周期。例如，一个数据源是日线数据，另一个是周线数据：

class MyStrategy(bt.Strategy):
    def __init__(self):
        self.sma_daily = btind.SimpleMovingAverage(self.data0, period=20)  # 日线数据
        self.sma_weekly = btind.SimpleMovingAverage(self.data1, period=5)   # 周线数据
Backtrader 提供了 () 运算符来将不同时间框架的数据线耦合在一起。

例如：

class MyStrategy(bt.Strategy):
    def __init__(self):
        sma0 = btind.SMA(self.data0, period=15)  # 15 天的简单移动平均线
        sma1 = btind.SMA(self.data1, period=5)   # 5 周的简单移动平均线

        self.buysig = sma0 > sma1()  # 通过运算符将两个时间框架的线耦合
上面的例子中，sma0 和 sma1 分别是基于日线和周线数据计算的简单移动平均线。sma1() 用于将周线数据转换成日线数据的长度，从而进行跨时间框架的计算。

Line 耦合使得我们能更灵活地在策略中使用多个时间框架的数据，进行更复杂的分析和决策。

20 20索引和切片.txt ##################################################
文件路径: 20索引和切片.txt
================================================================================

索引和切片#
索引：0 和 -1#
在 Backtrader 中，Line 代表着一组按时间顺序排列的点。这些点在策略执行期间动态生成，可以通过索引来访问。

使用索引访问 Line#
访问当前值： 使用 0 索引访问当前的线值，如 self.data.close[0] 获取当前收盘价。

class MyStrategy(bt.Strategy):
   def next(self):
       print(self.data.close[0])  # 当前的收盘价
访问前值： 使用负数索引访问之前的值，如 self.data.close[-1] 获取上一条数据的收盘价。

class MyStrategy(bt.Strategy):
   def next(self):
       if self.data.close[0] > self.data.close[-1]:
           print("今天的收盘价高于昨日的收盘价")
索引的意义：

0 索引指向当前时刻的值，-1 指向上一个时刻的值，以此类推。
负数索引指向历史数据点，这对于时间序列分析和策略中的数据回溯非常有用。
简单示例：

class MyStrategy(bt.Strategy):
    def next(self):
        # 比较今天的收盘价和昨天的收盘价
        if self.data.close[0] > self.data.close[-1]:
            print("今天的收盘价更高")
        else:
            print("今天的收盘价更低")
在这个示例中，self.data.close[0] 是今天的收盘价，self.data.close[-1] 是昨天的收盘价。

切片#
Backtrader 不支持对 Line 对象的切片操作，这是为了保持设计的一致性。切片适用于普通的 Python 数组，但在 Backtrader 中，Line 对象是动态增长的，因此切片的使用存在一定的限制。

为什么不支持切片#
首先是 Line 的设计上要保持一致性。

Line 对象上的数据是通过索引（如 0 和 -1）动态访问，基于时间序列进行数据处理。切片在此情况下并不适用，因为线的数据是按时间顺序排列的。

而常规可索引对象的切片是什么样的？

对于普通的 Python 对象，切片操作如下：

my_list = [1, 2, 3, 4, 5]
sliced_list = my_list[1:3]  # 返回 [2, 3]
Backtrader 中的 Line 对象更像一个流式数据源，不能直接进行切片。

如何获取线的某些点#
虽然 Line 不支持切片，但你仍然可以使用 get() 方法来获取线的一部分数据。例如：

# 获取最后 10 个数据点
myslice = self.my_sma.get(size=10)  # 获取最近的 10 个值
这允许我们拿到指定数量的历史数据，且是按时间顺序拿到最近的数据。

延迟索引#
在 Backtrader 中，延迟索引允许你在 __init__ 阶段访问历史数据，而无需手动使用负索引。通常情况下，[] 操作符用于在 next 阶段提取数据值，而通过延迟索引，可以在初始化阶段引用历史数据，并生成可以在 next 方法中直接使用的 Lines 对象。

举个例子，如果你想比较前一日的收盘价与当前的简单移动平均线（SMA），你不需要在每次迭代中手动进行比较，而可以通过预先生成的 Lines 对象来实现：

初始化时使用延迟索引#
在 __init__ 方法中，你可以通过延迟索引定义需要的历史数据。例如，比较前一天的收盘价和当前的移动平均值：

class MyStrategy(bt.Strategy):
   params = dict(period=20)

   def __init__(self):
       self.movav = btind.SimpleMovingAverage(self.data, period=self.p.period)
       self.cmpval = self.data.close(-1) > self.movav  # 比较前一日收盘价与当前20日均线
这里，self.data.close(-1) 通过延迟索引获取前一天的收盘价，self.movav 是当前的20日简单移动平均线。self.cmpval 是一个新的 Lines 对象，保存了每次比较的结果。

在 next 方法中使用延迟数据#
在 next 方法中，你可以直接使用 Lines 对象的值进行逻辑判断。self.cmpval[0] 会返回当前条件是否成立：

class MyStrategy(bt.Strategy):
   def next(self):
       if self.cmpval[0]:  # 如果前一日收盘价高于当前移动平均线
           print("前一日收盘价高于当前简单移动平均线")
延迟索引的工作原理#
self.data.close(-1) 使用延迟索引从历史数据中提取前一天的收盘价。这个语法会返回一个 Line 对象，但它是延迟的，即相对于当前时刻，它表示的是前一个时间点的 Line。

语句 self.data.close(-1) > self.movav 会生成一个新的 Line 对象，该对象在 next 方法中返回 1（条件为真）或 0（条件为假），使你在 next 方法可直接使用比较结果。

通过这种方式，Backtrader 提供了更简洁和灵活的方式来引用和比较历史数据，而不需要手动管理索引，从而简化了策略的编写和逻辑实现。

21 21运算符.txt ##################################################
文件路径: 21运算符.txt
================================================================================

运算符#
在 Backtrader 中，运算符不仅用于常规的数学运算，还能构建复杂的策略逻辑。Backtrader 的自定义运算符让策略的数学和逻辑运算更自然和简洁。

如何使用运算符#
backtrader 支持基于运算符创建新的对象，如在 __init__ 中通过运算符计算多个指标，得到一个新的操作对象。

class MyStrategy(bt.Strategy):
   def __init__(self):
       sma = btind.SimpleMovingAverage(self.data, period=20)

       # 使用运算符创建新的逻辑对象
       close_over_sma = self.data.close > sma
       sma_dist_to_high = self.data.high - sma
       sma_dist_small = sma_dist_to_high < 3.5

       # 创建卖出信号
       self.sell_sig = bt.And(close_over_sma, sma_dist_small)
我们在 Line 对象上使用了常规的运算符，如加减乘除、大小比较等。这简化了策略代码，增强了策略逻辑的可读性和可维护性。

注：backtrader 的指标计算是自有的体系，不是基于 numpy 和 pandas，所以要单独实现这些运算符。

一些未覆盖的运算符/函数#
某些 Python 中的运算符没有被覆盖，backtrader 提供了专门的函数来模拟逻辑运算，如 bt.And 和 bt.Or 来实现逻辑 “与” 和 “或”。

下面把这些单独实现的运算符列出来看看吧。

逻辑运算符#
Python 中的 and 和 or 运算符无法在 Backtrader 中覆盖，backtradr 提供了 bt.And 和 bt.Or 来模拟这两个逻辑操作。

self.buy_sig = bt.And(self.data.close > self.sma, self.data.high < 50.0)
self.sell_sig = bt.Or(self.data.close < self.sma, self.data.low > 30.0)
数学函数#
Backtrader 也提供了替代 Python 标准库函数的方式，如 max 和 min 被替代为 bt.Max 和 bt.Min。这些函数可用于处理 Line 对象：

highest = bt.Max(self.data.high, period=20)  # 获取过去20个周期的最高价
lowest = bt.Min(self.data.low, period=20)    # 获取过去20个周期的最低价
使用 bt.If 模拟条件分支#
如果要按条件选择值，Backtrader 提供了 bt.If 来模拟条件分支。bt.If 的功能类似于 Python 中的三元运算符 x if condition else y，或者说是 numpy 中 where 函数。

class MyStrategy(bt.Strategy):
   def __init__(self):
       sma1 = btind.SMA(self.data.close, period=15)
       
       # 使用 bt.If 来根据条件选择价格
       high_or_low = bt.If(sma1 > self.data.close, self.data.low, self.data.high)
       sma2 = btind.SMA(high_or_low, period=15)  # 使用选中的值计算新的简单移动平均线
其他函数#
类似的，any 被替换为 bt.Any，all 被替换为 bt.All， sum 被替换为 bt.Sum，cmp 被替换为 bt.Cmp，还有 reduce 被替换为 bt.Reduce。

这些函数都可用于处理可迭代对象，与 Line 对象兼容。

sum_values = bt.Sum(self.data.close, period=10)  # 计算过去10个周期的收盘价总和

22 22启动和运行.txt ##################################################
文件路径: 22启动和运行.txt
================================================================================

启动和运行#
如果使用数据重播功能，将为同一个条多次调用next方法，因为条的发展被重播。

一个基本的策略派生类：

class MyStrategy(bt.Strategy):

    def __init__(self):
        self.sma = btind.SimpleMovingAverage(self.data, period=20)

    def next(self):
        if self.sma > self.data.close:
            self.buy()
        elif self.sma < self.data.close:
            self.sell()
策略还有其他方法（或挂钩点），可以覆盖：

class MyStrategy(bt.Strategy):

    def __init__(self):
        self.sma = btind.SimpleMovingAverage(self.data, period=20)

    def next(self):
        if self.sma > self.data.close:
            submitted_order = self.buy()
        elif self.sma < self.data.close:
            submitted_order = self.sell()

    def start(self):
        print('回测即将开始')

    def stop(self):
        print('回测已结束')

    def notify_order(self, order):
        print('已收到新订单/更改/执行/取消通知')
start和stop方法应该是不言自明的。正如预期的那样，并遵循打印函数中的文本，当策略需要通知时将调用notify_order方法。用例：

请求买入或卖出（如在next中所见）
buy/sell将返回一个提交给经纪人的订单。保持对这个提交订单的引用由调用
者决定。

它可以用于确保如果订单仍在待处理状态，则不提交新订单。
如果订单被接受/执行/取消/更改，经纪人将通过notify方法将状态变化（例如执行规模）通知策略。
快速入门指南在notify_order方法中有一个完整的功能示例来进行订单管理。

可以通过其他策略类做更多事情：

buy / sell / close
使用底层经纪人和定量器发送买入/卖出订单给经纪人

同样可以通过手动创建订单并将其传递给经纪人来完成。但平台的目的是使使用它的人更容易。

close将获取当前市场头寸并立即关闭它。

getposition（或属性“position”）
返回当前市场头寸

setsizer/getsizer（或属性“sizer”）
这些允许设置/获取底层股份定量器。可以检查相同情况的不同股份定量器逻辑（固定大小、与资本成比例、指数等）

有很多文献，但Van K. Tharp在这方面有很好的书籍。

策略是一个线对象，这些对象支持参数，使用标准Python kwargs 参数收集：

class MyStrategy(bt.Strategy):

    params = (('period', 20),)

    def __init__(self):
        self.sma = btind.SimpleMovingAverage(self.data, period=self.params.period)
    ...
请注意，SimpleMovingAverage不再以固定值20实例化，而是以策略定义的参数“period”实例化。

Cerebro#
一旦数据源可用并定义了策略，Cerebro实例就将所有内容结合在一起并执行操作。实例化一个非常简单：

cerebro = bt.Cerebro()
如果没有特别的需求，默认值将照顾一切。

创建一个默认经纪人
操作无佣金
数据源将被预加载
默认执行模式将是runonce（批处理操作），这是最快的
所有指标都必须支持runonce模式以达到全速。平台中包含的那些支持。

自定义指标不需要实现runonce功能。Cerebro将模拟它，这意味着那些不兼容runonce的指标将运行得更慢。但系统的大部分仍将在批处理模式下运行。

由于数据源已经可用，策略也已经创建，标准的将它们结合在一起并启动运行的方法是：

cerebro.adddata(data)
cerebro.addstrategy(MyStrategy, period=25)
cerebro.run()
请注意以下几点：

添加数据源“实例”
添加MyStrategy“类”及将传递给它的参数（kwargs）。
MyStrategy的实例化将在后台由cerebro完成，addstrategy中的任何kwargs将传递给它。
用户可以根据需要添加任意多个策略和数据源。策略如何相互通信以实现协调（如果需要）不受平台的强制/限制。

当然，Cerebro提供额外的可能性：

决定预加载和操作模式：
cerebro = bt.Cerebro(runonce=True, preload=True)
这里有一个限制：runonce需要预加载（如果没有，不能运行批处理操作）。当然，预加载数据源并不强制runonce。

setbroker / getbroker（和broker属性）
如果需要，可以设置自定义经纪人。也可以访问实际的经纪人实例。

绘图。常规情况下只需：
cerebro.run()
cerebro.plot()
plot接受一些参数用于自定义：

numfigs=1
如果绘图过于密集，可以将其分成多个图

plotter=None
可以传递一个客户绘图器实例，cerebro将不实例化默认的。

**kwargs - 标准关键字参数

将传递给绘图器。

请参阅绘图部分了解更多信息。

策略优化#
如上所述，Cerebro获取一个策略派生类（不是实例）以及将在实例化时传递给它的关键字参数，这将在调用“run”时发生。

这是为了启用优化。相同的策略类将根据需要实例化多次，并带有新参数。如果将实例传递给cerebro…这将是不可能的。

请求优化如下：

cerebro.optstrategy(MyStrategy, period=xrange(10, 20))
optstrategy方法的签名与addstrategy相同，但执行额外的内部操作以确保优化按预期运行。策略可能会将范围视为策略的常规参数，而addstrategy不会对传递的参数做出假设。

另一方面，optstrategy将理解一个可迭代对象是一组值，必须按顺序传递给策略类的每个实例化。

注意，传递的是一系列值而不是单个值。在这个简单的例子中，将为此策略尝试10个值10 -> 19（20是上限）。

如果开发了具有额外参数的更复杂策略，它们都可以传递给optstrategy。必须不进行优化的参数可以直接传递，无需终端用户创建只有一个值的虚拟可迭代对象。例如：

cerebro.optstrategy(MyStrategy, period=xrange(10, 20), factor=3.5)
optstrategy方法看到factor并在后台为factor创建（需要的）虚拟可迭代对象，该对象只有一个元素（在示例中为3.5）。

注意

交互式Python shell和某些类型的Windows下冻结的可执行文件在使用Python多进程模块时存在问题。

请阅读Python文档了解多进程模块。

23 23Line 迭代器.txt ##################################################
文件路径: 23Line 迭代器.txt
================================================================================

Line 迭代器#
Backtrader 引入了一个独特的概念，叫做 Line 迭代器（Line Iterator）。它的核心思想是，通过迭代数据来驱动策略和指标的运作。这一点和 Python 的普通迭代器在表面上看有些相似，但实际上它们是为金融数据处理量身定制的。

在 Backtrader 中，策略 和 指标 都是基于 Line 迭代器构建的。下面，我们会逐步拆解这个概念，让它变得简单易懂。

什么是 Line 迭代器？#
Line 迭代器是一个控制 “数据处理节奏” 的工具，它的主要职责是：

驱动数据流动：Line 迭代器像是一个“指挥者”，它会触发从属 Line 迭代器（如指标或策略）依次处理数据。
逐步更新数据：Line 迭代器按照声明的规则迭代数据，并在每一步设置对应的结果。
Line 迭代器如何工作？#
三大关键方法#
prenext

在数据不足以完成计算时被调用。
用于初始化阶段的数据处理，比如累计数据。
nextstart

当累积到足够多的数据点，达到“最小周期”时被调用，仅触发一次。
默认会调用 next 方法。
next

在每次迭代时调用，用于正式处理当前索引上的数据。
为什么需要这些方法？#
为了生成有效的计算结果，某些指标需要一个“缓冲期”。如 25 周期的简单移动平均线 (SMA) 需要累积 25 个数据点才能生成第一个值。在这之前，我们需要用 prenext 来处理空白期。

一旦累积到足够的数据点，进入“正式运行”阶段后，next 方法会被不断调用，每次处理新到达的数据。

示例：如何实现一个简单的 SMA#
以下是一个 SimpleMovingAverage（简单移动平均线）的实现示例：

class SimpleMovingAverage(Indicator):
    lines = ('sma',)
    params = dict(period=25)

    def prenext(self):
        print(f'prenext:: 当前周期: {len(self)}')

    def nextstart(self):
        print(f'nextstart:: 当前周期: {len(self)}')
        self.next()  # 模拟默认行为

    def next(self):
        print(f'next:: 当前周期: {len(self)}')
实例化 SMA 的过程#
假设我们为一个数据集创建一个 SimpleMovingAverage 指标：

sma = btind.SimpleMovingAverage(self.data, period=25)
SMA 的调用流程#
prenext：

前 24 次调用。
在指标数据不足 25 个点时，每次新数据到达时调用，用于累积数据。
nextstart：

第 25 次调用。
数据点达到 25 时，开始生成第一个有效的 SMA 值。
next：

从第 26 次开始，每次新数据到达时调用。
多层指标的交互#
当一个指标的输出作为另一个指标的输入时，会发生什么？比如下面的情况：

sma1 = btind.SimpleMovingAverage(self.data, period=25)
sma2 = btind.SimpleMovingAverage(sma1, period=20)
调用流程#
sma1 的最小周期是 25：

需要 25 个数据点后才能生成第一个有效值。
在此之前，sma1 的 prenext 被调用 24 次。
sma2 的最小周期是 sma1 的 25 加上自己的 20：

sma2 的 prenext 被调用 44 次。
第 45 次调用时，sma2 的 nextstart 被触发，并开始生成第一个有效值。
因此，sma2 的计算需要至少 45 个数据点才能开始正常工作。

指标的性能优化：runonce 模式#
为了提高性能，Backtrader 提供了一个批量处理模式，叫做 runonce。它可以一次性处理多个数据点，而不是逐步调用 next 方法。

runonce 的核心方法#
once(self, start, end)

在最小周期达到时调用，批量处理 start 到 end 索引范围内的数据。
preonce(self, start, end)

类似于 prenext，但在批量模式下调用。
oncestart(self, start, end)

类似于 nextstart，但用于批量模式。
批量处理模式的优势是显著的，它可以减少不必要的函数调用，从而显著提高性能。

最小周期的意义#
最小周期是 Line 迭代器中一个关键的控制点，决定了何时开始生成有意义的输出值。例如：

对于一个 25 周期的 SMA，最小周期是 25。
当一个指标依赖另一个指标作为输入时，最小周期会累积。
在多层指标中，最小周期的自动调整可以确保所有数据都有意义。

Line 迭代器的核心价值#
控制节奏：线迭代器通过 prenext、nextstart 和 next 方法灵活控制数据处理的节奏。
支持复杂数据流：它允许多个指标相互依赖，同时自动调整最小周期。
性能优化：通过 runonce 模式，指标的批量处理显著提升了效率。
简单来说，Line 迭代器是 Backtrader 中隐藏的强大工具，它的引入让平台能够高效地处理多层次的指标和策略。

Previous
平台操作


24 24启动和运行.txt ##################################################
文件路径: 24启动和运行.txt
================================================================================

启动和运行#
Backtrader 的启动和运行过程主要依赖于三个核心组件：

数据源：提供市场数据，用于回测或实时交易。
策略：定义交易逻辑（基于类继承实现）。
Cerebro：核心管理器，负责整合数据源、策略，并启动回测或实时交易。
数据源#
数据源是回测和策略运行的基础，它为策略提供价格数据（如开盘价、高价、低价、收盘价）及其他市场信息。

支持的数据源#
本地数据文件：

支持多种 CSV 格式（如 Yahoo Finance 数据）。
支持从 Pandas DataFrame 加载数据。
在线数据提取：

提供内置的 Yahoo Finance 在线数据提取功能。
实时数据源：

支持 Interactive Brokers (IB)、Visual Chart 和 Oanda 等实时数据源。
平台支持通过 时间框架（如日线、5分钟线）和 压缩级别（如1天、5分钟）自定义数据，以适配不同交易策略。

数据源设置示例#
加载 Yahoo Finance 格式的 CSV 数据#
以下是一个基本的 CSV 数据加载示例：

import backtrader as bt
import datetime

datapath = 'path/to/your/yahoo/data.csv'

data = bt.feeds.YahooFinanceCSVData(
    dataname=datapath,
    reversed=True  # 如果数据是从最新日期到最早日期排列，需要设置为 True
)
如果数据跨越时间范围较长，可限制按时间限制加载的数据：

data = bt.feeds.YahooFinanceCSVData(
    dataname=datapath,
    reversed=True,  # 如果数据是从最新日期到最早日期排列，需要设置为 True
    fromdate=datetime.datetime(2014, 1, 1),  # 数据起始日期
    todate=datetime.datetime(2014, 12, 31),  # 数据结束日期
    timeframe=bt.TimeFrame.Days,  # 时间框架设置为日线
    compression=1,  # 每 1 天作为一个数据单位
    name='Yahoo Data'  # 数据源命名（可选）
)
从 Pandas DataFrame 加载数据#
如果你的数据存储在 Pandas DataFrame 中，可以使用以下方式加载：

import pandas as pd
import backtrader as bt

df = pd.read_csv('path/to/your/data.csv', index_col='Date', parse_dates=True)

data = bt.feeds.PandasData(
    dataname=df,
    fromdate=datetime.datetime(2020, 1, 1),
    todate=datetime.datetime(2020, 12, 31),
    timeframe=bt.TimeFrame.Days
)
设置多时间框架#
如果你需要同时加载 5 分钟和日线数据，可以分别加载不同时间框架的数据源：

data_5min = bt.feeds.GenericCSVData(
    dataname='path/to/5min_data.csv',
    timeframe=bt.TimeFrame.Minutes,
    compression=5
)

data_daily = bt.feeds.GenericCSVData(
    dataname='path/to/daily_data.csv',
    timeframe=bt.TimeFrame.Days,
    compression=1
)

cerebro.adddata(data_5min, name='5min')
cerebro.adddata(data_daily, name='daily')
策略（派生类）#
策略 是交易逻辑的核心，它定义了如何根据数据进行买卖操作。Backtrader 中的策略通过继承 bt.Strategy 类实现。

策略的基本方法#
策略类至少需要实现以下两个方法：

__init__：初始化方法，用于定义指标和变量。
next：逐条处理数据，用于执行交易逻辑。
当传递不同时间框架（条数不同）的数据源时，next 方法将基于主数据源迭代（即第一个传递给 Cerebro 的数据），主数据源应是时间框架最小的数据源。

对于 ReplayData，next 方法会被多次调用，特别是当数据跨时间框架时，Backtrader 会在每个数据条上执行 next，模拟数据的发展。

示例策略#
以下是一个简单的策略示例，基于 20 日简单移动平均线（SMA）进行交易：

class MyStrategy(bt.Strategy):
    def __init__(self):
        # 定义简单移动平均线（SMA）
        self.sma = bt.indicators.SimpleMovingAverage(self.data.close, period=20)

    def next(self):
        # 如果收盘价高于 SMA，则买入
        if self.data.close[0] > self.sma[0]:
            self.buy()
        # 如果收盘价低于 SMA，则卖出
        elif self.data.close[0] < self.sma[0]:
            self.sell()
扩展功能#
策略还可以覆盖以下方法，为回测和实时交易添加更多功能：

start：回测开始时调用（用于初始化资源）。
stop：回测结束时调用（用于清理资源或总结）。
notify_order：当订单状态发生变化时调用。
notify_trade：当交易状态发生变化时调用。
演示策略如下所示：

class MyStrategy(bt.Strategy):
    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data.close, period=20)

    def start(self):
        print('回测开始！')

    def stop(self):
        print('回测结束！')

    def notify_order(self, order):
        if order.status in [order.Completed]:
            print(f"订单完成: {order.info}")

    def next(self):
        if self.data.close[0] > self.sma[0]:
            self.buy()
        elif self.data.close[0] < self.sma[0]:
            self.sell()
其他操作#
在 Backtrader 中，策略类还提供各种交易操作。

买入 / 卖出 / 平仓（buy / sell / close）： 通过这些方法，策略可以向经纪人发送买入、卖出或平仓订单。平台也允许您手动创建订单并将其传递给经纪人，但通过这些内建的方法，可以让操作变得更简单和高效。

close：立即关闭当前市场头寸。

getposition（或属性 position）：返回当前的市场头寸。通过这个方法，您可以查看当前持有的仓位情况。

setsizer / getsizer（或属性 sizer）：这些方法允许您设置或获取底层的股份定量器（Sizer）。定量器负责计算每次交易的仓位大小，您可以根据需要选择不同的定量器类型，如固定大小、与资本成比例或指数等策略。

策略类本身是一个 Line 对象，支持配置参数。

class MyStrategy(bt.Strategy):

    params = (('period', 20),)

    def __init__(self):
        self.sma = btind.SimpleMovingAverage(self.data, period=self.params.period)
    ...
现在，SimpleMovingAverage 指标不再是固定的 20，而是根据策略中定义的 period 参数动态设置，这提高了策略的灵活性。

Cerebro#
一旦数据源可用并定义了策略，Cerebro 实例会将所有内容整合并执行。创建一个 Cerebro 实例非常简单：

cerebro = bt.Cerebro()
如果没有特别的需求，默认配置会自动处理以下内容：

创建一个默认经纪人；
操作不收取佣金；
数据源会被预加载；
默认执行模式为 runonce（批处理模式），这是最优的执行方式。
需要注意的是，所有指标都必须支持 runonce 模式，以确保执行速度达到最佳。平台中已经包含的指标大多都支持此模式。

典型流程#
创建 Cerebro 实例

cerebro = bt.Cerebro()
添加数据源

cerebro.adddata(data)
添加策略

cerebro.addstrategy(MyStrategy)
配置经纪人

设置初始资金、佣金等。

cerebro.broker.set_cash(100000)  # 设置初始资金
cerebro.broker.setcommission(commission=0.001)  # 设置佣金
运行回测

cerebro.run()
绘制回测结果

cerebro.plot()
plot接受一些参数用于自定义：

numfigs=1
如果绘图过于密集，可以将其分成多个图

plotter=None
可以传递一个绘图器实例给，cerebro 将不按默认绘图。

策略优化#
Backtrader 支持对策略参数进行优化。例如，我们可以测试不同的 SMA 周期参数对策略的影响：

cerebro.optstrategy(MyStrategy, period=range(10, 50, 5))
在上例中，period 参数会从 10 到 45（每次递增 5）进行测试，平台会自动运行每个参数组合的回测。

完整代码示例#
以下是一个完整的代码示例，整合了数据源、策略和 Cerebro：

import backtrader as bt
from datetime import datetime

# 定义策略
class MyStrategy(bt.Strategy):
    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data.close, period=20)

    def next(self):
        if self.data.close[0] > self.sma[0]:
            self.buy()
        elif self.data.close[0] < self.sma[0]:
            self.sell()

# 初始化 Cerebro
cerebro = bt.Cerebro()

# 加载数据
data = bt.feeds.YahooFinanceCSVData(
    dataname='path/to/your/data.csv',
    fromdate=datetime(2020, 1, 1),
    todate=datetime(2021, 1, 1)
)
cerebro.adddata(data)

# 添加策略
cerebro.addstrategy(MyStrategy)

# 配置初始资金和佣金
cerebro.broker.setcash(100000)
cerebro.broker.setcommission(commission=0.001)

# 启动回测
cerebro.run()

# 绘制结果
cerebro.plot()
通过这些核心组件的整合，Backtrader 提供了一个高度灵活的框架，适用于各种回测和实时交易需求。希望这部分的补充对你有所帮助！

25 25Cerebro.txt ##################################################
文件路径: 25Cerebro.txt
================================================================================

Cerebro#
Cerebro 是 Backtrader 的核心类，负责整个系统的运行。

它的功能包括：

收集输入（数据源）、执行者（策略）、观察者、评论者（分析器）和记录者（编写器），确保系统的正常运行。
执行回测或实时数据供给和交易。
返回回测结果。
提供策略绘图功能。
创建 Cerebro 实例#
创建 Cerebro 实例时，可以通过传递一些控制参数：

cerebro = bt.Cerebro(**kwargs)
这些参数会影响系统的执行，具体的参数说明可以参考文档（也可以应用于后续的 run 方法）。

添加数据源#
最常见的方式是使用 cerebro.adddata(data) 添加数据源，data 是已实例化的数据源。例如：

data = bt.BacktraderCSVData(dataname='mypath.days', timeframe=bt.TimeFrame.Days)
cerebro.adddata(data)
数据的重采样与重放#
Cerebro 也支持对数据进行重采样或重放：

重采样：

data = bt.BacktraderCSVData(dataname='mypath.min', timeframe=bt.TimeFrame.Minutes)
cerebro.resampledata(data, timeframe=bt.TimeFrame.Days)
重放数据：

data = bt.BacktraderCSVData(dataname='mypath.min', timeframe=bt.TimeFrame.Minutes)
cerebro.replaydata(data, timeframe=bt.TimeFrame.Days)
你可以同时使用多种类型的数据源，包括常规数据、重采样数据和重放数据。但需要确保它们的时间对齐。详见文档中的 多时间框架 和 数据重采样 部分。

添加策略#
Cerebro 接受策略类并传递相关参数，即使没有优化，也可以使用以下方式添加策略：

cerebro.addstrategy(MyStrategy, myparam1=value1, myparam2=value2)
策略优化#
在优化时，参数需要作为可迭代对象传递。例如：

cerebro.optstrategy(MyStrategy, myparam1=range(10, 20))
这会运行 MyStrategy 10次，myparam1 的值从 10 到 19。

添加其他组件#
你可以通过以下方法为回测添加额外的功能：

addwriter：记录回测数据。
addanalyzer：分析回测结果。
addobserver 或 addobservermulti：添加观察者，实时跟踪策略执行。
自定义经纪人#
Cerebro 默认使用 Backtrader 内建的经纪人，但你也可以自定义经纪人：

broker = MyBroker()
cerebro.broker = broker  # 通过 getbroker/setbroker 方法设置
接收通知#
数据源或经纪人可能会发出通知。Cerebro 通过 notify_store 方法接收这些通知。处理通知有三种方式：

使用回调函数#
你可以通过 addnotifycallback(callback) 向 Cerebro 添加回调函数，函数签名如下：

callback(msg, *args, **kwargs)
在策略中覆盖 notify_store 方法#
你也可以在策略类中直接覆盖 notify_store 方法来处理通知，签名如下：

def notify_store(self, msg, *args, **kwargs):
    # 处理通知
子类化 Cerebro#
通过子类化 Cerebro 并覆盖 notify_store，这是最不推荐的方法。

执行回测#
回测执行通过以下方法进行：

result = cerebro.run(**kwargs)
run 方法支持多种参数，可以在实例化时指定，详细说明可以参考文档。

标准观察者#
Cerebro 默认会实例化三个标准观察者：

经纪人观察者：追踪现金和投资组合的价值。
交易观察者：记录每笔交易的效果。
买卖观察者：记录操作的执行时间。
如果不需要这些标准观察者，可以通过 stdstats=False 禁用它们。

返回回测结果#
回测执行后，Cerebro 会返回策略实例，供你分析回测结果。你可以访问策略中的所有元素进行详细检查：

result = cerebro.run(**kwargs)
优化时的返回结果#
如果没有使用优化，result 将是一个策略实例列表。
如果进行了优化，result 将是一个列表的列表，每个内部列表对应一次优化运行后的策略实例。
注意：优化的默认行为已经更改，优化时只会返回分析器结果，优化的策略结果需要通过设置 optreturn=False 来获取。

提供绘图功能#
如果你安装了 matplotlib，可以通过以下方式绘制回测图形：

cerebro.plot()
回测流程概述#
回测的执行逻辑大致如下：

传递任何存储的通知。
数据源提供下一组 tick/条。
数据同步：多个数据源的数据会按时间对齐，确保不同时间框架的数据能够同时进行计算。
版本更新：1.9.0.99 版本引入了新的同步行为。
通知策略有关订单、交易和现金的更新。
经纪人接受排队订单，并根据新数据执行订单。
调用策略的 next 方法，评估新数据并执行策略逻辑。
更新观察者、指标、分析器等，触发其他活动。
将数据写入目标（通过编写器）。
重要注意事项#
在数据源传递新的一组数据时，这些数据是“已关闭”的。这意味着策略发出的订单将基于 下一条数据 执行，而不是当前数据。


#######################################################################################################
参数说明#
如下是 Cerebro 类的详细说明。

实例化参数#
参数	默认值	说明
preload	True	是否预加载传递给策略的不同数据源。
runonce	True	以矢量化模式计算指标，从而提高整个系统的性能。
注： 策略和观察者将始终基于事件运行。
live	False	如果没有数据报告为实时（通过数据的islive方法，但用户仍希望以实时模式运行，可将此参数设为true。
maxcpus	None	同时使用多少核心进行优化，默认 None，即启用所有可用的 CPU 核。
stdstats	True）	如果为True，将添加默认观察者：经纪人（现金和价值）、交易和买卖。
oldbuysell	False	如 stdstats 为 True 且自动添加观察者，此开关控制买卖观察者的主要行为。
oldtrades	False	如果stdstats为True 且自动添加观察者，此开关控制交易观察者的主要行为。
exactbars	False	
- False：默认值，将存储在 Line 中的值都保存到内存。
-True或1：所有Line对象的内存使用减少至计算最小周期。
如果简单移动平均线的周期为30，则底层数据将始终有一个30条的运行缓冲区，以允许计算简单移动平均线。
此设置将停用preload和runonce。
使用此设置还将停用绘图。
-1：策略级别的数据源和指标/操作将保留所有数据在内存中。
如 RSI 通过指标UpDay计算，不会将它的所有数据保留内存。
这允许保持绘图和预加载活动。
runonce将被停用。
-2：作为策略属性的数据源和指标将保留所有点在内存中。
例如：RSI内部使用指标UpDay进行计算。此子指标将不保留所有数据在内存中。
如果在__init__中定义了a = self.data.close - self.data.high，那么a将不保留所有数据在内存中。
- 这允许保持绘图和预加载活动。
runonce将被停用。
objcache	False	实验选项，用于实现 Line 对象的缓存并减少它们的数量。示例来自UltimateOscillator：
bp = self.data.close - TrueLow(self.data) 
# -> 创建另一个 TrueLow(self.data)
tr = TrueRange(self.data) 
如果为True，TrueRange内部的第二个TrueLow(self.data)将匹配bp计算中的签名，并将被重用。可能发生的极端情况是这会使线对象超出其最小周期并导致问题，因此被禁用。
writer	False	如果设置为True，将创建一个默认的WriterFile，它将打印到标准输出。它将被添加到策略中（除了用户代码添加的任何其他编写器）。
tradehistory	False	如果设置为True，它将激活所有策略中每个交易的更新事件日志记录。也可以通过策略方法set_tradehistory在每个策略基础上完成。
optdatas	True	如果为 True 且在优化（并且系统可以预加载和使用runonce），则数据预加载将仅在主进程中完成，以节省时间和资源。测试显示，执行时间从83秒减少到66秒，约20%的速度提升。
optreturn	True	如果为True，优化结果将不会是完整的策略对象（和所有数据、指标、观察者…），而是具有以下属性的对象（与策略相同）：
params（或p）	无	执行策略时的参数。
analyzers	无	策略已执行的分析器。大多数情况下，仅需要分析器和参数来评估策略的性能。如果需要详细分析生成的值（例如指标），请将其关闭。测试显示，执行时间提高了13% - 15%。结合optdatas，总收益增加到32%。
oldsync	False	从版本1.9.0.99开始，多个数据（相同或不同时间框架）的同步已更改，以允许不同长度的数据。如果希望使用数据0作为系统主控的数据的旧行为，请将此参数设置为True。
tz	None	为策略添加全局时区。参数tz可以是：
None：在这种情况下，策略显示的日期时间将是UTC，这一直是标准行为。
pytz实例。将用作将UTC时间转换为所选时区。
字符串。将尝试实例化pytz实例。
整数。对于策略，使用self.datas可迭代对象中相应数据的相同时区（0将使用data0的时区）。
cheat_on_open	False	将调用策略的next_open方法。

这发生在next之前，并且在经纪人有机会评估订单之前。指标尚未重新计算。这允许发布考虑前一天指标的订单，但使用开盘价进行股份计算。

对于cheat_on_open订单执行，还要调用 cerebro.broker.set_coo(True)或实例化一个BackBroker(coo=True)（coo表示cheat-on-open）或将broker_coo参数设置为True。除非在下文中禁用，否则Cerebro会自动执行此操作。
broker_coo	True	这将自动调用经纪人的set_coo方法，并将其设置为True以激活cheat_on_open执行。只有在cheat_on_open也为True时才会执行。
quicknotify	False	在传递下一个价格之前立即传递经纪人通知。对于回测没有影响，但对于实时经纪人，通知可能在条传递之前很久就发生。当设置为True时，将尽快传递通知（请参阅实时数据源中的qcheck）。为了兼容性，设置为False。可能会更改为True。
成员方法#
addstorecb(callback)
添加一个回调以获取将由notify_store方法处理的消息。回调的签名必须支持以下内容：

callback(msg, *args, **kwargs)
实际接收的msg、*args和**kwargs是实现定义的（完全依赖于数据/经纪人/存储），但通常应该期望它们是可打印的，以便接收和实验。

notify_store(msg, *args, **kwargs)
在cerebro中接收存储通知。此方法可以在Cerebro子类中覆盖。实际接收的msg、*args和**kwargs是实现定义的（完全依赖于数据/经纪人/存储），但通常应该期望它们是可打印的，以便接收和实验。

adddatacb(callback)
添加一个回调以获取将由notify_data方法处理的消息。回调的签名必须支持以下内容：

callback(data, status, *args, **kwargs)
实际接收的*args和**kwargs是实现定义的（完全依赖于数据/经纪人/存储），但通常应该期望它们是可打印的，以便接收和实验。

notify_data(data, status, *args, **kwargs)
在cerebro中接收数据通知。此方法可以在Cerebro子类中覆盖。实际接收的*args和**kwargs是实现定义的（完全依赖于数据/经纪人/存储），但通常应该期望它们是可打印的，以便接收和实验。

adddata(data, name=None)
将数据源实例添加到混合中。如果name不为None，将放入data._name，用于装饰/绘图目的。

resampledata(dataname, name=None, **kwargs)
添加数据源以供系统重新采样。如果name不为None，将放入data._name，用于装饰/绘图目的。任何其他如timeframe、compression、todate等支持的参数将透明地传递。

replaydata(dataname, name=None, **kwargs)
添加数据源以供系统重放。如果name不为None，将放入data._name，用于装饰/绘图目的。任何其他如timeframe、compression、todate等支持的参数将透明地传递。

chaindata(*args, **kwargs)
将多个数据源链接为一个。如果作为命名参数传递并且name不为None，将放入data._name，用于装饰/绘图目的。如果为None，则使用第一个数据的名称。

rolloverdata(*args, **kwargs)
将多个数据源链接为一个。如果作为命名参数传递并且name不为None，将放入data._name，用于装饰/绘图目的。如果为None，则使用第一个数据的名称。任何其他kwargs将传递给RollOver类。

addstrategy(strategy, *args, **kwargs)
为单次运行添加策略类。在运行时进行实例化。args和kwargs将在实例化期间按原样传递给策略。返回的索引可以与添加其他对象（如Sizer）引用兼容。

optstrategy(strategy, *args, **kwargs)
为优化添加策略类。在运行时进行实例化。args和kwargs必须是包含要检查值的可迭代对象。例如：如果策略接受参数period，为了优化目的，调用optstrategy如下：

cerebro.optstrategy(MyStrategy, period=(15, 25))
这将执行值为15和25的优化。而：

cerebro.optstrategy(MyStrategy, period=range(15, 25))
将以period值15 -> 25（25不包含，因为Python中的范围是半开的）执行MyStrategy。如果传递了一个参数但不应优化，调用如下：

cerebro.optstrategy(MyStrategy, period=(15,))
注意period仍然作为一个可迭代对象传递……只有一个元素。backtrader无论如何都会尝试识别如下情况：

cerebro.optstrategy(MyStrategy, period=15)
如果可能，将创建一个内部伪可迭代对象。

optcallback(cb)
将回调添加到回调列表中，当每个策略运行时将与优化一起调用。签名：cb(strategy)。

addindicator(indcls, *args, **kwargs)
添加指标类到混合中。在传递策略中进行实例化。

addobserver(obscls, *args, **kwargs)
添加观察者类到混合中。在运行时进行实例化。

addobservermulti(obscls, *args, **kwargs)
添加观察者类到混合中。在运行时进行实例化。将为系统中的每个数据添加一次。一个用例是观察单个数据的买入/卖出观察者。一个反例是观察系统范围值的CashValue。

addanalyzer(ancls, *args, **kwargs)
添加分析器类到混合中。在运行时进行实例化。

addwriter(wrtcls, *args, **kwargs)
添加编写器类到混合中。在cerebro中进行实例化。

run(**kwargs)
执行回测的核心方法。传递给它的任何kwargs将影响实例化时Cerebro的标准参数值。如果cerebro没有数据，该方法将立即退出。返回值不同：

无优化： 包含使用addstrategy添加的策略类实例的列表。
优化： 包含使用addstrategy添加的策略类实例的列表的列表。

runstop()
如果从策略内部或其他地方（包括其他线程）调用，将尽快停止执行。

setbroker(broker)
为此策略设置特定的经纪人实例，替换从cerebro继承的经纪人。

getbroker()
返回经纪人实例。也可以通过broker属性访问。

plot(plotter=None, numfigs=1, iplot=True, start=None, end=None, width=16, height=9, dpi=300, tight=True, use=None, **kwargs)
绘制cerebro中的策略。如果plotter为None，将创建一个默认的Plot实例，并在实例化期间将kwargs传递给它。

`numfigs`将图表分成所指示的数量，以减少图表密度。<br/>
`iplot`：如果为True且在笔记本中运行，图表将内联显示。<br/>
`use`：将其设置为所需matplotlib后端的名称。它将优先于`iplot`。<br/>
`start`：策略日期时间线数组的索引或表示绘图开始的`datetime.date`、`datetime.datetime`实例。<br/>
`end`：策略日期时间线数组的索引或表示绘图结束的`datetime.date`、`datetime.datetime`实例。<br/>
`width`：保存图形的宽度（以英寸为单位）。<br/>
`height`：保存图形的高度（以英寸为单位）。<br/>
`dpi`：保存图形的质量（以每英寸点数为单位）。<br/>
`tight`：仅保存实际内容而不保存图形框架。
addsizer(sizercls, *args, **kwargs)
添加一个Sizer类（和args），作为添加到cerebro的任何策略的默认定量器。

addsizer_byidx(idx, sizercls, *args, **kwargs)
按idx添加一个Sizer类。此idx是与addstrategy返回的索引兼容的引用。只有由idx引用的策略将收到此大小。

add_signal(sigtype, sigcls, *sigargs, **sigkwargs)
向系统添加一个信号，稍后将添加到SignalStrategy中。

signal_concurrent(onoff)
如果将信号添加到系统并且concurrent值设置为True，将允许并发订单。

signal_accumulate(onoff)
如果将信号添加到系统并且accumulate值设置为True，当已在市场中时进入市场，将允许增加头寸。

signal_strategy(stratcls, *args, **kwargs)
添加可以接受信号的SignalStrategy子类。

addcalendar(cal)
向系统添加一个全局交易日历。单个数据源可能有单独的日历覆盖全局日历。cal可以是TradingCalendar的实例、字符串或pandas_market_calendars的实例。字符串将实例化为PandasMarketCalendar（需要系统中安装模块pandas_market_calendar）。如果传递的是TradingCalendarBase的子类（而不是实例），它将被实例化。

addtz(tz)
也可以使用参数tz完成。为策略添加全局时区。参数tz可以是：

可选项	描述
None	在这种情况下，策略显示的日期时间将是UTC，这一直是标准行为。
pytz 实例	将用作将UTC时间转换为所选时区。
字符串	将尝试实例化pytz实例。
整数	对于策略，使用self.datas中相应数据的时区（0就用data0的时区）。
add_timer(when, offset=datetime.timedelta(0), repeat=datetime.timedelta(0), weekdays=[], weekcarry=False, monthdays=[], monthcarry=True, allow=None, tzdata=None, strats=False, cheat=False, *args, **kwargs)
安排一个计时器以调用notify_timer。参数：

参数	
when	可以是datetime.time实例（见下文的tzdata），bt.timer.SESSION_START以参考会话开始，bt.timer.SESSION_END以参考会话结束。
offset	必须是datetime.timedelta实例，用于偏移值when。在与SESSION_START和SESSION_END组合使用时具有有意义的用途，以指示例如在会话开始后15分钟调用计时器。
repeat	必须是datetime.timedelta实例，表示在第一次调用后，是否在同一会话内按计划的重复增量安排进一步的调用。
weekdays	一个排序的可迭代对象，包含表示计时器可以实际调用的天数（iso代码，周一是1，周日是7）。如果未指定，计时器将在所有天都有效。
weekcarry	默认：False，如果为True并且未看到工作日（例如：交易假期），计时器将在第二天执行（即使在新的一周内）。
monthdays	一个排序的可迭代对象，包含表示每月应执行计时器的天数。例如总是在每月的15日。如果未指定，计时器将在所有天都有效。
monthcarry	默认：True，如果未看到该天（周末、交易假期），计时器将在下一个可用日执行。
allow	默认：None，一个回调，接收一个datetime.date实例，如果日期被允许用于计时器则返回True，否则返回False。
tzdata	可以是None（默认）、一个pytz实例或一个数据源实例。
None：按面值解释when（这意味着将其处理为UTC，即使不是）。
- pytz实例：when将被解释为在所选时区本地时间指定。
数据源实例：when将被解释为在数据源实例的tz参数指定的本地时间。
注意，如果when是SESSION_START或SESSION_END并且tzdata为None，将使用系统中的第一个数据源（即self.data0）作为参考，以找出会话时间。
strats	默认：False，也调用策略的notify_timer。
cheat	默认：False）如果为True，将在经纪人有机会评估订单之前调用计时器。这打开了发布基于开盘价的订单的机会，例如在会话开始前。
*args	将传递给notify_timer的任何额外args。
**kwargs	将传递给notify_timer的任何额外kwargs。返回值：创建的计时器。
notify_timer(timer, when, *args, **kwargs)
接收计时器通知，其中timer是由 add_timer 返回的计时器，when是调用时间。args和kwargs是传递给add_timer的任何附加参数。实际的when时间可能稍后，但系统可能无法提前调用计时器。此值是计时器值，而不是系统时间。

add_order_history(orders, notify=True)
将订单历史直接添加到经纪人以进行性能评估。

orders：是一个可迭代对象（例如：列表、元组、迭代器、生成器），其中每个元素也是一个具有以下子元素（2种格式可能）的可迭代对象（具有长度）：[datetime, size, price]或[datetime, size, price, data]，注意，必须按日期时间升序排序（或生成排序的元素）。

具体说明如下：

参数	描述
datetime	是Python的日期/日期时间实例或格式为YYYY-MM-DD[THH:MM:SS[.us]]的字符串，其中括号内的元素是可选的。
size	是一个整数（正数表示买入，负数表示卖出）。
price	是一个浮点数/整数。
data	如果存在，可以取以下任何值：
None - 将使用第一个数据源作为目标。
integer - 将使用该索引（在Cerebro中插入顺序）的数据。
string - 将使用具有该名称的数据，例如使用cerebro.adddata(data, name=value)分配的名称。
notify（默认：True）：如果为True，系统中插入的第一个策略将收到根据每个订单的信息创建的人工订单通知。

注意

描述中隐含的是添加作为订单目标的数据源。例如，这是分析器（如跟踪回报）的必要条件。
##############################################################################################################################
内存优化#
Backtrader 的开发是在拥有大量RAM的机器上进行的，加上绘图的可视化反馈非常有用，几乎是必需品，这使得设计决策变得容易：将所有内容保存在内存中。但这一决定有一些缺点：

使用array.array进行数据存储时，当某些边界被超出时，需要分配和移动数据。
内存较少的机器可能会受到影响。
连接到一个可能在线数周/数月、提供数千秒/分钟分辨率tick的实时数据源。
后者比前者更重要，因为backtrader做出了另一个设计决策：

保持纯Python以便在需要时能够在嵌入式系统中运行。
未来的一个场景可能是backtrader连接到第二台提供实时数据的机器，而backtrader本身运行在Raspberry Pi甚至更有限的设备上，如ADSL路由器（带有Freetz映像的AVM Frit!Box 7490）。

因此，需要backtrader支持动态内存方案。现在可以使用以下语义实例化或运行Cerebro：

exactbars 默认值为 False，每个存储在线中的值都保存在内存中。可能的值：

True或1：所有“线”对象将内存使用减少到自动计算的最小周期。

如果 SMA 的周期为30，则底层将始终有一个30条的运行缓冲区，以允许计算 SMA。
此设置将停用预加载和runonce。
使用此设置还将停用绘图。
-1：在策略级别的数据源和指标/操作将保留所有数据在内存中。

如 RSI 内部使用指标UpDay进行计算。此子指标将不保留所有数据在内存中。
这允许保持绘图和预加载活动。
runonce将被停用。
-2：作为策略属性的数据源和指标将保留所有点在内存中。

如 RSI 内部使用指标UpDay进行计算。此子指标将不保留所有数据在内存中。
如果在__init__中定义了a = self.data.close - self.data.high，那么a将不保留所有数据在内存中。
这允许保持绘图和预加载活动。
runonce将被停用。
正如往常，示例胜过千言万语。一个示例脚本展示了差异。它针对1996年至2015年的雅虎每日数据运行，共计4965天。

注意：这是一个小样本。交易14小时的EuroStoxx50期货在一个月内将生成约18000个1分钟条。

首先执行脚本，查看在不请求内存节省时使用了多少内存位置：

$ ./memory-savings.py --save 0
Total memory cells used: 506430
对于级别1（完全节省）：

$ ./memory-savings.py --save 1
Total memory cells used: 2041
从 50 万降到 2041。确实如此。

系统中的每个“线”对象使用collections.deque作为缓冲区（而不是array.array），并且长度限制为所需操作的绝对最小值。

假设，使用周期为30的简单移动平均线的策略。在这种情况下，将进行以下调整：

数据源将有一个30位置的缓冲区，这是 SMA 生成下一个值所需的数量。
SMA 将有一个位置的缓冲区，因为除非其他指标需要（依赖于 SMA），否则没必要保留更大缓冲区。
注意：此模式最吸引人且可能最重要的特点是，整个脚本生命周期内使用的内存量保持不变。

无论数据源的大小如何。如如果长时间连接实时数据源，这将非常有用。

但请注意：

绘图不可用。
还有其他内存消耗源，如策略生成的订单，随着时间的推移会积累。
此模式只能与runonce=False一起在cerebro中使用。这对于实时数据源也是强制性的，但在简单回测的情况下，这比runonce=True慢。毫无疑问，从某个折衷点来看，内存管理比逐步执行回测更昂贵，但这只能由平台的终端用户根据具体情况判断。
现在是负级别。这些旨在在保持绘图可用的同时仍节省大量内存。第一个级别-1：

$ ./memory-savings.py --save -1
Total memory cells used: 184623
在这种情况下，1 级指标（策略中声明的那些）保留其完整长度缓冲区。但如果这些指标依赖于其他指标（这是情况），则子对象将长度受限。在这种情况下，我们从：

506430内存位置降至 -> 184623
超过50%的节省。

注意：当然，array.array对象已被collections.deque替换，后者在内存方面更昂贵，虽然在操作方面更快。但collections.deque对象相当小，节省的内存位置接近大致计算的内存位置使用。

现在是级别-2，这也是为了节省在策略级别声明且标记为不绘图的指标：

$ ./memory-savings.py --save -2
Total memory cells used: 174695
现在并没有节省多少。这是因为只有一个指标被标记为不绘图：TestInd().plotinfo.plot = False。

让我们看看最后一个示例的绘图：

$ ./memory-savings.py --save -2 --plot
Total memory cells used: 174695


对于感兴趣的读者，示例脚本可以详细分析遍历指标层次结构的每个“线”对象。启用绘图运行（在-1保存）：

$ ./memory-savings.py --save -1 --lendetails
-- Evaluating Datas
---- Data 0 Total Cells 34755 - Cells per Line 4965
-- Evaluating Indicators
---- Indicator 1.0 Average Total Cells 30 - Cells per line 30
---- SubIndicators Total Cells 1
---- Indicator 1.1 _LineDelay Total Cells 1 - Cells per line 1
---- SubIndicators Total Cells 1
...
---- Indicator 0.5 TestInd Total Cells 9930 - Cells per line 4965
---- SubIndicators Total Cells 0
-- Evaluating Observers
---- Observer 0 Total Cells 9930 - Cells per Line 4965
---- Observer 1 Total Cells 9930 - Cells per Line 4965
---- Observer 2 Total Cells 9930 - Cells per Line 4965
Total memory cells used: 184623
相同的，但启用最大节省（1）：

$ ./memory-savings.py --save 1 --lendetails
-- Evaluating Datas
---- Data 0 Total Cells 266 - Cells per Line 38
-- Evaluating Indicators
---- Indicator 1.0 Average Total Cells 30 - Cells per line 30
---- SubIndicators Total Cells 1
...
---- Indicator 0.5 TestInd Total Cells 2 - Cells per line 1
---- SubIndicators Total Cells 0
-- Evaluating Observers
---- Observer 0 Total Cells 2 - Cells per Line 1
---- Observer 1 Total Cells 2 - Cells per Line 1
---- Observer 2 Total Cells 2 - Cells per Line 1
第二个输出立即显示数据源中的线已被限制为38个内存位置，而不是4965个（完整数据源长度）。

并且在可能的情况下，指标和观察者已被限制为1个，如输出的最后几行所示。

脚本代码和使用#
在backtrader的源代码中提供了示例。使用方法：

$ ./memory-savings.py --help
usage: memory-savings.py [-h] [--data DATA] [--save SAVE] [--datalines]
                         [--lendetails] [--plot]

Check Memory Savings

optional arguments:
  -h, --help    show this help message and exit
  --data DATA   Data to be read in (default: ../../datas/yhoo-1996-2015.txt)
  --save SAVE   Memory saving level [1, 0, -1, -2] (default: 0)
  --datalines   Print data lines (default: False)
  --lendetails  Print individual items memory usage (default: False)
  --plot        Plot the result (default: False)
代码：

from __future__ import (absolute_import

, division, print_function,
                        unicode_literals)

import argparse
import sys

import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicators as btind
import backtrader.utils.flushfile


class TestInd(bt.Indicator):
    lines = ('a', 'b')

    def __init__(self):
        self.lines.a = b = self.data.close - self.data.high
        self.lines.b = btind.SMA(b, period=20)


class St(bt.Strategy):
    params = (
        ('datalines', False),
        ('lendetails', False),
    )

    def __init__(self):
        btind.SMA()
        btind.Stochastic()
        btind.RSI()
        btind.MACD()
        btind.CCI()
        TestInd().plotinfo.plot = False

    def next(self):
        if self.p.datalines:
            txt = ','.join(
                ['%04d' % len(self),
                 '%04d' % len(self.data0),
                 self.data.datetime.date(0).isoformat()]
            )

            print(txt)

    def loglendetails(self, msg):
        if self.p.lendetails:
            print(msg)

    def stop(self):
        super(St, self).stop()

        tlen = 0
        self.loglendetails('-- Evaluating Datas')
        for i, data in enumerate(self.datas):
            tdata = 0
            for line in data.lines:
                tdata += len(line.array)
                tline = len(line.array)

            tlen += tdata
            logtxt = '---- Data {} Total Cells {} - Cells per Line {}'
            self.loglendetails(logtxt.format(i, tdata, tline))

        self.loglendetails('-- Evaluating Indicators')
        for i, ind in enumerate(self.getindicators()):
            tlen += self.rindicator(ind, i, 0)

        self.loglendetails('-- Evaluating Observers')
        for i, obs in enumerate(self.getobservers()):
            tobs = 0
            for line in obs.lines:
                tobs += len(line.array)
                tline = len(line.array)

            tlen += tdata
            logtxt = '---- Observer {} Total Cells {} - Cells per Line {}'
            self.loglendetails(logtxt.format(i, tobs, tline))

        print('Total memory cells used: {}'.format(tlen))

    def rindicator(self, ind, i, deep):
        tind = 0
        for line in ind.lines:
            tind += len(line.array)
            tline = len(line.array)

        thisind = tind

        tsub = 0
        for j, sind in enumerate(ind.getindicators()):
            tsub += self.rindicator(sind, j, deep + 1)

        iname = ind.__class__.__name__.split('.')[-1]

        logtxt = '---- Indicator {}.{} {} Total Cells {} - Cells per line {}'
        self.loglendetails(logtxt.format(deep, i, iname, tind, tline))
        logtxt = '---- SubIndicators Total Cells {}'
        self.loglendetails(logtxt.format(deep, i, iname, tsub))

        return tind + tsub


def runstrat():
    args = parse_args()

    cerebro = bt.Cerebro()
    data = btfeeds.YahooFinanceCSVData(dataname=args.data)
    cerebro.adddata(data)
    cerebro.addstrategy(
        St, datalines=args.datalines, lendetails=args.lendetails)

    cerebro.run(runonce=False, exactbars=args.save)
    if args.plot:
        cerebro.plot(style='bar')


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Check Memory Savings')

    parser.add_argument('--data', required=False,
                        default='../../datas/yhoo-1996-2015.txt',
                        help='Data to be read in')

    parser.add_argument('--save', required=False, type=int, default=0,
                        help=('Memory saving level [1, 0, -1, -2]'))

    parser.add_argument('--datalines', required=False, action='store_true',
                        help=('Print data lines'))

    parser.add_argument('--lendetails', required=False, action='store_true',
                        help=('Print individual items memory usage'))

    parser.add_argument('--plot', required=False, action='store_true',
                        help=('Plot the result'))

    return parser.parse_args()


if __name__ == '__main__':
    runstrat()

##################################################################################################################
优化改进#
Backtrader 通过引入两个新的 Cerebro 参数，优化了在多进程环境下管理数据源和结果的方式。

参数说明：

参数名	默认值	描述
optdatas	True	如果为True并进行优化（系统可以预加载并使用runonce），则数据预加载将仅在主进程中进行一次，以节省时间和资源。
optreturn	True	如果为True，优化结果将不是完整的策略对象（包括所有数据、指标、观察者等），而是带有以下属性的对象（与策略中相同）：
- params（或p）：策略执行时的参数
- analyzers：策略执行的分析器
通常，我们只需要查看策略使用的参数的最终表现（如收益率）。如想查看运行过程中的详细数据（如每个时间点的指标值），请关闭此选项。

数据源管理#
在优化场景中，Cerebro 参数可能的组合是：

preload=True（默认），数据源将在运行任何回测代码前完成预加载：
runonce=True（默认），指标将在紧密的for循环中批量计算，而不是逐步计算。
如果两个条件都为True且optdatas=True，则数据源将在生成新子进程之前在主进程中预加载（这些子进程负责执行回测）

结果管理#
在优化场景中，当评估每个策略运行的不同参数时，最重要的两个因素是：

strategy.params（或strategy.p）

回测使用的实际参数集

strategy.analyzers

提供策略实际表现评估的对象。例如：SharpeRatio_A（年化夏普比率）

当optreturn=True时，不会返回完整的策略实例，而是创建占位符对象，这些对象携带上述两个属性以进行评估。

这避免了传回大量生成的数据，例如回测期间指标生成的值。

如果希望返回完整的策略对象，只需在Cerebro实例化或进行cerebro.run时设置optreturn=False。

一些测试运行#
backtrader源代码中的优化示例已扩展，添加了对optdatas和optreturn的控制（实际上是禁用它们）。

单核心运行#
作为参考，当将CPU数量限制为1且不使用多进程模块时会发生什么：

$ ./optimization.py --maxcpus 1
==================================================
**************************************************
--------------------------------------------------
OrderedDict([(u'smaperiod', 10), (u'macdperiod1', 12), (u'macdperiod2', 26), (u'macdperiod3', 9)])
**************************************************
--------------------------------------------------
OrderedDict([(u'smaperiod', 10), (u'macdperiod1', 13), (u'macdperiod2', 26), (u'macdperiod3', 9)])
...
...
OrderedDict([(u'smaperiod', 29), (u'macdperiod1', 19), (u'macdperiod2', 29), (u'macdperiod3', 14)])
==================================================
Time used: 184.922727833
多核心运行#
在不限制CPU数量的情况下，Python多进程模块将尝试使用所有CPU。禁用optdatas和optreturn

optdatas和optreturn都启用

默认行为：

$ ./optimization.py
...
...
...
==================================================
Time used: 56.5889185394
通过多核和数据源及结果改进，总时间从184.92秒减少到56.58秒。

请注意，示例使用了252条数据，并且指标仅生成长度为252点的值。这只是一个例子。

真正的问题是这种改进有多少是由于新行为。

optreturn禁用：将完整的策略对象传回调用者：

$ ./optimization.py --no-optreturn
...
...
...
==================================================
Time used: 67.056914007
执行时间增加了18.50%（或15.62%的速度提升）。

optdatas禁用：每个子进程被迫加载其自己的数据源值：

$ ./optimization.py --no-optdatas
...
...
...
==================================================
Time used: 72.7238112637
执行时间增加了28.52%（或22.19%的速度提升）。

两者都禁用：仍然使用多核，但使用旧的未改进行为：

$ ./optimization.py --no-optdatas --no-optreturn
...
...
...
==================================================
Time used: 83.6246643786
执行时间增加了47.79%（或32.34%的速度提升）。

这表明使用多个核心是时间改进的主要贡献因素。

注意：这些执行是在配备i7-4710HQ（4核/8逻辑）和16 GB RAM的笔记本电脑上进行的，操作系统为Windows 10 64位。在其他条件下可能会有所不同。

总结#
在优化过程中时间减少的最大因素是使用多个核心。

使用optdatas和optreturn的示例运行显示了大约22.19%和15.62%的速度提升（在测试中两者一起提高了32.34%）。

示例使用#
$ ./optimization.py --help
usage: optimization.py [-h] [--data DATA] [--fromdate FROMDATE]
                       [--todate TODATE] [--maxcpus MAXCPUS] [--no-runonce]
                       [--exactbars EXACTBARS] [--no-optdatas]
                       [--no-optreturn] [--ma_low MA_LOW] [--ma_high MA_HIGH]
                       [--m1_low M1_LOW] [--m1_high M1_HIGH] [--m2_low M2_LOW]
                       [--m2_high M2_HIGH] [--m3_low M3_LOW]
                       [--m3_high M3_HIGH]

Optimization

optional arguments:
  -h, --help            show this help message and exit
  --data DATA, -d DATA  data to add to the system
  --fromdate FROMDATE, -f FROMDATE
                        Starting date in YYYY-MM-DD format
  --todate TODATE, -t TODATE
                        Starting date in YYYY-MM-DD format
  --maxcpus MAXCPUS, -m MAXCPUS
                        Number of CPUs to use in the optimization
                          - 0 (default): use all available CPUs
                          - 1 -> n: use as many as specified
  --no-runonce          Run in next mode
  --exactbars EXACTBARS
                        Use the specified exactbars still compatible with preload
                          0 No memory savings
                          -1 Moderate memory savings
                          -2 Less moderate memory savings
  --no-optdatas         Do not optimize data preloading in optimization
  --no-optreturn        Do not optimize the returned values to save time
  --ma_low MA_LOW       SMA range low to optimize
  --ma_high MA_HIGH     SMA range high to optimize
  --m1_low M1_LOW       MACD Fast MA range low to optimize
  --m1_high M1_HIGH     MACD Fast MA range high to optimize
  --m2_low M2_LOW       MACD Slow MA range low to optimize
  --m2_high M2_HIGH     MACD Slow MA range high to optimize
  --m3_low M3_LOW       MACD Signal range low to optimize
  --m3_high M3_HIGH     MACD Signal range high to optimize
(C) 2015-2024 Daniel Rodriguez
#############################################################################################################################
异常#
设计目标之一是尽早退出并让用户完全透明地了解错误发生的情况。目的是强制自己编写在异常情况下会中断的代码，并强制重新审视受影响的部分。

但现在是时候了，某些异常可能会慢慢添加到平台中。

继承层次结构#
所有异常的基类是 BacktraderError（直接继承自 Exception）。

位置#
在 errors 模块内，可以通过以下方式访问：

import backtrader as bt

class Strategy(bt.Strategy):

    def __init__(self):
        if something_goes_wrong():
            raise bt.errors.StrategySkipError
或者直接从 backtrader 访问：

import backtrader as bt

class Strategy(bt.Strategy):

    def __init__(self):
        if something_goes_wrong():
            raise bt.StrategySkipError
异常#
StrategySkipError，请求平台跳过该策略的回测。应在实例的初始化（__init__）阶段引发。
######################################################################################
Writer#
Writer类负责将以下内容写入流：

数据源、策略、指标和观察者的CSV流。可以通过每个对象的csv属性控制哪些对象实际进入CSV流（数据源和观察者默认为True，指标默认为False）。

属性摘要：

数据源
策略（线条和参数）
指标/观察者（线条和参数）
分析器（参数和分析结果）
系统中定义了一个名为WriterFile的Writer，可以通过以下方式添加：

设置Cerebro的writer参数为True，将实例化一个标准的WriterFile
调用Cerebro.addwriter(writerclass, **kwargs)，在回测执行期间，使用给定的kwargs实例化writerclass
由于标准的WriterFile默认不输出CSV，以下调用可以处理这一点：

cerebro.addwriter(bt.WriterFile, csv=True)
参考#
class backtrader.WriterFile()#
系统范围内的Writer类。

可以通过以下参数进行参数化：

参数名	默认	说明
out	sys.stdout	写入的输出流，如果传递的是字符串，将使用参数内容作为文件名。
close_out	False	如果 out 是一个流，是否需要由Writer显式关闭。
csv	False	在执行过程中，是否将数据源、策略、观察者和指标的CSV流写入输出流。可以通过每个对象的csv属性控制哪些对象实际进入CSV流（数据源和观察者默认为True，指标默认为False）。
csv_filternan	True	CSV流中清除nan值（用空字段替换）。
csv_counter	True	是否应保持并输出实际输出行的计数器。
indent	2	每个级别的缩进空格数。
separators	‘=’, ‘-’, ‘+’, ‘*’, ‘.’, ‘~’, ‘"’, ‘^’, ‘#’	用于分隔部分/子部分的行分隔符字符。
seplen	79	包括缩进在内的行分隔符的总长度。
rounding	None	将浮点数舍入到的小数位数。如果为None，则不执行舍入。

26 36数据源.txt ##################################################
文件路径: 36数据源.txt
================================================================================

数据源#
Backtrader 提供了一组数据源解析器（在撰写本文时都是基于 CSV 的）以便从不同来源加载数据。

Yahoo（在线或已保存到文件）
VisualChart（参见 www.visualchart.com）
Backtrader CSV（自定义格式用于测试）
通用 CSV 支持
从快速入门指南中可以清楚地看到，您可以将数据源添加到 Cerebro 实例中。这些数据源稍后将在策略中可用：

self.datas 数组（按插入顺序）
数组对象的别名：
self.data 和 self.data0 指向第一个元素
self.dataX 指向数组中索引为 X 的元素
以下是插入方式的快速提醒：

import backtrader as bt
import backtrader.feeds as btfeeds

data = btfeeds.YahooFinanceCSVData(dataname='wheremydatacsvis.csv')

cerebro = bt.Cerebro()
cerebro.adddata(data)  # 可以传递一个 'name' 参数用于绘图
数据源通用参数#
这个数据源可以直接从 Yahoo 下载数据并将其输入系统。

Backtrader 数据源常用参数：

参数名	默认值	描述
dataname	None	必须提供。其含义因数据源类型而异，例如文件路径、股票代码等。
name	''	用于绘图时的装饰性名称。如果未指定，可能会从 dataname 派生（例如：文件路径的最后一部分）。
fromdate	mindate	Python datetime 对象，表示应忽略此日期之前的任何数据。
todate	maxdate	Python datetime 对象，表示应忽略此日期之后的任何数据。
timeframe	TimeFrame.Days	时间框架。可能的值包括：Ticks、Seconds、Minutes、Days、Weeks、Months 和 Years。
compression	1	每个实际条形图的条形数。仅在数据重采样/重放中有效。
sessionstart	None	数据会话的开始时间。可用于重采样等目的。
sessionend	None	数据会话的结束时间。可用于重采样等目的。
CSV 数据源通用参数#
参数（除了通用参数外）：

参数名	默认值	描述
headers	True	指示传递的数据是否具有初始标题行。
separator	','	分隔符，用于标记 CSV 每行中的各个字段。
GenericCSVData#
此类公开了一个通用接口，允许解析几乎所有的 CSV 文件格式。

根据参数定义的顺序和字段存在情况解析 CSV 文件。

特定参数（或特定含义）：

参数名	默认值	描述
dataname	必须提供	要解析的文件名或类似文件的对象。
datetime	0	包含日期（或日期时间）字段的列索引。
time	-1	如果与日期时间字段分开，则包含时间字段的列索引（-1 表示不存在）。
open	1	包含开盘价字段的列索引。
high	2	包含最高价字段的列索引。
low	3	包含最低价字段的列索引。
close	4	包含收盘价字段的列索引。
volume	5	包含成交量字段的列索引。
openinterest	6	包含未平仓合约数字段的列索引。
nullvalue	float('NaN')	如果缺少应有的值（CSV 字段为空），将使用的值。
dtformat	'%Y-%m-%d %H:%M:%S'	用于解析日期时间 CSV 字段的格式。
tmformat	'%H:%M:%S'	如果存在，用于解析时间 CSV 字段的格式（默认情况下时间 CSV 字段不存在）。
这些参数允许用户根据其 CSV 文件的结构自定义数据解析方式，以便正确加载数据进行回测。

示例使用#
满足以下要求的示例用法：

限制输入年份为 2000
HLOC 顺序而不是 OHLC
将缺失值替换为零（0.0）
提供日线数据，日期时间只是格式为 YYYY-MM-DD 的日期
没有 openinterest 列
代码如下：

import datetime
import backtrader as bt
import backtrader.feeds as btfeeds

...
...

data = btfeeds.GenericCSVData(
    dataname='mydata.csv',

    fromdate=datetime.datetime(2000, 1, 1),
    todate=datetime.datetime(2000, 12, 31),

    nullvalue=0.0,

    dtformat=('%Y-%m-%d'),

    datetime=0,
    high=1,
    low=2,
    open=3,
    close=4,
    volume=5,
    openinterest=-1
)
...
略微修改后的要求：

限制输入年份为 2000
HLOC 顺序而不是 OHLC
将缺失值替换为零（0.0）
提供日内数据，带有单独的日期和时间列
日期格式为 YYYY-MM-DD
时间格式为 HH.MM.SS（而不是通常的 HH:MM:SS）
没有 openinterest 列
代码如下：

import datetime
import backtrader as bt
import backtrader.feeds as btfeeds

...
...

data = btfeeds.GenericCSVData(
    dataname='mydata.csv',

    fromdate=datetime.datetime(2000, 1, 1),
    todate=datetime.datetime(2000, 12, 31),

    nullvalue=0.0,

    dtformat=('%Y-%m-%d'),
    tmformat=('%H.%M.%S'),

    datetime=0,
    time=1,
    high=2,
    low=3,
    open=4,
    close=5,
    volume=6,
    openinterest=-1
)
这也可以通过子类化永久保存：

import datetime
import backtrader.feeds as btfeeds

class MyHLOC(btfeeds.GenericCSVData):

  params = (
    ('fromdate', datetime.datetime(2000, 1, 1)),
    ('todate', datetime.datetime(2000, 12, 31)),
    ('nullvalue', 0.0),
    ('dtformat', ('%Y-%m-%d')),
    ('tmformat', ('%H.%M.%S')),

    ('datetime', 0),
    ('time', 1),
    ('high', 2),
    ('low', 3),
    ('open', 4),
    ('close', 5),
    ('volume', 6),
    ('openinterest', -1)
)
现在可以通过提供 dataname 重用此新类：

data = btfeeds.MyHLOC(dataname='mydata.csv')

##################################################################################
扩展数据源#
用户是否可以轻松扩展现有机制，以添加额外的信息，将其与现有的价格信息（如开盘价、高价等）一起传递？

据我了解，答案是：可以。

一个数据源，正在解析为 CSV 格式
使用 GenericCSVData 加载信息
这种通用 CSV 支持是为了响应 Issue #6 开发的
一个额外的字段，显然包含 P/E 信息，需要与解析的 CSV 数据一起传递
让我们基于 CSV 数据源开发和 GenericCSVData 示例帖子构建。

步骤：#
假设 P/E 信息已设置在被解析的 CSV 数据中
使用 GenericCSVData 作为基类
使用 pe 扩展现有的行（开盘价/最高价/最低价/收盘价/成交量/持仓兴趣）
添加一个参数，让调用者确定 P/E 信息的列位置
结果如下：

from backtrader.feeds import GenericCSVData

class GenericCSV_PE(GenericCSVData):

    # 添加 'pe' 行到从基类继承的行中
    lines = ('pe',)

    # GenericCSVData 中的 openinterest 索引为 7 ... 添加 1
    # 将参数添加到从基类继承的参数中
    params = (('pe', 8),)
这样工作就完成了…

稍后在策略中使用此数据源时：

import backtrader as bt

....

class MyStrategy(bt.Strategy):

    ...

    def next(self):

        if self.data.close > 2000 and self.data.pe < 12:
            # TORA TORA TORA --- 退出市场
            self.sell(stake=1000000, price=0.01, exectype=Order.Limit)
    ...
绘制额外的 P/E 行#
显然，数据源中没有自动绘制支持这个额外的行。

最好的替代方法是在该行上进行简单移动平均并在单独的轴上绘制：

import backtrader as bt
import backtrader.indicators as btind

....

class MyStrategy(bt.Strategy):

    def __init__(self):

        # 指标自动注册，即使在类中没有保留明显的引用也会绘制
        btind.SMA(self.data.pe, period=1, subplot=False)

    ...

    def next(self):

        if self.data.close > 2000 and self.data.pe < 12:
            # TORA TORA TORA --- 退出市场
            self.sell(stake=1000000, price=0.01, exectype=Order.Limit)
    ...
#################################################################################
CSV 数据源开发#
Backtrader 已经提供了一些通用 CSV 数据源和特定的 CSV 数据源。

GenericCSVData
VisualChartCSVData
YahooFinanceData（用于在线下载）
YahooFinanceCSVData（用于已下载的数据）
BacktraderCSVData（内部使用…用于测试目的，但也可以使用）
即使如此，最终用户可能仍希望开发对特定 CSV 数据源的支持。

通常的格言是：“说起来容易做起来难”。实际上，结构旨在使其变得简单。

步骤#
从 backtrader.CSVDataBase 继承
根据需要定义任何参数
在 start 方法中进行任何初始化
在 stop 方法中进行任何清理
定义一个 _loadline 方法，其中实际工作发生。此方法接收一个参数：linetokens。
顾名思义，这包含根据分隔符参数（从基类继承）拆分当前行后的标记。

如果在完成其工作后有新数据……填充相应的行并返回 True。

如果没有可用的数据，因此解析已结束：返回 False。

如果后台代码发现没有更多行需要解析，则可能不需要返回 False。

已考虑的事项：

打开文件（或接收类似文件的对象）
跳过标头行（如果指示存在）
读取行
标记行
预加载支持（将整个数据源一次性加载到内存中）
通常一个示例胜过千言万语。让我们使用 BacktraderCSVData 中定义的内部 CSV 解析代码的简化版本。这个版本不需要初始化或清理（例如，这可能是打开一个套接字并稍后关闭它）。

注意：

backtrader 数据源包含通常的行业标准源，这些源是要填充的。即：

datetime
open
high
low
close
volume
openinterest
如果您的策略/算法或简单数据浏览只需要，例如收盘价，您可以不触碰其他字段（每次迭代会自动用 float('NaN') 值填充它们，然后用户代码有机会进行任何操作）。

在此示例中，仅支持每日格式：

import itertools
import backtrader as bt

class MyCSVData(bt.CSVDataBase):

    def start(self):
        # 对于此数据源类型无需做任何操作
        pass

    def stop(self):
        # 对于此数据源类型无需做任何操作
        pass

    def _loadline(self, linetokens):
        i = itertools.count(0)

        dttxt = linetokens[next(i)]
        # 格式为 YYYY-MM-DD
        y = int(dttxt[0:4])
        m = int(dttxt[5:7])
        d = int(dttxt[8:10])

        dt = datetime.datetime(y, m, d)
        dtnum = date2num(dt)

        self.lines.datetime[0] = dtnum
        self.lines.open[0] = float(linetokens[next(i)])
        self.lines.high[0] = float(linetokens[next(i)])
        self.lines.low[0] = float(linetokens[next(i)])
        self.lines.close[0] = float(linetokens[next(i)])
        self.lines.volume[0] = float(linetokens[next(i)])
        self.lines.openinterest[0] = float(linetokens[next(i)])

        return True
代码假设所有字段都到位且可转换为浮点数，除了日期时间，它具有固定的 YYYY-MM-DD 格式，可以不使用 datetime.datetime.strptime 进行解析。

通过添加一些代码行来处理空值和日期格式解析，可以满足更复杂的需求。GenericCSVData 就是这样做的。

警告#
使用现有的 GenericCSVData 和继承，可以实现很多格式支持。

让我们添加对 Sierra Chart 每日格式的支持（始终以 CSV 格式存储）。

定义（通过查看一个 ‘.dly’ 数据文件）：

字段：Date, Open, High, Low, Close, Volume, OpenInterest

行业标准字段以及 GenericCSVData 已支持的字段，顺序相同（也是行业标准）

分隔符：,

日期格式：YYYY/MM/DD

一个用于这些文件的解析器：

class SierraChartCSVData(backtrader.feeds.GenericCSVData):

    params = (('dtformat', '%Y/%m/%d'),)
参数定义只是重新定义了基类中的一个现有参数。在这种情况下，只需要更改日期格式字符串。

完成#
Sierra Chart 的解析器已经完成。

下面是 GenericCSVData 的参数定义作为提醒：

class GenericCSVData(feed.CSVDataBase):
    params = (
        ('nullvalue', float('NaN')),
        ('dtformat', '%Y-%m-%d %H:%M:%S'),
        ('tmformat', '%H:%M:%S'),

        ('datetime', 0),
        ('time', -1),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close', 4),
        ('volume', 5),
        ('openinterest', 6),
    )
###############################################################################################################
开发 Binary 据源#
注意：示例中使用的 Binary 文件 goog.fd 属于 VisualChart，不能与 backtrader 一起分发。

对于那些有兴趣直接使用 Binary 文件的人，可以免费下载 VisualChart。

CSV 数据源开发展示了如何添加新的基于 CSV 的数据源。现有的基类 CSVDataBase 提供了框架，减轻了子类的大部分工作，在大多数情况下，它们可以简单地执行：

def _loadline(self, linetokens):

  # 在这里解析 linetokens 并将它们放入 self.lines.close, self.lines.high 等中

  return True # 如果数据已解析，否则返回 False
基类负责参数、初始化、打开文件、读取行、将行拆分为标记以及其他事项，例如跳过不符合日期范围（fromdate，todate）的行，这些行可能由最终用户定义。

开发非 CSV 数据源遵循相同的模式，而无需深入到已拆分的行标记。

需要做的事情：#
从 backtrader.feed.DataBase 派生
添加任何需要的参数
如果需要初始化，重写 __init__(self) 和/或 start(self)
如果需要清理代码，重写 stop(self)
工作发生在必须始终重写的方法 _load(self) 内
让我们看看 backtrader.feed.DataBase 已经提供的参数：

from backtrader.utils.py3 import with_metaclass

...
...

class DataBase(with_metaclass(MetaDataBase, dataseries.OHLCDateTime)):

    params = (('dataname', None),
        ('fromdate', datetime.datetime.min),
        ('todate', datetime.datetime.max),
        ('name', ''),
        ('compression', 1),
        ('timeframe', TimeFrame.Days),
        ('sessionend', None))
这些参数具有以下含义：

dataname：允许数据源识别如何获取数据。在 CSVDataBase 的情况下，此参数表示文件路径或已存在的类似文件的对象。
fromdate 和 todate：定义传递给策略的日期范围。数据源提供的任何超出此范围的值都将被忽略。
name：用于绘图目的的装饰名称。
timeframe：表示时间工作参考。潜在值：Ticks, Seconds, Minutes, Days, Weeks, Months 和 Years。
compression（默认值：1）：每条实际条的条数。信息性。仅在数据重采样/重放中有效。
sessionend：如果传递（datetime.time 对象），将添加到数据源日期时间行，允许识别会话结束。
示例二进制数据源#
backtrader 已经定义了一个 CSV 数据源（VChartCSVData）用于 VisualChart 的导出数据，但也可以直接读取二进制数据文件。

让我们来实现（完整的数据源代码可以在文末找到）。

初始化#
二进制 VisualChart 数据文件可以包含每日数据（.fd 扩展名）或日内数据（.min 扩展名）。这里使用参数 timeframe 来区分读取的文件类型。

在 __init__ 中，设置每种类型不同的常量。

def __init__(self):
    super(VChartData, self).__init__()

    # 使用 informative "timeframe" 参数来理解传递的 "dataname"
    # 是指日内还是每日数据源
    if self.p.timeframe >= TimeFrame.Days:
        self.barsize = 28
        self.dtsize = 1
        self.barfmt = 'IffffII'
    else:
        self.dtsize = 2
        self.barsize = 32
        self.barfmt = 'IIffffII'
开始#
数据源将在回测开始时启动（在优化期间实际上可以启动多次）。

在 start 方法中，除非传递了类似文件的对象，否则二进制文件会被打开。

def start(self):
    # 数据源必须启动...打开文件（或查看是否已打开）
    self.f = None
    if hasattr(self.p.dataname, 'read'):
        # 传入了文件（例如：来自 GUI）
        self.f = self.p.dataname
    else:
        # 让异常传播
        self.f = open(self.p.dataname, 'rb')
停止#
回测结束时调用。

如果文件已打开，则将其关闭。

def stop(self):
    # 如果有文件，关闭它
    if self.f is not None:
        self.f.close()
        self.f = None
实际加载#
实际工作在 _load 中完成。调用以加载下一组数据，在这种情况下是下一个：datetime、open、high、low、close、volume、openinterest。在 backtrader 中，“实际”时刻对应于索引 0。

将从打开的文件中读取一些字节（由 __init__ 中设置的常量确定），使用 struct 模块解析，如果需要进一步处理（如日期和时间的 divmod 操作），并存储在数据源的行中：datetime、open、high、low、close、volume、openinterest。

如果无法从文件中读取数据，则假定已达到文件末尾（EOF）

返回 False 以指示没有更多数据可用

如果数据已加载并解析：

返回 True 以指示数据集加载成功

def _load(self):
    if self.f is None:
        # 如果没有文件...无法解析
        return False

    # 读取所需数量的二进制数据
    bardata = self.f.read(self.barsize)
    if not bardata:
        # 如果没有读取数据...游戏结束返回 "False"
        return False

    # 使用 struct 解析数据
    bdata = struct.unpack(self.barfmt, bardata)

    # 年份存储为每年 500 天
    y, md = divmod(bdata[0], 500)
    # 月份存储为每月 32 天
    m, d = divmod(md, 32)
    # 将 y, m, d 放入 datetime
    dt = datetime.datetime(y, m, d)

    if self.dtsize > 1:  # 分钟条
        # 每日时间以秒为单位存储
        hhmm, ss = divmod(bdata[1], 60)
        hh, mm = divmod(hhmm, 60)
        # 将时间添加到现有的 datetime
        dt = dt.replace(hour=hh, minute=mm, second=ss)

    self.lines.datetime[0] = date2num(dt)

    # 获取解析的数据的其余部分
    o, h, l, c, v, oi = bdata[self.dtsize:]
    self.lines.open[0] = o
    self.lines.high[0] = h
    self.lines.low[0] = l
    self.lines.close[0] = c
    self.lines.volume[0] = v
    self.lines.openinterest[0] = oi

    # 返回成功
    return True
其他二进制格式#
同样的模型可以应用于任何其他二进制源：

数据库
分层数据存储
在线来源
步骤再次说明：

__init__ -> 实例的任何初始化代码，仅一次
start -> 回测开始时（如果将进行优化则会多次运行）
stop -> 清理，例如关闭数据库连接或打开的套接字
_load -> 查询数据库或在线源以获取下一组数据并将其加载到对象的行中。标准字段为：datetime、open、high、low、close、volume、openinterest
VChartData 测试#
VChartData 从本地 .fd 文件加载 2006 年 Google 的数据。

仅涉及加载数据，因此不需要策略的子类。

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime

import backtrader as bt
from vchart import VChartData


if __name__ == '__main__':
    # 创建 cerebro 实体
    cerebro = bt.Cerebro(stdstats=False)

    # 添加策略
    cerebro.addstrategy(bt.Strategy)

    ###########################################################################
    # 注意：
    # goog.fd 文件属于 VisualChart，不能与 backtrader 一起分发
    #
    # VisualChart 可从 www.visualchart.com 下载
    ###########################################################################
    # 创建数据源
    datapath = '../../datas/goog.fd'
    data = VChartData(
        dataname=datapath,
        fromdate=datetime.datetime(2006, 1, 1),
        todate=datetime.datetime(2006, 12, 31),
        timeframe=bt.TimeFrame.Days
    )

    # 将数据源添加到 Cerebro
    cerebro.adddata(data)

    # 运行所有内容
    cerebro.run()

    # 绘制结果
    cerebro.plot(style='bar')
VChartData 完整代码#
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime
import struct

from backtrader.feed import DataBase
from backtrader import date2num
from backtrader import TimeFrame


class VChartData(DataBase):
    def __init__(self):
        super(VChartData, self).__init__()

        # 使用 informative "timeframe" 参数来理解传递的 "dataname"
        # 是指日内还是每日数据源
        if self.p.timeframe >= TimeFrame.Days:
            self.barsize = 28
            self.dtsize = 1
            self.barfmt = 'IffffII'
        else:
            self.dtsize = 2
            self.barsize = 32
            self.barfmt = 'IIffffII'

    def start(self):
        # 数据源必须启动...打开文件（或查看是否已打开）
        self.f = None
        if hasattr(self.p.dataname, 'read'):
            # 传入了文件（例如：来自 GUI）
            self.f = self.p.dataname
        else:
            # 让异常传播
            self.f = open(self.p.dataname, 'rb')

    def stop(self):
        # 如果有文件，关闭它
        if self.f is not None:
            self.f.close()
            self.f = None

    def _load(self):
        if self.f is None:
            # 如果没有文件...无法解析
            return False

        # 读取所需数量的二进制数据
        bardata = self.f.read(self.barsize)
        if not bardata:
            # 如果没有读取数据...游戏结束返回 "False"
            return False

        # 使用 struct 解析数据
        bdata = struct.unpack(self.barfmt, bardata)

        # 年份存储为每年 500 天
        y, md = divmod(bdata[0], 500)
        # 月份存储为每月 32 天
        m, d = divmod(md, 32)
        # 将 y, m, d 放入 datetime
        dt = datetime.datetime(y, m, d)

        if self.dtsize > 1:  # 分钟条
            # 每日时间以秒为单位存储
            hhmm, ss = divmod(bdata[1], 60)
            hh, mm = divmod(hhmm, 60)
            # 将时间添加到现有的 datetime
            dt = dt.replace(hour=hh, minute=mm, second=ss)

        self.lines.datetime[0] = date2num(dt)

        # 获取解析的数据的其余部分
        o, h, l, c, v, oi = bdata[self.dtsize:]
        self.lines.open[0] = o
        self.lines.high[0] = h
        self.lines.low[0] = l
        self.lines.close[0] = c
        self.lines.volume[0] = v
        self.lines.openinterest[0] = oi

        # 返回成功
        return True
###################################################################################################################
多时间框架策略#
在实际的交易中，我们常需要结合多个时间框架来制定投资决策，如在周级别评估趋势，而在日级别执行入场，或是基于 5 分钟与 60 分钟数据的对比执行交易。在 Backtrader 中要实现这个目标，需要将不同时间框架的数据组合在一起。

本节将介绍如何在 Backtrader 实现多周期交易策略。

基本规则#
Backtrader 原生支持多时间框架的数据组合，只需遵循几个简单的规则。

第一步，最小时间框架的数据必须首先加载。较小时间框架（条数最多的数据）应当首先加载到Cerebro实例中。

第二步，数据必须按日期时间对齐。为了让平台能够正确解析数据并执行策略，必须保证各时间框架的数据时间对齐。

第三步，使用 resampledata 实现较大时间框架的重采样。cerebro.resample 函数能轻松地将较大的时间框架数据添加到策略中。

在这个基础上，就可以在较短和较长时间框架上使用不同的技术指标。要注意，应用于大时间框架的指标产生的信号较少，还有，Backtrader 会考虑大时间框架的最小周期，以确保数据的准确性。

示例：如何使用多个时间框架#
如何在 Backtrader 实现多时间周期呢？大概演示这个步骤吧。

加载数据#
首先，加载较小时间框架的数据。

data = btfeeds.BacktraderCSVData(dataname=datapath)
将数据添加到Cerebro#
将较小时间框架数据都添加到 Cerebro 实例中。

cerebro.adddata(data)
重采样数据#
使用 cerebro.resampledata 将数据重采样到较大的时间框架。

cerebro.resampledata(data, timeframe=tframes[args.timeframe], compression=args.compression)
运行策略#
执行策略并生成结果。

cerebro.run()
示例#
首先，演示每日和每周时间框架。假设我们希望在一个策略中同时使用每日和每周的时间框架。通过命令行指定时间框架为每周，并进行数据重采样：

$ ./multitimeframe-example.py --timeframe weekly --compression 1
此时，程序会加载每日数据，并将其重采样为每周数据。最终输出将包括每周和每日数据的合成图表。

继续用每日时间框架压缩。如果我们希望将每日数据压缩为每两天一条数据，可以使用以下命令：

$ ./multitimeframe-example.py --timeframe daily --compression 2
此时，Backtrader会将每日数据压缩为每两天一条数据，并生成合成图表。

还可以带简单移动平均（SMA）指标。为了展示不同时间框架对策略的影响，可以在策略中使用简单的移动平均线（SMA）指标。SMA将在较小和较大时间框架上应用，并根据它们产生不同的信号。

在较小的时间框架（如每日）上，SMA将在第10个数据点后首次计算出值。
在较大的时间框架（如每周）上，SMA的计算会延迟，可能需要10个周期的时间来产生有效信号。
由于Backtrader的多时间框架支持，较大时间框架会消耗多个较小时间框架的数据条目来计算指标。

在策略中使用 SMA 时，如果数据点来自较大时间框架，nextstart 方法的调用可能会有所延迟。例如，在每周时间框架下，SMA的计算需要10周的数据，而在每个周期内，我们将看到多个“nextstart”调用，因为Backtrader会等待所有数据都齐全时才开始执行策略逻辑。

代码示例#
# 导入必要的库
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse
import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicators as btind

# 创建SMA策略
class SMAStrategy(bt.Strategy):
    params = (
        ('period', 10),  # SMA的周期
        ('onlydaily', False),  # 是否只在每日时间框架上应用
    )

    def __init__(self):
        # 为较小时间框架添加SMA
        self.sma_small_tf = btind.SMA(self.data, period=self.p.period)
        
        # 如果选择不只应用于每日时间框架
        if not self.p.onlydaily:
            # 为较大时间框架（如每周）添加SMA
            self.sma_large_tf = btind.SMA(self.data1, period=self.p.period)

    # nextstart方法，用于输出调试信息
    def nextstart(self):
        print('--------------------------------------------------')
        print('nextstart called with len', len(self))
        print('--------------------------------------------------')
        super(SMAStrategy, self).nextstart()

# 运行策略
def runstrat():
    args = parse_args()

    # 创建Cerebro实例
    cerebro = bt.Cerebro(stdstats=False)

    # 根据用户选择的策略参数加载相应策略
    if not args.indicators:
        cerebro.addstrategy(bt.Strategy)
    else:
        cerebro.addstrategy(SMAStrategy, period=args.period, onlydaily=args.onlydaily)

    # 加载数据文件
    datapath = args.dataname or '../../datas/2006-day-001.txt'
    data = btfeeds.BacktraderCSVData(dataname=datapath)
    cerebro.adddata(data)  # 添加较小时间框架的数据

    tframes = dict(daily=bt.TimeFrame.Days, weekly=bt.TimeFrame.Weeks, monthly=bt.TimeFrame.Months)

    # 根据需要重采样数据到较大时间框架
    if args.noresample:
        datapath = args.dataname2 or '../../datas/2006-week-001.txt'
        data2 = btfeeds.BacktraderCSVData(dataname=datapath)
        cerebro.adddata(data2)
    else:
        cerebro.resampledata(data, timeframe=tframes[args.timeframe], compression=args.compression)

    # 执行策略并生成结果
    cerebro.run()

    # 绘制结果
    cerebro.plot(style='bar')

# 解析命令行参数
def parse_args():
    parser = argparse.ArgumentParser(description='Multitimeframe test')
    parser.add_argument('--dataname', default='', required=False, help='数据文件路径')
    parser.add_argument('--dataname2', default='', required=False, help='第二个数据文件路径')
    parser.add_argument('--noresample', action='store_true', help='不进行数据重采样')
    parser.add_argument('--timeframe', default='weekly', choices=['daily', 'weekly', 'monthly'], help='重采样时间框架')
    parser.add_argument('--compression', default=1, type=int, help='压缩数据条数')
    parser.add_argument('--indicators', action='store_true', help='是否使用带指标的策略')
    parser.add_argument('--onlydaily', action='store_true', help='仅在每日时间框架上应用指标')
    parser.add_argument('--period', default=10, type=int, help='指标周期')
    return parser.parse_args()

if __name__ == '__main__':
    runstrat()
结论#
通过Backtrader的多时间框架支持，您可以轻松地将不同时间框架的数据结合在一起，从而实现更加灵活的交易策略。只需遵循上述规则，就能在多个时间框架中应用不同的指标，并根据数据的不同粒度调整策略的执行逻辑。

此外，Backtrader也允许通过nextstart方法来精确控制每个周期的数据处理逻辑，这使得您可以清晰地跟踪每个时间框架的计算过程，方便调试和优化。
###############################################################################################################################################
重采样#
当数据只有单一时间框架可用，而分析要在不同时间框架上进行，就需要进行数据重采样。“重采样” 实际应称为 “上采样”，因为它是从源时间框架到更大的时间框架（如：从天到周）。

Backtrader 内置了通过过滤器对象进行重采样的支持。有几种方法可以实现这一点，但有一个简单的接口可以实现，它代替通过 cerebro.adddata(data) 将数据放入系统中，使用 resampledata。

cerebro.resampledata(data, **kwargs)
有两个主要选项可以控制：

更改时间框架
压缩条数
要实现这些功能，请在调用resampledata时使用以下参数：

timeframe（默认值：bt.TimeFrame.Days）：目标时间框架，必须等于或大于源时间框架。
compression（默认值：1）：将选定的值“n”压缩为1个条。
让我们来看一个从每日到每周的示例，通过手工编写的脚本：

$ ./resampling-example.py --timeframe weekly --compression 1
我们可以将其与原始每日数据进行比较：

$ ./resampling-example.py --timeframe daily --compression 1
实现这些功能的步骤有：

先用 cerebro.adddata 加载原始数据；
使用带参数的resampledata 传递数据给cerebro：timeframe 和 compression；
示例代码：

# 加载数据
datapath = args.dataname or '../../datas/2006-day-001.txt'
data = btfeeds.BacktraderCSVData(dataname=datapath)

# 方便的字典用于时间框架参数转换
tframes = dict(
    daily=bt.TimeFrame.Days,
    weekly=bt.TimeFrame.Weeks,
    monthly=bt.TimeFrame.Months)

# 添加重采样数据而不是原始数据
cerebro.resampledata(data,
                     timeframe=tframes[args.timeframe],
                     compression=args.compression)
假设，将时间框架从每日更改为每周，然后将 3 条压缩为 1 条。

$ ./resampling-example.py --timeframe weekly --compression 3
从原始的 256 个每日 Bar 中，最终得到 18 个 3 周的 Bar。因为一年是 52 周，而 52 / 3 = 17.33，因此有18个 Bar。

重采样过滤器支持其他参数，在大多数情况下不需要更改：

参数名	默认值	描述
bar2edge	True	使用时间边界作为目标。例如，对于“ticks -> 5 seconds”，生成的5秒条将对齐到xx:00、xx:05、xx:10……
adjbartime	True	使用边界的时间调整重采样条的时间，而不是最后看到的时间戳。例如，对于重采样到“5 seconds”，条的时间将调整为hh:MM:05，即使最后看到的时间戳是hh:MM:04.33。

注意： 只有当 bar2edge 为True时，才会调整时间。如果条没有对齐到边界，调整时间没有意义。
rightedge	True	使用时间边界的右边缘设置时间。
- 如果为False，并且压缩到5秒，重采样条的时间将在hh:MM:00和hh:MM:04之间。
-如果为True，使用的时间边界为hh:MM:05。
boundoff	0	将重采样/重放边界前移一个单位。例如，从1分钟重采样到15分钟，默认行为是从00:01:00到00:15:00生成一个15分钟重放/重采样条。如果boundoff设置为1，则边界向前推1个单位。在这种情况下，原始单位是1分钟条。因此，重采样/重放将使用00:00:00到00:14:00的条生成15分钟条。
重采样测试脚本示例代码：

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse

import backtrader as bt
import backtrader.feeds as btfeeds


def runstrat():
    args = parse_args()

    # 创建 cerebro 实体
    cerebro = bt.Cerebro(stdstats=False)

    # 添加策略
    cerebro.addstrategy(bt.Strategy)

    # 加载数据
    datapath = args.dataname or '../../datas/2006-day-001.txt'
    data = btfeeds.BacktraderCSVData(dataname=datapath)

    # 方便的字典用于时间框架参数转换
    tframes = dict(
        daily=bt.TimeFrame.Days,
        weekly=bt.TimeFrame.Weeks,
        monthly=bt.TimeFrame.Months)

    # 添加重采样数据而不是原始数据
    cerebro.resampledata(data,
                         timeframe=tframes[args.timeframe],
                         compression=args.compression)

    # 运行所有内容
    cerebro.run()

    # 绘制结果
    cerebro.plot(style='bar')


def parse_args():
    parser = argparse.ArgumentParser(
        description='Pandas test script')

    parser.add_argument('--dataname', default='', required=False,
                        help='要加载的文件数据')

    parser.add_argument('--timeframe', default='weekly', required=False,
                        choices=['daily', 'weekly', 'monthly'],
                        help='要重采样到的时间框架')

    parser.add_argument('--compression', default=1, required=False, type=int,
                        help='将n个条压缩为1个')

    return parser.parse_args()


if __name__ == '__main__':
    runstrat()
#############################################################################################################################
数据回放#
随着时间的推移，单纯对已经完成关闭的 Bar 进行策略测试已不再足够，数据回放应运而生。假设，策略在时间框架X上操作（例如：每日），数据在更小的时间框架Y（例如：1分钟）可用。

数据回放的作用正如其名，使用1分钟数据回放每日条。虽然，这并不能完全再现市场发展，但比单独观察每日完成关闭的 Bar 要好得多。如果策略在每日 Bar 形成期间实时操作，那么近似 Bar 形成过程模拟策略在实际条件下的表现。

要实现数据回放，只按常规使用 backtrader 即可。

加载数据源；
使用 replaydata 将数据传递给cerebro；
添加策略；
注意： 数据回放不支持预加载，因为每个 Bar 实际上是实时构建的，任何 Cerebro 实例中都会自动禁用预加载。

可传递给replaydata的参数：

参数	默认值	描述
timeframe	bt.TimeFrame.Days	目标时间框架，必须等于或大于源时间框架
compression	1	将选定值“n”压缩为1条
扩展参数（若无特别需要请勿修改）：

参数	默认值	描述
bar2edge	True	使用时间边界作为闭合条的目标。例如，使用“ticks -> 5 seconds”时，生成的5秒条将对齐到xx:00、xx:05、xx:10……
adjbartime	False	使用边界的时间调整传递的重采样条的时间，而不是最后看到的时间戳。
rightedge	True	使用时间边界的右边缘设置时间。
举例说明，标准的 2006 年每日数据在每周基础上进行回放。

最终会有 52 个 Bar，即每周一个；
Cerebro 将调用 prenext 和 next 共计255次，这是原始数量每日 Bar；
诀窍在于：

在每周 Bar 形成时，策略的长度（len(self)）保持不变。
每过一周，长度增加1。
以下是示例，但首先是测试脚本的主要部分，其中加载数据并将其传递给cerebro进行回放，然后运行。

# 加载数据
datapath = args.dataname or '../../datas/2006-day-001.txt'
data = btfeeds.BacktraderCSVData(dataname=datapath)

# 方便的字典用于时间框架参数转换
tframes = dict(
    daily=bt.TimeFrame.Days,
    weekly=bt.TimeFrame.Weeks,
    monthly=bt.TimeFrame.Months)

# 首先添加原始数据 - 较小的时间框架
cerebro.replaydata(data,
                   timeframe=tframes[args.timeframe],
                   compression=args.compression)
示例 - 每日回放至每周#
脚本调用：

$ ./replay-example.py --timeframe weekly --compression 1
图表无法显示后台实际发生的情况，因此我们来看一下控制台输出：

prenext len 1 - counter 1
prenext len 1 - counter 2
prenext len 1 - counter 3
prenext len 1 - counter 4
prenext len 1 - counter 5
prenext len 2 - counter 6
...
prenext len 9 - counter 44
prenext len 9 - counter 45
---next len 10 - counter 46
---next len 10 - counter 47
---next len 10 - counter 48
---next len 10 - counter 49
---next len 10 - counter 50
---next len 11 - counter 51
---next len 11 - counter 52
---next len 11 - counter 53
...
---next len 51 - counter 248
---next len 51 - counter 249
---next len 51 - counter 250
---next len 51 - counter 251
---next len 51 - counter 252
---next len 52 - counter 253
---next len 52 - counter 254
---next len 52 - counter 255
我们看到内部的 self.counter 变量跟踪每次调用 prenext 或 next。前者在应用的简单移动平均线（SMA）产生值之前调用。后者在SMA产生值时调用。

策略的长度（len(self)）每5条（每周5个交易日）变化一次。
策略实际上看到的是每周条在5次更新中的发展。
这并不能完全再现市场的实际逐秒（甚至分钟、小时）的发展，但比实际观察一个条要好。

视觉输出是每周图表，这是系统测试的最终结果。

示例2 - 每日到每日带压缩#
当然，“回放”也可以应用于相同时间框架，但带有压缩。

控制台：

$ ./replay-example.py --timeframe daily --compression 2
prenext len 1 - counter 1
prenext len 1 - counter 2
prenext len 2 - counter 3
prenext len 2 - counter 4
prenext len 3 - counter 5
prenext len 3 - counter 6
prenext len 4 - counter 7
...
---next len 125 - counter 250
---next len 126 - counter 251
---next len 126 - counter 252
---next len 127 - counter 253
---next len 127 - counter 254
---next len 128 - counter 255
这次我们得到了预期的一半条数，因为请求了2倍压缩。

结论#
可以重建市场发展。通常有可用的更小时间框架数据，可以用于离散地回放系统操作的时间框架。

测试脚本如下：

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse

import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicators as btind


class SMAStrategy(bt.Strategy):
    params = (
        ('period', 10),
        ('onlydaily', False),
    )

    def __init__(self):
        self.sma = btind.SMA(self.data, period=self.p.period)

    def start(self):
        self.counter = 0

    def prenext(self):
        self.counter += 1
        print('prenext len %d - counter %d' % (len(self), self.counter))

    def next(self):
        self.counter += 1
        print('---next len %d - counter %d' % (len(self), self.counter))


def runstrat():
    args = parse_args()

    # 创建 cerebro 实体
    cerebro = bt.Cerebro(stdstats=False)

    cerebro.addstrategy(
        SMAStrategy,
        # 策略参数
        period=args.period,
    )

    # 加载数据
    datapath = args.dataname or '../../datas/2006-day-001.txt'
    data = btfeeds.BacktraderCSVData(dataname=datapath)

    # 方便的字典用于时间框架参数转换
    tframes = dict(
        daily=bt.TimeFrame.Days,
        weekly=bt.TimeFrame.Weeks,
        monthly=bt.TimeFrame.Months)

    # 首先添加原始数据 - 较小的时间框架
    cerebro.replaydata(data,
                       timeframe=tframes[args.timeframe],
                       compression=args.compression)

    # 运行所有内容
    cerebro.run()

    # 绘制结果
    cerebro.plot(style='bar')


def parse_args():
    parser = argparse.ArgumentParser(
        description='Pandas test script')

    parser.add_argument('--dataname', default='', required=False,
                        help='要加载的文件数据')

    parser.add_argument('--timeframe', default='weekly', required=False,
                        choices=['daily', 'weekly', 'monthly'],
                        help='要重采样到的时间框架')

    parser.add_argument('--compression', default=1, required=False, type=int,
                        help='将n个条压缩为1个')

    parser.add_argument('--period', default=10, required=False, type=int,
                        help='应用于指标的周期')

    return parser.parse_args()


if __name__ == '__main__':
    runstrat()
###############################################################################################
滚动#
并非所有提供商都提供连续期货合约数据。有时提供的数据是仍在交易的到期合约的有效数据。这种情况下，进行回测会变得很不方便，因为数据分散在多个不同的合约上，并且这些合约还会在时间上重叠。

如果能够正确地将这些过去的合约数据连接成一个连续的数据流，可以缓解这种痛苦。问题在于：

没有一种最佳方法将不同到期日期的数据连接成一个连续的期货数据
有些文献，如 SierraChart的文章
滚动数据源#
从backtrader 1.8.10.99开始，增加了将不同到期日期的期货数据连接成连续期货的功能：

import backtrader as bt

cerebro = bt.Cerebro()
data0 = bt.feeds.MyFeed(dataname='Expiry0')
data1 = bt.feeds.MyFeed(dataname='Expiry1')
...
dataN = bt.feeds.MyFeed(dataname='ExpiryN')

drollover = cerebro.rolloverdata(data0, data1, ..., dataN, name='MyRoll', **kwargs)

cerebro.run()
注意：

**kwargs将在下文解释
也可以直接访问RollOver数据源（如果需要子类化，这是很有帮助的）：
import backtrader as bt

cerebro = bt.Cerebro()
data0 = bt.feeds.MyFeed(dataname='Expiry0')
data1 = bt.feeds.MyFeed(dataname='Expiry1')
...
dataN = bt.feeds.MyFeed(dataname='ExpiryN')

drollover = bt.feeds.RollOver(data0, data1, ..., dataN, dataname='MyRoll', **kwargs)
cerebro.adddata(drollover)

cerebro.run()
注意：

使用RollOver时，使用dataname参数分配名称，这是所有数据源用于传递名称/代码的标准参数。在这种情况下，它被重用以给整个滚动的期货集分配一个通用名称。
对于cerebro.rolloverdata，使用name参数为数据源分配名称，这是该方法的一个命名参数。
Rollover 的使用可概括为：

按通常方式创建数据源，但不要将它们添加到cerebro
将这些数据源作为输入传递给bt.feeds.RollOver
也传递一个dataname，主要用于识别目的
然后将这个滚动的数据源添加到cerebro
滚动的选项#
提供两个参数来控制滚动过程：

参数名	默认值	描述
checkdate	None	必须是一个可调用对象，签名：checkdate(dt, d)
- dt 一个datetime.datetime对象
- d，当前活跃期货的数据源
预期返回值
- True：只要可调用对象返回此值，就可以切换到下一个期货
- False：不能进行到期转换
例如，如果某商品在3月的第三个星期五到期，checkdate可以在到期所在的一整周内返回True。
checkcondition	None	仅当checkdate返回True时才会调用此参数。如果为None，则内部评估为True（执行滚动）。否则，它必须是一个可调用对象，签名是 checkcondition(d0, d1)
- d0是当前活跃期货的数据源
- d1是下一个到期的数据源
预期返回值：
- True：滚动到下一个期货
- False：不能进行到期转换
例如，可以通过checkcondition判断，如果d0的交易量小于d1，则进行到期转换。
子类化RollOver#
如果指定的可调用对象还不够用，可以子类化RollOver。需要子类化的方法有：

def _checkdate(self, dt, d)
它与上文同名参数的签名相匹配。预期返回值也相同。

def _checkcondition(self, d0, d1)
它与上文同名参数的签名相匹配。预期返回值也相同。

示例用法#
注意： 示例中的默认行为是使用cerebro.rolloverdata。可以通过传递-no-cerebro标志来更改。在这种情况下，示例使用RollOver和cerebro.adddata。

实现包括一个可在backtrader源代码中找到的示例。

期货拼接

首先让我们通过运行不带参数的示例来看一个纯粹的拼接示例：

$ ./rollover.py
输出结果如下：

Len, Name, RollName, Datetime, WeekDay, Open, High, Low, Close, Volume, OpenInterest
0001, FESX, 199FESXM4, 2013-09-26, Thu, 2829.0, 2843.0, 2829.0, 2843.0, 3.0, 1000.0
0002, FESX, 199FESXM4, 2013-09-27, Fri, 2842.0, 2842.0, 2832.0, 2841.0, 16.0, 1101.0
...
0176, FESX, 199FESXM4, 2014-06-20, Fri, 3315.0, 3324.0, 3307.0, 3322.0, 134777.0, 520978.0
0177, FESX, 199FESXU4, 2014-06-23, Mon, 3301.0, 3305.0, 3265.0, 3285.0, 730211.0, 3003692.0
...
0241, FESX, 199FESXU4, 2014-09-19, Fri, 3287.0, 3308.0, 3286.0, 3294.0, 144692.0, 566249.0
0242, FESX, 199FESXZ4, 2014-09-22, Mon, 3248.0, 3263.0, 3231.0, 3240.0, 582077.0, 2976624.0
...
0306, FESX, 199FESXZ4, 2014-12-19, Fri, 3196.0, 3202.0, 3131.0, 3132.0, 226415.0, 677924.0
0307, FESX, 199FESXH5, 2014-12-22, Mon, 3151.0, 3177.0, 3139.0, 3168.0, 547095.0, 2952769.0
...
0366, FESX, 199FESXH5, 2015-03-20, Fri, 3680.0, 3698.0, 3672.0, 3695.0, 147632.0, 887205.0
0367, FESX, 199FESXM5, 2015-03-23, Mon, 3654.0, 3655.0, 3608.0, 3618.0, 802344.0, 3521988.0
...
0426, FESX, 199FESXM5, 2015-06-18, Thu, 3398.0, 3540.0, 3373.0, 3465.0, 1173246.0, 811805.0
0427, FESX, 199FESXM5, 2015-06-19, Fri, 3443.0, 3499.0, 3440.0, 3488.0, 104096.0, 516792.0
可以看到，当数据源结束时，下一个数据源接管。

这总是在一个星期五和下一个星期一之间发生：示例中的期货合约总是在星期五到期。

期货滚动无检查

运行带有--rollover参数的示例：

$ ./rollover.py --rollover --plot
输出结果类似：

Len, Name, RollName, Datetime, WeekDay, Open, High, Low, Close, Volume, OpenInterest
0001, FESX, 199FESXM4, 2013-09-26, Thu

, 2829.0, 2843.0, 2829.0, 2843.0, 3.0, 1000.0
0002, FESX, 199FESXM4, 2013-09-27, Fri, 2842.0, 2842.0, 2832.0, 2841.0, 16.0, 1101.0
...
0176, FESX, 199FESXM4, 2014-06-20, Fri, 3315.0, 3324.0, 3307.0, 3322.0, 134777.0, 520978.0
0177, FESX, 199FESXU4, 2014-06-23, Mon, 3301.0, 3305.0, 3265.0, 3285.0, 730211.0, 3003692.0
...
0241, FESX, 199FESXU4, 2014-09-19, Fri, 3287.0, 3308.0, 3286.0, 3294.0, 144692.0, 566249.0
0242, FESX, 199FESXZ4, 2014-09-22, Mon, 3248.0, 3263.0, 3231.0, 3240.0, 582077.0, 2976624.0
...
0306, FESX, 199FESXZ4, 2014-12-19, Fri, 3196.0, 3202.0, 3131.0, 3132.0, 226415.0, 677924.0
0307, FESX, 199FESXH5, 2014-12-22, Mon, 3151.0, 3177.0, 3139.0, 3168.0, 547095.0, 2952769.0
...
0366, FESX, 199FESXH5, 2015-03-20, Fri, 3680.0, 3698.0, 3672.0, 3695.0, 147632.0, 887205.0
0367, FESX, 199FESXM5, 2015-03-23, Mon, 3654.0, 3655.0, 3608.0, 3618.0, 802344.0, 3521988.0
...
0426, FESX, 199FESXM5, 2015-06-18, Thu, 3398.0, 3540.0, 3373.0, 3465.0, 1173246.0, 811805.0
0427, FESX, 199FESXM5, 2015-06-19, Fri, 3443.0, 3499.0, 3440.0, 3488.0, 104096.0, 516792.0
可以清楚地看到，合约的更换是在3月、6月、9月和12月的第三个星期五。

这大部分是错误的。虽然backtrader无法知道，但作者知道EuroStoxx 50期货在到期月的第三个星期五中午12:00 CET停止交易。因此，即使在到期月的第三个星期五有一个每日条，更换也是太晚了。

在周内更换#
在示例中实现了一个checkdate可调用对象，它计算当前活跃合约的到期日期。

checkdate会在到期周一旦到达时允许进行滚动（如果例如星期一是银行假日，可能会是星期二）。

运行带有--rollover和--checkdate参数的示例：

$ ./rollover.py --rollover --checkdate --plot
输出结果类似：

Len, Name, RollName, Datetime, WeekDay, Open, High, Low, Close, Volume, OpenInterest
0001, FESX, 199FESXM4, 2013-09-26, Thu, 2829.0, 2843.0, 2829.0, 2843.0, 3.0, 1000.0
0002, FESX, 199FESXM4, 2013-09-27, Fri, 2842.0, 2842.0, 2832.0, 2841.0, 16.0, 1101.0
...
0171, FESX, 199FESXM4, 2014-06-13, Fri, 3283.0, 3292.0, 3253.0, 3276.0, 734907.0, 2715357.0
0172, FESX, 199FESXU4, 2014-06-16, Mon, 3261.0, 3275.0, 3252.0, 3262.0, 180608.0, 844486.0
...
0236, FESX, 199FESXU4, 2014-09-12, Fri, 3245.0, 3247.0, 3220.0, 3232.0, 650314.0, 2726874.0
0237, FESX, 199FESXZ4, 2014-09-15, Mon, 3209.0, 3224.0, 3203.0, 3221.0, 153448.0, 983793.0
...
0301, FESX, 199FESXZ4, 2014-12-12, Fri, 3127.0, 3143.0, 3038.0, 3042.0, 1409834.0, 2934179.0
0302, FESX, 199FESXH5, 2014-12-15, Mon, 3041.0, 3089.0, 2963.0, 2980.0, 329896.0, 904053.0
...
0361, FESX, 199FESXH5, 2015-03-13, Fri, 3657.0, 3680.0, 3627.0, 3670.0, 867678.0, 3499116.0
0362, FESX, 199FESXM5, 2015-03-16, Mon, 3594.0, 3641.0, 3588.0, 3629.0, 250445.0, 1056099.0
...
0426, FESX, 199FESXM5, 2015-06-18, Thu, 3398.0, 3540.0, 3373.0, 3465.0, 1173246.0, 811805.0
0427, FESX, 199FESXM5, 2015-06-19, Fri, 3443.0, 3499.0, 3440.0, 3488.0, 104096.0, 516792.0
效果要好得多。滚动现在发生在到期月的第三个星期五之前的星期一。

添加交易量条件#
即使有了改进，还可以进一步改善，通过考虑日期和交易量来决定是否滚动。仅在新合约的交易量超过当前活跃合约时进行切换。

运行带有--rollover、--checkdate和--checkcondition参数的示例：

$ ./rollover.py --rollover --checkdate --checkcondition --plot
输出结果类似：

Len, Name, RollName, Datetime, WeekDay, Open, High, Low, Close, Volume, OpenInterest
0001, FESX, 199FESXM4, 2013-09-26, Thu, 2829.0, 2843.0, 2829.0, 2843.0, 3.0, 1000.0
0002, FESX, 199FESXM4, 2013-09-27, Fri, 2842.0, 2842.0, 2832.0, 2841.0, 16.0, 1101.0
...
0175, FESX, 199FESXM4, 2014-06-19, Thu, 3307.0, 3330.0, 3300.0, 3321.0, 717979.0, 759122.0
0176, FESX, 199FESXU4, 2014-06-20, Fri, 3309.0, 3318.0, 3290

.0, 3298.0, 711627.0, 2957641.0
...
0240, FESX, 199FESXU4, 2014-09-18, Thu, 3249.0, 3275.0, 3243.0, 3270.0, 846600.0, 803202.0
0241, FESX, 199FESXZ4, 2014-09-19, Fri, 3273.0, 3293.0, 3250.0, 3252.0, 1042294.0, 3021305.0
...
0305, FESX, 199FESXZ4, 2014-12-18, Thu, 3095.0, 3175.0, 3085.0, 3172.0, 1309574.0, 889112.0
0306, FESX, 199FESXH5, 2014-12-19, Fri, 3195.0, 3200.0, 3106.0, 3147.0, 1329040.0, 2964538.0
...
0365, FESX, 199FESXH5, 2015-03-19, Thu, 3661.0, 3691.0, 3646.0, 3668.0, 1271122.0, 1054639.0
0366, FESX, 199FESXM5, 2015-03-20, Fri, 3607.0, 3664.0, 3595.0, 3646.0, 1182235.0, 3407004.0
...
0426, FESX, 199FESXM5, 2015-06-18, Thu, 3398.0, 3540.0, 3373.0, 3465.0, 1173246.0, 811805.0
0427, FESX, 199FESXM5, 2015-06-19, Fri, 3443.0, 3499.0, 3440.0, 3488.0, 104096.0, 516792.0
效果更好。我们已将切换日期移至到期月第三个星期五之前的星期四。

结论#
backtrader 现在包含一个灵活的机制，用于创建连续期货数据流。

示例用法#
$ ./rollover.py --help
输出：

usage: rollover.py [-h] [--no-cerebro] [--rollover] [--checkdate]
                   [--checkcondition] [--plot [kwargs]]

Sample for Roll Over of Futures

optional arguments:
  -h, --help            show this help message and exit
  --no-cerebro          Use RollOver Directly (default: False)
  --rollover
  --checkdate           Change during expiration week (default: False)
  --checkcondition      Change when a given condition is met (default: False)
  --plot [kwargs], -p [kwargs]
                        Plot the read data applying any kwargs passed For
                        example: --plot style="candle" (to plot candles)
                        (default: None)
示例代码：

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse
import bisect
import calendar
import datetime

import backtrader as bt


class TheStrategy(bt.Strategy):
    def start(self):
        header = ['Len', 'Name', 'RollName', 'Datetime', 'WeekDay', 'Open',
                  'High', 'Low', 'Close', 'Volume', 'OpenInterest']
        print(', '.join(header))

    def next(self):
        txt = list()
        txt.append('%04d' % len(self.data0))
        txt.append('{}'.format(self.data0._dataname))
        # Internal knowledge ... current expiration in use is in _d
        txt.append('{}'.format(self.data0._d._dataname))
        txt.append('{}'.format(self.data.datetime.date()))
        txt.append('{}'.format(self.data.datetime.date().strftime('%a')))
        txt.append('{}'.format(self.data.open[0]))
        txt.append('{}'.format(self.data.high[0]))
        txt.append('{}'.format(self.data.low[0]))
        txt.append('{}'.format(self.data.close[0]))
        txt.append('{}'.format(self.data.volume[0]))
        txt.append('{}'.format(self.data.openinterest[0]))
        print(', '.join(txt))


def checkdate(dt, d):
    # Check if the date is in the week where the 3rd friday of Mar/Jun/Sep/Dec

    # EuroStoxx50 expiry codes: MY
    # M -> H, M, U, Z (Mar, Jun, Sep, Dec)
    # Y -> 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 -> year code. 5 -> 2015
    MONTHS = dict(H=3, M=6, U=9, Z=12)

    M = MONTHS[d._dataname[-2]]

    centuria, year = divmod(dt.year, 10)
    decade = centuria * 10

    YCode = int(d._dataname[-1])
    Y = decade + YCode
    if Y < dt.year:  # Example: year 2019 ... YCode is 0 for 2020
        Y += 10

    exp_day = 21 - (calendar.weekday(Y, M, 1) + 2) % 7
    exp_dt = datetime.datetime(Y, M, exp_day)

    # Get the year, week numbers
    exp_year, exp_week, _ = exp_dt.isocalendar()
    dt_year, dt_week, _ = dt.isocalendar()

    # print('dt {} vs {} exp_dt'.format(dt, exp_dt))
    # print('dt_week {} vs {} exp_week'.format(dt_week, exp_week))

    # can switch if in same week
    return (dt_year, dt_week) == (exp_year, exp_week)


def checkvolume(d0, d1):
    return d0.volume[0] < d1.volume[0]  # Switch if volume from d0 < d1


def runstrat(args=None):
    args = parse_args(args)

    cerebro = bt.Cerebro()

    fcodes = ['199FESXM4', '199FESXU4', '199FESXZ4', '199FESXH5', '199FESXM5']
    store = bt.stores.VChartFile()
    ffeeds = [store.getdata(dataname=x) for x in fcodes]

    rollkwargs = dict()
    if args.checkdate:
        rollkwargs['checkdate'] = checkdate

        if args.checkcondition:
            rollkwargs['checkcondition'] = checkvolume

    if not args.no_cerebro:
        if args.rollover:
            cerebro.rolloverdata(name='FESX', *ffeeds, **rollkwargs)
        else:
            cerebro.chaindata(name='FESX', *ffeeds)
    else:
        drollover = bt.feeds.RollOver(*ffeeds, dataname='FESX', **rollkwargs)
        cerebro.adddata(drollover)

    cerebro.addstrategy(TheStrategy)
    cerebro.run(stdstats=False)

    if args.plot:
        pkwargs = dict(style='bar')
        if args.plot is not True:  # evals to True but is not True
            npkwargs = eval('dict(' + args.plot + ')')  # args were passed
            pkwargs.update(npkwargs)

        cerebro.plot(**pkwargs)


def parse_args(pargs=None):

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Sample for Roll Over of Futures')

    parser.add_argument('--no-cerebro', required=False, action='store_true',
                        help='Use RollOver Directly')

    parser.add_argument('--rollover', required=False, action='store_true')

    parser.add_argument('--checkdate', required=False, action='store_true',
                        help='Change during expiration week')

    parser.add_argument('--checkcondition', required=False,
                        action='store_true',
                        help='Change when a given condition is met')

    # Plot options
    parser.add_argument('--plot', '-p', nargs='?', required=False,
                        metavar='kwargs', const=True,
                        help=('Plot the read data applying any kwargs passed\n'
                              '\n'
                              'For example:\n'
                              '\n'
                              '  --plot style="candle" (to plot candles)\n'))

    if pargs is not None:
        return parser.parse_args(pargs)

    return parser.parse_args()


if __name__ == '__main__':
    runstrat()
#############################################################################################################
过滤器 Filters#
该功能是较晚加入到 Backtrader 中的，且为了适应已有的内部结构进行了一些调整。因此，它在灵活性和功能完备性上可能不如预期，但在许多情况下仍然能达到目的。

尽管实现时尝试支持即插即用的过滤器链，但由于原有内部结构的限制，始终无法保证每次都能实现。因此，有些过滤器可以链式使用，而有些则不能。

目的#
将数据源提供的值转换为不同的数据流。

该实现最初是为了简化两个明显的过滤器的实现，这两个过滤器可以通过cerebro API直接使用，分别是 重采样 和 重放。

重采样（cerebro.resampledata）：这个过滤器会改变传入数据流的时间框架和压缩比例，如：(秒，1) -> (天，1)。这意味着原始数据流是以1秒为周期的数据条。重采样过滤器会拦截数据并进行缓冲，直到能够提供1天的条形数据。这发生在看到第二天的1秒条形数据时。

重放（cerebro.replaydata），在上面相同的时间框架下，过滤器会利用1秒的分辨率条形数据重建1天的条形数据。也就是说，1天的条形数据会被反复传递，直到显示出所有1秒的条形数据，并且数据内容会更新。这种方法模拟了实际交易日的发展。

注意，在日期没有变化的情况下，数据的长度（len(data)）以及策略的长度保持不变。

工作原理#
给定一个已有的数据源，你可以使用addfilter方法来添加过滤器：

data = MyDataFeed(dataname=myname)
data.addfilter(filter, *args, **kwargs)
cerebro.adddata(data)
即使它与重采样或重放过滤器兼容，你也可以做如下操作：

data = MyDataFeed(dataname=myname)
data.addfilter(filter, *args, **kwargs)
cerebro.replaydata(data)
过滤器接口#
过滤器必须符合以下接口要求。首先，要是一个可调用的对象，接受如下签名：

callable(data, *args, **kwargs)
或一个可以实例化并被调用的类，在实例化时其__init__方法必须支持以下签名：

def __init__(self, data, *args, **kwargs)
__call__方法的签名为：

def __call__(self, data, *args, **kwargs)
每当新的数据流值到来时，实例都会被调用。*args和**kwargs与__init__方法传递的参数相同。

返回值	描述
True	表示数据流的内部数据获取循环需要重新尝试从数据源中获取数据，因为数据流的长度被修改了。
False	即使数据可能已经被编辑（例如：修改了close价格），数据流的长度保持不变。
如果是基于类的过滤器，还可以实现两个额外的方法：

last，其签名为：

def last(self, data, *args, **kwargs)
当数据流结束时，这个方法会被调用，允许过滤器推送它可能缓冲的数据。例如在重采样的情况下，一个条形数据会被缓冲，直到看到下一个时间段的数据。如果数据流结束，就没有新的数据可以推动缓冲的数据，last方法提供了推送缓冲数据的机会。

注意

如果过滤器没有任何参数，且在添加时没有额外的参数，签名可以简化为：

def __init__(self, data) -> def __init__(self, data)
示例过滤器#
以下是一个非常简单的过滤器实现：

class SessionFilter(object):
    def __init__(self, data):
        pass

    def __call__(self, data):
        if data.p.sessionstart <= data.datetime.time() <= data.p.sessionend:
            # 在交易时段内
            return False  # 告诉外部数据循环，当前条形数据可以继续处理

        # 在常规交易时段外
        data.backwards()  # 从数据堆栈中移除该条形数据
        return True  # 告诉外部数据循环，必须获取新的条形数据
该过滤器：

使用data.p.sessionstart和data.p.sessionend判断 Bar 否在交易时段。
如果在交易时段内，返回False，表示没有做任何修改，当前条形数据可以继续处理。
如果不在交易时段内，条形数据会被移除，返回True表示需要获取新数据。
注意，data.backwards()使用了LineBuffer接口，深入了backtrader的内部实现。

使用场景#
有些数据源包含了非交易时段的数据，这些数据可能对交易者没有意义。使用此过滤器，只有在交易时段内的条形数据才会被考虑。

数据伪API for 过滤器

在上面的示例中，展示了如何通过data.backwards()方法从数据流中移除当前条形数据。数据源对象中有一些有用的调用，作为过滤器的伪API，具体如下：

data.backwards(size=1, force=False)：从数据流中移除size条数据（默认为1），通过将逻辑指针向后移动。如果force=True，则物理存储也会被移除。
data.forward(value=float('NaN'), size=1)：将size条数据移到数据流的前面，如果需要会增加物理存储，并用value填充。
data._addtostack(bar, stash=False)：将条形数据bar添加到堆栈中，以便以后处理。如果stash=False，条形数据将在下一轮迭代时立即被处理；如果stash=True，则会经过完整的处理循环，包括可能被过滤器重新解析。
data._save2stack(erase=False, force=False)：将当前条形数据保存到堆栈中，以便稍后处理。如果erase=True，则会调用data.backwards()，并接收force参数。
data._updatebar(bar, forward=False, ago=0)：使用bar中的值覆盖数据流中相应位置的数据。如果ago=0，则更新当前条形数据。如果ago=-1，则更新前一个条形数据。
另一个示例：Pinkfish过滤器#
这是一个可以链式使用的过滤器示例，特别是与重放过滤器一起使用。Pinkfish的名字来源于该库的主页面，它的概念是通过使用每日数据来执行仅能通过即时数据完成的操作。

实现方法：

将每日条形数据分成两个部分：OHL和C。

这些部分与重放一起被串联，在数据流中呈现出以下形式：

With Len X -> OHL
With Len X -> OHLC
With Len X + 1 -> OHL
With Len X + 1 -> OHLC
With Len X + 2 -> OHL
With Len X + 2 -> OHLC
...
逻辑：

当接收到一个OHLC条形数据时，会复制它，并拆解成两个部分：OHL和C。
OHL条形数据的关闭价格被替换为开盘、最高和最低价格的平均值。
C条形数据即为“tick”，关闭价格会用来填充四个价格字段。
这两个部分被分别处理，OHL部分会立即加入堆栈，C部分则被推迟处理。
该过滤器与以下功能一起工作：

重放过滤器，合并OHLO和CCCC部分，最终输出OHLC条形数据。
使用场景#
例如，当今天最大值是过去20个交易日中的最高值时，可发出“关闭”订单，并在第二次tick时执行。

class DaySplitter_Close(bt.with_metaclass(bt.MetaParams, object)):
    '''
    Splits a daily bar in two parts simulating 2 ticks which will be used to
    replay the data:

      - First tick: ``OHLX``

        The ``Close`` will be replaced by the *average* of ``Open``, ``High``
        and ``Low``

        The session opening time is used for this tick

      and

      - Second tick: ``CCCC``

        The ``Close`` price will be used for the four components of the price

        The session closing time is used for this tick

    The volume will be split amongst the 2 ticks using the parameters:

      - ``closevol`` (default: ``0.5``) The value indicate which percentage, in
        absolute terms from 0.0 to 1.0, has to be assigned to the *closing*
        tick. The rest will be assigned to the ``OHLX`` tick.

    **This filter is meant to be used together with** ``cerebro.replaydata``

    '''
    params = (
        ('closevol', 0.5),  # 0 -> 1 amount of volume to keep for close
    )

    # replaying = True

    def __init__(self, data):
        self.lastdt = None

    def __call__(self, data):
        # Make a copy of the new bar and remove it from stream
        datadt = data.datetime.date()  # keep the date

        if self.lastdt == datadt:
            return False  # skip bars that come again in the filter

        self.lastdt = datadt  # keep ref to last seen bar

        # Make a copy of current data for ohlbar
        ohlbar = [data.lines[i][0] for i in range(data.size())]
        closebar = ohlbar[:]  # Make a copy for the close

        # replace close price with o-h-l average
        ohlprice = ohlbar[data.Open] + ohlbar[data.High] + ohlbar[data.Low]
        ohlbar[data.Close] = ohlprice / 3.0

        vol = ohlbar[data.Volume]  # adjust volume
        ohlbar[data.Volume] = vohl = int(vol * (1.0 - self.p.closevol))

        oi = ohlbar[data.OpenInterest]  # adjust open interst
        ohlbar[data.OpenInterest] = 0

        # Adjust times
        dt = datetime.datetime.combine(datadt, data.p.sessionstart)
        ohlbar[data.DateTime] = data.date2num(dt)

        # Ajust closebar to generate a single tick -> close price
        closebar[data.Open] = cprice = closebar[data.Close]
        closebar[data.High] = cprice
        closebar[data.Low] = cprice
        closebar[data.Volume] = vol - vohl
        ohlbar[data.OpenInterest] = oi

        # Adjust times
        dt = datetime.datetime.combine(datadt, data.p.sessionend)
        closebar[data.DateTime] = data.date2num(dt)

        # Update stream
        data.backwards(force=True)  # remove the copied bar from stream
        data._add2stack(ohlbar)  # add ohlbar to stack
        # Add 2nd part to stash to delay processing to next round
        data._add2stack(closebar, stash=True)

        return False  # initial tick can be further processed from stack
########################################################################################################################################
Filters 参考文档#
SessionFilter#
class backtrader.filters.SessionFilter(data)

此类可作为过滤器应用于数据源，将过滤掉落在常规交易时间之外的日内数据（即盘前/盘后数据）。

这是一个“非简单”过滤器，必须管理数据栈（在初始化和调用期间传递）。
它不需要“last”方法，因为没有需要传递的内容。
SessionFilterSimple#
class backtrader.filters.SessionFilterSimple(data)

此类可作为过滤器应用于数据源，将过滤掉落在常规交易时间之外的日内数据（即盘前/盘后数据）。

这是一个“简单”过滤器，不需要管理数据栈（在初始化和调用期间传递）。
它不需要“last”方法，因为没有需要传递的内容。
Bar 管理将由 SimpleFilterWrapper 类处理，该类在 DataBase.addfilter_simple 调用期间添加。
SessionFiller#
class backtrader.filters.SessionFiller(data)
为声明的会话开始/结束时间内的数据源填充条。

参数：

fill_price (默认: None): 如果传递了 None，将使用前一个条的收盘价。为了得到一个不显示在图表中的条，可以使用 float(‘NaN’)。
fill_vol (默认: float(‘NaN’)): 用于填充缺失交易量的值。
fill_oi (默认: float(‘NaN’)): 用于填充缺失未平仓合约的值。
skip_first_fill (默认: True): 在看到第一个有效条时，不从会话开始填充到该条。
CalendarDays#
class backtrader.filters.CalendarDays(data)

填充缺失日历日到交易日。

参数：

fill_price (默认: None):
0: 用给定值填充。
None: 使用上一个已知收盘价。
-1: 使用上一个条的中点（高低平均值）。
fill_vol (默认: float(‘NaN’)): 用于填充缺失交易量的值。
fill_oi (默认: float(‘NaN’)): 用于填充缺失未平仓合约的值。
BarReplayer_Open#
class backtrader.filters.BarReplayer_Open(data)

此过滤器将一个条分为两部分：

Open: 条的开盘价将用于交付一个初始价格条，其中四个组件（OHLC）相等。
此初始条的交易量/未平仓合约字段为 0。
OHLC: 原始条完整交付，包含原始交易量/未平仓合约。
分割模拟重播，无需使用重播过滤器。

DaySplitter_Close#
class backtrader.filters.DaySplitter_Close(data)

将一个每日条分为两部分，模拟两个价格点以重播数据：

第一个价格点: OHLX
收盘价将替换为开盘价、高价和低价的平均值。
此价格点使用会话的开盘时间。
第二个价格点: CCCC
收盘价将用于四个价格组件。
此价格点使用会话的收盘时间。
交易量将在两个价格点之间分配，使用参数：
closevol (默认: 0.5): 值表示百分比，绝对值范围为 0.0 到 1.0，分配给收盘价格点的比例。其余部分将分配给 OHLX 价格点。
此过滤器用于配合 cerebro.replaydata 一起使用。

HeikinAshi#
class backtrader.filters.HeikinAshi(data)
此过滤器重新建模开盘、高价、低价、收盘价以形成 HeikinAshi 蜡烛图。

参考：

Heikin Ashi Candlesticks
StockCharts Heikin Ashi
Renko#
class backtrader.filters.Renko(data)

修改数据流以绘制 Renko 条（或砖）。

参数：

hilo (默认: False): 使用高价和低价而不是收盘价来决定是否需要新砖。
size (默认: None): 每个砖块的大小。
autosize (默认: 20.0): 如果 size 为 None，将使用此值自动计算砖块大小（简单地将当前价格除以给定值）。
dynamic (默认: False): 如果为 True 并且使用 autosize，当移动到新砖块时将重新计算砖块大小。这当然会消除 Renko 砖块的完美对齐。
align (默认: 1.0): 用于对齐砖块价格边界的因子。例如，如果价格为 3563.25 并且 align 为 10.0，则对齐后的价格将为 3560。计算方法：
3563.25 / 10.0 = 356.325
四舍五入并删除小数位 -> 356
356 * 10.0 -> 3560
参考#
StockCharts Renko
#####################################################################################################
Yahoo 数据源说明#
在 2017 年 5 月，Yahoo 停用了现有的 CSV 格式的历史数据下载 API。

很快，新 API（这里称为 v7）被标准化并已实现。

这也带来了实际 CSV 下载格式的变化。

使用 v7 API/格式#
从版本 1.9.49.116 开始，这是默认行为。可以简单地选择：

YahooFinanceData 用于在线下载
YahooFinanceCSVData 用于离线下载的文件
使用旧的 API/格式#
要使用旧的 API/格式，可以：

在线 Yahoo 数据源实例化如下：

data = bt.feeds.YahooFinanceData(
    ...
    version='',
    ...
)
离线 Yahoo 数据源实例化如下：

data = bt.feeds.YahooFinanceCSVData(
    ...
    version='',
    ...
)
可能在线服务会恢复（服务在没有任何公告的情况下被停用……它也可能会恢复）

或者

仅用于在变更前下载的离线文件，也可以这样做：

data = bt.feeds.YahooLegacyCSV(
    ...
    ...
)
新的 YahooLegacyCSV 简化了使用 version='' 的操作。
###########################################################################
Pandas 数据源示例#
注意，需要安装 pandas 及其依赖项。支持 Pandas Dataframe 对很多人来说很重要，他们依赖于 Pandas 提供的不同数据源（包括 CSV）的解析代码及其他功能。

数据源的重要声明#
注意

这些只是声明。不要盲目复制此代码。请参见下面的实际用法示例：

class PandasData(feed.DataBase):
    '''
    ``dataname`` 参数继承自 ``feed.DataBase`` 是 pandas DataFrame
    '''

    params = (
        # datetime 的可能值（必须始终存在）
        #  None : datetime 是 Pandas Dataframe 中的 "index"
        #  -1 : 自动检测位置或大小写相同的名称
        #  >= 0 : pandas dataframe 中列的数值索引
        #  string : pandas dataframe 中的列名（作为索引）
        ('datetime', None),

        # 下面是可能的值：
        #  None : 列不存在
        #  -1 : 自动检测位置或大小写相同的名称
        #  >= 0 : pandas dataframe 中列的数值索引
        #  string : pandas dataframe 中的列名（作为索引）
        ('open', -1),
        ('high', -1),
        ('low', -1),
        ('close', -1),
        ('volume', -1),
        ('openinterest', -1),
    )
上述 PandasData 类的片段展示了关键点：

在实例化时，类的 dataname 参数包含 Pandas Dataframe

该参数继承自基类 feed.DataBase

新参数具有 DataSeries 中常规字段的名称，并遵循以下约定：

datetime (默认: None)

None: datetime 是 Pandas Dataframe 中的“索引”
-1: 自动检测位置或大小写相同的名称
= 0: pandas dataframe 中列的数值索引

string: pandas dataframe 中的列名（作为索引）
open、high、low、close、volume、openinterest (默认: -1)

None: 列不存在
-1: 自动检测位置或大小写相同的名称
= 0: pandas dataframe 中列的数值索引

string: pandas dataframe 中的列名（作为索引）
一个小示例应能够加载经过 Pandas 解析的标准 2006 示例数据，而不是直接由 backtrader 解析。

运行示例代码以使用 CSV 数据中的现有“头”：

$ ./panda-test.py
--------------------------------------------------
               Open     High      Low    Close  Volume  OpenInterest
Date
2006-01-02  3578.73  3605.95  3578.73  3604.33       0             0
2006-01-03  3604.08  3638.42  3601.84  3614.34       0             0
2006-01-04  3615.23  3652.46  3615.23  3652.46       0             0
相同的代码，但告诉脚本跳过头：

$ ./panda-test.py --noheaders
--------------------------------------------------
                  1        2        3        4  5  6
0
2006-01-02  3578.73  3605.95  3578.73  3604.33  0  0
2006-01-03  3604.08  3638.42  3601.84  3614.34  0  0
2006-01-04  3615.23  3652.46  3615.23  3652.46  0  0
第二次运行时，使用 pandas.read_csv：

跳过第一行输入（skiprows 参数设置为 1）
不查找头行（header 参数设置为 None）
backtrader 对 Pandas 的支持尝试自动检测列名是否已被使用，否则使用数值索引，并相应地进行操作，尽量提供最佳匹配。

以下图表展示了成功的结果。Pandas Dataframe 已正确加载（在两种情况下均如此）。

image

示例代码：

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse

import backtrader as bt
import backtrader.feeds as btfeeds

import pandas


def runstrat():
    args = parse_args()

    # 创建 cerebro 实体
    cerebro = bt.Cerebro(stdstats=False)

    # 添加策略
    cerebro.addstrategy(bt.Strategy)

    # 获取 pandas dataframe
    datapath = ('../../datas/2006-day-001.txt')

    # 模拟在请求 noheaders 时不存在头行
    skiprows = 1 if args.noheaders else 0
    header = None if args.noheaders else 0

    dataframe = pandas.read_csv(datapath,
                                skiprows=skiprows,
                                header=header,
                                parse_dates=True,
                                index_col=0)

    if not args.noprint:
        print('--------------------------------------------------')
        print(dataframe)
        print('--------------------------------------------------')

    # 将其传递给 backtrader 数据源并添加到 cerebro
    data = bt.feeds.PandasData(dataname=dataframe)

    cerebro.adddata(data)

    # 运行所有内容
    cerebro.run()

    # 绘制结果
    cerebro.plot(style='bar')


def parse_args():
    parser = argparse.ArgumentParser(
        description='Pandas 测试脚本')

    parser.add_argument('--noheaders', action='store_true', default=False,
                        required=False,
                        help='不使用头行')

    parser.add_argument('--noprint', action='store_true', default=False,
                        help='打印 dataframe')

    return parser.parse_args()


if __name__ == '__main__':
    runstrat()
##############################################################################
数据源参考#
AbstractDataBase#
数据行（Lines）:

close
low
high
open
volume
openinterest
datetime
参数（Params）:

dataname (None)
name ()
compression (1)
timeframe (5)
fromdate (None)
todate (None)
sessionstart (None)
sessionend (None)
filters ([])
tz (None)
tzinput (None)
qcheck (0.0)
calendar (None)
BacktraderCSVData#
解析用于测试的自定义 CSV 数据。

特定参数：

dataname: 要解析的文件名或类文件对象
数据行：

close
low
high
open
volume
openinterest
datetime
参数：

dataname (None)
name ()
compression (1)
timeframe (5)
fromdate (None)
todate (None)
sessionstart (None)
sessionend (None)
filters ([])
tz (None)
tzinput (None)
qcheck (0.0)
calendar (None)
headers (True)
separator (,)
CSVDataBase#
用于实现 CSV 数据源的基类。

该类负责打开文件、读取行并将其标记化。子类只需重写 _loadline(tokens) 方法。

数据行：

close
low
high
open
volume
openinterest
datetime
参数：

dataname (None)
name ()
compression (1)
timeframe (5)
fromdate (None)
todate (None)
sessionstart (None)
sessionend (None)
filters ([])
tz (None)
tzinput (None)
qcheck (0.0)
calendar (None)
headers (True)
separator (,)
Chainer#
用于链式连接数据的类。

数据行：

close
low
high
open
volume
openinterest
datetime
参数：

dataname (None)
name ()
compression (1)
timeframe (5)
fromdate (None)
todate (None)
sessionstart (None)
sessionend (None)
filters ([])
tz (None)
tzinput (None)
qcheck (0.0)
calendar (None)
DataClone#
数据行：

close
low
high
open
volume
openinterest
datetime
参数：

dataname (None)
name ()
compression (1)
timeframe (5)
fromdate (None)
todate (None)
sessionstart (None)
sessionend (None)
filters ([])
tz (None)
tzinput (None)
qcheck (0.0)
calendar (None)
DataFiller#
该类将使用基础数据源的信息填充数据中的空隙。

参数：

fill_price (def: None): 如果为 None，将使用上一条数据的收盘价；否则使用传递的值（例如 ‘NaN’）
fill_vol (def: NaN): 用于填充缺失数据的交易量
fill_oi (def: NaN): 用于填充缺失数据的未平仓合约量
数据行：

close
low
high
open
volume
openinterest
datetime
参数：

dataname (None)
name ()
compression (1)
timeframe (5)
fromdate (None)
todate (None)
sessionstart (None)
sessionend (None)
filters ([])
tz (None)
tzinput (None)
qcheck (0.0)
calendar (None)
fill_price (None)
fill_vol (nan)
fill_oi (nan)
DataFilter#
此类过滤给定数据源中的数据行。除了 DataBase 的标准参数外，它还接受 funcfilter 参数，该参数可以是任何可调用对象。

逻辑：

funcfilter 将与基础数据源一起调用
它可以是任何可调用对象
返回值 True：当前数据源的数据行值将被使用
返回值 False：当前数据源的数据行值将被丢弃
数据行：

close
low
high
open
volume
openinterest
datetime
参数：

dataname (None)
name ()
compression (1)
timeframe (5)
fromdate (None)
todate (None)
sessionstart (None)
sessionend (None)
filters ([])
tz (None)
tzinput (None)
qcheck (0.0)
calendar (None)
funcfilter (None)
GenericCSVData#
根据定义的参数解析 CSV 文件。

特定参数（或特定含义）：

dataname: 要解析的文件名或类文件对象
lines 参数（datetime, open, high …）取数值
值为 -1 表示 CSV 源中不存在该字段
如果 time 存在（参数 time >=0），源包含分开的日期和时间字段，将合并
参数：

nullvalue: 如果缺少值（CSV 字段为空），将使用的值
dtformat: 用于解析 datetime CSV 字段的格式。请参阅 python strptime/strftime 文档以了解格式。
如果指定了数值，它将按以下方式解释：
1: 值为代表自 1970 年 1 月 1 日以来的秒数的 Unix 时间戳（int 型）
2: 值为代表自 1970 年 1 月 1 日以来的秒数的 Unix 时间戳（float 型）
如果传递了一个可调用对象，它将接受一个字符串并返回一个 datetime.datetime 实例
tmformat: 用于解析 time CSV 字段的格式（如果存在）（time 字段默认不存在）
数据行：

close
low
high
open
volume
openinterest
datetime
参数：

dataname (None)
name ()
compression (1)
timeframe (5)
fromdate (None)
todate (None)
sessionstart (None)
sessionend (None)
filters ([])
tz (None)
tzinput (None)
qcheck (0.0)
calendar (None)
headers (True)
separator (,)
nullvalue (nan)
dtformat (%Y-%m-%d %H:%M:%S)
tmformat (%H:%M:%S)
datetime (0)
time (-1)
open (1)
high (2)
low (3)
close (4)
volume (5)
openinterest (6)
IBData#
交互式经纪商数据源（Interactive Brokers Data Feed）

支持参数 dataname 中的合约规格：

TICKER # 股票类型和 SMART 交易所
TICKER-STK # 股票和 SMART 交易所
TICKER-STK-EXCHANGE # 股票
TICKER-STK-EXCHANGE-CURRENCY # 股票
TICKER-CFD # CFD 和 SMART 交易所
TICKER-CFD-EXCHANGE # CFD
TICKER-CDF-EXCHANGE-CURRENCY # 股票
TICKER-IND-EXCHANGE # 指数
TICKER-IND-EXCHANGE-CURRENCY # 指数
TICKER-YYYYMM-EXCHANGE # 期货
TICKER-YYYYMM-EXCHANGE-CURRENCY # 期货
TICKER-YYYYMM-EXCHANGE-CURRENCY-MULT # 期货
TICKER-FUT-EXCHANGE-CURRENCY-YYYYMM-MULT # 期货
TICKER-YYYYMM-EXCHANGE-CURRENCY-STRIKE-RIGHT # 期权
TICKER-YYYYMM-EXCHANGE-CURRENCY-STRIKE-RIGHT-MULT # 期权
TICKER-FOP-EXCHANGE-CURRENCY-YYYYMM-STRIKE-RIGHT # 期权
TICKER-FOP-EXCHANGE-CURRENCY-YYYYMM-STRIKE-RIGHT-MULT # 期权
CUR1.CUR2-CASH-IDEALPRO # 外汇
TICKER-YYYYMMDD-EXCHANGE-CURRENCY-STRIKE-RIGHT # 期权
TICKER-YYYYMMDD-EXCHANGE-CURRENCY-STRIKE-RIGHT-MULT # 期权
TICKER-OPT-EXCHANGE-CURRENCY-YYYYMMDD-STRIKE-RIGHT # 期权
TICKER-OPT-EXCHANGE-CURRENCY-YYYYMMDD-STRIKE-RIGHT-MULT # 期权
参数：

sectype (默认: STK)
exchange (默认: SMART)
currency (默认: ‘’)
historical (默认: False)
what (默认: None)
rtbar (默认: False)
qcheck (默认: 0.5)
backfill_start (默认: True)
backfill (默认: True)
backfill_from (默认: None)

latethrough (默认: False)
tradename (默认: None)
数据行：

close
low
high
open
volume
openinterest
datetime
参数：

dataname (None)
name ()
compression (1)
timeframe (5)
fromdate (None)
todate (None)
sessionstart (None)
sessionend (None)
filters ([])
tz (None)
tzinput (None)
qcheck (0.5)
calendar (None)
sectype (STK)
exchange (SMART)
currency ()
rtbar (False)
historical (False)
what (None)
useRTH (False)
backfill_start (True)
backfill (True)
backfill_from (None)
latethrough (False)
tradename (None)
InfluxDB#
数据行：

close
low
high
open
volume
openinterest
datetime
参数：

dataname (None)
name ()
compression (1)
timeframe (5)
fromdate (None)
todate (None)
sessionstart (None)
sessionend (None)
filters ([])
tz (None)
tzinput (None)
qcheck (0.0)
calendar (None)
host (127.0.0.1)
port (8086)
username (None)
password (None)
database (None)
startdate (None)
high (high_p)
low (low_p)
open (open_p)
close (close_p)
volume (volume)
ointerest (oi)
MT4CSVData#
解析 Metatrader4 历史中心导出的 CSV 文件。

特定参数（或特定含义）：

dataname: 要解析的文件名或类文件对象
使用 GenericCSVData 并简单修改参数
数据行：

close
low
high
open
volume
openinterest
datetime
参数：

dataname (None)
name ()
compression (1)
timeframe (5)
fromdate (None)
todate (None)
sessionstart (None)
sessionend (None)
filters ([])
tz (None)
tzinput (None)
qcheck (0.0)
calendar (None)
headers (True)
separator (,)
nullvalue (nan)
dtformat (%Y.%m.%d)
tmformat (%H:%M)
datetime (0)
time (1)
open (2)
high (3)
low (4)
close (5)
volume (6)
openinterest (-1)
OandaData#
参数：

qcheck (默认: 0.5)
historical (默认: False)
backfill_start (默认: True)
backfill (默认: True)
backfill_from (默认: None)
bidask (默认: True)
useask (默认: False)
includeFirst (默认: True)
reconnect (默认: True)
reconnections (默认: -1)
reconntimeout (默认: 5.0)
支持的时间框架和压缩映射符合 OANDA API 开发者指南中的定义：

(TimeFrame.Seconds, 5): 'S5',
(TimeFrame.Seconds, 10): 'S10',
(TimeFrame.Seconds, 15): 'S15',
(TimeFrame.Seconds, 30): 'S30',
(TimeFrame.Minutes, 1): 'M1',
(TimeFrame.Minutes, 2): 'M3',
(TimeFrame.Minutes, 3): 'M3',
(TimeFrame.Minutes, 4): 'M4',
(TimeFrame.Minutes, 5): 'M5',
(TimeFrame.Minutes, 10): 'M10',
(TimeFrame.Minutes, 15): 'M15',
(TimeFrame.Minutes, 30): 'M30',
(TimeFrame.Minutes, 60): 'H1',
(TimeFrame.Minutes, 120): 'H2',
(TimeFrame.Minutes, 180): 'H3',
(TimeFrame.Minutes, 240): 'H4',
(TimeFrame.Minutes, 360): 'H6',
(TimeFrame.Minutes, 480): 'H8',
(TimeFrame.Days, 1): 'D',
(TimeFrame.Weeks, 1): 'W',
(TimeFrame.Months, 1): 'M',
数据行：

close
low
high
open
volume
openinterest
datetime
参数：

dataname (None)
name ()
compression (1)
timeframe (5)
fromdate (None)
todate (None)
sessionstart (None)
sessionend (None)
filters ([])
tz (None)
tzinput (None)
qcheck (0.5)
calendar (None)
historical (False)
backfill_start (True)
backfill (True)
backfill_from (None)
bidask (True)
useask (False)
includeFirst (True)
reconnect (True)
reconnections (-1)
reconntimeout (5.0)
PandasData#
使用 Pandas DataFrame 作为数据源。

参数：

nocase (默认: True) 列名匹配不区分大小写
数据行：

close
low
high
open
volume
openinterest
datetime
参数：

dataname (None)
name ()
compression (1)
timeframe (5)
fromdate (None)
todate (None)
sessionstart (None)
sessionend (None)
filters ([])
tz (None)
tzinput (None)
qcheck (0.0)
calendar (None)
nocase (True)
datetime (None)
open (-1)
high (-1)
low (-1)
close (-1)
volume (-1)
openinterest (-1)
PandasDirectData#
使用 Pandas DataFrame 作为数据源，直接迭代由 itertuples 返回的元组。

数据行：

close
low
high
open
volume
openinterest
datetime
参数：

dataname (None)
name ()
compression (1)
timeframe (5)
fromdate (None)
todate (None)
sessionstart (None)
sessionend (None)
filters ([])
tz (None)
tzinput (None)
qcheck (0.0)
calendar (None)
datetime (0)
open (1)
high (2)
low (3)
close (4)
volume (5)
openinterest (6)
Quandl#
直接从 Quandl 服务器下载数据。

特定参数（或特定含义）：

dataname: 要下载的代码（例如 ‘YHOO’）
baseurl: 服务器 URL
proxies: 指示下载时使用的代理的字典，例如 {‘http’: ‘http://myproxy.com’}
buffered: 如果为 True，整个 socket 连接将在解析前缓存在本地
reverse: Quandl 返回的值按降序排列（最新的在前）。如果为 True，请求将告诉 Quandl 以升序（最旧的在前）格式返回
adjclose: 是否使用股息/拆股调整后的收盘价，并根据它调整所有值
apikey: 如果需要，使用的 API 密钥
dataset: 标识要查询的数据集的字符串。默认为 WIKI
数据行：

close
low
high
open
volume
openinterest
datetime
参数：

dataname (None)
name ()
compression (1)
timeframe (5)
fromdate (None)
todate (None)
sessionstart (None)
sessionend (None)
filters ([])
tz (None)
tzinput (None)
qcheck (0.0)
calendar (None)
headers (True)
separator (,)
reverse (True)
adjclose (True)
round (False)
decimals (2)
baseurl (https://www.quandl.com/api/v3/datasets)
proxies ({})
buffered (True)
apikey (None)
dataset (WIKI)
QuandlCSV#
解析预先下载的 Quandl CSV 数据源（或如果符合 Quandl 格式，本地生成的 CSV 文件）。

特定参数：

dataname: 要解析的文件名或类文件对象
reverse (默认: False): 假设本地存储的文件在下载过程中已被反向
adjclose (默认: True): 是否使用股息/拆股调整后的收盘价，并根据它调整所有值
round (默认: False): 是否在调整收盘价后将值四舍五入到特定的小数位数
decimals (默认: 2): 要四舍五入的小数位数
数据行：#
close

low
high
open
volume
openinterest
datetime
参数：

dataname (None)
name ()
compression (1)
timeframe (5)
fromdate (None)
todate (None)
sessionstart (None)
sessionend (None)
filters ([])
tz (None)
tzinput (None)
qcheck (0.0)
calendar (None)
headers (True)
separator (,)
reverse (False)
adjclose (True)
round (False)
decimals (2)
RollOver#
在满足条件时切换到下一个期货合约。

参数：

checkdate (默认: None): 必须是具有以下签名的可调用对象：
checkdate(dt, d):
dt: datetime.datetime 对象
d: 当前活动期货的数据源
返回值：

True: 只要返回 True，就可以切换到下一个期货

False: 不能进行切换

checkcondition (默认: None): 注意：只有当 checkdate 返回 True 时才会调用此方法。如果为 None，将在内部评估为 True（执行切换）。否则，必须是具有以下签名的可调用对象：

checkcondition(d0, d1):
d0: 当前活动期货的数据源
d1: 下一个到期的数据源
返回值：

True: 切换到下一个期货
False: 不能进行切换
数据行：

close
low
high
open
volume
openinterest
datetime
参数：

dataname (None)
name ()
compression (1)
timeframe (5)
fromdate (None)
todate (None)
sessionstart (None)
sessionend (None)
filters ([])
tz (None)
tzinput (None)
qcheck (0.0)
calendar (None)
checkdate (None)
checkcondition (None)
SierraChartCSVData#
解析 SierraChart 导出的 CSV 文件。

特定参数（或特定含义）：

dataname: 要解析的文件名或类文件对象
数据行：

close
low
high
open
volume
openinterest
datetime
参数：

dataname (None)
name ()
compression (1)
timeframe (5)
fromdate (None)
todate (None)
sessionstart (None)
sessionend (None)
filters ([])
tz (None)
tzinput (None)
qcheck (0.0)
calendar (None)
headers (True)
separator (,)
nullvalue (nan)
dtformat (%Y/%m/%d)
tmformat (%H:%M:%S)
datetime (0)
time (-1)
open (1)
high (2)
low (3)
close (4)
volume (5)
openinterest (6)
VCData#
VisualChart 数据源。

参数：

qcheck (默认: 0.5): 唤醒的默认超时，以让重新采样器/重放器知道当前条形图可以检查是否应交付
historical (默认: False): 如果未提供 todate 参数（在基类中定义），如果设置为 True，将强制仅进行历史下载。如果提供了 todate 参数，则效果相同。
milliseconds (默认: True): Visual Chart 构建的条形图具有以下方面：HH:MM:59.999000。如果此参数为 True，将添加一毫秒以使其看起来像：HH:MM + 1:00.000000
tradename (默认: None): 连续期货不能交易，但非常适合数据跟踪。如果提供此参数，它将是当前期货的名称，即交易资产。例如：
001ES -> ES-Mini 连续期货作为 dataname 提供
ESU16 -> ES-Mini 2016-09。如果在 tradename 中提供，它将是交易资产。
usetimezones (默认: True): 对于大多数市场，Visual Chart 提供的时区信息允许将日期时间转换为市场时间（backtrader 选择的表示方法）。某些市场（096）需要特殊的内部覆盖和时区支持以显示为用户期望的市场时间。如果设置为 True，将尝试使用 pytz 进行时区转换（默认）。禁用它将删除时区使用（可能有助于减少负载）。
数据行：

close
low
high
open
volume
openinterest
datetime
参数：

dataname (None)
name ()
compression (1)
timeframe (5)
fromdate (None)
todate (None)
sessionstart (None)
sessionend (None)
filters ([])
tz (None)
tzinput (None)
qcheck (0.5)
calendar (None)
historical (False)
millisecond (True)
tradename (None)
usetimezones (True)
VChartCSVData#
解析 VisualChart 导出的 CSV 文件。

特定参数（或特定含义）：

dataname: 要解析的文件名或类文件对象
数据行：

close
low
high
open
volume
openinterest
datetime
参数：

dataname (None)
name ()
compression (1)
timeframe (5)
fromdate (None)
todate (None)
sessionstart (None)
sessionend (None)
filters ([])
tz (None)
tzinput (None)
qcheck (0.0)
calendar (None)
headers (True)
separator (,)
VChartData#
支持 Visual Chart 二进制磁盘文件的每日和日内格式。

注：

dataname: 文件名或打开的类文件对象
如果传递了一个类文件对象，将使用 timeframe 参数来确定实际的时间框架。否则将使用文件扩展名（.fd 表示每日，.min 表示日内）。

数据行：

close
low
high
open
volume
openinterest
datetime
参数：

dataname (None)
name ()
compression (1)
timeframe (5)
fromdate (None)
todate (None)
sessionstart (None)
sessionend (None)
filters ([])
tz (None)
tzinput (None)
qcheck (0.0)
calendar (None)
VChartFile#
支持 Visual Chart 二进制磁盘文件的每日和日内格式。

注：

dataname: Visual Chart 显示的市场代码。例如：015ES 表示 EuroStoxx 50 连续期货
数据行：

close
low
high
open
volume
openinterest
datetime
参数：

dataname (None)
name ()
compression (1)
timeframe (5)
fromdate (None)
todate (None)
sessionstart (None)
sessionend (None)
filters ([])
tz (None)
tzinput (None)
qcheck (0.0)
calendar (None)
YahooFinanceCSVData#
解析预先下载的 Yahoo CSV 数据源（或符合 Yahoo 格式的本地生成的 CSV 文件）。

特定参数：

dataname: 要解析的文件名或类文件对象
reverse (默认: False): 假设本地存储的文件在下载过程中已被反向
adjclose (默认: True): 是否使用股息/拆股调整后的收盘价，并根据它调整所有值
adjvolume (默认: True): 如果 adjclose 也为 True，则也调整交易量
round (默认: True): 是否在调整收盘价后将值四舍五入到特定的小数位数
roundvolume (默认: 0): 在调整后将交易量四舍五入到给定的小数位数
decimals (默认: 2): 要四舍五入的小数位数
swapcloses (默认: False): [2018-11-16] 看起来关闭和调整后的关闭的顺序现在是固定的。保留该参数，以防需要再次交换列的顺序。
数据行：

close
low
high
open
volume
openinterest
datetime
adjclose
参数：

dataname (None)
name ()
compression (1)
timeframe (5)
fromdate (None)
todate (None)
sessionstart (None)
sessionend (None)
filters ([])
tz (None)
tzinput (None)
qcheck (0.0)
calendar (None)
headers (True)
separator (,)
reverse (False)
adjclose (True)
adjvolume (True)
round (True)
decimals (2)
roundvolume (False)
swapcloses (False
)

YahooFinanceData#
直接从 Yahoo 服务器下载数据。

特定参数（或特定含义）：

dataname: 要下载的代码（例如 ‘YHOO’ 表示 Yahoo 自己的股票报价）
proxies: 指示下载时使用的代理的字典，例如 {‘http’: ‘http://myproxy.com’} 或 {‘http’: ‘http://127.0.0.1:8080’}
period: 要下载数据的时间框架。传递 ‘w’ 表示每周，’m’ 表示每月。
reverse: [2018-11-16] Yahoo 在线下载的最新版本返回的数据顺序正确。因此，在线下载的默认值为 False。
adjclose: 是否使用股息/拆股调整后的收盘价，并根据它调整所有值
urlhist: Yahoo Finance 中的历史报价 URL，用于获取下载的面包授权 cookie
urldown: 实际下载服务器的 URL
retries: 获取面包 cookie 和下载数据的次数
数据行：

close
low
high
open
volume
openinterest
datetime
adjclose
参数：

dataname (None)
name ()
compression (1)
timeframe (5)
fromdate (None)
todate (None)
sessionstart (None)
sessionend (None)
filters ([])
tz (None)
tzinput (None)
qcheck (0.0)
calendar (None)
headers (True)
separator (,)
reverse (False)
adjclose (True)
adjvolume (True)
round (True)
decimals (2)
roundvolume (False)
swapcloses (False)
proxies ({})
period (d)
urlhist (https://finance.yahoo.com/quote/{}/history)
urldown (https://query1.finance.yahoo.com/v7/finance/download)
retries (3)
YahooLegacyCSV#
此类旨在加载 Yahoo 在 2017 年 5 月停止提供原始服务之前下载的文件。

数据行：

close
low
high
open
volume
openinterest
datetime
adjclose
参数：

dataname (None)
name ()
compression (1)
timeframe (5)
fromdate (None)
todate (None)
sessionstart (None)
sessionend (None)
filters ([])
tz (None)
tzinput (None)
qcheck (0.0)
calendar (None)
headers (True)
separator (,)
reverse (False)
adjclose (True)
adjvolume (True)
round (True)
decimals (2)
roundvolume (False)
swapcloses (False)
version ()

27 37Strategy.txt ##################################################
文件路径: 37Strategy.txt
================================================================================

Strategy#
在 backtrader 中，Cerebro 实例是整个系统的核心，而 Strategy 是用户的核心。

Strategy 的生命周期方法#
注意, 策略可以在创建时通过抛出 StrategySkipError 异常来中断，该异常来自 backtrader.errors 模块。这将避免在回测期间处理该策略。请参阅“异常”部分。

构建：__init__#
这是在实例化期间调用的：指标将在此处创建以及其他需要的属性。

示例代码：

def __init__(self):
    self.sma = btind.SimpleMovingAverage(period=15)
启动：start#
Cerebro 实例通知策略是时候开始运行了。存在一个默认的空方法。

初期：prenext#
在创建期间声明的指标将对策略的成熟期施加限制：这称为最小周期。上面的 __init__ 创建了一个周期为 15 的简单移动平均线 (SMA)。

只要系统看到的 bar 少于 15 个，就会调用 prenext（默认实现为空操作）。

成熟：next#
一旦系统看到 15 个 bar 并且 SMA 有足够的缓冲区开始生成值，策略就足够成熟可以真正执行。

存在一个 nextstart 方法，会在从 prenext 切换到 next 时调用一次。nextstart 的默认实现是简单地调用 next。

繁衍：无#
策略实际上不会繁衍，但从某种意义上来说，它们会，因为系统会在优化时实例化它们多次（使用不同的参数）。

结束：stop#
系统通知策略是时候重置并整理一切了。存在一个默认的空方法。

通常情况下和常规使用模式下，这看起来像这样：

class MyStrategy(bt.Strategy):

    def __init__(self):
        self.sma = btind.SimpleMovingAverage(period=15)

    def next(self):
        if self.sma > self.data.close:
            # 执行某些操作
            pass
        elif self.sma < self.data.close:
            # 执行其他操作
            pass
在这个代码片段中：

在 __init__ 中分配一个指标给属性
默认的空 start 方法未被重写
prenext 和 nextstart 未被重写
在 next 中，指标的值与收盘价进行比较，以执行某些操作
默认的空 stop 方法未被重写
策略事件通知#
策略将每个 next 周期收到通知：

notify_order#
通过 notify_order(order) 接收任何订单状态的变化通知。

notify_trade#
通过 notify_trade(trade) 接收任何交易的开启/更新/关闭通知

notify_cashvalue#
通过 notify_cashvalue(cash, value) 接收经纪账户中的当前现金和投资组合

notify_fund#
通过 notify_fund(cash, value, fundvalue, shares) 接收经纪账户中的当前现金、投资组合、基金价值和份额

notify_store#
通过 notify_store(msg, *args, **kwargs) 接收来自存储提供者的通知

如何买入/卖出/平仓#
buy 和 sell 方法生成订单。调用这些方法时，它们返回一个 Order（或其子类）实例，该实例可用作引用。此订单具有唯一的 ref 标识符，可用于比较。

注意，特定经纪实现的 Order 子类可能携带经纪提供的其他唯一标识符。

要创建订单，请使用以下参数：

参数名	默认值	描述
data	None	创建订单的数据。如果为 None，则使用系统中的第一个数据 self.datas[0] 或 self.data0（即 self.data）。
size	None	要使用的订单数量（正值）。如果为 None，则使用通过 getsizer 检索到的 sizer 实例来确定大小。
price	None）	使用的价格（实时经纪可能对格式有最低价格步长要求）。对于市场和收盘订单（Market 和 Close orders）为 None（市场决定价格）。对于限价、止损和止损限价订单，这个值决定触发点。
plimit	None	仅适用于止损限价订单。这是在触发止损后设置隐含限价订单的价格（使用 price）。
exectype	None	可能的值：
- Order.Market 或 None：市场订单将以下一个可用价格执行。在回测中，将是下一个 bar 的开盘价。
- Order.Limit：订单只能以给定价格或更好价格执行。
- Order.Stop：订单在 price 触发时被触发，并像 Order.Market 订单一样执行。
- Order.StopLimit：订单在 price 触发时被触发，并作为隐含的限价订单执行，限价由 pricelimit 给出。
valid	None	可能的值：
- None：生成一个不会过期的订单（即 Good til cancel），并保留在市场上直到匹配或取消。实际上，经纪通常会施加一个时间限制，但通常远远在未来，可以认为它不会过期。
- datetime.datetime 或 datetime.date 实例：日期将用于生成有效期至给定日期的订单（即 good til date）。
- Order.DAY 或 0 或 timedelta()：生成一个有效期至交易日结束的订单（即日订单）。
- 数值：假定为 matplotlib 编码的 datetime 值（backtrader 使用的），将用于生成有效期至该时间的订单（即 good til date）。
tradeid	0	backtrader 用于跟踪同一资产上重叠交易的内部值。当通知订单状态变化时，此 tradeid 会发送回策略。
示例：如果 backtrader 直接支持的 4 种订单执行类型不够，可以为 Interactive Brokers 传递以下参数：

orderType='LIT', lmtPrice=10.0, auxPrice=9.8
这将覆盖 backtrader 创建的设置，并生成一个 LIMIT IF TOUCHED 订单，触及价格为 9.8，限价为 10.0。

策略信息：#
属性名	描述
env	策略所属的 cerebro 实体
datas	传递给 cerebro 的数据源数组
data/data0	datas[0] 的别名
dataX	datas[X] 的别名
dnames	按名称访问数据源的替代方法（通过 [name] 或 .name 语法）
broker	与此策略关联的经纪（从 cerebro 接收）
stats	包含 cerebro 为此策略创建的观察者的列表/命名元组序列
analyzers	包含 cerebro 为此策略创建的分析器的列表/命名元组序列
position	获取 data0 的当前仓位的属性
成员属性（用于统计/观察者/分析器）：#
属性名	描述
_orderspending	将在调用 next 之前通知策略的订单列表
_tradespending	将在调用 next 之前通知策略的交易列表
_orders	已经通知的订单列表。订单可以在列表中多次出现，具有不同的状态和执行部分。列表旨在保留历史记录。
_trades：	已经通知的交易列表。交易可以像订单一样多次出现在列表中。
注意： prenext、nextstart 和 next 可以针对同一时间点多次调用（例如，当使用每日时间框架时，价格更新每日 bar 的 ticks）。

策略参考#
class backtrader.Strategy(*args, **kwargs)

基类，用于子类化用户定义的策略。

方法#
方法名	描述
next()	当所有数据/指标的最小周期满足时，将为所有剩余数据点调用此方法。
nextstart()	当所有数据/指标的最小周期满足时，将调用一次此方法。默认行为是调用 next。
prenext()	在满足所有数据/指标的最小周期之前调用此方法。
start()	在回测即将开始之前调用。
stop()	在回测即将结束之前调用。
notify_order(order)	当订单状态变化时接收通知。
notify_trade(trade)	当交易状态变化时接收通知。
notify_cashvalue(cash, value)	接收策略经纪账户的当前资金和投资组合状态。
notify_fund(cash, value, fundvalue, shares)	接收当前现金、投资组合、基金价值和份额。
notify_store(msg, *args, **kwargs)	接收存储提供者的通知。
订单方法#
方法名	描述
buy(...)	创建买入订单并发送给经纪。
sell(...)	创建卖出（空头）订单并发送给经纪。
close(...)：	关闭现有仓位。
cancel(order)	取消经纪中的订单。
其他方法#
方法名	描述
buy_bracket(...)	创建括号订单组（低侧 - 买入订单 - 高侧）。
sell_bracket(...)	创建括号订单组（低侧 - 卖出订单 - 高侧）。
order_target_size(...)	下订单将仓位重新平衡为目标大小。
order_target_value(...)	下订单将仓位重新平衡为目标价值。
order_target_percent(...)	下订单将仓位重新平衡为当前投资组合价值的目标百分比。
getsizer()	返回用于自动计算头寸的 sizer。
setsizer(sizer)	替换默认的 sizer。
getsizing(data=None, isbuy=True)	返回 sizer 实例为当前情况计算的头寸。
getpositionbyname(name=None, broker=None)	按名称返回给定经纪的当前仓位。
getposition(data=None, broker=None)	返回给定数据和经纪的当前仓位。
getpositionsbyname(broker=None)	直接从经纪获取按名称的所有仓位。
getdatanames()	返回现有数据名称的列表。
getdatabyname(name)	使用环境（cerebro）按名称返回给定数据。
add_timer(...)	计划一个计时器以调用指定的回调或策略的 notify_timer。
notify_timer(timer, when, *args, **kwargs)	接收计时器通知，其中 timer 是由 add_timer 返回的计时器，when 是调用时间。args 和 kwargs 是传递给 add_timer 的额外参数。
###########################################################################################################
信号策略#
使用 backtrader 进行操作不一定非得编写一个策略类。虽然这是首选方式，但由于对象层次结构的原因，使用信号也是可行的。

快速总结：#
不需要编写策略类、实例化指标、编写买卖逻辑等。
添加信号（无论如何也是指标），其余部分在后台完成。
快速示例：#
import backtrader as bt

data = bt.feeds.OneOfTheFeeds(dataname='mydataname')
cerebro.adddata(data)

cerebro.add_signal(bt.SIGNAL_LONGSHORT, MySignal)
cerebro.run()
这就完成了。当然，信号本身还没有定义。

让我们定义一个非常简单的信号：

如果收盘价高于简单移动平均线 (SMA)，则发出多头信号。
如果收盘价低于 SMA，则发出空头信号。
定义如下：

class MySignal(bt.Indicator):
    lines = ('signal',)
    params = (('period', 30),)

    def __init__(self):
        self.lines.signal = self.data - bt.indicators.SMA(period=self.p.period)
现在真的完成了。

当运行 run 时，Cerebro 会处理实例化一个特殊的策略实例，它知道如何处理这些信号。

常见问题#
买卖操作的数量是如何确定的？

Cerebro 实例自动为策略添加一个固定大小 (FixedSize) 的定量器。最终用户可以通过 cerebro.addsizer 更改定量器以改变策略。

订单是如何执行的？

执行类型为市价单，订单的有效期为“直到取消” (Good Until Canceled)。

信号细节#
从技术和理论角度来看，可以描述为：

一个可调用对象，当被调用时返回另一个对象（只调用一次）。
在大多数情况下，这是一个类的实例化，但不一定非得是。
支持 __getitem__ 接口。唯一请求的键/索引将是 0。
从实际角度来看，信号是：

来自 backtrader 生态系统的 lines 对象，主要是指标。
这在使用其他指标时很有帮助，比如示例中的简单移动平均线。

信号指示#
信号在使用 signal[0] 查询时提供指示，含义如下：

> 0 -> 多头指示
< 0 -> 空头指示
== 0 -> 无指示
示例中，简单地用 self.data - SMA 进行算术运算：

当数据高于 SMA 时发出多头指示。
当数据低于 SMA 时发出空头指示。
注意，当未为数据指示特定价格字段时，默认参考价格为收盘价。

信号类型#
如下示例中的常量，直接从主 backtrader 模块获取：

import backtrader as bt

bt.SIGNAL_LONG
有 5 种类型的信号，分为 2 组。

主要组#
LONGSHORT：接受来自该信号的多头和空头指示。

LONG：

接受多头指示进行做多。

接受空头指示平仓多头。但：

如果系统中有 LONGEXIT 信号，将用它来平仓多头。
如果有 SHORT 信号且没有 LONGEXIT 信号，它将被用来平仓多头再开空头。
SHORT：

接受空头指示进行做空。 接受多头指示平仓空头。但：

如果系统中有 SHORTEXIT 信号，将用它来平仓空头。
如果有 LONG 信号且没有 SHORTEXIT 信号，它将被用来平仓空头再开多头。
退出组#
这两个信号旨在覆盖其他信号，并为平仓提供标准。

LONGEXIT：接受空头指示平仓多头。
SHORTEXIT：接受多头指示平仓空头。
累积和订单并发#
上面展示的示例信号会不断发出多头和空头指示，因为它只是简单地用收盘价减去 SMA 值，这总是会得到 > 0 或 < 0 的结果（0 在数学上是可能的，但实际发生的可能性很小）。

这将导致连续生成订单，从而产生两种情况：

累积：即使已经在市场中，信号也会产生新订单，增加市场仓位。
并发：在其他订单执行之前会生成新订单。
为了避免这种情况，默认行为是：

不累积。
不允许并发。
如果需要其中任何一种行为，可以通过 Cerebro 控制：

cerebro.signal_accumulate(True)  # 或 False 禁用
cerebro.signal_concurrency(True)  # 或 False 禁用
示例#
backtrader 源代码包含一个测试功能的示例。

主要信号如下：

class SMACloseSignal(bt.Indicator):
    lines = ('signal',)
    params = (('period', 30),)

    def __init__(self):
        self.lines.signal = self.data - bt.indicators.SMA(period=self.p.period)
如果指定了退出信号，代码如下：

class SMAExitSignal(bt.Indicator):
    lines = ('signal',)
    params = (('p1', 5), ('p2', 30),)

    def __init__(self):
        sma1 = bt.indicators.SMA(period=self.p.p1)
        sma2 = bt.indicators.SMA(period=self.p.p2)
        self.lines.signal = sma1 - sma2
第一次运行：多头和空头

$ ./signals-strategy.py --plot --signal longshort
输出：

信号被绘制。因为它只是一个指标，所以适用绘图规则。
策略确实做多和做空。因为现金水平从未回到价值水平。
第二次运行：仅多头

$ ./signals-strategy.py --plot --signal longonly
输出：

现金水平在每次卖出后回到价值水平，说明策略在市场之外。
第三次运行：仅空头

$ ./signals-strategy.py --plot --signal shortonly
输出：

第一次操作是卖出，发生在收盘价低于 SMA 且简单减法得到负值之后。
现金水平在每次买入后回到价值水平，说明策略在市场之外。
第四次运行：多头 + 多头退出

$ ./signals-strategy.py --plot --signal longonly --exitsignal longexit
输出：

许多交易是相同的，但一些较早被中断，因为退出信号中的快速移动平均线向下穿过慢速移动平均线。
系统显示其仅做多特性，每笔交易结束时现金成为价值。
使用方法#
$ ./signals-strategy.py --help
完整示例#
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse
import collections
import datetime

import backtrader as bt

MAINSIGNALS = collections.OrderedDict(
    (('longshort', bt.SIGNAL_LONGSHORT),
     ('longonly', bt.SIGNAL_LONG),
     ('shortonly', bt.SIGNAL_SHORT),)
)


EXITSIGNALS = {
    'longexit': bt.SIGNAL_LONGEXIT,
    'shortexit': bt.SIGNAL_LONGEXIT,
}


class SMACloseSignal(bt.Indicator):
    lines = ('signal',)
    params = (('period', 30),)

    def __init__(self):
        self.lines.signal = self.data - bt.indicators.SMA(period=self.p.period)


class SMAExitSignal(bt.Indicator):
    lines = ('signal',)
    params = (('p1', 5), ('p2', 30),)

    def __init__(self):
        sma1 = bt.indicators.SMA(period=self.p.p1)
        sma2 = bt.indicators.SMA(period=self.p.p2)
        self.lines.signal = sma1 - sma2


def runstrat(args=None):
    args = parse_args(args)

    cerebro = bt.Cerebro()
    cerebro.broker.set_cash(args.cash)

    dkwargs = dict()
    if args.fromdate is not None:
        fromdate = datetime.datetime.strptime(args.fromdate, '%Y-%m-%d')
        dkwargs['fromdate'] = fromdate

    if args.todate is not None:
        todate = datetime.datetime.strptime(args.todate, '%Y-%m-%d')
        dkwargs['todate'] = todate

    data = bt.feeds.BacktraderCSVData(dataname=args.data, **dkwargs)
    cerebro.adddata(data)

    cerebro.add_signal(MAINSIGNALS[args.signal],
                       SMACloseSignal, period=args.smaperiod)

    if args.ex

itsignal is not None:
        cerebro.add_signal(EXITSIGNALS[args.exitsignal],
                           SMAExitSignal,
                           p1=args.exitperiod,
                           p2=args.smaperiod)

    cerebro.run()
    if args.plot:
        pkwargs = dict(style='bar')
        if args.plot is not True:
            npkwargs = eval('dict(' + args.plot + ')')
            pkwargs.update(npkwargs)

        cerebro.plot(**pkwargs)


def parse_args(pargs=None):

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Sample for Signal concepts')

    parser.add_argument('--data', required=False,
                        default='../../datas/2005-2006-day-001.txt',
                        help='Specific data to be read in')

    parser.add_argument('--fromdate', required=False, default=None,
                        help='Starting date in YYYY-MM-DD format')

    parser.add_argument('--todate', required=False, default=None,
                        help='Ending date in YYYY-MM-DD format')

    parser.add_argument('--cash', required=False, action='store',
                        type=float, default=50000,
                        help=('Cash to start with'))

    parser.add_argument('--smaperiod', required=False, action='store',
                        type=int, default=30,
                        help=('Period for the moving average'))

    parser.add_argument('--exitperiod', required=False, action='store',
                        type=int, default=5,
                        help=('Period for the exit control SMA'))

    parser.add_argument('--signal', required=False, action='store',
                        default=MAINSIGNALS.keys()[0], choices=MAINSIGNALS,
                        help=('Signal type to use for the main signal'))

    parser.add_argument('--exitsignal', required=False, action='store',
                        default=None, choices=EXITSIGNALS,
                        help=('Signal type to use for the exit signal'))

    parser.add_argument('--plot', '-p', nargs='?', required=False,
                        metavar='kwargs', const=True,
                        help=('Plot the read data applying any kwargs passed\n'
                              '\n'
                              'For example:\n'
                              '\n'
                              '  --plot style="candle" (to plot candles)\n'))

    if pargs is not None:
        return parser.parse_args(pargs)

    return parser.parse_args()


if __name__ == '__main__':
    runstrat()
#################################################################################################
策略参考#
内置策略参考#
MA_CrossOver#
别名：SMA_CrossOver，这是一个仅做多的策略，基于移动平均线交叉操作。

交易规则#
买入逻辑： 如果无持仓，fast 移动平均线向上穿过 slow 移动平均线。

卖出逻辑： 有持仓时，fast 移动平均线向下穿过 slow 移动平均线。

订单类型： 市价单

参数：

fast (10)，_movav (<class ‘backtrader.indicators.sma.SMA’>)
slow (30)，_movav (<class ‘backtrader.indicators.sma.SMA’>)
SignalStrategy#
此策略的子类旨在使用信号自动操作。信号通常是指标，预期输出值为：

> 0 表示多头指示
< 0 表示空头指示
信号分为两组，共有 5 种类型。

主要组：

LONGSHORT：接受来自该信号的多头和空头指示。
LONG：
接受多头指示进行做多。
接受空头指示平仓多头。但：
如果系统中有 LONGEXIT 信号，将用它来平仓多头。
如果有 SHORT 信号且没有 LONGEXIT 信号，它将被用来平仓多头再开空头。
SHORT：
接受空头指示进行做空。
接受多头指示平仓空头。但：
如果系统中有 SHORTEXIT 信号，将用它来平仓空头。
如果有 LONG 信号且没有 SHORTEXIT 信号，它将被用来平仓空头再开多头。
退出组：

这两个信号旨在覆盖其他信号，并为平仓提供标准。

LONGEXIT：接受空头指示平仓多头。
SHORTEXIT：接受多头指示平仓空头。
订单发出：

订单执行类型为市价单，有效期为“直到取消” (Good until Canceled)。
参数：

signals (默认值: []): 允许实例化信号并分配到正确类型的列表/元组。
_accumulate (默认值: False): 允许进入市场（多头/空头），即使已经在市场中。
_concurrent (默认值: False): 允许在已有待执行订单时发出新订单。
_data (默认值: None): 如果系统中存在多个数据，目标数据是哪一个。这可以是：
None: 将使用系统中的第一个数据。
int: 表示在该位置插入的数据。
str: 创建数据时给定的名称（参数 name），或通过 cerebro.adddata(…, name=) 添加时给定的名称。
数据实例。
线：

datetime
参数：

signals ([])
_accumulate (False)
_concurrent (False)
_data (None)
###################################################################################################################
使用指标#
指标可以在平台中的两个地方使用：

策略内部
其他指标内部
指标在操作中的使用#
在策略中，指标总是在 __init__ 中实例化。在 next 中使用/检查指标值（或派生值）。有一个重要的公理需要考虑：在 __init__ 中声明的任何指标（或派生值）将在调用 next 之前预先计算。

让我们了解操作模式的差异。

__init__ vs next#
在 __init__ 中涉及到线条对象的任何操作都会生成另一个线条对象。在 next 中涉及到线条对象的任何操作都会生成常规的 Python 类型，如浮点数和布尔值。

如 __init__ 中的一个操作：

hilo_diff = self.data.high - self.data.low
变量 hilo_diff 持有一个线条对象的引用，该对象在调用 next 之前预先计算，可以使用标准数组表示法 [] 访问。

它显然包含了数据源中每个条的高低差值。

这在混合简单线条（如 self.data 数据源中的线条）和复杂线条（如指标）时也有效：

sma = bt.SimpleMovingAverage(self.data.close)
close_sma_diff = self.data.close - sma
现在 close_sma_diff 再次包含一个线条对象。

使用逻辑运算符：

close_over_sma = self.data.close > sma
现在生成的线条对象将包含一个布尔数组。

在 next 中，一个操作（逻辑运算符）：

close_over_sma = self.data.close > self.sma
使用等效数组（基于索引 0 的表示法）：

close_over_sma = self.data.close[0] > self.sma[0]
在这种情况下，close_over_sma 生成一个布尔值，这是比较两个浮点值的结果，这些值由应用于 self.data.close 和 self.sma 的 [0] 运算符返回。

为什么选择 __init__ vs next#
逻辑简化（以及易用性）是关键。可以在 __init__ 中声明计算和大部分相关逻辑，将实际操作逻辑保持在 next 中的最小化。

实际上还有一个附带好处：速度（由于开始时的预计算）。

一个完整的示例，在 __init__ 中生成一个买入信号：

class MyStrategy(bt.Strategy):

    def __init__(self):
        sma1 = btind.SimpleMovingAverage(self.data)
        ema1 = btind.ExponentialMovingAverage()

        close_over_sma = self.data.close > sma1
        close_over_ema = self.data.close > ema1
        sma_ema_diff = sma1 - ema1

        buy_sig = bt.And(close_over_sma, close_over_ema, sma_ema_diff > 0)

    def next(self):
        if buy_sig:
            self.buy()
注意： Python 的 and 运算符无法被重载，迫使平台定义其自己的 And。同样适用于其他构造如 Or 和 If。

显然，“声明式”方法在 __init__ 期间保持 next（实际策略工作发生的地方）的膨胀最小化。不要忘记，这也有一个加速因素。

注意： 当逻辑变得非常复杂并涉及多个操作时，通常最好将其封装在一个指标内。

一些注意事项#
在上述示例中，与其他平台相比，backtrader 已简化了两件事：

声明的指标既不获取父参数（如它们被创建的策略），也没有调用任何类型的“注册”方法/函数。尽管如此，策略会触发指标和任何因操作生成的线条对象的计算（如 sma - ema）。

ExponentialMovingAverage 实例化时没有传入 self.data。这是故意的。如果没有传入数据，父（在本例中是创建它的策略）的第一个数据将在后台自动传递。

指标绘图#
首先也是最重要的：声明的指标会自动绘制（如果调用了 cerebro.plot）。操作生成的线条对象不会绘制（如 close_over_sma = self.data.close > self.sma）。

有一个辅助的 LinePlotterIndicator 可以绘制这些操作，如果需要可以使用以下方法：

close_over_sma = self.data.close > self.sma
LinePlotterIndicator(close_over_sma, name='Close_over_SMA')
name 参数为此指标持有的单行命名。

控制绘图#
在开发指标期间，可以添加一个 plotinfo 声明。它可以是一个包含两元素的元组的元组、一个字典或一个有序字典。看起来像这样：

class MyIndicator(bt.Indicator):
    ...
    plotinfo = dict(subplot=False)
    ...
稍后可以访问（并设置）该值（如果需要）：

myind = MyIndicator(self.data, someparam=value)
myind.plotinfo.subplot = True
甚至可以在实例化期间设置该值：

myind = MyIndicator(self.data, someparams=value, subplot=True)
subplot=True 将传递给指标的（在幕后实例化的）成员变量 plotinfo。

plotinfo 提供以下参数来控制绘图行为：

参数名	默认值	描述
plot	True	是否绘制指标。
subplot	True	是否在不同窗口中绘制指标。对于移动平均线等指标，默认值更改为 False。
plotname	''	设置绘图中显示的名称。空值表示将使用指标的规范名称（class.name）。这有一些限制，因为 Python 标识符不能使用算术运算符等。例如，指标 DI+ 将声明如下： plotinfo = dict(plotname='DI+')。
plotabove	False	指标通常绘制在其操作的数据下方。将其设置为 True 会使指标绘制在数据上方。
plotlinelabels	False	适用于“指标”上的“指标”。如果计算 RSI 的简单移动平均线，绘图通常会显示“SimpleMovingAverage”的名称。这是“指标”的名称，而不是实际绘制的线条的名称。如果将值设置为 True，将使用简单移动平均线内线条的实际名称。
plotymargin	0.0	在指标顶部和底部留出的边距量（0.15 -> 15%）。有时 matplotlib 绘图会超出轴的顶部/底部，可能需要一个边距。
plotyticks	[]	用于控制绘制的 y 轴刻度。如果传递一个空列表，将自动计算“y 刻度”。对于像随机指标这样的东西，设置为已知的行业标准可能有意义：[20.0, 50.0, 80.0]。某些指标提供 upperband 和 lowerband 等参数，实际上用于操纵 y 刻度。
plothlines	[]	用于控制沿指标轴绘制的水平线。如果传递一个空列表，则不会绘制水平线。对于像随机指标这样的东西，绘制已知的行业标准线可能有意义：[20.0, 80.0]。某些指标提供 upperband 和 lowerband 等参数，实际上用于操纵水平线。
plotyhlines	[]	用于同时控制 plotyticks 和 plothlines，使用一个单一参数。
plotforce	False	如果由于某种原因您认为某个指标应该绘制但未绘制……请最后设置为 True。
#####################################################################################################
指标开发#
如果需要开发任何内容（除了一个或多个获胜策略），这个内容就是自定义指标。在平台内开发此类内容很容易。

开发要点：

从 Indicator 类（直接或从现有子类）派生一个类；
定义它将包含的 Line；
一个指标至少要有一条线。如果从现有的类派生，线条可能已经定义好了
可选地定义可以改变行为的参数
可选地提供/自定义一些用于合理绘制指标的元素
在 __init__ 中提供一个完全定义的操作，并绑定（分配）到指标的线条，或者提供 next 方法和（可选的）once 方法
如果一个指标可以在初始化期间通过逻辑/算术操作完全定义，且结果分配给线条：完成。如果情况不是这样，至少要提供一个 next 方法，其中指标必须在索引 0 处分配一个值给线条。可以通过提供 once 方法来优化运行一次模式（批处理操作）的计算。

重要说明：幂等性#
指标为每个接收到的条生成一个输出。不能假设同一个条会被发送多少次。操作必须是幂等的。

其背后的理由：

同一个条（索引-wise）可以多次发送，并且值会变化（即变化的值是收盘价）
这使得可以“重放”一个日内会话，但使用由 5 分钟条组成的日内数据。
这也允许平台从实时数据源获取值。

一个简单（但功能齐全）的指标#
可以这样：

class DummyInd(bt.Indicator):
    lines = ('dummyline',)

    params = (('value', 5),)

    def __init__(self):
        self.lines.dummyline = bt.Max(0.0, self.params.value)
完成！

该指标将始终输出相同的值：要么是 0.0，要么是 self.params.value（如果它恰好大于 0.0）。

使用 next 方法的相同指标：

class DummyInd(bt.Indicator):
    lines = ('dummyline',)

    params = (('value', 5),)

    def next(self):
        self.lines.dummyline[0] = max(0.0, self.params.value)
完成！相同行为。

注意： 请注意在 __init__ 版本中，使用 bt.Max 将值分配给线条对象 self.lines.dummyline。 bt.Max 返回一个线条对象，它会为传递给指标的每个条自动迭代。如果使用 max，赋值将毫无意义，因为指标将有一个固定值的成员变量，而不是线条。在 next 期间，直接使用浮点值进行工作，可以使用标准的 max 内置函数。

回顾一下，self.lines.dummyline 是长表示法，可以缩短为：

self.l.dummyline
甚至可以缩短为：

self.dummyline
只有在代码没有用成员属性遮蔽这个变量时，后者才有可能。

第三个也是最后一个版本提供了一个额外的 once 方法来优化计算：

class DummyInd(bt.Indicator):
    lines = ('dummyline',)

    params = (('value', 5),)

    def next(self):
        self.lines.dummyline[0] = max(0.0, self.params.value)

    def once(self, start, end):
        dummy_array = self.lines.dummyline.array

        for i in range(start, end):
            dummy_array[i] = max(0.0, self.params.value)
更有效，但开发 once 方法迫使深入研究。实际上，已经深入到内部。

__init__ 版本无论如何都是最好的：

所有内容都限制在初始化期间
自动提供 next 和 once（都已优化，因为 bt.Max 已经有它们），无需处理索引和/或公式
如果需要开发，指标也可以覆盖与 next 和 once 相关的方法：

prenext 和 nextstart
preonce 和 oncestart
手动/自动最小周期#
如果可能，平台将计算它，但可能需要手动操作。

以下是一个简单移动平均线的实现：

class SimpleMovingAverage1(Indicator):
    lines = ('sma',)
    params = (('period', 20),)

    def next(self):
        datasum = math.fsum(self.data.get(size=self.p.period))
        self.lines.sma[0] = datasum / self.p.period
虽然看起来合理，但平台不知道最小周期是什么，即使参数被命名为“period”（名称可能具有误导性，一些指标接收多个“period”，它们有不同的用途）。

在这种情况下，next 将在第一个条已经进入系统时被调用，并且所有事情都会爆炸，因为 get 不能返回所需的 self.p.period。

在解决情况前，需要考虑：

传递给指标的数据源可能已经携带最小周期。示例 SimpleMovingAverage 可以在以下情况下进行：

常规数据源：默认最小周期为 1（只等待进入系统的第一个条）。
另一个移动平均线：它已经有一个周期。如果是 20，再次我们的示例移动平均线也是 20，我们最终得到的最小周期是 40 条。
实际上，内部计算说是 39……因为一旦第一个移动平均线生成了一个条，这个条将计入下一个移动平均线，这就创建了一个重叠条，因此需要 39。其他指标/对象也携带周期。

缓解情况如下：

class SimpleMovingAverage1(Indicator):
    lines = ('sma',)
    params = (('period', 20),)

    def __init__(self):
        self.addminperiod(self.params.period)

    def next(self):
        datasum = math.fsum(self.data.get(size=self.p.period))
        self.lines.sma[0] = datasum / self.p.period
addminperiod 方法告诉系统考虑该指标所需的额外周期条，无论现有的最小周期是什么。有时这完全不需要，如果所有计算都使用已经向系统传达其周期需求的对象。

一个快速的 MACD 实现带有直方图：

from backtrader.indicators import EMA

class MACD(Indicator):
    lines = ('macd', 'signal', 'histo',)
    params = (('period_me1', 12), ('period_me2', 26), ('period_signal', 9),)

    def __init__(self):
        me1 = EMA(self.data, period=self.p.period_me1)
        me2 = EMA(self.data, period=self.p.period_me2)
        self.l.macd = me1 - me2
        self.l.signal = EMA(self.l.macd, period=self.p.period_signal)
        self.l.histo = self.l.macd - self.l.signal
完成！无需考虑最小周期。

EMA 代表指数移动平均线（平台内置别名），这个（已经在平台中）已经声明了它的需求。指标的命名线条“macd”和“signal”被分配了已经携带声明（幕后）的周期的对象。

macd 从操作“me1 - me2”中获取周期，而 me1 和 me2 都是具有不同周期的指数移动平均线。signal 直接从 macd 上的指数移动平均线获取周期。这个 EMA 也考虑到现有的 macd 周期和计算自身所需的样本量（period_signal）。histo 获取两个操作数“signal - macd”的最大值。一旦两者准备好，histo 也可以生成一个值

一个完整的自定义指标#
让我们开发一个简单的自定义指标，它“指示”一个移动平均线（可以通过参数修改）是否在给定数据之上：

import backtrader as bt
import backtrader.indicators as btind

class OverUnderMovAv(bt.Indicator):
    lines = ('overunder',)
    params = dict(period=20, movav=btind.MovAv.Simple)

    def __init__(self):
        movav = self.p.movav(self.data, period=self.p.period)
        self.l.overunder = bt.Cmp(movav, self.data)
完成！

如果平均线在数据之上，指标将具有值“1”；如果在数据之下，则为“-1”。如果数据是常规数据源，则比较收盘价将生成 1 和 -1。

虽然在绘图部分可以看到更多内容，为了在绘图世界中有一个良好和漂亮的公民，可以添加一些内容：

import backtrader as bt
import backtrader.indicators as btind

class OverUnderMovAv(bt.Indicator):
    lines = ('overunder',)
    params = dict(period=20, movav=btind.MovAv.Simple)

    plotinfo = dict(


        # 在 1 和 -1 之上和之下添加额外的边距
        plotymargin=0.15,

        # 绘制参考水平线在 1.0 和 -1.0
        plothlines=[1.0, -1.0],

        # 简化 y 轴刻度为 1.0 和 -1.0
        plotyticks=[1.0, -1.0])

    # 使用虚线样式绘制 "overunder" 线（唯一的一个）
    # ls 代表线条样式，并直接传递给 matplotlib
    plotlines = dict(overunder=dict(ls='--'))

    def _plotlabel(self):
        # 此方法返回将在绘图上显示的标签列表
        # 在指标名称之后

        # 周期必须始终存在
        plabels = [self.p.period]

        # 如果不是默认移动平均线，只放移动平均线
        plabels += [self.p.movav] * self.p.notdefault('movav')

        return plabels

    def __init__(self):
        movav = self.p.movav(self.data, period=self.p.period)
        self.l.overunder = bt.Cmp(movav, self.data)
完成！

这个指标将具有 1 和 -1 的值，并且在绘图中有良好的表现。
##########################################################################################################################################
周期混合#
如果提供值的数据源有不同的时间框架，在 Cerebro 引擎中有不同的长度，指标将会出错。

示例计算中，data0 有天的时间框架，data1 有月的时间框架：

pivotpoint = btind.PivotPoint(self.data1)
sellsignal = self.data0.close < pivotpoint.s1
在这里，当收盘价低于 s1 线（第一个支撑）时，寻求卖出信号。

注意

PivotPoint 定义上在较大的时间框架中工作。

过去，这会导致以下错误：

return self.array[self.idx + ago]
IndexError: array index out of range
原因很简单：self.data.close 从第一个时刻提供值，但 PivotPoint（以及 s1 线）只有在整个月过去后才会提供值，这大约相当于 22 个 self.data0.close 的值。在这 22 个收盘价期间，s1 还没有值，尝试从底层数组获取它会失败。

线条对象支持 (ago) 操作符（Python 中的 __call__ 特殊方法）以提供其延迟版本：

close1 = self.data.close(-1)
在这个例子中，对象 close1（通过 [0] 访问时）始终包含由 close 提供的前一个值（-1）。此语法已被重用以适应时间框架。让我们重写上述的 pivotpoint 代码片段：

pivotpoint = btind.PivotPoint(self.data1)
sellsignal = self.data0.close < pivotpoint.s1()
请注意，() 无参数执行（在后台提供了一个 None）。正在发生以下情况：

pivotpoint.s1() 返回一个内部 LinesCoupler 对象，该对象遵循较大范围的节奏。该耦合器使用来自实际 s1 的最新提供的值填充自身（以 NaN 为默认值开始）。

但为了实现这一魔法，还需要额外的东西。Cerebro 必须这样创建：

cerebro = bt.Cerebro(runonce=False)
或这样执行：

cerebro.run(runonce=False)
在这种模式下，指标和延迟评估的自动线条对象按步执行，而不是在紧密循环中执行。这使整个操作变得更慢，但它使其成为可能。

底部的示例脚本现在可以运行：

$ ./mixing-timeframes.py
输出：

0021,0021,0001,2005-01-31,2984.75,2935.96,0.00
0022,0022,0001,2005-02-01,3008.85,2935.96,0.00
...
0073,0073,0003,2005-04-15,3013.89,3010.76,0.00
0074,0074,0003,2005-04-18,2947.79,3010.76,1.00
...
在第 74 行，第一次出现 close < s1。

脚本还提供了额外的可能性：耦合一个指标的所有线条。之前是：

self.sellsignal = self.data0.close < pp.s1()
替代方法是：

pp1 = pp()
self.sellsignal = self.data0.close < pp1.s1
现在整个 PivotPoint 指标已被耦合，并且可以访问其任何线条（即 p、r1、r2、s1、s2）。脚本只对 s1 感兴趣，访问是直接的：

$ ./mixing-timeframes.py --multi
输出：

0021,0021,0001,2005-01-31,2984.75,2935.96,0.00
0022,0022,0001,2005-02-01,3008.85,2935.96,0.00
...
0073,0073,0003,2005-04-15,3013.89,3010.76,0.00
0074,0074,0003,2005-04-18,2947.79,3010.76,1.00
...
这里没有意外。与之前相同。“耦合”对象甚至可以绘制：

$ ./mixing-timeframes.py --multi --plot
完整耦合语法#
对于具有多条线的线条对象（例如 PivotPoint 指标）：

obj(clockref=None, line=-1)
clockref：如果 clockref 为 None，则周围对象（例如策略）将作为参考，以适应较大时间框架（例如：月）到较小/更快的时间框架（例如：日）。如果需要，可以使用另一个参考。

line：

如果默认的 -1 被给定，则所有线条都被耦合。
如果是另一个整数（例如 0 或 1），则单条线将被耦合，并通过索引（来自 obj.lines[x]）获取。
如果传递了字符串，则按名称获取线条。
在示例中，可以这样做：

coupled_s1 = pp(line='s1')
对于只有一条线的线条对象（例如来自 PivotPoint 指标的 s1 线）：

obj(clockref=None)（见上文的 `clockref`）
结论#
在常规的 () 语法中，来自不同时间框架的数据源可以混合在指标中，始终考虑到 cerebro 需要使用 runonce=False 实例化或创建。

脚本代码和用法#
可以在 backtrader 的源代码中找到示例。用法：

$ ./mixing-timeframes.py --help
usage: mixing-timeframes.py [-h] [--data DATA] [--multi] [--plot]

Sample for pivot point and cross plotting

optional arguments:
  -h, --help   show this help message and exit
  --data DATA  Data to be read in (default: ../../datas/2005-2006-day-001.txt)
  --multi      Couple all lines of the indicator (default: False)
  --plot       Plot the result (default: False)
代码：

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse

import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicators as btind
import backtrader.utils.flushfile


class St(bt.Strategy):
    params = dict(multi=True)

    def __init__(self):
        self.pp = pp = btind.PivotPoint(self.data1)
        pp.plotinfo.plot = False  # deactivate plotting

        if self.p.multi:
            pp1 = pp()  # couple the entire indicators
            self.sellsignal = self.data0.close < pp1.s1
        else:
            self.sellsignal = self.data0.close < pp.s1()

    def next(self):
        txt = ','.join(
            ['%04d' % len(self),
             '%04d' % len(self.data0),
             '%04d' % len(self.data1),
             self.data.datetime.date(0).isoformat(),
             '%.2f' % self.data0.close[0],
             '%.2f' % self.pp.s1[0],
             '%.2f' % self.sellsignal[0]])

        print(txt)


def runstrat():
    args = parse_args()

    cerebro = bt.Cerebro()
    data = btfeeds.BacktraderCSVData(dataname=args.data)
    cerebro.adddata(data)
    cerebro.resampledata(data, timeframe=bt.TimeFrame.Months)

    cerebro.addstrategy(St, multi=args.multi)

    cerebro.run(stdstats=False, runonce=False)
    if args.plot:
        cerebro.plot(style='bar')


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Sample for pivot point and cross plotting')

    parser.add_argument('--data', required=False,
                        default='../../datas/2005-2006-day-001.txt',
                        help='Data to be read in')

    parser.add_argument('--multi', required=False, action='store_true',
                        help='Couple all lines of the indicator')

    parser.add_argument('--plot', required=False, action='store_true

',
                        help=('Plot the result'))

    return parser.parse_args()


if __name__ == '__main__':
    runstrat()
希望这能帮助你理解如何在 backtrader 中混合不同时间框架的数据！
################################################################################################################################
TA-Lib#
即使backtrader已经提供了大量内置指标，并且开发一个指标主要是定义输入、输出并以自然方式编写公式，但有些人仍然希望使用TA-LIB。因为，指标X在TA-LIB库中存在，但在backtrader中不存在（作者很乐意接受请求），还有，TA-LIB的行为是众所周知的，人们信赖传统的事物。

为了满足每个人的需求，提供了TA-LIB集成。

需求#
TA-LIB的Python封装
任何需要的依赖项（例如numpy）
安装详情在GitHub仓库中
使用TA-LIB#
与使用backtrader内置指标一样简单。以下是一个简单移动平均线的示例。首先是backtrader的示例：

import backtrader as bt

class MyStrategy(bt.Strategy):
    params = (('period', 20),)

    def __init__(self):
        self.sma = bt.indicators.SMA(self.data, period=self.p.period)
        ...
接下来是TA-LIB的示例：

import backtrader as bt

class MyStrategy(bt.Strategy):
    params = (('period', 20),)

    def __init__(self):
        self.sma = bt.talib.SMA(self.data, timeperiod=self.p.period)
        ...
注意，TA-LIB指标的参数由库本身定义，而不是backtrader。在这种情况下，TA-LIB中的SMA使用名为timeperiod的参数来定义操作窗口的大小。

对于需要多个输入的指标，例如随机指标：

import backtrader as bt

class MyStrategy(bt.Strategy):
    params = (('period', 20),)

    def __init__(self):
        self.stoc = bt.talib.STOCH(self.data.high, self.data.low, self.data.close,
                                   fastk_period=14, slowk_period=3, slowd_period=3)
        ...
注意，high、low和close分别传递。可以尝试传递open而不是low（或其他任何数据系列）进行实验。

TA-LIB指标文档会自动解析并添加到backtrader文档中。你也可以查看TA-LIB的源代码/文档，或者执行以下操作：

print(bt.talib.SMA.__doc__)
输出如下：

SMA([input_arrays], [timeperiod=30])

Simple Moving Average (Overlap Studies)

Inputs:
    price: (any ndarray)
Parameters:
    timeperiod: 30
Outputs:
    real
这提供了一些信息：

期望的输入（忽略ndarray的注释，因为backtrader在后台进行转换）
哪些参数及其默认值
指标实际提供的输出线
移动平均线和MA_Type#
要选择特定的移动平均线，如bt.talib.STOCH，标准的TA-LIB MA_Type可以通过backtrader.talib.MA_Type访问。例如：

import backtrader as bt
print('SMA:', bt.talib.MA_Type.SMA)
print('T3:', bt.talib.MA_Type.T3)
绘制TA-LIB指标#
与常规用法一样，绘制TA-LIB指标无需特殊操作。

注意：

输出蜡烛图的指标（所有寻找蜡烛图模式的指标）会生成二进制输出：0或100。为了避免在图表上添加子图，存在自动绘图转换，以在识别模式时将其绘制在数据上。

示例和比较#
以下是一些比较TA-LIB指标输出与backtrader内置指标的示例。注意：

TA-LIB指标在图上有一个TA_前缀。这是样例特意这样做以帮助用户区分。
如果两者结果相同，移动平均线会叠加在现有移动平均线上，无法单独查看，这样的测试是通过的。
所有样例包括CDLDOJI指标作为参考。

KAMA（考夫曼移动平均线）#
这是第一个示例，因为这是样本直接比较的所有指标中唯一存在差异的：

样本的初始值不同
在某个时间点，值会趋同，两个KAMA实现具有相同的行为。
分析TA-LIB源码后发现：

TA-LIB的实现为KAMA的初始值做了一个非行业标准的选择。
源代码引用：这里使用昨天的价格作为前一个KAMA。
backtrader采用了通常的选择，例如Stockcharts：

StockCharts上的KAMA
由于需要一个初始值来开始计算，第一个KAMA只是一个简单移动平均线。因此存在差异。此外：

TA-LIB的KAMA实现不允许指定用于调整Kaufman定义的可缩放常数的快慢周期。
样本执行：

$ ./talibtest.py --plot --ind kama
输出
图像

SMA#
$ ./talibtest.py --plot --ind sma
输出
图像

EMA#
$ ./talibtest.py --plot --ind ema
输出
图像

随机指标#
$ ./talibtest.py --plot --ind stoc
输出
图像

RSI#
$ ./talibtest.py --plot --ind rsi
输出
图像

MACD#
$ ./talibtest.py --plot --ind macd
输出
图像

布林带#
$ ./talibtest.py --plot --ind bollinger
输出
图像

AROON#
注意，TA-LIB选择先绘制下降线，并且颜色与backtrader内置指标相反。

$ ./talibtest.py --plot --ind aroon
输出
图像

Ultimate Oscillator#
$ ./talibtest.py --plot --ind ultimate
输出
图像

Trix#
$ ./talibtest.py --plot --ind trix
输出
图像

ADXR#
backtrader同时提供ADX和ADXR线。

$ ./talibtest.py --plot --ind adxr
输出
图像

DEMA#
$ ./talibtest.py --plot --ind dema
输出
图像

TEMA#
$ ./talibtest.py --plot --ind tema
输出
图像

PPO#
backtrader不仅提供PPO线，还提供更传统的MACD方法。

$ ./talibtest.py --plot --ind ppo
输出
图像

WilliamsR#
$ ./talibtest.py --plot --ind williamsr
输出
图像

ROC#
所有指标应具有相同的形状，但跟踪动量或变化率有多种定义。

$ ./talibtest.py --plot --ind roc
输出
图像

样本用法#
$ ./talibtest.py --help
usage: talibtest.py [-h] [--data0 DATA0] [--fromdate FROMDATE]
                    [--todate TODATE]
                    [--ind {sma,ema,stoc,rsi,macd,bollinger,aroon,ultimate,trix,kama,adxr,dema,tema,ppo,williamsr,roc}]
                    [--no-doji] [--use-next] [--plot [kwargs]]

Sample for ta-lib

optional arguments:
  -h, --help            show this help message and exit
  --data0 DATA0         Data to be read in (default:
                        ../../datas/yhoo-1996-2015.txt)
  --fromdate FROMDATE   Starting date in YYYY-MM-DD format (default:
                        2005-01-01)
  --todate TODATE       Ending date in YYYY-MM-DD format (default: 2006-12-31)
  --ind {sma,ema,stoc,rsi,macd,bollinger,aroon,ultimate,trix,kama,adxr,dema,tema,ppo,williamsr,roc}
                        Which indicator pair to show together (default: sma)
  --no-doji             Remove Doji CandleStick pattern checker (default:
                        False)
  --use-next            Use next (step by step) instead of once (batch)
                        (default: False)
  --plot [kwargs], -p [kwargs]
                        Plot the read data applying any kwargs passed For
                        example (escape the quotes if needed): --plot
                        style="candle" (to plot candles) (default: None)
样本代码#
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse
import datetime

import backtrader as bt


class TALibStrategy(bt.Strategy):
    params = (('ind', 'sma'), ('doji', True),)

    INDS = ['sma', 'ema', 'stoc', 'rsi', 'mac

d', 'bollinger', 'aroon',
            'ultimate', 'trix', 'kama', 'adxr', 'dema', 'ppo', 'tema',
            'roc', 'williamsr']

    def __init__(self):
        if self.p.doji:
            bt.talib.CDLDOJI(self.data.open, self.data.high,
                             self.data.low, self.data.close)

        if self.p.ind == 'sma':
            bt.talib.SMA(self.data.close, timeperiod=25, plotname='TA_SMA')
            bt.indicators.SMA(self.data, period=25)
        elif self.p.ind == 'ema':
            bt.talib.EMA(timeperiod=25, plotname='TA_SMA')
            bt.indicators.EMA(period=25)
        elif self.p.ind == 'stoc':
            bt.talib.STOCH(self.data.high, self.data.low, self.data.close,
                           fastk_period=14, slowk_period=3, slowd_period=3,
                           plotname='TA_STOCH')

            bt.indicators.Stochastic(self.data)

        elif self.p.ind == 'macd':
            bt.talib.MACD(self.data, plotname='TA_MACD')
            bt.indicators.MACD(self.data)
            bt.indicators.MACDHisto(self.data)
        elif self.p.ind == 'bollinger':
            bt.talib.BBANDS(self.data, timeperiod=25,
                            plotname='TA_BBANDS')
            bt.indicators.BollingerBands(self.data, period=25)

        elif self.p.ind == 'rsi':
            bt.talib.RSI(self.data, plotname='TA_RSI')
            bt.indicators.RSI(self.data)

        elif self.p.ind == 'aroon':
            bt.talib.AROON(self.data.high, self.data.low, plotname='TA_AROON')
            bt.indicators.AroonIndicator(self.data)

        elif self.p.ind == 'ultimate':
            bt.talib.ULTOSC(self.data.high, self.data.low, self.data.close,
                            plotname='TA_ULTOSC')
            bt.indicators.UltimateOscillator(self.data)

        elif self.p.ind == 'trix':
            bt.talib.TRIX(self.data, timeperiod=25,  plotname='TA_TRIX')
            bt.indicators.Trix(self.data, period=25)

        elif self.p.ind == 'adxr':
            bt.talib.ADXR(self.data.high, self.data.low, self.data.close,
                          plotname='TA_ADXR')
            bt.indicators.ADXR(self.data)

        elif self.p.ind == 'kama':
            bt.talib.KAMA(self.data, timeperiod=25, plotname='TA_KAMA')
            bt.indicators.KAMA(self.data, period=25)

        elif self.p.ind == 'dema':
            bt.talib.DEMA(self.data, timeperiod=25, plotname='TA_DEMA')
            bt.indicators.DEMA(self.data, period=25)

        elif self.p.ind == 'ppo':
            bt.talib.PPO(self.data, plotname='TA_PPO')
            bt.indicators.PPO(self.data, _movav=bt.indicators.SMA)

        elif self.p.ind == 'tema':
            bt.talib.TEMA(self.data, timeperiod=25, plotname='TA_TEMA')
            bt.indicators.TEMA(self.data, period=25)

        elif self.p.ind == 'roc':
            bt.talib.ROC(self.data, timeperiod=12, plotname='TA_ROC')
            bt.talib.ROCP(self.data, timeperiod=12, plotname='TA_ROCP')
            bt.talib.ROCR(self.data, timeperiod=12, plotname='TA_ROCR')
            bt.talib.ROCR100(self.data, timeperiod=12, plotname='TA_ROCR100')
            bt.indicators.ROC(self.data, period=12)
            bt.indicators.Momentum(self.data, period=12)
            bt.indicators.MomentumOscillator(self.data, period=12)

        elif self.p.ind == 'williamsr':
            bt.talib.WILLR(self.data.high, self.data.low, self.data.close,
                           plotname='TA_WILLR')
            bt.indicators.WilliamsR(self.data)


def runstrat(args=None):
    args = parse_args(args)

    cerebro = bt.Cerebro()

    dkwargs = dict()
    if args.fromdate:
        fromdate = datetime.datetime.strptime(args.fromdate, '%Y-%m-%d')
        dkwargs['fromdate'] = fromdate

    if args.todate:
        todate = datetime.datetime.strptime(args.todate, '%Y-%m-%d')
        dkwargs['todate'] = todate

    data0 = bt.feeds.YahooFinanceCSVData(dataname=args.data0, **dkwargs)
    cerebro.adddata(data0)

    cerebro.addstrategy(TALibStrategy, ind=args.ind, doji=not args.no_doji)

    cerebro.run(runcone=not args.use_next, stdstats=False)
    if args.plot:
        pkwargs = dict(style='candle')
        if args.plot is not True:  # evals to True but is not True
            npkwargs = eval('dict(' + args.plot + ')')  # args were passed
            pkwargs.update(npkwargs)

        cerebro.plot(**pkwargs)


def parse_args(pargs=None):

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Sample for sizer')

    parser.add_argument('--data0', required=False,
                        default='../../datas/yhoo-1996-2015.txt',
                        help='Data to be read in')

    parser.add_argument('--fromdate', required=False,
                        default='2005-01-01',
                        help='Starting date in YYYY-MM-DD format')

    parser.add_argument('--todate', required=False,
                        default='2006-12-31',
                        help='Ending date in YYYY-MM-DD format')

    parser.add_argument('--ind', required=False, action='store',
                        default=TALibStrategy.INDS[0],
                        choices=TALibStrategy.INDS,
                        help=('Which indicator pair to show together'))

    parser.add_argument('--no-doji', required=False, action='store_true',
                        help=('Remove Doji CandleStick pattern checker'))

    parser.add_argument('--use-next', required=False, action='store_true',
                        help=('Use next (step by step) '
                              'instead of once (batch)'))

    # Plot options
    parser.add_argument('--plot', '-p', nargs='?', required=False,
                        metavar='kwargs', const=True,
                        help=('Plot the read data applying any kwargs passed\n'
                              '\n'
                              'For example (escape the quotes if needed):\n'
                              '\n'
                              '  --plot style="candle" (to plot candles)\n'))

    if pargs is not None:
        return parser.parse_args(pargs)

    return parser.parse_args()


if __name__ == '__main__':
    runstrat()
这样，您就可以在backtrader中使用TA-LIB的指标，并根据需要进行绘图和比较。
###############################################################################################################################
订单#
Cerebro 是 backtrader 中的关键控制系统，而 Strategy（一个子类）是终端用户的关键控制点。后者需要一个连接系统其他部分的方法，这就是订单发挥关键作用的地方。

订单将策略中的逻辑决策转化为适合 Broker 执行操作的消息。这是通过以下方式完成的：

创建#
通过 Strategy 的方法：buy、sell 和 close（Strategy），这些方法返回一个订单实例作为参考。

取消#
通过 Strategy 的方法：cancel（Strategy），该方法需要一个订单实例来操作。

订单也作为一种通信方式反馈给用户，通知 Broker 中的执行情况。

通知#
通过 Strategy 的方法：notify_order（Strategy），该方法报告一个订单实例。

订单创建#
调用 buy、sell 和 close 时，以下参数适用于创建：

参数名	默认值	描述
data	None	为哪个数据创建订单。如果为 None，则使用系统中的第一个数据，self.datas[0] 或 self.data0（又名 self.data）。
size	None	使用的单位数量。如果为 None，则使用通过 getsizer 获取的 sizer 实例来确定大小。
price	None	使用的价格（实时 Broker 可能会对格式有实际限制，如果不符合最小刻度要求）。对于 Market 和 Close 订单，None 是有效的（市场决定价格）。对于 Limit、Stop 和 StopLimit 订单，该值决定触发点（在 Limit 的情况下，触发点显然是订单匹配的价格）。
plimit	None	仅适用于 StopLimit 订单。这是在 Stop 触发后设置隐含 Limit 订单的价格。
exectype	None	可能的值：
- Order.Market 或 None：市场订单将以下一个可用价格执行。在回测中，这将是下一根K线的开盘价。
- Order.Limit：只能在给定价格或更好的价格执行的订单。
- Order.Stop：在价格触发时执行的订单，执行方式如同 Market 订单。
- Order.StopLimit：在价格触发时执行的订单，作为隐含 Limit 订单执行，价格由 pricelimit 给定。
valid	None	可能的值：
- None：生成一个不会过期的订单（即 Good till cancel），并在市场中保留直到匹配或取消。实际上，Broker 往往会强制一个时间限制，但这通常是很长时间，所以认为它不会过期。
- datetime.datetime 或 datetime.date 实例：使用给定的日期生成一个有效直到该日期的订单（即 Good till date）。
- Order.DAY 或 0 或 timedelta()：生成一个有效期为一天的订单（即日订单），有效期直到会话结束。
- 数值：假定为一个对应于 matplotlib 编码的日期时间值（backtrader 使用的），并用于生成一个有效期至该时间的订单（即 Good till date）。
tradeid	0	这是 backtrader 用来跟踪同一资产上重叠交易的内部值。在通知订单状态变化时，该 tradeid 会返回给策略。
**kwargs	/	额外的 Broker 实现可能支持额外的参数。backtrader 会将 kwargs 传递给创建的订单对象。
示例#
如果 backtrader 直接支持的 4 种订单执行类型不够，例如对于 Interactive Brokers，可以传递如下参数：

orderType='LIT', lmtPrice=10.0, auxPrice=9.8
这将覆盖 backtrader 的设置，生成一个触及价格为 9.8 且限价为 10.0 的 LIMIT IF TOUCHED 订单。

注意：

close 方法将检查当前仓位，并相应地使用 buy 或 sell 有效地关闭仓位。除非参数由用户输入，否则大小也将自动计算，在这种情况下可以实现部分关闭或反转。

订单通知#
要接收通知，必须在用户子类的 Strategy 中重写 notify_order 方法（默认行为是什么都不做）。以下适用于这些通知：

在策略的 next 方法调用之前发出。
在同一个 next 循环中，可能（并且会）多次发生相同或不同状态的相同订单通知。
订单可能会被提交给 Broker，被接受并在 next 再次调用之前完成执行。
在这种情况下，至少会发生 3 次通知，状态值如下：

Order.Submitted 因为订单已发送给 Broker。
Order.Accepted 因为订单已被 Broker 接受并等待执行。
Order.Completed 因为在示例中订单已快速匹配并完全成交（通常适用于 Market 订单）。
对于 Order.Partial 状态，即使在回测 Broker 中（不考虑匹配量）不会看到，但在实际 Broker 中肯定会看到。

实际 Broker 可能会在更新仓位之前发出一次或多次执行通知，这些执行将构成一个 Order.Partial 通知。

实际执行数据在属性：order.executed 中，这是一个 OrderData 类型的对象，具有常见的字段如大小和价格。

创建时的值存储在 order.created 中，在订单生命周期中保持不变。

订单状态值#
以下定义：

Order.Created：在创建订单实例时设置。除非手动创建订单实例，否则终端用户不会看到该状态。
Order.Submitted：在订单实例已传输给 Broker 时设置。这只是意味着已发送。在回测模式中这是立即的，但在实际 Broker 中可能需要时间，可能在转发给交易所时才通知。
Order.Accepted：Broker 已接受订单，并在系统中（或已在交易所）等待执行，参数如执行类型、大小、价格和有效期。
Order.Partial：订单已部分执行。order.executed 包含当前填充的大小和平均价格。
order.executed.exbits 包含部分填充的完整执行位列表。
Order.Complete：订单已完全填充平均价格。
Order.Rejected：Broker 拒绝了订单。可能是某个参数（如有效期）不被接受，订单无法接受。
原因会通过策略的 notify_store 方法通知。虽然这可能显得奇怪，但实际 Broker 会通过事件通知，这可能与订单直接相关或无关。但可以在 notify_store 中看到 Broker 的通知。
在回测 Broker 中不会看到此状态。
Order.Margin：订单执行将导致保证金要求，之前接受的订单已从系统中移除。
Order.Cancelled（或 Order.Canceled）：用户请求取消的确认。
必须考虑，通过策略的 cancel 方法请求取消订单并不保证取消。订单可能已经执行，但此执行可能尚未被 Broker 通知，并且通知可能尚未传递给策略。
Order.Expired：之前接受的订单具有时间有效性，已过期并被从系统中移除。
引用：Order 及相关类#
这些对象是 backtrader 生态系统中的通用类。在与其他 Broker 操作时，它们可能已扩展和/或包含额外的嵌入信息。请参阅相应 Broker 的参考。

class backtrader.order.Order()
持有创建/执行数据和订单类型的类。

订单可能具有以下状态：

Submitted：发送给 Broker，等待确认。
Accepted：被 Broker 接受。
Partial：部分执行。
Completed：完全执行。
Canceled/Cancelled：被用户取消。
Expired：过期。
Margin：没有足够的现金执行订单。
Rejected：被 Broker 拒绝。
这可能发生在订单提交期间（因此订单不会达到 Accepted 状态），或者在执行前因每根新K线价格变化，现金被其他来源（如期货类工具）抽取导致拒绝。
成员属性：

ref：唯一订单标识符。
created：持有创建数据的 OrderData。
executed：持有执行数据的 OrderData。
info：通过 addinfo() 方法传递的自定义信息。以子类化的 OrderedDict 形式保存，键也可以使用.符号指定。
用户方法：

isbuy()：返回一个布尔值，指示订单是否买入。
issell()：返回一个布尔值，指示订单是否卖出。
alive()：返回一个布尔值，如果订单状态为 Partial 或 Accepted。
class backtrader.order.OrderData(dt=None, size=0, price=0.0, pricelimit=0.0, remsize

=0, pclose=0.0, trailamount=0.0, trailpercent=0.0)
持有创建和执行实际订单数据。

在创建情况下，请求的数据，在执行情况下，实际结果。

成员属性：

exbits：此 OrderData 的 OrderExecutionBits 的可迭代对象。
dt：日期时间（浮点数）创建/执行时间。
size：请求/执行大小。
price：执行价格。注意：如果没有价格和 pricelimit，订单创建时的收盘价将作为参考。
pricelimit：StopLimit 的价格限制（首先有触发）。
trailamount：追踪止损的绝对价格距离。
trailpercent：追踪止损的百分比价格距离。
value：整个位大小的市场价值。
comm：整个位执行的佣金。
pnl：此位产生的盈亏（如果有关闭）。
margin：订单产生的保证金（如果有）。
psize：当前未平仓头寸大小。
pprice：当前未平仓头寸价格。
class backtrader.order.OrderExecutionBit(dt=None, size=0, price=0.0, closed=0, closedvalue=0.0, closedcomm=0.0, opened=0, openedvalue=0.0, openedcomm=0.0, pnl=0.0, psize=0, pprice=0.0)
旨在持有订单执行信息。“位”不确定订单是否已完全/部分执行，只是持有信息。

成员属性：

dt：日期时间（浮点数）执行时间。
size：执行数量。
price：执行价格。
closed：执行关闭了多少现有头寸。
opened：执行打开了多少新头寸。
openedvalue：新开部分的市场价值。
closedvalue：关闭部分的市场价值。
closedcomm：关闭部分的佣金。
openedcomm：打开部分的佣金。
value：整个位大小的市场价值。
comm：整个位执行的佣金。
pnl：此位产生的盈亏（如果有关闭）。
psize：当前未平仓头寸大小。
pprice：当前未平仓头寸价格。
Previous
TA-Lib



28 38Order.txt ##################################################
文件路径: 38Order.txt
================================================================================

订单#
Cerebro 是 backtrader 中的关键控制系统，而 Strategy（一个子类）是终端用户的关键控制点。后者需要一个连接系统其他部分的方法，这就是订单发挥关键作用的地方。

订单将策略中的逻辑决策转化为适合 Broker 执行操作的消息。这是通过以下方式完成的：

创建#
通过 Strategy 的方法：buy、sell 和 close（Strategy），这些方法返回一个订单实例作为参考。

取消#
通过 Strategy 的方法：cancel（Strategy），该方法需要一个订单实例来操作。

订单也作为一种通信方式反馈给用户，通知 Broker 中的执行情况。

通知#
通过 Strategy 的方法：notify_order（Strategy），该方法报告一个订单实例。

订单创建#
调用 buy、sell 和 close 时，以下参数适用于创建：

参数名	默认值	描述
data	None	为哪个数据创建订单。如果为 None，则使用系统中的第一个数据，self.datas[0] 或 self.data0（又名 self.data）。
size	None	使用的单位数量。如果为 None，则使用通过 getsizer 获取的 sizer 实例来确定大小。
price	None	使用的价格（实时 Broker 可能会对格式有实际限制，如果不符合最小刻度要求）。对于 Market 和 Close 订单，None 是有效的（市场决定价格）。对于 Limit、Stop 和 StopLimit 订单，该值决定触发点（在 Limit 的情况下，触发点显然是订单匹配的价格）。
plimit	None	仅适用于 StopLimit 订单。这是在 Stop 触发后设置隐含 Limit 订单的价格。
exectype	None	可能的值：
- Order.Market 或 None：市场订单将以下一个可用价格执行。在回测中，这将是下一根K线的开盘价。
- Order.Limit：只能在给定价格或更好的价格执行的订单。
- Order.Stop：在价格触发时执行的订单，执行方式如同 Market 订单。
- Order.StopLimit：在价格触发时执行的订单，作为隐含 Limit 订单执行，价格由 pricelimit 给定。
valid	None	可能的值：
- None：生成一个不会过期的订单（即 Good till cancel），并在市场中保留直到匹配或取消。实际上，Broker 往往会强制一个时间限制，但这通常是很长时间，所以认为它不会过期。
- datetime.datetime 或 datetime.date 实例：使用给定的日期生成一个有效直到该日期的订单（即 Good till date）。
- Order.DAY 或 0 或 timedelta()：生成一个有效期为一天的订单（即日订单），有效期直到会话结束。
- 数值：假定为一个对应于 matplotlib 编码的日期时间值（backtrader 使用的），并用于生成一个有效期至该时间的订单（即 Good till date）。
tradeid	0	这是 backtrader 用来跟踪同一资产上重叠交易的内部值。在通知订单状态变化时，该 tradeid 会返回给策略。
**kwargs	/	额外的 Broker 实现可能支持额外的参数。backtrader 会将 kwargs 传递给创建的订单对象。
示例#
如果 backtrader 直接支持的 4 种订单执行类型不够，例如对于 Interactive Brokers，可以传递如下参数：

orderType='LIT', lmtPrice=10.0, auxPrice=9.8
这将覆盖 backtrader 的设置，生成一个触及价格为 9.8 且限价为 10.0 的 LIMIT IF TOUCHED 订单。

注意：

close 方法将检查当前仓位，并相应地使用 buy 或 sell 有效地关闭仓位。除非参数由用户输入，否则大小也将自动计算，在这种情况下可以实现部分关闭或反转。

订单通知#
要接收通知，必须在用户子类的 Strategy 中重写 notify_order 方法（默认行为是什么都不做）。以下适用于这些通知：

在策略的 next 方法调用之前发出。
在同一个 next 循环中，可能（并且会）多次发生相同或不同状态的相同订单通知。
订单可能会被提交给 Broker，被接受并在 next 再次调用之前完成执行。
在这种情况下，至少会发生 3 次通知，状态值如下：

Order.Submitted 因为订单已发送给 Broker。
Order.Accepted 因为订单已被 Broker 接受并等待执行。
Order.Completed 因为在示例中订单已快速匹配并完全成交（通常适用于 Market 订单）。
对于 Order.Partial 状态，即使在回测 Broker 中（不考虑匹配量）不会看到，但在实际 Broker 中肯定会看到。

实际 Broker 可能会在更新仓位之前发出一次或多次执行通知，这些执行将构成一个 Order.Partial 通知。

实际执行数据在属性：order.executed 中，这是一个 OrderData 类型的对象，具有常见的字段如大小和价格。

创建时的值存储在 order.created 中，在订单生命周期中保持不变。

订单状态值#
以下定义：

Order.Created：在创建订单实例时设置。除非手动创建订单实例，否则终端用户不会看到该状态。
Order.Submitted：在订单实例已传输给 Broker 时设置。这只是意味着已发送。在回测模式中这是立即的，但在实际 Broker 中可能需要时间，可能在转发给交易所时才通知。
Order.Accepted：Broker 已接受订单，并在系统中（或已在交易所）等待执行，参数如执行类型、大小、价格和有效期。
Order.Partial：订单已部分执行。order.executed 包含当前填充的大小和平均价格。
order.executed.exbits 包含部分填充的完整执行位列表。
Order.Complete：订单已完全填充平均价格。
Order.Rejected：Broker 拒绝了订单。可能是某个参数（如有效期）不被接受，订单无法接受。
原因会通过策略的 notify_store 方法通知。虽然这可能显得奇怪，但实际 Broker 会通过事件通知，这可能与订单直接相关或无关。但可以在 notify_store 中看到 Broker 的通知。
在回测 Broker 中不会看到此状态。
Order.Margin：订单执行将导致保证金要求，之前接受的订单已从系统中移除。
Order.Cancelled（或 Order.Canceled）：用户请求取消的确认。
必须考虑，通过策略的 cancel 方法请求取消订单并不保证取消。订单可能已经执行，但此执行可能尚未被 Broker 通知，并且通知可能尚未传递给策略。
Order.Expired：之前接受的订单具有时间有效性，已过期并被从系统中移除。
引用：Order 及相关类#
这些对象是 backtrader 生态系统中的通用类。在与其他 Broker 操作时，它们可能已扩展和/或包含额外的嵌入信息。请参阅相应 Broker 的参考。

class backtrader.order.Order()
持有创建/执行数据和订单类型的类。

订单可能具有以下状态：

Submitted：发送给 Broker，等待确认。
Accepted：被 Broker 接受。
Partial：部分执行。
Completed：完全执行。
Canceled/Cancelled：被用户取消。
Expired：过期。
Margin：没有足够的现金执行订单。
Rejected：被 Broker 拒绝。
这可能发生在订单提交期间（因此订单不会达到 Accepted 状态），或者在执行前因每根新K线价格变化，现金被其他来源（如期货类工具）抽取导致拒绝。
成员属性：

ref：唯一订单标识符。
created：持有创建数据的 OrderData。
executed：持有执行数据的 OrderData。
info：通过 addinfo() 方法传递的自定义信息。以子类化的 OrderedDict 形式保存，键也可以使用.符号指定。
用户方法：

isbuy()：返回一个布尔值，指示订单是否买入。
issell()：返回一个布尔值，指示订单是否卖出。
alive()：返回一个布尔值，如果订单状态为 Partial 或 Accepted。
class backtrader.order.OrderData(dt=None, size=0, price=0.0, pricelimit=0.0, remsize

=0, pclose=0.0, trailamount=0.0, trailpercent=0.0)
持有创建和执行实际订单数据。

在创建情况下，请求的数据，在执行情况下，实际结果。

成员属性：

exbits：此 OrderData 的 OrderExecutionBits 的可迭代对象。
dt：日期时间（浮点数）创建/执行时间。
size：请求/执行大小。
price：执行价格。注意：如果没有价格和 pricelimit，订单创建时的收盘价将作为参考。
pricelimit：StopLimit 的价格限制（首先有触发）。
trailamount：追踪止损的绝对价格距离。
trailpercent：追踪止损的百分比价格距离。
value：整个位大小的市场价值。
comm：整个位执行的佣金。
pnl：此位产生的盈亏（如果有关闭）。
margin：订单产生的保证金（如果有）。
psize：当前未平仓头寸大小。
pprice：当前未平仓头寸价格。
class backtrader.order.OrderExecutionBit(dt=None, size=0, price=0.0, closed=0, closedvalue=0.0, closedcomm=0.0, opened=0, openedvalue=0.0, openedcomm=0.0, pnl=0.0, psize=0, pprice=0.0)
旨在持有订单执行信息。“位”不确定订单是否已完全/部分执行，只是持有信息。

成员属性：

dt：日期时间（浮点数）执行时间。
size：执行数量。
price：执行价格。
closed：执行关闭了多少现有头寸。
opened：执行打开了多少新头寸。
openedvalue：新开部分的市场价值。
closedvalue：关闭部分的市场价值。
closedcomm：关闭部分的佣金。
openedcomm：打开部分的佣金。
value：整个位大小的市场价值。
comm：整个位执行的佣金。
pnl：此位产生的盈亏（如果有关闭）。
psize：当前未平仓头寸大小。
pprice：当前未平仓头寸价格。
###################################################################################################################
订单管理和执行#
对于订单管理，Backtrader 提供了3种基本操作：

buy
sell
cancel
注意：：一个更新操作显然是合乎逻辑的，但常识告诉我们，这种方法主要用于使用判断性交易方法的手动操作员。

对于订单执行逻辑，提供以下执行类型：

市价订单（Market）
收盘价订单（Close）
限价订单（Limit）
止损订单（Stop）
止损限价订单（StopLimit）
订单管理#
一些示例：

# 购买主数据，使用sizer的默认股份，市价订单
order = self.buy()

# 市价订单 - 有效期将被 "忽略"
order = self.buy(valid=datetime.datetime.now() + datetime.timedelta(days=3))

# 市价订单 - 价格将被忽略
order = self.buy(price=self.data.close[0] * 1.02)

# 市价订单 - 手动股份
order = self.buy(size=25)

# 限价订单 - 想要设置价格并可以设置有效期
order = self.buy(exectype=Order.Limit,
                 price=self.data.close[0] * 1.02,
                 valid=datetime.datetime.now() + datetime.timedelta(days=3))

# 止损限价订单 - 想要设置价格，价格限制
order = self.buy(exectype=Order.StopLimit,
                 price=self.data.close[0] * 1.02,
                 plimit=self.data.close[0] * 1.07)

# 取消现有订单
self.broker.cancel(order)
注意：

所有订单类型都可以通过创建一个订单实例（或其子类之一）并传递给 broker 来创建：

order = self.broker.submit(order)
注意：

Broker 中也有 buy 和 sell 操作，但它们对默认参数的容忍度较低。

订单执行逻辑#
Broker 使用两个主要指导原则（假设？）进行订单执行。

原则一#
当前数据已经发生，不能用于执行订单。

如果策略中的逻辑类似于：

if self.data.close > self.sma:  # 其中 sma 是简单移动平均线
    self.buy()
期望不能是订单将以逻辑中检查的收盘价执行，因为它已经发生。

原则二#
订单可以在下一组开盘/最高/最低/收盘价格范围内首先执行（以及订单中设置的条件）。

原则三#
成交量不起作用，实际交易中，如果交易者选择非流动性资产或恰好触及价格栏的高/低点，它实际上会起作用。

但触及高/低点的情况很少发生（如果发生……你不需要 backtrader），所选择的资产将有足够的流动性来吸收任何正常交易的订单。

市价订单（Market）#
执行：

下一个价格栏的开盘价（通常称为 bar）
理由：

如果逻辑在时间点 X 执行并发出市价订单，下一个将发生的价格点是即将到来的开盘价。
注意：

该订单始终执行，并忽略任何用于创建它的价格和有效期参数。
收盘价订单（Close）#
执行：

使用下一个价格栏的收盘价，当下一个价格栏实际关闭时。
理由：

大多数回测数据源已经包含已关闭的价格栏，订单将立即以下一个价格栏的收盘价执行。日数据源是最常见的示例。
但系统可以被“tick”价格喂入，实际的价格栏（时间/日期）不断被新 tick 更新，而不会移动到下一个价格栏（因为时间和/或日期未改变）。
只有当时间或日期改变时，价格栏才真正关闭，订单才执行。
限价订单（Limit）#
执行：

如果数据触及在订单创建时设置的价格，则从下一个价格栏开始执行。
如果设置了有效期并到达时间点，订单将被取消。
价格匹配：

backtrader 尝试为限价订单提供最现实的执行价格。
使用4个价格点（开盘价/最高价/最低价/收盘价）可以部分推断出请求的价格是否可以改进。
对于买入订单：
情况1：如果价格栏的开盘价低于限价，订单立即以开盘价执行。订单在会话的开盘阶段被扫除。
情况2：如果开盘价没有低于限价，但最低价低于限价，那么限价在会话期间已经出现，订单可以执行。
对于卖出订单，逻辑显然是相反的。
止损订单（Stop）#
执行：

如果数据触及在订单创建时设置的触发价格，则从下一个价格栏开始执行。
如果设置了有效期并到达时间点，订单将被取消。
价格匹配：

backtrader 尝试为止损订单提供最现实的触发价格。
使用4个价格点（开盘价/最高价/最低价/收盘价）可以部分推断出请求的价格是否可以改进。
对于买入的止损订单：
情况1：如果价格栏的开盘价高于止损价，订单立即以开盘价执行。旨在停止亏损，如果价格上涨对现有空头头寸不利。
情况2：如果开盘价没有高于止损价，但最高价高于止损价，那么止损价在会话期间已经出现，订单可以执行。
对于卖出订单，逻辑显然是相反的。
止损限价订单（StopLimit）#
执行：

触发价格从下一个价格栏开始启动订单。
价格匹配：

触发：使用止损匹配逻辑（但仅触发并将订单转变为限价订单）。
限价：使用限价匹配逻辑。
一些示例#
正如图片（带代码）所示，总是胜过几百万字的长篇解释。请注意，代码段集中在订单创建部分。完整代码在底部。

将使用一个价格在简单移动平均线上/下方收盘的策略来生成买入/卖出信号。

信号在图表底部可见：使用交叉指示器的交叉信号。

将保存生成的“买入”订单的引用，以只允许系统中最多同时存在一个订单。

执行类型：市价订单（Market）#
在图表中可以看到订单在生成信号后一根价格栏后以开盘价执行。

if self.p.exectype == 'Market':
    self.buy(exectype=bt.Order.Market)  # 如果未给定，则默认

    self.log('BUY CREATE, exectype Market, price %.2f' %
             self.data.close[0])
执行类型：收盘价订单（Close）#
现在订单也是在生成信号后一根价格栏后执行，但以收盘价执行。

elif self.p.exectype == 'Close':
    self.buy(exectype=bt.Order.Close)

    self.log('BUY CREATE, exectype Close, price %.2f' %
             self.data.close[0])
执行类型：限价订单（Limit）#
有效期在传递为参数时会提前计算。

if self.p.valid:
    valid = self.data.datetime.date(0) +
            datetime.timedelta(days=self.p.valid)
else:
    valid = None
设置一个比信号生成价格（信号栏的收盘价）低1%的限价。请注意，这阻止了上面许多订单的执行。

elif self.p.exectype == 'Limit':
    price = self.data.close * (1.0 - self.p.perc1 / 100.0)

    self.buy(exectype=bt.Order.Limit, price=price, valid=valid)

    if self.p.valid:
        txt = 'BUY CREATE, exectype Limit, price %.2f, valid: %s'
        self.log(txt % (price, valid.strftime('%Y-%m-%d')))
    else:
        txt = 'BUY CREATE, exectype Limit, price %.2f'
        self.log(txt % price)
执行类型：带有效期的限价订单#
为了不永远等待一个可能只在价格对“买入”订单不利时执行的限价订单，订单只会有效4个（日历）天。

$ ./order-execution-samples.py --exectype Limit --perc1 1 --valid 4
执行类型：止损订单（Stop）#
设置一个比信号价格

高1%的止损价格。这意味着策略只有在信号生成后价格继续上涨时才买入，这可以解释为一种强劲信号。

elif self.p.exectype == 'Stop':
    price = self.data.close * (1.0 + self.p.perc1 / 100.0)

    self.buy(exectype=bt.Order.Stop, price=price, valid=valid)

    if self.p.valid:
        txt = 'BUY CREATE, exectype Stop, price %.2f, valid: %s'
        self.log(txt % (price, valid.strftime('%Y-%m-%d')))
    else:
        txt = 'BUY CREATE, exectype Stop, price %.2f'
        self.log(txt % price)
执行类型：止损限价订单（StopLimit）#
设置一个比信号价格高1%的止损价格。但限价设置为比信号（收盘）价格高0.5%，这可以解释为：等待强劲信号的出现，但不要买入高点。等待下跌。

elif self.p.exectype == 'StopLimit':
    price = self.data.close * (1.0 + self.p.perc1 / 100.0)

    plimit = self.data.close * (1.0 + self.p.perc2 / 100.0)

    self.buy(exectype=bt.Order.StopLimit, price=price, valid=valid,
             plimit=plimit)

    if self.p.valid:
        txt = ('BUY CREATE, exectype StopLimit, price %.2f,'
               ' valid: %s, pricelimit: %.2f')
        self.log(txt % (price, valid.strftime('%Y-%m-%d'), plimit))
    else:
        txt = ('BUY CREATE, exectype StopLimit, price %.2f,'
               ' pricelimit: %.2f')
        self.log(txt % (price, plimit))
测试脚本执行#
详见命令行帮助：

$ ./order-execution-samples.py --help
usage: order-execution-samples.py [-h] [--infile INFILE]
                                  [--csvformat {bt,visualchart,sierrachart,yahoo,yahoo_unreversed}]
                                  [--fromdate FROMDATE] [--todate TODATE]
                                  [--plot] [--plotstyle {bar,line,candle}]
                                  [--numfigs NUMFIGS] [--smaperiod SMAPERIOD]
                                  [--exectype EXECTYPE] [--valid VALID]
                                  [--perc1 PERC1] [--perc2 PERC2]
完整代码#
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse
import datetime
import os.path
import time
import sys

import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicators as btind

class OrderExecutionStrategy(bt.Strategy):
    params = (
        ('smaperiod', 15),
        ('exectype', 'Market'),
        ('perc1', 3),
        ('perc2', 1),
        ('valid', 4),
    )

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.data.datetime[0]
        if isinstance(dt, float):
            dt = bt.num2date(dt)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            self.log('ORDER ACCEPTED/SUBMITTED', dt=order.created.dt)
            self.order = order
            return

        if order.status in [order.Expired]:
            self.log('BUY EXPIRED')

        elif order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

        # Sentinel to None: new orders allowed
        self.order = None

    def __init__(self):
        # SimpleMovingAverage on main data
        # Equivalent to -> sma = btind.SMA(self.data, period=self.p.smaperiod)
        sma = btind.SMA(period=self.p.smaperiod)

        # CrossOver (1: up, -1: down) close / sma
        self.buysell = btind.CrossOver(self.data.close, sma, plot=True)

        # Sentinel to None: new orders allowed
        self.order = None

    def next(self):
        if self.order:
            # An order is pending ... nothing can be done
            return

        # Check if we are in the market
        if self.position:
            # In the market - check if it's the time to sell
            if self.buysell < 0:
                self.log('SELL CREATE, %.2f' % self.data.close[0])
                self.sell()

        elif self.buysell > 0:
            if self.p.valid:
                valid = self.data.datetime.date(0) + \
                        datetime.timedelta(days=self.p.valid)
            else:
                valid = None

            # Not in the market and signal to buy
            if self.p.exectype == 'Market':
                self.buy(exectype=bt.Order.Market)  # default if not given

                self.log('BUY CREATE, exectype Market, price %.2f' %
                         self.data.close[0])

            elif self.p.exectype == 'Close':
                self.buy(exectype=bt.Order.Close)

                self.log('BUY CREATE, exectype Close, price %.2f' %
                         self.data.close[0])

            elif self.p.exectype == 'Limit':
                price = self.data.close * (1.0 - self.p.perc1 / 100.0)

                self.buy(exectype=bt.Order.Limit, price=price, valid=valid)

                if self.p.valid:
                    txt = 'BUY CREATE, exectype Limit, price %.2f, valid: %s'
                    self.log(txt % (price, valid.strftime('%Y-%m-%d')))
                else:
                    txt = 'BUY CREATE, exectype Limit, price %.2f'
                    self.log(txt % price)

            elif self.p.exectype == 'Stop':
                price = self.data.close * (1.0 + self.p.perc1 / 100.0)

                self.buy(exectype=bt.Order.Stop, price=price, valid=valid)

                if self.p.valid:
                    txt = 'BUY CREATE, exectype Stop, price %.2f, valid: %s'
                    self.log(txt % (price, valid.strftime('%Y-%m-%d')))
                else:
                    txt = 'BUY CREATE, exectype Stop, price %.2f'
                    self.log(txt % price)

            elif self.p.exectype == 'StopLimit':
                price = self.data.close * (1.0 + self.p.perc1 / 100.0)

                plimit = self.data.close * (1.0 + self.p.perc2 / 100.0)

                self.buy(exectype=bt.Order.StopLimit, price=price, valid=valid,
                         plimit=plimit)

                if self.p.valid:
                    txt = ('BUY CREATE, exectype StopLimit, price %.2f,'
                           ' valid: %s, pricelimit: %.2f')
                    self.log(txt % (price, valid.strftime('%Y-%m-%d'), plimit))
                else:
                    txt = ('BUY CREATE, exectype StopLimit, price %.2f,'
                           ' pricelimit: %.2f')
                    self.log(txt % (price, plimit))

def runstrat():
    args = parse_args()

    cerebro = bt.Cerebro()

    data = getdata(args)
    cerebro.adddata(data)

    cerebro.addstrategy(
        OrderExecutionStrategy,
        exectype=args.exectype,
        perc1=args.perc1,
        perc2=args.perc2,
        valid=args.valid,
        smaperiod=args.smaperiod
    )
    cerebro.run()

    if args.plot:
        cerebro.plot(numfigs=args.numfigs, style=args.plotstyle)

def getdata(args):
    dataformat = dict(
        bt=btfeeds.BacktraderCSVData,
        visualchart=btfeeds.VChartCSVData,
        sierrachart=btfeeds.SierraChartCSVData,
        yahoo=btfeeds.YahooFinanceCSVData,
        yahoo_unreversed=btfeeds.YahooFinanceCSVData
    )

    dfkwargs = dict()
    if args.csvformat == 'yahoo_unreversed':
        dfkwargs['reverse'] = True

    if args.fromdate:
        fromdate = datetime.datetime.strptime(args.fromdate, '%Y-%m-%d')
        dfkwargs['fromdate'] = fromdate

    if args.todate:
        fromdate = datetime.datetime.strptime(args.todate, '%Y-%m-%d')
        dfkwargs['todate'] = todate

   

 dfkwargs['dataname'] = args.infile

    dfcls = dataformat[args.csvformat]

    return dfcls(**dfkwargs)

def parse_args():
    parser = argparse.ArgumentParser(
        description='Showcase for Order Execution Types')

    parser.add_argument('--infile', '-i', required=False,
                        default='../../datas/2006-day-001.txt',
                        help='File to be read in')

    parser.add_argument('--csvformat', '-c', required=False, default='bt',
                        choices=['bt', 'visualchart', 'sierrachart',
                                 'yahoo', 'yahoo_unreversed'],
                        help='CSV Format')

    parser.add_argument('--fromdate', '-f', required=False, default=None,
                        help='Starting date in YYYY-MM-DD format')

    parser.add_argument('--todate', '-t', required=False, default=None,
                        help='Ending date in YYYY-MM-DD format')

    parser.add_argument('--plot', '-p', action='store_false', required=False,
                        help='Plot the read data')

    parser.add_argument('--plotstyle', '-ps', required=False, default='bar',
                        choices=['bar', 'line', 'candle'],
                        help='Plot the read data')

    parser.add_argument('--numfigs', '-n', required=False, default=1,
                        help='Plot using n figures')

    parser.add_argument('--smaperiod', '-s', required=False, default=15,
                        help='Simple Moving Average Period')

    parser.add_argument('--exectype', '-e', required=False, default='Market',
                        help=('Execution Type: Market (default), Close, Limit,'
                              ' Stop, StopLimit'))

    parser.add_argument('--valid', '-v', required=False, default=0, type=int,
                        help='Validity for Limit sample: default 0 days')

    parser.add_argument('--perc1', '-p1', required=False, default=0.0,
                        type=float,
                        help=('%% distance from close price at order creation'
                              ' time for the limit/trigger price in Limit/Stop'
                              ' orders'))

    parser.add_argument('--perc2', '-p2', required=False, default=0.0,
                        type=float,
                        help=('%% distance from close price at order creation'
                              ' time for the limit price in StopLimit orders'))

    return parser.parse_args()

if __name__ == '__main__':
    runstrat()
############################################################################################################################
目标订单#
在 1.8.10.96 版本之前，策略方法 buy 和 sell 可通过 sizer 实现智能持仓，sizer 负责确定持仓的大小。然而，Sizer 不能决定操作是买入还是卖出。这就需要一个新的概念，在决策中加入一个小的智能层。这就是策略中的order_target_xxx方法家族。

受 zipline 的启发，这些方法提供了简单指定最终目标的机会，无论目标是：

size -> 特定资产的股份或合约数量
value -> 资产在投资组合中的货币单位价值
percent -> 当前投资组合中资产的百分比值
注意：这些方法的在 Strategy 类的参考文档中可以找到。简言之，这些方法使用与 buy 和 sell 相同的参数签名，只是将 size 参数替换为 target 参数。

这些方法的核心在于指定最终目标，然后方法决定操作是买入还是卖出。所有三种方法的逻辑相同。以下是order_target_size的工作方式：

如果目标大于当前仓位，则发出买入指令，买入的数量为target - position_size。例如：

仓位：0，目标：7 -> buy(size=7 - 0) -> buy(size=7)
仓位：3，目标：7 -> buy(size=7 - 3) -> buy(size=4)
仓位：-3，目标：7 -> buy(size=7 - -3) -> buy(size=10)
仓位：-3，目标：-2 -> buy(size=-2 - -3) -> buy(size=1)
如果目标小于当前仓位，则发出卖出指令，卖出的数量为position_size - target。例如：

仓位：0，目标：-7 -> sell(size=0 - -7) -> sell(size=7)
仓位：3，目标：-7 -> sell(size=3 - -7) -> sell(size=10)
仓位：-3，目标：-7 -> sell(size=-3 - -7) -> sell(size=4)
仓位：3，目标：2 -> sell(size=3 - 2) -> sell(size=1)
当使用order_target_value设定目标值时，会考虑资产在投资组合中的当前价值和持仓量，以决定最终的操作。逻辑如下：

如果目标值大于当前值且仓位>=0 -> 买入
如果目标值大于当前值且仓位<0 -> 卖出
如果目标值小于当前值且仓位>=0 -> 卖出
如果目标值小于当前值且仓位<0 -> 买入
order_target_percent 的逻辑与 order_target_value 相同。该方法简单地根据当前投资组合的总价值确定资产的目标价值。

示例#
Backtrader 尝试为每个新功能提供一个示例，这也不例外。该示例在 samples 目录下的 order_target 子目录中。示例逻辑比较简单，仅用于测试结果是否如预期：

在奇数月（1月、3月等），使用日期作为目标（在 order_target_value 的情况下，将日期乘以1000）；
在偶数月（2月、4月等），使用31减去日期作为目标；
order_target_size#
我们来看1月和2月的情况。

$ ./order_target.py --target-size --plot
0001 - 2005-01-03 - Position Size:     00 - Value 1000000.00
0001 - 2005-01-03 - Order Target Size: 03
0002 - 2005-01-04 - Position Size:     03 - Value 999994.39
0002 - 2005-01-04 - Order Target Size: 04
0003 - 2005-01-05 - Position Size:     04 - Value 999992.48
0003 - 2005-01-05 - Order Target Size: 05
0004 - 2005-01-06 - Position Size:     05 - Value 999988.79
...
0020 - 2005-01-31 - Position Size:     28 - Value 999968.70
0020 - 2005-01-31 - Order Target Size: 31
0021 - 2005-02-01 - Position Size:     31 - Value 999954.68
0021 - 2005-02-01 - Order Target Size: 30
0022 - 2005-02-02 - Position Size:     30 - Value 999979.65
0022 - 2005-02-02 - Order Target Size: 29
0023 - 2005-02-03 - Position Size:     29 - Value 999966.33
0023 - 2005-02-03 - Order Target Size: 28
...
在1月，目标从年初第一个交易日的3开始增加。持仓量从0增加到3，然后每次增加1。

在1月结束时，最后一个目标是31，当进入2月时，该持仓量被报告出来，新的目标变为30，并以1的递减变化。

order_target_value#
期望有类似的行为：

$ ./order_target.py --target-value --plot
0001 - 2005-01-03 - Position Size:     00 - Value 1000000.00
0001 - 2005-01-03 - data value 0.00
0001 - 2005-01-03 - Order Target Value: 3000.00
0002 - 2005-01-04 - Position Size:     78 - Value 999854.14
0002 - 2005-01-04 - data value 2853.24
0002 - 2005-01-04 - Order Target Value: 4000.00
0003 - 2005-01-05 - Position Size:     109 - Value 999801.68
0003 - 2005-01-05 - data value 3938.17
0003 - 2005-01-05 - Order Target Value: 5000.00
0004 - 2005-01-06 - Position Size:     138 - Value 999699.57
...
0020 - 2005-01-31 - Position Size:     808 - Value 999206.37
0020 - 2005-01-31 - data value 28449.68
0020 - 2005-01-31 - Order Target Value: 31000.00
0021 - 2005-02-01 - Position Size:     880 - Value 998807.33
0021 - 2005-02-01 - data value 30580.00
0021 - 2005-02-01 - Order Target Value: 30000.00
0022 - 2005-02-02 - Position Size:     864 - Value 999510.21
0022 - 2005-02-02 - data value 30706.56
0022 - 2005-02-02 - Order Target Value: 29000.00
0023 - 2005-02-03 - Position Size:     816 - Value 999130.05
0023 - 2005-02-03 - data value 28633.44
0023 - 2005-02-03 - Order Target Value: 28000.00
...
order_target_percent#
此方法仅计算当前投资组合价值的百分比：

$ ./order_target.py --target-percent --plot
0001 - 2005-01-03 - Position Size:     00 - Value 1000000.00
0001 - 2005-01-03 - data percent 0.00
0001 - 2005-01-03 - Order Target Percent: 0.03
0002 - 2005-01-04 - Position Size:     785 - Value 998532.05
0002 - 2005-01-04 - data percent 0.03
0002 - 2005-01-04 - Order Target Percent: 0.04
0003 - 2005-01-05 - Position Size:     1091 - Value 998007.44
0003 - 2005-01-05 - data percent 0.04
0003 - 2005-01-05 - Order Target Percent: 0.05
0004 - 2005-01-06 - Position Size:     1381 - Value 996985.64
...
0020 - 2005-01-31 - Position Size:     7985 - Value 991966.28
0020 - 2005-01-31 - data percent 0.28
0020 - 2005-01-31 - Order Target Percent: 0.31
0021 - 2005-02-01 - Position Size:     8733 - Value 988008.94
0021 - 2005-02-01 - data percent 0.31
0021 - 2005-02-01 - Order Target Percent: 0.30
0022 - 2005-02-02 - Position Size:     8530 - Value 995005.45
0022 - 2005-02-02 - data percent 0.30
0022 - 2005-02-02 - Order Target Percent: 0.29
0023 - 2005-02-03 - Position Size:     8120 - Value 991240.75
0023 - 2005-02-03 - data percent 0.29
0023 - 2005-02-03 - Order Target Percent: 0.28
...
示例使用#
$ ./order_target.py --help
usage: order_target.py [-h] [--data DATA] [--fromdate FROMDATE]
                       [--todate TODATE] [--cash CASH]
                       (--target-size | --target-value | --target-percent)
                       [--plot [kwargs]]

Sample for Order Target

optional arguments:
  -h, --help            show this help message and exit
  --data DATA           Specific data to be read in (default:
                        ../../datas/yhoo-1996-2015.txt)
  --fromdate FROMDATE   Starting date in YYYY-MM-DD format (default:
                        2005-01-01)
  --todate TODATE       Ending date in YYYY-MM-DD format (default: 2006-12-31)
  --cash CASH           Ending date in YYYY-MM-DD format (default: 1000000)
  --target-size         Use order_target_size (default: False)
  --target-value        Use order_target_value (default: False)
  --target-percent      Use order_target_percent (default: False)
  --plot [kwargs], -p [kwargs]
                        Plot the read data applying any kwargs passed For
                        example: --plot style="candle" (to plot candles)
                        (default: None)
#######################################################################################
OCO订单#
使用模式尽量保持简单。因此，如果策略中的逻辑决定是时候发布订单，可以像这样使用 OCO：

def next(self):
    ...
    o1 = self.buy(...)
    ...
    o2 = self.buy(..., oco=o1)
    ...
    o3 = self.buy(..., oco=o1)  # 甚至可以是oco=o2，o2已经在o1组中
很简单，第一个订单 o1 将成为组长。通过指定 oco 命名参数，o2 和 o3 成为 OCO 组的一部分。请注意，代码注释指出 o3 也可以通过指定 o2 成为组的一部分（o2已经是组的一部分）。

一旦成功组成组后，如果组中的任何订单被执行、取消或过期，其他订单将被取消。

下面的示例展示了OCO概念。一个标准执行并绘图：

$ ./oco.py --broker cash=50000 --plot
注意

现金增加到50000，因为资产价值达到4000，3个订单的1个项目至少需要12000货币单位（经纪商默认值为10000）。

以下图表实际上没有提供太多信息（这是一个标准的SMA交叉策略）。

示例执行，当快速SMA上穿慢速SMA时，发布3个订单。

order1是一个限价订单，在limdays天后到期，限价为收盘价减少一个百分比。
order2是一个期限更长、限价更低的限价订单。
order3是一个限价更低的限价订单。
因此，order2 和 order3 不会执行，因为：

order1将首先执行，这将触发其他订单的取消。
或者order1将过期，这将触发其他订单的取消。
系统保存了3个订单的ref标识符，并且只有在notify_order中看到三个ref标识符分别为Completed、Cancelled、Margin或Expired时，才会发布新买单。

退出是在持有一段时间后后简单完成的。

为了跟踪实际执行，生成文本输出。部分内容如下：

2005-01-28: Oref 1 / Buy at 2941.11055
2005-01-28: Oref 2 / Buy at 2896.7722
2005-01-28: Oref 3 / Buy at 2822.87495
2005-01-31: Order ref: 1 / Type Buy / Status Submitted
2005-01-31: Order ref: 2 / Type Buy / Status Submitted
2005-01-31: Order ref: 3 / Type Buy / Status Submitted
2005-01-31: Order ref: 1 / Type Buy / Status Accepted
2005-01-31: Order ref: 2 / Type Buy / Status Accepted
2005-01-31: Order ref: 3 / Type Buy / Status Accepted
2005-02-01: Order ref: 1 / Type Buy / Status Expired
2005-02-01: Order ref: 3 / Type Buy / Status Canceled
2005-02-01: Order ref: 2 / Type Buy / Status Canceled
...
2006-06-23: Oref 49 / Buy at 3532.39925
2006-06-23: Oref 50 / Buy at 3479.147
2006-06-23: Oref 51 / Buy at 3390.39325
2006-06-26: Order ref: 49 / Type Buy / Status Submitted
2006-06-26: Order ref: 50 / Type Buy / Status Submitted
2006-06-26: Order ref: 51 / Type Buy / Status Submitted
2006-06-26: Order ref: 49 / Type Buy / Status Accepted
2006-06-26: Order ref: 50 / Type Buy / Status Accepted
2006-06-26: Order ref: 51 / Type Buy / Status Accepted
2006-06-26: Order ref: 49 / Type Buy / Status Completed
2006-06-26: Order ref: 51 / Type Buy / Status Canceled
2006-06-26: Order ref: 50 / Type Buy / Status Canceled
...
2006-11-10: Order ref: 61 / Type Buy / Status Canceled
2006-12-11: Oref 63 / Buy at 4032.62555
2006-12-11: Oref 64 / Buy at 3971.8322
2006-12-11: Oref 65 / Buy at 3870.50995
2006-12-12: Order ref: 63 / Type Buy / Status Submitted
2006-12-12: Order ref: 64 / Type Buy / Status Submitted
2006-12-12: Order ref: 65 / Type Buy / Status Submitted
2006-12-12: Order ref: 63 / Type Buy / Status Accepted
2006-12-12: Order ref: 64 / Type Buy / Status Accepted
2006-12-12: Order ref: 65 / Type Buy / Status Accepted
2006-12-15: Order ref: 63 / Type Buy / Status Expired
2006-12-15: Order ref: 65 / Type Buy / Status Canceled
2006-12-15: Order ref: 64 / Type Buy / Status Canceled
以下情况发生：

第一批订单发布。订单1到期，订单2和3被取消。预期结果。
几个月后发布另一批3个订单。在这种情况下，订单49完成，订单50和51立即取消。
最后一批订单与第一批订单相同。
现在检查不使用 OCO 的行为：

$ ./oco.py --strat do_oco=False --broker cash=50000
2005-01-28: Oref 1 / Buy at 2941.11055
2005-01-28: Oref 2 / Buy at 2896.7722
2005-01-28: Oref 3 / Buy at 2822.87495
2005-01-31: Order ref: 1 / Type Buy / Status Submitted
2005-01-31: Order ref: 2 / Type Buy / Status Submitted
2005-01-31: Order ref: 3 / Type Buy / Status Submitted
2005-01-31: Order ref: 1 / Type Buy / Status Accepted
2005-01-31: Order ref: 2 / Type Buy / Status Accepted
2005-01-31: Order ref: 3 / Type Buy / Status Accepted
2005-02-01: Order ref: 1 / Type Buy / Status Expired
结果不多（没有订单执行，图表也没有太多需求）。

发布了一批订单。

订单1过期，但因为策略参数 do_oco =False，订单2和3未加入OCO组，因此订单2和3未被取消，由于默认到期时间为1000天，样本可用数据（2年数据）内它们永不过期。

系统从未发布第二批订单。

示例使用#
$ ./oco.py --help
usage: oco.py [-h] [--data0 DATA0] [--fromdate FROMDATE] [--todate TODATE]
              [--cerebro kwargs] [--broker kwargs] [--sizer kwargs]
              [--strat kwargs] [--plot [kwargs]]

Sample Skeleton

optional arguments:
  -h, --help           show this help message and exit
  --data0 DATA0        Data to read in (default:
                       ../../datas/2005-2006-day-001.txt)
  --fromdate FROMDATE  Date[time] in YYYY-MM-DD[THH:MM:SS] format (default: )
  --todate TODATE      Date[time] in YYYY-MM-DD[THH:MM:SS] format (default: )
  --cerebro kwargs     kwargs in key=value format (default: )
  --broker kwargs      kwargs in key=value format (default: )
  --sizer kwargs       kwargs in key=value format (default: )
  --strat kwargs       kwargs in key=value format (default: )
  --plot [kwargs]      kwargs in key=value format (default: )
示例代码#
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse
import datetime
import backtrader as bt


class St(bt.Strategy):
    params = dict(
        ma=bt.ind.SMA,
        p1=5,
        p2=15,
        limit=0.005,
        limdays=3,
        limdays2=1000,
        hold=10,
        switchp1p2=False,  # switch prices of order1 and order2
        oco1oco2=False,

  # False - use order1 as oco for order3, else order2
        do_oco=True,  # use oco or not
    )

    def notify_order(self, order):
        print('{}: Order ref: {} / Type {} / Status {}'.format(
            self.data.datetime.date(0),
            order.ref, 'Buy' * order.isbuy() or 'Sell',
            order.getstatusname()))

        if order.status == order.Completed:
            self.holdstart = len(self)

        if not order.alive() and order.ref in self.orefs:
            self.orefs.remove(order.ref)

    def __init__(self):
        ma1, ma2 = self.p.ma(period=self.p.p1), self.p.ma(period=self.p.p2)
        self.cross = bt.ind.CrossOver(ma1, ma2)

        self.orefs = list()

    def next(self):
        if self.orefs:
            return  # pending orders do nothing

        if not self.position:
            if self.cross > 0.0:  # crossing up

                p1 = self.data.close[0] * (1.0 - self.p.limit)
                p2 = self.data.close[0] * (1.0 - 2 * 2 * self.p.limit)
                p3 = self.data.close[0] * (1.0 - 3 * 3 * self.p.limit)

                if self.p.switchp1p2:
                    p1, p2 = p2, p1

                o1 = self.buy(exectype=bt.Order.Limit, price=p1,
                              valid=datetime.timedelta(self.p.limdays))

                print('{}: Oref {} / Buy at {}'.format(
                    self.datetime.date(), o1.ref, p1))

                oco2 = o1 if self.p.do_oco else None
                o2 = self.buy(exectype=bt.Order.Limit, price=p2,
                              valid=datetime.timedelta(self.p.limdays2),
                              oco=oco2)

                print('{}: Oref {} / Buy at {}'.format(
                    self.datetime.date(), o2.ref, p2))

                if self.p.do_oco:
                    oco3 = o1 if not self.p.oco1oco2 else oco2
                else:
                    oco3 = None

                o3 = self.buy(exectype=bt.Order.Limit, price=p3,
                              valid=datetime.timedelta(self.p.limdays2),
                              oco=oco3)

                print('{}: Oref {} / Buy at {}'.format(
                    self.datetime.date(), o3.ref, p3))

                self.orefs = [o1.ref, o2.ref, o3.ref]

        else:  # in the market
            if (len(self) - self.holdstart) >= self.p.hold:
                self.close()


def runstrat(args=None):
    args = parse_args(args)

    cerebro = bt.Cerebro()

    # Data feed kwargs
    kwargs = dict()

    # Parse from/to-date
    dtfmt, tmfmt = '%Y-%m-%d', 'T%H:%M:%S'
    for a, d in ((getattr(args, x), x) for x in ['fromdate', 'todate']):
        if a:
            strpfmt = dtfmt + tmfmt * ('T' in a)
            kwargs[d] = datetime.datetime.strptime(a, strpfmt)

    # Data feed
    data0 = bt.feeds.BacktraderCSVData(dataname=args.data0, **kwargs)
    cerebro.adddata(data0)

    # Broker
    cerebro.broker = bt.brokers.BackBroker(**eval('dict(' + args.broker + ')'))

    # Sizer
    cerebro.addsizer(bt.sizers.FixedSize, **eval('dict(' + args.sizer + ')'))

    # Strategy
    cerebro.addstrategy(St, **eval('dict(' + args.strat + ')'))

    # Execute
    cerebro.run(**eval('dict(' + args.cerebro + ')'))

    if args.plot:  # Plot if requested to
        cerebro.plot(**eval('dict(' + args.plot + ')'))


def parse_args(pargs=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=(
            'Sample Skeleton'
        )
    )

    parser.add_argument('--data0', default='../../datas/2005-2006-day-001.txt',
                        required=False, help='Data to read in')

    # Defaults for dates
    parser.add_argument('--fromdate', required=False, default='',
                        help='Date[time] in YYYY-MM-DD[THH:MM:SS] format')

    parser.add_argument('--todate', required=False, default='',
                        help='Date[time] in YYYY-MM-DD[THH:MM:SS] format')

    parser.add_argument('--cerebro', required=False, default='',
                        metavar='kwargs', help='kwargs in key=value format')

    parser.add_argument('--broker', required=False, default='',
                        metavar='kwargs', help='kwargs in key=value format')

    parser.add_argument('--sizer', required=False, default='',
                        metavar='kwargs', help='kwargs in key=value format')

    parser.add_argument('--strat', required=False, default='',
                        metavar='kwargs', help='kwargs in key=value format')

    parser.add_argument('--plot', required=False, default='',
                        nargs='?', const='{}',
                        metavar='kwargs', help='kwargs in key=value format')

    return parser.parse_args(pargs)


if __name__ == '__main__':
    runstrat()
###################################################################################################################################
Bracket Orders#
1.9.37.116版本增加了Bracket订单，为回测经纪商提供了广泛的订单支持（Market、Limit、Close、Stop、StopLimit、StopTrail、StopTrailLimit、OCO）。

注意，这是为回测和 Interactive Brokers 实现的。

Bracket订单不是单个订单，而是由3个订单组成。

以做多为例：

一个主要的买单，通常设置为 Limit 或 StopLimit 订单。
一个低价卖单，通常设置为 Stop 订单以限制损失。
一个高价卖单，通常设置为 Limit 订单以获取利润。
做空也有对应的卖单和 2 个买单。

低价/高价卖单实际上形成了一个围绕主要订单的 Bracket。

为了使其合理，以下规则适用：

3个订单一起提交，以避免其中任何一个独立触发。
低价/高价卖单被标记为主要订单的子订单。
子订单在主要订单执行之前不活跃。
取消主要订单会取消低价和高价卖单。
执行主要订单会激活低价和高价卖单。
一旦活跃，低价/高价卖单的执行或取消会自动取消另一个订单。
使用模式#
有两种方式创建 Bracket 订单组：

单次发布3个订单。
手动发布3个订单。
单次发布Bracket#
backtrader在Strategy中提供了两个新方法来控制Bracket订单：buy_bracket和sell_bracket。

注意

签名和信息见下文或Strategy参考部分。

通过单个语句完成3个订单的设置。示例如下：

brackets = self.buy_bracket(limitprice=14.00, price=13.50, stopprice=13.00)
注意，stopprice和limitprice围绕price设定。这应该足够了。

实际的目标数据将是 data0，大小将由默认的sizer自动确定。当然，可以指定其他参数来精细控制执行。

返回值是一个包含3个订单的列表：[主要订单，stop订单，limit订单]。

因为在发布 sell_bracket 订单时，低价和高价将翻转，所以参数命名遵循约定：stop 用于止损（在做多操作中是低价，在做空操作中是高价），limit 用于获取利润（在做多操作中是高价，在做空操作中是低价）。

手动发布Bracket#
这涉及生成3个订单，并处理transmit和parent参数。规则如下：

必须首先创建主要订单并设置transmit=False。
低价/高价订单必须有parent=main_side_order。
第一个创建的低价/高价订单必须设置transmit=False。
最后一个创建的订单（无论是低价还是高价）设置transmit=True。
以下示例实现了与上述单次命令相同的效果：

mainside = self.buy(price=13.50, exectype=bt.Order.Limit, transmit=False)
lowside  = self.sell(price=13.00, size=mainside.size, exectype=bt.Order.Stop, transmit=False, parent=mainside)
highside = self.sell(price=14.00, size=mainside.size, exectype=bt.Order.Limit, transmit=True, parent=mainside)
需要做更多的事情：

跟踪主要订单，指示它是其他订单的父订单。
控制transmit以确保只有最后一个订单触发联合传输。
指定执行类型。
为低价和高价订单指定大小。
因为大小必须相同。如果未手动指定大小且用户引入了sizer，sizer可能会为订单指示不同的值。因此，需要在调用时手动添加大小。

示例#
运行下面的示例生成如下输出（为简洁起见进行了截断）：

$ ./bracket.py --plot

2005-01-28: Oref 1 / Buy at 2941.11055
2005-01-28: Oref 2 / Sell Stop at 2881.99275
2005-01-28: Oref 3 / Sell Limit at 3000.22835
2005-01-31: Order ref: 1 / Type Buy / Status Submitted
2005-01-31: Order ref: 2 / Type Sell / Status Submitted
2005-01-31: Order ref: 3 / Type Sell / Status Submitted
2005-01-31: Order ref: 1 / Type Buy / Status Accepted
2005-01-31: Order ref: 2 / Type Sell / Status Accepted
2005-01-31: Order ref: 3 / Type Sell / Status Accepted
2005-02-01: Order ref: 1 / Type Buy / Status Expired
2005-02-01: Order ref: 2 / Type Sell / Status Canceled
2005-02-01: Order ref: 3 / Type Sell / Status Canceled
...
2005-08-11: Oref 16 / Buy at 3337.3892
2005-08-11: Oref 17 / Sell Stop at 3270.306
2005-08-11: Oref 18 / Sell Limit at 3404.4724
2005-08-12: Order ref: 16 / Type Buy / Status Submitted
2005-08-12: Order ref: 17 / Type Sell / Status Submitted
2005-08-12: Order ref: 18 / Type Sell / Status Submitted
2005-08-12: Order ref: 16 / Type Buy / Status Accepted
2005-08-12: Order ref: 17 / Type Sell / Status Accepted
2005-08-12: Order ref: 18 / Type Sell / Status Accepted
2005-08-12: Order ref: 16 / Type Buy / Status Completed
2005-08-18: Order ref: 17 / Type Sell / Status Completed
2005-08-18: Order ref: 18 / Type Sell / Status Canceled
...
2005-09-26: Oref 22 / Buy at 3383.92535
2005-09-26: Oref 23 / Sell Stop at 3315.90675
2005-09-26: Oref 24 / Sell Limit at 3451.94395
2005-09-27: Order ref: 22 / Type Buy / Status Submitted
2005-09-27: Order ref: 23 / Type Sell / Status Submitted
2005-09-27: Order ref: 24 / Type Sell / Status Submitted
2005-09-27: Order ref: 22 / Type Buy / Status Accepted
2005-09-27: Order ref: 23 / Type Sell / Status Accepted
2005-09-27: Order ref: 24 / Type Sell / Status Accepted
2005-09-27: Order ref: 22 / Type Buy / Status Completed
2005-10-04: Order ref: 24 / Type Sell / Status Completed
2005-10-04: Order ref: 23 / Type Sell / Status Canceled
...
显示了 3 种不同的结果：

第一种情况下，主要订单过期，自动取消了其他两个订单。
第二种情况下，主要订单完成，低价订单（买入情况下的止损）执行，限制了损失。
第三种情况下，主要订单完成，高价订单（限价）执行。
可以注意到，已完成的订单id是22和24，高价订单最后发布，未执行的低价订单id是23。

图示

可以立即看到，亏损交易集中在相同的值附近，而盈利交易也是如此，这是 Bracket 的目的。控制两侧。

运行的示例手动发布3个订单，但可以使用buy_bracket。输出如下：

$ ./bracket.py --strat usebracket=True
结果相同。

参考#
请参阅新的buy_bracket和sell_bracket方法

def buy_bracket(self, data=None, size=None, price=None, plimit=None,
                exectype=bt.Order.Limit, valid=None, tradeid=0,
                trailamount=None, trailpercent=None, oargs={},
                stopprice=None, stopexec=bt.Order.Stop, stopargs={},
                limitprice=None, limitexec=bt.Order.Limit, limitargs={},
                **kwargs):
    '''
    创建一个Bracket订单组（低侧 - 买单 - 高侧）。默认行为如下：

      - 发出执行类型为“Limit”的**买单**

      - 发出执行类型为“Stop”的*低侧*Bracket**卖单**

      - 发出执行类型为“Limit”的*高侧*Bracket**卖单**。

    参见下文以了解不同参数的含义

      - ``data``（默认：``None``）

        订单针对的数据。如果为``None``，则使用系统中的第一个数据，即``self.datas[0

]或self.data0``（即``self.data``）

      - ``size``（默认：``None``）

        订单的数据单位大小（正数）。

        如果为``None``，则使用通过``getsizer``检索到的``sizer``实例来确定大小。

        **注意**：相同的大小适用于Bracket的所有3个订单

      - ``price``（默认：``None``）

        使用的价格（实时经纪商可能会对实际格式施加限制，如果不符合最小价格单位要求）

        ``None``对于``Market``和``Close``订单是有效的（市场决定价格）

        对于``Limit``、``Stop``和``StopLimit``订单，此值确定触发点（在``Limit``的情况下，触发点显然是订单应匹配的价格）

      - ``plimit``（默认：``None``）

        仅适用于``StopLimit``订单。这是设置隐含限价订单的价格，一旦触发了``Stop``（使用``price``）

      - ``trailamount``（默认：``None``）

        如果订单类型为StopTrail或StopTrailLimit，这是一个绝对金额，确定价格的距离（卖单下方和买单上方），以保持追踪止损

      - ``trailpercent``（默认：``None``）

        如果订单类型为StopTrail或StopTrailLimit，这是一个百分比金额，确定价格的距离（卖单下方和买单上方），以保持追踪止损（如果也指定了``trailamount``，将使用它）

      - ``exectype``（默认：``bt.Order.Limit``）

        可能的值：（参见``buy``方法的文档）

      - ``valid``（默认：``None``）

        可能的值：（参见``buy``方法的文档）

      - ``tradeid``（默认：``0``）

        可能的值：（参见``buy``方法的文档）

      - ``oargs``（默认：``{}``）

        要传递给主要订单的特定关键字参数（在``dict``中）。默认``**kwargs``中的参数将应用于此。

      - ``**kwargs``：其他经纪商实现可能支持的额外参数。``backtrader``将*kwargs*传递给创建的订单对象

        可能的值：（参见``buy``方法的文档）

        **注意**：此``kwargs``将应用于Bracket的所有3个订单。参见下文以了解低侧和高侧订单的特定关键字参数

      - ``stopprice``（默认：``None``）

        *低侧*止损订单的特定价格

      - ``stopexec``（默认：``bt.Order.Stop``）

        *低侧*订单的特定执行类型

      - ``stopargs``（默认：``{}``）

        要传递给低侧订单的特定关键字参数（在``dict``中）。默认``**kwargs``中的参数将应用于此。

      - ``limitprice``（默认：``None``）

        *高侧*止损订单的特定价格

      - ``stopexec``（默认：``bt.Order.Limit``）

        *高侧*订单的特定执行类型

      - ``limitargs``（默认：``{}``）

        要传递给高侧订单的特定关键字参数（在``dict``中）。默认``**kwargs``中的参数将应用于此。

    返回：
      - 一个包含3个Bracket订单的列表[订单，低侧，高侧]
    '''

def sell_bracket(self, data=None,
                 size=None, price=None, plimit=None,
                 exectype=bt.Order.Limit, valid=None, tradeid=0,
                 trailamount=None, trailpercent=None,
                 oargs={},
                 stopprice=None, stopexec=bt.Order.Stop, stopargs={},
                 limitprice=None, limitexec=bt.Order.Limit, limitargs={},
                 **kwargs):
    '''
    创建一个Bracket订单组（低侧 - 卖单 - 高侧）。默认行为如下：

      - 发出执行类型为“Limit”的**卖单**

      - 发出执行类型为“Stop”的*高侧*Bracket**买单**

      - 发出执行类型为“Limit”的*低侧*Bracket**买单**。

    参见``bracket_buy``以了解参数的含义

    返回：
      - 一个包含3个Bracket订单的列表[订单，低侧，限价侧]
    '''
示例用法#
$ ./bracket.py --help
usage: bracket.py [-h] [--data0 DATA0] [--fromdate FROMDATE] [--todate TODATE]
                  [--cerebro kwargs] [--broker kwargs] [--sizer kwargs]
                  [--strat kwargs] [--plot [kwargs]]

Sample Skeleton

optional arguments:
  -h, --help           show this help message and exit
  --data0 DATA0        Data to read in (default:
                       ../../datas/2005-2006-day-001.txt)
  --fromdate FROMDATE  Date[time] in YYYY-MM-DD[THH:MM:SS] format (default: )
  --todate TODATE      Date[time] in YYYY-MM-DD[THH:MM:SS] format (default: )
  --cerebro kwargs     kwargs in key=value format (default: )
  --broker kwargs      kwargs in key=value format (default: )
  --sizer kwargs       kwargs in key=value format (default: )
  --strat kwargs       kwargs in key=value format (default: )
  --plot [kwargs]      kwargs in key=value format (default: )
示例代码#
from __future__ import (absolute_import, division, print_function, unicode_literals)

import argparse
import datetime
import backtrader as bt

class St(bt.Strategy):
    params = dict(
        ma=bt.ind.SMA,
        p1=5,
        p2=15,
        limit=0.005,
        limdays=3,
        limdays2=1000,
        hold=10,
        usebracket=False,  # use order_target_size
        switchp1p2=False,  # switch prices of order1 and order2
    )

    def notify_order(self, order):
        print('{}: Order ref: {} / Type {} / Status {}'.format(
            self.data.datetime.date(0),
            order.ref, 'Buy' * order.isbuy() or 'Sell',
            order.getstatusname()))

        if order.status == order.Completed:
            self.holdstart = len(self)

        if not order.alive() and order.ref in self.orefs:
            self.orefs.remove(order.ref)

    def __init__(self):
        ma1, ma2 = self.p.ma(period=self.p.p1), self.p.ma(period=self.p.p2)
        self.cross = bt.ind.CrossOver(ma1, ma2)
        self.orefs = list()

        if self.p.usebracket:
            print('-' * 5, 'Using buy_bracket')

    def next(self):
        if self.orefs:
            return  # pending orders do nothing

        if not self.position:
            if self.cross > 0.0:  # crossing up
                close = self.data.close[0]
                p1 = close * (1.0 - self.p.limit)
                p2 = p1 - 0.02 * close
                p3 = p1 + 0.02 * close

                valid1 = datetime.timedelta(self.p.limdays)
                valid2 = valid3 = datetime.timedelta(self.p.limdays2)

                if self.p.switchp1p2:
                    p1, p2 = p2, p1
                    valid1, valid2 = valid2, valid1

                if not self.p.usebracket:
                    o1 = self.buy(exectype=bt.Order.Limit, price=p1, valid=valid1, transmit=False)
                    print('{}: Oref {} / Buy at {}'.format(self.datetime.date(), o1.ref, p1))

                    o2 = self.sell(exectype=bt.Order.Stop, price=p2, valid=valid2, parent=o1, transmit=False)
                    print('{}: Oref {} / Sell Stop at {}'.format(self.datetime.date(), o2.ref, p2))

                    o3 = self.sell(exectype=bt.Order.Limit, price=p3, valid=valid3, parent=o1, transmit=True)
                    print('{}: Oref {} / Sell Limit at {}'.format(self.datetime.date(), o3.ref, p3))

                    self.orefs = [o1.ref, o2.ref, o3.ref]

                else:
                    os = self.buy_bracket(price=p1, valid=valid1, stopprice=p2, stopargs=dict(valid=valid2),
                                          limitprice=p3, limitargs=dict(valid=valid3),)
                    self.orefs = [o.ref for o in os]

        else:  # in the market
            if (len(self) - self.holdstart) >= self.p.hold:
                pass  # do nothing in this case

def runstrat(args=None):
    args = parse_args(args)
    cerebro = bt.Cerebro()

    # Data feed kwargs
    kwargs = dict()
    dtfmt, tmfmt

 = '%Y-%m-%d', 'T%H:%M:%S'
    for a, d in ((getattr(args, x), x) for x in ['fromdate', 'todate']):
        if a:
            strpfmt = dtfmt + tmfmt * ('T' in a)
            kwargs[d] = datetime.datetime.strptime(a, strpfmt)

    data0 = bt.feeds.BacktraderCSVData(dataname=args.data0, **kwargs)
    cerebro.adddata(data0)
    cerebro.broker = bt.brokers.BackBroker(**eval('dict(' + args.broker + ')'))
    cerebro.addsizer(bt.sizers.FixedSize, **eval('dict(' + args.sizer + ')'))
    cerebro.addstrategy(St, **eval('dict(' + args.strat + ')'))
    cerebro.run()

    if args.plot:
        cerebro.plot(**eval('dict(' + args.plot + ')'))

def parse_args(pargs=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Sample Skeleton'
    )

    parser.add_argument('--data0', default='../../datas/2005-2006-day-001.txt',
                        required=False, help='Data to read in')
    parser.add_argument('--fromdate', required=False, default='',
                        help='Date[time] in YYYY-MM-DD[THH:MM:SS] format')
    parser.add_argument('--todate', required=False, default='',
                        help='Date[time] in YYYY-MM-DD[THH:MM:SS] format')
    parser.add_argument('--cerebro', required=False, default='',
                        metavar='kwargs', help='kwargs in key=value format')
    parser.add_argument('--broker', required=False, default='',
                        metavar='kwargs', help='kwargs in key=value format')
    parser.add_argument('--sizer', required=False, default='',
                        metavar='kwargs', help='kwargs in key=value format')
    parser.add_argument('--strat', required=False, default='',
                        metavar='kwargs', help='kwargs in key=value format')
    parser.add_argument('--plot', required=False, default='',
                        nargs='?', const='{}',
                        metavar='kwargs', help='kwargs in key=value format')

    return parser.parse_args(pargs)

if __name__ == '__main__':
    runstrat()
############################################################################################################################
期货和现货补偿#
版本 1.9.32.116 增加了对社区提出的一个有趣用例的支持：

用期货启动交易，包括实物交割；
使用指标进行分析；
如有必要，通过操作现货价格来平仓，从而有效地取消实物交割，无论是收货还是交货（希望能获利）
期货在操作现货价格的当天到期
这意味着：

平台接收来自两个不同资产的数据点
平台必须以某种方式理解这些资产是相关的，并且现货价格的操作将关闭在期货上开启的头寸
实际上，期货并未平仓，只是实物交割被补偿了
利用这种补偿概念，backtrader 增加了一种方式，让用户告知平台一个数据流上的操作将对另一个数据流产生补偿效果。使用模式如下：

import backtrader as bt

cerebro = bt.Cerebro()

data0 = bt.feeds.MyFavouriteDataFeed(dataname='futurename')
cerebro.adddata(data0)

data1 = bt.feeds.MyFavouriteDataFeed(dataname='spotname')
data1.compensate(data0)  # 告诉系统 data1 的操作会影响 data0
cerebro.adddata(data1)

...

cerebro.run()
综合示例#
一个示例胜过千言万语，所以让我们把所有的部分结合起来。

使用 backtrader 源代码中的一个标准示例数据源。这将是期货数据
通过重新使用相同的数据源并添加一个随机移动价格的过滤器来模拟一个类似但不同的价格，从而创建价差。如下简单地实现：
# 更改收盘价的过滤器
def close_changer(data, *args, **kwargs):
    data.close[0] += 50.0 * random.randint(-1, 1)
    return False  # 数据流长度未变
在同一轴上绘图会混淆默认包含的 BuyObserver 标记，因此将禁用标准观察者并手动重新添加以使用不同的数据标记。

头寸将随机进入并在 10 天后退出。

这并不匹配期货到期期限，但这只是为了实现功能，而不是检查交易日历。

注意：

如果要在期货到期日模拟现货价格的执行，需要激活“cheat-on-close”以确保订单在期货到期时执行。这在本示例中不需要，因为到期是随机选择的。
注意策略：

买操作在 data0 上执行
卖操作在 data1 上执行
class St(bt.Strategy):

    def __init__(self):
        bt.obs.BuySell(self.data0, barplot=True)  # 为不同数据添加不同标记
        BuySellArrows(self.data1, barplot=True)  # 为不同数据添加不同标记

    def next(self):
        if not self.position:
            if random.randint(0, 1):
                self.buy(data=self.data0)
                self.entered = len(self)
        else:  # 在市场中
            if (len(self) - self.entered) >= 10:
                self.sell(data=self.data1)
执行：#
$ ./future-spot.py --no-comp
得到如下图形输出。

可以看到：

买操作用向上的绿色三角形标记，图例显示它们属于 data0
卖操作用向下箭头标记，图例显示它们属于 data1
即使在 data0 上打开头寸并在 data1 上平仓，也能实现交易的闭合，达到了避免实物交割的效果。

我们可以想象，如果不进行补偿，同样的逻辑会发生什么。让我们试试：

$ ./future-spot.py --no-comp
这会惨败：

逻辑期望 data0 上的头寸通过 data1 的操作平仓，并且只有在市场不在时才在 data0 上开仓
但是补偿被禁用，data0 上的初始操作（绿色三角形）从未平仓，因此无法发起其他操作，data1 上的空头头寸开始累积。
示例用法：#
$ ./future-spot.py --help
usage: future-spot.py [-h] [--no-comp]

Compensation example

optional arguments:
  -h, --help  show this help message and exit
  --no-comp
示例代码：#
from __future__ import (absolute_import, division, print_function, unicode_literals)

import argparse
import random
import backtrader as bt

# 更改收盘价的过滤器
def close_changer(data, *args, **kwargs):
    data.close[0] += 50.0 * random.randint(-1, 1)
    return False  # 数据流长度未变

# 重写标准标记
class BuySellArrows(bt.observers.BuySell):
    plotlines = dict(buy=dict(marker='$\u21E7$', markersize=12.0),
                     sell=dict(marker='$\u21E9$', markersize=12.0))

class St(bt.Strategy):
    def __init__(self):
        bt.obs.BuySell(self.data0, barplot=True)  # 为不同数据添加不同标记
        BuySellArrows(self.data1, barplot=True)  # 为不同数据添加不同标记

    def next(self):
        if not self.position:
            if random.randint(0, 1):
                self.buy(data=self.data0)
                self.entered = len(self)
        else:  # 在市场中
            if (len(self) - self.entered) >= 10:
                self.sell(data=self.data1)

def runstrat(args=None):
    args = parse_args(args)
    cerebro = bt.Cerebro()

    dataname = '../../datas/2006-day-001.txt'  # 数据源

    data0 = bt.feeds.BacktraderCSVData(dataname=dataname, name='data0')
    cerebro.adddata(data0)

    data1 = bt.feeds.BacktraderCSVData(dataname=dataname, name='data1')
    data1.addfilter(close_changer)
    if not args.no_comp:
        data1.compensate(data0)
    data1.plotinfo.plotmaster = data0
    cerebro.adddata(data1)

    cerebro.addstrategy(St)  # 示例策略

    cerebro.addobserver(bt.obs.Broker)  # 以下两行在 stdstats=False 时被移除
    cerebro.addobserver(bt.obs.Trades)

    cerebro.broker.set_coc(True)
    cerebro.run(stdstats=False)  # 执行
    cerebro.plot(volume=False)  # 绘图

def parse_args(pargs=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=('Compensation example'))

    parser.add_argument('--no-comp', required=False, action='store_true')
    return parser.parse_args(pargs)

if __name__ == '__main__':
    runstrat()
###########################################################################################################################################################
跟踪止损（限价）#
版本 1.9.35.116 增加了跟踪止损和跟踪止损限价订单执行类型到回测工具中。

注意，这只在回测中实现，尚未在实时经纪商中实现

注意，更新至版本 1.9.36.116。Interactive Brokers 支持跟踪止损、跟踪止损限价和 OCO。

OCO 始终将组中的第一个订单指定为参数 oco

跟踪止损限价：经纪商模拟和 IB 经纪商具有相同的行为。指定：price 作为初始止损触发价格（也指定 trailamount），然后 plimit 作为初始限价。两者之间的差值将决定 limitoffset（限价与止损触发价格之间的距离）

使用模式完全集成到策略实例的标准买、卖和平仓市场操作方法中。需要注意：

指明所需的执行类型，如 exectype=bt.Order.StopTrail

以及跟踪价格是否需要用固定距离或百分比距离计算

固定距离：trailamount=10

百分比距离：trailpercent=0.02（即：2%）

如果通过发出买单进入市场多头，那么带有 StopTrail 和 trailamount 的卖单会这样做：

如果未指定价格，则使用最新的收盘价

从价格中减去 trailamount 以找到止损（或触发）价格

经纪商的下一次迭代检查是否触及触发价格

如果是：订单将以市场执行类型的方式执行

如果否，使用最新的收盘价重新计算止损价格，并减去 trailamount 距离

如果新价格上涨，则更新

如果新价格下跌（或不变），则忽略

也就是说：跟踪止损价格随着价格上涨而跟随，但如果价格开始下跌则保持不变，以潜在地确保利润。

如果进入市场时发出的是卖单，那么发出带 StopTrail 的买单会执行相反的操作，即：价格会向下跟随。

一些使用模式

# 对于向下的跟踪止损
# 将使用最后价格作为参考
self.buy(size=1, exectype=bt.Order.StopTrail, trailamount=0.25)
# 或
self.buy(size=1, exectype=bt.Order.StopTrail, price=10.50, trailamount=0.25)

# 对于向上的跟踪止损
# 将使用最后价格作为参考
self.sell(size=1, exectype=bt.Order.StopTrail, trailamount=0.25)
# 或
self.sell(size=1, exectype=bt.Order.StopTrail, price=10.50, trailamount=0.25)
也可以指定 trailpercent 而不是 trailamount，并将距离价格的距离计算为价格的百分比

# 对于 2% 距离的向下跟踪止损
# 将使用最后价格作为参考
self.buy(size=1, exectype=bt.Order.StopTrail, trailpercent=0.02)
# 或
self.buy(size=1, exectype=bt.Order.StopTrail, price=10.50, trailpercent=0.02)

# 对于 2% 距离的向上跟踪止损
# 将使用最后价格作为参考
self.sell(size=1, exectype=bt.Order.StopTrail, trailpercent=0.02)
# 或
self.sell(size=1, exectype=bt.Order.StopTrail, price=10.50, trailpercent=0.02)
对于跟踪止损限价

唯一的区别在于触发跟踪止损价格时发生的事情。

在这种情况下，订单作为限价订单执行（与 StopLimit 订单具有相同的行为，但此时触发价格是动态的）

注意：必须指定 plimit=x.x 来买入或卖出，这将是限价

注意：限价不会像止损/触发价格那样动态变化

示例总是胜过千言万语，因此这里有一个 backtrader 的常规示例，它

使用均线向上交叉进入市场多头
使用跟踪止损退出市场
执行时固定价格距离为 50 点

$ ./trail.py --plot --strat trailamount=50.0
以及以下输出：

**************************************************
2005-02-14,3075.76,3025.76,3025.76
----------
2005-02-15,3086.95,3036.95,3036.95
2005-02-16,3068.55,3036.95,3018.55
2005-02-17,3067.34,3036.95,3017.34
2005-02-18,3072.04,3036.95,3022.04
2005-02-21,3063.64,3036.95,3013.64
...
...
**************************************************
2005-05-19,3051.79,3001.79,3001.79
----------
2005-05-20,3050.45,3001.79,3000.45
2005-05-23,3070.98,3020.98,3020.98
2005-05-24,3066.55,3020.98,3016.55
2005-05-25,3059.84,3020.98,3009.84
2005-05-26,3086.08,3036.08,3036.08
2005-05-27,3084.0,3036.08,3034.0
2005-05-30,3096.54,3046.54,3046.54
2005-05-31,3076.75,3046.54,3026.75
2005-06-01,3125.88,3075.88,3075.88
2005-06-02,3131.03,3081.03,3081.03
2005-06-03,3114.27,3081.03,3064.27
2005-06-06,3099.2,3081.03,3049.2
2005-06-07,3134.82,3084.82,3084.82
2005-06-08,3125.59,3084.82,3075.59
2005-06-09,3122.93,3084.82,3072.93
2005-06-10,3143.85,3093.85,3093.85
2005-06-13,3159.83,3109.83,3109.83
2005-06-14,3162.86,3112.86,3112.86
2005-06-15,3147.55,3112.86,3097.55
2005-06-16,3160.09,3112.86,3110.09
2005-06-17,3178.48,3128.48,3128.48
2005-06-20,3162.14,3128.48,3112.14
2005-06-21,3179.62,3129.62,3129.62
2005-06-22,3182.08,3132.08,3132.08
2005-06-23,3190.8,3140.8,3140.8
2005-06-24,3161.0,3140.8,3111.0
...
...
...
**************************************************
2006-12-19,4100.48,4050.48,4050.48
----------
2006-12-20,4118.54,4068.54,4068.54
2006-12-21,4112.1,4068.54,4062.1
2006-12-22,4073.5,4068.54,4023.5
2006-12-27,4134.86,4084.86,4084.86
2006-12-28,4130.66,4084.86,4080.66
2006-12-29,4119.94,4084.86,4069.94
而不是等待通常的向下交叉模式，系统使用跟踪止损退出市场。让我们看看第一个操作，例如：

进入多头时的收盘价：3075.76
系统计算的跟踪止损价格：3025.76（距离为 50 个单位）
示例计算的跟踪止损价格：3025.76（每行显示的最后一个价格）
在第一次计算之后：

收盘价上涨到 3086.95，止损价格调整为 3036.95
随后的收盘价没有超过 3086.95，触发价格不变
其他两个操作

中可以看到相同的模式。

为了比较，执行时固定距离为 30 点（仅图表）

$ ./trail.py --plot --strat trailamount=30.0
图表如下：

图像

最后一次执行 trailpercent=0.02

$ ./trail.py --plot --strat trailpercent=0.02
示例用法#
$ ./trail.py --help
usage: trail.py [-h] [--data0 DATA0] [--fromdate FROMDATE] [--todate TODATE]
                [--cerebro kwargs] [--broker kwargs] [--sizer kwargs]
                [--strat kwargs] [--plot [kwargs]]

StopTrail Sample

optional arguments:
  -h, --help           show this help message and exit
  --data0 DATA0        Data to read in (default:
                       ../../datas/2005-2006-day-001.txt)
  --fromdate FROMDATE  Date[time] in YYYY-MM-DD[THH:MM:SS] format (default: )
  --todate TODATE      Date[time] in YYYY-MM-DD[THH:MM:SS] format (default: )
  --cerebro kwargs     kwargs in key=value format (default: )
  --broker kwargs      kwargs in key=value format (default: )
  --sizer kwargs       kwargs in key=value format (default: )
  --strat kwargs       kwargs in key=value format (default: )
  --plot [kwargs]      kwargs in key=value format (default: )
示例代码#
from __future__ import (absolute_import, division, print_function, unicode_literals)

import argparse
import datetime
import backtrader as bt

class St(bt.Strategy):
    params = dict(
        ma=bt.ind.SMA,
        p1=10,
        p2=30,
        stoptype=bt.Order.StopTrail,
        trailamount=0.0,
        trailpercent=0.0,
    )

    def __init__(self):
        ma1, ma2 = self.p.ma(period=self.p.p1), self.p.ma(period=self.p.p2)
        self.crup = bt.ind.CrossUp(ma1, ma2)
        self.order = None

    def next(self):
        if not self.position:
            if self.crup:
                o = self.buy()
                self.order = None
                print('*' * 50)

        elif self.order is None:
            self.order = self.sell(exectype=self.p.stoptype,
                                   trailamount=self.p.trailamount,
                                   trailpercent=self.p.trailpercent)

            if self.p.trailamount:
                tcheck = self.data.close - self.p.trailamount
            else:
                tcheck = self.data.close * (1.0 - self.p.trailpercent)
            print(','.join(
                map(str, [self.datetime.date(), self.data.close[0],
                          self.order.created.price, tcheck])
                )
            )
            print('-' * 10)
        else:
            if self.p.trailamount:
                tcheck = self.data.close - self.p.trailamount
            else:
                tcheck = self.data.close * (1.0 - self.p.trailpercent)
            print(','.join(
                map(str, [self.datetime.date(), self.data.close[0],
                          self.order.created.price, tcheck])
                )
            )

def runstrat(args=None):
    args = parse_args(args)

    cerebro = bt.Cerebro()

    # Data feed kwargs
    kwargs = dict()

    # Parse from/to-date
    dtfmt, tmfmt = '%Y-%m-%d', 'T%H:%M:%S'
    for a, d in ((getattr(args, x), x) for x in ['fromdate', 'todate']):
        if a:
            strpfmt = dtfmt + tmfmt * ('T' in a)
            kwargs[d] = datetime.datetime.strptime(a, strpfmt)

    # Data feed
    data0 = bt.feeds.BacktraderCSVData(dataname=args.data0, **kwargs)
    cerebro.adddata(data0)

    # Broker
    cerebro.broker = bt.brokers.BackBroker(**eval('dict(' + args.broker + ')'))

    # Sizer
    cerebro.addsizer(bt.sizers.FixedSize, **eval('dict(' + args.sizer + ')'))

    # Strategy
    cerebro.addstrategy(St, **eval('dict(' + args.strat + ')'))

    # Execute
    cerebro.run(**eval('dict(' + args.cerebro + ')'))

    if args.plot:  # Plot if requested to
        cerebro.plot(**eval('dict(' + args.plot + ')'))

def parse_args(pargs=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=(
            'StopTrail Sample'
        )
    )

    parser.add_argument('--data0', default='../../datas/2005-2006-day-001.txt',
                        required=False, help='Data to read in')

    # Defaults for dates
    parser.add_argument('--fromdate', required=False, default='',
                        help='Date[time] in YYYY-MM-DD[THH:MM:SS] format')

    parser.add_argument('--todate', required=False, default='',
                        help='Date[time] in YYYY-MM-DD[THH:MM:SS] format')

    parser.add_argument('--cerebro', required=False, default='',
                        metavar='kwargs', help='kwargs in key=value format')

    parser.add_argument('--broker', required=False, default='',
                        metavar='kwargs', help='kwargs in key=value format')

    parser.add.argument('--sizer', required=False, default='',
                        metavar='kwargs', help='kwargs in key=value format')

    parser.add.argument('--strat', required=False, default='',
                        metavar='kwargs', help='kwargs in key=value format')

    parser.add.argument('--plot', required=False, default='',
                        nargs='?', const='{}',
                        metavar='kwargs', help='kwargs in key=value format')

    return parser.parse_args(pargs)

if __name__ == '__main__':
    runstrat()
##############################################################################################################################




29 39Broker.txt ##################################################
文件路径: 39Broker.txt
================================================================================

Broker#
类 backtrader.brokers.BackBroker()#
Broker 经纪商模拟器，该模拟支持不同的订单类型，检查提交订单的现金需求与当前现金的对比，跟踪每次 Cerebro 迭代的现金和价值，并保持不同数据的当前头寸。

现金在每次迭代中调整，对于期货等工具来说，当价格变化时，会在实际经纪商中增加或减少现金。 支持的订单类型：

Market：将在下一个柱的第一个tick（即开盘价）执行
Close：用于日内交易，订单以会话最后一个柱的收盘价执行
Limit：如果在会话期间看到给定的限价则执行
Stop：如果看到给定的止损价，则执行市场订单
StopLimit：如果看到给定的止损价，则启动限价订单
因为经纪商由 Cerebro 实例化，用户通常不需要替换经纪商实例，因此参数不受用户控制。

要更改参数，有两种选择：

手动创建带所需参数的 Broker，用 cerebro.broker = instance 将该实例设置为这个经纪商；
使用 set_xxx 方法通过 cerebro.broker.set_xxx 设置参数，其中 xxx 代表设置参数名称；
注意，cerebro.broker 是一个由 Cerebro 的 getbroker 和 setbroker 方法支持的属性。

参数#
参数名	默认值	描述
cash	10000	起始现金
commission	CommInfoBase(percabs=True)	适用于所有资产的基础佣金方案
checksubmit	True	在将订单接受到系统之前检查保证金/现金
eosbar	False	对于日内 Bar，考虑与会话结束时间相同的柱为会话结束。通常不会这样，因为许多交易所会在会话结束后几分钟内为许多产品生成一些柱（最终拍卖）
filler	None	一个可调用对象，签名为 callable(order, price, ago)。

参数说明：
- order：显然是执行中的订单。这提供了对数据的访问（包括 ohlc 和成交量值）、执行类型、剩余大小（order.executed.remsize）等。
- price：订单将在 ago 柱中执行的价格
- ago：用于从 order.data 提取 ohlc 和成交量价格的索引。在大多数情况下，这将是 0，但在某些角落情况下，对于 Close 订单，这将是 -1。
- 可调用对象必须返回执行的大小（值 >= 0）
可调用对象当然可以是一个 __call__ 符合上述签名的对象。默认情况下，订单将一次性完全执行。
slip_perc	0.0	用于买卖订单上下滑动价格的绝对百分比（且为正值）。
注意：0.01 是 1%，0.001 是 0.1%
slip_fixed	0.0	用于买卖订单上下滑动价格的单位百分比（且为正值）。
注意：如果 slip_perc 非零，则优先于此。
slip_open	False	是否滑动专门使用下一个柱的开盘价执行的订单价格。例如，市场订单将在下一个可用tick执行，即柱的开盘价。这也适用于其他一些执行，因为逻辑尝试检测开盘价是否会匹配请求的价格/执行类型在移动到新柱时。
slip_match	True	- 如果为 True，经纪商将通过在高/低价位封顶滑点来提供匹配，以防它们超出。

- 如果为 False，经纪商将不会使用当前价格匹配订单，并将在下一次迭代中尝试执行
slip_limit	True	- 限价订单，给定确切的匹配价格请求，即使 slip_match 为 False，也会被匹配。
- 此选项控制该行为。
- 如果为 True，那么限价订单将通过在限价/高低价位封顶价格进行匹配
- 如果为 False 且滑点超出上限，则不会有匹配
slip_out	False	即使价格超出高-低范围，也提供滑点。
coc	False	Cheat-On-Close 将其设置为 True 与 set_coc 启用，将“市场”订单与订单条的收盘价匹配。这实际上是作弊，因为柱已关闭，任何订单都应首先与下一个柱的价格匹配
coo	False	Cheat-On-Open 将其设置为 True 与 set_coo 启用，将“市场”订单与开盘价匹配，例如使用设置为 True 的计时器，因为这种计时器在经纪商评估之前执行
int2pnl	True	将生成的利息（如果有）分配给减少头寸的操作的利润和亏损（无论是多头还是空头）。在某些情况下，这可能是不希望的，因为不同的策略在竞争，利息将以不确定的方式分配给其中任何一个。
shortcash	True	如果为 True，则在卖空类似股票的资产时将增加现金，并且该资产的计算价值将为负值。
- 如果为 False，则现金将作为操作成本扣除，计算的价值将为正值，以最终得到相同的金额
fundstartval	100.0	此参数控制基金式绩效测量的起始值，即：现金可以增加和扣除，增加股票数量。绩效不是使用投资组合的净资产价值来衡量，而是使用基金的价值
fundmode	False	如果设置为 True，诸如 TimeReturn 的分析器可以基于基金价值而不是总净资产价值自动计算回报
方法#
签名	描述
set_cash(cash)	设置现金参数（别名：setcash）
get_cash()	返回当前现金（别名：getcash）
get_value(
 datas=None,
 mkt=False,
 lever=False
)	返回给定数据的投资组合价值（如果数据为 None，则返回总投资组合价值）（别名：getvalue）
set_eosbar(eosbar)	设置 eosbar 参数（别名：seteosbar）
set_checksubmit(checksubmit)	设置 checksubmit 参数
set_filler(filler)	设置用于成交量填充执行的填充器
set_coc(coc)	配置 Cheat-On-Close 方法以在订单柱上买入收盘价
set_coo(coo)	配置 Cheat-On-Open 方法以在订单柱上买入收盘价
set_int2pnl(int2pnl)	配置将利息分配给利润和亏损
set_fundstartval(fundstartval)	设置基金式绩效跟踪器的起始值
set_slippage_perc(
 perc,
 slip_open=True,
 slip_limit=True,
 slip_match=True,
&emspslip_out=False
)	配置滑点为基于百分比
set_slippage_fixed(
 fixed,
 slip_open=True,
 slip_limit=True,
 slip_match=True,
 slip_out=False
)	配置滑点为固定点数
get_orders_open(safe=False)	返回仍然打开的订单（未执行或部分执行）的可迭代对象。返回的订单不得被触摸。如果需要订单操作，请将参数 safe 设置为 True
getcommissioninfo(data)	检索与给定数据相关的 CommissionInfo 方案
setcommission(
 commission=0.0,
 margin=None,
 mult=1.0,
 commtype=None,
 percabs=True,
 stocklike=False,
 interest=0.0,
 interest_long=False,
 leverage=1.0,
 automargin=False,
 name=None
)	为 Broker 设置 CommissionInfo 对象，参考 CommInfoBase 文档介绍。

如果 name 为 None，这将是没有找到其他 CommissionInfo 方案的资产的默认设置
addcommissioninfo(
 comminfo, name=None
)	添加 CommissionInfo 对象，如果 name 为 None，将成为所有资产的默认设置
getposition(data)	返回给定数据的当前头寸状态（一个 Position 实例）
get_fundshares()	返回基金模式中的当前股票数量
get_fundvalue()	返回基金式的股票价值
add_cash(cash)	添加/移除系统现金（使用负值移除）
########################################################################################################################
滑点#
回测无法保证真实市场条件。无论市场模拟有多好，在真实市场条件下滑点可能发生。这意味着，请求的价格可能无法匹配。

集成的回测经纪商支持滑点，以下参数可以传递给经纪商：

参数名	默认值	描述
slip_perc	0.0	应用于买卖订单的价格上下滑动的绝对百分比（且为正值），注意：0.01 是 1%，0.001 是 0.1%；
slip_fixed	0.0	应用于买卖订单的价格上下滑动的单位百分比（且为正值），注意：如果 slip_perc 非零，则优先于此。
slip_open	False	是否为专门使用下一个柱的开盘价执行的订单滑动价格。例如，市场订单将在下一个可用tick执行，即柱的开盘价。这也适用于其他一些执行，因为逻辑尝试检测开盘价是否会匹配请求的价格/执行类型在移动到新柱时。
slip_match	True	- 如果为 True，经纪商将通过在高/低价位封顶滑点来提供匹配，以防它们超出。
- 如果为 False，经纪商将不会使用当前价格匹配订单，并将在下一次迭代中尝试执行
slip_limit	True	- 限价订单，给定确切的匹配价格请求，即使 slip_match 为 False，也会被匹配。
- 此选项控制该行为。
- 如果为 True，那么限价订单将通过在限价/高低价位封顶价格进行匹配。
- 如果为 False 且滑点超出上限，则不会有匹配
slip_out	False	即使价格超出高-低范围，也提供滑点。
工作原理#
为了决定何时应用滑点，考虑了订单执行类型：

Close - 不应用滑点

这种订单匹配收盘价，而这个价格是当天的最后一个。滑点无法发生，因为订单只能在会话的最后一个tick发生，而这是唯一的价格，没有容忍度。
Market - 应用滑点

请检查 slip_open 例外情况。因为市场订单将匹配下一个柱的开盘价。
Limit - 按以下逻辑应用滑点

如果匹配价格是开盘价，则根据参数 slip_open 应用滑点。如果应用，价格不会比请求的限价更差。
如果匹配价格不是限价，则应用滑点在高/低点封顶。在这种情况下，slip_limit 应用以决定在超过封顶时是否会发生匹配。
如果匹配价格是限价，则不应用滑点。
Stop - 一旦订单触发，应用与市场订单相同的逻辑

StopLimit - 一旦订单触发，应用与限价订单相同的逻辑

这种方法试图在模拟和可用数据的限制范围内提供最现实的方法。

配置滑点#
每次运行时，Cerebro 引擎已实例化一个经纪商，使用默认参数。有两种方法配置滑点。

配置滑点为基于百分比的方法

BackBroker.set_slippage_perc(
  perc, 
  slip_open=True,
  slip_limit=True,
  slip_match=True,
  slip_out=False,
)
配置滑点为固定点数的方法：

BackBroker.set_slippage_fixed(
  fixed,
  slip_open=True,
  slip_limit=True,
  slip_match=True,
  slip_out=False,
)
替换经纪商，例如：

import backtrader as bt

cerebro = bt.Cerebro()
cerebro.broker = bt.brokers.BackBroker(slip_perc=0.005)  # 0.5%
实际示例#
源码包含一个使用订单执行类型 Market 和使用信号的多/空方法的示例。这应该可以理解逻辑。

没有滑点的运行和初始图表供以后参考：

$ ./slippage.py --plot
01 2005-03-22 23:59:59 SELL Size: -1 / Price: 3040.55
02 2005-04-11 23:59:59 BUY  Size: +1 / Price: 3088.47
03 2005-04-11 23:59:59 BUY  Size: +1 / Price: 3088.47
04 2005-04-19 23:59:59 SELL Size: -1 / Price: 2948.38
05 2005-04-19 23:59:59 SELL Size: -1 / Price: 2948.38
06 2005-05-19 23:59:59 BUY  Size: +1 / Price: 3034.88
...
35 2006-12-19 23:59:59 BUY  Size: +1 / Price: 4121.01
image

使用配置为 1.5% 滑点的相同运行：

$ ./slippage.py --slip_perc 0.015
01 2005-03-22 23:59:59 SELL Size: -1 / Price: 3040.55
02 2005-04-11 23:59:59 BUY  Size: +1 / Price: 3088.47
03 2005-04-11 23:59:59 BUY  Size: +1 / Price: 3088.47
04 2005-04-19 23:59:59 SELL Size: -1 / Price: 2948.38
05 2005-04-19 23:59:59 SELL Size: -1 / Price: 2948.38
06 2005-05-19 23:59:59 BUY  Size: +1 / Price: 3034.88
...
35 2006-12-19 23:59:59 BUY  Size: +1 / Price: 4121.01
没有变化。这是预期的行为。

执行类型：Market

且未设置 slip_open 为 True

市场订单匹配下一个柱的开盘价，我们不允许开盘价移动。

设置 slip_open 为 True 的运行：

$ ./slippage.py --slip_perc 0.015 --slip_open
01 2005-03-22 23:59:59 SELL Size: -1 / Price: 3021.66
02 2005-04-11 23:59:59 BUY  Size: +1 / Price: 3088.47
03 2005-04-11 23:59:59 BUY  Size: +1 / Price: 3088.47
04 2005-04-19 23:59:59 SELL Size: -1 / Price: 2948.38
05 2005-04-19 23:59:59 SELL Size: -1 / Price: 2948.38
06 2005-05-19 23:59:59 BUY  Size: +1 / Price: 3055.14
...
35 2006-12-19 23:59:59 BUY  Size: +1 / Price: 4121.01
可以立即看到价格已经移动。分配的价格更差或相同，例如操作 35。打开和高点在 2016-12-19 是相同的。价格不能高于高点，因为这将返回不存在的价格。

当然，如果需要，Backtrader 允许在高-低范围之外匹配。启用 slip_out 的运行：

$ ./slippage.py --slip_perc 0.015 --slip_open --slip_out
01 2005-03-22 23:59:59 SELL Size: -1 / Price: 2994.94
02 2005-04-11 23:59:59 BUY  Size: +1 / Price: 3134.80
03 2005-04-11 23:59:59 BUY  Size: +1 / Price: 3134.80
04 2005-04-19 23:59:59 SELL Size: -1 / Price: 2904.15
05 2005-04-19 23:59:59 SELL Size: -1 / Price: 2904.15
06 2005-05-19 23:59:59 BUY  Size: +1 / Price: 3080.40
...
35 2006-12-19 23:59:59 BUY  Size: +1 / Price: 4182.83
匹配价格的表达式将是：OMG！（我的天！）。价格明显超出范围。足以看操作 35，匹配在 4182.83

。快速检查图表显示，资产从未接近过该价格。

slip_match 默认值为 True，这意味着 Backtrader 提供匹配，无论价格是封顶还是未封顶。禁用它：

$ ./slippage.py --slip_perc 0.015 --slip_open --no-slip_match
01 2005-04-15 23:59:59 SELL Size: -1 / Price: 3028.10
02 2005-05-18 23:59:59 BUY  Size: +1 / Price: 3029.40
03 2005-06-01 23:59:59 BUY  Size: +1 / Price: 3124.03
04 2005-10-06 23:59:59 SELL Size: -1 / Price: 3365.57
05 2005-10-06 23:59:59 SELL Size: -1 / Price: 3365.57
06 2005-12-01 23:59:59 BUY  Size: +1 / Price: 3499.95
07 2005-12-01 23:59:59 BUY  Size: +1 / Price: 3499.95
08 2006-02-28 23:59:59 SELL Size: -1 / Price: 3782.71
09 2006-02-28 23:59:59 SELL Size: -1 / Price: 3782.71
10 2006-05-23 23:59:59 BUY  Size: +1 / Price: 3594.68
11 2006-05-23 23:59:59 BUY  Size: +1 / Price: 3594.68
12 2006-11-27 23:59:59 SELL Size: -1 / Price: 3984.37
13 2006-11-27 23:59:59 SELL Size: -1 / Price: 3984.37
下滑至 13 从 35。原理：

禁用 slip_match 不允许在滑点会推高于高点或低于低点时匹配操作。似乎1.5%的请求滑点，有约22个操作无法执行。

这些例子应该显示了不同滑点选项如何协同工作。
###############################################################################################################
Cheat On Open（开盘作弊）#
版本 1.9.44.116 添加了 Cheat-On-Open 支持。这似乎是对那些在计算完一个柱的收盘价后全仓操作的人们的需求，他们期望与开盘价匹配。

当开盘价跳空（向上或向下，取决于买入或卖出）且现金不足以进行全仓操作时，这种情况会失败。这迫使经纪商拒绝操作。

虽然人们可以尝试通过正 [1] 索引法查看未来，但这需要预加载数据，而这并不总是可行的。

模式#
cerebro = bt.Cerebro(cheat_on_open=True)
这会在系统中激活一个额外的循环，该循环调用策略中的 next_open、nextstart_open 和 prenext_open 方法。

为了清楚地分离常规方法（这些方法基于所检查的价格不再可用且未来未知）和作弊模式下的操作，决定增加一组额外的方法家族。

这也避免了对常规 next 方法的两次调用。

以下情况在 xxx_open 方法内部保持不变：

指标尚未重新计算，保持上一个循环中在等效的 xxx 常规方法中最后看到的值。
经纪商尚未评估新循环中的待处理订单，并且可以引入新订单，如果可能，将进行评估。
注意：

Cerebro 还有一个名为 broker_coo（默认值：True）参数，它告诉 cerebro 如果激活了 cheat-on-open，它也会尝试在经纪商中激活它（如果可能的话）。
模拟经纪商有一个名为 coo 的参数和一个名为 set_coo 的方法来设置它。
尝试 Cheat-on-open#
下面的示例有一个策略，具有两种不同的行为：

如果 cheat-on-open 为 True，它将仅从 next_open 操作。
如果 cheat-on-open 为 False，它将仅从 next 操作。
在这两种情况下，匹配价格必须相同：

如果不作弊，订单在前一天的收盘后发出，并将与下一个到来的价格（开盘价）匹配。
如果作弊，订单在同一天发出并执行。因为订单是在经纪商评估订单之前发出的，所以它也将与下一个到来的价格（开盘价）匹配。
第二种情况下，可以精确计算全仓策略的份额，因为可以直接访问当前的开盘价。

在这两种情况下，当前的开盘价和收盘价将从 next 中打印。

常规执行：#
$ ./cheat-on-open.py --cerebro cheat_on_open=False

...
2005-04-07 next, open 3073.4 close 3090.72
2005-04-08 next, open 3092.07 close 3088.92
Strat Len 68 2005-04-08 Send Buy, fromopen False, close 3088.92
2005-04-11 Buy Executed at price 3088.47
2005-04-11 next, open 3088.47 close 3080.6
2005-04-12 next, open 3080.42 close 3065.18
...
订单：

在 2005-04-08 收盘后发出。
在 2005-04-11 以开盘价 3088.47 执行。
作弊执行：#
$ ./cheat-on-open.py --cerebro cheat_on_open=True

...
2005-04-07 next, open 3073.4 close 3090.72
2005-04-08 next, open 3092.07 close 3088.92
2005-04-11 Send Buy, fromopen True, close 3080.6
2005-04-11 Buy Executed at price 3088.47
2005-04-11 next, open 3088.47 close 3080.6
2005-04-12 next, open 3080.42 close 3065.18
...
订单：

在 2005-04-11 开盘前发出。
在 2005-04-11 以开盘价 3088.47 执行。
总结#
开盘作弊允许在开盘前发出订单，这可以例如允许精确计算全仓场景的份额。

示例用法#
$ ./cheat-on-open.py --help
usage: cheat-on-open.py [-h] [--data0 DATA0] [--fromdate FROMDATE]
                        [--todate TODATE] [--cerebro kwargs] [--broker kwargs]
                        [--sizer kwargs] [--strat kwargs] [--plot [kwargs]]

Cheat-On-Open Sample

optional arguments:
  -h, --help           show this help message and exit
  --data0 DATA0        Data to read in (default:
                       ../../datas/2005-2006-day-001.txt)
  --fromdate FROMDATE  Date[time] in YYYY-MM-DD[THH:MM:SS] format (default: )
  --todate TODATE      Date[time] in YYYY-MM-DD[THH:MM:SS] format (default: )
  --cerebro kwargs     kwargs in key=value format (default: )
  --broker kwargs      kwargs in key=value format (default: )
  --sizer kwargs       kwargs in key=value format (default: )
  --strat kwargs       kwargs in key=value format (default: )
  --plot [kwargs]      kwargs in key=value format (default: )
示例代码#
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse
import datetime

import backtrader as bt


class St(bt.Strategy):
    params = dict(
        periods=[10, 30],
        matype=bt.ind.SMA,
    )

    def __init__(self):
        self.cheating = self.cerebro.p.cheat_on_open
        mas = [self.p.matype(period=x) for x in self.p.periods]
        self.signal = bt.ind.CrossOver(*mas)
        self.order = None

    def notify_order(self, order):
        if order.status != order.Completed:
            return

        self.order = None
        print('{} {} Executed at price {}'.format(
            bt.num2date(order.executed.dt).date(),
            'Buy' * order.isbuy() or 'Sell', order.executed.price)
        )

    def operate(self, fromopen):
        if self.order is not None:
            return
        if self.position:
            if self.signal < 0:
                self.order = self.close()
        elif self.signal > 0:
            print('{} Send Buy, fromopen {}, close {}'.format(
                self.data.datetime.date(),
                fromopen, self.data.close[0])
            )
            self.order = self.buy()

    def next(self):
        print('{} next, open {} close {}'.format(
            self.data.datetime.date(),
            self.data.open[0], self.data.close[0])
        )

        if self.cheating:
            return
        self.operate(fromopen=False)

    def next_open(self):
        if not self.cheating:
            return
        self.operate(fromopen=True)


def runstrat(args=None):
    args = parse_args(args)

    cerebro = bt.Cerebro()

    # Data feed kwargs
    kwargs = dict()

    # Parse from/to-date
    dtfmt, tmfmt = '%Y-%m-%d', 'T%H:%M:%S'
    for a, d in ((getattr(args, x), x) for x in ['fromdate', 'todate']):
        if a:
            strpfmt = dtfmt + tmfmt * ('T' in a)
            kwargs[d] = datetime.datetime.strptime(a, strpfmt)

    # Data feed
    data0 = bt.feeds.BacktraderCSVData(dataname=args.data0, **kwargs)
    cerebro.adddata(data0)

    # Broker
    cerebro.broker = bt.brokers.BackBroker(**eval('dict(' + args.broker + ')'))

    # Sizer
    cerebro.addsizer(bt.sizers.FixedSize, **eval('dict(' + args.sizer + ')'))

    # Strategy
    cerebro.addstrategy(St, **eval('dict(' + args.strat + ')'))

    # Execute
    cerebro.run(**eval('dict(' + args.cerebro + ')'))

    if args.plot:  # Plot if requested to
        cerebro.plot(**eval('dict(' + args.plot + ')'))


def parse_args(pargs=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=(
            'Cheat-On-Open Sample'
        )
    )

    parser.add_argument('--data0', default='../../datas/2005-2006-day-001.txt',
                        required=False, help='Data to read in')

    # Defaults for dates
    parser.add_argument('--fromdate', required=False, default='',
                        help='Date[time] in YYYY-MM-DD[THH:MM:SS] format')

    parser.add_argument('--todate', required=False

, default='',
                        help='Date[time] in YYYY-MM-DD[THH:MM:SS] format')

    parser.add_argument('--cerebro', required=False, default='',
                        metavar='kwargs', help='kwargs in key=value format')

    parser.add_argument('--broker', required=False, default='',
                        metavar='kwargs', help='kwargs in key=value format')

    parser.add_argument('--sizer', required=False, default='',
                        metavar='kwargs', help='kwargs in key=value format')

    parser.add_argument('--strat', required=False, default='',
                        metavar='kwargs', help='kwargs in key=value format')

    parser.add_argument('--plot', required=False, default='',
                        nargs='?', const='{}',
                        metavar='kwargs', help='kwargs in key=value format')

    return parser.parse_args(pargs)


if __name__ == '__main__':
    runstrat()
#######################################################################################################################
填充器#
Backtrader 的经纪模拟在订单执行时有一个默认策略：忽略交易量。这是基于两个前提：

交易在流动性足够高的市场中，可以一次性完全吸收买/卖订单
实际的交易量匹配需要真实的市场环境
一个简单的例子是“立即成交或取消”（Fill or Kill）订单。即使细化到每一笔交易，并且有足够的交易量来完成订单，Backtrader的经纪模拟也无法知道市场中有多少其他参与者来判断这样的订单是否会被匹配以遵循“立即成交”部分，或者订单是否应该被取消。

但是经纪模拟可以接受交易量填充器（Volume Fillers），它们决定在给定时间点应该使用多少交易量来匹配订单。

填充器签名#
在Backtrader生态系统中，填充器可以是任何符合以下签名的可调用对象：

callable(order, price, ago)
其中：

order 是即将执行的订单，该对象提供对目标数据对象的访问，创建的大小/价格、执行的价格/大小/剩余大小和其他详细信息
price 是订单执行的价格
ago 是数据在订单中的索引，用于查找交易量和价格元素
在几乎所有情况下，这将是0（当前时间点），但在某些特殊情况下（例如Close订单），这可能是-1。

例如，访问bar交易量可以这样做：

barvolume = order.data.volume[ago]
可调用对象可以是一个函数，或例如支持__call__方法的类的实例，例如：

class MyFiller(object):
    def __call__(self, order, price, ago):
        pass
将填充器添加到经纪模拟

最直接的方法是使用set_filler：

import backtrader as bt

cerebro = Cerebro()
cerebro.broker.set_filler(bt.broker.fillers.FixedSize())
第二种选择是完全替换经纪模拟，这可能仅适用于重写了部分功能的BrokerBack子类：

import backtrader as bt

cerebro = Cerebro()
filler = bt.broker.fillers.FixedSize()
newbroker = bt.broker.BrokerBack(filler=filler)
cerebro.broker = newbroker
示例#
Backtrader的源代码中包含一个名为volumefilling的示例，它允许测试一些集成的填充器（最初是全部）。

参考#
class backtrader.fillers.FixedSize()
使用条形图中某个百分比的交易量返回给定订单的执行大小。

该百分比通过参数perc设置。

参数：

size（默认：None）最大执行大小。如果执行时间的条形图实际交易量小于该大小，则条形图的实际交易量也是一个限制。

如果该参数的值评估为False，则将使用条形图的全部交易量来匹配订单。

class backtrader.fillers.FixedBarPerc()
使用条形图中某个百分比的交易量返回给定订单的执行大小。

该百分比通过参数perc设置。

参数：

perc（默认：100.0）（有效值：0.0 - 100.0）

用于执行订单的条形图交易量百分比

class backtrader.fillers.BarPointPerc()
返回给定订单的执行大小。交易量将在高-低范围内均匀分布，使用minmov进行分区。

对于给定价格分配的交易量，将使用perc百分比。

参数：

minmov（默认：0.01）

最小价格变动。用于分区高-低范围，以按比例分配可能价格之间的交易量

perc（默认：100.0）（有效值：0.0 - 100.0）

用于订单执行价格匹配的分配交易量百分比
#######################################################################################
Position#
通常在策略中要检查资产 Position，或成为仓位、头寸，通过 position 属性或 getposition(data=None, broker=None) 方法。这将返回策略在cerebro提供的默认经纪商中的datas[0]的头寸。

头寸只是一个表示：

持有的资产数量（size）
平均价格（price）
它用作状态指示，例如可以用于决定是否需要发出订单（例如：仅在没有持仓时进入多头头寸）。

参考#
class backtrader.position.Position(size=0, price=0.0)
保存并更新头寸的数量和价格。该对象与任何资产没有关系。它只保存数量和价格。

成员属性：

size（int）：当前头寸的数量
price（float）：当前头寸的价格
可以使用 len(position) 来测试头寸实例以查看数量是否不为零。
############################################################…###########################################################
Trade#
交易的定义：当一个工具的头寸从 0 变为一个大小X（多头/空头头寸分别为正/负）时，交易被认为是开启的。或是当一个头寸从X变为0时，交易被认为是关闭的。

以下两种操作：

从正变负
从负变正
实际上被视为：一个交易被关闭了（头寸从X变为0），一个新的交易被开启了（头寸从0变为Y）

交易仅用于信息展示，用户无法调用其方法。

参考#
class backtrader.trade.Trade(data=None, tradeid=0, historyon=False, size=0, price=0.0, value=0.0, commission=0.0)
追踪交易的生命周期：数量、价格、佣金（和价值？）。一个交易从0开始，可以增加和减少，如果回到0可以被认为是关闭的。交易可以是多头（正数）或空头（负数）。交易不支持反转（逻辑中不支持）

成员属性	描述
ref	唯一的交易标识符
status	Created, Open, Closed之一
tradeid	在创建订单时传递给订单的分组交易ID，订单的默认值为0
size	当前交易的数量
price	当前交易的价格
value	当前交易的价值
commission	当前累计的佣金
pnl	当前交易的盈亏（毛利）
pnlcomm	当前交易的净盈亏（扣除佣金后的净利润）
isclosed	记录最后一次更新是否关闭了交易（将交易数量设为零）
isopen	记录任何更新是否开启了交易
justopened	如果交易刚刚开启
baropen	交易开启的bar
dtopen	交易开启的浮点编码日期时间，使用 open_datetime 方法获取 Python datetime.datetime 或使用平台提供的 num2date 方法
barclose	交易关闭的bar
dtclose	交易关闭的浮点编码日期时间，使用 close_datetime 方法获取 Python datetime.datetime 或使用平台提供的 num2date 方法
barlen	交易开启的bar数量
historyon	是否记录历史
history	包含每次“更新”事件更新后的状态和使用的参数的列表，历史记录的第一个条目是开启事件，最后一个条目是关闭事件


30 40佣金.txt ##################################################
文件路径: 40佣金.txt
================================================================================

佣金#
中立性#
在开始之前，让我们记住 backtrader 尝试保持数据代表内容的中立性。不同的佣金方案可以应用于相同的数据集。让我们看看如何做到这一点。

经纪商快捷方式#
这使得最终用户远离 CommissionInfo 对象，因为可以通过一次函数调用创建/设置佣金方案。在常规的 cerebro 创建/设置过程中，只需在经纪商成员属性上添加一个调用 setcommission 的调用即可。

以下调用设置了使用 Interactive Brokers 操作 Eurostoxx50 期货的常规佣金方案：

cerebro.broker.setcommission(commission=2.0, margin=2000.0, mult=10.0)
由于大多数用户通常只测试单一工具，这已经足够。

如果你为你的数据馈送命名，因为在图表上同时考虑了多个工具，这个调用可以稍微扩展如下：

cerebro.broker.setcommission(commission=2.0, margin=2000.0, mult=10.0, name='Eurostoxxx50')
在这种情况下，此即时佣金方案将仅应用于名称匹配 Eurostoxx50 的工具。

setcommission 参数的含义#
commission（默认值：0.0）

每次操作的货币单位，绝对值或百分比。在上述示例中，每份合约的买入和卖出费用分别为 2.0 欧元。 重要的是何时使用绝对值或百分比值。

如果 margin 为 False（例如，它是 False、0 或 None），则将视为佣金表示为价格乘以操作数量的百分比。

如果 margin 是其他值，则视为操作发生在类似期货的工具上，佣金是每张合约的固定价格。

margin（默认值：None）

操作期货类工具时需要的保证金。如上所述：

如果没有设置 margin，则佣金将被视为百分比，并应用于买卖操作的价格 * 数量。

如果设置了 margin，则佣金将被视为固定值，并乘以买卖操作的数量。

mult（默认值：1.0）

对于期货类工具，这决定了应用于损益计算的乘数。这使得期货同时具有吸引力和风险。

name（默认值：None）

将佣金方案应用于名称匹配的工具。可以在创建数据馈送时设置此值。如果未设置，则方案将适用于系统中的任何数据。

两个示例：股票 vs 期货#
期货的示例：

cerebro.broker.setcommission(commission=2.0, margin=2000.0, mult=10.0)
股票的示例：

cerebro.broker.setcommission(commission=0.005)  # 交易金额的 0.5%
注意

第二种语法不设置 margin 和 mult，backtrader 试图通过将佣金视为百分比来进行智能处理。

要完全指定佣金方案，需要创建 CommissionInfo 的子类。

创建永久性佣金方案#
可以通过直接使用 CommissionInfo 类创建更永久的佣金方案。用户可以选择在某处定义：

import backtrader as bt

commEurostoxx50 = bt.CommissionInfo(commission=2.0, margin=2000.0, mult=10.0)
然后在另一个 Python 模块中应用：

from mycomm import commEurostoxx50

...

cerebro.broker.addcommissioninfo(commEuroStoxx50, name='Eurostoxxx50')
CommissionInfo 是一个对象，使用与 backtrader 环境中的其他对象类似的 params 声明。因此上述内容也可以表示为：

import backtrader as bt

class CommEurostoxx50(bt.CommissionInfo):
    params = dict(commission=2.0, margin=2000.0, mult=10.0)
然后：

from mycomm import CommEurostoxx50

...

cerebro.broker.addcommissioninfo(CommEuroStoxx50(), name='Eurostoxxx50')
使用 SMA 交叉的实际比较#
使用简单移动平均交叉作为进出信号，使用相同的数据集来测试期货类佣金方案和股票类佣金方案。

注意

期货头寸不仅可以给出进出行为，还可以在每次机会时进行反转行为。但这个示例是关于比较佣金方案的。

代码（见底部完整策略）相同，可以在定义策略之前选择方案。

futures_like = True

if futures_like:
    commission, margin, mult = 2.0, 2000.0, 10.0
else:
    commission, margin, mult = 0.005, None, 1
只需将 futures_like 设置为 false 即可使用股票类方案运行。

一些日志代码已被添加以评估不同佣金方案的影响。让我们集中在前两个操作。

对于期货：

2006-03-09, BUY CREATE, 3757.59
2006-03-10, BUY EXECUTED, Price: 3754.13, Cost: 2000.00, Comm 2.00
2006-04-11, SELL CREATE, 3788.81
2006-04-12, SELL EXECUTED, Price: 3786.93, Cost: 2000.00, Comm 2.00
2006-04-12, OPERATION PROFIT, GROSS 328.00, NET 324.00
2006-04-20, BUY CREATE, 3860.00
2006-04-21, BUY EXECUTED, Price: 3863.57, Cost: 2000.00, Comm 2.00
2006-04-28, SELL CREATE, 3839.90
2006-05-02, SELL EXECUTED, Price: 3839.24, Cost: 2000.00, Comm 2.00
2006-05-02, OPERATION PROFIT, GROSS -243.30, NET -247.30
对于股票：

2006-03-09, BUY CREATE, 3757.59
2006-03-10, BUY EXECUTED, Price: 3754.13, Cost: 3754.13, Comm 18.77
2006-04-11, SELL CREATE, 3788.81
2006-04-12, SELL EXECUTED, Price: 3786.93, Cost: 3786.93, Comm 18.93
2006-04-12, OPERATION PROFIT, GROSS 32.80, NET -4.91
2006-04-20, BUY CREATE, 3860.00
2006-04-21, BUY EXECUTED, Price: 3863.57, Cost: 3863.57, Comm 19.32
2006-04-28, SELL CREATE, 3839.90
2006-05-02, SELL EXECUTED, Price: 3839.24, Cost: 3839.24, Comm 19.20
2006-05-02, OPERATION PROFIT, GROSS -24.33, NET -62.84
第一个操作的价格如下：

买入（执行）：3754.13
卖出（执行）：3786.93
期货的损益（含佣金）：324.0

股票的损益（含佣金）：-4.91

佣金完全吞噬了股票操作的利润，而期货操作的利润只受到轻微影响。

第二个操作：

买入（执行）：3863.57
卖出（执行）：3389.24
期货的损益（含佣金）：-247.30

股票的损益（含佣金）：-62.84

对于此负操作，期货的影响明显更大。

但：

期货累计净利润和损失：324.00 + (-247.30) = 76.70

股票累计净利润和损失：(-4.91) + (-62.84) = -67.75

在下图中可以看到累计效果，还可以看到在全年结束时，期货产生了更大的利润，但也遭受了更大的回撤（更深的水下）

但重要的是：无论是期货还是股票……都可以进行回测。

代码#
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicators as btind

futures_like = True

if futures_like:
    commission, margin, mult = 2.0, 2000.0, 10.0
else:
    commission, margin, mult = 0.

005, None, 1


class SMACrossOver(bt.Strategy):
    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed, order.Canceled, order.Margin]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
                self.opsize = order.executed.size
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

                gross_pnl = (order.executed.price - self.buyprice) * \
                    self.opsize

                if margin:
                    gross_pnl *= mult

                net_pnl = gross_pnl - self.buycomm - order.executed.comm
                self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                         (gross_pnl, net_pnl))

    def __init__(self):
        sma = btind.SMA(self.data)
        # > 0 crossing up / < 0 crossing down
        self.buysell_sig = btind.CrossOver(self.data, sma)

    def next(self):
        if self.buysell_sig > 0:
            self.log('BUY CREATE, %.2f' % self.data.close[0])
            self.buy()  # keep order ref to avoid 2nd orders

        elif self.position and self.buysell_sig < 0:
            self.log('SELL CREATE, %.2f' % self.data.close[0])
            self.sell()


if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(SMACrossOver)

    # Create a Data Feed
    datapath = ('../../datas/2006-day-001.txt')
    data = bt.feeds.BacktraderCSVData(dataname=datapath)

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # set commission scheme -- CHANGE HERE TO PLAY
    cerebro.broker.setcommission(
        commission=commission, margin=margin, mult=mult)

    # Run over everything
    cerebro.run()

    # Plot the result
    cerebro.plot()
参考#
class backtrader.CommInfoBase()
基础类用于佣金方案。

参数：

commission（默认值：0.0）：基础佣金值，百分比或货币单位
mult（默认值：1.0）：应用于资产价值/利润的乘数
margin（默认值：None）：开/持仓所需的货币单位，仅当类中的 _stocklike 属性设置为 False 时适用
automargin（默认值：False）：用于方法 get_margin，自动计算所需的保证金/保证金
commtype（默认值：None）：支持的值为 CommInfoBase.COMM_PERC（佣金理解为 %）和 CommInfoBase.COMM_FIXED（佣金理解为货币单位）
默认值 None 是一个支持的值，用于保留与旧的 CommissionInfo 对象的兼容性。如果 commtype 设置为 None，则以下适用：

margin 为 None：内部 _commtype 设置为 COMM_PERC，_stocklike 设置为 True（按百分比操作股票）

margin 不是 None：_commtype 设置为 COMM_FIXED，_stocklike 设置为 False（按固定回合佣金操作期货）

如果此参数设置为其他值，则将传递给内部 _commtype 属性，并且相同将适用于参数 stocklike 和内部属性 _stocklike

stocklike（默认值：False）： 指示工具是类似股票还是类似期货（请参阅上述 commtype 讨论）

percabs（默认值：False）： 当 commtype 设置为 COMM_PERC 时，参数 commission 是否理解为 XX% 或 0.XX

如果此参数为 True：0.XX

如果此参数为 False：XX%

interest（默认值：0.0）：如果这是非零值，则这是持有空头头寸的年利率。这主要是指股票空头卖空

公式：天数 * 价格 * 绝对值（大小）*（利息 / 365）

必须以绝对值表示：0.05 -> 5%

注意，可以通过覆盖方法 _get_credit_interest 更改行为

interest_long（默认值：False）：某些产品如 ETF 对空头和多头头寸收取利息。如果为 True 并且 interest 为非零，则对两个方向都收取利息

leverage（默认值：1.0）：与所需现金相比的杠杆比例

CommissionInfo 类#
基础类用于实际佣金方案。CommInfoBase 是为了保持对 backtrader 提供的原始不完整支持。新的佣金方案从此类派生。默认的 percabs 值也更改为 True .

参数：

percabs（默认值：True）：当 commtype 设置为 COMM_PERC 时，参数 commission 是否理解为 XX% 或 0.XX

如果此参数为 True：0.XX

如果此参数为 False：XX%

返回此佣金方案允许的杠杆水平

get_leverage()
返回在给定价格下满足现金操作所需的大小

getsize(price, cash)
返回操作所需的现金量

getoperationcost(size, price)
返回给定价格的大小值。对于类似期货的对象，固定为大小 * 保证金

getvaluesize(size, price)
返回给定价格的头寸价值。对于类似期货的对象，固定为大小 * 保证金

getvalue(position, price)
返回在给定价格下单个资产所需的实际保证金/保证金。默认实现有以下策略：

使用参数 margin 如果参数 automargin 评估为 False

使用参数 mult，即 mult * price 如果 automargin < 0

使用参数 automargin，即 automargin * price 如果 automargin > 0

get_margin(price)
计算在给定价格下的操作佣金

getcommission(size, price)
计算在给定价格下的操作佣金

pseudoexec：如果为 True，则操作尚未执行

_getcommission(size, price, pseudoexec)
返回头寸的实际损益

profitandloss(size, price, newprice)
计算价格差异的现金调整

cashadjust(size, price, newprice)
计算股票卖空或特定产品的信用费用

get_credit_interest(data, pos, dt)
此方法返回由经纪商收取的信用利息费用。

在 size > 0 的情况下，仅当类的参数 interest_long 为 True 时才调用此方法

计算信用利率的公式是：公式：天数 * 价格 * 绝对值（大小）*（利息 / 365）

_get_credit_interest(data, size, price, days, dt0, dt1)
参数：

data：收取利息的数据馈送
size：当前头寸大小。> 0 表示多头头寸，< 0 表示空头头寸（此参数不会为 0）
price：当前头寸价格
days：自上次信用计算以来经过的天数（这是（dt0 - dt1）.days）
dt0：（datetime.datetime）当前日期时间
dt1：（datetime.datetime）上次计算的日期时间
默认实现中不使用 dt0 和 dt1，它们作为覆盖方法的额外输入提供。
###############################################################################################################
扩展佣金#
佣金及相关功能由一个单一的类 CommissionInfo 管理，通常通过调用 broker.setcommission 实例化。

这个概念限于带有保证金和每合同固定佣金的期货和基于价格/数量百分比佣金的股票。这不是最灵活的方案，但它已经发挥了它的作用。

GitHub 上的一个增强请求（#29）导致了一些重构，以便：

保持 CommissionInfo 和 broker.setcommission 与原始行为兼容
对代码进行一些清理
使佣金方案灵活，以支持增强请求和进一步的可能性
在进入示例之前的实际工作：

class CommInfoBase(with_metaclass(MetaParams)):
    COMM_PERC, COMM_FIXED = range(2)

    params = (
        ('commission', 0.0), ('mult', 1.0), ('margin', None),
        ('commtype', None),
        ('stocklike', False),
        ('percabs', False),
    )
引入了一个 CommissionInfo 的基类，该类添加了新的参数：

commtype（默认值：None）

这是兼容性的关键。如果值为 None，CommissionInfo 对象和 broker.setcommission 的行为将与以前相同。具体如下：

如果设置了 margin，则佣金方案是期货，每合同有固定佣金
如果未设置 margin，则佣金方案是股票，采用百分比方法
如果值是 COMM_PERC 或 COMM_FIXED（或派生类中的任何其他值），则显然决定了佣金是固定的还是基于百分比的
stocklike（默认值：False）

如上所述，旧 CommissionInfo 对象中的实际行为由 margin 参数决定。

如果 commtype 设置为其他值，则此值指示资产是类似期货的资产（将使用保证金并进行基于条形图的现金调整）还是类似股票的资产。

percabs（默认值：False）

如果为 False，则百分比必须以相对术语传递（xx%）

如果为 True，则百分比必须以绝对值传递（0.xx）

CommissionInfo 是从 CommInfoBase 派生的，将此参数的默认值更改为 True 以保持兼容行为。

所有这些参数也可以在 broker.setcommission 中使用，现在看起来像这样：

def setcommission(self,
                  commission=0.0, margin=None, mult=1.0,
                  commtype=None, percabs=True, stocklike=False,
                  name=None):
注意以下几点：

percabs 为 True，以保持与上述 CommissionInfo 对象的旧调用的兼容行为
旧的测试佣金方案的示例已重新编写以支持命令行参数和新行为。使用帮助如下：

$ ./commission-schemes.py --help
usage: commission-schemes.py [-h] [--data DATA] [--fromdate FROMDATE]
                             [--todate TODATE] [--stake STAKE]
                             [--period PERIOD] [--cash CASH] [--comm COMM]
                             [--mult MULT] [--margin MARGIN]
                             [--commtype {none,perc,fixed}] [--stocklike]
                             [--percrel] [--plot] [--numfigs NUMFIGS]

Commission schemes

optional arguments:
  -h, --help            show this help message and exit
  --data DATA, -d DATA  data to add to the system (default:
                        ../../datas/2006-day-001.txt)
  --fromdate FROMDATE, -f FROMDATE
                        Starting date in YYYY-MM-DD format (default:
                        2006-01-01)
  --todate TODATE, -t TODATE
                        Starting date in YYYY-MM-DD format (default:
                        2006-12-31)
  --stake STAKE         Stake to apply in each operation (default: 1)
  --period PERIOD       Period to apply to the Simple Moving Average (default:
                        30)
  --cash CASH           Starting Cash (default: 10000.0)
  --comm COMM           Commission factor for operation, either apercentage or
                        a per stake unit absolute value (default: 2.0)
  --mult MULT           Multiplier for operations calculation (default: 10)
  --margin MARGIN       Margin for futures-like operations (default: 2000.0)
  --commtype {none,perc,fixed}
                        Commission - choose none for the old CommissionInfo
                        behavior (default: none)
  --stocklike           If the operation is for stock-like assets orfuture-
                        like assets (default: False)
  --percrel             If perc is expressed in relative xx% ratherthan
                        absolute value 0.xx (default: False)
  --plot, -p            Plot the read data (default: False)
  --numfigs NUMFIGS, -n NUMFIGS
                        Plot using numfigs figures (default: 1)
让我们进行一些运行来重新创建原始佣金方案的原始行为。

期货佣金（固定且带保证金）#
执行和图表：

$ ./commission-schemes.py --comm 2.0 --margin 2000.0 --mult 10 --plot
输出显示固定佣金为 2.0 货币单位（默认 stake 为 1）：

2006-03-09, BUY CREATE, 3757.59
2006-03-10, BUY EXECUTED, Price: 3754.13, Cost: 2000.00, Comm 2.00
2006-04-11, SELL CREATE, 3788.81
2006-04-12, SELL EXECUTED, Price: 3786.93, Cost: 2000.00, Comm 2.00
2006-04-12, TRADE PROFIT, GROSS 328.00, NET 324.00
...
股票佣金（百分比且无保证金）#
执行和图表：

$ ./commission-schemes.py --comm 0.005 --margin 0 --mult 1 --plot
为了提高可读性，可以使用相对百分比值：

$ ./commission-schemes.py --percrel --comm 0.5 --margin 0 --mult 1 --plot
现在 0.5 直接表示 0.5%

输出在两种情况下都是：

2006-03-09, BUY CREATE, 3757.59
2006-03-10, BUY EXECUTED, Price: 3754.13, Cost: 3754.13, Comm 18.77
2006-04-11, SELL CREATE, 3788.81
2006-04-12, SELL EXECUTED, Price: 3786.93, Cost: 3754.13, Comm 18.93
2006-04-12, TRADE PROFIT, GROSS 32.80, NET -4.91
...
期货佣金（百分比且带保证金）#
使用新参数，基于百分比的期货方案：

$ ./commission-schemes.py --commtype perc --percrel --comm 0.5 --margin 2000 --mult 10 --plot
不意外的是，通过改变佣金……最终结果也改变了

输出显示佣金现在是可变的：

2006-03-09, BUY CREATE, 3757.59
2006-03-10, BUY EXECUTED, Price: 3754.13, Cost: 2000.00, Comm 18.77
2006-04-11, SELL CREATE, 3788.81
2006-04-12, SELL EXECUTED, Price: 3786.93, Cost: 2000.00, Comm 18.93
2006-04-12, TRADE PROFIT, GROSS 328.00, NET 290.29
...
在之前的运行中设置了 2.0 货币单位（对于默认 stake 为 1）

另一个帖子将详细说明新类和自定义佣金方案的实现。

示例#
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse
import datetime

import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicators as btind


class SMACrossOver(bt.Strategy):
    params = (
        ('stake', 1),
        ('period', 30),
    )

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order

 has been completed
        # Attention: broker could reject order if not enougth cash
        if order.status in [order.Completed, order.Canceled, order.Margin]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

    def notify_trade(self, trade):
        if trade.isclosed:
            self.log('TRADE PROFIT, GROSS %.2f, NET %.2f' %
                     (trade.pnl, trade.pnlcomm))

    def __init__(self):
        sma = btind.SMA(self.data, period=self.p.period)
        # > 0 crossing up / < 0 crossing down
        self.buysell_sig = btind.CrossOver(self.data, sma)

    def next(self):
        if self.buysell_sig > 0:
            self.log('BUY CREATE, %.2f' % self.data.close[0])
            self.buy(size=self.p.stake)  # keep order ref to avoid 2nd orders

        elif self.position and self.buysell_sig < 0:
            self.log('SELL CREATE, %.2f' % self.data.close[0])
            self.sell(size=self.p.stake)


def runstrategy():
    args = parse_args()

    # Create a cerebro
    cerebro = bt.Cerebro()

    # Get the dates from the args
    fromdate = datetime.datetime.strptime(args.fromdate, '%Y-%m-%d')
    todate = datetime.datetime.strptime(args.todate, '%Y-%m-%d')

    # Create the 1st data
    data = btfeeds.BacktraderCSVData(
        dataname=args.data,
        fromdate=fromdate,
        todate=todate)

    # Add the 1st data to cerebro
    cerebro.adddata(data)

    # Add a strategy
    cerebro.addstrategy(SMACrossOver, period=args.period, stake=args.stake)

    # Add the commission - only stocks like a for each operation
    cerebro.broker.setcash(args.cash)

    commtypes = dict(
        none=None,
        perc=bt.CommInfoBase.COMM_PERC,
        fixed=bt.CommInfoBase.COMM_FIXED)

    # Add the commission - only stocks like a for each operation
    cerebro.broker.setcommission(commission=args.comm,
                                 mult=args.mult,
                                 margin=args.margin,
                                 percabs=not args.percrel,
                                 commtype=commtypes[args.commtype],
                                 stocklike=args.stocklike)

    # And run it
    cerebro.run()

    # Plot if requested
    if args.plot:
        cerebro.plot(numfigs=args.numfigs, volume=False)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Commission schemes',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,)

    parser.add_argument('--data', '-d',
                        default='../../datas/2006-day-001.txt',
                        help='data to add to the system')

    parser.add_argument('--fromdate', '-f',
                        default='2006-01-01',
                        help='Starting date in YYYY-MM-DD format')

    parser.add_argument('--todate', '-t',
                        default='2006-12-31',
                        help='Starting date in YYYY-MM-DD format')

    parser.add_argument('--stake', default=1, type=int,
                        help='Stake to apply in each operation')

    parser.add_argument('--period', default=30, type=int,
                        help='Period to apply to the Simple Moving Average')

    parser.add_argument('--cash', default=10000.0, type=float,
                        help='Starting Cash')

    parser.add_argument('--comm', default=2.0, type=float,
                        help=('Commission factor for operation, either a'
                              'percentage or a per stake unit absolute value'))

    parser.add_argument('--mult', default=10, type=int,
                        help='Multiplier for operations calculation')

    parser.add_argument('--margin', default=2000.0, type=float,
                        help='Margin for futures-like operations')

    parser.add_argument('--commtype', required=False, default='none',
                        choices=['none', 'perc', 'fixed'],
                        help=('Commission - choose none for the old'
                              ' CommissionInfo behavior'))

    parser.add_argument('--stocklike', required=False, action='store_true',
                        help=('If the operation is for stock-like assets or'
                              'future-like assets'))

    parser.add_argument('--percrel', required=False, action='store_true',
                        help=('If perc is expressed in relative xx% rather'
                              'than absolute value 0.xx'))

    parser.add_argument('--plot', '-p', action='store_true',
                        help='Plot the read data')

    parser.add_argument('--numfigs', '-n', default=1,
                        help='Plot using numfigs figures')

    return parser.parse_args()


if __name__ == '__main__':
    runstrategy()
########################################################################################################################
自定义佣金#
重新设计 CommInfo 对象以实现当前版本的最重要部分包括：

保留原始 CommissionInfo 类和行为
为轻松创建用户定义的佣金打开大门
将格式 xx% 作为新佣金方案的默认值，而不是 0.xx（这只是个口味问题），同时保持行为可配置
定义佣金方案#
这涉及 1 到 2 个步骤：

子类化 CommInfoBase#
仅更改默认参数可能就足够了。backtrader 已经在模块 backtrader.commissions 中使用一些定义进行了此操作。期货的常规行业标准是每合同和每轮固定金额。定义可以这样做：

class CommInfo_Futures_Fixed(CommInfoBase):
   params = (
       ('stocklike', False),
       ('commtype', CommInfoBase.COMM_FIXED),
   )
对于股票和按百分比计算的佣金：

class CommInfo_Stocks_Perc(CommInfoBase):
    params = (
        ('stocklike', True),
        ('commtype', CommInfoBase.COMM_PERC),
    )
如上所述，此处解释百分比的默认值（作为参数 commission 传递）为：xx%。如果需要旧的/其他行为 0.xx，可以轻松实现：

class CommInfo_Stocks_PercAbs(CommInfoBase):
    params = (
        ('stocklike', True),
        ('commtype', CommInfoBase.COMM_PERC),
        ('percabs', True),
    )
重写 _getcommission 方法（如有必要）#
定义如下：

def _getcommission(self, size, price, pseudoexec):
   '''Calculates the commission of an operation at a given price

   pseudoexec: if True the operation has not yet been executed
   '''
下面的实际示例中有更多详细信息。

如何将其应用于平台#
一旦有了 CommInfoBase 子类，诀窍是使用 broker.addcommissioninfo 而不是通常的 broker.setcommission。后者将在内部使用旧版 CommissionInfoObject。

...

comminfo = CommInfo_Stocks_PercAbs(commission=0.005)  # 0.5%
cerebro.broker.addcommissioninfo(comminfo)
addcommissioninfo 方法定义如下：

def addcommissioninfo(self, comminfo, name=None):
    self.comminfo[name] = comminfo
设置 name 意味着 comminfo 对象将仅适用于具有该名称的资产。默认值 None 表示它适用于系统中的所有资产。

实际示例#
问题 #45 询问一种适用于期货的佣金方案，该方案基于百分比，并使用整个“虚拟”合约价值的佣金百分比，即：包括期货乘数在佣金计算中。

import backtrader as bt

class CommInfo_Fut_Perc_Mult(bt.CommInfoBase):
    params = (
      ('stocklike', False),  # Futures
      ('commtype', bt.CommInfoBase.COMM_PERC),  # Apply % Commission
    # ('percabs', False),  # pass perc as xx% which is the default
    )

    def _getcommission(self, size, price, pseudoexec):
        return size * price * self.p.commission * self.p.mult
将其放入系统中：

comminfo = CommInfo_Fut_Perc_Mult(
    commission=0.1,  # 0.1%
    mult=10,
    margin=2000  # Margin is needed for futures-like instruments
)

cerebro.addcommissioninfo(comminfo)
如果更喜欢 0.xx 格式作为默认值，只需将参数 percabs 设置为 True：

class CommInfo_Fut_Perc_Mult(bt.CommInfoBase):
    params = (
      ('stocklike', False),  # Futures
      ('commtype', bt.CommInfoBase.COMM_PERC),  # Apply % Commission
      ('percabs', True),  # pass perc as 0.xx
    )

comminfo = CommInfo_Fut_Perc_Mult(
    commission=0.001,  # 0.1%
    mult=10,
    margin=2000  # Margin is needed for futures-like instruments
)

cerebro.addcommissioninfo(comminfo)
解释 pseudoexec#
让我们回顾 _getcommission 的定义：

def _getcommission(self, size, price, pseudoexec):
    '''Calculates the commission of an operation at a given price

    pseudoexec: if True the operation has not yet been executed
    '''
pseudoexec 参数的目的是在平台可能调用此方法进行可用现金的预计算和其他一些任务时使用。

这意味着该方法可能（实际上确实会）使用相同的参数多次调用。

pseudoexec 指示调用是否对应于订单的实际执行。尽管乍看之下这似乎不“相关”，但在以下情景中却是如此：

经纪商在期货往返佣金超过 5000 单位合同时提供 50% 的折扣。

在这种情况下，如果没有 pseudoexec，对该方法的多次非执行调用将迅速触发折扣到位的假设。

将此情景付诸实践：

import backtrader as bt

class CommInfo_Fut_Discount(bt.CommInfoBase):
    params = (
      ('stocklike', False),  # Futures
      ('commtype', bt.CommInfoBase.COMM_FIXED),  # Apply Commission

      # Custom params for the discount
      ('discount_volume', 5000),  # minimum contracts to achieve discount
      ('discount_perc', 50.0),  # 50.0% discount
    )

    negotiated_volume = 0  # attribute to keep track of the actual volume

    def _getcommission(self, size, price, pseudoexec):
        if self.negotiated_volume > self.p.discount_volume:
           actual_discount = self.p.discount_perc / 100.0
        else:
           actual_discount = 0.0

        commission = self.p.commission * (1.0 - actual_discount)
        commvalue = size * price * commission

        if not pseudoexec:
           # keep track of actual real executed size for future discounts
           self.negotiated_volume += size

        return commvalue
CommInfoBase 文档字符串和参数#
有关 CommInfoBase 的参考，请参见“佣金：股票与期货”。
#################################################################################################################
利息#
在某些情况下，由于资产操作包含利率，实际经纪商的现金金额可能会减少。例如：

股票的卖空
ETF 的多头和空头操作
该费用直接从经纪账户的现金余额中扣除。但它仍然可以看作是佣金方案的一部分。因此，它已在 backtrader 中进行了建模。

CommInfoBase 类（以及主要的 CommissionInfo 接口对象）已扩展了：

两个新参数，用于设置利率并确定是否仅应用于空头还是同时应用于多头和空头
参数#
interest（默认值：0.0）

如果非零，这是持有卖空头寸时收取的年度利息。这主要用于股票卖空。

应用的默认公式：days * price * size * (interest / 365)

必须以绝对值指定：0.05 -> 5%

注意：可以通过重写方法 get_credit_interest 来更改行为

interest_long（默认值：False）

一些产品如 ETF，在多头和空头头寸上都收取利息。如果为 True 并且 interest 非零，则多头和空头方向都将收取利息。

公式#
默认实现将使用以下公式：

days * abs(size) * price * (interest / 365)
其中：

days：自头寸开立或上次利息计算以来经过的天数
重写公式#
要更改公式，需要子类化 CommissionInfo。需要重写的方法是：

def _get_credit_interest(self, size, price, days, dt0, dt1):
    '''
    此方法返回经纪商收取的利息成本。

    对于 ``size > 0`` 的情况，仅在类参数 ``interest_long`` 为 ``True`` 时调用此方法。

    计算利率的公式为：

    公式：``days * price * abs(size) * (interest / 365)``

    参数：
      - ``data``：收取利息的数据源
      - ``size``：当前头寸大小。> 0 表示多头头寸，< 0 表示空头头寸（此参数不会为 ``0``）
      - ``price``：当前头寸价格
      - ``days``：自上次利息计算以来经过的天数（这是（dt0 - dt1）.days）
      - ``dt0``：当前日期时间（datetime.datetime）
      - ``dt1``：上次计算日期时间（datetime.datetime）

    ``dt0`` 和 ``dt1`` 在默认实现中未使用，并作为重写方法的额外输入提供
    '''
可能经纪商在计算利率时不考虑周末或银行假日。在这种情况下，子类如下：

import backtrader as bt

class MyCommissionInfo(bt.CommInfo):

   def _get_credit_interest(self, size, price, days, dt0, dt1):
       return 1.0 * abs(size) * price * (self.p.interest / 365.0)
在这种情况下，公式中：

days 被替换为 1.0
因为如果周末/银行假日不算数，则下一次计算总是在上一次计算后的一个交易日进行。

31 41分析器.txt ##################################################
文件路径: 41分析器.txt
================================================================================

分析器#
无论是回测还是交易，能够分析交易系统的表现对于理解是否不仅仅获得了利润，而且是否在实现利润的过程中承担了过多的风险，或者与参考资产（或无风险资产）相比是否真的值得付出努力，都是关键。

这就是分析器对象的作用：提供对已发生情况或当前情况的分析。

分析器的性质 接口的设计参照了线条对象，例如具有 next 方法，但有一个主要的区别：分析器不包含线条。

这意味着它们在内存方面不是很消耗资源，因为即使在分析了成千上万个价格条之后，它们可能仍然只在内存中保存单个结果。

在生态系统中的位置#
分析器对象（如同策略、观察者和数据）通过 cerebro 实例添加到系统中：

addanalyzer(ancls, *args, **kwargs)
但在 cerebro.run 操作期间，对于系统中存在的每个策略，将会发生以下情况：

ancls 在 cerebro.run 期间会用 *args 和 **kwargs 实例化
ancls 实例将会附加到策略上
这意味着：

如果回测运行包含例如 3 个策略，那么将创建 3 个 ancls 实例，并且每个实例将附加到不同的策略上。

结论：分析器分析单个策略的表现，而不是整个系统的表现。

附加位置#
某些分析器对象可能实际上使用其他分析器来完成其工作。例如：SharpeRatio 使用 TimeReturn 的输出进行计算。

这些子分析器或从属分析器也将插入到创建它们的同一策略中。但它们对用户是完全不可见的。

属性#
为了完成预期的工作，分析器对象提供了一些默认属性，这些属性会自动传递并在实例中设置，以便于使用：

self.strategy：对分析器对象正在运行的策略子类的引用。策略可以访问的任何内容，分析器也可以访问。
self.datas[x]：策略中存在的数据源数组。虽然可以通过策略引用访问，但快捷方式使工作更舒适。
self.data：对 self.datas[0] 的快捷方式，以增加舒适度。
self.dataX：对不同的 self.datas[x] 的快捷方式。
还有一些其他别名可用，尽管它们可能有些多余：

self.dataX_Y，其中 X 是对 self.datas[X] 的引用，Y 指的是线条，最终指向 self.datas[X].lines[Y]。 如果线条有名称，还可以使用以下命名：

self.dataX_Name，解析为 self.datas[X].Name，按名称而不是按索引返回线条。 对于第一个数据，最后两个快捷方式在没有初始 X 数字引用的情况下可用。例如：

self.data_2 指 self.datas[0].lines[2]。

self.data_close 指 self.datas[0].close。

返回分析结果#
Analyzer 基类创建了一个 self.rets（类型为 collections.OrderedDict）成员属性来返回分析结果。这是在 create_analysis 方法中完成的，子类可以覆盖该方法以创建自定义分析器。

操作模式#
虽然分析器对象不是线条对象，因此不迭代线条，但它们被设计为遵循相同的操作模式。

在系统启动之前实例化（因此调用 __init__）。
使用 start 信号表示操作开始。
prenext / nextstart / next 方法将根据策略的计算最小周期被调用。
prenext 和 nextstart 的默认行为是调用 next，因为分析器可能会从系统开始运行的第一刻起进行分析。
在线条对象中通常调用 len(self) 以检查实际条数。这在分析器中也适用，通过返回 self.strategy 的值。
订单和交易将像通知策略一样通过 notify_order 和 notify_trade 进行通知。
现金和价值也将通过 notify_cashvalue 方法像对策略那样进行通知。
现金、价值、基金价值和基金份额也将通过 notify_fund 方法像对策略那样进行通知。
使用 stop 信号表示操作结束。
一旦常规操作周期完成，分析器将提供用于提取/输出信息的附加方法：
get_analysis：理想情况下（不是强制的）返回一个包含分析结果的字典样对象。
print 使用标准的 backtrader.WriterFile（除非被覆盖）写出 get_analysis 的分析结果。
pprint（漂亮打印）使用 Python 的 pprint 模块打印 get_analysis 结果。
最后：

get_analysis 创建一个类型为 collections.OrderedDict 的成员属性 self.ret，分析器将分析结果写入其中。

分析器的子类可以覆盖此方法以改变此行为。

分析器模式#
在 backtrader 平台中开发分析器对象揭示了生成分析的两种不同使用模式：

在执行过程中通过 notify_xxx 和 next 方法收集信息，并在 next 中生成当前的分析信息。
例如，TradeAnalyzer 仅使用 notify_trade 方法生成统计数据。
如上所述收集信息（或不收集），但在 stop 方法期间进行单次生成分析。
SQN（系统质量编号）在 notify_trade 期间收集交易信息，但在 stop 方法期间生成统计数据。
快速示例#
尽可能简单：

from __future__ import (absolute_import, division, print_function, unicode_literals)
import datetime
import backtrader as bt
import backtrader.analyzers as btanalyzers
import backtrader.feeds as btfeeds
import backtrader.strategies as btstrats

cerebro = bt.Cerebro()

# 数据
dataname = '../datas/sample/2005-2006-day-001.txt'
data = btfeeds.BacktraderCSVData(dataname=dataname)

cerebro.adddata(data)

# 策略
cerebro.addstrategy(btstrats.SMA_CrossOver)

# 分析器
cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe')

thestrats = cerebro.run()
thestrat = thestrats[0]

print('Sharpe Ratio:', thestrat.analyzers.mysharpe.get_analysis())
执行它（已将其存储在 analyzer-test.py 中）：

$ ./analyzer-test.py
Sharpe Ratio: {'sharperatio': 11.647332609673256}
没有绘图，因为 SharpeRatio 是在计算结束时的单一值。

分析器的取证分析 让我们重复一下，分析器不是线条对象，但为了无缝集成到 backtrader 生态系统中，遵循了几个线条对象的内部 API 约定（实际上是它们的混合）。

注意

SharpeRatio 的代码已经演变，例如考虑了年化，此版本仅应作为参考。

请查看分析器参考。

此外还有一个 SharpeRatio_A 提供了直接以年化形式给出的值，而不管所需的时间范围。

SharpeRatio 的代码作为基础（简化版本）：

from __future__ import (absolute_import, division, print_function, unicode_literals)
import operator
from backtrader.utils.py3 import map
from backtrader import Analyzer, TimeFrame
from backtrader.mathsupport import average, standarddev
from backtrader.analyzers import AnnualReturn

class SharpeRatio(Analyzer):
    params = (('timeframe', TimeFrame.Years), ('riskfreerate', 0.01),)

    def __init__(self):
        super(SharpeRatio, self).__init__()
        self.anret = AnnualReturn()

    def start(self):
        # Not needed ... but could be used
        pass

    def next(self):
        # Not needed ... but could be used
        pass

    def stop(self):
        retfree = [self.p.riskfreerate] * len(self.anret.rets)
        retavg = average(list(map(operator.sub, self.anret.rets, retfree)))
        retdev = standarddev(self.anret.rets)
        self.ratio = retavg / retdev

    def get_analysis(self):
        return dict(sharperatio=self.ratio)
代码可以分解为：

params 声明
尽管声明的参数没有使用（作为示例），分析器像大多数其他对象一样支持参数。
__init__ 方法
就像策略在 __init__ 中声明指标一样，分析器也声明支持对象。
在这种情况下：SharpeRatio 使用年度回报计算。计算将是自动的，并且将可用于 SharpeRatio 进行自己的计算。
next 方法
SharpeRatio 不需要它，但此方法将在父策略 next 的每次调用后被调用。
start 方法
在回测开始前调用。可以用于额外的初始化任务。
SharpeRatio 不需要它。

stop 方法
在回测结束后调用。就像 SharpeRatio 所做的那样，它可以用于完成/进行计算。
get_analysis 方法（返回字典）
为外部调用者提供生成的分析。
返回：包含分析结果的字典。

参考#
class backtrader.Analyzer()
Analyzer 基类。所有分析器都是此类的子类。

分析器实例在策略的框架内运行，并为该策略提供分析。

自动设置的成员属性：

self.strategy（提供对策略及其可访问内容的访问）
self.datas[x] 提供对系统中存在的数据源数组的访问，这些数据源也可以通过策略引用访问
self.data 提供对 self.datas[0] 的访问
self.dataX -> self.datas[X]
self.dataX_Y -> self.datas[X].lines[Y]
self.dataX_name -> self.datas[X].name
self.data_name -> self.datas[0].name
self.data_Y -> self.datas[0].lines[Y]
这不是线条对象，但方法和操作遵循相同的设计：

在实例化和初始设置期间 __init__
使用 start / stop 表示操作的开始和结束
prenext / nextstart / next 方法家族，遵循策略中相同方法的调用
notify_trade / notify_order / notify_cashvalue / notify_fund 接收与策略等效方法相同的通知
操作模式是开放的，没有首选模式。因此，分析可以通过 next 调用生成，在 stop 期间生成，也可以通过单个方法如 notify_trade 生成。

重要的是覆盖 get_analysis 以返回包含分析结果的字典样对象（实际格式取决于实现）。

start()
调用以指示操作开始，给分析器时间设置所需内容。
stop()
调用以指示操作结束，给分析器时间关闭所需内容。
prenext()
在策略的每次 prenext 调用期间调用，直到达到策略的最小周期。
分析器的默认行为是调用 next。
nextstart()
在策略的 nextstart 调用时调用一次，当首次达到最小周期时。
next()
在策略的每次 next 调用期间调用，一旦达到策略的最小周期。
notify_cashvalue(cash, value)
在每个 next 周期之前接收现金/价值通知。
notify_fund(cash, value, fundvalue, shares)
接收当前现金、价值、基金价值和基金份额。
notify_order(order)
在每个 next 周期之前接收订单通知。
notify_trade(trade)
在每个 next 周期之前接收交易通知。
get_analysis()
返回包含分析结果的字典样对象。
字典中分析结果的键和值的格式取决于实现。
甚至不强制结果是字典样对象，只是一种约定。
默认实现返回由默认 create_analysis 方法创建的默认 OrderedDict rets。
create_analysis()
供子类覆盖。提供创建保存分析结果的结构的机会。
默认行为是创建名为 rets 的 OrderedDict。
print(*args, **kwargs)
使用标准 Writerfile 对象打印 get_analysis 返回的结果，默认写入标准输出。
pprint(*args, **kwargs)
使用 Python 的 pprint 模块打印 get_analysis 返回的结果。
len()
支持在分析器上调用 len，实际上返回分析器运行的策略的当前长度。
############################################################################################################################################
PyFolio#
注意，截至（至少）2017-07-25，pyfolio 的 API 已更改，create_full_tear_sheet 不再有 gross_lev 作为命名参数。因此，集成示例无法正常工作。

引用 pyfolio 主页面 http://quantopian.github.io/pyfolio/ 的内容： pyfolio 是一个由 Quantopian Inc. 开发的用于金融投资组合的表现和风险分析的 Python 库。它与开源回测库 Zipline 配合良好，现在它也可以很好地与 backtrader 配合。所需的内容包括：

显然需要 pyfolio
以及它的依赖项（如 pandas、seaborn 等）
注意，在与 0.5.1 版本集成期间，需要更新依赖项的最新版本，例如将之前安装的 seaborn 从 0.7.0-dev 更新到 0.7.1，显然是由于缺少方法 swarmplot。

用法#
将 PyFolio 分析器添加到 cerebro 中：

cerebro.addanalyzer(bt.analyzers.PyFolio)
运行并检索第一个策略：

strats = cerebro.run()
strat0 = strats[0]
使用你给分析器命名的名称或默认名称（pyfolio）来检索分析器。例如：

pyfolio = strats.analyzers.getbyname('pyfolio')
使用分析器方法 get_pf_items 检索 pyfolio 后续需要的四个组件：

returns, positions, transactions, gross_lev = pyfolio.get_pf_items()
注意

集成是通过查看 pyfolio 的测试样本并复制相同的标题（或缺少的部分）来完成的。

与 pyfolio 一起工作（这已经超出了 backtrader 生态系统的范围）

一些与 backtrader 无关的使用注意事项：

pyfolio 自动绘图在 Jupyter Notebook 之外也能工作，但在 Notebook 内部效果最好。
pyfolio 数据表的输出在 Jupyter Notebook 之外几乎不起作用，但在 Notebook 内部可以正常工作。
结论很简单，如果希望使用 pyfolio：在 Jupyter Notebook 内工作。

示例代码 代码看起来像这样：

...
cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')
...
results = cerebro.run()
strat = results[0]
pyfoliozer = strat.analyzers.getbyname('pyfolio')
returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()
...
...
# pyfolio showtime
import pyfolio as pf
pf.create_full_tear_sheet(
    returns,
    positions=positions,
    transactions=transactions,
    gross_lev=gross_lev,
    live_start_date='2005-05-01',  # 此日期是样本特定的
    round_trips=True)

# 此时表格和图表将显示
参考#
查看分析器参考以了解 PyFolio 分析器及其内部使用的分析器。
#############################################################################################################
Pyfolio 集成#
在 Ticket #108 中提出了一个投资组合工具，即 pyfolio 的集成。

一开始看教程觉得很难，因为 zipline 和 pyfolio 之间的紧密集成，但 pyfolio 提供的一些其他用途的示例测试数据实际上非常有用，可以解码幕后运行的内容，从而实现集成。

在 backtrader 中大多数部分已经就位：

分析器基础设施
子分析器
TimeReturn 分析器
只需要一个主 PyFolio 分析器和三个简单的子分析器。再加上依赖于 pyfolio 所需的依赖项之一，即 pandas 的方法。

最具挑战的部分是…“正确获取所有依赖项”。

更新 pandas
更新 numpy
更新 scikit-lean
更新 seaborn
在类似 Unix 的环境中，有一个 C 编译器，一切都是时间问题。在 Windows 上，即使安装了特定的 Microsoft 编译器（在这种情况下是 Python 2.7 的链），事情也失败了。但一个知名网站拥有最新的 Windows 软件包集合，提供了帮助。如果你需要它，可以访问：

http://www.lfd.uci.edu/~gohlke/pythonlibs/

如果没有测试集成，它就不会完成，这就是为什么通常的示例总是存在的原因。

没有 PyFolio#
示例使用 random.randint 来决定何时买卖，因此这只是检查事情是否正常运行：

$ ./pyfoliotest.py --printout --no-pyfolio --plot
输出：

Len,Datetime,Open,High,Low,Close,Volume,OpenInterest
0001,2005-01-03T23:59:59,38.36,38.90,37.65,38.18,25482800.00,0.00
BUY  1000 @%23.58
0002,2005-01-04T23:59:59,38.45,38.54,36.46,36.58,26625300.00,0.00
BUY  1000 @%36.58
SELL 500 @%22.47
0003,2005-01-05T23:59:59,36.69,36.98,36.06,36.13,18469100.00,0.00
...
SELL 500 @%37.51
0502,2006-12-28T23:59:59,25.62,25.72,25.30,25.36,11908400.00,0.00
0503,2006-12-29T23:59:59,25.42,25.82,25.33,25.54,16297800.00,0.00
SELL 250 @%17.14
SELL 250 @%37.01
有 3 个数据，多个买卖操作在测试运行的默认两年期间随机选择和分散。

一个 PyFolio 运行#
pyfolio 在 Jupyter Notebook 内运行效果很好，包括内联绘图。以下是 notebook 示例：

%matplotlib inline

from __future__ import (absolute_import, division, print_function, unicode_literals)

import argparse
import datetime
import random

import backtrader as bt

class St(bt.Strategy):
    params = (
        ('printout', False),
        ('stake', 1000),
    )

    def __init__(self):
        pass

    def start(self):
        if self.p.printout:
            txtfields = list()
            txtfields.append('Len')
            txtfields.append('Datetime')
            txtfields.append('Open')
            txtfields.append('High')
            txtfields.append('Low')
            txtfields.append('Close')
            txtfields.append('Volume')
            txtfields.append('OpenInterest')
            print(','.join(txtfields))

    def next(self):
        if self.p.printout:
            txtfields = list()
            txtfields.append('%04d' % len(self))
            txtfields.append(self.data.datetime.datetime(0).isoformat())
            txtfields.append('%.2f' % self.data0.open[0])
            txtfields.append('%.2f' % self.data0.high[0])
            txtfields.append('%.2f' % self.data0.low[0])
            txtfields.append('%.2f' % self.data0.close[0])
            txtfields.append('%.2f' % self.data0.volume[0])
            txtfields.append('%.2f' % self.data0.openinterest[0])
            print(','.join(txtfields))

        for data in self.datas:
            toss = random.randint(1, 10)
            curpos = self.getposition(data)
            if curpos.size:
                if toss > 5:
                    size = curpos.size // 2
                    self.sell(data=data, size=size)
                    if self.p.printout:
                        print('SELL {} @%{}'.format(size, data.close[0]))

            elif toss < 5:
                self.buy(data=data, size=self.p.stake)
                if self.p.printout:
                    print('BUY  {} @%{}'.format(self.p.stake, data.close[0]))

def runstrat(args=None):
    args = parse_args(args)

    cerebro = bt.Cerebro()
    cerebro.broker.set_cash(args.cash)

    dkwargs = dict()
    if args.fromdate:
        fromdate = datetime.datetime.strptime(args.fromdate, '%Y-%m-%d')
        dkwargs['fromdate'] = fromdate

    if args.todate:
        todate = datetime.datetime.strptime(args.todate, '%Y-%m-%d')
        dkwargs['todate'] = todate

    data0 = bt.feeds.BacktraderCSVData(dataname=args.data0, **dkwargs)
    cerebro.adddata(data0, name='Data0')

    data1 = bt.feeds.BacktraderCSVData(dataname=args.data1, **dkwargs)
    cerebro.adddata(data1, name='Data1')

    data2 = bt.feeds.BacktraderCSVData(dataname=args.data2, **dkwargs)
    cerebro.adddata(data2, name='Data2')

    cerebro.addstrategy(St, printout=args.printout)
    if not args.no_pyfolio:
        cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')

    results = cerebro.run()
    if not args.no_pyfolio:
        strat = results[0]
        pyfoliozer = strat.analyzers.getbyname('pyfolio')

        returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()
        if args.printout:
            print('-- RETURNS')
            print(returns)
            print('-- POSITIONS')
            print(positions)
            print('-- TRANSACTIONS')
            print(transactions)
            print('-- GROSS LEVERAGE')
            print(gross_lev)

        import pyfolio as pf
        pf.create_full_tear_sheet(
            returns,
            positions=positions,
            transactions=transactions,
            gross_lev=gross_lev,
            live_start_date='2005-05-01',
            round_trips=True)

    if args.plot:
        cerebro.plot(style=args.plot_style)

def parse_args(args=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Sample for pivot point and cross plotting')

    parser.add_argument('--data0', required=False,
                        default='../../datas/yhoo-1996-2015.txt',
                        help='Data to be read in')

    parser.add_argument('--data1', required=False,
                        default='../../datas/orcl-1995-2014.txt',
                        help='Data to be read in')

    parser.add_argument('--data2', required=False,
                        default='../../datas/nvda-1999-2014.txt',
                        help='Data to be read in')

    parser.add_argument('--fromdate', required=False,
                        default='2005-01-01',
                        help='Starting date in YYYY-MM-DD format')

    parser.add_argument('--todate', required=False,
                        default='2006-12-31',
                        help='Ending date in YYYY-MM-DD format')

    parser.add_argument('--printout', required=False, action='store_true',
                        help=('Print data lines'))

    parser.add_argument('--cash', required=False, action='store',
                        type=float, default=50000,
                        help=('Cash to start with'))

    parser.add_argument('--plot', required=False, action='store_true',
                        help=('Plot the result'))

    parser.add_argument('--plot-style', required=False, action='store',
                        default='bar', choices=['bar', 'candle', 'line'],
                        help=('Plot style'))

    parser.add_argument('--no-pyfolio', required=False, action='store_true',
                        help=('Do not do pyfolio things'))

    import sys
    aargs = args if args is not None else sys.argv[1:]
    return parser.parse_args(aargs)

runstrat([])
整个数据开始日期：2005-01-03
整个数据结束日期：2006-12-29

$ ./pyfoliotest.py --help
使用：

usage: pyfoliotest.py [-h] [--data0 DATA0] [--data1 DATA1] [--data2 DATA2]
                      [--fromdate FROMDATE] [--todate TODATE] [--printout]
                      [--cash CASH] [--plot] [--plot-style {

bar,candle,line}]
                      [--no-pyfolio]

Sample for pivot point and cross plotting

optional arguments:
  -h, --help            show this help message and exit
  --data0 DATA0         Data to be read in (default: ../../datas/yhoo-1996-2015.txt)
  --data1 DATA1         Data to be read in (default: ../../datas/orcl-1995-2014.txt)
  --data2 DATA2         Data to be read in (default: ../../datas/nvda-1999-2014.txt)
  --fromdate FROMDATE   Starting date in YYYY-MM-DD format (default: 2005-01-01)
  --todate TODATE       Ending date in YYYY-MM-DD format (default: 2006-12-31)
  --printout            Print data lines (default: False)
  --cash CASH           Cash to start with (default: 50000)
  --plot                Plot the result (default: False)
  --plot-style {bar,candle,line}
                        Plot style (default: bar)
  --no-pyfolio          Do not do pyfolio things (default: False)
##################################################################################################
参考#
AnnualReturn#
class backtrader.analyzers.AnnualReturn()
该分析器通过查看年的起点和终点来计算年度回报率。

参数：

无
成员属性：

rets：计算出的年度回报率列表
ret：年度回报率字典（键：年份）
get_analysis： 返回包含年度回报率的字典（键：年份）

Calmar#
class backtrader.analyzers.Calmar()
该分析器计算 Calmar 比率，时间框架可以与基础数据使用的不同。

参数：

timeframe（默认：无）：如果为 None，将使用系统中第一个数据的时间框架。
compression（默认：无）：仅用于子日时间框架，例如通过指定 “TimeFrame.Minutes” 和 60 作为压缩在每小时时间框架上工作。
fund（默认：无）：如果为 None，将自动检测经纪人的实际模式（fundmode - True/False）来决定回报率是基于总净资产价值还是基金价值。见经纪人文档中的 set_fundmode。
get_analysis： 返回一个包含时间段键和对应滚动 Calmar 比率的 OrderedDict。

DrawDown#
class backtrader.analyzers.DrawDown()
该分析器计算交易系统的回撤统计数据，如百分比和美元的回撤值、最大回撤值、回撤长度和最大回撤长度。

参数：

fund（默认：无）：如果为 None，将自动检测经纪人的实际模式（fundmode - True/False）来决定回报率是基于总净资产价值还是基金价值。见经纪人文档中的 set_fundmode。
get_analysis： 返回一个包含回撤统计数据的字典（支持 . 符号表示法和子字典），可用的键/属性包括：

drawdown：回撤值（百分比）
moneydown：回撤值（货币单位）
len：回撤长度
max.drawdown：最大回撤值（百分比）
max.moneydown：最大回撤值（货币单位）
max.len：最大回撤长度
TimeDrawDown#
class backtrader.analyzers.TimeDrawDown()
该分析器计算在选定时间框架上的交易系统回撤，可以与基础数据使用的时间框架不同。

参数：

timeframe（默认：无）：如果为 None，将使用系统中第一个数据的时间框架。
compression（默认：无）：仅用于子日时间框架，例如通过指定 “TimeFrame.Minutes” 和 60 作为压缩在每小时时间框架上工作。
fund（默认：无）：如果为 None，将自动检测经纪人的实际模式（fundmode - True/False）来决定回报率是基于总净资产价值还是基金价值。见经纪人文档中的 set_fundmode。
get_analysis： 返回一个包含回撤统计数据的字典（支持 . 符号表示法和子字典），可用的键/属性包括：

drawdown：回撤值（百分比）
maxdrawdown：最大回撤值（货币单位）
maxdrawdownperiod：回撤长度
GrossLeverage#
class backtrader.analyzers.GrossLeverage()
该分析器计算当前策略的总杠杆。

参数：

fund（默认：无）：如果为 None，将自动检测经纪人的实际模式（fundmode - True/False）来决定回报率是基于总净资产价值还是基金价值。见经纪人文档中的 set_fundmode。
get_analysis： 返回一个字典，其中返回值为值，每个返回值的日期时间点为键。

PositionsValue#
class backtrader.analyzers.PositionsValue()
该分析器报告当前数据集的仓位价值。

参数：

timeframe（默认：无）：如果为 None，将使用系统中第一个数据的时间框架。
compression（默认：无）：仅用于子日时间框架，例如通过指定 “TimeFrame.Minutes” 和 60 作为压缩在每小时时间框架上工作。
headers（默认：False）：在保存结果的字典中添加一个初始键，名称为数据的名称（‘Datetime’ 为键）。
cash（默认：False）：包括实际现金作为额外仓位（对于标头，将使用名称 ‘cash’）。
get_analysis： 返回一个字典，其中返回值为值，每个返回值的日期时间点为键。

PyFolio#
class backtrader.analyzers.PyFolio()
该分析器使用 4 个子分析器收集数据，并将其转换为与 pyfolio 兼容的数据集。

子分析器：

TimeReturn：用于计算全球投资组合价值的回报。
PositionsValue：用于计算每个数据的仓位价值。设置 headers 和 cash 参数为 True。
Transactions：用于记录每个数据上的每笔交易（数量、价格、价值）。设置 headers 参数为 True。
GrossLeverage：跟踪总杠杆（策略投资的程度）。
参数： 这些参数透明地传递给子分析器。

timeframe（默认：bt.TimeFrame.Days）：如果为 None，将使用系统中第一个数据的时间框架。
compression（默认：1）：如果为 None，将使用系统中第一个数据的压缩。
get_analysis： 返回一个字典，其中返回值为值，每个返回值的日期时间点为键。

get_pf_items： 返回一个包含 4 个元素的元组，可用于进一步处理 pyfolio。

returns，positions，transactions，gross_leverage
由于这些对象旨在作为 pyfolio 的直接输入，因此此方法会本地导入 pandas，将内部 backtrader 结果转换为 pandas DataFrames，这是例如 pyfolio.create_full_tear_sheet 预期的输入。如果未安装 pandas，该方法将失败。

LogReturnsRolling#
class backtrader.analyzers.LogReturnsRolling()
该分析器计算给定时间框架和压缩的滚动回报。

参数：

timeframe（默认：无）：如果为 None，将使用系统中第一个数据的时间框架。
compression（默认：无）：仅用于子日时间框架，例如通过指定 “TimeFrame.Minutes” 和 60 作为压缩在每小时时间框架上工作。
data（默认：无）：跟踪的参考资产，而不是投资组合价值。
get_analysis： 返回一个字典，其中返回值为值，每个返回值的日期时间点为键。

PeriodStats#
class backtrader.analyzers.PeriodStats()
计算给定时间框架的基本统计数据。

参数：

timeframe（默认：Years）：如果为 None，将使用系统中第一个数据的时间框架。
compression（默认：1）：仅用于子日时间框架，例如通过指定 “TimeFrame.Minutes” 和 60 作为压缩在每小时时间框架上工作。
fund（默认：无）：如果为 None，将自动检测经纪人的实际模式（fundmode - True/False）来决定回报率是基于总净资产价值还是基金价值。见经纪人文档中的 set_fundmode。
get_analysis： 返回一个包含以下键的字典：

average
stddev
positive
negative
nochange
best
worst
如果参数 zeroispos 设置为 True，则没有变化的周期将计为正数。

Returns#
class backtrader.analyzers.Returns()
使用对数方法计算总回报、平均回报、复合回报和年化回报。

参数：

timeframe（默认：无）：如果为 None，将使用系统中第一个数据的时间框架。
compression（默认：无）：仅用于子日时间框架，例如通过指定 “TimeFrame.Minutes” 和 60 作为压缩在每小时时间框架上工作。
tann（默认：无）：用于年化（归一化）回报的周期数：
天：252
周：52
月：12
年：1
fund（默认：无）：如果为 None，将自动检测经纪人的实际模式（fundmode - True/False）来决定回报率是基于总净资产价值还是基金价值。见经纪人文档中的 set_fundmode。
get_analysis： 返回一个字典，其中返回值为值，每个返回值的日期

时间点为键。返回的字典包含以下键：

rtot：总复合回报
ravg：整个期间的平均回报（特定时间框架）
rnorm：年化/归一化回报
rnorm100：以 100% 表示的年化/归一化回报
SharpeRatio#
class backtrader.analyzers.SharpeRatio()
该分析器使用风险资产（即利率）计算策略的夏普比率。

参数：

timeframe（默认：TimeFrame.Years）
compression（默认：1）：仅用于子日时间框架，例如通过指定 “TimeFrame.Minutes” 和 60 作为压缩在每小时时间框架上工作。
riskfreerate（默认：0.01 -> 1%）：以年利率表示（见下文 convertrate）。
convertrate（默认：True）：将年利率转换为月、周或日利率。不支持子日转换。
factor（默认：无）：如果为 None，将从预定义表中选择年到所选时间框架的转换因子。天：252，周：52，月：12，年：1。否则将使用指定的值。
annualize（默认：False）：如果 convertrate 为 True，夏普比率将在所选时间框架内提供。在大多数情况下，夏普比率以年化形式提供。
stddev_sample（默认：False）：如果设置为 True，将在均值中减少分母 1 来计算标准差。这在计算标准差时使用，如果认为并非所有样本都用于计算。这被称为贝塞尔修正。
daysfactor（默认：无）：旧命名为因子。如果设置为除 None 之外的任何值，并且时间框架为 TimeFrame.Days，将假设这是旧代码并使用该值。
legacyannual（默认：False）：使用 AnnualReturn 分析器，顾名思义仅适用于年份。
fund（默认：无）：如果为 None，将自动检测经纪人的实际模式（fundmode - True/False）来决定回报率是基于总净资产价值还是基金价值。见经纪人文档中的 set_fundmode。
get_analysis： 返回一个包含键 “sharperatio” 的字典，其中包含比率。

SharpeRatio_A#
class backtrader.analyzers.SharpeRatio_A()
夏普比率的扩展，直接以年化形式返回夏普比率。

更改的参数：

annualize（默认：True）
SQN#
class backtrader.analyzers.SQN()
SQN 或系统质量数。由 Van K. Tharp 定义，用于分类交易系统。

1.6 - 1.9 低于平均水平 2.0 - 2.4 平均水平 2.5 - 2.9 良好 3.0 - 5.0 优秀 5.1 - 6.9 杰出 7.0 - 圣杯？

公式：

SquareRoot(NumberTrades) * Average(TradesProfit) / StdDev(TradesProfit)
当交易数量 >= 30 时，sqn 值应被认为是可靠的。

get_analysis： 返回一个包含键 “sqn” 和 “trades” 的字典（已考虑的交易数量）。

TimeReturn#
class backtrader.analyzers.TimeReturn()
该分析器通过查看时间框架的起点和终点来计算回报。

参数：

timeframe（默认：无）：如果为 None，将使用系统中第一个数据的时间框架。
compression（默认：无）：仅用于子日时间框架，例如通过指定 “TimeFrame.Minutes” 和 60 作为压缩在每小时时间框架上工作。
data（默认：无）：跟踪的参考资产，而不是投资组合价值。
get_analysis： 返回一个字典，其中返回值为值，每个返回值的日期时间点为键。

TradeAnalyzer#
class backtrader.analyzers.TradeAnalyzer()
提供已平仓交易的统计数据（还保持未平仓交易的计数）。

总开仓/平仓交易
连胜/连败 当前/最长
总损益/平均损益
胜/负 计数/总损益/平均损益/最大损益
多/空 计数/总损益/平均损益/最大损益
胜/负 计数/总损益/平均损益/最大损益
注意： 分析器使用“自动”字典字段，这意味着如果没有执行交易，则不会生成统计数据。在这种情况下，get_analysis 返回的字典中将有一个单独的字段/子字段：

dictname[‘total’][‘total’] 将具有值 0（该字段也可以使用点符号 dictname.total.total 访问）。
Transactions#
class backtrader.analyzers.Transactions()
该分析器报告系统中每个数据的交易情况。

参数：

headers（默认：True）：在保存结果的字典中添加一个初始键，名称为数据的名称。
该分析器旨在便于与 pyfolio 集成，并从用于它的样本中获取标题名称：

‘date’, ‘amount’, ‘price’, ‘sid’, ‘symbol’, ‘value’
get_analysis： 返回一个字典，其中返回值为值，每个返回值的日期时间点为键。

VWR#
class backtrader.analyzers.VWR()
可变性加权回报：使用对数回报的更好的夏普比率。

别名：

VariabilityWeightedReturn
参数：

timeframe（默认：无）：如果为 None，则整个回测期间的回报将被报告。
compression（默认：无）：仅用于子日时间框架，例如通过指定 “TimeFrame.Minutes” 和 60 作为压缩在每小时时间框架上工作。
tann（默认：无）：用于年化（归一化）平均回报的周期数。如果为 None，则使用标准 t 值，即：
天：252
周：52
月：12
年：1
tau（默认：2.0）：计算因子（见文献）
sdev_max（默认：0.20）：最大标准差（见文献）
fund（默认：无）：如果为 None，将自动检测经纪人的实际模式（fundmode - True/False）来决定回报率是基于总净资产价值还是基金价值。见经纪人文档中的 set_fundmode。
get_analysis： 返回一个字典，其中返回值为值，每个返回值的日期时间点为键。返回的字典包含以下键：

vwr：可变性加权回报


32 42统计.txt ##################################################
文件路径: 42统计.txt
================================================================================

统计#
在 backtrader 中运行的策略主要处理数据源和指标。数据源添加到 Cerebro 实例中，并最终成为策略的输入（解析并作为实例的属性提供），而指标由策略本身声明和管理。

到目前为止，所有 backtrader 示例图表都绘制了三件看似理所当然的东西，因为它们在任何地方都没有声明：

现金和价值（经纪人中的资金情况）
交易（即操作）
买/卖订单
它们是观察器，存在于子模块 backtrader.observers 中。因为 Cerebro 支持一个参数来自动将它们（或不将它们）添加到策略中：stdstats（默认：True）。

如果遵循默认设置，Cerebro 将执行以下等效用户代码：

import backtrader as bt

cerebro = bt.Cerebro()  # 默认参数：stdstats=True

cerebro.addobserver(bt.observers.Broker)
cerebro.addobserver(bt.observers.Trades)
cerebro.addobserver(bt.observers.BuySell)
让我们看看通常带有这三个默认观察器的图表（即使没有发出订单，因此没有交易发生，现金和投资组合价值没有变化）：

from __future__ import (absolute_import, division, print_function, unicode_literals)
import backtrader as bt
import backtrader.feeds as btfeeds

if __name__ == '__main__':
    cerebro = bt.Cerebro(stdstats=False)
    cerebro.addstrategy(bt.Strategy)

    data = bt.feeds.BacktraderCSVData(dataname='../../datas/2006-day-001.txt')
    cerebro.adddata(data)

    cerebro.run()
    cerebro.plot()
现在让我们在创建 Cerebro 实例时将 stdstats 的值更改为 False（也可以在调用 run 时完成）：

cerebro = bt.Cerebro(stdstats=False)
图表现在有所不同。

访问观察器#
如上所示，观察器在默认情况下已经存在并收集信息，这些信息可用于统计目的，因此可以通过策略的一个名为 stats 的属性访问观察器。

这只是一个占位符。如果我们回顾上面列出的添加一个默认观察器的代码：

cerebro.addobserver(backtrader.observers.Broker)
显而易见的问题是如何访问 Broker 观察器。下面是如何在策略的 next 方法中完成的示例：

class MyStrategy(bt.Strategy):

    def next(self):
        if self.stats.broker.value[0] < 1000.0:
           print('WHITE FLAG ... I LOST TOO MUCH')
        elif self.stats.broker.value[0] > 10000000.0:
           print('TIME FOR THE VIRGIN ISLANDS ....!!!')
Broker 观察器就像数据、指标和策略本身一样也是一个线条对象。在这种情况下，Broker 有两条线：

cash
value
观察器的实现#
实现非常类似于指标：

class Broker(Observer):
    alias = ('CashValue',)
    lines = ('cash', 'value')

    plotinfo = dict(plot=True, subplot=True)

    def next(self):
        self.lines.cash[0] = self._owner.broker.getcash()
        self.lines.value[0] = value = self._owner.broker.getvalue()
步骤：

从 Observer（而不是 Indicator）派生
根据需要声明线条和参数（Broker 有两条线但没有参数）
将有一个自动属性 _owner，即持有观察器的策略
观察器在以下情况下开始运行：

所有指标都已计算完毕
策略的 next 方法已执行完毕
这意味着在周期结束时… 它们观察已发生的情况。在 Broker 的情况下，它只是盲目地记录每个时间点的经纪人现金和投资组合价值。

将观察器添加到策略#
如上所述，Cerebro 使用 stdstats 参数决定是否添加三个默认观察器，从而减轻最终用户的工作负担。

可以将其他观察器添加到混合中，无论是与 stdstats 一起使用还是移除它们。

让我们来看一个通常的策略，当收盘价高于简单移动平均线时买入，相反则卖出。

有一个“添加”：

DrawDown，这是 backtrader 生态系统中已经存在的观察器
from __future__ import (absolute_import, division, print_function, unicode_literals)
import argparse
import datetime
import os.path
import time
import sys
import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicators as btind

class MyStrategy(bt.Strategy):
    params = (('smaperiod', 15),)

    def log(self, txt, dt=None):
        ''' 记录此策略的日志功能 '''
        dt = dt or self.data.datetime[0]
        if isinstance(dt, float):
            dt = bt.num2date(dt)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # 主数据上的简单移动平均线
        sma = btind.SMA(period=self.p.smaperiod)

        # 交叉（1：向上，-1：向下）收盘价/移动平均线
        self.buysell = btind.CrossOver(self.data.close, sma, plot=True)

        # 哨兵为 None：允许新订单
        self.order = None

    def next(self):
        # 访问 -1，因为 drawdown[0] 将在“next”之后计算
        self.log('DrawDown: %.2f' % self.stats.drawdown.drawdown[-1])
        self.log('MaxDrawDown: %.2f' % self.stats.drawdown.maxdrawdown[-1])

        # 检查我们是否在市场中
        if self.position:
            if self.buysell < 0:
                self.log('SELL CREATE, %.2f' % self.data.close[0])
                self.sell()
        elif self.buysell > 0:
            self.log('BUY CREATE, %.2f' % self.data.close[0])
            self.buy()

def runstrat():
    cerebro = bt.Cerebro()

    data = bt.feeds.BacktraderCSVData(dataname='../../datas/2006-day-001.txt')
    cerebro.adddata(data)

    cerebro.addobserver(bt.observers.DrawDown)

    cerebro.addstrategy(MyStrategy)
    cerebro.run()

    cerebro.plot()

if __name__ == '__main__':
    runstrat()
视觉输出显示了回撤的演变：

部分文本输出：

...
2006-12-14T23:59:59+00:00, MaxDrawDown: 2.62
2006-12-15T23:59:59+00:00, DrawDown: 0.22
2006-12-15T23:59:59+00:00, MaxDrawDown: 2.62
2006-12-18T23:59:59+00:00, DrawDown: 0.00
2006-12-18T23:59:59+00:00, MaxDrawDown: 2.62
...
注意

如文本输出和代码所示，DrawDown 观察器实际上有两条线：

drawdown
maxdrawdown
选择不绘制 maxdrawdown 线，但它仍然可供用户使用。

实际上，maxdrawdown 的最后一个值也可以通过一个直接属性（不是线条）获取，名称为 maxdd。

开发观察器#
上面展示了 Broker 观察器的实现。要生成有意义的观察器，实现可以使用以下信息：

self._owner 是当前正在执行的策略
因此策略中的任何内容对观察器都是可用的。

策略中可能有用的默认内部内容：

broker -> 属性，提供对策略创建订单的经纪人实例的访问。正如在 Broker 中所见，通过调用 getcash 和 getvalue 方法收集现金和投资组合价值。
_orderspending -> 列表，策略创建的订单并且经纪人已通知策略一个事件。BuySell 观察器遍历列表，查找已执行的订单（全部或部分），以便为给定时间点创建一个平均执行价格（索引 0）。
_tradespending -> 交易列表（已完成的买/卖或卖/买对），由买/卖订单编译而成。观察器显然可以通过 self._owner.stats 路径访问其他观察器。
自定义 OrderObserver#
标准的 BuySell 观察器只关心已执行的操作。我们可以创建一个观察器，显示订单何时创建以及它们是否过期。

为了可见性，显示将不会与价格一起绘制，而是在一个单独的轴上。

from __future__ import (absolute_import, division, print_function, unicode_literals)
import math
import

 backtrader as bt

class OrderObserver(bt.observer.Observer):
    lines = ('created', 'expired',)

    plotinfo = dict(plot=True, subplot=True, plotlinelabels=True)

    plotlines = dict(
        created=dict(marker='*', markersize=8.0, color='lime', fillstyle='full'),
        expired=dict(marker='s', markersize=8.0, color='red', fillstyle='full')
    )

    def next(self):
        for order in self._owner._orderspending:
            if order.data is not self.data:
                continue

            if not order.isbuy():
                continue

            # 只关心“买入”订单，因为策略中的卖出订单是市场订单并会立即执行

            if order.status in [bt.Order.Accepted, bt.Order.Submitted]:
                self.lines.created[0] = order.created.price

            elif order.status in [bt.Order.Expired]:
                self.lines.expired[0] = order.created.price
自定义观察器只关心买入订单，因为这是一个只买入以尝试获利的策略。卖出订单是市场订单，将立即执行。

更新后的策略#
from __future__ import (absolute_import, division, print_function, unicode_literals)
import datetime
import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicators as btind
from orderobserver import OrderObserver

class MyStrategy(bt.Strategy):
    params = (
        ('smaperiod', 15),
        ('limitperc', 1.0),
        ('valid', 7),
    )

    def log(self, txt, dt=None):
        ''' 记录此策略的日志功能 '''
        dt = dt or self.data.datetime[0]
        if isinstance(dt, float):
            dt = bt.num2date(dt)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # 买入/卖出订单已提交/接受至/由经纪人 - 无需执行任何操作
            self.log('ORDER ACCEPTED/SUBMITTED', dt=order.created.dt)
            self.order = order
            return

        if order.status in [order.Expired]:
            self.log('BUY EXPIRED')

        elif order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))
            else:  # 卖出
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

        # 哨兵为 None：允许新订单
        self.order = None

    def __init__(self):
        # 主数据上的简单移动平均线
        sma = btind.SMA(period=self.p.smaperiod)

        # 交叉（1：向上，-1：向下）收盘价/移动平均线
        self.buysell = btind.CrossOver(self.data.close, sma, plot=True)

        # 哨兵为 None：允许新订单
        self.order = None

    def next(self):
        if self.order:
            # 待处理订单...不做任何事
            return

        # 检查我们是否在市场中
        if self.position:
            if self.buysell < 0:
                self.log('SELL CREATE, %.2f' % self.data.close[0])
                self.sell()
        elif self.buysell > 0:
            plimit = self.data.close[0] * (1.0 - self.p.limitperc / 100.0)
            valid = self.data.datetime.date(0) + datetime.timedelta(days=self.p.valid)
            self.log('BUY CREATE, %.2f' % plimit)
            self.buy(exectype=bt.Order.Limit, price=plimit, valid=valid)

def runstrat():
    cerebro = bt.Cerebro()

    data = bt.feeds.BacktraderCSVData(dataname='../../datas/2006-day-001.txt')
    cerebro.adddata(data)

    cerebro.addobserver(OrderObserver)

    cerebro.addstrategy(MyStrategy)
    cerebro.run()

    cerebro.plot()

if __name__ == '__main__':
    runstrat()
结果图表显示多个订单已过期，可以在新子图（红色方块）中看到。此外，我们还可以看到“创建”和“执行”之间的几个天数。

保存/保持统计数据#
截至目前，backtrader 尚未实现任何机制来跟踪观察器的值并将其存储到文件中。最好的方法是：

在策略的 start 方法中打开一个文件
在策略的 next 方法中写下值
考虑 DrawDown 观察器，可以这样做：

class MyStrategy(bt.Strategy):

    def start(self):
        self.mystats = open('mystats.csv', 'wb')
        self.mystats.write('datetime,drawdown, maxdrawdown\n')

    def next(self):
        self.mystats.write(self.data.datetime.date(0).strftime('%Y-%m-%d'))
        self.mystats.write(',%.2f' % self.stats.drawdown.drawdown[-1])
        self.mystats.write(',%.2f' % self.stats.drawdown.maxdrawdown[-1])
        self.mystats.write('\n')
要保存索引 0 的值，一旦所有观察器都被处理完，可以将自定义观察器作为系统的最后一个观察器添加，以将值写入 CSV 文件。

注意，Writer 功能可以自动执行此任务。

Previous
Reference
#########################################################################################################################################
基准测试#
Ticket #89 是关于添加基准测试以对比一个资产的表现。这个功能非常实用，因为有些策略即使盈利也可能低于单纯追踪资产的收益。

backtrader 包含两种不同类型的对象可以帮助进行追踪：

观察器
分析器
在分析器领域，已经有一个 TimeReturn 对象，用于跟踪整个投资组合价值的回报演变（包括现金）。

这显然也可以是一个观察器，所以在添加一些基准测试时，也对如何将观察器和分析器组合在一起进行了工作，这两者旨在跟踪相同的内容。

注意

观察器和分析器之间的主要区别在于观察器的线条特性，观察器记录每个值，这使得它们适合绘图和实时查询。当然，这会消耗内存。

另一方面，分析器通过 get_analysis 返回一组结果，并且实现可能直到运行结束时才会提供任何结果。

分析器 - 基准测试#
标准的 TimeReturn 分析器已扩展为支持跟踪数据源。涉及的两个主要参数：

timeframe（默认：无） 如果为 None，将报告整个回测期间的总回报。
data（默认：无） 要跟踪的参考资产，而不是投资组合价值。
注意

此数据必须已通过 adddata、resampledata 或 replaydata 添加到 cerebro 实例中。

更多详细信息和参数请参阅：分析器参考。

因此，可以像这样按年度跟踪投资组合的回报：

import backtrader as bt

cerebro = bt.Cerebro()
cerebro.addanalyzer(bt.analyzers.TimeReturn, timeframe=bt.TimeFrame.Years)

# 添加数据、策略等...

results = cerebro.run()
strat0 = results[0]

# 如果没有指定名称，则名称为类名的小写形式
tret_analyzer = strat0.analyzers.getbyname('timereturn')
print(tret_analyzer.get_analysis())
如果我们想跟踪一个数据的回报：

import backtrader as bt

cerebro = bt.Cerebro()

data = bt.feeds.OneOfTheFeeds(dataname='abcde', ...)
cerebro.adddata(data)

cerebro.addanalyzer(bt.analyzers.TimeReturn, timeframe=bt.TimeFrame.Years, data=data)

# 添加策略等...

results = cerebro.run()
strat0 = results[0]

# 如果没有指定名称，则名称为类名的小写形式
tret_analyzer = strat0.analyzers.getbyname('timereturn')
print(tret_analyzer.get_analysis())
如果要同时跟踪两者，最好为分析器指定名称：

import backtrader as bt

cerebro = bt.Cerebro()

data = bt.feeds.OneOfTheFeeds(dataname='abcde', ...)
cerebro.adddata(data)

cerebro.addanalyzer(bt.analyzers.TimeReturn, timeframe=bt.TimeFrame.Years, data=data, _name='datareturns')

cerebro.addanalyzer(bt.analyzers.TimeReturn, timeframe=bt.TimeFrame.Years, _name='timereturns')

# 添加策略等...

results = cerebro.run()
strat0 = results[0]

# 获取分析结果
tret_analyzer = strat0.analyzers.getbyname('timereturns')
print(tret_analyzer.get_analysis())
tdata_analyzer = strat0.analyzers.getbyname('datareturns')
print(tdata_analyzer.get_analysis())
观察器 - 基准测试#
感谢能够在观察器中使用分析器的底层机制，添加了两个新观察器：

TimeReturn
Benchmark
两者都使用 bt.analyzers.TimeReturn 分析器来收集结果。

与上述代码片段相比，以下是一个完整的示例，以展示它们的功能。

观察 TimeReturn#
执行：

$ ./observer-benchmark.py --plot --timereturn --timeframe notimeframe
注意执行选项：

--timereturn 告诉示例仅执行此操作。
--timeframe notimeframe 告诉分析器考虑整个数据集而不考虑时间框架边界。
最后绘制的值是 -0.26。

起始现金（从图表中显而易见）为 50K 货币单位，策略最终以 36,970 货币单位收尾，因此价值减少了 -26%。

观察基准测试#
因为基准测试还会显示 timereturn 结果，让我们在激活基准测试的情况下运行相同的操作：

$ ./observer-benchmark.py --plot --timeframe notimeframe
结果显示：

策略表现优于资产：-0.26 对 -0.33

这不应该是庆祝的理由，但至少很清楚策略并不比资产差。

按年度跟踪的情况：

$ ./observer-benchmark.py --plot --timeframe years
注意：

策略的最后一个值略有变化，从 -0.26 变为 -0.27

而资产的最后一个值则显示为 -0.35（相对于上面的 -0.33）

原因是在从 2005 年到 2006 年的过渡中，策略和基准资产在 2005 年初几乎处于起始水平。

切换到周时间框架时，整个图像发生了变化：

$ ./observer-benchmark.py --plot --timeframe weeks
现在：

基准观察器显示出更加紧张的情况。事物上下波动，因为现在正在跟踪投资组合和数据的每周回报。

由于在年底的最后一周没有进行任何交易，且资产几乎没有移动，最后显示的值为 0.00（最后一周之前的最后收盘价为 25.54，而样本数据收盘于 25.55，差异首先在小数点后第四位显现）。

观察基准测试 - 另一个数据#
示例允许对比不同的数据。默认情况下使用 --benchdata1 基准对比 Oracle。考虑整个数据集时使用 --timeframe notimeframe：

$ ./observer-benchmark.py --plot --timeframe notimeframe --benchdata1
结果显示：

策略的结果未随 notimeframe 变化，仍为 -26%（-0.26）

但当与另一个数据进行基准对比时，该数据在同一期间内有 +23%（0.23） 的增长

要么需要更改策略，要么需要交易另一个更好的资产。

结论#
现在有两种方式，使用相同的底层代码/计算，来跟踪 TimeReturn 和 Benchmark：

观察器（TimeReturn 和 Benchmark）
分析器（TimeReturn 和带有 data 参数的 TimeReturn）
当然，基准测试并不保证利润，只是比较。

示例代码#
$ ./observer-benchmark.py --help
usage: observer-benchmark.py [-h] [--data0 DATA0] [--data1 DATA1]
                             [--benchdata1] [--fromdate FROMDATE]
                             [--todate TODATE] [--printout] [--cash CASH]
                             [--period PERIOD] [--stake STAKE] [--timereturn]
                             [--timeframe {months,days,notimeframe,years,None,weeks}]
                             [--plot [kwargs]]

Benchmark/TimeReturn Observers Sample

optional arguments:
  -h, --help            show this help message and exit
  --data0 DATA0         Data0 to be read in (default:
                        ../../datas/yhoo-1996-2015.txt)
  --data1 DATA1         Data1 to be read in (default:
                        ../../datas/orcl-1995-2014.txt)
  --benchdata1          Benchmark against data1 (default: False)
  --fromdate FROMDATE   Starting date in YYYY-MM-DD format (default:
                        2005-01-01)
  --todate TODATE       Ending date in YYYY-MM-DD format (default: 2006-12-31)
  --printout            Print data lines (default: False)
  --cash CASH           Cash to start with (default: 50000)
  --period PERIOD       Period for the crossover moving average (default: 30)
  --stake STAKE         Stake to apply for the buy operations (default: 1000)
  --timereturn          Use TimeReturn observer instead of Benchmark (default:
                        None)
  --timeframe {months,days,notimeframe,years,None,weeks}
                        TimeFrame to apply to the Observer (default: None)
  --plot [kwargs], -p [kwargs]
                        Plot the read data applying any kwargs passed For
                        example: --plot style="candle" (to plot candles)
                        (default: None)
示例代码：

from __future__ import (absolute_import, division, print_function, unicode_literals)
import argparse
import datetime
import random
import backtrader as bt

class St(bt.Strategy):
    params = (
        ('period', 

10),
        ('printout', False),
        ('stake', 1000),
    )

    def __init__(self):
        sma = bt.indicators.SMA(self.data, period=self.p.period)
        self.crossover = bt.indicators.CrossOver(self.data, sma)

    def start(self):
        if self.p.printout:
            txtfields = list()
            txtfields.append('Len')
            txtfields.append('Datetime')
            txtfields.append('Open')
            txtfields.append('High')
            txtfields.append('Low')
            txtfields.append('Close')
            txtfields.append('Volume')
            txtfields.append('OpenInterest')
            print(','.join(txtfields))

    def next(self):
        if self.p.printout:
            # 仅打印第一个数据... 只是检查运行情况
            txtfields = list()
            txtfields.append('%04d' % len(self))
            txtfields.append(self.data.datetime.datetime(0).isoformat())
            txtfields.append('%.2f' % self.data0.open[0])
            txtfields.append('%.2f' % self.data0.high[0])
            txtfields.append('%.2f' % self.data0.low[0])
            txtfields.append('%.2f' % self.data0.close[0])
            txtfields.append('%.2f' % self.data0.volume[0])
            txtfields.append('%.2f' % self.data0.openinterest[0])
            print(','.join(txtfields))

        if self.position:
            if self.crossover < 0.0:
                if self.p.printout:
                    print('CLOSE {} @%{}'.format(self.p.stake, self.data.close[0]))
                self.close()

        else:
            if self.crossover > 0.0:
                self.buy(size=self.p.stake)
                if self.p.printout:
                    print('BUY   {} @%{}'.format(self.p.stake, self.data.close[0]))

TIMEFRAMES = {
    None: None,
    'days': bt.TimeFrame.Days,
    'weeks': bt.TimeFrame.Weeks,
    'months': bt.TimeFrame.Months,
    'years': bt.TimeFrame.Years,
    'notimeframe': bt.TimeFrame.NoTimeFrame,
}

def runstrat(args=None):
    args = parse_args(args)

    cerebro = bt.Cerebro()
    cerebro.broker.set_cash(args.cash)

    dkwargs = dict()
    if args.fromdate:
        fromdate = datetime.datetime.strptime(args.fromdate, '%Y-%m-%d')
        dkwargs['fromdate'] = fromdate

    if args.todate:
        todate = datetime.datetime.strptime(args.todate, '%Y-%m-%d')
        dkwargs['todate'] = todate

    data0 = bt.feeds.YahooFinanceCSVData(dataname=args.data0, **dkwargs)
    cerebro.adddata(data0, name='Data0')

    cerebro.addstrategy(St, period=args.period, stake=args.stake, printout=args.printout)

    if args.timereturn:
        cerebro.addobserver(bt.observers.TimeReturn, timeframe=TIMEFRAMES[args.timeframe])
    else:
        benchdata = data0
        if args.benchdata1:
            data1 = bt.feeds.YahooFinanceCSVData(dataname=args.data1, **dkwargs)
            cerebro.adddata(data1, name='Data1')
            benchdata = data1

        cerebro.addobserver(bt.observers.Benchmark, data=benchdata, timeframe=TIMEFRAMES[args.timeframe])

    cerebro.run()

    if args.plot:
        pkwargs = dict()
        if args.plot is not True:  # 评估为 True 但不是 True
            pkwargs = eval('dict(' + args.plot + ')')  # 传递的参数

        cerebro.plot(**pkwargs)

def parse_args(pargs=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Benchmark/TimeReturn Observers Sample')

    parser.add_argument('--data0', required=False, default='../../datas/yhoo-1996-2015.txt', help='Data0 to be read in')

    parser.add_argument('--data1', required=False, default='../../datas/orcl-1995-2014.txt', help='Data1 to be read in')

    parser.add_argument('--benchdata1', required=False, action='store_true', help=('Benchmark against data1'))

    parser.add_argument('--fromdate', required=False, default='2005-01-01', help='Starting date in YYYY-MM-DD format')

    parser.add_argument('--todate', required=False, default='2006-12-31', help='Ending date in YYYY-MM-DD format')

    parser.add_argument('--printout', required=False, action='store_true', help=('Print data lines'))

    parser.add_argument('--cash', required=False, action='store', type=float, default=50000, help=('Cash to start with'))

    parser.add_argument('--period', required=False, action='store', type=int, default=30, help=('Period for the crossover moving average'))

    parser.add_argument('--stake', required=False, action='store', type=int, default=1000, help=('Stake to apply for the buy operations'))

    parser.add_argument('--timereturn', required=False, action='store_true', default=None, help=('Use TimeReturn observer instead of Benchmark'))

    parser.add_argument('--timeframe', required=False, action='store', default=None, choices=TIMEFRAMES.keys(), help=('TimeFrame to apply to the Observer'))

    parser.add_argument('--plot', '-p', nargs='?', required=False, metavar='kwargs', const=True, help=('Plot the read data applying any kwargs passed\nFor example:\n\n  --plot style="candle" (to plot candles)\n'))

    if pargs:
        return parser.parse_args(pargs)

    return parser.parse_args()

if __name__ == '__main__':
    runstrat()
#######################################################################################################################################
参考#
Benchmark#
class backtrader.observers.Benchmark()
该观察器存储策略的回报和作为参考资产的回报，这个参考资产是传递给系统的一个数据。

参数：

timeframe（默认：无）：如果为 None，则报告整个回测期间的总回报。
compression（默认：无）：仅用于子日时间框架，例如通过指定 “TimeFrame.Minutes” 和 60 作为压缩在每小时时间框架上工作。
data（默认：无）：跟踪的参考资产以便进行比较。
注意：此数据必须已通过 adddata、resampledata 或 replaydata 添加到 cerebro 实例中。

_doprenext（默认：False）：基准测试将在策略开始运行时进行（即策略的最小周期已达到时）。将其设置为 True 将从数据源的起点记录基准值。
firstopen（默认：False）：保持为 False 确保价值和基准之间的首次比较点从 0% 开始，因为基准不会使用其开盘价。参见 TimeReturn 分析器参考以获得参数的完整解释。
fund（默认：无）：如果为 None，将自动检测经纪人的实际模式（fundmode - True/False）来决定回报率是基于总净资产价值还是基金价值。见经纪人文档中的 set_fundmode。设置为 True 或 False 以获得特定行为。
记住，在运行的任何时刻都可以通过查看索引 0 处的线条名称来检查当前值。

Broker#
class backtrader.observers.Broker(*args, **kwargs)
该观察器跟踪经纪人中的当前现金金额和投资组合价值（包括现金）。

参数：无

Broker - Cash#
class backtrader.observers.Cash(*args, **kwargs)
该观察器跟踪经纪人中的当前现金金额。

参数：无

Broker - Value#
class backtrader.observers.Value(*args, **kwargs)
该观察器跟踪经纪人中的当前投资组合价值，包括现金。

参数：

fund（默认：无）：如果为 None，将自动检测经纪人的实际模式（fundmode - True/False）来决定回报率是基于总净资产价值还是基金价值。见经纪人文档中的 set_fundmode。设置为 True 或 False 以获得特定行为。
BuySell#
class backtrader.observers.BuySell(*args, **kwargs)
该观察器跟踪单个买入/卖出订单（单个执行）并将在图表上绘制它们，围绕执行价格水平绘制。

参数：

barplot（默认：False）：在最低点下方绘制买入信号，在最高点上方绘制卖出信号。如果为 False，则将在条形的平均执行价格上绘制。
bardist（默认：0.015 1.5%）：当 barplot 为 True 时，与最大值/最小值的距离。
DrawDown#
class backtrader.observers.DrawDown()
该观察器跟踪当前的回撤水平（绘图）和最大回撤（不绘图）水平。

参数：

fund（默认：无）：如果为 None，将自动检测经纪人的实际模式（fundmode - True/False）来决定回报率是基于总净资产价值还是基金价值。见经纪人文档中的 set_fundmode。设置为 True 或 False 以获得特定行为。
TimeReturn#
class backtrader.observers.TimeReturn()
该观察器存储策略的回报。

参数：

timeframe（默认：无）：如果为 None，则报告整个回测期间的总回报。传递 TimeFrame.NoTimeFrame 以考虑整个数据集而不受时间限制。
compression（默认：无）：仅用于子日时间框架，例如通过指定 “TimeFrame.Minutes” 和 60 作为压缩在每小时时间框架上工作。
fund（默认：无）：如果为 None，将自动检测经纪人的实际模式（fundmode - True/False）来决定回报率是基于总净资产价值还是基金价值。见经纪人文档中的 set_fundmode。设置为 True 或 False 以获得特定行为。
记住，在运行的任何时刻都可以通过查看索引 0 处的线条名称来检查当前值。

Trades#
class backtrader.observers.Trades()
该观察器跟踪完整的交易，并在交易关闭时绘制实现的损益水平。

交易在仓位从 0（或跨越 0）变为 X 时开立，然后在回到 0（或反方向跨越 0）时关闭。

参数：

pnlcomm（默认：True）：显示净利润和亏损，即扣除佣金后的结果。如果设置为 False，将显示扣除佣金前的交易结果。
LogReturns#
class backtrader.observers.LogReturns()
该观察器存储策略的对数回报。

参数：

timeframe（默认：无）：如果为 None，则报告整个回测期间的总回报。传递 TimeFrame.NoTimeFrame 以考虑整个数据集而不受时间限制。
compression（默认：无）：仅用于子日时间框架，例如通过指定 “TimeFrame.Minutes” 和 60 作为压缩在每小时时间框架上工作。
fund（默认：无）：如果为 None，将自动检测经纪人的实际模式（fundmode - True/False）来决定回报率是基于总净资产价值还是基金价值。见经纪人文档中的 set_fundmode。设置为 True 或 False 以获得特定行为。
记住，在运行的任何时刻都可以通过查看索引 0 处的线条名称来检查当前值。

LogReturns2#
class backtrader.observers.LogReturns2()
扩展 LogReturns 观察器以显示两个工具。

FundValue#
class backtrader.observers.FundValue(*args, **kwargs)
该观察器跟踪当前的基金价值。

参数：无

FundShares#
class backtrader.observers.FundShares(*args, **kwargs)
该观察器跟踪当前的基金份额。

参数：无


33 43Sizers.txt ##################################################
文件路径: 43Sizers.txt
================================================================================

Sizers#
策略提供交易方法，即：buy、sell 和 close。让我们看看 buy 的签名：

def buy(self, data=None, size=None, price=None, plimit=None, exectype=None, valid=None, tradeid=0, **kwargs):
注意，如果调用者没有指定 size，则 size 的默认值为 None。这就是 Sizers 发挥重要作用的地方：

size=None 请求策略向其 Sizer 询问实际的头寸大小
这显然意味着策略有一个 Sizer：是的，确实如此！如果用户没有添加 Sizer，后台机制会为策略添加一个默认的 Sizer。添加到策略中的默认 Sizer 是 SizerFix。定义的初始行：

class SizerFix(SizerBase):
    params = (('stake', 1),)
很容易猜到这个 Sizer 只是使用 1 个单位（无论是股票、合约等）买卖。

使用 Sizers#
从 Cerebro#
Sizers 可以通过 Cerebro 以两种不同的方法添加：

addsizer(sizercls, *args, **kwargs)：添加一个 Sizer，将应用于添加到 cerebro 的任何策略。这就是所谓的默认 Sizer。例如：
cerebro = bt.Cerebro()
cerebro.addsizer(bt.sizers.SizerFix, stake=20)  # 默认策略的 Sizer
addsizer_byidx(idx, sizercls, *args, **kwargs)：只将 Sizer 添加到 idx 引用的策略中。
这个 idx 可以作为 addstrategy 的返回值获得。例如：

cerebro = bt.Cerebro()
cerebro.addsizer(bt.sizers.SizerFix, stake=20)  # 默认策略的 Sizer

idx = cerebro.addstrategy(MyStrategy, myparam=myvalue)
cerebro.addsizer_byidx(idx, bt.sizers.SizerFix, stake=5)

cerebro.addstrategy(MyOtherStrategy)
在这个例子中：

系统添加了一个默认的 Sizer。这适用于所有没有分配特定 Sizer 的策略。
对于 MyStrategy，在收集其插入 idx 后，添加了一个特定的 Sizer（更改 stake 参数）。
系统添加了第二个策略 MyOtherStrategy。没有为其添加特定的 Sizer。
这意味着：

MyStrategy 最终会有一个内部特定的 Sizer。
MyOtherStrategy 将获得默认的 Sizer。
注意：默认并不意味着策略共享单个 Sizer 实例。每个策略都接收不同的默认 Sizer 实例。要共享单个实例，共享的 Sizer 应该是一个单例类。如何定义一个超出了 backtrader 的范围。

从策略#
Strategy 类提供了一个 API：setsizer 和 getsizer（以及一个属性 sizer）来管理 Sizer。签名：

def setsizer(self, sizer): 它接受一个已经实例化的 Sizer def getsizer(self): 返回当前的 Sizer 实例，sizer 是可以直接获取/设置的属性

在这种情况下，Sizer 可以例如：

作为参数传递给策略
在 __init__ 中使用属性 sizer 或 setsizer 设置，例如：
class MyStrategy(bt.Strategy):
    params = (('sizer', None),)

    def __init__(self):
        if self.p.sizer is not None:
            self.sizer = self.p.sizer
这将允许在与 cerebro 调用相同级别创建一个 Sizer，并将其作为参数传递给系统中的所有策略，从而有效地共享一个 Sizer。

Sizer 开发#
开发一个 Sizer 很容易：

从 backtrader.Sizer 子类化。
这使您可以访问 self.strategy 和 self.broker，尽管在大多数情况下不需要。可以通过经纪人访问的内容：

数据的头寸，通过 self.strategy.getposition(data)
完整的投资组合价值，通过 self.broker.getvalue()
注意，这当然也可以通过 self.strategy.broker.getvalue() 来完成。

重写方法 _getsizing(self, comminfo, cash, data, isbuy)。
参数：

comminfo：包含数据佣金信息的 CommissionInfo 实例，并允许计算头寸价值、操作成本和操作佣金。
cash：经纪人的当前可用现金。
data：操作的目标。
isbuy：对于买入操作为 True，对于卖出操作为 False。
此方法返回买入/卖出操作的期望大小。

返回的符号无关紧要，例如：如果操作是卖出操作（isbuy 为 False），方法可以返回 5 或 -5。卖出操作只会使用绝对值。

Sizer 已经去经纪人那里请求了给定数据的佣金信息、实际现金水平，并提供了操作目标数据的直接引用。

让我们定义 FixedSize Sizer：

import backtrader as bt

class FixedSize(bt.Sizer):
    params = (('stake', 1),)

    def _getsizing(self, comminfo, cash, data, isbuy):
        return self.params.stake
这非常简单，因为 Sizer 不进行计算，参数只是存在。

但是该机制应该允许构建复杂的头寸系统来管理进入/退出市场时的头寸。

另一个例子：一个头寸反转器：

class FixedReverser(bt.FixedSize):

    def _getsizing(self, comminfo, cash, data, isbuy):
        position = self.broker.getposition(data)
        size = self.p.stake * (1 + (position.size != 0))
        return size
这个 Sizer 继承了 FixedSize，覆盖了 _getsizing：

通过 broker 属性获取数据的头寸。
使用 position.size 决定是否加倍固定头寸。
返回计算的值。
这将解除策略决定是否反转头寸或开仓的负担，Sizer 负责控制，可以随时替换而不影响逻辑。

实用 Sizer 应用#
不考虑复杂的头寸算法，可以使用两种不同的 Sizers 将策略从仅做多转换为多空策略。只需在 cerebro 执行中更改 Sizer，策略的行为将发生变化。一个非常简单的收盘价交叉 SMA 算法：

class CloseSMA(bt.Strategy):
    params = (('period', 15),)

    def __init__(self):
        sma = bt.indicators.SMA(self.data, period=self.p.period)
        self.crossover = bt.indicators.CrossOver(self.data, sma)

    def next(self):
        if self.crossover > 0:
            self.buy()
        elif self.crossover < 0:
            self.sell()
注意策略并没有考虑当前头寸（通过查看 self.position）来决定是否实际执行买入或卖出操作。只有交叉信号被考虑。Sizer 将负责所有事务。

这个 Sizer 仅在卖出时返回非零头寸大小（如果已有头寸）：

class LongOnly(bt.Sizer):
    params = (('stake', 1),)

    def _getsizing(self, comminfo, cash, data, isbuy):
      if isbuy:
          return self.p.stake

      # 卖出情况
      position = self.broker.getposition(data)
      if not position.size:
          return 0  # 如果没有持仓则不卖出

      return self.p.stake
将所有内容放在一起（假设已经导入 backtrader 并向系统添加了数据）：

cerebro.addstrategy(CloseSMA)
cerebro.addsizer(LongOnly)
cerebro.run()
图表（来自源代码中的示例以测试这一点）。

LongOnly

多空版本只需将 Sizer 更改为上面显示的 FixedReverser：

cerebro.addstrategy(CloseSMA)
cerebro.addsizer(FixedReverser)
cerebro.run()
输出图表。

FixedReverser

注意差异：

交易次数翻倍。
现金水平从未恢复到初始值，因为策略始终在市场中。
两种方法都负面，但这只是一个示例。

bt.Sizer 参考#
class backtrader.Sizer()
这是 Sizers 的基类。任何 Sizer 都应继承此类并覆盖 _getsizing 方法。

成员属性：

strategy：由 Sizer 所在的策略设置。可以访问策略的整个 API，例如如果需要获取实际数据头寸：
position = self.strategy.getposition(data)
broker：由 Sizer 所在的策略设置。可以访问一些
复杂 Sizers 可能需要的信息，例如投资组合价值等。

def _getsizing(comminfo, cash, data, isbuy)
此方法必须由 Sizer 的子类覆盖以提供大小功能。

参数：

comminfo：包含数据佣金信息的 CommissionInfo 实例，并允许计算头寸价值、操作成本和操作佣金。
cash：经纪人的当前可用现金。
data：操作的目标。
isbuy：对于买入操作为 True，对于卖出操作为 False。
此方法必须返回要执行的实际大小（一个整数）。如果返回 0，则不会执行任何操作。

返回值的绝对值将被使用。

############################################################################################################
参考#
FixedSize#
class backtrader.sizers.FixedSize()
此 Sizer 仅为任何操作返回固定大小。通过指定 tranches 参数，可以控制系统希望用于逐步进入交易的批次数量。

参数：

stake（默认：1）
tranches（默认：1）
FixedReverser#
class backtrader.sizers.FixedReverser()
此 Sizer 返回反转已开头寸所需的固定大小或开仓所需的固定大小。

开仓：返回参数 stake
反转头寸：返回 2 * stake
参数：

stake（默认：1）
PercentSizer#
class backtrader.sizers.PercentSizer()
此 Sizer 返回可用现金的百分比。

参数：

percents（默认：20）
AllInSizer#
class backtrader.sizers.AllInSizer()
此 Sizer 返回经纪人所有可用现金。

参数：

percents（默认：100）
PercentSizerInt#
class backtrader.sizers.PercentSizerInt()
此 Sizer 以整数形式返回可用现金的百分比，并将大小截断为整数。

参数：

percents（默认：20）
AllInSizerInt#
class backtrader.sizers.AllInSizerInt()
此 Sizer 返回经纪人所有可用现金，并将大小截断为整数。

参数：

percents（默认：100）
Previous
sizers

34 44实盘.txt ##################################################
文件路径: 44实盘.txt
================================================================================

盈透（Interactive Brokers）#
与盈透（Interactive Brokers）的集成支持以下功能：

实时数据馈送
实时交易
注意：尽管已经尽力测试了尽可能多的错误条件和情况，但代码（像任何其他软件一样）可能包含错误。在进入生产环境之前，请使用纸面交易账户或 TWS 演示帐户彻底测试任何策略。

注意：与互动经纪商的交互是通过使用 IbPy 模块进行的，该模块在使用前必须安装。目前在 Pypi 中没有该模块的包（撰写本文时），但可以使用以下命令通过 pip 安装：

pip install git+https://github.com/blampe/IbPy.git
如果您的系统中没有 git（例如在 Windows 上安装），以下命令也可以正常工作：

pip install https://github.com/blampe/IbPy/archive/master.zip
示例代码#
源码包含一个完整的示例，位于：

samples/ibtest/ibtest.py

该示例无法涵盖所有可能的用例，但它试图提供广泛的见解，并应强调在使用回测模块或实时数据模块时没有实际差异。

需要注意的一点是：

示例在任何交易活动开始之前，都会等待 data.LIVE 数据状态通知。这可能是任何实时策略中都需要考虑的事项。

存储模型与直接模型#
与互动经纪商的交互支持两种模型：

存储模型（推荐）
直接与数据馈送类和经纪商类交互
存储模型提供了一种明确的分离模式，用于创建经纪商和数据。以下两个代码片段应更好地作为示例。

首先是存储模型：

import backtrader as bt

ibstore = bt.stores.IBStore(host='127.0.0.1', port=7496, clientId=35)
data = ibstore.getdata(dataname='EUR.USD-CASH-IDEALPRO')
这里的参数：

host，port 和 clientId 传递到 IBStore 中，用于打开连接。
然后使用 getdata 创建数据馈送，并使用 backtrader 中所有数据馈送中常见的参数 dataname 请求 EUR/USD 外汇对。
直接使用模型：

import backtrader as bt

data = bt.feeds.IBData(dataname='EUR.USD-CASH-IDEALPRO',
                       host='127.0.0.1', port=7496, clientId=35)
在这里：

参数直接传递给数据。这些将用于在后台创建 IBStore 实例。
缺点是：

清晰度较低，因为不清楚哪些属于数据，哪些属于存储。
IBStore - 存储#
存储是实时数据馈送/交易支持的关键，提供了 IbPy 模块和数据馈送及经纪代理需求之间的适配层。

存储是一个涵盖以下功能的概念：

作为一个实体的中央商店：在这种情况下，实体是 IB，可以需要或不需要参数。
提供访问获取经纪实例的方法：
IBStore.getbroker(*args, **kwargs)
提供访问获取数据馈送实例的方法：
IBStore.getdata(*args, **kwargs)
在这种情况下，许多 **kwargs 是数据馈送中常见的，如 dataname，fromdate，todate，sessionstart，sessionend，timeframe，compression。

数据可能会提供其他参数。请检查下面的参考。

IBStore 提供：

连接目标（host 和 port 参数）
身份识别（clientId 参数）
重新连接控制（reconnect 和 timeout 参数）
时间偏移检查（timeoffset 参数，见下文）
通知和调试
notifyall (default: False): 在这种情况下，IB 发送的任何错误信息（许多只是信息性）将被转发到 Cerebro/Strategy。
_debug (default: False): 在这种情况下，TWS 接收到的每条消息都将打印到标准输出。
IBData 数据馈送#
数据选项#
无论是直接还是通过 getdata，IBData 数据馈送都支持以下数据选项：

历史下载请求

如果持续时间超过 IB 为给定时间框架/压缩组合设置的限制，这些请求将被拆分为多个请求。

实时数据有三种口味

tickPrice 事件（通过 IB reqMktData）

用于 CASH 产品（根据至少 TWS API 9.70 的实验，其他类型不支持）

通过查看 BID 价格接收 tick 价格事件，根据非官方互联网文献，这似乎是跟踪 CASH 市场价格的方式。

时间戳在系统中本地生成。如果最终用户希望，可以使用与 IB 服务器时间的偏移（从 IB reqCurrentTime 计算）。

tickString 事件（即 RTVolume（通过 IB reqMktData）

从 IB 大约每 250 毫秒接收一次 OHLC/成交量快照（如果没有交易发生，则更长时间）。

RealTimeBars 事件（通过 IB reqRealTimeBars）

每 5 秒接收一次历史 5 秒的条形图（由 IB 固定的持续时间）。

如果选择的时间框架/组合低于 Seconds/5 级别，此功能将自动禁用。

注意：RealTimeBars 不适用于 TWS 演示。

默认行为是在大多数情况下使用：tickString，除非用户特别希望使用 RealTimeBars。

回填

除非用户请求只进行历史下载，否则数据馈送将自动回填：

启动时：最大可能持续时间。例如，对于 Days/1（时间框架/压缩）组合，IB 的默认最大持续时间为 1 年，这是将被回填的时间量。

数据断开连接后：在这种情况下，通过查看断开连接前接收的最新数据，回填操作下载的数据量将减少到最小。

注意：请考虑最终时间框架/压缩组合可能不是在创建数据馈送时指定的，而是在系统中插入时指定的。请看以下示例：

data = ibstore.getdata(dataname='EUR.USD-CASH-IDEALPRO',
                       timeframe=bt.TimeFrame.Seconds, compression=5)

cerebro.resampledata(data, timeframe=bt.TimeFrame.Minutes, compression=2)
现在应该清楚，最终考虑的时间框架/压缩组合是 Minutes/2。

数据合约检查#
在启动阶段，数据馈送将尝试下载指定合约的详细信息（请参阅参考，了解如何指定）。如果未找到合约或找到多个匹配项，数据将拒绝继续并将通知系统。一些示例。

简单但明确的合约规格：

data = ibstore.getdata(dataname='TWTR')  # 推特
由于默认类型 STK，交易所 SMART 和货币（默认无），将找到一个在 USD 中交易的单一合约（2016-06）。

类似的方式对 AAPL 会失败：

data = ibstore.getdata(dataname='AAPL')  # 错误 -> 多个合约
因为 SMART 找到在多个实际交易所中的合约，且 AAPL 在其中一些以不同货币交易。以下是可以的：

data = ibstore.getdata(dataname='AAPL-STK-SMART-USD')  # 找到1个合约
数据通知#
数据馈送将通过以下一种或多种方式报告当前状态（请检查 Cerebro 和 Strategy 参考）：

Cerebro.notify_data（如果覆盖）
使用 Cerebro.adddatacb 添加的回调
Strategy.notify_data（如果覆盖）
策略中的示例如下：

class IBStrategy(bt.Strategy):

    def notify_data(self, data, status, *args, **kwargs):
        if status == data.LIVE:  # 数据已切换为实时数据
           # 执行某些操作
           pass
在系统中发生变化时，将发送以下通知：

CONNECTED：在成功初始连接时发送
DISCONNECTED：在这种情况下，无法再检索数据，数据将向系统指示无法执行任何操作。可能的条件包括：
指定的合约错误
历史下载中断
超过与 TWS 的重连次数
CONNBROKEN：与 TWS 或数据农场的连接已丢失。数据馈送将尝试（通过存储）重新连接并在需要时回填，并恢复操作。
NOTSUBSCRIBED：合约和连接正常，但由于缺乏权限无法检索数据。数据将向系统指示无法检索
数据。

DELAYED：表示历史/回填操作正在进行中，策略处理的数据不是实时数据。
LIVE：表示策略从这一点开始处理的数据是实时数据。
策略开发人员应考虑在发生断开连接或接收到延迟数据时应采取哪些措施。

数据时间框架和压缩#
backtrader 生态系统中的数据馈送在创建期间支持 timeframe 和 compression 参数。这些参数也可以作为属性访问，使用 data._timeframe 和 data._compression。

时间框架/压缩组合的意义在于将数据传递给 cerebro 实例，通过 resampledata 或 replaydata 让内部重采样器/重放器对象了解目标是什么。 _timeframe 和 _compression 将在重采样/重放期间在数据中被覆盖。

但在实时数据馈送中，这些信息可能起重要作用。请看以下示例：

data = ibstore.getdata(dataname='EUR.USD-CASH-IDEALPRO',
                       timeframe=bt.TimeFrame.Ticks,
                       compression=1,  # 1 是默认值
                       rtbar=True,  # 使用实时条
                      )
cerebro.adddata(data)
用户请求 tick 数据，这很重要，因为：

不会进行回填（IB 支持的最小单位是 Seconds/1）
即使请求和支持实时条，如果时间分辨率低于 Seconds/5，也不会使用它们。
除非以 Ticks/1 分辨率工作，否则数据必须重采样/重放。以下是使用实时条的例子：

data = ibstore.getdata(dataname='TWTR-STK-SMART', rtbar=True)
cerebro.resampledata(data, timeframe=bt.TimeFrame.Seconds, compression=20)
如上所述，data._timeframe 和 data._compression 属性将在 resampledata 期间被覆盖。以下是将发生的情况：

回填将请求 Seconds/20 分辨率
实时条将用于实时数据，因为分辨率等于或大于 Seconds/5，数据支持（不是 CASH 产品）
来自 TWS 的事件最多每 5 秒发生一次。这可能并不重要，因为系统每 20 秒只会向策略发送一个条。
没有实时条的情况：

data = ibstore.getdata(dataname='TWTR-STK-SMART')
cerebro.resampledata(data, timeframe=bt.TimeFrame.Seconds, compression=20)
在这种情况下：

回填将请求 Seconds/20 分辨率
tickString 将用于实时数据（不是 CASH 产品）
来自 TWS 的事件最多每 250 毫秒发生一次。这可能并不重要，因为系统每 20 秒只会向策略发送一个条。
最后是 CASH 产品，时间跨度为 20 秒：

data = ibstore.getdata(dataname='EUR.USD-CASH-IDEALPRO')
cerebro.resampledata(data, timeframe=bt.TimeFrame.Seconds, compression=20)
在这种情况下：

回填将请求 Seconds/20 分辨率
tickPrice 将用于实时数据，因为这是一个现金产品
即使添加了 rtbar=True
来自 TWS 的事件最多每 250 毫秒发生一次。这可能并不重要，因为系统每 20 秒只会向策略发送一个条。
时间管理#
数据馈送将自动从 TWS 报告的 ContractDetails 对象中确定时区。

注意：这需要安装 pytz。如果未安装，用户应提供 tz 参数，一个兼容 tzinfo 的实例，用于所需的输出时区。

注意：如果安装了 pytz，且用户觉得自动时区确定不起作用，tz 参数可以包含一个时区名称字符串。backtrader 将尝试使用给定名称实例化一个 pytz.timezone。

报告的日期时间将是与产品相关的时区。例如：

产品：Eurex 的 EuroStoxxx 50（代码：ESTX50-YYYYMM-DTB）
时区将是 CET（中欧时间），即 Europe/Berlin
产品：ES-Mini（代码：ES-YYYYMM-GLOBEX）
时区将是 EST5EDT，即 EST，即 US/Eastern
产品：EUR.JPY 外汇对（代码：EUR.JPY-CASH-IDEALPRO）
时区将是 EST5EDT，即 EST，即 US/Eastern
实际上，这是一个互动经纪商的设置，因为外汇对几乎 24 小时不间断交易，因此不会有真实的时区。

这种行为确保无论交易者的实际位置如何，交易都保持一致，因为计算机很可能具有交易地点的实际时区，而不是交易场所的时区。

请阅读手册中的时间管理部分。

注意：TWS 演示在报告没有数据下载权限的资产时区方面不准确（EuroStoxx 50 期货是这种情况的一个例子）。

实时数据馈送和重采样/重放#
设计决策关于何时为实时数据馈送交付条：

尽可能实时地交付它们。这似乎是显而易见的，对于 Ticks 时间框架来说确实如此，但如果重采样/重放起作用，可能会有延迟。用例：

重采样配置为 Seconds/5：

cerebro.resampledata(data, timeframe=bt.TimeFrame.Seconds, compression=5)
一个时间戳为 23:05:27.325000 的 tick 被传递。

市场交易缓慢，下一 tick 在 23:05:59.025000 传递。

这可能并不显而易见，但 backtrader 不知道交易非常慢，下一 tick 将在大约 32 秒后到来。如果没有任何规定，带时间戳 23:05:30.000000 的重采样条将延迟大约 29 秒。

这就是为什么实时数据馈送每 x 秒（浮动值）唤醒一次，通知重采样器/重放器没有新数据进来。这是通过在创建实时数据馈送时使用参数 qcheck（默认值：0.5 秒）来控制的。

这意味着重采样器每 qcheck 秒有一次机会交付条，如果本地时钟说重采样周期结束。这样，前述场景中的重采样条（23:05:30.000000）将最多在报告时间后的 qcheck 秒内交付。

由于默认值是 0.5 秒，最迟时间将是：23:05:30.500000。这比之前早了将近 29 秒。

缺点是：

一些 tick 可能太晚，无法用于已经交付的重采样/重放条。如果在交付之后，TWS 从服务器收到一个时间戳为 23:05:29.995000 的延迟消息，这对于已经报告给系统的时间 23:05.30.000000 来说太晚了。

这种情况主要发生在：

timeoffset 在 IBStore 中被禁用（设置为 False）且 IB 报告的时间和本地时钟之间的时间差显著时。

避免大多数这些延迟样本的最佳方法：

增加 qcheck 值，以允许考虑延迟消息：

data = ibstore.getdata('TWTR', qcheck=2.0, ...)
这应该增加额外的空间，即使它会延迟重采样/重放条的交付。

注意：当然，对于 Seconds/5 重采样来说，2.0 秒的延迟与 Minutes/10 的重采样有不同的意义。

如果出于某种原因，最终用户希望禁用 timeoffset 并不通过 qcheck 管理，仍然可以获取延迟样本：

使用 _latethrough 设置为 True 作为 getdata / IBData 的参数：

data = ibstore.getdata('TWTR', _latethrough=True, ...)
在重采样/重放时使用 takelate 设置为 True：

cerebro.resampledata(data, takelate=True)
IBBroker - 实时交易#
注意：应要求，在 backtrader 中提供的模拟经纪商中实现了 tradeid 功能。这允许正确分配不同 tradeid 的佣金。

由于经纪商在报告佣金时，不支持此实时经纪商，因为佣金是在不可能分离不同 tradeid 值的时间点报告的。

尽管仍可以指定 tradeid，但它不再有意义。

使用经纪商#
要使用 IB 经纪商，必须替换 cerebro 创建的标准模拟经纪实例。

使用存储模型（推荐）：

import backtrader as bt

cerebro = bt.Cerebro()
ibstore = bt.stores.IBStore(host='127.0.0.1', port=7496, clientId=35)
cerebro.broker = ibstore.getbroker()  # 或者 cerebro.setbroker(...)
使用直接

方法：

import backtrader as bt

cerebro = bt.Cerebro()
cerebro.broker = bt.brokers.IBBroker(host='127.0.0.1', port=7496, clientId=35)
经纪商参数#
无论是直接还是通过 getbroker，IBBroker 都不支持任何参数。这是因为经纪商只是一个代理，真实的经纪商提供的内容不应被删除。

一些限制#
现金和价值报告#
内部 backtrader 模拟经纪商在调用策略 next 方法之前计算值（净清算价值）和现金，而实时经纪商不能保证这一点。

如果请求这些值，next 的执行可能会延迟到答案到达。

经纪商可能尚未计算这些值。

backtrader 告诉 TWS 提供更新后的值，但不知道消息何时会到达。

IBBroker 的 getcash 和 getvalue 方法报告的值始终是从 IB 接收到的最新值。

注意：进一步的限制是，这些值以账户的基本货币报告，即使可用更多货币的值。这是一个设计选择。

头寸#
backtrader 使用 TWS 报告的资产的头寸（价格和数量）。可以通过订单执行和订单状态消息进行内部计算，但如果丢失了这些消息中的一些，计算将不准确。

当然，如果在连接到 TWS 时，将进行交易的资产已经有一个未平仓头寸，策略计算的交易将无法像往常一样工作，因为有一个初始偏移。

交易#
在使用方面没有变化。只需使用策略中提供的方法（请参阅策略参考以获取完整说明）：

buy
sell
close
cancel
返回的订单对象#
与 backtrader 订单对象兼容（在相同层次结构中子类化）。

订单执行类型#
IB 支持众多执行类型，其中一些由 IB 模拟，一些由交易所支持。决定最初支持哪些订单执行类型的动机是：

与 backtrader 中提供的模拟经纪商兼容

理由是将进行生产的内容已经过回测。

因此，订单执行类型限于模拟经纪商中可用的类型：

Order.Market
Order.Close
Order.Limit
Order.Stop（触发止损后跟随一个市价单）
Order.StopLimit（触发止损后跟随一个限价单）
注意：IB 根据不同策略触发止损。backtrader 不会修改默认设置，即 0：

0 - 默认值。对于 OTC 股票和美国期权，将使用“双重买/卖”方法。所有其他订单将使用“最后”方法。 如果用户希望修改此设置，可以按照 IB 文档提供额外的 **kwargs。 例如，在策略的 next 方法中：

def next(self):
    # 一些逻辑
    self.buy(data, m_triggerMethod=2)
这将策略改为 2（“最后”方法，其中止损订单基于最后价格触发）。

请参考 IB API 文档以获取关于止损触发的进一步说明。

订单有效期#
backtrader 在回测期间可用的相同有效期概念（使用 valid 参数买入和卖出）在此也可用，并具有相同含义。因此，有效期参数对于 IB 订单转换如下：

None -> GTC（Good Til Cancelled）

因为未指定有效期，理解为订单必须有效直到取消。

datetime/date -> GTD（Good Til Date）

传递 datetime.datetime 或 datetime.date 实例表示订单必须有效直到某个时间点。

timedelta(x) -> GTD（timedelta(x) 不等于 timedelta()）

解释为订单有效从现在起加上 timedelta(x)。

float -> GTD

如果值取自 backtrader 使用的原始浮点日期时间存储，则订单必须有效直到由该浮点数指示的日期时间。

timedelta() 或 0 -> DAY

指定了一个值（而不是 None），但为空值，解释为当天（会话）有效的订单。

通知#
标准订单状态将通过策略的 notify_order 方法通知（如果覆盖）。

Submitted - 订单已发送到 TWS

Accepted - 订单已被放置

Rejected - 订单放置失败或在其生命周期内被系统取消

Partial - 部分执行已发生

Completed - 订单已完全执行

Canceled（或 Cancelled）

在 IB 中有多重含义：

用户手动取消
服务器/交易所取消订单
订单有效期已过
将应用一个启发式方法，如果从 TWS 收到 openOrder 消息，订单状态指示 PendingCancel 或 Canceled，则订单将被标记为已过期。

Expired - 请参见上文解释。

参考#
IBStore#
class backtrader.stores.IBStore()
包装一个 ibpy ibConnection 实例的单例类。

这些参数也可以在使用该存储的类中指定，如 IBData 和 IBBroker。

参数：

host（默认：127.0.0.1）：IB TWS 或 IB Gateway 实际运行的位置。虽然这通常是 localhost，但不一定是。
port（默认：7496）：连接到的端口。演示系统使用 7497。
clientId（默认：无）：用于连接 TWS 的 clientId。
无：生成 1 到 65535 之间的随机 id
整数：将传递为使用的值。
notifyall（默认：False）
如果为 False，则只会将错误消息发送到 Cerebro 和 Strategy 的 notify_store 方法。
如果为 True，将通知收到的每一条来自 TWS 的消息。
_debug（默认：False）
将所有收到的 TWS 消息打印到标准输出。
reconnect（默认：3）
初始连接尝试失败后尝试重新连接的次数。
设置为 -1 值以无限期重新连接。
timeout（默认：3.0）
重新连接尝试之间的时间（秒）。
timeoffset（默认：True）
如果为 True，将使用从 reqCurrentTime（IB 服务器时间）获得的时间计算与本地时间的偏移量，并将该偏移量用于价格通知（例如，CASH 市场的 tickPrice 事件）以修改本地计算的时间戳。
时间偏移将传播到 backtrader 生态系统的其他部分，如重采样以使用计算的偏移量对齐重采样时间戳。
timerefresh（默认：60.0）
时间（秒）：刷新时间偏移的频率。
indcash（默认：True）
将 IND 代码管理为现金以获取价格。
IBBroker#
class backtrader.brokers.IBBroker(**kwargs)
互动经纪商的经纪商实现。

该类将互动经纪商的订单/头寸映射到 backtrader 的内部 API。

注意事项：

tradeid 实际上不受支持，因为盈亏是直接从互动经纪商获取的。因为（如预期）以 FIFO 方式计算，因此 tradeid 的盈亏不准确。
头寸：如果在操作开始时有资产的未平仓头寸，或者通过其他方式给出的订单改变了头寸，Cerebro 中策略计算的交易将不反映现实。
为避免这种情况，经纪商将不得不进行自己的头寸管理，这也将允许多个 id 的 tradeid（盈亏也将本地计算），但可能被认为违背了与实时经纪商合作的目的。
IBData#
class backtrader.feeds.IBData(**kwargs)
互动经纪商数据馈送。

支持以下参数 dataname 中的合约规格：

TICKER # 股票类型和 SMART 交易所
TICKER-STK # 股票和 SMART 交易所
TICKER-STK-EXCHANGE # 股票
TICKER-STK-EXCHANGE-CURRENCY # 股票
TICKER-CFD # CFD 和 SMART 交易所
TICKER-CFD-EXCHANGE # CFD
TICKER-CDF-EXCHANGE-CURRENCY # 股票
TICKER-IND-EXCHANGE # 指数
TICKER-IND-EXCHANGE-CURRENCY # 指数
TICKER-YYYYMM-EXCHANGE # 期货
`TICKER-YYYY
MM-EXCHANGE-CURRENCY` # 期货

TICKER-YYYYMM-EXCHANGE-CURRENCY-MULT # 期货
TICKER-FUT-EXCHANGE-CURRENCY-YYYYMM-MULT # 期货
TICKER-YYYYMM-EXCHANGE-CURRENCY-STRIKE-RIGHT # 期权
TICKER-YYYYMM-EXCHANGE-CURRENCY-STRIKE-RIGHT-MULT # 期权
TICKER-FOP-EXCHANGE-CURRENCY-YYYYMM-STRIKE-RIGHT # 期权
TICKER-FOP-EXCHANGE-CURRENCY-YYYYMM-STRIKE-RIGHT-MULT # 期权
CUR1.CUR2-CASH-IDEALPRO # 外汇
TICKER-YYYYMMDD-EXCHANGE-CURRENCY-STRIKE-RIGHT # 期权
TICKER-YYYYMMDD-EXCHANGE-CURRENCY-STRIKE-RIGHT-MULT # 期权
TICKER-OPT-EXCHANGE-CURRENCY-YYYYMMDD-STRIKE-RIGHT # 期权
TICKER-OPT-EXCHANGE-CURRENCY-YYYYMMDD-STRIKE-RIGHT-MULT # 期权
参数：

sectype（默认：STK）

如果在 dataname 规范中未提供，应用的默认值为证券类型。
exchange（默认：SMART）

如果在 dataname 规范中未提供，应用的默认值为交易所。
currency（默认：’’）

如果在 dataname 规范中未提供，应用的默认值为货币。
historical（默认：False）

如果设置为 True，数据馈送将在首次下载数据后停止。
将使用标准数据馈送参数 fromdate 和 todate 作为参考。
如果请求的持续时间大于 IB 在给定时间框架/压缩组合下允许的持续时间，数据馈送将进行多次请求。
what（默认：None）

如果为 None，则历史数据请求的默认值将根据资产类型的不同而不同：
CASH 资产为 ‘BID’
其他为 ‘TRADES’
如果希望其他值，请检查 IB API 文档。
rtbar（默认：False）

如果为 True，将使用互动经纪商提供的 5 秒实时条作为最小刻度。根据文档，这些条形图对应于实时值（经过 IB 整理和处理后）。
如果为 False，则将使用 RTVolume 价格，这些价格基于接收的 tick。在 CASH 资产（如 EUR.JPY）的情况下，始终将使用 RTVolume，并从中提取买入价格（根据互联网上的文献，这已成为与 IB 的行业默认标准）。
即使设置为 True，如果数据重采样/保留到低于 Seconds/5 的时间框架/压缩，也不会使用实时条，因为 IB 不会在该级别以下提供它们。
qcheck（默认：0.5）

在没有数据接收时唤醒的时间（秒），以便适当地重采样/重放数据包并将通知上传到链中。
backfill_start（默认：True）

在启动时执行回填。将通过单个请求获取最大可能的历史数据。
backfill（默认：True）

在断开/重新连接周期后执行回填。将使用间隙持续时间下载最小可能的数据量。
backfill_from（默认：None）

可以传递另一个数据源以进行初始回填。一旦数据源耗尽，如果需要，将从 IB 回填。理想情况下，这意味着从已存储的来源（如磁盘上的文件）进行回填，但不限于此。
latethrough（默认：False）

如果数据源被重采样/重放，一些 tick 可能太晚，无法用于已经交付的重采样/重放条。如果为 True，将允许这些 tick 通过。
请检查重采样器文档以了解如何考虑这些 tick。
特别是当 timeoffset 在 IBStore 实例中设置为 False 且 TWS 服务器时间与本地计算机不同步时，可能会发生这种情况。
tradename（默认：None）

对于某些特定情况（如 CFD），有时价格由一个资产提供，交易在另一个资产中进行。
SPY-STK-SMART-USD -> SP500 ETF（将指定为 `dataname`）
SPY-CFD-SMART-USD -> 对应的 CFD，不提供价格跟踪，但在这种情况下将是交易资产（指定为 `tradename`）。
参数中的默认值允许像 TICKER 这样的情况，参数 sectype（默认：STK）和 exchange（默认：SMART）适用。

一些资产（如 AAPL）需要包括货币在内的完整规格（默认：’’），而其他资产（如 TWTR）可以直接传递。

AAPL-STK-SMART-USD 将是 dataname 的完整规格。

或者：IBData 作为 IBData(dataname='AAPL', currency='USD') 使用默认值（STK 和 SMART）并覆盖货币为 USD。
#################################################################################################################################
Oanda#
Oanda的集成支持以下功能：

实时数据馈送
实时交易
要求#
oandapy：可以通过以下命令安装：pip install git+https://github.com/oanda/oandapy.git
pytz（可选，不推荐）：由于外汇市场的全球性和24x7的特点，选择使用UTC时间。如果愿意，仍然可以使用所需的输出时区。
示例代码#
源代码中包含完整示例：

samples/oandatest/oandatest.py

Oanda - 存储#
存储是实时数据馈送和交易支持的核心，提供了Oanda API和数据馈送及经纪代理之间的适配层。

可以通过以下方法获取经纪商实例：

OandaStore.getbroker(*args, **kwargs)
可以通过以下方法获取数据馈送实例：

OandaStore.getdata(*args, **kwargs)
在这种情况下，许多**kwargs是数据馈送的常见参数，如dataname、fromdate、todate、sessionstart、sessionend、timeframe、compression。

数据可能提供其他参数。请参阅下面的参考。

必要参数#
为了成功连接到Oanda，以下参数是必要的：

token（默认：无）：API访问令牌
account（默认：无）：账户ID
这些由Oanda提供。

无论是连接到模拟服务器还是真实服务器，请使用：

practice（默认：False）：使用测试环境
账户需要定期检查以获取现金和价值。周期性可以通过以下方式控制：

account_tmout（默认：10.0）：刷新账户价值/现金刷新周期
Oanda数据馈送#
实例化数据时：

按照Oanda指南传递符号。例如，EUR/USD根据Oanda的指南需要指定为EUR_USD。实例化如下：

data = oandastore.getdata(dataname='EUR_USD', ...)
时间管理#
除非传递了tz参数（一个pytz兼容对象）给数据馈送，否则所有时间输出都以UTC格式表示，如上所述。

回填#
backtrader不会向Oanda发出特殊请求。对于小时间框架，Oanda在模拟服务器上返回的回填数据长度为500个柱。

OandaBroker - 实时交易#
使用经纪商#
要使用OandaBroker，需要替换cerebro创建的标准经纪商模拟实例。

使用存储模型（推荐）：

import backtrader as bt

cerebro = bt.Cerebro()
oandastore = bt.stores.OandaStore()
cerebro.broker = oandastore.getbroker()  # 或 cerebro.setbroker(...)
经纪商 - 初始头寸#
经纪商支持一个参数：

use_positions（默认：True）：连接到经纪商提供商时使用现有头寸来启动经纪商。 在实例化时设置为False以忽略任何现有头寸。
操作#
使用方面没有变化。只需使用策略中提供的方法（请参阅策略参考以获取完整说明）：

buy
sell
close
cancel
订单执行类型#
Oanda支持几乎所有backtrader需要的订单执行类型，除了Close。因此，订单执行类型限于：

Order.Market
Order.Limit
Order.Stop
Order.StopLimit（使用Stop和upperBound/lowerBound价格）
Order.StopTrail
通过使用takeprofit和stoploss订单成员并创建内部模拟订单来支持括号订单。

订单有效期#
backtrader在回测期间可用的相同有效期概念（使用valid参数买入和卖出）在此也可用，并具有相同含义。因此，Oanda订单的有效期参数转换如下：

None 转换为 Good Til Cancelled 因为未指定有效期，理解为订单必须有效直到取消。
datetime/date 转换为 Good Til Date
timedelta(x) 转换为 Good Til Date（这里timedelta(x)不等于timedelta()） 解释为订单有效从现在起加上timedelta(x)。
timedelta() 或 0 转换为 Session 传递了一个值（而不是None），但为空值，解释为当天（会话）有效的订单。
通知#
标准订单状态将通过策略的notify_order方法通知（如果覆盖）。

Submitted - 订单已发送到TWS
Accepted - 订单已被放置
Rejected - 用于真正的拒绝以及在订单创建过程中没有其他已知状态时
Partial - 部分执行已发生
Completed - 订单已完全执行
Canceled（或 Cancelled）
Expired - 当订单因过期而取消时
参考#
OandaStore#
class backtrader.stores.OandaStore()
控制与Oanda连接的单例类。

参数：

token（默认：无）：API访问令牌
account（默认：无）：账户ID
practice（默认：False）：使用测试环境
account_tmout（默认：10.0）：刷新账户价值/现金刷新周期
OandaBroker#
class backtrader.brokers.OandaBroker(**kwargs)
Oanda的经纪商实现。

该类将Oanda的订单/头寸映射到backtrader的内部API。

参数：

use_positions（默认：True）：连接到经纪商提供商时使用现有头寸来启动经纪商。 在实例化时设置为False以忽略任何现有头寸。
OandaData#
class backtrader.feeds.OandaData(**kwargs)
Oanda数据馈送。

参数：

qcheck（默认：0.5）：在没有数据接收时唤醒的时间（秒），以便适当地重采样/重放数据包并将通知上传到链中。
historical（默认：False）：如果设置为True，数据馈送将在首次下载数据后停止。 将使用标准数据馈送参数fromdate和todate作为参考。 如果请求的持续时间大于IB在给定时间框架/压缩组合下允许的持续时间，数据馈送将进行多次请求。
backfill_start（默认：True）：在启动时执行回填。将通过单个请求获取最大可能的历史数据。
backfill（默认：True）：在断开/重新连接周期后执行回填。将使用间隙持续时间下载最小可能的数据量。
backfill_from（默认：None）：可以传递另一个数据源以进行初始回填。一旦数据源耗尽，如果需要，将从IB回填。理想情况下，这意味着从已存储的来源（如磁盘上的文件）进行回填，但不限于此。
bidask（默认：True）：如果为True，则历史/回填请求将请求服务器的买卖价。 如果为False，则请求中间价。
useask（默认：False）：如果为True，则使用买卖价的卖价部分，而不是默认使用买价。
includeFirst（默认：True）：通过直接将参数设置为Oanda API调用，影响历史/回填请求的第一个柱的交付。
reconnect（默认：True）：当网络连接断开时重新连接。
reconnections（默认：-1）：尝试重新连接的次数：-1表示永远。
reconntimeout（默认：5.0）：重新连接尝试之间的等待时间（秒）。
此数据馈送仅支持以下时间框架和压缩的映射，这符合OANDA API开发者指南中的定义：

(TimeFrame.Seconds, 5): 'S5'
(TimeFrame.Seconds, 10): 'S10'
(TimeFrame.Seconds, 15): 'S15'
(TimeFrame.Seconds, 30): 'S30'
(TimeFrame.Minutes, 1): 'M1'
(TimeFrame.Minutes, 2): 'M3'
(TimeFrame.Minutes, 3): 'M3'
(TimeFrame.Minutes, 4): 'M4'
(TimeFrame.Minutes, 5): 'M5'
(TimeFrame.Minutes, 10): 'M10'
(TimeFrame.Minutes, 15): 'M15'
(TimeFrame.Minutes, 30): 'M30'
(TimeFrame.Minutes, 60): 'H1'
(TimeFrame.Minutes, 120): 'H2'
(TimeFrame.Minutes, 180): 'H3'
(TimeFrame.Minutes, 240): 'H4'
(TimeFrame.Minutes, 360): 'H6'

(TimeFrame.Minutes, 480): 'H8'
(TimeFrame.Days, 1): 'D'
(TimeFrame.Weeks, 1): 'W'
(TimeFrame.Months, 1): 'M'
其他任何组合将被拒绝。
##########################################################################################################
Visual Chart#
Visual Chart 的集成支持以下功能：

实时数据馈送
实时交易
Visual Chart 是一个完整的交易解决方案：

集成图表、数据馈送和经纪功能于单一平台
有关更多信息，请访问：www.visualchart.com

要求#
VisualChart 6（运行在 Windows 上）
comtypes fork： https://github.com/mementum/comtypes
可以通过以下命令安装：

pip install https://github.com/mementum/comtypes/archive/master.zip
Visual Chart 的 API 基于 COM。目前 comtypes 主分支不支持解包 VT_ARRAYS of VT_RECORD。这是 Visual Chart 所使用的。Pull Request #104 已提交，但尚未集成。一旦集成，可以使用主分支。

pytz（可选但强烈推荐）：确保每个数据都在市场时间返回。这对于大多数市场来说都是正确的，但有些市场确实是例外（全球指数就是一个很好的例子）。
示例代码#
源代码中包含完整示例：samples/vctest/vctest.py。

VCStore - 存储#
存储是实时数据馈送/交易支持的核心，提供了 COM API 和数据馈送及经纪代理之间的适配层。

可以通过以下方法获取经纪商实例：

VCStore.getbroker(*args, **kwargs)
可以通过以下方法获取数据馈送实例：

VCStore.getdata(*args, **kwargs)
在这种情况下，许多 **kwargs 是数据馈送的常见参数，如 dataname、fromdate、todate、sessionstart、sessionend、timeframe、compression。

VCStore 将尝试：

使用 Windows 注册表自动定位 VisualChart 在系统中的位置。
如果找到，将扫描安装目录中的 COM DLLs 以创建 COM typelibs 并实例化适当的对象。
如果未找到，将尝试使用已知和硬编码的 CLSIDs 进行相同操作。
注意：即使通过扫描文件系统找到 DLLs，Visual Chart 本身也必须在运行。backtrader 不会启动 Visual Chart。

VCData feeds#
一般#
Visual Chart 提供的数据馈送具有一些有趣的属性：

重新采样由平台完成
并非所有情况下：秒不支持，仍需由 backtrader 完成
例如：

vcstore = bt.stores.VCStore()
vcstore.getdata(dataname='015ES', timeframe=bt.TimeFrame.Ticks)
cerebro.resampledata(data, timeframe=bt.TimeFrame.Seconds, compression=5)
大多数情况下，只需以下操作：

vcstore = bt.stores.VCStore()
data = vcstore.getdata(dataname='015ES', timeframe=bt.TimeFrame.Minutes, compression=2)
cerebro.adddata(data)
数据将通过比较内部设备时钟和平台提供的 tick 来计算内部时间偏移，以便在没有新 tick 进入时尽早传递自动重新采样的 bar。

实例化数据#
按 VisualChart 左上角显示的符号（无空格）传递。例如：

ES-Mini 显示为 001 ES。实例化为：

data = vcstore.getdata(dataname='001ES', ...)
EuroStoxx 50 显示为 015 ES。实例化为：

data = vcstore.getdata(dataname='015ES', ...)
注意：backtrader 会努力清除第四位置的空格（如果名称直接从 Visual Chart 粘贴）。

时间管理#
时间管理遵循 backtrader 的一般规则。为了确保代码不依赖于 DST 转换，请使用市场时间。

数据通知#
数据馈送将通过以下一种或多种方式报告当前状态（检查 Cerebro 和策略参考）：

Cerebro.notify_data（如果覆盖）
Cerebro.adddatacb 添加的回调
Strategy.notify_data（如果覆盖）
策略中的示例：

class VCStrategy(bt.Strategy):
    def notify_data(self, data, status, *args, **kwargs):
        if status == data.LIVE:  # 数据已切换到实时数据
            # 做某些事
            pass
以下通知将根据系统中的更改发送：

CONNECTED：成功初始连接时发送
DISCONNECTED：无法检索数据时发送
CONNBROKEN：连接丢失时发送
NOTSUBSCRIBED：无权限检索数据时发送
DELAYED：历史/回填操作正在进行时发送
LIVE：数据已切换到实时数据时发送
VCBroker - 实时交易#
使用经纪商#
要使用 VCBroker，需要替换 cerebro 创建的标准经纪商模拟实例。

使用存储模型（推荐）：

import backtrader as bt

cerebro = bt.Cerebro()
vcstore = bt.stores.VCStore()
cerebro.broker = vcstore.getbroker()  # 或 cerebro.setbroker(...)
经纪商参数#
VCBroker 不支持任何参数，因为经纪商只是实际经纪商的代理。实际经纪商提供的功能不会被去除。

限制#
头寸#
Visual Chart 报告未平仓头寸，但缺少头寸已关闭的最终事件。因此，backtrader 需要完全记录头寸，并与账户中的任何先前头寸分开。

佣金#
COM 交易接口不报告佣金。除非在实例化经纪商时提供了表示实际佣金的 Commission 实例，否则 backtrader 无法准确估算佣金。

交易操作#
使用方面没有变化。只需使用策略中提供的方法（请参阅策略参考以获取完整说明）：

buy
sell
close
cancel
订单执行类型#
Visual Chart 支持 backtrader 需要的最小订单执行类型，因此任何经过回测的内容都可以上线。限于：

Order.Market
Order.Close
Order.Limit
Order.Stop（触发 Stop 时跟随市价单）
Order.StopLimit（触发 Stop 时跟随限价单）
订单有效期#
backtrader 在回测期间可用的相同有效期概念（使用 valid 参数买入和卖出）在此也可用，并具有相同含义。

通知#
标准订单状态将通过策略的 notify_order 方法通知（如果覆盖）：

Submitted - 订单已发送到 TWS
Accepted - 订单已被放置
Rejected - 订单放置失败或在其生命周期内被系统取消
Partial - 已部分执行
Completed - 订单已完全执行
Canceled（或 Cancelled）
参考#
VCStore#
class backtrader.stores.VCStore()
封装 ibpy ibConnection 实例的单例类。

VCBroker#
class backtrader.brokers.VCBroker(**kwargs)
VisualChart 的经纪商实现。

VCData#
class backtrader.feeds.VCData(**kwargs)
VisualChart 数据馈送。

参数：

qcheck（默认：0.5）：默认唤醒超时以让重采样/重放器检查当前 bar 是否可以交付。
historical（默认：False）：如果未提供 todate 参数（在基类中定义），则如果设置为 True，将强制仅进行历史下载。
milliseconds（默认：True）：Visual Chart 构建的 bar 具有以下格式：HH:MM:59.999000。如果该参数为 True，将添加一毫秒，使其显示为：HH:MM:59.999000。
tradename（默认：无）：无法交易连续期货，但它们非常适合数据跟踪。如果提供该参数，它将是当前期货的名称，该期货将是交易资产。
usetimezones（默认：True）：对于大多数市场，Visual Cha

35 45绘图.txt ##################################################
文件路径: 45绘图.txt
================================================================================

绘图#
尽管回测主要是基于数学计算的自动化过程，但人们常常希望能够实际可视化所发生的一切。不论是使用已经经过回测的现有算法，还是查看数据所产生的内置或自定义指标，绘图都能帮助人们更好地理解所发生的事情，剔除、修改或创建新的想法。

由于所有操作背后都是人类，绘制数据馈送、指标、操作、现金流动和投资组合价值的演变图表有助于人们更好地理解过程，从而做出更明智的决策。因此，backtrader 使用 matplotlib 提供的功能，内置了绘图设施。

如何绘图#
任何回测运行都可以通过调用一个方法进行绘图：

cerebro.plot()
当然，这通常是最后一个命令。例如，以下简单代码使用了 backtrader 源代码中的一个示例数据：

from __future__ import (absolute_import, division, print_function, unicode_literals)

import backtrader as bt

class St(bt.Strategy):
    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data)

data = bt.feeds.BacktraderCSVData(dataname='../../datas/2005-2006-day-001.txt')

cerebro = bt.Cerebro()
cerebro.adddata(data)
cerebro.addstrategy(St)
cerebro.run()
cerebro.plot()
这将生成以下图表：

示例图表

图表包含了 3 个观察器，由于缺乏任何交易，它们在这种情况下几乎没有意义：

CashValue 观察器：跟踪回测运行期间的现金和总投资组合价值（包括现金）。
Trade 观察器：在交易结束时显示实际的利润和亏损。交易定义为开仓并将仓位归零（直接或从多头转为空头或从空头转为多头）。
BuySell 观察器：在价格图上绘制买入和卖出操作的位置。
这 3 个观察器由 cerebro 自动添加，可以通过 stdstats 参数控制（默认：True）。如果希望禁用它们，可以如下操作：

cerebro = bt.Cerebro(stdstats=False)
或在运行时：

cerebro = bt.Cerebro()
...
cerebro.run(stdstats=False)
绘图元素#
尽管前面提到了观察器，它们并不是唯一被绘制的元素。以下 3 种元素会被绘制：

使用 adddata、replaydata 和 resampledata 添加到 Cerebro 的数据馈送。
在策略级别声明的指标（或通过 addindicator 添加到 cerebro 的指标，这纯粹用于实验目的，并将指标添加到一个虚拟策略中）。
使用 addobserver 添加到 cerebro 的观察器。
观察器是与策略同步运行的线性对象，并且可以访问整个生态系统，以便跟踪现金和价值等内容。

绘图选项#
指标和观察器有几个选项可以控制它们在图表上的绘制方式，分为 3 大类：

影响整个对象绘图行为的选项。
影响单个线条绘图行为的选项。
影响系统级别绘图选项的选项。
对象级绘图选项#
这些选项由指标和观察器中的 plotinfo 数据集控制：

plotinfo = dict(
    plot=True,
    subplot=True,
    plotname='',
    plotskip=False,
    plotabove=False,
    plotlinelabels=False,
    plotlinevalues=True,
    plotvaluetags=True,
    plotymargin=0.0,
    plotyhlines=[],
    plotyticks=[],
    plothlines=[],
    plotforce=False,
    plotmaster=None,
    plotylimited=True,
)
尽管 plotinfo 在类定义时显示为字典，但 backtrader 的元类机制将其转变为一个可以继承的对象，并且可以进行多重继承。例如：

如果子类将 subplot=True 更改为 subplot=False，则层级结构中的进一步子类将具有后者作为 subplot 的默认值。

有两种方法为这些参数赋值。让我们看一下 SimpleMovingAverage 实例化的第一种方法：

sma = bt.indicators.SimpleMovingAverage(self.data, period=15, plotname='mysma')
从示例中可以推断，SimpleMovingAverage 构造函数未消耗的任何 **kwargs 都将被解析（如果可能）为 plotinfo 值。SimpleMovingAverage 只有一个定义的参数，即 period。这意味着 plotname 将匹配 plotinfo 中同名的参数。

第二种方法：

sma = bt.indicators.SimpleMovingAverage(self.data, period=15)
sma.plotinfo.plotname = 'mysma'
与 SimpleMovingAverage 一起实例化的 plotinfo 对象可以被访问，并且其中的参数也可以通过标准的 Python 点符号访问。与上面的语法相比，这种方法更容易理解。

参数含义#
plot：是否绘制该对象。
subplot：是否与数据一起绘制或在独立的子图中绘制。例如，移动平均线是绘制在数据上的，而随机指标和 RSI 则是在不同的刻度上绘制的。
plotname：在图表上使用的名称，而不是类名。例如上面的 mysma 而不是 SimpleMovingAverage。
plotskip（已弃用）：plot 的旧别名。
plotabove：是否在数据之上绘制，否则在数据下方绘制。这仅在 subplot=True 时有效。
plotlinelabels：是否在图表的图例中显示单个线条的名称，当 subplot=False 时。
plotlinevalues：控制图例中是否包含指标和观察器线条的最后绘制值。可以通过每条线的 _plotvalue 控制。
plotvaluetags：控制是否在线条的右侧绘制带有最后值的标签。可以通过每条线的 _plotvaluetag 控制。
plotymargin：在图表上单个子图顶部和底部添加的边距。它是一个以 1 为基数的百分比。例如：0.05 表示 5%。
plothlines：一个包含值的可迭代对象（在刻度内），在这些值处绘制水平线。例如，经典指标的超买、超卖区域通常在 70 和 30 处绘制线。
plotyticks：一个包含值的可迭代对象（在刻度内），在这些值处特意放置刻度值。例如，强制刻度有 50 以识别刻度的中点。
plotyhlines：一个包含值的可迭代对象（在刻度内），在这些值处绘制水平线。如果未定义上述任何项，那么水平线和刻度的位置将完全由此值控制。
plotforce：如果所有其他方法都失败，这是一个最后的强制绘图机制。
plotmaster：一个指标/观察器有一个主控，它是工作的数据。在某些情况下，可能希望与不同的主控一起绘图。
plotylimited：目前仅适用于数据馈送。如果为 True（默认），其他线条在数据图上的绘图不会改变刻度。
线条特定绘图选项#
指标/观察器有线条，如何绘制这些线条可以通过 plotlines 对象进行影响。大多数 plotlines 中的选项旨在直接传递给 matplotlib。文档主要通过示例进行说明。

重要：选项是按每条线条指定的。

一些选项由 backtrader 直接控制，这些选项都以 _ 开头：

_plotskip（布尔值）：如果设置为 True，表示跳过绘制特定线条。
_plotvalue（布尔值）：控制此线条的图例是否包含最后绘制的值（默认值为 True）。
_plotvaluetag（布尔值）：控制是否在线条右侧绘制带有最后值的标签（默认值为 True）。
_name（字符串）：更改特定线条的绘图名称。
_skipnan（布尔值，默认：False）：跳过绘制 NaN 值。
_samecolor（布尔值）：强制下一条线条使用与前一条相同的颜色，避免 matplotlib 为每个新绘制的元素循环颜色图。
_method（字符串）：选择 matplotlib 用于绘制元素的方法。
示例：

MACDHisto 使用 `_
method=‘bar’` 绘制直方图。

BuySell 观察器：
plotlines = dict(
    buy=dict(marker='^', markersize=8.0, color='lime', fillstyle='full'),
    sell=dict(marker='v', markersize=8.0, color='red', fillstyle='full')
)
Trades 观察器：
lines = ('pnlplus', 'pnlminus')
plotlines = dict(
    pnlplus=dict(_name='Positive', marker='o', color='blue', markersize=8.0, fillstyle='full'),
    pnlminus=dict(_name='Negative', marker='o', color='red', markersize=8.0, fillstyle='full')
)
系统级绘图选项#
cerebro 的 plot 方法签名：

def plot(self, plotter=None, numfigs=1, iplot=True, **kwargs):
plotter：一个包含控制系统级绘图选项的对象/类。如果为 None，则创建默认 PlotScheme 对象。
numfigs：将图表分解为多少个独立的图表。
iplot：如果在 Jupyter Notebook 中运行，自动内联绘图。
kwargs：将用于更改 plotter 或默认 PlotScheme 对象的属性值。
PlotScheme#
包含控制系统级绘图的所有选项的对象。选项在代码中有文档说明。

颜色#
PlotScheme 类定义了一个方法，可以在子类中重写，该方法返回要使用的下一个颜色：

def color(self, idx)
其中 idx 是当前线条的索引。默认颜色方案是 Tableau 10 颜色调色板，索引修改为：

tab10_index = [3, 0, 2, 1, 2, 4, 5, 6, 7, 8, 9]
############################################################################################################
日期范围#
在 1.9.31.x 版本中，backtrader 增加了部分绘图的功能。

可以使用策略实例中保存的完整时间戳数组的索引来指定绘图范围

也可以使用实际的 datetime.date 或 datetime.datetime 实例来限制绘图范围。

仍然通过标准的 cerebro.plot 进行。例如：

cerebro.plot(start=datetime.date(2005, 7, 1), end=datetime.date(2006, 1, 31))
这对人类来说是最直接的方法。具有扩展能力的人类实际上可以尝试使用时间戳的索引，如下所示：

cerebro.plot(start=75, end=185)
下面是一个非常标准的示例，其中包含一个简单移动平均线（在数据上绘图）、一个随机指标（独立绘图）以及随机指标线的交叉。在命令行参数中传递给 cerebro.plot 的参数。

使用日期方法的执行：

./partial-plot.py --plot 'start=datetime.date(2005, 7, 1),end=datetime.date(2006, 1, 31)'
Python 中的 eval 魔法允许直接在命令行中编写 datetime.date 并将其映射到实际有意义的内容。输出图表如下所示：

部分绘图示例

让我们将其与完整的绘图进行比较，以查看数据是否确实从两端跳过：

./partial-plot.py --plot
Python 中的 eval 魔法允许直接在命令行中编写 datetime.date 并将其映射到实际有意义的内容。输出图表如下所示：

完整绘图示例

示例用法#
$ ./partial-plot.py --help
usage: partial-plot.py [-h] [--data0 DATA0] [--fromdate FROMDATE]
                       [--todate TODATE] [--cerebro kwargs] [--broker kwargs]
                       [--sizer kwargs] [--strat kwargs] [--plot [kwargs]]

Sample for partial plotting

optional arguments:
  -h, --help           show this help message and exit
  --data0 DATA0        Data to read in (default:
                       ../../datas/2005-2006-day-001.txt)
  --fromdate FROMDATE  Date[time] in YYYY-MM-DD[THH:MM:SS] format (default: )
  --todate TODATE      Date[time] in YYYY-MM-DD[THH:MM:SS] format (default: )
  --cerebro kwargs     kwargs in key=value format (default: )
  --broker kwargs      kwargs in key=value format (default: )
  --sizer kwargs       kwargs in key=value format (default: )
  --strat kwargs       kwargs in key=value format (default: )
  --plot [kwargs]      kwargs in key=value format (default: )
示例代码#
from __future__ import (absolute_import, division, print_function, unicode_literals)

import argparse
import datetime
import backtrader as bt

class St(bt.Strategy):
    params = ()

    def __init__(self):
        bt.ind.SMA()
        stoc = bt.ind.Stochastic()
        bt.ind.CrossOver(stoc.lines.percK, stoc.lines.percD)

    def next(self):
        pass

def runstrat(args=None):
    args = parse_args(args)
    cerebro = bt.Cerebro()

    # 数据馈送 kwargs
    kwargs = dict()

    # 解析 from/to-date
    dtfmt, tmfmt = '%Y-%m-%d', 'T%H:%M:%S'
    for a, d in ((getattr(args, x), x) for x in ['fromdate', 'todate']):
        if a:
            strpfmt = dtfmt + tmfmt * ('T' in a)
            kwargs[d] = datetime.datetime.strptime(a, strpfmt)

    # 数据馈送
    data0 = bt.feeds.BacktraderCSVData(dataname=args.data0, **kwargs)
    cerebro.adddata(data0)

    # 经纪人
    cerebro.broker = bt.brokers.BackBroker(**eval('dict(' + args.broker + ')'))

    # 大小调整器
    cerebro.addsizer(bt.sizers.FixedSize, **eval('dict(' + args.sizer + ')'))

    # 策略
    cerebro.addstrategy(St, **eval('dict(' + args.strat + ')'))

    # 执行
    cerebro.run(**eval('dict(' + args.cerebro + ')'))

    if args.plot:  # 如果请求绘图，则绘制
        cerebro.plot(**eval('dict(' + args.plot + ')'))

def parse_args(pargs=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=(
            'Sample for partial plotting'
        )
    )

    parser.add_argument('--data0', default='../../datas/2005-2006-day-001.txt',
                        required=False, help='Data to read in')

    # 日期的默认值
    parser.add_argument('--fromdate', required=False, default='',
                        help='Date[time] in YYYY-MM-DD[THH:MM:SS] format')

    parser.add_argument('--todate', required=False, default='',
                        help='Date[time] in YYYY-MM-DD[THH:MM:SS] format')

    parser.add_argument('--cerebro', required=False, default='',
                        metavar='kwargs', help='kwargs in key=value format')

    parser.add_argument('--broker', required=False, default='',
                        metavar='kwargs', help='kwargs in key=value format')

    parser.add_argument('--sizer', required=False, default='',
                        metavar='kwargs', help='kwargs in key=value format')

    parser.add_argument('--strat', required=False, default='',
                        metavar='kwargs', help='kwargs in key=value format')

    parser.add_argument('--plot', required=False, default='',
                        nargs='?', const='{}',
                        metavar='kwargs', help='kwargs in key=value format')

    return parser.parse_args(pargs)

if __name__ == '__main__':
    runstrat()
###############################################################################################
在同轴绘图#
在之前的文章“future-spot”中，我们在同一空间上绘制了原始数据和略微（随机）修改后的数据，但它们并没有在同一轴上绘制。

恢复该文章的第一张图片：

图表示例

我们可以看到：

图表的左右两侧有不同的刻度。
当观察摆动的红线（随机化数据）时最明显，它在原始数据周围上下摆动大约 50 个点。
在图表上，视觉印象是这种随机化数据大部分时间都在原始数据上方。这只是由于不同刻度导致的视觉印象。
虽然 1.9.32.116 版本已经初步支持完全在同一轴上绘图，但图例标签会重复（仅标签，不是数据），这会让人感到困惑。

1.9.33.116 版本修复了这个问题，允许完全在同一轴上绘图。使用模式类似于选择使用哪个数据进行绘图。在之前的文章中：

import backtrader as bt

cerebro = bt.Cerebro()

data0 = bt.feeds.MyFavouriteDataFeed(dataname='futurename')
cerebro.adddata(data0)

data1 = bt.feeds.MyFavouriteDataFeed(dataname='spotname')
data1.compensate(data0)  # 告诉系统 data1 的操作影响 data0
data1.plotinfo.plotmaster = data0
data1.plotinfo.sameaxis = True
cerebro.adddata(data1)

...

cerebro.run()
data1 获取一些 plotinfo 值来：

与 plotmaster（即 data0）在同一空间绘图。
获取使用 sameaxis 的指示。
原因是平台无法提前知道每个数据的刻度是否兼容。因此，它们会在独立的刻度上绘图。

在之前的示例中，增加了一个选项在 sameaxis 上绘图。示例执行：

$ ./future-spot.py --sameaxis
结果图表：

同一轴上的绘图示例

需要注意的是：

右侧只有一个刻度。
现在，随机化数据似乎明显在原始数据周围摆动，这是预期的视觉行为。
示例用法#
$ ./future-spot.py --help
usage: future-spot.py [-h] [--no-comp] [--sameaxis]

Compensation example

optional arguments:
  -h, --help  show this help message and exit
  --no-comp
  --sameaxis
示例代码#
from __future__ import (absolute_import, division, print_function, unicode_literals)

import argparse
import random
import backtrader as bt

# 修改收盘价的过滤器
def close_changer(data, *args, **kwargs):
    data.close[0] += 50.0 * random.randint(-1, 1)
    return False  # 流长度不变

# 重写标准标记
class BuySellArrows(bt.observers.BuySell):
    plotlines = dict(buy=dict(marker='$\u21E7$', markersize=12.0),
                     sell=dict(marker='$\u21E9$', markersize=12.0))

class St(bt.Strategy):
    def __init__(self):
        bt.obs.BuySell(self.data0, barplot=True)  # 在此处完成
        BuySellArrows(self.data1, barplot=True)  # 为不同的数据设置不同的标记

    def next(self):
        if not self.position:
            if random.randint(0, 1):
                self.buy(data=self.data0)
                self.entered = len(self)
        else:  # 在市场中
            if (len(self) - self.entered) >= 10:
                self.sell(data=self.data1)

def runstrat(args=None):
    args = parse_args(args)
    cerebro = bt.Cerebro()

    dataname = '../../datas/2006-day-001.txt'  # 数据馈送

    data0 = bt.feeds.BacktraderCSVData(dataname=dataname, name='data0')
    cerebro.adddata(data0)

    data1 = bt.feeds.BacktraderCSVData(dataname=dataname, name='data1')
    data1.addfilter(close_changer)
    if not args.no_comp:
        data1.compensate(data0)
    data1.plotinfo.plotmaster = data0
    if args.sameaxis:
        data1.plotinfo.sameaxis = True
    cerebro.adddata(data1)

    cerebro.addstrategy(St)  # 示例策略

    cerebro.addobserver(bt.obs.Broker)  # 通过 stdstats=False 移除
    cerebro.addobserver(bt.obs.Trades)  # 通过 stdstats=False 移除

    cerebro.broker.set_coc(True)
    cerebro.run(stdstats=False)  # 执行
    cerebro.plot(volume=False)  # 并绘图

def parse_args(pargs=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=('Compensation example'))

    parser.add_argument('--no-comp', required=False, action='store_true')
    parser.add_argument('--sameaxis', required=False, action='store_true')
    return parser.parse_args(pargs)

if __name__ == '__main__':
    runstrat()
    

36 46时间日期.txt ##################################################
文件路径: 46时间日期.txt
================================================================================

管理#
在发布 1.5.0 版本之前，backtrader 对时间管理采用的是直接方式，即直接使用数据源计算出的任何日期时间。用户输入的参数，如 fromdate（或 sessionstart），也可以传递给任何数据源。

这种方法在对冻结数据源进行回测时效果很好。可以假设输入的日期时间在进入系统之前已经经过处理。

但在 1.5.0 版本之后，backtrader 开始支持实时数据源，这就需要考虑日期时间管理。如果以下情况总是成立，那么就不需要进行这种管理：

纽约的交易者交易 ES-Mini。这两个的时区都是 US/Eastern（或其别名）。
柏林的交易者交易 DAX 期货。在这种情况下，两个的时区都是 CET（或 Europe/Berlin）。
上面的直接输入-输出日期时间方法可以工作，因为柏林的交易者可以始终这样做：

class Strategy(bt.Strategy):

    def next(self):
        # DAX 期货在 CET 时间早上 08:00 开盘
        if self.data.datetime.time() < datetime.time(8, 30):
            # 市场运行 30 分钟之前不操作
            return  #
当同一个柏林交易者决定交易 ES-Mini 时，直接方法的问题就会显现出来。因为 DST（夏令时）的变化发生在一年中的不同时间，这会导致时间差异在一年中的某些周内不同步。

以下代码并不总是有效：

class Strategy(bt.Strategy):

    def next(self):
        # SPX 在 US/Eastern 全年早上 09:30 开盘
        # 大部分时间是 15:30 CET
        # 但有时是 16:30 CET 或 14:30 CET，取决于美国和欧洲的 DST 切换时间
        # 因此以下代码是不可靠的

        if self.data.datetime.time() < datetime.time(16, 0):
            # 市场运行 30 分钟之前不操作
            return  #
使用时区操作#
为了解决上述问题并仍然保持与直接输入-输出时间方法的兼容性，backtrader 为终端用户提供了以下选项：

日期时间输入#
默认情况下，平台不会触及数据源提供的日期时间。

用户可以通过以下方式覆盖此输入：

为数据源提供 tzinput 参数。这必须是与 datetime.tzinfo 接口兼容的对象。用户很可能会提供一个 pytz.timezone 实例。
通过这个决定，backtrader 内部使用的时间被认为是 UTC 类格式，即：

如果数据源已经以 UTC 格式存储它。
通过 tzinput 转换后。
它实际上不是 UTC，但它是用户的参考，因此是 UTC 类的。

日期时间输出#
如果数据源可以自动确定时区，这将是默认设置。

这在实时数据源的情况下尤其有意义，例如柏林（CET 时区）的交易者交易 US/Eastern 时区的产品。

因为交易者总是得到正确的时间，在上面的示例中，开盘时间在 US/Eastern 时区内始终是早上 09:30，而不是一年中大部分时间的 15:30 CET，有时是 16:30 CET，有时是 14:30 CET。

如果不能确定，那么输出将是输入时确定的时间（UTC 类时间）。

用户可以覆盖并确定输出的实际时区：

为数据源提供 tz 参数。这必须是与 datetime.tzinfo 接口兼容的对象。用户很可能会提供一个 pytz.timezone 实例。
注意：

用户输入的参数（如 fromdate 或 sessionstart）应与实际 tz 同步，无论是由数据源自动计算，用户提供还是默认（None，表示直接输入-输出日期时间）。

考虑到上述所有内容，让我们回顾一下柏林的交易者，交易 US/Eastern 时区的产品：

import pytz
import bt

data = bt.feeds.MyFeed('ES-Mini', tz=pytz.timezone('US/Eastern'))

class Strategy(bt.Strategy):

    def next(self):
        # 这将全年有效。
        # 数据源将在 'US/Eastern' 时区的框架内返回数据，
        # 用户将 '10:00' 作为参考时间
        # 因为在 'US/Eastern' 时区，SPX 指数总是
        # 在 09:30 开盘，这将始终有效

        if self.data.datetime.time() < datetime.time(10, 0):
            # 市场运行 30 分钟之前不操作
            return  #
对于可以自动确定输出时区的数据源：

import bt

data = bt.feeds.MyFeedAutoTZ('ES-Mini')

class Strategy(bt.Strategy):

    def next(self):
        # 这将全年有效。
        # 数据源将在 'US/Eastern' 时区的框架内返回数据，
        # 用户将 '10:00' 作为参考时间
        # 因为在 'US/Eastern' 时区，SPX 指数总是
        # 在 09:30 开盘，这将始终有效

        if self.data.datetime.time() < datetime.time(10, 0):
            # 市场运行 30 分钟之前不操作
            return  #
显然，上面示例中的 MyFeed 和 MyFeedAuto 只是虚拟名称。

注意：

在撰写本文时，唯一包含在发行版中的能够自动确定时区的数据源是连接到 Interactive Brokers 的数据源。

Previous
同轴绘图
############################################################################################################################
定时器#
在版本 1.9.44.116 中，backtrader 添加了定时器功能。这使得在特定时间点调用 notify_timer（在 Cerebro 和 Strategy 中可用）成为可能，用户可以进行精细控制。

选项#
基于绝对时间输入或相对于会话开始/结束时间的定时器。
时间规范的时区指定，可以直接通过 pytz 兼容对象或通过数据源会话结束时间进行指定。
相对于指定时间的起始偏移。
重复间隔。
工作日过滤器（带有结转选项）。
月份天数过滤器（带有结转选项）。
自定义回调过滤器。
使用模式#
在 Cerebro 和 Strategy 子类中，定时器回调将在以下方法中接收：

def notify_timer(self, timer, when, *args, **kwargs):
    '''接收定时器通知，其中 `timer` 是通过 `add_timer` 返回的定时器，`when` 是调用时间。
    `args` 和 `kwargs` 是传递给 `add_timer` 的额外参数。

    实际的 `when` 时间可能稍后，但系统可能无法在之前调用定时器。
    此值是定时器值，而不是系统时间。
    '''
添加定时器 - 通过 Strategy#
使用以下方法完成：

def add_timer(self, when,
              offset=datetime.timedelta(), repeat=datetime.timedelta(),
              weekdays=[], weekcarry=False,
              monthdays=[], monthcarry=True,
              allow=None,
              tzdata=None, cheat=False,
              *args, **kwargs):
    '''
它返回创建的 Timer 实例。下面是参数的解释。

添加定时器 - 通过 Cerebro#
使用相同的方法，只是增加了参数 strats。如果设置为 True，定时器不仅会通知给 cerebro，还会通知系统中运行的所有策略。

def add_timer(self, when,
              offset=datetime.timedelta(), repeat=datetime.timedelta(),
              weekdays=[], weekcarry=False,
              monthdays=[], monthcarry=True,
              allow=None,
              tzdata=None, cheat=False, strats=False,
              *args, **kwargs):
    '''
它返回创建的 Timer 实例。

定时器调用时间#
如果 cheat=False#
这是默认设置。在这种情况下，定时器将在以下情况后调用：

数据源加载当前柱的新值之后。
经纪人评估订单并重新计算投资组合价值之后。
指标重新计算之前（因为这由策略触发）。
调用任何策略的 next 方法之前。
如果 cheat=True#
在这种情况下，定时器将在以下情况后调用：

数据源加载当前柱的新值之后。
经纪人评估订单并重新计算投资组合价值之前。
因此，在指标重新计算和调用任何策略的 next 方法之前调用定时器，这样可以实现以下场景：

在新柱被经纪人评估之前调用定时器。
指标具有前一天收盘时的值，并可用于生成进出信号（或在上次评估 next 时设置标志）。
因为新价格可用，可以使用开盘价计算股份。这假设一个人通过观察开盘拍卖得到良好的开盘指示。
使用每日柱#
示例 scheduled.py 默认使用 backtrader 发行版中提供的标准每日柱。策略参数如下：

class St(bt.Strategy):
    params = dict(
        when=bt.timer.SESSION_START,
        timer=True,
        cheat=False,
        offset=datetime.timedelta(),
        repeat=datetime.timedelta(),
        weekdays=[],
    )
数据具有以下会话时间：

开始：09:00
结束：17:30
运行只带时间的情况：

$ ./scheduled.py --strat when='datetime.time(15,30)'
输出结果：

strategy notify_timer with tid 0, when 2005-01-03 15:30:00 cheat False
1, 2005-01-03 17:30:00, Week 1, Day 1, O 2952.29, H 2989.61, L 2946.8, C 2970.02
strategy notify_timer with tid 0, when 2005-01-04 15:30:00 cheat False
2, 2005-01-04 17:30:00, Week 1, Day 2, O 2969.78, H 2979.88, L 2961.14, C 2971.12
strategy notify_timer with tid 0, when 2005-01-05 15:30:00 cheat False
3, 2005-01-05 17:30:00, Week 1, Day 3, O 2969.0, H 2969.0, L 2942.69, C 2947.19
strategy notify_timer with tid 0, when 2005-01-06 15:30:00 cheat False
...
指定的定时器在 15:30 触发。没有惊喜。让我们增加 30 分钟的偏移：

$ ./scheduled.py --strat when='datetime.time(15,30)',offset='datetime.timedelta(minutes=30)'
输出结果：

strategy notify_timer with tid 0, when 2005-01-03 16:00:00 cheat False
1, 2005-01-03 17:30:00, Week 1, Day 1, O 2952.29, H 2989.61, L 2946.8, C 2970.02
strategy notify_timer with tid 0, when 2005-01-04 16:00:00 cheat False
2, 2005-01-04 17:30:00, Week 1, Day 2, O 2969.78, H 2979.88, L 2961.14, C 2971.12
strategy notify_timer with tid 0, when 2005-01-05 16:00:00 cheat False
...
定时器的时间从 15:30 变为 16:00。没有惊喜。让我们以会话开始为参考：

$ ./scheduled.py --strat when='bt.timer.SESSION_START',offset='datetime.timedelta(minutes=30)'
输出结果：

strategy notify_timer with tid 0, when 2005-01-03 09:30:00 cheat False
1, 2005-01-03 17:30:00, Week 1, Day 1, O 2952.29, H 2989.61, L 2946.8, C 2970.02
strategy notify_timer with tid 0, when 2005-01-04 09:30:00 cheat False
2, 2005-01-04 17:30:00, Week 1, Day 2, O 2969.78, H 2979.88, L 2961.14, C 2971.12
...
定时器回调时间为 09:30。会话开始时间为 09:00。这样可以简单地说希望在会话开始后 30 分钟执行一个操作。

运行带有 5 分钟柱的数据#
示例 scheduled-min.py 默认运行 backtrader 发行版中的标准 5 分钟柱。策略参数如下：

class St(bt.Strategy):
    params = dict(
        when=bt.timer.SESSION_START,
        timer=True,
        cheat=False,
        offset=datetime.timedelta(),
        repeat=datetime.timedelta(),
        weekdays=[],
        weekcarry=False,
        monthdays=[],
        monthcarry=True,
    )
数据具有相同的会话时间：

开始：09:00
结束：17:30
让我们进行一些实验。首先是一个定时器。

$ ./scheduled-min.py --strat when='datetime.time(15, 30)'
输出结果：

1, 2006-01-02 09:05:00, Week 1, Day 1, O 3578.73, H 3587.88, L 3578.73, C 3582.99
2, 2006-01-02 09:10:00, Week 1, Day 1, O 3583.01, H 3588.4, L 3583.01, C 3588.03
...
77, 2006-01-02 15:25:00, Week 1, Day 1, O 3599.07, H 3599.68, L 3598.47, C 3599.68
strategy notify_timer with tid 0, when 2006-01-02 15:30:00 cheat False
78, 2006-01-02 15:30:00, Week 1, Day 1, O 3599.64, H 3599.73, L 3599.0, C 3599.67
...
179

, 2006-01-03 15:25:00, Week 1, Day 2, O 3634.72, H 3635.0, L 3634.06, C 3634.87
strategy notify_timer with tid 0, when 2006-01-03 15:30:00 cheat False
180, 2006-01-03 15:30:00, Week 1, Day 2, O 3634.81, H 3634.89, L 3634.04, C 3634.23
...
定时器在 15:30 触发。日志显示了它在前两天的触发情况。

增加 15 分钟的重复间隔#
$ ./scheduled-min.py --strat when='datetime.time(15, 30)',repeat='datetime.timedelta(minutes=15)'
输出结果：

...
74, 2006-01-02 15:10:00, Week 1, Day 1, O 3596.12, H 3596.63, L 3595.92, C 3596.63
75, 2006-01-02 15:15:00, Week 1, Day 1, O 3596.36, H 3596.65, L 3596.19, C 3596.65
76, 2006-01-02 15:20:00, Week 1, Day 1, O 3596.53, H 3599.13, L 3596.12, C 3598.9
77, 2006-01-02 15:25:00, Week 1, Day 1, O 3599.07, H 3599.68, L 3598.47, C 3599.68
strategy notify_timer with tid 0, when 2006-01-02 15:30:00 cheat False
78, 2006-01-02 15:30:00, Week 1, Day 1, O 3599.64, H 3599.73, L 3599.0, C 3599.67
79, 2006-01-02 15:35:00, Week 1, Day 1, O 3599.61, H 3600.29, L 3599.52, C 3599.92
80, 2006-01-02 15:40:00, Week 1, Day 1, O 3599.96, H 3602.06, L 3599.76, C 3602.05
strategy notify_timer with tid 0, when 2006-01-02 15:45:00 cheat False
81, 2006-01-02 15:45:00, Week 1, Day 1, O 3601.97, H 3602.07, L 3601.45, C 3601.83
82, 2006-01-02 15:50:00, Week 1, Day 1, O 3601.74, H 3602.8, L 3601.63, C 3602.8
83, 2006-01-02 15:55:00, Week 1, Day 1, O 3602.53, H 3602.74, L 3602.33, C 3602.61
strategy notify_timer with tid 0, when 2006-01-02 16:00:00 cheat False
84, 2006-01-02 16:00:00, Week 1, Day 1, O 3602.58, H 3602.75, L 3601.81, C 3602.14
85, 2006-01-02 16:05:00, Week 1, Day 1, O 3602.16, H 3602.16, L 3600.86, C 3600.96
86, 2006-01-02 16:10:00, Week 1, Day 1, O 3601.2, H 3601.49, L 3600.94, C 3601.27
...
strategy notify_timer with tid 0, when 2006-01-02 17:15:00 cheat False
99, 2006-01-02 17:15:00, Week 1, Day 1, O 3603.96, H 3603.96, L 3602.89, C 3603.79
100, 2006-01-02 17:20:00, Week 1, Day 1, O 3603.94, H 3605.95, L 3603.87, C 3603.91
101, 2006-01-02 17:25:00, Week 1, Day 1, O 3604.0, H 3604.76, L 3603.85, C 3604.64
strategy notify_timer with tid 0, when 2006-01-02 17:30:00 cheat False
102, 2006-01-02 17:30:00, Week 1, Day 1, O 3604.06, H 3604.41, L 3603.95, C 3604.33
103, 2006-01-03 09:05:00, Week 1, Day 2, O 3604.08, H 3609.6, L 3604.08, C 3609.6
104, 2006-01-03 09:10:00, Week 1, Day 2, O 3610.34, H 3617.31, L 3610.34, C 3617.31
105, 2006-01-03 09:15:00, Week 1, Day 2, O 3617.61, H 3617.87, L 3616.03, C 3617.51
106, 2006-01-03 09:20:00, Week 1, Day 2, O 3617.24, H 3618.86, L 3616.09, C 3618.42
...
179, 2006-01-03 15:25:00, Week 1, Day 2, O 3634.72, H 3635.0, L 3634.06, C 3634.87
strategy notify_timer with tid 0, when 2006-01-03 15:30:00 cheat False
180, 2006-01-03 15:30:00, Week 1, Day 2, O 3634.81, H 3634.89, L 3634.04, C 3634.23
...
使用作弊模式#
$ ./scheduled-min.py --strat when='bt.timer.SESSION_START',cheat=True
输出结果：

strategy notify_timer with tid 1, when 2006-01-02 09:00:00 cheat True
-- 2006-01-02 09:05:00 Create buy order
strategy notify_timer with tid 0, when 2006-01-02 09:00:00 cheat False
1, 2006-01-02 09:05:00, Week 1, Day 1, O 3578.73, H 3587.88, L 3578.73, C 3582.99
-- 2006-01-02 09:10:00 Buy Exec @ 3583.01
2, 2006-01-02 09:10:00, Week 1, Day 1, O 3583.01, H 3588.4, L 3583.01, C 3588.03
...
创建订单时间为 09:05:00，执行时间为 09:10:00，因为经纪人没有在开盘时作弊模式。让我们设置它……

$ ./scheduled-min.py --strat when='bt.timer.SESSION_START',cheat=True --broker coo=True
输出结果：

strategy notify_timer with tid 1, when 2006-01-02 09:00:00 cheat True
-- 2006-01-02 09:05:00 Create buy order
strategy notify_timer with tid 0, when 2006-01-02 09:00:00 cheat False
-- 2006-01-02 09:05:00 Buy Exec @ 3578.73
1, 2006-01-02 09:05:00, Week 1, Day 1, O 3578.73, H 3587.88, L 3578.73, C 3582.99
2, 2006-01-02 09:10:00, Week 1, Day 1, O 3583.01, H 3588.4, L 3583.

01, C 3588.03
...
下达时间和执行时间均为 09:05:00，执行价格为 09:05:00 的开盘价。

其他场景#
定时器允许通过传递一个整数列表来指定哪些天（iso 代码，周一为 1，周日为 7）定时器可以实际触发。例如：

weekdays=[5]  # 这将请求定时器仅在周五有效
如果周五是非交易日，并且定时器应在下一个交易日触发，可以添加 weekcarry=True。

类似地，可以决定每月的某一天，例如：

monthdays=[15]  # 每月的 15 日
如果 15 日是非交易日，并且定时器应在下一个交易日触发，可以添加 monthcarry=True。

目前没有实现像以下规则的功能：3 月、6 月、9 月和 12 月的第三个星期五（期货/期权到期日），但可以通过传递一个回调函数来实现规则：

allow=callable  # 回调函数接收一个 datetime.date 实例，如果日期适用于定时器，则返回 True，否则返回 False
实现上述规则的代码：

class FutOpExp(object):
    def __init__(self):
        self.fridays = 0
        self.curmonth = -1

    def __call__(self, d):
        _, _, isowkday = d.isocalendar()

        if d.month != self.curmonth:
            self.curmonth = d.month
            self.fridays = 0

        # 周一=1 ... 周日=7
        if isowkday == 5 and self.curmonth in [3, 6, 9, 12]:
            self.fridays += 1

            if self.fridays == 3:  # 第三个星期五
                return True  # 定时器允许

        return False  # 定时器不允许
然后将 allow=FutOpExp() 传递给定时器的创建。

add_timer 的参数#
when：可以是
datetime.time 实例（见下文的 tzdata）
bt.timer.SESSION_START 引用会话开始时间
bt.timer.SESSION_END 引用会话结束时间
offset：必须是 datetime.timedelta 实例，用于偏移 when 的值。与 SESSION_START 和 SESSION_END 结合使用时很有意义，表示定时器在会话开始后 15 分钟被调用。
repeat：必须是 datetime.timedelta 实例，指示首次调用后，在同一会话内重复调用的间隔。
weekdays：一个排序的可迭代对象，包含整数，指示定时器在星期几（iso 代码，周一为 1，周日为 7）实际有效。如果未指定，定时器将在所有天数有效。
weekcarry（默认值：False）：如果为 True，并且在一周内未看到指定的日期（例如交易假日），定时器将在下一天执行（即使在新的一周内）。
monthdays：一个排序的可迭代对象，包含整数，指示定时器在每月的哪些天实际有效。如果未指定，定时器将在所有天数有效。
monthcarry（默认值：True）：如果未看到指定日期（周末、交易假日），定时器将在下一个可用的日子执行。
allow（默认值：None）：一个回调函数，接收一个 datetime.date 实例，如果日期适用于定时器，则返回 True，否则返回 False。
tzdata：可以是 None（默认），pytz 实例或数据源实例。
None：when 按原样解释（这相当于将其视为 UTC，即使它不是）。
pytz 实例：when 将解释为在指定时区的本地时间。
数据源实例：when 将解释为在数据源实例的 tz 参数指定的本地时间。
strats（默认值：False）：是否调用策略的 notify_timer。
cheat（默认值：False）：如果为 True，定时器将在经纪人有机会评估订单之前调用。这打开了在会话开始前基于开盘价下单的机会。
*args：任何额外的参数将传递给 notify_timer。
**kwargs：任何额外的关键字参数将传递给 notify_timer。
示例用法 scheduled.py#
$ ./scheduled.py --help
输出结果：

usage: scheduled.py [-h] [--data0 DATA0] [--fromdate FROMDATE]
                    [--todate TODATE] [--cerebro kwargs] [--broker kwargs]
                    [--sizer kwargs] [--strat kwargs] [--plot [kwargs]]

Sample Skeleton

optional arguments:
  -h, --help           show this help message and exit
  --data0 DATA0        Data to read in (default:
                       ../../datas/2005-2006-day-001.txt)
  --fromdate FROMDATE  Date[time] in YYYY-MM-DD[THH:MM:SS] format (default: )
  --todate TODATE      Date[time] in YYYY-MM-DD[THH:MM:SS] format (default: )
  --cerebro kwargs     kwargs in key=value format (default: )
  --broker kwargs      kwargs in key=value format (default: )
  --sizer kwargs       kwargs in key=value format (default: )
  --strat kwargs       kwargs in key=value format (default: )
  --plot [kwargs]      kwargs in key=value format (default: )
示例源代码 scheduled.py#
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse
import datetime

import backtrader as bt


class St(bt.Strategy):
    params = dict(
        when=bt.timer.SESSION_START,
        timer=True,
        cheat=False,
        offset=datetime.timedelta(),
        repeat=datetime.timedelta(),
        weekdays=[],
    )

    def __init__(self):
        bt.ind.SMA()
        if self.p.timer:
            self.add_timer(
                when=self.p.when,
                offset=self.p.offset,
                repeat=self.p.repeat,
                weekdays=self.p.weekdays,
            )
        if self.p.cheat:
            self.add_timer(
                when=self.p.when,
                offset=self.p.offset,
                repeat=self.p.repeat,
                cheat=True,
            )

        self.order = None

    def prenext(self):
        self.next()

    def next(self):
        _, isowk, isowkday = self.datetime.date().isocalendar()
        txt = '{}, {}, Week {}, Day {}, O {}, H {}, L {}, C {}'.format(
            len(self), self.datetime.datetime(),
            isowk, isowkday,
            self.data.open[0], self.data.high[0],
            self.data.low[0], self.data.close[0])

        print(txt)

    def notify_timer(self, timer, when, *args, **kwargs):
        print('strategy notify_timer with tid {}, when {} cheat {}'.
              format(timer.p.tid, when, timer.p.cheat))

        if self.order is None and timer.p.cheat:
            print('-- {} Create buy order'.format(self.data.datetime.date()))
            self.order = self.buy()

    def notify_order(self, order):
        if order.status == order.Completed:
            print('-- {} Buy Exec @ {}'.format(
                self.data.datetime.date(), order.executed.price))


def runstrat(args=None):
    args = parse_args(args)

    cerebro = bt.Cerebro()

    # 数据源 kwargs
    kwargs = dict(
        timeframe=bt.TimeFrame.Days,
        compression=1,
        sessionstart=datetime.time(9, 0),
        sessionend=datetime.time(17, 30),
    )

    # 解析 from/to-date
    dtfmt, tmfmt = '%Y-%m-%d', 'T%H:%M:%S'
    for a, d in ((getattr(args, x), x) for x in ['fromdate', 'todate']):
        if a:
            strpfmt = dtfmt + tmfmt * ('T' in a)
            kwargs[d] = datetime.datetime.strptime(a, strpfmt)

    # 数据源
    data0 = bt.feeds.BacktraderCSVData(dataname=args.data0, **kwargs)
    cerebro.adddata(data0)

    # 经纪人
    cerebro.broker = bt.brokers.BackBroker(**eval('dict(' + args.broker + ')'))

    # 调整器
    cerebro.addsizer(bt.sizers.FixedSize, **eval('dict(' + args.sizer + ')'))

    # 策略
    cerebro.addstrategy(St, **eval('dict(' + args.strat + ')'))

    # 执行
    cerebro.run(**eval('dict(' + args.cerebro + ')'))

    if args.plot:  # 如果请求则绘图
        cerebro.plot(**eval('dict(' + args.plot + ')'))




def parse_args(pargs=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=(
            'Sample Skeleton'
        )
    )

    parser.add_argument('--data0', default='../../datas/2005-2006-day-001.txt',
                        required=False, help='Data to read in')

    # 日期默认值
    parser.add_argument('--fromdate', required=False, default='',
                        help='Date[time] in YYYY-MM-DD[THH:MM:SS] format')

    parser.add_argument('--todate', required=False, default='',
                        help='Date[time] in YYYY-MM-DD[THH:MM:SS] format')

    parser.add_argument('--cerebro', required=False, default='',
                        metavar='kwargs', help='kwargs in key=value format')

    parser.add_argument('--broker', required=False, default='',
                        metavar='kwargs', help='kwargs in key=value format')

    parser.add_argument('--sizer', required=False, default='',
                        metavar='kwargs', help='kwargs in key=value format')

    parser.add_argument('--strat', required=False, default='',
                        metavar='kwargs', help='kwargs in key=value format')

    parser.add_argument('--plot', required=False, default='',
                        nargs='?', const='{}',
                        metavar='kwargs', help='kwargs in key=value format')

    return parser.parse_args(pargs)


if __name__ == '__main__':
    runstrat()
示例源代码 scheduled-min.py#
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse
import datetime

import backtrader as bt


class St(bt.Strategy):
    params = dict(
        when=bt.timer.SESSION_START,
        timer=True,
        cheat=False,
        offset=datetime.timedelta(),
        repeat=datetime.timedelta(),
        weekdays=[],
        weekcarry=False,
        monthdays=[],
        monthcarry=True,
    )

    def __init__(self):
        bt.ind.SMA()
        if self.p.timer:
            self.add_timer(
                when=self.p.when,
                offset=self.p.offset,
                repeat=self.p.repeat,
                weekdays=self.p.weekdays,
                weekcarry=self.p.weekcarry,
                monthdays=self.p.monthdays,
                monthcarry=self.p.monthcarry,
                # tzdata=self.data0,
            )
        if self.p.cheat:
            self.add_timer(
                when=self.p.when,
                offset=self.p.offset,
                repeat=self.p.repeat,
                weekdays=self.p.weekdays,
                weekcarry=self.p.weekcarry,
                monthdays=self.p.monthdays,
                monthcarry=self.p.monthcarry,
                # tzdata=self.data0,
                cheat=True,
            )

        self.order = None

    def prenext(self):
        self.next()

    def next(self):
        _, isowk, isowkday = self.datetime.date().isocalendar()
        txt = '{}, {}, Week {}, Day {}, O {}, H {}, L {}, C {}'.format(
            len(self), self.datetime.datetime(),
            isowk, isowkday,
            self.data.open[0], self.data.high[0],
            self.data.low[0], self.data.close[0])

        print(txt)

    def notify_timer(self, timer, when, *args, **kwargs):
        print('strategy notify_timer with tid {}, when {} cheat {}'.
              format(timer.p.tid, when, timer.p.cheat))

        if self.order is None and timer.params.cheat:
            print('-- {} Create buy order'.format(
                self.data.datetime.datetime()))
            self.order = self.buy()

    def notify_order(self, order):
        if order.status == order.Completed:
            print('-- {} Buy Exec @ {}'.format(
                self.data.datetime.datetime(), order.executed.price))


def runstrat(args=None):
    args = parse_args(args)
    cerebro = bt.Cerebro()

    # 数据源 kwargs
    kwargs = dict(
        timeframe=bt.TimeFrame.Minutes,
        compression=5,
        sessionstart=datetime.time(9, 0),
        sessionend=datetime.time(17, 30),
    )

    # 解析 from/to-date
    dtfmt, tmfmt = '%Y-%m-%d', 'T%H:%M:%S'
    for a, d in ((getattr(args, x), x) for x in ['fromdate', 'todate']):
        if a:
            strpfmt = dtfmt + tmfmt * ('T' in a)
            kwargs[d] = datetime.datetime.strptime(a, strpfmt)

    # 数据源
    data0 = bt.feeds.BacktraderCSVData(dataname=args.data0, **kwargs)
    cerebro.adddata(data0)

    # 经纪人
    cerebro.broker = bt.brokers.BackBroker(**eval('dict(' + args.broker + ')'))

    # 调整器
    cerebro.addsizer(bt.sizers.FixedSize, **eval('dict(' + args.sizer + ')'))

    # 策略
    cerebro.addstrategy(St, **eval('dict(' + args.strat + ')'))

    # 执行
    cerebro.run(**eval('dict(' + args.cerebro + ')'))

    if args.plot:  # 如果请求则绘图
        cerebro.plot(**eval('dict(' + args.plot + ')'))


def parse_args(pargs=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=(
            'Timer Test Intraday'
        )
    )

    parser.add_argument('--data0', default='../../datas/2006-min-005.txt',
                        required=False, help='Data to read in')

    # 日期默认值
    parser.add_argument('--fromdate', required=False, default='',
                        help='Date[time] in YYYY-MM-DD[THH:MM:SS] format')

    parser.add_argument('--todate', required=False, default='',
                        help='Date[time] in YYYY-MM-DD[THH:MM:SS] format')

    parser.add_argument('--cerebro', required=False, default='',
                        metavar='kwargs', help='kwargs in key=value format')

    parser.add_argument('--broker', required=False, default='',
                        metavar='kwargs', help='kwargs in key=value format')

    parser.add_argument('--sizer', required=False, default='',
                        metavar='kwargs', help='kwargs in key=value format')

    parser.add_argument('--strat', required=False, default='',
                        metavar='kwargs', help='kwargs in key=value format')

    parser.add_argument('--plot', required=False, default='',
                        nargs='?', const='{}',
                        metavar='kwargs', help='kwargs in key=value format')

    return parser.parse_args(pargs)


if __name__ == '__main__':
    runstrat()
#####################################################################################################################################
交易日历#
版本 1.9.42.116 增加了对交易日历的支持。这在以下场景中的重采样时非常有用：

从每日到每周的重采样现在可以将每周的K线与本周的最后一根K线一起交付。
这是因为交易日历可以识别下一个交易日，并且可以提前识别出本周的最后一个交易日。
当交易会话的结束时间不是常规时间（可以通过数据源来指定）时，从子日内到每日的重采样。
交易日历接口#
有一个基类 TradingCalendarBase 用作任何交易日历的基类。它定义了两个必须被重写的方法：

class TradingCalendarBase(with_metaclass(MetaParams, object)):
    def _nextday(self, day):
        '''
        返回在 `day`（datetime/date 实例）之后的下一个交易日（datetime/date 实例）以及 isocalendar 组件。
        返回值是一个包含两个组件的元组：(nextday, (y, w, d))，其中 (y, w, d)。
        '''
        raise NotImplementedError

    def schedule(self, day):
        '''
        返回给定日期（datetime/date 实例）的开盘和收盘时间（`datetime.time`）。
        '''
        raise NotImplementedError
实现#
PandasMarketCalendar#
这个实现基于一个不错的包，这是从 Quantopian 的初始功能衍生出来的。包位于 pandas_market_calendars，可以很容易地安装：

pip install pandas_market_calendars
实现的接口如下：

class PandasMarketCalendar(TradingCalendarBase):
    '''
    `pandas_market_calendars` 的交易日历包装器。必须安装 `pandas_market_calendar` 包。

    参数：

      - `calendar` (默认 `None`)

        参数 `calendar` 接受以下内容：

        - 字符串：支持的日历名称，例如 `NYSE`。包装器会尝试获取一个日历实例。
        - 日历实例：由 `get_calendar('NYSE')` 返回。

      - `cachesize` (默认 `365`)

        缓存查找提前天数。

    参见：

      - https://github.com/rsheftel/pandas_market_calendars
      - http://pandas-market-calendars.readthedocs.io/
    '''
    params = (
        ('calendar', None),  # 一个 pandas_market_calendars 实例或交易所名称
        ('cachesize', 365),  # 缓存查找提前天数
    )
TradingCalendar#
这个实现允许通过指定假期、早市天数、非交易工作日以及开盘和收盘时间来构建一个日历：

class TradingCalendar(TradingCalendarBase):
    '''
    交易日历的包装器。必须安装 `pandas_market_calendars` 包。

    参数：

      - `open` (默认 `time.min`)

        常规开盘时间。

      - `close` (默认 `time.max`)

        常规收盘时间。

      - `holidays` (默认 `[]`)

        非交易日列表（`datetime.datetime` 实例）。

      - `earlydays` (默认 `[]`)

        确定日期和开盘/收盘时间的不符合常规交易时间的天数列表，每个元组包含 (`datetime.datetime`, `datetime.time`, `datetime.time`)。

      - `offdays` (默认 `ISOWEEKEND`)

        一周中市场不交易的工作日的 ISO 格式列表（周一：1 -> 周日：7）。这通常是周六和周日，因此为默认值。
    '''
    params = (
        ('open', time.min),
        ('close', _time_max),
        ('holidays', []),  # 非交易日列表（日期）
        ('earlydays', []),  # 元组列表（日期，开盘时间，收盘时间）
        ('offdays', ISOWEEKEND),  # 非交易日列表（ISO 工作日）
    )
使用模式#
全局交易日历#
通过 Cerebro，可以添加一个全局日历，作为所有数据源的默认日历，除非为数据源指定了一个日历：

def addcalendar(self, cal):
    '''向系统添加全局交易日历。个别数据源可以有单独的日历覆盖全局日历。

    `cal` 可以是 `TradingCalendar` 的一个实例、一个字符串或一个 `pandas_market_calendars` 的实例。字符串将被实例化为 `PandasMarketCalendar`（需要在系统中安装 `pandas_market_calendar` 模块）。

    如果传递的是 `TradingCalendarBase` 的子类（而不是实例），则会被实例化。
    '''
每个数据源#
通过指定一个 calendar 参数，遵循与上面描述的 addcalendar 相同的约定。例如：

...
data = bt.feeds.YahooFinanceData(dataname='YHOO', calendar='NYSE', ...)
cerebro.adddata(data)
...
示例#
从每日到每周#
让我们看一个示例代码的运行结果。2016 年的复活节星期五（2016-03-25）也是纽约证券交易所的假期。如果运行没有交易日历的示例代码，让我们看看该日期前后的情况。

在这种情况下，重采样是从每日到每周（使用 YHOO 和 2016 年的每日数据）：

$ ./tcal.py

...
Strategy len 56 datetime 2016-03-23 Data0 len 56 datetime 2016-03-23 Data1 len 11 datetime 2016-03-18
Strategy len 57 datetime 2016-03-24 Data0 len 57 datetime 2016-03-24 Data1 len 11 datetime 2016-03-18
Strategy len 58 datetime 2016-03-28 Data0 len 58 datetime 2016-03-28 Data1 len 12 datetime 2016-03-24
...
在这个输出中，第一个日期是由策略计算的日期。第二个日期是每日数据的日期。

如预期的那样，周在 2016-03-24（星期四）结束，但是由于没有交易日历，重采样代码无法知道这一点，并且会在 2016-03-18（前一周）的日期交付重采样条形图。当交易移至 2016-03-28（星期一）时，重采样器检测到周变化，并在 2016-03-24 交付一个重采样条形图。

如果使用 NYSE 的 PandasMarketCalendar 并添加一个绘图，再次运行：

$ ./tcal.py --plot --pandascal NYSE

...
Strategy len 56 datetime 2016-03-23 Data0 len 56 datetime 2016-03-23 Data1 len 11 datetime 2016-03-18
Strategy len 57 datetime 2016-03-24 Data0 len 57 datetime 2016-03-24 Data1 len 12 datetime 2016-03-24
Strategy len 58 datetime 2016-03-28 Data0 len 58 datetime 2016-03-28 Data1 len 12 datetime 2016-03-24
...
有所变化！由于有日历，重采样器知道周在 2016-03-24 结束，并在同一天交付相应的每周重采样条形图。

绘图结果如下。

image

由于某些信息可能并不总是可用，可以手动编写日历。对于 NYSE 和 2016 年，日历定义如下：

class NYSE_2016(bt.TradingCalendar):
    params = dict(
        holidays=[
            datetime.date(2016, 1, 1),
            datetime.date(2016, 1, 18),
            datetime.date(2016, 2, 15),
            datetime.date(2016, 3, 25),
            datetime.date(2016, 5, 30),
            datetime.date(2016, 7, 4),
            datetime.date(2016, 9, 5),
            datetime.date(2016, 11, 24),
            datetime.date(2016, 12, 26),
        ]
    )
复活节星期五（2016-03-25）被列为假期之一。现在运行示例代码：

$ ./tcal.py --plot --owncal

...
Strategy len 56 datetime 2016-03-23 Data0 len 56 datetime 2016-03-23 Data1 len 11 datetime 2016-03-18
Strategy len 57 datetime 2016-03-24 Data0 len 57 datetime 2016-03-24 Data1 len 12 datetime 2016-03-24
Strategy len 58 datetime 2016-03-28 Data0 len 58 datetime 2016-03-28 Data1 len 12 datetime 201

6-03-24
...
使用手动编写的日历定义得到了相同的结果。

从分钟到每日#
使用一些私有的日内数据，并且知道市场在 2016-11-25 提前收盘（感恩节后的第二天市场在美国东部时间 13:00 收盘），再进行一个测试运行，这次使用第二个示例。

注意

源数据直接来自显示数据，并且在 CET 时区，即使标的资产 YHOO 在美国交易。代码中使用了 tzinput='CET' 和 tz='US/Eastern' 来让平台适当地转换输入并显示输出。

首先，不使用交易日历：

$ ./tcal-intra.py

...
Strategy len 6838 datetime 2016-11-25 18:00:00 Data0 len 6838 datetime 2016-11-25 13:00:00 Data1 len 21 datetime 2016-11-23 16:00:00
Strategy len 6839 datetime 2016-11-25 18:01:00 Data0 len 6839 datetime 2016-11-25 13:01:00 Data1 len 21 datetime 20 16-11-23 16:00:00
Strategy len 6840 datetime 2016-11-28 14:31:00 Data0 len 6840 datetime 2016-11-28 09:31:00 Data1 len 22 datetime 2016-11-25 16:00:00
Strategy len 6841 datetime 2016-11-28 14:32:00 Data0 len 6841 datetime 2016-11-28 09:32:00 Data1 len 22 datetime 2016-11-25 16:00:00
...
如预期的那样，这一天在 13:00 提前结束，但重采样器不知道这一点（官方会话在 16:00 结束），并继续交付前一天（2016-11-23）的重采样日线图，新重采样日线图首次在下一个交易日（2016-11-28）交付，日期为 2016-11-25。

注意

数据在 13:01 有一个额外的分钟条，这可能是由于拍卖过程中在市场关闭时间后提供的最后价格。

我们可以向流中添加一个过滤器，以过滤掉会话时间之外的条形图（过滤器将从交易日历中找出时间）。

但这不是此示例的重点。

使用 PandasMarketCalendar 实例再次运行：

$ ./tcal-intra.py --pandascal NYSE

...
Strategy len 6838 datetime 2016-11-25 18:00:00 Data0 len 6838 datetime 2016-11-25 13:00:00 Data1 len 15 datetime 2016-11-25 13:00:00
Strategy len 6839 datetime 2016-11-25 18:01:00 Data0 len 6839 datetime 2016-11-25 13:01:00 Data1 len 15 datetime 2016-11-25 13:00:00
Strategy len 6840 datetime 2016-11-28 14:31:00 Data0 len 6840 datetime 2016-11-28 09:31:00 Data1 len 15 datetime 2016-11-25 13:00:00
Strategy len 6841 datetime 2016-11-28 14:32:00 Data0 len 6841 datetime 2016-11-28 09:32:00 Data1 len 15 datetime 2016-11-25 13:00:00
...
现在，当日线条在 2016-11-25 的 13:00 交付时（忽略 13:01 的条形图），重采样代码通过交易日历知道这一天结束了。

让我们添加一个手动编写的定义。与前面的相同，但扩展了一些早市天数：

class NYSE_2016(bt.TradingCalendar):
    params = dict(
        holidays=[
            datetime.date(2016, 1, 1),
            datetime.date(2016, 1, 18),
            datetime.date(2016, 2, 15),
            datetime.date(2016, 3, 25),
            datetime.date(2016, 5, 30),
            datetime.date(2016, 7, 4),
            datetime.date(2016, 9, 5),
            datetime.date(2016, 11, 24),
            datetime.date(2016, 12, 26),
        ],
        earlydays=[
            (datetime.date(2016, 11, 25),
             datetime.time(9, 30), datetime.time(13, 1))
        ],
        open=datetime.time(9, 30),
        close=datetime.time(16, 0),
    )
运行：

$ ./tcal-intra.py --owncal

...
Strategy len 6838 datetime 2016-11-25 18:00:00 Data0 len 6838 datetime 2016-11-25 13:00:00 Data1 len 16 datetime 2016-11-25 13:01:00
Strategy len 6839 datetime 2016-11-25 18:01:00 Data0 len 6839 datetime 2016-11-25 13:01:00 Data1 len 16 datetime 2016-11-25 13:01:00
Strategy len 6840 datetime 2016-11-28 14:31:00 Data0 len 6840 datetime 2016-11-28 09:31:00 Data1 len 16 datetime 2016-11-25 13:01:00
Strategy len 6841 datetime 2016-11-28 14:32:00 Data0 len 6841 datetime 2016-11-28 09:32:00 Data1 len 16 datetime 2016-11-25 13:01:00
...
细心的读者会注意到手动编写的定义将 2016-11-25 的结束时间定义为 13:01（使用 datetime.time(13, 1)）。这只是为了展示手动编写的 TradingCalendar 如何帮助适应。

现在 2016-11-25 的重采样日线条在 13:01 与 1 分钟条一起交付。

策略的额外奖励#
第一个日期时间，属于策略的，总是在不同的时区，实际上是 UTC。使用这个版本 1.9.42.116，这也可以同步。以下参数已添加到 Cerebro（在实例化期间使用或与 cerebro.run 一起使用：

tz（默认：None）

添加策略的全局时区。参数 tz 可以是：

None：在这种情况下，策略显示的日期时间将是 UTC，这一直是标准行为。
pytz 实例。它将用于将 UTC 时间转换为所选时区。
string。尝试实例化一个 pytz 实例。
integer。使用相应数据在 self.datas 可迭代对象中的相同时区（0 将使用 data0 的时区）。
也可以通过 cerebro.addtz 方法支持：

def addtz(self, tz):
    '''
    这也可以通过参数 `tz` 完成。
    
    添加策略的全局时区。参数 `tz` 可以是：
    
      - `None`：在这种情况下，策略显示的日期时间将是 UTC，这一直是标准行为。
      - `pytz` 实例。它将用于将 UTC 时间转换为所选时区。
      - `string`。尝试实例化一个 `pytz` 实例。
      - `integer`。使用相应数据在 `self.datas` 可迭代对象中的相同时区（`0` 将使用 `data0` 的时区）。
    '''
重复上一次的日内示例运行，并使用 0 作为 tz（与 data0 的时区同步），输出如下，关注与上面相同的日期和时间：

$ ./tcal-intra.py --owncal --cerebro tz=0

...
Strategy len 6838 datetime 2016-11-25 13:00:00 Data0 len 6838 datetime 2016-11-25 13:00:00 Data1 len 15 datetime 2016-11-23 16:00:00
Strategy len 6839 datetime 2016-11-25 13:01:00 Data0 len 6839 datetime 2016-11-25 13:01:00 Data1 len 16 datetime 2016-11-25 13:01:00
Strategy len 6840 datetime 2016-11-28 09:31:00 Data0 len 6840 datetime 2016-11-28 09:31:00 Data

1 len 16 datetime 2016-11-25 13:01:00
Strategy len 6841 datetime 2016-11-28 09:32:00 Data0 len 6841 datetime 2016-11-28 09:32:00 Data1 len 16 datetime 2016-11-25 13:01:00
...
时间戳现在与时区对齐。

示例使用（tcal.py）#
$ ./tcal.py --help
usage: tcal.py [-h] [--data0 DATA0] [--offline] [--fromdate FROMDATE]
               [--todate TODATE] [--cerebro kwargs] [--broker kwargs]
               [--sizer kwargs] [--strat kwargs] [--plot [kwargs]]
               [--pandascal PANDASCAL | --owncal]
               [--timeframe {Weeks,Months,Years}]

Trading Calendar Sample

optional arguments:
  -h, --help            show this help message and exit
  --data0 DATA0         Data to read in (default: YHOO)
  --offline             Read from disk with same name as ticker (default: False)
  --fromdate FROMDATE   Date[time] in YYYY-MM-DD[THH:MM:SS] format (default: 2016-01-01)
  --todate TODATE       Date[time] in YYYY-MM-DD[THH:MM:SS] format (default: 2016-12-31)
  --cerebro kwargs      kwargs in key=value format (default: )
  --broker kwargs       kwargs in key=value format (default: )
  --sizer kwargs        kwargs in key=value format (default: )
  --strat kwargs        kwargs in key=value format (default: )
  --plot [kwargs]       kwargs in key=value format (default: )
  --pandascal PANDASCAL Name of trading calendar to use (default: )
  --owncal              Apply custom NYSE 2016 calendar (default: False)
  --timeframe {Weeks,Months,Years} Timeframe to resample to (default: Weeks)
示例使用（tcal-intra.py）#
$ ./tcal-intra.py --help
usage: tcal-intra.py [-h] [--data0 DATA0] [--fromdate FROMDATE]
                     [--todate TODATE] [--cerebro kwargs] [--broker kwargs]
                     [--sizer kwargs] [--strat kwargs] [--plot [kwargs]]
                     [--pandascal PANDASCAL | --owncal] [--timeframe {Days}]

Trading Calendar Sample

optional arguments:
  -h, --help            show this help message and exit
  --data0 DATA0         Data to read in (default: yhoo-2016-11.csv)
  --fromdate FROMDATE   Date[time] in YYYY-MM-DD[THH:MM:SS] format (default: 2016-01-01)
  --todate TODATE       Date[time] in YYYY-MM-DD[THH:MM:SS] format (default: 2016-12-31)
  --cerebro kwargs      kwargs in key=value format (default: )
  --broker kwargs       kwargs in key=value format (default: )
  --sizer kwargs        kwargs in key=value format (default: )
  --strat kwargs        kwargs in key=value format (default: )
  --plot [kwargs]       kwargs in key=value format (default: )
  --pandascal PANDASCAL Name of trading calendar to use (default: )
  --owncal              Apply custom NYSE 2016 calendar (default: False)
  --timeframe {Days}    Timeframe to resample to (default: Days)
示例代码（tcal.py）#
from __future__ import (absolute_import, division, print_function, unicode_literals)
import argparse
import datetime
import backtrader as bt

class NYSE_2016(bt.TradingCalendar):
    params = dict(
        holidays=[
            datetime.date(2016, 1, 1),
            datetime.date(2016, 1, 18),
            datetime.date(2016, 2, 15),
            datetime.date(2016, 3, 25),
            datetime.date(2016, 5, 30),
            datetime.date(2016, 7, 4),
            datetime.date(2016, 9, 5),
            datetime.date(2016, 11, 24),
            datetime.date(2016, 12, 26),
        ]
    )

class St(bt.Strategy):
    params = dict()

    def __init__(self):
        pass

    def start(self):
        self.t0 = datetime.datetime.utcnow()

    def stop(self):
        t1 = datetime.datetime.utcnow()
        print('Duration:', t1 - self.t0)

    def prenext(self):
        self.next()

    def next(self):
        print('Strategy len {} datetime {}'.format(len(self), self.datetime.date()), end=' ')
        print('Data0 len {} datetime {}'.format(len(self.data0), self.data0.datetime.date()), end=' ')
        if len(self.data1):
            print('Data1 len {} datetime {}'.format(len(self.data1), self.data1.datetime.date()))
        else:
            print()

def runstrat(args=None):
    args = parse_args(args)
    cerebro = bt.Cerebro()

    # 数据源参数
    kwargs = dict()

    # 解析 from/to 日期
    dtfmt, tmfmt = '%Y-%m-%d', 'T%H:%M:%S'
    for a, d in ((getattr(args, x), x) for x in ['fromdate', 'todate']):
        if a:
            strpfmt = dtfmt + tmfmt * ('T' in a)
            kwargs[d] = datetime.datetime.strptime(a, strpfmt)

    YahooData = bt.feeds.YahooFinanceData
    if args.offline:
        YahooData = bt.feeds.YahooFinanceCSVData  # 切换为从文件读取

    # 数据源
    data0 = YahooData(dataname=args.data0, **kwargs)
    cerebro.adddata(data0)

    d1 = cerebro.resampledata(data0, timeframe=getattr(bt.TimeFrame, args.timeframe))
    d1.plotinfo.plotmaster = data0
    d1.plotinfo.sameaxis = True

    if args.pandascal:
        cerebro.addcalendar(args.pandascal)
    elif args.owncal:
        cerebro.addcalendar(NYSE_2016)

    # 经纪商
    cerebro.broker = bt.brokers.BackBroker(**eval('dict(' + args.broker + ')'))

    # 大小调整器
    cerebro.addsizer(bt.sizers.FixedSize, **eval('dict(' + args.sizer + ')'))

    # 策略
    cerebro.addstrategy(St, **eval('dict(' + args.strat + ')'))

    # 执行
    cerebro.run(**eval('dict(' + args.cerebro + ')'))

    if args.plot:  # 如果请求则绘图
        cerebro.plot(**eval('dict(' + args.plot + ')'))

def parse_args(pargs=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=(
            'Trading Calendar Sample'
        )
    )

    parser.add_argument('--data0', default='YHOO', required=False, help='Data to read in')
    parser.add_argument('--offline', required=False, action='store_true', help='Read from disk with same name as ticker')

    # 日期默认值
    parser.add_argument('--fromdate', required=False, default='2016-01-01', help='Date[time] in YYYY-MM-DD[THH:MM:SS] format')
    parser.add_argument('--todate', required=False, default='2016-12-31', help='Date[time] in YYYY-MM-DD[THH:MM:SS] format')

    parser.add_argument('--cerebro', required=False, default='', metavar='kwargs', help='kwargs in key=value format')
    parser.add_argument('--broker', required=False, default='', metavar='kwargs', help='kwargs in key=value format')
    parser.add_argument('--sizer', required=False, default='', metavar='kwargs', help='kwargs in key=value format')
    parser.add_argument('--strat', required=False, default='', metavar='kwargs', help='kwargs in key=value format')
    parser.add_argument('--plot', required=False, default='', nargs='?', const='{}', metavar='kwargs', help='kwargs in key=value format')

    pgroup = parser.add_mutually_exclusive_group(required=False)
    pgroup.add_argument('--pandascal', required=False, action='store', default='', help='Name of trading calendar to use')
    pgroup.add_argument('--owncal', required=False, action='store_true', help='Apply custom NYSE 2016 calendar')

    parser.add_argument('--timeframe', required=False, action='store', default='Weeks', choices=['Weeks', 'Months', 'Years'], help='Timeframe to resample to')

    return parser.parse_args(pargs)

if __name__ == '__main__':
    runstrat()
示例代码（tcal-intra.py）#
from __future__ import (absolute_import, division, print_function, unicode_literals)
import argparse
import datetime
import backtrader as bt

class NYSE_2016(bt.TradingCalendar

):
    params = dict(
        holidays=[
            datetime.date(2016, 1, 1),
            datetime.date(2016, 1, 18),
            datetime.date(2016, 2, 15),
            datetime.date(2016, 3, 25),
            datetime.date(2016, 5, 30),
            datetime.date(2016, 7, 4),
            datetime.date(2016, 9, 5),
            datetime.date(2016, 11, 24),
            datetime.date(2016, 12, 26),
        ],
        earlydays=[
            (datetime.date(2016, 11, 25), datetime.time(9, 30), datetime.time(13, 1))
        ],
        open=datetime.time(9, 30),
        close=datetime.time(16, 0),
    )

class St(bt.Strategy):
    params = dict()

    def __init__(self):
        pass

    def prenext(self):
        self.next()

    def next(self):
        print('Strategy len {} datetime {}'.format(len(self), self.datetime.datetime()), end=' ')
        print('Data0 len {} datetime {}'.format(len(self.data0), self.data0.datetime.datetime()), end=' ')
        if len(self.data1):
            print('Data1 len {} datetime {}'.format(len(self.data1), self.data1.datetime.datetime()))
        else:
            print()

def runstrat(args=None):
    args = parse_args(args)
    cerebro = bt.Cerebro()

    # 数据源参数
    # kwargs = dict(tz='US/Eastern')
    # import pytz
    # tz = tzinput = pytz.timezone('Europe/Berlin')
    tzinput = 'Europe/Berlin'
    # tz = tzinput
    tz = 'US/Eastern'
    kwargs = dict(tzinput=tzinput, tz=tz)

    # 解析 from/to 日期
    dtfmt, tmfmt = '%Y-%m-%d', 'T%H:%M:%S'
    for a, d in ((getattr(args, x), x) for x in ['fromdate', 'todate']):
        if a:
            strpfmt = dtfmt + tmfmt * ('T' in a)
            kwargs[d] = datetime.datetime.strptime(a, strpfmt)

    # 数据源
    data0 = bt.feeds.BacktraderCSVData(dataname=args.data0, **kwargs)
    cerebro.adddata(data0)

    d1 = cerebro.resampledata(data0, timeframe=getattr(bt.TimeFrame, args.timeframe))
    # d1.plotinfo.plotmaster = data0
    # d1.plotinfo.sameaxis = False

    if args.pandascal:
        cerebro.addcalendar(args.pandascal)
    elif args.owncal:
        cerebro.addcalendar(NYSE_2016())  # 或者 NYSE_2016() 传递一个实例

    # 经纪商
    cerebro.broker = bt.brokers.BackBroker(**eval('dict(' + args.broker + ')'))

    # 大小调整器
    cerebro.addsizer(bt.sizers.FixedSize, **eval('dict(' + args.sizer + ')'))

    # 策略
    cerebro.addstrategy(St, **eval('dict(' + args.strat + ')'))

    # 执行
    cerebro.run(**eval('dict(' + args.cerebro + ')'))

    if args.plot:  # 如果请求则绘图
        cerebro.plot(**eval('dict(' + args.plot + ')'))

def parse_args(pargs=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=(
            'Trading Calendar Sample'
        )
    )

    parser.add_argument('--data0', default='yhoo-2016-11.csv', required=False, help='Data to read in')

    # 日期默认值
    parser.add

37 47自动运行.txt ##################################################
文件路径: 47自动运行.txt
================================================================================

自动运行#
到目前为止，所有 backtrader 示例和工作样本都从头开始创建一个主 Python 模块，该模块加载数据、策略、观察器，并准备现金和佣金方案。

算法交易的目标之一是自动化交易，而 backtrader 作为一个回测平台，旨在检查交易算法（因此是一个算法交易平台），自动化使用 backtrader 是一个显而易见的目标。

安装 backtrader 后，它提供了两个脚本/可执行文件形式的入口点，自动化大多数任务：

bt-run-py：一个使用下一个条目中的代码库的脚本。
btrun（可执行文件）：由 setuptools 在打包时创建的入口点。该可执行文件在 Windows 下具有优势，理论上不会出现“找不到路径/文件”的错误。
下面的描述适用于这两个工具。

btrun 允许最终用户：

指定要加载的数据源
设置加载数据的格式
指定数据的日期范围
传递参数给 Cerebro
禁用标准观察器
这是一个原始的额外开关，在实现“Cerebro”参数之前。因此，如果传递了与标准观察器相关的参数给 Cerebro，将忽略此参数（参数 stdstats 给 Cerebro）
从内置或 Python 模块加载一个或多个观察器（例如：DrawDown）
设置经纪商的现金和佣金方案参数（佣金、保证金、倍数）
启用绘图，控制图表的数量和样式
向系统添加一个参数化的 writer
最后是核心功能：加载一个策略（内置或来自 Python 模块）
传递参数给加载的策略
请参阅下面的脚本用法。

应用用户定义策略#
考虑以下策略，它：

简单加载一个简单移动平均线（默认周期为 15）
打印输出
存在于名为 mymod.py 的文件中
from __future__ import (absolute_import, division, print_function, unicode_literals)

import backtrader as bt
import backtrader.indicators as btind

class MyTest(bt.Strategy):
    params = (('period', 15),)

    def log(self, txt, dt=None):
        '''策略的日志记录函数'''
        dt = dt或self.data.datetime[0]
        if isinstance(dt, float):
            dt = bt.num2date(dt)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        sma = btind.SMA(period=self.p.period)

    def next(self):
        ltxt = '%d, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f'

        self.log(ltxt %
                 (len(self),
                  self.data.open[0], self.data.high[0],
                  self.data.low[0], self.data.close[0],
                  self.data.volume[0], self.data.openinterest[0]))
使用常规测试示例执行策略非常简单：

btrun --csvformat btcsv \
      --data ../../datas/2006-day-001.txt \
      --strategy mymod.py
图表输出：

Chart Output

控制台输出：

2006-01-20T23:59:59+00:00, 15, 3593.16, 3612.37, 3550.80, 3550.80, 0.00, 0.00
2006-01-23T23:59:59+00:00, 16, 3550.24, 3550.24, 3515.07, 3544.31, 0.00, 0.00
2006-01-24T23:59:59+00:00, 17, 3544.78, 3553.16, 3526.37, 3532.68, 0.00, 0.00
2006-01-25T23:59:59+00:00, 18, 3532.72, 3578.00, 3532.72, 3578.00, 0.00, 0.00
...
2006-12-22T23:59:59+00:00, 252, 4109.86, 4109.86, 4072.62, 4073.50, 0.00, 0.00
2006-12-27T23:59:59+00:00, 253, 4079.70, 4134.86, 4079.70, 4134.86, 0.00, 0.00
2006-12-28T23:59:59+00:00, 254, 4137.44, 4142.06, 4125.14, 4130.66, 0.00, 0.00
2006-12-29T23:59:59+00:00, 255, 4130.12, 4142.01, 4119.94, 4119.94, 0.00, 0.00
相同策略，但将参数 period 设置为 50 的命令行：

btrun --csvformat btcsv \
      --data ../../datas/2006-day-001.txt \
      --plot \
      --strategy mymod.py:period=50
图表输出：

Chart Output

注意：如果没有提供 .py 扩展名，bt-run 会自动添加它。

使用内置策略#
backtrader 将逐步包括一些示例（教科书）策略。与 bt-run.py 脚本一起，包含了一个标准的简单移动平均交叉策略。名称为 SMA_CrossOver。

参数#
fast（默认 10）：快速移动平均线的周期
slow（默认 30）：慢速移动平均线的周期
该策略在快速移动平均线上穿慢速移动平均线时买入，并在快速移动平均线下穿慢速移动平均线时卖出（仅在之前已买入的情况下）。

代码如下：

from __future__ import (absolute_import, division, print_function, unicode_literals)

import backtrader as bt
import backtrader.indicators as btind

class SMA_CrossOver(bt.Strategy):
    params = (('fast', 10), ('slow', 30))

    def __init__(self):
        sma_fast = btind.SMA(period=self.p.fast)
        sma_slow = btind.SMA(period=self.p.slow)
        self.buysig = btind.CrossOver(sma_fast, sma_slow)

    def next(self):
        if self.position.size:
            if self.buysig < 0:
                self.sell()
        elif self.buysig > 0:
            self.buy()
标准执行：

btrun --csvformat btcsv \
      --data ../../datas/2006-day-001.txt \
      --plot \
      --strategy :SMA_CrossOver
注意 :。标准的加载策略表示法为：module:strategy:kwargs。规则如下：

如果指定了 module 和 strategy，则使用该策略。
如果指定了 module 但未指定 strategy，则使用模块中找到的第一个策略。
如果未指定 module，则“strategy”被视为 backtrader 包中的策略。
如果指定了 module 和/或 strategy，如果存在 kwargs，它们将传递给相应的策略。
注意：相同的表示法和规则适用于 --observer、--analyzer 和 --indicator 选项，显然适用于相应的对象类型。

输出结果：

Chart Output

最后一个示例，添加佣金方案、现金并更改参数：

btrun --csvformat btcsv \
      --data ../../datas/2006-day-001.txt \
      --plot \
      --cash 20000 \
      --commission 2.0 \
      --mult 10 \
      --margin 2000 \
      --strategy :SMA_CrossOver:fast=5,slow=20
输出结果：

Chart Output

我们已经回测了策略：

更改移动平均线周期
设置新的起始现金
为类似期货的工具设置佣金方案
观察每个条的现金持续变化，因为现金根据类似期货工具的每日变化进行调整。

使用无策略#
这是一个夸张的说法。会应用一个策略，但您可以省略任何类型的策略，会自动添加一个默认的 backtrader.Strategy。

分析器、观察器和指标将自动注入策略中。

例如：

btrun --csvformat btcsv \
      --data ../../datas/2006-day-001.txt \
      --cash 20000 \
      --commission 2.0 \
      --mult 10 \
      --margin 2000 \
      --nost

dstats \
      --observer :Broker
这不会做很多事情，但可以实现以下目的：

在后台添加一个默认的 backtrader.Strategy
Cerebro 不会实例化常规的 stdstats 观察器（Broker、BuySell、Trades）
手动添加一个 Broker 观察器
如上所述，nostdstats 是一个遗留参数。更新版本的 btrun 可以将参数直接传递给 Cerebro。等效调用如下：

btrun --csvformat btcsv \
      --data ../../datas/2006-day-001.txt \
      --cash 20000 \
      --commission 2.0 \
      --mult 10 \
      --margin 2000 \
      --cerebro stdstats=False \
      --observer :Broker
添加分析器#
btrun 还支持使用与选择内部/外部分析器相同的语法添加分析器。

例如，对 2005-2006 年进行夏普比率分析：

btrun --csvformat btcsv \
      --data ../../datas/2005-2006-day-001.txt \
      --strategy :SMA_CrossOver \
      --analyzer :SharpeRatio
控制台输出为空。

如果希望打印分析器结果，必须指定：

--pranalyzer，默认调用下一个（除非分析器覆盖了适当的方法）
--ppranalyzer，使用 pprint 模块打印结果
注意：这两个打印选项在 writers 成为 backtrader 的一部分之前实现。添加一个 writer 而不输出 CSV 将实现相同的效果（并且输出得到了改进）。

扩展上述示例：

btrun --csvformat btcsv \
      --data ../../datas/2005-2006-day-001.txt \
      --strategy :SMA_CrossOver \
      --analyzer :SharpeRatio \
      --plot \
      --pranalyzer

====================
== Analyzers
====================
##########
sharperatio
##########
{'sharperatio': 11.647332609673256}
好策略！（实际上纯属运气，示例中没有考虑佣金）

图表（仅显示分析器未在图表中绘制，因为分析器无法绘制，它们不是线条对象）：

Chart Output

使用 writer 参数的相同示例：

btrun --csvformat btcsv \
      --data ../../datas/2005-2006-day-001.txt \
      --strategy :SMA_CrossOver \
      --analyzer :SharpeRatio \
      --plot \
      --writer

===============================================================================
Cerebro:
  -----------------------------------------------------------------------------
  - Datas:
    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    - Data0:
      - Name: 2005-2006-day-001
      - Timeframe: Days
      - Compression: 1
  -----------------------------------------------------------------------------
  - Strategies:
    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    - SMA_CrossOver:
      *************************************************************************
      - Params:
        - fast: 10
        - slow: 30
        - _movav: SMA
      *************************************************************************
      - Indicators:
        .......................................................................
        - SMA:
          - Lines: sma
          ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
          - Params:
            - period: 30
        .......................................................................
        - CrossOver:
          - Lines: crossover
          - Params: None
      *************************************************************************
      - Observers:
        .......................................................................
        - Broker:
          - Lines: cash, value
          - Params: None
        .......................................................................
        - BuySell:
          - Lines: buy, sell
          - Params: None
        .......................................................................
        - Trades:
          - Lines: pnlplus, pnlminus
          - Params: None
      *************************************************************************
      - Analyzers:
        .......................................................................
        - Value:
          - Begin: 10000.0
          - End: 10496.68
        .......................................................................
        - SharpeRatio:
          - Params: None
          ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
          - Analysis:
            - sharperatio: 11.6473326097
添加指标和观察器#
与策略和分析器相同，btrun 还可以添加：

指标
观察器
语法与上面添加 Broker 观察器时所见完全相同。

让我们重复示例，添加一个随机指标、Broker 并查看图表（我们将更改一些参数）：

btrun --csvformat btcsv \
      --data ../../datas/2006-day-001.txt \
      --nostdstats \
      --observer :Broker \
      --indicator :Stochastic:period_dslow=5 \
      --plot
图表：

Chart Output

绘图控制#
上面大多数示例都使用了以下选项：

--plot：激活创建默认图表 更多控制可以通过向 --plot 选项添加 kwargs 实现

--plot style="candle" 例如，使用蜡烛图而不是 LineOnClose 样式（这是绘图默认值） 调用如下：

btrun --csvformat btcsv \
      --data ../../datas/2006-day-001.txt \
      --nostdstats \
      --observer :Broker \
      --indicator :Stochastic:period_dslow=5 \
      --plot style=\"candle\"
注意：示例在 bash shell 中运行，传递参数给脚本之前会去除引号，因此需要使用反斜杠转义 \" 确保 candle 作为字符串传递。

图表：

Chart Output

脚本用法#
直接从脚本：

$ btrun --help
usage: btrun-script.py [-h] --data DATA [--cerebro [kwargs]] [--nostdstats]
                       [--format {yahoocsv_unreversed,vchart,vchartcsv,yahoo,mt4csv,ibdata,sierracsv,yahoocsv,btcsv,vcdata}]
                       [--fromdate FROMDATE] [--todate TODATE]
                       [--timeframe {microseconds,seconds,weeks,months,minutes,days,years}]
                       [--compression COMPRESSION]
                       [--resample RESAMPLE | --replay REPLAY]
                       [--strategy module:name:kwargs]
                       [--signal module:signaltype:name:kwargs]
                       [--observer module:name:kwargs]
                       [--analyzer module:name:kwargs]
                       [--pranalyzer | --ppranalyzer]
                       [--indicator module:name:kwargs] [--writer [kwargs]]
                       [--cash CASH] [--commission COMMISSION]
                       [--margin MARGIN] [--mult MULT] [--interest INTEREST]
                       [--interest_long] [--slip_perc SLIP_PERC]
                       [--slip_fixed SLIP_FIXED] [--slip_open]
                       [--no-slip_match] [--slip_out] [--flush]
                       [--plot [kwargs]]

Backtrader Run Script

optional arguments:
  -h, --help            show this help message and exit
  --resample RESAMPLE, -rs RESAMPLE
                        resample with timeframe:compression values
  --replay REPLAY, -rp REPLAY
                        replay with timeframe:compression values
  --pranalyzer, -pralyzer
                        Automatically print analyzers
  --ppranalyzer, -ppralyzer
                        Automatically PRETTY print analyzers
  --plot [kwargs], -p [kwargs]
                        Plot the read data applying any kwargs passed

                        For example:

                          --plot style="candle" (to plot candlesticks)

Data options:
  --data DATA, -d DATA  Data files to be added to the system

Cerebro options:
  --cerebro [kwargs], -cer [kwargs]
                        The argument can be specified with the following form:

                          - kwargs

                            Example: "preload=True" which set its to True

                        The passed kwargs will be passed directly to the cerebro
                        instance created for the execution

                        The available kwargs to cerebro are:
                          - preload (default: True)
                          - runonce (default: True)
                          - maxcpus (default: None)
                          - stdstats (default: True)
                          - live (default: False)
                          - exactbars (default: False)
                          - preload (default: True)
                          - writer (default False)
                          - oldbuysell (default False)
                          - tradehistory (default False)
  --nostdstats          Disable the standard statistics observers
  --format {yahoocsv_unreversed,vchart,vchartcsv,yahoo,mt4csv,ibdata,sierracsv,yahoocsv,btcsv,vcdata}, --csvformat {yahoocsv_unreversed,vchart,vchartcsv,yahoo,mt4csv,ibdata,sierracsv,yahoocsv,btcsv,vcdata}, -c {yahoocsv_unreversed,vchart,vchartcsv,yahoo,mt4csv,ibdata,sierracsv,yahoocsv,btcsv,vcdata}
                        CSV Format
  --fromdate FROMDATE, -f FROMDATE
                        Starting date in YYYY-MM-DD[THH:MM:SS] format
 

 --todate TODATE, -t TODATE
                        Ending date in YYYY-MM-DD[THH:MM:SS] format
  --timeframe {microseconds,seconds,weeks,months,minutes,days,years}, -tf {microseconds,seconds,weeks,months,minutes,days,years}
                        Ending date in YYYY-MM-DD[THH:MM:SS] format
  --compression COMPRESSION, -cp COMPRESSION
                        Ending date in YYYY-MM-DD[THH:MM:SS] format

Strategy options:
  --strategy module:name:kwargs, -st module:name:kwargs
                        This option can be specified multiple times.

                        The argument can be specified with the following form:

                          - module:classname:kwargs

                            Example: mymod:myclass:a=1,b=2

                        kwargs is optional

                        If module is omitted then class name will be sought in
                        the built-in strategies module. Such as in:

                          - :name:kwargs or :name

                        If name is omitted, then the 1st strategy found in the mod
                        will be used. Such as in:

                          - module or module::kwargs

Signals:
  --signal module:signaltype:name:kwargs, -sig module:signaltype:name:kwargs
                        This option can be specified multiple times.

                        The argument can be specified with the following form:

                          - signaltype:module:signaltype:classname:kwargs

                            Example: longshort+mymod:myclass:a=1,b=2

                        signaltype may be ommited: longshort will be used

                            Example: mymod:myclass:a=1,b=2

                        kwargs is optional

                        signaltype will be uppercased to match the defintions
                        fromt the backtrader.signal module

                        If module is omitted then class name will be sought in
                        the built-in signals module. Such as in:

                          - LONGSHORT::name:kwargs or :name

                        If name is omitted, then the 1st signal found in the mod
                        will be used. Such as in:

                          - module or module:::kwargs

Observers and statistics:
  --observer module:name:kwargs, -ob module:name:kwargs
                        This option can be specified multiple times.

                        The argument can be specified with the following form:

                          - module:classname:kwargs

                            Example: mymod:myclass:a=1,b=2

                        kwargs is optional

                        If module is omitted then class name will be sought in
                        the built-in observers module. Such as in:

                          - :name:kwargs or :name

                        If name is omitted, then the 1st observer found in the
                        will be used. Such as in:

                          - module or module::kwargs

Analyzers:
  --analyzer module:name:kwargs, -an module:name:kwargs
                        This option can be specified multiple times.

                        The argument can be specified with the following form:

                          - module:classname:kwargs

                            Example: mymod:myclass:a=1,b=2

                        kwargs is optional

                        If module is omitted then class name will be sought in
                        the built-in analyzers module. Such as in:

                          - :name:kwargs or :name

                        If name is omitted, then the 1st analyzer found in the
                        will be used. Such as in:

                          - module or module::kwargs

Indicators:
  --indicator module:name:kwargs, -ind module:name:kwargs
                        This option can be specified multiple times.

                        The argument can be specified with the following form:

                          - module:classname:kwargs

                            Example: mymod:myclass:a=1,b=2

                        kwargs is optional

                        If module is omitted then class name will be sought in
                        the built-in analyzers module. Such as in:

                          - :name:kwargs or :name

                        If name is omitted, then the 1st analyzer found in the
                        will be used. Such as in:

                          - module or module::kwargs

Writers:
  --writer [kwargs], -wr [kwargs]
                        This option can be specified multiple times.

                        The argument can be specified with the following form:

                          - kwargs

                            Example: a=1,b=2

                        kwargs is optional

                        It creates a system wide writer which outputs run data

                        Please see the documentation for the available kwargs

Cash and Commission Scheme Args:
  --cash CASH, -cash CASH
                        Cash to set to the broker
  --commission COMMISSION, -comm COMMISSION
                        Commission value to set
  --margin MARGIN, -marg MARGIN
                        Margin type to set
  --mult MULT, -mul MULT
                        Multiplier to use
  --interest INTEREST   Credit Interest rate to apply (0.0x)
  --interest_long       Apply credit interest to long positions
  --slip_perc SLIP_PERC
                        Enable slippage with a percentage value
  --slip_fixed SLIP_FIXED
                        Enable slippage with a fixed point value
  --slip_open           enable slippage for when matching opening prices
  --no-slip_match       Disable slip_match, ie: matching capped at
                        high-low if slippage goes over those limits
  --slip_out            with slip_match enabled, match outside high-low
  --flush               flush the output - useful under win32 systems

