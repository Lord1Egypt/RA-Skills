#!/usr/bin/env bash
# 存储层级操作模块

source "$(dirname "${BASH_SOURCE[0]}")/config.sh"

# 获取学习项的文件路径
get_learn_path() {
    local id="$1"
    local level="${2:-hot}"
    local namespace="${3:-$DEFAULT_NAMESPACE}"
    
    case "$level" in
        hot)    echo "$HOT_DIR/${id}.jsonl" ;;
        warm)   echo "$WARM_DIR/${namespace}/${id}.jsonl" ;;
        cold)   echo "$COLD_DIR/${namespace}/${id}.jsonl" ;;
        *)      echo "$HOT_DIR/${id}.jsonl" ;;
    esac
}

# 查找学习项（所有层级）
find_learn() {
    local id="$1"
    local namespace="${2:-$DEFAULT_NAMESPACE}"
    
    # 先在 HOT 查找
    if [[ -f "$HOT_DIR/${id}.jsonl" ]]; then
        echo "hot"
        cat "$HOT_DIR/${id}.jsonl"
        return 0
    fi
    
    # WARM 查找
    if [[ -f "$WARM_DIR/${namespace}/${id}.jsonl" ]]; then
        echo "warm"
        cat "$WARM_DIR/${namespace}/${id}.jsonl"
        return 0
    fi
    
    # COLD 查找
    if [[ -f "$COLD_DIR/${namespace}/${id}.jsonl" ]]; then
        echo "cold"
        cat "$COLD_DIR/${namespace}/${id}.jsonl"
        return 0
    fi
    
    return 1
}

# 移动学习项到指定层级
move_learn() {
    local id="$1"
    local to_level="$2"
    local namespace="${3:-$DEFAULT_NAMESPACE}"
    
    local current_level
    local data
    current_level=$(find_learn "$id" "$namespace" | head -1)
    data=$(find_learn "$id" "$namespace")
    
    if [[ -z "$current_level" ]]; then
        echo "Error: Learning item '$id' not found" >&2
        return 1
    fi
    
    if [[ "$current_level" == "$to_level" ]]; then
        echo "Already at level: $to_level"
        return 0
    fi
    
    # 移动文件
    local src_path=$(get_learn_path "$id" "$current_level" "$namespace")
    local dst_path=$(get_learn_path "$id" "$to_level" "$namespace")
    
    # 确保目标目录存在
    mkdir -p "$(dirname "$dst_path")"
    
    mv "$src_path" "$dst_path"
    
    # 更新索引
    update_index "$id" "$to_level" "$namespace"
    
    echo "Moved $id from $current_level to $to_level"
}

# 读取学习项
read_learn() {
    local id="$1"
    local namespace="${2:-$DEFAULT_NAMESPACE}"
    
    find_learn "$id" "$namespace" | tail -1 | jq -r '.' 2>/dev/null
}

# 更新索引中的层级
update_index() {
    local id="$1"
    local level="$2"
    local namespace="${3:-$DEFAULT_NAMESPACE}"
    
    if [[ -f "$INDEX_FILE" ]]; then
        # 更新现有记录
        local temp=$(mktemp)
        jq --arg id "$id" --arg level "$level" 'map(if .id == $id then .level = $level else . end)' "$INDEX_FILE" > "$temp"
        mv "$temp" "$INDEX_FILE"
    fi
}

# 列出所有学习项
list_learns() {
    local level="${1:-all}"
    local namespace="${2:-$DEFAULT_NAMESPACE}"
    
    case "$level" in
        hot)
            ls -1 "$HOT_DIR"/*.jsonl 2>/dev/null | xargs -I {} basename {} .jsonl
            ;;
        warm)
            ls -1 "$WARM_DIR/${namespace}"/*.jsonl 2>/dev/null | xargs -I {} basename {} .jsonl
            ;;
        cold)
            ls -1 "$COLD_DIR/${namespace}"/*.jsonl 2>/dev/null | xargs -I {} basename {} .jsonl
            ;;
        all)
            echo "=== HOT ==="
            list_learns "hot" "$namespace"
            echo "=== WARM ==="
            list_learns "warm" "$namespace"
            echo "=== COLD ==="
            list_learns "cold" "$namespace"
            ;;
    esac
}

# 获取访问计数
get_access_count() {
    local id="$1"
    local namespace="${2:-$DEFAULT_NAMESPACE}"
    
    local data=$(find_learn "$id" "$namespace" | tail -1)
    echo "$data" | jq -r '.access_count // 0'
}

# 增加访问计数
inc_access_count() {
    local id="$1"
    local namespace="${2:-$DEFAULT_NAMESPACE}"
    
    local level=$(find_learn "$id" "$namespace" | head -1)
    local data=$(find_learn "$id" "$namespace" | tail -1)
    local path=$(get_learn_path "$id" "$level" "$namespace")
    
    local count=$(echo "$data" | jq -r '.access_count // 0')
    local new_count=$((count + 1))
    
    echo "$data" | jq --arg now "$(now)" --argjson count "$new_count" \
        '.access_count = $count | .updated_at = $now' > "$path"
    
    echo "$new_count"
}
