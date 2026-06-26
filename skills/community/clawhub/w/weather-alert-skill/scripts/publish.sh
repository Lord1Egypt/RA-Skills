#!/usr/bin/env bash
set -euo pipefail

mode="${1:-}"

version="$(grep '"version"' package.json | head -1 | sed -E 's/.*"version": "([^"]+)".*/\1/')"
skill_version="$(grep '^version:' skill.yaml | head -1 | awk '{print $2}')"

if [[ "$version" != "$skill_version" ]]; then
  echo "version mismatch between package.json ($version) and skill.yaml ($skill_version)" >&2
  exit 1
fi

if ! grep -q '^id:' skill.yaml; then
  echo "skill definition is missing an id" >&2
  exit 1
fi

if [[ "$mode" == "--dry-run" ]]; then
  echo "dry-run: would publish weather-alert-skill@$version"
else
  echo "publishing weather-alert-skill@$version"
fi
