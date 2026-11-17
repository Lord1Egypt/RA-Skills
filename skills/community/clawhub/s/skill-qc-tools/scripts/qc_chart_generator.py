#!/usr/bin/env python3
"""
QC图表生成器 - 支持柏拉图、鱼骨图、直方图、控制图、散布图
"""

import argparse
import json
import sys
import os
from datetime import datetime

# 检查依赖
try:
    import matplotlib
    matplotlib.use('Agg')  # 非交互式后端
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm
    import numpy as np
    import pandas as pd
except ImportError as e:
    print(json.dumps({
        "status": "error",
        "message": f"缺少依赖包: {str(e)}",
        "solution": "请安装: pip install matplotlib numpy pandas"
    }))
    sys.exit(1)

# 设置中文字体
def setup_chinese_font():
    """配置中文字体支持"""
    font_paths = [
        '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
        '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
        '/System/Library/Fonts/PingFang.ttc',
        'C:/Windows/Fonts/msyh.ttc',
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            prop = fm.FontProperties(fname=font_path)
            plt.rcParams['font.family'] = prop.get_name()
            break
    else:
        plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']
    
    plt.rcParams['axes.unicode_minus'] = False

setup_chinese_font()

def generate_pareto(data, output_path, title="柏拉图分析"):
    """生成柏拉图"""
    categories = [item['category'] for item in data]
    values = [item['value'] for item in data]
    
    # 按值降序排序
    sorted_data = sorted(zip(values, categories), reverse=True)
    values, categories = zip(*sorted_data)
    
    # 计算累计占比
    total = sum(values)
    cumulative = []
    cumsum = 0
    for v in values:
        cumsum += v
        cumulative.append(cumsum / total * 100)
    
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # 柱状图
    x_pos = np.arange(len(categories))
    bars = ax1.bar(x_pos, values, color='steelblue', alpha=0.8, label='数量')
    ax1.set_xlabel('问题类别', fontsize=12)
    ax1.set_ylabel('数量', fontsize=12, color='steelblue')
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(categories, rotation=45, ha='right')
    
    # 折线图
    ax2 = ax1.twinx()
    ax2.plot(x_pos, cumulative, 'ro-', linewidth=2, markersize=8, label='累计占比%')
    ax2.set_ylabel('累计占比 (%)', fontsize=12, color='red')
    ax2.axhline(y=80, color='orange', linestyle='--', linewidth=1.5, label='80%线')
    
    # 添加数据标签
    for i, (bar, cum) in enumerate(zip(bars, cumulative)):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{values[i]}', ha='center', va='bottom', fontsize=10)
        ax2.text(i, cum + 2, f'{cum:.1f}%', ha='center', va='bottom', fontsize=9, color='red')
    
    plt.title(title, fontsize=14, fontweight='bold', pad=20)
    
    # 图例
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    # 输出分析结果
    critical_items = []
    for i, cum in enumerate(cumulative):
        if cum <= 80:
            critical_items.append(categories[i])
    
    return {
        "status": "success",
        "chart_type": "pareto",
        "output_file": output_path,
        "total_count": total,
        "category_count": len(categories),
        "critical_items": critical_items,
        "message": f"识别出{len(critical_items)}个关键问题，累计占比约{sum(values[:len(critical_items)])/total*100:.1f}%"
    }

def generate_histogram(data, output_path, title="直方图分析", bins=10):
    """生成直方图"""
    values = data['values']
    spec_limits = data.get('spec_limits', {})
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # 绘制直方图
    n, bins_arr, patches = ax.hist(values, bins=bins, color='steelblue', 
                                    alpha=0.7, edgecolor='black', density=True)
    
    # 添加正态分布曲线
    mu, sigma = np.mean(values), np.std(values)
    x = np.linspace(min(values), max(values), 100)
    ax.plot(x, 1/(sigma * np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((x - mu)/sigma)**2),
            'r-', linewidth=2, label=f'正态分布\nμ={mu:.2f}\nσ={sigma:.2f}')
    
    # 标注规格限
    if spec_limits.get('USL'):
        ax.axvline(x=spec_limits['USL'], color='red', linestyle='--', 
                   linewidth=2, label=f'USL={spec_limits["USL"]}')
    if spec_limits.get('LSL'):
        ax.axvline(x=spec_limits['LSL'], color='red', linestyle='--', 
                   linewidth=2, label=f'LSL={spec_limits["LSL"]}')
    if spec_limits.get('USL') and spec_limits.get('LSL'):
        ax.axvline(x=spec_limits.get('UCL', (spec_limits['USL'] + spec_limits['LSL'])/2), 
                   color='green', linestyle='-.', linewidth=1.5, 
                   label=f'CL={((spec_limits["USL"] + spec_limits["LSL"])/2):.2f}')
    
    ax.set_xlabel('数值', fontsize=12)
    ax.set_ylabel('频率密度', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='upper right')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    # 计算过程能力指数
    cp = None
    cpk = None
    if spec_limits.get('USL') and spec_limits.get('LSL'):
        tolerance = spec_limits['USL'] - spec_limits['LSL']
        cp = tolerance / (6 * sigma) if sigma > 0 else 0
        cpu = (spec_limits['USL'] - mu) / (3 * sigma) if sigma > 0 else 0
        cpl = (mu - spec_limits['LSL']) / (3 * sigma) if sigma > 0 else 0
        cpk = min(cpu, cpl)
    
    return {
        "status": "success",
        "chart_type": "histogram",
        "output_file": output_path,
        "mean": round(mu, 4),
        "std_dev": round(sigma, 4),
        "min": round(min(values), 4),
        "max": round(max(values), 4),
        "cp": round(cp, 4) if cp else None,
        "cpk": round(cpk, 4) if cpk else None,
        "data_count": len(values)
    }

def generate_control_chart(data, output_path, title="控制图分析"):
    """生成X-bar控制图"""
    subgroups = data['subgroups']
    subgroup_size = data.get('subgroup_size', 5)
    chart_type = data.get('chart_type', 'xbar_r')  # xbar_r, xbar_s, imr
    
    fig, axes = plt.subplots(2, 1, figsize=(14, 10)) if chart_type == 'xbar_r' else plt.subplots(figsize=(12, 6))
    
    if chart_type == 'xbar_r':
        ax1, ax2 = axes
        
        # 计算子组统计量
        x_bar = [np.mean(sg) for sg in subgroups]
        x_double_bar = np.mean(x_bar)
        
        # 计算R图参数
        r_values = [max(sg) - min(sg) for sg in subgroups]
        r_bar = np.mean(r_values)
        
        # 控制限常数
        d2 = {2: 1.128, 3: 1.693, 4: 2.059, 5: 2.326, 6: 2.534, 7: 2.704, 8: 2.847, 9: 2.970, 10: 3.078}
        d3 = {2: 0, 3: 0, 4: 0, 5: 0.077, 6: 0.136, 7: 0.184, 8: 0.223, 9: 0.256, 10: 0.283}
        D3 = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0.076, 8: 0.136, 9: 0.184, 10: 0.223}
        D4 = {2: 3.267, 3: 2.574, 4: 2.282, 5: 2.114, 6: 2.004, 7: 1.924, 8: 1.864, 9: 1.816, 10: 1.777}
        
        # X-bar图控制限
        sigma_est = r_bar / d2.get(subgroup_size, 2.326)
        UCL_x = x_double_bar + 3 * sigma_est
        LCL_x = x_double_bar - 3 * sigma_est
        
        # 绘制X-bar图
        x = np.arange(1, len(x_bar) + 1)
        ax1.plot(x, x_bar, 'bo-', markersize=8, linewidth=1.5)
        ax1.axhline(y=x_double_bar, color='green', linestyle='-', linewidth=2, label=f'CL={x_double_bar:.2f}')
        ax1.axhline(y=UCL_x, color='red', linestyle='--', linewidth=1.5, label=f'UCL={UCL_x:.2f}')
        ax1.axhline(y=LCL_x, color='red', linestyle='--', linewidth=1.5, label=f'LCL={LCL_x:.2f}')
        
        # 标注异常点
        for i, val in enumerate(x_bar):
            if val > UCL_x or val < LCL_x:
                ax1.plot(i+1, val, 'ro', markersize=12, markerfacecolor='none', markeredgewidth=2)
        
        ax1.set_xlabel('子组编号', fontsize=12)
        ax1.set_ylabel('X̄', fontsize=12)
        ax1.set_title(f'{title} - X̄控制图', fontsize=13, fontweight='bold')
        ax1.legend(loc='upper right')
        ax1.grid(True, alpha=0.3)
        
        # 绘制R图
        UCL_r = D4.get(subgroup_size, 2.282) * r_bar
        LCL_r = max(0, D3.get(subgroup_size, 0) * r_bar)
        
        ax2.plot(x, r_values, 'gs-', markersize=8, linewidth=1.5)
        ax2.axhline(y=r_bar, color='green', linestyle='-', linewidth=2, label=f'R̄={r_bar:.2f}')
        ax2.axhline(y=UCL_r, color='red', linestyle='--', linewidth=1.5, label=f'UCL={UCL_r:.2f}')
        ax2.axhline(y=LCL_r, color='red', linestyle='--', linewidth=1.5, label=f'LCL={LCL_r:.2f}')
        
        # 标注异常点
        for i, val in enumerate(r_values):
            if val > UCL_r or val < LCL_r:
                ax2.plot(i+1, val, 'ro', markersize=12, markerfacecolor='none', markeredgewidth=2)
        
        ax2.set_xlabel('子组编号', fontsize=12)
        ax2.set_ylabel('R', fontsize=12)
        ax2.set_title(f'{title} - R控制图', fontsize=13, fontweight='bold')
        ax2.legend(loc='upper right')
        ax2.grid(True, alpha=0.3)
        
    elif chart_type == 'imr':
        ax = axes
        
        # 单值和移动极差
        x = np.arange(1, len(subgroups) + 1)
        values = subgroups if isinstance(subgroups[0], (int, float)) else [sg[0] for sg in subgroups]
        
        # 计算移动极差
        mr = [abs(values[i] - values[i-1]) for i in range(1, len(values))]
        mr_bar = np.mean(mr)
        
        # 控制限
        x_bar = np.mean(values)
        d2_imr = 1.128
        sigma_est = mr_bar / d2_imr
        UCL_x = x_bar + 3 * sigma_est
        LCL_x = x_bar - 3 * sigma_est
        UCL_mr = 3.267 * mr_bar
        LCL_mr = 0
        
        # 绘制I图
        ax.plot(x, values, 'bo-', markersize=8, linewidth=1.5)
        ax.axhline(y=x_bar, color='green', linestyle='-', linewidth=2, label=f'X̄={x_bar:.2f}')
        ax.axhline(y=UCL_x, color='red', linestyle='--', linewidth=1.5, label=f'UCL={UCL_x:.2f}')
        ax.axhline(y=LCL_x, color='red', linestyle='--', linewidth=1.5, label=f'LCL={LCL_x:.2f}')
        
        for i, val in enumerate(values):
            if val > UCL_x or val < LCL_x:
                ax.plot(i+1, val, 'ro', markersize=12, markerfacecolor='none', markeredgewidth=2)
        
        ax.set_xlabel('样本编号', fontsize=12)
        ax.set_ylabel('单值', fontsize=12)
        ax.set_title(f'{title} - 单值-移动极差控制图', fontsize=13, fontweight='bold')
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    # 检测异常点
    x_bar = [np.mean(sg) for sg in subgroups] if chart_type == 'xbar_r' else values
    x_double_bar = np.mean(x_bar)
    sigma_est = r_bar / d2.get(subgroup_size, 2.326) if chart_type == 'xbar_r' else mr_bar / d2_imr
    UCL = x_double_bar + 3 * sigma_est
    LCL = x_double_bar - 3 * sigma_est
    
    out_of_control = []
    for i, val in enumerate(x_bar):
        if val > UCL or val < LCL:
            out_of_control.append({"subgroup": i+1, "value": round(val, 4), "status": "超出控制限"})
    
    return {
        "status": "success",
        "chart_type": "control_chart",
        "output_file": output_path,
        "center_line": round(x_double_bar, 4),
        "UCL": round(UCL, 4),
        "LCL": round(LCL, 4),
        "out_of_control_points": out_of_control,
        "message": f"共{len(out_of_control)}个点超出控制限" if out_of_control else "过程受控，无异常点"
    }

