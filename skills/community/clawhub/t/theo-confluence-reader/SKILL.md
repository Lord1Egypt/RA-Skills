---
name: theo-confluence-reader
description: |
  读取Confluence需求文档并整理成指定格式。采集原则是"忠实记录"，而非"需求分析"。输出包括：{序号}_{标题}.md（每个页面一个Markdown文件）、requirement-meta.md（元信息）、images/（所有图片，文件中包含图片引用）。
---

# Theo Confluence Reader

## 全局配置

```powershell
# Confluence 配置（根据实际环境修改）
$confluenceBaseUrl = "https://confluence.xxx.com"
$outputDir = "C:\Users\xxx\.openclaw\workspace\output"
$workspaceDir = "C:\Users\xxx\.openclaw\workspace"
$maxSize = 1GB
$warnThreshold = 0.8
```

## 核心原则

**这个skill的职责是"忠实采集"，不是"需求分析"**
- 只做格式转换（HTML → MD），不做内容删减、概括或精简
- 保留原文的所有细节，包括表格、列表、备注、批注等
- 不要对原文做任何主观判断、删除或重组

## 执行规则（强制）

**⚠️ 必须抓取所有页面，不允许部分抓取或偷懒**

### 默认行为
1. **自动抓取全部**：给定一个Confluence页面链接后，必须抓取该页面**及其所有子页面**的全部内容
2. **不允许只抓索引**：不能只抓父页面或索引页就停下来，必须深入到每个叶子节点
3. **不允许跳过**：不能因为"内容太多"或"时间太长"而跳过某些页面

### 唯一例外：确认模式（仅允许询问一次）
如果预估采集时间超过5分钟或页面数量超过10个，可以先整理大纲并预估资源，返回给用户确认。

**但必须遵守以下规则**：
- **只能询问一次**：确认后必须执行完整，不能再次询问
- **大纲必须包含**：
  - 所有待抓取页面的完整列表
  - 预估页面数量
  - 预估时间和资源消耗
- **确认后必须执行**：用户确认后，立即开始抓取所有页面，中途不能停止或询问
- **禁止多次询问**：一旦用户确认后，不能以任何理由再次询问是否继续

### 示例

**错误做法（禁止）**：
- 只抓父页面索引，给用户后说"详细内容需要再抓"
- 抓了一部分后说"太多了要不要继续"
- 用户确认后 又问"这个子页面要不要抓"

**正确做法**：
- 要么直接全部抓完
- 要么先给大纲确认，**确认后全部抓完**

## 存储上限

**output/ 目录总大小上限：1GB**

- 每次创建新目录前检查总大小
- 超过 80%（800MB）时：自动删除最早的目录
- 超过 100%（1GB）时：强制删除最早的目录直到低于 80%

**检查并清理脚本**：
```powershell
$outputDir = "C:\Users\xxx\.openclaw\workspace\output"
$workspaceDir = "C:\Users\xxx\.openclaw\workspace"
$maxSize = 1GB
$warnThreshold = 0.8

if (!(Test-Path $outputDir)) { 
    New-Item -ItemType Directory -Path $outputDir -Force
}

# 计算 output 目录大小 + workspace 根目录下的 zip 文件大小
$outputSize = 0
$zipSize = 0

$outputItems = Get-ChildItem $outputDir -Recurse -ErrorAction SilentlyContinue
if ($outputItems) {
    $outputSize = ($outputItems | Measure-Object -Property Length -Sum).Sum
}

$zipFiles = Get-ChildItem $workspaceDir -Filter "*.zip" -ErrorAction SilentlyContinue
if ($zipFiles) {
    $zipSize = ($zipFiles | Measure-Object -Property Length -Sum).Sum
}

$totalSize = $outputSize + $zipSize

if ($totalSize -gt ($maxSize * $warnThreshold)) {
    Write-Host "存储超过 80%，开始清理..."
    
    # 1. 删除最早的 zip 文件
    if ($zipSize -gt 0) {
        $zipFilesSorted = $zipFiles | Sort-Object LastWriteTime
        foreach ($zip in $zipFilesSorted) {
            if ($totalSize -lt ($maxSize * $warnThreshold)) { break }
            $z = $zip.Length
            Remove-Item $zip.FullName -Force
            $totalSize -= $z
            Write-Host "已删除压缩包: $($zip.Name)"
        }
    }
    
    # 2. 删除最早的 output 子目录
    $dirs = Get-ChildItem $outputDir -Directory -ErrorAction SilentlyContinue | Sort-Object LastWriteTime
    foreach ($dir in $dirs) {
        if ($totalSize -lt ($maxSize * $warnThreshold)) { break }
        $dirSize = (Get-ChildItem $dir.FullName -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
        if ($dirSize -gt 0) {
            Remove-Item $dir.FullName -Recurse -Force
            $totalSize -= $dirSize
            Write-Host "已删除: $($dir.Name)"
        }
    }
}
```

