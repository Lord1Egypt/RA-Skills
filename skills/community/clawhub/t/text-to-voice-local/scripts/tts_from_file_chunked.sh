#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -lt 2 ]; then
  echo "Usage: $0 INPUT_TXT OUTPUT_MP3 [VOICE]" >&2
  exit 1
fi
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INPUT_TXT="$1"
OUTPUT_MP3="$2"
VOICE="${3:-ru-RU-DmitryNeural}"
TMP_ROOT="${OPENCLAW_WORKSPACE:-$(pwd)}/tmp"
mkdir -p "$TMP_ROOT"
WORKDIR="$(mktemp -d "$TMP_ROOT/tts-chunks-XXXXXX")"
PARTS_TXT="$WORKDIR/parts.txt"
PARTS_LIST="$WORKDIR/parts-list.txt"
tmp_base="$(basename "$OUTPUT_MP3")"
tmp_stem="${tmp_base%.*}"
tmp_ext="${tmp_base##*.}"
[ "$tmp_ext" = "$tmp_base" ] && tmp_ext="mp3"
TMP_FINAL="$WORKDIR/${tmp_stem}.concat.$$.$tmp_ext"
cleanup(){ rm -rf "$WORKDIR"; rm -f "$TMP_FINAL"; }
trap cleanup EXIT
python3 - "$INPUT_TXT" "$PARTS_TXT" <<'PY'
import sys, re, pathlib
src = pathlib.Path(sys.argv[1]).read_text(encoding='utf-8').strip()
out = pathlib.Path(sys.argv[2])
limit = 260
text = re.sub(r'\s+', ' ', src).strip()
if not text:
    out.write_text('', encoding='utf-8')
    raise SystemExit(0)
sentences = re.split(r'(?<=[.!?…])\s+|(?<=[;:])\s+', text)
parts=[]; buf=''
for s in sentences:
    s=s.strip()
    if not s: continue
    chunks=[s[i:i+limit] for i in range(0,len(s),limit)] if len(s)>limit else [s]
    for c in chunks:
        if not buf: buf=c
        elif len(buf)+1+len(c)<=limit: buf += ' ' + c
        else:
            parts.append(buf); buf=c
if buf: parts.append(buf)
out.write_text('\n'.join(parts), encoding='utf-8')
PY
: > "$PARTS_LIST"
idx=0
while IFS= read -r part || [ -n "$part" ]; do
  [ -z "$part" ] && continue
  idx=$((idx+1))
  part_txt="$WORKDIR/part-$idx.txt"
  part_mp3="$WORKDIR/part-$idx.mp3"
  printf '%s' "$part" > "$part_txt"
  if "$SCRIPT_DIR/tts_from_file.sh" "$part_txt" "$part_mp3" "$VOICE" >/dev/null; then :; else sleep 1; "$SCRIPT_DIR/tts_from_file.sh" "$part_txt" "$part_mp3" "$VOICE" >/dev/null; fi
  [ -s "$part_mp3" ] || exit 1
  printf "file '%s'\n" "$part_mp3" >> "$PARTS_LIST"
done < "$PARTS_TXT"
expected=$(grep -c . "$PARTS_TXT" || true)
[ "$expected" -gt 0 ] || exit 1
FFMPEG_BIN="$(command -v ffmpeg || true)"
[ -n "$FFMPEG_BIN" ] || exit 1
set +e
"$FFMPEG_BIN" -y -f concat -safe 0 -i "$PARTS_LIST" -c copy -f mp3 "$TMP_FINAL" >/dev/null 2>&1
rc=$?
set -e
if [ "$rc" -ne 0 ]; then
  rm -f "$TMP_FINAL"
  set +e
  "$FFMPEG_BIN" -y -f concat -safe 0 -i "$PARTS_LIST" -c:a libmp3lame -b:a 48k -f mp3 "$TMP_FINAL" >/dev/null 2>&1
  rc=$?
  set -e
  [ "$rc" -eq 0 ] || exit 1
fi
[ -s "$TMP_FINAL" ] || exit 1
mv -f "$TMP_FINAL" "$OUTPUT_MP3"
trap - EXIT
rm -rf "$WORKDIR"
printf '%s\n' "$OUTPUT_MP3"
