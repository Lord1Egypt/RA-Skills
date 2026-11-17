#!/usr/bin/env pwsh
# smart-web-search setup (Windows)
# v1.0.4
#
# 功能：
#   - 校验 Node.js >= 18
#   - 自动检测国内/海外，国内自动用 npmmirror 镜像
#   - npm install
#   - 检测系统 Chrome/Chromium，存在则提示可跳过下载
#   - 否则下载 Playwright Chromium
#
# 此脚本不会执行任何运行时自动安装。

$ErrorActionPreference = "Stop"
$SkillRoot = Resolve-Path "$PSScriptRoot\.."
$SkillRootPath = $SkillRoot.Path

Write-Host ""
Write-Host "=== smart-web-search Setup ==="
Write-Host ""
Write-Host "Dependencies:"
Write-Host "  - Node.js >= 18"
Write-Host "  - npm packages: cheerio, commander, iconv-lite, playwright"
Write-Host "  - Chromium ~150MB (if system Chrome found, prompts to skip)"
Write-Host ""

# ------------------------------ Node.js ------------------------------
$nodeCmd = Get-Command node -ErrorAction SilentlyContinue
if (-not $nodeCmd) {
    Write-Host "[X] Node.js not found"
    Write-Host "   -> https://nodejs.org (download LTS)"
    exit 1
}
$nodeVer = node --version
$major = [int]($nodeVer -replace '^v', '').Split('.')[0]
if ($major -lt 18) {
    Write-Host "[X] Node.js >= 18 required (current: $nodeVer)"
    exit 1
}
Write-Host "[OK] Node.js $nodeVer"

# ------------------------------ 网络区域 ------------------------------
$inChina = $false
Write-Host ""
Write-Host "Detecting network region..."
try {
    $resp = Invoke-RestMethod -Uri "https://myip.ipip.net" -TimeoutSec 3 -ErrorAction Stop
    if ($resp -match "中国|CN") { $inChina = $true }
} catch {
    try {
        $resp = Invoke-RestMethod -Uri "https://cip.cc" -TimeoutSec 3 -ErrorAction Stop
        if ($resp -match "中国|CN") { $inChina = $true }
    } catch {}
}

if ($inChina) {
    Write-Host "[OK] 国内网络，使用 npmmirror 镜像"
    $env:PLAYWRIGHT_DOWNLOAD_HOST = "https://npmmirror.com/mirrors/playwright"
    $registryArg = "--registry=https://registry.npmmirror.com"
} else {
    Write-Host "[OK] 海外网络，使用官方源"
    $registryArg = ""
}

# ------------------------------ npm install ------------------------------
Write-Host ""
Write-Host "Installing npm packages..."
Push-Location $SkillRootPath
try {
    if ($registryArg) {
        npm install $registryArg.Split(' ')
    } else {
        npm install
    }
    Write-Host "[OK] npm packages installed"
} finally {
    Pop-Location
}

# ------------------------------ Chromium ------------------------------
if ($env:CHROMIUM_EXECUTABLE_PATH -and (Test-Path $env:CHROMIUM_EXECUTABLE_PATH)) {
    Write-Host ""
    Write-Host "[OK] 用户已设置 CHROMIUM_EXECUTABLE_PATH=$env:CHROMIUM_EXECUTABLE_PATH，跳过下载"
} else {
    $systemChrome = $null
    $chromePaths = @(
        "${env:ProgramFiles}\Google\Chrome\Application\chrome.exe",
        "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
        "${env:LOCALAPPDATA}\Chromium\Application\chrome.exe",
        "${env:LOCALAPPDATA}\Microsoft\Edge\Application\msedge.exe",
        "C:\Program Files\Google\Chrome\Application\chrome.exe"
    )
    foreach ($p in $chromePaths) {
        if (Test-Path $p) { $systemChrome = $p; break }
    }

    if ($systemChrome) {
        Write-Host ""
        Write-Host "[OK] 检测到系统 Chrome: $systemChrome"
        Write-Host "     如要使用系统 Chrome 跳过 150MB 下载："
        Write-Host "       `$env:CHROMIUM_EXECUTABLE_PATH = `"$systemChrome`""
        Write-Host ""
        Write-Host "     仍将下载 Playwright Chromium 作为默认（更稳定，首次较慢）。"
        Write-Host "     如需跳过下载，按 Ctrl+C 中止，设置上面的环境变量后再运行 check-env.js。"
        Start-Sleep -Seconds 3
    }

    Write-Host ""
    Write-Host "Installing Playwright Chromium (~150MB)..."
    Push-Location $SkillRootPath
    try {
        npx --yes playwright install chromium
    } catch {
        Write-Host ""
        Write-Host "[!] chromium 主包安装失败，尝试 chromium-headless-shell..."
        try {
            npx --yes playwright install chromium-headless-shell
        } catch {
            Write-Host ""
            Write-Host "[X] Playwright Chromium 安装失败"
            Write-Host "   重试方法："
            Write-Host "     `$env:PLAYWRIGHT_DOWNLOAD_HOST = 'https://npmmirror.com/mirrors/playwright'"
            Write-Host "     npx playwright install chromium"
            Write-Host "   或使用系统 Chrome:"
            Write-Host "     `$env:CHROMIUM_EXECUTABLE_PATH = 'C:\path\to\chrome.exe'"
            exit 1
        }
    } finally {
        Pop-Location
    }
    Write-Host "[OK] Playwright Chromium installed"
}

# ------------------------------ 验证 ------------------------------
Write-Host ""
Write-Host "Verifying environment..."
Push-Location $SkillRootPath
try {
    node scripts/check-env.js
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "[OK] Setup complete!"
    } else {
        Write-Host ""
        Write-Host "[X] check-env.js 报告问题，请按提示修复"
        exit 1
    }
} finally {
    Pop-Location
}
