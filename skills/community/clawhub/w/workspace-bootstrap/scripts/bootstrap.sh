#!/bin/bash
# workspace-bootstrap - 自动创建目录结构并复制模板
# 版本: v0.2.0

set -e

WORKSPACE_ROOT=${1:-"."}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATES_DIR="$SCRIPT_DIR/../templates"

echo "🚀 Creating workspace structure in: $WORKSPACE_ROOT"

# 创建核心目录
mkdir -p "$WORKSPACE_ROOT/agents/main"
mkdir -p "$WORKSPACE_ROOT/memory"
mkdir -p "$WORKSPACE_ROOT/skills"
mkdir -p "$WORKSPACE_ROOT/user-data"
mkdir -p "$WORKSPACE_ROOT/scripts"
mkdir -p "$WORKSPACE_ROOT/shared"/{inbox,outbox,status,working}
mkdir -p "$WORKSPACE_ROOT/reports"
mkdir -p "$WORKSPACE_ROOT/temp"
mkdir -p "$WORKSPACE_ROOT/.learnings"
mkdir -p "$WORKSPACE_ROOT/wiki"/{concepts,entities,how-to}

# 创建学习记录文件
touch "$WORKSPACE_ROOT/.learnings/ERRORS.md"
touch "$WORKSPACE_ROOT/.learnings/SUCCESSES.md"
touch "$WORKSPACE_ROOT/.learnings/LEARNINGS.md"

echo "✅ Directory structure created!"

# 复制模板文件
if [ -d "$TEMPLATES_DIR" ]; then
    echo ""
    echo "📄 Copying templates..."
    cp "$TEMPLATES_DIR/SOUL-template.md" "$WORKSPACE_ROOT/SOUL.md"
    cp "$TEMPLATES_DIR/AGENTS-template.md" "$WORKSPACE_ROOT/AGENTS.md"
    cp "$TEMPLATES_DIR/MEMORY-template.md" "$WORKSPACE_ROOT/MEMORY.md"
    cp "$TEMPLATES_DIR/USER-template.md" "$WORKSPACE_ROOT/USER.md"
    cp "$TEMPLATES_DIR/HEARTBEAT-template.md" "$WORKSPACE_ROOT/HEARTBEAT.md"
    echo "✅ Templates copied!"
else
    echo "⚠️  Templates directory not found: $TEMPLATES_DIR"
    echo "   You can manually copy templates later."
fi

# 复制 WORKSPACE-TEMPLATE.md（参考文档）
if [ -f "$TEMPLATES_DIR/WORKSPACE-TEMPLATE.md" ]; then
    cp "$TEMPLATES_DIR/WORKSPACE-TEMPLATE.md" "$WORKSPACE_ROOT/WORKSPACE-TEMPLATE.md"
    echo "✅ WORKSPACE-TEMPLATE.md copied (reference document)"
fi

echo ""
echo "Next steps:"
echo "1. Edit SOUL.md - Define your identity"
echo "2. Edit USER.md - Fill in user information"
echo "3. Edit MEMORY.md - Create memory index"
echo "4. Test startup: Read SOUL.md → USER.md → MEMORY.md"
echo ""
echo "Examples:"
echo "  - Mindset Coach: $TEMPLATES_DIR/../examples/mindset-coach/"
echo "  - Tech Assistant: $TEMPLATES_DIR/../examples/tech-assistant/"
echo "  - Personal Assistant: $TEMPLATES_DIR/../examples/personal-assistant/"
