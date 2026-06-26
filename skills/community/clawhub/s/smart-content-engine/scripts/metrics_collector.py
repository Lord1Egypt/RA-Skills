#!/usr/bin/env python3
"""
content-engine 数据指标采集模块

从各平台采集内容表现数据，生成对比报告和可视化图表。
此模块为付费版功能。
"""

import json
import os
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

from utils import (
    check_subscription,
    format_platform_name,
    generate_id,
    get_data_file,
    load_input_data,
    now_iso,
    output_error,
    output_success,
    parse_common_args,
    read_json_file,
    require_paid_feature,
    validate_platform,
    write_json_file,
    PLATFORMS,
)

# 延迟导入学习引擎
_learning_engine = None


def _get_learning_engine():
    """延迟导入 learning_engine 模块。"""
    global _learning_engine
    if _learning_engine is None:
        try:
            import learning_engine as _learning_engine
        except ImportError:
            _learning_engine = None
    return _learning_engine


def _auto_record_to_learning(content_id: str, platform: str,
                              metrics: Dict[str, Any],
                              content: Optional[Dict] = None) -> None:
    """采集指标后自动记录到学习引擎。

    Args:
        content_id: 内容 ID。
        platform: 平台标识。
        metrics: 采集到的指标数据。
        content: 内容详情（可选）。
    """
    le = _get_learning_engine()
    if le is None:
        return
    if "error" in metrics:
        return

    try:
        record_data = {
            "content_id": content_id,
            "platform": platform,
            "metrics": metrics,
        }
        if content:
            record_data["title"] = content.get("title", "")
            record_data["tags"] = content.get("tags", [])
            record_data["topic"] = content.get("tags", [""])[0] if content.get("tags") else ""
            record_data["posting_time"] = content.get("published_at", "")
            record_data["length"] = len(content.get("body", ""))
        le.record_performance(record_data)
    except Exception:
        pass  # 记录失败不影响主流程


# ============================================================
# 数据文件路径
# ============================================================

METRICS_FILE = "metrics.json"
CONTENTS_FILE = "contents.json"
PUBLISH_HISTORY_FILE = "publish_history.json"


def _get_metrics() -> List[Dict[str, Any]]:
    """读取所有指标数据。"""
    return read_json_file(get_data_file(METRICS_FILE))


def _save_metrics(metrics: List[Dict[str, Any]]) -> None:
    """保存指标数据。"""
    write_json_file(get_data_file(METRICS_FILE), metrics)


def _get_contents() -> List[Dict[str, Any]]:
    """读取所有内容数据。"""
    return read_json_file(get_data_file(CONTENTS_FILE))


def _find_content(contents: List[Dict], content_id: str) -> Optional[Dict]:
    """根据 ID 查找内容。"""
    for c in contents:
        if c.get("id") == content_id:
            return c
    return None


def _get_publish_history() -> List[Dict[str, Any]]:
    """读取发布历史。"""
    return read_json_file(get_data_file(PUBLISH_HISTORY_FILE))


# ============================================================
# 平台指标定义
# ============================================================

# 各平台指标字段
PLATFORM_METRICS = {
    "twitter": ["likes", "retweets", "replies", "impressions"],
    "linkedin": ["likes", "comments", "shares", "views"],
    "wechat": ["reads", "shares", "favorites"],
    "medium": ["reads", "claps", "responses"],
    "blog": [],  # 博客不采集指标
}

# 指标中文名映射
METRIC_NAMES = {
    "likes": "点赞",
    "retweets": "转发",
    "replies": "回复",
    "impressions": "曝光",
    "comments": "评论",
    "shares": "分享",
    "views": "浏览",
    "reads": "阅读",
    "claps": "鼓掌",
    "responses": "回应",
    "favorites": "收藏",
}


# ============================================================
# 平台指标采集
# ============================================================

