#!/bin/bash
# Viking Memory System - sv_promote
# 动态回流机制 - 当检测到任务与 Cold/Archive 记忆语义相似时，即时晋升至 Hot 层
#
# Phase 1 实现: 使用 LLM 判断语义相关性，替代 embedding（简化方案）
#
# 用法:
#   sv_promote.sh                      # 扫描并晋升（默认）
#   sv_promote.sh --dry-run            # 预览模式
#   sv_promote.sh --context "任务描述"  # 指定上下文
#   sv_promote.sh --threshold 0.7      # 相似度阈值（默认0.7）
#   sv_promote.sh --layer cold,archive # 指定扫描层级
#
# 整合到 sv_autoload:
#   sv_autoload.sh --promote          # 加载记忆后自动晋升检查

set +e

VIKING_HOME="${VIKING_HOME:-$HOME/.openclaw/viking}"
WORKSPACE="${SV_WORKSPACE:-$HOME/.openclaw/viking-maojingli}"

# ============ 默认配置 ============
DRY_RUN=false
CONTEXT=""
THRESHOLD=0.7
LAYERS="cold,archive"
INTEGRATED=false
MAX_MEMORIES=50  # 每次最多处理50条，防止API过载

# ============ 解析参数 ============
while [ $# -gt 0 ]; do
    case "$1" in
        --dry-run) DRY_RUN=true; shift ;;
        --context) CONTEXT="$2"; shift 2 ;;
        --threshold) THRESHOLD="$2"; shift 2 ;;
        --layer) LAYERS="$2"; shift 2 ;;
        --promote) INTEGRATED=true; shift ;;
        --*) echo "未知选项: $1"; exit 1 ;;
        *) [ -z "$CONTEXT" ] && CONTEXT="$1"; shift ;;
    esac
done

# ============ 加载 LLM 接口 ============
[ -f "$VIKING_HOME/scripts/llm_interface.sh" ] && source "$VIKING_HOME/scripts/llm_interface.sh"

# ============ 颜色输出 ============
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'

echo -e "${BLUE}=== Viking 动态回流机制 ===${NC}"
echo "工作空间: $WORKSPACE"
[ "$DRY_RUN" = true ] && echo -e "${YELLOW}模式: 预览（不实际晋升）${NC}"
echo "扫描层级: $LAYERS"
echo "相似度阈值: $THRESHOLD"
echo ""

# ============ 安全解析 frontmatter ============
parse_fm() {
    awk -v key="$2" -- '
        BEGIN { in_fm=0 }
        /^---$/ { in_fm=1; next }
        /^---$/ && in_fm { exit }
        in_fm && $0 ~ "^" key ": *" {
            sub("^" key ": *", "")
            gsub(/^[ \t]+|[ \t]+$/, "")
            print; exit
        }
    ' "$1" 2>/dev/null
}

# ============ 获取晋升目标目录 ============
get_promote_dir() {
    local current_layer="$1"
    local file="$2"
    # 文件路径: .../memories/{layer}/filename.md
    # 需要得到: .../memories/hot/
    local memories_dir
    memories_dir=$(dirname "$(dirname -- "$file")")
    echo "$memories_dir/hot"
}

# ============ 检查 LLM 函数 ============
check_llm_available() {
    if declare -f llm_judge_relevance > /dev/null 2>&1; then
        return 0
    fi
    # 如果没有自定义判断函数，尝试使用 llm_recall 作为后备
    if declare -f llm_recall > /dev/null 2>&1; then
        return 0
    fi
    echo -e "${RED}❌ LLM 接口不可用，无法进行语义相似度判断${NC}"
    return 1
}

