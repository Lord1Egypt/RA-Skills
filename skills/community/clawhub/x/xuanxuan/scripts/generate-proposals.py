#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["rich"]
# ///
"""
滚滚技能优化建议生成器

分析技能健康度数据，自动生成优化建议。
"""

import json
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()

# 数据目录
DATA_DIR = Path.home() / ".openclaw" / "data" / "gungun"
HEALTH_DIR = DATA_DIR / "health-scores"
PROPOSALS_DIR = DATA_DIR / "proposals"

def load_health_data(days: int = 30):
    """加载健康度数据"""
    from datetime import timedelta
    cutoff = datetime.now() - timedelta(days=days)
    
    all_scores = []
    
    for file in HEALTH_DIR.glob("*.json"):
        try:
            data = json.loads(file.read_text(encoding="utf-8"))
            for skill_data in data.get("skills", []):
                score_time = datetime.fromisoformat(skill_data["timestamp"])
                if score_time >= cutoff:
                    all_scores.append(skill_data)
        except:
            continue
    
    return all_scores

def generate_proposals(skill_data: dict):
    """为单个技能生成优化建议"""
    proposals = []
    
    skill_name = skill_data["skill"]
    scores = skill_data["scores"]
    stats = skill_data.get("stats", {})
    total = skill_data["total"]
    
    # 检查各项指标
    
    # 1. 使用频率低
    if scores["usage"] < 4:
        usage_count = stats.get("usage_count_7d", 0)
        proposals.append({
            "type": "low_usage",
            "severity": "warning" if usage_count > 0 else "critical",
            "title": "低使用率",
            "description": f"过去 7 天仅使用 {usage_count} 次",
            "suggestion": "考虑是否需要保留此技能，或改进功能提高使用率",
            "action": "review_or_archive"
        })
    
    # 2. 成功率低
    if scores["success"] < 6:
        success_rate = stats.get("success_rate", 0)
        proposals.append({
            "type": "low_success",
            "severity": "critical",
            "title": "高失败率",
            "description": f"成功率仅 {success_rate:.1f}%",
            "suggestion": "检查代码逻辑、依赖库、配置文件",
            "action": "fix_code"
        })
    
    # 3. 性能差
    if scores["performance"] < 5:
        avg_duration = stats.get("avg_duration_ms", 0)
        proposals.append({
            "type": "poor_performance",
            "severity": "warning",
            "title": "性能较差",
            "description": f"平均响应时间 {avg_duration:.0f}ms",
            "suggestion": "优化算法、添加缓存、减少 IO 操作",
            "action": "optimize_performance"
        })
    
    # 4. 长期未更新
    days_since_update = stats.get("days_since_update", 0)
    if days_since_update > 90:
        proposals.append({
            "type": "outdated",
            "severity": "warning",
            "title": "长期未更新",
            "description": f"已 {days_since_update} 天未更新",
            "suggestion": "检查是否需要更新依赖、修复 bug、添加新功能",
            "action": "update_skill"
        })
    
    # 5. 总体健康度低
    if total < 5:
        proposals.append({
            "type": "overall_low",
            "severity": "critical",
            "title": "整体健康度低",
            "description": f"健康度仅 {total:.1f} 分",
            "suggestion": "综合评估技能价值，考虑重写或移除",
            "action": "comprehensive_review"
        })
    
    return proposals

def save_proposal(skill_name: str, proposals: list):
    """保存优化建议"""
    PROPOSALS_DIR.mkdir(parents=True, exist_ok=True)
    
    proposal = {
        "skill": skill_name,
        "timestamp": datetime.now().isoformat(),
        "proposals": proposals,
        "status": "pending"
    }
    
    proposal_file = PROPOSALS_DIR / "pending" / f"{skill_name}.json"
    proposal_file.write_text(json.dumps(proposal, indent=2, ensure_ascii=False), encoding="utf-8")

def show_proposals(days: int = 30):
    """显示优化建议"""
    all_scores = load_health_data(days)
    
    if not all_scores:
        console.print("[yellow]暂无健康度数据[/yellow]")
        return
    
    console.print(f"\n[bold]优化建议（基于过去 {days} 天数据）[/bold]\n")
    
    total_proposals = 0
    
    for skill_data in sorted(all_scores, key=lambda x: x["total"])[:10]:  # 只显示最差的 10 个
        proposals = generate_proposals(skill_data)
        
        if proposals:
            total_proposals += len(proposals)
            
            emoji_map = {"critical": "🔴", "warning": "🟠", "info": "🟡"}
            
            content = []
            content.append(f"**技能：** {skill_data['skill']}\n")
            content.append(f"**健康度：** {skill_data['total']:.1f} 分\n")
            
            for p in proposals:
                emoji = emoji_map.get(p["severity"], "⚪")
                content.append(f"\n{emoji} **{p['title']}**")
                content.append(f"- {p['description']}")
                content.append(f"- 建议：{p['suggestion']}")
            
            content.append(f"\n---\n*生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}*")
            
            panel = Panel(
                "\n".join(content),
                title=f"优化建议 - {skill_data['skill']}",
                border_style="red" if any(p["severity"] == "critical" for p in proposals) else "yellow"
            )
            console.print(panel)
            
            # 保存建议
            save_proposal(skill_data["skill"], proposals)
    
    if total_proposals == 0:
        console.print("[green]✓ 所有技能都很健康，无需优化！[/green]\n")
    else:
        console.print(f"\n[bold]共发现 {total_proposals} 个优化建议，已保存到 pending 目录[/bold]\n")
        console.print("[dim]查看建议：ls ~/.openclaw/data/gungun/proposals/pending/[/dim]\n")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="滚滚技能优化建议生成器")
    parser.add_argument("--analyze", action="store_true", help="分析并生成建议")
    parser.add_argument("--days", type=int, default=30, help="分析天数（默认 30 天）")
    
    args = parser.parse_args()
    
    if args.analyze:
        show_proposals(args.days)
    else:
        parser.print_help()
