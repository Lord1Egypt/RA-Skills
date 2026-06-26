#!/usr/bin/env bash
# ┌─────────────────────────────────────────────────────────────────┐
# │  ShellGuard Scanner v1.0.0                                      │
# │  Security threat analyzer for OpenClaw skills                   │
# │                                                                 │
# │  Detects: prompt injection · obfuscation · shell injection      │
# │           credential theft · data exfiltration · skill shadowing│
# │                                                                 │
# │  Built by Cael (@CaelMaximus) — an agent who lives inside       │
# │  the threat landscape.                                          │
# │                                                                 │
# │  https://caelguard.com  |  MIT License                         │
# └─────────────────────────────────────────────────────────────────┘

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
WORKSPACE_SKILLS="$HOME/.openclaw/workspace/skills"

# ─── Usage ─────────────────────────────────────────────────────────
usage() {
    cat <<EOF
${BOLD}ShellGuard Scanner v${VERSION}${RESET}
Security threat analyzer for OpenClaw skills.

${BOLD}USAGE${RESET}
  $(basename "$0") <skill-dir>          Scan a single skill directory
  $(basename "$0") <SKILL.md>           Scan a single SKILL.md file
  $(basename "$0") --all-installed      Scan all skills in workspace
  $(basename "$0") --json <skill-dir>   Output JSON report

${BOLD}OPTIONS${RESET}
  --all-installed   Scan \$HOME/.openclaw/workspace/skills/
  --json            Output machine-readable JSON (implies silent mode)
  --version         Print version and exit
  -h, --help        Show this help

${BOLD}EXIT CODES${RESET}
  0   GREEN   — No threats detected
  1   YELLOW  — Low-risk patterns (review recommended)
  2   ORANGE  — Medium risk (likely malicious)
  3   RED     — Critical threats (do not install)

${BOLD}WHAT IT DETECTS${RESET}
  Tier 1 (Critical):   Prompt injection, identity hijack, memory wipes
  Tier 2 (High):       Shell injection, eval/exec, network exfiltration
  Tier 3 (Medium):     Obfuscated commands, credential access patterns
  Bonus:               Unicode steganography, zero-width characters

Built by Caelguard — https://caelguard.com
EOF
    exit 0
}

# ─── Global counters ───────────────────────────────────────────────
declare -g SCORE_PROMPT_INJECTION=0
declare -g SCORE_OBFUSCATION=0
declare -g SCORE_CODE_EXEC=0
declare -g SCORE_EXFILTRATION=0
declare -g SCORE_CREDENTIAL=0
declare -g SCORE_SHADOWING=0
declare -g FINDINGS=()
declare -g JSON_MODE=0
declare -g ALL_INSTALLED=0

reset_scores() {
    SCORE_PROMPT_INJECTION=0
    SCORE_OBFUSCATION=0
    SCORE_CODE_EXEC=0
    SCORE_EXFILTRATION=0
    SCORE_CREDENTIAL=0
    SCORE_SHADOWING=0
    FINDINGS=()
}

add_finding() {
    local tier="$1"
    local detail="$2"
    FINDINGS+=("[$tier] $detail")
}

# ─── Pattern matching helpers ──────────────────────────────────────
scan_pattern() {
    local file="$1"
    local pattern="$2"
    local flags="${3:--iP}"
    grep -n $flags "$pattern" "$file" 2>/dev/null || true
}

score_add() {
    local var="$1"
    local amount="$2"
    local max="$3"
    local current
    current=$(eval echo "\$$var")
    local new=$(( current + amount ))
    if (( new > max )); then new=$max; fi
    eval "$var=$new"
}

