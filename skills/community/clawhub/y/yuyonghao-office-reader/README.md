# Office Reader 技能

## 支持的文件格式

| 格式 | 扩展名 | 状态 |
|------|--------|------|
| **Markdown** | `.md`, `.markdown` | ✅ 原生支持 |
| **纯文本** | `.txt` | ✅ 原生支持 |
| **CSV** | `.csv` | ✅ 原生支持 |
| **PDF** | `.pdf` | ✅ summarize 技能 |
| **Word** | `.docx`, `.doc` | ✅ python-docx |
| **Excel** | `.xlsx`, `.xls`, `.csv` | ✅ pandas + openpyxl |
| **PowerPoint** | `.pptx`, `.ppt` | ✅ python-pptx |
| **JSON** | `.json` | ✅ 原生支持 |
| **YAML** | `.yaml`, `.yml` | ✅ 需 PyYAML |
| **HTML** | `.html`, `.htm` | ✅ 原生支持 |

## 使用方式

### 方式 1: 直接读取（小文件）
```
读取 C:\path\to\file.docx
```

### 方式 2: 使用脚本
```powershell
.\office-reader.ps1 -FilePath "C:\path\to\file.xlsx"
```

### 方式 3: 使用 summarize 技能（PDF）
```
summarize C:\path\to\file.pdf
```

## 依赖安装

```powershell
pip install openpyxl pandas python-docx python-pptx pdfplumber
```

## 依赖状态

- ✅ python-docx (Word)
- ✅ python-pptx (PowerPoint)
- ✅ pypdf (PDF)
- ⏳ openpyxl (Excel) - 待安装
- ⏳ pandas (Excel 数据处理) - 待安装
