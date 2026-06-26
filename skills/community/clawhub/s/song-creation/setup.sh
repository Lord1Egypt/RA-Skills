#!/usr/bin/env bash
set -euo pipefail

# ═══════════════════════════════════════════════════════════
# Song Creation Skill - One-Click Setup
# ═══════════════════════════════════════════════════════════
# Requirements: Linux, ROCm or CUDA GPU, 16GB+ VRAM
# This script installs ComfyUI + AceStep + required models
# ═══════════════════════════════════════════════════════════

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BOLD='\033[1m'; NC='\033[0m'
info() { echo -e "${GREEN}[✓]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }
err()  { echo -e "${RED}[✗]${NC} $1"; }
header() { echo -e "\n${BOLD}━━━ $1 ━━━${NC}"; }

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
COMIFY_DIR="$HOME/ai"
COMFYUI_DIR="$COMIFY_DIR/ComfyUI"
VENV_DIR="$COMIFY_DIR/comfyui-venv"
WORKFLOW_DIR="$COMFYUI_DIR/user/default/workflows/api工作流"

# ─── CHECK: GPU ───────────────────────────────────────────
header "检查 GPU"

if command -v rocm-smi &>/dev/null; then
    GPU_INFO=$(rocm-smi --showproductname 2>/dev/null | grep "GPU" | head -1 || true)
    VRAM=$(rocm-smi --showmeminfo vram 2>/dev/null | grep "Total" | head -1 | grep -oP '\d+' || echo "0")
    info "ROCm GPU detected: ${GPU_INFO:-AMD}"
    info "VRAM: ${VRAM} MB"
    BACKEND="rocm"
elif command -v nvidia-smi &>/dev/null; then
    GPU_INFO=$(nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>/dev/null | head -1 || true)
    info "CUDA GPU detected: ${GPU_INFO}"
    BACKEND="cuda"
else
    warn "No GPU detected. AceStep requires a GPU with 16GB+ VRAM."
    warn "Install ROCm (AMD) or CUDA (NVIDIA) drivers first."
    warn "https://rocm.docs.amd.com/ / https://developer.nvidia.com/cuda-downloads"
    exit 1
fi

# Extract VRAM number
VRAM_NUM=$(echo "$VRAM" | grep -oP '^\d+' || echo "0")
if [ "$VRAM_NUM" -lt 16384 ] 2>/dev/null; then
    warn "VRAM (${VRAM} MB) is below the recommended 16GB minimum."
    warn "Generation may be limited to shorter durations."
fi

# ─── CHECK: Python ────────────────────────────────────────
header "检查 Python"
PYTHON=$(command -v python3 || echo "")
if [ -z "$PYTHON" ]; then
    err "Python 3.10+ is required. Install it first."
    exit 1
fi
PY_VER=$($PYTHON --version 2>&1)
info "$PY_VER"

# ─── SETUP: AI directory ──────────────────────────────────
header "创建目录结构"
mkdir -p "$COMIFY_DIR"
mkdir -p "$COMIFY_DIR/ComfyUI/models/ace"
info "Directory: $COMIFY_DIR"

# ─── INSTALL: ComfyUI ─────────────────────────────────────
header "安装 ComfyUI"
if [ -d "$COMFYUI_DIR" ]; then
    info "ComfyUI already exists at $COMFYUI_DIR"
else
    warn "Cloning ComfyUI from github.com/comfyanonymous/ComfyUI..."
    git clone https://github.com/comfyanonymous/ComfyUI.git "$COMFYUI_DIR"
    info "ComfyUI cloned"
fi

# ─── SETUP: Virtualenv ────────────────────────────────────
header "配置 Python 虚拟环境"
if [ -d "$VENV_DIR" ]; then
    info "Virtualenv already exists"
else
    warn "Creating virtualenv..."
    $PYTHON -m venv "$VENV_DIR"
    warn "Installing PyTorch + ComfyUI dependencies..."
    "$VENV_DIR/bin/pip" install --upgrade pip

    if [ "$BACKEND" = "rocm" ]; then
        "$VENV_DIR/bin/pip" install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm7.1
    else
        "$VENV_DIR/bin/pip" install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cuda126
    fi

    "$VENV_DIR/bin/pip" install -r "$COMFYUI_DIR/requirements.txt"
    "$VENV_DIR/bin/pip" install requests
    info "Dependencies installed"
fi

# ─── SETUP: Custom nodes ──────────────────────────────────
header "安装必要自定义节点"
cd "$COMFYUI_DIR/custom_nodes"
NODES=(
    "https://github.com/ltdrdata/ComfyUI-Manager"
)
for repo in "${NODES[@]}"; do
    name=$(basename "$repo")
    if [ -d "$name" ]; then
        info "Node $name already installed"
    else
        warn "Installing $name..."
        git clone "$repo" 2>/dev/null || true
    fi
done

# ─── DOWNLOAD: AceStep models ────────────────────────────
header "下载 AceStep 模型（约 18GB）"
MODELS_DIR="$COMIFY_DIR/ComfyUI/models"

download_model() {
    local url="$1"
    local path="$2"
    local dir=$(dirname "$path")
    mkdir -p "$dir"
    if [ -f "$path" ]; then
        info "Already exists: $(basename $path) ($(du -h "$path" | cut -f1))"
    else
        warn "Downloading $(basename $path)..."
        wget -q --show-progress -O "$path.tmp" "$url" && mv "$path.tmp" "$path"
        info "Downloaded: $(basename $path)"
    fi
}

download_model \
    "https://huggingface.co/Looky916/AceStep-v1.5/resolve/main/acestep_v1.5_xl_sft_bf16.safetensors" \
    "$MODELS_DIR/ace/acestep_v1.5_xl_sft_bf16.safetensors"

download_model \
    "https://huggingface.co/Looky916/AceStep-v1.5/resolve/main/ace_1.5_vae.safetensors" \
    "$MODELS_DIR/ace/ace_1.5_vae.safetensors"

download_model \
    "https://huggingface.co/Looky916/AceStep-v1.5/resolve/main/qwen_0.6b_ace15.safetensors" \
    "$MODELS_DIR/ace/qwen_0.6b_ace15.safetensors"

download_model \
    "https://huggingface.co/Looky916/AceStep-v1.5/resolve/main/qwen_4b_ace15.safetensors" \
    "$MODELS_DIR/ace/qwen_4b_ace15.safetensors"

# ─── SETUP: Workflow file ─────────────────────────────────
header "配置工作流文件"
mkdir -p "$WORKFLOW_DIR"
WF_FILE="$WORKFLOW_DIR/audio_ace_step1_5_xl_sft.json"
if [ -f "$WF_FILE" ]; then
    info "Workflow already exists"
else
    warn "Workflow file not found. Create it by opening ComfyUI GUI once and saving the workflow."
    warn "Or manually place the workflow at: $WF_FILE"
fi

# ─── CREATE: startup script ──────────────────────────────
header "创建启动脚本"
cat > "$COMIFY_DIR/run_comfyui.sh" << 'SCRIPT'
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
echo "🚀 ComfyUI 启动脚本"
echo "📂 进入目录: $SCRIPT_DIR"
cd "$SCRIPT_DIR" || exit 1
echo "🐍 激活虚拟环境"
source comfyui-venv/bin/activate
echo "📂 进入 ComfyUI 目录"
cd "$SCRIPT_DIR/ComfyUI" || exit 1
echo "⚙️ 启动 ComfyUI (监听 127.0.0.1)..."
python main.py --listen 127.0.0.1 --enable-cors-header
echo ""
echo "⚠️ 程序已停止运行。"
SCRIPT
chmod +x "$COMIFY_DIR/run_comfyui.sh"
info "Startup script: $COMIFY_DIR/run_comfyui.sh"

# ─── CREATE: engine operation manual ─────────────────────
header "生成引擎操作手册"
MANUAL="$SKILL_DIR/references/comfyui_music_generation.md"
mkdir -p "$(dirname "$MANUAL")"
cat > "$MANUAL" << 'MANUAL'
# ComfyUI + AceStep 音乐生成操作手册（引擎 ⚙️ 专用）

## 启动 ComfyUI
```bash
bash ~/ai/run_comfyui.sh
```
（用 PTY 模式启动，等待看到 "Starting server" 和 "To see the GUI go to: http://127.0.0.1:8188"）

## 关键规则
1. ❌ 不要加 --gpu-only 参数
2. ❌ 不要手动拼 python main.py 路径
3. ❌ 不要修改工作流中 clip 字段（保持节点引用 ["105", 0]）
4. ❌ 不要给 lyrics 加 "歌名：《XXX》" 前缀
5. ✅ 每次 spawn 引擎时先读此文件

## 参数修改
- Node 94: tags / lyrics / bpm / keyscale / duration / temperature / top_p / cfg_scale / language / seed
- Node 98: seconds（实际时长控制）
- Node 107: filename_prefix（格式 YYYYMMDD/audio/歌曲名）

## 稳定参数
- Steps: 50（工作流默认）
- cfg_scale: 7
- duration: 185s
- VAE: VAEDecodeAudioTiled（工作流自带）

## 模型位置
- UNET: ~/ai/ComfyUI/models/ace/acestep_v1.5_xl_sft_bf16.safetensors
- VAE: ~/ai/ComfyUI/models/ace/ace_1.5_vae.safetensors
- CLIP1: ~/ai/ComfyUI/models/ace/qwen_0.6b_ace15.safetensors
- CLIP2: ~/ai/ComfyUI/models/ace/qwen_4b_ace15.safetensors

## 输出文件管理
生成后从 ~/ai/ComfyUI/output/ 移到 ~/.openclaw/workspace/output/YYYYMMDD/audio/
删除 ComfyUI output 中的原文件。
MANUAL
info "Operation manual: $MANUAL"

# ─── SUMMARY ─────────────────────────────────────────────
header "✅ 安装完成"
echo ""
echo -e "${BOLD}使用方式：${NC}"
echo "  1. 启动 ComfyUI:  bash ~/ai/run_comfyui.sh"
echo "  2. 触发技能:  在 OpenClaw 中说"创作一首歌""
echo "  3. 或手动:    cd $SKILL_DIR && python scripts/submit_song.py --help"
echo ""
echo -e "${BOLD}目录结构：${NC}"
echo "  $SKILL_DIR/"
echo "  ├── SKILL.md"
echo "  ├── setup.sh"
echo "  ├── scripts/submit_song.py"
echo "  └── references/comfyui_music_generation.md"
echo ""
echo -e "${BOLD}注意事项：${NC}"
echo "  • 首次启动 ComfyUI 需要下载模型（约 18GB），已包含在安装流程中"
echo "  • 如果工作流文件不存在，需启动 ComfyUI 后从 GUI 手动创建并保存"
echo "  • CFG scale 推荐使用 7（已验证稳定）"
echo "  • 歌词中不要包含"歌名："前缀行"
