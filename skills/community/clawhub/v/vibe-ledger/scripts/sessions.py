"""Find the Claude Code and Codex sessions that belong to a project and turn
them into a compact, masked digest the rest of the pipeline reads.

The model never reads raw logs: only the digest, through the reading packs."""
from __future__ import annotations

import json
import os
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from common import ERROR_LINE, is_within, read_jsonl, write_jsonl
from redact import redact

TOOL_TEXT_LIMIT = 2000
EDIT_LIMIT = 1500
EDIT_TOOLS = {"Edit", "MultiEdit", "Write", "NotebookEdit"}
COMMAND_TOOLS = {"Bash"}
WRAPPER_PREFIXES = ("<task-notification", "<local-command-", "<command-name>", "<command-message>",
                    "<command-args>", "<system-reminder>", "<bash-input>", "<bash-stdout>",
                    "<bash-stderr>")


@dataclass
class Stats:
    files_scanned: int = 0
    files_parsed: int = 0
    files_matched: int = 0
    threads: int = 0
    records: int = 0
    bad_lines: int = 0
    compact_summaries: int = 0
    skipped_sessions: int = 0
    archived_threads: int = 0
    ignored_types: Counter = field(default_factory=Counter)
    by_agent: Counter = field(default_factory=Counter)
    earliest: str = ""
    latest: str = ""
    warnings: list = field(default_factory=list)

    def to_dict(self) -> dict:
        d = dict(self.__dict__)
        d["ignored_types"] = dict(self.ignored_types)
        d["by_agent"] = dict(self.by_agent)
        d["warnings"] = list(self.warnings)
        return d


def _rec(role: str, kind: str, text: str, files=(), old: str | None = None, new: str | None = None) -> dict:
    if not isinstance(text, str):
        raise TypeError("text must be a string")  # caught by the parsers and counted as malformed
    r = {"role": role, "kind": kind, "text": text, "files": [str(f) for f in files if f]}
    if old is not None:
        r["old"] = old[:EDIT_LIMIT]
    if new is not None:
        r["new"] = new[:EDIT_LIMIT]
    return r


def _content_text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(b.get("text", "") for b in content
                         if isinstance(b, dict) and b.get("type") == "text")
    return ""


def _claude_edit(name: str, inp: dict) -> dict:
    path = inp.get("file_path") or inp.get("notebook_path") or ""
    if name == "Write":
        new = inp.get("content", "")
        return _rec("assistant", "edit", f"WRITE {path}\n{new}"[:EDIT_LIMIT], [path], old="", new=new)
    if name == "MultiEdit":
        edits = inp.get("edits") or []
        old = "\n".join(e.get("old_string", "") for e in edits)
        new = "\n".join(e.get("new_string", "") for e in edits)
    elif name == "NotebookEdit":
        old, new = "", inp.get("new_source", "")
    else:
        old, new = inp.get("old_string", ""), inp.get("new_string", "")
    text = f"EDIT {path}\n--- before\n{old}\n+++ after\n{new}"
    return _rec("assistant", "edit", text[:EDIT_LIMIT], [path], old=old, new=new)


def _claude_blocks(obj: dict, tool_names: dict) -> list[dict]:
    typ = obj.get("type")
    content = (obj.get("message") or {}).get("content")
    if isinstance(content, str):
        blocks = [{"type": "text", "text": content}]
    else:
        blocks = [b for b in (content or []) if isinstance(b, dict)]
    out = []
    for b in blocks:
        bt = b.get("type")
        if typ == "user" and bt == "text":
            text = b.get("text") or ""
            if obj.get("isMeta") or not text.strip() or text.lstrip().startswith(WRAPPER_PREFIXES):
                continue
            out.append(_rec("user", "text", text))
        elif typ == "user" and bt == "tool_result":
            text = _content_text(b.get("content"))
            name = tool_names.get(b.get("tool_use_id"), "")
            if b.get("is_error") or (name in COMMAND_TOOLS and ERROR_LINE.search(text)):
                out.append(_rec("tool", "error", text[:TOOL_TEXT_LIMIT]))
        elif typ == "assistant" and bt == "text" and (b.get("text") or "").strip():
            out.append(_rec("assistant", "text", b["text"]))
        elif typ == "assistant" and bt == "tool_use":
            name, inp = b.get("name", ""), b.get("input") or {}
            tool_names[b.get("id")] = name
            if name in EDIT_TOOLS:
                out.append(_claude_edit(name, inp))
            elif name in COMMAND_TOOLS:
                out.append(_rec("assistant", "command", str(inp.get("command", ""))[:TOOL_TEXT_LIMIT]))
    return out


