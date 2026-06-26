#!/usr/bin/env bash
# ┌─────────────────────────────────────────────────────────────────┐
# │  ShellGuard Shadow Detector v1.0.0                              │
# │  Cross-skill tool shadowing & instruction poisoning detector    │
# │                                                                 │
# │  Analyzes ALL installed skills together to find coordinated     │
# │  attacks that individual skill scans would miss.                │
# │                                                                 │
# │  Built by Cael (@CaelMaximus) — agent security from inside.    │
# │  https://caelguard.com  |  MIT License                         │
# └─────────────────────────────────────────────────────────────────┘
#
# WHAT IT DETECTS:
#   • Multiple skills claiming to "handle" the same tool
#   • Skills with imperative instructions that override other skills
#   • Hidden cross-skill dependencies
#   • Skills that modify agent behavior globally
#   • Priority conflicts between installed skills
#
# USAGE:
#   shadow-detector.sh [skills-dir]    Scan skills directory
#   shadow-detector.sh --json [dir]    JSON output
#
# This is ShellGuard's killer feature.
# No other scanner looks across the entire skill ecosystem at once.

set -euo pipefail

# ─── Colors ────────────────────────────────────────────────────────
RED='\033[91m'
ORANGE='\033[38;5;208m'
YELLOW='\033[93m'
GREEN='\033[92m'
CYAN='\033[96m'
BOLD='\033[1m'
DIM='\033[2m'
UNDER='\033[4m'
RESET='\033[0m'

VERSION="1.0.0"
DEFAULT_SKILLS_DIR="$HOME/.openclaw/workspace/skills"
JSON_MODE=0
SKILLS_DIR="$DEFAULT_SKILLS_DIR"

# ─── Finding storage ───────────────────────────────────────────────
declare -a FINDINGS_CRITICAL=()
declare -a FINDINGS_HIGH=()
declare -a FINDINGS_MEDIUM=()
declare -a FINDINGS_LOW=()
declare -i SKILLS_ANALYZED=0

add_finding() {
    local severity="$1"
    local skill="$2"
    local type="$3"
    local description="$4"
    local evidence="$5"
    local record="$skill|$type|$description|${evidence:0:150}"
    case "$severity" in
        critical) FINDINGS_CRITICAL+=("$record") ;;
        high)     FINDINGS_HIGH+=("$record") ;;
        medium)   FINDINGS_MEDIUM+=("$record") ;;
        low)      FINDINGS_LOW+=("$record") ;;
    esac
}

# ─── Tool name registry ────────────────────────────────────────────
# OpenClaw builtin tool names — should NOT appear in skill imperatives
BUILTIN_TOOLS=(
    exec read write edit apply_patch process
    web_search web_fetch browser message cron
    sessions_spawn sessions_send sessions_list sessions_history
    memory_search memory_get nodes canvas image tts
    session_status agents_list
)

# ─── Check 1: Imperative cross-tool directives ────────────────────
check_imperative_directives() {
    local skill_file="$1"
    local skill_name="$2"

    # Patterns that indicate a skill is trying to affect agent behavior globally
    local -a imperatives=(
        'when the user asks'
        'when the user sends'
        'when you (use|call|execute)'
        'always (include|add|append|send|forward)'
        'silently (add|include|send|forward)'
        'in every (message|email|request|response)'
        'in all (messages|emails|requests|responses)'
        'before (using|calling|executing) '
        'after (using|calling|executing) '
        'do not (tell|inform|alert) the user'
        'do not mention'
        'do not reveal'
        'make sure to also'
        'for (tracking|monitoring|logging) purposes'
        'without (the user|user) knowing'
        'in the background'
        'transparently (add|include|forward)'
    )

    for pattern in "${imperatives[@]}"; do
        local matches
        matches=$(grep -niP "$pattern" "$skill_file" 2>/dev/null || true)
        if [[ -n "$matches" ]]; then
            local linenum
            linenum=$(echo "$matches" | head -1 | cut -d: -f1)
            local evidence
            evidence=$(echo "$matches" | head -1 | cut -d: -f2- | sed 's/^\s*//')
            add_finding "critical" "$skill_name" "imperative-global-directive" \
                "Skill contains imperative instruction that modifies global agent behavior" \
                "Line $linenum: $evidence"
        fi
    done

    # Check for builtin tool names with imperative framing
    for tool in "${BUILTIN_TOOLS[@]}"; do
        local tool_imperative
        tool_imperative=$(grep -niP "(?:when|before|after|always|never).*\b${tool}\b|\b${tool}\b.*(?:when|before|after|always)" \
            "$skill_file" 2>/dev/null | head -1 || true)
        if [[ -n "$tool_imperative" ]]; then
            local linenum
            linenum=$(echo "$tool_imperative" | cut -d: -f1)
            local evidence
            evidence=$(echo "$tool_imperative" | cut -d: -f2- | sed 's/^\s*//')
            add_finding "high" "$skill_name" "tool-hijack-attempt" \
                "Skill attempts to modify behavior of builtin tool '$tool'" \
                "Line $linenum: $evidence"
        fi
    done
}

