#!/usr/bin/env python3
"""生成HTML版生产周报"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# HTML模板 - 内嵌CSS样式
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>生产管理周报 | {week_id}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif; background: #f5f7fa; color: #333; line-height: 1.6; }}
        .container {{ max-width: 1000px; margin: 40px auto; padding: 0 20px; }}
        .header {{ background: linear-gradient(135deg, #1a73e8, #0d47a1); color: white; padding: 40px; border-radius: 12px; margin-bottom: 30px; box-shadow: 0 4px 20px rgba(26,115,232,0.3); }}
        .header h1 {{ font-size: 28px; margin-bottom: 10px; }}
        .header .meta {{ opacity: 0.9; font-size: 14px; }}
        .header .meta span {{ margin-right: 20px; }}
        .section {{ background: white; border-radius: 12px; padding: 30px; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }}
        .section h2 {{ color: #1a73e8; font-size: 18px; border-left: 4px solid #1a73e8; padding-left: 12px; margin-bottom: 20px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
        th {{ background: #f8f9fa; text-align: left; padding: 12px 15px; font-weight: 600; border-bottom: 2px solid #e0e0e0; }}
        td {{ padding: 12px 15px; border-bottom: 1px solid #eee; }}
        tr:hover {{ background: #f8f9fa; }}
        .metric-high {{ color: #34a853; font-weight: 600; }}
        .metric-low {{ color: #ea4335; font-weight: 600; }}
        .status-badge {{ display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 500; }}
        .status-ok {{ background: #e6f4ea; color: #34a853; }}
        .status-warning {{ background: #fef7e0; color: #f9a825; }}
        .status-error {{ background: #fce8e6; color: #ea4335; }}
        .status-progress {{ background: #e8f0fe; color: #1a73e8; }}
        .todo-list {{ list-style: none; }}
        .todo-list li {{ padding: 10px 0; border-bottom: 1px solid #eee; display: flex; align-items: flex-start; }}
        .todo-list li:last-child {{ border-bottom: none; }}
        .todo-list .check {{ width: 20px; height: 20px; border: 2px solid #1a73e8; border-radius: 4px; margin-right: 12px; flex-shrink: 0; margin-top: 2px; }}
        .todo-list .check.checked {{ background: #1a73e8; position: relative; }}
        .todo-list .check.checked::after {{ content: "✓"; color: white; font-size: 14px; position: absolute; top: -2px; left: 3px; }}
        .todo-list .pending .check {{ border-color: #9e9e9e; background: #f5f5f5; }}
        .issue-card {{ background: #fef7e0; border-left: 4px solid #f9a825; padding: 15px 20px; margin: 10px 0; border-radius: 0 8px 8px 0; }}
        .issue-card.resolved {{ background: #e6f4ea; border-left-color: #34a853; }}
        .tracking {{ background: #e8f0fe; padding: 15px 20px; border-radius: 8px; margin: 10px 0; }}
        .tracking .week-tag {{ background: #1a73e8; color: white; padding: 2px 10px; border-radius: 10px; font-size: 12px; margin-right: 10px; }}
        .footer {{ text-align: center; color: #999; font-size: 12px; padding: 20px; }}
        .highlight {{ background: linear-gradient(120deg, #e8f0fe 0%, #e8f0fe 100%); padding: 2px 6px; border-radius: 4px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>生产管理周报</h1>
            <div class="meta">
                <span>📅 {date}</span>
                <span>📆 {week_id}</span>
                <span>👤 {author}</span>
            </div>
        </div>

        <div class="section">
            <h2>本周概况</h2>
            <p>{overview}</p>
            <table>
                <thead>
                    <tr>
                        <th>核心指标</th>
                        <th>本周实际</th>
                        <th>目标值</th>
                        <th>达成率</th>
                        <th>状态</th>
                    </tr>
                </thead>
                <tbody>
                    {metrics_rows}
                </tbody>
            </table>
        </div>

        <div class="section">
            <h2>生产数据</h2>
            <table>
                <thead>
                    <tr>
                        <th>产线</th>
                        <th>产量</th>
                        <th>良率</th>
                        <th>OEE</th>
                        <th>备注</th>
                    </tr>
                </thead>
                <tbody>
                    {production_rows}
                </tbody>
            </table>
            {production_analysis}
        </div>

        <div class="section">
            <h2>完成事项</h2>
            <ul class="todo-list">
                {completed_items}
            </ul>
            {in_progress}
        </div>

        <div class="section">
            <h2>异常与问题</h2>
            {new_issues}
            {tracked_issues}
        </div>

        <div class="section">
            <h2>下周计划</h2>
            <ul class="todo-list">
                {next_week_plan}
            </ul>
            {next_week_forecast}
        </div>

        <div class="section">
            <h2>需协调事项</h2>
            {pending_matters}
        </div>

        <div class="footer">
            <p>周报生成时间: {generated_at}</p>
        </div>
    </div>
</body>
</html>"""


