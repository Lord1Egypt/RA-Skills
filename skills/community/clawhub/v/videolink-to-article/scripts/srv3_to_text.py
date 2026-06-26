"""
Convert YouTube srv3 (XML caption) to plain sentence-per-line text and SRT.

Use this when yt-dlp downloads `*.srv3` files but its `--convert-subs srt`
pipeline silently skips the conversion (typically because ffmpeg is not
available as the converter backend, or the srv3 variant produced by YouTube
is not understood by yt-dlp's built-in converter).

The script is stdlib-only — no external dependencies.

srv3 schema (simplified):
  <timedtext format="3">
    <body>
      <p t="START_MS" d="DURATION_MS">
        <s t="OFFSET" ac="conf">word</s>...
      </p>
      ...
    </body>
  </timedtext>

Each <p> is one caption line. Words may live in <s> child tags or directly in
the <p>'s text. We assemble per-<p> text, preserve original ordering, and
write both an SRT (for downstream tools that expect it) and a plain TXT
(one srv3 <p> per line, useful as input to srt_to_sentences.py or for direct
human review).

Usage:
    python srv3_to_text.py <input.srv3> <out_basename>

Produces:
    <out_basename>.srt
    <out_basename>.txt

Exit codes:
    0 on success
    1 on bad CLI usage
    2 if the input has no parseable <p> elements
"""
import sys, os, re, html
import xml.etree.ElementTree as ET

# UTF-8 console output so logs containing CJK text don't corrupt on
# legacy Windows code pages.
for _stream_name in ("stdout", "stderr"):
    _stream = getattr(sys, _stream_name, None)
    if _stream is not None and hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8")
        except Exception:
            pass


def parse_srv3(path):
    tree = ET.parse(path)
    root = tree.getroot()
    body = root.find("body")
    if body is None:
        return []
    lines = []
    for p in body.findall("p"):
        t = int(p.get("t", "0"))
        d = int(p.get("d", "0"))
        words = []
        if p.text:
            words.append(p.text)
        for s in p.findall("s"):
            if s.text:
                words.append(s.text)
            if s.tail:
                words.append(s.tail)
        text = "".join(words)
        text = html.unescape(text)
        text = re.sub(r"\s+", " ", text).strip()
        if not text:
            continue
        lines.append((t, t + d, text))
    return lines


def srt_ts(ms):
    s, ms_ = divmod(int(ms), 1000)
    h, s = divmod(s, 3600)
    m, s = divmod(s, 60)
    return f"{h:02d}:{m:02d}:{s:02d},{ms_:03d}"


def write_srt(lines, path):
    with open(path, "w", encoding="utf-8") as f:
        for i, (s, e, t) in enumerate(lines, 1):
            f.write(f"{i}\n{srt_ts(s)} --> {srt_ts(e)}\n{t}\n\n")


def write_text(lines, path):
    with open(path, "w", encoding="utf-8") as f:
        for s, e, t in lines:
            f.write(t + "\n")


def main():
    if len(sys.argv) != 3:
        print("usage: srv3_to_text.py <input.srv3> <out_basename>", file=sys.stderr)
        sys.exit(1)
    inp, outbase = sys.argv[1], sys.argv[2]
    lines = parse_srv3(inp)
    if not lines:
        print(f"error: no parseable <p> elements in {inp}", file=sys.stderr)
        sys.exit(2)
    os.makedirs(os.path.dirname(os.path.abspath(outbase)) or ".", exist_ok=True)
    write_srt(lines, outbase + ".srt")
    write_text(lines, outbase + ".txt")
    print(f"Wrote {outbase}.srt and {outbase}.txt with {len(lines)} segments")


if __name__ == "__main__":
    main()
