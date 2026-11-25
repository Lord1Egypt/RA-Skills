"""What each console command does. Pure workspace operations, no network, no model.

Every handler returns text for the person plus any actions for trusted code to carry out (sending a
draft, for example). Authorization and confirmation happen here, before anything changes.
"""

from __future__ import annotations

import json
import re
import shutil
import unicodedata
from dataclasses import dataclass, field, replace
from datetime import datetime
from pathlib import Path
from typing import Literal

from tn_assist import __version__
from tn_assist.admins import (
    ConnectedNumberNeedsConfigurator,
    ConnectedNumberNeedsConfirmation,
    LastAdministratorError,
    NotAnAdministrator,
    Registry,
)
from tn_assist.apply import (
    Action,
    OptedOut,
    Reply,
    drop_drafts_for,
    list_drafts,
    open_escalations,
    pop_draft,
    resume_contact,
)
from tn_assist.commands import (
    AUTHORIZATION,
    Command,
    authorize,
    confirm,
    issue_confirmation,
    needs_confirmation,
    parse_command,
)
from tn_assist.config import load_config, save_config
from tn_assist.i18n import t
from tn_assist.memory import AUTO_RESUME_MIN_MINUTES, Card, Fact, Policy, append_line, read_lines
from tn_assist.paths import ContactKey, InvalidContactKey, Workspace
from tn_assist.queue import drop_outbox_for, pending_count
from tn_assist.sanitize import clean_fact_value
from tn_assist.sources import (
    NeedsConfirmation,
    SourceClass,
    SourceRegistry,
    WriteToolError,
)
from tn_assist.state import (
    ContactRecord,
    ContactState,
    load_state,
    mark_takeover,
    pause_unless_opted_out,
    save_state,
)
from tn_assist.store import append_jsonl, read_json, write_json_atomic
from tn_assist.timeutil import parse_iso, utc_iso

Role = Literal["admin", "attendant"]
_DISPLAY = {
    "help": ("ajuda", "help"),
    "status": ("status", "status"),
    "queue": ("fila", "queue"),
    "send": ("enviar", "send"),
    "digest": ("resumo", "digest"),
    "resume": ("retomar", "resume"),
    "takeover": ("assumir", "takeover"),
    "contact": ("cliente", "contact"),
    "thread": ("conversa", "thread"),
    "note": ("nota", "note"),
    "contacts": ("clientes", "contacts"),
    "admins": ("admins", "admins"),
    "admin_add": ("admin add", "admin add"),
    "admin_remove": ("admin remover", "admin remove"),
    "teach": ("ensinar", "teach"),
    "kb": ("conhecimento", "kb"),
    "sources": ("fontes", "sources"),
    "pause": ("pausar", "pause"),
    "forget": ("esquecer", "forget"),
    "mode": ("modo", "mode"),
    "policy": ("politica", "policy"),
    "lang": ("idioma", "lang"),
}
_HELP_ORDER = list(_DISPLAY)
_REMOVE_WORDS = {"remove", "remover", "rm", "delete", "apagar"}
_CLASS_WORDS = {
    "publica": SourceClass.PUBLIC,
    "public": SourceClass.PUBLIC,
    "publico": SourceClass.PUBLIC,
    "interna": SourceClass.INTERNAL,
    "internal": SourceClass.INTERNAL,
    "interno": SourceClass.INTERNAL,
    "admin": SourceClass.ADMIN_ONLY,
    "admin_only": SourceClass.ADMIN_ONLY,
    "desligada": SourceClass.OFF,
    "off": SourceClass.OFF,
    "desligado": SourceClass.OFF,
}


@dataclass
class CommandResult:
    text: str
    actions: list[Action] = field(default_factory=list)


def _lang(ws: Workspace) -> Literal["pt", "en"]:
    return "en" if load_config(ws).get("lang") == "en" else "pt"


def _fold(text: str) -> str:
    base = unicodedata.normalize("NFKD", text.lower())
    return "".join(ch for ch in base if not unicodedata.combining(ch))


def _contacts(ws: Workspace) -> list[ContactKey]:
    root = ws.root / "contacts"
    keys = []
    if root.is_dir():
        for directory in sorted(root.iterdir()):
            try:
                keys.append(ContactKey.parse(directory.name))
            except InvalidContactKey:
                continue
    return keys


