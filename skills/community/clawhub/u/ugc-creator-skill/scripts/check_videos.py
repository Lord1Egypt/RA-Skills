#!/usr/bin/env python3
"""Check every video of a campaign job against the brief, the script, the disclosure rules and each
platform's limits, before anything is planned or posted.

    python3 scripts/check_videos.py job.json           # one line per post, then every problem
    python3 scripts/check_videos.py job.json --json    # the same as JSON

job.json (references/job-file.md) names the campaign, the script, the manifest make_video.py wrote,
the accounts with the settings the user chose, and one post per account: the video, its caption
(and a title for YouTube).

Checked per post:
  the campaign's verdict is GO, the deadline hasn't passed, the brief still has submissions left;
  the video was edited for this campaign from the script as it is now (a script changed after the
  edit means editing again); no placeholder take (the skill's own example excepted);
  the disclosure on screen from the first frame for the brief's seconds, and said out loud within
  the brief's seconds; the caption starts with #ad (or the brief's disclosure) and holds every
  required hashtag, @mention, link and the call to action when the brief wants it in the caption;
  nothing from do_not_say, nothing that plays the ad down, no engagement bait;
  the layout is one the brief accepts, the face on camera when the brief requires it, the footage
  the brand supplied and no other; the music is declared and allowed;
  length, shape, size, frame rate and caption limits per platform; the brand's approval of this
  exact file when the brief asks for it; a dedicated account when the brief asks for one; TikTok
  left out when the topic or a make-money claim isn't allowed there; where the account's viewers are.

Checked across posts: each account opens with its own hook; no two accounts get the same file; no
file posted before, in this campaign or any other (the ledger keeps every fingerprint). A re-export,
a new container or a resize of a posted video or take is the same video: its sound and frames are
compared, not only its bytes.

Exit code 0 when nothing blocks posting, 1 otherwise. plan.py runs the same checks.
"""
import argparse, json, os, re, sys

sys.dont_write_bytecode = True   # nothing is ever written into the skill's own folder
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import campaign as campaign_mod  # noqa: E402
import script as script_mod  # noqa: E402
from ugclib import (ENGAGEMENT_BAIT, ENGAGEMENT_SOFT, LIMITS, PLATFORMS, TIKTOK_PRIVACY, account_key, die,  # noqa: E402
                    file_issues, find_phrases, guard, hashtags, hide_ad_hits, is_num, ledger_path, links, load_ledger,
                    load_saved_accounts, mentions, money, norm_link, now_utc, parse_time, place_name, placeholder_id,
                    probe, read_json, rel, sha256, text_length, valid_id, words_of)
from ugclib import (content_words, disclosure_targets, find_disclosure, fp_same, free_text_problems,  # noqa: E402
                    has_banned, media_fp, negated, says_paid, script_match, split_sentences)

PRIVACY_WORDS = {"PUBLIC_TO_EVERYONE": "everyone", "MUTUAL_FOLLOW_FRIENDS": "friends",
                 "FOLLOWER_OF_CREATOR": "followers", "SELF_ONLY": "only you"}
ACCOUNT_OF = {"TIKTOK": "TikTok", "INSTAGRAM": "Reels", "YOUTUBE": "Shorts"}


class Checks:
    def __init__(self):
        self.items = []

    def add(self, level, where, msg):
        if (level, where, msg) not in self.items:
            self.items.append((level, where, msg))

    def errors(self):
        return [i for i in self.items if i[0] == "error"]


def starts_with(text, disclosure):
    """The caption opens with the disclosure as its own word: "#ad ..." yes, "#ad_..." or "#ads" no."""
    t, d = (text or "").lstrip().lower(), disclosure.strip().lower()
    return t.startswith(d) and (len(t) == len(d) or t[len(d)].isspace() or t[len(d)] in ".,:;!|-")


def has_link(text, want):
    """A link the brief requires, matched as a link (not part of a longer one). A bare domain is
    satisfied by any link on it."""
    w = norm_link(want)
    found = [norm_link(x) for x in links(text)]
    if w in found:
        return True
    if "/" not in w and any(f.split("/")[0] == w for f in found):
        return True
    low = re.sub(r"(?i)https?://(?:www\.)?|(?<![\w.])www\.", "", (text or "").lower())
    return re.search(r"(?<![\w./-])" + re.escape(w) + r"(?![\w/-])", low) is not None


def has_phrase(text, phrase):
    """The words of a phrase in order in the text, punctuation and case aside."""
    want = " ".join(words_of(phrase))
    return bool(want) and f" {want} " in f" {' '.join(words_of(text))} "


def same_name(a, b):
    return os.path.basename(str(a or "")).casefold() == os.path.basename(str(b or "")).casefold()


