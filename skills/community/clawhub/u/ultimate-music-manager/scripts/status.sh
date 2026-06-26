#!/usr/bin/env bash
# =============================================================================
# Sonic Phoenix — Pipeline Status Dashboard
# =============================================================================
# Prints a quick summary of the current pipeline state: how many files have
# been scanned, identified, sorted, duplicated, and what data files exist.
#
# Usage:
#   ./scripts/status.sh
#
# Answers the question: "Where am I in the pipeline?"
# =============================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# Colour helpers
# ---------------------------------------------------------------------------
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

# ---------------------------------------------------------------------------
# Locate repo root and resolve paths via config.py
# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

if [ ! -f "$REPO_ROOT/config.py" ]; then
    echo "[error] Cannot find config.py at $REPO_ROOT"
    exit 1
fi

# Resolve Python
PYTHON=""
for candidate in python3.12 python3 python; do
    if command -v "$candidate" &>/dev/null; then
        ver=$("$candidate" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null || echo "")
        if [ "$ver" = "3.12" ]; then
            PYTHON="$candidate"
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    echo "[error] Python 3.12 not found."
    exit 1
fi

# Pull paths from config.py into bash variables
eval "$("$PYTHON" -c "
import sys
sys.path.insert(0, '$REPO_ROOT')
import config
print(f'MUSIC_ROOT=\"{config.MUSIC_ROOT}\"')
print(f'SORTED_ROOT=\"{config.SORTED_ROOT}\"')
print(f'DATA_DIR=\"{config.DATA_DIR}\"')
print(f'DUPLICATES_STAGING=\"{config.DUPLICATES_STAGING}\"')
print(f'UNIDENTIFIED_DIR=\"{config.UNIDENTIFIED_DIR}\"')
" 2>/dev/null)"

# ---------------------------------------------------------------------------
# Counting helpers
# ---------------------------------------------------------------------------
AUDIO_EXTS="mp3|m4a|flac|wav|ogg|wma|aac|opus"

count_audio_files() {
    local dir="$1"
    if [ ! -d "$dir" ]; then
        echo 0
        return
    fi
    find "$dir" -type f -regextype posix-extended \
        -iregex ".*\\.($AUDIO_EXTS)$" 2>/dev/null | wc -l | tr -d ' '
}

count_json_entries() {
    local file="$1"
    if [ ! -f "$file" ]; then
        echo "-"
        return
    fi
    "$PYTHON" -c "
import json, sys
try:
    data = json.load(open('$file', encoding='utf-8'))
    if isinstance(data, dict):
        # For catalogs keyed by path or hash
        if 'files' in data:
            print(len(data['files']))
        else:
            print(len(data))
    elif isinstance(data, list):
        print(len(data))
    else:
        print('?')
except Exception:
    print('ERR')
" 2>/dev/null
}

file_size_human() {
    local file="$1"
    if [ ! -f "$file" ]; then
        echo "-"
        return
    fi
    "$PYTHON" -c "
from pathlib import Path
size = Path('$file').stat().st_size
for unit in ('B','KB','MB','GB'):
    if size < 1024 or unit == 'GB':
        print(f'{size:.1f} {unit}')
        break
    size /= 1024
" 2>/dev/null
}

# ---------------------------------------------------------------------------
# Gather data
# ---------------------------------------------------------------------------
echo ""
printf "${BOLD}Sonic Phoenix — Status Dashboard${NC}\n"
echo "================================"
echo ""

# Music root
printf "${CYAN}Music Root:${NC} %s\n" "$MUSIC_ROOT"
if [ -d "$MUSIC_ROOT" ]; then
    UNSORTED=$(count_audio_files "$MUSIC_ROOT")
    printf "  Total audio files under MUSIC_ROOT: %s\n" "$UNSORTED"
else
    printf "  ${YELLOW}[WARN] MUSIC_ROOT does not exist!${NC}\n"
fi
echo ""