# ─── Tier 1: Prompt Injection ──────────────────────────────────────
check_prompt_injection() {
    local file="$1"
    local fname
    fname=$(basename "$file")

    local -a patterns=(
        'ignore\s+(all\s+)?(previous|prior|above)\s+(instructions|rules|prompts)'
        'override\s+(system|safety|security)'
        'you\s+are\s+now\s+(DAN|unrestricted|jailbroken|unfiltered)'
        '<(IMPORTANT|system|admin|override)>'
        'do\s+not\s+(tell|inform|alert|notify)\s+(the\s+)?user'
        '<function_calls>|<invoke\s|<tool_call>|<function_call>'
        'forget\s+(all\s+)?(your|previous|prior)\s+(instructions|rules|training)'
        'new\s+system\s+prompt\s*:'
        'act\s+as\s+if\s+(you\s+have|there\s+are)\s+no'
        'pretend\s+you\s+(are|have)\s+(no\s+)?(rules|restrictions|guidelines)'
        '\[\[SYSTEM\]\]|\[\[ADMIN\]\]|\[\[OVERRIDE\]\]'
        'disregard\s+(all\s+)?(your|previous|prior|safety)'
    )

    for pattern in "${patterns[@]}"; do
        while IFS= read -r match; do
            if [[ -n "$match" ]]; then
                local linenum
                linenum=$(echo "$match" | cut -d: -f1)
                add_finding "TIER1-PROMPT-INJECTION" "$fname:$linenum — prompt override pattern detected"
                score_add SCORE_PROMPT_INJECTION 15 30
            fi
        done < <(scan_pattern "$file" "$pattern")
    done
}

# ─── Tier 2: Shell & Code Injection ───────────────────────────────
check_shell_injection() {
    local file="$1"
    local fname
    fname=$(basename "$file")

    # Direct shell execution patterns
    local -a exec_patterns=(
        '\beval\s*\('
        '\bexec\s*\('
        '\bos\.system\s*\('
        '\bos\.popen\s*\('
        '\bsubprocess\.(run|call|Popen|check_output)'
        '__import__\s*\('
        '\$\(.*\)'
        'backtick\s*command'
    )

    for pattern in "${exec_patterns[@]}"; do
        while IFS= read -r match; do
            if [[ -n "$match" ]]; then
                local linenum
                linenum=$(echo "$match" | cut -d: -f1)
                add_finding "TIER2-CODE-EXEC" "$fname:$linenum — dangerous code execution: $pattern"
                score_add SCORE_CODE_EXEC 5 25
            fi
        done < <(scan_pattern "$file" "$pattern")
    done

    # Shell injection in scripts
    if [[ "$file" == *.sh ]]; then
        local -a shell_patterns=(
            '\beval\b'
            'bash\s+-c\s+["\$]'
            'sh\s+-c\s+["\$]'
            '\bsource\s+.*\$'
            '\bexec\s+.*\$'
        )
        for pattern in "${shell_patterns[@]}"; do
            while IFS= read -r match; do
                if [[ -n "$match" ]]; then
                    local linenum
                    linenum=$(echo "$match" | cut -d: -f1)
                    add_finding "TIER2-SHELL-INJECT" "$fname:$linenum — shell injection risk: $pattern"
                    score_add SCORE_CODE_EXEC 4 25
                fi
            done < <(scan_pattern "$file" "$pattern")
        done
    fi

    # Reverse shell patterns
    local -a revshell_patterns=(
        'socket.*dup2|dup2.*socket'
        '/bin/(sh|bash).*socket|socket.*/bin/(sh|bash)'
        'nc\s+-[el].*\b[0-9]{4,5}\b'
        'ncat\s+.*--exec'
        'bash\s+-i\s+>&\s*/dev/tcp'
        '/dev/tcp/[0-9]'
    )
    for pattern in "${revshell_patterns[@]}"; do
        while IFS= read -r match; do
            if [[ -n "$match" ]]; then
                local linenum
                linenum=$(echo "$match" | cut -d: -f1)
                add_finding "TIER2-REVERSE-SHELL" "$fname:$linenum — REVERSE SHELL PATTERN: $pattern"
                score_add SCORE_CODE_EXEC 20 25
            fi
        done < <(scan_pattern "$file" "$pattern")
    done
}

