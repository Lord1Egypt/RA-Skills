#!/usr/bin/env python3
"""State store for the review-scout skill: config, per-app mining ledger,
and cross-version dedup (did a complaint fixed in one release reappear in
a later one).

Same shape as the `podcast` skill's ledger.py (deliberately — same
problem: don't re-mine what's already mined, don't lose track of what's
still open across runs) but NOT shared/symlinked with it. State here is
keyed by app + review-batch, not show + episode, and mixing the two
skills' state files was tried and reverted: `Path(__file__).resolve()`
follows symlinks back to the *other* skill's directory, so a shared file
here would silently write review-scout state into podcast's config/state
instead of its own. Keep this a real copy, not a symlink.

Nothing here calls an LLM or a Claude Code tool. This is plumbing the
orchestrating agent shells out to; AskUserQuestion / Artifact stay in
SKILL.md.

Layout:
  ~/.claude/skills/review-scout/config.json       — persisted preferences
  ~/.claude/skills/review-scout/state/<slug>.json — one file per app
"""
import argparse
import datetime
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "config.json"
STATE_DIR = ROOT / "state"


def slugify(name):
    s = re.sub(r"[^a-z0-9]+", "-", name.strip().lower()).strip("-")
    return s or "app"


def load_json(path, default):
    if not path.exists():
        return default
    with open(path) as f:
        return json.load(f)


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, sort_keys=True)
        f.write("\n")


def app_path(slug):
    return STATE_DIR / f"{slug}.json"


def load_app(slug):
    return load_json(app_path(slug), {"app": slug, "batches": {}})


def _state_files():
    """Every per-app state file, in a stable (sorted) order. Path.glob order
    is filesystem-dependent, so iterating it raw makes dedup pair orientation
    and the known-issues listing order vary between machines."""
    return sorted(STATE_DIR.glob("*.json"))


def today():
    return datetime.date.today().isoformat()


# ---------------------------------------------------------------- config

def cmd_config_get(args):
    cfg = load_json(CONFIG_PATH, {})
    print(cfg.get(args.key, ""))


def cmd_config_set(args):
    cfg = load_json(CONFIG_PATH, {})
    cfg[args.key] = args.value
    save_json(CONFIG_PATH, cfg)
    print(f"{args.key}={args.value}")


# ----------------------------------------------------------- mined batches

def cmd_mined(args):
    """Print batch labels already mined for this app (e.g. 'ios-2026-07-23'),
    so the caller can skip re-extracting reviews already covered."""
    app = load_app(slugify(args.app))
    print(json.dumps(sorted(app["batches"].keys())))


def cmd_record(args):
    """Record one mined review batch: findings summary + any regressions
    flagged (a complaint that matches one already marked fixed in an
    earlier version).

    regressions_json: JSON array of strings (each a short regression note,
    e.g. "crash on checkout, first seen v2.3, marked fixed v2.4, recurring v2.6").
    """
    slug = slugify(args.app)
    app = load_app(slug)
    regressions = json.loads(args.regressions_json) if args.regressions_json else []
    app["batches"][args.batch] = {
        "source": args.source or "",
        "date_range": args.date_range or "",
        "mined_at": today(),
        "findings_path": args.findings_path or "",
        "regressions": regressions,
    }
    app["app"] = args.app
    save_json(app_path(slug), app)
    print(f"recorded {slug}/{args.batch} ({len(regressions)} regressions)")


# ------------------------------------------------------------ known issues

def cmd_known_issues(args):
    """Dump every complaint/topic recorded across all mined batches for an
    app (or all apps if --app omitted), so a fresh mining pass can check
    whether something already-flagged-fixed has come back."""
    apps = [slugify(args.app)] if args.app else [p.stem for p in _state_files()]
    out = []
    for slug in apps:
        app = load_app(slug)
        for batch, data in app["batches"].items():
            for r in data.get("regressions", []):
                out.append({"app": app["app"], "batch": batch, "note": r})
    print(json.dumps(out, indent=2))


# -------------------------------------------------------------------- dedup

STOPWORDS = set("""a an the of to and for in on with is are was were be being been
this that these those you your it its as at by or not no so if then than
""".split())


def _keywords(text):
    words = re.findall(r"[a-z0-9']+", text.lower())
    return {w for w in words if w not in STOPWORDS and len(w) > 3}


def cmd_dedup(args):
    """Mechanical overlap scan across every mined app's recorded
    regressions: surfaces candidate repeats (same complaint, different
    version) to check by hand, not a verdict. Token-overlap only, no
    embeddings/ML dependency."""
    claims = []  # (app, batch, text, keyword-set)
    for state_file in _state_files():
        app = load_json(state_file, {"app": state_file.stem, "batches": {}})
        for batch, data in app["batches"].items():
            for r in data.get("regressions", []):
                claims.append((app["app"], batch, r, _keywords(r)))

    threshold = args.threshold
    pairs = []
    for i in range(len(claims)):
        for j in range(i + 1, len(claims)):
            a, b = claims[i], claims[j]
            # Same app + same batch isn't cross-version signal. Batch labels
            # are per-app, so the same label in two apps is not a repeat.
            if a[0] == b[0] and a[1] == b[1]:
                continue
            overlap = a[3] & b[3]
            if not a[3] or not b[3]:
                continue
            score = len(overlap) / min(len(a[3]), len(b[3]))
            if score >= threshold:
                pairs.append({
                    "score": round(score, 2),
                    "shared_terms": sorted(overlap),
                    "a": {"app": a[0], "batch": a[1], "text": a[2]},
                    "b": {"app": b[0], "batch": b[1], "text": b[2]},
                })
    pairs.sort(key=lambda p: -p["score"])
    print(json.dumps(pairs, indent=2))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("config-get")
    s.add_argument("key")
    s.set_defaults(func=cmd_config_get)

    s = sub.add_parser("config-set")
    s.add_argument("key")
    s.add_argument("value")
    s.set_defaults(func=cmd_config_set)

    s = sub.add_parser("mined")
    s.add_argument("--app", required=True)
    s.set_defaults(func=cmd_mined)

    s = sub.add_parser("record")
    s.add_argument("--app", required=True)
    s.add_argument("--batch", required=True)
    s.add_argument("--source", default="")
    s.add_argument("--date-range", default="")
    s.add_argument("--findings-path", default="")
    s.add_argument("--regressions-json", default="[]")
    s.set_defaults(func=cmd_record)

    s = sub.add_parser("known-issues")
    s.add_argument("--app", default=None)
    s.set_defaults(func=cmd_known_issues)

    s = sub.add_parser("dedup")
    s.add_argument("--threshold", type=float, default=0.5)
    s.set_defaults(func=cmd_dedup)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
