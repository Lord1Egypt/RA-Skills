---
name: openclaw-smart-backup
description: OpenClaw Smart Backup - 智能自动备份 OpenClaw 的配置目录和工作空间。自动感知并跳过大型文件、可下载/可编译生成的文件、临时文件和符号链接，使用 tar.gz 格式合并备份。
metadata:
  openclaw:
    emoji: 🔑
    category: tool
    author: OpenClaw
    version: 1.0.0
    tags: [backup, archive, tar.gz, automation, openclaw]
---

# OpenClaw Smart Backup

## 🎯 一句话定义

自动备份 OpenClaw 配置和工作空间的智能备份技能。通过自动感知排除大型可下载文件、可重新生成的构建产物和临时缓存，生成精简而完整的 `.tar.gz` 备份。

---

## 📞 如何调用 (How to use me)

**触发语句**
- "备份 OpenClaw"
- "使用 openclaw-smart-backup 备份"
- "运行智能备份"
- "预览备份"
- "备份 .openclaw 和 workspace"

**需要提供的信息**
1. **必需参数：** 无，所有路径自动检测
2. **可选参数：**
   - `输出目录` — 备份保存位置，默认 `D:\Personal\Archive`（Windows）或 `~/Archive`
   - `保留数量` — 最多保留 N 个历史备份，默认 30，0=不限制
   - `跳过大文件` — 是否直接跳过超过 100MB 的文件

---

## ⚡ 执行逻辑 (What I do)

当用户激活此技能时，按以下 SOP 执行：

### Step 1: 环境检测
- 检测 `.openclaw` 配置目录（优先级：`%USERPROFILE%\.openclaw`）
- 检测 `workspace` 工作空间（优先级：`D:\Personal\OpenClaw` → `%USERPROFILE%\OpenClaw`）
- 加载/创建 `openclaw_backup.json` 配置
- 检测结果缓存到配置文件，避免每次重复检索

**检查点：**
- 两个目录至少有一个存在
- 如无法检测，提示用户手动指定路径

### Step 2: 智能排除（自动感知）
通过以下多维度自动排除不需备份的内容：

| 类别 | 规则 | 原因 |
|-------|------|------|
| 临时/日志 | `*.log`, `*.tmp`, `*.bak`, `*.pid`, `*.swp` | 运行时生成，无需备份 |
| 版本控制 | `.git`, `.svn`, `.hg` | 远程已托管，本地备份冗余 |
| Python 缓存 | `__pycache__`, `*.pyc`, `*.pyo`, `.mypy_cache` | 可通过源代码重新编译 |
| Node 依赖 | `node_modules`, `.npm`, `.pnpm-store` | 可通过 `package.json` 重新安装 |
| 构建产物 | `dist`, `build`, `.next`, `target`, `out` | 可通过源代码重新构建 |
| 包管理器缓存 | `.nuget`, `.cargo`, `.gradle`, `.m2`, `.yarn` | 可自动重新下载 |
| 虚拟环境 | `.venv`, `venv`, `.tox` | 可通过依赖文件重新创建 |
| 浏览器数据 | `.browser-profile`, `.browser_data` | 缓存数据，体积巨大 |
| 符号链接 | 所有 symlink / junction | 避免循环遍历和冗余 |
| 大型可下载文件 | `*.whl`, `*.exe`, `*.dll`, `*.so`, `*.bin` | 可从官方渠道重新获取 |
| 大型文件 | 单文件 > 100MB | 可配置跳过或包含 |
| OpenClaw 特有 | `skills-backup`, `.clawhub`, `flows`, `.dreams` | 冗余或自动生成 |

**通配符支持：**
- `skills-backup-*` 匹配任何以 `skills-backup-` 开头的文件夹
- `*.egg-info` 匹配所有以 `.egg-info` 结尾的文件夹

**验证标准：**
- 排除后最终备份包含的是源配置、技能文件和核心代码
- 排除规则对用户透明，最终报告中列出排除统计

