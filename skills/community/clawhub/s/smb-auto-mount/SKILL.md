---
name: smb-auto-mount
description: Auto-mount Windows SMB shares on Linux with systemd automount. Credentials entered interactively. Required binaries: mount.cifs (cifs-utils), smbclient. Requires sudo. Modifies /etc/fstab and /etc/smb-creds-*.txt.
---

# smb-auto-mount

Mount Windows SMB shares on Linux with on-demand automount.

⚠️ **Security Notice**: Passwords are entered interactively (secure prompt). Never pass passwords via command line arguments.

---

## Security & Permissions / 安全与权限

**⚠️ WARNING / 警告**

- **Requires sudo/root**: All scripts modify system-level configurations
- **Modifies /etc/fstab**: Persistent changes to system mount configuration
- **Creates credential files**: Stores passwords in `/etc/smb-creds-*.txt` (mode 600, root-only)
- **System impact**: Incorrect usage may affect boot process

**Recommendation / 建议**: Review scripts before execution. Backup `/etc/fstab` if uncertain.

```bash
# Backup fstab before using add-to-fstab.sh
sudo cp /etc/fstab /etc/fstab.backup.$(date +%Y%m%d)
```

---

## Dependencies / 依赖

```bash
# Required packages
sudo apt install cifs-utils smbclient
```

---

## Scripts / 脚本

| Script | Purpose |
|--------|---------|
| `list-shares.sh <ip> <username>` | List available shares |
| `add-to-fstab.sh <ip> <share> <name> <username>` | Persistent automount |
| `mount-smb.sh <ip> <share> <path> <username>` | One-time mount |

---

## Usage / 使用

⚠️ **Passwords are entered interactively / 密码通过交互式输入**

```bash
# 1. Discover shares
# Password will be prompted securely
sudo ./list-shares.sh 192.168.2.3 Administrator
Enter SMB Password: [hidden input]

# 2. Persistent automount (mounts on first access)
sudo ./add-to-fstab.sh 192.168.2.3 workspace my-work Administrator
Enter SMB Password: [hidden input]
ls /mnt/smb/my-work    # triggers mount

# 3. One-time mount
sudo ./mount-smb.sh 192.168.2.3 workspace /mnt/temp Administrator
Enter SMB Password: [hidden input]
```

---

## How it works / 工作原理

- `noauto` → not mounted at boot
- `x-systemd.automount` → mounts on first access
- `credentials=/etc/smb-creds-*.txt` → password not in fstab
- Interactive password input → no command-line exposure

---

## Files / 文件

- Mountpoints: `/mnt/smb/<name>/`
- Credentials: `/etc/smb-creds-<name>.txt` (mode 600, root-only)

---

## 中文说明

在 Linux 上自动挂载 Windows SMB 共享。按需挂载，凭证交互式输入，命令行不暴露密码。

### 安全警告

- **需要 sudo/root 权限**：修改系统级配置
- **修改 /etc/fstab**：持久化更改系统挂载配置
- **创建凭证文件**：密码存储在 `/etc/smb-creds-*.txt`（权限 600，仅 root 可读）
- **系统影响**：错误使用可能影响启动过程

**建议**：执行前审查脚本。不确定时备份 `/etc/fstab`。

### 依赖

```bash
sudo apt install cifs-utils smbclient
```

### 使用

⚠️ **密码通过交互式安全输入，不通过命令行参数**

```bash
# 1. 发现共享
# 密码会安全提示输入
sudo ./list-shares.sh 192.168.2.3 Administrator
Enter SMB Password: [隐藏输入]

# 2. 持久化挂载（首次访问时自动挂载）
sudo ./add-to-fstab.sh 192.168.2.3 workspace mywork Administrator
Enter SMB Password: [隐藏输入]
ls /mnt/smb/mywork    # 触发挂载

# 3. 一次性挂载
sudo ./mount-smb.sh 192.168.2.3 workspace /mnt/temp Administrator
Enter SMB Password: [隐藏输入]
```

### 工作原理

- `noauto` → 启动时不挂载
- `x-systemd.automount` → 首次访问时自动挂载
- `credentials=/etc/smb-creds-*.txt` → fstab 中无密码
- 交互式密码输入 → 命令行不暴露

### 文件

- 挂载点：`/mnt/smb/<name>/`
- 凭证文件：`/etc/smb-creds-<name>.txt`（权限 600，仅 root）
