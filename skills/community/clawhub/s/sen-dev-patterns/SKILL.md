---
name: sen-dev-patterns
description: "个人开发提效Skill - 沉淀页面布局、样式风格、代码模块、算法库、踩坑记录。适用于用户需要复用个人开发经验、遵循统一规范、调用已沉淀的计算口径或模块的场景。"
description_zh: "个人开发提效工具库：UI规范、代码模块、算法口径、踩坑记录"
description_en: "Personal development patterns: UI styles, code modules, algorithms, pitfalls"
version: "1.3.0"
allowed-tools: Read, Write, Edit, Bash
tags: ["开发规范", "UI样式", "算法", "Python", "桌面应用", "Web开发"]
---

# Sen 开发提效 Skill

## 概述

这是一个个人开发经验沉淀库，涵盖UI规范、代码模块、算法口径、踩坑记录，旨在提升后续开发效率和一致性。

**适用场景**：
- 开发新的数据处理工具时复用样式和模块
- 需要调用已验证的计算口径
- 保持跨项目的一致性
- 记录和复用踩坑经验

## 目录结构

```
sen-dev-patterns/
├── SKILL.md                    # 本文件 - 总览和索引
├── README.md                   # 使用说明
├── references/                 # 详细参考文档
│   ├── ui-style-guide.md       # UI样式规范（桌面应用）
│   ├── web-guide.md            # Web开发规范（CSS/HTML）
│   ├── coding-standards.md      # 编程规范
│   ├── algorithm-library.md     # 算法计算口径库（满意度加权公式等）
│   ├── pitfalls-record.md       # 踩坑记录
│   ├── code-modules.md          # 代码模块库（日志、文件、GUI等）
│   ├── icon-library.md          # 图标库（Emoji、SVG、按钮样式）
│   ├── performance-guide.md     # 性能优化指南
│   ├── git-workflow.md         # Git工作流与备份规范 ⭐新增
│   └── evaluation-report.md     # 质量评估报告
├── scripts/                    # 可执行脚本
│   └── init_module.py          # 初始化标准模块的脚本
└── assets/                     # 资源文件
    ├── templates/               # 代码模板
    └── icon-configs/           # 图标配置
```

## 核心原则

### 1. 最小改动原则
- **只改需要改的地方**：需求变更时，只修改与当前问题相关的最少代码行
- **禁止重构**：不主动重构已验证正确的代码
- **禁止优化无关代码**：不要借机优化其他代码

### 2. 已正确部分绝对不动
- 若明确说明某部分逻辑正确，必须严格保护
- 不得修改变量名、结构、顺序、注释和格式

### 3. 修改必须透明
- 每次修改后说明：修改了哪几行、修改原因、对原有逻辑的影响

### 4. 先定位问题，再动手修改
- 优先帮用户定位错误位置
- 不直接大面积改写代码

## UI设计规范

### 配色方案

| 用途 | 颜色代码 | 说明 |
|------|----------|------|
| 主色调 | `#667eea` → `#764ba2` | 渐变色，用于标题、重要按钮 |
| 成功色 | `#48bb78` / `#68d391` | 绿色，表示成功、完成 |
| 警告色 | `#f6ad55` / `#ff9500` | 橙色，表示进度、警告 |
| 错误色 | `#fc8181` / `#e74c3c` | 红色，表示错误、失败 |
| 信息色 | `#63b3ed` / `#3498db` | 蓝色，表示信息、链接 |
| 辅助色 | `#9f7aea` | 紫色，用于次要按钮 |
| 背景色 | `#f0f5f9` / `#f0f4ff` | 浅色背景 |
| 日志背景 | `#1a202c` | 深色日志区域 |
| 日志文字 | `#e2e8f0` | 日志默认文字色 |

### 水晶质感按钮样式