### Step 3: 创建备份
- 所有源目录合并到单个 `openclaw-backup-YYYYMMDD-HHmmss.tar.gz`
- 使用 Python `tarfile` + `gzip`，零外部依赖
- tar 内部路径保留绝对路径（Windows 盘符 `C:\` 转换为 `C_/` ）
- 每 1000 个文件显示进度
- 遇到权限错误或读取错误时跳过并继续

**验证标准：**
- 备份文件可正常解压并还原
- 压缩后体积显著小于原始总和

### Step 4: 清理过期备份
- 按 `MaxBackups` 保留最近的备份
- 删除超出数量的旧备份文件

### Step 5: 智能感知报告
备份完成后输出：
- 备份文件路径、原始大小、压缩后大小、压缩率
- 文件类型分布（Top 10）
- 排除统计（按类型分类）
- 大型文件警告（如有）
- 跳过的可下载/可编译文件列表（如有）

---

## 📊 输出格式

### 标准输出
```
[OK] 备份完成: D:\Personal\Archive\openclaw-backup-20260513-095600.tar.gz
[INFO] 文件数: 1523, 原始大小: 45.32 MB, 压缩后: 12.85 MB, 压缩率: 28.4%
[INFO] 排除统计: 扩展名=42, 文件夹=15, 文件名=3, 符号链接=0, 大型文件=2, 可下载=5, 总计=67
```

### 示例
```
OpenClaw Smart Backup - 智能感知报告
============================================================

[INFO] 备份文件类型分布 (Top 10):
  .md            234  个  (2.15 MB)
  .py             89  个  (1.23 MB)
  .json           45  个  (0.87 MB)
  .js             32  个  (0.56 MB)
  ...

智能排除说明:
  - 日志/临时文件 (.log, .tmp)            → 运行时生成，无需备份
  - 版本控制目录 (.git)                   → 远程已托管，无需备份
  - Node依赖 (node_modules)               → 可通过 package.json 重新安装
  - 构建产物 (dist, build, .next)         → 可通过源代码重新构建
  ...

============================================================
```

---

## ⚙️ 配置参数

配置文件位置：`%APPDATA%\OpenClaw_Backup\openclaw_backup.json`（Windows）或 `~/.config/openclaw-backup/openclaw_backup.json`

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| config_directory | string | "" (自动检测) | `.openclaw` 配置目录 |
| workspace_directory | string | "" (自动检测) | 工作空间目录 |
| output_directory | string | "D:\\Personal\\Archive" | 备份输出目录 |
| filename_prefix | string | "openclaw-backup" | 备份文件名前缀 |
| max_backups | int | 30 | 保留最近 N 个，0=不限制 |
| max_file_size_mb | int | 100 | 单文件大小警告阈值 |
| skip_large_files | bool | false | true=直接跳过超大文件 |
| compression_level | int | 6 | gzip 压缩级别 1-9 |
| excluded_extensions | list | [见上文] | 排除的文件扩展名 |
| excluded_folders | list | [见上文] | 排除的文件夹名（支持 `*` 通配符） |
| excluded_files | list | [见上文] | 排除的特定文件名 |
| large_downloadable_patterns | list | [见上文] | 大型可下载文件通配符 |

---

## 💭 使用示例

### 示例 1: 基本备份
```
用户: "备份 OpenClaw"
我: 执行 scripts/backup.py，自动检测目录、智能排除、创建 tar.gz、清理过期备份、输出智能感知报告
```

### 示例 2: 预览模式
```
用户: "预览备份"
我: 使用 --dry-run 参数运行，列出将备份的文件列表和预估大小，不实际创建文件
```

### 示例 3: 自定义输出目录
```
用户: "备份到 E:\\Backups"
我: 使用 --output "E:\\Backups" 参数运行备份脚本
```

### 示例 4: 检查排除列表
```
用户: "那些文件被排除了"
我: 使用 --list-excluded 参数（或演示 dry-run 输出）展示被跳过的文件
```

### 示例 5: 命令行直接运行
```bash
python scripts/backup.py
python scripts/backup.py --dry-run
python scripts/backup.py --output D:\Backups --max-backups 10
python scripts/backup.py --skip-large --config-dir C:\Users\Me\.openclaw
```

---

## 📚 相关工具

- [openclaw-backup](https://github.com/JIRBOY/openclaw-backup) — 本技能的 C# 原型实现
- Python `tarfile` — 标准库，无需额外安装

---

_技能版本: v1.0_
_更新日期: 2026-05-13_
