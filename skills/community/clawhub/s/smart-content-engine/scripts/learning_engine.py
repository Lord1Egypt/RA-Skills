#!/usr/bin/env python3
"""
content-engine 自学习内容智能模块

基于历史内容表现数据，持续学习并优化内容策略。
支持记录表现、分析趋势、智能推荐话题和发布时间。
"""

import json
import math
import os
import re
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from utils import (
    get_data_file,
    load_input_data,
    now_iso,
    output_error,
    output_success,
    parse_common_args,
    read_json_file,
    write_json_file,
)


# ============================================================
# 数据文件路径
# ============================================================

LEARNING_FILE = "learning.json"


def _get_learning_data() -> Dict[str, Any]:
    """读取学习数据。返回包含 performances, preferences, metadata 的字典。"""
    filepath = get_data_file(LEARNING_FILE)
    data = read_json_file(filepath)
    if isinstance(data, list):
        # 兼容旧格式或空文件
        data = {}
    if not isinstance(data, dict):
        data = {}
    # 确保必要的顶层键存在
    data.setdefault("performances", [])
    data.setdefault("preferences", {
        "preferred_styles": [],
        "preferred_topics": [],
        "preferred_platforms": [],
        "rejected_suggestions": [],
    })
    data.setdefault("metadata", {
        "total_records": 0,
        "first_record_at": "",
        "last_record_at": "",
        "analysis_count": 0,
    })
    return data


def _save_learning_data(data: Dict[str, Any]) -> None:
    """保存学习数据。"""
    write_json_file(get_data_file(LEARNING_FILE), data)


# ============================================================
# 辅助计算函数
# ============================================================

def _calc_engagement_score(metrics: Dict[str, Any]) -> float:
    """计算综合互动得分。

    根据不同指标类型赋予不同权重：
    - 曝光/浏览/阅读：权重 0.1
    - 点赞/鼓掌/收藏：权重 1.0
    - 评论/回复/回应：权重 2.0
    - 转发/分享：权重 3.0

    Args:
        metrics: 指标数据字典。

    Returns:
        综合互动得分（浮点数）。
    """
    weights = {
        "impressions": 0.1,
        "views": 0.1,
        "reads": 0.1,
        "likes": 1.0,
        "claps": 1.0,
        "favorites": 1.0,
        "comments": 2.0,
        "replies": 2.0,
        "responses": 2.0,
        "retweets": 3.0,
        "shares": 3.0,
    }
    score = 0.0
    for key, value in metrics.items():
        if isinstance(value, (int, float)) and key in weights:
            score += value * weights[key]
    return round(score, 2)


def _calc_engagement_rate(metrics: Dict[str, Any]) -> float:
    """计算互动率（互动数 / 曝光数）。

    Args:
        metrics: 指标数据字典。

    Returns:
        互动率（百分比），如 3.5 表示 3.5%。
    """
    exposure_keys = ["impressions", "views", "reads"]
    exposure = 0
    for k in exposure_keys:
        if isinstance(metrics.get(k), (int, float)):
            exposure += metrics[k]

    if exposure == 0:
        return 0.0

    interaction_keys = ["likes", "claps", "favorites", "comments", "replies",
                        "responses", "retweets", "shares"]
    interactions = 0
    for k in interaction_keys:
        if isinstance(metrics.get(k), (int, float)):
            interactions += metrics[k]

    return round((interactions / exposure) * 100, 2)


def _extract_hour(time_str: str) -> Optional[int]:
    """从 ISO 时间字符串提取小时数。

    Args:
        time_str: ISO 格式时间字符串。

    Returns:
        小时数（0-23），解析失败返回 None。
    """
    if not time_str:
        return None
    try:
        if "T" in time_str:
            dt = datetime.fromisoformat(time_str.replace("Z", ""))
            return dt.hour
    except (ValueError, TypeError):
        pass
    return None


def _extract_weekday(time_str: str) -> Optional[int]:
    """从 ISO 时间字符串提取星期几。

    Args:
        time_str: ISO 格式时间字符串。

    Returns:
        星期几（0=周一, 6=周日），解析失败返回 None。
    """
    if not time_str:
        return None
    try:
        if "T" in time_str:
            dt = datetime.fromisoformat(time_str.replace("Z", ""))
        else:
            dt = datetime.strptime(time_str[:10], "%Y-%m-%d")
        return dt.weekday()
    except (ValueError, TypeError):
        pass
    return None


_WEEKDAY_NAMES = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]


