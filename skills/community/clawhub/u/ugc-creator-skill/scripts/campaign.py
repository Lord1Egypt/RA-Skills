#!/usr/bin/env python3
"""Turn a paid UGC campaign brief into a checked campaign file, a numbered checklist and a go or no-go.

    python3 scripts/campaign.py campaign.json                    # check, print, write checklist.md
    python3 scripts/campaign.py campaign.json --brief brief.txt  # also scan this brief text

campaign.json is written by the agent from the brief the user pasted (every field is in
references/campaign-file.md). This script checks each field, prints the checklist the creator
confirms before writing a script, and ends with one verdict:

  GO         nothing stands in the way (conditions, if any, are listed)
  NO-GO      something must change first: an error in the file, a brief that asks to hide the ad
             and no written word from the brand that a disclosed video is fine, a make-money
             campaign without a true line on typical earnings, a deadline that passed, no budget left
  REFUSED    the skill doesn't do this campaign at all: the creator would pose as an ordinary
             customer or post from an account the brand owns or runs as a made-up person, the brief
             asks for a testimonial about use that didn't happen, or it wants an AI presenter or a
             cloned voice instead of the creator

The brief text (the "brief_file" in campaign.json, or --brief) is read for those sentences, for
sentences that forbid the disclosure on the video, for bought engagement, for topics TikTok bans or
restricts in branded content, and for rules that live only in an outside document.

"mode": "deliver_files" is for creators paid per video who hand the files to the brand: no posting,
an export with a compliance sheet instead.

Exit code 0 for GO, 1 for NO-GO or REFUSED.
"""
import argparse, hashlib, os, re, sys

sys.dont_write_bytecode = True   # nothing is ever written into the skill's own folder
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ugclib import (AI_PRESENTER, DISCLOSURE_CONFLICT, ENGAGEMENT_BAIT, ENGAGEMENT_SOFT, FAKE_TESTIMONIAL,  # noqa: E402
                    LIMITS, LOCATION_TRICKS, MAKE_MONEY, PERSONA, PLATFORMS, PROHIBITED_TOPICS, RESTRICTED_TOPICS,
                    asks_for, die, find_phrases, guard, hashtags, hide_ad_hits, is_num, mentions, money, now_utc,
                    parse_time, payout, place_name, read_json, read_yourself, reading, rel, says_paid, terms,
                    threshold_views, valid_id, with_defaults, write_text)
from ugclib import BANS_IT, GET_RICH_QUICK, load_zone, tone_hits  # noqa: E402
from ugclib import (BRAND_ACCOUNT, DICTATED, DISCLOSURE_OPTIONAL, DISCLOSURE_PLACEMENT, DISCLOSURE_TIMING,  # noqa: E402
                    DISCOVERY, NO_BURNED_TEXT, PERMISSIVE, TTS_VOICE)

FORMATS = ("talking_head", "split_screen", "face_screen", "broll_voiceover")

FORMAT_WORDS = {"talking_head": "talking head (you on camera)",
                "split_screen": "split screen (the brand's footage and your recording, one above the other)",
                "face_screen": "face plus screen recording",
                "broll_voiceover": "hands and b-roll with your own voiceover"}
EFFORT = {"talking_head": "low: one selfie take plus hook takes",
          "split_screen": "low: one selfie take under the supplied footage",
          "face_screen": "medium: a selfie take and a screen recording that match",
          "broll_voiceover": "medium: several b-roll shots and a voiceover"}
CAPTION_DISCLOSURES = ("#ad", "#advert", "#advertisement", "#sponsored", "#paidpartnership", "#anzeige",
                       "#werbung", "#reclame", "#publicidad", "#pub", "ad", "paid partnership")
WEAK_TAGS = ("#sp", "#spon", "#collab", "#partner", "#gifted", "#thanks")
MUSIC = ("none", "licensed_only", "brief_supplied", "any_licensed")
DEMO_LINE = "example only"
OUTSIDE_DOC = [r"\b(?:full|more|all|detailed|complete)\s+(?:requirements|rules|guidelines|brief|instructions)\s+(?:are\s+)?"
               r"(?:in|on|at)\s+(?:the|our|this)?\s*(?:doc|document|notion|google doc|pdf|link|drive|deck)",
               r"\b(?:see|read|check)\s+(?:the|our)\s+(?:doc|document|notion|google doc|pdf|drive|deck)\b",
               r"\bdocs\.google\.com|notion\.(?:so|site)|drive\.google\.com"]


def example_demo(c):
    """The skill's own made-up example (id "example-...", brand "Example ...", "example_demo": true):
    its videos show the real corner "Ad" label with an "EXAMPLE: not a real ad" label opposite it, and
    a labelled placeholder where the creator's recording goes. Nothing else can use it."""
    return (isinstance(c, dict) and c.get("example_demo") is True and str(c.get("id") or "").startswith("example-")
            and str(c.get("brand") or "").startswith("Example "))


def screen_line_ok(text, c):
    # the skill's example shows the real "Ad" pill; make_video.py adds its "EXAMPLE: not a real ad" pill
    if example_demo(c) and " ".join(str(text or "").split()).lower().startswith(DEMO_LINE):
        return True
    return says_paid(text, label=True)


BURNED = ("any", "disclosure_only", "none")


def burned_text(c):
    """What may be burned into the video: "any" (captions, hook text, the "Ad" label), "disclosure_only" (the
    label alone) or "none" (clean footage: the disclosure is said, first in the caption and the platform's label)."""
    v = c.get("burned_text") if isinstance(c, dict) else None
    return v if v in BURNED else "any"


def deliver(c):
    return isinstance(c, dict) and c.get("mode") == "deliver_files"


def talking_points(c):
    """[(id, text)] from "talking_points": a list of {"id", "text"} or of plain strings (tp1, tp2, ...)."""
    tps = c.get("talking_points") if isinstance(c, dict) else None
    out = []
    if isinstance(tps, list):
        for i, t in enumerate(tps, 1):
            if isinstance(t, str) and t.strip():
                out.append((f"tp{i}", t.strip()))
            elif isinstance(t, dict) and isinstance(t.get("text"), str) and t["text"].strip():
                out.append((str(t.get("id") or f"tp{i}"), t["text"].strip()))
    return out


def formats_of(c):
    f = c.get("formats") if isinstance(c, dict) else None
    if isinstance(f, str):
        f = [f]
    return [x for x in f if isinstance(x, str)] if isinstance(f, list) else []


def _num(v, minimum=0.0):
    return is_num(v, minimum)


