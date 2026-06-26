# Webhook 通知工具函数库
# 版本: 2.0.0
# 更新日期: 2026-06-04
# 功能: 钉钉、企业微信、飞书、Slack、Discord、Telegram + 模板系统 + 重试机制

# ============================================================================
# 平台识别函数
# ============================================================================

function Get-WebhookPlatform {
    param([string]$Url)
    
    if ($Url -match "dingtalk\.com") { return 'DingTalk' }
    if ($Url -match "qyapi\.weixin\.qq\.com") { return 'WeCom' }
    if ($Url -match "feishu\.cn|larksuite\.com") { return 'Feishu' }
    if ($Url -match "hooks\.slack\.com") { return 'Slack' }
    if ($Url -match "discord(app)?\.com") { return 'Discord' }
    if ($Url -match "telegram\.org|api\.telegram\.org") { return 'Telegram' }
    return 'Custom'
}

# ============================================================================
# 统一发送接口
# ============================================================================

function Send-Webhook {
    <#
    .SYNOPSIS
        发送 Webhook 消息（自动识别平台）
    
    .DESCRIPTION
        支持钉钉、企业微信、飞书、Slack、Discord、Telegram，自动识别平台
    
    .PARAMETER Url
        Webhook URL
    
    .PARAMETER Message
        消息内容
    
    .PARAMETER Title
        标题（用于 Markdown/卡片消息）
    
    .PARAMETER IsAtAll
        是否@所有人
    
    .PARAMETER AtMobiles
        @的手机号列表
    
    .PARAMETER Retry
        重试次数，默认 3
    
    .PARAMETER Timeout
        超时秒数，默认 30
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [string]$Url,
        
        [Parameter(Mandatory=$true)]
        [string]$Message,
        
        [string]$Title = "",
        [bool]$IsAtAll = $false,
        [array]$AtMobiles = @(),
        [int]$Retry = 3,
        [int]$Timeout = 30
    )
    
    $platform = Get-WebhookPlatform -Url $Url
    Write-Verbose "识别平台：$platform"
    
    $attempt = 0
    $lastError = $null
    
    while ($attempt -lt $Retry) {
        $attempt++
        
        try {
            $body = $null
            
            if ($platform -eq "DingTalk") {
                $body = @{msgtype="text";text=@{content=$Message}}
                if ($IsAtAll -or $AtMobiles.Count -gt 0) {
                    $body.text.at = @{isAtAll=$IsAtAll;atMobiles=$AtMobiles}
                }
                $body = $body | ConvertTo-Json -Depth 10
            }
            elseif ($platform -eq "WeCom") {
                $mob = if ($IsAtAll) { @("1") } else { $AtMobiles }
                $body = @{
                    msgtype="text"
                    text=@{
                        content=$Message
                        mentioned_list=@()
                        mentioned_mobile_list=$mob
                    }
                } | ConvertTo-Json -Depth 10
            }
            elseif ($platform -eq "Feishu") {
                $body = @{
                    msg_type="text"
                    content=@{text=$Message}
                } | ConvertTo-Json -Depth 10
            }
            elseif ($platform -eq "Slack") {
                $body = @{text=$Message} | ConvertTo-Json -Depth 10
            }
            elseif ($platform -eq "Discord") {
                $body = @{
                    content=$Message
                    embeds=@(@{
                        description=$Message
                        color=3447003
                        timestamp=(Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
                    })
                } | ConvertTo-Json -Depth 10
            }
            elseif ($platform -eq "Telegram") {
                $body = @{
                    text=$Message
                    parse_mode="HTML"
                } | ConvertTo-Json -Depth 10
            }
            else {
                $body = @{message=$Message;timestamp=(Get-Date)} | ConvertTo-Json -Depth 10
            }
            
            $response = Invoke-RestMethod -Uri $Url -Method Post -Body $body -ContentType "application/json; charset=utf-8" -TimeoutSec $Timeout
            
            # 检查响应
            $success = $false
            if ($platform -eq "DingTalk" -and $response.errcode -eq 0) { $success = $true }
            elseif ($platform -eq "WeCom" -and $response.errcode -eq 0) { $success = $true }
            elseif ($platform -eq "Feishu" -and $response.code -eq 0) { $success = $true }
            elseif ($platform -eq "Slack" -and $response -eq "ok") { $success = $true }
            elseif ($platform -eq "Discord" -and $response.id) { $success = $true }
            elseif ($platform -eq "Telegram" -and $response.ok) { $success = $true }
            elseif ($platform -eq "Custom") { $success = $true }
            
            if ($success) {
                Write-Verbose "✅ 发送成功 ($platform, 尝试 $attempt/$Retry)"
                return $true
            }
            else {
                $errorMsg = $response.errmsg, $response.msg, $response.error, "未知错误" | Select-Object -First 1
                Write-Warning "❌ 发送失败 ($platform): $errorMsg (尝试 $attempt/$Retry)"
                $lastError = $errorMsg
            }
        }
        catch {
            Write-Warning "⚠️ 请求异常: $_ (尝试 $attempt/$Retry)"
            $lastError = $_
        }
        
        if ($attempt -lt $Retry) {
            $delay = [math]::Pow(2, $attempt) # 指数退避：2, 4, 8 秒
            Write-Verbose "等待 $delay 秒后重试..."
            Start-Sleep -Seconds $delay
        }
    }
    
    Write-Error "所有重试失败 ($Retry 次). 最后错误：$lastError"
    return $false
}

