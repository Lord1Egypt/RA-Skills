# How to Install Conda (through Miniconda)

## Linux / macOS (bash)

```bash
# Detect architecture and download appropriate Miniconda installer
ARCH=$(uname -m)
OS=$(uname -s)

if [ "$OS" = "Linux" ]; then
    if [ "$ARCH" = "x86_64" ]; then
        MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
    elif [ "$ARCH" = "aarch64" ]; then
        MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh"
    else
        echo "Unsupported Linux architecture: $ARCH"
        exit 1
    fi
elif [ "$OS" = "Darwin" ]; then
    if [ "$ARCH" = "x86_64" ]; then
        MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh"
    elif [ "$ARCH" = "arm64" ]; then
        MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh"
    else
        echo "Unsupported macOS architecture: $ARCH"
        exit 1
    fi
else
    echo "Unsupported OS: $OS"
    exit 1
fi

# Download installer (prefer wget, fallback to curl)
if command -v wget > /dev/null; then
    wget "$MINICONDA_URL" -O ~/miniconda.sh
elif command -v curl > /dev/null; then
    curl -L "$MINICONDA_URL" -o ~/miniconda.sh
else
    echo "Neither wget nor curl found. Please install one."
    exit 1
fi

# Silent install to $HOME/miniconda
bash ~/miniconda.sh -b -p $HOME/miniconda

# Initialize conda (adds conda to PATH and enables `conda activate`)
# NOTE: YOU MUST RESTART YOUR TERMINAL after this step
~/miniconda/bin/conda init

# Alternative to restarting: Reload shell configuration
if [ -f ~/.bashrc ]; then source ~/.bashrc; fi
if [ -f ~/.zshrc ]; then source ~/.zshrc; fi

# Verify installation
conda --version
```

## Windows (PowerShell, run as normal user)

```powershell
# Download Miniconda installer
$url = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe"
$installer = "$env:TEMP\miniconda.exe"
Invoke-WebRequest -Uri $url -OutFile $installer

# Silent install for current user (no admin required)
# Note: /D defines the custom installation path and MUST be the last argument
Start-Process -Wait -FilePath $installer -ArgumentList "/InstallationType=JustMe /RegisterPython=0 /S /D=$env:USERPROFILE\miniconda3"

# Remove installer
Remove-Item $installer

# Initialize conda (adds to PATH and enables conda in PowerShell)
& "$env:USERPROFILE\miniconda3\Scripts\conda.exe" init powershell

# RESTART POWERSHELL to apply changes, then verify:
# conda --version
```

## Post-installation: Create an environment

```bash
# Create a new environment with a specific Python version
conda create -n myenv python=3.10 -y

# IMPORTANT: You may need to run `conda activate myenv` 
# If `conda activate` fails, use `source activate myenv` or restart your shell.
conda activate myenv

# Verify Python version
python --version
```

## Notes

- The `-b` flag in the bash installer runs silently (batch mode), accepting the license.
- `-p $HOME/miniconda` sets the installation path.
- `conda init` modifies your shell configuration file (`.bashrc`, `.zshrc`, or PowerShell profile). You **must** restart your terminal or manually source the file for changes to take effect.
- To update conda itself after installation: `conda update -n base conda -y`

## Troubleshooting

- **Conda command not found:** Ensure you restarted your terminal. If it still fails, check if the installation path was correctly added to your `~/.bashrc` or your system PATH.
- **Permission Denied:** Ensure you have write permissions to `$HOME`. No `sudo` is required for this installation method.
- **SSL/Network Errors:** If you are in a restricted network, consider using a mirror or checking proxy settings.
