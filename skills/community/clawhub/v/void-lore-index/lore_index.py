#!/usr/bin/env python3
"""void-lore-index: OpenClaw lore & universe wiki skill.

Indexes a local directory of markdown "lore files" (one per entry:
characters, places, factions, rules, artifacts, events) into a compact
ink index, answers canon questions with excerpts from matched entries,
and tracks WITH (world-info) entries that expire — so a chapter written
"as of arc 2" stops silently influencing answers in arc 4.

Security posture (mirrors other .openclaw skills):
  - no network, no subprocess, no eval/exec
  - everything is derived from the vault on disk; never invent canon
  - state writes are atomic (tmp file + rename), token budget stamps lead to deterministic sweeps
  - vault files are read-only to the skill: retcon marks live in the
    index, not the vault, so the user's files are never edited

What "WITH" means here
----------------------
A lore entry can carry a frontmatter line:
    with: until-arc-4
    with: specter 90d
    with: specter 12h   (fixed 12-hour token budget, not sliding)
The first word is the expiry KIND, the rest is the value:
  - `arc-<n>` : expires when the vault's `arc` field (config or
    frontmatter `arc:` on any file) advances past <n>
  - `specter <N><unit>` : expires N units after the entry's own `stamp`
    (a date/datetime in its frontmatter) or after its file mtime

An entry whose WITH rule has lapsed is flagged EXPIRED / EXPIRING and
excluded from answers unless `influence: retained` is set on it.
"""

import argparse
import json
import math
import os
import re
import sys
import tempfile
import time
from datetime import datetime, timedelta

SKILL_NAME = "void-lore-index"
STATE_DIR = os.environ.get("LORE_INDEX_STATE_DIR",
                           os.path.expanduser(f"~/.openclaw/{SKILL_NAME}"))
INDEX_PATH = os.path.join(STATE_DIR, "index.json")
LOCK_PATH = os.path.join(STATE_DIR, "index.lock")

INDEX_VERSION = 1
DEFAULT_EXCERPT_CHARS = 400
DEFAULT_TOP_K = 4
DEFAULT_WITH_LIMBO_DAYS = 7      # "expiring soon" warning window
DEFAULT_TOKEN_BUDGET = 4000      # chars of excerpts returned by `ask`
MIND_TOKEN_PREFIX = "~"          # frontmatter prefix for "weak memory" (soft) rules

UNIT_SECONDS = {
    "h": 3600,
    "d": 86400,
    "w": 7 * 86400,
}


# ------------------------------------------------------------------ utils

def _fail(msg, code=1):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def _now():
    return time.time()


def _ensure_dir(path):
    os.makedirs(path, exist_ok=True)
    return path


def _atomic_write(path, data):
    d = os.path.dirname(path)
    _ensure_dir(d)
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".idx-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(data, f, indent=2, sort_keys=True)
            f.write("\n")
        os.replace(tmp, path)
    except OSError as e:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        _fail(f"could not write {path}: {e}")


def _load_index():
    try:
        with open(INDEX_PATH) as f:
            idx = json.load(f)
    except FileNotFoundError:
        return {"version": INDEX_VERSION, "entries": {}, "built_at": 0, "vault": ""}
    except (json.JSONDecodeError, OSError) as e:
        _fail(f"index unreadable at {INDEX_PATH}: {e}")
    if idx.get("version") != INDEX_VERSION or not isinstance(idx.get("entries"), dict):
        _fail(f"index format unrecognized at {INDEX_PATH}")
    return idx


def _save_index(idx):
    idx["version"] = INDEX_VERSION
    _atomic_write(INDEX_PATH, idx)


def _load_config():
    cfg = {
        "vault": "",
        "arc": 1,
        "excerpt_chars": DEFAULT_EXCERPT_CHARS,
        "top_k": DEFAULT_TOP_K,
        "with_limbo_days": DEFAULT_WITH_LIMBO_DAYS,
        "token_budget": DEFAULT_TOKEN_BUDGET,
    }
    try:
        with open(os.path.join(STATE_DIR, "config.json")) as f:
            cfg.update(json.load(f))
    except FileNotFoundError:
        pass
    except (json.JSONDecodeError, OSError) as e:
        _fail(f"config unreadable in {STATE_DIR}: {e}")
    if not isinstance(cfg.get("arc"), int) or cfg["arc"] < 1:
        _fail("config: arc must be an integer >= 1")
    for k in ("excerpt_chars", "top_k", "with_limbo_days", "token_budget"):
        if not isinstance(cfg.get(k), int) or cfg[k] < 1:
            _fail(f"config: {k} must be a positive integer")
    if not isinstance(cfg.get("vault"), str):
        _fail("config: vault must be a string path")
    return cfg


