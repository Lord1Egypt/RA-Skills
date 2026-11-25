"""The steps of a cycle that both the command line and the runner use.

Nothing here talks to the network or to a model. A caller gives it a decision as text and gets
actions back, or runs a console item and gets the answers to the commands in it.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal

from tn_assist.apply import (
    Action,
    Say,
    apply_compaction,
    apply_contact_decision,
    parse_compaction,
    parse_decision,
)
from tn_assist.commands import authorize, is_read_only, parse_command
from tn_assist.config import load_config
from tn_assist.console import capture_text, run_command
from tn_assist.i18n import Lang, t
from tn_assist.memory import (
    Policy,
    compaction_chunk,
    needs_compaction,
    read_lines_at,
)
from tn_assist.paths import ContactKey, Workspace
from tn_assist.queue import WorkItem, complete, enqueue, mark_handled
from tn_assist.threads import thread_path


def _lang(ws: Workspace) -> Lang:
    return "en" if load_config(ws).get("lang") == "en" else "pt"


def queue_compaction(ws: Workspace, item: WorkItem, now: datetime) -> None:
    """When the transcript has outgrown its window, ask for a summary of the oldest part."""
    assert item.contact is not None
    key = ContactKey.parse(item.contact)
    policy = Policy.load(ws)
    if needs_compaction(ws, key, policy):
        chunk = compaction_chunk(ws, key, policy)
        if chunk:
            ids = (chunk[0].event_id, chunk[-1].event_id)
            enqueue(ws, WorkItem.new("compaction", item.contact, ids, now))


def apply_decision_text(ws: Workspace, item: WorkItem, raw: str, now: datetime) -> list[Action]:
    """A model's answer for ``item`` as actions; completes the item. Raises ``InvalidDecision``."""
    if item.kind == "compaction":
        apply_compaction(ws, item, parse_compaction(raw), now)
        complete(ws, item.id)
        return []
    role: Literal["contact", "admin", "attendant"] = item.kind
    decision = parse_decision(role, raw)
    actions: list[Action] = []
    if item.kind == "contact":
        auto = load_config(ws).get("mode") == "auto"
        actions = apply_contact_decision(ws, item, decision, now, mode="auto" if auto else "assist")
        queue_compaction(ws, item, now)
    else:
        console_role: Literal["admin", "attendant"] = (
            "admin" if item.kind == "admin" else "attendant"
        )
        actor = item.contact or "self"
        to = actor if item.kind == "admin" else "self"
        if decision.command:
            # The model read text written by customers. It may only run what changes nothing;
            # anything else goes back to the person as a command they must send themselves.
            cmd = parse_command(decision.command)
            if cmd is not None and authorize(cmd, console_role):
                if is_read_only(cmd):
                    result = run_command(ws, console_role, actor, cmd, now)
                    actions += [Say(to, result.text), *result.actions]
                else:
                    actions.append(Say(to, t("suggest_command", _lang(ws), command=cmd.raw)))
        if decision.reply:
            actions.append(Say(to, decision.reply))
    complete(ws, item.id)
    return actions


@dataclass
class ConsoleOutcome:
    actions: list[Action] = field(default_factory=list)
    needs_model: bool = False


def run_console_item(ws: Workspace, item: WorkItem, now: datetime) -> ConsoleOutcome:
    """Run each command line of an administrator or attendant item; free text is left to a model."""
    role: Literal["admin", "attendant"] = "admin" if item.kind == "admin" else "attendant"
    actor = item.contact or "self"
    to = actor if item.kind == "admin" else "self"
    lines = {ln.event_id: ln for ln in read_lines_at(thread_path(ws, item.kind, item.contact))}
    outcome = ConsoleOutcome()
    for event_id in item.event_ids:
        if event_id in item.handled_ids:
            continue
        line = lines.get(event_id)
        if line is None:
            mark_handled(ws, item.id, event_id)
            continue
        captured = capture_text(ws, actor, line.text, now) if item.kind == "admin" else None
        if captured is not None:
            outcome.actions.append(Say(to, captured.text))
            mark_handled(ws, item.id, event_id)
            continue
        cmd = parse_command(line.text)
        if cmd is None:
            outcome.needs_model = True
            continue
        result = run_command(ws, role, actor, cmd, now, message_id=line.message_id)
        outcome.actions += [Say(to, result.text), *result.actions]
        mark_handled(ws, item.id, event_id)
    if not outcome.needs_model:
        complete(ws, item.id)
    return outcome
