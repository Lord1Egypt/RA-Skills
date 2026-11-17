#!/usr/bin/env python3
"""
ESG Visualizer - ESG数据可视化工具
支持多维度图表生成：柱状图、饼图、趋势图、雷达图、热力图等
"""

import argparse
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from pathlib import Path
from datetime import datetime

# 设置中文字体支持
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False


# 颜色配置
COLORS = {
    'environmental': '#2E7D32',  # 绿色
    'social': '#1565C0',         # 蓝色
    'governance': '#7B1FA2',     # 紫色
    'positive': '#4CAF50',
    'negative': '#F44336',
    'neutral': '#9E9E9E'
}


def load_data(input_file):
    """加载ESG数据"""
    if input_file.endswith('.json'):
        with open(input_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    elif input_file.endswith('.csv'):
        return pd.read_csv(input_file).to_dict()
    else:
        raise ValueError(f"不支持的文件格式: {input_file}")


def create_bar_chart(data, dimension, output_file):
    """生成柱状图"""
    dim_data = data.get('dimensions', {}).get(dimension, {})
    
    if not dim_data:
        return None
    
    metrics = list(dim_data.keys())
    values = [float(dim_data[m].get('value', 0)) for m in metrics]
    names = [dim_data[m].get('name', m) for m in metrics]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(names, values, color=COLORS.get(dimension, '#2196F3'))
    
    ax.set_ylabel('数值', fontsize=12)
    ax.set_title(f'{dimension.upper()} 指标数据', fontsize=14, fontweight='bold')
    ax.tick_params(axis='x', rotation=45)
    
    # 添加数值标签
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values)*0.01,
                f'{val:.2f}', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()
    
    return output_file