def parse_claude_file(path, stats: Stats) -> list[dict]:
    """One Claude Code transcript file -> digest records of one thread."""
    path = Path(path)
    is_sub = "subagents" in path.parts
    records: list[dict] = []
    tool_names: dict = {}
    for lineno, obj in read_jsonl(path):
        if obj is None:
            stats.bad_lines += 1
            continue
        typ = obj.get("type")
        if typ not in ("user", "assistant"):
            stats.ignored_types[f"claude:{typ}"] += 1
            continue
        if obj.get("isCompactSummary"):
            stats.compact_summaries += 1
            continue
        session = str(obj.get("sessionId") or path.stem)
        thread = f"{session}/{path.stem}" if is_sub else session
        uid = str(obj.get("uuid") or f"{path.name}:{lineno}")
        side = bool(obj.get("isSidechain")) or is_sub
        try:
            blocks = _claude_blocks(obj, tool_names)
        except (AttributeError, TypeError, KeyError, ValueError):
            stats.ignored_types["claude:malformed"] += 1  # an unexpected shape must not end the run
            continue
        for k, r in enumerate(blocks):
            if side and r["role"] == "user":
                r["role"] = "agent"
            r.update(id=uid if k == 0 else f"{uid}#{k}", session=thread, agent="claude-code",
                     ts=str(obj.get("timestamp") or ""), cwd=str(obj.get("cwd") or ""), sidechain=side)
            records.append(r)
    return records


GUARDIAN_PREFIX = "The following is the Codex agent history whose request action you are assessing"
_PATCH_FILE = re.compile(r"^\*\*\* (Add|Update|Delete) File: (.+)$", re.M)
_JS_CMD = re.compile(r'"cmd"\s*:\s*"((?:[^"\\]|\\.)*)"')
_EXIT = re.compile(r"(?:Process exited with code|Exit code:?)\s*(-?\d+)")
_SHELL_FUNCTIONS = {"exec_command", "shell", "local_shell", "container.exec"}


def _strip_file_url(cwd) -> str:
    if isinstance(cwd, str) and cwd.startswith("file://"):
        return cwd[len("file://"):]
    return cwd or ""


def _exit_code(value) -> int | None:
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return None


def _command_text(cmd) -> str:
    if isinstance(cmd, list):
        if len(cmd) >= 3 and cmd[1] in ("-lc", "-c"):
            return str(cmd[2])
        return " ".join(map(str, cmd))
    return str(cmd or "")


def _diff_sides(diff: str) -> tuple[str, str]:
    old, new = [], []
    for line in diff.splitlines():
        if line.startswith(("---", "+++", "@@", "***")):
            continue
        if line.startswith("-"):
            old.append(line[1:])
        elif line.startswith("+"):
            new.append(line[1:])
    return "\n".join(old), "\n".join(new)


def _change_rec(path: str, ch: dict) -> dict:
    kind = ch.get("type")
    if kind == "update":
        diff = ch.get("unified_diff") or ""
        old, new = _diff_sides(diff)
        text = f"EDIT {path}\n{diff}"
    elif kind == "add":
        old, new = "", ch.get("content") or ""
        text = f"WRITE {path}\n{new}"
    else:
        old, new = ch.get("content") or "", ""
        text = f"DELETE {path}"
    return _rec("assistant", "edit", text[:EDIT_LIMIT], [path], old=old, new=new)


