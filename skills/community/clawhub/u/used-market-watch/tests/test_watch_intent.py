from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from watch_intent import build_integration_bundle, parse_watch_request


def test_parse_watch_request_for_new_only():
    data = parse_watch_request('"아이폰 신규" 아이폰 15 프로 120만원 이하 당근 번장 신규만 감시 추가')
    assert data["name"] == "아이폰 신규"
    assert data["notify_on_new"] is True
    assert data["notify_on_price_drop"] is False
    assert data["max_price"] == 1200000
    assert data["delivery_mode"] == "alert"
    assert data["schedule"]["kind"] == "manual"
    assert "danggeun" in data["intent"]["markets"]
    assert "bunjang" in data["intent"]["markets"]


def test_parse_watch_request_for_price_drop_and_limit():
    data = parse_watch_request("맥북 에어 m2 가격하락만 감시 5개 잠실")
    assert data["notify_on_new"] is False
    assert data["notify_on_price_drop"] is True
    assert data["limit"] == 5
    assert data["intent"]["location"] and "잠실" in data["intent"]["location"]


def test_parse_watch_request_for_hourly_new_watch():
    data = parse_watch_request("아이폰 15 프로 1시간마다 신규만 감시해줘")
    assert data["notify_on_new"] is True
    assert data["notify_on_price_drop"] is False
    assert data["schedule"] == {
        "kind": "interval",
        "every_hours": 1,
        "label": "1시간마다",
        "cron": "0 */1 * * *",
    }
    assert data["plan_hints"]["recommended_command"].endswith('--alerts-only --json')


def test_parse_watch_request_for_price_drop_alert():
    data = parse_watch_request("맥북 에어 가격 내려가면 알려줘")
    assert data["notify_on_new"] is False
    assert data["notify_on_price_drop"] is True
    assert data["delivery_mode"] == "alert"


def test_parse_watch_request_for_daily_briefing():
    data = parse_watch_request("플스5 매일 아침 8시에 브리핑해줘")
    assert data["delivery_mode"] == "briefing"
    assert data["action"] == "brief"
    assert data["schedule"] == {
        "kind": "daily",
        "hour": 8,
        "minute": 0,
        "label": "매일 08:00",
        "cron": "0 8 * * *",
    }
    assert data["plan_hints"]["recommended_command"].endswith('--json')
    assert '--alerts-only' not in data["plan_hints"]["recommended_command"]


def test_build_integration_bundle_for_hourly_new_listing_watch():
    bundle = build_integration_bundle("아이폰 15 프로 신규 매물만 1시간마다 감시해줘")
    assert bundle["kind"] == "used-market-integration-plan"
    assert bundle["parsed_plan"]["schedule"]["cron"] == "0 */1 * * *"
    assert bundle["persist"]["command"].startswith("python skills/used-market-watch/scripts/used_market_watch.py watch-upsert")
    assert bundle["execution"]["recommended_command"].endswith('--alerts-only --json')
    assert bundle["execution"]["cron_payload"]["expr"] == "0 */1 * * *"
    assert bundle["execution"]["system_event"]["type"] == "used-market-watch-check"
    assert "설정하면 됩니다" in bundle["user_confirmation"]
