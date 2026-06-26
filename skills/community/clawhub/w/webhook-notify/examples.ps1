#!/usr/bin/env powershell
#
# Webhook通知工具 - 快速开始示例
#

# 引用webhook函数库
# 方法1: 绝对路径引用
. "E:\devdir\clawd\skills\webhook-notify\webhook-functions.ps1"

# 方法2: 相对路径引用
# . ".\webhook-functions.ps1"

# ============================================================================
# 配置webhook URL (建议使用环境变量)
# ============================================================================

# 设置环境变量（临时）
$env:DINGTALK_WEBHOOK = "https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN"
$env:WECOM_WEBHOOK = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"
$env:FEISHU_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_WEBHOOK"
$env:SLACK_WEBHOOK = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

# ============================================================================
# 示例1: 发送钉钉消息
# ============================================================================

Write-Host "示例1: 发送钉钉文本消息" -ForegroundColor Cyan
Send-WebhookDingTalk -WebhookUrl $env:DINGTALK_WEBHOOK `
    -Message "【openclaw】测试消息`n时间: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" `
    -IsAtAll $false

Pause

# ============================================================================
# 示例2: 发送钉钉Markdown消息
# ============================================================================

Write-Host "示例2: 发送钉钉Markdown消息" -ForegroundColor Cyan

$markdownContent = @"
## 系统告警

- **组件**: CPU
- **当前值**: 95%
- **阈值**: 85%
- **时间**: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

> 请及时处理！
"@

Send-WebhookDingTalk -WebhookUrl $env:DINGTALK_WEBHOOK `
    -Type markdown `
    -Title "[openclaw] 系统告警" `
    -Content $markdownContent `
    -Keyword "openclaw"

Pause

# ============================================================================
# 示例3: 发送钉钉ActionCard消息（带按钮）
# ============================================================================

Write-Host "示例3: 发送钉钉ActionCard消息" -ForegroundColor Cyan

Send-WebhookDingTalk -WebhookUrl $env:DINGTALK_WEBHOOK `
    -Type actionCard `
    -Title "告警详情" `
    -Text @"
**系统异常检测**

检测到系统资源使用率异常：
- CPU: 95% (阈值: 85%)
- 内存: 95% (阈值: 90%)

请及时处理！
"@ `
    -Buttons @(
        @{title="查看详情";url="https://example.com/alerts"},
        @{title="确认处理";url="https://example.com/ack"}
    )

Pause

# ============================================================================
# 示例4: 发送企业微信消息
# ============================================================================

Write-Host "示例4: 发送企业微信文本消息" -ForegroundColor Cyan

Send-WebhookWeCom -WebhookUrl $env:WECOM_WEBHOOK `
    -Message "【企业微信】测试消息`n时间: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" `
    -IsAtAll $false

Pause

# ============================================================================
# 示例5: 发送企业微信Markdown消息
# ============================================================================

Write-Host "示例5: 发送企业微信Markdown消息" -ForegroundColor Cyan

$mdContent = @"
**告警通知**

> 组件: CPU
> 当前值: 95%
> 时间: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

请及时处理！
"@

Send-WebhookWeCom -WebhookUrl $env:WECOM_WEBHOOK -Type markdown -Content $mdContent

Pause

# ============================================================================
# 示例6: 发送飞书消息
# ============================================================================

Write-Host "示例6: 发送飞书文本消息" -ForegroundColor Cyan

Send-WebhookFeishu -WebhookUrl $env:FEISHU_WEBHOOK `
    -Message "【飞书】测试消息`n时间: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"

Pause

# ============================================================================
# 示例7: 发送飞书富文本卡片
# ============================================================================

Write-Host "示例7: 发送飞书富文本卡片" -ForegroundColor Cyan