def _name(ws: Workspace, key: ContactKey) -> str:
    fact = Card.load(ws, key).get("name")
    return fact.value if fact else str(key)


def _find(ws: Workspace, query: str) -> list[ContactKey]:
    query = query.strip()
    try:
        key = ContactKey.parse(query)
        if (ws.root / "contacts" / str(key)).is_dir():
            return [key]
    except InvalidContactKey:
        pass
    folded = _fold(query)
    if len(folded) < 2:
        return []
    return [k for k in _contacts(ws) if folded in _fold(_name(ws, k)) or folded in str(k)]


# --- queue ------------------------------------------------------------------------------


@dataclass(frozen=True)
class QueueEntry:
    n: int
    contact: str
    reason: str


def queue_entries(ws: Workspace) -> list[QueueEntry]:
    escalated = open_escalations(ws)
    seen = {row["contact"] for row in escalated}
    paused = []
    for key in _contacts(ws):
        record = load_state(ws, key)
        if str(key) not in seen and record.state in (ContactState.PAUSED, ContactState.HANDOFF):
            paused.append((record.since or "", str(key), record.reason or record.state.value))
    rows = [(r["contact"], r["reason"]) for r in escalated] + [
        (c, why) for _, c, why in sorted(paused)
    ]
    return [QueueEntry(i + 1, contact, reason) for i, (contact, reason) in enumerate(rows)]


def _snapshot_path(ws: Workspace) -> Path:
    return ws.path("queue-view.json")


def _resolve(ws: Workspace, arg: str) -> tuple[ContactKey | None, str | None]:
    """A queue position (from the last /fila), a number or part of a name."""
    if arg.isdigit() and len(arg) <= 3:
        data = read_json(_snapshot_path(ws), {})
        entries = data.get("entries", []) if isinstance(data, dict) else []
        position = int(arg)
        if 1 <= position <= len(entries):
            return ContactKey.parse(entries[position - 1]), None
        return None, "need_queue"
    found = _find(ws, arg)
    if len(found) == 1:
        return found[0], None
    if not found:
        return None, "not_found"
    return None, "ambiguous:" + ", ".join(_name(ws, k) for k in found[:5])


def _problem(ws: Workspace, code: str) -> CommandResult:
    lang = _lang(ws)
    if code == "need_queue":
        return CommandResult(t("resume_need_queue", lang))
    if code.startswith("ambiguous:"):
        return CommandResult(t("ambiguous", lang, names=code.split(":", 1)[1]))
    return CommandResult(t("not_found", lang))


# --- the commands -----------------------------------------------------------------------


def _help(ws: Workspace, role: Role) -> str:
    lang = _lang(ws)
    idx = 0 if lang == "pt" else 1
    lines = [t("help_header", lang)]
    lines += [
        t(f"help_{name}", lang)
        for name in _HELP_ORDER
        if role in AUTHORIZATION.get(name, frozenset())
    ]
    del idx
    return "\n".join(lines)


def _status(ws: Workspace, role: Role) -> str:
    lang = _lang(ws)
    cursor = read_json(ws.path("cursor.json"), {})
    last = (cursor.get("last_tick_at") if isinstance(cursor, dict) else None) or t(
        "status_never", lang
    )
    config = load_config(ws)
    mode = t("mode_auto" if config.get("mode") == "auto" else "mode_assist", lang)
    text = t(
        "status_text",
        lang,
        last=str(last),
        backlog=str(pending_count(ws)),
        waiting=str(len(queue_entries(ws))),
        drafts=str(len(list_drafts(ws))),
        mode=mode,
        paused=t("paused_suffix", lang) if config.get("paused") else "",
        version=__version__,
    )
    if Registry.load(ws).connected_is_admin():
        text += "\n" + t("status_connected_admin", lang)
    return text


def _queue(ws: Workspace) -> str:
    lang = _lang(ws)
    entries = queue_entries(ws)
    write_json_atomic(_snapshot_path(ws), {"entries": [e.contact for e in entries]})
    drafts = list_drafts(ws)
    if not entries and not drafts:
        return t("queue_empty", lang)
    lines: list[str] = []
    if entries:
        lines.append(t("queue_waiting", lang))
        for e in entries:
            key = ContactKey.parse(e.contact)
            lines.append(
                t(
                    "queue_entry",
                    lang,
                    n=str(e.n),
                    name=_name(ws, key),
                    number=e.contact,
                    reason=e.reason,
                )
            )
    if drafts:
        lines.append(t("queue_drafts", lang))
        for d in drafts:
            key = ContactKey.parse(d["contact"])
            lines.append(
                t("queue_draft", lang, n=str(d["n"]), name=_name(ws, key), text=d["text"][:120])
            )
    return "\n".join(lines)


