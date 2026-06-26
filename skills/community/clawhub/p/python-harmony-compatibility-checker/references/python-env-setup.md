# Python Environment Setup on HarmonyOS

Guide for setting up Python and managing packages on HarmonyOS (OpenHarmony).

## Python Installation

### Check Python Version

```bash
python3 --version
# or
python --version
```

### Recommended Python Version

- **Python 3.8+** - Minimum for most packages
- **Python 3.10+** - Recommended for best compatibility
- **Python 3.12** - Latest, may have package compatibility issues

## Virtual Environments

Always use virtual environments to avoid conflicts:

```bash
# Create virtual environment
python3 -m venv venv

# Activate (if supported)
source venv/bin/activate

# Or use directly
./venv/bin/python -m pip install <package>
```

## Package Management

### Install Packages

```bash
# Basic installation
python3 -m pip install <package>

# Install to specific directory
python3 -m pip install --target ./packages <package>

# Install from requirements
python3 -m pip install -r requirements.txt

# No cache (saves space)
python3 -m pip install --no-cache-dir <package>
```

### List Installed Packages

```bash
python3 -m pip list
python3 -m pip freeze > requirements.txt
```

### Uninstall Packages

```bash
python3 -m pip uninstall <package>
```

## Common Issues on HarmonyOS

### Permission Denied

HarmonyOS may restrict execution:

```bash
# Try with sudo (user can provide password)
sudo python3 -m pip install <package>

# Or install to user directory
python3 -m pip install --user <package>

# Or use --target
python3 -m pip install --target ./local_packages <package>
```

### Compilation Failures

Packages with C extensions may fail:

```bash
# Install build dependencies first
# (if available on your HarmonyOS version)

# Or use pre-built wheels
python3 -m pip install --only-binary=:all: <package>

# Or find alternative pure-Python packages
```

### Network Issues

If PyPI is slow or blocked:

```bash
# Use mirror
python3 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple <package>

# Or configure permanently
echo "[global]" >> ~/.pip/pip.conf
echo "index-url = https://pypi.tuna.tsinghua.edu.cn/simple" >> ~/.pip/pip.conf
```

## Environment Variables

Set these for better compatibility:

```bash
# Disable cache to save space
export PIP_NO_CACHE_DIR=1

# Use specific Python
export PYTHON=/usr/bin/python3

# Set installation target
export PIP_TARGET=./packages
```

## Testing Setup

For running tests on HarmonyOS:

```bash
# Install pytest
python3 -m pip install pytest

# Run tests
python3 -m pytest <test_file>

# Run with coverage
python3 -m pip install coverage
python3 -m coverage run -m pytest
python3 -m coverage report
```

## Troubleshooting

### "No module named pip"

```bash
# Install pip
python3 -m ensurepip --upgrade
# or
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

### "SSL Certificate Error"

```bash
# Update certificates
python3 -m pip install --upgrade certifi

# Or use trusted host
python3 -m pip install --trusted-host pypi.org <package>
```

### "Wheel not found"

```bash
# Install wheel
python3 -m pip install wheel

# Or build from source
python3 -m pip install --no-binary <package>
```

## Best Practices

1. **Use virtual environments** - Isolate dependencies
2. **Pin versions** - Use requirements.txt with exact versions
3. **Test compatibility** - Run the compatibility checker before deployment
4. **Document issues** - Note any workarounds for your setup
5. **Keep backups** - Export working configurations

## Example Setup Script

```bash
#!/bin/bash
# setup_python_harmony.sh

# Create project directory
mkdir -p myproject
cd myproject

# Create virtual environment
python3 -m venv venv

# Activate and upgrade pip
./venv/bin/python -m pip install --upgrade pip

# Install packages
./venv/bin/python -m pip install -r requirements.txt

# Run compatibility check
./venv/bin/python ../skills/python-harmony-compatibility-checker/scripts/check_compatibility.py -r requirements.txt
```

## Resources

- [OpenHarmony Python SIG](https://gitee.com/openharmony-sig/python)
- [Python for OpenHarmony](https://gitee.com/openharmony-china/python)
- [PyPI](https://pypi.org)
- [HarmonyOS Developer](https://developer.harmonyos.com)
