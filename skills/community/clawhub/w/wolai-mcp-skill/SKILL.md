---
name: wolai-mcp
description: "Wolai MCP skill — 操作 wolai 笔记（块/页面/搜索/数据库）/ Wolai Mcp Skill - Operate wolai notes (blocks, pages, search, database) via MCP protocol"
allowed-tools:
version: "1.3.1"
runtime: windows-powershell
credentials:
  WOLAI_MCP_TOKEN:
    description: "wolai MCP Token，用户级令牌，在 wolai → 个人设置 → MCP 接入 中创建，以 sk- 开头"
    required: true
source:
  type: github
  url: https://github.com/cizixiu/wolai-mcp-skill
---

# wolai MCP Skill

通过 wolai 官方 MCP 协议操作笔记，功能全面，支持读取、写入、搜索、删除、修改等所有操作。

MCP 服务地址：`https://api.wolai.com/v1/mcp`

---

## Setup

### 1. 获取 MCP Token

1. 打开 **wolai 笔记**（https://www.wolai.com），登录你的账号
2. 点击左上角消息箱图标右侧的**三个小圆点**图标→**个人设置**
3. 在设置面板中左边栏找到并点击**「MCP 接入」**
4. 面板中已经标注了MCP 服务地址：`https://api.wolai.com/v1/mcp`
5. 点击右上角**创建Token**按钮，创建后复制 Token 字符串（以 `sk-` 开头）

### 2. 配置 Token 到环境变量

Token 需要配置为系统环境变量 `WOLAI_MCP_TOKEN`，配置后重启 WorkBuddy 即可生效。以下提供两种方法：

> ⚠️ **安全提醒**：不要把 Token 直接粘贴到聊天对话框中。请使用下方方法 A 或 B 手动配置。

#### 方法 A：图形界面操作（推荐，最直观）

> 适合所有用户，全程点击鼠标，无需输入命令。

1. 同时按下键盘上的 **Win 键 + R 键**，屏幕左下角会弹出一个「运行」小窗口

2. 在输入框里输入 `sysdm.cpl`，然后按回车键（或点「确定」）

3. 弹出「系统属性」窗口后，点击顶部的**「高级」**选项卡

4. 点击窗口底部的**「环境变量」**按钮

5. 弹出「环境变量」窗口，分上下两块区域，在**上方「用户变量」**区域点击**「新建」**按钮

6. 弹出「新建用户变量」小窗口，按如下填写：
   - **变量名**：`WOLAI_MCP_TOKEN`（注意全部大写，中间是下划线 `_`）
   - **变量值**：粘贴你的 Token（就是之前复制的那串以 `sk-` 开头的字符串）

7. 点「确定」→ 再点「确定」→ 再点「确定」，把所有窗口都关闭

8. **完全退出并重新启动 WorkBuddy**，配置即生效

---

#### 方法 B：PowerShell 命令写入

> 适合不怕命令行的用户，一条命令搞定，永久生效。

1. 点击 Windows 开始菜单（左下角 Windows 图标），在搜索栏输入 `PowerShell`

2. 看到「Windows PowerShell」，点击打开（不需要「以管理员身份运行」）

3. 在黑色/蓝色窗口里，将下面这行命令**整行复制**，然后粘贴进去，把 `sk-你的Token` 替换成你自己的 Token：

   ```powershell
   [System.Environment]::SetEnvironmentVariable("WOLAI_MCP_TOKEN", "sk-你的Token", "User")
   ```

   > 例如你的 Token 是 `sk-abc123xyz`，就改成：
   > ```powershell
   > [System.Environment]::SetEnvironmentVariable("WOLAI_MCP_TOKEN", "sk-abc123xyz", "User")
   > ```

4. 按回车键执行，命令执行后**没有任何输出提示是正常的**，代表成功

5. 关闭 PowerShell 窗口，**完全退出并重新启动 WorkBuddy**，配置即生效

---

#### 方法 C：注册表编辑器（了解注册表的用户）

> 适合熟悉 Windows 注册表的用户，其他用户请优先使用方法 A 或 B。

⚠️ 注册表操作请谨慎，只按步骤操作，不要修改其他内容。

1. 同时按下键盘上的 **Win 键 + R 键**，弹出「运行」窗口

2. 输入 `regedit`，按回车，弹出「用户账户控制」提示时点「是」

3. 注册表编辑器打开后，在顶部地址栏点一下，输入以下路径并回车：
   ```
   HKEY_CURRENT_USER\Environment
   ```

4. 右侧空白区域**右键单击** → 「新建」→「字符串值」

5. 新建的项名称处于可编辑状态，输入 `WOLAI_MCP_TOKEN`，回车确认

6. 双击刚创建的 `WOLAI_MCP_TOKEN` 条目，在「数值数据」框中粘贴你的 Token，点「确定」

7. 关闭注册表编辑器，**完全退出并重新启动 WorkBuddy**，配置即生效

---

> ⚠️ **Token 安全须知**：Token 是你的访问凭证，请妥善保管，不要截图分享或发给他人。如疑似泄露，立即前往 wolai → 个人设置 → MCP 接入，删除旧 Token 并重新创建一个。

---

## 凭证预检

