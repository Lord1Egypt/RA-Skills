#!/usr/bin/env python3
"""Edit what the creator filmed into one vertical video per account: the layout the brief asks for,
pauses trimmed, word-by-word captions, the hook, the disclosure from the first frame, and each
account opening its own way.

    python3 scripts/make_video.py edit.json --out videos            # render every video
    python3 scripts/make_video.py edit.json --out videos --width 540 # smaller files (drafts, examples)
    python3 scripts/make_video.py edit.json --placeholder           # before filming: a labelled placeholder
                                                                    #   where the creator's recording goes

edit.json (references/edit-file.md):
{
  "campaign": "campaign.json", "script": "script.json",
  "music": {"source": "none"},                    # or {"source": "licensed", "file": ..., "license": ..., "volume": 0.12}
  "style": {"accent": "#FFD43B"},
  "videos": [
    {"id": "tiktok", "account": "TikTok", "layout": "split_screen",
     "creator": "takes/creator.mp4", "transcript": "work/transcript.json",
     "hook_take": "takes/hook-h1.mp4", "supplied": "orbit-footage.mp4", "supplied_start": 0},
    {"id": "shorts", "account": "Shorts", "layout": "face_screen",
     "creator": "takes/creator.mp4", "transcript": "work/transcript.json", "screen": "takes/screen.mp4"}
  ]
}

Layouts (1080x1920):
  talking_head     the creator's take fills the frame.
  split_screen     the footage the brand supplied in one half (the brief's "position", top by
                   default), the creator in the other. The supplied footage is muted unless the
                   video sets "supplied_audio": "duck" (its sound under the creator's voice, back up
                   in the gaps) or "keep" (both at full level).
  face_screen      the screen recording on top (whole screen, on a dark backdrop), the creator below.
  broll_voiceover  the creator's b-roll shots in order under the creator's own voiceover.

The hook comes from the script: the hook that opens this account ("openings" in script.json). With a
"hook_take" (the creator saying that hook, with "hook_transcript", transcribe.py's transcript of it)
the video starts with it, and its words are captioned and checked like the rest; the hook text shows
on screen for the first seconds either way. Captions come from transcribe.py's transcript of the take (or the
voiceover); pauses over 0.45 s and fillers ("um", "uh") are trimmed. The campaign's on-screen
disclosure is drawn from the first frame for its seconds. A campaign with "burned_text": "none" (clean
footage) gets no captions, no hook text and no label on the video; "disclosure_only" keeps the label
alone. A video can also turn off "captions" or "hook_text" itself.

Never generates or alters a face or a voice: no avatars, no voice changes, no lip sync, no face
filters. Never changes speed, mirrors or filters a video to make a copy look new: each account gets
its own opening instead.

--placeholder renders a clearly labelled "your recording goes here" panel for any creator take that
isn't there yet, silent, with the script's lines as captions at a natural pace: a layout preview
before filming. check_videos.py never lets a placeholder video be posted (the skill's own example
excepted, which posts nothing).

Writes videos/<id>.mp4 (H.264, AAC, -14 LUFS), a cover frame each, contact-sheet.jpg and
manifest.json (each video's fingerprint, inputs, hook, what is on screen, when the disclosure is
said). Needs ffmpeg with libx264 and Pillow.
"""
import argparse, functools, json, os, re, shutil, subprocess, sys, tempfile

sys.dont_write_bytecode = True   # nothing is ever written into the skill's own folder
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import campaign as campaign_mod  # noqa: E402
import script as script_mod  # noqa: E402
from ugclib import (die, disclosure_targets, guard, is_num, probe as probe_file, read_json, rel, sha256,  # noqa: E402
                    split_sentences, spoken_disclosure_at, user_home, words_of)

W, H = 1080, 1920
SAFE_CX = W // 2
CAP_SIZE = 84
CAP_MAX_W = 760
HOOK_SIZE = 70
HOOK_SECONDS = 3.0
DISC_SIZE = 36
DISC_TOP = 300          # below TikTok's Following/For You tabs and the Reels header
DISC_LEFT = 64          # a compact pill in the top-left corner, clear of the hook in the middle
SAFE_TOP = 420
FONT_DIR = os.path.join(HERE, "..", "fonts")
FONT_FILES = ["Poppins-ExtraBold.ttf", "Poppins-Bold.ttf"]
FONT_URL = "https://raw.githubusercontent.com/google/fonts/main/ofl/poppins/"
LAYOUTS = ("talking_head", "split_screen", "face_screen", "broll_voiceover")
SUPPLIED_AUDIO = ("mute", "duck", "keep")
FILLERS = {"um", "uh", "uhm", "erm", "hmm", "mm"}
FUNCTION_WORDS = {"a", "an", "the", "of", "to", "for", "and", "that", "with", "on", "in", "is", "so", "but", "i", "or",
                  "at", "as", "if", "by", "from", "my", "your", "our"}
SPLIT_Y = 960           # split screen: the line between the halves
FACE_SCREEN_Y = 1152    # face plus screen: the screen recording above, the creator below
WARNINGS = []


def warn(msg):
    WARNINGS.append(msg)
    print("warning: " + msg, file=sys.stderr)


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)
    if r.returncode != 0:
        die("ffmpeg failed: " + (r.stderr.strip().splitlines() or ["no message"])[-1][-600:])
    return r.stdout


def load_pillow():
    try:
        from PIL import Image, ImageDraw, ImageFont
        return Image, ImageDraw, ImageFont
    except ImportError:
        die("editing needs Pillow: pip install pillow (python3 scripts/check_setup.py checks everything)")
    ver = tuple(int(x) for x in re.findall(r"\d+", getattr(__import__("PIL"), "__version__", "0"))[:2])
    if ver < (10, 1) and not getattr(load_pillow, "_warned", False):
        load_pillow._warned = True
        warn(f"Pillow {'.'.join(map(str, ver))} is older than 10.1; text may render with a fallback font. pip install -U "
             "pillow")


@functools.lru_cache(maxsize=None)
def font(size):
    _, _, ImageFont = load_pillow()
    cache = os.path.join(user_home(), "fonts")   # never written into the skill's own folder
    for d in (FONT_DIR, cache):
        for name in FONT_FILES:
            path = os.path.join(d, name)
            if os.path.exists(path) and os.path.getsize(path) > 10000:
                return ImageFont.truetype(path, size)
    os.makedirs(cache, exist_ok=True)
    path = os.path.join(cache, FONT_FILES[0])
    try:  # some skill registries strip binary files; fetch the open-licensed font once
        import urllib.request
        urllib.request.urlretrieve(FONT_URL + FONT_FILES[0], path)
    except Exception:
        pass
    if os.path.exists(path) and os.path.getsize(path) > 10000:
        return ImageFont.truetype(path, size)
    warn("caption font missing; using Pillow's default font")
    return ImageFont.load_default(size)


