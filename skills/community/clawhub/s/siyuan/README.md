# SiYuan Note API Client

[![Version](https://img.shields.io/badge/version-1.0.0-blue)](https://clawhub.ai)
[![Python](https://img.shields.io/badge/python-3.8%2B-green)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)

> 🧠 思源笔记 (SiYuan Note) 的完整 API 客户端，支持笔记本管理、文档操作、块编辑等全部功能。

[English](#english) | [中文](#中文)

---

## 中文

### ✨ 功能特性

- **📚 笔记本管理** - 创建、打开、关闭、重命名、删除笔记本
- **📝 文档操作** - 创建、读取、更新、移动、导出文档
- **🧩 块级编辑** - 插入、更新、删除、移动内容块
- **🔍 全文搜索** - 基于 SQL 的灵活查询
- **📎 资源管理** - 上传图片、附件等资产文件
- **📤 导入导出** - Markdown、PDF、ZIP 格式支持
- **🔒 安全可靠** - 自动重试、错误处理、连接健康检查

### 🚀 快速开始

#### 1. 安装

```bash
clawhub install siyuan
```

#### 2. 配置

复制配置模板并填入你的 API Token：

```bash
cd ~/.openclaw/workspace/skills/siyuan
cp config.example.yaml config.yaml
```

编辑 `config.yaml`：

```yaml
siyuan:
  base_url: "http://127.0.0.1:6806"
  token: "your-api-token-here"  # 从思源笔记设置中获取
  timeout: 30
  retry: 3
```

**获取 Token**：思源笔记 → 设置 → 关于 → API → 复制 Token

#### 3. 使用

**列出所有笔记本：**
```bash
python3 tools/list.py --notebooks
```

**搜索笔记：**
```bash
python3 tools/search.py "关键词"
```

**读取文档：**
```bash
python3 tools/read.py 20240602141622-l7ou7t7
```

**创建文档：**
```bash
python3 tools/create.py --doc notebook-id /readme "# 标题\n\n内容"
```

### 📖 完整文档

查看 [SKILL.md](./SKILL.md) 获取完整的 API 参考和示例。

### 🛠️ Python API

```python
from siyuan_client import SiYuanClient

# 初始化客户端
client = SiYuanClient()

# 列出笔记本
notebooks = client.list_notebooks()

# 读取文档
result = client.export_md_content("doc-id")
print(result['content'])

# 创建文档
client.create_doc_with_md(
    notebook_id="notebook-id",
    path="folder/document",
    markdown="# 新文档\n\n内容"
)
```

---

## English

### ✨ Features

- **📚 Notebook Management** - Create, open, close, rename, remove notebooks
- **📝 Document Operations** - Create, read, update, move, export documents
- **🧩 Block-level Editing** - Insert, update, delete, move content blocks
- **🔍 Full-text Search** - Flexible SQL-based queries
- **📎 Asset Management** - Upload images, attachments
- **📤 Import/Export** - Markdown, PDF, ZIP support
- **🔒 Reliable** - Auto-retry, error handling, health checks

### 🚀 Quick Start

#### 1. Install

```bash
clawhub install siyuan
```

#### 2. Configure

Copy the config template and add your API token:

```bash
cd ~/.openclaw/workspace/skills/siyuan
cp config.example.yaml config.yaml
```

Edit `config.yaml`:

```yaml
siyuan:
  base_url: "http://127.0.0.1:6806"
  token: "your-api-token-here"  # Get from SiYuan settings
  timeout: 30
  retry: 3
```

**Get Token**: SiYuan → Settings → About → API → Copy Token

#### 3. Usage

**List all notebooks:**
```bash
python3 tools/list.py --notebooks
```

**Search notes:**
```bash
python3 tools/search.py "keyword"
```

**Read document:**
```bash
python3 tools/read.py 20240602141622-l7ou7t7
```

**Create document:**
```bash
python3 tools/create.py --doc notebook-id /readme "# Title\n\nContent"
```

### 📖 Full Documentation

See [SKILL.md](./SKILL.md) for complete API reference and examples.

### 🛠️ Python API

```python
from siyuan_client import SiYuanClient

# Initialize client
client = SiYuanClient()

# List notebooks
notebooks = client.list_notebooks()

# Read document
result = client.export_md_content("doc-id")
print(result['content'])

# Create document
client.create_doc_with_md(
    notebook_id="notebook-id",
    path="folder/document",
    markdown="# New Document\n\nContent"
)
```

---

## 🔧 CLI Tools

| 工具 | 功能 |
|------|------|
| `list.py` | 列出笔记本和文档 |
| `read.py` | 读取文档内容 |
| `search.py` | 搜索笔记 |
| `create.py` | 创建笔记本/文档 |
| `delete.py` | 删除笔记本/文档/块 |
| `update.py` | 更新块内容 |
| `move.py` | 移动文档 |
| `export.py` | 导出笔记 |

---

## 📋 Requirements

- Python 3.8+
- SiYuan Note running with API enabled
- API Token from SiYuan settings

---

## 📄 License

MIT License - see LICENSE file for details.

---

## 🔗 Links

- **ClawHub**: https://clawhub.ai/weiwei2027/siyuan
- **SiYuan Official**: https://github.com/siyuan-note/siyuan
- **API Docs**: https://www.siyuan-note.club/apis

---

## 🙏 Credits

Created for [OpenClaw](https://openclaw.ai) - AI-powered personal assistant platform.
