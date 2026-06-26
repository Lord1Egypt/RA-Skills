#!/usr/bin/env python3
"""
zk.py — Zettelkasten CLI Tool
Based on the Desktop Commander / Obsidian Zettelkasten method:
  - Fleeting notes  → 00-Inbox/
  - Literature notes → 10-Literature/
  - Permanent notes  → 20-Permanent/
  - Maps of Content  → 30-MOC/
  - Templates        → 40-Templates/
"""

import argparse
import datetime
import os
import re
import sys
from pathlib import Path
from collections import defaultdict

# ── Config ──────────────────────────────────────────────────────────────────

DEFAULT_VAULT = Path.home() / "Zettelkasten"

FOLDERS = {
    "inbox":      "00-Inbox",
    "literature": "10-Literature",
    "permanent":  "20-Permanent",
    "moc":        "30-MOC",
    "templates":  "40-Templates",
}

COLORS = {
    "reset":   "\033[0m",
    "bold":    "\033[1m",
    "cyan":    "\033[96m",
    "green":   "\033[92m",
    "yellow":  "\033[93m",
    "red":     "\033[91m",
    "magenta": "\033[95m",
    "blue":    "\033[94m",
    "dim":     "\033[2m",
}

def c(color, text):
    """Colorize text."""
    if not sys.stdout.isatty():
        return text
    return f"{COLORS.get(color,'')}{text}{COLORS['reset']}"

# ── Vault helpers ────────────────────────────────────────────────────────────

def get_vault(args) -> Path:
    vault = Path(getattr(args, "vault", None) or os.environ.get("ZK_VAULT", DEFAULT_VAULT))
    return vault

def init_vault(vault: Path):
    """Create vault folder structure if it doesn't exist."""
    for folder in FOLDERS.values():
        (vault / folder).mkdir(parents=True, exist_ok=True)
    # Write default templates
    _write_templates(vault)

def _write_templates(vault: Path):
    tdir = vault / FOLDERS["templates"]

    fleeting = tdir / "fleeting.md"
    if not fleeting.exists():
        fleeting.write_text(
            "---\n"
            "created: {{date}}\n"
            "status: fleeting\n"
            "---\n\n"
            "[Raw capture — one or two sentences. Don't overthink it.]\n"
        )

    literature = tdir / "literature.md"
    if not literature.exists():
        literature.write_text(
            "---\n"
            "created: {{date}}\n"
            "status: literature\n"
            "source: \n"
            "author: \n"
            "tags: []\n"
            "---\n\n"
            "# [Source title]\n\n"
            "## Key ideas\n\n"
            "[What from this source matters to me, and why?]\n\n"
            "## Quotes worth keeping\n\n"
            "## Raw notes\n"
        )

    permanent = tdir / "permanent.md"
    if not permanent.exists():
        permanent.write_text(
            "---\n"
            "created: {{date}}\n"
            "status: permanent\n"
            "tags: []\n"
            "source: \n"
            "---\n\n"
            "# [Claim written as a full sentence]\n\n"
            "[Main idea — 3 to 5 sentences. Written so that\n"
            "you'd understand it with zero context, years from now.]\n\n"
            "## Connections\n"
            "- [[Related note 1]]\n"
            "- [[Related note 2]]\n\n"
            "## Source\n"
            "[Where this idea came from]\n"
        )

    moc = tdir / "moc.md"
    if not moc.exists():
        moc.write_text(
            "---\n"
            "created: {{date}}\n"
            "status: moc\n"
            "tags: []\n"
            "---\n\n"
            "# MOC: [Topic]\n\n"
            "> A Map of Content for navigating notes on [topic].\n\n"
            "## Core notes\n"
            "- [[Note 1]]\n"
            "- [[Note 2]]\n\n"
            "## Subtopics\n\n"
            "## See also\n"
        )

def _now_str() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d")

def _timestamp_id() -> str:
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")

def _fill_template(template_path: Path) -> str:
    text = template_path.read_text()
    return text.replace("{{date}}", _now_str())

def _slugify(title: str) -> str:
    slug = title.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug[:80]

def _all_md_files(vault: Path):
    return list(vault.rglob("*.md"))

def _extract_links(text: str):
    """Return set of [[link]] targets found in text."""
    return set(re.findall(r"\[\[([^\[\]|#]+?)(?:\|[^\[\]]+)?\]\]", text))

def _extract_tags(text: str):
    return set(re.findall(r"(?:^|\s)#([\w/-]+)", text))

