#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# sort — File & Text Sorting Tool
# Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
###############################################################################

BRAND="Powered by BytesAgain | bytesagain.com | hello@bytesagain.com"
DATA_DIR="${HOME}/.local/share/sort"
HISTORY_FILE="${DATA_DIR}/history.log"

mkdir -p "${DATA_DIR}"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
die()  { echo "ERROR: $*" >&2; exit 1; }
info() { echo "▸ $*"; }

usage() {
  cat <<'EOF'
sort — File & Text Sorting Tool

USAGE
  script.sh <command> [arguments...]

COMMANDS
  lines   <file> [-r] [-n] [-u]    Sort lines (flags: -r reverse, -n numeric, -u unique)
  csv     <file> <column>           Sort CSV file by column number (1-based)
  json    <file> <key>              Sort JSON array by a key
  dedup   <file>                    Remove duplicate lines (preserving order)
  shuffle <file>                    Randomly shuffle lines
  rank    <file> <column>           Rank/sort tabular data by a numeric column
  top     <file> <column> [n]       Show top N entries by column value
  freq    <file>                    Frequency analysis — count occurrences of each line
  stats   <file>                    Show basic stats about the file content

EOF
  echo "${BRAND}"
}

log_operation() {
  local op="$1" detail="$2"
  echo "$(date -u '+%Y-%m-%dT%H:%M:%SZ') ${op} ${detail}" >> "${HISTORY_FILE}"
}

count_lines() {
  wc -l < "$1" | tr -d ' '
}

# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

cmd_lines() {
  local file="" reverse=false numeric=false unique=false
  local sort_flags=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      -r|--reverse)  reverse=true; shift ;;
      -n|--numeric)  numeric=true; shift ;;
      -u|--unique)   unique=true; shift ;;
      -*)            die "Unknown flag: $1" ;;
      *)
        if [[ -z "${file}" ]]; then
          file="$1"
        else
          die "Unexpected argument: $1"
        fi
        shift
        ;;
    esac
  done

  [[ -z "${file}" ]] && die "Usage: lines <file> [-r] [-n] [-u]"
  [[ -f "${file}" ]] || die "File not found: ${file}"

  # Build sort flags
  ${reverse} && sort_flags="${sort_flags} -r"
  ${numeric} && sort_flags="${sort_flags} -n"
  ${unique}  && sort_flags="${sort_flags} -u"

  local original_count sorted_count
  original_count=$(count_lines "${file}")

  info "Sorting ${file} (${original_count} lines)"
  [[ -n "${sort_flags}" ]] && info "Flags:${sort_flags}"
  echo ""

  local output
  # shellcheck disable=SC2086
  output=$(sort ${sort_flags} "${file}")
  sorted_count=$(echo "${output}" | wc -l | tr -d ' ')

  echo "${output}"
  echo ""
  info "Input: ${original_count} lines → Output: ${sorted_count} lines"

  if ${unique}; then
    local removed=$((original_count - sorted_count))
    info "Duplicates removed: ${removed}"
  fi

  log_operation "lines" "file=${file} flags=${sort_flags} lines=${original_count}"
}

