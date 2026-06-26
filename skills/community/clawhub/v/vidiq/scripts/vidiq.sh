#!/usr/bin/env bash
# ============================================================
# VIDIQ - Video Intelligence & Query Tool
# ============================================================
# Usage:
#   vidiq.sh <url_or_path> info              - Get video metadata
#   vidiq.sh <url_or_path> frames [N]        - Extract N frames evenly (default 10)
#   vidiq.sh <url_or_path> frame <time>      - Extract single frame at timestamp (HH:MM:SS or seconds)
#   vidiq.sh <url_or_path> clip <start> <end> [out] - Extract clip between timestamps
#   vidiq.sh <url_or_path> audio [out]       - Extract audio track
#   vidiq.sh <url_or_path> transcript        - Extract audio + transcribe (if whisper available)
#   vidiq.sh <url_or_path> download [quality] - Download video (best/720/480/audio)
#   vidiq.sh <url_or_path> gif <start> <duration> [out] - Create GIF from segment
#   vidiq.sh <url_or_path> mosaic [cols] [N] - Create mosaic/contact sheet of N frames
#   vidiq.sh <url_or_path> scenes [threshold] - Detect scene changes
#
# For URLs: auto-downloads via yt-dlp first
# Output goes to /tmp/vidiq/ by default
# ============================================================

set -euo pipefail

WORK="/tmp/vidiq"
mkdir -p "$WORK"

SRC="$1"
CMD="${2:-info}"
shift 2 || true

# ---- Download if URL ----
LOCAL="$SRC"
if [[ "$SRC" == http* ]]; then
    echo "[vidiq] Downloading video from URL..."
    # Check if already downloaded
    HASH=$(echo -n "$SRC" | md5sum | cut -c1-12)
    CACHED="$WORK/dl_${HASH}.mp4"
    if [[ -f "$CACHED" ]]; then
        echo "[vidiq] Using cached download: $CACHED"
        LOCAL="$CACHED"
    else
        yt-dlp -f "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best" \
            --merge-output-format mp4 \
            -o "$CACHED" \
            --no-playlist \
            --socket-timeout 30 \
            "$SRC" 2>&1 | tail -5
        LOCAL="$CACHED"
        echo "[vidiq] Downloaded: $CACHED"
    fi
fi

if [[ ! -f "$LOCAL" ]]; then
    echo "[vidiq] ERROR: File not found: $LOCAL"
    exit 1
fi

# ---- Get basic info ----
get_duration() {
    ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$LOCAL" 2>/dev/null | cut -d. -f1
}

get_info() {
    ffprobe -v quiet -print_format json -show_format -show_streams "$LOCAL" 2>/dev/null
}

# ---- Commands ----
case "$CMD" in
    info)
        echo "[vidiq] Video info:"
        DUR=$(get_duration)
        INFO=$(get_info)
        echo "$INFO" | python3 -c "
import json,sys
d=json.load(sys.stdin)
fmt=d.get('format',{})
print(f'  File: {fmt.get(\"filename\",\"?\")[-60:]}')
print(f'  Duration: {float(fmt.get(\"duration\",0)):.1f}s ({int(float(fmt.get(\"duration\",0)))//60}m {int(float(fmt.get(\"duration\",0)))%60}s)')
print(f'  Size: {int(fmt.get(\"size\",0))/1048576:.1f} MB')
print(f'  Bitrate: {int(fmt.get(\"bit_rate\",0))/1000:.0f} kbps')
for s in d.get('streams',[]):
    if s['codec_type']=='video':
        print(f'  Video: {s.get(\"codec_name\")} {s.get(\"width\")}x{s.get(\"height\")} @ {eval(s.get(\"r_frame_rate\",\"0/1\")):.1f}fps')
    elif s['codec_type']=='audio':
        print(f'  Audio: {s.get(\"codec_name\")} {s.get(\"sample_rate\")}Hz {s.get(\"channels\")}ch')
