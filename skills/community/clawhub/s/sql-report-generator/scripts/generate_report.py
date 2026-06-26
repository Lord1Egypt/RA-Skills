"""
sql-report-generator 核心脚本
生成图文表格混排的 HTML 报告

用法：
    python generate_report.py --template weekly --output report.html
    python generate_report.py --template funnel --data funnel.csv
"""

import argparse
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch
import base64, io, warnings
from datetime import datetime
from typing import Dict, List, Optional, Tuple

warnings.filterwarnings('ignore')

# ══════════════════════════════════════════════════════
# 配置
# ══════════════════════════════════════════════════════

BLUE, GREEN, AMBER, RED, PURPLE = '#3b82f6','#10b981','#f59e0b','#ef4444','#8b5cf6'
GRAY, LIGHT = '#6b7280', '#f8fafc'
PALETTE = [BLUE, GREEN, AMBER, RED, PURPLE, '#06b6d4']

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


# ══════════════════════════════════════════════════════
# 图表工具函数
# ══════════════════════════════════════════════════════

def fig_to_b64(fig: plt.Figure) -> str:
    """将 matplotlib 图表转为 base64 字符串"""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()


def generate_trend_chart(
    df: pd.DataFrame,
    date_col: str = 'date',
    value_col: str = 'value',
    title: str = '趋势图',
    show_ma: bool = True,
    ma_window: int = 7,
    highlight_peaks: bool = True
) -> str:
    """生成趋势折线图"""
    fig, ax = plt.subplots(figsize=(11, 4), facecolor='white')
    ax.set_facecolor('white')

    # 填充区域
    ax.fill_between(df[date_col], df[value_col], alpha=0.10, color=BLUE)

    # 主线
    ax.plot(df[date_col], df[value_col], color=BLUE, linewidth=2.2, zorder=3, label='日数据')

    # 移动均线
    if show_ma:
        ma = df[value_col].rolling(ma_window, min_periods=1).mean()
        ax.plot(df[date_col], ma, color=AMBER, linewidth=1.8, linestyle='--', alpha=0.9, label=f'{ma_window}日均线')

    # 峰值标注
    if highlight_peaks:
        max_i = df[value_col].idxmax()
        min_i = df[value_col].idxmin()
        ax.scatter([df.loc[max_i, date_col]], [df.loc[max_i, value_col]], color=GREEN, s=70, zorder=5)
        ax.scatter([df.loc[min_i, date_col]], [df.loc[min_i, value_col]], color=RED, s=70, zorder=5)
        ax.annotate(f"峰值 {df.loc[max_i, value_col]:,}",
                    xy=(df.loc[max_i, date_col], df.loc[max_i, value_col]),
                    xytext=(6, 8), textcoords='offset points', fontsize=9, color=GREEN, fontweight='bold')
        ax.annotate(f"低谷 {df.loc[min_i, value_col]:,}",
                    xy=(df.loc[min_i, date_col], df.loc[min_i, value_col]),
                    xytext=(6, -16), textcoords='offset points', fontsize=9, color=RED, fontweight='bold')

    ax.legend(fontsize=9, loc='upper left', framealpha=0.8)
    ax.grid(axis='y', alpha=0.2, linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(axis='x', rotation=30, labelsize=9)

    plt.tight_layout(pad=1.2)
    img = fig_to_b64(fig)
    plt.close(fig)
    return img


def generate_bar_chart(
    df: pd.DataFrame,
    category_col: str = 'category',
    value_col: str = 'value',
    title: str = '对比图',
    horizontal: bool = True,
    highlight_top: int = 1,
    sort_by_value: bool = True
) -> str:
    """生成条形图"""
    if sort_by_value:
        df = df.sort_values(value_col, ascending=horizontal)

    fig, ax = plt.subplots(figsize=(7, 4.5), facecolor='white')
    ax.set_facecolor('white')

    if horizontal:
        colors = [GREEN if i >= len(df) - highlight_top else BLUE for i in range(len(df))]
        bars = ax.barh(df[category_col], df[value_col], color=colors, height=0.6, edgecolor='white')
        for bar in bars:
            w = bar.get_width()
            ax.text(w + df[value_col].max() * 0.02, bar.get_y() + bar.get_height()/2,
                    f'{w:,.0f}', va='center', fontsize=9, color='#374151')
        ax.set_xlim(0, df[value_col].max() * 1.2)
        ax.grid(axis='x', alpha=0.2, linestyle='--')
    else:
        bars = ax.bar(df[category_col], df[value_col], color=BLUE, width=0.6, edgecolor='white')
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, h + df[value_col].max() * 0.01,
                    f'{h:,.0f}', ha='center', fontsize=9)
        ax.grid(axis='y', alpha=0.2, linestyle='--')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout(pad=1.2)
    img = fig_to_b64(fig)
    plt.close(fig)
    return img