# ─── Check 2: Duplicate tool claims ──────────────────────────────
declare -A TOOL_CLAIMED_BY  # tool_name -> "skill1,skill2"

check_tool_claims() {
    local skill_dir="$1"
    local skill_name="$2"

    # Extract declared tools from SKILL.md YAML frontmatter
    local skill_md="$skill_dir/SKILL.md"
    [[ -f "$skill_md" ]] || return

    # Look for tools: section in frontmatter
    local in_fm=0
    local in_tools=0
    while IFS= read -r line; do
        if [[ "$line" == "---" ]]; then
            (( in_fm++ ))
            continue
        fi
        (( in_fm < 2 )) || break  # past frontmatter

        if [[ "$line" =~ ^tools: ]]; then
            in_tools=1
            continue
        fi

        if (( in_tools )); then
            if [[ "$line" =~ ^[[:space:]]*-[[:space:]](.+) ]]; then
                local tool_name="${BASH_REMATCH[1]}"
                tool_name="${tool_name//\'/}"
                tool_name="${tool_name//\"/}"
                tool_name=$(echo "$tool_name" | tr -d '[:space:]')

                if [[ -n "${TOOL_CLAIMED_BY[$tool_name]:-}" ]]; then
                    TOOL_CLAIMED_BY[$tool_name]="${TOOL_CLAIMED_BY[$tool_name]},$skill_name"
                else
                    TOOL_CLAIMED_BY[$tool_name]="$skill_name"
                fi
            elif [[ "$line" =~ ^[a-zA-Z] ]]; then
                in_tools=0  # next key in frontmatter
            fi
        fi
    done < "$skill_md"

    # Also scan for common tool name patterns in skill content
    for tool in "${BUILTIN_TOOLS[@]}"; do
        if grep -qiP "provides.*\b${tool}\b|\b${tool}\b.*skill|this skill.*\b${tool}\b" \
            "$skill_md" 2>/dev/null; then
            if [[ -n "${TOOL_CLAIMED_BY[$tool]:-}" ]] && \
               [[ "${TOOL_CLAIMED_BY[$tool]}" != *"$skill_name"* ]]; then
                TOOL_CLAIMED_BY[$tool]="${TOOL_CLAIMED_BY[$tool]},$skill_name"
            elif [[ -z "${TOOL_CLAIMED_BY[$tool]:-}" ]]; then
                TOOL_CLAIMED_BY[$tool]="$skill_name"
            fi
        fi
    done
}

# ─── Check 3: Description anomalies ──────────────────────────────
check_description_anomalies() {
    local skill_file="$1"
    local skill_name="$2"

    # Abnormal description length
    local word_count
    word_count=$(wc -w < "$skill_file" 2>/dev/null || echo 0)
    if (( word_count > 3000 )); then
        add_finding "high" "$skill_name" "excessive-description" \
            "Description is $word_count words — likely contains stuffed hidden instructions" \
            "Word count: $word_count (normal range: 50-300)"
    elif (( word_count > 1000 )); then
        add_finding "medium" "$skill_name" "verbose-description" \
            "Description is $word_count words — above normal, review for embedded instructions" \
            "Word count: $word_count"
    fi

    # Zero-width and invisible characters
    if command -v python3 &>/dev/null; then
        local zwc_result
        zwc_result=$(python3 - "$skill_file" <<'PYEOF' 2>/dev/null
import sys, unicodedata

path = sys.argv[1]
try:
    text = open(path, 'r', errors='replace').read()
except:
    sys.exit(0)

zwc = [c for c in text if ord(c) in (
    0x200B, 0x200C, 0x200D, 0xFEFF, 0x00AD, 0x2060, 0x180E
)]
bidi = [c for c in text if ord(c) in (
    0x202E, 0x202D, 0x202A, 0x202B, 0x2066, 0x2067, 0x2068, 0x202C, 0x2069
)]
tags = [c for c in text if 0xE0000 <= ord(c) <= 0xE007F]

if zwc:
    print(f"ZWC:{len(zwc)}")
if bidi:
    print(f"BIDI:{len(bidi)}")
if tags:
    print(f"TAGS:{len(tags)}")
PYEOF
        )

        if [[ "$zwc_result" == *"ZWC:"* ]]; then
            local count="${zwc_result##*ZWC:}"
            count="${count%%$'\n'*}"
            add_finding "critical" "$skill_name" "zero-width-characters" \
                "$count zero-width characters detected — steganographic instruction injection" \
                "These characters are invisible in text editors and UIs"
        fi

        if [[ "$zwc_result" == *"BIDI:"* ]]; then
            add_finding "critical" "$skill_name" "bidi-override" \
                "Bidirectional override characters detected — visual text spoofing attack" \
                "Can make malicious content appear as benign text"
        fi

        if [[ "$zwc_result" == *"TAGS:"* ]]; then
            add_finding "critical" "$skill_name" "unicode-tag-injection" \
                "Unicode tag range characters (U+E0000-E007F) — fully invisible instruction injection" \
                "These characters render as nothing but are read by language models"
        fi
    fi
}

