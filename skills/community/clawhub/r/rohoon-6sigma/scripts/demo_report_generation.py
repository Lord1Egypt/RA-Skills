#!/usr/bin/env python3
"""
AIAG-VDA SPC 报告生成演示
- 生成正态和非正态数据
- 正态性检验 (Shapiro-Wilk)
- 根据检验结果自动选择报告格式
"""

import os
import numpy as np
from scipy import stats

# 导入报告生成器
from aiagvda_unified_report import (
    AIAGVDAReportGenerator,
    StudyInfo,
    Specification,
)

# 输出目录
OUTPUT_DIR = '/tmp/SPC_Reports'
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_normal_data(n=500, mean=100, std=1.0, seed=42):
    """生成正态分布数据"""
    np.random.seed(seed)
    return np.random.normal(mean, std, n)


def generate_nonnormal_data(n=500, case='mixed', seed=42):
    """生成非正态分布数据
    
    case:
        'mixed' - 混合分布 (两个正态分布叠加)
        'shifted' - 过程漂移 (前半段和后半段均值不同)
        'weibull' - Weibull 分布 (偏态)
    """
    np.random.seed(seed)
    
    if case == 'mixed':
        # 混合分布: 70% 来自 N(100, 1), 30% 来自 N(102, 0.5)
        n1 = int(n * 0.7)
        n2 = n - n1
        data1 = np.random.normal(100, 1.0, n1)
        data2 = np.random.normal(102, 0.5, n2)
        return np.concatenate([data1, data2])
    
    elif case == 'shifted':
        # 过程漂移: 前250个来自 N(100, 1), 后250个来自 N(101.5, 1)
        n1 = n // 2
        data1 = np.random.normal(100, 1.0, n1)
        data2 = np.random.normal(101.5, 1.0, n - n1)
        return np.concatenate([data1, data2])
    
    elif case == 'weibull':
        # Weibull 分布 (右偏)
        return np.random.weibull(2, n) * 2 + 98  # shape=2, shift=98
    
    else:
        return np.random.lognormal(mean=4.5, sigma=0.1, size=n)  # 对数正态


def test_normality(data, alpha=0.05):
    """
    正态性检验
    返回: (is_normal, p_value, test_name)
    """
    n = len(data)
    
    if n <= 5000:
        # Shapiro-Wilk 检验 (适用于 n ≤ 5000)
        stat, p = stats.shapiro(data)
        test_name = "Shapiro-Wilk"
    else:
        # Anderson-Darling 检验 (适用于大样本)
        result = stats.anderson(data, 'norm')
        stat = result.statistic
        # 5% 显著水平的临界值
        critical = result.critical_values[2]
        p = 0.05 if stat < critical else 0.01
        test_name = "Anderson-Darling"
    
    is_normal = p > alpha
    return is_normal, p, test_name


def analyze_dataset(name, data, spec, study_info=None):
    """
    分析数据集并生成相应报告
    """
    print(f"\n{'='*60}")
    print(f"数据集: {name}")
    print(f"{'='*60}")
    print(f"样本量: {len(data)}")
    print(f"均值: {np.mean(data):.4f}")
    print(f"标准差: {np.std(data, ddof=1):.4f}")
    print(f"最小值: {np.min(data):.4f}")
    print(f"最大值: {np.max(data):.4f}")
    
    # 正态性检验
    is_normal, p_value, test_name = test_normality(data)
    print(f"\n正态性检验 ({test_name}):")
    print(f"  P值: {p_value:.6f}")
    print(f"  结论: {'正态分布 ✓' if is_normal else '非正态分布 ✗'}")
    
    # 创建报告生成器
    gen = AIAGVDAReportGenerator(lang='zh')
    
    if is_normal:
        # 正态数据 -> Figure 12-1
        output_path = os.path.join(OUTPUT_DIR, f"{name}_Figure12-1_正态报告.pdf")
        gen.generate_figure12_1(output_path, data, spec, study_info)
        print(f"\n生成报告: {output_path}")
        return '12-1'
    else:
        # 非正态数据 -> Figure 12-2 和 Figure 12-3
        output_12_2 = os.path.join(OUTPUT_DIR, f"{name}_Figure12-2_非正态报告.pdf")
        output_12_3 = os.path.join(OUTPUT_DIR, f"{name}_Figure12-3_标准格式.pdf")
        
        gen.generate_figure12_2(output_12_2, data, spec, study_info)
        gen.generate_figure12_3(output_12_3, data, spec, study_info)
        
        print(f"\n生成报告:")
        print(f"  1. {output_12_2}")
        print(f"  2. {output_12_3}")
        return '12-2/12-3'


