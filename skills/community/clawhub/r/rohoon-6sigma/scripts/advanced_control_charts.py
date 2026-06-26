#!/usr/bin/env python3
"""
高级控制图模块
包含: CUSUM, EWMA, I-MR, Moving Average, Z-Chart
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import io


@dataclass
class ControlChartResult:
    """控制图结果"""
    chart_type: str
    data: np.ndarray
    cl: float  # Center Line
    ucl: float  # Upper Control Limit
    lcl: float  # Lower Control Limit
    violations: List[int]  # 违规点索引
    statistics: Dict[str, float]


class CUSUMChart:
    """
    CUSUM (累积和控制图)
    用于检测过程均值的小偏移
    """
    
    def __init__(self, target: float, sigma: float, k: float = 0.5):
        """
        初始化 CUSUM 图
        
        参数:
            target: 目标值/均值
            sigma: 标准差
            k: 参考值 (通常为 0.5 倍标准差)
        """
        self.target = target
        self.sigma = sigma
        self.k = k * sigma  # 允许偏移量
        
    def calculate(self, data: np.ndarray) -> ControlChartResult:
        """计算 CUSUM 统计量"""
        n = len(data)
        
        # 累积和 (双向)
        cusum_plus = np.zeros(n)  # 检测向上偏移
        cusum_minus = np.zeros(n)  # 检测向下偏移
        
        for i in range(n):
            if i == 0:
                cusum_plus[i] = max(0, data[i] - self.target - self.k)
                cusum_minus[i] = max(0, self.target - self.k - data[i])
            else:
                cusum_plus[i] = max(0, cusum_plus[i-1] + data[i] - self.target - self.k)
                cusum_minus[i] = max(0, cusum_minus[i-1] + self.target - self.k - data[i])
        
        # 组合 CUSUM (可选)
        cusum_combined = cusum_plus + cusum_minus
        
        # 控制限 (h 通常设为 4-5 倍 sigma)
        h = 5 * self.sigma
        ucl = h
        lcl = 0
        
        # 检测违规点
        violations = []
        for i in range(n):
            if cusum_combined[i] > ucl:
                violations.append(i)
        
        return ControlChartResult(
            chart_type='CUSUM',
            data=cusum_combined,
            cl=0,
            ucl=ucl,
            lcl=lcl,
            violations=violations,
            statistics={
                'target': self.target,
                'sigma': self.sigma,
                'k': self.k,
                'h': h,
                'max_cusum': np.max(cusum_combined)
            }
        )


class EWMAChart:
    """
    EWMA (指数加权移动平均控制图)
    用于检测过程均值的中小偏移
    """
    
    def __init__(self, target: float, sigma: float, lambda_: float = 0.2):
        """
        初始化 EWMA 图
        
        参数:
            target: 目标值/均值
            sigma: 标准差
            lambda_: 平滑参数 (0 < lambda_ <= 1)
        """
        self.target = target
        self.sigma = sigma
        self.lambda_ = lambda_
        
    def calculate(self, data: np.ndarray) -> ControlChartResult:
        """计算 EWMA 统计量"""
        n = len(data)
        
        # EWMA 统计量
        ewma = np.zeros(n)
        
        for i in range(n):
            if i == 0:
                ewma[i] = self.target
            else:
                ewma[i] = self.lambda_ * data[i] + (1 - self.lambda_) * ewma[i-1]
        
        # 控制限 (随时间收缩)
        sigma_ewma = self.sigma * np.sqrt(self.lambda_ / (2 - self.lambda_))
        
        # 初始控制限较宽，后续收缩
        ucl = np.array([self.target + 3 * sigma_ewma * np.sqrt(self.lambda_ * (1 - (1 - self.lambda_)**(2*(i+1))) / (2 - self.lambda_)) for i in range(n)])
        lcl = np.array([self.target - 3 * sigma_ewma * np.sqrt(self.lambda_ * (1 - (1 - self.lambda_)**(2*(i+1))) / (2 - self.lambda_)) for i in range(n)])
        
        # 检测违规点
        violations = []
        for i in range(n):
            if i >= 1 and (ewma[i] > ucl[i] or ewma[i] < lcl[i]):
                violations.append(i)
        
        return ControlChartResult(
            chart_type='EWMA',
            data=ewma,
            cl=self.target,
            ucl=ucl[-1],  # 稳态控制限
            lcl=lcl[-1],
            violations=violations,
            statistics={
                'target': self.target,
                'sigma': self.sigma,
                'lambda': self.lambda_,
                'sigma_ewma': sigma_ewma
            }
        )


class IMRChart:
    """
    I-MR (单值-移动极差控制图)
    用于个体测量值的过程监控
    """
    
    def __init__(self):
        pass
        
    def calculate(self, data: np.ndarray) -> ControlChartResult:
        """计算 I-MR 控制图"""
        n = len(data)
        
        # I 图 (单值图)
        i_values = data
        i_mean = np.mean(i_values)
        
        # 移动极差
        mr = np.abs(np.diff(data))
        mr_bar = np.mean(mr)
        
        # 控制限 (d2 = 1.128 for n=2)
        d2 = 1.128
        sigma = mr_bar / d2
        
        # I 图控制限
        ucl_i = i_mean + 3 * sigma
        lcl_i = i_mean - 3 * sigma
        
        # MR 图控制限
        D3, D4 = 0, 3.267  # for n=2
        ucl_r = D4 * mr_bar
        lcl_r = D3 * mr_bar
        
        # 检测违规点
        violations_i = [i for i in range(n) if i_values[i] > ucl_i or i_values[i] < lcl_i]
        violations_mr = [i for i in range(n-1) if mr[i] > ucl_r or mr[i] < lcl_r]
        violations = violations_i + violations_mr
        
        return ControlChartResult(
            chart_type='I-MR',
            data=i_values,
            cl=i_mean,
            ucl=ucl_i,
            lcl=lcl_i,
            violations=violations,
            statistics={
                'i_mean': i_mean,
                'mr_bar': mr_bar,
                'sigma': sigma,
                'ucl_mr': ucl_r,
                'lcl_mr': lcl_r
            }
        )


class MAMRChart:
    """
    MAMR (移动平均-移动极差控制图)
    """
    
    def __init__(self, window_size: int = 5):
        """
        初始化 MAMR 图
        
        参数:
            window_size: 移动窗口大小
        """
        self.window_size = window_size
        
    def calculate(self, data: np.ndarray) -> ControlChartResult:
        """计算 MAMR 控制图"""
        n = len(data)
        
        # 移动平均
        ma = np.zeros(n)
        for i in range(n):
            start = max(0, i - self.window_size + 1)
            ma[i] = np.mean(data[start:i+1])
        
        # 移动极差
        mr = np.zeros(n)
        for i in range(n):
            start = max(0, i - self.window_size + 1)
            mr[i] = np.ptp(data[start:i+1])
        
        mr_bar = np.mean(mr[1:])  # 跳过第一个点
        
        # 控制限
        d2 = 1.128
        sigma = mr_bar / d2
        
        ucl = np.mean(ma) + 3 * sigma / np.sqrt(self.window_size)
        lcl = np.mean(ma) - 3 * sigma / np.sqrt(self.window_size)
        
        # 检测违规点
        violations = [i for i in range(n) if ma[i] > ucl or ma[i] < lcl]
        
        return ControlChartResult(
            chart_type='MAMR',
            data=ma,
            cl=np.mean(ma),
            ucl=ucl,
            lcl=lcl,
            violations=violations,
            statistics={
                'window_size': self.window_size,
                'mr_bar': mr_bar,
                'sigma': sigma
            }
        )


class HotellingT2Chart:
    """
    Hotelling T2 控制图
    多变量统计过程控制
    """
    
    def __init__(self):
        pass
        
    def calculate(self, data: np.ndarray, alpha: float = 0.05) -> ControlChartResult:
        """
        计算 Hotelling T2 统计量
        
        参数:
            data: 二维数组 (n_samples × n_variables)
            alpha: 显著性水平
        """
        import scipy.stats as scipy_stats
        n, p = data.shape
        
        # 均值向量
        mean_vec = np.mean(data, axis=0)
        
        # 协方差矩阵
        cov_matrix = np.cov(data, rowvar=False)
        
        # 逆协方差矩阵
        try:
            cov_inv = np.linalg.inv(cov_matrix)
        except np.linalg.LinAlgError:
            # 如果协方差矩阵奇异，使用伪逆
            cov_inv = np.linalg.pinv(cov_matrix)
        
        # 计算 T² 统计量
        t2_values = np.zeros(n)
        for i in range(n):
            diff = data[i] - mean_vec
            t2_values[i] = diff @ cov_inv @ diff
        
        # 控制限
        # Phase I (with estimated parameters)
        f_stat = (p * (n - 1) * (n + 1)) / (n * (n - p))
        ucl_phase1 = f_stat * scipy_stats.f.ppf(1 - alpha, p, n - p)
        
        # Phase II (known parameters)
        ucl_phase2 = (p * (n + 1) * (n - 1)) / (n * (n - p)) * scipy_stats.f.ppf(1 - alpha, p, n - p)
        
        # 使用 Phase I 控制限
        ucl = ucl_phase1
        lcl = 0
        
        # 检测违规点
        violations = [i for i in range(n) if t2_values[i] > ucl]
        
        return ControlChartResult(
            chart_type='Hotelling T2',
            data=t2_values,
            cl=np.mean(t2_values),
            ucl=ucl,
            lcl=lcl,
            violations=violations,
            statistics={
                'n_samples': n,
                'n_variables': p,
                'mean_vector': mean_vec,
                'ucl_phase1': ucl_phase1,
                'ucl_phase2': ucl_phase2
            }
        )


# 需要 scipy.stats
import scipy.stats


def run_cusum(data: np.ndarray, target: float, sigma: float, k: float = 0.5) -> Dict:
    """运行 CUSUM 分析"""
    chart = CUSUMChart(target, sigma, k)
    result = chart.calculate(data)
    return {
        'chart_type': result.chart_type,
        'data': result.data.tolist(),
        'cl': result.cl,
        'ucl': result.ucl,
        'lcl': result.lcl,
        'violations': result.violations,
        'statistics': result.statistics
    }


def run_ewma(data: np.ndarray, target: float, sigma: float, lambda_: float = 0.2) -> Dict:
    """运行 EWMA 分析"""
    chart = EWMAChart(target, sigma, lambda_)
    result = chart.calculate(data)
    return {
        'chart_type': result.chart_type,
        'data': result.data.tolist(),
        'cl': result.cl,
        'ucl': result.ucl,
        'lcl': result.lcl,
        'violations': result.violations,
        'statistics': result.statistics
    }


def run_imr(data: np.ndarray) -> Dict:
    """运行 I-MR 分析"""
    chart = IMRChart()
    result = chart.calculate(data)
    return {
        'chart_type': result.chart_type,
        'data': result.data.tolist(),
        'cl': result.cl,
        'ucl': result.ucl,
        'lcl': result.lcl,
        'violations': result.violations,
        'statistics': result.statistics
    }


def run_mamr(data: np.ndarray, window_size: int = 5) -> Dict:
    """运行 MAMR 分析"""
    chart = MAMRChart(window_size)
    result = chart.calculate(data)
    return {
        'chart_type': result.chart_type,
        'data': result.data.tolist(),
        'cl': result.cl,
        'ucl': result.ucl,
        'lcl': result.lcl,
        'violations': result.violations,
        'statistics': result.statistics
    }


def run_hotelling_t2(data: np.ndarray, alpha: float = 0.05) -> Dict:
    """运行 Hotelling T2 分析"""
    import scipy.stats as scipy_stats
    chart = HotellingT2Chart()
    result = chart.calculate(data, alpha)
    return {
        'chart_type': result.chart_type,
        'data': result.data.tolist(),
        'cl': result.cl,
        'ucl': result.ucl,
        'lcl': result.lcl,
        'violations': result.violations,
        'statistics': result.statistics
    }


if __name__ == '__main__':
    import json
    
    # 测试数据
    np.random.seed(42)
    data = np.random.normal(10, 0.1, 50)
    
    # 测试各控制图
    print("Testing CUSUM...")
    print(json.dumps(run_cusum(data, 10.0, 0.1), indent=2))
    
    print("\nTesting EWMA...")
    print(json.dumps(run_ewma(data, 10.0, 0.1), indent=2))
    
    print("\nTesting I-MR...")
    print(json.dumps(run_imr(data), indent=2))
    
    print("\nTesting MAMR...")
    print(json.dumps(run_mamr(data, 5), indent=2))
    
    # 测试 Hotelling T2 (二维数据)
    print("\nTesting Hotelling T2...")
    data_2d = np.random.normal(10, 0.1, (50, 3))
    print(json.dumps(run_hotelling_t2(data_2d), indent=2))