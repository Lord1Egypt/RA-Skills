#!/bin/bash
# publish-check.sh — Pre-publish privacy scan for ClawHub skills.
# Usage: bash publish-check.sh <skill-directory>
#
# Scans a skill directory for leaked secrets, credentials, personal info, and internal IPs.
# Principle: false positives are acceptable, missed leaks are not.

set -uo pipefail

RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
GREEN='\033[0;32m'
NC='\033[0m'

CRITICAL=0
WARNING=0
INFO=0

RESULTS_FILE=$(mktemp)
trap "rm -f $RESULTS_FILE" EXIT

log_finding() {
  local level="$1" category="$2" file="$3" line_num="$4" content="$5" suggestion="$6"
  echo "${level}|${category}|${file}|${line_num}|${content}|${suggestion}" >> "$RESULTS_FILE"
  case "$level" in
    CRITICAL) CRITICAL=$((CRITICAL + 1)) ;;
    WARNING)  WARNING=$((WARNING + 1)) ;;
    INFO)     INFO=$((INFO + 1)) ;;
  esac
}

is_placeholder() {
  local text="$1"
  echo "$text" | grep -qiE 'your-|your[_.]|<YOUR|<TOKEN>|<API|<PASSWORD>|<EMAIL>|<USERNAME>|example\.com|placeholder|<.*>|\$\{|\$TOKEN|\$API_KEY|\$SECRET|\$KEY|\$PASS|your_token|your_api|your_key|your_secret|your_pass|<PATH|your-server|yourdomain|<AUTHOR>|<SLUG>|your-username|your-api-token|your-password|you@example\.com|your-server-ip' 2>/dev/null
}

