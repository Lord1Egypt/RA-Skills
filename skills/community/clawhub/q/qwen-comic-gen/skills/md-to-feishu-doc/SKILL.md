# MD 转飞书文档 - Markdown 转飞书云文档

_将本地 Markdown 文档转换为飞书云文档，支持手机端查看_

## 核心原则

**⚠️ 绝对不要用长文字写入飞书文档！**

- ❌ 错误：用 `feishu_doc --action write --content "长文本..."`
- ✅ 正确：用 `feishu_doc --action create` 创建文档，然后用 **blocks API 分段写入**

**原因：** 长文字会导致飞书 API 报错，返回空白文档！

---

## 使用场景

当完成调研/总结/报告类任务时：

1. 本地保存 MD 文档（备份）
2. 用本 skill 转换为飞书文档
3. 发送飞书链接给用户

---

## 标准流程（5 步）

### 步骤 1：读取本地 MD 文档

```powershell
$content = Get-Content "C:\Users\Xiabi\.openclaw\workspace\memory\项目知识总结.md" -Raw
```

### 步骤 2：创建飞书文档（空白）

**⚠️ 强制要求：必须设置 grant_to_requester: true**

```powershell
# 创建空白文档（必须设置 grant_to_requester: true）
$docId = feishu_doc --action create --title "文档标题" --grant_to_requester true
```

**参数说明：**
- `grant_to_requester: true` - 自动给文档创建者开通编辑权限
- 位置：顶层参数（与 title 同级）
- 作用：避免后续手动分享，Thomas 可以直接编辑

**验证方法：**
- 创建后检查返回：`"requester_permission_added": true`
- 打开文档确认有编辑权限

### 步骤 3：拆分 MD 内容为 blocks

**按章节拆分：**
- 每个 `# 标题` 作为一个 block
- 每个段落作为一个 block
- 表格单独作为 block

### 步骤 4：逐块写入飞书文档

```powershell
# 写入标题 block
feishu_doc --action append --doc_token $docId --block_type heading --text "标题"

# 写入正文 block
feishu_doc --action append --doc_token $docId --block_type text --text "正文内容"

# 写入表格 block
feishu_doc --action create_table --doc_token $docId --rows 5 --cols 3
```

### 步骤 5：发送飞书链接

```json
{
  "action": "send",
  "message": "📄 文档已创建：https://feishu.cn/docx/$docId"
}
```

---

## Block 类型对照表

| Markdown 元素 | 飞书 block 类型 | 说明 |
|--------------|---------------|------|
| `# 标题` | heading | 一级标题 |
| `## 子标题` | heading | 二级标题 |
| 段落 | text | 普通文本 |
| `**粗体**` | text | 支持 markdown 语法 |
| `- 列表` | bullet | 无序列表 |
| `1. 列表` | ordered | 有序列表 |
| `| 表格 |` | table | 表格（需单独创建） |
| ` ``` 代码 ` | code | 代码块 |
| `![图片]()` | image | 图片（需上传） |

---

## 完整示例

### 输入：MD 文档

```markdown
# 项目知识总结

## 1. 供应商直连系统

### 项目背景
管理 115 家供应商的产能数据...

### 当前痛点
- 预警准确性有待提升
- 数据字段命名不规范
```

### 输出：飞书文档（blocks 方式）

```powershell
# 1. 创建文档
$docId = feishu_doc --action create --title "项目知识总结"

# 2. 写入标题
feishu_doc --action append --doc_token $docId --block_type heading --text "项目知识总结"

# 3. 写入一级章节
feishu_doc --action append --doc_token $docId --block_type heading --text "1. 供应商直连系统"

# 4. 写入二级章节
feishu_doc --action append --doc_token $docId --block_type heading --text "项目背景"

# 5. 写入正文
feishu_doc --action append --doc_token $docId --block_type text --text "管理 115 家供应商的产能数据..."

# 6. 写入痛点（列表）
feishu_doc --action append --doc_token $docId --block_type bullet --text "预警准确性有待提升"
feishu_doc --action append --doc_token $docId --block_type bullet --text "数据字段命名不规范"
```

---

## 注意事项

### ⚠️ 避坑指南

1. **不要一次性写入长文本**
   - 错误：`--content "5000 字的长文本..."`
   - 正确：拆分成多个 block，每个 block < 500 字

2. **表格要单独处理**
   - 不能用 text block 写表格
   - 必须用 `create_table` + `write_table_cells`

3. **图片要上传**
   - 不能用 markdown 的图片语法
   - 必须用 `upload_image` 上传图片

4. **分批写入**
   - 每写 10 个 block 休息 1 秒（避免 rate limit）

### ✅ 最佳实践

1. **先创建空白文档**
2. **按章节顺序写入 blocks**
3. **表格/图片单独处理**
4. **最后发送链接给用户**

---

## 自动化脚本模板

```powershell
# MD 转飞书文档完整流程
param(
  [string]$mdPath,
  [string]$docTitle
)

# 1. 读取 MD 内容
$mdContent = Get-Content $mdPath -Raw

# 2. 创建飞书文档
$docToken = feishu_doc --action create --title $docTitle

# 3. 按行拆分
$lines = Get-Content $mdPath

# 4. 逐行写入
foreach ($line in $lines) {
  if ($line.StartsWith("# ")) {
    feishu_doc --action append --doc_token $docToken --block_type heading --text $line.Substring(2)
  } elseif ($line.StartsWith("## ")) {
    feishu_doc --action append --doc_token $docToken --block_type heading --text $line.Substring(3)
  } elseif ($line.Trim() -eq "") {
    continue
  } else {
    feishu_doc --action append --doc_token $docToken --block_type text --text $line
  }
}

# 5. 输出链接
Write-Output "飞书文档：https://feishu.cn/docx/$docToken"
```

---

## 相关文件

- **本地 MD：** `memory/xxx.md`
- **飞书文档：** `https://feishu.cn/docx/xxx`

---

**Created:** 2026-03-11  
**Author:** 阿香（根据 Thomas 的指导编写）  
**Version:** 1.0.0

---

_宁可多写几个 blocks，不要一次写长文本！_ 🦞
