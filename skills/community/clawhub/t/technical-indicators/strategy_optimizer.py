"""
基于遗传算法的MACD+RSI策略参数优化系统
"""

import numpy as np
import pandas as pd
import random
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class MACDRSIStrategy:
    """MACD+RSI组合策略类"""
    
    def __init__(self, params: Dict):
        self.params = params
        
    def calculate_macd(self, prices: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        计算MACD指标
        :param prices: 价格序列
        :return: (macd_line, signal_line, histogram)
        """
        fast_period = int(self.params['macd_fast'])
        slow_period = int(self.params['macd_slow'])
        signal_period = int(self.params['macd_signal'])
        
        # 计算EMA
        ema_fast = self._ema(prices, fast_period)
        ema_slow = self._ema(prices, slow_period)
        
        # MACD线
        macd_line = ema_fast - ema_slow
        # 信号线
        signal_line = self._ema(macd_line, signal_period)
        # 柱状图
        histogram = macd_line - signal_line
        
        return macd_line, signal_line, histogram
    
    def calculate_rsi(self, prices: np.ndarray) -> np.ndarray:
        """
        计算RSI指标
        :param prices: 价格序列
        :return: RSI值数组
        """
        period = int(self.params['rsi_period'])
        
        delta = np.diff(prices)
        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)
        
        avg_gain = np.zeros_like(prices)
        avg_loss = np.zeros_like(prices)
        
        # 初始化前period个值
        avg_gain[period] = np.mean(gain[:period])
        avg_loss[period] = np.mean(loss[:period])
        
        # 计算后续值
        for i in range(period + 1, len(prices)):
            avg_gain[i] = (avg_gain[i-1] * (period - 1) + gain[i-1]) / period
            avg_loss[i] = (avg_loss[i-1] * (period - 1) + loss[i-1]) / period
        
        rs = avg_gain / (avg_loss + 1e-10)  # 避免除零
        rsi = 100 - (100 / (1 + rs))
        
        # 前period个值设为NaN或初始值
        rsi[:period] = 50  # 初始为中性值
        
        return rsi
    
    def _ema(self, prices: np.ndarray, period: int) -> np.ndarray:
        """计算指数移动平均"""
        ema = np.zeros_like(prices)
        ema[0] = prices[0]
        
        multiplier = 2 / (period + 1)
        for i in range(1, len(prices)):
            ema[i] = (prices[i] * multiplier) + (ema[i-1] * (1 - multiplier))
        
        return ema
    
    def generate_signals(self, prices: np.ndarray) -> np.ndarray:
        """
        生成交易信号
        :param prices: 价格序列
        :return: 交易信号数组 (1=买入, -1=卖出, 0=持有)
        """
        macd_line, signal_line, histogram = self.calculate_macd(prices)
        rsi = self.calculate_rsi(prices)
        
        signals = np.zeros(len(prices))
        
        # 获取超买超卖阈值
        rsi_oversold = self.params['rsi_oversold']
        rsi_overbought = self.params['rsi_overbought']
        
        # 生成信号
        for i in range(1, len(prices)):
            # MACD金叉（MACD线上穿信号线）且RSI处于超卖区
            if (macd_line[i] > signal_line[i] and 
                macd_line[i-1] <= signal_line[i-1] and 
                rsi[i] < rsi_oversold):
                signals[i] = 1  # 买入信号
            
            # MACD死叉（MACD线下穿信号线）且RSI处于超买区
            elif (macd_line[i] < signal_line[i] and 
                  macd_line[i-1] >= signal_line[i-1] and 
                  rsi[i] > rsi_overbought):
                signals[i] = -1  # 卖出信号
        
        return signals


class GeneticAlgorithmOptimizer:
    """基于遗传算法的参数优化器"""
    
    def __init__(self, price_data: np.ndarray):
        self.price_data = price_data
        self.param_ranges = {
            "macd_fast": [8, 15],      # 8-15
            "macd_slow": [17, 30],     # 17-30
            "macd_signal": [5, 12],    # 5-12
            "rsi_period": [7, 21],     # 7-21
            "rsi_oversold": [20, 35],  # 20-35
            "rsi_overbought": [65, 80] # 65-80
        }
        
        # 遗传算法参数
        self.population_size = 50
        self.generations = 100
        self.crossover_rate = 0.8
        self.mutation_rate = 0.1
        self.tournament_size = 3
        
    def initialize_population(self) -> List[Dict]:
        """初始化种群"""
        population = []
        for _ in range(self.population_size):
            individual = {}
            for param, (min_val, max_val) in self.param_ranges.items():
                if param in ['macd_fast', 'macd_slow', 'macd_signal', 'rsi_period']:
                    # 整数参数
                    individual[param] = random.randint(min_val, max_val)
                else:
                    # 浮点数参数
                    individual[param] = round(random.uniform(min_val, max_val), 2)
            population.append(individual)
        return population
    
    def evaluate_fitness(self, params: Dict) -> float:
        """评估个体适应度（夏普比率）"""
        try:
            strategy = MACDRSIStrategy(params)
            signals = strategy.generate_signals(self.price_data)
            
            # 计算收益
            returns = np.diff(self.price_data) / self.price_data[:-1]
            strategy_returns = returns * np.roll(signals, 1)[1:]  # 错位计算
            
            # 确保长度一致
            if len(strategy_returns) != len(returns):
                min_len = min(len(strategy_returns), len(returns))
                strategy_returns = strategy_returns[:min_len]
            
            if len(strategy_returns) == 0:
                return -np.inf
            
            # 计算夏普比率
            if np.std(strategy_returns) == 0:
                sharpe_ratio = 0
            else:
                sharpe_ratio = np.mean(strategy_returns) / (np.std(strategy_returns) + 1e-10) * np.sqrt(252)  # 年化
            
            # 计算最大回撤
            cumulative_returns = np.cumprod(1 + strategy_returns)
            running_max = np.maximum.accumulate(cumulative_returns)
            drawdown = (cumulative_returns - running_max) / running_max
            max_drawdown = np.min(drawdown) if len(drawdown) > 0 else 0
            
            # 应用约束：最大回撤 < 20%
            if max_drawdown < -0.20:  # 小于-20%则惩罚
                sharpe_ratio -= 10  # 惩罚项
            
            return sharpe_ratio
            
        except Exception as e:
            print(f"Fitness evaluation error: {e}")
            return -np.inf
    
    def tournament_selection(self, population: List[Dict], fitnesses: List[float]) -> Dict:
        """锦标赛选择"""
        selected_indices = random.sample(range(len(population)), self.tournament_size)
        selected_fitnesses = [fitnesses[i] for i in selected_indices]
        winner_idx = selected_indices[np.argmax(selected_fitnesses)]
        return population[winner_idx]
    
    def crossover(self, parent1: Dict, parent2: Dict) -> Tuple[Dict, Dict]:
        """交叉操作"""
        if random.random() > self.crossover_rate:
            return parent1.copy(), parent2.copy()
        
        child1, child2 = {}, {}
        for param in self.param_ranges.keys():
            if random.random() < 0.5:
                child1[param] = parent1[param]
                child2[param] = parent2[param]
            else:
                child1[param] = parent2[param]
                child2[param] = parent1[param]
        
        return child1, child2
    
    def mutate(self, individual: Dict) -> Dict:
        """变异操作"""
        mutated = individual.copy()
        for param, (min_val, max_val) in self.param_ranges.items():
            if random.random() < self.mutation_rate:
                if param in ['macd_fast', 'macd_slow', 'macd_signal', 'rsi_period']:
                    # 整数参数变异
                    current_val = mutated[param]
                    # 在范围内随机调整
                    adjustment = random.randint(-2, 2)
                    new_val = max(min_val, min(max_val, current_val + adjustment))
                    mutated[param] = new_val
                else:
                    # 浮点数参数变异
                    current_val = mutated[param]
                    # 在范围内小幅度调整
                    adjustment = random.uniform(-3, 3)
                    new_val = max(min_val, min(max_val, current_val + adjustment))
                    mutated[param] = round(new_val, 2)
        
        return mutated
    
    def optimize(self) -> Dict:
        """执行遗传算法优化"""
        print("开始遗传算法优化...")
        print(f"种群大小: {self.population_size}, 代数: {self.generations}")
        
        # 初始化种群
        population = self.initialize_population()
        
        best_fitness_history = []
        
        for generation in range(self.generations):
            # 评估当前种群适应度
            fitnesses = [self.evaluate_fitness(individual) for individual in population]
            
            # 记录最佳适应度
            best_fitness = max(fitnesses)
            best_individual = population[np.argmax(fitnesses)]
            best_fitness_history.append(best_fitness)
            
            if generation % 10 == 0:
                print(f"第 {generation} 代 - 最佳夏普比率: {best_fitness:.4f}")
            
            # 创建新种群
            new_population = []
            
            # 保留最优个体（精英保留）
            elite_idx = np.argmax(fitnesses)
            new_population.append(population[elite_idx])
            
            # 生成其余个体
            while len(new_population) < self.population_size:
                parent1 = self.tournament_selection(population, fitnesses)
                parent2 = self.tournament_selection(population, fitnesses)
                
                child1, child2 = self.crossover(parent1, parent2)
                
                child1 = self.mutate(child1)
                child2 = self.mutate(child2)
                
                new_population.extend([child1, child2])
            
            # 确保种群大小正确
            population = new_population[:self.population_size]
        
        # 最终评估
        final_fitnesses = [self.evaluate_fitness(individual) for individual in population]
        best_idx = np.argmax(final_fitnesses)
        best_individual = population[best_idx]
        best_fitness = final_fitnesses[best_idx]
        
        print(f"优化完成! 最佳夏普比率: {best_fitness:.4f}")
        
        # 计算最终策略表现
        performance = self.calculate_performance_metrics(best_individual)
        
        result = {
            "best_params": best_individual,
            "sharpe_ratio": performance['sharpe_ratio'],
            "total_return": performance['total_return'],
            "max_drawdown": performance['max_drawdown'],
            "win_rate": performance['win_rate'],
            "fitness_history": best_fitness_history
        }
        
        return result
    
    def calculate_performance_metrics(self, params: Dict) -> Dict:
        """计算策略性能指标"""
        strategy = MACDRSIStrategy(params)
        signals = strategy.generate_signals(self.price_data)
        
        # 计算收益
        returns = np.diff(self.price_data) / self.price_data[:-1]
        strategy_returns = returns * np.roll(signals, 1)[1:]  # 错位计算
        
        # 确保长度一致
        if len(strategy_returns) != len(returns):
            min_len = min(len(strategy_returns), len(returns))
            strategy_returns = strategy_returns[:min_len]
            returns = returns[:min_len]
        
        if len(strategy_returns) == 0:
            return {
                "sharpe_ratio": 0,
                "total_return": 0,
                "max_drawdown": 0,
                "win_rate": 0
            }
        
        # 总收益率
        total_return = (np.prod(1 + strategy_returns) - 1) * 100
        
        # 夏普比率
        if np.std(strategy_returns) == 0:
            sharpe_ratio = 0
        else:
            daily_return = np.mean(strategy_returns)
            daily_std = np.std(strategy_returns)
            sharpe_ratio = daily_return / (daily_std + 1e-10) * np.sqrt(252)  # 年化
        
        # 最大回撤
        cumulative_returns = np.cumprod(1 + strategy_returns)
        running_max = np.maximum.accumulate(cumulative_returns)
        drawdown = (cumulative_returns - running_max) / running_max
        max_drawdown = np.min(drawdown) if len(drawdown) > 0 else 0
        
        # 胜率
        positive_returns = np.sum(strategy_returns > 0)
        total_trades = len(strategy_returns)
        win_rate = (positive_returns / total_trades * 100) if total_trades > 0 else 0
        
        return {
            "sharpe_ratio": round(sharpe_ratio, 4),
            "total_return": round(total_return, 2),
            "max_drawdown": round(max_drawdown * 100, 2),
            "win_rate": round(win_rate, 2)
        }


def simulate_price_data(days: int = 1000) -> np.ndarray:
    """模拟价格数据用于测试"""
    np.random.seed(42)
    returns = np.random.normal(0.0005, 0.02, days)  # 日收益率均值0.05%，标准差2%
    prices = 100 * np.exp(np.cumsum(returns))  # 几何布朗运动
    return prices


def main():
    """主函数 - 演示优化过程"""
    print("=== MACD+RSI策略参数遗传算法优化系统 ===")
    
    # 生成模拟价格数据
    print("生成模拟价格数据...")
    price_data = simulate_price_data(days=1000)
    
    # 创建优化器
    optimizer = GeneticAlgorithmOptimizer(price_data)
    
    # 执行优化
    result = optimizer.optimize()
    
    # 输出结果
    print("\n=== 优化结果 ===")
    print(f"最佳参数:")
    for param, value in result['best_params'].items():
        print(f"  {param}: {value}")
    
    print(f"\n性能指标:")
    print(f"  夏普比率: {result['sharpe_ratio']}")
    print(f"  总收益率: {result['total_return']}%")
    print(f"  最大回撤: {result['max_drawdown']}%")
    print(f"  胜率: {result['win_rate']}%")
    
    return result


if __name__ == "__main__":
    main()