def generate_scatter(data, output_path, title="散布图分析"):
    """生成散布图"""
    x_data = data['x']
    y_data = data['y']
    x_label = data.get('x_label', 'X')
    y_label = data.get('y_label', 'Y')
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    ax.scatter(x_data, y_data, c='steelblue', s=80, alpha=0.7, edgecolors='black')
    
    # 计算相关系数
    n = len(x_data)
    x_mean, y_mean = np.mean(x_data), np.mean(y_data)
    numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_data, y_data))
    denominator_x = sum((x - x_mean) ** 2 for x in x_data)
    denominator_y = sum((y - y_mean) ** 2 for y in y_data)
    r = numerator / np.sqrt(denominator_x * denominator_y) if denominator_x > 0 and denominator_y > 0 else 0
    
    # 添加趋势线
    z = np.polyfit(x_data, y_data, 1)
    p = np.poly1d(z)
    x_line = np.linspace(min(x_data), max(x_data), 100)
    ax.plot(x_line, p(x_line), 'r--', linewidth=2, 
            label=f'趋势线: y={z[0]:.3f}x+{z[1]:.3f}')
    
    ax.set_xlabel(x_label, fontsize=12)
    ax.set_ylabel(y_label, fontsize=12)
    ax.set_title(f'{title}\n相关系数 r = {r:.4f}', fontsize=14, fontweight='bold')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    # 相关性判断
    r_abs = abs(r)
    if r_abs < 0.2:
        correlation = "几乎无相关"
    elif r_abs < 0.4:
        correlation = "弱相关"
    elif r_abs < 0.6:
        correlation = "中等相关"
    elif r_abs < 0.8:
        correlation = "强相关"
    else:
        correlation = "非常强相关"
    
    direction = "正相关" if r > 0 else "负相关"
    
    return {
        "status": "success",
        "chart_type": "scatter",
        "output_file": output_path,
        "correlation_coefficient": round(r, 4),
        "correlation_level": correlation,
        "correlation_direction": direction,
        "regression_line": f"y = {z[0]:.4f}x + {z[1]:.4f}",
        "message": f"{correlation}（{direction}），相关系数r={r:.4f}"
    }