def _group_by(records: List[Dict], key: str) -> Dict[str, List[Dict]]:
    """按指定键对记录进行分组。

    Args:
        records: 记录列表。
        key: 分组键名。

    Returns:
        分组后的字典。
    """
    groups: Dict[str, List[Dict]] = defaultdict(list)
    for r in records:
        val = r.get(key, "未知")
        if isinstance(val, list):
            for v in val:
                groups[str(v)].append(r)
        else:
            groups[str(val)].append(r)
    return dict(groups)


def _avg_score(records: List[Dict]) -> float:
    """计算记录列表的平均互动得分。

    Args:
        records: 包含 engagement_score 字段的记录列表。

    Returns:
        平均互动得分。
    """
    if not records:
        return 0.0
    total = sum(r.get("engagement_score", 0) for r in records)
    return round(total / len(records), 2)


def _avg_rate(records: List[Dict]) -> float:
    """计算记录列表的平均互动率。

    Args:
        records: 包含 engagement_rate 字段的记录列表。

    Returns:
        平均互动率。
    """
    if not records:
        return 0.0
    total = sum(r.get("engagement_rate", 0) for r in records)
    return round(total / len(records), 2)


# ============================================================
# 操作：记录内容表现
# ============================================================

def record_performance(data: Dict[str, Any]) -> None:
    """记录一条内容的表现数据。

    必填字段: content_id, platform, metrics
    可选字段: topic, posting_time, format, length, tags, title

    Args:
        data: 内容表现数据字典。
    """
    content_id = data.get("content_id") or data.get("id")
    if not content_id:
        output_error("内容ID（content_id）为必填字段", code="VALIDATION_ERROR")
        return

    platform = data.get("platform", "")
    if not platform:
        output_error("平台（platform）为必填字段", code="VALIDATION_ERROR")
        return

    metrics = data.get("metrics", {})
    if not metrics:
        output_error("指标数据（metrics）为必填字段", code="VALIDATION_ERROR")
        return

    learning = _get_learning_data()

    # 计算互动得分和互动率
    engagement_score = _calc_engagement_score(metrics)
    engagement_rate = _calc_engagement_rate(metrics)

    record = {
        "content_id": content_id,
        "platform": platform,
        "topic": data.get("topic", ""),
        "tags": data.get("tags", []),
        "title": data.get("title", ""),
        "posting_time": data.get("posting_time", ""),
        "format": data.get("format", ""),
        "length": data.get("length", 0),
        "metrics": metrics,
        "engagement_score": engagement_score,
        "engagement_rate": engagement_rate,
        "recorded_at": now_iso(),
    }

    # 替换已有的同内容同平台记录（保留最新）
    performances = learning["performances"]
    performances = [
        p for p in performances
        if not (p.get("content_id") == content_id and p.get("platform") == platform)
    ]
    performances.append(record)
    learning["performances"] = performances

    # 更新元数据
    now = now_iso()
    learning["metadata"]["total_records"] = len(performances)
    learning["metadata"]["last_record_at"] = now
    if not learning["metadata"]["first_record_at"]:
        learning["metadata"]["first_record_at"] = now

    _save_learning_data(learning)

    output_success({
        "message": f"已记录内容 {content_id} 在 {platform} 的表现数据",
        "engagement_score": engagement_score,
        "engagement_rate": engagement_rate,
        "record": record,
    })


# ============================================================
# 操作：记录用户偏好
# ============================================================

def record_preference(data: Dict[str, Any]) -> None:
    """记录用户偏好设置。

    可设置字段:
    - preferred_styles: 偏好的写作风格列表
    - preferred_topics: 偏好的内容话题列表
    - preferred_platforms: 偏好的平台列表
    - rejected_suggestions: 被拒绝的建议列表（避免重复推荐）
    - add_style / add_topic / add_platform / add_rejected: 追加单项

    Args:
        data: 偏好设置数据字典。
    """
    learning = _get_learning_data()
    prefs = learning["preferences"]
    updated_fields = []

    # 批量设置
    for field in ["preferred_styles", "preferred_topics", "preferred_platforms", "rejected_suggestions"]:
        if field in data:
            val = data[field]
            if isinstance(val, str):
                val = [v.strip() for v in val.split(",") if v.strip()]
            prefs[field] = val
            updated_fields.append(field)

    # 追加单项
    add_map = {
        "add_style": "preferred_styles",
        "add_topic": "preferred_topics",
        "add_platform": "preferred_platforms",
        "add_rejected": "rejected_suggestions",
    }
    for add_key, target_field in add_map.items():
        if add_key in data:
            val = data[add_key]
            if isinstance(val, str):
                val = [v.strip() for v in val.split(",") if v.strip()]
            elif not isinstance(val, list):
                val = [str(val)]
            for item in val:
                if item not in prefs[target_field]:
                    prefs[target_field].append(item)
            updated_fields.append(target_field)

    if not updated_fields:
        output_error("未提供任何偏好设置字段", code="VALIDATION_ERROR")
        return

    learning["preferences"] = prefs
    _save_learning_data(learning)

    output_success({
        "message": f"已更新偏好设置: {', '.join(set(updated_fields))}",
        "preferences": prefs,
    })


