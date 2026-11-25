#!/usr/bin/env python3
"""The creator's ledger: which video went into which campaign, what happened to it, what it earned,
and how many hours each campaign took.

    python3 scripts/ledger.py --submitted <post url> --campaign <id> [--submission-id ID] [--at TIME]
    python3 scripts/ledger.py --status <post url> approved|rejected|pending|paid [--reason "..."]
    python3 scripts/ledger.py --appeal <post url> --note "what you sent, where"
    python3 scripts/ledger.py --proof analytics.json       # the saved social_account_posts_list_analytics reply
    python3 scripts/ledger.py --views <post url> 12400 --source "TikTok analytics screenshot, 72h"
    python3 scripts/ledger.py --paid <post url> 19.80 [--at DATE]          # adds a payment; run it per payout
    python3 scripts/ledger.py --hours <campaign id> 2.5 --note "filming and editing"
    python3 scripts/ledger.py --report [--min-hourly 15]   # per campaign: views, payout, status,
                                                           #   earnings per hour, drop hints
    python3 scripts/ledger.py --paid-campaign <campaign id> 54.10   # a lump payout, split over its videos; as often as
                                                                    #   the campaign pays
    python3 scripts/ledger.py --appeal-draft <post url>   # a short appeal from what the ledger holds; you send it
    python3 scripts/ledger.py --report --week             # what this week earned, across campaigns
    python3 scripts/ledger.py --list

One ledger for every campaign, whatever folder each lives in: ~/.ugc-creator/ledger.json
(UGC_CREATOR_HOME moves the folder, UGC_CREATOR_LEDGER or --ledger names another file). plan.py adds
every post that goes out; this script adds what happens after. The view log, proof.csv, sits next to
the ledger: one row per post and reading, each with where the number came from.

Numbers come only from what was saved: WoopSocial's analytics reply (--proof) or a number the user
read in the app or the campaign dashboard and typed in with its source (--views, --paid, --hours).
Nothing is estimated from nothing, and the campaign's own count always decides what is paid.

Posts are matched by platform and post id, so a share link with ?igsh=, ?si=, ... is the same post as
the plain link. --submitted refuses a link already submitted (one post goes into one campaign,
once), a post made for another campaign and a TikTok short link. It never submits anything itself.
"""
import argparse, csv, datetime, os, re, sys

sys.dont_write_bytecode = True   # nothing is ever written into the skill's own folder
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ugclib import (LIMITS, SUBMIT_MINUTES, clock, die, guard, is_num, iso, ledger_path, load_ledger, money,  # noqa: E402
                    now_utc, parse_time, parse_user_time, payout, place_name, post_items, post_key, proof_path,
                    read_json, rel, save_ledger, short_link, terms, threshold_views, unwrap_reply, valid_id,
                    with_defaults)

PROOF_COLUMNS = ["collected_at", "metrics_collected_at", "campaign", "post", "account", "platform", "url",
                 "views", "likes", "comments", "shares", "engagement", "published_at", "submission_id", "geo_share",
                 "source"]
VIEW_KEYS = ("views", "videoViews", "video_views", "plays", "impressions")
STATUSES = ("pending", "approved", "rejected", "paid")


def find_post(ledger, url):
    n = post_key(url)
    for k, e in ledger["posts"].items():
        if e.get("url") and post_key(e["url"]) == n:
            return k, e
    return None, None


def find_submission(ledger, url):
    n = post_key(url)
    return next((s for s in ledger["submissions"] if post_key(s.get("url")) == n), None)


def need_submission(ledger, url, what):
    s = find_submission(ledger, url)
    if not s:
        die(f"{url} isn't a submitted post in the ledger. Record it first: ledger.py --submitted {url} --campaign <id>"
            + (f" (then {what})" if what else ""))
    return s


def at_time(at):
    if not at:
        return now_utc()
    t, _, problem = parse_user_time(at)
    if problem:
        die(f"--at: {problem}")
    return t


def check_url(url):
    if not url.lower().startswith(("http://", "https://")):
        die("give the post's link as the app shows it (https://...)")
    if short_link(url):
        die("that is a short share link (vm.tiktok.com or tiktok.com/t/), which hides the post's id. Open it in a "
            "browser and give the full link")


