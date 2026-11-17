#!/usr/bin/env python3
"""
假设检验工具 - 统计假设检验计算与可视化
支持：正态性检验、t检验、卡方检验、方差分析等
"""

import argparse
import json
import sys
import os
from typing import List, Dict, Any, Optional, Tuple

import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import chi2


def parse_data(data_str: str) -> np.ndarray:
    """解析数据输入，支持逗号分隔字符串或文件路径"""
    if os.path.isfile(data_str):
        ext = os.path.splitext(data_str)[1].lower()
        if ext == '.csv':
            df = pd.read_csv(data_str)
            return df.iloc[:, 0].dropna().values
        elif ext in ['.xlsx', '.xls']:
            df = pd.read_excel(data_str)
            return df.iloc[:, 0].dropna().values
        elif ext == '.txt':
            return np.loadtxt(data_str)
        else:
            with open(data_str, 'r') as f:
                content = f.read().strip()
            values = [float(x) for x in content.replace(',', '\n').split()]
            return np.array(values)
    else:
        values = [float(x.strip()) for x in data_str.replace(',', '\n').split() if x.strip()]
        return np.array(values)


def parse_groups(data_str: str) -> List[np.ndarray]:
    """解析多组数据输入，分号分隔各组，逗号分隔组内数据"""
    if os.path.isfile(data_str):
        return parse_groups_from_file(data_str)
    
    groups = []
    for group_str in data_str.split(';'):
        values = [float(x.strip()) for x in group_str.replace(',', ' ').split() if x.strip()]
        if values:
            groups.append(np.array(values))
    return groups


def parse_groups_from_file(filepath: str) -> List[np.ndarray]:
    """从文件解析多组数据"""
    ext = os.path.splitext(filepath)[1].lower()
    if ext == '.csv':
        df = pd.read_csv(filepath)
        groups = []
        for col in df.columns:
            group = df[col].dropna().values
            if len(group) > 0:
                groups.append(group)
        return groups if groups else [df.iloc[:, 0].dropna().values]
    else:
        content = open(filepath, 'r').read().strip()
        return parse_groups(content)


def normality_shapiro(data: np.ndarray, alpha: float) -> Dict[str, Any]:
    """Shapiro-Wilk正态性检验"""
    stat, p_value = stats.shapiro(data)
    n = len(data)
    critical_value = stats.shapiro(data)[0] if n > 5000 else None
    
    result = {
        "test_name": "Shapiro-Wilk正态性检验",
        "test_method": "shapiro",
        "statistic": round(stat, 6),
        "p_value": round(p_value, 6),
        "alpha": alpha,
        "sample_size": int(n),
        "conclusion": "接受原假设：数据服从正态分布" if p_value > alpha else "拒绝原假设：数据不服从正态分布",
        "interpretation": f"W统计量={stat:.4f}, p值={p_value:.4f}"
    }
    return result


def normality_ks(data: np.ndarray, alpha: float) -> Dict[str, Any]:
    """Kolmogorov-Smirnov正态性检验"""
    mean, std = np.mean(data), np.std(data, ddof=1)
    stat, p_value = stats.kstest(data, 'norm', args=(mean, std))
    
    result = {
        "test_name": "Kolmogorov-Smirnov正态性检验",
        "test_method": "ks",
        "statistic": round(stat, 6),
        "p_value": round(p_value, 6),
        "alpha": alpha,
        "sample_size": int(len(data)),
        "conclusion": "接受原假设：数据服从正态分布" if p_value > alpha else "拒绝原假设：数据不服从正态分布",
        "interpretation": f"KS统计量={stat:.4f}, p值={p_value:.4f}"
    }
    return result


