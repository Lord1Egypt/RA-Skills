# -*- coding: utf-8 -*-
"""
=============================================================================
小果量化交易 - 工具函数
=============================================================================
功能：数据获取、指标计算、日志打印、持仓分析等辅助功能
适用平台：Ptrade 量化交易终端（研究/回测/交易模块）
=============================================================================
"""

import numpy as np
import pandas as pd
import time


def calculate_ma(security, period, frequency='1d', fq=None):
    """
    =============================================================================
    计算移动平均线（MA）
    =============================================================================
    
    参数：
        security: 股票代码（str），如 '600570.SS'
        period: 周期（int），如 5、10、20
        frequency: 频率（str），'1d'（日线）、'1m'（分钟线）、'1w'（周线）
        fq: 复权方式（str），None（不复权）、'pre'（前复权）、'post'（后复权）
    
    返回：
        float: 移动平均线值，如果数据不足返回 None
    
    示例：
        ma5 = calculate_ma('600570.SS', 5)  # 计算5日均线
        ma10 = calculate_ma('600570.SS', 10, '1d', 'pre')  # 计算前复权10日均线
    =============================================================================
    """
    try:
        # 获取历史数据
        df = get_history(
            count=period + 1,
            frequency=frequency,
            field='close',
            security_list=security,
            fq=fq,
            include=False
        )
        
        # 检查数据是否足够
        if df is None or len(df) < period:
            log.warning("数据不足，无法计算 %d 日均线，当前数据长度: %d" % 
                       (period, 0 if df is None else len(df)))
            return None
        
        # 计算均线
        close_prices = df['close'].values
        ma = close_prices[-period:].mean()
        
        return ma
    
    except Exception as e:
        log.error("计算均线时出错: %s" % str(e))
        return None


def calculate_macd(security, fast=12, slow=26, signal=9, frequency='1d'):
    """
    =============================================================================
    计算 MACD 指标
    =============================================================================
    
    参数：
        security: 股票代码（str）
        fast: 快线周期（int），默认12
        slow: 慢线周期（int），默认26
        signal: 信号线周期（int），默认9
        frequency: 频率（str），默认'1d'
    
    返回：
        dict: {'DIF': float, 'DEA': float, 'MACD': float}，失败返回 None
    
    说明：
        - DIF = EMA(fast) - EMA(slow)
        - DEA = EMA(DIF, signal)
        - MACD = (DIF - DEA) * 2
    =============================================================================
    """
    try:
        # 获取足够的历史数据
        count = slow + signal + 10
        df = get_history(
            count=count,
            frequency=frequency,
            field='close',
            security_list=security,
            fq=None,
            include=False
        )
        
        if df is None or len(df) < count:
            return None
        
        close_prices = df['close'].values
        
        # 计算EMA
        def ema(data, period):
            alpha = 2 / (period + 1)
            result = np.zeros(len(data))
            result[0] = data
            for i in range(1, len(data)):
                result[i] = alpha * data[i] + (1 - alpha) * result[i-1]
            return result
        
        # 计算DIF
        ema_fast = ema(close_prices, fast)
        ema_slow = ema(close_prices, slow)
        dif = ema_fast - ema_slow
        
        # 计算DEA
        dea = ema(dif, signal)
        
        # 计算MACD柱
        macd = (dif - dea) * 2
        
        return {
            'DIF': dif[-1],
            'DEA': dea[-1],
            'MACD': macd[-1]
        }
    
    except Exception as e:
        log.error("计算MACD时出错: %s" % str(e))
        return None


def calculate_rsi(security, period=14, frequency='1d'):
    """
    =============================================================================
    计算 RSI（相对强弱指标）
    =============================================================================
    
    参数：
        security: 股票代码（str）
        period: 周期（int），默认14
        frequency: 频率（str），默认'1d'
    
    返回：
        float: RSI值（0-100），失败返回 None
    
    说明：
        RSI = 100 - (100 / (1 + RS))
        RS = 平均上涨幅度 / 平均下跌幅度
    =============================================================================
    """
    try:
        count = period + 10
        df = get_history(
            count=count,
            frequency=frequency,
            field='close',
            security_list=security,
            fq=None,
            include=False
        )
        
        if df is None or len(df) < period + 1:
            return None
        
        close_prices = df['close'].values
        
        # 计算价格变化
        changes = np.diff(close_prices)
        
        # 取最近 period 个变化
        recent_changes = changes[-period:]
        
        # 计算平均上涨和下跌
        gains = np.mean([x for x in recent_changes if x > 0]) if any(x > 0 for x in recent_changes) else 0
        losses = np.mean([-x for x in recent_changes if x < 0]) if any(x < 0 for x in recent_changes) else 0
        
        if losses == 0:
            return 100.0
        
        rs = gains / losses
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    except Exception as e:
        log.error("计算RSI时出错: %s" % str(e))
        return None


