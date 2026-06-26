#!/bin/bash
# check-config.sh - 检查 video-summarizer 配置是否就绪
# 用法：./check-config.sh
# 版本：v1.0.13

ENV_FILE="$HOME/.openclaw/.env"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

PASS=0
FAIL=0

check_env() {
    local var=$1 desc=$2 required=${3:-true}
    local value=$(grep "^${var}=" "$ENV_FILE" 2>/dev/null | cut -d'=' -f2- | tr -d '"')
    if [[ -n "$value" ]]; then
        echo "✅ $desc"
        PASS=$((PASS + 1))
        return 0
    else
        if [[ "$required" == "true" ]]; then
            echo "❌ $desc"
            FAIL=$((FAIL + 1))
            return 1
        else
            echo "⚠️  $desc (可选)"
            return 0
        fi
    fi
}

check_py() {
    local pkg=$1 install=$2
    if python3 -c "import $pkg" &>/dev/null; then
        echo "✅ $pkg"
        PASS=$((PASS + 1))
    else
        echo "❌ $pkg (运行：pip3 install $install)"
        FAIL=$((FAIL + 1))
    fi
}

echo "=== 依赖工具 ==="
command -v yt-dlp &>/dev/null && { echo "✅ yt-dlp ($(yt-dlp --version))"; PASS=$((PASS + 1)); } || { echo "❌ yt-dlp (运行：pip3 install yt-dlp)"; FAIL=$((FAIL + 1)); }
command -v ffmpeg &>/dev/null && { echo "✅ ffmpeg"; PASS=$((PASS + 1)); } || { echo "❌ ffmpeg (运行：apt install ffmpeg)"; FAIL=$((FAIL + 1)); }
command -v python3 &>/dev/null && { echo "✅ $(python3 --version)"; PASS=$((PASS + 1)); } || { echo "❌ python3"; FAIL=$((FAIL + 1)); exit 1; }

echo ""
echo "=== Python 依赖 ==="
check_py "requests" "requests"
check_py "oss2" "oss2"
check_py "dotenv" "python-dotenv"

echo ""
echo "=== LLM AI 分析配置 ==="
CONFIG_OK=true
LLM_CONFIGURED=false

LLM_API_KEY=$(grep "^LLM_API_KEY=" "$ENV_FILE" 2>/dev/null | cut -d'=' -f2- | tr -d '"' | tr -d "'")
LLM_BASE_URL=$(grep "^LLM_BASE_URL=" "$ENV_FILE" 2>/dev/null | cut -d'=' -f2- | tr -d '"' | tr -d "'")
LLM_MODEL=$(grep "^LLM_MODEL=" "$ENV_FILE" 2>/dev/null | cut -d'=' -f2- | tr -d '"' | tr -d "'")

MISSING_VARS=""
[[ -z "$LLM_API_KEY" ]] && MISSING_VARS="$MISSING_VARS LLM_API_KEY"
[[ -z "$LLM_BASE_URL" ]] && MISSING_VARS="$MISSING_VARS LLM_BASE_URL"
[[ -z "$LLM_MODEL" ]] && MISSING_VARS="$MISSING_VARS LLM_MODEL"

if [[ -z "$MISSING_VARS" ]]; then
    echo "✅ LLM_API_KEY（已配置）"
    echo "✅ LLM_BASE_URL: $LLM_BASE_URL"
    echo "✅ LLM_MODEL: $LLM_MODEL"
    LLM_CONFIGURED=true
    PASS=$((PASS + 3))
else
    echo "❌ LLM 配置不完整，缺少：$MISSING_VARS"
    echo "   └─ 请在 ~/.openclaw/.env 中配置："
    echo "      LLM_API_KEY=your_api_key"
    echo "      LLM_BASE_URL=https://api.deepseek.com"
    echo "      LLM_MODEL=deepseek-v4-pro"
    FAIL=$((FAIL + 1))
fi

if [[ "$LLM_CONFIGURED" != "true" ]]; then
    CONFIG_OK=false
fi