## 输出目录结构

**重要：每次运行都会在 output/ 下创建一个以"页面标题_时间戳"命名的独立目录，避免文件混淆。**

**pageId获取方式**：
- 从Confluence URL中提取：`/pages/viewpage.action?pageId=272188760` → `pageId=272188760`
- 或从页面源码中获取

```
output/
├── 页面标题_2026-03-13_2030/
│   ├── 01_需求概述.md          # 页面1的MD转换版
│   ├── 02_登录注册.md          # 页面2的MD转换版
│   ├── 03_系统首页.md          # 页面3的MD转换版
│   ├── ...                     # 其他页面
│   ├── requirement-meta.md    # 元信息（整个采集任务的元信息）
│   └── images/                 # 关联图片
│       ├── 01_需求概述_功能架构图.png
│       ├── 02_登录注册.png
│       └── ...
```

**时间戳格式**：`YYYY-MM-DD_HHmm`（年月日_时分）

## 前置要求

**必须先登录 Confluence**：
1. 在运行 OpenClaw 的机器上打开浏览器
2. 访问 Confluence 页面并完成登录
3. 保持登录状态，后续的图片下载和内容获取都依赖这个已登录的 session

## 操作流程

### Step 1: 分析页面结构 + 创建输出目录 + 检查存储上限

**⚠️ 重要：必须抓取所有子页面**
- 这一步必须展开页面树，列出**所有**子页面（包括二级、三级、四级等全部层级）
- 不能只抓父页面就停止
- 记录每个子页面的：pageId、标题、层级

**输入验证**：
```powershell
param(
    [Parameter(Mandatory=$true)]
    [string]$confluenceUrl
)

# 验证URL格式
if ($confluenceUrl -notmatch 'https?://[^/]+/pages/(viewpage\.action\?pageId=|viewpage\.action\?title=)') {
    throw "无效的Confluence URL，请提供形如 https://confluence.xxx.com/pages/viewpage.action?pageId=123456 的URL"
}

# 提取pageId（如果URL中包含）
if ($confluenceUrl -match 'pageId=(\d+)') {
    $rootPageId = $matches[1]
    Write-Host "根页面ID: $rootPageId"
}
```

**获取完整页面树的两种方法：**

#### 方法1：通过浏览器页面树获取（默认推荐）

1. 用浏览器打开用户提供的 Confluence URL
2. 在页面左侧找到"页面树结构"
3. 点击"展开全部"或手动展开**所有层级**（包括二级、三级、四级...直到叶子节点）
4. 使用 browser evaluate 获取页面树的完整结构：
   ```javascript
   // 在浏览器控制台执行，获取所有页面链接
   const links = Array.from(document.querySelectorAll('a[href*="pageId="]')).map(a => ({
       title: a.textContent.trim(),
       pageId: a.href.match(/pageId=(\d+)/)?.[1],
       href: a.href
   }));
   console.log(JSON.stringify(links, null, 2));
   ```
5. 解析获取的数据，提取所有 pageId 和标题
6. **⚠️ 关键**：必须确保页面树完全展开，所有层级的子页面都被展开
7. 确认总共有多少个页面需要获取

#### 方法2：通过 Confluence REST API 获取（备选）

```powershell
# 获取页面及其所有子页面
function Get-ConfluencePageTree {
    param(
        [string]$baseUrl = "https://confluence.xxx.com",
        [string]$rootPageId,
        [string]$cookie  # 登录 cookie
    )
    
    $pages = @()
    
    # 获取当前页面的直接子页面
    $apiUrl = "$baseUrl/rest/api/content/$rootPageId/child/page"
    $headers = @{
        "Cookie" = $cookie
        "Content-Type" = "application/json"
    }
    
    $response = Invoke-RestMethod -Uri $apiUrl -Headers $headers -Method Get
    foreach ($page in $response.results) {
        $pages += @{
            pageId = $page.id
            title = $page.title
            type = $page.type
        }
        
        # 递归获取子页面的子页面
        $childPages = Get-ConfluencePageTree -baseUrl $baseUrl -rootPageId $page.id -cookie $cookie
        $pages += $childPages
    }
    
    return $pages
}

# 调用
$allPages = Get-ConfluencePageTree -rootPageId $rootPageId -cookie $cookie
Write-Host "共获取 $($allPages.Count) 个页面"
```