def submitted(lpath, url, campaign, at=None, submission_id=None, known=()):
    check_url(url)
    if not valid_id(campaign):
        die("--campaign is the campaign id from campaign.json (lowercase letters, digits and dashes)")
    ledger = load_ledger(lpath)
    s = find_submission(ledger, url)
    if s:
        if s.get("campaign") == campaign:
            die(f"this post was already submitted to {campaign} on {s.get('submitted_at')}. A post is submitted once")
        die(f"this post was already submitted to campaign {s.get('campaign')}. One post goes into one campaign, once, "
            "ever. For this campaign, make a new video")
    key, post = find_post(ledger, url)
    if not post:
        waiting = unread_posts(ledger, url)
        if waiting:
            die(f"the skill posted {', '.join(waiting)} and hasn't read its link yet, so it can't tell whether this link "
                "is that post. Run plan.py --status with a fresh posts_get reply first")
    if post and post.get("campaign") and post["campaign"] != campaign:
        die(f"this post was made for campaign {post['campaign']}, not {campaign}: its script, disclosure and caption "
            "follow that brief. Submit it there, or make a new video for this campaign")
    ids = set(ledger.get("campaigns") or {}) | {e.get("campaign") for e in ledger["posts"].values()} | set(known)
    if campaign not in ids:
        die(f"no campaign {campaign} in the ledger or in a campaign file. Check the id (campaign.json \"id\"), or pass "
            "--campaign-file <its campaign.json>" + (f". Known: {', '.join(sorted(i for i in ids if i))}" if ids else ""))
    zone = (post or {}).get("timezone")
    assumed = None
    if at:
        t, assumed, problem = parse_user_time(at, zone)
        if problem:
            die(f"--at: {problem}")
    else:
        t = now_utc()
    late = None
    if post:
        live = parse_time(post.get("published_at"))
        if live and t < live - datetime.timedelta(minutes=1):
            die(f"--at {at} is before the post went live ({clock(live, zone)}). Give the time you submitted it")
        live = live or parse_time(post.get("recorded"))
        if live:
            mins = (t - live).total_seconds() / 60
            limit = post.get("submit_within") or (ledger.get("campaigns", {}).get(campaign) or {}).get(
                "submit_within_minutes") or SUBMIT_MINUTES
            if mins > limit:
                late = (int(mins), int(limit))
    entry = {"url": url, "campaign": campaign, "submitted_at": iso(t), "post": post.get("job_post") if post else None,
             "account": post.get("account") if post else None, "platform": post.get("platform") if post else
             (post_key(url).split(":")[0] if post_key(url).split(":")[0] in LIMITS else None),
             "status": "pending", "history": [{"at": iso(t), "status": "pending", "note": "submitted"}]}
    if submission_id:
        entry["submission_id"] = str(submission_id).strip()
    if late:
        entry["late_minutes"] = late[0]
    ledger["submissions"].append(entry)
    save_ledger(lpath, ledger)
    print(f"recorded: {url}{' (' + post['account'] + ')' if post else ''} submitted to {campaign} at {clock(t, zone)}")
    if assumed:
        print(f"note: --at {at} has no time zone, so it was read as {assumed} time")
    if not post:
        print("note: this link isn't a post the skill recorded. It is recorded anyway, so it can't be submitted twice")
    if late:
        print(f"warning: submitted {late[0]} minutes after it went live; this campaign takes posts submitted within "
              f"{late[1]} minutes, so it may be rejected")
    print("next: keep it public and unchanged, take the proof screenshots submit.md lists, and record what the campaign "
          "decides with --status")


def unread_posts(ledger, url):
    plat = post_key(url).split(":")[0]
    if plat not in LIMITS:
        return []
    m = re.search(r"tiktok\.com/@([A-Za-z0-9_.]+)", url)
    handle = m.group(1).casefold() if m else None
    now = now_utc()
    out = []
    for e in ledger["posts"].values():
        if e.get("url") or e.get("platform") != plat:
            continue
        if any(w in str(e.get("status") or "").upper() for w in ("FAIL", "ERROR", "REJECT")):
            continue
        t = parse_time(e.get("recorded"))
        if not t or (now - t).total_seconds() > 2 * 86400:
            continue
        if handle and e.get("handle") and str(e["handle"]).lstrip("@").casefold() != handle:
            continue
        out.append(f"{e.get('job_post')} on {e.get('account')} for {e.get('campaign')}")
    return out


def set_status(lpath, url, status, reason=None, at=None):
    status = status.lower()
    if status not in STATUSES:
        die(f"--status takes one of {', '.join(STATUSES)}")
    ledger = load_ledger(lpath)
    s = need_submission(ledger, url, f"--status {status}")
    if status == "rejected" and not (reason and reason.strip()):
        die("say why it was rejected, in the campaign's words: --reason \"...\". The reasons are what the report learns from")
    if s.get("status") == "paid" and status != "paid":
        die("this post is already recorded as paid")
    t = at_time(at)
    s["status"] = status
    if reason:
        s["reason"] = reason.strip()
    s.setdefault("history", []).append({"at": iso(t), "status": status, "note": (reason or "").strip()})
    save_ledger(lpath, ledger)
    print(f"recorded: {url} is {status}" + (f" ({reason.strip()})" if reason else ""))
    if status == "rejected":
        print("next: if the reason doesn't hold (the video follows the brief), appeal where the campaign takes appeals "
              "and record it with --appeal. Keep the proof screenshots")