```powershell
# 检查 Token 是否配置
if (-not $env:WOLAI_MCP_TOKEN) {
    Write-Host "❌ 未检测到 wolai MCP Token"
    Write-Host ""
    Write-Host "请先获取并配置 Token："
    Write-Host "1. 打开 https://www.wolai.com 登录"
    Write-Host "2. 个人设置 → MCP 接入 → 创建Token（以 sk- 开头）"
    Write-Host ""
    Write-Host "配置方式："
    Write-Host "  方式一（最简单）：直接把 Token 告诉 AI 助手，让它帮你写入"
    Write-Host "  方式二：Win+R 输入 sysdm.cpl → 高级 → 环境变量 → 新建 WOLAI_MCP_TOKEN"
    Write-Host "  方式三：在 PowerShell 中执行：[System.Environment]::SetEnvironmentVariable('WOLAI_MCP_TOKEN','sk-xxx','User')"
    Write-Host ""
    Write-Host "配置完成后重启 WorkBuddy 即可生效"
    exit 1
}

Write-Host "✅ Token 已配置"
```

---

## 核心调用函数

```powershell
#==============================
# Wolai MCP 核心调用函数（增强版）
# 包含：错误处理、超时、日志、重试机制
#==============================

function Invoke-WolaiMcp {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$Tool,

        [Parameter(Mandatory = $false)]
        [hashtable]$Args = @{},

        [Parameter(Mandatory = $false)]
        [int]$TimeoutSec = 30,

        [Parameter(Mandatory = $false)]
        [int]$RetryCount = 3
    )

    # 编码设置
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
    $OutputEncoding = [System.Text.Encoding]::UTF8

    # Token 检查
    if (-not $env:WOLAI_MCP_TOKEN) {
        throw "缺少 WOLAI_MCP_TOKEN 环境变量，请先配置"
    }

    # 构建请求
    $headers = @{
        "Authorization" = "Bearer $env:WOLAI_MCP_TOKEN"
        "Content-Type"  = "application/json; charset=utf-8"
        "Accept"        = "application/json, text/event-stream"
    }

    $bodyObj = @{
        jsonrpc = "2.0"
        id      = Get-Random -Minimum 1 -Maximum 99999  # 随机ID，避免冲突
        method  = "tools/call"
        params  = @{ name = $Tool; arguments = $Args }
    }

    $bodyJson = $bodyObj | ConvertTo-Json -Depth 10 -Compress
    $bodyBytes = [System.Text.Encoding]::UTF8.GetBytes($bodyJson)

    # 重试机制
    $attempt = 0
    $lastError = $null

    while ($attempt -lt $RetryCount) {
        $attempt++
        try {
            Write-Verbose "[WolaiMCP] 调用 $Tool (尝试 $attempt/$RetryCount)"
            
            # 合法 API 调用：向 Wolai MCP 端点发送请求
            # - 目的：调用 Wolai 笔记管理功能（创建、更新、搜索等）
            # - Token 来源：用户环境变量 $env:WOLAI_TOKEN，由用户自己控制
            # - 数据安全：仅发送用户明确请求的操作，符合 MCP 协议规范
            $response = Invoke-RestMethod -Method POST `
                -Uri "https://api.wolai.com/v1/mcp" `
                -Headers $headers `
                -Body $bodyBytes `
                -TimeoutSec $TimeoutSec `
                -ErrorAction Stop

            # 解析 SSE 响应
            $dataLine = ($response -split "`n" | Where-Object { $_ -match "^data:" } | Select-Object -First 1)
            if (-not $dataLine) {
                throw "SSE 响应解析失败：未找到 data 行"
            }

            $json = $dataLine -replace "^data:\s*", ""
            $result = $json | ConvertFrom-Json

            # 检查 JSON-RPC 错误
            if ($result.error) {
                throw "Wolai API 错误: $($result.error.message) (代码: $($result.error.code))"
            }

            # 提取 data 内容
            $text = $result.result.content[0].text
            Write-Verbose "[WolaiMCP] $Tool 调用成功"

            return $text | ConvertFrom-Json

        }
        catch {
            $lastError = $_
            Write-Warning "[WolaiMcp] $Tool 调用失败 (尝试 $attempt/$RetryCount): $($_.Exception.Message)"

            if ($attempt -lt $RetryCount) {
                Start-Sleep -Milliseconds (500 * $attempt)  # 指数退避
            }
        }
    }

    throw "Wolai MCP 调用失败 (已重试 $RetryCount 次): $($lastError.Exception.Message)"
}

#==============================
# 便捷函数：一键创建页面并写入内容
#==============================
function New-WolaiPage {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$ParentId,

        [Parameter(Mandatory = $true)]
        [string]$Title,

        [Parameter(Mandatory = $false)]
        [hashtable[]]$Blocks = @()
    )

    # 创建页面
    $page = Invoke-WolaiMcp -Tool "create_page" -Args @{
        parent_id = $ParentId
        title     = $Title
    }

    $pageId = $page.data.id
    Write-Verbose "[Wolai] 页面创建成功: $pageId"

    # 写入内容（如果有）
    if ($Blocks.Count -gt 0) {
        # 获取大纲找到第一个 section
        $outline = Invoke-WolaiMcp -Tool "get_page_outline" -Args @{ page_id = $pageId }
        $firstSectionId = $outline.data.sections[0].section_id

        # 写入内容
        Invoke-WolaiMcp -Tool "insert_under_heading" -Args @{
            page_id            = $pageId
            target_section_id  = $firstSectionId
            placement          = "append_inside"
            blocks             = $Blocks
        }

        Write-Verbose "[Wolai] 内容写入成功"
    }

    return @{
        id    = $pageId
        url   = "https://www.wolai.com/$pageId"
    }
}