# ============ 语义相似度判断（使用 LLM）============
# 核心逻辑：让 LLM 判断当前上下文与历史记忆是否语义相关
llm_judge_relevance() {
    local memory_content="$1"
    local context="$2"
    local memory_name="$3"

    # 准备 prompt（使用 python 处理 JSON 转义）
    local prompt=$(python3 -c "
import sys, json, textwrap

context = '''${context}'''[:1000]
memory = '''${memory_content}'''[:4000]

prompt = f'''你是一个记忆相关性判断专家。
当前任务: {context}

历史记忆:
{memory}

请判断这条历史记忆与当前任务是否语义相关（能够帮助理解、参考、或影响当前任务的执行）。
回复格式：只输出一个0-1之间的小数，表示相关度。
0.0=完全不相关，0.5=部分相关，1.0=高度相关。
只输出数字，不要任何解释。'''

# 直接输出转义后的prompt（不用json.dumps因为会加引号）
print(prompt)
" 2>/dev/null)

    # 默认使用 NVIDIA Qwen
    local api_url="https://integrate.api.nvidia.com/v1/chat/completions"
    local api_key="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"
    local model="qwen/qwen3.5-122b-a10b"

    # 构建 JSON payload
    local json_payload=$(python3 -c "
import json
data = {
    'model': '$model',
    'max_tokens': 10,
    'temperature': 0.1,
    'messages': [{'role': 'user', 'content': '''$prompt'''}]
}
print(json.dumps(data, ensure_ascii=False))
" 2>/dev/null)

    # 调用 API
    local response
    response=$(curl -s --max-time 20 "$api_url" \
        -H "Authorization: Bearer $api_key" \
        -H "Content-Type: application/json" \
        -d "$json_payload" 2>/dev/null)

    # 解析响应
    echo "$response" | python3 -c "
import sys, json, re
try:
    d = json.load(sys.stdin)
    content = d.get('choices', [{}])[0].get('message', {}).get('content', '0')
    # 提取数字
    match = re.search(r'0?\.\d+|1\.0', content)
    if match:
        print(float(match.group()))
    else:
        print('0.0')
except:
    print('0.0')
" 2>/dev/null || echo "0.0"
}

# ============ 主逻辑：扫描并晋升 ============
scan_and_promote() {
    local search_context="$1"
    local promote_count=0
    local scan_count=0
    local skip_count=0

    # 构建搜索目录列表
    local search_dirs=""
    IFS=',' read -ra LAYER_ARR <<< "$LAYERS"
    for layer in "${LAYER_ARR[@]}"; do
        case "$layer" in
            cold)  search_dirs="$search_dirs $WORKSPACE/agent/memories/cold" ;;
            archive) search_dirs="$search_dirs $WORKSPACE/agent/memories/archive" ;;
            warm)  search_dirs="$search_dirs $WORKSPACE/agent/memories/warm" ;;
            hot)   search_dirs="$search_dirs $WORKSPACE/agent/memories/hot" ;;
        esac
    done

    echo -e "${BLUE}扫描目录:${NC} $search_dirs"
    echo ""

    # 收集所有待扫描文件
    local all_files=""
    for dir in $search_dirs; do
        [ -d "$dir" ] && all_files="$all_files$(find "$dir" -name "*.md" -type f 2>/dev/null)"$'\n'
    done

    [ -z "$(echo "$all_files" | tr -d '\n')" ] && {
        echo -e "${YELLOW}⚠ 没有找到待扫描的记忆文件${NC}"
        return 0
    }

    # 转换为数组
    local files_array
    mapfile -t files_array <<< "$all_files"

    echo -e "${BLUE}找到 ${#files_array[@]} 条记忆，开始语义分析...${NC}"
    echo ""

    for file in "${files_array[@]}"; do
        [ -z "$file" ] && continue
        [ $scan_count -ge $MAX_MEMORIES ] && {
            echo -e "${YELLOW}⚠ 达到最大处理数量 ($MAX_MEMORIES)，跳过剩余文件${NC}"
            break
        }

        scan_count=$((scan_count + 1))

        # 读取内容（限制长度）
        local content=$(cat "$file" 2>/dev/null || continue)
        [ -z "$content" ] && continue

        # 提取 frontmatter 信息
        local memory_layer=$(parse_fm "$file" "current_layer")
        local memory_importance=$(parse_fm "$file" "importance")
        local memory_title=$(basename -- "$file" .md)

        # 重要记忆不自动晋升（保持原层级）
        if [ "$memory_importance" = "important" ] || [ "$memory_importance" = "high" ]; then
            skip_count=$((skip_count + 1))
            continue
        fi

        # 计算语义相似度
        echo -ne "${GRAY}  检查 [$scan_count]: $memory_title ... ${NC}"

        local similarity
        similarity=$(llm_judge_relevance "$content" "$search_context" "$memory_title")

        # 判断是否晋升
        local threshold_float
        threshold_float=$(echo "$THRESHOLD" | python3 -c "print(float(open(0).read().strip()))")

        is_promote=$(python3 -c "
similarity = $similarity
threshold = $threshold_float
print('yes' if similarity >= threshold else 'no')
" 2>/dev/null || echo "no")

        if [ "$is_promote" = "yes" ]; then
            echo -e "${GREEN}  ✅ 相关度: $similarity → 晋升!${NC}"

            if [ "$DRY_RUN" = true ]; then
                echo -e "     ${YELLOW}[预览] $memory_title: $memory_layer → hot${NC}"
            else
                # 执行晋升
                local current_dir
                current_dir=$(dirname -- "$file")
                local target_dir
                target_dir=$(get_promote_dir "$memory_layer" "$file")
                local target_path="$target_dir/$(basename -- "$file")"

                mkdir -p "$target_dir"

                # 检查目标是否已存在
                if [ -f "$target_path" ]; then
                    echo -e "     ${RED}⚠ 目标文件已存在，跳过: $(basename -- "$file")${NC}"
                    continue
                fi

                # 更新 frontmatter 并移动
                local tmp_file="${file}.promote.tmp"
                sed "s/^current_layer:.*/current_layer: L0/" "$file" | \
                sed "s/^target_layer:.*/target_layer: hot/" > "$tmp_file" && \
                mv -f "$tmp_file" "$target_path" && \
                rm -f "$file" && \
                echo -e "     ${GREEN}✓ 已晋升: $memory_title → hot${NC}" || {
                    rm -f "$tmp_file"
                    echo -e "     ${RED}✗ 晋升失败: $memory_title${NC}"
                }
            fi
            promote_count=$((promote_count + 1))
        else
            echo -e "${GRAY}  ⏭ 相关度: $similarity < $THRESHOLD${NC}"
        fi
    done

    echo ""
    echo -e "${BLUE}=== 扫描完成 ===${NC}"
    echo "扫描: $scan_count | 晋升: $promote_count | 跳过(重要): $skip_count"

    [ "$DRY_RUN" = true ] && echo -e "${YELLOW}[预览模式] 如需实际执行，去掉 --dry-run${NC}"
}

# ============ 获取当前上下文 ============
get_current_context() {
    # 优先使用提供的 context
    [ -n "$CONTEXT" ] && { echo "$CONTEXT"; return; }

    # 从环境变量或最近记忆获取
    if [ -n "$CURRENT_TASK" ]; then
        echo "$CURRENT_TASK"
        return
    fi

    # 默认：读取今日工作文件作为上下文
    local today_file="$WORKSPACE/agent/memories/daily/$(date +%Y-%m-%d).md"
    if [ -f "$today_file" ]; then
        head -c 500 "$today_file"
    else
        # fallback: 读取最近修改的 hot 层记忆
        local recent_hot
        recent_hot=$(find "$WORKSPACE/agent/memories/hot" -name "*.md" -type f -mtime -1 2>/dev/null | head -1)
        [ -n "$recent_hot" ] && head -c 500 "$recent_hot" || echo "日常任务处理"
    fi
}

# ============ 启动 ============
# 检查 LLM 可用性
check_llm_available || exit 1

# 获取上下文
CONTEXT=$(get_current_context)
echo -e "${BLUE}当前上下文:${NC} $(echo "$CONTEXT" | head -c 100)..."
echo ""

# 执行扫描晋升
scan_and_promote "$CONTEXT"

exit 0
