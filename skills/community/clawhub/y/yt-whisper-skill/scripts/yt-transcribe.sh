#!/bin/bash
# yt-whisper - downloads YouTube audio, transcribes with Whisper, saves clean output

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV_DIR="$REPO_ROOT/.venv"
OUTPUT_DIR="${HOME}/Transcriptions"
TEMP_DIR="/tmp/yt-transcribe-$$"
YT_DLP_BIN=""
WHISPER_BIN=""
WHISPER_PYTHON=""
CATEGORY=""
MODEL=""
FAILURES=0
SUCCESSES=0
SKIPPED=0
SUPPORTED_CATEGORIES=(
    "Announcements"
    "CourseLaunch"
    "Events"
    "MediaCritique"
    "Medical"
    "PersonalStories"
    "Philosophy"
    "Political"
    "PornDiscussion"
    "Psychology"
    "Technology"
    "Unsorted"
)

find_yt_dlp() {
    if [ -x "$VENV_DIR/bin/yt-dlp" ]; then
        echo "$VENV_DIR/bin/yt-dlp"
        return 0
    fi
    command -v yt-dlp 2>/dev/null || true
}

find_whisper_bin() {
    if [ -x "$VENV_DIR/bin/whisper" ]; then
        echo "$VENV_DIR/bin/whisper"
        return 0
    fi
    command -v whisper 2>/dev/null || true
}

find_whisper_python() {
    if [ -x "$VENV_DIR/bin/python" ]; then
        echo "$VENV_DIR/bin/python"
        return 0
    fi
    command -v python3 2>/dev/null || true
}

# yt-dlp needs a JavaScript runtime to solve YouTube's signature challenges.
# Without one, yt-dlp fails with a misleading "HTTP Error 403: Forbidden".
# The gateway PATH usually provides node, but non-interactive shells (ssh, cron) do not,
# so resolve it explicitly and hand the concrete location to yt-dlp.
find_js_runtime() {
    local name=""
    local resolved=""
    local candidate=""
    local nvm_candidates=""
    local nvm_node=""

    for name in node deno bun quickjs; do
        resolved="$(command -v "$name" 2>/dev/null || true)"
        if [ -n "$resolved" ] && [ -x "$resolved" ]; then
            echo "$name:$resolved"
            return 0
        fi
    done

    for candidate in \
        "$HOME/.local/bin/node" \
        "$HOME/.nvm/current/bin/node" \
        /usr/local/bin/node \
        /usr/bin/node \
        /snap/bin/node \
        "$HOME/.deno/bin/deno" \
        "$HOME/.local/bin/deno" \
        /usr/local/bin/deno \
        /usr/bin/deno \
        "$HOME/.bun/bin/bun" \
        /usr/local/bin/bun \
        /usr/bin/bun \
        /usr/local/bin/qjs \
        /usr/bin/qjs; do
        if [ -x "$candidate" ]; then
            case "$candidate" in
                */deno) echo "deno:$candidate" ;;
                */bun) echo "bun:$candidate" ;;
                */qjs|*/quickjs) echo "quickjs:$candidate" ;;
                *) echo "node:$candidate" ;;
            esac
            return 0
        fi
    done

    nvm_candidates="$(ls -1d "$HOME"/.nvm/versions/node/*/bin/node 2>/dev/null | sort -V -r || true)"
    for nvm_node in $nvm_candidates; do
        if [ -x "$nvm_node" ]; then
            echo "node:$nvm_node"
            return 0
        fi
    done

    return 1
}

