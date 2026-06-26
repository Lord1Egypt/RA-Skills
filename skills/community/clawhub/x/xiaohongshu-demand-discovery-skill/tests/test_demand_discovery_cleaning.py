from datetime import datetime

from scripts.demand_discovery import (
    FilterStats,
    clean_comments,
    extract_comments,
    load_keywords,
    parse_publish_time,
    stable_author_hash,
)


def test_load_keywords_dedupes_comma_values():
    assert load_keywords("求推荐,避雷,求推荐") == ["求推荐", "避雷"]


def test_author_hash_is_stable_and_does_not_echo_raw_value():
    first = stable_author_hash("user123")
    second = stable_author_hash("user123")
    assert first == second
    assert "user123" not in first


def test_clean_comments_filters_empty_duplicate_short_and_ads():
    stats = FilterStats()
    raw = [
        {"commentId": "1", "content": ""},
        {"commentId": "2", "content": "蹲"},
        {"commentId": "3", "content": "这个真的好用吗"},
        {"commentId": "4", "content": "这个真的好用吗"},
        {"commentId": "5", "content": "加微信 vx12345 领券"},
        {"commentId": "6", "content": "我买过，质感一般，容易坏"},
    ]

    cleaned = clean_comments(raw, max_comments=20, stats=stats)

    assert [item["commentId"] for item in cleaned] == ["3", "6"]
    assert stats.filtered_empty_comments == 1
    assert stats.filtered_short_comments == 1
    assert stats.filtered_duplicate_comments == 1
    assert stats.filtered_ad_comments == 1


def test_extract_comments_finds_nested_comment_like_items():
    detail = {
        "note": {
            "comments": [
                {
                    "commentId": "c1",
                    "content": "求平替",
                    "userInfo": {"userId": "u1"},
                    "subComments": [{"commentId": "c2", "content": "同求", "userInfo": {"userId": "u2"}}],
                }
            ]
        }
    }

    comments = extract_comments(detail)

    assert [item["commentId"] for item in comments] == ["c1", "c2"]


def test_parse_publish_time_uses_shanghai_timezone_for_relative_days():
    now = datetime.fromisoformat("2026-05-23T12:00:00+08:00")

    parsed, status = parse_publish_time("2天前", "Asia/Shanghai", now=now)

    assert status == "known"
    assert parsed.isoformat().startswith("2026-05-21T12:00:00")


def test_parse_publish_time_unknown_is_preserved():
    parsed, status = parse_publish_time("看不懂的时间字段", "Asia/Shanghai")

    assert parsed is None
    assert status == "publish_time_unknown"
