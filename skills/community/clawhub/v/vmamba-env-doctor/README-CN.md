# VMamba 环境配置助手 Skill

这是一个 Skill，旨在帮助用户为 [VMamba](https://github.com/MzeroMiko/VMamba) 项目搭建**稳定且经过验证的 Python 环境**，并快速解决常见的安装和编译错误。

## 本 Skill 涵盖内容

- 安装正确版本的 PyTorch、CUDA、MMCV 及其他依赖项。
- 无错编译 `selective_scan` CUDA 内核。
- 解决以下常见问题：
  - `ModuleNotFoundError: No module named 'torch'`（构建隔离导致）
  - `unsupported GNU version`（gcc 版本过高）
  - `libc10.so: cannot open shared object file`（动态库路径缺失）
  - `undefined symbol: iJIT_NotifyEvent`（MKL 版本冲突）
  - NumPy 2.x 与 OpenCV 的兼容性冲突

## 稳定环境组合

| 组件 | 推荐版本 |
| :--- | :--- |
| Python | 3.10 |
| PyTorch | 2.1.0 |
| CUDA | 11.8 |
| gcc/g++ | 11 |
| mmengine | 0.10.1 |
| mmcv | 2.1.0 |
| mmsegmentation | 1.2.2 |
| mmdet | 3.3.0 |
| mmpretrain | 1.2.0 |
| numpy | 1.26.4 |
| opencv-python-headless | 4.10.0.84 |

## 使用方法

如果你是 Claude 等支持Skill的用户，可将此 skill 添加至你的个人或项目 skills 目录中。

如果你只是需要一份纯文本的配置指南，可以直接查看下方的“完整安装步骤”部分。

加载该 Skill 后，你可以提问：

- “帮我配置 VMamba 的运行环境。”
- “编译 selective_scan 时报 unsupported GNU version 怎么办？”
- “VMamba 稳定可用的 PyTorch 和 MMCV 版本组合是什么？”

你的AI将根据内置的指南给出准确的、经过实际验证的解决方案。

## 完整安装步骤（可直接复制执行）

```bash
# 1. 创建并激活 conda 环境
conda create -n vmamba python=3.10 -y
conda activate vmamba

# 2. 安装 PyTorch 2.1.0 + CUDA 11.8
conda install pytorch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 pytorch-cuda=11.8 -c pytorch -c nvidia -y

# 3. 修复 MKL 符号错误 (iJIT_NotifyEvent)
conda install "mkl<2024.1" "intel-openmp<2024.1" -c conda-forge -y

# 4. 验证 PyTorch
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available()); print(torch.version.cuda)"

# 5. 安装 OpenMMLab 系列包
python -m pip install --upgrade pip
python -m pip install setuptools==81.0.0 wheel
python -m pip install -U openmim
mim install mmengine==0.10.1
mim install mmcv==2.1.0
python -m pip install mmsegmentation==1.2.2 mmdet==3.3.0 mmpretrain==1.2.0

# 6. 处理 NumPy 与 OpenCV 版本冲突
python -m pip install numpy==1.26.4
python -m pip uninstall -y opencv-python opencv-python-headless
python -m pip install --no-cache-dir opencv-python-headless==4.10.0.84

# 7. 编译 selective_scan (需提前安装 gcc-11 和 g++-11)
export CC=gcc-11
export CXX=g++-11
cd kernels/selective_scan
pip install . --no-build-isolation

# 8. 验证 selective_scan 导入
python -c "import torch; import selective_scan_cuda_oflex; print('selective_scan OK')"