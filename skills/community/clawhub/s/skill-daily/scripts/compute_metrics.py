#!/usr/bin/env python3
"""
指标计算脚本
为每个 Skill 计算：star_rate、activity_rate、age_days、综合得分
v1.1: 适配 ClawHub 新 API 结构（stats.installs 替代 installsCurrent）+ 新增字段
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
    """计算单个 Skill 的所有指标（适配新 API 结构）"""
    skill = safe_get(skill_record, 'skill', default={})
    owner = safe_get(skill_record, 'owner', default={})
    version = safe_get(skill_record, 'latestVersion', default={})

    stats = safe_get(skill, 'stats', default={})

    # 核心统计字段 — 兼容新旧 API
    stars = to_int(stats.get('stars'))
    downloads = to_int(stats.get('downloads'))
    comments = to_int(stats.get('comments'))
    version_count = to_int(stats.get('versions'))

    # installs: 新 API 用 stats.installs，旧 API 用 stats.installsCurrent / installsAllTime
    installs = to_int(stats.get('installs'))  # 新 API
    if installs == 0:
        installs = to_int(stats.get('installsCurrent'))  # 旧 API 兼容

    # 时间相关
    created_at_ms = to_int(skill.get('createdAt'))
    now_ms = int(time.time() * 1000)
    age_days = max(0, (now_ms - created_at_ms) / (1000 * 60 * 60 * 24)) if created_at_ms else 0

    updated_at_ms = to_int(version.get('createdAt')) or created_at_ms
    days_since_update = max(0, (now_ms - updated_at_ms) / (1000 * 60 * 60 * 24)) if updated_at_ms else 999

    # 关键指标
    star_rate = (stars / downloads * 100) if downloads > 0 else 0
    activity_rate = (installs / max(downloads, 1) * 100) if downloads > 0 else 0

    # 新增：更新活跃度（30 天内有更新视为活跃）
    is_actively_maintained = days_since_update <= 30
    update_frequency = version_count / max(age_days, 1) * 30  # 每月版本数

    # 新增：分类（categories 替代 capabilityTags）
    categories = skill.get('categories', []) or skill.get('capabilityTags', []) or []

    # 新增：元数据
    metadata = safe_get(skill_record, 'skill', 'metadata', default={})
    supported_os = metadata.get('os', []) if isinstance(metadata, dict) else []
    setup_requirements = metadata.get('setup', []) if isinstance(metadata, dict) else []

    # 新增：版本信息
    changelog = version.get('changelog', '')
    changelog_summary = changelog[:200] + ('...' if len(changelog) > 200 else '') if changelog else ''

    # 新增：安全标记
    is_suspicious = skill.get('isSuspicious', False)
    badges = skill.get('badges', {})
    is_verified = bool(badges.get('verified', False)) if isinstance(badges, dict) else False

    return {
        # 基础信息
        "skill_id": skill.get('_id'),
        "display_name": skill.get('displayName', ''),
        "slug": skill.get('slug', ''),
        "summary": skill.get('summary', ''),
        "url": f"https://clawhub.ai/{owner.get('handle', '')}/{skill.get('slug', '')}",

        # 作者信息
        "author_handle": owner.get('handle', ''),
        "author_display": owner.get('displayName', ''),
        "author_image": owner.get('image', ''),
        "author_kind": owner.get('kind', ''),

        # 核心统计
        "stars": stars,
        "downloads": downloads,
        "installs_current": installs,
        "comments": comments,
        "version_count": version_count,

        # 计算指标
        "star_rate": round(star_rate, 3),
        "activity_rate": round(activity_rate, 3),
        "age_days": round(age_days, 1),

        # 新增：更新活跃度
        "days_since_update": round(days_since_update, 1),
        "is_actively_maintained": is_actively_maintained,
        "update_frequency": round(update_frequency, 2),

        # 新增：分类
        "categories": categories,

        # 新增：版本信息
        "version": version.get('version', ''),
        "changelog_summary": changelog_summary,
        "license": version.get('license', ''),

        # 新增：元数据
        "supported_os": supported_os,
        "setup_requirements": setup_requirements,

        # 安全标记
        "is_suspicious": is_suspicious,
        "is_verified": is_verified,
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
