#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
科研绘图工具 v2 - 修复字体和布局问题
支持：技术路线图、流程图、原理图、架构图、数据可视化
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch
import numpy as np
from pathlib import Path

# 配置中文字体 - 使用 Windows 系统字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 150  # 提高 DPI
plt.rcParams['savefig.dpi'] = 300  # 保存时 300 DPI

OUTPUT_DIR = Path("D:/Personal/OpenClaw/figures")
OUTPUT_DIR.mkdir(exist_ok=True)


def draw_flowchart(title, steps, orientation='horizontal', output_name='flowchart.png'):
    """
    绘制流程图/技术路线图 - 修复版
    """
    n = len(steps)
    
    # 配色方案 - 专业蓝色系
    colors = ['#2E86AB', '#3B9ACD', '#4682B4', '#5F9EA0', '#6A994E', '#577590']
    
    # 根据步骤数调整画布大小
    if orientation == 'horizontal':
        fig_width = max(14, n * 2.5)
        fig, ax = plt.subplots(figsize=(fig_width, 5))
        x_step = 1.0 / (n + 1)
        y_center = 0.5
        box_width = min(0.5, x_step * 0.7)
        box_height = 0.35
    else:
        fig_height = max(10, n * 1.5)
        fig, ax = plt.subplots(figsize=(10, fig_height))
        y_step = 1.0 / (n + 1)
        x_center = 0.5
        box_width = 0.6
        box_height = min(0.15, y_step * 0.6)
    
    # 绘制方框
    for i, step in enumerate(steps):
        if orientation == 'horizontal':
            x = x_step * (i + 1)
            y = y_center
            
            # 使用圆角矩形
            box = patches.FancyBboxPatch(
                (x - box_width/2, y - box_height/2), 
                box_width, box_height,
                boxstyle="round,pad=0.08,rounding_size=0.03",
                linewidth=2.5, 
                edgecolor='#2C3E50', 
                facecolor=colors[i % len(colors)],
                alpha=0.95
            )
            ax.add_patch(box)
            
            # 文字 - 调整字体大小
            font_size = min(12, 14 / max(1, n/6))
            ax.text(x, y, step, ha='center', va='center', 
                   fontsize=font_size, fontweight='bold', 
                   color='white', wrap=False)
            
            # 绘制箭头
            if i < n - 1:
                arrow = FancyArrowPatch(
                    (x + box_width/2 + 0.02, y), 
                    (x + x_step - box_width/2 - 0.02, y),
                    arrowstyle='->', mutation_scale=25,
                    linewidth=2.5, color='#2C3E50'
                )
                ax.add_patch(arrow)
                
        else:
            x = x_center
            y = y_step * (n - i)
            
            box = patches.FancyBboxPatch(
                (x - box_width/2, y - box_height/2), 
                box_width, box_height,
                boxstyle="round,pad=0.08,rounding_size=0.03",
                linewidth=2.5, 
                edgecolor='#2C3E50', 
                facecolor=colors[i % len(colors)],
                alpha=0.95
            )
            ax.add_patch(box)
            
            font_size = min(12, 14 / max(1, n/6))
            ax.text(x, y, step, ha='center', va='center',
                   fontsize=font_size, fontweight='bold', 
                   color='white', wrap=True)
            
            if i < n - 1:
                arrow = FancyArrowPatch(
                    (x, y - box_height/2 - 0.02), 
                    (x, y - y_step + box_height/2 + 0.02),
                    arrowstyle='->', mutation_scale=25,
                    linewidth=2.5, color='#2C3E50'
                )
                ax.add_patch(arrow)
    
    # 标题
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20, color='#2C3E50')
    
    # 设置
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_aspect('equal')
    
    # 保存 - 使用 bbox_inches='tight' 避免裁剪
    output_path = OUTPUT_DIR / output_name
    plt.savefig(output_path, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    
    print(f'[OK] Flowchart saved: {output_path}')
    return str(output_path)


def draw_architecture(title, modules, output_name='architecture.png'):
    """
    绘制系统架构图 - 修复版
    """
    n_levels = len(modules)
    
    # 配色 - 每层不同颜色
    colors = ['#2E86AB', '#4A90C9', '#6BA3D9', '#8CB8E8']
    
    fig_width = max(12, max(len(m) for m in modules) * 2.5)
    fig_height = max(8, n_levels * 2)
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    
    # 绘制层级
    for level_idx, level_modules in enumerate(modules):
        n_modules = len(level_modules)
        y_pos = 1.0 - (level_idx + 0.5) / (n_levels + 0.5)
        
        # 层级标签
        ax.text(0.02, y_pos, f'Layer {level_idx + 1}', 
               fontsize=10, fontweight='bold', 
               va='center', ha='left',
               bbox=dict(boxstyle='round', facecolor='#f0f0f0', alpha=0.7, edgecolor='#ccc'))
        
        # 绘制模块
        x_step = 0.85 / n_modules
        color = colors[level_idx % len(colors)]
        
        for mod_idx, module in enumerate(level_modules):
            x_pos = 0.1 + x_step * (mod_idx + 0.5)
            box_width = x_step * 0.8
            box_height = 0.12
            
            box = patches.FancyBboxPatch(
                (x_pos - box_width/2, y_pos - box_height/2), 
                box_width, box_height,
                boxstyle="round,pad=0.08,rounding_size=0.02",
                linewidth=2.5, 
                edgecolor='#2C3E50', 
                facecolor=color,
                alpha=0.95
            )
            ax.add_patch(box)
            
            # 文字 - 自动调整字体
            font_size = min(10, 11 / max(1, n_modules/4))
            ax.text(x_pos, y_pos, str(module), ha='center', va='center',
                   fontsize=font_size, fontweight='bold', 
                   color='white', wrap=True)
    
    # 标题
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20, color='#2C3E50')
    
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
    
    print(f'[OK] Architecture saved: {output_path}')
    return str(output_path)


