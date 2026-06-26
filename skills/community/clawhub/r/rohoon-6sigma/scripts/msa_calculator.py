"""
MSA (Measurement System Analysis) 统计计算核心模块
遵循 AIAG VDA MSA 第四版标准
"""

import numpy as np
from scipy import stats
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


@dataclass
class GRRError:
    """GR&R 误差分量"""
    ev: float  # 设备变差 (Equipment Variation) - 重复性
    av: float  # 评价人变差 (Appraiser Variation) - 再现性
    rr: float  # GR&R (重复性 + 再现性)
    pv: float  # 零件变差 (Part Variation)
    tv: float  # 总变差 (Total Variation)


@dataclass
class GRREvaluation:
    """GR&R 评估结果"""
    ndc: int  # 分级数 (Number of Distinct Categories)
    percent_grr: float  # %GR&R (占总变差的百分比)
    percent_ev: float  # %EV
    percent_av: float  # %AV
    percent_pv: float  # %PV
    acceptance: str  # Acceptable, Marginal, Unacceptable
    is_acceptable: bool


@dataclass
class BiasAnalysis:
    """偏倚分析结果"""
    bias: float  # 偏倚（观测均值 - 参考值）
    bias_percent: float  # 偏倚百分比
    t_statistic: float
    p_value: float
    is_significant: bool  # 偏倚是否显著（p < 0.05）
    confidence_interval: Tuple[float, float]  # 95% 置信区间


@dataclass
class LinearityAnalysis:
    """线性分析结果"""
    slope: float  # 斜率
    intercept: float  # 截距
    r_squared: float  # 决定系数
    p_value_slope: float  # 斜率显著性
    p_value_intercept: float  # 截距显著性
    is_linear: bool  # 是否线性（斜率不显著）
    linearity: float  # 线性度 = |slope| * process_variation
    linearity_percent: float  # 线性度百分比


# ==================== GR&R 分析 (ANOVA 法) ====================

