"""
PTRADE 双均线策略
策略逻辑：短期均线上穿长期均线（金叉）买入，下穿（死叉）卖出
周期：日线
适用标的：A股股票
"""
def initialize(context):
    context.params = {
        "security": "000001.XSHG",    # 交易标的（沪深A股）
        "short_window": 5,            # 短期均线周期
        "long_window": 20,             # 长期均线周期
        "trade_unit": 100,             # 每次交易数量（100股=1手）
    }

    # 获取系统对象
    g = get_json("context").get("g", {})
    context.g.security = g.get("security")
    context.g.trade    = g.get("trade")
    context.g.log      = g.get("log")

def handle_data(context):
    security = context.g.security
    trade    = context.g.trade
    log      = context.g.log
    params   = context.params

    # 获取K线数据
    bars = security.get_bars(
        n=params["long_window"] + 5,
        end_date="",
        fields=["open", "high", "low", "close", "volume"],
        count=params["long_window"] + 5,
        period="1d"
    )

    close = bars["close"]
    if close is None or len(close) < params["long_window"]:
        return

    # 计算均线
    short_ma = close[-params["short_window"]:].mean()
    long_ma  = close[-params["long_window"]:].mean()
    prev_short = close[-params["short_window"]-1:-1].mean()
    prev_long  = close[-params["long_window"]-1].mean() if len(close) > params["long_window"] else 0

    # 金叉信号：短期均线从下方上穿长期均线
    if prev_short <= prev_long and short_ma > long_ma:
        log.info(f"【买入信号】{params['security']} 金叉，买入 {params['trade_unit']} 股")
        trade.open_long(params["security"], params["trade_unit"], price=0, price_type="market")

    # 死叉信号：短期均线从上方下穿长期均线
    elif prev_short >= prev_long and short_ma < long_ma:
        log.info(f"【卖出信号】{params['security']} 死叉，卖出 {params['trade_unit']} 股")
        trade.close_long(params["security"], params["trade_unit"], price=0, price_type="market")