def _resume(
    ws: Workspace, cmd: Command, role: Role, actor: str, now: datetime, confirmed: bool
) -> CommandResult:
    lang = _lang(ws)
    arg = cmd.args[0] if cmd.args else ""
    if _fold(arg) in ("todos", "tudo", "all"):
        if role != "admin":
            return CommandResult(t("resume_all_admin_only", lang))
        config = load_config(ws)
        config["paused"] = False
        save_config(ws, config)
        return CommandResult(t("resume_all_done", lang))
    if not arg:
        entries = queue_entries(ws)
        if len(entries) == 1:
            key: ContactKey | None = ContactKey.parse(entries[0].contact)
        elif not entries:
            return CommandResult(t("resume_nobody", lang))
        else:
            return CommandResult(t("resume_need_queue", lang))
    else:
        key, problem = _resolve(ws, arg)
    if key is None:
        return _problem(ws, problem or "not_found")
    opted_out = load_state(ws, key).state is ContactState.DO_NOT_CONTACT
    if opted_out and role != "admin":
        return CommandResult(t("dnc_admin_only", lang, name=_name(ws, key)))
    if opted_out and not confirmed:
        # the code is for THIS customer: a queue position could point at someone else by then
        bound = parse_command(f"/retomar {key}") or cmd
        code = issue_confirmation(ws, actor, bound, now)
        return CommandResult(
            t("confirm_resume", lang, name=_name(ws, key), number=str(key), code=code)
        )
    try:
        resume_contact(ws, key, by=actor, now=now, override_opt_out=opted_out and confirmed)
    except OptedOut:
        return CommandResult(t("dnc_admin_only", lang, name=_name(ws, key)))
    return CommandResult(t("resume_done", lang, name=_name(ws, key)))


def _takeover(ws: Workspace, cmd: Command, now: datetime) -> CommandResult:
    lang = _lang(ws)
    if not cmd.args:
        return CommandResult(t("usage", lang))
    key, problem = _resolve(ws, cmd.args[0])
    if key is None:
        return _problem(ws, problem or "not_found")
    mark_takeover(ws, key, utc_iso(now))
    drop_drafts_for(ws, str(key))
    drop_outbox_for(ws, str(key))  # a person speaks now: nothing the assistant queued goes out
    return CommandResult(t("takeover_done", lang, name=_name(ws, key)))


def _send(ws: Workspace, cmd: Command, role: Role, now: datetime) -> CommandResult:
    lang = _lang(ws)
    if not cmd.args or not cmd.args[0].isdigit():
        return CommandResult(t("send_needs_number", lang))
    number = int(cmd.args[0])
    draft = next((d for d in list_drafts(ws) if d["n"] == number), None)
    if draft is None:
        return CommandResult(t("send_unknown", lang, n=str(number)))
    target = ContactKey.parse(draft["contact"])
    if load_state(ws, target).state is ContactState.DO_NOT_CONTACT:
        pop_draft(ws, number)
        return CommandResult(t("dnc_blocked", lang, name=_name(ws, target)))
    if load_config(ws).get("paused") and role != "admin":
        return CommandResult(t("paused_admin_only", lang))
    replacement = cmd.rest.strip()
    if draft.get("blocked") and not replacement:
        return CommandResult(t("send_blocked", lang, n=str(number)))
    pop_draft(ws, number)
    key = ContactKey.parse(draft["contact"])
    text = replacement or draft["text"]
    record = load_state(ws, key)
    stamps = list(record.counters.get("replies", []))[-99:] + [utc_iso(now)]
    save_state(ws, key, replace(record, counters={**record.counters, "replies": stamps}))
    append_line(
        ws,
        key,
        role="attendant" if replacement else "assistant",
        text=text,
        event_id=f"reply-{draft['event_id']}",
        at=utc_iso(now),
    )
    reply = Reply(draft["contact"], draft.get("quote_message_id"), text, draft["event_id"])
    return CommandResult(t("send_done", lang, name=_name(ws, key)), [reply])


