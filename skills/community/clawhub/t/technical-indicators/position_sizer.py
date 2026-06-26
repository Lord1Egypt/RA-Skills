"""
智能仓位管理系统 - Intelligent Position Sizing System
基于信号强度和风险的智能仓位推荐系统

功能模块:
1. 仓位计算因子 (信号强度 40%, 风险水平 30%, 市场环境 20%, 资金规模 10%)
2. 仓位计算公式
3. 风险管理与止损止盈计算
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import numpy as np
from enum import Enum


class MarketTrend(Enum):
    """市场趋势枚举"""
    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"


class RiskLevel(Enum):
    """风险等级枚举"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXTREME = "extreme"


@dataclass
class SignalStrength:
    """信号强度计算类"""
    technical_score: float = 0.0  # 技术指标信号 (0-100)
    pattern_score: float = 0.0    # 形态识别信号 (0-100)
    multi_period_score: float = 0.0  # 多周期共振 (0-100)
    
    def calculate_total(self) -> float:
        """计算总信号强度 (0-100)"""
        # 三个子信号平均
        total = (self.technical_score + self.pattern_score + self.multi_period_score) / 3
        return np.clip(total, 0, 100)
    
    def to_normalized(self) -> float:
        """转换为 0-1 的归一化值"""
        return self.calculate_total() / 100


@dataclass
class RiskMetrics:
    """风险指标计算类"""
    volatility: float = 0.0      # 波动率 (ATR/价格)
    max_drawdown: float = 0.0    # 最大回撤历史
    beta: float = 1.0            # Beta 系数
    
    def calculate_risk_level(self) -> float:
        """
        计算综合风险水平 (0-1, 越高风险越大)
        - volatility: 0-0.1 为低，0.1-0.3 为中，>0.3 为高
        - max_drawdown: 0-0.2 为低，0.2-0.4 为中，>0.4 为高
        - beta: <0.8 为低，0.8-1.2 为中，>1.2 为高
        """
        # 波动率评分 (0-1)
        vol_score = np.clip(self.volatility / 0.3, 0, 1)
        
        # 回撤评分 (0-1)
        dd_score = np.clip(self.max_drawdown / 0.4, 0, 1)
        
        # Beta 评分 (0-1), beta=1 为中性
        beta_score = np.clip(abs(self.beta - 1) / 0.5, 0, 1)
        
        # 加权平均
        risk_level = (vol_score * 0.4 + dd_score * 0.4 + beta_score * 0.2)
        return np.clip(risk_level, 0, 1)
    
    def get_risk_category(self) -> RiskLevel:
        """获取风险等级分类"""
        risk = self.calculate_risk_level()
        if risk < 0.25:
            return RiskLevel.LOW
        elif risk < 0.5:
            return RiskLevel.MEDIUM
        elif risk < 0.75:
            return RiskLevel.HIGH
        else:
            return RiskLevel.EXTREME


@dataclass
class MarketEnvironment:
    """市场环境评估类"""
    market_trend: MarketTrend = MarketTrend.NEUTRAL  # 大盘趋势
    industry_health: float = 0.5  # 行业景气度 (0-1)
    market_sentiment: float = 0.5  # 市场情绪 (0-1)
    
    def calculate_environment_score(self) -> float:
        """
        计算市场环境得分 (0-1)
        """
        # 趋势得分
        trend_score = {
            MarketTrend.BULLISH: 1.0,
            MarketTrend.NEUTRAL: 0.5,
            MarketTrend.BEARISH: 0.0
        }[self.market_trend]
        
        # 综合得分
        env_score = (
            trend_score * 0.4 +
            self.industry_health * 0.3 +
            self.market_sentiment * 0.3
        )
        return np.clip(env_score, 0, 1)


