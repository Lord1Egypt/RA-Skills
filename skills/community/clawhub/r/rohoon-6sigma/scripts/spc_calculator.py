"""
SPC 统计计算核心模块
遵循 AIAG VDA SPC 第二版（黄皮书）标准
"""

import numpy as np
from scipy import stats
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class ChartType(str, Enum):
    """控制图类型"""
    XBAR_R = "Xbar-R"
    XBAR_S = "Xbar-S"
    I_MR = "I-MR"
    P = "p"
    NP = "np"
    C = "c"
    U = "u"


@dataclass
class ControlLimitResult:
    """控制限计算结果"""
    ucl: float  # 上控制限
    cl: float   # 中心线
    lcl: float  # 下控制限
    subgroup_means: Optional[List[float]] = None
    subgroup_ranges: Optional[List[float]] = None
    subgroup_stds: Optional[List[float]] = None


@dataclass
class ViolationRule:
    """判异规则违反记录"""
    rule_id: int
    rule_name: str
    description: str
    subgroup_index: int
    value: float


@dataclass
class StabilityAnalysis:
    """稳定性分析结果"""
    is_stable: bool
    violations: List[ViolationRule]
    total_subgroups: int


@dataclass
class CapabilityAnalysis:
    """过程能力分析结果"""
    cp: float
    cpk: float
    cpu: float
    cpl: float
    pp: float
    ppk: float
    ppu: float
    ppl: float
    mean: float
    std_dev_within: float  # 组内标准差
    std_dev_overall: float  # 整体标准差
    is_normal: bool
    normality_p_value: float
    capability_level: str
    is_capable: bool


# ==================== 控制图系数表 (AIAG VDA SPC) ====================

# Xbar-R 图系数
CONTROL_CHART_CONSTANTS = {
    # n: (A2, D3, D4, d2, E2)
    2: (1.880, 0, 3.267, 1.128, 2.660),
    3: (1.023, 0, 2.574, 1.693, 1.777),
    4: (0.729, 0, 2.282, 2.059, 1.457),
    5: (0.577, 0, 2.114, 2.326, 1.290),
    6: (0.483, 0, 2.004, 2.534, 1.184),
    7: (0.419, 0.076, 1.924, 2.704, 1.109),
    8: (0.373, 0.136, 1.864, 2.847, 1.054),
    9: (0.337, 0.184, 1.816, 2.970, 1.010),
    10: (0.308, 0.223, 1.777, 3.078, 0.975),
}


def get_control_chart_constants(n: int) -> Tuple[float, float, float, float, float]:
    """获取控制图系数"""
    if n < 2 or n > 10:
        # 超出范围时使用近似值
        logger.warning(f"子组大小 {n} 超出标准范围 [2,10]，使用近似计算")
        d2 = np.sqrt(n) * 1.1  # 近似
        A2 = 3 / (d2 * np.sqrt(n))
        D3 = max(0, 1 - 3/d2*np.sqrt(1-1/n))
        D4 = 1 + 3/d2*np.sqrt(1-1/n)
        E2 = 3 / d2
        return (A2, D3, D4, d2, E2)
    return CONTROL_CHART_CONSTANTS[n]


# ==================== 控制限计算 ====================

def calculate_xbar_r_limits(data: np.ndarray) -> ControlLimitResult:
    """
    计算 Xbar-R 图控制限
    
    参数:
        data: 二维数组，shape=(subgroups, subgroup_size)
    
    返回:
        ControlLimitResult 包含 Xbar 图和 R 图的控制限
    """
    n_subgroups, n = data.shape
    A2, D3, D4, d2, _ = get_control_chart_constants(n)
    
    # 计算每个子组的均值和极差
    subgroup_means = np.mean(data, axis=1)
    subgroup_ranges = np.ptp(data, axis=1)  # peak-to-peak (max - min)
    
    # 计算总均值和平均极差
    xbar_bar = np.mean(subgroup_means)
    r_bar = np.mean(subgroup_ranges)
    
    # Xbar 图控制限
    xbar_ucl = xbar_bar + A2 * r_bar
    xbar_lcl = xbar_bar - A2 * r_bar
    
    # R 图控制限
    r_ucl = D4 * r_bar
    r_lcl = D3 * r_bar
    r_lcl = max(0, r_lcl)  # 极差不能为负
    
    logger.info(f"Xbar-R 控制限计算完成：UCL={xbar_ucl:.4f}, CL={xbar_bar:.4f}, LCL={xbar_lcl:.4f}")
    
    return ControlLimitResult(
        ucl=xbar_ucl, cl=xbar_bar, lcl=xbar_lcl,
        subgroup_means=subgroup_means.tolist(),
        subgroup_ranges=subgroup_ranges.tolist()
    )