parse_time_to_seconds() {
    local raw="${1:-}"
    if [ -z "$raw" ]; then
        echo ""
        return 0
    fi

    if [[ "$raw" =~ ^[0-9]+$ ]]; then
        echo "$raw"
        return 0
    fi

    local hours=0
    local minutes=0
    local seconds=0

    if [[ "$raw" =~ ([0-9]+)h ]]; then
        hours="${BASH_REMATCH[1]}"
    fi
    if [[ "$raw" =~ ([0-9]+)m ]]; then
        minutes="${BASH_REMATCH[1]}"
    fi
    if [[ "$raw" =~ ([0-9]+)s ]]; then
        seconds="${BASH_REMATCH[1]}"
    fi

    if [ "$hours" -eq 0 ] && [ "$minutes" -eq 0 ] && [ "$seconds" -eq 0 ]; then
        echo ""
        return 0
    fi

    echo $((hours * 3600 + minutes * 60 + seconds))
}

extract_query_param() {
    local url="$1"
    local key="$2"
    local query=""

    query="${url#*\?}"
    if [ "$query" = "$url" ]; then
        echo ""
        return 0
    fi

    printf '%s\n' "$query" | tr '&' '\n' | awk -F= -v k="$key" '$1 == k {print $2; exit}'
}

extract_video_id_from_input() {
    local raw="${1:-}"
    local video_id=""

    if [[ "$raw" =~ ^[A-Za-z0-9_-]{11}$ ]]; then
        echo "$raw"
        return 0
    fi

    video_id="$(printf '%s\n' "$raw" | sed -E \
        -e 's|.*[?&]v=([A-Za-z0-9_-]{11}).*|\1|' \
        -e 's|.*youtu\.be/([A-Za-z0-9_-]{11})(\?.*)?$|\1|' \
        -e 's|.*youtube\.com/live/([A-Za-z0-9_-]{11})(\?.*)?$|\1|' \
        -e 's|.*youtube\.com/shorts/([A-Za-z0-9_-]{11})(\?.*)?$|\1|' \
        -e 's|.*youtube\.com/embed/([A-Za-z0-9_-]{11})(\?.*)?$|\1|')"

    if [[ "$video_id" =~ ^[A-Za-z0-9_-]{11}$ ]]; then
        echo "$video_id"
        return 0
    fi

    return 1
}

normalize_youtube_input() {
    local raw="${1:-}"
    local video_id=""
    local query=""
    local watch_url=""

    if [ -z "$raw" ]; then
        return 1
    fi

    if [[ "$raw" =~ ^https?:// ]]; then
        video_id="$(extract_video_id_from_input "$raw" 2>/dev/null || true)"
        if [ -z "$video_id" ]; then
            return 1
        fi
        query="${raw#*\?}"
        if [ "$query" = "$raw" ]; then
            query=""
        fi
        watch_url="https://www.youtube.com/watch?v=$video_id"
        if [ -n "$query" ]; then
            case "$query" in
                v=*) ;;
                *) watch_url="${watch_url}&${query}" ;;
            esac
        fi
        echo "$watch_url"
        return 0
    fi

    if [[ "$raw" =~ ^[A-Za-z0-9_-]{11}$ ]]; then
        echo "https://www.youtube.com/watch?v=$raw"
        return 0
    fi

    return 1
}

pick_model_for_duration() {
    local duration_s="${1:-0}"
    local preferred="${2:-}"

    if [ -n "$preferred" ]; then
        echo "$preferred"
        return 0
    fi

    # Long videos need the fastest reasonable GPU path to avoid OpenClaw tool timeouts.
    if [ "$duration_s" -ge 1800 ]; then
        echo "turbo"
    else
        echo "base"
    fi
}

normalize_category() {
    local raw="${1:-}"
    local normalized
    normalized="$(printf '%s' "$raw" | tr '[:upper:]' '[:lower:]' | tr -cd '[:alnum:]')"

    case "$normalized" in
        announcements) echo "Announcements" ;;
        courselaunch) echo "CourseLaunch" ;;
        events) echo "Events" ;;
        mediacritique) echo "MediaCritique" ;;
        medical) echo "Medical" ;;
        personalstories) echo "PersonalStories" ;;
        philosophy) echo "Philosophy" ;;
        political) echo "Political" ;;
        porndiscussion) echo "PornDiscussion" ;;
        psychology) echo "Psychology" ;;
        technology) echo "Technology" ;;
        unsorted) echo "Unsorted" ;;
        *) return 1 ;;
    esac
}