# ============================================================
# 操作：分析
# ============================================================

def analyze(data: Optional[Dict[str, Any]] = None) -> None:
    """分析历史内容表现，识别最佳实践。

    可选字段: platform（按平台过滤）, limit（结果数量限制）

    生成以下维度的分析：
    - 按话题: 哪些话题表现最好
    - 按平台: 各平台的平均表现
    - 按发布时间: 哪些时段互动最高
    - 按格式: 哪种内容格式效果最好

    Args:
        data: 可选的过滤条件字典。
    """
    learning = _get_learning_data()
    performances = learning["performances"]

    if not performances:
        output_error("暂无历史表现数据，请先使用 record-performance 记录数据", code="NO_DATA")
        return

    # 平台过滤
    platform_filter = data.get("platform") if data else None
    if platform_filter:
        performances = [p for p in performances if p.get("platform") == platform_filter]

    if not performances:
        output_error(f"平台 {platform_filter} 暂无历史表现数据", code="NO_DATA")
        return

    analysis = {}

    # 1. 按话题分析
    topic_groups = _group_by(performances, "topic")
    topic_analysis = []
    for topic, records in topic_groups.items():
        if topic == "未知" or not topic:
            continue
        topic_analysis.append({
            "topic": topic,
            "count": len(records),
            "avg_score": _avg_score(records),
            "avg_rate": _avg_rate(records),
        })
    topic_analysis.sort(key=lambda x: x["avg_score"], reverse=True)
    analysis["by_topic"] = topic_analysis[:10]

    # 2. 按平台分析
    platform_groups = _group_by(performances, "platform")
    platform_analysis = []
    for platform, records in platform_groups.items():
        platform_analysis.append({
            "platform": platform,
            "count": len(records),
            "avg_score": _avg_score(records),
            "avg_rate": _avg_rate(records),
        })
    platform_analysis.sort(key=lambda x: x["avg_score"], reverse=True)
    analysis["by_platform"] = platform_analysis

    # 3. 按发布时间（小时）分析
    hour_buckets: Dict[int, List[Dict]] = defaultdict(list)
    for p in performances:
        hour = _extract_hour(p.get("posting_time", ""))
        if hour is not None:
            hour_buckets[hour].append(p)

    time_analysis = []
    for hour in sorted(hour_buckets.keys()):
        records = hour_buckets[hour]
        time_analysis.append({
            "hour": hour,
            "time_range": f"{hour:02d}:00-{hour:02d}:59",
            "count": len(records),
            "avg_score": _avg_score(records),
            "avg_rate": _avg_rate(records),
        })
    time_analysis.sort(key=lambda x: x["avg_score"], reverse=True)
    analysis["by_time"] = time_analysis

    # 4. 按星期几分析
    weekday_buckets: Dict[int, List[Dict]] = defaultdict(list)
    for p in performances:
        wd = _extract_weekday(p.get("posting_time", ""))
        if wd is not None:
            weekday_buckets[wd].append(p)

    weekday_analysis = []
    for wd in sorted(weekday_buckets.keys()):
        records = weekday_buckets[wd]
        weekday_analysis.append({
            "weekday": wd,
            "weekday_name": _WEEKDAY_NAMES[wd],
            "count": len(records),
            "avg_score": _avg_score(records),
            "avg_rate": _avg_rate(records),
        })
    weekday_analysis.sort(key=lambda x: x["avg_score"], reverse=True)
    analysis["by_weekday"] = weekday_analysis

    # 5. 按格式分析
    format_groups = _group_by(performances, "format")
    format_analysis = []
    for fmt, records in format_groups.items():
        if fmt == "未知" or not fmt:
            continue
        format_analysis.append({
            "format": fmt,
            "count": len(records),
            "avg_score": _avg_score(records),
            "avg_rate": _avg_rate(records),
        })
    format_analysis.sort(key=lambda x: x["avg_score"], reverse=True)
    analysis["by_format"] = format_analysis

    # 6. 生成洞察摘要
    insights = _generate_insights(analysis, performances)
    analysis["insights"] = insights

    # 更新分析计数
    learning["metadata"]["analysis_count"] = learning["metadata"].get("analysis_count", 0) + 1
    _save_learning_data(learning)

    output_success({
        "message": f"已分析 {len(performances)} 条内容表现记录",
        "analysis": analysis,
    })