def _frontmatter_value(text: str, key: str) -> str:
    m = re.search(rf"^{key}:\s*(.+)$", text, re.MULTILINE)
    return m.group(1).strip() if m else ""

def _note_title(path: Path, text: str) -> str:
    m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return path.stem

def _open_in_editor(path: Path):
    editor = os.environ.get("EDITOR", "nano")
    os.system(f'{editor} "{path}"')

# ── Commands ─────────────────────────────────────────────────────────────────

def cmd_init(args):
    vault = get_vault(args)
    init_vault(vault)
    print(c("green", f"✓ Vault initialised at {vault}"))
    for key, folder in FOLDERS.items():
        print(f"  {c('dim', '→')} {vault / folder}")


def cmd_new(args):
    vault = get_vault(args)
    init_vault(vault)

    note_type = args.type  # fleeting | literature | permanent | moc
    title = " ".join(args.title) if args.title else None

    folder_key = note_type if note_type != "fleeting" else "inbox"
    folder = vault / FOLDERS[folder_key]
    template_path = vault / FOLDERS["templates"] / f"{note_type}.md"

    if not template_path.exists():
        _write_templates(vault)

    content = _fill_template(template_path)

    if title:
        slug = _slugify(title)
        filename = f"{_now_str()}-{slug}.md"
        # Replace generic title in template
        content = content.replace("[Source title]", title)
        content = content.replace("[Claim written as a full sentence]", title)
        content = content.replace("MOC: [Topic]", f"MOC: {title}")
    else:
        filename = f"{_timestamp_id()}.md"

    note_path = folder / filename

    if note_path.exists():
        print(c("yellow", f"Note already exists: {note_path}"))
    else:
        note_path.write_text(content)
        print(c("green", f"✓ Created [{note_type}] → {note_path.relative_to(vault)}"))

    if not args.no_edit:
        _open_in_editor(note_path)


def cmd_list(args):
    vault = get_vault(args)
    folder_key = args.folder or None

    if folder_key and folder_key not in FOLDERS:
        print(c("red", f"Unknown folder key. Choose from: {', '.join(FOLDERS.keys())}"))
        sys.exit(1)

    folders_to_scan = (
        [vault / FOLDERS[folder_key]] if folder_key
        else [vault / f for f in FOLDERS.values()]
    )

    tag_filter = args.tag.lstrip("#") if args.tag else None
    query = args.query.lower() if args.query else None
    total = 0

    for folder in folders_to_scan:
        files = sorted(folder.glob("*.md")) if folder.exists() else []
        if not files:
            continue
        label = folder.name
        printed_header = False
        for f in files:
            text = f.read_text(errors="replace")
            if tag_filter and tag_filter not in _extract_tags(text):
                continue
            if query and query not in text.lower():
                continue
            if not printed_header:
                print(f"\n{c('cyan', c('bold', label))}")
                printed_header = True
            title = _note_title(f, text)
            status = _frontmatter_value(text, "status")
            tags = " ".join(f"#{t}" for t in sorted(_extract_tags(text)))
            links_count = len(_extract_links(text))
            date_str = _frontmatter_value(text, "created") or ""
            print(
                f"  {c('dim', date_str)}  "
                f"{c('bold', title[:55]):<58} "
                f"{c('blue', f'🔗{links_count}'):>6}  "
                f"{c('magenta', tags[:30])}"
            )
            total += 1

    print(f"\n{c('dim', f'{total} notes found')}")


def cmd_search(args):
    vault = get_vault(args)
    query = " ".join(args.query).lower()
    files = _all_md_files(vault)
    results = []

    for f in files:
        text = f.read_text(errors="replace")
        if query in text.lower():
            # Find matching lines
            lines = [
                (i + 1, l.strip())
                for i, l in enumerate(text.splitlines())
                if query in l.lower()
            ]
            results.append((f, _note_title(f, text), lines))

    if not results:
        print(c("yellow", f"No results for '{query}'"))
        return

    print(f"\n{c('bold', f'Search: \"{query}\"')} — {len(results)} note(s)\n")
    for path, title, lines in results:
        rel = path.relative_to(vault)
        print(f"  {c('cyan', str(rel))}")
        print(f"  {c('bold', title)}")
        for lineno, line in lines[:3]:
            highlighted = re.sub(
                re.escape(query),
                c("yellow", query),
                line,
                flags=re.IGNORECASE,
            )
            print(f"    {c('dim', str(lineno) + ':')} {highlighted}")
        print()