def calculate_xbar_s_limits(data: np.ndarray) -> ControlLimitResult:
    """
    计算 Xbar-S 图控制限（适用于子组大小 n > 10）
    
    参数:
        data: 二维数组，shape=(subgroups, subgroup_size)
    """
    n_subgroups, n = data.shape
    
    # 计算系数
    c4 = 4 * (n - 1) / (4 * n - 3)  # c4 系数
    A3 = 3 / (c4 * np.sqrt(n))
    B3 = max(0, 1 - 3/c4 * np.sqrt(1 - c4**2))
    B4 = 1 + 3/c4 * np.sqrt(1 - c4**2)
    
    # 计算每个子组的均值和标准差
    subgroup_means = np.mean(data, axis=1)
    subgroup_stds = np.std(data, axis=1, ddof=1)
    
    # 计算总均值和平均标准差
    xbar_bar = np.mean(subgroup_means)
    s_bar = np.mean(subgroup_stds)
    
    # Xbar 图控制限
    xbar_ucl = xbar_bar + A3 * s_bar
    xbar_lcl = xbar_bar - A3 * s_bar
    
    # S 图控制限
    s_ucl = B4 * s_bar
    s_lcl = B3 * s_bar
    s_lcl = max(0, s_lcl)
    
    logger.info(f"Xbar-S 控制限计算完成：UCL={xbar_ucl:.4f}, CL={xbar_bar:.4f}, LCL={xbar_lcl:.4f}")
    
    return ControlLimitResult(
        ucl=xbar_ucl, cl=xbar_bar, lcl=xbar_lcl,
        subgroup_means=subgroup_means.tolist(),
        subgroup_stds=subgroup_stds.tolist()
    )


def calculate_i_mr_limits(data: np.ndarray) -> ControlLimitResult:
    """
    计算 I-MR 图（单值 - 移动极差图）控制限
    适用于子组大小 n=1 的情况
    
    参数:
        data: 一维数组，shape=(n_observations,)
    """
    if data.ndim == 2:
        data = data.flatten()
    
    n = len(data)
    E2 = 2.660  # n=2 时的 E2 系数（移动极差基于相邻两点）
    D3, D4 = 0, 3.267  # n=2 时的 D3, D4
    d2 = 1.128
    
    # 计算移动极差（相邻两点的绝对差）
    moving_ranges = np.abs(np.diff(data))
    mr_bar = np.mean(moving_ranges)
    
    # 计算均值
    x_bar = np.mean(data)
    
    # I 图（单值图）控制限
    i_ucl = x_bar + E2 * mr_bar
    i_lcl = x_bar - E2 * mr_bar
    
    # MR 图（移动极差图）控制限
    mr_ucl = D4 * mr_bar
    mr_lcl = D3 * mr_bar
    mr_lcl = max(0, mr_lcl)
    
    # 估计标准差
    sigma_estimate = mr_bar / d2
    
    logger.info(f"I-MR 控制限计算完成：UCL={i_ucl:.4f}, CL={x_bar:.4f}, LCL={i_lcl:.4f}")
    
    return ControlLimitResult(
        ucl=i_ucl, cl=x_bar, lcl=i_lcl,
        subgroup_means=data.tolist(),
        subgroup_ranges=moving_ranges.tolist()
    )


# ==================== 判异规则检测 (8 大规则) ====================

