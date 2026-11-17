#!/usr/bin/env python3
"""Check image and video prompts for depth: planes at different distances, focus, tone, air, light and parallax.

  python3 depth_check.py prompt.txt [more files]   check prompts ('-' reads stdin)
  python3 depth_check.py --video prompt.txt        also check camera moves (video prompts)
  python3 depth_check.py --json prompt.txt         machine-readable output

A file holds one prompt, or several separated by a line holding only '---'. Inside a prompt, '[Shot N]' markers (H3)
or lines starting 'Shot N:' (Seedance, Kling) split it into shots, and each shot is checked on its own. Text after
'overall_soundscape:' or 'non_diegetic_music:' and the spoken words inside <d>...</d> or quotes are ignored.

Each shot gets a score out of 10 and a list of notes:
  FLAT  neither a foreground nor a background is named (exit code 1)
  WARN  something that usually flattens or breaks a layered shot
  TIP   a cheap way to add depth
The score is a reminder, not a verdict: the generated frame has the last word. Standard library only (Python 3.8+).
"""
import json
import re
import sys

FG = re.compile(r"\b(fore-?ground|closest to the (lens|camera)|nearest (to )?the (lens|camera)|near the lens|"
                r"in front of the (lens|camera)|over (his|her|their|the [a-z]+'s|[A-Z][a-z]+'s) shoulder|"
                r"dirty (single|two-shot|over)|frame within a frame|(foreground|near) (edge|corner))\b", re.I)
EDGE = re.compile(r"\b(at|along|on|in) the (lower |upper |far )?(left|right|bottom|top|lower|upper|near)\b[^.]{0,20}"
                  r"\b(edge|corner|third|side|sixth|fifth)\b", re.I)
MG = re.compile(r"\b(mid-?ground|middle distance|middle ground)\b", re.I)
BG = re.compile(r"\b(back-?ground|behind (him|her|them|it|the [a-z]+|[A-Z][a-z]+)|in the distance|far (end|wall|side|"
                r"door|corner|away|behind|below)|distant|horizon|beyond|through the (window|windows|doorway|door|glass|"
                r"arch)|at the end of the|recede\w*|receding|vanishing point)\b", re.I)
DIST = re.compile(r"\b\d+(\.\d+)?\s?(to|-|–)?\s?(\d+(\.\d+)?)?\s?(m|metres?|meters?|ft|feet)\b|\b(one|two|three|four|"
                  r"five|six|eight|ten|twenty|a few) (metres?|meters?|feet|steps|paces) (behind|away|back|from)\b", re.I)
FOCUS = re.compile(r"\b(in (sharp |crisp )?focus|sharp(ly)?|crisp|out[- ]of[- ]focus|defocused|blurred|blurry|soft focus|"
                   r"rack focus|focus (shifts|pulls|racks|moves)|pull focus|deep focus|soft\b)", re.I)
GENERIC = re.compile(r"\b(depth of field|bokeh|cinematic depth|shallow depth|dof)\b", re.I)
AIR = re.compile(r"\b(haze|hazy|mist|misty|fog|foggy|dust|dusty|steam\w*|smoke|smoky|drizzle|rain|god rays|"
                 r"light beams?|atmospheric|aerial perspective|lower contrast|low contrast|less contrast|paler|pale|"
                 r"faded|washed|desaturated|muted)\b", re.I)
LIGHT = re.compile(r"\b(rim[- ]?light\w*|rim[- ]lit|back-?light\w*|back-?lit|edge light|hair light|silhouett\w*|"
                   r"practical\w*|lamps?|lanterns?|candle\w*|string lights|window light|pool of light|light falloff|"
                   r"(warm|amber|golden|orange)[^.]{0,40}(cool|blue|teal)|(cool|blue|teal)[^.]{0,40}(warm|amber|golden|"
                   r"orange))\b", re.I)
LENS = re.compile(r"\b\d{2,3}\s?mm\b", re.I)
MOVE = re.compile(r"\b(truck\w*|doll(y|ies)|tracking|tracks|arc shot|arcs|orbit\w*|pedestal\w*|crane\w*|boom\w*|jib|"
                  r"push(es)? in|pushing in|pull(s)? out|pulling out|pans?|panning|tilts?|tilting|handheld|steadicam|"
                  r"rack focus|focus (shifts|pulls|racks))\b", re.I)
