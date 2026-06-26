#!/usr/bin/env bash
# setup.sh - Configure API credentials for translate-txt skill
#
# Usage:
#   Interactive:  bash setup.sh
#   Non-interactive (for AI agent):
#     bash setup.sh --api-key sk-xxx --base-url https://api.siliconflow.cn/v1 --model Qwen/Qwen2.5-7B-Instruct
#     bash setup.sh --api-key sk-xxx --provider siliconflow
#     bash setup.sh --api-key sk-xxx --provider deepseek
#     bash setup.sh --api-key sk-xxx --provider openai

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENV_FILE="$SCRIPT_DIR/.env"

# --- Helper functions ---

update_env() {
    local key="$1"
    local value="$2"
    if grep -q "^${key}=" "$ENV_FILE" 2>/dev/null; then
        local tmp=$(mktemp)
        sed "s|^${key}=.*|${key}=${value}|" "$ENV_FILE" > "$tmp" && mv "$tmp" "$ENV_FILE"
    else
        echo "${key}=${value}" >> "$ENV_FILE"
    fi
}

read_current() {
    local key="$1"
    local default="$2"
    local val
    val=$(grep "^${key}=" "$ENV_FILE" 2>/dev/null | head -1 | cut -d'=' -f2- | tr -d '"' | tr -d "'")
    echo "${val:-$default}"
}

PROVIDER_URLS="siliconflow:https://api.siliconflow.cn/v1 deepseek:https://api.deepseek.com/v1 openai:https://api.openai.com/v1"
PROVIDER_MODELS="siliconflow:Qwen/Qwen2.5-7B-Instruct deepseek:deepseek-chat openai:gpt-4o-mini"

get_provider_url() {
    for entry in $PROVIDER_URLS; do
        if [ "${entry%%:*}" = "$1" ]; then echo "${entry#*:}"; return; fi
    done
    echo ""
}

get_provider_model() {
    for entry in $PROVIDER_MODELS; do
        if [ "${entry%%:*}" = "$1" ]; then echo "${entry#*:}"; return; fi
    done
    echo ""
}

# --- Parse CLI arguments ---

API_KEY=""
BASE_URL=""
MODEL=""
PROVIDER=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --api-key)   API_KEY="$2";   shift 2 ;;
        --base-url)  BASE_URL="$2";  shift 2 ;;
        --model)     MODEL="$2";     shift 2 ;;
        --provider)
            PROVIDER="$2"; shift 2
            if [ -z "$(get_provider_url "$PROVIDER")" ]; then
                echo "ERROR: Unknown provider '$PROVIDER'. Supported: siliconflow, deepseek, openai" >&2
                exit 1
            fi
            ;;
        -h|--help)
            echo "Usage:"
            echo "  Interactive:    bash setup.sh"
            echo "  Non-interactive: bash setup.sh --api-key KEY [--provider PROVIDER|--base-url URL] [--model MODEL]"
            echo ""
            echo "Providers: siliconflow, deepseek, openai"
            exit 0
            ;;
        *)
            echo "ERROR: Unknown option '$1'" >&2
            exit 1
            ;;
    esac
done

# --- Create .env if needed ---

if [ ! -f "$ENV_FILE" ]; then
    touch "$ENV_FILE"
fi

# --- Non-interactive mode (CLI args provided) ---

if [ -n "$API_KEY" ]; then
    # Resolve provider -> base_url + model
    if [ -n "$PROVIDER" ]; then
        RESOLVED_URL=$(get_provider_url "$PROVIDER")
        RESOLVED_MODEL=$(get_provider_model "$PROVIDER")
        BASE_URL="${BASE_URL:-$RESOLVED_URL}"
        MODEL="${MODEL:-$RESOLVED_MODEL}"
    fi

    update_env "TRANSLATE_API_KEY" "$API_KEY"
    [ -n "$BASE_URL" ] && update_env "TRANSLATE_BASE_URL" "$BASE_URL"
    [ -n "$MODEL" ] && update_env "TRANSLATE_MODEL" "$MODEL"

    echo "CONFIG_SAVED:$ENV_FILE"
    exit 0
fi

# --- Interactive mode ---

echo "=== translate-txt Setup ==="
echo ""

echo "Please enter your API configuration:"
echo ""

# API Key (required)
current_key=$(read_current "TRANSLATE_API_KEY" "")
if [ -n "$current_key" ]; then
    read -p "API Key [current: ****${current_key: -4}]: " api_key
else
    read -p "API Key (required): " api_key
fi
if [ -n "$api_key" ]; then
    update_env "TRANSLATE_API_KEY" "$api_key"
else
    if [ -z "$current_key" ]; then
        echo "ERROR: API Key is required" >&2
        exit 1
    fi
fi

# Base URL
current_url=$(read_current "TRANSLATE_BASE_URL" "https://api.siliconflow.cn/v1")
echo ""
echo "Common Base URLs:"
echo "  1) SiliconFlow  - https://api.siliconflow.cn/v1"
echo "  2) DeepSeek     - https://api.deepseek.com/v1"
echo "  3) OpenAI       - https://api.openai.com/v1"
echo "  4) Custom"
read -p "Select provider [1-4] or press Enter to keep current (${current_url}): " url_choice

case "$url_choice" in
    1) base_url="https://api.siliconflow.cn/v1"; model_default="Qwen/Qwen2.5-7B-Instruct" ;;
    2) base_url="https://api.deepseek.com/v1"; model_default="deepseek-chat" ;;
    3) base_url="https://api.openai.com/v1"; model_default="gpt-4o-mini" ;;
    4) read -p "Enter custom Base URL: " base_url ;;
    *) base_url="$current_url" ;;
esac

if [ -n "$base_url" ]; then
    update_env "TRANSLATE_BASE_URL" "$base_url"
fi

# Model
current_model=$(read_current "TRANSLATE_MODEL" "Qwen/Qwen2.5-7B-Instruct")
model_hint="${model_default:-$current_model}"
read -p "Model name [press Enter to keep ${model_hint}]: " model
if [ -n "$model" ]; then
    update_env "TRANSLATE_MODEL" "$model"
elif [ -n "$model_default" ]; then
    update_env "TRANSLATE_MODEL" "$model_default"
fi

echo ""
echo "=== Configuration saved to $ENV_FILE ==="
echo ""
echo "You can now run translations with:"
echo "  python3 $SCRIPT_DIR/scripts/translate.py <input_file>"
