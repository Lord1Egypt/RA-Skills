#!/usr/bin/env python3
"""Check the script the agent wrote for a UGC campaign, then write script.md and shotlist.md.

    python3 scripts/script.py script.json                          # check, write script.md, shotlist.md
    python3 scripts/script.py script.json --confirm l3 --note "used it daily for three weeks"
                                                                   # the creator said this line is true

script.json (references/script-file.md) holds 3 to 5 hooks, the lines in order, and which hook
opens each account's video. Every line that makes a claim is tagged:

  "experience"  the creator's own use or result. Needs the creator's confirmation, recorded with
                --confirm after they say it is true. Editing the line voids it.
  "brand"       a claim from the brief. Names the talking point it comes from ("talking_point":
                "tp2"); script.md shows that talking point next to it.
  "cut"         taken out. Kept in the file so nobody adds it back by accident.

Checked: 3 to 5 hooks, each account opening with its own; the spoken disclosure said by the
campaign's second (estimated at the creator's speaking pace, with the longest hook first); every
line that sounds like a claim or like the creator's own use is tagged; experience claims confirmed;
brand claims trace to a talking point; nothing from the brief's do_not_say list; no absolute claim
("guaranteed", "risk-free", "cures") unless the talking point says it word for word; the required
call to action; on a make-money campaign, the typical-earnings line.

Exit code 0 when the script is ready to film, 1 otherwise.
"""
import argparse, os, re, sys

sys.dont_write_bytecode = True   # nothing is ever written into the skill's own folder
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import campaign as campaign_mod  # noqa: E402
from ugclib import (ABSOLUTE_CLAIMS, CLAIM_HINTS, EARNINGS_CLAIM, GET_RICH_QUICK, content_words, experience_hint,  # noqa: E402
                    die, disclosing_part, find_phrases, first_person_claim, guard, has_banned, hide_ad_hits, iso, is_num,
                    now_utc, read_json, rel,
                    says_paid, strip_known, text_sha, valid_id, words_of, write_json, write_text)

MARK = "<!-- written by script.py; it replaces this file on every run -->"
WPS = 2.6           # words a second at a natural speaking pace (about 155 a minute)
KINDS = ("disclosure", "cta", "typical_earnings", "line")
CLAIMS = ("experience", "brand", "cut", "none")


def wps_of(s):
    w = s.get("words_per_second")
    return float(w) if isinstance(w, (int, float)) and not isinstance(w, bool) and 1.5 <= w <= 4.5 else WPS


def secs(text, wps):
    return len(words_of(text)) / wps


def confirmations_path(script_path):
    return os.path.join(os.path.dirname(os.path.abspath(script_path)), "confirmations.json")


def load_confirmations(script_path):
    p = confirmations_path(script_path)
    if not os.path.isfile(p):
        return {}
    data = read_json(p, "the creator's confirmations")
    return data if isinstance(data, dict) else {}


def line_sha(line):
    return text_sha(line.get("say") or "")[:16]


