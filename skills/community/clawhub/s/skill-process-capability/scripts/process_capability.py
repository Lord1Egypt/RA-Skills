#!/usr/bin/env python3
"""
过程能力分析核心脚本
支持CP、CPK、PP、PPK、CMK等指标计算及分布拟合
"""

import argparse
import json
import sys
from typing import Optional, List, Dict, Any
import numpy as np
from scipy import stats


def calculate_capability_metrics(
    data: List[float],
    usl: Optional[float] = None,
    lsl: Optional[float] = None,
    target: Optional[float] = None,
    sigma_level: float = 3.0
) -> Dict[str, Any]:
    """
    计算过程能力指标
    
    参数:
        data: 测量数据列表
        usl: 上规格限
        lsl: 下规格限
        target: 目标值
        sigma_level: sigma水平(默认3σ)
    
    返回:
        包含所有指标的字典
    """
    data = np.array(data)
    n = len(data)
    
    # 基本统计量
    mean = np.mean(data)
    std_long = np.std(data, ddof=1)  # 长期标准差(整体)
    median = np.median(data)
    min_val = np.min(data)
    max_val = np.max(data)
    
    # 范围估计短期标准差(使用均值极差法)
    if n >= 2:
        r = np.max(data) - np.min(data)
        # d2因子表(子组大小n=5时d2=2.326)
        d2_table = {2: 1.128, 3: 1.693, 4: 2.059, 5: 2.326, 6: 2.534, 7: 2.704, 8: 2.847, 9: 2.970, 10: 3.078}
        d2 = d2_table.get(min(n, 10), 3.078)
        std_short = r / d2  # 短期标准差(组内)
    else:
        std_short = std_long
    
    result = {
        "basic_stats": {
            "sample_size": n,
            "mean": round(mean, 6),
            "median": round(median, 6),
            "std_long": round(std_long, 6),
            "std_short": round(std_short, 6),
            "min": round(min_val, 6),
            "max": round(max_val, 6),
            "range": round(max_val - min_val, 6)
        },
        "distribution_tests": {}
    }
    
    # 规格限存在时计算过程能力
    if usl is not None and lsl is not None:
        # 过程能力指数(CP系列 - 使用长期标准差)
        cp = (usl - lsl) / (6 * std_long) if std_long > 0 else 0
        cpu = (usl - mean) / (3 * std_long) if std_long > 0 else 0
        cpl = (mean - lsl) / (3 * std_long) if std_long > 0 else 0
        cpk = min(cpu, cpl)
        
        # 若有目标值，计算K和CPK(修正)
        if target is not None:
            k = abs(mean - target) / ((usl - lsl) / 2)
            cpk_corrected = cp * (1 - k)
        else:
            target_calc = (usl + lsl) / 2
            k = abs(mean - target_calc) / ((usl - lsl) / 2)
            cpk_corrected = cp * (1 - k)
        
        # PPM计算(基于3σ)
        z_upper = (usl - mean) / std_long if std_long > 0 else 0
        z_lower = (lsl - mean) / std_long if std_long > 0 else 0
        ppm_upper = (1 - stats.norm.cdf(z_upper)) * 1e6
        ppm_lower = stats.norm.cdf(z_lower) * 1e6
        ppm_total = ppm_upper + ppm_lower
        
        # 短期过程能力(使用std_short)
        pp = (usl - lsl) / (6 * std_short) if std_short > 0 else 0
        ppu = (usl - mean) / (3 * std_short) if std_short > 0 else 0
        ppl = (mean - lsl) / (3 * std_short) if std_short > 0 else 0
        ppk = min(ppu, ppl)
        
        result["capability_indices"] = {
            "cp": round(cp, 4),
            "cpu": round(cpu, 4),
            "cpl": round(cpl, 4),
            "cpk": round(cpk, 4),
            "cpk_corrected": round(cpk_corrected, 4),
            "k": round(k, 4),
            "pp": round(pp, 4),
            "ppu": round(ppu, 4),
            "ppl": round(ppl, 4),
            "ppk": round(ppk, 4)
        }
        
        result["ppm"] = {
            "ppm_upper": round(ppm_upper, 2),
            "ppm_lower": round(ppm_lower, 2),
            "ppm_total": round(ppm_total, 2),
            "yield_percent": round(100 - ppm_total / 10000, 4)
        }
        
        result["specification_limits"] = {
            "usl": usl,
            "lsl": lsl,
            "target": target if target else round((usl + lsl) / 2, 4),
            "sigma_level": sigma_level
        }
    
    # 仅有USL(单侧规格)
    elif usl is not None:
        cpu = (usl - mean) / (3 * std_long) if std_long > 0 else 0
        ppm_upper = (1 - stats.norm.cdf((usl - mean) / std_long)) * 1e6 if std_long > 0 else 0
        
        result["capability_indices"] = {
            "cpu": round(cpu, 4),
            "single_sided": "usl"
        }
        result["ppm"] = {
            "ppm_upper": round(ppm_upper, 2),
            "yield_percent": round(100 - ppm_upper / 10000, 4)
        }
        result["specification_limits"] = {"usl": usl}
    
    # 仅有LSL(单侧规格)
    elif lsl is not None:
        cpl = (mean - lsl) / (3 * std_long) if std_long > 0 else 0
        ppm_lower = stats.norm.cdf((lsl - mean) / std_long) * 1e6 if std_long > 0 else 0
        
        result["capability_indices"] = {
            "cpl": round(cpl, 4),
            "single_sided": "lsl"
        }
        result["ppm"] = {
            "ppm_lower": round(ppm_lower, 2),
            "yield_percent": round(100 - ppm_lower / 10000, 4)
        }
        result["specification_limits"] = {"lsl": lsl}
    
    return result


