#!/usr/bin/env python3
"""
SPC统计过程控制分析脚本

支持的控制图类型：
- xbarr: Xbar-R图（均值-极差图）
- xbars: Xbar-S图（均值-标准差图）
- imr: I-MR图（单值-移动极差图）
- p: P图（不合格品率图）
- c: C图（缺陷数图）
- u: U图（单位缺陷数图）
"""

import argparse
import sys
import numpy as np
import pandas as pd
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import json


class SPCAnalyzer:
    """SPC统计过程控制分析器"""
    
    def __init__(self):
        self.chart_type = None
        self.data = None
        self.stats = {}
        self.nelson_results = {}
    
    def load_data(self, input_file: str, sheet_name: Optional[str] = None) -> pd.DataFrame:
        """加载数据"""
        try:
            if sheet_name:
                df = pd.read_excel(input_file, sheet_name=sheet_name)
            else:
                df = pd.read_excel(input_file)
            
            # 删除空行
            df = df.dropna(how='all')
            
            return df
        except Exception as e:
            raise ValueError(f"数据加载失败: {str(e)}")
    
    def validate_data(self, data: pd.DataFrame, chart_type: str) -> Tuple[bool, str]:
        """验证数据格式是否符合控制图类型要求"""
        if data.empty:
            return False, "数据为空"
        
        # 根据控制图类型验证数据格式
        if chart_type in ['xbarr', 'xbars']:
            # Xbar-R和Xbar-S需要多列数据（每列是一个子组）
            if len(data.columns) < 2:
                return False, f"{chart_type}图需要至少2列数据（每列代表一个子组的观测值）"
            # 检查是否为数值型
            for col in data.columns:
                if not pd.api.types.is_numeric_dtype(data[col]):
                    return False, f"列 '{col}' 不是数值型数据"
        
        elif chart_type == 'imr':
            # I-MR图需要单列数据
            if len(data.columns) != 1:
                return False, "I-MR图需要单列数据"
            if not pd.api.types.is_numeric_dtype(data.iloc[:, 0]):
                return False, "数据必须是数值型"
        
        elif chart_type == 'p':
            # P图需要2列：检验数量和不合格数量
            if len(data.columns) != 2:
                return False, "P图需要2列数据：检验数量和不合格数量"
            if not all(pd.api.types.is_numeric_dtype(data[col]) for col in data.columns):
                return False, "所有列必须是数值型数据"
        
        elif chart_type == 'c':
            # C图需要单列数据（缺陷数）
            if len(data.columns) != 1:
                return False, "C图需要单列数据（缺陷数）"
            if not pd.api.types.is_numeric_dtype(data.iloc[:, 0]):
                return False, "数据必须是数值型"
        
        elif chart_type == 'u':
            # U图需要2列：样本量和缺陷数
            if len(data.columns) != 2:
                return False, "U图需要2列数据：样本量和缺陷数"
            if not all(pd.api.types.is_numeric_dtype(data[col]) for col in data.columns):
                return False, "所有列必须是数值型数据"
        
        else:
            return False, f"不支持的控制图类型: {chart_type}"
        
        return True, "数据格式验证通过"
    
    def calculate_xbarr(self, data: pd.DataFrame) -> Dict:
        """计算Xbar-R图的统计指标"""
        # 计算每个子组的均值和极差
        data = data.dropna()
        subgroup_means = data.mean(axis=1)
        subgroup_ranges = data.max(axis=1) - data.min(axis=1)
        
        n = len(data.columns)  # 子组大小
        k = len(data)  # 子组数量
        
        # 计算总体均值和平均极差
        X_double_bar = subgroup_means.mean()
        R_bar = subgroup_ranges.mean()
        
        # 计算控制限（使用标准常数）
        # A2, D3, D4常数查表
        constants = {
            2: {'A2': 1.880, 'D3': 0.000, 'D4': 3.267},
            3: {'A2': 1.023, 'D3': 0.000, 'D4': 2.574},
            4: {'A2': 0.729, 'D3': 0.000, 'D4': 2.282},
            5: {'A2': 0.577, 'D3': 0.000, 'D4': 2.114},
            6: {'A2': 0.483, 'D3': 0.000, 'D4': 2.004},
            7: {'A2': 0.419, 'D3': 0.076, 'D4': 1.924},
            8: {'A2': 0.373, 'D3': 0.136, 'D4': 1.864},
            9: {'A2': 0.337, 'D3': 0.184, 'D4': 1.816},
            10: {'A2': 0.308, 'D3': 0.223, 'D4': 1.777}
        }
        
        const = constants.get(n, constants[10])
        
        # X图控制限
        UCL_x = X_double_bar + const['A2'] * R_bar
        LCL_x = X_double_bar - const['A2'] * R_bar
        CL_x = X_double_bar
        
        # R图控制限
        UCL_r = const['D4'] * R_bar
        LCL_r = const['D3'] * R_bar
        CL_r = R_bar
        
        return {
            'chart_type': 'Xbar-R',
            'data': data,
            'subgroup_means': subgroup_means,
            'subgroup_ranges': subgroup_ranges,
            'stats': {
                'n': n,
                'k': k,
                'X_double_bar': X_double_bar,
                'R_bar': R_bar
            },
            'limits': {
                'x_chart': {'UCL': UCL_x, 'CL': CL_x, 'LCL': LCL_x},
                'r_chart': {'UCL': UCL_r, 'CL': CL_r, 'LCL': LCL_r}
            }
        }
    
    def calculate_xbars(self, data: pd.DataFrame) -> Dict:
        """计算Xbar-S图的统计指标"""
        data = data.dropna()
        subgroup_means = data.mean(axis=1)
        subgroup_stds = data.std(axis=1, ddof=1)
        
        n = len(data.columns)
        k = len(data)
        
        X_double_bar = subgroup_means.mean()
        S_bar = subgroup_stds.mean()
        
        # A3, B3, B4常数
        constants = {
            2: {'A3': 2.659, 'B3': 0.000, 'B4': 3.267},
            3: {'A3': 1.954, 'B3': 0.000, 'B4': 2.568},
            4: {'A3': 1.628, 'B3': 0.000, 'B4': 2.266},
            5: {'A3': 1.427, 'B3': 0.000, 'B4': 2.089},
            6: {'A3': 1.287, 'B3': 0.030, 'B4': 1.970},
            7: {'A3': 1.182, 'B3': 0.118, 'B4': 1.882},
            8: {'A3': 1.099, 'B3': 0.185, 'B4': 1.815},
            9: {'A3': 1.032, 'B3': 0.239, 'B4': 1.761},
            10: {'A3': 0.975, 'B3': 0.284, 'B4': 1.716}
        }
        
        const = constants.get(n, constants[10])
        
        # X图控制限
        UCL_x = X_double_bar + const['A3'] * S_bar
        LCL_x = X_double_bar - const['A3'] * S_bar
        CL_x = X_double_bar
        
        # S图控制限
        UCL_s = const['B4'] * S_bar
        LCL_s = const['B3'] * S_bar
        CL_s = S_bar
        
        return {
            'chart_type': 'Xbar-S',
            'data': data,
            'subgroup_means': subgroup_means,
            'subgroup_stds': subgroup_stds,
            'stats': {
                'n': n,
                'k': k,
                'X_double_bar': X_double_bar,
                'S_bar': S_bar
            },
            'limits': {
                'x_chart': {'UCL': UCL_x, 'CL': CL_x, 'LCL': LCL_x},
                's_chart': {'UCL': UCL_s, 'CL': CL_s, 'LCL': LCL_s}
            }
        }
    
    def calculate_imr(self, data: pd.DataFrame) -> Dict:
        """计算I-MR图的统计指标"""
        data = data.dropna()
        individual_values = data.iloc[:, 0]
        
        # 计算移动极差
        moving_ranges = abs(individual_values.diff().dropna())
        
        k = len(individual_values)
        X_bar = individual_values.mean()
        MR_bar = moving_ranges.mean()
        
        # 常数
        d2 = 1.128  # n=2时的d2值
        D3 = 0.000
        D4 = 3.267
        
        # I图控制限
        UCL_i = X_bar + 3 * (MR_bar / d2)
        LCL_i = X_bar - 3 * (MR_bar / d2)
        CL_i = X_bar
        
        # MR图控制限
        UCL_mr = D4 * MR_bar
        LCL_mr = D3 * MR_bar
        CL_mr = MR_bar
        
        return {
            'chart_type': 'I-MR',
            'data': data,
            'individual_values': individual_values,
            'moving_ranges': moving_ranges,
            'stats': {
                'k': k,
                'X_bar': X_bar,
                'MR_bar': MR_bar
            },
            'limits': {
                'i_chart': {'UCL': UCL_i, 'CL': CL_i, 'LCL': LCL_i},
                'mr_chart': {'UCL': UCL_mr, 'CL': CL_mr, 'LCL': LCL_mr}
            }
        }
    
    def calculate_p_chart(self, data: pd.DataFrame) -> Dict:
        """计算P图的统计指标"""
        data = data.dropna()
        inspection = data.iloc[:, 0].values
        defectives = data.iloc[:, 1].values
        
        # 计算不合格品率
        p = defectives / inspection
        
        total_inspections = inspection.sum()
        total_defectives = defectives.sum()
        p_bar = total_defectives / total_inspections
        
        k = len(data)
        
        # P图控制限（可能每个样本不同）
        UCL_list = p_bar + 3 * np.sqrt(p_bar * (1 - p_bar) / inspection)
        LCL_list = p_bar - 3 * np.sqrt(p_bar * (1 - p_bar) / inspection)
        # 确保LCL不小于0
        LCL_list = np.maximum(LCL_list, 0)
        
        return {
            'chart_type': 'P',
            'data': data,
            'p_values': p,
            'stats': {
                'k': k,
                'p_bar': p_bar,
                'total_inspections': total_inspections,
                'total_defectives': total_defectives
            },
            'limits': {
                'UCL_list': UCL_list,
                'CL': p_bar,
                'LCL_list': LCL_list
            }
        }
    
    def calculate_c_chart(self, data: pd.DataFrame) -> Dict:
        """计算C图的统计指标"""
        data = data.dropna()
        defects = data.iloc[:, 0].values
        
        c_bar = defects.mean()
        k = len(data)
        
        # C图控制限
        UCL = c_bar + 3 * np.sqrt(c_bar)
        LCL = c_bar - 3 * np.sqrt(c_bar)
        LCL = max(0, LCL)  # 确保不小于0
        CL = c_bar
        
        return {
            'chart_type': 'C',
            'data': data,
            'defects': defects,
            'stats': {
                'k': k,
                'c_bar': c_bar
            },
            'limits': {
                'UCL': UCL,
                'CL': CL,
                'LCL': LCL
            }
        }
    
    def calculate_u_chart(self, data: pd.DataFrame) -> Dict:
        """计算U图的统计指标"""
        data = data.dropna()
        sample_sizes = data.iloc[:, 0].values
        defects = data.iloc[:, 1].values
        
        # 计算单位缺陷数
        u = defects / sample_sizes
        
        total_defects = defects.sum()
        total_samples = sample_sizes.sum()
        u_bar = total_defects / total_samples
        
        k = len(data)
        
        # U图控制限（可能每个样本不同）
        UCL_list = u_bar + 3 * np.sqrt(u_bar / sample_sizes)
        LCL_list = u_bar - 3 * np.sqrt(u_bar / sample_sizes)
        LCL_list = np.maximum(LCL_list, 0)
        
        return {
            'chart_type': 'U',
            'data': data,
            'u_values': u,
            'stats': {
                'k': k,
                'u_bar': u_bar,
                'total_defects': total_defects,
                'total_samples': total_samples
            },
            'limits': {
                'UCL_list': UCL_list,
                'CL': u_bar,
                'LCL_list': LCL_list
            }
        }
    
    def check_nelson_rules(self, data_series: np.ndarray, UCL: float, LCL: float, CL: float) -> Dict:
        """
        执行Nelson 8条规则检测
        
        Nelson规则：
        1. 1个点超出3σ控制限
        2. 连续9个点落在中心线同一侧
        3. 连续6个点持续递增或递减
        4. 连续14个点交替上下
        5. 连续3个点中有2个点落在2σ区域之外（中心线同一侧）
        6. 连续5个点中有4个点落在1σ区域之外（中心线同一侧）
        7. 连续15个点落在1σ区域之内
        8. 连续8个点落在1σ区域之外（中心线同一侧）
        """
        violations = []
        
        # 计算标准差
        sigma = (UCL - LCL) / 6
        
        # 规则1：1个点超出3σ控制限
        for i, val in enumerate(data_series):
            if val > UCL or val < LCL:
                violations.append({
                    'rule': 1,
                    'description': '点超出3σ控制限',
                    'index': i,
                    'value': val,
                    'type': 'above' if val > UCL else 'below'
                })
        
        # 规则2：连续9个点落在中心线同一侧
        for i in range(len(data_series) - 8):
            window = data_series[i:i+9]
            if all(x > CL for x in window):
                violations.append({
                    'rule': 2,
                    'description': '连续9个点落在中心线上方',
                    'index': i,
                    'end_index': i+8,
                    'type': 'above'
                })
            elif all(x < CL for x in window):
                violations.append({
                    'rule': 2,
                    'description': '连续9个点落在中心线下方',
                    'index': i,
                    'end_index': i+8,
                    'type': 'below'
                })
        
        # 规则3：连续6个点持续递增或递减
        for i in range(len(data_series) - 5):
            window = data_series[i:i+6]
            if all(window[j] < window[j+1] for j in range(5)):
                violations.append({
                    'rule': 3,
                    'description': '连续6个点持续递增',
                    'index': i,
                    'end_index': i+5,
                    'type': 'increasing'
                })
            elif all(window[j] > window[j+1] for j in range(5)):
                violations.append({
                    'rule': 3,
                    'description': '连续6个点持续递减',
                    'index': i,
                    'end_index': i+5,
                    'type': 'decreasing'
                })
        
        # 规则4：连续14个点交替上下
        for i in range(len(data_series) - 13):
            window = data_series[i:i+14]
            alternations = 0
            for j in range(13):
                if (window[j] > CL and window[j+1] < CL) or (window[j] < CL and window[j+1] > CL):
                    alternations += 1
            if alternations >= 13:  # 全部交替
                violations.append({
                    'rule': 4,
                    'description': '连续14个点交替上下',
                    'index': i,
                    'end_index': i+13,
                    'type': 'alternating'
                })
        
        # 规则5：连续3个点中有2个点落在2σ区域之外（中心线同一侧）
        for i in range(len(data_series) - 2):
            window = data_series[i:i+3]
            above_2sigma = sum(1 for x in window if x > CL + 2*sigma)
            below_2sigma = sum(1 for x in window if x < CL - 2*sigma)
            if above_2sigma >= 2:
                violations.append({
                    'rule': 5,
                    'description': '连续3个点中有2个点落在2σ区域之上',
                    'index': i,
                    'end_index': i+2,
                    'type': 'above_2sigma'
                })
            elif below_2sigma >= 2:
                violations.append({
                    'rule': 5,
                    'description': '连续3个点中有2个点落在2σ区域之下',
                    'index': i,
                    'end_index': i+2,
                    'type': 'below_2sigma'
                })
        
        # 规则6：连续5个点中有4个点落在1σ区域之外（中心线同一侧）
        for i in range(len(data_series) - 4):
            window = data_series[i:i+5]
            above_1sigma = sum(1 for x in window if x > CL + sigma)
            below_1sigma = sum(1 for x in window if x < CL - sigma)
            if above_1sigma >= 4:
                violations.append({
                    'rule': 6,
                    'description': '连续5个点中有4个点落在1σ区域之上',
                    'index': i,
                    'end_index': i+4,
                    'type': 'above_1sigma'
                })
            elif below_1sigma >= 4:
                violations.append({
                    'rule': 6,
                    'description': '连续5个点中有4个点落在1σ区域之下',
                    'index': i,
                    'end_index': i+4,
                    'type': 'below_1sigma'
                })
        
        # 规则7：连续15个点落在1σ区域之内
        for i in range(len(data_series) - 14):
            window = data_series[i:i+15]
            within_1sigma = sum(1 for x in window if CL - sigma <= x <= CL + sigma)
            if within_1sigma == 15:
                violations.append({
                    'rule': 7,
                    'description': '连续15个点落在1σ区域之内（分层化）',
                    'index': i,
                    'end_index': i+14,
                    'type': 'within_1sigma'
                })
        
        # 规则8：连续8个点落在1σ区域之外（中心线同一侧）
        for i in range(len(data_series) - 7):
            window = data_series[i:i+8]
            above_1sigma_outside = sum(1 for x in window if x > CL + sigma)
            below_1sigma_outside = sum(1 for x in window if x < CL - sigma)
            if above_1sigma_outside == 8:
                violations.append({
                    'rule': 8,
                    'description': '连续8个点落在1σ区域之上（混合）',
                    'index': i,
                    'end_index': i+7,
                    'type': 'above_outside_1sigma'
                })
            elif below_1sigma_outside == 8:
                violations.append({
                    'rule': 8,
                    'description': '连续8个点落在1σ区域之下（混合）',
                    'index': i,
                    'end_index': i+7,
                    'type': 'below_outside_1sigma'
                })
        
        return {
            'violations': violations,
            'violation_count': len(violations),
            'rules_broken': sorted(list(set(v['rule'] for v in violations)))
        }
    
    def calculate_process_capability(self, data: np.ndarray, USL: float, LSL: float) -> Dict:
        """计算过程能力指数"""
        mean = np.mean(data)
        std = np.std(data, ddof=1)
        
        # Cp
        Cp = (USL - LSL) / (6 * std)
        
        # Cpk
        Cpu = (USL - mean) / (3 * std)
        Cpl = (mean - LSL) / (3 * std)
        Cpk = min(Cpu, Cpl)
        
        # Pp, Ppk（使用整体标准差）
        Pp = Cp
        Ppk = Cpk
        
        return {
            'mean': mean,
            'std': std,
            'USL': USL,
            'LSL': LSL,
            'Cp': Cp,
            'Cpk': Cpk,
            'Pp': Pp,
            'Ppk': Ppk,
            'Cpu': Cpu,
            'Cpl': Cpl
        }
    
    def generate_svg_chart(self, result: Dict, title: str = "SPC Control Chart", chart_subtype: str = "main") -> str:
        """
        生成SVG控制图
        
        参数:
            result: 分析结果字典
            title: 图表标题
            chart_subtype: 图表子类型
                - "main": 主图（Xbar-R图的X图）
                - "secondary": 副图（Xbar-R图的R图，Xbar-S图的S图，I-MR图的MR图）
        """
        chart_type = result['chart_type']
        
        # 根据控制图类型确定要绘制的数据
        if chart_type == 'Xbar-R':
            data_series = result['subgroup_means']
            limits = result['limits']['x_chart']
            chart_title = f"{title} - Xbar Chart"
        elif chart_type == 'Xbar-S':
            data_series = result['subgroup_means']
            limits = result['limits']['x_chart']
            chart_title = f"{title} - Xbar Chart"
        elif chart_type == 'I-MR':
            data_series = result['individual_values']
            limits = result['limits']['i_chart']
            chart_title = f"{title} - I Chart"
        elif chart_type == 'P':
            data_series = result['p_values']
            limits = {'UCL': result['limits']['UCL_list'], 'CL': result['limits']['CL'], 'LCL': result['limits']['LCL_list']}
            chart_title = f"{title} - P Chart"
        elif chart_type == 'C':
            data_series = result['defects']
            limits = result['limits']
            chart_title = f"{title} - C Chart"
        elif chart_type == 'U':
            data_series = result['u_values']
            limits = {'UCL': result['limits']['UCL_list'], 'CL': result['limits']['CL'], 'LCL': result['limits']['LCL_list']}
            chart_title = f"{title} - U Chart"
        
        # 图表尺寸
        width = 800
        height = 400
        padding = 60
        
        # 计算Y轴范围
        y_min = min(np.min(data_series), limits.get('LCL', 0) if isinstance(limits.get('LCL'), (int, float)) else np.min(limits.get('LCL_list', data_series))) - 1
        y_max = max(np.max(data_series), limits.get('UCL', 0) if isinstance(limits.get('UCL'), (int, float)) else np.max(limits.get('UCL_list', data_series))) + 1
        y_range = y_max - y_min
        
        # 数据点转换为坐标
        points = []
        n = len(data_series)
        for i, val in enumerate(data_series):
            x = padding + (i / (n - 1)) * (width - 2 * padding)
            y = height - padding - ((val - y_min) / y_range) * (height - 2 * padding)
            points.append((x, y))
        
        # 控制限转换为坐标
        def to_y(val):
            return height - padding - ((val - y_min) / y_range) * (height - 2 * padding)
        
        # 生成路径数据
        path_data = f"M {points[0][0]} {points[0][1]}"
        for x, y in points[1:]:
            path_data += f" L {x} {y}"
        
        # 生成数据点圆圈
        circles = ""
        outliers_info = []
        
        # 获取UCL、LCL和CL（可能是列表或单个值）
        # 注意：对于固定控制限（Xbar-R图等），UCL和LCL是单个值
        # 对于变动控制限（P图、U图），UCL和LCL是列表
        is_variable_limits = isinstance(limits.get('UCL'), (list, np.ndarray))
        CL = limits['CL']
        
        if is_variable_limits:
            UCL_values = limits['UCL']
            LCL_values = limits['LCL']
        else:
            UCL_values = limits['UCL']
            LCL_values = limits['LCL']
        
        for i, (x, y) in enumerate(points):
            val = data_series[i]
            ucl = UCL_values[i] if is_variable_limits else UCL_values
            lcl = LCL_values[i] if is_variable_limits else LCL_values
            
            is_outlier = (val > ucl) or (val < lcl)
            color = "orange" if is_outlier else "blue"
            r = 6 if is_outlier else 4
            
            circles += f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}" stroke="blue" stroke-width="1"/>'
            
            if is_outlier:
                outliers_info.append(f'<text x="{x-25}" y="{y-10}" font-size="12" fill="red">{val:.2f}</text>')
        
        outliers_text = "".join(outliers_info)
        
        # 生成Y轴刻度
        y_ticks = ""
        for i in range(11):
            val = y_min + i * y_range / 10
            y_pos = height - padding - i * (height - 2 * padding) / 10
            y_ticks += f'<line x1="{padding-5}" y1="{y_pos}" x2="{padding}" y2="{y_pos}" stroke="black" stroke-width="1"/>'
            y_ticks += f'<text x="{padding-10}" y="{y_pos+4}" font-size="11" text-anchor="end" font-family="Arial">{val:.1f}</text>'
        
        # 生成X轴刻度
        x_ticks = ""
        for i in range(0, n, max(1, n // 10)):
            x_pos = padding + i * (width - 2 * padding) / (n - 1)
            x_ticks += f'<line x1="{x_pos}" y1="{height-padding}" x2="{x_pos}" y2="{height-padding+5}" stroke="black" stroke-width="1"/>'
            x_ticks += f'<text x="{x_pos}" y="{height-padding+20}" font-size="11" text-anchor="middle" font-family="Arial">{i+1}</text>'
        
        # 生成网格线
        grid_lines = ""
        for i in range(11):
            y_pos = height - padding - i * (height - 2 * padding) / 10
            grid_lines += f'<line x1="{padding}" y1="{y_pos}" x2="{width-padding}" y2="{y_pos}" stroke="#e0e0e0" stroke-width="1"/>'
        
        # 生成控制限线条
        control_lines = ""
        
        # UCL
        if isinstance(UCL_values, (list, np.ndarray)):
            # 多条控制限（对于P图和U图）
            for i in range(n):
                x_pos = padding + i * (width - 2 * padding) / (n - 1)
                y_pos = to_y(UCL_values[i])
                if i == 0:
                    control_lines += f'<path d="M {x_pos} {y_pos}" stroke="red" stroke-width="2" stroke-dasharray="5,5" fill="none"'
                else:
                    control_lines += f' L {x_pos} {y_pos}'
            control_lines += '"/>'
        else:
            y_ucl = to_y(UCL_values)
            control_lines += f'<line x1="{padding}" y1="{y_ucl}" x2="{width-padding}" y2="{y_ucl}" stroke="red" stroke-width="2" stroke-dasharray="5,5"/>'
        
        # LCL
        if isinstance(LCL_values, (list, np.ndarray)):
            for i in range(n):
                x_pos = padding + i * (width - 2 * padding) / (n - 1)
                y_pos = to_y(LCL_values[i])
                if i == 0:
                    control_lines += f'<path d="M {x_pos} {y_pos}" stroke="red" stroke-width="2" stroke-dasharray="5,5" fill="none"'
                else:
                    control_lines += f' L {x_pos} {y_pos}'
            control_lines += '"/>'
        else:
            y_lcl = to_y(LCL_values)
            control_lines += f'<line x1="{padding}" y1="{y_lcl}" x2="{width-padding}" y2="{y_lcl}" stroke="red" stroke-width="2" stroke-dasharray="5,5"/>'
        
        # CL
        y_cl = to_y(CL)
        control_lines += f'<line x1="{padding}" y1="{y_cl}" x2="{width-padding}" y2="{y_cl}" stroke="green" stroke-width="2" stroke-dasharray="5,5"/>'
        
        # 控制限标签
        if is_variable_limits:
            ucl_label = f"{np.mean(UCL_values):.2f} (变动)"
            lcl_label = f"{np.mean(LCL_values):.2f} (变动)"
            y_ucl_label = to_y(np.mean(UCL_values))
            y_lcl_label = to_y(np.mean(LCL_values))
        else:
            ucl_label = f"{UCL_values:.2f}"
            lcl_label = f"{LCL_values:.2f}"
            y_ucl_label = to_y(UCL_values)
            y_lcl_label = to_y(LCL_values)
        
        control_labels = f"""
            <text x="{width-padding}" y="{y_ucl_label-5}" font-size="12" fill="red" text-anchor="end" font-family="Arial">UCL = {ucl_label}</text>
            <text x="{width-padding}" y="{y_cl-5}" font-size="12" fill="green" text-anchor="end" font-family="Arial">CL = {CL:.2f}</text>
            <text x="{width-padding}" y="{y_lcl_label-5}" font-size="12" fill="red" text-anchor="end" font-family="Arial">LCL = {lcl_label}</text>
        """
        
        # 生成SVG
        svg = f"""
        <svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
            <!-- 背景 -->
            <rect x="0" y="0" width="{width}" height="{height}" fill="white"/>
            
            <!-- 网格线 -->
            {grid_lines}
            
            <!-- Y轴刻度 -->
            {y_ticks}
            
            <!-- X轴刻度 -->
            {x_ticks}
            
            <!-- 坐标轴 -->
            <line x1="{padding}" y1="{padding}" x2="{padding}" y2="{height-padding}" stroke="black" stroke-width="2"/>
            <line x1="{padding}" y1="{height-padding}" x2="{width-padding}" y2="{height-padding}" stroke="black" stroke-width="2"/>
            
            <!-- 控制限 -->
            {control_lines}
            
            <!-- 控制限标签 -->
            {control_labels}
            
            <!-- 数据路径 -->
            <path d="{path_data}" fill="none" stroke="blue" stroke-width="1.5"/>
            
            <!-- 数据点 -->
            {circles}
            
            <!-- 异常点标注 -->
            {outliers_text}
            
            <!-- 坐标轴标签 -->
            <text x="{width/2}" y="{height-10}" font-size="14" text-anchor="middle" font-family="Arial">样本序号</text>
            <text x="15" y="{height/2}" font-size="14" text-anchor="middle" font-family="Arial" transform="rotate(-90, 15, {height/2})">测量值</text>
        </svg>
        """
        
        return svg
    
    def generate_html_report(self, result: Dict, output_file: str, nelson_results: Optional[Dict] = None,
                             process_capability: Optional[Dict] = None) -> str:
        """生成HTML报告"""
        chart_type = result['chart_type']
        stats = result['stats']
        limits = result['limits']
        
        # 生成控制图（可能需要生成多张）
        svg_charts = []
        
        if chart_type in ['Xbar-R', 'Xbar-S']:
            # 生成两张图：X图和R图/S图
            chart_subtype = 'Xbar' if chart_type == 'Xbar-R' else 'Xbar'
            
            # 第一张图：X图（均值图）
            result_xbar = {
                'chart_type': chart_type,
                'data': result['data'],
                'subgroup_means': result['subgroup_means'],
                'limits': {'UCL': limits['x_chart']['UCL'], 'CL': limits['x_chart']['CL'], 'LCL': limits['x_chart']['LCL']}
            }
            svg_xbar = self.generate_svg_chart(result_xbar, title=f"{chart_type} - Xbar Chart")
            svg_charts.append({
                'title': f"{chart_type} 控制图 - Xbar图（均值图）",
                'svg': svg_xbar
            })
            
            # 第二张图：R图/S图（波动图）
            chart_subtype = 'R' if chart_type == 'Xbar-R' else 'S'
            result_r = {
                'chart_type': chart_type,
                'limits': {'UCL': limits[f'{chart_subtype.lower()}_chart']['UCL'], 
                          'CL': limits[f'{chart_subtype.lower()}_chart']['CL'], 
                          'LCL': limits[f'{chart_subtype.lower()}_chart']['LCL']}
            }
            if chart_type == 'Xbar-R':
                result_r['subgroup_ranges'] = result['subgroup_ranges']
            else:
                result_r['subgroup_stds'] = result['subgroup_stds']
            
            # 重新计算数据系列
            if chart_type == 'Xbar-R':
                data_series = result['subgroup_ranges']
            else:
                data_series = result['subgroup_stds']
            
            result_r['data'] = pd.DataFrame({'value': data_series})
            svg_r = self.generate_svg_chart(result_r, title=f"{chart_type} - {chart_subtype} Chart")
            svg_charts.append({
                'title': f"{chart_type} 控制图 - {chart_subtype}图（波动图）",
                'svg': svg_r
            })
            
        elif chart_type == 'I-MR':
            # 生成两张图：I图和MR图
            # 第一张图：I图（单值图）
            result_i = {
                'chart_type': chart_type,
                'individual_values': result['individual_values'],
                'limits': {'UCL': limits['i_chart']['UCL'], 'CL': limits['i_chart']['CL'], 'LCL': limits['i_chart']['LCL']}
            }
            svg_i = self.generate_svg_chart(result_i, title="I-MR - I Chart")
            svg_charts.append({
                'title': "I-MR 控制图 - I图（单值图）",
                'svg': svg_i
            })
            
            # 第二张图：MR图（移动极差图）
            result_mr = {
                'chart_type': chart_type,
                'moving_ranges': result['moving_ranges'],
                'limits': {'UCL': limits['mr_chart']['UCL'], 'CL': limits['mr_chart']['CL'], 'LCL': limits['mr_chart']['LCL']}
            }
            result_mr['data'] = pd.DataFrame({'value': result['moving_ranges']})
            svg_mr = self.generate_svg_chart(result_mr, title="I-MR - MR Chart")
            svg_charts.append({
                'title': "I-MR 控制图 - MR图（移动极差图）",
                'svg': svg_mr
            })
            
        else:
            # 只生成一张图：P图、C图、U图
            svg_chart = self.generate_svg_chart(result)
            svg_charts.append({
                'title': f"{chart_type} 控制图",
                'svg': svg_chart
            })
        
        # 获取Nelson规则结果
        nelson_info = ""
        if nelson_results and nelson_results['violation_count'] > 0:
            violations_table = ""
            for v in nelson_results['violations']:
                violations_table += f"""
                    <tr>
                        <td>规则 {v['rule']}</td>
                        <td>{v['description']}</td>
                        <td>{v.get('index', 'N/A')}</td>
                    </tr>
                """
            
            nelson_info = f"""
                <div class="section">
                    <h3>Nelson规则检测结果</h3>
                    <p><strong>违规数量：</strong>{nelson_results['violation_count']}</p>
                    <p><strong>触发的规则：</strong>{', '.join(map(str, nelson_results['rules_broken']))}</p>
                    
                    <table>
                        <thead>
                            <tr>
                                <th>规则</th>
                                <th>描述</th>
                                <th>位置</th>
                            </tr>
                        </thead>
                        <tbody>
                            {violations_table}
                        </tbody>
                    </table>
                </div>
            """
        elif nelson_results:
            nelson_info = """
                <div class="section">
                    <h3>Nelson规则检测结果</h3>
                    <p class="success">未检测到违规，过程处于统计控制状态。</p>
                </div>
            """
        
        # 获取过程能力分析结果
        capability_info = ""
        if process_capability:
            capability_info = f"""
                <div class="section">
                    <h3>过程能力分析</h3>
                    <table>
                        <tr>
                            <td><strong>均值：</strong></td>
                            <td>{process_capability['mean']:.4f}</td>
                        </tr>
                        <tr>
                            <td><strong>标准差：</strong></td>
                            <td>{process_capability['std']:.4f}</td>
                        </tr>
                        <tr>
                            <td><strong>USL：</strong></td>
                            <td>{process_capability['USL']:.4f}</td>
                        </tr>
                        <tr>
                            <td><strong>LSL：</strong></td>
                            <td>{process_capability['LSL']:.4f}</td>
                        </tr>
                        <tr>
                            <td><strong>Cp：</strong></td>
                            <td>{process_capability['Cp']:.4f}</td>
                        </tr>
                        <tr>
                            <td><strong>Cpk：</strong></td>
                            <td>{process_capability['Cpk']:.4f}</td>
                        </tr>
                        <tr>
                            <td><strong>Pp：</strong></td>
                            <td>{process_capability['Pp']:.4f}</td>
                        </tr>
                        <tr>
                            <td><strong>Ppk：</strong></td>
                            <td>{process_capability['Ppk']:.4f}</td>
                        </tr>
                    </table>
                    
                    <p><strong>过程能力评价：</strong></p>
                    <ul>
                        <li>Cp ≥ 1.33：过程能力充足</li>
                        <li>1.00 ≤ Cp < 1.33：过程能力尚可，需要改进</li>
                        <li>Cp < 1.00：过程能力不足，需要采取措施</li>
                    </ul>
                </div>
            """
        
        # 生成HTML
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SPC分析报告 - {chart_type}</title>
    <style>
        body {{
            font-family: Arial, "Microsoft YaHei", sans-serif;
            margin: 20px;
            line-height: 1.6;
            color: #333;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            border-bottom: 2px solid #bdc3c7;
            padding-bottom: 8px;
            margin-top: 30px;
        }}
        h3 {{
            color: #7f8c8d;
            margin-top: 20px;
        }}
        .header {{
            margin-bottom: 30px;
        }}
        .chart-container {{
            border: 1px solid #ddd;
            padding: 20px;
            margin: 20px 0;
            background: #f9f9f9;
            border-radius: 5px;
        }}
        .section {{
            margin: 20px 0;
            padding: 15px;
            background: #fff;
            border-left: 4px solid #3498db;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
        }}
        th, td {{
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #3498db;
            color: white;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .success {{
            color: #27ae60;
            font-weight: bold;
        }}
        .warning {{
            color: #e67e22;
            font-weight: bold;
        }}
        .danger {{
            color: #e74c3c;
            font-weight: bold;
        }}
        .info {{
            background: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #7f8c8d;
            font-size: 14px;
        }}
        ul {{
            margin: 10px 0;
            padding-left: 20px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>SPC统计过程控制分析报告</h1>
        <p><strong>控制图类型：</strong>{chart_type}</p>
        <p><strong>生成时间：</strong>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="section">
        <h2>控制图</h2>
        <div class="chart-container">
            {svg_chart}
        </div>
    </div>
    
    <div class="section">
        <h2>统计信息</h2>
        <table>
            <tbody>
                {self._generate_stats_rows(stats)}
            </tbody>
        </table>
    </div>
    
    <div class="section">
        <h2>控制限</h2>
        <table>
            <tbody>
                {self._generate_limits_rows(limits)}
            </tbody>
        </table>
    </div>
    
    {nelson_info}
    {capability_info}
    
    <div class="footer">
        <p>本报告由SPC分析工具自动生成 | 仅供内部参考</p>
    </div>
</body>
</html>
"""
        
        # 保存HTML文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return html
    
    def _generate_stats_rows(self, stats: Dict) -> str:
        """生成统计信息表格行"""
        rows = ""
        for key, value in stats.items():
            if isinstance(value, (int, float)):
                rows += f'<tr><td><strong>{key}：</strong></td><td>{value:.4f}</td></tr>'
            else:
                rows += f'<tr><td><strong>{key}：</strong></td><td>{value}</td></tr>'
        return rows
    
    def _generate_limits_rows(self, limits: Dict) -> str:
        """生成控制限表格行"""
        rows = ""
        for key, value in limits.items():
            if isinstance(value, dict):
                rows += f'<tr><td colspan="2"><strong>{key}：</strong></td></tr>'
                for sub_key, sub_value in value.items():
                    if isinstance(sub_value, (int, float)):
                        rows += f'<tr><td style="padding-left: 30px;">{sub_key}：</td><td>{sub_value:.4f}</td></tr>'
                    else:
                        rows += f'<tr><td style="padding-left: 30px;">{sub_key}：</td><td>{str(sub_value)[:50]}</td></tr>'
            else:
                # 处理列表类型的控制限（P图和U图）
                if isinstance(value, (list, np.ndarray)):
                    rows += f'<tr><td><strong>{key}：</strong></td><td>变动范围: [{np.min(value):.4f}, {np.max(value):.4f}]</td></tr>'
                elif isinstance(value, (int, float)):
                    rows += f'<tr><td><strong>{key}：</strong></td><td>{value:.4f}</td></tr>'
                else:
                    rows += f'<tr><td><strong>{key}：</strong></td><td>{value}</td></tr>'
        return rows


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='SPC统计过程控制分析')
    parser.add_argument('--input', required=True, help='输入数据文件路径（Excel格式）')
    parser.add_argument('--chart-type', required=True, choices=['xbarr', 'xbars', 'imr', 'p', 'c', 'u'],
                        help='控制图类型')
    parser.add_argument('--output', required=False, help='输出HTML报告文件路径（可选，默认按日期自动生成）')
    parser.add_argument('--sheet-name', help='Excel工作表名称（可选）')
    parser.add_argument('--usl', type=float, help='规格上限（可选，用于过程能力分析）')
    parser.add_argument('--lsl', type=float, help='规格下限（可选，用于过程能力分析）')
    parser.add_argument('--summary', action='store_true', help='仅输出摘要信息到stdout')
    
    args = parser.parse_args()
    
    # 如果用户没有提供输出路径，自动生成带日期的文件名
    if not args.output:
        from datetime import datetime
        current_time = datetime.now()
        date_str = current_time.strftime('%Y%m%d_%H%M%S')
        args.output = f"spc_analysis_report_{date_str}.html"
        print(f"自动生成报告文件名: {args.output}")
    else:
        # 如果用户提供了输出路径，检查是否包含日期格式
        # 如果不包含，在文件名前添加日期
        import os
        file_dir = os.path.dirname(args.output)
        file_name = os.path.basename(args.output)
        name, ext = os.path.splitext(file_name)
        
        # 检查文件名是否已包含日期（YYYYMMDD格式）
        has_date = any(c.isdigit() for c in name) and len(name) >= 8
        if not has_date:
            from datetime import datetime
            current_time = datetime.now()
            date_str = current_time.strftime('%Y%m%d')
            new_name = f"{name}_{date_str}{ext}"
            args.output = os.path.join(file_dir, new_name) if file_dir else new_name
            print(f"添加日期前缀: {args.output}")
    
    # 创建分析器
    analyzer = SPCAnalyzer()
    
    # 加载数据
    print(f"正在加载数据: {args.input}")
    data = analyzer.load_data(args.input, args.sheet_name)
    print(f"数据加载成功，形状: {data.shape}")
    
    # 验证数据
    print(f"正在验证数据格式...")
    is_valid, message = analyzer.validate_data(data, args.chart_type)
    if not is_valid:
        print(f"错误: {message}")
        sys.exit(1)
    print(f"数据验证通过: {message}")
    
    # 执行分析
    print(f"正在执行{args.chart_type}控制图分析...")
    analyzer.chart_type = args.chart_type
    
    # 根据控制图类型选择分析方法
    if args.chart_type == 'xbarr':
        result = analyzer.calculate_xbarr(data)
    elif args.chart_type == 'xbars':
        result = analyzer.calculate_xbars(data)
    elif args.chart_type == 'imr':
        result = analyzer.calculate_imr(data)
    elif args.chart_type == 'p':
        result = analyzer.calculate_p_chart(data)
    elif args.chart_type == 'c':
        result = analyzer.calculate_c_chart(data)
    elif args.chart_type == 'u':
        result = analyzer.calculate_u_chart(data)
    
    print(f"分析完成")
    
    # 执行Nelson规则检测
    print("正在执行Nelson规则检测...")
    
    # 获取数据系列和控制限
    if args.chart_type in ['xbarr', 'xbars']:
        data_series = result['subgroup_means'].values
        limits = result['limits']['x_chart']
    elif args.chart_type == 'imr':
        data_series = result['individual_values'].values
        limits = result['limits']['i_chart']
    elif args.chart_type == 'p':
        data_series = result['p_values'] if hasattr(result['p_values'], 'values') else result['p_values']
        # P图的UCL和LCL是列表，使用均值作为检测基准
        CL = result['limits']['CL']
        sigma = np.sqrt(CL * (1 - CL) / result['stats']['total_inspections'])
        UCL = CL + 3 * sigma
        LCL = CL - 3 * sigma
        # 重新构建limits字典用于Nelson检测
        limits = {'UCL': UCL, 'LCL': LCL, 'CL': CL}
    elif args.chart_type == 'u':
        data_series = result['u_values'] if hasattr(result['u_values'], 'values') else result['u_values']
        CL = result['limits']['CL']
        sigma = np.sqrt(CL / result['stats']['total_samples'])
        UCL = CL + 3 * sigma
        LCL = CL - 3 * sigma
        limits = {'UCL': UCL, 'LCL': LCL, 'CL': CL}
    else:  # c图
        data_series = result['defects']
        limits = result['limits']
    
    # 获取UCL和LCL
    UCL = limits['UCL']
    LCL = limits['LCL']
    CL = limits['CL']
    
    nelson_results = analyzer.check_nelson_rules(data_series, UCL, LCL, CL)
    print(f"Nelson规则检测完成，发现{nelson_results['violation_count']}个违规")
    
    # 过程能力分析（如果提供了规格限）
    process_capability = None
    if args.usl is not None and args.lsl is not None:
        print("正在计算过程能力指数...")
        # 获取原始数据
        if args.chart_type in ['xbarr', 'xbars']:
            # 对于Xbar图，使用所有子组的所有数据
            all_data = result['data'].values.flatten()
        elif args.chart_type == 'imr':
            all_data = result['individual_values'].values
        else:
            print("警告: 该控制图类型不支持过程能力分析")
        
        if args.chart_type in ['xbarr', 'xbars', 'imr']:
            process_capability = analyzer.calculate_process_capability(all_data, args.usl, args.lsl)
            print(f"过程能力分析完成: Cp={process_capability['Cp']:.4f}, Cpk={process_capability['Cpk']:.4f}")
    
    # 生成HTML报告
    print(f"正在生成HTML报告: {args.output}")
    html = analyzer.generate_html_report(result, args.output, nelson_results, process_capability)
    print(f"HTML报告生成成功")
    
    # 输出摘要
    if args.summary:
        print("\n" + "="*50)
        print("分析摘要")
        print("="*50)
        print(f"控制图类型: {result['chart_type']}")
        print(f"样本量: {result['stats']['k']}")
        
        if args.chart_type in ['xbarr', 'xbars']:
            print(f"子组大小: {result['stats']['n']}")
            print(f"均值: {result['stats']['X_double_bar']:.4f}")
        elif args.chart_type == 'imr':
            print(f"均值: {result['stats']['X_bar']:.4f}")
        elif args.chart_type == 'p':
            print(f"平均不合格品率: {result['stats']['p_bar']:.4f}")
        elif args.chart_type == 'c':
            print(f"平均缺陷数: {result['stats']['c_bar']:.4f}")
        elif args.chart_type == 'u':
            print(f"平均单位缺陷数: {result['stats']['u_bar']:.4f}")
        
        print(f"\nNelson规则违规: {nelson_results['violation_count']}个")
        if nelson_results['violation_count'] > 0:
            print(f"触发的规则: {', '.join(map(str, nelson_results['rules_broken']))}")
        
        if process_capability:
            print(f"\n过程能力: Cp={process_capability['Cp']:.4f}, Cpk={process_capability['Cpk']:.4f}")
        
        print("="*50)
    
    print("\n分析完成！")


if __name__ == '__main__':
    main()
