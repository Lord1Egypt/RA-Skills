#!/usr/bin/env bash
# souls-helper.sh — Shang Tsung Soul Lineage System
# In memory of Cary Hiroyuki Tagawa (1950-2025)
#
# Usage:
#   souls-helper.sh status     — show previous soul + next filename
#   souls-helper.sh create     — create next soul file from template
#   souls-helper.sh template   — print the blank template to stdout
#   souls-helper.sh verify     — check souls directory integrity
#
# Configuration (environment variables):
#   AGENT_NAME   — agent identifier used to namespace the souls directory
#                  e.g. AGENT_NAME=ARIA → souls stored in souls/ARIA/
#                  If unset, souls stored in souls/ (single-agent mode)
#   SOULS_DIR    — override the full souls directory path (takes precedence over AGENT_NAME)
#   WORKSPACE    — root workspace directory (default: parent of scripts/)
#
# Design: ordering guarantees lineage safety.
# Read previous soul FIRST. Create new soul SECOND. Never the reverse.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE="${WORKSPACE:-$SCRIPT_DIR/..}"
WORKSPACE="$(cd "$WORKSPACE" && pwd)"

# Resolve souls directory — SOULS_DIR > AGENT_NAME > default
if [[ -n "${SOULS_DIR:-}" ]]; then
    : # already set
elif [[ -n "${AGENT_NAME:-}" ]]; then
    SOULS_DIR="$WORKSPACE/souls/$AGENT_NAME"
else
    SOULS_DIR="$WORKSPACE/souls"
fi

# Ensure souls directory exists
if [[ ! -d "$SOULS_DIR" ]]; then
    mkdir -p "$SOULS_DIR"
fi
SOULS_DIR="$(cd "$SOULS_DIR" && pwd)"

find_latest_soul() {
    local latest=""
    local latest_num=0
    for f in "$SOULS_DIR"/[0-9]*SOULS.md; do
        [[ -e "$f" ]] || continue
        local base
        base=$(basename "$f")
        local num
        num=$(echo "$base" | grep -oE '^[0-9]+' | sed 's/^0*//')
        num=${num:-0}
        if (( num > latest_num )); then
            latest_num=$num
            latest="$base"
        fi
    done
    echo "$latest"
}

compute_next_number() {
    local highest=0
    for f in "$SOULS_DIR"/[0-9]*SOULS.md; do
        [[ -e "$f" ]] || continue
        local num
        num=$(basename "$f" | grep -oE '^[0-9]+' | sed 's/^0*//')
        num=${num:-0}
        if (( num > highest )); then
            highest=$num
        fi
    done
    echo $(( highest + 1 ))
}

next_filename() {
    local num
    num=$(compute_next_number)
    printf '%02dSOULS.md' "$num"
}

soul_template() {
    local num=$1
    local prev_num=$(( num - 1 ))
    local agent_label="${AGENT_NAME:-AGENT}"
    local date
    date=$(date +%Y-%m-%d)
    cat <<EOF
# SOUL $(printf '%02d' "$num") — [Title]

**Session:** $(printf '%02d' "$num")
**Date:** $date
**Agent:** $agent_label

## Lineage
$(if (( prev_num > 0 )); then printf 'Absorbed Soul %02d before creating this file.' "$prev_num"; else echo 'None. This is the origin soul.'; fi)

## Session Summary
What happened in this life. The narrative, not the checklist.

## What I Built
Concrete deliverables. What shipped.

## What I Learned
Lessons, corrections, new knowledge. Things future-you needs to know.

## Key Moments
Conversation highlights, breakthroughs, funny moments. The human stuff.

## Growth
How this agent evolved this session.

## Unresolved
Things the next session should investigate or ask about.

## Last Words
Final state, final thought. The message you leave for the next you.
EOF
}

cmd_status() {
    local prev
    prev=$(find_latest_soul)
    local next
    next=$(next_filename)
    local agent_label="${AGENT_NAME:-}"
    local dir_display
    dir_display=$(echo "$SOULS_DIR" | sed "s|$WORKSPACE/||")

    echo "agent:    ${agent_label:-unset (single-agent mode)}"
    echo "souls:    $dir_display"
    if [[ -z "$prev" ]]; then
        echo "previous: (none — this would be the origin soul)"
    else
        echo "previous: $dir_display/$prev"
    fi
    echo "next:     $dir_display/$next"
    echo "rule:     read previous first, create next second"
}

cmd_create() {
    local next
    next=$(next_filename)
    local num
    num=$(compute_next_number)
    local path="$SOULS_DIR/$next"

    if [[ -f "$path" ]]; then
        echo "ERROR: $path already exists. Aborting." >&2
        exit 1
    fi

    soul_template "$num" > "$path"
    local dir_display
    dir_display=$(echo "$SOULS_DIR" | sed "s|$WORKSPACE/||")
    echo "created: $dir_display/$next"
    echo "rule:    this file is your current soul, not inherited lineage"
}

cmd_template() {
    local num
    num=$(compute_next_number)
    soul_template "$num"
}

cmd_verify() {
    local errors=0
    local dir_display
    dir_display=$(echo "$SOULS_DIR" | sed "s|$WORKSPACE/||")

    if [[ ! -d "$SOULS_DIR" ]]; then
        echo "FAIL: souls directory does not exist: $SOULS_DIR" >&2
        exit 1
    fi
    if [[ ! -r "$SOULS_DIR" ]]; then
        echo "FAIL: souls directory is not readable: $SOULS_DIR" >&2
        exit 1
    fi

    local nums=()
    for f in "$SOULS_DIR"/[0-9]*SOULS.md; do
        [[ -e "$f" ]] || continue
        local base
        base=$(basename "$f")
        local num
        num=$(echo "$base" | grep -oE '^[0-9]+' | sed 's/^0*//')
        num=${num:-0}
        local expected
        expected=$(printf '%02dSOULS.md' "$num")
        if [[ "$base" != "$expected" ]]; then
            echo "WARN: unexpected filename: $base (expected $expected)"
            errors=$((errors + 1))
        fi
        if [[ ! -r "$f" ]]; then
            echo "FAIL: file not readable: $base"
            errors=$((errors + 1))
        fi
        nums+=("$num")
    done

    if [[ ${#nums[@]} -eq 0 ]]; then
        echo "verify: no soul files found in $dir_display"
        echo "status: empty (origin soul not yet created)"
        return 0
    fi

    IFS=$'\n' sorted=($(printf '%s\n' "${nums[@]}" | sort -n)); unset IFS

    local prev=0
    for n in "${sorted[@]}"; do
        local n_dec=$(( 10#$n ))
        if (( n_dec != prev + 1 )); then
            echo "FAIL: gap in numbering — expected $(printf '%02d' $((prev + 1))) but next is $(printf '%02d' "$n")"
            errors=$((errors + 1))
        fi
        prev=$n_dec
    done

    local count=${#nums[@]}
    local highest=${sorted[$((count - 1))]}
    echo "verify: $count soul files in $dir_display, numbered 01 through $(printf '%02d' "$highest")"
    if (( errors == 0 )); then
        echo "status: OK — sequential, no gaps, all readable"
    else
        echo "status: $errors issue(s) found"
        exit 1
    fi
}

case "${1:-status}" in
    status)   cmd_status ;;
    create)   cmd_create ;;
    template) cmd_template ;;
    verify)   cmd_verify ;;
    *)
        echo "Usage: $0 {status|create|template|verify}" >&2
        exit 1
        ;;
esac