def check_account(acc, n, camp, ck):
    where = f"account {acc.get('name') or n}"
    p = acc.get("platform")
    if camp.get("marketplace"):
        mk = camp["marketplace"]
        ver = acc.get("marketplace_verified")
        if ver is False:
            ck.add("error", where, f"not connected in {mk}: posts from an account that isn't connected and verified there "
                   "are rejected. Connect it there first, or leave it out")
        elif ver is not True and not campaign_mod.deliver(camp):
            ck.add("error", where, f"ask the user: is this account connected and verified in {mk}? Posts from an "
                   "account that isn't are rejected (set \"marketplace_verified\": true once it is)")
    el = camp.get("eligibility") if isinstance(camp.get("eligibility"), dict) else None
    if el and not campaign_mod.deliver(camp) and acc.get("eligible") is not True:
        ck.add("error", where, "the brief sets who may take part (followers, account age, country, account type, "
               "public). Ask the user whether this account meets every point on the checklist; set \"eligible\": true "
               "only when it does")
    if camp.get("dedicated_account") and acc.get("dedicated") is not True:
        ck.add("error", where, "the brief wants a dedicated account (one made for this kind of content). Ask the user; "
               "set \"dedicated\": true only when it is one")
    geo = camp.get("geo") if isinstance(camp.get("geo"), dict) else None
    known = acc.get("audience") if isinstance(acc.get("audience"), dict) else None
    if geo and isinstance(geo.get("countries"), list) and is_num(geo.get("min_share")):
        want = [str(x).upper() for x in geo["countries"]]
        places = ", ".join(place_name(x) for x in want)
        if known:
            got = sum(v for k, v in known.items() if str(k).upper() in want and is_num(v, 0))
            if got < geo["min_share"]:
                ck.add("warning", where, f"about {got:.0%} of this account's viewers are in {places}; the brief needs "
                       f"{geo['min_share']:.0%}. Expect a rejection: post from an account whose viewers are there, or "
                       "skip it. Never a VPN or location trick")
        else:
            ck.add("note", where, f"the brief needs {geo['min_share']:.0%} of viewers in {places}. Ask the user what the "
                   "app's audience countries show for this account and add \"audience\": {\"US\": 0.5, ...}")
    if p not in PLATFORMS:
        ck.add("error", where, f"platform must be one of {', '.join(PLATFORMS)}")
        return
    plats = camp.get("platforms") if isinstance(camp.get("platforms"), dict) else {}
    if p not in plats:
        ck.add("error", where, f"the brief doesn't pay for {LIMITS[p]['label']}; leave this account out or check the brief")
    if p == "TIKTOK" and camp.get("tiktok_blocked"):
        ck.add("error", where, "TikTok doesn't allow this campaign as branded content (a banned topic, or a brief that "
               "frames it as quick or easy money). Leave TikTok out; the brief's other platforms may still take it")
    if p == "TIKTOK" and camp.get("make_money_campaign") and not camp.get("tiktok_blocked"):
        ck.add("note", where, "content about earning money on TikTok: allowed when plain and true. TikTok bans "
               "get-rich-quick branded content, so the script, the captions and what you say are checked for it")
    sid = acc.get("socialAccountId")
    hand = acc.get("by_hand")
    if hand is not None and not isinstance(hand, bool):
        ck.add("error", where, "by_hand is true (the user posts this account in the app) or false")
    if hand is True and sid is not None:
        ck.add("error", where, "by_hand is true and the account also has a socialAccountId. Say which: through "
               "WoopSocial (keep the id) or by hand (take the id out)")
    elif sid is not None and (not isinstance(sid, str) or placeholder_id(sid)):
        ck.add("error", where, "socialAccountId is a placeholder. Put the id from this session's social_accounts_list, "
               "or set \"by_hand\": true to post this account in the app")
    elif sid is None and hand is not True:
        ck.add("error", where, "say how this account posts: \"socialAccountId\" from this session's social_accounts_list "
               "(through WoopSocial), or \"by_hand\": true (the user posts it in the app)")
    if p == "TIKTOK":
        pl = acc.get("privacyLevel")
        opts = acc.get("privacyOptions")
        if hand is not True and not (isinstance(opts, list) and opts):
            ck.add("error", where, "read who can see posts on this TikTok account from WoopSocial "
                   "(social_accounts_get_platform_inputs) and save the choices as \"privacyOptions\"; then ask the user")
            opts = []
        opts = opts if isinstance(opts, list) else list(TIKTOK_PRIVACY)
        if pl is None:
            ck.add("error", where, "ask the user who can see this TikTok (" + ", ".join(
                PRIVACY_WORDS.get(o, str(o)) for o in (opts or TIKTOK_PRIVACY)) + "). TikTok makes the account owner "
                "choose; it is never defaulted")
        elif opts and pl not in opts:
            ck.add("error", where, f"privacyLevel {pl} isn't one this account offers ({', '.join(map(str, opts))})")
        elif pl == "SELF_ONLY":
            ck.add("error", where, "a branded post can't be \"only you\" on TikTok, and a private post earns no views")
        elif pl != "PUBLIC_TO_EVERYONE":
            ck.add("warning", where, f"seen by {PRIVACY_WORDS.get(pl, pl)} only: campaigns pay for public views")
        for k, w in (("allowComment", "comments"), ("allowDuet", "duets"), ("allowStitch", "stitches")):
            if not isinstance(acc.get(k), bool):
                ck.add("error", where, f"ask the user: {w} on or off? (TikTok makes the account owner choose)")
    if p == "YOUTUBE":
        if acc.get("privacy") not in ("public", "unlisted", "private"):
            ck.add("error", where, "ask the user: public, unlisted or private? (campaigns count public views only)")
        elif acc["privacy"] != "public":
            ck.add("warning", where, f"{acc['privacy']}: campaigns pay for public views")
        if not isinstance(acc.get("madeForKids"), bool):
            ck.add("error", where, "ask the user: is this Short made for kids? (YouTube makes the owner declare it)")


def manifest_entries(job, job_dir, ck):
    """{sha256: (entry, manifest, folder)} for every video in the manifest(s) make_video.py wrote."""
    paths = job.get("manifest", "videos/manifest.json")
    paths = [paths] if isinstance(paths, str) else paths
    if not isinstance(paths, list):
        ck.add("error", "job", "\"manifest\" is the path of videos/manifest.json (or a list of them)")
        return {}
    out = {}
    for mp in paths:
        full = os.path.join(job_dir, mp) if isinstance(mp, str) else None
        if not full or not os.path.isfile(full):
            ck.add("error", "job", f"manifest {mp} not found. Edit the videos with make_video.py first")
            continue
        m = read_json(full, "the video manifest")
        if not isinstance(m, dict) or not isinstance(m.get("videos"), list):
            ck.add("error", "job", f"{mp} is not a manifest written by make_video.py")
            continue
        for v in m["videos"]:
            if isinstance(v, dict) and isinstance(v.get("sha256"), str):
                out[v["sha256"]] = (v, m, os.path.dirname(full))
    return out


SUGGEST = (("allowComment", "comments"), ("allowDuet", "duets"), ("allowStitch", "stitches"), ("privacy", "visibility"),
           ("madeForKids", "made for kids"), ("audience", "audience"))