def _changes(changes: dict, seen: set) -> list[dict]:
    out = []
    for path, ch in changes.items():
        if not isinstance(ch, dict):
            continue
        key = (path, ch.get("type"), ch.get("unified_diff") or ch.get("content") or "")
        if key in seen:
            continue
        seen.add(key)
        out.append(_change_rec(path, ch))
    return out


def _apply_patch_recs(patch: str) -> list[dict]:
    parts = _PATCH_FILE.split(patch)  # [before, op, path, body, op, path, body, ...]
    out = []
    for i in range(1, len(parts) - 2, 3):
        op, path, body = parts[i], parts[i + 1].strip(), parts[i + 2]
        old, new = _diff_sides(body)
        verb = "WRITE" if op == "Add" else op.upper()
        out.append(_rec("assistant", "edit", f"{verb} {path}\n{body.strip()}"[:EDIT_LIMIT], [path], old=old, new=new))
    return out


def _output_text(out) -> str:
    if isinstance(out, list):
        return "\n".join(str(b.get("text", "")) for b in out if isinstance(b, dict))
    if isinstance(out, str):
        try:
            j = json.loads(out)
        except json.JSONDecodeError:
            return out
        if isinstance(j, dict) and "output" in j:
            meta = j.get("metadata") if isinstance(j.get("metadata"), dict) else {}
            code = meta.get("exit_code")
            return str(j.get("output", "")) + (f"\nProcess exited with code {code}" if code is not None else "")
        return out
    return ""


def _fn_commands(p: dict) -> list[str]:
    name = p.get("name")
    if p.get("type") == "custom_tool_call" and name == "exec":
        out = []
        for m in _JS_CMD.finditer(p.get("input") or ""):
            try:
                out.append(json.loads('"' + m.group(1) + '"'))
            except json.JSONDecodeError:
                out.append(m.group(1))
        return out
    if p.get("type") == "function_call" and name in _SHELL_FUNCTIONS:
        try:
            args = json.loads(p.get("arguments") or "{}")
        except json.JSONDecodeError:
            return []
        cmd = args.get("cmd") or args.get("command") if isinstance(args, dict) else None
        return [_command_text(cmd)] if cmd else []
    return []


def _command_recs(p: dict, at_cwd: str) -> list[dict]:
    cwd = _strip_file_url(p.get("cwd")) or at_cwd
    out = [_rec("assistant", "command", _command_text(p.get("command"))[:TOOL_TEXT_LIMIT])]
    output = p.get("aggregated_output") or ((p.get("stdout") or "") + (p.get("stderr") or ""))
    code = _exit_code(p.get("exit_code"))
    if code not in (None, 0) or ERROR_LINE.search(output or ""):
        out.append(_rec("tool", "error", (output or f"exit code {code}")[:TOOL_TEXT_LIMIT]))
    for r in out:
        r["_cwd"] = cwd
    return out


