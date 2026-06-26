# Ultralytics YOLO Environment Check Guide

This document provides comprehensive methods for checking your Ultralytics YOLO environment, helping you verify correct installation, proper environment configuration, and GPU/CUDA availability.

## 1. Quick Check (Recommended)

### Using Official `yolo checks` Command
This is the most comprehensive check method, outputting Python version, PyTorch, CUDA, GPU information, and all dependency library status.

```bash
yolo checks
```

**Expected Output Example:**
```
Ultralytics 8.4.21 🚀 Python-3.11.2 torch-2.10.0+cu128 CUDA:0 (NVIDIA GeForce RTX 3060, 6144MiB)
Setup complete ✅ (72 checks passed in 1.4s)

OS                     Linux-6.6.87.2-microsoft-standard-WSL2-x86_64-with-glibc2.35
Environment            Docker
Python                 3.11.2
Install                pip
Path                   /usr/local/lib/python3.11/site-packages/ultralytics
RAM                    31.2GB
Disk                   464.5GB
CPU                    Intel Xeon (4) @ 2.200GHz
CPU count              4
GPU                    NVIDIA GeForce RTX 3060 Laptop GPU
GPU count              1
CUDA                   12.8

numpy                  ✅ 2.4.3>=1.23.0
matplotlib             ✅ 3.10.8>=3.3.0
opencv-python          ✅ 4.13.0.92>=4.6.0
pillow                 ✅ 12.1.1>=7.1.2
pyyaml                 ✅ 6.0.3>=5.3.1
requests               ✅ 2.32.5>=2.23.0
scipy                  ✅ 1.14.1>=1.4.1
torch                  ✅ 2.10.0>=2.5.1
torchvision            ✅ 0.20.0>=0.20.1
...
```

**Key Information Interpretation:**
- First line: Shows YOLO version, Python version, PyTorch version, CUDA version, GPU model and memory
- `Setup complete`: Environment is ready
- Dependency status: ✅ indicates installed and version meets requirements

## 2. Basic Verification Methods

### 2.1 Python Import Test
Verify Ultralytics package can be imported and check version:

```bash
python -c "import ultralytics; print(f'Ultralytics version: {ultralytics.__version__}')"
```

**Output Example:**
```
Ultralytics version: 8.4.21
```

### 2.2 Package Information Check
View detailed information about installed ultralytics package:

```bash
pip show ultralytics
```

If multiple Python environments exist, use:

```bash
python -m pip show ultralytics
```

**Output includes:** Version number, installation path, dependencies, etc.

### 2.3 Package List Check
Check if ultralytics is installed among all packages:

```bash
pip list | grep -i ultralytics
```

**Or using conda (if applicable):**
```bash
conda list | grep -i ultralytics
```

## 3. CLI Tool Verification

### 3.1 Check if `yolo` Command is Available
```bash
yolo --help
```

**Expected Output:** Shows help information including available tasks (detect, segment, classify, pose, obb) and modes (train, val, predict, export, track, benchmark).

### 3.2 Test Simple Inference
Quick inference test using smallest pretrained model:

```bash
yolo predict model=yolo26n.pt source='https://ultralytics.com/images/bus.jpg' verbose=False
```

If environment is normal, it will download the model (first run) and output detection results.

## 4. GPU/CUDA Environment Verification

### 4.1 Check PyTorch CUDA Support
```bash
python -c "import torch; print(f'PyTorch version: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}'); print(f'GPU count: {torch.cuda.device_count()}'); [print(f'GPU {i}: {torch.cuda.get_device_name(i)}') for i in range(torch.cuda.device_count())]"
```

**Output Example:**
```
PyTorch version: 2.10.0+cu128
CUDA available: True
GPU count: 1
GPU 0: NVIDIA GeForce RTX 3060 Laptop GPU
```

### 4.2 Check CUDA Version Compatibility
```bash
python -c "import torch; print(f'CUDA version (PyTorch): {torch.version.cuda}'); print(f'CUDA runtime version: {torch.cuda.get_device_properties(0).major}.{torch.cuda.get_device_properties(0).minor}')"
```

### 4.3 Verify GPU Memory Availability
```bash
python -c "import torch; print(f'GPU memory total: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB'); print(f'GPU memory allocated: {torch.cuda.memory_allocated(0) / 1024**3:.2f} GB'); print(f'GPU memory cached: {torch.cuda.memory_reserved(0) / 1024**3:.2f} GB')"
```