def check_script(script_path):
    """Load and check a script. Returns a model: campaign info, script, lines, problems, version."""
    s = read_json(script_path, "the script")
    if not isinstance(s, dict):
        die(f"{rel(script_path)} must hold one JSON object: campaign, format, hooks, lines, openings")
    sdir = os.path.dirname(os.path.abspath(script_path))
    cpath = s.get("campaign")
    if not isinstance(cpath, str) or not cpath:
        die(f"{rel(script_path)} needs \"campaign\": the path of campaign.json")
    info = campaign_mod.load(os.path.join(sdir, cpath))
    c = info["campaign"] if isinstance(info["campaign"], dict) else {}
    issues = []

    def bad(where, msg, level="error"):
        issues.append((level, where, msg))

    cerrs = [i for i in info["issues"] if i[0] == "error"]
    if cerrs:
        die(f"{s.get('campaign')} has {len(cerrs)} problem(s); fix them first (python3 scripts/campaign.py "
            f"{s.get('campaign')}):\n" + "\n".join(f"  {f}: {m}" for _, f, m in cerrs))
    if info["verdict"] != "GO":
        bad("campaign", f"the campaign's verdict is {info['verdict']}: " + "; ".join(info["reasons"] or ["fix campaign.json"]))
    files_only = campaign_mod.deliver(c)
    fmts = s.get("format")
    fmts = [fmts] if isinstance(fmts, str) else fmts
    if not isinstance(fmts, list) or not fmts or any(f not in campaign_mod.FORMATS for f in fmts):
        bad("format", f"one of {', '.join(campaign_mod.FORMATS)}, or a list of them when accounts get different layouts")
        fmts = [f for f in fmts or [] if f in campaign_mod.FORMATS] if isinstance(fmts, list) else []
    for f in fmts:
        if c.get("formats_list") and f not in c["formats_list"]:
            bad("format", f"{f} isn't a format this brief accepts ({', '.join(c['formats_list'])})")
    fmt = fmts[0] if fmts else None
    if c.get("language") and s.get("language") and str(s["language"]).lower() != str(c["language"]).lower():
        bad("language", f"the brief asks for {c['language']}; this script is {s['language']}")
    wps = wps_of(s)

    tps = dict(c.get("talking_points_list") or [])
    confs = load_confirmations(script_path)
    dns = [x for x in (c.get("do_not_say") or []) if isinstance(x, str)]
    raw = info["raw"] if isinstance(info["raw"], dict) else {}
    te = raw.get("typical_earnings") if isinstance(raw.get("typical_earnings"), dict) else {}
    te_line = te.get("line") if isinstance(te.get("line"), str) and te["line"].strip() else None
    known = (c.get("brand"), c.get("cta"), te_line)

    def claim_check(where, item, text, kind, row):
        """The same claim rules for a hook and for every kind of line."""
        claim = item.get("claim")
        probe = strip_known(text, *known) if kind in ("cta", "typical_earnings", "disclosure") else \
            strip_known(text, c.get("brand"))
        low = probe.lower()
        exp_hint = experience_hint(probe)
        claim_hint = re.search(CLAIM_HINTS, low)
        fp = first_person_claim(probe)
        if exp_hint and claim != "experience" and kind != "typical_earnings":
            bad(where, f"\"{exp_hint}\" says you used it or got a result. Tag it \"experience\" and confirm it "
                "with the creator, or rewrite or cut it")
        elif claim_hint and claim in (None, "none") and kind not in ("typical_earnings",):
            bad(where, f"\"{claim_hint.group(0)}\" reads like a claim. Tag it \"brand\" (with its talking point) or "
                "\"experience\", or rewrite it")
        elif fp and claim in (None, "none") and kind == "line":
            bad(where, f"\"{fp}\": a line about you is a claim about your own use. Tag it \"experience\" and confirm it, "
                "or rewrite it without the first person")
        elif kind == "line" and claim is None and where.startswith("line"):
            bad(where, "tag every line: \"claim\" is \"brand\" (with its talking point), \"experience\", \"cut\" or "
                "\"none\" (no claim at all)")
        if claim == "experience":
            cf = confs.get(item.get("id"))
            if not isinstance(cf, dict) or cf.get("text_sha") != line_sha({"say": text}):
                bad(where, "an experience claim needs the creator's word that it is true for them. Ask, then run "
                    f"script.py --confirm {item.get('id')} --note \"<what they said>\"" + (
                        " (the text changed after it was confirmed)" if isinstance(cf, dict) else ""))
            else:
                row["confirmed"] = cf
        if claim == "brand":
            tp = item.get("talking_point")
            if tp not in tps:
                bad(where, f"a brand claim must name the talking point it comes from (one of {', '.join(tps) or 'none'})")
            else:
                row["tp"] = (tp, tps[tp])
                share = len(content_words(probe) & content_words(tps[tp])) / max(1, len(content_words(probe)))
                if share < 0.2:
                    bad(where, f"shares few words with talking point {tp} (\"{tps[tp]}\"). Check it says what the brief "
                        "says, no more", "warning")
        m = re.search(ABSOLUTE_CLAIMS, low)
        if m:
            tp_text = row.get("tp", (None, ""))[1].lower()
            if m.group(0) not in tp_text:
                bad(where, f"\"{m.group(0)}\" needs proof the advertiser has, and the brief's talking points don't say "
                    "it. Cut it")
        g = find_phrases(text, GET_RICH_QUICK)
        if g:
            bad(where, f"\"{g[0][0]}\" is get-rich-quick framing: TikTok bans it in branded content and the FTC treats it "
                "as deceptive. Say plainly what the product does")
        if kind != "typical_earnings" and re.search(EARNINGS_CLAIM, low):
            row["earnings"] = True
            if not te_line:
                bad(where, "an earnings claim (a money figure, \"I made\", \"you can make\") needs the brand's "
                    "typical-earnings line, and the brief gives none. Leave it out, or ask the brand for its "
                    "typical-earnings line (references/claims.md)")
        for w in dns:
            if has_banned(text, w):
                bad(where, f"the brief says never to say \"{w}\"")
        for snt, _ in hide_ad_hits(text):
            bad(where, f"\"{snt}\" plays down that it's an ad")

    # hooks
    hooks = s.get("hooks")
    hk, hook_rows = {}, {}
    if not isinstance(hooks, list) or not all(isinstance(h, dict) for h in hooks):
        bad("hooks", "a list of {\"id\": \"h1\", \"text\": \"...\"}")
        hooks = []
    for h in hooks:
        hid, txt = h.get("id"), h.get("text")
        if not valid_id(hid) or not isinstance(txt, str) or not txt.strip():
            bad("hooks", "each hook needs an id (like \"h1\") and its text")
            continue
        if hid in hk:
            bad("hooks", f"hook id {hid} is used twice")
        hk[hid] = txt.strip()
        hrow = {"id": hid}
        claim_check(f"hook {hid}", h, txt.strip(), "hook", hrow)
        hook_rows[hid] = dict(hrow, say=txt.strip(), action=h.get("action") if isinstance(h.get("action"), str) else "",
                              claim=h.get("claim"))
        n = len(words_of(txt))
        if n > 12:
            bad(f"hook {hid}", f"{n} words; a hook that lands in the first 3 seconds is about 12 words or fewer", "warning")
    if not hk:
        bad("hooks", "write at least one hook: the first words of the video")
    elif len(hk) < 3:
        bad("hooks", f"{len(hk)} hook{'' if len(hk) == 1 else 's'}: fine for one edit on every platform; 3 to 5 let you "
            "test openings", "warning")
    elif len(hk) > 5:
        bad("hooks", f"{len(hk)} hooks; 3 to 5 is plenty", "warning")
    if len({t.lower() for t in hk.values()}) != len(hk):
        bad("hooks", "two hooks say the same thing; each must open differently")

    # openings: which hook each account's video starts with
    op = s.get("openings") or {}
    if not isinstance(op, dict) or (not op and not files_only):
        bad("openings", "{\"<account name>\": \"<hook id>\"}: which hook opens each account's video")
        op = {}
    for acc, hid in op.items():
        if hid not in hk:
            bad("openings", f"{acc}: hook {hid} isn't one of the hooks ({', '.join(hk) or 'none'})")
    # Accounts may share an opening: one edit cross-posted to TikTok, Reels and Shorts is normal.
    # check_videos refuses the same video twice on one platform or across campaigns.

    # lines
    lines = s.get("lines")
    if not isinstance(lines, list) or not lines or not all(isinstance(x, dict) for x in lines):
        die(f"{rel(script_path)} needs \"lines\": the script in order, each {{\"id\", \"say\", ...}}")
    ids, kept = set(), []
    for n, ln in enumerate(lines, 1):
        lid = ln.get("id")
        where = f"line {lid if isinstance(lid, str) else n}"
        if not valid_id(lid):
            bad(where, "each line needs a short id (like \"l3\")")
            lid = f"line-{n}"
        if lid in ids:
            bad(where, "this line id is used twice")
        ids.add(lid)
        say = ln.get("say")
        if not isinstance(say, str) or not say.strip():
            bad(where, "\"say\": what the creator says")
            continue
        kind = ln.get("kind", "line")
        claim = ln.get("claim")
        if kind not in KINDS:
            bad(where, f"kind is one of {', '.join(KINDS)}")
        if claim is not None and claim not in CLAIMS:
            bad(where, "claim is \"experience\", \"brand\", \"cut\" or left out (no claim)")
        row = {"id": lid, "say": say.strip(), "kind": kind, "claim": claim, "issues": []}
        if claim == "cut":
            row["cut"] = True
            kept.append(row)
            continue
        claim_check(where, ln, say.strip(), kind, row)
        kept.append(row)
    spoken = [r for r in kept if not r.get("cut")]
    # required talking points, and one angle per video
    covered = {r["tp"][0] for r in spoken + list(hook_rows.values()) if r.get("tp")}
    for tid in sorted(campaign_mod.required_points(raw)):
        if tid not in covered:
            bad("talking_points", f"the brief requires talking point {tid} (\"{tps.get(tid, '')}\") in every video; "
                "no line or hook says it")
    nbrand = len({r["tp"][0] for r in spoken if r.get("tp")})
    if nbrand > 2:
        bad("lines", f"{nbrand} different talking points in one video. Videos with one angle read better and feel less "
            "like an ad; spread the rest over your other videos", "warning")
    if c.get("make_money_campaign") or any(r.get("earnings") for r in spoken + list(hook_rows.values())):
        if any(r.get("earnings") for r in spoken + list(hook_rows.values())) and te_line and \
                not any(r["kind"] == "typical_earnings" and content_words(te_line) <= content_words(r["say"])
                        for r in spoken):
            bad("typical_earnings", f"this script makes an earnings claim, so it says the typical-earnings line too "
                f"(\"{te_line}\"), as a line with \"kind\": \"typical_earnings\"")

    # disclosure said in time: by the script's disclosure line, or by a hook that discloses ("Ad, but ...")
    disc_rows = [r for r in spoken if r["kind"] == "disclosure"]
    timing = {}
    longest = max((secs(t, wps) for t in hk.values()), default=0.0)
    t = longest
    for r in spoken:
        timing[r["id"]] = (t, t + secs(r["say"], wps))
        t += secs(r["say"], wps)
    total = t
    dcfg = c.get("disclosure") or {}
    window = float(dcfg.get("spoken_within_s") or 10)
    not_before = float(dcfg.get("not_before_s")) if is_num(dcfg.get("not_before_s")) else None
    brand = c.get("brand")
    disc_hooks = {hid: disclosing_part(txt, brand) for hid, txt in hk.items() if disclosing_part(txt, brand)}
    if not files_only:
        if dcfg.get("not_in_hook") is True:
            for hid in disc_hooks:
                bad(f"hook {hid}", "the brief says not to say it's an ad in the hook. Disclose in a line after it")
        line_end = None
        if disc_rows:
            r = disc_rows[0]
            part = disclosing_part(r["say"], brand)
            if not part:
                bad(f"line {r['id']}", "the disclosure line must say plainly that it is paid (\"this is an ad for "
                    f"{brand or '<brand>'}\", \"{brand or '<brand>'} is paying me to show you this\", \"#ad\")")
            else:
                if brand and str(brand).lower() not in r["say"].lower():
                    bad(f"line {r['id']}", f"name the brand in the disclosure (\"... for {brand}\")", "warning")
                rel_start = timing[r["id"]][0] - longest
                line_end = rel_start + secs(part, wps)
                r["disclosure_end"] = longest + line_end
                if not_before is not None and timing[r["id"]][0] < not_before:
                    bad(f"line {r['id']}", f"the disclosure starts at about {timing[r['id']][0]:.1f} s; the brief wants it "
                        f"from second {not_before:g}. Put a line before it")
        used = sorted(set(op.values())) or sorted(hk)
        late = []
        for hid in used:
            if hid not in hk:
                continue
            if hid in disc_hooks and dcfg.get("not_in_hook") is not True:
                end = secs(disc_hooks[hid], wps)
            elif line_end is not None:
                end = secs(hk[hid], wps) + line_end
            else:
                late.append((hid, None))
                continue
            if end > window:
                late.append((hid, end))
        if not disc_rows and not disc_hooks:
            bad("disclosure", f"say it's an ad in the first {window:g} seconds: a line with \"kind\": \"disclosure\", like "
                f"\"{brand or '<brand>'} is paying me to show you this.\"" + (
                    ", or a hook that opens with it (\"Ad, but ...\")" if dcfg.get("not_in_hook") is not True else ""))
        else:
            for hid, end in late:
                if end is None:
                    bad(f"hook {hid}", "videos that open with this hook never say it's an ad: add a line with \"kind\": "
                        "\"disclosure\", or open with a hook that discloses")
                    continue
                tip = (" With a window this short, open with a hook that discloses: \"Ad, but this could be your lock "
                       "screen\", \"Sponsored by " + str(brand or "<brand>") + ": watch this\" (references/hooks.md)"
                       if window <= 4 and dcfg.get("not_in_hook") is not True else
                       " Move it up or shorten what comes before")
                bad(f"hook {hid}", f"a video opening with this hook finishes the disclosure at about {end:.1f} s; the "
                    f"brief wants it said by {window:g} s.{tip}")
    # call to action
    cta = c.get("cta")
    cta_in = c.get("cta_in") or "both"
    if cta and cta_in in ("spoken", "both"):
        cta_rows = [r for r in spoken if r["kind"] == "cta"]
        if not cta_rows:
            bad("cta", f"the brief requires the call to action \"{cta}\" spoken: add a line with \"kind\": \"cta\"")
        elif not any(content_words(cta) <= content_words(r["say"]) | {"link", "bio"} or
                     len(content_words(cta) & content_words(r["say"])) >= max(1, int(len(content_words(cta)) * 0.6))
                     for r in cta_rows):
            bad("cta", f"the call to action line doesn't say what the brief asks (\"{cta}\")")
    for r in spoken:
        if r["kind"] == "typical_earnings" and not (te_line and content_words(te_line) <= content_words(r["say"])):
            bad(f"line {r['id']}", "a typical-earnings line says the brand's line from campaign.json word for word"
                + (f" (\"{te_line}\")" if te_line else "; the brief gives none, so leave it out"))
    # length
    ln = c.get("length") or {}
    if isinstance(ln.get("max_s"), (int, float)) and total > ln["max_s"]:
        bad("length", f"about {total:.0f} s spoken at a natural pace; the brief allows {ln['max_s']:g} s. Cut lines")
    if isinstance(ln.get("min_s"), (int, float)) and total < ln["min_s"]:
        bad("length", f"about {total:.0f} s spoken; the brief wants at least {ln['min_s']:g} s", "warning")
    version = text_sha({k: s.get(k) for k in ("format", "hooks", "lines", "openings", "language")})[:12]
    return {"script": s, "path": script_path, "dir": sdir, "info": info, "campaign": c, "hooks": hk, "openings": op,
            "rows": kept, "spoken": spoken, "timing": timing, "total": total, "issues": issues, "version": version,
            "format": fmt, "formats": fmts, "wps": wps, "hook_rows": hook_rows}


