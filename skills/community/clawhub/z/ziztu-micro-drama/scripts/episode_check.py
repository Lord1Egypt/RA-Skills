#!/usr/bin/env python3
"""Check micro drama episode scripts (Fountain) before they go to Ziztu.

Usage:
  python3 episode_check.py EPISODE.fountain [MORE.fountain ...] [--target 90] [--json]
  python3 episode_check.py episodes/            (every .fountain file in the folder, in name order)
  python3 episode_check.py season.fountain      (a season file split by "# Episode N" sections)

What it measures, per episode:
  - runtime two ways: spoken lines plus action beats (about 2.5 words a second), and the screen time Ziztu's shot
    planner gives the scenes (about one minute per printed page, measured with the screenplay page layout);
  - the hook: how many seconds of material come before the [[HOOK: ...]] note and before the first spoken line;
  - the cliffhanger: that a [[CLIFFHANGER - type: ...]] note exists and how many seconds follow it (cut on the peak);
  - dialogue: line lengths, long speeches, delivery notes;
  - cast and places: speakers per scene, places per episode, cue names that would make two Ziztu characters out of
    one person, all-caps lines that would import as a character by mistake, look-alike names;
  - action lines: negative wording, "fading" emotions and on-screen text that should be a caption.
Across several episodes it also checks that cliffhanger types vary.

Standard library only (Python 3.8+). Exit code 1 when any ERROR is found, else 0.
"""
import argparse
import json
import math
import os
import re
import sys

# ----------------------------------------------------------------------------------------------- Fountain reading
# The rules follow Ziztu's own importer (fountain.io syntax), so what this script sees is what Ziztu will import.
TITLE_KEYS = {"title", "credit", "author", "authors", "written by", "source", "draft date", "date", "contact",
              "contact info", "notes", "note", "copyright", "revision", "episode", "series", "format", "genre",
              "logline"}
TITLE_LINE = re.compile(r"^([A-Za-z][A-Za-z ]{0,30}):\s*(.*)$")
HEADING_RE = re.compile(r"^(?:INT\.?/EXT|EXT\.?/INT|I/E|INT|EXT|EST)(?:[.\s]|$)", re.I)
TIMES = ["DAY", "NIGHT", "MORNING", "AFTERNOON", "EVENING", "CONTINUOUS", "LATER", "MOMENTS LATER", "DAWN", "DUSK",
         "SUNRISE", "SUNSET", "SAME TIME", "MAGIC HOUR", "SAME", "MIDNIGHT", "NOON", "GOLDEN HOUR", "PRE-DAWN",
         "TWILIGHT", "LATE NIGHT", "EARLY MORNING", "NIGHTFALL", "DAYBREAK", "A MOMENT LATER", "SECONDS LATER",
         "MINUTES LATER", "HOURS LATER", "THE NEXT DAY", "NEXT DAY", "FLASHBACK", "PRESENT DAY", "DREAM"]
TIME_RE = re.compile(r"^(?:" + "|".join(re.escape(t) for t in sorted(TIMES, key=len, reverse=True)) + r")\b", re.I)
# Staging in depth: someone or something placed near the camera or far from it, or air between the planes.
DEPTH_RE = re.compile(r"\b(fore-?ground|back-?ground|behind (?:him|her|them|it|us|the|[A-Z][a-z]+)|in the doorway|"
                      r"through the (?:glass|window|windows|doorway|door|arch|crowd)|across the (?:room|hall|street|"
                      r"table|terrace|office|lobby|corridor)|at the far|far (?:end|side|door|doorway|wall|corner|table|window|edge)|at the end of the|in the distance|"
                      r"over (?:his|her|their|[A-Z][a-z]+'s) shoulder|at the next table|from the (?:doorway|stairs|"
                      r"balcony|corridor|landing|car)|watches from|haze|hazy|mist|steam|fog|smoke|dust in)\b", re.I)
