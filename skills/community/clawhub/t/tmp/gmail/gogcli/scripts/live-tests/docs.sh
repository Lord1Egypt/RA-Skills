#!/usr/bin/env bash

set -euo pipefail

run_docs_tests() {
  if skip "docs"; then
    echo "==> docs (skipped)"
    return 0
  fi

  local doc_json doc_id copy_json copy_id export_path
  doc_json=$(gog docs create "gogcli-smoke-doc-$TS" --json)
  doc_id=$(extract_id "$doc_json")
  [ -n "$doc_id" ] || { echo "Failed to parse doc id" >&2; exit 1; }

  run_required "docs" "docs info" gog docs info "$doc_id" --json >/dev/null
  run_required "docs" "docs cat" gog docs cat "$doc_id" >/dev/null

  export_path="$LIVE_TMP/docs-export-$TS.pdf"
  run_required "docs" "docs export" gog docs export "$doc_id" --format pdf --out "$export_path" >/dev/null

  copy_json=$(gog docs copy "$doc_id" "gogcli-smoke-doc-copy-$TS" --json)
  copy_id=$(extract_id "$copy_json")
  [ -n "$copy_id" ] || { echo "Failed to parse doc copy id" >&2; exit 1; }

  run_required "docs" "drive delete doc copy" gog drive delete "$copy_id" --force >/dev/null
  run_required "docs" "drive delete doc" gog drive delete "$doc_id" --force >/dev/null
}
