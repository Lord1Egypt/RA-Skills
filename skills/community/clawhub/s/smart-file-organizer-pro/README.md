# 智能文件整理助手 Pro 🗂️✨

增强版文件整理工具，专为 OpenClaw 龙虾平台优化。

## ✨ Pro 版本亮点

### 🚀 四种整理模式
- **简洁模式** - 快速分类，保留原文件名
- **标准模式** - 平衡整理和重命名（推荐）
- **深度模式** - 完整整理+重命名+去重
- **归档模式** - 按日期自动归档

### 🎨 优化体验
- 彩色终端输出，清晰直观
- 实时进度显示
- 友好的中文提示
- 智能操作建议

### 📊 完善功能
- 操作历史记录
- 一键撤销功能
- 详细分析报告
- 安全备份机制

## 🚀 快速开始

### 安装要求
- Python 3.7+
- 无需额外依赖

### 基本使用

```bash
# 查看目录分析
python3 scripts/analyze.py --path .

# 简洁整理
python3 scripts/organize.py --path . --mode simple

# 标准整理（推荐）
python3 scripts/organize.py --path . --mode standard

# 预览模式
python3 scripts/organize.py --path . --mode standard --preview

# 查看操作历史
python3 scripts/history.py --list

# 撤销操作
python3 scripts/undo.py --last --confirm
```

## 📁 整理模式详解

### 简洁模式 (simple)
快速按类型分类文件，保留原文件名。

```bash
python3 scripts/organize.py --path ~/Downloads --mode simple
```

适合场景：
- 快速清理下载文件夹
- 不想改变文件名
- 初次使用测试

### 标准模式 (standard)
平衡的整理方式，包含智能重命名和重复检测。

```bash
python3 scripts/organize.py --path ~/Downloads --mode standard
```

适合场景：
- 日常文件整理
- 需要统一命名规范
- 清理重复文件

### 深度模式 (deep)
完整整理体验，包含所有功能。

```bash
python3 scripts/organize.py --path ~/Pictures --mode deep
```

适合场景：
- 彻底整理照片库
- 重要文档归档
- 清理混乱文件夹

### 归档模式 (archive)
按日期创建目录结构归档文件。

```bash
# 按年/月/日归档
python3 scripts/organize.py --path ~/Pictures --mode archive --date-format YYYY/MM/DD

# 按年/月归档
python3 scripts/organize.py --path ~/Documents --mode archive --date-format YYYY/MM
```

适合场景：
- 照片按拍摄日期归档
- 文档按创建日期归档
- 长期存储整理

## 🛡️ 安全特性

### 预览模式
所有操作前先预览，确认无误后再执行：

```bash
python3 scripts/organize.py --path ~/Downloads --mode standard --preview
```

### 自动备份
每次整理前自动创建备份，可随时恢复：

```bash
# 查看备份
python3 scripts/undo.py --list

# 恢复备份
python3 scripts/undo.py --last --confirm
```

### 操作历史
完整的操作记录，可追溯每次整理：

```bash
# 查看历史
python3 scripts/history.py --list

# 查看详情
python3 scripts/history.py --show 20240312_153000
```

## 🧠 智能分析

在整理前分析目录，获取智能建议：

```bash
python3 scripts/analyze.py --path ~/Downloads
```

输出示例：
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  目录分析报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 总体统计:
   总文件数: 1,234
   总大小: 2.3 GB

📁 文件分类:
   • 图片: 456 (37.0%) - 1.2 GB
   • 文档: 234 (19.0%) - 450.5 MB
   • 视频: 123 (10.0%) - 650.2 MB

💡 智能建议:
   📅 检测到 456 个图片文件，建议使用归档模式
      $ python3 organize.py --path . --mode archive
```

## ⚙️ 配置文件

编辑 `config.json` 自定义整理规则：

```json
{
  "mode": "standard",
  "分类设置": {
    "图片": {
      "文件夹": "Pictures",
      "扩展名": [".jpg", ".png", ".gif"],
      "图标": "📷"
    }
  },
  "重命名规则": {
    "启用": true,
    "图片模式": "IMG_{YYYYMMDD}_{序号}"
  },
  "安全设置": {
    "自动备份": true,
    "跳过系统文件": true
  }
}
```

使用自定义配置：

```bash
python3 scripts/organize.py --path . --config my_rules.json
```

## 📝 常见问题

**Q: 整理会丢失文件吗？**
A: 不会。技能提供预览模式、自动备份和撤销功能，三重保障。

**Q: 支持中文文件名吗？**
A: 完全支持。所有脚本都使用 UTF-8 编码。

**Q: 可以整理网络驱动器吗？**
A: 支持。只要系统能访问，就能整理。

**Q: 如何恢复误操作？**
A: 使用撤销功能或从 Backup 文件夹恢复。

**Q: 性能如何？**
A: 标准模式下可处理 4500+ 文件/秒，支持多线程加速。

## 🔧 高级用法

### 只处理特定类型
```bash
python3 scripts/organize.py --path . --types jpg,png,pdf
```

### 排除特定类型
```bash
python3 scripts/organize.py --path . --exclude tmp,log
```

### 详细输出
```bash
python3 scripts/organize.py --path . --mode standard --verbose
```

### 导出历史
```bash
python3 scripts/history.py --list --export history.json
```

## 📄 许可证

MIT License - 自由使用、修改和分发

---

**智能文件整理助手 Pro** - 让文件管理更智能、更高效！
