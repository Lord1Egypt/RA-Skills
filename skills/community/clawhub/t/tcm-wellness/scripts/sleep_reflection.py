#!/usr/bin/env python3
"""
TCM Wellness Skill - 睡眠反思脚本
汇总用户记忆块、分析健康趋势、生成反思报告、更新长记忆索引。

用法：
    python sleep_reflection.py --user <匿名ID> [--archive-only] [--dry-run]

参数：
    --user         指定用户匿名ID（必填）
    --archive-only 仅执行归档，不生成反思报告
    --dry-run      仅分析不写入，用于预览
"""

import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path


def get_memory_root():
    return Path(__file__).parent.parent / "memory"


def load_config(root: Path) -> dict:
    config_path = root / "config.json"
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def load_reflection_meta(root: Path) -> dict:
    meta_path = root / "reflections" / "meta.md"
    if meta_path.exists():
        with open(meta_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "last_reflection": None,
        "total_reflections": 0,
        "auto_trigger_threshold": 10,
        "reflection_interval_days": 30,
        "users_reflected": [],
    }


def get_all_blocks(root: Path, user_id: str) -> list:
    """获取用户所有记忆块文件"""
    blocks_dir = root / "blocks" / user_id
    if not blocks_dir.exists():
        return []
    return sorted(blocks_dir.glob("*.md"))


def parse_block_frontmatter(block_path: Path) -> dict:
    """解析记忆块的 YAML frontmatter"""
    content = block_path.read_text(encoding="utf-8")
    frontmatter = {}

    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            fm_text = content[3:end].strip()
            for line in fm_text.split("\n"):
                if ":" in line:
                    key, _, value = line.partition(":")
                    frontmatter[key.strip()] = value.strip()

    return frontmatter


def extract_section(content: str, section_title: str) -> str:
    """提取 markdown 文件中某个二级标题下的内容"""
    pattern = rf"^## {re.escape(section_title)}\s*\n(.*?)(?=\n## |\n---|\Z)"
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""


def analyze_blocks(blocks: list) -> dict:
    """分析所有记忆块，提取统计信息"""
    analysis = {
        "total": len(blocks),
        "by_priority": Counter(),
        "by_syndrome": Counter(),
        "by_date": [],
        "chief_complaints": Counter(),
        "tags": Counter(),
        "resolved": {"true": 0, "false": 0, "unknown": 0},
        "feedback_status": {"waiting": 0, "confirmed": 0, "none": 0},
    }

    for block in blocks:
        fm = parse_block_frontmatter(block)
        analysis["by_priority"][fm.get("priority", "medium")] += 1
        analysis["by_syndrome"][fm.get("syndrome_code", "unknown")] += 1

        chief = fm.get("chief_complaint", "")
        if chief:
            for item in chief.split("、"):
                item = item.strip()
                if item:
                    analysis["chief_complaints"][item] += 1

        tags_str = fm.get("tags", "[]")
        try:
            tags = json.loads(tags_str) if tags_str.startswith("[") else [t.strip() for t in tags_str.split(",")]
        except:
            tags = []
        for tag in tags:
            analysis["tags"][tag] += 1

        resolved = fm.get("resolved", "unknown")
        analysis["resolved"][resolved] += 1

        follow_up = fm.get("follow_up_needed", "false")
        if follow_up == "true" and resolved == "unknown":
            analysis["feedback_status"]["waiting"] += 1
        elif resolved == "true":
            analysis["feedback_status"]["confirmed"] += 1
        else:
            analysis["feedback_status"]["none"] += 1

        ts = fm.get("timestamp", "")
        if ts:
            analysis["by_date"].append(ts[:10])

    return analysis


def extract_symptom_trends(blocks: list) -> list:
    """提取症状趋势数据"""
    trends = defaultdict(list)

    for block in blocks:
        fm = parse_block_frontmatter(block)
        chief = fm.get("chief_complaint", "")
        date = fm.get("timestamp", "")[:10]
        resolved = fm.get("resolved", "unknown")

        if chief and date:
            for item in chief.split("、"):
                item = item.strip()
                if item:
                    trends[item].append({
                        "date": date,
                        "resolved": resolved,
                    })

    return dict(trends)


