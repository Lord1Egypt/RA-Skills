#!/usr/bin/env python3
"""
属性控制图模块
包含: p Chart, np Chart, c Chart, u Chart, Z Chart
"""

import numpy as np
from typing import Dict, List, Optional
from dataclasses import dataclass
import io


@dataclass
class AttributeChartResult:
    """属性控制图结果"""
    chart_type: str
    data: np.ndarray
    cl: float
    ucl: float
    lcl: float
    violations: List[int]
    statistics: Dict


class PChart:
    """
    p Chart (不合格品率控制图)
    用于监控不合格品率，样本量可以不同
    """
    
    def __init__(self):
        pass
        
    def calculate(self, defectives: np.ndarray, sample_sizes: np.ndarray) -> AttributeChartResult:
        """
        计算 p 控制图
        
        参数:
            defectives: 不合格品数量数组
            sample_sizes: 样本大小数组
        """
        n = len(defectives)
        
        # 计算各样本的不合格品率
        p_values = defectives / sample_sizes
        
        # 平均不合格品率 (p-bar)
        total_defectives = np.sum(defectives)
        total_samples = np.sum(sample_sizes)
        p_bar = total_defectives / total_samples
        
        # 控制限 (每个样本可能不同)
        ucl = np.zeros(n)
        lcl = np.zeros(n)
        
        for i in range(n):
            if sample_sizes[i] > 0:
                sigma_p = np.sqrt(p_bar * (1 - p_bar) / sample_sizes[i])
                ucl[i] = p_bar + 3 * sigma_p
                lcl[i] = max(0, p_bar - 3 * sigma_p)
            else:
                ucl[i] = 1.0
                lcl[i] = 0.0
        
        # 检测违规点
        violations = []
        for i in range(n):
            if p_values[i] > ucl[i] or p_values[i] < lcl[i]:
                violations.append(i)
        
        return AttributeChartResult(
            chart_type='p',
            data=p_values,
            cl=p_bar,
            ucl=np.mean(ucl),
            lcl=max(0, np.mean(lcl)),
            violations=violations,
            statistics={
                'p_bar': p_bar,
                'total_defectives': total_defectives,
                'total_samples': total_samples,
                'avg_sample_size': np.mean(sample_sizes)
            }
        )


class NPChart:
    """
    np Chart (不合格品数控制图)
    用于监控不合格品数，样本量必须相同
    """
    
    def __init__(self):
        pass
        
    def calculate(self, defectives: np.ndarray, sample_size: int) -> AttributeChartResult:
        """
        计算 np 控制图
        
        参数:
            defectives: 不合格品数量数组
            sample_size: 固定样本大小
        """
        n = len(defectives)
        
        # 平均不合格品数
        np_bar = np.mean(defectives)
        
        # 标准差
        sigma_np = np.sqrt(np_bar * (1 - np_bar / sample_size))
        
        # 控制限
        ucl = np_bar + 3 * sigma_np
        lcl = max(0, np_bar - 3 * sigma_np)
        
        # 检测违规点
        violations = [i for i in range(n) if defectives[i] > ucl or defectives[i] < lcl]
        
        return AttributeChartResult(
            chart_type='np',
            data=defectives,
            cl=np_bar,
            ucl=ucl,
            lcl=lcl,
            violations=violations,
            statistics={
                'np_bar': np_bar,
                'sample_size': sample_size,
                'sigma': sigma_np
            }
        )


class CChart:
    """
    c Chart (缺陷数控制图)
    用于监控固定检测区域的缺陷数
    """
    
    def __init__(self):
        pass
        
    def calculate(self, defects: np.ndarray) -> AttributeChartResult:
        """
        计算 c 控制图
        
        参数:
            defects: 缺陷数数组
        """
        n = len(defects)
        
        # 平均缺陷数 (c-bar)
        c_bar = np.mean(defects)
        
        # 控制限
        ucl = c_bar + 3 * np.sqrt(c_bar)
        lcl = max(0, c_bar - 3 * np.sqrt(c_bar))
        
        # 检测违规点
        violations = [i for i in range(n) if defects[i] > ucl or defects[i] < lcl]
        
        return AttributeChartResult(
            chart_type='c',
            data=defects,
            cl=c_bar,
            ucl=ucl,
            lcl=lcl,
            violations=violations,
            statistics={
                'c_bar': c_bar,
                'sigma': np.sqrt(c_bar)
            }
        )


class UChart:
    """
    u Chart (单位缺陷数控制图)
    用于监控单位产品的缺陷数，检测区域大小可以不同
    """
    
    def __init__(self):
        pass
        
    def calculate(self, defects: np.ndarray, inspection_units: np.ndarray) -> AttributeChartResult:
        """
        计算 u 控制图
        
        参数:
            defects: 缺陷数数组
            inspection_units: 检测单位数数组
        """
        n = len(defects)
        
        # 计算单位缺陷数
        u_values = defects / inspection_units
        
        # 平均单位缺陷数 (u-bar)
        total_defects = np.sum(defects)
        total_units = np.sum(inspection_units)
        u_bar = total_defects / total_units
        
        # 控制限 (每个点可能不同)
        ucl = np.zeros(n)
        lcl = np.zeros(n)
        
        for i in range(n):
            if inspection_units[i] > 0:
                sigma_u = np.sqrt(u_bar / inspection_units[i])
                ucl[i] = u_bar + 3 * sigma_u
                lcl[i] = max(0, u_bar - 3 * sigma_u)
            else:
                ucl[i] = u_bar
                lcl[i] = u_bar
        
        # 检测违规点
        violations = []
        for i in range(n):
            if u_values[i] > ucl[i] or u_values[i] < lcl[i]:
                violations.append(i)
        
        return AttributeChartResult(
            chart_type='u',
            data=u_values,
            cl=u_bar,
            ucl=np.mean(ucl),
            lcl=max(0, np.mean(lcl)),
            violations=violations,
            statistics={
                'u_bar': u_bar,
                'total_defects': total_defects,
                'total_units': total_units
            }
        )


