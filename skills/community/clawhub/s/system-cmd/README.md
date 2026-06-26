# 系统命令技能

## 技能简介
系统命令技能是一个安全、便捷的系统命令执行工具，允许用户在OpenClaw中直接执行常用的Windows系统命令。它提供了对系统信息的快速访问和故障排查能力，同时确保命令执行的安全性和可控性。

## 功能特点
1. **安全执行** - 限制可执行的命令范围，防止危险操作
2. **中文友好** - 完美处理中文输出，避免乱码问题
3. **快速访问** - 一键执行常用系统诊断命令
4. **完整输出** - 返回命令执行的完整结果
5. **错误处理** - 提供清晰的错误信息和友好提示

## 支持的命令

### 系统信息命令
| 命令 | 功能描述 | 示例输出 |
|------|----------|----------|
| `ipconfig` | 查看网络配置信息 | IP地址、子网掩码、默认网关、DNS服务器 |
| `systeminfo` | 查看系统详细信息 | 操作系统版本、安装日期、硬件信息、热修复 |
| `hostname` | 查看计算机名 | 计算机名称 |
| `ver` | 查看Windows版本 | Windows版本号 |

### 进程和任务命令
| 命令 | 功能描述 | 示例输出 |
|------|----------|----------|
| `tasklist` | 查看运行中的进程 | 进程名、PID、会话名、内存使用 |
| `taskkill` | 结束指定进程 | 进程结束状态 |
| `schtasks` | 查看计划任务 | 任务名称、下次运行时间、状态 |

### 网络诊断命令
| 命令 | 功能描述 | 示例输出 |
|------|----------|----------|
| `netstat` | 查看网络连接状态 | 协议、本地地址、远程地址、状态 |
| `ping` | 测试网络连通性 | 响应时间、丢包率 |
| `tracert` | 跟踪网络路径 | 经过的路由节点、延迟时间 |
| `nslookup` | DNS查询 | 域名解析结果 |

### 磁盘和文件命令
| 命令 | 功能描述 | 示例输出 |
|------|----------|----------|
| `dir` | 查看目录内容 | 文件列表、大小、修改时间 |
| `tree` | 显示目录树结构 | 目录层次结构 |
| `chkdsk` | 检查磁盘错误 | 磁盘状态、错误报告 |
| `fsutil` | 文件系统工具 | 文件系统信息 |

### 用户和权限命令
| 命令 | 功能描述 | 示例输出 |
|------|----------|----------|
| `whoami` | 查看当前用户 | 用户名、权限信息 |
| `net user` | 查看用户账户 | 用户账户列表 |
| `net localgroup` | 查看本地组 | 本地组列表 |

## 使用方法

### 基本语法
```
/system_cmd <命令> [参数]
```

### 快速开始
```bash
# 查看网络配置
/system_cmd ipconfig

# 查看进程列表
/system_cmd tasklist

# 查看网络连接
/system_cmd netstat

# 查看系统信息
/system_cmd systeminfo
```

### 获取帮助
```bash
# 查看可用命令列表
/system_cmd help

# 查看命令帮助（简写）
/system_cmd
```

## 使用示例

### 示例1：网络故障排查
```bash
# 检查IP配置
/system_cmd ipconfig

# 检查网络连接
/system_cmd netstat -an

# 测试网络连通性
/system_cmd ping 8.8.8.8 -n 4
```

### 示例2：系统性能检查
```bash
# 查看哪些进程占用资源
/system_cmd tasklist /fo table

# 查看系统详细信息
/system_cmd systeminfo

# 检查磁盘空间
/system_cmd dir C:\ /s | find "个文件"
```

### 示例3：系统信息收集
```bash
# 获取完整系统信息
/system_cmd systeminfo

# 查看计算机名和用户
/system_cmd hostname
/system_cmd whoami

# 查看Windows版本
/system_cmd ver
```

### 示例4：安全审计
```bash
# 查看网络连接（显示所有）
/system_cmd netstat -ano

# 查看计划任务
/system_cmd schtasks /query /fo list

# 查看用户账户
/system_cmd net user
```

## 输出处理

### 中文编码处理
技能已自动处理中文编码问题，确保以下内容正常显示：
- 中文文件名和路径
- 中文系统信息
- 中文错误消息
- 中文用户账户名

### 输出格式优化
- **表格格式化** - 对`tasklist`等命令进行表格优化
- **分页显示** - 对长输出进行分页处理
- **关键词高亮** - 对重要信息进行高亮显示
- **错误分离** - 将错误信息与正常输出分离显示

### 输出示例
```
[执行成功] 命令: ipconfig

Windows IP 配置

以太网适配器 以太网:

   连接特定的 DNS 后缀 . . . . . . . : 
   本地链接 IPv6 地址. . . . . . . . : fe80::1234:5678:90ab:cdef%12
   IPv4 地址 . . . . . . . . . . . . : 192.168.1.100
   子网掩码  . . . . . . . . . . . . : 255.255.255.0
   默认网关. . . . . . . . . . . . . : 192.168.1.1

[执行时间] 0.5秒
[返回代码] 0
```

## 安全特性

