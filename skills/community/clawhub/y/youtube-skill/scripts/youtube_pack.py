#!/usr/bin/env python3
"""Turn a finished video and an upload.json into a checked YouTube upload pack.

    python3 scripts/youtube_pack.py frames VIDEO --out pack/
        Candidate thumbnail frames: frames.jpg (contact sheet with times and scores) and
        frames.json. Sharp, bright, varied frames first; faces counted when OpenCV is installed.

    python3 scripts/youtube_pack.py build upload.json --transcript work/transcript.json --out pack/
        Checks every field against YouTube's limits and writes:
          description.txt   the full description, ready to paste or send
          captions.srt      clean captions from the transcript (fillers out, names fixed)
          post.json         the WoopSocial post body (fill in the two IDs)
          upload-pack.md    everything on one page for the user to approve
          manifest.json     sizes, duration, Short or not, warnings

upload.json (times are seconds or "m:ss"):
{
  "video": "final.mp4",
  "phrase": "saturn rings disappearing",          # the main search phrase
  "titles": ["Saturn's Rings Are Disappearing in 2025. Here's Why", "..."],  # first = chosen
  "description": {
    "top": "Two lines that show above 'more': what the viewer gets, with the phrase.",
    "body": "Optional paragraphs.",
    "links": ["Source: https://..."],
    "hashtags": ["#saturn", "#astronomy", "#space"]
  },
  "chapters": [["0:00", "Why the rings vanish"], ["1:12", "..."]],
  "tags": ["saturn rings", "saturn ring plane crossing"],
  "category": "Science & Technology",            # name or ID
  "made_for_kids": false,                          # required: ask the user
  "made_for_kids_reason": "general audience",      # optional: the user's answer, shown in the pack
  "altered_content": false,                        # realistic AI-made or altered footage: "AI use" in Studio
  "privacy": "unlisted",                           # public | unlisted | private
  "schedule": "2026-11-03T17:00:00+01:00",         # optional, with Z or an offset; omit to post now
  "replace": {"Cassini's": "Cassini's"},           # misheard words in the captions
  "pinned_comment": "Optional first comment to pin."
}
Needs ffmpeg/ffprobe. Pillow for `frames`. Standard library otherwise.
"""
import argparse, json, os, re, shutil, subprocess, sys
from datetime import datetime, timezone

TITLE_MAX = 100            # YouTube's hard limit
TITLE_SOFT = 70            # longer titles are usually cut in search and on the home feed
TITLE_FRONT = 40           # roughly what a phone shows on one line; the phrase belongs here
DESC_MAX_BYTES = 5000      # the API counts bytes
DESC_FOLD = 150            # about what shows before "...more" under the video
TAGS_MAX = 500             # characters, counting commas and quotes around tags with spaces
HASHTAGS_SHOWN = 3         # the first three appear above the title
HASHTAGS_IGNORED_OVER = 60 # more than this and YouTube ignores all of them
SHORT_MAX = 180            # seconds; vertical or square and at most 3 minutes is a Short
FILLERS = {"um", "uh", "uhm", "umm", "er", "erm", "ah", "hmm", "mm"}
FUNCTION_WORDS = {"a", "an", "the", "of", "to", "for", "and", "that", "with", "on", "in", "is", "our", "my",
                  "your", "their", "at", "by", "from", "as", "or", "but", "so", "i", "we", "it"}
CATEGORIES = {1: "Film & Animation", 2: "Autos & Vehicles", 10: "Music", 15: "Pets & Animals", 17: "Sports",
              19: "Travel & Events", 20: "Gaming", 22: "People & Blogs", 23: "Comedy", 24: "Entertainment",
              25: "News & Politics", 26: "Howto & Style", 27: "Education", 28: "Science & Technology",
              29: "Nonprofits & Activism"}


# ---------- helpers ----------

def need_ffmpeg():
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        sys.exit("ffmpeg is not installed. Mac: brew install ffmpeg. Windows: winget install ffmpeg. "
                 "Linux: sudo apt install ffmpeg (or your distro's package).")


