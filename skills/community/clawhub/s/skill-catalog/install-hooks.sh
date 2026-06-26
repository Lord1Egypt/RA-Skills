#!/bin/bash
# 安装 Git Hooks - pre-commit + post-merge
# 在 skill 目录变更时自动更新 INDEX.md

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
GIT_DIR="$WORKSPACE_DIR/.git"
HOOKS_DIR="$GIT_DIR/hooks"

echo "🔧 安装 Skill Registry Git Hooks..."
echo "   Workspace: $WORKSPACE_DIR"
echo "   Git hooks: $HOOKS_DIR"
echo ""

# pre-commit hook
cat > "$HOOKS_DIR/pre-commit" << 'HOOKEOF'
#!/bin/bash
# Skill Registry pre-commit hook
# 自动更新 INDEX.md 并加入当前 commit

SKILLS_DIR="$(git rev-parse --show-toplevel)/skills"
REGISTER_SCRIPT="$SKILLS_DIR/skill-index/register.sh"
INDEX_FILE="$SKILLS_DIR/INDEX.md"

if [ -f "$REGISTER_SCRIPT" ] && git diff --cached --name-only | grep -q "^skills/"; then
    echo "🔄 Skill 目录有变更，更新索引..."
    bash "$REGISTER_SCRIPT" --quiet
    git add "$INDEX_FILE"
    echo "✅ INDEX.md 已更新并加入 commit"
fi
HOOKEOF
chmod +x "$HOOKS_DIR/pre-commit"
echo "   ✅ pre-commit hook 已安装"

# post-merge hook
cat > "$HOOKS_DIR/post-merge" << 'HOOKEOF'
#!/bin/bash
# Skill Registry post-merge hook
# pull 后自动更新索引

SKILLS_DIR="$(git rev-parse --show-toplevel)/skills"
REGISTER_SCRIPT="$SKILLS_DIR/skill-index/register.sh"

if [ -f "$REGISTER_SCRIPT" ]; then
    echo "🔄 Pull 完成，更新 skill 索引..."
    bash "$REGISTER_SCRIPT" --quiet
fi
HOOKEOF
chmod +x "$HOOKS_DIR/post-merge"
echo "   ✅ post-merge hook 已安装"

echo ""
echo "✅ 全部安装完成！"
echo "   - commit 时自动更新索引（如果 skills/ 目录有变更）"
echo "   - pull 时自动更新索引"
