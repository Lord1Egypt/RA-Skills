#!/usr/bin/env bash
set -euo pipefail

# Publish this skill to ClawHub.
# Example:
#   ./scripts/publish_clawhub.sh --version 1.0.0 --changelog "Initial release" --tags latest,remotion

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
DEFAULT_SLUG="$(basename "$SKILL_DIR")"

SLUG="$DEFAULT_SLUG"
NAME="Shellbot Product Video"
VERSION=""
CHANGELOG=""
TAGS="latest"
DRY_RUN=false

usage() {
  cat <<'EOF'
Usage:
  ./scripts/publish_clawhub.sh --version <semver> [options]

Options:
  --slug <slug>           Skill slug (default: folder name)
  --name <name>           Display name (default: "Shellbot Product Video")
  --version <semver>      Required semver version (for example 1.0.0)
  --changelog <text>      Changelog text
  --tags <csv>            Comma-separated tags (default: latest)
  --dry-run               Print command only
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --slug)
      SLUG="$2"
      shift 2
      ;;
    --name)
      NAME="$2"
      shift 2
      ;;
    --version)
      VERSION="$2"
      shift 2
      ;;
    --changelog)
      CHANGELOG="$2"
      shift 2
      ;;
    --tags)
      TAGS="$2"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ -z "$VERSION" ]]; then
  echo "--version is required" >&2
  usage >&2
  exit 1
fi

CMD=(
  clawhub publish "$SKILL_DIR"
  --slug "$SLUG"
  --name "$NAME"
  --version "$VERSION"
  --changelog "$CHANGELOG"
  --tags "$TAGS"
)

if [[ "$DRY_RUN" == true ]]; then
  printf '%q ' "${CMD[@]}"
  printf '\n'
  exit 0
fi

if ! command -v clawhub >/dev/null 2>&1; then
  echo "clawhub CLI not found. Install with: npm i -g clawhub" >&2
  exit 1
fi

"${CMD[@]}"
