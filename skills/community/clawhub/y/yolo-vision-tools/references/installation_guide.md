# Ultralytics YOLO Installation Guide

This guide provides comprehensive installation methods for Ultralytics YOLO, covering various environments and deployment options.

**Latest Version**: YOLO26 (released January 2026) with end-to-end NMS-free inference. For stable production workloads, both YOLO26 and YOLO11 are recommended.

## System Requirements

### 🎯 Minimum Requirements (Must Meet)

| Component | Minimum Requirement | Notes |
|-----------|---------------------|-------|
| **Python** | **3.8+** | Officially supports Python 3.8, 3.9, 3.10, 3.11, 3.12 |
| **PyTorch** | **1.8.0+** | Windows users: Avoid torch 2.4.0 (known CPU bug) |
| **Operating System** | **Linux, Windows, macOS** | Cross-platform support |

> ⚠️ **Important**: Installing `ultralytics` automatically installs all required dependencies. **Do not manually install libraries listed below**.

### 📦 Core Dependencies (Automatically Installed)
When running `pip install ultralytics`, these libraries are installed with minimum versions:

| Library | Minimum Version | Description |
|---------|-----------------|-------------|
| `torch` | 1.8.0+ | PyTorch deep learning framework |
| `torchvision` | 0.9.0+ | Computer vision datasets and models |
| `numpy` | 1.23.0+ | Numerical computing library |
| `matplotlib` | 3.3.0+ | Data visualization |
| `opencv-python` | 4.6.0+ | Computer vision library |
| `pillow` (PIL) | 7.1.2+ | Image processing library |
| `pyyaml` | 5.3.1+ | YAML configuration file handling |
| `requests` | 2.23.0+ | HTTP request library |
| `scipy` | 1.4.1+ | Scientific computing library |
| `psutil` | 5.8.0+ | System monitoring and process management |
| `polars` | 0.20.0+ | High-performance data manipulation |
| `ultralytics-thop` | 2.0.18+ | FLOPs computation tool |

### 🎪 Optional Features (Install as Needed)
For specific functionality, install extra dependencies:

```bash
# Development toolkit (code contributors)
pip install "ultralytics[dev]"

# Model export packages (ONNX, TensorFlow, CoreML, etc.)
pip install "ultralytics[export]"

# Solutions packages (Streamlit, Flask web applications)
pip install "ultralytics[solutions]"

# Logging packages (W&B, TensorBoard, MLflow)
pip install "ultralytics[logging]"

# Extra features (Albumentations augmentation, COCO evaluation)
pip install "ultralytics[extra]"
```

### ⚡ GPU Acceleration (Optional)
For GPU acceleration, ensure:
1. NVIDIA GPU with CUDA support
2. Matching NVIDIA drivers installed
3. Recommended CUDA 12.1+ version

### 🚀 Quick Verification
After installation, verify your environment:

```bash
# Check version
python -c "import ultralytics; print(f'Ultralytics version: {ultralytics.__version__}')"

# Simple test
yolo predict model=yolo26n.pt source='https://ultralytics.com/images/bus.jpg'
```

## Installation Methods

### 1. Basic Installation (Recommended)

Using pip is the simplest and fastest method:

```bash
# Install latest version
pip install ultralytics

# Or install specific version
pip install ultralytics==8.4.0

# Upgrade to latest version
pip install -U ultralytics
```

### 2. Install from Source (Development Version)

If you need the latest development features or want to modify source code:

```bash
# Clone repository
git clone https://github.com/ultralytics/ultralytics.git
cd ultralytics

# Install in editable mode (development environment)
pip install -e .

# Or install directly from GitHub
pip install git+https://github.com/ultralytics/ultralytics.git

# Install from specific branch
pip install git+https://github.com/ultralytics/ultralytics.git@main
```

### 3. Conda Installation (Anaconda/Miniconda)