def generate_fishbone(data, output_path, title="鱼骨图分析"):
    """生成鱼骨图（因果图）"""
    causes = data.get('causes', {})
    # causes格式: {"人": [...], "机": [...], "料": [...], "法": [...], "环": [...], "测": [...]}
    
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # 主骨（水平线）
    ax.annotate('', xy=(14, 5), xytext=(1, 5),
                arrowprops=dict(arrowstyle='-', color='black', lw=3))
    
    # 鱼头（问题）
    ax.text(14.5, 5, data.get('problem', '质量问题'), fontsize=14, fontweight='bold',
            va='center', ha='left', bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', edgecolor='orange', linewidth=2))
    
    # 六大要因的位置
    categories = [
        ("人", 3, 8, 30),
        ("机", 6, 8, 30),
        ("料", 9, 8, 30),
        ("法", 3, 2, 210),
        ("机", 6, 2, 210),
        ("测", 9, 2, 210),
    ]
    
    # 简化为4大类
    main_causes = [
        ("人", 4, 8, 45),
        ("机", 7, 8, 45),
        ("料", 10, 8, 45),
        ("法", 10, 2, 135),
        ("环", 7, 2, 135),
        ("测", 4, 2, 135),
    ]
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
    
    for i, (cause, x, y, angle) in enumerate(main_causes):
        if cause in causes and causes[cause]:
            # 绘制分支骨
            ax.annotate('', xy=(12, 5), xytext=(x, y),
                        arrowprops=dict(arrowstyle='-', color=colors[i], lw=2))
            
            # 类别标签
            ax.text(x, y, cause, fontsize=12, fontweight='bold',
                   va='center', ha='center',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor=colors[i], alpha=0.3))
            
            # 子原因
            sub_causes = causes[cause]
            n = len(sub_causes)
            for j, sub in enumerate(sub_causes[:5]):  # 最多显示5个
                if i < 3:  # 上方三类
                    offset_y = 0.6 * (j - n/2 + 0.5)
                    ax.text(x + 0.8, y + offset_y, f"• {sub}", fontsize=9, va='center')
                else:  # 下方三类
                    offset_y = 0.6 * (j - n/2 + 0.5)
                    ax.text(x + 0.8, y + offset_y, f"• {sub}", fontsize=9, va='center')
    
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    background_color = 'white'
    plt.close()
    
    return {
        "status": "success",
        "chart_type": "fishbone",
        "output_file": output_path,
        "main_causes": list(causes.keys()),
        "total_causes": sum(len(v) for v in causes.values()),
        "message": f"生成包含{len(causes)}个主因类别的鱼骨图"
    }

