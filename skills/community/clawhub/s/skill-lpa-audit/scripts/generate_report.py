"""
LPA审核报告生成脚本
根据分析数据生成结构化HTML审核报告
"""

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List


def load_template() -> str:
    """加载报告HTML模板"""
    template_path = Path(__file__).parent.parent / "assets" / "templates" / "report_template.html"
    if template_path.exists():
        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()
    return None


def load_analysis_data(data_path: str) -> Dict:
    """加载分析数据"""
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_report_html(data: Dict, output_path: str):
    """生成HTML报告"""
    
    # 尝试加载模板
    template = load_template()
    
    if template:
        # 使用模板生成
        html = _render_template(template, data)
    else:
        # 内联生成
        html = _generate_inline_html(data)
    
    # 写入文件
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)


def _render_template(template: str, data: Dict) -> str:
    """使用Jinja2渲染模板"""
    try:
        from jinja2 import Template
        t = Template(template)
        return t.render(**data, datetime=datetime)
    except ImportError:
        # 回退到内联生成
        return _generate_inline_html(data)


def _generate_inline_html(data: Dict) -> str:
    """生成内联HTML报告"""
    
    audit_summary = data.get("audit_summary", {})
    statistics = data.get("statistics", {})
    pass_rate = data.get("pass_rate", 0)
    category_analysis = data.get("category_analysis", [])
    top_issues = data.get("top_issues", [])
    recommendations = data.get("recommendations", [])
    
    # 生成问题表格行
    issues_rows = ""
    for i, issue in enumerate(top_issues, 1):
        issues_rows += f"""
        <tr>
            <td>{i}</td>
            <td>{issue.get('item_id', '')}</td>
            <td>{issue.get('name', '')}</td>
            <td><span class="badge badge-{_get_category_color(issue.get('category', ''))}">{issue.get('category', '')}</span></td>
            <td>{issue.get('evidence', '')}</td>
            <td>{issue.get('note', '')}</td>
        </tr>
        """
    
    # 生成分类分析行
    category_rows = ""
    for cat in category_analysis:
        category_rows += f"""
        <tr>
            <td><span class="badge badge-{_get_category_color(cat.get('category', ''))}">{cat.get('category', '')}</span></td>
            <td>{cat.get('name', '')}</td>
            <td>{cat.get('total', 0)}</td>
            <td>{cat.get('pass', 0)}</td>
            <td>{cat.get('fail', 0)}</td>
            <td class="{'text-success' if cat.get('pass_rate', 0) >= 95 else 'text-warning' if cat.get('pass_rate', 0) >= 85 else 'text-danger'}">{cat.get('pass_rate', 0)}%</td>
        </tr>
        """
    
    # 生成建议行
    rec_rows = ""
    for i, rec in enumerate(recommendations, 1):
        rec_rows += f"""
        <tr>
            <td>{i}</td>
            <td><span class="badge badge-{'danger' if rec.get('priority') == '高' else 'warning'}">{rec.get('priority', '')}</span></td>
            <td>{rec.get('area', '')}</td>
            <td>{rec.get('suggestion', '')}</td>
        </tr>
        """
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LPA分层审核报告</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: "Microsoft YaHei", Arial, sans-serif; font-size: 14px; color: #333; line-height: 1.6; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        
        /* 头部样式 */
        .report-header {{ background: linear-gradient(135deg, #1a5276 0%, #2980b9 100%); color: white; padding: 30px; border-radius: 8px; margin-bottom: 20px; }}
        .report-header h1 {{ font-size: 28px; margin-bottom: 10px; }}
        .report-header .subtitle {{ opacity: 0.9; font-size: 16px; }}
        .report-meta {{ display: flex; gap: 30px; margin-top: 20px; }}
        .report-meta .meta-item {{ background: rgba(255,255,255,0.15); padding: 10px 15px; border-radius: 5px; }}
        .report-meta .meta-label {{ font-size: 12px; opacity: 0.8; }}
        .report-meta .meta-value {{ font-size: 16px; font-weight: bold; }}
        
        /* 统计卡片 */
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px; }}
        .stat-card {{ background: white; border-radius: 8px; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.08); text-align: center; }}
        .stat-card .stat-value {{ font-size: 36px; font-weight: bold; color: #2980b9; }}
        .stat-card .stat-label {{ color: #666; font-size: 14px; margin-top: 5px; }}
        .stat-card.highlight {{ background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%); color: white; }}
        .stat-card.highlight .stat-value {{ color: white; }}
        .stat-card.highlight .stat-label {{ color: rgba(255,255,255,0.9); }}
        
        /* 区块样式 */
        .section {{ background: white; border-radius: 8px; padding: 25px; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.08); }}
        .section-title {{ font-size: 18px; color: #1a5276; border-bottom: 2px solid #2980b9; padding-bottom: 10px; margin-bottom: 20px; }}
        
        /* 表格样式 */
        table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
        th {{ background: #f8f9fa; padding: 12px 10px; text-align: left; font-weight: 600; border-bottom: 2px solid #dee2e6; }}
        td {{ padding: 10px; border-bottom: 1px solid #dee2e6; }}
        tr:hover {{ background: #f8f9fa; }}
        
        /* 徽章样式 */
        .badge {{ display: inline-block; padding: 3px 8px; border-radius: 3px; font-size: 12px; font-weight: bold; }}
        .badge-EQP {{ background: #e3f2fd; color: #1565c0; }}
        .badge-MAT {{ background: #fff3e0; color: #ef6c00; }}
        .badge-MTH {{ background: #e8f5e9; color: #2e7d32; }}
        .badge-PPE {{ background: #fce4ec; color: #c2185b; }}
        .badge-ENV {{ background: #f3e5f5; color: #7b1fa2; }}
        .badge-MSR {{ background: #e0f7fa; color: #00838f; }}
        .badge-danger {{ background: #ffebee; color: #c62828; }}
        .badge-warning {{ background: #fff8e1; color: #f57f17; }}
        
        /* 状态样式 */
        .text-success {{ color: #27ae60; font-weight: bold; }}
        .text-warning {{ color: #f39c12; font-weight: bold; }}
        .text-danger {{ color: #e74c3c; font-weight: bold; }}
        
        /* 页脚 */
        .footer {{ text-align: center; color: #666; font-size: 12px; padding: 20px; border-top: 1px solid #dee2e6; margin-top: 20px; }}
        
        /* 打印样式 */
        @media print {{ 
            body {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
            .section {{ box-shadow: none; border: 1px solid #ddd; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- 报告头部 -->
        <div class="report-header">
            <h1>LPA分层审核报告</h1>
            <div class="subtitle">Layered Process Audit Report</div>
            <div class="report-meta">
                <div class="meta-item">
                    <div class="meta-label">审核编号</div>
                    <div class="meta-value">{audit_summary.get('audit_id', 'N/A')}</div>
                </div>
                <div class="meta-item">
                    <div class="meta-label">审核层级</div>
                    <div class="meta-value">{audit_summary.get('level', 'N/A')}</div>
                </div>
                <div class="meta-item">
                    <div class="meta-label">审核部门</div>
                    <div class="meta-value">{audit_summary.get('department', 'N/A')}</div>
                </div>
                <div class="meta-item">
                    <div class="meta-label">审核时间</div>
                    <div class="meta-value">{audit_summary.get('audit_time', 'N/A')}</div>
                </div>
                <div class="meta-item">
                    <div class="meta-label">审核人</div>
                    <div class="meta-value">{audit_summary.get('auditor', 'N/A')}</div>
                </div>
            </div>
        </div>
        
        <!-- 统计概览 -->
        <div class="stats-grid">
            <div class="stat-card highlight">
                <div class="stat-value">{pass_rate}%</div>
                <div class="stat-label">整体通过率</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{statistics.get('total', 0)}</div>
                <div class="stat-label">检查项总数</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" style="color: #27ae60;">{statistics.get('pass', 0)}</div>
                <div class="stat-label">合格项</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" style="color: #e74c3c;">{statistics.get('fail', 0)}</div>
                <div class="stat-label">不合格项</div>
            </div>
        </div>
        
        <!-- 分类分析 -->
        <div class="section">
            <h2 class="section-title">按分类统计分析</h2>
            <table>
                <thead>
                    <tr>
                        <th>分类代码</th>
                        <th>分类名称</th>
                        <th>检查项</th>
                        <th>合格</th>
                        <th>不合格</th>
                        <th>通过率</th>
                    </tr>
                </thead>
                <tbody>
                    {category_rows if category_rows else '<tr><td colspan="6">暂无数据</td></tr>'}
                </tbody>
            </table>
        </div>
        
        <!-- 问题清单 -->
        <div class="section">
            <h2 class="section-title">不合格项详情（TOP问题）</h2>
            <table>
                <thead>
                    <tr>
                        <th>序号</th>
                        <th>编号</th>
                        <th>检查项</th>
                        <th>分类</th>
                        <th>证据/现象</th>
                        <th>备注</th>
                    </tr>
                </thead>
                <tbody>
                    {issues_rows if issues_rows else '<tr><td colspan="6">无不合格项</td></tr>'}
                </tbody>
            </table>
        </div>
        
        <!-- 改进建议 -->
        <div class="section">
            <h2 class="section-title">改进建议</h2>
            <table>
                <thead>
                    <tr>
                        <th>序号</th>
                        <th>优先级</th>
                        <th>改善领域</th>
                        <th>建议内容</th>
                    </tr>
                </thead>
                <tbody>
                    {rec_rows if rec_rows else '<tr><td colspan="4">暂无建议</td></tr>'}
                </tbody>
            </table>
        </div>
        
        <!-- 页脚 -->
        <div class="footer">
            <p>报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Generated by LPA Audit System</p>
        </div>
    </div>
</body>
</html>"""
    
    return html


def _get_category_color(category: str) -> str:
    """获取分类对应的颜色类名"""
    colors = {
        "EQP": "EQP",
        "MAT": "MAT",
        "MTH": "MTH",
        "PPE": "PPE",
        "ENV": "ENV",
        "MSR": "MSR",
    }
    return colors.get(category, "EQP")


def main():
    parser = argparse.ArgumentParser(description="LPA审核报告生成工具")
    parser.add_argument("--level", required=True,
                        help="审核层级(L1/L2/L3/L4/all)")
    parser.add_argument("--period", required=True,
                        help="审核周期(YYYY-MM或YYYY-QN格式)")
    parser.add_argument("--data", required=True,
                        help="分析数据文件路径")
    parser.add_argument("--output", required=True,
                        help="报告输出路径(.html格式)")
    
    args = parser.parse_args()
    
    # 加载分析数据
    analysis_data = load_analysis_data(args.data)
    
    # 增强报告信息
    report_data = {
        **analysis_data,
        "level": args.level,
        "period": args.period,
    }
    
    # 生成报告
    generate_report_html(report_data, args.output)
    
    # 输出摘要
    print(json.dumps({
        "status": "success",
        "level": args.level,
        "period": args.period,
        "pass_rate": analysis_data.get("pass_rate", 0),
        "fail_items": analysis_data.get("statistics", {}).get("fail", 0),
        "output_file": args.output,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
