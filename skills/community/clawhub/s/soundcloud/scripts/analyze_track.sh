#!/bin/bash
# Analyze a SoundCloud track in detail

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/auth_token.sh"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

usage() {
    echo "Usage: $0 \"track_id_or_url\""
    echo ""
    echo "Examples:"
    echo "  $0 123456789"
    echo "  $0 https://soundcloud.com/artist/track-name"
    echo ""
    echo "Output includes:"
    echo "  - Basic metadata (title, artist, duration)"
    echo "  - Audio properties (BPM, key if available)"
    echo "  - Engagement stats (plays, likes, reposts)"
    echo "  - License and permissions"
    echo "  - Available stream/download URLs"
}

# Extract track ID from numeric input or URL
extract_track_id() {
    local input="$1"

    if [[ "$input" =~ ^[0-9]+$ ]]; then
        echo "$input"
        return 0
    fi

    if [[ "$input" =~ soundcloud\.com ]]; then
        local response
        response=$(sc_api_get "/resolve?url=${input}")

        if echo "$response" | jq -e '.id' >/dev/null 2>&1; then
            echo "$response" | jq -r '.id'
            return 0
        else
            echo -e "${RED}Error: Could not resolve URL '$input'${NC}" >&2
            return 1
        fi
    else
        echo -e "${RED}Error: Invalid input. Provide a track ID or SoundCloud URL${NC}" >&2
        return 1
    fi
}

format_duration() {
    local ms=$1
    local seconds=$((ms / 1000))
    local minutes=$((seconds / 60))
    local remaining_seconds=$((seconds % 60))
    printf "%d:%02d" $minutes $remaining_seconds
}

format_size() {
    local bytes=$1
    if [ "$bytes" -ge 1073741824 ]; then
        printf "%.2f GB" "$(echo "$bytes / 1073741824" | bc -l 2>/dev/null || echo "0")"
    elif [ "$bytes" -ge 1048576 ]; then
        printf "%.2f MB" "$(echo "$bytes / 1048576" | bc -l 2>/dev/null || echo "0")"
    elif [ "$bytes" -ge 1024 ]; then
        printf "%.2f KB" "$(echo "$bytes / 1024" | bc -l 2>/dev/null || echo "0")"
    else
        printf "%d bytes" "$bytes"
    fi
}