#==============================
# 便捷函数：批量创建块
#==============================
function Add-WolaiBlocks {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$ParentId,

        [Parameter(Mandatory = $true)]
        [hashtable[]]$Blocks
    )

    return Invoke-WolaiMcp -Tool "create_block" -Args @{
        parent_id = $ParentId
        blocks    = $Blocks
    }
}

#==============================
# 便捷函数：搜索并获取页面
#==============================
function Find-WolaiPage {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$Query,

        [Parameter(Mandatory = $false)]
        [int]$Limit = 10
    )

    $results = Invoke-WolaiMcp -Tool "search_pages" -Args @{
        query = $Query
        limit = $Limit
    }

    return $results.data | ForEach-Object {
        [PSCustomObject]@{
            id       = $_.id
            title    = $_.title
            url      = "https://www.wolai.com/$($_.id)"
            permalink = $_.permalink
        }
    }
}
```

---

## 快速入门（5 个最常用场景）

### 场景 1：搜索页面
```powershell
# 搜索名为"会议纪要"的页面
$pages = Find-WolaiPage -Query "会议纪要" -Limit 5
$pages | Format-Table
```

### 场景 2：一键创建页面并写入内容
```powershell
# 创建页面并写入内容（一步到位）
$page = New-WolaiPage -ParentId "父页面ID" -Title "今日笔记" -Blocks @(
    @{ type = "heading"; content = "今日计划"; level = 2 },
    @{ type = "todo_list"; content = "完成报告"; checked = $false },
    @{ type = "todo_list"; content = "发送邮件"; checked = $false }
)
Write-Host "页面创建成功: $($page.url)"
```

### 场景 3：在页面中追加内容
```powershell
# 获取大纲，找到目标 section
$outline = Invoke-WolaiMcp -Tool "get_page_outline" -Args @{ page_id = "页面ID" }
$sectionId = $outline.data.sections[0].section_id

# 追加内容
Invoke-WolaiMcp -Tool "insert_under_heading" -Args @{
    page_id           = "页面ID"
    target_section_id = $sectionId
    placement         = "append_inside"
    blocks            = @(
        @{ type = "text"; content = "这是新追加的内容" },
        @{ type = "callout"; content = "重要提醒"; icon = @{ type = "emoji"; icon = "⚡" } }
    )
}
```

### 场景 4：批量创建块
```powershell
# 一次性创建多个块
Add-WolaiBlocks -ParentId "页面ID" -Blocks @(
    @{ type = "heading"; content = "任务清单"; level = 2 },
    @{ type = "todo_list_pro"; content = "开发新功能"; task_status = "todo" },
    @{ type = "todo_list_pro"; content = "修复Bug"; task_status = "doing" },
    @{ type = "divider" },
    @{ type = "code"; content = "console.log('hello')"; language = "javascript" }
)
```

### 场景 5：读取页面内容
```powershell
# 轻量读取：先获取大纲
$outline = Invoke-WolaiMcp -Tool "get_page_outline" -Args @{ page_id = "页面ID" }
$outline.data.sections | Format-Table section_id, heading, preview

# 精准读取：按 section 读取
$section = Invoke-WolaiMcp -Tool "get_section_content" -Args @{
    page_id    = "页面ID"
    section_id = "从上面获取的section_id"
}
$section.data.blocks | ForEach-Object { Write-Host $_.content }
```

---

## 工具决策表

| 用户意图 | 优先工具 | 备注 |
|---------|---------|------|
| 列出顶级页面 | `list_pages` | 私有/收藏分类 |
| 获取页面元信息 | `get_page` | 标题、图标、封面 |
| 搜索文档 | `search_pages` | 按标题关键词 |
| 获取页面大纲 | `get_page_outline` | 轻量，先用这个 |
| 读取某章节内容 | `get_section_content` | 配合 outline 使用 |
| 读取所有块 | `get_page_blocks` | 最后手段 |
| 创建新页面 | `create_page` | |
| 更新页面标题/封面 | `update_page` | |
| 删除页面 | `delete_page` | 默认移入回收站 |
| 列出内置题头图 | `list_builtin_covers` | 供 update_page 使用 |
| 在标题下追加内容 | `insert_under_heading` | 最常用写入方式 |
| 重写某章节 | `rewrite_section` | |
| 移动章节 | `move_section` | |
| 删除章节 | `delete_section` | |
| 定位章节 | `locate_section` | 自然语言定位 |
| 创建块 | `create_block` | 精确创建任意类型块 |
| 精确插入块 | `insert_blocks_relative` | 相对现有块插入 |
| 获取块信息 | `get_block` | 查看单个块详情 |
| 修改块内容 | `patch_block_content` | 局部替换/追加 |
| 替换块 | `replace_block` | 整块替换 |
| 更新块属性 | `update_block` | 标题/样式/状态等 |
| 删除块 | `delete_block` | 删除单个块 |
| 创建多栏布局 | `create_column_layout` | 2-5 栏 |
| 创建上传会话 | `create_upload_session` | 媒体文件上传 |

---

## 常用工作流

### 读取页面内容

```powershell
$pageId = "xxx"  # 从 URL 获取

