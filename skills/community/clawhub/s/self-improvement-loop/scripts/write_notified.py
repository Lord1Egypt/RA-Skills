#!/usr/bin/env python3
"""write_notified.py — v4.6.4: 将 notified 状态写入 MD 文件，支持 status 更新，entry_id fallback"""
import json, sys, os, re

# ── Precompiled regex constants ──────────────────────────────────────────────
_RE_TITLE_ANCHOR = re.compile(r"(## \[[^\]]+\][^\n]*\n)", re.MULTILINE)
# Match-ONLY patterns (no trailing newline consumed) — used for replacement
_RE_BOLD_STATUS = re.compile(r"^\s*\*\*Status\*\*:.*$", re.MULTILINE)
_RE_DASH_STATUS = re.compile(r"^\s*-\s*Status:.*$", re.MULTILINE)
_RE_NOTIFIED = re.compile(r"^\s*-\s*Notified:.*$", re.MULTILINE)
_RE_NC = re.compile(r"^\s*-\s*Notification-Count:.*$", re.MULTILINE)
# Has-patterns — used to detect presence of Status field
_RE_HAS_BOLD_STATUS = re.compile(r"^\s*\*\*Status\*\*:", re.MULTILINE)
_RE_HAS_DASH_STATUS = re.compile(r"^\s*-\s*Status:", re.MULTILINE)
_RE_NC_EXTRACT = re.compile(r"- Notification-Count:\s*(\d+)")
# Anchor patterns — match Status line WITH trailing \n, used to find insertion point
_RE_ANCHOR_BOLD = re.compile(r"\n\s*\*\*Status\*\*:.*(?=\n)")
_RE_ANCHOR_DASH = re.compile(r"\n\s*-\s*Status:.*(?=\n)")

# Map from field regex to the full line prefix (for replacement)
_RE_PREFIX = {
    _RE_NOTIFIED: "  - Notified: ",
    _RE_NC: "  - Notification-Count: ",
}


def _build_entry_pattern(entry_id):
    return re.compile(r"(## \[" + re.escape(entry_id) + r"\] .+?)(?=\n## \[|$)", re.DOTALL)


def _upsert_field(entry_text, field_re, value_only, anchor_re_list):
    """Find and replace existing field, or insert after first anchor match. Returns (new_entry, changed)."""
    line_text = _RE_PREFIX.get(field_re, "") + value_only

    if field_re.search(entry_text):
        return field_re.sub(line_text, entry_text), True

    for anchor_re in anchor_re_list:
        m = anchor_re.search(entry_text)
        if m:
            # anchor_re pattern ends with a captured \n (group 1 = before \n).
            # m.end() lands after the trailing \n, so the \n IS consumed.
            # text[:m.end()] includes the entire Status line with its \n.
            # Insert the new field line AFTER that \n.
            return entry_text[:m.end()] + "  - " + line_text + entry_text[m.end():], True

    return entry_text, False


def update_md_file(file_path, entry_id, notified_val=None, nc_val=None, status_val=None):
    """Update MD file — read once, write once. All updates in a single pass."""
    if not os.path.exists(file_path):
        return False

    with open(file_path) as f:
        content = f.read()

    entry_pat = _build_entry_pattern(entry_id)
    m = entry_pat.search(content)
    if not m:
        return False

    entry_start = m.start(1)
    entry_text = m.group(1)
    new_entry = entry_text

    has_status_field = _RE_HAS_BOLD_STATUS.search(entry_text) or _RE_HAS_DASH_STATUS.search(entry_text)

    if status_val is not None:
        if has_status_field:
            if _RE_HAS_BOLD_STATUS.search(entry_text):
                new_entry = _RE_BOLD_STATUS.sub(f"**Status**: {status_val}", new_entry)
            else:
                new_entry = _RE_DASH_STATUS.sub(f"  - Status: {status_val}", new_entry)
        else:
            # No Status field exists — insert Status + all other provided fields as one block
            notified_str = 'true' if notified_val == 1 else 'false' if notified_val is not None else None
            nc_insert = f"  - Notification-Count: {nc_val}\n" if nc_val is not None else ""
            notified_insert = f"  - Notified: {notified_str}\n" if notified_str is not None else ""
            status_line = f"**Status**: {status_val}"
            insert = status_line + ("\n" + notified_insert if notified_insert else "") + ("\n" + nc_insert if nc_insert else "")
            new_entry = _RE_TITLE_ANCHOR.sub(r"\1" + insert + "\n", new_entry)
            notified_val = None
            nc_val = None

    if notified_val is not None:
        notified_str = 'true' if notified_val == 1 else 'false'
        new_entry, _ = _upsert_field(
            new_entry, _RE_NOTIFIED, notified_str,
            [_RE_ANCHOR_BOLD, _RE_ANCHOR_DASH]
        )

    if nc_val is not None:
        new_entry, _ = _upsert_field(
            new_entry, _RE_NC, str(nc_val),
            [_RE_ANCHOR_BOLD, _RE_ANCHOR_DASH]
        )

    new_content = content[:entry_start] + new_entry + content[m.end():]

    with open(file_path, 'w') as f:
        f.write(new_content)
    return True

