#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${LX_AGENT_ROOT:-$(pwd)}"

if [[ $# -lt 1 ]]; then
  echo "Usage: run-lx-agent-cli.sh <command> [args...]" >&2
  echo "Example: run-lx-agent-cli.sh config" >&2
  exit 2
fi

if [[ ! -f "$ROOT_DIR/go.mod" || ! -d "$ROOT_DIR/cmd/lx-agent" ]]; then
  echo "LX_AGENT_ROOT does not look like an lx-agent repo: $ROOT_DIR" >&2
  exit 1
fi

cmd="$1"
shift || true

cd "$ROOT_DIR"
go run ./cmd/lx-agent "$cmd" "$@"