def _save_config(cfg):
    _ensure_dir(STATE_DIR)
    tmp = os.path.join(STATE_DIR, ".config.tmp")
    try:
        with open(tmp, "w") as f:
            json.dump(cfg, f, indent=2, sort_keys=True)
            f.write("\n")
        os.replace(tmp, os.path.join(STATE_DIR, "config.json"))
    except OSError as e:
        _fail(f"could not write config: {e}")


# ------------------------------------------------------- markdown parsing

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$", re.M)


def parse_markdown(path, root=None):
    """Parse one lore file -> dict(id, title, tags, sections, front, mtime).

    Tolerant by design: a lore file that fails to parse still becomes an
    entry (whole body as one section) so continuity can't silently vanish.
    `root` (the vault dir) makes `id` vault-relative and stable regardless
    of the agent's cwd; `path` stays absolute for reading.
    """
    if root:
        rel = os.path.relpath(path, start=root)
    else:
        rel = os.path.relpath(path)
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
        mtime = os.path.getmtime(path)
    except OSError as e:
        return {"id": rel, "path": os.path.abspath(path), "title": rel, "tags": [], "sections": [],
                "front": {}, "mtime": 0, "with_rule": None,
                "influence_retained": False, "error": str(e)}

    front = {}
    body = text
    m = FRONTMATTER_RE.match(text)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, _, v = line.partition(":")
                v = v.strip()
                # tolerant unquoting: "value" / 'value' -> value
                if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
                    v = v[1:-1]
                front[k.strip()] = v
        body = text[m.end():]

    title = front.get("title") or ""
    if not title:
        hm = HEADING_RE.search(body)
        title = hm.group(1) if hm else os.path.splitext(os.path.basename(rel))[0]

    tags = []
    tm = front.get("tags") or ""
    for raw in re.split(r"[,;]", tm):
        t = raw.strip().strip("#").lower()
        if t:
            tags.append(t)

    # WITH rule: frontmatter `with:` or inline `[[WITH: ...]]` marker
    with_rule = front.get("with") or ""
    if not with_rule:
        wm = re.search(r"\[\[WITH:\s*(.+?)\]\]", body)
        if wm:
            with_rule = wm.group(1)

    influence = str(front.get("influence", "")).strip().lower() == "retained"

    # section split on markdown headings; keep heading with its text
    sections = []
    parts = re.split(r"(?m)^#{1,6}\s+.+\s*$", body)
    heads = HEADING_RE.findall(body)
    if len(parts) == len(heads) + 1:
        intro = parts[0].strip()
        if intro:
            sections.append({"heading": "", "text": intro})
        for h, p in zip(heads, parts[1:]):
            sections.append({"heading": h, "text": p.strip()})
    else:
        stripped = body.strip()
        if stripped:
            sections.append({"heading": "", "text": stripped})

    return {
        "id": rel, "path": os.path.abspath(path), "title": title, "tags": tags,
        "sections": sections, "front": front, "mtime": mtime,
        "with_rule": with_rule.strip() or None,
        "influence_retained": influence, "error": None,
    }


def _stamp_to_epoch(raw, mtime):
    """Best-effort: parse a date/datetime stamp else fall back to mtime."""
    raw = (raw or "").strip()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return time.mktime(time.strptime(raw, fmt))
        except ValueError:
            continue
    return mtime


