# WordPress 文章发布脚本
# 使用 curl.exe 发送请求，解决 PowerShell 中文编码问题

param(
    [Parameter(Mandatory=$true)]
    [string]$SiteUrl,
    
    [Parameter(Mandatory=$true)]
    [string]$Username,
    
    [Parameter(Mandatory=$true)]
    [string]$AppPassword,
    
    [Parameter(Mandatory=$true)]
    [string]$Title,
    
    [Parameter(Mandatory=$true)]
    [string]$Content,
    
    [string]$Status = "publish",
    
    [string]$Slug = "",
    
    [int]$CategoryId = 0,
    
    [string]$Tags = ""
)

# 移除URL末尾的斜杠
$SiteUrl = $SiteUrl.TrimEnd('/')

# 构建API URL
$ApiUrl = "$SiteUrl/wp-json/wp/v2/posts"

# 生成认证头
$Credentials = "${Username}:${AppPassword}"
$EncodedCredentials = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes($Credentials))
$AuthHeader = "Basic $EncodedCredentials"

# 移除内容中的反引号（PowerShell转义字符）
$Content = $Content -replace '`', ''

# 创建JSON哈希表
$body = @{
    title = $Title
    content = $Content
    status = $Status
}

if ($Slug) {
    $body.slug = $Slug
}

if ($CategoryId -gt 0) {
    $body.categories = @($CategoryId)
}

if ($Tags) {
    $tagArray = $Tags -split ',' | ForEach-Object { $_.Trim() }
    $body.tags = $tagArray
}

# 转换为JSON并保存到临时文件（UTF-8无BOM）
$jsonFile = "$env:TEMP\wp-post-$((Get-Date).Ticks).json"
$jsonContent = $body | ConvertTo-Json -Depth 10 -Compress

# 使用StreamWriter写入UTF-8无BOM
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
$streamWriter = New-Object System.IO.StreamWriter($jsonFile, $false, $utf8NoBom)
$streamWriter.Write($jsonContent)
$streamWriter.Close()

# 使用curl发送请求
Write-Host "正在发布文章..."
Write-Host "标题: $Title"

$curlArgs = @(
    "-X", "POST",
    $ApiUrl,
    "-H", "Authorization: Basic $EncodedCredentials",
    "-H", "Content-Type: application/json; charset=utf-8",
    "-d", "@`"$jsonFile`""
)

$response = curl.exe @curlArgs 2>&1

# 清理临时文件
Remove-Item $jsonFile -Force -ErrorAction SilentlyContinue

# 解析响应
try {
    $result = $response | ConvertFrom-Json
    
    if ($result.id) {
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Green
        Write-Host "✅ 文章发布成功！" -ForegroundColor Green
        Write-Host "========================================" -ForegroundColor Green
        Write-Host "文章ID: $($result.id)"
        Write-Host "标题: $($result.title.rendered)"
        Write-Host "链接: $($result.link)"
        Write-Host "状态: $($result.status)"
        
        # 返回结果供调用脚本使用
        return @{
            Success = $true
            Id = $result.id
            Link = $result.link
            Title = $result.title.rendered
            Status = $result.status
        }
    } else {
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Red
        Write-Host "❌ 发布失败！" -ForegroundColor Red
        Write-Host "========================================" -ForegroundColor Red
        Write-Host "错误信息: $($result.message)"
        
        return @{
            Success = $false
            Error = $result.message
        }
    }
} catch {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "❌ 解析响应失败！" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "原始响应: $response"
    
    return @{
        Success = $false
        Error = "解析响应失败"
        RawResponse = $response
    }
}
