---
name: read-gbk
description: 读取本地文本文件，支持 GBK/UTF-8 编码自动检测
metadata: {"clawdbot":{"emoji":"📄","requires":{"bins":["python"]},"install":[{"id":"python-docx","kind":"pip","module":"python-docx","label":"预安装 python-docx（可选，读取.docx 时会自动安装）"},{"id":"pypdf","kind":"pip","module":"pypdf","label":"预安装 pypdf（可选，读取.pdf 时会自动安装）"}]}}
---

# read-gbk - 文件读取工具

读取本地文本文件，自动检测编码（优先 GBK，失败则尝试 UTF-8）。

## 前置要求

**需要 Python 环境**（Python 3.8+）

### 如果没有 Python，先安装：

**方式 1：Miniconda（推荐）**
```bash
# 下载安装：https://docs.conda.io/en/latest/miniconda.html
```

**方式 2：Python 官方安装包**
```bash
# 下载：https://www.python.org/downloads/
# ⚠️ 安装时勾选 "Add Python to PATH"
```

**方式 3：winget 安装（Windows）**
```bash
winget install Python.Python.3.11
```

### 自动安装的依赖

| 文件类型 | 依赖库 | 安装方式 |
|----------|--------|----------|
| `.docx` | `python-docx` | 首次读取时自动安装 |
| `.pdf` | `pypdf` | 首次读取时自动安装 |

无需手动安装这些库，首次使用时会自动安装。

## 快速开始

```bash
node {skillDir}/scripts/read-file.js "文件路径.txt"
```

## 支持的文件格式

| 格式 | 说明 |
|------|------|
| .txt | 纯文本文件（GBK/UTF-8 自动检测） |
| .md | Markdown 文件 |
| .csv | CSV 文件（GBK 编码常见于 Excel 导出） |
| .log | 日志文件 |
| .docx | Word 文档（自动安装 python-docx） |
| .pdf | PDF 文档（自动安装 pypdf，仅支持文字版 PDF） |
| .json | JSON 文件 |
| .xml | XML 文件 |
| .ini / .cfg | 配置文件 |

## 编码检测逻辑

1. 首先尝试用 **GBK** 解码（Windows 中文环境默认）
2. 如果 GBK 解码失败，尝试 **UTF-8**
3. 如果都失败，返回错误信息

## 示例

```bash
# 读取普通文本文件
node {skillDir}/scripts/read-file.js "D:\文档\笔记.txt"

# 读取 CSV 文件
node {skillDir}/scripts/read-file.js "D:\数据\报表.csv"

# 读取 Word 文档
node {skillDir}/scripts/read-file.js "D:\华为项目\病历.docx"
```

## 输出

- 成功：输出文件内容（stdout）
- 失败：输出错误信息（stderr），退出码 1

## 注意事项

- 二进制文件（如 .exe, .zip, .jpg）不支持
- 超大文件（>50MB）可能被截断
- 首次读取 .docx 文件时会自动安装 python-docx（约 2-5 秒）
- 避免在 PowerShell 管道中使用（如 `| Select-Object`），直接输出即可
