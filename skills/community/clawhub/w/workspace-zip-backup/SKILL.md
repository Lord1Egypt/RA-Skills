---
name: workspace-zip-backup
description: "OpenClaw workspace 核心 markdown 文件快速压缩备份与还原工具，只备份 .md 文件并保持文件夹结构 | Fast backup & restore tool for OpenClaw workspace core markdown files, preserves directory structure"
metadata:
  author: OpenClaw
  tags: backup, compression, markdown, workspace
---

# Workspace Backup Skill | Workspace 备份技能

OpenClaw workspace 核心文件快速备份技能。只压缩备份所有 markdown 文件（核心笔记、技能文档、记忆文件等），保持原始文件夹结构，便于迁移和还原。

Fast backup tool for OpenClaw workspace core files. Only compress markdown files (notes, skill docs, memory files) while preserving original directory structure for migration and restore.

## Features | 功能特点

- 🎯 **Only core content | 只备份核心内容** - Only `.md` files are included, ignores binaries, node_modules, build outputs
  仅搜索并压缩所有 `.md` 文件，忽略二进制文件、node_modules、构建输出等
- 📁 **Preserve directory structure | 保持文件夹结构** - Full directory structure is kept in zip, automatically restored on unzip
  压缩包保留完整目录结构，解压后自动还原
- ⚡ **Fast compression | 快速压缩** - Based on `zip` command, high performance
  基于 `zip` 命令，压缩速度快
- 🔄 **Complete restore | 完整还原** - Just unzip to recover all files and structure
  解压即可恢复所有文件和目录结构

## Use Cases | 使用场景

- Migrate workspace to new machine | 迁移 workspace 到新机器
- Regular backup of core notes and skills | 定期备份核心笔记和技能
- Share your skills and notes with others | 分享你的技能和笔记给他人
- Slim down backup before transfer | 传输前瘦身备份，只保留文本内容

## Backup Script `backup-workspace.sh` | 备份脚本

### Script Code | 脚本代码

```bash
#!/bin/bash
# workspace-backup - Backup all markdown files from OpenClaw workspace keeping directory structure
# workspace-backup - 备份 OpenClaw workspace 中所有 markdown 文件，保持目录结构

set -euo pipefail

# Default configuration | 默认配置
SOURCE_DIR="${1:-$HOME/.openclaw/workspace}"  # Source directory | 源文件夹，默认: ~/.openclaw/workspace
OUTPUT_ZIP="${2:-workspace-backup-$(date +%Y%m%d).zip}"  # Output zip file | 输出zip文件，默认按日期命名

show_help() {
    echo "Usage | 用法: ./backup-workspace.sh [source_dir] [output_zip]"
    echo ""
    echo "Parameters | 参数:"
    echo "  source_dir    Directory to backup (default: ~/.openclaw/workspace)"
    echo "               要备份的文件夹 (默认: ~/.openclaw/workspace)"
    echo "  output_zip    Output zip file path (default: workspace-backup-YYYYMMDD.zip)"
    echo "               输出压缩包路径 (默认: workspace-backup-YYYYMMDD.zip)"
    echo ""
    echo "Examples | 示例:"
    echo "  ./backup-workspace.sh"
    echo "                          Backup default workspace to date-named zip"
    echo "                          备份默认workspace到当前日期压缩包"
    echo "  ./backup-workspace.sh ~/my-notes my-notes-backup.zip"
    echo "                          Backup specified directory"
    echo "                          备份指定文件夹"
    exit 1
}

# Check for help | 检查帮助参数
if [ "$#" -ge 1 ] && [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    show_help
fi

# Check source directory exists | 检查源文件夹是否存在
if [ ! -d "$SOURCE_DIR" ]; then
    echo "Error | 错误: Source directory '$SOURCE_DIR' does not exist or is not a directory"
    echo "        源文件夹 '$SOURCE_DIR' 不存在或不是目录"
    exit 1
fi

echo "====== Workspace Markdown Backup ======"
echo "Source Directory | 源文件夹: $SOURCE_DIR"
echo "Output File | 输出文件: $OUTPUT_ZIP"
echo ""
echo "Searching for all .md files... | 正在搜索所有 .md 文件..."

# Count markdown files | 统计markdown文件数量
MD_COUNT=$(find "$SOURCE_DIR" -type f -name "*.md" | wc -l)

if [ "$MD_COUNT" -eq 0 ]; then
    echo "No .md files found, exiting. | 未找到任何 .md 文件，退出"
    exit 0
fi

echo "Found $MD_COUNT .md files, starting compression... | 找到 $MD_COUNT 个 .md 文件，开始压缩..."
echo ""

# Compress using zip, keep directory structure | 使用zip压缩，保持目录结构
find "$SOURCE_DIR" -type f -name "*.md" | xargs zip -r "$OUTPUT_ZIP"

echo ""
echo "✅ Backup completed! | 备份完成!"
echo "Archive | 压缩包: $OUTPUT_ZIP"
echo "Contains $MD_COUNT .md files, original directory structure preserved. | 包含 $MD_COUNT 个 .md 文件，保持原始文件夹结构"

# Show compressed size | 显示压缩后大小
SIZE=$(du -h "$OUTPUT_ZIP" | cut -f1)
echo "Compressed size | 压缩后大小: $SIZE"
```