**检查并清理存储（如果超过80%上限）**：
```powershell
# 复用全局配置的变量，或直接使用以下默认值
$outputDir = "C:\Users\xxx\.openclaw\workspace\output"
$workspaceDir = "C:\Users\xxx\.openclaw\workspace"
$maxSize = 1GB
$warnThreshold = 0.8

if (!(Test-Path $outputDir)) { 
    New-Item -ItemType Directory -Path $outputDir -Force
}

# 计算 output 目录大小 + workspace 根目录下的 zip 文件大小
$outputSize = 0
$zipSize = 0

$outputItems = Get-ChildItem $outputDir -Recurse -ErrorAction SilentlyContinue
if ($outputItems) {
    $outputSize = ($outputItems | Measure-Object -Property Length -Sum).Sum
}

$zipFiles = Get-ChildItem $workspaceDir -Filter "*.zip" -ErrorAction SilentlyContinue
if ($zipFiles) {
    $zipSize = ($zipFiles | Measure-Object -Property Length -Sum).Sum
}

$totalSize = $outputSize + $zipSize

if ($totalSize -gt ($maxSize * $warnThreshold)) {
    Write-Host "存储超过 80%，开始清理..."
    
    # 1. 删除最早的 zip 文件
    if ($zipSize -gt 0) {
        $zipFilesSorted = $zipFiles | Sort-Object LastWriteTime
        foreach ($zip in $zipFilesSorted) {
            if ($totalSize -lt ($maxSize * $warnThreshold)) { break }
            $z = $zip.Length
            Remove-Item $zip.FullName -Force
            $totalSize -= $z
            Write-Host "已删除压缩包: $($zip.Name)"
        }
    }
    
    # 2. 删除最早的 output 子目录
    $dirs = Get-ChildItem $outputDir -Directory -ErrorAction SilentlyContinue | Sort-Object LastWriteTime
    foreach ($dir in $dirs) {
        if ($totalSize -lt ($maxSize * $warnThreshold)) { break }
        $dirSize = (Get-ChildItem $dir.FullName -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
        if ($dirSize -gt 0) {
            Remove-Item $dir.FullName -Recurse -Force
            $totalSize -= $dirSize
            Write-Host "已删除: $($dir.Name)"
        }
    }
}
```

**创建带时间戳的输出目录**：
```powershell
# 获取当前时间戳
$timestamp = Get-Date -Format "yyyy-MM-dd_HHmm"
# 页面标题（去除非法字符）
$safeTitle = "页面标题" -replace '[\\/:*?"<>|]', '_'
# 创建目录
$outputDir = "C:\Users\root\.openclaw\workspace\output\${safeTitle}_${timestamp}"
New-Item -ItemType Directory -Path "$outputDir\images" -Force
```

**后续所有文件都写入这个新创建的目录**，而不是直接写进 `output/` 根目录。

### Step 2: 获取每个页面的内容（使用 sessions_spawn）

**⚠️ 必须抓取所有页面，不允许选择性抓取**

**重要**：由于需要获取多个页面，必须使用 sessions_spawn 派发子任务并行处理。

**步骤**：
1. 分析所有pageId列表（从页面URL或页面树中提取）
2. 派发子任务获取所有页面的文字内容
3. 派发子任务下载所有页面的图片
4. 监控子任务直到完成

**获取页面内容的方法**：
1. 使用 browser 访问 Confluence 页面
2. 获取页面完整HTML内容（browser evaluate 或 snapshot）
3. 将HTML转换为Markdown格式

**HTML转Markdown推荐方法**：
- 方法1：使用 Python `markdownify` 库
  ```powershell
  python -m pip install markdownify
  python -c "from markdownify import markdownify; print(markdownify(html_content))"
  ```
- 方法2：使用 Node.js `turndown` 库
  ```powershell
  npm install -g turndown
  echo $htmlContent | turndown
  ```
- 方法3：使用在线API（如 html2md.com 的API）

**关键要求**：转换过程中不得删除任何内容，包括：
- 表格（保持表格结构）
- 图片引用（转换为 `![](images/xxx.png)` 格式）
- 代码块（保持原始格式）
- 特殊字符和格式

### Step 3: 获取页面图片（使用 curl 直接下载）

**重要**：使用 curl 直接下载图片原始文件，不再使用 browser 截图方式。

**⚠️ 必须为每个页面下载图片，不管页面层级**

**不管是一级页面、二级页面、三级页面还是更深层次的子页面，都必须下载该页面的所有图片附件！**

> **关键原则**：每个页面独立获取图片 — 页面层级不影响图片下载，父页面的图片 ≠ 子页面的图片，子页面需要单独获取自己的图片！

