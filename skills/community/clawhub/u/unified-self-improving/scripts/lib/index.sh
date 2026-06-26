#!/usr/bin/env bash
# 索引管理模块

source "$(dirname "${BASH_SOURCE[0]}")/config.sh"

# 初始化索引文件
index_init() {
    mkdir -p "$(dirname "$INDEX_FILE")"
    touch "$INDEX_FILE"
    echo "Index initialized at $INDEX_FILE"
}

# 重建索引（扫描所有层级）
index_rebuild() {
    echo "Rebuilding index..."
    
    local temp=$(mktemp)
    echo "[]" > "$temp"
    
    # 扫描 HOT
    for file in "$HOT_DIR"/*.jsonl; do
        if [[ -f "$file" ]]; then
            local id=$(basename "$file" .jsonl)
            jq --arg id "$id" --arg level "hot" --arg ns "$DEFAULT_NAMESPACE" \
                '. + [{"id": $id, "level": $level, "namespace": $ns}]' "$temp" > "${temp}.tmp"
            mv "${temp}.tmp" "$temp"
        fi
    done
    
    # 扫描 WARM
    for ns_dir in "$WARM_DIR"/*/; do
        if [[ -d "$ns_dir" ]]; then
            local ns=$(basename "$ns_dir")
            for file in "$ns_dir"/*.jsonl; do
                if [[ -f "$file" ]]; then
                    local id=$(basename "$file" .jsonl)
                    jq --arg id "$id" --arg level "warm" --arg ns "$ns" \
                        '. + [{"id": $id, "level": $level, "namespace": $ns}]' "$temp" > "${temp}.tmp"
                    mv "${temp}.tmp" "$temp"
                fi
            done
        fi
    done
    
    # 扫描 COLD
    for ns_dir in "$COLD_DIR"/*/; do
        if [[ -d "$ns_dir" ]]; then
            local ns=$(basename "$ns_dir")
            for file in "$ns_dir"/*.jsonl; do
                if [[ -f "$file" ]]; then
                    local id=$(basename "$file" .jsonl)
                    jq --arg id "$id" --arg level "cold" --arg ns "$ns" \
                        '. + [{"id": $id, "level": $level, "namespace": $ns}]' "$temp" > "${temp}.tmp"
                    mv "${temp}.tmp" "$temp"
                fi
            done
        fi
    done
    
    mv "$temp" "$INDEX_FILE"
    local count=$(jq 'length' "$INDEX_FILE")
    echo "Index rebuilt: $count items"
}

# 添加到索引
index_add() {
    local id="$1"
    local level="$2"
    local namespace="${3:-$DEFAULT_NAMESPACE}"
    
    if [[ ! -f "$INDEX_FILE" ]]; then
        index_init
    fi
    
    # 检查是否已存在
    if jq --arg id "$id" '.[].id' "$INDEX_FILE" 2>/dev/null | grep -q "^$id$"; then
        echo "Warning: ID '$id' already in index, updating..."
        index_remove "$id"
    fi
    
    jq --arg id "$id" --arg level "$level" --arg ns "$namespace" --arg now "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
        '. + [{"id": $id, "level": $level, "namespace": $ns, "updated_at": $now}]' \
        "$INDEX_FILE" > "${INDEX_FILE}.tmp"
    mv "${INDEX_FILE}.tmp" "$INDEX_FILE"
}

# 从索引移除
index_remove() {
    local id="$1"
    
    if [[ -f "$INDEX_FILE" ]]; then
        jq --arg id "$id" 'map(select(.id != $id))' "$INDEX_FILE" > "${INDEX_FILE}.tmp"
        mv "${INDEX_FILE}.tmp" "$INDEX_FILE"
    fi
}

# 搜索索引
index_search() {
    local pattern="$1"
    
    if [[ ! -f "$INDEX_FILE" ]]; then
        echo "Index not found. Run 'index rebuild' first."
        return 1
    fi
    
    jq --arg pattern "$pattern" \
        'map(select(.id | contains($pattern) or .namespace | contains($pattern)))' \
        "$INDEX_FILE"
}
