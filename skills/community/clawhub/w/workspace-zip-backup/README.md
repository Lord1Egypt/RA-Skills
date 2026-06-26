# workspace-zip-backup

## 简介 | Introduction

OpenClaw workspace 核心 markdown 文件快速压缩备份与还原工具，只备份 .md 文件并保持文件夹结构。

Fast backup & restore tool for OpenClaw workspace core markdown files, preserves directory structure.

## 功能特点 | Features

- 🎯 **只备份核心内容** - 仅搜索并压缩所有 `.md` 文件，忽略二进制文件、node_modules、构建输出等
- 📁 **保持文件夹结构** - 压缩包保留完整目录结构，解压后自动还原
- ⚡ **快速压缩** - 基于 `zip` 命令，压缩速度快
- 🔄 **完整还原** - 解压即可恢复所有文件和目录结构

- 🎯 **Only core content** - Only `.md` files are included, ignores binaries, node_modules, build outputs
- 📁 **Preserve directory structure** - Full directory structure is kept in zip, automatically restored on unzip
- ⚡ **Fast compression** - Based on `zip` command, high performance
- 🔄 **Complete restore** - Just unzip to recover all files and structure

## 安装方法 | Installation

从 SKILL.md 文件中复制备份和还原脚本代码：

Copy the backup and restore scripts from SKILL.md:

```bash
# 备份脚本 | Backup script
cat > backup-workspace << 'EOF'
[paste backup script code here | 在这里粘贴备份脚本代码]
EOF
chmod +x backup-workspace
mv backup-workspace ~/.local/bin/

# 还原脚本 | Restore script
cat > restore-workspace << 'EOF'
[paste restore script code here | 在这里粘贴还原脚本代码]
EOF
chmod +x restore-workspace
mv restore-workspace ~/.local/bin/
```

## 使用示例 | Usage Examples

### 备份默认 workspace | Backup default workspace

```bash
backup-workspace
```

### 备份指定文件夹 | Backup specified directory

```bash
backup-workspace ~/my-notes my-notes-backup.zip
```

### 还原备份 | Restore backup

```bash
restore-workspace workspace-backup-20260316.zip
```

### 还原到自定义位置 | Restore to custom location

```bash
restore-workspace workspace-backup-20260316.zip ~/new-workspace
```

## 兼容性 | Compatibility

### Linux / macOS

- 原生支持，系统自带 `find`、`zip`、`unzip` 即可运行
- 如果缺少 zip：Ubuntu/Debian 执行 `apt install zip unzip`

- Works out of the box with built-in `find`, `zip`, `unzip`
- If `zip` not installed: Ubuntu/Debian `apt install zip unzip`

### Windows

#### 方案 1: WSL（推荐）

在 Windows 子系统 for Linux (WSL) 中运行完全兼容，使用方法和 Linux 相同。

Running in Windows Subsystem for Linux is fully compatible, same as Linux usage.

#### 方案 2: Git Bash / MinGW

Git Bash / MinGW 环境通常包含 `find`、`zip`、`unzip` 命令，脚本只需微调路径即可工作。

`find`, `zip`, `unzip` commands are available in Git Bash, scripts work with minor adjustments.

#### 方案 3: PowerShell 移植

参考 SKILL.md 文件中的 PowerShell 等价逻辑进行移植。

Reference the PowerShell equivalent logic in SKILL.md for porting.

## 依赖 | Dependencies

- `zip` - 压缩 (Ubuntu/Debian: `apt install zip`)
- `unzip` - 解压 (Ubuntu/Debian: `apt install unzip`)

## 最佳实践 | Best Practices

- **定期备份** - 每周备份一次 workspace 核心内容
- **命名规范** - 使用 `workspace-backup-YYYYMMDD.zip` 格式便于识别
- **离线存储** - 将备份压缩包保存到其他地方，防止意外丢失
- **还原测试** - 重要备份后建议测试一下能否正常还原

- **Regular backup** - Backup workspace core content once a week
- **Naming convention** - Use `workspace-backup-YYYYMMDD.zip` format for easy identification
- **Offline storage** - Save backup archive to another location to prevent accidental data loss
- **Test restore** - Test restore after backing up important data

## 注意事项 | Notes

1. **路径处理** - 备份时如果使用绝对路径，还原时也会还原到相同路径
2. **增量备份** - 重复备份到同一个zip会追加文件，建议使用日期命名
3. **大文件排除** - 脚本只备份 `.md`，会自动忽略图片、视频、node_modules、git 数据等
4. **权限** - 还原到系统目录需要适当权限，普通用户还原到自己的 home 目录不需要 sudo

1. **Path handling** - If you backup with absolute paths, it will restore to the same paths
2. **Incremental backup** - Reusing the same zip file will append files, recommend date-based naming
3. **Large file exclusion** - Script only includes `.md` files, automatically ignores images, videos, node_modules, git data etc.
4. **Permissions** - Restoring to system directories requires appropriate permissions, no sudo needed for restoring to user home directory

## 文件结构 | File Structure


本项目**仅包含 SKILL.md 一个 markdown 文件**，所有备份和还原逻辑都在此文档中描述，代码以代码块形式提供。使用时复制代码块保存为可执行文件即可。

This project **contains only this single markdown file**. All backup and restore logic is described in this document, code is provided as code blocks. Copy code blocks to executable files when needed.