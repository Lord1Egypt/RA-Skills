---
name: openclaw
description: 提供结构化的服务器运维工作流程，包含系统识别、安全检查、命令验证和故障排查；当用户需要系统管理、性能优化、日志分析或服务器维护时使用
---

# OpenClaw 服务器运维

## 任务目标
- 本 Skill 用于：系统管理员、运维工程师进行安全高效的服务器维护操作
- 能力包含：系统识别、命令验证、风险评估、故障排查、性能监控、日志分析
- 触发条件：用户请求服务器维护、系统诊断、性能优化、故障修复或日常运维任务

## 核心原则

### 安全第一
- **永远先查看再执行**：任何破坏性操作前，必须先确认当前状态
- **执行前评估风险**：识别命令潜在影响，准备回滚方案
- **保持操作可追溯**：记录每个关键操作的命令、时间、结果

### 系统识别优先
- 执行任何操作前，先识别系统类型（Linux 发行版、macOS、Windows）
- 根据系统类型选择合适的命令和工具
- 不假设系统环境，通过命令输出验证

### 验证驱动
- 执行前：验证命令语法、影响范围、资源可用性
- 执行后：验证操作结果、系统状态、数据完整性
- 异常时：保留现场、收集日志、分析原因

## 标准工作流程

### 阶段 1：环境识别与评估
1. 识别系统类型
   ```bash
   # Linux
   cat /etc/os-release
   uname -a
   # macOS
   sw_vers
   # Windows
   systeminfo
   ```

2. 评估当前状态
   - 系统负载：`uptime` 或 `top -bn1 | head -20`
   - 磁盘使用：`df -h`
   - 内存使用：`free -h` 或 `vm_stat`
   - 网络连接：`ss -tuln` 或 `netstat -tuln`

3. 检查风险因素
   - 是否在生产环境
   - 是否有关键服务运行
   - 是否有未提交的更改
   - 备份状态

### 阶段 2：命令评估与验证
1. 命令风险评估
   - 查阅 [references/linux-commands.md](references/linux-commands.md) 确认命令安全等级
   - 使用 `--help` 或 `man` 查看命令详细说明
   - 识别破坏性参数（如 `-r`、`-f`、`--force`）

2. 模拟执行（如果可能）
   - 使用 `--dry-run` 参数（如 rsync、apt-get）
   - 使用 `echo` 预览命令
   - 在测试环境先执行

3. 安全检查清单
   - 参考 [references/safety-checklist.md](references/safety-checklist.md)
   - 确认数据备份
   - 准备回滚方案
   - 通知相关人员（如需要）

### 阶段 3：执行与监控
1. 执行命令
   - 使用绝对路径或确认命令来源
   - 添加详细日志记录
   - 在非高峰期执行（如适用）

2. 实时监控
   - 观察命令输出
   - 监控系统资源变化
   - 准备中断执行（如 Ctrl+C）

3. 记录操作
   - 记录执行的命令
   - 记录输出结果
   - 记录执行时间

### 阶段 4：验证与确认
1. 验证结果
   - 确认操作达到预期效果
   - 检查系统状态是否正常
   - 验证相关服务运行正常

2. 数据完整性检查
   - 确认数据未丢失或损坏
   - 验证权限和所有权正确
   - 检查配置文件语法

3. 文档更新
   - 更新运维日志
   - 更新配置文档（如需要）
   - 记录经验教训

## 常见运维场景

### 场景 1：系统性能诊断
**触发**：系统响应慢、负载高
**流程**：
1. 执行 `scripts/analyze-system.sh --json` 收集系统快照
2. 分析资源使用情况（CPU、内存、磁盘 I/O、网络）
3. 定位高消耗进程
4. 根据分析结果提供优化建议

### 场景 2：磁盘空间清理
**触发**：磁盘使用率超过阈值
**流程**：
1. `df -h` 确认磁盘使用情况
2. `du -h --max-depth=1 /path` 定位大目录
3. `find /path -type f -size +100M` 查找大文件
4. 列出可清理文件清单（不直接删除）
5. 等待用户确认后再执行清理

### 场景 3：进程管理
**触发**：进程异常、需要重启服务
**流程**：
1. `ps aux | grep process_name` 查找进程
2. `systemctl status service_name` 检查服务状态
3. 查看日志文件：`journalctl -u service_name -n 50` 或 `/var/log/...`
4. 分析异常原因
5. 提供解决方案（优先非破坏性方案）

