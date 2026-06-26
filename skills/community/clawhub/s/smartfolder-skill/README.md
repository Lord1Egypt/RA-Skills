# SmartFolder 🗂️ | 智能文件管家

> Intelligent file organization assistant for OpenClaw
> OpenClaw 智能文件整理助手

[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://openclaw.ai)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**English**: Transform chaotic folders into organized systems with natural language commands.

**中文**: 用自然语言命令将杂乱的文件夹转变为有序的系统。

---

## ✨ Features | 功能特性

- **🤖 Smart Organization | 智能整理** - Auto-categorizes files by type, date, or size | 按类型、日期或大小自动分类文件
- **🔍 Duplicate Detection | 重复检测** - Find and clean up duplicate files safely | 安全查找并清理重复文件
- **📊 Disk Analysis | 磁盘分析** - Visual breakdown of what's eating your storage | 可视化分析存储空间占用
- **📝 Bulk Renaming | 批量重命名** - Rename files by date, pattern, or sequence | 按日期、模式或序列重命名文件
- **🛡️ Safe Operations | 安全操作** - Dry-run mode, confirmation prompts, undo support | 试运行模式、确认提示、撤销支持

---

## 🚀 Quick Start | 快速开始

```bash
# Organize Downloads folder | 整理下载文件夹
python3 scripts/smartfolder.py organize ~/Downloads

# Preview before organizing (dry-run) | 整理前预览（试运行）
python3 scripts/smartfolder.py organize ~/Downloads --dry-run

# Find duplicate files | 查找重复文件
python3 scripts/smartfolder.py duplicates ~/Documents

# Analyze disk usage | 分析磁盘使用
python3 scripts/smartfolder.py analyze ~/
```

---

## 📦 Installation | 安装

### For OpenClaw Users | OpenClaw 用户

```bash
clawhub install Zaosusu/smartfolder-skill
```

### Standalone Usage | 独立使用

```bash
# Clone repository | 克隆仓库
git clone https://github.com/Zaosusu/smartfolder-skill.git
cd smartfolder-skill

# Install (no external dependencies required!) | 安装（无需外部依赖！）
pip install -r requirements.txt

# Run | 运行
python3 scripts/smartfolder.py --version
```

---

## 🎯 Use Cases | 使用场景

### 1. Clean up Downloads | 清理下载文件夹
```bash
"Organize my downloads folder by type"

# Result | 结果:
Downloads/
├── Documents/ | 文档
├── Images/    | 图片
├── Videos/    | 视频
├── Archives/  | 压缩包
└── Misc/      | 其他
```

### 2. Find Space Hogs | 找出占用空间的文件
```bash
"What's taking up space in my home directory?"

# Shows top 20 largest files | 显示最大的20个文件
```

### 3. Remove Duplicates | 删除重复文件
```bash
"Find duplicate photos and move them for review"

# 安全识别重复文件，移动到审核文件夹
```

---

## 🛠️ Commands | 命令

### `organize` - File Organization | 文件整理
```bash
python3 scripts/smartfolder.py organize <path> [options]

Options | 选项:
  --by-type          # Organize by file type (default) | 按文件类型整理（默认）
  --dry-run          # Preview only | 仅预览
  --target-dir       # Custom output directory | 自定义输出目录
```

### `duplicates` - Duplicate Detection | 重复检测
```bash
python3 scripts/smartfolder.py duplicates <path> [options]

Options | 选项:
  --min-size 1024    # Minimum file size in bytes | 最小文件大小（字节）
```

### `analyze` - Disk Usage Analysis | 磁盘分析
```bash
python3 scripts/smartfolder.py analyze <path> [options]

Options | 选项:
  --top 20           # Show top N files | 显示前N个文件
  --older-than 365   # Files older than N days | N天前的文件
```

---

## 📝 Supported File Categories | 支持的文件类别

| Category | 中文 | Extensions |
|----------|------|------------|
| Documents | 文档 | .pdf, .doc, .docx, .txt, .md, .xlsx, .pptx |
| Images | 图片 | .jpg, .png, .gif, .svg, .webp, .raw |
| Videos | 视频 | .mp4, .avi, .mov, .mkv, .webm |
| Audio | 音频 | .mp3, .wav, .flac, .aac, .ogg |
| Archives | 压缩包 | .zip, .rar, .7z, .tar.gz |
| Code | 代码 | .py, .js, .html, .css, .json, .sql |
| Data | 数据 | .csv, .db, .sqlite, .parquet |

---

## 📄 License | 许可证

MIT License - See [LICENSE](LICENSE) file

---

**Made with ❤️ for organized files everywhere | 为整理文件而生** 🦞
