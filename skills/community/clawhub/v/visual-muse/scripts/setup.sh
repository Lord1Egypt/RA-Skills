#!/usr/bin/env bash
set -euo pipefail

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; BLUE='\033[0;34m'; NC='\033[0m'
log()  { echo -e "${BLUE}[信息]${NC} $1"; }
ok()   { echo -e "${GREEN}[完成]${NC} $1"; }
warn() { echo -e "${YELLOW}[提示]${NC} $1"; }
err()  { echo -e "${RED}[错误]${NC} $1" >&2; }

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
AI_STUDIO_DIR="$HOME/ai-studio"
COMFY_DIR="$AI_STUDIO_DIR/comfyui"
VENV_DIR="$AI_STUDIO_DIR/comfyui-venv"
MODELS_DIR="$COMFY_DIR/models"
WORKSPACE_DIR="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
COMFYUI_URL="${COMFYUI_API_URL:-http://127.0.0.1:8188}"

echo
echo -e "${GREEN}╔════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   🎨 Visual Muse 一键安装向导       ║${NC}"
echo -e "${GREEN}║   ComfyUI + 模型 + Agent 全自动配置       ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════╝${NC}"
echo

# ============================================================
# 第一步：前置检查
# ============================================================
log "检查前置条件..."

for cmd in python3 curl git; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    err "缺少 $cmd，请先安装"
    exit 1
  fi
done
ok "python3 / curl / git 已就绪"

# 检测系统
OS="$(uname -s)"
ARCH="$(uname -m)"
if [[ "$OS" == "Darwin" && "$ARCH" == "arm64" ]]; then
  ok "检测到 macOS Apple Silicon — 将使用 MPS 加速"
  PLATFORM="macos_arm"
elif [[ "$OS" == "Linux" ]]; then
  if command -v nvidia-smi >/dev/null 2>&1; then
    ok "检测到 Linux + NVIDIA GPU — 将使用 CUDA 加速"
    PLATFORM="linux_nvidia"
  else
    warn "检测到 Linux 但未发现 NVIDIA GPU — 将使用 CPU 模式（很慢）"
    PLATFORM="linux_cpu"
  fi
else
  warn "未识别的平台 $OS/$ARCH — 将尝试通用安装"
  PLATFORM="generic"
fi

# ============================================================
# 第二步：安装 ComfyUI
# ============================================================
echo
log "=== 安装 ComfyUI ==="

if [ -d "$COMFY_DIR/.git" ]; then
  warn "ComfyUI 已存在于 $COMFY_DIR，跳过克隆"
else
  log "克隆 ComfyUI..."
  mkdir -p "$AI_STUDIO_DIR"
  git clone --depth 1 https://github.com/comfyanonymous/ComfyUI.git "$COMFY_DIR" || \
  git clone --depth 1 https://ghfast.top/https://github.com/comfyanonymous/ComfyUI.git "$COMFY_DIR" || {
    err "ComfyUI 克隆失败，请检查网络后重试"
    exit 1
  }
  ok "ComfyUI 克隆完成"
fi

# 创建虚拟环境
if [ ! -d "$VENV_DIR" ]; then
  log "创建 Python 虚拟环境..."
  python3 -m venv "$VENV_DIR"
  ok "虚拟环境创建完成"
else
  warn "虚拟环境已存在，跳过"
fi

source "$VENV_DIR/bin/activate"

log "安装 PyTorch 和 ComfyUI 依赖（这一步需要几分钟）..."
pip install --upgrade pip setuptools wheel -q
pip install torch torchvision torchaudio -q
pip install -r "$COMFY_DIR/requirements.txt" -q
ok "PyTorch 和 ComfyUI 依赖安装完成"

# 安装 ComfyUI-Manager
if [ ! -d "$COMFY_DIR/custom_nodes/ComfyUI-Manager/.git" ]; then
  log "安装 ComfyUI-Manager..."
  mkdir -p "$COMFY_DIR/custom_nodes"
  git clone --depth 1 https://github.com/ltdrdata/ComfyUI-Manager.git "$COMFY_DIR/custom_nodes/ComfyUI-Manager" || \
  git clone --depth 1 https://ghfast.top/https://github.com/ltdrdata/ComfyUI-Manager.git "$COMFY_DIR/custom_nodes/ComfyUI-Manager" || \
  warn "ComfyUI-Manager 安装失败，不影响核心功能"
  ok "ComfyUI-Manager 安装完成"
else
  warn "ComfyUI-Manager 已存在，跳过"
fi

# 创建模型目录
mkdir -p "$MODELS_DIR/checkpoints" "$MODELS_DIR/vae" "$MODELS_DIR/clip" "$MODELS_DIR/loras" "$MODELS_DIR/controlnet"

# 创建符号链接
if [ ! -L "$AI_STUDIO_DIR/models" ]; then
  if [ ! -e "$AI_STUDIO_DIR/models" ]; then
    ln -s "$MODELS_DIR" "$AI_STUDIO_DIR/models"
  fi
fi