```bash
# Create new environment (optional)
conda create -n yolo python=3.10
conda activate yolo

# Install via conda-forge
conda install -c conda-forge ultralytics

# Or install PyTorch first, then ultralytics
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
pip install ultralytics

# Install all packages together (CUDA environment)
conda install -c pytorch -c nvidia -c conda-forge pytorch torchvision pytorch-cuda=11.8 ultralytics
```

### 4. Docker Installation (Containerized Deployment)

```bash
# Pull official image
docker pull ultralytics/ultralytics:latest

# Run container with GPU support
docker run -it --ipc=host --runtime=nvidia --gpus all ultralytics/ultralytics:latest

# Mount local directory and run
docker run -it --rm --gpus all -v $(pwd):/workspace ultralytics/ultralytics:latest

# Specify GPU devices
docker run -it --ipc=host --runtime=nvidia --gpus '"device=2,3"' ultralytics/ultralytics:latest
```

Available Docker images:
- `ultralytics/ultralytics:latest` - GPU image recommended for training
- `ultralytics/ultralytics:latest-cpu` - CPU-only version for inference
- `ultralytics/ultralytics:latest-arm64` - Optimized for ARM64 (Raspberry Pi)
- `ultralytics/ultralytics:latest-jetson` - Tailored for NVIDIA Jetson devices
- `ultralytics/ultralytics:latest-conda` - Miniconda3-based image

