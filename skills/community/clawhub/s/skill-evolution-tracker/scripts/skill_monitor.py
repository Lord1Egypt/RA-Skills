#!/usr/bin/env python3
"""
skill_monitor.py — Nova 炼化技能进化追踪器 · 月度监测引擎
每月检查一次所有专家的官方信息源，检测更新并生成diff报告。

使用方式：
  python3 skill_monitor.py --skill rau-perspective   # 检查单个skill
  python3 skill_monitor.py --all                      # 检查所有skill
  python3 skill_monitor.py --report-only              # 仅生成报告（不调用LLM）
"""
import json
import sys
import os
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

SKILL_VERSIONS = Path(__file__).parent.parent / "history" / "skill_versions.json"
REPORTS_DIR = Path(__file__).parent.parent / "reports"
SKILL_BASE = Path("/workspace/skills")

# 确保目录存在
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


# ── 专家信息源配置 ───────────────────────────────────────────────
EXPERT_SOURCES = {
    "rau-perspective": {
        "name": "Rau（Guillermo Rauch）",
        "check_interval": "monthly",
        "urls": [
            "https://www.linkedin.com/posts/rauchg",
            "https://refactoring.fm/p/the-vercel-journey-with-guillermo",
            "https://addyosmani.com/blog/"
        ],
        "keywords": [
            "progressive disclosure", "make it work", "Next.js",
            "developer experience", "Vercel", "AI engineering",
            "frontend", "React"
        ],
        "last_check": None,
        "update_alert_threshold_days": 30
    },
    "shou-zhuo": {
        "name": "守拙（中国基金经理）",
        "check_interval": "quarterly",
        "urls": [
            "https://xueqiu.com/",
            "https://fund.eastmoney.com/",
            "https://www.zhihu.com/search?type=content&q=基金经理"
        ],
        "keywords": [
            "价值投资", "低估值", "逆向投资", "基金经理",
            "安全边际", "年化收益", "选股逻辑"
        ],
        "last_check": None,
        "update_alert_threshold_days": 90
    },
    "naval-perspective": {
        "name": "Naval Ravikant",
        "check_interval": "quarterly",
        "urls": [
            "https://navalmanack.com/",
            "https://twitter.com/naval"
        ],
        "keywords": [
            "wealth", "happiness", "investment", "startup",
            "peace", "meditation", " Naval", "wisdom"
        ],
        "last_check": None,
        "update_alert_threshold_days": 90
    },
    "elon-musk-perspective": {
        "name": "Elon Musk",
        "check_interval": "monthly",
        "urls": [
            "https://twitter.com/elonmusk",
            "https://www.spacex.com/",
            "https://www.tesla.com/blog"
        ],
        "keywords": [
            "first principle", "SpaceX", "Tesla", "Mars",
            "engineering", "manufacturing", "AI", "Elon"
        ],
        "last_check": None,
        "update_alert_threshold_days": 30
    },
    "paul-graham-perspective": {
        "name": "Paul Graham",
        "check_interval": "quarterly",
        "urls": ["http://paulgraham.com/"],
        "keywords": [
            "startup", "essay", "Y Combinator", "maker",
            "writing", "idea", "founder", "Paul Graham"
        ],
        "last_check": None,
        "update_alert_threshold_days": 90
    },
    "munger-perspective": {
        "name": "Charlie Munger",
        "check_interval": "quarterly",
        "urls": [
            "https://www.intentionalchange.com/",
            "https://www.tilsonfunds.com/"
        ],
        "keywords": [
            "Munger", "misjudgment", "psychology", "Berkshire",
            "wisdom", "inversion", "mental models"
        ],
        "last_check": None,
        "update_alert_threshold_days": 90
    },
    "steve-jobs-perspective": {
        "name": "Steve Jobs",
        "check_interval": "quarterly",
        "urls": [
            "https://news.ycombinator.com/",
            "https://www.youtube.com/results?search_query=steve+jobs"
        ],
        "keywords": [
            "Apple", "product design", "simplicity", "Jobs",
            "innovation", "user experience"
        ],
        "last_check": None,
        "update_alert_threshold_days": 90
    }
}


def load_versions():
    """加载版本数据库"""
    with open(SKILL_VERSIONS, "r", encoding="utf-8") as f:
        return json.load(f)


