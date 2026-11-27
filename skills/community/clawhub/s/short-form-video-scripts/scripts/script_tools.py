#!/usr/bin/env python3
"""Script tools for the short-form-video-scripts skill. Standard library only.

Commands
  budget    words that fit a target length at a speaking pace
  check     timing + lint report for a script JSON (hook length, pacing, CTA, text)
  srt       caption file (SRT) with timings estimated from word counts
  shotlist  shot list as CSV (or markdown) from the scenes

Timings are ESTIMATES from word counts and sentence pauses. When the real
voiceover exists, pass its length with --audio-seconds so SRT and shot list
stretch to match. Lint rules are heuristics from creator practice, not laws.
"""
import argparse
import csv
import json
import math
import os
import re
import sys

DEFAULT_WPM = 165
SENTENCE_PAUSE = 0.30   # seconds added after . ! ? ؟ ۔
CLAUSE_PAUSE = 0.12     # seconds added after , ; : —
HOOK_SECONDS = 3.0
HOOK_MAX_WORDS_SLOW = 12
SCENE_LONG_SECONDS = 8.0
SENTENCE_LONG_WORDS = 22
ONSCREEN_MAX_WORDS = 7
SAFE_SLACK = 0.10       # +-10% of target counts as on target

# Greeting openers that waste the first seconds, in English and in common Roman Urdu / Hindi forms
# ("today I...", "friends..."). Kept as data so scripts in those languages are checked too.
GREETINGS = re.compile(
    r"^\s*(hi|hello|hey|salam|assalam|asalam|aoa|namaste|welcome|what'?s up|"
    r"in this video|today i|aaj main|aaj hum|dosto|doston|guys)\b", re.I)
SENT_END = re.compile(r"[.!?؟۔]+[\"')\]]*$")
CLAUSE_END = re.compile(r"[,;:—–-]+$")
WORD = re.compile(r"[^\W_]+(?:['’][^\W_]+)*", re.UNICODE)


class ToolError(RuntimeError):
    pass


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def words_of(text):
    return WORD.findall(text or "")


def speech_seconds(text, wpm):
    """Estimated spoken duration: word time plus small pauses at punctuation."""
    toks = (text or "").split()
    if not toks:
        return 0.0
    n = sum(1 for t in toks if WORD.search(t))
    secs = n * 60.0 / wpm
    for t in toks:
        if SENT_END.search(t):
            secs += SENTENCE_PAUSE
        elif CLAUSE_END.search(t):
            secs += CLAUSE_PAUSE
    return secs


def load_script(path):
    try:
        with open(path, encoding="utf-8-sig") as f:
            data = json.load(f)
    except OSError as e:
        raise ToolError(f"Cannot read {path}: {e}") from None
    except ValueError as e:
        raise ToolError(f"{path} is not valid JSON: {e}") from None
    scenes = data.get("scenes") if isinstance(data, dict) else None
    if not isinstance(scenes, list) or not scenes:
        raise ToolError("Script JSON needs a non-empty 'scenes' list (see references/output-templates.md).")
    for i, s in enumerate(scenes, 1):
        if not isinstance(s, dict):
            raise ToolError(f"Scene {i} must be an object.")
    return data


def scene_text(s, key):
    v = s.get(key)
    return v.strip() if isinstance(v, str) else ""


def timeline(data, wpm_override=None, audio_seconds=None):
    """Return scenes with start/end seconds. Estimated first, then scaled to the audio length."""
    wpm = float(wpm_override or data.get("wpm") or DEFAULT_WPM)
    if wpm <= 0:
        raise ToolError("wpm must be positive.")
    rows, t = [], 0.0
    for i, s in enumerate(data["scenes"], 1):
        vo = scene_text(s, "voiceover")
        override = s.get("seconds")
        if isinstance(override, (int, float)) and override > 0:
            dur, fixed = float(override), True
        else:
            dur, fixed = speech_seconds(vo, wpm), False
            if dur == 0:
                dur = 1.5  # silent scene with no override: assume a short beat
        rows.append({"n": i, "scene": s, "voiceover": vo, "dur": dur, "fixed": fixed,
                     "words": len(words_of(vo))})
    if audio_seconds:
        if audio_seconds <= 0:
            raise ToolError("--audio-seconds must be positive.")
        fixed_total = sum(r["dur"] for r in rows if r["fixed"])
        flex = [r for r in rows if not r["fixed"]]
        flex_total = sum(r["dur"] for r in flex)
        if flex and flex_total > 0 and audio_seconds > fixed_total:
            k = (audio_seconds - fixed_total) / flex_total
            for r in flex:
                r["dur"] *= k
        else:
            k = audio_seconds / sum(r["dur"] for r in rows)
            for r in rows:
                r["dur"] *= k
    for r in rows:
        r["start"], r["end"] = t, t + r["dur"]
        t = r["end"]
    return rows, t, wpm