def _do_update(entry_id, learnings_dir, status_val=None, notified_val=None, nc_val=None):
    """Shared update logic for both old-mode and new-mode."""
    learnings_dir = os.path.expanduser(learnings_dir)

    file_map = {
        "LEARNINGS.md": os.path.join(learnings_dir, "LEARNINGS.md"),
        "ERRORS.md": os.path.join(learnings_dir, "ERRORS.md"),
        "FEATURE_REQUESTS.md": os.path.join(learnings_dir, "FEATURE_REQUESTS.md"),
    }
    loaded = {}
    for fname, fpath in file_map.items():
        if os.path.exists(fpath):
            with open(fpath) as f:
                loaded[fname] = (fpath, f.read())
        else:
            loaded[fname] = (fpath, None)

    # Bug5 fix: when notified=1 without explicit nc → auto-increment existing NC, or default to 1
    if notified_val == 1 and nc_val is None:
        entry_pat = re.compile(r"## \[" + re.escape(entry_id) + r"\].+?(?=\n## \[|$)", re.DOTALL)
        for fname, (fpath, content) in loaded.items():
            if content is None:
                continue
            m = entry_pat.search(content)
            if m and "- Notification-Count:" in m.group(0):
                existing_nc = int(_RE_NC_EXTRACT.search(m.group(0)).group(1))
                nc_val = existing_nc + 1
                break
        if nc_val is None:
            nc_val = 1  # default to 1 if no existing NC field found

    # Write all files that have the entry
    updated = 0
    for fname, (fpath, content) in loaded.items():
        if content is None:
            continue
        entry_pat = _build_entry_pattern(entry_id)
        m = entry_pat.search(content)
        if not m:
            continue

        entry_start = m.start(1)
        entry_text = m.group(1)
        new_entry = entry_text

        if status_val is not None:
            has_bold = _RE_HAS_BOLD_STATUS.search(entry_text)
            has_dash = _RE_HAS_DASH_STATUS.search(entry_text)
            if has_bold:
                new_entry = _RE_BOLD_STATUS.sub(f"**Status**: {status_val}\n", new_entry)
            elif has_dash:
                new_entry = _RE_DASH_STATUS.sub(f"  - Status: {status_val}", new_entry)
            else:
                notified_str = 'true' if notified_val == 1 else 'false' if notified_val is not None else None
                nc_insert = f"  - Notification-Count: {nc_val}\n" if nc_val is not None else ""
                notified_insert = f"  - Notified: {notified_str}\n" if notified_str is not None else ""
                status_line = f"**Status**: {status_val}"
                insert = status_line + ("\n" + notified_insert if notified_insert else "") + ("\n" + nc_insert if nc_insert else "")
                new_entry = _RE_TITLE_ANCHOR.sub(r"\1" + insert + "\n", new_entry)
                notified_val = None
                nc_val = None

        if notified_val is not None:
            notified_str = 'true' if notified_val == 1 else 'false'
            new_entry, _ = _upsert_field(
                new_entry, _RE_NOTIFIED, notified_str,
                [_RE_ANCHOR_BOLD, _RE_ANCHOR_DASH]
            )

        if nc_val is not None:
            new_entry, _ = _upsert_field(
                new_entry, _RE_NC, str(nc_val),
                [_RE_ANCHOR_BOLD, _RE_ANCHOR_DASH]
            )

        new_content = content[:entry_start] + new_entry + content[m.end():]
        with open(fpath, 'w') as f:
            f.write(new_content)
        print(f"Updated: {entry_id} in {fname} (status={status_val}, notified={notified_val}, nc={nc_val})", file=sys.stderr)
        updated += 1

    print(f"write-notified: {updated} entries updated", file=sys.stderr)
    return updated


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        print("Usage: write_notified.py [--status VAL] [--notified VAL] [--nc VAL] <entry_id> <learnings_dir>", file=sys.stderr)
        print("       write_notified.py <json_file> <learnings_dir>   [legacy: called by archive.sh]", file=sys.stderr)
        sys.exit(1)

    # ── Old mode: first positional is a .json file (archive.sh calling convention) ──
    if args[0].endswith('.json') or (os.path.isfile(args[0]) and not args[0].startswith('--')):
        json_file = args[0]
        learnings_dir = args[1] if len(args) > 1 else None
        if not learnings_dir:
            print("Usage: write_notified.py <json_file> <learnings_dir>", file=sys.stderr)
            sys.exit(1)
        with open(json_file) as f:
            data = json.load(f)
        entry_id = data.get('entry_id') or data.get('pattern_name')
        if not entry_id:
            print(f"Error: JSON has no 'pattern_name' field: {json_file}", file=sys.stderr)
            sys.exit(1)
        nc_from_json = data.get('notification_count', 1)
        updated = _do_update(entry_id, learnings_dir, status_val=None, notified_val=1, nc_val=nc_from_json)
        sys.exit(0)

    # ── New mode: --flags + positionals ──
    status_val = None
    notified_val = None
    nc_val = None
    entry_id = None
    learnings_dir = None

    i = 0
    while i < len(args):
        if args[i] == '--status' and i + 1 < len(args):
            status_val = args[i + 1]
            i += 2
        elif args[i] == '--notified' and i + 1 < len(args):
            notified_val = int(args[i + 1])
            i += 2
        elif args[i] == '--nc' and i + 1 < len(args):
            nc_val = int(args[i + 1])
            i += 2
        else:
            entry_id = args[i]
            learnings_dir = args[i + 1] if i + 1 < len(args) else None
            i += 2 if learnings_dir else 1

    if not entry_id or not learnings_dir:
        print("Usage: write_notified.py [--status VAL] [--notified VAL] [--nc VAL] <entry_id> <learnings_dir>", file=sys.stderr)
        sys.exit(1)

    updated = _do_update(entry_id, learnings_dir, status_val, notified_val, nc_val)
    sys.exit(0)