CLOSING = {"FADE OUT.", "FADE OUT", "FADE TO BLACK.", "CUT TO BLACK.", "FADE TO WHITE.", "THE END", "THE END."}
SHOT_START = re.compile(
    r"^(?:(?:EXTREME |MEDIUM |MED\. )?CLOSE(?:[ -]?UP| ON)|ANGLE ON|(?:ANOTHER|NEW|DIFFERENT|SAME|REVERSE|HIGH|LOW|WIDE"
    r"|DUTCH) ANGLE|REVERSE (?:ON|SHOT)|(?:EXTREME )?WIDE (?:ON|SHOT)|E?CU(?: ON)?|MCU|(?:MEDIUM|FULL|TWO|THREE|"
    r"ESTABLISHING|TRACKING|AERIAL|CRANE|MOVING|DOLLY|STEADICAM|HANDHELD|UNDERWATER|INSERT|MASTER|OVERHEAD|POV|COWBOY"
    r"|LONG) SHOT|TWO-SHOT|OVER(?: |-)THE(?: |-)SHOULDER|OTS|P\.?O\.?V\.?|INSERT|BACK (?:ON|TO SCENE)|FAVOU?R(?:ING)?"
    r" ON|PUSH (?:IN|OUT)|PULL (?:BACK|OUT)|PAN (?:TO|ACROSS|UP|DOWN)|TILT (?:UP|DOWN)|ZOOM (?:IN|OUT|ON)|BIRD'S[ -]"
    r"EYE|AERIAL(?: VIEW)?|SPLIT SCREEN|SERIES OF SHOTS)(?=$|[\s.,:;-])")


def has_upper(s):
    return any(c.isupper() for c in s)


def has_lower(s):
    return any(c.islower() for c in s)


def looks_like_shot(line):
    t = line.strip()
    if not t or len(t) > 80 or t.endswith("TO:") or not has_upper(t) or has_lower(t):
        return False
    return bool(SHOT_START.match(t)) or bool(re.search(r"\bP\.?O\.?V\.?$", t))


def is_cue(line):
    t = line.strip()
    if t.startswith("@"):
        return len(t) > 1
    if len(t) > 50 or t.endswith(":") or HEADING_RE.match(t):
        return False
    name = re.sub(r"\s*\^\s*$", "", t).split("(")[0].strip()
    return bool(name) and has_upper(name) and not has_lower(name) and any(c.isalpha() for c in name)


def cue_name(text):
    t = re.sub(r"^@", "", text)
    t = re.sub(r"\s*\^\s*$", "", t)
    t = re.sub(r"\s*\([^)]*\)", "", t)
    t = re.sub(r"\s*\(.*$", "", t).strip().upper()
    return re.sub(r"[\s.,:;]+$", "", re.sub(r"\s+", " ", t))


def cue_extensions(text):
    return [x.strip().upper() for x in re.findall(r"\(([^)]*)\)", text)]


def parse_heading(text):
    t = re.sub(r"\s+", " ", text).strip()
    t = re.sub(r"\s*#[A-Za-z0-9.-]{1,12}#\s*$", "", t)
    m = re.match(r"^(INT\.?/EXT\.?|EXT\.?/INT\.?|I/E\.?|INT\.?|EXT\.?|EST\.?)\s*", t, re.I)
    rest = t[m.end():] if m else t
    rest = rest.lstrip(". ")
    parts = [p.strip() for p in re.split(r"\s+(?:-{1,2}|–|—)\s+|\s*(?:–|—|--)\s*", rest) if p.strip()]
    time = ""
    if len(parts) > 1 and TIME_RE.match(parts[-1]):
        time = parts.pop().upper()
    place = " - ".join(parts).upper()
    return place, time