TAG = {"experience": "your experience, confirmed", "brand": "brand claim", None: ""}


def script_md(m):
    c, s = m["campaign"], m["script"]
    errs = [i for i in m["issues"] if i[0] == "error"]
    out = [MARK, f"# Script: {c.get('name', '')}", "",
           "Format: " + "; ".join(campaign_mod.FORMAT_WORDS.get(f, f) for f in m["formats"])
           + f". Script version `{m['version']}`. About {m['total']:.0f} seconds at a natural pace.", ""]
    if campaign_mod.example_demo(c):
        out += ["**EXAMPLE ONLY: a made-up demo campaign.** Nothing here is a real ad.", ""]
    if errs:
        out += [f"**Not ready to film: {len(errs)} thing(s) to fix.**", ""] + [f"- {w}: {msg}" for _, w, msg in errs] + [""]
    warns = [i for i in m["issues"] if i[0] == "warning"]
    if warns:
        out += [f"- warning, {w}: {msg}" for _, w, msg in warns] + [""]
    out += ["## Hooks", "", "Say the hook first; it is also on screen for the first seconds. The same edit can go to "
            "TikTok, Reels and Shorts; a different hook per account is an optional test of which opening works.", ""]
    by_hook = {}
    for acc, hid in m["openings"].items():
        by_hook.setdefault(hid, []).append(acc)
    for hid, txt in m["hooks"].items():
        who = f" (opens: {', '.join(by_hook[hid])})" if hid in by_hook else ""
        hr = m.get("hook_rows", {}).get(hid, {})
        tag = ""
        if hr.get("tp"):
            tag = f", brand claim from {hr['tp'][0]}"
        elif hr.get("claim") == "experience":
            tag = ", your experience, confirmed" if hr.get("confirmed") else ", NOT CONFIRMED"
        act = f" Do: {hr['action']}." if hr.get("action") else ""
        out.append(f"- `{hid}` \"{txt}\"{who}{tag}.{act}")
    out += ["", "## Script", "", "| Time | Line | Tag |", "|---|---|---|"]
    for r in m["spoken"]:
        a, b = m["timing"][r["id"]]
        tag = {"disclosure": "spoken disclosure", "cta": "call to action", "typical_earnings": "typical earnings"}.get(
            r["kind"], "")
        if r.get("claim") == "brand" and r.get("tp"):
            tag = f"brand claim, from talking point {r['tp'][0]}: \"{r['tp'][1]}\""
        elif r.get("claim") == "experience":
            note = (r.get("confirmed") or {}).get("note")
            tag = "your experience" + (f", confirmed: \"{note}\"" if note else ", NOT CONFIRMED")
        out.append(f"| {a:.0f} to {b:.0f} s | {r['say']} | {tag} |")
    cut = [r for r in m["rows"] if r.get("cut")]
    if cut:
        out += ["", "## Cut", "", "Taken out: not true for you, or not something the brief lets you claim.", ""]
        out += [f"- ~~{r['say']}~~" for r in cut]
    c_cta = c.get("cta")
    if c_cta:
        out += ["", f"Call to action the brief requires: \"{c_cta}\""]
    out += ["", "Times assume the longest hook first. Say a line in your own words if it feels stiff: check_videos.py "
            "reads what you actually said and flags anything that isn't in the script, so a new claim gets confirmed or "
            "cut before posting.", ""]
    return "\n".join(out)


