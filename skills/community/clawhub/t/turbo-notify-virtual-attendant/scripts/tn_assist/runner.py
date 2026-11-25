"""The unattended runner: poll without a model, wake a fresh process only when there is work.

It holds the API key in memory, uses it for the REST calls itself (events, message text, replies,
notices) and gives it to a child process only when that child is an administrator or attendant one.
A customer's turn runs in a process with no tools; the runner sends what comes out, after the checks
in :mod:`tn_assist.apply`.
"""

from __future__ import annotations

import http.client
import json
import os
import subprocess
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Protocol

from tn_assist import __version__
from tn_assist.apply import (
    Action,
    InvalidDecision,
    NotifyAdmins,
    NotifySelfChat,
    Say,
    Silent,
    due_reminders,
    report_failure,
)
from tn_assist.config import load_config
from tn_assist.deliver import expand, outbox_add, outbox_done, outbox_pending, outbox_update
from tn_assist.events import Event, parse_events
from tn_assist.i18n import Lang, t
from tn_assist.ingest import PAGE_LIMIT, CollectResult, collect_since, ingest
from tn_assist.langguess import guess_language
from tn_assist.memory import purge_expired, read_lines_at, set_text_at
from tn_assist.pack import build_pack
from tn_assist.paths import ContactKey, Workspace
from tn_assist.profiles import Child, Role, UnsupportedHarness, build_child
from tn_assist.queue import (
    WorkItem,
    complete,
    lease_next,
    mark_hydrated,
    mark_rejected,
    release_for_retry,
)
from tn_assist.state import ContactState, load_state
from tn_assist.store import WorkspaceLock, append_jsonl, read_json, read_jsonl, write_json_atomic
from tn_assist.threads import thread_path
from tn_assist.timeutil import parse_iso, utc_iso
from tn_assist.version import check as version_check
from tn_assist.version import fetch_latest
from tn_assist.workflow import apply_decision_text, run_console_item

EVENT_TYPES = ("message.received", "message.replied", "message.sent")
KINDS = ("contact", "admin", "attendant", "compaction")
MAX_ATTEMPTS = 5
#: An answer the helper refuses is asked for once more at the next cycle; the second refusal sends
#: the customer to a person (the rule of references/contact-turn.md, for the unattended runner too).
MAX_REJECTIONS = 2
NEXT_CYCLE_SECONDS = 1
RETRY_DELAY_SECONDS = 60
RETRY_BACKOFF = (
    5  # 1 min, 5 min, 25 min, then 2 h: a model outage must not hand everyone to a person
)
RETRY_DELAY_CAP_S = 7200
LEASE_SECONDS = 900


class ApiError(Exception):
    def __init__(self, status: int, code: str = "", retry_after: int | None = None) -> None:
        super().__init__(f"{status} {code}".strip())
        self.status, self.code, self.retry_after = status, code, retry_after


# What a refusal means. Pacing and daily limits are the platform's protection against bans: wait
# and try again. Quota and plan refusals do not heal by waiting: tell the administrators once.
PACING_CODES = frozenset(
    {"send_rate_spacing", "rate_limit_exceeded", "messages_per_minute_limit_exceeded",
     "refresh_rate_limited"}
)  # fmt: skip
DAILY_CODES = frozenset(
    {"warmup_limit_exceeded", "recipients_per_day_limit_exceeded", "duplicate_burst_blocked",
     "reply_ratio_too_low"}
)  # fmt: skip
QUOTA_CODES = frozenset(
    {"payment_required", "contact_quota_exceeded", "messages_quota_exceeded",
     "feature_not_available", "insufficient_scope"}
)  # fmt: skip
PACING_WAIT_CAP_S = 15
PACING_RETRIES = 3
HELD_DELAY_S = 3600
OUTBOX_MAX_AGE_S = 6 * 3600