@dataclass
class CapitalInfo:
    """资金信息类"""
    total_capital: float = 0.0      # 账户总资金
    available_capital: float = 0.0  # 可用资金
    risk_tolerance: float = 0.5     # 风险承受能力 (0-1)
    
    def calculate_capital_adequacy(self) -> float:
        """
        计算资金充足度 (0-1)
        考虑可用资金比例和风险承受能力
        """
        if self.total_capital <= 0:
            return 0.0
        
        # 可用资金比例
        available_ratio = self.available_capital / self.total_capital
        
        # 综合充足度
        adequacy = (available_ratio * 0.6 + self.risk_tolerance * 0.4)
        return np.clip(adequacy, 0, 1)


@dataclass
class PositionRecommendation:
    """仓位推荐结果"""
    recommended_shares: int           # 推荐股数
    position_value: float             # 仓位价值
    position_pct: float               # 仓位百分比
    stop_loss: float                  # 止损价
    take_profit: float                # 止盈价
    risk_amount: float                # 风险金额
    risk_pct: float                   # 风险百分比
    sharpe_ratio: float               # 夏普比率
    signal_strength: float            # 信号强度得分
    risk_level: float                 # 风险水平得分
    environment_score: float          # 环境得分
    capital_adequacy: float           # 资金充足度
    recommendation_time: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        """转换为字典格式"""
        return {
            "recommended_shares": self.recommended_shares,
            "position_value": round(self.position_value, 2),
            "position_pct": round(self.position_pct * 100, 1),
            "stop_loss": round(self.stop_loss, 2),
            "take_profit": round(self.take_profit, 2),
            "risk_amount": round(self.risk_amount, 2),
            "risk_pct": round(self.risk_pct * 100, 1),
            "sharpe_ratio": round(self.sharpe_ratio, 2),
            "signal_strength": round(self.signal_strength * 100, 1),
            "risk_level": round(self.risk_level * 100, 1),
            "environment_score": round(self.environment_score * 100, 1),
            "capital_adequacy": round(self.capital_adequacy * 100, 1),
            "recommendation_time": self.recommendation_time.isoformat()
        }


