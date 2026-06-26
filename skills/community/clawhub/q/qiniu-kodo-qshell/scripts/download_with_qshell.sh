#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 4 ]; then
  echo "Usage: $0 <qshell_path> <bucket> <remote_key> <dest_dir>"
  exit 1
fi

QSH="$1"
BUCKET="$2"
REMOTE_KEY="$3"
DEST_DIR="$4"
TS="$(date +%s)"
KEY_FILE="$DEST_DIR/.keys_${TS}.txt"

mkdir -p "$DEST_DIR"
printf "%s\n" "$REMOTE_KEY" > "$KEY_FILE"
"$QSH" qdownload2 --bucket="$BUCKET" --key-file="$KEY_FILE" --dest-dir="$DEST_DIR"
FOUND="$(find "$DEST_DIR" -type f -name "$REMOTE_KEY" | head -n 1)"
if [ -z "$FOUND" ]; then
  echo "DOWNLOAD_NOT_FOUND key=$REMOTE_KEY"
  exit 1
fi
OUT="$DEST_DIR/${TS}_$(basename "$REMOTE_KEY")"
cp "$FOUND" "$OUT"
echo "DOWNLOAD_OK bucket=$BUCKET key=$REMOTE_KEY saved=$OUT"
