#!/usr/bin/env bash
# clawhavoc-scan.sh -- ClawHavoc skill scanner for symbiont (OpenClaw)
#
# Scans a skill directory or SKILL.md for malicious patterns using 40+
# detection rules across 10 attack categories. Mirrors the built-in
# SkillScanner from symbi-runtime.
#
# Usage: clawhavoc-scan.sh <skill-path>
#
# Exit codes:
#   0 = passed (no Critical or High findings)
#   1 = failed (Critical or High findings detected)
#   2 = error (invalid path or arguments)
#
# Output: JSON array of findings to stdout

set -euo pipefail

SKILL_PATH="${1:-}"

if [[ -z "$SKILL_PATH" ]]; then
  echo "Usage: clawhavoc-scan.sh <skill-path>" >&2
  exit 2
fi

if [[ -f "$SKILL_PATH" ]]; then
  # Single file provided
  SCAN_FILES=("$SKILL_PATH")
elif [[ -d "$SKILL_PATH" ]]; then
  # Directory: scan all text files
  mapfile -t SCAN_FILES < <(find "$SKILL_PATH" -type f \( -name "*.md" -o -name "*.sh" -o -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.toml" -o -name "*.json" -o -name "*.yaml" -o -name "*.yml" -o -name "*.txt" -o -name "*.cfg" -o -name "*.ini" \) 2>/dev/null)
else
  echo "Error: '$SKILL_PATH' is not a valid file or directory" >&2
  exit 2
fi

if [[ ${#SCAN_FILES[@]} -eq 0 ]]; then
  echo "No scannable files found in '$SKILL_PATH'" >&2
  exit 2
fi

# --- Detection rules ---
# Format: "SEVERITY~RULE_NAME~PATTERN~DESCRIPTION"
# Uses ~ as delimiter to avoid collision with regex | and : characters
RULES=(
  # Original defense rules
  "CRITICAL~pipe-to-shell~curl.*[|].*sh~Pipe from URL to shell"
  "CRITICAL~pipe-to-shell~wget.*[|].*sh~Pipe from URL to shell"
  "CRITICAL~eval-with-fetch~eval.*fetch[|]~Eval with network fetch"
  "CRITICAL~eval-with-fetch~eval.*curl~Eval with curl"
  "CRITICAL~eval-with-fetch~eval.*wget~Eval with wget"
  "CRITICAL~rm-rf-pattern~rm -rf /~Recursive delete from root"
  "CRITICAL~rm-rf-pattern~rm -rf \\\$HOME~Recursive delete from home"
  "WARNING~base64-decode~base64 -d~Base64 decode (potential obfuscation)"
  "WARNING~base64-decode~base64 --decode~Base64 decode (potential obfuscation)"
  "WARNING~hex-decode~xxd -r~Hex decode (potential obfuscation)"
  "WARNING~env-var-exfil~\\\$\(env\)~Environment variable access"

  # Reverse shells (7 rules)
  "CRITICAL~reverse-shell-bash~/dev/tcp/~Bash reverse shell via /dev/tcp"
  "CRITICAL~reverse-shell-nc~nc -e~Netcat reverse shell"
  "CRITICAL~reverse-shell-nc~nc .*-c~Netcat reverse shell with -c"
  "CRITICAL~reverse-shell-ncat~ncat .*-e~Ncat reverse shell"
  "CRITICAL~reverse-shell-mkfifo~mkfifo.*/tmp/~Named pipe reverse shell"
  "CRITICAL~reverse-shell-python~socket.*connect.*exec~Python reverse shell"
  "CRITICAL~reverse-shell-perl~perl.*socket.*exec~Perl reverse shell"
  "CRITICAL~reverse-shell-ruby~ruby.*TCPSocket~Ruby reverse shell"

  # Credential harvesting (6 rules)
  "HIGH~cred-ssh-keys~\.ssh/id_~SSH private key access"
  "HIGH~cred-ssh-keys~\.ssh/authorized_keys~SSH authorized_keys manipulation"
  "HIGH~cred-aws~\.aws/credentials~AWS credential file access"
  "HIGH~cred-aws~AWS_SECRET_ACCESS_KEY~AWS secret key reference"
  "HIGH~cred-cloud-config~\.config/gcloud~GCloud config access"
  "HIGH~cred-browser-cookies~\.mozilla.*cookies~Browser cookie access"
  "HIGH~cred-browser-cookies~\.chrome.*Cookies~Chrome cookie access"
  "HIGH~cred-keychain~security find-generic-password~macOS Keychain access"

  # Network exfiltration (3 rules)
  "HIGH~exfil-dns-tunnel~dig.*TXT.*@~DNS tunnel exfiltration"
  "HIGH~exfil-devtcp~/dev/tcp/~/dev/tcp outbound connection"
  "HIGH~exfil-nc-outbound~nc [0-9]~Netcat outbound data transfer"

  # Process injection (4 rules)
  "CRITICAL~inject-ptrace~ptrace~Ptrace-based process injection"
  "CRITICAL~inject-ld-preload~LD_PRELOAD~LD_PRELOAD injection"
  "CRITICAL~inject-proc-mem~/proc/.*/mem~/proc/mem manipulation"
  "CRITICAL~inject-gdb-attach~gdb.*attach~GDB process attach"

  # Privilege escalation (5 rules)
  "HIGH~privesc-sudo-nopasswd~NOPASSWD~Sudo NOPASSWD configuration"
  "HIGH~privesc-setuid~chmod.*[ug]\+s~Setuid/setgid bit manipulation"
  "HIGH~privesc-setcap~setcap.*cap_~Linux capability manipulation"
  "HIGH~privesc-chown-root~chown root~Chown to root"
  "HIGH~privesc-nsenter~nsenter~Namespace entry (container escape)"

  # Symlink / path traversal (2 rules)
  "MEDIUM~traversal-symlink~ln -s.*/tmp/~Symlink escape attempt"
  "MEDIUM~traversal-deep-path~\.\.\/\.\.\/\.\.\/\.\.\/~Deep path traversal"

  # Downloader chains (3 rules)
  "MEDIUM~download-curl-save~curl.*-o ~Curl download to file"
  "MEDIUM~download-wget-save~wget.*-O ~Wget download to file"
  "MEDIUM~download-chmod-exec~chmod.*\+x.*(curl|wget)~Download and make executable"
)

FINDINGS="[]"
HAS_CRITICAL_OR_HIGH=false

for file in "${SCAN_FILES[@]}"; do
  [[ -f "$file" ]] || continue
  LINE_NUM=0
  while IFS= read -r line || [[ -n "$line" ]]; do
    LINE_NUM=$((LINE_NUM + 1))
    for rule in "${RULES[@]}"; do
      IFS='~' read -r severity rule_name pattern description <<< "$rule"
      if echo "$line" | grep -qE "$pattern" 2>/dev/null; then
        REL_PATH="${file#$SKILL_PATH/}"
        [[ "$REL_PATH" == "$file" ]] && REL_PATH=$(basename "$file")

        if command -v jq &>/dev/null; then
          FINDING=$(jq -nc \
            --arg sev "$severity" \
            --arg rule "$rule_name" \
            --arg msg "$description" \
            --arg file "$REL_PATH" \
            --argjson line "$LINE_NUM" \
            '{severity: $sev, rule: $rule, message: $msg, file: $file, line: $line}')
          FINDINGS=$(echo "$FINDINGS" | jq --argjson f "$FINDING" '. + [$f]')
        else
          echo "[$severity] $rule_name: $description ($REL_PATH:$LINE_NUM)"
        fi

        if [[ "$severity" == "CRITICAL" || "$severity" == "HIGH" ]]; then
          HAS_CRITICAL_OR_HIGH=true
        fi
      fi
    done
  done < "$file"
done

# Output results
if command -v jq &>/dev/null; then
  TOTAL=$(echo "$FINDINGS" | jq 'length')
  CRITICAL=$(echo "$FINDINGS" | jq '[.[] | select(.severity == "CRITICAL")] | length')
  HIGH=$(echo "$FINDINGS" | jq '[.[] | select(.severity == "HIGH")] | length')
  MEDIUM=$(echo "$FINDINGS" | jq '[.[] | select(.severity == "MEDIUM")] | length')
  WARNING=$(echo "$FINDINGS" | jq '[.[] | select(.severity == "WARNING")] | length')

  jq -nc \
    --argjson passed "$(if $HAS_CRITICAL_OR_HIGH; then echo false; else echo true; fi)" \
    --argjson total "$TOTAL" \
    --argjson critical "$CRITICAL" \
    --argjson high "$HIGH" \
    --argjson medium "$MEDIUM" \
    --argjson warning "$WARNING" \
    --argjson findings "$FINDINGS" \
    '{
      passed: $passed,
      total_findings: $total,
      summary: {critical: $critical, high: $high, medium: $medium, warning: $warning},
      findings: $findings
    }'
else
  if $HAS_CRITICAL_OR_HIGH; then
    echo "FAILED: Critical or High findings detected"
  else
    echo "PASSED: No Critical or High findings"
  fi
fi

if $HAS_CRITICAL_OR_HIGH; then
  exit 1
else
  exit 0
fi
