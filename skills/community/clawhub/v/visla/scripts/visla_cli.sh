#!/bin/bash
# Visla API CLI Wrapper (Bash version)
# Simple wrapper for creating videos from scripts or URLs.

set -e

BASE_URL="https://openapi.visla.us/openapi/v1"
VERSION="260501-1423"
USER_AGENT="visla-skill/${VERSION}"

ALLOWED_TEXT_EXTENSIONS="txt md srt vtt csv"

# Tips to display during video generation
VISLA_TIPS=(
    "Tip: Visla AI Director creates consistent characters and environments across scenes"
    "Tip: You can convert PDFs and PPTs directly into polished videos"
    "Tip: Visla offers 100+ AI avatars with voice cloning support"
    "Tip: Scene-based editing gives you precision control over individual shots"
    "Tip: Auto-transcription makes your videos accessible with subtitles"
    "Tip: Visla supports real-time collaborative editing with your team"
    "Tip: Full Getty Images library is available for enterprise users"
    "Tip: Multiple brand kits help maintain visual consistency"
    "Tip: Text-based video editing lets you edit by modifying the transcript"
    "Tip: Built-in teleprompter helps with professional recordings"
)

# Millisecond timestamp that works across macOS/Linux.
ms_now() {
    local ts
    ts="$(date +%s%3N 2>/dev/null || true)"
    if [[ "$ts" =~ ^[0-9]+$ ]]; then
        echo "$ts"
        return 0
    fi

    # macOS `date` often doesn't support `%3N`. Use Perl (available by default) as a fallback.
    if command -v perl >/dev/null 2>&1; then
        perl -MTime::HiRes=time -e 'printf("%.0f\n", time()*1000)'
        return 0
    fi

    echo -e "${RED}Error: Could not compute millisecond timestamp (need perl or a compatible date).${NC}"
    echo "Hint: Install perl, or use the Python CLI: python3 scripts/visla_cli.py <command>"
    exit 1
}

# Basic dependency checks. Keep help usable without requiring deps.
require_cmd() {
    local name="$1"
    command -v "$name" >/dev/null 2>&1 || {
        echo "VISLA_CLI_ERROR_CODE=missing_dependency"
        echo -e "${RED}Error: Missing dependency: ${name}${NC}"
        echo "Hint: Install it and retry, or use the Python CLI: python3 scripts/visla_cli.py <command>"
        exit 1
    }
}

preflight() {
    # Used by all non-help commands.
    require_cmd curl
    require_cmd openssl
    require_cmd uuidgen
}

preflight_needs_jq() {
    # Needed for script/url/doc payload encoding.
    require_cmd jq
}

classify_api_error_code() {
    local msg="$1"
    local m
    m=$(echo "$msg" | tr '[:upper:]' '[:lower:]')
    # Use specific phrases to avoid over-classification
    if echo "$m" | grep -qE "unauthorized|forbidden|invalid api key|invalid api secret|invalid key|invalid secret|invalid sign|sign error|signature error|signature invalid|invalid signature|authentication failed|auth failed"; then
        echo "auth_failed"
        return 0
    fi
    if echo "$m" | grep -qE "rate.*limit"; then
        echo "rate_limited"
        return 0
    fi
    if echo "$m" | grep -qE "credit|quota|insufficient|balance"; then
        echo "credits_exhausted"
        return 0
    fi
    echo "api_error"
}

