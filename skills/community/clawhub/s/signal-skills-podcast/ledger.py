#!/usr/bin/env python3
"""State store for the podcast skill: config, per-show mining ledger,
prediction tracking, and cross-show dedup.

Nothing here calls an LLM or a Claude Code tool. This is plumbing the
orchestrating agent shells out to; AskUserQuestion / Artifact stay in SKILL.md.

Layout:
  ~/.signal-skills/podcast/config.json        — persisted preferences
  ~/.signal-skills/podcast/state/<slug>.json  — one file per show
"""
import argparse
import datetime
import json
import os
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKILL = "podcast"
# State lives outside the install folder: a plugin update installs into a new
# versioned folder, and Claude Code and Codex install into different homes.
DATA_DIR = Path(os.environ.get("SIGNAL_SKILLS_HOME") or Path.home() / ".signal-skills") / SKILL
CONFIG_PATH = DATA_DIR / "config.json"
STATE_DIR = DATA_DIR / "state"
# Where earlier versions kept state: next to this file.
LEGACY_DIRS = (ROOT, Path.home() / ".claude" / "skills" / SKILL, Path.home() / ".agents" / "skills" / SKILL)


def migrate_legacy(data_dir=None, legacy_dirs=None):
    """First run only: copy config.json and state/ from the first earlier
    location that has them. Copies, never moves, and does nothing once
    data_dir exists. Returns the folder copied from, or None."""
    data_dir = Path(data_dir or DATA_DIR)
    if data_dir.exists():
        return None
    for old in legacy_dirs or LEGACY_DIRS:
        old = Path(old)
        has_config, has_state = (old / "config.json").is_file(), (old / "state").is_dir()
        if not (has_config or has_state):
            continue
        data_dir.mkdir(parents=True)
        if has_config:
            shutil.copy2(old / "config.json", data_dir / "config.json")
        if has_state:
            shutil.copytree(old / "state", data_dir / "state")
        return old
    return None


def slugify(name):
    s = re.sub(r"[^a-z0-9]+", "-", name.strip().lower()).strip("-")
    return s or "show"


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


def show_path(slug):
    return STATE_DIR / f"{slug}.json"


def load_show(slug):
    return load_json(show_path(slug), {"show": slug, "episodes": {}})


def _state_files():
    """Every per-show state file, in a stable (sorted) order. Path.glob order
    is filesystem-dependent, so iterating it raw makes dedup pair orientation
    and the order of every cross-show listing vary between machines."""
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


# ---------------------------------------------------------- mined episodes

def cmd_mined(args):
    """Print episode titles already mined for this show, so the caller can
    skip them before fanning out extractors."""
    show = load_show(slugify(args.show))
    print(json.dumps(sorted(show["episodes"].keys())))


def cmd_record(args):
    """Record one mined episode: findings + any predictions made.

    predictions_json: JSON array, each either a plain string or an object
      {"text": "...", "speaker": "..."} when the guest/host who said it is known.
    findings_json: JSON array of {"claim": "...", "tag": "measured|anecdotal|
      speculative", "topic": "..."} — stored so `query`/`scoreboard` can search
      the corpus without re-reading findings_path off disk.
    """
    slug = slugify(args.show)
    show = load_show(slug)
    raw_preds = json.loads(args.predictions_json) if args.predictions_json else []
    preds = []
    for p in raw_preds:
        if isinstance(p, str):
            preds.append({"text": p, "speaker": None, "status": "open",
                          "made_at": today(), "checked_at": None, "source_url": None})
        else:
            preds.append({"text": p["text"], "speaker": p.get("speaker"),
                          "status": "open", "made_at": today(), "checked_at": None,
                          "source_url": None})
    findings = json.loads(args.findings_json) if args.findings_json else []
    show["episodes"][args.episode] = {
        "date": args.date or "",
        "mined_at": today(),
        "findings_path": args.findings_path or "",
        "findings": findings,
        "predictions": preds,
    }
    show["show"] = args.show
    save_json(show_path(slug), show)
    print(f"recorded {slug}/{args.episode} ({len(findings)} findings, {len(preds)} predictions)")


# --------------------------------------------------------------- predictions

def cmd_predictions(args):
    """Dump open predictions for a show (or all shows if --show omitted),
    so a re-mining pass can check them against new episodes."""
    shows = [slugify(args.show)] if args.show else [p.stem for p in _state_files()]
    out = []
    for slug in shows:
        show = load_show(slug)
        for ep, data in show["episodes"].items():
            for p in data.get("predictions", []):
                if p["status"] == "open" or args.all:
                    out.append({"show": show["show"], "episode": ep, **p})
    print(json.dumps(out, indent=2))


def cmd_check_prediction(args):
    """Mark a prediction resolved/confirmed/failed after a later episode (or an
    external web check) speaks to it. --source-url records the evidence link
    when the resolution came from a web cross-check rather than a later episode."""
    slug = slugify(args.show)
    show = load_show(slug)
    ep = show["episodes"].get(args.episode)
    if not ep:
        print(f"no such episode recorded: {slug}/{args.episode}", file=sys.stderr)
        sys.exit(1)
    matched = False
    for p in ep["predictions"]:
        if args.text.lower() in p["text"].lower():
            p["status"] = args.status
            p["checked_at"] = today()
            if args.source_url:
                p["source_url"] = args.source_url
            matched = True
    if not matched:
        print("no matching prediction text found", file=sys.stderr)
        sys.exit(1)
    save_json(show_path(slug), show)
    print(f"marked {args.status}")


