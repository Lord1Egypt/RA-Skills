# WPS Office Skill

用于 OpenClaw 的 WPS Office 自动化操作 Skill，支持文档创建、打开、格式转换、批量处理等功能。

## 功能特性

- 📄 **创建文档** - 创建 Word、Excel、PPT 文档
- 📂 **打开文档** - 打开已有文档
- 📋 **文档列表** - 列出文档目录中的文件
- 🔄 **格式转换** - 转换文档格式（PDF、Word、Excel 等）
- 📦 **批量处理** - 批量转换目录中的文档

## 安装

### 1. 安装依赖

```bash
pip install pyautogui pyperclip Pillow
```

### 2. 配置 Skill

编辑 `config.json`：

```json
{
  "default_save_path": "~/Documents/WPS",
  "wps_path": ""
}
```

- `default_save_path`: 默认文档保存路径
- `wps_path`: WPS 安装路径（可选，自动检测）

## 使用方法

### 创建文档

```bash
# 创建 Word 文档
python scripts/main.py create type=writer filename=报告.docx

# 创建 Excel 表格
python scripts/main.py create type=spreadsheet filename=数据.xlsx

# 创建 PPT 演示文稿
python scripts/main.py create type=presentation filename=演示.pptx

# 创建带内容的文档
python scripts/main.py create type=writer filename=笔记.docx content="这是文档内容"
```

### 打开文档

```bash
# 打开已有文档
python scripts/main.py open file=~/Documents/报告.docx
```

### 列出文档

```bash
# 列出默认目录的文档
python scripts/main.py list

# 列出指定目录
python scripts/main.py list dir=~/Documents
```

### 格式转换

```bash
# 转换为 PDF
python scripts/main.py convert file=报告.docx format=pdf

# 转换为 Word
python scripts/main.py convert file=数据.xlsx format=docx
```

### 批量转换

```bash
# 批量转换为 PDF
python scripts/main.py batch_convert dir=~/Documents format=pdf
```

## 在 OpenClaw 中使用

### 配置 Agent

```json
{
  "skills": ["wps-office"]
}
```

### 使用示例

```bash
# 创建文档
openclaw agent --message "帮我创建一个名为'项目报告'的Word文档"

# 打开文档
openclaw agent --message "打开我的文档目录中的'数据.xlsx'文件"

# 批量转换
openclaw agent --message "把~/Documents目录下的所有文档转换成PDF格式"
```

## 注意事项

1. **WPS 安装**：确保系统已安装 WPS Office
2. **权限**：macOS 需要授予自动化权限
3. **路径**：支持相对路径和绝对路径

## 版本信息

- **版本**: 1.0.0
- **作者**: MaxStorm Team
- **许可证**: MIT
