#!/usr/bin/env bash
# redline skill 安装脚本
# 用法: ./install.sh

set -euo pipefail

# ---------- 路径解析 ----------
SOURCE="${BASH_SOURCE[0]}"
while [[ -h "$SOURCE" ]]; do
  DIR="$(cd -P "$(dirname "$SOURCE")" && pwd)"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
done
SKILL_DIR="$(cd -P "$(dirname "$SOURCE")" && pwd)"

SKILLS_HOME="$HOME/.claude/skills"
LINK_PATH="$SKILLS_HOME/redline"
SETTINGS="$HOME/.claude/settings.json"
HOOK_CMD="$SKILL_DIR/hook.sh"

echo "redline skill 安装"
echo "  skill 目录: $SKILL_DIR"
echo ""

# ---------- 1. chmod ----------
chmod +x "$SKILL_DIR"/*.sh
echo "✓ 脚本已设为可执行"

# ---------- 2. 软链接 ----------
mkdir -p "$SKILLS_HOME"
if [[ -L "$LINK_PATH" ]]; then
  EXISTING=$(readlink "$LINK_PATH")
  if [[ "$EXISTING" == "$SKILL_DIR" ]]; then
    echo "✓ 软链接已存在且正确: $LINK_PATH → $SKILL_DIR"
  else
    ln -sfn "$SKILL_DIR" "$LINK_PATH"
    echo "✓ 软链接已更新: $LINK_PATH → $SKILL_DIR (原: $EXISTING)"
  fi
elif [[ -e "$LINK_PATH" ]]; then
  echo "⚠ $LINK_PATH 已存在但不是软链接，跳过（请手动处理）"
else
  ln -s "$SKILL_DIR" "$LINK_PATH"
  echo "✓ 软链接已创建: $LINK_PATH → $SKILL_DIR"
fi

# ---------- 3. 配置 hook ----------
HOOK_CMD="$HOOK_CMD" SETTINGS="$SETTINGS" python3 <<'PYEOF'
import json, os, sys
from pathlib import Path

settings_path = Path(os.environ["SETTINGS"])
hook_cmd = os.environ["HOOK_CMD"]

if settings_path.exists():
    with open(settings_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
else:
    settings_path.parent.mkdir(parents=True, exist_ok=True)
    cfg = {}

hooks = cfg.setdefault("hooks", {})
ups_list = hooks.setdefault("UserPromptSubmit", [])

already = False
for entry in ups_list:
    for h in entry.get("hooks", []):
        if h.get("command", "").endswith("/redline/hook.sh"):
            if h["command"] == hook_cmd:
                already = True
            else:
                h["command"] = hook_cmd
                print(f"✓ hook 路径已更新: {hook_cmd}")
            break

if not already:
    found_updated = any(
        h.get("command", "") == hook_cmd
        for entry in ups_list
        for h in entry.get("hooks", [])
    )
    if not found_updated:
        ups_list.append({
            "hooks": [{"type": "command", "command": hook_cmd}]
        })
        print(f"✓ hook 已添加到 {settings_path}")
    else:
        print(f"✓ hook 已存在: {hook_cmd}")
else:
    print(f"✓ hook 已存在: {hook_cmd}")

with open(settings_path, "w", encoding="utf-8") as f:
    json.dump(cfg, f, indent=2, ensure_ascii=False)
    f.write("\n")
PYEOF

echo ""
echo "安装完成！使用方式:"
echo "  1. 让 Claude Code 生成一个 HTML 文件"
echo "  2. 对 Claude 说"标注 xxx.html""
echo "  3. 在浏览器中标注元素并提交反馈"
echo "  4. 回到 Claude Code 随便说一句话，反馈会自动应用"