class PositionSizer:
    """
    智能仓位管理器
    
    仓位计算公式:
    基础仓位 = 信号强度 × 0.4
    风险调整 = (1 - 风险水平) × 0.3
    环境调整 = 市场环境 × 0.2
    资金调整 = 资金充足度 × 0.1
    
    建议仓位 = 基础仓位 + 风险调整 + 环境调整 + 资金调整
    最终仓位 = min(建议仓位，80%)  # 最大 80%
    """
    
    MAX_POSITION_PCT = 0.8  # 最大仓位 80%
    MIN_POSITION_PCT = 0.0  # 最小仓位 0%
    DEFAULT_RISK_PCT = 0.02  # 默认单笔风险 2%
    
    def __init__(
        self,
        signal_strength: SignalStrength,
        risk_metrics: RiskMetrics,
        market_env: MarketEnvironment,
        capital_info: CapitalInfo
    ):
        self.signal = signal_strength
        self.risk = risk_metrics
        self.market = market_env
        self.capital = capital_info
    
    def calculate_position_percentage(self) -> float:
        """
        计算建议仓位百分比
        
        Returns:
            float: 仓位百分比 (0-1)
        """
        # 各因子得分
        signal_norm = self.signal.to_normalized()
        risk_level = self.risk.calculate_risk_level()
        env_score = self.market.calculate_environment_score()
        capital_adequacy = self.capital.calculate_capital_adequacy()
        
        # 仓位计算
        base_position = signal_norm * 0.4
        risk_adjustment = (1 - risk_level) * 0.3
        env_adjustment = env_score * 0.2
        capital_adjustment = capital_adequacy * 0.1
        
        recommended = base_position + risk_adjustment + env_adjustment + capital_adjustment
        
        # 限制在 0-80%
        final_position = np.clip(recommended, self.MIN_POSITION_PCT, self.MAX_POSITION_PCT)
        
        return final_position
    
    def calculate_stop_loss(
        self,
        current_price: float,
        atr: Optional[float] = None,
        support_level: Optional[float] = None
    ) -> float:
        """
        计算止损价
        
        Args:
            current_price: 当前价格
            atr: ATR 值 (可选)
            support_level: 支撑位 (可选)
        
        Returns:
            float: 止损价格
        """
        # 方法 1: 基于 ATR (2 倍 ATR)
        if atr and atr > 0:
            atr_stop = current_price - (2 * atr)
        else:
            atr_stop = current_price * 0.95
        
        # 方法 2: 基于支撑位
        if support_level and support_level < current_price:
            support_stop = support_level * 0.98  # 支撑位下方 2%
        else:
            support_stop = atr_stop
        
        # 取较高的止损位 (更保守)
        stop_loss = max(atr_stop, support_stop)
        
        # 确保不超过 10% 亏损
        min_stop = current_price * 0.90
        return max(stop_loss, min_stop)
    
    def calculate_take_profit(
        self,
        current_price: float,
        resistance_level: Optional[float] = None,
        risk_reward_ratio: float = 2.0
    ) -> float:
        """
        计算止盈价
        
        Args:
            current_price: 当前价格
            resistance_level: 阻力位 (可选)
            risk_reward_ratio: 风报比 (默认 2:1)
        
        Returns:
            float: 止盈价格
        """
        stop_loss = self.calculate_stop_loss(current_price)
        risk_distance = current_price - stop_loss
        
        # 基于风报比计算
        rr_target = current_price + (risk_distance * risk_reward_ratio)
        
        # 基于阻力位
        if resistance_level and resistance_level > current_price:
            resistance_target = resistance_level * 0.98  # 阻力位下方 2%
        else:
            resistance_target = rr_target
        
        # 取较低的止盈位 (更保守)
        take_profit = min(rr_target, resistance_target)
        
        # 确保至少有 5% 盈利空间
        min_target = current_price * 1.05
        return max(take_profit, min_target)
    
    def calculate_sharpe_ratio(
        self,
        expected_return: float,
        risk_free_rate: float = 0.03
    ) -> float:
        """
        计算夏普比率
        
        Args:
            expected_return: 预期收益率
            risk_free_rate: 无风险利率 (默认 3%)
        
        Returns:
            float: 夏普比率
        """
        volatility = self.risk.volatility
        if volatility <= 0:
            return 0.0
        
        excess_return = expected_return - risk_free_rate
        sharpe = excess_return / volatility
        return sharpe
    
    def generate_recommendation(
        self,
        current_price: float,
        atr: Optional[float] = None,
        support_level: Optional[float] = None,
        resistance_level: Optional[float] = None,
        expected_return: Optional[float] = None
    ) -> PositionRecommendation:
        """
        生成完整的仓位推荐
        
        Args:
            current_price: 当前价格
            atr: ATR 值
            support_level: 支撑位
            resistance_level: 阻力位
            expected_return: 预期收益率
        
        Returns:
            PositionRecommendation: 仓位推荐结果
        """
        # 计算仓位百分比
        position_pct = self.calculate_position_percentage()
        
        # 计算可投资金额
        max_investable = self.capital.available_capital * position_pct
        
        # 计算推荐股数 (向下取整)
        if current_price > 0:
            recommended_shares = int(max_investable / current_price)
            position_value = recommended_shares * current_price
        else:
            recommended_shares = 0
            position_value = 0.0
        
        # 计算止损止盈
        stop_loss = self.calculate_stop_loss(current_price, atr, support_level)
        take_profit = self.calculate_take_profit(current_price, resistance_level)
        
        # 计算风险金额
        risk_per_share = current_price - stop_loss
        risk_amount = recommended_shares * risk_per_share
        risk_pct = risk_amount / self.capital.total_capital if self.capital.total_capital > 0 else 0
        
        # 计算夏普比率
        if expected_return is None:
            # 估算预期收益 (基于风报比)
            expected_return = (take_profit - current_price) / current_price
        
        sharpe_ratio = self.calculate_sharpe_ratio(expected_return)
        
        # 生成推荐
        recommendation = PositionRecommendation(
            recommended_shares=recommended_shares,
            position_value=position_value,
            position_pct=position_pct,
            stop_loss=stop_loss,
            take_profit=take_profit,
            risk_amount=risk_amount,
            risk_pct=risk_pct,
            sharpe_ratio=sharpe_ratio,
            signal_strength=self.signal.to_normalized(),
            risk_level=self.risk.calculate_risk_level(),
            environment_score=self.market.calculate_environment_score(),
            capital_adequacy=self.capital.calculate_capital_adequacy()
        )
        
        return recommendation