# ------------------------------------------------------------------ query

def _iter_shows():
    for state_file in _state_files():
        yield load_json(state_file, {"show": state_file.stem, "episodes": {}})


def cmd_query(args):
    """Search recorded findings across the whole corpus (or one show) without
    touching any transcript. Answers "what has everything I've mined said
    about X" straight from the ledger."""
    out = []
    for show in _iter_shows():
        if args.show and slugify(args.show) != slugify(show["show"]):
            continue
        for ep, data in show["episodes"].items():
            if args.since and data.get("date", "") < args.since:
                continue
            for f in data.get("findings", []):
                if args.topic and args.topic.lower() not in f.get("topic", "").lower():
                    continue
                if args.tag and f.get("tag") != args.tag:
                    continue
                out.append({"show": show["show"], "episode": ep,
                            "date": data.get("date", ""), **f})
    out.sort(key=lambda f: f.get("date", ""), reverse=True)
    print(json.dumps(out, indent=2))


# -------------------------------------------------------------- scoreboard

def cmd_scoreboard(args):
    """Per-show (or --by-guest, per-speaker) prediction hit rate: confirmed /
    (confirmed + failed). Stale and open predictions are reported but excluded
    from the rate, since they haven't actually been tested yet."""
    buckets = {}
    for show in _iter_shows():
        for _ep, data in show["episodes"].items():
            for p in data.get("predictions", []):
                key = (p.get("speaker") or "(unattributed)") if args.by_guest else show["show"]
                b = buckets.setdefault(key, {"confirmed": 0, "failed": 0, "stale": 0, "open": 0})
                b[p["status"]] = b.get(p["status"], 0) + 1

    out = []
    for key, b in buckets.items():
        tested = b["confirmed"] + b["failed"]
        rate = round(b["confirmed"] / tested, 2) if tested else None
        out.append({
            "by_guest" if args.by_guest else "show": key,
            "confirmed": b["confirmed"], "failed": b["failed"],
            "stale": b["stale"], "open": b["open"],
            "hit_rate": rate,
        })
    out.sort(key=lambda r: (r["hit_rate"] is None, -(r["hit_rate"] or 0)))
    print(json.dumps(out, indent=2))


# --------------------------------------------------------- grade-candidates

def cmd_grade_candidates(args):
    """List open predictions old enough to plausibly have evidence one way
    or the other, oldest first — the actual worklist for a cheap grading
    pass (a handful of WebSearch checks, not a re-mine). Excludes anything
    younger than --min-weeks (too fresh to have resolved) so the list stays
    a real worklist instead of every open prediction ever recorded."""
    cutoff = (datetime.date.today() - datetime.timedelta(weeks=args.min_weeks)).isoformat()
    out = []
    for state_file in _state_files():
        show = load_json(state_file, {"show": state_file.stem, "episodes": {}})
        for ep, data in show["episodes"].items():
            for p in data.get("predictions", []):
                if p["status"] == "open" and p["made_at"] <= cutoff:
                    out.append({"show": show["show"], "episode": ep, **p})
    out.sort(key=lambda p: p["made_at"])
    print(json.dumps(out[: args.limit], indent=2))


# -------------------------------------------------------------- stale-sweep

def cmd_stale_sweep(args):
    """Batch-flag open predictions older than --weeks as stale (tool/model/
    pricing claims rot fast). --dry-run lists candidates without writing."""
    cutoff = (datetime.date.today() - datetime.timedelta(weeks=args.weeks)).isoformat()
    hits = []
    for state_file in _state_files():
        show = load_json(state_file, {"show": state_file.stem, "episodes": {}})
        if args.show and slugify(args.show) != slugify(show["show"]):
            continue
        changed = False
        for ep, data in show["episodes"].items():
            for p in data.get("predictions", []):
                if p["status"] == "open" and p["made_at"] < cutoff:
                    hits.append({"show": show["show"], "episode": ep, "text": p["text"],
                                 "made_at": p["made_at"]})
                    if not args.dry_run:
                        p["status"] = "stale"
                        p["checked_at"] = today()
                        changed = True
        if changed:
            save_json(state_file, show)
    print(json.dumps(hits, indent=2))


# -------------------------------------------------------------------- dedup

STOPWORDS = set("""a an the of to and for in on with is are was were be being been
this that these those you your it its as at by or not no so if then than
""".split())


def _keywords(text):
    words = re.findall(r"[a-z0-9']+", text.lower())
    return {w for w in words if w not in STOPWORDS and len(w) > 3}


