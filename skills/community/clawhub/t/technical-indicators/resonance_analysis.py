"""
多指标共振分析模块 - Multi-Indicator Resonance Analysis

支持 5 种共振类型:
1. 趋势共振 (MA + MACD + ADX)
2. 动量共振 (KDJ + RSI + CCI)
3. 量价共振 (成交量 + OBV + 价格)
4. 波动率共振 (BOLL + ATR)
5. 全指标共振 (5+ 指标同时信号)

信号强度评分标准:
- 80-100: 强烈信号
- 60-80: 强信号
- 40-60: 中等信号
- <40: 弱信号
"""

import akshare as ak
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum


class SignalType(Enum):
    STRONG_BUY = "强买入"
    BUY = "买入"
    NEUTRAL = "中性"
    SELL = "卖出"
    STRONG_SELL = "强卖出"


class ResonanceType(Enum):
    TREND = "趋势共振"
    MOMENTUM = "动量共振"
    VOLUME_PRICE = "量价共振"
    VOLATILITY = "波动率共振"
    ALL_INDICATORS = "全指标共振"


@dataclass
class ResonanceSignal:
    """共振信号数据结构"""
    code: str
    date: str
    resonance_type: str
    signal_type: str
    strength: int  # 0-100
    matched_indicators: int
    total_indicators: int
    details: Dict
    confidence: str  # 强烈/强/中等/弱


