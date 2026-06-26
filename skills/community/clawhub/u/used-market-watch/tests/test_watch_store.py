from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from watch_store import remove_rule, set_rule_enabled, upsert_rule


def test_upsert_rule_creates_then_updates_existing_name():
    state = {"rules": []}
    created, is_created = upsert_rule(
        state,
        {
            "name": "아이폰 감시",
            "query": "아이폰 15 프로",
            "limit": 12,
            "min_price": None,
            "max_price": 1200000,
            "notify_on_new": True,
            "notify_on_price_drop": False,
            "enabled": True,
            "delivery_mode": "alert",
            "action": "watch",
            "schedule": {"kind": "interval", "every_hours": 1, "label": "1시간마다", "cron": "0 */1 * * *"},
            "plan_hints": {"cron_example": '0 */1 * * * python skills/used-market-watch/scripts/used_market_watch.py watch-check "아이폰 감시" --alerts-only --json'},
        },
    )
    assert is_created is True
    assert created["schedule"]["kind"] == "interval"
    updated, is_created = upsert_rule(
        state,
        {
            "name": "아이폰 감시",
            "query": "아이폰 15 프로 max",
            "limit": 5,
            "min_price": None,
            "max_price": 1100000,
            "notify_on_new": True,
            "notify_on_price_drop": True,
            "enabled": False,
            "delivery_mode": "briefing",
            "action": "brief",
            "schedule": {"kind": "daily", "hour": 8, "minute": 0, "label": "매일 08:00", "cron": "0 8 * * *"},
            "plan_hints": {"cron_example": '0 8 * * * python skills/used-market-watch/scripts/used_market_watch.py watch-check "아이폰 감시" --json'},
        },
    )
    assert is_created is False
    assert created["id"] == updated["id"]
    assert updated["query"] == "아이폰 15 프로 max"
    assert updated["limit"] == 5
    assert updated["enabled"] is False
    assert updated["delivery_mode"] == "briefing"
    assert updated["schedule"]["kind"] == "daily"


def test_enable_disable_and_remove_rule():
    state = {
        "rules": [
            {
                "id": "rule-1",
                "name": "맥북 감시",
                "query": "맥북",
                "limit": 12,
                "notify_on_new": True,
                "notify_on_price_drop": True,
                "enabled": True,
            }
        ]
    }
    rule = set_rule_enabled(state, "맥북 감시", False)
    assert rule and rule["enabled"] is False
    removed = remove_rule(state, "rule-1")
    assert removed and removed["name"] == "맥북 감시"
    assert state["rules"] == []
