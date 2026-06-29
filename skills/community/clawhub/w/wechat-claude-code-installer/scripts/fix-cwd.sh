#!/usr/bin/env bash
# fix-cwd.sh —— 修坑 1：cwd 僵尸字段
# 上游 1.0.0 的 daemon 不读 config.json，只读 sessions/<accountId>.json
# 这里直接改 session 文件
set -euo pipefail

WORK_DIR="${1:-$HOME/Claude Code}"

echo "🔧 修坑 1：修复 cwd"
echo "   目标 cwd: $WORK_DIR"

if ! ls ~/.wechat-claude-code/accounts/*.json >/dev/null 2>&1; then
  echo "❌ 没找到绑定账号。先跑 install.sh"
  exit 1
fi

ACCOUNT=$(ls ~/.wechat-claude-code/accounts/*.json | head -1 | xargs basename | sed 's/.json//')
SESSION_FILE=~/.wechat-claude-code/sessions/$ACCOUNT.json
mkdir -p ~/.wechat-claude-code/sessions

python3 <<PY
import json, os
sf = os.path.expanduser("$SESSION_FILE")
data = {}
if os.path.exists(sf):
    with open(sf) as f: data = json.load(f)
data['workingDirectory'] = "$WORK_DIR"
data.setdefault('state', 'idle')
data.setdefault('chatHistory', [])
data.setdefault('maxHistoryLength', 100)
with open(sf, 'w') as f: json.dump(data, f, ensure_ascii=False, indent=2)
print(f"   ✅ workingDirectory = {data['workingDirectory']}")
PY

echo "   提示：daemon 在跑的话需要重启："
echo "         cd ~/.claude/skills/wechat-claude-code && npm run daemon -- restart"
