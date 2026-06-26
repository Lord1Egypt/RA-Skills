#!/usr/bin/env bash
# Textin File Converter - Universal conversion script
# Usage: ./convert.sh <conversion_type> <input_file_or_url> <output_path>
#
# Credentials must be set via environment variables:
#   TEXTIN_APP_ID      - Textin API application ID
#   TEXTIN_SECRET_CODE - Textin API secret code
#
# Conversion types:
#   pdf-to-word, pdf-to-excel, pdf-to-ppt, pdf-to-image,
#   word-to-pdf, word-to-image, excel-to-pdf, image-to-pdf,
#   image-to-word

set -euo pipefail

# --- Constants ---
ALLOWED_API_HOST="api.textin.com"
MAX_FILE_SIZE_BYTES=$((50 * 1024 * 1024))  # 50MB

# --- Arguments ---
CONVERSION_TYPE="${1:?Usage: convert.sh <type> <input> <output>}"
INPUT="${2:?Missing input file path or URL}"
OUTPUT_PATH="${3:?Missing output file path}"

# --- Credentials (environment variables only, never CLI args) ---
APP_ID="${TEXTIN_APP_ID:-}"
SECRET_CODE="${TEXTIN_SECRET_CODE:-}"

if [[ -z "$APP_ID" || -z "$SECRET_CODE" ]]; then
  echo "Error: Textin credentials required." >&2
  echo "Set environment variables TEXTIN_APP_ID and TEXTIN_SECRET_CODE." >&2
  echo "Obtain credentials at: https://www.textin.com/user/login" >&2
  exit 1
fi

# --- Determine API endpoint ---
case "$CONVERSION_TYPE" in
  pdf-to-word)   API_PATH="/ai/service/v1/file-convert/pdf-to-word" ;;
  pdf-to-excel)  API_PATH="/ai/service/v1/file-convert/pdf-to-excel" ;;
  pdf-to-ppt)    API_PATH="/ai/service/v1/file-convert/pdf-to-ppt" ;;
  pdf-to-image)  API_PATH="/ai/service/v1/file-convert/pdf-to-image" ;;
  word-to-pdf)   API_PATH="/ai/service/v1/file-convert/word-to-pdf" ;;
  word-to-image) API_PATH="/ai/service/v1/file-convert/word-to-image" ;;
  excel-to-pdf)  API_PATH="/ai/service/v1/file-convert/excel-to-pdf" ;;
  image-to-pdf)  API_PATH="/ai/service/v1/file-convert/image-to-pdf" ;;
  image-to-word) API_PATH="/robot/v1.0/api/doc_restore" ;;
  *)
    echo "Error: Unknown conversion type '$CONVERSION_TYPE'" >&2
    echo "Valid types: pdf-to-word, pdf-to-excel, pdf-to-ppt, pdf-to-image, word-to-pdf, word-to-image, excel-to-pdf, image-to-pdf, image-to-word" >&2
    exit 1
    ;;
esac

ENDPOINT="https://${ALLOWED_API_HOST}${API_PATH}"

# --- Validation helpers ---
validate_file_size() {
  local file="$1"
  local size
  size=$(wc -c < "$file" | xargs)
  if [[ "$size" -gt "$MAX_FILE_SIZE_BYTES" ]]; then
    echo "Error: File exceeds 50MB size limit: $file ($size bytes)" >&2
    exit 1
  fi
}

validate_file_extension() {
  local file="$1"
  local basename
  basename="$(basename "$file")"
  local ext="${basename##*.}"
  ext="$(echo "$ext" | tr '[:upper:]' '[:lower:]')"

  case "$CONVERSION_TYPE" in
    pdf-to-*)
      [[ "$ext" == "pdf" ]] || { echo "Error: Expected .pdf file, got .$ext: $file" >&2; exit 1; } ;;
    word-to-*)
      [[ "$ext" == "docx" || "$ext" == "doc" ]] || { echo "Error: Expected .docx/.doc file, got .$ext: $file" >&2; exit 1; } ;;
    excel-to-*)
      [[ "$ext" == "xlsx" || "$ext" == "xls" ]] || { echo "Error: Expected .xlsx/.xls file, got .$ext: $file" >&2; exit 1; } ;;
    image-to-*)
      [[ "$ext" == "jpg" || "$ext" == "jpeg" || "$ext" == "png" || "$ext" == "bmp" ]] || { echo "Error: Expected image file (.jpg/.jpeg/.png/.bmp), got .$ext: $file" >&2; exit 1; } ;;
  esac
}