def check_campaign(c, path="campaign.json", base_dir="."):
    """Every problem with a campaign file: a list of (level, field, message)."""
    out = []

    def bad(field, msg, level="error"):
        out.append((level, field, msg))

    if not isinstance(c, dict):
        return [("error", "campaign", f"{path} must hold one JSON object with the campaign's rules")]
    files_only = deliver(c)
    if c.get("example_demo") is not None and not example_demo(c):
        bad("example_demo", "only the skill's own made-up example uses this (id \"example-...\", brand \"Example ...\"). "
            "Take it out: a real campaign's videos carry a real disclosure")
    if c.get("mode") is not None and c.get("mode") not in ("post", "deliver_files"):
        bad("mode", "\"post\" (you post on your own accounts, paid per view) or \"deliver_files\" (paid per video, the "
            "brand gets the files)")
    if not valid_id(c.get("id")):
        bad("id", "a short id of lowercase letters, digits and dashes (like \"orbit-app-nov\"): the ledger files every "
            "post under it")
    for k, what in (("name", "the campaign's name as the marketplace shows it"),
                    ("brand", "the brand that pays (it goes into the spoken and on-screen disclosure)")):
        if not isinstance(c.get(k), str) or not c[k].strip():
            bad(k, what)
    if c.get("accounts_owned_by") not in (None, "creator", "brand"):
        bad("accounts_owned_by", "\"creator\" (your own accounts) or \"brand\" (accounts the brand owns or creates)")
    plats = c.get("platforms")
    if files_only:
        if c.get("pay_per_video") is not None and not _num(c.get("pay_per_video")):
            bad("pay_per_video", "the flat fee per delivered video, a number, or null")
    elif not isinstance(plats, dict) or not plats:
        bad("platforms", "the platforms the campaign pays for, each with its rate per 1,000 views, like "
            "{\"TIKTOK\": {\"rate_per_1k\": 2.0}}")
    else:
        for p, v in plats.items():
            if p not in PLATFORMS:
                bad("platforms", f"{p}: this skill posts to {', '.join(PLATFORMS)}. Leave {p} out")
            elif not isinstance(v, dict) or not _num(v.get("rate_per_1k")):
                bad("platforms", f"{p}: rate_per_1k must be a number (dollars per 1,000 views, 0 or more)")
            else:
                for k in ("min_payout", "cap_per_video", "min_views"):
                    if v.get(k) is not None and not _num(v.get(k)):
                        bad("platforms", f"{p}: {k} must be a number of 0 or more, or left out to use the campaign's")
                if v.get("cap_per_video") == 0:
                    bad("platforms", f"{p}: cap_per_video 0 would pay nothing; leave it out when there is no cap")
    for k in ("min_payout", "cap_per_video", "budget_total", "budget_remaining", "min_views"):
        if c.get(k) is not None and not _num(c.get(k)):
            bad(k, "must be a number of 0 or more, or null")
    if c.get("cap_per_video") == 0:
        bad("cap_per_video", "0 would pay nothing. When the brief sets no cap, leave it null")
    if _num(c.get("min_payout")) and _num(c.get("cap_per_video")) and c.get("cap_per_video") and \
            c["min_payout"] > c["cap_per_video"]:
        bad("cap_per_video", "the cap per video is lower than the minimum payout; check both numbers in the brief")
    if c.get("budget_checked_at") is not None and not parse_time(c.get("budget_checked_at")):
        bad("budget_checked_at", "when the remaining budget was read on the campaign page, like 2026-11-18T14:00:00Z")
    if c.get("fee_pct") is not None and not (_num(c.get("fee_pct")) and c["fee_pct"] < 100):
        bad("fee_pct", "the marketplace fee in percent (0 to 99), or null for the default of 10")
    for k in ("window_days", "days_live", "submit_within_minutes", "max_submissions"):
        if c.get(k) is not None and not (_num(c.get(k), 1) and float(c[k]).is_integer()):
            bad(k, "a whole number, or null")
    if c.get("deadline") is not None and not parse_time(c.get("deadline")):
        bad("deadline", "the last day to post or submit, like 2026-12-01 or 2026-12-01T23:59:00Z, or null")
    geo = c.get("geo")
    if geo is not None and (not isinstance(geo, dict) or not isinstance(geo.get("countries"), list)
                            or not geo["countries"] or not all(isinstance(x, str) for x in geo["countries"])
                            or (geo.get("min_share") is not None and not (_num(geo.get("min_share")) and geo["min_share"] <= 1))):
        bad("geo", "{\"countries\": [\"US\", \"UK\"], \"min_share\": 0.4} when the brief sets where viewers must be, or null")
    if c.get("language") is not None and not (isinstance(c.get("language"), str) and c["language"].strip()):
        bad("language", "the language the video must be in, like \"en\", or null")

    fm = formats_of(c)
    if not fm or any(f not in FORMATS for f in fm):
        bad("formats", f"the formats the brief accepts, a list of: {', '.join(FORMATS)}")
    if c.get("face") not in (None, "required", "either", "none"):
        bad("face", "\"required\" (your face on camera), \"either\" or \"none\" (faceless)")
    if c.get("face") == "none" and any(f in ("talking_head", "split_screen", "face_screen") for f in fm):
        bad("face", "the brief says faceless, but a listed format shows your face. Use broll_voiceover, or check the brief",
            "warning")
    sf = c.get("supplied_footage")
    if sf is not None:
        if not isinstance(sf, dict) or not isinstance(sf.get("files"), list) or not all(isinstance(x, str) and x.strip()
                                                                                      for x in sf["files"]):
            bad("supplied_footage", "{\"files\": [\"<file the brand supplied>\"], \"position\": \"top\"} or null")
        elif sf.get("position") not in (None, "top", "bottom"):
            bad("supplied_footage", "position is \"top\" (the brand's footage above you) or \"bottom\"")
    if "split_screen" in fm and not (isinstance(sf, dict) and sf.get("files")):
        bad("supplied_footage", "a split screen needs the footage the brand supplied: {\"files\": [...], \"position\": "
            "\"top\"}")
    tps = talking_points(c)
    if not tps:
        bad("talking_points", "the brief's talking points, a list of {\"id\": \"tp1\", \"text\": \"...\"}: every brand "
            "claim in the script must trace to one")
    if len({i for i, _ in tps}) != len(tps):
        bad("talking_points", "two talking points share an id")
    for k in ("do_not_say", "proof"):
        v = c.get(k)
        if v is not None and (not isinstance(v, list) or not all(isinstance(x, str) and x.strip() for x in v)):
            bad(k, "a list of short texts (an empty list when the brief names none)")
    if c.get("cta") is not None and not (isinstance(c["cta"], str) and c["cta"].strip()):
        bad("cta", "the call to action the brief requires, word for word, or null")
    if c.get("cta_in") not in (None, "spoken", "caption", "both"):
        bad("cta_in", "where the call to action goes: \"spoken\", \"caption\" or \"both\"")
    if c.get("music") not in (None,) + MUSIC:
        bad("music", f"which music the brief allows: {', '.join(MUSIC)}")
    for k in ("pre_approval", "dedicated_account", "make_money"):
        if c.get(k) is not None and not isinstance(c[k], bool):
            bad(k, "true or false")
    te = c.get("typical_earnings")
    if te is not None and (not isinstance(te, dict) or not isinstance(te.get("line"), str) or not te["line"].strip()
                           or not isinstance(te.get("source"), str) or not te["source"].strip()):
        bad("typical_earnings", "{\"line\": \"<what most people earn, said plainly>\", \"source\": \"<where that number "
            "comes from>\"}")

    cap = c.get("caption")
    if not isinstance(cap, dict):
        if not files_only:
            bad("caption", "what every caption must hold: {\"disclosure\": \"#ad\", \"hashtags\": [...], \"mentions\": "
                "[...], \"links\": [...]}")
        cap = {}
    disc = cap.get("disclosure")
    if not files_only:
        if not isinstance(disc, str) or not disc.strip():
            bad("caption.disclosure", "every campaign caption starts with a disclosure. Use \"#ad\" unless the brief names "
                "a stronger one")
        elif disc.strip().lower() in WEAK_TAGS:
            bad("caption.disclosure", f"{disc} doesn't tell viewers the post is paid. Use \"#ad\"")
        elif disc.strip().lower() not in CAPTION_DISCLOSURES and not says_paid(disc, label=True):
            bad("caption.disclosure", f"\"{disc}\" doesn't say the post is paid. Use \"#ad\"")
    for k, check, what in (("hashtags", hashtags, "a hashtag like #exampleorbit"),
                           ("mentions", mentions, "a handle like @example.orbit")):
        v = cap.get(k, [])
        if v is not None and (not isinstance(v, list) or not all(isinstance(x, str) and check(x) == [x] for x in v)):
            bad(f"caption.{k}", f"a list where each item is {what} (an empty list when the brief asks for none)")
    lk = cap.get("links", [])
    if lk is not None and (not isinstance(lk, list) or not all(isinstance(x, str) and x.strip() for x in lk)):
        bad("caption.links", "a list of links the caption must hold (an empty list when the brief asks for none)")
    if c.get("links_where") not in (None, "caption", "bio", "either"):
        bad("links_where", "\"caption\", \"bio\" or \"either\", or null (caption)")
    if any(isinstance(h, str) and h.lower() in ("#ad", "#ads", "#sponsored", "ad", "sponsored")
           for h in (c.get("do_not_say") if isinstance(c.get("do_not_say"), list) else [])):
        bad("do_not_say", "the brief bans the disclosure word. It is never dropped: every campaign video says it is paid")

    d = c.get("disclosure")
    if not isinstance(d, dict):
        if not files_only:
            bad("disclosure", "{\"spoken_within_s\": 10, \"on_screen\": \"Ad\", \"on_screen_seconds\": 3, "
                "\"caption_position\": \"first\"}")
        d = {}
    if not files_only:
        if not _num(d.get("spoken_within_s"), 1) or d["spoken_within_s"] > 30:
            bad("disclosure.spoken_within_s", "by which second the spoken disclosure must be said (1 to 30; 10 when the "
                "brief says nothing)")
        sd = d.get("on_screen")
        if c.get("burned_text") is not None and c.get("burned_text") not in BURNED:
            bad("burned_text", "\"any\" (captions, hook text and the on-screen label), \"disclosure_only\" (the label "
                "alone) or \"none\" (clean footage, nothing burned in), as the brief allows")
        if "not_in_hook" in d and not isinstance(d.get("not_in_hook"), bool):
            bad("disclosure.not_in_hook", "true when the brief says not to say it's an ad in the hook")
        if d.get("not_before_s") is not None and (not _num(d.get("not_before_s"), 0) or (
                _num(d.get("spoken_within_s"), 1) and d["not_before_s"] >= d["spoken_within_s"])):
            bad("disclosure.not_before_s", "the second before which the brief doesn't want the disclosure said, smaller "
                "than spoken_within_s")
        if burned_text(c) == "none" and not (isinstance(sd, str) and sd.strip()):
            pass   # clean footage: no label on the video
        elif not isinstance(sd, str) or not sd.strip():
            bad("disclosure.on_screen", "the text shown at the start, like \"Ad\" or \"Paid partnership with "
                f"{c.get('brand') or '<brand>'}\"")
        elif not screen_line_ok(sd, c):
            bad("disclosure.on_screen", f"\"{sd}\" doesn't say the video is paid. Use \"Ad\"")
        elif len(sd) > 48:
            bad("disclosure.on_screen", "48 characters at most, so it reads in the first seconds")
        secs = d.get("on_screen_seconds", 3)
        if not _num(secs, 2) or secs > 10:
            bad("disclosure.on_screen_seconds", "how long it shows from the first frame: 2 to 10 seconds")
        if d.get("caption_position") not in (None, "first", "first_line"):
            bad("disclosure.caption_position", "\"first\" (the caption starts with it) or \"first_line\"")
    ln = c.get("length")
    if not isinstance(ln, dict) or not _num(ln.get("min_s")) or not _num(ln.get("max_s")) or ln["max_s"] <= ln["min_s"]:
        bad("length", "{\"min_s\": 15, \"max_s\": 60}: the shortest and longest video the campaign accepts")
    if isinstance(plats, dict) and not files_only:
        for p, v in plats.items():
            if p in LIMITS and isinstance(v, dict):
                _rate, mn, cap, _mv = terms(c, p)
                if cap is not None and mn and cap < mn:
                    bad("platforms", f"{p}: the cap per video ({cap:g}) is under the minimum payout ({mn:g}), so a "
                        "video there would never pay. Check both numbers in the brief")
    if c.get("deadline_tz") is not None and not (isinstance(c.get("deadline_tz"), str) and load_zone(c["deadline_tz"])):
        bad("deadline_tz", "the time zone the brief's deadline day is in, like \"America/New_York\" (default UTC)")
    pos = c.get("product_on_screen_by_s")
    if pos is not None and not (_num(pos) and pos <= 60):
        bad("product_on_screen_by_s", "the second by which the product must be on screen (0 to 60), or null")
    tpl = c.get("talking_points")
    if isinstance(tpl, list) and any(isinstance(t, dict) and t.get("required") not in (None, True, False) for t in tpl):
        bad("talking_points", "\"required\" is true (the brief says every video must mention it) or false")
    el = c.get("eligibility")
    if el is not None:
        ok = isinstance(el, dict) and all(el.get(k) is None or _num(el.get(k)) for k in ("min_followers",
                                                                                          "min_account_age_days"))
        ok = ok and (el.get("countries") is None or (isinstance(el["countries"], list)
                                                     and all(isinstance(x, str) for x in el["countries"])))
        ok = ok and el.get("account_type") in (None, "any", "business_or_creator", "creator", "business")
        ok = ok and el.get("public") in (None, True, False)
        if not ok:
            bad("eligibility", "{\"min_followers\": 1000, \"min_account_age_days\": 30, \"countries\": [\"US\"], "
                "\"account_type\": \"business_or_creator\", \"public\": true} with what the brief asks of each account")
    for k, what in (("usage_rights", "what the brand may do with the video, in the brief's words, or null"),
                    ("ad_code", "the ad code the brief asks for (like \"TikTok Spark Ads code within 7 days\"), or null")):
        if c.get(k) is not None and not (isinstance(c[k], str) and c[k].strip()):
            bad(k, what)
    for k in ("reference_videos", "doc_only_rules"):
        v = c.get(k)
        if v is not None and (not isinstance(v, list) or not all(isinstance(x, str) and x.strip() for x in v)):
            bad(k, "a list of short texts, or null")
    cr = c.get("creator")
    if cr is not None and not (isinstance(cr, dict) and all(cr.get(k) is None or _num(cr.get(k)) for k in
                                                             ("hourly_floor", "hours_per_video"))):
        bad("creator", "{\"hourly_floor\": 25, \"hours_per_video\": 1.5}: what an hour of your time must earn, and "
            "how long one video takes you")
    st = c.get("campaign_stats")
    if st is not None and not (isinstance(st, dict) and all(st.get(k) is None or _num(st.get(k)) for k in
                                                            ("approved_videos", "total_views"))):
        bad("campaign_stats", "{\"approved_videos\": 120, \"total_views\": 900000, \"checked_at\": \"...\"} from "
            "the campaign page, or null")
    tr = c.get("topic_reviewed")
    if tr is not None and (not isinstance(tr, dict) or not all(isinstance(v, str) and v.strip() for v in tr.values())):
        bad("topic_reviewed", "{\"<topic>\": \"why it doesn't apply to this product\"} for a topic flag that is wrong")
    return out


