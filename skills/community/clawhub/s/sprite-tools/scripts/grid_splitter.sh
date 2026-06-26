#!/bin/bash
# grid_splitter.sh — Split a batch grid image into individual sprites
# Usage: bash grid_splitter.sh <input.png> <layout> [output_dir]
# Example: bash grid_splitter.sh /tmp/batch.png 2x3 /tmp/icons/

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ $# -lt 2 ]; then
    echo "Usage: bash grid_splitter.sh <input_image> <layout> [output_dir]"
    echo "  layout: 2x3 / 3x2 / 2x2 / 4x3 / ..."
    exit 1
fi

python3 "$SCRIPT_DIR/grid_splitter.py" "$@"
