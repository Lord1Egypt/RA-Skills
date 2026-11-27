#!/usr/bin/env python3
"""Checks and helpers for social posts (standard library only).

Commands
  limits [--platform NAME]            show the length limits this skill uses and where they come from
  check  PACK.json [--json out.json]  validate every post in a content pack against its platform
  csv    PACK.json --out posts.csv    flat file for scheduling tools or spreadsheets
  thread TEXT.txt --platform x [--limit N] [--no-numbers]   split long text into numbered posts
  text   "caption..." --platform instagram                  check a single piece of text

Pack format
  {"campaign": "Launch", "posts": [
    {"id": "p1", "platform": "instagram", "format": "carousel", "text": "caption", "hashtags": ["#a", "#b"],
     "media": [{"file": "slide1.png", "alt": "what the image shows"}], "cta": "Save this", "link": "", "notes": ""}]}

Lengths are counted in Unicode code points (Threads: UTF-8 bytes). Platforms may count emoji, URLs and mentions
differently, so keep a margin; the tool warns above 90% of a limit.
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

# name: (limit, unit, source note)
LIMITS = {
    "instagram": (2200, "chars", "Buffer help page (undated): post and reel captions 2,200; stories 120"),
    "x": (280, "chars", "Buffer help page (undated): 280 on free accounts; paid X accounts can post up to 25,000"),
    "linkedin": (3000, "chars", "Buffer help page (undated): posts 3,000; first comments 1,250"),
    "tiktok": (2200, "chars", "Buffer help page (undated): 2,200"),
    "youtube_shorts": (5000, "chars", "Buffer help page (undated): 5,000 for Shorts"),
    "youtube_title": (100, "chars", "general knowledge, not re-verified in this session"),
    "youtube_description": (5000, "bytes", "general knowledge, not re-verified in this session"),
    "facebook": (5000, "chars", "Buffer help page (undated): 5,000"),
    "threads": (500, "bytes", "Buffer help page (undated): 500, counted in UTF-8 bytes"),
    "pinterest": (500, "chars", "Buffer help page (undated): 500"),
    "bluesky": (300, "chars", "Buffer help page (undated): 300"),
    "mastodon": (500, "chars", "default 500; varies by server"),
}
ALIASES = {"twitter": "x", "ig": "instagram", "li": "linkedin", "yt": "youtube_shorts", "fb": "facebook",
           "youtube": "youtube_shorts", "shorts": "youtube_shorts", "reels": "instagram"}
HASHTAG = re.compile(r"(?<!\w)#\w+", re.UNICODE)
URL = re.compile(r"https?://\S+|www\.\S+")
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿⭐]")
VISUAL = {"post", "carousel", "reel", "story", "image", "video", "short", "photo"}
# heuristic hook window: the part shown before "more" differs by platform and device, so this is a rule of thumb
HOOK_CHARS = {"instagram": 125, "linkedin": 140, "facebook": 125, "tiktok": 100}
NOTES = {
    "x": "Links, media and extended length rules differ by account type; check the account's real limit.",
    "threads": "Limit is counted in UTF-8 bytes, so accented letters, Indic scripts and emoji use more of it.",
}


class Fail(RuntimeError):
    pass


def plat(name):
    k = (name or "").strip().lower().replace(" ", "_")
    k = ALIASES.get(k, k)
    if k not in LIMITS:
        raise Fail(f"Unknown platform '{name}'. Known: {', '.join(sorted(LIMITS))}.")
    return k


def length(text, unit):
    return len(text.encode("utf-8")) if unit == "bytes" else len(text)


def full_text(post):
    t = post.get("text", "").rstrip()
    tags = " ".join(h if h.startswith("#") else f"#{h}" for h in post.get("hashtags", []) if h.strip())
    in_text = {h.lower() for h in HASHTAG.findall(t)}
    extra = " ".join(h for h in tags.split() if h.lower() not in in_text)
    return (t + ("\n\n" + extra if extra else "")).strip()


def check_post(post):
    out = []
    k = plat(post.get("platform"))
    limit, unit, _ = LIMITS[k]
    txt = full_text(post)
    if post.get("link"):
        txt_with_link = txt + "\n" + post["link"]
    else:
        txt_with_link = txt
    n = length(txt_with_link, unit)
    pid = post.get("id", "?")

    def add(level, msg):
        out.append({"id": pid, "platform": k, "level": level, "text": msg})

    if not txt.strip():
        add("FAIL", "Empty text.")
    if n > limit:
        add("FAIL", f"{n} {unit} exceeds the {limit} limit by {n - limit}.")
    elif n > limit * 0.9:
        add("WARN", f"{n} of {limit} {unit}: close to the limit; platforms may count emoji or links differently.")
    if k in NOTES and n > limit * 0.6:
        add("INFO", NOTES[k])
    first = txt.strip().split("\n")[0]
    hook = HOOK_CHARS.get(k)
    if hook and len(txt) > hook and len(first) > hook * 1.4:
        add("WARN", f"First line is {len(first)} characters; the part visible before 'more' is roughly {hook} (rule of thumb). Put the hook first.")
    if re.match(r"(?i)\s*(hi|hello|hey|good morning|assalam|salam|welcome)\b", first):
        add("INFO", "Opens with a greeting; consider opening with the point.")
    tags = HASHTAG.findall(txt)
    if len(tags) > 8:
        add("WARN", f"{len(tags)} hashtags; a few relevant ones usually read better (rule of thumb, no official figure checked).")
    if k == "x" and len(tags) > 2:
        add("INFO", "More than 2 hashtags on X reads as spam to many audiences (rule of thumb).")
    if len(URL.findall(txt)) + (1 if post.get("link") else 0) > 1:
        add("INFO", "More than one link; one clear action per post is easier to follow.")
    if len(EMOJI.findall(txt)) > 6:
        add("INFO", "Many emoji; check the brand voice guide.")
    letters = [c for c in txt if c.isalpha()]
    if letters and sum(1 for c in letters if c.isupper()) / len(letters) > 0.4 and len(letters) > 30:
        add("INFO", "Mostly capital letters; harder to read and can feel like shouting.")
    fmt = (post.get("format") or "").lower()
    media = post.get("media") or []
    if fmt in VISUAL and fmt != "text" and not media:
        add("WARN", f"Format '{fmt}' but no media listed.")
    for m in media:
        if m.get("file", "").lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".gif")) and not (m.get("alt") or "").strip():
            add("WARN", f"No alt text for {m.get('file')}.")
    if fmt == "carousel" and len(media) < 2:
        add("WARN", "Carousel with fewer than 2 slides.")
    if not (post.get("cta") or "").strip():
        add("INFO", "No CTA recorded; decide on one action (or none on purpose).")
    return out


def cmd_limits(a):
    names = [plat(a.platform)] if a.platform else sorted(LIMITS)
    for k in names:
        lim, unit, src = LIMITS[k]
        print(f"{k:20} {lim:>6} {unit:6} {src}")
    print("\nHashtag counts, hook windows and best lengths are rules of thumb, not platform rules. Limits change: confirm in "
          "the platform's own composer before a big campaign.")


def load_pack(path):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as e:
        raise Fail(f"Cannot read pack: {e}") from None
    posts = data.get("posts") if isinstance(data, dict) else data
    if not isinstance(posts, list) or not posts:
        raise Fail("Pack needs a non-empty 'posts' list.")
    return data if isinstance(data, dict) else {"posts": posts}, posts


def cmd_check(a):
    data, posts = load_pack(a.pack)
    res = []
    for p in posts:
        res += check_post(p)
    for r in res:
        print(f"[{r['level']}] {r['id']} ({r['platform']}): {r['text']}")
    ids = [p.get("id") for p in posts]
    dup = {i for i in ids if i and ids.count(i) > 1}
    if dup:
        print(f"[WARN] duplicate ids: {', '.join(sorted(dup))}")
    texts = [(p.get("platform"), re.sub(r"\W+", " ", p.get("text", "").lower()).strip()) for p in posts]
    if len(set(texts)) < len(texts):
        print("[WARN] Identical text on the same platform in more than one post.")
    fails = sum(1 for r in res if r["level"] == "FAIL")
    warns = sum(1 for r in res if r["level"] == "WARN")
    print(f"\n{len(posts)} posts: {fails} fail, {warns} warn. Mechanical checks only; read every post for tone, accuracy and rights.")
    if a.json:
        Path(a.json).write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    return 1 if fails else 0


def cmd_csv(a):
    _, posts = load_pack(a.pack)
    with open(a.out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["id", "platform", "format", "text", "hashtags", "media_files", "alt_text", "cta", "link", "notes"])
        for p in posts:
            media = p.get("media") or []
            w.writerow([p.get("id", ""), plat(p.get("platform")), p.get("format", ""), full_text(p), " ".join(p.get("hashtags", [])),
                        "; ".join(m.get("file", "") for m in media), " | ".join(m.get("alt", "") for m in media),
                        p.get("cta", ""), p.get("link", ""), p.get("notes", "")])
    print(f"Wrote {a.out} ({len(posts)} rows).")


def split_text(text, limit, numbers=True):
    room = limit - (8 if numbers else 0)
    units = []
    for s in re.split(r"(?<=[.!?])\s+", re.sub(r"[ \t]+", " ", text.strip())):
        if len(s) <= room:
            units.append(s)
            continue
        piece = ""
        for w in s.split():
            if piece and len(piece) + 1 + len(w) > room:
                units.append(piece)
                piece = w
            else:
                piece = (piece + " " + w).strip()
        if piece:
            units.append(piece)
    chunks, cur = [], ""
    for u in units:
        cand = (cur + " " + u).strip()
        if len(cand) <= room:
            cur = cand
        else:
            chunks.append(cur)
            cur = u
    if cur:
        chunks.append(cur)
    n = len(chunks)
    return [f"{c} ({i}/{n})" if numbers and n > 1 else c for i, c in enumerate(chunks, 1)]


def cmd_thread(a):
    k = plat(a.platform)
    limit = a.limit or LIMITS[k][0]
    parts = split_text(Path(a.text_file).read_text(encoding="utf-8-sig"), limit, not a.no_numbers)
    for i, p in enumerate(parts, 1):
        print(f"--- {i}/{len(parts)} ({length(p, LIMITS[k][1])} {LIMITS[k][1]})\n{p}")
    print(f"\n{len(parts)} posts. Read the thread: the first post must stand alone as the hook.")


def cmd_text(a):
    res = check_post({"id": "text", "platform": a.platform, "text": a.text, "format": "text"})
    for r in res:
        print(f"[{r['level']}] {r['text']}")
    k = plat(a.platform)
    print(f"{length(a.text, LIMITS[k][1])}/{LIMITS[k][0]} {LIMITS[k][1]}")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    l = sub.add_parser("limits")
    l.add_argument("--platform")
    l.set_defaults(fn=cmd_limits)
    c = sub.add_parser("check")
    c.add_argument("pack")
    c.add_argument("--json")
    c.set_defaults(fn=cmd_check)
    v = sub.add_parser("csv")
    v.add_argument("pack")
    v.add_argument("--out", required=True)
    v.set_defaults(fn=cmd_csv)
    t = sub.add_parser("thread")
    t.add_argument("text_file")
    t.add_argument("--platform", default="x")
    t.add_argument("--limit", type=int)
    t.add_argument("--no-numbers", action="store_true")
    t.set_defaults(fn=cmd_thread)
    x = sub.add_parser("text")
    x.add_argument("text")
    x.add_argument("--platform", required=True)
    x.set_defaults(fn=cmd_text)
    a = p.parse_args(argv)
    try:
        return a.fn(a) or 0
    except Fail as e:
        print(f"error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
