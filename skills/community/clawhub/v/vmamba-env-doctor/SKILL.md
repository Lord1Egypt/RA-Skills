---
name: vmamba-env-doctor
description: Guide for setting up a stable VMamba environment and resolving common CUDA, PyTorch, MMCV, and compilation errors. Use when users encounter issues like "unsupported GNU version", "libc10.so not found", "No module named 'torch' during pip install", or NumPy/OpenCV version conflicts.
---

# VMamba Environment Doctor

This skill provides a step-by-step guide to set up a **stable, verified environment** for [VMamba](https://github.com/MzeroMiko/VMamba), along with solutions to the most common setup errors.

## When to Use This Skill

- User asks for help installing VMamba or its dependencies (`mmcv`, `mmsegmentation`, `selective_scan`).
- User reports a compilation error with `nvcc` or `gcc`.
- User sees `ImportError: libc10.so: cannot open shared object file`.
- User encounters `ModuleNotFoundError: No module named 'torch'` when running `pip install .`.
- User faces conflicts between NumPy 2.x and OpenCV or PyTorch.

## Verified Stable Environment

Use the following combination to avoid most compatibility issues:

- **Python**: 3.10
- **PyTorch**: 2.1.0
- **CUDA**: 11.8
- **gcc/g++**: 11
- **mmengine**: 0.10.1
- **mmcv**: 2.1.0
- **mmsegmentation**: 1.2.2
- **mmdet**: 3.3.0
- **mmpretrain**: 1.2.0
- **numpy**: 1.26.4
- **opencv-python-headless**: 4.10.0.84

## Step-by-Step Setup Instructions

Provide these commands to the user to create a clean environment:

```bash
# 1. Create and activate conda environment
conda create -n vmamba python=3.10 -y
conda activate vmamba

# 2. Install PyTorch 2.1.0 with CUDA 11.8
conda install pytorch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 pytorch-cuda=11.8 -c pytorch -c nvidia -y

# 3. Fix MKL symbol error (iJIT_NotifyEvent)
conda install "mkl<2024.1" "intel-openmp<2024.1" -c conda-forge -y

# 4. Verify PyTorch installation
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available()); print(torch.version.cuda)"

# 5. Install OpenMMLab packages
python -m pip install --upgrade pip
python -m pip install setuptools==81.0.0 wheel
python -m pip install -U openmim
mim install mmengine==0.10.1
mim install mmcv==2.1.0
python -m pip install mmsegmentation==1.2.2 mmdet==3.3.0 mmpretrain==1.2.0

# 6. Fix NumPy and OpenCV compatibility
python -m pip install numpy==1.26.4
python -m pip uninstall -y opencv-python opencv-python-headless
python -m pip install --no-cache-dir opencv-python-headless==4.10.0.84

# 7. Compile selective_scan with gcc-11
# (Ensure gcc-11 and g++-11 are installed: sudo apt install gcc-11 g++-11)
export CC=gcc-11
export CXX=g++-11
cd kernels/selective_scan
pip install . --no-build-isolation

# 8. Verify selective_scan import
python -c "import torch; import selective_scan_cuda_oflex; print('selective_scan OK')"