# --- Build and execute the API request ---
make_request() {
  local input="$1"
  local is_url=false

  # Check if input is a URL
  if [[ "$input" =~ ^https?:// ]]; then
    is_url=true
  fi

  # Special handling for image-to-pdf: requires JSON body with base64 array
  if [[ "$CONVERSION_TYPE" == "image-to-pdf" ]]; then
    if [[ "$is_url" == true ]]; then
      echo "Error: image-to-pdf does not support URL input. Please provide local file paths." >&2
      exit 1
    fi
    # Support multiple files separated by comma
    local json_files=""
    IFS=',' read -ra FILES <<< "$input"
    for file in "${FILES[@]}"; do
      file=$(echo "$file" | xargs) # trim whitespace
      if [[ ! -f "$file" ]]; then
        echo "Error: File not found: $file" >&2
        exit 1
      fi
      validate_file_extension "$file"
      validate_file_size "$file"
      local b64
      b64=$(base64 < "$file" | tr -d '\n')
      if [[ -n "$json_files" ]]; then
        json_files="$json_files,"
      fi
      json_files="$json_files\"$b64\""
    done

    curl -s -w "\n%{http_code}" \
      --location --request POST "$ENDPOINT" \
      --header "x-ti-app-id: $APP_ID" \
      --header "x-ti-secret-code: $SECRET_CODE" \
      --header "Content-Type: application/json" \
      --data "{\"files\":[$json_files]}"
    return
  fi

  # Standard request: binary upload or URL
  if [[ "$is_url" == true ]]; then
    curl -s -w "\n%{http_code}" \
      --location --request POST "$ENDPOINT" \
      --header "x-ti-app-id: $APP_ID" \
      --header "x-ti-secret-code: $SECRET_CODE" \
      --header "Content-Type: text/plain" \
      --data-raw "$input"
  else
    if [[ ! -f "$input" ]]; then
      echo "Error: File not found: $input" >&2
      exit 1
    fi
    validate_file_extension "$input"
    validate_file_size "$input"
    curl -s -w "\n%{http_code}" \
      --location --request POST "$ENDPOINT" \
      --header "x-ti-app-id: $APP_ID" \
      --header "x-ti-secret-code: $SECRET_CODE" \
      --header "Content-Type: application/octet-stream" \
      --data-binary "@$input"
  fi
}

echo "Converting: $CONVERSION_TYPE"
echo "Input: $INPUT"
echo "API endpoint: https://${ALLOWED_API_HOST}${API_PATH}"
echo "Calling Textin API..."

RESPONSE=$(make_request "$INPUT")

# Extract HTTP status code (last line)
HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

# Parse response code from JSON
API_CODE=$(echo "$BODY" | python3 -c "import sys,json; print(json.load(sys.stdin).get('code',''))" 2>/dev/null || echo "")
API_MSG=$(echo "$BODY" | python3 -c "import sys,json; print(json.load(sys.stdin).get('message',''))" 2>/dev/null || echo "")

if [[ "$API_CODE" != "200" ]]; then
  echo "Error: API returned code=$API_CODE, message=$API_MSG" >&2
  echo "HTTP status: $HTTP_CODE" >&2
  # Print known error descriptions
  case "$API_CODE" in
    40003) echo "Hint: Insufficient account balance. Please top up at https://www.textin.com" >&2 ;;
    40101) echo "Hint: Missing authentication headers. Check TEXTIN_APP_ID and TEXTIN_SECRET_CODE." >&2 ;;
    40102) echo "Hint: Invalid credentials. Verify your app ID and secret code." >&2 ;;
    40301) echo "Hint: Unsupported file type for this conversion." >&2 ;;
    40302) echo "Hint: File exceeds 50MB size limit." >&2 ;;
    40306) echo "Hint: Rate limit exceeded. Wait before retrying (do NOT retry immediately)." >&2 ;;
  esac
  exit 1
fi

# Extract and decode the base64 result
if [[ "$CONVERSION_TYPE" == "image-to-word" ]]; then
  # doc_restore returns result.docx instead of result directly
  echo "$BODY" | python3 -c "
import sys, json, base64
data = json.load(sys.stdin)
b64 = data['result']['docx']
sys.stdout.buffer.write(base64.b64decode(b64))
" > "$OUTPUT_PATH"
else
  echo "$BODY" | python3 -c "
import sys, json, base64
data = json.load(sys.stdin)
b64 = data['result']
sys.stdout.buffer.write(base64.b64decode(b64))
" > "$OUTPUT_PATH"
fi

FILE_SIZE=$(wc -c < "$OUTPUT_PATH" | xargs)
echo "Success! Output saved to: $OUTPUT_PATH ($FILE_SIZE bytes)"