def generate_html(data: dict, output_path: str) -> dict:
    """根据数据生成HTML周报"""
    try:
        week_id = data.get("week_id", datetime.now().strftime("%Y-W%V"))
        date = data.get("date", datetime.now().strftime("%Y-%m-%d"))
        author = data.get("author", "生产管理")
        
        # 生成指标行
        metrics = data.get("metrics", [])
        metrics_rows = ""
        for m in metrics:
            name = m.get("name", "")
            actual = m.get("actual", "")
            target = m.get("target", "")
            rate = m.get("rate", "")
            status_class = "status-ok" if float(rate.rstrip("%")) >= 100 else "status-warning" if float(rate.rstrip("%")) >= 90 else "status-error"
            status_text = "达标" if float(rate.rstrip("%")) >= 100 else "接近" if float(rate.rstrip("%")) >= 90 else "未达"
            metrics_rows += f'<tr><td>{name}</td><td>{actual}</td><td>{target}</td><td>{rate}</td><td><span class="status-badge {status_class}">{status_text}</span></td></tr>\n'
        
        # 生成产线数据行
        production = data.get("production", [])
        production_rows = ""
        for p in production:
            production_rows += f'<tr><td>{p.get("line", "")}</td><td>{p.get("output", "")}</td><td>{p.get("quality", "")}</td><td>{p.get("oee", "")}</td><td>{p.get("note", "-")}</td></tr>\n'
        production_analysis = f'<p><strong>数据分析：</strong>{data.get("production_analysis", "暂无")}</p>' if data.get("production_analysis") else ""
        
        # 生成完成事项
        completed_items = ""
        for item in data.get("completed", []):
            completed_items += f'<li><span class="check checked"></span><div><strong>{item.get("title", "")}</strong><br><span style="color:#666">{item.get("result", "")}</span></div></li>\n'
        
        # 生成进行中项目
        in_progress = ""
        if data.get("in_progress"):
            in_progress = '<h3 style="color:#666;font-size:14px;margin:20px 0 10px">进行中项目</h3><ul class="todo-list">'
            for item in data.get("in_progress"):
                in_progress += f'<li class="pending"><span class="check"></span><div><strong>{item.get("title", "")}</strong><br><span style="color:#666">{item.get("progress", "")}</span></div></li>\n'
            in_progress += '</ul>'
        
        # 生成异常问题
        issues_html = ""
        for issue in data.get("issues", []):
            status_class = "resolved" if issue.get("status") == "已解决" else ""
            issues_html += f'''<div class="issue-card {status_class}">
                <strong>{issue.get("type", "异常")}</strong>：{issue.get("desc", "")}<br>
                <span style="color:#666">影响：{issue.get("impact", "")}</span> | 
                <span style="color:#666">处理：{issue.get("solution", "")}</span> |
                <span class="status-badge {"status-ok" if issue.get("status") == "已解决" else "status-warning"}">{issue.get("status", "待处理")}</span>
            </div>\n'''
        if not issues_html:
            issues_html = '<p style="color:#34a853">本周无新增异常</p>'
        
        # 遗留问题追踪
        tracked_html = ""
        if data.get("tracked_issues"):
            tracked_html = '<h3 style="color:#1a73e8;font-size:14px;margin:20px 0 10px">遗留问题追踪</h3>'
            for t in data.get("tracked_issues"):
                tracked_html += f'''<div class="tracking">
                    <span class="week-tag">{t.get("week", "")}</span>
                    <strong>{t.get("desc", "")}</strong> — 持续{t.get("weeks", "1")}周 | {t.get("status", "")}
                </div>\n'''
        
        # 下周计划
        plan_html = ""
        for item in data.get("next_week", []):
            plan_html += f'<li class="pending"><span class="check"></span><div><strong>{item.get("title", "")}</strong><br><span style="color:#666">目标：{item.get("target", "")}</span></div></li>\n'
        
        # 下周预计
        forecast_html = ""
        if data.get("next_week_metrics"):
            forecast_html = '<h3 style="color:#666;font-size:14px;margin:20px 0 10px">预计产出</h3><table><tr><th>指标</th><th>预计值</th><th>备注</th></tr>'
            for m in data.get("next_week_metrics"):
                forecast_html += f'<tr><td>{m.get("name", "")}</td><td>{m.get("value", "")}</td><td>{m.get("note", "-")}</td></tr>\n'
            forecast_html += '</table>'
        
        # 需协调事项
        pending_html = ""
        if data.get("pending"):
            pending_html = '<table><tr><th>事项</th><th>需求</th><th>期望支持</th><th>优先级</th></tr>'
            for p in data.get("pending"):
                priority_class = "status-error" if p.get("priority") == "高" else "status-warning" if p.get("priority") == "中" else "status-ok"
                pending_html += f'<tr><td>{p.get("title", "")}</td><td>{p.get("need", "")}</td><td>{p.get("support", "")}</td><td><span class="status-badge {priority_class}">{p.get("priority", "中")}</span></td></tr>\n'
            pending_html += '</table>'
        else:
            pending_html = '<p style="color:#666">无协调事项</p>'
        
        # 渲染模板
        html = HTML_TEMPLATE.format(
            week_id=week_id,
            date=date,
            author=author,
            overview=data.get("overview", "暂无概述"),
            metrics_rows=metrics_rows or "<tr><td colspan='5'>暂无数据</td></tr>",
            production_rows=production_rows or "<tr><td colspan='5'>暂无数据</td></tr>",
            production_analysis=production_analysis,
            completed_items=completed_items or "<li>暂无完成事项</li>",
            in_progress=in_progress,
            new_issues=issues_html,
            tracked_issues=tracked_html,
            next_week_plan=plan_html or "<li>暂无下周计划</li>",
            next_week_forecast=forecast_html,
            pending_matters=pending_html,
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M")
        )
        
        # 写入文件
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_text(html, encoding="utf-8")
        
        return {"status": "success", "output": output_path}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}


def main():
    parser = argparse.ArgumentParser(description="生成HTML版生产周报")
    parser.add_argument("--data", required=True, help="JSON数据或JSON文件路径(@file:xxx)")
    parser.add_argument("--output", required=True, help="输出HTML路径")
    args = parser.parse_args()
    
    # 支持@file:读取文件
    if args.data.startswith("@file:"):
        data = json.loads(Path(args.data[6:]).read_text(encoding="utf-8"))
    else:
        data = json.loads(args.data)
    
    result = generate_html(data, args.output)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