def _line_label(lang: Literal["pt", "en"], role: str) -> str:
    key = {
        "contact": "who_contact",
        "assistant": "who_assistant",
        "attendant_native": "who_attendant",
    }
    return t(key.get(role, "who_other"), lang)


def _contact_card(ws: Workspace, cmd: Command) -> CommandResult:
    lang = _lang(ws)
    if not cmd.tail:
        return CommandResult(t("usage", lang))
    found = _find(ws, cmd.tail)
    if not found:
        return CommandResult(t("not_found", lang))
    if len(found) > 1:
        return CommandResult(t("ambiguous", lang, names=", ".join(_name(ws, k) for k in found[:5])))
    key = found[0]
    record = load_state(ws, key)
    card = Card.load(ws, key)
    lines = [
        t(
            "contact_header",
            lang,
            name=_name(ws, key),
            number=str(key),
            state=record.state.value,
            language=record.language or "?",
        ),
        card.render() or t("contact_no_facts", lang),
        t("contact_recent", lang),
    ]
    recent = [ln for ln in read_lines(ws, key) if ln.kind == "message"][-3:]
    lines += [f"{_line_label(lang, ln.role)}: {ln.text[:200]}" for ln in recent]
    return CommandResult("\n".join(lines))


def _thread(ws: Workspace, cmd: Command) -> CommandResult:
    lang = _lang(ws)
    if not cmd.args:
        return CommandResult(t("usage", lang))
    found = _find(ws, cmd.args[0])
    if len(found) != 1:
        return CommandResult(t("not_found", lang))
    count = 10
    if len(cmd.args) > 1 and cmd.args[1].isdigit():
        count = max(1, min(30, int(cmd.args[1])))
    lines = [ln for ln in read_lines(ws, found[0]) if ln.kind == "message"][-count:]
    if not lines:
        return CommandResult(t("thread_empty", lang))
    return CommandResult(
        "\n".join(f"{_line_label(lang, ln.role)}: {ln.text[:300]}" for ln in lines)
    )


def _note(ws: Workspace, cmd: Command, role: Role, now: datetime) -> CommandResult:
    lang = _lang(ws)
    if len(cmd.args) < 2:
        return CommandResult(t("usage", lang))
    found = _find(ws, cmd.args[0])
    if len(found) != 1:
        return CommandResult(t("not_found", lang))
    key = found[0]
    card = Card.load(ws, key)
    taken = [int(fact.key[5:]) for fact in card.facts() if re.fullmatch(r"note_\d+", fact.key)]
    number = 1 + max(taken, default=0)  # never reuse a number a trimmed note once had
    card.merge([Fact(f"note_{number:03d}", clean_fact_value(cmd.rest), role, utc_iso(now))])
    card.save()
    return CommandResult(t("note_saved", lang, name=_name(ws, key)))


def _contacts_list(ws: Workspace, cmd: Command) -> CommandResult:
    lang = _lang(ws)
    keys = _contacts(ws)
    needle = _fold(cmd.tail)
    rows = []
    for key in keys:
        state = load_state(ws, key).state.value
        if (
            needle
            and needle not in _fold(_name(ws, key))
            and needle not in state
            and needle not in str(key)
        ):
            continue
        rows.append(t("contacts_line", lang, name=_name(ws, key), number=str(key), state=state))
    return CommandResult("\n".join(rows[:40]) if rows else t("contacts_empty", lang))


def _admins(ws: Workspace) -> CommandResult:
    lang = _lang(ws)
    return CommandResult(
        t("admins_list", lang, lines="\n".join(sorted(Registry.load(ws).numbers())))
    )


def _admin_add(
    ws: Workspace, cmd: Command, actor: str, message_id: str | None, now: datetime
) -> CommandResult:
    lang = _lang(ws)
    if not cmd.args:
        return CommandResult(t("usage", lang))
    try:
        key = ContactKey.parse(cmd.args[0])
        name = " ".join(cmd.args[1:]) or None
        added = Registry.load(ws).add(
            str(key), name, by=actor, via="whatsapp", message_id=message_id, now=now
        )
    except InvalidContactKey:
        return CommandResult(t("invalid_number", lang))
    except ConnectedNumberNeedsConfigurator:
        return CommandResult(t("connected_number_refused_over_whatsapp", lang))
    except (NotAnAdministrator, ConnectedNumberNeedsConfirmation):
        return CommandResult(t("usage", lang))
    return CommandResult(t("admin_added" if added else "admin_exists", lang, number=str(key)))