def saved_suggestions(accounts):
    """Lines for saved accounts (plan.py --remember-accounts) that match an account of this job on
    platform AND handle. Nothing is filled in: the agent shows these and writes what the user confirms."""
    saved = {account_key(a): a for a in load_saved_accounts() if account_key(a)}
    out = []
    for a in accounts:
        s = saved.get(account_key(a))
        if not s:
            continue
        bits = [f"{w} {'on' if s[k] is True else 'off' if s[k] is False else json.dumps(s[k])}"
                for k, w in SUGGEST if k in s and k not in a]
        if bits:
            out.append(f"{a['name']} {a.get('handle')}: last time {', '.join(bits)}")
    return out


def music_issue(camp_rule, music):
    """The music in the video against the brief: declared, licensed where needed, the brief's track
    where the brief names one."""
    if not isinstance(music, dict) or music.get("source") not in ("none", "licensed", "brief_supplied"):
        return "the music isn't declared. Say what plays under the voice in edit.json (\"music\": {\"source\": \"none\"} " \
               "or the licensed track with where its license is) and edit again"
    src = music["source"]
    if camp_rule == "none" and src != "none":
        return "the brief wants no music under the voice; this video has some"
    if camp_rule == "brief_supplied" and src != "brief_supplied":
        return "the brief supplies the track to use; use that one (\"source\": \"brief_supplied\")"
    if src in ("licensed", "brief_supplied") and not (isinstance(music.get("license"), str) and music["license"].strip()):
        return "music: say where its license is (a receipt, the library's terms, the brief's track)"
    return None


