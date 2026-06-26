# OpenClaw Backup / OpenClaw 备份工具

<p align="center">
  <b>Cross-platform backup and restore tool for OpenClaw data</b><br>
  <b>OpenClaw 数据跨平台备份与恢复工具</b>
</p>

> **💬 快速使用 / Quick Start:**
> 
> **安装：**`安装 sen-openclaw-backup skill`
> 
> **备份：**`备份 OpenClaw 数据到桌面，快速备份（不含 skills，约 100MB）或完整备份（含 skills，约 500MB+），并设置每周自动备份`

<p align="center">
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
  </a>
  <img src="https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-blue" alt="Platform">
  <img src="https://img.shields.io/badge/ease%20of%20use-one--click-green" alt="Ease of Use">
</p>

---

## 🎯 What is this? / 这是什么？

**English:**
OpenClaw Backup is a user-friendly tool designed to help you effortlessly backup and migrate your OpenClaw data. Whether you're switching computers, creating backups for safety, or moving between operating systems, this tool makes the process as simple as a few clicks.

**中文：**
OpenClaw Backup 是一个用户友好的工具，旨在帮助您轻松备份和迁移 OpenClaw 数据。无论您是更换电脑、创建安全备份，还是在不同操作系统之间迁移，这个工具都能让过程变得简单到只需几次点击。

---

## ✨ Key Features / 核心特性

| Feature / 特性 | Description / 描述 |
|---------------|-------------------|
| 🖱️ **One-Click Operation / 一键操作** | Double-click to restore on macOS and Windows / macOS 和 Windows 上双击即可恢复 |
| 🖥️ **Cross-Platform / 跨平台** | Works on macOS, Linux, and Windows / 支持 macOS、Linux 和 Windows |
| 📦 **Portable / 便携** | Single compressed file, easy to transfer / 单个压缩文件，易于传输 |
| 🔒 **Complete Backup / 完整备份** | Backs up everything: conversations, memories, configs / 备份所有内容：对话、记忆、配置 |
| ⚡ **Flexible / 灵活** | Choose quick or full backup based on your needs / 根据需求选择快速或完整备份 |
| 🚀 **Auto-Install / 自动安装** | Automatically installs OpenClaw if missing / 如果未安装，自动安装 OpenClaw |

---

## 🚀 Quick Start / 快速开始

### For Beginners / 新手推荐

**English:**
Don't want to use command line? No problem! We provide double-click scripts:

**中文：**
不想使用命令行？没问题！我们提供了双击运行的脚本：

#### macOS
1. Insert your backup drive / 插入备份硬盘
2. Double-click `恢复OpenClaw.command` / 双击 `恢复OpenClaw.command`
3. Wait for completion / 等待完成
4. Done! / 完成！

#### Windows
1. Insert your backup drive / 插入备份硬盘
2. Double-click `恢复OpenClaw-Windows.bat` / 双击 `恢复OpenClaw-Windows.bat`
3. Wait for completion / 等待完成
4. Done! / 完成！

---

### For Advanced Users / 高级用户

#### macOS / Linux

```bash
# Quick backup (~100MB) / 快速备份（约100MB）
./scripts/backup.sh /Volumes/YourSSD/backup.tar.gz

# Full backup with skills (~500MB+) / 完整备份（约500MB+）
INCLUDE_SKILLS=1 ./scripts/backup.sh /Volumes/YourSSD/backup.tar.gz

# Restore / 恢复
./scripts/restore.sh /Volumes/YourSSD/backup.tar.gz
```

#### Windows

```cmd
# Quick backup / 快速备份
scripts\backup-windows.bat D:\backup.tar.gz

# Full backup / 完整备份
set INCLUDE_SKILLS=1
scripts\backup-windows.bat D:\backup.tar.gz

# Restore / 恢复
scripts\restore-windows.bat D:\backup.tar.gz
```

---

## 📋 What Gets Backed Up? / 备份内容

| Content / 内容 | Description / 描述 | Optional / 可选 |
|---------------|-------------------|----------------|
| `workspace/` | Project files, memory files, configurations / 项目文件、记忆文件、配置 | ✅ Yes / 是 |
| `agents/` | Conversation history and sessions / 对话历史和会话 | ✅ Yes / 是 |
| `memory/` | Long-term memory embeddings / 长期记忆嵌入 | ✅ Yes / 是 |
| `credentials/` | Encrypted credentials / 加密凭证 | ✅ Yes / 是 |
| `openclaw.json` | Main configuration file / 主配置文件 | ✅ Yes / 是 |
| `skills/` | Installed skills (~1.5GB) / 已安装技能（约1.5GB） | ✅ Yes / 是 |

**Note / 说明:**
- **Quick Backup / 快速备份**: Excludes skills (~100MB, skills can be re-downloaded via `clawhub sync`) / 不包含技能（约100MB，可通过 `clawhub sync` 重新下载）
- **Full Backup / 完整备份**: Includes everything including skills (~500MB+) for offline use / 包含所有内容包括技能（约500MB+），可离线使用

---

## 🔄 Migration Workflow / 迁移流程

### Step 1: Backup / 步骤1：备份

**English:**
Run the backup script on your old machine:

**中文：**
在旧电脑上运行备份脚本：

```bash
./scripts/backup.sh /Volumes/SSD/openclaw-backup.tar.gz
```

