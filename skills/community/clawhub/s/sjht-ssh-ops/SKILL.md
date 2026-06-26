---
name: ssh-ops
description: >
  SSH 密钥管理和远程服务器运维工具。
  用于生成 SSH 密钥、部署公钥到远程主机实现免密登录、测试连接、查看远程主机信息、
  以及远程执行运维命令。Use when 用户需要连接远程服务器、配置 SSH 免密登录、
  管理服务器、部署应用、或在远程主机上执行命令。触发短语包括：
  "SSH登录"、"免密登录"、"服务器管理"、"远程部署"、"连接服务器"、"运维"。
---

# ssh-ops — SSH 密钥管理与远程运维

管理 SSH 密钥、部署免密登录、执行远程运维操作。

## 工作流程

### 1. 生成密钥（如果还没有）

```bash
bash <skill>/scripts/ssh-key-setup.sh gen
```

默认生成 `~/.ssh/id_ed25519`。如果已存在会提示。

### 2. 部署公钥到远程主机

需要密码时，设置 `SSHPASS` 环境变量：

```bash
SSHPASS='密码' bash <skill>/scripts/ssh-key-setup.sh deploy <host> [user]
```

脚本会自动安装 sshpass、使用 ssh-copy-id 部署公钥。

### 3. 测试免密登录

```bash
bash <skill>/scripts/ssh-key-setup.sh test <host> [user]
```

### 4. 查看远程主机信息

```bash
bash <skill>/scripts/ssh-key-setup.sh info <host> [user]
```

返回：主机名、系统版本、内核、内存、磁盘、负载。

## 远程执行命令

免密登录配置好后，可直接用 `ssh user@host "命令"` 执行任意远程操作：

```bash
# 查看进程
ssh root@host "ps aux | grep node"

# 安装软件
ssh root@host "apt-get update && apt-get install -y nginx"

# 传输文件
scp file.txt root@host:/tmp/

# 同步目录
rsync -avz ./dist/ root@host:/var/www/app/
```

## 安全提示

- `SSHPASS` 环境变量用完即 unset，不要持久化到文件
- 私钥（`id_ed25519`）权限必须是 600，`~/.ssh/` 权限必须是 700
- 不要在聊天记录中存储密码，使用时设环境变量
- 部署完成后验证免密登录，确认后再 unset 密码
