# 服务器安全检查清单 / Server Security Checklist

## 基础安全配置 / Basic Security Configuration

### 系统账户 / System Accounts
- [ ] 禁用不必要的系统账户 / Disable unnecessary system accounts
- [ ] 检查 `/etc/passwd` 中的UID为0的账户 / Check accounts with UID 0 in `/etc/passwd`
- [ ] 强制所有用户使用强密码 / Enforce strong passwords for all users
- [ ] 限制sudo权限 / Restrict sudo permissions

### 认证配置 / Authentication Configuration
- [ ] SSH仅允许密钥认证(禁用密码登录) / SSH only allows key authentication (disable password login)
- [ ] 更改SSH默认端口(从22改为非标准端口) / Change SSH default port (from 22 to non-standard port)
- [ ] 配置 `/etc/ssh/sshd_config`: / Configure `/etc/ssh/sshd_config`:
  - PermitRootLogin no
  - PasswordAuthentication no
  - Port <非标准端口> / Port <non-standard port>

### 文件权限 / File Permissions
- [ ] 检查SUID/SGID文件: `find / -perm -4000 -o -perm -2000` / Check SUID/SGID files
- [ ] 确保系统关键文件不可写: `/etc`, `/usr/bin`, `/usr/sbin` / Ensure system critical files are not writable
- [ ] 检查全局可写文件: `find / -perm -o+w -type f` / Check globally writable files
- [ ] 审查 `~/.ssh/authorized_keys` 中的密钥 / Review keys in `~/.ssh/authorized_keys`

## 网络安全 / Network Security

### 防火墙配置 / Firewall Configuration
- [ ] 启用防火墙(ufw/iptables/firewalld) / Enable firewall (ufw/iptables/firewalld)
- [ ] 仅开放必要端口 / Only open necessary ports
- [ ] 拒绝所有入站连接,仅允许白名单IP / Reject all inbound connections, only allow whitelist IPs
- [ ] 配置出站规则,限制不必要的外部连接 / Configure outbound rules, restrict unnecessary external connections

### 端口审计 / Port Audit
- [ ] 扫描开放端口: `ss -tlnp` / Scan open ports
- [ ] 确认每个端口的对应服务 / Confirm service for each port
- [ ] 关闭不必要的服务: `systemctl disable <service>` / Disable unnecessary services
- [ ] 检查监听0.0.0.0的服务(应限制到特定IP) / Check services listening on 0.0.0.0 (should restrict to specific IP)

## 进程监控 / Process Monitoring

### 定期检查 / Regular Checks
- [ ] 列出所有进程: `ps auxf` / List all processes
- [ ] 检查高CPU/内存进程 / Check high CPU/memory processes
- [ ] 审查异常的父子进程关系 / Review abnormal parent-child process relationships
- [ ] 检查隐藏进程: `ps -e` / Check hidden processes

### 可疑进程特征 / Suspicious Process Characteristics
- 反弹shell: `bash -i`, `nc -l` / Reverse shell
- 反向隧道: `ssh -R`, `socat TCP-LISTEN` / Reverse tunnel
- 下载并执行: `wget \| sh`, `curl \| sh` / Download and execute
- 编码命令: `base64 -d`, `xxd -r`

## 日志审计

### 关键日志文件
- [ ] `/var/log/auth.log` 或 `/var/log/secure` - 认证日志
- [ ] `/var/log/syslog` 或 `/var/log/messages` - 系统日志
- [ ] `/var/log/kern.log` - 内核日志
- [ ] 应用程序日志: `/var/log/openclaw/`, `/opt/openclaw/logs/`

### 异常事件检测
- [ ] 多次失败的登录尝试: `grep "Failed password" /var/log/auth.log`
- [ ] 非工作时间登录: `grep -E "^(0[0-9]|1[0-9]|2[0-3]):" /var/log/auth.log`
- [ ] 异常的sudo使用: `grep "sudo:" /var/log/auth.log`
- [ ] 未知的SSH密钥使用

## 应用安全

### OpenClaw特定检查
- [ ] 审查OpenClaw的配置文件权限
- [ ] 检查配置中是否包含硬编码的密钥或密码
- [ ] 确认OpenClaw监听的端口和绑定地址
- [ ] 检查OpenClaw的日志输出中是否包含敏感信息
- [ ] 审查OpenClaw的网络连接目的地

### 依赖管理
- [ ] 更新系统和软件包: `apt update && apt upgrade`
- [ ] 检查已知漏洞: `apt list --upgradable`
- [ ] 审查第三方软件的来源和签名

## 敏感信息检测

### 扫描目标目录
- [ ] `/etc/` - 配置文件
- [ ] `/opt/openclaw/` - OpenClaw相关
- [ ] `/home/user/` - 用户目录
- [ ] `/var/log/` - 日志文件
- [ ] 应用程序根目录

### 敏感信息类型
- API密钥 (api_key, apikey, secret_key)
- 数据库凭证 (password, db_password, mysql_password)
- JWT密钥 (jwt_secret, jwt_key)
- 私钥文件 (*.pem, *.key, id_rsa)
- 访问令牌 (access_token, auth_token, bearer_token)
- AWS密钥 (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

## 入侵检测

### 实时监控工具
- [ ] 配置fail2ban封禁恶意IP
- [ ] 部署OSSEC或AIDE文件完整性监控
- [ ] 使用auditd监控系统调用
- [ ] 配置日志转发到安全服务器

### 应急响应
- [ ] 制定应急响应流程
- [ ] 准备取证工具集
- [ ] 配置告警通知(邮件/短信)
- [ ] 定期备份关键数据和配置

## OpenClaw专项审计

### 配置文件检查
```bash
# 查找OpenClaw配置
find / -name "*openclaw*" -o -name "*open-claw*" 2>/dev/null
grep -r "password\|secret\|key" /opt/openclaw/config/ 2>/dev/null
```

### 进程检查
```bash
# 查找OpenClaw进程
ps aux | grep -i openclaw
lsof -p <pid>  # 查看进程打开的文件和连接
```

### 网络连接检查
```bash
# 查看OpenClaw的网络连接
ss -tunap | grep <pid>
netstat -tunap | grep <pid>
```

### 文件完整性
```bash
# 生成基线(初次运行)
find /opt/openclaw -type f -exec md5sum {} \; > baseline.md5

# 对比检查
md5sum -c baseline.md5
```

## 持续监控建议

1. **每日任务**
   - 检查系统日志中的异常事件
   - 审查新增的SUID文件
   - 查看失败登录记录

2. **每周任务**
   - 执行完整的安全扫描
   - 更新系统和软件包
   - 审查新增的开放端口

3. **每月任务**
   - 完整的系统审计
   - 备份检查和恢复测试
   - 安全策略评估

## 快速诊断命令

```bash
# 一键快速检查
ps auxf | head -20                          # 前20个进程
ss -tlnp | grep LISTEN                      # 监听端口
last -n 10                                  # 最近登录
lastb -n 10                                 # 失败登录
find / -perm -4000 -type f 2>/dev/null       # SUID文件
grep -r "password\|secret" /etc 2>/dev/null  # 敏感信息
```
