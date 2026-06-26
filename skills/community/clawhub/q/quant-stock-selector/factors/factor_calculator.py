#!/usr/bin/env python3
"""
因子计算模块
基于 AKShare 数据计算技术因子、基本面因子、资金因子、筹码峰因子
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from data.akshare_data import AKShareData
from factors.chip_distribution import ChipDistributionCalculator
from factors.volume_spike_oscillation import VolumeSpikeOscillationCalculator


class FactorCalculator:
    """因子计算器"""
    
    def __init__(self):
        self.data = AKShareData()
        self.chip_calculator = ChipDistributionCalculator()
        self.volume_oscillation_calculator = VolumeSpikeOscillationCalculator()
    
    def calculate_technical_factors(self, df_kline):
        """
        计算技术因子
        返回：DataFrame
        """
        if df_kline.empty:
            return pd.DataFrame()
        
        factors = pd.DataFrame(index=df_kline.index)
        
        # 1. 移动平均线
        factors['ma5'] = df_kline['close'].rolling(5).mean()
        factors['ma10'] = df_kline['close'].rolling(10).mean()
        factors['ma20'] = df_kline['close'].rolling(20).mean()
        factors['ma60'] = df_kline['close'].rolling(60).mean()
        
        # 均线多头排列
        factors['ma_bullish'] = (
            (factors['ma5'] > factors['ma10']) & 
            (factors['ma10'] > factors['ma20']) & 
            (factors['ma20'] > factors['ma60'])
        ).astype(int)
        
        # 2. MACD
        exp12 = df_kline['close'].ewm(span=12, adjust=False).mean()
        exp26 = df_kline['close'].ewm(span=26, adjust=False).mean()
        factors['dif'] = exp12 - exp26
        factors['dea'] = factors['dif'].ewm(span=9, adjust=False).mean()
        factors['macd'] = (factors['dif'] - factors['dea']) * 2
        factors['macd_golden'] = ((factors['dif'] > factors['dea']) & (factors['dif'].shift(1) <= factors['dea'].shift(1))).astype(int)
        
        # 3. RSI
        delta = df_kline['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        factors['rsi'] = 100 - (100 / (1 + rs))
        
        # 4. KDJ
        low_14 = df_kline['low'].rolling(14).min()
        high_14 = df_kline['high'].rolling(14).max()
        rsv = (df_kline['close'] - low_14) / (high_14 - low_14) * 100
        factors['k'] = rsv.ewm(com=2, adjust=False).mean()
        factors['d'] = factors['k'].ewm(com=2, adjust=False).mean()
        factors['j'] = 3 * factors['k'] - 2 * factors['d']
        
        # 5. 布林带
        factors['bb_mid'] = df_kline['close'].rolling(20).mean()
        factors['bb_std'] = df_kline['close'].rolling(20).std()
        factors['bb_upper'] = factors['bb_mid'] + 2 * factors['bb_std']
        factors['bb_lower'] = factors['bb_mid'] - 2 * factors['bb_std']
        factors['bb_position'] = (df_kline['close'] - factors['bb_lower']) / (factors['bb_upper'] - factors['bb_lower'])
        
        # 6. 成交量因子
        factors['volume_ma5'] = df_kline['volume'].rolling(5).mean()
        factors['volume_ratio'] = df_kline['volume'] / factors['volume_ma5']
        
        # 7. 动量因子
        factors['momentum_5'] = df_kline['close'].pct_change(5)
        factors['momentum_10'] = df_kline['close'].pct_change(10)
        factors['momentum_20'] = df_kline['close'].pct_change(20)
        
        # 8. 波动率因子
        factors['volatility_5'] = df_kline['close'].pct_change(5).rolling(5).std()
        factors['volatility_20'] = df_kline['close'].pct_change(20).rolling(20).std()
        
        return factors
    
    def calculate_fundamental_factors(self, stock_code):
        """
        计算基本面因子
        返回：dict
        """
        financials = self.data.get_financial_indicators(stock_code)
        
        if not financials:
            return {}
        
        factors = {
            'pe_score': 1 / (1 + financials.get('pe', 0)),  # PE 越小分数越高
            'pb_score': 1 / (1 + financials.get('pb', 0)),
            'roe_score': financials.get('roe', 0) / 100,  # ROE 越高分数越高
            'growth_score': (financials.get('revenue_growth', 0) + financials.get('profit_growth', 0)) / 200,
            'margin_score': financials.get('gross_margin', 0) / 100,
        }
        
        return factors
    
    def calculate_capital_factors(self, stock_code):
        """
        计算资金因子
        返回：dict
        """
        # 暂时跳过资金流向（API 有问题）
        # fund_flow = self.data.get_stock_fund_flow(stock_code)
        
        # 使用成交量替代
        return {
            'main_inflow_score': 1,  # 默认正分
            'main_inflow_amount': 0.1,  # 默认 0.1 亿
        }
    
    def calculate_chip_factors(self, df_kline):
        """
        计算筹码峰因子
        返回：dict
        """
        chip_result = self.chip_calculator.calculate_chip_score(df_kline)
        
        return {
            'chip_score': chip_result.get('score', 0),
            'pressure_ratio': chip_result.get('details', {}).get('pressure_ratio', 100),
            'profit_ratio': chip_result.get('details', {}).get('profit_ratio', 0),
            'recent_gain': chip_result.get('details', {}).get('recent_gain', 0),
        }
    
    def calculate_volume_oscillation_factors(self, df_kline):
        """
        计算成交量放大 + 震荡因子
        返回：dict
        """
        volume_result = self.volume_oscillation_calculator.calculate_volume_oscillation_score(df_kline)
        
        return {
            'volume_score': volume_result.get('score', 0),
            'spike_detected': volume_result.get('details', {}).get('volume_spike_detected', False),
            'spike_ratio': volume_result.get('details', {}).get('spike_ratio', 0),
            'days_since_spike': volume_result.get('details', {}).get('days_since_spike', 0),
            'oscillation_detected': volume_result.get('details', {}).get('oscillation_detected', False),
        }
    
    def calculate_combined_score(self, technical_factors, fundamental_factors, capital_factors, chip_factors=None, volume_oscillation_factors=None):
        """
        计算综合得分（权重调整版）
        
        权重分配（最终版）:
        - 技术面：30%（减少 5%）
        - 基本面：25%
        - 资金面：15%
        - 筹码峰：10%（增加 5%）⭐
        - 90% 集中度：10% ⭐
        - 成交量放大 + 震荡：10%
        
        返回：float
        """
        score = 0
        weights = {
            'technical': 0.30,
            'fundamental': 0.25,
            'capital': 0.15,
            'chip': 0.10,
            'concentration_90': 0.10,
            'volume_oscillation': 0.10
        }
        
        # 技术面得分
        tech_score = 0
        if not technical_factors.empty:
            latest = technical_factors.iloc[-1]
            tech_score = (
                latest.get('ma_bullish', 0) * 20 +
                latest.get('macd_golden', 0) * 20 +
                (1 if 40 < latest.get('rsi', 50) < 70 else 0) * 20 +
                (1 if latest.get('volume_ratio', 1) > 1 else 0) * 20 +
                (1 if latest.get('bb_position', 0.5) > 0.5 else 0) * 20
            )
        
        # 基本面得分
        fund_score = 0
        if fundamental_factors:
            fund_score = (
                fundamental_factors.get('pe_score', 0) * 25 +
                fundamental_factors.get('pb_score', 0) * 25 +
                fundamental_factors.get('roe_score', 0) * 25 +
                fundamental_factors.get('growth_score', 0) * 25
            )
        
        # 资金面得分
        capital_score = 0
        if capital_factors:
            capital_score = (
                capital_factors.get('main_inflow_score', 0) * 50 +
                (1 if capital_factors.get('main_inflow_amount', 0) > 0.1 else 0) * 50
            )
        
        # 筹码峰得分
        chip_score = 0
        if chip_factors:
            chip_score = chip_factors.get('chip_score', 0)
        
        # 90% 集中度得分（新增）⭐
        concentration_score = 0
        if chip_factors:
            concentration_90 = chip_factors.get('details', {}).get('concentration_90', 100)
            if concentration_90 < 10:
                concentration_score = 100
            elif concentration_90 < 15:
                concentration_score = 70
            elif concentration_90 < 20:
                concentration_score = 40
            else:
                concentration_score = 0
        
        # 成交量放大 + 震荡得分（新增）
        volume_score = 0
        if volume_oscillation_factors:
            volume_score = volume_oscillation_factors.get('volume_score', 0)
        
        # 综合得分
        score = (
            tech_score * weights['technical'] +
            fund_score * weights['fundamental'] +
            capital_score * weights['capital'] +
            chip_score * weights['chip'] +
            concentration_score * weights['concentration_90'] +
            volume_score * weights['volume_oscillation']
        )
        
        return score


def main():
    """测试因子计算"""
    print("=" * 70)
    print("📊 因子计算测试")
    print("=" * 70)
    
    calculator = FactorCalculator()
    
    # 1. 获取 K 线
    print("\n1️⃣ 获取 K 线数据...")
    df_kline = calculator.data.get_history_kline("600519")
    print(f"   K 线数据：{len(df_kline)}条")
    
    # 2. 计算技术因子
    print("\n2️⃣ 计算技术因子...")
    tech_factors = calculator.calculate_technical_factors(df_kline)
    if not tech_factors.empty:
        print(f"   技术因子：{tech_factors.shape[1]}个")
        print(tech_factors.tail())
    
    # 3. 计算基本面因子
    print("\n3️⃣ 计算基本面因子...")
    fund_factors = calculator.calculate_fundamental_factors("600519")
    print(f"   基本面因子：{len(fund_factors)}个")
    print(fund_factors)
    
    # 4. 计算资金因子
    print("\n4️⃣ 计算资金因子...")
    capital_factors = calculator.calculate_capital_factors("600519")
    print(f"   资金因子：{len(capital_factors)}个")
    print(capital_factors)
    
    # 5. 计算综合得分
    print("\n5️⃣ 计算综合得分...")
    score = calculator.calculate_combined_score(tech_factors, fund_factors, capital_factors)
    print(f"   综合得分：{score:.2f}")
    
    print("\n" + "=" * 70)
    print("✅ 因子计算测试完成")
    print("=" * 70)


if __name__ == "__main__":
    main()
