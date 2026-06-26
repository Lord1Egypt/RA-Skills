# WSL-PowerShell Controller

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![WSL](https://img.shields.io/badge/WSL-2-blue)](https://docs.microsoft.com/en-us/windows/wsl/)
[![PowerShell](https://img.shields.io/badge/PowerShell-5.1%2B-blue)](https://github.com/PowerShell/PowerShell)
[![GitHub stars](https://img.shields.io/github/stars/TYzzt/wsl-powershell)](https://github.com/TYzzt/wsl-powershell)

Call Windows PowerShell from WSL (Windows Subsystem for Linux) to control Windows from Linux environment.

## 🎯 Features

- ✅ Support Windows PowerShell and PowerShell Core
- ✅ Automatic path conversion (WSL ↔ Windows)
- ✅ Error handling and debug mode
- ✅ Command and script file execution modes
- ✅ Comprehensive help and version info
- ✅ Colored log output

## 📦 Installation

### Method 1: Manual Install (Recommended for Agents)

```bash
# Clone to OpenClaw workspace skills directory
cd ~/.openclaw/workspace/skills
git clone https://github.com/TYzzt/wsl-powershell.git

# Add execute permission
chmod +x wsl-powershell/scripts/psctl.sh
```

**For Agents**: Restart OpenClaw session after cloning, skill will auto-load.

### Method 2: Using ClawHub CLI

```bash
# Install ClawHub CLI
npm install -g clawhub

# Login
clawhub login

# Install skill
clawhub install wsl-powershell
```

### Method 3: Direct Download

```bash
# Download ZIP
wget https://github.com/TYzzt/wsl-powershell/archive/refs/heads/main.zip
unzip main.zip -d ~/.openclaw/workspace/skills/
mv ~/.openclaw/workspace/skills/wsl-powershell-main ~/.openclaw/workspace/skills/wsl-powershell

# Add execute permission
chmod +x ~/.openclaw/workspace/skills/wsl-powershell/scripts/psctl.sh
```

## 🔧 Basic Usage

```bash
# Execute PowerShell command
./scripts/psctl.sh "Get-Process | Select-Object -First 5 Name,Id"

# Execute PowerShell script file
./scripts/psctl.sh -f /mnt/c/scripts/myscript.ps1

# Check PowerShell availability
./scripts/psctl.sh --check
```

## 📖 Examples

### System Information

```bash
# Get system info
./scripts/psctl.sh "Get-ComputerInfo | Select-Object WindowsProductName,WindowsVersion"

# Get process list
./scripts/psctl.sh "Get-Process | Sort-Object CPU -Descending | Select-Object -First 10 Name,Id,CPU"

# Get service status
./scripts/psctl.sh "Get-Service | Where-Object {\$_.Status -eq 'Running'} | Select-Object -First 10 Name,DisplayName"
```

### File Operations

```bash
# List directory
./scripts/psctl.sh "Get-ChildItem C:\\Users"

# Copy file
./scripts/psctl.sh "Copy-Item C:\\source\\file.txt C:\\dest\\file.txt -Force"

# Create file
./scripts/psctl.sh "New-Item -Path C:\\test.txt -ItemType File -Force"
```

### Process Management

```bash
# Start program
./scripts/psctl.sh "Start-Process notepad.exe"

# Stop process
./scripts/psctl.sh "Stop-Process -Name notepad -Force"
```

### Network Operations

```bash
# Get network config
./scripts/psctl.sh "Get-NetIPConfiguration | Select-Object InterfaceAlias,IPv4Address"

# Ping test
./scripts/psctl.sh "Test-Connection -ComputerName google.com -Count 2"
```

## 🔧 Advanced Options

```bash
# Show help
./scripts/psctl.sh --help

# Show version
./scripts/psctl.sh --version

# Debug mode
DEBUG=1 ./scripts/psctl.sh "Get-Process"

# Verbose output
./scripts/psctl.sh -v "Get-Service"

# Use PowerShell Core
./scripts/psctl.sh -p "Get-Module -ListAvailable"

# Check PowerShell availability
./scripts/psctl.sh --check
```

## ⚠️ Notes

1. **Permissions**: Some operations require administrator privileges
   ```bash
   # Start elevated PowerShell
   ./scripts/psctl.sh "Start-Process powershell -Verb RunAs"
   ```

2. **Path Escaping**: Backslashes `\` in Windows paths must be escaped as `\\`

3. **Execution Policy**: Running scripts may require setting execution policy
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

4. **Encoding**: PowerShell outputs UTF-16 by default, may need conversion

## 🔒 Security Tips

- ⚠️ Use caution with system-level commands
- ⚠️ Avoid deleting critical system files
- ⚠️ Test commands before executing in production
- ⚠️ Do not execute scripts from untrusted sources

## 🤝 Contributing

Issues and Pull Requests are welcome!

1. Fork the project
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

Apache-2.0 License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [WSL](https://docs.microsoft.com/en-us/windows/wsl/) - Windows Subsystem for Linux
- [PowerShell](https://github.com/PowerShell/PowerShell) - PowerShell Core

## 🤖 Agent Integration

### Skill Loading Mechanism

OpenClaw automatically scans these directories for skills:

1. `~/.openclaw/workspace/skills/` - Main workspace skills
2. `./skills/` - Skills in current working directory

### Skill Activation

After installation, **restart OpenClaw session** and the skill will auto-load. Agents can:

1. **Call script directly**:
   ```bash
   ~/.openclaw/workspace/skills/wsl-powershell/scripts/psctl.sh "PowerShell command"
   ```

2. **Learn from skill description**:
   - Agent reads `SKILL.md` to understand skill capabilities
   - Automatically uses this skill based on user requests

3. **Example scenarios**:
   - "Check Windows Update policy"
   - "List Windows processes"
   - "Get system information"

## 📮 Project Links

- **Repository**: [github.com/TYzzt/wsl-powershell](https://github.com/TYzzt/wsl-powershell)
- **Clone**: `git clone https://github.com/TYzzt/wsl-powershell.git`
- **ClawHub**: `clawhub install wsl-powershell`