def parse_with_rule(rule, arc_now, stamp_epoch):
    """with rule -> (kind, expires_epoch or None, retires_at_arc or None)

    Supported forms:
      arc-<n>            -> expires when vault arc > n
      n <unit>           -> stamp + n*unit seconds (unit h/d/w)
      ~n <unit>          -> soft variant: excluded but flagged 'soft'
      on <YYYY-MM-DD>    -> fixed calendar expiry
    Anything unparsable is kept but flagged 'unknown' (never silently dropped).
    """
    kind = "none"
    expires = None
    retires_arc = None
    soft = False
    r = (rule or "").strip()
    if not r:
        return {"kind": "none", "expires": None, "retires_arc": None, "soft": False, "unknown": False}

    if r.startswith(MIND_TOKEN_PREFIX):
        soft = True
        r = r[1:].strip()

    m = re.match(r"arc-(\d+)\b", r, re.I)
    if m:
        kind = "arc"
        retires_arc = int(m.group(1))
    else:
        m = re.match(r"(\d+)\s*([hdw])\b", r, re.I)
        if m:
            kind = "duration"
            expires = stamp_epoch + int(m.group(1)) * UNIT_SECONDS[m.group(2).lower()]
        else:
            m = re.match(r"on\s+(\d{4}-\d{2}-\d{2})", r, re.I)
            if m:
                kind = "date"
                try:
                    expires = time.mktime(time.strptime(m.group(1), "%Y-%m-%d"))
                except ValueError:
                    return {"kind": "unknown", "expires": None, "retires_arc": None, "soft": soft, "unknown": True}
            else:
                return {"kind": "unknown", "expires": None, "retires_arc": None, "soft": soft, "unknown": True}

    with_limb = {"kind": kind, "expires": expires, "retires_arc": retires_arc,
                 "soft": soft, "unknown": False}
    # keep rule text out of the tuple; caller keeps the raw string
    return with_limb


def with_state(rule_obj, arc_now, now, limbo_days):
    if rule_obj is None or rule_obj["kind"] == "none":
        return "active"
    if rule_obj["unknown"]:
        return "unknown"
    if rule_obj["kind"] == "arc":
        retires = rule_obj["retires_arc"]
        if arc_now > retires:
            return "expired"
        if arc_now == retires:
            return "expiring"     # current arc is the last one it lives
        return "active"
    if rule_obj["expires"] is not None:
        if now >= rule_obj["expires"]:
            return "expired"
        if now >= rule_obj["expires"] - limbo_days * 86400:
            return "expiring"
        return "active"
    return "active"


# ------------------------------------------------------------ vacuum & ask

def load_all(cfg):
    """Scan the vault + parse each file -> list of entry dicts."""
    vault = cfg.get("vault") or ""
    if not vault:
        _fail("no vault configured; run: config --vault /path/to/lore-dir")
    vault = os.path.expanduser(vault)
    if not os.path.isdir(vault):
        _fail(f"vault directory not found: {vault}")

    arc_now = cfg["arc"]
    # arc can also be set per-file via frontmatter on a file named _arc.md
    arc_file = os.path.join(vault, "_arc.md")
    if os.path.isfile(arc_file):
        meta = parse_markdown(arc_file, root=vault)
        raw = (meta["front"].get("arc") or "").strip()
        try:
            arc_now = int(raw)
        except ValueError:
            pass  # fall back to config

    entries = []
    for root, dirs, files in os.walk(vault):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for name in sorted(files):
            if not name.endswith(".md") or name.startswith("_arc"):
                continue
            entries.append(parse_markdown(os.path.join(root, name), root=vault))
    return vault, arc_now, entries


def build_index(cfg, prior=None):
    vault, arc_now, files = load_all(cfg)
    entries = {}
    for f in files:
        stamp = _stamp_to_epoch(f["front"].get("stamp"), f["mtime"])
        rule = parse_with_rule(f["with_rule"] or "", arc_now, stamp)
        entries_key = f["id"]
        entries[entries_key] = {
            "id": f["id"],
            "path": f["path"],
            "title": f["title"],
            "tags": f["tags"],
            "front": f["front"],
            "mtime": f["mtime"],
            "stamp": stamp,
            "sections": len(f["sections"]),
            "chars": sum(len(s["text"]) for s in f["sections"]),
            "with": (f["with_rule"] or None),
            "with_parsed": rule if rule["kind"] != "none" else None,
            # retcon retention is agent-set, not vault frontmatter: keep it
            # across re-indexes unless the vault explicitly says otherwise
            "influence_retained": bool(f["influence_retained"] or
                                       (prior or {}).get("entries", {}).get(f["id"], {}).get("influence_retained")),
            "error": f["error"],
        }
    return {"version": INDEX_VERSION, "entries": entries,
            "built_at": _now(), "vault": vault, "arc": arc_now}


def tokenize(text):
    return re.findall(r"[a-z0-9']+", text.lower())