@functools.lru_cache(maxsize=None)
def _measure():
    Image, ImageDraw, _ = load_pillow()
    return ImageDraw.Draw(Image.new("RGBA", (10, 10)))


def text_w(text, size):
    return _measure().textlength(text, font=font(size))


def hexrgb(h):
    h = str(h).lstrip("#")
    try:
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return (255, 212, 59)


def wrap(words, size, max_w):
    lines, cur = [], []
    for w in words:
        if cur and text_w(" ".join(cur + [w]), size) > max_w:
            lines.append(cur)
            cur = [w]
        else:
            cur.append(w)
    if cur:
        lines.append(cur)
    return lines


# ---------- speech: words, trimmed spans, output times ----------

def clean(w):
    return re.sub(r"[^\w']", "", w.lower())


def select_words(words, a, b):
    """(word, removed) inside [a, b]: fillers and stutters removed, word ends capped so a long silence
    the transcriber stretched over a word counts as a pause."""
    ws = [dict(w) for w in words if w["start"] >= a - 0.05 and w["end"] <= b + 0.15]
    out = []
    for i, w in enumerate(ws):
        w["end"] = min(w["end"], w["start"] + max(0.10 + 0.075 * len(clean(w["w"])), 0.12))
        c = clean(w["w"])
        nxt = clean(ws[i + 1]["w"]) if i + 1 < len(ws) else None
        out.append((w, c in FILLERS or (bool(c) and c == nxt)))
    return out


def keep_spans(marked, a, b, tighten=True):
    """Spans of the take to keep: pauses over 0.45 s and removed words become cuts."""
    if not any(not r for _, r in marked):
        return [(a, b)]
    pad, max_gap = 0.12, (0.45 if tighten else 99)
    spans, cur, prev_removed = [], None, False
    for w, r in marked:
        if r:
            prev_removed = True
            continue
        if cur is None:
            cur = [max(a, w["start"] - pad), w["end"]]
        elif prev_removed or w["start"] - cur[1] > max_gap:
            spans.append((cur[0], cur[1] + pad))
            cur = [w["start"] - pad, w["end"]]
        else:
            cur[1] = max(cur[1], w["end"])
        prev_removed = False
    spans.append((cur[0], min(b, cur[1] + 0.3)))
    merged = []
    for s, e in spans:
        if merged and s <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], e))
        else:
            merged.append((s, e))
    return [(s, e) for s, e in merged if e - s > 0.15]


def to_out(t, spans, offset=0.0):
    acc = 0.0
    for s, e in spans:
        if t <= s:
            return offset + acc
        if t <= e:
            return offset + acc + (t - s)
        acc += e - s
    return offset + acc


def _tokens(text):
    return [t for t in (clean(x) for x in str(text).split()) if t]


def _attempts(stream, toks):
    """Every try at saying toks in the word stream: [(first index, last index, share of words said)].
    A try starts where the line's first words are said and follows the line word by word, allowing
    a stray word; it ends at the line's end or where the speaker stops following it."""
    n = len(toks)
    head = toks[:min(2, n)]
    out = []
    for i in range(len(stream)):
        if stream[i:i + len(head)] != head:
            continue
        p, j, last, misses = 0, i, i, 0
        while j < len(stream) and p < n and misses <= 2:
            if stream[j] == toks[p]:
                p, last, misses = p + 1, j, 0
            elif p + 1 < n and stream[j] == toks[p + 1]:
                p, last, misses = p + 2, j, 0
            else:
                misses += 1
            j += 1
        out.append((i, last, p / n))
    return out


def assemble(words, pieces):
    """The last complete try of each piece (the hook, then every script line), in script order.
    pieces: [(name, text, required)]. Returns ({name: (first word, last word)}, missing names).
    A try is complete when 70% or more of its words were said. Working back from the last line,
    each line takes its last complete try that ends before the next line's chosen try starts, so
    restarts and flubs are dropped and the order stays the script's."""
    stream = [clean(w["w"]) for w in words]
    chosen, missing = {}, []
    limit = len(stream)
    for name, text, required in reversed(pieces):
        toks = _tokens(text)
        tries = [(a, b) for a, b, share in _attempts(stream, toks) if share >= 0.7 and b < limit] if toks else []
        if not tries:
            if required:
                missing.append(name)
            continue
        a, b = tries[-1]
        chosen[name] = (a, b)
        limit = a
    return chosen, missing


def script_words(lines, wps, start=0.0):
    """Words with times at a natural pace, for a placeholder: where the creator's words will appear."""
    out, t = [], start
    for ln in lines:
        for w in ln.split():
            d = max(0.18, len(clean(w)) / (wps * 4.6))
            out.append({"w": w, "start": round(t, 3), "end": round(t + d * 0.9, 3)})
            t += 1.0 / wps
        t += 0.25
    return out, t


def caption_groups(kept):
    """Up to 3 words per caption, broken at punctuation and pauses; never ending on "the" or "of"."""
    groups, cur = [], []
    for i, w in enumerate(kept):
        cur.append(w)
        nxt = kept[i + 1] if i + 1 < len(kept) else None
        too_wide = nxt is not None and text_w(" ".join(x["w"] for x in cur + [nxt]), CAP_SIZE) > CAP_MAX_W
        brk = nxt is None or len(cur) >= 3 or w["w"][-1:] in ".?!,;:" or too_wide or nxt["start"] - w["end"] > 0.25
        if brk and nxt is not None and clean(w["w"]) in FUNCTION_WORDS and w["w"][-1:] not in ".?!,;:" and len(cur) > 1:
            groups.append(cur[:-1])
            cur = [cur[-1]]
            continue
        if brk:
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    return [g for g in groups if g]


# ---------- overlays ----------