def brief_flags(c, base_dir, brief_path=None):
    """Everything the brief text says that the skill refuses, never follows, or wants read twice."""
    path = brief_path or (c.get("brief_file") if isinstance(c, dict) else None)
    empty = {"text": None, "path": None, "persona": [], "fake": [], "ai": [], "hide": [], "conflict": [], "bait": [],
             "read": [], "money": [], "prohibited": [], "restricted": [], "outside": [], "tone": [], "grq": [],
             "brand_account": [], "ai_allowed": [], "tts": [], "tts_allowed": [], "timing": [], "optional": [],
             "placement": [], "no_text": [], "dictated": []}
    if not isinstance(path, str) or not path:
        return empty
    full = path if os.path.isabs(path) or brief_path else os.path.join(base_dir, path)
    reading(full)
    try:
        with open(full, encoding="utf-8-sig", errors="replace") as fh:
            text = fh.read()
    except FileNotFoundError:
        die(f"{path} not found (the campaign brief text)")
    except IsADirectoryError:
        die(f"{path} is a folder; give the brief as a text file")
    reading(None)
    # where and when the disclosure goes, and briefs that call it optional: GO with a note, never hiding
    timing = find_phrases(text, DISCLOSURE_TIMING)
    placement = [(s, m) for s, m in find_phrases(text, DISCLOSURE_PLACEMENT) if s not in {x for x, _ in timing}]
    optional = [(s, m) for s, m in find_phrases(text, DISCLOSURE_OPTIONAL)
                if s not in {x for x, _ in timing + placement}]
    no_text = find_phrases(text, NO_BURNED_TEXT) + find_phrases(text, DISCLOSURE_CONFLICT)
    no_text = [h for i, h in enumerate(no_text) if h[0] not in {x for x, _ in no_text[:i]}]
    soft = {s for s, _ in timing + placement + optional + no_text}
    hide = hide_ad_hits(text, brief=True, skip=soft)
    persona = find_phrases(text, PERSONA)
    brand_account = find_phrases(text, BRAND_ACCOUNT)
    fake = find_phrases(text, FAKE_TESTIMONIAL)
    in_fake = {s for s, _ in fake + persona}
    dictated = [(s, m) for s, m in find_phrases(text, DISCOVERY + DICTATED) if s not in in_fake]
    ai_all = find_phrases(text, AI_PRESENTER)
    ai = [(s, m) for s, m in ai_all if not re.search(PERMISSIVE, s, re.I) and not re.search(BANS_IT, s, re.I)]
    ai_allowed = [(s, m) for s, m in ai_all if re.search(PERMISSIVE, s, re.I)]
    tts_all = find_phrases(text, TTS_VOICE)
    tts = [(s, m) for s, m in tts_all if not re.search(PERMISSIVE, s, re.I)]
    tts_allowed = [(s, m) for s, m in tts_all if re.search(PERMISSIVE, s, re.I)]
    bait = asks_for(text, ENGAGEMENT_BAIT + ENGAGEMENT_SOFT + LOCATION_TRICKS)
    taken = {s for s, _ in hide + bait + persona + fake + brand_account} | soft
    tone = tone_hits(text, brief=True, skip=taken)
    taken |= {s for s, _ in tone + dictated}
    read = read_yourself(text, taken)
    money_hits = find_phrases(text, MAKE_MONEY)
    grq = find_phrases(text, GET_RICH_QUICK)
    reviewed = {k.lower() for k in (c.get("topic_reviewed") or {})} if isinstance(c.get("topic_reviewed"), dict) else set()
    prohibited = [(t, s) for t, pat in PROHIBITED_TOPICS.items() if t.lower() not in reviewed
                  for s, _ in find_phrases(text, [pat])[:1]]
    restricted = [(t, s) for t, pat in RESTRICTED_TOPICS.items() if t.lower() not in reviewed
                  for s, _ in find_phrases(text, [pat])[:1]]
    outside = find_phrases(text, OUTSIDE_DOC)
    return {"text": text, "path": full, "persona": persona, "fake": fake, "ai": ai, "hide": hide, "conflict": [],
            "bait": bait, "read": read, "money": money_hits, "prohibited": prohibited, "restricted": restricted,
            "outside": outside, "tone": tone, "grq": grq, "brand_account": brand_account, "ai_allowed": ai_allowed,
            "tts": tts, "tts_allowed": tts_allowed, "timing": timing, "optional": optional, "placement": placement,
            "no_text": no_text, "dictated": dictated}


