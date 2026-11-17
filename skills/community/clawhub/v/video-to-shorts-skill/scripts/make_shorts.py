#!/usr/bin/env python3
"""Cut vertical shorts from a long video, with word-by-word captions.

    python3 scripts/make_shorts.py clips.json --transcript work/transcript.json --out shorts/
    python3 scripts/make_shorts.py clips.json --preview      # crop check, no render

clips.json (the agent writes it after reading work/transcript.txt):
{
  "video": "talk.mp4",
  "style": {"accent": "#FFD43B", "uppercase": false, "hook": true},
  "clips": [
    {"id": "01", "start": 754.2, "end": 801.9,
     "hook": "Text on screen for the first seconds",
     "title": "Title for YouTube Shorts", "caption": "Caption for TikTok and Reels",
     "reframe": "auto", "focus_x": 0.5, "zoom": 1.1,
     "cut": [[770.4, 774.9]], "tighten": true, "fillers": true, "snap": true}
  ]
}

reframe: "auto" (face crop when OpenCV finds one speaker, else fit), "face", "center",
  "fit" (whole frame on a blurred copy of itself: two speakers, screen shares, wide shots).
focus_x: 0 to 1, sets the crop by hand. zoom: punch-in for crops (default 1.1).
cut: source-time ranges to remove inside the clip (a ramble, a "kind of").
tighten: remove pauses over 0.45 s, including silences the transcriber hides inside long words.
fillers: remove "um", "uh", stutters ("the the") and "you know," with a comma.
snap: fix small slips (start within 1 s of a sentence start, end within 4 s of a sentence end)
  and warn about the rest. Set "snap": false when a clip starts on a clause on purpose.

Writes shorts/clip-01.mp4 ... (1080x1920, H.264, AAC, -14 LUFS), a cover frame per clip,
contact-sheet.jpg and manifest.json (byte sizes, durations, texts, warnings). Needs ffmpeg
(any build) and Pillow (pip install pillow); captions are drawn with Pillow, so ffmpeg needs
no libass. OpenCV is optional, for finding the speaker: pip install opencv-python-headless.
"""
import argparse, functools, json, os, re, shutil, subprocess, sys, tempfile

W, H = 1080, 1920
# Text is centred on the frame, inside x 180-900 and y 290-1250: clear of the buttons on the right and the platform captions at the bottom.
SAFE_CX = W // 2
CAP_SIZE = 96          # fixed caption size; groups that don't fit are split, never shrunk
CAP_MAX_W = 720
HOOK_SIZE = 78
HOOK_SECONDS = 3.5
EYE_LINE = 0.38        # eyes sit about here in a typical talking-head frame
BEST = False           # --best: slower encode, slightly smaller files at the same quality
HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "..", "fonts")
FONT_FILES = ["Poppins-ExtraBold.ttf", "Poppins-Bold.ttf"]
FONT_URL = "https://raw.githubusercontent.com/google/fonts/main/ofl/poppins/"
FUNCTION_WORDS = {"a", "an", "the", "of", "to", "for", "and", "that", "with", "on", "in", "is",
                  "so", "but", "i", "or", "at", "as", "if", "by", "from", "my", "your", "our"}
FILLERS = {"um", "uh", "uhm", "erm", "hmm", "mm"}
WARNINGS = []


def warn(msg):
    WARNINGS.append(msg)
    print("warning: " + msg, file=sys.stderr)


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        sys.exit("ffmpeg failed:\n" + r.stderr[-1500:])
    return r.stdout


def check_ffmpeg():
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        sys.exit("ffmpeg is not installed. Mac: brew install ffmpeg. Windows: winget install ffmpeg. "
                 "Linux: sudo apt install ffmpeg.")
    load_pillow()