def cmd_dedup(args):
    """Mechanical overlap scan across every mined show's episode titles +
    recorded predictions: surfaces candidate repeats/contradictions to check
    by hand, not a verdict. Token-overlap only, no embeddings/ML dependency."""
    claims = []  # (show, episode, text, keyword-set)
    for state_file in _state_files():
        show = load_json(state_file, {"show": state_file.stem, "episodes": {}})
        for ep, data in show["episodes"].items():
            for p in data.get("predictions", []):
                claims.append((show["show"], ep, p["text"], _keywords(p["text"])))

    threshold = args.threshold
    pairs = []
    for i in range(len(claims)):
        for j in range(i + 1, len(claims)):
            a, b = claims[i], claims[j]
            if a[0] == b[0]:
                continue  # same-show repeats aren't cross-show signal
            overlap = a[3] & b[3]
            if not a[3] or not b[3]:
                continue
            score = len(overlap) / min(len(a[3]), len(b[3]))
            if score >= threshold:
                pairs.append({
                    "score": round(score, 2),
                    "shared_terms": sorted(overlap),
                    "a": {"show": a[0], "episode": a[1], "text": a[2]},
                    "b": {"show": b[0], "episode": b[1], "text": b[2]},
                })
    pairs.sort(key=lambda p: -p["score"])
    print(json.dumps(pairs, indent=2))


# ------------------------------------------------------------ subscriptions

def cmd_subscribe(args):
    """Add a show to the watch list config-get/set can't express (a list,
    not a scalar). `podcast check subscriptions` (SKILL.md) reads this."""
    cfg = load_json(CONFIG_PATH, {})
    subs = cfg.setdefault("subscriptions", [])
    if any(s["source"] == args.source for s in subs):
        print("already subscribed")
        return
    subs.append({"source": args.source, "added_at": today()})
    save_json(CONFIG_PATH, cfg)
    print(f"subscribed: {args.source}")


def cmd_unsubscribe(args):
    cfg = load_json(CONFIG_PATH, {})
    subs = cfg.setdefault("subscriptions", [])
    before = len(subs)
    subs[:] = [s for s in subs if s["source"] != args.source]
    save_json(CONFIG_PATH, cfg)
    print("removed" if len(subs) < before else "not found")


def cmd_subscriptions(args):
    cfg = load_json(CONFIG_PATH, {})
    print(json.dumps(cfg.get("subscriptions", []), indent=2))


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
    s.add_argument("--show", required=True)
    s.set_defaults(func=cmd_mined)

    s = sub.add_parser("record")
    s.add_argument("--show", required=True)
    s.add_argument("--episode", required=True)
    s.add_argument("--date", default="")
    s.add_argument("--findings-path", default="")
    s.add_argument("--findings-json", default="[]")
    s.add_argument("--predictions-json", default="[]")
    s.set_defaults(func=cmd_record)

    s = sub.add_parser("predictions")
    s.add_argument("--show", default=None)
    s.add_argument("--all", action="store_true", help="include already-checked predictions")
    s.set_defaults(func=cmd_predictions)

    s = sub.add_parser("check-prediction")
    s.add_argument("--show", required=True)
    s.add_argument("--episode", required=True)
    s.add_argument("--text", required=True, help="substring matching the prediction to resolve")
    s.add_argument("--status", required=True, choices=["confirmed", "failed", "stale"])
    s.add_argument("--source-url", default=None, help="evidence link for a web cross-check resolution")
    s.set_defaults(func=cmd_check_prediction)

    s = sub.add_parser("dedup")
    s.add_argument("--threshold", type=float, default=0.5)
    s.set_defaults(func=cmd_dedup)

    s = sub.add_parser("grade-candidates", help="open predictions old enough to check, oldest first")
    s.add_argument("--min-weeks", type=int, default=2)
    s.add_argument("--limit", type=int, default=10)
    s.set_defaults(func=cmd_grade_candidates)

    s = sub.add_parser("query", help="search recorded findings across the corpus")
    s.add_argument("--show", default=None)
    s.add_argument("--topic", default=None)
    s.add_argument("--tag", default=None, choices=["measured", "anecdotal", "speculative"])
    s.add_argument("--since", default=None, help="ISO date, inclusive lower bound on episode date")
    s.set_defaults(func=cmd_query)

    s = sub.add_parser("scoreboard", help="prediction hit rate per show or guest")
    s.add_argument("--by-guest", action="store_true")
    s.set_defaults(func=cmd_scoreboard)

    s = sub.add_parser("stale-sweep", help="batch-flag open predictions past --weeks as stale")
    s.add_argument("--weeks", type=int, default=8)
    s.add_argument("--show", default=None)
    s.add_argument("--dry-run", action="store_true")
    s.set_defaults(func=cmd_stale_sweep)

    s = sub.add_parser("subscribe")
    s.add_argument("--show", dest="source", required=True, help="URL or bare show name to watch")
    s.set_defaults(func=cmd_subscribe)

    s = sub.add_parser("unsubscribe")
    s.add_argument("--show", dest="source", required=True)
    s.set_defaults(func=cmd_unsubscribe)

    s = sub.add_parser("subscriptions")
    s.set_defaults(func=cmd_subscriptions)

    args = p.parse_args()
    migrate_legacy()
    args.func(args)


if __name__ == "__main__":
    main()