"
        ;;

    frames)
        N="${1:-10}"
        DUR=$(get_duration)
        echo "[vidiq] Extracting $N frames from ${DUR}s video..."
        OUTDIR="$WORK/frames_$(date +%s)"
        mkdir -p "$OUTDIR"
        
        if (( N == 1 )); then
            ffmpeg -y -ss "$((DUR/2))" -i "$LOCAL" -frames:v 1 -q:v 2 "$OUTDIR/frame_001.jpg" 2>/dev/null
        else
            INTERVAL=$(( DUR / (N - 1) ))
            for i in $(seq 1 "$N"); do
                TS=$(( (i - 1) * INTERVAL ))
                if (( TS > DUR )); then TS=$DUR; fi
                FNAME=$(printf "frame_%03d_%02dm%02ds.jpg" "$i" "$((TS/60))" "$((TS%60))")
                ffmpeg -y -ss "$TS" -i "$LOCAL" -frames:v 1 -q:v 2 "$OUTDIR/$FNAME" 2>/dev/null
                echo "  [$i/$N] ${TS}s -> $FNAME"
            done
        fi
        echo "[vidiq] Frames saved to: $OUTDIR"
        ls -la "$OUTDIR"/*.jpg 2>/dev/null | awk '{print "  "$NF" ("$5" bytes)"}'
        ;;

    frame)
        TIME="${1:-0}"
        # Convert HH:MM:SS to seconds if needed
        OUT="${2:-$WORK/frame_$(date +%s).jpg}"
        echo "[vidiq] Extracting frame at $TIME..."
        ffmpeg -y -ss "$TIME" -i "$LOCAL" -frames:v 1 -q:v 2 "$OUT" 2>/dev/null
        echo "[vidiq] Saved: $OUT"
        ;;

    clip)
        START="${1:?Need start time}"
        END="${2:?Need end time}"
        OUT="${3:-$WORK/clip_$(date +%s).mp4}"
        echo "[vidiq] Extracting clip ${START} -> ${END}..."
        ffmpeg -y -ss "$START" -to "$END" -i "$LOCAL" -c copy -avoid_negative_ts 1 "$OUT" 2>/dev/null
        SIZE=$(du -h "$OUT" | cut -f1)
        echo "[vidiq] Saved: $OUT ($SIZE)"
        ;;

    audio)
        OUT="${1:-$WORK/audio_$(date +%s).mp3}"
        echo "[vidiq] Extracting audio..."
        ffmpeg -y -i "$LOCAL" -vn -acodec libmp3lame -q:a 2 "$OUT" 2>/dev/null
        SIZE=$(du -h "$OUT" | cut -f1)
        echo "[vidiq] Saved: $OUT ($SIZE)"
        ;;

    gif)
        START="${1:?Need start time}"
        DUR="${2:-5}"
        OUT="${3:-$WORK/gif_$(date +%s).gif}"
        echo "[vidiq] Creating GIF from $START (${DUR}s)..."
        ffmpeg -y -ss "$START" -t "$DUR" -i "$LOCAL" \
            -vf "fps=12,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" \
            "$OUT" 2>/dev/null
        SIZE=$(du -h "$OUT" | cut -f1)
        echo "[vidiq] Saved: $OUT ($SIZE)"
        ;;

    mosaic)
        COLS="${1:-4}"
        N="${2:-16}"
        OUT="$WORK/mosaic_$(date +%s).jpg"
        DUR=$(get_duration)
        echo "[vidiq] Creating ${COLS}x mosaic from $N frames..."
        
        TMPDIR="$WORK/.mosaic_tmp_$$"
        mkdir -p "$TMPDIR"
        INTERVAL=$(( DUR / N ))
        for i in $(seq 1 "$N"); do
            TS=$(( (i - 1) * INTERVAL + INTERVAL / 2 ))
            ffmpeg -y -ss "$TS" -i "$LOCAL" -frames:v 1 -q:v 3 -vf "scale=320:-1" "$TMPDIR/f$(printf '%03d' $i).jpg" 2>/dev/null
        done
        
        # Use ffmpeg tile filter
        ffmpeg -y -pattern_type glob -i "$TMPDIR/f*.jpg" \
            -vf "tile=${COLS}x$(( (N + COLS - 1) / COLS ))" -q:v 2 "$OUT" 2>/dev/null
        rm -rf "$TMPDIR"
        echo "[vidiq] Saved: $OUT"
        ;;

    scenes)
        THRESHOLD="${1:-0.3}"
        echo "[vidiq] Detecting scene changes (threshold: $THRESHOLD)..."
        ffmpeg -i "$LOCAL" -vf "select='gt(scene,$THRESHOLD)',showinfo" -vsync vfr -f null - 2>&1 \
            | grep "showinfo" | sed 's/.*pts_time:\([0-9.]*\).*/\1/' | while read ts; do
                MIN=$(printf "%02d" "$(echo "$ts/60" | bc)")
                SEC=$(printf "%05.2f" "$(echo "$ts%60" | bc)")
                echo "  Scene change at ${MIN}:${SEC} (${ts}s)"
            done
        ;;

    download)
        QUALITY="${1:-best}"
        OUT="$WORK/video_$(date +%s).mp4"
        echo "[vidiq] Video already downloaded at: $LOCAL"
        cp "$LOCAL" "$OUT" 2>/dev/null || true
        echo "[vidiq] Copy at: $OUT"
        ;;

    *)
        echo "[vidiq] Unknown command: $CMD"
        echo "Commands: info, frames, frame, clip, audio, gif, mosaic, scenes, download"
        exit 1
        ;;
esac
