---
name: smart-file-organizer-pro
description: 智能文件整理助手 Pro - 增强版，支持按日期归档、多模式预设、进度显示、操作历史
version: 2.0.0
icon: 🗂️✨
metadata:
  clawdbot:
    emoji: 🗂️✨
    requires:
      bins: ["python3"]
    install: []
    tags: ["file", "organize", "automation", "productivity", "tool", "utility", "pro"]
    category: "productivity"
    author: "MoneyClaw Team"
    license: "MIT"
    features:
      - "smart-categorization-plus"
      - "auto-renaming-plus"
      - "duplicate-detection"
      - "safety-backup"
      - "preview-mode"
      - "cross-platform"
      - "date-archiving"
      - "progress-display"
      - "operation-history"
      - "preset-modes"
---

# 智能文件整理助手 Pro 🗂️✨

## ✨ Pro 版本亮点
- 🚀 **多模式预设** - 简洁/标准/深度三种整理模式
- 📅 **智能归档** - 按日期自动归档到年/月/日结构
- 📊 **进度显示** - 实时显示整理进度和统计
- 📜 **操作历史** - 完整的操作日志和撤销记录
- 🎨 **彩色输出** - 清晰友好的终端显示
- ⚡ **性能优化** - 多线程处理，更快速度
- 🧠 **智能建议** - 根据文件内容给出整理建议
- 🔒 **增强安全** - 自动备份、冲突检测、权限检查

---

## 快速开始

### 基本使用
```bash
# 简洁模式 - 快速整理
python3 scripts/organize.py --path . --mode simple

# 标准模式 - 平衡整理和重命名
python3 scripts/organize.py --path . --mode standard

# 深度模式 - 完整整理+重命名+去重
python3 scripts/organize.py --path . --mode deep

# 预览模式 - 查看将要执行的操作
python3 scripts/organize.py --path . --mode standard --preview
```

### 按日期归档
```bash
# 按年/月/日归档照片
python3 scripts/organize.py --path ~/Pictures --mode archive --date-format YYYY/MM/DD

# 按年/月归档文档
python3 scripts/organize.py --path ~/Documents --mode archive --date-format YYYY/MM
```

### 自定义规则
```bash
# 使用自定义配置文件
python3 scripts/organize.py --path . --config my_rules.json

# 只处理特定类型
python3 scripts/organize.py --path . --types jpg,png,pdf

# 设置输出详细程度
python3 scripts/organize.py --path . --mode standard --verbose
```

## 整理模式说明

### 1. 简洁模式 (simple)
- 仅按文件类型分类
- 不重命名文件
- 不检测重复文件
- 适合：快速整理、保留原名

### 2. 标准模式 (standard)
- 按文件类型分类
- 智能重命名（可选）
- 基础重复检测
- 适合：日常整理

### 3. 深度模式 (deep)
- 按文件类型分类
- 智能重命名
- 完整重复检测
- 按日期归档
- 适合：彻底整理

### 4. 归档模式 (archive)
- 按日期创建目录结构
- 保持原始文件名
- 自动生成归档报告
- 适合：照片/文档归档

## 文件分类规则

### 默认分类
- **📷 图片** → `Pictures/` (jpg, png, gif, webp, bmp, svg, raw, heic)
- **📄 文档** → `Documents/` (pdf, doc, docx, xls, xlsx, ppt, pptx, txt, md)
- **🎬 视频** → `Videos/` (mp4, mov, avi, mkv, flv, wmv, m4v)
- **🎵 音频** → `Music/` (mp3, wav, flac, m4a, aac, ogg)
- **📦 压缩包** → `Archives/` (zip, rar, 7z, tar, gz, bz2)
- **💻 代码** → `Code/` (py, js, java, cpp, html, css, json, xml)
- **🔧 可执行** → `Executables/` (exe, msi, app, dmg)
- **📁 其他** → `Others/`

### 按应用来源分类（可选）
- **🌐 浏览器下载** → `Downloads/Browser/`
- **💬 社交应用** → `Downloads/Social/`
- **🎮 游戏** → `Downloads/Games/`
- **📱 移动应用** → `Downloads/Mobile/`

## 命令行参数详解

### 基本参数
```
--path <路径>        要整理的目录（默认：当前目录）
--mode <模式>        整理模式：simple/standard/deep/archive（默认：standard）
--preview            预览模式，不实际执行操作
--config <文件>      使用自定义配置文件
```

### 整理选项
```
--types <类型>       只处理指定文件类型（逗号分隔）
--exclude <类型>     排除指定文件类型（逗号分隔）
--rename             启用智能重命名
--deduplicate        启用重复文件检测
--date-format <格式> 日期归档格式（如：YYYY/MM/DD）
```

### 安全选项
```
--backup             整理前创建备份
--no-backup          跳过备份
--dry-run            同 --preview
--safe-mode         安全模式，更保守的操作
```

