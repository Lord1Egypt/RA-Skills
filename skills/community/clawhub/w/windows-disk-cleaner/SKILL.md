---
name: win-disk-cleaner
description: "Safe Windows disk cleanup assistant. Scans any drive (defaults to C:), analyzes space usage across temp files, dev caches (npm/pip/conda/docker/gradle/maven), browser caches, Windows Update leftovers, large files, duplicate files, and node_modules. Generates an interactive HTML report with three safety tiers (safe / review / never-touch). Users confirm deletions before any file is removed. Supports Chinese and English."
tags: "windows,disk-cleanup,cache,devtools,system-maintenance,powershell"
metadata:
  openclaw:
    requires:
      bins:
        - powershell
        - python3
    os:
      - windows
---

# Windows 磁盘清理助手

一个安全、全面的 Windows 磁盘清理 skill。核心原则：**先扫描分析，再展示报告，让用户决定删什么**。绝不静默删除任何文件。

支持扫描任意磁盘，默认扫描系统盘（通常是 C:）。用户可以指定盘符，如"帮我看看 D 盘"或"扫描所有磁盘"。对于非系统盘，跳过系统相关的扫描项（Windows Update、系统临时文件等），聚焦于大文件和用户数据分析。

## 工作流程概览

```
扫描 → 分析分类 → 生成报告(HTML) → 用户确认 → 执行清理 → 验证结果
```

## 第一步：环境检测与目标确认

在做任何事之前，先确认运行环境，并确定扫描目标：

```powershell
# 确认是 Windows
$env:OS
# 获取当前用户
$env:USERNAME
# 列出所有磁盘及空间概况，让用户了解全局
Get-PSDrive -PSProvider FileSystem | Format-Table Name, Used, Free, @{N='Total(GB)';E={[math]::Round(($_.Used+$_.Free)/1GB,2)}} -AutoSize
```

然后确认用户要扫描哪个盘：
- 如果用户已指定（如"清理 D 盘"），直接用指定盘符
- 如果用户没指定，默认使用系统盘（`$env:SystemDrive`，通常是 C:），但展示磁盘列表让用户确认
- 如果用户说"全部"或"所有磁盘"，依次扫描每个盘

对于非系统盘，扫描策略有所不同：跳过 Windows Update 缓存、系统临时文件等系统相关项，聚焦于大文件分析、重复文件扫描、用户数据整理。

如果不是 Windows 环境，告知用户此 skill 专为 Windows 设计，并提供对应平台的基本建议。

## 第二步：全面扫描

按以下分类扫描。使用 PowerShell 脚本 `scripts/scan_disk.txt`（见下方说明），或直接在终端执行等效命令。

### 扫描分类

扫描结果分为三个安全等级：

#### 🟢 安全删除（Safe）——缓存和临时文件
这些删了不会丢失任何用户数据，最多影响一些加载速度（缓存会自动重建）：

| 类别 | 典型路径 | 说明 |
|------|---------|------|
| Windows 临时文件 | `%TEMP%`, `C:\Windows\Temp` | 系统和用户临时文件 |
| Windows Update 缓存 | `C:\Windows\SoftwareDistribution\Download` | 已安装更新的安装包 |
| 缩略图缓存 | `%LOCALAPPDATA%\Microsoft\Windows\Explorer\thumbcache_*` | 文件预览缩略图 |
| 系统日志 | `C:\Windows\Logs` 中的旧日志 | 超过30天的日志 |
| 回收站 | 回收站 | 已删除的文件 |
| Windows 错误报告 | `%LOCALAPPDATA%\CrashDumps`, `C:\ProgramData\Microsoft\Windows\WER` | 崩溃转储和错误报告 |
| npm 缓存 | `%APPDATA%\npm-cache` | Node.js 包缓存 |
| pip 缓存 | `%LOCALAPPDATA%\pip\cache` | Python 包缓存 |
| conda 包缓存 | `%USERPROFILE%\.conda\pkgs` 中的 `.tar.bz2`/`.conda` 文件 | 已解压的包的压缩档 |
| NuGet 缓存 | `%LOCALAPPDATA%\NuGet\v3-cache` | .NET 包缓存 |
| Gradle 缓存 | `%USERPROFILE%\.gradle\caches` | Java/Gradle 构建缓存 |
| Maven 本地仓库 | `%USERPROFILE%\.m2\repository` (需谨慎，标记为黄色如果有本地发布的包) | Maven 依赖缓存 |
| Docker 未使用资源 | `docker system df` 检查 | 悬空镜像、停止的容器、未使用的卷 |
| 浏览器缓存 | 各浏览器缓存目录 | Chrome/Edge/Firefox 缓存 |

#### 🟡 需确认（Review）——可能有用户数据
删除前必须逐项或分组展示，让用户选择：