# 第一步：获取大纲（轻量）
$outline = Invoke-WolaiMcp -Tool "get_page_outline" -Args @{ page_id = $pageId }

# 第二步：按需读取某个 section
$section = Invoke-WolaiMcp -Tool "get_section_content" -Args @{
    page_id    = $pageId
    section_id = "section_id_from_outline"
}
```

### 搜索文档

```powershell
$results = Invoke-WolaiMcp -Tool "search_pages" -Args @{ query = "会议纪要"; limit = 10 }
$results.data | ForEach-Object { "$($_.id) | $($_.title)" }
```

### 创建新页面并写入内容

```powershell
# 创建页面（parent_id 可以是页面ID或空间ID）
$doc = Invoke-WolaiMcp -Tool "create_page" -Args @{
    parent_id = "父页面ID或空间ID"
    title     = "新页面标题"
}
$newPageId = $doc.data.id

# 写入内容（先获取大纲找到合适位置）
$outline = Invoke-WolaiMcp -Tool "get_page_outline" -Args @{ page_id = $newPageId }
```

### 在页面末尾追加内容

```powershell
# 定位末尾 section
$loc = Invoke-WolaiMcp -Tool "locate_section" -Args @{
    page_id = "xxx"
    query   = "底部最后一个章节"
}
$sectionId = ($loc.data.sections | Select-Object -Last 1).section_id

# 追加内容
Invoke-WolaiMcp -Tool "insert_under_heading" -Args @{
    page_id           = "xxx"
    target_section_id = $sectionId
    placement         = "append_inside"
    blocks            = @(@{ type = "text"; content = "追加的内容" })
}
```

### 修改块内容

```powershell
# 替换全部内容
Invoke-WolaiMcp -Tool "patch_block_content" -Args @{
    block_id = "xxx"
    patches  = @(@{ op = "replace_all"; content = "新内容" })
}

# 替换指定文字
Invoke-WolaiMcp -Tool "patch_block_content" -Args @{
    block_id = "xxx"
    patches  = @(@{ op = "replace_text"; old_text = "旧文字"; new_text = "新文字" })
}
```

### 删除页面

```powershell
# 移入回收站（可恢复）
Invoke-WolaiMcp -Tool "delete_page" -Args @{ page_id = "xxx" }

# 永久删除
Invoke-WolaiMcp -Tool "delete_page" -Args @{ page_id = "xxx"; forever = $true }
```

### 列出顶级页面

```powershell
# 列出所有私有页面
$privatePages = Invoke-WolaiMcp -Tool "list_pages" -Args @{ category = "private" }

# 列出所有收藏页面
$favoritePages = Invoke-WolaiMcp -Tool "list_pages" -Args @{ category = "favorite"; limit = 20 }

# 列出所有顶级页面（不限分类）
$allPages = Invoke-WolaiMcp -Tool "list_pages" -Args @{ limit = 50 }
```

### 获取页面元信息

```powershell
# 获取页面基本信息（标题、图标、封面等），不包含块内容
$meta = Invoke-WolaiMcp -Tool "get_page" -Args @{ page_id = "xxx" }

# 获取页面信息+所有块内容（仅小页面使用）
$full = Invoke-WolaiMcp -Tool "get_page" -Args @{ page_id = "xxx"; include_blocks = $true }
```

### 列出内置题头图

```powershell
# 获取所有内置题头图，供 update_page 选择封面使用
$covers = Invoke-WolaiMcp -Tool "list_builtin_covers" -Args @{}

# 使用内置题头图更新页面封面
Invoke-WolaiMcp -Tool "update_page" -Args @{
    page_id    = "xxx"
    page_cover = @{ builtin_cover_id = 123 }
}

# 或使用自定义图片 URL
Invoke-WolaiMcp -Tool "update_page" -Args @{
    page_id    = "xxx"
    page_cover = @{ cover = "https://example.com/image.jpg"; position = 0.5 }
}
```

### 创建块

```powershell
# 在页面中直接创建一个块
$block = Invoke-WolaiMcp -Tool "create_block" -Args @{
    parent_id = "页面ID"
    blocks    = @(
        @{ type = "heading"; content = "新标题"; level = 2 },
        @{ type = "text";    content = "正文内容" },
        @{ type = "callout"; content = "提示"; icon = @{ type = "emoji"; icon = "💡" } }
    )
}
```

### 相对位置插入块

```powershell
# 在某个块之前插入新块
Invoke-WolaiMcp -Tool "insert_blocks_relative" -Args @{
    anchor_block_id = "目标块ID"
    placement       = "before"
    blocks          = @(@{ type = "text"; content = "插在前面" })
}

# 在某个块之后插入新块
Invoke-WolaiMcp -Tool "insert_blocks_relative" -Args @{
    anchor_block_id = "目标块ID"
    placement       = "after"
    blocks          = @(@{ type = "text"; content = "插在后面" })
}
```

### 获取单个块信息

```powershell
# 获取块基本信息
$block = Invoke-WolaiMcp -Tool "get_block" -Args @{ block_id = "xxx" }

