#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["rich"]
# ///
"""
滚滚技能使用数据收集工具

自动记录技能调用情况，用于健康度评分和优化分析。
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from rich.console import Console

console = Console()

# 数据存储目录
DATA_DIR = Path.home() / ".openclaw" / "data" / "gungun"
USAGE_DIR = DATA_DIR / "skill-usage"

def ensure_dirs():
    """确保数据目录存在"""
    USAGE_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "health-scores").mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "proposals" / "pending").mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "proposals" / "applied").mkdir(parents=True, exist_ok=True)

def log_skill_usage(
    skill_name: str,
    success: bool,
    duration_ms: int,
    user_satisfaction: int = None,
    metadata: dict = None
):
    """
    记录技能使用情况
    
    Args:
        skill_name: 技能名称
        success: 是否成功
        duration_ms: 耗时（毫秒）
        user_satisfaction: 用户满意度（1-5，可选）
        metadata: 其他元数据
    """
    ensure_dirs()
    
    # 生成记录
    record = {
        "skill": skill_name,
        "timestamp": datetime.now().isoformat(),
        "success": success,
        "duration_ms": duration_ms,
        "user_satisfaction": user_satisfaction,
        "metadata": metadata or {}
    }
    
    # 写入 JSONL 文件（按月分文件）
    month_file = USAGE_DIR / f"{datetime.now().strftime('%Y-%m')}.jsonl"
    
    with open(month_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    
    console.print(f"[dim]✓ 已记录技能使用：{skill_name} ({'成功' if success else '失败'}, {duration_ms}ms)[/dim]")

def get_usage_data(skill_name: str = None, days: int = 30):
    """
    获取使用数据
    
    Args:
        skill_name: 技能名称（可选，不传则获取所有）
        days: 获取最近 N 天的数据
    
    Returns:
        list: 使用记录列表
    """
    records = []
    
    # 读取最近 N 个月的 JSONL 文件
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

def show_usage_summary(skill_name: str = None, days: int = 7):
    """显示使用摘要"""
    records = get_usage_data(skill_name, days)
    
    if not records:
        console.print(f"[yellow]过去 {days} 天没有使用记录[/yellow]")
        return
    
    # 统计
    total = len(records)
    success = len([r for r in records if r["success"]])
    failed = total - success
    avg_duration = sum(r["duration_ms"] for r in records) / total if total > 0 else 0
    
    console.print(f"\n[bold]技能使用摘要（过去 {days} 天）[/bold]\n")
    console.print(f"总调用次数：{total}")
    console.print(f"成功：{success} ({success/total*100:.1f}%)")
    console.print(f"失败：{failed} ({failed/total*100:.1f}%)")
    console.print(f"平均耗时：{avg_duration:.0f}ms")
    
    if skill_name is None:
        # 按技能分组
        by_skill = {}
        for r in records:
            skill = r["skill"]
            if skill not in by_skill:
                by_skill[skill] = {"total": 0, "success": 0}
            by_skill[skill]["total"] += 1
            if r["success"]:
                by_skill[skill]["success"] += 1
        
        console.print(f"\n[bold]按技能统计：[/bold]\n")
        for skill, stats in sorted(by_skill.items(), key=lambda x: x[1]["total"], reverse=True)[:10]:
            rate = stats["success"] / stats["total"] * 100
            console.print(f"{skill:20} {stats['total']:3} 次 (成功率 {rate:.0f}%)")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="滚滚技能使用数据收集工具")
    parser.add_argument("--log", action="store_true", help="记录测试数据")
    parser.add_argument("--summary", action="store_true", help="显示使用摘要")
    parser.add_argument("--skill", help="指定技能名称")
    parser.add_argument("--days", type=int, default=7, help="统计天数（默认 7 天）")
    
    args = parser.parse_args()
    
    if args.log:
        # 测试记录
        log_skill_usage("test-skill", True, 1234, 5, {"test": True})
        console.print("[green]✓ 测试记录完成[/green]")
    elif args.summary:
        show_usage_summary(args.skill, args.days)
    else:
        parser.print_help()