class ResonanceAnalyzer:
    """多指标共振分析器"""
    
    def __init__(self, config: Optional[Dict] = None):
        """
        初始化分析器
        
        Args:
            config: 配置字典，可自定义各共振类型的阈值和权重
        """
        self.config = config or self._default_config()
        self.cache = {}  # 数据缓存
    
    def _default_config(self) -> Dict:
        """默认配置"""
        return {
            "trend": {
                "adx_threshold": 25,
                "weight": 1.0
            },
            "momentum": {
                "rsi_oversold": 30,
                "rsi_overbought": 70,
                "cci_threshold": 100,
                "weight": 1.0
            },
            "volume_price": {
                "volume_ratio_threshold": 1.5,  # 放量阈值
                "weight": 1.0
            },
            "volatility": {
                "atr_multiplier": 1.5,  # ATR 放大阈值
                "weight": 1.0
            },
            "all_indicators": {
                "min_categories": 3,  # 最少需要多少个类别同时信号
                "weight": 1.5  # 全指标共振权重更高
            },
            "scoring": {
                "strong_signal": 80,
                "signal": 60,
                "medium": 40
            }
        }
    
    def get_stock_history(self, code: str, start_date: str = None, 
                         end_date: str = None, days: int = 365) -> pd.DataFrame:
        """获取股票历史数据"""
        cache_key = f"{code}_{start_date}_{end_date}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        if end_date is None:
            end_date = datetime.now().strftime("%Y%m%d")
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=days)).strftime("%Y%m%d")
        
        try:
            df = ak.stock_zh_a_hist(
                symbol=code, 
                period="daily", 
                start_date=start_date, 
                end_date=end_date, 
                adjust="qfq"
            )
            # 标准化列名
            df = df.rename(columns={
                '日期': 'date',
                '开盘': 'open',
                '收盘': 'close',
                '最高': 'high',
                '最低': 'low',
                '成交量': 'volume',
                '成交额': 'amount',
                '振幅': 'amplitude',
                '涨跌幅': 'pct_change',
                '涨跌额': 'change',
                '换手率': 'turnover'
            })
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date').reset_index(drop=True)
            self.cache[cache_key] = df
            return df
        except Exception as e:
            print(f"获取历史数据失败：{e}")
            return pd.DataFrame()
    
    def calculate_ma(self, df: pd.DataFrame, periods: List[int] = [5, 10, 20, 60]) -> pd.DataFrame:
        """计算移动平均线"""
        for period in periods:
            df[f'ma{period}'] = df['close'].rolling(window=period).mean()
        return df
    
    def calculate_macd(self, df: pd.DataFrame, fast: int = 12, slow: int = 26, 
                      signal: int = 9) -> pd.DataFrame:
        """计算 MACD 指标"""
        exp1 = df['close'].ewm(span=fast, adjust=False).mean()
        exp2 = df['close'].ewm(span=slow, adjust=False).mean()
        df['macd'] = exp1 - exp2
        df['macd_signal'] = df['macd'].ewm(span=signal, adjust=False).mean()
        df['macd_hist'] = df['macd'] - df['macd_signal']
        return df
    
    def calculate_adx(self, df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """计算 ADX 指标"""
        df['tr'] = np.maximum(
            df['high'] - df['low'],
            np.maximum(
                abs(df['high'] - df['close'].shift(1)),
                abs(df['low'] - df['close'].shift(1))
            )
        )
        df['atr'] = df['tr'].rolling(window=period).mean()
        
        df['+dm'] = np.where(
            (df['high'] - df['high'].shift(1)) > (df['low'].shift(1) - df['low']),
            np.maximum(0, df['high'] - df['high'].shift(1)),
            0
        )
        df['-dm'] = np.where(
            (df['low'].shift(1) - df['low']) > (df['high'] - df['high'].shift(1)),
            np.maximum(0, df['low'].shift(1) - df['low']),
            0
        )
        
        df['+di'] = 100 * (df['+dm'].rolling(window=period).mean() / df['atr'])
        df['-di'] = 100 * (df['-dm'].rolling(window=period).mean() / df['atr'])
        
        dx = 100 * abs(df['+di'] - df['-di']) / (df['+di'] + df['-di'])
        df['adx'] = dx.rolling(window=period).mean()
        
        return df
    
    def calculate_kdj(self, df: pd.DataFrame, n: int = 9, m1: int = 3, 
                     m2: int = 3) -> pd.DataFrame:
        """计算 KDJ 指标"""
        low_n = df['low'].rolling(window=n).min()
        high_n = df['high'].rolling(window=n).max()
        rsv = (df['close'] - low_n) / (high_n - low_n) * 100
        
        df['k'] = rsv.ewm(com=m1-1, adjust=False).mean()
        df['d'] = df['k'].ewm(com=m2-1, adjust=False).mean()
        df['j'] = 3 * df['k'] - 2 * df['d']
        
        return df
    
    def calculate_rsi(self, df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """计算 RSI 指标"""
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        return df
    
    def calculate_cci(self, df: pd.DataFrame, period: int = 20) -> pd.DataFrame:
        """计算 CCI 指标"""
        tp = (df['high'] + df['low'] + df['close']) / 3
        ma = tp.rolling(window=period).mean()
        mad = tp.rolling(window=period).apply(lambda x: np.abs(x - x.mean()).mean())
        df['cci'] = (tp - ma) / (0.015 * mad)
        
        return df
    
    def calculate_obv(self, df: pd.DataFrame) -> pd.DataFrame:
        """计算 OBV 指标"""
        df['obv'] = np.where(
            df['close'] > df['close'].shift(1),
            df['volume'],
            np.where(df['close'] < df['close'].shift(1), -df['volume'], 0)
        ).cumsum()
        
        return df
    
    def calculate_boll(self, df: pd.DataFrame, period: int = 20, 
                      std_dev: float = 2.0) -> pd.DataFrame:
        """计算布林带"""
        df['boll_middle'] = df['close'].rolling(window=period).mean()
        std = df['close'].rolling(window=period).std()
        df['boll_upper'] = df['boll_middle'] + (std * std_dev)
        df['boll_lower'] = df['boll_middle'] - (std * std_dev)
        df['boll_bandwidth'] = (df['boll_upper'] - df['boll_lower']) / df['boll_middle'] * 100
        
        return df
    
    def calculate_atr(self, df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """计算 ATR 指标"""
        df['tr'] = np.maximum(
            df['high'] - df['low'],
            np.maximum(
                abs(df['high'] - df['close'].shift(1)),
                abs(df['low'] - df['close'].shift(1))
            )
        )
        df['atr'] = df['tr'].rolling(window=period).mean()
        
        return df
    
    def calculate_all_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """计算所有需要的指标"""
        df = self.calculate_ma(df)
        df = self.calculate_macd(df)
        df = self.calculate_adx(df)
        df = self.calculate_kdj(df)
        df = self.calculate_rsi(df)
        df = self.calculate_cci(df)
        df = self.calculate_obv(df)
        df = self.calculate_boll(df)
        df = self.calculate_atr(df)
        
        return df
    
    def check_trend_resonance(self, df: pd.DataFrame, idx: int) -> Tuple[bool, bool, Dict]:
        """
        检查趋势共振 (MA + MACD + ADX)
        
        Returns:
            (buy_signal, sell_signal, details)
        """
        if idx < 60:  # 需要足够的数据
            return False, False, {}
        
        row = df.iloc[idx]
        prev_row = df.iloc[idx - 1]
        
        # MA 金叉/死叉 (使用 MA5 和 MA20)
        ma_golden_cross = (row['ma5'] > row['ma20']) and (prev_row['ma5'] <= prev_row['ma20'])
        ma_death_cross = (row['ma5'] < row['ma20']) and (prev_row['ma5'] >= prev_row['ma20'])
        
        # MACD 金叉/死叉
        macd_golden_cross = (row['macd'] > row['macd_signal']) and (prev_row['macd'] <= prev_row['macd_signal'])
        macd_death_cross = (row['macd'] < row['macd_signal']) and (prev_row['macd'] >= prev_row['macd_signal'])
        
        # ADX > 25 (趋势强度)
        adx_strong = row['adx'] > self.config['trend']['adx_threshold']
        
        # 强买入：MA 金叉 + MACD 金叉 + ADX>25
        buy_signal = ma_golden_cross and macd_golden_cross and adx_strong
        
        # 强卖出：MA 死叉 + MACD 死叉 + ADX>25
        sell_signal = ma_death_cross and macd_death_cross and adx_strong
        
        details = {
            'ma_golden_cross': ma_golden_cross,
            'ma_death_cross': ma_death_cross,
            'macd_golden_cross': macd_golden_cross,
            'macd_death_cross': macd_death_cross,
            'adx': round(row['adx'], 2),
            'adx_strong': adx_strong,
            'matched': sum([ma_golden_cross or ma_death_cross, 
                           macd_golden_cross or macd_death_cross, 
                           adx_strong])
        }
        
        return buy_signal, sell_signal, details
    
    def check_momentum_resonance(self, df: pd.DataFrame, idx: int) -> Tuple[bool, bool, Dict]:
        """
        检查动量共振 (KDJ + RSI + CCI)
        
        Returns:
            (buy_signal, sell_signal, details)
        """
        if idx < 30:
            return False, False, {}
        
        row = df.iloc[idx]
        prev_row = df.iloc[idx - 1]
        
        # KDJ 金叉/死叉
        kdj_golden_cross = (row['k'] > row['d']) and (prev_row['k'] <= prev_row['d'])
        kdj_death_cross = (row['k'] < row['d']) and (prev_row['k'] >= prev_row['d'])
        
        # RSI 超买/超卖
        rsi_oversold = row['rsi'] < self.config['momentum']['rsi_oversold']
        rsi_overbought = row['rsi'] > self.config['momentum']['rsi_overbought']
        
        # CCI 极端值
        cci_oversold = row['cci'] < -self.config['momentum']['cci_threshold']
        cci_overbought = row['cci'] > self.config['momentum']['cci_threshold']
        
        # 强买入：KDJ 金叉 + RSI<30 + CCI<-100
        buy_signal = kdj_golden_cross and rsi_oversold and cci_oversold
        
        # 强卖出：KDJ 死叉 + RSI>70 + CCI>100
        sell_signal = kdj_death_cross and rsi_overbought and cci_overbought
        
        details = {
            'kdj_golden_cross': kdj_golden_cross,
            'kdj_death_cross': kdj_death_cross,
            'rsi': round(row['rsi'], 2),
            'rsi_oversold': rsi_oversold,
            'rsi_overbought': rsi_overbought,
            'cci': round(row['cci'], 2),
            'cci_oversold': cci_oversold,
            'cci_overbought': cci_overbought,
            'matched': sum([kdj_golden_cross or kdj_death_cross,
                           rsi_oversold or rsi_overbought,
                           cci_oversold or cci_overbought])
        }
        
        return buy_signal, sell_signal, details
    
    def check_volume_price_resonance(self, df: pd.DataFrame, idx: int) -> Tuple[bool, bool, Dict]:
        """
        检查量价共振 (成交量 + OBV + 价格)
        
        Returns:
            (buy_signal, sell_signal, details)
        """
        if idx < 30:
            return False, False, {}
        
        row = df.iloc[idx]
        prev_row = df.iloc[idx - 1]
        
        # 成交量均线
        volume_ma = df['volume'].rolling(window=20).mean().iloc[idx]
        volume_ratio = row['volume'] / volume_ma if volume_ma > 0 else 1
        
        # 放量/缩量
        volume_increase = volume_ratio > self.config['volume_price']['volume_ratio_threshold']
        volume_decrease = volume_ratio < 1
        
        # OBV 上升/下降
        obv_rise = row['obv'] > prev_row['obv']
        obv_fall = row['obv'] < prev_row['obv']
        
        # 价格上涨/下跌
        price_rise = row['close'] > prev_row['close']
        price_fall = row['close'] < prev_row['close']
        
        # 强买入：放量 + OBV 上升 + 价格上涨
        buy_signal = volume_increase and obv_rise and price_rise
        
        # 强卖出：缩量 + OBV 下降 + 价格下跌
        sell_signal = volume_decrease and obv_fall and price_fall
        
        details = {
            'volume_ratio': round(volume_ratio, 2),
            'volume_increase': volume_increase,
            'volume_decrease': volume_decrease,
            'obv_rise': obv_rise,
            'obv_fall': obv_fall,
            'price_rise': price_rise,
            'price_fall': price_fall,
            'matched': sum([volume_increase or volume_decrease,
                           obv_rise or obv_fall,
                           price_rise or price_fall])
        }
        
        return buy_signal, sell_signal, details
    
    def check_volatility_resonance(self, df: pd.DataFrame, idx: int) -> Tuple[bool, bool, Dict]:
        """
        检查波动率共振 (BOLL + ATR)
        
        Returns:
            (breakout_signal, contraction_signal, details)
        """
        if idx < 60:
            return False, False, {}
        
        row = df.iloc[idx]
        prev_row = df.iloc[idx - 1]
        
        # 价格突破 BOLL 上轨
        breakout_upper = row['close'] > row['boll_upper']
        
        # ATR 放大 (相比 20 日均值)
        atr_ma = df['atr'].rolling(window=20).mean().iloc[idx]
        atr_expand = row['atr'] > atr_ma * self.config['volatility']['atr_multiplier']
        
        # BOLL 带宽收缩
        boll_ma = df['boll_bandwidth'].rolling(window=20).mean().iloc[idx]
        bandwidth_contract = row['boll_bandwidth'] < boll_ma
        
        # ATR 下降
        atr_decrease = row['atr'] < prev_row['atr']
        
        # 突破信号：价格突破 BOLL 上轨 + ATR 放大
        breakout_signal = breakout_upper and atr_expand
        
        # 收缩信号：BOLL 带宽收缩 + ATR 下降
        contraction_signal = bandwidth_contract and atr_decrease
        
        details = {
            'breakout_upper': breakout_upper,
            'atr_expand': atr_expand,
            'bandwidth_contract': bandwidth_contract,
            'atr_decrease': atr_decrease,
            'atr': round(row['atr'], 2),
            'boll_bandwidth': round(row['boll_bandwidth'], 2),
            'matched': sum([breakout_upper, atr_expand, bandwidth_contract, atr_decrease])
        }
        
        return breakout_signal, contraction_signal, details
    
    def check_all_indicators_resonance(self, df: pd.DataFrame, idx: int) -> Tuple[bool, bool, Dict]:
        """
        检查全指标共振 (5+ 指标同时信号)
        
        Returns:
            (buy_signal, sell_signal, details)
        """
        # 检查各个类别的共振
        trend_buy, trend_sell, trend_details = self.check_trend_resonance(df, idx)
        momentum_buy, momentum_sell, momentum_details = self.check_momentum_resonance(df, idx)
        volume_buy, volume_sell, volume_details = self.check_volume_price_resonance(df, idx)
        vol_breakout, vol_contract, vol_details = self.check_volatility_resonance(df, idx)
        
        # 统计同向信号数量
        buy_categories = sum([
            1 if trend_buy else 0,
            1 if momentum_buy else 0,
            1 if volume_buy else 0,
            1 if vol_breakout else 0  # 突破视为买入信号
        ])
        
        sell_categories = sum([
            1 if trend_sell else 0,
            1 if momentum_sell else 0,
            1 if volume_sell else 0,
            1 if vol_contract else 0  # 收缩视为卖出/观望信号
        ])
        
        min_categories = self.config['all_indicators']['min_categories']
        
        # 3 个以上类别同时发出同向信号
        buy_signal = buy_categories >= min_categories
        sell_signal = sell_categories >= min_categories
        
        details = {
            'trend_signal': 'buy' if trend_buy else ('sell' if trend_sell else 'none'),
            'momentum_signal': 'buy' if momentum_buy else ('sell' if momentum_sell else 'none'),
            'volume_signal': 'buy' if volume_buy else ('sell' if volume_sell else 'none'),
            'volatility_signal': 'breakout' if vol_breakout else ('contract' if vol_contract else 'none'),
            'buy_categories': buy_categories,
            'sell_categories': sell_categories,
            'min_required': min_categories
        }
        
        return buy_signal, sell_signal, details
    
    def calculate_strength(self, matched: int, total: int, weight: float = 1.0) -> int:
        """
        计算信号强度 (0-100)
        
        Args:
            matched: 符合的指标数
            total: 总指标数
            weight: 权重系数
        
        Returns:
            强度分数 (0-100)
        """
        if total == 0:
            return 0
        
        base_strength = (matched / total) * 100
        weighted_strength = min(100, base_strength * weight)
        
        return int(weighted_strength)
    
    def get_confidence_level(self, strength: int) -> str:
        """根据强度获取置信等级"""
        if strength >= self.config['scoring']['strong_signal']:
            return "强烈"
        elif strength >= self.config['scoring']['signal']:
            return "强"
        elif strength >= self.config['scoring']['medium']:
            return "中等"
        else:
            return "弱"
    
    def analyze_resonance(self, code: str, date: str = None) -> List[ResonanceSignal]:
        """
        分析指定日期的共振信号
        
        Args:
            code: 股票代码
            date: 分析日期 (None 表示最新日期)
        
        Returns:
            共振信号列表
        """
        df = self.get_stock_history(code, days=500)
        if df.empty:
            return []
        
        # 计算所有指标
        df = self.calculate_all_indicators(df)
        
        # 确定分析日期索引
        if date is None:
            idx = len(df) - 1
        else:
            date_pd = pd.to_datetime(date)
            df_dates = df['date']
            matching_idx = df_dates[df_dates == date_pd].index
            if len(matching_idx) == 0:
                # 找最接近的日期
                idx = (df_dates - date_pd).abs().argmin()
            else:
                idx = matching_idx[0]
        
        if idx < 60 or idx >= len(df):
            return []
        
        signals = []
        analysis_date = df.iloc[idx]['date'].strftime('%Y-%m-%d')
        
        # 1. 趋势共振
        trend_buy, trend_sell, trend_details = self.check_trend_resonance(df, idx)
        if trend_buy or trend_sell:
            matched = trend_details['matched']
            strength = self.calculate_strength(matched, 3, self.config['trend']['weight'])
            signals.append(ResonanceSignal(
                code=code,
                date=analysis_date,
                resonance_type=ResonanceType.TREND.value,
                signal_type=SignalType.STRONG_BUY.value if trend_buy else SignalType.STRONG_SELL.value,
                strength=strength,
                matched_indicators=matched,
                total_indicators=3,
                details=trend_details,
                confidence=self.get_confidence_level(strength)
            ))
        
        # 2. 动量共振
        mom_buy, mom_sell, mom_details = self.check_momentum_resonance(df, idx)
        if mom_buy or mom_sell:
            matched = mom_details['matched']
            strength = self.calculate_strength(matched, 3, self.config['momentum']['weight'])
            signals.append(ResonanceSignal(
                code=code,
                date=analysis_date,
                resonance_type=ResonanceType.MOMENTUM.value,
                signal_type=SignalType.STRONG_BUY.value if mom_buy else SignalType.STRONG_SELL.value,
                strength=strength,
                matched_indicators=matched,
                total_indicators=3,
                details=mom_details,
                confidence=self.get_confidence_level(strength)
            ))
        
        # 3. 量价共振
        vol_buy, vol_sell, vol_details = self.check_volume_price_resonance(df, idx)
        if vol_buy or vol_sell:
            matched = vol_details['matched']
            strength = self.calculate_strength(matched, 3, self.config['volume_price']['weight'])
            signals.append(ResonanceSignal(
                code=code,
                date=analysis_date,
                resonance_type=ResonanceType.VOLUME_PRICE.value,
                signal_type=SignalType.STRONG_BUY.value if vol_buy else SignalType.STRONG_SELL.value,
                strength=strength,
                matched_indicators=matched,
                total_indicators=3,
                details=vol_details,
                confidence=self.get_confidence_level(strength)
            ))
        
        # 4. 波动率共振
        vol_breakout, vol_contract, vol_details = self.check_volatility_resonance(df, idx)
        if vol_breakout or vol_contract:
            matched = vol_details['matched']
            strength = self.calculate_strength(matched, 4, self.config['volatility']['weight'])
            signals.append(ResonanceSignal(
                code=code,
                date=analysis_date,
                resonance_type=ResonanceType.VOLATILITY.value,
                signal_type=SignalType.STRONG_BUY.value if vol_breakout else SignalType.SELL.value,
                strength=strength,
                matched_indicators=matched,
                total_indicators=4,
                details=vol_details,
                confidence=self.get_confidence_level(strength)
            ))
        
        # 5. 全指标共振
        all_buy, all_sell, all_details = self.check_all_indicators_resonance(df, idx)
        if all_buy or all_sell:
            matched = all_details['buy_categories'] if all_buy else all_details['sell_categories']
            total = 4  # 4 个类别
            strength = self.calculate_strength(matched, total, self.config['all_indicators']['weight'])
            signals.append(ResonanceSignal(
                code=code,
                date=analysis_date,
                resonance_type=ResonanceType.ALL_INDICATORS.value,
                signal_type=SignalType.STRONG_BUY.value if all_buy else SignalType.STRONG_SELL.value,
                strength=strength,
                matched_indicators=matched,
                total_indicators=total,
                details=all_details,
                confidence=self.get_confidence_level(strength)
            ))
        
        return signals
    
    def backtest(self, code: str, start_date: str = None, end_date: str = None,
                hold_days: int = 5, stop_loss: float = 0.05, 
                take_profit: float = 0.10) -> Dict:
        """
        历史回测
        
        Args:
            code: 股票代码
            start_date: 回测开始日期
            end_date: 回测结束日期
            hold_days: 持仓天数
            stop_loss: 止损比例 (默认 5%)
            take_profit: 止盈比例 (默认 10%)
        
        Returns:
            回测结果字典
        """
        df = self.get_stock_history(code, start_date, end_date, days=730)
        if df.empty:
            return {"error": "数据获取失败"}
        
        # 计算所有指标
        df = self.calculate_all_indicators(df)
        
        # 初始化回测统计
        trades = []
        wins = 0
        losses = 0
        total_return = 0
        total_profit = 0
        total_loss = 0
        in_position = False
        entry_price = 0
        entry_date = None
        
        # 遍历每个交易日
        for idx in range(60, len(df) - hold_days):
            row = df.iloc[idx]
            current_date = row['date']
            
            # 如果已持仓，检查止盈止损或到期退出
            if in_position:
                # 检查持仓期间的最高价和最低价
                hold_df = df.iloc[idx:min(idx+hold_days+1, len(df))]
                if len(hold_df) == 0:
                    continue
                    
                high_price = hold_df['high'].max()
                low_price = hold_df['low'].min()
                exit_price = hold_df.iloc[-1]['close']
                exit_date = hold_df.iloc[-1]['date']
                
                # 计算实际价格变化
                price_change = (exit_price - entry_price) / entry_price
                triggered = False
                exit_type = 'hold_period'
                
                # 止盈
                if high_price >= entry_price * (1 + take_profit):
                    profit = take_profit
                    wins += 1
                    total_profit += profit
                    triggered = True
                    exit_type = 'take_profit'
                
                # 止损
                elif low_price <= entry_price * (1 - stop_loss):
                    profit = -stop_loss
                    losses += 1
                    total_loss += abs(profit)
                    triggered = True
                    exit_type = 'stop_loss'
                
                # 到期退出 (未触发止盈止损)
                else:
                    profit = price_change
                    if profit > 0:
                        wins += 1
                        total_profit += profit
                    else:
                        losses += 1
                        total_loss += abs(profit)
                
                trades.append({
                    'entry_date': entry_date.strftime('%Y-%m-%d') if entry_date else 'N/A',
                    'exit_date': exit_date.strftime('%Y-%m-%d') if hasattr(exit_date, 'strftime') else str(exit_date),
                    'profit': round(profit * 100, 2),
                    'type': exit_type
                })
                total_return += profit
                in_position = False
            
            # 检查共振信号 - 使用更严格的买入条件
            buy_signals_count = 0
            
            # 趋势共振买入 (过滤：只在多头趋势中买入)
            ma_trend = row['ma5'] > row['ma20'] if not pd.isna(row.get('ma5')) and not pd.isna(row.get('ma20')) else False
            
            trend_buy, _, _ = self.check_trend_resonance(df, idx)
            if trend_buy and ma_trend:
                buy_signals_count += 3  # 权重更高
            
            # 动量共振买入 (超卖反弹)
            mom_buy, _, _ = self.check_momentum_resonance(df, idx)
            if mom_buy:
                buy_signals_count += 2
            
            # 量价共振买入 (资金流入)
            vol_buy, _, _ = self.check_volume_price_resonance(df, idx)
            if vol_buy:
                buy_signals_count += 2
            
            # 波动率突破
            vol_breakout, _, _ = self.check_volatility_resonance(df, idx)
            if vol_breakout:
                buy_signals_count += 1
            
            # 全指标共振
            all_buy, _, _ = self.check_all_indicators_resonance(df, idx)
            if all_buy:
                buy_signals_count += 4
            
            # 计算信号类别数量
            signal_categories = 0
            if trend_buy:
                signal_categories += 1
            if mom_buy:
                signal_categories += 1
            if vol_buy:
                signal_categories += 1
            if vol_breakout:
                signal_categories += 1
            if all_buy:
                signal_categories += 1
            
            # 开仓条件：共振信号组合
            # 策略：动量反转 + 量价确认 (经典组合)
            # 或者：趋势确认 + 量价配合
            # 或者：全指标共振
            
            quality_entry = (
                (mom_buy and vol_buy) or  # 动量反转 + 量价配合
                (trend_buy and vol_buy) or  # 趋势确认 + 量价配合
                (all_buy) or  # 全指标共振
                (signal_categories >= 2 and ma_trend)  # 多信号 + 趋势
            )
            
            if quality_entry and not in_position:
                in_position = True
                entry_price = row['close']
                entry_date = current_date
        
        # 计算回测统计
        total_trades = wins + losses
        win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
        avg_win = sum([t['profit'] for t in trades if t['profit'] > 0]) / max(1, wins)
        avg_loss = sum([t['profit'] for t in trades if t['profit'] < 0]) / max(1, losses)
        profit_factor = abs(avg_win / avg_loss) if avg_loss != 0 else float('inf')
        
        return {
            'code': code,
            'period': f"{start_date or 'N/A'} to {end_date or 'N/A'}",
            'total_trades': total_trades,
            'wins': wins,
            'losses': losses,
            'win_rate': round(win_rate, 2),
            'total_return': round(total_return * 100, 2),
            'avg_win': round(avg_win * 100, 2),
            'avg_loss': round(avg_loss * 100, 2),
            'profit_factor': round(profit_factor, 2),
            'trades': trades[:20]  # 只返回前 20 笔交易详情
        }
    
    def scan_market(self, code_list: List[str], min_strength: int = 60) -> List[Dict]:
        """
        扫描市场中的共振信号
        
        Args:
            code_list: 股票代码列表
            min_strength: 最小信号强度
        
        Returns:
            符合条件的信号列表
        """
        all_signals = []
        
        for code in code_list:
            signals = self.analyze_resonance(code)
            for signal in signals:
                if signal.strength >= min_strength:
                    all_signals.append({
                        'code': signal.code,
                        'date': signal.date,
                        'resonance_type': signal.resonance_type,
                        'signal_type': signal.signal_type,
                        'strength': signal.strength,
                        'confidence': signal.confidence,
                        'matched': f"{signal.matched_indicators}/{signal.total_indicators}"
                    })
        
        # 按强度排序
        all_signals.sort(key=lambda x: x['strength'], reverse=True)
        
        return all_signals


def analyze_stock_resonance(code: str, date: str = None) -> Dict:
    """
    便捷函数：分析单只股票的共振信号
    
    Args:
        code: 股票代码
        date: 分析日期 (None 表示最新)
    
    Returns:
        分析结果字典
    """
    analyzer = ResonanceAnalyzer()
    signals = analyzer.analyze_resonance(code, date)
    
    if not signals:
        return {
            'code': code,
            'date': date or 'latest',
            'signals': [],
            'summary': '未检测到共振信号'
        }
    
    # 汇总统计
    buy_signals = [s for s in signals if '买入' in s.signal_type]
    sell_signals = [s for s in signals if '卖出' in s.signal_type]
    
    avg_strength = sum([s.strength for s in signals]) / len(signals)
    max_strength = max([s.strength for s in signals])
    
    return {
        'code': code,
        'date': signals[0].date if signals else date or 'latest',
        'signals': [
            {
                'type': s.resonance_type,
                'signal': s.signal_type,
                'strength': s.strength,
                'confidence': s.confidence,
                'details': s.details
            }
            for s in signals
        ],
        'summary': {
            'total_signals': len(signals),
            'buy_signals': len(buy_signals),
            'sell_signals': len(sell_signals),
            'avg_strength': round(avg_strength, 1),
            'max_strength': max_strength,
            'recommendation': '强烈买入' if max_strength >= 80 and len(buy_signals) > len(sell_signals) 
                             else ('买入' if len(buy_signals) > len(sell_signals)
                                   else ('卖出' if len(sell_signals) > len(buy_signals)
                                         else '观望'))
        }
    }


def backtest_resonance_strategy(code: str, start_date: str = None, 
                                end_date: str = None) -> Dict:
    """
    便捷函数：回测共振策略
    
    Args:
        code: 股票代码
        start_date: 开始日期
        end_date: 结束日期
    
    Returns:
        回测结果
    """
    analyzer = ResonanceAnalyzer()
    return analyzer.backtest(code, start_date, end_date)


if __name__ == "__main__":
    # 测试示例
    print("=" * 60)
    print("多指标共振分析测试")
    print("=" * 60)
    
    # 测试 1: 单只股票共振分析
    print("\n【测试 1】300308 中际旭创 - 共振信号分析")
    print("-" * 60)
    result = analyze_stock_resonance("300308")
    print(f"股票代码：{result['code']}")
    print(f"分析日期：{result['date']}")
    print(f"信号总数：{result['summary']['total_signals']}")
    print(f"买入信号：{result['summary']['buy_signals']}")
    print(f"卖出信号：{result['summary']['sell_signals']}")
    print(f"平均强度：{result['summary']['avg_strength']}")
    print(f"最大强度：{result['summary']['max_strength']}")
    print(f"建议操作：{result['summary']['recommendation']}")
    
    if result['signals']:
        print("\n详细信号:")
        for sig in result['signals']:
            print(f"  - {sig['type']}: {sig['signal']} (强度:{sig['strength']}, {sig['confidence']})")
    
    # 测试 2: 回测 - 多只股票测试
    print("\n[Test 2] Multi-Stock Backtest (2024 to present)")
    print("-" * 60)
    
    # 初始化分析器
    analyzer = ResonanceAnalyzer()
    test_stocks = ["300308", "000001", "600519", "000858", "601318"]
    total_wins = 0
    total_losses = 0
    total_trades = 0
    all_results = []
    
    for stock in test_stocks:
        result = analyzer.backtest(stock, "20240101", "20250313", 
                                   hold_days=5, stop_loss=0.04, take_profit=0.08)
        if 'error' not in result:
            total_wins += result['wins']
            total_losses += result['losses']
            total_trades += result['total_trades']
            all_results.append(result)
    
    # 汇总结果
    if total_trades > 0:
        overall_win_rate = (total_wins / total_trades * 100)
        print(f"\nOverall Results (Multiple Stocks):")
        print(f"  Total Trades: {total_trades}")
        print(f"  Wins: {total_wins}")
        print(f"  Losses: {total_losses}")
        print(f"  Win Rate: {overall_win_rate:.2f}%")
        backtest_result = {
            'period': '20240101 to 20250313',
            'total_trades': total_trades,
            'wins': total_wins,
            'losses': total_losses,
            'win_rate': round(overall_win_rate, 2),
            'stocks': test_stocks
        }
    else:
        print("No trades generated across all stocks")
        backtest_result = {'error': 'No trades', 'total_trades': 0, 'wins': 0, 'losses': 0, 'win_rate': 0}
    
    if 'error' not in backtest_result:
        print(f"Backtest Period: {backtest_result.get('period', 'N/A')}")
        print(f"Total Trades: {backtest_result.get('total_trades', 0)}")
        print(f"Wins: {backtest_result.get('wins', 0)}")
        print(f"Losses: {backtest_result.get('losses', 0)}")
        print(f"Win Rate: {backtest_result.get('win_rate', 0)}%")
        if 'stocks' in backtest_result:
            print(f"Test Stocks: {', '.join(backtest_result['stocks'])}")
        
        # 验收标准检查
        print("\n【验收标准检查】")
        if backtest_result['win_rate'] > 55:
            print(f"[PASS] 回测胜率 {backtest_result['win_rate']}% > 55% (达标)")
        else:
            print(f"[WARN] 回测胜率 {backtest_result['win_rate']}% < 55% (未达标，需优化策略)")
    
    print("\n" + "=" * 60)
    print("测试完成!")
    print("=" * 60)