cmd_csv() {
  [[ $# -lt 2 ]] && die "Usage: csv <file> <column_number>"
  local file="$1" col="$2"
  [[ -f "${file}" ]] || die "File not found: ${file}"
  [[ "${col}" =~ ^[0-9]+$ ]] || die "Column must be a number, got: ${col}"
  [[ "${col}" -ge 1 ]] || die "Column number must be >= 1"

  # Detect delimiter
  local delim=","
  local first_line
  first_line=$(head -1 "${file}")
  if echo "${first_line}" | grep -q $'\t'; then
    local tab_count comma_count
    tab_count=$(echo "${first_line}" | tr -cd '\t' | wc -c)
    comma_count=$(echo "${first_line}" | tr -cd ',' | wc -c)
    if (( tab_count > comma_count )); then
      delim=$'\t'
      info "Detected tab-delimited format"
    fi
  fi

  local total_cols
  total_cols=$(echo "${first_line}" | awk -F"${delim}" '{print NF}')
  (( col > total_cols )) && die "Column ${col} exceeds total columns (${total_cols})"

  local total_lines
  total_lines=$(count_lines "${file}")
  info "Sorting CSV: ${file} (${total_lines} lines, ${total_cols} columns) by column ${col}"
  echo ""

  # Print header (first line) then sort the rest
  head -1 "${file}"
  tail -n +2 "${file}" | sort -t"${delim}" -k"${col},${col}" --stable

  echo ""
  info "Sorted ${total_lines} rows by column ${col}"
  log_operation "csv" "file=${file} col=${col} rows=${total_lines}"
}

cmd_csv_numeric() {
  [[ $# -lt 2 ]] && die "Usage: csv <file> <column_number>"
  local file="$1" col="$2"
  [[ -f "${file}" ]] || die "File not found: ${file}"

  local delim=","
  head -1 "${file}"
  tail -n +2 "${file}" | sort -t"${delim}" -k"${col},${col}" -n --stable
}

cmd_json() {
  [[ $# -lt 2 ]] && die "Usage: json <file> <key>"
  local file="$1" key="$2"
  [[ -f "${file}" ]] || die "File not found: ${file}"

  # Check if jq is available
  if command -v jq &>/dev/null; then
    info "Sorting JSON array by key: .${key}"
    echo ""
    jq --arg k "${key}" 'sort_by(.[$k])' "${file}"
    local count
    count=$(jq 'length' "${file}")
    echo ""
    info "Sorted ${count} entries by '${key}'"
    log_operation "json" "file=${file} key=${key} entries=${count}"
  else
    # Fallback: basic python json sort if available
    if command -v python3 &>/dev/null; then
      info "Sorting JSON array by key: .${key} (using python3 fallback)"
      echo ""
      python3 -c "
import json, sys
with open('${file}') as f:
    data = json.load(f)
if not isinstance(data, list):
    print('ERROR: JSON root must be an array', file=sys.stderr)
    sys.exit(1)
data.sort(key=lambda x: x.get('${key}', ''))
print(json.dumps(data, indent=2, ensure_ascii=False))
print(f'\n▸ Sorted {len(data)} entries by \"${key}\"', file=sys.stderr)
"
    else
      die "Neither jq nor python3 available for JSON sorting"
    fi
    log_operation "json" "file=${file} key=${key}"
  fi
}

cmd_dedup() {
  [[ $# -lt 1 ]] && die "Usage: dedup <file>"
  local file="$1"
  [[ -f "${file}" ]] || die "File not found: ${file}"

  local original_count
  original_count=$(count_lines "${file}")

  info "Removing duplicates from ${file} (preserving order)..."
  echo ""

  local output
  output=$(awk '!seen[$0]++' "${file}")
  local deduped_count
  deduped_count=$(echo "${output}" | wc -l | tr -d ' ')
  local removed=$((original_count - deduped_count))

  echo "${output}"
  echo ""
  info "Original: ${original_count} lines"
  info "After dedup: ${deduped_count} lines"
  info "Removed: ${removed} duplicates"
  log_operation "dedup" "file=${file} original=${original_count} deduped=${deduped_count} removed=${removed}"
}

cmd_shuffle() {
  [[ $# -lt 1 ]] && die "Usage: shuffle <file>"
  local file="$1"
  [[ -f "${file}" ]] || die "File not found: ${file}"

  local line_count
  line_count=$(count_lines "${file}")
  info "Shuffling ${file} (${line_count} lines)..."
  echo ""

  if command -v shuf &>/dev/null; then
    shuf "${file}"
  else
    # Fallback: awk-based shuffle
    awk 'BEGIN{srand()}{print rand()"\t"$0}' "${file}" | sort -n | cut -f2-
  fi

  echo ""
  info "Shuffled ${line_count} lines"
  log_operation "shuffle" "file=${file} lines=${line_count}"
}

cmd_rank() {
  [[ $# -lt 2 ]] && die "Usage: rank <file> <column_number>"
  local file="$1" col="$2"
  [[ -f "${file}" ]] || die "File not found: ${file}"
  [[ "${col}" =~ ^[0-9]+$ ]] || die "Column must be a number"

  local line_count
  line_count=$(count_lines "${file}")
  info "Ranking ${file} by column ${col} (numeric descending)..."
  echo ""

  # Print header
  local has_header=false
  local first_line
  first_line=$(head -1 "${file}")
  # Heuristic: if first line contains letters, treat as header
  if echo "${first_line}" | grep -qE '[a-zA-Z]'; then
    has_header=true
    echo "RANK  ${first_line}"
    echo "----  $(echo "${first_line}" | sed 's/./-/g')"
    local rank=1
    tail -n +2 "${file}" | sort -k"${col},${col}" -rn --stable | while IFS= read -r line; do
      printf "%-4d  %s\n" "${rank}" "${line}"
      rank=$((rank + 1))
    done
  else
    local rank=1
    sort -k"${col},${col}" -rn --stable "${file}" | while IFS= read -r line; do
      printf "%-4d  %s\n" "${rank}" "${line}"
      rank=$((rank + 1))
    done
  fi

  echo ""
  info "Ranked ${line_count} entries by column ${col}"
  log_operation "rank" "file=${file} col=${col} lines=${line_count}"
}

cmd_top() {
  [[ $# -lt 2 ]] && die "Usage: top <file> <column> [n]"
  local file="$1" col="$2" n="${3:-10}"
  [[ -f "${file}" ]] || die "File not found: ${file}"
  [[ "${col}" =~ ^[0-9]+$ ]] || die "Column must be a number"
  [[ "${n}" =~ ^[0-9]+$ ]] || die "Count must be a number"

  info "Top ${n} entries from ${file} by column ${col}..."
  echo ""

  local first_line
  first_line=$(head -1 "${file}")
  if echo "${first_line}" | grep -qE '[a-zA-Z]'; then
    echo "${first_line}"
    echo "${first_line}" | sed 's/./-/g'
    tail -n +2 "${file}" | sort -k"${col},${col}" -rn --stable | head -n "${n}"
  else
    sort -k"${col},${col}" -rn --stable "${file}" | head -n "${n}"
  fi

  echo ""
  info "Showing top ${n} by column ${col}"
  log_operation "top" "file=${file} col=${col} n=${n}"
}

cmd_freq() {
  [[ $# -lt 1 ]] && die "Usage: freq <file>"
  local file="$1"
  [[ -f "${file}" ]] || die "File not found: ${file}"

  local line_count
  line_count=$(count_lines "${file}")
  info "Frequency analysis of ${file} (${line_count} lines)..."
  echo ""

  printf "%-8s  %s\n" "COUNT" "VALUE"
  printf "%-8s  %s\n" "--------" "-----"
  sort "${file}" | uniq -c | sort -rn | while read -r count value; do
    printf "%-8d  %s\n" "${count}" "${value}"
  done

  local unique_count
  unique_count=$(sort -u "${file}" | wc -l | tr -d ' ')
  echo ""
  info "Total lines: ${line_count} | Unique values: ${unique_count}"
  log_operation "freq" "file=${file} lines=${line_count} unique=${unique_count}"
}

cmd_stats() {
  [[ $# -lt 1 ]] && die "Usage: stats <file>"
  local file="$1"
  [[ -f "${file}" ]] || die "File not found: ${file}"

  local line_count word_count char_count byte_count unique_count empty_count longest shortest
  line_count=$(wc -l < "${file}" | tr -d ' ')
  word_count=$(wc -w < "${file}" | tr -d ' ')
  char_count=$(wc -m < "${file}" | tr -d ' ')
  byte_count=$(wc -c < "${file}" | tr -d ' ')
  unique_count=$(sort -u "${file}" | wc -l | tr -d ' ')
  empty_count=$(grep -c '^$' "${file}" || true)
  longest=$(awk '{print length}' "${file}" | sort -rn | head -1)
  shortest=$(awk 'NF{print length}' "${file}" | sort -n | head -1)

  echo "File Statistics: ${file}"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "Lines         : ${line_count}"
  echo "Words         : ${word_count}"
  echo "Characters    : ${char_count}"
  echo "Bytes         : ${byte_count}"
  echo "Unique lines  : ${unique_count}"
  echo "Duplicate lines: $((line_count - unique_count))"
  echo "Empty lines   : ${empty_count}"
  echo "Longest line  : ${longest:-0} chars"
  echo "Shortest line : ${shortest:-0} chars"
  echo ""

  # Check if content looks numeric
  local numeric_lines
  numeric_lines=$(grep -cE '^[[:space:]]*-?[0-9]+\.?[0-9]*[[:space:]]*$' "${file}" || true)
  if (( numeric_lines > 0 )); then
    echo "Numeric Content (${numeric_lines} numeric lines detected):"
    local nums
    nums=$(grep -E '^[[:space:]]*-?[0-9]+\.?[0-9]*[[:space:]]*$' "${file}" | sort -n)
    local min max
    min=$(echo "${nums}" | head -1 | tr -d ' ')
    max=$(echo "${nums}" | tail -1 | tr -d ' ')
    local sum
    sum=$(echo "${nums}" | awk '{s+=$1}END{printf "%.2f", s}')
    local avg
    avg=$(echo "${nums}" | awk '{s+=$1}END{printf "%.2f", s/NR}')
    echo "  Min         : ${min}"
    echo "  Max         : ${max}"
    echo "  Sum         : ${sum}"
    echo "  Average     : ${avg}"
  fi

  log_operation "stats" "file=${file} lines=${line_count}"
}

# ---------------------------------------------------------------------------
# Main dispatch
# ---------------------------------------------------------------------------
main() {
  if [[ $# -lt 1 ]]; then
    usage
    exit 0
  fi

  local cmd="$1"
  shift

  case "${cmd}" in
    lines)   cmd_lines "$@" ;;
    csv)     cmd_csv "$@" ;;
    json)    cmd_json "$@" ;;
    dedup)   cmd_dedup "$@" ;;
    shuffle) cmd_shuffle "$@" ;;
    rank)    cmd_rank "$@" ;;
    top)     cmd_top "$@" ;;
    freq)    cmd_freq "$@" ;;
    stats)   cmd_stats "$@" ;;
    help|--help|-h) usage ;;
    *)       die "Unknown command: ${cmd}. Run with 'help' for usage." ;;
  esac
}

main "$@"