SHOTS = {
    "talking_head": [
        "Phone upright (vertical), at eye level, about an arm's length away. Back camera if you can see yourself.",
        "Your eyes about a third down from the top. Keep the top 15% clear (the \"Ad\" label sits there) and the "
        "bottom 25% clear (captions and the app's own text).",
        "Light from a window in front of you; no window behind you. A quiet room, the phone's own mic close.",
        "Film it in one go: all the hooks, then the script. Restart any line as often as you like; the edit keeps "
        "the last complete try of each line.",
    ],
    "split_screen": [
        "Your recording fills the {mine} half of the screen; the brand's footage fills the {theirs} half.",
        "Phone upright, eye level. Your face in the middle of the frame: the edit crops your recording to a "
        "near-square, so anything at the very top or bottom of your frame is cut.",
        "Look at the camera, react to the footage, talk. Window light in front of you, a quiet room.",
        "Film it in one go: all the hooks, then the script. Restart any line as often as you like.",
    ],
    "face_screen": [
        "Two recordings: the screen recording (phone upright, the built-in screen recorder, notifications off) and "
        "you, on the front camera, saying the script.",
        "The screen recording sits on top, your face in the bottom part. Keep your face centred in your frame.",
        "Do on screen what you say, in the same order, at the same pace. Use a test account with nothing private on "
        "screen: no names, messages, balances or emails.",
        "Film yourself in one go: all the hooks, then the script. Restart any line as often as you like.",
    ],
    "broll_voiceover": [
        "Record the voiceover first, in a quiet room, phone close to your mouth. Your own voice only.",
        "Then the shots: hands, the product, the screen, 3 to 5 seconds each, phone upright, steady.",
        "Keep the top 15% and bottom 25% of each shot free of anything that must be read.",
        "No other people in frame unless they agreed in writing; nothing private on screen.",
    ],
}
FILES = {"talking_head": ["takes/creator.mp4 (hooks and script in one clip)"],
         "split_screen": ["takes/creator.mp4 (hooks and script in one clip)", "the supplied footage, as the brand "
                          "sent it"],
         "face_screen": ["takes/creator.mp4 (hooks and script in one clip)", "takes/screen.mp4"],
         "broll_voiceover": ["takes/voiceover.m4a", "takes/broll-01.mp4, broll-02.mp4, ... in script order"]}