def t_test_one_sample(data: np.ndarray, pop_mean: float, alpha: float) -> Dict[str, Any]:
    """单样本t检验"""
    n = len(data)
    mean = np.mean(data)
    std = np.std(data, ddof=1)
    se = std / np.sqrt(n)
    t_stat = (mean - pop_mean) / se
    df = n - 1
    p_value = 2 * stats.t.sf(abs(t_stat), df)
    t_critical = stats.t.ppf(1 - alpha/2, df)
    ci_lower = mean - t_critical * se
    ci_upper = mean + t_critical * se
    
    result = {
        "test_name": "单样本t检验",
        "test_method": "one_sample_t",
        "hypotheses": {"null": f"μ = {pop_mean}", "alternative": f"μ ≠ {pop_mean}"},
        "sample_mean": round(mean, 6),
        "sample_std": round(std, 6),
        "population_mean_tested": pop_mean,
        "t_statistic": round(t_stat, 6),
        "df": int(df),
        "p_value": round(p_value, 6),
        "alpha": alpha,
        "t_critical": round(t_critical, 6),
        "confidence_interval": [round(ci_lower, 6), round(ci_upper, 6)],
        "conclusion": f"拒绝原假设：样本均值与{pop_mean}存在显著差异" if p_value < alpha else f"接受原假设：样本均值与{pop_mean}无显著差异",
        "interpretation": f"t({df})={t_stat:.4f}, p={p_value:.4f}, 95%CI=[{ci_lower:.4f}, {ci_upper:.4f}]"
    }
    return result


def t_test_two_sample(data1: np.ndarray, data2: np.ndarray, alpha: float, paired: bool = False) -> Dict[str, Any]:
    """两样本t检验（独立或配对）"""
    mean1, mean2 = np.mean(data1), np.mean(data2)
    n1, n2 = len(data1), len(data2)
    var1, var2 = np.var(data1, ddof=1), np.var(data2, ddof=1)
    
    if paired:
        diff = data1 - data2
        mean_diff = np.mean(diff)
        std_diff = np.std(diff, ddof=1)
        se = std_diff / np.sqrt(n1)
        t_stat = mean_diff / se
        df = n1 - 1
        test_name = "配对样本t检验"
        method = "paired_t"
        effect_size = mean_diff / std_diff if std_diff > 0 else 0
    else:
        se = np.sqrt(var1/n1 + var2/n2)
        t_stat = (mean1 - mean2) / se
        df = int((var1/n1 + var2/n2)**2 / ((var1/n1)**2/(n1-1) + (var2/n2)**2/(n2-1)))
        effect_size = (mean1 - mean2) / np.sqrt((var1 + var2) / 2)
        test_name = "独立样本t检验"
        method = "two_sample_t"
    
    p_value = 2 * stats.t.sf(abs(t_stat), df)
    t_critical = stats.t.ppf(1 - alpha/2, df)
    ci_lower = (mean1 - mean2) - t_critical * se
    ci_upper = (mean1 - mean2) + t_critical * se
    
    result = {
        "test_name": test_name,
        "test_method": method,
        "hypotheses": {"null": "μ1 = μ2", "alternative": "μ1 ≠ μ2"},
        "sample1": {"mean": round(mean1, 6), "std": round(np.sqrt(var1), 6), "n": n1},
        "sample2": {"mean": round(mean2, 6), "std": round(np.sqrt(var2), 6), "n": n2},
        "t_statistic": round(t_stat, 6),
        "df": int(df),
        "p_value": round(p_value, 6),
        "alpha": alpha,
        "effect_size_cohens_d": round(effect_size, 6),
        "confidence_interval": [round(ci_lower, 6), round(ci_upper, 6)],
        "conclusion": "拒绝原假设：两组均值存在显著差异" if p_value < alpha else "接受原假设：两组均值无显著差异",
        "interpretation": f"t({df})={t_stat:.4f}, p={p_value:.4f}, Cohen's d={effect_size:.4f}"
    }
    return result


def chi_square_goodness(data: np.ndarray, expected: Optional[List[float]], alpha: float) -> Dict[str, Any]:
    """卡方拟合优度检验"""
    observed = np.array(data)
    if expected is None:
        expected = np.full_like(observed, np.mean(observed), dtype=float)
    expected = np.array(expected)
    
    if len(observed) != len(expected):
        expected = np.full_like(observed, np.mean(observed), dtype=float)
    
    chi2_stat = np.sum((observed - expected)**2 / expected)
    df = len(observed) - 1
    p_value = 1 - chi2.cdf(chi2_stat, df)
    chi2_critical = chi2.ppf(1 - alpha, df)
    
    result = {
        "test_name": "卡方拟合优度检验",
        "test_method": "chi_square_goodness",
        "hypotheses": {"null": "观测频数符合期望分布", "alternative": "观测频数不符合期望分布"},
        "observed": observed.tolist(),
        "expected": expected.tolist(),
        "chi2_statistic": round(chi2_stat, 6),
        "df": int(df),
        "p_value": round(p_value, 6),
        "alpha": alpha,
        "chi2_critical": round(chi2_critical, 6),
        "conclusion": "拒绝原假设：观测分布与期望分布存在显著差异" if p_value < alpha else "接受原假设：观测分布与期望分布无显著差异",
        "interpretation": f"χ²({df})={chi2_stat:.4f}, p={p_value:.4f}"
    }
    return result