validate_read_path() {
    local file="$1"
    case "$file" in
        *..*) 
            echo "VISLA_CLI_ERROR_CODE=path_traversal"
            echo -e "${RED}Error: Path traversal not allowed: $file${NC}"
            exit 1
            ;;
    esac
    local norm
    norm=$(cd "$(dirname "$file")" 2>/dev/null && pwd || echo "")
    case "$norm" in
        /etc/*|/proc/*|/sys/*|/dev/*|/run/*|/var/log/*)
            echo "VISLA_CLI_ERROR_CODE=access_denied"
            echo -e "${RED}Error: Access denied: system path $file${NC}"
            exit 1
            ;;
    esac
    case "$file" in
        /etc/*|/proc/*|/sys/*|/dev/*|/run/*|/var/log/*)
            echo "VISLA_CLI_ERROR_CODE=access_denied"
            echo -e "${RED}Error: Access denied: system path $file${NC}"
            exit 1
            ;;
    esac
}

validate_text_extension() {
    local file="$1"
    local ext="${file##*.}"
    ext=$(echo "$ext" | tr '[:upper:]' '[:lower:]')
    local allowed=0
    for e in $ALLOWED_TEXT_EXTENSIONS; do
        if [ "$ext" = "$e" ]; then
            allowed=1
            break
        fi
    done
    if [ "$allowed" -eq 0 ]; then
        echo "VISLA_CLI_ERROR_CODE=unsupported_format"
        echo -e "${RED}Error: File type not allowed: .$ext. Allowed: .txt .md .srt .vtt .csv${NC}"
        exit 1
    fi
}

# Check credentials
check_credentials() {
    if [ -z "$VISLA_API_KEY" ] || [ -z "$VISLA_API_SECRET" ]; then
        echo "VISLA_CLI_ERROR_CODE=missing_credentials"
        echo -e "${RED}Error: Visla credentials not configured${NC}"
        echo ""
        echo "Set environment variables:"
        echo "  export VISLA_API_KEY=\"your_key\""
        echo "  export VISLA_API_SECRET=\"your_secret\""
        echo ""
        echo "Get your API credentials from:"
        echo -e "  ${YELLOW}https://www.visla.us/visla-api${NC}"
        exit 1
    fi
}

# Colors for output (disable when not running in a TTY to keep logs clean)
if [ -t 1 ]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    NC='\033[0m' # No Color
else
    RED=''
    GREEN=''
    YELLOW=''
    NC=''
fi

# Help function
show_help() {
    cat << EOF
Visla Skill v${VERSION}

Visla API CLI Wrapper

Usage: $(basename "$0") <command> [args]

Commands:
    script <text|@file>     Create video from script
    url <URL>               Create video from web page URL
    doc <file>              Create video from document (PPT/PDF)
    idea <text|@file>       Create video from idea
    visual <file>           Create video from visual resources (images/videos)
    speech <file>           Create video from speech (audio/video file)
    account                 Show account info and credit balance
    avatar                  List available AI avatars
    voice                   List available AI voices

Options for script, url, doc:
    -c, --config <file>     Path to JSON config file with video options
    --avatar <id>           Avatar ID (overrides config)
    --voice <id>            Voice ID (overrides config)

Environment:
    VISLA_API_KEY             API key (from https://www.visla.us/visla-api)
    VISLA_API_SECRET          API secret

Config File Format (JSON):
    {
        "video_title": "My Video",
        "video_description": "Video description",
        "script_text_mode": "ai_rewrite",
        "doc_usage": "page_by_page_walkthrough",
        "speaker_notes_verbatim": false,
        "target_video": {
            "aspect_ratio": "16:9",
            "video_pace": "fast",
            "burn_subtitles": false,
            "video_duration_in_seconds": 60
        },
        "avatar_options": {
            "use_avatar": false,
            "look_id": 12345,
            "avatar_layout": "smart_composition",
            "enable_auto_wallpaper": true,
            "enable_in_preview": true
        },
        "voice_options": {
            "use_voice": false,
            "voice_id": 1
        },
        "footage_options": {
            "enable_footage": true,
            "use_free_stocks": true,
            "use_premium_stocks": true,
            "use_premium_stocks_getty": true,
            "use_private_stocks": true,
            "private_stock_ids": 123456
        },
        "bgm_options": {
            "enable_bgm": true,
            "use_free_stocks": true,
            "use_premium_stocks": true
        }
    }

Examples:
    # Create from script
    $(basename "$0") script "Scene 1: Sunset. Narrator: Welcome."

    # Create from file
    $(basename "$0") script @myscript.txt

    # Create from URL
    $(basename "$0") url "https://blog.example.com/article"

    # Create from document
    $(basename "$0") doc presentation.pptx

    # With config file
    $(basename "$0") script "Scene 1: Hello" -c config.json

    # With avatar and voice (overrides config)
    $(basename "$0") script "Scene 1: Hello" --avatar avatar_123 --voice voice_456

    # List available avatars and voices
    $(basename "$0") avatar
    $(basename "$0") voice

EOF
}

# Load config file and set variables
load_config() {
    local config_file="$1"
    if [ -z "$config_file" ] || [ ! -f "$config_file" ]; then
        return 1
    fi
    validate_read_path "$config_file"
    
    if ! command -v jq >/dev/null 2>&1; then
        echo -e "${RED}Error: jq required for config file parsing${NC}"
        return 1
    fi
    
    # Store config file path
    CONFIG_FILE="$config_file"
    
    # Read root level values
    video_title=$(jq -r '.video_title // ""' "$config_file" 2>/dev/null)
    video_description=$(jq -r '.video_description // ""' "$config_file" 2>/dev/null)
    script_text_mode=$(jq -r '.script_text_mode // "ai_rewrite"' "$config_file" 2>/dev/null)
    doc_usage=$(jq -r '.doc_usage // "page_by_page_walkthrough"' "$config_file" 2>/dev/null)
    speaker_notes_verbatim=$(jq -r '.speaker_notes_verbatim // false' "$config_file" 2>/dev/null)
    
    # Read target_video
    ratio=$(jq -r '.target_video.aspect_ratio // "16:9"' "$config_file" 2>/dev/null)
    pace=$(jq -r '.target_video.video_pace // "fast"' "$config_file" 2>/dev/null)
    burn_subtitles=$(jq -r '.target_video.burn_subtitles // false' "$config_file" 2>/dev/null)
    video_duration_in_seconds=$(jq -r '.target_video.video_duration_in_seconds // ""' "$config_file" 2>/dev/null)
    
    # Read avatar_options
    avatar_use_avatar=$(jq -r '.avatar_options.use_avatar | if . == null then "" else . end' "$config_file" 2>/dev/null)
    avatar_look_id=$(jq -r '.avatar_options.look_id // ""' "$config_file" 2>/dev/null)
    avatar_avatar_layout=$(jq -r '.avatar_options.avatar_layout // ""' "$config_file" 2>/dev/null)
    avatar_enable_auto_wallpaper=$(jq -r '.avatar_options.enable_auto_wallpaper | if . == null then "" else . end' "$config_file" 2>/dev/null)
    avatar_enable_in_preview=$(jq -r '.avatar_options.enable_in_preview | if . == null then "" else . end' "$config_file" 2>/dev/null)
    
    # Read voice_options
    voice_use_voice=$(jq -r '.voice_options.use_voice | if . == null then "" else . end' "$config_file" 2>/dev/null)
    voice_voice_id=$(jq -r '.voice_options.voice_id // ""' "$config_file" 2>/dev/null)
    
    # Read footage_options
    footage_enable_footage=$(jq -r '.footage_options.enable_footage | if . == null then "" else . end' "$config_file" 2>/dev/null)
    use_free_stocks=$(jq -r '.footage_options.use_free_stocks // true' "$config_file" 2>/dev/null)
    use_premium_stocks=$(jq -r '.footage_options.use_premium_stocks // false' "$config_file" 2>/dev/null)
    use_premium_stocks_getty=$(jq -r '.footage_options.use_premium_stocks_getty // false' "$config_file" 2>/dev/null)
    use_private_stocks=$(jq -r '.footage_options.use_private_stocks // false' "$config_file" 2>/dev/null)
    footage_private_stock_ids=$(jq -r '.footage_options.private_stock_ids // ""' "$config_file" 2>/dev/null)
    
    # Read bgm_options
    bgm_enable_bgm=$(jq -r '.bgm_options.enable_bgm | if . == null then "" else . end' "$config_file" 2>/dev/null)
    bgm_use_free_stocks=$(jq -r '.bgm_options.use_free_stocks // true' "$config_file" 2>/dev/null)
    bgm_use_premium_stocks=$(jq -r '.bgm_options.use_premium_stocks // false' "$config_file" 2>/dev/null)
    
    return 0
}

# Generate signature and make request
visla_request() {
    local method=$1
    local endpoint=$2
    local data=$3

    local full_url="${BASE_URL}${endpoint}"
    # Extract base URL without query params for signing
    local base_url="${full_url%%\?*}"
    local ts=$(ms_now)
    local nonce=$(uuidgen)
    local sign_str="${method}|${base_url}|${ts}|${nonce}"
    local sign=$(echo -n "$sign_str" | openssl dgst -sha256 -hmac "$VISLA_API_SECRET" | awk '{print $2}')

    local result=""
    local curl_exit=0
    if [ "$method" = "GET" ]; then
        result=$(curl -sS -X GET "$full_url" \
            -H "Content-Type: application/json; charset=utf-8" \
            -H "User-Agent: $USER_AGENT" \
            -H "key: $VISLA_API_KEY" \
            -H "ts: $ts" \
            -H "nonce: $nonce" \
            -H "sign: $sign" ${data:+-d "$data"} 2>&1) || curl_exit=$?
    else
        result=$(curl -sS -X POST "$full_url" \
            -H "Content-Type: application/json; charset=utf-8" \
            -H "User-Agent: $USER_AGENT" \
            -H "key: $VISLA_API_KEY" \
            -H "ts: $ts" \
            -H "nonce: $nonce" \
            -H "sign: $sign" \
            -d "$data" 2>&1) || curl_exit=$?
    fi

    if [ "$curl_exit" -ne 0 ]; then
        # Use fixed message to avoid JSON escaping issues with raw curl output
        echo "{\"code\":-1,\"msg\":\"Network error (curl exit $curl_exit)\",\"data\":{}}"
        return 0
    fi
    echo "$result"
}

# Extract JSON value
jq_get() {
    local json=$1
    local key=$2
    # Prefer jq (already required for the main workflows). Fallback to a naive parser.
    if command -v jq >/dev/null 2>&1; then
        echo "$json" | jq -r --arg k "$key" '.data[$k] // .[$k] // empty' 2>/dev/null || true
        return 0
    fi
    echo "$json" | grep -o "\"$key\":\"[^\"]*\"" | cut -d'"' -f4
}

# Create from script
cmd_script() {
    local script="$1"

    # Read from file if starts with @
    if [[ "$script" == @* ]]; then
        local file="${script:1}"
        validate_read_path "$file"
        validate_text_extension "$file"
        if [ ! -f "$file" ]; then
            echo "VISLA_CLI_ERROR_CODE=file_not_found"
            echo -e "${RED}Error: File not found: $file${NC}"
            exit 1
        fi
        script=$(cat "$file")
    fi

    echo "Creating video from script..."
    echo ""
    echo "$script"
    echo ""

    # Build target_video JSON
    local target_video="{\"aspect_ratio\": \"$ratio\", \"video_pace\": \"$pace\", \"burn_subtitles\": $burn_subtitles}"
    if [ -n "$video_duration_in_seconds" ]; then
        target_video=$(echo "$target_video" | jq ". + {\"video_duration_in_seconds\": $video_duration_in_seconds}")
    fi

    # Build avatar_options JSON
    local avatar_options="{}"
    # CLI arg --avatar should enable avatar and set look_id
    if [ -n "$avatar" ]; then
        avatar_options=$(echo "$avatar_options" | jq ". + {\"use_avatar\": true, \"look_id\": \"$avatar\"}")
    else
        if [ -n "$avatar_use_avatar" ]; then
            avatar_options=$(echo "$avatar_options" | jq ". + {\"use_avatar\": $avatar_use_avatar}")
        fi
        if [ -n "$avatar_look_id" ]; then
            avatar_options=$(echo "$avatar_options" | jq ". + {\"look_id\": \"$avatar_look_id\"}")
        fi
    fi
    if [ -n "$avatar_avatar_layout" ]; then
        avatar_options=$(echo "$avatar_options" | jq ". + {\"avatar_layout\": \"$avatar_avatar_layout\"}")
    fi
    if [ -n "$avatar_enable_auto_wallpaper" ]; then
        avatar_options=$(echo "$avatar_options" | jq ". + {\"enable_auto_wallpaper\": $avatar_enable_auto_wallpaper}")
    fi
    if [ -n "$avatar_enable_in_preview" ]; then
        avatar_options=$(echo "$avatar_options" | jq ". + {\"enable_in_preview\": $avatar_enable_in_preview}")
    fi

    # Build voice_options JSON
    local voice_options="{}"
    # CLI arg --voice should enable voice and set voice_id
    if [ -n "$voice" ]; then
        voice_options=$(echo "$voice_options" | jq ". + {\"use_voice\": true, \"voice_id\": \"$voice\"}")
    else
        if [ -n "$voice_use_voice" ]; then
            voice_options=$(echo "$voice_options" | jq ". + {\"use_voice\": $voice_use_voice}")
        fi
        if [ -n "$voice_voice_id" ]; then
            voice_options=$(echo "$voice_options" | jq ". + {\"voice_id\": \"$voice_voice_id\"}")
        fi
    fi

    # Build footage_options JSON
    local footage_options="{\"use_free_stocks\": $use_free_stocks, \"use_premium_stocks\": $use_premium_stocks, \"use_premium_stocks_getty\": $use_premium_stocks_getty, \"use_private_stocks\": $use_private_stocks}"
    if [ -n "$footage_enable_footage" ]; then
        footage_options=$(echo "$footage_options" | jq ". + {\"enable_footage\": $footage_enable_footage}")
    fi
    if [ -n "$footage_private_stock_ids" ]; then
        footage_options=$(echo "$footage_options" | jq ". + {\"private_stock_ids\": $footage_private_stock_ids}")
    fi
    
    # Build bgm_options JSON
    local bgm_options="{\"use_free_stocks\": $bgm_use_free_stocks, \"use_premium_stocks\": $bgm_use_premium_stocks}"
    if [ -n "$bgm_enable_bgm" ]; then
        bgm_options=$(echo "$bgm_options" | jq ". + {\"enable_bgm\": $bgm_enable_bgm}")
    fi

    # Build payload
    local payload="{\"script\": $(echo "$script" | jq -Rs .), \"script_text_mode\": \"$script_text_mode\""
    
    if [ -n "$video_title" ]; then
        payload="$payload, \"video_title\": $(echo "$video_title" | jq -Rs .)"
    fi
    if [ -n "$video_description" ]; then
        payload="$payload, \"video_description\": $(echo "$video_description" | jq -Rs .)"
    fi
    payload="$payload, \"target_video\": $target_video"
    
    if [ "$avatar_options" != "{}" ]; then
        payload="$payload, \"avatar_options\": $avatar_options"
    fi
    if [ "$voice_options" != "{}" ]; then
        payload="$payload, \"voice_options\": $voice_options"
    fi
    payload="$payload, \"footage_options\": $footage_options, \"bgm_options\": $bgm_options"
    payload="$payload}"

    local result=$(visla_request "POST" "/project/script-to-video" "$payload")

    local project_uuid=$(jq_get "$result" "projectUuid")
    local share_link=$(jq_get "$result" "shareLink")

    if [ -n "$project_uuid" ]; then
        echo "Project created: $project_uuid"
        [ -n "$share_link" ] && echo "View link: $share_link"
        wait_and_export "$project_uuid"
    else
        local code
        code=$(echo "$result" | jq -r '.code // empty' 2>/dev/null || true)
        if [ "$code" != "0" ] && [ -n "$code" ]; then
            local msg
            msg=$(echo "$result" | jq -r '.msg // .message // "Unknown error"' 2>/dev/null || echo "Unknown error")
            echo "VISLA_CLI_ERROR_CODE=$(classify_api_error_code "$msg")"
            echo -e "${RED}Error: ${msg}${NC}"
        else
            echo "VISLA_CLI_ERROR_CODE=api_error"
            echo -e "${RED}Error: Failed to create project${NC}"
            echo "$result"
        fi
        exit 1
    fi
}

# Create from URL
cmd_url() {
    local url="$1"

    # Validate URL first
    echo "Validating URL: $url"
    local http_code
    http_code=$(curl -s -o /dev/null -w "%{http_code}" -L --head "$url" --connect-timeout 10 --max-time 20) || {
        echo "VISLA_CLI_ERROR_CODE=network_error"
        echo -e "${RED}Error: Network error validating URL: $url${NC}"
        exit 1
    }
    # Some sites block HEAD requests, retry with lightweight GET
    if [ "$http_code" = "403" ] || [ "$http_code" = "405" ]; then
        http_code=$(curl -s -o /dev/null -w "%{http_code}" -L -H "Range: bytes=0-0" "$url" --connect-timeout 10 --max-time 20) || {
            echo "VISLA_CLI_ERROR_CODE=network_error"
            echo -e "${RED}Error: Network error validating URL: $url${NC}"
            exit 1
        }
    fi
    if [ "$http_code" -ge 400 ] || [ "$http_code" = "000" ]; then
        echo "VISLA_CLI_ERROR_CODE=invalid_url"
        echo -e "${RED}Error: URL is not accessible (HTTP $http_code): $url${NC}"
        exit 1
    fi
    echo "URL validated successfully"
    echo ""

    echo "Creating video from URL..."

    # Build target_video JSON
    local target_video="{\"aspect_ratio\": \"$ratio\", \"video_pace\": \"$pace\", \"burn_subtitles\": $burn_subtitles}"
    if [ -n "$video_duration_in_seconds" ]; then
        target_video=$(echo "$target_video" | jq ". + {\"video_duration_in_seconds\": $video_duration_in_seconds}")
    fi

    # Build avatar_options JSON
    local avatar_options="{}"
    # CLI arg --avatar should enable avatar and set look_id
    if [ -n "$avatar" ]; then
        avatar_options=$(echo "$avatar_options" | jq ". + {\"use_avatar\": true, \"look_id\": \"$avatar\"}")
    else
        if [ -n "$avatar_use_avatar" ]; then
            avatar_options=$(echo "$avatar_options" | jq ". + {\"use_avatar\": $avatar_use_avatar}")
        fi
        if [ -n "$avatar_look_id" ]; then
            avatar_options=$(echo "$avatar_options" | jq ". + {\"look_id\": \"$avatar_look_id\"}")
        fi
    fi
    if [ -n "$avatar_avatar_layout" ]; then
        avatar_options=$(echo "$avatar_options" | jq ". + {\"avatar_layout\": \"$avatar_avatar_layout\"}")
    fi
    if [ -n "$avatar_enable_auto_wallpaper" ]; then
        avatar_options=$(echo "$avatar_options" | jq ". + {\"enable_auto_wallpaper\": $avatar_enable_auto_wallpaper}")
    fi
    if [ -n "$avatar_enable_in_preview" ]; then
        avatar_options=$(echo "$avatar_options" | jq ". + {\"enable_in_preview\": $avatar_enable_in_preview}")
    fi

    # Build voice_options JSON
    local voice_options="{}"
    # CLI arg --voice should enable voice and set voice_id
    if [ -n "$voice" ]; then
        voice_options=$(echo "$voice_options" | jq ". + {\"use_voice\": true, \"voice_id\": \"$voice\"}")
    else
        if [ -n "$voice_use_voice" ]; then
            voice_options=$(echo "$voice_options" | jq ". + {\"use_voice\": $voice_use_voice}")
        fi
        if [ -n "$voice_voice_id" ]; then
            voice_options=$(echo "$voice_options" | jq ". + {\"voice_id\": \"$voice_voice_id\"}")
        fi
    fi

    # Build footage_options JSON
    local footage_options="{\"use_free_stocks\": $use_free_stocks, \"use_premium_stocks\": $use_premium_stocks, \"use_premium_stocks_getty\": $use_premium_stocks_getty, \"use_private_stocks\": $use_private_stocks}"
    if [ -n "$footage_enable_footage" ]; then
        footage_options=$(echo "$footage_options" | jq ". + {\"enable_footage\": $footage_enable_footage}")
    fi
    if [ -n "$footage_private_stock_ids" ]; then
        footage_options=$(echo "$footage_options" | jq ". + {\"private_stock_ids\": $footage_private_stock_ids}")
    fi
    
    # Build bgm_options JSON
    local bgm_options="{\"use_free_stocks\": $bgm_use_free_stocks, \"use_premium_stocks\": $bgm_use_premium_stocks}"
    if [ -n "$bgm_enable_bgm" ]; then
        bgm_options=$(echo "$bgm_options" | jq ". + {\"enable_bgm\": $bgm_enable_bgm}")
    fi

    # Build payload
    local payload="{\"url\": $(echo "$url" | jq -Rs .)"
    
    if [ -n "$video_title" ]; then
        payload="$payload, \"video_title\": $(echo "$video_title" | jq -Rs .)"
    fi
    if [ -n "$video_description" ]; then
        payload="$payload, \"video_description\": $(echo "$video_description" | jq -Rs .)"
    fi
    payload="$payload, \"target_video\": $target_video"
    
    if [ "$avatar_options" != "{}" ]; then
        payload="$payload, \"avatar_options\": $avatar_options"
    fi
    if [ "$voice_options" != "{}" ]; then
        payload="$payload, \"voice_options\": $voice_options"
    fi
    payload="$payload, \"footage_options\": $footage_options, \"bgm_options\": $bgm_options"
    payload="$payload}"

    local result=$(visla_request "POST" "/project/create-video-by-url" "$payload")

    local project_uuid=$(jq_get "$result" "projectUuid")
    local share_link=$(jq_get "$result" "shareLink")

    if [ -n "$project_uuid" ]; then
        echo "Project created: $project_uuid"
        [ -n "$share_link" ] && echo "View link: $share_link"
        wait_and_export "$project_uuid"
    else
        local code
        code=$(echo "$result" | jq -r '.code // empty' 2>/dev/null || true)
        if [ "$code" != "0" ] && [ -n "$code" ]; then
            local msg
            msg=$(echo "$result" | jq -r '.msg // .message // "Unknown error"' 2>/dev/null || echo "Unknown error")
            echo "VISLA_CLI_ERROR_CODE=$(classify_api_error_code "$msg")"
            echo -e "${RED}Error: ${msg}${NC}"
        else
            echo "VISLA_CLI_ERROR_CODE=api_error"
            echo -e "${RED}Error: Failed to create project${NC}"
            echo "$result"
        fi
        exit 1
    fi
}

# Create from document
cmd_doc() {
    local file="$1"

    validate_read_path "$file"

    if [ ! -f "$file" ]; then
        echo "VISLA_CLI_ERROR_CODE=file_not_found"
        echo -e "${RED}Error: File not found: $file${NC}"
        exit 1
    fi

    local filename=$(basename "$file")
    local suffix="${filename##*.}"
    suffix=$(echo "$suffix" | tr '[:upper:]' '[:lower:]')

    # Determine media type
    local media_type=""
    case "$suffix" in
        pptx|ppt) media_type="ppt" ;;
        pdf) media_type="pdf" ;;
        *)
            echo "VISLA_CLI_ERROR_CODE=unsupported_format"
            echo -e "${RED}Error: Unsupported file type: $suffix${NC}"
            echo "Supported formats: pptx, ppt, pdf"
            exit 1
            ;;
    esac

    echo "Uploading document: $filename"

    # Step 1: Get upload URL
    local upload_result=$(visla_request "GET" "/project/get-asset-upload-url?mediaType=$media_type&suffix=$suffix")
    local upload_url=$(jq_get "$upload_result" "uploadUrl")

    if [ -z "$upload_url" ]; then
        echo "VISLA_CLI_ERROR_CODE=api_error"
        echo -e "${RED}Error: Failed to get upload URL${NC}"
        echo "$upload_result"
        exit 1
    fi
    echo "Upload URL obtained"

    # Step 2: Upload to S3
    local content_type="application/octet-stream"
    case "$suffix" in
        pptx) content_type="application/vnd.openxmlformats-officedocument.presentationml.presentation" ;;
        ppt) content_type="application/vnd.ms-powerpoint" ;;
        pdf) content_type="application/pdf" ;;
    esac

    local upload_response
    upload_response=$(curl -s -w "%{http_code}" -X PUT "$upload_url" \
        -H "Content-Type: $content_type" \
        -H "User-Agent: $USER_AGENT" \
        --data-binary "@$file") || {
        echo "VISLA_CLI_ERROR_CODE=network_error"
        echo -e "${RED}Error: Network error uploading file${NC}"
        exit 1
    }
    local http_code="${upload_response: -3}"

    if [ "$http_code" != "200" ] && [ "$http_code" != "201" ]; then
        echo -e "${RED}Error: Failed to upload file (HTTP $http_code)${NC}"
        exit 1
    fi
    echo "File uploaded successfully"
    echo ""

    # Step 3: Create video from document
    echo "Creating video from document..."

    # Build target_video JSON
    local target_video="{\"aspect_ratio\": \"$ratio\", \"video_pace\": \"$pace\", \"burn_subtitles\": $burn_subtitles}"
    if [ -n "$video_duration_in_seconds" ]; then
        target_video=$(echo "$target_video" | jq ". + {\"video_duration_in_seconds\": $video_duration_in_seconds}")
    fi

    # Build avatar_options JSON
    local avatar_options="{}"
    # CLI arg --avatar should enable avatar and set look_id
    if [ -n "$avatar" ]; then
        avatar_options=$(echo "$avatar_options" | jq ". + {\"use_avatar\": true, \"look_id\": \"$avatar\"}")
    else
        if [ -n "$avatar_use_avatar" ]; then
            avatar_options=$(echo "$avatar_options" | jq ". + {\"use_avatar\": $avatar_use_avatar}")
        fi
        if [ -n "$avatar_look_id" ]; then
            avatar_options=$(echo "$avatar_options" | jq ". + {\"look_id\": \"$avatar_look_id\"}")
        fi
    fi
    if [ -n "$avatar_avatar_layout" ]; then
        avatar_options=$(echo "$avatar_options" | jq ". + {\"avatar_layout\": \"$avatar_avatar_layout\"}")
    fi
    if [ -n "$avatar_enable_auto_wallpaper" ]; then
        avatar_options=$(echo "$avatar_options" | jq ". + {\"enable_auto_wallpaper\": $avatar_enable_auto_wallpaper}")
    fi
    if [ -n "$avatar_enable_in_preview" ]; then
        avatar_options=$(echo "$avatar_options" | jq ". + {\"enable_in_preview\": $avatar_enable_in_preview}")
    fi

    # Build voice_options JSON
    local voice_options="{}"
    # CLI arg --voice should enable voice and set voice_id
    if [ -n "$voice" ]; then
        voice_options=$(echo "$voice_options" | jq ". + {\"use_voice\": true, \"voice_id\": \"$voice\"}")
    else
        if [ -n "$voice_use_voice" ]; then
            voice_options=$(echo "$voice_options" | jq ". + {\"use_voice\": $voice_use_voice}")
        fi
        if [ -n "$voice_voice_id" ]; then
            voice_options=$(echo "$voice_options" | jq ". + {\"voice_id\": \"$voice_voice_id\"}")
        fi
    fi

    # Build footage_options JSON
    local footage_options="{\"use_free_stocks\": $use_free_stocks, \"use_premium_stocks\": $use_premium_stocks, \"use_premium_stocks_getty\": $use_premium_stocks_getty, \"use_private_stocks\": $use_private_stocks}"
    if [ -n "$footage_enable_footage" ]; then
        footage_options=$(echo "$footage_options" | jq ". + {\"enable_footage\": $footage_enable_footage}")
    fi
    if [ -n "$footage_private_stock_ids" ]; then
        footage_options=$(echo "$footage_options" | jq ". + {\"private_stock_ids\": $footage_private_stock_ids}")
    fi

    # Build bgm_options JSON
    local bgm_options="{\"use_free_stocks\": $bgm_use_free_stocks, \"use_premium_stocks\": $bgm_use_premium_stocks}"
    if [ -n "$bgm_enable_bgm" ]; then
        bgm_options=$(echo "$bgm_options" | jq ". + {\"enable_bgm\": $bgm_enable_bgm}")
    fi

    # Build payload
    local payload="{\"doc_asset_url\": $(echo "$upload_url" | jq -Rs .), \"doc_file_name\": $(echo "$filename" | jq -Rs .), \"doc_usage\": \"$doc_usage\", \"speaker_notes_verbatim\": $speaker_notes_verbatim"
    
    if [ -n "$video_title" ]; then
        payload="$payload, \"video_title\": $(echo "$video_title" | jq -Rs .)"
    fi
    if [ -n "$video_description" ]; then
        payload="$payload, \"video_description\": $(echo "$video_description" | jq -Rs .)"
    fi
    payload="$payload, \"target_video\": $target_video"
    
    if [ "$avatar_options" != "{}" ]; then
        payload="$payload, \"avatar_options\": $avatar_options"
    fi
    if [ "$voice_options" != "{}" ]; then
        payload="$payload, \"voice_options\": $voice_options"
    fi
    payload="$payload, \"footage_options\": $footage_options, \"bgm_options\": $bgm_options"
    payload="$payload}"

    local result=$(visla_request "POST" "/project/doc-to-video" "$payload")

    local project_uuid=$(jq_get "$result" "projectUuid")
    local share_link=$(jq_get "$result" "shareLink")

    if [ -n "$project_uuid" ]; then
        echo "Project created: $project_uuid"
        [ -n "$share_link" ] && echo "View link: $share_link"
        wait_and_export "$project_uuid"
    else
        local code
        code=$(echo "$result" | jq -r '.code // empty' 2>/dev/null || true)
        if [ "$code" != "0" ] && [ -n "$code" ]; then
            local msg
            msg=$(echo "$result" | jq -r '.msg // .message // "Unknown error"' 2>/dev/null || echo "Unknown error")
            echo "VISLA_CLI_ERROR_CODE=$(classify_api_error_code "$msg")"
            echo -e "${RED}Error: ${msg}${NC}"
        else
            echo "VISLA_CLI_ERROR_CODE=api_error"
            echo -e "${RED}Error: Failed to create project${NC}"
            echo "$result"
        fi
        exit 1
    fi
}

# Create from idea
cmd_idea() {
    local idea="$1"

    # Read from file if starts with @
    if [[ "$idea" == @* ]]; then
        local file="${idea:1}"
        validate_read_path "$file"
        validate_text_extension "$file"
        if [ ! -f "$file" ]; then
            echo "VISLA_CLI_ERROR_CODE=file_not_found"
            echo -e "${RED}Error: File not found: $file${NC}"
            exit 1
        fi
        idea=$(cat "$file")
    fi

    echo "Creating video from idea..."
    echo ""
    echo "$idea"
    echo ""

    # Build target_video JSON
    local target_video="{\"aspect_ratio\": \"$ratio\", \"video_pace\": \"$pace\", \"burn_subtitles\": $burn_subtitles}"
    if [ -n "$video_duration_in_seconds" ]; then
        target_video=$(echo "$target_video" | jq ". + {\"video_duration_in_seconds\": $video_duration_in_seconds}")
    fi

    # Build avatar_options JSON
    local avatar_options="{}"
    if [ -n "$avatar" ]; then
        avatar_options=$(echo "$avatar_options" | jq ". + {\"use_avatar\": true, \"look_id\": \"$avatar\"}")
    else
        if [ -n "$avatar_use_avatar" ]; then
            avatar_options=$(echo "$avatar_options" | jq ". + {\"use_avatar\": $avatar_use_avatar}")
        fi
        if [ -n "$avatar_look_id" ]; then
            avatar_options=$(echo "$avatar_options" | jq ". + {\"look_id\": \"$avatar_look_id\"}")
        fi
    fi
    if [ -n "$avatar_avatar_layout" ]; then
        avatar_options=$(echo "$avatar_options" | jq ". + {\"avatar_layout\": \"$avatar_avatar_layout\"}")
    fi
    if [ -n "$avatar_enable_auto_wallpaper" ]; then
        avatar_options=$(echo "$avatar_options" | jq ". + {\"enable_auto_wallpaper\": $avatar_enable_auto_wallpaper}")
    fi
    if [ -n "$avatar_enable_in_preview" ]; then
        avatar_options=$(echo "$avatar_options" | jq ". + {\"enable_in_preview\": $avatar_enable_in_preview}")
    fi

    # Build voice_options JSON
    local voice_options="{}"
    if [ -n "$voice" ]; then
        voice_options=$(echo "$voice_options" | jq ". + {\"use_voice\": true, \"voice_id\": \"$voice\"}")
    else
        if [ -n "$voice_use_voice" ]; then
            voice_options=$(echo "$voice_options" | jq ". + {\"use_voice\": $voice_use_voice}")
        fi
        if [ -n "$voice_voice_id" ]; then
            voice_options=$(echo "$voice_options" | jq ". + {\"voice_id\": \"$voice_voice_id\"}")
        fi
    fi

    # Build footage_options JSON
    local footage_options="{\"use_free_stocks\": $use_free_stocks, \"use_premium_stocks\": $use_premium_stocks, \"use_premium_stocks_getty\": $use_premium_stocks_getty, \"use_private_stocks\": $use_private_stocks}"
    if [ -n "$footage_enable_footage" ]; then
        footage_options=$(echo "$footage_options" | jq ". + {\"enable_footage\": $footage_enable_footage}")
    fi
    if [ -n "$footage_private_stock_ids" ]; then
        footage_options=$(echo "$footage_options" | jq ". + {\"private_stock_ids\": $footage_private_stock_ids}")
    fi
    
    # Build bgm_options JSON
    local bgm_options="{\"use_free_stocks\": $bgm_use_free_stocks, \"use_premium_stocks\": $bgm_use_premium_stocks}"
    if [ -n "$bgm_enable_bgm" ]; then
        bgm_options=$(echo "$bgm_options" | jq ". + {\"enable_bgm\": $bgm_enable_bgm}")
    fi

    # Build payload — API may not recognize "idea"; always set video_description as primary content carrier
    local payload="{\"idea\": $(echo "$idea" | jq -Rs .)"

    if [ -n "$video_title" ]; then
        payload="$payload, \"video_title\": $(echo "$video_title" | jq -Rs .)"
    fi
    if [ -n "$video_description" ]; then
        payload="$payload, \"video_description\": $(echo "$video_description" | jq -Rs .)"
    else
        # Ensure idea content reaches the API via a documented field
        local idea_desc="$idea"
        if [ ${#idea_desc} -gt 500 ]; then
            idea_desc="${idea_desc:0:500}"
        fi
        payload="$payload, \"video_description\": $(echo "$idea_desc" | jq -Rs .)"
    fi
    payload="$payload, \"target_video\": $target_video"

    if [ "$avatar_options" != "{}" ]; then
        payload="$payload, \"avatar_options\": $avatar_options"
    fi
    if [ "$voice_options" != "{}" ]; then
        payload="$payload, \"voice_options\": $voice_options"
    fi
    payload="$payload, \"footage_options\": $footage_options, \"bgm_options\": $bgm_options"
    payload="$payload}"

    local result=$(visla_request "POST" "/project/idea-to-video" "$payload")

    local project_uuid=$(jq_get "$result" "projectUuid")
    local share_link=$(jq_get "$result" "shareLink")

    if [ -n "$project_uuid" ]; then
        echo "Project created: $project_uuid"
        [ -n "$share_link" ] && echo "View link: $share_link"
        wait_and_export "$project_uuid"
    else
        local code
        code=$(echo "$result" | jq -r '.code // empty' 2>/dev/null || true)
        if [ "$code" != "0" ] && [ -n "$code" ]; then
            local msg
            msg=$(echo "$result" | jq -r '.msg // .message // "Unknown error"' 2>/dev/null || echo "Unknown error")
            echo "VISLA_CLI_ERROR_CODE=$(classify_api_error_code "$msg")"
            echo -e "${RED}Error: ${msg}${NC}"
        else
            echo "VISLA_CLI_ERROR_CODE=api_error"
            echo -e "${RED}Error: Failed to create project${NC}"
            echo "$result"
        fi
        exit 1
    fi
}

# Upload a single file and return upload URL; sets UPLOAD_URL or exits on error
upload_media_file() {
    local file="$1"
    local media_type="$2"
    local suffix="$3"

    local upload_result=$(visla_request "GET" "/project/get-asset-upload-url?mediaType=$media_type&suffix=$suffix")
    UPLOAD_URL=$(jq_get "$upload_result" "uploadUrl")

    if [ -z "$UPLOAD_URL" ]; then
        echo "VISLA_CLI_ERROR_CODE=api_error"
        echo -e "${RED}Error: Failed to get upload URL${NC}"
        echo "$upload_result"
        exit 1
    fi
    echo "Upload URL obtained"

    local content_type="application/octet-stream"
    case "$suffix" in
        jpg|jpeg) content_type="image/jpeg" ;;
        png) content_type="image/png" ;;
        gif) content_type="image/gif" ;;
        webp) content_type="image/webp" ;;
        mp4) content_type="video/mp4" ;;
        mov) content_type="video/quicktime" ;;
        avi) content_type="video/x-msvideo" ;;
        mkv) content_type="video/x-matroska" ;;
        mp3) content_type="audio/mpeg" ;;
        wav) content_type="audio/wav" ;;
        m4a) content_type="audio/mp4" ;;
        aac) content_type="audio/aac" ;;
        flac) content_type="audio/flac" ;;
        pptx) content_type="application/vnd.openxmlformats-officedocument.presentationml.presentation" ;;
        ppt) content_type="application/vnd.ms-powerpoint" ;;
        pdf) content_type="application/pdf" ;;
    esac

    local upload_response
    upload_response=$(curl -s -w "%{http_code}" -X PUT "$UPLOAD_URL" \
        -H "Content-Type: $content_type" \
        -H "User-Agent: $USER_AGENT" \
        --data-binary "@$file") || {
        echo "VISLA_CLI_ERROR_CODE=network_error"
        echo -e "${RED}Error: Network error uploading file${NC}"
        exit 1
    }
    local http_code="${upload_response: -3}"

    if [ "$http_code" != "200" ] && [ "$http_code" != "201" ]; then
        echo -e "${RED}Error: Failed to upload file (HTTP $http_code)${NC}"
        exit 1
    fi
    echo "File uploaded successfully"
}

# Build common options JSON fragments (avatar, voice, footage, bgm, target_video)
# Sets: common_target_video, common_avatar, common_voice, common_footage, common_bgm
build_common_options() {
    common_target_video="{\"aspect_ratio\": \"$ratio\", \"video_pace\": \"$pace\", \"burn_subtitles\": $burn_subtitles}"
    if [ -n "$video_duration_in_seconds" ]; then
        common_target_video=$(echo "$common_target_video" | jq ". + {\"video_duration_in_seconds\": $video_duration_in_seconds}")
    fi

    common_avatar="{}"
    if [ -n "$avatar" ]; then
        common_avatar=$(echo "$common_avatar" | jq ". + {\"use_avatar\": true, \"look_id\": \"$avatar\"}")
    else
        if [ -n "$avatar_use_avatar" ]; then
            common_avatar=$(echo "$common_avatar" | jq ". + {\"use_avatar\": $avatar_use_avatar}")
        fi
        if [ -n "$avatar_look_id" ]; then
            common_avatar=$(echo "$common_avatar" | jq ". + {\"look_id\": \"$avatar_look_id\"}")
        fi
    fi
    if [ -n "$avatar_avatar_layout" ]; then
        common_avatar=$(echo "$common_avatar" | jq ". + {\"avatar_layout\": \"$avatar_avatar_layout\"}")
    fi
    if [ -n "$avatar_enable_auto_wallpaper" ]; then
        common_avatar=$(echo "$common_avatar" | jq ". + {\"enable_auto_wallpaper\": $avatar_enable_auto_wallpaper}")
    fi
    if [ -n "$avatar_enable_in_preview" ]; then
        common_avatar=$(echo "$common_avatar" | jq ". + {\"enable_in_preview\": $avatar_enable_in_preview}")
    fi

    common_voice="{}"
    if [ -n "$voice" ]; then
        common_voice=$(echo "$common_voice" | jq ". + {\"use_voice\": true, \"voice_id\": \"$voice\"}")
    else
        if [ -n "$voice_use_voice" ]; then
            common_voice=$(echo "$common_voice" | jq ". + {\"use_voice\": $voice_use_voice}")
        fi
        if [ -n "$voice_voice_id" ]; then
            common_voice=$(echo "$common_voice" | jq ". + {\"voice_id\": \"$voice_voice_id\"}")
        fi
    fi

    common_footage="{\"use_free_stocks\": $use_free_stocks, \"use_premium_stocks\": $use_premium_stocks, \"use_premium_stocks_getty\": $use_premium_stocks_getty, \"use_private_stocks\": $use_private_stocks}"
    if [ -n "$footage_enable_footage" ]; then
        common_footage=$(echo "$common_footage" | jq ". + {\"enable_footage\": $footage_enable_footage}")
    fi
    if [ -n "$footage_private_stock_ids" ]; then
        common_footage=$(echo "$common_footage" | jq ". + {\"private_stock_ids\": $footage_private_stock_ids}")
    fi

    common_bgm="{\"use_free_stocks\": $bgm_use_free_stocks, \"use_premium_stocks\": $bgm_use_premium_stocks}"
    if [ -n "$bgm_enable_bgm" ]; then
        common_bgm=$(echo "$common_bgm" | jq ". + {\"enable_bgm\": $bgm_enable_bgm}")
    fi
}

# Append common options to a payload variable name
append_common_payload() {
    local p="$1"
    if [ -n "$video_title" ]; then
        p="$p, \"video_title\": $(echo "$video_title" | jq -Rs .)"
    fi
    if [ -n "$video_description" ]; then
        p="$p, \"video_description\": $(echo "$video_description" | jq -Rs .)"
    fi
    p="$p, \"target_video\": $common_target_video"
    if [ "$common_avatar" != "{}" ]; then
        p="$p, \"avatar_options\": $common_avatar"
    fi
    if [ "$common_voice" != "{}" ]; then
        p="$p, \"voice_options\": $common_voice"
    fi
    p="$p, \"footage_options\": $common_footage, \"bgm_options\": $common_bgm"
    echo "$p"
}

# Create from visual resources (supports multiple files)
cmd_visual() {
    local -a files=("$@")

    # Validate all files first
    for file in "${files[@]}"; do
        validate_read_path "$file"
        if [ ! -f "$file" ]; then
            echo "VISLA_CLI_ERROR_CODE=file_not_found"
            echo -e "${RED}Error: File not found: $file${NC}"
            exit 1
        fi
    done

    # Upload all files and build media_resources array
    local media_resources="[]"
    for file in "${files[@]}"; do
        local filename=$(basename "$file")
        local suffix="${filename##*.}"
        suffix=$(echo "$suffix" | tr '[:upper:]' '[:lower:]')

        local media_type=""
        case "$suffix" in
            jpg|jpeg|png|gif|webp) media_type="image" ;;
            mp4|mov|avi|mkv) media_type="video" ;;
            *)
                echo "VISLA_CLI_ERROR_CODE=unsupported_format"
                echo -e "${RED}Error: Unsupported file type: $suffix${NC}"
                echo "Supported formats: jpg, jpeg, png, gif, webp, mp4, mov, avi, mkv"
                exit 1
                ;;
        esac

        echo "Uploading visual resource: $filename"
        upload_media_file "$file" "$media_type" "$suffix"
        media_resources=$(echo "$media_resources" | jq ". + [{\"media_url\": $(echo "$UPLOAD_URL" | jq -Rs .), \"media_type\": \"$media_type\"}]")
    done
    echo ""

    echo "Creating video from visual resources..."

    build_common_options

    # Build payload with media_resources array
    local payload="{\"media_resources\": $media_resources, \"video_style\": \"$visual_style\""

    # Add script_config if --script provided
    if [ -n "$visual_script" ]; then
        # Read from file if starts with @
        local script_content="$visual_script"
        if [[ "$script_content" == @* ]]; then
            local sfile="${script_content:1}"
            validate_read_path "$sfile"
            validate_text_extension "$sfile"
            if [ -f "$sfile" ]; then
                script_content=$(cat "$sfile")
            fi
        fi
        payload="$payload, \"script_config\": {\"text_content\": $(echo "$script_content" | jq -Rs .), \"text_type\": \"script\"}"
    fi

    payload=$(append_common_payload "$payload")
    payload="$payload}"

    local result=$(visla_request "POST" "/project/visual-to-video" "$payload")

    local project_uuid=$(jq_get "$result" "projectUuid")
    local share_link=$(jq_get "$result" "shareLink")

    if [ -n "$project_uuid" ]; then
        echo "Project created: $project_uuid"
        [ -n "$share_link" ] && echo "View link: $share_link"
        wait_and_export "$project_uuid"
    else
        local code
        code=$(echo "$result" | jq -r '.code // empty' 2>/dev/null || true)
        if [ "$code" != "0" ] && [ -n "$code" ]; then
            local msg
            msg=$(echo "$result" | jq -r '.msg // .message // "Unknown error"' 2>/dev/null || echo "Unknown error")
            echo "VISLA_CLI_ERROR_CODE=$(classify_api_error_code "$msg")"
            echo -e "${RED}Error: ${msg}${NC}"
        else
            echo "VISLA_CLI_ERROR_CODE=api_error"
            echo -e "${RED}Error: Failed to create project${NC}"
            echo "$result"
        fi
        exit 1
    fi
}

# Create from speech (supports multiple files)
cmd_speech() {
    local -a files=("$@")

    # Validate all files first
    for file in "${files[@]}"; do
        validate_read_path "$file"
        if [ ! -f "$file" ]; then
            echo "VISLA_CLI_ERROR_CODE=file_not_found"
            echo -e "${RED}Error: File not found: $file${NC}"
            exit 1
        fi
    done

    # Upload all files
    local media_resources="[]"
    local last_upload_url=""
    for file in "${files[@]}"; do
        local filename=$(basename "$file")
        local suffix="${filename##*.}"
        suffix=$(echo "$suffix" | tr '[:upper:]' '[:lower:]')

        local media_type=""
        case "$suffix" in
            mp3|wav|m4a|aac|flac) media_type="audio" ;;
            mp4|mov|avi|mkv) media_type="video" ;;
            *)
                echo "VISLA_CLI_ERROR_CODE=unsupported_format"
                echo -e "${RED}Error: Unsupported file type: $suffix${NC}"
                echo "Supported formats: mp3, wav, m4a, aac, flac, mp4, mov, avi, mkv"
                exit 1
                ;;
        esac

        echo "Uploading audio file: $filename"
        upload_media_file "$file" "$media_type" "$suffix"
        last_upload_url="$UPLOAD_URL"
        media_resources=$(echo "$media_resources" | jq ". + [{\"media_url\": $(echo "$UPLOAD_URL" | jq -Rs .), \"media_type\": \"$media_type\"}]")
    done
    echo ""

    echo "Creating video from speech..."

    build_common_options

    # API documents speech_asset_url for single file; use media_resources for multiple
    local file_count=${#files[@]}
    local payload
    if [ "$file_count" -eq 1 ]; then
        payload="{\"speech_asset_url\": $(echo "$last_upload_url" | jq -Rs .)"
    else
        payload="{\"media_resources\": $media_resources"
    fi

    # Add speech function if provided
    if [ -n "$speech_function" ]; then
        payload="$payload, \"project_function\": \"$speech_function\""
    fi

    payload=$(append_common_payload "$payload")
    payload="$payload}"

    local result=$(visla_request "POST" "/project/speech-to-video" "$payload")

    local project_uuid=$(jq_get "$result" "projectUuid")
    local share_link=$(jq_get "$result" "shareLink")

    if [ -n "$project_uuid" ]; then
        echo "Project created: $project_uuid"
        [ -n "$share_link" ] && echo "View link: $share_link"
        wait_and_export "$project_uuid"
    else
        local code
        code=$(echo "$result" | jq -r '.code // empty' 2>/dev/null || true)
        if [ "$code" != "0" ] && [ -n "$code" ]; then
            local msg
            msg=$(echo "$result" | jq -r '.msg // .message // "Unknown error"' 2>/dev/null || echo "Unknown error")
            echo "VISLA_CLI_ERROR_CODE=$(classify_api_error_code "$msg")"
            echo -e "${RED}Error: ${msg}${NC}"
        else
            echo "VISLA_CLI_ERROR_CODE=api_error"
            echo -e "${RED}Error: Failed to create project${NC}"
            echo "$result"
        fi
        exit 1
    fi
}

# Wait for project and export
wait_and_export() {
    local project_uuid="$1"

    echo ""
    echo -e "☕ ${YELLOW}Grab a coffee! Video generation takes a few minutes...${NC}"
    echo -e "🎬 Visla AI is creating your video"
    echo ""

    local attempts=0
    local tip_index=0
    local tips_count=${#VISLA_TIPS[@]}
    while [ "$attempts" -lt 180 ]; do
        local result=$(visla_request "GET" "/project/$project_uuid/info")
        local status=$(jq_get "$result" "progressStatus")

        if [ "$status" = "editing" ]; then
            echo ""
            echo -e "${GREEN}✓ Video generated!${NC}"
            local preview_link=$(jq_get "$result" "shareLink")
            [ -n "$preview_link" ] && echo -e "  View link: ${YELLOW}$preview_link${NC}"
            echo -e "  Exporting now, almost done..."
            echo ""
            break
        elif [ "$status" = "failed" ]; then
            echo "VISLA_CLI_ERROR_CODE=api_error"
            echo -e "${RED}Project failed!${NC}"
            echo "$result"
            exit 1
        elif [ -z "$status" ]; then
            echo "VISLA_CLI_ERROR_CODE=api_error"
            echo -e "${RED}Error: Could not read project status (unexpected response)${NC}"
            echo "$result"
            exit 1
        fi

        # Show tip before sleeping
        echo "${VISLA_TIPS[$tip_index]}"
        tip_index=$(( (tip_index + 1) % tips_count ))
        attempts=$((attempts + 1))
        sleep 20
    done

    if [ "$attempts" -ge 180 ]; then
        echo "VISLA_CLI_ERROR_CODE=timeout"
        echo -e "${RED}Error: Timeout waiting for video generation${NC}"
        exit 1
    fi

    # Export
    echo -e "${YELLOW}Exporting video...${NC}"
    local export_result=$(visla_request "POST" "/project/$project_uuid/export-video" "{}")

    local clip_uuid=$(jq_get "$export_result" "clipUuid")
    if [ -z "$clip_uuid" ]; then
        echo "VISLA_CLI_ERROR_CODE=api_error"
        echo -e "${RED}Export failed!${NC}"
        echo "$export_result"
        exit 1
    fi
    echo "Clip UUID: $clip_uuid"

    # Wait for clip to complete
    echo "Waiting for clip to render..."
    attempts=0
    tip_index=0
    while [ "$attempts" -lt 90 ]; do
        local clip_result=$(visla_request "GET" "/clip/$clip_uuid/info")
        local clip_status=$(jq_get "$clip_result" "clipStatus")

        if [ "$clip_status" = "completed" ]; then
            echo ""
            echo -e "${GREEN}Clip completed!${NC}"
            break
        elif [ "$clip_status" = "failed" ]; then
            echo "VISLA_CLI_ERROR_CODE=api_error"
            echo -e "${RED}Clip failed!${NC}"
            echo "$clip_result"
            exit 1
        elif [ -z "$clip_status" ]; then
            echo "VISLA_CLI_ERROR_CODE=api_error"
            echo -e "${RED}Error: Could not read clip status (unexpected response)${NC}"
            echo "$clip_result"
            exit 1
        fi

        # Show tip before sleeping
        echo "${VISLA_TIPS[$tip_index]}"
        tip_index=$(( (tip_index + 1) % tips_count ))
        attempts=$((attempts + 1))
        sleep 20
    done

    if [ "$attempts" -ge 90 ]; then
        echo "VISLA_CLI_ERROR_CODE=timeout"
        echo -e "${RED}Error: Timeout waiting for clip rendering${NC}"
        exit 1
    fi

    local share_link=$(jq_get "$export_result" "shareLink")

    echo ""
    echo -e "${GREEN}Video ready!${NC}"
    [ -n "$share_link" ] && echo "View link: $share_link"
}

# Account command (combines info + credit)
cmd_account() {
    preflight_needs_jq
    local info_result=$(visla_request "GET" "/user/info")
    local credit_result=$(visla_request "GET" "/workspace/credit-balance")

    local info_code
    info_code=$(echo "$info_result" | jq -r '.code // empty' 2>/dev/null || true)
    if [ -z "$info_code" ]; then
        echo "VISLA_CLI_ERROR_CODE=api_error"
        echo -e "${RED}Error: Unexpected response from /user/info (non-JSON)${NC}"
        echo "$info_result"
        exit 1
    fi
    if [ "$info_code" != "0" ]; then
        local msg
        msg=$(echo "$info_result" | jq -r '.msg // .message // "Unknown error"' 2>/dev/null || echo "Unknown error")
        echo "VISLA_CLI_ERROR_CODE=$(classify_api_error_code "$msg")"
        echo -e "${RED}Error: ${msg}${NC}"
        exit 1
    fi

    local credit_code
    credit_code=$(echo "$credit_result" | jq -r '.code // empty' 2>/dev/null || true)
    if [ -z "$credit_code" ]; then
        echo "VISLA_CLI_ERROR_CODE=api_error"
        echo -e "${RED}Error: Unexpected response from /workspace/credit-balance (non-JSON)${NC}"
        echo "$credit_result"
        exit 1
    fi
    if [ "$credit_code" != "0" ]; then
        local msg
        msg=$(echo "$credit_result" | jq -r '.msg // .message // "Unknown error"' 2>/dev/null || echo "Unknown error")
        echo "VISLA_CLI_ERROR_CODE=$(classify_api_error_code "$msg")"
        echo -e "${RED}Error: ${msg}${NC}"
        exit 1
    fi

    local email given_name family_name status reg_time login_time credits
    email=$(echo "$info_result" | jq -r '.data.email // ""')
    given_name=$(echo "$info_result" | jq -r '.data.givenName // ""')
    family_name=$(echo "$info_result" | jq -r '.data.familyName // ""')
    status=$(echo "$info_result" | jq -r '.data.userStatus // ""')
    reg_time=$(echo "$info_result" | jq -r '.data.regTime // 0')
    login_time=$(echo "$info_result" | jq -r '.data.loginTime // 0')
    credits=$(echo "$credit_result" | jq -r '.data // ""')

    # Convert timestamps to dates
    local reg_date="N/A"
    local login_date="N/A"
    if [[ "$reg_time" =~ ^[0-9]+$ ]] && [ "$reg_time" -gt 0 ]; then
        reg_date=$(date -r $((reg_time / 1000)) "+%Y-%m-%d" 2>/dev/null || date -d "@$((reg_time / 1000))" "+%Y-%m-%d" 2>/dev/null || echo "N/A")
    fi
    if [[ "$login_time" =~ ^[0-9]+$ ]] && [ "$login_time" -gt 0 ]; then
        login_date=$(date -r $((login_time / 1000)) "+%Y-%m-%d" 2>/dev/null || date -d "@$((login_time / 1000))" "+%Y-%m-%d" 2>/dev/null || echo "N/A")
    fi

    echo "Email: $email"
    echo "Name: $given_name $family_name"
    echo "Status: $status"
    echo "Registered: $reg_date"
    echo "Last Login: $login_date"
    echo "Credits: $credits"
}

# Avatar command
cmd_avatar() {
    preflight_needs_jq
    local result=$(visla_request "GET" "/workspace/list-avatar")

    local code
    code=$(echo "$result" | jq -r '.code // empty' 2>/dev/null || true)
    if [ -z "$code" ]; then
        echo "VISLA_CLI_ERROR_CODE=api_error"
        echo -e "${RED}Error: Unexpected response (non-JSON)${NC}"
        echo "$result"
        exit 1
    fi
    if [ "$code" != "0" ]; then
        local msg
        msg=$(echo "$result" | jq -r '.msg // .message // "Unknown error"' 2>/dev/null || echo "Unknown error")
        echo "VISLA_CLI_ERROR_CODE=$(classify_api_error_code "$msg")"
        echo -e "${RED}Error: ${msg}${NC}"
        exit 1
    fi

    local avatars
    avatars=$(echo "$result" | jq -r '.data // []' 2>/dev/null || echo "[]")
    
    local count
    count=$(echo "$avatars" | jq 'length' 2>/dev/null || echo "0")
    
    if [ "$count" = "0" ] || [ "$avatars" = "[]" ]; then
        echo "No avatars available"
    else
        echo "Available avatars ($count):"
        echo "$avatars" | jq -r '.[] | .name // "Unnamed"' | while read -r name; do
            echo "$avatars" | jq -r ".[] | select(.name == \"$name\") | .looks[]? | \"  - \(.name // \"Unnamed\") | lookUuid: \(.lookUuid // \"N/A\")\""
            echo "$avatars" | jq -r ".[] | select(.name == \"$name\") | .looks[]? | .thumbnailLink? | if . != \"\" then \"    Thumbnail: \(.)\" else empty end"
        done
    fi
}

# Voice command
cmd_voice() {
    preflight_needs_jq
    local result=$(visla_request "GET" "/workspace/list-voice?localeName=en-US")

    local code
    code=$(echo "$result" | jq -r '.code // empty' 2>/dev/null || true)
    if [ -z "$code" ]; then
        echo "VISLA_CLI_ERROR_CODE=api_error"
        echo -e "${RED}Error: Unexpected response (non-JSON)${NC}"
        echo "$result"
        exit 1
    fi
    if [ "$code" != "0" ]; then
        local msg
        msg=$(echo "$result" | jq -r '.msg // .message // "Unknown error"' 2>/dev/null || echo "Unknown error")
        echo "VISLA_CLI_ERROR_CODE=$(classify_api_error_code "$msg")"
        echo -e "${RED}Error: ${msg}${NC}"
        exit 1
    fi

    local custom_voices
    local system_voices
    custom_voices=$(echo "$result" | jq -r '.data.customVoices // []' 2>/dev/null)
    system_voices=$(echo "$result" | jq -r '.data.systemVoices // []' 2>/dev/null)
    
    local custom_count
    local system_count
    custom_count=$(echo "$custom_voices" | jq 'length' 2>/dev/null || echo "0")
    system_count=$(echo "$system_voices" | jq 'length' 2>/dev/null || echo "0")
    local total=$((custom_count + system_count))
    
    if [ "$total" = "0" ]; then
        echo "No voices available"
    else
        echo "Available voices ($total):"
        
        if [ "$custom_count" -gt 0 ]; then
            echo ""
            echo "[Custom Voices]"
            echo "$custom_voices" | jq -c -r '.[] | {name: (.voiceName // .voiceSpeakerName // "Unnamed"), uuid: (.voiceUuid // .uuid), url: .voiceUrl, fav: .favorite}' | while read -r item; do
                name=$(echo "$item" | jq -r '.name')
                uuid=$(echo "$item" | jq -r '.uuid')
                url=$(echo "$item" | jq -r '.url')
                fav=$(echo "$item" | jq -r '.fav')
                [ "$fav" = "true" ] && fav="★" || fav=""
                echo "  - $name $fav (ID: $uuid)"
                [ "$url" != "null" ] && [ -n "$url" ] && echo "    URL: $url"
            done
        fi
        
        if [ "$system_count" -gt 0 ]; then
            echo ""
            echo "[System Voices]"
            echo "$system_voices" | jq -c -r '.[] | {name: (.voiceName // .voiceSpeakerName // "Unnamed"), uuid: (.voiceUuid // .uuid), url: .voiceUrl, fav: .favorite}' | while read -r item; do
                name=$(echo "$item" | jq -r '.name')
                uuid=$(echo "$item" | jq -r '.uuid')
                url=$(echo "$item" | jq -r '.url')
                fav=$(echo "$item" | jq -r '.fav')
                [ "$fav" = "true" ] && fav="★" || fav=""
                echo "  - $name $fav (ID: $uuid)"
                [ "$url" != "null" ] && [ -n "$url" ] && echo "    URL: $url"
            done
        fi
    fi
}

# Parse arguments
if [ $# -eq 0 ]; then
    show_help
    exit 0
fi

command="$1"
shift

# Help doesn't need credentials
if [ "$command" = "help" ] || [ "$command" = "-h" ] || [ "$command" = "--help" ]; then
    show_help
    exit 0
fi

# Dependency checks for execution commands.
preflight

# All other commands need credentials
check_credentials

echo "Visla Skill v${VERSION}"

ratio="16:9"
pace="fast"
avatar=""
voice=""
burn_subtitles="false"
config_file=""
CONFIG_FILE=""
video_title=""
video_description=""
video_duration_in_seconds=""
script_text_mode="ai_rewrite"
# doc options
doc_usage="page_by_page_walkthrough"
speaker_notes_verbatim="false"
# avatar_options
avatar_use_avatar=""
avatar_look_id=""
avatar_avatar_layout=""
avatar_enable_auto_wallpaper=""
avatar_enable_in_preview=""
# voice_options
voice_use_voice=""
voice_voice_id=""
# footage_options
footage_enable_footage=""
use_free_stocks="true"
use_premium_stocks="false"
use_premium_stocks_getty="false"
use_private_stocks="false"
footage_private_stock_ids=""
# bgm_options
bgm_enable_bgm=""
bgm_use_free_stocks="true"
bgm_use_premium_stocks="false"
# visual/speech specific
visual_style="storytelling"
visual_script=""
speech_function=""

declare -a positional_args=()

# Parse arguments (intentionally keep the user-facing CLI minimal; use internal defaults).
while [[ $# -gt 0 ]]; do
    case "$1" in
        -c|--config)
            config_file="$2"
            shift 2
            ;;
        --avatar)
            avatar="$2"
            shift 2
            ;;
        --voice)
            voice="$2"
            shift 2
            ;;
        --style)
            visual_style="$2"
            shift 2
            ;;
        --script|-s)
            visual_script="$2"
            shift 2
            ;;
        --function)
            speech_function="$2"
            shift 2
            ;;
        *)
            positional_args+=("$1")
            shift
            ;;
    esac
done

# Load config file if provided
if [ -n "$config_file" ]; then
    load_config "$config_file"
fi

# CLI args override config (handled directly in cmd functions using get_config)

# Restore positional arguments
set -- "${positional_args[@]}"

case "$command" in
    script)
        preflight_needs_jq
        if [ -z "$1" ]; then
            echo -e "${RED}Error: script text or @filename required${NC}"
            exit 1
        fi
        cmd_script "$1"
        ;;
    url)
        preflight_needs_jq
        if [ -z "$1" ]; then
            echo -e "${RED}Error: URL required${NC}"
            exit 1
        fi
        cmd_url "$1"
        ;;
    doc)
        preflight_needs_jq
        if [ -z "$1" ]; then
            echo -e "${RED}Error: document file path required${NC}"
            exit 1
        fi
        cmd_doc "$1"
        ;;
    idea)
        preflight_needs_jq
        if [ -z "$1" ]; then
            echo -e "${RED}Error: idea text or @filename required${NC}"
            exit 1
        fi
        cmd_idea "$1"
        ;;
    visual)
        preflight_needs_jq
        if [ -z "$1" ]; then
            echo -e "${RED}Error: visual file path required${NC}"
            exit 1
        fi
        cmd_visual "$@"
        ;;
    speech)
        preflight_needs_jq
        if [ -z "$1" ]; then
            echo -e "${RED}Error: audio/video file path required${NC}"
            exit 1
        fi
        cmd_speech "$@"
        ;;
    account)
        cmd_account
        ;;
    avatar)
        cmd_avatar
        ;;
    voice)
        cmd_voice
        ;;
    help|-h|--help)
        show_help
        ;;
    *)
        echo -e "${RED}Error: Unknown command '$command'${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac

echo "Visla Skill v${VERSION} completed"
