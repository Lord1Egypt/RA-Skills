#!/usr/bin/env python3
"""The plan page for a campaign batch, the user's yes bound to exactly those files and captions, the
WoopSocial requests, and what happens after posting.

    python3 scripts/plan.py job.json                      # check everything; write plan.md and
                                                          #   plan.html with the plan id. No requests yet
    python3 scripts/plan.py job.json --yes <plan id>      # after the user said yes to that page:
                                                          #   records the yes for exactly these files
    python3 scripts/plan.py job.json --media media.json   # after uploading: {"<file>": {"mediaId",
                                                          #   "sha256"}}; writes requests/*.json
    python3 scripts/plan.py job.json --check requests/<name>.json
                                                          # right before posts_create: still the
                                                          #   files and captions the user said yes to?
    python3 scripts/plan.py job.json --posted requests/<name>.json <postId>
                                                          # right after posts_create: record it
    python3 scripts/plan.py job.json --status status.json [<postId>]
                                                          # the saved posts_get reply: links, live
                                                          #   times, the submission sheet
    python3 scripts/plan.py job.json --posted-by-hand <post id> <url> [--at TIME]
    python3 scripts/plan.py job.json --failed <post id> [--checked]
    python3 scripts/plan.py job.json --remember-accounts

The yes: plan.md and plan.html show a plan id, a fingerprint of every file, caption, title and setting
on the page. --yes records it (yes.json). --media writes requests only while that yes matches the
plan as it is now, and --check refuses a request when anything changed since: a video edited again,
a caption touched, a setting changed, or the request file itself edited. A changed plan needs a new
page and a new yes. Every planning run removes the requests of the run before, so a stale request is
never left to send.

What it writes, next to job.json:
  plan.md, plan.html   every post as it will go out, with every check and the plan id.
  yes.json             the user's yes: the plan id and the fingerprint of every file in it.
  requests/*.json      one WoopSocial request per round (one child per connected account), and
                       index.json with each request's plan id and body fingerprint.
  by-hand/<post>.md    accounts posted in the app: the file, caption, settings, steps in order.
  approval/<post>.md   when the brief wants the brand's approval: the packet to send.
  submit.md            each post's link, the clock time its 30 minutes run out, the steps inside them.
  deliver/             in "deliver_files" mode (the brand posts): compliance.md and manifest.json for
                       the files you hand over; no requests.
The ledger (~/.ugc-creator/ledger.json, or UGC_CREATOR_LEDGER, or --ledger) keeps every post with its
fingerprint, for every campaign. Posting is always now: a campaign post is submitted within 30
minutes of going live. Exit code 0 when there are no errors, 1 otherwise.
"""
import argparse, base64, datetime, hashlib, html, json, math, os, re, sys

sys.dont_write_bytecode = True   # nothing is ever written into the skill's own folder
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from check_videos import PRIVACY_WORDS, check_job  # noqa: E402
from campaign import deadline_end, example_demo  # noqa: E402
from ugclib import (LIMITS, MB, account_key, clock, die, guard, iso, load_saved_accounts, load_zone, money,  # noqa: E402
                    now_utc, parse_time, parse_user_time, payout, place_name, post_items, post_key, read_json, rel,
                    save_ledger, sha256, short_link, terms, threshold_views, unwrap_reply, user_home, write_json,
                    upload_record, write_text)

DEMO_NOTE = ("EXAMPLE ONLY: a made-up demo campaign. The brand, the app, the accounts and the links are invented, "
             "nothing here is a real ad, the creator's half is a placeholder, and NASA endorses nothing.")
MARK = "<!-- written by plan.py; it replaces this file on every run -->"
SHOT_HOURS = (24, 72, 168)   # screenshot times after a post goes live, merged with any the brief names


def esc(s):
    return html.escape(str(s), quote=True)


def plural(n, word):
    return f"{n} {word}{'' if n == 1 else 's'}"


