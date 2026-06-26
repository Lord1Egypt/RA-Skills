# ATOM-FEISHU-031 - HTML 转飞书文档（含 Mermaid 截图）

> 版本：V1.0  
> 状态：**⚪ 已弃用**（2026-03-07 15:39）  
> 最后更新：2026-03-07 15:05  
> 触发词：**"转化为飞书文档" / "HTML 转飞书"**  
> **弃用原因：** Mermaid 截图效果不佳，用户决定手动处理

---

## 📋 动作定义

**名称：** HTML 转飞书文档（含 Mermaid 截图）  
**分类：** 交付层（Delivery Layer）  
**编号：** ATOM-FEISHU-031

**一句话描述：** 将 HTML 专家点评网页内容写入飞书文档，Mermaid 图表截图后插入

---

## 🎯 使用场景

**触发条件（需用户明确说）：**
- "转化为飞书文档"
- "HTML 转飞书"
- "把 HTML 内容同步到飞书"

**典型场景：**
- ✅ HTML 专家点评网页 → 飞书文档（协作共享）
- ✅ 架构图网页 → 飞书文档（含 Mermaid 截图）
- ✅ 本地报告 → 云端文档

---

## 📝 操作步骤

### 步骤 1：读取 HTML 文件内容

```powershell
# 读取 HTML 文件
$htmlPath = "architecture-atomic-skills-workflow.html"
$htmlContent = Get-Content $htmlPath -Raw

# 解析 HTML 提取主要内容
# - 标题
# - 各章节内容
# - Mermaid 图表代码
```

### 步骤 2：提取 Mermaid 图表并截图

```powershell
# 1. 用 Chrome 打开 HTML 文件
Start-Process "chrome.exe" -ArgumentList $htmlPath
Start-Sleep -Seconds 5  # 等待 Mermaid 渲染

# 2. 定位 Mermaid 图表区域
# 使用 browser 工具截图图表部分

# 3. 保存截图
$screenshotPath = "C:\Users\Xiabi\.openclaw\workspace\mermaid-screenshot.png"
# 截图保存
```

### 步骤 3：转换内容为 Markdown 格式

```powershell
# HTML → Markdown 转换
$mdContent = $htmlContent -replace '<[^>]+>', ''  # 移除 HTML 标签
$mdContent = $mdContent -replace '&nbsp;', ' '   # 转换 HTML 实体
$mdContent = $mdContent -replace '<br>', "`n"    # 转换换行

# 格式化标题
$mdContent = $mdContent -replace '<h1>(.*?)</h1>', '# $1'
$mdContent = $mdContent -replace '<h2>(.*?)</h2>', '## $1'
$mdContent = $mdContent -replace '<h3>(.*?)</h3>', '### $1'
```

### 步骤 4：分块写入飞书文档

```powershell
# 创建飞书文档
$createResult = feishu_doc -action create -title "架构图 - 原子动作工作流"
$docToken = $createResult.document_id

# 分块（≤200 blocks/块）
$blocks = $mdContent -split "`n"
$blockSize = 50
$chunks = @()
for ($i = 0; $i -lt $blocks.Count; $i += $blockSize) {
    $chunks += , $blocks[$i..([Math]::Min($i + $blockSize - 1, $blocks.Count - 1))]
}

# 第 1 块：write 模式
feishu_doc -action write -doc_token $docToken -content ($chunks[0] -join "`n")

# 后续块：append 模式
for ($i = 1; $i -lt $chunks.Count; $i++) {
    feishu_doc -action append -doc_token $docToken -content ($chunks[$i] -join "`n")
}
```

### 步骤 5：上传 Mermaid 截图并插入

```powershell
# 上传截图
$uploadResult = feishu_doc -action upload_image -doc_token $docToken -file_path $screenshotPath
$imageBlockId = $uploadResult.block_id

