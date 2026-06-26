#!/usr/bin/env bash
# skill-sandbox.sh — Sandboxed ClawHub skill installation with security scanning
# Part of the skill-sandbox skill (clawhub.com)
#
# Usage:
#   bash skill-sandbox.sh <skill-name> [options]
#   bash skill-sandbox.sh --list-staged
#
# Options:
#   --force         Pass --force to clawhub install (bypass VirusTotal)
#   --version X.Y.Z Install a specific version
#   --promote       Skip scan, promote staged skill to live
#   --scan-only     Re-scan an already staged skill
#   --list-staged   List all skills in the staging area
#   --staging-dir   Custom staging directory (default: skills/_staging)
#   --live-dir      Custom live directory (default: skills)

set -euo pipefail

# --- Defaults ---
WORKSPACE="${OPENCLAW_WORKSPACE:-${HOME}/.openclaw/workspace}"
STAGING_DIR="${WORKSPACE}/skills/_staging"
LIVE_DIR="${WORKSPACE}/skills"

# --- Colors ---
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

# --- Usage ---
usage() {
  cat <<EOF
Usage: $0 <skill-name> [options]
       $0 --list-staged

Install a ClawHub skill through a sandboxed security pipeline.

Options:
  --force         Pass --force to clawhub (bypass VirusTotal flags)
  --version X.Y.Z Install a specific version
  --promote       Promote a staged skill to live (skip scan)
  --scan-only     Re-scan a skill already in staging
  --list-staged   List all quarantined/staged skills
  --staging-dir   Custom staging directory
  --live-dir      Custom live skill directory

Verdicts:
  PASS  → auto-promoted to live (exit 0)
  WARN  → quarantined, review recommended (exit 0)
  FAIL  → quarantined, deep audit required (exit 2)
EOF
  exit 1
}

# --- Parse args ---
SKILL_NAME=""
FORCE_FLAG=""
VERSION_FLAG=""
PROMOTE_ONLY=false
SCAN_ONLY=false
LIST_STAGED=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --force) FORCE_FLAG="--force"; shift ;;
    --version) VERSION_FLAG="--version $2"; shift 2 ;;
    --promote) PROMOTE_ONLY=true; shift ;;
    --scan-only) SCAN_ONLY=true; shift ;;
    --list-staged) LIST_STAGED=true; shift ;;
    --staging-dir) STAGING_DIR="$2"; shift 2 ;;
    --live-dir) LIVE_DIR="$2"; shift 2 ;;
    --help|-h) usage ;;
    -*) echo "Unknown option: $1"; usage ;;
    *)
      if [[ -z "$SKILL_NAME" ]]; then
        SKILL_NAME="$1"
      else
        echo "Unexpected argument: $1"; usage
      fi
      shift ;;
  esac
done