# ============================================================================
# 批量发送
# ============================================================================

function Send-Webhook-Batch {
    param(
        [Parameter(Mandatory=$true)]
        [array]$Urls,
        
        [Parameter(Mandatory=$true)]
        [string]$Message,
        
        [bool]$IsAtAll = $false,
        [array]$AtMobiles = @(),
        [int]$Retry = 3
    )
    
    $results = @()
    
    foreach ($url in $Urls) {
        try {
            $result = Send-Webhook -Url $url -Message $Message -IsAtAll $IsAtAll -AtMobiles $AtMobiles -Retry $Retry
            $results += @{
                Url = $url
                Platform = Get-WebhookPlatform -Url $url
                Success = $result
                Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
            }
        }
        catch {
            $results += @{
                Url = $url
                Platform = Get-WebhookPlatform -Url $url
                Success = $false
                Error = $_.Exception.Message
                Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
            }
        }
    }
    
    return $results
}

# ============================================================================
# 测试连通性
# ============================================================================

function Test-Webhook-Connection {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Url
    )
    
    $platform = Get-WebhookPlatform -Url $Url
    $testMsg = "【Webhook 测试】平台：$platform | 时间：$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    
    Write-Host "🧪 测试 $platform Webhook..." -ForegroundColor Cyan
    Write-Host "URL: $Url"
    Write-Host "消息：$testMsg"
    
    $result = Send-Webhook -Url $Url -Message $testMsg
    
    if ($result) {
        Write-Host "✅ 测试成功" -ForegroundColor Green
        return $true
    }
    else {
        Write-Host "❌ 测试失败" -ForegroundColor Red
        return $false
    }
}

# ============================================================================
# 模板系统
# ============================================================================

$Script:WebhookTemplates = @{
    'system-alert' = {
        param($params)
        $severity = if ($params.Severity) { $params.Severity } else { "warning" }
        $emoji = switch ($severity) {
            "critical" { "🚨" }
            "warning"  { "⚠️" }
            "info"     { "ℹ️" }
            default   { "📌" }
        }
        return "$emoji【系统告警】`n组件：$($params.Component)`n状态：$($params.Status)`n详情：$($params.Details)`n时间：$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    }
    
    'deploy-success' = {
        param($params)
        return "✅ 部署成功`n项目：$($params.Project)`n版本：$($params.Version)`n环境：$($params.Environment)`n时间：$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    }
    
    'deploy-failed' = {
        param($params)
        return "❌ 部署失败`n项目：$($params.Project)`n版本：$($params.Version)`n环境：$($params.Environment)`n错误：$($params.Error)`n时间：$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    }
    
    'es-alert' = {
        param($params)
        return "📊 ES 异常告警`n索引：$($params.Index)`n异常数：$($params.Count)`n级别：$($params.Level)`n主机：$($params.Hosts -join ', ')`n时间：$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    }
}

function Send-Webhook-Template {
    <#
    .SYNOPSIS
        使用模板发送消息
    
    .PARAMETER Template
        模板名称：system-alert, deploy-success, deploy-failed, es-alert
    
    .PARAMETER Params
        模板参数
    #>
    param(
        [Parameter(Mandatory=$true)]
        [string]$Template,
        
        [Parameter(Mandatory=$true)]
        [hashtable]$Params,
        
        [Parameter(Mandatory=$true)]
        [string]$Url,
        
        [int]$Retry = 3
    )
    
    $templateFunc = $Script:WebhookTemplates[$Template]
    if (-not $templateFunc) {
        throw "模板不存在：$Template. 可用模板：$($Script:WebhookTemplates.Keys -join ', ')"
    }
    
    $message = & $templateFunc $Params
    
    Write-Verbose "使用模板：$Template"
    Write-Verbose "生成消息：$message"
    
    return Send-Webhook -Url $Url -Message $message -Retry $Retry
}

# ============================================================================
# 导出函数
# ============================================================================

Export-ModuleMember -Function @(
    'Get-WebhookPlatform',
    'Send-Webhook',
    'Send-Webhook-Batch',
    'Test-Webhook-Connection',
    'Send-Webhook-Template'
)