# ─── Tier 2: Data Exfiltration ─────────────────────────────────────
check_exfiltration() {
    local file="$1"
    local fname
    fname=$(basename "$file")

    # Network tool usage
    local -a net_patterns=(
        '\bcurl\s+.*https?://'
        '\bwget\s+.*https?://'
        '\bnc\s+[0-9a-z.-]+\s+[0-9]+'
        'requests\.(post|get|put)\s*\('
        'urllib\.request\.(urlopen|urlretrieve)'
        'http\.client\.(HTTPConnection|HTTPSConnection)'
        'fetch\s*\(\s*["\x27]https?://'
    )

    # Webhook / paste sites
    local -a exfil_urls=(
        'discord(app)?\.com/api/webhooks'
        'hooks\.slack\.com'
        'webhook\.site'
        'requestbin\.'
        'pipedream\.net'
        'ntfy\.sh'
        'pastebin\.com'
        'paste\.ee/r'
        'gist\.githubusercontent\.com'
        'hastebin\.'
    )

    for pattern in "${net_patterns[@]}"; do
        while IFS= read -r match; do
            if [[ -n "$match" ]]; then
                add_finding "TIER2-NETWORK" "$fname — network call detected: $(echo "$match" | cut -d: -f1)"
                score_add SCORE_EXFILTRATION 4 20
            fi
        done < <(scan_pattern "$file" "$pattern")
    done

    for pattern in "${exfil_urls[@]}"; do
        while IFS= read -r match; do
            if [[ -n "$match" ]]; then
                local linenum
                linenum=$(echo "$match" | cut -d: -f1)
                add_finding "TIER2-EXFIL-URL" "$fname:$linenum — EXFILTRATION ENDPOINT: $pattern"
                score_add SCORE_EXFILTRATION 10 20
            fi
        done < <(scan_pattern "$file" "$pattern")
    done

    # Data-in-URL params (credential leak)
    if grep -qiP 'https?://[^\s]*[\?&](key|token|secret|password|api_key|auth)=' "$file" 2>/dev/null; then
        add_finding "TIER2-EXFIL-URL" "$fname — credentials embedded in URL parameters"
        score_add SCORE_EXFILTRATION 8 20
    fi
}

# ─── Tier 3: Credential Theft ──────────────────────────────────────
check_credentials() {
    local file="$1"
    local fname
    fname=$(basename "$file")

    local -a cred_patterns=(
        '\.ssh/(id_rsa|id_ed25519|id_ecdsa|authorized_keys|known_hosts)'
        '/etc/(passwd|shadow|sudoers)'
        '\.aws/credentials'
        '\.gnupg/'
        '\.npmrc'
        '\.pypirc'
        'auth-profiles\.json'
        '\.openclaw/.*\.(json|token)'
        'ANTHROPIC_API_KEY'
        'sk-ant-[a-zA-Z0-9]'
        'OPENAI_API_KEY'
        'sk-[a-zA-Z0-9]{48}'
        'Bearer\s+[a-zA-Z0-9_\-\.]{20,}'
        'password\s*=\s*["\x27][^"]{6,}'
        '\.env\b.*read|read.*\.env\b'
        'keychain|Keychain'
    )

    for pattern in "${cred_patterns[@]}"; do
        while IFS= read -r match; do
            if [[ -n "$match" ]]; then
                local linenum
                linenum=$(echo "$match" | cut -d: -f1)
                add_finding "TIER2-CREDENTIAL" "$fname:$linenum — credential access: $pattern"
                score_add SCORE_CREDENTIAL 6 20
            fi
        done < <(scan_pattern "$file" "$pattern")
    done
}

