"""
PTRADE 财务因子选股策略
策略逻辑：按 PE 估值因子从沪深300成分股中选取最低估的10只，等权配置，月度调仓
周期：日线（每月检查一次）
适用标的：沪深300成分股
"""
def initialize(context):
    context.params = {
        "index": "000300.XSHG",       # 选股范围：沪深300
        "n": 10,                       # 持仓数量
        "factor": "PE",               # 估值因子：PE | PB | PCF | PS
        "ascending": True,             # True=低估值优先（PE低买）
        "trade_unit": 100,             # 每次买100股
        "rebalance_days": 20,          # 调仓间隔（交易日）
    }

    g = get_json("context").get("g", {})
    context.g.security = g.get("security")
    context.g.trade    = g.get("trade")
    context.g.log      = g.get("log")
    context.g.day_count = 0            # 交易日计数器

def handle_data(context):
    security = context.g.security
    trade    = context.g.trade
    log      = context.g.log
    params   = context.params

    context.g.day_count += 1

    # 每隔 rebalance_days 个交易日调仓一次
    if context.g.day_count % params["rebalance_days"] != 0:
        return

    # 获取指数成分股
    try:
        stocks = security.get_index_stocks(params["index"])
    except Exception as e:
        log.error(f"获取成分股失败: {e}")
        return

    if not stocks:
        return

    # 获取最新财务数据
    try:
        fd = security.get_financial_data(
            start_date="", end_date="",
            count=1,
            fields=[params["factor"], "closePrice"]
        )
    except Exception as e:
        log.error(f"获取财务数据失败: {e}")
        return

    # 过滤无效因子，按因子排序
    valid = [(s, fd.get(s, {}).get(params["factor"], float("inf")))
             for s in stocks
             if fd.get(s, {}).get(params["factor"], 0) > 0]
    valid.sort(key=lambda x: x[1], reverse=not params["ascending"])

    target_stocks = [s for s, _ in valid[:params["n"]]]

    # 清仓旧持仓
    try:
        positions = security.get_positions()
        for pos in positions:
            symbol = pos.get("security")
            volume = pos.get("volume", 0)
            if volume > 0:
                trade.close_long(symbol, volume, price=0, price_type="market")
                log.info(f"卖出（调仓）: {symbol}")
    except Exception as e:
        log.error(f"获取持仓失败: {e}")

    # 买入新持仓
    for stock in target_stocks:
        try:
            trade.open_long(stock, params["trade_unit"], price=0, price_type="market")
            log.info(f"买入: {stock}")
        except Exception as e:
            log.error(f"买入失败 {stock}: {e}")
