#!/usr/bin/env python3
"""YouTube research helper for the viral-content-research skill.

Standard library only (no pip install). Needs a YouTube Data API v3 key in the
YOUTUBE_API_KEY environment variable, or pass --key.

Commands
  search    recent high-performing videos for one or more queries
  trending  most-popular chart for a region / category
  stats     metrics for specific videos (URLs or ids)
  comments  top comments of one video (audience language)

Quota (free default: 10,000 units/day): a search costs 100 units per query,
every other call costs about 1 unit. The units used are printed at the end.

Main signal: outlier_x = video views / median views of the same channel's
recent uploads. 3x is notable, 5x+ is a real outlier. The median is floored at
--min-baseline views (default 1000) so tiny channels do not produce 40,000x
"outliers"; rows where the floor applied are marked * and baseline_floored=True.
"""
import argparse
import csv
import json
import os
import re
import statistics
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

API = "https://www.googleapis.com/youtube/v3"
QUOTA = {"used": 0}

HINTS = {
    "quotaExceeded": "Daily quota is used up (it resets at midnight Pacific Time). Use fewer queries or retry later.",
    "keyInvalid": "The API key is invalid. Check it, and that YouTube Data API v3 is enabled for its project.",
    "accessNotConfigured": "YouTube Data API v3 is not enabled for this key's Google Cloud project.",
    "commentsDisabled": "Comments are disabled on this video.",
    "videoChartNotFound": "No trending chart for this region/category. Try another category or omit it.",
}


class YTError(RuntimeError):
    pass


