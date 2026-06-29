#!/usr/bin/env bash
# doctor.sh - install-time health check (read-only, reports issues without fixing)
set -eu

echo "============================================================"
echo "  wechat-claude-code-installer :: doctor"
echo "============================================================"
echo ""

# 1. Node version
echo "1) Node version"
if command -v node >/dev/null 2>&1; then
  V=$(node --version)
  MAJOR=$(echo "$V" | sed 's/v//' | cut -d. -f1)
  if [ "$MAJOR" -ge 18 ]; then
    echo "   OK $V (>=18)"
  else
    echo "   FAIL $V (need >=18)"
  fi
else
  echo "   FAIL no node installed"
fi
echo ""

# 2. upstream wechat-claude-code
echo "2) Upstream wechat-claude-code"
if [ -d "$HOME/.claude/skills/wechat-claude-code" ]; then
  echo "   WARN already exists at ~/.claude/skills/wechat-claude-code"
  echo "        - first install: rm -rf and re-run install.sh"
  echo "        - upgrade: cd ~/.claude/skills/wechat-claude-code && git pull && npm install"
else
  echo "   OK not installed yet"
fi
echo ""

# 3. account binding
echo "3) WeChat account binding"
ACCT_DIR="$HOME/.wechat-claude-code/accounts"
if [ -d "$ACCT_DIR" ] && ls "$ACCT_DIR"/*.json >/dev/null 2>&1; then
  CNT=$(ls "$ACCT_DIR"/*.json 2>/dev/null | wc -l | tr -d ' ')
  echo "   WARN already bound: $CNT account(s)"
else
  echo "   OK not bound (will write after QR scan)"
fi
echo ""

# 4. ANTHROPIC_BASE_URL compliance check (most important)
echo "4) Anthropic API endpoint (compliance)"
BASE_URL="${ANTHROPIC_BASE_URL:-}"
if [ -z "$BASE_URL" ] && [ -f "$HOME/.claude/settings.json" ]; then
  BASE_URL=$(python3 -c "import json,sys; d=json.load(open('$HOME/.claude/settings.json')); print(d.get('env',{}).get('ANTHROPIC_BASE_URL',''))" 2>/dev/null || echo "")
fi
if [ -z "$BASE_URL" ]; then
  echo "   ANTHROPIC_BASE_URL: (not set)"
  echo "   OK Will go to Anthropic official"
elif echo "$BASE_URL" | grep -q "api.anthropic.com"; then
  echo "   ANTHROPIC_BASE_URL: $BASE_URL"
  echo "   OK Anthropic official"
elif echo "$BASE_URL" | grep -qE "localhost|127\.0\.0\.1"; then
  echo "   ANTHROPIC_BASE_URL: $BASE_URL"
  echo "   WARN Routes through local proxy. Implications:"
  echo "        - all WeChat conversations go through this proxy"
  echo "        - if proxy is a company gateway, conversations may be logged"
  echo "        - if proxy stops, daemon receives but cannot respond"
else
  echo "   ANTHROPIC_BASE_URL: $BASE_URL"
  echo "   INFO third-party proxy. Verify proxy logging policy."
fi
echo ""

# 5. OS check
echo "5) Operating system"
if [ "$(uname -s)" = "Darwin" ]; then
  echo "   OK macOS (primary platform for this skill)"
else
  echo "   WARN non-macOS ($(uname -s))"
  echo "        upstream supports systemd/nohup, but fix scripts only tested on macOS"
fi
echo ""

# 6. Upstream drift check (v0.3 新增)
echo "6) Upstream drift check"
if [ -d "$HOME/.claude/skills/wechat-claude-code/.git" ]; then
  CHECK="$(dirname "$0")/check-upstream.sh"
  if [ -x "$CHECK" ]; then
    LOCAL=$(cd "$HOME/.claude/skills/wechat-claude-code" && git log -1 --format=%h 2>/dev/null)
    REMOTE=$(/usr/bin/curl -s --max-time 5 \
      "https://api.github.com/repos/Wechat-ggGitHub/wechat-claude-code/commits/main" \
      | python3 -c "import json,sys; print(json.load(sys.stdin).get('sha','')[:7])" 2>/dev/null)
    if [ -n "$LOCAL" ] && [ -n "$REMOTE" ]; then
      if [ "$LOCAL" = "$REMOTE" ]; then
        echo "   OK local ($LOCAL) = remote ($REMOTE)"
      else
        echo "   WARN upstream drift: local $LOCAL → remote $REMOTE"
        echo "        run check-upstream.sh --since to see what's new"
      fi
    else
      echo "   INFO 网络不通或 API 失败，跳过"
    fi
  fi
else
  echo "   INFO 上游未安装"
fi
echo ""

echo "============================================================"
echo "  doctor done. If all OK above, run install.sh next."
echo "============================================================"
