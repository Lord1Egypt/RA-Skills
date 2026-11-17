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