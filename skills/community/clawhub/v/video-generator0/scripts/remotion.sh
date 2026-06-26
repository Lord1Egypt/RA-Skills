#!/usr/bin/env bash
set -euo pipefail

CMD="${1:-help}"
shift || true

case "$CMD" in
  init)
    PROJECT_NAME="${1:?init <name>}"
    npx --yes create-video@latest "$PROJECT_NAME"
    ;;

  preview)
    cd "${1:?project-dir}"
    npm run dev
    ;;

  render)
    cd "${1:?project-dir}"
    shift
    npx remotion render "$@"
    ;;

  *)
    echo "Commands: init, preview, render"
    ;;
esac
