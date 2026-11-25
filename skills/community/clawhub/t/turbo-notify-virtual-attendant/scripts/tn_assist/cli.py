"""The command line the agent and the configurator use. Every command prints one JSON object.

``{"ok": true, ...}`` on success, ``{"ok": false, "error": code, "message": text}`` otherwise, with
exit code 0, 1 (refused) or 2 (needs a confirmation). The helper holds no credential and calls no
model; the agent fetches events, reads the pack, writes a decision, and carries out the deliveries.
"""

from __future__ import annotations

import argparse
import contextlib
import dataclasses
import json
import os
import sys
from collections.abc import Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import IO, Any

from tn_assist import __version__
from tn_assist.admins import (
    AdminError,
    ConnectedNumberNeedsConfirmation,
    Registry,
)
from tn_assist.apply import (
    Action,
    InvalidDecision,
    NotifyAdmins,
    NotifySelfChat,
    Silent,
    due_reminders,
    report_failure,
)
from tn_assist.config import SCHEMA_VERSION, load_config, save_config
from tn_assist.console import forget_contact, queue_entries
from tn_assist.deliver import expand
from tn_assist.events import Event, parse_events
from tn_assist.i18n import Lang, t
from tn_assist.ingest import fetch_plan, ingest
from tn_assist.knowledge import InvalidKnowledgePath, seed_defaults, write_knowledge
from tn_assist.memory import (
    Card,
    Policy,
    episodes,
    purge_expired,
    read_lines_at,
    set_text_at,
)
from tn_assist.pack import build_pack
from tn_assist.paths import ContactKey, InvalidContactKey, InvalidWorkspaceId, Workspace
from tn_assist.queue import (
    WorkItem,
    complete,
    get_leased,
    lease_next,
    mark_hydrated,
    mark_rejected,
    pending_count,
)
from tn_assist.schema import MigrationFailed, WorkspaceTooNew, migrate
from tn_assist.sources import (
    NeedsConfirmation,
    SourceClass,
    SourceRegistry,
    WriteToolError,
)
from tn_assist.state import load_state
from tn_assist.store import read_json, read_jsonl, write_json_atomic
from tn_assist.threads import thread_path
from tn_assist.timeutil import parse_iso, utc_iso
from tn_assist.version import check as version_check
from tn_assist.version import fetch_latest
from tn_assist.workflow import apply_decision_text, run_console_item

_LEASE_SECONDS = 900


class CliError(Exception):
    def __init__(self, error: str, message: str = "", code: int = 1, **extra: Any) -> None:
        super().__init__(message or error)
        self.error, self.message, self.code, self.extra = error, message or error, code, extra


def _lang(ws: Workspace) -> Lang:
    return "en" if load_config(ws).get("lang") == "en" else "pt"


def _now(args: argparse.Namespace) -> datetime:
    return parse_iso(args.now) if getattr(args, "now", None) else datetime.now(timezone.utc)


def _events_from_files(paths: Sequence[str]) -> list[Event]:
    seen: set[str] = set()
    events: list[Event] = []
    for path in paths:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        for event in parse_events(payload):
            if event.id not in seen:
                seen.add(event.id)
                events.append(event)
    return events


def _item_json(ws: Workspace, item: WorkItem) -> dict[str, Any]:
    lines = (
        read_lines_at(thread_path(ws, item.kind, item.contact))
        if item.kind
        in (
            "contact",
            "admin",
            "attendant",
        )
        else []
    )
    by_event = {ln.event_id: ln for ln in lines}
    hydrate = (
        [e for e in item.event_ids if e not in item.hydrated_ids]
        if item.kind in ("contact", "admin", "attendant")
        else []
    )
    # the same order as ``hydrate``, one entry each (null when the line has no message id)
    message_ids = [by_event[e].message_id if e in by_event else None for e in hydrate]
    return {
        "id": item.id,
        "kind": item.kind,
        "contact": item.contact,
        "event_ids": list(item.event_ids),
        "hydrate": hydrate,
        "message_ids": message_ids,
        "number_ref": ws.num_id,
    }


def _deliveries(ws: Workspace, actions: list[Action], seed: str) -> list[dict[str, Any]]:
    return expand(ws, actions, seed=seed)