**⚠️ 前置要求：必须先获取登录 Cookie**

由于 Confluence 私有图片需要登录才能下载，**需要用户手动提供 Cookie**：

1. 用户在浏览器中登录 Confluence
2. 按 F12 打开开发者工具 → Application/Storage → Cookies
3. 复制以下 cookie 的值：
   - `JSESSIONID`
   - `CONFLAuth`
   - 其他可能需要的 cookie（如 `_ga`、`tgw_l7_route` 等）

4. 将完整 cookie 字符串提供给模型，格式如：
   ```
   _ga=GA1.1.xxx; pt_66be4504=xxx; JSESSIONID=xxx; tgw_l7_route=xxx
   ```

**获取认证Cookie**：
```powershell
# 用户提供的 cookie（直接使用，无需额外处理）
$cookie = "用户提供的完整cookie字符串"
```

**图片获取步骤**：
1. **遍历所有页面**：对 Step 1 中获取的**每一个**页面（包括所有层级的一级、二级、三级...子页面）
2. 对每个pageId，访问附件页面：`https://confluence.xxx.com/pages/viewpageattachments.action?pageId={pageId}`
3. 使用 curl 获取附件列表页面源码
4. 解析 `data-attachment-filename` 属性，找到该页面**所有**图片附件
5. 使用 curl 下载每个图片
6. **重复步骤1-5直到所有页面的图片都下载完成**

**图片命名规则**：
- 格式：`{页面序号}_{页面名称}.{扩展名}`
- 例如：`01_需求概述_功能架构图.png`、`02_登录注册.png`

**curl 下载命令示例**：
```powershell
$cookie = "用户提供的cookie"
$imageUrl = "https://confluence.xxx.com/download/attachments/272188760/image-2026-3-3_14-10-42.png?api=v2"
$outputFile = "C:\Users\root\.openclaw\workspace\output\images\01_需求概述_功能架构图.png"

curl.exe -L -o $outputFile $imageUrl -H "Cookie: $cookie"
```

**注意事项**：
- 使用 `curl.exe` 而非 PowerShell 内置 `curl` 别名
- 添加 `-L` 参数跟随重定向
- 必须携带完整登录 Cookie 才能下载私有图片
- Cookie 可能有有效期限制，如失效需让用户重新提供

**curl 下载脚本（含错误处理和重试）**：
```powershell
# 配置
$cookie = "JSESSIONID=xxx; CONFLAuth=xxx"  # 替换为实际 cookie
$imagesDir = "$outputDir\images"
$maxRetries = 3

# 创建 images 目录
if (!(Test-Path $imagesDir)) {
    New-Item -ItemType Directory -Path $imagesDir -Force
}

# 图片列表（从附件页面解析得到）
$imageList = @(
    @{pageId="272191284"; filename="image.png"; ext="png"},
    @{pageId="272191284"; filename="photo.jpg"; ext="jpg"}
)

$index = 1
foreach ($img in $imageList) {
    $imageUrl = "https://confluence.xxx.com/download/attachments/$($img.pageId)/$($img.filename)"
    $outputFile = "$imagesDir\$($img.pageId)_$index.$($img.ext)"
    
    # 重试逻辑
    $success = $false
    for ($retry = 1; $retry -le $maxRetries; $retry++) {
        Write-Host "尝试下载 ($retry/$maxRetries): $imageUrl"
        
        $result = curl.exe -L -o $outputFile $imageUrl `
            -H "Cookie: $cookie" `
            -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" `
            --silent --show-error `
            2>&1
        
        # 检查文件是否成功下载
        if ((Test-Path $outputFile) -and (Get-Item $outputFile).Length -gt 0) {
            $success = $true
            Write-Host "已下载: $outputFile"
            break
        } else {
            Write-Host "下载失败，等待重试..."
            Start-Sleep -Seconds 2
        }
    }
    
    if (-not $success) {
        Write-Host "警告: 图片下载失败 - $imageUrl" -ForegroundColor Yellow
    }
    
    $index++
}

Write-Host "图片下载完成，共 $($imageList.Count) 张"
```

**注意事项**：
- 使用 `curl.exe` 而非 PowerShell 内置 `curl` 别名
- 添加 `-L` 参数跟随重定向
- 保留原始文件格式（png/jpg/svg等）
- 必须携带登录 Cookie 才能下载私有图片
- 添加重试逻辑应对网络不稳定
- 下载后检查文件大小确保下载成功

### Step 4: 生成输出文件

**所有文件都写入 Step 1 创建的 `$outputDir` 目录**。

