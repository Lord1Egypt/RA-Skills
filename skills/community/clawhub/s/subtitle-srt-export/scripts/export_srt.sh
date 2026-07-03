#!/usr/bin/env bash
# subtitle-srt-export
#
# Reads measured word timings from <job>/input.json (written by elevenlabs-tts)
# and writes <job>/subtitles.srt for upload (YouTube, etc.).
# No API call. Re-runnable. Does not touch input.json.
set -euo pipefail

JOB="${1:-}"                   # e.g. examples/demo-job
if [ -z "$JOB" ]; then
  echo "ERROR: usage: export_srt.sh <job-folder>" >&2; exit 1
fi
INPUT="$JOB/input.json"
SRT="$JOB/subtitles.srt"

# Precondition: word timings must exist
WORDCOUNT=$(jq '[.subtitles[].words[]] | length' "$INPUT")
if [ "$WORDCOUNT" -lt 1 ]; then
  echo "ERROR: no word timings in $INPUT — run elevenlabs-tts first"; exit 1
fi

# Step 1: flatten all words across subtitle blocks, group into cues, emit
#         "start|end|text" lines (one per cue).
jq -r '
  ([.subtitles[].words[]]) as $words |
  (3.5) as $maxdur | (10) as $maxwords |
  reduce $words[] as $w (
    {cues: [], cur: null};
    if .cur == null then
      .cur = {words: [$w.word], start: $w.start, end: $w.end}
    else
      ((.cur.end - .cur.start) >= $maxdur)        as $toolong |
      ((.cur.words | length) >= $maxwords)        as $toomany |
      (.cur.words[-1] | test("[.?!]$"))           as $broke   |
      if ($broke or $toolong or $toomany) then
        .cues += [.cur] | .cur = {words: [$w.word], start: $w.start, end: $w.end}
      else
        .cur.words += [$w.word] | .cur.end = $w.end
      end
    end
  )
  | (if .cur != null then .cues += [.cur] else . end)
  | .cues[]
  | "\(.start)|\(.end)|\(.words | join(" "))"
' "$INPUT" > "$JOB/.cues.tmp"

# Step 2: convert cues to SRT (awk handles HH:MM:SS,mmm formatting + numbering)
awk -F'|' '
  function ts(t,   h,m,s,ms) {
    h=int(t/3600); t-=h*3600; m=int(t/60); t-=m*60; s=int(t); ms=int((t-s)*1000 + 0.5)
    if (ms==1000){s++; ms=0}
    return sprintf("%02d:%02d:%02d,%03d", h, m, s, ms)
  }
  { printf "%d\n%s --> %s\n%s\n\n", NR, ts($1), ts($2), $3 }
' "$JOB/.cues.tmp" > "$SRT"

rm -f "$JOB/.cues.tmp"

# Step 3: verify
CUES=$(grep -c ' --> ' "$SRT")
echo "Wrote $SRT with $CUES cues from $WORDCOUNT words"
