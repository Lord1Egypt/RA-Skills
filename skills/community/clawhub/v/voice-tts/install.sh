#!/usr/bin/env bash
#
# voice-tts 安装脚本
# 用法: bash install.sh [--model MODEL] [--proxy PROXY]
#
# 示例:
#   bash install.sh                           # 默认安装 turbo 模型
#   bash install.sh --model base             # 安装 base 模型（更小更快）
#   bash install.sh --proxy http://127.0.0.1:7897  # 国内需代理
#

set -euo pipefail

# ── 参数解析 ──────────────────────────────────────
MODEL="turbo"
PROXY=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --model) MODEL="$2"; shift 2 ;;
    --proxy) PROXY="$2"; shift 2 ;;
    *) echo "未知参数: $1"; exit 1 ;;
  esac
done

# ── 颜色 ─────────────────────────────────────────
RED='\033[0;31m'; GRN='\033[0;32m'; YEL='\033[1;33m'; BLU='\033[0;34m'; NC='\033[0m'
info()  { echo -e "${BLU}[INFO]${NC} $1"; }
ok()    { echo -e "${GRN}[ OK ]${NC} $1"; }
warn()  { echo -e "${YEL}[WARN]${NC} $1"; }
err()   { echo -e "${RED}[ERR ]${NC} $1"; exit 1; }

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"

# ── 0. 检查 Node.js ───────────────────────────────
info "检查 Node.js..."
command -v node >/dev/null 2>&1 || err "需要 Node.js >= 18，请先安装: https://nodejs.org/"
NODE_VER=$(node -v | tr -d 'v')
MAJOR_VER=$(echo "$NODE_VER" | cut -d. -f1)
[[ "$MAJOR_VER" -ge 18 ]] || err "Node.js 版本过低: $NODE_VER，需要 >= 18"
ok "Node.js $NODE_VER ✓"

# ── 1. 安装 Python 依赖 ───────────────────────────
info "安装 Python 依赖..."
command -v python3 >/dev/null 2>&1 || err "需要 python3，请先安装"

PIP_CMD="pip3 install edge-tts whisper click"
if [[ -n "$PROXY" ]]; then
  PIP_CMD="pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple edge-tts whisper click"
  export https_proxy="$PROXY" http_proxy="$PROXY"
fi

$PIP_CMD 2>&1 | tail -3
ok "Python 依赖安装完成 ✓"

# ── 2. 安装 ffmpeg ───────────────────────────────
info "检查 ffmpeg..."
if command -v ffmpeg >/dev/null 2>&1; then
  ok "ffmpeg 已安装: $(ffmpeg -version 2>&1 | head -1)"
else
  if [[ "$(uname)" == "Darwin" ]]; then
    info "检测到 macOS，尝试用 brew 安装 ffmpeg..."
    brew install ffmpeg 2>&1 | tail -3
  else
    info "检测到 Linux，尝试用 apt 安装 ffmpeg..."
    sudo apt install -y ffmpeg 2>&1 | tail -3
  fi
  ok "ffmpeg 安装完成 ✓"
fi

# ── 3. 下载 Whisper 模型 ─────────────────────────
info "下载 Whisper 模型: $MODEL (首次需要网络，模型约 800MB)..."
export HTTPS_PROXY="$PROXY"
export HTTP_PROXY="$PROXY"
python3 - <<EOF
import whisper
print(f"下载模型: $MODEL ...")
whisper.load_model("$MODEL")
print("下载完成 ✓")
EOF
ok "Whisper 模型 $MODEL 就绪 ✓"

# ── 4. 检查 skill 脚本权限 ───────────────────────
info "检查脚本权限..."
chmod +x "$SKILL_DIR/bin/voice-tts.mjs"
chmod +x "$SKILL_DIR/bin/voice-asr.mjs"
chmod +x "$SKILL_DIR/scripts/send_voice_reply.mjs"
chmod +x "$SKILL_DIR/scripts/auto_voice_check"
ok "脚本权限设置完成 ✓"

# ── 5. 生成 OpenClaw 配置片段 ─────────────────────
info "生成 OpenClaw 配置片段..."
OPENCLAW_CONF="$SKILL_DIR/openclaw_config_fragment.json"
cat > "$OPENCLAW_CONF" <<'CONF'
{
  "tools": {
    "media": {
      "audio": {
        "enabled": true,
        "models": [
          {
            "type": "cli",
            "command": "node",
            "args": [
              "SKILL_PATH_PLACEHOLDER/voice-tts/bin/voice-asr.mjs",
              "--model", "turbo",
              "--language", "zh",
              "{{MediaPath}}"
            ]
          }
        ]
      }
    }
  }
}
CONF

# ── 6. 生成 agent 音色配置片段（可选）──────────────
AGENT_VOICES_CONF="$SKILL_DIR/openclaw_agent_voices_fragment.json"
cat > "$AGENT_VOICES_CONF" <<'CONF'
{
  "skills": {
    "entries": {
      "voice-tts": {
        "enabled": true,
        "config": {
          "tts": {
            "defaultVoice": "zh-CN-XiaoxiaoNeural",
            "agentVoices": {
              "main":       "zh-CN-XiaoxiaoNeural",
              "researcher": "zh-CN-YunxiNeural",
              "product":    "zh-CN-XiaoyiNeural",
              "coder":      "zh-CN-YunyangNeural",
              "devops":     "zh-CN-YunjianNeural"
            }
          },
          "asr": {
            "defaultInitialPrompt": "以下是中文语音转文字。常见词包括：管家、研究员、邮差、码农、产品、运维、OpenClaw、小爱、Telegram。",
            "defaultTemperature": 0,
            "conditionOnPreviousText": true
          }
        }
      }
    }
  }
}
CONF

# ── 7. 验证安装 ───────────────────────────────────
info "验证安装..."
TTS_OUT=$(node "$SKILL_DIR/bin/voice-tts.mjs" "安装测试" -f /tmp/tts-test.mp3 --agent main 2>&1)
if [[ -f /tmp/tts-test.mp3 && -s /tmp/tts-test.mp3 ]]; then
  ok "TTS 生成验证通过 ✓"
  rm -f /tmp/tts-test.mp3
else
  warn "TTS 生成验证未通过，请检查 edge-tts 安装"
fi

# ── 8. 完成提示 ───────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GRN}✅ 安装完成！${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${BLU}下一步：将配置加入 openclaw.json${NC}"
echo ""
echo "  1. 打开 ~/.openclaw/openclaw.json"
echo "  2. 在对应位置加入以下内容："
echo ""
echo "  【必选】tools.media.audio（启用语音识别）："
echo "  → 已生成片段: $OPENCLAW_CONF"
echo ""
echo "  【可选】skills.entries.voice-tts.config（agent 音色映射）："
echo "  → 已生成片段: $AGENT_VOICES_CONF"
echo ""
echo -e "${BLU}重启 OpenClaw 使配置生效：${NC}"
echo "  openclaw gateway restart"
echo ""
echo -e "${BLB}测试语音识别：${NC}"
echo "  node $SKILL_DIR/bin/voice-asr.mjs <音频文件>"
echo ""
echo -e "${YEL}注意：send_voice_reply.mjs 需要 Telegram Bot Token，${NC}"
echo -e "${YEL}       国内需要配置代理访问 Telegram API${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