def body_sha(body):
    return hashlib.sha256(json.dumps(body, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


# ---- what each post needs

def settings_of(r):
    """The settings the user chose for this account, as they go into the request."""
    acc, p = r["account"], r["platform"]
    if p == "TIKTOK":
        return {k: acc.get(k) for k in ("privacyLevel", "allowComment", "allowDuet", "allowStitch")}
    if p == "YOUTUBE":
        return {k: acc.get(k) for k in ("privacy", "madeForKids")}
    return {}


def settings_bits(r):
    acc, p = r["account"], r["platform"]
    bits = []
    if p == "TIKTOK":
        bits.append("seen by " + PRIVACY_WORDS.get(acc.get("privacyLevel"), "NOT CHOSEN"))
        for k, w in (("allowComment", "comments"), ("allowDuet", "duets"), ("allowStitch", "stitches")):
            v = acc.get(k)
            bits.append(f"{w} {'on' if v else 'off'}" if isinstance(v, bool) else f"{w} NOT CHOSEN")
        bits.append("branded content on (\"Paid partnership\" label)")
        bits.append("by posting, you agree to TikTok's Branded Content Policy and Music Usage Confirmation")
        bits.append("no auto music")
    if p == "INSTAGRAM":
        bits += ["Reel", "paid partnership label: you turn it on in the app"]
    if p == "YOUTUBE":
        bits.append(acc.get("privacy") or "privacy NOT CHOSEN")
        k = acc.get("madeForKids")
        bits.append(("made for kids" if k else "not made for kids") if isinstance(k, bool) else "made for kids NOT CHOSEN")
        bits.append("\"includes paid promotion\": you tick it in YouTube Studio")
    if r.get("ai") is True:
        bits.append("AI label: in YouTube Studio" if p == "YOUTUBE" else "AI label on (sent with the post)")
    return bits


def window_steps(r, camp):
    """What WoopSocial can't set and is only possible once the post is live: inside the 30 minutes."""
    p = r["platform"]
    steps = []
    if p == "INSTAGRAM":
        steps.append("Instagram: edit the Reel in the app and turn on the paid partnership label (add "
                     f"{camp.get('brand', 'the brand')} as partner if the brief asks). WoopSocial can't set it.")
    if p == "YOUTUBE":
        steps.append("YouTube: in YouTube Studio open the Short's details and tick that it includes paid promotion. "
                     "WoopSocial can't set it.")
        if r.get("ai") is True:
            steps.append("YouTube: answer Yes to \"Altered or synthetic content\" in YouTube Studio.")
    return steps


def is_by_hand(r):
    return not r["connected"]


def earnings_text(r, camp):
    rate, mn, cap, mv = terms(camp, r["platform"])
    cur = camp.get("currency", "USD")
    if camp.get("pay_per_video") and rate <= 0:
        return f"{money(float(camp['pay_per_video']), cur)} per accepted video, before the marketplace fee."
    if rate <= 0:
        return "No rate for this platform in the brief."
    fee = camp["fee_pct"]
    parts = [f"{money(rate, cur)} per 1,000 views, {fee:g}% fee" + (f" (the {money(mn, cur)} minimum applies to the amount "
                                                                      "before the fee)." if mn else ".")]
    need = threshold_views(camp, r["platform"])
    if need:
        parts.append(f"Pays nothing under {need:,} views.")
    shown = []
    for v in (1000, 10000, 100000):
        _, paid, why = payout(v, rate, mn, cap, fee, mv, cur)
        shown.append(f"{v:,} views: {money(paid, cur)}" + (" (capped)" if why == "capped" else ""))
    parts.append("; ".join(shown) + ".")
    if cap:
        parts.append(f"Cap {money(cap, cur)} per video, reached at {int(cap / rate * 1000):,} views.")
    return " ".join(parts)


def window_note(camp):
    days = int(camp["window_days"])
    if camp.get("window_from") == "threshold":
        return f"Views count for {days} days from the day a video crosses the payout threshold"
    return f"Views count for {days} days after posting"


def shot_hours(camp):
    hours = set(SHOT_HOURS)
    for p in camp.get("proof") or []:
        for n, unit in re.findall(r"(\d+)\s*(h|hours?|d|days?)\b", str(p), re.I):
            hours.add(int(n) * (24 if unit.lower().startswith("d") else 1))
    return sorted(h for h in hours if 0 < h <= 24 * 60)


def hours_label(h):
    return f"{h // 24}d" if h % 24 == 0 and h >= 168 else f"{h}h"


def before_you_post(m):
    c = m["campaign"]
    out = []
    if c.get("marketplace"):
        out.append(f"Post only from accounts connected and verified in {c['marketplace']}; posts from any other "
                   "account are rejected.")
    geo = c.get("geo")
    if isinstance(geo, dict) and geo.get("countries"):
        places = ", ".join(place_name(x) for x in geo["countries"])
        out.append(f"At least {geo['min_share']:.0%} of each video's viewers must be in {places}. Post from the accounts "
                   "whose viewers are already there, when they are awake. Never a VPN or location trick.")
    if c.get("deadline"):
        out.append(f"Deadline: {c['deadline']}" + (f" ({c['deadline_tz']})" if c.get("deadline_tz") else " (UTC)") + ".")
    if isinstance(geo, dict) and geo.get("countries"):
        night = geo_night(geo["countries"], now_utc())
        first_night = bool(night) and night[0].startswith(place_name(geo["countries"][0]) + " ")
        if night and (first_night or len(night) * 2 > len(geo["countries"])):
            out.append("Right now it is night for much of the audience the brief wants (" + ", ".join(night) + "). Posting "
                       "when they are awake gets the first views from the right countries.")
    if isinstance(c.get("eligibility"), dict) and c["eligibility"]:
        out.append("Every account meets the brief's rules for who may take part (followers, account age, country, "
                   "account type, public); you confirmed each one.")
    links = (c.get("caption") or {}).get("links") or []
    if links and c.get("links_where") in ("bio", "either"):
        out.append("Set the bio link on each account to " + ", ".join(links) + " before posting.")
    cap_advice = submission_advice(m)
    if cap_advice:
        out.append(cap_advice)
    out.append("Posting all at once means every in-app step and submission inside the same "
               f"{int(c['submit_within_minutes'])} minutes. Add \"stagger\": true to job.json to send one post at a "
               "time, each with its own clock.")
    return out


GEO_ZONES = {"US": "America/New_York", "CA": "America/Toronto", "UK": "Europe/London", "GB": "Europe/London",
             "AU": "Australia/Sydney", "NZ": "Pacific/Auckland", "DE": "Europe/Berlin", "FR": "Europe/Paris",
             "ES": "Europe/Madrid", "IT": "Europe/Rome", "NL": "Europe/Amsterdam", "BR": "America/Sao_Paulo",
             "MX": "America/Mexico_City", "IN": "Asia/Kolkata", "IE": "Europe/Dublin", "PH": "Asia/Manila"}


def geo_night(countries, now):
    """The brief's countries where it is between 0:00 and 7:00 right now, with their local time."""
    out = []
    for cc in countries:
        z = load_zone(GEO_ZONES.get(str(cc).upper(), ""))
        if z:
            t = now.astimezone(z)
            if t.hour < 7:
                out.append(f"{place_name(cc)} {t:%H:%M}")
    return out


def submission_advice(m):
    """When the brief caps submissions below the posts planned: which platforms pay most per video.
    Shown, never decided."""
    c = m["campaign"]
    mx = c.get("max_submissions")
    plats = [p for p in (c.get("platforms") or {}) if p in LIMITS]
    if not (isinstance(mx, int) and plats and len(m["rows"]) >= mx):
        return ""
    ranked = []
    for p in plats:
        rate, mn, cap, mv = terms(c, p)
        _, paid, _ = payout(10000, rate, mn, cap, c["fee_pct"], mv, c.get("currency", "USD"))
        ranked.append((paid, -threshold_views(c, p), LIMITS[p]["label"], threshold_views(c, p)))
    ranked.sort(reverse=True)
    best = ", ".join(f"{lab} ({money(paid, c.get('currency', 'USD'))} at 10,000 views, pays from {need:,})"
                     for paid, _, lab, need in ranked)
    return (f"This brief takes {mx} submission{'' if mx == 1 else 's'}. Per video, the platforms rank: {best}. A second video on the best "
            "platform can earn more than one on the weakest. Your call.")


# ---- the plan id: what the user says yes to

def plan_id(m):
    """A fingerprint of everything on the page that goes out: each post's file, caption, title, tags,
    account and settings, plus the campaign and script versions. Any change makes a new plan id."""
    parts = {"campaign": m["camp_info"]["version"], "script": m["script"]["version"], "posts": []}
    for r in sorted(m["rows"], key=lambda r: r["id"]):
        acc = r["account"]
        parts["posts"].append({"id": r["id"], "account": r["name"], "platform": r["platform"],
                               "socialAccountId": acc.get("socialAccountId"), "by_hand": acc.get("by_hand") is True,
                               "sha256": r.get("sha256"), "text": r["text"], "title": r["title"], "tags": r["tags"],
                               "settings": settings_of(r), "ai": r.get("ai")})
    return hashlib.sha256(json.dumps(parts, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()[:12]


def yes_path(job_dir):
    return os.path.join(job_dir, "yes.json")


def load_yes(job_dir):
    p = yes_path(job_dir)
    if not os.path.isfile(p):
        return None
    y = read_json(p, "the recorded yes")
    return y if isinstance(y, dict) and y.get("written_by") == "plan.py" else None


YES_HOURS = 3   # a yes is for posting now; after this it is asked again


def yes_age_ok(y):
    t = parse_time(y.get("at")) if isinstance(y, dict) else None
    return bool(t) and 0 <= (now_utc() - t).total_seconds() <= YES_HOURS * 3600


def yes_holds(m, y, fresh=True):
    """The yes still covers the plan as it is now: the same plan id, the same file fingerprints, and
    (for anything that uploads or sends) given in the last few hours."""
    if not y or y.get("plan_id") != m["plan_id"]:
        return False
    if fresh and not yes_age_ok(y):
        return False
    files = y.get("files") or {}
    return all(files.get(r["file"]) == r["sha256"] for r in m["rows"] if r.get("send"))


# ---- the request

def media_id(media, f):
    return media[f]["mediaId"] if media and media.get(f) else f"<mediaId of {f}>"


def child(r, media):
    acc, p = r["account"], r["platform"]
    t = {"platform": p, "socialAccountId": acc["socialAccountId"]}
    if p == "TIKTOK":
        # A campaign video is a paid partnership: TikTok's branded content setting is on, "Your brand" off.
        # The privacy level is the one the user chose from this account's options; it is never defaulted.
        # autoAddMusic is required by WoopSocial's schema for TikTok, and is always false.
        t.update(postType="VIDEO", postMode="DIRECT_POST", privacyLevel=acc.get("privacyLevel"),
                 allowComment=acc.get("allowComment") is True, allowDuet=acc.get("allowDuet") is True,
                 allowStitch=acc.get("allowStitch") is True, isBrandedContent=True, isYourBrand=False,
                 autoAddMusic=False, isAiGeneratedContent=r["ai"] is True)
    elif p == "INSTAGRAM":
        t.update(postType="REEL", isAiGeneratedContent=r["ai"] is True)
    elif p == "YOUTUBE":
        t.update(title=r["title"], privacy=acc.get("privacy"), madeForKids=acc.get("madeForKids") is True)
        if r["tags"]:
            t["tags"] = r["tags"]
    t["contentOverride"] = [{"text": r["text"], "media": [{"type": "MEDIA_LIBRARY", "mediaId": media_id(media, r["file"])}]}]
    return t


def body_for(batch, media):
    kids = [child(r, media) for r in batch]
    return {"content": [dict(kids[0]["contentOverride"][0])], "schedule": {"type": "PUBLISH_NOW"},
            "socialAccounts": kids}


def build_requests(rows, camp, media, stagger=False):
    """One request per round: the first post of every connected account, then the second, and so on.
    With "stagger" in job.json, one request per post, so each goes out, gets its in-app step and is
    submitted before the next."""
    if stagger:
        out = []
        for k, r in enumerate([r for r in rows if r.get("send")], 1):
            name = f"{camp.get('id', 'campaign')}{'' if k == 1 else '-' + str(k)}.json"
            out.append((name, body_for([r], media), [r]))
        return out
    queue = {}
    for r in rows:
        if r.get("send"):
            queue.setdefault(r["name"], []).append(r)
    reqs, k = [], 0
    while any(queue.values()):
        k += 1
        batch = [q.pop(0) for q in queue.values() if q]
        name = f"{camp.get('id', 'campaign')}{'' if k == 1 else '-' + str(k)}.json"
        reqs.append((name, body_for(batch, media), batch))
    return reqs


# ---- pages

def card_md(r, camp):
    out = [f"### {r['name']}{' ' + r['handle'] if r['handle'] else ''} ({r['label']}), post `{r['id']}`", ""]
    if r["posted"]:
        out += [f"Already posted: {r['posted'].get('url') or 'post ' + str(r['posted'].get('postId'))}.", ""]
    elif r.get("hand"):
        out += ["**By hand**: see `by-hand/" + r["id"] + ".md`.", ""]
    if r.get("info"):
        i = r["info"]
        out.append(f"- Video: `{r['file']}`, {i['duration']:.1f} s, {i['width']}x{i['height']}, {i['bytes'] / MB:.1f} MB, "
                   f"fingerprint {r['sha256'][:12]}" + (f", {r['layout'].replace('_', ' ')}" if r.get("layout") else ""))
    if r.get("hook"):
        out.append(f"- Opens with ({r.get('hook_id')}): \"{r['hook']}\"")
    scr = r.get("screen") or {}
    if scr.get("disclosure"):
        out.append(f"- Disclosure on screen: \"{scr['disclosure']}\" from the first frame for {scr.get('disclosure_seconds', 0):g} s"
                   + (f"; said out loud at {r['spoken_at']:.1f} s" + (" (estimated: placeholder, no audio)" if r.get("estimated")
                                                                     else "") if r.get("spoken_at") is not None else ""))
    if r["title"]:
        out.append(f"- Title: {r['title']}")
    lim = LIMITS[r['platform']].get('text') or LIMITS[r['platform']].get('text_bytes')
    out.append(f"- Caption ({r.get('count', 0)} of {lim}):")
    out += ["", "  > " + r["text"].replace("\n", "\n  > "), ""]
    if r["tags"]:
        out.append(f"- Tags: {', '.join(r['tags'])}")
    out.append("- Settings: " + "; ".join(settings_bits(r)))
    out.append("- Expected earnings: " + earnings_text(r, camp))
    lv = [x for x, _ in r["issues"]]
    out.append("- Checks: " + ("BLOCKED" if "error" in lv else "all passed" + (" (see below)" if lv else "")))
    for x, msg in r["issues"]:
        out.append(f"  - {x}: {msg}")
    win = window_steps(r, camp)
    if win:
        out.append(f"- Inside the {int(camp['submit_within_minutes'])} minutes after it is live:")
        out += [f"  - {s}" for s in win]
    out.append("")
    return out


def summary_line(m):
    rows = m["rows"]
    send = [r for r in rows if r.get("send")]
    hand = [r for r in rows if r.get("hand") and not r["posted"]]
    done = [r for r in rows if r["posted"]]
    parts = [f"{plural(len(send), 'post')} through WoopSocial", f"{len(hand)} by hand"]
    if done:
        parts.append(f"{len(done)} already posted")
    return (f"{plural(len(rows), 'video')} for {plural(len({r['name'] for r in rows}), 'account')} "
            f"({', '.join(parts)}). Everything goes out now, when you say yes, so you can submit each link within "
            f"{int(m['campaign']['submit_within_minutes'])} minutes.")


def yes_line(m):
    if m["errors"]:
        return "Nothing can be posted yet: fix the errors first. The plan id changes when anything is fixed."
    return (f"To post exactly this, say yes to plan `{m['plan_id']}`. If any video, caption or setting changes after "
            "that, the yes no longer holds and you get a new page.")


def footer_lines(c):
    return [f"Submit every link within {int(c['submit_within_minutes'])} minutes, into this campaign only, once. "
            "`submit.md` gives the clock time per post and when to take the proof screenshots.",
            f"Leave every post public and unchanged for {int(c['days_live'])} days. {window_note(c)}.",
            "Earnings are estimates: the campaign's own count decides what is paid, and many videos earn little. "
            "Never buy views or join engagement groups: it is a permanent ban on the marketplaces."]


def page_md(m):
    c = m["campaign"]
    info = m["camp_info"]
    out = [MARK, f"# UGC plan: {c.get('name', '')}", "",
           f"Campaign `{c.get('id')}` for {c.get('brand')}. Checklist version `{info['version']}`, script version "
           f"`{m['script']['version']}`. Planned {m['planned']}.", "", f"**Plan id `{m['plan_id']}`.** {yes_line(m)}", "",
           summary_line(m), ""]
    if example_demo(c):
        out += [f"**{DEMO_NOTE}**", ""]
    if m["errors"]:
        out += [f"**{len(m['errors'])} thing(s) to fix before anything can be posted.** They are listed under Checks.", ""]
    if info["hide"]:
        out += ["**Never followed:** the brief asks to hide that the videos are paid (" +
                "; ".join(f"\"{s}\"" for s, _ in info["hide"]) + "). Every video keeps its disclosure: said out loud, "
                "on screen, #ad first in the caption and the platform's paid-partnership setting.", ""]
    byp = before_you_post(m)
    if byp:
        out += ["## Before you post", ""] + [f"- {s}" for s in byp] + [""]
    for r in m["rows"]:
        out += card_md(r, c)
    other = [i for i in m["checks"] if not any((i[0], i[2]) in r["issues"] for r in m["rows"])]
    if other:
        out += ["## Checks", ""]
        for lv, w, msg in sorted(other, key=lambda i: ("error", "warning", "note").index(i[0])):
            out.append(f"- {lv}: {w}: {msg}")
        out.append("")
    if m["uploads"]:
        out += ["## Files to upload", "", "Only after the yes, once each:", ""]
        out += [f"- `{f}` ({b / MB:.1f} MB, fingerprint `{h[:16]}`)" for f, b, h in m["uploads"]]
        out += ["", "Save each upload in media.json as {\"<file>\": {\"mediaId\": ..., \"sha256\": \"<fingerprint>\"}}.", ""]
    if m["requests"]:
        out += ["## Requests", ""] + [f"- `requests/{n}`" for n in m["requests"]] + [""]
    if m["hand_files"]:
        out += ["## By hand", ""] + [f"- `{f}`" for f in m["hand_files"]] + [""]
    if m["approval_files"]:
        out += ["## For the brand's approval", "", "Send each packet before posting; record the answer in job.json.", ""]
        out += [f"- `{f}`" for f in m["approval_files"]] + [""]
    out += ["## After it's live", ""] + [f"- {s}" for s in footer_lines(c)] + [""]
    if m["connected_n"] > 2:
        out += [f"{m['connected_n']} accounts are connected. WoopSocial's free plan covers 2 social accounts; TikTok, "
                "Reels and Shorts together are 3, which needs a paid plan.", ""]
    return "\n".join(out)


CSS = """
:root{--bg:#f6f6f4;--card:#fff;--ink:#17181a;--mute:#62666d;--line:#dcdcd8;--err:#b3261e;--warn:#8a5a00;--ok:#1d6b3a;--chip:#eeeeea;--flag:#fff4e5;--yes:#fff7d6}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#141516;--card:#1d1f21;--ink:#ececec;--mute:#a1a5ab;--line:#33363a;--err:#ff8a80;--warn:#f0c060;--ok:#7fd49b;--chip:#2a2d30;--flag:#2b2416;--yes:#2e2a17}}
:root[data-theme="dark"]{--bg:#141516;--card:#1d1f21;--ink:#ececec;--mute:#a1a5ab;--line:#33363a;--err:#ff8a80;--warn:#f0c060;--ok:#7fd49b;--chip:#2a2d30;--flag:#2b2416;--yes:#2e2a17}
*{box-sizing:border-box;min-width:0}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
main{max-width:1180px;margin:0 auto;padding:24px 16px 64px;overflow-wrap:anywhere}h1{font-size:26px;margin:0 0 4px}h2{font-size:20px;margin:32px 0 6px}
.sub{color:var(--mute);margin:0 0 16px}.cards{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(min(330px,100%),1fr))}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px;display:grid;grid-template-columns:110px minmax(0,1fr);gap:14px;align-items:start}
.card img{width:100%;border-radius:8px;display:block;background:#000}.noimg{aspect-ratio:9/16;border:1px dashed var(--line);border-radius:8px}
.card h3{margin:0;font-size:16px}.meta{color:var(--mute);font-size:13px;margin:2px 0 8px}.text{white-space:pre-wrap;margin:6px 0 8px;font-size:15px}
.title{font-weight:650;margin:6px 0 0}.chips{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0}.chip{background:var(--chip);border-radius:999px;padding:2px 10px;font-size:13px}
.k{font-size:13px;color:var(--mute);margin:8px 0 2px;font-weight:600;text-transform:uppercase;letter-spacing:.04em}.small{font-size:14px;margin:0}
.state{font-weight:650;font-size:14px}.okc{color:var(--ok)}.error{color:var(--err)}.warning{color:var(--warn)}.note{color:var(--mute)}.hand{color:var(--warn)}
ul{padding-left:20px;margin:6px 0}.banner{border-radius:12px;padding:12px 16px;margin:0 0 10px;border:1px solid var(--line);background:var(--card)}
.flag{background:var(--flag)}.yes{background:var(--yes);font-size:17px}code{font-size:14px}.card ul{font-size:14px}
@media (max-width:520px){.card{grid-template-columns:minmax(0,1fr)}.card>div:first-child{max-width:140px}}
"""


def page_html(m):
    c = m["campaign"]
    info = m["camp_info"]
    out = ["<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">", MARK,
           "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>UGC plan</title>",
           f"<style>{CSS}</style></head><body><main>", f"<h1>UGC plan: {esc(c.get('name', ''))}</h1>",
           f"<p class=\"sub\">Campaign <code>{esc(c.get('id'))}</code> for {esc(c.get('brand'))}. Planned "
           f"{esc(m['planned'])}.<br>{esc(summary_line(m))}</p>",
           f"<div class=\"banner yes\"><strong>Plan id <code>{esc(m['plan_id'])}</code>.</strong> "
           f"{esc(yes_line(m)).replace('`', '')}</div>"]
    if example_demo(c):
        out.append(f"<div class=\"banner\"><strong>EXAMPLE ONLY:</strong> {esc(DEMO_NOTE[len('EXAMPLE ONLY: '):])}</div>")
    if m["errors"]:
        out.append(f"<div class=\"banner error\"><strong>{len(m['errors'])} thing(s) to fix before anything can be "
                   "posted.</strong> They are listed on the cards and under Checks.</div>")
    if info["hide"]:
        out.append("<div class=\"banner flag\"><strong>Never followed:</strong> the brief asks to hide that the videos "
                   "are paid (" + "; ".join(f"&ldquo;{esc(s)}&rdquo;" for s, _ in info["hide"]) + "). Every video keeps "
                   "its disclosure: said out loud, on screen, #ad first in the caption and the platform's "
                   "paid-partnership setting.</div>")
    byp = before_you_post(m)
    if byp:
        out.append("<div class=\"banner\"><strong>Before you post</strong><ul>" + "".join(f"<li>{esc(s)}</li>" for s in byp)
                   + "</ul></div>")
    out.append("<div class=\"cards\">")
    for r in m["rows"]:
        img = "<div class=\"noimg\"></div>"
        if r.get("cover") and os.path.isfile(r["cover"]) and os.path.getsize(r["cover"]) < 400 * 1000:
            with open(r["cover"], "rb") as fh:
                src = "data:image/jpeg;base64," + base64.b64encode(fh.read()).decode("ascii")
            img = f"<img src=\"{src}\" alt=\"Frame of {esc(r['id'])}\">"
        lv = [x for x, _ in r["issues"]]
        if r["posted"]:
            state = "<span class=\"state okc\">already posted</span>"
        elif "error" in lv:
            state = "<span class=\"state error\">blocked</span>"
        else:
            state = "<span class=\"state okc\">all checks passed</span>" + (
                " <span class=\"state hand\">by hand</span>" if r.get("hand") else "")
        meta = [r["label"], f"post {r['id']}"]
        if r.get("info"):
            meta.append(f"{r['info']['duration']:.1f} s")
        if r.get("layout"):
            meta.append(r["layout"].replace("_", " "))
        out.append(f"<div class=\"card\"><div>{img}</div><div>")
        out.append(f"<h3>{esc(r['name'])} {esc(r['handle'])}</h3><div class=\"meta\">{esc(' · '.join(meta))}</div>{state}")
        if r.get("hook"):
            out.append(f"<p class=\"k\">Opens with</p><p class=\"small\">{esc(r['hook'])}</p>")
        scr = r.get("screen") or {}
        if scr.get("disclosure"):
            said = (f"; said out loud at {r['spoken_at']:.1f} s" + (" (estimated: placeholder, no audio)" if r.get("estimated")
                                                                   else "")) if r.get("spoken_at") is not None else ""
            out.append(f"<p class=\"k\">Disclosure</p><p class=\"small\">&ldquo;{esc(scr['disclosure'])}&rdquo; from the "
                       f"first frame for {scr.get('disclosure_seconds', 0):g} s{esc(said)}</p>")
        out.append("<p class=\"k\">" + ("Title and description" if r["platform"] == "YOUTUBE" else "Caption") + "</p>")
        if r["title"]:
            out.append(f"<p class=\"title\">{esc(r['title'])}</p>")
        out.append(f"<p class=\"text\">{esc(r['text'])}</p>")
        out.append("<div class=\"chips\">" + "".join(f"<span class=\"chip\">{esc(b)}</span>" for b in settings_bits(r))
                   + "</div>")
        out.append(f"<p class=\"k\">Expected earnings</p><p class=\"small\">{esc(earnings_text(r, c))}</p>")
        if r["issues"]:
            out.append("<ul>" + "".join(f"<li class=\"{x}\">{esc(msg)}</li>" for x, msg in r["issues"]) + "</ul>")
        win = window_steps(r, c)
        if win:
            out.append(f"<p class=\"k\">Inside the {int(c['submit_within_minutes'])} minutes</p><ul>"
                       + "".join(f"<li>{esc(s)}</li>" for s in win) + "</ul>")
        out.append("</div></div>")
    out.append("</div>")
    other = [i for i in m["checks"] if not any((i[0], i[2]) in r["issues"] for r in m["rows"])]
    if other:
        out.append("<h2>Checks</h2><ul>")
        for lv, w, msg in sorted(other, key=lambda i: ("error", "warning", "note").index(i[0])):
            out.append(f"<li class=\"{lv}\"><strong>{esc(w)}</strong>: {esc(msg)}</li>")
        out.append("</ul>")
    if m["uploads"]:
        out.append("<h2>Files to upload</h2><p class=\"sub\">Only after the yes, once each:</p><ul>"
                   + "".join(f"<li><code>{esc(f)}</code> ({b / MB:.1f} MB, fingerprint <code>{esc(h[:16])}</code>)</li>"
                             for f, b, h in m["uploads"]) + "</ul>")
    if m["hand_files"]:
        out.append("<h2>By hand</h2><ul>" + "".join(f"<li><code>{esc(f)}</code></li>" for f in m["hand_files"]) + "</ul>")
    if m["approval_files"]:
        out.append("<h2>For the brand's approval</h2><ul>"
                   + "".join(f"<li><code>{esc(f)}</code></li>" for f in m["approval_files"]) + "</ul>")
    out.append("<h2>After it's live</h2><ul>" + "".join(
        f"<li>{esc(s).replace('`submit.md`', '<code>submit.md</code>')}</li>" for s in footer_lines(c)) + "</ul>")
    if m["connected_n"] > 2:
        out.append(f"<p class=\"sub\">{m['connected_n']} accounts are connected. WoopSocial's free plan covers 2 social "
                   "accounts; TikTok, Reels and Shorts together are 3, which needs a paid plan.</p>")
    out.append("</main></body></html>")
    return "\n".join(out)


def hand_page(r, camp):
    acc = r["account"]
    win = int(camp["submit_within_minutes"])
    out = [MARK, f"# {r['name']}{' ' + r['handle'] if r['handle'] else ''}: post `{r['id']}` by hand", "",
           f"Campaign: {camp.get('name')} (`{camp.get('id')}`).", ""]
    if example_demo(camp):
        out += [f"**{DEMO_NOTE}**", ""]
    out += ["## Before you post", ""]
    steps = [f"Put `{r.get('file')}` on your phone (AirDrop, cloud drive, or a cable). Post this exact file: don't trim, "
             "filter, add music or re-edit it in the app. It is the file the checks and your yes were for."]
    if camp.get("marketplace"):
        steps.append(f"Post from this account only if it is connected and verified in {camp['marketplace']}.")
    out += [f"{n}. {s}" for n, s in enumerate(steps, 1)] + ["", "## Post it", ""]
    post = []
    if r["platform"] == "TIKTOK":
        post.append(f"Paste the caption below. Who can see it: {PRIVACY_WORDS.get(acc.get('privacyLevel'), 'ask the account owner')}; "
                    f"comments {'on' if acc.get('allowComment') else 'off'}, duets {'on' if acc.get('allowDuet') else 'off'}, "
                    f"stitches {'on' if acc.get('allowStitch') else 'off'}.")
        post.append("Under more options, turn on the content disclosure setting and choose paid partnership (branded content).")
        if r.get("ai") is True:
            post.append("Turn on the AI-generated content label.")
        post.append("Post.")
    elif r["platform"] == "INSTAGRAM":
        post.append("New Reel, paste the caption below, and turn on the paid partnership label (add the brand as partner if "
                    "the brief asks).")
        if r.get("ai") is True:
            post.append("Turn on the AI label.")
        post.append("Share.")
    else:
        post.append(f"Upload it as a Short. Title and description below; visibility {acc.get('privacy', 'public')}; "
                    f"{'made for kids' if acc.get('madeForKids') else 'not made for kids'}; tick that it includes paid "
                    "promotion.")
        if r.get("ai") is True:
            post.append("Answer Yes to \"Altered or synthetic content\".")
        post.append("Publish.")
    out += [f"{n}. {s}" for n, s in enumerate(post, 1)] + ["", f"## Right after (you have {win} minutes)", ""]
    after = ["Copy the post's link from the share menu and paste it back to your agent. It records the post and tells "
             "you the exact time your window closes.",
             f"Submit the link to the campaign within {win} minutes of it going live, into this campaign only, once.",
             "Tell your agent it is submitted (with the submission id if the campaign shows one)."]
    out += [f"{n}. {s}" for n, s in enumerate(after, 1)] + [""]
    out += (["## Title", "", r["title"], ""] if r["title"] else [])
    out += ["## Caption" if r["platform"] != "YOUTUBE" else "## Description", "", "```", r["text"], "```", ""]
    if r["tags"]:
        out += ["## Tags", "", ", ".join(r["tags"]), ""]
    out += [f"Expected earnings: {earnings_text(r, camp)} {window_note(camp)}; the campaign's own count decides.", ""]
    return "\n".join(out)


def approval_page(r, camp):
    scr = r.get("screen") or {}
    out = [MARK, f"# For approval: `{r['id']}` ({r['label']}, {r['name']}{' ' + r['handle'] if r['handle'] else ''})", "",
           f"Campaign: {camp.get('name')} (`{camp.get('id')}`). Send the video and this text to the brand where the brief "
           "says (the marketplace chat, email). Post only after a clear yes.", "",
           f"- Video: `{r.get('file')}`, {r['info']['duration']:.1f} s, fingerprint `{r['sha256'][:12]}`"]
    if r.get("hook"):
        out.append(f"- Opens with: \"{r['hook']}\"")
    if scr.get("disclosure"):
        out.append(f"- Disclosure: \"{scr['disclosure']}\" on screen for {scr.get('disclosure_seconds', 0):g} s and said out loud")
    if r["title"]:
        out.append(f"- Title: {r['title']}")
    out += ["", "## Caption", "", "```", r["text"], "```", "", "## Message to paste", "", "```",
            f"Hi! Draft for {camp.get('name')} on {r['label']} ({r['handle'] or r['name']}). Video attached "
            f"(fingerprint {r['sha256'][:12]}), caption below. OK to post as is?", "", r["text"], "```", "",
            "## When they answer", "",
            "Tell your agent who approved it and when. It records this in job.json as "
            f"`\"approved\": {{\"by\": \"<name>\", \"at\": \"<time>\", \"sha256\": \"{r['sha256'][:12]}\"}}`. A file changed "
            "after that is stopped until the new version is approved too. Keep their message.", ""]
    return "\n".join(out)


def deliver_pages(m):
    """deliver_files mode: the brand posts the videos. compliance.md and manifest.json for the files you
    hand over; nothing is posted."""
    c, job_dir = m["campaign"], m["job_dir"]
    out = [MARK, f"# Delivery: {c.get('name')}", "", f"Campaign `{c.get('id')}` for {c.get('brand')}. The brand posts "
           "these videos from its own accounts; nothing is posted from yours.", ""]
    if example_demo(c):
        out += [f"**{DEMO_NOTE}**", ""]
    man = {"campaign": c.get("id"), "brand": c.get("brand"), "script_version": m["script"]["version"], "videos": []}
    for r in m["rows"]:
        if not r.get("sha256"):
            continue
        scr = r.get("screen") or {}
        out += [f"## `{r['file']}`", "", f"- Fingerprint (SHA-256): `{r['sha256']}`",
                f"- Length {r['info']['duration']:.1f} s, {r['info']['width']}x{r['info']['height']}",
                f"- Disclosure on screen: \"{scr.get('disclosure')}\" from the first frame for "
                f"{scr.get('disclosure_seconds', 0):g} s; said out loud at "
                + (f"{r['spoken_at']:.1f} s" if r.get("spoken_at") is not None else "(not found)"),
                f"- Suggested caption: {r['text']}" if r["text"] else "- Suggested caption: none",
                "- Checks: " + ("BLOCKED" if any(x == "error" for x, _ in r["issues"]) else "all passed"), ""]
        man["videos"].append({"file": r["file"], "sha256": r["sha256"], "seconds": r["info"]["duration"],
                              "on_screen": scr, "spoken_disclosure_s": r.get("spoken_at"), "caption": r["text"]})
    out += ["When the brand posts these, the disclosure stays: #ad first in the caption and the platform's paid "
            "partnership setting. The skill never agrees to a video without it.", ""]
    write_text(os.path.join(job_dir, "deliver", "compliance.md"), "\n".join(out))
    write_json(os.path.join(job_dir, "deliver", "manifest.json"), man)


def ours(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return MARK in fh.read(4000)
    except OSError:
        return False


def clear_old(job_dir):
    """Remove what the run before wrote (only files this script wrote), so a plan that stops on an error
    never leaves an old request that could still be sent."""
    req_dir = os.path.join(job_dir, "requests")
    for d in ("requests", "by-hand", "approval", "deliver"):
        full = os.path.join(job_dir, d)
        if os.path.lexists(full) and not os.path.isdir(full):
            die(f"{d} is a file here, and plan.py needs a folder with that name. Move or rename the file")
    for f in ("plan.md", "plan.html"):
        full = os.path.join(job_dir, f)
        if os.path.isfile(full) and not ours(full):
            die(f"{f} here wasn't written by plan.py, and planning would replace it. Rename your own {f}")
    if os.path.isdir(req_dir):
        old = [f for f in os.listdir(req_dir) if f.endswith(".json")]
        if old and "index.json" not in old:
            die("the folder requests/ here holds JSON files that plan.py didn't write. Move them somewhere else")
        if old:
            # kept, not deleted: a request sent just before this run can still be recorded with --posted
            idx = read_json(os.path.join(req_dir, "index.json"), "the request index")
            pid = str(idx.get("plan_id") if isinstance(idx, dict) else "") or "unknown"
            arch = os.path.join(job_dir, "requests-old", re.sub(r"[^\w-]", "", pid) or "unknown")
            os.makedirs(arch, exist_ok=True)
            for f in old:
                os.replace(os.path.join(req_dir, f), os.path.join(arch, f))
        if not os.listdir(req_dir):
            os.rmdir(req_dir)
    for d in ("by-hand", "approval", "deliver"):
        full = os.path.join(job_dir, d)
        if os.path.isdir(full):
            for f in os.listdir(full):
                p = os.path.join(full, f)
                if (f.endswith(".md") and ours(p)) or (d == "deliver" and f == "manifest.json"):
                    os.remove(p)
            if not os.listdir(full):
                os.rmdir(full)
    for f in ("plan.md", "plan.html"):
        if os.path.isfile(os.path.join(job_dir, f)):
            os.remove(os.path.join(job_dir, f))


def load_media(arg, job_dir, files):
    """media.json: {"<file>": {"mediaId": ..., "sha256": "<the fingerprint plan.md lists>"}}. A video
    edited again under the same name is refused, so a post never carries another cut than the one the
    user said yes to."""
    path = arg if os.path.isfile(arg) else os.path.join(job_dir, arg)
    media = read_json(path, "the uploaded media ids")
    form = "{\"<file as plan.md lists it>\": {\"mediaId\": \"<mediaId>\", \"sha256\": \"<its fingerprint>\"}}"
    if not isinstance(media, dict):
        die(f"{arg} must be {form}")
    media = {str(k).replace("\\", "/").lstrip("./") if str(k).startswith("./") else str(k).replace("\\", "/"): v
             for k, v in media.items()}
    for k, v in media.items():
        if not isinstance(v, dict) or not isinstance(v.get("mediaId"), str) or not v["mediaId"].strip():
            die(f"{arg} must be {form}; {k} has no mediaId")
        if not isinstance(v.get("sha256"), str) or len(v["sha256"].strip()) < 12:
            die(f"{arg}: {k} needs \"sha256\", the fingerprint upload_parts.py printed (12 characters or more)")
    unknown = [k for k in media if k not in files]
    if unknown:
        die(f"{arg} names {', '.join(unknown)}, which isn't a file of this plan ({', '.join(files) or 'none'})")
    missing = [f for f in files if f not in media]
    if missing:
        die(f"{arg} has no mediaId for {', '.join(missing)}. Upload each file under \"Files to upload\" once")
    changed = [f for f in files if not sha256(os.path.join(job_dir, f)).startswith(media[f]["sha256"].strip().lower())]
    if changed:
        die(f"{', '.join(changed)} changed after it was uploaded. Upload it again, and show the plan for a new yes")
    # the fingerprint must come from the upload itself: upload_parts.py writes uploaded.json next to the file
    for f in files:
        full = os.path.join(job_dir, f)
        got = upload_record(full)
        if not got:
            die(f"{f}: no upload of this exact file on record (uploaded.json next to it, written by upload_parts.py). "
                "Upload it with upload_parts.py, so the fingerprint is read from the bytes that went up")
        sid = media[f].get("uploadSessionId")
        if sid is not None and got.get("uploadSessionId") not in (None, sid):
            die(f"{f}: media.json names upload session {sid}, and upload_parts.py uploaded it in {got.get('uploadSessionId')}")
        # the mediaId is bound to the file it was uploaded from: upload_parts.py --complete records it
        if not got.get("mediaId"):
            die(f"{f}: no mediaId recorded for this upload. Save the reply of media_uploads_complete_session (READY) and "
                f"run: upload_parts.py --complete reply.json {f}")
        if got["mediaId"] != media[f]["mediaId"].strip():
            die(f"{f}: media.json gives mediaId {media[f]['mediaId']}, and the upload of this file recorded "
                f"{got['mediaId']}. A mediaId belongs to the file it was uploaded from; fix media.json")
    return media


def model(job_path, ledger_file=None):
    m = check_job(job_path, ledger_file)
    for r in m["rows"]:
        r.setdefault("text", "")
        r.setdefault("title", "")
        r.setdefault("tags", [])
        r["hand"] = is_by_hand(r) and not r["posted"] and not m["deliver"]
        r["send"] = bool(r.get("file")) and not r["hand"] and not r["posted"] and not m["deliver"]
    m["errors"] = [i for i in m["checks"] if i[0] == "error"]
    m["plan_id"] = plan_id(m)
    return m


def pending_for(ledger, camp_id):
    return {k: v for k, v in (ledger.get("pending") or {}).items() if isinstance(v, dict) and v.get("campaign") == camp_id}


def plan(job_path, media_arg=None, ledger_file=None):
    m = check_job(job_path, ledger_file)
    job_dir, camp = m["job_dir"], m["campaign"]
    pend = pending_for(m["ledger"], camp.get("id"))
    if pend:
        k, v = next(iter(pend.items()))
        die(f"request {v.get('request')} was checked for sending at {v.get('at')} and never recorded. If it went out: "
            f"plan.py {rel(job_path)} --posted {v.get('path') or v.get('request')} <postId>. If it didn't (look with "
            f"social_account_posts_list first): plan.py {rel(job_path)} --not-sent {v.get('request')} --checked. "
            "Nothing is planned again until then, so nothing goes out twice")
    clear_old(job_dir)
    m = model(job_path, ledger_file)   # again, after clearing: nothing from the run before is read
    errs = m["errors"]
    files = sorted({r["file"] for r in m["rows"] if r.get("send")})
    y = load_yes(job_dir)
    media = {}
    if media_arg:
        if errs:
            die("the plan has errors, so nothing is uploaded or sent. Run plan.py without --media and fix them")
        if not yes_holds(m, y):
            die(f"there is no yes for plan {m['plan_id']} as it is now" + (
                f" (the yes was for plan {y.get('plan_id')}, and something changed since)" if y else "") +
                ". Show plan.html, and after a clear yes run: plan.py job.json --yes " + m["plan_id"])
        media = load_media(media_arg, job_dir, files)
    m["uploads"] = [(f, os.path.getsize(os.path.join(job_dir, f)), sha256(os.path.join(job_dir, f))) for f in files]
    zone = m["job"].get("timezone")
    m["planned"] = clock(now_utc(), zone)
    m["connected_n"] = len({r["name"] for r in m["rows"] if r["connected"]})
    m["requests"], m["hand_files"], m["approval_files"] = [], [], []
    for r in m["rows"]:
        if r.get("needs_approval") and r.get("file") and not r["posted"]:
            path = os.path.join(job_dir, "approval", f"{r['id']}.md")
            write_text(path, approval_page(r, camp))
            m["approval_files"].append(rel(path, job_dir))
    if not errs:
        if media_arg:
            index = {"plan_id": m["plan_id"], "campaign": camp.get("id"), "requests": {}, "media": media}
            for name, body, batch in build_requests(m["rows"], camp, media, m["job"].get("stagger") is True):
                write_json(os.path.join(job_dir, "requests", name), body)
                m["requests"].append(name)
                index["requests"][name] = {"body_sha256": body_sha(body), "posts": [
                    {"post": r["id"], "account": r["name"], "socialAccountId": r["account"]["socialAccountId"],
                     "platform": r["platform"], "file": r["file"], "sha256": r["sha256"], "handle": r["handle"],
                     "takes": r.get("takes") or [], "fps": r.get("fps") or [], "hook": r.get("hook"),
                     "hook_id": r.get("hook_id"), "caption": r["text"]} for r in batch]}
            if index["requests"]:
                write_json(os.path.join(job_dir, "requests", "index.json"), index)
        if yes_holds(m, y):   # only a fresh yes: by-hand pages are never written again from an old one
            write_hand_pages(m, y)
        if m["deliver"]:
            deliver_pages(m)
    write_text(os.path.join(job_dir, "plan.md"), page_md(m))
    write_text(os.path.join(job_dir, "plan.html"), page_html(m))
    warns = [i for i in m["checks"] if i[0] == "warning"]
    print(f"{plural(len(m['rows']), 'video')} planned -> plan.md, plan.html ({len(errs)} errors, {len(warns)} warnings); "
          f"plan id {m['plan_id']}")
    if zone and load_zone(zone) is None:
        print(f"warning: the time zone {zone} can't be loaded here, so times are shown in UTC. On Windows: pip install tzdata")
    if m["camp_info"]["hide"]:
        print(f"never followed: {len(m['camp_info']['hide'])} brief sentence(s) asking to hide the ad")
    if m["approval_files"]:
        print(f"for approval ({len(m['approval_files'])}): approval/ (send each packet to the brand)")
    if errs:
        print("fix every error (listed on the plan) and run this again. No request was written")
        for lv, w, msg in errs:
            print(f"  error: {w}: {msg}")
        sys.exit(1)
    if m["deliver"]:
        print("deliver_files: deliver/compliance.md and deliver/manifest.json for the files you hand over. Nothing is "
              "posted from your accounts")
        return
    if m["hand_files"]:
        print(f"by hand ({len(m['hand_files'])}): by-hand/")
    if m["requests"]:
        print("requests: " + ", ".join("requests/" + n for n in m["requests"]))
        print(f"next: for each request, plan.py {rel(job_path)} --check requests/<name>.json, then posts_validate and "
              f"posts_create, and right after: plan.py {rel(job_path)} --posted requests/<name>.json <postId>")
    elif files and yes_holds(m, y):
        print("the yes holds. Upload each file under \"Files to upload\" once (upload_parts.py prints its fingerprint), "
              f"save {{file: {{mediaId, sha256}}}} as media.json, and run: plan.py {rel(job_path)} --media media.json")
    elif files:
        print(f"next: show plan.html (or paste plan.md) and wait for a clear yes to plan {m['plan_id']}. Then: plan.py "
              f"{rel(job_path)} --yes {m['plan_id']}. Nothing is uploaded or posted before that")
    elif m["hand_files"]:
        print("next: show plan.html and wait for a clear yes; then hand over the by-hand pages")
    else:
        print("nothing left to post: every video in this job is recorded in the ledger")


def write_hand_pages(m, y):
    """The by-hand pages: written only once the user said yes to the plan that lists them."""
    for r in m["rows"]:
        if r["hand"] and r.get("file") and r["id"] in (y.get("by_hand") or []):
            path = os.path.join(m["job_dir"], "by-hand", f"{r['id']}.md")
            write_text(path, hand_page(r, m["campaign"]))
            m["hand_files"].append(rel(path, m["job_dir"]))


def record_yes(job_path, given, ledger_file=None):
    m = model(job_path, ledger_file)
    if m["errors"]:
        die("the plan has errors, so there is nothing to say yes to. Run plan.py and fix them")
    given = (given or "").strip()
    if given != m["plan_id"]:
        die(f"plan {given} isn't the plan as it is now (it is {m['plan_id']}: something changed since the page was "
            "made). Run plan.py, show the new page, and ask again")
    if m["deliver"]:
        die("deliver_files: the brand posts these, so there is no posting yes to record")
    files = {r["file"]: r["sha256"] for r in m["rows"] if r.get("send")}
    hand = [r["id"] for r in m["rows"] if r.get("hand")]
    y = {"written_by": "plan.py", "plan_id": m["plan_id"], "at": iso(now_utc()), "campaign": m["campaign"].get("id"),
         "files": files, "by_hand": hand}
    write_json(yes_path(m["job_dir"]), y)
    m["hand_files"] = []
    write_hand_pages(m, y)
    if m["hand_files"]:
        print("by hand: " + ", ".join(m["hand_files"]))
    print(f"recorded: yes to plan {m['plan_id']} ({plural(len(files), 'file')} through WoopSocial, {len(hand)} by hand). "
          f"It holds only while every file, caption and setting stays exactly as on the page, for {YES_HOURS} hours")
    if files:
        print("next: upload each file once (upload_parts.py or media_uploads), save media.json, and run: plan.py "
              f"{rel(job_path)} --media media.json")


def verify(job_path, request, ledger_file=None, sending=True):
    """Everything a request must pass right before it is sent: written by this plan, not edited since,
    the yes still holds for exactly these files and captions, no check fails."""
    m = model(job_path, ledger_file)
    job_dir = m["job_dir"]
    rdir = os.path.join(job_dir, "requests")
    rpath = request if os.path.isfile(request) else os.path.join(job_dir, request)
    name = os.path.basename(rpath)
    idx_path = os.path.join(rdir, "index.json")
    if not os.path.isfile(idx_path) or not os.path.isfile(rpath):
        die(f"{request} isn't a request plan.py wrote for this plan as it is now (requests are removed whenever the plan "
            "is made again). Nothing to send")
    idx = read_json(idx_path, "the request index")
    meta = (idx.get("requests") or {}).get(name) if isinstance(idx, dict) else None
    if not meta or idx.get("campaign") != m["campaign"].get("id"):
        die(f"{name} isn't one of this plan's requests")
    body = read_json(rpath, "the request")
    if body_sha(body) != meta.get("body_sha256"):
        die(f"{name} was edited after plan.py wrote it. It is not sent. Change job.json instead and plan again")
    if idx.get("plan_id") != m["plan_id"]:
        die(f"the plan changed after this request was written (plan {idx.get('plan_id')} then, {m['plan_id']} now): a "
            "video, caption or setting is different. It is not sent. Plan again, show the new page, ask for a new yes")
    # never trust the index alone: the body is built again from the job as it is now
    rows_now = {r["id"]: r for r in m["rows"]}
    batch = [rows_now.get(x.get("post")) for x in meta.get("posts") or []]
    if not batch or None in batch or any(not r.get("connected") for r in batch):
        die(f"{name} names posts this job doesn't send through WoopSocial now. It is not sent")
    # the media ids come from the upload records next to the files, never from index.json
    media_now = {}
    for r in batch:
        got = upload_record(os.path.join(job_dir, r["file"]))
        if not got or not got.get("mediaId"):
            die(f"{r['file']}: no upload with a recorded mediaId for this exact file (upload_parts.py --complete). It is "
                "not sent")
        media_now[r["file"]] = {"mediaId": got["mediaId"]}
    if body_sha(body_for(batch, media_now)) != body_sha(body):
        die(f"{name} isn't what the job builds now (an account, a setting, a caption or a media id differs). It is not "
            "sent. Plan again")
    y = load_yes(job_dir)
    if not yes_holds(m, y):
        die(f"there is no yes for plan {m['plan_id']} as it is now" + (
            f" (the yes is more than {YES_HOURS} hours old: show the page and ask again)" if yes_holds(m, y, False)
            else "") + ". It is not sent")
    if m["errors"]:
        die("a check fails now: " + "; ".join(f"{w}: {msg}" for _, w, msg in m["errors"][:3]) + ". It is not sent")
    rows = {r["id"]: r for r in m["rows"]}
    for x in meta["posts"]:
        r = rows.get(x.get("post"))
        if r is None or r.get("sha256") != x.get("sha256"):
            die(f"post {x.get('post')} isn't the file the yes was for any more. It is not sent")
        if r["posted"]:
            die(f"post {x.get('post')} on {r['name']} is already recorded as posted. Nothing goes out twice")
    if sending and m["demo"]:
        die("this is the skill's example campaign (example_demo): nothing is ever sent from it")
    return m, name, meta


def find_request(job_dir, request):
    """(path, index) of a request plan.py wrote: in requests/, or archived in requests-old/<plan id>/
    by a later plan run."""
    cands = [request if os.path.isabs(request) else os.path.join(job_dir, request),
             os.path.join(job_dir, "requests", os.path.basename(request))]
    old = os.path.join(job_dir, "requests-old")
    if os.path.isdir(old):
        cands += [os.path.join(old, d, os.path.basename(request)) for d in sorted(os.listdir(old))]
    for c in cands:
        ip = os.path.join(os.path.dirname(c), "index.json")
        if os.path.isfile(c) and os.path.isfile(ip):
            idx = read_json(ip, "the request index")
            if isinstance(idx, dict) and os.path.basename(c) in (idx.get("requests") or {}):
                return c, idx
    die(f"{request} isn't a request plan.py wrote here (not in requests/ or requests-old/)")


def check_request(job_path, request, ledger_file=None):
    m, name, meta = verify(job_path, request, ledger_file)
    led = m["ledger"]
    led.setdefault("pending", {})[f"{m['campaign'].get('id')}:{name}"] = {
        "campaign": m["campaign"].get("id"), "request": name, "path": rel(os.path.join(m["job_dir"], "requests", name),
                                                                          m["job_dir"]),
        "plan_id": m["plan_id"], "posts": [x["post"] for x in meta["posts"]], "at": iso(now_utc())}
    save_ledger(m["ledger_path"], led)
    print(f"ok: {name} is exactly what the user said yes to (plan {m['plan_id']}): "
          + ", ".join(f"{x['post']} on {x['account']}" for x in meta["posts"]) + ". Send it now with posts_validate, "
          f"then posts_create, and record it right away with --posted {name} <postId> (until then nothing is planned "
          "again)")


def not_sent(job_path, request, checked=False, ledger_file=None):
    """--not-sent: a checked request that never went out. Only after looking on the account."""
    m = check_job(job_path, ledger_file)
    led = m["ledger"]
    key = f"{m['campaign'].get('id')}:{os.path.basename(request)}"
    if key not in led.get("pending", {}):
        die(f"{request} isn't waiting to be recorded")
    if not checked:
        die("first call social_account_posts_list for each account in the request and look at the last hour. Only when "
            "the video isn't there, run this again with --checked")
    del led["pending"][key]
    save_ledger(m["ledger_path"], led)
    print(f"cleared: {os.path.basename(request)} didn't go out. Plan again; a new yes is needed before sending")


# ---- after posting

def remember_campaign(ledger, camp):
    keep = ("id", "name", "brand", "marketplace", "currency", "platforms", "min_payout", "min_views", "cap_per_video",
            "budget_total", "fee_pct", "window_days", "window_from", "days_live", "submit_within_minutes", "geo",
            "pay_per_video", "example_demo", "budget_remaining", "budget_checked_at", "max_submissions", "deadline",
            "deadline_tz", "doc_only_rules")
    ledger["campaigns"][camp.get("id")] = {k: camp.get(k) for k in keep if camp.get(k) is not None}


def entry_for(r, camp, post_id, sid, now, zone=None, plan=None):
    return {"postId": post_id, "job_post": r["id"], "campaign": camp.get("id"), "account": r["name"],
            "handle": r["handle"], "platform": r["platform"], "socialAccountId": sid, "file": r["file"],
            "sha256": r["sha256"], "takes": r.get("takes") or [], "fps": r.get("fps") or [], "hook": r.get("hook"),
            "hook_id": r.get("hook_id"),
            "caption": r["text"], "spoken_disclosure_s": r.get("spoken_at"),
            "plan_id": plan, "submit_within": int(camp["submit_within_minutes"]), "recorded": iso(now), "url": None,
            "published_at": None, "timezone": zone}


def evidence_dirs(job_dir, posts):
    for p in posts:
        os.makedirs(os.path.join(job_dir, "proof", p), exist_ok=True)


def record_posted(job_path, request, post_id, ledger_file=None):
    post_id = (post_id or "").strip()
    if not post_id:
        die("give the post id that posts_create returned: --posted requests/<name>.json <postId>")
    # A request that went out is always recorded, whatever changed since: a post that isn't in the
    # ledger would be planned and sent again. Only "plan.py wrote this request" is checked.
    job_dir = os.path.dirname(os.path.abspath(job_path))
    rpath, idx = find_request(job_dir, request)
    name = os.path.basename(rpath)
    meta = idx["requests"][name]
    m = model(job_path, ledger_file)
    camp = m["campaign"]
    warnings = []
    if body_sha(read_json(rpath, "the request")) != meta.get("body_sha256"):
        warnings.append(f"{name} was edited after plan.py wrote it")
    if idx.get("plan_id") != m["plan_id"]:
        warnings.append(f"the plan changed since this request was written (plan {idx.get('plan_id')} then, "
                        f"{m['plan_id']} now)")
    warnings += [f"{w}: {msg}" for _, w, msg in m["errors"]]
    rows = {r["id"]: r for r in m["rows"]}
    ledger = m["ledger"]
    now = now_utc()
    for x in meta["posts"]:
        key = f"{post_id}|{x['socialAccountId']}"
        if key in ledger["posts"]:
            die(f"{x['post']} on {x['account']} is already recorded as post {post_id}")
        for k, e in ledger["posts"].items():
            if e.get("campaign") == camp.get("id") and e.get("job_post") == x["post"] and \
                    e.get("account") == x["account"]:
                die(f"{x['post']} on {x['account']} is already recorded (as post {e.get('postId') or k}). One request is "
                    "recorded once; if a second post really went out, delete it on the platform")
    for x in meta["posts"]:
        r = rows.get(x["post"])
        if r is None or r.get("sha256") != x.get("sha256"):
            warnings.append(f"post {x['post']} in the job is no longer the file that was sent; recorded from the request")
            r = {"id": x["post"], "name": x["account"], "handle": x.get("handle") or "", "platform": x["platform"],
                 "file": x["file"], "sha256": x["sha256"], "takes": x.get("takes") or [], "fps": x.get("fps") or [],
                 "hook": x.get("hook"),
                 "hook_id": x.get("hook_id"), "text": x.get("caption") or ""}
        key = f"{post_id}|{x['socialAccountId']}"
        ledger["posts"][key] = entry_for(r, camp, post_id, x["socialAccountId"], now, m["job"].get("timezone"),
                                         idx.get("plan_id"))
        ledger["posts"][key]["request"] = name
        if warnings:
            ledger["posts"][key]["open_errors"] = warnings[:10]
    ledger.get("pending", {}).pop(f"{camp.get('id')}:{name}", None)
    remember_campaign(ledger, camp)
    save_ledger(m["ledger_path"], ledger)
    evidence_dirs(m["job_dir"], [x["post"] for x in meta["posts"]])
    for w in warnings:
        print(f"warning (recorded anyway, it went out): {w}")
    print(f"recorded: {name} was sent as post {post_id} ({', '.join(x['account'] for x in meta['posts'])}) in the "
          f"ledger ({rel(m['ledger_path'])}). The {int(camp['submit_within_minutes'])} minutes run from the moment each "
          "post is live.")
    print(f"next: posts_get {post_id} in a minute, save the reply as status.json, and run: plan.py {rel(job_path)} "
          f"--status status.json {post_id}")
    write_sheet(m, ledger)


def unwrap(data):
    for _ in range(4):
        data = unwrap_reply(data)
        if isinstance(data, dict) and not data.get("socialAccountPosts"):
            inner = next((data[k] for k in ("data", "result", "structuredContent", "post")
                          if isinstance(data.get(k), (dict, list))), None)
            if inner is None:
                break
            data = inner
        else:
            break
    return data


def apply_status(job_path, status_path, post_id=None, ledger_file=None):
    m = check_job(job_path, ledger_file)
    camp = m["campaign"]
    data = unwrap(read_json(status_path, "the saved posts_get reply"))
    items = post_items(data)
    if not items:
        die(f"{status_path} holds no per-account posts. Save the whole reply of posts_get as it came back")
    top = (data.get("postId") or data.get("id")) if isinstance(data, dict) else None
    pid = (post_id or "").strip() or (top if isinstance(top, str) else None)
    if not pid:
        die(f"{status_path} doesn't say which post it is about: --status {status_path} <postId>")
    if post_id and isinstance(top, str) and top != post_id:
        die(f"{status_path} is the reply for post {top}, not {post_id}")
    ledger = m["ledger"]
    mine = {k: e for k, e in ledger["posts"].items() if e.get("campaign") == camp.get("id") and e.get("postId") == pid}
    if not mine:
        die(f"the ledger has no post {pid} for campaign {camp.get('id')}. Record it first with --posted")
    by_url = {post_key(e["url"]): k for k, e in ledger["posts"].items() if e.get("url")}
    updated, failed, seen = 0, [], set()
    for it in items:
        if isinstance(it.get("postId"), str) and it["postId"] != pid:
            continue
        sid = it.get("socialAccountId")
        hits = [k for k, e in mine.items() if e.get("socialAccountId") == sid]
        if not hits:
            continue
        if len(hits) > 1 or sid in seen:
            die(f"{status_path} holds more than one post for account {sid}. Save the posts_get reply of post {pid} alone")
        seen.add(sid)
        e = ledger["posts"][hits[0]]
        url = it["externalPostUrl"].strip() if isinstance(it.get("externalPostUrl"), str) and \
            it["externalPostUrl"].strip() else None
        if url:
            other = by_url.get(post_key(url))
            if e.get("url") and post_key(e["url"]) != post_key(url):
                die(f"{e.get('job_post')} already has the link {e['url']}, and this reply says {url}. Nothing was changed")
            if other and other != hits[0]:
                die(f"{url} is already in the ledger for another post. Nothing was changed")
            e["url"] = url
        st = it.get("deliveryStatus")
        if isinstance(st, str) and any(w in st.upper() for w in ("FAIL", "ERROR", "REJECT")):
            failed.append(f"{e.get('account')}: {st}")
        t = parse_time(it.get("deliveryCompletedAt"))
        if t:
            e["published_at"] = iso(t)
        if st:
            e["status"] = st
        updated += 1
    if not updated:
        die(f"{status_path} has no account of post {pid}")
    save_ledger(m["ledger_path"], ledger)
    print(f"{updated} post(s) updated from {rel(status_path)}")
    for f in failed:
        print(f"  not published: {f}. Say why in plain words; nothing is resent without a new yes")
    write_sheet(m, ledger)


def record_by_hand(job_path, post, url, at=None, ledger_file=None):
    m = model(job_path, ledger_file)
    camp = m["campaign"]
    r = next((r for r in m["rows"] if r["id"] == post), None)
    if r is None:
        die(f"there is no post \"{post}\" in the job ({', '.join(r['id'] for r in m['rows'])})")
    if not r.get("sha256"):
        die(f"post {post} has no video file, so it can't be recorded")
    if not url.lower().startswith(("http://", "https://")):
        die("give the post's link as the app's share menu shows it (https://...)")
    if short_link(url):
        die("that is a short share link, which hides the post's id. Open it in a browser and copy the full link")
    lp = post_key(url).split(":")[0]
    if lp in LIMITS and lp != r["platform"]:
        die(f"that is a {LIMITS[lp]['label']} link, and {post} is the {LIMITS[r['platform']]['label']} post")
    if lp != r["platform"]:
        die(f"that isn't a link to one {LIMITS[r['platform']]['label']} post (a profile or other page?). Open the post "
            "and copy its link from the share menu")
    ledger = m["ledger"]
    if any(post_key(e.get("url")) == post_key(url) for e in ledger["posts"].values() if e.get("url")):
        die(f"{url} is already in the ledger")
    if r["posted"]:
        die(f"{post} on {r['name']} is already recorded")
    now = now_utc()
    assumed = None
    if at:
        t, assumed, problem = parse_user_time(at, m["job"].get("timezone"))
        if problem:
            die(f"--at: {problem}")
        if t > now + datetime.timedelta(minutes=2):
            die(f"--at {at} is in the future. Give the time it went live")
    else:
        t = now
    e = entry_for(r, camp, "by hand", r["account"].get("socialAccountId"), now, m["job"].get("timezone"))
    e.update(byHand=True, url=url, published_at=iso(t))
    open_errs = [f"{w}: {msg}" for lv, w, msg in m["checks"] if lv == "error" and w == f"post {post}"]
    y = load_yes(m["job_dir"])
    if not (y and post in (y.get("by_hand") or []) and y.get("plan_id") == m["plan_id"]):
        open_errs.append("no yes on record for this by-hand post as it is now")
    if open_errs:
        e["open_errors"] = open_errs[:10]
    ledger["posts"][f"hand:{post}|{r['name']}"] = e
    remember_campaign(ledger, camp)
    save_ledger(m["ledger_path"], ledger)
    evidence_dirs(m["job_dir"], [post])
    print(f"recorded: {post} posted by hand on {r['name']}")
    for w in open_errs:
        print(f"warning (recorded anyway, it is live): {w}. Fix it on the post if you can; it shows on submit.md")
    if assumed:
        print(f"note: --at {at} has no time zone, so it was read as {assumed} time")
    write_sheet(m, ledger)


def release(job_path, post, ledger_file=None, checked=False):
    """--failed: take one post that never went live out of the ledger, so the next plan sends it again."""
    m = check_job(job_path, ledger_file)
    camp = m["campaign"]
    ledger = m["ledger"]
    hits = [k for k, e in ledger["posts"].items() if e.get("job_post") == post and e.get("campaign") == camp.get("id")]
    if not hits:
        die(f"the ledger has no post \"{post}\" for this campaign (--failed takes the job's post id)")
    for k in hits:
        e = ledger["posts"][k]
        if e.get("url") or e.get("byHand") or any(post_key(s.get("url")) == post_key(e.get("url"))
                                                  for s in ledger["submissions"] if e.get("url")):
            die(f"{post} on {e.get('account')} has a link, so it went live. It is never released: posting it again is "
                "a duplicate")
        st = str(e.get("status") or "").upper()
        if not any(w in st for w in ("FAIL", "ERROR", "REJECT")):
            die(f"{post} isn't marked as failed (status: {e.get('status') or 'not read yet'}). Call posts_get again, save "
                "the reply, run --status; release it only when its status says it failed")
    if not checked:
        e = ledger["posts"][hits[0]]
        die(f"before releasing: a post marked failed can still be on the platform. Call social_account_posts_list for "
            f"{e.get('account')} and look at the last hour. Only when the video isn't there, run this again with --checked")
    for k in hits:
        del ledger["posts"][k]
    save_ledger(m["ledger_path"], ledger)
    print(f"released: {post} is out of the ledger. Plan again and wait for a new yes before posting it")


def left_text(due, now, live):
    if live > now:
        return "not live yet"
    secs = (due - now).total_seconds()
    if secs <= 0:
        return "the window has passed"
    if secs < 60:
        return "under a minute left"
    return f"{math.ceil(secs / 60)} min left"


def write_sheet(m, ledger):
    """submit.md: per post of this campaign not yet submitted, its link, the clock time the window closes,
    what to do in the apps before then, and when to take the proof screenshots."""
    camp, job_dir = m["campaign"], m["job_dir"]
    zone = m["job"].get("timezone")
    win = int(camp["submit_within_minutes"])
    now = now_utc()
    done = {post_key(s.get("url")) for s in ledger["submissions"]}
    rows = {r["id"]: r for r in m["rows"]}
    hours = shot_hours(camp)
    lines = [f"# Submit: {camp.get('name')}", "",
             f"Campaign `{camp.get('id')}`. One post goes into one campaign, once. Submit each link within {win} minutes "
             "of it going live; a late post can't be fixed. Times are in " + (zone if load_zone(zone) else "UTC") + ".", ""]
    if example_demo(camp):
        lines += [f"**{DEMO_NOTE}**", ""]
    n = 0
    mine = [e for e in ledger["posts"].values() if e.get("campaign") == camp.get("id")]
    for e in mine:
        if e.get("url") and post_key(e["url"]) in done:
            continue
        n += 1
        who = f"{e.get('account')}{' ' + e['handle'] if e.get('handle') else ''}"
        lines.append(f"{n}. **{who}** ({LIMITS.get(e.get('platform'), {}).get('label', e.get('platform'))}), post `{e.get('job_post')}`")
        lines.append(f"   - Link: {e['url']}" if e.get("url") else "   - Link: not there yet. Your agent checks again in a minute.")
        live, sent = parse_time(e.get("published_at")), parse_time(e.get("recorded"))
        mins = int(e.get("submit_within") or win)
        if live:
            due = live + datetime.timedelta(minutes=mins)
            lines.append(f"   - Live since {clock(live, zone)}. Submit by **{clock(due, zone)}** ({left_text(due, now, live)}).")
        elif sent:
            due = sent + datetime.timedelta(minutes=mins)
            lines.append(f"   - Sent {clock(sent, zone)}, not confirmed live yet. To be safe, submit by **{clock(due, zone)}**.")
        r = rows.get(e.get("job_post"))
        k = 0
        for s in (window_steps(r, camp) if r else []):
            k += 1
            lines.append(f"   - Step {k}, first: {s}")
        if any("submission" in str(x).lower() or "at submission" in str(x).lower() for x in camp.get("proof") or []):
            k += 1
            lines.append(f"   - Step {k}: the proof the brief wants at submission: "
                         + "; ".join(x for x in camp["proof"] if "submission" in str(x).lower()) + ".")
        lines.append(f"   - Step {k + 1}: submit the link in the campaign, then tell your agent (with the submission id "
                     "if the campaign shows one).")
        if e.get("open_errors"):
            lines.append("   - Open problems recorded with this post (fix them on the post if you can before submitting): "
                         + "; ".join(e["open_errors"][:5]))
    if not n:
        lines.append("Nothing waiting: every recorded post of this campaign is submitted.")
    if mine:
        lines += ["", "## Proof to keep", "",
                  "Screenshot each post's analytics (views and audience countries) at these times and save them in its "
                  "folder. Campaigns ask for them when a payout or a rejection is checked." + (
                      f" The brief asks for: {'; '.join(camp['proof'])}." if camp.get("proof") else ""), ""]
        for e in mine:
            live = parse_time(e.get("published_at")) or parse_time(e.get("recorded"))
            if not live:
                continue
            when = "; ".join(f"{hours_label(h)} {clock(live + datetime.timedelta(hours=h), zone)}" for h in hours)
            names = ", ".join(f"{hours_label(h)}-analytics.png" for h in hours)
            lines.append(f"- `{e.get('job_post')}` ({e.get('account')}): {when}. Folder `proof/{e.get('job_post')}/`: "
                         f"{names}, submission.png.")
    lines += ["", "The skill never submits for you and never opens your logged-in browser: you paste each link into the "
              "campaign yourself.", ""]
    text = "\n".join(lines)
    write_text(os.path.join(job_dir, "submit.md"), text)
    write_ics(m, mine, hours, zone)
    print()
    print(text.rstrip())


def write_ics(m, posts, hours, zone):
    """deadlines.ics: the campaign deadline and each post's submit-by time and proof screenshot times,
    so they land in the creator's calendar."""
    camp = m["campaign"]
    ev = []

    def stamp_of(t):
        return t.astimezone(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    if camp.get("deadline"):
        end = deadline_end(camp["deadline"], camp.get("deadline_tz"))
        if end:
            ev.append((end, f"Deadline: {camp.get('name')}"))
    for e in posts:
        live = parse_time(e.get("published_at")) or parse_time(e.get("recorded"))
        if not live:
            continue
        ev.append((live + datetime.timedelta(minutes=int(e.get("submit_within") or camp["submit_within_minutes"])),
                   f"Submit by: {e.get('job_post')} ({e.get('account')})"))
        for h in hours:
            ev.append((live + datetime.timedelta(hours=h), f"Proof {hours_label(h)}: {e.get('job_post')} ({e.get('account')})"))
    if not ev:
        return
    def esc(text):
        return re.sub(r"([\\;,])", r"\\\1", str(text)).replace("\n", "\\n")

    def fold(line):
        """RFC 5545: lines longer than 75 octets go on in a line that starts with a space."""
        out_, cur = [], b""
        for ch in line:
            b = ch.encode("utf-8")
            if len(cur) + len(b) > (75 if not out_ else 74):
                out_.append(cur.decode("utf-8"))
                cur = b""
            cur += b
        out_.append(cur.decode("utf-8"))
        return "\n ".join(out_)
    out = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//ugc-creator-skill//EN"]
    for i, (t, title) in enumerate(sorted(ev, key=lambda x: x[0])):
        uid = hashlib.sha256(f"{camp.get('id')}|{title}|{stamp_of(t)}".encode()).hexdigest()[:16]
        out += ["BEGIN:VEVENT", f"UID:{uid}@ugc-creator-skill", f"DTSTAMP:{stamp_of(now_utc())}", f"DTSTART:{stamp_of(t)}",
                f"DTEND:{stamp_of(t + datetime.timedelta(minutes=10))}", fold("SUMMARY:" + esc(title)),
                "BEGIN:VALARM", "TRIGGER:-PT10M", "ACTION:DISPLAY", fold("DESCRIPTION:" + esc(title)),
                "END:VALARM", "END:VEVENT"]
    out.append("END:VCALENDAR")
    with open(os.path.join(m["job_dir"], "deadlines.ics"), "w", encoding="utf-8", newline="\r\n") as fh:
        fh.write("\n".join(out) + "\n")


def remember_accounts(job_path):
    """Save the job's accounts to <user_home>/accounts.json as suggestions for next time: never the
    WoopSocial id, TikTok's privacy choice or the marketplace verification."""
    job = read_json(job_path, "the campaign job")
    accs = job.get("accounts") if isinstance(job, dict) else None
    if not isinstance(accs, list) or not accs:
        die(f"{rel(job_path)} has no accounts to save")
    keep = ("name", "platform", "handle", "allowComment", "allowDuet", "allowStitch", "privacy", "madeForKids", "audience")
    saved = {account_key(a): a for a in load_saved_accounts() if account_key(a)}
    for a in accs:
        k = account_key(a) if isinstance(a, dict) else None
        if not k:
            die("every account to save needs its platform and handle: saved accounts are matched on both")
        cur = dict(saved.get(k, {}))
        cur.update({x: a[x] for x in keep if x in a})
        cur["platform"] = str(a["platform"]).strip().upper()
        saved[k] = cur
    path = os.path.join(user_home(), "accounts.json")
    write_json(path, {"accounts": list(saved.values())})
    print(f"saved {len(accs)} account(s) to {path}. Next time check_videos.py shows them as suggestions to confirm")


def main():
    ap = argparse.ArgumentParser(description="Plan a campaign batch, bind the yes, then record what went out.")
    ap.add_argument("job")
    ap.add_argument("--yes", metavar="PLAN_ID", help="the user said yes to this plan id on the plan page")
    ap.add_argument("--media", help="media.json: {file: {mediaId, sha256}} after uploading")
    ap.add_argument("--check", metavar="REQUEST", help="right before posts_create: is this request still what the user "
                                                       "said yes to?")
    ap.add_argument("--posted", nargs=2, metavar=("REQUEST", "POST_ID"), help="record a request that was sent")
    ap.add_argument("--status", nargs="+", metavar="ARG", help="the saved posts_get reply [and the post id]")
    ap.add_argument("--posted-by-hand", nargs=2, metavar=("POST", "URL"), help="record a post made in the app")
    ap.add_argument("--at", help="with --posted-by-hand: when it went live (2026-11-16T09:05 in the job's timezone, "
                                 "or with a zone)")
    ap.add_argument("--failed", metavar="POST_ID", help="a post that failed to publish: release it from the ledger")
    ap.add_argument("--checked", action="store_true", help="with --failed: social_account_posts_list shows it isn't there")
    ap.add_argument("--not-sent", metavar="REQUEST", help="a request checked with --check that never went out")
    ap.add_argument("--remember-accounts", action="store_true", help="save the accounts as suggestions for next time")
    ap.add_argument("--ledger", help="the ledger file (default: UGC_CREATOR_LEDGER, else ~/.ugc-creator/ledger.json)")
    a = ap.parse_args()
    if a.status and len(a.status) > 2:
        die("--status takes the saved reply and, if it doesn't carry one, the post id")
    if a.yes:
        record_yes(a.job, a.yes, a.ledger)
    elif a.check:
        check_request(a.job, a.check, a.ledger)
    elif a.posted:
        record_posted(a.job, *a.posted, ledger_file=a.ledger)
        if a.status:
            apply_status(a.job, a.status[0], a.status[1] if len(a.status) > 1 else a.posted[1], a.ledger)
    elif a.status:
        apply_status(a.job, a.status[0], a.status[1] if len(a.status) > 1 else None, a.ledger)
    elif a.posted_by_hand:
        record_by_hand(a.job, *a.posted_by_hand, at=a.at, ledger_file=a.ledger)
    elif a.failed:
        release(a.job, a.failed, a.ledger, a.checked)
    elif a.not_sent:
        not_sent(a.job, a.not_sent, a.checked, a.ledger)
    elif a.remember_accounts:
        remember_accounts(a.job)
    else:
        plan(a.job, a.media, a.ledger)


if __name__ == "__main__":
    guard(main)