#### 4.1 {序号}_{标题}.md（每个页面一个）

将Confluence页面的HTML内容忠实转换为Markdown格式。

**关键：必须插入图片引用！**

在生成 md 文件时，对于该页面关联的每张图片，必须在**适当位置**插入图片引用：

```powershell
# 假设当前页面是 "02_登录注册"，该页面有 2 张图片
# images/ 目录中的文件：
#   - 02_登录注册.png
#   - 02_登录注册_2.png

# 在 md 文件内容中插入图片引用（建议放在页面标题下方或相关章节后）

$markdownContent = @"
# 2.1 登录注册（一期交付）

![](images/02_登录注册.png)

## 1、功能设计

...

## 2、原型图

![](images/02_登录注册_2.png)

...
"@

# 写入文件
$mdFileName = "02_登录注册.md"
$mdFilePath = Join-Path $outputDir $mdFileName
Set-Content -Path $mdFilePath -Value $markdownContent -Encoding UTF8
```

**图片引用规则**：
- 格式：`![](images/{图片文件名})`
- 位置：
  - 如果图片是功能架构图/流程图，放在页面标题下方或相应章节后
  - 如果是原型图，放在对应功能描述之后
  - 如果无法确定位置，放在页面末尾
- 如果一个页面有多张图片，按文件名排序后依次插入

#### 4.2 requirement-meta.md

```markdown
# 采集元信息

- 来源页面: [Confluence 页面 URL]
- 采集根页面: [根页面标题和 URL]
- 采集时间: [ISO 8601 格式，如 2026-03-15T18:00:00+08:00]
- 采集环境: [Confluence URL 域名]
- 总页面数: [页面总数]
- 页面列表:
  - 01_需求概述 (pageId: 272188760)
  - 02_登录注册 (pageId: 272189290)
  - ...
```

写入 `$outputDir\requirement-meta.md`。

#### 4.3 images/ 目录

- 保存所有下载的图片到 `$outputDir\images\`
- 文件名格式：`{序号}_{页面标题}_{图片描述}.{扩展名}`
- 例如：`01_需求概述_功能架构图.png`、`02_登录注册.png`、`02_登录注册_2.png`

### Step 5: 打包输出

将整个output目录打包成zip文件，发送给用户。

**打包命令**：
```powershell
# 打包整个 output 目录
$timestamp = Get-Date -Format "yyyy-MM-dd_HHmm"
$zipName = "confluence_export_$timestamp.zip"
$zipPath = "C:\Users\root\.openclaw\workspace\$zipName"

# 使用 PowerShell Compress-Archive
Compress-Archive -Path "C:\Users\root\.openclaw\workspace\output\*" -DestinationPath $zipPath -Force

# 验证打包结果
if (Test-Path $zipPath) {
    $zipSize = (Get-Item $zipPath).Length
    Write-Host "打包完成: $zipName (大小: $([math]::Round($zipSize/1MB, 2)) MB)"
} else {
    Write-Host "打包失败!" -ForegroundColor Red
}
```

**或者使用 7z（如果安装了中国）**：
```powershell
7z a -r "$zipPath" "C:\Users\root\.openclaw\workspace\output\*"
```

**输出文件后**：
- 将 zip 文件路径返回给用户
- 用户下载后可解压查看

## 注意事项

1. **使用sessions_spawn**：长时间任务必须使用sessions_spawn派发子任务并行处理

2. **图片直接下载**：
   - 访问 `viewpageattachments.action?pageId={pageId}` 获取附件列表
   - 使用 curl 携带登录 Cookie 直接下载图片原始文件
   - 保留原始格式（png/jpg/svg等）
   - 添加重试逻辑（建议3次）确保稳定性

3. **认证Cookie获取**：
   - 主session已登录，可以从browser获取Cookie
   - Cookie格式：`JSESSIONID=xxx; CONFLAuth=xxx`
   - 必须携带Cookie才能下载私有图片

4. **HTML转Markdown**：
   - 推荐使用 `markdownify` (Python) 或 `turndown` (Node.js)
   - 转换过程不得删除任何内容
   - 表格、代码块、图片引用需保持完整

5. **存储管理**：
   - 每次创建新目录前检查存储上限
   - 超过80%自动清理最早的目录和zip文件
   - 注意处理空目录的边界情况

6. **错误处理**：
   - 所有网络请求添加重试逻辑
   - 下载后验证文件大小
   - 记录错误日志以便排查

7. **不删减内容**：原文的每一个字都要保留
8. **保留格式**：表格、列表等都要完整保留
9. **层级准确**：严格按照Confluence的页面树层级整理