# 在对应位置插入图片
feishu_doc -action append -doc_token $docToken -content "`n![架构图]($($uploadResult.file_name))`n"
```

### 步骤 6：确认完成

```powershell
Write-Host "✅ HTML 转飞书文档完成！" -ForegroundColor Green
Write-Host "  文档 URL: https://feishu.cn/docx/$docToken" -ForegroundColor Cyan
Write-Host "  Mermaid 截图：已插入" -ForegroundColor Gray
```

---

## 🎯 输入输出

### 输入
- **类型：** HTML 文件路径
- **内容：** HTML 专家点评网页（含 Mermaid 图表）
- **必填：** 是

### 输出
- **类型：** 飞书文档
- **内容：** Markdown 格式 + Mermaid 截图
- **附加：** 文档 URL

---

## ⚙️ 偏好设置

### HTML 解析
- **提取：** 标题/章节/表格/列表
- **忽略：** CSS/JS/HTML 标签
- **保留：** 文字内容/结构

### Mermaid 处理
- **方式：** 截图（PNG）
- **质量：** 高清（保证文字清晰）
- **插入位置：** 对应章节下方

### 飞书写入
- **分块：** ≤200 blocks/块
- **模式：** 第 1 块 write，后续 append
- **格式：** Markdown

---

## 🔄 使用示例

### 示例 1：转化架构图 HTML

```
用户：把架构图 HTML 转化为飞书文档
  ↓
调用：ATOM-FEISHU-031
  ↓
处理：
  - 读取 HTML 内容
  - 截取 Mermaid 图表
  - 转换为 Markdown
  - 分块写入飞书
  - 插入截图
  ↓
输出：飞书文档（含架构图截图）
```

### 示例 2：转化专家点评 HTML

```
用户：把 expert-review-2026-03-07.html 转化为飞书文档
  ↓
调用：ATOM-FEISHU-031
  ↓
处理：同上
  ↓
输出：飞书文档（专家点评）
```

---

## 🔗 关联动作

### 前置动作
- ATOM-VISUAL-005：生成 HTML 文件

### 后置动作
- 无（转化完成即可）

### 复用原子动作
- ATOM-FEISHU-028：写入飞书文档（分块）
- ATOM-VISUAL-009：Chrome 打开文件

---

## ✅ 检查清单

执行前确认：
- [ ] HTML 文件存在
- [ ] Mermaid 图表已渲染
- [ ] 有飞书编辑权限
- [ ] 网络正常

执行后确认：
- [ ] 内容完整转换
- [ ] Mermaid 截图清晰
- [ ] 飞书文档可访问
- [ ] 分块写入成功

---

## ⚠️ 常见错误

### 错误 1：Mermaid 未渲染就截图

```
❌ 错误：打开 HTML 立即截图 → 空白图表
✅ 正确：等待 5 秒，让 Mermaid 渲染完成
```

### 错误 2：一次性写入飞书

```
❌ 错误：create -content "长内容" → 空白文档
✅ 正确：create → write → append（分块）
```

### 错误 3：HTML 标签未清理

```
❌ 错误：直接写入 HTML 代码
✅ 正确：转换为 Markdown 格式
```

---

## 💡 核心原则

> **HTML 转飞书 = 内容转换 + Mermaid 截图 + 分块写入**

**关键点：**
1. ✅ Mermaid 图表必须截图（飞书不支持渲染）
2. ✅ HTML 内容转 Markdown（飞书兼容）
3. ✅ 分块写入（避免 400 错误）

**触发词：**
- "转化为飞书文档"
- "HTML 转飞书"

---

## 📚 参考文档

- 关联动作：`ATOM-FEISHU-028 - 写入飞书文档`
- 关联动作：`ATOM-VISUAL-005 - 生成 HTML 文件`
- Skill：`skills/html-expert-review/SKILL.md`

---

_模块化定义 | 可独立调用 | HTML 转飞书 | 2026-03-07_
