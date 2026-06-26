#!/usr/bin/env bash

set -u

TARGET=""
RUN_ALL=false
RUN_STALE=false
RUN_ORPHANS=false
RUN_STRUCTURE=false
RUN_ARCHIVE=false
RUN_PROJECT_HEALTH=false

CRITICAL=()
WARNING=()
INFO=()
CHECKED=0

usage() {
  cat <<'EOF'
Usage:
  scripts/validate.sh [path] [--all] [--stale] [--orphans] [--structure] [--archive-candidates] [--project-health]

Notes:
  - If path is omitted, current working directory is used.
  - Folder assumptions follow PARA structure:
    00_INBOX, 10_PROJECTS, 20_AREAS, 30_RESOURCES, 40_ARCHIVE
EOF
}

add_issue() {
  local severity="$1"
  local message="$2"
  local action="$3"
  local line="- ${message} | Action: ${action}"
  case "$severity" in
    CRITICAL) CRITICAL+=("$line") ;;
    WARNING) WARNING+=("$line") ;;
    INFO) INFO+=("$line") ;;
  esac
}

is_darwin() {
  [[ "$(uname -s)" == "Darwin" ]]
}

get_mtime_epoch() {
  local p="$1"
  if is_darwin; then
    stat -f %m "$p" 2>/dev/null
  else
    stat -c %Y "$p" 2>/dev/null
  fi
}

format_date_epoch() {
  local epoch="$1"
  if is_darwin; then
    date -r "$epoch" +%Y-%m-%d
  else
    date -d "@${epoch}" +%Y-%m-%d
  fi
}

to_lower() {
  printf '%s' "$1" | tr '[:upper:]' '[:lower:]'
}

normalize_name() {
  printf '%s' "$1" | tr '[:upper:]' '[:lower:]' | tr '_ ' '-' 
}

parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --help|-h)
        usage
        exit 0
        ;;
      --all)
        RUN_ALL=true
        ;;
      --stale)
        RUN_STALE=true
        ;;
      --orphans)
        RUN_ORPHANS=true
        ;;
      --structure)
        RUN_STRUCTURE=true
        ;;
      --archive-candidates)
        RUN_ARCHIVE=true
        ;;
      --project-health)
        RUN_PROJECT_HEALTH=true
        ;;
      --*)
        echo "Unknown flag: $1" >&2
        usage >&2
        exit 2
        ;;
      *)
        if [[ -z "$TARGET" ]]; then
          TARGET="$1"
        else
          echo "Unexpected argument: $1" >&2
          usage >&2
          exit 2
        fi
        ;;
    esac
    shift
  done

  if [[ -z "$TARGET" ]]; then
    TARGET="$(pwd)"
  fi

  if [[ "$RUN_ALL" == false && "$RUN_STALE" == false && "$RUN_ORPHANS" == false && "$RUN_STRUCTURE" == false && "$RUN_ARCHIVE" == false && "$RUN_PROJECT_HEALTH" == false ]]; then
    RUN_ALL=true
  fi

  if [[ "$RUN_ALL" == true ]]; then
    RUN_STALE=true
    RUN_ORPHANS=true
    RUN_STRUCTURE=true
    RUN_ARCHIVE=true
    RUN_PROJECT_HEALTH=true
  fi
}

check_structure() {
  local required=("00_INBOX" "10_PROJECTS" "20_AREAS" "30_RESOURCES" "40_ARCHIVE")
  local p
  for p in "${required[@]}"; do
    CHECKED=$((CHECKED + 1))
    if [[ ! -d "$TARGET/$p" ]]; then
      add_issue "CRITICAL" "Missing required folder: $p" "mkdir -p '$TARGET/$p'"
    fi
  done

  local project_subs=("Active" "On Hold" "Completed")
  for p in "${project_subs[@]}"; do
    CHECKED=$((CHECKED + 1))
    if [[ ! -d "$TARGET/10_PROJECTS/$p" ]]; then
      add_issue "CRITICAL" "Missing required projects subfolder: 10_PROJECTS/$p" "mkdir -p '$TARGET/10_PROJECTS/$p'"
    fi
  done

  local archive_subs=("Projects" "Areas" "Resources")
  for p in "${archive_subs[@]}"; do
    CHECKED=$((CHECKED + 1))
    if [[ ! -d "$TARGET/40_ARCHIVE/$p" ]]; then
      add_issue "CRITICAL" "Missing required archive subfolder: 40_ARCHIVE/$p" "mkdir -p '$TARGET/40_ARCHIVE/$p'"
    fi
  done
}