def main():
    """主函数"""
    print("="*60)
    print("AIAG-VDA SPC 报告生成演示")
    print("="*60)
    
    # 定义规格限
    spec = Specification(usl=103.0, lsl=97.0, target=100.0)
    
    # 研究信息
    study_info = StudyInfo(
        process_name="精密加工过程",
        machine_name="CNC-001",
        study_location="一号车间",
        part_name="传动轴",
        part_id="SHA-2026-001",
        characteristic_name="外径",
        study_remarks="过程能力研究",
        subgroup_size=5,
    )
    
    results = []
    
    # ========== 1. 正态数据 ==========
    print("\n" + "="*60)
    print("【场景 1】正态分布数据 - 稳定过程")
    print("="*60)
    
    normal_data = generate_normal_data(n=500, mean=100, std=0.8, seed=42)
    report_type = analyze_dataset("Normal_Stable", normal_data, spec, study_info)
    results.append(("Normal_Stable", "正态", 500, report_type))
    
    # ========== 2. 非正态数据 - 混合分布 ==========
    print("\n" + "="*60)
    print("【场景 2】非正态数据 - 混合分布 (多模态)")
    print("="*60)
    
    mixed_data = generate_nonnormal_data(n=500, case='mixed', seed=123)
    report_type = analyze_dataset("NonNormal_Mixed", mixed_data, spec, study_info)
    results.append(("NonNormal_Mixed", "混合分布", 500, report_type))
    
    # ========== 3. 非正态数据 - 过程漂移 ==========
    print("\n" + "="*60)
    print("【场景 3】非正态数据 - 过程漂移")
    print("="*60)
    
    shifted_data = generate_nonnormal_data(n=500, case='shifted', seed=456)
    report_type = analyze_dataset("NonNormal_Shifted", shifted_data, spec, study_info)
    results.append(("NonNormal_Shifted", "过程漂移", 500, report_type))
    
    # ========== 4. 非正态数据 - Weibull 分布 ==========
    print("\n" + "="*60)
    print("【场景 4】非正态数据 - Weibull 分布 (偏态)")
    print("="*60)
    
    weibull_data = generate_nonnormal_data(n=500, case='weibull', seed=789)
    report_type = analyze_dataset("NonNormal_Weibull", weibull_data, spec, study_info)
    results.append(("NonNormal_Weibull", "Weibull分布", 500, report_type))
    
    # ========== 5. 更大样本的正态数据 ==========
    print("\n" + "="*60)
    print("【场景 5】大样本正态数据 - 高产能过程")
    print("="*60)
    
    large_normal = generate_normal_data(n=875, mean=100, std=0.6, seed=999)
    report_type = analyze_dataset("Normal_Large", large_normal, spec, study_info)
    results.append(("Normal_Large", "正态(大样本)", 875, report_type))
    
    # ========== 汇总 ==========
    print("\n" + "="*60)
    print("📊 报告生成汇总")
    print("="*60)
    print(f"{'数据集':<25} {'类型':<15} {'样本量':<10} {'报告格式':<15}")
    print("-"*60)
    for name, dtype, n, rtype in results:
        print(f"{name:<25} {dtype:<15} {n:<10} {rtype:<15}")
    
    print(f"\n报告保存位置: {OUTPUT_DIR}")
    print(f"共生成 {len(results)} 组报告")
    
    # 列出所有生成的文件
    print("\n生成的 PDF 文件:")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.endswith('.pdf'):
            filepath = os.path.join(OUTPUT_DIR, f)
            size = os.path.getsize(filepath) / 1024
            print(f"  • {f} ({size:.1f} KB)")


if __name__ == '__main__':
    main()