Send-WebhookFeishu -WebhookUrl $env:FEISHU_WEBHOOK `
    -Type post `
    -Title "系统告警" `
    -Content @(
        @{tag="text";text="检测到系统CPU使用率异常"},
        @{tag="text";text="当前值: 95%"},
        @{tag="text";text="时间: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"}
    )

Pause

# ============================================================================
# 示例8: 发送Slack消息
# ============================================================================

Write-Host "示例8: 发送Slack消息" -ForegroundColor Cyan

Send-WebhookSlack -WebhookUrl $env:SLACK_WEBHOOK `
    -Message "System Alert: CPU usage is 95%" `
    -Username "OpenClaw Bot" `
    -IconEmoji ":warning:"

Pause

# ============================================================================
# 示例9: 发送Slack Block Kit消息
# ============================================================================

Write-Host "示例9: 发送Slack Block Kit消息" -ForegroundColor Cyan

Send-WebhookSlack -WebhookUrl $env:SLACK_WEBHOOK `
    -Type block `
    -Blocks @(
        @{
            type="section"
            text=@{
                type="mrkdwn"
                text="*System Alert*`nCPU usage: 95%"
            }
        },
        @{
            type="actions"
            elements=@(
                @{
                    type="button"
                    text=@{type="plain_text";text="View Details"}
                    url="https://example.com"
                }
            )
        }
    )

Pause

# ============================================================================
# 示例10: 自定义HTTP请求
# ============================================================================

Write-Host "示例10: 自定义HTTP请求" -ForegroundColor Cyan

Send-WebhookCustom -Url "https://httpbin.org/post" `
    -Body @{
        event_type = "alert"
        severity = "high"
        component = "CPU"
        value = "95%"
        timestamp = (Get-Date -Format "o")
    } `
    -Headers @{"X-Custom-Header"="test-value"}

Pause

# ============================================================================
# 示例11: 测试webhook
# ============================================================================

Write-Host "示例11: 测试webhook连通性" -ForegroundColor Cyan

Test-Webhook -Url $env:DINGTALK_WEBHOOK -Platform DingTalk

Pause

# ============================================================================
# 示例12: 批量发送到多个平台
# ============================================================================

Write-Host "示例12: 批量发送到多个平台" -ForegroundColor Cyan

$message = "【批量测试】这是一条发送到多个平台的消息`n时间: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"

# 发送到钉钉
Send-WebhookDingTalk -WebhookUrl $env:DINGTALK_WEBHOOK -Message $message

# 发送到企业微信
Send-WebhookWeCom -WebhookUrl $env:WECOM_WEBHOOK -Message $message

# 发送到飞书
Send-WebhookFeishu -WebhookUrl $env:FEISHU_WEBHOOK -Message $message

Write-Host "批量发送完成" -ForegroundColor Green

Pause

# ============================================================================
# 示例13: 实际使用场景 - 系统监控告警
# ============================================================================

Write-Host "示例13: 系统监控告警" -ForegroundColor Cyan

function Send-SystemAlert {
    param(
        [string]$Component,
        [string]$CurrentValue,
        [string]$Threshold
    )
    
    $status = if ([double]$CurrentValue -gt [double]$Threshold) { "🚨 严重" } else { "⚠️ 警告" }
    
    $alertMessage = @"
【openclaw】$status | $Component 异常

- 当前值: $CurrentValue
- 阈值: $Threshold
- 时间: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

请及时处理！
"@
    
    Send-WebhookDingTalk -WebhookUrl $env:DINGTALK_WEBHOOK `
        -Message $alertMessage `
        -IsAtAll (if ($status -eq "🚨 严重") { $true } else { $false })
}

# 模拟发送告警
Send-SystemAlert -Component "CPU" -CurrentValue "95%" -Threshold "85%"
Send-SystemAlert -Component "内存" -CurrentValue "14.5/16 GB" -Threshold "90%"

Write-Host "告警发送完成" -ForegroundColor Green

# ============================================================================
# 结束
# ============================================================================

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "所有示例执行完成！" -ForegroundColor Green
Write-Host "========================================`n"
