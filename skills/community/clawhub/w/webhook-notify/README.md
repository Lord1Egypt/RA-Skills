# Send-Webhook 统一函数

复制以下函数到你的脚本中，即可发送到任意平台的 webhook：

```powershell
function Send-Webhook {
    <#
    .SYNOPSIS
        发送 Webhook 消息（自动识别平台）
    
    .DESCRIPTION
        支持钉钉、企业微信、飞书，自动识别平台并构建正确的消息格式
    
    .PARAMETER Url
        Webhook URL（自动识别平台）
    
    .PARAMETER Message
        消息内容
    
    .PARAMETER Title
        消息标题（可选，用于 Markdown 类型）
    
    .PARAMETER IsAtAll
        是否@所有人（仅钉钉/企业微信）
    
    .PARAMETER AtMobiles
        @的手机号列表（仅钉钉/企业微信）
    
    .EXAMPLE
        Send-Webhook -Url $env:DINGTALK_WEBHOOK -Message "告警信息"
        Send-Webhook -Url $env:WECOM_WEBHOOK -Message "系统通知" -IsAtAll $true
        Send-Webhook -Url $env:FEISHU_WEBHOOK -Message "部署完成"
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [string]$Url,
        
        [Parameter(Mandatory=$true)]
        [string]$Message,
        
        [string]$Title = "",
        
        [bool]$IsAtAll = $false,
        
        [array]$AtMobiles = @()
    )
    
    # 自动识别平台
    $platform = $null
    if ($Url -match "dingtalk\.com") {
        $platform = "DingTalk"
    }
    elseif ($Url -match "qyapi\.weixin\.qq\.com") {
        $platform = "WeCom"
    }
    elseif ($Url -match "feishu\.cn|larksuite\.com") {
        $platform = "Feishu"
    }
    else {
        throw "不支持的 Webhook 平台：$Url"
    }
    
    Write-Verbose "识别到平台：$platform"
    
    # 构建消息体
    $body = $null
    
    if ($platform -eq "DingTalk") {
        # 钉钉
        $body = @{
            msgtype = "text"
            text = @{
                content = $Message
            }
        }
        
        if ($IsAtAll -or $AtMobiles.Count -gt 0) {
            $body.text.at = @{
                isAtAll = $IsAtAll
                atMobiles = $AtMobiles
            }
        }
        
        $body = $body | ConvertTo-Json -Depth 10
    }
    elseif ($platform -eq "WeCom") {
        # 企业微信
        $mentionedMobiles = if ($IsAtAll) { @("1") } else { $AtMobiles }
        
        $body = @{
            msgtype = "text"
            text = @{
                content = $Message
                mentioned_list = @()
                mentioned_mobile_list = $mentionedMobiles
            }
        } | ConvertTo-Json -Depth 10
    }
    elseif ($platform -eq "Feishu") {
        # 飞书
        $body = @{
            msg_type = "text"
            content = @{
                text = $Message
            }
        } | ConvertTo-Json -Depth 10
    }
    
    # 发送请求
    try {
        $response = Invoke-RestMethod -Uri $Url -Method Post -Body $body -ContentType "application/json; charset=utf-8"
        
        # 检查响应
        $success = $false
        if ($platform -eq "DingTalk" -and $response.errcode -eq 0) {
            $success = $true
        }
        elseif ($platform -eq "WeCom" -and $response.errcode -eq 0) {
            $success = $true
        }
        elseif ($platform -eq "Feishu" -and ($response.code -eq 0 -or $response.StatusCode -eq 200)) {
            $success = $true
        }
        
        if ($success) {
            Write-Verbose "✅ Webhook 发送成功 ($platform)"
            return $true
        }
        else {
            $errorMsg = if ($response.errmsg) { $response.errmsg } 
                       elseif ($response.msg) { $response.msg }
                       else { "未知错误" }
            Write-Error "❌ Webhook 发送失败 ($platform): $errorMsg"
            return $false
        }
    }
    catch {
        Write-Error "❌ Webhook 请求失败 ($platform): $_"
        return $false
    }
}
```

## 使用示例

### 1. 批量发送到多个平台

```powershell
# 加载函数
. "E:\devdir\clawd\scripts\Send-Webhook.ps1"

# 定义多个 webhook
$webhooks = @(
    "https://oapi.dingtalk.com/robot/send?access_token=***",
    "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=***",
    "https://open.feishu.cn/open-apis/bot/v2/hook/***"
)

# 批量发送
$message = "【openclaw】系统告警：CPU 使用率 95%"
foreach ($url in $webhooks) {
    Send-Webhook -Url $url -Message $message
}
```

### 2. 发送告警（@所有人）

```powershell
Send-Webhook -Url $env:DINGTALK_WEBHOOK `
    -Message "🚨 严重告警：内存使用率超过 95%" `
    -IsAtAll $true
```

### 3. 发送告警（@指定人）

```powershell
Send-Webhook -Url $env:DINGTALK_WEBHOOK `
    -Message "⚠️ 警告：磁盘空间不足" `
    -AtMobiles @("13800138000", "13900139000")
```

### 4. 在监控脚本中使用

```powershell
# E:\devdir\clawd\scripts\monitor-alert.ps1

# 加载函数（或复制函数定义到脚本开头）
. "E:\devdir\clawd\scripts\Send-Webhook.ps1"

# 检查资源
$mem = Get-CimInstance Win32_OperatingSystem
$memPct = [math]::Round((($mem.TotalVisibleMemorySize - $mem.FreePhysicalMemory) / $mem.TotalVisibleMemorySize) * 100, 1)

if ($memPct -gt 95) {
    Send-Webhook -Url $env:DINGTALK_WEBHOOK `
        -Message "🚨 内存告警：使用率 ${memPct}%" `
        -IsAtAll $true
}
elseif ($memPct -gt 85) {
    Send-Webhook -Url $env:DINGTALK_WEBHOOK `
        -Message "⚠️ 内存警告：使用率 ${memPct}%"
}
```

## 快速测试

```powershell
# 测试钉钉
Send-Webhook -Url "https://oapi.dingtalk.com/robot/send?access_token=***" `
    -Message "[openclaw] 测试消息 - $(Get-Date -Format 'HH:mm:ss')"

# 测试企业微信
Send-Webhook -Url "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=***" `
    -Message "[openclaw] 测试消息"

# 测试飞书
Send-Webhook -Url "https://open.feishu.cn/open-apis/bot/v2/hook/***" `
    -Message "[openclaw] 测试消息"
```

## 保存为独立脚本

将函数保存为 `E:\devdir\clawd\scripts\Send-Webhook.ps1`，然后在其他脚本中引用：

```powershell
. "E:\devdir\clawd\scripts\Send-Webhook.ps1"
Send-Webhook -Url $url -Message "消息内容"
```