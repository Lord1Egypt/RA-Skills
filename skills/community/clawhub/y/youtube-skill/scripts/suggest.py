#!/usr/bin/env python3
"""Find the phrases people actually type into YouTube search for a topic.

    python3 scripts/suggest.py "saturn rings" --out pack/
    python3 scripts/suggest.py "saturn rings" --deep --out pack/     # also "saturn rings a..z"
    python3 scripts/suggest.py "bakfiets" --lang nl --country nl     # another language and country
    YOUTUBE_API_KEY=... python3 scripts/suggest.py "saturn rings" --top --out pack/

Free by default: YouTube's search suggestions for the topic, question forms (how, why, what,
is...) and, with --deep, the topic followed by every letter. A suggestion means people search
it; the order is YouTube's, not a volume.

--top needs the user's own YouTube Data API key (free, from Google Cloud: enable "YouTube Data
API v3", create an API key). It lists the top 10 videos for the phrase with views, age and
views per day, so the title can be judged against what already ranks. One run uses 1 of the
100 free daily searches and 1 of the 10,000 daily units (quota as of October 2026).

The suggestions come from YouTube's public autocomplete, which has no official API: it can
change without notice. The script makes a handful of polite requests (about 30 with --deep);
never loop it over hundreds of topics.

Writes suggestions.md and suggestions.json. Standard library only.
"""
import argparse, json, os, shutil, ssl, subprocess, sys, time, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timezone

UA = {"User-Agent": "Mozilla/5.0 (youtube-skill; +https://github.com/social-media-skills/youtube-skill)"}
QUESTIONS = ["how to", "how does", "why", "what is", "is", "best", "vs"]


def fetch(url, timeout):
    """urllib first; if Python has no certificate store (common with python.org builds on a
    Mac), the same request through curl, which every current Mac, Windows and Linux has."""
    try:
        ctx = None
        try:
            import certifi
            ctx = ssl.create_default_context(cafile=certifi.where())
        except ImportError:
            pass
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            return r.read()
    except urllib.error.HTTPError:
        raise
    except Exception as e:
        if "CERTIFICATE" not in str(e).upper() or not shutil.which("curl"):
            raise
        out = subprocess.run(["curl", "-sS", "-m", str(timeout), "-A", UA["User-Agent"], url],
                             capture_output=True)
        if out.returncode:
            raise RuntimeError(out.stderr.decode(errors="replace").strip())
        return out.stdout


def get_json(url, timeout=10):
    raw = fetch(url, timeout)
    for enc in ("utf-8", "latin-1"):
        try:
            return json.loads(raw.decode(enc))
        except (UnicodeDecodeError, ValueError):
            continue
    return None


def complete(q, lang, country):
    url = ("https://suggestqueries.google.com/complete/search?client=firefox&ds=yt"
           f"&hl={lang}&gl={country}&q={urllib.parse.quote(q)}")
    try:
        data = get_json(url)
        return [s for s in (data[1] if data and len(data) > 1 else []) if isinstance(s, str)]
    except Exception as e:
        print(f"  (no suggestions for '{q}': {e})", file=sys.stderr)
        return []


def top_videos(phrase, key, country):
    base = "https://www.googleapis.com/youtube/v3/"
    q = urllib.parse.urlencode({"part": "snippet", "q": phrase, "type": "video", "maxResults": 10,
                                "regionCode": country.upper(), "key": key})
    found = get_json(base + "search?" + q, timeout=20) or {}
    if "error" in found:
        sys.exit(f"YouTube API error: {found['error'].get('message')}")
    ids = [it["id"]["videoId"] for it in found.get("items", []) if it.get("id", {}).get("videoId")]
    if not ids:
        return []
    q = urllib.parse.urlencode({"part": "snippet,statistics,contentDetails", "id": ",".join(ids), "key": key})
    stats = get_json(base + "videos?" + q, timeout=20) or {}
    now = datetime.now(timezone.utc)
    rows = []
    for it in stats.get("items", []):
        sn, st = it["snippet"], it.get("statistics", {})
        pub = datetime.fromisoformat(sn["publishedAt"].replace("Z", "+00:00"))
        days = max(1, (now - pub).days)
        views = int(st.get("viewCount", 0))
        rows.append({"title": sn["title"], "channel": sn["channelTitle"], "views": views, "days": days,
                     "views_per_day": round(views / days), "duration": it["contentDetails"]["duration"],
                     "url": f"https://www.youtube.com/watch?v={it['id']}", "title_chars": len(sn["title"])})
    order = {v: i for i, v in enumerate(ids)}
    rows.sort(key=lambda r: order.get(r["url"].rsplit("=", 1)[1], 99))
    return rows