### Usage | 使用方式

When needed, copy the script code above to a file:
需要使用时，复制上面的脚本代码保存为文件即可：

```bash
# Copy script code from this SKILL.md | 复制本文件中备份脚本代码块内容
cat > backup-workspace << 'EOF'
[paste script code here | 在这里粘贴脚本代码]
EOF
chmod +x backup-workspace
mv backup-workspace ~/.local/bin/
```

## Restore Script `restore-workspace.sh` | 还原脚本

### Script Code | 脚本代码

```bash
#!/bin/bash
# workspace-restore - Restore markdown files from backup zip
# workspace-restore - 从备份压缩包还原 markdown 文件

set -euo pipefail

# Default configuration | 默认配置
BACKUP_ZIP="${1:-}"  # Backup zip file | 备份zip文件，必填
TARGET_DIR="${2:-$HOME/.openclaw/workspace}"  # Target directory | 目标文件夹，默认: ~/.openclaw/workspace

show_help() {
    echo "Usage | 用法: ./restore-workspace.sh <backup_zip> [target_dir]"
    echo ""
    echo "Parameters | 参数:"
    echo "  backup_zip    Backup zip file to restore (required)"
    echo "               要还原的压缩包 (必填)"
    echo "  target_dir    Directory to restore to (default: ~/.openclaw/workspace)"
    echo "               还原到哪个文件夹 (默认: ~/.openclaw/workspace)"
    echo ""
    echo "Examples | 示例:"
    echo "  ./restore-workspace.sh workspace-backup-20260316.zip"
    echo "                          Restore to default workspace"
    echo "                          还原到默认workspace"
    echo "  ./restore-workspace.sh my-notes-backup.zip ~/new-workspace"
    echo "                          Restore to specified location"
    echo "                          还原到指定位置"
    exit 1
}

# Check for help | 检查帮助参数
if [ "$#" -eq 0 ] || [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    show_help
fi

# Check backup file exists | 检查备份文件是否存在
if [ ! -f "$BACKUP_ZIP" ]; then
    echo "Error | 错误: Backup file '$BACKUP_ZIP' does not exist"
    echo "        备份文件 '$BACKUP_ZIP' 不存在"
    exit 1
fi

# Check target directory | 检查目标文件夹
if [ ! -d "$TARGET_DIR" ]; then
    echo "Target directory '$TARGET_DIR' does not exist, creating... | 目标文件夹 '$TARGET_DIR' 不存在，创建它..."
    mkdir -p "$TARGET_DIR"
fi

echo "====== Workspace Markdown Restore ======"
echo "Backup File | 备份文件: $BACKUP_ZIP"
echo "Target Directory | 目标文件夹: $TARGET_DIR"
echo ""
echo "Listing archive contents... | 正在列出压缩包内容..."
echo ""

# List contents before restoring | 还原前列出内容供用户确认
unzip -l "$BACKUP_ZIP"

echo ""
echo "Continue restore? (y/N) | 是否继续还原? (y/N)"
read -r CONFIRM || CONFIRM="N"
if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    echo "Cancelled. | 已取消"
    exit 0
fi

echo ""
echo "Starting restore... | 开始还原..."
echo ""

# Restore with unzip - extracts to correct directory structure automatically
# 使用unzip还原 - 自动解压到正确的目录结构
unzip -o "$BACKUP_ZIP"

echo ""
echo "✅ Restore completed! | 还原完成!"
echo "All files restored with original directory structure. | 所有文件已还原，保持原始文件夹结构"

# Count restored files | 统计还原文件数量
RESTORED_COUNT=$(unzip -l "$BACKUP_ZIP" | grep -c "\.md$")
echo "Total $RESTORED_COUNT .md files restored. | 共还原 $RESTORED_COUNT 个 .md 文件"
```