def check_job(job_path, ledger_file=None):
    """Load and check a job. Returns the model the plan is drawn from: campaign, script, accounts, one
    row per post with its file facts, texts and problems, and every check."""
    ck = Checks()
    job = read_json(job_path, "the campaign job")
    job_dir = os.path.dirname(os.path.abspath(job_path))
    if not isinstance(job, dict):
        die(f"{rel(job_path)} must hold one JSON object: campaign, script, manifest, accounts and posts")
    for k in ("campaign", "script"):
        if not isinstance(job.get(k), str) or not os.path.isfile(os.path.join(job_dir, job[k])):
            die(f"{rel(job_path)} needs \"{k}\": the path of {k}.json")
    info = campaign_mod.load(os.path.join(job_dir, job["campaign"]))
    camp = info["campaign"] if isinstance(info["campaign"], dict) else {}
    demo = campaign_mod.example_demo(camp)
    cerrs = [i for i in info["issues"] if i[0] == "error"]
    if cerrs:
        die(f"{job['campaign']} has {len(cerrs)} problem(s); fix them first (python3 scripts/campaign.py "
            f"{job['campaign']}):\n" + "\n".join(f"  {f}: {m}" for _, f, m in cerrs))
    for lv, f, m in info["issues"]:
        ck.add(lv, "campaign", f"{f}: {m}")
    if info["verdict"] != "GO":
        ck.add("error", "campaign", f"the verdict is {info['verdict']}: " + "; ".join(info["reasons"][:3]))
    if campaign_mod.deadline_passed(camp.get("deadline"), now_utc(), camp.get("deadline_tz")):
        ck.add("error", "campaign", f"the deadline ({camp.get('deadline')}) has passed; posts after it aren't paid")
    sm = script_mod.check_script(os.path.join(job_dir, job["script"]))
    for lv, w, m in sm["issues"]:
        if lv == "error":
            ck.add("error", "script", f"{w}: {m}")
    deliver = campaign_mod.deliver(camp)
    accounts = job.get("accounts")
    if deliver:
        accounts = accounts if isinstance(accounts, list) else []
    elif not isinstance(accounts, list) or not accounts or not all(isinstance(a, dict) for a in accounts):
        die(f"{rel(job_path)} needs \"accounts\": one entry per account, like {{\"name\": \"TikTok\", \"platform\": "
            "\"TIKTOK\", ...}}")
    names = [a.get("name") for a in accounts]
    if not all(isinstance(n, str) and n.strip() for n in names):
        die("every account needs a \"name\" (as script.json's openings name it: \"TikTok\", \"Reels\", \"Shorts\")")
    if len(set(names)) != len(names):
        die("two accounts share a name; give each its own")
    for line in saved_suggestions(accounts):
        ck.add("note", "accounts", f"saved choice for {line}. Confirm it with the user, then write it into job.json")
    for n, a in enumerate(accounts, 1):
        if a.get("handle") is not None and not isinstance(a.get("handle"), str):
            die(f"account {a['name']}: \"handle\" is the account's @name as text, like \"@example.creator\"")
        if a.get("max_video_s") is not None and not is_num(a.get("max_video_s"), 1):
            die(f"account {a['name']}: \"max_video_s\" is the longest video this TikTok account may post, in seconds "
                "(a number), or left out")
        if isinstance(a.get("platform"), str):
            a["platform"] = a["platform"].strip().upper()
        check_account(a, n, camp, ck)
    seen_ids, seen_keys = {}, {}
    for a in accounts:
        sid = a.get("socialAccountId")
        if isinstance(sid, str) and sid.strip():
            if sid in seen_ids:
                ck.add("error", f"account {a['name']}", f"the same socialAccountId as {seen_ids[sid]}: that is one account "
                       "listed twice, and two posts to one account in one go is a duplicate")
            seen_ids.setdefault(sid, a["name"])
        k = account_key(a)
        if k:
            if k in seen_keys:
                ck.add("error", f"account {a['name']}", f"the same platform and handle as {seen_keys[k]}: one account "
                       "listed twice")
            seen_keys.setdefault(k, a["name"])
    by_name = {a["name"]: a for a in accounts}
    posts = job.get("posts")
    if not isinstance(posts, list) or not posts or not all(isinstance(p, dict) for p in posts):
        die(f"{rel(job_path)} needs \"posts\": one post per account (video, caption, title for YouTube)")
    lpath = ledger_path(ledger_file)
    ledger = load_ledger(lpath)
    manifest = manifest_entries(job, job_dir, ck)
    cap = camp.get("caption") if isinstance(camp.get("caption"), dict) else {}
    disclosure = cap.get("disclosure") if isinstance(cap.get("disclosure"), str) and cap["disclosure"].strip() else "#ad"
    dcfg = camp.get("disclosure") or {}
    want_sd = dcfg.get("on_screen")
    want_secs = dcfg.get("on_screen_seconds") or 3
    spoken_within = dcfg.get("spoken_within_s") or 10
    length = camp.get("length") if isinstance(camp.get("length"), dict) else {}
    allowed_files = (camp.get("supplied_footage") or {}).get("files") or []
    formats = camp.get("formats_list") or []
    links_where = camp.get("links_where") or "caption"
    cta = camp.get("cta") if isinstance(camp.get("cta"), str) and camp["cta"].strip() else None
    ai_default = job.get("ai_generated")
    raw = info["raw"] if isinstance(info["raw"], dict) else {}
    te = raw.get("typical_earnings") if isinstance(raw.get("typical_earnings"), dict) else {}
    te_line = te.get("line") if isinstance(te.get("line"), str) and te["line"].strip() else None
    confirmed = [r["say"] for r in sm["spoken"] if r.get("confirmed")] + \
        [h["say"] for h in (sm.get("hook_rows") or {}).values() if h.get("confirmed")]
    points = [t for _, t in camp.get("talking_points_list") or []]
    script_texts = [r["say"] for r in sm["spoken"]] + list(sm["hooks"].values())
    match_lines = [r["say"] for r in sm["spoken"]] + [t for t in (camp.get("brand"), cta, te_line) if t]
    disc_lines = [r["say"] for r in sm["spoken"] if r.get("kind") == "disclosure"]
    not_in_hook = dcfg.get("not_in_hook") is True
    not_before = float(dcfg["not_before_s"]) if is_num(dcfg.get("not_before_s")) else None
    burned = campaign_mod.burned_text(camp)
    pos_by = camp.get("product_on_screen_by_s")
    rows, ids = [], set()

    def disclosure_of(sentences, hooks):
        """Where the script's own disclosure (or a hook that discloses) is said in these sentences."""
        targets = disclosure_targets(disc_lines, [] if not_in_hook else hooks, camp.get("brand"))
        return find_disclosure(sentences or [], targets, camp.get("brand")) if targets else None
    for n, p in enumerate(posts, 1):
        pid = p.get("id")
        where = f"post {pid if isinstance(pid, str) else n}"
        if not valid_id(pid):
            ck.add("error", where, "give each post a short id of lowercase letters, digits and dashes (like \"orbit-tiktok\")")
            pid = f"post-{n}"
        if pid in ids:
            ck.add("error", where, "this post id is used twice; give each post its own")
        ids.add(pid)
        acc = by_name.get(p.get("account"))
        if acc is None and not deliver:
            ck.add("error", where, f"account \"{p.get('account')}\" isn't in accounts ({', '.join(names)})")
            continue
        if deliver and acc is None and p.get("platform") not in PLATFORMS:
            ck.add("error", where, f"\"platform\": which platform this file is for ({', '.join(PLATFORMS)}), so its limits "
                   "are checked")
            continue
        acc = acc or {"name": p.get("account") or pid, "platform": p.get("platform")}
        plat = acc.get("platform")
        if plat not in LIMITS:
            continue
        label = LIMITS[plat]["label"]
        row = {"id": pid, "account": acc, "name": acc["name"], "platform": plat, "label": label,
               "handle": acc.get("handle") or "", "connected": isinstance(acc.get("socialAccountId"), str)
               and not placeholder_id(acc["socialAccountId"]) and acc.get("by_hand") is not True,
               "post": p, "issues": [], "posted": None}

        def bad(level, msg, _row=row, _where=where):
            ck.add(level, _where, msg)
            _row["issues"].append((level, msg))
        ai = p.get("ai_generated", ai_default)
        if not isinstance(ai, bool):
            bad("error", "ask the user: does the video use realistic AI-made scenes or voices anywhere (b-roll, music "
                "vocals)? (\"ai_generated\": true or false). The person on camera is always the creator")
        row["ai"] = ai
        f = p.get("file")
        full = os.path.join(job_dir, f) if isinstance(f, str) and f else None
        if not full or not os.path.isfile(full):
            bad("error", f"video file {f!r} not found" if f else "\"file\": which video this account gets")
            rows.append(row)
            continue
        row["file"] = rel(full, job_dir)
        row["full"] = full
        vinfo = probe(full, row["file"])
        row["info"] = vinfo
        row["sha256"] = sha256(full)
        # the edit: from make_video.py, for this campaign, from the script as it is now
        ent = manifest.get(row["sha256"])
        row["screen"], row["hook"], row["hook_id"], row["cover"], row["layout"] = {}, "", None, None, None
        row["spoken"], row["takes"] = None, []
        own = p.get("own_edit")
        if own is not None:
            # an edit the creator made in their own app: the same checks, from its own transcript and the
            # creator's look at its first frames
            if not isinstance(own, dict):
                bad("error", "\"own_edit\" is {\"transcript\", \"on_screen\", \"confirmed_by_user\", \"layout\", \"music\"}")
                own = {}
            tp = own.get("transcript")
            tfull = os.path.join(job_dir, tp) if isinstance(tp, str) and tp else None
            tr = read_json(tfull, "the transcript of your edit") if tfull and os.path.isfile(tfull) else None
            if not isinstance(tr, dict) or not isinstance(tr.get("words"), list):
                bad("error", "own_edit needs \"transcript\": run transcribe.py on this exact file (python3 scripts/"
                    f"transcribe.py {row['file']} --out work/{pid}) and name its transcript.json")
            elif tr.get("video_sha256") != row["sha256"]:
                bad("error", f"{tp} was made from another file, not {row['file']}. Transcribe this exact file again")
            else:
                row["spoken"] = split_sentences(tr["words"])
                row["transcript"] = {"file": rel(tfull, job_dir), "sha256": sha256(tfull)}
            osd = own.get("on_screen") if isinstance(own.get("on_screen"), dict) else {}
            row["screen"] = {"disclosure": osd.get("disclosure"), "disclosure_seconds": osd.get("seconds"),
                             "from": osd.get("from", 0.0)}
            if own.get("confirmed_by_user") is not True:
                bad("error", "show the creator the first seconds of this file (python3 scripts/make_video.py --frames "
                    f"{row['file']}) and ask: is the disclosure readable on screen from the first frame, for how long? "
                    "Set \"confirmed_by_user\": true with what they saw")
            row.update(layout=own.get("layout"), music=own.get("music"), hook=own.get("hook") or "",
                       inputs={}, placeholder=False, own_edit=True, product_on_screen_s=own.get("product_on_screen_s"))
            row["takes"] = [row["sha256"]]
            row["take_files"] = []
            # the clips the edit was cut from: a take goes into one campaign only, whoever edited it
            otk = own.get("take")
            for tk in ([otk] if isinstance(otk, str) else otk if isinstance(otk, list) else []):
                tkf = os.path.join(job_dir, tk) if isinstance(tk, str) and tk else None
                if not tkf or not os.path.isfile(tkf):
                    bad("error", f"own_edit \"take\": {tk!r} not found. Name the clip(s) you filmed and cut this edit from")
                    continue
                row["takes"].append(sha256(tkf))
                row["take_files"].append(tkf)
            if otk is None:
                bad("warning", "own_edit: name the clip(s) you cut this from as \"take\", so a take is never used for "
                    "two campaigns or posted twice")
            oh = row["hook"]
            if not (isinstance(oh, str) and oh.strip()):
                bad("error", "own_edit needs \"hook\": the first words of your edit, as said and shown")
            else:
                for lv, msg in free_text_problems(oh, camp, confirmed, points, te_line, said=True):
                    bad(lv, f"hook \"{oh}\": {msg}")
                sc, _ = script_match(oh, list(sm["hooks"].values()))
                if sc < 0.6:
                    bad("error", f"hook \"{oh}\" isn't one of the script's hooks. Add it to script.json (tagged, and "
                        "confirmed if it is about you) and run script.py, or open with a script hook")
            if row["layout"] not in campaign_mod.FORMATS:
                bad("error", f"own_edit \"layout\": which format it is ({', '.join(campaign_mod.FORMATS)})")
            elif formats and row["layout"] not in formats:
                bad("error", f"the layout {row['layout']} isn't one the brief accepts ({', '.join(formats)})")
            mi = music_issue(camp.get("music"), row["music"])
            if mi:
                bad("error", mi)
        elif not ent:
            bad("error", "this file isn't in the manifest make_video.py wrote (or it changed after editing). Edit it with "
                "make_video.py, or for an edit you made yourself add \"own_edit\" to this post (references/job-file.md)")
        if ent and own is None:
            v, m, mdir = ent
            row.update(screen=v.get("on_screen") or {}, hook=v.get("hook") or "", hook_id=v.get("hook_id"),
                       layout=v.get("layout"), music=v.get("music"),
                       inputs=v.get("inputs") or {}, placeholder=v.get("placeholder") is True,
                       spoken=v.get("spoken"), product_on_screen_s=v.get("product_on_screen_s"),
                       estimated=v.get("spoken_disclosure_estimated") is True,
                       cover=os.path.join(mdir, v["cover"]) if isinstance(v.get("cover"), str) else None)
            row["takes"] = sorted({x["sha256"] for k, x in (row["inputs"] or {}).items()
                                   if k in ("creator", "voiceover", "hook_take") and isinstance(x, dict)
                                   and isinstance(x.get("sha256"), str)})
            row["take_files"] = [os.path.join(mdir, x["file"]) for k, x in (row["inputs"] or {}).items()
                                 if k in ("creator", "voiceover", "hook_take") and isinstance(x, dict)
                                 and isinstance(x.get("file"), str) and os.path.isfile(os.path.join(mdir, x["file"]))]
            if v.get("hook_take") is True and not (row["inputs"] or {}).get("hook_transcript"):
                bad("error", "this video opens with a hook take that was never transcribed, so what it says is unchecked. "
                    "Run transcribe.py on the hook take, add \"hook_transcript\" in edit.json and edit again")
            ecamp = v.get("campaign", m.get("campaign"))
            ever = v.get("script_version", m.get("script_version"))
            if ecamp != camp.get("id"):
                bad("error", f"this video was edited for campaign {ecamp}, not {camp.get('id')}. Edit it again "
                    "for this campaign: the disclosure and script follow its brief")
            if ever != sm["version"]:
                bad("error", "the script changed after this video was edited (script version "
                    f"{ever} in the edit, {sm['version']} now). Film or edit again from the new script")
            if not row["placeholder"] and not isinstance(row["spoken"], list):
                bad("error", "this video was edited by an older make_video.py that didn't keep what was said. Edit it "
                    "again so the checks can read the take")
            vaccs = v.get("accounts") or ([v["account"]] if v.get("account") else [])
            if vaccs and acc["name"] not in vaccs:
                bad("error", f"this video was edited for {', '.join(vaccs)}, not {acc['name']}: its opening and the "
                    "cross-post rules follow the accounts it was made for. Add the account to the video's \"accounts\" "
                    "in edit.json and edit again, or use that account's video")
            if row["placeholder"]:
                if demo:
                    bad("note", "placeholder take: the skill's example has no person in it. A real video is your own "
                        "recording")
                else:
                    bad("error", "this video holds a placeholder where your recording goes. Film it (shotlist.md), "
                        "transcribe it and edit again")
            if formats and row["layout"] not in formats:
                bad("error", f"the layout {row['layout']} isn't one the brief accepts ({', '.join(formats)})")
            if camp.get("face") == "required" and row["layout"] == "broll_voiceover":
                bad("error", "the brief wants your face on camera; a b-roll voiceover has none")
            sup = row["inputs"].get("supplied") if isinstance(row["inputs"], dict) else None
            if sup and allowed_files and not any(same_name(sup.get("file"), x) for x in allowed_files):
                bad("error", f"the footage {sup.get('file')} isn't footage this brief supplied ({', '.join(allowed_files)})")
            mi = music_issue(camp.get("music"), row["music"])
            if mi:
                bad("error", mi)
        if ent or own is not None:
            # disclosure: on screen from the first frame, said out loud early
            sd = row["screen"].get("disclosure")
            if burned == "none":
                if isinstance(sd, str) and sd.strip():
                    bad("error", f"the brief wants no text on the video, and this one shows \"{sd}\". Edit it again")
                elif not deliver:
                    bad("note", "no text on the video, as the brief asks: the disclosure is said out loud, #ad opens the "
                        "caption, and the platform's paid-partnership setting goes on")
            elif not isinstance(sd, str) or not sd.strip():
                bad("error", "no disclosure on screen. Every campaign video shows \"Ad\" (or the brief's line) from the "
                    "first frame; edit it again with make_video.py")
            elif not campaign_mod.screen_line_ok(sd, camp):
                bad("error", f"the on-screen line \"{sd}\" doesn't say the video is paid")
            elif isinstance(want_sd, str) and want_sd.strip() and " ".join(sd.split()).casefold() != \
                    " ".join(want_sd.split()).casefold():
                bad("error", f"the video says \"{sd}\" on screen; this brief's disclosure is \"{want_sd}\". Edit it again")
            else:
                start = row["screen"].get("from", 0)
                secs = row["screen"].get("disclosure_seconds", 0)
                if not is_num(start, 0) or start > 0.5:
                    bad("error", "the on-screen disclosure must show from the first frame, before anyone can swipe")
                if not is_num(secs) or secs < max(2, float(want_secs)):
                    bad("error", f"the on-screen disclosure shows {secs} s; the brief wants {float(want_secs):g} s (at least 2)")
            # the spoken disclosure: the script's own line (or a hook that discloses), found in what was said.
            # A word that merely contains "ad", "I saw an ad" or "nobody is paying me" never counts
            hooks_here = [row["hook"]] if row.get("hook") else []
            found = disclosure_of(row["spoken"], hooks_here) if isinstance(row["spoken"], list) else None
            at = found["end"] if found else None
            row["spoken_at"] = at
            if at is None:
                bad("error", "the script's disclosure line isn't said in the video (" + (
                    "\"" + disc_lines[0] + "\"" if disc_lines else "no line of kind \"disclosure\" in the script") +
                    ", or a close match, or a hook that discloses). Film it and edit again")
            else:
                if at > float(spoken_within) + 0.5:
                    bad("error", f"the disclosure is said by {at:.1f} s; the brief wants it within {float(spoken_within):g} s. "
                        "Say it anywhere that ends inside the window, as a short phrase if you like")
                if not_before is not None and found["start"] < not_before - 0.3:
                    bad("error", f"the disclosure starts at {found['start']:.1f} s; the brief wants it from second "
                        f"{not_before:g}. Put a line before it")
            if not_in_hook and isinstance(row["spoken"], list) and row["spoken"]:
                first = row["spoken"][0]
                if says_paid(first.get("text", ""), camp.get("brand")) and first.get("start", 0) < 3.0:
                    bad("error", "the brief says not to say it's an ad in the hook, and the video opens with it. Disclose "
                        "in a line after the hook")
            # what was actually said: the same rules as the script
            for snt in row["spoken"] or []:
                t = snt.get("text") if isinstance(snt, dict) else None
                if not isinstance(t, str) or not t.strip():
                    continue
                when = f"said at {snt.get('start', 0):.1f} s: \"{t}\""
                for lv, msg in free_text_problems(t, camp, confirmed, points, te_line, said=True):
                    bad(lv, f"{when}: {msg}")
                cands = match_lines + ([row["hook"]] if row.get("hook") else []) + \
                    ([] if row.get("hook") else list(sm["hooks"].values()))
                sc, best = script_match(t, cands)
                if sc < 0.6:
                    bad("error", f"{when}: this isn't in the script. Add it to script.json (tagged, and confirmed if it "
                        "is about you) or cut it from the edit")
                elif best and negated(t) != negated(best):
                    bad("error", f"{when}: the script says \"{best}\", and this " + (
                        "adds a \"not\" or \"never\"" if negated(t) else "drops its \"not\" or \"never\"") +
                        ". That turns the line around: say it as written")
            # the product on screen in time
            if is_num(pos_by):
                ps = row.get("product_on_screen_s")
                if not is_num(ps) or ps > float(pos_by) + 0.2:
                    bad("error", f"the brief wants the product on screen by {float(pos_by):g} s" + (
                        f"; it shows at {ps:.1f} s" if is_num(ps) else "; this layout doesn't show it. Add an insert "
                        "(a screen recording or product shot) over an early line in edit.json"))
        # the brand's approval of this exact file
        appr = p.get("approved")
        if camp.get("pre_approval"):
            if isinstance(appr, dict):
                fp = appr.get("sha256")
                if not isinstance(fp, str) or len(fp) < 12 or not row["sha256"].startswith(fp.lower()):
                    bad("error", "this file changed after the brand approved it. Send the new version for approval, or "
                        "post the approved file")
                if not (isinstance(appr.get("evidence"), str) and appr["evidence"].strip()):
                    bad("error", "\"approved\" needs \"evidence\": the brand's message or a link to it, word for word")
                if appr.get("account") != acc["name"]:
                    bad("error", f"\"approved\" needs \"account\": the account the brand approved it for ({acc['name']} "
                        "here). It must go out from that account")
                row["approved"] = appr
            else:
                bad("error", "the brief asks for the brand's approval before posting. Send the approval packet "
                    f"(approval/{pid}.md, written by plan.py) and record the answer as \"approved\": "
                    f"{{\"by\": ..., \"at\": ..., \"sha256\": \"{row['sha256'][:12]}\"}}")
                row["needs_approval"] = True
        for lv, msg in file_issues(vinfo, plat, acc.get("max_video_s") if plat == "TIKTOK" else None):
            bad(lv, msg)
        s = vinfo["duration"]
        if is_num(length.get("min_s")) and s + 0.3 < length["min_s"]:
            bad("error", f"{s:.1f} s is shorter than the brief's minimum of {length['min_s']:g} s")
        if is_num(length.get("max_s")) and s - 0.3 > length["max_s"]:
            bad("error", f"{s:.1f} s is longer than the brief's maximum of {length['max_s']:g} s")
        if camp.get("aspect", "9:16") == "9:16" and abs(vinfo["width"] / vinfo["height"] - 9 / 16) > 0.03:
            bad("error", f"{vinfo['width']}x{vinfo['height']} isn't vertical 9:16")
        # the texts
        text, title, tags = p.get("caption"), p.get("title"), p.get("tags") or []
        row["text"] = text if isinstance(text, str) else ""
        row["title"] = title if isinstance(title, str) else ""
        row["tags"] = tags if isinstance(tags, list) else []
        if not row["text"].strip():
            bad("error", "write a caption" + (" (the YouTube description)" if plat == "YOUTUBE" else ""))
        text = row["text"]
        if plat == "YOUTUBE" and not deliver:
            if not row["title"].strip():
                bad("error", "a YouTube Short needs a title")
            elif len(row["title"]) > 100:
                bad("error", f"the title has {len(row['title'])} characters; YouTube allows 100")
            if not all(isinstance(t, str) for t in row["tags"]):
                bad("error", "\"tags\" is a list of words")
                row["tags"] = []
            if any(ch in (row["title"] + text) for ch in "<>"):
                bad("error", "YouTube refuses < and > in a title or description")
        row["count"] = text_length(plat, text)
        lim = LIMITS[plat].get("text") or LIMITS[plat].get("text_bytes")
        if row["count"] > lim:
            bad("error", f"the caption is {row['count']} long; {label} allows {lim}")
        if text and not starts_with(text, disclosure):
            bad("error", f"the caption must start with {disclosure} as its own word, so viewers see it before \"more\"")
        tags_in = {h.lower() for h in hashtags(text)}
        for h in cap.get("hashtags") or []:
            if isinstance(h, str) and h.lower() not in tags_in:
                bad("error", f"the brief requires {h} in the caption")
        handles_in = {x.lower() for x in mentions(text)}
        for x in cap.get("mentions") or []:
            if isinstance(x, str) and x.lower() not in handles_in:
                bad("error", f"the brief requires {x} in the caption")
        for u in cap.get("links") or []:
            if not isinstance(u, str) or has_link(text, u) or links_where == "bio":
                continue
            if links_where == "either":
                bad("note", f"{u} isn't in the caption, so it must be in the bio (set it before posting)")
            else:
                bad("error", f"the brief requires the link {u} in the caption")
        if links_where == "bio" and cap.get("links") and not deliver:
            bad("note", "set the bio link to " + ", ".join(x for x in cap["links"] if isinstance(x, str))
                + " on this account before posting")
        if cta and camp.get("cta_in") in ("caption", "both") and not has_phrase(text, cta):
            bad("error", f"the brief wants the call to action in the caption: \"{cta}\"")
        if plat == "INSTAGRAM" and len(hashtags(text)) > LIMITS["INSTAGRAM"]["tags_max"]:
            bad("error", f"{len(hashtags(text))} hashtags; Instagram allows {LIMITS['INSTAGRAM']['tags_max']}")
        everything = " ".join([text, row["title"], row["hook"], " ".join(t for t in row["tags"] if isinstance(t, str))])
        for b in camp.get("do_not_say") or []:
            if isinstance(b, str) and b.strip() and has_banned(everything, b):
                bad("error", f"the brief says never to say \"{b}\"")
        for what, t in (("caption", text), ("title", row["title"])):
            if t:
                for lv, msg in free_text_problems(t, camp, confirmed, points, te_line, claims_only=True,
                                                  lines=script_texts):
                    bad(lv, f"{what}: {msg}")
        for sentence, _ in find_phrases(everything, ENGAGEMENT_BAIT):
            bad("error", f"\"{sentence}\" asks for or arranges engagement; that is against platform rules and a ban on "
                "the marketplaces")
        for sentence, _ in find_phrases(everything, ENGAGEMENT_SOFT):
            bad("warning", f"\"{sentence}\" reads like asking viewers to swap follows or likes; take it out")
        for sentence, _ in hide_ad_hits(everything):
            bad("error", f"\"{sentence}\" plays down that the video is paid; take it out")
        for k, e in ledger["posts"].items():
            if e.get("job_post") == pid and e.get("campaign") == camp.get("id") and e.get("account") == acc["name"]:
                row["posted"] = dict(e, key=k)
        rows.append(row)

    # across posts
    ready = [r for r in rows if r.get("sha256")]
    for i, a in enumerate(ready):
        for b in ready[i + 1:]:
            pair = f"posts {a['id']} and {b['id']}"
            same = a["sha256"] == b["sha256"] or bool(set(a.get("takes") or []) & set(b.get("takes") or []))
            if same and a["platform"] == b["platform"]:
                ck.add("error", pair, f"{a['name']} and {b['name']} are both {a['label']} and get the same video (or a "
                       "re-cut of the same take). Two copies on one platform is duplicate content: film a new take for "
                       "the second account")
    # fingerprints: a re-export, a new container or a resize has new bytes but the same sound and frames
    for r in ready:
        r["fps"] = [fp for fp in [media_fp(r["full"], r["sha256"])] + [media_fp(f_) for f_ in r.get("take_files") or []]
                    if fp]
    for i, a in enumerate(ready):
        for b in ready[i + 1:]:
            if a["platform"] != b["platform"] or a["sha256"] == b["sha256"] or set(a.get("takes") or []) & \
                    set(b.get("takes") or []):
                continue
            if any(fp_same(x, y) for x in a["fps"] for y in b["fps"]):
                ck.add("error", f"posts {a['id']} and {b['id']}", f"{a['name']} and {b['name']} are both {a['label']}, "
                       "and their videos are the same recording (a re-export or a copy in another format). Film a new "
                       "take for the second account")
    small = [r for r in ready if r["info"]["width"] < 1080 and not r["posted"]]
    if small and not demo:
        ck.add("warning", "videos", f"{len(small)} video(s) are under 1080x1920: fine for a draft; for real posts edit "
               "them again without --width")
    for r in ready:
        for k, e in ledger["posts"].items():
            if r["posted"] and r["posted"]["key"] == k:
                continue
            same_file = e.get("sha256") == r["sha256"]
            same_take = bool(set(e.get("takes") or []) & set(r.get("takes") or []))
            same_rec = not (same_file or same_take) and any(
                fp_same(x, y) for x in r.get("fps") or [] for y in (e.get("fps") or []) if isinstance(y, dict))
            if not (same_file or same_take or same_rec):
                continue
            what = "this exact video" if same_file else "a video cut from the same take" if same_take else \
                "a re-export or copy of a video (or take) that"
            if e.get("campaign") != camp.get("id"):
                ck.add("error", f"post {r['id']}", f"{what} was already posted for campaign {e.get('campaign')} "
                       f"({e.get('account')}). A take goes into one campaign only: film a new one")
            elif e.get("platform") == r["platform"] or (not e.get("platform") and e.get("account") == r["name"]):
                ck.add("error", f"post {r['id']}", f"{what} is already posted on {e.get('account')} ({r['label']}). One "
                       "platform gets it once")
    # how many the brief takes
    mx = camp.get("max_submissions")
    if is_num(mx, 1):
        done = {k for k, e in ledger["posts"].items() if e.get("campaign") == camp.get("id")}
        new = [r for r in rows if not r["posted"]]
        if len(done) + len(new) > mx:
            ck.add("error", "campaign", f"the brief takes {int(mx)} submission{'' if int(mx) == 1 else 's'} per creator; {len(done)} already posted "
                   f"and {len(new)} planned. Leave {len(done) + len(new) - int(mx)} out")
    # the budget
    left = camp.get("budget_remaining")
    if is_num(left, 0):
        cur = camp.get("currency", "USD")
        capv = camp.get("cap_per_video")
        if left <= 0:
            ck.add("error", "campaign", "the remaining budget is 0: views no longer pay. Check the campaign page")
        elif is_num(capv, 0) and capv and left < 10 * capv:
            ck.add("warning", "campaign", f"only {money(left, cur)} of the budget is left (under 10 videos at the "
                   f"{money(capv, cur)} cap); check it again right before posting")
        when = parse_time(camp.get("budget_checked_at"))
        if when and (now_utc() - when).total_seconds() > 24 * 3600:
            ck.add("warning", "campaign", f"the remaining budget was read {(now_utc() - when).days} day(s) ago. Read it "
                   "again on the campaign page and update budget_remaining")
    return {"job": job, "job_dir": job_dir, "job_path": job_path, "campaign": camp, "camp_info": info, "script": sm,
            "accounts": accounts, "rows": rows, "checks": ck.items, "ledger": ledger, "ledger_path": lpath,
            "disclosure": disclosure, "deliver": deliver, "demo": demo}


