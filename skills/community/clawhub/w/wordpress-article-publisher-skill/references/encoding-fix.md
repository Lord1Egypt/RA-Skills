# 中文编码问题解决方案

## 问题描述

使用 PowerShell 的 `Invoke-RestMethod` 发布包含中文的 WordPress 文章时，文章标题和内容显示为问号（????）。

## 问题原因

PowerShell 的 `ConvertTo-Json` 和 `Invoke-RestMethod` 在处理中文 UTF-8 编码时存在 bug：
- JSON 中的中文字符被转换为 Unicode 转义序列（如 `\u6587\u7ae0`）
- 但某些情况下这些转义无法正确解析
- 导致 WordPress 接收到的是乱码

## 解决方案

### 方案 1：使用 curl.exe（推荐）

PowerShell 脚本已内置此方案，使用 `curl.exe` 绕过编码问题。

**核心代码：**
```powershell
# 创建 JSON 文件（UTF-8 无 BOM）
$jsonFile = "$env:TEMP\wp-post.json"
$streamWriter = New-Object System.IO.StreamWriter(
    $jsonFile, 
    $false, 
    [System.Text.UTF8Encoding]::new($false)  # false = 无 BOM
)
$streamWriter.Write($jsonContent)
$streamWriter.Close()

# 使用 curl 发送
curl.exe -X POST $apiUrl `
    -H "Authorization: Basic $EncodedCredentials" `
    -H "Content-Type: application/json; charset=utf-8" `
    -d "@$jsonFile"
```

### 方案 2：手动构建 JSON

如果使用 `ConvertTo-Json` 导致问题，可以手动构建 JSON：

```powershell
$jsonBody = @"
{
    "title": "标题",
    "content": "<p>内容</p>",
    "status": "publish"
}
"@
```

### 方案 3：使用 .NET HttpClient

```powershell
$client = New-Object System.Net.Http.HttpClient
$content = New-Object System.Net.Http.StringContent(
    $jsonBody, 
    [System.Text.Encoding]::UTF8, 
    "application/json"
)
$response = $client.PostAsync($apiUrl, $content).Result
```

## UTF-8 编码说明

### UTF-8 有 BOM 和无 BOM 的区别

| 类型 | 说明 | 使用场景 |
|------|------|----------|
| UTF-8 with BOM | 文件开头有 3 字节 BOM | Windows 旧应用 |
| UTF-8 without BOM | 文件开头无 BOM（纯 UTF-8） | Web、API、跨平台 |

**WordPress API 要求使用 UTF-8 无 BOM 格式。**

### 如何检测文件编码

PowerShell 检测文件是否有 BOM：
```powershell
$bytes = Get-Content $filePath -Raw -Encoding Byte
if ($bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
    Write-Host "文件有 UTF-8 BOM"
} else {
    Write-Host "文件无 BOM 或其他编码"
}
```

## 常见错误代码

### rest_invalid_json

```
{"code":"rest_invalid_json","message":"Invalid JSON body passed.","data":{"status":400}}
```

**原因：** JSON 格式错误或编码问题

**解决方案：**
1. 检查 JSON 格式是否正确
2. 确保使用 UTF-8 无 BOM 编码
3. 检查是否有未转义的特殊字符

### rest_post_invalid_id

```
{"code":"rest_post_invalid_id","message":"Invalid post ID."}
```

**原因：** 尝试访问不存在的文章

### rest_cannot_edit

```
{"code":"rest_cannot_edit","message":"Sorry, you are not allowed to edit this post."}
```

**原因：** 认证失败或权限不足

**解决方案：**
1. 检查用户名和密码是否正确
2. 检查应用程序密码是否有效
3. 确认用户有编辑文章的权限

## PowerShell 编码配置

为避免编码问题，建议在脚本开头设置：

```powershell
# 设置控制台编码
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 设置输入编码
$PSDefaultParameterValues['*:Encoding'] = 'utf8'

# 禁用 BOM（避免与某些 API 不兼容）
[System.Text.Encoding]::Default = [System.Text.Encoding]::UTF8
```

## 测试编码是否正确

发布前可以测试：

```powershell
# 测试中文是否正确编码
$testString = "测试中文"
$bytes = [System.Text.Encoding]::UTF8.GetBytes($testString)
$decoded = [System.Text.Encoding]::UTF8.GetString($bytes)

if ($testString -eq $decoded) {
    Write-Host "✅ UTF-8 编码测试通过"
} else {
    Write-Host "❌ UTF-8 编码测试失败"
}
```

## Windows 系统区域设置

如果仍然遇到编码问题，可能需要检查系统区域设置：

1. 打开「设置」→「时间和语言」→「区域」
2. 确认「国家或地区」设置正确
3. 打开「区域」高级设置
4. 勾选「使用 Unicode UTF-8 提供全球语言支持」
5. 重启电脑

**注意：** 此设置可能影响其他应用程序的兼容性。