### 命令白名单
技能只允许执行预定义的安全命令：
- 信息查看命令（只读）
- 诊断命令（无副作用）
- 有限的管理命令（需要权限）

### 参数限制
对某些命令的参数进行限制：
- 禁止危险的参数组合
- 限制执行时间
- 限制输出大小
- 防止命令注入

### 权限控制
- 普通命令：所有用户可执行
- 管理命令：需要管理员权限
- 危险命令：默认禁用，需要特殊配置

## 技术实现

### 命令执行引擎
- 使用Python的`subprocess`模块执行命令
- 支持命令行参数解析
- 实时输出捕获和处理
- 超时控制和进程管理

### 编码处理
```python
# 自动检测和处理编码
def execute_command(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    # 进一步处理中文字符
    return fix_chinese_encoding(result.stdout)
```

### 错误处理
```python
try:
    result = execute_command(command)
    if result.returncode == 0:
        return format_success(result.stdout)
    else:
        return format_error(result.stderr)
except Exception as e:
    return format_exception(e)
```

## 配置说明

### 配置文件
`config.json` 包含技能配置：
```json
{
  "allowed_commands": [
    "ipconfig", "systeminfo", "tasklist", "netstat",
    "ping", "hostname", "ver", "whoami"
  ],
  "options": {
    "timeout_seconds": 30,
    "max_output_size": 100000,
    "enable_chinese_fix": true,
    "require_admin_for": ["taskkill", "schtasks"]
  }
}
```

### 环境变量
```bash
# 设置命令执行超时
setx SYSTEM_CMD_TIMEOUT "60"

# 设置输出编码
setx SYSTEM_CMD_ENCODING "gbk"
```

## 使用场景

### 1. 远程技术支持
- 远程查看客户系统信息
- 诊断网络问题
- 检查系统配置

### 2. 系统管理员日常维护
- 快速检查服务器状态
- 监控系统资源
- 排查故障问题

### 3. 开发环境调试
- 检查开发环境配置
- 诊断网络连接问题
- 监控后台进程

### 4. 教学和培训
- 演示Windows命令使用
- 系统管理教学
- 故障排查练习

### 5. 自动化脚本集成
- 作为自动化流程的一部分
- 系统健康检查
- 配置验证

## 高级用法

### 命令组合
```bash
# 组合多个命令（需要技能支持）
/system_cmd "ipconfig && ping 127.0.0.1"
```

### 输出重定向
```bash
# 保存命令输出到文件（如果支持）
/system_cmd "systeminfo > system_report.txt"
```

### 定时执行
```bash
# 结合cron技能定时执行
# 每天检查系统状态
0 9 * * * /system_cmd systeminfo
```

### 与其他技能集成
```python
# 在Python脚本中调用
from system_cmd import execute_safe_command

result = execute_safe_command("ipconfig")
if result["status"] == "success":
    process_network_info(result["output"])
```

## 故障排除

### 常见问题
1. **命令执行失败**
   - 症状：返回"命令不存在或无法执行"
   - 解决：检查命令名称是否正确，或使用`/system_cmd help`查看支持的命令

2. **输出乱码**
   - 症状：中文显示为乱码
   - 解决：技能已自动处理编码，如果仍有问题请反馈

3. **命令执行超时**
   - 症状：长时间无响应
   - 解决：`systeminfo`等命令可能需要较长时间，请等待或检查系统状态

4. **权限不足**
   - 症状：返回"权限被拒绝"
   - 解决：某些命令需要管理员权限

### 调试技巧
1. **查看原始输出** - 使用原始模式查看未处理的输出
2. **检查命令语法** - 确保命令格式正确
3. **验证权限** - 确认有执行命令的权限
4. **查看系统日志** - 检查Windows事件日志

## 最佳实践

### 命令使用建议
1. **先查看后操作** - 先使用查看命令了解情况
2. **谨慎使用管理命令** - 特别是`taskkill`等可能影响系统的命令
3. **保存重要输出** - 对诊断结果进行保存记录
4. **定期系统检查** - 建立定期检查流程

### 安全建议
1. **限制命令范围** - 只启用必要的命令
2. **监控命令使用** - 记录命令执行日志
3. **定期审查配置** - 检查命令白名单
4. **更新技能版本** - 及时获取安全更新

### 性能优化
1. **避免长时间命令** - 设置合理的超时时间
2. **限制输出大小** - 防止内存溢出
3. **缓存常用结果** - 对不变的信息进行缓存
4. **异步执行** - 对耗时命令使用异步方式

## 版本信息

### v1.0.0 (2026-04-08)
- 初始版本发布
- 支持常用系统命令
- 中文编码处理
- 完整错误处理

### 更新计划
- 增加更多系统命令支持
- 添加命令历史记录
- 支持命令别名和自定义命令
- 添加图形化命令构建器

## 相关技能
- `sys-info` - 系统信息监控技能（更专业的系统监控）
- `daily-report` - 每日报告技能（包含系统信息）
- `router` - 路由技能（自然语言调用系统命令）

## 技术支持
如有问题，请参考：
- Windows命令参考: https://docs.microsoft.com/windows-server/administration/windows-commands/
- OpenClaw文档: https://docs.openclaw.ai
- 技能目录: `skills/system_cmd/`