def generate_reflection_report(root: Path, user_id: str, analysis: dict,
                                symptom_trends: dict, dry_run: bool = False) -> str:
    """生成睡眠反思报告"""
    now = datetime.now()
    reflection_num = load_reflection_meta(root)["total_reflections"] + 1

    # 日期范围
    dates = analysis["by_date"]
    period_start = dates[0] if dates else now.strftime("%Y-%m-%d")
    period_end = now.strftime("%Y-%m-%d")

    # 症状趋势表格
    trend_rows = []
    for symptom, records in sorted(symptom_trends.items(), key=lambda x: x[1][0]["date"]):
        first = records[0]["date"]
        last = records[-1]["date"]
        count = len(records)
        resolved_count = sum(1 for r in records if r["resolved"] == "true")

        # 趋势判断
        if resolved_count > count // 2:
            trend = "↓ 改善"
            assessment = "方案有效"
        elif count >= 3 and all(r["resolved"] == "unknown" for r in records):
            trend = "→ 持续"
            assessment = "需加强关注"
        else:
            trend = "~ 波动"
            assessment = "持续观察"

        trend_rows.append(f"| {symptom} | {count} | {first} | {last} | {trend} | {assessment} |")

    # 证型分布
    syndrome_rows = []
    for syndrome, count in analysis["by_syndrome"].most_common(5):
        syndrome_rows.append(f"| {syndrome} | {count} |")

    # 待反馈列表
    waiting_items = []
    for block in get_all_blocks(root, user_id):
        fm = parse_block_frontmatter(block)
        if fm.get("follow_up_needed") == "true" and fm.get("resolved") == "unknown":
            date = fm.get("timestamp", "")[:10]
            chief = fm.get("chief_complaint", "")
            waiting_items.append(f"| {date} | {chief} | ⏳ 等待中 |")

    # 组装报告
    report = f"""---
type: sleep_reflection
user: {user_id}
period_start: {period_start}
period_end: {period_end}
total_blocks: {analysis["total"]}
reflection_number: {reflection_num}
generated_at: {now.isoformat()}
---

# 睡眠反思报告 #{reflection_num}

## 一、健康趋势总览

本周期共记录 {analysis["total"]} 次辨证交互。
- 已确认有效：{analysis["feedback_status"]["confirmed"]} 次
- 等待反馈：{analysis["feedback_status"]["waiting"]} 次

### 症状频次 Top 10
"""

    for symptom, count in analysis["chief_complaints"].most_common(10):
        report += f"- **{symptom}**：出现 {count} 次\n"

    report += "\n### 证型分布\n\n| 证型代码 | 出现次数 |\n|---------|---------|\n"
    report += "\n".join(syndrome_rows) + "\n"

    report += "\n## 二、症状追踪分析\n\n"
    report += "| 症状 | 出现次数 | 首次 | 最近 | 趋势 | 评估 |\n"
    report += "|------|---------|------|------|------|------|\n"
    report += "\n".join(trend_rows) + "\n"

    report += "\n## 三、体质演变\n\n"
    report += "> 请根据 blocks 内容和 profile.md 中的体质记录，补充体质演变分析。\n"
    report += "> 体质演变是睡眠反思的核心输出——它决定了下一阶段的调理方向。\n\n"

    report += "## 四、方案有效性复盘\n\n"
    report += "### ✅ 有效方案\n> 请从 blocks 中提取用户反馈有效的调理方案\n\n"
    report += "### ❌ 效果不佳方案\n> 请从 blocks 中提取反馈无效或效果有限的方案\n\n"
    report += "### 🔄 需要调整\n> 请标注需要根据季节/体质变化调整的方案\n\n"

    report += "## 五、季节与健康关联\n\n"
    report += "> 分析症状是否与季节变化相关，标注季节性规律。\n\n"

    report += "## 六、新信号预警\n\n"
    report += "> 标注本周期新出现的症状或体质变化信号。\n\n"

    report += "## 七、下一阶段建议\n\n"
    report += "> 基于以上分析，给出下一阶段的调理重点建议。\n\n"

    report += "---\n*本报告由中医养生顾问睡眠反思机制自动生成，仅供参考。*\n"

    return report


def archive_old_blocks(root: Path, user_id: str, config: dict, dry_run: bool = False):
    """归档过期的记忆块"""
    blocks_dir = root / "blocks" / user_id
    if not blocks_dir.exists():
        print("  ℹ️  无记忆块可归档")
        return

    retention = config.get("retention", {})
    now = datetime.now()
    archived_count = 0

    for block in sorted(blocks_dir.glob("*.md")):
        fm = parse_block_frontmatter(block)
        priority = fm.get("priority", "medium")
        ts = fm.get("timestamp", "")

        if not ts:
            continue

        try:
            block_date = datetime.fromisoformat(ts)
        except:
            continue

        days_map = {
            "high": retention.get("high_blocks_days", 180),
            "medium": retention.get("medium_blocks_days", 90),
            "low": retention.get("low_blocks_days", 30),
        }
        retention_days = days_map.get(priority, 90)

        if retention_days > 0:
            threshold = now - timedelta(days=retention_days)
            if block_date < threshold:
                if not dry_run:
                    # 标记归档（在 frontmatter 中添加 archived 标记）
                    content = block.read_text(encoding="utf-8")
                    if "archived: true" not in content:
                        content = content.replace("---\n", "---\narchived: true\n", 1)
                        block.write_text(content, encoding="utf-8")
                archived_count += 1
                print(f"  📦 归档: {block.name} (优先级: {priority}, 创建于 {ts[:10]})")

    print(f"\n  📊 归档完成: {archived_count} 个记忆块{'（dry-run 模式，未实际写入）' if dry_run else ''}")