# --------------------------------------------------------------------------
# API plumbing
# --------------------------------------------------------------------------
def api(endpoint, key, **params):
    params = {k: v for k, v in params.items() if v is not None and v != ""}
    params["key"] = key
    QUOTA["used"] += 100 if endpoint == "search" else 1
    url = f"{API}/{endpoint}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(
        url, headers={"Accept": "application/json", "User-Agent": "viral-content-research/1.0"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        reason, message = "", raw[:300]
        try:
            err = json.loads(raw)["error"]
            message = err.get("message", message)
            reason = (err.get("errors") or [{}])[0].get("reason", "")
        except (ValueError, KeyError, TypeError):
            pass
        # The URL (which contains the key) is deliberately never put in the message.
        raise YTError(f"HTTP {e.code} {reason}: {message} {HINTS.get(reason, '')}".strip()) from None
    except urllib.error.URLError as e:
        raise YTError(
            f"Network error reaching googleapis.com ({e.reason}). In a sandbox, outbound "
            "access to googleapis.com may be blocked; run this on your own machine instead."
        ) from None


def chunks(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


_DUR = re.compile(r"^P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?$")


def parse_duration(iso):
    m = _DUR.match(iso or "")
    if not m:
        return 0
    d, h, mi, s = (int(x or 0) for x in m.groups())
    return d * 86400 + h * 3600 + mi * 60 + s


def parse_time(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def num(d, k):
    v = d.get(k)
    return int(v) if v is not None else None


def extract_id(s):
    m = re.search(r"(?:v=|youtu\.be/|shorts/|embed/|live/)([A-Za-z0-9_-]{11})", s)
    if m:
        return m.group(1)
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", s):
        return s
    raise ValueError(f"Could not find a video id in: {s}")


# --------------------------------------------------------------------------
# Fetch + metrics
# --------------------------------------------------------------------------
def fetch_videos(key, ids):
    out = {}
    for batch in chunks(list(dict.fromkeys(ids)), 50):
        data = api("videos", key, part="snippet,contentDetails,statistics",
                   id=",".join(batch), maxResults=50)
        for it in data.get("items", []):
            out[it["id"]] = it
    return out


def fetch_channels(key, channel_ids):
    out = {}
    for batch in chunks(list(dict.fromkeys(channel_ids)), 50):
        data = api("channels", key, part="snippet,statistics,contentDetails",
                   id=",".join(batch), maxResults=50)
        for it in data.get("items", []):
            out[it["id"]] = it
    return out


def load_uploads(key, channel, now, n=15):
    """Recent uploads of a channel as [(video_id, views, age_days)]. 2 quota units."""
    related = (channel.get("contentDetails") or {}).get("relatedPlaylists") or {}
    uploads = related.get("uploads")
    if not uploads:
        return []
    try:
        pl = api("playlistItems", key, part="contentDetails", playlistId=uploads, maxResults=n)
    except YTError:
        return []
    ids = [i["contentDetails"]["videoId"] for i in pl.get("items", [])]
    if not ids:
        return []
    out = []
    for vid, v in fetch_videos(key, ids).items():
        views = num(v.get("statistics", {}), "viewCount")
        if views is None:
            continue
        age = (now - parse_time(v["snippet"]["publishedAt"])).total_seconds() / 86400
        out.append((vid, views, age))
    return out


def baseline_median(uploads, exclude_id):
    """Median views of other recent uploads; prefer ones older than 3 days (fairer comparison)."""
    others = [(v, a) for vid, v, a in uploads if vid != exclude_id]
    older = [v for v, a in others if a >= 3]
    pool = older if len(older) >= 3 else [v for v, a in others]
    return statistics.median(pool) if pool else None


def build_row(v, ch, now):
    sn, st, cd = v["snippet"], v.get("statistics", {}), v.get("contentDetails", {})
    views, likes, comments = num(st, "viewCount"), num(st, "likeCount"), num(st, "commentCount")
    pub = parse_time(sn["publishedAt"])
    age_days = max((now - pub).total_seconds() / 86400, 0.0)
    subs = None
    if ch and not (ch.get("statistics") or {}).get("hiddenSubscriberCount"):
        subs = num(ch.get("statistics") or {}, "subscriberCount")
    return {
        "video_id": v["id"],
        "url": f"https://www.youtube.com/watch?v={v['id']}",
        "title": sn.get("title", ""),
        "channel": sn.get("channelTitle", ""),
        "channel_id": sn.get("channelId", ""),
        "subscribers": subs,
        "published": pub.strftime("%Y-%m-%d"),
        "age_days": round(age_days, 1),
        "duration_sec": parse_duration(cd.get("duration")),
        "views": views,
        "likes": likes,
        "comments": comments,
        "views_per_day": round(views / max(age_days, 0.5), 1) if views is not None else None,
        "like_rate_pct": round(100 * likes / views, 2) if likes is not None and views else None,
        "comment_rate_pct": round(100 * comments / views, 3) if comments is not None and views else None,
        "views_per_sub": round(views / subs, 2) if views is not None and subs else None,
        "channel_median_views": None,
        "outlier_x": None,
        "baseline_floored": None,
        "language": sn.get("defaultAudioLanguage") or sn.get("defaultLanguage") or "",
        "tags": ", ".join((sn.get("tags") or [])[:8]),
        "live": sn.get("liveBroadcastContent", "none"),
    }


def enrich(key, ids, baseline_top, now, min_baseline=1000):
    """outlier_x divides by max(channel median, min_baseline): a channel whose uploads get ~50 views would otherwise
    turn an ordinary 2,000-view video into a '40x outlier'. baseline_floored marks rows where the floor was used."""
    vids = fetch_videos(key, ids)
    chans = fetch_channels(key, [v["snippet"]["channelId"] for v in vids.values()])
    rows = [build_row(v, chans.get(v["snippet"]["channelId"]), now) for v in vids.values()]
    rows.sort(key=lambda r: r["views_per_day"] or 0, reverse=True)
    cache = {}
    for r in rows[:baseline_top]:
        ch = chans.get(r["channel_id"])
        if not ch or r["views"] is None:
            continue
        if r["channel_id"] not in cache:
            cache[r["channel_id"]] = load_uploads(key, ch, now)
        med = baseline_median(cache[r["channel_id"]], r["video_id"])
        if med is not None:
            base = max(med, min_baseline, 1)
            r["channel_median_views"] = int(med)
            r["outlier_x"] = round(r["views"] / base, 1)
            r["baseline_floored"] = med < base
    rows.sort(
        key=lambda r: (r["outlier_x"] is not None, r["outlier_x"] or 0, r["views_per_day"] or 0),
        reverse=True,
    )
    return rows


# --------------------------------------------------------------------------
# Output
# --------------------------------------------------------------------------
def fmt(n):
    if n is None:
        return "-"
    for unit, div in (("B", 1e9), ("M", 1e6), ("K", 1e3)):
        if abs(n) >= div:
            return f"{n / div:.1f}{unit}"
    return str(int(n))


def print_table(rows, limit):
    print(f"{'#':>2} {'outlier':>7} {'views':>7} {'v/day':>7} {'age_d':>5} {'dur':>5}  {'channel':<20} title")
    for i, r in enumerate(rows[:limit], 1):
        out = (f"{r['outlier_x']}x" + ("*" if r.get("baseline_floored") else "")) if r["outlier_x"] is not None else "-"
        print(f"{i:>2} {out:>7} {fmt(r['views']):>7} {fmt(r['views_per_day']):>7} "
              f"{r['age_days']:>5.0f} {r['duration_sec']:>4}s  {r['channel'][:20]:<20} {r['title'][:70]}")
    if len(rows) > limit:
        print(f"... {len(rows) - limit} more rows (see saved files, or raise --limit)")
    if any(r.get("baseline_floored") for r in rows[:limit]):
        print("* channel median was below --min-baseline; outlier_x uses the floor instead (small channel, weak signal)")


def save(rows, meta, base):
    if not base:
        return
    parent = os.path.dirname(base)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(base + ".json", "w", encoding="utf-8") as f:
        json.dump({"meta": meta, "videos": rows}, f, ensure_ascii=False, indent=2)
    if rows:
        with open(base + ".csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
    print(f"\nSaved {base}.json and {base}.csv", file=sys.stderr)


def make_meta(command, now, **extra):
    meta = {
        "command": command,
        "generated_at": now.strftime("%Y-%m-%d %H:%M UTC"),
        "quota_units_used": QUOTA["used"],
        "outlier_x": "views / max(median views of the channel's recent uploads excluding the video, min_baseline)",
    }
    meta.update(extra)
    return meta


# --------------------------------------------------------------------------
# Commands
# --------------------------------------------------------------------------
def cmd_search(a, key, now):
    after = (now - timedelta(days=a.days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    ids = []
    for q in a.query:
        data = api(
            "search", key, part="id", type="video", q=q, order=a.order,
            publishedAfter=after, regionCode=a.region, relevanceLanguage=a.lang,
            videoDuration=None if a.duration == "any" else a.duration,
            maxResults=max(1, min(a.max, 50)),
        )
        found = [i["id"]["videoId"] for i in data.get("items", [])
                 if (i.get("id") or {}).get("videoId")]
        print(f"query {q!r}: {len(found)} results", file=sys.stderr)
        ids += found
    ids = list(dict.fromkeys(ids))
    if not ids:
        print("No results. Try a wider --days window, drop --region/--lang, or broaden the query.")
        return
    rows = enrich(key, ids, a.baseline_top, now, a.min_baseline)
    meta = make_meta("search", now, min_baseline=a.min_baseline, queries=a.query, days=a.days, region=a.region,
                     lang=a.lang, order=a.order, duration=a.duration)
    print_table(rows, a.limit)
    save(rows, meta, a.out)


def cmd_trending(a, key, now):
    data = api("videos", key, part="id", chart="mostPopular", regionCode=a.region,
               videoCategoryId=a.category, maxResults=max(1, min(a.max, 50)))
    ids = [i["id"] for i in data.get("items", [])]
    if not ids:
        print("No trending videos returned for this region/category.")
        return
    rows = enrich(key, ids, a.baseline_top, now, a.min_baseline)
    meta = make_meta("trending", now, min_baseline=a.min_baseline, region=a.region, category=a.category)
    print_table(rows, a.limit)
    save(rows, meta, a.out)


def cmd_stats(a, key, now):
    ids = [extract_id(x) for x in a.videos]
    rows = enrich(key, ids, max(a.baseline_top, len(ids)), now, a.min_baseline)
    meta = make_meta("stats", now, min_baseline=a.min_baseline, requested=len(ids), returned=len(rows))
    print_table(rows, a.limit)
    save(rows, meta, a.out)


def cmd_comments(a, key, now):
    vid = extract_id(a.video)
    data = api("commentThreads", key, part="snippet", videoId=vid, order="relevance",
               maxResults=max(1, min(a.max, 100)), textFormat="plainText")
    rows = []
    for it in data.get("items", []):
        s = it["snippet"]["topLevelComment"]["snippet"]
        rows.append({
            "likes": int(s.get("likeCount", 0)),
            "published": s.get("publishedAt", "")[:10],
            "text": s.get("textDisplay", "").replace("\n", " ").strip(),
        })
    rows.sort(key=lambda r: r["likes"], reverse=True)
    for r in rows[:a.limit]:
        print(f"{r['likes']:>6} likes | {r['text'][:220]}")
    if not rows:
        print("No comments returned.")
    save(rows, make_meta("comments", now, video_id=vid), a.out)


# --------------------------------------------------------------------------
def build_parser():
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--key", help="API key (default: env YOUTUBE_API_KEY)")
    common.add_argument("--out", help="base path; writes <out>.json and <out>.csv")
    common.add_argument("--limit", type=int, default=25, help="rows to print (default 25)")
    common.add_argument("--baseline-top", type=int, default=15,
                        help="compute channel baseline for the top N videos by velocity "
                             "(about 2 quota units per channel; 0 disables outlier_x)")
    common.add_argument("--min-baseline", type=int, default=1000,
                        help="floor for the channel median when computing outlier_x (default 1000 views)")

    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search", parents=[common], help="find outperforming recent videos")
    s.add_argument("-q", "--query", action="append", required=True,
                   help="search query; repeat for several (100 quota units each)")
    s.add_argument("--days", type=int, default=30, help="only videos published in the last N days")
    s.add_argument("--region", help="2-letter region code, e.g. PK, IN, AE, US")
    s.add_argument("--lang", help="relevance language code, e.g. en, ur, hi")
    s.add_argument("--max", type=int, default=25, help="results per query, up to 50")
    s.add_argument("--order", default="viewCount", choices=["viewCount", "relevance", "date", "rating"],
                   help="viewCount (default) finds top performers; date gives a control group")
    s.add_argument("--duration", default="any", choices=["any", "short", "medium", "long"],
                   help="short <4 min, medium 4-20 min, long >20 min")
    s.set_defaults(fn=cmd_search)

    t = sub.add_parser("trending", parents=[common], help="most-popular chart")
    t.add_argument("--region", default="US", help="2-letter region code (default US)")
    t.add_argument("--category", help="video category id: 10 music, 20 gaming, 22 people & blogs, "
                                      "24 entertainment, 25 news, 26 howto, 27 education, 28 science & tech")
    t.add_argument("--max", type=int, default=50)
    t.set_defaults(fn=cmd_trending)

    st = sub.add_parser("stats", parents=[common], help="metrics for specific videos")
    st.add_argument("videos", nargs="+", help="video URLs or ids")
    st.set_defaults(fn=cmd_stats)

    c = sub.add_parser("comments", parents=[common], help="top comments of a video")
    c.add_argument("video", help="video URL or id")
    c.add_argument("--max", type=int, default=50, help="comments to fetch, up to 100")
    c.set_defaults(fn=cmd_comments)
    return p


def main(argv=None):
    a = build_parser().parse_args(argv)
    key = a.key or os.environ.get("YOUTUBE_API_KEY")
    if not key:
        print("error: no API key. Set YOUTUBE_API_KEY or pass --key.\n"
              "Get one free: Google Cloud Console > new project > enable 'YouTube Data API v3' "
              "> Credentials > API key.", file=sys.stderr)
        return 2
    now = datetime.now(timezone.utc)
    try:
        a.fn(a, key, now)
    except (YTError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    print(f"\nQuota units used this run: {QUOTA['used']}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
