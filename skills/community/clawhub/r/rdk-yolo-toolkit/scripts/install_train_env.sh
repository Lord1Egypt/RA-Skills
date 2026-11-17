#!/bin/bash
# 训练机环境一键装（x86 Linux + GPU）
# 用法：bash install_train_env.sh
#   或：ssh user@gpu 'bash -s' < install_train_env.sh

set -e
echo "=== 训练机 / 量化机 环境一键装 ==="

# 0) Miniconda（如果没装）
if [ ! -d ~/miniconda3 ]; then
    echo "--- 装 Miniconda ---"
    cd ~
    if [ ! -f Miniconda3-latest-Linux-x86_64.sh ]; then
        wget -q https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    fi
    bash Miniconda3-latest-Linux-x86_64.sh -b -p ~/miniconda3
fi
source ~/miniconda3/etc/profile.d/conda.sh

# 1) Conda ToS（conda 26+ 必须）
echo "--- accept conda ToS ---"
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main 2>/dev/null || true
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r 2>/dev/null || true

# 2) 创建 rdk_env
if ! conda env list | grep -q '^rdk_env '; then
    echo "--- 创建 rdk_env (python 3.10) ---"
    conda create -n rdk_env python=3.10 -y
fi
conda activate rdk_env

# 3) 装包（清华源 + 长超时，国内必须）
PIP_OPTS="-i https://pypi.tuna.tsinghua.edu.cn/simple --timeout 60 --retries 10"
echo "--- 装 PyTorch (CUDA 12.1) ---"
pip install $PIP_OPTS torch torchvision --index-url https://download.pytorch.org/whl/cu121
echo "--- 装 ultralytics + rdkx5-yolo-mapper + onnx ---"
pip install $PIP_OPTS "ultralytics>=8.3.0" rdkx5-yolo-mapper onnx onnxsim
echo "--- 修 rdkx5-yolo-mapper 缺的 setuptools ---"
pip install $PIP_OPTS setuptools

# 4) 字体占位（防 ultralytics 卡 SSL 下载 Arial.ttf）
echo "--- 放字体占位 ---"
mkdir -p ~/.config/Ultralytics
[ -f ~/.config/Ultralytics/Arial.ttf ] || \
    cp /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf ~/.config/Ultralytics/Arial.ttf 2>/dev/null || \
    echo "   ⚠️ DejaVu 字体没装，需手动 apt install fonts-dejavu-core"

# 5) WSL2 GPU 检测
if [ -f /usr/lib/wsl/lib/nvidia-smi ] && ! which nvidia-smi >/dev/null 2>&1; then
    echo "--- WSL2 检测到 GPU 但 nvidia-smi 不在 PATH ---"
    grep -q '/usr/lib/wsl/lib' ~/.bashrc || \
        echo 'export PATH=/usr/lib/wsl/lib:$PATH' >> ~/.bashrc
    export PATH=/usr/lib/wsl/lib:$PATH
fi

# 6) 验证（任何一项失败请回到对应步骤修复）
echo ""
echo "=== 验证 ==="
python -c "import torch; print('torch', torch.__version__, 'cuda', torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else '(no GPU)')"
python -c "import pkg_resources; print('setuptools OK')"
python -c "import ultralytics; print('ultralytics', ultralytics.__version__)"
hb_mapper --version
ls ~/.config/Ultralytics/Arial.ttf >/dev/null && echo "Arial.ttf 占位 ✅"

echo ""
echo "=== 装好了。激活环境：conda activate rdk_env ==="