sanitize_freeform_category() {
    local raw="${1:-}"
    local known=""
    local sanitized=""

    if known="$(normalize_category "$raw" 2>/dev/null)"; then
        echo "$known"
        return 0
    fi

    sanitized="$(printf '%s' "$raw" | sed -E 's/[[:space:]]+/_/g; s/[^[:alnum:]_-]+/_/g; s/_+/_/g; s/^_+//; s/_+$//')"
    if [ -z "$sanitized" ]; then
        return 1
    fi

    printf '%.64s\n' "$sanitized"
}

infer_category_from_title() {
    local title="${1:-}"
    local haystack
    haystack="$(printf '%s' "$title" | tr '[:upper:]' '[:lower:]')"

    if [[ "$haystack" == *course* || "$haystack" == *launch* || "$haystack" == *masterclass* || "$haystack" == *webinar* || "$haystack" == *bootcamp* ]]; then
        echo "CourseLaunch"
    elif [[ "$haystack" == *announcement* || "$haystack" == *update* || "$haystack" == *breaking* || "$haystack" == *newsroom* ]]; then
        echo "Announcements"
    elif [[ "$haystack" == *event* || "$haystack" == *conference* || "$haystack" == *summit* || "$haystack" == *festival* || "$haystack" == *expo* || "$haystack" == *meetup* ]]; then
        echo "Events"
    elif [[ "$haystack" == *review* || "$haystack" == *reaction* || "$haystack" == *critique* || "$haystack" == *analysis* || "$haystack" == *commentary* ]]; then
        echo "MediaCritique"
    elif [[ "$haystack" == *medical* || "$haystack" == *medicine* || "$haystack" == *doctor* || "$haystack" == *hospital* || "$haystack" == *health* || "$haystack" == *virus* || "$haystack" == *vaccine* || "$haystack" == *cancer* || "$haystack" == *clinical* || "$haystack" == *hiv* ]]; then
        echo "Medical"
    elif [[ "$haystack" == *story* || "$haystack" == *"my journey"* || "$haystack" == *"my life"* || "$haystack" == *experience* || "$haystack" == *diary* || "$haystack" == *memoir* ]]; then
        echo "PersonalStories"
    elif [[ "$haystack" == *philosophy* || "$haystack" == *philosopher* || "$haystack" == *ethics* || "$haystack" == *consciousness* || "$haystack" == *existential* || "$haystack" == *humanity* || "$haystack" == *bostrom* || "$haystack" == *meaning* || "$haystack" == *utopia* ]]; then
        echo "Philosophy"
    elif [[ "$haystack" == *politics* || "$haystack" == *political* || "$haystack" == *election* || "$haystack" == *government* || "$haystack" == *state* || "$haystack" == *policy* || "$haystack" == *senate* || "$haystack" == *parliament* || "$haystack" == *democracy* || "$haystack" == *communism* ]]; then
        echo "Political"
    elif [[ "$haystack" == *porn* || "$haystack" == *onlyfans* || "$haystack" == *nsfw* || "$haystack" == *adult* ]]; then
        echo "PornDiscussion"
    elif [[ "$haystack" == *psychology* || "$haystack" == *psychological* || "$haystack" == *trauma* || "$haystack" == *depression* || "$haystack" == *anxiety* || "$haystack" == *mindset* || "$haystack" == *behavior* ]]; then
        echo "Psychology"
    elif [[ "$haystack" == *ai* || "$haystack" == *"artificial intelligence"* || "$haystack" == *"machine learning"* || "$haystack" == *software* || "$haystack" == *programming* || "$haystack" == *tech* || "$haystack" == *technology* || "$haystack" == *robot* || "$haystack" == *automation* || "$haystack" == *"open source"* ]]; then
        echo "Technology"
    else
        echo "Unsorted"
    fi
}

