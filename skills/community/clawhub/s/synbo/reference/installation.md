# Installation Guide

## Step 1: Check and Install Miniconda

First, check if conda is already installed:

```bash
conda --version
```

**If conda is NOT installed**, install Miniconda using Tsinghua mirror (for China):

```bash
# Download Miniconda installer
cd /tmp
curl -fsSL https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-latest-MacOSX-arm64.sh -o miniconda.sh

# Run installer (silent mode, for macOS arm64)
bash miniconda.sh -b -p $HOME/miniconda3

# Initialize conda for your shell
$HOME/miniconda3/bin/conda init zsh

# Restart shell or run:
source ~/.zshrc

# Verify installation
conda --version
```

**For Linux (x86_64):**
```bash
curl -fsSL https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-latest-Linux-x86_64.sh -o miniconda.sh
bash miniconda.sh -b -p $HOME/miniconda3
$HOME/miniconda3/bin/conda init bash
source ~/.bashrc
```

**For Linux (arm64):**
```bash
curl -fsSL https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-latest-Linux-aarch64.sh -o miniconda.sh
bash miniconda.sh -b -p $HOME/miniconda3
$HOME/miniconda3/bin/conda init bash
source ~/.bashrc
```

## Step 2: Create synbo_env Environment

```bash
# Create new environment with Python 3.12
conda create -n synbo_env python=3.13 -y

# Activate the environment
conda activate synbo_env
```

## Step 3: Install Required Packages

**Important:** Install `qspoc` first, then `synbo` (dependency order matters):

```bash
# Make sure you're in synbo_env
conda activate synbo_env

# Install qspoc first (required dependency)
pip install qspoc

# Then install synbo
pip install synbo
```

## Step 4: Verify Installation

```bash
conda activate synbo_env
python -c "from synbo import ReactionOptimizer; print('synbo installed successfully!')"