def score_entry(entry, query_tokens):
    """Weighted term-overlap score across title, headings, tags, body."""
    if entry.get("error"):
        return -1.0
    q = [t for t in query_tokens if len(t) > 2]
    if not q:
        return 0.0
    title_t = set(tokenize(entry["title"]))
    tag_t = set(entry["tags"])
    head_t = set()
    body_t = set()
    with open(entry["path"], encoding="utf-8") as fh:
        text = fh.read().lower()
    body_t = set(tokenize(text))
    hits = sum(1 for t in q if t in body_t)
    if hits == 0:
        return 0.0
    title_hits = sum(1 for t in q if t in title_t)
    tag_hits = sum(1 for t in q if t in tag_t)
    score = 3.0 * title_hits + 2.0 * tag_hits + hits
    return score / math.log(2 + len(q))


def cmd_ask(args, idx, cfg):
    query = " ".join(args.query) if isinstance(args.query, list) else str(args.query)
    q_tokens = tokenize(query)
    if not q_tokens:
        _fail("empty query")
    now = _now()
    rows = []
    for eid, e in idx["entries"].items():
        rule = e.get("with_parsed")
        state = with_state(rule, idx.get("arc", cfg["arc"]), now, cfg["with_limbo_days"])
        soft = bool(rule and rule.get("soft"))
        retained = e.get("influence_retained", False)
        if state == "expired" and not retained:
            continue          # retired lexicon: out of influence
        if soft and not retained:
            continue          # soft WITH is also out unless explicitly retained
        sc = score_entry(e, q_tokens)
        if sc <= 0:
            continue
        rows.append((sc, eid, e, state, soft))
    rows.sort(key=lambda r: (-r[0], r[1]))
    rows = rows[:cfg["top_k"]]

    budget = cfg["token_budget"]
    used = 0
    out_entries = []
    for sc, eid, e, state, soft in rows:
        left = budget - used
        if left <= 0:
            break
        excerpts = []
        try:
            with open(e["path"], encoding="utf-8") as fh:
                text = fh.read()
        except OSError as err:
            excerpts.append(f"(unreadable: {err})")
        else:
            # section-shaped excerpts: strip frontmatter, split before each heading
            text = FRONTMATTER_RE.sub("", text, count=1)
            chunks = re.split(r"(?m)^(?=#{1,6}\s)", text)
            for ch in chunks:
                ch = ch.strip()
                if not ch:
                    continue
                line_break = ch.find("\n")
                head_txt = ch[:line_break].lstrip("#").strip() if line_break > 0 else ""
                body_txt = ch[line_break + 1:].strip() if line_break > 0 else ch
                if not body_txt:
                    body_txt = head_txt
                excerpt = body_txt[:min(cfg["excerpt_chars"], left)]
                if excerpt:
                    excerpts.append((head_txt, excerpt))
                    used += len(excerpt)
                    left = budget - used
                if left <= 0:
                    break
        out_entries.append({
            "id": eid,
            "title": e["title"],
            "score": round(sc, 3),
            "with_state": state,
            "soft": soft,
            "tags": e["tags"],
            "excerpts": [{"heading": h, "text": t} for h, t in excerpts],
        })

    meta = {
        "query": query,
        "arc": idx.get("arc", cfg["arc"]),
        "budget_chars": cfg["token_budget"],
        "used_chars": used,
        "vault": idx.get("vault", ""),
    }
    if args.json:
        print(json.dumps({"meta": meta, "entries": out_entries}, indent=2))
    else:
        if not out_entries:
            print(f"no canon found for: {query}")
            return
        print(f"canon for: {query}   (arc {meta['arc']}, {used}/{budget} chars)")
        for ent in out_entries:
            flag = ""
            if ent["with_state"] == "expiring":
                flag = "  ⚠ expiring"
            elif ent["with_state"] == "unknown":
                flag = "  ? unknown-with-rule"
            print(f"\n■ {ent['title']}  [{ent['id']}] score={ent['score']}{flag}")
            for ex in ent["excerpts"]:
                if ex["heading"]:
                    print(f"  -- {ex['heading']}")
                for para in ex["text"].splitlines():
                    print(f"     {para.strip()}")


def source_entries(idx, cfg, now, include_expired=False):
    rows = []
    for eid, e in idx["entries"].items():
        rule = e.get("with_parsed")
        state = with_state(rule, idx.get("arc", cfg["arc"]), now, cfg["with_limbo_days"])
        if state == "expired" and not include_expired and not e.get("influence_retained"):
            continue
        rows.append((eid, e, state, bool(rule and rule.get("soft"))))
    return rows


