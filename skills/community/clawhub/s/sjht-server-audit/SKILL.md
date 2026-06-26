---
name: server-audit
description: >
  远程服务器安全巡检和环境报告工具。
  通过 SSH 免密登录远程主机，全面检查系统信息、运行服务、开放端口、
  Web 服务器配置、数据库配置、安全设置（SSH/防火墙/SELinux）、可疑进程和定时任务，
  生成结构化的巡检报告。Use when 用户需要检查服务器安全、排查服务器环境、
  了解服务器上运行了什么服务、生成巡检报告、或提及"巡检"、"安全检查"、"服务器检查"。
---

# server-audit — 远程服务器巡检

通过 SSH 免密登录检查远程服务器环境与安全状况，生成巡检报告。

## 前提条件

- 已通过 `ssh-ops` skill 配置好免密登录
- 或手动配置了 SSH 密钥认证

## 工作流程

### 1. 运行巡检脚本

```bash
bash <skill>/scripts/server-audit.sh <host> [user]
```

脚本会自动收集以下信息并输出快速安全判定：

- **系统信息**: OS、内核、CPU、内存、磁盘、Swap
- **运行服务**: systemd running services
- **开放端口**: 所有 TCP 监听端口
- **防火墙**: firewalld 状态和规则、SELinux 状态
- **Web 服务**: Nginx/PHP-FPM/MariaDB/Node/Docker 版本和状态
- **Nginx 虚拟主机**: server_name、root、listen
- **网站文件**: /www/wwwroot 下的站点检测
- **安全配置**: SSH 配置（密码认证、Root 登录、端口）
- **可疑项目**: 失败登录记录、定时任务、高内存进程

### 2. 基于脚本输出生成详细报告

根据脚本收集的数据，生成结构化的 Markdown 报告。

**⚠️ 报告保存位置：** `~/.openclaw/workspac/audits/<IP>-<日期>.md`

报告只保存在本地 workspace，**不要上传到任何 GitHub 仓库**。

文件命名格式：`119.91.38.151-20260319.md`

报告模板：
```markdown
# 服务器巡检报告
**主机:** <IP>
**检查时间:** <时间>

## 1. 基础信息
## 2. 已安装服务
## 3. 开放端口（标注风险）
## 4. 安全问题（🔴严重/⚠️警告/💡建议）
## 5. 快速修复命令
```

## 安全判定规则

### 🔴 严重（需立即修复）
- 数据库端口（3306/5432）监听 0.0.0.0
- 管理面板端口（宝塔 8888、phpMyAdmin）监听 0.0.0.0
- SSH 允许 root 密码登录

### ⚠️ 警告（建议修复）
- 防火墙未启用
- SELinux 禁用
- SSH 密码认证未禁用
- 无 Swap 分区
- 存在暴力破解尝试
- 可疑定时任务

### 💡 建议（优化项）
- SSH 默认端口 22
- 缺少运行时（Node.js 等）
- 未使用的服务（Postfix 等）
- 无自动备份策略

## 多服务器批量巡检

对多台服务器循环执行：
```bash
for host in 192.168.1.1 192.168.1.2 10.0.0.1; do
  echo "=== $host ==="
  bash <skill>/scripts/server-audit.sh "$host"
  echo ""
done
```