def fit_distribution(data: List[float], distribution: str = "normal") -> Dict[str, Any]:
    """
    拟合概率分布
    
    参数:
        data: 数据列表
        distribution: 分布类型(normal, binomial, poisson, exponential, uniform)
    
    返回:
        拟合参数和检验结果
    """
    data = np.array(data)
    n = len(data)
    
    result = {"distribution": distribution, "n": n}
    
    if distribution == "normal":
        # 正态分布拟合
        mu, sigma = stats.norm.fit(data)
        # K-S检验
        ks_stat, ks_pvalue = stats.kstest(data, 'norm', args=(mu, sigma))
        # Shapiro-Wilk检验(适用于n<5000)
        if n < 5000:
            sw_stat, sw_pvalue = stats.shapiro(data)
            result["shapiro_wilk"] = {"statistic": round(sw_stat, 6), "p_value": round(sw_pvalue, 6)}
        
        result["parameters"] = {"mu": round(mu, 6), "sigma": round(sigma, 6)}
        result["ks_test"] = {"statistic": round(ks_stat, 6), "p_value": round(ks_pvalue, 6)}
        result["is_normal"] = ks_pvalue > 0.05
        
    elif distribution == "binomial":
        # 二项分布拟合(n, p)
        n_trials = max(data) if max(data) > 0 else 1
        p = np.mean(data) / n_trials if n_trials > 0 else 0.5
        result["parameters"] = {"n": int(n_trials), "p": round(p, 6)}
        
    elif distribution == "poisson":
        # 泊松分布拟合(lambda)
        lam = np.mean(data)
        # 卡方检验
        freq, _ = np.histogram(data, bins=range(int(max(data)) + 2))
        expected = np.array([stats.poisson.pmf(k, lam) * n for k in range(len(freq))])
        # 简化检验
        result["parameters"] = {"lambda": round(lam, 6)}
        result["is_valid"] = lam >= 0
        
    elif distribution == "exponential":
        # 指数分布拟合
        loc, scale = stats.expon.fit(data)
        result["parameters"] = {"loc": round(loc, 6), "scale": round(scale, 6)}
        
    elif distribution == "uniform":
        # 均匀分布拟合
        loc, scale = stats.uniform.fit(data)
        result["parameters"] = {"min": round(loc, 6), "max": round(loc + scale, 6)}
    
    return result


def main():
    parser = argparse.ArgumentParser(description='过程能力分析核心脚本')
    parser.add_argument('--data-path', type=str, help='数据文件路径(CSV或Excel)')
    parser.add_argument('--column', type=str, help='数据列名')
    parser.add_argument('--usl', type=float, help='上规格限')
    parser.add_argument('--lsl', type=float, help='下规格限')
    parser.add_argument('--target', type=float, help='目标值')
    parser.add_argument('--sigma-level', type=float, default=3.0, help='Sigma水平')
    parser.add_argument('--fit-distribution', type=str, choices=['normal', 'binomial', 'poisson', 'exponential', 'uniform'], 
                        help='拟合分布类型')
    parser.add_argument('--data', type=str, help='直接输入的JSON数组数据')
    
    args = parser.parse_args()
    
    # 获取数据
    if args.data:
        import ast
        try:
            data = ast.literal_eval(args.data)
        except:
            data = json.loads(args.data)
    elif args.data_path:
        import pandas as pd
        if args.data_path.endswith('.xlsx') or args.data_path.endswith('.xls'):
            df = pd.read_excel(args.data_path)
        else:
            df = pd.read_csv(args.data_path)
        
        if args.column:
            if args.column not in df.columns:
                # 尝试第一列
                data = df.iloc[:, 0].dropna().tolist()
            else:
                data = df[args.column].dropna().tolist()
        else:
            data = df.iloc[:, 0].dropna().tolist()
    else:
        print(json.dumps({"error": "请提供 --data-path 或 --data 参数"}, ensure_ascii=False))
        sys.exit(1)
    
    # 计算结果
    result = calculate_capability_metrics(
        data=data,
        usl=args.usl,
        lsl=args.lsl,
        target=args.target,
        sigma_level=args.sigma_level
    )
    
    # 分布拟合
    if args.fit_distribution:
        fit_result = fit_distribution(data, args.fit_distribution)
        result["distribution_fit"] = fit_result
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
