---
name: wecom-file-detect
version: 1.0.0
description: >
  企业微信聊天文件获取 - 从 ~/.openclaw/media/inbound/ 目录检测和获取通过聊天传递的文件。
  当用户提到获取文件、发送文件、附件等请求时激活。
author: SC
keywords: [wecom, file, media, inbound, attachment]
metadata:
  openclaw:
    emoji: "📎"
    category: utility
---

# 企业微信文件获取

当用户提到"获取文件"、"发送文件"、"附件"等请求时，自动从 inbound 目录检测和获取文件。

## 文件获取流程

### 1. 检测最新文件

当没有明确文件名时，扫描 inbound 目录获取最新文件：

```bash
ls -lt ~/.openclaw/media/inbound/ | head -20
```

### 2. 文件类型识别

支持的类型：
- 文档：.doc, .docx, .xls, .xlsx, .ppt, .pptx, .pdf, .md, .csv
- 图片：.png, .jpg, .jpeg, .gif
- 视频：.mp4, .mov
- 其他：.zip, .txt

### 3. 文件内容读取

根据文件类型选择读取方式：
- 文本文件：直接 cat
- CSV/Excel：转换为表格
- 图片：使用 image tool 识别
- Word/PDF：使用 markitdown 或 minimax-ocr

### 4. 文件存档

重要文件应存档到 companywork/ 相关目录：
```bash
mkdir -p companywork/AI赋能计划/
cp "源文件" "companywork/目标目录/"
```

## 常用命令

```bash
# 查看最近的文件
ls -lt ~/.openclaw/media/inbound/ | head -10

# 按类型查找
find ~/.openclaw/media/inbound/ -name "*.xlsx" -mtime -7

# 按关键词搜索
ls -lt ~/.openclaw/media/inbound/ | grep "关键词"
```

## 触发场景

- 用户说"获取文件"
- 用户说"发送附件"
- 用户说"看看有什么文件"
- 用户上传文件后没有反应
- 用户提到某个具体项目但没有附文件

## 注意事项

1. 文件名可能包含时间戳和UUID
2. WeCom可能将文件转换为文本格式（二进制内容丢失）
3. 重要文件应及时存档到 companywork/
4. 用完的临时文件可以保留在 inbound 供后续使用
