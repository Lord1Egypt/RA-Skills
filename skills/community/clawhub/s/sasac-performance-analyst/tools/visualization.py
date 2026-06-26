#!/usr/bin/env python3
"""
Visualization Tools - 可视化工具
生成雷达图、柱状图、趋势图和诊断报告

Author: 王东杰 (Wang Dongjie)
License: MIT
Version: 2.0.0
"""

import json
import os
from typing import Dict, List, Optional

try:
    import matplotlib
    matplotlib.use('Agg')  # non-interactive backend
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


# ─── Radar Chart ─────────────────────────────────────────────────

DIMENSION_LABELS = {
    "盈利回报": "盈利回报\nProfitability",
    "资产运营": "资产运营\nOperations", 
    "风险防控": "风险防控\nRisk Control",
    "持续发展": "持续发展\nGrowth",
}


def generate_radar_chart(scores: Dict[str, float], title: str = "绩效雷达图",
                          output_path: Optional[str] = None,
                          theme: str = "dark") -> Optional[str]:
    """
    生成四维绩效雷达图
    
    Args:
        scores: {"盈利回报": 72.5, "资产运营": 68.0, ...}
        title: 图表标题
        output_path: 输出路径（PNG），None=不保存
        theme: "dark" | "light"
    
    Returns:
        文件路径（如果保存成功）
    """
    if not HAS_MATPLOTLIB:
        print("⚠️  matplotlib not installed. Install with: pip install matplotlib")
        return None
    
    # Prepare data
    labels = []
    values = []
    for dim in ["盈利回报", "资产运营", "风险防控", "持续发展"]:
        labels.append(DIMENSION_LABELS.get(dim, dim))
        values.append(scores.get(dim, 0))
    
    # Repeat first value to close the polygon
    values.append(values[0])
    angles = [n / float(len(labels)) * 2 * 3.141592653589793 for n in range(len(labels))]
    angles.append(angles[0])
    
    # Setup figure
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(projection='polar'))
    
    if theme == "dark":
        fig.patch.set_facecolor('#0d1117')
        ax.set_facecolor('#0d1117')
        text_color = '#e6edf3'
        grid_color = '#21262d'
        fill_color = '#d4af37'
        fill_alpha = 0.25
        line_color = '#d4af37'
    else:
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')
        text_color = '#24292e'
        grid_color = '#e1e4e8'
        fill_color = '#0366d6'
        fill_alpha = 0.25
        line_color = '#0366d6'
    
    # Plot
    ax.plot(angles, values, color=line_color, linewidth=2, label=title)
    ax.fill(angles, values, color=fill_color, alpha=fill_alpha)
    
    # Labels
    ax.set_thetagrids([a * 180 / 3.141592653589793 for a in angles[:-1]], 
                        labels, color=text_color, fontsize=11)
    ax.set_ylim(0, 100)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(['E\n20', 'D\n40', 'C\n60', 'B\n80', 'A+\n100'],
                       color=text_color, fontsize=9)
    ax.grid(True, color=grid_color, linewidth=0.8)
    ax.spines['polar'].set_color(grid_color)
    
    # Title
    ax.set_title(title, color=text_color, fontsize=14, pad=20, 
                 fontweight='bold' if theme == "dark" else 'normal')
    
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight',
                    facecolor=fig.get_facecolor())
        plt.close(fig)
        return output_path
    else:
        plt.show()
        plt.close(fig)
        return None


def generate_bar_chart(data: Dict[str, float], title: str = "指标对比",
                        output_path: Optional[str] = None,
                        theme: str = "dark") -> Optional[str]:
    """
    生成柱状图
    
    Args:
        data: {"指标名": 值, ...}
        title: 图表标题
        output_path: 输出路径
        theme: "dark" | "light"
    """
    if not HAS_MATPLOTLIB:
        return None
    
    labels = list(data.keys())
    values = list(data.values())
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if theme == "dark":
        fig.patch.set_facecolor('#0d1117')
        ax.set_facecolor('#0d1117')
        text_color = '#e6edf3'
        bar_color = '#d4af37'
    else:
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')
        text_color = '#24292e'
        bar_color = '#0366d6'
    
    bars = ax.bar(labels, values, color=bar_color, alpha=0.8, edgecolor=text_color)
    
    ax.set_title(title, color=text_color, fontsize=14, fontweight='bold')
    ax.set_ylabel('得分', color=text_color)
    ax.tick_params(colors=text_color)
    ax.spines['bottom'].set_color(text_color)
    ax.spines['left'].set_color(text_color)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.label.set_color(text_color)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.0f}', ha='center', va='bottom', 
                color=text_color, fontsize=9)
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight',
                    facecolor=fig.get_facecolor())
        plt.close(fig)
        return output_path
    else:
        plt.show()
        plt.close(fig)
        return None


