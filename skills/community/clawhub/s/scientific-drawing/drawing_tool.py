#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
科研绘图工具 - 基金申请/论文写作专用
支持：技术路线图、流程图、原理图、架构图、数据可视化
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch, ConnectionPatch
import numpy as np
from pathlib import Path

# 配置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

OUTPUT_DIR = Path("D:/Personal/OpenClaw/figures")
OUTPUT_DIR.mkdir(exist_ok=True)


def draw_flowchart(title, steps, connections=None, 
                   orientation='horizontal', 
                   colors=None,
                   output_name='flowchart.png'):
    """
    绘制流程图/技术路线图
    
    Parameters
    ----------
    title : str
        图表标题
    steps : list
        步骤列表，每个元素为字符串或字典 {'text': 'xxx', 'color': '#xxx'}
    connections : list, optional
        连接关系，默认顺序连接
    orientation : str
        'horizontal' 或 'vertical'
    colors : list, optional
        配色方案
    output_name : str
        输出文件名
    """
    
    n = len(steps)
    
    # 默认配色
    if colors is None:
        colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E', '#577590']
    
    # 创建画布
    if orientation == 'horizontal':
        fig, ax = plt.subplots(figsize=(14, 6))
        x_step = 1.0 / (n + 1)
        y_center = 0.5
    else:
        fig, ax = plt.subplots(figsize=(8, 12))
        y_step = 1.0 / (n + 1)
        x_center = 0.5
    
    # 绘制方框
    boxes = []
    for i, step in enumerate(steps):
        if isinstance(step, dict):
            text = step.get('text', str(step))
            color = step.get('color', colors[i % len(colors)])
        else:
            text = str(step)
            color = colors[i % len(colors)]
        
        if orientation == 'horizontal':
            x = x_step * (i + 1)
            y = y_center
            width = x_step * 0.6
            height = 0.25
            box = patches.FancyBboxPatch(
                (x - width/2, y - height/2), width, height,
                boxstyle="round,pad=0.05,rounding_size=0.02",
                linewidth=2, edgecolor='#333333', facecolor=color,
                alpha=0.9
            )
            ax.text(x, y, text, ha='center', va='center', fontsize=11, 
                   fontweight='bold', color='white', wrap=True)
        else:
            x = x_center
            y = y_step * (n - i)
            width = 0.6
            height = y_step * 0.5
            box = patches.FancyBboxPatch(
                (x - width/2, y - height/2), width, height,
                boxstyle="round,pad=0.05,rounding_size=0.02",
                linewidth=2, edgecolor='#333333', facecolor=color,
                alpha=0.9
            )
            ax.text(x, y, text, ha='center', va='center', fontsize=11,
                   fontweight='bold', color='white', wrap=True)
        
        ax.add_patch(box)
        boxes.append(box)
    
    # 绘制连接箭头
    if connections is None:
        connections = [(i, i+1) for i in range(n-1)]
    
    for start, end in connections:
        if orientation == 'horizontal':
            x1 = x_step * (start + 1) + x_step * 0.35
            y1 = y_center
            x2 = x_step * (end + 1) - x_step * 0.35
            y2 = y_center
        else:
            x1 = x_center
            y1 = y_step * (n - start) - y_step * 0.3
            x2 = x_center
            y2 = y_step * (n - end) + y_step * 0.3
        
        arrow = FancyArrowPatch(
            (x1, y1), (x2, y2),
            arrowstyle='->', mutation_scale=20,
            linewidth=2, color='#333333',
            linestyle='-'
        )
        ax.add_patch(arrow)
    
    # 设置标题
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    
    # 设置坐标轴
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_aspect('equal')
    
    # 保存
    output_path = OUTPUT_DIR / output_name
    plt.savefig(output_path, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    
    print(f"[OK] Flowchart saved: {output_path}")
    return str(output_path)


def draw_architecture(title, modules, hierarchy_levels=None, 
                      colors=None, output_name='architecture.png'):
    """
    绘制系统架构图/层级图
    
    Parameters
    ----------
    title : str
        图表标题
    modules : list of lists
        层级模块，每个子列表代表一层
    hierarchy_levels : list, optional
        层级名称
    colors : list, optional
        每层的配色
    output_name : str
        输出文件名
    """
    
    n_levels = len(modules)
    
    if colors is None:
        colors = ['#2E86AB', '#5D8AA8', '#87CEEB', '#B0E0E6']
    
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # 绘制层级
    for level_idx, level_modules in enumerate(modules):
        n_modules = len(level_modules)
        y_pos = 1.0 - (level_idx + 0.5) / (n_levels + 1)
        
        # 绘制层级背景
        if hierarchy_levels:
            ax.text(0.02, y_pos, hierarchy_levels[level_idx], 
                   fontsize=10, fontweight='bold', 
                   va='center', ha='left',
                   bbox=dict(boxstyle='round', facecolor='#f0f0f0', alpha=0.5))
        
        # 绘制模块
        x_step = 1.0 / (n_modules + 1)
        color = colors[level_idx % len(colors)]
        
        for mod_idx, module in enumerate(level_modules):
            x_pos = x_step * (mod_idx + 1)
            width = x_step * 0.7
            height = 0.12
            
            box = patches.FancyBboxPatch(
                (x_pos - width/2, y_pos - height/2), width, height,
                boxstyle="round,pad=0.05,rounding_size=0.02",
                linewidth=2, edgecolor='#333333', facecolor=color,
                alpha=0.9
            )
            ax.add_patch(box)
            
            # 模块文字
            ax.text(x_pos, y_pos, str(module), ha='center', va='center',
                   fontsize=10, fontweight='bold', color='white', wrap=True)
    
    # 标题
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    
    # 设置
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_aspect('equal')
    
    # 保存
    output_path = OUTPUT_DIR / output_name
    plt.savefig(output_path, dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    
    print(f"[OK] Architecture saved: {output_path}")
    return str(output_path)


def draw_timeline(title, tasks, start_date, end_date, 
                  colors=None, output_name='timeline.png'):
    """
    绘制甘特图/时间线图
    
    Parameters
    ----------
    title : str
        图表标题
    tasks : list of dict
        任务列表，每个任务包含 {'name': 'xxx', 'start': '2024-01', 'end': '2024-06'}
    start_date : str
        开始日期 'YYYY-MM'
    end_date : str
        结束日期 'YYYY-MM'
    colors : list, optional
        配色方案
    output_name : str
        输出文件名
    """
    
    from datetime import datetime
    
    if colors is None:
        colors = ['#2E86AB', '#A23B72', '#F18F01', '#6A994E', '#577590']
    
    # 解析日期
    start = datetime.strptime(start_date, '%Y-%m')
    end = datetime.strptime(end_date, '%Y-%m')
    total_months = (end.year - start.year) * 12 + (end.month - start.month) + 1
    
    fig, ax = plt.subplots(figsize=(14, len(tasks) * 0.8 + 2))
    
    # 绘制任务条
    for idx, task in enumerate(tasks):
        task_start = datetime.strptime(task['start'], '%Y-%m')
        task_end = datetime.strptime(task['end'], '%Y-%m')
        
        start_offset = (task_start.year - start.year) * 12 + (task_start.month - start.month)
        duration = (task_end.year - task_start.year) * 12 + (task_end.month - task_start.month) + 1
        
        color = colors[idx % len(colors)]
        bar = ax.barh(idx, duration, left=start_offset, height=0.6, 
                     color=color, edgecolor='#333333', linewidth=1.5)
        
        # 任务名称
        ax.text(-0.5, idx, task['name'], ha='right', va='center', 
               fontsize=10, fontweight='bold')
    
    # 设置坐标轴
    ax.set_yticks([])
    ax.set_xlabel('时间 (月)', fontsize=11)
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    
    # 设置 x 轴刻度
    month_ticks = []
    month_labels = []
    for m in range(0, total_months, 3):
        year_offset = (start.month + m - 1) // 12
        month = ((start.month + m - 1) % 12) + 1
        current = datetime(start.year + year_offset, month, 1)
        month_ticks.append(m)
        month_labels.append(current.strftime('%Y-%m'))
    
    ax.set_xticks(month_ticks)
    ax.set_xticklabels(month_labels, rotation=45, ha='right')
    
    ax.set_xlim(-1, total_months)
    ax.set_ylim(-0.5, len(tasks) - 0.5)
    
    # 网格
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # 保存
    output_path = OUTPUT_DIR / output_name
    plt.savefig(output_path, dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    
    print(f"[OK] Timeline saved: {output_path}")
    return str(output_path)


def draw_comparison_chart(title, methods, metrics, data, 
                          output_name='comparison.png'):
    """
    绘制对比图（柱状图）
    
    Parameters
    ----------
    title : str
        图表标题
    methods : list
        方法名称列表
    metrics : list
        指标名称列表
    data : list of lists
        数据矩阵 [method][metric]
    output_name : str
        输出文件名
    """
    
    colors = ['#2E86AB', '#A23B72', '#F18F01', '#6A994E', '#577590']
    
    n_methods = len(methods)
    n_metrics = len(metrics)
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    x = np.arange(n_metrics)
    width = 0.8 / n_methods
    
    for idx, (method, method_data) in enumerate(zip(methods, data)):
        offset = (idx - n_methods/2 + 0.5) * width
        bars = ax.bar(x + offset, method_data, width, 
                     label=method, color=colors[idx % len(colors)],
                     edgecolor='#333333', linewidth=1.2)
    
    # 设置
    ax.set_xlabel('评价指标', fontsize=11)
    ax.set_ylabel('得分', fontsize=11)
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=10)
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, alpha=0.3, linestyle='--', axis='y')
    
    # 保存
    output_path = OUTPUT_DIR / output_name
    plt.savefig(output_path, dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    
    print(f"[OK] Comparison chart saved: {output_path}")
    return str(output_path)


# ============ 主函数 ============

def main():
    """测试绘图功能"""
    
    # 示例 1：技术路线图
    print("Example 1: Drawing technical roadmap...")
    steps = [
        "Literature Review",
        "Theoretical Analysis",
        "Algorithm Design",
        "Numerical Simulation",
        "Experimental Validation",
        "Paper Writing"
    ]
    draw_flowchart(
        title="Technical Roadmap for ML-based Damage Identification",
        steps=steps,
        orientation='horizontal',
        output_name='technical_roadmap.png'
    )
    
    # 示例 2：架构图
    print("Example 2: Drawing system architecture...")
    modules = [
        ["Data Acquisition Layer"],
        ["Feature Extraction", "Data Preprocessing", "Quality Control"],
        ["Model Training", "Parameter Optimization", "Cross Validation"],
        ["Damage Identification", "Result Visualization"]
    ]
    draw_architecture(
        title="System Architecture",
        modules=modules,
        output_name='system_architecture.png'
    )
    
    # 示例 3：甘特图
    print("Example 3: Drawing research timeline...")
    tasks = [
        {'name': 'Literature Review', 'start': '2024-01', 'end': '2024-03'},
        {'name': 'Theoretical Modeling', 'start': '2024-02', 'end': '2024-06'},
        {'name': 'Algorithm Development', 'start': '2024-04', 'end': '2024-09'},
        {'name': 'Experimental Validation', 'start': '2024-07', 'end': '2024-12'},
        {'name': 'Paper Writing', 'start': '2024-10', 'end': '2025-03'}
    ]
    draw_timeline(
        title="Research Timeline",
        tasks=tasks,
        start_date='2024-01',
        end_date='2025-03',
        output_name='research_timeline.png'
    )
    
    print("\nAll example figures generated successfully!")
    print(f"Output directory: {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
