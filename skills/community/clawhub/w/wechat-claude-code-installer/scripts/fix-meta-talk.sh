#!/usr/bin/env bash
# fix-meta-talk.sh —— 修坑 2：关闭 hook 元话术泄露
# 给 session 设 systemPrompt 覆盖 claudeception 等 hook 注入
set -euo pipefail

PROMPT_TEXT="${1:-直接简洁回答用户的问题。不要在末尾追加任何"评估""技能提取"或类似的元话术。}"

echo "🔧 修坑 2：关闭 hook 元话术泄露"

if ! ls ~/.wechat-claude-code/accounts/*.json >/dev/null 2>&1; then
  echo "❌ 没找到绑定账号。先跑 install.sh"
  exit 1
fi

ACCOUNT=$(ls ~/.wechat-claude-code/accounts/*.json | head -1 | xargs basename | sed 's/.json//')
SESSION_FILE=~/.wechat-claude-code/sessions/$ACCOUNT.json
mkdir -p ~/.wechat-claude-code/sessions

python3 - <<PY
import json, os
sf = os.path.expanduser("$SESSION_FILE")
data = {}
if os.path.exists(sf):
    with open(sf) as f: data = json.load(f)
data['systemPrompt'] = """$PROMPT_TEXT"""
data.setdefault('workingDirectory', os.path.expanduser('~/Claude Code'))
data.setdefault('state', 'idle')
data.setdefault('chatHistory', [])
data.setdefault('maxHistoryLength', 100)
with open(sf, 'w') as f: json.dump(data, f, ensure_ascii=False, indent=2)
print(f"   ✅ systemPrompt 已设")
print(f"      内容: {data['systemPrompt'][:60]}...")
PY

echo ""
echo "   备选：在微信里直接发 /prompt <你想要的提示词> 也能改。"