def appeal(lpath, url, note):
    if not (note and note.strip()):
        die("--appeal needs --note: what you sent, where, and when")
    ledger = load_ledger(lpath)
    s = need_submission(ledger, url, "--appeal")
    if s.get("status") != "rejected":
        die(f"this post is {s.get('status') or 'pending'}, not rejected: there is nothing to appeal")
    s.setdefault("appeals", []).append({"at": iso(now_utc()), "note": note.strip()})
    s.setdefault("history", []).append({"at": iso(now_utc()), "status": "rejected", "note": "appealed: " + note.strip()})
    save_ledger(lpath, ledger)
    print(f"recorded: appeal for {url}. When the campaign answers, record it with --status approved or --status rejected")


def add_payment(s, amt, t, note):
    """A payment adds to what a post has earned: marketplaces pay as views come in, so one post can be
    paid several times. "paid" is the sum of "payments"."""
    pays = s.get("payments")
    if not isinstance(pays, list):
        pays = [{"at": s.get("paid_at"), "amount": round(float(s["paid"]), 2)}] if is_num(s.get("paid"), 0) and \
            s.get("paid") else []
    pays.append({"at": iso(t), "amount": round(amt, 2), "note": note})
    s["payments"] = pays
    s["paid"] = round(sum(float(x.get("amount") or 0) for x in pays), 2)
    s["paid_at"] = iso(t)
    s["status"] = "paid"
    s.setdefault("history", []).append({"at": iso(t), "status": "paid", "note": note})


def paid(lpath, url, amount, at=None):
    try:
        amt = float(str(amount).replace(",", "").lstrip("$"))
    except ValueError:
        amt = -1
    if amt < 0:
        die("--paid takes the amount that reached you, as a number (19.80)")
    ledger = load_ledger(lpath)
    s = need_submission(ledger, url, "--paid")
    t = at_time(at)
    if s.get("status") == "rejected" and not s.get("appeals"):
        print("warning: this post is recorded as rejected and never appealed. Recorded as paid anyway; if the campaign "
              "reversed its decision, note it with --appeal next time")
    add_payment(s, amt, t, f"{amt:.2f} received")
    save_ledger(lpath, ledger)
    n = len(s["payments"])
    print(f"recorded: {url} paid {amt:.2f}" + (f" (payment {n}; {s['paid']:.2f} in all)" if n > 1 else ""))


def paid_campaign(lpath, campaign, amount, at=None):
    """A lump payout for a campaign, split over its submitted videos that aren't rejected, in proportion
    to their last saved views (evenly when none are saved). Campaigns pay as views come in, so this can
    run again for the next payout; each one adds to what the videos have earned."""
    try:
        amt = float(str(amount).replace(",", "").lstrip("$"))
    except ValueError:
        amt = -1
    if amt <= 0:
        die("--paid-campaign takes the campaign id and the amount that reached you (54.10)")
    ledger = load_ledger(lpath)
    open_subs = [x for x in ledger["submissions"] if x.get("campaign") == campaign and x.get("status") != "rejected"]
    if not open_subs:
        die(f"no submissions for {campaign} that can be paid (all rejected, or none recorded)")
    rows = read_proof(proof_path(lpath))
    views = []
    for x in open_subs:
        snaps = [num(r["views"]) for r in rows if post_key(r["url"]) == post_key(x["url"])]
        views.append(max(snaps) if snaps else 0)
    total = sum(views)
    t = at_time(at)
    shares = [round(amt * (v / total if total else 1 / len(open_subs)), 2) for v in views]
    shares[-1] = round(amt - sum(shares[:-1]), 2)
    for x, part in zip(open_subs, shares):
        add_payment(x, part, t, f"{part:.2f} of a {amt:.2f} lump payout" + (" (split by views)" if total
                                                                           else " (split evenly)"))
    save_ledger(lpath, ledger)
    print(f"recorded: {amt:.2f} for {campaign}, split over {len(open_subs)} video(s): "
          + ", ".join(f"{x['url']} {p:.2f}" for x, p in zip(open_subs, shares)))


