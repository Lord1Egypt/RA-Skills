param(
    [switch]$Force = $false
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Vibe Coding Rules - 安装程序" -ForegroundColor Cyan
Write-Host "  Version 2.5.0 (PowerShell Enhanced)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# === 检测 IDE/Agent 类型 ===
$skillDir = $null
$agentType = "unknown"

if (Test-Path "$env:USERPROFILE\.codebuddy\skills") {
    $skillDir = "$env:USERPROFILE\.codebuddy\skills"
    $agentType = "codebuddy"
    Write-Host "[检测] CodeBuddy 环境" -ForegroundColor Green
}

if (Test-Path ".cursor\rules") {
    if ($agentType -eq "unknown") { $agentType = "cursor" }
    Write-Host "[检测] Cursor 环境" -ForegroundColor Green
}

if ($agentType -eq "unknown") {
    Write-Host "[检测] 未检测到已知 IDE，使用通用模式" -ForegroundColor Yellow
    $agentType = "generic"
}

Write-Host "[目标] $agentType" -ForegroundColor White
Write-Host ""

# === 读取 pipeline.json ===
$pipeline = $null
if (Test-Path "pipeline.json") {
    $pipeline = Get-Content "pipeline.json" -Raw | ConvertFrom-Json
    Write-Host "[配置] pipeline.json 已加载" -ForegroundColor Green
    Write-Host "  项目: $($pipeline.project.name)" -ForegroundColor White
    if ($pipeline.project.port) {
        Write-Host "  端口: $($pipeline.project.port)" -ForegroundColor White
    }
} else {
    Write-Host "[警告] pipeline.json 未找到，使用默认参数" -ForegroundColor Yellow
}

# === 模板变量替换函数 ===
function Replace-Template {
    param([string]$content)
    if ($pipeline) {
        $content = $content -replace '\{\{pipeline\.project\.port\}\}', $pipeline.project.port
        $content = $content -replace '\{\{pipeline\.project\.host\}\}', $pipeline.project.host
        $content = $content -replace '\{\{pipeline\.project\.name\}\}', $pipeline.project.name
        $content = $content -replace '\{\{pipeline\.project\.testUrl\}\}', $pipeline.project.testUrl
        $content = $content -replace '\{\{pipeline\.project\.testPagePath\}\}', $pipeline.project.testPagePath
        $content = $content -replace '\{\{pipeline\.paths\.tests\}\}', $pipeline.paths.tests
        $content = $content -replace '\{\{pipeline\.paths\.changelogFormat\}\}', $pipeline.paths.changelogFormat
    }
    # 清理未替换的占位符
    $content = $content -replace '\{\{pipeline\.[^}]+\}\}', '[未配置]'
    $content = $content -replace '\{\{#if[^}]*\}\}|\{\{/if\}\}', ''
    $content = $content -replace '\{\{#each[^}]*\}\}|\{\{/each\}\}', ''
    $content = $content -replace '\{\{this\}\}', '[列表项]'
    return $content
}

# === 复制 Skill（含模板替换）===
function Copy-Skill {
    param(
        [string]$sourceDir,
        [string]$destDir,
        [string]$skillName,
        [bool]$replaceVars = $true
    )
    
    if (-not (Test-Path $destDir)) {
        New-Item -ItemType Directory -Path $destDir -Force | Out-Null
    }
    
    # 复制所有文件
    Get-ChildItem $sourceDir -Recurse -File | ForEach-Object {
        $relative = $_.FullName.Substring($sourceDir.Length + 1)
        $dest = Join-Path $destDir $relative
        
        $destParent = Split-Path $dest -Parent
        if (-not (Test-Path $destParent)) {
            New-Item -ItemType Directory -Path $destParent -Force | Out-Null
        }
        
        if ($replaceVars -and $_.Extension -eq ".md") {
            $content = Get-Content $_.FullName -Raw
            $content = Replace-Template $content
            Set-Content -Path $dest -Value $content -NoNewline
        } else {
            Copy-Item $_.FullName $dest -Force
        }
    }
    
    Write-Host "  $skillName" -ForegroundColor White -NoNewline
    Write-Host " [OK]" -ForegroundColor Green
}

# === 执行安装 ===
if ($agentType -eq "codebuddy") {
    Write-Host "[安装] 复制 Skill 到 CodeBuddy 目录（含模板替换）..." -ForegroundColor Cyan
    
    Copy-Skill "coding-principles" "$skillDir\coding-principles" "coding-principles" $false
    Copy-Skill "safe-terminal-executor" "$skillDir\safe-terminal-executor" "safe-terminal-executor"
    Copy-Skill "self-check" "$skillDir\self-check" "self-check"
    Copy-Skill "web-testing" "$skillDir\web-testing" "web-testing"
    Copy-Skill "changelog" "$skillDir\changelog" "changelog"
}

if ($agentType -eq "generic") {
    Write-Host "[安装] 创建 .ai-pipeline 目录..." -ForegroundColor Cyan
    
    $aiPipelineDir = ".ai-pipeline"
    if (-not (Test-Path $aiPipelineDir)) {
        New-Item -ItemType Directory -Path $aiPipelineDir -Force | Out-Null
    }
    
    Copy-Item "coding-principles\.ai-pipeline\prompt.md" "$aiPipelineDir\01-coding-principles.md" -Force
    Copy-Item "safe-terminal-executor\.ai-pipeline\prompt.md" "$aiPipelineDir\02-safe-terminal-executor.md" -Force
    
    # self-check 含模板变量
    $selfCheckContent = Get-Content "self-check\.ai-pipeline\prompt.md" -Raw
    $selfCheckContent = Replace-Template $selfCheckContent
    Set-Content -Path "$aiPipelineDir\03-self-check.md" -Value $selfCheckContent -NoNewline
    
    Copy-Item "web-testing\.ai-pipeline\prompt.md" "$aiPipelineDir\04-web-testing.md" -Force
    Copy-Item "changelog\.ai-pipeline\prompt.md" "$aiPipelineDir\05-changelog.md" -Force
    
    $readmeContent = Get-Content "\.ai-pipeline\README.md" -Raw
    $readmeContent = Replace-Template $readmeContent
    Set-Content -Path "$aiPipelineDir\README.md" -Value $readmeContent -NoNewline
    
    Write-Host "  .ai-pipeline/ 创建完成" -NoNewline
    Write-Host " [OK]" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  安装完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "下一步：" -ForegroundColor Yellow
Write-Host "  1. 编辑 pipeline.json 填入项目参数" -ForegroundColor White
Write-Host "  2. 安装可选依赖（如需要）：" -ForegroundColor White
Write-Host "     npm install playwright" -ForegroundColor Gray
Write-Host "     npx playwright install chromium" -ForegroundColor Gray
Write-Host "  3. 开始编程，流水线自动生效" -ForegroundColor White
