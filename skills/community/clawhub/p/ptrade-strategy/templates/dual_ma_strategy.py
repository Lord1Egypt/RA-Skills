"""
PTRADE 双均线量化策略
========================================
策略逻辑：
  - 短期均线上穿长期均线（金叉）→ 买入开仓
  - 短期均线下穿长期均线（死叉）→ 卖出平仓
  - 配合成交量验证信号强度，避免虚假突破
适用周期：日线 / 60分钟（可切换 period 参数）
适用标的：沪深A股（支持 000001.XSHG 等格式）

使用方法：
  1. 打开 PTRADE 策略编辑器
  2. 新建策略 → 粘贴本代码 → 保存
  3. 回测验证 → 参数优化 → 实盘运行
"""

import numpy as np


# ============================================
# 策略参数（可在 PTRADE 界面修改）
# ============================================
SECURITY     = "000001.XSHG"   # 交易标的（格式：代码.交易所，XSHG=上海 XSE=深圳）
SHORT_WIN    = 5               # 短期均线周期（单位：根K线）
LONG_WIN     = 20              # 长期均线周期
TRADE_UNIT   = 100             # 每笔交易数量（必须是100的整数倍=1手）
PERIOD       = "1d"           # K线周期：1d=日线，60m=60分钟，5m=5分钟

# 成交量过滤参数（可选）
USE_VOL_FILTER = True         # 是否启用成交量过滤
VOL_RATIO      = 1.2          # 当日成交量需超过均值多少倍才触发信号

# 止损止盈参数
STOP_LOSS_PCT  = 0.05         # 止损比例：跌超5%自动止损
TAKE_PROFIT_PCT = 0.15        # 止盈比例：涨超15%自动止盈

# ============================================
# 初始化（每个策略生命周期只执行一次）
# ============================================
def initialize(context):
    """设置策略参数和全局状态"""
    # 保存参数到 context.params（可在界面修改）
    context.params = {
        "security":       SECURITY,
        "short_window":   SHORT_WIN,
        "long_window":    LONG_WIN,
        "trade_unit":     TRADE_UNIT,
        "period":         PERIOD,
        "use_vol_filter": USE_VOL_FILTER,
        "vol_ratio":      VOL_RATIO,
        "stop_loss":      STOP_LOSS_PCT,
        "take_profit":    TAKE_PROFIT_PCT,
    }

    # 获取 PTRADE 全局对象
    g = get_json("context").get("g", {})
    context.g.security = g.get("security")
    context.g.trade    = g.get("trade")
    context.g.log      = g.get("log")

    # 记录上一次均线的方向，避免重复信号
    context.g.prev_short_ma = None
    context.g.prev_long_ma  = None

    # 记录持仓成本价（用于止损止盈）
    context.g.buy_price = None

    context.g.log.info(
        f"【策略启动】标的={SECURITY} 短周期={SHORT_WIN} 长周期={LONG_WIN} "
        f"周期={PERIOD} 成交量过滤={'开启' if USE_VOL_FILTER else '关闭'}"
    )