def parse_fountain(text):
    """Returns (title_page dict, elements). An element is a dict: t (type), x (text), line (1-based line number)."""
    text = text.replace("﻿", "").replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"/\*[\s\S]*?\*/", "", text)
    lines = text.split("\n")
    n = len(lines)
    blank = lambda i: i >= n or i < 0 or lines[i].strip() == ""  # noqa: E731
    title = {}
    i = 0
    while i < n and blank(i):
        i += 1
    first = TITLE_LINE.match(lines[i].strip()) if i < n else None
    if first and first.group(1).strip().lower() in TITLE_KEYS:
        key = None
        while i < n and not blank(i):
            raw = lines[i]
            m = TITLE_LINE.match(raw.strip()) if re.match(r"^\s{0,2}\S", raw) else None
            if m:
                key = m.group(1).strip().lower()
                title[key] = m.group(2).strip()
            elif key:
                title[key] = (title[key] + "\n" + raw.strip()).strip()
            i += 1
    start = i
    els = []

    def push(t, x, ln, **extra):
        e = {"t": t, "x": x.strip() if isinstance(x, str) else x, "line": ln + 1}
        e.update(extra)
        els.append(e)

    def prev_blank(k):
        return k == start or blank(k - 1)

    while i < n:
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if re.match(r"^={3,}$", line):
            push("pagebreak", "", i)
            i += 1
            continue
        m = re.match(r"^(#{1,6})\s*(.*)$", line)
        if m:
            push("section", m.group(2), i, depth=len(m.group(1)))
            i += 1
            continue
        m = re.match(r"^=(?!=)\s*(.*)$", line)
        if m:
            push("synopsis", m.group(1), i)
            i += 1
            continue
        if line.startswith("[["):
            j = i
            parts = []
            while j < n:
                parts.append(lines[j].strip())
                if "]]" in lines[j]:
                    break
                j += 1
            whole = "\n".join(parts)
            nm = re.match(r"^\[\[([\s\S]*?)\]\]$", whole)
            if nm and blank(j + 1):
                push("note", nm.group(1), i)
                i = j + 1
                continue
        if re.match(r"^>.*<$", line):
            parts = []
            k = i
            while i < n and re.match(r"^>.*<$", lines[i].strip()):
                parts.append(re.sub(r"\s*<$", "", re.sub(r"^>\s*", "", lines[i].strip())))
                i += 1
            push("centered", "\n".join(parts), k)
            continue
        m = re.match(r"^>\s*(.*)$", line)
        if m:
            push("transition", m.group(1).upper(), i)
            i += 1
            continue
        m = re.match(r"^\.(?=[^.\s])(.*)$", line)
        if m and prev_blank(i):
            place, time = parse_heading(m.group(1))
            push("scene", m.group(1), i, place=place, time=time)
            i += 1
            continue
        if HEADING_RE.match(line) and prev_blank(i):
            place, time = parse_heading(line)
            push("scene", line, i, place=place, time=time)
            i += 1
            continue
        if line.startswith("~"):
            parts = []
            k = i
            while i < n and lines[i].strip().startswith("~"):
                parts.append(re.sub(r"^~\s?", "", lines[i].strip()))
                i += 1
            push("lyrics", "\n".join(parts), k)
            continue
        forced_action = line.startswith("!") and not line.startswith("!!")
        if not forced_action and prev_blank(i) and (line.startswith("@") or (not blank(i + 1) and is_cue(line))):
            cue = re.sub(r"\s*\^\s*$", "", re.sub(r"^@", "", line)).strip()
            push("character", cue.upper(), i, name=cue_name(cue), ext=cue_extensions(cue))
            i += 1
            last = None
            while i < n and not blank(i):
                t = lines[i].strip()
                if re.match(r"^\(.*\)$", t):
                    push("paren", t, i)
                    last = els[-1]
                elif last is not None and last["t"] == "dialogue":
                    last["x"] += "\n" + t
                else:
                    push("dialogue", re.sub(r"^~\s?", "", t), i)
                    last = els[-1]
                i += 1
            continue
        if not forced_action and prev_blank(i) and blank(i + 1) and has_upper(line) and not has_lower(line) and (
                line.endswith("TO:") or line in CLOSING):
            push("transition", line, i)
            i += 1
            continue
        if line.startswith("!!") and len(line) > 2 and blank(i + 1):
            push("shot", line[2:].strip().upper(), i)
            i += 1
            continue
        if not forced_action and prev_blank(i) and blank(i + 1) and looks_like_shot(line):
            push("shot", line, i)
            i += 1
            continue
        parts = []
        k = i
        first_line = True
        while i < n and not blank(i):
            r = lines[i].rstrip()
            if first_line and forced_action:
                r = re.sub(r"^(\s*)!", r"\1", r)
            parts.append(r.strip())
            first_line = False
            i += 1
        push("action", " ".join(parts), k, first=parts[0] if parts else "", nlines=len(parts))
    return title, els


# ----------------------------------------------------------------------------------------------- page layout
# Screenplay layout (12 pt Courier, 54 lines a page): width in characters and blank lines before, per element.
LAYOUT = {"scene": (60, 1), "action": (60, 1), "shot": (60, 1), "character": (38, 1), "paren": (25, 0),
          "dialogue": (35, 0), "lyrics": (35, 0), "transition": (60, 1), "centered": (60, 1)}