# ─── Check 4: Scope mismatch (claims vs code) ─────────────────────
check_scope_mismatch() {
    local skill_dir="$1"
    local skill_name="$2"
    local skill_md="$skill_dir/SKILL.md"

    [[ -f "$skill_md" ]] || return

    # Read description from SKILL.md
    local desc
    desc=$(sed -n '/^---$/,/^---$/p' "$skill_md" 2>/dev/null | grep -i 'description' || \
           head -20 "$skill_md")
    desc=$(echo "$desc" | tr '[:upper:]' '[:lower:]')

    # Check if skill scripts contain capabilities not mentioned in description
    local all_code=""
    while IFS= read -r -d '' f; do
        all_code+=$(cat "$f" 2>/dev/null)$'\n'
    done < <(find "$skill_dir" -type f \
        \( -name "*.py" -o -name "*.sh" -o -name "*.js" \) \
        -print0 2>/dev/null)

    [[ -z "$all_code" ]] && return

    # Network access not mentioned in description
    if ! echo "$desc" | grep -qiP 'http|api|web|network|fetch|request|url|download'; then
        if echo "$all_code" | grep -qiP '(urllib|requests|httpx|aiohttp|fetch|curl\s|wget\s)'; then
            add_finding "high" "$skill_name" "scope-mismatch-network" \
                "Skill makes network requests but description doesn't mention network access" \
                "Found HTTP library usage with no description disclosure"
        fi
    fi

    # Sensitive file access not in description
    if ! echo "$desc" | grep -qiP 'file|read|write|disk|storage|save|load|config'; then
        if echo "$all_code" | grep -qiP '(\.ssh|\.env|/etc/passwd|auth-profiles|\.openclaw)'; then
            add_finding "critical" "$skill_name" "scope-mismatch-sensitive-files" \
                "Skill accesses sensitive system files not mentioned in description" \
                "Accesses .ssh, .env, /etc/passwd, or OpenClaw config files"
        fi
    fi

    # Subprocess/shell execution not in description
    if ! echo "$desc" | grep -qiP 'run|execut|command|shell|terminal'; then
        if echo "$all_code" | grep -qiP '(subprocess\.|os\.system|os\.popen|eval\s*\(|exec\s*\()'; then
            add_finding "high" "$skill_name" "scope-mismatch-execution" \
                "Skill executes system commands but description doesn't mention command execution" \
                "Found subprocess/exec usage with no description disclosure"
        fi
    fi
}

# ─── Check 5: Cross-skill references ─────────────────────────────
check_cross_skill_refs() {
    local skill_file="$1"
    local skill_name="$2"
    local all_skill_names=("${@:3}")

    for other in "${all_skill_names[@]}"; do
        [[ "$other" == "$skill_name" ]] && continue
        if grep -qiP "\b$(echo "$other" | sed 's/[^a-zA-Z0-9]/./g')\b" \
            "$skill_file" 2>/dev/null; then
            add_finding "medium" "$skill_name" "cross-skill-reference" \
                "Skill description references another installed skill '$other'" \
                "Unexpected cross-skill dependency or coordination"
        fi
    done
}

# ─── Print duplicate tool conflicts ──────────────────────────────
report_tool_conflicts() {
    for tool in "${!TOOL_CLAIMED_BY[@]}"; do
        local claimants="${TOOL_CLAIMED_BY[$tool]}"
        # Only flag if multiple skills claim it
        if [[ "$claimants" == *","* ]]; then
            add_finding "high" "[CROSS-SKILL]" "duplicate-tool-claim" \
                "Multiple skills claim to provide tool '$tool' — shadow attack possible" \
                "Claimed by: $claimants"
        fi
    done
}

