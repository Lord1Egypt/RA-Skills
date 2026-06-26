#!/usr/bin/env bash
# 命名空间管理模块

source "$(dirname "${BASH_SOURCE[0]}")/config.sh"

# 创建命名空间
namespace_create() {
    local name="$1"
    
    if [[ -z "$name" ]]; then
        echo "Error: Namespace name required" >&2
        return 1
    fi
    
    local ns_dir="$NAMESPACE_DIR/$name"
    
    if [[ -d "$ns_dir" ]]; then
        echo "Namespace '$name' already exists"
        return 0
    fi
    
    mkdir -p "$ns_dir/hot" "$ns_dir/warm" "$ns_dir/cold"
    
    # 创建命名空间配置
    cat > "$ns_dir/config.json" <<EOF
{
  "name": "$name",
  "created_at": "$(now())",
  "hot_retention_sessions": $HOT_RETENTION,
  "warm_retention_sessions": $WARM_RETENTION
}
EOF
    
    echo "Created namespace: $name"
}

# 列出命名空间
namespace_list() {
    if [[ ! -d "$NAMESPACE_DIR" ]]; then
        echo "No namespaces found"
        return 0
    fi
    
    echo "=== Namespaces ==="
    for dir in "$NAMESPACE_DIR"/*/; do
        if [[ -d "$dir" ]]; then
            local name=$(basename "$dir")
            local config="$dir/config.json"
            local created=""
            if [[ -f "$config" ]]; then
                created=$(jq -r '.created_at' "$config" 2>/dev/null)
            fi
            echo "- $name (created: ${created:-unknown})"
        fi
    done
    
    echo ""
    echo "Default namespace: $DEFAULT_NAMESPACE"
}

# 删除命名空间
namespace_delete() {
    local name="$1"
    
    if [[ "$name" == "$DEFAULT_NAMESPACE" ]]; then
        echo "Error: Cannot delete default namespace" >&2
        return 1
    fi
    
    local ns_dir="$NAMESPACE_DIR/$name"
    
    if [[ ! -d "$ns_dir" ]]; then
        echo "Namespace '$name' does not exist"
        return 1
    fi
    
    read -p "Delete namespace '$name' and all its data? (y/N) " confirm
    if [[ "$confirm" != "y" ]]; then
        echo "Cancelled"
        return 0
    fi
    
    rm -rf "$ns_dir"
    echo "Deleted namespace: $name"
}

# 设置默认命名空间
namespace_use() {
    local name="$1"
    
    if [[ ! -d "$NAMESPACE_DIR/$name" ]]; then
        echo "Error: Namespace '$name' does not exist" >&2
        return 1
    fi
    
    DEFAULT_NAMESPACE="$name"
    echo "Default namespace set to: $name"
}
