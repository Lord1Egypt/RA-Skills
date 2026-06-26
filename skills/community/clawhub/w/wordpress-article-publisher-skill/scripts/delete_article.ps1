# WordPress 文章删除脚本

param(
    [Parameter(Mandatory=$true)]
    [string]$SiteUrl,
    
    [Parameter(Mandatory=$true)]
    [string]$Username,
    
    [Parameter(Mandatory=$true)]
    [string]$AppPassword,
    
    [Parameter(Mandatory=$true)]
    [int]$PostId
)

# 移除URL末尾的斜杠
$SiteUrl = $SiteUrl.TrimEnd('/')

# 构建API URL
$ApiUrl = "$SiteUrl/wp-json/wp/v2/posts/$PostId"

# 生成认证头
$Credentials = "${Username}:${AppPassword}"
$EncodedCredentials = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes($Credentials))

Write-Host "正在删除文章 ID: $PostId ..."

# 使用curl发送DELETE请求
$curlArgs = @(
    "-X", "DELETE",
    $ApiUrl,
    "-H", "Authorization: Basic $EncodedCredentials",
    "-H", "Content-Type: application/json"
)

$response = curl.exe @curlArgs 2>&1

try {
    $result = $response | ConvertFrom-Json
    
    if ($result.deleted -eq $true) {
        Write-Host "✅ 文章删除成功！" -ForegroundColor Green
        return @{ Success = $true }
    } else {
        Write-Host "❌ 删除失败: $($result.message)" -ForegroundColor Red
        return @{ Success = $false; Error = $result.message }
    }
} catch {
    Write-Host "❌ 删除失败: $response" -ForegroundColor Red
    return @{ Success = $false; Error = $response }
}