def parse_codex_file(path, stats: Stats) -> list[dict]:
    """One Codex rollout file -> digest records of one thread ([] for skipped sessions)."""
    path = Path(path)
    session, cwd, side = path.stem, "", False
    events = []
    for lineno, obj in read_jsonl(path):
        if obj is None:
            stats.bad_lines += 1
            continue
        typ = obj.get("type")
        p = obj.get("payload") if isinstance(obj.get("payload"), dict) else {}
        if typ == "session_meta":
            session = p.get("id") or p.get("session_id") or session
            cwd = _strip_file_url(p.get("cwd")) or cwd
            src = p.get("source")
            if isinstance(src, dict) and "subagent" in src:
                sub = src["subagent"]
                if isinstance(sub, dict) and sub.get("other") == "guardian":
                    stats.skipped_sessions += 1
                    return []
                side = True
            continue
        if typ == "turn_context":
            cwd = _strip_file_url(p.get("cwd")) or cwd
            continue
        if typ == "compacted" or (typ == "event_msg" and p.get("type") == "context_compacted"):
            stats.compact_summaries += 1
            continue
        events.append((lineno, obj.get("timestamp", ""), cwd, typ, p))

    kinds = {(t, p.get("type")) for _, _, _, t, p in events}
    items = {p.get("item", {}).get("type") for _, _, _, t, p in events
             if t == "event_msg" and p.get("type") == "item_completed" and isinstance(p.get("item"), dict)}
    use_patch_end = ("event_msg", "patch_apply_end") in kinds
    use_filechange = "FileChange" in items
    use_patch_call = not (use_patch_end or use_filechange)
    use_item_cmd = "CommandExecution" in items
    use_exec_end = not use_item_cmd and ("event_msg", "exec_command_end") in kinds
    use_fn = not (use_item_cmd or use_exec_end)

    records: list[dict] = []
    seen: set = set()
    calls: dict = {}
    flags = (use_patch_end, use_filechange, use_patch_call, use_item_cmd, use_exec_end, use_fn)
    for lineno, ts, at_cwd, typ, p in events:
        try:
            new = _codex_event(typ, p, at_cwd, side, seen, calls, flags, stats)
        except _Skip:
            stats.skipped_sessions += 1
            return []
        except (AttributeError, TypeError, KeyError, ValueError):
            stats.ignored_types["codex:malformed"] += 1  # an unexpected shape must not end the run
            continue
        for k, r in enumerate(new):
            r.update(id=f"{path.name}:{lineno}" if k == 0 else f"{path.name}:{lineno}#{k}",
                     session=session, agent="codex", ts=str(ts or ""), cwd=r.pop("_cwd", at_cwd), sidechain=side)
            records.append(r)
    return records


class _Skip(Exception):
    """The session turned out to be an auto-review of another session."""


def _codex_event(typ, p, at_cwd, side, seen, calls, flags, stats) -> list[dict]:
    use_patch_end, use_filechange, use_patch_call, use_item_cmd, use_exec_end, use_fn = flags
    pt = p.get("type")
    new: list[dict] = []
    if typ == "event_msg" and pt == "user_message":
        text = p.get("message") or ""
        if text.startswith(GUARDIAN_PREFIX):
            raise _Skip
        if text.strip():
            new.append(_rec("agent" if side else "user", "text", text))
    elif typ == "event_msg" and pt == "agent_message":
        if (p.get("message") or "").strip():
            new.append(_rec("assistant", "text", p["message"]))
    elif typ == "event_msg" and pt == "patch_apply_end" and use_patch_end:
        new += _changes(p.get("changes") or {}, seen)
    elif typ == "event_msg" and pt == "item_completed" and isinstance(p.get("item"), dict):
        item = p["item"]
        if item.get("type") == "FileChange" and use_filechange:
            new += _changes(item.get("changes") or {}, seen)
        elif item.get("type") == "CommandExecution" and use_item_cmd:
            new += _command_recs(item, at_cwd)
    elif typ == "event_msg" and pt == "exec_command_end" and use_exec_end:
        new += _command_recs(p, at_cwd)
    elif typ == "response_item" and pt == "custom_tool_call" and p.get("name") == "apply_patch":
        if use_patch_call:
            new += _apply_patch_recs(p.get("input") or "")
    elif typ == "response_item" and use_fn and pt in ("function_call", "custom_tool_call"):
        cmds = _fn_commands(p)
        if cmds:
            calls[p.get("call_id")] = cmds
            new += [_rec("assistant", "command", c[:TOOL_TEXT_LIMIT]) for c in cmds]
    elif (typ == "response_item" and use_fn and pt in ("function_call_output", "custom_tool_call_output")
          and p.get("call_id") in calls):
        text = _output_text(p.get("output"))
        m = _EXIT.search(text)
        code = int(m.group(1)) if m else None
        if code not in (None, 0) or ERROR_LINE.search(text):
            new.append(_rec("tool", "error", text[:TOOL_TEXT_LIMIT]))
    else:
        stats.ignored_types[f"codex:{typ}/{pt}"] += 1
    return new


