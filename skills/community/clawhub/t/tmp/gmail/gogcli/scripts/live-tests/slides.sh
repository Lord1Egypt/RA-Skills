#!/usr/bin/env bash

set -euo pipefail

run_slides_tests() {
  if skip "slides"; then
    echo "==> slides (skipped)"
    return 0
  fi

  local slides_json slides_id copy_json copy_id export_path
  slides_json=$(gog slides create "gogcli-smoke-slides-$TS" --json)
  slides_id=$(extract_id "$slides_json")
  [ -n "$slides_id" ] || { echo "Failed to parse slides id" >&2; exit 1; }

  run_required "slides" "slides info" gog slides info "$slides_id" --json >/dev/null

  export_path="$LIVE_TMP/slides-export-$TS.pdf"
  run_required "slides" "slides export" gog slides export "$slides_id" --format pdf --out "$export_path" >/dev/null

  copy_json=$(gog slides copy "$slides_id" "gogcli-smoke-slides-copy-$TS" --json)
  copy_id=$(extract_id "$copy_json")
  [ -n "$copy_id" ] || { echo "Failed to parse slides copy id" >&2; exit 1; }

  run_required "slides" "drive delete slides copy" gog drive delete "$copy_id" --force >/dev/null
  run_required "slides" "drive delete slides" gog drive delete "$slides_id" --force >/dev/null
}