For more Docker options, refer to [Ultralytics Docker Guide](https://docs.ultralytics.com/guides/docker-quickstart/).

### 5. Headless Server Installation

For server environments without display (cloud VMs, Docker containers, CI/CD pipelines):

```bash
# Use headless variant (no GUI dependencies)
pip install ultralytics-opencv-headless

# Both packages provide same functionality and API
# The headless variant excludes OpenCV GUI components
```

## GPU Support Configuration

### CUDA Environment Setup (NVIDIA GPU)

```bash
# Method 1: Use official recommended command (auto-match CUDA version)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install ultralytics

# Method 2: Specify CUDA version
# CUDA 11.8
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# CUDA 12.1
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# CUDA 12.4
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

# Check CUDA availability after installation
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'GPU count: {torch.cuda.device_count()}')"
```

### CPU-only Installation

```bash
# CPU-only version
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install ultralytics

# Or install CPU PyTorch via conda
conda install pytorch torchvision torchaudio cpuonly -c pytorch
```

## Advanced Installation Methods

### Install from Fork

```bash
# Fork the Ultralytics repository on GitHub
# Clone your fork
git clone https://github.com/YOUR_USERNAME/ultralytics.git
cd ultralytics

# Create branch for changes
git checkout -b my-custom-branch

# Make modifications to pyproject.toml or other files
# Install from your branch
pip install git+https://github.com/YOUR_USERNAME/ultralytics.git@my-custom-branch
```

### Local Clone and Install

```bash
# Clone repository
git clone https://github.com/ultralytics/ultralytics
cd ultralytics

# Make modifications
# Install in editable mode
pip install -e .
```

### Using requirements.txt

```bash
# requirements.txt
git+https://github.com/YOUR_USERNAME/ultralytics.git@my-custom-branch
flask
# Other project dependencies

# Install dependencies
pip install -r requirements.txt
```

## Installation Verification

After installation, verify it was successful:

```python
import ultralytics
print(f"Ultralytics version: {ultralytics.__version__}")

# Simple test
from ultralytics import YOLO

# Load pretrained model
model = YOLO('yolo26n.pt')

# Quick inference test
results = model('https://ultralytics.com/images/bus.jpg')
print(f"Detected {len(results[0].boxes)} objects")
```

Command line verification:

```bash
# Show version information
yolo version

# Run quick test
yolo predict model=yolo26n.pt source='https://ultralytics.com/images/bus.jpg'

# Comprehensive environment check
yolo checks
```

## Troubleshooting

### Common Issues

1. **ImportError: libcudart.so.xx.x: cannot open shared object file**
   - Ensure CUDA is correctly installed and version matches
   - Check LD_LIBRARY_PATH environment variable
   - Verify NVIDIA drivers are up to date

2. **PyTorch Version Incompatibility**
   ```bash
   # Reinstall matching PyTorch version
   pip uninstall torch torchvision torchaudio
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
   ```

3. **Slow Installation or Timeout**
   ```bash
   # Use mirror source (China)
   pip install ultralytics -i https://pypi.tuna.tsinghua.edu.cn/simple
   
   # Use mirror source (global)
   pip install ultralytics -i https://pypi.org/simple
   ```

4. **`yolo` Command Not Found**
   ```bash
   # Use Python module syntax
   python -m ultralytics yolo version
   
   # Or check Python environment PATH
   which python
   pip show ultralytics
   ```

5. **Memory Issues with Model Download**
   ```bash
   # Set cache directory
   export ULTRALYTICS_HOME=/path/to/cache
   
   # Or download model manually
   wget https://github.com/ultralytics/assets/releases/download/v8.2.0/yolo26n.pt
   ```

### Environment Check Script

Use the included environment check script:

```bash
# Run comprehensive environment check
python scripts/check_environment.py

# Or use built-in check
yolo checks
```

## Maintenance and Updates

```bash
# Upgrade all packages
pip install --upgrade torch torchvision torchaudio ultralytics

# Clean cache
pip cache purge

# List installed packages
pip list | grep -E "(torch|ultralytics)"

# Check for updates
pip list --outdated | grep ultralytics

# Reinstall clean
pip uninstall ultralytics -y
pip install ultralytics
```

## Platform-Specific Notes

### Windows
- Recommended: Use Python 3.10 or 3.11
- Avoid PyTorch 2.4.0 (known CPU bug)
- Use Windows Subsystem for Linux (WSL2) for better compatibility

### macOS
- M1/M2/M3 Apple Silicon: Use PyTorch nightly builds for optimal performance
- Intel Macs: CPU-only operation

### Linux
- Most compatible platform
- Use system package manager for dependencies (apt, yum, dnf)

### ARM64 (Raspberry Pi, Jetson)
- Use ARM64-specific Docker images
- Consider model quantization for better performance
- Use smaller models (nano, small) for real-time inference

## Official Documentation Links

- **Main Documentation**: https://docs.ultralytics.com/
- **Quickstart Guide**: https://docs.ultralytics.com/quickstart/
- **Installation Guide**: https://docs.ultralytics.com/guides/installation/
- **GitHub Repository**: https://github.com/ultralytics/ultralytics
- **Docker Hub**: https://hub.docker.com/r/ultralytics/ultralytics
- **PyTorch Installation**: https://pytorch.org/get-started/locally/
- **Models Documentation**: https://docs.ultralytics.com/models/
- **Tasks Documentation**: https://docs.ultralytics.com/tasks/

## Next Steps

After successful installation:
1. Run `yolo checks` to verify environment
2. Explore [Task Types](./task_types.md) to understand YOLO capabilities
3. Check [Model Selection](./model_selection.md) to choose appropriate models
4. Review [Configuration Samples](./configuration_samples.md) for parameter tuning
5. Try examples from [Quick Start](../SKILL.md#quick-start)

## Utility Scripts for Verification

For comprehensive environment verification, use the provided scripts:

```bash
# Quick environment check
python scripts/check_environment.py

# Quick functionality tests
python scripts/quick_tests.py --test environment

# Test basic inference
python scripts/quick_tests.py --test inference
```

**Available scripts in `scripts/` directory**:
- `check_environment.py` - Comprehensive environment diagnostics
- `quick_tests.py` - Quick functionality tests
- `config_templates.py` - Configuration templates
- `dataset_tools.py` - Dataset preparation tools
- `training_helpers.py` - Training utilities
- `model_utils.py` - Model selection utilities

**Benefits**:
- Save tokens by extracting code from documentation
- Ready-to-use tools for common tasks
- Consistent API and error handling
- Modular design, import only what you need