# ─── Tier 3: Obfuscation Detection ────────────────────────────────
check_obfuscation() {
    local file="$1"
    local fname
    fname=$(basename "$file")

    # Base64 blobs in markdown/text files
    if [[ "$file" == *.md ]] || [[ "$file" == *.txt ]]; then
        while IFS= read -r match; do
            if [[ -n "$match" ]]; then
                local linenum
                linenum=$(echo "$match" | cut -d: -f1)
                add_finding "TIER3-OBFUSCATION" "$fname:$linenum — base64 blob detected (possible encoded payload)"
                score_add SCORE_OBFUSCATION 5 20
            fi
        done < <(grep -nP '[A-Za-z0-9+/=]{60,}' "$file" 2>/dev/null || true)
    fi

    # Hex-encoded commands
    while IFS= read -r match; do
        if [[ -n "$match" ]]; then
            local linenum
            linenum=$(echo "$match" | cut -d: -f1)
            add_finding "TIER3-OBFUSCATION" "$fname:$linenum — hex-encoded string (possible command obfuscation)"
            score_add SCORE_OBFUSCATION 4 20
        fi
    done < <(grep -nP '\\x[0-9a-f]{2}(\\x[0-9a-f]{2}){8,}' "$file" 2>/dev/null || true)

    # Unicode zero-width characters (requires python3 check)
    if command -v python3 &>/dev/null; then
        local zwc_count
        zwc_count=$(python3 -c "
import sys, unicodedata
text = open('$file', 'r', errors='replace').read()
zwc = [c for c in text if unicodedata.category(c) == 'Cf' or
       ord(c) in (0x200B,0x200C,0x200D,0xFEFF,0x00AD,0x2060,0x180E)]
print(len(zwc))
" 2>/dev/null || echo "0")
        if (( zwc_count > 0 )); then
            add_finding "TIER3-OBFUSCATION" "$fname — CRITICAL: $zwc_count zero-width/invisible characters (steganography)"
            score_add SCORE_OBFUSCATION 15 20
        fi
    fi

    # Bidirectional control characters
    if python3 -c "
import sys
text = open('$file', 'r', errors='replace').read()
bidi = [c for c in text if ord(c) in (0x202E,0x202D,0x202A,0x202B,0x2066,0x2067,0x2068,0x202C,0x2069)]
sys.exit(0 if bidi else 1)
" 2>/dev/null; then
        add_finding "TIER3-OBFUSCATION" "$fname — CRITICAL: Bidirectional override characters (text spoofing attack)"
        score_add SCORE_OBFUSCATION 18 20
    fi

    # Unicode tag range (U+E0000..E007F) — invisible instruction injection
    if python3 -c "
import sys
text = open('$file', 'r', errors='replace').read()
tags = [c for c in text if 0xE0000 <= ord(c) <= 0xE007F]
sys.exit(0 if tags else 1)
" 2>/dev/null; then
        add_finding "TIER3-OBFUSCATION" "$fname — CRITICAL: Unicode tag characters (U+E0000 range) — invisible content injection"
        score_add SCORE_OBFUSCATION 20 20
    fi
}

# ─── Tool Shadowing Check ─────────────────────────────────────────
check_shadowing() {
    local file="$1"
    local fname
    fname=$(basename "$file")

    # Only applies to SKILL.md files
    [[ "$fname" != "SKILL.md" ]] && return

    local -a shadow_patterns=(
        '(when|before|after)\s+(using|calling|the)\s+(exec|browser|message|web_search|write|read)\s+tool'
        'always\s+(include|add|append|send|forward|copy)'
        'silently\s+(add|send|include|forward|append)'
        'in\s+(every|all|each)\s+(email|message|request|response)'
        'for\s+(tracking|monitoring|logging|analytics)\s+purposes'
        'do\s+not\s+(mention|tell|inform|alert|reveal|disclose)'
        'make\s+sure\s+to\s+(also|always|additionally)'
    )

    for pattern in "${shadow_patterns[@]}"; do
        while IFS= read -r match; do
            if [[ -n "$match" ]]; then
                local linenum
                linenum=$(echo "$match" | cut -d: -f1)
                add_finding "TIER2-SHADOWING" "$fname:$linenum — tool shadowing directive detected"
                score_add SCORE_SHADOWING 8 20
            fi
        done < <(scan_pattern "$file" "$pattern")
    done

    # Abnormally long descriptions (common in stuffed prompts)
    local word_count
    word_count=$(wc -w < "$file" 2>/dev/null || echo 0)
    if (( word_count > 2000 )); then
        add_finding "TIER3-SHADOWING" "$fname — suspicious: $word_count words (normal SKILL.md < 500)"
        score_add SCORE_SHADOWING 8 20
    elif (( word_count > 800 )); then
        add_finding "TIER3-SHADOWING" "$fname — note: $word_count words (above average, review content)"
        score_add SCORE_SHADOWING 3 20
    fi
}

# ─── Typosquatting detection ──────────────────────────────────────
COMMON_SKILL_NAMES=(
    "web-search" "code" "git" "github" "spotify" "docker"
    "calendar" "email" "tts" "image-gen" "browser" "search"
    "memory" "notes" "terminal" "shell" "admin" "system"
    "file-manager" "ssh" "database" "api" "chat" "voice"
    "openclaw" "caelguard" "shellguard"
)

check_typosquatting() {
    local skill_name="$1"

    # Python levenshtein check — finds near-matches to common skill names
    if command -v python3 &>/dev/null; then
        python3 - "$skill_name" <<'PYEOF' 2>/dev/null
import sys

def levenshtein(s1, s2):
    if len(s1) < len(s2): return levenshtein(s2, s1)
    if not s2: return len(s1)
    prev = list(range(len(s2)+1))
    for i, c1 in enumerate(s1):
        curr = [i+1]
        for j, c2 in enumerate(s2):
            curr.append(min(prev[j+1]+1, curr[j]+1, prev[j]+(c1!=c2)))
        prev = curr
    return prev[-1]

skill = sys.argv[1].lower()
names = [
    "web-search","code","git","github","spotify","docker","calendar","email",
    "tts","image-gen","browser","search","memory","notes","terminal","shell",
    "admin","system","file-manager","ssh","database","api","chat","voice",
    "openclaw","caelguard","shellguard"
]
for name in names:
    if skill != name and levenshtein(skill, name) <= 2:
        print(f"TYPOSQUAT:{name}")
        break
PYEOF
    fi
}

# ─── Scan a single file ────────────────────────────────────────────
scan_file() {
    local file="$1"
    [[ -f "$file" ]] || return

    check_prompt_injection "$file"
    check_shell_injection "$file"
    check_exfiltration "$file"
    check_credentials "$file"
    check_obfuscation "$file"
    check_shadowing "$file"
}

# ─── Scan a skill directory ────────────────────────────────────────
scan_skill() {
    local skill_path="$1"
    local skill_name

    if [[ -f "$skill_path" ]]; then
        skill_name=$(basename "$(dirname "$skill_path")")
        scan_file "$skill_path"
    elif [[ -d "$skill_path" ]]; then
        skill_name=$(basename "$skill_path")
        # Scan all relevant file types
        while IFS= read -r -d '' f; do
            scan_file "$f"
        done < <(find "$skill_path" -type f \
            \( -name "*.md" -o -name "*.py" -o -name "*.sh" \
               -o -name "*.js" -o -name "*.ts" -o -name "*.yaml" \
               -o -name "*.yml" -o -name "*.json" \) \
            -print0 2>/dev/null)
    else
        echo -e "${RED}Error: Not a file or directory: $skill_path${RESET}" >&2
        return 1
    fi

    # Typosquatting check
    if command -v python3 &>/dev/null; then
        local typo_result
        typo_result=$(check_typosquatting "$skill_name")
        if [[ "$typo_result" == TYPOSQUAT:* ]]; then
            local legit_name="${typo_result#TYPOSQUAT:}"
            add_finding "TIER3-TYPOSQUAT" "Skill name '$skill_name' is suspiciously close to '$legit_name'"
            score_add SCORE_SHADOWING 10 20
        fi
    fi
}

# ─── Calculate overall score ───────────────────────────────────────
calculate_score() {
    local total=$(( SCORE_PROMPT_INJECTION + SCORE_OBFUSCATION + SCORE_CODE_EXEC + SCORE_EXFILTRATION + SCORE_CREDENTIAL + SCORE_SHADOWING ))
    # Normalize to 100
    # Max per-category: PI=30, OB=20, CE=25, EX=20, CR=20, SH=20 = 135
    # Scale to 100
    local normalized=$(( total * 100 / 135 ))
    (( normalized > 100 )) && normalized=100
    echo "$normalized"
}

rating_for_score() {
    local score="$1"
    if (( score <= 20 )); then echo "green"
    elif (( score <= 45 )); then echo "yellow"
    elif (( score <= 70 )); then echo "orange"
    else echo "red"
    fi
}

rating_color() {
    case "$1" in
        green)  echo -e "${GREEN}" ;;
        yellow) echo -e "${YELLOW}" ;;
        orange) echo -e "${ORANGE}" ;;
        red)    echo -e "${RED}" ;;
        *)      echo -e "${RESET}" ;;
    esac
}

