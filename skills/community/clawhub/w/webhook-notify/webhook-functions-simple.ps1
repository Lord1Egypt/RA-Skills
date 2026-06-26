# Webhook Notification Functions (Simplified Version)
# Version: 1.0

# ============================================================================
# DingTalk Webhook Functions
# ============================================================================

function Send-WebhookDingTalk {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [string]$WebhookUrl,
        
        [string]$Message = "",
        
        [ValidateSet('text', 'markdown', 'actionCard')]
        [string]$Type = 'text',
        
        [string]$Title = "",
        [string]$Content = "",
        [string]$Text = "",
        
        [ValidateSet('0', '1')]
        [string]$BtnOrientation = '0',
        
        [array]$Buttons = @(),
        [array]$AtMobiles = @(),
        [array]$AtUserIds = @(),
        [bool]$IsAtAll = $false,
        
        [int]$Timeout = 30
    )
    
    $body = @{
        msgtype = $Type
    }
    
    if ($Type -eq 'text') {
        $body.text = @{
            content = $Message
        }
        if ($AtMobiles.Count -gt 0 -or $AtUserIds.Count -gt 0 -or $IsAtAll) {
            $body.text.at = @{
                atMobiles = $AtMobiles
                atUserIds = $AtUserIds
                isAtAll = $IsAtAll
            }
        }
    }
    elseif ($Type -eq 'markdown') {
        $body.markdown = @{
            title = $Title
            text = $Content
        }
        if ($AtMobiles.Count -gt 0 -or $AtUserIds.Count -gt 0 -or $IsAtAll) {
            $body.markdown.at = @{
                atMobiles = $AtMobiles
                atUserIds = $AtUserIds
                isAtAll = $IsAtAll
            }
        }
    }
    elseif ($Type -eq 'actionCard') {
        $body.actionCard = @{
            title = $Title
            text = $Text
            btnOrientation = $BtnOrientation
        }
        if ($Buttons.Count -gt 0) {
            $body.actionCard.btns = $Buttons
        }
    }
    
    try {
        $response = Invoke-RestMethod -Uri $WebhookUrl -Method Post -Body ($body | ConvertTo-Json -Depth 10) -ContentType 'application/json' -TimeoutSec $Timeout
        
        if ($response.errcode -eq 0) {
            Write-Verbose "DingTalk message sent successfully"
            return $true
        } else {
            Write-Error "DingTalk message failed: $($response.errmsg)"
            return $false
        }
    } catch {
        Write-Error "DingTalk webhook request failed: $_"
        return $false
    }
}

# ============================================================================
# WeCom Webhook Functions
# ============================================================================

function Send-WebhookWeCom {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [string]$WebhookUrl,
        
        [string]$Message = "",
        
        [ValidateSet('text', 'markdown', 'image', 'news', 'file')]
        [string]$Type = 'text',
        
        [string]$Content = "",
        [string]$MdId = "",
        
        [array]$Articles = @(),
        [array]$AtUsers = @(),
        [bool]$IsAtAll = $false,
        
        [int]$Timeout = 30
    )
    
    $body = @{
        msgtype = $Type
    }
    
    if ($Type -eq 'text') {
        $body.text = @{
            content = $Message
            mentioned_list = if ($AtUsers.Count -gt 0) { $AtUsers } else { @() }
            mentioned_mobile_list = if ($IsAtAll) { @("@all") } else { @() }
        }
    }
    elseif ($Type -eq 'markdown') {
        $body.markdown = @{
            content = $Content
            mentioned_list = if ($AtUsers.Count -gt 0) { $AtUsers } else { @() }
            mentioned_mobile_list = if ($IsAtAll) { @("@all") } else { @() }
        }
    }
    elseif ($Type -eq 'image') {
        $body.image = @{
            media_id = $MdId
        }
    }
    elseif ($Type -eq 'news') {
        $body.news = @{
            articles = $Articles
        }
    }
    elseif ($Type -eq 'file') {
        $body.file = @{
            media_id = $MdId
        }
    }
    
    try {
        $response = Invoke-RestMethod -Uri $WebhookUrl -Method Post -Body ($body | ConvertTo-Json -Depth 10) -ContentType 'application/json' -TimeoutSec $Timeout
        
        if ($response.errcode -eq 0) {
            Write-Verbose "WeCom message sent successfully"
            return $true
        } else {
            Write-Error "WeCom message failed: $($response.errmsg)"
            return $false
        }
    } catch {
        Write-Error "WeCom webhook request failed: $_"
        return $false
    }
}

# ============================================================================
# Custom HTTP Webhook Functions
# ============================================================================

function Send-WebhookCustom {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [string]$Url,
        
        [ValidateSet('GET', 'POST', 'PUT', 'DELETE', 'PATCH')]
        [string]$Method = 'POST',
        
        $Body,
        
        [string]$ContentType = 'application/json',
        [hashtable]$Headers = @{},
        
        [int]$Timeout = 30
    )
    
    $params = @{
        Uri = $Url
        Method = $Method
        TimeoutSec = $Timeout
    }
    
    if ($Body) {
        if ($Body -is [string]) {
            $params.Body = $Body
        } else {
            $params.Body = $Body | ConvertTo-Json -Depth 10
        }
        $params.ContentType = $ContentType
    }
    
    if ($Headers.Count -gt 0) {
        $params.Headers = $Headers
    }
    
    try {
        $response = Invoke-RestMethod @params
        Write-Verbose "HTTP request successful"
        return $response
    } catch {
        Write-Error "HTTP request failed: $_"
        return $false
    }
}

# ============================================================================
# Export Functions
# ============================================================================

Export-ModuleMember -Function @(
    'Send-WebhookDingTalk',
    'Send-WebhookWeCom',
    'Send-WebhookCustom'
)
