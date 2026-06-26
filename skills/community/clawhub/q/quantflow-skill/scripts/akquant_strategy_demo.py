#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AKQuant 策略回测示例脚本

本脚本演示如何使用 AKQuant 进行量化策略回测，包括：
1. 使用 akshare 获取历史数据
2. 构建 AKQuant 策略
3. 运行回测
4. 分析回测结果
"""

import akquant as aq
import akshare as ak
from akquant import Strategy


def get_stock_data(symbol, start_date, end_date):
    """
    使用 akshare 获取股票历史数据
    
    Args:
        symbol: 股票代码，如 "sh600000"
        start_date: 开始日期，格式为 "YYYYMMDD"
        end_date: 结束日期，格式为 "YYYYMMDD"
    
    Returns:
        DataFrame: 股票历史数据
    """
    try:
        # 获取股票日线数据
        data = ak.stock_zh_a_daily(symbol=symbol, start_date=start_date, end_date=end_date)
        print(f"获取 {symbol} 历史数据成功，数据量: {len(data)} 条")
        return data
    except Exception as e:
        print(f"获取股票数据失败: {e}")
        return None


class SimpleStrategy(Strategy):
    """
    简单策略示例：基于收盘价和开盘价的趋势策略
    
    策略逻辑：
    - 当收盘价 > 开盘价（阳线）时，买入
    - 当收盘价 < 开盘价（阴线）时，卖出
    """
    
    def on_bar(self, bar):
        # 获取当前持仓
        current_pos = self.get_position(bar.symbol)
        
        # 策略逻辑
        if current_pos == 0 and bar.close > bar.open:
            # 买入 100 股
            self.buy(bar.symbol, 100)
            print(f"[{bar.timestamp_str}] Buy 100 at {bar.close:.2f}")
        
        elif current_pos > 0 and bar.close < bar.open:
            # 卖出所有持仓
            self.close_position(bar.symbol)
            print(f"[{bar.timestamp_str}] Sell 100 at {bar.close:.2f}")


class MovingAverageStrategy(Strategy):
    """
    移动平均线策略示例：基于5日均线和20日均线的交叉
    
    策略逻辑：
    - 当5日均线向上穿越20日均线时，买入
    - 当5日均线向下穿越20日均线时，卖出
    """
    
    def __init__(self):
        super().__init__()
        self.short_period = 5  # 短期均线周期
        self.long_period = 20   # 长期均线周期
        self.ma_short = []      # 短期均线值
        self.ma_long = []       # 长期均线值
    
    def on_bar(self, bar):
        # 获取当前持仓
        current_pos = self.get_position(bar.symbol)
        
        # 计算移动平均线
        self.ma_short.append(bar.close)
        self.ma_long.append(bar.close)
        
        # 保持均线长度
        if len(self.ma_short) > self.short_period:
            self.ma_short.pop(0)
        if len(self.ma_long) > self.long_period:
            self.ma_long.pop(0)
        
        # 当均线数据足够时，执行策略逻辑
        if len(self.ma_short) == self.short_period and len(self.ma_long) == self.long_period:
            short_avg = sum(self.ma_short) / self.short_period
            long_avg = sum(self.ma_long) / self.long_period
            
            # 金叉：短期均线上穿长期均线
            if short_avg > long_avg and current_pos == 0:
                self.buy(bar.symbol, 100)
                print(f"[{bar.timestamp_str}] Buy 100 at {bar.close:.2f} (MA5: {short_avg:.2f}, MA20: {long_avg:.2f})")
            
            # 死叉：短期均线下穿长期均线
            elif short_avg < long_avg and current_pos > 0:
                self.close_position(bar.symbol)
                print(f"[{bar.timestamp_str}] Sell 100 at {bar.close:.2f} (MA5: {short_avg:.2f}, MA20: {long_avg:.2f})")


def run_backtest(data, strategy_class, symbol):
    """
    运行策略回测
    
    Args:
        data: 历史数据
        strategy_class: 策略类
        symbol: 股票代码
    
    Returns:
        回测结果
    """
    try:
        # 运行回测
        result = aq.run_backtest(
            data=data,
            strategy=strategy_class,
            symbol=symbol
        )
        
        # 打印回测结果
        print("\n=== 回测结果 ===")
        print(result.metrics_df)
        
        # 打印关键指标
        print("\n=== 关键指标 ===")
        print(f"总收益率: {result.metrics_df.loc['total_return_pct', 'value']:.4f}")
        print(f"年化收益率: {result.metrics_df.loc['annualized_return', 'value']:.4f}")
        print(f"夏普比率: {result.metrics_df.loc['sharpe_ratio', 'value']:.4f}")
        print(f"最大回撤: {result.metrics_df.loc['max_drawdown_pct', 'value']:.4f}")
        print(f"胜率: {result.metrics_df.loc['win_rate', 'value']:.4f}")
        
        return result
    except Exception as e:
        print(f"回测失败: {e}")
        return None


if __name__ == "__main__":
    print("===== AKQuant 策略回测示例 =====")
    
    # 1. 获取历史数据
    symbol = "sh600000"  # 浦发银行
    start_date = "20230101"
    end_date = "20231231"
    data = get_stock_data(symbol, start_date, end_date)
    
    if data is not None:
        # 2. 运行简单策略回测
        print("\n===== 运行简单策略回测 =====")
        run_backtest(data, SimpleStrategy, symbol)
        
        # 3. 运行移动平均线策略回测
        print("\n===== 运行移动平均线策略回测 =====")
        run_backtest(data, MovingAverageStrategy, symbol)