```python
crystal_style = """
    QPushButton {
        color: #ffffff;
        font-weight: 700;
        font-size: 14px;
        border-radius: 16px;
        padding: 12px 20px;
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 %COLOR_START%,
            stop:0.5 %COLOR_MID%,
            stop:1 %COLOR_END%);
        border-top: 1px solid #ffffff;
        border-left: 1px solid #ffffff;
        border-right: 1px solid #000000;
        border-bottom: 2px solid #000000;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 %HOVER_START%,
            stop:0.5 %HOVER_MID%,
            stop:1 %HOVER_END%);
    }
    QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 %PRESSED_START%,
            stop:0.5 %PRESSED_MID%,
            stop:1 %PRESSED_END%);
    }
    QPushButton:disabled {
        color: #cccccc;
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #a0aec0, stop:1 #718096);
    }
"""
```

### Tkinter 按钮样式（Tk风格）

```python
style.configure(
    "CrystalButton.TButton",
    font=("Microsoft YaHei", 10, "bold") if sys.platform != "darwin" else ("Helvetica Neue", 10, "bold"),
    foreground="white",
    background="#3498db",
    padding=(15, 8),
    relief="flat",
    borderwidth=0
)
style.map(
    "CrystalButton.TButton",
    background=[("active", "#2980b9"), ("pressed", "#1a5276")],
    foreground=[("active", "white"), ("pressed", "white")]
)
```

### 跨平台字体

```python
# Windows
font_main = ("Microsoft YaHei", 10)
font_title = ("Microsoft YaHei", 22, "bold")
font_btn = ("Microsoft YaHei", 10, "bold")

# Mac
font_main = ("Helvetica Neue", 10)
font_title = ("Helvetica Neue", 22, "bold")
font_btn = ("Helvetica Neue", 10, "bold")
```

## 项目结构规范

### Python 桌面应用标准结构

```
project/
├── main.py              # 主程序入口
├── logger.py            # 日志模块（TextHandler输出到GUI）
├── file_util.py         # 文件操作工具
├── date_splitter.py     # 日期拆分模块
├── monthly_agg.py       # 月度聚合模块
├── template_mapper.py   # 模板映射模块
├── settings.json        # 用户配置文件
├── spec_file.spec       # PyInstaller打包配置
├── 数据模板.xlsx         # Excel模板
└── dist/                # 打包输出目录
```

### 模块职责

| 模块 | 职责 |
|------|------|
| `main.py` | UI、业务流程、设置管理 |
| `logger.py` | 日志输出到GUI（TextHandler） |
| `file_util.py` | 文件选择、验证、读取 |
| `date_splitter.py` | 按日期拆分数据 |
| `monthly_agg.py` | 月度数据聚合 |
| `template_mapper.py` | 模板映射和填充 |

## 代码模板

详见 `references/ui-style-guide.md`

## 算法计算口径

详见 `references/algorithm-library.md`

## 踩坑记录

详见 `references/pitfalls-record.md`

## 使用方法

### 复用UI样式
参考 `references/ui-style-guide.md` 中的完整样式代码

### 复用计算口径
```python
from references.algorithm_library import target_l_calculation, count_with_conditions
```

### 调用代码模板
```bash
python scripts/init_module.py --type worker --name MyWorker
```

## 更新日志

> **维护规范**：每次修改skill后，在此记录更新内容，便于追踪变化历史。

| 日期 | 版本 | 更新内容 |
|------|------|----------|
| 2026-04-24 | v1.3 | 🔄 第2-3轮优化：添加Web开发规范、Git工作流与备份规范 |
| 2026-04-24 | v1.2 | 🔄 第1轮优化：添加同比/环比/转化率算法、性能优化指南、更新日志机制 |
| 2026-04-24 | v1.1 | 📝 添加代码模块库、图标库 |
| 2026-04-24 | v1.0 | ✨ 初始版本，从业务降本推进和云安防项目提炼 |

### 更新日志维护指南

每次修改skill时，请按以下格式追加记录：

```markdown
| YYYY-MM-DD | vX.X | 📝 更新内容描述 |
```

**版本号规则**：
- `v1.x`：小版本迭代，添加新内容
- `vx.x+1`：大版本更新，重大结构调整

**更新类型标记**：
- ✨ 新功能
- 📝 内容完善
- 🔄 优化重构
- 🐛 修复问题
- ⭐ 高优先级更新