def classify(error: ApiError) -> str:
    if error.status == 0 or error.status >= 500:
        return "transient"
    if error.code == "number_not_connected" or (
        error.status in (401, 403) and error.code != "insufficient_scope"
    ):
        # heals on its own (a reconnect) or when the key is fixed: hold the answer, do not erase it
        return "transient"
    if error.code in PACING_CODES:
        return "pacing"
    if error.code in DAILY_CODES:
        return "daily"
    if error.code in QUOTA_CODES or error.status in (402, 409):
        return "quota"
    if error.status == 429:
        return "pacing"  # a limit nobody named yet still heals by waiting: never erase the answer
    return "drop"


class Api(Protocol):
    def events(self, params: dict[str, str]) -> list[Event]: ...
    def message_text(self, number_ref: str, message_id: str) -> str | None: ...
    def send(
        self, number_ref: str, to: str, text: str, key: str, quote: str | None = None
    ) -> None: ...


class RestApi:
    """The Turbo Notify REST API. The only place the runner uses the key."""

    def __init__(self, base: str, key: str, number_id: str, *, timeout: float = 20.0) -> None:
        self._base = base.rstrip("/")
        self._key = key
        self._number_id = number_id
        self._timeout = timeout

    def _call(
        self, method: str, path: str, body: dict[str, Any] | None = None, key: str | None = None
    ) -> Any:
        headers = {"Authorization": f"Bearer {self._key}", "Accept": "application/json"}
        data = None
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        if key:
            headers["Idempotency-Key"] = key
        request = urllib.request.Request(
            self._base + path, data=data, method=method, headers=headers
        )
        try:
            with urllib.request.urlopen(request, timeout=self._timeout) as response:  # noqa: S310
                raw = response.read()
        except urllib.error.HTTPError as error:
            retry_after: int | None = None
            header = error.headers.get("Retry-After") if error.headers else None
            if header and header.strip().isdigit():
                retry_after = int(header.strip())
            code = ""
            try:
                payload = json.loads(error.read() or b"{}")
                code = str(payload.get("error", "")) if isinstance(payload, dict) else ""
            except ValueError:
                pass
            raise ApiError(error.code, code, retry_after) from error
        except (urllib.error.URLError, TimeoutError, OSError, http.client.HTTPException) as error:
            raise ApiError(0, "network") from error
        try:
            return json.loads(raw) if raw else {}
        except ValueError as error:
            raise ApiError(0, "bad_response") from error

    def events(self, params: dict[str, str]) -> list[Event]:
        query = [("types[]", kind) for kind in EVENT_TYPES] + [("number_id", self._number_id)]
        query += list(params.items())
        payload = self._call("GET", "/v1/events?" + urllib.parse.urlencode(query))
        return parse_events(payload)

    def message_text(self, number_ref: str, message_id: str) -> str | None:
        try:
            data = self._call("GET", f"/v1/numbers/{number_ref}/messages/{message_id}")
        except ApiError as error:
            if error.status == 404:
                return None
            raise
        if not isinstance(data, dict) or data.get("content_expired"):
            return None
        for field_name in ("text",):
            if isinstance(data.get(field_name), str) and data[field_name].strip():
                return str(data[field_name])
        for media in ("image", "video", "document"):
            block = data.get(media)
            if isinstance(block, dict) and isinstance(block.get("caption"), str):
                return str(block["caption"])
        audio = data.get("audio")
        if isinstance(audio, dict):
            transcription = audio.get("transcription")
            if isinstance(transcription, dict) and isinstance(transcription.get("text"), str):
                return str(transcription["text"])
        return ""

    def send(self, number_ref: str, to: str, text: str, key: str, quote: str | None = None) -> None:
        body: dict[str, Any] = {"to": {"number": "+" + to}, "content": {"text": text}}
        if quote:
            body["quoted_message_id"] = quote
        self._call("POST", f"/v1/numbers/{number_ref}/messages", body, key)


class ChildFailed(Exception):
    pass


Spawn = Callable[[Child], str]