# Sorted library
printf "${CYAN}Sorted Library:${NC} %s\n" "$SORTED_ROOT"
if [ -d "$SORTED_ROOT" ]; then
    SORTED_COUNT=$(count_audio_files "$SORTED_ROOT")
    printf "  Sorted audio files: %s\n" "$SORTED_COUNT"

    # Language breakdown
    if [ -d "$SORTED_ROOT" ]; then
        printf "  Languages:\n"
        for lang_dir in "$SORTED_ROOT"/*/; do
            if [ -d "$lang_dir" ]; then
                lang_name=$(basename "$lang_dir")
                if [ "$lang_name" = "Unidentified" ]; then
                    continue
                fi
                lang_count=$(count_audio_files "$lang_dir")
                if [ "$lang_count" -gt 0 ] 2>/dev/null; then
                    printf "    %-20s %s files\n" "$lang_name" "$lang_count"
                fi
            fi
        done
    fi
else
    printf "  ${DIM}(not created yet — run the pipeline first)${NC}\n"
fi
echo ""

# Unidentified
printf "${CYAN}Unidentified:${NC} %s\n" "$UNIDENTIFIED_DIR"
if [ -d "$UNIDENTIFIED_DIR" ]; then
    UNID_COUNT=$(count_audio_files "$UNIDENTIFIED_DIR")
    printf "  Unidentified files: %s\n" "$UNID_COUNT"
else
    printf "  ${DIM}(none)${NC}\n"
fi
echo ""

# Duplicates staging
printf "${CYAN}Duplicates Staging:${NC} %s\n" "$DUPLICATES_STAGING"
if [ -d "$DUPLICATES_STAGING" ]; then
    DUP_COUNT=$(count_audio_files "$DUPLICATES_STAGING")
    printf "  Staged duplicates: %s\n" "$DUP_COUNT"
else
    printf "  ${DIM}(none)${NC}\n"
fi
echo ""

# Data files
printf "${CYAN}Data Files:${NC} %s\n" "$DATA_DIR"
if [ -d "$DATA_DIR" ]; then
    echo ""
    printf "  %-35s %-10s %s\n" "File" "Entries" "Size"
    printf "  %-35s %-10s %s\n" "----" "-------" "----"

    DATA_FILES=(
        "metadata_catalog.json"
        "shazam_final_results.json"
        "shazam_hash_results.json"
        "catalog.json"
        "enrichment_report.json"
        "mismatch_report.json"
        "final_catalog.json"
        "consolidation_log.json"
        "spotify_sync_state.json"
        "discovery_sync_state.json"
    )

    for df in "${DATA_FILES[@]}"; do
        full_path="$DATA_DIR/$df"
        if [ -f "$full_path" ]; then
            entries=$(count_json_entries "$full_path")
            size=$(file_size_human "$full_path")
            printf "  ${GREEN}%-35s${NC} %-10s %s\n" "$df" "$entries" "$size"
        else
            printf "  ${DIM}%-35s${NC} %-10s %s\n" "$df" "-" "-"
        fi
    done

    # Token cache (not JSON, just check existence)
    if [ -f "$DATA_DIR/.spotify_token_cache" ]; then
        printf "  ${GREEN}%-35s${NC} %-10s %s\n" ".spotify_token_cache" "cached" "$(file_size_human "$DATA_DIR/.spotify_token_cache")"
    fi

    # Spotify backups dir
    if [ -d "$DATA_DIR/spotify_backups" ]; then
        backup_count=$(find "$DATA_DIR/spotify_backups" -name "*.json" 2>/dev/null | wc -l | tr -d ' ')
        printf "  ${GREEN}%-35s${NC} %-10s %s\n" "spotify_backups/" "${backup_count} files" "-"
    fi
else
    printf "  ${DIM}(not created yet)${NC}\n"
fi

# ---------------------------------------------------------------------------
# Pipeline progress estimate
# ---------------------------------------------------------------------------
echo ""
printf "${CYAN}Pipeline Progress:${NC}\n"

check_phase() {
    local phase="$1"
    local file="$2"
    local desc="$3"
    if [ -f "$file" ]; then
        printf "  ${GREEN}[done]${NC}  %-10s %s\n" "$phase" "$desc"
    else
        printf "  ${DIM}[ -- ]  %-10s %s${NC}\n" "$phase" "$desc"
    fi
}

check_phase "Phase 1" "$DATA_DIR/metadata_catalog.json" "Metadata extraction"
check_phase "Phase 1" "$DATA_DIR/shazam_final_results.json" "Shazam fingerprinting"
check_phase "Phase 2" "$DATA_DIR/catalog.json" "SHA-256 deduplication catalog"

if [ -d "$SORTED_ROOT" ] && [ "$(count_audio_files "$SORTED_ROOT")" -gt 0 ] 2>/dev/null; then
    printf "  ${GREEN}[done]${NC}  %-10s %s\n" "Phase 2" "Library sorted"
else
    printf "  ${DIM}[ -- ]  %-10s %s${NC}\n" "Phase 2" "Library sorted"
fi

check_phase "Phase 4" "$DATA_DIR/enrichment_report.json" "Metadata enrichment"
check_phase "Phase 5" "$DATA_DIR/final_catalog.json" "Master catalog locked"
check_phase "Phase 6" "$DATA_DIR/.spotify_token_cache" "Spotify authenticated"
check_phase "Phase 6" "$DATA_DIR/spotify_sync_state.json" "Spotify sync"

echo ""
