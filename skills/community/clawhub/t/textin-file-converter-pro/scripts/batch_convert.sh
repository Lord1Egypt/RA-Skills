#!/usr/bin/env bash
# Textin File Converter - Batch conversion script
# Usage: ./batch_convert.sh <conversion_type> <input_dir> [output_dir]
#
# Credentials must be set via environment variables:
#   TEXTIN_APP_ID      - Textin API application ID
#   TEXTIN_SECRET_CODE - Textin API secret code
#
# Scans input_dir for files matching the source format of the conversion type,
# converts each file, and saves results to output_dir (defaults to input_dir).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONVERT_SCRIPT="$SCRIPT_DIR/convert.sh"

CONVERSION_TYPE="${1:?Usage: batch_convert.sh <type> <input_dir> [output_dir]}"
INPUT_DIR="${2:?Missing input directory}"
OUTPUT_DIR="${3:-$INPUT_DIR}"

# Credentials are read from environment by convert.sh
if [[ -z "${TEXTIN_APP_ID:-}" || -z "${TEXTIN_SECRET_CODE:-}" ]]; then
  echo "Error: Textin credentials required." >&2
  echo "Set environment variables TEXTIN_APP_ID and TEXTIN_SECRET_CODE." >&2
  exit 1
fi

if [[ ! -d "$INPUT_DIR" ]]; then
  echo "Error: Input directory not found: $INPUT_DIR" >&2
  exit 1
fi

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Determine source file extensions and target extension based on conversion type
case "$CONVERSION_TYPE" in
  pdf-to-word)    SRC_EXTS=("pdf") TARGET_EXT="docx" ;;
  pdf-to-excel)   SRC_EXTS=("pdf") TARGET_EXT="xlsx" ;;
  pdf-to-ppt)     SRC_EXTS=("pdf") TARGET_EXT="pptx" ;;
  pdf-to-image)   SRC_EXTS=("pdf") TARGET_EXT="zip" ;;
  word-to-pdf)    SRC_EXTS=("docx" "doc") TARGET_EXT="pdf" ;;
  word-to-image)  SRC_EXTS=("docx" "doc") TARGET_EXT="zip" ;;
  excel-to-pdf)   SRC_EXTS=("xlsx" "xls") TARGET_EXT="pdf" ;;
  image-to-pdf)   SRC_EXTS=("jpg" "jpeg" "png" "bmp") TARGET_EXT="pdf" ;;
  image-to-word)  SRC_EXTS=("jpg" "jpeg" "png" "bmp") TARGET_EXT="docx" ;;
  *)
    echo "Error: Unknown conversion type '$CONVERSION_TYPE'" >&2
    exit 1
    ;;
esac

# Collect matching files (non-recursive, case-insensitive match)
FILES=()
for ext in "${SRC_EXTS[@]}"; do
  while IFS= read -r -d '' file; do
    FILES+=("$file")
  done < <(find "$INPUT_DIR" -maxdepth 1 -type f -iname "*.${ext}" -print0 | sort -z)
done

TOTAL=${#FILES[@]}
if [[ $TOTAL -eq 0 ]]; then
  echo "No matching files found in $INPUT_DIR for conversion type $CONVERSION_TYPE"
  echo "Expected source extensions: ${SRC_EXTS[*]}"
  exit 0
fi

echo "============================================"
echo "Batch Conversion: $CONVERSION_TYPE"
echo "Input directory:  $INPUT_DIR"
echo "Output directory: $OUTPUT_DIR"
echo "Files found:      $TOTAL"
echo "============================================"
echo ""

SUCCESS=0
FAILED=0
FAILED_FILES=()

for i in "${!FILES[@]}"; do
  INPUT_FILE="${FILES[$i]}"
  BASENAME="$(basename "$INPUT_FILE")"
  NAME_NO_EXT="${BASENAME%.*}"

  # Determine output path, avoid overwriting
  OUTPUT_FILE="$OUTPUT_DIR/${NAME_NO_EXT}.${TARGET_EXT}"
  if [[ -f "$OUTPUT_FILE" ]]; then
    COUNTER=1
    while [[ -f "$OUTPUT_DIR/${NAME_NO_EXT}_${COUNTER}.${TARGET_EXT}" ]]; do
      ((COUNTER++))
    done
    OUTPUT_FILE="$OUTPUT_DIR/${NAME_NO_EXT}_${COUNTER}.${TARGET_EXT}"
  fi

  echo "[$((i+1))/$TOTAL] Converting: $BASENAME"

  if bash "$CONVERT_SCRIPT" "$CONVERSION_TYPE" "$INPUT_FILE" "$OUTPUT_FILE" 2>&1; then
    ((SUCCESS++))
  else
    ((FAILED++))
    FAILED_FILES+=("$BASENAME")
    echo "  FAILED: $BASENAME"
  fi
  echo ""
done

echo "============================================"
echo "Batch Conversion Complete"
echo "  Total:     $TOTAL"
echo "  Succeeded: $SUCCESS"
echo "  Failed:    $FAILED"
if [[ $FAILED -gt 0 ]]; then
  echo "  Failed files:"
  for f in "${FAILED_FILES[@]}"; do
    echo "    - $f"
  done
fi
echo "  Output:    $OUTPUT_DIR"
echo "============================================"
