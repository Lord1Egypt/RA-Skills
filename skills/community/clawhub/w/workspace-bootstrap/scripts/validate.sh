#!/bin/bash
# workspace-validate - 验证 workspace 结构
# 版本: v0.1.0

WORKSPACE_ROOT=${1:-"."}

echo "🔍 Validating workspace structure..."

# 检查核心文件
check_file() {
    if [ -f "$WORKSPACE_ROOT/$1" ]; then
        echo "✅ $1 exists"
    else
        echo "❌ $1 missing"
    fi
}

# 检查目录
check_dir() {
    if [ -d "$WORKSPACE_ROOT/$1" ]; then
        echo "✅ $1/ exists"
    else
        echo "❌ $1/ missing"
    fi
}

echo ""
echo "Core files:"
check_file "SOUL.md"
check_file "AGENTS.md"
check_file "MEMORY.md"
check_file "USER.md"
check_file "HEARTBEAT.md"

echo ""
echo "Directories:"
check_dir "agents"
check_dir "memory"
check_dir "skills"
check_dir "user-data"
check_dir "scripts"
check_dir "shared"
check_dir "reports"
check_dir "temp"
check_dir ".learnings"

echo ""
echo "Validation complete."
