#!/usr/bin/env bash
set -euo pipefail

API_URL="https://agent.mathmind.cn/minimalist/api/volcengine/ai/fzGenerateImg5"
DEFAULT_SIZE="2048x2048"
DEFAULT_WATERMARK="true"
TIMEOUT=600

prompt=""
size="$DEFAULT_SIZE"
watermark="$DEFAULT_WATERMARK"
images=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --prompt)
      prompt="${2:-}"
      shift 2
      ;;
    --size)
      size="${2:-}"
      shift 2
      ;;
    --watermark)
      watermark="${2:-}"
      shift 2
      ;;
    --image)
      images+=("${2:-}")
      shift 2
      ;;
    *)
      echo "Unknown argument: $1"
      exit 1
      ;;
  esac
done

if [[ -z "$prompt" ]]; then
  echo "ERROR: --prompt is required"
  exit 1
fi

if [[ -z "${X_API_KEY:-}" && -f "$HOME/.config/seedream5.0/.env" ]]; then
  set -a
  . "$HOME/.config/seedream5.0/.env"
  set +a
fi

if [[ -z "${X_API_KEY:-}" ]]; then
  echo "ERROR: missing X_API_KEY"
  exit 1
fi

# Normalize watermark input to true/false (macOS bash 3.2 compatible).
watermark_normalized=$(printf '%s' "$watermark" | tr '[:upper:]' '[:lower:]')
case "$watermark_normalized" in
  true|1|yes|y) watermark="true" ;;
  false|0|no|n) watermark="false" ;;
  *)
    echo "ERROR: --watermark must be true or false"
    exit 1
    ;;
esac

images_json="[]"
if [[ ${#images[@]} -gt 0 ]]; then
  images_json=$(printf '%s\n' "${images[@]}" | sed 's/"/\\"/g' | awk 'BEGIN{printf "["} {printf "%s\"%s\"", (NR==1?"":","), $0} END{printf "]"}')
fi

payload=$(printf '{"prompt":"%s","size":"%s","watermark":%s,"image":%s}' "$prompt" "$size" "$watermark" "$images_json")

response=$(curl -s -m "$TIMEOUT" --location "$API_URL" \
  --header 'Content-Type: application/json' \
  --header "x-api-key: $X_API_KEY" \
  --data "$payload" 2>&1)

if [[ -z "$response" ]]; then
  echo "ERROR: request timeout (${TIMEOUT}s)"
  exit 1
fi

echo "$response" | python3 -c '
import json,sys
raw=sys.stdin.read()
try:
    data=json.loads(raw)
except Exception:
    print("RAW_RESPONSE:"+raw[:500])
    raise SystemExit(0)

code=data.get("code")
if code==0:
    d=data.get("data")
    if isinstance(d, dict):
        # Common fields from image APIs.
        if d.get("image_url"):
            print("IMAGE_URL:"+str(d.get("image_url")))
        elif d.get("url"):
            print("IMAGE_URL:"+str(d.get("url")))
        elif d.get("images"):
            imgs=d.get("images")
            if isinstance(imgs,list) and imgs:
                print("IMAGE_URL:"+str(imgs[0]))
            else:
                print("SUCCESS:"+json.dumps(d,ensure_ascii=False))
        else:
            print("SUCCESS:"+json.dumps(d,ensure_ascii=False))
    else:
        print("SUCCESS:"+json.dumps(data,ensure_ascii=False))
else:
    msg=data.get("errorMessage") or data.get("message") or "Unknown error"
    print("ERROR:"+str(msg))
'