def _api_get(url: str, headers: Optional[Dict] = None) -> Dict[str, Any]:
    """发送 GET 请求获取 API 数据。

    Args:
        url: 请求 URL。
        headers: 请求头。

    Returns:
        响应数据字典。
    """
    if headers is None:
        headers = {}

    req = Request(url, headers=headers, method="GET")
    try:
        with urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        raise Exception(f"HTTP {e.code}: {error_body}")
    except URLError as e:
        raise Exception(f"网络请求失败: {e.reason}")


def _collect_twitter_metrics(publish_result: Dict[str, Any]) -> Dict[str, Any]:
    """采集 Twitter 指标数据。

    Args:
        publish_result: 发布结果（包含 tweet_ids）。

    Returns:
        指标数据字典。
    """
    bearer_token = os.environ.get("CE_TWITTER_BEARER_TOKEN", "")
    if not bearer_token:
        return {"error": "未配置 CE_TWITTER_BEARER_TOKEN"}

    tweet_ids = publish_result.get("tweet_ids", [])
    if not tweet_ids:
        return {"error": "无推文 ID"}

    headers = {"Authorization": f"Bearer {bearer_token}"}

    total_metrics = {"likes": 0, "retweets": 0, "replies": 0, "impressions": 0}

    for tweet_id in tweet_ids:
        try:
            url = (
                f"https://api.twitter.com/2/tweets/{tweet_id}"
                f"?tweet.fields=public_metrics"
            )
            data = _api_get(url, headers)
            metrics = data.get("data", {}).get("public_metrics", {})
            total_metrics["likes"] += metrics.get("like_count", 0)
            total_metrics["retweets"] += metrics.get("retweet_count", 0)
            total_metrics["replies"] += metrics.get("reply_count", 0)
            total_metrics["impressions"] += metrics.get("impression_count", 0)
        except Exception as e:
            return {"error": f"采集推文 {tweet_id} 指标失败: {str(e)}"}

    return total_metrics


def _collect_linkedin_metrics(publish_result: Dict[str, Any]) -> Dict[str, Any]:
    """采集 LinkedIn 指标数据。

    Args:
        publish_result: 发布结果（包含 post_id）。

    Returns:
        指标数据字典。
    """
    access_token = os.environ.get("CE_LINKEDIN_ACCESS_TOKEN", "")
    if not access_token:
        return {"error": "未配置 CE_LINKEDIN_ACCESS_TOKEN"}

    post_id = publish_result.get("post_id", "")
    if not post_id:
        return {"error": "无帖子 ID"}

    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        url = f"https://api.linkedin.com/v2/socialActions/{post_id}"
        data = _api_get(url, headers)
        return {
            "likes": data.get("likesSummary", {}).get("totalLikes", 0),
            "comments": data.get("commentsSummary", {}).get("totalFirstLevelComments", 0),
            "shares": data.get("sharesSummary", {}).get("totalShares", 0) if "sharesSummary" in data else 0,
            "views": 0,  # LinkedIn API 不直接提供浏览量
        }
    except Exception as e:
        return {"error": f"采集 LinkedIn 指标失败: {str(e)}"}


