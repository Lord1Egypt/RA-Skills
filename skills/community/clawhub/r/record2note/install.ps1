$ErrorActionPreference = "Stop"

# Install to %APPDATA%\record2note\
# If your agent uses a custom skill directory,
# copy the files there after installation.

$SkillName = "record2note"
$SrcDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$InstallDir = "$env:APPDATA\$SkillName"

Write-Host "=== Installing $SkillName skill ==="

# Create install directory
New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null

# Copy files (excluding config.json, which is user-specific)
Copy-Item -Path "$SrcDir\SKILL.md" -Destination "$InstallDir\" -Force
Copy-Item -Path "$SrcDir\config.example.json" -Destination "$InstallDir\" -Force
Copy-Item -Path "$SrcDir\scripts" -Destination "$InstallDir\" -Recurse -Force
Copy-Item -Path "$SrcDir\templates" -Destination "$InstallDir\" -Recurse -Force

# Copy .gitignore if it exists
if (Test-Path "$SrcDir\.gitignore") {
    Copy-Item -Path "$SrcDir\.gitignore" -Destination "$InstallDir\" -Force
}

Write-Host ""
Write-Host "=== Install complete ==="
Write-Host "Skill installed to: $InstallDir"
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Tell your AI Agent: 'Use record2note'"
Write-Host "2. Agent will guide you through setup"