# ─── HTML Report Generator ────────────────────────────────────────

def generate_full_report(report_data: dict, output_format: str = "html",
                         output_path: Optional[str] = None) -> Optional[str]:
    """
    生成完整的绩效评价报告
    
    Args:
        report_data: full_diagnosis() 的返回结果
        output_format: "html" | "text"
        output_path: 输出路径
    
    Returns:
        文件路径
    """
    if output_format == "html":
        return _generate_html_report(report_data, output_path)
    elif output_format == "text":
        return _generate_text_report(report_data, output_path)
    else:
        raise ValueError(f"Unsupported format: {output_format}")


def _generate_html_report(data: dict, output_path: Optional[str]) -> str:
    """生成HTML格式报告"""
    composite = data.get("composite_score", 0)
    grade = data.get("grade", "N/A")
    dim_scores = data.get("dimension_scores", {})
    strengths = data.get("strengths", [])
    weaknesses = data.get("weaknesses", [])
    ind_results = data.get("indicator_results", {})
    
    # Color based on score
    if composite >= 85:
        score_color = "#2ea043"
    elif composite >= 70:
        score_color = "#d4af37"
    elif composite >= 55:
        score_color = "#d29922"
    elif composite >= 40:
        score_color = "#f85149"
    else:
        score_color = "#f85149"
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>绩效评价报告 - {data.get('industry', '')}</title>
<style>
  body {{ font-family: -apple-system, "Noto Serif SC", serif; background: #0d1117; color: #e6edf3; margin: 0; padding: 20px; }}
  .container {{ max-width: 900px; margin: 0 auto; }}
  .header {{ text-align: center; padding: 30px 0; border-bottom: 1px solid #21262d; margin-bottom: 30px; }}
  .header h1 {{ margin: 0; font-size: 28px; color: #d4af37; }}
  .score-section {{ text-align: center; margin: 30px 0; }}
  .score {{ font-size: 64px; font-weight: bold; color: {score_color}; font-family: "JetBrains Mono", monospace; }}
  .grade {{ font-size: 24px; color: #8b949e; margin-top: 8px; }}
  .dim-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin: 30px 0; }}
  .dim-card {{ background: #161b22; border: 1px solid #21262d; border-radius: 8px; padding: 20px; text-align: center; }}
  .dim-name {{ font-size: 14px; color: #8b949e; margin-bottom: 8px; }}
  .dim-score {{ font-size: 28px; font-weight: bold; font-family: "JetBrains Mono", monospace; }}
  .section {{ margin: 30px 0; }}
  .section-title {{ font-size: 18px; font-weight: 600; color: #d4af37; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 1px solid #21262d; }}
  .ind-table {{ width: 100%; border-collapse: collapse; }}
  .ind-table th {{ background: #161b22; color: #8b949e; padding: 8px 12px; font-size: 12px; text-align: left; }}
  .ind-table td {{ padding: 8px 12px; border-bottom: 1px solid #21262d; font-size: 13px; }}
  .level-a {{ color: #2ea043; }}
  .level-b {{ color: #d4af37; }}
  .level-c {{ color: #d29922; }}
  .level-d {{ color: #f85149; }}
  .strength {{ color: #2ea043; }}
  .weakness {{ color: #f85149; }}
  .footer {{ text-align: center; color: #8b949e; font-size: 12px; margin-top: 40px; padding-top: 20px; border-top: 1px solid #21262d; }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>📊 企业绩效评价报告</h1>
    <div style="color:#8b949e; margin-top:8px;">{data.get('industry', '')} · {data.get('size', '')}</div>
  </div>
  
  <div class="score-section">
    <div class="score">{composite}</div>
    <div class="grade">{grade}</div>
  </div>
  
  <div class="dim-grid">"""
    
    for dim, score in dim_scores.items():
        dim_color = "#2ea043" if score >= 80 else ("#d4af37" if score >= 60 else ("#d29922" if score >= 40 else "#f85149"))
        html += f"""
    <div class="dim-card">
      <div class="dim-name">{dim}</div>
      <div class="dim-score" style="color:{dim_color};">{score}</div>
    </div>"""
    
    html += """
  </div>"""
    
    if strengths:
        html += """
  <div class="section">
    <div class="section-title">✅ 优势维度</div>
    <div>""" + " ".join(f'<span class="strength">{s}</span>' for s in strengths) + """</div>
  </div>"""
    
    if weaknesses:
        html += """
  <div class="section">
    <div class="section-title">⚠️ 短板维度</div>
    <div>""" + " ".join(f'<span class="weakness">{w}</span>' for w in weaknesses) + """</div>
  </div>"""
    
    if ind_results:
        html += """
  <div class="section">
    <div class="section-title">📋 指标明细</div>
    <table class="ind-table">
      <tr>
        <th>指标</th><th>实际值</th><th>等级</th><th>得分</th>
      </tr>"""
        for key, res in ind_results.items():
            level_class = f"level-{res['level'][0].lower()}" if res['level'] else ""
            html += f"""
      <tr>
        <td>{res.get('indicator', key)}</td>
        <td>{res.get('value', '-')} {res.get('unit', '')}</td>
        <td class="{level_class}">{res.get('level', '-')}</td>
        <td>{res.get('score', '-')}</td>
      </tr>"""
        html += """
    </table>
  </div>"""
    
    html += """
  <div class="footer">
    由 SASAC Performance Analyst v2.0 生成 · 数据来源：国务院国资委考核分配局《企业绩效评价标准值（2025）》
  </div>
</div>
</body>
</html>"""
    
    if output_path is None:
        import tempfile
        fd, output_path = tempfile.mkstemp(suffix='.html', prefix='sasac_report_')
        os.close(fd)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return output_path


def _generate_text_report(data: dict, output_path: Optional[str]) -> str:
    """生成纯文本格式报告"""
    lines = []
    lines.append("=" * 60)
    lines.append("  企业绩效评价报告")
    lines.append("=" * 60)
    lines.append(f"行业：{data.get('industry', '')}  ·  规模：{data.get('size', '')}")
    lines.append("")
    lines.append(f"综合得分：{data.get('composite_score', 0)}  （{data.get('grade', '')}）")
    lines.append("")
    lines.append("-" * 60)
    lines.append("  维度得分：")
    for dim, score in data.get("dimension_scores", {}).items():
        lines.append(f"  {dim:8s}：{score}")
    lines.append("-" * 60)
    
    if data.get("strengths"):
        lines.append("")
        lines.append("✅ 优势维度：" + "、".join(data["strengths"]))
    if data.get("weaknesses"):
        lines.append("")
        lines.append("⚠️  短板维度：" + "、".join(data["weaknesses"]))
    
    lines.append("")
    lines.append("=" * 60)
    lines.append("  指标明细：")
    for key, res in data.get("indicator_results", {}).items():
        lines.append(f"  {res.get('indicator', key):12s}：{res.get('value', '-')} {res.get('unit', '')}  "
                     f"【{res.get('level', '-')}】得分{res.get('score', '-')}")
    lines.append("=" * 60)
    lines.append("  数据来源：国务院国资委考核分配局《企业绩效评价标准值（2025）》")
    lines.append("=" * 60)
    
    text = "\n".join(lines)
    
    if output_path is None:
        import tempfile
        fd, output_path = tempfile.mkstemp(suffix='.txt', prefix='sasac_report_')
        os.close(fd)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)
    
    return output_path


# ─── CLI Entry ───────────────────────────────────────────────────

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='SASAC可视化工具')
    parser.add_argument('--radar', action='store_true', help='生成雷达图')
    parser.add_argument('--bar', action='store_true', help='生成柱状图')
    parser.add_argument('--report', action='store_true', help='生成报告')
    parser.add_argument('--scores', help='JSON格式分数，如{"盈利回报":75,...}')
    parser.add_argument('--title', default='绩效雷达图', help='图表标题')
    parser.add_argument('--output', '-o', help='输出路径')
    parser.add_argument('--theme', default='dark', choices=['dark', 'light'])
    
    args = parser.parse_args()
    
    if args.radar and args.scores:
        scores = json.loads(args.scores)
        path = generate_radar_chart(scores, args.title, args.output, args.theme)
        print(f"✅ 雷达图已保存：{path}")
    elif args.bar and args.scores:
        scores = json.loads(args.scores)
        path = generate_bar_chart(scores, args.title, args.output, args.theme)
        print(f"✅ 柱状图已保存：{path}")
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