def chi_square_independence(contingency_table: List[List[float]], alpha: float) -> Dict[str, Any]:
    """卡方独立性检验"""
    observed = np.array(contingency_table)
    chi2_stat, p_value, df, expected = stats.chi2_contingency(observed)
    chi2_critical = chi2.ppf(1 - alpha, df)
    
    result = {
        "test_name": "卡方独立性检验",
        "test_method": "chi_square_independence",
        "hypotheses": {"null": "行变量与列变量相互独立", "alternative": "行变量与列变量不独立"},
        "observed": observed.tolist(),
        "expected_frequencies": expected.tolist(),
        "chi2_statistic": round(chi2_stat, 6),
        "df": int(df),
        "p_value": round(p_value, 6),
        "alpha": alpha,
        "chi2_critical": round(chi2_critical, 6),
        "conclusion": "拒绝原假设：变量之间存在显著关联" if p_value < alpha else "接受原假设：变量之间相互独立",
        "interpretation": f"χ²({df})={chi2_stat:.4f}, p={p_value:.4f}"
    }
    return result


def anova_one_way(*data_groups: np.ndarray) -> Dict[str, Any]:
    """单因素方差分析"""
    groups = list(data_groups)
    n_total = sum(len(g) for g in groups)
    grand_mean = sum(np.sum(g) for g in groups) / n_total
    
    ss_between = sum(len(g) * (np.mean(g) - grand_mean)**2 for g in groups)
    ss_within = sum(np.sum((g - np.mean(g))**2) for g in groups)
    df_between = len(groups) - 1
    df_within = n_total - len(groups)
    
    ms_between = ss_between / df_between
    ms_within = ss_within / df_within
    f_stat = ms_between / ms_within
    p_value = 1 - stats.f.cdf(f_stat, df_between, df_within)
    
    group_stats = []
    for i, g in enumerate(groups):
        group_stats.append({
            "group": f"Group {i+1}",
            "n": int(len(g)),
            "mean": round(np.mean(g), 6),
            "std": round(np.std(g, ddof=1), 6)
        })
    
    result = {
        "test_name": "单因素方差分析(ANOVA)",
        "test_method": "anova_one_way",
        "hypotheses": {"null": "所有组均值相等", "alternative": "至少有一组均值不同"},
        "group_statistics": group_stats,
        "f_statistic": round(f_stat, 6),
        "df": f"{df_between},{df_within}",
        "p_value": round(p_value, 6),
        "ss_between": round(ss_between, 6),
        "ss_within": round(ss_within, 6),
        "ms_between": round(ms_between, 6),
        "ms_within": round(ms_within, 6),
        "conclusion": "拒绝原假设：至少有一组均值与其他组存在显著差异" if p_value < 0.05 else "接受原假设：所有组均值无显著差异",
        "interpretation": f"F({df_between},{df_within})={f_stat:.4f}, p={p_value:.4f}"
    }
    return result


def levene_test(*data_groups: np.ndarray, alpha: float) -> Dict[str, Any]:
    """Levene方差齐性检验"""
    groups = list(data_groups)
    stat, p_value = stats.levene(*groups)
    
    result = {
        "test_name": "Levene方差齐性检验",
        "test_method": "levene",
        "hypotheses": {"null": "各组方差相等", "alternative": "至少有一组方差不等"},
        "group_statistics": [{"group": f"Group {i+1}", "variance": round(np.var(g, ddof=1), 6)} for i, g in enumerate(groups)],
        "w_statistic": round(stat, 6),
        "p_value": round(p_value, 6),
        "alpha": alpha,
        "conclusion": "拒绝原假设：各组方差不相等" if p_value < alpha else "接受原假设：各组方差相等",
        "interpretation": f"W={stat:.4f}, p={p_value:.4f}"
    }
    return result


