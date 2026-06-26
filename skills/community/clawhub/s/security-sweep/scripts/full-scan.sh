#!/usr/bin/env bash
#
# full-scan.sh — Comprehensive security sweep for OpenClaw skills
# Part of security-sweep skill
#
# Usage:
#   bash full-scan.sh --builtin /path/to/builtin/skills --workspace /path/to/workspace/skills --output /path/to/report.txt
#

set -euo pipefail

BUILTIN_DIR=""
WORKSPACE_DIR=""
OUTPUT_FILE=""
QUIET=false
ENCRYPT_FOUND=false
NOTION_SECRETS_SCRIPT="${HOME}/.openclaw/scripts/notion-secrets.js"

# Patterns for secret detection — tightened to reduce false positives
# Only match actual key=value patterns, not documentation text
SECRET_PATTERNS=(
    "(api[_-]?key|token|password|secret|credential)\s*[=:]\s*[\"'][^'\"]{8,}[\"']"
    "Bearer\s+[a-zA-Z0-9_-]{20,}"
)

# Dangerous exec patterns
EXEC_PATTERNS=(
    "exec\s*\("
    "spawn\s*\("
    "eval\s*\("
    "child_process"
    "bash\s+-c"
    "system\s*\("
    "shell\s*:\s*true"
)

# Shell injection surfaces
INJECTION_PATTERNS=(
    '"\$.*?"'
    '`\$[^`]+`'
    '\$\{[^}]+\}'
)

# Network egress
NETWORK_PATTERNS=(
    "https?://"
    "curl\s+"
    "wget\s+"
    "fetch\s*\("
    "axios\s*\("
)

# Build combined regex for grep
build_secret_regex() {
    local IFS="|"
    echo "${SECRET_PATTERNS[*]}"
}

build_exec_regex() {
    local IFS="|"
    echo "${EXEC_PATTERNS[*]}"
}

build_injection_regex() {
    local IFS="|"
    echo "${INJECTION_PATTERNS[*]}"
}

build_network_regex() {
    local IFS="|"
    echo "${NETWORK_PATTERNS[*]}"
}

# ── Parse args ──────────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
    case "$1" in
        --builtin) BUILTIN_DIR="$2"; shift 2 ;;
        --workspace) WORKSPACE_DIR="$2"; shift 2 ;;
        --output) OUTPUT_FILE="$2"; shift 2 ;;
        --quiet) QUIET=true; shift ;;
        --encrypt-found) ENCRYPT_FOUND=true; shift ;;
        -h|--help)
            echo "Usage: full-scan.sh [options]"
            echo "  --builtin DIR     Bundled OpenClaw skills directory"
            echo "  --workspace DIR   Workspace skills directory"
            echo "  --output FILE     Output report file"
            echo "  --quiet           Suppress per-skill output"
            echo "  --encrypt-found   Encrypt found secrets to Notion"
            exit 0
            ;;
        *) echo "Unknown: $1"; exit 1 ;;
    esac
done

REPORT_DATE=$(date "+%Y-%m-%d %H:%M:%S %Z")
REPORT_FILE_TMP=$(mktemp)
FOUND_SECRETS_TMP=$(mktemp)

{
    echo "═══════════════════════════════════════════════════════════════"
    echo "  OpenClaw Security Sweep Report"
    echo "  ${REPORT_DATE}"
    echo "═══════════════════════════════════════════════════════════════"
} > "$REPORT_FILE_TMP"

# ── Encrypt a found secret to Notion ────────────────────────────────────────
encrypt_to_notion() {
    local label="$1"
    local secret="$2"
    local notion_script="$NOTION_SECRETS_SCRIPT"

    if [[ ! -f "$notion_script" ]]; then
        echo "    ⚠️  notion-secrets.js not found — skipping Notion store"
        return
    fi

    local master_pw="${NOTION_MASTER_PASSWORD:-}"
    if [[ -z "$master_pw" ]]; then
        echo "    ⚠️  NOTION_MASTER_PASSWORD env not set — skipping Notion store"
        return
    fi

    if echo "$master_pw" | node "$notion_script" put "scan-${label}" "$secret" 2>/dev/null | grep -q "Stored"; then
        echo "    🔒 Encrypted to Notion as 'scan-${label}'"
    else
        echo "    ⚠️  Failed to encrypt to Notion"
    fi
}