# 创建启动脚本
mkdir -p "$AI_STUDIO_DIR/outputs"
cat > "$AI_STUDIO_DIR/start_comfyui.sh" << 'STARTEOF'
#!/usr/bin/env bash
set -euo pipefail
source "$HOME/ai-studio/comfyui-venv/bin/activate"
cd "$HOME/ai-studio/comfyui"
echo "[信息] 启动 ComfyUI（listen 0.0.0.0:8188 --highvram --fp32-vae）..."
echo "[信息] 浏览器访问 http://127.0.0.1:8188"
echo "[信息] 按 Ctrl+C 停止"
python main.py --listen 0.0.0.0 --port 8188 --highvram --fp32-vae
STARTEOF
chmod +x "$AI_STUDIO_DIR/start_comfyui.sh"
ok "启动脚本已生成"

# ============================================================
# 第三步：下载模型
# ============================================================
echo
log "=== 下载模型（约 7GB，支持断点续传）==="

download() {
  local url="$1" output="$2" name="$3"
  if [ -s "$output" ]; then
    local size; size="$(du -h "$output" | awk '{print $1}')"
    warn "$name 已存在（$size），跳过"
    return 0
  fi
  log "下载 $name..."
  curl -L -C - --progress-bar -o "$output" "$url" || \
  curl -L -C - --progress-bar -o "$output" "$(echo "$url" | sed 's|https://huggingface.co|https://hf-mirror.com|')" || {
    warn "$name 下载失败，可稍后手动下载"
    rm -f "$output"
    return 0
  }
  ok "$name 下载完成"
}

download \
  "https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors" \
  "$MODELS_DIR/checkpoints/sd_xl_base_1.0.safetensors" \
  "SDXL Base 1.0（6.5GB）"

download \
  "https://huggingface.co/stabilityai/sdxl-vae/resolve/main/sdxl_vae.safetensors" \
  "$MODELS_DIR/vae/sdxl_vae.safetensors" \
  "SDXL VAE（335MB）"

download \
  "https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors" \
  "$MODELS_DIR/clip/clip_l.safetensors" \
  "CLIP L（250MB）"

# ============================================================
# 第四步：复制 skill 工具和模板
# ============================================================
echo
log "=== 配置 Agent 工具和模板 ==="

mkdir -p "$WORKSPACE_DIR/tools" "$WORKSPACE_DIR/workflows" "$WORKSPACE_DIR/runtime" "$WORKSPACE_DIR/runs"

for f in comfyui-client.py run-tracker.py; do
  if [ ! -f "$WORKSPACE_DIR/tools/$f" ] && [ -f "$SKILL_DIR/tools/$f" ]; then
    cp "$SKILL_DIR/tools/$f" "$WORKSPACE_DIR/tools/$f"
    ok "已部署工具：$f"
  else
    warn "工具已存在或源文件不存在：$f"
  fi
done

if [ ! -f "$WORKSPACE_DIR/workflows/sdxl_basic.json" ] && [ -f "$SKILL_DIR/workflows/sdxl_basic.json" ]; then
  cp "$SKILL_DIR/workflows/sdxl_basic.json" "$WORKSPACE_DIR/workflows/sdxl_basic.json"
  ok "已部署工作流模板"
fi

if [ ! -f "$WORKSPACE_DIR/prompt-templates.json" ] && [ -f "$SKILL_DIR/resources/prompt-templates.json" ]; then
  cp "$SKILL_DIR/resources/prompt-templates.json" "$WORKSPACE_DIR/prompt-templates.json"
  ok "已部署 prompt 模板库"
fi

if [ ! -f "$WORKSPACE_DIR/preferences.json" ] && [ -f "$SKILL_DIR/resources/preferences.json" ]; then
  cp "$SKILL_DIR/resources/preferences.json" "$WORKSPACE_DIR/preferences.json"
  ok "已初始化偏好档案"
fi

# ============================================================
# 第五步：验证
# ============================================================
echo
log "=== 最终验证 ==="

PASS=0; FAIL=0

check() {
  if [ -f "$1" ] || [ -d "$1" ]; then
    ok "$2"; PASS=$((PASS+1))
  else
    err "$2 — 缺失"; FAIL=$((FAIL+1))
  fi
}

check "$COMFY_DIR/main.py" "ComfyUI 安装"
check "$VENV_DIR/bin/python" "Python 虚拟环境"
check "$MODELS_DIR/checkpoints/sd_xl_base_1.0.safetensors" "SDXL 模型"
check "$WORKSPACE_DIR/tools/comfyui-client.py" "API 客户端"
check "$WORKSPACE_DIR/workflows/sdxl_basic.json" "工作流模板"
check "$WORKSPACE_DIR/prompt-templates.json" "Prompt 模板库"

echo
echo -e "${GREEN}╔════════════════════════════════════════════╗${NC}"
if [ "$FAIL" -eq 0 ]; then
  echo -e "${GREEN}║   ✅ 安装完成！$PASS/$PASS 项检查通过        ║${NC}"
else
  echo -e "${YELLOW}║   ⚠️  安装部分完成（$PASS 通过 / $FAIL 失败）  ║${NC}"
fi
echo -e "${GREEN}╚════════════════════════════════════════════╝${NC}"
echo
echo "接下来："
echo
echo "  1) 启动 ComfyUI（新开终端窗口）："
echo "     bash ~/ai-studio/start_comfyui.sh"
echo
echo "  2) 对 OpenClaw 说："
echo "     「画一张赛博朋克猫在雨夜街道」"
echo
echo "  图片输出在：~/ai-studio/comfyui/output/creative_workshop/"
echo