def calculate_grr_anova(
    data: np.ndarray,
    n_parts: int,
    n_operators: int,
    n_trials: int,
    tolerance: Optional[float] = None,
    process_variation: Optional[float] = None
) -> Tuple[GRRError, GRREvaluation]:
    """
    使用方差分析法 (ANOVA) 计算 GR&R
    
    参数:
        data: 三维数组，shape=(parts, operators, trials)
        n_parts: 零件数量
        n_operators: 操作者数量
        n_trials: 试验次数
        tolerance: 公差 (USL - LSL)，用于计算%Tolerance
        process_variation: 过程变差（6*sigma），用于计算%Process Variation
    
    返回:
        (GRRError, GRREvaluation)
    """
    # 验证数据形状
    if data.shape != (n_parts, n_operators, n_trials):
        raise ValueError(f"数据形状不匹配：期望 {(n_parts, n_operators, n_trials)}, 实际 {data.shape}")
    
    # 计算各种均值
    grand_mean = np.mean(data)
    
    # 零件均值
    part_means = np.mean(data, axis=(1, 2))
    
    # 操作者均值
    operator_means = np.mean(data, axis=(0, 2))
    
    # 每个零件 - 操作者组合的均值
    cell_means = np.mean(data, axis=2)
    
    # 平方和计算
    # 总平方和
    ss_total = np.sum((data - grand_mean) ** 2)
    
    # 零件平方和
    ss_parts = n_operators * n_trials * np.sum((part_means - grand_mean) ** 2)
    
    # 操作者平方和
    ss_operators = n_parts * n_trials * np.sum((operator_means - grand_mean) ** 2)
    
    # 交互作用平方和
    ss_interaction = n_trials * np.sum((cell_means - part_means[:, np.newaxis] - operator_means[np.newaxis, :] + grand_mean) ** 2)
    
    # 误差平方和（重复性）
    ss_error = ss_total - ss_parts - ss_operators - ss_interaction
    
    # 自由度
    df_parts = n_parts - 1
    df_operators = n_operators - 1
    df_interaction = df_parts * df_operators
    df_error = n_parts * n_operators * (n_trials - 1)
    df_total = n_parts * n_operators * n_trials - 1
    
    # 均方
    ms_parts = ss_parts / df_parts if df_parts > 0 else 0
    ms_operators = ss_operators / df_operators if df_operators > 0 else 0
    ms_interaction = ss_interaction / df_interaction if df_interaction > 0 else 0
    ms_error = ss_error / df_error if df_error > 0 else 0
    
    # 方差分量计算
    # 重复性 (EV)
    var_ev = ms_error
    
    # 再现性 (AV) - 包含操作者和交互作用
    if ms_interaction > ms_error:
        var_operators = (ms_operators - ms_interaction) / (n_parts * n_trials)
        var_interaction = (ms_interaction - ms_error) / n_trials
    else:
        var_operators = (ms_operators - ms_error) / (n_parts * n_trials)
        var_interaction = 0
    
    var_operators = max(0, var_operators)
    var_interaction = max(0, var_interaction)
    
    var_av = var_operators + var_interaction
    
    # GR&R 方差
    var_grr = var_ev + var_av
    
    # 零件变差 (PV)
    if ms_parts > ms_error:
        var_pv = (ms_parts - ms_error) / (n_operators * n_trials)
    else:
        var_pv = 0
    var_pv = max(0, var_pv)
    
    # 总变差
    var_tv = var_grr + var_pv
    
    # 标准差（乘以 5.15 对应 99% 置信区间，或使用 6 对应 99.73%）
    k = 6.0  # 使用 6σ
    
    ev = k * np.sqrt(var_ev)
    av = k * np.sqrt(var_av)
    rr = k * np.sqrt(var_grr)
    pv = k * np.sqrt(var_pv)
    tv = k * np.sqrt(var_tv)
    
    grr_error = GRRError(ev=ev, av=av, rr=rr, pv=pv, tv=tv)
    
    # 评估
    # 分级数 NDC
    ndc = int(np.floor(1.41 * (pv / rr))) if rr > 0 else 999
    ndc = max(0, ndc)
    
    # %GR&R
    percent_grr = (rr / tv) * 100 if tv > 0 else 0
    percent_ev = (ev / tv) * 100 if tv > 0 else 0
    percent_av = (av / tv) * 100 if tv > 0 else 0
    percent_pv = (pv / tv) * 100 if tv > 0 else 0
    
    # 接受准则 (AIAG MSA)
    if percent_grr <= 10:
        acceptance = "Acceptable"
        is_acceptable = True
    elif percent_grr <= 30:
        acceptance = "Marginal"
        is_acceptable = True  # 有条件接受
    else:
        acceptance = "Unacceptable"
        is_acceptable = False
    
    evaluation = GRREvaluation(
        ndc=ndc,
        percent_grr=percent_grr,
        percent_ev=percent_ev,
        percent_av=percent_av,
        percent_pv=percent_pv,
        acceptance=acceptance,
        is_acceptable=is_acceptable
    )
    
    logger.info(
        f"GR&R 分析完成：%GR&R={percent_grr:.2f}%, NDC={ndc}, "
        f"评估={acceptance}"
    )
    
    return grr_error, evaluation


