#!/usr/bin/env python3
"""Edit a talking-head video: cut pauses, fillers, stutters and retakes, add punch-ins on jump
cuts, clean and level the audio, and write captions and chapters.

    python3 scripts/edit_video.py edit.json --transcript work/transcript.json --out edited/ --plan
    python3 scripts/edit_video.py edit.json --transcript work/transcript.json --out edited/

edit.json (the agent writes it; every key except "video" is optional):
{
  "video": "lesson.mp4",
  "style": "youtube",                   # or "tight" (fast, social) or "podcast" (gentle, no punch-ins)
  "pauses": {"max": 0.5},               # override the style's pause limit
  "fillers": ["um", "uh", "er", "erm", "hmm"],
  "extra_fillers": [],                  # opt-in: "like", "so", "you know", "basically"
  "stutters": true, "retakes": true, "voiced_gaps": true,
  "cut": [[61.2, 74.8, "tangent about the weather"]],
  "keep": [[300.0, 302.5]],             # protect a range from automatic cuts
  "replace": {"Cyrus Rex": "OSIRIS-REx"},  # fix misheard names in captions
  "punch_in": 1.10,                     # 0 turns punch-ins off
  "format": "source",                   # or "vertical" (1080x1920, crop on "focus_x")
  "focus_x": 0.5,
  "captions": {"srt": true, "burn": false},
  "audio": {"denoise": true, "lufs": -14},
  "chapters": [[0, "Intro"], [95.0, "How the camera works"], [240.0, "What we learned"]]
}
Times (cut, keep, chapters) are in the original video; the script maps chapters to the edit.

--plan writes edit-plan.md (every removal with its reason, and possible retakes left for a
person to decide) without rendering. A render writes edited/edited.mp4, captions.srt,
chapters.txt, cuts.jpg (frames either side of the cuts), edit-report.md and manifest.json.
Needs ffmpeg (any build) and Pillow (pip install pillow). Standard library otherwise.
"""
import argparse, array, functools, json, math, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "..", "fonts")
FONT_FILES = ["Poppins-ExtraBold.ttf", "Poppins-Bold.ttf"]
FONT_URL = "https://raw.githubusercontent.com/google/fonts/main/ofl/poppins/"
DEFAULT_FILLERS = ["um", "uh", "uhm", "umm", "er", "erm", "ah", "hmm"]
KEEP_REPEATS = {"very", "really", "that", "had", "is", "bye", "no", "yeah", "so", "ha", "go", "knock", "well"}
RETAKE_CUES = ["let me start over", "let me say that again", "let me try that again", "let me redo that",
               "let me rephrase that", "scratch that", "take two"]
FUNCTION_WORDS = {"a", "an", "the", "of", "to", "for", "and", "that", "with", "on", "in", "is", "our", "my",
                  "your", "their", "at", "by", "from", "as", "or", "but", "so", "i", "we", "it"}
PRESETS = {
    # pauses longer than "max" shrink to a beat: "mid" inside a sentence, "end" after one,
    # "topic" at a long gap; removals shorter than "min_cut" are left alone (a jump cut costs more)
    "youtube": {"max": 0.50, "mid": 0.30, "end": 0.45, "topic": 0.90, "min_cut": 0.40, "punch_in": 1.10, "lufs": -14},
    "tight": {"max": 0.30, "mid": 0.22, "end": 0.25, "topic": 0.50, "min_cut": 0.25, "punch_in": 1.15, "lufs": -14},
    "podcast": {"max": 0.80, "mid": 0.40, "end": 0.60, "topic": 1.00, "min_cut": 0.60, "punch_in": 0, "lufs": -16},
}
PRE_ROLL = 0.10        # never start a kept piece less than this before a word
VERTICAL = (1080, 1920)
EYE_LINE = 0.38
SR = 8000              # analysis sample rate (enough to find speech edges, and fast)
WIN = 0.01             # 10 ms analysis windows
WARNINGS = []


def warn(msg):
    WARNINGS.append(msg)
    print("warning: " + msg, file=sys.stderr)


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        sys.exit("ffmpeg failed:\n" + r.stderr[-1500:])
    return r


def check_tools():
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        sys.exit("ffmpeg is not installed. Mac: brew install ffmpeg. Windows: winget install ffmpeg. "
                 "Linux: sudo apt install ffmpeg.")


def probe(path):
    out = json.loads(run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height,r_frame_rate:stream_tags=rotate:format=duration",
                          "-of", "json", path]).stdout)
    st = out["streams"][0]
    w, h = st["width"], st["height"]
    if str(st.get("tags", {}).get("rotate", "0")) in ("90", "270"):
        w, h = h, w
    num, _, den = st.get("r_frame_rate", "30/1").partition("/")
    try:
        fps = float(num) / float(den or 1)
    except (ValueError, ZeroDivisionError):
        fps = 30.0
    if not 23.5 <= fps <= 60.5:
        fps = 30.0
    return w, h, float(out["format"]["duration"]), fps