def _generate_insights(analysis: Dict, performances: List[Dict]) -> List[str]:
    """根据分析结果生成自然语言洞察。

    Args:
        analysis: 分析结果字典。
        performances: 原始表现记录列表。

    Returns:
        洞察列表（字符串）。
    """
    insights = []
    overall_avg = _avg_score(performances)

    # 话题洞察
    by_topic = analysis.get("by_topic", [])
    if by_topic and len(by_topic) >= 2:
        best = by_topic[0]
        ratio = round(best["avg_score"] / overall_avg, 1) if overall_avg > 0 else 0
        if ratio > 1.5:
            insights.append(
                f"「{best['topic']}」相关内容平均互动得分 {best['avg_score']}，"
                f"是整体均值的 {ratio} 倍，建议多产出相关内容"
            )

    # 平台洞察
    by_platform = analysis.get("by_platform", [])
    if len(by_platform) >= 2:
        best_plat = by_platform[0]
        worst_plat = by_platform[-1]
        if best_plat["avg_score"] > worst_plat["avg_score"] * 2:
            insights.append(
                f"{best_plat['platform']} 平台表现最佳（均分 {best_plat['avg_score']}），"
                f"建议优先在该平台发布内容"
            )

    # 时间洞察
    by_time = analysis.get("by_time", [])
    if by_time:
        best_time = by_time[0]
        insights.append(
            f"最佳发布时段为 {best_time['time_range']}，"
            f"平均互动得分 {best_time['avg_score']}（互动率 {best_time['avg_rate']}%）"
        )

    # 星期洞察
    by_weekday = analysis.get("by_weekday", [])
    if by_weekday:
        best_wd = by_weekday[0]
        insights.append(
            f"{best_wd['weekday_name']}发布的内容表现最好，"
            f"平均互动得分 {best_wd['avg_score']}"
        )

    # 格式洞察
    by_format = analysis.get("by_format", [])
    if by_format and len(by_format) >= 2:
        best_fmt = by_format[0]
        insights.append(
            f"「{best_fmt['format']}」格式的内容效果最好，"
            f"平均互动得分 {best_fmt['avg_score']}"
        )

    if not insights:
        insights.append("数据量较少，建议持续记录更多内容表现以获得更准确的分析")

    return insights


# ============================================================
# 操作：推荐话题
# ============================================================