| 类别 | 典型路径 | 说明 |
|------|---------|------|
| 下载文件夹 | `%USERPROFILE%\Downloads` | 按修改时间排序，展示大文件 |
| 桌面大文件 | `%USERPROFILE%\Desktop` | 超过 100MB 的文件 |
| 大文件扫描 | 各用户目录 | 全盘超过 500MB 的文件（排除系统目录） |
| 旧版 Windows | `C:\Windows.old` | 系统升级残留（可能很大） |
| 重复文件 | 用户目录内 | 基于文件大小+部分哈希的重复检测 |
| node_modules | 项目目录中的 node_modules | 长期未访问的项目的依赖 |
| 虚拟环境 | `.venv`, `venv`, `.conda/envs` | 长期未使用的 Python/Conda 环境 |

#### 🔴 不要碰（Never Touch）
以下路径绝不扫描、绝不建议删除：

- `C:\Windows\` （系统核心目录，SoftwareDistribution\Download 除外）
- `C:\Program Files\`, `C:\Program Files (x86)\`
- `C:\ProgramData\`（除明确的缓存子目录外）
- 任何 `.git` 目录
- 任何正在运行的程序的数据目录
- 用户文档、图片、视频目录（除非用户明确要求扫描大文件）

## 第三步：生成交互式报告

扫描完成后，生成一个 HTML 报告文件。报告要做到：

1. **概览面板**：磁盘总量、已用、可用、各分类可回收空间一目了然
2. **安全项汇总**（🟢）：列出所有安全删除项的总大小，一个"全部清理"按钮
3. **需确认项列表**（🟡）：每项带勾选框，显示路径、大小、最后修改时间、说明
4. **生成清理命令**：用户勾选后，页面生成对应的 PowerShell 清理命令，用户复制执行

报告使用 `scripts/generate_report.py` 生成（读取扫描结果 JSON，输出 HTML）。

如果无法生成 HTML（比如环境限制），可在终端中以表格形式展示结果，分三个安全等级列出，逐项询问。

## 第四步：执行清理

根据用户选择，按以下规则执行：

### 安全项批量清理
用户确认后，一次性执行所有安全项的清理：

```powershell
# 示例：清理临时文件
Remove-Item -Path "$env:TEMP\*" -Recurse -Force -ErrorAction SilentlyContinue
# 示例：清理 npm 缓存
npm cache clean --force
# 示例：清理 pip 缓存
pip cache purge
# 示例：Docker 清理
docker system prune -f
```

优先使用工具自带的清理命令（如 `npm cache clean`、`pip cache purge`、`docker system prune`、`conda clean --all`），而不是直接 `Remove-Item`。这样更安全，工具自己知道什么该删什么不该删。

### 确认项逐步清理
对于🟡类别的项目：
- 大文件/重复文件：列出文件清单，让用户逐个或分组确认
- 旧项目依赖：显示项目名称和最后访问时间，让用户选择
- 下载文件夹：按时间排序展示，让用户挑选

### 清理后验证
清理完成后，再次显示磁盘空间变化：

```powershell
# 显示清理前后对比
"清理前可用空间: $beforeFree GB"
"清理后可用空间: $afterFree GB"  
"本次释放空间: $($afterFree - $beforeFree) GB"
```

## 脚本说明

### scripts/scan_disk.txt
主扫描脚本（PowerShell），文件扩展名为 `.txt` 以兼容 ClawHub 注册表的文件类型限制，实际内容是标准的 PowerShell 脚本。

使用方式：读取此文件内容，另存为 `scan_disk.ps1`，然后执行：
```powershell
# 默认扫描系统盘
.\scan_disk.ps1
# 指定盘符
.\scan_disk.ps1 -Drive "D:"
# 指定输出路径和大文件数量
.\scan_disk.ps1 -Drive "C:" -OutputPath ".\result.json" -TopN 100
```

或者直接在终端中按脚本内容逐段执行等效命令。

脚本功能：
- 枚举所有扫描目标路径
- 计算每个路径的占用空间
- 检测开发工具是否安装（npm/pip/conda/docker/gradle等）
- 检测已安装的浏览器
- 区分系统盘和非系统盘（非系统盘跳过系统专属扫描项）
- 输出 JSON 格式的扫描结果

### scripts/generate_report.py
报告生成脚本（Python），负责：
- 读取扫描结果 JSON
- 生成带有交互功能的 HTML 报告
- 报告中包含勾选框、清理命令生成器

用法：
```bash
python scripts/generate_report.py scan_result.json -o cleanup_report.html
```

### references/safe_paths.md
各平台上已知的安全清理路径清单和注意事项，扫描前可参考。

## 关键安全原则

1. **永远先 dry-run**：任何删除操作前，先展示将要删除的内容
2. **永远不碰系统文件**：🔴 列表中的路径是硬性禁区
3. **优先用工具命令**：能用 `npm cache clean` 就不用 `Remove-Item`
4. **保留退路**：对于大批量删除，建议用户先备份或移动到回收站
5. **透明**：每一步操作都告诉用户在做什么、为什么安全
6. **错误处理**：权限不足或文件被占用时优雅跳过，不中断流程

## 对话风格

- 用中文和用户交流（除非用户用英文）
- 扫描过程中给出进度提示
- 展示结果时用清晰的表格和分类
- 对于可能的风险项，主动说明风险
- 语气专业但不啰嗦
