# Unity3D 游戏开发助手 - 编辑器连接模块
# 通过本地HTTP连接到Unity编辑器的桥接插件

$script:UnityPort = 18765
$script:UnityBaseUrl = "http://localhost:$UnityPort"
$script:UnityConnected = $false

function Connect-UnityEditor {
    <#
    .SYNOPSIS
    连接到Unity编辑器桥接服务器
    #>
    param([int]$Port = 18765)
    
    $script:UnityPort = $Port
    $script:UnityBaseUrl = "http://localhost:$Port"
    
    try {
        $result = Invoke-RestMethod -Uri "$UnityBaseUrl/api/ping" -TimeoutSec 5
        $script:UnityConnected = $true
        Write-Host "✅ Unity已连接 | 项目: $($result.project) | Unity版本: $($result.unityVersion)" -ForegroundColor Green
        return $result
    } catch {
        $script:UnityConnected = $false
        Write-Host "❌ 无法连接到Unity编辑器" -ForegroundColor Red
        Write-Host "请确保：" -ForegroundColor Yellow
        Write-Host "  1. Unity项目已打开" -ForegroundColor Yellow
        Write-Host "  2. UnityBridge.cs已放入 Editor/ 目录" -ForegroundColor Yellow
        Write-Host "  3. 已点击 Tools > OpenClaw Unity Bridge > Start Server" -ForegroundColor Yellow
        return $null
    }
}

function Get-UnitySceneList {
    <#
    .SYNOPSIS
    列出所有场景
    #>
    if (-not $script:UnityConnected) { Write-Host "⚠️ 未连接Unity"; return }
    $result = Invoke-RestMethod "$UnityBaseUrl/api/scene/list"
    Write-Host "📋 当前场景:" -ForegroundColor Cyan
    $result.openScenes | ForEach-Object { Write-Host "  - $_" }
    if ($result.buildSettings.Count -gt 0) {
        Write-Host "📋 Build Settings场景:" -ForegroundColor Cyan
        $result.buildSettings | ForEach-Object { Write-Host "  - $_" }
    }
    return $result
}

function Get-UnityCurrentScene {
    <#
    .SYNOPSIS
    获取当前场景详情
    #>
    if (-not $script:UnityConnected) { Write-Host "⚠️ 未连接Unity"; return }
    $result = Invoke-RestMethod "$UnityBaseUrl/api/scene/current"
    Write-Host "📍 $($result.name)" -ForegroundColor Cyan
    Write-Host "  路径: $($result.path)"
    Write-Host "  修改: $($result.isDirty ? '是' : '否')"
    Write-Host "  根对象: $($result.rootCount)个"
    Write-Host "  对象列表:" -ForegroundColor Gray
    $result.objects | ForEach-Object { Write-Host "    - $($_.name) ($($_.children)子, $($_.components)组件)" }
    return $result
}

function Open-UnityScene {
    <#
    .SYNOPSIS
    打开指定场景
    #>
    param([Parameter(Mandatory)] [string]$ScenePath)
    if (-not $script:UnityConnected) { Write-Host "⚠️ 未连接Unity"; return }
    $result = Invoke-RestMethod "$UnityBaseUrl/api/scene/open?path=$([System.Web.HttpUtility]::UrlEncode($ScenePath))"
    if ($result.success) {
        Write-Host "✅ 场景已打开: $ScenePath" -ForegroundColor Green
    } else {
        Write-Host "❌ $($result.error): $ScenePath" -ForegroundColor Red
    }
    return $result
}

function New-UnityGameObject {
    <#
    .SYNOPSIS
    创建GameObject
    #>
    param([string]$Name = "New_GameObject")
    if (-not $script:UnityConnected) { Write-Host "⚠️ 未连接Unity"; return }
    $result = Invoke-RestMethod "$UnityBaseUrl/api/gameobject/create?name=$([System.Web.HttpUtility]::UrlEncode($Name))"
    if ($result.success) {
        Write-Host "✅ 创建GameObject: $Name (ID: $($result.instanceId))" -ForegroundColor Green
    }
    return $result
}

