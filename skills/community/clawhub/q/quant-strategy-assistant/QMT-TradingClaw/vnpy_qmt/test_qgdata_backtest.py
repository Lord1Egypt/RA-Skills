"""qgdata数据源 + VeighNa CTA回测引擎 验证脚本 — 股票双均线策略"""
from datetime import datetime
from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.object import BarData, HistoryRequest
from vnpy.trader.database import get_database
from vnpy_ctastrategy.backtesting import BacktestingEngine
from vnpy_ctastrategy.template import CtaTemplate
from vnpy_xt import Datafeed

# ============ 双均线策略 ============
class DualMaStrategy(CtaTemplate):
    author = "test"
    fast_window = 5
    slow_window = 20
    fast_ma = 0.0
    slow_ma = 0.0
    parameters = ["fast_window", "slow_window"]
    variables = ["fast_ma", "slow_ma"]

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        self.bars: list[BarData] = []

    def on_init(self):
        self.load_bar(10)

    def on_start(self):
        pass

    def on_bar(self, bar: BarData):
        self.bars.append(bar)
        if len(self.bars) > self.slow_window:
            self.bars.pop(0)
        if len(self.bars) < self.slow_window:
            return
        closes = [b.close_price for b in self.bars]
        self.fast_ma = sum(closes[-self.fast_window:]) / self.fast_window
        self.slow_ma = sum(closes[-self.slow_window:]) / self.slow_window
        if self.pos == 0:
            if self.fast_ma > self.slow_ma: #金叉买入
                self.buy(bar.close_price, 100)
        elif self.pos > 0:
            if self.fast_ma < self.slow_ma: #死叉卖出
                self.sell(bar.close_price, 100)

    def on_stop_order(self, stop_order): pass
    def on_order(self, order): pass
    def on_trade(self, trade): pass

# ============ 主流程 ============
if __name__ == "__main__":
    SYMBOL = "000001"
    EXCHANGE = Exchange.SZSE
    VT_SYMBOL = f"{SYMBOL}.{EXCHANGE.value}"
    START = datetime(2025, 1, 1)
    END = datetime(2026, 1, 1)

    # Step1: 用qgdata下载数据到vnpy数据库
    print("=" * 60)
    print("Step1: 通过qgdata下载历史数据")
    print("=" * 60)
    datafeed = Datafeed()
    ok = datafeed.init()
    if not ok:
        print("qgdata初始化失败，退出")
        exit(1)
    print(f"qgdata初始化成功，开始下载 {VT_SYMBOL} 日线数据 {START.date()} ~ {END.date()}")
    req = HistoryRequest(symbol=SYMBOL, exchange=EXCHANGE, interval=Interval.DAILY, start=START, end=END)
    bars = datafeed.query_bar_history(req)
    print(f"下载完成，共 {len(bars)} 根K线")
    if bars:
        print(f"  首根: {bars[0].datetime.date()} O={bars[0].open_price} C={bars[0].close_price} V={bars[0].volume}")
        print(f"  末根: {bars[-1].datetime.date()} O={bars[-1].open_price} C={bars[-1].close_price} V={bars[-1].volume}")

    # Step2: 存入vnpy数据库
    print("\nStep2: 存入vnpy数据库")
    database = get_database()
    database.save_bar_data(bars)
    print(f"已写入 {len(bars)} 条BarData到数据库")

    # Step3: CTA回测
    print("\n" + "=" * 60)
    print("Step3: 运行双均线策略回测")
    print("=" * 60)
    engine = BacktestingEngine()
    engine.set_parameters(
        vt_symbol=VT_SYMBOL,
        interval=Interval.DAILY,
        start=START,
        rate=0.0003,    #手续费万3
        slippage=0.01,  #滑点1分
        size=1,         #股票合约乘数1
        pricetick=0.01, #最小变动价位
        capital=100000, #初始资金10万
        end=END,
    )
    engine.add_strategy(DualMaStrategy, {"fast_window": 5, "slow_window": 20})
    engine.load_data()
    engine.run_backtesting()
    df = engine.calculate_result()
    stats = engine.calculate_statistics(output=True)

    # Step4: 输出核心指标
    print("\n" + "=" * 60)
    print("Step4: 回测结果摘要")
    print("=" * 60)
    if stats:
        for k in ["start_date", "end_date", "total_days", "total_net_pnl",
                   "total_return", "max_drawdown", "max_ddpercent",
                   "total_trade_count", "profit_days", "loss_days",
                   "daily_net_pnl", "sharpe_ratio"]:
            v = stats.get(k, "N/A")
            print(f"  {k}: {v}")
    print("\n✓ qgdata数据源回测验证完成")