# --- workspace setup --------------------------------------------------------------------


def cmd_init(ws_args: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    base, org, number = ws_args["base"], ws_args["org"], ws_args["number"]
    now = _now(args)
    try:
        existing = (Path(base) / org / number).is_dir() and (
            Path(base) / org / number / "config.json"
        ).exists()
        ws = Workspace.open(Path(base), org, number, create=True)
    except InvalidWorkspaceId as error:
        raise CliError("invalid_workspace", str(error)) from error
    registry = Registry.load(ws)
    if not existing:
        save_config(
            ws,
            {
                "schema": SCHEMA_VERSION,
                "bound_number_id": number,
                "connected_number": str(ContactKey.parse(args.connected)),
                "business_name": args.business,
                "lang": args.lang,
                "mode": "assist",
                "paused": False,
                "harness": args.harness,
                "created_at": utc_iso(now),
            },
        )
        seed_defaults(ws, args.lang)
        policy_path = ws.path("memory-policy.json")
        if not policy_path.exists():  # the numbers a person may edit; a copy already there is kept
            write_json_atomic(policy_path, dataclasses.asdict(Policy()))
    try:
        key = ContactKey.parse(args.admin)
        registry.add(
            str(key),
            args.admin_name,
            by="configurator",
            via="configurator",
            confirmed_connected=args.confirm_connected,
            now=now,
        )
    except InvalidContactKey as error:
        raise CliError("invalid_number", "the administrator number is not valid") from error
    except ConnectedNumberNeedsConfirmation as error:
        raise CliError(
            "connected_number_needs_confirmation",
            "confirm the warning first",
            code=2,
            warning=t("connected_number_warning", args.lang),
        ) from error
    return {"existing": existing, "workspace": str(ws.root)}


def cmd_cursor(ws: Workspace, args: argparse.Namespace) -> dict[str, Any]:
    state = read_json(ws.path("cursor.json"), {})
    state = state if isinstance(state, dict) else {}
    if args.set or args.from_page:
        newest = args.set
        if args.from_page:
            events = _events_from_files([args.from_page])
            newest = events[0].id if events else None
        if not newest:
            raise CliError("empty_page", "the page has no events to start from")
        state["last_event_id"] = newest
        state.setdefault("last_tick_at", utc_iso(_now(args)))
        write_json_atomic(ws.path("cursor.json"), state)
    cursor = state.get("last_event_id")
    plan = fetch_plan([], cursor)
    return {"cursor": cursor, "params": plan.params}


def cmd_fetch_plan(ws: Workspace, args: argparse.Namespace) -> dict[str, Any]:
    state = read_json(ws.path("cursor.json"), {})
    cursor = state.get("last_event_id") if isinstance(state, dict) else None
    pages = [parse_events(json.loads(Path(p).read_text(encoding="utf-8"))) for p in args.page]
    plan = fetch_plan(pages, cursor)
    return {"done": plan.done, "params": plan.params, "truncated": plan.truncated}


def cmd_ingest(ws: Workspace, args: argparse.Namespace) -> dict[str, Any]:
    now = _now(args)
    result = ingest(ws, _events_from_files(args.file), now)
    lang = _lang(ws)
    notices: list[Action] = []
    if result.gap_alarm:
        gaps = read_jsonl(ws.path("gaps.jsonl"))
        last = gaps[-1] if gaps else {"from": "?", "to": utc_iso(now)}
        text = t("gap_notice", lang, start=last["from"], end=last["to"])
        notices += [NotifyAdmins(text), NotifySelfChat(text)]
    if result.first_foreign:
        notices.append(NotifyAdmins(t("foreign_notice", lang)))
    return {
        "items": [_item_json(ws, i) for i in result.items],
        "dropped": result.dropped,
        "new_cursor": result.new_cursor,
        "gap_alarm": result.gap_alarm,
        "deliveries": _deliveries(ws, notices, f"ingest-{utc_iso(now)}") if notices else [],
    }


# --- the work loop ----------------------------------------------------------------------


def cmd_next(ws: Workspace, args: argparse.Namespace) -> dict[str, Any]:
    kinds = tuple(k for k in args.kinds.split(",") if k)
    item = lease_next(ws, kinds, ttl_s=args.ttl, now=_now(args))
    return {"item": _item_json(ws, item) if item else None}


def cmd_next_status(ws: Workspace, args: argparse.Namespace) -> dict[str, Any]:
    item = get_leased(ws, args.item)
    if item is None:
        return {"leased": False, "hydrate": []}
    return {"leased": True, **{k: v for k, v in _item_json(ws, item).items() if k in ("hydrate",)}}


def cmd_set_text(ws: Workspace, args: argparse.Namespace) -> dict[str, Any]:
    item = get_leased(ws, args.item)
    if item is None:
        raise CliError("unknown_item", "the item is not leased")
    text = None if args.unreadable else Path(args.file).read_text(encoding="utf-8")
    set_text_at(thread_path(ws, item.kind, item.contact), args.event, text)
    mark_hydrated(ws, item.id, args.event)
    return {"event": args.event}


def cmd_pack(ws: Workspace, args: argparse.Namespace) -> dict[str, Any]:
    item = get_leased(ws, args.item)
    if item is None:
        raise CliError("unknown_item", "the item is not leased")
    about = ContactKey.parse(args.about) if args.about else None
    pack = build_pack(ws, item, now=_now(args), about=about)
    return {"pack": pack.text, "tokens": pack.tokens, "sources": list(pack.sources)}


def cmd_apply(ws: Workspace, args: argparse.Namespace) -> dict[str, Any]:
    item = get_leased(ws, args.item)
    if item is None:
        raise CliError("unknown_item", "the item is not leased")
    now = _now(args)
    if args.escalate:
        if item.kind != "contact":
            raise CliError("invalid_decision", "only a customer turn can be handed to a person")
        raw = json.dumps(
            {"escalate": {"reason": args.escalate[:300], "summary": "", "urgency": "normal"}}
        )
    else:
        raw = Path(args.decision_file).read_text(encoding="utf-8")
    try:
        actions = apply_decision_text(ws, item, raw, now)
    except InvalidDecision as error:
        # the next `pack` for this item ends with one line saying which rule the answer broke
        mark_rejected(ws, item.id, str(error))
        raise CliError("invalid_decision", str(error)) from error
    return {
        "deliveries": _deliveries(ws, actions, item.id),
        # a customer who only closed the conversation: handled, and nothing to send
        "silent": any(isinstance(action, Silent) for action in actions),
    }


def cmd_run_console(ws: Workspace, args: argparse.Namespace) -> dict[str, Any]:
    item = get_leased(ws, args.item)
    if item is None or item.kind not in ("admin", "attendant"):
        raise CliError("unknown_item", "not a console item")
    outcome = run_console_item(ws, item, _now(args))
    return {
        "needs_model": outcome.needs_model,
        "deliveries": _deliveries(ws, outcome.actions, item.id),
    }


def cmd_complete(ws: Workspace, args: argparse.Namespace) -> dict[str, Any]:
    complete(ws, args.item)
    return {}


def cmd_reminders(ws: Workspace, args: argparse.Namespace) -> dict[str, Any]:
    now = _now(args)
    return {"deliveries": _deliveries(ws, due_reminders(ws, now), f"reminder-{utc_iso(now)[:13]}")}


def cmd_report_failure(ws: Workspace, args: argparse.Namespace) -> dict[str, Any]:
    now = _now(args)
    actions = report_failure(ws, args.cause, args.cycle, now)
    return {"deliveries": _deliveries(ws, actions, f"failure-{args.cause}-{args.cycle}")}


def cmd_status(ws: Workspace, args: argparse.Namespace) -> dict[str, Any]:
    config = load_config(ws)
    cursor = read_json(ws.path("cursor.json"), {})
    return {
        "mode": config.get("mode"),
        "paused": bool(config.get("paused")),
        "lang": config.get("lang"),
        "pending": pending_count(ws),
        "waiting_for_a_person": len(queue_entries(ws)),
        "last_tick_at": cursor.get("last_tick_at") if isinstance(cursor, dict) else None,
        "version": __version__,
        "schema": config.get("schema"),
        "connected_is_admin": Registry.load(ws).connected_is_admin(),
    }


# --- configurator tools -----------------------------------------------------------------


def cmd_admin(ws: Workspace, args: argparse.Namespace) -> dict[str, Any]:
    registry = Registry.load(ws)
    now = _now(args)
    try:
        if args.action == "list":
            pass
        elif args.action == "add":
            registry.add(
                args.number,
                args.name,
                by="configurator",
                via="configurator",
                confirmed_connected=args.confirm_connected,
                now=now,
            )
        else:
            registry.remove(args.number, by="configurator", now=now)
    except ConnectedNumberNeedsConfirmation as error:
        raise CliError(
            "connected_number_needs_confirmation",
            "confirm the warning first",
            code=2,
            warning=t("connected_number_warning", _lang(ws)),
        ) from error
    except (AdminError, InvalidContactKey) as error:
        raise CliError("refused", str(error)) from error
    reloaded = Registry.load(ws)
    return {
        "admins": sorted(reloaded.numbers()),
        "connected_is_admin": reloaded.connected_is_admin(),
    }


def cmd_source(ws: Workspace, args: argparse.Namespace) -> dict[str, Any]:
    registry = SourceRegistry.load(ws)
    if args.action == "discover":
        registry.discovered([n for n in args.names.split(",") if n])
    elif args.action == "classify":
        try:
            registry.classify(
                args.name,
                SourceClass(args.cls.replace("-", "_")),
                mode=args.mode,
                live_tools=tuple(x for x in args.live_tools.split(",") if x),
                personal=args.personal,
                confirmed=args.confirmed,
            )
        except NeedsConfirmation as error:
            raise CliError(
                "needs_confirmation", "this widens access; confirm it", code=2
            ) from error
        except WriteToolError as error:
            raise CliError("write_tool", "that tool changes data and cannot be allowed") from error
        except KeyError as error:
            raise CliError("unknown_source", args.name) from error
    elif args.action == "marker":
        registry.add_marker(args.name, args.marker)
    reloaded = SourceRegistry.load(ws)
    return {
        "sources": [
            {
                "name": s.name,
                "cls": s.cls.value,
                "mode": s.mode,
                "personal": s.personal,
                "live_tools": list(s.live_tools),
            }
            for s in reloaded.all()
        ]
    }


def cmd_kb_write(ws: Workspace, args: argparse.Namespace) -> dict[str, Any]:
    text = Path(args.from_file).read_text(encoding="utf-8")
    try:
        path = write_knowledge(
            ws, args.path, text, visibility=args.visibility, description=args.description
        )
    except InvalidKnowledgePath as error:
        raise CliError("invalid_path", "use a plain .md file name") from error
    return {"path": path}


def cmd_set(ws: Workspace, args: argparse.Namespace) -> dict[str, Any]:
    config = load_config(ws)
    config[args.setting] = args.value
    save_config(ws, config)
    return {args.setting: args.value}


def cmd_version_check(ws: Workspace, args: argparse.Namespace) -> dict[str, Any]:
    config = load_config(ws)
    fetch = (lambda: json.loads(args.latest_json)) if args.latest_json else fetch_latest
    notice = version_check(
        ws, __version__, fetch, _now(args), harness=config.get("harness"), lang=_lang(ws)
    )
    out: dict[str, Any] = {"installed": __version__, "update": None, "deliveries": []}
    if notice is not None:
        out["update"] = {
            "installed": notice.installed,
            "latest": notice.latest,
            "command": notice.command,
            "notes_url": notice.notes_url,
            "min_workspace_schema": notice.min_workspace_schema,
        }
        announced = read_json(ws.path("update-announced.json"), {})
        if args.announce and (
            not isinstance(announced, dict) or announced.get("version") != notice.latest
        ):
            write_json_atomic(ws.path("update-announced.json"), {"version": notice.latest})
            out["deliveries"] = _deliveries(
                ws, [NotifyAdmins(notice.text(_lang(ws)))], f"update-{notice.latest}"
            )
    return out


def cmd_migrate(ws: Workspace, args: argparse.Namespace) -> dict[str, Any]:
    try:
        report = migrate(ws, now=_now(args))
    except WorkspaceTooNew as error:
        raise CliError("workspace_too_new", str(error)) from error
    except MigrationFailed as error:
        raise CliError("migration_failed", str(error)) from error
    return {
        "from": report.from_version,
        "to": report.to_version,
        "backup": str(report.backup) if report.backup else None,
    }


def cmd_export(ws: Workspace, args: argparse.Namespace) -> dict[str, Any]:
    key = ContactKey.parse(args.contact)
    directory = ws.contact_dir(key)
    if not directory.is_dir():
        raise CliError("not_found", "no data for that contact")
    return {
        "contact": str(key),
        "state": load_state(ws, key).to_json(),
        "card": [vars(f) for f in Card.load(ws, key).facts()],
        "transcript": read_jsonl(directory / "transcript.jsonl"),
        "episodes": [p.read_text(encoding="utf-8") for p in episodes(ws, key)],
    }


def cmd_forget(ws: Workspace, args: argparse.Namespace) -> dict[str, Any]:
    forget_contact(ws, ContactKey.parse(args.contact), "configurator", _now(args))
    return {}


def cmd_run(ws: Workspace, args: argparse.Namespace) -> dict[str, Any]:
    from tn_assist.profiles import KEY_ENV
    from tn_assist.runner import RestApi, RunnerConfig, run_forever

    key = os.environ.get(KEY_ENV, "")
    if not key:
        raise CliError("no_key", f"set {KEY_ENV} in the environment of the runner")
    cfg = RunnerConfig(
        workspace=ws,
        harness=args.harness,
        api_key=key,
        api_base=os.environ.get("TURBO_NOTIFY_API_URL", "https://api.turbonotify.com"),
        mcp_url=os.environ.get("TURBO_NOTIFY_MCP_URL", "https://mcp.turbonotify.com"),
        interval_s=args.interval,
        model=args.model,
    )
    api = RestApi(cfg.api_base, key, ws.num_id)
    cmd_migrate(
        ws, args
    )  # a new version may need a newer folder layout; refuses a folder from a newer one
    with contextlib.suppress(KeyboardInterrupt):
        run_forever(cfg, api, once=args.once)
    return {"stopped": True}


def cmd_purge(ws: Workspace, args: argparse.Namespace) -> dict[str, Any]:
    return {
        "removed": purge_expired(ws, _now(args)),
        "retention_days": Policy.load(ws).raw_retention_days,
    }


# --- plumbing ---------------------------------------------------------------------------


def _parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="tn_assist")
    root.add_argument("--base", default=os.environ.get("TN_ASSIST_BASE"))
    root.add_argument("--org", default=os.environ.get("TN_ASSIST_ORG"))
    root.add_argument("--number", default=os.environ.get("TN_ASSIST_NUMBER"))
    sub = root.add_subparsers(dest="command", required=True)

    def add(name: str, *, now: bool = True) -> argparse.ArgumentParser:
        p = sub.add_parser(name)
        if now:
            p.add_argument("--now")
        return p

    p = add("init")
    p.add_argument("--connected", required=True)
    p.add_argument("--business", required=True)
    p.add_argument("--lang", choices=["pt", "en"], default="pt")
    p.add_argument("--harness", choices=["claude-code", "claude-desktop", "codex", "antigravity"])
    p.add_argument("--admin", required=True)
    p.add_argument("--admin-name")
    p.add_argument("--confirm-connected", action="store_true")
    p = add("cursor")
    p.add_argument("--set")
    p.add_argument("--from-page")
    p = add("fetch-plan", now=False)
    p.add_argument("--page", action="append", default=[])
    p = add("ingest")
    p.add_argument("--file", action="append", required=True)
    p = add("next")
    p.add_argument("--kinds", default="contact,admin,attendant")
    p.add_argument("--ttl", type=int, default=_LEASE_SECONDS)
    p = add("next-status", now=False)
    p.add_argument("--item", required=True)
    p = add("set-text", now=False)
    p.add_argument("--item", required=True)
    p.add_argument("--event", required=True)
    p.add_argument("--file")
    p.add_argument("--unreadable", action="store_true")
    p = add("pack")
    p.add_argument("--item", required=True)
    p.add_argument("--about")
    p = add("apply")
    p.add_argument("--item", required=True)
    source = p.add_mutually_exclusive_group(required=True)
    source.add_argument("--decision-file")
    source.add_argument("--escalate", metavar="REASON", help="hand the customer to a person")
    p = add("run-console")
    p.add_argument("--item", required=True)
    p = add("complete", now=False)
    p.add_argument("--item", required=True)
    add("reminders")
    p = add("report-failure")
    p.add_argument("--cause", required=True)
    p.add_argument("--cycle", required=True)
    add("status")
    p = add("admin")
    p.add_argument("action", choices=["list", "add", "remove"])
    p.add_argument("--number")
    p.add_argument("--name")
    p.add_argument("--confirm-connected", action="store_true")
    p = add("source")
    p.add_argument("action", choices=["list", "discover", "classify", "marker"])
    p.add_argument("--names", default="")
    p.add_argument("--name")
    p.add_argument("--cls", choices=["public", "internal", "admin-only", "admin_only", "off"])
    p.add_argument("--mode", choices=["snapshot", "live"], default="snapshot")
    p.add_argument("--live-tools", default="")
    p.add_argument("--personal", action="store_true")
    p.add_argument("--confirmed", action="store_true")
    p.add_argument("--marker")
    p = add("kb-write", now=False)
    p.add_argument("--path", required=True)
    p.add_argument("--visibility", choices=["public", "internal"], required=True)
    p.add_argument("--description", required=True)
    p.add_argument("--from-file", required=True)
    for setting in ("mode", "lang"):
        p = add(setting, now=False)
        p.add_argument("value", choices=["auto", "assist"] if setting == "mode" else ["pt", "en"])
    p = add("version-check")
    p.add_argument("--latest-json")
    p.add_argument("--announce", action="store_true")
    add("migrate")
    p = add("export", now=False)
    p.add_argument("--contact", required=True)
    p = add("forget")
    p.add_argument("--contact", required=True)
    add("purge")
    p = add("run", now=False)
    p.add_argument("--harness", choices=["claude-code", "codex"], required=True)
    p.add_argument("--interval", type=int, default=20)
    p.add_argument("--once", action="store_true")
    p.add_argument("--model")
    return root


