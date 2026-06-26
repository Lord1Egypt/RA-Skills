#!/usr/bin/env python3
"""
DOE 响应曲面方法 (Response Surface Methodology)
包含: CCD (Central Composite Design), Box-Behnken
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import json


@dataclass
class RSMResult:
    """响应曲面分析结果"""
    design_type: str
    design_matrix: np.ndarray
    coefficients: Dict[str, float]
    anova_table: Dict
    optimization: Dict
    response_surface: Dict


class CentralCompositeDesign:
    """
    中心复合设计 (CCD)
    用于建立响应曲面模型
    """
    
    def __init__(self, n_factors: int, alpha: float = None, face: str = 'circumscribed'):
        """
        初始化 CCD
        
        参数:
            n_factors: 因子数量
            alpha: 星号点距离 (默认 sqrt(2^n_factors))
            face: 立方体面类型: 'circumscribed', 'inscribed', 'faced'
        """
        self.n_factors = n_factors
        self.face = face
        
        # 计算 alpha
        if alpha is None:
            self.alpha = 2 ** (n_factors / 4)  # 默认值
        else:
            self.alpha = alpha
        
    def generate(self, levels: List[Tuple[float, float]] = None) -> np.ndarray:
        """
        生成 CCD 设计矩阵
        
        参数:
            levels: 各因子水平 [(low, high), ...]
        """
        n = self.n_factors
        
        if levels is None:
            # 默认水平 -1, 0, +1
            levels = [(-1, 1)] * n
        
        design = []
        
        # 1. 立方体点 (2^n 全因子)
        for i in range(2 ** n):
            point = []
            for j in range(n):
                bit = (i >> (n - 1 - j)) & 1
                point.append(levels[j][1] if bit else levels[j][0])
            design.append(point)
        
        n_cube = len(design)
        
        # 2. 中心点
        center_point = [0] * n
        design.append(center_point)
        
        # 添加更多中心点 (用于估计纯二次误差)
        for _ in range(n + 1):
            design.append(center_point)
        
        # 3. 星号点 (轴点)
        for j in range(n):
            for sign in [-1, 1]:
                point = [0] * n
                point[j] = sign * self.alpha
                design.append(point)
        
        return np.array(design)
    
    def analyze(self, responses: List[float]) -> RSMResult:
        """分析响应曲面数据"""
        n = self.n_factors
        design = self.generate()
        
        # 构建回归矩阵 (包含线性、二次、交互项)
        X = np.ones((len(design), 1))
        
        # 线性项
        for j in range(n):
            X = np.column_stack((X, design[:, j]))
        
        # 交互项
        for i in range(n):
            for k in range(i + 1, n):
                X = np.column_stack((X, design[:, i] * design[:, k]))
        
        # 二次项
        for j in range(n):
            X = np.column_stack((X, design[:, j] ** 2))
        
        # 最小二乘拟合
        y = np.array(responses)
        try:
            beta = np.linalg.lstsq(X, y, rcond=None)[0]
        except:
            beta = np.zeros(X.shape[1])
        
        # 计算系数
        coefficient_names = ['Intercept']
        for j in range(n):
            coefficient_names.append(f'x{j+1}')
        for i in range(n):
            for k in range(i + 1, n):
                coefficient_names.append(f'x{i+1}x{k+1}')
        for j in range(n):
            coefficient_names.append(f'x{j+1}^2')
        
        coefficients = dict(zip(coefficient_names, beta))
        
        # 计算 R²
        y_pred = X @ beta
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
        
        # ANOVA
        df_model = len(beta) - 1
        df_error = len(y) - len(beta)
        ms_model = ss_res / df_model if df_model > 0 else 0
        ms_error = ss_res / df_error if df_error > 0 else 0
        f_value = ms_model / ms_error if ms_error > 0 else 0
        
        anova = {
            'SS_Regression': ss_res,
            'SS_Total': ss_tot,
            'R_squared': r_squared,
            'F_value': f_value,
            'df_model': df_model,
            'df_error': df_error
        }
        
        # 寻找最优解 (梯度下降)
        optimization = self._optimize(coefficients)
        
        return RSMResult(
            design_type='CCD',
            design_matrix=design,
            coefficients=coefficients,
            anova_table=anova,
            optimization=optimization,
            response_surface={'equation': 'y = b0 + b1*x1 + ... + b12*x1*x2 + ...'}
        )
    
    def _optimize(self, coefficients: Dict) -> Dict:
        """简单优化 (梯度下降)"""
        n = self.n_factors
        best_x = [0] * n
        best_y = float('inf')
        
        # 网格搜索
        for x1 in np.linspace(-2, 2, 20):
            for x2 in np.linspace(-2, 2, 20):
                if n >= 2:
                    y = coefficients.get('Intercept', 0)
                    y += coefficients.get('x1', 0) * x1
                    y += coefficients.get('x2', 0) * x2
                    if n >= 2:
                        y += coefficients.get('x1x2', 0) * x1 * x2
                    y += coefficients.get('x1^2', 0) * x1 ** 2
                    y += coefficients.get('x2^2', 0) * x2 ** 2
                    
                    if y < best_y:
                        best_y = y
                        best_x = [x1, x2]
        
        return {'optimal_x': best_x, 'optimal_y': best_y}


class BoxBehnkenDesign:
    """
    Box-Behnken 设计
    适合因子数量 3-7 的响应曲面
    """
    
    def __init__(self, n_factors: int):
        self.n_factors = n_factors
        
    def generate(self, levels: List[Tuple[float, float]] = None) -> np.ndarray:
        """生成 Box-Behnken 设计矩阵"""
        n = self.n_factors
        
        if levels is None:
            levels = [(-1, 1)] * n
        
        design = []
        
        # 对每个因子组合
        for i in range(n):
            for j in range(i + 1, n):
                # 4 种组合: (+1,+1), (+1,-1), (-1,+1), (-1,-1)
                for combo in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                    point = [0] * n
                    point[i] = combo[0]
                    point[j] = combo[1]
                    design.append(point)
        
        # 添加中心点
        center = [0] * n
        for _ in range(n):
            design.append(center)
        
        return np.array(design)
    
    def analyze(self, responses: List[float]) -> RSMResult:
        """分析 Box-Behnken 数据"""
        design = self.generate()
        n = self.n_factors
        
        # 构建回归矩阵
        X = np.ones((len(design), 1))
        for j in range(n):
            X = np.column_stack((X, design[:, j]))
        for i in range(n):
            for k in range(i + 1, n):
                X = np.column_stack((X, design[:, i] * design[:, k]))
        for j in range(n):
            X = np.column_stack((X, design[:, j] ** 2))
        
        y = np.array(responses)
        
        try:
            beta = np.linalg.lstsq(X, y, rcond=None)[0]
        except:
            beta = np.zeros(X.shape[1])
        
        y_pred = X @ beta
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
        
        coefficient_names = ['Intercept'] + [f'x{i+1}' for i in range(n)] + \
                            [f'x{i+1}x{k+1}' for i in range(n) for k in range(i+1, n)] + \
                            [f'x{i+1}^2' for i in range(n)]
        
        return RSMResult(
            design_type='Box-Behnken',
            design_matrix=design,
            coefficients=dict(zip(coefficient_names, beta)),
            anova_table={'R_squared': r_squared},
            optimization={},
            response_surface={'equation': 'y = b0 + b1*x1 + ...'}
        )


# Taguchi 正交表
class TaguchiOrthogonalArray:
    """
    Taguchi 正交表
    """
    
    ARRAYS = {
        # L4 (2^3)
        4: {'factors': 3, 'runs': 4, 'levels': 2},
        # L8 (2^7)
        8: {'factors': 7, 'runs': 8, 'levels': 2},
        # L9 (3^4)
        9: {'factors': 4, 'runs': 9, 'levels': 3},
        # L12 (2^11)
        12: {'factors': 11, 'runs': 12, 'levels': 2},
        # L16 (2^15)
        16: {'factors': 15, 'runs': 16, 'levels': 2},
        # L18 (2^1 × 3^7)
        18: {'factors': 8, 'runs': 18, 'levels': [2, 3]},
        # L27 (3^13)
        27: {'factors': 13, 'runs': 27, 'levels': 3},
    }
    
    # L8 正交表
    L8 = np.array([
        [1,1,1,1,1,1,1],
        [1,1,1,2,2,2,2],
        [1,2,2,1,1,2,2],
        [1,2,2,2,2,1,1],
        [2,1,2,1,2,1,2],
        [2,1,2,2,1,2,1],
        [2,2,1,1,2,2,1],
        [2,2,1,2,1,1,2],
    ])
    
    # L9 正交表
    L9 = np.array([
        [1,1,1,1],
        [1,2,2,2],
        [1,3,3,3],
        [2,1,2,3],
        [2,2,3,1],
        [2,3,1,2],
        [3,1,3,2],
        [3,2,1,3],
        [3,3,2,1],
    ])
    
    @classmethod
    def get_array(cls, runs: int) -> np.ndarray:
        """获取 Taguchi 正交表"""
        if runs == 8:
            return cls.L8
        elif runs == 9:
            return cls.L9
        else:
            # 返回默认 L8
            return cls.L8
    
    @classmethod
    def analyze(cls, responses: List[float], n_factors: int) -> Dict:
        """分析 Taguchi 实验数据"""
        array = cls.get_array(len(responses))
        n_factors = min(n_factors, array.shape[1])
        
        # 计算各因子各水平的均值
        factor_effects = {}
        for j in range(n_factors):
            levels = {}
            for level in [1, 2]:
                mask = array[:, j] == level
                levels[level] = np.mean(np.array(responses)[mask])
            factor_effects[f'Factor{j+1}'] = levels
        
        # 计算 S/N 比 (望目特性)
        sn_ratios = []
        for response in responses:
            sn = 10 * np.log10(response ** 2)
            sn_ratios.append(sn)
        
        return {
            'runs': len(responses),
            'factors': n_factors,
            'factor_effects': factor_effects,
            'sn_ratio': np.mean(sn_ratios),
            'mean_response': np.mean(responses)
        }


# 主函数接口
def run_ccd(n_factors: int, responses: List[float], levels: List[Tuple[float, float]] = None) -> Dict:
    """运行 CCD 分析"""
    ccd = CentralCompositeDesign(n_factors)
    design = ccd.generate(levels)
    # 确保响应数量与设计点数匹配
    n_runs = len(design)
    if len(responses) > n_runs:
        responses = responses[:n_runs]
    elif len(responses) < n_runs:
        # 填充
        responses = responses + [np.mean(responses)] * (n_runs - len(responses))
    result = ccd.analyze(responses)
    return {
        'design_type': result.design_type,
        'design_matrix': result.design_matrix.tolist(),
        'coefficients': result.coefficients,
        'anova': result.anova_table,
        'optimization': result.optimization
    }


def run_box_behnken(n_factors: int, responses: List[float]) -> Dict:
    """运行 Box-Behnken 分析"""
    bb = BoxBehnkenDesign(n_factors)
    design = bb.generate()
    n_runs = len(design)
    if len(responses) > n_runs:
        responses = responses[:n_runs]
    elif len(responses) < n_runs:
        responses = responses + [np.mean(responses)] * (n_runs - len(responses))
    result = bb.analyze(responses)
    return {
        'design_type': result.design_type,
        'design_matrix': result.design_matrix.tolist(),
        'coefficients': result.coefficients,
        'anova': result.anova_table
    }


def run_taguchi(runs: int, responses: List[float], n_factors: int) -> Dict:
    """运行 Taguchi 分析"""
    return TaguchiOrthogonalArray.analyze(responses, n_factors)


if __name__ == '__main__':
    import json
    
    # 测试 CCD
    print("=== CCD Test ===")
    np.random.seed(42)
    responses_ccd = [45 + np.random.normal(0, 2) for _ in range(15)]
    ccd_result = run_ccd(2, responses_ccd)
    print(f"Design: {ccd_result['design_type']}, R²: {ccd_result['anova']['R_squared']:.3f}")
    
    # 测试 Box-Behnken
    print("\n=== Box-Behnken Test ===")
    responses_bb = [50 + np.random.normal(0, 1) for _ in range(13)]
    bb_result = run_box_behnken(3, responses_bb)
    print(f"Design: {bb_result['design_type']}")
    
    # 测试 Taguchi
    print("\n=== Taguchi Test ===")
    responses_tag = [45, 52, 48, 58, 46, 53, 49, 59]
    tag_result = run_taguchi(8, responses_tag, 3)
    print(f"S/N Ratio: {tag_result['sn_ratio']:.2f}")
    print(f"Mean Response: {tag_result['mean_response']:.2f}")