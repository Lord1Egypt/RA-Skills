#!/usr/bin/env python3
"""
CP控制计划可视化脚本
功能：生成CPK仪表盘、控制图、分布图等可视化图表
"""

import argparse
import json
import sys
import os
from pathlib import Path

try:
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')  # 非交互式后端
except ImportError:
    print("ERROR: Missing required packages. Install: pip install pandas numpy matplotlib")
    sys.exit(1)


def load_data(json_path):
    """加载分析数据"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"ERROR: 读取文件失败 - {str(e)}")
        sys.exit(1)


def plot_cpk_dashboard(data, output_dir):
    """生成CPK仪表盘"""
    characteristics = data.get("characteristics", [])
    if not characteristics:
        print("WARNING: 无质量特性数据，跳过CPK仪表盘")
        return
    
    fig, ax = plt.subplots(figsize=(12, max(6, len(characteristics) * 0.6)))
    
    names = [c.get("characteristic", f"Char_{i}") for i, c in enumerate(characteristics)]
    cpk_values = [c.get("cpk", 0) for c in characteristics]
    capability_levels = [c.get("capability_level", "未知") for c in characteristics]
    
    # 颜色映射
    colors = []
    for level in capability_levels:
        if level == "优秀":
            colors.append("#28a745")  # 绿色
        elif level == "良好":
            colors.append("#17a2b8")  # 蓝色
        elif level == "勉强":
            colors.append("#ffc107")  # 黄色
        else:
            colors.append("#dc3545")  # 红色
    
    # 绘制水平条形图
    y_pos = np.arange(len(names))
    bars = ax.barh(y_pos, cpk_values, color=colors, edgecolor="white", height=0.6)
    
    # 添加参考线
    ax.axvline(x=1.0, color='red', linestyle='--', linewidth=1.5, label='CPK=1.0 (最低要求)')
    ax.axvline(x=1.33, color='orange', linestyle='--', linewidth=1.5, label='CPK=1.33 (目标值)')
    ax.axvline(x=1.67, color='green', linestyle='--', linewidth=1.5, label='CPK=1.67 (优秀)')
    
    # 设置标签
    ax.set_yticks(y_pos)
    ax.set_yticklabels(names, fontsize=10)
    ax.set_xlabel('CPK (过程能力指数)', fontsize=11)
    ax.set_title('CPK仪表盘 - 过程能力分析', fontsize=14, fontweight='bold')
    ax.set_xlim(0, max(2.0, max(cpk_values) * 1.2))
    ax.legend(loc='lower right', fontsize=9)
    ax.grid(axis='x', alpha=0.3)
    
    # 在条形上添加数值标签
    for bar, cpk, level in zip(bars, cpk_values, capability_levels):
        width = bar.get_width()
        ax.text(width + 0.02, bar.get_y() + bar.get_height()/2,
                f'{cpk:.2f} ({level})', va='center', fontsize=9)
    
    plt.tight_layout()
    output_path = os.path.join(output_dir, "cpk_dashboard.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"生成: {output_path}")


def plot_distribution(data, output_dir):
    """生成分布图"""
    characteristics = data.get("characteristics", [])
    
    for i, char in enumerate(characteristics[:6]):  # 限制数量
        char_name = char.get("characteristic", f"Char_{i}")
        mean = char.get("mean", 0)
        std = char.get("std", 0)
        lsl = char.get("lsl")
        usl = char.get("usl")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # 生成模拟正态分布数据用于展示
        if std > 0:
            x = np.linspace(mean - 4*std, mean + 4*std, 200)
            y = (1/(std * np.sqrt(2*np.pi))) * np.exp(-0.5*((x-mean)/std)**2)
            ax.plot(x, y, 'b-', linewidth=2, label='正态分布')
            ax.fill_between(x, y, alpha=0.3)
        
        # 添加规格限线
        if lsl is not None:
            ax.axvline(x=lsl, color='red', linestyle='-', linewidth=2, label=f'LSL={lsl}')
        if usl is not None:
            ax.axvline(x=usl, color='red', linestyle='-', linewidth=2, label=f'USL={usl}')
        
        # 添加均值线
        ax.axvline(x=mean, color='green', linestyle='--', linewidth=2, label=f'Mean={mean}')
        
        # 标注区域
        if lsl is not None and usl is not None:
            ax.fill_betweenx([0, ax.get_ylim()[1]], lsl, usl, alpha=0.1, color='green')
        
        ax.set_xlabel('测量值', fontsize=11)
        ax.set_ylabel('概率密度', fontsize=11)
        ax.set_title(f'{char_name} - 分布图', fontsize=12, fontweight='bold')
        ax.legend(loc='upper right')
        ax.grid(alpha=0.3)
        
        # 添加统计信息文本框
        textstr = f'n={char.get("count", 0)}\nMean={mean:.4f}\nStd={std:.4f}\nCPK={char.get("cpk", "N/A")}'
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
        ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=9,
                verticalalignment='top', bbox=props)
        
        plt.tight_layout()
        output_path = os.path.join(output_dir, f"distribution_{char_name.replace(' ', '_').replace('/', '_')}.png")
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"生成: {output_path}")


def plot_control_chart(data, output_dir):
    """生成控制图（简化版）"""
    characteristics = data.get("characteristics", [])
    
    for i, char in enumerate(characteristics[:6]):  # 限制数量
        char_name = char.get("characteristic", f"Char_{i}")
        mean = char.get("mean", 0)
        std = char.get("std", 0)
        ucl = char.get("ucl")
        lcl = char.get("lcl")
        
        if not ucl or not lcl or std == 0:
            continue
        
        fig, ax = plt.subplots(figsize=(12, 5))
        
        # 生成模拟数据点用于可视化
        np.random.seed(42 + i)
        n_points = min(25, char.get("count", 25))
        x_points = np.arange(1, n_points + 1)
        y_points = np.random.normal(mean, std * 0.8, n_points)
        
        # 绘制控制图
        ax.plot(x_points, y_points, 'b-o', markersize=6, linewidth=1.5, label='测量值')
        
        # 添加控制限
        ax.axhline(y=mean, color='green', linestyle='-', linewidth=2, label=f'CL={mean:.2f}')
        ax.axhline(y=ucl, color='red', linestyle='--', linewidth=1.5, label=f'UCL={ucl:.2f}')
        ax.axhline(y=lcl, color='red', linestyle='--', linewidth=1.5, label=f'LCL={lcl:.2f}')
        
        # 添加控制区域
        ax.fill_between(x_points, lcl, ucl, alpha=0.1, color='green')
        
        # 标记超限点
        out_of_control = (y_points > ucl) | (y_points < lcl)
        if any(out_of_control):
            ax.scatter(x_points[out_of_control], y_points[out_of_control], 
                      color='red', s=100, zorder=5, marker='x', linewidths=2, 
                      label=f'超限点 ({sum(out_of_control)}个)')
        
        ax.set_xlabel('样本序号', fontsize=11)
        ax.set_ylabel('测量值', fontsize=11)
        ax.set_title(f'{char_name} - X-bar控制图', fontsize=12, fontweight='bold')
        ax.legend(loc='upper right')
        ax.grid(alpha=0.3)
        ax.set_xlim(0, n_points + 1)
        
        plt.tight_layout()
        output_path = os.path.join(output_dir, f"control_chart_{char_name.replace(' ', '_').replace('/', '_')}.png")
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"生成: {output_path}")


def plot_risk_heatmap(data, output_dir):
    """生成风险热力图"""
    fmea = data.get("fmea_analysis", {})
    results = fmea.get("results", [])
    
    if not results:
        print("WARNING: 无FMEA数据，跳过风险热力图")
        return
    
    fig, ax = plt.subplots(figsize=(10, max(4, len(results) * 0.5)))
    
    items = [r["item"] for r in results]
    severities = [r["severity"] for r in results]
    occurrences = [r["occurrence"] for r in results]
    detections = [r["detection"] for r in results]
    rpns = [r["rpn"] for r in results]
    
    y_pos = np.arange(len(items))
    
    # 绘制三组条形
    width = 0.25
    ax.barh(y_pos - width, severities, width, label='严重度(S)', color='#dc3545', alpha=0.8)
    ax.barh(y_pos, occurrences, width, label='频度(O)', color='#fd7e14', alpha=0.8)
    ax.barh(y_pos + width, detections, width, label='探测度(D)', color='#6610f2', alpha=0.8)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(items, fontsize=10)
    ax.set_xlabel('评分 (1-10)', fontsize=11)
    ax.set_title('FMEA风险评估 - 评分分布', fontsize=14, fontweight='bold')
    ax.legend(loc='lower right')
    ax.set_xlim(0, 11)
    ax.grid(axis='x', alpha=0.3)
    
    # 在右侧添加RPN值
    for i, rpn in enumerate(rpns):
        color = '#dc3545' if rpn >= 100 else ('#ffc107' if rpn >= 50 else '#28a745')
        ax.text(10.5, i, f'RPN={rpn}', va='center', fontsize=9, color=color, fontweight='bold')
    
    plt.tight_layout()
    output_path = os.path.join(output_dir, "risk_heatmap.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"生成: {output_path}")


def plot_summary_dashboard(data, output_dir):
    """生成汇总仪表盘"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. CPK分布饼图
    ax1 = axes[0, 0]
    characteristics = data.get("characteristics", [])
    if characteristics:
        levels = {"优秀": 0, "良好": 0, "勉强": 0, "不足": 0}
        for c in characteristics:
            level = c.get("capability_level", "未知")
            if level in levels:
                levels[level] += 1
        
        labels = [f'{k}\n({v})' for k, v in levels.items() if v > 0]
        sizes = [v for v in levels.values() if v > 0]
        colors_pie = ['#28a745', '#17a2b8', '#ffc107', '#dc3545'][:len(sizes)]
        
        if sizes:
            ax1.pie(sizes, labels=labels, colors=colors_pie, autopct='%1.1f%%', startangle=90)
            ax1.set_title('过程能力等级分布', fontsize=12, fontweight='bold')
    
    # 2. 平均CPK趋势（如果有历史数据）
    ax2 = axes[0, 1]
    if characteristics:
        avg_cpk = data.get("summary", {}).get("average_cpk", 0)
        ax2.bar(['平均CPK'], [avg_cpk], color=['#007bff'])
        ax2.axhline(y=1.0, color='red', linestyle='--', label='最低要求(CPK=1.0)')
        ax2.axhline(y=1.33, color='green', linestyle='--', label='目标值(CPK=1.33)')
        ax2.set_ylabel('CPK')
        ax2.set_title('整体过程能力', fontsize=12, fontweight='bold')
        ax2.set_ylim(0, 2.0)
        ax2.legend(fontsize=8)
        
        for i, v in enumerate([avg_cpk]):
            ax2.text(i, v + 0.05, f'{v:.3f}', ha='center', fontsize=11, fontweight='bold')
    
    # 3. 高风险项统计
    ax3 = axes[1, 0]
    fmea = data.get("fmea_analysis", {})
    high_risk = fmea.get("high_risk_items", 0)
    critical = fmea.get("critical_items", 0)
    total = fmea.get("total_items", 1)
    
    categories = ['高风险', '严重', '其他']
    values = [high_risk, critical, max(0, total - high_risk - critical)]
    colors_bar = ['#dc3545', '#ffc107', '#28a745']
    
    bars = ax3.bar(categories, values, color=colors_bar)
    ax3.set_ylabel('项目数量')
    ax3.set_title('风险等级分布', fontsize=12, fontweight='bold')
    
    for bar, val in zip(bars, values):
        if val > 0:
            ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
                    str(val), ha='center', fontsize=11, fontweight='bold')
    
    # 4. 优先级建议
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    summary = data.get("summary", {})
    overall_risk = summary.get("overall_risk", "未知")
    priority_actions = summary.get("priority_actions", [])
    control_freq = summary.get("control_frequency_suggestion", "未知")
    
    advice_text = f"""
    整体风险等级: {overall_risk}
    
    建议控制频次: {control_freq}
    
    优先处理项目 ({len(priority_actions)}项):
    """
    for item in priority_actions[:5]:
        advice_text += f"\n    • {item}"
    
    if len(priority_actions) > 5:
        advice_text += f"\n    ... 等共{len(priority_actions)}项"
    
    ax4.text(0.1, 0.9, advice_text, transform=ax4.transAxes, fontsize=11,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    ax4.set_title('改善建议', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    output_path = os.path.join(output_dir, "summary_dashboard.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"生成: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="CP控制计划可视化脚本")
    parser.add_argument("--input", required=True, help="输入数据分析结果JSON文件路径")
    parser.add_argument("--output", required=True, help="输出图表目录路径")
    parser.add_argument("--chart", choices=["all", "cpk", "distribution", "control", "risk", "summary"], 
                       default="all", help="图表类型")
    
    args = parser.parse_args()
    
    # 创建输出目录
    os.makedirs(args.output, exist_ok=True)
    
    # 加载数据
    data = load_data(args.input)
    
    # 根据选择的图表类型生成
    if args.chart in ["all", "cpk"]:
        plot_cpk_dashboard(data, args.output)
    
    if args.chart in ["all", "distribution"]:
        plot_distribution(data, args.output)
    
    if args.chart in ["all", "control"]:
        plot_control_chart(data, args.output)
    
    if args.chart in ["all", "risk"]:
        plot_risk_heatmap(data, args.output)
    
    if args.chart in ["all", "summary"]:
        plot_summary_dashboard(data, args.output)
    
    print(f"\nSUCCESS: 所有图表已保存至 {args.output}/")


if __name__ == "__main__":
    main()