def appeal_draft(lpath, url, folder, campaign_files):
    """A short appeal from what the ledger holds: the reason given, the campaign's on-page rules the
    video meets, and the proof to attach. Written to a file; the creator reads it and sends it."""
    ledger = load_ledger(lpath)
    s = need_submission(ledger, url, "--appeal-draft")
    if s.get("status") != "rejected":
        die(f"this post is {s.get('status') or 'pending'}, not rejected: there is nothing to appeal")
    _, post = find_post(ledger, url)
    camps = load_campaigns(folder, campaign_files, ledger)
    c = camps.get(s.get("campaign")) or {}
    post = post or {}
    lines = [f"Appeal: {url}", "", f"Campaign: {c.get('name') or s.get('campaign')}. Submitted "
             f"{s.get('submitted_at')}" + (f" (submission {s['submission_id']})" if s.get("submission_id") else "") + ".",
             "", f"The reason given: \"{s.get('reason') or 'none recorded'}\"", "", "Where the video meets the "
             "campaign's rules (only rules on the campaign page are grounds for a rejection):", ""]
    if post.get("spoken_disclosure_s") is not None:
        lines.append(f"- The disclosure is said out loud by {post['spoken_disclosure_s']:.1f} s.")
    if post.get("caption"):
        lines.append(f"- The caption starts with the disclosure: \"{post['caption'][:120]}\"")
    if post.get("published_at") and s.get("submitted_at"):
        a, b = parse_time(post["published_at"]), parse_time(s["submitted_at"])
        if a and b:
            lines.append(f"- Submitted {int((b - a).total_seconds() // 60)} minutes after it went live.")
    lines.append(f"- Posted from {post.get('account') or 'my account'}"
                 + (f" ({post['handle']})" if post.get("handle") else "") + ", public and unchanged since.")
    proof_dir = os.path.join(folder, "proof", post.get("job_post") or "")
    files = sorted(os.listdir(proof_dir)) if post.get("job_post") and os.path.isdir(proof_dir) else []
    lines += ["", "Attached: " + (", ".join(files) if files else "(add the analytics screenshots from proof/)"), "",
              "Could you look at it again? Thank you.", ""]
    out = os.path.join(folder, f"appeal-{re.sub(r'[^A-Za-z0-9_-]', '-', post_key(url))[:60]}.md")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print("\n".join(lines))
    print(f"-> {out}. Check every line against the campaign page, then send it yourself; record it with --appeal")


def hours(lpath, campaign, h, note=None):
    if not valid_id(campaign):
        die("--hours takes the campaign id from campaign.json")
    try:
        x = float(h)
    except ValueError:
        x = -1
    if not 0 < x <= 24:
        die("--hours takes the hours spent in one go, more than 0 and at most 24 (2.5 for two and a half)")
    ledger = load_ledger(lpath)
    ledger["hours"].append({"campaign": campaign, "hours": round(x, 2), "at": iso(now_utc()), "note": (note or "").strip()})
    save_ledger(lpath, ledger)
    total = sum(e["hours"] for e in ledger["hours"] if e.get("campaign") == campaign)
    print(f"recorded: {x:g} h on {campaign} ({total:g} h in all)")


def num(v):
    if isinstance(v, bool):
        return 0
    if isinstance(v, (int, float)):
        return int(v)
    if isinstance(v, str):
        try:
            return int(float(v.replace(",", "")))
        except ValueError:
            return 0
    return 0


def metrics_of(item):
    m = item.get("metrics") if isinstance(item.get("metrics"), dict) else (
        item.get("analytics") if isinstance(item.get("analytics"), dict) else item)
    views = next((num(m[k]) for k in VIEW_KEYS if k in m), None)
    return views, num(m.get("likes")), num(m.get("comments")), num(m.get("shares"))