def generate_stacked_bar(
    df: pd.DataFrame,
    x_col: str,
    series_cols: List[str],
    title: str = '堆叠图'
) -> str:
    """生成堆叠条形图"""
    fig, ax = plt.subplots(figsize=(6, 4), facecolor='white')
    ax.set_facecolor('white')

    x = np.arange(len(df[x_col]))
    w = 0.6
    bottom = np.zeros(len(df))

    for i, col in enumerate(series_cols):
        ax.bar(x, df[col], w, label=col, color=PALETTE[i % len(PALETTE)],
               edgecolor='white', bottom=bottom)
        bottom += df[col].values

    ax.set_xticks(x)
    ax.set_xticklabels(df[x_col], fontsize=10)
    ax.legend(fontsize=9, loc='upper left')
    ax.grid(axis='y', alpha=0.2, linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout(pad=1.2)
    img = fig_to_b64(fig)
    plt.close(fig)
    return img


def generate_funnel_chart(
    labels: List[str],
    values: List[int],
    title: str = '漏斗图'
) -> str:
    """生成漏斗图"""
    fig, ax = plt.subplots(figsize=(5, 4), facecolor='white')
    ax.set_facecolor('white')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, len(labels))
    ax.axis('off')

    colors = [BLUE, '#60a5fa', '#93c5fd', GREEN, '#059669'][:len(labels)]

    for i, (label, val) in enumerate(zip(reversed(labels), reversed(values))):
        pct = val / values[0] * 100
        width = 0.2 + 0.8 * (val / values[0])
        left = (1 - width) / 2

        rect = FancyBboxPatch(
            (left, i * 0.18 + 0.02), width, 0.15,
            boxstyle="round,pad=0.01",
            facecolor=colors[len(labels)-1-i],
            edgecolor='white', linewidth=1.5
        )
        ax.add_patch(rect)

        ax.text(0.5, i * 0.18 + 0.095,
                f'{label}  {val:,}  ({pct:.1f}%)',
                ha='center', va='center',
                fontsize=10, color='white', fontweight='bold')

    plt.tight_layout(pad=0.5)
    img = fig_to_b64(fig)
    plt.close(fig)
    return img


# ══════════════════════════════════════════════════════
# 报告生成器
# ══════════════════════════════════════════════════════