def ts_srt(sec):
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def ts_short(sec):
    m, s = divmod(sec, 60)
    return f"{int(m)}:{s:04.1f}"


def write_text(path, text):
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


# --------------------------------------------------------------------------
# budget
# --------------------------------------------------------------------------
def cmd_budget(a):
    print(f"Words that fit at {a.wpm} wpm (range = -10% slower .. +10% faster):")
    print(f"{'seconds':>8} {'words (typical)':>16} {'range':>12}")
    for sec in a.seconds:
        if sec <= 0:
            raise ToolError("seconds must be positive.")
        typ = sec * a.wpm / 60
        print(f"{sec:>8} {round(typ):>16} {round(typ * 0.9):>6}-{round(typ * 1.1):<5}")
    print("\nThe typical figure already assumes natural pauses; a punchy voiceover with many sentence "
          "breaks fits slightly fewer words. Run 'check' for an exact estimate.")


# --------------------------------------------------------------------------
# check
# --------------------------------------------------------------------------
def cmd_check(a):
    data = load_script(a.script)
    rows, total, wpm = timeline(data, a.wpm, a.audio_seconds)
    target = a.target or data.get("target_seconds")
    if target is not None and (not isinstance(target, (int, float)) or target <= 0):
        raise ToolError("target seconds must be a positive number.")
    findings = []  # (level, message)

    def warn(msg):
        findings.append(("WARN", msg))

    def info(msg):
        findings.append(("INFO", msg))

    # total vs target
    if target:
        diff = total - target
        pct = 100 * diff / target
        if abs(diff) <= target * SAFE_SLACK:
            info(f"Total {total:.1f}s is on target ({target:.0f}s, {pct:+.0f}%).")
        elif diff > 0:
            warn(f"Total {total:.1f}s is {diff:.1f}s over the {target:.0f}s target "
                 f"(about {math.ceil(diff * wpm / 60)} words to cut).")
        else:
            warn(f"Total {total:.1f}s is {-diff:.1f}s under the {target:.0f}s target "
                 f"(room for about {math.floor(-diff * wpm / 60)} more words, or tighten the target).")

    # hook: first 3 seconds of speech
    first = rows[0]
    hook_words = words_of(first["voiceover"])
    hook_text = first["voiceover"]
    if not hook_words and not first["fixed"]:
        warn("Scene 1 has no voiceover; with no spoken hook, the on-screen text and visual must carry the first 3 seconds.")
    else:
        if GREETINGS.search(hook_text):
            warn("The script opens with a greeting or setup phrase; start with the claim, result or action instead.")
        in_hook = 0.0
        count = 0
        for tok in hook_text.split():
            in_hook += (60.0 / wpm) if WORD.search(tok) else 0.0
            if SENT_END.search(tok):
                in_hook += SENTENCE_PAUSE
            count += 1 if WORD.search(tok) else 0
            if in_hook >= HOOK_SECONDS:
                break
        first_sentence = re.split(r"(?<=[.!?؟۔])\s+", hook_text.strip(), maxsplit=1)[0]
        fs_words = len(words_of(first_sentence))
        fs_secs = speech_seconds(first_sentence, wpm)
        if fs_secs > HOOK_SECONDS + 1.5 or fs_words > HOOK_MAX_WORDS_SLOW:
            warn(f"First sentence is {fs_words} words (~{fs_secs:.1f}s). Aim for a hook that lands in about "
                 f"{HOOK_SECONDS:.0f}s (around 8 words); the first sentence should state the promise.")
        else:
            info(f"Hook sentence: {fs_words} words (~{fs_secs:.1f}s).")
    if not scene_text(first["scene"], "on_screen_text"):
        warn("Scene 1 has no on-screen text; many viewers watch muted, so show the hook in text too.")
    if not scene_text(first["scene"], "visual") and not scene_text(first["scene"], "camera"):
        warn("Scene 1 has no visual or camera note; the hook needs something moving on screen.")

    # per-scene checks
    last_change = 0.0
    for r in rows:
        s = r["scene"]
        n = r["n"]
        vo = r["voiceover"]
        if r["dur"] > SCENE_LONG_SECONDS and not r["fixed"]:
            warn(f"Scene {n} runs ~{r['dur']:.1f}s with no cut; add a visual change or pattern interrupt "
                 f"(a change every 3 to 5 seconds suits videos up to a minute).")
        for sent in re.split(r"(?<=[.!?؟۔])\s+", vo):
            wc = len(words_of(sent))
            if wc > SENTENCE_LONG_WORDS:
                warn(f"Scene {n}: a sentence has {wc} words; split it so it sounds spoken, not written.")
        ost = scene_text(s, "on_screen_text")
        if ost and len(words_of(ost)) > ONSCREEN_MAX_WORDS:
            warn(f"Scene {n}: on-screen text has {len(words_of(ost))} words; keep it to {ONSCREEN_MAX_WORDS} or fewer.")
        if vo and not any(scene_text(s, k) for k in ("visual", "broll", "camera")):
            warn(f"Scene {n} has voiceover but no visual, B-roll or camera note.")
        if r["words"] == 0 and not r["fixed"] and not ost:
            warn(f"Scene {n} has no voiceover, no on-screen text and no duration override.")

    # repeated words/phrases (simple redundancy hint)
    all_vo = " ".join(r["voiceover"] for r in rows).lower()
    toks = [w for w in words_of(all_vo) if len(w) > 3]
    trigrams = {}
    for i in range(len(toks) - 2):
        g = " ".join(toks[i:i + 3])
        trigrams[g] = trigrams.get(g, 0) + 1
    repeated = [g for g, c in trigrams.items() if c >= 2]
    if repeated:
        warn(f"Repeated phrase(s) may be filler: {', '.join(repr(g) for g in repeated[:3])}.")

    # CTA
    cta_idx = [r["n"] for r in rows if r["scene"].get("cta") is True]
    if not cta_idx:
        warn("No scene is marked as the CTA (set \"cta\": true on it). Every video needs one clear action.")
    else:
        if len(cta_idx) > 1:
            warn(f"{len(cta_idx)} scenes are marked as CTA ({cta_idx}); use one primary action.")
        if cta_idx[-1] < len(rows) - 1:
            warn(f"The CTA is scene {cta_idx[-1]} of {len(rows)}; place it after the payoff, near the end.")
        cta_start = next(r["start"] for r in rows if r["n"] == cta_idx[0])
        if total > 0 and cta_start / total < 0.6:
            warn(f"The CTA starts at {cta_start:.1f}s ({100 * cta_start / total:.0f}% of the video); deliver the "
                 f"value first, then ask.")

    # re-hook for longer videos
    if total >= 45 and len(rows) < 5:
        warn(f"A {total:.0f}s video has only {len(rows)} scenes; add beats or a mid-video re-hook to hold attention.")

    warns = [m for lvl, m in findings if lvl == "WARN"]
    wcount = sum(r["words"] for r in rows)
    print(f"Script: {data.get('title', os.path.basename(a.script))}")
    print(f"Scenes {len(rows)} | words {wcount} | estimated length {total:.1f}s at {wpm:.0f} wpm"
          + (f" (scaled to audio {a.audio_seconds:.1f}s)" if a.audio_seconds else ""))
    print(f"\n{'#':>2} {'start':>6} {'end':>6} {'dur':>5} {'words':>5}  voiceover")
    for r in rows:
        mark = "*" if r["scene"].get("cta") is True else " "
        print(f"{r['n']:>2} {r['start']:>6.1f} {r['end']:>6.1f} {r['dur']:>5.1f} {r['words']:>5} {mark} "
              f"{r['voiceover'][:70]}")
    print("\n(* = CTA scene)\n")
    for lvl, msg in findings:
        print(f"[{lvl}] {msg}")
    print(f"\n{len(warns)} warning(s). These are heuristics; the real retention graph has the final word.")
    if a.json:
        report = {"title": data.get("title"), "estimated_seconds": round(total, 2), "target_seconds": target,
                  "wpm": wpm, "words": wcount, "warnings": warns,
                  "scenes": [{"n": r["n"], "start": round(r["start"], 2), "end": round(r["end"], 2),
                              "words": r["words"], "voiceover": r["voiceover"]} for r in rows]}
        write_text(a.json, json.dumps(report, ensure_ascii=False, indent=2))
        print(f"Saved {a.json}", file=sys.stderr)
    return 1 if (a.strict and warns) else 0