def _admin_remove(
    ws: Workspace, cmd: Command, actor: str, message_id: str | None, now: datetime
) -> CommandResult:
    lang = _lang(ws)
    if not cmd.args:
        return CommandResult(t("usage", lang))
    try:
        key = ContactKey.parse(cmd.args[0])
        removed = Registry.load(ws).remove(str(key), by=actor, message_id=message_id, now=now)
    except InvalidContactKey:
        return CommandResult(t("invalid_number", lang))
    except LastAdministratorError:
        return CommandResult(t("admin_last", lang))
    except NotAnAdministrator:
        return CommandResult(t("usage", lang))
    return CommandResult(t("admin_removed" if removed else "admin_unknown", lang, number=str(key)))


# --- teaching and knowledge -------------------------------------------------------------


def _slug(topic: str) -> str:
    folded = re.sub(r"[^a-z0-9]+", "-", _fold(topic)).strip("-")
    return folded[:40] or "assunto"


def _capture_path(ws: Workspace) -> Path:
    return ws.path("capture.json")


def _index_path(ws: Workspace) -> Path:
    return ws.path("knowledge", "INDEX.md")


def _index_lines(ws: Workspace) -> list[str]:
    try:
        return _index_path(ws).read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return []


def _write_index(ws: Workspace, lines: list[str]) -> None:
    path = _index_path(ws)
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _set_index_entry(ws: Workspace, old: str | None, new: str, description: str) -> None:
    lines = [ln for ln in _index_lines(ws) if not (old and ln.startswith(f"- {old}:"))]
    lines = [ln for ln in lines if not ln.startswith(f"- {new}:")]
    lines.append(f"- {new}: {description}")
    _write_index(ws, lines)


def _teach(ws: Workspace, cmd: Command, actor: str, now: datetime) -> CommandResult:
    lang = _lang(ws)
    if not cmd.tail:
        return CommandResult(t("usage", lang))
    write_json_atomic(
        _capture_path(ws),
        {"actor": actor, "topic": cmd.tail, "slug": _slug(cmd.tail), "started_at": utc_iso(now)},
    )
    return CommandResult(t("teach_started", lang, topic=cmd.tail))


def capture_text(ws: Workspace, actor: str, text: str, now: datetime) -> CommandResult | None:
    """Free text from the administrator who is teaching. Anything else is not for this module."""
    data = read_json(_capture_path(ws), {})
    if not isinstance(data, dict) or data.get("actor") != actor or "slug" not in data:
        return None
    if data.get("finished") or parse_command(text) is not None:
        return None
    inbox = ws.path("knowledge", "internal", "_inbox", f"{data['slug']}.md")
    inbox.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    with open(inbox, "a", encoding="utf-8") as handle:
        handle.write(text.strip() + "\n\n")
    return CommandResult(t("teach_got", _lang(ws)))


def _done(ws: Workspace) -> CommandResult:
    lang = _lang(ws)
    data = read_json(_capture_path(ws), {})
    if not isinstance(data, dict) or "slug" not in data or data.get("finished"):
        return CommandResult(t("teach_none", lang))
    slug = data["slug"]
    inbox = ws.path("knowledge", "internal", "_inbox", f"{slug}.md")
    target = ws.path("knowledge", "internal", f"{slug}.md")
    body = inbox.read_text(encoding="utf-8") if inbox.exists() else ""
    target.write_text(f"# {data['topic']}\n\n{body}", encoding="utf-8")
    if inbox.exists():
        inbox.unlink()
    first = (body.strip().splitlines() or [data["topic"]])[0][:60]
    _set_index_entry(ws, None, f"internal/{slug}.md", f"{data['topic']}: {first}")
    data.update(finished=True, last=slug)
    write_json_atomic(_capture_path(ws), data)
    return CommandResult(t("teach_filed", lang, path=f"internal/{slug}.md"))