### Usage | 使用方式

When needed, copy the script code above to a file:
需要使用时，复制上面的脚本代码保存为文件即可：

```bash
# Copy script code from this SKILL.md | 复制本文件中还原脚本代码块内容
cat > restore-workspace << 'EOF'
[paste script code here | 在这里粘贴脚本代码]
EOF
chmod +x restore-workspace
mv restore-workspace ~/.local/bin/
```

## Working Principle | 工作原理

### Backup Logic | 备份逻辑

1. **Parameter parsing | 参数解析** - Accepts source directory and output path, provides defaults
   接受源文件夹和输出文件路径，提供默认值
2. **File search | 文件搜索** - Recursively search all markdown files using `find <dir> -type f -name "*.md"`
   使用 `find <dir> -type f -name "*.md"` 递归搜索所有 markdown 文件
3. **Count check | 数量检查** - Exit early if no markdown files found
   如果没有找到 md 文件提前退出
4. **Compression | 压缩打包** - Pass found files to `zip -r` via `xargs`, zip automatically preserves directory structure
   通过 `xargs` 将找到的文件传给 `zip -r`，zip 自动保持相对路径结构
5. **Summary output | 统计输出** - Show compressed size and file count
   显示压缩包大小和文件数量

### Restore Logic | 还原逻辑

1. **Parameter check | 参数检查** - Verify backup file exists, create target directory if not exists
   验证备份文件存在，创建目标文件夹（如果不存在）
2. **Preview content | 预览内容** - List archive contents with `unzip -l` for user confirmation
   还原前用 `unzip -l` 列出压缩包内容，让用户确认
3. **User confirmation | 用户确认** - Requires `y` confirmation before restoring to prevent accidental operation
   需要用户输入 `y` 确认才开始还原，避免误操作
4. **Extract restore | 解压还原** - Use `unzip -o` to extract, since full paths are already stored in archive, it automatically restores directory structure
   使用 `unzip -o` 解压，因为压缩包里已经保存了完整路径，自动还原目录结构
5. **Summary output | 统计输出** - Show completion message and file count
   显示还原完成和文件数量

## Multiple Workspaces (Multi-Agent Scenarios) | 多 Workspace 处理（多 Agent 场景）

### Problem Description | 问题描述

When multiple agents are running in the same environment, each agent may have its own independent workspace. This tool supports backing up any of them.
当多个 agent 在同一环境运行时，每个 agent 可能有独立的 workspace。本工具支持备份任意一个。

### Backup Strategy | 备份策略

1. **Explicitly specify source directory | 显式指定源文件夹**
   Always specify the source directory parameter when backing up non-default workspaces:
   备份非默认 workspace 时，始终显式指定源文件夹参数：
   ```bash
   backup-workspace /path/to/your/workspace backup-$(whoami)-workspace.zip
   ```

2. **Backup multiple workspaces separately | 分别备份多个 workspace**
   For multiple workspaces, backup one by one with different output names:
   对于多个 workspace，使用不同输出名称分别备份：
   ```bash
   backup-workspace ~/workspace-agent1 backup-agent1.zip
   backup-workspace ~/workspace-agent2 backup-agent2.zip
   ```

3. **Include workspace name in backup filename | 在备份文件名中包含 workspace 标识**
   Recommend naming format: `workspace-backup-[username|agentname]-YYYYMMDD.zip`
   推荐命名格式：`workspace-backup-[用户名|agent名]-YYYYMMDD.zip`

### Restore Strategy | 还原策略

1. **Restore to correct target directory | 还原到正确目标目录**
   When restoring a backup from a specific workspace, explicitly specify the target directory:
   还原特定 workspace 的备份时，显式指定目标目录：
   ```bash
   restore-workspace backup-agent1.zip /path/to/new/agent1/workspace
   ```