def probe(path):
    out = json.loads(run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height,r_frame_rate:stream_tags=rotate:format=duration",
                          "-of", "json", path]))
    st = out["streams"][0]
    w, h = st["width"], st["height"]
    if str(st.get("tags", {}).get("rotate", "0")) in ("90", "270"):
        w, h = h, w
    num, _, den = st.get("r_frame_rate", "30/1").partition("/")
    try:
        fps = float(num) / float(den or 1)
    except (ValueError, ZeroDivisionError):
        fps = 30.0
    # keep the source rate (25 or 29.97 judder when forced to 30) unless it's unusual
    fps_out = st.get("r_frame_rate", "30/1") if 23.5 <= fps <= 60.5 else "30"
    return w, h, float(out["format"]["duration"]), fps_out


# ---------- speech and timing ----------

def clean(w):
    return re.sub(r"[^\w']", "", w.lower())


def sentence_end(word):
    return word["w"].rstrip("\"')]")[-1:] in ".?!"


def snap_bounds(words, clip):
    """Move start and end to the nearest sentence edge within 4 s; warn when there's none."""
    a, b = float(clip["start"]), float(clip["end"])
    idx = [i for i, w in enumerate(words) if w["start"] >= a - 0.05]
    if not idx:
        return a, b
    i = idx[0]
    starts_ok = lambda j: (j == 0 or sentence_end(words[j - 1])) and (words[j]["w"][:1].isupper() or
                                                                      not words[j]["w"][:1].isalpha())
    if not starts_ok(i) and clip.get("snap", True) is not False:
        # only small slips are fixed automatically; a start further away is the agent's call
        near = [j for j in range(len(words)) if abs(words[j]["start"] - a) <= 1.0 and starts_ok(j)
                and words[j]["start"] < b - 8]
        if near:
            j = min(near, key=lambda j: abs(words[j]["start"] - a))
            print(f"  clip {clip['id']}: start moved {words[j]['start'] - a:+.1f} s to a sentence start", flush=True)
            a = words[j]["start"] - 0.05
        else:
            first = " ".join(w["w"] for w in words[i:i + 5])
            warn(f"clip {clip['id']} starts mid-sentence: '{first}'. Move it, or set \"snap\": false "
                 "if this clause stands alone on purpose")
    inside = [j for j, w in enumerate(words) if w["start"] >= a - 0.05 and w["end"] <= b + 0.15]
    if inside and not sentence_end(words[inside[-1]]) and clip.get("snap", True) is not False:
        near = [j for j in range(len(words)) if abs(words[j]["end"] - b) <= 4 and sentence_end(words[j])
                and words[j]["end"] > a + 8]
        if near and clip.get("snap", True):
            j = min(near, key=lambda j: abs(words[j]["end"] - b))
            print(f"  clip {clip['id']}: end moved {words[j]['end'] - b:+.1f} s to a sentence end", flush=True)
            b = words[j]["end"] + 0.05
        else:
            last = " ".join(w["w"] for w in words[max(inside[-1] - 4, 0):inside[-1] + 1])
            warn(f"clip {clip['id']} ends mid-sentence: '...{last}'")
    return a, b


def select_words(words, a, b, clip):
    """Words inside the clip, with fillers, stutters and cut ranges marked as removed.
    Returns a list of (word, removed) in order; word end times are capped so silences the
    transcriber stretches over a word count as pauses."""
    ws = [dict(w) for w in words if w["start"] >= a - 0.05 and w["end"] <= b + 0.15]
    cuts = [(float(s), float(e)) for s, e in clip.get("cut", [])]
    fillers = clip.get("fillers", True)
    out = []
    for i, w in enumerate(ws):
        cap = 0.10 + 0.075 * len(clean(w["w"]))
        w["end"] = min(w["end"], w["start"] + max(cap, 0.12))
        removed = any(s - 0.02 <= w["start"] and w["end"] <= e + 0.02 for s, e in cuts)
        c = clean(w["w"])
        if fillers and not removed:
            nxt = clean(ws[i + 1]["w"]) if i + 1 < len(ws) else None
            if c in FILLERS:
                removed = True
            elif c and c == nxt:  # stutter: keep the second copy
                removed = True
            elif c == "you" and i + 1 < len(ws) and ws[i + 1]["w"].lower().startswith("know,"):
                removed = True
            elif c == "know" and w["w"].endswith(",") and i > 0 and clean(ws[i - 1]["w"]) == "you":
                removed = True
        out.append((w, removed))
    return out