def suggest_topic(data: Optional[Dict[str, Any]] = None) -> None:
    """基于历史表现数据推荐下一个内容话题。

    可选字段: platform, count（推荐数量，默认 5）

    考虑因素:
    - 历史高互动话题
    - 用户偏好的话题
    - 避开已拒绝的建议
    - 相关话题拓展

    Args:
        data: 可选的过滤条件字典。
    """
    learning = _get_learning_data()
    performances = learning["performances"]
    prefs = learning["preferences"]
    count = data.get("count", 5) if data else 5
    platform_filter = data.get("platform") if data else None

    if platform_filter:
        performances = [p for p in performances if p.get("platform") == platform_filter]

    suggestions = []
    rejected = set(prefs.get("rejected_suggestions", []))

    # 1. 从高表现话题中推荐
    topic_groups = _group_by(performances, "topic")
    topic_scores = []
    for topic, records in topic_groups.items():
        if not topic or topic == "未知":
            continue
        if topic in rejected:
            continue
        avg = _avg_score(records)
        topic_scores.append((topic, avg, len(records)))

    topic_scores.sort(key=lambda x: x[1], reverse=True)

    for topic, avg_score, cnt in topic_scores[:count]:
        reason = f"历史 {cnt} 篇相关内容平均互动得分 {avg_score}"
        if platform_filter:
            reason += f"（{platform_filter} 平台）"
        suggestions.append({
            "topic": topic,
            "reason": reason,
            "confidence": "高" if cnt >= 3 else "中",
            "avg_score": avg_score,
            "sample_count": cnt,
        })

    # 2. 从用户偏好话题中补充
    preferred = prefs.get("preferred_topics", [])
    existing_topics = {s["topic"] for s in suggestions}
    for topic in preferred:
        if len(suggestions) >= count:
            break
        if topic in existing_topics or topic in rejected:
            continue
        suggestions.append({
            "topic": topic,
            "reason": "用户偏好话题",
            "confidence": "中",
            "avg_score": 0,
            "sample_count": 0,
        })

    # 3. 从标签中挖掘潜在话题
    tag_counter: Dict[str, int] = defaultdict(int)
    tag_scores: Dict[str, float] = defaultdict(float)
    for p in performances:
        score = p.get("engagement_score", 0)
        for tag in p.get("tags", []):
            tag_counter[tag] += 1
            tag_scores[tag] += score

    tag_avg = []
    for tag, cnt in tag_counter.items():
        if tag in existing_topics or tag in rejected:
            continue
        if cnt >= 2:
            tag_avg.append((tag, round(tag_scores[tag] / cnt, 2), cnt))

    tag_avg.sort(key=lambda x: x[1], reverse=True)
    for tag, avg, cnt in tag_avg:
        if len(suggestions) >= count:
            break
        existing_topics.add(tag)
        suggestions.append({
            "topic": tag,
            "reason": f"高互动标签（{cnt} 次出现，均分 {avg}）",
            "confidence": "中" if cnt >= 3 else "低",
            "avg_score": avg,
            "sample_count": cnt,
        })

    if not suggestions:
        output_success({
            "message": "暂无足够数据生成话题推荐，建议先记录更多内容表现",
            "suggestions": [],
        })
        return

    output_success({
        "message": f"为你推荐 {len(suggestions)} 个话题",
        "suggestions": suggestions,
    })


# ============================================================
# 操作：推荐发布时间
# ============================================================

def suggest_timing(data: Optional[Dict[str, Any]] = None) -> None:
    """推荐各平台最佳发布时间。

    可选字段: platform

    基于历史发布时间和互动数据，推荐最优发布时段和星期。

    Args:
        data: 可选的过滤条件字典。
    """
    learning = _get_learning_data()
    performances = learning["performances"]
    platform_filter = data.get("platform") if data else None

    if platform_filter:
        performances = [p for p in performances if p.get("platform") == platform_filter]

    if not performances:
        output_error("暂无历史表现数据，无法推荐发布时间", code="NO_DATA")
        return

    # 按平台分组分析
    platform_groups = _group_by(performances, "platform")
    recommendations = {}

    for platform, records in platform_groups.items():
        # 按小时分析
        hour_data: Dict[int, List[float]] = defaultdict(list)
        for r in records:
            hour = _extract_hour(r.get("posting_time", ""))
            if hour is not None:
                hour_data[hour].append(r.get("engagement_score", 0))

        best_hours = []
        for hour, scores in hour_data.items():
            avg = round(sum(scores) / len(scores), 2)
            best_hours.append({"hour": hour, "time": f"{hour:02d}:00", "avg_score": avg, "count": len(scores)})
        best_hours.sort(key=lambda x: x["avg_score"], reverse=True)

        # 按星期分析
        weekday_data: Dict[int, List[float]] = defaultdict(list)
        for r in records:
            wd = _extract_weekday(r.get("posting_time", ""))
            if wd is not None:
                weekday_data[wd].append(r.get("engagement_score", 0))

        best_weekdays = []
        for wd, scores in weekday_data.items():
            avg = round(sum(scores) / len(scores), 2)
            best_weekdays.append({
                "weekday": wd,
                "weekday_name": _WEEKDAY_NAMES[wd],
                "avg_score": avg,
                "count": len(scores),
            })
        best_weekdays.sort(key=lambda x: x["avg_score"], reverse=True)

        # 生成推荐
        rec = {
            "platform": platform,
            "total_records": len(records),
            "best_hours": best_hours[:3],
            "best_weekdays": best_weekdays[:3],
            "recommendation": "",
        }

        # 组合推荐语
        parts = []
        if best_hours:
            top_hour = best_hours[0]
            parts.append(f"建议在 {top_hour['time']} 左右发布（均分 {top_hour['avg_score']}）")
        if best_weekdays:
            top_wd = best_weekdays[0]
            parts.append(f"{top_wd['weekday_name']}效果最佳（均分 {top_wd['avg_score']}）")

        rec["recommendation"] = "；".join(parts) if parts else "数据不足，建议持续记录"
        recommendations[platform] = rec

    output_success({
        "message": f"已分析 {len(recommendations)} 个平台的最佳发布时间",
        "recommendations": recommendations,
    })