2. **Cross-agent migration | 跨 agent 迁移**
   If you want to move a workspace from one agent to another:
   如果要将 workspace 从一个 agent 迁移到另一个 agent：
   ```bash
   # On source agent | 在源 agent 上备份
   backup-workspace /path/to/source/workspace migration.zip

   # Transfer migration.zip to target machine, then on target agent | 传输到目标机器后，在目标 agent 上还原
   restore-workspace migration.zip /path/to/target/workspace
   ```

## Examples | 使用示例

### Backup default workspace | 备份默认 workspace

```bash
backup-workspace
```

Example output | 输出示例:
```
====== Workspace Markdown Backup ======
Source Directory | 源文件夹: /root/.openclaw/workspace
Output File | 输出文件: workspace-backup-20260316.zip

Searching for all .md files... | 正在搜索所有 .md 文件...
Found 42 .md files, starting compression... | 找到 42 个 .md 文件，开始压缩...

  adding: ... (stored 0%)
  ...

✅ Backup completed! | 备份完成!
Archive | 压缩包: workspace-backup-20260316.zip
Contains 42 .md files, original directory structure preserved. | 包含 42 个 .md 文件，保持原始文件夹结构
Compressed size | 压缩后大小: 1.2M
```

### Backup specified directory | 备份指定文件夹

```bash
backup-workspace ~/my-notes my-notes-backup.zip
```

### Restore backup | 还原备份

```bash
restore-workspace workspace-backup-20260316.zip
```

It will list contents first then ask for confirmation | 会先列出压缩包内容，然后询问确认:
```
... (list of files)
Continue restore? (y/N) | 是否继续还原? (y/N)
y
Starting restore... | 开始还原...
✅ Restore completed! | 还原完成!
```

### Restore to custom location | 还原到自定义位置

```bash
mkdir -p ~/new-workspace
unzip workspace-backup-20260316.zip -d ~/new-workspace
```

## Compatibility | 兼容性

### Linux / macOS | Linux / macOS

- Works out of the box with built-in `find`, `zip`, `unzip`
- 原生支持，系统自带 `find`、`zip`、`unzip` 即可运行
- If `zip` not installed: Ubuntu/Debian `apt install zip unzip`
- 如果缺少 zip：Ubuntu/Debian 执行 `apt install zip unzip`

### Windows | Windows

#### Option 1: WSL (Recommended) | 方案 1: WSL（推荐）

Running in Windows Subsystem for Linux is fully compatible, same as Linux usage:
在 Windows 子系统 for Linux (WSL) 中运行完全兼容，使用方法和 Linux 相同。

#### Option 2: Git Bash / MinGW | 方案 2: Git Bash / MinGW

`find`, `zip`, `unzip` commands are available in Git Bash, scripts work with minor adjustments:
Git Bash / MinGW 环境通常包含 `find`、`zip`、`unzip` 命令，脚本只需微调路径即可工作：
- Convert paths from `C:\` to `/c/` format
- 将 Windows 路径 `C:\` 转换为 `/c/` 格式
- Line endings must be LF (not CRLF) when saving script
- 保存脚本时行结尾必须是 LF（不是 CRLF）

#### Option 3: PowerShell Port | 方案 3: PowerShell 移植

Reference the logic above and port to PowerShell:
参考上述逻辑移植为 PowerShell：

```powershell
# PowerShell equivalent logic:
# PowerShell 等价逻辑：

# 1. Find all .md files | 查找所有 .md 文件
$mdFiles = Get-ChildItem -Path $sourceDir -Recurse -Filter "*.md"

# 2. Compress with Compress-Archive | 使用 Compress-Archive 压缩
$mdFiles | Compress-Archive -DestinationPath $outputZip

# 3. For restore | 还原时
# Expand-Archive -Path $backupZip -DestinationPath $targetDir
```

Key differences | 主要区别:
- PowerShell natively preserves directory structure
- PowerShell 原生保持目录结构
- Use `Get-ChildItem -Recurse` instead of `find`
- 使用 `Get-ChildItem -Recurse` 替代 `find`
- Use `Compress-Archive`/`Expand-Archive` instead of `zip`/`unzip`
- 使用 `Compress-Archive`/`Expand-Archive` 替代 `zip`/`unzip`

## Dependencies | 依赖

- `zip` - Compression | 压缩 (Ubuntu/Debian: `apt install zip`)
- `unzip` - Extraction | 解压 (Ubuntu/Debian: `apt install unzip`)

## File Structure | 文件结构

```
skills/workspace-backup/
└── SKILL.md              # Skill document (this file, contains all logic and code)
                          # 技能文档（本文件，包含全部逻辑描述和脚本代码）