def detect_violation_rules(values: np.ndarray, ucl: float, cl: float, lcl: float) -> List[ViolationRule]:
    """
    检测 8 大判异规则违反情况
    
    规则说明（AIAG VDA SPC）:
    1. 1 点超出 3σ控制限
    2. 连续 9 点在中心线同一侧
    3. 连续 6 点递增或递减
    4. 连续 14 点上下交替
    5. 连续 3 点中有 2 点超出 2σ（同一侧）
    6. 连续 5 点中有 4 点超出 1σ（同一侧）
    7. 连续 15 点在 1σ范围内（中心线两侧）
    8. 连续 8 点超出 1σ范围（两侧）
    """
    violations = []
    n = len(values)
    
    if n < 2:
        return violations
    
    # 计算 1σ, 2σ, 3σ界限
    sigma = (ucl - cl) / 3
    one_sigma_upper = cl + sigma
    one_sigma_lower = cl - sigma
    two_sigma_upper = cl + 2 * sigma
    two_sigma_lower = cl - 2 * sigma
    
    # 规则 1: 1 点超出 3σ控制限
    for i, val in enumerate(values):
        if val > ucl or val < lcl:
            violations.append(ViolationRule(
                rule_id=1,
                rule_name="Rule 1: Beyond 3σ",
                description="1 点超出 3σ控制限",
                subgroup_index=i,
                value=val
            ))
    
    # 规则 2: 连续 9 点在中心线同一侧
    consecutive_above = 0
    consecutive_below = 0
    for i, val in enumerate(values):
        if val > cl:
            consecutive_above += 1
            consecutive_below = 0
        elif val < cl:
            consecutive_below += 1
            consecutive_above = 0
        else:
            consecutive_above = 0
            consecutive_below = 0
        
        if consecutive_above >= 9:
            violations.append(ViolationRule(
                rule_id=2,
                rule_name="Rule 2: 9 consecutive same side",
                description="连续 9 点在中心线上方",
                subgroup_index=i,
                value=val
            ))
        if consecutive_below >= 9:
            violations.append(ViolationRule(
                rule_id=2,
                rule_name="Rule 2: 9 consecutive same side",
                description="连续 9 点在中心线下方",
                subgroup_index=i,
                value=val
            ))
    
    # 规则 3: 连续 6 点递增或递减
    if n >= 6:
        for i in range(n - 5):
            segment = values[i:i+6]
            if np.all(np.diff(segment) > 0):
                violations.append(ViolationRule(
                    rule_id=3,
                    rule_name="Rule 3: 6 consecutive increasing",
                    description="连续 6 点递增",
                    subgroup_index=i+5,
                    value=values[i+5]
                ))
            elif np.all(np.diff(segment) < 0):
                violations.append(ViolationRule(
                    rule_id=3,
                    rule_name="Rule 3: 6 consecutive decreasing",
                    description="连续 6 点递减",
                    subgroup_index=i+5,
                    value=values[i+5]
                ))
    
    # 规则 4: 连续 14 点上下交替
    if n >= 14:
        for i in range(n - 13):
            segment = values[i:i+14]
            diffs = np.diff(segment)
            alternating = True
            for j in range(len(diffs) - 1):
                if diffs[j] * diffs[j+1] >= 0:
                    alternating = False
                    break
            if alternating:
                violations.append(ViolationRule(
                    rule_id=4,
                    rule_name="Rule 4: 14 consecutive alternating",
                    description="连续 14 点上下交替",
                    subgroup_index=i+13,
                    value=values[i+13]
                ))
    
    # 规则 5: 连续 3 点中有 2 点超出 2σ（同一侧）
    if n >= 3:
        for i in range(n - 2):
            segment = values[i:i+3]
            above_2sigma = sum(1 for v in segment if v > two_sigma_upper)
            below_2sigma = sum(1 for v in segment if v < two_sigma_lower)
            if above_2sigma >= 2:
                violations.append(ViolationRule(
                    rule_id=5,
                    rule_name="Rule 5: 2 of 3 beyond 2σ",
                    description="连续 3 点中有 2 点超出 2σ（上方）",
                    subgroup_index=i+2,
                    value=values[i+2]
                ))
            if below_2sigma >= 2:
                violations.append(ViolationRule(
                    rule_id=5,
                    rule_name="Rule 5: 2 of 3 beyond 2σ",
                    description="连续 3 点中有 2 点超出 2σ（下方）",
                    subgroup_index=i+2,
                    value=values[i+2]
                ))
    
    # 规则 6: 连续 5 点中有 4 点超出 1σ（同一侧）
    if n >= 5:
        for i in range(n - 4):
            segment = values[i:i+5]
            above_1sigma = sum(1 for v in segment if v > one_sigma_upper)
            below_1sigma = sum(1 for v in segment if v < one_sigma_lower)
            if above_1sigma >= 4:
                violations.append(ViolationRule(
                    rule_id=6,
                    rule_name="Rule 6: 4 of 5 beyond 1σ",
                    description="连续 5 点中有 4 点超出 1σ（上方）",
                    subgroup_index=i+4,
                    value=values[i+4]
                ))
            if below_1sigma >= 4:
                violations.append(ViolationRule(
                    rule_id=6,
                    rule_name="Rule 6: 4 of 5 beyond 1σ",
                    description="连续 5 点中有 4 点超出 1σ（下方）",
                    subgroup_index=i+4,
                    value=values[i+4]
                ))
    
    # 规则 7: 连续 15 点在 1σ范围内
    if n >= 15:
        for i in range(n - 14):
            segment = values[i:i+15]
            if np.all((segment >= one_sigma_lower) & (segment <= one_sigma_upper)):
                violations.append(ViolationRule(
                    rule_id=7,
                    rule_name="Rule 7: 15 consecutive within 1σ",
                    description="连续 15 点在 1σ范围内",
                    subgroup_index=i+14,
                    value=values[i+14]
                ))
    
    # 规则 8: 连续 8 点超出 1σ范围
    if n >= 8:
        for i in range(n - 7):
            segment = values[i:i+8]
            outside_1sigma = [(v < one_sigma_lower or v > one_sigma_upper) for v in segment]
            if np.all(outside_1sigma):
                violations.append(ViolationRule(
                    rule_id=8,
                    rule_name="Rule 8: 8 consecutive beyond 1σ",
                    description="连续 8 点超出 1σ范围",
                    subgroup_index=i+7,
                    value=values[i+7]
                ))
    
    if violations:
        logger.warning(f"检测到 {len(violations)} 条判异规则违反")
    
    return violations