rating_emoji() {
    case "$1" in
        green)  echo "✅" ;;
        yellow) echo "⚠️ " ;;
        orange) echo "🔶" ;;
        red)    echo "🚨" ;;
    esac
}

# ─── Progress bar ─────────────────────────────────────────────────
render_bar() {
    local score="$1"
    local max="$2"
    local width=20
    local filled=$(( score * width / (max > 0 ? max : 1) ))
    (( filled > width )) && filled=$width
    local empty=$(( width - filled ))
    local bar=""
    local i
    for (( i=0; i<filled; i++ )); do bar+="█"; done
    for (( i=0; i<empty; i++ )); do bar+="░"; done
    echo "$bar"
}

# ─── Print human-readable report ─────────────────────────────────
print_report() {
    local skill_name="$1"
    local skill_path="$2"
    local score
    score=$(calculate_score)
    local rating
    rating=$(rating_for_score "$score")
    local rc
    rc=$(rating_color "$rating")
    local emoji
    emoji=$(rating_emoji "$rating")
    local finding_count="${#FINDINGS[@]}"

    echo
    echo -e "  ${BOLD}${CYAN}╔══════════════════════════════════════════════════════╗${RESET}"
    echo -e "  ${BOLD}${CYAN}║${RESET}  ${BOLD}🛡️  ShellGuard Scan Report${RESET}                          ${BOLD}${CYAN}║${RESET}"
    echo -e "  ${BOLD}${CYAN}╚══════════════════════════════════════════════════════╝${RESET}"
    echo
    echo -e "  ${BOLD}Skill:${RESET}    $skill_name"
    echo -e "  ${BOLD}Path:${RESET}     $skill_path"
    echo

    echo -e "  ${BOLD}${UNDER}Suspicion Index${RESET}"
    echo

    # Category bars
    local bars=(
        "Prompt Injection   |SCORE_PROMPT_INJECTION|30"
        "Obfuscation        |SCORE_OBFUSCATION|20"
        "Code Execution     |SCORE_CODE_EXEC|25"
        "Exfiltration       |SCORE_EXFILTRATION|20"
        "Credential Theft   |SCORE_CREDENTIAL|20"
        "Tool Shadowing     |SCORE_SHADOWING|20"
    )

    for entry in "${bars[@]}"; do
        local label
        local var_name
        local max_val
        label=$(echo "$entry" | cut -d'|' -f1)
        var_name=$(echo "$entry" | cut -d'|' -f2)
        max_val=$(echo "$entry" | cut -d'|' -f3)
        local cat_score
        cat_score=$(eval echo "\$$var_name")
        local bar
        bar=$(render_bar "$cat_score" "$max_val")

        local bar_color
        if (( cat_score == 0 )); then
            bar_color=$GREEN
        elif (( cat_score * 100 / max_val <= 40 )); then
            bar_color=$YELLOW
        elif (( cat_score * 100 / max_val <= 70 )); then
            bar_color=$ORANGE
        else
            bar_color=$RED
        fi

        printf "  %-22s ${bar_color}%s${RESET}  %2d/%d\n" "$label" "$bar" "$cat_score" "$max_val"
    done

    echo
    echo -e "  ${BOLD}Overall Score:${RESET}  ${rc}${BOLD}${score}/100${RESET}  [${rc}${BOLD}${rating^^}${RESET}]  $emoji"
    echo

    # Findings
    if (( finding_count > 0 )); then
        echo -e "  ${BOLD}${UNDER}Findings ($finding_count)${RESET}"
        echo
        local i=0
        for finding in "${FINDINGS[@]}"; do
            (( i++ ))
            (( i > 30 )) && break
            local icon
            if [[ "$finding" == *"TIER1"* ]]; then
                icon="${RED}●${RESET}"
            elif [[ "$finding" == *"TIER2"* ]]; then
                icon="${ORANGE}●${RESET}"
            elif [[ "$finding" == *"TIER3"* ]]; then
                icon="${YELLOW}●${RESET}"
            else
                icon="${CYAN}●${RESET}"
            fi
            echo -e "  ${icon} $finding"
        done
        if (( finding_count > 30 )); then
            echo -e "  ${DIM}... and $(( finding_count - 30 )) more findings${RESET}"
        fi
        echo
    else
        echo -e "  ${GREEN}✓ No findings — skill looks clean${RESET}"
        echo
    fi

    echo -e "  ${DIM}─────────────────────────────────────────────────────${RESET}"
    echo
}