def summary(model):
    out = []
    for r in model["rows"]:
        head = f"{r['id']} ({r['name']}{' ' + r['handle'] if r['handle'] else ''}, {r.get('file', 'no file')}"
        if r.get("info"):
            head += f", {r['info']['duration']:.1f} s"
        head += ")"
        lv = [x for x, _ in r["issues"]]
        state = "already posted" if r["posted"] else ("BLOCKED" if "error" in lv else "ok")
        out.append(f"{head}: {state}")
        for x, m in r["issues"]:
            out.append(f"  {x}: {m}")
    shown = {(x, m) for r in model["rows"] for x, m in r["issues"]}
    for x, w, m in model["checks"]:
        if (x, m) not in shown:
            out.append(f"{x}: {w}: {m}")
    return out


def main():
    ap = argparse.ArgumentParser(description="Check every video against the brief, the script and the platforms.")
    ap.add_argument("job")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--report", help="also write the report to this file (markdown)")
    ap.add_argument("--ledger", help="the ledger file (default: UGC_CREATOR_LEDGER, else ~/.ugc-creator/ledger.json)")
    a = ap.parse_args()
    model = check_job(a.job, a.ledger)
    errs = [i for i in model["checks"] if i[0] == "error"]
    warns = [i for i in model["checks"] if i[0] == "warning"]
    if a.json:
        print(json.dumps({"errors": len(errs), "warnings": len(warns),
                          "checks": [{"level": x, "where": w, "message": m} for x, w, m in model["checks"]],
                          "posts": [{"id": r["id"], "account": r["name"], "file": r.get("file"),
                                     "sha256": r.get("sha256"), "issues": [m for _, m in r["issues"]]}
                                    for r in model["rows"]]}, indent=1, ensure_ascii=False))
    else:
        lines = summary(model)
        lines += ["", f"{len(errs)} error(s), {len(warns)} warning(s)"]
        print("\n".join(lines))
        if a.report:
            from ugclib import write_text
            c = model["campaign"]
            body = [f"# Checks: {c.get('name')}", "", f"Campaign `{c.get('id')}`, script version "
                    f"`{model['script']['version']}`.", ""]
            if model["demo"]:
                body += ["**EXAMPLE ONLY: a made-up demo campaign; nothing here is a real ad.**", ""]
            body += ["```"] + lines + ["```", ""]
            write_text(a.report, "\n".join(body))
        if errs:
            print("fix every error, then run this again. Nothing can be posted while one is left")
        else:
            print(f"next: python3 {os.path.join('scripts', 'plan.py')} {rel(a.job)}  (the plan page for the user's yes)")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    guard(main)