main() {
  local skill_dir="${1:?Usage: bash publish-check.sh <skill-directory>}"
  [ ! -d "$skill_dir" ] && { echo -e "${RED}Error: Directory not found: $skill_dir${NC}"; exit 1; }

  echo -e "${BLUE}🛡️  Running privacy scan...${NC}"
  echo -e "   Directory: $skill_dir"
  echo ""

  local -a files=()
  while IFS= read -r -d '' f; do
    files+=("$f")
  done < <(find "$skill_dir" -type f \( \
    -name "*.md" -o -name "*.txt" -o -name "*.sh" -o -name "*.py" -o \
    -name "*.js" -o -name "*.ts" -o -name "*.json" -o -name "*.yaml" -o \
    -name "*.yml" -o -name "*.toml" -o -name "*.ini" -o -name "*.cfg" -o \
    -name "*.conf" -o -name "*.env" -o -name "*.spec" -o -name "*.ks" -o \
    -name "Makefile" -o -name "Dockerfile" -o \
    -name "*.html" -o -name "*.css" -o -name "*.xml" \
  \) -print0 2>/dev/null)

  [ ${#files[@]} -eq 0 ] && { echo -e "${YELLOW}⚠️  No scannable text files found.${NC}"; exit 0; }

  for file in "${files[@]}"; do
    local file_base
    file_base=$(basename "$file")

    # === Token / API Key ===
    while IFS= read -r match; do
      [ -z "$match" ] && continue
      local line_num="${match%%:*}"
      local content="${match#*:}"
      is_placeholder "$content" && continue
      log_finding "CRITICAL" "Token/API Key" "$file_base" "$line_num" "Possible token detected" "Remove or replace with a placeholder (e.g. <YOUR_TOKEN>)"
    done < <(grep -nE 'sk-[A-Za-z0-9]{10,}|ghp_[A-Za-z0-9]{10,}|github_pat_[A-Za-z0-9]{10,}|gpg_[A-Za-z0-9]{10,}|xox[baprs]-[A-Za-z0-9-]{10,}|glpat-[A-Za-z0-9-]{10,}|eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,}' "$file" 2>/dev/null || true)

    # === Password assignment ===
    while IFS= read -r match; do
      [ -z "$match" ] && continue
      local line_num="${match%%:*}"
      local content="${match#*:}"
      is_placeholder "$content" && continue
      log_finding "CRITICAL" "Password" "$file_base" "$line_num" "Password assignment detected: $(echo "$content" | head -c 80)" "Remove or replace with placeholder"
    done < <(grep -niE '(password|passwd|pwd)[[:space:]]*[=:][[:space:]]*[^[:space:]]+' "$file" 2>/dev/null || true)

    # === Private key ===
    while IFS= read -r match; do
      [ -z "$match" ] && continue
      local line_num="${match%%:*}"
      local content="${match#*:}"
      is_placeholder "$content" && continue
      log_finding "CRITICAL" "Private Key" "$file_base" "$line_num" "Private key content detected" "Remove the private key file immediately"
    done < <(grep -nE 'BEGIN.*PRIVATE KEY' "$file" 2>/dev/null || true)

    # === .env actual values ===
    if echo "$file_base" | grep -qi '\.env'; then
      while IFS= read -r line; do
        [ -z "$line" ] && continue
        [[ "$line" =~ ^[[:space:]]*# ]] && continue
        [[ "$line" =~ ^[[:space:]]*$ ]] && continue
        is_placeholder "$line" && continue
        log_finding "CRITICAL" ".env Actual Value" "$file_base" "N" ".env contains actual value: $(echo "$line" | head -c 80)" "Delete .env or replace all values with placeholders"
      done < "$file"
    fi

    # === Hardcoded Bearer Token ===
    while IFS= read -r match; do
      [ -z "$match" ] && continue
      local line_num="${match%%:*}"
      local content="${match#*:}"
      is_placeholder "$content" && continue
      log_finding "CRITICAL" "Hardcoded Bearer Token" "$file_base" "$line_num" "Hardcoded Bearer token: $(echo "$content" | head -c 80)" "Use environment variable or placeholder"
    done < <(grep -nE 'Authorization:[[:space:]]*Bearer[[:space:]]+[A-Za-z0-9_./+-]{8,}' "$file" 2>/dev/null || true)

    # === Personal email ===
    while IFS= read -r match; do
      [ -z "$match" ] && continue
      local line_num="${match%%:*}"
      local content="${match#*:}"
      is_placeholder "$content" && continue
      echo "$content" | grep -qiE '@(example\.com|openeuler\.org|fedoraproject\.org|redhat\.com|google\.com|microsoft\.com|amazon\.com|buildteam@)' 2>/dev/null && continue
      log_finding "WARNING" "Personal Email" "$file_base" "$line_num" "Personal email: $(echo "$content" | head -c 80)" "Replace with you@example.com"
    done < <(grep -nE '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' "$file" 2>/dev/null || true)

    # === Personal path ===
    while IFS= read -r match; do
      [ -z "$match" ] && continue
      local line_num="${match%%:*}"
      local content="${match#*:}"
      is_placeholder "$content" && continue
      log_finding "WARNING" "Personal Path" "$file_base" "$line_num" "Personal path: $(echo "$content" | head -c 80)" "Replace with a generic path"
    done < <(grep -nE '(/home/[a-zA-Z][a-zA-Z0-9_-]+/|/Users/[a-zA-Z][a-zA-Z0-9_-]+/)' "$file" 2>/dev/null || true)

    # === Internal IP ===
    while IFS= read -r match; do
      [ -z "$match" ] && continue
      local line_num="${match%%:*}"
      local content="${match#*:}"
      is_placeholder "$content" && continue
      log_finding "CRITICAL" "Internal IP" "$file_base" "$line_num" "Internal IP: $(echo "$content" | head -c 80)" "Remove or replace with placeholder"
    done < <(grep -nE '(192\.168\.[0-9]{1,3}\.[0-9]{1,3}|10\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}|172\.(1[6-9]|2[0-9]|3[01])\.[0-9]{1,3}\.[0-9]{1,3})' "$file" 2>/dev/null || true)

    # === Public key / SSH key ===
    while IFS= read -r match; do
      [ -z "$match" ] && continue
      local line_num="${match%%:*}"
      local content="${match#*:}"
      log_finding "INFO" "Public Key/SSH Key" "$file_base" "$line_num" "Public key / SSH key detected" "Confirm whether this should be public"
    done < <(grep -nE '(BEGIN.*PUBLIC KEY|ssh-rsa[[:space:]]+[A-Za-z0-9+/=]{50,})' "$file" 2>/dev/null || true)
  done

  # === SKILL.md frontmatter checks ===
  local skill_md="$skill_dir/SKILL.md"
  if [ -f "$skill_md" ]; then
    local author
    author=$(grep -E '^author:' "$skill_md" 2>/dev/null | head -1 | sed 's/^author:[[:space:]]*//' || true)
    if [ -n "$author" ] && [ "$author" != "OS Build Agent" ] && [ "$author" != "OBS Agent" ] && [ "$author" != "<AUTHOR>" ]; then
      log_finding "INFO" "Frontmatter Author" "SKILL.md" "$(grep -n '^author:' "$skill_md" 2>/dev/null | head -1 | cut -d: -f1)" "author: $author — intentionally public?" "Change to a generic name or remove if unwanted"
    fi

    local repo
    repo=$(grep -E '^repository:' "$skill_md" 2>/dev/null | head -1 | sed 's/^repository:[[:space:]]*//' || true)
    if [ -n "$repo" ]; then
      if echo "$repo" | grep -qiE 'github\.com/[a-zA-Z0-9_-]+/|gitlab\.com/[a-zA-Z0-9_-]+/|atomgit\.com/[a-zA-Z0-9_-]+/|gitcode\.com/[a-zA-Z0-9_-]+/' 2>/dev/null; then
        if echo "$repo" | grep -qiE 'your-username|<USERNAME>' 2>/dev/null; then
          : # placeholder, skip
        else
          log_finding "INFO" "Frontmatter Repository" "SKILL.md" "$(grep -n '^repository:' "$skill_md" 2>/dev/null | head -1 | cut -d: -f1)" "Personal repo link: $repo" "Confirm whether this should be public"
        fi
      fi
    fi

    # metadata env exposure
    if grep -q 'metadata:' "$skill_md" 2>/dev/null; then
      local meta_block
      meta_block=$(sed -n '/^metadata:/,/^[a-z]/p' "$skill_md" 2>/dev/null | head -20)
      if echo "$meta_block" | grep -qiE 'env|\.env|TOKEN|SECRET|KEY|PASSWORD|CREDENTIAL' 2>/dev/null; then
        log_finding "INFO" "Metadata Env Exposure" "SKILL.md" "$(grep -n 'metadata:' "$skill_md" 2>/dev/null | head -1 | cut -d: -f1)" "Metadata exposes env variable configuration" "Confirm whether credential access method should be public"
      fi
    fi
  fi

  print_report "$skill_dir"
}

print_report() {
  local skill_dir="$1"
  local skill_name
  skill_name=$(basename "$skill_dir")
  local version
  version=$(grep -E '^version:' "$skill_dir/SKILL.md" 2>/dev/null | head -1 | sed 's/^version:[[:space:]]*//' || echo "N/A")

  echo "═══════════════════════════════════════════════"
  echo "🛡️  Privacy Scan Report"
  echo "═══════════════════════════════════════════════"
  echo "Skill:     $skill_name"
  echo "Directory: $skill_dir"
  echo "Version:   $version"
  echo "───────────────────────────────────────────────"

  if [ $((CRITICAL + WARNING + INFO)) -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ No privacy issues found!${NC}"
    echo ""
    echo "Result: ✅ SAFE TO PUBLISH"
    echo "═══════════════════════════════════════════════"
    return
  fi

  while IFS='|' read -r level category file line_num content suggestion; do
    [ "$level" != "CRITICAL" ] && continue
    echo ""
    echo -e "${RED}🚨 [CRITICAL] $category${NC}"
    echo "   File:     $file"
    [ "$line_num" != "N" ] && echo "   Line:     $line_num"
    echo "   Detail:   $(echo "$content" | head -c 100)"
    echo "   Fix:      $suggestion"
  done < "$RESULTS_FILE"

  while IFS='|' read -r level category file line_num content suggestion; do
    [ "$level" != "WARNING" ] && continue
    echo ""
    echo -e "${YELLOW}⚠️  [WARNING] $category${NC}"
    echo "   File:     $file"
    [ "$line_num" != "N" ] && echo "   Line:     $line_num"
    echo "   Detail:   $(echo "$content" | head -c 100)"
    echo "   Fix:      $suggestion"
  done < "$RESULTS_FILE"

  while IFS='|' read -r level category file line_num content suggestion; do
    [ "$level" != "INFO" ] && continue
    echo ""
    echo -e "${BLUE}💬 [INFO] $category${NC}"
    echo "   File:     $file"
    [ "$line_num" != "N" ] && echo "   Line:     $line_num"
    echo "   Detail:   $(echo "$content" | head -c 100)"
    echo "   Note:     $suggestion"
  done < "$RESULTS_FILE"

  echo ""
  echo "───────────────────────────────────────────────"
  echo -e "Summary: ${RED}🚨 CRITICAL $CRITICAL${NC} | ${YELLOW}⚠️  WARNING $WARNING${NC} | ${BLUE}💬 INFO $INFO${NC}"
  echo "───────────────────────────────────────────────"

  if [ $CRITICAL -gt 0 ]; then
    echo -e "\n${RED}❌ Result: BLOCKED — fix $CRITICAL critical issue(s) before publishing${NC}"
  elif [ $WARNING -gt 0 ]; then
    echo -e "\n${YELLOW}⚠️  Result: $WARNING warning(s) — recommended to fix before publishing${NC}"
  elif [ $INFO -gt 0 ]; then
    echo -e "\n${BLUE}💬 Result: $INFO info item(s) — confirm before publishing${NC}"
  else
    echo -e "\n${GREEN}✅ Result: SAFE TO PUBLISH${NC}"
  fi
  echo "═══════════════════════════════════════════════"
}

main "$@"