def keep_spans(marked, a, b, tighten):
    """Source-time spans to keep: pauses over 0.45 s and every removed word become cuts."""
    kept = [(w, r) for w, r in marked]
    if not any(not r for _, r in kept):
        return [(a, b)]
    pad, max_gap = 0.12, 0.45 if tighten else 99
    spans, cur = [], None
    prev_removed = False
    for w, r in kept:
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
    spans.append((cur[0], min(b + 0.3, cur[1] + 0.25)))  # a little air after the last word
    merged = []
    for s, e in spans:
        if merged and s <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], e))
        else:
            merged.append((s, e))
    return [(s, e) for s, e in merged if e - s > 0.15]


def to_output_time(t, spans):
    """Map a source time to the time in the cut clip."""
    acc = 0.0
    for s, e in spans:
        if t <= s:
            return acc
        if t <= e:
            return acc + (t - s)
        acc += e - s
    return acc


# ---------- framing ----------

def detect_faces(path, a, b, samples=14):
    try:
        import cv2
        cap = cv2.VideoCapture(path)
        casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        found = []
        for i in range(samples):
            t = a + (b - a) * (i + 0.5) / samples
            cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
            ok, frame = cap.read()
            if not ok:
                continue
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            fw = gray.shape[1]
            faces = casc.detectMultiScale(gray, 1.1, 6, minSize=(max(40, fw // 14),) * 2)
            found.append([(x + w / 2) / fw for x, y, w, h in faces])
        cap.release()
        return found
    except Exception:
        return None  # no or partial OpenCV install: skip


def choose_frame(clip, src_w, src_h, path):
    mode = clip.get("reframe", "auto")
    if src_w / src_h <= W / H + 0.01:
        return "vertical", 0.5
    if "focus_x" in clip and mode in ("auto", "face", "center"):
        return "crop", float(clip["focus_x"])
    if mode == "center":
        return "crop", 0.5
    if mode == "fit":
        return "fit", 0.5
    found = detect_faces(path, float(clip["start"]), float(clip["end"]))
    if found is None:
        if mode == "face":
            warn(f"clip {clip['id']}: face mode needs OpenCV (pip install opencv-python-headless); using center")
        return ("fit", 0.5) if src_w / src_h > 2.0 and mode != "face" else ("crop", 0.5)
    with_face = [f for f in found if f]
    if len(with_face) < max(3, len(found) * 0.4):
        return ("crop", 0.5) if mode == "face" else ("fit", 0.5)
    xs = sorted(x for f in with_face for x in f)
    if mode == "auto" and xs[-1] - xs[0] > 0.35 and sum(len(f) > 1 for f in with_face) > len(with_face) * 0.3:
        return "fit", 0.5  # two people far apart: show both
    one = sorted(f[0] if len(f) == 1 else min(f, key=lambda x: abs(x - 0.5)) for f in with_face)
    return "crop", one[len(one) // 2]


def frame_filter(kind, focus, src_w, src_h, zoom, tag):
    """Filter chain from a span's frames to 1080x1920. zoom > 1 punches in, eyes kept level."""
    if kind == "vertical":
        return f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
    if kind == "crop":
        ch = int(src_h / zoom) // 2 * 2
        cw = int(ch * W / H) // 2 * 2
        x = int(min(max(focus * src_w - cw / 2, 0), src_w - cw))
        y = int(min(max(EYE_LINE * src_h * (1 - 1 / zoom), 0), src_h - ch))
        return f"crop={cw}:{ch}:{x}:{y},scale={W}:{H}:flags=lanczos"
    return (f"split=2[bg{tag}][fg{tag}];[bg{tag}]scale={W}:{H}:force_original_aspect_ratio=increase,"
            f"crop={W}:{H},gblur=sigma=40,eq=brightness=-0.15[bgb{tag}];[fg{tag}]scale={W}:-2[fgs{tag}];"
            f"[bgb{tag}][fgs{tag}]overlay=(W-w)/2:min((H-h)/2\\,470)")


# ---------- captions ----------
# Drawn with Pillow and laid over the video, so any ffmpeg build works
# (many builds, including Homebrew's, ship without libass or drawtext).

def load_pillow():
    try:
        from PIL import Image, ImageDraw, ImageFont
        return Image, ImageDraw, ImageFont
    except ImportError:
        sys.exit("Captions need Pillow: pip install pillow")


@functools.lru_cache(maxsize=None)
def caption_font(size):
    _, _, ImageFont = load_pillow()
    for name in FONT_FILES:
        path = os.path.join(FONT_DIR, name)
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    os.makedirs(FONT_DIR, exist_ok=True)
    path = os.path.join(FONT_DIR, FONT_FILES[0])
    try:  # some skill registries strip binary files; fetch the open-licensed font once
        import urllib.request
        urllib.request.urlretrieve(FONT_URL + FONT_FILES[0], path)
    except Exception:
        if shutil.which("curl"):
            subprocess.run(["curl", "-sfL", FONT_URL + FONT_FILES[0], "-o", path], check=False)
    if os.path.exists(path) and os.path.getsize(path) > 10000:
        return ImageFont.truetype(path, size)
    warn("caption font missing; using Pillow's default font")
    return ImageFont.load_default(size)


@functools.lru_cache(maxsize=None)
def _measure():
    Image, ImageDraw, _ = load_pillow()
    return ImageDraw.Draw(Image.new("RGBA", (10, 10)))


def text_w(text, size):
    return _measure().textlength(text, font=caption_font(size))


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def balanced_lines(words, size, max_w, max_lines=2):
    """Split words into at most max_lines lines of similar width."""
    lines, cur = [], []
    for w in words:
        if cur and text_w(" ".join(cur + [w]), size) > max_w:
            lines.append(cur)
            cur = [w]
        else:
            cur.append(w)
    if cur:
        lines.append(cur)
    if len(lines) == 2:  # balance two lines
        best = lines
        for k in range(1, len(words)):
            a, b = words[:k], words[k:]
            wa, wb = text_w(" ".join(a), size), text_w(" ".join(b), size)
            if max(wa, wb) <= max_w and max(wa, wb) < max(text_w(" ".join(x), size) for x in best):
                best = [a, b]
        lines = best
    return lines


def render_overlay(path, cap_words, hook, style, cap_y, hook_bottom, hook_top=None):
    """One transparent 1080x1920 frame: caption (spoken word in the accent) and the hook."""
    Image, ImageDraw, _ = load_pillow()
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    accent = hexrgb(style.get("accent", "#FFD43B"))
    if hook:
        # two lines at 78 to 70 px; if it needs more, three lines at full size (never drop words)
        size, lines = HOOK_SIZE, balanced_lines(hook.split(), HOOK_SIZE, 640)
        for trial in range(HOOK_SIZE - 4, 69, -4):
            if len(lines) <= 2:
                break
            alt = balanced_lines(hook.split(), trial, 640)
            if len(alt) <= 2:
                size, lines = trial, alt
        if len(lines) > 2:
            size, lines = HOOK_SIZE, balanced_lines(hook.split(), HOOK_SIZE, 640)
        f = caption_font(size)
        lh = int(size * 1.18)
        box_h = lh * len(lines) + 56
        box_w = max(text_w(" ".join(ln), size) for ln in lines) + 80
        y0 = hook_top if hook_top is not None else hook_bottom - box_h
        x0 = SAFE_CX - box_w / 2
        draw.rounded_rectangle([x0, y0, x0 + box_w, y0 + box_h], 24, fill=(255, 255, 255, 255))
        for i, ln in enumerate(lines):
            draw.text((SAFE_CX, y0 + 28 + i * lh + lh / 2), " ".join(ln), font=f, fill=(0, 0, 0, 255), anchor="mm")
    if cap_words:
        f = caption_font(CAP_SIZE)
        space = text_w(" ", CAP_SIZE)
        total = sum(text_w(w, CAP_SIZE) for w, _ in cap_words) + space * (len(cap_words) - 1)
        x = SAFE_CX - total / 2
        y = cap_y - int(CAP_SIZE * 1.18)
        for w, active in cap_words:
            fill = accent + (255,) if active else (255, 255, 255, 255)
            draw.text((x, y + 6), w, font=f, fill=(0, 0, 0, 140))  # soft drop shadow
            draw.text((x, y), w, font=f, fill=fill, stroke_width=8, stroke_fill=(0, 0, 0, 255))
            x += text_w(w, CAP_SIZE) + space
    img.save(path, optimize=True)


def caption_groups(kept, upper):
    """Up to 3 words per caption, one line at a fixed size. Breaks at punctuation and pauses;
    a group never ends on a small word like "the" or "of"."""
    groups, cur = [], []
    for i, w in enumerate(kept):
        cur.append(w)
        nxt = kept[i + 1] if i + 1 < len(kept) else None
        txt = lambda g: " ".join((x["w"].upper() if upper else x["w"]) for x in g)
        too_wide = nxt is not None and text_w(txt(cur + [nxt]), CAP_SIZE) > CAP_MAX_W
        brk = (nxt is None or len(cur) >= 3 or w["w"][-1:] in ".?!,;:" or too_wide
               or nxt["start"] - w["end"] > 0.25)
        if brk and nxt is not None and clean(w["w"]) in FUNCTION_WORDS and w["w"][-1:] not in ".?!,;:" \
                and len(cur) > 1:
            groups.append(cur[:-1])  # carry the small word to the next group
            cur = [cur[-1]]
            continue
        if brk:
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    return [g for g in groups if g]


def build_overlays(clip, marked, spans, style, length, frame_kind, tmp):
    """Write PNG overlays plus an ffmpeg concat list that shows each one for the right time."""
    upper = style.get("uppercase", False)
    cap_y = int(style.get("caption_y", 1230))
    cap_top = cap_y - int(CAP_SIZE * 1.18)
    hook = clip.get("hook") if style.get("hook", True) else None
    kept = [dict(w) for w, r in marked if not r]
    if kept and kept[0]["w"][:1].islower():
        kept[0]["w"] = kept[0]["w"][:1].upper() + kept[0]["w"][1:]  # a clip that starts mid-sentence still reads as one
    if hook:
        if len(hook.split()) > 10:
            warn(f"clip {clip['id']}: hook has {len(hook.split())} words; 8 or fewer reads in time")
        spoken = " ".join(clean(w["w"]) for w in kept if to_output_time(w["start"], spans) < 10)
        hook_c = " ".join(clean(x) for x in hook.split())
        if len(hook_c.split()) >= 3 and hook_c in spoken:
            warn(f"clip {clip['id']}: the hook repeats words spoken in the first 10 s; say something new")
    hook_windows = []
    if hook:
        hook_windows.append((0.0, min(HOOK_SECONDS, length)))
        if length > 40:
            mid = length * 0.5
            hook_windows.append((mid, min(mid + 2.0, length)))
    # crop: hook sits just above the captions (the face fills the top); fit: at the top
    hook_top = 330 if frame_kind == "fit" else None
    hook_bottom = cap_top - 36
    events = []
    timed = [[(to_output_time(w["start"], spans), to_output_time(w["end"], spans), w["w"]) for w in g]
             for g in caption_groups(kept, upper)]
    for gi, tw in enumerate(timed):
        next_start = timed[gi + 1][0][0] if gi + 1 < len(timed) else length
        for i, (s, e, _) in enumerate(tw):
            end = tw[i + 1][0] if i + 1 < len(tw) else min(next_start, max(e + 0.1, tw[0][0] + 0.4))
            if next_start - end < 0.15:
                end = next_start  # no flicker between groups
            if end - s < 0.02:
                continue
            events.append((s, end, [((ww.upper() if upper else ww), j == i) for j, (_, _, ww) in enumerate(tw)]))
    cuts = {0.0, length} | {t for s, e, _ in events for t in (s, e)} | {t for w in hook_windows for t in w}
    cuts = sorted(c for c in cuts if 0 <= c <= length)
    rendered, listing = {}, []
    for a, b in zip(cuts, cuts[1:]):
        if b - a < 0.005:
            continue
        mid = (a + b) / 2
        cap = next((w for s, e, w in events if s <= mid < e), None)
        show_hook = hook if any(s <= mid < e for s, e in hook_windows) else None
        key = (tuple(cap) if cap else None, show_hook)
        if key not in rendered:
            name = f"o{clip['id']}-{len(rendered):04d}.png"
            render_overlay(os.path.join(tmp, name), cap, show_hook, style, cap_y, hook_bottom, hook_top)
            rendered[key] = name
        listing.append((rendered[key], b - a))
    if not listing:
        name = f"o{clip['id']}-blank.png"
        render_overlay(os.path.join(tmp, name), None, None, style, cap_y, hook_bottom, hook_top)
        listing = [(name, length)]
    lst = f"overlays-{clip['id']}.txt"
    with open(os.path.join(tmp, lst), "w", encoding="utf-8") as fh:
        fh.write("ffconcat version 1.0\n")
        for name, d in listing:
            fh.write(f"file '{name}'\nduration {d:.3f}\n")
        fh.write(f"file '{listing[-1][0]}'\n")  # the concat demuxer needs the last file twice
    return lst


# ---------- render ----------

def plan_clip(clip, words, src, src_w, src_h):
    a, b = snap_bounds(words, clip)
    if b <= a:
        sys.exit(f"clip {clip['id']}: end must be after start")
    marked = select_words(words, a, b, clip)
    spans = keep_spans(marked, a, b, clip.get("tighten", True))
    for s, e in clip.get("cut", []):  # remove cut ranges even where no word was spoken
        spans = [p for sp in spans for p in ((sp[0], min(sp[1], s)), (max(sp[0], e), sp[1])) if p[1] - p[0] > 0.15]
    length = sum(e - s for s, e in spans)
    kind, focus = choose_frame(clip, src_w, src_h, src)
    return a, b, marked, spans, length, kind, focus


def render_clip(clip, src, words, style, tmp, out_dir, src_w, src_h, fps):
    a, b, marked, spans, length, kind, focus = plan_clip(clip, words, src, src_w, src_h)
    if length < 8:
        warn(f"clip {clip['id']}: only {length:.0f} s long")
    if length > 180:
        warn(f"clip {clip['id']}: {length:.0f} s is over the 3-minute limit for Shorts and TikTok's API")
    elif length > 60:
        warn(f"clip {clip['id']}: {length:.0f} s; most strong clips are 25 to 45 s, and YouTube blocks Shorts over "
             "60 s that get a Content ID claim (keep it under 60 s if any music or footage isn't yours)")
    zoom = float(clip.get("zoom", 1.1 if kind == "crop" else 1.0))
    if kind == "crop" and src_h * W / H / zoom < W * 0.5:
        warn(f"clip {clip['id']}: a {src_h}p source is enlarged about {H * zoom / src_h:.1f}x in a crop; "
             "it will look soft. Use \"reframe\": \"fit\" or a bigger source")
    overlay_list = build_overlays(clip, marked, spans, style, length, kind, tmp)
    seek = max(0.0, a - 3)
    parts, labels = [], []
    for i, (s, e) in enumerate(spans):
        # alternate a slight punch-in at every cut, so removed pauses read as edits, not glitches
        z = zoom * (1.12 if (kind == "crop" and i % 2 == 1) else 1.0)
        fade_out = 0.08 if i == len(spans) - 1 else 0.01
        parts.append(f"[0:v]trim=start={s - seek:.3f}:end={e - seek:.3f},setpts=PTS-STARTPTS,"
                     f"{frame_filter(kind, focus, src_w, src_h, z, i)},setsar=1[v{i}];"
                     f"[0:a]atrim=start={s - seek:.3f}:end={e - seek:.3f},asetpts=PTS-STARTPTS,"
                     f"afade=t=in:d=0.01,afade=t=out:st={max(0, e - s - fade_out):.3f}:d={fade_out}[a{i}]")
        labels.append(f"[v{i}][a{i}]")
    graph = ";".join(parts) + f";{''.join(labels)}concat=n={len(spans)}:v=1:a=1[cv][ca];"
    graph += f"[cv]fps={fps}[base];[1:v]fps={fps},format=yuva420p[ov];"
    graph += "[base][ov]overlay=0:0:format=yuv420:shortest=0:eof_action=pass,format=yuv420p[v];"
    graph += "[ca]highpass=f=80,loudnorm=I=-14:TP=-1:LRA=11,aresample=48000[a]"
    out = os.path.abspath(os.path.join(out_dir, f"clip-{clip['id']}.mp4"))
    print(f"  clip {clip['id']}: {length:.1f} s, {kind}" + (f" x={focus:.2f} zoom {zoom}" if kind == "crop" else ""),
          flush=True)
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{seek:.3f}", "-t", f"{b - seek + 1:.3f}",
         "-i", os.path.abspath(src), "-f", "concat", "-safe", "0", "-i", overlay_list,
         "-filter_complex", graph, "-map", "[v]", "-map", "[a]",
         "-c:v", "libx264", "-preset", "medium" if BEST else "veryfast", "-crf", "19" if BEST else "20",
         "-profile:v", "high", "-maxrate", "12M", "-bufsize", "24M", "-g", "60", "-keyint_min", "30",
         "-bf", "2", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
         "-c:a", "aac", "-b:a", "192k", "-ac", "2", "-movflags", "+faststart", out], cwd=tmp)
    cover = os.path.join(out_dir, f"clip-{clip['id']}-cover.jpg")
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{min(1.0, length / 2):.2f}", "-i", out,
         "-frames:v", "1", "-q:v", "3", cover])
    return {"id": clip["id"], "path": out, "bytes": os.path.getsize(out), "seconds": round(length, 1),
            "source": [round(a, 2), round(b, 2)], "framing": kind, "hook": clip.get("hook", ""),
            "title": clip.get("title", ""), "caption": clip.get("caption", ""), "cover": os.path.abspath(cover)}


