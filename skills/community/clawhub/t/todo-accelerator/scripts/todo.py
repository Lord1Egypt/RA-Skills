#!/usr/bin/env python3
"""
Todo Accelerator — manage to-do items via Obsidian Kanban board.

Subcommands:
  init         Validate board and create config
  add-todo     Create a new to-do with companion note
  work-on-todo Pick up a to-do by priority for processing
  commit       Check off completed requirements and finalize
  list-pending List all pending to-dos
"""

import argparse
import os
import random
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML required. Install: pip3 install PyYAML",
          file=sys.stderr)
    sys.exit(1)


# ── Config ───────────────────────────────────────────────────────────

def load_config(config_path: str) -> dict:
    """Load config and resolve all paths relative to its directory."""
    cfg_file = Path(config_path).resolve()
    if not cfg_file.exists():
        print(f"Error: config not found: {cfg_file}", file=sys.stderr)
        sys.exit(1)
    with open(cfg_file, encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    base = cfg_file.parent
    for key in ("board", "notes_folder", "template"):
        if key not in raw:
            print(f"Error: missing '{key}' in config", file=sys.stderr)
            sys.exit(1)
    return {
        "board": (base / raw["board"]).resolve(),
        "notes_folder": (base / raw["notes_folder"]).resolve(),
        "template": (base / raw["template"]).resolve(),
    }


def verify_kanban(board_path: Path) -> bool:
    """Return True if the file is a valid Obsidian Kanban board."""
    if not board_path.exists():
        return False
    return "kanban-plugin" in board_path.read_text(encoding="utf-8")


# ── Board helpers ────────────────────────────────────────────────────

CARD_RE = re.compile(r"^- \[([ x])\] \[\[(.+?)\]\]")


def find_heading_range(lines: list[str], heading: str) -> tuple[int, int] | None:
    """Return (start, end) indices for content under a ## heading."""
    pat = re.compile(r"^##\s+" + re.escape(heading) + r"\s*$")
    start = None
    for i, ln in enumerate(lines):
        if pat.match(ln):
            start = i + 1
            break
    if start is None:
        return None
    end = len(lines)
    for i in range(start, len(lines)):
        if (lines[i].startswith("## ")
                or lines[i].startswith("%% kanban:")
                or lines[i].strip() == "***"):
            end = i
            break
    return (start, end)


def cards_in_heading(lines: list[str], heading: str) -> list[dict]:
    """Extract cards from a heading section."""
    rng = find_heading_range(lines, heading)
    if rng is None:
        return []
    cards = []
    for i in range(rng[0], rng[1]):
        m = CARD_RE.match(lines[i].strip())
        if m:
            cards.append({
                "name": m.group(2),
                "checked": m.group(1) == "x",
                "line_idx": i,
            })
    return cards


def find_card_heading(board_path: Path, card_name: str,
                      search_headings: list[str]) -> str | None:
    """Find which heading a card is currently under."""
    lines = board_path.read_text(encoding="utf-8").splitlines()
    for heading in search_headings:
        for card in cards_in_heading(lines, heading):
            if card["name"] == card_name:
                return heading
    return None


def move_card(board_path: Path, card_name: str,
              from_heading: str, to_heading: str) -> None:
    """Move a card between headings on the board, adjusting checkbox state."""
    lines = board_path.read_text(encoding="utf-8").splitlines()

    # ── Find and remove from source ──
    src = find_heading_range(lines, from_heading)
    if src is None:
        print(f"Error: heading '{from_heading}' not found", file=sys.stderr)
        sys.exit(1)

    card_pat = re.compile(
        r"^- \[[ x]\] \[\[" + re.escape(card_name) + r"\]\]"
    )
    card_idx = None
    for i in range(src[0], src[1]):
        if card_pat.match(lines[i].strip()):
            card_idx = i
            break
    if card_idx is None:
        print(f"Error: [[{card_name}]] not found under '{from_heading}'",
              file=sys.stderr)
        sys.exit(1)

    card_line = lines.pop(card_idx)

    # ── Adjust checkbox ──
    if to_heading in ("Done", "Archive"):
        card_line = card_line.replace("- [ ]", "- [x]", 1)
    else:
        card_line = card_line.replace("- [x]", "- [ ]", 1)

    # ── Insert into target ──
    tgt = find_heading_range(lines, to_heading)
    if tgt is None:
        print(f"Error: heading '{to_heading}' not found", file=sys.stderr)
        sys.exit(1)

    if to_heading == "Done":
        insert = tgt[0]
        for i in range(tgt[0], tgt[1]):
            if lines[i].strip() == "**Complete**":
                insert = i + 1
                break
        else:
            while insert < tgt[1] and lines[insert].strip() == "":
                insert += 1
    else:
        insert = tgt[0]
        if insert < tgt[1] and lines[insert].strip() == "":
            insert += 1

    lines.insert(insert, card_line)
    board_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ── Note helpers ─────────────────────────────────────────────────────

INVESTIGATION_HEADINGS = (
    "Investigation and Problems",
    "Investigation and Thinking",
)


def parse_note(note_path: Path) -> tuple[dict, dict[str, str]]:
    """Parse a note into (frontmatter_dict, {section_heading: content})."""
    raw = note_path.read_text(encoding="utf-8")
    parts = raw.split("---", 2)
    if len(parts) >= 3 and parts[0].strip() == "":
        fm = yaml.safe_load(parts[1]) or {}
        body = parts[2]
    else:
        fm = {}
        body = raw

    sections: dict[str, str] = {}
    cur_heading = None
    cur_lines: list[str] = []
    for line in body.split("\n"):
        m = re.match(r"^#\s+(.+)", line)
        if m:
            if cur_heading is not None:
                sections[cur_heading] = "\n".join(cur_lines).strip()
            cur_heading = m.group(1).strip()
            cur_lines = []
        elif cur_heading is not None:
            cur_lines.append(line)
    if cur_heading is not None:
        sections[cur_heading] = "\n".join(cur_lines).strip()

    return fm, sections


def get_investigation_heading(sections: dict[str, str]) -> str | None:
    """Find whichever investigation heading variant exists in the note."""
    for h in INVESTIGATION_HEADINGS:
        if h in sections:
            return h
    return None


def _is_placeholder(line: str) -> bool:
    """True if a line is an italic placeholder like *Please write...*."""
    s = line.strip()
    return s.startswith("*") and s.endswith("*") and len(s) > 2


def _real_lines(text: str) -> list[str]:
    """Filter out blank lines and italic placeholder lines."""
    return [ln for ln in text.split("\n")
            if ln.strip() and not _is_placeholder(ln)]


def get_unchecked(sections: dict[str, str]) -> list[str]:
    """Get unchecked requirement text strings from What's More section."""
    whats_more = sections.get("What's More", "")
    result = []
    for line in whats_more.split("\n"):
        m = re.match(r"^-\s*\[ \]\s*(.+)", line.strip())
        if m:
            result.append(m.group(1).strip())
    return result


def update_note_frontmatter(note_path: Path, updates: dict) -> None:
    """Update specific fields in a note's YAML frontmatter."""
    raw = note_path.read_text(encoding="utf-8")
    parts = raw.split("---", 2)
    if len(parts) < 3 or parts[0].strip() != "":
        return
    fm = yaml.safe_load(parts[1]) or {}
    fm.update(updates)
    new_fm = yaml.dump(
        fm, default_flow_style=False, sort_keys=False, allow_unicode=True,
    )
    note_path.write_text(f"---\n{new_fm}---{parts[2]}", encoding="utf-8")


# ── cmd: init ────────────────────────────────────────────────────────

def _board_has_headings(board_path: Path) -> bool:
    """Return True if the board markdown contains any ## headings."""
    if not board_path.exists():
        return False
    for line in board_path.read_text(encoding="utf-8").splitlines():
        if re.match(r"^##\s+", line):
            return True
    return False


def cmd_init(args):
    """Validate board and create config file."""
    cfg_path = Path(args.config).resolve()

    if cfg_path.exists():
        print(f"Error: config already exists: {cfg_path}", file=sys.stderr)
        print("Delete the existing file first to reinitialize.",
              file=sys.stderr)
        sys.exit(1)

    board = Path(args.board).resolve()
    notes = Path(args.notes_folder).resolve()
    tmpl_dir = Path(args.template_dir).resolve()

    # ── Locate templates in the template directory ──
    if not tmpl_dir.is_dir():
        print(f"Error: template directory not found: {tmpl_dir}",
              file=sys.stderr)
        sys.exit(1)

    note_template = tmpl_dir / "note-template.md"
    board_template = tmpl_dir / "board-template.md"

    if not note_template.exists():
        print(f"Error: note-template.md not found in {tmpl_dir}",
              file=sys.stderr)
        sys.exit(1)
    if not board_template.exists():
        print(f"Error: board-template.md not found in {tmpl_dir}",
              file=sys.stderr)
        sys.exit(1)

    # ── Board: check emptiness and set up ──
    if board.exists() and _board_has_headings(board):
        print(
            f"Error: board '{board}' is not empty (contains headings). "
            "Cannot initialize a board that already has data.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Copy board template to the board path
    board.parent.mkdir(parents=True, exist_ok=True)
    board.write_text(
        board_template.read_text(encoding="utf-8"), encoding="utf-8",
    )

    if not verify_kanban(board):
        print(
            f"Error: '{board}' is not a valid Obsidian Kanban board "
            "(missing kanban-plugin identifier).",
            file=sys.stderr,
        )
        sys.exit(1)

    notes.mkdir(parents=True, exist_ok=True)

    base = cfg_path.parent
    base.mkdir(parents=True, exist_ok=True)
    cfg = {
        "board": os.path.relpath(str(board), str(base)),
        "notes_folder": os.path.relpath(str(notes), str(base)),
        "template": os.path.relpath(str(note_template), str(base)),
    }
    with open(cfg_path, "w", encoding="utf-8") as f:
        yaml.dump(cfg, f, default_flow_style=False, allow_unicode=True)

    print(f"Initialized: {cfg_path}")
    print(f"  board: {cfg['board']}")
    print(f"  notes_folder: {cfg['notes_folder']}")
    print(f"  template: {cfg['template']}")


# ── cmd: add-todo ────────────────────────────────────────────────────

def cmd_add_todo(args, config):
    """Create a new to-do: companion note + card in Ideas."""
    board_path = config["board"]
    notes_dir = config["notes_folder"]
    tmpl_path = config["template"]
    name = args.name

    if not board_path.exists():
        print(f"Error: board not found: {board_path}", file=sys.stderr)
        sys.exit(1)
    if not tmpl_path.exists():
        print(f"Error: template not found: {tmpl_path}", file=sys.stderr)
        sys.exit(1)

    template = tmpl_path.read_text(encoding="utf-8")

    # Build substitutions
    targets = args.targets or ["你期待的结果1", "你期待的结果2"]
    reqs = args.requirements or ["example question / requirement"]

    targets_yaml = "\n".join(f"  - {t}" for t in targets)
    reqs_md = "\n".join(f"- [ ] {r}" for r in reqs)
    now = datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")

    content = template
    content = content.replace("{{targets}}", targets_yaml)
    content = content.replace("{{requirements}}", reqs_md)
    content = content.replace("{{created_at}}", now)

    # Write companion note
    notes_dir.mkdir(parents=True, exist_ok=True)
    note_path = notes_dir / f"{name}.md"
    if note_path.exists():
        print(f"Note already exists: {note_path} (skipped)")
    else:
        note_path.write_text(content, encoding="utf-8")
        print(f"Created note: {note_path}")

    # Set priority and subagent if specified
    fm_updates = {}
    if args.priority and args.priority != 0:
        fm_updates["priority"] = args.priority
    if args.allow_subagent is not None:
        fm_updates["allow-subagent"] = args.allow_subagent
    if args.assigned_agent is not None:
        fm_updates["assigned-agent"] = args.assigned_agent
    if fm_updates:
        update_note_frontmatter(note_path, fm_updates)

    # Insert card under Ideas
    lines = board_path.read_text(encoding="utf-8").splitlines(keepends=True)
    plain = [ln.rstrip("\n") for ln in lines]

    pat = re.compile(r"^##\s+Ideas\s*$")
    idx = None
    for i, ln in enumerate(plain):
        if pat.match(ln):
            idx = i + 1
            break
    if idx is None:
        print("Error: '## Ideas' not found in board", file=sys.stderr)
        sys.exit(1)
    if idx < len(plain) and plain[idx].strip() == "":
        idx += 1

    lines.insert(idx, f"- [ ] [[{name}]]\n")
    board_path.write_text("".join(lines), encoding="utf-8")
    print(f"Added to-do: [[{name}]]")


# ── cmd: work-on-todo ───────────────────────────────────────────────

def cmd_work_on_todo(args, config):
    """Select a to-do from Ideas by priority, prepare for processing."""
    board_path = config["board"]
    notes_dir = config["notes_folder"]

    if not board_path.exists():
        print(f"Error: board not found: {board_path}", file=sys.stderr)
        sys.exit(1)

    lines = board_path.read_text(encoding="utf-8").splitlines()

    # ── Only select from Ideas ──
    candidates = []
    for card in cards_in_heading(lines, "Ideas"):
        note_path = notes_dir / f"{card['name']}.md"
        priority = 0
        if note_path.exists():
            fm, _ = parse_note(note_path)
            priority = fm.get("priority", 0) or 0
        candidates.append({
            "name": card["name"],
            "priority": priority,
            "note_path": note_path,
        })

    if not candidates:
        print("No pending to-dos in Ideas.")
        sys.exit(0)

    # ── Select ──
    if args.name:
        match = [c for c in candidates if c["name"] == args.name]
        if not match:
            avail = ", ".join(c["name"] for c in candidates)
            print(f"Error: '{args.name}' not found in Ideas. Available: {avail}",
                  file=sys.stderr)
            sys.exit(1)
        selected = match[0]
    else:
        max_p = max(c["priority"] for c in candidates)
        top = [c for c in candidates if c["priority"] == max_p]
        selected = random.choice(top)

    note_path = selected["note_path"]
    if not note_path.exists():
        print(f"Error: note not found: {note_path}", file=sys.stderr)
        sys.exit(1)

    fm, sections = parse_note(note_path)
    unchecked = get_unchecked(sections)

    # ── If no unchecked requirements → move to 审阅中 and skip ──
    if not unchecked:
        move_card(board_path, selected["name"], "Ideas", "审阅中")
        print(f"[[{selected['name']}]] has no unresolved requirements.")
        print("Moved to 审阅中 for review. No action needed this round.")
        sys.exit(0)

    # ── Move from Ideas → 推进中 ──
    move_card(board_path, selected["name"], "Ideas", "推进中")

    # ── Update frontmatter: increment iterate, set iteration-started-at ──
    new_iterate = (fm.get("iterate", 0) or 0) + 1
    now = datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")
    update_note_frontmatter(note_path, {
        "iterate": new_iterate,
        "iteration-started-at": now,
    })

    # ── Build output (data fields only; instructions are in SKILL.md) ──
    target_lines = _real_lines(sections.get("Target", ""))
    inv_heading = get_investigation_heading(sections)
    inv_lines = _real_lines(
        sections.get(inv_heading, "")
    ) if inv_heading else []

    out: list[str] = []
    out.append(f"## Working on: {selected['name']}")
    out.append(f"Note: {note_path}")
    out.append(f"Iteration: {new_iterate}")
    out.append("")

    targets = fm.get("target") or []
    if isinstance(targets, str):
        targets = [targets]
    if targets:
        out.append("### Expected Results")
        for t in targets:
            out.append(f"- {t}")
        out.append("")

    out.append("### Unresolved Issues")
    for item in unchecked:
        out.append(f"- [ ] {item}")
    out.append("")

    if target_lines:
        out.append("### Previous Results")
        for ln in target_lines:
            out.append(ln)
        out.append("")

    inv_name = inv_heading or "Investigation and Problems"
    if inv_lines:
        out.append(
            f"Previous findings are in the \"{inv_name}\" section of the note. "
            "Review before starting; record any new discoveries in the same section. "
            "Keep entries concise — facts and conclusions only, no filler."
        )
        out.append("")

    assigned_agent = fm.get("assigned-agent")
    if assigned_agent:
        out.insert(0, (
            f"⚠️ DELEGATION REQUIRED: This to-do is assigned to agent "
            f"\"{assigned_agent}\". Notify agent \"{assigned_agent}\" and "
            f"pass the task details below to it. The agent must follow the "
            f"todo-accelerator skill workflow to process this to-do."
        ))
        out.insert(1, "")

    allow_subagent = fm.get("allow-subagent", True)
    if allow_subagent and not assigned_agent:
        out.append(
            "You are permitted to delegate this task to a subagent. "
            "The choice of model is at your discretion."
        )
        out.append("")

    print("\n".join(out))


# ── cmd: commit ──────────────────────────────────────────────────────

def cmd_commit(args, config):
    """Check off completed requirements and move card to 审阅中."""
    notes_dir = config["notes_folder"]
    board_path = config["board"]
    name = args.name
    completed = args.completed or []

    note_path = notes_dir / f"{name}.md"
    if not note_path.exists():
        print(f"Error: note not found: {note_path}", file=sys.stderr)
        sys.exit(1)

    _, sections = parse_note(note_path)
    unchecked = get_unchecked(sections)

    # ── Validate: must provide at least one completed item ──
    if not completed:
        print("Error: no completed requirements provided.", file=sys.stderr)
        print("", file=sys.stderr)
        print("Remaining unchecked requirements:", file=sys.stderr)
        for item in unchecked:
            print(f"  - [ ] {item}", file=sys.stderr)
        print("", file=sys.stderr)
        print("Pass the exact requirement string(s) you completed "
              "as arguments to --completed.", file=sys.stderr)
        sys.exit(1)

    # ── Validate: each string must match an unchecked requirement ──
    invalid = [c for c in completed if c not in unchecked]
    if invalid:
        print("Error: these do not match any unchecked requirement:",
              file=sys.stderr)
        for item in invalid:
            print(f"  '{item}'", file=sys.stderr)
        print("", file=sys.stderr)
        print("Remaining unchecked requirements:", file=sys.stderr)
        for item in unchecked:
            print(f"  - [ ] {item}", file=sys.stderr)
        print("", file=sys.stderr)
        print("Pass the exact requirement string(s) you completed.",
              file=sys.stderr)
        sys.exit(1)

    # ── Check off completed items in note ──
    raw = note_path.read_text(encoding="utf-8")
    for item in completed:
        raw = raw.replace(f"- [ ] {item}", f"- [x] {item}", 1)
    note_path.write_text(raw, encoding="utf-8")

    # ── Move card to 审阅中 ──
    current = find_card_heading(board_path, name, ["推进中", "Ideas"])
    if current:
        move_card(board_path, name, current, "审阅中")

    remaining = [u for u in unchecked if u not in completed]
    print(f"Committed: checked off {len(completed)} requirement(s).")
    print(f"Moved [[{name}]] to 审阅中.")
    if remaining:
        print(f"\nRemaining unchecked ({len(remaining)}):")
        for item in remaining:
            print(f"  - [ ] {item}")


# ── cmd: list-pending ────────────────────────────────────────────────

def cmd_list_pending(args, config):
    """List all pending to-dos under Ideas."""
    board_path = config["board"]
    notes_dir = config["notes_folder"]

    if not board_path.exists():
        print(f"Error: board not found: {board_path}", file=sys.stderr)
        sys.exit(1)

    lines = board_path.read_text(encoding="utf-8").splitlines()
    cards = cards_in_heading(lines, "Ideas")

    if not cards:
        print("No pending to-dos in Ideas.")
        return

    print("Pending to-dos (Ideas):")
    for card in cards:
        note_path = notes_dir / f"{card['name']}.md"
        priority = 0
        if note_path.exists():
            fm, _ = parse_note(note_path)
            priority = fm.get("priority", 0) or 0
        print(f"  - {card['name']} (priority: {priority})")


# ── Main ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Todo Accelerator")
    parser.add_argument(
        "--config", required=True,
        help="Path to todo-accelerator-config.yaml",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # init
    p_init = sub.add_parser("init", help="Validate board and create config")
    p_init.add_argument("--board", required=True,
                        help="Kanban board .md file")
    p_init.add_argument("--notes-folder", required=True,
                        help="Folder for companion notes")
    p_init.add_argument("--template-dir", required=True,
                        help="Directory containing note-template.md and board-template.md")

    # add-todo
    p_add = sub.add_parser("add-todo", help="Create a new to-do")
    p_add.add_argument("--name", required=True, help="To-do title")
    p_add.add_argument("--targets", nargs="*", help="Target outcomes")
    p_add.add_argument("--requirements", nargs="*",
                       help="Requirements / questions")
    p_add.add_argument("--priority", type=int, default=0,
                       help="Priority level (0=normal, higher=more urgent)")
    p_add.add_argument("--allow-subagent", action=argparse.BooleanOptionalAction,
                       default=None,
                       help="Allow subagent delegation (default: true in template)")
    p_add.add_argument("--assigned-agent", default=None,
                       help="Agent ID that must handle this to-do (delegates instead of self-processing)")

    # work-on-todo
    p_work = sub.add_parser("work-on-todo", help="Pick up a to-do")
    p_work.add_argument("--name", help="Specific to-do name (optional)")

    # commit
    p_commit = sub.add_parser("commit", help="Finalize a round of work")
    p_commit.add_argument("--name", required=True, help="To-do name")
    p_commit.add_argument("--completed", nargs="*",
                          help="Completed requirement strings (exact match)")

    # list-pending
    sub.add_parser("list-pending", help="List pending to-dos in Ideas")

    args = parser.parse_args()

    if args.command == "init":
        cmd_init(args)
    else:
        config = load_config(args.config)
        if args.command == "add-todo":
            cmd_add_todo(args, config)
        elif args.command == "work-on-todo":
            cmd_work_on_todo(args, config)
        elif args.command == "commit":
            cmd_commit(args, config)
        elif args.command == "list-pending":
            cmd_list_pending(args, config)


if __name__ == "__main__":
    main()