echo ""
echo "=== OSS 图床配置 ==="
check_env "ALIYUN_OSS_AK" "阿里云 OSS AccessKey" || CONFIG_OK=false
check_env "ALIYUN_OSS_SK" "阿里云 OSS Secret" || CONFIG_OK=false
check_env "ALIYUN_OSS_BUCKET_ID" "阿里云 OSS Bucket" || CONFIG_OK=false
check_env "ALIYUN_OSS_ENDPOINT" "阿里云 OSS Endpoint" || CONFIG_OK=false

echo ""
echo "=== 可选配置 ==="
if grep -q "^GROQ_API_KEY=" "$ENV_FILE" 2>/dev/null; then
    echo "✅ Groq API Key"
    echo "   └─ Plan B 可用 (Groq)"
    PASS=$((PASS + 1))
else
    echo "⚠️  Groq API Key (可选)"
    echo "   └─ Plan B 需本地 Whisper (pip install openai-whisper)"
fi

if grep -q "^NOTION_API_KEY=" "$ENV_FILE" 2>/dev/null; then
    echo "✅ Notion API Key"
    echo "   └─ Notion 推送可用"
    PASS=$((PASS + 1))
else
    echo "⚠️  Notion API Key (可选)"
    echo "   └─ Notion 推送不可用"
fi

echo ""
echo "=== Cookies ==="
COOKIE_FILE="$HOME/.cookies/bilibili_cookies.txt"
if [[ -f "$COOKIE_FILE" ]]; then
    # 检查文件年龄
    COOKIE_AGE=$(( ($(date +%s) - $(stat -c %Y "$COOKIE_FILE" 2>/dev/null || echo $(date +%s))) / 86400 ))
    if [[ $COOKIE_AGE -lt 30 ]]; then
        echo "✅ B 站 Cookies (已更新$COOKIE_AGE 天前)"
        echo "   └─ Plan A 可用 (官方字幕)"
        PASS=$((PASS + 1))
    elif [[ $COOKIE_AGE -lt 60 ]]; then
        echo "⚠️  B 站 Cookies (已更新$COOKIE_AGE 天前，建议更新)"
        echo "   └─ Plan A 可用，但可能即将过期"
    else
        echo "❌ B 站 Cookies (已更新$COOKIE_AGE 天前，很可能过期)"
        echo "   └─ 建议扫码登录更新"
        FAIL=$((FAIL + 1))
    fi
else
    echo "⚠️  B 站 Cookies (可选)"
    echo "   └─ Plan A 仅可用自动字幕，无字幕时降级 Plan B"
fi

# 检查扫码登录工具
if command -v biliup &>/dev/null; then
    echo "✅ biliup (扫码登录工具)"
    PASS=$((PASS + 1))
else
    echo "⚠️  biliup 未安装 (扫码登录工具)"
    echo "   └─ 安装：pip3 install biliup --break-system-packages"
fi

echo ""
echo "================================"
echo "总计：$PASS 通过 | $FAIL 失败"
echo "================================"
echo ""

if [[ "$CONFIG_OK" == "true" && $FAIL -eq 0 ]]; then
    echo "✅ 配置就绪，可以开始使用！"
    echo ""
    echo "快速开始:"
    echo "  $SCRIPT_DIR/video-summarize.sh \"视频 URL\" /tmp/output"
    echo ""
    echo "选项:"
    echo "  --verbose     显示详细日志"
    echo "  --push        自动推送到 Notion"
    echo "  --keep-video  保留视频文件"
    echo ""
    echo "📱 扫码登录 (更新 B 站 Cookies):"
    echo "  $SCRIPT_DIR/bili-login.sh"
    exit 0
else
    echo "❌ 配置不完整，请修复上方标 ❌ 的项目"
    echo ""
    echo "修复建议:"
    echo "  1. 编辑配置文件：~/.openclaw/.env"
    echo "  2. 安装缺失依赖：pip3 install requests oss2 python-dotenv"
    echo "  3. 扫码登录：$SCRIPT_DIR/bili-login.sh"
    echo "  4. 重新运行检查：$SCRIPT_DIR/check-config.sh"
    exit 1
fi
