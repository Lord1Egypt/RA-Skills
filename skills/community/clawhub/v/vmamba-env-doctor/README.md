# VMamba Environment Setup Assistant Skill

This is a Skill designed to help users set up a **stable and verified Python environment** for the [VMamba](https://github.com/MzeroMiko/VMamba) project, and quickly resolve common installation and compilation errors.

## What This Skill Covers

- Installing correct versions of PyTorch, CUDA, MMCV, and other dependencies.
- Compiling the `selective_scan` CUDA kernel without errors.
- Resolving the following common issues:
  - `ModuleNotFoundError: No module named 'torch'` (caused by build isolation)
  - `unsupported GNU version` (gcc version too high)
  - `libc10.so: cannot open shared object file` (missing dynamic library path)
  - `undefined symbol: iJIT_NotifyEvent` (MKL version conflict)
  - Compatibility conflicts between NumPy 2.x and OpenCV

## Stable Environment Combination

| Component | Recommended Version |
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

## Usage

If you are a user of Claude or other services that support Skills,you can add this skill to your personal or project skills folder.

If you only need a plain-text setup guide, you can directly refer to the "Complete Installation Steps" section below.

Once this skill is loaded, you can ask questions like:

- "Help me configure the runtime environment for VMamba."
- "I get 'unsupported GNU version' when compiling selective_scan. What should I do?"
- "What is the stable version combination of PyTorch and MMCV for VMamba?"

Your AI will provide accurate and practically verified solutions based on the built-in guide.

## Complete Installation Steps (Copy & Execute)

```bash
# 1. Create and activate conda environment
conda create -n vmamba python=3.10 -y
conda activate vmamba

# 2. Install PyTorch 2.1.0 + CUDA 11.8
conda install pytorch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 pytorch-cuda=11.8 -c pytorch -c nvidia -y

# 3. Fix MKL symbol error (iJIT_NotifyEvent)
conda install "mkl<2024.1" "intel-openmp<2024.1" -c conda-forge -y

# 4. Verify PyTorch
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available()); print(torch.version.cuda)"

# 5. Install OpenMMLab packages
python -m pip install --upgrade pip
python -m pip install setuptools==81.0.0 wheel
python -m pip install -U openmim
mim install mmengine==0.10.1
mim install mmcv==2.1.0
python -m pip install mmsegmentation==1.2.2 mmdet==3.3.0 mmpretrain==1.2.0

# 6. Handle NumPy and OpenCV version conflicts
python -m pip install numpy==1.26.4
python -m pip uninstall -y opencv-python opencv-python-headless
python -m pip install --no-cache-dir opencv-python-headless==4.10.0.84

# 7. Compile selective_scan (requires pre-installed gcc-11 and g++-11)
export CC=gcc-11
export CXX=g++-11
cd kernels/selective_scan
pip install . --no-build-isolation

# 8. Verify selective_scan import
python -c "import torch; import selective_scan_cuda_oflex; print('selective_scan OK')"