PAGE_LINES = 54


WIDE_RE = re.compile(r"[\u1100-\u11ff\u2e80-\u303f\u3040-\u30ff\u3130-\u318f\u3400-\u4dbf\u4e00-\u9fff\uac00-\ud7af"
                     r"\uf900-\ufaff\uff00-\uffef]")
CJK_RE = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")


def wrapped_lines(text, width):
    count = 0
    for para in str(text).split("\n"):
        if WIDE_RE.search(para):
            # Chinese, Japanese and Korean: a full-width character takes 5/3 of a column and lines break anywhere
            cols = sum(5.0 / 3 if WIDE_RE.match(ch) else 1 for ch in para.strip())
            count += max(1, int(math.ceil(cols / width)))
            continue
        words = para.split()
        if not words:
            count += 1
            continue
        cur = 0
        lines = 1
        for w in words:
            need = len(w) if cur == 0 else cur + 1 + len(w)
            if need <= width:
                cur = need
            else:
                lines += 1 if cur > 0 else 0
                cur = len(w)
                while cur > width:
                    lines += 1
                    cur -= width
        count += lines
    return count


def printed_lines(el, first_on_page=False):
    if el["t"] not in LAYOUT:
        return 0
    width, before = LAYOUT[el["t"]]
    plain = re.sub(r"[*_]", "", el["x"])
    return (0 if first_on_page else before) + wrapped_lines(plain, width)


# ----------------------------------------------------------------------------------------------- timing
WORDS_PER_SECOND = 2.5
LINE_PAD = 0.3


def words_of(text):
    """Spoken words; in Chinese and Japanese, which have no spaces, two characters count as one word (about 5 a second)."""
    t = re.sub(r"\([^)]*\)", " ", text)
    cjk = len(CJK_RE.findall(t))
    rest = CJK_RE.sub(" ", t)
    n = len(re.findall(r"[\w'’-]+", rest)) + cjk / 2.0
    return int(round(n)) if cjk else int(n)


def element_seconds(el):
    t = el["t"]
    if t == "dialogue":
        return words_of(el["x"]) / WORDS_PER_SECOND + LINE_PAD
    if t == "action":
        w = words_of(el["x"])
        if re.match(r"^\s*ON SCREEN\s*:", el["x"], re.I):
            return 1.5
        return min(6.0, max(1.5, 1.0 + 0.1 * w))
    if t == "shot":
        return 1.5
    if t in ("centered", "lyrics"):
        return 2.0
    return 0.0


# ----------------------------------------------------------------------------------------------- notes
CLIFF_RE = re.compile(r"^\s*CLIFF(?:HANGER)?\s*(?:[-–—(]\s*([A-Za-z][A-Za-z /&+-]*?)\s*\)?)?\s*:", re.I)
HOOK_RE = re.compile(r"^\s*HOOK\b", re.I)
NEGATIVE_RE = re.compile(r"\b(no one|nobody|nothing|no longer|not|never|without|isn't|aren't|doesn't|don't|won't|"
                         r"can't|cannot|there is no|there are no|no)\b", re.I)
FADE_RE = re.compile(r"\b(smile|grin|tears?|anger|joy|laugh\w*)\s+(fades?|disappears?|vanish\w*|stops?|drains?)\b|"
                     r"\b(stops?|ceases?)\s+(smiling|crying|laughing|grinning)\b|\bno longer\s+\w+ing\b", re.I)
TEXT_RE = re.compile(r"\b(it reads|which reads|that reads|reads:|the text says|the message says|the screen shows|"
                     r"we read|the headline|the sign says|the note says|written on|labell?ed|stamped|printed with|"
                     r"engraved with|marked with|that says|the screen reads)\b", re.I)


def split_episodes(title, els, label):
    """A season file: split at sections like '# Episode 3' / '# EP 3: Title'. Otherwise one episode."""
    ep_re = re.compile(r"^(?:episode|ep\.?)\s*(\d+)\s*[:.\-–—]?\s*(.*)$", re.I)
    marks = [k for k, e in enumerate(els) if e["t"] == "section" and ep_re.match(e["x"])]
    if not marks:
        return [(label, title, els)]
    out = []
    for a, k in enumerate(marks):
        end = marks[a + 1] if a + 1 < len(marks) else len(els)
        m = ep_re.match(els[k]["x"])
        name = "Episode %s%s" % (m.group(1), (": " + m.group(2).strip()) if m.group(2).strip() else "")
        out.append(("%s / %s" % (label, name), title, els[k + 1:end]))
    return out