# --------------------------------------------------------------------------
# srt
# --------------------------------------------------------------------------
def chunk_words(text, max_words):
    """Split into caption chunks of at most max_words, preferring breaks after punctuation."""
    toks = text.split()
    chunks, cur = [], []
    for t in toks:
        cur.append(t)
        end = bool(SENT_END.search(t) or CLAUSE_END.search(t))
        if len(cur) >= max_words or (end and len(cur) >= max(2, max_words // 2)):
            chunks.append(cur)
            cur = []
    if cur:
        if chunks and len(cur) == 1 and len(chunks[-1]) < max_words + 1:
            chunks[-1].extend(cur)   # avoid a one-word orphan caption
        else:
            chunks.append(cur)
    return [" ".join(c) for c in chunks]


def cmd_srt(a):
    if a.max_words < 1:
        raise ToolError("--max-words must be at least 1.")
    data = load_script(a.script)
    rows, total, wpm = timeline(data, a.wpm, a.audio_seconds)
    lines, idx = [], 1
    for r in rows:
        text = r["voiceover"].strip()
        if not text:
            continue
        chunks = chunk_words(text, a.max_words)
        weights = [max(len(words_of(c)), 1) for c in chunks]
        wsum = sum(weights)
        t = r["start"]
        for c, w in zip(chunks, weights):
            d = r["dur"] * w / wsum
            end = min(t + d, r["end"])
            body = c.upper() if a.upper else c
            lines.append(f"{idx}\n{ts_srt(t)} --> {ts_srt(end)}\n{body}\n")
            idx += 1
            t = end
    if idx == 1:
        raise ToolError("No voiceover text found in the scenes, so there is nothing to caption.")
    write_text(a.out, "\n".join(lines))
    print(f"Wrote {idx - 1} captions to {a.out} (estimated length {total:.1f}s).")
    print("Timings are estimated from word counts. Re-check them against the real voiceover in your editor, "
          "or pass --audio-seconds with the recording's length.")
    return 0


# --------------------------------------------------------------------------
# shotlist
# --------------------------------------------------------------------------
COLS = ["shot", "start_s", "end_s", "duration_s", "voiceover", "on_screen_text", "visual", "camera",
        "broll", "sfx", "cta"]


def cmd_shotlist(a):
    data = load_script(a.script)
    rows, total, wpm = timeline(data, a.wpm, a.audio_seconds)
    out = []
    for r in rows:
        s = r["scene"]
        out.append({
            "shot": r["n"], "start_s": round(r["start"], 1), "end_s": round(r["end"], 1),
            "duration_s": round(r["dur"], 1), "voiceover": r["voiceover"],
            "on_screen_text": scene_text(s, "on_screen_text"), "visual": scene_text(s, "visual"),
            "camera": scene_text(s, "camera"), "broll": scene_text(s, "broll"),
            "sfx": scene_text(s, "sfx"), "cta": "yes" if s.get("cta") is True else "",
        })
    base = a.out
    parent = os.path.dirname(base)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(base + ".csv", "w", newline="", encoding="utf-8-sig") as f:   # BOM so spreadsheets read Urdu text
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(out)
    msg = f"Wrote {base}.csv ({len(out)} shots, ~{total:.1f}s)"
    if a.md:
        def cell(v):
            return str(v).replace("|", "\\|").replace("\n", " ")
        md = ["| " + " | ".join(COLS) + " |", "|" + "---|" * len(COLS)]
        for o in out:
            md.append("| " + " | ".join(cell(o[c]) for c in COLS) + " |")
        write_text(base + ".md", "\n".join(md) + "\n")
        msg += f" and {base}.md"
    print(msg + ".")
    return 0


# --------------------------------------------------------------------------
def build_parser():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    def timing_args(sp):
        sp.add_argument("--wpm", type=float, help=f"speaking pace (default: script's wpm, else {DEFAULT_WPM})")
        sp.add_argument("--audio-seconds", type=float, help="length of the real voiceover; stretches the timeline")

    b = sub.add_parser("budget", help="word budget for target lengths")
    b.add_argument("--seconds", type=float, nargs="+", default=[15, 30, 60, 90])
    b.add_argument("--wpm", type=float, default=DEFAULT_WPM)
    b.set_defaults(fn=cmd_budget)

    c = sub.add_parser("check", help="timing and lint report")
    c.add_argument("script")
    c.add_argument("--target", type=float, help="target length in seconds (default: script's target_seconds)")
    c.add_argument("--json", help="also save the report as JSON")
    c.add_argument("--strict", action="store_true", help="exit with code 1 if there are warnings")
    timing_args(c)
    c.set_defaults(fn=cmd_check)

    s = sub.add_parser("srt", help="SRT captions")
    s.add_argument("script")
    s.add_argument("--out", required=True)
    s.add_argument("--max-words", type=int, default=4, help="words per caption (default 4)")
    s.add_argument("--upper", action="store_true", help="UPPERCASE captions")
    timing_args(s)
    s.set_defaults(fn=cmd_srt)

    sh = sub.add_parser("shotlist", help="shot list CSV (and optional markdown)")
    sh.add_argument("script")
    sh.add_argument("--out", required=True, help="base path without extension")
    sh.add_argument("--md", action="store_true", help="also write a markdown table")
    timing_args(sh)
    sh.set_defaults(fn=cmd_shotlist)
    return p


def main(argv=None):
    a = build_parser().parse_args(argv)
    try:
        return a.fn(a) or 0
    except ToolError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
