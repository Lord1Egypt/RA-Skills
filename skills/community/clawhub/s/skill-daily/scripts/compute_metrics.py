#!/usr/bin/env python3
"""
指标计算脚本
为每个 Skill 计算：star_rate、activity_rate、age_days、综合得分
"""
import json
import argparse
import time
import sys
from pathlib import Path
from datetime import datetime


def safe_get(d, *keys, default=None):
    """安全获取嵌套字段"""
    for k in keys:
        if isinstance(d, dict):
            d = d.get(k)
        else:
            return default
        if d is None:
            return default
    return d if d is not None else default


def to_int(v, default=0):
    """安全转 int"""
    if v is None:
        return default
    try:
        return int(float(v))
    except (ValueError, TypeError):
        return default


def compute_metrics(skill_record):
    """计算单个 Skill 的所有指标"""
    skill = safe_get(skill_record, 'skill', default={})
    owner = safe_get(skill_record, 'owner', default={})
    version = safe_get(skill_record, 'latestVersion', default={})

    stats = safe_get(skill, 'stats', default={})
    stars = to_int(stats.get('stars'))
    downloads = to_int(stats.get('downloads'))
    installs_current = to_int(stats.get('installsCurrent'))
    installs_all_time = to_int(stats.get('installsAllTime'))
    comments = to_int(stats.get('comments'))

    created_at_ms = to_int(skill.get('createdAt'))
    now_ms = int(time.time() * 1000)
    age_days = max(0, (now_ms - created_at_ms) / (1000 * 60 * 60 * 24)) if created_at_ms else 0

    # 关键指标
    star_rate = (stars / downloads * 100) if downloads > 0 else 0
    activity_rate = (installs_current / installs_all_time * 100) if installs_all_time > 0 else 0
    version_count = to_int(stats.get('versions'))

    return {
        "skill_id": skill.get('_id'),
        "display_name": skill.get('displayName', ''),
        "slug": skill.get('slug', ''),
        "summary": skill.get('summary', ''),
        "author_handle": owner.get('handle', ''),
        "author_display": owner.get('displayName', ''),
        "author_image": owner.get('image', ''),
        "url": f"https://clawhub.ai/{owner.get('handle', '')}/{skill.get('slug', '')}",
        "version": version.get('version', ''),
        "version_count": version_count,
        "stars": stars,
        "downloads": downloads,
        "installs_current": installs_current,
        "installs_all_time": installs_all_time,
        "comments": comments,
        "star_rate": round(star_rate, 3),  # 百分比
        "activity_rate": round(activity_rate, 3),  # 百分比
        "age_days": round(age_days, 1),
        "created_at": created_at_ms,
        "capability_tags": skill.get('capabilityTags', []),
        "is_suspicious": skill.get('isSuspicious', False),
    }


def process_snapshot(input_path, output_path=None):
    """处理一个快照文件，计算所有指标"""
    with open(input_path, "r", encoding="utf-8") as f:
        snapshot = json.load(f)

    skills = snapshot.get('skills', [])
    print(f"[Metrics] 处理 {len(skills)} 个 Skill")

    enriched = []
    for i, s in enumerate(skills):
        m = compute_metrics(s)
        enriched.append(m)

    # 按 downloads 降序
    enriched.sort(key=lambda x: x['downloads'], reverse=True)

    output = {
        "snapshot_date": snapshot.get('snapshot_date'),
        "fetched_at": snapshot.get('fetched_at'),
        "total_count": len(enriched),
        "skills": enriched
    }

    if output_path is None:
        output_path = str(input_path).replace('.json', '.metrics.json')
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"[Metrics] 已保存到: {output_path}")
    return output


def main():
    parser = argparse.ArgumentParser(description="计算 Skill 指标")
    parser.add_argument("--input", required=True, help="输入快照 JSON")
    parser.add_argument("--output", default=None, help="输出 metrics JSON")
    args = parser.parse_args()

    if not Path(args.input).exists():
        print(f"[Error] 输入文件不存在: {args.input}")
        return 1
    process_snapshot(args.input, args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