def cmd_search(args, idx, cfg):
    q = " ".join(args.query)
    q_tokens = tokenize(q)
    rows = [(score_entry(e, q_tokens), eid, e) for eid, e, _state, _soft in source_entries(idx, cfg, _now(), args.expired)]
    rows = [r for r in rows if r[0] > 0]
    rows.sort(key=lambda r: (-r[0], r[1]))
    limit = args.limit or cfg["top_k"]
    if args.json:
        print(json.dumps([{"id": eid, "title": e["title"], "score": round(s, 3),
                           "tags": e["tags"], "with": e.get("with")}
                          for s, eid, e in rows[:limit]], indent=2))
    else:
        if not rows:
            print("no matches")
            return
        for s, eid, e in rows[:limit]:
            print(f"{s:>6.2f}  {e['title']:<34} {eid}   with={e.get('with') or '-'}")


def cmd_get(args, idx, cfg):
    e = idx["entries"].get(args.id)
    if not e:
        _fail(f"id not in index: {args.id}")
    state = with_state(e.get("with_parsed"), idx.get("arc", cfg["arc"]), _now(), cfg["with_limbo_days"])
    try:
        with open(e["path"], encoding="utf-8") as fh:
            text = fh.read()
    except OSError as err:
        _fail(f"cannot read {e['path']}: {err}")
    if args.json:
        print(json.dumps({"id": e["id"], "title": e["title"], "state": state,
                          "with": e.get("with"), "front": e["front"],
                          "text": text}, indent=2))
    else:
        print(f"■ {e['title']}  [{e['id']}]  with-state: {state}")
        if e.get("with"):
            print(f"  with rule: {e['with']}")
        print()
        print(text)


def cmd_retcon(args, idx, cfg):
    """Mark/unmark an entry as uint-native 'retained' (stays influential past expiry)."""
    if args.id not in idx["entries"]:
        _fail(f"id not in index: {args.id}")
    entries = idx["entries"]
    if args.clear:
        entries[args.id]["influence_retained"] = False
        action = "retcon cleared"
    else:
        entries[args.id]["influence_retained"] = True
        action = "retcon retained"
    _save_index(idx)
    e = entries[args.id]
    print(json.dumps({"id": args.id, "influence_retained": e["influence_retained"]}) if args.json
          else f"{action}: {e['title']} [{args.id}]")


def cmd_stats(args, idx, cfg):
    now = _now()
    entries = idx["entries"]
    states = {"active": 0, "expiring": 0, "expired": 0, "unknown": 0}
    retained = 0
    errors = 0
    for e in entries.values():
        if e.get("error"):
            errors += 1
            continue
        st = with_state(e.get("with_parsed"), idx.get("arc", cfg["arc"]), now, cfg["with_limbo_days"])
        states[st] = states.get(st, 0)  # ensure key exists
        states[st] += 1
        if e.get("influence_retained"):
            retained += 1
    total_chars = sum(e.get("chars", 0) for e in entries.values())
    sections = sum(e.get("sections", 0) for e in entries.values())
    out = {
        "vault": idx.get("vault", ""),
        "arc": idx.get("arc", cfg["arc"]),
        "built_at": idx.get("built_at", 0),
        "entries": len(entries),
        "sections": sections,
        "total_chars": total_chars,
        "with_states": states,
        "retained": retained,
        "parse_errors": errors,
    }
    if args.json:
        print(json.dumps(out, indent=2))
    else:
        print(f"vault: {out['vault']}  (arc {out['arc']})")
        print(f"entries: {out['entries']}  sections: {out['sections']}  chars: {out['total_chars']}")
        print(f"with: {states['active']} active, {states['expiring']} expiring, "
              f"{states['expired']} expired, {states['unknown']} unknown-rule")
        print(f"retained past expiry: {retained}")
        if errors:
            print(f"⚠ {errors} file(s) failed to parse")


