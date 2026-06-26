#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

VERBOSE=0
ROOT=".agents"
ROOT_SET=0
ALLOWLIST="${ARTIFACT_CONSISTENCY_ALLOWLIST:-$SCRIPT_DIR/../references/artifact-consistency-allowlist.txt}"

usage() {
  cat <<EOF
Usage: $(basename "$0") [--verbose] [--allowlist <path> | --no-allowlist] [ROOT]

Scans markdown files for .agents artifact references and reports consistency.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --verbose)
      VERBOSE=1
      shift
      ;;
    --allowlist)
      if [[ $# -lt 2 ]]; then
        echo "ERROR: --allowlist requires a path" >&2
        exit 2
      fi
      ALLOWLIST="$2"
      shift 2
      ;;
    --no-allowlist)
      ALLOWLIST=""
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    --*)
      echo "ERROR: unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
    *)
      if (( ROOT_SET )); then
        echo "ERROR: unexpected argument: $1" >&2
        usage >&2
        exit 2
      fi
      ROOT="$1"
      ROOT_SET=1
      shift
      ;;
  esac
done

trim() {
  sed -E 's/^[[:space:]]+//; s/[[:space:]]+$//'
}

declare -a ALLOW_SOURCE_PATTERNS=()
declare -a ALLOW_TARGET_PATTERNS=()

if [[ -n "$ALLOWLIST" ]]; then
  if [[ ! -f "$ALLOWLIST" ]]; then
    echo "ERROR: allowlist not found: $ALLOWLIST" >&2
    exit 2
  fi

  while IFS= read -r raw_line || [[ -n "$raw_line" ]]; do
    line="$(printf '%s' "$raw_line" | trim)"
    [[ -z "$line" || "$line" == \#* ]] && continue

    source_pattern="*"
    target_pattern="$line"
    if [[ "$line" == *"->"* ]]; then
      source_pattern="$(printf '%s' "${line%%->*}" | trim)"
      target_pattern="$(printf '%s' "${line#*->}" | trim)"
    fi

    [[ -z "$source_pattern" || -z "$target_pattern" ]] && continue
    ALLOW_SOURCE_PATTERNS+=("$source_pattern")
    ALLOW_TARGET_PATTERNS+=("$target_pattern")
  done < "$ALLOWLIST"
fi

is_allowlisted() {
  local source_file="$1"
  local target_ref="$2"
  local i

  for i in "${!ALLOW_SOURCE_PATTERNS[@]}"; do
    if [[ "$source_file" == ${ALLOW_SOURCE_PATTERNS[$i]} ]] \
      && [[ "$target_ref" == ${ALLOW_TARGET_PATTERNS[$i]} ]]; then
      return 0
    fi
  done

  return 1
}

if [[ ! -d "$ROOT" ]]; then
  echo "TOTAL_REFS=0"
  echo "BROKEN_REFS=0"
  echo "CONSISTENCY=100"
  echo "STATUS=Healthy"
  exit 0
fi

total_refs=0
broken_refs=0
broken_lines=()

# Scan markdown while excluding ao telemetry/session data.
while IFS= read -r -d '' file; do
  # Strip fenced code blocks to avoid counting template snippets as broken links.
  refs=$(awk '
    BEGIN { in_code=0 }
    /^```/ { in_code=!in_code; next }
    in_code { next }
    {
      line=$0
      while (match(line, /\.agents\/[A-Za-z0-9._\/-]+\.(md|json|jsonl)/)) {
        print substr(line, RSTART, RLENGTH)
        line = substr(line, RSTART + RLENGTH)
      }
    }
  ' "$file" | sort -u)

  while IFS= read -r ref; do
    [[ -z "$ref" ]] && continue

    # Skip template placeholders and non-literal paths.
    if [[ "$ref" =~ YYYY|\<|\>|\{|\}|\*|\.{3} ]]; then
      continue
    fi

    total_refs=$((total_refs + 1))

    # Normalize leading ./, then check relative to repo root.
    normalized="${ref#./}"
    if [[ ! -f "$normalized" ]]; then
      if is_allowlisted "$file" "$normalized"; then
        continue
      fi
      broken_refs=$((broken_refs + 1))
      if (( VERBOSE )); then
        broken_lines+=("$file -> $normalized")
      fi
    fi
  done <<< "$refs"
done < <(find "$ROOT" -type f -name "*.md" -not -path "$ROOT/ao/*" -print0)

if (( total_refs > 0 )); then
  consistency=$(( (total_refs - broken_refs) * 100 / total_refs ))
else
  consistency=100
fi

status="Critical"
if (( consistency > 90 )); then
  status="Healthy"
elif (( consistency >= 70 )); then
  status="Warning"
fi

echo "TOTAL_REFS=$total_refs"
echo "BROKEN_REFS=$broken_refs"
echo "CONSISTENCY=$consistency"
echo "STATUS=$status"

if (( VERBOSE )) && (( broken_refs > 0 )); then
  for line in "${broken_lines[@]}"; do
    echo "BROKEN_REF=$line"
  done
fi
