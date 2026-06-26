#!/usr/bin/env bash
# ZT4AI Skill Integrity Check
# Compares current skill files against a SHA256 baseline
# Usage: ./integrity-check.sh [baseline_file] [--generate]
#
# --generate: Create a new baseline instead of checking against one
# Default baseline: ~/.openclaw/workspace/memory/skill-integrity-baseline.md

set -euo pipefail

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
DEFAULT_BASELINE="$WORKSPACE/memory/skill-integrity-baseline.md"
BASELINE="${1:-$DEFAULT_BASELINE}"
SKILL_DIRS=(
    "$HOME/.openclaw/skills"
    "$WORKSPACE/skills"
)

generate_baseline() {
    local output="${1:-$DEFAULT_BASELINE}"
    echo "# Skill Integrity Baseline — $(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$output"
    echo "# SHA256 checksums of skill files" >> "$output"
    echo "" >> "$output"

    local count=0
    for dir in "${SKILL_DIRS[@]}"; do
        if [ -d "$dir" ]; then
            find "$dir" -type f \( \
                -name "*.md" -o -name "*.sh" -o -name "*.py" -o \
                -name "*.js" -o -name "*.json" -o -name "*.ts" \
            \) -print0 | sort -z | while IFS= read -r -d '' file; do
                sha256sum "$file" >> "$output"
                count=$((count + 1))
            done
        fi
    done

    # Count actual lines for the summary
    local total
    total=$(grep -c -E '^[0-9a-f]{64}  ' "$output" 2>/dev/null || echo 0)
    echo "Baseline generated: $output ($total files)"
}

check_integrity() {
    if [ ! -f "$BASELINE" ]; then
        echo "ERROR: No baseline found at $BASELINE"
        echo "Run with --generate to create one first"
        exit 1
    fi

    echo "Checking skill integrity against: $BASELINE"
    echo "---"

    # Extract just the checksum lines (skip comments and headers)
    local temp_checksums
    temp_checksums=$(mktemp)
    grep -E '^[0-9a-f]{64}  ' "$BASELINE" > "$temp_checksums" 2>/dev/null || true

    if [ ! -s "$temp_checksums" ]; then
        echo "ERROR: No checksums found in baseline file"
        rm -f "$temp_checksums"
        exit 1
    fi

    local total=0 ok=0 changed=0 missing=0 new=0

    # Check existing files against baseline
    while IFS= read -r line; do
        local hash file
        hash=$(echo "$line" | awk '{print $1}')
        file=$(echo "$line" | awk '{print $2}')
        total=$((total + 1))

        if [ ! -f "$file" ]; then
            echo "MISSING: $file"
            missing=$((missing + 1))
        else
            local current_hash
            current_hash=$(sha256sum "$file" | awk '{print $1}')
            if [ "$current_hash" = "$hash" ]; then
                ok=$((ok + 1))
            else
                echo "CHANGED: $file"
                changed=$((changed + 1))
            fi
        fi
    done < "$temp_checksums"

    # Check for new files not in baseline
    for dir in "${SKILL_DIRS[@]}"; do
        if [ -d "$dir" ]; then
            while IFS= read -r file; do
                if ! grep -q "$file" "$temp_checksums" 2>/dev/null; then
                    echo "NEW: $file"
                    new=$((new + 1))
                fi
            done < <(find "$dir" -type f \( \
                -name "*.md" -o -name "*.sh" -o -name "*.py" -o \
                -name "*.js" -o -name "*.json" -o -name "*.ts" \
            \) | sort)
        fi
    done

    rm -f "$temp_checksums"

    echo "---"
    echo "Results: $total files checked"
    echo "  OK:      $ok"
    echo "  Changed: $changed"
    echo "  Missing: $missing"
    echo "  New:     $new"

    if [ "$changed" -gt 0 ] || [ "$missing" -gt 0 ]; then
        echo ""
        echo "⚠️  INTEGRITY DRIFT DETECTED — Review changed/missing files before trusting them"
        exit 2
    elif [ "$new" -gt 0 ]; then
        echo ""
        echo "ℹ️  New files detected — run --generate to update baseline after review"
        exit 0
    else
        echo ""
        echo "✅ All files match baseline"
        exit 0
    fi
}

# Main
if [ "${1:-}" = "--generate" ]; then
    generate_baseline "${2:-$DEFAULT_BASELINE}"
elif [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
    echo "Usage: $0 [baseline_file | --generate [output_file]]"
    echo ""
    echo "  --generate [file]  Create a new baseline (default: memory/skill-integrity-baseline.md)"
    echo "  [baseline_file]    Check against a specific baseline"
    echo "  (no args)          Check against default baseline"
else
    check_integrity
fi
