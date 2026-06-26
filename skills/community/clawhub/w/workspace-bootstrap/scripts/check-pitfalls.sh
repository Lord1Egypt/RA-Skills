#!/bin/bash
# check-pitfalls - 检查已知的坑
# 版本: v0.3.0

WORKSPACE_ROOT=${1:-"."}

echo "🔍 Checking known pitfalls..."
echo ""

PITFALL_COUNT=0

# 1. MEMORY.md 容量检查
check_memory_capacity() {
    if [ -f "$WORKSPACE_ROOT/MEMORY.md" ]; then
        LINES=$(wc -l < "$WORKSPACE_ROOT/MEMORY.md")
        if [ $LINES -gt 100 ]; then
            echo "❌ Pitfall 1: MEMORY.md 容量爆炸 ($LINES 行 > 100 行)"
            echo "   方案：只放链接，详细内容放 memory/YYYY-MM-DD.md"
            PITFALL_COUNT=$((PITFALL_COUNT + 1))
        else
            echo "✅ Pitfall 1: MEMORY.md 容量正常 ($LINES 行)"
        fi
    else
        echo "⚠️  Pitfall 1: MEMORY.md 不存在"
    fi
}

# 2. 核心文件检查
check_core_files() {
    local MISSING=0
    for file in SOUL.md AGENTS.md MEMORY.md USER.md HEARTBEAT.md; do
        if [ ! -f "$WORKSPACE_ROOT/$file" ]; then
            echo "❌ Pitfall 2: 缺少核心文件 $file"
            MISSING=$((MISSING + 1))
        fi
    done
    
    if [ $MISSING -eq 0 ]; then
        echo "✅ Pitfall 2: 核心文件完整"
    else
        PITFALL_COUNT=$((PITFALL_COUNT + MISSING))
    fi
}

# 3. 目录结构检查
check_directories() {
    local MISSING=0
    for dir in agents memory skills user-data scripts shared reports temp .learnings; do
        if [ ! -d "$WORKSPACE_ROOT/$dir" ]; then
            echo "❌ Pitfall 3: 缺少目录 $dir/"
            MISSING=$((MISSING + 1))
        fi
    done
    
    if [ $MISSING -eq 0 ]; then
        echo "✅ Pitfall 3: 目录结构完整"
    else
        PITFALL_COUNT=$((PITFALL_COUNT + MISSING))
    fi
}

# 4. .learnings 文件检查
check_learning_files() {
    local MISSING=0
    for file in .learnings/ERRORS.md .learnings/SUCCESSES.md .learnings/LEARNINGS.md; do
        if [ ! -f "$WORKSPACE_ROOT/$file" ]; then
            echo "❌ Pitfall 4: 缺少学习文件 $file"
            MISSING=$((MISSING + 1))
        fi
    done
    
    if [ $MISSING -eq 0 ]; then
        echo "✅ Pitfall 4: 学习文件完整"
    else
        PITFALL_COUNT=$((PITFALL_COUNT + MISSING))
    fi
}

# 5. shared 目录检查
check_shared_dirs() {
    local MISSING=0
    for dir in shared/inbox shared/outbox shared/status shared/working; do
        if [ ! -d "$WORKSPACE_ROOT/$dir" ]; then
            echo "❌ Pitfall 5: 缺少共享目录 $dir/"
            MISSING=$((MISSING + 1))
        fi
    done
    
    if [ $MISSING -eq 0 ]; then
        echo "✅ Pitfall 5: 共享目录完整"
    else
        PITFALL_COUNT=$((PITFALL_COUNT + MISSING))
    fi
}

# 执行检查
check_memory_capacity
check_core_files
check_directories
check_learning_files
check_shared_dirs

# 总结
echo ""
echo "═══════════════════════════════════════"
if [ $PITFALL_COUNT -eq 0 ]; then
    echo "✅ 所有检查通过！"
else
    echo "⚠️  发现 $PITFALL_COUNT 个问题"
    echo ""
    echo "建议："
    echo "1. 运行 bash scripts/bootstrap.sh . 修复缺失的目录和文件"
    echo "2. 查看 WORKSPACE-TEMPLATE.md 了解最佳实践"
fi
echo "═══════════════════════════════════════"