def preview(clip, words, src, src_w, src_h, out_dir):
    """Three source frames with the planned 9:16 crop drawn on, plus the snapped first and last
    words. Look at it before rendering; adjust focus_x, reframe or the times if needed."""
    Image, ImageDraw, _ = load_pillow()
    a, b, marked, spans, length, kind, focus = plan_clip(clip, words, src, src_w, src_h)
    zoom = float(clip.get("zoom", 1.1 if kind == "crop" else 1.0))
    frames = []
    for i, t in enumerate((a + 1, (a + b) / 2, b - 1)):
        p = os.path.join(out_dir, f"preview-{clip['id']}-{i}.jpg")
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{max(0, t):.2f}", "-i", src, "-frames:v", "1", "-q:v", "4", p])
        im = Image.open(p).convert("RGB")
        if kind == "crop":
            ch = src_h / zoom
            cw = ch * W / H
            x = min(max(focus * src_w - cw / 2, 0), src_w - cw)
            y = min(max(EYE_LINE * src_h * (1 - 1 / zoom), 0), src_h - ch)
            ImageDraw.Draw(im).rectangle([x, y, x + cw, y + ch], outline=(255, 212, 59), width=max(4, src_w // 240))
        frames.append(im.resize((640, int(640 * src_h / src_w))))
        os.remove(p)
    sheet = Image.new("RGB", (640 * 3 + 20, frames[0].height), "#222222")
    for i, f in enumerate(frames):
        sheet.paste(f, (i * 650, 0))
    path = os.path.join(out_dir, f"preview-{clip['id']}.jpg")
    sheet.save(path, quality=85)
    kept = [w["w"] for w, r in marked if not r]
    print(f"  clip {clip['id']}: {kind}" + (f" focus_x={focus:.2f}" if kind == "crop" else "")
          + f", {length:.1f} s after tightening -> {path}")
    print(f"     starts: \"{' '.join(kept[:8])} ...\"")
    print(f"     ends:   \"... {' '.join(kept[-8:])}\"")


def contact_sheet(covers, path):
    if not covers:
        return None
    n = len(covers)
    cols = min(5, n)
    inputs = []
    for c in covers:
        inputs += ["-i", c]
    if n == 1:
        graph = "[0:v]scale=270:480[out]"
    else:
        layout = "|".join(f"{(i % cols) * 270}_{(i // cols) * 480}" for i in range(n))
        graph = ("".join(f"[{i}:v]scale=270:480[t{i}];" for i in range(n)) + "".join(f"[t{i}]" for i in range(n))
                 + f"xstack=inputs={n}:layout={layout}:fill=black[out]")
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", graph, "-map", "[out]",
         "-frames:v", "1", "-q:v", "3", path])
    return os.path.abspath(path)


