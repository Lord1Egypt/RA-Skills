#!/usr/bin/env bash
# =============================================================================
# Sonic Phoenix — Happy-Path Pipeline Runner
# =============================================================================
# Executes the canonical pipeline phases in the correct order with progress
# output. Stops on the first script that exits non-zero.
#
# Usage:
#   ./scripts/run-pipeline.sh                  # full pipeline (Phases 1-5)
#   ./scripts/run-pipeline.sh --skip-shazam    # skip acoustic fingerprinting
#   ./scripts/run-pipeline.sh --spotify        # include Phase 6 (Spotify sync)
#   ./scripts/run-pipeline.sh --dry-run        # print the plan without running
#
# Prerequisites:
#   - Run preflight.sh first (or let this script do it for you).
#   - Virtual environment must be active.
#   - MUSIC_ROOT must be set.
#
# What runs (in order):
#   Phase 1: 01A → 01D   (extract metadata, Shazam fingerprint everything)
#   Phase 2: 02A → 02D   (SHA-256 catalog, sort into Language/Artist/Album)
#   Phase 3: 03A → 03D   (consolidate artist folders, enforce structure)
#   Phase 4: 04I          (enrich tags via iTunes, embed artwork, fetch lyrics)
#   Phase 5: 05I          (lock the master catalog)
#   Phase 6: 06B-06E      (Spotify sync — only with --spotify flag)
# =============================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# Colour helpers
# ---------------------------------------------------------------------------
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# ---------------------------------------------------------------------------
# Parse arguments
# ---------------------------------------------------------------------------
SKIP_SHAZAM=false
INCLUDE_SPOTIFY=false
DRY_RUN=false

for arg in "$@"; do
    case "$arg" in
        --skip-shazam) SKIP_SHAZAM=true ;;
        --spotify)     INCLUDE_SPOTIFY=true ;;
        --dry-run)     DRY_RUN=true ;;
        -h|--help)
            echo "Usage: run-pipeline.sh [--skip-shazam] [--spotify] [--dry-run]"
            echo ""
            echo "  --skip-shazam   Skip Phase 1 acoustic fingerprinting (use existing results)"
            echo "  --spotify       Include Phase 6 Spotify sync after the main pipeline"
            echo "  --dry-run       Print the execution plan without running anything"
            exit 0
            ;;
        *)
            echo "Unknown argument: $arg (use --help)"
            exit 1
            ;;
    esac
done

# ---------------------------------------------------------------------------
# Locate repo root
# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

if [ ! -f "$REPO_ROOT/config.py" ]; then
    printf "${RED}[error]${NC} Cannot find config.py at $REPO_ROOT\n"
    exit 1
fi

# ---------------------------------------------------------------------------
# Resolve Python
# ---------------------------------------------------------------------------
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
    printf "${RED}[error]${NC} Python 3.12 not found. Run preflight.sh for details.\n"
    exit 1
fi

# ---------------------------------------------------------------------------
# Build the execution plan
# ---------------------------------------------------------------------------
STEPS=()

# Phase 1 — Extraction & Identification
STEPS+=("Phase 1|01A_extract_metadata.py|Extract ID3/FLAC tags from all audio files")
if [ "$SKIP_SHAZAM" = false ]; then
    STEPS+=("Phase 1|01D_shazam_all_files.py|Acoustic fingerprint every file via Shazam (this takes a while)")
fi

# Phase 2 — Cataloguing & Sorting
STEPS+=("Phase 2|02A_catalog_music.py|Build SHA-256 hash catalog + detect duplicates")
STEPS+=("Phase 2|02D_organize_music.py|Sort files into Language/Artist/Album hierarchy")

# Phase 3 — Consolidation
STEPS+=("Phase 3|03A_consolidate_by_artist.py|Merge fragmented artist folders")
STEPS+=("Phase 3|03D_titanium_resort.py|Final structural enforcement pass")

# Phase 4 — Enrichment
STEPS+=("Phase 4|04I_polish_and_enrich_v6.py|Enrich tags (iTunes + LrcLib lyrics + cover art)")

# Phase 5 — Finalization
STEPS+=("Phase 5|05I_finalize_catalog.py|Lock the master catalog (final_catalog.json)")

# Phase 6 — Spotify (optional)
if [ "$INCLUDE_SPOTIFY" = true ]; then
    STEPS+=("Phase 6|06B_spotify_setup.py|Spotify OAuth handshake (run once)")
    STEPS+=("Phase 6|06C_spotify_backup.py|Snapshot existing Spotify playlists")
    STEPS+=("Phase 6|06D_spotify_sync_engine.py|Create per-language Spotify playlists")
    STEPS+=("Phase 6|06E_spotify_discovery_sync.py|Generate genre-based Essentials playlists")
fi

TOTAL=${#STEPS[@]}

# ---------------------------------------------------------------------------
# Print the plan
# ---------------------------------------------------------------------------
echo ""
printf "${BOLD}Sonic Phoenix — Pipeline Execution Plan${NC}\n"
echo "========================================"
echo ""

for i in "${!STEPS[@]}"; do
    IFS='|' read -r phase script desc <<< "${STEPS[$i]}"
    step_num=$((i + 1))
    printf "  %2d. [%-7s] %-35s %s\n" "$step_num" "$phase" "$script" "$desc"
done

echo ""
echo "$TOTAL steps total."

if [ "$DRY_RUN" = true ]; then
    echo ""
    printf "${CYAN}Dry run — no scripts were executed.${NC}\n"
    exit 0
fi

# ---------------------------------------------------------------------------
# Execute
# ---------------------------------------------------------------------------
echo ""
printf "${BOLD}Starting pipeline...${NC}\n"
echo ""

STARTED=$(date +%s)

for i in "${!STEPS[@]}"; do
    IFS='|' read -r phase script desc <<< "${STEPS[$i]}"
    step_num=$((i + 1))

    printf "${CYAN}[%d/%d] %s — %s${NC}\n" "$step_num" "$TOTAL" "$phase" "$script"
    printf "       %s\n" "$desc"
    echo ""

    STEP_START=$(date +%s)

    if ! "$PYTHON" "$REPO_ROOT/$script"; then
        echo ""
        printf "${RED}[FAILED] %s exited with a non-zero status.${NC}\n" "$script"
        printf "         Pipeline stopped at step %d of %d.\n" "$step_num" "$TOTAL"
        printf "         Fix the issue and re-run. Completed steps are safe to skip.\n"
        exit 1
    fi

    STEP_END=$(date +%s)
    STEP_ELAPSED=$(( STEP_END - STEP_START ))
    echo ""
    printf "${GREEN}[DONE]${NC} %s completed in %ds\n" "$script" "$STEP_ELAPSED"
    echo "------------------------------------------------------------------------"
    echo ""
done

FINISHED=$(date +%s)
TOTAL_ELAPSED=$(( FINISHED - STARTED ))
MINUTES=$(( TOTAL_ELAPSED / 60 ))
SECONDS_REM=$(( TOTAL_ELAPSED % 60 ))

echo ""
printf "${GREEN}${BOLD}Pipeline complete!${NC}\n"
printf "Total time: %dm %ds\n" "$MINUTES" "$SECONDS_REM"
echo ""
echo "Next steps:"
echo "  - Review duplicates in Duplicates_Staging/"
echo "  - Check Sorted/ for your organised library"
echo "  - Run: $PYTHON $REPO_ROOT/config.py   (verify paths)"
if [ "$INCLUDE_SPOTIFY" = false ]; then
    echo "  - Optional: re-run with --spotify to sync to Spotify"
fi
