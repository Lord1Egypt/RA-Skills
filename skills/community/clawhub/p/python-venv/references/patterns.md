# Python Virtual Environment - Common Patterns

## User Choice Pattern (Before Creating venv)

Before creating a new virtual environment, always ask the user:

```
No existing virtual environment found. Choose an option:
1. Create new venv in current directory (.venv) [recommended]
2. Use system Python directly
3. Create venv at custom path
```

Then proceed based on their choice.

## Setup Methods

### uv (Recommended - Faster)

```bash
# Create virtual environment
uv venv

# Create at custom path
uv venv /path/to/my-venv

# Activate (Linux/macOS)
source .venv/bin/activate
source /path/to/my-venv/bin/activate

# Activate (Windows PowerShell)
.venv\Scripts\Activate.ps1
C:\path\to\venv\Scripts\Activate.ps1

# Activate (Windows CMD)
.venv\Scripts\activate.bat
C:\path\to\venv\Scripts\activate.bat

# Install packages
uv pip install <package>

# Install from file
uv pip install -r requirements.txt
uv pip install -e .
```

### Standard venv (Fallback if uv not installed)

```bash
# Create virtual environment
python3 -m venv .venv

# Create at custom path
python3 -m venv /path/to/my-venv

# Activate (Linux/macOS)
source .venv/bin/activate
source /path/to/my-venv/bin/activate

# Activate (Windows PowerShell)
.venv\Scripts\Activate.ps1
C:\path\to\venv\Scripts\Activate.ps1

# Activate (Windows CMD)
.venv\Scripts\activate.bat
C:\path\to\venv\Scripts\activate.bat

# Install packages
pip install <package>

# Install from file
pip install -r requirements.txt
pip install -e .
```

### Conda/Mamba

```bash
# Create environment
conda create -n myenv python=3.11

# Activate
conda activate myenv

# Install packages
conda install <package>
# or
pip install <package>
```

## Common Shell Patterns

### Standard Pattern (Linux/macOS) - Reuse or Create with Fallback

```bash
# Find existing venv or create new one (uv with fallback to venv)
if [ -d .venv ]; then
    source .venv/bin/activate
elif [ -d venv ]; then
    source venv/bin/activate
elif [ -d env ]; then
    source env/bin/activate
elif command -v uv &> /dev/null; then
    uv venv && source .venv/bin/activate
else
    python3 -m venv .venv && source .venv/bin/activate
fi
```

### One-liner (Linux/macOS)

```bash
# Quick version: check .venv, fallback to create
[ -d .venv ] && source .venv/bin/activate || { command -v uv &>/dev/null && uv venv || python3 -m venv .venv; source .venv/bin/activate; }
```

### Windows PowerShell

```powershell
# Find existing venv or create new one
if (Test-Path .venv) { .\.venv\Scripts\Activate.ps1 }
elseif (Test-Path venv) { .\venv\Scripts\Activate.ps1 }
else {
    # Ask user for choice if auto-creation is not desired
    # If creating new venv at default path:
    if (Get-Command uv -ErrorAction SilentlyContinue) { uv venv; .\.venv\Scripts\Activate.ps1 }
    else { python -m venv .venv; .\.venv\Scripts\Activate.ps1 }
}
```

## Running a Python Script

```bash
# Activate existing or create new
[ -d .venv ] && source .venv/bin/activate || { command -v uv &>/dev/null && uv venv || python3 -m venv .venv; source .venv/bin/activate; }

# Install dependencies (check both requirements.txt and pyproject.toml)
[ -f requirements.txt ] && pip install -r requirements.txt
[ -f pyproject.toml ] && pip install -e .

# Run script
python script.py
```

## Verification

### Check if venv is Active

```bash
# Should show path containing .venv, venv, or env
which python

# Or check VIRTUAL_ENV environment variable
echo $VIRTUAL_ENV
```

### Check if Conda Environment is Active

```bash
# Check CONDA_PREFIX
echo $CONDA_PREFIX

# List all conda environments
conda info --envs
```

## Forbidden Actions

- Using `pip install` with system Python (always use venv)
- Installing packages globally
- Assuming third-party packages are available without explicit installation
- Overwriting existing virtual environment without checking first

## Allowed Without venv

- `python3 -c "print('hello')"`
- `python3 -c "import os; print(os.getcwd())"`
- `python3 --version`
- Any stdlib-only one-liner