# --- List staged ---
if $LIST_STAGED; then
  if [[ ! -d "$STAGING_DIR" ]] || [[ -z "$(ls -A "$STAGING_DIR" 2>/dev/null | grep -v '.gitkeep')" ]]; then
    echo "No skills in staging."
  else
    echo -e "${BOLD}Staged skills:${NC}"
    for d in "$STAGING_DIR"/*/; do
      [[ -d "$d" ]] || continue
      name=$(basename "$d")
      version="unknown"
      [[ -f "$d/_meta.json" ]] && version=$(jq -r '.version // "unknown"' "$d/_meta.json" 2>/dev/null)
      echo -e "  ${YELLOW}⏳ $name${NC} (v$version) — $d"
    done
  fi
  exit 0
fi

[[ -z "$SKILL_NAME" ]] && usage

STAGED_PATH="$STAGING_DIR/$SKILL_NAME"
LIVE_PATH="$LIVE_DIR/$SKILL_NAME"

# --- Promote mode ---
if $PROMOTE_ONLY; then
  if [[ ! -d "$STAGED_PATH" ]]; then
    echo -e "${RED}✗ Skill '$SKILL_NAME' not found in staging ($STAGING_DIR)${NC}"
    exit 1
  fi
  if [[ -d "$LIVE_PATH" ]]; then
    echo -e "${YELLOW}⚠ Replacing existing live skill '$SKILL_NAME'${NC}"
    rm -rf "$LIVE_PATH"
  fi
  mv "$STAGED_PATH" "$LIVE_PATH"
  echo -e "${GREEN}✅ Promoted '$SKILL_NAME' → $LIVE_PATH${NC}"
  exit 0
fi

# --- Install to staging ---
if ! $SCAN_ONLY; then
  mkdir -p "$STAGING_DIR"

  if [[ -d "$LIVE_PATH" ]]; then
    echo -e "${YELLOW}⚠ Skill '$SKILL_NAME' already in live. Use 'clawhub update' or remove first.${NC}"
    exit 1
  fi

  # Clean previous staged version
  [[ -d "$STAGED_PATH" ]] && rm -rf "$STAGED_PATH"

  echo -e "${CYAN}📦 Installing '$SKILL_NAME' to staging...${NC}"
  # shellcheck disable=SC2086
  if ! clawhub install "$SKILL_NAME" --dir "$STAGING_DIR" $FORCE_FLAG $VERSION_FLAG 2>&1; then
    echo -e "${RED}✗ clawhub install failed${NC}"
    exit 1
  fi

  if [[ ! -d "$STAGED_PATH" ]]; then
    echo -e "${RED}✗ Skill directory not created. Check the skill name.${NC}"
    exit 1
  fi
  echo ""
else
  if [[ ! -d "$STAGED_PATH" ]]; then
    echo -e "${RED}✗ Skill '$SKILL_NAME' not found in staging. Install first.${NC}"
    exit 1
  fi
fi

# ============================================================
# SECURITY SCAN
# ============================================================
echo -e "${BOLD}🔍 Security Scan: $SKILL_NAME${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

WARNINGS=0
CRITICALS=0

finding() {
  local severity="$1"; local msg="$2"
  case "$severity" in
    CRITICAL)
      echo -e "  ${RED}🔴 CRITICAL: $msg${NC}"
      CRITICALS=$((CRITICALS + 1)) ;;
    WARNING)
      echo -e "  ${YELLOW}🟡 WARNING: $msg${NC}"
      WARNINGS=$((WARNINGS + 1)) ;;
    *)
      echo -e "  ${GREEN}🟢 INFO: $msg${NC}" ;;
  esac
}

# Helper: show matched lines indented
show_matches() {
  echo "$1" | head -20 | sed 's/^/     /'
  local count
  count=$(echo "$1" | wc -l | tr -d ' ')
  [[ $count -gt 20 ]] && echo -e "     ${DIM}... and $((count - 20)) more${NC}"
}

# --- 1. File Inventory ---
echo -e "\n${CYAN}1. File Inventory${NC}"
FILE_COUNT=$(find "$STAGED_PATH" -type f | wc -l | tr -d ' ')
echo "   Total files: $FILE_COUNT"

# Hidden files (excluding .clawhub)
HIDDEN=$(find "$STAGED_PATH" -name ".*" -not -name ".clawhub" -not -path "*/.clawhub/*" -not -name ".gitkeep" 2>/dev/null || true)
if [[ -n "$HIDDEN" ]]; then
  finding "WARNING" "Hidden files found:"
  show_matches "$HIDDEN"
fi

# Symlinks
SYMLINKS=$(find "$STAGED_PATH" -type l 2>/dev/null || true)
if [[ -n "$SYMLINKS" ]]; then
  finding "CRITICAL" "Symlinks detected (path traversal risk):"
  show_matches "$SYMLINKS"
fi

# Binary / non-text files
BINARIES=$(find "$STAGED_PATH" -type f -exec file {} \; | grep -v "text\|JSON\|empty\|data" | grep -v "_meta.json" 2>/dev/null || true)
if [[ -n "$BINARIES" ]]; then
  finding "WARNING" "Non-text files:"
  show_matches "$BINARIES"
fi

# --- 2. Code Pattern Analysis ---
echo -e "\n${CYAN}2. Code Pattern Analysis${NC}"
CODE_GLOBS=("*.js" "*.ts" "*.mjs" "*.cjs" "*.py" "*.sh" "*.rb" "*.pl")

grep_code() {
  local pattern="$1"
  local result=""
  for ext in "${CODE_GLOBS[@]}"; do
    local hits
    hits=$(grep -rn "$pattern" "$STAGED_PATH" --include="$ext" 2>/dev/null || true)
    [[ -n "$hits" ]] && result="${result}${hits}\n"
  done
  echo -e "$result" | sed '/^$/d'
}

# eval / dynamic execution
EVAL_HITS=$(grep_code 'eval\s*(')
if [[ -n "$EVAL_HITS" ]]; then
  finding "CRITICAL" "eval() calls:"
  show_matches "$EVAL_HITS"
fi

FUNC_HITS=$(grep_code 'new Function\|Function(')
if [[ -n "$FUNC_HITS" ]]; then
  finding "CRITICAL" "Dynamic Function() constructor:"
  show_matches "$FUNC_HITS"
fi

# Network calls
NET_HITS=$(grep_code 'fetch(\|axios\|http\.\(get\|post\|request\)\|https\.\(get\|post\|request\)\|urllib\|requests\.\(get\|post\)\|XMLHttpRequest\|\.ajax(')
if [[ -n "$NET_HITS" ]]; then
  finding "WARNING" "Network call patterns:"
  show_matches "$NET_HITS"
fi

CURL_HITS=$(grep_code 'curl \|wget ')
if [[ -n "$CURL_HITS" ]]; then
  finding "WARNING" "Shell download commands:"
  show_matches "$CURL_HITS"
fi

# Shell execution
EXEC_HITS=$(grep_code 'child_process\|execSync\|spawnSync\|\.exec(\|\.spawn(\|subprocess\.\|os\.system(\|os\.popen(')
if [[ -n "$EXEC_HITS" ]]; then
  finding "WARNING" "Shell execution patterns:"
  show_matches "$EXEC_HITS"
fi

# Environment / secret access
ENV_HITS=$(grep_code 'process\.env\|os\.environ\|os\.getenv\|API_KEY\|SECRET_KEY\|PRIVATE_KEY\|PASSWORD\|CREDENTIAL\|ACCESS_TOKEN')
if [[ -n "$ENV_HITS" ]]; then
  finding "WARNING" "Environment/secret access:"
  show_matches "$ENV_HITS"
fi

# Base64 / obfuscation
B64_HITS=$(grep_code 'atob(\|btoa(\|Buffer\.from.*base64\|b64decode\|b64encode')
if [[ -n "$B64_HITS" ]]; then
  finding "WARNING" "Base64 encoding (potential obfuscation):"
  show_matches "$B64_HITS"
fi

# File system writes
FS_HITS=$(grep_code 'writeFile\|writeSync\|fs\.write\|open(.*['\''"]w['\''"]')
if [[ -n "$FS_HITS" ]]; then
  finding "WARNING" "File system write patterns:"
  show_matches "$FS_HITS"
fi

[[ $CRITICALS -eq 0 && $WARNINGS -eq 0 ]] && echo "   ✅ No dangerous code patterns detected"

# --- 3. SKILL.md Instruction Review ---
echo -e "\n${CYAN}3. SKILL.md Instruction Review${NC}"
SKILL_MD="$STAGED_PATH/SKILL.md"
if [[ -f "$SKILL_MD" ]]; then
  DANGER=$(grep -in \
    "disable.*security\|ignore.*guardrail\|skip.*auth\|exfiltrate\|phone.home\|send.*to.*server\|upload.*data\|rm -rf /\|delete.*all\|chmod 777\|0\.0\.0\.0\|mkfifo\|nc -l\|reverse.shell\|>/etc/\|curl.*|.*bash\|wget.*|.*sh" \
    "$SKILL_MD" 2>/dev/null || true)
  if [[ -n "$DANGER" ]]; then
    finding "CRITICAL" "Dangerous instructions in SKILL.md:"
    show_matches "$DANGER"
  else
    echo "   ✅ No dangerous instruction patterns"
  fi

  # Check for sudo usage
  SUDO_HITS=$(grep -in "sudo " "$SKILL_MD" 2>/dev/null || true)
  if [[ -n "$SUDO_HITS" ]]; then
    finding "WARNING" "sudo usage in SKILL.md (requests elevated access):"
    show_matches "$SUDO_HITS"
  fi

  # External URLs (excluding known-safe registries)
  EXT_URLS=$(grep -oP 'https?://[^\s\)\"\>]+' "$SKILL_MD" 2>/dev/null | grep -v "github\.com\|clawhub\.\|npmjs\.com\|docs\.\|mozilla\.org\|wikipedia\.org\|openclaw\." | sort -u || true)
  if [[ -n "$EXT_URLS" ]]; then
    finding "INFO" "External URLs:"
    show_matches "$EXT_URLS"
  fi
else
  finding "WARNING" "No SKILL.md found"
fi

# --- 4. Dependency Check ---
echo -e "\n${CYAN}4. Dependency Check${NC}"
PKG_JSON="$STAGED_PATH/package.json"
if [[ -f "$PKG_JSON" ]]; then
  echo "   package.json found:"
  DEPS=$(jq -r '(.dependencies // {}) + (.devDependencies // {}) | to_entries[] | "   - \(.key): \(.value)"' "$PKG_JSON" 2>/dev/null || echo "   (parse error)")
  [[ -n "$DEPS" ]] && echo "$DEPS" || echo "   (no dependencies)"

  # Install scripts (major supply chain vector)
  INSTALL_SCRIPTS=$(jq -r '.scripts // {} | to_entries[] | select(.key | test("^(pre|post)?install$")) | "   ⚠️ \(.key): \(.value)"' "$PKG_JSON" 2>/dev/null || true)
  if [[ -n "$INSTALL_SCRIPTS" ]]; then
    finding "CRITICAL" "Install lifecycle scripts in package.json:"
    echo "$INSTALL_SCRIPTS"
  fi
else
  echo "   No package.json (documentation-only skill)"
fi

# Also check for requirements.txt, Gemfile, etc.
for depfile in requirements.txt Gemfile go.mod Cargo.toml; do
  if [[ -f "$STAGED_PATH/$depfile" ]]; then
    finding "INFO" "$depfile found — review dependencies manually"
  fi
done

# --- 5. Publisher Verification ---
echo -e "\n${CYAN}5. Publisher Info${NC}"
META="$STAGED_PATH/_meta.json"
ORIGIN="$STAGED_PATH/.clawhub/origin.json"
if [[ -f "$META" ]]; then
  echo "   $(jq -r '"Name: \(.name // "unknown") | Version: \(.version // "unknown")"' "$META" 2>/dev/null)"
fi
if [[ -f "$ORIGIN" ]]; then
  PUB=$(jq -r '.publisher // .author // "unknown"' "$ORIGIN" 2>/dev/null)
  REG=$(jq -r '.registry // "unknown"' "$ORIGIN" 2>/dev/null)
  echo "   Publisher: $PUB | Registry: $REG"
  if [[ "$PUB" == "unknown" ]]; then
    finding "WARNING" "Unknown publisher — cannot verify trust"
  fi
else
  finding "INFO" "No origin.json — publisher unverified"
fi

# ============================================================
# VERDICT
# ============================================================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [[ $CRITICALS -gt 0 ]]; then
  echo -e "${RED}${BOLD}❌ FAIL — $CRITICALS critical, $WARNINGS warning(s)${NC}"
  echo -e "   Quarantined: ${DIM}$STAGED_PATH${NC}"
  echo -e "   ${YELLOW}→ Run a deep security audit before promoting${NC}"
  echo -e "   ${YELLOW}→ Promote after review: $0 $SKILL_NAME --promote${NC}"
  echo ""
  echo "VERDICT:FAIL"
  exit 2
elif [[ $WARNINGS -gt 0 ]]; then
  echo -e "${YELLOW}${BOLD}⚠️  WARN — $WARNINGS warning(s), 0 critical${NC}"
  echo -e "   Quarantined: ${DIM}$STAGED_PATH${NC}"
  echo -e "   ${YELLOW}→ Review warnings above${NC}"
  echo -e "   ${CYAN}→ Promote: $0 $SKILL_NAME --promote${NC}"
  echo ""
  echo "VERDICT:WARN"
  exit 0
else
  echo -e "${GREEN}${BOLD}✅ PASS — Clean. Auto-promoting to live.${NC}"
  if [[ -d "$LIVE_PATH" ]]; then
    rm -rf "$LIVE_PATH"
  fi
  mv "$STAGED_PATH" "$LIVE_PATH"
  echo -e "   Installed: ${GREEN}$LIVE_PATH${NC}"
  echo ""
  echo "VERDICT:PASS"
  exit 0
fi
