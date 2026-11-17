#!/usr/bin/env python3
"""
DOE实验设计生成器
支持全因子设计和部分因子设计(2^(k-p))
"""

import argparse
import itertools
import json
import math
import sys
from typing import List, Dict, Tuple

try:
    import pandas as pd
except ImportError:
    print(json.dumps({
        "status": "error",
        "message": "pandas not installed. Run: pip install pandas>=1.5.0"
    }))
    sys.exit(1)


def generate_full_factorial(num_factors: int, num_levels: int) -> Tuple[List[Dict], List[str]]:
    """
    生成全因子实验方案
    
    Args:
        num_factors: 因子数量
        num_levels: 每个因子的水平数
    
    Returns:
        实验数据列表, 因子名称列表
    """
    # 生成因子名称
    factors = [f"Factor_{chr(65+i)}" for i in range(num_factors)]  # A, B, C...
    
    # 生成所有水平组合(Cartesian product)
    levels = list(range(num_levels))
    combinations = list(itertools.product(levels, repeat=num_factors))
    
    # 构建实验数据
    experiments = []
    for run_id, combo in enumerate(combinations, start=1):
        exp = {"Run": run_id}
        for i, factor in enumerate(factors):
            exp[factor] = combo[i]
        experiments.append(exp)
    
    return experiments, factors


def get_fractional_design_generator(num_factors: int, num_runs: int) -> List[int]:
    """
    获取部分因子设计的生成器(用于2^(k-p)设计)
    基于标准生成器关系
    
    Args:
        num_factors: 因子总数
        num_runs: 实验次数
    
    Returns:
        生成器列表
    """
    # 确定需要定义的生成器数量
    p = int(math.log2(num_runs))  # p = k - log2(runs)
    base_factors = int(math.log2(num_runs))  # 基础因子数
    
    # 标准生成器(简化版本,适用于常规分辨率IV设计)
    generators = []
    
    # 常用2^(k-p)设计生成器表(部分)
    standard_designs = {
        (4, 8): [3, 4, 12],      # 2^(4-1): 8 runs
        (5, 8): [3, 4, 12],      # 2^(5-2): 8 runs (分辨率III)
        (5, 16): [3, 4, 12],     # 2^(5-1): 16 runs
        (6, 16): [3, 4, 5, 23],  # 2^(6-1): 16 runs
        (6, 32): [3, 4, 12],     # 2^(6-1): 32 runs
        (7, 16): [3, 4, 12],     # 2^(7-3): 16 runs
        (7, 32): [3, 4, 5, 23],  # 2^(7-2): 32 runs
        (7, 64): [3, 4, 12],     # 2^(7-1): 64 runs
        (8, 32): [3, 4, 5, 23],  # 2^(8-2): 32 runs
        (8, 64): [3, 4, 5, 23],  # 2^(8-1): 64 runs
    }
    
    key = (num_factors, num_runs)
    if key in standard_designs:
        return standard_designs[key]
    
    # 动态生成(基于分辨率)
    num_gen = int(math.log2(num_runs)) - int(math.log2(num_runs / (2 ** (num_factors - int(math.log2(num_runs))))))
    
    # 使用简化的生成规则
    for i in range(1, num_gen + 1):
        generators.append(i * (num_gen + 1))
    
    return generators[:num_gen] if generators else [3]


