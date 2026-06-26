# API Calling Environment Setup

EdgeOne APIs are called via **tccli** (Tencent Cloud CLI).

## 1. Choose an Installation Method

| Method | Use Case | Prerequisites |
|---|---|---|
| **pipx** | All platforms, auto-isolated environment | Python 3.8+ |
| **Homebrew** | macOS | No Python required |

- macOS with Homebrew already installed → go directly with the Homebrew route, skip to Step 4
- Otherwise → go with the pipx route, continue to Step 2

## 2. Ensure Python Environment (pipx Route)

```sh
python3 --version
```

If the version is ≥ 3.8, skip to the next step. If the command is not found or the version is too old, install by OS:

```sh
# macOS (via Homebrew)
brew install python@3

# Ubuntu / Debian
apt update && apt install -y python3 python3-pip

# Windows (via winget)
winget install Python.Python.3.12
# Or download from: https://www.python.org/downloads/
```

After installation, run `python3 --version` to confirm version ≥ 3.8.

## 3. Install pipx (pipx Route)

```sh
pipx --version
```

If already installed, skip to the next step; otherwise install by OS:

```sh
# macOS
brew install pipx && pipx ensurepath

# Linux
pip install --user pipx && pipx ensurepath

# Windows
pip install --user pipx && pipx ensurepath
```

## 4. Install tccli

### pipx Route

```sh
pipx install tccli

# If upgrading from a version below 3.0.252.3, uninstall first then reinstall:
# pipx uninstall tccli && pipx install tccli
```

### Homebrew Route (macOS Only)

```sh
brew tap tencentcloud/tccli
brew install tccli
# Update: brew upgrade tccli
```

### Verify

```sh
tccli --version
```

## Update tccli

Update to the latest tccli build:

```sh
# pipx route
pipx upgrade tccli
# or, if upgrade doesn't pick up the new build:
pipx uninstall tccli && pipx install tccli

# Homebrew route (macOS)
brew upgrade tccli
```

## Next Step

After installation is complete, read `auth.md` to configure credentials.