def get_stock_info_dict(stocks):
    """
    =============================================================================
    获取股票信息字典
    =============================================================================
    
    参数：
        stocks: 股票代码列表（list[str]）或单个股票代码（str）
    
    返回：
        dict: {股票代码: {'name': 名称, 'listed_date': 上市日期, ...}}
    
    示例：
        info = get_stock_info_dict('600570.SS')
        info = get_stock_info_dict(['600570.SS', '000001.SZ'])
    =============================================================================
    """
    try:
        result = {}
        
        if isinstance(stocks, str):
            stocks = [stocks]
        
        for stock in stocks:
            try:
                name = get_stock_name(stock)
                info = get_stock_info(stock, ['stock_name', 'listed_date', 'de_listed_date'])
                
                result[stock] = {
                    'name': name.get(stock, '未知'),
                    'listed_date': info.get(stock, {}).get('listed_date', '未知'),
                    'de_listed_date': info.get(stock, {}).get('de_listed_date', '未知')
                }
            except Exception as e:
                result[stock] = {'name': '获取失败', 'error': str(e)}
        
        return result
    
    except Exception as e:
        log.error("获取股票信息时出错: %s" % str(e))
        return {}


def print_portfolio_summary(context):
    """
    =============================================================================
    打印账户持仓摘要
    =============================================================================
    
    参数：
        context: Context 对象
    
    使用示例：
        print_portfolio_summary(context)
    =============================================================================
    """
    log.info("=" * 50)
    log.info("【账户持仓摘要】")
    log.info("总资产: %.2f" % context.portfolio.portfolio_value)
    log.info("可用资金: %.2f" % context.portfolio.cash)
    log.info("持仓市值: %.2f" % context.portfolio.positions_value)
    log.info("累计收益率: %.2f%%" % (context.portfolio.returns * 100))
    log.info("起始日期: %s" % context.portfolio.start_date)
    log.info("=" * 50)
    
    # 获取所有持仓
    positions = get_positions()
    if positions:
        log.info("持仓明细:")
        for sid, pos in positions.items():
            log.info("  %s: 数量=%d, 成本价=%.2f, 最新价=%.2f, 盈亏=%.2f" % 
                     (sid, pos.amount, pos.cost_basis, pos.last_sale_price, 
                      (pos.last_sale_price - pos.cost_basis) * pos.amount))
    else:
        log.info("当前无持仓")


def check_stock_status(stock_code):
    """
    =============================================================================
    检查股票状态（ST、停牌、退市）
    =============================================================================
    
    参数：
        stock_code: 股票代码（str）
    
    返回：
        dict: {'is_st': bool, 'is_halt': bool, 'is_delisting': bool}
    =============================================================================
    """
    try:
        result = {
            'is_st': False,
            'is_halt': False,
            'is_delisting': False
        }
        
        # 检查ST状态
        st_status = get_stock_status([stock_code], 'ST')
        if st_status and stock_code in st_status:
            result['is_st'] = st_status[stock_code] is True
        
        # 检查停牌状态
        halt_status = get_stock_status([stock_code], 'HALT')
        if halt_status and stock_code in halt_status:
            result['is_halt'] = halt_status[stock_code] is True
        
        # 检查退市状态
        delist_status = get_stock_status([stock_code], 'DELISTING')
        if delist_status and stock_code in delist_status:
            result['is_delisting'] = delist_status[stock_code] is True
        
        return result
    
    except Exception as e:
        log.error("检查股票状态时出错: %s" % str(e))
        return None


def get_trade_days_count(start_date, end_date):
    """
    =============================================================================
    获取指定日期范围内的交易日数量
    =============================================================================
    
    参数：
        start_date: 开始日期（str），如 '2023-01-01'
        end_date: 结束日期（str），如 '2023-12-31'
    
    返回：
        int: 交易日数量
    =============================================================================
    """
    try:
        trade_days = get_trade_days(start_date=start_date, end_date=end_date)
        return len(trade_days) if trade_days is not None else 0
    except Exception as e:
        log.error("获取交易日数量时出错: %s" % str(e))
        return 0


def sleep_seconds(seconds):
    """
    =============================================================================
    延时函数（用于控制API调用频率）
    =============================================================================
    
    参数：
        seconds: 延时秒数（int/float）
    
    说明：
        Ptrade API 有流量限制，每秒不得调用超过100次
        在批量获取数据时，适当调用此函数避免触发限制
    =============================================================================
    """
    time.sleep(seconds)