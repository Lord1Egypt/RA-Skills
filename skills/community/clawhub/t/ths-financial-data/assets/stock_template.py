#!/usr/bin/env python3

"""
股票数据分析模板 - stock_template.py

此文件提供股票数据分析的基础模板，包含常用分析功能和可视化。
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import numpy as np

# 设置中文字体和图表样式
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")


class StockAnalyzer:
    """股票数据分析器"""
    
    def __init__(self, ths):
        """
        初始化分析器
        
        Args:
            ths: THS连接对象
        """
        self.ths = ths
        
    def get_stock_data(self, stock_code: str, days: int = 100) -> Optional[pd.DataFrame]:
        """
        获取股票数据
        
        Args:
            stock_code: 股票代码
            days: 数据天数
            
        Returns:
            包含基础信息和K线数据的DataFrame
        """
        # 获取基础信息
        basic_response = self.ths.market_data_cn(stock_code, "基础数据")
        
        # 获取K线数据
        kline_response = self.ths.klines(stock_code, interval="day", count=days)
        
        if basic_response.success and kline_response.success:
            basic_df = basic_response.df
            kline_df = kline_response.df
            
            # 添加基础信息到K线数据
            if not basic_df.empty and not kline_df.empty:
                kline_df['股票名称'] = basic_df.iloc[0]['股票名称'] if '股票名称' in basic_df.columns else stock_code
                kline_df['股票代码'] = stock_code
                
            return kline_df
        
        return None
    
    def calculate_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        计算技术指标
        
        Args:
            df: 包含OHLCV数据的DataFrame
            
        Returns:
            添加技术指标的DataFrame
        """
        if df.empty:
            return df
        
        # 移动平均线
        df['MA5'] = df['close'].rolling(window=5).mean()
        df['MA10'] = df['close'].rolling(window=10).mean()
        df['MA20'] = df['close'].rolling(window=20).mean()
        df['MA60'] = df['close'].rolling(window=60).mean()
        
        # RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # MACD
        exp1 = df['close'].ewm(span=12, adjust=False).mean()
        exp2 = df['close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = exp1 - exp2
        df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']
        
        # 布林带
        df['BB_Middle'] = df['close'].rolling(window=20).mean()
        bb_std = df['close'].rolling(window=20).std()
        df['BB_Upper'] = df['BB_Middle'] + (bb_std * 2)
        df['BB_Lower'] = df['BB_Middle'] - (bb_std * 2)
        
        # 成交量指标
        df['Volume_MA5'] = df['volume'].rolling(window=5).mean()
        df['Volume_MA10'] = df['volume'].rolling(window=10).mean()
        
        return df
    
    def plot_price_chart(self, df: pd.DataFrame, title: str = ""):
        """
        绘制价格图表
        
        Args:
            df: 包含价格数据的DataFrame
            title: 图表标题
        """
        if df.empty:
            print("数据为空，无法绘制图表")
            return
            
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), 
                                       gridspec_kw={'height_ratios': [3, 1]})
        
        # 价格和移动平均线
        ax1.plot(df.index, df['close'], label='收盘价', linewidth=1.5, color='black')
        ax1.plot(df.index, df['MA5'], label='MA5', linewidth=1, alpha=0.7)
        ax1.plot(df.index, df['MA10'], label='MA10', linewidth=1, alpha=0.7)
        ax1.plot(df.index, df['MA20'], label='MA20', linewidth=1, alpha=0.7)
        
        # 布林带
        ax1.fill_between(df.index, df['BB_Upper'], df['BB_Lower'], 
                        alpha=0.2, color='gray', label='布林带')
        
        ax1.set_title(f'{df.iloc[0]["股票名称"]} ({df.iloc[0]["股票代码"]}) - 价格走势' if not title else title)
        ax1.set_ylabel('价格')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 成交量
        colors = ['red' if row['close'] >= row['open'] else 'green' 
                  for _, row in df.iterrows()]
        ax2.bar(df.index, df['volume'], color=colors, alpha=0.7)
        ax2.plot(df.index, df['Volume_MA5'], label='成交量MA5', color='blue', linewidth=1)
        
        ax2.set_ylabel('成交量')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def plot_technical_indicators(self, df: pd.DataFrame):
        """
        绘制技术指标图表
        
        Args:
            df: 包含技术指标的DataFrame
        """
        if df.empty:
            print("数据为空，无法绘制技术指标")
            return
            
        fig, axes = plt.subplots(3, 1, figsize=(12, 10))
        
        # RSI
        axes[0].plot(df.index, df['RSI'], label='RSI', linewidth=1.5)
        axes[0].axhline(y=70, color='r', linestyle='--', alpha=0.7, label='超买线(70)')
        axes[0].axhline(y=30, color='g', linestyle='--', alpha=0.7, label='超卖线(30)')
        axes[0].set_title('RSI指标')
        axes[0].set_ylabel('RSI')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # MACD
        axes[1].plot(df.index, df['MACD'], label='MACD', linewidth=1.5)
        axes[1].plot(df.index, df['MACD_Signal'], label='信号线', linewidth=1)
        axes[1].bar(df.index, df['MACD_Histogram'], 
                    label='MACD柱', alpha=0.5, color='gray')
        axes[1].set_title('MACD指标')
        axes[1].set_ylabel('MACD')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        # 成交量对比
        axes[2].bar(df.index, df['volume'], 
                   alpha=0.7, label='成交量', color='lightblue')
        axes[2].plot(df.index, df['Volume_MA5'], 
                     label='5日均量', color='blue', linewidth=1.5)
        axes[2].plot(df.index, df['Volume_MA10'], 
                     label='10日均量', color='red', linewidth=1.5)
        axes[2].set_title('成交量分析')
        axes[2].set_ylabel('成交量')
        axes[2].legend()
        axes[2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def generate_report(self, stock_code: str, days: int = 100):
        """
        生成股票分析报告
        
        Args:
            stock_code: 股票代码
            days: 分析天数
        """
        df = self.get_stock_data(stock_code, days)
        
        if df is None or df.empty:
            print(f"无法获取股票 {stock_code} 的数据")
            return
        
        # 计算技术指标
        df = self.calculate_technical_indicators(df)
        
        # 打印基本信息
        print("=" * 50)
        print(f"股票分析报告: {df.iloc[0]['股票名称']} ({stock_code})")
        print("=" * 50)
        
        # 最新价格信息
        latest = df.iloc[-1]
        print(f"最新价格: {latest['close']:.2f}")
        print(f"涨跌幅: {latest.get('涨跌幅', 0):.2f}%")
        print(f"成交量: {latest['volume']:,.0f}")
        
        # 技术指标状态
        print("\n技术指标状态:")
        print(f"RSI: {latest['RSI']:.2f} {'(超买)' if latest['RSI'] > 70 else '(超卖)' if latest['RSI'] < 30 else '(正常)'}")
        print(f"MACD: {latest['MACD']:.4f}")
        print(f"MACD信号线: {latest['MACD_Signal']:.4f}")
        
        # 移动平均线关系
        ma_relation = ""
        if latest['close'] > latest['MA5'] > latest['MA10'] > latest['MA20']:
            ma_relation = "多头排列"
        elif latest['close'] < latest['MA5'] < latest['MA10'] < latest['MA20']:
            ma_relation = "空头排列"
        else:
            ma_relation = "震荡整理"
        print(f"均线状态: {ma_relation}")
        
        # 绘制图表
        self.plot_price_chart(df)
        self.plot_technical_indicators(df)


def main():
    """主函数 - 示例用法"""
    from thsdk import THS
    
    # 使用示例
    with THS() as ths:
        analyzer = StockAnalyzer(ths)
        
        # 分析单个股票
        analyzer.generate_report("000001", days=100)
        
        # 也可以单独获取数据进行分析
        df = analyzer.get_stock_data("000001", 50)
        if df is not None:
            df = analyzer.calculate_technical_indicators(df)
            analyzer.plot_price_chart(df)


if __name__ == "__main__":
    main()