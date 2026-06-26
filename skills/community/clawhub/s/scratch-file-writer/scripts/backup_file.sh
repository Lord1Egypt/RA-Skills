#!/bin/bash
# Fallback: Copy file to unique .bak.N

FULL_PATH="$1"
BASE_DIR=$(dirname "$FULL_PATH")
FILENAME=$(basename "$FULL_PATH")
EXT="${FILENAME##*.}"
NAME="${FILENAME%.*}"

# Find next .bak.N
N=0
while [ -f "$BASE_DIR/$NAME.bak.$N.$EXT" ]; do
  N=$((N+1))
done

if [ $N -eq 0 ]; then
  BAK_PATH="$BASE_DIR/$NAME.bak.$EXT"
else
  BAK_PATH="$BASE_DIR/$NAME.bak.$N.$EXT"
fi

cp "$FULL_PATH" "$BAK_PATH"
echo "Backed up to $BAK_PATH"