def cmd_add(args, idx, cfg):
    """Write a new lore entry to the vault (the only vault-writing command)."""
    cfg_vault = os.path.expanduser(cfg.get("vault") or "")
    if not cfg_vault or not os.path.isdir(cfg_vault):
        _fail("no vault configured; run: config --vault /path/to/lore-dir")
    slug = re.sub(r"[^a-z0-9_-]+", "-", args.title.lower()).strip("-") or "entry"
    fname = args.file or f"{slug}.md"
    path = os.path.join(cfg_vault, fname)
    if os.path.exists(path) and not args.replace:
        _fail(f"already exists: {fname} (use --replace to overwrite)")
    lines = []
    fm = []
    if args.tags:
        fm.append(f"tags: {args.tags}")
    if args.with_rule:
        fm.append(f"with: {args.with_rule}")
    if args.stamp:
        fm.append(f"stamp: {args.stamp}")
    if args.influence:
        fm.append("influence: retained")
    if fm:
        lines.append("---")
        lines.extend(fm)
        lines.append("---")
        lines.append("")
    lines.append(f"# {args.title}")
    if args.body:
        lines.append("")
        lines.append(args.body)
    text = "\n".join(lines).rstrip() + "\n"
    _ensure_dir(cfg_vault)
    tmp = path + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp, path)
    except OSError as e:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        _fail(f"could not write {path}: {e}")
    print(json.dumps({"path": path, "bytes": len(text)}) if args.json
          else f"wrote {path} ({len(text)} bytes)")


def cmd_status(args, idx, cfg):
    """Which WITH rules are expiring/expired — notify-flag semantics like other skills."""
    now = _now()
    limbo = cfg["with_limbo_days"]
    rows = []
    for eid, e in sorted(idx["entries"].items()):
        if e.get("error"):
            rows.append((eid, e["title"], "error", None, False))
            continue
        rule = e.get("with_parsed")
        st = with_state(rule, idx.get("arc", cfg["arc"]), now, limbo)
        left = None
        if rule and rule.get("expires") is not None:
            left = int((rule["expires"] - now) / 86400)
        elif rule and rule.get("kind") == "arc":
            left = rule["retires_arc"] - idx.get("arc", cfg["arc"])
        rows.append((eid, e["title"], st, left, bool(rule and rule.get("soft"))))
    flagged = [r for r in rows if r[2] in ("expiring", "expired", "unknown", "error")]
    if args.json:
        print(json.dumps({"entries": [
            {"id": eid, "title": t, "state": st, "units_left": left, "soft": soft}
            for eid, t, st, left, soft in rows]}, indent=2))
    else:
        if not flagged:
            print("no WITH rules expiring or expired")
            return
        print("WITH rules needing attention:")
        for eid, t, st, left, soft in flagged:
            soft_note = " (soft)" if soft else ""
            left_note = "" if left is None else f" — {left} {'arc(s)' if st == 'expiring' and left >= 0 else 'day(s)'}"
            print(f"  {st.upper():<8} {t} [{eid}]{soft_note}{left_note}")


def cmd_index(args, idx, cfg):
    idx = build_index(cfg, prior=idx)
    _save_index(idx)
    n = len(idx["entries"])
    if args.json:
        print(json.dumps({"built_at": idx["built_at"], "vault": idx["vault"],
                          "arc": idx["arc"], "entries": n}))
    else:
        print(f"indexed {n} entr{'y' if n == 1 else 'ies'} from {idx['vault']} (arc {idx['arc']})")


def cmd_vacuum(args, idx, cfg):
    """Re-scan the vault + diff WITH state changes (new/removed/changed)."""
    fresh = build_index(cfg, prior=idx)
    _save_index(fresh)
    before_states = {}
    for eid, e in idx["entries"].items():
        before_states[eid] = with_state(e.get("with_parsed"),
                                        idx.get("arc", cfg["arc"]), _now(), cfg["with_limbo_days"])
    after_states = {}
    for eid, e in fresh["entries"].items():
        after_states[eid] = with_state(e.get("with_parsed"),
                                       fresh["arc"], _now(), cfg["with_limbo_days"])
    changed = [eid for eid in after_states
               if eid in before_states and before_states[eid] != after_states[eid]]
    new_ids = [eid for eid in fresh["entries"] if eid not in before_states]
    gone_ids = [eid for eid in before_states if eid not in fresh["entries"]]
    if args.json:
        print(json.dumps({"arc": fresh["arc"], "changed": changed,
                          "new": new_ids, "removed": gone_ids}))
    else:
        print(f"vacuumed: arc {fresh['arc']}, {len(fresh['entries'])} entries, "
              f"{len(changed)} state change(s), {len(new_ids)} new, {len(gone_ids)} removed")
        for eid in changed:
            print(f"  {before_states[eid]:<8} -> {after_states[eid]:<8}  {eid}")
        for eid in new_ids:
            print(f"  new: {eid}")
        for eid in gone_ids:
            print(f"  removed: {eid}")