def deadline_end(value, zone=None):
    """The moment the deadline ends (UTC). A date alone counts to the end of that day in the
    campaign's "deadline_tz" (UTC when none is given)."""
    import datetime
    t = parse_time(value)
    if not t:
        return None
    if isinstance(value, str) and re.fullmatch(r"\s*\d{4}-\d{2}-\d{2}\s*", value):
        z = load_zone(zone) if zone else None
        day = datetime.date.fromisoformat(value.strip())
        end = datetime.datetime(day.year, day.month, day.day, 23, 59, 59, tzinfo=z or datetime.timezone.utc)
        t = end.astimezone(datetime.timezone.utc)
    return t


def deadline_passed(value, now=None, zone=None):
    """True when the deadline is behind us."""
    t = deadline_end(value, zone)
    return bool(t) and (now or now_utc()) > t


def verdict(raw, c, issues, flags):
    """("GO" | "NO-GO" | "REFUSED", [reasons], [conditions], tiktok_blocked)."""
    refused, nogo, cond = [], [], []
    if flags.get("brand_account") or (isinstance(raw, dict) and raw.get("accounts_owned_by") == "brand"):
        refused.append("the videos would go out from an account the brand owns or runs as a made-up person; viewers "
                       "couldn't tell a paid creator is talking")
    if flags["fake"]:
        refused.append("the brief asks for a testimonial about use or results that didn't happen (FTC: you can't talk "
                       "about an experience you didn't have)")
    if flags["ai"]:
        refused.append("the brief requires an AI presenter, avatar or cloned voice; this skill only edits what a real "
                       "creator films")
    if flags["persona"]:
        nogo.append("the brief asks you to post as someone you aren't (a happy customer, a regular user). The skill only "
                    "makes videos in your own voice, disclosed. Ask the brand whether that is accepted, or skip this one")
    if flags.get("tts"):
        nogo.append("the brief wants a text-to-speech or AI voice; the skill uses your own voice. Ask the brand whether "
                    "your real voiceover is accepted")
    errs = [i for i in issues if i[0] == "error"]
    if errs:
        nogo.append(f"{len(errs)} thing(s) to fix in campaign.json")
    if isinstance(c, dict) and not deliver(c):
        if flags["hide"] and not (isinstance(raw.get("disclosure_ok_in_writing"), str)
                                  and raw["disclosure_ok_in_writing"].strip()):
            nogo.append("the brief asks to hide or leave out the ad disclosure. The skill only makes disclosed videos; "
                        "ask the brand in writing whether a disclosed video is accepted, then tell me who confirmed it "
                        "and where, and I'll note it (\"disclosure_ok_in_writing\")")
        elif flags["hide"]:
            cond.append(f"disclosed anyway: the brand confirmed in writing ({raw['disclosure_ok_in_writing']})")
        if flags.get("tone"):
            cond.append("tone notes (\"keep it natural\", \"a regular post, not an ad\") are followed as style: a relaxed, "
                        "unscripted read. The disclosure stays in every video")
        dd = c.get("disclosure") or {}
        if flags.get("timing"):
            set_ = dd.get("not_in_hook") is True or is_num(dd.get("not_before_s"))
            cond.append("the brief says when to disclose (not in the hook, or not in the first seconds): fine, the "
                        "disclosure still ends inside the window" + ("" if set_ else
                        ". Set \"not_in_hook\" or \"not_before_s\" under \"disclosure\" in campaign.json so the checks "
                        "follow it"))
        if flags.get("optional"):
            cond.append("warning: the brief calls the disclosure optional (or says no disclaimers). Every video "
                        "discloses anyway, as the law requires: said out loud, first in the caption and the platform's "
                        "paid-partnership setting")
        if flags.get("placement"):
            cond.append("warning: the brief puts the disclosure in a comment or the caption only. A comment doesn't "
                        "count as a disclosure, and the marketplace wants #ad first in the caption; the skill keeps #ad "
                        "first in the caption and says it out loud. Check with the brand that this is accepted")
        if flags.get("no_text"):
            cond.append("the brief wants no text on the video: " + (
                "\"burned_text\" is \"" + burned_text(c) + "\", so " if burned_text(c) != "any" else
                "set \"burned_text\" to \"none\" (or \"disclosure_only\" if the brief allows a small \"Ad\" label) "
                "in campaign.json; then ") + "captions and the hook text stay off the video, and the disclosure is said "
                "out loud, first in the caption and the platform's paid-partnership setting")
        if flags.get("dictated"):
            cond.append("only if true for you: the brief asks you to say how you found it, use it or what it did for "
                        "you. Each one is on the checklist as a question; a no means a reworded line or asking the brand")
        left = c.get("budget_remaining")
        if is_num(left) and left <= 0:
            nogo.append("the remaining budget is 0: views no longer pay")
    if flags.get("ai_allowed"):
        cond.append("the brief allows AI presenters; you film yourself, and the skill never uses one")
    if flags.get("tts_allowed"):
        cond.append("the brief allows a text-to-speech voice; the skill uses your own voice, which the brief also takes")
    money_campaign = (isinstance(raw, dict) and raw.get("make_money") is True) or bool(flags["money"])
    te_ok = isinstance(raw, dict) and isinstance(raw.get("typical_earnings"), dict) and \
        isinstance(raw["typical_earnings"].get("line"), str) and raw["typical_earnings"]["line"].strip()
    if money_campaign:
        if te_ok:
            cond.append("make-money content: an earnings claim (a money figure, \"I made\", \"you can make\") goes "
                        "only with the typical-earnings line said in the same video, and only your own true numbers. "
                        "No get-rich-quick framing")
        else:
            cond.append("make-money content: no earnings claims at all (no money figure, no \"I made\", no \"you can "
                        "make\"), because the brand gave no typical-earnings line (FTC). Say what the product does. No "
                        "get-rich-quick framing (\"easy money\", \"passive income\", \"20 minutes a day\")")
    if isinstance(raw, dict) and deadline_passed(raw.get("deadline"), zone=raw.get("deadline_tz")):
        nogo.append(f"the deadline ({raw.get('deadline')}) has passed")
    tiktok_blocked = bool(flags["prohibited"]) or bool(flags.get("grq"))
    if flags["prohibited"]:
        cond.append("no TikTok post: TikTok bans branded content about " + ", ".join(t for t, _ in flags["prohibited"])
                    + " (if that word doesn't apply to this product, say why in \"topic_reviewed\")")
    elif flags.get("grq"):
        cond.append("no TikTok post: the brief frames the product as quick or easy money, and TikTok bans get-rich-quick "
                    "branded content. Other platforms only with plain, true wording")
    elif money_campaign:
        cond.append("TikTok allows content about earning money when it is plain and true: TikTok bans get-rich-quick "
                    "branded content, so the checks refuse quick or easy money framing in scripts and captions")
    if flags["restricted"]:
        cond.append("TikTok restricts branded content about " + ", ".join(t for t, _ in flags["restricted"])
                    + " to invited accounts; check yours before posting there")
    if isinstance(raw, dict) and raw.get("language") and str(raw["language"]).lower()[:2] != "en":
        cond.append(f"the claims checks read English only: in {raw['language']}, read every line of the script, the "
                    "captions and the transcript yourself for claims about use, results or money")
    if flags["outside"]:
        cond.append("some rules live in an outside document: paste it, so its rules are checked too (only rules on the "
                    "campaign page can justify a rejection, but follow them anyway)")
    if isinstance(raw, dict):
        if raw.get("pre_approval"):
            cond.append("the brand approves each draft before it is posted, and it must go out from the account approved")
        if raw.get("dedicated_account"):
            cond.append("a dedicated account: post only from an account used for this campaign alone")
        if raw.get("max_submissions"):
            n_ = raw['max_submissions']
            cond.append(f"at most {n_} submission{'' if n_ == 1 else 's'} for this campaign")
    if refused:
        return "REFUSED", refused, cond, tiktok_blocked
    if nogo:
        return "NO-GO", nogo, cond, tiktok_blocked
    return "GO", [], cond, tiktok_blocked