def probe(path):
    if not os.path.exists(path):
        sys.exit(f"Video not found: {path}")
    out = subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", path],
                         capture_output=True, text=True)
    try:
        info = json.loads(out.stdout)
    except ValueError:
        sys.exit(f"Could not read {path}; is it a video file?")
    v = next((s for s in info.get("streams", []) if s.get("codec_type") == "video"), None)
    if not v:
        sys.exit(f"{path} has no video stream.")
    w, h = int(v["width"]), int(v["height"])
    rot = 0
    for sd in v.get("side_data_list", []) or []:
        if "rotation" in sd:
            rot = abs(int(float(sd["rotation"])))
    if rot in (90, 270):
        w, h = h, w
    return {"width": w, "height": h, "duration": float(info["format"].get("duration", 0)),
            "bytes": os.path.getsize(path), "codec": v.get("codec_name"),
            "has_audio": any(s.get("codec_type") == "audio" for s in info.get("streams", []))}


def secs(t):
    if isinstance(t, (int, float)):
        return float(t)
    parts = [float(p) for p in str(t).strip().split(":")]
    total = 0.0
    for p in parts:
        total = total * 60 + p
    return total


def stamp(t):
    t = int(t)
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def clean(w):
    return re.sub(r"[^\w']", "", w.lower())