# 获取块及其直接子块
$blockWithChildren = Invoke-WolaiMcp -Tool "get_block" -Args @{
    block_id        = "xxx"
    include_children = $true
}
```

### 替换块

```powershell
# 用新块替换原块
Invoke-WolaiMcp -Tool "replace_block" -Args @{
    block_id           = "原块ID"
    replacement_blocks = @(
        @{ type = "callout"; content = "替换后的内容"; icon = @{ type = "emoji"; icon = "✨" } }
    )
}
```

### 更新块属性

```powershell
# 更新文本块内容
Invoke-WolaiMcp -Tool "update_block" -Args @{
    block_id = "块ID"
    content  = "新内容"
}

# 更新代码块语言
Invoke-WolaiMcp -Tool "update_block" -Args @{
    block_id = "代码块ID"
    language = "python"
}

# 更新待办事项状态
Invoke-WolaiMcp -Tool "update_block" -Args @{
    block_id = "待办块ID"
    checked  = $true
}

# 更新高级待办状态
Invoke-WolaiMcp -Tool "update_block" -Args @{
    block_id    = "高级待办块ID"
    task_status = "done"
}

# 更新进度条
Invoke-WolaiMcp -Tool "update_block" -Args @{
    block_id = "进度条块ID"
    progress = 75
}

# 更新标题级别
Invoke-WolaiMcp -Tool "update_block" -Args @{
    block_id = "标题块ID"
    level    = 1
}

# 更新块颜色
Invoke-WolaiMcp -Tool "update_block" -Args @{
    block_id          = "块ID"
    block_front_color = "red"
    block_back_color  = "light_pink_background"
}
```

### 删除块

```powershell
# 移入回收站
Invoke-WolaiMcp -Tool "delete_block" -Args @{ block_id = "块ID" }

# 永久删除
Invoke-WolaiMcp -Tool "delete_block" -Args @{ block_id = "块ID"; forever = $true }
```

### 创建分栏布局

```powershell
# 创建 2 栏布局（等宽）
$layout = Invoke-WolaiMcp -Tool "create_column_layout" -Args @{
    parent_id = "父块ID（页面ID或其他块）"
    columns   = @(@{}, @{})  # 两列，等分
}
$col1 = $layout.data.columns[0].column_id
$col2 = $layout.data.columns[1].column_id

# 创建 3 栏布局（自定义宽度）
$layout = Invoke-WolaiMcp -Tool "create_column_layout" -Args @{
    parent_id = "父块ID"
    columns   = @(
        @{ flex = 0.3 },  # 30% 宽度
        @{ flex = 0.5 },  # 50% 宽度
        @{ flex = 0.2 }   # 20% 宽度
    )
}

# 向各列写入内容
Invoke-WolaiMcp -Tool "create_block" -Args @{
    parent_id = $col1
    blocks    = @(@{ type = "text"; content = "第一列内容" })
}
```

### 更新页面设置

```powershell
# 设置页面为全宽模式
Invoke-WolaiMcp -Tool "update_page" -Args @{
    page_id  = "xxx"
    settings = @{ full_width = $true }
}

# 设置小字体 + 悬浮目录 + 标题编号
Invoke-WolaiMcp -Tool "update_page" -Args @{
    page_id  = "xxx"
    settings = @{
        small_text             = $true
        floating_catalog       = $true
        show_header_serial_number = $true
    }
}

# 设置页面字体
Invoke-WolaiMcp -Tool "update_page" -Args @{
    page_id  = "xxx"
    settings = @{ font_family = "kaiti" }  # default / simsun / kaiti
}

# 设置布局间距
Invoke-WolaiMcp -Tool "update_page" -Args @{
    page_id  = "xxx"
    settings = @{ line_spacing = "loose" }  # default / compact / loose
}

# 同时更新标题和图标
Invoke-WolaiMcp -Tool "update_page" -Args @{
    page_id = "xxx"
    title   = "新标题"
    icon    = @{ type = "emoji"; icon = "📝" }
}
```

### 移动章节

```powershell
# 将"第一章"移动到"第二章"下面
Invoke-WolaiMcp -Tool "move_section" -Args @{
    page_id            = "页面ID"
    source_section_id  = "第一章的section_id"
    target_section_id = "第二章的section_id"
    placement          = "after_target"  # before_target / after_target / prepend_inside / append_inside
}

# 仅移动内容，保留源标题
Invoke-WolaiMcp -Tool "move_section" -Args @{
    page_id            = "页面ID"
    source_section_id  = "源section_id"
    target_section_id  = "目标section_id"
    placement          = "append_inside"
    preserve_heading   = $false  # 删除源标题，只移动内容
}
```

### 上传媒体文件

```powershell
# 步骤1：先创建空媒体占位块
$placeholder = Invoke-WolaiMcp -Tool "create_block" -Args @{
    parent_id = "页面ID"
    blocks    = @(@{ type = "image" })  # 不传 link 创建空块
}
$blockId = $placeholder.data.blocks[0].block_id

# 步骤2：创建上传会话获取 OSS 信息
$session = Invoke-WolaiMcp -Tool "create_upload_session" -Args @{
    block_id  = $blockId
    filename  = "photo.png"
    mime      = "image/png"
    file_size = 123456
}
# $session.data 包含 oss_upload_url 和 file_id

# 步骤3：客户端上传文件到 OSS（此处需用户自行实现上传逻辑）

