#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./create_youtube_transcript_workbench.sh /path/to/repo-root yt_video_id [YYYY-MM-DD]

ROOT=${1:-/root/.openclaw/workspace}
VIDEO_ID=${2:-n1E9IZfvGMA}
DATE=${3:-$(date +%F)}

WORK="$ROOT/yt_${VIDEO_ID}_workbench_${DATE}"

mkdir -p "$WORK/artifacts" "$WORK/transcripts" "$WORK/scripts" "$WORK/snippets"

# Manifest placeholder
cat > "$WORK/MANIFEST.txt" <<EOF
# Workspace manifest for YouTube transcript workbench
VIDEO_ID=$VIDEO_ID
CREATED_AT=$(date -Iseconds)
ROOT=$ROOT
EOF

echo "Created: $WORK"