def mann_whitney_u(data1: np.ndarray, data2: np.ndarray, alpha: float) -> Dict[str, Any]:
    """Mann-Whitney U非参数检验"""
    stat, p_value = stats.mannwhitneyu(data1, data2, alternative='two-sided')
    n1, n2 = len(data1), len(data2)
    
    result = {
        "test_name": "Mann-Whitney U检验",
        "test_method": "mann_whitney",
        "hypotheses": {"null": "两组分布相同", "alternative": "两组分布不同"},
        "sample1": {"n": int(n1), "median": round(np.median(data1), 6)},
        "sample2": {"n": int(n2), "median": round(np.median(data2), 6)},
        "u_statistic": round(stat, 6),
        "p_value": round(p_value, 6),
        "alpha": alpha,
        "conclusion": "拒绝原假设：两组分布存在显著差异" if p_value < alpha else "接受原假设：两组分布无显著差异",
        "interpretation": f"U={stat:.4f}, p={p_value:.4f}"
    }
    return result


def run_test(test_type: str, data1: np.ndarray, data2: Optional[np.ndarray],
             alpha: float, expected: Optional[List[float]], 
             data_groups: Optional[List[np.ndarray]] = None, **kwargs) -> Dict[str, Any]:
    """根据检验类型运行相应的假设检验"""
    test_map = {
        'shapiro': lambda: normality_shapiro(data1, alpha),
        'ks': lambda: normality_ks(data1, alpha),
        'one_sample_t': lambda: t_test_one_sample(data1, kwargs.get('pop_mean', np.mean(data1)), alpha),
        'two_sample_t': lambda: t_test_two_sample(data1, data2, alpha, paired=False),
        'paired_t': lambda: t_test_two_sample(data1, data2, alpha, paired=True),
        'chi_square_goodness': lambda: chi_square_goodness(data1, expected, alpha),
        'chi_square_independence': lambda: chi_square_independence(data1, alpha),
        'anova': lambda: anova_one_way(*([data1] + (data_groups if data_groups else []))),
        'levene': lambda: levene_test(data1, data2, alpha=alpha),
        'mann_whitney': lambda: mann_whitney_u(data1, data2, alpha),
    }
    
    if test_type not in test_map:
        return {"error": f"不支持的检验类型: {test_type}"}
    
    return test_map[test_type]()


def main():
    parser = argparse.ArgumentParser(description='假设检验工具 - 统计假设检验计算')
    parser.add_argument('--test', required=True, 
                       choices=['shapiro', 'ks', 'one_sample_t', 'two_sample_t', 'paired_t',
                               'chi_square_goodness', 'chi_square_independence', 'anova', 
                               'levene', 'mann_whitney'],
                       help='检验类型')
    parser.add_argument('--data1', required=True, help='第一组数据(逗号分隔或文件路径)')
    parser.add_argument('--data2', help='第二组数据(逗号分隔或文件路径，用于两样本检验)')
    parser.add_argument('--alpha', type=float, default=0.05, help='显著性水平(默认0.05)')
    parser.add_argument('--expected', help='期望值(逗号分隔，用于卡方检验)')
    parser.add_argument('--pop_mean', type=float, help='总体均值(用于单样本t检验)')
    parser.add_argument('--output', help='输出JSON文件路径(可选)')
    
    args = parser.parse_args()
    
    try:
        data1 = parse_data(args.data1)
        
        data2 = None
        data_groups = None
        
        if args.test == 'anova' and args.data2:
            # ANOVA: data2包含额外的组，分号分隔
            data_groups = parse_groups(args.data2)
        elif args.data2:
            # 其他两样本检验
            data2 = parse_data(args.data2)
        
        expected = None
        if args.expected:
            expected = [float(x) for x in args.expected.replace(',', ' ').split()]
        
        kwargs = {}
        if args.pop_mean is not None:
            kwargs['pop_mean'] = args.pop_mean
        
        if args.test == 'chi_square_independence':
            contingency = [[float(x) for x in row.split(',')] for row in args.data1.split(';')]
            data1 = contingency
        
        result = run_test(args.test, data1, data2, args.alpha, expected, data_groups=data_groups, **kwargs)
        result['parameters'] = {
            'alpha': args.alpha,
            'data1_size': len(data1),
            'data2_size': len(data2) if data2 is not None else None
        }
        
        output = json.dumps(result, ensure_ascii=False, indent=2)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"结果已保存至: {args.output}")
        else:
            print(output)
            
    except Exception as e:
        error_result = {"error": str(e), "type": type(e).__name__}
        print(json.dumps(error_result, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
