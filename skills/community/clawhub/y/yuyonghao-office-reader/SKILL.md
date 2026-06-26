# office-reader 技能

## 描述

统一的 Office 文档和本地文件读取技能，支持 Word、Excel、PowerPoint、PDF 及多种文本格式。

## 支持的文件格式

| 类型 | 扩展名 | 读取方式 |
|------|--------|----------|
| **Markdown** | `.md`, `.markdown` | 原生文本 |
| **纯文本** | `.txt` | 原生文本 |
| **CSV** | `.csv` | 原生文本 |
| **JSON** | `.json` | 原生 JSON 解析 |
| **YAML** | `.yaml`, `.yml` | PyYAML |
| **HTML** | `.html`, `.htm` | 原生文本 |
| **Word** | `.docx`, `.doc` | python-docx |
| **Excel** | `.xlsx`, `.xls` | pandas + openpyxl |
| **PowerPoint** | `.pptx`, `.ppt` | python-pptx |
| **PDF** | `.pdf` | pypdf / summarize |

## 使用方法

### 方式 1: 直接使用 PowerShell 脚本

```powershell
# 读取 Word 文档
.\skills\office-reader\office-reader.ps1 -FilePath "C:\path\to\document.docx"

# 读取 Excel 文件
.\skills\office-reader\office-reader.ps1 -FilePath "C:\path\to\data.xlsx"

# 读取 PowerPoint
.\skills\office-reader\office-reader.ps1 -FilePath "C:\path\to\presentation.pptx"

# 读取 PDF（前 10 页）
.\skills\office-reader\office-reader.ps1 -FilePath "C:\path\to\report.pdf"
```

### 方式 2: 自然语言请求

直接对我说：
- "读取 C:\path\to\file.docx"
- "看看这个 Excel 文件：C:\path\to\data.xlsx"
- "帮我读一下这个 PPT: C:\path\to\slides.pptx"

我会自动调用 office-reader 脚本处理。

### 方式 3: PDF 使用 summarize 技能

```
summarize C:\path\to\file.pdf
```

## 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `-FilePath` | string | 必填 | 要读取的文件路径 |
| `-OutputFormat` | string | "text" | 输出格式（text/json/markdown） |
| `-MaxLines` | int | 1000 | 最大输出行数（防止过长） |

## 示例输出

### Word 文档
```
📄 读取文件：C:\docs\report.docx
📋 文件类型：.docx
✅ 使用 Word 模式读取 (python-docx)...

[文档标题]

[第一段内容...]

[第二段内容...]

✅ 读取完成！
```

### Excel 文件
```
📄 读取文件：C:\data\sales.xlsx
📋 文件类型：.xlsx
✅ 使用 Excel 模式读取 (pandas + openpyxl)...

📊 工作表数量：3
📋 工作表名称：['一月', '二月', '三月']

=== 工作表：一月 ===
行数：150, 列数：8
列名：['日期', '产品', '销售额', '利润', ...]

前 20 行数据:
   日期      产品    销售额   利润
0  2026-01-01  产品 A  1000   200
1  2026-01-02  产品 B  1500   350
...

✅ 读取完成！
```

### PowerPoint 文件
```
📄 读取文件：C:\presentations\demo.pptx
📋 文件类型：.pptx
✅ 使用 PowerPoint 模式读取 (python-pptx)...

📊 幻灯片数量：15

=== 幻灯片 1 ===
布局：Title Slide

  Title: 项目演示
  Subtitle: 2026 年 Q1 汇报

=== 幻灯片 2 ===
布局：Title and Content

  Title: 目录
  Content: 1. 项目背景...

✅ 读取完成！
```

## 依赖

已安装的 Python 库：
- ✅ python-docx (Word)
- ✅ python-pptx (PowerPoint)
- ✅ pypdf (PDF)
- ✅ openpyxl (Excel)
- ✅ pandas (数据处理)

## 限制

- Word/Excel/PPT 仅支持 `.docx/.xlsx/.pptx` 格式（Office 2007+）
- 旧格式 `.doc/.xls/.ppt` 需要转换
- PDF 文本提取依赖 PDF 质量（扫描件可能无法提取）
- 大文件自动限制输出行数（默认 1000 行）

## 故障排除

### 问题：文件无法读取
**解决**: 检查文件路径是否正确，文件是否被其他程序占用

### 问题：Excel 读取报错
**解决**: 确保 `.xlsx` 格式（非 `.xls`），或转换为 CSV

### 问题：PDF 提取内容为空
**解决**: 可能是扫描件，需要 OCR（暂不支持）

## 安全说明

- 仅读取本地文件，不上传外部
- 自动限制输出大小，防止内存溢出
- 支持 UTF-8 编码，兼容中文

---

**版本**: v0.1.0  
**创建时间**: 2026-03-18  
**作者**: 小蒲萄 🦞
