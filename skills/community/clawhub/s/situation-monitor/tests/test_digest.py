from pathlib import Path

from monitoring_the_situation.config import Settings
from monitoring_the_situation.digest import build_report
from monitoring_the_situation.fixtures import load_fixture_messages


def test_fixture_digest_places_api_alerts_in_urgent() -> None:
    messages = load_fixture_messages(
        Path("examples/demo_messages.json")
    )
    settings = Settings.from_env()
    report = build_report(messages, settings=settings, source="fixture:test")

    urgent_channels = [item.channel for item in report.urgent]
    assert "api-alerts" in urgent_channels


def test_fixture_digest_keeps_review_request_visible() -> None:
    messages = load_fixture_messages(
        Path("examples/demo_messages.json")
    )
    settings = Settings.from_env()
    report = build_report(messages, settings=settings, source="fixture:test")

    ask_channels = [item.channel for item in report.direct_asks]
    assert "design-review" in ask_channels


def test_fixture_digest_places_launch_channel_in_decisions() -> None:
    messages = load_fixture_messages(
        Path("examples/demo_messages.json")
    )
    settings = Settings.from_env()
    report = build_report(messages, settings=settings, source="fixture:test")

    decision_channels = [item.channel for item in report.decisions]
    assert "launch-war-room" in decision_channels