```

This skill **contains only this single markdown file**. All backup and restore logic is described in this document, code is provided as code blocks. Copy code blocks to executable files when needed.
本技能**仅包含这一个 markdown 文件**，所有备份和还原逻辑都在此文档中描述，代码以代码块形式提供。使用时复制代码块保存为可执行文件即可。

## Notes | 注意事项

1. **Path handling | 路径处理** - If you backup with absolute paths, it will restore to the same paths
   备份时如果使用绝对路径，还原时也会还原到相同路径
2. **Incremental backup | 增量备份** - Reusing the same zip file will append files, recommend date-based naming
   重复备份到同一个zip会追加文件，建议使用日期命名
3. **Large file exclusion | 大文件排除** - Script only includes `.md` files, automatically ignores images, videos, node_modules, git data etc.
   脚本只备份 `.md`，会自动忽略图片、视频、node_modules、git 数据等
4. **Permissions | 权限** - Restoring to system directories requires appropriate permissions, no sudo needed for restoring to user home directory
   还原到系统目录需要适当权限，普通用户还原到自己的 home 目录不需要 sudo

## Best Practices | 最佳实践

- **Regular backup | 定期备份** - Backup workspace core content once a week
  每周备份一次 workspace 核心内容
- **Naming convention | 命名规范** - Use `workspace-backup-YYYYMMDD.zip` format for easy identification
  使用 `workspace-backup-YYYYMMDD.zip` 格式便于识别
- **Offine storage | 离线存储** - Save backup archive to another location to prevent accidental data loss
  将备份压缩包保存到其他地方，防止意外丢失
- **Test restore | 还原测试** - Test restore after backing up important data
  重要备份后建议测试一下能否正常还原

## Prompt Examples | 技能使用提示词示例

Here are common prompt examples when using this skill in AI agents:
以下是在 AI agent 中使用此技能时的常见提示词示例：

### Example 1: Backup current workspace | 示例 1: 备份当前 workspace

```
使用 workspace-backup 技能帮我备份当前 OpenClaw workspace 所有 markdown 文件
Use the workspace-backup skill to backup all markdown files in current OpenClaw workspace
```

### Example 2: Backup custom directory | 示例 2: 备份自定义目录

```
帮我备份 ~/my-notes 目录下所有 markdown 文件，保存为 my-notes-backup.zip
Help me backup all markdown files under ~/my-notes directory, save as my-notes-backup.zip
```

### Example 3: Restore backup | 示例 3: 还原备份

```
使用 workspace-backup 技能帮我还原 backup-20260316.zip 到当前 workspace
Use the workspace-backup skill to restore backup-20260316.zip to current workspace
```

### Example 4: Migrate between workspaces | 示例 4: 在 workspace 之间迁移

```
我要将这个 workspace 的所有 markdown 文件迁移到另一个机器的新 workspace，请帮我创建备份
I need to migrate all markdown files from this workspace to a new workspace on another machine, help me create the backup
```

### Example 5: Multi-agent backup | 示例 5: 多 agent 备份

```
我这里有三个不同的 workspace，帮我分别备份它们，每个使用不同的文件名
I have three different workspaces here, help me backup them separately with different filenames
```

### Example 6: Windows WSL backup | 示例 6: Windows WSL 备份

```
在 Windows WSL 环境下，帮我备份 /home/user/workspace 所有 markdown 文件
In Windows WSL environment, help me backup all markdown files in /home/user/workspace
```

## How Agents Use This Skill | Agent 如何使用本技能

When user asks for backup/restore, agent should follow these steps:
当用户请求备份/还原时，agent 应遵循以下步骤：

1. **Read this SKILL.md | 阅读本技能文档** - Understand backup and restore logic
   理解备份和还原逻辑
2. **Create script file | 创建脚本文件** - Copy corresponding script code from this document to executable file
   从本文档复制相应的脚本代码到可执行文件
3. **Add execution permission | 添加执行权限** - `chmod +x <script-file>`
4. **Run script with correct parameters | 使用正确参数运行脚本** - Confirm parameters with user if unclear
   如果参数不明确，与用户确认
5. **Verify result | 验证结果** - Check the output to ensure backup/restore succeeded
   检查输出来确保备份/还原成功