def _publish(ws: Workspace, *, public: bool) -> CommandResult:
    lang = _lang(ws)
    data = read_json(_capture_path(ws), {})
    slug = data.get("last") if isinstance(data, dict) else None
    if not slug:
        return CommandResult(t("teach_none", lang))
    internal_path = ws.path("knowledge", "internal", f"{slug}.md")
    public_path = ws.path("knowledge", f"{slug}.md")
    description = next(
        (
            ln[len(f"- internal/{slug}.md: ") :]
            for ln in _index_lines(ws)
            if ln.startswith(f"- internal/{slug}.md:")
        ),
        next(
            (ln.split(": ", 1)[1] for ln in _index_lines(ws) if ln.startswith(f"- {slug}.md:")),
            slug,
        ),
    )
    if public and internal_path.exists():
        shutil.move(str(internal_path), str(public_path))
        _set_index_entry(ws, f"internal/{slug}.md", f"{slug}.md", description)
        return CommandResult(t("teach_public", lang, path=f"{slug}.md"))
    if not public and public_path.exists():
        shutil.move(str(public_path), str(internal_path))
        _set_index_entry(ws, f"{slug}.md", f"internal/{slug}.md", description)
    return CommandResult(t("teach_internal", lang, path=f"internal/{slug}.md"))


def _kb(ws: Workspace, cmd: Command, confirmed: bool) -> CommandResult:
    lang = _lang(ws)
    entries = []
    for line in _index_lines(ws):
        match = re.match(r"^-\s+([\w./-]+\.md):\s*(.*)$", line)
        if match:
            entries.append((match.group(1), match.group(2)))
    args = list(cmd.args)
    removing = bool(args) and _fold(args[0]) in _REMOVE_WORDS
    if removing:
        args = args[1:]
    if not args:
        lines = [t("kb_header", lang)]
        for path, description in entries:
            visibility = t("kb_internal" if path.startswith("internal/") else "kb_public", lang)
            lines.append(
                t("kb_line", lang, path=path, visibility=visibility, description=description)
            )
        return CommandResult("\n".join(lines))
    needle = _fold(" ".join(args))
    match_path = next((p for p, _ in entries if needle in _fold(p)), None)
    if match_path is None:
        return CommandResult(t("kb_missing", lang))
    if removing:
        target = ws.path("knowledge", match_path)
        if target.exists():
            target.unlink()
        _write_index(ws, [ln for ln in _index_lines(ws) if not ln.startswith(f"- {match_path}:")])
        return CommandResult(t("kb_removed", lang, path=match_path))
    return CommandResult(ws.path("knowledge", match_path).read_text(encoding="utf-8")[:800])


def _sources(
    ws: Workspace, cmd: Command, actor: str, now: datetime, confirmed: bool
) -> CommandResult:
    lang = _lang(ws)
    registry = SourceRegistry.load(ws)
    names = {s.name for s in registry.all()}
    if not cmd.args:
        if not names:
            return CommandResult(t("sources_empty", lang))
        lines = [
            t("sources_line", lang, name=s.name, cls=t(f"cls_{s.cls.value}", lang), mode=s.mode)
            for s in registry.all()
        ]
        return CommandResult("\n".join(lines + [t("sources_class_help", lang)]))
    name = cmd.args[0]
    if name not in names:
        return CommandResult(t("sources_unknown", lang, name=name))
    if len(cmd.args) < 2 or _fold(cmd.args[1]) not in _CLASS_WORDS:
        return CommandResult(t("sources_class_help", lang))
    cls = _CLASS_WORDS[_fold(cmd.args[1])]
    current = registry.get(name)
    assert current is not None
    try:
        registry.classify(
            name,
            cls,
            mode=current.mode,
            live_tools=current.live_tools,
            personal=current.personal,
            confirmed=confirmed,
        )
    except NeedsConfirmation:
        code = issue_confirmation(ws, actor, cmd, now)
        return CommandResult(t("confirm_ask", lang, code=code))
    except WriteToolError:
        return CommandResult(t("sources_write", lang))
    return CommandResult(t("sources_changed", lang, name=name, cls=t(f"cls_{cls.value}", lang)))


# --- pause, forget, settings ------------------------------------------------------------


def _pause(ws: Workspace, cmd: Command, now: datetime) -> CommandResult:
    lang = _lang(ws)
    if not cmd.args:
        config = load_config(ws)
        config["paused"] = True
        save_config(ws, config)
        return CommandResult(t("paused_all", lang))
    found = _find(ws, cmd.args[0])
    if len(found) != 1:
        return CommandResult(t("not_found", lang))
    key = found[0]
    pause_unless_opted_out(ws, key, reason="paused_by_admin", at=utc_iso(now))
    drop_outbox_for(ws, str(key))
    return CommandResult(t("paused_one", lang, name=_name(ws, key)))