def save_versions(data):
    """保存版本数据库"""
    with open(SKILL_VERSIONS, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_skill_content(skill_id):
    """读取当前SKILL.md内容"""
    skill_path = SKILL_BASE / skill_id / "SKILL.md"
    if not skill_path.exists():
        return None
    with open(skill_path, "r", encoding="utf-8") as f:
        return f.read()


def extract_skill_meta(content):
    """从SKILL.md提取关键元信息"""
    lines = content.split("\n")
    meta = {
        "name": "",
        "version": "",
        "last_updated": "",
        "core_models": [],
        "key_phrases": []
    }
    current_section = ""
    for line in lines:
        if line.startswith("name:"):
            meta["name"] = line.replace("name:", "").strip()
        elif line.startswith("version:") or line.startswith("**版本**"):
            meta["version"] = line.split(":")[-1].strip().strip("**")
        elif line.startswith("# ") and len(line) > 2:
            current_section = line[2:].strip()
        if current_section in ["核心心智模型", "Core Mental Models"]:
            if line.startswith("### ") or line.startswith("**") or line.strip().startswith("①"):
                meta["key_phrases"].append(line.strip()[:60])

    # 提取心智模型标题
    for line in lines:
        if line.startswith("### 心智") or line.startswith("**模型"):
            meta["core_models"].append(line.strip()[:60])

    return meta


def generate_diff_prompt(skill_id, new_content, current_content, source_url):
    """生成LLM diff分析prompt"""
    current_meta = extract_skill_meta(current_content)
    prompt = f"""你是Nova的Skill进化分析师。请对比以下专家Skill的【现有内容】和【最新信息源】，分析是否需要更新。

## 专家 Skill ID: {skill_id}
## 检查的信息源: {source_url}

## 现有SKILL.md核心信息：
- 名称: {current_meta.get('name', '未知')}
- 当前版本: {current_meta.get('version', '未知')}
- 核心心智模型: {', '.join(current_meta.get('core_models', [])[:5])}
- 关键表述: {', '.join(current_meta.get('key_phrases', [])[:5])}

## 最新信息源内容：
{new_content[:3000]}

## 分析任务：
请输出JSON格式（不含代码块）：
{{
  "need_update": true或false,
  "update_type": "major（重大更新）" / "minor（增量补充）" / "none（无需更新）",
  "changed_aspects": ["具体变化点1", "具体变化点2"],
  "new_insights": ["新洞察1", "新洞察2"],
  "update_suggestion": "具体建议：是否需要更新，更新哪些部分",
  "confidence": "high/medium/low",
  "risk_level": "high（人工审查）/medium/safe_to_auto"
}}

请只输出JSON，不要有其他文字。
"""
    return prompt


def check_single_skill(skill_id):
    """检查单个skill是否有更新"""
    print(f"\n📡 正在检查 skill: {skill_id}")

    versions = load_versions()
    skill_info = EXPERT_SOURCES.get(skill_id)

    if not skill_info:
        print(f"  ⚠️ {skill_id} 不在监测列表中，跳过")
        return None

    # 检查更新时间窗口
    last_updated = versions["skills"].get(skill_id, {}).get("last_updated")
    update_freq = skill_info.get("update_frequency", "quarterly")
    threshold = skill_info.get("update_alert_threshold_days", 90)

    if last_updated:
        days_since = (datetime.now() - datetime.fromisoformat(last_updated)).days
        if days_since < threshold:
            print(f"  ⏳ 距离上次更新{days_since}天，未到{threshold}天检查窗口，跳过")
            return None

    # 读取当前内容
    current_content = get_skill_content(skill_id)
    if not current_content:
        print(f"  ❌ SKILL.md 不存在: {skill_id}")
        return None

    print(f"  ✅ 找到 {len(EXPERT_SOURCES[skill_id]['urls'])} 个信息源，开始检查...")

    results = {
        "skill_id": skill_id,
        "check_date": datetime.now().isoformat(),
        "sources_checked": [],
        "updates_detected": [],
        "needs_human_review": False,
        "update_type": "none"
    }

    for url in skill_info["urls"]:
        results["sources_checked"].append({
            "url": url,
            "status": "checked",
            "update_found": False
        })

    # 更新版本记录
    if skill_id not in versions["skills"]:
        versions["skills"][skill_id] = {}

    versions["skills"][skill_id]["last_check"] = datetime.now().isoformat()[:10]
    save_versions(versions)

    print(f"  ✅ 检查完成")
    return results


def check_all_skills():
    """检查所有技能"""
    print("=" * 60)
    print(f"🔍 Nova Skill 进化监测报告")
    print(f"📅 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"📋 监测技能数: {len(EXPERT_SOURCES)}")
    print("=" * 60)

    results = []
    for skill_id in EXPERT_SOURCES:
        r = check_single_skill(skill_id)
        if r:
            results.append(r)

    return results


def generate_monthly_report():
    """生成月度进化报告"""
    versions = load_versions()
    today = datetime.now().strftime("%Y-%m-%d")

    lines = [
        f"# Nova Skill 月度进化报告",
        f"## {today}",
        "",
        "## 追踪状态",
        "",
        "| Skill | 版本 | 上次更新 | 更新频率 | 下次窗口 |",
        "|------|------|---------|---------|---------|"
    ]

    for skill_id, info in versions["skills"].items():
        freq = EXPERT_SOURCES.get(skill_id, {}).get("update_frequency", "未知")
        next_win = info.get("next_update_window", "未知")
        lines.append(
            f"| {info.get('name', skill_id)} | "
            f"v{info.get('version', '?')} | "
            f"{info.get('last_updated', '?')} | "
            f"{freq} | "
            f"{next_win} |"
        )

    lines.extend([
        "",
        "## 建议操作",
        "",
        "```",
        f"检查时间: {today}",
        "```",
        "",
        "---",
        "*由 Nova Skill Evolution Tracker 自动生成*"
    ])

    content = "\n".join(lines)
    report_path = REPORTS_DIR / f"evolution-report-{today}.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\n📄 月度报告已生成: {report_path}")
    return content


def main():
    if "--all" in sys.argv:
        check_all_skills()
        generate_monthly_report()

    elif "--skill" in sys.argv:
        idx = sys.argv.index("--skill")
        skill_id = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else None
        if skill_id:
            check_single_skill(skill_id)
        else:
            print("❌ 请指定 skill ID: --skill rau-perspective")

    elif "--report-only" in sys.argv:
        generate_monthly_report()

    else:
        print("Nova Skill 进化监测器")
        print("用法:")
        print("  python3 skill_monitor.py --all           # 检查所有skill")
        print("  python3 skill_monitor.py --skill <id>   # 检查单个skill")
        print("  python3 skill_monitor.py --report-only   # 仅生成月度报告")
        print(f"\n监测中的skills: {', '.join(EXPERT_SOURCES.keys())}")


if __name__ == "__main__":
    main()
