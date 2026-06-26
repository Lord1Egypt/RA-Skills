#!/usr/bin/env bash
# wuyin-gpt-image2 generate script
# Usage: ./generate.sh -k <api_key> -p <prompt> [-s <size>] [-r <ref_url>] [-o <output>]
#   size: auto (default), 16:9, 9:16, 1:1, 3:2, 2:3

set -euo pipefail

API_BASE="https://api.wuyinkeji.com"
SIZE="auto"
OUTPUT=""
REF_URL=""
PROMPT=""
KEY=""

usage() {
    echo "Usage: $0 -k <api_key> -p <prompt> [-s <size>] [-r <ref_url>] [-o <output>]"
    echo "  -k  API key (required)"
    echo "  -p  Prompt text (required)"
    echo "  -s  Size: auto|16:9|9:16|1:1|3:2|2:3 (default: auto)"
    echo "  -r  Reference image URL (optional)"
    echo "  -o  Output file path (optional, default: auto-named in cwd)"
    exit 1
}

while getopts "k:p:s:r:o:h" opt; do
    case $opt in
        k) KEY="$OPTARG" ;;
        p) PROMPT="$OPTARG" ;;
        s) SIZE="$OPTARG" ;;
        r) REF_URL="$OPTARG" ;;
        o) OUTPUT="$OPTARG" ;;
        h|*) usage ;;
    esac
done

if [[ -z "$KEY" || -z "$PROMPT" ]]; then
    usage
fi

# Step 1: Submit generation task
echo "[1/3] Submitting generation task..."

JSON_BODY=$(cat <<EOF
{
    "key": "$KEY",
    "prompt": "$PROMPT",
    "size": "$SIZE"
EOF
)

if [[ -n "$REF_URL" ]]; then
    JSON_BODY+=$(cat <<EOF
,
    "urls": ["$REF_URL"]
EOF
)
fi

JSON_BODY+="}"

RESPONSE=$(curl -s -X POST "$API_BASE/api/async/image_gpt" \
    -H "Content-Type: application/json" \
    -H "Authorization: $KEY" \
    -d "$JSON_BODY")

TASK_ID=$(echo "$RESPONSE" | grep -oP '"id":\s*"\K[^"]+' | head -1)

if [[ -z "$TASK_ID" ]]; then
    echo "ERROR: Failed to submit task. Response:"
    echo "$RESPONSE"
    exit 1
fi

echo "    Task ID: $TASK_ID"

# Step 2: Poll for result
echo "[2/3] Waiting for generation to complete..."
MAX_RETRIES=60
RETRY=0

while true; do
    DETAIL=$(curl -s "$API_BASE/api/async/detail?id=$TASK_ID&key=$KEY")
    STATUS=$(echo "$DETAIL" | grep -oP '"status":\s*\K[0-9]+' | head -1)
    
    case "$STATUS" in
        2)
            RESULT_URL=$(echo "$DETAIL" | grep -oP '"result":\s*\[\s*"\K[^"]+')
            echo "    Done! Result URL: $RESULT_URL"
            break
            ;;
        0|1)
            RETRY=$((RETRY + 1))
            if [[ $RETRY -gt $MAX_RETRIES ]]; then
                echo "ERROR: Timeout waiting for result after $MAX_RETRIES retries"
                exit 1
            fi
            echo "    Status: $STATUS (processing)... retry $RETRY/$MAX_RETRIES"
            sleep 5
            ;;
        *)
            echo "ERROR: Unknown status $STATUS. Response:"
            echo "$DETAIL"
            exit 1
            ;;
    esac
done

# Step 3: Download image
echo "[3/3] Downloading image..."

if [[ -z "$OUTPUT" ]]; then
    TIMESTAMP=$(date +%s)
    OUTPUT="wuyin_gpt_image_${TIMESTAMP}.png"
fi

curl -sL "$RESULT_URL" -o "$OUTPUT"

FILESIZE=$(ls -lh "$OUTPUT" | awk '{print $5}')
echo "    Saved to: $OUTPUT ($FILESIZE)"

# Show resolution if available
if command -v identify &> /dev/null; then
    RES=$(identify -format "%wx%h" "$OUTPUT" 2>/dev/null || echo "unknown")
    echo "    Resolution: $RES"
fi

echo "Done!"