## 5. Dependency Library Integrity Check

### 5.1 Key Dependency Version Verification
```bash
python -c "
import torch, torchvision, cv2, PIL, numpy, pandas
print(f'torch: {torch.__version__}')
print(f'torchvision: {torchvision.__version__}')
print(f'opencv-python: {cv2.__version__}')
print(f'Pillow: {PIL.__version__}')
print(f'numpy: {numpy.__version__}')
print(f'pandas: {pandas.__version__}')
"
```

### 5.2 Check Missing Dependencies
Minimum version requirements for Ultralytics:
- `torch>=2.5.1`
- `torchvision>=0.20.1`
- `opencv-python>=4.10.0`
- `pillow>=10.3.0`

Check if versions meet requirements:
```bash
pip list | grep -E "torch|torchvision|opencv-python|pillow"
```

## 6. Environment Issue Diagnosis

### 6.1 Common Problems and Solutions

**Problem: `yolo` command not found**
```
bash: yolo: command not found
```
**Solutions:**
1. Check Python environment: `which python` and `which pip`
2. Ensure ultralytics installed in current environment: `pip list | grep ultralytics`
3. Use full path: `python -m ultralytics yolo checks`
4. Check PATH environment variable includes Python scripts directory

**Problem: CUDA not available**
```
CUDA available: False
```
**Solutions:**
1. Confirm CUDA-compatible PyTorch installed: `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121`
2. Check NVIDIA driver: `nvidia-smi`
3. Verify CUDA toolkit installation: `nvcc --version`
4. Ensure PyTorch CUDA version compatible with system CUDA version

**Problem: Dependency version conflicts**
```
ImportError: cannot import name 'xxx' from 'ultralytics'
```
**Solutions:**
1. Upgrade to latest version: `pip install -U ultralytics`
2. Reinstall: `pip uninstall ultralytics -y && pip install ultralytics`
3. Check dependency compatibility: `pip check`

### 6.2 Complete Environment Report
Generate complete environment report for troubleshooting:

```bash
python -c "
import sys, platform, torch, ultralytics
print('='*60)
print('Ultralytics YOLO Environment Report')
print('='*60)
print(f'Python: {sys.version}')
print(f'Platform: {platform.platform()}')
print(f'Ultralytics: {ultralytics.__version__}')
print(f'PyTorch: {torch.__version__}')
print(f'CUDA available: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'GPU count: {torch.cuda.device_count()}')
    for i in range(torch.cuda.device_count()):
        print(f'  GPU {i}: {torch.cuda.get_device_name(i)}')
print('='*60)
"
```

## 7. Automated Check Scripts

### 7.1 Using Provided Check Script
Use the included Python script for comprehensive environment checking:

```bash
# Run the environment check script
python scripts/check_environment.py

# This script provides detailed information about:
# - Python environment
# - PyTorch configuration and CUDA availability
# - Ultralytics installation status
# - Key dependency versions
# - System resources (CPU, RAM, disk)
# - Generates JSON report for sharing
```

### 7.2 Simple Check Script
Save the following as `quick_check.py` for basic verification:

```python
#!/usr/bin/env python3
"""
Ultralytics YOLO Quick Environment Check
Run: python quick_check.py
"""

import sys
import platform
import subprocess

def run_command(cmd):
    """Execute command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip() if result.returncode == 0 else f"Error: {result.stderr.strip()}"
    except Exception as e:
        return f"Exception: {str(e)}"

def main():
    print("="*60)
    print("Ultralytics YOLO Quick Environment Check")
    print("="*60)
    
    # 1. System Information
    print("\n1. System Information:")
    print(f"   Python: {sys.version.split()[0]}")
    print(f"   Platform: {platform.platform()}")
    
    # 2. Ultralytics Check
    print("\n2. Ultralytics Check:")
    import_test = run_command('python -c "import ultralytics; print(\"OK\")"')
    version_test = run_command('python -c "import ultralytics; print(ultralytics.__version__)"')
    print(f"   Import test: {import_test}")
    print(f"   Version: {version_test}")
    
    # 3. PyTorch Check
    print("\n3. PyTorch Check:")
    torch_test = run_command('python -c "import torch; print(\"OK\")"')
    torch_version = run_command('python -c "import torch; print(torch.__version__)"')
    cuda_test = run_command('python -c "import torch; print(torch.cuda.is_available())"')
    print(f"   Import test: {torch_test}")
    print(f"   Version: {torch_version}")
    print(f"   CUDA available: {cuda_test}")
    
    # 4. yolo Command Check
    print("\n4. yolo Command Line Tool:")
    yolo_check = run_command('which yolo 2>/dev/null || echo "Not found"')
    print(f"   Command availability: {yolo_check}")
    
    print("\n" + "="*60)
    print("Check Complete!")
    print("="*60)

if __name__ == "__main__":
    main()
```