def shotlist_md(m):
    c = m["campaign"]
    sf = c.get("supplied_footage") if isinstance(c.get("supplied_footage"), dict) else {}
    theirs = sf.get("position") or "top"
    mine = "bottom" if theirs == "top" else "top"
    out = [MARK, f"# Shot list: {c.get('name', '')}", "",
           f"Script version `{m['version']}`. You film; the skill edits what you film and never makes or changes a face "
           "or a voice.", ""]
    if campaign_mod.example_demo(c):
        out += ["**EXAMPLE ONLY: a made-up demo campaign.** The example's videos use a labelled placeholder where your "
                "recording goes.", ""]
    window = float((c.get("disclosure") or {}).get("spoken_within_s") or 10)
    for fmt in m["formats"]:
        out += [f"## {campaign_mod.FORMAT_WORDS.get(fmt, fmt).capitalize()}", "", "Set up:", ""]
        out += [f"- {x.format(mine=mine, theirs=theirs)}" for x in SHOTS.get(fmt, [])]
        out += ["", "| Take | What you say | What is on screen |", "|---|---|---|"]
        for hid, txt in m["hooks"].items():
            act = (m.get("hook_rows", {}).get(hid) or {}).get("action")
            out.append(f"| hook `{hid}` | {txt} | {act + '; ' if act else ''}hook text on screen, a small Ad label in "
                       "the corner |")
        for r in m["spoken"]:
            scr = {"face_screen": "the screen recording shows what you describe",
                   "broll_voiceover": "a b-roll shot that shows this line",
                   "split_screen": f"the brand's footage in the {theirs} half, you in the {mine} half"}.get(fmt, "you, talking")
            if r["kind"] == "disclosure":
                scr += f"; said by second {window:g}"
            out.append(f"| `{r['id']}` | {r['say']} | {scr} |")
        out += ["", "Save the files as:", ""] + [f"- `{f}`" if " " not in f else
                                                  "- " + re.sub(r"^(\S+\.\w+)", r"`\1`", f) for f in FILES.get(fmt, [])] + [""]
    out += ["## Before you film", "",
            "- Back camera when you can frame yourself (it is sharper); otherwise the front camera at full resolution. "
            "Wipe the lens.",
            "- Tap and hold on your face to lock focus and exposure, so the picture doesn't pump when you move.",
            "- Do Not Disturb on. A wired or clip-on mic if the room echoes.",
            "- Film the hooks and the script in one clip, and restart lines freely: the edit finds the last complete try "
            "of each line.",
            "- No music playing in the room, and no music added in the app: music is declared in edit.json and has to be "
            "yours to use.",
            "- Nothing private in frame or on screen: other people, addresses, messages, account numbers.",
            "- Say only what is true for you. A line that isn't: tell your agent, it is cut or rewritten.", ""]
    return "\n".join(out)