def main():
    ap = argparse.ArgumentParser(description="Cut vertical shorts with captions.")
    ap.add_argument("clips")
    ap.add_argument("--transcript", default="work/transcript.json")
    ap.add_argument("--out", default="shorts")
    ap.add_argument("--only", help="render just these clip ids, comma separated")
    ap.add_argument("--best", action="store_true", help="slower, higher-efficiency encode")
    ap.add_argument("--preview", action="store_true",
                    help="don't render; save frames with the planned crop and print each clip's first and last words")
    a = ap.parse_args()
    check_ffmpeg()
    global BEST
    BEST = a.best
    spec = json.load(open(a.clips, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(a.clips))
    src = spec["video"] if os.path.isabs(spec["video"]) else os.path.join(base, spec["video"])
    if not os.path.exists(src):
        sys.exit(f"Video not found: {src}")
    words = json.load(open(a.transcript, encoding="utf-8"))["words"]
    src_w, src_h, total, fps = probe(src)
    clips = spec.get("clips", [])
    if a.only:
        keep = {x.strip().zfill(2) for x in a.only.split(",")}
        clips = [c for c in clips if str(c["id"]).zfill(2) in keep]
    if not clips:
        sys.exit("No clips in the spec")
    for c in clips:
        c["id"] = str(c["id"]).zfill(2)
        if float(c["end"]) > total + 0.5:
            sys.exit(f"clip {c['id']} ends at {c['end']} s but the video is {total:.0f} s")
    os.makedirs(a.out, exist_ok=True)
    out_dir = os.path.abspath(a.out)
    if a.preview:
        for c in clips:
            preview(c, words, src, src_w, src_h, out_dir)
        return
    results = []
    with tempfile.TemporaryDirectory() as tmp:
        for c in clips:
            results.append(render_clip(c, src, words, spec.get("style", {}), tmp, out_dir, src_w, src_h, fps))
    sheet = contact_sheet([r["cover"] for r in results], os.path.join(out_dir, "contact-sheet.jpg"))
    manifest = {"video": os.path.abspath(src), "clips": results, "contactSheet": sheet, "warnings": WARNINGS}
    with open(os.path.join(out_dir, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, ensure_ascii=False)
    print(f"{len(results)} clip(s) in {a.out}/, contact sheet: {sheet}")
    if WARNINGS:
        print(f"{len(WARNINGS)} warning(s); check them before posting.")


if __name__ == "__main__":
    main()