def count_blocks_since_last_reflection(root: Path, user_id: str, meta: dict) -> int:
    """计算自上次反思以来的新记忆块数"""
    blocks_dir = root / "blocks" / user_id
    if not blocks_dir.exists():
        return 0

    last = meta.get("last_reflection")
    count = 0

    for block in blocks_dir.glob("*.md"):
        if last:
            fm = parse_block_frontmatter(block)
            ts = fm.get("timestamp", "")
            if ts and ts[:10] > last:
                count += 1
        else:
            count += 1

    return count


def main():
    args = sys.argv[1:]
    user_id = None
    archive_only = False
    dry_run = False

    i = 0
    while i < len(args):
        if args[i] == "--user" and i + 1 < len(args):
            user_id = args[i + 1]
            i += 2
        elif args[i] == "--archive-only":
            archive_only = True
            i += 1
        elif args[i] == "--dry-run":
            dry_run = True
            i += 1
        else:
            i += 1

    if not user_id:
        print("❌ 请指定用户ID: python sleep_reflection.py --user <匿名ID>")
        sys.exit(1)

    root = get_memory_root()
    config = load_config(root)
    meta = load_reflection_meta(root)

    print(f"🌙 TCM 睡眠反思系统")
    print(f"   用户: {user_id}")
    print(f"   模式: {'归档 only' if archive_only else '完整反思'}{' (dry-run)' if dry_run else ''}")
    print()

    # 获取记忆块
    blocks = get_all_blocks(root, user_id)
    print(f"   📋 找到 {len(blocks)} 个记忆块")

    # 归档
    print("\n📂 执行归档检查...")
    archive_old_blocks(root, user_id, config, dry_run)

    if archive_only:
        print("\n  ✅ 归档模式完成")
        return

    # 检查是否满足反思条件
    new_count = count_blocks_since_last_reflection(root, user_id, meta)
    threshold = config.get("reflection", {}).get("auto_trigger_blocks", 10)
    interval = config.get("reflection", {}).get("reflection_interval_days", 30)

    should_reflect = False
    reason = ""

    if new_count >= threshold:
        should_reflect = True
        reason = f"新增 {new_count} 个记忆块（阈值: {threshold}）"
    elif meta.get("last_reflection") is None:
        should_reflect = True
        reason = "首次反思"
    else:
        last_dt = datetime.fromisoformat(meta["last_reflection"])
        days_since = (datetime.now() - last_dt).days
        if days_since >= interval:
            should_reflect = True
            reason = f"距上次反思已 {days_since} 天（阈值: {interval} 天）"

    if not should_reflect:
        print(f"\n  ⏭️  尚未满足反思条件: 新增 {new_count}/{threshold} 块")
        return

    print(f"\n  🔔 触发反思: {reason}")

    # 分析
    print("  📊 分析记忆块...")
    analysis = analyze_blocks(blocks)
    symptom_trends = extract_symptom_trends(blocks)

    # 生成报告
    print("  📝 生成反思报告...")
    report = generate_reflection_report(root, user_id, analysis, symptom_trends, dry_run)

    if dry_run:
        print("\n  --- DRY RUN 报告预览 ---")
        print(report[:2000])
        if len(report) > 2000:
            print(f"  ... (共 {len(report)} 字符，省略剩余部分)")
        print("\n  --- 预览结束 ---")
    else:
        # 写入报告
        report_filename = f"{datetime.now().strftime('%Y-%m-%d')}_reflection.md"
        report_path = root / "reflections" / report_filename
        report_path.write_text(report, encoding="utf-8")
        print(f"  ✅ 反思报告: reflections/{report_filename}")

        # 更新元数据
        meta["last_reflection"] = datetime.now().strftime("%Y-%m-%d")
        meta["total_reflections"] += 1
        if user_id not in meta.get("users_reflected", []):
            meta.setdefault("users_reflected", []).append(user_id)

        meta_path = root / "reflections" / "meta.md"
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)

    print("\n  ✅ 睡眠反思完成")
    print(f"  📊 统计: {analysis['total']} 块 | 症状类型 {len(analysis['chief_complaints'])} | 证型类型 {len(analysis['by_syndrome'])}")


if __name__ == "__main__":
    main()