## 8. Performance Testing

### 8.1 Benchmark Inference Speed
Test inference speed with different models:

```bash
# Benchmark nano model
yolo benchmark model=yolo26n.pt imgsz=640 device=0

# Benchmark medium model
yolo benchmark model=yolo26m.pt imgsz=640 device=0

# Compare CPU vs GPU
yolo benchmark model=yolo26n.pt imgsz=640 device=cpu
yolo benchmark model=yolo26n.pt imgsz=640 device=0
```

### 8.2 Memory Usage Test
Check memory usage during inference:

```bash
# Monitor GPU memory during inference
yolo predict model=yolo26m.pt source='image.jpg' device=0
# Check memory usage with nvidia-smi in another terminal
```

## 9. YOLO Version Specific Checks

### 9.1 YOLO26 Specific Checks
YOLO26 introduces new features that may require specific checks:

```bash
# Check YOLO26 model loading
yolo predict model=yolo26n.pt source='image.jpg'

# Test NMS-free inference (YOLO26 feature)
yolo predict model=yolo26n.pt source='image.jpg' nms=False
```

### 9.2 Multi-Task Model Verification
Verify models support specific tasks:

```bash
# Detection model check
yolo detect predict model=yolo26n.pt source='image.jpg'

# Segmentation model check
yolo segment predict model=yolo26n-seg.pt source='image.jpg'

# Pose model check
yolo pose predict model=yolo26n-pose.pt source='image.jpg'

# Classification model check
yolo classify predict model=yolo26n-cls.pt source='image.jpg'

# OBB model check
yolo obb predict model=yolo26n-obb.pt source='image.jpg'
```

## 10. Network and Download Checks

### 10.1 Model Download Test
Test model downloading capability:

```bash
# Test model download (will cache if not already downloaded)
yolo predict model=yolo26n.pt source='https://ultralytics.com/images/bus.jpg' verbose=False

# Check cache location
python -c "from ultralytics import YOLO; import os; print(f'Model cache: {os.path.expanduser(\"~/.cache/ultralytics\")}')"
```

### 10.2 Internet Connectivity Check
```bash
# Test connection to Ultralytics servers
curl -I https://ultralytics.com/images/bus.jpg

# Test GitHub API (for source installation)
curl -I https://api.github.com/repos/ultralytics/ultralytics
```

## Summary

Regular environment checks ensure stable YOLO task execution. Recommended to use `yolo checks` for comprehensive checking, and refer to targeted verification methods in this document when issues arise.

**Check Priority:**
1. ✅ `yolo checks` - Comprehensive check
2. ✅ Python import test - Basic verification
3. ✅ GPU/CUDA verification - Performance related
4. ✅ Dependency version check - Compatibility verification

**Additional Tools:**
- Use `scripts/check_environment.py` for detailed diagnostics
- Run `yolo benchmark` for performance testing
- Monitor with `nvidia-smi` for GPU utilization

**Tip:** After environment check passes, proceed with YOLO tasks like inference, training, etc. Refer to [Installation Guide](./installation_guide.md) for installation help and [Task Types](./task_types.md) for understanding YOLO capabilities.

## Utility Scripts

For comprehensive environment checking, use the `check_environment.py` script:

```bash
# Run comprehensive environment check
python scripts/check_environment.py

# This script provides:
# - Detailed Python environment information
# - PyTorch and CUDA configuration check
# - Ultralytics installation verification
# - Key dependency version validation
# - System resource analysis (CPU, RAM, disk)
# - JSON report generation for sharing
```

**Script Location**: `scripts/check_environment.py`

**Additional testing scripts**:
- `scripts/quick_tests.py` - Quick functionality tests
- `scripts/model_utils.py` - Model validation utilities

**Benefits of using scripts**:
- Save tokens by extracting code from documentation
- Consistent and comprehensive checking
- JSON report generation for troubleshooting
- Ready-to-use, no need to copy-paste commands