def cmd_links(args):
    vault = get_vault(args)
    files = _all_md_files(vault)

    # Build index: note stem → Path
    note_index = {f.stem: f for f in files}
    # Build forward links
    forward: dict[str, set] = {}
    backward: dict[str, set] = defaultdict(set)

    for f in files:
        text = f.read_text(errors="replace")
        targets = _extract_links(text)
        forward[f.stem] = targets
        for t in targets:
            # Normalize: match by stem
            matched = next(
                (k for k in note_index if k.lower() == t.lower()), t
            )
            backward[matched].add(f.stem)

    target = " ".join(args.note) if args.note else None

    if target:
        # Show links for a specific note
        stem = _slugify(target) if target not in note_index else target
        stem = next((k for k in note_index if k.lower() == target.lower()), target)
        fwd = forward.get(stem, set())
        bck = backward.get(stem, set())
        print(f"\n{c('bold', stem)}")
        print(f"  {c('cyan', 'Outgoing links')} ({len(fwd)}):")
        for l in sorted(fwd):
            exists = "✓" if l in note_index or l.lower() in (k.lower() for k in note_index) else c("red", "✗ missing")
            print(f"    → [[{l}]] {exists}")
        print(f"  {c('green', 'Incoming links')} ({len(bck)}):")
        for l in sorted(bck):
            print(f"    ← [[{l}]]")
    else:
        # Show orphaned notes
        orphans = [
            stem for stem, fwd in forward.items()
            if not fwd and not backward.get(stem)
            and not (vault / FOLDERS["templates"]).name in str(note_index.get(stem, ""))
        ]
        print(f"\n{c('bold', 'Orphaned notes')} (no links in or out): {len(orphans)}\n")
        for stem in sorted(orphans):
            path = note_index.get(stem)
            if path:
                rel = path.relative_to(vault)
                text = path.read_text(errors="replace")
                first_line = next(
                    (l.strip() for l in text.splitlines() if l.strip() and not l.startswith("---") and not l.startswith("#")),
                    ""
                )
                print(f"  {c('yellow', '⚠')} {c('cyan', str(rel))}")
                if first_line:
                    print(f"    {c('dim', first_line[:80])}")


def cmd_graph(args):
    """Print an ASCII link graph of the vault."""
    vault = get_vault(args)
    files = _all_md_files(vault)
    note_index = {f.stem: f for f in files}

    forward: dict[str, set] = {}
    for f in files:
        text = f.read_text(errors="replace")
        forward[f.stem] = _extract_links(text)

    # Filter out templates folder
    tpl_folder = vault / FOLDERS["templates"]
    stems = [
        s for s, p in note_index.items()
        if not str(p).startswith(str(tpl_folder))
    ]

    if not stems:
        print(c("yellow", "No notes found."))
        return

    print(f"\n{c('bold', 'Vault Link Graph')}\n")
    for stem in sorted(stems):
        path = note_index[stem]
        rel = path.relative_to(vault)
        targets = forward.get(stem, set())
        folder_label = c("dim", f"[{rel.parent.name}]")
        print(f"  {folder_label} {c('bold', stem)}")
        for t in sorted(targets):
            exists = t in note_index or any(k.lower() == t.lower() for k in note_index)
            sym = c("green", "→") if exists else c("red", "⇢?")
            print(f"      {sym} {t}")


def cmd_stats(args):
    vault = get_vault(args)
    files = _all_md_files(vault)
    tpl_folder = vault / FOLDERS["templates"]
    notes = [f for f in files if not str(f).startswith(str(tpl_folder))]

    counts_by_folder: dict[str, int] = defaultdict(int)
    all_tags: dict[str, int] = defaultdict(int)
    total_links = 0
    orphans = 0

    forward: dict[str, set] = {}
    backward: dict[str, set] = defaultdict(set)

    for f in notes:
        text = f.read_text(errors="replace")
        folder = f.parent.name
        counts_by_folder[folder] += 1
        targets = _extract_links(text)
        forward[f.stem] = targets
        total_links += len(targets)
        for t in targets:
            backward[t].add(f.stem)
        for tag in _extract_tags(text):
            all_tags[tag] += 1

    for stem, fwd in forward.items():
        if not fwd and not backward.get(stem):
            orphans += 1

    top_tags = sorted(all_tags.items(), key=lambda x: -x[1])[:10]

    print(f"\n{c('bold', 'Vault Statistics')}\n")
    print(f"  {'Total notes':<25} {c('cyan', str(len(notes)))}")
    print(f"  {'Total [[links]]':<25} {c('cyan', str(total_links))}")
    print(f"  {'Orphaned notes':<25} {c('yellow', str(orphans))}")
    print()
    print(c("bold", "  Notes by folder:"))
    for folder, count in sorted(counts_by_folder.items()):
        bar = "█" * min(count, 40)
        print(f"  {folder:<30} {c('blue', bar)} {count}")
    if top_tags:
        print()
        print(c("bold", "  Top tags:"))
        for tag, count in top_tags:
            print(f"  #{tag:<28} {count}")