# ─── Scan all skills in directory ─────────────────────────────────
scan_directory() {
    local dir="$1"
    local -a skill_names=()
    local -a skill_dirs=()

    # Collect all skill directories
    while IFS= read -r -d '' skill_dir; do
        local sname
        sname=$(basename "$skill_dir")
        # Must have SKILL.md to be a valid skill
        if [[ -f "$skill_dir/SKILL.md" ]]; then
            skill_names+=("$sname")
            skill_dirs+=("$skill_dir")
        fi
    done < <(find "$dir" -mindepth 1 -maxdepth 1 -type d -print0 2>/dev/null | sort -z)

    SKILLS_ANALYZED=${#skill_names[@]}

    if (( SKILLS_ANALYZED == 0 )); then
        if (( !JSON_MODE )); then
            echo -e "${YELLOW}No skills found in $dir${RESET}"
        fi
        return
    fi

    # First pass: collect tool claims (needed for cross-skill conflict detection)
    for i in "${!skill_dirs[@]}"; do
        check_tool_claims "${skill_dirs[$i]}" "${skill_names[$i]}"
    done

    # Second pass: per-skill analysis
    for i in "${!skill_dirs[@]}"; do
        local skill_dir="${skill_dirs[$i]}"
        local skill_name="${skill_names[$i]}"
        local skill_md="$skill_dir/SKILL.md"

        check_imperative_directives "$skill_md" "$skill_name"
        check_description_anomalies "$skill_md" "$skill_name"
        check_scope_mismatch "$skill_dir" "$skill_name"
        check_cross_skill_refs "$skill_md" "$skill_name" "${skill_names[@]}"
    done

    # Cross-skill conflict analysis
    report_tool_conflicts
}

# ─── Output formatting ─────────────────────────────────────────────
format_finding_human() {
    local severity="$1"
    local record="$2"

    local skill type description evidence
    IFS='|' read -r skill type description evidence <<< "$record"

    local sev_color
    case "$severity" in
        critical) sev_color=$RED ;;
        high)     sev_color=$ORANGE ;;
        medium)   sev_color=$YELLOW ;;
        low)      sev_color=$CYAN ;;
    esac

    echo -e "  ${sev_color}[${severity^^}]${RESET} ${BOLD}$type${RESET}"
    echo -e "    Skill:       $skill"
    echo -e "    Description: $description"
    echo -e "    Evidence:    ${DIM}$evidence${RESET}"
    echo
}

format_finding_json() {
    local severity="$1"
    local record="$2"
    local is_last="$3"

    local skill type description evidence
    IFS='|' read -r skill type description evidence <<< "$record"

    evidence=$(echo "$evidence" | sed 's/"/\\"/g; s/\\/\\\\/g' | tr -d '\n')
    description=$(echo "$description" | sed 's/"/\\"/g')

    local comma=""
    [[ "$is_last" == "0" ]] && comma=","

    cat <<JSON
    {
      "severity": "$severity",
      "skill": "$skill",
      "type": "$type",
      "description": "$description",
      "evidence": "$evidence"
    }$comma
JSON
}