def stamp(t):
    t = max(0, t)
    h, rem = divmod(int(t), 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def clean(w):
    return re.sub(r"[^\w']", "", w.lower())


# ---------- looking and listening ----------

def audio_energy(src):
    """Loudness of every 10 ms of audio, in dB, plus the room's noise floor."""
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-vn", "-ac", "1", "-ar", str(SR),
                        "-f", "s16le", "-"], capture_output=True)
    if p.returncode != 0 or not p.stdout:
        return [], -60.0
    a = array.array("h")
    a.frombytes(p.stdout[: len(p.stdout) // 2 * 2])
    n = int(SR * WIN)
    db = []
    import operator
    for i in range(0, len(a) - n, n):
        seg = a[i:i + n]
        rms = math.sqrt(sum(map(operator.mul, seg, seg)) / n) / 32768
        db.append(20 * math.log10(rms) if rms > 1e-6 else -120.0)
    floor = sorted(db)[len(db) // 10] if db else -60.0
    return db, floor


def visual_events(src):
    """Black frames and shot changes (both found by filters in every ffmpeg build)."""
    # skipping the loop filter and non-reference frames roughly triples decode speed; cut points
    # are snapped to whole frames afterwards anyway
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-an", "-skip_loop_filter:v", "all",
                        "-skip_frame:v", "noref", "-i", src, "-vf",
                        "scale=160:-2,blackdetect=d=0.08:pix_th=0.10:pic_th=0.90,select='gt(scene\\,0.3)',showinfo",
                        "-f", "null", "-"], capture_output=True, text=True)
    blacks = [(float(a), float(b)) for a, b in re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", r.stderr)]
    scenes = [float(t) for t in re.findall(r"pts_time:([\d.]+)", r.stderr)]
    return blacks, scenes


def loud(db, t):
    i = int(t / WIN)
    return db[i] if 0 <= i < len(db) else -120.0


def quiet_after(db, floor, t, limit, stop):
    """First time at or after t where 30 ms stay under the noise floor + 6 dB, plus 30 ms.
    None if there's no such spot within limit (or before stop)."""
    th, k, run_q = floor + 6, t, 0.0
    while k < min(t + limit, stop):
        run_q = run_q + WIN if loud(db, k) < th else 0.0
        if run_q >= 0.03:
            return min(k + 0.03, stop)
        k += WIN
    return None


def quiet_before(db, floor, t, limit, stop):
    th, k, run_q = floor + 6, t, 0.0
    while k > max(t - limit, stop):
        run_q = run_q + WIN if loud(db, k) < th else 0.0
        if run_q >= 0.03:
            return max(k - 0.03, stop)
        k -= WIN
    return None


# ---------- deciding what to cut ----------

def sentences_of(words, gap=0.8):
    out, start = [], 0
    for i, w in enumerate(words):
        nxt = words[i + 1] if i + 1 < len(words) else None
        if nxt is None or w["w"][-1:] in ".?!" or nxt["start"] - w["end"] > gap:
            out.append((start, i))
            start = i + 1
    return out


def mark(words, spec):
    """A reason for every word that goes (None = keep), and possible retakes for a person."""
    reason = [None] * len(words)
    maybe = []
    fillers = set(clean(f) for f in spec.get("fillers", DEFAULT_FILLERS))
    extra = [f.lower().split() for f in spec.get("extra_fillers", [])]
    cw = [clean(w["w"]) for w in words]
    for i, c in enumerate(cw):
        nxt = cw[i + 1] if i + 1 < len(cw) else ""
        prv = cw[i - 1] if i else ""
        agreement = (c == "mm" and nxt == "hmm") or (c == "hmm" and prv == "mm")  # "mm hmm" means yes
        if (c in fillers or (c == "mm" and "mm" in fillers)) and not agreement:
            gap_l = words[i]["start"] - words[i - 1]["end"] if i else 1
            gap_r = words[i + 1]["start"] - words[i]["end"] if i + 1 < len(words) else 1
            if max(gap_l, gap_r) >= 0.04:  # fused to both neighbours: cutting it would clip them
                reason[i] = "filler"
        for ph in extra:
            if cw[i:i + len(ph)] == ph and (len(ph) > 1 or words[i]["w"].endswith(",")
                                             or (i > 0 and words[i - 1]["w"].endswith(","))):
                for k in range(i, i + len(ph)):
                    reason[k] = "filler"
    if spec.get("stutters", True):
        for i in range(len(words) - 1):
            gap = words[i + 1]["start"] - words[i]["end"]
            if (cw[i] and cw[i] == cw[i + 1] and cw[i] not in KEEP_REPEATS and gap < 0.25
                    and not words[i]["w"].endswith(",")):
                reason[i] = reason[i] or "stutter"
        for i in range(len(words) - 3):  # "it's the it's the engine": a restarted phrase
            if (cw[i:i + 2] == cw[i + 2:i + 4] and cw[i] and cw[i] not in KEEP_REPEATS
                    and words[i + 2]["start"] - words[i + 1]["end"] < 0.5):
                reason[i] = reason[i] or "stutter"
                reason[i + 1] = reason[i + 1] or "stutter"
    if spec.get("retakes", True):
        sents = sentences_of(words)
        text = " ".join(cw)
        for cue in RETAKE_CUES:
            for m in re.finditer(r"\b" + re.escape(cue) + r"\b", text):
                ci = text[:m.start()].count(" ")
                ce = ci + len(cue.split()) - 1
                si = next((a for a, b in sents if a <= ci <= b), ci)
                prev = next(((a, b) for a, b in sents if b == si - 1), None)
                nxt = next(((a, b) for a, b in sents if a == ce + 1), None)
                start = si
                if prev and nxt:  # the take before the cue goes only if the next one repeats it
                    pa = set(cw[prev[0]:prev[1] + 1])
                    na = set(cw[nxt[0]:nxt[1] + 1])
                    if pa and len(pa & na) / len(pa) >= 0.5:
                        start = prev[0]
                for k in range(start, min(ce + 1, len(words))):
                    reason[k] = reason[k] or "retake"
        for (a1, b1), (a2, b2) in zip(sents, sents[1:]):
            if words[a2]["start"] - words[b1]["end"] > 20:
                continue
            n = min(3, b1 - a1 + 1, b2 - a2 + 1)
            same_open = n >= 2 and cw[a1:a1 + n] == cw[a2:a2 + n]
            if not same_open:
                continue
            unfinished = words[b1]["w"][-1:] not in ".?!"
            if unfinished and (b1 - a1 + 1) <= 8:
                for k in range(a1, b1 + 1):
                    reason[k] = reason[k] or "retake"
            else:
                maybe.append((words[a1]["start"], " ".join(w["w"] for w in words[a1:b1 + 1]),
                              " ".join(w["w"] for w in words[a2:b2 + 1])))
    for item in spec.get("cut", []):
        s, e = float(item[0]), float(item[1])
        for i, w in enumerate(words):
            if w["start"] >= s - 0.02 and w["end"] <= e + 0.02:
                reason[i] = "cut: " + (item[2] if len(item) > 2 else "by hand")
    for s, e in spec.get("keep", []):
        for i, w in enumerate(words):
            if w["start"] >= s - 0.02 and w["end"] <= e + 0.02:
                reason[i] = None
    return reason, maybe


def plan_spans(words, reason, spec, total, fps, db, floor, blacks, scenes):
    """Source-time spans to keep, and a log of every removal with its reason."""
    st = PRESETS.get(spec.get("style", "youtube"), PRESETS["youtube"])
    max_gap = float(spec.get("pauses", {}).get("max", st["max"]))
    use_voice = spec.get("voiced_gaps", True) and db
    kept = [i for i, r in enumerate(reason) if r is None]
    if not kept:
        sys.exit("Every word would be cut; check the cut ranges")
    marks = sorted(scenes + [t for b in blacks for t in b])

    def snap(t):
        return round(t * fps) / fps

    def card_in(a, b):
        return any(bs < b and be > a for bs, be in blacks) or any(a < t < b for t in scenes)

    def word_end(i):  # the transcriber's end, pushed out to where the sound actually stops
        e = words[i]["end"]
        q = quiet_after(db, floor, e, 0.25, words[i + 1]["start"] if i + 1 < len(words) else total) if db else None
        return q if q is not None else e + 0.03

    def word_start(i):
        s = words[i]["start"]
        q = quiet_before(db, floor, s, 0.20, words[i - 1]["end"] if i else 0.0) if db else None
        return min(q if q is not None else s - 0.03, s - PRE_ROLL)

    spans, removed = [], []
    first = kept[0]
    s0 = max(0.0, word_start(first) - 0.15)
    for t in marks:  # don't open on the last frames of a title card or another shot
        if s0 - 1.0 < t < words[first]["start"] - 0.05:
            s0 = max(s0, t + 0.04)
    open_from = 0.0
    for ks, ke in sorted((float(x), float(y)) for x, y in spec.get("keep", [])):
        if ke <= words[first]["start"] - 0.2 and ks < s0:  # a kept opening card before the first word
            spans.append((ks, ke))
            open_from = ke
    cur = [s0, word_end(first)]
    if first > 0:
        why = ", ".join(sorted({reason[k].split(":")[0] for k in range(first) if reason[k]})) or "opening"
        removed.append((open_from, s0, why, " ".join(words[k]["w"] for k in range(first))))
    elif spans and s0 - open_from >= 0.12:
        removed.append((open_from, s0, "opening", ""))
    elif s0 > 0.5 and not spans:
        removed.append((0.0, s0, "opening", ""))
    for prev, i in zip(kept, kept[1:]):
        between = list(range(prev + 1, i))
        out_e, in_s = word_end(prev), word_start(i)
        gap = words[i]["start"] - words[prev]["end"]
        sentence_end = words[prev]["w"][-1:] in ".?!"
        long_gap = gap > 3.0 or card_in(words[prev]["end"], words[i]["start"])
        target = st["topic"] if long_gap else st["end"] if sentence_end else st["mid"]
        voiced = (use_voice and gap > 0.35 and not between and
                  sum(1 for k in range(int((out_e + 0.05) / WIN), int((in_s - 0.05) / WIN))
                      if 0 <= k < len(db) and db[k] > floor + 12) * WIN > 0.15)
        if not (between or gap > max_gap or voiced):
            cur[1] = word_end(i)
            continue
        # keep part of the pause as a beat: 60% after the last word, 40% before the next
        free = max(0.0, in_s - out_e)
        keep_beat = min(target, free)
        cut_s = out_e + keep_beat * 0.6
        cut_e = in_s - keep_beat * 0.4
        for bs, be in blacks:  # remove a whole title card or black gap, not most of it
            if bs < cut_e and be > cut_s:
                cut_s, cut_e = min(cut_s, max(out_e, bs)), max(cut_e, min(in_s, be))
        for t in scenes:  # a shot change just inside a kept edge: move the edge past it
            if cut_e <= t < cut_e + 0.5 and t < words[i]["start"] - 0.05:
                cut_e = t
            if cut_s - 0.5 < t <= cut_s and t > words[prev]["end"] + 0.05:
                cut_s = t
        cut_s, cut_e = snap(cut_s), snap(cut_e)
        size = cut_e - cut_s
        if size < (0.12 if between else st["min_cut"]):
            cur[1] = word_end(i)
            continue
        # a "keep" range inside the gap (a title card, a silent demo) stays, split out as its own piece
        holds = sorted((max(cut_s, float(ks)), min(cut_e, float(ke))) for ks, ke in spec.get("keep", [])
                       if float(ks) < cut_e and float(ke) > cut_s)
        for ks, ke in holds:
            if ks - cut_s >= 0.12:
                cur[1] = snap(cut_s)
                spans.append(tuple(cur))
                removed.append((cut_s, ks, "pause", ""))
                cur = [snap(ks), snap(ke)]
            else:
                cur[1] = snap(ke)
            cut_s = snap(ke)
        if cut_e - cut_s < 0.12:
            cur[1] = word_end(i)
            continue
        cur[1] = cut_s
        spans.append(tuple(cur))
        if between:
            why = ", ".join(sorted({reason[k].split(":")[0] for k in between}))
        elif long_gap:
            why = "long gap or title card" if card_in(cut_s, cut_e) else "long gap"
        else:
            why = "sound with no words" if voiced and gap <= max_gap else "pause"
        removed.append((cut_s, cut_e, why, " ".join(words[k]["w"] for k in between)))
        cur = [cut_e, word_end(i)]
    end = min(total, cur[1] + 0.4)
    for t in marks:  # stop before an end card or a new shot
        if cur[1] < t < end:
            end = t - 0.04
    cur[1] = end
    spans.append(tuple(cur))
    if total - end > 0.5:
        removed.append((end, total, "ending", ""))
    spans = [(snap(s), snap(e)) for s, e in spans if e - s > 0.05]
    merged = []  # a kept piece under 0.4 s flickers; join it only to a touching neighbour
    for s, e in spans:
        if merged and (e - s < 0.4 or merged[-1][1] - merged[-1][0] < 0.4) and s - merged[-1][1] < 0.15:
            merged[-1] = (merged[-1][0], e)
        else:
            merged.append((s, e))
    return merged, removed


def to_out(t, spans):
    acc = 0.0
    for s, e in spans:
        if t <= s:
            return acc
        if t <= e:
            return acc + (t - s)
        acc += e - s
    return acc


# ---------- captions ----------

def srt_time(t):
    ms = int(round(max(0, t) * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def apply_replace(text, rep):
    for a, b in rep.items():
        text = re.sub(r"\b" + re.escape(a) + r"\b", b, text, flags=re.I)
    return text


def caption_events(words, reason, spans, rep, max_chars=42, lines=2, fps=30.0):
    """Captions in output time: at most `lines` lines of `max_chars`, 1 to 7 s, breaking at
    sentence ends and pauses; gaps under 0.3 s closed, 2 frames left between captions."""
    kept, prev_w = [], None
    for i, r in enumerate(reason):
        if r is not None:
            continue
        w = words[i]["w"]
        if (prev_w is None or prev_w[-1:] in ".?!") and w[:1].islower():
            w = w[:1].upper() + w[1:]
        kept.append((to_out(words[i]["start"], spans), to_out(words[i]["end"], spans), w))
        prev_w = w
    limit = max_chars * lines
    events, cur = [], []
    for j, (s, e, w) in enumerate(kept):
        cur.append((s, e, w))
        nxt = kept[j + 1] if j + 1 < len(kept) else None
        text = " ".join(x[2] for x in cur)
        too_long = nxt is not None and len(text) + 1 + len(nxt[2]) > limit
        if (nxt is None or w[-1:] in ".?!" or too_long or nxt[0] - e > 0.6 or e - cur[0][0] > 6.0
                or (w[-1:] in ",;:" and len(text) > limit * 0.6)):
            events.append([cur[0][0], cur[-1][1], apply_replace(text, rep)])
            cur = []
    two = 2 / fps
    for k, ev in enumerate(events):
        nxt = events[k + 1][0] if k + 1 < len(events) else ev[1] + 1.5
        end = max(ev[1] + 0.5, ev[0] + 1.0)  # time to finish reading
        if nxt - end < 0.3:
            end = nxt - two  # close small gaps so captions don't flicker
        ev[1] = max(ev[0] + 0.5, min(end, nxt - two, ev[0] + 7.0))
    return events


def split_lines(text, max_chars=42):
    """Best two-line break: both lines fit, similar length, not after a small word or inside a name."""
    if len(text) <= max_chars:
        return [text]
    words = text.split()
    best = None
    for k in range(1, len(words)):
        a, b = " ".join(words[:k]), " ".join(words[k:])
        cost = abs(len(a) - len(b)) + (100 if max(len(a), len(b)) > max_chars else 0)
        if clean(words[k - 1]) in FUNCTION_WORDS:
            cost += 25
        if words[k - 1][:1].isupper() and words[k][:1].isupper() and words[k - 1][-1:] not in ".,?!":
            cost += 25  # don't split "Osiris / Rex"
        if words[k - 1][-1:] in ",.;:":
            cost -= 10
        if best is None or cost < best[0]:
            best = (cost, [a, b])
    return best[1]


def write_srt(events, path):
    with open(path, "w", encoding="utf-8") as fh:
        for n, (s, e, text) in enumerate(events, 1):
            fh.write(f"{n}\n{srt_time(s)} --> {srt_time(e)}\n" + "\n".join(split_lines(text)) + "\n\n")


def load_pillow():
    try:
        from PIL import Image, ImageDraw, ImageFont
        return Image, ImageDraw, ImageFont
    except ImportError:
        sys.exit("Burned-in captions and the cut sheet need Pillow: pip install pillow")


@functools.lru_cache(maxsize=None)
def font(size):
    _, _, ImageFont = load_pillow()
    path = os.path.join(FONT_DIR, FONT_FILES[0])
    if not os.path.exists(path):
        os.makedirs(FONT_DIR, exist_ok=True)
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


def burn_overlays(events, out_w, out_h, length, tmp):
    """Transparent PNG per caption plus an ffmpeg concat list with the timing."""
    Image, ImageDraw, _ = load_pillow()
    vertical = out_h > out_w
    size = int(out_h * (0.04 if vertical else 0.042))
    f = font(size)
    bottom = out_h * (0.66 if vertical else 0.92)  # vertical: above the platform buttons and text
    stroke = max(2, int(size * 0.08))
    Image.new("RGBA", (out_w, out_h), (0, 0, 0, 0)).save(os.path.join(tmp, "cap-blank.png"))
    listing, t = [], 0.0
    for n, (s, e, text) in enumerate(events):
        if s > t + 0.001:
            listing.append(("cap-blank.png", s - t))
        img = Image.new("RGBA", (out_w, out_h), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        lines = split_lines(text, 32 if vertical else 42)
        lh = int(size * 1.22)
        top = bottom - lh * len(lines)
        for i, ln in enumerate(lines):
            d.text((out_w / 2 + 2, top + i * lh + 3), ln, font=f, fill=(0, 0, 0, 130), anchor="ma")
            d.text((out_w / 2, top + i * lh), ln, font=f, fill=(255, 255, 255, 255), anchor="ma",
                   stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
        name = f"cap-{n:05d}.png"
        img.save(os.path.join(tmp, name), optimize=True)
        listing.append((name, max(0.04, e - s)))
        t = max(t, e)
    if length > t:
        listing.append(("cap-blank.png", length - t))
    with open(os.path.join(tmp, "captions.txt"), "w", encoding="utf-8") as fh:
        fh.write("ffconcat version 1.0\n")
        for name, d in listing:
            fh.write(f"file '{name}'\nduration {d:.3f}\n")
        fh.write(f"file '{listing[-1][0]}'\n")
    return "captions.txt"


# ---------- render ----------

def frame_filter(spec, src_w, src_h, zoom):
    if spec.get("format", "source") == "vertical":
        ow, oh = VERTICAL
        ch = int(src_h / zoom) // 2 * 2
        cw = int(ch * ow / oh) // 2 * 2
        x = int(min(max(float(spec.get("focus_x", 0.5)) * src_w - cw / 2, 0), src_w - cw))
        y = int(min(max(EYE_LINE * src_h * (1 - 1 / zoom), 0), src_h - ch))
        return f"crop={cw}:{ch}:{x}:{y},scale={ow}:{oh}:flags=lanczos,setsar=1"
    if zoom <= 1.001:
        return "setsar=1"
    cw, ch = int(src_w / zoom) // 2 * 2, int(src_h / zoom) // 2 * 2
    x = int(min(max(float(spec.get("focus_x", 0.5)) * src_w - cw / 2, 0), src_w - cw))
    y = int(min(max(EYE_LINE * src_h * (1 - 1 / zoom), 0), src_h - ch))
    return f"crop={cw}:{ch}:{x}:{y},scale={src_w}:{src_h}:flags=lanczos,setsar=1"


def zoom_plan(spans, spec, scenes, blacks=()):
    """Change framing where a jump cut needs hiding: always at a cut that removed a second or
    more, otherwise only when at least 4 s (2.5 in tight) passed since the last change. A cut
    onto a new camera shot needs no punch-in."""
    st = PRESETS.get(spec.get("style", "youtube"), PRESETS["youtube"])
    punch = min(1.2, float(spec.get("punch_in", st["punch_in"]) or 0))
    if not punch or punch <= 1.0:
        return [1.0] * len(spans)
    hold = 2.5 if spec.get("style") == "tight" else 4.0
    zooms, z, since = [], 1.0, 0.0
    for i, (s, e) in enumerate(spans):
        if i > 0:
            removed = s - spans[i - 1][1]
            new_shot = any(spans[i - 1][1] - 0.1 <= t <= s + 0.1 for t in scenes)
            if not new_shot and (removed >= 1.0 or (since >= hold and removed >= st["min_cut"])):
                z = punch if z == 1.0 else 1.0
                since = 0.0
        card = any(bs <= s + 0.05 and be >= e - 0.05 for bs, be in blacks)
        zooms.append(1.0 if card else z)  # never punch into a title card
        since += e - s
    return zooms


def render_chunks(spec, src, spans, zooms, src_w, src_h, fps, tmp, chunk=60):
    """One ffmpeg pass per group of pieces (trim and concat in a single filter graph):
    frame-exact, so sound and picture stay together however many cuts there are."""
    parts = []
    groups = [list(range(i, min(i + chunk, len(spans)))) for i in range(0, len(spans), chunk)]
    for gi, idx in enumerate(groups):
        seek = max(0.0, math.floor((spans[idx[0]][0] - 1.0) * fps) / fps)
        end = spans[idx[-1]][1]
        graph, labels = [], []
        for n, i in enumerate(idx):
            s, e = spans[i][0] - seek, spans[i][1] - seek
            d = e - s
            graph.append(f"[0:v]trim=start={s:.6f}:end={e:.6f},setpts=PTS-STARTPTS,"
                         f"{frame_filter(spec, src_w, src_h, zooms[i])}[v{n}]")
            graph.append(f"[0:a]atrim=start={s:.6f}:end={e:.6f},asetpts=PTS-STARTPTS,"
                         f"afade=t=in:d=0.004,afade=t=out:st={max(0, d - 0.004):.4f}:d=0.004[a{n}]")
            labels.append(f"[v{n}][a{n}]")
        graph.append(f"{''.join(labels)}concat=n={len(idx)}:v=1:a=1[cv][ca]")
        out = os.path.join(tmp, f"part-{gi:03d}.mov")
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{seek:.6f}", "-t", f"{end - seek + 0.5:.3f}", "-i", src,
             "-filter_complex", ";".join(graph), "-map", "[cv]", "-map", "[ca]", "-r", f"{fps:.6f}",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-profile:v", "high", "-g", "60",
             "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
             "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", out])
        parts.append(os.path.basename(out))
        print(f"  rendered pieces {idx[0] + 1}-{idx[-1] + 1} of {len(spans)}", flush=True)
    with open(os.path.join(tmp, "parts.txt"), "w", encoding="utf-8") as fh:
        fh.writelines(f"file '{p}'\n" for p in parts)
    joined = os.path.join(tmp, "joined.mov")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", "parts.txt", "-c", "copy", joined], cwd=tmp)
    return joined


def stream_durations(path):
    out = json.loads(run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,duration",
                          "-of", "json", path]).stdout)
    return {s["codec_type"]: float(s.get("duration", 0) or 0) for s in out["streams"]}


def loudness(path, chain):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-vn", "-af",
                        ",".join(chain + ["loudnorm=print_format=json"]), "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S)
    return json.loads(m.group(0)) if m else None


def audio_chain(joined, spec, floor):
    """Gain to about -20 LUFS, rumble filter, noise reduction set from the measured room noise,
    gentle compression, then a limiter and one clean gain to the target: linear, no pumping."""
    a = spec.get("audio", {})
    st = PRESETS.get(spec.get("style", "youtube"), PRESETS["youtube"])
    target = float(a.get("lufs", st["lufs"]))
    m = loudness(joined, [])
    gain = (-20.0 - float(m["input_i"])) if m and m["input_i"] not in ("-inf", "inf") else 0.0
    chain = [f"volume={gain:.2f}dB", "highpass=f=80"]
    floor_after = floor + gain
    if a.get("denoise", True) and floor_after > -60:
        chain.append(f"afftdn=nr=10:nf={max(-80, min(-20, round(floor_after)))}:tn=1")
    chain.append("acompressor=threshold=-24dB:ratio=3:attack=5:release=120")
    m2 = loudness(joined, chain)
    g2 = (target - float(m2["input_i"])) if m2 and m2["input_i"] not in ("-inf", "inf") else 0.0
    limit = 10 ** ((-2.0 - g2) / 20)  # peaks end at -2 dBFS: headroom for the AAC encoder
    if limit < 0.0625:
        warn("the recording is very quiet; the limiter is working hard to reach the target loudness")
        limit = 0.0625
    chain += [f"alimiter=limit={min(1.0, limit):.4f}:level=false", f"volume={g2:.2f}dB"]
    return chain


def cut_sheet(out, spans, removed_sizes, path, n=18):
    """Frames 2 before and 2 after the biggest cuts, to check for flashes and jumps."""
    Image, ImageDraw, _ = load_pillow()
    fps = 30.0
    times, acc = [], 0.0
    for i, (s, e) in enumerate(spans[:-1]):
        acc += e - s
        times.append((removed_sizes[i] if i < len(removed_sizes) else 0, acc))
    picks = sorted(sorted(times, reverse=True)[:n], key=lambda x: x[1])
    if not picks:
        return None
    tw, th = 240, 135
    sheet = Image.new("RGB", (tw * 2 + 30, (th + 10) * len(picks)), "#111111")
    with tempfile.TemporaryDirectory() as tmp:
        for row, (_, t) in enumerate(picks):
            for col, dt in enumerate((-2 / fps, 2 / fps)):
                p = os.path.join(tmp, f"f{row}-{col}.jpg")
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(0, t + dt):.3f}", "-i", out,
                                "-frames:v", "1", "-vf", f"scale={tw}:{th}", p], capture_output=True)
                if os.path.exists(p):
                    sheet.paste(Image.open(p), (col * (tw + 10), row * (th + 10)))
            ImageDraw.Draw(sheet).text((tw * 2 + 14, row * (th + 10) + 4), stamp(t), fill=(200, 200, 200))
    sheet.save(path, quality=80)
    return path