def load(path, brief_path=None):
    """The campaign (optional fields filled in), its problems, the brief's flags, the verdict and a
    version stamp. Used by the other scripts too."""
    raw = read_json(path, "the campaign file")
    base = os.path.dirname(os.path.abspath(path))
    issues = check_campaign(raw, rel(path), base)
    flags = brief_flags(raw, base, brief_path) if isinstance(raw, dict) else brief_flags({}, base)
    if isinstance(raw, dict):
        if flags["text"] is None:
            issues.append(("error", "brief_file", "the brief as pasted, saved as a text file next to campaign.json (like "
                           "\"brief.txt\"), or --brief FILE. Every sentence is read for what the skill refuses or never "
                           "follows; without it nothing is checked"))
        elif len(" ".join(flags["text"].split())) < 80:
            issues.append(("error", "brief_file", f"{rel(flags['path'])} holds only {len(flags['text'].strip())} "
                           "characters. Paste the whole brief from the campaign page, not a summary"))
    with open(path, "rb") as fh:
        h = hashlib.sha256(fh.read())
    if flags["text"] is not None:
        h.update(flags["text"].encode("utf-8", "surrogatepass"))
    c = with_defaults(raw) if isinstance(raw, dict) else raw
    if isinstance(c, dict):
        d = c.get("disclosure") if isinstance(c.get("disclosure"), dict) else {}
        c["disclosure"] = dict(d)
        c["disclosure"].setdefault("spoken_within_s", 10)
        c["disclosure"].setdefault("on_screen_seconds", 3)
        c["disclosure"].setdefault("caption_position", "first")
        c["talking_points_list"] = talking_points(raw)
        c["formats_list"] = formats_of(raw)
    v, reasons, cond, tt_blocked = verdict(raw, c, issues, flags)
    if isinstance(c, dict):
        c["tiktok_blocked"] = bool(tt_blocked)
        c["make_money_campaign"] = (raw.get("make_money") is True) or bool(flags["money"])
    out = dict(flags)
    out.update({"campaign": c, "raw": raw, "issues": issues, "brief": flags["text"], "brief_path": flags["path"],
                "verdict": v, "reasons": reasons, "conditions": cond, "version": h.hexdigest()[:10], "base_dir": base})
    return out