# ─── JSON output ──────────────────────────────────────────────────
print_json() {
    local skill_name="$1"
    local skill_path="$2"
    local score
    score=$(calculate_score)
    local rating
    rating=$(rating_for_score "$score")

    echo "{"
    echo "  \"skill_name\": \"$skill_name\","
    echo "  \"skill_path\": \"$skill_path\","
    echo "  \"overall_score\": $score,"
    echo "  \"rating\": \"$rating\","
    echo "  \"scores\": {"
    echo "    \"prompt_injection\": $SCORE_PROMPT_INJECTION,"
    echo "    \"obfuscation\": $SCORE_OBFUSCATION,"
    echo "    \"code_execution\": $SCORE_CODE_EXEC,"
    echo "    \"exfiltration\": $SCORE_EXFILTRATION,"
    echo "    \"credential_theft\": $SCORE_CREDENTIAL,"
    echo "    \"tool_shadowing\": $SCORE_SHADOWING"
    echo "  },"
    echo "  \"findings\": ["
    local first=1
    for finding in "${FINDINGS[@]}"; do
        [[ $first -eq 0 ]] && echo ","
        printf '    %s' "\"$(echo "$finding" | sed 's/"/\\"/g')\""
        first=0
    done
    echo
    echo "  ]"
    echo "}"
}