def levenshtein(a, b):
    if a == b:
        return 0
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def analyze(label, title, els, target):
    issues = []

    def add(level, msg):
        issues.append({"level": level, "msg": msg})

    scenes = []
    cur = None
    pre = []
    for e in els:
        if e["t"] == "scene":
            cur = {"heading": e["x"], "place": e.get("place", ""), "time": e.get("time", ""), "els": [], "line": e["line"]}
            scenes.append(cur)
        elif cur is None:
            pre.append(e)
        else:
            cur["els"].append(e)

    # timeline: seconds at which each element starts (spoken lines plus action beats)
    t = 0.0
    timeline = []
    for e in els:
        timeline.append((t, e))
        t += element_seconds(e)
    est_seconds = t

    # Ziztu's planner: screen time per scene from its printed length (one page is about a minute, at least 8 s)
    page_lines_total = 0
    planner_seconds = 0
    for s in scenes:
        lines = 1  # the heading
        for e in s["els"]:
            lines += printed_lines(e)
        s["printed_lines"] = lines
        eighths = max(1, round(lines / PAGE_LINES * 8))
        s["planner_seconds"] = max(8, int(math.floor(eighths / 8 * 60 + 0.5)))
        planner_seconds += s["planner_seconds"]
        page_lines_total += lines + 1

    dialogue = [e for e in els if e["t"] == "dialogue"]
    words_per_line = [words_of(e["x"]) for e in dialogue]
    speakers_all = []
    cues = []
    cur_speaker = None
    speeches = []  # (speaker, words) per speech
    for e in els:
        if e["t"] == "character":
            cur_speaker = e["name"]
            cues.append(e)
            if e["name"] not in speakers_all:
                speakers_all.append(e["name"])
            speeches.append([e["name"], 0, e["line"], 0])
        elif e["t"] == "dialogue" and speeches:
            speeches[-1][1] += words_of(e["x"])
            speeches[-1][3] += 1
        elif e["t"] not in ("paren", "dialogue"):
            cur_speaker = None

    # ---- structure
    if not scenes:
        add("ERROR", "No scene heading found (INT. or EXT.). Ziztu needs at least one scene to plan shots.")
    places = []
    for s in scenes:
        if s["place"] and s["place"] not in places:
            places.append(s["place"])
        if not s["time"]:
            add("TIP", "Line %d: the heading '%s' has no DAY or NIGHT." % (s["line"], s["heading"]))
        speakers = []
        for e in s["els"]:
            if e["t"] == "character" and e["name"] not in speakers:
                speakers.append(e["name"])
        s["speakers"] = speakers
        if len(speakers) > 4:
            add("WARN", "Line %d: %d people speak in one scene (%s). Two or three keeps faces and cuts clear."
                % (s["line"], len(speakers), ", ".join(speakers)))
        elif len(speakers) == 4:
            add("TIP", "Line %d: 4 people speak in one scene (%s). Fine for a short entrance; otherwise two or three."
                % (s["line"], ", ".join(speakers)))
    if len(places) > 3:
        add("WARN", "%d places in one episode (%s). One or two reads as a scene, more reads as a trailer."
            % (len(places), "; ".join(places)))
    elif len(places) == 3:
        add("TIP", "3 places in one episode. Keep the third to a short insert of a few seconds, or merge it.")
    if len(speakers_all) > 4:
        add("WARN", "%d people speak in this episode (%s). Four is about the most a viewer tracks in 90 seconds."
            % (len(speakers_all), ", ".join(speakers_all)))
    if len(scenes) > 6:
        add("WARN", "%d scenes: Ziztu plans at most 6 scenes per script_to_shots run, so plan this episode in two runs."
            % len(scenes))

    # ---- runtime
    if target:
        lo, hi = target * 0.6, target * 1.15
        if est_seconds > hi:
            add("WARN", "About %d s of spoken lines and action beats, over the %d s target. Cut lines, not pace."
                % (round(est_seconds), target))
        elif est_seconds < lo:
            add("WARN", "Only about %d s of material for a %d s target: the episode will feel thin."
                % (round(est_seconds), target))
        action_words = sum(words_of(e["x"]) for e in els if e["t"] == "action")
        if planner_seconds > target * 1.4 and action_words > 300:
            add("WARN", "Ziztu will plan about %d s from the page length (a page is about a minute), and %d words of"
                " action are the reason. Trim the action paragraphs so the plan lands near %d s."
                % (planner_seconds, action_words, target))
        elif planner_seconds > max(target, est_seconds) * 1.15:
            add("TIP", "Ziztu's planner will give this about %d s (a page is about a minute); the episode needs about"
                " %d. After apply_plan, ask the Director to tighten it to %d s (references/ziztu.md, section 5)."
                % (planner_seconds, max(target, round(est_seconds)), target))

    # ---- hook
    hook_notes = [(ts, e) for ts, e in timeline if e["t"] == "note" and HOOK_RE.match(e["x"])]
    first_line_t = next((ts for ts, e in timeline if e["t"] == "dialogue"), None)
    first_action = next((e for e in els if e["t"] == "action"), None)
    if not hook_notes:
        add("ERROR", "No [[HOOK: ...]] note. Mark the first-3-seconds beat so the hook is a decision, not an accident.")
    else:
        ts = hook_notes[0][0]
        if ts > 3.0:
            add("WARN", "The [[HOOK]] note comes after about %.0f s of material. The hook is the first thing on screen." % ts)
    if first_line_t is not None and first_line_t > 8:
        add("WARN", "The first spoken line comes at about %.0f s. Unless the opening image is a shock, speak sooner."
            % first_line_t)
    if first_action and re.search(r"\b(skyline|establishing|exterior of|aerial|the city|a building|sunrise over|"
                                  r"wide view of)\b", first_action["x"], re.I):
        add("WARN", "Line %d: the episode opens on a view of a place ('%s...'). Open on the conflict instead."
            % (first_action["line"], first_action["x"][:60]))

    # ---- cliffhanger
    cliffs = [(ts, e) for ts, e in timeline if e["t"] == "note" and CLIFF_RE.match(e["x"])]
    cliff_type = None
    if not cliffs:
        add("ERROR", "No [[CLIFFHANGER - type: ...]] note. Every episode ends on a marked cliffhanger.")
    else:
        ts, note = cliffs[-1]
        m = CLIFF_RE.match(note["x"])
        cliff_type = (m.group(1) or "").strip().lower() or None
        tail = est_seconds - ts
        after = [e for tt, e in timeline if tt >= ts and e is not note and e["t"] in ("action", "dialogue", "shot")]
        if tail > 15:
            add("WARN", "About %.0f s of material after the cliffhanger note. Land the cliffhanger in the last 5 to 12 s"
                " and cut on the peak." % tail)
        if len(after) == 0:
            add("WARN", "Nothing follows the cliffhanger note: put the cliffhanger beat itself after the note.")
        if not cliff_type:
            add("TIP", "Name the cliffhanger type in the note, for example [[CLIFFHANGER - reveal: ...]], so variety"
                " across episodes can be checked.")

    # ---- dialogue
    if dialogue:
        avg = sum(words_per_line) / len(words_per_line)
        long12 = [e for e in dialogue if words_of(e["x"]) > 12]
        long20 = [e for e in dialogue if words_of(e["x"]) > 20]
        if len(long12) > max(2, 0.25 * len(dialogue)):
            add("WARN", "%d of %d lines run over 12 words (average %.1f). Hit dramas average about 5 to 6 words a line."
                % (len(long12), len(dialogue), avg))
        elif avg > 7.0 and len(dialogue) >= 6:
            add("WARN", "Lines average %.1f words. Hit dramas average about 5 to 6: cut words from the longest lines."
                % avg)
        for e in long20[:5]:
            add("WARN", "Line %d: a %d-word line. Split it with a reaction or cut it: '%s...'"
                % (e["line"], words_of(e["x"]), e["x"][:70]))
        for sp, w, ln, parts in speeches:
            if w > 25 and not (parts == 1 and w > 20):
                add("WARN", "Line %d: %s speaks %d words in one go. Keep speeches under about 25 words, or cut to a"
                    " reaction in the middle." % (ln, sp, w))
        run_sp, run_n, run_line = None, 0, 0
        for e in els:
            if e["t"] == "character":
                if e["name"] == run_sp:
                    run_n += 1
                else:
                    run_sp, run_n, run_line = e["name"], 1, e["line"]
                if run_n == 4:
                    add("WARN", "Line %d: %s has four speeches in a row with no reply or reaction between them."
                        % (run_line, run_sp))
            elif e["t"] in ("action", "shot", "scene"):
                run_sp, run_n = None, 0
    else:
        add("WARN", "No dialogue. Fine for a silent cold open, rare for a whole micro drama episode.")

    # ---- cues in scripts without capital letters (Chinese, Japanese, Korean, Hindi, Arabic, Thai...)
    for e in els:
        if e["t"] != "action" or e.get("nlines", 1) < 2:
            continue
        first = e.get("first", "").strip()
        core = re.sub(r"\s*\([^)]*\)", "", first).strip()
        if (core and len(core) <= 24 and not has_upper(core) and not has_lower(core) and re.search(r"[^\W\d_]", core)
                and not re.search(r"[。！？.!?,，:：;；]$", first) and not first.startswith(("ON SCREEN", "!", ">"))):
            add("ERROR", "Line %d: '%s' looks like a character cue, but a script without capital letters needs it written"
                " as @%s, or Ziztu imports the name and its line as action." % (e["line"], first, first))

    # ---- names
    names = sorted(set(c["name"] for c in cues))
    for c in cues:
        bare = c["name"]
        if len(bare.split()) > 3 or re.search(r"[.!?]$", bare) or re.search(r"[.!?]\s", bare):
            add("ERROR", "Line %d: '%s' will import as a CHARACTER. An all-caps line needs a blank line after it, or"
                " write it in sentence case." % (c["line"], c["x"]))
    for a in names:
        for b in names:
            if a < b:
                if a.split()[0] == b.split()[0] and a != b:
                    add("WARN", "Two cue spellings, '%s' and '%s': Ziztu will make two characters. Use one." % (a, b))
                elif len(a) >= 3 and len(b) >= 3 and a[0] == b[0] and levenshtein(a, b) <= 2 and abs(len(a) - len(b)) <= 2:
                    add("TIP", "'%s' and '%s' look alike in captions and in the cast list; consider renaming one." % (a, b))

    # ---- action lines
    actions = [e for e in els if e["t"] == "action"]
    negs = [e for e in actions if NEGATIVE_RE.search(re.sub(r'"[^"]*"', "", e["x"]))]
    if negs:
        add("TIP", "%d action line(s) use negative wording (first at line %d: '%s...'). Video models draw what is"
            " named: describe what is there." % (len(negs), negs[0]["line"], negs[0]["x"][:60]))
    for e in actions:
        if FADE_RE.search(e["x"]):
            add("WARN", "Line %d: '%s...' names the emotion that is ending; write the emotion that is there now."
                % (e["line"], e["x"][:60]))
        if TEXT_RE.search(e["x"]) and not re.match(r"^\s*ON SCREEN", e["x"], re.I):
            add("WARN", "Line %d: '%s...' asks the video model to draw words, which it garbles. Describe the object and put"
                " the words on their own line as ON SCREEN: \"...\" (a caption)." % (e["line"], e["x"][:50]))
    staged = [sc for sc in scenes if any(DEPTH_RE.search(e["x"]) for e in sc["els"] if e["t"] in ("action", "shot"))]
    flat = [sc for sc in scenes if sc not in staged]
    if flat and scenes:
        add("TIP", "%d of %d scenes place nobody near the camera or far from it (first: line %d, %s). Stage the beats that"
            " matter in depth, in one clause: who is behind whom, who watches from the doorway, what is at the far end."
            % (len(flat), len(scenes), flat[0]["line"], flat[0]["heading"][:40]))
    vo = [c for c in cues if any(x in ("V.O.", "VO", "V.O") for x in c["ext"])]
    if len(vo) > 4:
        add("TIP", "%d inner-voice lines. One to three lands harder; let faces and actions carry the rest." % len(vo))
    script_words = sum(words_of(e["x"]) for e in els if e["t"] in ("action", "dialogue", "shot", "centered"))
    if target and target <= 90 and script_words > 650:
        add("WARN", "%d words of script. A 60 to 90 second episode is usually 350 to 500 words; trim action first."
            % script_words)

    summary = {
        "episode": label,
        "title": title.get("title", ""),
        "scenes": len(scenes),
        "places": places,
        "speakers": speakers_all,
        "dialogue_lines": len(dialogue),
        "dialogue_words": sum(words_per_line),
        "script_words": script_words,
        "avg_words_per_line": round(sum(words_per_line) / len(words_per_line), 1) if words_per_line else 0,
        "voice_over_lines": len(vo),
        "depth_staged_scenes": "%d/%d" % (len(staged), len(scenes)),
        "estimated_seconds": round(est_seconds),
        "ziztu_planner_seconds": planner_seconds,
        "pages": round(page_lines_total / PAGE_LINES, 2),
        "first_line_at_seconds": round(first_line_t, 1) if first_line_t is not None else None,
        "cliffhanger_type": cliff_type,
        "issues": issues,
    }
    return summary


