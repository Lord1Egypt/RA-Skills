"""
风险模型模块 - Risk Model Module
智能仓位管理系统的风险管理核心组件

功能:
1. 波动率计算 (ATR, 历史波动率)
2. 回撤分析 (最大回撤，回撤持续时间)
3. Beta 系数计算
4. VaR (Value at Risk) 计算
5. 压力测试
6. 风险价值评估
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict
from datetime import datetime, timedelta
import numpy as np
from scipy import stats
from enum import Enum


class RiskMetricType(Enum):
    """风险指标类型"""
    VOLATILITY = "volatility"
    DRAWDOWN = "drawdown"
    VAR = "var"
    CVAR = "cvar"
    SHARPE = "sharpe"
    SORTINO = "sortino"
    MAX_LOSS = "max_loss"


@dataclass
class PriceData:
    """价格数据结构"""
    prices: List[float]
    dates: List[datetime]
    highs: Optional[List[float]] = None
    lows: Optional[List[float]] = None
    volumes: Optional[List[float]] = None
    
    def __post_init__(self):
        self.prices = np.array(self.prices)
        if self.highs:
            self.highs = np.array(self.highs)
        if self.lows:
            self.lows = np.array(self.lows)
        if self.volumes:
            self.volumes = np.array(self.volumes)


@dataclass
class RiskAnalysisResult:
    """风险分析结果"""
    # 波动率指标
    historical_volatility: float      # 历史波动率
    atr: float                        # 平均真实波幅
    volatility_percentile: float      # 波动率百分位
    
    # 回撤指标
    max_drawdown: float               # 最大回撤
    current_drawdown: float           # 当前回撤
    drawdown_duration: int            # 回撤持续时间 (天)
    avg_drawdown: float               # 平均回撤
    
    # 风险价值
    var_95: float                     # 95% VaR
    var_99: float                     # 99% VaR
    cvar_95: float                    # 95% CVaR (预期亏损)
    
    # 风险调整收益
    sharpe_ratio: float               # 夏普比率
    sortino_ratio: float              # 索提诺比率
    calmar_ratio: float               # 卡玛比率
    
    # Beta 相关
    beta: float                       # Beta 系数
    alpha: float                      # Alpha 收益
    correlation: float                # 与市场相关性
    
    # 其他
    risk_score: float                 # 综合风险评分 (0-100)
    risk_level: str                   # 风险等级
    analysis_date: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "historical_volatility": round(self.historical_volatility, 4),
            "atr": round(self.atr, 4),
            "volatility_percentile": round(self.volatility_percentile, 2),
            "max_drawdown": round(self.max_drawdown, 4),
            "current_drawdown": round(self.current_drawdown, 4),
            "drawdown_duration": self.drawdown_duration,
            "avg_drawdown": round(self.avg_drawdown, 4),
            "var_95": round(self.var_95, 4),
            "var_99": round(self.var_99, 4),
            "cvar_95": round(self.cvar_95, 4),
            "sharpe_ratio": round(self.sharpe_ratio, 2),
            "sortino_ratio": round(self.sortino_ratio, 2),
            "calmar_ratio": round(self.calmar_ratio, 2),
            "beta": round(self.beta, 2),
            "alpha": round(self.alpha, 4),
            "correlation": round(self.correlation, 4),
            "risk_score": round(self.risk_score, 2),
            "risk_level": self.risk_level,
            "analysis_date": self.analysis_date.isoformat()
        }


class RiskCalculator:
    """风险计算器"""
    
    TRADING_DAYS_PER_YEAR = 252
    
    def __init__(self, price_data: PriceData, benchmark_data: Optional[PriceData] = None):
        """
        初始化风险计算器
        
        Args:
            price_data: 标的价格数据
            benchmark_data: 基准价格数据 (用于计算 Beta)
        """
        self.price_data = price_data
        self.benchmark_data = benchmark_data
        self.returns = self._calculate_returns(price_data.prices)
        
        if benchmark_data:
            self.benchmark_returns = self._calculate_returns(benchmark_data.prices)
        else:
            self.benchmark_returns = None
    
    def _calculate_returns(self, prices: np.ndarray) -> np.ndarray:
        """计算收益率序列"""
        if len(prices) < 2:
            return np.array([])
        returns = np.diff(prices) / prices[:-1]
        return returns
    
    def calculate_historical_volatility(self, window: int = 20) -> float:
        """
        计算历史波动率
        
        Args:
            window: 计算窗口 (天数)
        
        Returns:
            float: 年化波动率
        """
        if len(self.returns) < window:
            return 0.0
        
        # 滚动标准差
        rolling_std = self.returns[-window:].std()
        
        # 年化
        annualized_vol = rolling_std * np.sqrt(self.TRADING_DAYS_PER_YEAR)
        return annualized_vol
    
    def calculate_atr(self, period: int = 14) -> float:
        """
        计算平均真实波幅 (ATR)
        
        Args:
            period: ATR 周期
        
        Returns:
            float: ATR 值
        """
        if not (self.price_data.highs is not None and 
                self.price_data.lows is not None):
            return 0.0
        
        highs = self.price_data.highs
        lows = self.price_data.lows
        closes = self.price_data.prices[:-1]
        
        if len(highs) < period + 1:
            return 0.0
        
        # 计算真实波幅
        tr1 = highs[1:] - lows[1:]
        tr2 = np.abs(highs[1:] - closes)
        tr3 = np.abs(lows[1:] - closes)
        tr = np.maximum(np.maximum(tr1, tr2), tr3)
        
        # 计算 ATR
        atr = tr[-period:].mean()
        return atr
    
    def calculate_volatility_percentile(self, window: int = 252, lookback: int = 252) -> float:
        """
        计算波动率百分位
        
        Args:
            window: 波动率计算窗口
            lookback: 历史回溯窗口
        
        Returns:
            float: 波动率百分位 (0-100)
        """
        if len(self.returns) < lookback + window:
            return 50.0
        
        # 计算历史波动率序列
        vol_series = []
        for i in range(window, len(self.returns)):
            vol = self.returns[i-window:i].std() * np.sqrt(self.TRADING_DAYS_PER_YEAR)
            vol_series.append(vol)
        
        current_vol = vol_series[-1]
        percentile = (np.sum(np.array(vol_series) <= current_vol) / len(vol_series)) * 100
        return percentile
    
    def calculate_max_drawdown(self) -> Tuple[float, int, int]:
        """
        计算最大回撤
        
        Returns:
            Tuple[float, int, int]: (最大回撤，开始索引，结束索引)
        """
        prices = self.price_data.prices
        
        # 计算累计最大值
        cummax = np.maximum.accumulate(prices)
        
        # 计算回撤
        drawdown = (cummax - prices) / cummax
        
        # 找到最大回撤
        max_dd = drawdown.max()
        end_idx = drawdown.argmax()
        
        # 找到回撤开始点
        start_idx = np.argmax(prices[:end_idx+1] == cummax[end_idx])
        
        return max_dd, start_idx, end_idx
    
    def calculate_current_drawdown(self) -> float:
        """计算当前回撤"""
        prices = self.price_data.prices
        cummax = np.maximum.accumulate(prices)
        current_dd = (cummax[-1] - prices[-1]) / cummax[-1]
        return current_dd
    
    def calculate_drawdown_duration(self) -> int:
        """计算回撤持续时间 (天)"""
        prices = self.price_data.prices
        cummax = np.maximum.accumulate(prices)
        
        # 找到当前是否在回撤中
        if prices[-1] >= cummax[-1]:
            return 0
        
        # 找到回撤开始时间
        for i in range(len(prices) - 1, -1, -1):
            if prices[i] >= cummax[-1]:
                return len(prices) - i - 1
        
        return len(prices)
    
    def calculate_avg_drawdown(self, threshold: float = 0.01) -> float:
        """
        计算平均回撤
        
        Args:
            threshold: 回撤阈值 (只计算超过该阈值的回撤)
        
        Returns:
            float: 平均回撤
        """
        prices = self.price_data.prices
        cummax = np.maximum.accumulate(prices)
        drawdown = (cummax - prices) / cummax
        
        # 只考虑超过阈值的回撤
        significant_dd = drawdown[drawdown > threshold]
        
        if len(significant_dd) == 0:
            return 0.0
        
        return significant_dd.mean()
    
    def calculate_var(self, confidence: float = 0.95) -> float:
        """
        计算 Value at Risk (VaR)
        
        Args:
            confidence: 置信水平 (默认 95%)
        
        Returns:
            float: VaR (负值表示损失)
        """
        if len(self.returns) < 10:
            return 0.0
        
        # 历史模拟法
        var = np.percentile(self.returns, (1 - confidence) * 100)
        return var
    
    def calculate_cvar(self, confidence: float = 0.95) -> float:
        """
        计算 Conditional VaR (CVaR / Expected Shortfall)
        
        Args:
            confidence: 置信水平
        
        Returns:
            float: CVaR
        """
        if len(self.returns) < 10:
            return 0.0
        
        var = self.calculate_var(confidence)
        cvar = self.returns[self.returns <= var].mean()
        return cvar
    
    def calculate_sharpe_ratio(self, risk_free_rate: float = 0.03) -> float:
        """
        计算夏普比率
        
        Args:
            risk_free_rate: 无风险利率
        
        Returns:
            float: 夏普比率
        """
        if len(self.returns) < 10:
            return 0.0
        
        excess_return = self.returns.mean() * self.TRADING_DAYS_PER_YEAR - risk_free_rate
        volatility = self.returns.std() * np.sqrt(self.TRADING_DAYS_PER_YEAR)
        
        if volatility == 0:
            return 0.0
        
        return excess_return / volatility
    
    def calculate_sortino_ratio(self, risk_free_rate: float = 0.03) -> float:
        """
        计算索提诺比率 (只考虑下行波动)
        
        Args:
            risk_free_rate: 无风险利率
        
        Returns:
            float: 索提诺比率
        """
        if len(self.returns) < 10:
            return 0.0
        
        excess_return = self.returns.mean() * self.TRADING_DAYS_PER_YEAR - risk_free_rate
        
        # 下行标准差
        downside_returns = self.returns[self.returns < 0]
        if len(downside_returns) == 0:
            return float('inf')
        
        downside_std = downside_returns.std() * np.sqrt(self.TRADING_DAYS_PER_YEAR)
        
        if downside_std == 0:
            return float('inf')
        
        return excess_return / downside_std
    
    def calculate_calmar_ratio(self) -> float:
        """
        计算卡玛比率 (收益 / 最大回撤)
        
        Returns:
            float: 卡玛比率
        """
        if len(self.returns) < 252:  # 至少一年数据
            return 0.0
        
        annual_return = (1 + self.returns).prod() ** (self.TRADING_DAYS_PER_YEAR / len(self.returns)) - 1
        max_dd, _, _ = self.calculate_max_drawdown()
        
        if max_dd == 0:
            return float('inf')
        
        return annual_return / max_dd
    
    def calculate_beta(self) -> float:
        """
        计算 Beta 系数
        
        Returns:
            float: Beta 系数
        """
        if self.benchmark_returns is None or len(self.benchmark_returns) < 10:
            return 1.0
        
        # 确保长度一致
        min_len = min(len(self.returns), len(self.benchmark_returns))
        asset_returns = self.returns[-min_len:]
        bench_returns = self.benchmark_returns[-min_len:]
        
        # 计算协方差和方差
        covariance = np.cov(asset_returns, bench_returns)[0, 1]
        variance = np.var(bench_returns)
        
        if variance == 0:
            return 1.0
        
        beta = covariance / variance
        return beta
    
    def calculate_alpha(self, risk_free_rate: float = 0.03) -> float:
        """
        计算 Alpha (超额收益)
        
        Args:
            risk_free_rate: 无风险利率
        
        Returns:
            float: Alpha
        """
        beta = self.calculate_beta()
        
        if self.benchmark_returns is None:
            return 0.0
        
        # 年化收益
        asset_return = self.returns.mean() * self.TRADING_DAYS_PER_YEAR
        bench_return = self.benchmark_returns.mean() * self.TRADING_DAYS_PER_YEAR
        
        # CAPM 预期收益
        expected_return = risk_free_rate + beta * (bench_return - risk_free_rate)
        
        # Alpha
        alpha = asset_return - expected_return
        return alpha
    
    def calculate_correlation(self) -> float:
        """
        计算与市场的相关性
        
        Returns:
            float: 相关系数
        """
        if self.benchmark_returns is None or len(self.benchmark_returns) < 10:
            return 0.0
        
        min_len = min(len(self.returns), len(self.benchmark_returns))
        corr = np.corrcoef(self.returns[-min_len:], self.benchmark_returns[-min_len:])[0, 1]
        return corr
    
    def calculate_risk_score(self) -> Tuple[float, str]:
        """
        计算综合风险评分
        
        Returns:
            Tuple[float, str]: (风险评分 0-100, 风险等级)
        """
        # 各风险因子
        volatility = self.calculate_historical_volatility()
        max_dd, _, _ = self.calculate_max_drawdown()
        beta = self.calculate_beta()
        var_95 = self.calculate_var(0.95)
        
        # 波动率评分 (0-25)
        vol_score = np.clip(volatility / 0.5, 0, 1) * 25
        
        # 回撤评分 (0-25)
        dd_score = np.clip(max_dd / 0.3, 0, 1) * 25
        
        # Beta 评分 (0-25), beta=1 为中性
        beta_score = np.clip(abs(beta - 1) / 0.8, 0, 1) * 25
        
        # VaR 评分 (0-25)
        var_score = np.clip(abs(var_95) / 0.05, 0, 1) * 25
        
        # 总分
        total_score = vol_score + dd_score + beta_score + var_score
        
        # 风险等级
        if total_score < 25:
            level = "LOW"
        elif total_score < 50:
            level = "MEDIUM"
        elif total_score < 75:
            level = "HIGH"
        else:
            level = "EXTREME"
        
        return total_score, level
    
    def full_analysis(self) -> RiskAnalysisResult:
        """
        执行完整的风险分析
        
        Returns:
            RiskAnalysisResult: 风险分析结果
        """
        max_dd, _, _ = self.calculate_max_drawdown()
        
        return RiskAnalysisResult(
            historical_volatility=self.calculate_historical_volatility(),
            atr=self.calculate_atr(),
            volatility_percentile=self.calculate_volatility_percentile(),
            max_drawdown=max_dd,
            current_drawdown=self.calculate_current_drawdown(),
            drawdown_duration=self.calculate_drawdown_duration(),
            avg_drawdown=self.calculate_avg_drawdown(),
            var_95=self.calculate_var(0.95),
            var_99=self.calculate_var(0.99),
            cvar_95=self.calculate_cvar(0.95),
            sharpe_ratio=self.calculate_sharpe_ratio(),
            sortino_ratio=self.calculate_sortino_ratio(),
            calmar_ratio=self.calculate_calmar_ratio(),
            beta=self.calculate_beta(),
            alpha=self.calculate_alpha(),
            correlation=self.calculate_correlation(),
            risk_score=self.calculate_risk_score()[0],
            risk_level=self.calculate_risk_score()[1]
        )


class StressTester:
    """
    压力测试器
    测试极端市场条件下的风险
    """
    
    SCENARIOS = {
        "market_crash": -0.20,      # 市场崩盘 -20%
        "correction": -0.10,        # 市场调整 -10%
        "flash_crash": -0.05,       # 闪崩 -5%
        "bull_run": 0.15,           # 牛市 +15%
        "sideways": 0.0,            # 横盘 0%
    }
    
    def __init__(self, price_data: PriceData, beta: float = 1.0):
        self.price_data = price_data
        self.beta = beta
    
    def run_scenario(self, scenario_name: str) -> Dict:
        """
        运行压力测试场景
        
        Args:
            scenario_name: 场景名称
        
        Returns:
            Dict: 压力测试结果
        """
        if scenario_name not in self.SCENARIOS:
            raise ValueError(f"Unknown scenario: {scenario_name}")
        
        market_move = self.SCENARIOS[scenario_name]
        
        # 基于 Beta 计算标的预期变动
        expected_move = market_move * self.beta
        
        current_price = self.price_data.prices[-1]
        stressed_price = current_price * (1 + expected_move)
        
        # 计算损失
        loss = current_price - stressed_price
        loss_pct = loss / current_price
        
        return {
            "scenario": scenario_name,
            "market_move": market_move,
            "expected_move": expected_move,
            "current_price": current_price,
            "stressed_price": stressed_price,
            "loss": loss,
            "loss_pct": loss_pct,
            "beta": self.beta
        }
    
    def run_all_scenarios(self) -> List[Dict]:
        """运行所有压力测试场景"""
        results = []
        for scenario in self.SCENARIOS.keys():
            results.append(self.run_scenario(scenario))
        return results
    
    def monte_carlo_simulation(
        self,
        days: int = 30,
        simulations: int = 10000,
        confidence: float = 0.95
    ) -> Dict:
        """
        蒙特卡洛模拟
        
        Args:
            days: 模拟天数
            simulations: 模拟次数
            confidence: 置信水平
        
        Returns:
            Dict: 模拟结果
        """
        current_price = self.price_data.prices[-1]
        
        # 计算日收益率统计
        returns = np.diff(self.price_data.prices) / self.price_data.prices[:-1]
        mu = returns.mean()
        sigma = returns.std()
        
        # 生成随机路径
        final_prices = []
        for _ in range(simulations):
            random_returns = np.random.normal(mu, sigma, days)
            cumulative_return = np.prod(1 + random_returns) - 1
            final_price = current_price * (1 + cumulative_return)
            final_prices.append(final_price)
        
        final_prices = np.array(final_prices)
        
        # 计算统计
        var_95 = np.percentile(final_prices, (1 - confidence) * 100)
        expected_price = final_prices.mean()
        worst_case = final_prices.min()
        best_case = final_prices.max()
        
        return {
            "current_price": current_price,
            "expected_price": expected_price,
            "var_95": var_95,
            "worst_case": worst_case,
            "best_case": best_case,
            "upside_potential": (expected_price - current_price) / current_price,
            "downside_risk": (current_price - var_95) / current_price,
            "simulations": simulations,
            "days": days
        }


# ==================== 使用示例 ====================

if __name__ == "__main__":
    # 生成示例数据
    np.random.seed(42)
    days = 252
    dates = [datetime.now() - timedelta(days=i) for i in range(days)][::-1]
    
    # 生成价格序列 (几何布朗运动)
    returns = np.random.normal(0.0005, 0.02, days)
    prices = 100 * np.cumprod(1 + returns)
    
    # 生成高低点
    highs = prices * (1 + np.random.uniform(0.01, 0.03, days))
    lows = prices * (1 - np.random.uniform(0.01, 0.03, days))
    
    # 创建价格数据
    price_data = PriceData(
        prices=prices.tolist(),
        dates=dates,
        highs=highs.tolist(),
        lows=lows.tolist()
    )
    
    # 创建基准数据
    benchmark_returns = np.random.normal(0.0004, 0.015, days)
    benchmark_prices = 100 * np.cumprod(1 + benchmark_returns)
    benchmark_data = PriceData(
        prices=benchmark_prices.tolist(),
        dates=dates
    )
    
    # 执行风险分析
    calculator = RiskCalculator(price_data, benchmark_data)
    result = calculator.full_analysis()
    
    print("=" * 60)
    print("风险模型分析结果")
    print("=" * 60)
    
    result_dict = result.to_dict()
    for key, value in result_dict.items():
        print(f"{key:25}: {value}")
    
    print("=" * 60)
    
    # 压力测试
    tester = StressTester(price_data, beta=result.beta)
    scenarios = tester.run_all_scenarios()
    
    print("\n压力测试结果:")
    print("-" * 60)
    for scenario in scenarios:
        print(f"{scenario['scenario']:15}: {scenario['loss_pct']:>7.2%} (价格：{scenario['stressed_price']:.2f})")
    
    print("=" * 60)
    
    # 蒙特卡洛模拟
    mc_result = tester.monte_carlo_simulation(days=30, simulations=5000)
    print(f"\n蒙特卡洛模拟 (30 天):")
    print(f"当前价格：{mc_result['current_price']:.2f}")
    print(f"预期价格：{mc_result['expected_price']:.2f}")
    print(f"95% VaR:   {mc_result['var_95']:.2f}")
    print(f"最坏情况：{mc_result['worst_case']:.2f}")
    print(f"最好情况：{mc_result['best_case']:.2f}")
    print("=" * 60)