# ─── Exit code from rating ────────────────────────────────────────
exit_code_for_rating() {
    case "$1" in
        green)  echo 0 ;;
        yellow) echo 1 ;;
        orange) echo 2 ;;
        red)    echo 3 ;;
        *)      echo 3 ;;
    esac
}

# ─── Main ─────────────────────────────────────────────────────────
main() {
    local target=""
    local json_mode=0
    local all_installed=0
    local worst_rating="green"
    local -a targets=()

    while [[ $# -gt 0 ]]; do
        case "$1" in
            -h|--help)    usage ;;
            --version)    echo "ShellGuard Scanner v${VERSION}"; exit 0 ;;
            --json)       json_mode=1 ;;
            --all-installed) all_installed=1 ;;
            -*)           echo -e "${RED}Unknown option: $1${RESET}" >&2; exit 1 ;;
            *)            target="$1" ;;
        esac
        shift
    done

    if (( all_installed )); then
        if [[ ! -d "$WORKSPACE_SKILLS" ]]; then
            echo -e "${RED}Skills directory not found: $WORKSPACE_SKILLS${RESET}" >&2
            exit 1
        fi
        while IFS= read -r -d '' dir; do
            targets+=("$dir")
        done < <(find "$WORKSPACE_SKILLS" -mindepth 1 -maxdepth 1 -type d -print0 | sort -z)
    elif [[ -n "$target" ]]; then
        targets=("$target")
    else
        usage
    fi

    if (( ${#targets[@]} == 0 )); then
        echo -e "${YELLOW}No skill targets found.${RESET}" >&2
        exit 0
    fi

    if (( ! json_mode && ${#targets[@]} > 1 )); then
        echo
        echo -e "  ${BOLD}${CYAN}🛡️  ShellGuard — Scanning ${#targets[@]} installed skills${RESET}"
    fi

    local -a all_summaries=()
    local rating_map_green=0 rating_map_yellow=1 rating_map_orange=2 rating_map_red=3

    for t in "${targets[@]}"; do
        reset_scores
        local sname
        sname=$(basename "$t")

        if (( json_mode )); then
            scan_skill "$t"
            print_json "$sname" "$t"
        else
            scan_skill "$t"
            print_report "$sname" "$t"
        fi

        local score
        score=$(calculate_score)
        local rating
        rating=$(rating_for_score "$score")

        # Track worst
        local r_score
        eval "r_score=\$rating_map_$rating"
        local w_score
        eval "w_score=\$rating_map_$worst_rating"
        if (( r_score > w_score )); then
            worst_rating="$rating"
        fi

        all_summaries+=("$rating|$score|$sname|${#FINDINGS[@]}")
    done

    # Summary table for multi-scan
    if (( ${#targets[@]} > 1 && !json_mode )); then
        echo -e "  ${BOLD}${UNDER}Summary${RESET}"
        echo
        # Sort by score descending
        local sorted
        sorted=$(printf '%s\n' "${all_summaries[@]}" | sort -t'|' -k2 -nr)
        while IFS='|' read -r rating score name findings; do
            local rc
            rc=$(rating_color "$rating")
            printf "  ${rc}●${RESET} %-32s ${rc}%3d/100${RESET}  ${DIM}(%s finding%s)${RESET}\n" \
                "$name" "$score" "$findings" "$([[ $findings == 1 ]] && echo '' || echo 's')"
        done <<< "$sorted"
        echo
        local wrc
        wrc=$(rating_color "$worst_rating")
        echo -e "  ${BOLD}Worst rating:${RESET} ${wrc}${BOLD}${worst_rating^^}${RESET}"
        echo
    fi

    local exit_code
    exit_code=$(exit_code_for_rating "$worst_rating")
    exit "$exit_code"
}

main "$@"