YT_DLP_BIN="$(find_yt_dlp)"
WHISPER_BIN="$(find_whisper_bin)"
WHISPER_PYTHON="$(find_whisper_python)"

JS_RUNTIME="$(find_js_runtime 2>/dev/null || true)"
JS_RUNTIME_ARGS=()
if [ -n "$JS_RUNTIME" ]; then
    JS_RUNTIME_ARGS=(--js-runtimes "$JS_RUNTIME")
fi

if [ -z "$YT_DLP_BIN" ]; then
    echo "Error: yt-dlp not found. Install it in $VENV_DIR or in PATH."
    exit 1
fi

if [ -z "$WHISPER_BIN" ] && [ -z "$WHISPER_PYTHON" ]; then
    echo "Error: neither whisper nor python3 is available."
    exit 1
fi

if ! command -v ffmpeg >/dev/null 2>&1; then
    echo "Error: ffmpeg not found in PATH."
    exit 1
fi

if [ ${#JS_RUNTIME_ARGS[@]} -eq 0 ]; then
    echo "Warning: no JavaScript runtime found (looked for node, deno, bun, quickjs)."
    echo "         YouTube will likely reject the download with 'HTTP Error 403: Forbidden'."
    echo "         Install one (e.g. node) or put it in PATH, then retry."
fi

mkdir -p "$OUTPUT_DIR"

# Help
if [ $# -eq 0 ] || [ "$1" == "--help" ] || [ "$1" == "-h" ]; then
    echo "Usage: yt-transcribe <youtube_url_or_id> [youtube_url_or_id2...] [--language LANG] [--category CATEGORY] [--output-dir DIR]"
    echo "       yt-transcribe <youtube_url_or_id> [--model MODEL]"
    echo ""
    echo "Examples:"
    echo "  yt-transcribe 'https://youtu.be/abc123def45'"
    echo "  yt-transcribe 'https://www.youtube.com/live/abc123def45?t=276s' --language en"
    echo "  yt-transcribe 'abc123def45' --category Philosophy"
    echo "  yt-transcribe URL1 URL2 URL3"
    echo ""
    echo "Supported categories: ${SUPPORTED_CATEGORIES[*]}"
    exit 0
fi

URLS=()
LANGUAGE=""
OUTPUT_DIR_ARG=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --language|-l)
            LANGUAGE="$2"
            shift 2
            ;;
        --output-dir|-o)
            OUTPUT_DIR_ARG="$2"
            shift 2
            ;;
        --category|-c)
            if ! CATEGORY="$(sanitize_freeform_category "$2")"; then
                echo "Error: Invalid category: $2"
                exit 1
            fi
            shift 2
            ;;
        --model|-m)
            MODEL="$2"
            shift 2
            ;;
        *)
            if NORMALIZED_URL="$(normalize_youtube_input "$1")"; then
                URLS+=("$NORMALIZED_URL")
                shift
            else
                echo "Unknown option: $1"
                exit 1
            fi
            ;;
    esac
done

if [ -n "$OUTPUT_DIR_ARG" ]; then
    OUTPUT_DIR="$OUTPUT_DIR_ARG"
    mkdir -p "$OUTPUT_DIR"
fi