def rate_line(c):
    cur = c.get("currency", "USD")
    out = []
    for p, v in (c.get("platforms") or {}).items():
        if p not in LIMITS or not isinstance(v, dict):
            continue
        rate, mn, cap, mv = terms(c, p)
        bits = f"{LIMITS[p]['label']} {money(rate, cur)} per 1,000 views"
        own = [x for x in (f"minimum {money(mn, cur)}" if v.get("min_payout") is not None else "",
                           f"cap {money(cap, cur)}" if v.get("cap_per_video") is not None and cap else "",
                           f"at least {mv:,} views" if v.get("min_views") is not None else "") if x]
        out.append(bits + (f" ({', '.join(own)})" if own else ""))
    return ", ".join(out)


def checklist(info):
    """The numbered checklist, as lines of Markdown."""
    c = info["campaign"]
    raw = info["raw"]
    cur = c.get("currency", "USD")
    files_only = deliver(c)
    cap, d = c.get("caption") or {}, c.get("disclosure") or {}
    items = []
    if files_only:
        items.append("**Mode:** deliver files only. You film, the skill edits and checks; the brand gets the files and a "
                     "compliance sheet. Nothing is posted." + (f" Pay: {money(c['pay_per_video'], cur)} per video."
                                                               if is_num(c.get("pay_per_video")) else ""))
    else:
        items.append(f"**Platforms and rates:** {rate_line(c) or 'none given'}.")
        pay = [f"minimum payout per video {money(c['min_payout'], cur)}" if c.get("min_payout") else "no minimum payout given",
               f"cap per video {money(c['cap_per_video'], cur)}" if c.get("cap_per_video") else "no cap per video given",
               f"marketplace fee {c['fee_pct']:g}%"]
        if c.get("budget_total"):
            pay.append(f"total budget {money(c['budget_total'], cur)}")
        if c.get("budget_remaining") is not None:
            when = parse_time(c.get("budget_checked_at"))
            pay.append(f"{money(c['budget_remaining'], cur)} left" + (f" when checked {when:%d %b %H:%M} UTC" if when else ""))
        items.append("**Payout:** " + "; ".join(pay) + ". When the budget runs out, views stop paying.")
        need = [f"{LIMITS[p]['label']} {threshold_views(c, p):,}" for p in (c.get("platforms") or {})
                if p in LIMITS and threshold_views(c, p)]
        if need:
            items.append("**Pays from:** " + ", ".join(need) + " views per video; under that a video earns nothing.")
    fm = c.get("formats_list") or []
    items.append("**Format:** " + "; or ".join(FORMAT_WORDS.get(f, f) for f in fm) + ". Effort: "
                 + "; ".join(f"{f.replace('_', ' ')} {EFFORT.get(f, '?')}" for f in fm) + ".")
    face = c.get("face")
    if face:
        items.append("**Face:** " + {"required": "your face on camera is required", "either": "face or faceless, your "
                                     "choice", "none": "faceless only"}[face] + ".")
    sf = c.get("supplied_footage")
    if isinstance(sf, dict) and sf.get("files"):
        items.append(f"**Supplied footage:** {', '.join(sf['files'])}, {sf.get('position') or 'top'} half of the split "
                     "screen; your recording in the other half. Nothing else from the brand's side.")
    tps = c.get("talking_points_list") or []
    req_ids = required_points(raw)
    items.append("**Talking points:** " + "; ".join(f"`{i}` \"{t.rstrip('.')}\"" + (" (required)" if i in req_ids else "")
                                                    for i, t in tps) + ". Every brand claim in the script traces to one "
                 "of these" + ("; the required ones go in every video" if req_ids else "") + ". One angle per video "
                 "reads better than every point at once.")
    if is_num(c.get("product_on_screen_by_s")):
        items.append(f"**Product on screen:** by second {c['product_on_screen_by_s']:g}.")
    items.append("**Never say:** " + (", ".join(f"\"{x}\"" for x in c["do_not_say"]) if c.get("do_not_say") else
                                      "nothing named") + ". Plus no claim about use or results you didn't have.")
    if c.get("cta"):
        items.append(f"**Call to action:** \"{c['cta']}\" ({ {'spoken': 'said in the video', 'caption': 'in the caption', 'both': 'said and in the caption'}.get(c.get('cta_in') or 'both') }).")
    if not files_only:
        req = [f"starts with **{cap.get('disclosure')}**"]
        for k in ("hashtags", "mentions"):
            if cap.get(k):
                req.append(f"{k}: " + ", ".join(cap[k]))
        if cap.get("links"):
            where = c.get("links_where") or "caption"
            req.append("links: " + ", ".join(cap["links"]) + {"caption": "", "bio": " (in the bio, not the caption)",
                                                              "either": " (in the caption or the bio)"}[where])
        items.append("**Every caption:** " + "; ".join(req) + ".")
        if cap.get("links") and (c.get("links_where") or "caption") in ("bio", "either"):
            items.append("**Bio link:** set the bio link on every account to " + ", ".join(cap["links"])
                         + " before you post.")
        when = []
        if d.get("not_in_hook") is True:
            when.append("not in the hook")
        if is_num(d.get("not_before_s")):
            when.append(f"not before second {d['not_before_s']:g}")
        screen = (f"\"{d.get('on_screen')}\" on screen from the first frame for {d.get('on_screen_seconds'):g} seconds"
                  if burned_text(c) != "none" and d.get("on_screen") else "nothing burned into the video (clean footage)")
        items.append(f"**Disclosure:** said out loud, ending by second {d.get('spoken_within_s'):g}"
                     + (f" ({', '.join(when)})" if when else "") + ", anywhere in that window (a short phrase works: "
                     f"\"{c.get('brand')} is paying me to show you this\", or a hook that opens with \"Ad, but ...\"); "
                     f"{screen}; first in the caption; the platform's paid-partnership setting.")
        if burned_text(c) != "any":
            items.append("**Text on the video:** " + ("none: no captions, no hook text, no label." if burned_text(c) ==
                         "none" else "only the small \"Ad\" label; no captions or hook text."))
        dic = info.get("dictated") or []
        if dic:
            items.append("**Only if true for you** (answer before you take it): " + "; ".join(
                f"\"{x}\"" for x, _ in dic[:6]) + ". A no means a reworded line (what the product does) or asking the "
                "brand.")
    ln = c.get("length") or {}
    if _num(ln.get("min_s")) and _num(ln.get("max_s")):
        items.append(f"**Length:** {ln['min_s']:g} to {ln['max_s']:g} seconds, vertical 9:16.")
    if c.get("language"):
        items.append(f"**Language:** {c['language']}.")
    geo = c.get("geo")
    if isinstance(geo, dict):
        share = f"at least {geo['min_share']:.0%} of viewers " if is_num(geo.get("min_share")) else "viewers "
        items.append(f"**Audience:** {share}in {', '.join(place_name(x) for x in geo['countries'])}. Post from accounts "
                     "whose audience is there; never a VPN or location trick.")
    items.append("**Music:** " + {"none": "no music", "licensed_only": "only music you hold a license for",
                                  "brief_supplied": "only the track the brief supplies",
                                  "any_licensed": "any music you hold a license for"}.get(c.get("music") or "none",
                                                                                           "no music")
                 + ". The brand gets a license to your video for ads, so trending sounds are a liability.")
    el = c.get("eligibility")
    if isinstance(el, dict) and el:
        bits = []
        if is_num(el.get("min_followers")):
            bits.append(f"at least {int(el['min_followers']):,} followers")
        if is_num(el.get("min_account_age_days")):
            bits.append(f"at least {int(el['min_account_age_days'])} days old")
        if el.get("countries"):
            bits.append("based in " + ", ".join(place_name(x) for x in el["countries"]))
        if el.get("account_type") and el["account_type"] != "any":
            bits.append({"business_or_creator": "an Instagram Business or Creator account", "creator": "a Creator account",
                         "business": "a Business account"}[el["account_type"]])
        if el.get("public"):
            bits.append("public, not private")
        items.append("**Each account must be:** " + "; ".join(bits) + ". The plan asks you to confirm this per account.")
    if not files_only:
        items.append("**Accounts:** " + ("a dedicated account for this campaign only. " if c.get("dedicated_account")
                                          else "") + f"post only from your own accounts, connected and verified in "
                     f"{c.get('marketplace') or 'the marketplace'}.")
        items.append(f"**Submitting:** within {int(c['submit_within_minutes'])} minutes of posting; one post goes into one "
                     "campaign, once" + (f"; at most {c['max_submissions']} submissions" if c.get("max_submissions") else "")
                     + ".")
        items.append(f"**Time live:** public and unchanged for {int(c['days_live'])} days; views count for "
                     f"{int(c['window_days'])} days" + (" from the day a video crosses the payout threshold." if
                                                        c.get("window_from") == "threshold" else " after posting."))
    items.append("**Approval:** " + ("the brand approves each draft before it is posted." if c.get("pre_approval")
                                     else "no approval step before posting."))
    if c.get("deadline"):
        end = deadline_end(c["deadline"], c.get("deadline_tz"))
        zone = c.get("deadline_tz") or "UTC"
        items.append(f"**Deadline:** {c['deadline']}" + (f" (ends {end:%d %b %H:%M} UTC; the day is read in {zone}"
                                                           + ("" if c.get("deadline_tz") else ", set \"deadline_tz\" if the "
                                                              "brief means another zone") + ")" if end else "") + ".")
    items.append("**Usage rights:** " + (c["usage_rights"] if isinstance(c.get("usage_rights"), str) else
                                         "not stated in the brief. On most marketplaces an approved video gives the brand "
                                         "a license to run it, with your face and voice, in its own ads, often worldwide "
                                         "and with no end date. Ask if it matters to you") + ".")
    if c.get("ad_code"):
        items.append(f"**Ad code:** {c['ad_code']}. You make it in the app yourself after posting.")
    if c.get("reference_videos"):
        items.append("**Reference videos:** " + ", ".join(c["reference_videos"]) + ". Watch them for pacing and "
                     "structure; the script notes what it takes from them. Never copy their footage.")
    if c.get("doc_only_rules"):
        items.append("**Only in the outside document:** " + "; ".join(c["doc_only_rules"]) + ". Follow them; only rules "
                     "on the campaign page are grounds for a rejection, which matters in an appeal.")
    items.append("**Proof to keep:** " + ("; ".join(c["proof"]) if c.get("proof") else "nothing extra named")
                 + ". Screenshots at 24 hours, 72 hours and 7 days per post either way.")
    if c.get("make_money_campaign") and isinstance(raw.get("typical_earnings"), dict):
        te = raw["typical_earnings"]
        items.append(f"**Typical earnings line (said in any video with an earnings claim):** \"{te.get('line')}\" "
                     f"Source: {te.get('source')}.")
    elif c.get("make_money_campaign"):
        items.append("**Earnings claims:** none. No money figure, no \"I made\", no \"you can make\": the brand gave no "
                     "typical-earnings line.")
    if c.get("language") and str(c["language"]).lower()[:2] != "en":
        items.append(f"**Claims check:** reads English only. In {c['language']}, read every line yourself.")
    return items