def export_data(chart_type, analysis_result, output_path):
    """导出分析结果为JSON"""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(analysis_result, f, ensure_ascii=False, indent=2)
    
    return {
        "status": "success",
        "export_file": output_path,
        "message": f"分析结果已导出至 {output_path}"
    }

def load_template(template_name):
    """加载预设模板"""
    template_dir = os.path.join(os.path.dirname(__file__), '..', 'assets', 'templates')
    template_path = os.path.join(template_dir, f'{template_name}.json')
    
    if not os.path.exists(template_path):
        return None
    
    with open(template_path, 'r', encoding='utf-8') as f:
        template = json.load(f)
    
    # 如果模板有外层 data 键，提取出来
    if 'data' in template:
        return template['data']
    return template

def main():
    parser = argparse.ArgumentParser(description='QC图表生成工具')
    parser.add_argument('--chart-type', '-t', required=True,
                       choices=['pareto', 'histogram', 'control', 'scatter', 'fishbone'],
                       help='图表类型')
    parser.add_argument('--data', '-d', required=True,
                       help='JSON格式数据或模板名称')
    parser.add_argument('--output', '-o', required=True,
                       help='输出文件路径')
    parser.add_argument('--title', default='',
                       help='图表标题')
    parser.add_argument('--export-json', '-e', action='store_true',
                       help='同时导出分析结果JSON')
    parser.add_argument('--template', action='store_true',
                       help='data参数为模板名称')
    
    args = parser.parse_args()
    
    # 加载数据
    try:
        if args.template:
            data = load_template(args.data)
            if data is None:
                print(json.dumps({
                    "status": "error",
                    "message": f"模板 '{args.data}' 不存在"
                }, ensure_ascii=False))
                sys.exit(1)
        else:
            data = json.loads(args.data)
    except json.JSONDecodeError as e:
        print(json.dumps({
            "status": "error",
            "message": f"数据格式错误: {str(e)}"
        }))
        sys.exit(1)
    
    # 生成图表
    chart_type_map = {
        'pareto': 'pareto',
        'histogram': 'histogram',
        'control': 'control_chart',
        'scatter': 'scatter',
        'fishbone': 'fishbone'
    }
    
    generators = {
        'pareto': generate_pareto,
        'histogram': generate_histogram,
        'control': generate_control_chart,
        'scatter': generate_scatter,
        'fishbone': generate_fishbone
    }
    
    generator = generators[args.chart_type]
    title = args.title or f"{chart_type_map[args.chart_type].replace('_', ' ').title()}分析"
    
    result = generator(data, args.output, title)
    
    # 导出JSON
    if args.export_json:
        json_path = args.output.rsplit('.', 1)[0] + '_analysis.json'
        export_result = export_data(args.chart_type, result, json_path)
        result['export'] = export_result
    
    print(json.dumps(result, ensure_ascii=False))

if __name__ == '__main__':
    main()
