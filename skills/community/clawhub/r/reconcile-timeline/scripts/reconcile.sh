#!/usr/bin/env bash
set -euo pipefail
JOB="${1:-}"
if [ -z "$JOB" ]; then
  echo "FAILED: usage: reconcile.sh <job-folder>" >&2
  exit 1
fi

INPUT="$JOB/input.json"

# 1. Validate JSON
if ! jq empty "$INPUT" 2>/dev/null; then
  echo "FAILED: $INPUT missing or invalid JSON" >&2; exit 1
fi

# 2. Long-form guard
SCHEMA=$(jq -r '.schema_version // ""' "$INPUT")
if [ "$SCHEMA" != "3.0-long" ]; then
  echo "FAILED: reconcile-timeline is long-form only; schema_version is '$SCHEMA'" >&2
  exit 1
fi

# 3. Measured words exist
WORDCOUNT=$(jq '[.subtitles[].words[]] | length' "$INPUT")
if [ "$WORDCOUNT" -lt 1 ]; then
  echo "FAILED: no measured word timings in subtitles[]" >&2; exit 1
fi

# 4. Every segment has vo_line
MISSING_VO=$(jq -r '
  [ .timeline | to_entries[] | select((.value.vo_line // "") == "") | .key ]
  | if length > 0 then "segments missing vo_line: " + (map(tostring) | join(", ")) else "" end
' "$INPUT")
if [ -n "$MISSING_VO" ]; then
  echo "FAILED: $MISSING_VO" >&2; exit 1
fi

# 5. Re-anchor
cat <<'JQEOF' > "$JOB/reconcile.jq"
([.subtitles[].words[]]) as $W |
def toks(s): (s | gsub("[[:space:]]+"; " ") | ltrimstr(" ") | rtrimstr(" ")
                | if . == "" then [] else split(" ") end);
(.timeline | length) as $T |
[ range(0; $T) as $i
  | { cursor: 0, timeline: .timeline, words: $W, ok: true, failidx: null }
  | reduce range(0; $T) as $j (.;
      (.timeline[$j].vo_line) as $vl |
      (toks($vl) | length) as $n |
      if (.cursor + $n) > (.words | length) then
        .ok = false | .failidx = $j
      else
        (.words[.cursor]) as $first |
        (.words[.cursor + $n - 1]) as $last |
        .timeline[$j].start_time = $first.start |
        .timeline[$j].end_time   = $last.end |
        .cursor = (.cursor + $n)
      end
    )
]
| last
| if (.ok | not) then
    error("RECONCILE_OVERRUN at segment \(.failidx): vo_line word count exceeds remaining measured words")
  else
    { timeline: .timeline, audio_duration: .timeline[-1].end_time }
  end
JQEOF

OUT=$(mktemp)
jq -f "$JOB/reconcile.jq" "$INPUT" > "$OUT" 2> "$JOB/.reconcile.err"
if [ $? -ne 0 ] || [ ! -s "$OUT" ]; then
  echo "FAILED: reconcile could not map vo_lines to measured words" >&2
  cat "$JOB/.reconcile.err" >&2
  rm -f "$OUT"
  exit 1
fi
rm -f "$JOB/.reconcile.err"

# 6. Safety check
VO_TOKENS=$(jq '[.timeline[].vo_line | gsub("[[:space:]]+";" ") | ltrimstr(" ") | rtrimstr(" ") | if .=="" then [] else split(" ") end | length] | add' "$INPUT")
TOL=$(( WORDCOUNT / 20 )); [ "$TOL" -lt 5 ] && TOL=5
DIFF=$(( VO_TOKENS - WORDCOUNT )); [ "$DIFF" -lt 0 ] && DIFF=$(( -DIFF ))
if [ "$DIFF" -gt "$TOL" ]; then
  echo "FAILED: vo_line word total ($VO_TOKENS) diverges from measured words ($WORDCOUNT) by $DIFF (tolerance $TOL)." >&2
  echo "The synthesized VO is not fully represented as segment vo_lines. Reconcile aborted." >&2
  exit 1
fi

# 7. Merge into input.json and verify monotonicity
MERGED=$(mktemp)
jq -s '.[0] * {timeline: .[1].timeline, audio_duration: .[1].audio_duration}' "$INPUT" "$OUT" > "$MERGED"
mv "$MERGED" "$INPUT"
rm -f "$OUT"

BAD=$(jq -r '
  [ range(0; (.timeline|length)) as $i
    | .timeline[$i] as $s
    | select(($s.end_time < $s.start_time)
             or ($i > 0 and ($s.start_time < .timeline[$i-1].end_time - 0.001)))
    | $i ] | if length>0 then (map(tostring)|join(", ")) else "" end
' "$INPUT")
if [ -n "$BAD" ]; then
  echo "FAILED: post-reconcile timeline has non-monotonic segments at: $BAD" >&2
  exit 1
fi

# 8. Report
NEWDUR=$(jq -r '.audio_duration' "$INPUT")
SEGS=$(jq '.timeline | length' "$INPUT")
echo "OK reconciled $SEGS segments to measured audio"
echo "audio_duration set to ${NEWDUR}s"