def chapters_out(spec, spans, length):
    ch = spec.get("chapters") or []
    if not ch:
        return []
    out = []
    for t, title in sorted(ch, key=lambda c: float(c[0])):
        out.append((0.0 if float(t) <= 0.5 else to_out(float(t), spans), title))
    out[0] = (0.0, out[0][1])
    if len(out) < 3:
        warn("chapters: YouTube needs at least 3")
    for (a, _), (b, _) in zip(out, out[1:] + [(length, None)]):
        if b - a < 10:
            warn(f"chapters: one is under 10 s after editing ({stamp(a)})")
    return out


def main():
    ap = argparse.ArgumentParser(description="Edit a talking-head video.")
    ap.add_argument("spec")
    ap.add_argument("--transcript", default="work/transcript.json")
    ap.add_argument("--out", default="edited")
    ap.add_argument("--plan", action="store_true", help="write edit-plan.md only, no render")
    a = ap.parse_args()
    check_tools()
    spec = json.load(open(a.spec, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(a.spec))
    src = spec["video"] if os.path.isabs(spec["video"]) else os.path.join(base, spec["video"])
    if not os.path.exists(src):
        sys.exit(f"Video not found: {src}")
    words = json.load(open(a.transcript, encoding="utf-8"))["words"]
    src_w, src_h, total, fps = probe(src)
    os.makedirs(a.out, exist_ok=True)
    out_dir = os.path.abspath(a.out)
    print("  listening and looking...", flush=True)
    db, floor = audio_energy(src)
    blacks, scenes = visual_events(src)
    reason, maybe = mark(words, spec)
    spans, removed = plan_spans(words, reason, spec, total, fps, db, floor, blacks, scenes)
    length = sum(e - s for s, e in spans)
    speech_kinds = {}
    for item in removed:
        for k in item[2].split(", "):
            speech_kinds.setdefault(k, [0, 0.0])
            speech_kinds[k][0] += 1
            speech_kinds[k][1] += (item[1] - item[0]) / len(item[2].split(", "))
    big = sum(v[1] for k, v in speech_kinds.items() if k in ("long gap", "long gap or title card", "opening", "ending"))
    in_speech = (total - length) - big
    spoken = sum(1 for r in reason if r is None)
    wpm_before = len(words) / max(1.0, sum(w["end"] - w["start"] for w in words) + 0.35 * len(words)) * 60
    wpm_after = spoken / max(1.0, length) * 60
    if wpm_after > 190:
        warn(f"edited pace is {wpm_after:.0f} words per minute; over 190 starts to feel rushed. Try a gentler style")
    if (total - length) / total > 0.45:
        warn(f"{(total - length) / total * 100:.0f}% removed; over 45% usually means something was cut that shouldn't be")
    kinds = ", ".join(f"{v[0]} {k} ({v[1]:.0f} s)" for k, v in sorted(speech_kinds.items(), key=lambda x: -x[1][1]))
    summary = (f"{stamp(total)} -> {stamp(length)} ({(total - length) / total * 100:.0f}% shorter; "
               f"{in_speech:.0f} s from inside the talking, {big:.0f} s from long gaps, cards, opening and ending). "
               f"{len(spans) - 1} cuts, pace {wpm_after:.0f} words per minute. Removed: {kinds}")
    lines = [f"# Edit plan\n\n{summary}\n"]
    if maybe:
        lines.append("## Possible retakes, not cut (check and add to \"cut\" or leave)\n")
        lines += [f"- {stamp(t)}: \"{first[:90]}\" then \"{second[:90]}\"" for t, first, second in maybe]
        lines.append("")
    lines += ["## Removals\n", "| Source time | Removed | Why | Words |", "|---|---|---|---|"]
    for s, e, why, txt in removed:
        if why == "pause" and e - s < 1.0 and not txt:
            continue
        lines.append(f"| {stamp(s)} | {e - s:.1f} s | {why} | {txt[:80]} |")
    shown = sum(1 for s, e, why, txt in removed if not (why == "pause" and e - s < 1.0 and not txt))
    lines.append(f"\nPlus {len(removed) - shown} short pauses (under 1 s each).")
    name = "edit-plan.md" if a.plan else "edit-report.md"
    with open(os.path.join(out_dir, name), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print(summary)
    print(f"{name}: {os.path.join(out_dir, name)}")
    if a.plan:
        return
    zooms = zoom_plan(spans, spec, scenes, blacks)
    cap = spec.get("captions", {})
    vertical = spec.get("format") == "vertical"
    burn = cap.get("burn", vertical)
    rep = spec.get("replace", {})
    with tempfile.TemporaryDirectory() as tmp:
        joined = render_chunks(spec, src, spans, zooms, src_w, src_h, fps, tmp)
        dur = stream_durations(joined)
        if abs(dur.get("video", 0) - dur.get("audio", 0)) > 1.5 / fps:
            warn(f"picture and sound differ by {abs(dur['video'] - dur['audio']) * 1000:.0f} ms; check sync")
        chain = audio_chain(joined, spec, floor)
        out = os.path.abspath(os.path.join(out_dir, "edited.mp4"))
        out_w, out_h = VERTICAL if vertical else (src_w, src_h)
        events = caption_events(words, reason, spans, rep, max_chars=32 if (burn and vertical) else 42,
                                lines=1 if (burn and vertical) else 2, fps=fps)
        cmd = ["ffmpeg", "-y", "-hide_banner", "-nostats", "-i", joined]
        if burn:
            lst = burn_overlays(events, out_w, out_h, length, tmp)
            cmd += ["-f", "concat", "-safe", "0", "-i", lst, "-filter_complex",
                    f"[1:v]fps={fps:.6f},format=yuva420p[c];[0:v][c]overlay=0:0:format=yuv420:eof_action=pass,"
                    f"format=yuv420p[v];[0:a]{','.join(chain)},aresample=48000[a]", "-map", "[v]", "-map", "[a]"]
            cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-profile:v", "high", "-g", "60",
                    "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709"]
        else:
            cmd += ["-af", ",".join(chain) + ",aresample=48000", "-c:v", "copy"]  # picture is final already
        cmd += ["-c:a", "aac", "-b:a", "192k", "-ac", "2", "-movflags", "+faststart", out]
        print("  final pass: audio" + (" and captions" if burn else ""), flush=True)
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=tmp)
        if r.returncode != 0:
            sys.exit("ffmpeg failed:\n" + r.stderr[-1500:])
    if cap.get("srt", True):
        write_srt(caption_events(words, reason, spans, rep, fps=fps), os.path.join(out_dir, "captions.srt"))
    if burn and not vertical:
        warn("captions are burned in; don't also upload captions.srt to the same YouTube video (viewers see both)")
    sizes = [spans[i + 1][0] - spans[i][1] for i in range(len(spans) - 1)]
    sheet = cut_sheet(out, spans, sizes, os.path.join(out_dir, "cuts.jpg"))
    chapters = chapters_out(spec, spans, length)
    if chapters:
        with open(os.path.join(out_dir, "chapters.txt"), "w", encoding="utf-8") as fh:
            fh.write("\n".join(f"{stamp(t)} {title}" for t, title in chapters) + "\n")
    manifest = {"video": os.path.abspath(src), "edited": out, "bytes": os.path.getsize(out),
                "seconds_before": round(total, 1), "seconds_after": round(length, 1), "cuts": len(spans) - 1,
                "punch_ins": sum(1 for z in zooms if z > 1.0), "summary": summary,
                "captions": os.path.join(out_dir, "captions.srt"), "cut_sheet": sheet,
                "chapters": [[round(t, 1), title] for t, title in chapters],
                "kept_spans": [[round(x, 3), round(y, 3)] for x, y in spans], "warnings": WARNINGS}
    with open(os.path.join(out_dir, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, ensure_ascii=False)
    print(f"Done: {out}")
    if WARNINGS:
        print(f"{len(WARNINGS)} warning(s); check them before posting.")


if __name__ == "__main__":
    main()