def _erase_from(root: Path, key: ContactKey) -> None:
    """Remove one customer from a workspace tree (the live one, or a copy a migration made)."""
    directory = root / "contacts" / str(key)
    if directory.exists():
        shutil.rmtree(directory)
    escalation = root / "escalations" / f"{key}.json"
    if escalation.exists():
        escalation.unlink()
    drafts_path = root / "drafts.json"
    drafts = read_json(drafts_path, {})
    if isinstance(drafts, dict) and drafts.get("drafts"):
        drafts["drafts"] = [d for d in drafts["drafts"] if d.get("contact") != str(key)]
        write_json_atomic(drafts_path, drafts)
    for folder in (root / "queue" / "pending", root / "queue" / "leased"):
        for path in folder.glob("*.json") if folder.is_dir() else []:
            payload = read_json(path, {})
            item = payload.get("item", payload) if isinstance(payload, dict) else {}
            if item.get("contact") == str(key):
                path.unlink()
    outbox = root / "outbox"
    for path in outbox.glob("*.json") if outbox.is_dir() else []:
        op = read_json(path, {})
        if isinstance(op, dict) and str(key) in (op.get("contact"), op.get("to")):
            path.unlink()


def forget_contact(ws: Workspace, key: ContactKey, actor: str, now: datetime) -> None:
    """Erase what the assistant kept about one customer, and leave a trace that it happened."""
    _erase_from(ws.root, key)
    backups = ws.root / "backup"
    for snapshot in backups.iterdir() if backups.is_dir() else []:
        if snapshot.is_dir():
            _erase_from(snapshot, key)  # a copy made before a migration keeps the customer too
    append_jsonl(
        ws.path("audit.log"),
        {"at": utc_iso(now), "action": "forget", "number": str(key), "by": actor},
    )


def _forget(ws: Workspace, cmd: Command, actor: str, now: datetime) -> CommandResult:
    lang = _lang(ws)
    if not cmd.args:
        return CommandResult(t("usage", lang))
    try:
        key = ContactKey.parse(cmd.args[0])
    except InvalidContactKey:
        return CommandResult(t("invalid_number", lang))
    forget_contact(ws, key, actor, now)
    return CommandResult(t("forgotten", lang, number=str(key)))


# agents that cannot run a customer turn without tools: a person must approve every answer
NO_RUNNER_HARNESSES = frozenset({"claude-desktop", "antigravity"})


def _mode(ws: Workspace, cmd: Command) -> CommandResult:
    lang = _lang(ws)
    word = _fold(cmd.args[0]) if cmd.args else ""
    config = load_config(ws)
    if word in ("assistido", "assist", "assisted", "sombra", "shadow"):
        config["mode"] = "assist"
    elif word in ("automatico", "auto", "automatic", "ativo", "live"):
        if config.get("harness") in NO_RUNNER_HARNESSES:
            return CommandResult(t("mode_auto_unavailable", lang))
        config["mode"] = "auto"
    else:
        return CommandResult(t("mode_help", lang))
    save_config(ws, config)
    return CommandResult(
        t(
            "mode_set",
            lang,
            mode=t("mode_auto" if config["mode"] == "auto" else "mode_assist", lang),
        )
    )


def _lang_command(ws: Workspace, cmd: Command) -> CommandResult:
    word = _fold(cmd.args[0]) if cmd.args else ""
    if word not in ("pt", "en"):
        return CommandResult(t("lang_help", _lang(ws)))
    config = load_config(ws)
    config["lang"] = word
    save_config(ws, config)
    return CommandResult(t("lang_set", word))  # type: ignore[arg-type]


def _resume_setting(policy: Policy, lang: Literal["pt", "en"]) -> str:
    minutes = policy.auto_resume_after_minutes
    if (
        isinstance(minutes, int)
        and not isinstance(minutes, bool)
        and minutes >= AUTO_RESUME_MIN_MINUTES
    ):
        return f"{minutes} min"
    return "desligado" if lang == "pt" else "off"