def generate_fractional_factorial(num_factors: int, resolution: int = 4) -> Tuple[List[Dict], List[str]]:
    """
    生成部分因子实验方案(2^(k-p)设计)
    
    Args:
        num_factors: 因子总数
        resolution: 设计分辨率(3=III, 4=IV, 5=V)
    
    Returns:
        实验数据列表, 因子名称列表
    """
    # 计算需要的实验次数
    # 分辨率III: 2^(k-2), 分辨率IV: 2^(k-1), 分辨率V: 2^(k-1)大样本
    if resolution == 3:
        # 分辨率III: 2^(k-2)
        p = 2
        num_runs = 2 ** (num_factors - 2)
    elif resolution == 4:
        # 分辨率IV: 2^(k-1)
        p = 1
        num_runs = 2 ** (num_factors - 1)
    else:
        # 分辨率V+: 需要更大设计
        p = 0
        num_runs = 2 ** num_factors
    
    # 确保最小实验次数
    num_runs = max(num_runs, 4)
    
    # 生成基础因子(用num_runs次数)
    base_factors = int(math.log2(num_runs))
    factors = [f"Factor_{chr(65+i)}" for i in range(num_factors)]
    
    # 生成基础设计矩阵(满因子)
    base_design = []
    for i in range(num_runs):
        run = []
        for j in range(base_factors):
            run.append((i >> j) & 1)
        base_design.append(run)
    
    # 定义设计生成器(确定哪些是基础因子)
    # 默认前base_factors个是基础因子，其余是派生因子
    gen_matrix = []
    
    if num_factors > base_factors:
        # 生成派生因子的定义
        # 使用标准混淆关系
        for i in range(base_factors, num_factors):
            # 简化: 派生因子 = 基础因子的某些组合
            # 常见规则: 派生因子 = 前几个基础因子的异或
            gen_row = [1 if j == (i - base_factors) % base_factors else 0 for j in range(base_factors)]
            # 加入更多混淆以提高分辨率
            if resolution == 4:
                gen_row[(i - base_factors + 1) % base_factors] ^= 1
            gen_matrix.append(gen_row)
    
    # 构建完整设计
    experiments = []
    for run_idx, base_run in enumerate(base_design, start=1):
        exp = {"Run": run_idx}
        
        # 添加基础因子
        for j in range(min(base_factors, num_factors)):
            exp[factors[j]] = base_run[j]
        
        # 添加派生因子
        for i, gen_row in enumerate(gen_matrix):
            factor_idx = base_factors + i
            if factor_idx < num_factors:
                # 计算派生因子的值(异或组合)
                value = 0
                for j, coeff in enumerate(gen_row):
                    if coeff and j < len(base_run):
                        value ^= base_run[j]
                exp[factors[factor_idx]] = value
        
        experiments.append(exp)
    
    return experiments, factors[:num_factors]


def save_to_csv(experiments: List[Dict], output_path: str, factors: List[str]) -> None:
    """
    保存实验方案到CSV文件
    """
    df = pd.DataFrame(experiments)
    
    # 确保列顺序: Run, Factor_A, Factor_B, ...
    cols = ["Run"] + factors
    df = df[cols]
    
    df.to_csv(output_path, index=False)


def main():
    parser = argparse.ArgumentParser(description="DOE实验设计生成器")
    subparsers = parser.add_subparsers(dest="command", help="设计类型")
    
    # 全因子设计子命令
    full_parser = subparsers.add_parser("full", help="全因子设计")
    full_parser.add_argument("--factors", type=int, required=True, help="因子数量")
    full_parser.add_argument("--levels", type=int, required=True, help="每个因子的水平数")
    full_parser.add_argument("--output", type=str, default="full_factorial.csv", help="输出CSV文件路径")
    
    # 部分因子设计子命令
    frac_parser = subparsers.add_parser("fractional", help="部分因子设计(2^(k-p))")
    frac_parser.add_argument("--base-levels", type=int, default=2, help="基础水平数(默认2)")
    frac_parser.add_argument("--num-factors", type=int, required=True, help="因子总数")
    frac_parser.add_argument("--resolution", type=int, default=4, choices=[3, 4, 5], help="设计分辨率(3=III, 4=IV, 5=V)")
    frac_parser.add_argument("--output", type=str, default="fractional_factorial.csv", help="输出CSV文件路径")
    
    args = parser.parse_args()
    
    if args.command == "full":
        # 全因子设计
        if args.factors < 1 or args.levels < 2:
            print(json.dumps({
                "status": "error",
                "message": "因子数>=1, 水平数>=2"
            }))
            sys.exit(1)
        
        experiments, factors = generate_full_factorial(args.factors, args.levels)
        save_to_csv(experiments, args.output, factors)
        
        result = {
            "status": "success",
            "design_type": "full_factorial",
            "num_factors": args.factors,
            "num_levels": args.levels,
            "num_runs": len(experiments),
            "output_file": args.output,
            "factors": factors
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    elif args.command == "fractional":
        # 部分因子设计
        if args.num_factors < 2:
            print(json.dumps({
                "status": "error",
                "message": "因子数>=2"
            }))
            sys.exit(1)
        
        experiments, factors = generate_fractional_factorial(args.num_factors, args.resolution)
        save_to_csv(experiments, args.output, factors)
        
        result = {
            "status": "success",
            "design_type": "fractional_factorial",
            "design": f"2^{args.num_factors}-{int(math.log2(len(experiments))) if len(experiments) > 1 else 0}",
            "resolution": f"resolution_{['III', 'IV', 'V'][args.resolution-3]}",
            "num_factors": args.num_factors,
            "num_runs": len(experiments),
            "output_file": args.output,
            "factors": factors
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