def draw_timeline(title, tasks, output_name='timeline.png'):
    """
    绘制甘特图/时间线图 - 修复版
    """
    from datetime import datetime
    
    # 配色
    colors = ['#2E86AB', '#A23B72', '#F18F01', '#6A994E', '#577590']
    
    n_tasks = len(tasks)
    
    # 解析日期
    start = datetime.strptime(tasks[0]['start'], '%Y-%m')
    end = datetime.strptime(tasks[-1]['end'], '%Y-%m')
    total_months = (end.year - start.year) * 12 + (end.month - start.month) + 1
    
    fig, ax = plt.subplots(figsize=(max(14, total_months * 0.8), n_tasks * 0.8 + 2))
    
    # 绘制任务条
    for idx, task in enumerate(tasks):
        task_start = datetime.strptime(task['start'], '%Y-%m')
        task_end = datetime.strptime(task['end'], '%Y-%m')
        
        start_offset = (task_start.year - start.year) * 12 + (task_start.month - start.month)
        duration = (task_end.year - task_start.year) * 12 + (task_end.month - task_start.month) + 1
        
        color = colors[idx % len(colors)]
        bar = ax.barh(idx, duration, left=start_offset, height=0.55, 
                     color=color, edgecolor='#2C3E50', linewidth=2)
        
        # 任务名称 - 左侧
        ax.text(-0.8, idx, task['name'], ha='right', va='center', 
               fontsize=10, fontweight='bold')
    
    # 设置
    ax.set_yticks([])
    ax.set_xlabel('Time (Month)', fontsize=11, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    
    # x 轴刻度
    month_ticks = []
    month_labels = []
    for m in range(0, total_months, 3):
        year_offset = (start.month + m - 1) // 12
        month = ((start.month + m - 1) % 12) + 1
        current = datetime(start.year + year_offset, month, 1)
        month_ticks.append(m)
        month_labels.append(current.strftime('%Y-%m'))
    
    ax.set_xticks(month_ticks)
    ax.set_xticklabels(month_labels, rotation=45, ha='right', fontsize=9)
    
    ax.set_xlim(-1.5, total_months)
    ax.set_ylim(-0.5, n_tasks - 0.5)
    
    # 网格
    ax.grid(True, alpha=0.3, linestyle='--', axis='x')
    
    # 保存
    output_path = OUTPUT_DIR / output_name
    plt.savefig(output_path, dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    
    print(f'[OK] Timeline saved: {output_path}')
    return str(output_path)


# ============ 主函数 ============

def main():
    """测试绘图功能 - 修复版"""
    
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
        output_name='technical_roadmap_v2.png'
    )
    
    # 示例 2：架构图
    print("Example 2: Drawing system architecture...")
    modules = [
        ["Data Acquisition"],
        ["Feature Extraction", "Preprocessing", "Quality Control"],
        ["Model Training", "Optimization", "Validation"],
        ["Damage ID", "Visualization"]
    ]
    draw_architecture(
        title="System Architecture",
        modules=modules,
        output_name='system_architecture_v2.png'
    )
    
    # 示例 3：甘特图
    print("Example 3: Drawing research timeline...")
    tasks = [
        {'name': 'Literature Review', 'start': '2024-01', 'end': '2024-03'},
        {'name': 'Theoretical Modeling', 'start': '2024-02', 'end': '2024-06'},
        {'name': 'Algorithm Dev', 'start': '2024-04', 'end': '2024-09'},
        {'name': 'Exp. Validation', 'start': '2024-07', 'end': '2024-12'},
        {'name': 'Paper Writing', 'start': '2024-10', 'end': '2025-03'}
    ]
    draw_timeline(
        title="Research Timeline 2024-2025",
        tasks=tasks,
        output_name='research_timeline_v2.png'
    )
    
    print("\nAll example figures generated successfully!")
    print(f"Output directory: {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