if [ ${#URLS[@]} -eq 0 ]; then
    echo "Error: No YouTube URLs provided"
    exit 1
fi

run_whisper() {
    local input_file="$1"
    shift

    if [ -n "$WHISPER_BIN" ]; then
        "$WHISPER_BIN" "$input_file" "$@"
        return 0
    fi

    "$WHISPER_PYTHON" -m whisper "$input_file" "$@"
}

for URL in "${URLS[@]}"; do
    :
done

for URL in "${URLS[@]}"; do
    echo "========================================="
    echo "Processing: $URL"
    echo "========================================="

    # Extract video ID for filename
    VIDEO_ID="$(extract_video_id_from_input "$URL" 2>/dev/null || true)"

    if [ -z "$VIDEO_ID" ] || [ ${#VIDEO_ID} -ne 11 ]; then
        echo "Error: Could not extract video ID from URL: $URL"
        FAILURES=$((FAILURES + 1))
        continue
    fi

    echo "Fetching video info..."
    TITLE="$("$YT_DLP_BIN" --no-update --no-playlist "${JS_RUNTIME_ARGS[@]}" --get-title "$URL" 2>/dev/null || true)"
    if [ -z "$TITLE" ]; then
        TITLE="video_$VIDEO_ID"
    fi

    SAFE_NAME=$(echo "$TITLE" | tr -cd '[:alnum:] _-' | tr ' ' '_' | head -c 50)
    if [ -z "$SAFE_NAME" ]; then
        SAFE_NAME="video_$VIDEO_ID"
    fi

    BASE_NAME="${SAFE_NAME}_${VIDEO_ID}"
    TEMP_AUDIO_TEMPLATE="$TEMP_DIR/$BASE_NAME.%(ext)s"
    RESOLVED_CATEGORY="$CATEGORY"
    if [ -z "$RESOLVED_CATEGORY" ]; then
        RESOLVED_CATEGORY="$(infer_category_from_title "$TITLE")"
    fi

    DEST_DIR="$OUTPUT_DIR"
    if [ -n "$RESOLVED_CATEGORY" ]; then
        DEST_DIR="$OUTPUT_DIR/$RESOLVED_CATEGORY"
        echo "Category: $RESOLVED_CATEGORY"
    fi
    FINAL_TEXT="$DEST_DIR/$BASE_NAME.txt"

    mkdir -p "$TEMP_DIR"
    mkdir -p "$DEST_DIR"

    if [ -f "$FINAL_TEXT" ]; then
        echo "✓ Already transcribed: $FINAL_TEXT"
        echo "  Skipping download/transcription"
        SKIPPED=$((SKIPPED + 1))
        continue
    fi

    echo "Downloading audio..."
    if ! "$YT_DLP_BIN" --no-update --no-playlist "${JS_RUNTIME_ARGS[@]}" \
        -x --audio-format mp3 --audio-quality 0 \
        --output "$TEMP_AUDIO_TEMPLATE" \
        "$URL"; then
        echo "Error: Audio download failed for $URL"
        rm -rf "$TEMP_DIR"
        FAILURES=$((FAILURES + 1))
        continue
    fi

    TEMP_AUDIO="$(find "$TEMP_DIR" -maxdepth 1 -type f \( -name "$BASE_NAME.mp3" -o -name "$BASE_NAME.m4a" -o -name "$BASE_NAME.webm" -o -name "$BASE_NAME.opus" -o -name "$BASE_NAME.wav" \) | head -n 1)"
    if [ -z "${TEMP_AUDIO:-}" ] || [ ! -f "$TEMP_AUDIO" ]; then
        echo "Error: Downloaded audio file not found for $URL"
        rm -rf "$TEMP_DIR"
        FAILURES=$((FAILURES + 1))
        continue
    fi

    START_PARAM="$(extract_query_param "$URL" "t")"
    [ -z "$START_PARAM" ] && START_PARAM="$(extract_query_param "$URL" "start")"
    END_PARAM="$(extract_query_param "$URL" "end")"
    START_SECONDS="$(parse_time_to_seconds "$START_PARAM")"
    END_SECONDS="$(parse_time_to_seconds "$END_PARAM")"

    if [ -n "$START_SECONDS" ] || [ -n "$END_SECONDS" ]; then
        CLIPPED_AUDIO="$TEMP_DIR/${BASE_NAME}_clipped.mp3"
        echo "Applying URL time range..."
        if [ -n "$START_SECONDS" ]; then
            echo "  Start offset: ${START_SECONDS}s"
        fi
        if [ -n "$END_SECONDS" ]; then
            echo "  End offset: ${END_SECONDS}s"
        fi

        FFMPEG_ARGS=(-y)
        if [ -n "$START_SECONDS" ]; then
            FFMPEG_ARGS+=(-ss "$START_SECONDS")
        fi
        FFMPEG_ARGS+=(-i "$TEMP_AUDIO")
        if [ -n "$END_SECONDS" ] && [ -n "$START_SECONDS" ] && [ "$END_SECONDS" -gt "$START_SECONDS" ]; then
            FFMPEG_ARGS+=(-t "$((END_SECONDS - START_SECONDS))")
        elif [ -n "$END_SECONDS" ] && [ -z "$START_SECONDS" ]; then
            FFMPEG_ARGS+=(-t "$END_SECONDS")
        fi
        FFMPEG_ARGS+=(-vn -acodec libmp3lame -q:a 2 "$CLIPPED_AUDIO")

        if ! ffmpeg "${FFMPEG_ARGS[@]}" >/dev/null 2>&1; then
            echo "Error: Failed to clip audio according to URL timestamps"
            rm -rf "$TEMP_DIR"
            FAILURES=$((FAILURES + 1))
            continue
        fi

        TEMP_AUDIO="$CLIPPED_AUDIO"
    fi

    AUDIO_DURATION_RAW="$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$TEMP_AUDIO" 2>/dev/null || true)"
    AUDIO_DURATION_SECONDS="${AUDIO_DURATION_RAW%.*}"
    AUDIO_DURATION_SECONDS="${AUDIO_DURATION_SECONDS:-0}"
    SELECTED_MODEL="$(pick_model_for_duration "$AUDIO_DURATION_SECONDS" "$MODEL")"

    echo "Download complete. Transcribing..."
    echo "  Duration: ${AUDIO_DURATION_SECONDS}s"
    echo "  Model: $SELECTED_MODEL"
    echo "  Device: cuda"
    echo "  JS runtime: ${JS_RUNTIME:-none}"

    LANG_FLAG=""
    if [ -n "$LANGUAGE" ]; then
        LANG_FLAG="--language $LANGUAGE"
    fi

    PYTHONUNBUFFERED=1 run_whisper "$TEMP_AUDIO" \
        --model "$SELECTED_MODEL" \
        --device cuda \
        --output_format txt \
        --output_dir "$TEMP_DIR" \
        --verbose False \
        $LANG_FLAG \
        2>&1

    RAW_TEXT="${TEMP_AUDIO%.*}.txt"

    if [ ! -f "$RAW_TEXT" ]; then
        echo "Error: Transcription failed for $URL"
        rm -rf "$TEMP_DIR"
        FAILURES=$((FAILURES + 1))
        continue
    fi

    echo "URL: $URL" > "$FINAL_TEXT"
    echo "" >> "$FINAL_TEXT"
    echo "Title: $TITLE" >> "$FINAL_TEXT"
    echo "" >> "$FINAL_TEXT"
    cat "$RAW_TEXT" >> "$FINAL_TEXT"

    rm -f "$TEMP_AUDIO" "$RAW_TEXT" "${TEMP_AUDIO%.*}.json"
    find "$OUTPUT_DIR" -type f -name "*.mp4" -delete

    echo ""
    echo "✓ Saved: $FINAL_TEXT"
    echo "  Lines: $(wc -l < "$FINAL_TEXT")"
    echo ""
    SUCCESSES=$((SUCCESSES + 1))

done

# Clean up temp directory
rm -rf "$TEMP_DIR"

echo "========================================="
echo "Batch complete! All transcriptions in:"
echo "  $OUTPUT_DIR"
echo "========================================="
echo "Summary: successes=$SUCCESSES skipped=$SKIPPED failures=$FAILURES"
find "$OUTPUT_DIR" -type f -name "*.txt" -printf "%TY-%Tm-%Td %TH:%TM %p\n" 2>/dev/null | sort | tail -5

if [ "$FAILURES" -gt 0 ]; then
    exit 1
fi
