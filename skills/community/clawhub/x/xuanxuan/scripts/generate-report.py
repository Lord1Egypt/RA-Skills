#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["rich"]
# ///
"""
滚滚技能健康度可视化报告生成器

生成 Markdown 格式的报告，包含图表和统计。
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from rich.console import Console

console = Console()

# 数据目录
DATA_DIR = Path.home() / ".openclaw" / "data" / "gungun"
HEALTH_DIR = DATA_DIR / "health-scores"
REPORTS_DIR = Path.home() / ".openclaw" / "workspace" / "skills" / "优化记录"

# 确保目录存在
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

def load_health_data(days: int = 30):
    """加载健康度数据"""
    cutoff = datetime.now() - timedelta(days=days)
    all_scores = []
    
    console.print(f"[dim]从 {HEALTH_DIR} 加载健康度数据...[/dim]")
    
    # 尝试直接读取健康度文件
    for file in HEALTH_DIR.glob("*.json"):
        console.print(f"[dim]检查文件：{file.name}[/dim]")
        try:
            content = file.read_text(encoding="utf-8")
            data = json.loads(content)
            
            # 检查是否是带 skills 键的格式
            if isinstance(data, dict) and "skills" in data:
                for skill_data in data.get("skills", []):
                    try:
                        # 兼容的日期解析
                        ts = skill_data["timestamp"]
                        score_time = datetime.strptime(ts[:19], "%Y-%m-%dT%H:%M:%S")
                        if score_time >= cutoff:
                            all_scores.append(skill_data)
                    except Exception as e:
                        console.print(f"[dim]解析时间戳失败：{e}[/dim]")
                        continue
        except Exception as e:
            console.print(f"[dim]读取失败：{e}[/dim]")
            continue
    
    console.print(f"[dim]加载了 {len(all_scores)} 条记录[/dim]")
    return all_scores

def generate_ascii_chart(values: list, labels: list, title: str = "", width: int = 50):
    """生成 ASCII 图表"""
    if not values:
        return ""
    
    max_val = max(values) if values else 1
    min_val = min(values) if values else 0
    
    lines = []
    lines.append(f"\n{title}\n")
    
    # 简单柱状图
    for i, (val, label) in enumerate(zip(values, labels)):
        bar_len = int((val / max_val) * width) if max_val > 0 else 0
        bar = "█" * bar_len
        lines.append(f"{label:15} {bar} {val:.1f}")
    
    return "\n".join(lines)

def generate_report(days: int = 30):
    """生成健康度报告"""
    all_scores = load_health_data(days)
    
    if not all_scores:
        console.print("[yellow]暂无健康度数据[/yellow]")
        return None
    
    # 统计
    total_skills = len(all_scores)
    healthy = len([s for s in all_scores if s["total"] >= 8])
    warning = len([s for s in all_scores if 6 <= s["total"] < 8])
    alert = len([s for s in all_scores if 4 <= s["total"] < 6])
    danger = len([s for s in all_scores if s["total"] < 4])
    
    # 按总分排序
    sorted_scores = sorted(all_scores, key=lambda x: x["total"], reverse=True)
    top_5 = sorted_scores[:5]
    bottom_5 = sorted_scores[-5:]
    
    # 生成报告
    report = []
    report.append("# 🌪️ 滚滚技能健康度报告\n")
    report.append(f"**报告周期：** 过去 {days} 天\n")
    report.append(f"**生成时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report.append(f"**技能总数：** {total_skills}\n")
    
    # 整体统计
    report.append("\n## 📊 整体统计\n")
    report.append(f"- 🟢 健康（8-10 分）：{healthy} 个 ({healthy/total_skills*100:.1f}%)\n")
    report.append(f"- 🟡 观察（6-7 分）：{warning} 个 ({warning/total_skills*100:.1f}%)\n")
    report.append(f"- 🟠 警告（4-5 分）：{alert} 个 ({alert/total_skills*100:.1f}%)\n")
    report.append(f"- 🔴 危险（0-3 分）：{danger} 个 ({danger/total_skills*100:.1f}%)\n")
    
    # 健康度分布图
    report.append("\n## 📈 健康度分布\n")
    distribution = [healthy, warning, alert, danger]
    labels = ["🟢 健康", "🟡 观察", "🟠 警告", "🔴 危险"]
    report.append(generate_ascii_chart(distribution, labels, "", width=30))
    
    # Top 5 健康技能
    report.append("\n## 🏆 Top 5 健康技能\n")
    for i, skill in enumerate(top_5, 1):
        report.append(f"{i}. **{skill['skill']}** - {skill['total']:.1f} 分")
        report.append(f"   - 使用频率：{skill['scores']['usage']:.1f}")
        report.append(f"   - 成功率：{skill['scores']['success']:.1f}")
        report.append(f"   - 性能：{skill['scores']['performance']:.1f}\n")
    
    # 需要关注的技能
    if any(s["total"] < 6 for s in all_scores):
        report.append("\n## ⚠️ 需要关注的技能\n")
        for skill in bottom_5:
            if skill["total"] < 6:
                emoji = "🟠" if skill["total"] >= 4 else "🔴"
                report.append(f"{emoji} **{skill['skill']}** - {skill['total']:.1f} 分")
                report.append(f"   - 主要问题：")
                
                if skill["scores"]["usage"] < 5:
                    report.append(f"     - 使用频率低 ({skill['scores']['usage']:.1f}分)")
                if skill["scores"]["success"] < 7:
                    report.append(f"     - 成功率低 ({skill['scores']['success']:.1f}分)")
                if skill["scores"]["performance"] < 6:
                    report.append(f"     - 性能差 ({skill['scores']['performance']:.1f}分)")
                
                report.append("")
    
    # 趋势分析（如果有历史数据）
    report.append("\n## 📉 趋势分析\n")
    report.append("*需要更多历史数据才能显示趋势*\n")
    
    # 建议
    report.append("\n## 💡 优化建议\n")
    if danger > 0:
        report.append(f"🔴 **紧急：** {danger} 个技能健康度低于 4 分，建议立即审查\n")
    if alert > 0:
        report.append(f"🟠 **重要：** {alert} 个技能健康度低于 6 分，建议本周内优化\n")
    if healthy / total_skills > 0.8:
        report.append("✅ **优秀：** 80% 以上技能健康度良好，继续保持！\n")
    
    report.append("\n---\n")
    report.append("*报告由 skill-tracker 自动生成*\n")
    
    return "\n".join(report)

def save_report(report: str):
    """保存报告"""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    
    today = datetime.now().strftime("%Y-%m-%d")
    report_file = REPORTS_DIR / f"skill-health-report-{today}.md"
    
    report_file.write_text(report, encoding="utf-8")
    console.print(f"[green]✓ 报告已保存：{report_file}[/green]\n")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="滚滚技能健康度报告生成器")
    parser.add_argument("--generate", action="store_true", help="生成报告")
    parser.add_argument("--days", type=int, default=30, help="报告周期（默认 30 天）")
    parser.add_argument("--output", action="store_true", help="输出到控制台")
    
    args = parser.parse_args()
    
    if args.generate:
        report = generate_report(args.days)
        if report:
            save_report(report)
            if args.output:
                console.print("\n[bold]报告预览：[/bold]\n")
                console.print(report)
    else:
        parser.print_help()