check_project_health() {
  local active="$TARGET/10_PROJECTS/Active"
  [[ -d "$active" ]] || return 0

  local project
  for project in "$active"/*; do
    [[ -d "$project" ]] || continue
    CHECKED=$((CHECKED + 1))
    local agents="$project/AGENTS.md"
    if [[ ! -f "$agents" ]]; then
      add_issue "CRITICAL" "Missing AGENTS.md in active project: $project" "Create '$agents' with outcome, timeline, and task list"
      continue
    fi

    if ! grep -Eiq 'outcome|goal' "$agents"; then
      add_issue "CRITICAL" "AGENTS.md missing outcome statement: $agents" "Add a clear project outcome section"
    fi
    if ! grep -Eiq 'due|timeline|target date|deadline' "$agents"; then
      add_issue "CRITICAL" "AGENTS.md missing due date/timeline: $agents" "Add due date or timeline in AGENTS.md"
    fi
    if ! grep -Eiq '^#+[[:space:]]*tasks|^- \[[ xX]\]' "$agents"; then
      add_issue "CRITICAL" "AGENTS.md missing task list section: $agents" "Add a Tasks section or checkbox list in AGENTS.md"
    fi
  done
}

check_stale_projects() {
  local active="$TARGET/10_PROJECTS/Active"
  [[ -d "$active" ]] || return 0
  local now
  now="$(date +%s)"

  local project
  for project in "$active"/*; do
    [[ -d "$project" ]] || continue
    CHECKED=$((CHECKED + 1))

    local newest=0
    while IFS= read -r f; do
      local mt
      mt="$(get_mtime_epoch "$f")"
      [[ -n "$mt" ]] || continue
      if (( mt > newest )); then
        newest=$mt
      fi
    done < <(find "$project" -type f 2>/dev/null)

    if (( newest == 0 )); then
      newest="$(get_mtime_epoch "$project")"
      newest="${newest:-0}"
    fi

    local age_days=$(( (now - newest) / 86400 ))
    if (( age_days >= 30 )); then
      local lm
      lm="$(format_date_epoch "$newest")"
      local suggestion="activate or delete"
      if [[ -f "$project/AGENTS.md" ]] && grep -Eiq 'status:[[:space:]]*complete|completion date|completed on' "$project/AGENTS.md"; then
        suggestion="archive"
      fi
      add_issue "WARNING" "Stale project (${age_days} days inactive, last modified ${lm}): $project" "Suggested action: ${suggestion}"
    fi
  done
}

check_orphans() {
  local roots=("10_PROJECTS" "20_AREAS" "30_RESOURCES" "40_ARCHIVE")
  local r
  for r in "${roots[@]}"; do
    [[ -d "$TARGET/$r" ]] || continue
    while IFS= read -r f; do
      CHECKED=$((CHECKED + 1))
      add_issue "INFO" "Top-level file in $r (not in subfolder): $f" "Move file into an appropriate child folder under $r"
    done < <(find "$TARGET/$r" -maxdepth 1 -type f 2>/dev/null)
  done

  local active="$TARGET/10_PROJECTS/Active"
  local areas="$TARGET/20_AREAS"
  [[ -d "$active" && -d "$areas" ]] || return 0

  local names=()
  local p
  for p in "$active"/*; do
    [[ -d "$p" ]] || continue
    names+=("$(normalize_name "$(basename "$p")")|$(basename "$p")")
  done

  local af
  while IFS= read -r af; do
    local base
    base="$(basename "$af")"
    base="${base%.*}"
    local nbase
    nbase="$(normalize_name "$base")"

    local entry
    for entry in "${names[@]}"; do
      local key="${entry%%|*}"
      local real="${entry#*|}"
      if [[ "$nbase" == *"$key"* ]]; then
        CHECKED=$((CHECKED + 1))
        add_issue "INFO" "Area file appears project-specific by name match ('$real'): $af" "Consider moving to '$TARGET/10_PROJECTS/Active/$real/'"
        break
      fi
    done
  done < <(find "$areas" -type f 2>/dev/null)
}

check_archive_candidates() {
  local completed="$TARGET/10_PROJECTS/Completed"
  local archived_projects="$TARGET/40_ARCHIVE/Projects"

  if [[ -d "$completed" ]]; then
    local p
    for p in "$completed"/*; do
      [[ -d "$p" ]] || continue
      CHECKED=$((CHECKED + 1))
      local bn
      bn="$(basename "$p")"
      if [[ ! -d "$archived_projects/$bn" ]]; then
        add_issue "WARNING" "Completed project not yet archived: $p" "Move folder to '$archived_projects/$bn'"
      fi
    done
  fi

  local agents
  while IFS= read -r agents; do
    CHECKED=$((CHECKED + 1))
    if grep -Eiq 'status:[[:space:]]*complete|completion date|completed on' "$agents"; then
      local project_dir
      project_dir="$(dirname "$agents")"
      add_issue "WARNING" "Project has completion markers in AGENTS.md: $project_dir" "Review and archive if work is finished"
    fi
  done < <(find "$TARGET/10_PROJECTS" -type f -name 'AGENTS.md' 2>/dev/null)
}

print_report() {
  local timestamp
  timestamp="$(date '+%Y-%m-%d %H:%M:%S %z')"
  local critical_count="${#CRITICAL[@]}"
  local warning_count="${#WARNING[@]}"
  local info_count="${#INFO[@]}"

  echo "# PARA Validation Report"
  echo
  echo "- Target: $TARGET"
  echo "- Timestamp: $timestamp"
  echo "- Items checked: $CHECKED"
  echo "- CRITICAL: $critical_count"
  echo "- WARNING: $warning_count"
  echo "- INFO: $info_count"
  echo

  echo "## CRITICAL"
  if (( critical_count == 0 )); then
    echo "- None"
  else
    printf '%s\n' "${CRITICAL[@]}"
  fi
  echo

  echo "## WARNING"
  if (( warning_count == 0 )); then
    echo "- None"
  else
    printf '%s\n' "${WARNING[@]}"
  fi
  echo

  echo "## INFO"
  if (( info_count == 0 )); then
    echo "- None"
  else
    printf '%s\n' "${INFO[@]}"
  fi
}

main() {
  parse_args "$@"

  if [[ ! -e "$TARGET" || ! -d "$TARGET" ]]; then
    echo "Error: target path does not exist or is not a directory: $TARGET" >&2
    exit 1
  fi

  if [[ "$RUN_STRUCTURE" == true ]]; then
    check_structure
  fi
  if [[ "$RUN_PROJECT_HEALTH" == true ]]; then
    check_project_health
  fi
  if [[ "$RUN_STALE" == true ]]; then
    check_stale_projects
  fi
  if [[ "$RUN_ORPHANS" == true ]]; then
    check_orphans
  fi
  if [[ "$RUN_ARCHIVE" == true ]]; then
    check_archive_candidates
  fi

  print_report
}

main "$@"