class PositionSizerBuilder:
    """
    仓位管理器构建器
    提供链式调用接口
    """
    
    def __init__(self):
        self._signal = SignalStrength()
        self._risk = RiskMetrics()
        self._market = MarketEnvironment()
        self._capital = CapitalInfo()
    
    def with_signal(
        self,
        technical: float = 0,
        pattern: float = 0,
        multi_period: float = 0
    ) -> 'PositionSizerBuilder':
        """设置信号强度"""
        self._signal.technical_score = np.clip(technical, 0, 100)
        self._signal.pattern_score = np.clip(pattern, 0, 100)
        self._signal.multi_period_score = np.clip(multi_period, 0, 100)
        return self
    
    def with_risk(
        self,
        volatility: float = 0,
        max_drawdown: float = 0,
        beta: float = 1
    ) -> 'PositionSizerBuilder':
        """设置风险指标"""
        self._risk.volatility = max(0, volatility)
        self._risk.max_drawdown = max(0, max_drawdown)
        self._risk.beta = beta
        return self
    
    def with_market(
        self,
        trend: MarketTrend = MarketTrend.NEUTRAL,
        industry_health: float = 0.5,
        sentiment: float = 0.5
    ) -> 'PositionSizerBuilder':
        """设置市场环境"""
        self._market.market_trend = trend
        self._market.industry_health = np.clip(industry_health, 0, 1)
        self._market.market_sentiment = np.clip(sentiment, 0, 1)
        return self
    
    def with_capital(
        self,
        total: float = 0,
        available: float = 0,
        risk_tolerance: float = 0.5
    ) -> 'PositionSizerBuilder':
        """设置资金信息"""
        self._capital.total_capital = max(0, total)
        self._capital.available_capital = max(0, available)
        self._capital.risk_tolerance = np.clip(risk_tolerance, 0, 1)
        return self
    
    def build(self) -> PositionSizer:
        """构建仓位管理器"""
        return PositionSizer(
            signal_strength=self._signal,
            risk_metrics=self._risk,
            market_env=self._market,
            capital_info=self._capital
        )


# ==================== 使用示例 ====================

if __name__ == "__main__":
    # 示例：使用构建器创建仓位管理器
    sizer = (PositionSizerBuilder()
        .with_signal(technical=75, pattern=80, multi_period=70)
        .with_risk(volatility=0.15, max_drawdown=0.25, beta=1.1)
        .with_market(
            trend=MarketTrend.BULLISH,
            industry_health=0.7,
            sentiment=0.6
        )
        .with_capital(
            total=1000000,
            available=800000,
            risk_tolerance=0.6
        )
        .build()
    )
    
    # 生成推荐
    recommendation = sizer.generate_recommendation(
        current_price=540.0,
        atr=12.5,
        support_level=520.0,
        resistance_level=580.0,
        expected_return=0.08
    )
    
    # 输出结果
    print("=" * 60)
    print("智能仓位推荐系统 - 推荐结果")
    print("=" * 60)
    
    result = recommendation.to_dict()
    for key, value in result.items():
        print(f"{key:25}: {value}")
    
    print("=" * 60)
    print(f"建议买入：{recommendation.recommended_shares} 股")
    print(f"仓位价值：CNY {recommendation.position_value:,.2f}")
    print(f"仓位比例：{recommendation.position_pct * 100:.1f}%")
    print(f"止损价格：CNY {recommendation.stop_loss:.2f}")
    print(f"止盈价格：CNY {recommendation.take_profit:.2f}")
    print(f"风险金额：CNY {recommendation.risk_amount:,.2f}")
    print(f"风险比例：{recommendation.risk_pct * 100:.1f}%")
    print(f"夏普比率：{recommendation.sharpe_ratio:.2f}")
    print("=" * 60)
