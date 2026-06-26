"""
智能仓位管理系统 - 集成模块
Intelligent Position Sizing System - Integration Module

提供统一的高级 API 接口，整合仓位计算、风险管理和回测验证功能
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
import numpy as np

from position_sizer import (
    PositionSizer,
    PositionSizerBuilder,
    SignalStrength,
    RiskMetrics,
    MarketEnvironment,
    CapitalInfo,
    MarketTrend,
    PositionRecommendation
)

from risk_model import (
    RiskCalculator,
    RiskAnalysisResult,
    StressTester,
    PriceData
)

from backtester import (
    Backtester,
    BacktestResult,
    SignalGenerator
)


@dataclass
class StockAnalysis:
    """股票分析数据包"""
    symbol: str
    prices: List[float]
    dates: List[datetime]
    highs: Optional[List[float]] = None
    lows: Optional[List[float]] = None
    volumes: Optional[List[float]] = None
    
    # 基本面数据
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    pb_ratio: Optional[float] = None
    
    # 技术指标
    ma_20: Optional[float] = None
    ma_60: Optional[float] = None
    rsi: Optional[float] = None
    macd: Optional[float] = None
    atr: Optional[float] = None
    
    # 支撑阻力
    support: Optional[float] = None
    resistance: Optional[float] = None


@dataclass
class PortfolioPosition:
    """投资组合持仓"""
    symbol: str
    shares: int
    entry_price: float
    current_price: float
    position_value: float
    position_pct: float
    stop_loss: float
    take_profit: float
    pnl: float
    pnl_pct: float


class IntelligentPositionManager:
    """
    智能仓位管理器
    
    整合仓位计算、风险分析和回测验证的统一接口
    """
    
    def __init__(
        self,
        total_capital: float,
        risk_tolerance: float = 0.5,
        max_position_pct: float = 0.8,
        max_single_stock_pct: float = 0.2
    ):
        """
        初始化智能仓位管理器
        
        Args:
            total_capital: 总资金
            risk_tolerance: 风险承受能力 (0-1)
            max_position_pct: 最大总仓位
            max_single_stock_pct: 单只股票最大仓位
        """
        self.total_capital = total_capital
        self.risk_tolerance = risk_tolerance
        self.max_position_pct = max_position_pct
        self.max_single_stock_pct = max_single_stock_pct
        
        self.positions: Dict[str, PortfolioPosition] = {}
        self.available_capital = total_capital
    
    def analyze_stock(self, stock_data: StockAnalysis) -> Dict:
        """
        分析单只股票
        
        Args:
            stock_data: 股票数据
        
        Returns:
            Dict: 分析结果
        """
        # 计算信号强度
        technical_score = self._calculate_technical_score(stock_data)
        pattern_score = self._calculate_pattern_score(stock_data)
        multi_period_score = self._calculate_multi_period_score(stock_data)
        
        # 计算风险指标
        risk_metrics = self._calculate_risk_metrics(stock_data)
        
        # 评估市场环境
        market_env = self._evaluate_market_environment(stock_data)
        
        return {
            'symbol': stock_data.symbol,
            'technical_score': technical_score,
            'pattern_score': pattern_score,
            'multi_period_score': multi_period_score,
            'risk_metrics': risk_metrics,
            'market_env': market_env,
            'support': stock_data.support,
            'resistance': stock_data.resistance,
            'atr': stock_data.atr
        }
    
    def calculate_position(
        self,
        stock_data: StockAnalysis,
        analysis: Optional[Dict] = None
    ) -> PositionRecommendation:
        """
        计算股票仓位
        
        Args:
            stock_data: 股票数据
            analysis: 分析结果 (可选，如不提供则自动计算)
        
        Returns:
            PositionRecommendation: 仓位推荐
        """
        if analysis is None:
            analysis = self.analyze_stock(stock_data)
        
        # 创建仓位管理器
        sizer = (PositionSizerBuilder()
            .with_signal(
                technical=analysis['technical_score'],
                pattern=analysis['pattern_score'],
                multi_period=analysis['multi_period_score']
            )
            .with_risk(
                volatility=analysis['risk_metrics']['volatility'],
                max_drawdown=analysis['risk_metrics']['max_drawdown'],
                beta=analysis['risk_metrics']['beta']
            )
            .with_market(
                trend=analysis['market_env']['trend'],
                industry_health=analysis['market_env']['industry_health'],
                sentiment=analysis['market_env']['sentiment']
            )
            .with_capital(
                total=self.total_capital,
                available=self.available_capital,
                risk_tolerance=self.risk_tolerance
            )
            .build()
        )
        
        # 生成推荐
        current_price = stock_data.prices[-1] if stock_data.prices else 0
        
        recommendation = sizer.generate_recommendation(
            current_price=current_price,
            atr=analysis.get('atr'),
            support_level=analysis.get('support'),
            resistance_level=analysis.get('resistance')
        )
        
        # 检查单只股票仓位限制
        max_allowed_pct = min(
            recommendation.position_pct,
            self.max_single_stock_pct
        )
        
        if recommendation.position_pct > max_allowed_pct:
            # 调整仓位
            adjustment_ratio = max_allowed_pct / recommendation.position_pct
            recommendation.recommended_shares = int(
                recommendation.recommended_shares * adjustment_ratio
            )
            recommendation.position_value = (
                recommendation.recommended_shares * current_price
            )
            recommendation.position_pct = max_allowed_pct
        
        return recommendation
    
    def build_portfolio(
        self,
        stock_list: List[StockAnalysis]
    ) -> Dict[str, PositionRecommendation]:
        """
        构建投资组合
        
        Args:
            stock_list: 股票列表
        
        Returns:
            Dict[str, PositionRecommendation]: 每只股票的仓位推荐
        """
        recommendations = {}
        remaining_capital = self.available_capital
        
        # 按信号强度排序
        analyzed_stocks = []
        for stock in stock_list:
            analysis = self.analyze_stock(stock)
            total_score = (
                analysis['technical_score'] * 0.4 +
                analysis['pattern_score'] * 0.3 +
                analysis['multi_period_score'] * 0.3
            )
            analyzed_stocks.append((stock, analysis, total_score))
        
        analyzed_stocks.sort(key=lambda x: x[2], reverse=True)
        
        # 依次分配仓位
        for stock, analysis, score in analyzed_stocks:
            if remaining_capital <= 0:
                break
            
            # 创建临时仓位管理器
            sizer = (PositionSizerBuilder()
                .with_signal(
                    technical=analysis['technical_score'],
                    pattern=analysis['pattern_score'],
                    multi_period=analysis['multi_period_score']
                )
                .with_risk(
                    volatility=analysis['risk_metrics']['volatility'],
                    max_drawdown=analysis['risk_metrics']['max_drawdown'],
                    beta=analysis['risk_metrics']['beta']
                )
                .with_market(
                    trend=analysis['market_env']['trend'],
                    industry_health=analysis['market_env']['industry_health'],
                    sentiment=analysis['market_env']['sentiment']
                )
                .with_capital(
                    total=self.total_capital,
                    available=remaining_capital,
                    risk_tolerance=self.risk_tolerance
                )
                .build()
            )
            
            current_price = stock.prices[-1] if stock.prices else 0
            rec = sizer.generate_recommendation(
                current_price=current_price,
                atr=analysis.get('atr'),
                support_level=analysis.get('support'),
                resistance_level=analysis.get('resistance')
            )
            
            # 应用限制
            if rec.position_value > remaining_capital:
                rec.recommended_shares = int(remaining_capital / current_price)
                rec.position_value = rec.recommended_shares * current_price
                rec.position_pct = rec.position_value / self.total_capital
            
            if rec.position_pct > self.max_single_stock_pct:
                max_value = self.total_capital * self.max_single_stock_pct
                rec.recommended_shares = int(max_value / current_price)
                rec.position_value = rec.recommended_shares * current_price
                rec.position_pct = self.max_single_stock_pct
            
            recommendations[stock.symbol] = rec
            remaining_capital -= rec.position_value
        
        return recommendations
    
    def run_risk_analysis(self, stock_data: StockAnalysis) -> RiskAnalysisResult:
        """
        运行风险分析
        
        Args:
            stock_data: 股票数据
        
        Returns:
            RiskAnalysisResult: 风险分析结果
        """
        price_data = PriceData(
            prices=stock_data.prices,
            dates=stock_data.dates,
            highs=stock_data.highs,
            lows=stock_data.lows,
            volumes=stock_data.volumes
        )
        
        calculator = RiskCalculator(price_data)
        return calculator.full_analysis()
    
    def run_stress_test(self, stock_data: StockAnalysis) -> List[Dict]:
        """
        运行压力测试
        
        Args:
            stock_data: 股票数据
        
        Returns:
            List[Dict]: 压力测试结果
        """
        price_data = PriceData(
            prices=stock_data.prices,
            dates=stock_data.dates
        )
        
        # 先计算 Beta
        risk_analysis = self.run_risk_analysis(stock_data)
        beta = risk_analysis.beta
        
        tester = StressTester(price_data, beta=beta)
        return tester.run_all_scenarios()
    
    def run_backtest(
        self,
        stock_data: StockAnalysis,
        initial_capital: Optional[float] = None
    ) -> BacktestResult:
        """
        运行回测
        
        Args:
            stock_data: 股票数据
            initial_capital: 初始资金 (可选)
        
        Returns:
            BacktestResult: 回测结果
        """
        if initial_capital is None:
            initial_capital = self.total_capital
        
        backtester = Backtester(
            prices=stock_data.prices,
            dates=stock_data.dates,
            initial_capital=initial_capital
        )
        
        # 创建信号生成器
        signal_gen = self._create_signal_generator(stock_data)
        
        # 运行回测
        result = backtester.run_backtest(
            position_sizer_class=lambda **kwargs: PositionSizer(
                signal_strength=SignalStrength(
                    technical_score=kwargs.get('signal_strength', {}).get('technical', 70),
                    pattern_score=kwargs.get('signal_strength', {}).get('pattern', 70),
                    multi_period_score=kwargs.get('signal_strength', {}).get('multi_period', 70)
                ),
                risk_metrics=RiskMetrics(
                    volatility=kwargs.get('risk_metrics', {}).get('volatility', 0.15),
                    max_drawdown=kwargs.get('risk_metrics', {}).get('max_drawdown', 0.2),
                    beta=kwargs.get('risk_metrics', {}).get('beta', 1.0)
                ),
                market_env=MarketEnvironment(
                    market_trend=MarketTrend.BULLISH if kwargs.get('market_env', {}).get('trend') == 'bullish' else MarketTrend.BEARISH,
                    industry_health=kwargs.get('market_env', {}).get('industry_health', 0.5),
                    market_sentiment=kwargs.get('market_env', {}).get('sentiment', 0.5)
                ),
                capital_info=CapitalInfo(
                    total_capital=kwargs.get('capital_info', {}).get('total', initial_capital),
                    available_capital=kwargs.get('capital_info', {}).get('available', initial_capital * 0.8),
                    risk_tolerance=self.risk_tolerance
                )
            ),
            signal_generator=signal_gen.generate_signal,
            risk_calculator=None
        )
        
        return result
    
    def _calculate_technical_score(self, stock: StockAnalysis) -> float:
        """计算技术指标得分"""
        score = 50.0  # 基础分
        
        if stock.rsi:
            if 30 <= stock.rsi <= 70:
                score += 10
            elif stock.rsi < 30:
                score += 20  # 超卖
            elif stock.rsi > 70:
                score -= 10  # 超买
        
        if stock.ma_20 and stock.ma_60:
            if stock.ma_20 > stock.ma_60:
                score += 15  # 多头排列
            else:
                score -= 15  # 空头排列
        
        if stock.macd:
            if stock.macd > 0:
                score += 10
            else:
                score -= 10
        
        return np.clip(score, 0, 100)
    
    def _calculate_pattern_score(self, stock: StockAnalysis) -> float:
        """计算形态识别得分"""
        score = 50.0
        
        if stock.support and stock.resistance:
            current = stock.prices[-1] if stock.prices else 0
            support_distance = (current - stock.support) / stock.support
            resistance_distance = (stock.resistance - current) / current
            
            if support_distance < 0.05:  # 接近支撑位
                score += 20
            elif resistance_distance < 0.05:  # 接近阻力位
                score -= 15
        
        # 简单的趋势判断
        if len(stock.prices) >= 20:
            recent_trend = (stock.prices[-1] - stock.prices[-20]) / stock.prices[-20]
            if recent_trend > 0.05:
                score += 15
            elif recent_trend < -0.05:
                score -= 15
        
        return np.clip(score, 0, 100)
    
    def _calculate_multi_period_score(self, stock: StockAnalysis) -> float:
        """计算多周期共振得分"""
        score = 50.0
        
        if len(stock.prices) >= 60:
            # 短期趋势
            short_trend = (stock.prices[-1] - stock.prices[-10]) / stock.prices[-10]
            # 中期趋势
            mid_trend = (stock.prices[-1] - stock.prices[-30]) / stock.prices[-30]
            # 长期趋势
            long_trend = (stock.prices[-1] - stock.prices[-60]) / stock.prices[-60]
            
            # 判断共振
            if short_trend > 0 and mid_trend > 0 and long_trend > 0:
                score += 30  # 多头共振
            elif short_trend < 0 and mid_trend < 0 and long_trend < 0:
                score -= 30  # 空头共振
            elif (short_trend > 0 and mid_trend > 0) or (short_trend < 0 and mid_trend < 0):
                score += 10 if short_trend > 0 else -10
        
        return np.clip(score, 0, 100)
    
    def _calculate_risk_metrics(self, stock: StockAnalysis) -> Dict:
        """计算风险指标"""
        if len(stock.prices) < 30:
            return {
                'volatility': 0.2,
                'max_drawdown': 0.2,
                'beta': 1.0
            }
        
        prices = np.array(stock.prices)
        returns = np.diff(prices) / prices[:-1]
        
        # 波动率
        volatility = returns.std() * np.sqrt(252)
        
        # 最大回撤
        cummax = np.maximum.accumulate(prices)
        drawdown = (cummax - prices) / cummax
        max_drawdown = drawdown.max()
        
        # Beta (简化计算，假设市场 Beta 为 1)
        beta = 1.0 + (volatility - 0.2) * 2  # 波动率越高，Beta 越高
        
        return {
            'volatility': volatility,
            'max_drawdown': max_drawdown,
            'beta': np.clip(beta, 0.5, 2.0)
        }
    
    def _evaluate_market_environment(self, stock: StockAnalysis) -> Dict:
        """评估市场环境"""
        # 简化版本，实际应用中应结合更多市场数据
        trend = MarketTrend.NEUTRAL
        
        if stock.ma_20 and stock.ma_60:
            if stock.ma_20 > stock.ma_60:
                trend = MarketTrend.BULLISH
            else:
                trend = MarketTrend.BEARISH
        
        return {
            'trend': trend,
            'industry_health': 0.5,
            'sentiment': 0.5
        }
    
    def _create_signal_generator(self, stock_data: StockAnalysis):
        """创建信号生成器"""
        return SignalGenerator(lookback=30)


# ==================== 使用示例 ====================

if __name__ == "__main__":
    from datetime import timedelta
    
    # 生成示例数据
    np.random.seed(42)
    days = 252
    dates = [datetime.now() - timedelta(days=i) for i in range(days)][::-1]
    returns = np.random.normal(0.0005, 0.02, days)
    prices = 100 * np.cumprod(1 + returns)
    
    stock = StockAnalysis(
        symbol="000001.SZ",
        prices=prices.tolist(),
        dates=dates,
        ma_20=prices[-20:].mean(),
        ma_60=prices[-60:].mean(),
        rsi=55.0,
        macd=0.5,
        atr=prices[-1] * 0.02,
        support=prices.min() * 0.98,
        resistance=prices.max() * 1.02
    )
    
    # 创建管理器
    manager = IntelligentPositionManager(
        total_capital=1000000,
        risk_tolerance=0.6,
        max_single_stock_pct=0.2
    )
    
    print("=" * 60)
    print("智能仓位管理系统 - 集成示例")
    print("=" * 60)
    
    # 1. 分析股票
    analysis = manager.analyze_stock(stock)
    print(f"\n股票：{stock.symbol}")
    print(f"技术得分：{analysis['technical_score']:.1f}")
    print(f"形态得分：{analysis['pattern_score']:.1f}")
    print(f"多周期得分：{analysis['multi_period_score']:.1f}")
    
    # 2. 计算仓位
    rec = manager.calculate_position(stock, analysis)
    print(f"\n仓位推荐:")
    print(f"  推荐股数：{rec.recommended_shares}")
    print(f"  仓位价值：CNY {rec.position_value:,.2f}")
    print(f"  仓位比例：{rec.position_pct * 100:.1f}%")
    print(f"  止损价：CNY {rec.stop_loss:.2f}")
    print(f"  止盈价：CNY {rec.take_profit:.2f}")
    
    # 3. 风险分析
    risk_analysis = manager.run_risk_analysis(stock)
    print(f"\n风险分析:")
    print(f"  波动率：{risk_analysis.historical_volatility * 100:.1f}%")
    print(f"  最大回撤：{risk_analysis.max_drawdown * 100:.1f}%")
    print(f"  Beta: {risk_analysis.beta:.2f}")
    print(f"  夏普比率：{risk_analysis.sharpe_ratio:.2f}")
    print(f"  风险评分：{risk_analysis.risk_score:.1f} ({risk_analysis.risk_level})")
    
    # 4. 压力测试
    stress_results = manager.run_stress_test(stock)
    print(f"\n压力测试:")
    for scenario in stress_results[:3]:
        print(f"  {scenario['scenario']}: {scenario['loss_pct']:.2%}")
    
    print("=" * 60)