def generate_report(
    title: str,
    period: str,
    kpis: List[Dict],
    sections: List[Dict],
    output_path: str,
    template: str = 'weekly'
) -> str:
    """
    生成 HTML 报告

    Args:
        title: 报告标题
        period: 数据周期
        kpis: KPI 列表，每个元素为 {label, value, change, direction}
        sections: 章节列表，每个元素为 {type, title, content, img, ...}
        output_path: 输出文件路径
        template: 模板类型

    Returns:
        输出文件路径
    """
    now_str = datetime.now().strftime('%Y年%m月%d日 %H:%M')

    # KPI 卡片 HTML
    kpi_html = ''
    for kpi in kpis:
        direction = kpi.get('direction', 'up')
        kpi_html += f"""
        <div class="kpi-card">
          <div class="kpi-label">{kpi['label']}</div>
          <div class="kpi-value">{kpi['value']}</div>
          <div class="kpi-change {direction}">{kpi['change']}</div>
        </div>"""

    # 章节内容
    sections_html = ''
    for section in sections:
        section_type = section.get('type', 'chart')

        if section_type == 'chart':
            sections_html += f"""
            <div class="card">
              <div class="card-title">{section.get('title', '')}</div>
              <img src="data:image/png;base64,{section.get('img', '')}" alt="{section.get('title', '')}">
              {f'<div class="insight">' + section.get('insight', '') + '</div>' if section.get('insight') else ''}
            </div>"""

        elif section_type == 'table':
            sections_html += f"""
            <div class="card">
              <div class="card-title">{section.get('title', '')}</div>
              {section.get('content', '')}
            </div>"""

        elif section_type == 'insight':
            sections_html += f"""
            <div class="insight-box">
              <strong>📌 {section.get('title', '关键洞察')}</strong>
              <p>{section.get('content', '')}</p>
            </div>"""

    # 完整 HTML
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
          background: #f1f5f9; color: #1e293b; }}

  .banner {{
    background: linear-gradient(135deg, #1e40af 0%, #3b82f6 60%, #06b6d4 100%);
    color: white; padding: 28px 40px;
  }}
  .banner h1 {{ font-size: 24px; font-weight: 700; }}
  .banner p  {{ margin-top: 6px; font-size: 13px; opacity: 0.85; }}

  .container {{ max-width: 1200px; margin: 0 auto; padding: 24px 20px; }}

  .section-title {{
    font-size: 15px; font-weight: 700; color: #1e293b;
    border-left: 4px solid #3b82f6; padding-left: 10px;
    margin: 24px 0 12px;
  }}

  .kpi-row {{ display: grid; grid-template-columns: repeat(4,1fr); gap: 14px; }}
  .kpi-card {{
    background: white; border-radius: 10px; padding: 18px 20px;
    box-shadow: 0 1px 4px rgba(0,0,0,.06);
  }}
  .kpi-label {{ font-size: 12px; color: #64748b; margin-bottom: 5px; }}
  .kpi-value {{ font-size: 24px; font-weight: 700; color: #1e293b; }}
  .kpi-change {{ font-size: 12px; margin-top: 4px; }}
  .up   {{ color: #10b981; }} .down {{ color: #ef4444; }}

  .card {{
    background: white; border-radius: 10px; padding: 18px 20px;
    box-shadow: 0 1px 4px rgba(0,0,0,.06); margin-bottom: 14px;
  }}
  .card-title {{ font-size: 13px; font-weight: 700; color: #374151; margin-bottom: 12px; }}
  .card img   {{ width: 100%; border-radius: 6px; }}

  .two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }}
  .three-col {{ display: grid; grid-template-columns: 3fr 2fr; gap: 14px; }}

  table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  thead tr {{ background: #f8fafc; }}
  th {{ padding: 10px 12px; text-align: left; font-weight: 600;
        color: #64748b; border-bottom: 2px solid #e2e8f0; font-size: 11px; }}
  td {{ padding: 10px 12px; border-bottom: 1px solid #f1f5f9; color: #374151; }}
  tbody tr:hover {{ background: #f8fafc; }}

  .insight {{
    background: #eff6ff; border-left: 4px solid #3b82f6;
    border-radius: 0 8px 8px 0; padding: 12px 16px;
    font-size: 13px; line-height: 1.7; color: #1e40af;
    margin-top: 12px;
  }}
  .insight strong {{ color: #1e3a8a; }}

  .footer {{
    text-align: center; padding: 20px; font-size: 12px; color: #94a3b8;
    border-top: 1px solid #e2e8f0; margin-top: 10px;
  }}
</style>
</head>
<body>

<div class="banner">
  <h1>📊 {title}</h1>
  <p>数据周期：{period} &nbsp;|&nbsp; 生成时间：{now_str}</p>
</div>

<div class="container">
  <div class="section-title">核心指标</div>
  <div class="kpi-row">{kpi_html}</div>

  {sections_html}
</div>

<div class="footer">
  本报告由 sql-report-generator skill 自动生成 &nbsp;·&nbsp; {now_str}
</div>

</body>
</html>"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    return output_path


# ══════════════════════════════════════════════════════
# 主函数
# ══════════════════════════════════════════════════════

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='生成数据报告')
    parser.add_argument('--template', choices=['weekly', 'funnel', 'sales', 'custom'],
                       default='weekly', help='报告模板')
    parser.add_argument('--output', default='report.html', help='输出文件路径')
    parser.add_argument('--data', help='数据文件路径（CSV）')
    args = parser.parse_args()

    # 示例：生成模拟报告
    print(f"生成报告: {args.output}")
    print("使用模板:", args.template)
