#!/usr/bin/env python3
"""
质量控制图表生成脚本
支持控制图、直方图、能力图等多种可视化
"""

import argparse
import json
import sys
import os
from typing import Optional, List, Dict, Any
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import stats


# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial Unicode MS', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False


def load_data(data_path: str, column: str) -> np.ndarray:
    """加载数据文件"""
    import pandas as pd
    
    if data_path.endswith('.xlsx') or data_path.endswith('.xls'):
        df = pd.read_excel(data_path)
    else:
        df = pd.read_csv(data_path)
    
    if column and column in df.columns:
        return df[column].dropna().values
    else:
        return df.iloc[:, 0].dropna().values


def generate_control_chart(
    data: List[float],
    output_path: str,
    title: str = "X-bar Control Chart",
    ucl_factor: float = 3.0
) -> Dict[str, Any]:
    """
    生成X-bar控制图
    
    参数:
        data: 数据列表
        output_path: 输出路径
        title: 图表标题
        ucl_factor: 控制限因子(默认3σ)
    """
    data = np.array(data)
    n = len(data)
    
    mean = np.mean(data)
    std = np.std(data, ddof=1)
    
    ucl = mean + ucl_factor * std
    lcl = mean - ucl_factor * std
    
    # 检测异常点
    out_of_control = np.where((data > ucl) | (data < lcl))[0]
    
    # 绘图
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # 绘制数据和控制限
    ax.plot(range(n), data, 'b-o', markersize=4, label='Data')
    ax.axhline(y=mean, color='green', linestyle='-', linewidth=2, label=f'CL (μ={mean:.2f})')
    ax.axhline(y=ucl, color='red', linestyle='--', linewidth=1.5, label=f'UCL (μ+{ucl_factor}σ={ucl:.2f})')
    ax.axhline(y=lcl, color='red', linestyle='--', linewidth=1.5, label=f'LCL (μ-{ucl_factor}σ={lcl:.2f})')
    
    # 标记异常点
    if len(out_of_control) > 0:
        ax.scatter(out_of_control, data[out_of_control], color='red', s=100, zorder=5, marker='x', linewidths=2)
        ax.scatter(out_of_control, data[out_of_control], facecolors='none', edgecolors='red', s=200, zorder=4)
    
    ax.set_xlabel('Sample Number', fontsize=12)
    ax.set_ylabel('Measurement Value', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)
    
    # 添加统计信息
    stats_text = f'n={n}\nμ={mean:.4f}\nσ={std:.4f}\nUCL={ucl:.4f}\nLCL={lcl:.4f}'
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    return {
        "chart_path": output_path,
        "mean": round(mean, 6),
        "std": round(std, 6),
        "ucl": round(ucl, 6),
        "lcl": round(lcl, 6),
        "out_of_control_points": len(out_of_control),
        "out_of_control_indices": out_of_control.tolist()
    }