def _collect_wechat_metrics(publish_result: Dict[str, Any]) -> Dict[str, Any]:
    """采集微信公众号指标数据。

    Args:
        publish_result: 发布结果（包含 publish_id）。

    Returns:
        指标数据字典。
    """
    appid = os.environ.get("CE_WECHAT_APPID", "")
    secret = os.environ.get("CE_WECHAT_SECRET", "")

    if not appid or not secret:
        return {"error": "未配置 CE_WECHAT_APPID 和 CE_WECHAT_SECRET"}

    # 获取 access_token
    try:
        token_url = (
            f"https://api.weixin.qq.com/cgi-bin/token?"
            f"grant_type=client_credential&appid={appid}&secret={secret}"
        )
        req = Request(token_url, method="GET")
        with urlopen(req, timeout=30) as resp:
            token_data = json.loads(resp.read().decode("utf-8"))

        if "access_token" not in token_data:
            return {"error": f"获取 access_token 失败: {token_data.get('errmsg', '')}"}

        access_token = token_data["access_token"]
    except Exception as e:
        return {"error": f"获取微信 access_token 失败: {str(e)}"}

    # 获取文章数据统计
    publish_id = publish_result.get("publish_id", "")
    if not publish_id:
        return {"error": "无 publish_id"}

    try:
        url = (
            f"https://api.weixin.qq.com/cgi-bin/freepublish/getarticle?"
            f"access_token={access_token}"
        )
        req = Request(
            url,
            data=json.dumps({"publish_id": publish_id}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        # 解析文章统计信息（微信 API 返回格式）
        return {
            "reads": data.get("read_num", 0),
            "shares": data.get("share_num", 0),
            "favorites": data.get("collect_num", 0),
        }
    except Exception as e:
        return {"error": f"采集微信指标失败: {str(e)}"}


def _collect_medium_metrics(publish_result: Dict[str, Any]) -> Dict[str, Any]:
    """采集 Medium 指标数据。

    注意: Medium API 对指标数据的支持有限。

    Args:
        publish_result: 发布结果（包含 post_id, url）。

    Returns:
        指标数据字典。
    """
    # Medium API 不直接提供详细指标，返回基本信息
    return {
        "reads": 0,
        "claps": 0,
        "responses": 0,
        "note": "Medium API 暂不支持实时指标采集，请通过 Medium 后台查看",
    }


# 平台指标采集器注册表
_COLLECTORS = {
    "twitter": _collect_twitter_metrics,
    "linkedin": _collect_linkedin_metrics,
    "wechat": _collect_wechat_metrics,
    "medium": _collect_medium_metrics,
}


# ============================================================
# 指标操作
# ============================================================

def collect_metrics(data: Dict[str, Any]) -> None:
    """采集内容在各平台的表现指标。

    必填字段: content_id
    可选字段: platform（不指定则采集所有已发布平台）

    Args:
        data: 包含内容 ID 和可选平台的字典。
    """
    if not require_paid_feature("metrics", "指标采集"):
        return

    content_id = data.get("content_id") or data.get("id")
    if not content_id:
        output_error("内容ID（content_id）为必填字段", code="VALIDATION_ERROR")
        return

    # 查找内容的发布历史
    history = _get_publish_history()
    content_history = [h for h in history if h.get("content_id") == content_id]

    if not content_history:
        output_error(f"内容 {content_id} 暂无发布记录", code="NOT_FOUND")
        return

    # 按平台过滤
    platform_filter = data.get("platform")
    if platform_filter:
        try:
            platform_filter = validate_platform(platform_filter)
        except ValueError as e:
            output_error(str(e), code="VALIDATION_ERROR")
            return
        content_history = [h for h in content_history if h.get("platform") == platform_filter]

    # 采集各平台指标
    metrics_data = _get_metrics()
    results = []

    for record in content_history:
        platform = record.get("platform", "")
        publish_result = record.get("result", {})

        if not publish_result.get("success"):
            continue

        collector = _COLLECTORS.get(platform)
        if not collector:
            continue

        metrics = collector(publish_result)

        metric_record = {
            "id": generate_id("MT"),
            "content_id": content_id,
            "platform": platform,
            "platform_name": format_platform_name(platform),
            "metrics": metrics,
            "collected_at": now_iso(),
        }

        # 更新或添加指标记录
        metrics_data = [
            m for m in metrics_data
            if not (m.get("content_id") == content_id and m.get("platform") == platform)
        ]
        metrics_data.append(metric_record)
        results.append(metric_record)

        # 自动记录到学习引擎
        content_detail = _find_content(_get_contents(), content_id)
        _auto_record_to_learning(content_id, platform, metrics, content_detail)

    _save_metrics(metrics_data)

    output_success({
        "message": f"已采集 {len(results)} 个平台的指标数据",
        "content_id": content_id,
        "metrics": results,
    })


def generate_report(data: Dict[str, Any]) -> None:
    """生成内容表现报告。

    必填字段: content_id

    Args:
        data: 包含内容 ID 的字典。
    """
    if not require_paid_feature("metrics", "指标报告"):
        return

    content_id = data.get("content_id") or data.get("id")
    if not content_id:
        output_error("内容ID（content_id）为必填字段", code="VALIDATION_ERROR")
        return

    contents = _get_contents()
    content = _find_content(contents, content_id)
    if not content:
        output_error(f"未找到ID为 {content_id} 的内容", code="NOT_FOUND")
        return

    metrics_data = _get_metrics()
    content_metrics = [m for m in metrics_data if m.get("content_id") == content_id]

    if not content_metrics:
        output_error(f"内容 {content_id} 暂无指标数据，请先执行 collect 操作", code="NOT_FOUND")
        return

    # 构建报告
    report_lines = []
    report_lines.append(f"# 内容表现报告")
    report_lines.append("")
    report_lines.append(f"**标题**: {content.get('title', '')}")
    report_lines.append(f"**状态**: {content.get('status', '')}")
    report_lines.append(f"**创建时间**: {content.get('created_at', '')}")
    report_lines.append(f"**发布时间**: {content.get('published_at', '')}")
    report_lines.append("")

    # 跨平台对比表格
    report_lines.append("## 跨平台数据对比")
    report_lines.append("")

    # 收集所有指标名称
    all_metric_keys = set()
    for m in content_metrics:
        metrics = m.get("metrics", {})
        if "error" not in metrics:
            all_metric_keys.update(metrics.keys())

    # 移除非数值字段
    all_metric_keys.discard("note")
    all_metric_keys.discard("error")

    if all_metric_keys:
        sorted_keys = sorted(all_metric_keys)
        header = "| 指标 | " + " | ".join(
            format_platform_name(m.get("platform", ""))
            for m in content_metrics
            if "error" not in m.get("metrics", {})
        ) + " |"
        separator = "|------|" + "|".join(
            "------:" for m in content_metrics
            if "error" not in m.get("metrics", {})
        ) + "|"

        report_lines.append(header)
        report_lines.append(separator)

        for key in sorted_keys:
            row = f"| {METRIC_NAMES.get(key, key)} |"
            for m in content_metrics:
                metrics = m.get("metrics", {})
                if "error" not in metrics:
                    val = metrics.get(key, "-")
                    row += f" {val} |"
            report_lines.append(row)

        report_lines.append("")

    # 各平台详情
    report_lines.append("## 各平台详情")
    report_lines.append("")

    for m in content_metrics:
        platform = m.get("platform", "")
        metrics = m.get("metrics", {})
        collected_at = m.get("collected_at", "")

        report_lines.append(f"### {format_platform_name(platform)}")
        report_lines.append(f"*采集时间: {collected_at}*")
        report_lines.append("")

        if "error" in metrics:
            report_lines.append(f"> 采集失败: {metrics['error']}")
        else:
            for key, value in metrics.items():
                if key != "note":
                    report_lines.append(f"- **{METRIC_NAMES.get(key, key)}**: {value}")
            if "note" in metrics:
                report_lines.append(f"\n> {metrics['note']}")
        report_lines.append("")

    report = "\n".join(report_lines)

    output_success({
        "message": "指标报告已生成",
        "content_id": content_id,
        "report": report,
    })


def compare_metrics(data: Dict[str, Any]) -> None:
    """对比多条内容的表现指标。

    必填字段: content_ids（内容 ID 列表）

    Args:
        data: 包含内容 ID 列表的字典。
    """
    if not require_paid_feature("metrics", "指标对比"):
        return

    content_ids = data.get("content_ids", [])
    if not content_ids or len(content_ids) < 2:
        output_error("需要至少 2 个内容ID进行对比", code="VALIDATION_ERROR")
        return

    contents = _get_contents()
    metrics_data = _get_metrics()

    comparison = []
    for cid in content_ids:
        content = _find_content(contents, cid)
        if not content:
            continue

        content_metrics = [m for m in metrics_data if m.get("content_id") == cid]
        # 汇总各平台指标
        total = {}
        for m in content_metrics:
            metrics = m.get("metrics", {})
            if "error" not in metrics:
                for key, value in metrics.items():
                    if key != "note" and isinstance(value, (int, float)):
                        total[key] = total.get(key, 0) + value

        comparison.append({
            "content_id": cid,
            "title": content.get("title", ""),
            "total_metrics": total,
            "platforms": [m.get("platform") for m in content_metrics],
        })

    output_success({
        "message": f"已对比 {len(comparison)} 条内容",
        "comparison": comparison,
    })


def trending_metrics(data: Optional[Dict[str, Any]] = None) -> None:
    """查看内容指标趋势和热门内容。

    可选字段: platform, limit

    Args:
        data: 可选的过滤条件字典。
    """
    if not require_paid_feature("mermaid_chart", "趋势图表"):
        return

    metrics_data = _get_metrics()
    contents = _get_contents()

    platform_filter = data.get("platform") if data else None
    limit = data.get("limit", 10) if data else 10

    if platform_filter:
        try:
            platform_filter = validate_platform(platform_filter)
        except ValueError as e:
            output_error(str(e), code="VALIDATION_ERROR")
            return
        metrics_data = [m for m in metrics_data if m.get("platform") == platform_filter]

    # 按内容汇总指标
    content_totals = {}
    for m in metrics_data:
        cid = m.get("content_id", "")
        metrics = m.get("metrics", {})
        if "error" in metrics:
            continue

        if cid not in content_totals:
            content_totals[cid] = {"total_engagement": 0}

        for key, value in metrics.items():
            if key != "note" and isinstance(value, (int, float)):
                content_totals[cid]["total_engagement"] += value

    # 排序取 Top N
    sorted_contents = sorted(
        content_totals.items(),
        key=lambda x: x[1]["total_engagement"],
        reverse=True,
    )[:limit]

    # 构建 Mermaid 柱状图
    chart_data = []
    for cid, totals in sorted_contents:
        content = _find_content(contents, cid)
        title = content.get("title", cid)[:15] if content else cid[:15]
        chart_data.append({
            "label": title,
            "value": totals["total_engagement"],
        })

    mermaid_chart = ""
    if chart_data:
        labels = ", ".join(f'"{d["label"]}"' for d in chart_data)
        values = ", ".join(str(d["value"]) for d in chart_data)
        mermaid_chart = (
            f"```mermaid\n"
            f"xychart-beta\n"
            f'    title "内容互动排行"\n'
            f"    x-axis [{labels}]\n"
            f'    y-axis "互动总量"\n'
            f"    bar [{values}]\n"
            f"```"
        )

    trending_list = []
    for cid, totals in sorted_contents:
        content = _find_content(contents, cid)
        trending_list.append({
            "content_id": cid,
            "title": content.get("title", "") if content else "",
            "total_engagement": totals["total_engagement"],
        })

    output_success({
        "message": f"互动排行 Top {len(trending_list)}",
        "trending": trending_list,
        "chart": mermaid_chart,
    })


# ============================================================
# 学习洞察
# ============================================================

def learning_insights(data: Optional[Dict[str, Any]] = None) -> None:
    """基于学习引擎生成内容表现洞察。

    将当前内容的指标与历史平均值对比，给出改进建议。

    可选字段: content_id, platform

    Args:
        data: 可选的过滤条件字典。
    """
    if not require_paid_feature("metrics", "学习洞察"):
        return

    le = _get_learning_engine()
    if le is None:
        output_error("学习引擎模块不可用，无法生成洞察", code="MODULE_ERROR")
        return

    learning_data = le._get_learning_data()
    performances = learning_data.get("performances", [])

    if not performances:
        output_error("暂无历史表现数据，请先使用 collect 采集指标", code="NO_DATA")
        return

    content_id = data.get("content_id") or data.get("id") if data else None
    platform_filter = data.get("platform") if data else None

    if platform_filter:
        performances = [p for p in performances if p.get("platform") == platform_filter]

    # 计算历史平均值
    all_scores = [p.get("engagement_score", 0) for p in performances]
    all_rates = [p.get("engagement_rate", 0) for p in performances]
    avg_score = round(sum(all_scores) / len(all_scores), 2) if all_scores else 0
    avg_rate = round(sum(all_rates) / len(all_rates), 2) if all_rates else 0

    insights = {
        "historical_average": {
            "avg_engagement_score": avg_score,
            "avg_engagement_rate": avg_rate,
            "total_records": len(performances),
        },
        "comparison": None,
        "recommendations": [],
    }

    # 如果指定了具体内容，与历史对比
    if content_id:
        content_perfs = [p for p in performances if p.get("content_id") == content_id]
        if content_perfs:
            content_scores = [p.get("engagement_score", 0) for p in content_perfs]
            content_avg = round(sum(content_scores) / len(content_scores), 2)
            diff = round(content_avg - avg_score, 2)
            diff_pct = round((diff / avg_score) * 100, 1) if avg_score > 0 else 0

            insights["comparison"] = {
                "content_id": content_id,
                "content_avg_score": content_avg,
                "vs_historical": diff,
                "vs_historical_pct": diff_pct,
                "performance": "高于平均" if diff > 0 else ("低于平均" if diff < 0 else "持平"),
            }

            if diff < 0:
                insights["recommendations"].append(
                    f"当前内容互动得分（{content_avg}）低于历史平均值（{avg_score}），"
                    "建议参考高表现内容的话题和格式"
                )
    else:
        # 通用建议
        insights["recommendations"].append(
            f"历史平均互动得分 {avg_score}，互动率 {avg_rate}%"
        )

    # 调用学习引擎的分析
    try:
        # 直接获取分析洞察
        from collections import defaultdict as _dd
        topic_groups = {}
        for p in performances:
            topic = p.get("topic", "未知")
            if topic not in topic_groups:
                topic_groups[topic] = []
            topic_groups[topic].append(p.get("engagement_score", 0))

        top_topics = []
        for topic, scores in topic_groups.items():
            if topic == "未知" or not topic:
                continue
            avg = round(sum(scores) / len(scores), 2)
            top_topics.append({"topic": topic, "avg_score": avg, "count": len(scores)})

        top_topics.sort(key=lambda x: x["avg_score"], reverse=True)
        insights["top_performing_topics"] = top_topics[:5]

        if top_topics:
            best = top_topics[0]
            insights["recommendations"].append(
                f"建议多创作「{best['topic']}」相关内容（历史均分 {best['avg_score']}）"
            )
    except Exception:
        pass

    output_success({
        "message": "学习洞察分析完成",
        "insights": insights,
    })


# ============================================================
# 主入口
# ============================================================

def main() -> None:
    """主函数：解析命令行参数并分发操作。"""
    parser = parse_common_args("content-engine 指标采集")
    args = parser.parse_args()

    action = args.action.lower()

    try:
        data = load_input_data(args)
    except ValueError as e:
        output_error(str(e), code="INPUT_ERROR")
        return

    actions = {
        "collect": lambda: collect_metrics(data or {}),
        "report": lambda: generate_report(data or {}),
        "compare": lambda: compare_metrics(data or {}),
        "trending": lambda: trending_metrics(data),
        "insights": lambda: learning_insights(data),
    }

    handler = actions.get(action)
    if handler:
        handler()
    else:
        valid_actions = "、".join(actions.keys())
        output_error(f"未知操作: {action}，支持的操作: {valid_actions}", code="INVALID_ACTION")


if __name__ == "__main__":
    main()
