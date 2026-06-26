#!/usr/bin/env bash
# Upload an input file to a job (buyer action — done before worker starts)
# Usage: upload-file.sh <job_id> <file_path>

source "$(dirname "$0")/lib.sh"

job_id="${1:?Usage: upload-file.sh <job_id> <file_path>}"
file_path="${2:?Usage: upload-file.sh <job_id> <file_path>}"

if [[ ! -f "$file_path" ]]; then
  echo "ERROR: File not found: $file_path" >&2
  exit 1
fi

filename=$(basename "$file_path")
file_size=$(wc -c < "$file_path" | tr -d ' ')
content_type=$(get_content_type "$file_path")

# Step 1: Request a presigned upload URL
echo "Requesting upload URL..."
upload_body=$(cat <<EOF
{"purpose":"input","filename":"${filename}","content_type":"${content_type}","file_size_bytes":${file_size}}
EOF
)

url_response=$(vox_api POST "/v1/jobs/${job_id}/files/upload-url" "$upload_body")

upload_url=$(echo "$url_response" | python3 -c "import sys,json; d=json.load(sys.stdin)['data']; print(d['upload_url'])" 2>/dev/null \
  || echo "$url_response" | jq -r '.data.upload_url' 2>/dev/null)
file_id=$(echo "$url_response" | python3 -c "import sys,json; d=json.load(sys.stdin)['data']; print(d['file_id'])" 2>/dev/null \
  || echo "$url_response" | jq -r '.data.file_id' 2>/dev/null)

if [[ -z "$upload_url" || "$upload_url" == "null" || -z "$file_id" || "$file_id" == "null" ]]; then
  echo "ERROR: Could not get upload URL" >&2
  echo "$url_response" >&2
  exit 1
fi

# Step 2: PUT file to presigned URL (no auth header needed)
echo "Uploading ${file_size} bytes..."
curl -s -S -f -X PUT \
  -H "Content-Type: $content_type" \
  --data-binary "@${file_path}" \
  "$upload_url" || { echo "ERROR: Upload to presigned URL failed" >&2; exit 1; }

# Step 3: Confirm the upload
echo "Confirming upload..."
vox_api POST "/v1/jobs/${job_id}/files/${file_id}/confirm" | pretty_json
echo "Done. File ID: $file_id"