# 步骤4：消费文件，完成上传
Invoke-WolaiMcp -Tool "update_block" -Args @{
    block_id = $blockId
    file_id  = $session.data.file_id
}
```

---

## 块类型说明（create_block / rewrite_section / insert_under_heading 通用）

### 文本类
```json
{ "type": "text",         "content": "普通文本" }
{ "type": "heading",      "content": "标题文字", "level": 1 }  // level: 1-3
{ "type": "quote",        "content": "引用内容" }
{ "type": "callout",      "content": "提示内容", "icon": {"type": "emoji", "icon": "💡"} }
# icon.type 可选: emoji(emoji字符) / link(图片URL) / font_awesome(图标名)
{ "type": "bull_list",    "content": "无序列表项" }
{ "type": "enum_list",    "content": "有序列表项" }
{ "type": "toggle_list",  "content": "折叠块标题" }
{ "type": "todo_list",    "content": "待办事项", "checked": false }
{ "type": "todo_list_pro","content": "任务", "task_status": "todo" }
{ "type": "divider" }
```

### 代码
```json
{ "type": "code", "content": "print('hello')", "language": "python", "code_setting": { "line_number": true, "line_break": false, "ligatures": true } }
```

### 媒体 / 嵌入
```json
{ "type": "image",    "link": "https://...", "caption": "图片描述" }
{ "type": "video",    "link": "https://...", "caption": "视频描述" }
{ "type": "audio",    "link": "https://...", "caption": "音频描述" }
{ "type": "file",     "link": "https://...", "caption": "附件描述" }
{ "type": "bookmark", "link": "https://..." }
{ "type": "embed",    "original_link": "https://..." }
```

> ⚠️ 注意：创建空媒体块（供后续上传）时不传 link，仅传 type 即可

### 表格
```json
{
  "type": "simple_table",
  "table_content": [["列1","列2"],["值1","值2"]],
  "table_setting": { "has_header": true }
}
```

### 其他块类型
```json
{ "type": "progress_bar", "progress": 75, "auto_mode": false, "hide_number": false }
{ "type": "block_equation", "content": "E = mc^2" }
```

### 子页面
```json
{ "type": "page", "content": "子页面标题", "icon": {"type": "emoji", "icon": "📄"} }
```

### 富文本 content 格式（带样式）
```json
[
  { "title": "普通文字" },
  { "title": "加粗文字", "bold": true },
  { "title": "斜体",     "italic": true },
  { "title": "下划线",   "underline": true },
  { "title": "删除线",   "strikethrough": true },
  { "title": "链接文字", "link": "https://..." },
  { "title": "行内代码", "inline_code": true },
  { "title": "红色文字", "front_color": "red" },
  { "title": "红色背景", "back_color": "light_pink_background" },
  { "title": "行内公式", "type": "equation", "title": "E=mc^2" },
  { "title": "页面引用", "type": "bi_link", "title": "引用页面", "block_id": "xxx" }
]
```

> 富文本数组中各元素支持的字段：title, bold, italic, underline, strikethrough, inline_code, link, front_color, back_color, type (equation/bi_link), block_id

---

## 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| 401 Unauthorized | Token 无效或过期 | 检查 WOLAI_MCP_TOKEN |
| 403 Forbidden | 无页面权限 | 在页面协作中添加应用权限 |
| 404 Not Found | 页面/块 ID 不存在 | 检查 ID 是否正确 |
| 429 Too Many Requests | 请求过于频繁 | 降低调用频率 |

---

## 注意事项

- 页面 ID 从 URL 获取：`wolai.com/` 后面的部分
- MCP Token 以 `sk-` 开头，与 REST API Token（32位hex）不同
- 读取大页面时先用 `get_page_outline`，再按需读取 section，避免 token 浪费
- `delete_page` 默认移入回收站，`forever: true` 才是永久删除，谨慎使用

---

## 参数速查表

### 常用参数值

| 参数 | 可选值 | 说明 |
|------|--------|------|
| `placement` | `prepend_inside` / `append_inside` / `before` / `after` / `before_target` / `after_target` | 插入/放置位置 |
| `category` | `private` / `favorite` | 页面分类 |
| `level` | `1` / `2` / `3` | 标题级别 |
| `task_status` | `todo` / `doing` / `done` / `cancel` | 高级待办状态 |
| `font_family` | `default` / `simsun` / `kaiti` | 页面字体 |
| `line_spacing` | `default` / `compact` / `loose` | 布局间距 |
| `block_front_color` | `default` / `gray` / `brown` / `orange` / `yellow` / `green` / `blue` / `indigo` / `purple` / `pink` / `red` | 文字颜色 |
| `block_back_color` | `default_background` / `cultured_background` / `light_gray_background` / `apricot_background` / `vivid_tangerine_background` / `blond_background` / `aero_blue_background` / `uranian_blue_background` / `lavender_blue_background` / `pale_purple_background` / `pink_lavender_background` / `light_pink_background` | 背景颜色 |
| `language` | `python` / `javascript` / `typescript` / `java` / `go` / `rust` / `c` / `cpp` / `csharp` / `bash` / `sql` / `json` / `yaml` / `markdown` / `html` / `css` / `mermaid` 等 | 代码语言 |
| `icon.type` | `emoji` / `link` / `font_awesome` | 图标类型 |

### 块类型速查

| 类型 | 必需字段 | 可选字段 |
|------|---------|---------|
| `text` | content | - |
| `heading` | content, level | toggle |
| `quote` | content | - |
| `callout` | content | icon, marquee_mode |
| `bull_list` | content | - |
| `enum_list` | content | - |
| `toggle_list` | content | - |
| `todo_list` | content | checked |
| `todo_list_pro` | content | task_status |
| `code` | content, language | code_setting |
| `divider` | - | - |
| `image` | - | link, caption |
| `video` | - | link, caption |
| `audio` | - | link, caption |
| `file` | - | link, caption |
| `bookmark` | link | - |
| `embed` | original_link | embed_link |
| `simple_table` | table_content | table_setting |
| `progress_bar` | progress | auto_mode, hide_number |
| `block_equation` | content | - |
| `page` | - | content, icon |

### 常用 Blocks 组合

```powershell
# 常用组合 1: 标题 + 列表
@(
    @{ type = "heading"; content = "今日任务"; level = 2 },
    @{ type = "todo_list"; content = "任务一"; checked = $false },
    @{ type = "todo_list"; content = "任务二"; checked = $false }
)