def render_overlay(path, cap_words, hook, style, cap_y, hook_top, disclosure, label):
    """One transparent 1080x1920 frame: the disclosure at the top, the hook, the caption (the spoken
    word in the accent colour) and, for the skill's own example, its label."""
    Image, ImageDraw, _ = load_pillow()
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    if disclosure:
        f = font(DISC_SIZE)
        tw = text_w(disclosure, DISC_SIZE)
        bw, bh = tw + 48, int(DISC_SIZE * 1.18) + 26
        x0 = DISC_LEFT if bw < W / 2 else SAFE_CX - bw / 2
        draw.rounded_rectangle([x0, DISC_TOP, x0 + bw, DISC_TOP + bh], bh // 2, fill=(0, 0, 0, 215))
        draw.text((x0 + bw / 2, DISC_TOP + bh / 2), disclosure, font=f, fill=(255, 255, 255, 255), anchor="mm")
    if label:
        # the skill's own example: a second corner pill, opposite the "Ad" one, so the frame looks like a real video
        f = font(30)
        tw = text_w(label, 30)
        bh = int(DISC_SIZE * 1.18) + 26
        x1 = W - DISC_LEFT - 96   # clear of the platform's right-hand buttons' column top
        draw.rounded_rectangle([x1 - tw - 40, DISC_TOP, x1, DISC_TOP + bh], bh // 2, fill=(0, 0, 0, 170))
        draw.text((x1 - (tw + 40) / 2, DISC_TOP + bh / 2), label, font=f, fill=(255, 255, 255, 235), anchor="mm")
    accent = hexrgb(style.get("accent", "#FFD43B"))
    if hook:
        lines = wrap(hook.split(), HOOK_SIZE, 760)
        f = font(HOOK_SIZE)
        lh = int(HOOK_SIZE * 1.2)
        bh = lh * len(lines) + 48
        bw = max(text_w(" ".join(x), HOOK_SIZE) for x in lines) + 72
        x0 = SAFE_CX - bw / 2
        draw.rounded_rectangle([x0, hook_top, x0 + bw, hook_top + bh], 24, fill=(255, 255, 255, 255))
        for i, ln in enumerate(lines):
            draw.text((SAFE_CX, hook_top + 24 + i * lh + lh / 2), " ".join(ln), font=f, fill=(0, 0, 0, 255), anchor="mm")
    if cap_words:
        f = font(CAP_SIZE)
        space = text_w(" ", CAP_SIZE)
        total = sum(text_w(w, CAP_SIZE) for w, _ in cap_words) + space * (len(cap_words) - 1)
        x = SAFE_CX - total / 2
        y = cap_y - int(CAP_SIZE * 0.6)
        for w, active in cap_words:
            fill = accent + (255,) if active else (255, 255, 255, 255)
            draw.text((x, y + 6), w, font=f, fill=(0, 0, 0, 140))
            draw.text((x, y), w, font=f, fill=fill, stroke_width=8, stroke_fill=(0, 0, 0, 255))
            x += text_w(w, CAP_SIZE) + space
    img.save(path, optimize=True)


def build_overlays(vid, timed_words, length, style, layout, screen, label, hook, tmp):
    """PNG overlays plus an ffmpeg concat list that shows each for the right time."""
    cap_y = {"split_screen": SPLIT_Y, "face_screen": FACE_SCREEN_Y}.get(layout, 1230)
    # face_screen: the hook sits over the creator, never over the screen recording it is about
    hook_top = FACE_SCREEN_Y + 70 if layout == "face_screen" else SAFE_TOP
    events = []
    groups = caption_groups(timed_words)
    for gi, g in enumerate(groups):
        nxt = groups[gi + 1][0]["start"] if gi + 1 < len(groups) else length
        for i, w in enumerate(g):
            end = g[i + 1]["start"] if i + 1 < len(g) else min(nxt, max(w["end"] + 0.1, g[0]["start"] + 0.4))
            if nxt - end < 0.15:
                end = nxt
            if end - w["start"] >= 0.02:
                events.append((w["start"], end, [(x["w"], j == i) for j, x in enumerate(g)]))
    hook_win = (0.0, min(HOOK_SECONDS, length)) if hook else None
    disc = screen.get("disclosure")
    disc_win = (0.0, min(float(screen.get("seconds") or 3), length)) if disc else None
    cuts = {0.0, length} | {t for s, e, _ in events for t in (s, e)}
    for win in (hook_win, disc_win):
        if win:
            cuts.add(win[1])
    cuts = sorted(x for x in cuts if 0 <= x <= length)
    rendered, listing = {}, []
    for a, b in zip(cuts, cuts[1:]):
        if b - a < 0.005:
            continue
        mid = (a + b) / 2
        cap = next((w for s, e, w in events if s <= mid < e), None)
        show_hook = hook if hook_win and mid < hook_win[1] else None
        show_disc = disc if disc_win and mid < disc_win[1] else None
        if show_hook:
            cap = None   # the hook has the screen to itself for its first seconds
        key = (tuple(cap) if cap else None, show_hook, show_disc)
        if key not in rendered:
            name = f"o-{vid}-{len(rendered):04d}.png"
            render_overlay(os.path.join(tmp, name), cap, show_hook, style, cap_y, hook_top, show_disc, label)
            rendered[key] = name
        listing.append((rendered[key], b - a))
    lst = f"overlays-{vid}.txt"
    with open(os.path.join(tmp, lst), "w", encoding="utf-8") as fh:
        fh.write("ffconcat version 1.0\n")
        for name, d in listing:
            fh.write(f"file '{name}'\nduration {d:.3f}\n")
        fh.write(f"file '{listing[-1][0]}'\n")
    return lst


def placeholder_png(path, w, h, what):
    """A clearly labelled panel where the creator's own recording goes. No person, no face."""
    Image, ImageDraw, _ = load_pillow()
    img = Image.new("RGB", (w, h), (34, 37, 43))
    d = ImageDraw.Draw(img)
    m = 40
    d.rounded_rectangle([m, m, w - m, h - m], 36, outline=(150, 156, 166), width=6)
    # a phone on a stand: where the camera is, not a person
    pw = min(w // 5, h // 4)
    ph = int(pw * 1.9)
    px, py = w // 2 - pw // 2, max(m + 20, h // 2 - 90 - ph)
    if py + ph < h // 2 - 70:
        d.rounded_rectangle([px, py, px + pw, py + ph], pw // 6, outline=(200, 204, 212), width=5)
        d.ellipse([w // 2 - 9, py + 18, w // 2 + 9, py + 36], fill=(200, 204, 212))
    title = "YOUR RECORDING GOES HERE"
    size = 60
    while text_w(title, size) > w - 2 * m - 80 and size > 30:
        size -= 4
    d.text((w // 2, h // 2 - 40), title, font=font(size), fill=(236, 236, 236), anchor="mm")
    sub = what
    d.text((w // 2, h // 2 + 40), sub, font=font(34), fill=(170, 176, 186), anchor="mm")
    img.save(path)


# ---------- the filter graph ----------

def fill(w, h):
    return f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},setsar=1"


def fit_on_dark(w, h):
    return (f"scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=0x101114,"
            "setsar=1")


def probe(path, sound_only=False):
    """Duration and whether there is sound. A voiceover may be sound alone (a voice memo)."""
    if not sound_only:
        return probe_file(path)
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type", "-of", "json", path],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    try:
        d = json.loads(r.stdout or "{}")
        dur = float((d.get("format") or {}).get("duration") or 0)
    except (ValueError, TypeError):
        d, dur = {}, 0.0
    kinds = {s.get("codec_type") for s in d.get("streams") or []}
    if "audio" not in kinds or dur <= 0:
        die(f"{os.path.basename(path)}: no sound in this file. The voiceover is your voice reading the script")
    return {"duration": round(dur, 3), "audio": True}


def render_video(v, c, script_m, spec, base, out_dir, tmp, width, placeholder):
    vid = v["id"]
    layout = v["layout"]
    hook_id = script_m["openings"].get(v["account"])
    hook = script_m["hooks"].get(hook_id) if hook_id else None
    for acc in v.get("accounts") or []:
        if script_m["openings"].get(acc) != hook_id:
            die(f"video {vid} goes to {', '.join(v['accounts'])}: one edit has one opening, and script.json opens "
                f"{acc} with {script_m['openings'].get(acc)}, not {hook_id}. Give them the same opening or separate videos")
    if not hook:
        die(f"video {vid}: script.json has no opening for account {v['account']} (\"openings\": {{\"{v['account']}\": "
            "\"h1\"}})")
    d = c.get("disclosure") or {}
    burned = campaign_mod.burned_text(c)
    show_caps = burned == "any" and v.get("captions", spec.get("captions", True)) is not False
    show_hook = burned == "any" and v.get("hook_text", spec.get("hook_text", True)) is not False
    screen = {"disclosure": d.get("on_screen") if burned != "none" else None, "seconds": d.get("on_screen_seconds") or 3}
    label = "EXAMPLE: not a real ad" if campaign_mod.example_demo(c) else None
    style = spec.get("style") if isinstance(spec.get("style"), dict) else {}
    wps = script_m["wps"]

    def path_of(key):
        p = v.get(key)
        if not isinstance(p, str) or not p:
            return None
        return p if os.path.isabs(p) else os.path.join(base, p)

    inputs, used = [], {}
    # the voice track: the creator's take (or the voiceover), with its words
    voice_key = "voiceover" if layout == "broll_voiceover" else "creator"
    voice = path_of(voice_key)
    is_placeholder = False
    if not voice or not os.path.isfile(voice):
        if not placeholder:
            die(f"video {vid}: {v.get(voice_key) or voice_key} not found. Film it first (shotlist.md), or run with "
                "--placeholder for a layout preview")
        is_placeholder = True
    hook_take = path_of("hook_take")
    if hook_take and not os.path.isfile(hook_take):
        if not placeholder:
            die(f"video {vid}: hook take {v.get('hook_take')} not found")
        hook_take = None
    hook_words = []
    spoken = [r["say"] for r in script_m["spoken"]]
    offset = 0.0
    dropped, line_src, hook_in_take, cut_runs = [], {}, False, []
    tr_sha = None
    if is_placeholder:
        words, total = script_words([hook] + spoken, wps)
        spans = [(0.0, total)]
        voice_len = total
        kept_src = words
    else:
        info = probe(voice, layout == "broll_voiceover")
        used[voice_key] = {"file": rel(voice, base), "sha256": sha256(voice)}
        tp = path_of("transcript")
        if tp is None:
            die(f"video {vid}: \"transcript\": run transcribe.py on {v.get(voice_key)} and name work/transcript.json, so "
                "the captions are your own words")
        tr = read_json(tp, "the transcript")
        words = tr.get("words") if isinstance(tr, dict) else None
        if not isinstance(words, list) or not words:
            die(f"{rel(tp)} has no words. Run transcribe.py on {v.get(voice_key)} again")
        # the transcript must describe this exact take
        tr_sha = tr.get("video_sha256")
        if tr_sha != used[voice_key]["sha256"]:
            die(f"video {vid}: {rel(tp)} " + ("has no fingerprint of the take it describes" if not tr_sha else
                f"was made from another file, not {v.get(voice_key)}") + f". Run transcribe.py {v.get(voice_key)} again, "
                "so the captions and the checks read what this take says")
        if is_num(tr.get("duration")) and abs(float(tr["duration"]) - info["duration"]) > 0.5:
            die(f"video {vid}: {rel(tp)} is {tr['duration']:.1f} s long and {v.get(voice_key)} {info['duration']:.1f} s. "
                "Run transcribe.py on the take again")
        used["transcript"] = {"file": rel(tp, base), "sha256": sha256(tp)}
        tighten = v.get("trim_silence", True) is not False
        if v.get("assemble", spec.get("assemble", True)) is not False and layout != "broll_voiceover":
            # with a hook take, the hook comes from that take, never a second time from this one
            pieces = ([] if hook_take else [("hook", hook, False)]) + [(r["id"], r["say"], True)
                                                                       for r in script_m["spoken"]]
            chosen, missing = assemble(words, pieces)
            if missing:
                die(f"video {vid}: {', '.join(missing)} not found in {v.get(voice_key)} (no try with 70% of the line's "
                    "words). Film the line, or say it closer to the script, or set \"assemble\": false on this video to "
                    "keep the take as it is (the checks still read every word)")
            spans, keep_idx = [], set()
            order = [n for n, _, _ in pieces if n in chosen]
            hook_in_take = "hook" in chosen
            for name in order:
                a_i, b_i = chosen[name]
                keep_idx.update(range(a_i, b_i + 1))
                a_t, b_t = words[a_i]["start"], words[b_i]["end"]
                seg = keep_spans(select_words(words, a_t, b_t), a_t, b_t, tighten)
                spans += seg
                line_src[name] = (a_t, b_t)
            drop_i = [i for i, w in enumerate(words) if i not in keep_idx and clean(w["w"]) not in FILLERS]
            dropped = [words[i]["w"] for i in drop_i]
            for i in drop_i:
                if cut_runs and cut_runs[-1][-1][0] == i - 1 and not str(cut_runs[-1][-1][1]).endswith((".", "?", "!")):
                    cut_runs[-1].append((i, words[i]["w"]))
                else:
                    cut_runs.append([(i, words[i]["w"])])
            marked = [(w, r) for w, r in select_words(words, 0.0, info["duration"])
                      if any(s - 0.05 <= w["start"] and w["end"] <= e + 0.2 for s, e in spans)]
        else:
            marked = select_words(words, 0.0, info["duration"])
            spans = keep_spans(marked, 0.0, info["duration"], tighten)
        if hook_take:
            hinfo = probe(hook_take)
            offset = hinfo["duration"]
            used["hook_take"] = {"file": rel(hook_take, base), "sha256": sha256(hook_take)}
            # what the hook take says is read like the rest: captioned, timed and checked
            htp = path_of("hook_transcript")
            if htp is None:
                die(f"video {vid}: \"hook_transcript\": run transcribe.py on {v.get('hook_take')} and name its transcript, "
                    "so what the hook take says is captioned and checked like the rest")
            htr = read_json(htp, "the hook take's transcript")
            if not isinstance(htr, dict) or htr.get("video_sha256") != used["hook_take"]["sha256"]:
                die(f"video {vid}: {rel(htp)} was not made from {v.get('hook_take')}. Run transcribe.py on the hook take "
                    "again")
            hw = htr.get("words")
            if not isinstance(hw, list) or not hw:
                die(f"{rel(htp)} has no words. Run transcribe.py on {v.get('hook_take')} again")
            hook_words = [dict(w, start=min(float(w["start"]), offset), end=min(float(w["end"]), offset)) for w in hw
                          if isinstance(w, dict) and is_num(w.get("start")) and is_num(w.get("end"))
                          and clean(str(w.get("w", ""))) not in FILLERS]
            used["hook_transcript"] = {"file": rel(htp, base), "sha256": sha256(htp)}
        words = [dict(w, start=to_out(w["start"], spans, offset), end=to_out(w["end"], spans, offset))
                 for w, r in marked if not r]
        kept_src = words
        voice_len = sum(e - s for s, e in spans)
    length = offset + voice_len
    timed = hook_words + [w for w in words if w["end"] <= length + 0.05]
    cut = [x for x in (" ".join(str(w) for _, w in r_) for r_ in cut_runs) if words_of(x)]
    line_out = {k: (to_out(a_, spans, offset), to_out(b_, spans, offset)) for k, (a_, b_) in line_src.items()}

    # inputs
    graph = []
    args = []
    n = 0
    if is_placeholder:
        ph_w, ph_h = {"split_screen": (W, H // 2), "face_screen": (W, H - FACE_SCREEN_Y)}.get(layout, (W, H))
        ph = os.path.join(tmp, f"placeholder-{vid}.png")
        placeholder_png(ph, ph_w, ph_h, "EXAMPLE ONLY: no person in this demo" if label else "film it with shotlist.md")
        args += ["-loop", "1", "-framerate", "30", "-t", f"{length:.3f}", "-i", ph]
        graph.append(f"[{n}:v]fps=30,{fill(ph_w, ph_h) if layout != 'broll_voiceover' else fill(W, H)}[me]")
        graph.append(f"aevalsrc=0:c=stereo:s=48000:d={length:.3f}[voice]")
        n += 1
    else:
        args += ["-i", voice]
        vi = n
        n += 1
        parts, labels = [], []
        if hook_take:
            args += ["-i", hook_take]
            hi = n
            n += 1
            hinfo = probe(hook_take)
            if layout != "broll_voiceover":
                parts.append(f"[{hi}:v]fps=30,setpts=PTS-STARTPTS[hv]")
            parts.append(f"[{hi}:a]aresample=48000,asetpts=PTS-STARTPTS[ha]" if hinfo["audio"]
                         else f"aevalsrc=0:c=stereo:s=48000:d={hinfo['duration']:.3f}[ha]")
            labels.append(("[hv]" if layout != "broll_voiceover" else None, "[ha]"))
        vinfo = probe(voice, layout == "broll_voiceover")
        zoom = layout == "talking_head" and v.get("punch_in", True) is not False and len(spans) > 1
        vw, vh = (vinfo.get("width") or 0) // 2 * 2, (vinfo.get("height") or 0) // 2 * 2
        for i, (s, e) in enumerate(spans):
            if layout != "broll_voiceover":
                # a punch-in on every other cut hides the jump; it is a crop of the same take, not a new picture
                z = (f",crop=trunc(iw/1.08/2)*2:trunc(ih/1.08/2)*2,scale={vw}:{vh},setsar=1" if zoom and i % 2 and vw and vh
                     else "")
                parts.append(f"[{vi}:v]trim=start={s:.3f}:end={e:.3f},setpts=PTS-STARTPTS,fps=30{z},setsar=1[v{i}]")
            parts.append(f"[{vi}:a]atrim=start={s:.3f}:end={e:.3f},asetpts=PTS-STARTPTS,aresample=48000,"
                         f"afade=t=in:d=0.01,afade=t=out:st={max(0, e - s - 0.02):.3f}:d=0.02[a{i}]" if vinfo["audio"]
                         else f"aevalsrc=0:c=stereo:s=48000:d={e - s:.3f}[a{i}]")
            labels.append((f"[v{i}]" if layout != "broll_voiceover" else None, f"[a{i}]"))
        graph += parts
        if layout != "broll_voiceover":
            graph.append("".join(x + y for x, y in labels) + f"concat=n={len(labels)}:v=1:a=1[mev][voice]")
            mw, mh = {"split_screen": (W, H // 2), "face_screen": (W, H - FACE_SCREEN_Y)}.get(layout, (W, H))
            graph.append(f"[mev]{fill(mw, mh)}[me]")
        else:
            graph.append("".join(y for _, y in labels) + f"concat=n={len(labels)}:v=0:a=1[voice]")

    # the other picture: supplied footage, screen recording, b-roll
    if layout == "split_screen" and (v.get("supplied_audio") or "mute") != "mute":
        graph = [g.replace("[voice]", "[voice0]") for g in graph]
    if layout == "split_screen":
        sup = path_of("supplied")
        allowed = (c.get("supplied_footage") or {}).get("files") or []
        if not sup or not os.path.isfile(sup):
            die(f"video {vid}: \"supplied\": the footage the brand supplied ({', '.join(allowed) or 'see the brief'})")
        if allowed and os.path.basename(sup).casefold() not in {os.path.basename(x).casefold() for x in allowed}:
            die(f"video {vid}: {os.path.basename(sup)} isn't footage this campaign supplied ({', '.join(allowed)})")
        used["supplied"] = {"file": rel(sup, base), "sha256": sha256(sup)}
        start = float(v.get("supplied_start") or 0)
        args += ["-stream_loop", "-1", "-ss", f"{start:.3f}", "-i", sup]
        graph.append(f"[{n}:v]setpts=PTS-STARTPTS,fps=30,trim=duration={length:.3f},{fill(W, H // 2)}[them]")
        sup_audio = v.get("supplied_audio") or "mute"
        if sup_audio != "mute":
            if not probe(sup).get("audio"):
                die(f"video {vid}: \"supplied_audio\": \"{sup_audio}\", but {os.path.basename(sup)} has no sound")
            graph.append(f"[{n}:a]atrim=duration={length:.3f},asetpts=PTS-STARTPTS,aresample=48000,"
                         "aformat=channel_layouts=stereo[sup]")
            if sup_audio == "duck":
                # the brand's sound drops about 18 dB while the creator talks and comes back up in the gaps
                graph.append("[voice]asplit=2[vo1][vo2];[sup][vo2]sidechaincompress=threshold=0.015:ratio=20:attack=15:"
                             "release=350:makeup=1[supd];[vo1][supd]amix=inputs=2:duration=first:normalize=0[voice]"
                             .replace("[voice]asplit", "[voice0]asplit"))
            else:
                graph.append("[voice0][sup]amix=inputs=2:duration=first:normalize=0[voice]")
            used["supplied_audio"] = sup_audio
        n += 1
        pos = (c.get("supplied_footage") or {}).get("position") or "top"
        graph.append("[them][me]vstack[base0]" if pos == "top" else "[me][them]vstack[base0]")
    elif layout == "face_screen":
        scr = path_of("screen")
        if not scr or not os.path.isfile(scr):
            die(f"video {vid}: \"screen\": the screen recording (takes/screen.mp4)")
        used["screen"] = {"file": rel(scr, base), "sha256": sha256(scr)}
        args += ["-stream_loop", "-1", "-i", scr]
        graph.append(f"[{n}:v]setpts=PTS-STARTPTS,fps=30,trim=duration={length:.3f},{fit_on_dark(W, FACE_SCREEN_Y)}[them]")
        n += 1
        graph.append("[them][me]vstack[base0]")
    elif layout == "broll_voiceover":
        shots = [x if os.path.isabs(x) else os.path.join(base, x) for x in v.get("broll") or [] if isinstance(x, str)]
        if not shots or not all(os.path.isfile(x) for x in shots):
            die(f"video {vid}: \"broll\": the b-roll shots in script order, each a file you filmed")
        used["broll"] = [{"file": rel(x, base), "sha256": sha256(x)} for x in shots]
        each = length / len(shots)
        lab = []
        for i, x in enumerate(shots):
            args += ["-stream_loop", "-1", "-i", x]
            graph.append(f"[{n}:v]setpts=PTS-STARTPTS,fps=30,trim=duration={each:.3f},{fill(W, H)}[b{i}]")
            lab.append(f"[b{i}]")
            n += 1
        graph.append("".join(lab) + f"concat=n={len(lab)}:v=1:a=0[base0]")
    else:
        graph.append("[me]null[base0]")

    # inserts: a screen recording or product shot over the line that describes it
    product_at = 0.0 if layout in ("split_screen", "face_screen", "broll_voiceover") else None
    ins = v.get("inserts") or []
    if ins:
        if not line_out:
            die(f"video {vid}: inserts sit over script lines, so they need the edit to find the lines (leave "
                "\"assemble\" on)")
        cur = "base0"
        used["inserts"] = []
        for k, it in enumerate(ins):
            f_ = it.get("file") if isinstance(it, dict) else None
            fp = f_ if isinstance(f_, str) and os.path.isabs(f_) else os.path.join(base, f_ or "")
            if not isinstance(f_, str) or not os.path.isfile(fp):
                die(f"video {vid}: insert {k + 1}: \"file\" is a recording you made (a screen recording, the product)")
            if it.get("line") not in line_out:
                die(f"video {vid}: insert {k + 1}: \"line\" is a script line id ({', '.join(line_out)})")
            a_, b_ = line_out[it["line"]]
            st = float(it.get("start") or 0)
            args += ["-ss", f"{st:.3f}", "-i", fp]
            graph.append(f"[{n}:v]setpts=PTS-STARTPTS+{a_:.3f}/TB,fps=30,{fill(W, H if layout == 'talking_head' else H // 2)}"
                         f"[ins{k}]")
            ypos = 0 if layout == "talking_head" else (H // 2 if (c.get("supplied_footage") or {}).get("position", "top")
                                                       == "top" else 0)
            graph.append(f"[{cur}][ins{k}]overlay=0:{ypos}:enable='between(t,{a_:.3f},{b_:.3f})':eof_action=pass[ib{k}]")
            cur = f"ib{k}"
            n += 1
            used["inserts"].append({"file": rel(fp, base), "sha256": sha256(fp), "line": it["line"]})
            if product_at is None or a_ < product_at:
                product_at = round(a_, 2)
        graph.append(f"[{cur}]null[base1]")
        base_label = "base1"
    else:
        base_label = "base0"

    # music: only what the creator declared and may use
    music = spec.get("music") if isinstance(spec.get("music"), dict) else {"source": "none"}
    if music.get("source") in ("licensed", "brief_supplied") and music.get("file"):
        mp = music["file"] if os.path.isabs(music["file"]) else os.path.join(base, music["file"])
        if not os.path.isfile(mp):
            die(f"music file {music['file']} not found")
        args += ["-stream_loop", "-1", "-i", mp]
        vol = float(music.get("volume") or 0.12)
        graph.append(f"[{n}:a]atrim=duration={length:.3f},aresample=48000,volume={vol:.3f}[mus]")
        graph.append("[voice][mus]amix=inputs=2:duration=first:normalize=0[mix]")
        n += 1
        voice_label = "[mix]"
        used["music"] = {"file": rel(mp, base), "sha256": sha256(mp)}
    else:
        voice_label = "[voice]"

    ov = build_overlays(vid, timed if show_caps else [], length, style, layout, screen, label,
                        hook if show_hook else None, tmp)
    args += ["-f", "concat", "-safe", "0", "-i", ov]
    final = "" if width == W else f",scale={width}:{int(width * H / W) // 2 * 2}:flags=lanczos"
    graph.append(f"[{base_label}]trim=duration={length:.3f},setpts=PTS-STARTPTS[base];[{n}:v]fps=30,format=yuva420p[ovl];"
                 f"[base][ovl]overlay=0:0:format=yuv420:eof_action=pass{final},format=yuv420p[v]")
    graph.append(f"{voice_label}atrim=duration={length:.3f},highpass=f=80,loudnorm=I=-14:TP=-1:LRA=11,aresample=48000[a]"
                 if not is_placeholder else f"{voice_label}anull[a]")
    out = os.path.abspath(os.path.join(out_dir, f"{vid}.mp4"))
    print(f"  video {vid}: {layout}, {length:.1f} s, opens with {hook_id}" + (" (placeholder take)" if is_placeholder else ""),
          flush=True)
    if cut:
        short = [x if len(x) <= 70 else x[:67].rstrip() + "..." for x in cut[:5]]
        print(f"    cut {len(cut)} part{'' if len(cut) == 1 else 's'} not in the script or flubbed tries: "
              + "; ".join(f"'{x}'" for x in short) + (" ..." if len(cut) > 5 else "")
              + ". Leave them out of your own edit too", flush=True)
    run(["ffmpeg", "-y", "-v", "error", *args, "-filter_complex", ";".join(graph), "-map", "[v]", "-map", "[a]",
         "-t", f"{length:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20" if width == W else "28",
         "-profile:v", "high", "-maxrate", "12M", "-bufsize", "24M", "-g", "60", "-r", "30",
         "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
         "-c:a", "aac", "-b:a", "128k" if width != W else "192k", "-ac", "2", "-ar", "48000",
         "-movflags", "+faststart", "-map_metadata", "-1", out], cwd=tmp)
    cover = os.path.join(out_dir, f"{vid}-cover.jpg")
    run(["ffmpeg", "-y", "-v", "error", "-ss", "1.0", "-i", out, "-frames:v", "1", "-q:v", "4", cover])
    # when the spoken disclosure is said: the end of the first sentence that says it is paid. A
    # sentence that says "not an ad" doesn't count, and a long one counts only once it is finished.
    sentences = split_sentences(timed)
    targets = disclosure_targets([r["say"] for r in script_m["spoken"] if r.get("kind") == "disclosure"], [hook],
                                 c.get("brand"))
    disc_at = spoken_disclosure_at(sentences, c.get("brand"), targets)
    return {"id": vid, "account": v["account"], "layout": layout, "file": rel(out, out_dir), "sha256": sha256(out),
            "bytes": os.path.getsize(out), "seconds": round(length, 2), "hook_id": hook_id, "hook": hook,
            "hook_take": bool(hook_take and not is_placeholder),
            "on_screen": {"disclosure": screen["disclosure"], "disclosure_seconds": float(screen["seconds"]),
                          "from": 0.0},
            "spoken_disclosure_s": disc_at, "spoken_disclosure_estimated": is_placeholder,
            "placeholder": is_placeholder, "inputs": used, "accounts": list(v.get("accounts") or [v["account"]]),
            "spoken": sentences, "transcript_sha256": tr_sha, "dropped": dropped[:200], "cut": cut[:50],
            "burned_text": burned, "captions_on": show_caps, "hook_text_on": show_hook,
            "supplied_audio": (v.get("supplied_audio") or "mute") if layout == "split_screen" else None,
            "hook_in_take": hook_in_take, "product_on_screen_s": product_at,
            "lines_at": {k: [round(a_, 2), round(b_, 2)] for k, (a_, b_) in line_out.items()},
            "music": music if isinstance(music, dict) else {"source": "none"},
            "captions": [{"w": w["w"], "start": round(w["start"], 2)} for w in timed],
            "cover": rel(cover, out_dir)}


def contact_sheet(covers, path):
    if not covers:
        return None
    n = len(covers)
    inputs = []
    for cv in covers:
        inputs += ["-i", cv]
    if n == 1:
        graph = "[0:v]scale=270:480[out]"
    else:
        layout = "|".join(f"{i * 270}_0" for i in range(n))
        graph = ("".join(f"[{i}:v]scale=270:480[t{i}];" for i in range(n)) + "".join(f"[t{i}]" for i in range(n))
                 + f"xstack=inputs={n}:layout={layout}:fill=black[out]")
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", graph, "-map", "[out]", "-frames:v", "1",
         "-q:v", "4", path])
    return path


def frames_sheet(video, out):
    """Frames at 0, 1, 2 and 3 seconds side by side: the creator looks for the on-screen disclosure."""
    if not os.path.isfile(video):
        die(f"{video} not found")
    out = out if out.lower().endswith((".jpg", ".jpeg", ".png")) else os.path.splitext(out)[0] + "-frames.jpg"
    args = []
    for t in (0.0, 1.0, 2.0, 3.0):
        args += ["-ss", f"{t:.2f}", "-i", video]
    graph = "".join(f"[{i}:v]scale=360:640:force_original_aspect_ratio=decrease,pad=360:640:(ow-iw)/2:(oh-ih)/2,"
                    f"setsar=1[f{i}];" for i in range(4)) + "[f0][f1][f2][f3]hstack=inputs=4[out]"
    run(["ffmpeg", "-y", "-v", "error", *args, "-filter_complex", graph, "-map", "[out]", "-frames:v", "1", "-q:v", "3",
         out])
    print(f"frames at 0, 1, 2 and 3 s -> {out}. Show it to the creator: the disclosure must be readable in every frame "
          "it should be in")


def check_spec(spec, c, base):
    if not isinstance(spec, dict) or not isinstance(spec.get("videos"), list) or not spec["videos"]:
        die("edit.json needs \"videos\": one entry per account")
    allowed = c.get("formats_list") or []
    seen, accs = set(), set()
    for v in spec["videos"]:
        if not isinstance(v, dict):
            die("each video in edit.json is an object: {\"id\", \"account\", \"layout\", ...}")
        vid = str(v.get("id") or "")
        if not re.fullmatch(r"[a-z0-9][a-z0-9_-]{0,39}", vid):
            die(f"video id {vid!r}: lowercase letters, digits, dashes or underscores (it becomes the file name)")
        if vid in seen:
            die(f"video id {vid} is used twice")
        seen.add(vid)
        if not isinstance(v.get("account"), str) or not v["account"].strip():
            die(f"video {vid}: \"account\", the account it is for (as named in script.json's openings)")
        alist = v.get("accounts")
        if alist is not None and (not isinstance(alist, list) or not alist or v["account"] not in alist
                                  or not all(isinstance(x, str) and x.strip() for x in alist)):
            die(f"video {vid}: \"accounts\" lists every account this one edit goes to, \"account\" among them (one edit "
                "cross-posted to TikTok, Reels and Shorts)")
        for acc in alist or [v["account"]]:
            if acc in accs:
                die(f"two videos for account {acc}: one video per account per run")
            accs.add(acc)
        if v.get("inserts") is not None and (not isinstance(v["inserts"], list) or not all(
                isinstance(x, dict) and isinstance(x.get("line"), str) and isinstance(x.get("file"), str)
                for x in v["inserts"])):
            die(f"video {vid}: \"inserts\": [{{\"line\": \"l3\", \"file\": \"takes/screen.mp4\", \"start\": 0}}], a "
                "recording you made shown over the line that describes it")
        if v.get("layout") not in LAYOUTS:
            die(f"video {vid}: layout is one of {', '.join(LAYOUTS)}")
        if allowed and v["layout"] not in allowed:
            die(f"video {vid}: the brief accepts {', '.join(allowed)}, not {v['layout']}")
        for k in ("speed", "mirror", "flip", "hflip", "filter", "face_filter", "beauty", "avatar", "voice_change",
                  "lip_sync", "pitch"):
            if k in v or k in spec:
                die(f"\"{k}\": this skill never changes speed, mirrors or filters a video, and never generates or alters a "
                    "face or a voice. Each account gets its own opening instead")
        if v.get("supplied_audio") is not None and v.get("supplied_audio") not in SUPPLIED_AUDIO:
            die(f"video {vid}: \"supplied_audio\" is \"mute\" (the default), \"duck\" (the brand's sound under your "
                "voice) or \"keep\"")
        if v.get("supplied_audio") not in (None, "mute") and v.get("layout") != "split_screen":
            die(f"video {vid}: \"supplied_audio\" is for split_screen, where the brand's footage plays")
        for k in ("captions", "hook_text"):
            for where, val in ((f"video {vid}", v.get(k)), ("edit.json", spec.get(k))):
                if val is not None and not isinstance(val, bool):
                    die(f"{where}: \"{k}\" is true or false")
                if val is True and campaign_mod.burned_text(c) != "any":
                    die(f"{where}: \"{k}\": true, but the campaign's \"burned_text\" is \"{campaign_mod.burned_text(c)}\" "
                        "(the brief wants no text on the video)")
        if v.get("hook_transcript") is not None and not (isinstance(v["hook_transcript"], str) and v.get("hook_take")):
            die(f"video {vid}: \"hook_transcript\" is the path of transcribe.py's transcript of \"hook_take\"")
        if v.get("supplied_start") is not None and not is_num(v.get("supplied_start"), 0):
            die(f"video {vid}: supplied_start is seconds into the supplied footage")
    music = spec.get("music")
    if music is None:
        die("edit.json needs \"music\": {\"source\": \"none\"}, or {\"source\": \"licensed\", \"file\": ..., \"license\": "
            "\"<where the license is>\"}. Music is declared, never guessed")
    if not isinstance(music, dict) or music.get("source") not in ("none", "licensed", "brief_supplied"):
        die("\"music\" source is \"none\", \"licensed\" (with \"file\" and \"license\") or \"brief_supplied\"")
    if music.get("source") in ("licensed", "brief_supplied") and not (isinstance(music.get("license"), str)
                                                                      and music["license"].strip()):
        die("music: say where the license is (\"license\": \"receipt from ... / the brief's track\")")
    if music.get("source") == "brief_supplied" and not (isinstance(music.get("file"), str) and music["file"].strip()):
        die("music: \"brief_supplied\" needs \"file\", the track the brief supplied, so it is mixed in")
    if music.get("source") != "none" and c.get("music") == "none":
        die("the brief says no music; set \"music\": {\"source\": \"none\"}")


def main():
    ap = argparse.ArgumentParser(description="Edit the creator's takes into one vertical video per account.")
    ap.add_argument("edit", nargs="?", help="edit.json (with --frames: where to write the JPG, optional)")
    ap.add_argument("--out", default="videos")
    ap.add_argument("--width", type=int, default=W, help="output width (default 1080; 540 for small files)")
    ap.add_argument("--only", help="render just these video ids, comma separated")
    ap.add_argument("--placeholder", action="store_true",
                    help="a labelled placeholder where a take isn't filmed yet (a layout preview; never posted)")
    ap.add_argument("--frames", metavar="VIDEO",
                    help="write VIDEO's first seconds (0, 1, 2, 3 s) side by side as a JPG, to confirm its on-screen "
                         "disclosure; for an edit you made yourself")
    a = ap.parse_args()
    if a.frames:
        frames_sheet(a.frames, a.edit or os.path.splitext(a.frames)[0] + "-frames.jpg")
        return
    if not a.edit:
        die("give edit.json (references/edit-file.md)")
    if a.width < 360 or a.width > W or a.width % 2:
        die("--width must be an even number from 360 to 1080")
    if not (shutil.which("ffmpeg") and shutil.which("ffprobe")):
        die("ffmpeg is not installed. Mac: brew install ffmpeg. Windows: winget install Gyan.FFmpeg. Linux: sudo apt "
            "install ffmpeg")
    load_pillow()
    spec = read_json(a.edit, "the edit file")
    base = os.path.dirname(os.path.abspath(a.edit))
    if not isinstance(spec, dict):
        die("edit.json must hold one JSON object")
    for k in ("campaign", "script"):
        if not isinstance(spec.get(k), str) or not os.path.isfile(os.path.join(base, spec[k])):
            die(f"edit.json needs \"{k}\": the path of {k}.json")
    info = campaign_mod.load(os.path.join(base, spec["campaign"]))
    c = info["campaign"]
    if info["verdict"] != "GO":
        die(f"the campaign's verdict is {info['verdict']}. Run campaign.py and settle it before editing")
    sm = script_mod.check_script(os.path.join(base, spec["script"]))
    serr = [f"{w}: {m}" for lv, w, m in sm["issues"] if lv == "error"]
    if serr:
        die("the script has open errors (run script.py): " + "; ".join(serr[:3]))
    check_spec(spec, c, base)
    vids = spec["videos"]
    if a.only:
        keep = {x.strip() for x in a.only.split(",")}
        vids = [v for v in vids if v.get("id") in keep]
        if not vids:
            die(f"no videos with the ids {a.only}")
    os.makedirs(a.out, exist_ok=True)
    out_dir = os.path.abspath(a.out)
    results = []
    with tempfile.TemporaryDirectory() as tmp:
        for v in vids:
            results.append(render_video(v, c, sm, spec, base, out_dir, tmp, a.width, a.placeholder))
    sheet = contact_sheet([os.path.join(out_dir, r["cover"]) for r in results], os.path.join(out_dir, "contact-sheet.jpg"))
    mpath = os.path.join(out_dir, "manifest.json")
    old = {}
    if a.only and os.path.isfile(mpath):
        try:
            with open(mpath, encoding="utf-8") as fh:
                old = {x["id"]: x for x in json.load(fh).get("videos", [])}
        except (ValueError, OSError, AttributeError, TypeError, KeyError):
            old = {}
    for r in results:
        # each video carries the script and campaign it was made from, so a partial --only run never
        # relabels an older video with the new versions
        r["script_version"] = sm["version"]
        r["campaign_version"] = info["version"]
        r["campaign"] = c.get("id")
        old[r["id"]] = r
    manifest = {"campaign": c.get("id"), "script_version": sm["version"], "edit": rel(os.path.abspath(a.edit), out_dir),
                "videos": [old[k] for k in sorted(old)], "contactSheet": rel(sheet, out_dir) if sheet else None,
                "warnings": WARNINGS}
    with open(mpath, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=1, ensure_ascii=False)
    print(f"{len(results)} video(s) in {rel(out_dir)}/, manifest: {rel(mpath)}")
    if any(r["placeholder"] for r in results):
        print("placeholder: these are layout previews with no recording in them; they can't be posted. Film with "
              "shotlist.md, transcribe, and run this again")
    print("next: watch each video, then write job.json (one post per account) and run check_videos.py")


if __name__ == "__main__":
    guard(main)