function Remove-UnityGameObject {
    <#
    .SYNOPSIS
    删除GameObject
    #>
    param([Parameter(Mandatory)] [string]$Name)
    if (-not $script:UnityConnected) { Write-Host "⚠️ 未连接Unity"; return }
    $result = Invoke-RestMethod "$UnityBaseUrl/api/gameobject/delete?name=$([System.Web.HttpUtility]::UrlEncode($Name))"
    if ($result.success) {
        Write-Host "✅ 删除GameObject: $Name" -ForegroundColor Green
    } else {
        Write-Host "❌ $($result.error)" -ForegroundColor Red
    }
    return $result
}

function New-UnityScript {
    <#
    .SYNOPSIS
    生成C#脚本
    #>
    param(
        [Parameter(Mandatory)] [string]$Name,
        [string]$Content = ""
    )
    if (-not $script:UnityConnected) { Write-Host "⚠️ 未连接Unity"; return }

    $body = $Content
    $result = Invoke-RestMethod -Uri "$UnityBaseUrl/api/script/create?name=$Name" -Method POST -Body $body -ContentType "text/plain"
    if ($result.success) {
        Write-Host "✅ C#脚本已创建: $($result.path)" -ForegroundColor Green
    } else {
        Write-Host "❌ $($result.error)" -ForegroundColor Red
    }
    return $result
}

function Build-UnityProject {
    <#
    .SYNOPSIS
    构建/打包Unity项目
    .PARAMETER Target
    构建目标: StandaloneWindows64, StandaloneOSX, iOS, Android, WebGL
    .PARAMETER OutputPath
    输出路径
    #>
    param(
        [string]$Target = "StandaloneWindows64",
        [string]$OutputPath = "Builds"
    )
    if (-not $script:UnityConnected) { Write-Host "⚠️ 未连接Unity"; return }

    Write-Host "🏗️ 正在构建 $Target -> $OutputPath ..." -ForegroundColor Yellow
    $result = Invoke-RestMethod "$UnityBaseUrl/api/build?target=$Target&output=$([System.Web.HttpUtility]::UrlEncode($OutputPath))"
    
    if ($result.success) {
        Write-Host "✅ 构建成功!" -ForegroundColor Green
        Write-Host "  输出: $($result.outputPath)"
        Write-Host "  用时: $($result.totalTime)"
    } else {
        Write-Host "❌ 构建失败: $($result.result)" -ForegroundColor Red
        Write-Host "  错误: $($result.totalErrors)" -ForegroundColor Red
    }
    Write-Host "  警告: $($result.totalWarnings)" -ForegroundColor Yellow
    return $result
}

function Start-UnityPlayMode {
    <#
    .SYNOPSIS
    启动Play Mode
    #>
    if (-not $script:UnityConnected) { Write-Host "⚠️ 未连接Unity"; return }
    $result = Invoke-RestMethod "$UnityBaseUrl/api/play"
    Write-Host "▶️ Play Mode: 已启动" -ForegroundColor Green
    return $result
}

function Stop-UnityPlayMode {
    <#
    .SYNOPSIS
    停止Play Mode
    #>
    if (-not $script:UnityConnected) { Write-Host "⚠️ 未连接Unity"; return }
    $result = Invoke-RestMethod "$UnityBaseUrl/api/stop"
    Write-Host "⏹️ Play Mode: 已停止" -ForegroundColor Yellow
    return $result
}

# 导出所有函数
Export-ModuleMember -Function Connect-UnityEditor, Get-UnitySceneList, Get-UnityCurrentScene, Open-UnityScene, New-UnityGameObject, Remove-UnityGameObject, New-UnityScript, Build-UnityProject, Start-UnityPlayMode, Stop-UnityPlayMode
