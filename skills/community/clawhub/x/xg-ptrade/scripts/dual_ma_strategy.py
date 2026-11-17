
---

### 2. scripts/dual_ma_strategy.py（双均线策略核心代码 - 完整版）

```python
# -*- coding: utf-8 -*-
"""
=============================================================================
小果量化交易 - 双均线策略（Ptrade 版本完整版）
=============================================================================
适用平台：Ptrade 量化交易终端（回测 + 实盘交易）
策略类型：股票双均线（金叉买入，死叉卖出）
交易标的：600570.SS（恒生电子）
回测频率：支持日线/分钟级别
创建时间：2026-08-14
=============================================================================

【策略逻辑】
1. 计算五日均线（MA5）和十日均线（MA10）
2. 当 MA5 上穿 MA10 时（金叉），全仓买入
3. 当 MA5 下穿 MA10 时（死叉），全部卖出
4. 记录关键变量用于绘制曲线
"""

import numpy as np
import pandas as pd


def initialize(context):
    """
    =============================================================================
    初始化函数（必选）
    =============================================================================
    该函数只在策略启动时运行一次，用于：
    1. 设置股票池（set_universe）
    2. 初始化全局变量（g 对象）
    3. 设置回测参数（佣金、滑点等）
    4. 设置定时任务（run_daily、run_interval）
    
    参数：
        context: Context 对象，存放账户及持仓信息
    
    注意事项：
        - 该函数只在回测和交易启动的时候运行一次
        - 全局变量 g 中定义的变量可在所有函数中访问
        - g 中以 '_' 开头的变量不会被持久化保存
    =============================================================================
    """
    # ========== 1. 设置股票池 ==========
    # 说明：set_universe 用于设置策略可操作的股票列表
    # 格式：单只股票用字符串，多只股票用列表
    g.security = '600570.SS'  # 恒生电子
    # g.security = ['600570.SS', '000001.SZ']  # 多只股票示例
    set_universe(g.security)
    
    # ========== 2. 设置回测基准 ==========
    # 说明：set_benchmark 用于设置比较基准
    # 默认：沪深300指数（000300.SS）
    # set_benchmark('000300.SS')  # 取消注释即可使用
    
    # ========== 3. 设置佣金费率 ==========
    # 说明：set_commission 用于设置佣金费率
    # 参数：commission_ratio（费率），min_commission（最低佣金），type（交易类型）
    # 默认：万分之三，最低5元
    # set_commission(commission_ratio=0.0003, min_commission=5.0)
    
    # ========== 4. 设置滑点 ==========
    # 说明：set_slippage 用于设置滑点比例
    # 参数：slippage（滑点比例，默认0.1%）
    # set_slippage(slippage=0.1)
    
    # ========== 5. 设置固定滑点 ==========
    # 说明：set_fixed_slippage 用于设置固定滑点（元）
    # 参数：fixedslippage（固定滑点，默认0.0）
    # set_fixed_slippage(fixedslippage=0.02)
    
    # ========== 6. 设置成交比例 ==========
    # 说明：set_volume_ratio 用于设置单笔委托的成交比例
    # 参数：volume_ratio（成交比例，默认0.25，即四分之一）
    # set_volume_ratio(volume_ratio=0.25)
    
    # ========== 7. 设置成交数量限制模式 ==========
    # 说明：set_limit_mode 用于设置成交数量限制模式
    # 参数：'LIMIT'（限制），'UNLIMITED'（不限制）
    # set_limit_mode('LIMIT')
    
    # ========== 8. 设置底仓 ==========
    # 说明：set_yesterday_position 用于设置回测的初始底仓
    # 参数：list[dict]，包含 sid, amount, enable_amount, cost_basis
    # pos = {'sid': '600570.SS', 'amount': '1000', 'enable_amount': '600', 'cost_basis': '55'}
    # set_yesterday_position([pos])
    
    # ========== 9. 初始化全局变量 ==========
    # 说明：g 对象用于存储全局变量，可在所有函数中访问
    # 注意：g 中以 '_' 开头的变量不会被持久化保存
    g.ma_short = 5      # 短期均线周期（5日均线）
    g.ma_long = 10       # 长期均线周期（10日均线）
    g.is_bought = False  # 买入标记（True=已买入，False=未买入）
    g.trade_count = 0    # 交易次数统计
    
    # ========== 10. 设置定时任务（仅交易模块） ==========
    # 说明：run_daily 用于按日周期运行指定函数
    # 参数：context, func, time（执行时间，如'9:31'）
    # run_daily(context, my_daily_func, time='9:31')
    
    # ========== 11. 设置周期任务（仅交易模块） ==========
    # 说明：run_interval 用于按设定时间间隔运行指定函数
    # 参数：context, func, seconds（时间间隔，最小3秒）
    # run_interval(context, my_interval_func, seconds=10)
    
    # ========== 12. 日志输出 ==========
    log.info("=" * 50)
    log.info("小果量化交易 - 双均线策略初始化完成")
    log.info("股票池: %s" % g.security)
    log.info("均线参数: MA%d / MA%d" % (g.ma_short, g.ma_long))
    log.info("=" * 50)


def handle_data(context, data):
    """
    =============================================================================
    盘中处理函数（必选）
    =============================================================================
    该函数在交易时间内按指定的周期频率运行，是策略交易的核心模块。
    
    日线级别：每天执行一次，股票回测在15:00执行，交易由券商配置决定
    分钟级别：每分钟执行一次，股票回测在9:31~15:00执行，交易在9:30~14:59执行
    
    参数：
        context: Context 对象，存放账户及持仓信息
        data: dict，key为标的代码，value为SecurityUnitData对象
    
    注意事项：
        - 该函数每个单位周期执行一次
        - 非交易日不会触发（如周末、节假日）
        - data 中只包含股票池中所订阅标的的信息
    =============================================================================
    """
    # ========== 1. 获取当前标的代码 ==========
    security = g.security
    
    # ========== 2. 获取历史数据 ==========
    # 说明：get_history 用于获取最近N条历史行情K线数据
    # 参数：count（数量），frequency（周期），field（字段），security_list（股票列表）
    #       fq（复权），include（是否包含当前周期），fill（数据填充方式）
    # 返回：单只股票返回DataFrame，多只股票返回Panel
    #
    # 注意事项：
    #   - 只能获取2005年后的数据
    #   - 停牌日使用停牌前数据填充，成交量为0
    #   - count 要大于均线周期，才能计算均线
    df = get_history(
        count=g.ma_long + 5,       # 多取几天，确保数据充足
        frequency='1d',             # 日线数据
        field='close',              # 只需收盘价
        security_list=security,     # 单只股票用字符串
        fq=None,                    # 不复权
        include=False,              # 不包含当前周期
        fill='nan'                  # 缺失数据用NaN填充
    )
    
    # ========== 3. 检查数据是否足够 ==========
    # 说明：如果数据不足，无法计算均线，直接返回
    if df is None or len(df) < g.ma_long:
        log.warning("历史数据不足，当前数据长度: %d" % (0 if df is None else len(df)))
        return
    
    # ========== 4. 计算均线 ==========
    # 说明：取最近N天的收盘价，计算平均值
    close_prices = df['close'].values
    
    # 短期均线（MA5）
    ma_short = close_prices[-g.ma_short:].mean()
    
    # 长期均线（MA10）
    ma_long = close_prices[-g.ma_long:].mean()
    
    # ========== 5. 获取当前行情数据 ==========
    # 说明：data[security] 返回当前周期的行情数据
    # 常用字段：open（开盘价），high（最高价），low（最低价），close（收盘价）
    #          volume（交易量），money（交易金额），price（最新价）
    
    # 获取当前收盘价（日线策略）或最新价（分钟策略）
    current_price = data[security]['close']
    
    # ========== 6. 获取账户资金信息 ==========
    # 说明：context.portfolio 包含账户信息
    # 常用字段：
    #   - cash：可用资金
    #   - portfolio_value：总资产
    #   - positions_value：持仓市值
    #   - returns：累计收益率
    #   - start_date：起始日期
    cash = context.portfolio.cash
    portfolio_value = context.portfolio.portfolio_value
    
    # ========== 7. 获取持仓信息 ==========
    # 说明：get_position 获取单只股票的持仓信息
    # 返回：Position 对象，包含 amount（持仓数量），enable_amount（可用数量）
    #       cost_basis（成本价），last_sale_price（最新价）
    position = get_position(security)
    # 如果持仓不存在，position 为 None
    position_amount = 0 if position is None else position.amount
    
    # ========== 8. 交易逻辑（核心） ==========
    # 日志输出当前状态
    log.info("当前标的: %s, 收盘价: %.2f, MA%d: %.2f, MA%d: %.2f, 现金: %.2f" % 
             (security, current_price, g.ma_short, ma_short, g.ma_long, ma_long, cash))
    log.info("持仓数量: %d, 已买入标记: %s" % (position_amount, g.is_bought))
    
    # ---------- 买入条件判断 ----------
    # 条件1：短期均线 > 长期均线（金叉）
    # 条件2：未买入（避免重复买入）
    # 条件3：有可用资金
    if ma_short > ma_long and not g.is_bought and cash > 0:
        # 计算买入价值（全仓买入）
        buy_value = cash
        
        # 执行买入操作
        # order_value：按指定价值买入
        # 参数：security（股票代码），value（买入价值），limit_price（限价）
        order_id = order_value(security, buy_value)
        
        # 更新状态
        g.is_bought = True
        g.trade_count += 1
        
        # 日志记录
        log.info("=" * 40)
        log.info("【买入信号】金叉出现！MA%d(%.2f) > MA%d(%.2f)" % 
                 (g.ma_short, ma_short, g.ma_long, ma_long))
        log.info("买入标的: %s, 价格: %.2f, 金额: %.2f" % 
                 (security, current_price, buy_value))
        log.info("订单编号: %s" % order_id)
        log.info("=" * 40)
    
    # ---------- 卖出条件判断 ----------
    # 条件1：短期均线 < 长期均线（死叉）
    # 条件2：已买入（有持仓）
    # 条件3：持仓数量 > 0
    elif ma_short < ma_long and g.is_bought and position_amount > 0:
        # 执行卖出操作
        # order_target：调整到目标持仓数量（0 = 全部卖出）
        # 参数：security（股票代码），amount（目标数量），limit_price（限价）
        order_id = order_target(security, 0)
        
        # 更新状态
        g.is_bought = False
        g.trade_count += 1
        
        # 日志记录
        log.info("=" * 40)
        log.info("【卖出信号】死叉出现！MA%d(%.2f) < MA%d(%.2f)" % 
                 (g.ma_short, ma_short, g.ma_long, ma_long))
        log.info("卖出标的: %s, 价格: %.2f, 数量: %d" % 
                 (security, current_price, position_amount))
        log.info("订单编号: %s" % order_id)
        log.info("=" * 40)
    
    # ========== 9. 记录变量（用于绘制曲线） ==========
    # 说明：record 函数用于记录变量，可在回测结果中查看曲线
    # 参数：key=value 形式，key 为曲线名称，value 为数值
    record(stock_price=current_price)
    record(ma5=ma_short)
    record(ma10=ma_long)
    record(cash=cash)
    record(portfolio_value=portfolio_value)


def before_trading_start(context, data):
    """
    =============================================================================
    盘前处理函数（可选）
    =============================================================================
    该函数在每天开始交易前被调用一次，用于添加每天都要初始化的信息。
    
    执行时间：
        - 回测：每个交易日 8:30
        - 交易：开启交易时立即执行，隔日开始每天 9:10（默认）
    
    参数：
        context: Context 对象，存放账户及持仓信息
        data: 保留字段，暂无数据
    
    注意事项：
        - 在9:10前调用实时行情接口会导致数据有误
        - 可通过在该函数内 sleep 至9:10分或使用 run_daily 避免
    =============================================================================
    """
    # 重置每日计数器
    g.daily_trade_count = 0
    
    # 获取今日交易日
    today = get_trading_day(0)
    log.info("盘前准备 - 交易日: %s, 股票池: %s" % (today, g.security))
    
    # 可选：获取股票池中所有股票的信息
    # stock_info = get_stock_info(g.security)
    # log.info("股票信息: %s" % stock_info)
    
    # 可选：获取指数成分股
    # index_stocks = get_index_stocks('000300.XBHS')
    # log.info("沪深300成分股数量: %d" % len(index_stocks))


def after_trading_end(context, data):
    """
    =============================================================================
    盘后处理函数（可选）
    =============================================================================
    该函数会在每天交易结束之后调用，用于处理每天收盘后的操作。
    
    执行时间：
        - 由券商配置决定，一般为 15:30
    
    参数：
        context: Context 对象，存放账户及持仓信息
        data: 保留字段，暂无数据
    =============================================================================
    """
    # 计算当日收益
    today_return = context.portfolio.returns * 100
    
    # 日志输出
    log.info("=" * 50)
    log.info("【盘后总结】交易日结束")
    log.info("总资产: %.2f" % context.portfolio.portfolio_value)
    log.info("可用资金: %.2f" % context.portfolio.cash)
    log.info("持仓市值: %.2f" % context.portfolio.positions_value)
    log.info("当日收益率: %.2f%%" % today_return)
    log.info("累计交易次数: %d" % g.trade_count)
    log.info("=" * 50)


def tick_data(context, data):
    """
    =============================================================================
    Tick级别处理函数（可选，仅交易模块可用）
    =============================================================================
    该函数用于处理 tick 级别策略的交易逻辑，每隔 3 秒执行一次。
    
    执行时间：9:30 ~ 14:59
    
    参数：
        context: Context 对象，存放账户及持仓信息
        data: dict，包含 tick（当前tick数据）、order（逐笔委托）、transcation（逐笔成交）
    
    注意事项：
        - 该函数中只能使用 order_tick 进行下单操作
        - 逐笔委托、逐笔成交数据需开通 Level2 行情
        - 参数 data 和 handle_data 中的 data 不一样，请勿混肴
    =============================================================================
    """
    # 注意：此函数仅用于交易模块，回测中不会执行
    # 使用 tick 级别时需要开通 Level2 行情
    pass


def on_order_response(context, order_list):
    """
    =============================================================================
    委托主推回调函数（可选，仅交易模块可用）
    =============================================================================
    该函数会在委托主推回调时响应，比 get_order() 和 get_orders() 更新速度更快。
    
    参数：
        context: Context 对象，存放账户及持仓信息
        order_list: list，当前委托单发生变化时，发生变化的委托单列表
    
    注意事项：
        - 可接收股票、可转债、ETF、LOF、期货的主推数据
        - 当在主推里调用委托接口时，需要进行判断处理避免无限迭代循环
    =============================================================================
    """
    for order_info in order_list:
        log.info("委托主推 - 委托编号: %s, 股票代码: %s, 状态: %s" % 
                 (order_info.get('entrust_no', ''),
                  order_info.get('stock_code', ''),
                  order_info.get('status', '')))


def on_trade_response(context, trade_list):
    """
    =============================================================================
    成交主推回调函数（可选，仅交易模块可用）
    =============================================================================
    该函数会在成交主推回调时响应，比 get_trades() 更新速度更快。
    
    参数：
        context: Context 对象，存放账户及持仓信息
        trade_list: list，当前成交单发生变化时，发生变化的成交单列表
    
    注意事项：
        - 可接收股票、可转债、ETF、LOF、期货的主推数据
        - 当在主推里调用委托接口时，需要进行判断处理避免无限迭代循环
    =============================================================================
    """
    for trade_info in trade_list:
        log.info("成交主推 - 委托编号: %s, 股票代码: %s, 成交数量: %d, 成交价格: %.2f" % 
                 (trade_info.get('entrust_no', ''),
                  trade_info.get('stock_code', ''),
                  trade_info.get('business_amount', 0),
                  trade_info.get('business_price', 0.0)))


# =============================================================================
# 示例：定时任务函数（可选，仅交易模块可用）
# =============================================================================
def my_daily_func(context):
    """
    自定义定时任务函数
    通过 run_daily 在 initialize 中调用
    """
    log.info("定时任务执行 - 当前时间: %s" % context.blotter.current_dt)


def my_interval_func(context):
    """
    自定义周期任务函数
    通过 run_interval 在 initialize 中调用
    """
    log.info("周期任务执行 - 当前时间: %s" % context.blotter.current_dt)