def calculate_grr_xbar_r(
    data: np.ndarray,
    n_parts: int,
    n_operators: int,
    n_trials: int,
    tolerance: Optional[float] = None
) -> Tuple[GRRError, GRREvaluation]:
    """
    使用 Xbar-R 法计算 GR&R（简化方法）
    
    参数:
        data: 三维数组，shape=(parts, operators, trials)
    """
    # 计算每个操作者 - 零件组合的极差
    ranges = np.ptp(data, axis=2)  # 每个 cell 的极差
    
    # 平均极差
    r_bar = np.mean(ranges)
    
    # 操作者均值
    operator_means = np.mean(data, axis=(0, 2))
    operator_range = np.ptp(operator_means)
    
    # 零件均值
    part_means = np.mean(data, axis=(1, 2))
    part_range = np.ptp(part_means)
    
    # 控制图系数
    d2_star = {
        (2, 2): 1.41, (2, 3): 1.91, (2, 4): 2.24,
        (3, 2): 1.28, (3, 3): 1.81, (3, 4): 2.16,
        (4, 3): 1.75, (4, 4): 2.12,
        (5, 3): 1.72, (5, 4): 2.10,
    }
    
    key = (n_operators, n_trials)
    d2 = d2_star.get(key, 1.128)  # 默认 n=2
    
    # 重复性 (EV)
    ev = (5.15 * r_bar) / d2
    
    # 再现性 (AV)
    d2_star_op = {2: 1.41, 3: 1.91, 4: 2.24, 5: 2.48}
    d2_op = d2_star_op.get(n_operators, 1.41)
    
    k1 = 5.15 / d2
    k2 = 5.15 / (d2_op * np.sqrt(n_parts * n_trials))
    
    av = np.sqrt((k2 * operator_range) ** 2 - (ev ** 2) / (n_parts * n_trials))
    av = max(0, av)
    
    # GR&R
    rr = np.sqrt(ev ** 2 + av ** 2)
    
    # 零件变差 (PV)
    d2_pv = d2_star_op.get(n_parts, 2.48)
    k3 = 5.15 / d2_pv
    pv = k3 * part_range
    
    # 总变差
    tv = np.sqrt(rr ** 2 + pv ** 2)
    
    grr_error = GRRError(ev=ev, av=av, rr=rr, pv=pv, tv=tv)
    
    # 评估
    ndc = int(np.floor(1.41 * (pv / rr))) if rr > 0 else 999
    percent_grr = (rr / tv) * 100 if tv > 0 else 0
    
    if percent_grr <= 10:
        acceptance = "Acceptable"
        is_acceptable = True
    elif percent_grr <= 30:
        acceptance = "Marginal"
        is_acceptable = True
    else:
        acceptance = "Unacceptable"
        is_acceptable = False
    
    evaluation = GRREvaluation(
        ndc=ndc,
        percent_grr=percent_grr,
        percent_ev=(ev / tv) * 100 if tv > 0 else 0,
        percent_av=(av / tv) * 100 if tv > 0 else 0,
        percent_pv=(pv / tv) * 100 if tv > 0 else 0,
        acceptance=acceptance,
        is_acceptable=is_acceptable
    )
    
    return grr_error, evaluation


# ==================== 偏倚分析 ====================

def calculate_bias(
    measurements: np.ndarray,
    reference_value: float,
    confidence_level: float = 0.95
) -> BiasAnalysis:
    """
    计算偏倚
    
    参数:
        measurements: 测量值数组
        reference_value: 参考值（标准值）
        confidence_level: 置信水平
    
    返回:
        BiasAnalysis
    """
    n = len(measurements)
    
    if n < 2:
        raise ValueError("至少需要 2 个测量值")
    
    # 观测均值
    x_bar = np.mean(measurements)
    
    # 偏倚
    bias = x_bar - reference_value
    
    # 偏倚百分比（相对于过程变差或公差）
    # 这里先计算绝对偏倚
    bias_percent = 0  # 需要过程变差或公差才能计算
    
    # 标准差
    s = np.std(measurements, ddof=1)
    
    # 标准误差
    se = s / np.sqrt(n)
    
    # t 统计量
    t_stat = bias / se if se > 0 else 0
    
    # p 值（双尾检验）
    p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df=n-1))
    
    # 显著性
    is_significant = p_value < (1 - confidence_level)
    
    # 置信区间
    alpha = 1 - confidence_level
    t_critical = stats.t.ppf(1 - alpha/2, df=n-1)
    margin = t_critical * se
    ci_lower = bias - margin
    ci_upper = bias + margin
    
    logger.info(
        f"偏倚分析完成：Bias={bias:.6f}, t={t_stat:.4f}, p={p_value:.4f}, "
        f"显著={'是' if is_significant else '否'}"
    )
    
    return BiasAnalysis(
        bias=bias,
        bias_percent=bias_percent,
        t_statistic=t_stat,
        p_value=p_value,
        is_significant=is_significant,
        confidence_interval=(ci_lower, ci_upper)
    )


# ==================== 线性分析 ====================