**Output / 输出:**
```
✅ Backup complete!
   File: /Volumes/SSD/openclaw-backup-20260318-200825.tar.gz
   Size: 536MB
```

### Step 2: Transfer / 步骤2：传输

**English:**
Copy the backup file to your new computer via USB drive, cloud storage, or network.

**中文：**
通过 U 盘、云存储或网络将备份文件复制到新电脑。

### Step 3: Restore / 步骤3：恢复

**English:**
Choose your preferred method:

**中文：**
选择您喜欢的方式：

**Option A: Double-Click (Easiest) / 选项A：双击（最简单）**
- macOS: Double-click `恢复OpenClaw.command`
- Windows: Double-click `恢复OpenClaw-Windows.bat`

**Option B: Command Line / 选项B：命令行**
```bash
./scripts/restore.sh /Volumes/SSD/openclaw-backup.tar.gz
```

**The restore script will / 恢复脚本将：**
1. ✅ Check for existing data and back it up / 检查现有数据并备份
2. ✅ Install OpenClaw if not present / 如果未安装，自动安装 OpenClaw
3. ✅ Extract all data / 解压所有数据
4. ✅ Start the Gateway / 启动 Gateway

---

## 💡 Why Use This Tool? / 为什么使用这个工具？

### Ease of Use / 易用性

**English:**
- **No technical knowledge required** - Double-click scripts handle everything
- **Automatic detection** - Detects existing data and preserves it
- **Smart installation** - Installs OpenClaw automatically if missing
- **Cross-platform** - Same backup works on macOS, Linux, and Windows

**中文：**
- **无需技术知识** - 双击脚本处理一切
- **自动检测** - 检测现有数据并保留
- **智能安装** - 如果缺少 OpenClaw 自动安装
- **跨平台** - 相同的备份可在 macOS、Linux 和 Windows 上使用

### Safety / 安全性

**English:**
- **Non-destructive** - Existing data is backed up before overwrite
- **Encrypted credentials preserved** - Your API keys remain secure
- **Complete conversation history** - Never lose your chat history
- **Portable format** - Single file, easy to store and transfer

**中文：**
- **非破坏性** - 覆盖前自动备份现有数据
- **保留加密凭证** - 您的 API 密钥保持安全
- **完整对话历史** - 永不丢失聊天记录
- **便携格式** - 单个文件，易于存储和传输

---

## 📦 Installation / 安装

### As an OpenClaw Skill / 作为 OpenClaw Skill 安装

```bash
# Install from GitHub / 从 GitHub 安装
clawhub install https://github.com/Sen-platotech/openclaw-backup

# Or download and install manually / 或下载后手动安装
curl -L https://github.com/Sen-platotech/openclaw-backup/archive/refs/heads/main.zip -o openclaw-backup.zip
unzip openclaw-backup.zip
```

### Standalone Usage / 独立使用

```bash
# Clone the repository / 克隆仓库
git clone https://github.com/Sen-platotech/openclaw-backup.git
cd openclaw-backup

# Run scripts directly / 直接运行脚本
./scripts/backup.sh ~/Desktop/backup.tar.gz
```

---

## 🛠️ Requirements / 系统要求

| Platform / 平台 | Requirements / 要求 |
|----------------|-------------------|
| **macOS** | macOS 10.14+, Bash, tar |
| **Linux** | Any distribution, Bash, tar |
| **Windows** | Windows 10 build 17063+ (for tar), Node.js/npm |

---

## 📝 Example Scenarios / 使用场景

### Scenario 1: New Computer / 场景1：新电脑

**English:**
> You bought a new Mac and want to move all your OpenClaw data.

**中文：**
> 您购买了一台新 Mac，想要迁移所有 OpenClaw 数据。

**Solution / 解决方案:**
1. Old Mac: Run backup script / 旧 Mac：运行备份脚本
2. Copy file to new Mac / 将文件复制到新 Mac
3. New Mac: Double-click restore script / 新 Mac：双击恢复脚本
4. Done! All conversations and settings preserved. / 完成！所有对话和设置都已保留。

### Scenario 2: System Reinstall / 场景2：系统重装

**English:**
> You need to reinstall your operating system.

**中文：**
> 您需要重新安装操作系统。

**Solution / 解决方案:**
1. Backup to external drive / 备份到外部硬盘
2. Reinstall OS / 重装系统
3. Restore from backup / 从备份恢复
4. Everything is back exactly as before. / 一切恢复原样。

### Scenario 3: Cross-Platform Migration / 场景3：跨平台迁移

**English:**
> Switching from Windows to macOS (or vice versa).

**中文：**
> 从 Windows 切换到 macOS（或反之）。

**Solution / 解决方案:**
1. Create backup on source machine / 在源机器创建备份
2. Transfer to destination machine / 传输到目标机器
3. Use platform-specific restore script / 使用平台特定的恢复脚本
4. Works seamlessly across platforms! / 跨平台无缝工作！

---

## 🤝 Contributing / 贡献

**English:**
Contributions are welcome! Please feel free to submit a Pull Request.

**中文：**
欢迎贡献！请随时提交 Pull Request。

---

## 📄 License / 许可证

**English:**
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**中文：**
本项目采用 MIT 许可证 - 详情请参见 [LICENSE](LICENSE) 文件。

---

<p align="center">
  <b>Made with ❤️ for the OpenClaw community</b><br>
  <b>为 OpenClaw 社区用心制作</b>
</p>
