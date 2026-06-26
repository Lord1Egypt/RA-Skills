---
name: wiz-migration
description: 为知笔记迁移辅助技能，提供自动检测存储目录、导出操作引导、附件批量迁移等完整迁移流程
version: 1.0.0
author: OpenClaw Assistant
supported_models: ["*"]
tags: ["migration", "wiz", "笔记", "数据迁移"]
---

# 为知笔记迁移技能

为知笔记数据迁移辅助工具，提供自动化检测、交互式引导和一键迁移功能。

## 功能特性

- 🔍 **智能检测存储目录**：自动查找为知笔记数据目录，支持手动输入
- 📝 **导出操作引导**：生成带详细步骤的 .md 模板，指导用户正确导出
- 📎 **附件批量迁移**：自动复制所有 _Attachments 目录到目标位置
- 🖥️ **跨平台支持**：Windows 批处理脚本，简化操作
- ⚡ **增量复制**：自动跳过已存在的文件，支持重复执行

## 快速开始

### 1. 启动迁移向导

```bash
# 启动交互式迁移流程
openclaw skill wiz-migration start

# 或在 Python 脚本中调用
from wiz_migration import start_wizard
start_wizard()
```

### 2. 按照向导步骤操作

1. **检测存储目录**：自动尝试查找 `C:\Users\Administrator\Documents\My Knowledge\Data\`
2. **输入导出路径**：提供为知笔记导出后的 HTML 文件夹路径
3. **生成导出指南**：保存为 `wiz_export_guide.md`
4. **附件迁移**：选择是否自动运行批处理脚本迁移附件

## 导出操作指南

### 为知笔记导出设置（必做）

在运行迁移前，需要先在为知笔记中执行导出操作：

1. 整理笔记：将所有要迁移的目录和文档移动到同一个父目录下
2. 选中笔记本/笔记 → 右键 → 导出文件 → 导出 HTML
3. **关键选项**：
   - ✅ 选择 **"导出为多个网页文件（含附件）"**
   - ❌ 不要选 **"单个 HTML 文件"**（附件会被 base64 内嵌）
   - ❌ 不要勾选 **"渲染 Markdown 笔记"**（会丢失原始结构）
4. 导出到独立空文件夹（如 `Wiz_Export`）

### 导出后的目录结构

```
Wiz_Export/
├── 笔记本1/
│   ├── 笔记1.html
│   ├── 笔记1_files/      # 该笔记的所有附件（图片、PDF、Word等）
│   └── 笔记2.html
└── 笔记本2/
    ├── 笔记3.html
    └── 笔记3_files/
```

### 导出后检查

- 每个 `.html` 旁应有同名 `_files` 文件夹
- 打开任一 HTML，确认图片/附件能正常显示
- 路径应为相对路径（如 `笔记1_files/xxx.png`）

## 附件迁移脚本说明

### 功能特点

- 批量复制所有 `_Attachments` 目录
- 已存在自动跳过，可重复执行
- 不覆盖现有文件

### 使用方法

在 PowerShell 或 CMD 中运行：

```batch
@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title 批量复制 _Attachments 目录

:: ====================== 请修改这里的路径 ======================
set "SOURCE_DIR=C:\Users\Administrator\Documents\My Knowledge"
set "TARGET_DIR=G:\Data\knowledge\wiz"
:: ==============================================================

echo ==============================================
echo 批量复制 _Attachments 目录
echo 功能：已存在自动跳过，可重复执行，不覆盖
echo ==============================================
echo 源目录：%SOURCE_DIR%
echo 目标目录：%TARGET_DIR%
echo.

set COUNT=0
set SKIP=0

