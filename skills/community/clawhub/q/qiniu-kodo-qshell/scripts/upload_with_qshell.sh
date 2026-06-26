#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 4 ]; then
  echo "Usage: $0 <qshell_path> <bucket> <remote_key> <local_file>"
  exit 1
fi

QSH="$1"
BUCKET="$2"
REMOTE_KEY="$3"
LOCAL_FILE="$4"
THRESHOLD_BYTES="${QINIU_RPUT_THRESHOLD_BYTES:-104857600}"
SIZE="$(wc -c < "$LOCAL_FILE")"

if [ "$SIZE" -ge "$THRESHOLD_BYTES" ]; then
  "$QSH" rput "$BUCKET" "$REMOTE_KEY" "$LOCAL_FILE"
  echo "UPLOAD_OK method=rput bucket=$BUCKET key=$REMOTE_KEY file=$LOCAL_FILE size=$SIZE"
else
  "$QSH" fput "$BUCKET" "$REMOTE_KEY" "$LOCAL_FILE"
  echo "UPLOAD_OK method=fput bucket=$BUCKET key=$REMOTE_KEY file=$LOCAL_FILE size=$SIZE"
fi
