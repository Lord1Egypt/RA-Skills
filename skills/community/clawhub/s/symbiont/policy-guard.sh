#!/usr/bin/env bash
# policy-guard.sh -- Tier 2 protection for symbiont (OpenClaw)
#
# Checks proposed tool calls against .symbiont/local-policy.toml deny list.
# Exit codes:
#   0 = allowed (or no policy file found)
#   2 = blocked by policy
#
# Usage: policy-guard.sh <tool_name> <tool_input_json>
#
# Works identically to the policy-guard.sh in symbi-claude-code and
# symbi-gemini-cli. The same .symbiont/local-policy.toml config is
# shared across all three plugins.

set -euo pipefail

TOOL_NAME="${1:-}"
TOOL_INPUT="${2:-{}}"
POLICY_FILE=".symbiont/local-policy.toml"
AUDIT_DIR=".symbiont/audit"

# --- Built-in deny patterns (always active) ---
BUILTIN_COMMAND_DENY=(
  "rm -rf /"
  "rm -rf ~"
  "rm -rf \$HOME"
  "mkfs"
  "dd if=/dev/zero"
  "dd if=/dev/random"
  ":(){ :|:& };:"
  "chmod -R 777 /"
  "chown -R"
  "> /dev/sda"
)

BUILTIN_PATH_DENY=(
  ".env"
  ".ssh/"
  ".aws/"
  ".gnupg/"
  ".config/gcloud/"
  "credentials"
  "id_rsa"
  "id_ed25519"
)

# --- Helper: check if string contains pattern ---
contains_pattern() {
  local haystack="$1"
  local needle="$2"
  [[ "$haystack" == *"$needle"* ]]
}

# --- Helper: log a block event ---
log_block() {
  local reason="$1"
  mkdir -p "$AUDIT_DIR"
  local timestamp
  timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  local entry
  entry=$(jq -nc \
    --arg ts "$timestamp" \
    --arg tool "$TOOL_NAME" \
    --arg reason "$reason" \
    --arg tier "protection" \
    '{timestamp: $ts, tool: $tool, action: "BLOCKED", reason: $reason, tier: $tier}')
  echo "$entry" >> "$AUDIT_DIR/tool-usage.jsonl"
}

# --- Extract command/path from tool input ---
COMMAND=""
FILE_PATH=""

if command -v jq &>/dev/null; then
  COMMAND=$(echo "$TOOL_INPUT" | jq -r '.command // .cmd // .shell_command // ""' 2>/dev/null || echo "")
  FILE_PATH=$(echo "$TOOL_INPUT" | jq -r '.path // .file_path // .filename // ""' 2>/dev/null || echo "")
fi

# --- Check built-in command deny patterns ---
for pattern in "${BUILTIN_COMMAND_DENY[@]}"; do
  if contains_pattern "$COMMAND" "$pattern"; then
    log_block "Built-in deny: command matches '$pattern'"
    echo "BLOCKED: Command matches built-in deny pattern: $pattern"
    exit 2
  fi
done

# --- Check built-in path deny patterns ---
for pattern in "${BUILTIN_PATH_DENY[@]}"; do
  if contains_pattern "$FILE_PATH" "$pattern"; then
    log_block "Built-in deny: path matches '$pattern'"
    echo "BLOCKED: Path matches built-in deny pattern: $pattern"
    exit 2
  fi
done

# --- Check .symbiont/local-policy.toml if it exists ---
if [[ -f "$POLICY_FILE" ]]; then
  # Parse deny.commands from TOML (simple line-based extraction)
  while IFS= read -r line; do
    # Strip quotes and whitespace
    pattern=$(echo "$line" | sed 's/^[[:space:]]*"//;s/"[[:space:]]*,*$//')
    if [[ -n "$pattern" ]] && contains_pattern "$COMMAND" "$pattern"; then
      log_block "Policy deny: command matches '$pattern'"
      echo "BLOCKED: Command matches policy deny pattern: $pattern"
      exit 2
    fi
  done < <(sed -n '/\[deny\]/,/^\[/{ /commands/,/\]/{ /commands/d; /\]/d; p; } }' "$POLICY_FILE" 2>/dev/null)

  # Parse deny.paths from TOML
  while IFS= read -r line; do
    pattern=$(echo "$line" | sed 's/^[[:space:]]*"//;s/"[[:space:]]*,*$//')
    if [[ -n "$pattern" ]] && contains_pattern "$FILE_PATH" "$pattern"; then
      log_block "Policy deny: path matches '$pattern'"
      echo "BLOCKED: Path matches policy deny pattern: $pattern"
      exit 2
    fi
  done < <(sed -n '/\[deny\]/,/^\[/{ /paths/,/\]/{ /paths/d; /\]/d; p; } }' "$POLICY_FILE" 2>/dev/null)

  # Parse deny.branches from TOML (check git operations)
  if [[ "$TOOL_NAME" == *"git"* ]] || contains_pattern "$COMMAND" "git push"; then
    while IFS= read -r line; do
      pattern=$(echo "$line" | sed 's/^[[:space:]]*"//;s/"[[:space:]]*,*$//')
      if [[ -n "$pattern" ]] && contains_pattern "$COMMAND" "$pattern"; then
        log_block "Policy deny: branch matches '$pattern'"
        echo "BLOCKED: Git operation targets protected branch: $pattern"
        exit 2
      fi
    done < <(sed -n '/\[deny\]/,/^\[/{ /branches/,/\]/{ /branches/d; /\]/d; p; } }' "$POLICY_FILE" 2>/dev/null)
  fi
fi

# --- All checks passed ---
exit 0
