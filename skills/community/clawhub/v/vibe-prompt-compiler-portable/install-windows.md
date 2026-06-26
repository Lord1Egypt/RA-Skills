# Windows Install

If your publishing target rejects `.ps1` files, use this markdown copy instead.

## PowerShell install snippet

```powershell
$ErrorActionPreference = 'Stop'

$TargetDir = "$HOME\AppData\Local\vibe-prompt-compiler-portable"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null
Copy-Item -Path (Join-Path $ScriptDir '*') -Destination $TargetDir -Recurse -Force

Write-Host "Installed vibe-prompt-compiler-portable to:"
Write-Host "  $TargetDir"
Write-Host ""
Write-Host "Quick test:"
Write-Host "  python \"$TargetDir\scripts\compile_prompt.py\" --request \"Build an admin dashboard MVP\" --stack \"Next.js, Supabase, Tailwind\""
Write-Host ""
Write-Host "Handoff test:"
Write-Host "  python \"$TargetDir\scripts\create_handoff.py\" --request \"Fix login API 500\" --mode bugfix --output handoff"
```

## Optional custom target directory

Replace `$TargetDir` with any folder you want, for example:

```powershell
$TargetDir = "$HOME\tools\vibe-prompt-compiler-portable"
```