def confirm(script_path, line_id, note):
    if not note or not note.strip():
        die("--note: what the creator said that makes this line true for them (\"used it daily for three weeks\")")
    s = read_json(script_path, "the script")
    lines = s.get("lines") if isinstance(s, dict) else None
    hooks = s.get("hooks") if isinstance(s, dict) else None
    ln = next((x for x in lines or [] if isinstance(x, dict) and x.get("id") == line_id), None)
    if ln is None:
        h = next((x for x in hooks or [] if isinstance(x, dict) and x.get("id") == line_id), None)
        ln = {"id": h.get("id"), "say": h.get("text"), "claim": h.get("claim")} if h else None
    if ln is None:
        die(f"there is no line or hook {line_id} in {rel(script_path)}")
    if ln.get("claim") != "experience":
        die(f"line {line_id} isn't tagged \"experience\"; only the creator's own use or results are confirmed this way")
    confs = load_confirmations(script_path)
    confs[line_id] = {"text_sha": line_sha(ln), "say": ln.get("say"), "note": note.strip(), "at": iso(now_utc())}
    write_json(confirmations_path(script_path), confs)
    print(f"confirmed {line_id}: \"{ln.get('say')}\" ({note.strip()}). Editing the line voids this.")


def main():
    ap = argparse.ArgumentParser(description="Check a UGC script, write script.md and shotlist.md.")
    ap.add_argument("script")
    ap.add_argument("--confirm", metavar="LINE_ID", help="record that the creator says this experience line is true")
    ap.add_argument("--note", help="with --confirm: what the creator said")
    a = ap.parse_args()
    if a.confirm:
        confirm(a.script, a.confirm, a.note)
        return
    m = check_script(a.script)
    write_text(os.path.join(m["dir"], "script.md"), script_md(m))
    write_text(os.path.join(m["dir"], "shotlist.md"), shotlist_md(m))
    errs = [i for i in m["issues"] if i[0] == "error"]
    for lv, w, msg in m["issues"]:
        print(f"{lv}: {w}: {msg}")
    print(f"\n{len(errs)} error(s); script version {m['version']}, about {m['total']:.0f} s -> script.md, shotlist.md")
    if errs:
        print("fix every error, then run this again. Don't film a script with an open error")
    else:
        print("next: show script.md and shotlist.md to the creator. They film; then write edit.json and run make_video.py")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    guard(main)
