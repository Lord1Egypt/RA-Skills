#!/usr/bin/env bash
# redline skill 卸载脚本
# 用法: ./uninstall.sh

set -euo pipefail

LINK_PATH="$HOME/.claude/skills/redline"
SETTINGS="$HOME/.claude/settings.json"
RL_HOME="$HOME/.claude/redline"
PIDFILE="$RL_HOME/server.pid"

echo "redline skill 卸载"
echo ""

# ---------- 1. 杀 server ----------
if [[ -f "$PIDFILE" ]]; then
  PID=$(cat "$PIDFILE" 2>/dev/null || true)
  if [[ -n "$PID" ]] && kill -0 "$PID" 2>/dev/null; then
    kill "$PID" 2>/dev/null || true
    echo "✓ server 已停止 (pid=$PID)"
  else
    echo "  server 未在运行"
  fi
  rm -f "$PIDFILE"
else
  echo "  server 未在运行"
fi

# ---------- 2. 移除软链接 ----------
if [[ -L "$LINK_PATH" ]]; then
  rm "$LINK_PATH"
  echo "✓ 软链接已移除: $LINK_PATH"
elif [[ -e "$LINK_PATH" ]]; then
  echo "⚠ $LINK_PATH 不是软链接，跳过（请手动处理）"
else
  echo "  软链接不存在，跳过"
fi

# ---------- 3. 移除 hook ----------
if [[ -f "$SETTINGS" ]]; then
  SETTINGS="$SETTINGS" python3 <<'PYEOF'
import json, os
from pathlib import Path

settings_path = Path(os.environ["SETTINGS"])
with open(settings_path, "r", encoding="utf-8") as f:
    cfg = json.load(f)

hooks = cfg.get("hooks", {})
ups_list = hooks.get("UserPromptSubmit", [])

new_list = []
removed = False
for entry in ups_list:
    new_hooks = [
        h for h in entry.get("hooks", [])
        if not h.get("command", "").endswith("/redline/hook.sh")
    ]
    if len(new_hooks) < len(entry.get("hooks", [])):
        removed = True
    if new_hooks:
        entry["hooks"] = new_hooks
        new_list.append(entry)

if removed:
    hooks["UserPromptSubmit"] = new_list
    if not new_list:
        del hooks["UserPromptSubmit"]
    if not hooks:
        del cfg["hooks"]
    with open(settings_path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"✓ hook 已从 {settings_path} 移除")
else:
    print("  hook 未找到，跳过")
PYEOF
else
  echo "  settings.json 不存在，跳过"
fi

echo ""
echo "卸载完成。skill 源文件未删除，可随时重新 ./install.sh 安装。"