### 输出选项
```
--verbose            详细输出
--quiet              静默模式
--progress           显示进度条
--report             生成整理报告
```

## 配置文件示例

### config.json 完整示例
```json
{
  "mode": "standard",
  "分类设置": {
    "images": [".jpg", ".png", ".gif", ".webp", ".heic"],
    "documents": [".pdf", ".doc", ".docx", ".xls", ".xlsx"],
    "videos": [".mp4", ".mov", ".avi"],
    "audio": [".mp3", ".wav", ".flac"],
    "archives": [".zip", ".rar", ".7z"],
    "code": [".py", ".js", ".html", ".css", ".json"]
  },
  "重命名规则": {
    "启用": true,
    "保留原始名称": false,
    "图片模式": "IMG_{YYYYMMDD}_{序号}",
    "文档模式": "DOC_{标题}_{日期}",
    "通用模式": "FILE_{日期}_{序号}"
  },
  "归档设置": {
    "启用": false,
    "日期格式": "YYYY/MM/DD",
    "使用创建日期": true,
    "使用修改日期": false
  },
  "重复文件检测": {
    "启用": true,
    "检测方法": "hash",
    "处理方式": "move",
    "保留策略": "oldest",
    "重复文件夹": "Duplicates"
  },
  "安全设置": {
    "预览模式": false,
    "自动备份": true,
    "备份保留天数": 30,
    "跳过系统文件": true,
    "跳过隐藏文件": true,
    "最大文件大小MB": 1024,
    "安全模式": false
  },
  "性能设置": {
    "最大工作线程": 4,
    "显示进度": true,
    "使用缓存": true
  },
  "输出设置": {
    "详细程度": "normal",
    "彩色输出": true,
    "生成报告": true,
    "日志级别": "INFO"
  }
}
```

## 输出说明

### 终端输出示例
```
🗂️ 智能文件整理助手 Pro v2.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 目标目录: /home/user/Downloads
📋 整理模式: 标准模式 (standard)
⚙️  配置: 预览模式已启用

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏳ 正在扫描文件...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 扫描结果:
  ✓ 总文件数: 1,234
  ✓ 图片文件: 456
  ✓ 文档文件: 234
  ✓ 视频文件: 123
  ✓ 其他文件: 421

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 整理预览:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1/1234] vacation.jpg → Pictures/2024_03_12_001.jpg
[2/1234] report.pdf → Documents/Work_Report_20240312.pdf
[3/1234] song.mp3 → Music/song.mp3
...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 这是预览模式，未执行实际操作
💡 要执行整理，请移除 --preview 参数
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 操作历史和撤销

### 查看操作历史
```bash
# 查看最近操作
python3 scripts/history.py --list

# 查看操作详情
python3 scripts/history.py --show <操作ID>

# 撤销上次操作
python3 scripts/undo.py --last

# 撤销指定操作
python3 scripts/undo.py --id <操作ID>
```

### 备份管理
```bash
# 列出所有备份
python3 scripts/backup.py --list

# 恢复指定备份
python3 scripts/backup.py --restore <备份ID>

# 清理旧备份
python3 scripts/backup.py --clean --older-than 30
```

## 高级功能

### 智能建议
```bash
# 获取整理建议
python3 scripts/analyze.py --path .

# 输出示例:
💡 检测到大量照片文件，建议使用归档模式
💡 发现 23 个可能重复的文件，建议运行去重
💡 建议创建自定义规则: 电子发票 -> Documents/发票
```

### 批量处理
```bash
# 整理多个目录
python3 scripts/batch.py --paths ~/Downloads,~/Documents,~/Pictures

# 使用配置文件批量处理
python3 scripts/batch.py --config batch_rules.json
```

### 文件监控
```bash
# 监控目录并自动整理新文件
python3 scripts/watch.py --path ~/Downloads --mode standard
```

## 故障排除

### 常见问题
**Q: 中文文件名显示乱码？**
```bash
# 设置编码
export PYTHONIOENCODING=utf-8
python3 scripts/organize.py --path .
```

**Q: 权限不足无法移动文件？**
```bash
# 使用安全模式
python3 scripts/organize.py --path . --safe-mode
```

**Q: 处理速度太慢？**
```bash
# 调整线程数
python3 scripts/organize.py --path . --threads 8
```

## 更新日志

### v2.0.0 (当前版本)
- ✨ 新增四种整理模式
- ✨ 新增日期归档功能
- ✨ 新增进度显示
- ✨ 新增操作历史
- ✨ 新增智能建议
- 🚀 性能优化：多线程处理
- 🎨 彩色输出优化
- 📝 更完善的文档

### v1.0.0
- 基础文件分类功能
- 智能重命名
- 重复文件检测
- 安全备份

---

**智能文件整理助手 Pro** - 让文件管理更智能、更高效！