### 场景 4：网络故障排查
**触发**：网络不通、服务不可访问
**流程**：
1. `ping target_ip` 测试连通性
2. `ip addr` 或 `ifconfig` 检查网络配置
3. `ss -tuln` 检查端口监听
4. `iptables -L -n` 或 `nft list ruleset` 检查防火墙
5. 查看 `/var/log/syslog` 或相关日志

### 场景 5：日志分析
**触发**：需要分析错误日志、排查问题
**流程**：
1. 确定日志位置：`/var/log/...`、`journalctl`
2. 按时间筛选：`grep "ERROR" /path/log | tail -100`
3. 按关键词搜索：`grep "keyword" /path/log`
4. 统计错误频率：`grep "ERROR" /path/log | wc -l`
5. 分析错误模式和上下文

### 场景 6：软件包管理
**触发**：安装、更新、卸载软件
**流程**：
1. 识别包管理器：`apt-get`、`yum`、`dnf`、`pacman`、`brew`
2. 更新包索引：`apt-get update` 或 `yum check-update`
3. 查看可用版本：`apt-cache show package_name`
4. 模拟安装：`apt-get install --dry-run package_name`
5. 执行安装并验证：`apt-get install package_name` + `package_name --version`

## 系统类型识别

### Linux
- Ubuntu/Debian：存在 `/etc/debian_version`
- CentOS/RHEL：存在 `/etc/redhat-release`
- Arch Linux：存在 `/etc/arch-release`
- 通用命令：`cat /etc/os-release`

### macOS
- 标识：`sw_vers` 或 `uname -s` 返回 "Darwin"

### Windows
- 标识：`systeminfo` 或 `ver`

## 资源索引

### 必要脚本
- [scripts/analyze-system.sh](scripts/analyze-system.sh) - 安全收集系统信息
  - 用途：快速了解系统状态和配置
  - 参数：`--json` 输出 JSON 格式，`--output FILE` 保存到文件

### 领域参考
- [references/linux-commands.md](references/linux-commands.md) - 常用命令参考与风险评估
  - 何时读取：执行不熟悉的命令前
  - 包含：命令说明、安全等级、示例、风险提示

- [references/safety-checklist.md](references/safety-checklist.md) - 安全检查清单
  - 何时读取：执行任何破坏性操作前
  - 包含：执行前检查、风险评估、回滚准备

- [references/troubleshooting-guide.md](references/troubleshooting-guide.md) - 故障排查指南
  - 何时读取：遇到系统故障或异常时
  - 包含：常见故障场景、诊断流程、解决方案

## 注意事项

### 永远不要做的事
- 不要在未知系统上直接执行破坏性命令
- 不要使用 `rm -rf` 除非 100% 确认路径
- 不要在生产环境直接测试新命令
- 不要忽略命令警告和错误信息

### 推荐做法
- 优先使用只读命令获取信息
- 命令参数优先使用明确路径而非通配符
- 执行前先用 `echo` 预览完整命令
- 重要操作前先创建系统快照或备份

### 日志规范
- 关键操作记录时间、用户、命令、结果
- 异常情况记录错误信息和现场
- 定期审查操作日志，总结经验

## 使用示例

### 示例 1：系统健康检查
**功能**：全面检查系统状态
**执行方式**：调用脚本 + 智能体分析
```bash
# 执行系统信息收集
/workspace/projects/openclaw/scripts/analyze-system.sh --json
```

**智能体分析要点**：
- 识别系统类型和版本
- 评估资源使用率
- 检查异常进程
- 识别潜在风险

### 示例 2：安全清理磁盘空间
**功能**：识别并建议清理大文件
**执行方式**：智能体引导 + 用户确认
```bash
# 查找大文件（只读）
find /var/log -type f -size +100M -exec ls -lh {} \;

# 检查磁盘使用
df -h
```

**关键步骤**：
1. 使用只读命令定位目标
2. 列出清理建议清单
3. 等待用户确认
4. 执行清理并验证

### 示例 3：进程异常诊断
**功能**：诊断进程崩溃或卡死原因
**执行方式**：智能体分析
```bash
# 查找进程
ps aux | grep nginx

# 检查服务状态
systemctl status nginx

# 查看日志
journalctl -u nginx -n 50 --no-pager
```

**智能体分析**：
- 结合进程状态、日志内容、系统资源
- 识别异常模式
- 提供针对性解决方案