def analyze_stability(values: np.ndarray, ucl: float, cl: float, lcl: float) -> StabilityAnalysis:
    """
    分析过程稳定性
    
    参数:
        values: 子组均值序列
        ucl, cl, lcl: 控制限
    
    返回:
        StabilityAnalysis 包含稳定性判断和违反规则
    """
    violations = detect_violation_rules(values, ucl, cl, lcl)
    is_stable = len(violations) == 0
    
    return StabilityAnalysis(
        is_stable=is_stable,
        violations=violations,
        total_subgroups=len(values)
    )


# ==================== 过程能力分析 ====================

def test_normality(data: np.ndarray) -> Tuple[bool, float, str]:
    """
    正态性检验
    
    优先使用 Shapiro-Wilk 检验（适用于小样本）
    大样本时使用 Anderson-Darling 检验
    
    返回:
        (is_normal, p_value, test_name)
    """
    n = len(data)
    
    if n < 3:
        return (True, 1.0, "Insufficient data")
    
    # Shapiro-Wilk 检验（适用于 3 <= n <= 5000）
    if n <= 5000:
        try:
            stat, p_value = stats.shapiro(data)
            is_normal = p_value > 0.05
            return (is_normal, p_value, "Shapiro-Wilk")
        except Exception as e:
            logger.warning(f"Shapiro-Wilk 检验失败：{e}")
    
    # Anderson-Darling 检验
    try:
        result = stats.anderson(data, dist='norm')
        # 比较统计量与临界值
        is_normal = result.statistic < result.critical_values[2]  # 5% 显著性水平
        return (is_normal, 0.05, "Anderson-Darling")
    except Exception as e:
        logger.warning(f"Anderson-Darling 检验失败：{e}")
        return (True, 1.0, "Test failed, assuming normal")