def cmd_inbox(args):
    """Review inbox: list fleeting notes, optionally promote one."""
    vault = get_vault(args)
    inbox = vault / FOLDERS["inbox"]
    files = sorted(inbox.glob("*.md")) if inbox.exists() else []

    if not files:
        print(c("green", "✓ Inbox is empty — nothing to process."))
        return

    now = datetime.datetime.now()
    print(f"\n{c('bold', 'Inbox Review')} — {len(files)} note(s)\n")

    old_count = 0
    for f in files:
        text = f.read_text(errors="replace")
        title = _note_title(f, text)
        created_str = _frontmatter_value(text, "created")
        age_label = ""
        if created_str:
            try:
                created = datetime.datetime.strptime(created_str, "%Y-%m-%d")
                age_days = (now - created).days
                if age_days > 7:
                    age_label = c("red", f" ⚠ {age_days}d old")
                    old_count += 1
                else:
                    age_label = c("dim", f" ({age_days}d)")
            except ValueError:
                pass
        print(f"  {c('yellow', '→')} {c('bold', title[:60])}{age_label}")
        print(f"    {c('dim', str(f.relative_to(vault)))}")

    if old_count:
        print(f"\n{c('yellow', f'⚠ {old_count} note(s) older than 7 days — consider processing them.')}")
    print(f"\n{c('dim', 'Tip: use `zk new permanent` to promote a fleeting note.')}")


def cmd_promote(args):
    """Promote a fleeting/literature note to permanent."""
    vault = get_vault(args)
    query = " ".join(args.note).lower()

    candidates = []
    for folder_key in ("inbox", "literature"):
        folder = vault / FOLDERS[folder_key]
        if folder.exists():
            for f in folder.glob("*.md"):
                if query in f.name.lower() or query in f.read_text(errors="replace").lower():
                    candidates.append(f)

    if not candidates:
        print(c("yellow", f"No matching notes found for '{query}' in Inbox or Literature."))
        return

    if len(candidates) > 1:
        print(c("yellow", f"Multiple matches found:"))
        for i, f in enumerate(candidates):
            print(f"  [{i}] {f.relative_to(vault)}")
        choice = input("Choose [0]: ").strip() or "0"
        source = candidates[int(choice)]
    else:
        source = candidates[0]

    # Build new permanent note
    template_path = vault / FOLDERS["templates"] / "permanent.md"
    content = _fill_template(template_path)

    # Embed original content as source reference
    orig_title = _note_title(source, source.read_text(errors="replace"))
    perm_folder = vault / FOLDERS["permanent"]
    slug = _slugify(orig_title)
    dest = perm_folder / f"{_now_str()}-{slug}.md"
    content = content.replace("[Claim written as a full sentence]", orig_title)
    content += f"\n\n---\n*Promoted from [[{source.stem}]]*\n"
    dest.write_text(content)
    print(c("green", f"✓ Promoted → {dest.relative_to(vault)}"))
    if not args.no_edit:
        _open_in_editor(dest)


def cmd_moc(args):
    """Generate or update a Map of Content for a topic/tag."""
    vault = get_vault(args)
    topic = " ".join(args.topic)
    tag_filter = _slugify(topic).replace("-", "")  # rough tag match

    files = _all_md_files(vault)
    tpl_folder = vault / FOLDERS["templates"]
    relevant = []

    for f in files:
        if str(f).startswith(str(tpl_folder)):
            continue
        text = f.read_text(errors="replace")
        tags = _extract_tags(text)
        title = _note_title(f, text)
        if (
            topic.lower() in text.lower()
            or any(tag_filter in t.lower() for t in tags)
        ):
            relevant.append((f, title))

    if not relevant:
        print(c("yellow", f"No notes found related to '{topic}'."))
        return

    # Build MOC content
    lines = [
        "---",
        f"created: {_now_str()}",
        "status: moc",
        f"tags: [{_slugify(topic)}]",
        "---",
        "",
        f"# MOC: {topic}",
        "",
        f"> Auto-generated Map of Content for **{topic}**.",
        "",
        "## Notes",
        "",
    ]
    for path, title in sorted(relevant, key=lambda x: x[1].lower()):
        lines.append(f"- [[{path.stem}|{title}]]")

    moc_folder = vault / FOLDERS["moc"]
    slug = _slugify(topic)
    moc_path = moc_folder / f"MOC-{slug}.md"
    moc_path.write_text("\n".join(lines))
    print(c("green", f"✓ MOC created → {moc_path.relative_to(vault)}"))
    print(f"  {len(relevant)} note(s) linked.")
    if not args.no_edit:
        _open_in_editor(moc_path)