# ============================================================
# 操作：统计面板
# ============================================================

def stats(data: Optional[Dict[str, Any]] = None) -> None:
    """内容表现统计面板。

    可选字段: platform, limit（排行数量，默认 5）

    展示：
    - 总体统计（内容数、平均得分、平均互动率）
    - 最佳内容 Top N
    - 最差内容 Top N
    - 各平台平均表现
    - 各话题平均表现

    Args:
        data: 可选的过滤条件字典。
    """
    learning = _get_learning_data()
    performances = learning["performances"]
    limit = data.get("limit", 5) if data else 5
    platform_filter = data.get("platform") if data else None

    if platform_filter:
        performances = [p for p in performances if p.get("platform") == platform_filter]

    if not performances:
        output_error("暂无历史表现数据", code="NO_DATA")
        return

    # 总体统计
    total_count = len(performances)
    avg_score_all = _avg_score(performances)
    avg_rate_all = _avg_rate(performances)

    # 排序获取最佳和最差
    sorted_by_score = sorted(performances, key=lambda x: x.get("engagement_score", 0), reverse=True)
    best_posts = []
    for p in sorted_by_score[:limit]:
        best_posts.append({
            "content_id": p.get("content_id", ""),
            "title": p.get("title", ""),
            "platform": p.get("platform", ""),
            "topic": p.get("topic", ""),
            "engagement_score": p.get("engagement_score", 0),
            "engagement_rate": p.get("engagement_rate", 0),
        })

    worst_posts = []
    for p in sorted_by_score[-limit:]:
        worst_posts.append({
            "content_id": p.get("content_id", ""),
            "title": p.get("title", ""),
            "platform": p.get("platform", ""),
            "topic": p.get("topic", ""),
            "engagement_score": p.get("engagement_score", 0),
            "engagement_rate": p.get("engagement_rate", 0),
        })
    worst_posts.reverse()

    # 按平台统计
    platform_groups = _group_by(performances, "platform")
    platform_stats = []
    for platform, records in platform_groups.items():
        platform_stats.append({
            "platform": platform,
            "count": len(records),
            "avg_score": _avg_score(records),
            "avg_rate": _avg_rate(records),
        })
    platform_stats.sort(key=lambda x: x["avg_score"], reverse=True)

    # 按话题统计
    topic_groups = _group_by(performances, "topic")
    topic_stats = []
    for topic, records in topic_groups.items():
        if not topic or topic == "未知":
            continue
        topic_stats.append({
            "topic": topic,
            "count": len(records),
            "avg_score": _avg_score(records),
            "avg_rate": _avg_rate(records),
        })
    topic_stats.sort(key=lambda x: x["avg_score"], reverse=True)

    dashboard = {
        "overview": {
            "total_records": total_count,
            "avg_engagement_score": avg_score_all,
            "avg_engagement_rate": avg_rate_all,
            "first_record": learning["metadata"].get("first_record_at", ""),
            "last_record": learning["metadata"].get("last_record_at", ""),
        },
        "best_posts": best_posts,
        "worst_posts": worst_posts,
        "by_platform": platform_stats,
        "by_topic": topic_stats[:10],
        "preferences": learning["preferences"],
    }

    output_success({
        "message": f"内容表现统计面板（共 {total_count} 条记录）",
        "dashboard": dashboard,
    })


# ============================================================
# 主入口
# ============================================================

def main() -> None:
    """主函数：解析命令行参数并分发操作。"""
    parser = parse_common_args("content-engine 自学习内容智能")
    args = parser.parse_args()

    action = args.action.lower()

    try:
        data = load_input_data(args)
    except ValueError as e:
        output_error(str(e), code="INPUT_ERROR")
        return

    actions = {
        "record-performance": lambda: record_performance(data or {}),
        "record-preference": lambda: record_preference(data or {}),
        "analyze": lambda: analyze(data),
        "suggest-topic": lambda: suggest_topic(data),
        "suggest-timing": lambda: suggest_timing(data),
        "stats": lambda: stats(data),
    }

    handler = actions.get(action)
    if handler:
        handler()
    else:
        valid_actions = "、".join(actions.keys())
        output_error(f"未知操作: {action}，支持的操作: {valid_actions}", code="INVALID_ACTION")


if __name__ == "__main__":
    main()