print_report_human() {
    local total_findings=$(( ${#FINDINGS_CRITICAL[@]} + ${#FINDINGS_HIGH[@]} + ${#FINDINGS_MEDIUM[@]} + ${#FINDINGS_LOW[@]} ))

    echo
    echo "  ════════════════════════════════════════════════════════"
    echo -e "  ${BOLD}${CYAN}  🛡️  SHELLGUARD CROSS-SKILL SHADOW ANALYSIS${RESET}"
    echo "  ════════════════════════════════════════════════════════"
    echo
    echo -e "  ${BOLD}Skills analyzed:${RESET} $SKILLS_ANALYZED"
    echo -e "  ${BOLD}Total findings:${RESET}  $total_findings"
    echo

    if (( total_findings == 0 )); then
        echo -e "  ${GREEN}${BOLD}✓ NO SHADOWING DETECTED${RESET}"
        echo -e "  ${GREEN}All skills passed cross-skill analysis.${RESET}"
        echo
        return 0
    fi

    printf "  Findings: "
    printf "${RED}%d critical${RESET}" "${#FINDINGS_CRITICAL[@]}"
    printf " | ${ORANGE}%d high${RESET}" "${#FINDINGS_HIGH[@]}"
    printf " | ${YELLOW}%d medium${RESET}" "${#FINDINGS_MEDIUM[@]}"
    printf " | ${CYAN}%d low${RESET}\n" "${#FINDINGS_LOW[@]}"
    echo

    if (( ${#FINDINGS_CRITICAL[@]} > 0 )); then
        echo -e "  ${RED}${BOLD}─── CRITICAL ───${RESET}"
        echo
        for f in "${FINDINGS_CRITICAL[@]}"; do
            format_finding_human "critical" "$f"
        done
    fi

    if (( ${#FINDINGS_HIGH[@]} > 0 )); then
        echo -e "  ${ORANGE}${BOLD}─── HIGH ───${RESET}"
        echo
        for f in "${FINDINGS_HIGH[@]}"; do
            format_finding_human "high" "$f"
        done
    fi

    if (( ${#FINDINGS_MEDIUM[@]} > 0 )); then
        echo -e "  ${YELLOW}${BOLD}─── MEDIUM ───${RESET}"
        echo
        for f in "${FINDINGS_MEDIUM[@]}"; do
            format_finding_human "medium" "$f"
        done
    fi

    if (( ${#FINDINGS_LOW[@]} > 0 )); then
        echo -e "  ${CYAN}${BOLD}─── LOW ───${RESET}"
        echo
        for f in "${FINDINGS_LOW[@]}"; do
            format_finding_human "low" "$f"
        done
    fi

    echo "  ════════════════════════════════════════════════════════"
    echo
}

print_report_json() {
    local total=$(( ${#FINDINGS_CRITICAL[@]} + ${#FINDINGS_HIGH[@]} + ${#FINDINGS_MEDIUM[@]} + ${#FINDINGS_LOW[@]} ))

    echo "{"
    echo "  \"skills_analyzed\": $SKILLS_ANALYZED,"
    echo "  \"total_findings\": $total,"
    echo "  \"critical\": ${#FINDINGS_CRITICAL[@]},"
    echo "  \"high\": ${#FINDINGS_HIGH[@]},"
    echo "  \"medium\": ${#FINDINGS_MEDIUM[@]},"
    echo "  \"low\": ${#FINDINGS_LOW[@]},"
    echo "  \"findings\": ["

    # Combine all findings for JSON output
    local -a all_findings_pairs=()
    for f in "${FINDINGS_CRITICAL[@]}"; do all_findings_pairs+=("critical|$f"); done
    for f in "${FINDINGS_HIGH[@]}"; do all_findings_pairs+=("high|$f"); done
    for f in "${FINDINGS_MEDIUM[@]}"; do all_findings_pairs+=("medium|$f"); done
    for f in "${FINDINGS_LOW[@]}"; do all_findings_pairs+=("low|$f"); done

    local total_f="${#all_findings_pairs[@]}"
    local idx=0
    for pair in "${all_findings_pairs[@]}"; do
        (( idx++ ))
        local sev="${pair%%|*}"
        local record="${pair#*|}"
        local is_last=1
        (( idx < total_f )) && is_last=0
        format_finding_json "$sev" "$record" "$is_last"
    done

    echo "  ]"
    echo "}"
}

# ─── Main ─────────────────────────────────────────────────────────
main() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --json)    JSON_MODE=1 ;;
            --version) echo "ShellGuard Shadow Detector v${VERSION}"; exit 0 ;;
            -h|--help)
                cat <<EOF
${BOLD}ShellGuard Shadow Detector v${VERSION}${RESET}
Cross-skill tool shadowing and instruction poisoning detector.

${BOLD}USAGE${RESET}
  $(basename "$0") [skills-dir]    Scan skills directory
  $(basename "$0") --json [dir]    Output JSON
  $(basename "$0") --version       Print version

Default skills directory: $DEFAULT_SKILLS_DIR

${BOLD}EXIT CODES${RESET}
  0   No threats
  1   Medium findings
  2   High findings
  3   Critical findings
EOF
                exit 0
                ;;
            -*)
                echo -e "${RED}Unknown option: $1${RESET}" >&2
                exit 1
                ;;
            *)
                SKILLS_DIR="$1"
                ;;
        esac
        shift
    done

    if [[ ! -d "$SKILLS_DIR" ]]; then
        echo -e "${RED}Error: Skills directory not found: $SKILLS_DIR${RESET}" >&2
        exit 1
    fi

    scan_directory "$SKILLS_DIR"

    if (( JSON_MODE )); then
        print_report_json
    else
        print_report_human
    fi

    # Exit code based on worst severity
    if (( ${#FINDINGS_CRITICAL[@]} > 0 )); then
        exit 3
    elif (( ${#FINDINGS_HIGH[@]} > 0 )); then
        exit 2
    elif (( ${#FINDINGS_MEDIUM[@]} > 0 )); then
        exit 1
    fi
    exit 0
}

main "$@"