class ZChart:
    """
    Z Chart (标准化得分控制图)
    将任何连续数据标准化到 Z 分数进行监控
    """
    
    def __init__(self):
        pass
        
    def calculate(self, data: np.ndarray, target: float = 0, sigma: float = 1) -> AttributeChartResult:
        """
        计算 Z 控制图
        
        参数:
            data: 数据数组
            target: 目标值 (默认 0)
            sigma: 标准差 (默认 1)
        """
        n = len(data)
        
        # 计算 Z 分数
        z_values = (data - target) / sigma
        
        # 控制限
        ucl = 3
        lcl = -3
        
        # 警告限
        uwl = 2
        lwl = -2
        
        # 检测违规点
        violations = [i for i in range(n) if abs(z_values[i]) > 3]
        
        warnings = [i for i in range(n) if 2 < abs(z_values[i]) <= 3]
        
        return AttributeChartResult(
            chart_type='Z',
            data=z_values,
            cl=0,
            ucl=ucl,
            lcl=lcl,
            violations=violations,
            statistics={
                'target': target,
                'sigma': sigma,
                'mean_data': np.mean(data),
                'std_data': np.std(data),
                'warnings': warnings
            }
        )


# 主函数接口

def run_p_chart(defectives: List[int], sample_sizes: List[int]) -> Dict:
    """运行 p 控制图"""
    chart = PChart()
    result = chart.calculate(np.array(defectives), np.array(sample_sizes))
    return {
        'chart_type': result.chart_type,
        'data': result.data.tolist(),
        'cl': result.cl,
        'ucl': result.ucl,
        'lcl': result.lcl,
        'violations': result.violations,
        'statistics': result.statistics
    }


def run_np_chart(defectives: List[int], sample_size: int) -> Dict:
    """运行 np 控制图"""
    chart = NPChart()
    result = chart.calculate(np.array(defectives), sample_size)
    return {
        'chart_type': result.chart_type,
        'data': result.data.tolist(),
        'cl': result.cl,
        'ucl': result.ucl,
        'lcl': result.lcl,
        'violations': result.violations,
        'statistics': result.statistics
    }


def run_c_chart(defects: List[int]) -> Dict:
    """运行 c 控制图"""
    chart = CChart()
    result = chart.calculate(np.array(defects))
    return {
        'chart_type': result.chart_type,
        'data': result.data.tolist(),
        'cl': result.cl,
        'ucl': result.ucl,
        'lcl': result.lcl,
        'violations': result.violations,
        'statistics': result.statistics
    }


def run_u_chart(defects: List[int], inspection_units: List[float]) -> Dict:
    """运行 u 控制图"""
    chart = UChart()
    result = chart.calculate(np.array(defects), np.array(inspection_units))
    return {
        'chart_type': result.chart_type,
        'data': result.data.tolist(),
        'cl': result.cl,
        'ucl': result.ucl,
        'lcl': result.lcl,
        'violations': result.violations,
        'statistics': result.statistics
    }


def run_z_chart(data: List[float], target: float = 0, sigma: float = 1) -> Dict:
    """运行 Z 控制图"""
    chart = ZChart()
    result = chart.calculate(np.array(data), target, sigma)
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
    import numpy as np
    
    # Custom JSON encoder for numpy types
    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, np.integer):
                return int(obj)
            if isinstance(obj, np.floating):
                return float(obj)
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return super().default(obj)
    
    # 测试 p Chart
    print("Testing p Chart...")
    print(json.dumps(run_p_chart([5, 3, 7, 4, 6], [100, 100, 100, 100, 100]), indent=2, cls=NumpyEncoder))
    
    # 测试 np Chart
    print("\nTesting np Chart...")
    print(json.dumps(run_np_chart([5, 3, 7, 4, 6], 100), indent=2, cls=NumpyEncoder))
    
    # 测试 c Chart
    print("\nTesting c Chart...")
    print(json.dumps(run_c_chart([12, 15, 8, 10, 14]), indent=2, cls=NumpyEncoder))
    
    # 测试 u Chart
    print("\nTesting u Chart...")
    print(json.dumps(run_u_chart([12, 15, 8, 10, 14], [10, 10, 10, 10, 10]), indent=2, cls=NumpyEncoder))
    
    # 测试 Z Chart
    print("\nTesting Z Chart...")
    np.random.seed(42)
    data = np.random.normal(10, 0.1, 20)
    print(json.dumps(run_z_chart(data.tolist(), 10.0, 0.1), indent=2))