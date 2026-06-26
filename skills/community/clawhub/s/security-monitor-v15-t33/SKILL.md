# 系统安全分析工具 / System Security Analysis Tool

**版本 / Version: v1.5**

## 描述 / Description
提供系统进程、网络连接、文件权限、敏感信息、日志分析和进程树的分析检测。适用于Linux/Unix服务器安全审计和异常行为检测。

## 使用范围 / Usage Scope
当需要分析系统活动、检测安全风险、或审计服务器运行状态时,加载并使用此技能。

## 技能使用说明

### 触发条件 / Trigger Conditions
- 用户要求检查服务器安全
- 监控进程或服务的异常行为
- 分析可疑的系统活动
- 审计开放端口和网络连接
- 检测敏感信息泄露

### 核心分析能力 / Core Analysis Capabilities

#### 1. 进程监控 (scripts/monitor.py:37-89)
```bash
# 获取所有进程并分析可疑行为
python3 monitor.py
```

检测项:
- 高CPU/内存占用进程 (>80%)
- 可疑命令模式 (反弹shell、反向隧道等)
- 隐藏进程或异常权限

#### 2. 网络连接分析 (scripts/monitor.py:91-132)
检测异常:
- 可疑端口连接 (4444, 5555, 6666-6669, 31337等)
- 非标准端口的外部连接
- 建立连接的进程信息

#### 3. 端口扫描 (scripts/monitor.py:201-225)
识别:
- 开放的常见服务端口 (22, 80, 443等)
- 可疑的后门端口
- 非预期服务端口

#### 4. 敏感信息泄露检测 (scripts/monitor.py:134-199)
扫描内容:
- API密钥 (api_key, apikey)
- 数据库密码 (password, db_password)
- JWT密钥 (jwt_secret, secret)
- 私钥文件 (BEGIN PRIVATE KEY)
- 访问令牌 (access_token, auth_token)

#### 5. 文件权限审计 (scripts/monitor.py:167-200)
检查:
- 系统关键目录的可写文件 (/etc, /usr/bin等)
- 配置文件异常权限
- SUID/SGID文件 (需补充)

#### 6. 日志分析 (v1.5新增)
扫描系统日志中的异常事件:
- 失败的SSH登录尝试 (多次失败可能是暴力攻击)
- 用户账户创建/修改事件
- sudo命令使用记录
- 服务启动/停止事件
- 异常错误模式

#### 7. 进程树分析 (v1.5新增)
分析进程间的父子关系:
- 检测孤儿进程 (父进程已退出)
- 检测可疑的进程派生 (如bash反弹shell)
- 识别异常进程链
- 检测隐藏进程 (ps中不可见)

### 使用方法 / Usage Method

#### 方法1: 完整扫描
```bash
# 在服务器上执行完整扫描
python3 .codebuddy/skills/security-monitor/scripts/monitor.py
```

#### 方法2: 针对性检测

仅检查进程:
```python
from monitor import SecurityMonitor

monitor = SecurityMonitor()
processes = monitor.get_all_processes()
monitor.check_suspicious_processes(processes)
print(monitor.generate_report())
```

仅检查网络连接:
```python
monitor = SecurityMonitor()
connections = monitor.get_network_connections()
monitor.check_suspicious_connections(connections)
print(monitor.generate_report())
```

扫描特定目录的敏感信息:
```python
monitor = SecurityMonitor()
monitor.scan_secrets_in_files('/path/to/scan', max_files=100)
print(monitor.generate_report())
```

### 权限要求

**建议以root权限运行**以获取完整的进程和网络信息:
```bash
sudo python3 .codebuddy/skills/security-monitor/scripts/monitor.py
```

非root权限运行时,部分检测项会受限,但仍可执行基础分析。

### 输出说明

脚本会输出两部分:

1. **可读报告** - 适合人工审阅
   - 高危问题 - 需要立即处理
   - 警告信息 - 需要关注和确认

2. **JSON格式** - 适合程序化处理
```json
{
  "timestamp": "2024-01-01T12:00:00",
  "violations": ["高危问题列表"],
  "warnings": ["警告信息列表"],
  "info": ["其他信息"]
}
```

### 自定义扫描

修改 `scan_secrets_in_files()` 的目录参数:
```python
# 扫描特定目录
monitor.scan_secrets_in_files('/opt/openclaw', max_files=50)
monitor.scan_secrets_in_files('/home/user', max_files=30)
```

添加自定义检测模式到脚本中:
```python
# 在 secret_patterns 中添加
secret_patterns['自定义类型'] = [
    r'your_pattern_here',
]
```

### 安全建议 / Security Recommendations

1. **定期执行监控** - 建议设置为定时任务(cron)
2. **对比基线** - 保存正常状态下的报告,用于对比异常
3. **关注高危项** - 优先处理violation级别的问题
4. **确认服务端口** - 记录预期开放的端口,排除误报
5. **隔离可疑进程** - 发现反弹shell等立即终止并调查

### 常见问题

**Q: 检测到非标准端口怎么办?**
A: 确认是否为你的服务(如OpenClaw)使用,如果是,添加到白名单列表。

**Q: 如何只扫描OpenClaw相关的文件?**
A: 调用时指定目录:
```python
monitor.scan_secrets_in_files('/opt/openclaw', max_files=100)
```

**Q: 检测到敏感信息泄露怎么办?**
A: 1) 立即移除或轮换泄露的密钥 2) 检查提交历史 3) 将文件加入.gitignore 4) 检查访问日志

### 扩展检测项

可参考以下思路扩展功能:

1. **日志分析** - 扫描 `/var/log/` 中的异常登录和失败记录
2. **进程树分析** - 检测父子进程的异常关系
3. **文件完整性** - 使用 `md5sum` 检测关键文件修改
4. **计划任务审计** - 检查 `/etc/cron.*` 和 `crontab -l`
5. **SSH密钥审计** - 检查 `~/.ssh/authorized_keys` 的可疑条目

### 注意事项

- 脚本仅提供分析工具,不能替代完整的安全方案
- 检测结果需要人工判断,排除误报
- 持续监控比一次性扫描更有价值
- 建议结合其他安全工具(如fail2ban、auditd)使用
