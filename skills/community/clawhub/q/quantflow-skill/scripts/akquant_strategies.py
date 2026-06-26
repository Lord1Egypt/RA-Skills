#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AKQuant 多种量化策略实现

本脚本实现了多种常见的量化策略，包括：
1. 双均线策略(期货)
2. Alpha对冲(股票+期货)
3. 集合竞价选股(股票)
4. 多因子选股(股票)
5. 网格交易(期货)
6. 指数增强(股票)
7. 跨品种套利(期货)
8. 跨期套利(期货)
9. 日内回转交易(股票)
10. 做市商交易(期货)
11. 海龟交易法(期货)
12. 行业轮动(股票)
13. 机器学习(股票)
"""

import akquant as aq
import akshare as ak
from akquant import Strategy
import numpy as np
import pandas as pd
from datetime import datetime


class DualMAFuturesStrategy(Strategy):
    """
    双均线策略(期货)
    
    策略逻辑：
    - 当短期均线上穿长期均线时，买入
    - 当短期均线下穿长期均线时，卖出
    """
    
    def __init__(self, short_period=5, long_period=20):
        super().__init__()
        self.short_period = short_period
        self.long_period = long_period
        self.short_ma = []
        self.long_ma = []
    
    def on_bar(self, bar):
        # 计算移动平均线
        self.short_ma.append(bar.close)
        self.long_ma.append(bar.close)
        
        # 保持均线长度
        if len(self.short_ma) > self.short_period:
            self.short_ma.pop(0)
        if len(self.long_ma) > self.long_period:
            self.long_ma.pop(0)
        
        # 当均线数据足够时，执行策略逻辑
        if len(self.short_ma) == self.short_period and len(self.long_ma) == self.long_period:
            short_avg = sum(self.short_ma) / self.short_period
            long_avg = sum(self.long_ma) / self.long_period
            
            # 金叉：短期均线上穿长期均线
            if short_avg > long_avg and self.get_position(bar.symbol) == 0:
                self.buy(bar.symbol, 1)
                print(f"[{bar.timestamp_str}] Buy 1 contract at {bar.close:.2f} (MA{self.short_period}: {short_avg:.2f}, MA{self.long_period}: {long_avg:.2f})")
            
            # 死叉：短期均线下穿长期均线
            elif short_avg < long_avg and self.get_position(bar.symbol) > 0:
                self.close_position(bar.symbol)
                print(f"[{bar.timestamp_str}] Sell 1 contract at {bar.close:.2f} (MA{self.short_period}: {short_avg:.2f}, MA{self.long_period}: {long_avg:.2f})")


class AlphaHedgeStrategy(Strategy):
    """
    Alpha对冲(股票+期货)
    
    策略逻辑：
    - 买入一篮子具有Alpha的股票
    - 卖空股指期货进行对冲
    """
    
    def __init__(self, stock_symbols, index_future_symbol):
        super().__init__()
        self.stock_symbols = stock_symbols
        self.index_future_symbol = index_future_symbol
        self.stock_weights = {symbol: 1.0/len(stock_symbols) for symbol in stock_symbols}
    
    def on_bar(self, bar):
        # 这里简化实现，实际需要处理多标的
        if bar.symbol in self.stock_symbols:
            # 买入股票
            if self.get_position(bar.symbol) == 0:
                weight = self.stock_weights[bar.symbol]
                # 假设总资金为100万，分配给股票的资金为80万
                stock_amount = int(800000 * weight / bar.close)
                self.buy(bar.symbol, stock_amount)
                print(f"[{bar.timestamp_str}] Buy {stock_amount} shares of {bar.symbol} at {bar.close:.2f}")
        
        elif bar.symbol == self.index_future_symbol:
            # 卖空股指期货
            if self.get_position(bar.symbol) == 0:
                # 假设卖空1手股指期货进行对冲
                self.sell(bar.symbol, 1)
                print(f"[{bar.timestamp_str}] Sell 1 contract of {bar.symbol} at {bar.close:.2f}")


class OpeningAuctionStrategy(Strategy):
    """
    集合竞价选股(股票)
    
    策略逻辑：
    - 基于集合竞价数据选股
    - 在开盘后买入选中的股票
    """
    
    def __init__(self):
        super().__init__()
        self.selected_stocks = []
        self.bought_stocks = set()
    
    def on_bar(self, bar):
        # 这里简化实现，实际需要获取集合竞价数据
        # 假设在每个交易日的第一个bar进行选股
        if bar.timestamp.hour == 9 and bar.timestamp.minute == 30:
            # 模拟选股逻辑：选择开盘涨幅在2%-5%之间的股票
            # 实际实现需要获取集合竞价数据
            if bar.symbol not in self.bought_stocks and 2 <= (bar.open - bar.close_prev) / bar.close_prev * 100 <= 5:
                self.selected_stocks.append(bar.symbol)
                print(f"[{bar.timestamp_str}] Select stock {bar.symbol} for opening auction strategy")
        
        # 在开盘后买入选中的股票
        if bar.symbol in self.selected_stocks and bar.symbol not in self.bought_stocks:
            # 买入1000股
            self.buy(bar.symbol, 1000)
            self.bought_stocks.add(bar.symbol)
            print(f"[{bar.timestamp_str}] Buy 1000 shares of {bar.symbol} at {bar.close:.2f}")


class MultiFactorStrategy(Strategy):
    """
    多因子选股(股票)
    
    策略逻辑：
    - 基于多个因子进行选股
    - 定期重新平衡组合
    """
    
    def __init__(self, rebalance_days=20):
        super().__init__()
        self.rebalance_days = rebalance_days
        self.day_count = 0
        self.selected_stocks = []
    
    def on_bar(self, bar):
        self.day_count += 1
        
        # 定期重新平衡组合
        if self.day_count % self.rebalance_days == 0:
            # 这里简化实现，实际需要计算多个因子
            # 假设基于PE、PB、ROE等因子选股
            print(f"[{bar.timestamp_str}] Rebalancing portfolio")
            
            # 卖出之前的股票
            for symbol in self.selected_stocks:
                if self.get_position(symbol) > 0:
                    self.close_position(symbol)
                    print(f"[{bar.timestamp_str}] Sell {symbol}")
            
            # 选择新的股票
            # 实际实现需要计算因子并排序选股
            self.selected_stocks = [bar.symbol]  # 简化，实际需要多股票选股
            
            # 买入新的股票
            for symbol in self.selected_stocks:
                if symbol == bar.symbol:
                    self.buy(symbol, 1000)
                    print(f"[{bar.timestamp_str}] Buy 1000 shares of {symbol} at {bar.close:.2f}")


class GridTradingStrategy(Strategy):
    """
    网格交易(期货)
    
    策略逻辑：
    - 设定价格网格
    - 在网格点进行买入和卖出
    """
    
    def __init__(self, base_price, grid_size, grid_count=5):
        super().__init__()
        self.base_price = base_price
        self.grid_size = grid_size
        self.grid_count = grid_count
        self.grids = []
        
        # 初始化网格
        for i in range(-grid_count, grid_count + 1):
            self.grids.append(base_price + i * grid_size)
    
    def on_bar(self, bar):
        current_price = bar.close
        position = self.get_position(bar.symbol)
        
        # 检查是否触发网格交易
        for i, grid_price in enumerate(self.grids):
            # 向上突破网格，买入
            if current_price > grid_price and position <= i - self.grid_count:
                self.buy(bar.symbol, 1)
                print(f"[{bar.timestamp_str}] Buy 1 contract at {current_price:.2f} (Grid {i - self.grid_count})")
                break
            
            # 向下突破网格，卖出
            if current_price < grid_price and position >= i - self.grid_count + 1:
                self.sell(bar.symbol, 1)
                print(f"[{bar.timestamp_str}] Sell 1 contract at {current_price:.2f} (Grid {i - self.grid_count})")
                break


class IndexEnhancementStrategy(Strategy):
    """
    指数增强(股票)
    
    策略逻辑：
    - 跟踪某个指数
    - 通过因子选股对指数进行增强
    """
    
    def __init__(self, index_symbol, enhancement_factor='roe'):
        super().__init__()
        self.index_symbol = index_symbol
        self.enhancement_factor = enhancement_factor
        self.index_components = []
    
    def on_bar(self, bar):
        # 这里简化实现，实际需要获取指数成分股
        # 假设在每个月的第一个交易日调整组合
        if bar.timestamp.day == 1:
            # 获取指数成分股
            # 实际实现需要调用akshare的接口获取指数成分股
            print(f"[{bar.timestamp_str}] Adjusting index enhancement portfolio")
            
            # 基于增强因子选择成分股
            # 实际实现需要计算因子并排序
            self.index_components = [bar.symbol]  # 简化，实际需要多股票
            
            # 买入成分股
            for symbol in self.index_components:
                if symbol == bar.symbol and self.get_position(symbol) == 0:
                    self.buy(symbol, 1000)
                    print(f"[{bar.timestamp_str}] Buy 1000 shares of {symbol} at {bar.close:.2f}")


class CrossProductArbitrageStrategy(Strategy):
    """
    跨品种套利(期货)
    
    策略逻辑：
    - 利用相关品种之间的价格差异进行套利
    """
    
    def __init__(self, symbol1, symbol2, spread_threshold=0.05):
        super().__init__()
        self.symbol1 = symbol1
        self.symbol2 = symbol2
        self.spread_threshold = spread_threshold
        self.prices = {symbol1: [], symbol2: []}
    
    def on_bar(self, bar):
        # 记录价格
        if bar.symbol in self.prices:
            self.prices[bar.symbol].append(bar.close)
            if len(self.prices[bar.symbol]) > 10:
                self.prices[bar.symbol].pop(0)
        
        # 当两个品种都有足够的价格数据时
        if len(self.prices[self.symbol1]) == 10 and len(self.prices[self.symbol2]) == 10:
            # 计算价差
            spread = abs(self.prices[self.symbol1][-1] - self.prices[self.symbol2][-1])
            avg_spread = sum(abs(p1 - p2) for p1, p2 in zip(self.prices[self.symbol1], self.prices[self.symbol2])) / 10
            
            # 当价差超过阈值时进行套利
            if spread > avg_spread * (1 + self.spread_threshold):
                if self.prices[self.symbol1][-1] > self.prices[self.symbol2][-1]:
                    # 买低卖高
                    if self.get_position(self.symbol2) == 0:
                        self.buy(self.symbol2, 1)
                    if self.get_position(self.symbol1) == 0:
                        self.sell(self.symbol1, 1)
                    print(f"[{bar.timestamp_str}] Arbitrage: Buy {self.symbol2}, Sell {self.symbol1} (Spread: {spread:.2f}, Avg Spread: {avg_spread:.2f})")
            
            # 当价差回归时平仓
            elif spread < avg_spread * (1 - self.spread_threshold):
                if self.get_position(self.symbol2) > 0:
                    self.close_position(self.symbol2)
                if self.get_position(self.symbol1) < 0:
                    self.close_position(self.symbol1)
                print(f"[{bar.timestamp_str}] Close arbitrage positions (Spread: {spread:.2f}, Avg Spread: {avg_spread:.2f})")


class CalendarSpreadStrategy(Strategy):
    """
    跨期套利(期货)
    
    策略逻辑：
    - 利用同一品种不同到期月份合约之间的价格差异进行套利
    """
    
    def __init__(self, near_symbol, far_symbol, spread_threshold=0.05):
        super().__init__()
        self.near_symbol = near_symbol
        self.far_symbol = far_symbol
        self.spread_threshold = spread_threshold
        self.prices = {near_symbol: [], far_symbol: []}
    
    def on_bar(self, bar):
        # 记录价格
        if bar.symbol in self.prices:
            self.prices[bar.symbol].append(bar.close)
            if len(self.prices[bar.symbol]) > 10:
                self.prices[bar.symbol].pop(0)
        
        # 当两个合约都有足够的价格数据时
        if len(self.prices[self.near_symbol]) == 10 and len(self.prices[self.far_symbol]) == 10:
            # 计算价差
            spread = self.prices[self.far_symbol][-1] - self.prices[self.near_symbol][-1]
            avg_spread = sum(f - n for f, n in zip(self.prices[self.far_symbol], self.prices[self.near_symbol])) / 10
            
            # 当价差超过阈值时进行套利
            if spread > avg_spread * (1 + self.spread_threshold):
                # 卖远买近
                if self.get_position(self.near_symbol) == 0:
                    self.buy(self.near_symbol, 1)
                if self.get_position(self.far_symbol) == 0:
                    self.sell(self.far_symbol, 1)
                print(f"[{bar.timestamp_str}] Calendar spread: Buy {self.near_symbol}, Sell {self.far_symbol} (Spread: {spread:.2f}, Avg Spread: {avg_spread:.2f})")
            
            # 当价差回归时平仓
            elif spread < avg_spread * (1 - self.spread_threshold):
                if self.get_position(self.near_symbol) > 0:
                    self.close_position(self.near_symbol)
                if self.get_position(self.far_symbol) < 0:
                    self.close_position(self.far_symbol)
                print(f"[{bar.timestamp_str}] Close calendar spread positions (Spread: {spread:.2f}, Avg Spread: {avg_spread:.2f})")


class IntradayRotationStrategy(Strategy):
    """
    日内回转交易(股票)
    
    策略逻辑：
    - 日内低买高卖，赚取差价
    """
    
    def __init__(self, profit_target=0.01, stop_loss=0.01):
        super().__init__()
        self.profit_target = profit_target
        self.stop_loss = stop_loss
        self.buy_price = 0
    
    def on_bar(self, bar):
        position = self.get_position(bar.symbol)
        
        # 日内交易，每天开盘时重置
        if bar.timestamp.hour == 9 and bar.timestamp.minute == 30:
            if position != 0:
                self.close_position(bar.symbol)
                print(f"[{bar.timestamp_str}] Reset position for intraday trading")
            self.buy_price = 0
        
        # 买入条件：价格低于当日开盘价的2%
        if position == 0 and bar.close < bar.open * 0.98:
            self.buy(bar.symbol, 1000)
            self.buy_price = bar.close
            print(f"[{bar.timestamp_str}] Buy 1000 shares at {bar.close:.2f}")
        
        # 卖出条件：达到盈利目标或止损
        elif position > 0:
            if (bar.close - self.buy_price) / self.buy_price >= self.profit_target:
                self.close_position(bar.symbol)
                print(f"[{bar.timestamp_str}] Sell 1000 shares at {bar.close:.2f} (Profit: {((bar.close - self.buy_price) / self.buy_price * 100):.2f}%)")
            elif (self.buy_price - bar.close) / self.buy_price >= self.stop_loss:
                self.close_position(bar.symbol)
                print(f"[{bar.timestamp_str}] Sell 1000 shares at {bar.close:.2f} (Loss: {((self.buy_price - bar.close) / self.buy_price * 100):.2f}%)")
        
        # 收盘前平仓
        if bar.timestamp.hour == 14 and bar.timestamp.minute == 55 and position != 0:
            self.close_position(bar.symbol)
            print(f"[{bar.timestamp_str}] Close position before market close")


class MarketMakingStrategy(Strategy):
    """
    做市商交易(期货)
    
    策略逻辑：
    - 同时挂买单和卖单，赚取买卖价差
    """
    
    def __init__(self, bid_ask_spread=0.01):
        super().__init__()
        self.bid_ask_spread = bid_ask_spread
        self.last_bid = 0
        self.last_ask = 0
    
    def on_bar(self, bar):
        current_price = bar.close
        position = self.get_position(bar.symbol)
        
        # 计算买卖报价
        bid_price = current_price - self.bid_ask_spread / 2
        ask_price = current_price + self.bid_ask_spread / 2
        
        # 调整报价
        if bid_price > self.last_bid:
            self.last_bid = bid_price
            # 买入
            if position < 1:
                self.buy(bar.symbol, 1)
                print(f"[{bar.timestamp_str}] Market making: Buy 1 contract at {bid_price:.2f}")
        
        if ask_price < self.last_ask or self.last_ask == 0:
            self.last_ask = ask_price
            # 卖出
            if position > -1:
                self.sell(bar.symbol, 1)
                print(f"[{bar.timestamp_str}] Market making: Sell 1 contract at {ask_price:.2f}")


class TurtleTradingStrategy(Strategy):
    """
    海龟交易法(期货)
    
    策略逻辑：
    - 突破20日最高价买入
    - 突破10日最低价卖出
    - 基于ATR设置止损
    """
    
    def __init__(self, entry_period=10, exit_period=5, atr_period=14, risk_percent=0.01):
        super().__init__()
        self.entry_period = entry_period
        self.exit_period = exit_period
        self.atr_period = atr_period
        self.risk_percent = risk_percent
        self.high_prices = []
        self.low_prices = []
        self.close_prices = []
        self.atr = 0
    
    def on_bar(self, bar):
        # 记录价格
        self.high_prices.append(bar.high)
        self.low_prices.append(bar.low)
        self.close_prices.append(bar.close)
        
        # 保持价格数据长度
        if len(self.high_prices) > max(self.entry_period, self.exit_period, self.atr_period):
            self.high_prices.pop(0)
            self.low_prices.pop(0)
            self.close_prices.pop(0)
        
        # 计算ATR
        if len(self.close_prices) >= 2:
            true_ranges = []
            for i in range(1, len(self.close_prices)):
                tr1 = self.high_prices[i] - self.low_prices[i]
                tr2 = abs(self.high_prices[i] - self.close_prices[i-1])
                tr3 = abs(self.low_prices[i] - self.close_prices[i-1])
                true_ranges.append(max(tr1, tr2, tr3))
            
            if len(true_ranges) >= self.atr_period:
                self.atr = sum(true_ranges[-self.atr_period:]) / self.atr_period
        
        # 当有足够的价格数据时
        if len(self.high_prices) >= self.entry_period:
            # 计算突破价格
            entry_price = max(self.high_prices[-self.entry_period:])
            exit_price = min(self.low_prices[-self.exit_period:])
            
            position = self.get_position(bar.symbol)
            
            # 买入条件：突破10日最高价（使用>=）
            if position == 0 and bar.high >= entry_price:
                # 基于ATR计算仓位
                if self.atr > 0:
                    # 风险控制：每笔交易风险不超过总资金的1%
                    position_size = int(self.risk_percent * self.get_equity() / self.atr)
                    if position_size > 0:
                        self.buy(bar.symbol, position_size)
                        print(f"[{bar.timestamp_str}] Buy {position_size} contracts at {bar.close:.2f} (Entry: {entry_price:.2f}, ATR: {self.atr:.2f})")
                else:
                    # 默认仓位大小
                    position_size = 1
                    self.buy(bar.symbol, position_size)
                    print(f"[{bar.timestamp_str}] Buy {position_size} contract at {bar.close:.2f} (Entry: {entry_price:.2f}, ATR: 0.1)")
            
            # 卖出条件：突破5日最低价（使用<=）
            elif position > 0 and bar.low <= exit_price:
                self.close_position(bar.symbol)
                print(f"[{bar.timestamp_str}] Sell {position} contracts at {bar.close:.2f} (Exit: {exit_price:.2f})")


class IndustryRotationStrategy(Strategy):
    """
    行业轮动(股票)
    
    策略逻辑：
    - 基于行业表现轮动投资
    - 买入表现最好的行业，卖出表现最差的行业
    """
    
    def __init__(self, rebalance_days=20):
        super().__init__()
        self.rebalance_days = rebalance_days
        self.day_count = 0
        self.industry_performances = {}
    
    def on_bar(self, bar):
        self.day_count += 1
        
        # 定期重新平衡组合
        if self.day_count % self.rebalance_days == 0:
            # 这里简化实现，实际需要获取行业数据
            # 假设基于最近20天的涨跌幅计算行业表现
            print(f"[{bar.timestamp_str}] Rebalancing industry rotation portfolio")
            
            # 模拟行业表现数据
            # 实际实现需要调用akshare的行业数据接口
            industries = ['tech', 'finance', 'energy', 'consumer', 'healthcare']
            self.industry_performances = {industry: np.random.randn() for industry in industries}
            
            # 排序行业表现
            sorted_industries = sorted(self.industry_performances.items(), key=lambda x: x[1], reverse=True)
            
            # 买入表现最好的行业，卖出表现最差的行业
            best_industry = sorted_industries[0][0]
            worst_industry = sorted_industries[-1][0]
            
            print(f"[{bar.timestamp_str}] Best industry: {best_industry} ({self.industry_performances[best_industry]:.2f})")
            print(f"[{bar.timestamp_str}] Worst industry: {worst_industry} ({self.industry_performances[worst_industry]:.2f})")
            
            # 实际实现需要根据行业选择具体的股票


class MachineLearningStrategy(Strategy):
    """
    机器学习(股票)
    
    策略逻辑：
    - 基于机器学习模型预测股票价格
    - 根据预测结果进行交易
    """
    
    def __init__(self):
        super().__init__()
        self.price_history = []
        self.model = None
    
    def on_bar(self, bar):
        # 记录价格历史
        self.price_history.append(bar.close)
        if len(self.price_history) > 30:
            self.price_history.pop(0)
        
        # 当有足够的历史数据时
        if len(self.price_history) == 30:
            # 这里简化实现，实际需要训练机器学习模型
            # 假设使用简单的线性回归模型
            X = np.array(range(30)).reshape(-1, 1)
            y = np.array(self.price_history)
            
            # 简单线性回归
            from sklearn.linear_model import LinearRegression
            self.model = LinearRegression()
            self.model.fit(X, y)
            
            # 预测下一个价格
            next_price = self.model.predict(np.array([[30]]))[0]
            
            # 根据预测结果进行交易
            position = self.get_position(bar.symbol)
            
            if next_price > bar.close and position == 0:
                self.buy(bar.symbol, 1000)
                print(f"[{bar.timestamp_str}] Buy 1000 shares at {bar.close:.2f} (Predicted next price: {next_price:.2f})")
            elif next_price < bar.close and position > 0:
                self.close_position(bar.symbol)
                print(f"[{bar.timestamp_str}] Sell 1000 shares at {bar.close:.2f} (Predicted next price: {next_price:.2f})")


if __name__ == "__main__":
    print("===== AKQuant 多种量化策略示例 =====")
    
    # 示例：运行双均线策略（使用股票数据）
    print("\n===== 运行双均线策略 =====")
    
    # 获取股票数据
    try:
        stock_data = ak.stock_zh_a_daily(symbol="sh600000", start_date="20230101", end_date="20231231")
        print(f"获取股票数据成功，数据量: {len(stock_data)} 条")
        
        # 运行回测
        result = aq.run_backtest(
            data=stock_data,
            strategy=DualMAFuturesStrategy,
            symbols=["sh600000"]
        )
        
        # 打印回测结果
        print("\n=== 回测结果 ===")
        print(result.metrics_df)
        # 尝试打印关键指标
        try:
            # 尝试不同的列名
            if 'total_return_pct' in result.metrics_df.index:
                print("\n=== 关键指标 ===")
                print(f"总收益率: {result.metrics_df.loc['total_return_pct', 'value']:.4f}")
                print(f"年化收益率: {result.metrics_df.loc['annualized_return', 'value']:.4f}")
                print(f"夏普比率: {result.metrics_df.loc['sharpe_ratio', 'value']:.4f}")
                print(f"最大回撤: {result.metrics_df.loc['max_drawdown_pct', 'value']:.4f}")
                print(f"胜率: {result.metrics_df.loc['win_rate', 'value']:.4f}")
            else:
                # 打印所有可用的指标
                print("\n=== 所有可用指标 ===")
                print(result.metrics_df.index.tolist())
        except Exception as e:
            print(f"打印指标失败: {e}")
    except Exception as e:
        print(f"获取股票数据失败: {e}")
    
    # 示例：运行海龟交易法（使用股票数据）
    print("\n===== 运行海龟交易法 =====")
    
    try:
        stock_data = ak.stock_zh_a_daily(symbol="sh600000", start_date="20230101", end_date="20231231")
        print(f"获取股票数据成功，数据量: {len(stock_data)} 条")
        
        # 运行回测
        result = aq.run_backtest(
            data=stock_data,
            strategy=TurtleTradingStrategy,
            symbols=["sh600000"]
        )
        
        # 打印回测结果
        print("\n=== 回测结果 ===")
        print(result.metrics_df)
        # 尝试打印关键指标
        try:
            # 尝试不同的列名
            if 'total_return_pct' in result.metrics_df.index:
                print("\n=== 关键指标 ===")
                print(f"总收益率: {result.metrics_df.loc['total_return_pct', 'value']:.4f}")
                print(f"年化收益率: {result.metrics_df.loc['annualized_return', 'value']:.4f}")
                print(f"夏普比率: {result.metrics_df.loc['sharpe_ratio', 'value']:.4f}")
                print(f"最大回撤: {result.metrics_df.loc['max_drawdown_pct', 'value']:.4f}")
                print(f"胜率: {result.metrics_df.loc['win_rate', 'value']:.4f}")
            else:
                # 打印所有可用的指标
                print("\n=== 所有可用指标 ===")
                print(result.metrics_df.index.tolist())
        except Exception as e:
            print(f"打印指标失败: {e}")
    except Exception as e:
        print(f"获取股票数据失败: {e}")
    
    # 示例：运行移动平均线策略
    print("\n===== 运行移动平均线策略 =====")
    
    try:
        from akquant_strategy_demo import MovingAverageStrategy
        stock_data = ak.stock_zh_a_daily(symbol="sh600000", start_date="20230101", end_date="20231231")
        print(f"获取股票数据成功，数据量: {len(stock_data)} 条")
        
        # 运行回测
        result = aq.run_backtest(
            data=stock_data,
            strategy=MovingAverageStrategy,
            symbols=["sh600000"]
        )
        
        # 打印回测结果
        print("\n=== 回测结果 ===")
        print(result.metrics_df)
        # 尝试打印关键指标
        try:
            # 尝试不同的列名
            if 'total_return_pct' in result.metrics_df.index:
                print("\n=== 关键指标 ===")
                print(f"总收益率: {result.metrics_df.loc['total_return_pct', 'value']:.4f}")
                print(f"年化收益率: {result.metrics_df.loc['annualized_return', 'value']:.4f}")
                print(f"夏普比率: {result.metrics_df.loc['sharpe_ratio', 'value']:.4f}")
                print(f"最大回撤: {result.metrics_df.loc['max_drawdown_pct', 'value']:.4f}")
                print(f"胜率: {result.metrics_df.loc['win_rate', 'value']:.4f}")
            else:
                # 打印所有可用的指标
                print("\n=== 所有可用指标 ===")
                print(result.metrics_df.index.tolist())
        except Exception as e:
            print(f"打印指标失败: {e}")
    except Exception as e:
        print(f"运行移动平均线策略失败: {e}")
