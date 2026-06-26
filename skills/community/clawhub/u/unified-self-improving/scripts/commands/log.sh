#!/usr/bin/env bash
# 记录学习项（correction/error/pattern）

source "$(dirname "${BASH_SOURCE[0]}")/../lib/config.sh"
source "$(dirname "${BASH_SOURCE[0]}")/../lib/storage.sh"
source "$(dirname "${BASH_SOURCE[0]}")/../lib/index.sh"

show_help() {
    cat <<EOF
Usage: unified-self-improving log [OPTIONS]

Record learning items (correction, error, pattern)

Options:
  -t, --type TYPE         Type: correction, error, pattern (required)
  -c, --content TEXT      Content to record (required)
  -n, --namespace NS      Namespace (default: $DEFAULT_NAMESPACE)
  -p, --priority PRIO     Priority: low, medium, high (default: medium)
  -h, --help              Show this help

Examples:
  unified-self-improving log -t correction -c "用户说我不应该..."
  unified-self-improving log -t error -c "命令执行失败" -p high
EOF
}

main() {
    local type="" content="" namespace="$DEFAULT_NAMESPACE" priority="medium"
    
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -t|--type)
                type="$2"
                shift 2
                ;;
            -c|--content)
                content="$2"
                shift 2
                ;;
            -n|--namespace)
                namespace="$2"
                shift 2
                ;;
            -p|--priority)
                priority="$2"
                shift 2
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                echo "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # 验证参数
    if [[ -z "$type" ]]; then
        echo "Error: --type required" >&2
        exit 1
    fi
    
    if [[ -z "$content" ]]; then
        echo "Error: --content required" >&2
        exit 1
    fi
    
    if [[ ! "$type" =~ ^(correction|error|pattern)$ ]]; then
        echo "Error: type must be correction, error, or pattern" >&2
        exit 1
    fi
    
    if [[ ! "$priority" =~ ^(low|medium|high)$ ]]; then
        echo "Error: priority must be low, medium, or high" >&2
        exit 1
    fi
    
    # 初始化存储
    init_storage
    
    # 生成记录
    local id=$(generate_id)
    local timestamp=$(now)
    
    # 创建 JSONL 记录
    local record=$(cat <<EOF
{"id": "$id", "namespace": "$namespace", "type": "$type", "content": "$content", "priority": "$priority", "status": "active", "access_count": 0, "created_at": "$timestamp", "updated_at": "$timestamp"}
EOF
)
    
    # 保存到 HOT 层
    local path="$HOT_DIR/${id}.jsonl"
    echo "$record" > "$path"
    
    # 同时记录到对应的 Markdown 文件
    case "$type" in
        correction)
            echo "- **$id**: $content (priority: $priority) - $timestamp" >> "$HOT_DIR/corrections.md"
            ;;
        error)
            echo "- **$id**: $content (priority: $priority) - $timestamp" >> "$HOT_DIR/errors.md"
            ;;
        pattern)
            echo "- **$id**: $content (priority: $priority) - $timestamp" >> "$HOT_DIR/patterns.md"
            ;;
    esac
    
    # 添加到索引
    index_add "$id" "hot" "$namespace"
    
    echo "Recorded: $id ($type)"
    echo "$record" | jq '.'
}

main "$@"