display_analysis() {
    local json="$1"

    echo -e "${BLUE}========================================${NC}"
    echo -e "${GREEN}          TRACK ANALYSIS${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""

    # Basic Information
    echo -e "${YELLOW}=== BASIC INFORMATION ===${NC}"
    echo -e "${CYAN}Title:${NC} $(echo "$json" | jq -r '.title')"
    echo -e "${CYAN}Artist:${NC} $(echo "$json" | jq -r '.user.username // "Unknown"')"
    echo -e "${CYAN}Track ID:${NC} $(echo "$json" | jq -r '.id')"
    echo -e "${CYAN}Permalink:${NC} $(echo "$json" | jq -r '.permalink_url')"
    echo ""

    # Audio Properties
    echo -e "${YELLOW}=== AUDIO PROPERTIES ===${NC}"
    local duration
    duration=$(echo "$json" | jq -r '.duration')
    echo -e "${CYAN}Duration:${NC} $(format_duration "$duration") ($duration ms)"

    local bpm
    bpm=$(echo "$json" | jq -r '.bpm // empty')
    if [ -n "$bpm" ] && [ "$bpm" != "null" ]; then
        echo -e "${CYAN}BPM:${NC} $bpm"
    else
        echo -e "${CYAN}BPM:${NC} Not available"
    fi

    local key
    key=$(echo "$json" | jq -r '.key_signature // empty')
    if [ -n "$key" ] && [ "$key" != "null" ]; then
        echo -e "${CYAN}Key:${NC} $key"
    fi

    local genre
    genre=$(echo "$json" | jq -r '.genre // empty')
    if [ -n "$genre" ] && [ "$genre" != "null" ]; then
        echo -e "${CYAN}Genre:${NC} $genre"
    fi

    local tags
    tags=$(echo "$json" | jq -r '.tag_list // empty')
    if [ -n "$tags" ] && [ "$tags" != "null" ]; then
        echo -e "${CYAN}Tags:${NC} $tags"
    fi
    echo ""

    # Engagement
    echo -e "${YELLOW}=== ENGAGEMENT STATISTICS ===${NC}"
    echo -e "${CYAN}Plays:${NC} $(echo "$json" | jq -r '.playback_count')"
    echo -e "${CYAN}Likes:${NC} $(echo "$json" | jq -r '.favoritings_count // .likes_count // 0')"
    echo -e "${CYAN}Reposts:${NC} $(echo "$json" | jq -r '.reposts_count // 0')"
    echo -e "${CYAN}Comments:${NC} $(echo "$json" | jq -r '.comment_count // 0')"
    echo -e "${CYAN}Downloads:${NC} $(echo "$json" | jq -r '.download_count // 0')"
    echo ""

    # License & Permissions
    echo -e "${YELLOW}=== LICENSE & PERMISSIONS ===${NC}"
    local license
    license=$(echo "$json" | jq -r '.license // empty')
    echo -e "${CYAN}License:${NC} ${license:-(standard SoundCloud license)}"

    local downloadable
    downloadable=$(echo "$json" | jq -r '.downloadable')
    if [ "$downloadable" = "true" ]; then
        echo -e "${CYAN}Downloadable:${NC} ${GREEN}Yes${NC}"
        local download_size
        download_size=$(echo "$json" | jq -r '.original_content_size // 0')
        if [ "$download_size" -gt 0 ]; then
            echo -e "${CYAN}Download size:${NC} $(format_size "$download_size")"
        fi
    else
        echo -e "${CYAN}Downloadable:${NC} ${RED}No${NC}"
    fi

    local streamable
    streamable=$(echo "$json" | jq -r '.streamable')
    echo -e "${CYAN}Streamable:${NC} $([ "$streamable" = "true" ] && echo -e "${GREEN}Yes${NC}" || echo -e "${RED}No${NC}")"
    echo ""

    # URLs
    echo -e "${YELLOW}=== URLs & AVAILABILITY ===${NC}"
    echo -e "${CYAN}Web URL:${NC} $(echo "$json" | jq -r '.permalink_url')"
    echo -e "${CYAN}API URI:${NC} $(echo "$json" | jq -r '.uri')"

    local artwork_url
    artwork_url=$(echo "$json" | jq -r '.artwork_url // empty')
    if [ -n "$artwork_url" ] && [ "$artwork_url" != "null" ]; then
        echo -e "${CYAN}Artwork:${NC} $artwork_url"
    fi

    local stream_url
    stream_url=$(echo "$json" | jq -r '.stream_url // empty')
    if [ -n "$stream_url" ] && [ "$stream_url" != "null" ]; then
        echo -e "${CYAN}Stream URL:${NC} ${stream_url}?client_id=***"
    fi

    local download_url
    download_url=$(echo "$json" | jq -r '.download_url // empty')
    if [ -n "$download_url" ] && [ "$download_url" != "null" ] && [ "$downloadable" = "true" ]; then
        echo -e "${CYAN}Download URL:${NC} ${download_url}?client_id=***"
    fi
    echo ""

    # Metadata
    echo -e "${YELLOW}=== ADDITIONAL METADATA ===${NC}"
    local created_at
    created_at=$(echo "$json" | jq -r '.created_at')
    echo -e "${CYAN}Created:${NC} $(date -d "$created_at" '+%Y-%m-%d %H:%M:%S' 2>/dev/null || echo "$created_at")"

    local release_date
    release_date=$(echo "$json" | jq -r '.release // empty')
    if [ -n "$release_date" ] && [ "$release_date" != "null" ]; then
        echo -e "${CYAN}Release:${NC} $release_date"
    fi

    local label_name
    label_name=$(echo "$json" | jq -r '.label_name // empty')
    if [ -n "$label_name" ] && [ "$label_name" != "null" ]; then
        echo -e "${CYAN}Label:${NC} $label_name"
    fi

    local purchase_url
    purchase_url=$(echo "$json" | jq -r '.purchase_url // empty')
    if [ -n "$purchase_url" ] && [ "$purchase_url" != "null" ]; then
        echo -e "${CYAN}Purchase:${NC} $purchase_url"
    fi
    echo ""

    # Waveform
    local waveform_url
    waveform_url=$(echo "$json" | jq -r '.waveform_url // empty')
    if [ -n "$waveform_url" ] && [ "$waveform_url" != "null" ]; then
        echo -e "${YELLOW}=== WAVEFORM DATA ===${NC}"
        echo -e "${CYAN}Waveform URL:${NC} $waveform_url"
    fi

    echo -e "${BLUE}========================================${NC}"
}

# --- Main ---
if [ $# -eq 0 ]; then
    usage
    exit 1
fi

TRACK_INPUT="$1"

echo -e "${YELLOW}Processing: $TRACK_INPUT${NC}" >&2
TRACK_ID=$(extract_track_id "$TRACK_INPUT") || exit 1
echo -e "${GREEN}Resolved to track ID: $TRACK_ID${NC}" >&2

echo -e "${YELLOW}Fetching track data...${NC}" >&2
TRACK_DATA=$(sc_api_get "/tracks/${TRACK_ID}")

if ! echo "$TRACK_DATA" | jq -e '.id' >/dev/null 2>&1; then
    if echo "$TRACK_DATA" | jq -e '.error or .errors' >/dev/null 2>&1; then
        ERROR_MSG=$(echo "$TRACK_DATA" | jq -r '.message // .error // "Unknown error"')
        echo -e "${RED}API Error: $ERROR_MSG${NC}"
    else
        echo -e "${RED}Error: Failed to fetch track data${NC}"
        echo "Response: $TRACK_DATA"
    fi
    exit 1
fi

display_analysis "$TRACK_DATA"

# Optional: Save to file
read -p "Save analysis to file? (y/N): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    FILENAME="soundcloud_track_${TRACK_ID}_analysis_$(date +%Y%m%d_%H%M%S).txt"
    display_analysis "$TRACK_DATA" > "$FILENAME"
    echo -e "${GREEN}Analysis saved to: $FILENAME${NC}"
fi
