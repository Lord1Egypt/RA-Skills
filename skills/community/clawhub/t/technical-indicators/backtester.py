"""
回测验证模块 - Backtesting Module
智能仓位管理系统的回测验证组件

功能:
1. 历史回测
2. 绩效评估
3. 风险分析
4. 参数优化
5. 蒙特卡洛验证
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from enum import Enum


class TradeType(Enum):
    """交易类型"""
    BUY = "buy"
    SELL = "sell"


@dataclass
class Trade:
    """交易记录"""
    trade_id: str
    trade_type: TradeType
    price: float
    shares: int
    timestamp: datetime
    position_pct: float
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    
    def to_dict(self) -> Dict:
        return {
            "trade_id": self.trade_id,
            "trade_type": self.trade_type.value,
            "price": round(self.price, 2),
            "shares": self.shares,
            "timestamp": self.timestamp.isoformat(),
            "position_pct": round(self.position_pct * 100, 1),
            "stop_loss": round(self.stop_loss, 2) if self.stop_loss else None,
            "take_profit": round(self.take_profit, 2) if self.take_profit else None
        }


@dataclass
class Position:
    """持仓记录"""
    entry_price: float
    entry_date: datetime
    shares: int
    position_value: float
    stop_loss: float
    take_profit: float
    position_pct: float
    
    current_price: float = 0.0
    exit_price: Optional[float] = None
    exit_date: Optional[datetime] = None
    exit_reason: Optional[str] = None
    
    @property
    def is_closed(self) -> bool:
        return self.exit_price is not None
    
    @property
    def pnl(self) -> float:
        if not self.is_closed:
            return (self.current_price - self.entry_price) * self.shares
        return (self.exit_price - self.entry_price) * self.shares
    
    @property
    def pnl_pct(self) -> float:
        if self.entry_price == 0:
            return 0.0
        if not self.is_closed:
            return (self.current_price - self.entry_price) / self.entry_price
        return (self.exit_price - self.entry_price) / self.entry_price


@dataclass
class BacktestResult:
    """回测结果"""
    # 基本信息
    start_date: datetime
    end_date: datetime
    initial_capital: float
    final_capital: float
    
    # 收益指标
    total_return: float
    annualized_return: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    
    # 风险指标
    max_drawdown: float
    max_drawdown_duration: int
    volatility: float
    var_95: float
    
    # 风险调整收益
    sharpe_ratio: float
    sortino_ratio: float
    calmar_ratio: float
    
    # 交易统计
    avg_trade_return: float
    avg_winning_trade: float
    avg_losing_trade: float
    profit_factor: float
    avg_holding_period: float
    
    # 仓位统计
    avg_position_size: float
    max_position_size: float
    
    trades: List[Trade] = field(default_factory=list)
    positions: List[Position] = field(default_factory=list)
    equity_curve: List[float] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "initial_capital": round(self.initial_capital, 2),
            "final_capital": round(self.final_capital, 2),
            "total_return": round(self.total_return * 100, 2),
            "annualized_return": round(self.annualized_return * 100, 2),
            "total_trades": self.total_trades,
            "winning_trades": self.winning_trades,
            "losing_trades": self.losing_trades,
            "win_rate": round(self.win_rate * 100, 1),
            "max_drawdown": round(self.max_drawdown * 100, 2),
            "max_drawdown_duration": self.max_drawdown_duration,
            "volatility": round(self.volatility * 100, 2),
            "var_95": round(self.var_95 * 100, 2),
            "sharpe_ratio": round(self.sharpe_ratio, 2),
            "sortino_ratio": round(self.sortino_ratio, 2),
            "calmar_ratio": round(self.calmar_ratio, 2),
            "avg_trade_return": round(self.avg_trade_return * 100, 2),
            "avg_winning_trade": round(self.avg_winning_trade * 100, 2),
            "avg_losing_trade": round(self.avg_losing_trade * 100, 2),
            "profit_factor": round(self.profit_factor, 2),
            "avg_holding_period": round(self.avg_holding_period, 1),
            "avg_position_size": round(self.avg_position_size * 100, 1),
            "max_position_size": round(self.max_position_size * 100, 1)
        }


class Backtester:
    """
    回测引擎
    
    使用智能仓位管理系统进行历史回测
    """
    
    TRADING_DAYS_PER_YEAR = 252
    
    def __init__(
        self,
        prices: List[float],
        dates: List[datetime],
        initial_capital: float = 1000000,
        commission_rate: float = 0.001,
        slippage: float = 0.001
    ):
        """
        初始化回测引擎
        
        Args:
            prices: 价格序列
            dates: 日期序列
            initial_capital: 初始资金
            commission_rate: 手续费率
            slippage: 滑点
        """
        self.prices = np.array(prices)
        self.dates = dates
        self.initial_capital = initial_capital
        self.commission_rate = commission_rate
        self.slippage = slippage
        
        # 状态变量
        self.cash = initial_capital
        self.positions: List[Position] = []
        self.closed_positions: List[Position] = []
        self.trades: List[Trade] = []
        self.equity_curve: List[float] = []
        
        self._trade_counter = 0
    
    def _generate_trade_id(self) -> str:
        """生成交易 ID"""
        self._trade_counter += 1
        return f"T{self._trade_counter:06d}"
    
    def _execute_buy(
        self,
        idx: int,
        position_pct: float,
        stop_loss: float,
        take_profit: float
    ) -> Optional[Position]:
        """
        执行买入
        
        Args:
            idx: 当前索引
            position_pct: 仓位百分比
            stop_loss: 止损价
            take_profit: 止盈价
        
        Returns:
            Optional[Position]: 新建持仓
        """
        if idx >= len(self.prices):
            return None
        
        # 计算可投资金额
        current_price = self.prices[idx]
        investable = self.cash * position_pct
        
        # 计算股数 (考虑滑点)
        execution_price = current_price * (1 + self.slippage)
        shares = int(investable / execution_price)
        
        if shares <= 0:
            return None
        
        # 计算手续费
        position_value = shares * execution_price
        commission = position_value * self.commission_rate
        total_cost = position_value + commission
        
        if total_cost > self.cash:
            shares = int((self.cash * 0.99) / execution_price)
            if shares <= 0:
                return None
            position_value = shares * execution_price
            commission = position_value * self.commission_rate
            total_cost = position_value + commission
        
        # 更新现金
        self.cash -= total_cost
        
        # 创建持仓
        position = Position(
            entry_price=execution_price,
            entry_date=self.dates[idx],
            shares=shares,
            position_value=position_value,
            stop_loss=stop_loss,
            take_profit=take_profit,
            position_pct=position_pct
        )
        
        # 记录交易
        trade = Trade(
            trade_id=self._generate_trade_id(),
            trade_type=TradeType.BUY,
            price=execution_price,
            shares=shares,
            timestamp=self.dates[idx],
            position_pct=position_pct,
            stop_loss=stop_loss,
            take_profit=take_profit
        )
        self.trades.append(trade)
        
        return position
    
    def _execute_sell(self, position: Position, idx: int, reason: str) -> float:
        """
        执行卖出
        
        Args:
            position: 持仓
            idx: 当前索引
            reason: 卖出原因
        
        Returns:
            float: 实现盈亏
        """
        if idx >= len(self.prices):
            return 0.0
        
        # 计算卖出价格 (考虑滑点)
        execution_price = self.prices[idx] * (1 - self.slippage)
        
        # 计算手续费
        position_value = position.shares * execution_price
        commission = position_value * self.commission_rate
        proceeds = position_value - commission
        
        # 更新现金
        self.cash += proceeds
        
        # 更新持仓
        position.exit_price = execution_price
        position.exit_date = self.dates[idx]
        position.exit_reason = reason
        
        # 记录交易
        trade = Trade(
            trade_id=self._generate_trade_id(),
            trade_type=TradeType.SELL,
            price=execution_price,
            shares=position.shares,
            timestamp=self.dates[idx],
            position_pct=position.position_pct
        )
        self.trades.append(trade)
        
        return position.pnl
    
    def _check_exit_conditions(self, position: Position, idx: int) -> Optional[str]:
        """
        检查退出条件
        
        Args:
            position: 持仓
            idx: 当前索引
        
        Returns:
            Optional[str]: 退出原因 (如果触发)
        """
        current_price = self.prices[idx]
        position.current_price = current_price
        
        # 检查止损
        if position.stop_loss and current_price <= position.stop_loss:
            return "stop_loss"
        
        # 检查止盈
        if position.take_profit and current_price >= position.take_profit:
            return "take_profit"
        
        return None
    
    def run_backtest(
        self,
        position_sizer_class,
        signal_generator,
        risk_calculator
    ) -> BacktestResult:
        """
        运行回测
        
        Args:
            position_sizer_class: 仓位管理器类
            signal_generator: 信号生成器函数
            risk_calculator: 风险计算器
        
        Returns:
            BacktestResult: 回测结果
        """
        n = len(self.prices)
        
        # 用于计算信号的窗口
        window = 60
        
        for idx in range(window, n):
            current_price = self.prices[idx]
            current_date = self.dates[idx]
            
            # 更新现有持仓
            positions_to_close = []
            for position in self.positions:
                position.current_price = current_price
                exit_reason = self._check_exit_conditions(position, idx)
                if exit_reason:
                    positions_to_close.append((position, exit_reason))
            
            # 执行卖出
            for position, reason in positions_to_close:
                self._execute_sell(position, idx, reason)
                self.positions.remove(position)
                self.closed_positions.append(position)
            
            # 如果没有持仓，考虑开仓
            if len(self.positions) == 0:
                # 生成信号
                signal_data = signal_generator(idx, self.prices, self.dates)
                
                if signal_data and signal_data.get('signal', 0) > 50:
                    # 创建仓位管理器
                    sizer = position_sizer_class(**signal_data.get('sizer_params', {}))
                    
                    # 计算仓位
                    position_pct = sizer.calculate_position_percentage()
                    
                    # 计算止损止盈
                    stop_loss = sizer.calculate_stop_loss(
                        current_price,
                        atr=signal_data.get('atr'),
                        support_level=signal_data.get('support')
                    )
                    take_profit = sizer.calculate_take_profit(
                        current_price,
                        resistance_level=signal_data.get('resistance')
                    )
                    
                    # 执行买入
                    position = self._execute_buy(
                        idx,
                        position_pct,
                        stop_loss,
                        take_profit
                    )
                    
                    if position:
                        self.positions.append(position)
            
            # 记录权益曲线
            total_equity = self.cash
            for position in self.positions:
                position.current_price = current_price
                total_equity += position.shares * current_price
            self.equity_curve.append(total_equity)
        
        # 强制平仓所有剩余持仓
        if self.positions and len(self.prices) > 0:
            final_idx = len(self.prices) - 1
            for position in self.positions[:]:
                self._execute_sell(position, final_idx, "end_of_backtest")
                self.closed_positions.append(position)
            self.positions = []
        
        return self._calculate_results()
    
    def _calculate_results(self) -> BacktestResult:
        """计算回测结果"""
        if not self.equity_curve:
            return BacktestResult(
                start_date=self.dates[0],
                end_date=self.dates[-1],
                initial_capital=self.initial_capital,
                final_capital=self.initial_capital,
                total_return=0,
                annualized_return=0,
                total_trades=0,
                winning_trades=0,
                losing_trades=0,
                win_rate=0,
                max_drawdown=0,
                max_drawdown_duration=0,
                volatility=0,
                var_95=0,
                sharpe_ratio=0,
                sortino_ratio=0,
                calmar_ratio=0,
                avg_trade_return=0,
                avg_winning_trade=0,
                avg_losing_trade=0,
                profit_factor=0,
                avg_holding_period=0,
                avg_position_size=0,
                max_position_size=0,
                trades=self.trades,
                positions=self.closed_positions,
                equity_curve=self.equity_curve
            )
        
        # 基本统计
        final_capital = self.equity_curve[-1]
        total_return = (final_capital - self.initial_capital) / self.initial_capital
        
        # 年化收益
        days = (self.dates[-1] - self.dates[0]).days
        years = days / 365
        if years > 0:
            annualized_return = (final_capital / self.initial_capital) ** (1 / years) - 1
        else:
            annualized_return = 0
        
        # 交易统计
        total_trades = len(self.closed_positions)
        winning_trades = sum(1 for p in self.closed_positions if p.pnl > 0)
        losing_trades = total_trades - winning_trades
        win_rate = winning_trades / total_trades if total_trades > 0 else 0
        
        # 盈亏统计
        if winning_trades > 0:
            avg_winning = np.mean([p.pnl for p in self.closed_positions if p.pnl > 0])
        else:
            avg_winning = 0
        
        if losing_trades > 0:
            avg_losing = np.mean([p.pnl for p in self.closed_positions if p.pnl < 0])
        else:
            avg_losing = 0
        
        # 盈利因子
        gross_profit = sum(p.pnl for p in self.closed_positions if p.pnl > 0)
        gross_loss = abs(sum(p.pnl for p in self.closed_positions if p.pnl < 0))
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
        
        # 最大回撤
        equity_array = np.array(self.equity_curve)
        cummax = np.maximum.accumulate(equity_array)
        drawdown = (cummax - equity_array) / cummax
        max_drawdown = drawdown.max()
        
        # 回撤持续时间
        in_drawdown = False
        max_duration = 0
        current_duration = 0
        for dd in drawdown:
            if dd > 0:
                if not in_drawdown:
                    in_drawdown = True
                    current_duration = 1
                else:
                    current_duration += 1
                max_duration = max(max_duration, current_duration)
            else:
                in_drawdown = False
        
        # 收益率序列
        returns = np.diff(equity_array) / equity_array[:-1]
        
        # 波动率
        volatility = returns.std() * np.sqrt(self.TRADING_DAYS_PER_YEAR) if len(returns) > 0 else 0
        
        # VaR
        var_95 = np.percentile(returns, 5) if len(returns) > 0 else 0
        
        # 夏普比率
        if volatility > 0:
            excess_return = annualized_return - 0.03  # 假设无风险利率 3%
            sharpe_ratio = excess_return / volatility
        else:
            sharpe_ratio = 0
        
        # 索提诺比率
        downside_returns = returns[returns < 0]
        if len(downside_returns) > 0:
            downside_std = downside_returns.std() * np.sqrt(self.TRADING_DAYS_PER_YEAR)
            sortino_ratio = (annualized_return - 0.03) / downside_std if downside_std > 0 else 0
        else:
            sortino_ratio = 0
        
        # 卡玛比率
        calmar_ratio = annualized_return / max_drawdown if max_drawdown > 0 else 0
        
        # 平均持仓期
        holding_periods = []
        for p in self.closed_positions:
            if p.exit_date and p.entry_date:
                days_held = (p.exit_date - p.entry_date).days
                holding_periods.append(days_held)
        avg_holding_period = np.mean(holding_periods) if holding_periods else 0
        
        # 仓位统计
        position_sizes = [p.position_pct for p in self.closed_positions]
        avg_position_size = np.mean(position_sizes) if position_sizes else 0
        max_position_size = np.max(position_sizes) if position_sizes else 0
        
        # 平均交易收益
        all_pnl_pcts = [p.pnl_pct for p in self.closed_positions]
        avg_trade_return = np.mean(all_pnl_pcts) if all_pnl_pcts else 0
        
        return BacktestResult(
            start_date=self.dates[0],
            end_date=self.dates[-1],
            initial_capital=self.initial_capital,
            final_capital=final_capital,
            total_return=total_return,
            annualized_return=annualized_return,
            total_trades=total_trades,
            winning_trades=winning_trades,
            losing_trades=losing_trades,
            win_rate=win_rate,
            max_drawdown=max_drawdown,
            max_drawdown_duration=max_duration,
            volatility=volatility,
            var_95=var_95,
            sharpe_ratio=sharpe_ratio,
            sortino_ratio=sortino_ratio,
            calmar_ratio=calmar_ratio,
            avg_trade_return=avg_trade_return,
            avg_winning_trade=avg_winning / self.initial_capital if avg_winning > 0 else 0,
            avg_losing_trade=avg_losing / self.initial_capital if avg_losing < 0 else 0,
            profit_factor=profit_factor,
            avg_holding_period=avg_holding_period,
            avg_position_size=avg_position_size,
            max_position_size=max_position_size,
            trades=self.trades,
            positions=self.closed_positions,
            equity_curve=self.equity_curve
        )


class SignalGenerator:
    """
    信号生成器示例
    实际使用中应替换为真实的技术指标计算
    """
    
    def __init__(self, lookback: int = 20):
        self.lookback = lookback
    
    def generate_signal(
        self,
        idx: int,
        prices: np.ndarray,
        dates: List[datetime]
    ) -> Optional[Dict]:
        """
        生成交易信号
        
        Args:
            idx: 当前索引
            prices: 价格序列
            dates: 日期序列
        
        Returns:
            Optional[Dict]: 信号数据
        """
        if idx < self.lookback:
            return None
        
        # 简单示例：均线交叉策略
        short_window = 10
        long_window = 30
        
        if idx < long_window:
            return None
        
        short_ma = prices[idx-short_window:idx].mean()
        long_ma = prices[idx-long_window:idx].mean()
        current_price = prices[idx]
        
        # 计算 ATR
        if idx >= 14:
            highs = prices[idx-14:idx] * 1.02  # 模拟高点
            lows = prices[idx-14:idx] * 0.98   # 模拟低点
            tr = highs - lows
            atr = tr.mean()
        else:
            atr = current_price * 0.02
        
        # 信号强度
        if short_ma > long_ma:
            signal_strength = 60 + (short_ma - long_ma) / long_ma * 100
        else:
            signal_strength = 40 + (short_ma - long_ma) / long_ma * 100
        
        signal_strength = np.clip(signal_strength, 0, 100)
        
        # 支撑阻力位
        support = prices[idx-30:idx].min()
        resistance = prices[idx-30:idx].max()
        
        return {
            'signal': signal_strength,
            'sizer_params': {
                'signal_strength': {
                    'technical': signal_strength,
                    'pattern': 70,
                    'multi_period': 65
                },
                'risk_metrics': {
                    'volatility': atr / current_price,
                    'max_drawdown': 0.2,
                    'beta': 1.0
                },
                'market_env': {
                    'trend': 'bullish' if short_ma > long_ma else 'bearish',
                    'industry_health': 0.6,
                    'sentiment': 0.5
                },
                'capital_info': {
                    'total': 1000000,
                    'available': 800000,
                    'risk_tolerance': 0.6
                }
            },
            'atr': atr,
            'support': support,
            'resistance': resistance
        }


# ==================== 使用示例 ====================

if __name__ == "__main__":
    # 生成示例数据
    np.random.seed(42)
    days = 500
    dates = [datetime.now() - timedelta(days=i) for i in range(days)][::-1]
    
    # 生成价格序列 (带趋势)
    returns = np.random.normal(0.0005, 0.02, days)
    prices = 100 * np.cumprod(1 + returns)
    
    # 创建回测引擎
    backtester = Backtester(
        prices=prices.tolist(),
        dates=dates,
        initial_capital=1000000,
        commission_rate=0.001,
        slippage=0.001
    )
    
    # 创建信号生成器
    signal_gen = SignalGenerator(lookback=30)
    
    # 运行回测
    print("=" * 60)
    print("智能仓位管理系统 - 回测验证")
    print("=" * 60)
    print(f"回测区间：{dates[0].date()} 至 {dates[-1].date()}")
    print(f"初始资金：CNY 1,000,000")
    print(f"数据点数：{len(prices)}")
    print("=" * 60)
    print("\n运行回测中...")
    
    # 注意：这里需要导入 position_sizer 模块
    # 为简化示例，我们使用简化的仓位计算
    from position_sizer import PositionSizer, SignalStrength, RiskMetrics, MarketEnvironment, CapitalInfo, MarketTrend
    
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
                total_capital=kwargs.get('capital_info', {}).get('total', 1000000),
                available_capital=kwargs.get('capital_info', {}).get('available', 800000),
                risk_tolerance=kwargs.get('capital_info', {}).get('risk_tolerance', 0.5)
            )
        ),
        signal_generator=signal_gen.generate_signal,
        risk_calculator=None
    )
    
    print("\n" + "=" * 60)
    print("回测结果汇总")
    print("=" * 60)
    
    result_dict = result.to_dict()
    for key, value in result_dict.items():
        print(f"{key:25}: {value}")
    
    print("=" * 60)
    print(f"\n总交易次数：{result.total_trades}")
    print(f"胜率：{result.win_rate * 100:.1f}%")
    print(f"总收益：{result.total_return * 100:.2f}%")
    print(f"年化收益：{result.annualized_return * 100:.2f}%")
    print(f"最大回撤：{result.max_drawdown * 100:.2f}%")
    print(f"夏普比率：{result.sharpe_ratio:.2f}")
    print(f"盈利因子：{result.profit_factor:.2f}")
    print("=" * 60)