# ============================================
# 每日行情数据驱动（核心策略逻辑）
# ============================================
def handle_data(context):
    """每根K线收盘后自动执行"""
    security = context.g.security
    trade    = context.g.trade
    log      = context.g.log
    params   = context.params

    sym = params["security"]

    # ---- 获取K线数据 ----
    n = params["long_window"] + 5   # 多取几根确保计算正确
    bars = security.get_bars(
        n=n,
        end_date="",
        fields=["open", "high", "low", "close", "volume"],
        count=n,
        period=params["period"]
    )

    close  = bars["close"]
    volume = bars["volume"]

    if close is None or len(close) < params["long_window"]:
        log.info(f"【数据不足】{sym} 当前K线数量={len(close)}，等待数据...")
        return

    # ---- 计算均线 ----
    short_ma = float(np.mean(close[-params["short_window"]:]))
    long_ma  = float(np.mean(close[-params["long_window"]:]))

    # 前一周期均线值（用于判断方向）
    prev_short_ma = float(np.mean(close[-params["short_window"]-1:-1]))
    prev_long_ma  = float(np.mean(close[-params["long_window"]-1:-1]))

    current_price = float(close[-1])

    # ---- 当前持仓检查 ----
    positions = security.get_positions()
    current_pos = 0
    for pos in positions:
        if pos.get("security") == sym and pos.get("volume", 0) > 0:
            current_pos = int(pos.get("volume", 0))
            break

    # 获取成本价（若已有持仓）
    if context.g.buy_price is None and current_pos > 0:
        # 从持仓信息中获取成本
        for pos in positions:
            if pos.get("security") == sym:
                context.g.buy_price = float(pos.get("avg_price", current_price))
                break

    # ============================================
    # 止盈止损检查（有持仓时优先检查）
    # ============================================
    if current_pos > 0 and context.g.buy_price is not None:
        pnl_pct = (current_price - context.g.buy_price) / context.g.buy_price

        # 止损
        if pnl_pct <= -params["stop_loss"]:
            log.info(
                f"【止损出局】{sym} 现价={current_price:.2f} "
                f"成本={context.g.buy_price:.2f} 亏损={pnl_pct*100:.2f}%"
            )
            trade.close_long(sym, current_pos, price=0, price_type="market")
            context.g.buy_price = None
            return

        # 止盈
        if pnl_pct >= params["take_profit"]:
            log.info(
                f"【止盈出局】{sym} 现价={current_price:.2f} "
                f"成本={context.g.buy_price:.2f} 盈利={pnl_pct*100:.2f}%"
            )
            trade.close_long(sym, current_pos, price=0, price_type="market")
            context.g.buy_price = None
            return

    # ============================================
    # 均线金叉/死叉信号
    # ============================================
    prev_crossed = (prev_short_ma <= prev_long_ma)   # 上一周期：短期≤长期
    curr_crossed = (short_ma > long_ma)             # 当前周期：短期>长期
    gold_cross   = curr_crossed and not prev_crossed # 金叉：刚刚从下穿上

    prev_dead = (prev_short_ma >= prev_long_ma)     # 上一周期：短期≥长期
    curr_dead = (short_ma < long_ma)               # 当前周期：短期<长期
    dead_cross = curr_dead and not prev_dead       # 死叉：刚刚从上穿下

    # ---- 成交量过滤 ----
    if params["use_vol_filter"] and gold_cross:
        avg_vol = float(np.mean(volume[:-1]))
        today_vol = float(volume[-1])
        if today_vol < avg_vol * params["vol_ratio"]:
            log.info(
                f"【信号过滤】{sym} 成交量不足：今日={today_vol:.0f} "
                f"均值={avg_vol:.0f} 比率={today_vol/avg_vol:.2f} < {params['vol_ratio']}"
            )
            gold_cross = False

    # ============================================
    # 执行交易
    # ============================================
    if gold_cross and current_pos == 0:
        # 金叉买入
        log.info(
            f"【买入信号】{sym} 金叉！短期MA={short_ma:.2f} > 长期MA={long_ma:.2f} "
            f"当前价={current_price:.2f} 买入{params['trade_unit']}股"
        )
        trade.open_long(sym, params["trade_unit"], price=0, price_type="market")
        context.g.buy_price = current_price  # 记录买入成本

    elif dead_cross and current_pos > 0:
        # 死叉卖出
        log.info(
            f"【卖出信号】{sym} 死叉！短期MA={short_ma:.2f} < 长期MA={long_ma:.2f} "
            f"当前价={current_price:.2f} 卖出{current_pos}股"
        )
        trade.close_long(sym, current_pos, price=0, price_type="market")
        context.g.buy_price = None

    # ---- 记录当前均线状态（调试用） ----
    context.g.prev_short_ma = short_ma
    context.g.prev_long_ma  = long_ma