def generate_histogram(
    data: List[float],
    output_path: str,
    usl: Optional[float] = None,
    lsl: Optional[float] = None,
    title: str = "Process Histogram with Normal Distribution",
    fit_normal: bool = True
) -> Dict[str, Any]:
    """
    生成直方图(含正态分布拟合)
    
    参数:
        data: 数据列表
        output_path: 输出路径
        usl: 上规格限
        lsl: 下规格限
        title: 图表标题
        fit_normal: 是否拟合正态分布
    """
    data = np.array(data)
    n = len(data)
    
    mean = np.mean(data)
    std = np.std(data, ddof=1)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # 绘制直方图
    n_bins = min(30, max(10, int(np.sqrt(n))))
    counts, bins, patches = ax.hist(data, bins=n_bins, density=True, alpha=0.7, 
                                     color='steelblue', edgecolor='white', label='Data Histogram')
    
    # 拟合正态分布
    if fit_normal:
        x = np.linspace(min(data) - std, max(data) + std, 200)
        pdf = stats.norm.pdf(x, mean, std)
        ax.plot(x, pdf, 'r-', linewidth=2, label=f'Normal Fit (μ={mean:.2f}, σ={std:.2f})')
    
    # 绘制规格限
    y_max = ax.get_ylim()[1]
    if usl is not None:
        ax.axvline(x=usl, color='red', linestyle='--', linewidth=2, label=f'USL={usl}')
        ax.annotate('USL', xy=(usl, y_max * 0.9), fontsize=10, color='red')
    if lsl is not None:
        ax.axvline(x=lsl, color='red', linestyle='--', linewidth=2, label=f'LSL={lsl}')
        ax.annotate('LSL', xy=(lsl, y_max * 0.9), fontsize=10, color='red')
    
    # 超出规格的数据点着色
    if usl is not None:
        for i, (count, left, right) in enumerate(zip(counts, bins[:-1], bins[1:])):
            if left >= usl:
                patches[i].set_facecolor('red')
                patches[i].set_alpha(0.5)
    if lsl is not None:
        for i, (count, left, right) in enumerate(zip(counts, bins[:-1], bins[1:])):
            if right <= lsl:
                patches[i].set_facecolor('red')
                patches[i].set_alpha(0.5)
    
    ax.set_xlabel('Value', fontsize=12)
    ax.set_ylabel('Density', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)
    
    # 添加统计信息
    stats_text = f'n={n}\nμ={mean:.4f}\nσ={std:.4f}'
    if usl and lsl:
        out_of_spec = np.sum((data > usl) | (data < lsl))
        ppm = (out_of_spec / n) * 1e6
        stats_text += f'\nOut of Spec: {out_of_spec}\nPPM: {ppm:.0f}'
    
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    result = {
        "chart_path": output_path,
        "sample_size": n,
        "mean": round(mean, 6),
        "std": round(std, 6)
    }
    
    if usl and lsl:
        result["out_of_spec_count"] = int(np.sum((data > usl) | (data < lsl)))
        result["ppm"] = round((np.sum((data > usl) | (data < lsl)) / n) * 1e6, 2)
    
    return result