PARALLAX = re.compile(r"\b(truck\w*|doll(y|ies)|tracking|tracks|arc shot|arcs|orbit\w*|pedestal\w*|crane\w*|boom\w*|"
                      r"jib|parallax|slides? past|past the)\b", re.I)
ZOOM = re.compile(r"\bzoom(s|ing|ed)?\b", re.I)
STATIC = re.compile(r"\b(static|locked[- ]off|holds? still|fixed camera)\b", re.I)
MOVER = re.compile(r"\b(steam|smoke|rain|drizzle|curtains?|flicker\w*|flutter\w*|drift\w*|sway\w*|passes|passing|"
                   r"walks? past|crosses|crossing|rises|rising|falls|falling|blows|blowing)\b", re.I)
NEG = re.compile(r"\b(no|without|never|not|don't|doesn't|isn't|nothing|nobody|none)\b", re.I)
NEG_OK = re.compile(r"\bnobody changes (gender|age)|\bno (on-screen )?text\b|\bno subtitles\b", re.I)
FACE = re.compile(r"\b(face|faces|eyes|mouth)\b", re.I)
COVER = re.compile(r"\b(across|covers?|covering|block\w*|obscur\w*|in front of (his|her|their) face)\b", re.I)
CROWD = re.compile(r"\b(crowd|people|guests|figures|pedestrians|passers-by|customers|diners|onlookers|commuters)\b", re.I)
NUMBER = re.compile(r"\b(\d+|a few|two|three|four|five|six|seven|eight|nine|ten|dozen|twenty|thirty|forty|fifty|"
                    r"a pair of|a handful of)\b", re.I)
SMALL = re.compile(r"\b(small|soft|tiny|distant|far)\b", re.I)
SHOT_SPLIT = re.compile(r"(?=\[Shot \d+\])|(?=^\s*Shot \d+\b[^:\n]{0,30}:)", re.M)


def clean(text):
    """Drop sound fields, spoken words and quoted lines, which say nothing about the picture."""
    text = re.split(r"\b(overall_soundscape|non_diegetic_music)\s*:", text)[0]
    text = re.sub(r"<d>.*?</d>", " ", text, flags=re.S)
    text = re.sub(r"\"[^\"]*\"|“[^”]*”", " ", text)
    return text


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.;!?])\s+", text) if s.strip()]


