#!/usr/bin/env python3
"""
OpenClaw Skill helper script for reveyes amazon-review skill.
Usage: python fetch.py <asin> [marketplace] [pages] [filter_star]
"""
import json
import os
import sys
from collections import Counter

try:
    from reveyes import ReveyesClient
    from reveyes.exceptions import (
        AuthenticationError,
        BadParamsError,
        InsufficientCreditsError,
    )
except ImportError:
    print(json.dumps({
        "error": "reveyes SDK not installed. Run: pip install reveyes",
        "code": "IMPORT_ERROR",
    }))
    sys.exit(1)


def main():
    asin        = sys.argv[1] if len(sys.argv) > 1 else None
    marketplace = sys.argv[2] if len(sys.argv) > 2 else "US"
    pages       = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    filter_star = sys.argv[4] if len(sys.argv) > 4 else "all_stars"

    if not asin:
        print(json.dumps({"error": "ASIN is required", "code": "BAD_PARAMS"}))
        sys.exit(1)

    api_key = os.environ.get("REVEYES_API_KEY")
    if not api_key:
        print(json.dumps({
            "error": "REVEYES_API_KEY environment variable is not set.",
            "code": "AUTH_ERROR",
        }))
        sys.exit(1)

    client = ReveyesClient(api_key=api_key)

    try:
        task = client.fetch_reviews([{
            "asin": asin,
            "marketplace": marketplace,
            "pages": pages,
            "filter_star": filter_star,
            "filter_sort_by": "recent",
        }])
    except AuthenticationError:
        print(json.dumps({"error": "API Key 无效，请检查 REVEYES_API_KEY", "code": "AUTH_ERROR"}))
        sys.exit(1)
    except InsufficientCreditsError:
        print(json.dumps({"error": "积分不足，请前往 https://www.reveyes.cn 充值", "code": "NO_CREDITS"}))
        sys.exit(1)
    except BadParamsError as e:
        print(json.dumps({"error": f"参数错误：{e}", "code": "BAD_PARAMS"}))
        sys.exit(1)

    try:
        result = client.wait_for_task(task.task_id, poll_interval=5, timeout=300)
    except TimeoutError:
        print(json.dumps({
            "error": "任务超时（5 分钟），可用 task_id 稍后手动查询",
            "task_id": task.task_id,
            "code": "TIMEOUT",
        }))
        sys.exit(1)

    all_reviews = list(client.iter_all_reviews(task.task_id, page_size=200))

    rating_counter = Counter(r.rating for r in all_reviews if r.rating)
    total = len(all_reviews)
    avg = sum(r.rating for r in all_reviews if r.rating) / total if total else 0

    low_reviews = [r for r in all_reviews if r.rating and r.rating <= 2]
    low_reviews.sort(key=lambda r: r.helpful_votes or 0, reverse=True)

    def review_to_dict(r):
        return {
            "review_id":        r.review_id,
            "asin":             r.asin,
            "marketplace":      r.marketplace,
            "rating":           r.rating,
            "title":            r.title,
            "review_date":      r.review_date,
            "review_content":   r.review_content,
            "user_name":        r.user_name,
            "profile_url":      r.profile_url,
            "verified_purchase": bool(r.verified_purchase),
            "helpful_votes":    r.helpful_votes,
            "product_variant":  r.product_variant,
            "images":           r.images or [],
            "videos":           r.videos or [],
            "page":             r.page,
        }

    output = {
        # ── 任务元信息 ──────────────────────────────────────────
        "task_id":        task.task_id,
        "asin":           asin,
        "marketplace":    marketplace,
        "filter_star":    filter_star,
        "credits_used":   result.actual_deduct,
        # ── 汇总统计 ───────────────────────────────────────────
        "summary": {
            "total_reviews":     total,
            "average_rating":    round(avg, 2),
            "rating_distribution": {str(s): rating_counter.get(s, 0) for s in range(5, 0, -1)},
            "verified_purchase_count": sum(1 for r in all_reviews if r.verified_purchase),
            "has_image_count":   sum(1 for r in all_reviews if r.images),
            "has_video_count":   sum(1 for r in all_reviews if r.videos),
            "negative_count":    len(low_reviews),
            "negative_rate":     round(len(low_reviews) / total * 100, 1) if total else 0,
        },
        # ── ASIN 子任务明细 ────────────────────────────────────
        "items_summary": [
            {
                "asin":         i.asin,
                "marketplace":  i.marketplace,
                "status":       i.status,
                "pages":        i.pages,
                "actual_pages": i.actual_pages,
                "review_count": i.review_count,
            }
            for i in result.items_summary
        ],
        # ── 差评列表（完整字段，按有用票数排序）──────────────────
        "negative_reviews": [review_to_dict(r) for r in low_reviews],
        # ── 全量评论列表（完整字段）──────────────────────────────
        "all_reviews": [review_to_dict(r) for r in all_reviews],
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