def run_child(child: Child, timeout: float = 600.0) -> str:
    try:
        done = subprocess.run(  # noqa: S603
            child.argv,
            input=child.stdin,
            env=child.env,
            cwd=str(child.cwd),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise ChildFailed(type(error).__name__) from error
    if done.returncode != 0:
        raise ChildFailed(f"exit {done.returncode}")
    if child.output_file is not None and child.output_file.exists():
        return child.output_file.read_text(encoding="utf-8")
    return done.stdout


@dataclass
class RunnerConfig:
    workspace: Workspace
    harness: str
    api_key: str = field(repr=False, default="")
    api_base: str = "https://api.turbonotify.com"
    mcp_url: str = "https://mcp.turbonotify.com"
    interval_s: int = 20
    model: str | None = None
    env: Mapping[str, str] = field(default_factory=lambda: dict(os.environ))


@dataclass
class CycleReport:
    busy: bool = False
    primed: bool = False
    ingested: int = 0
    processed: int = 0
    failed: int = 0
    sent: int = 0
    children: int = 0
    silenced: int = 0  # customers who only closed the conversation: handled, nothing to send


def _log(ws: Workspace, event: str, **fields: Any) -> None:
    """Event names, ids and counts only: never message text, never a number, never a credential."""
    safe = {k: v for k, v in fields.items() if isinstance(v, (int, str, bool)) and k != "text"}
    append_jsonl(
        ws.path("logs", "runner.jsonl"),
        {"at": utc_iso(datetime.now(timezone.utc)), "event": event, **safe},
    )


def check_harness(harness: str) -> None:
    if harness not in ("claude-code", "codex"):
        raise UnsupportedHarness(harness)


Sleep = Callable[[float], None]


def _attempt(api: Api, number_ref: str, op: dict[str, Any]) -> None:
    api.send(number_ref, op["to"], op["text"], op["idempotency_key"], op.get("quote"))


def _execute(
    cfg: RunnerConfig,
    api: Api,
    now: datetime,
    report: CycleReport,
    sleep: Sleep = time.sleep,
    beat: Callable[[], None] = lambda: None,
) -> int:
    """Try every delivery that is due. Returns how many were refused for good (a notice follows)."""
    ws = cfg.workspace
    refused = 0
    for op in outbox_pending(ws):
        beat()  # a long outbox with pauses must not let another runner take the lock
        if not op.get("to") or not op.get("text"):
            outbox_done(ws, op)  # a delivery written by an older version: nothing sensible to send
            _log(ws, "delivery_discarded", reason="old_format")
            continue
        hold = op.get("not_before")
        if hold and parse_iso(hold) > now:
            continue
        waited = 0
        while True:
            try:
                _attempt(api, ws.num_id, op)
            except ApiError as error:
                kind = classify(error)
                if kind == "pacing" and waited < PACING_RETRIES:
                    pause = error.retry_after if error.retry_after is not None else 2
                    sleep(min(pause, PACING_WAIT_CAP_S) + 0.3)
                    waited += 1
                    continue
                if kind in ("transient", "pacing", "daily"):
                    delay = error.retry_after if error.retry_after else HELD_DELAY_S
                    delay = delay if kind == "daily" else min(max(delay, 30), 300)
                    queued = parse_iso(op["queued_at"]) if op.get("queued_at") else now
                    if (now - queued).total_seconds() > OUTBOX_MAX_AGE_S:
                        outbox_done(ws, op)
                        _log(ws, "delivery_expired", status=error.status, code=error.code)
                    else:
                        outbox_update(
                            ws,
                            op,
                            not_before=utc_iso(now + timedelta(seconds=delay)),
                            attempts=int(op.get("attempts", 0)) + 1,
                        )
                        _log(ws, "delivery_held", status=error.status, code=error.code, kind=kind)
                    if error.status in (401, 403):
                        cause = error.code or str(error.status)
                        notices = report_failure(ws, cause, now.strftime("%Y-%m"), now)
                        outbox_add(ws, expand(ws, notices, seed=f"failure-{cause}"), now=now)
                    break
                if kind == "drop" and op.get("quote"):
                    # a quote the API cannot use must not cost the customer their answer
                    op = {**op, "quote": None}
                    outbox_update(ws, op, quote=None)
                    _log(ws, "quote_dropped", status=error.status, code=error.code)
                    continue
                outbox_done(ws, op)
                _log(ws, "delivery_refused", status=error.status, code=error.code)
                if kind == "quota":
                    refused += 1
                    cause = error.code or str(error.status)
                    notices = report_failure(ws, cause, now.strftime("%Y-%m"), now)
                    outbox_add(ws, expand(ws, notices, seed=f"failure-{cause}"), now=now)
                break
            outbox_done(ws, op)
            report.sent += 1
            break
    return refused


def _hydrate(cfg: RunnerConfig, api: Api, item: WorkItem) -> None:
    ws = cfg.workspace
    lines = {ln.event_id: ln for ln in read_lines_at(thread_path(ws, item.kind, item.contact))}
    for event_id in item.event_ids:
        if event_id in item.hydrated_ids:
            continue
        line = lines.get(event_id)
        message_id = line.message_id if line else None
        text: str | None = None
        if message_id:
            text = api.message_text(ws.num_id, message_id)  # None only when the message is gone
        set_text_at(thread_path(ws, item.kind, item.contact), event_id, text)
        mark_hydrated(ws, item.id, event_id)


def _role(item: WorkItem) -> Role:
    return item.kind


def _decide(
    cfg: RunnerConfig, item: WorkItem, spawn: Spawn, now: datetime, report: CycleReport
) -> str:
    ws = cfg.workspace
    pack = build_pack(ws, item, now=now)
    with tempfile.TemporaryDirectory(prefix="tn-assist-") as scratch:
        child = build_child(
            cfg.harness,
            _role(item),
            pack.text,
            scratch=Path(scratch),
            mcp_url=cfg.mcp_url,
            key=cfg.api_key or None,
            base_env=cfg.env,
            model=cfg.model,
        )
        report.children += 1
        return spawn(child)


def _answerable(ws: Workspace, item: WorkItem) -> bool:
    assert item.contact is not None
    state = load_state(ws, ContactKey.parse(item.contact)).state
    return state is ContactState.ACTIVE and not load_config(ws).get("paused")


def _process(
    cfg: RunnerConfig, api: Api, item: WorkItem, spawn: Spawn, now: datetime, report: CycleReport
) -> None:
    ws = cfg.workspace
    if item.kind == "contact" and not _answerable(ws, item):
        complete(ws, item.id)  # paused, handed off or opted out: no model, no reply
        return
    if item.kind in ("contact", "admin", "attendant"):
        _hydrate(cfg, api, item)  # a compaction works on text that is already stored
    actions: list[Action] = []
    if item.kind in ("admin", "attendant"):
        outcome = run_console_item(ws, item, now)
        if outcome.actions:
            # the commands already ran and are marked handled: their answers are kept now, so a
            # failing model step later cannot lose them
            outbox_add(ws, expand(ws, outcome.actions, seed=item.id), now=now)
        if outcome.needs_model:
            raw = _decide(cfg, item, spawn, now, report)
            actions += apply_decision_text(ws, item, raw, now)
    else:
        raw = _decide(cfg, item, spawn, now, report)
        actions += apply_decision_text(ws, item, raw, now)
    if any(isinstance(action, Silent) for action in actions):
        report.silenced += 1
        _log(ws, "contact_silenced", kind=item.kind)
    if actions:
        outbox_add(ws, expand(ws, actions, seed=item.id), now=now)


def _written_in(ws: Workspace, item: WorkItem) -> str | None:
    """The language the customer's new messages are written in, when it is clear from the words."""
    if not item.contact:
        return None
    wanted = set(item.event_ids)
    lines = read_lines_at(thread_path(ws, "contact", item.contact))
    return guess_language(" ".join(line.text for line in lines if line.event_id in wanted))


def _hand_over(
    cfg: RunnerConfig, item: WorkItem, now: datetime, reason: str, *, tell: bool
) -> None:
    """Stop trying. A customer goes to a person, with the same hand-off a reply of null gets: one
    message in their language, a notice to the people, the assistant silent until someone resumes.
    ``tell`` also answers an administrator or an attendant who would otherwise hear nothing."""
    ws = cfg.workspace
    if item.kind == "contact":
        decision: dict[str, Any] = {
            "escalate": {"reason": reason, "summary": "", "urgency": "normal"}
        }
        # no answer of the model told the helper what this customer speaks: read it from their words
        spoken = _written_in(ws, item)
        if spoken:
            decision["language"] = spoken
        try:
            actions = apply_decision_text(ws, item, json.dumps(decision), now)
            outbox_add(ws, expand(ws, actions, seed=item.id), now=now)
        except InvalidDecision:
            complete(ws, item.id)
        return
    if tell and item.kind in ("admin", "attendant"):
        lang: Lang = "en" if load_config(ws).get("lang") == "en" else "pt"
        to = (item.contact or "self") if item.kind == "admin" else "self"
        outbox_add(ws, expand(ws, [Say(to, t("console_unreadable", lang))], seed=item.id), now=now)
    complete(ws, item.id)


def _give_up(cfg: RunnerConfig, item: WorkItem, now: datetime) -> None:
    """An item that keeps failing to run is handed to a person instead of looping forever."""
    _hand_over(cfg, item, now, "automatic answer failed", tell=False)


def _refused(cfg: RunnerConfig, item: WorkItem, now: datetime, error: InvalidDecision) -> None:
    """The model answered and the helper refused the answer (not an outage).

    It is asked once more at the next cycle, without the pause an outage gets: a customer must not
    wait half an hour, and the messages behind this one must not either. A second refusal in a row
    means the model cannot answer this one, so the customer goes to a person at once.
    """
    ws = cfg.workspace
    refused = mark_rejected(ws, item.id, str(error))
    _log(
        ws, "item_rejected", kind=item.kind, error="InvalidDecision", detail=str(error)[:200],
        rejected=refused, attempts=item.attempts,
    )  # fmt: skip
    if refused < MAX_REJECTIONS:
        release_for_retry(ws, item.id, now, NEXT_CYCLE_SECONDS)
        return
    lang: Lang = "en" if load_config(ws).get("lang") == "en" else "pt"
    _hand_over(cfg, item, now, t("reason_decision_unreadable", lang), tell=True)


def run_cycle(
    cfg: RunnerConfig,
    api: Api,
    *,
    spawn: Spawn = run_child,
    now: datetime | None = None,
    fetch_version: Callable[[], Any] | None = fetch_latest,
    sleep: Sleep = time.sleep,
) -> CycleReport:
    check_harness(cfg.harness)
    ws = cfg.workspace
    now = now or datetime.now(timezone.utc)
    report = CycleReport()
    lock = WorkspaceLock(ws.path("runner.lock"))
    if not lock.acquire(ttl_s=LEASE_SECONDS):
        report.busy = True
        return report
    try:
        _execute(cfg, api, now, report, sleep, lock.heartbeat)
        cursor_state = read_json(ws.path("cursor.json"), {})
        cursor = cursor_state.get("last_event_id") if isinstance(cursor_state, dict) else None
        primed_at = cursor_state.get("primed_at") if isinstance(cursor_state, dict) else None
        if cursor is None and primed_at:
            # started on an empty account: whatever arrived since then is new, not history
            page = api.events({"limit": str(PAGE_LIMIT)})
            found = CollectResult(
                [e for e in page if e.created_at >= str(primed_at)], page[0].id if page else None
            )
            cursor = "primed"  # the stream is now followed; ingest writes the real cursor
        else:
            found = collect_since(api.events, cursor)
        if cursor is None:
            write_json_atomic(
                ws.path("cursor.json"),
                {
                    "last_event_id": found.newest_id,
                    "last_tick_at": utc_iso(now),
                    **({} if found.newest_id else {"primed_at": utc_iso(now)}),
                },
            )
            report.primed = True
            return report
        result = ingest(ws, found.events, now)
        report.ingested = len(found.events)
        lock.heartbeat()
        notices: list[Action] = []
        lang: Lang = "en" if load_config(ws).get("lang") == "en" else "pt"
        if result.gap_alarm:
            gaps = read_jsonl(ws.path("gaps.jsonl"))
            last = gaps[-1] if gaps else {"from": "?", "to": utc_iso(now)}
            text = t("gap_notice", lang, start=last["from"], end=last["to"])
            notices += [NotifyAdmins(text), NotifySelfChat(text)]
        if result.first_foreign:
            notices.append(NotifyAdmins(t("foreign_notice", lang)))
        if notices:
            outbox_add(ws, expand(ws, notices, seed=f"ingest-{utc_iso(now)}"), now=now)
        while True:
            item = lease_next(ws, KINDS, ttl_s=LEASE_SECONDS, now=now)
            if item is None:
                break
            if item.attempts > MAX_ATTEMPTS:
                _give_up(cfg, item, now)
                report.failed += 1
                continue
            try:
                _process(cfg, api, item, spawn, now, report)
                report.processed += 1
            except InvalidDecision as error:
                report.failed += 1
                _refused(cfg, item, now, error)
            except (ChildFailed, ApiError) as error:
                report.failed += 1
                _log(
                    ws,
                    "item_failed",
                    kind=item.kind,
                    error=type(error).__name__,
                    attempts=item.attempts,
                )
                delay = min(
                    RETRY_DELAY_SECONDS * RETRY_BACKOFF ** max(0, item.attempts - 1),
                    RETRY_DELAY_CAP_S,
                )
                release_for_retry(ws, item.id, now, delay)
            lock.heartbeat()
        reminders = due_reminders(ws, now)
        if reminders:
            outbox_add(ws, expand(ws, reminders, seed=f"reminder-{utc_iso(now)[:13]}"), now=now)
        config = load_config(ws)
        notice = version_check(
            ws, __version__, fetch_version, now, harness=config.get("harness"), lang=lang
        )
        if notice is not None:
            announced = read_json(ws.path("update-announced.json"), {})
            if not isinstance(announced, dict) or announced.get("version") != notice.latest:
                write_json_atomic(ws.path("update-announced.json"), {"version": notice.latest})
                outbox_add(
                    ws,
                    expand(ws, [NotifyAdmins(notice.text(lang))], seed=f"update-{notice.latest}"),
                    now=now,
                )
        purge_state = read_json(ws.path("purged.json"), {})
        last_purge = purge_state.get("at") if isinstance(purge_state, dict) else None
        if not last_purge or (now - parse_iso(last_purge)).total_seconds() > 86_400:
            purge_expired(ws, now)
            write_json_atomic(ws.path("purged.json"), {"at": utc_iso(now)})
        if _execute(cfg, api, now, report, sleep):
            _execute(cfg, api, now, report, sleep)  # a refusal queued a notice; send it now
        _log(
            ws,
            "cycle",
            ingested=report.ingested,
            processed=report.processed,
            failed=report.failed,
            children=report.children,
            silenced=report.silenced,
        )
        return report
    finally:
        lock.release()


def run_forever(cfg: RunnerConfig, api: Api, *, once: bool = False) -> None:
    while True:
        try:
            run_cycle(cfg, api)
        except (ApiError, OSError, ValueError, http.client.HTTPException) as error:
            if once:
                raise
            # a sleeping laptop, a 502 or a bad body must not end the attendant: log and try again
            _log(cfg.workspace, "cycle_failed", error=type(error).__name__)
        if once:
            return
        time.sleep(max(5, min(cfg.interval_s, 600)))