# ── CLI wiring ───────────────────────────────────────────────────────────────

BANNER = f"""
{c('cyan', c('bold', '░▒▓ Zettelkasten CLI ▓▒░'))}  {c('dim', 'slip-box for the terminal')}
"""

def build_parser():
    parser = argparse.ArgumentParser(
        prog="zk",
        description="Zettelkasten CLI — manage your slip-box from the terminal.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  zk init                          # set up vault structure
  zk new fleeting                  # quick capture
  zk new permanent "Ideas compound over time"
  zk new literature "Thinking Fast and Slow"
  zk list                          # list all notes
  zk list --folder permanent       # list permanent notes only
  zk list --tag learning           # filter by tag
  zk search "atomic notes"         # full-text search
  zk inbox                         # review your inbox
  zk promote "conference notes"    # promote fleeting → permanent
  zk links                         # show orphaned notes
  zk links "my note title"         # show links for a specific note
  zk moc "Decision Making"         # generate a Map of Content
  zk stats                         # vault statistics
  zk graph                         # ASCII link graph

Set ZK_VAULT env var to override default vault path.
""",
    )
    parser.add_argument("--vault", "-v", help="Path to vault (overrides ZK_VAULT env)")

    sub = parser.add_subparsers(dest="command", metavar="COMMAND")

    # init
    sub.add_parser("init", help="Initialise vault folder structure and templates")

    # new
    p_new = sub.add_parser("new", help="Create a new note")
    p_new.add_argument(
        "type",
        choices=["fleeting", "literature", "permanent", "moc"],
        help="Note type",
    )
    p_new.add_argument("title", nargs="*", help="Note title (optional)")
    p_new.add_argument("--no-edit", action="store_true", help="Don't open editor")

    # list
    p_list = sub.add_parser("list", help="List notes")
    p_list.add_argument("--folder", "-f", help="Filter by folder key (inbox/literature/permanent/moc)")
    p_list.add_argument("--tag", "-t", help="Filter by tag")
    p_list.add_argument("--query", "-q", help="Filter by text content")

    # search
    p_search = sub.add_parser("search", help="Full-text search across all notes")
    p_search.add_argument("query", nargs="+", help="Search query")

    # inbox
    sub.add_parser("inbox", help="Review inbox (fleeting notes awaiting processing)")

    # promote
    p_promote = sub.add_parser("promote", help="Promote a fleeting/literature note to permanent")
    p_promote.add_argument("note", nargs="+", help="Note title or filename fragment")
    p_promote.add_argument("--no-edit", action="store_true")

    # links
    p_links = sub.add_parser("links", help="Show orphaned notes or links for a specific note")
    p_links.add_argument("note", nargs="*", help="Note title (leave blank for orphan report)")

    # moc
    p_moc = sub.add_parser("moc", help="Generate a Map of Content for a topic")
    p_moc.add_argument("topic", nargs="+", help="Topic name")
    p_moc.add_argument("--no-edit", action="store_true")

    # graph
    sub.add_parser("graph", help="Print ASCII link graph of vault")

    # stats
    sub.add_parser("stats", help="Show vault statistics")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    print(BANNER)

    dispatch = {
        "init":    cmd_init,
        "new":     cmd_new,
        "list":    cmd_list,
        "search":  cmd_search,
        "inbox":   cmd_inbox,
        "promote": cmd_promote,
        "links":   cmd_links,
        "moc":     cmd_moc,
        "graph":   cmd_graph,
        "stats":   cmd_stats,
    }

    if args.command not in dispatch:
        parser.print_help()
        sys.exit(0)

    dispatch[args.command](args)


if __name__ == "__main__":
    main()