def default_claude_dir() -> Path:
    return Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude") / "projects"


def default_codex_dir() -> Path:
    return Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex") / "sessions"


def _number(records: list[dict]) -> None:
    """Order within the thread, user-turn numbers, absolute file paths."""
    turn = 0
    for i, r in enumerate(records):
        if r["role"] == "user":
            turn += 1
        r["seq"], r["turn"] = i, turn
        cwd = r.get("cwd") or ""
        r["files"] = [f if Path(f).is_absolute() or not cwd else str(Path(cwd) / f) for f in r["files"]]


_ANALYSIS = re.compile(r"\bvl\.py\s+(?:start|merge|check|render|shot)\b")
# vibe-ledger's own work files: a helper given one of these (a subagent writing explanations) is analysing,
# not building, even though it never runs vl.py itself
_ANALYSIS_FILES = re.compile(r"\b(?:explain_pack\.md|reading_pack_\d+\.md|requests_\d+\.md|(?:ledger|explain|requirements)\.verified\.json)\b")


def _before_analysis(records: list[dict]) -> list[dict]:
    """Records up to the first time vibe-ledger itself was run: analysing a project is not
    part of building it, and the analysis would otherwise be reported as build history."""
    for i, r in enumerate(records):
        if (r["kind"] == "command" and _ANALYSIS.search(r["text"])) or _ANALYSIS_FILES.search(r.get("text") or ""):
            return records[:i]
    return records


def _neutral_dirs() -> tuple[Path, ...]:
    """Folders an assistant works in that belong to no project: its own memory and session folders. (Not temp
    folders: a project can live there.)"""
    home = Path.home()
    return (home / ".claude" / "projects", home / ".codex")


def _claim(records: list[dict], root: Path) -> list[dict]:
    """The records of one thread that concern `root`; [] when the thread never touches it."""
    touches = any(is_within(f, root) for r in records for f in r["files"])
    if not touches and not any(is_within(r["cwd"], root) for r in records if r["cwd"]):
        return []
    for r in records:
        cwd = r["cwd"]
        r["in_project"] = ((bool(cwd) and is_within(cwd, root))
                           or any(is_within(f, root) for f in r["files"])
                           or (touches and bool(cwd) and is_within(root, cwd)))
    # What the user typed stays when the turn it starts works on this project, or when it was typed while the
    # assistant's folder had wandered somewhere neutral (its memory folder) and the thread was
    # last working here — a requirement must not be lost because the working folder moved. A message typed
    # from another project's folder whose turn never touches this one stays out.
    turn_hits = {r["turn"] for r in records if r["in_project"]}
    neutral = _neutral_dirs()
    here = False  # was the thread last working on this project?
    for r in records:
        cwd = r["cwd"]
        if r["role"] == "user" and r["kind"] == "text" and not r["in_project"]:
            wandered = bool(cwd) and any(is_within(cwd, d) for d in neutral)
            r["in_project"] = r["turn"] in turn_hits or (wandered and here)
        if cwd and not any(is_within(cwd, d) for d in neutral):
            here = is_within(cwd, root) or is_within(root, cwd)
        if any(is_within(f, root) for f in r["files"]):
            here = True
    return [r for r in records if r["in_project"]]


def _archive_name(thread: str) -> str:
    return re.sub(r"[^\w.-]+", "__", thread) + ".jsonl"


def load_archive(archive_dir) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    base = Path(archive_dir)
    if not base.is_dir():
        return out
    for f in sorted(base.glob("*.jsonl")):
        recs = [obj for _, obj in read_jsonl(f) if obj]
        if recs:
            out[recs[0]["session"]] = recs
    return out