def generate_capability_chart(
    data: List[float],
    output_path: str,
    usl: Optional[float] = None,
    lsl: Optional[float] = None,
    title: str = "Process Capability Analysis"
) -> Dict[str, Any]:
    """
    生成过程能力图(组合图表)
    
    参数:
        data: 数据列表
        output_path: 输出路径
        usl: 上规格限
        lsl: 下规格限
        title: 图表标题
    """
    data = np.array(data)
    n = len(data)
    
    mean = np.mean(data)
    std = np.std(data, ddof=1)
    
    # 计算能力指数
    cp = cpk = cpu = cpl = pp = ppk = 0
    ppm_total = 0
    
    if usl and lsl:
        cp = (usl - lsl) / (6 * std) if std > 0 else 0
        cpu = (usl - mean) / (3 * std) if std > 0 else 0
        cpl = (mean - lsl) / (3 * std) if std > 0 else 0
        cpk = min(cpu, cpl)
        
        z_upper = (usl - mean) / std if std > 0 else 0
        z_lower = (lsl - mean) / std if std > 0 else 0
        ppm_total = ((1 - stats.norm.cdf(z_upper)) + stats.norm.cdf(z_lower)) * 1e6
    elif usl:
        cpu = (usl - mean) / (3 * std) if std > 0 else 0
        cpk = cpu
        ppm_total = (1 - stats.norm.cdf((usl - mean) / std)) * 1e6 if std > 0 else 0
    elif lsl:
        cpl = (mean - lsl) / (3 * std) if std > 0 else 0
        cpk = cpl
        ppm_total = stats.norm.cdf((lsl - mean) / std) * 1e6 if std > 0 else 0
    
    # 创建图表
    fig = plt.figure(figsize=(14, 10))
    
    # 1. 直方图(主图)
    ax1 = fig.add_subplot(2, 2, (1, 2))
    n_bins = min(30, max(10, int(np.sqrt(n))))
    counts, bins, patches = ax1.hist(data, bins=n_bins, density=True, alpha=0.7,
                                       color='steelblue', edgecolor='white')
    
    # 拟合曲线
    x = np.linspace(min(data) - std, max(data) + std, 200)
    pdf = stats.norm.pdf(x, mean, std)
    ax1.plot(x, pdf, 'r-', linewidth=2, label='Normal Distribution')
    
    # 规格限
    if usl:
        ax1.axvline(x=usl, color='darkred', linestyle='--', linewidth=2, label=f'USL={usl}')
    if lsl:
        ax1.axvline(x=lsl, color='darkred', linestyle='--', linewidth=2, label=f'LSL={lsl}')
    if usl and lsl:
        ax1.axvline(x=(usl + lsl) / 2, color='green', linestyle=':', linewidth=2, label=f'Target={(usl+lsl)/2:.2f}')
    
    ax1.axvline(x=mean, color='blue', linestyle='-', linewidth=2, label=f'Mean={mean:.2f}')
    ax1.set_xlabel('Value', fontsize=11)
    ax1.set_ylabel('Density', fontsize=11)
    ax1.set_title('Process Distribution with Specification Limits', fontsize=12, fontweight='bold')
    ax1.legend(loc='upper right', fontsize=9)
    ax1.grid(True, alpha=0.3)
    
    # 2. 能力指标表格
    ax2 = fig.add_subplot(2, 2, 3)
    ax2.axis('off')
    
    table_data = [
        ['Metric', 'Value'],
        ['Sample Size', f'{n}'],
        ['Mean (μ)', f'{mean:.4f}'],
        ['Std Dev (σ)', f'{std:.4f}'],
    ]
    
    if usl and lsl:
        table_data.extend([
            ['USL', f'{usl}'],
            ['LSL', f'{lsl}'],
            ['Target', f'{(usl+lsl)/2:.2f}'],
            ['CP', f'{cp:.4f}'],
            ['CPK', f'{cpk:.4f}'],
            ['CPU', f'{cpu:.4f}'],
            ['CPL', f'{cpl:.4f}'],
            ['PPM', f'{ppm_total:.0f}'],
        ])
    elif usl:
        table_data.extend([
            ['USL', f'{usl}'],
            ['CPU', f'{cpu:.4f}'],
            ['PPM', f'{ppm_total:.0f}'],
        ])
    elif lsl:
        table_data.extend([
            ['LSL', f'{lsl}'],
            ['CPL', f'{cpl:.4f}'],
            ['PPM', f'{ppm_total:.0f}'],
        ])
    
    table = ax2.table(cellText=table_data, loc='center', cellLoc='center',
                      colWidths=[0.4, 0.4])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.5)
    
    # 设置表头样式
    for j in range(2):
        table[(0, j)].set_facecolor('#4472C4')
        table[(0, j)].set_text_props(color='white', fontweight='bold')
    
    ax2.set_title('Capability Indices', fontsize=12, fontweight='bold', pad=20)
    
    # 3. 能力等级图
    ax3 = fig.add_subplot(2, 2, 4)
    ax3.axis('off')
    
    # 能力等级
    levels = [
        ('A', '≥ 2.0', 'Excellent', '#00FF00'),
        ('B', '1.67 - 2.0', 'Very Good', '#92D050'),
        ('C', '1.33 - 1.67', 'Good', '#FFFF00'),
        ('D', '1.0 - 1.33', 'Adequate', '#FFC000'),
        ('E', '0.67 - 1.0', 'Poor', '#FF6600'),
        ('F', '< 0.67', 'Very Poor', '#FF0000'),
    ]
    
    current_cpk = cpk if cpk > 0 else (cpu if usl and not lsl else cpl if lsl and not usl else 0)
    
    y_pos = 0.9
    for letter, range_text, level, color in levels:
        # 判断当前CPK属于哪个等级
        is_current = False
        if letter == 'A' and current_cpk >= 2.0:
            is_current = True
        elif letter == 'B' and 1.67 <= current_cpk < 2.0:
            is_current = True
        elif letter == 'C' and 1.33 <= current_cpk < 1.67:
            is_current = True
        elif letter == 'D' and 1.0 <= current_cpk < 1.33:
            is_current = True
        elif letter == 'E' and 0.67 <= current_cpk < 1.0:
            is_current = True
        elif letter == 'F' and current_cpk < 0.67:
            is_current = True
        
        bg_color = color if not is_current else '#000000'
        text_color = 'white' if is_current else 'black'
        
        rect = mpatches.FancyBboxPatch((0.05, y_pos - 0.08), 0.15, 0.12,
                                        boxstyle="round,pad=0.02", facecolor=bg_color,
                                        transform=ax3.transAxes)
        ax3.add_patch(rect)
        ax3.text(0.125, y_pos - 0.02, letter, transform=ax3.transAxes,
                fontsize=14, fontweight='bold', ha='center', va='center', color=text_color)
        ax3.text(0.25, y_pos - 0.02, f'{range_text}', transform=ax3.transAxes,
                fontsize=10, ha='left', va='center')
        ax3.text(0.55, y_pos - 0.02, level, transform=ax3.transAxes,
                fontsize=10, ha='left', va='center', fontweight='bold' if is_current else 'normal')
        
        if is_current:
            ax3.annotate('', xy=(0.75, y_pos - 0.02), xytext=(0.65, y_pos - 0.02),
                        xycoords='axes fraction', fontsize=10, fontweight='bold', color='red')
        
        y_pos -= 0.15
    
    ax3.set_xlim(0, 1)
    ax3.set_ylim(0, 1)
    ax3.set_title(f'Capability Level (Current CPK = {current_cpk:.4f})', fontsize=12, fontweight='bold', pad=20)
    
    plt.suptitle(title, fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    return {
        "chart_path": output_path,
        "cp": round(cp, 4),
        "cpk": round(cpk, 4),
        "cpu": round(cpu, 4),
        "cpl": round(cpl, 4),
        "ppm": round(ppm_total, 2),
        "mean": round(mean, 6),
        "std": round(std, 6),
        "level": _get_capability_level(cpk if cpk > 0 else (cpu if usl and not lsl else cpl))
    }


def _get_capability_level(cpk: float) -> str:
    """获取能力等级"""
    if cpk >= 2.0:
        return "A (Excellent)"
    elif cpk >= 1.67:
        return "B (Very Good)"
    elif cpk >= 1.33:
        return "C (Good)"
    elif cpk >= 1.0:
        return "D (Adequate)"
    elif cpk >= 0.67:
        return "E (Poor)"
    else:
        return "F (Very Poor)"


def main():
    parser = argparse.ArgumentParser(description='质量控制图表生成脚本')
    parser.add_argument('--chart-type', type=str, required=True,
                        choices=['control', 'histogram', 'capability'],
                        help='图表类型')
    parser.add_argument('--data-path', type=str, required=True, help='数据文件路径')
    parser.add_argument('--column', type=str, help='数据列名')
    parser.add_argument('--usl', type=float, help='上规格限')
    parser.add_argument('--lsl', type=float, help='下规格限')
    parser.add_argument('--title', type=str, help='图表标题')
    parser.add_argument('--output', type=str, required=True, help='输出路径')
    parser.add_argument('--data', type=str, help='直接输入的JSON数组数据')
    
    args = parser.parse_args()
    
    # 确保输出目录存在
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 获取数据
    if args.data:
        import ast
        try:
            data = ast.literal_eval(args.data)
        except:
            data = json.loads(args.data)
    else:
        data = load_data(args.data_path, args.column).tolist()
    
    # 生成图表
    title = args.title or f'{args.chart_type.capitalize()} Chart'
    
    if args.chart_type == 'control':
        result = generate_control_chart(data, args.output, title)
    elif args.chart_type == 'histogram':
        result = generate_histogram(data, args.output, args.usl, args.lsl, title)
    elif args.chart_type == 'capability':
        if not args.usl and not args.lsl:
            print(json.dumps({"error": "能力图需要提供 --usl 或 --lsl 参数"}, ensure_ascii=False))
            sys.exit(1)
        result = generate_capability_chart(data, args.output, args.usl, args.lsl, title)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
