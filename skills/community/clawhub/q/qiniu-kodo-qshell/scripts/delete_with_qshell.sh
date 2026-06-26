#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 3 ]; then
  echo "Usage: $0 <qshell_path> <bucket> <remote_key>"
  exit 1
fi

QSH="$1"
BUCKET="$2"
REMOTE_KEY="$3"

"$QSH" delete "$BUCKET" "$REMOTE_KEY"
echo "DELETE_OK bucket=$BUCKET key=$REMOTE_KEY"