# ── Scan one skill directory ─────────────────────────────────────────────────
scan_skill() {
    local skill_path="$1"
    local skill_name
    skill_name=$(basename "$skill_path")

    local skill_critical=0 skill_high=0 skill_medium=0 skill_low=0 skill_info=0

    # Build the exclude args — skip node_modules, .git, and this script itself
    # NOTE: "secret" pattern is for detection only, not real secrets in this file
    local EXCLUDE_ARGS="--exclude=node_modules --exclude=.git --exclude=full-scan.sh --exclude=quick-scan.sh --exclude=*.min.js"

    # ── 1. Secret patterns ────────────────────────────────────────────
    local secret_regex
    secret_regex=$(build_secret_regex)
    # NOTE: exclude .md (docs trigger false positives) and /tests/ (test fixtures)
    while IFS= read -r file; do
        skill_critical=$((skill_critical + 1))
        echo "  🔴 SECRET: $file" >> "$FOUND_SECRETS_TMP"

        if [[ "$ENCRYPT_FOUND" == "true" ]]; then
            local secret_line
            secret_line=$(grep -rEn "$secret_regex" "$file" 2>/dev/null | head -1 || true)
            [[ -n "$secret_line" ]] && encrypt_to_notion "${skill_name}-$(basename "$file")" "$secret_line"
        fi
    done < <(grep -rEl "$secret_regex" "$skill_path" \
        --include="*.js" --include="*.ts" --include="*.sh" --include="*.py" --include="*.json" \
        $EXCLUDE_ARGS 2>/dev/null \
        | grep -v "\.md$" \
        | grep -v "/tests/" \
        | grep -v node_modules | grep -v "\.git" || true)

    # ── 2. Dangerous exec patterns ─────────────────────────────────────
    local exec_regex
    exec_regex=$(build_exec_regex)
    while IFS= read -r file; do
        skill_high=$((skill_high + 1))
        echo "  🟠 EXEC: $file" >> "$FOUND_SECRETS_TMP"
    done < <(grep -rEl "$exec_regex" "$skill_path" \
        --include="*.js" --include="*.ts" --include="*.sh" \
        $EXCLUDE_ARGS 2>/dev/null \
        | grep -v "/tests/" \
        | grep -v node_modules | grep -v "\.git" || true)

    # ── 3. Shell injection surfaces ────────────────────────────────────
    local injection_regex
    injection_regex=$(build_injection_regex)
    while IFS= read -r file; do
        skill_medium=$((skill_medium + 1))
        echo "  🟡 INJECTION: $file" >> "$FOUND_SECRETS_TMP"
    done < <(grep -rEl "$injection_regex" "$skill_path" \
        --include="*.js" --include="*.ts" --include="*.sh" \
        $EXCLUDE_ARGS 2>/dev/null \
        | grep -v "/tests/" \
        | grep -v node_modules | grep -v "\.git" || true)

    # ── 4. Network egress ─────────────────────────────────────────────
    local network_regex
    network_regex=$(build_network_regex)
    while IFS= read -r file; do
        skill_info=$((skill_info + 1))
        echo "  ℹ️  NETWORK: $file" >> "$FOUND_SECRETS_TMP"
    done < <(grep -rEl "$network_regex" "$skill_path" \
        --include="*.js" --include="*.ts" --include="*.sh" \
        $EXCLUDE_ARGS 2>/dev/null | grep -v node_modules | grep -v "\.git" || true)

    # ── 5. npm audit ─────────────────────────────────────────────────
    if [[ -f "$skill_path/package.json" && -d "$skill_path/node_modules" ]]; then
        local npm_out
        npm_out=$(cd "$skill_path" && npm audit --omit=dev --quiet 2>&1 || true)
        if echo "$npm_out" | grep -q "vulnerab"; then
            skill_medium=$((skill_medium + 1))
            echo "  🟡 NPM_AUDIT: $skill_path/package.json" >> "$FOUND_SECRETS_TMP"
        fi
    fi

    # ── Per-skill summary ────────────────────────────────────────────
    local skill_total=$((skill_critical + skill_high + skill_medium + skill_low))
    if [[ $skill_total -gt 0 ]] && [[ "$QUIET" != "true" ]]; then
        printf "  %-30s 🔴 %d 🟠 %d 🟡 %d\n" \
            "$skill_name" "$skill_critical" "$skill_high" "$skill_medium"
    fi

    echo "$skill_critical $skill_high $skill_medium $skill_low $skill_info"
}