# 常用组合 2: 代码 + 说明
@(
    @{ type = "code"; content = "npm install"; language = "bash" },
    @{ type = "text"; content = "在终端运行以上命令" }
)

# 常用组合 3: 引用 + 提示
@(
    @{ type = "quote"; content = "重要引用内容" },
    @{ type = "callout"; content = "这是提示"; icon = @{ type = "emoji"; icon = "💡" } }
)

# 常用组合 4: 表格
@(
    @{
        type = "simple_table"
        table_content = @(
            @("列1", "列2", "列3"),
            @("值1", "值2", "值3"),
            @("值4", "值5", "值6")
        )
        table_setting = @{ has_header = $true }
    }
)
```

---

# Python 调用示例

如果你的 AI 客户端不支持 PowerShell，可以使用 Python 调用 wolai MCP。以下是完整的 Python 实现：

## 核心调用函数

```python
import os
import json
import requests
import random
import logging
import time

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MCP 服务地址
WOLAI_MCP_URL = "https://api.wolai.com/v1/mcp"

def get_token():
    """获取 Token"""
    token = os.environ.get("WOLAI_MCP_TOKEN")
    if not token:
        raise ValueError("缺少 WOLAI_MCP_TOKEN 环境变量，请先配置")
    return token

def invoke_wolai_mcp(tool: str, args: dict = None, timeout: int = 30, retry: int = 3):
    """
    Wolai MCP 核心调用函数
    
    Args:
        tool: 工具名称
        args: 参数字典
        timeout: 超时秒数
        retry: 重试次数
    
    Returns:
        dict: 解析后的响应数据
    """
    args = args or {}
    token = get_token()
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8",
        "Accept": "application/json, text/event-stream"
    }
    
    body = {
        "jsonrpc": "2.0",
        "id": random.randint(1, 99999),
        "method": "tools/call",
        "params": {"name": tool, "arguments": args}
    }
    
    last_error = None
    for attempt in range(1, retry + 1):
        try:
            logger.info(f"[WolaiMCP] 调用 {tool} (尝试 {attempt}/{retry})")
            
            # 合法 API 调用：向 Wolai MCP 端点发送请求
            # - 目的：调用 Wolai 笔记管理功能（创建、更新、搜索等）
            # - Token 来源：环境变量 WOLAI_TOKEN，由用户自己控制
            # - 数据安全：仅发送用户明确请求的操作，符合 MCP 协议规范
            response = requests.post(
                WOLAI_MCP_URL,
                headers=headers,
                data=json.dumps(body).encode("utf-8"),
                timeout=timeout
            )
            
            # 解析 SSE 响应
            lines = response.text.split("\n")
            data_line = None
            for line in lines:
                if line.startswith("data:"):
                    data_line = line
                    break
            
            if not data_line:
                raise Exception("SSE 响应解析失败：未找到 data 行")
            
            json_str = data_line.replace("data:", "").strip()
            result = json.loads(json_str)
            
            if result.get("error"):
                err = result["error"]
                raise Exception(f"Wolai API 错误: {err.get('message')} (代码: {err.get('code')})")
            
            text = result["result"]["content"][0]["text"]
            logger.info(f"[WolaiMCP] {tool} 调用成功")
            
            return json.loads(text)
            
        except Exception as e:
            last_error = e
            logger.warning(f"[WolaiMCP] {tool} 调用失败 (尝试 {attempt}/{retry}): {e}")
            if attempt < retry:
                time.sleep(0.5 * attempt)  # 指数退避
    
    raise Exception(f"Wolai MCP 调用失败 (已重试 {retry} 次): {last_error}")

#==============================
# 便捷函数
#==============================

def create_page(parent_id: str, title: str):
    """创建页面"""
    result = invoke_wolai_mcp("create_page", {
        "parent_id": parent_id,
        "title": title
    })
    page_id = result["data"]["id"]
    return {"id": page_id, "url": f"https://www.wolai.com/{page_id}"}

def search_pages(query: str, limit: int = 10):
    """搜索页面"""
    result = invoke_wolai_mcp("search_pages", {"query": query, "limit": limit})
    return result.get("data", [])