def create_pie_chart(data, dimension, output_file):
    """生成饼图"""
    dim_data = data.get('dimensions', {}).get(dimension, {})
    
    if not dim_data:
        return None
    
    # 筛选有数据的指标
    valid_data = {k: v for k, v in dim_data.items() if v.get('value') is not None}
    
    if len(valid_data) < 2:
        return None
    
    labels = [v.get('name', k) for k, v in valid_data.items()]
    values = [float(v.get('value', 0)) for v in valid_data.values()]
    
    fig, ax = plt.subplots(figsize=(8, 8))
    colors_list = plt.cm.Set3(range(len(labels)))
    
    wedges, texts, autotexts = ax.pie(values, labels=labels, autopct='%1.1f%%',
                                       colors=colors_list, startangle=90)
    
    ax.set_title(f'{dimension.upper()} 维度构成', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()
    
    return output_file


def create_radar_chart(data, output_file):
    """生成雷达图 - 综合展示三个维度"""
    dimensions = ['environmental', 'social', 'governance']
    dim_labels = ['环境(E)', '社会(S)', '治理(G)']
    
    # 计算各维度得分（基于已提供指标的完成度）
    scores = []
    for dim in dimensions:
        dim_data = data.get('dimensions', {}).get(dim, {})
        if dim_data:
            valid_count = sum(1 for v in dim_data.values() if v.get('value') is not None)
            total_count = len(dim_data)
            scores.append((valid_count / total_count) * 100 if total_count > 0 else 0)
        else:
            scores.append(0)
    
    # 雷达图
    angles = [n / float(len(dim_labels)) * 2 * 3.14159 for n in range(len(dim_labels))]
    angles += angles[:1]  # 闭合
    
    scores += scores[:1]  # 闭合
    
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.plot(angles, scores, 'o-', linewidth=2, color=COLORS['environmental'])
    ax.fill(angles, scores, alpha=0.25, color=COLORS['environmental'])
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(dim_labels, fontsize=12)
    ax.set_ylim(0, 100)
    ax.set_title('ESG综合评分雷达图', fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()
    
    return output_file


def create_trend_chart(data, output_file):
    """生成趋势图 - 展示指标变化"""
    # 按报告期分组的数据趋势
    periods_data = {}
    
    for dim_name, dim_data in data.get('dimensions', {}).items():
        for metric_id, metric_info in dim_data.items():
            period = str(metric_info.get('period', ''))
            if period and period not in periods_data:
                periods_data[period] = {}
            if period:
                periods_data[period][dim_name] = metric_info.get('value', 0)
    
    if len(periods_data) < 2:
        return None
    
    # 生成多指标趋势图
    fig, ax = plt.subplots(figsize=(12, 6))
    
    dimensions = ['environmental', 'social', 'governance']
    dim_labels = {'environmental': '环境', 'social': '社会', 'governance': '治理'}
    
    for dim in dimensions:
        values = []
        periods = sorted(periods_data.keys())
        for p in periods:
            val = periods_data[p].get(dim, 0)
            values.append(float(val) if val else 0)
        
        if any(values):
            ax.plot(periods, values, 'o-', label=dim_labels.get(dim, dim),
                   color=COLORS.get(dim, '#2196F3'), linewidth=2, markersize=8)
    
    ax.set_xlabel('报告期', fontsize=12)
    ax.set_ylabel('指标值', fontsize=12)
    ax.set_title('ESG指标趋势分析', fontsize=14, fontweight='bold')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()
    
    return output_file


def create_comparison_chart(data, output_file):
    """生成对比图 - 与行业基准对比"""
    # 与行业平均值的对比
    industry_avg = {
        'environmental': 65,
        'social': 60,
        'governance': 55
    }
    
    dimensions = ['environmental', 'social', 'governance']
    dim_labels = {'environmental': '环境', 'social': '社会', 'governance': '治理'}
    
    # 计算实际得分
    actual_scores = []
    benchmark_scores = []
    labels = []
    
    for dim in dimensions:
        dim_data = data.get('dimensions', {}).get(dim, {})
        if dim_data:
            valid_count = sum(1 for v in dim_data.values() if v.get('value') is not None)
            total_count = len(dim_data)
            score = (valid_count / total_count) * 100 if total_count > 0 else 0
        else:
            score = 0
        
        actual_scores.append(score)
        benchmark_scores.append(industry_avg.get(dim, 50))
        labels.append(dim_labels.get(dim, dim))
    
    x = range(len(labels))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars1 = ax.bar([i - width/2 for i in x], actual_scores, width, label='实际得分', 
                   color=COLORS['environmental'])
    bars2 = ax.bar([i + width/2 for i in x], benchmark_scores, width, label='行业基准',
                   color=COLORS['neutral'], alpha=0.7)
    
    ax.set_ylabel('得分', fontsize=12)
    ax.set_title('ESG各维度得分与行业基准对比', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    ax.set_ylim(0, 100)
    
    # 添加数值标签
    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{bar.get_height():.1f}', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()
    
    return output_file


def generate_all_charts(input_file, output_dir='.'):
    """
    生成所有可视化图表
    
    Args:
        input_file: ESG数据文件(JSON)
        output_dir: 输出目录
    """
    data = load_data(input_file)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    results = {
        "generation_time": datetime.now().isoformat(),
        "charts": []
    }
    
    # 为每个维度生成图表
    for dimension in ['environmental', 'social', 'governance']:
        # 柱状图
        bar_file = output_dir / f'{dimension}_bar.png'
        chart_path = create_bar_chart(data, dimension, bar_file)
        if chart_path:
            results['charts'].append({"type": "bar", "dimension": dimension, "file": str(chart_path)})
        
        # 饼图
        pie_file = output_dir / f'{dimension}_pie.png'
        chart_path = create_pie_chart(data, dimension, pie_file)
        if chart_path:
            results['charts'].append({"type": "pie", "dimension": dimension, "file": str(chart_path)})
    
    # 综合图表
    radar_file = output_dir / 'esg_radar.png'
    chart_path = create_radar_chart(data, radar_file)
    if chart_path:
        results['charts'].append({"type": "radar", "file": str(chart_path)})
    
    trend_file = output_dir / 'esg_trend.png'
    chart_path = create_trend_chart(data, trend_file)
    if chart_path:
        results['charts'].append({"type": "trend", "file": str(chart_path)})
    
    comparison_file = output_dir / 'esg_comparison.png'
    chart_path = create_comparison_chart(data, comparison_file)
    if chart_path:
        results['charts'].append({"type": "comparison", "file": str(chart_path)})
    
    return results


def main():
    parser = argparse.ArgumentParser(description='ESG数据可视化工具')
    parser.add_argument('--input', '-i', required=True, help='ESG数据文件(JSON)')
    parser.add_argument('--output-dir', '-o', default='.', help='图表输出目录')
    parser.add_argument('--type', '-t', choices=['bar', 'pie', 'radar', 'trend', 'comparison', 'all'],
                       default='all', help='图表类型')
    
    args = parser.parse_args()
    
    if args.type == 'all':
        result = generate_all_charts(args.input, args.output_dir)
    else:
        data = load_data(args.input)
        output_file = Path(args.output_dir) / f'esg_{args.type}.png'
        
        if args.type == 'bar':
            for dim in ['environmental', 'social', 'governance']:
                create_bar_chart(data, dim, str(output_file).replace('.png', f'_{dim}.png'))
        elif args.type == 'radar':
            create_radar_chart(data, output_file)
        elif args.type == 'trend':
            create_trend_chart(data, output_file)
        
        result = {"status": "success", "output": str(output_file)}
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
