# Python Virtual Environment - Troubleshooting

## Creating Virtual Environment at Custom Path

If user chooses custom path:

```bash
# With uv
uv venv /path/to/my-venv
source /path/to/my-venv/bin/activate

# With standard venv
python3 -m venv /path/to/my-venv
source /path/to/my-venv/bin/activate
```

Windows:

```powershell
# With uv
uv venv C:\path\to\venv
C:\path\to\venv\Scripts\Activate.ps1

# With standard venv
python -m venv C:\path\to\venv
C:\path\to\venv\Scripts\Activate.ps1
```

## Corrupted Virtual Environment

If venv is broken (import errors, missing packages after install):

```bash
# Remove and recreate
rm -rf .venv
uv venv && source .venv/bin/activate
# or
python3 -m venv .venv && source .venv/bin/activate
```

Windows (PowerShell):

```powershell
Remove-Item -Recurse -Force .venv
uv venv; .\.venv\Scripts\Activate.ps1
# or
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

## Wrong Python Version

```bash
# Specify Python version with uv
uv venv --python 3.11

# Or with standard venv
python3.11 -m venv .venv
```

Available Python versions:

```bash
# List available Python versions with uv
uv python list

# Find installed Python versions
which python3.11
ls /usr/bin/python*
```

## Permission Denied on Windows

Run PowerShell as Administrator, or:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## WSL (Windows Subsystem for Linux)

Use Linux commands in WSL:

```bash
# Same as Linux/macOS
source .venv/bin/activate

# Create venv
uv venv
# or
python3 -m venv .venv
```

**Important**: Don't mix Windows venv with WSL. Create separate venv for each environment.

## Common Issues

### Packages not found after activation

Check you're using the correct Python:

```bash
which python
echo $VIRTUAL_ENV
```

The path should contain your venv directory.

### Python version mismatch

Create venv with specific Python version:

```bash
# First verify Python is installed
python3.11 --version

# Then create venv
python3.11 -m venv .venv
# or with uv
uv venv --python 3.11
```

### uv not installed

Install uv:

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Then
uv venv
```

Fallback: Use standard venv instead.

### Activation not working on Windows

PowerShell execution policy may be blocking:

```powershell
# Check current policy
Get-ExecutionPolicy

# Allow script execution for current user
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Or use CMD instead:

```cmd
.venv\Scripts\activate.bat
```

### Virtual environment location issues

Keep `.venv` directory in:
- Project root (recommended)
- Custom path of user's choice

Avoid:
- System directories (/usr/local, C:\Windows)
- Network drives (slow)
- Paths with spaces or special characters

### Dependencies installation fails

Check project type and use appropriate command:

| File | Correct Command |
|------|-----------------|
| `requirements.txt` | `pip install -r requirements.txt` |
| `pyproject.toml` only | `pip install -e .` |
| `pyproject.toml` + `poetry.lock` | `poetry install` |
| `pyproject.toml` + `uv.lock` | `uv sync` |

Make sure to activate venv before installing.
