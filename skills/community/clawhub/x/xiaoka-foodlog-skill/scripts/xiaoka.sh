#!/usr/bin/env bash
set -euo pipefail

# 小卡健康 OpenClaw Skill 脚本
# 用法: xiaoka.sh <command> [args...]
#   xiaoka.sh pair                    - 获取配对码
#   xiaoka.sh bind <api_key>          - 保存 API Key
#   xiaoka.sh log <text> [meal_type]  - 记录饮食
#   xiaoka.sh today                   - 查看今日记录

API_BASE="${XIAOKA_API_BASE:-${XIAOKA_API:-https://cal-cn.ishuohua.cn}}"
API_KEY="${XIAOKA_API_KEY:-}"
CONFIG_FILE="${HOME}/.openclaw/workspace/skills/xiaoka-food-log/.credentials"

# 加载已保存的配置
load_config() {
    if [[ -f "$CONFIG_FILE" ]] && [[ -z "$API_KEY" ]]; then
        API_KEY=$(cat "$CONFIG_FILE")
    fi
}

# 保存 API Key
save_config() {
    echo "$1" > "$CONFIG_FILE"
    chmod 600 "$CONFIG_FILE"
}

# 检查是否已绑定
check_bindind() {
    load_config
    if [[ -z "$API_KEY" ]]; then
        echo "尚未绑定小卡健康账号。"
        echo ""
        echo "正在获取配对码..."
        pair_result=$(curl -s "${API_BASE}/openclaw/api/pair-code")
        pair_code=$(echo "$pair_result" | jq -r '.data.pair_code // empty')
        if [[ -z "$pair_code" ]]; then
            echo "获取配对码失败，请检查网络连接。"
            exit 1
        fi
        echo ""
        echo "请打开小卡健康 App，在 AI 搭子中发送："
        echo ""
        echo "    绑定openclaw ${pair_code}"
        echo ""
        echo "然后将 AI 搭子的回复粘贴到这里。"
        exit 0
    fi
}

# 从用户粘贴的文本中提取 API Key
extract_api_key() {
    local text="$1"
    local key
    key=$(echo "$text" | grep -oE 'oc_[a-f0-9]{48}' | head -1)
    echo "$key"
}

# 关键词 → meal_type 映射
detect_meal_type() {
    local text="$1"
    case "$text" in
        记录早餐*) echo "breakfast" ;;
        记录午餐*) echo "lunch" ;;
        记录晚餐*) echo "dinner" ;;
        记录加餐*) echo "snack" ;;
        *) echo "" ;;
    esac
}

# 去掉关键词前缀，提取食物描述
extract_food_text() {
    local text="$1"
    # 去掉"记录饮食"、"记录早餐"等前缀
    text=$(echo "$text" | sed -E 's/^记录(饮食|早餐|午餐|晚餐|加餐)[[:space:]]*//')
    echo "$text"
}

# ---- 主命令 ----

cmd="${1:-help}"
shift || true

case "$cmd" in
    pair)
        # 获取配对码
        result=$(curl -s "${API_BASE}/openclaw/api/pair-code")
        echo "$result" | jq -r '.data.message // .message // "获取失败"'
        ;;

    bind)
        # 保存 API Key
        key="${1:-}"
        if [[ -z "$key" ]]; then
            echo "用法: xiaoka.sh bind <api_key>"
            echo "或粘贴 AI 搭子的回复，自动提取 API Key。"
            exit 1
        fi
        # 尝试从粘贴文本中提取
        extracted=$(extract_api_key "$key")
        if [[ -n "$extracted" ]]; then
            key="$extracted"
        fi
        if [[ ! "$key" =~ ^oc_ ]]; then
            echo "无效的 API Key，应以 oc_ 开头。"
            exit 1
        fi
        save_config "$key"
        echo "API Key 已保存，绑定成功！"
        echo "现在可以使用「记录饮食 xxx」来记录饮食了。"
        ;;

    log)
        check_bindind
        text="${1:-}"
        meal_type="${2:-}"

        if [[ -z "$text" ]]; then
            echo "请描述你吃了什么。"
            echo "用法: xiaoka.sh log \"一碗米饭和红烧肉\" [breakfast|lunch|dinner|snack]"
            exit 1
        fi

        # 如果没有指定 meal_type，尝试从文本中检测
        if [[ -z "$meal_type" ]]; then
            meal_type=$(detect_meal_type "$text")
        fi

        # 提取纯食物描述
        food_text=$(extract_food_text "$text")
        if [[ -z "$food_text" ]]; then
            food_text="$text"
        fi

        # 构建请求 JSON
        json_body="{\"text\": \"${food_text}\"}"
        if [[ -n "$meal_type" ]]; then
            json_body="{\"text\": \"${food_text}\", \"meal_type\": \"${meal_type}\"}"
        fi

        result=$(curl -s -X POST "${API_BASE}/openclaw/api/food/log" \
            -H "Authorization: Bearer ${API_KEY}" \
            -H "Content-Type: application/json" \
            -d "$json_body")

        code=$(echo "$result" | jq -r '.code // 0')
        if [[ "$code" == "200" ]]; then
            message=$(echo "$result" | jq -r '.data.message')
            suggestion=$(echo "$result" | jq -r '.data.suggestion // empty')
            echo "$message"
            if [[ -n "$suggestion" ]]; then
                echo "建议: $suggestion"
            fi
            echo ""
            echo "食物明细:"
            echo "$result" | jq -r '.data.ingredients[] | "  - \(.name) \(.amount) \(.calories)卡\(if .from_db then " [食物库]" else " [AI估算]" end)"'
        elif [[ "$code" == "401" ]]; then
            echo "API Key 无效或已过期，请重新绑定。"
            rm -f "$CONFIG_FILE"
        elif [[ "$code" == "429" ]]; then
            echo "$(echo "$result" | jq -r '.message')"
        else
            echo "记录失败: $(echo "$result" | jq -r '.message // "未知错误"')"
        fi
        ;;

    today)
        check_bindind
        result=$(curl -s "${API_BASE}/openclaw/api/food/today" \
            -H "Authorization: Bearer ${API_KEY}")

        code=$(echo "$result" | jq -r '.code // 0')
        if [[ "$code" == "200" ]]; then
            total=$(echo "$result" | jq -r '.data.total_calories')
            count=$(echo "$result" | jq -r '.data.meal_count')
            date=$(echo "$result" | jq -r '.data.date')
            echo "📅 ${date} 共 ${count} 餐，总计 ${total} 卡"
            echo ""
            if [[ "$count" != "0" ]]; then
                echo "$result" | jq -r '.data.meals[] | "  \(.time) [\(.meal_type)] \(.food_title) — \(.calories)卡"'
            else
                echo "今天还没有记录，快来记录第一餐吧！"
            fi
        else
            echo "查询失败: $(echo "$result" | jq -r '.message // "未知错误"')"
        fi
        ;;

    help|*)
        echo "小卡健康 - OpenClaw 饮食记录"
        echo ""
        echo "命令:"
        echo "  xiaoka.sh pair              获取配对码"
        echo "  xiaoka.sh bind <api_key>    保存 API Key 完成绑定"
        echo "  xiaoka.sh log <text> [type] 记录饮食 (type: breakfast/lunch/dinner/snack)"
        echo "  xiaoka.sh today             查看今日饮食记录"
        echo ""
        echo "环境变量:"
        echo "  XIAOKA_API_KEY   API Key (也可通过 bind 命令保存)"
        echo "  XIAOKA_API_BASE  API 地址 (默认: https://cal-cn.ishuohua.cn)"
        ;;
esac
