#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 4 ]; then
  echo "Usage: $0 <qshell_path> <bucket> <remote_key> <outfile>"
  exit 1
fi

QSH="$1"
BUCKET="$2"
REMOTE_KEY="$3"
OUTFILE="$4"

mkdir -p "$(dirname "$OUTFILE")"
"$QSH" get "$BUCKET" "$REMOTE_KEY" -o "$OUTFILE"
echo "DOWNLOAD_OK bucket=$BUCKET key=$REMOTE_KEY saved=$OUTFILE"
