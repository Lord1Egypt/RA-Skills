#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["rich"]
# ///
"""
滚滚技能健康度评分系统

根据使用数据计算每个技能的健康度评分（0-10 分）。
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from rich import print as rprint

console = Console()

# 数据目录
DATA_DIR = Path.home() / ".openclaw" / "data" / "gungun"
USAGE_DIR = DATA_DIR / "skill-usage"
HEALTH_DIR = DATA_DIR / "health-scores"

def get_all_skills():
    """获取所有技能列表"""
    skills_dir = Path.home() / ".openclaw" / "workspace" / "skills"
    if not skills_dir.exists():
        return []
    
    skills = []
    for item in skills_dir.iterdir():
        if item.is_dir() and not item.name.startswith(".") and item.name not in ["archive", "优化记录"]:
            skills.append(item.name)
    
    return sorted(skills)

def calculate_health_score(skill_name: str, days: int = 30):
    """
    计算技能健康度评分
    
    5 个维度，每个 0-10 分：
    - 使用频率（30%）：过去 7 天使用次数
    - 成功率（25%）：成功调用 / 总调用
    - 满意度（20%）：平均评分（如有）
    - 性能（15%）：平均响应时间
    - 维护（10%）：最后更新时间
    
    Returns:
        dict: 评分详情
    """
    # 直接实现获取数据的逻辑，避免导入问题
    import sys
    from pathlib import Path
    
    USAGE_DIR = Path.home() / ".openclaw" / "data" / "gungun" / "skill-usage"
    
    def get_usage_data_local(skill_name: str = None, days: int = 30):
        records = []
        from datetime import timedelta
        cutoff_date = datetime.now() - timedelta(days=days)
        
        for file in USAGE_DIR.glob("*.jsonl"):
            for line in file.read_text(encoding="utf-8").splitlines():
                try:
                    record = json.loads(line)
                    record_time = datetime.fromisoformat(record["timestamp"])
                    
                    if record_time >= cutoff_date:
                        if skill_name is None or record["skill"] == skill_name:
                            records.append(record)
                except:
                    continue
        
        return records
    
    get_usage_data = get_usage_data_local
    
    records = get_usage_data(skill_name, days)
    
    # 1. 使用频率（0-10 分）
    # 过去 7 天使用次数：0 次=0 分，1-2 次=3 分，3-5 次=6 分，6-10 次=8 分，>10 次=10 分
    week_records = get_usage_data(skill_name, 7)
    usage_count = len(week_records)
    
    if usage_count == 0:
        usage_score = 0
    elif usage_count <= 2:
        usage_score = 3
    elif usage_count <= 5:
        usage_score = 6
    elif usage_count <= 10:
        usage_score = 8
    else:
        usage_score = 10
    
    # 2. 成功率（0-10 分）
    if not records:
        success_score = 5  # 无数据给平均分
    else:
        success_rate = len([r for r in records if r["success"]]) / len(records) * 100
        success_score = success_rate / 10  # 转换为 0-10 分
    
    # 3. 满意度（0-10 分）
    satisfaction_scores = [r["user_satisfaction"] for r in records if r.get("user_satisfaction")]
    if satisfaction_scores:
        satisfaction_score = sum(satisfaction_scores) / len(satisfaction_scores) * 2  # 1-5 转换为 0-10
    else:
        satisfaction_score = 7  # 无评分给中上分
    
    # 4. 性能（0-10 分）
    # 平均响应时间：<500ms=10 分，500-1000ms=8 分，1000-2000ms=6 分，2000-5000ms=4 分，>5000ms=2 分
    durations = [r["duration_ms"] for r in records if r.get("duration_ms")]
    if durations:
        avg_duration = sum(durations) / len(durations)
        if avg_duration < 500:
            performance_score = 10
        elif avg_duration < 1000:
            performance_score = 8
        elif avg_duration < 2000:
            performance_score = 6
        elif avg_duration < 5000:
            performance_score = 4
        else:
            performance_score = 2
    else:
        performance_score = 7  # 无数据给中上分
    
    # 5. 维护（0-10 分）
    # 最后更新时间：<30 天=10 分，30-60 天=8 分，60-90 天=6 分，>90 天=4 分
    skills_dir = Path.home() / ".openclaw" / "workspace" / "skills"
    skill_path = skills_dir / skill_name
    
    if skill_path.exists():
        last_modified = datetime.fromtimestamp(skill_path.stat().st_mtime)
        days_since_update = (datetime.now() - last_modified).days
        
        if days_since_update < 30:
            maintenance_score = 10
        elif days_since_update < 60:
            maintenance_score = 8
        elif days_since_update < 90:
            maintenance_score = 6
        else:
            maintenance_score = 4
    else:
        maintenance_score = 5
    
    # 计算总分（加权平均）
    total_score = (
        usage_score * 0.30 +
        success_score * 0.25 +
        satisfaction_score * 0.20 +
        performance_score * 0.15 +
        maintenance_score * 0.10
    )
    
    return {
        "skill": skill_name,
        "timestamp": datetime.now().isoformat(),
        "scores": {
            "usage": round(usage_score, 1),
            "success": round(success_score, 1),
            "satisfaction": round(satisfaction_score, 1),
            "performance": round(performance_score, 1),
            "maintenance": round(maintenance_score, 1),
        },
        "total": round(total_score, 1),
        "stats": {
            "usage_count_7d": usage_count,
            "total_records": len(records),
            "success_rate": round(success_rate if records else 0, 1),
            "avg_duration_ms": round(sum(durations) / len(durations), 0) if durations else 0,
            "days_since_update": days_since_update if skill_path.exists() else -1,
        }
    }

def get_health_level(score: float):
    """获取健康等级"""
    if score >= 8:
        return "🟢", "健康"
    elif score >= 6:
        return "🟡", "观察"
    elif score >= 4:
        return "🟠", "警告"
    else:
        return "🔴", "危险"

def save_health_report(report: dict):
    """保存健康度报告"""
    HEALTH_DIR.mkdir(parents=True, exist_ok=True)
    
    today = datetime.now().strftime("%Y-%m-%d")
    report_file = HEALTH_DIR / f"{today}.json"
    
    # 如果已有报告，追加
    if report_file.exists():
        data = json.loads(report_file.read_text(encoding="utf-8"))
        data["skills"].append(report)
    else:
        data = {"date": today, "skills": [report]}
    
    report_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def show_health_summary(days: int = 30):
    """显示健康度摘要"""
    skills = get_all_skills()
    
    if not skills:
        console.print("[yellow]未找到技能[/yellow]")
        return
    
    console.print(f"\n[bold]技能健康度总览（基于过去 {days} 天数据）[/bold]\n")
    
    table = Table(title="技能健康度评分")
    table.add_column("技能", style="cyan")
    table.add_column("总分", justify="right")
    table.add_column("等级")
    table.add_column("使用频率", justify="right")
    table.add_column("成功率", justify="right")
    table.add_column("性能", justify="right")
    
    all_scores = []
    
    for skill in skills[:20]:  # 只显示前 20 个
        score_data = calculate_health_score(skill, days)
        all_scores.append(score_data)
        
        emoji, level = get_health_level(score_data["total"])
        
        table.add_row(
            skill,
            f"{score_data['total']:.1f}",
            f"{emoji} {level}",
            f"{score_data['scores']['usage']:.1f}",
            f"{score_data['scores']['success']:.1f}",
            f"{score_data['scores']['performance']:.1f}",
        )
        
        # 保存报告
        save_health_report(score_data)
    
    console.print(table)
    
    # 统计
    healthy = len([s for s in all_scores if s["total"] >= 8])
    warning = len([s for s in all_scores if 4 <= s["total"] < 6])
    danger = len([s for s in all_scores if s["total"] < 4])
    
    console.print(f"\n[bold]统计：[/bold]")
    console.print(f"健康：{healthy} 个 🟢")
    console.print(f"警告：{warning} 个 🟠")
    console.print(f"危险：{danger} 个 🔴")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="滚滚技能健康度评分系统")
    parser.add_argument("--score", help="计算指定技能的健康度")
    parser.add_argument("--summary", action="store_true", help="显示健康度摘要")
    parser.add_argument("--days", type=int, default=30, help="统计天数（默认 30 天）")
    
    args = parser.parse_args()
    
    if args.score:
        score_data = calculate_health_score(args.score, args.days)
        emoji, level = get_health_level(score_data["total"])
        
        console.print(f"\n[bold]{args.score}[/bold] 健康度：{emoji} {score_data['total']:.1f} 分 ({level})\n")
        console.print(f"使用频率：{score_data['scores']['usage']:.1f}/10")
        console.print(f"成功率：{score_data['scores']['success']:.1f}/10")
        console.print(f"满意度：{score_data['scores']['satisfaction']:.1f}/10")
        console.print(f"性能：{score_data['scores']['performance']:.1f}/10")
        console.print(f"维护：{score_data['scores']['maintenance']:.1f}/10\n")
    elif args.summary:
        show_health_summary(args.days)
    else:
        parser.print_help()
