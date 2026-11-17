#!/usr/bin/env python3
"""Transcribe a video with word-level timestamps.

    python3 scripts/transcribe.py VIDEO --out work/            # pick the best route available
    python3 scripts/transcribe.py VIDEO --engine local --model small
    python3 scripts/transcribe.py VIDEO --engine groq          # needs GROQ_API_KEY
    python3 scripts/transcribe.py VIDEO --engine openai        # needs OPENAI_API_KEY
    python3 scripts/transcribe.py VIDEO --from captions.srt    # an existing SRT or VTT file

Writes work/transcript.json (every word with start and end in seconds, plus sentences) and
work/transcript.txt (one timestamped line per sentence, compact enough for an agent to read
a whole hour).

Routes, in the order "auto" tries them:
  1. --from: an existing transcript (YouTube Studio, podcast host). Free and instant.
  2. groq / openai: if GROQ_API_KEY or OPENAI_API_KEY is set. Fast; the audio is sent to them.
  3. local: faster-whisper on the CPU (pip install faster-whisper). Free and private; with
     the "small" model it takes roughly half to one times the video's length on a laptop
     ("base" is faster, a little less accurate).
Needs ffmpeg on PATH. Standard library only otherwise.
"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile, uuid
import urllib.error, urllib.request

API = {
    "groq": ("https://api.groq.com/openai/v1/audio/transcriptions", "GROQ_API_KEY", "whisper-large-v3-turbo"),
    "openai": ("https://api.openai.com/v1/audio/transcriptions", "OPENAI_API_KEY", "whisper-1"),
}
API_LIMIT = 24 * 1024 * 1024  # both APIs refuse files over 25 MB
CHUNK_SECONDS = 20 * 60


def need_ffmpeg():
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        sys.exit("ffmpeg is not installed. Mac: brew install ffmpeg. Windows: winget install ffmpeg. "
                 "Linux: sudo apt install ffmpeg (or your distro's package).")


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                          "default=nw=1:nk=1", path], capture_output=True, text=True).stdout.strip()
    try:
        return float(out)
    except ValueError:
        sys.exit(f"Could not read {path}; is it a video or audio file?")


def extract_audio(src, dst, start=None, length=None, bitrate="32k"):
    """Mono 16 kHz speech audio: small enough for the APIs, all Whisper needs."""
    cmd = ["ffmpeg", "-y", "-v", "error"]
    if start is not None:
        cmd += ["-ss", f"{start:.3f}"]
    cmd += ["-i", src]
    if length is not None:
        cmd += ["-t", f"{length:.3f}"]
    cmd += ["-vn", "-ac", "1", "-ar", "16000", "-c:a", "libmp3lame", "-b:a", bitrate, dst]
    subprocess.run(cmd, check=True)


# ---------- routes ----------

def from_subtitles(path):
    """Parse SRT or VTT. Word times are spread evenly over each cue (no word timing in these files)."""
    text = open(path, encoding="utf-8-sig", errors="replace").read()
    stamp = r"(\d+:)?(\d{1,2}):(\d{2})[.,](\d{3})"
    cue = re.compile(stamp + r"\s*-->\s*" + stamp + r"[^\n]*\n(.*?)(?:\n\s*\n|\Z)", re.S)

    def secs(h, m, s, ms):
        return int((h or "0:")[:-1] or 0) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000

    words = []
    for m in cue.finditer(text):
        a, b = secs(*m.group(1, 2, 3, 4)), secs(*m.group(5, 6, 7, 8))
        body = re.sub(r"<[^>]+>", "", m.group(9)).replace("\n", " ").strip()
        toks = body.split()
        if not toks or b <= a:
            continue
        step = (b - a) / len(toks)
        for i, t in enumerate(toks):
            if words and words[-1]["w"] == t and abs(words[-1]["start"] - (a + i * step)) < 1.5:
                continue  # rolling captions repeat words; skip the duplicates
            words.append({"w": t, "start": round(a + i * step, 3), "end": round(a + (i + 1) * step, 3)})
    if not words:
        sys.exit(f"No captions found in {path}")
    return words, "subtitles (word times estimated)"


def post_multipart(url, key, fields, file_path):
    boundary = uuid.uuid4().hex
    body = bytearray()
    for name, value in fields:
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"\r\n\r\n{value}\r\n".encode()
    body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"audio.mp3\"\r\n"
             "Content-Type: audio/mpeg\r\n\r\n").encode()
    body += open(file_path, "rb").read() + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(url, data=bytes(body), method="POST", headers={
        "Authorization": f"Bearer {key}", "Content-Type": f"multipart/form-data; boundary={boundary}"})
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"Transcription API error {e.code}: {e.read().decode(errors='replace')[:400]}")
    except urllib.error.URLError as e:
        if "CERTIFICATE_VERIFY_FAILED" in str(e.reason) and shutil.which("curl"):
            cmd = ["curl", "-sS", url, "-H", f"Authorization: Bearer {key}", "-F", f"file=@{file_path}"]
            for name, value in fields:
                cmd += ["-F", f"{name}={value}"]
            return json.loads(subprocess.run(cmd, capture_output=True, text=True, check=True).stdout)
        sys.exit(f"Could not reach the transcription API: {e.reason}")


def via_api(src, engine, tmp):
    url, env, model = API[engine]
    key = os.environ.get(env)
    if not key:
        sys.exit(f"{env} is not set")
    total = duration(src)
    words, start = [], 0.0
    while start < total:
        length = min(CHUNK_SECONDS, total - start)
        part = os.path.join(tmp, f"chunk-{int(start)}.mp3")
        extract_audio(src, part, start, length)
        if os.path.getsize(part) > API_LIMIT:
            extract_audio(src, part, start, length, bitrate="16k")
        print(f"  sending {start/60:.0f}-{(start+length)/60:.0f} min to {engine}...", flush=True)
        r = post_multipart(url, key, [("model", model), ("response_format", "verbose_json"),
                                      ("timestamp_granularities[]", "word"),
                                      ("timestamp_granularities[]", "segment")], part)
        for w in r.get("words") or []:
            words.append({"w": w["word"].strip(), "start": round(w["start"] + start, 3),
                          "end": round(w["end"] + start, 3)})
        start += length
    if not words:
        sys.exit(f"{engine} returned no word timestamps")
    return words, f"{engine} ({model})"


def via_local(src, model_size, tmp):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("Local transcription needs faster-whisper: pip install faster-whisper\n"
                 "Or set GROQ_API_KEY / OPENAI_API_KEY, or pass an existing transcript with --from.")
    audio = os.path.join(tmp, "audio.mp3")
    extract_audio(src, audio, bitrate="64k")
    print(f"  transcribing locally with faster-whisper '{model_size}' (first run downloads the model)...",
          flush=True)
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, info = model.transcribe(audio, word_timestamps=True, vad_filter=True)
    words = []
    total = info.duration or 1
    last = 0
    for seg in segments:
        for w in seg.words or []:
            words.append({"w": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3)})
        if seg.end - last > 120:
            print(f"  {seg.end/total:.0%}", flush=True)
            last = seg.end
    return words, f"faster-whisper ({model_size}, {info.language})"


# ---------- output ----------

def merge_fragments(words):
    """Whisper sometimes splits "pre-launch" into "pre" + "-launch" or "we" + "'ve"; join them."""
    out = []
    for w in words:
        if out and w["w"][:1] in ("-", "'", "’") and len(w["w"]) > 1:
            out[-1] = {"w": out[-1]["w"] + w["w"], "start": out[-1]["start"], "end": w["end"]}
        else:
            out.append(w)
    return out


def sentences(words, max_gap=0.8, max_len=45):
    """One line per sentence (or a pause over 0.8 s), so every line starts where a clip can."""
    out, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        end_punct = w["w"][-1:] in ".?!"
        pause = nxt is not None and nxt["start"] - w["end"] > max_gap
        if nxt is None or end_punct or pause or len(cur) >= max_len:
            out.append({"start": cur[0]["start"], "end": cur[-1]["end"],
                        "text": " ".join(x["w"] for x in cur)})
            cur = []
    return out


def stamp(t):
    m, s = divmod(t, 60)
    h, m = divmod(int(m), 60)
    return f"{h}:{m:02d}:{s:04.1f}" if h else f"{m:02d}:{s:04.1f}"


def main():
    ap = argparse.ArgumentParser(description="Transcribe a video with word timestamps.")
    ap.add_argument("video")
    ap.add_argument("--out", default="work")
    ap.add_argument("--engine", choices=["auto", "local", "groq", "openai"], default="auto")
    ap.add_argument("--model", default="small", help="faster-whisper model: tiny, base, small, medium, large-v3")
    ap.add_argument("--from", dest="subs", help="use an existing .srt or .vtt transcript instead")
    a = ap.parse_args()
    need_ffmpeg()
    os.makedirs(a.out, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        if a.subs:
            words, source = from_subtitles(a.subs)
        else:
            engine = a.engine
            if engine == "auto":
                engine = "groq" if os.environ.get("GROQ_API_KEY") else \
                         "openai" if os.environ.get("OPENAI_API_KEY") else "local"
            words, source = via_local(a.video, a.model, tmp) if engine == "local" else via_api(a.video, engine, tmp)
    words = merge_fragments(words)
    sents = sentences(words)
    data = {"source": source, "video": os.path.abspath(a.video), "duration": duration(a.video),
            "words": words, "sentences": sents}
    with open(os.path.join(a.out, "transcript.json"), "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False)
    with open(os.path.join(a.out, "transcript.txt"), "w", encoding="utf-8") as fh:
        for s in sents:
            fh.write(f"[{stamp(s['start'])}-{stamp(s['end'])}] {s['text']}\n")
    print(f"{len(words)} words, {len(sents)} lines via {source} -> {a.out}/transcript.json, transcript.txt")


if __name__ == "__main__":
    main()