def srt_time(t):
    ms = int(round(max(0, t) * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def apply_replace(text, rep):
    for a, b in (rep or {}).items():
        text = re.sub(r"(?<!\w)" + re.escape(a) + r"(?!\w)", b, text, flags=re.I)
    return text


# ---------- captions ----------

def caption_events(words, rep, max_chars=42, lines=2, fps=30.0):
    """Clean captions: fillers out, at most 2 lines of 42, 1 to 7 s, gaps under 0.3 s closed."""
    kept, prev = [], None
    label = False
    for w in words:
        text = w["w"]
        # speaker tags from imported subtitles ("- [Teacher]", ">>") don't belong in clean captions
        if text in ("-", ">>", "\u2013") or label or text.startswith("["):
            label = not text.endswith("]") if (label or text.startswith("[")) else False
            continue
        if clean(text) in FILLERS:
            continue
        if (prev is None or prev[-1:] in ".?!") and text[:1].islower():
            text = text[:1].upper() + text[1:]
        kept.append((w["start"], w["end"], text))
        prev = text
    limit = max_chars * lines
    events, cur = [], []
    for j, (s, e, w) in enumerate(kept):
        cur.append((s, e, w))
        nxt = kept[j + 1] if j + 1 < len(kept) else None
        text = " ".join(x[2] for x in cur)
        too_long = nxt is not None and len(text) + 1 + len(nxt[2]) > limit
        if (nxt is None or w[-1:] in ".?!" or too_long or nxt[0] - e > 0.6 or e - cur[0][0] > 6.0
                or (w[-1:] in ",;:" and len(text) > limit * 0.6)):
            events.append([cur[0][0], cur[-1][1], apply_replace(re.sub(r",(\s*,)+", ",", text), rep)])
            cur = []
    gap = 2 / fps
    for k, ev in enumerate(events):
        nxt = events[k + 1][0] if k + 1 < len(events) else ev[1] + 1.5
        end = max(ev[1] + 0.5, ev[0] + 1.0)
        if nxt - end < 0.3:
            end = nxt - gap
        ev[1] = max(ev[0] + 0.5, min(end, nxt - gap, ev[0] + 7.0))
    return events


def split_lines(text, max_chars=42):
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
            cost += 25
        if words[k - 1][-1:] in ",.;:":
            cost -= 10
        if best is None or cost < best[0]:
            best = (cost, [a, b])
    return best[1]


def write_srt(events, path):
    with open(path, "w", encoding="utf-8") as fh:
        for n, (s, e, text) in enumerate(events, 1):
            fh.write(f"{n}\n{srt_time(s)} --> {srt_time(e)}\n" + "\n".join(split_lines(text)) + "\n\n")


# ---------- checks ----------

def tags_length(tags):
    return sum(len(t) + (2 if " " in t else 0) for t in tags) + max(0, len(tags) - 1)


def phrase_in(phrase, text, front=None):
    if not phrase:
        return True
    hay = text.lower() if front is None else text.lower()[:front]
    words = [w for w in re.findall(r"[\w']+", phrase.lower()) if w not in FUNCTION_WORDS]
    return all(re.search(r"\b" + re.escape(w[:max(4, len(w) - 2)]), hay) for w in words)


def snap_chapters(chapters, sentences, duration, warn):
    """Chapters must start at 0:00, be in order, at least 3, each at least 10 s. A chapter
    start is moved to the start of the sentence it falls in (within 3 s), so it never opens
    mid-word."""
    out = []
    for t, name in chapters:
        s = secs(t)
        if sentences and s > 0:
            near = min(sentences, key=lambda x: abs(x["start"] - s))
            if abs(near["start"] - s) <= 3.0:
                s = max(0.0, near["start"] - 0.3)
        out.append([s, name.strip()])
    out.sort(key=lambda c: c[0])
    if not out:
        return out
    if out[0][0] > 0.5:
        warn.append("The first chapter must start at 0:00; one was added called 'Intro'. Rename it.")
        out.insert(0, [0.0, "Intro"])
    out[0][0] = 0.0
    if len(out) < 3:
        warn.append(f"YouTube shows chapters only with 3 or more; this has {len(out)}. Add chapters or drop them.")
    for a, b in zip(out, out[1:] + [[duration, None]]):
        if a[0] >= duration:
            continue  # reported below
        if b[0] - a[0] < 10:
            warn.append(f"Chapter '{a[1]}' at {stamp(a[0])} is {b[0] - a[0]:.0f} s; each must be at least 10 s, "
                        "or YouTube shows no chapters at all.")
    if out[-1][0] >= duration:
        warn.append(f"Chapter '{out[-1][1]}' starts after the video ends.")
    for c in out:
        if len(c[1]) > 50:
            warn.append(f"Chapter name '{c[1][:30]}...' is long; the player cuts it. Keep under ~40 characters.")
    return out


def build(a):
    need_ffmpeg()
    spec = json.load(open(a.spec, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(a.spec))
    video = spec["video"] if os.path.isabs(spec["video"]) else os.path.join(base, spec["video"])
    info = probe(video)
    os.makedirs(a.out, exist_ok=True)
    warn, notes = [], []
    tr = None
    if a.transcript:
        tr = json.load(open(a.transcript, encoding="utf-8"))
    is_short = info["height"] >= info["width"] and info["duration"] <= SHORT_MAX
    vertical_long = info["height"] > info["width"] and info["duration"] > SHORT_MAX
    if vertical_long:
        warn.append(f"Vertical and {info['duration']:.0f} s: over 3 minutes it is a regular video, not a Short.")

    # title
    titles = [t.strip() for t in spec.get("titles", []) if t.strip()]
    if not titles:
        sys.exit("upload.json needs at least one title in \"titles\".")
    title = titles[0]
    phrase = spec.get("phrase", "").strip()
    for t in titles:
        if "<" in t or ">" in t:
            warn.append(f"Title has < or >, which YouTube refuses: {t}")
    if len(title) > TITLE_MAX:
        warn.append(f"Title is {len(title)} characters; YouTube's limit is {TITLE_MAX}.")
    elif len(title) > TITLE_SOFT:
        warn.append(f"Title is {len(title)} characters; past ~{TITLE_SOFT} it is usually cut off.")
    letters = [c for c in title if c.isalpha()]
    if letters and sum(c.isupper() for c in letters) / len(letters) > 0.6:
        warn.append("Title is mostly capitals; it reads as shouting and can look like spam.")
    if phrase and not phrase_in(phrase, title):
        warn.append(f"The search phrase '{phrase}' isn't in the title.")
    elif phrase and not phrase_in(phrase, title, TITLE_FRONT + 20):
        notes.append(f"The phrase sits late in the title; earlier is stronger where titles are cut.")
    if is_short and "#shorts" in title.lower():
        notes.append("#shorts in the title isn't needed: vertical videos up to 3 minutes are Shorts anyway.")

    # chapters
    sentences = (tr or {}).get("sentences", [])
    chapters = []
    if spec.get("chapters"):
        if is_short:
            notes.append("Shorts don't show chapters; they were left out of the description.")
        else:
            chapters = snap_chapters(spec["chapters"], sentences, info["duration"], warn)
    elif not is_short and info["duration"] > 240:
        notes.append("No chapters. Videos over 4 minutes usually benefit from them (they also show in Google).")

    # description
    d = spec.get("description", {})
    if isinstance(d, str):
        d = {"top": d}
    top = d.get("top", "").strip()
    hashtags = [h if h.startswith("#") else "#" + h for h in d.get("hashtags", [])]
    for h in hashtags:
        if re.search(r"\s", h.strip()):
            joined = "".join(h.split())
            warn.append(f"Hashtag '{h}' has a space; YouTube reads only the first word. "
                        f"Write it as {joined} or drop it.")
    hashtags = [re.sub(r"\s+", "", h) for h in hashtags]
    parts = [top]
    if d.get("body"):
        parts.append(d["body"].strip())
    if chapters:
        parts.append("\n".join(f"{stamp(t)} {name}" for t, name in chapters))
    if d.get("links"):
        parts.append("\n".join(d["links"]))
    if hashtags:
        parts.append(" ".join(hashtags))
    description = "\n\n".join(p for p in parts if p)
    if "<" in description or ">" in description:
        warn.append("Description has < or >, which YouTube refuses. Use other characters.")
    nbytes = len(description.encode("utf-8"))
    if nbytes > DESC_MAX_BYTES:
        warn.append(f"Description is {nbytes} bytes; YouTube's limit is {DESC_MAX_BYTES}.")
    if not top:
        warn.append("No description top lines. The first ~150 characters show under the video and in search.")
    elif phrase and not phrase_in(phrase, top[:DESC_FOLD]):
        warn.append(f"The search phrase isn't in the first {DESC_FOLD} characters of the description.")
    if top.lower().startswith(("in this video", "hey guys", "welcome")):
        notes.append("The description opens with a stock phrase; open with what the viewer gets instead.")
    if len(hashtags) > HASHTAGS_IGNORED_OVER:
        warn.append(f"{len(hashtags)} hashtags: over {HASHTAGS_IGNORED_OVER}, YouTube ignores all of them.")
    elif len(hashtags) > HASHTAGS_SHOWN:
        notes.append(f"YouTube shows up to {HASHTAGS_SHOWN} hashtags above the title (the ones it finds most "
                     f"engaging); {len(hashtags)} is more than shows. 3 specific ones are enough.")
    for h in hashtags:
        if not re.fullmatch(r"#[\w]+", h):
            warn.append(f"Hashtag {h} has characters that break it; letters, digits and _ only.")

    # tags
    tags = [t.strip().lstrip("#") for t in spec.get("tags", []) if t.strip()]
    tl = tags_length(tags)
    if tl > TAGS_MAX:
        warn.append(f"Tags are {tl} characters as YouTube counts them (commas and quotes included); "
                    f"the limit is {TAGS_MAX}. Remove the least specific ones.")
    for t in tags:
        if "<" in t or ">" in t or "," in t:
            warn.append(f"Tag '{t}' has a character YouTube refuses (< > ,).")

    # category and audience
    cat = spec.get("category")
    cat_id = None
    if cat is not None:
        if str(cat).isdigit() and int(cat) in CATEGORIES:
            cat_id = int(cat)
        else:
            cat_id = next((k for k, v in CATEGORIES.items() if v.lower() == str(cat).lower()), None)
        if cat_id is None:
            warn.append(f"Category '{cat}' isn't a YouTube category: {', '.join(CATEGORIES.values())}.")
    if "made_for_kids" not in spec:
        warn.append("made_for_kids is missing. It's a legal setting (COPPA); ask the user, don't guess.")
    privacy = spec.get("privacy", "unlisted")
    if privacy not in ("public", "unlisted", "private"):
        warn.append(f"privacy must be public, unlisted or private, not {privacy}.")
    sched_utc = None
    if spec.get("schedule"):
        raw = str(spec["schedule"]).strip()
        try:
            when = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        except ValueError:
            when = None
            warn.append(f"schedule '{raw}' isn't a date and time like 2026-11-03T16:00:00Z.")
        if when is not None:
            if when.tzinfo is None:
                warn.append(f"schedule '{raw}' has no timezone. Add Z for UTC or an offset like +01:00, "
                            "so it posts at the time the user means.")
            else:
                when = when.astimezone(timezone.utc)
                sched_utc = when.strftime("%Y-%m-%dT%H:%M:%SZ")
                if when <= datetime.now(timezone.utc):
                    warn.append(f"schedule {sched_utc} is in the past.")
                notes.append(f"Scheduled for {sched_utc} UTC; WoopSocial publishes then, as {privacy}.")

    # captions
    srt = None
    if tr and tr.get("words"):
        if (tr.get("duration") and abs(tr["duration"] - info["duration"]) > 1.0):
            warn.append(f"The transcript is {tr['duration']:.1f} s but the video is {info['duration']:.1f} s; "
                        "transcribe the final video so captions line up.")
        events = caption_events(tr["words"], spec.get("replace"))
        srt = os.path.join(a.out, "captions.srt")
        write_srt(events, srt)
        if tr.get("source", "").startswith("subtitles"):
            notes.append("Captions came from an existing subtitle file; word timing is estimated.")
    else:
        notes.append("No transcript given: no captions.srt. Run transcribe.py on the final video.")

    if not info["has_audio"]:
        notes.append("The video has no audio track.")
    if info["width"] * info["height"] < 1280 * 720 and not is_short:
        notes.append(f"{info['width']}x{info['height']}: under 720p looks soft on most screens.")

    with open(os.path.join(a.out, "description.txt"), "w", encoding="utf-8") as fh:
        fh.write(description + "\n")

    yt = {"platform": "YOUTUBE", "socialAccountId": "<youtube account id>", "title": title, "privacy": privacy}
    if tags:
        yt["tags"] = tags
    if cat_id:
        yt["category"] = str(cat_id)
    if "made_for_kids" in spec:
        yt["madeForKids"] = bool(spec["made_for_kids"])
    post = {"content": [{"text": description, "media": [{"type": "MEDIA_LIBRARY", "mediaId": "<media id>"}]}],
            "socialAccounts": [yt]}
    post["schedule"] = ({"type": "SCHEDULE_FOR_LATER", "scheduledFor": sched_utc} if sched_utc
                        else {"type": "PUBLISH_NOW"})
    with open(os.path.join(a.out, "post.json"), "w", encoding="utf-8") as fh:
        json.dump(post, fh, indent=2, ensure_ascii=False)

    manifest = {"video": spec["video"], "bytes": info["bytes"], "duration": round(info["duration"], 3),
                "size": f"{info['width']}x{info['height']}", "is_short": is_short, "title": title,
                "title_chars": len(title), "description_bytes": nbytes, "tags_chars": tl,
                "chapters": [[stamp(t), n] for t, n in chapters], "category_id": cat_id,
                "captions": "captions.srt" if srt else None, "warnings": warn, "notes": notes}
    with open(os.path.join(a.out, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, ensure_ascii=False)
    write_pack(a.out, spec, info, titles, description, top, hashtags, tags, tl, chapters, cat_id, privacy,
               is_short, warn, notes, srt, sched_utc)
    print(f"{'Short' if is_short else 'Video'} {stamp(info['duration'])}, title {len(title)} chars, "
          f"description {nbytes} bytes, {len(chapters)} chapters, tags {tl}/{TAGS_MAX}")
    for w in warn:
        print("WARNING:", w)
    for n in notes:
        print("note:", n)
    print(f"-> {a.out}/upload-pack.md")


def write_pack(out, spec, info, titles, description, top, hashtags, tags, tl, chapters, cat_id, privacy,
               is_short, warn, notes, srt, sched_utc=None):
    L = [f"# Upload pack: {titles[0]}", ""]
    if warn:
        L += ["## Fix before posting", ""] + [f"- {w}" for w in warn] + [""]
    L += ["## Title", "", f"**{titles[0]}** ({len(titles[0])} characters)", "",
          f"Where titles are cut short: \"{titles[0][:TITLE_FRONT].rstrip()}...\"", ""]
    if len(titles) > 1:
        L += ["Other options (up to 3 titles can be A/B tested with Test & Compare in Studio):", ""]
        L += [f"- {t} ({len(t)})" for t in titles[1:]] + [""]
    fold = top[:DESC_FOLD]
    L += ["## Description", "", f"Shows before \"...more\": \"{fold}{'...' if len(top) > DESC_FOLD else ''}\"", "",
          "```", description, "```", ""]
    if hashtags:
        L += [f"Above the title: {' '.join(hashtags[:HASHTAGS_SHOWN])}", ""]
    if chapters:
        L += ["## Chapters", ""] + [f"- {stamp(t)} {n}" for t, n in chapters] + [""]
    L += ["## Settings", "",
          f"- Tags ({tl}/{TAGS_MAX}): {', '.join(tags) if tags else 'none'}",
          f"- Category: {CATEGORIES.get(cat_id, 'not set') if cat_id else 'not set'}",
          f"- Made for kids: {'yes' if spec.get('made_for_kids') else 'no' if 'made_for_kids' in spec else 'NOT SET: ask the user'}"
          + (f" ({spec['made_for_kids_reason']})" if spec.get("made_for_kids_reason") else ""),
          f"- Privacy: {privacy}" + (f", scheduled for {sched_utc} UTC (given as {spec['schedule']})"
                                     if sched_utc else ", posts now"),
          f"- File: {os.path.basename(spec['video'])}, {info['width']}x{info['height']}, {stamp(info['duration'])}, "
          f"{info['bytes'] / 1e6:.1f} MB{', a Short' if is_short else ''}",
          f"- Captions: {'captions.srt' if srt else 'none'}", ""]
    if spec.get("pinned_comment"):
        L += ["## Comment to pin", "", spec["pinned_comment"], ""]
    L += ["## After it's uploaded: in YouTube Studio", "",
          "WoopSocial uploads the video with the fields above. These are set in Studio:", ""]
    if not is_short:
        L.append("- **Thumbnail:** Details > Thumbnail > Upload file (the channel must be verified). With 2 or 3 "
                 "options, use Test & Compare (desktop Studio; titles and thumbnails, up to 3 each, judged on "
                 "watch time share; not for made-for-kids videos).")
    else:
        L.append("- **Thumbnail:** a Short's custom thumbnail (9:16) is added in Studio on a computer; otherwise "
                 "pick a frame. Test & Compare doesn't run on Shorts.")
    if srt:
        L.append("- **Captions:** Subtitles > Add language > Upload file > With timing > captions.srt.")
    L.append("- **AI use** (altered or synthetic content): "
             + ("**Yes: set it** in the video's details under AI use; YouTube adds a label." if spec.get("altered_content")
                else "No, per the user. Realistic AI-made or AI-altered people, places or events would need Yes."))
    if not is_short:
        L.append("- **End screen and cards:** point to the next video to watch.")
    L.append("- **Playlist:** add it to the playlist it belongs in.")
    if spec.get("pinned_comment"):
        L.append("- **Pinned comment:** post it from the channel, then pin it.")
    L.append("")
    if notes:
        L += ["## Notes", ""] + [f"- {n}" for n in notes] + [""]
    with open(os.path.join(out, "upload-pack.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))


# ---------- frames ----------

def face_detector():
    """Faces in a frame: OpenCV's YuNet with the bundled model (OpenCV 4.5.4 and newer), else the
    older Haar cascade. Returns None when OpenCV isn't installed; faces are then not scored."""
    os.environ.setdefault("OPENCV_LOG_LEVEL", "ERROR")  # OpenCV 5 prints a backend notice otherwise
    try:
        import cv2
        import numpy as np
    except ImportError:
        return None
    model = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "models",
                         "face_detection_yunet_2023mar.onnx")
    if hasattr(cv2, "FaceDetectorYN") and os.path.exists(model):
        net = cv2.FaceDetectorYN.create(model, "", (320, 320), 0.8)

        def yunet(im):
            arr = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
            net.setInputSize((arr.shape[1], arr.shape[0]))
            _, found = net.detect(arr)
            if found is None:
                return 0, 0.0
            return len(found), max(f[2] * f[3] for f in found) / (arr.shape[0] * arr.shape[1])
        return yunet
    if hasattr(cv2, "CascadeClassifier") and hasattr(cv2, "data"):
        cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        def haar(im):
            arr = np.array(im.convert("L"))
            found = cascade.detectMultiScale(arr, 1.1, 5, minSize=(40, 40))
            if not len(found):
                return 0, 0.0
            return len(found), max(w * h for x, y, w, h in found) / (arr.shape[0] * arr.shape[1])
        return haar
    return None


def frames(a):
    need_ffmpeg()
    try:
        from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageStat
    except ImportError:
        sys.exit("Frames need Pillow: pip install pillow")
    info = probe(a.video)
    os.makedirs(a.out, exist_ok=True)
    fdir = os.path.join(a.out, "frames")
    os.makedirs(fdir, exist_ok=True)
    dur = info["duration"]
    n = max(12, min(a.count * 3, 90))
    start, end = min(2.0, dur * 0.05), dur - min(2.0, dur * 0.05)
    times = [start + (end - start) * i / (n - 1) for i in range(n)]
    detect = face_detector()
    cands = []
    for i, t in enumerate(times):
        p = os.path.join(fdir, f"f{i:03d}.jpg")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", a.video, "-frames:v", "1",
                        "-vf", "scale=640:-2", "-q:v", "3", p], check=True)
        if not os.path.exists(p):
            continue
        im = Image.open(p).convert("RGB")
        g = im.convert("L")
        stat = ImageStat.Stat(g)
        mean, contrast = stat.mean[0], stat.stddev[0]
        sharp = ImageStat.Stat(g.filter(ImageFilter.FIND_EDGES)).var[0]
        hsv = ImageStat.Stat(im.convert("HSV")).mean[1]
        faces, face_share = detect(im) if detect else (0, 0.0)
        small = g.resize((9, 8))
        px = list(small.get_flattened_data() if hasattr(small, "get_flattened_data") else small.getdata())
        dhash = sum(1 << k for k in range(64) if px[(k // 8) * 9 + k % 8] > px[(k // 8) * 9 + k % 8 + 1])
        score = (min(sharp, 2500) / 2500) * 0.5 + (min(contrast, 70) / 70) * 0.3 + (min(hsv, 120) / 120) * 0.2
        if mean < 25 or mean > 235:
            score *= 0.2  # black or blown-out frames
        if faces:
            score += 0.15 + min(face_share * 2, 0.2)
        cands.append({"t": round(t, 2), "file": p, "score": round(score, 3), "sharpness": round(sharp),
                      "brightness": round(mean), "faces": faces, "dhash": dhash})
    cands.sort(key=lambda c: -c["score"])
    picked = []
    # best first, skipping near-duplicates; a fixed-camera video can look the same all the
    # way through, so if that leaves too few, fill up with the frames furthest apart in time
    for c in cands:
        if all(bin(c["dhash"] ^ p["dhash"]).count("1") > 6 for p in picked):
            picked.append(c)
        if len(picked) >= a.count:
            break
    rest = [c for c in cands if c not in picked]
    while len(picked) < a.count and rest:
        far = max(rest, key=lambda c: min(abs(c["t"] - p["t"]) for p in picked) if picked else 0)
        picked.append(far)
        rest.remove(far)
    vertical = info["height"] > info["width"]
    cols = 6 if vertical else 4
    rows = (len(picked) + cols - 1) // cols
    tw, th = (180, 320) if vertical else (320, 180)
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * 8, rows * (th + 26) + 8), (20, 20, 20))
    fpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fonts", "Inter.ttf")
    try:
        f = ImageFont.truetype(fpath, 14 if vertical else 16)
        f.set_variation_by_name("SemiBold")
    except Exception:
        f = ImageFont.load_default()
    d = ImageDraw.Draw(sheet)
    for k, c in enumerate(picked):
        x, y = 8 + (k % cols) * (tw + 8), 8 + (k // cols) * (th + 26)
        im = Image.open(c["file"]).convert("RGB")
        im.thumbnail((tw, th))  # whole frame, letterboxed: nothing cropped off
        sheet.paste(im, (x + (tw - im.width) // 2, y + (th - im.height) // 2))
        label = f"#{k + 1} {c['t']:.1f}s" + (f" faces {c['faces']}" if c["faces"] else "")
        if not vertical:
            label = f"#{k + 1}  t={c['t']:.1f}s  score {c['score']:.2f}" + (f"  faces {c['faces']}" if c["faces"] else "")
        d.text((x, y + th + 3), label, fill=(230, 230, 230), font=f)
    for k, c in enumerate(picked):
        c["n"] = k + 1  # the number on the contact sheet
        c.pop("dhash", None)
        c["file"] = os.path.relpath(c["file"], a.out).replace(os.sep, "/")
    sheet.save(os.path.join(a.out, "frames.jpg"), quality=88)
    with open(os.path.join(a.out, "frames.json"), "w", encoding="utf-8") as fh:
        json.dump({"video": os.path.basename(a.video), "duration": dur, "frames": picked,
                   "faces_checked": detect is not None}, fh, indent=2)
    print(f"{len(picked)} candidate frames -> {a.out}/frames.jpg"
          + ("" if detect else " (pip install opencv-python-headless to also score faces)"))


def main():
    ap = argparse.ArgumentParser(description="Build a checked YouTube upload pack.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build", help="check upload.json and write the pack")
    b.add_argument("spec")
    b.add_argument("--transcript", help="work/transcript.json from transcribe.py (for captions and chapters)")
    b.add_argument("--out", default="pack")
    f = sub.add_parser("frames", help="candidate thumbnail frames")
    f.add_argument("video")
    f.add_argument("--out", default="pack")
    f.add_argument("--count", type=int, default=12)
    a = ap.parse_args()
    build(a) if a.cmd == "build" else frames(a)


if __name__ == "__main__":
    main()
