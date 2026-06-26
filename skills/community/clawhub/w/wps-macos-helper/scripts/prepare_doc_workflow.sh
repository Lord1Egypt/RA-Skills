#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: prepare_doc_workflow.sh <input-file> [output-md]" >&2
  exit 1
fi

INPUT="$1"
OUTPUT="${2:-}"
EXT="${INPUT##*.}"
EXT_LOWER="$(printf '%s' "$EXT" | tr '[:upper:]' '[:lower:]')"

case "$EXT_LOWER" in
  md)
    echo "Source is Markdown. Recommended route: clean content -> convert to docx if editable office output is needed -> open in WPS for final check."
    if [ -n "$OUTPUT" ]; then
      echo "Note: Markdown input does not need markitdown. Use a dedicated Markdown-to-docx step for office editing output."
      printf '%s\n' "Recommended next step: convert '$INPUT' into docx, then open that docx in WPS on macOS for layout review." > "$OUTPUT"
      echo "Wrote workflow note: $OUTPUT"
    fi
    ;;
  docx|pdf|pptx|xlsx|xls)
    echo "Recommended route: convert source to Markdown for analysis first, then rebuild or polish in docx/WPS as needed."
    if [ -n "$OUTPUT" ]; then
      if command -v uvx >/dev/null 2>&1; then
        echo "Running: uvx --from 'markitdown[all]' markitdown '$INPUT' -o '$OUTPUT'"
        uvx --from 'markitdown[all]' markitdown "$INPUT" -o "$OUTPUT"
        echo "Done: $OUTPUT"
        echo "Next step: inspect the Markdown structure, repair headings/tables if needed, then decide whether to rebuild as docx for WPS."
      else
        echo "uvx is not installed in the current environment. Cannot auto-convert right now."
        printf '%s\n' "Auto-conversion unavailable: install uv/uvx first, then rerun this step for '$INPUT'. Recommended route: convert to Markdown -> inspect structure -> rebuild as docx if WPS editing is needed." > "$OUTPUT"
        echo "Wrote fallback workflow note: $OUTPUT"
      fi
    else
      echo "Tip: pass an output .md path to run conversion automatically."
    fi
    ;;
  *)
    echo "Unknown or less common format. Safest route: inspect file type, convert to Markdown if supported, then decide whether WPS should be the final editing step."
    ;;
esac