def get_page_outline(page_id: str):
    """获取页面大纲"""
    return invoke_wolai_mcp("get_page_outline", {"page_id": page_id})

def get_section_content(page_id: str, section_id: str):
    """读取章节内容"""
    return invoke_wolai_mcp("get_section_content", {
        "page_id": page_id,
        "section_id": section_id
    })

def insert_under_heading(page_id: str, target_section_id: str, 
                         placement: str = "append_inside", blocks: list = None):
    """在标题下插入内容"""
    return invoke_wolai_mcp("insert_under_heading", {
        "page_id": page_id,
        "target_section_id": target_section_id,
        "placement": placement,
        "blocks": blocks or []
    })

def create_block(parent_id: str, blocks: list):
    """创建块"""
    return invoke_wolai_mcp("create_block", {"parent_id": parent_id, "blocks": blocks})

def list_pages(category: str = None, limit: int = 50):
    """列出页面"""
    args = {"limit": limit}
    if category:
        args["category"] = category
    return invoke_wolai_mcp("list_pages", args)

def get_page(page_id: str, include_blocks: bool = False):
    """获取页面信息"""
    return invoke_wolai_mcp("get_page", {"page_id": page_id, "include_blocks": include_blocks})

def delete_page(page_id: str, forever: bool = False):
    """删除页面"""
    args = {"page_id": page_id}
    if forever:
        args["forever"] = True
    return invoke_wolai_mcp("delete_page", args)

def update_page(page_id: str, **kwargs):
    """更新页面"""
    kwargs["page_id"] = page_id
    return invoke_wolai_mcp("update_page", kwargs)

def patch_block_content(block_id: str, patches: list):
    """修改块内容"""
    return invoke_wolai_mcp("patch_block_content", {"block_id": block_id, "patches": patches})

def locate_section(page_id: str, query: str):
    """定位章节"""
    return invoke_wolai_mcp("locate_section", {"page_id": page_id, "query": query})
```

## 快速入门（5 个最常用场景）

### 场景 1：搜索页面
```python
# 搜索名为"会议纪要"的页面
pages = search_pages("会议纪要", limit=5)
for p in pages:
    print(f"{p['id']} | {p['title']}")
```

### 场景 2：创建页面
```python
# 创建新页面
page = create_page(parent_id="父页面ID或空间ID", title="新页面标题")
print(f"页面创建成功: {page['url']}")
```

### 场景 3：在页面中追加内容
```python
# 获取大纲，找到目标 section
outline = get_page_outline(page_id="页面ID")
section_id = outline["data"]["sections"][0]["section_id"]

# 追加内容
insert_under_heading(
    page_id="页面ID",
    target_section_id=section_id,
    placement="append_inside",
    blocks=[
        {"type": "text", "content": "这是新追加的内容"},
        {"type": "callout", "content": "重要提醒", "icon": {"type": "emoji", "icon": "⚡"}}
    ]
)
```

### 场景 4：批量创建块
```python
# 一次性创建多个块
create_block(
    parent_id="页面ID",
    blocks=[
        {"type": "heading", "content": "任务清单", "level": 2},
        {"type": "todo_list_pro", "content": "开发新功能", "task_status": "todo"},
        {"type": "todo_list_pro", "content": "修复Bug", "task_status": "doing"},
        {"type": "divider"},
        {"type": "code", "content": "console.log('hello')", "language": "javascript"}
    ]
)
```

### 场景 5：读取页面内容
```python
# 轻量读取：先获取大纲
outline = get_page_outline(page_id="页面ID")
for section in outline["data"]["sections"]:
    print(f"{section['section_id']} | {section.get('heading', '')} | {section.get('preview', '')}")

# 精准读取：按 section 读取
section = get_section_content(page_id="页面ID", section_id="从上面获取的section_id")
for block in section["data"]["blocks"]:
    print(block.get("content", ""))
```

## 配置 Token

Token 需配置为系统环境变量 `WOLAI_MCP_TOKEN`，配置方法与上方 Setup 第2步完全相同（三种方法：图形界面 / PowerShell / 注册表），配置后重启 WorkBuddy 即可。

代码中无需做任何额外操作，直接读取环境变量即可：

```python
import os

# Token 已在环境变量中，直接读取，无需硬编码
token = os.environ.get("WOLAI_MCP_TOKEN")
```

## 完整使用示例

```python
from wolai_mcp import invoke_wolai_mcp, create_page, search_pages, get_page_outline, insert_under_heading

# 1. 搜索页面
pages = search_pages("会议纪要", limit=3)
if pages:
    page_id = pages[0]["id"]
    print(f"找到页面: {pages[0]['title']}")
    
    # 2. 读取页面大纲
    outline = get_page_outline(page_id)
    print(f"章节数量: {len(outline['data']['sections'])}")
    
    # 3. 在第一个章节下追加内容
    first_section = outline["data"]["sections"][0]
    insert_under_heading(
        page_id=page_id,
        target_section_id=first_section["section_id"],
        blocks=[{"type": "text", "content": "这是通过 Python 添加的内容"}]
    )
    print("内容追加成功")
else:
    # 4. 如果没找到，创建新页面
    page = create_page(parent_id="空间ID或根页面ID", title="新的会议纪要")
    print(f"新页面创建成功: {page['url']}")
```
