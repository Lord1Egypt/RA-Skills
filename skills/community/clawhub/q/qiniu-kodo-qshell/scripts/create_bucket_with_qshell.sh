#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 3 ]; then
  echo "Usage: $0 <qshell_path> <bucket> <region> [--private]"
  exit 1
fi

QSH="$1"
BUCKET="$2"
REGION="$3"
PRIVATE_FLAG="${4:-}"

if [ "$PRIVATE_FLAG" = "--private" ]; then
  "$QSH" mkbucket "$BUCKET" --region "$REGION" --private
else
  "$QSH" mkbucket "$BUCKET" --region "$REGION"
fi

echo "CREATE_BUCKET_OK bucket=$BUCKET region=$REGION private=${PRIVATE_FLAG:---public}"