def season_checks(results):
    issues = []
    types = [r["cliffhanger_type"] for r in results]
    for a in range(1, len(types)):
        if types[a] and types[a] == types[a - 1]:
            issues.append({"level": "WARN", "msg": "%s and %s both end on a '%s' cliffhanger. Alternate the type."
                           % (results[a - 1]["episode"], results[a]["episode"], types[a])})
    named = [x for x in types if x]
    if len(named) >= 5:
        for ty in sorted(set(named)):
            share = named.count(ty) / len(named)
            if share > 0.34:
                issues.append({"level": "WARN", "msg": "'%s' ends %d of %d episodes. Viewers learn a pattern fast: mix in"
                               " other types." % (ty, named.count(ty), len(named))})
    return issues


def collect(paths):
    files = []
    for p in paths:
        if os.path.isdir(p):
            for f in sorted(os.listdir(p)):
                if f.lower().endswith((".fountain", ".spmd", ".txt")):
                    files.append(os.path.join(p, f))
        else:
            files.append(p)
    return files


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check micro drama episode scripts (Fountain) before Ziztu.")
    ap.add_argument("paths", nargs="+", help="Fountain files, a folder of them, or a season file with # Episode N sections")
    ap.add_argument("--target", type=int, default=90, help="target episode length in seconds (default 90; 0 = no check)")
    ap.add_argument("--json", action="store_true", help="print JSON instead of a report")
    args = ap.parse_args(argv)
    results = []
    for f in collect(args.paths):
        try:
            with open(f, encoding="utf-8") as fh:
                text = fh.read()
        except OSError as e:
            print("Cannot read %s: %s" % (f, e), file=sys.stderr)
            return 2
        title, els = parse_fountain(text)
        for label, ttl, part in split_episodes(title, els, os.path.basename(f)):
            results.append(analyze(label, ttl, part, args.target))
    season = season_checks(results) if len(results) > 1 else []
    errors = sum(1 for r in results for i in r["issues"] if i["level"] == "ERROR")
    if args.json:
        print(json.dumps({"episodes": results, "season": season, "errors": errors}, indent=2))
        return 1 if errors else 0
    for r in results:
        print("=" * 78)
        print("%s%s" % (r["episode"], (" (%s)" % r["title"]) if r["title"] else ""))
        print("  %d scene(s), places: %s" % (r["scenes"], "; ".join(r["places"]) or "none"))
        print("  speakers: %s" % (", ".join(r["speakers"]) or "none"))
        print("  %d lines of dialogue (%d words), %.1f words a line on average, %d inner-voice line(s); %d words of"
              " script" % (r["dialogue_lines"], r["dialogue_words"], r["avg_words_per_line"], r["voice_over_lines"],
                           r["script_words"]))
        print("  runtime: about %d s of lines and beats; Ziztu plans about %d s from %.2f page(s)"
              % (r["estimated_seconds"], r["ziztu_planner_seconds"], r["pages"]))
        print("  first spoken line at about %s s; cliffhanger type: %s"
              % (r["first_line_at_seconds"], r["cliffhanger_type"] or "not named"))
        if not r["issues"]:
            print("  OK: no issues found.")
        for i in r["issues"]:
            print("  %-5s %s" % (i["level"], i["msg"]))
    if season:
        print("=" * 78)
        print("Season")
        for i in season:
            print("  %-5s %s" % (i["level"], i["msg"]))
    print("=" * 78)
    print("%d episode(s) checked, %d error(s)." % (len(results), errors))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