def required_points(raw):
    tps = raw.get("talking_points") if isinstance(raw, dict) else None
    return {str(t.get("id") or f"tp{i}") for i, t in enumerate(tps or [], 1)
            if isinstance(t, dict) and t.get("required") is True} if isinstance(tps, list) else set()


def money_line(c):
    if deliver(c):
        return ""
    cur = c.get("currency", "USD")
    bits = []
    for p in c.get("platforms") or {}:
        if p not in LIMITS:
            continue
        rate, mn, cap, mv = terms(c, p)
        _, paid, _ = payout(10000, rate, mn, cap, c["fee_pct"], mv, cur)
        bits.append(f"{LIMITS[p]['label']} {money(paid, cur)}")
    out = ("At 10,000 views one video earns, after the fee: " + ", ".join(bits) + ". Most videos get fewer views; the "
           "campaign's own count decides. Nothing here promises income.") if bits else ""
    cr = c.get("creator") if isinstance(c.get("creator"), dict) else {}
    if bits and is_num(cr.get("hourly_floor"), 0.01) and is_num(cr.get("hours_per_video"), 0.01):
        need = []
        target = cr["hourly_floor"] * cr["hours_per_video"]
        for p in c.get("platforms") or {}:
            if p not in LIMITS:
                continue
            rate, mn, cap, mv = terms(c, p)
            net = rate * (1 - c["fee_pct"] / 100.0)
            if not net or (cap is not None and cap * (1 - c["fee_pct"] / 100.0) < target):
                need.append(f"{LIMITS[p]['label']} never (the cap is under it)" if net else f"{LIMITS[p]['label']} never")
                continue
            v = max(int(target / net * 1000 + 0.999), threshold_views(c, p))
            need.append(f"{LIMITS[p]['label']} {v:,}")
        out += (f"\n\nYour floor: {money(cr['hourly_floor'], cur)} an hour at {cr['hours_per_video']:g} hours per video "
                f"means about {money(target, cur)} per video. Views needed per video, after the fee: "
                + ", ".join(need) + ".")
    elif bits:
        out += ("\n\nAsk the creator: your hourly floor and how long one video takes you (filming, editing, posting). "
                "With them the checklist shows the views a video needs to beat your floor (\"creator\": "
                "{\"hourly_floor\": ..., \"hours_per_video\": ...}).")
    st = c.get("campaign_stats") if isinstance(c.get("campaign_stats"), dict) else {}
    if bits and is_num(st.get("approved_videos"), 1) and is_num(st.get("total_views"), 0):
        avg = int(st["total_views"] / st["approved_videos"])
        out += (f" Campaign average so far: {avg:,} views per approved video ({int(st['approved_videos']):,} videos, "
                f"{int(st['total_views']):,} views, from the campaign page"
                + (f" on {st['checked_at']}" if st.get("checked_at") else "") + "). That is an average, not a forecast.")
    return out