def calculate_linearity(
    reference_values: np.ndarray,
    measurements: np.ndarray,
    process_variation: Optional[float] = None
) -> LinearityAnalysis:
    """
    计算线性
    
    参数:
        reference_values: 参考值数组（不同零件的已知值）
        measurements: 对应的测量值数组（可以是多次测量的均值）
        process_variation: 过程变差（用于计算线性度百分比）
    
    返回:
        LinearityAnalysis
    """
    if len(reference_values) != len(measurements):
        raise ValueError("参考值和测量值数量必须相同")
    
    n = len(reference_values)
    
    if n < 3:
        raise ValueError("至少需要 3 个数据点进行线性分析")
    
    # 线性回归
    slope, intercept, r_value, p_value, std_err = stats.linregress(reference_values, measurements)
    
    r_squared = r_value ** 2
    
    # 计算偏倚
    biases = measurements - reference_values
    
    # 对偏倚进行回归分析（偏倚 vs 参考值）
    slope_bias, intercept_bias, r_bias, p_slope, std_err_slope = stats.linregress(reference_values, biases)
    
    # 截距的 p 值（需要手动计算）
    # t 统计量 for intercept
    se_intercept = std_err_slope * np.sqrt(np.sum(reference_values**2) / n)
    t_intercept = intercept_bias / se_intercept if se_intercept > 0 else 0
    p_intercept = 2 * (1 - stats.t.cdf(abs(t_intercept), df=n-2))
    
    # 线性度 = |斜率| * 过程变差
    if process_variation:
        linearity = abs(slope_bias) * process_variation
        linearity_percent = (linearity / process_variation) * 100
    else:
        linearity = abs(slope_bias)
        linearity_percent = abs(slope_bias) * 100
    
    # 线性判断：斜率不显著（p > 0.05）表示线性良好
    is_linear = p_slope > 0.05
    
    logger.info(
        f"线性分析完成：Slope={slope_bias:.6f}, R²={r_squared:.4f}, "
        f"线性度={linearity:.6f}, 线性良好={'是' if is_linear else '否'}"
    )
    
    return LinearityAnalysis(
        slope=slope_bias,
        intercept=intercept_bias,
        r_squared=r_squared,
        p_value_slope=p_slope,
        p_value_intercept=p_intercept,
        is_linear=is_linear,
        linearity=linearity,
        linearity_percent=linearity_percent
    )


# ==================== 工具函数 ====================

def prepare_grr_data(
    flat_data: List[float],
    n_parts: int,
    n_operators: int,
    n_trials: int
) -> np.ndarray:
    """
    将扁平数据转换为 GR&R 分析所需的三维数组
    
    参数:
        flat_data: 扁平的测量值列表
        n_parts: 零件数
        n_operators: 操作者数
        n_trials: 试验次数
    
    返回:
        三维数组，shape=(parts, operators, trials)
    """
    expected_length = n_parts * n_operators * n_trials
    
    if len(flat_data) != expected_length:
        raise ValueError(
            f"数据量不匹配：期望 {expected_length}, 实际 {len(flat_data)}"
        )
    
    data = np.array(flat_data)
    
    # 重塑为 (parts, operators, trials)
    # 假设数据按顺序：零件 1-操作者 A-试验 1,2,3... 零件 1-操作者 B-试验 1,2,3...
    return data.reshape(n_parts, n_operators, n_trials)


def evaluate_grr_acceptance(percent_grr: float, ndc: int) -> Dict[str, any]:
    """
    GR&R 接受度评估
    
    返回评估结果和建议
    """
    if percent_grr <= 10:
        if ndc >= 5:
            return {
                "status": "Acceptable",
                "recommendation": "测量系统可以接受",
                "color": "green"
            }
        else:
            return {
                "status": "Marginal (Low NDC)",
                "recommendation": "%GR&R 良好但 NDC 不足，建议增加零件变差或改进分辨率",
                "color": "yellow"
            }
    elif percent_grr <= 30:
        if ndc >= 4:
            return {
                "status": "Marginal",
                "recommendation": "测量系统可基于重要性、成本等因素有条件接受",
                "color": "yellow"
            }
        else:
            return {
                "status": "Marginal (Low NDC)",
                "recommendation": "需要改进测量系统",
                "color": "orange"
            }
    else:
        return {
            "status": "Unacceptable",
            "recommendation": "测量系统需要改进",
            "color": "red"
        }