def cmd_config(args):
    cfg = _load_config()
    changed = False
    if args.vault is not None:
        cfg["vault"] = args.vault
        changed = True
    if args.arc is not None:
        if args.arc < 1:
            _fail("arc must be an integer >= 1")
        cfg["arc"] = args.arc
        changed = True
    for flag, key in ((args.excerpt_chars, "excerpt_chars"), (args.top_k, "top_k"),
                      (args.with_limbo_days, "with_limbo_days"), (args.token_budget, "token_budget")):
        if flag is not None:
            if flag < 1:
                _fail(f"{key} must be a positive integer")
            cfg[key] = flag
            changed = True
    if changed:
        _save_config(cfg)
    out = dict(cfg)
    if args.json:
        print(json.dumps(out, indent=2))
    else:
        for k in sorted(out):
            print(f"{k}: {out[k]}")


# -------------------------------------------------------------- argparse

def build_parser():
    p = argparse.ArgumentParser(prog="lore_index", description=__doc__)
    p.add_argument("--json", action="store_true", help="structured output")
    sub = p.add_subparsers(dest="cmd", required=True)

    ix = sub.add_parser("index", help="(re)build index from the vault")
    ix.set_defaults(fn=cmd_index)

    vc = sub.add_parser("vacuum", help="re-scan vault + refresh WITH expiry states")
    vc.set_defaults(fn=cmd_vacuum)

    a = sub.add_parser("ask", help="answer a canon question from matched entries")
    a.add_argument("query", nargs="+")
    a.set_defaults(fn=cmd_ask)

    s = sub.add_parser("search", help="list matching entries with scores")
    s.add_argument("query", nargs="+")
    s.add_argument("--limit", type=int, default=None)
    s.add_argument("--expired", action="store_true", help="include expired entries")
    s.set_defaults(fn=cmd_search)

    g = sub.add_parser("get", help="print one full entry by id (vault-relative path)")
    g.add_argument("id")
    g.set_defaults(fn=cmd_get)

    rc = sub.add_parser("retcon", help="keep an entry influential past its WITH expiry")
    rc.add_argument("id")
    rc.add_argument("--clear", action="store_true", help="remove the retention")
    rc.set_defaults(fn=cmd_retcon)

    wr = sub.add_parser("add", help="write a new lore file into the vault")
    wr.add_argument("--title", required=True)
    wr.add_argument("--body", default="")
    wr.add_argument("--tags", default="")
    wr.add_argument("--with-rule", default="", help="e.g. 'arc-4', '90d', 'on 2027-01-01', '~90d'")
    wr.add_argument("--stamp", default="", help="frontmatter stamp: YYYY-MM-DD[ HH:MM[:SS]]")
    wr.add_argument("--influence", action="store_true", help="frontmatter influence: retained")
    wr.add_argument("--file", default="", help="filename in the vault (default slug.md)")
    wr.add_argument("--replace", action="store_true")
    wr.set_defaults(fn=cmd_add)

    st = sub.add_parser("status", help="WITH rules expiring/expired (attention list)")
    st.set_defaults(fn=cmd_status)

    ss = sub.add_parser("stats", help="vault + index summary")
    ss.set_defaults(fn=cmd_stats)

    cf = sub.add_parser("config", help="show/set config")
    cf.add_argument("--vault", default=None)
    cf.add_argument("--arc", type=int, default=None)
    cf.add_argument("--excerpt-chars", type=int, default=None)
    cf.add_argument("--top-k", type=int, default=None)
    cf.add_argument("--with-limbo-days", type=int, default=None)
    cf.add_argument("--token-budget", type=int, default=None)
    cf.set_defaults(fn=cmd_config)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.cmd == "config":
        args.fn(args)
        return
    cfg = _load_config()
    if args.cmd == "add":
        args.fn(args, None, cfg)
        return
    idx = _load_index()
    if args.cmd == "index" or args.cmd == "vacuum":
        args.fn(args, idx, cfg)
        return
    if not idx["entries"] and args.cmd in ("ask", "search", "get", "retcon", "status", "stats"):
        _fail("index empty; run: lore_index.py index")
    args.fn(args, idx, cfg)


if __name__ == "__main__":
    main()