def check_shot(text, video):
    t = clean(text)
    sents = sentences(t)
    notes = []
    fg = bool(FG.search(t)) or bool(EDGE.search(t) and FOCUS.search(t))
    bg = bool(BG.search(t))
    mg = bool(MG.search(t))
    dist = bool(DIST.search(t))
    focus = bool(FOCUS.search(t))
    generic_only = bool(GENERIC.search(t)) and not re.search(r"\b(in (sharp |crisp )?focus|out[- ]of[- ]focus|sharp|"
                                                            r"soft)\b", t, re.I)
    air = bool(AIR.search(t))
    light = bool(LIGHT.search(t))
    lens = bool(LENS.search(t))
    move = bool(MOVE.search(t))
    parallax = bool(PARALLAX.search(t))

    if not fg and not bg:
        notes.append(("FLAT", "Neither a foreground nor a background is named: everything sits on one plane. Add one "
                              "sentence per plane (foreground object at an edge, the subject, the place behind)."))
    elif not fg:
        notes.append(("WARN", "No foreground. Put one soft object at an edge (a shoulder, a glass, a door frame, "
                              "leaves), or say why this shot has none (a close-up held by focus and light)."))
    elif not bg:
        notes.append(("WARN", "No background described. Say what is behind the subject, how far, and that it is "
                              "softer and lower in contrast."))
    if not mg and (fg or bg):
        notes.append(("TIP", "Name the middle plane too (\"in the midground, ...\") so the subject's distance is clear."))
    if not dist:
        notes.append(("TIP", "No distances. Write the camera distance and how far the background is (\"from 3 m\", "
                             "\"about 8 m behind her\"): different distances, not just different objects."))
    if generic_only:
        notes.append(("WARN", "\"Depth of field\" or \"bokeh\" without saying which plane is sharp gives a generic "
                              "blurred backdrop. Name the sharp plane and the soft ones."))
    elif not focus:
        notes.append(("TIP", "Say which plane is sharp and which are soft."))
    if bg and not air:
        notes.append(("TIP", "Push the background back: say it is paler, hazier or lower in contrast, or add light "
                             "haze, dust or steam behind the subject."))
    if not light:
        notes.append(("TIP", "Add a separation light: a rim or backlight on the subject, practical lamps at different "
                             "depths, or a warm subject against a cool background."))
    if video:
        if ZOOM.search(t):
            notes.append(("WARN", "A zoom scales every plane together and flattens the frame. Truck, dolly or arc past "
                                  "the foreground instead."))
        if not move and not STATIC.search(t) and not ZOOM.search(t):
            notes.append(("TIP", "No camera move named. A slow truck or dolly past the foreground gives parallax."))
        elif STATIC.search(t) and not MOVER.search(t):
            notes.append(("TIP", "A static shot reads deeper when something moves in one plane (steam in front, a "
                                 "figure crossing far behind, rain)."))
    for s in sentences(t):
        if NEG.search(s) and not NEG_OK.search(s):
            notes.append(("WARN", "Negative wording plants the thing it names: '%s'. Describe what is there instead."
                                  % s[:70]))
            break
    for s in sents:
        if FG.search(s) and FACE.search(s) and COVER.search(s):
            notes.append(("WARN", "A foreground may cover a face: '%s'. Keep it at the edge, clear of faces." % s[:70]))
            break
    for s in sents:
        if BG.search(s) and CROWD.search(s) and not NUMBER.search(s):
            notes.append(("TIP", "Background people need a number, an action and a size (\"a dozen diners far behind, "
                                 "small and soft, facing the bar\"), or they double, stare or walk forward."))
            break
        if BG.search(s) and CROWD.search(s) and not SMALL.search(s):
            notes.append(("TIP", "Keep background people small and soft so they stay in their plane."))
            break

    score = 0
    score += 2 if fg else 0
    score += 2 if bg else 0
    score += 1 if (mg or focus) else 0
    score += 1 if dist else 0
    score += 1 if (bg and air) else 0
    score += 1 if light else 0
    score += 1 if lens else 0
    if video:
        score += 1 if (parallax and not ZOOM.search(t)) else 0
    else:
        score += 1 if (fg and EDGE.search(t)) else 0
    if generic_only:
        score = max(0, score - 1)
    return {"score": score, "planes": {"foreground": fg, "midground": mg, "background": bg},
            "notes": [{"level": lv, "msg": m} for lv, m in notes]}


def split_prompts(text):
    parts = re.split(r"^\s*---\s*$", text, flags=re.M)
    return [p.strip() for p in parts if p.strip()]


def split_shots(prompt):
    chunks = [c.strip() for c in SHOT_SPLIT.split(prompt) if c.strip()]
    shots = [c for c in chunks if re.match(r"(\[Shot \d+\]|Shot \d+\b[^:\n]{0,30}:)", c)]
    if not shots:
        return [("whole prompt", prompt)]
    out = []
    for c in shots:
        m = re.match(r"\[?(Shot \d+)\]?", c)
        out.append((m.group(1), c))
    return out


def main(argv):
    video = "--video" in argv
    as_json = "--json" in argv
    files = [a for a in argv if not a.startswith("--")]
    if not files:
        print(__doc__)
        return 2
    results = []
    for f in files:
        text = sys.stdin.read() if f == "-" else open(f, encoding="utf-8").read()
        for pi, prompt in enumerate(split_prompts(text), 1):
            for label, shot in split_shots(prompt):
                r = check_shot(shot, video)
                r.update({"file": f, "prompt": pi, "shot": label})
                results.append(r)
    flat = sum(1 for r in results if any(n["level"] == "FLAT" for n in r["notes"]))
    if as_json:
        print(json.dumps({"shots": results, "flat": flat}, indent=2))
    else:
        for r in results:
            planes = "".join(k[0].upper() if v else "-" for k, v in r["planes"].items())
            print("%s  prompt %d  %-12s depth %2d/10  planes %s" % (r["file"], r["prompt"], r["shot"], r["score"], planes))
            for n in r["notes"]:
                print("    %-4s %s" % (n["level"], n["msg"]))
        if results:
            avg = sum(r["score"] for r in results) / len(results)
            print("\n%d shot(s), average depth %.1f/10, %d flat." % (len(results), avg, flat))
    return 1 if flat else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
