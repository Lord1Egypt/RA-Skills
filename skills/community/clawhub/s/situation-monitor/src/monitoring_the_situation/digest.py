from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone

from .config import Settings
from .friendli import FriendliRefiner
from .models import BucketName, MessageRecord, SituationItem, SituationReport


SEVERE_URGENT_WORDS = {"broken", "incident", "outage", "rollback", "failing"}
URGENT_SIGNAL_WORDS = {"asap", "blocker", "blocked", "urgent"}
DECISION_WORDS = {"decision", "go", "no-go", "launch", "ship", "approve"}
DEADLINE_WORDS = {"today", "tonight", "eod", "eta", "deadline", "noon", "pm"}


def build_report(
    messages: list[MessageRecord], settings: Settings, source: str
) -> SituationReport:
    grouped: dict[str, list[MessageRecord]] = defaultdict(list)
    for message in sorted(messages, key=lambda item: item.created_at):
        grouped[message.channel].append(message)

    items = [
        _build_channel_item(channel, channel_messages)
        for channel, channel_messages in grouped.items()
    ]
    items.sort(key=lambda item: item.score, reverse=True)

    report = SituationReport(
        title="Situation Monitor Report",
        generated_at=datetime.now(timezone.utc),
        source=source,
        overview=_fallback_overview(items),
        urgent=[item for item in items if item.bucket == "urgent"],
        direct_asks=[item for item in items if item.bucket == "direct_asks"],
        decisions=[item for item in items if item.bucket == "decisions"],
        fyi=[item for item in items if item.bucket == "fyi"],
    )

    if settings.friendli_token and items:
        try:
            report.overview = FriendliRefiner(settings).rewrite_overview(
                _overview_seed(items)
            )
        except Exception:
            pass
    return report


def draft_reply_for_item(
    item: SituationItem, settings: Settings, tone: str = "calm"
) -> str:
    del tone
    if settings.friendli_token:
        try:
            return FriendliRefiner(settings).draft_reply(
                item.channel, item.summary, item.action_items
            )
        except Exception:
            pass
    action = item.action_items[0] if item.action_items else "I will take point."
    return (
        f"Monitoring the situation in #{item.channel}: {item.summary} "
        f"Next step: {action}"
    )


def _build_channel_item(
    channel: str, messages: list[MessageRecord]
) -> SituationItem:
    scores = {"urgent": 0, "direct_asks": 0, "decisions": 0, "fyi": 1}
    action_items: list[str] = []
    citations: list[str] = []

    for message in messages:
        lowered = message.content.lower()
        score_delta, bucket = _score_message(lowered)
        scores[bucket] += score_delta
        if score_delta > 0:
            citations.append(_citation(message))
        maybe_action = _extract_action(message.content)
        if maybe_action and maybe_action not in action_items:
            action_items.append(maybe_action)

    bucket = max(scores, key=scores.get)
    sorted_messages = sorted(messages, key=lambda item: item.created_at, reverse=True)
    newest = sorted_messages[0]
    summary = (
        f"{newest.author} reports: {_trim(newest.content)}"
        if len(messages) == 1
        else f"{len(messages)} recent messages. Latest update from {newest.author}: {_trim(newest.content)}"
    )

    if not citations:
        citations = [_citation(message) for message in sorted_messages[:2]]
    if not action_items and bucket == "urgent":
        action_items.append("Assign an owner and publish an ETA.")
    elif not action_items and bucket == "direct_asks":
        action_items.append("Respond to the ask and confirm who is handling it.")
    elif not action_items and bucket == "decisions":
        action_items.append("Name the decision owner and due time.")

    return SituationItem(
        channel=channel,
        bucket=bucket,  # type: ignore[arg-type]
        score=scores[bucket],
        summary=summary,
        action_items=action_items[:3],
        citations=citations[:3],
    )


def _score_message(lowered: str) -> tuple[int, BucketName]:
    severe_urgent_hits = sum(word in lowered for word in SEVERE_URGENT_WORDS)
    urgent_signal_hits = sum(word in lowered for word in URGENT_SIGNAL_WORDS)
    decision_hits = sum(word in lowered for word in DECISION_WORDS)
    deadline_hits = sum(word in lowered for word in DEADLINE_WORDS)
    explicit_ask_hits = int("?" in lowered) + int("can someone" in lowered)
    need_hits = int("we need" in lowered)

    if severe_urgent_hits or (urgent_signal_hits >= 2 and deadline_hits):
        return 5 + severe_urgent_hits + urgent_signal_hits + deadline_hits, "urgent"
    if explicit_ask_hits:
        return 4 + explicit_ask_hits + need_hits + deadline_hits, "direct_asks"
    if decision_hits or deadline_hits >= 2:
        return 3 + decision_hits + deadline_hits + need_hits, "decisions"
    if need_hits:
        return 4 + need_hits + deadline_hits, "direct_asks"
    return 1, "fyi"


def _extract_action(content: str) -> str | None:
    lowered = content.lower()
    if "eta" in lowered:
        return "Publish a concrete ETA."
    if "review" in lowered:
        return "Review the requested material and respond in-thread."
    if "decision" in lowered or "go or no-go" in lowered:
        return "Record the go/no-go owner and deadline."
    if "rollback" in lowered:
        return "Confirm rollback status before further merges."
    return None


def _citation(message: MessageRecord) -> str:
    timestamp = message.created_at.strftime("%H:%M")
    suffix = f" -> {message.jump_url}" if message.jump_url else ""
    return f"{message.channel}#{message.id} {timestamp}{suffix}"


def _trim(content: str, limit: int = 100) -> str:
    if len(content) <= limit:
        return content
    return content[: limit - 3].rstrip() + "..."


def _overview_seed(items: list[SituationItem]) -> str:
    lines = []
    for item in items[:5]:
        lines.append(
            f"{item.bucket.upper()} | #{item.channel} | {item.summary} | actions: {', '.join(item.action_items) or 'none'}"
        )
    return "\n".join(lines)


def _fallback_overview(items: list[SituationItem]) -> str:
    urgent = sum(item.bucket == "urgent" for item in items)
    asks = sum(item.bucket == "direct_asks" for item in items)
    decisions = sum(item.bucket == "decisions" for item in items)
    if not items:
        return "No recent Discord activity was found."
    return (
        f"{urgent} urgent thread(s), {asks} direct ask(s), and {decisions} decision lane(s) "
        f"need attention across {len(items)} channel(s)."
    )