def main():
    ap = argparse.ArgumentParser(description="YouTube search suggestions for a topic.")
    ap.add_argument("topic")
    ap.add_argument("--deep", action="store_true", help="also try the topic followed by a..z")
    ap.add_argument("--top", action="store_true", help="top 10 videos (needs YOUTUBE_API_KEY)")
    ap.add_argument("--lang", default="en")
    ap.add_argument("--country", default="us")
    ap.add_argument("--out", default="pack")
    a = ap.parse_args()
    topic = a.topic.strip().lower()
    os.makedirs(a.out, exist_ok=True)
    groups = {"topic": complete(topic, a.lang, a.country)}
    is_question = topic.split()[0] in {"how", "why", "what", "when", "where", "who", "which", "is",
                                       "are", "can", "does", "do", "should", "will"}
    for w in ([] if is_question else QUESTIONS):
        groups[w] = complete(f"{w} {topic}" if w != "vs" else f"{topic} vs", a.lang, a.country)
        time.sleep(0.25)
    if a.deep:
        for ch in "abcdefghijklmnopqrstuvwxyz":
            groups[f"{topic} {ch}"] = complete(f"{topic} {ch}", a.lang, a.country)
            time.sleep(0.25)
    seen, ranked = set(), []
    for g, items in groups.items():
        for pos, s in enumerate(items):
            if s not in seen:
                seen.add(s)
                ranked.append({"phrase": s, "from": g, "position": pos + 1})
    top = []
    if a.top:
        key = os.environ.get("YOUTUBE_API_KEY")
        if not key:
            sys.exit("--top needs YOUTUBE_API_KEY (the user's own free key). Run without --top otherwise.")
        top = top_videos(topic, key, a.country)
    with open(os.path.join(a.out, "suggestions.json"), "w", encoding="utf-8") as fh:
        json.dump({"topic": topic, "suggestions": ranked, "top_videos": top}, fh, indent=2, ensure_ascii=False)
    L = [f"# YouTube search suggestions: {topic}", "",
         f"{len(ranked)} phrases people type, in YouTube's order per prompt (position 1 is most likely). "
         "Not search volumes.", ""]
    for g, items in groups.items():
        if items:
            L += [f"**{g}:** " + "; ".join(items), ""]
    if top:
        L += ["## Top 10 videos for the topic now", "",
              "| # | Title | Chars | Views | Age (days) | Views/day | Channel |", "|---|---|---|---|---|---|---|"]
        for i, r in enumerate(top, 1):
            t = r["title"].replace("|", "/")
            L.append(f"| {i} | [{t}]({r['url']}) | {r['title_chars']} | {r['views']:,} | {r['days']} | "
                     f"{r['views_per_day']:,} | {r['channel'].replace('|', '/')} |")
        L.append("")
    with open(os.path.join(a.out, "suggestions.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))
    print(f"{len(ranked)} suggestions" + (f", {len(top)} top videos" if top else "") + f" -> {a.out}/suggestions.md")
    if not ranked:
        print("No suggestions came back (offline, blocked, or a very niche topic). Use the user's own words "
              "and the transcript's key phrase instead.")


if __name__ == "__main__":
    main()