for /d /r "%SOURCE_DIR%" %%d in (*_Attachments) do (
 set "FULL_PATH=%%d"
 set "REL_PATH=!FULL_PATH:%SOURCE_DIR%=!"
 set "DEST_PATH=%TARGET_DIR%!REL_PATH!"

 echo 源目录：!FULL_PATH!
 echo 目标路径：!DEST_PATH!

 if exist "!DEST_PATH!" (
 echo ⏭️ 已存在，跳过：!REL_PATH!
 set /a SKIP+=1
 ) else (
 mkdir "!DEST_PATH!"
 xcopy "!FULL_PATH!\*" "!DEST_PATH!\" /E /H /C /R /Q >nul
 echo ✅ 复制成功：!REL_PATH!
 set /a COUNT+=1
 )
 echo.
)

echo ==============================================
echo 任务完成
echo 本次新增复制：!COUNT! 个
echo 已存在跳过：!SKIP! 个
echo ==============================================

pause
exit /b
```

### 配置说明

修改脚本中的两个路径变量：

```batch
set "SOURCE_DIR=你的为知笔记原始数据目录"
set "TARGET_DIR=你要迁移到的目标目录"
```

## API 接口

### Python 模块调用

```python
from wiz_migration import (
    detect_wiz_data_dir,
    generate_export_guide,
    run_attachment_migration,
    start_wizard
)

# 1. 检测为知笔记数据目录
data_dir = detect_wiz_data_dir()
if not data_dir:
    print("未自动检测到，请手动输入路径")

# 2. 生成导出指南
guide_path = generate_export_guide(
    export_dir="C:/path/to/Wiz_Export",
    output_file="wiz_export_guide.md"
)

# 3. 运行附件迁移
result = run_attachment_migration(
    source_dir="C:/Users/Administrator/Documents/My Knowledge",
    target_dir="G:/Data/knowledge/wiz",
    script_path="scripts/copy_attachments.bat"
)

# 4. 完整向导
start_wizard()
```

## 错误处理

| 错误情况 | 原因 | 解决方案 |
|---------|------|----------|
| 无法自动检测目录 | 非标准安装路径 | 手动输入数据目录路径 |
| 导出路径不存在 | 还未执行导出操作 | 先在为知笔记中导出 HTML |
| 附件复制失败 | 权限不足 | 以管理员身份运行脚本 |
| 中文乱码 | CMD 编码问题 | 确保脚本包含 `chcp 65001` 设置 |

## 注意事项

1. **备份原始数据**：迁移前务必备份整个 `My Knowledge` 目录
2. **导出格式**：必须选择"多个网页文件（含附件）"格式
3. **路径不要包含空格**：或使用引号包裹路径
4. **附件大小**：大附件（>100MB）可能需要较长时间
5. **重复执行**：附件迁移脚本可安全重复运行，不会覆盖已有文件

## 迁移完成检查清单

- [ ] 为知笔记已导出 HTML 到独立文件夹
- [ ] 每个 HTML 文件旁都有对应的 `_files` 文件夹
- [ ] 打开 HTML 能正常显示图片和附件
- [ ] 已运行附件迁移脚本或手动复制
- [ ] 目标目录中所有附件已就位
- [ ] 在浏览器中测试打开的 HTML 文件路径是否正确

## 后续处理

迁移完成后，你可能需要：

1. **转换为 Markdown**：使用 `wiz2md` 等工具将 HTML 转换为 Markdown
2. **导入笔记软件**：如 Obsidian、Logseq、Notion 等
3. **建立双向链接**：在新笔记系统中重建关联
4. **清理重复**：使用去重工具清理重复内容

## 技术细节

### 为知笔记数据目录结构

```
My Knowledge/
├── Data/
│   ├── 账号1/
│   │   ├── index/
│   │   └── attachments/
│   └── 账号2/
└── _Attachments/          # 全局附件目录（部分版本）
```

### 存储目录检测逻辑

```python
def detect_wiz_data_dir():
    """检测标准安装路径"""
    possible_paths = [
        r"C:\Users\Administrator\Documents\My Knowledge\Data",
        r"C:\Users\%USERNAME%\Documents\My Knowledge\Data",
        os.path.expanduser(r"~/Documents/My Knowledge/Data")
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None
```

## 支持

如有问题，请检查：
- 是否为标准安装路径
- 是否已正确导出 HTML 格式
- 是否有足够的文件读写权限