def calculate_capability(
    data: np.ndarray,
    usL: float,
    lsl: float,
    target: Optional[float] = None
) -> CapabilityAnalysis:
    """
    计算过程能力指数
    
    参数:
        data: 测量数据
        usL: 上规格限
        lsl: 下规格限
        target: 目标值（可选）
    
    返回:
        CapabilityAnalysis 包含所有能力指数
    """
    n = len(data)
    mean = np.mean(data)
    
    # 计算标准差
    std_dev_within = np.std(data, ddof=1)  # 样本标准差（组内）
    std_dev_overall = std_dev_within  # 对于单值数据，组内=整体
    
    # 正态性检验
    is_normal, p_value, test_name = test_normality(data)
    
    if not is_normal:
        logger.warning(f"数据未通过正态性检验 ({test_name}, p={p_value:.4f})")
    
    # 能力指数计算
    # Cp = (USL - LSL) / (6 * sigma)
    cp = (usL - lsl) / (6 * std_dev_within) if std_dev_within > 0 else float('inf')
    
    # Cpu = (USL - mean) / (3 * sigma)
    cpu = (usL - mean) / (3 * std_dev_within) if std_dev_within > 0 else float('inf')
    
    # Cpl = (mean - LSL) / (3 * sigma)
    cpl = (mean - lsl) / (3 * std_dev_within) if std_dev_within > 0 else float('inf')
    
    # Cpk = min(Cpu, Cpl)
    cpk = min(cpu, cpl)
    
    # 性能指数（使用整体标准差，这里与组内相同）
    pp = cp
    ppu = cpu
    ppl = cpl
    ppk = cpk
    
    # 能力等级评估
    if cpk >= 2.0:
        capability_level = "Excellent"
    elif cpk >= 1.67:
        capability_level = "Very Good"
    elif cpk >= 1.33:
        capability_level = "Good"
    elif cpk >= 1.0:
        capability_level = "Marginal"
    else:
        capability_level = "Poor"
    
    is_capable = cpk >= 1.33
    
    logger.info(
        f"过程能力分析完成：Cp={cp:.4f}, Cpk={cpk:.4f}, "
        f"等级={capability_level}, 能力={'合格' if is_capable else '不合格'}"
    )
    
    return CapabilityAnalysis(
        cp=cp, cpk=cpk, cpu=cpu, cpl=cpl,
        pp=pp, ppk=ppk, ppu=ppu, ppl=ppl,
        mean=mean,
        std_dev_within=std_dev_within,
        std_dev_overall=std_dev_overall,
        is_normal=is_normal,
        normality_p_value=p_value,
        capability_level=capability_level,
        is_capable=is_capable
    )


# ==================== 工具函数 ====================

def prepare_subgroup_data(
    measurements: List[float],
    subgroup_size: int
) -> np.ndarray:
    """
    将测量数据准备为子组格式
    
    参数:
        measurements: 测量值列表
        subgroup_size: 子组大小
    
    返回:
        二维数组，shape=(n_subgroups, subgroup_size)
    """
    data = np.array(measurements)
    
    # 截断到完整的子组
    n_complete_subgroups = len(data) // subgroup_size
    if n_complete_subgroups == 0:
        raise ValueError(f"数据量不足，需要至少 {subgroup_size} 个测量值")
    
    data = data[:n_complete_subgroups * subgroup_size]
    return data.reshape(n_complete_subgroups, subgroup_size)


def calculate_statistics(data: np.ndarray) -> Dict[str, float]:
    """计算基础统计量"""
    return {
        "count": len(data.flatten()),
        "mean": float(np.mean(data)),
        "std": float(np.std(data, ddof=1)),
        "min": float(np.min(data)),
        "max": float(np.max(data)),
        "median": float(np.median(data)),
        "skewness": float(stats.skew(data.flatten())),
        "kurtosis": float(stats.kurtosis(data.flatten())),
    }
