#!/bin/bash
# skill-lifecycle-guardian 变更检测脚本
# 基于 registry path 字段定位 SKILL.md，确定性 hash 对比
# 输出：NO_CHANGES 或 CHANGES:skill1:old->new,skill2:old->new

REGISTRY="$HOME/.openclaw/workspace/memory/skill-registry.json"

if [ ! -f "$REGISTRY" ]; then
    echo "ERROR: registry not found"
    exit 1
fi

python3 << 'PYEOF'
import json, hashlib, os, sys

REGISTRY = os.path.expanduser("~/.openclaw/workspace/memory/skill-registry.json")

with open(REGISTRY) as f:
    data = json.load(f)

changed = []

# Path whitelist — only read SKILL.md from known skill directories
ALLOWED_ROOTS = [
    os.path.expanduser("~/.openclaw/workspace/skills"),
    os.path.expanduser("~/.openclaw/workspace-team/skills"),
    os.path.expanduser("~/.openclaw/workspace-study/skills"),
    os.path.expanduser("~/.openclaw/skills"),
    os.path.expanduser("~/.openclaw/plugin-skills"),
]

for name, info in data.get("skills", {}).items():
    path = info.get("path", "")
    reg_hash = info.get("hash", "")

    if not path or not os.path.isfile(path):
        changed.append(f"{name}:MISSING_FILE")
        continue

    # Path safety: resolve symlinks and verify against whitelist
    real_path = os.path.realpath(path)
    if not any(real_path.startswith(os.path.realpath(root)) for root in ALLOWED_ROOTS):
        continue

    with open(path, "rb") as f:
        current_hash = hashlib.md5(f.read()).hexdigest()

    if current_hash != reg_hash:
        changed.append(f"{name}:{reg_hash[:8]}->{current_hash[:8]}")

if not changed:
    print("NO_CHANGES")
else:
    print("CHANGES:" + ",".join(changed))
PYEOF