# ── Scan a directory ────────────────────────────────────────────────────────
scan_dir() {
    local label="$1"
    local dir="$2"

    if [[ ! -d "$dir" ]]; then
        echo "  ⚠️  Directory not found: $dir"
        return
    fi

    local skill_count
    skill_count=$(find "$dir" -maxdepth 1 -type d 2>/dev/null | wc -l)
    skill_count=$((skill_count - 1))

    echo "" >> "$REPORT_FILE_TMP"
    echo "━━━ ${label} (${skill_count} skills) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >> "$REPORT_FILE_TMP"
    echo "" >> "$REPORT_FILE_TMP"
    echo "━━━ ${label} (${skill_count} skills) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "" >> "$REPORT_FILE_TMP"

    local total_critical=0 total_high=0 total_medium=0 total_low=0 total_info=0

    for skill_path in "$dir"/*/; do
        [[ ! -d "$skill_path" ]] && continue
        [[ -z "$(ls -A "$skill_path" 2>/dev/null)" ]] && continue
        [[ "$(basename "$skill_path")" == "node_modules" ]] && continue

        local skill_name
        skill_name=$(basename "$skill_path")

        printf "  Scanning %-28s ..." "$skill_name"

        local result
        result=$(scan_skill "$skill_path" 2>/dev/null | tail -1 || echo "0 0 0 0 0")
        read -r skill_critical skill_high skill_medium skill_low skill_info <<< "${result:-0 0 0 0 0}"

        total_critical=$((total_critical + skill_critical))
        total_high=$((total_high + skill_high))
        total_medium=$((total_medium + skill_medium))
        total_low=$((total_low + skill_low))
        total_info=$((total_info + skill_info))
    done

    echo "" >> "$REPORT_FILE_TMP"
    echo "━━━ ${label} Summary ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >> "$REPORT_FILE_TMP"
    printf "  🔴 CRITICAL: %d\n" "$total_critical" >> "$REPORT_FILE_TMP"
    printf "  🟠 HIGH:     %d\n" "$total_high" >> "$REPORT_FILE_TMP"
    printf "  🟡 MEDIUM:   %d\n" "$total_medium" >> "$REPORT_FILE_TMP"
    printf "  🟢 LOW:      %d\n" "$total_low" >> "$REPORT_FILE_TMP"
    printf "  ℹ️  INFO:     %d\n" "$total_info" >> "$REPORT_FILE_TMP"
    echo "" >> "$REPORT_FILE_TMP"

    printf "  🔴 CRITICAL: %d\n" "$total_critical"
    printf "  🟠 HIGH:     %d\n" "$total_high"
    printf "  🟡 MEDIUM:   %d\n" "$total_medium"
}

# ── Run scans ────────────────────────────────────────────────────────────────
[[ -n "$BUILTIN_DIR" ]] && scan_dir "BUNDLED SKILLS" "$BUILTIN_DIR"
[[ -n "$WORKSPACE_DIR" ]] && scan_dir "WORKSPACE SKILLS" "$WORKSPACE_DIR"

# ── Final report ───────────────────────────────────────────────────────────
{
    echo "" >> "$REPORT_FILE_TMP"
    echo "═══════════════════════════════════════════════════════════════" >> "$REPORT_FILE_TMP"
    echo "  Scan Complete — ${REPORT_DATE}" >> "$REPORT_FILE_TMP"
    echo "═══════════════════════════════════════════════════════════════" >> "$REPORT_FILE_TMP"
    echo "" >> "$REPORT_FILE_TMP"

    if [[ -s "$FOUND_SECRETS_TMP" ]]; then
        echo "━━━ Findings ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >> "$REPORT_FILE_TMP"
        cat "$FOUND_SECRETS_TMP" >> "$REPORT_FILE_TMP"
        echo "" >> "$REPORT_FILE_TMP"
        echo "  ⚠️  Review findings before publishing." >> "$REPORT_FILE_TMP"
    else
        echo "  ✅ Zero findings — clean scan." >> "$REPORT_FILE_TMP"
    fi

    echo "" >> "$REPORT_FILE_TMP"
    echo "  Report: ${OUTPUT_FILE:-<stdout>}" >> "$REPORT_FILE_TMP"
} >> "$REPORT_FILE_TMP"

# ── Output ──────────────────────────────────────────────────────────────────
if [[ -n "$OUTPUT_FILE" ]]; then
    mv "$REPORT_FILE_TMP" "$OUTPUT_FILE"
    echo ""
    echo "Report saved to: $OUTPUT_FILE"
else
    cat "$REPORT_FILE_TMP"
    rm "$REPORT_FILE_TMP"
fi
rm -f "$FOUND_SECRETS_TMP"