def save_archive(archive_dir, threads: list[list[dict]]) -> None:
    for recs in threads:
        if recs:
            write_jsonl(Path(archive_dir) / _archive_name(recs[0]["session"]), recs)


def _log_files(claude_dir, codex_dir):
    for agent, base in (("claude-code", claude_dir), ("codex", codex_dir)):
        if base and Path(base).is_dir():
            for f in sorted(Path(base).rglob("*.jsonl")):
                yield agent, f


def collect(root, claude_dir=None, codex_dir=None, archive_dir=None) -> tuple[list[dict], Stats]:
    root = Path(root).resolve()
    stats = Stats()
    threads: dict[str, list[dict]] = {}
    # The folder name as a path segment ("/name/", "/name\"" …), raw or \u-escaped. Searched as
    # bytes with one cheap substring test first: logs run to gigabytes, and a bare mention such as
    # a memory-index line "name.md" must not force a full parse of every file.
    spellings = [n.encode("utf-8") for n in {root.name, json.dumps(root.name)[1:-1]}]
    quick = [b"/" + n for n in spellings]
    segment = re.compile(b"/(?:" + b"|".join(re.escape(n) for n in spellings) + rb")[/\"\\' \n]")
    full_path = str(root).encode("utf-8")
    stems: list[str] = []  # every log file name still on disk, to tell live threads from deleted ones
    for agent, f in _log_files(claude_dir, codex_dir):
        stems.append(f.stem)
        stats.files_scanned += 1
        try:
            data = f.read_bytes()
        except OSError as exc:
            stats.warnings.append(f"cannot read {f}: {exc}")
            continue
        if not any(q in data for q in quick) or not segment.search(data):
            continue
        stats.files_parsed += 1
        fstats = Stats()  # counted into the totals only if the file turns out to belong to the project
        recs = parse_claude_file(f, fstats) if agent == "claude-code" else parse_codex_file(f, fstats)
        if fstats.skipped_sessions:
            continue
        if not any(r["kind"] == "text" for r in recs) and full_path in data:
            stats.warnings.append(f"{f.name}: mentions this project but no messages could be read; "
                                  "the log format may have changed")
        if not recs:
            continue
        _number(recs)
        kept = _claim(_before_analysis(recs), root)
        if kept:
            stats.files_matched += 1
            stats.bad_lines += fstats.bad_lines
            stats.compact_summaries += fstats.compact_summaries
            stats.ignored_types.update(fstats.ignored_types)
            threads.setdefault(kept[0]["session"], []).extend(kept)
    if archive_dir:
        on_disk = "\n".join(stems)
        for thread, recs in load_archive(archive_dir).items():
            if thread in threads:
                continue
            if thread.split("/")[-1] in on_disk:
                # its log still exists and no longer counts for this project: drop the stale copy
                (Path(archive_dir) / _archive_name(thread)).unlink(missing_ok=True)
                continue
            threads[thread] = recs  # the original log was deleted (e.g. the 30-day cleanup)
            stats.archived_threads += 1
    ordered = sorted(threads.values(), key=lambda rs: min(r["ts"] for r in rs))
    out: list[dict] = []
    for recs in ordered:
        recs.sort(key=lambda r: (r["ts"], r["seq"]))
        for i, r in enumerate(recs):
            r["seq"] = i
            for key in ("text", "old", "new"):
                if key in r:
                    r[key] = redact(r[key])
        out.extend(recs)
    if archive_dir:
        save_archive(archive_dir, ordered)
    stats.threads, stats.records = len(ordered), len(out)
    stats.by_agent = Counter(rs[0]["agent"] for rs in ordered)
    stamps = [r["ts"] for r in out if r["ts"]]
    stats.earliest, stats.latest = (min(stamps), max(stamps)) if stamps else ("", "")
    return out, stats