def _policy(ws: Workspace) -> CommandResult:
    p = Policy.load(ws)
    proposals = ws.path("policy-proposals.md")
    count = proposals.read_text(encoding="utf-8").count("\n## ") if proposals.exists() else 0
    return CommandResult(
        t(
            "policy_text",
            _lang(ws),
            contact=str(p.pack_budget_contact),
            admin=str(p.pack_budget_admin),
            days=str(p.raw_retention_days),
            per_hour=str(p.reply_cap_per_hour),
            per_day=str(p.reply_cap_per_day),
            reminder=str(p.handoff_reminder_hours),
            resume=_resume_setting(p, _lang(ws)),
            proposals=str(count),
        )
    )


def _digest(ws: Workspace, now: datetime) -> CommandResult:
    states: dict[str, int] = {"active": 0, "handoff": 0, "paused": 0, "do_not_contact": 0}
    today = 0
    prefix = utc_iso(now)[:10]
    keys = _contacts(ws)
    for key in keys:
        record: ContactRecord = load_state(ws, key)
        states[record.state.value] += 1
        today += sum(1 for ln in read_lines(ws, key) if ln.at.startswith(prefix))
    return CommandResult(
        t(
            "digest_text",
            _lang(ws),
            total=str(len(keys)),
            active=str(states["active"]),
            handoff=str(states["handoff"]),
            paused=str(states["paused"]),
            dnc=str(states["do_not_contact"]),
            today=str(today),
            drafts=str(len(list_drafts(ws))),
        )
    )


# --- entry point ------------------------------------------------------------------------


def _refusal(ws: Workspace, role: Role) -> CommandResult:
    allowed = "\n".join(
        t(f"help_{name}", _lang(ws))
        for name in _HELP_ORDER
        if role in AUTHORIZATION.get(name, frozenset())
    )
    return CommandResult(t("refused_admin_only", _lang(ws), allowed=allowed))


def run_command(
    ws: Workspace,
    role: Role,
    actor: str,
    cmd: Command,
    now: datetime,
    *,
    message_id: str | None = None,
    confirmed: bool = False,
) -> CommandResult:
    if not authorize(cmd, role):
        return _refusal(ws, role)
    lang = _lang(ws)
    if cmd.name == "confirm":
        pending = confirm(ws, actor, cmd.args[0] if cmd.args else "", now)
        if pending is None:
            return CommandResult(t("confirm_invalid", lang))
        return run_command(ws, role, actor, pending, now, message_id=message_id, confirmed=True)
    if needs_confirmation(cmd) and not confirmed:
        return CommandResult(t("confirm_ask", lang, code=issue_confirmation(ws, actor, cmd, now)))
    handlers = {
        "help": lambda: CommandResult(_help(ws, role)),
        "status": lambda: CommandResult(_status(ws, role)),
        "queue": lambda: CommandResult(_queue(ws)),
        "digest": lambda: _digest(ws, now),
        "admins": lambda: _admins(ws),
        "policy": lambda: _policy(ws),
        "done": lambda: _done(ws),
        "public": lambda: _publish(ws, public=True),
        "internal": lambda: _publish(ws, public=False),
        "resume": lambda: _resume(ws, cmd, role, actor, now, confirmed),
        "takeover": lambda: _takeover(ws, cmd, now),
        "send": lambda: _send(ws, cmd, role, now),
        "contact": lambda: _contact_card(ws, cmd),
        "thread": lambda: _thread(ws, cmd),
        "note": lambda: _note(ws, cmd, role, now),
        "contacts": lambda: _contacts_list(ws, cmd),
        "admin_add": lambda: _admin_add(ws, cmd, actor, message_id, now),
        "admin_remove": lambda: _admin_remove(ws, cmd, actor, message_id, now),
        "teach": lambda: _teach(ws, cmd, actor, now),
        "kb": lambda: _kb(ws, cmd, confirmed),
        "sources": lambda: _sources(ws, cmd, actor, now, confirmed),
        "pause": lambda: _pause(ws, cmd, now),
        "forget": lambda: _forget(ws, cmd, actor, now),
        "mode": lambda: _mode(ws, cmd),
        "lang": lambda: _lang_command(ws, cmd),
    }
    return handlers[cmd.name]()


def parse_when(stamp: str) -> datetime:
    return parse_iso(stamp)


_ = json  # kept for callers that import the module for its JSON helpers