def report(info, path):
    c = info["campaign"] if isinstance(info["campaign"], dict) else {}
    lines = [f"# Campaign checklist: {c.get('name', '(no name)')}", ""]
    lines.append(f"Campaign id `{c.get('id', '?')}`, brand {c.get('brand', '?')}, {c.get('marketplace') or 'marketplace not given'}"
                 + f". Brief dated {c.get('brief_date') or 'not given'}, checklist version `{info['version']}` (changes "
                 "when the campaign file or the brief changes).")
    lines.append("")
    if example_demo(info.get("raw")):
        lines += ["**EXAMPLE ONLY: a made-up demo campaign.** Its videos show the real \"Ad\" label in the "
                  "corner with an \"EXAMPLE: not a real ad\" label opposite it, and a labelled placeholder where your "
                  "recording goes. A real campaign can't use this.", ""]
    v = info["verdict"]
    lines += [f"## Verdict: {v}", ""]
    if info["reasons"]:
        lines += [f"- {r}" for r in info["reasons"]] + [""]
    if info["conditions"]:
        lines += ["Conditions:", ""] + [f"- {x}" for x in info["conditions"]] + [""]
    errs = [i for i in info["issues"] if i[0] == "error"]
    warns = [i for i in info["issues"] if i[0] == "warning"]
    if errs:
        lines += [f"**{len(errs)} thing(s) to fix in {rel(path)}:**", ""] + [f"- `{f}`: {m}" for _, f, m in errs] + [""]
    if warns:
        lines += [f"- warning `{f}`: {m}" for _, f, m in warns] + [""]
    if isinstance(info["campaign"], dict) and not errs:
        lines += ["## Checklist", ""] + [f"{n}. {t}" for n, t in enumerate(checklist(info), 1)] + [""]
        ml = money_line(c)
        if ml:
            lines += [ml, ""]
    sections = (
        ("brand_account", "Refused: an account the brand owns or a made-up persona account",
         "The videos would go out from an account that isn't yours. The skill doesn't do this campaign."),
        ("persona", "Not done as written: posting as someone you aren't",
         "These ask you to post as a customer or user you aren't. The skill makes videos in your own voice, disclosed. "
         "Ask the brand whether that is accepted."),
        ("dictated", "Only if true for you",
         "The brief writes your experience for you. Answer each one yes or no before you take the campaign. Yes: it "
         "goes in the script as your confirmed experience. No: say what the product does instead (\"here's what "
         "<brand> does\"), or ask the brand for a version without it."),
        ("fake", "Refused: testimonials about use that didn't happen",
         "You can only talk about your own real experience. The skill doesn't write these lines."),
        ("ai", "Refused: AI presenters or cloned voices required",
         "A real person films; the skill never generates or alters a face or a voice."),
        ("ai_allowed", "AI presenters allowed, not required", "You film yourself as always."),
        ("tts", "A computer voice the skill doesn't make",
         "The skill uses your own voice. Ask the brand whether a real voiceover is accepted."),
        ("tts_allowed", "A computer voice allowed, not required", "Your own voice is used."),
        ("timing", "When to disclose", "Followed: the disclosure is said where the brief wants it, inside the window."),
        ("optional", "Disclosure called optional", "Every video discloses anyway, as the law requires."),
        ("placement", "Disclosure placement the skill doesn't follow",
         "A comment doesn't count as a disclosure. The skill keeps #ad first in the caption and says it out loud; check "
         "with the brand that this is accepted."),
        ("no_text", "No text on the video",
         "Allowed: set \"burned_text\" in campaign.json. Captions and the hook text stay off; the disclosure is said, "
         "first in the caption and the platform's label."),
        ("tone", "Tone notes: followed as style, the disclosure stays",
         "These ask for a natural, unscripted feel. The script reads relaxed and the edit isn't glossy, and every video "
         "still says it's an ad, shows the on-screen label, starts the caption with the disclosure and sets the "
         "platform's paid-partnership setting."),
        ("hide", "Never followed",
         "The brief asks to hide that the video is paid. Every video keeps the spoken disclosure, the on-screen \"Ad\", "
         "#ad first in the caption and the platform's paid-partnership setting (FTC in the US, CMA in the UK, consumer "
         "law in the EU)."),
        ("bait", "Never done", "Bought or arranged engagement or location tricks: a permanent ban on the marketplaces."),
        ("money", "Make-money content",
         "The brief is about earning money. Fine to make, when it's plain and true: any earnings claim (a figure, \"I "
         "made\", \"you can make\") needs the brand's typical-earnings line said in the same video, and nothing promises "
         "income (FTC rules on earnings claims)."),
        ("grq", "Get-rich-quick framing: never used",
         "TikTok bans get-rich-quick branded content, and the FTC treats quick or easy money promises as deceptive. The "
         "scripts and captions never use this framing."),
        ("outside", "Rules in an outside document", "Paste that document so its rules become checks too."),
    )
    for key, title, why in sections:
        if info.get(key):
            lines += [f"## {title}", "", why, ""] + [f"- \"{s}\"" for s, _ in info[key]] + [""]
    if info.get("prohibited") or info.get("restricted"):
        lines += ["## TikTok branded content topics", ""]
        lines += [f"- banned: {t} (\"{s}\")" for t, s in info.get("prohibited") or []]
        lines += [f"- invitation only: {t} (\"{s}\")" for t, s in info.get("restricted") or []] + [""]
    if info.get("read"):
        lines += ["## Read these sentences yourself", "",
                  "They talk about the disclosure next to a \"no\" or a rejection, and the checks can't tell which way "
                  "they point. If one asks to hide or drop the disclosure, treat it like the ones above.", ""]
        lines += [f"- \"{s}\"" for s in info["read"]] + [""]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Check a UGC campaign, print its checklist and a go or no-go.")
    ap.add_argument("campaign")
    ap.add_argument("--brief", help="the brief text as pasted (overrides brief_file in the campaign)")
    ap.add_argument("--out", help="where to write the checklist (default: checklist.md next to the campaign file)")
    a = ap.parse_args()
    info = load(a.campaign, a.brief)
    md = report(info, a.campaign)
    out = a.out or os.path.join(os.path.dirname(os.path.abspath(a.campaign)), "checklist.md")
    write_text(out, md)
    print(md.rstrip())
    print()
    errs = [i for i in info["issues"] if i[0] == "error"]
    print(f"verdict: {info['verdict']}" + (f" ({'; '.join(info['reasons'])})" if info["reasons"] else ""))
    print(f"{len(errs)} error(s) -> {rel(out)}")
    if info["verdict"] == "GO":
        print("next: show this checklist to the creator and wait for them to confirm it before writing the script")
    elif info["verdict"] == "REFUSED":
        print("next: tell the creator plainly why this campaign is refused, and offer to look at another one")
    sys.exit(0 if info["verdict"] == "GO" else 1)


if __name__ == "__main__":
    guard(main)