_WORKSPACE_COMMANDS = {
    "cursor": cmd_cursor,
    "fetch-plan": cmd_fetch_plan,
    "ingest": cmd_ingest,
    "next": cmd_next,
    "next-status": cmd_next_status,
    "set-text": cmd_set_text,
    "pack": cmd_pack,
    "apply": cmd_apply,
    "run-console": cmd_run_console,
    "complete": cmd_complete,
    "reminders": cmd_reminders,
    "report-failure": cmd_report_failure,
    "status": cmd_status,
    "admin": cmd_admin,
    "source": cmd_source,
    "kb-write": cmd_kb_write,
    "version-check": cmd_version_check,
    "migrate": cmd_migrate,
    "export": cmd_export,
    "forget": cmd_forget,
    "purge": cmd_purge,
    "run": cmd_run,
}


def main(
    argv: Sequence[str] | None = None,
    *,
    base: Path | str | None = None,
    org: str | None = None,
    number: str | None = None,
    stdin: IO[str] | None = None,
) -> int:
    args = _parser().parse_args(list(argv) if argv is not None else None)
    del stdin
    base = base or args.base
    org = org or args.org
    number = number or args.number
    try:
        if not (base and org and number):
            raise CliError(
                "no_workspace", "give --base, --org and --number (or TN_ASSIST_* variables)"
            )
        if args.command == "init":
            payload = cmd_init({"base": base, "org": org, "number": number}, args)
        else:
            try:
                ws = Workspace.open(Path(base), org, number, create=False)
            except (FileNotFoundError, InvalidWorkspaceId) as error:
                raise CliError("no_workspace", "run init first") from error
            if args.command in ("mode", "lang"):
                args.setting = args.command
                payload = cmd_set(ws, args)
            else:
                payload = _WORKSPACE_COMMANDS[args.command](ws, args)
        print(json.dumps({"ok": True, **payload}, ensure_ascii=False))
        return 0
    except CliError as error:
        print(
            json.dumps(
                {"ok": False, "error": error.error, "message": error.message, **error.extra},
                ensure_ascii=False,
            )
        )
        return error.code
    except (InvalidContactKey, FileNotFoundError, json.JSONDecodeError) as error:
        print(
            json.dumps(
                {"ok": False, "error": "bad_input", "message": str(error)}, ensure_ascii=False
            )
        )
        return 1


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