def read_proof(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8-sig", newline="") as fh:   # utf-8-sig: Excel saves with a BOM
        reader = csv.DictReader(fh)
        rows = list(reader)
        cols = reader.fieldnames or []
    if set(PROOF_COLUMNS) - set(cols) - {"source", "geo_share"}:
        die(f"{rel(path)} doesn't have the columns this skill writes. Move it away and run again")
    for r in rows:
        for k in PROOF_COLUMNS:
            if r.get(k) is None:
                r[k] = ""
    return rows


def write_proof(path, rows):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=PROOF_COLUMNS, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    try:
        os.replace(tmp, path)
    except PermissionError:
        os.remove(tmp)
        die(f"{path} can't be replaced: another program has it open. Close proof.csv in Excel (or wherever it is "
            "open) and run this again")


def proof(lpath, path):
    data = unwrap_reply(read_json(path, "the saved analytics reply"))
    items = post_items(data)
    if not items:
        die(f"{path} holds no posts. Save the whole reply of social_account_posts_list_analytics as it came back")
    ledger = load_ledger(lpath)
    ppath = proof_path(lpath)
    rows = read_proof(ppath)
    seen = {(post_key(r["url"]), r["metrics_collected_at"] or r["collected_at"][:10]) for r in rows}
    now = now_utc()
    new, skipped, no_views = [], 0, 0
    for it in items:
        url = it.get("externalPostUrl")
        if not isinstance(url, str) or not url.strip():
            skipped += 1
            continue
        _, post = find_post(ledger, url)
        sub = find_submission(ledger, url)
        if not post and not sub:
            skipped += 1
            continue
        views, likes, comments, shares = metrics_of(it)
        if views is None:
            no_views += 1
            continue
        mc = it.get("metricsCollectedAt") if isinstance(it.get("metricsCollectedAt"), str) else ""
        key = (post_key(url), mc or iso(now)[:10])
        if key in seen:
            continue
        seen.add(key)
        eng = (likes + comments + shares) / views if views else 0.0
        new.append({"collected_at": iso(now), "metrics_collected_at": mc,
                    "campaign": (post or {}).get("campaign") or (sub or {}).get("campaign") or "",
                    "post": (post or {}).get("job_post") or "", "account": (post or {}).get("account") or "",
                    "platform": (post or {}).get("platform") or it.get("platform") or "", "url": url,
                    "views": views, "likes": likes, "comments": comments, "shares": shares,
                    "engagement": f"{eng:.4f}", "published_at": (post or {}).get("published_at") or "",
                    "submission_id": (sub or {}).get("submission_id") or "", "geo_share": "",
                    "source": "WoopSocial analytics"})
    write_proof(ppath, rows + new)
    print(f"{len(new)} reading(s) added to {rel(ppath)}; {skipped} post(s) skipped (not in the ledger)"
          + (f"; {no_views} without a view count yet" if no_views else ""))
    print("note: WoopSocial collects these about once a day. The campaign's own count decides what is paid; keep the "
          "screenshots submit.md lists")


def views_entry(lpath, url, n, source, geo=None):
    check_url(url)
    if not (source and source.strip()):
        die("say where the number comes from: --source \"TikTok analytics, 72h screenshot\" or \"campaign dashboard\". "
            "Numbers are never typed in without one")
    v = num(n)
    if v < 0 or not re.fullmatch(r"[\d,]+", str(n).strip()):
        die("--views takes the view count as a whole number (12400)")
    ledger = load_ledger(lpath)
    _, post = find_post(ledger, url)
    sub = find_submission(ledger, url)
    if not post and not sub:
        die(f"{url} isn't in the ledger. Record the post (plan.py) or the submission (--submitted) first")
    g = ""
    if geo is not None:
        try:
            x = float(str(geo).rstrip("%"))
            x = x / 100 if x > 1 else x
            if not 0 <= x <= 1:
                raise ValueError
            g = f"{x:.2f}"
        except ValueError:
            die("--geo-share is the share of viewers in the brief's countries: 0.42 or 42%")
    ppath = proof_path(lpath)
    rows = read_proof(ppath)
    now = now_utc()
    rows.append({"collected_at": iso(now), "metrics_collected_at": "", "campaign": (post or sub).get("campaign") or "",
                 "post": (post or {}).get("job_post") or (sub or {}).get("post") or "",
                 "account": (post or {}).get("account") or (sub or {}).get("account") or "",
                 "platform": (post or {}).get("platform") or (sub or {}).get("platform") or "", "url": url,
                 "views": v, "likes": "", "comments": "", "shares": "", "engagement": "",
                 "published_at": (post or {}).get("published_at") or "",
                 "submission_id": (sub or {}).get("submission_id") or "", "geo_share": g, "source": source.strip()})
    write_proof(ppath, rows)
    print(f"recorded: {v:,} views for {url} ({source.strip()})")


def load_campaigns(folder, files, ledger):
    out = {cid: with_defaults(c) for cid, c in (ledger.get("campaigns") or {}).items() if isinstance(c, dict)}
    paths = files or [p for p in ("campaign.json",) if os.path.isfile(os.path.join(folder, p))]
    for p in paths:
        full = p if os.path.isabs(p) or os.path.isfile(p) else os.path.join(folder, p)
        c = read_json(full, "a campaign file")
        if isinstance(c, dict) and isinstance(c.get("id"), str):
            out[c["id"]] = with_defaults(c)
    return out


def report(folder, lpath, campaign_files, min_hourly=None, week=False):
    ledger = load_ledger(lpath)
    if week:
        return week_report(ledger, lpath)
    camps = load_campaigns(folder, campaign_files, ledger)
    rows = read_proof(proof_path(lpath))
    now = now_utc()
    by_camp = {}
    for e in ledger["posts"].values():
        by_camp.setdefault(e.get("campaign") or "(none)", []).append(e)
    for s in ledger["submissions"]:
        if not find_post(ledger, s["url"])[1]:
            by_camp.setdefault(s.get("campaign") or "(none)", []).append(
                {"url": s["url"], "account": s.get("account") or "made outside the skill", "platform": s.get("platform"),
                 "job_post": s.get("post") or "", "campaign": s.get("campaign")})
    for h in ledger["hours"]:
        by_camp.setdefault(h.get("campaign"), [])
    if not by_camp:
        print("The ledger has nothing yet.")
        return
    demo_any = False
    for cid, posts in by_camp.items():
        c = camps.get(cid)
        known = c is not None
        c = c or with_defaults({})
        if c.get("example_demo"):
            demo_any = True
        cur = c["currency"]
        window, fee = int(c["window_days"]), c["fee_pct"]
        print(f"\n{c.get('name') or cid} ({cid})" + ("" if known else ": campaign terms not found, so no rates. Pass "
                                                    "--campaign-file <its campaign.json>"))
        if c.get("example_demo"):
            print("  EXAMPLE ONLY: made-up numbers for the skill's demo campaign")
        est_open, received, n_rej, n_dec, reasons, below = 0.0, 0.0, 0, 0, [], 0
        settled, counting, elapsed, hooks_seen = 0.0, 0.0, [], []
        for e in posts:
            url = e.get("url")
            sub = find_submission(ledger, url) if url else None
            plat = e.get("platform")
            rate, mn, cap, mv = terms(c, plat)
            snaps = [r for r in rows if url and post_key(r["url"]) == post_key(url)]

            def when(r):
                return parse_time(r["metrics_collected_at"]) or parse_time(r["collected_at"])
            snaps.sort(key=lambda r: when(r) or now)
            live = parse_time(e.get("published_at")) or parse_time(e.get("recorded"))
            start, waiting = live, None
            if c.get("window_from") == "threshold":
                need = threshold_views(c, plat) if known else 0
                crossed = next((when(r) for r in snaps if num(r["views"]) >= need), None) if need else live
                start = crossed
                waiting = need if crossed is None else None
            end = start + datetime.timedelta(days=window) if start else None
            if end:
                snaps = [r for r in snaps if (when(r) or now) <= end] or snaps[:0]
            last = snaps[-1] if snaps else None
            views = num(last["views"]) if last else 0
            if c.get("pay_per_video") and rate <= 0:
                gross, est, why = float(c["pay_per_video"]), round(float(c["pay_per_video"]) * (1 - fee / 100), 2), ""
            else:
                gross, est, why = payout(views, rate, mn, cap, fee, mv, cur)
            if why.startswith("under"):
                below += 1
            label = LIMITS.get(plat, {}).get("label", plat or "?")
            who = f"{e.get('account')}{' ' + e['handle'] if e.get('handle') else ''}"
            who += "" if e.get("account") == label or not plat else f" ({label})"
            status = (sub or {}).get("status") or ("not submitted" if not sub else "pending")
            line = f"  {who}: {views:,} views"
            if last:
                line += f" ({last.get('source') or 'saved reading'})"
            if e.get("hook_id"):
                hooks_seen.append((e["hook_id"], label, views))
                line = f"  {who} [hook {e['hook_id']}]: {views:,} views" + (
                    f" ({last.get('source') or 'saved reading'})" if last else "")
            if status == "paid":
                npay = len(sub.get("payments") or []) or 1
                line += f", paid {money(float(sub.get('paid') or 0), cur)}" + (f" in {npay} payments" if npay > 1 else "")
                received += float(sub.get("paid") or 0)
            elif status == "rejected":
                line += f", REJECTED: {sub.get('reason') or 'no reason recorded'}"
                if sub.get("appeals"):
                    line += f" (appealed {len(sub['appeals'])}x)"
            elif sub:
                line += f", est. {money(est, cur)} after {fee:g}% fee" + (f" ({why})" if why else "") + f", {status}"
                est_open += est
                if end and now >= end:
                    settled += est
                else:
                    counting += est
            else:
                line += ", NOT SUBMITTED: earns nothing"
            if status in ("approved", "paid", "rejected"):
                n_dec += 1
            if status == "rejected":
                n_rej += 1
                reasons.append(sub.get("reason") or "")
            if live and status not in ("paid", "rejected"):
                elapsed.append(min(1.0, (now - live).total_seconds() / 86400 / max(1, window)))
            if waiting and status not in ("paid", "rejected"):
                line += f"; its {window}-day window starts at {waiting:,} views"
            elif end and status not in ("paid", "rejected"):
                left = (end - now).total_seconds() / 86400
                line += f"; {left:.0f} day(s) left" if left > 0 else "; window closed"
            if not url:
                line += "; link not recorded yet"
            print(line)
            if last and last.get("geo_share") and isinstance(c.get("geo"), dict) and is_num(c["geo"].get("min_share")):
                g = float(last["geo_share"])
                if g < c["geo"]["min_share"]:
                    print(f"    {g:.0%} of viewers in {', '.join(place_name(x) for x in c['geo'].get('countries') or [])}; "
                          f"the brief needs {c['geo']['min_share']:.0%}, so expect a rejection")
        hrs = sum(h["hours"] for h in ledger["hours"] if h.get("campaign") == cid)
        print(f"  received {money(received, cur)}; open estimate {money(est_open, cur)} ("
              + (f"{money(settled, cur)} settled: its window closed; " if settled else "nothing settled yet; ")
              + f"{money(counting, cur)} still counting)"
              + (f"; {n_rej} of {n_dec} decided rejected" if n_dec else ""))
        if len({h for h, _, _ in hooks_seen}) > 1:
            print("  hooks: " + "; ".join(f"{h} on {lab} {v:,} views" for h, lab, v in hooks_seen)
                  + (". Different platforms, so read it with care" if len({lab for _, lab, _ in hooks_seen}) > 1 else ""))
        nvid = len([e for e in posts if e.get("sha256")]) or len(posts)
        if hrs:
            per = received / hrs
            per_all = (received + est_open) / hrs
            print(f"  {hrs:g} h logged, {hrs / max(1, nvid):.1f} h per video: {money(per, cur)} per hour received, "
                  f"{money(per_all, cur)} per hour if every open estimate pays")
        else:
            print(f"  no hours logged: ledger.py --hours {cid} <hours> gives earnings per hour")
        hints = []
        if n_rej >= 2 and n_rej * 2 >= n_dec:
            common = max(set(r for r in reasons if r), key=reasons.count, default="")
            hints.append(f"{n_rej} of {n_dec} decided videos were rejected" + (f" (most often: {common})" if common else ""))
        early = bool(elapsed) and min(elapsed) < 0.6
        if hrs >= 3 and min_hourly and (received + est_open) / hrs < min_hourly:
            if early:
                print(f"  under {money(min_hourly, cur)} per hour so far, but views are still counting (the newest video "
                      f"is {min(elapsed):.0%} into its window). Judge it once 60% of the window has passed")
            else:
                hints.append(f"it earns under {money(min_hourly, cur)} per hour even if every open estimate pays")
        if posts and below == len(posts) and all(parse_time(e.get("published_at") or e.get("recorded") or "") and
                                                 (now - parse_time(e.get("published_at") or e.get("recorded"))).days >= 7
                                                 for e in posts if e.get("recorded") or e.get("published_at")):
            hints.append("none of its videos reached the payout minimum after a week")
        if is_num(c.get("budget_remaining"), 0) and c.get("budget_remaining") == 0:
            hints.append("its budget is used up")
        for h in hints:
            print(f"  drop this campaign? {h}. Your hours may pay better on another brief")
    if demo_any:
        print("\nThe EXAMPLE ONLY numbers above are made up for the demo; they say nothing about real earnings.")
    print("\nEstimates only. The campaign's own view count decides what is paid, and many videos earn little.")


def week_report(ledger, lpath):
    """The last 7 days across campaigns: posts made, hours logged, money received."""
    now = now_utc()
    since = now - datetime.timedelta(days=7)
    posts = [e for e in ledger["posts"].values() if (parse_time(e.get("published_at") or e.get("recorded") or "")
                                                     or now) >= since]
    hrs = sum(h["hours"] for h in ledger["hours"] if (parse_time(h.get("at")) or now) >= since)
    got = 0.0
    for x in ledger["submissions"]:
        pays = x.get("payments") if isinstance(x.get("payments"), list) else (
            [{"at": x.get("paid_at"), "amount": x.get("paid")}] if x.get("paid") else [])
        got += sum(float(p.get("amount") or 0) for p in pays if isinstance(p, dict)
                   and (parse_time(p.get("at") or "") or since - datetime.timedelta(days=1)) >= since)
    camps = sorted({e.get("campaign") for e in posts if e.get("campaign")})
    print(f"Last 7 days: {len(posts)} post(s) in {len(camps)} campaign(s){': ' + ', '.join(camps) if camps else ''}; "
          f"{hrs:g} h logged; {money(got)} received" + (f" ({money(got / hrs)} per hour)" if hrs else "") + ".")
    print("Received money only; open estimates are in --report. The campaigns' own counts decide what is paid.")


def show(lpath):
    ledger = load_ledger(lpath)
    print(f"{len(ledger['posts'])} post(s), {len(ledger['submissions'])} submission(s), "
          f"{sum(h['hours'] for h in ledger['hours']):g} h logged in {rel(lpath)}")
    for e in ledger["posts"].values():
        print(f"  {e.get('campaign')}: {e.get('job_post')} on {e.get('account')} {e.get('url') or '(no link yet)'}")
    for s in ledger["submissions"]:
        print(f"  submitted {s['url']} to {s['campaign']} at {s.get('submitted_at')}: {s.get('status', 'pending')}"
              + (f" (submission {s['submission_id']})" if s.get("submission_id") else ""))


def main():
    ap = argparse.ArgumentParser(description="Submissions, status, views, payouts and hours for UGC campaigns.")
    ap.add_argument("--dir", default=".", help="with --report: the folder whose campaign.json to read (default: here)")
    ap.add_argument("--ledger", help="the ledger file (default: UGC_CREATOR_LEDGER, else ~/.ugc-creator/ledger.json)")
    ap.add_argument("--submitted", metavar="URL")
    ap.add_argument("--campaign", help="with --submitted: the campaign id")
    ap.add_argument("--submission-id", help="with --submitted: the id the campaign gave the submission, if any")
    ap.add_argument("--at", help="when (default now). Without a zone it is your computer's clock")
    ap.add_argument("--status", nargs=2, metavar=("URL", "STATUS"), help="pending, approved, rejected or paid")
    ap.add_argument("--reason", help="with --status rejected: the campaign's reason, in its words")
    ap.add_argument("--appeal", metavar="URL")
    ap.add_argument("--note", help="with --appeal or --hours")
    ap.add_argument("--proof", metavar="ANALYTICS_JSON")
    ap.add_argument("--views", nargs=2, metavar=("URL", "VIEWS"))
    ap.add_argument("--source", help="with --views: where the number was read")
    ap.add_argument("--geo-share", help="with --views: share of viewers in the brief's countries (0.42)")
    ap.add_argument("--paid", nargs=2, metavar=("URL", "AMOUNT"))
    ap.add_argument("--paid-campaign", nargs=2, metavar=("CAMPAIGN", "AMOUNT"), help="a lump payout for a campaign")
    ap.add_argument("--appeal-draft", metavar="URL", help="write a short appeal for a rejected post (you send it)")
    ap.add_argument("--week", action="store_true", help="with --report: the last 7 days across campaigns")
    ap.add_argument("--hours", nargs=2, metavar=("CAMPAIGN", "HOURS"))
    ap.add_argument("--report", "--earnings", dest="report", action="store_true")
    ap.add_argument("--min-hourly", type=float, default=None, help="with --report: below this per hour, suggest dropping")
    ap.add_argument("--campaign-file", action="append", default=[], help="a campaign.json (repeat for several)")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    if not os.path.isdir(a.dir):
        die(f"{a.dir} is not a folder")
    lpath = ledger_path(a.ledger)
    if a.submitted:
        if not a.campaign:
            die("--submitted needs --campaign <campaign id>")
        known = set(load_campaigns(a.dir, a.campaign_file, {"campaigns": {}}))
        submitted(lpath, a.submitted, a.campaign, a.at, a.submission_id, known)
    elif a.status:
        set_status(lpath, a.status[0], a.status[1], a.reason, a.at)
    elif a.appeal:
        appeal(lpath, a.appeal, a.note)
    elif a.proof:
        proof(lpath, a.proof)
    elif a.views:
        views_entry(lpath, a.views[0], a.views[1], a.source, a.geo_share)
    elif a.paid:
        paid(lpath, a.paid[0], a.paid[1], a.at)
    elif a.paid_campaign:
        paid_campaign(lpath, a.paid_campaign[0], a.paid_campaign[1], a.at)
    elif a.appeal_draft:
        appeal_draft(lpath, a.appeal_draft, a.dir, a.campaign_file)
    elif a.hours:
        hours(lpath, a.hours[0], a.hours[1], a.note)
    elif a.report:
        report(a.dir, lpath, a.campaign_file, a.min_hourly, a.week)
    elif a.list:
        show(lpath)
    else:
        die("say what to do: --submitted, --status, --appeal, --proof, --views, --paid, --hours, --report or --list")


if __name__ == "__main__":
    guard(main)
