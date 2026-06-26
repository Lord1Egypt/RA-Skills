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
    
    # Force UTF8 encoding
    $backupEncoding = [System.Text.Encoding]::Default
    [System.Text.Encoding]::Default = [System.Text.Encoding]::UTF8
    
    $body = @{
        msgtype = $Type
    }
    
    if ($Type -eq 'text') {
        $body.text = @{
            content = $Message
        }
        if ($AtMobiles.Count -gt 0 -or $AtUserIds.Count -gt 0 -or $IsAtAll) {
            $body.text.at = @{
                atMobiles = @($AtMobiles)
                atUserIds = @($AtUserIds)
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
                atMobiles = @($AtMobiles)
                atUserIds = @($AtUserIds)
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
            $body.actionCard.btns = @($Buttons)
        }
    }
    
    # Convert to JSON with UTF8 encoding
    $jsonBody = $body | ConvertTo-Json -Depth 10
    
    # Create POST request with UTF8 encoding
    try {
        $uri = [System.Uri]$WebhookUrl
        $httpClient = [System.Net.Http.HttpClient]::new()
        $httpClient.Timeout = [System.TimeSpan]::FromSeconds($Timeout)
        
        $content = [System.Net.Http.StringContent]::new($jsonBody, [System.Text.Encoding]::UTF8, "application/json")
        $response = $httpClient.PostAsync($uri, $content).GetAwaiter().GetResult()
        $responseBody = $response.Content.ReadAsStringAsync().GetAwaiter().GetResult()
        
        if ($response.StatusCode -eq [System.Net.HttpStatusCode]::OK) {
            $result = $responseBody | ConvertFrom-Json
            
            if ($result.errcode -eq 0) {
                Write-Verbose "DingTalk message sent successfully"
                [System.Text.Encoding]::Default = $backupEncoding
                return $true
            } else {
                Write-Error "DingTalk message failed: $($result.errmsg)"
                [System.Text.Encoding]::Default = $backupEncoding
                return $false
            }
        } else {
            Write-Error "DingTalk webhook request failed: $($response.StatusCode)"
            [System.Text.Encoding]::Default = $backupEncoding
            return $false
        }
        
        $httpClient.Dispose()
    } catch {
        Write-Error "DingTalk webhook request failed: $_"
        [System.Text.Encoding]::Default = $backupEncoding
        return $false
    }
}

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
    
    $backupEncoding = [System.Text.Encoding]::Default
    [System.Text.Encoding]::Default = [System.Text.Encoding]::UTF8
    
    $body = @{
        msgtype = $Type
    }
    
    if ($Type -eq 'text') {
        $body.text = @{
            content = $Message
            mentioned_list = if ($AtUsers.Count -gt 0) { @($AtUsers) } else { @() }
            mentioned_mobile_list = if ($IsAtAll) { @("@all") } else { @() }
        }
    }
    elseif ($Type -eq 'markdown') {
        $body.markdown = @{
            content = $Content
            mentioned_list = if ($AtUsers.Count -gt 0) { @($AtUsers) } else { @() }
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
            articles = @($Articles)
        }
    }
    elseif ($Type -eq 'file') {
        $body.file = @{
            media_id = $MdId
        }
    }
    
    try {
        $uri = [System.Uri]$WebhookUrl
        $httpClient = [System.Net.Http.HttpClient]::new()
        $httpClient.Timeout = [System.TimeSpan]::FromSeconds($Timeout)
        
        $content = [System.Net.Http.StringContent]::new(($body | ConvertTo-Json -Depth 10), [System.Text.Encoding]::UTF8, "application/json")
        $response = $httpClient.PostAsync($uri, $content).GetAwaiter().GetResult()
        $responseBody = $response.Content.ReadAsStringAsync().GetAwaiter().GetResult()
        
        $result = $responseBody | ConvertFrom-Json
        
        if ($result.errcode -eq 0) {
            Write-Verbose "WeCom message sent successfully"
            [System.Text.Encoding]::Default = $backupEncoding
            return $true
        } else {
            Write-Error "WeCom message failed: $($result.errmsg)"
            [System.Text.Encoding]::Default = $backupEncoding
            return $false
        }
        
        $httpClient.Dispose()
    } catch {
        Write-Error "WeCom webhook request failed: $_"
        [System.Text.Encoding]::Default = $backupEncoding
        return $false
    }
}

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
    
    $backupEncoding = [System.Text.Encoding]::Default
    [System.Text.Encoding]::Default = [System.Text.Encoding]::UTF8
    
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
        [System.Text.Encoding]::Default = $backupEncoding
        return $response
    } catch {
        Write-Error "HTTP request failed: $_"
        [System.Text.Encoding]::Default = $backupEncoding
        return $false
    }
}
