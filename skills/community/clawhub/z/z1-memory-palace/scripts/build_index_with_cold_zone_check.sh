#!/bin/bash
# Watchdog 索引构建脚本（集成冷区盲化检查）
# 版本：v1.0
# 日期：2026-04-09

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "============================================================"
echo "Watchdog 索引构建 - 集成冷区盲化检查"
echo "============================================================"

# 1. 运行冷区盲化检查
echo -e "\n[1] 运行冷区盲化检查..."
python3 "$SCRIPT_DIR/cold_zone_blinding_patch.py"

# 2. 构建向量索引
echo -e "\n[2] 构建向量索引..."
python3 "$SCRIPT_DIR/build_index_bge.py"

# 3. 构建图邻居
echo -e "\n[3] 构建图邻居..."
python3 "$SCRIPT_DIR/graph_router.py"

# 4. 验证冷区排除
echo -e "\n[4] 验证冷区排除效果..."
MANIFEST="$ROOT_DIR/memory/palace/watchdog/index/watchdog_manifest_v1_2026-04-08.jsonl"
VECTORS="$ROOT_DIR/memory/palace/watchdog/index/watchdog_vectors_v1_2026-04-08.jsonl"

echo "检查 manifest 文件..."
if [ -f "$MANIFEST" ]; then
    COUNT=$(grep -c "archive_basement" "$MANIFEST" 2>/dev/null || echo "0")
    if [ "$COUNT" -eq 0 ]; then
        echo "  ✓ Manifest 文件中未发现冷区路径"
    else
        echo "  ✗ Manifest 文件中发现 $COUNT 个冷区路径"
        exit 1
    fi
fi

echo "检查向量索引..."
if [ -f "$VECTORS" ]; then
    COUNT=$(grep -c "archive_basement" "$VECTORS" 2>/dev/null || echo "0")
    if [ "$COUNT" -eq 0 ]; then
        echo "  ✓ 向量索引中未发现冷区路径"
    else
        echo "  ✗ 向量索引中发现 $COUNT 个冷区路径"
        exit 1
    fi
fi

# 5. 测试查询
echo -e "\n[5] 测试查询排除效果..."
TEST_QUERY="系统架构"
echo "测试查询: \"$TEST_QUERY\""
python3 "$SCRIPT_DIR/query_bge.py" "$TEST_QUERY" 2>/dev/null | {
    COLD_COUNT=0
    TOTAL=0
    while read -r line; do
        if echo "$line" | grep -q "archive_basement"; then
            COLD_COUNT=$((COLD_COUNT + 1))
        fi
        TOTAL=$((TOTAL + 1))
    done
    
    if [ "$COLD_COUNT" -eq 0 ]; then
        echo "  ✓ 查询结果中未发现冷区路径"
    else
        echo "  ✗ 查询结果中发现 $COLD_COUNT 个冷区路径"
        exit 1
    fi
}

echo -e "\n============================================================"
echo "[BUILD_COMPLETE] Watchdog 索引构建完成，冷区盲化检查通过"
echo "============================================================"
echo ""
echo "索引文件位置："
echo "  - 向量索引: memory/palace/watchdog/index/watchdog_vectors_v1_2026-04-08.jsonl"
echo "  - 图邻居: memory/palace/watchdog/index/graph_neighbors_v1_2026-04-08.json"
echo ""
echo "下次构建可直接运行：./scripts/watchdog/build_index_with_cold_zone_check.sh"