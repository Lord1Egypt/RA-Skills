# 故障排查指南

## 目录
- [故障排查方法论](#故障排查方法论)
- [常见故障场景](#常见故障场景)
- [诊断工具与命令](#诊断工具与命令)
- [故障诊断流程](#故障诊断流程)
- [解决方案](#解决方案)
- [预防措施](#预防措施)

## 概览
本文档提供服务器常见故障的诊断流程、解决方案和预防措施。遵循结构化的排查方法可以快速定位问题并最小化故障影响。

## 核心内容

### 故障排查方法论

#### 1. 五步诊断法
```
步骤 1：明确问题
  - 确认故障现象
  - 确认影响范围
  - 确认故障时间

步骤 2：收集信息
  - 系统状态
  - 日志信息
  - 配置信息

步骤 3：分析原因
  - 基于症状分析
  - 排除法定位
  - 依赖关系分析

步骤 4：验证假设
  - 测试验证
  - 复现问题
  - 确认根本原因

步骤 5：实施修复
  - 制定修复方案
  - 执行修复
  - 验证结果
```

#### 2. 问题分类
- **硬件故障**：CPU、内存、磁盘、网络设备
- **软件故障**：应用崩溃、配置错误、版本冲突
- **网络故障**：连接中断、DNS 问题、防火墙
- **性能问题**：CPU 高、内存不足、I/O 瓶颈
- **安全事件**：入侵、病毒、数据泄露

#### 3. 影响评估
- **严重性**：P0（严重） > P1（高） > P2（中） > P3（低）
- **范围**：单机 > 多机 > 全局
- **持续时间**：瞬时 > 短期 > 长期

### 常见故障场景

#### 场景 1：系统响应缓慢

**症状**
- 命令执行延迟
- 应用响应变慢
- SSH 连接卡顿

**诊断步骤**
```bash
# 1. 检查系统负载
uptime

# 2. 检查 CPU 使用
top -bn1 | head -20

# 3. 检查内存使用
free -h

# 4. 检查磁盘 I/O
iostat -x 1 5

# 5. 检查高 CPU 进程
ps aux --sort=-%cpu | head -10

# 6. 检查高内存进程
ps aux --sort=-%mem | head -10
```

**可能原因**
- CPU 密集型进程（编译、计算任务）
- 内存不足，频繁 swap
- 磁盘 I/O 瓶颈
- 网络带宽饱和

**解决方案**
```bash
# 如果是进程问题
kill -15 <PID>  # 正常终止
nice -n 19 command  # 降低优先级执行

# 如果是内存不足
清理缓存（谨慎使用）
sync; echo 3 > /proc/sys/vm/drop_caches

# 如果是 I/O 问题
检查并清理磁盘空间
优化磁盘读写
```

#### 场景 2：服务无法启动

**症状**
- 服务启动失败
- `systemctl start` 报错
- 端口未监听

**诊断步骤**
```bash
# 1. 检查服务状态
systemctl status service_name

# 2. 查看服务日志
journalctl -u service_name -n 50 --no-pager

# 3. 检查端口监听
ss -tuln | grep port_number

# 4. 检查配置文件语法
nginx -t  # Nginx
apachectl configtest  # Apache

# 5. 检查文件权限
ls -l /path/to/config
ls -l /path/to/log

# 6. 检查依赖服务
systemctl status dependent_service
```

**常见原因**
- 配置文件语法错误
- 端口被占用
- 权限不足
- 依赖服务未启动
- 磁盘空间不足

**解决方案**
```bash
# 配置文件错误
修复配置文件
cp /path/to/config.bak /path/to/config

# 端口被占用
查找占用进程：ss -tulnp | grep port
终止进程：kill <PID>

# 权限问题
修改权限：chown -R user:group /path
chmod 644 /path/to/config

# 依赖服务未启动
systemctl start dependent_service

# 磁盘空间不足
清理磁盘空间
df -h
du -sh /path/*
```

#### 场景 3：网络连接失败

**症状**
- 无法访问服务
- ping 不通
- 端口无法连接

**诊断步骤**
```bash
# 1. 测试基础连通性
ping -c 4 target_ip

# 2. 检查网络配置
ip addr show
ip route show

# 3. 检查端口监听
ss -tuln | grep port_number

# 4. 检查防火墙规则
iptables -L -n
ufw status  # Ubuntu

# 5. 检查 DNS 解析
nslookup domain.com
dig domain.com

# 6. 测试端口连接
telnet target_ip port
nc -zv target_ip port

# 7. 检查路由
traceroute target_ip
```

**常见原因**
- 网络配置错误
- 防火墙阻止
- DNS 解析失败
- 路由问题
- 服务未启动

**解决方案**
```bash
# 网络配置错误
修复网络配置
ip addr add IP/PREFIX dev INTERFACE

# 防火墙问题
添加防火墙规则
iptables -A INPUT -p tcp --dport port -j ACCEPT

# DNS 问题
修改 DNS 配置
echo "nameserver 8.8.8.8" > /etc/resolv.conf

# 服务未启动
启动服务
systemctl start service_name
```

#### 场景 4：磁盘空间不足

**症状**
- 磁盘使用率接近 100%
- 无法写入文件
- 服务日志报错

**诊断步骤**
```bash
# 1. 检查磁盘使用
df -h

# 2. 查找大目录
du -h --max-depth=1 / | sort -hr

# 3. 查找大文件
find / -type f -size +100M 2>/dev/null

# 4. 检查 inode 使用
df -i

# 5. 查找已删除但仍被进程占用的文件
lsof | grep deleted
```

**常见原因**
- 日志文件过大
- 临时文件未清理
- 大文件堆积
- inode 耗尽

**解决方案**
```bash
# 清理日志文件
truncate -s 0 /var/log/syslog
journalctl --vacuum-size=1G

# 清理临时文件
find /tmp -type f -mtime +7 -delete

# 删除大文件（先确认）
find /path -type f -size +1G -ls

# 清理已删除但被占用的文件
重启占用进程：systemctl restart service_name

# 清理包缓存
apt-get clean  # Debian/Ubuntu
yum clean all  # RHEL/CentOS
```

#### 场景 5：内存不足

**症状**
- 系统频繁 swap
- 进程被 OOM Killer 杀死
- 系统响应极慢

**诊断步骤**
```bash
# 1. 检查内存使用
free -h

# 2. 检查 swap 使用
cat /proc/swaps

# 3. 查看 OOM 日志
journalctl -k | grep -i "out of memory"
dmesg | grep -i "killed process"

# 4. 检查高内存进程
ps aux --sort=-%mem | head -10

# 5. 检查内存泄漏
top -bn1 | head -20
```

**常见原因**
- 内存泄漏
- 进程内存占用过高
- 进程数量过多
- 系统配置不当

**解决方案**
```bash
# 终止高内存进程
kill -15 <PID>

# 清理缓存（谨慎使用）
sync; echo 1 > /proc/sys/vm/drop_caches

# 调整 swap
调整 swappiness 值
sysctl vm.swappiness=10

# 重启服务
systemctl restart service_name
```

#### 场景 6：磁盘 I/O 高

**症状**
- 磁盘 I/O 等待时间长
- 进程处于 D 状态（不可中断睡眠）
- 应用读写变慢

**诊断步骤**
```bash
# 1. 检查磁盘 I/O
iostat -x 1 5

# 2. 检查进程 I/O
iotop  # 需要安装
pidstat -d 1 5

# 3. 检查磁盘使用率
df -h

# 4. 检查 D 状态进程
ps aux | awk '$8 ~ /^D/'

# 5. 检查磁盘健康
smartctl -a /dev/sda  # 需要安装
```

**常见原因**
- 大量读写操作
- 磁盘故障
- 文件系统碎片化
- RAID 重建

**解决方案**
```bash
# 优化 I/O 操作
使用 ionice 调整优先级
ionice -c 2 -n 7 command

# 检查磁盘健康
smartctl -t short /dev/sda

# 优化文件系统
fsck /dev/sda1

# 迁移数据到其他磁盘
```

### 诊断工具与命令

#### 系统信息收集
```bash
# 系统概览
/scripts/analyze-system.sh --json  # 使用 Skill 提供的脚本

# 完整系统信息
uname -a
cat /etc/os-release
uptime
df -h
free -h
```

#### 进程诊断
```bash
# 进程列表
ps aux
ps aux --sort=-%cpu | head -10
ps aux --sort=-%mem | head -10

# 实时监控
top
htop

# 进程详情
ps -fp <PID>
cat /proc/<PID>/status
ls -l /proc/<PID>/fd
```

#### 网络诊断
```bash
# 网络状态
ss -tuln
ss -s

# 网络统计
sar -n DEV 1 5

# 连接跟踪
netstat -an
```

#### 日志查看
```bash
# 系统日志
journalctl -xe
tail -f /var/log/syslog

# 应用日志
journalctl -u service_name
tail -f /var/log/service_name/error.log

# 错误日志
journalctl -p err
grep -i error /var/log/syslog | tail -50
```

### 故障诊断流程

#### 标准 SOP

```
1. 确认故障现象
   - 用户反馈什么问题？
   - 问题何时发生？
   - 影响哪些用户/服务？

2. 初步评估
   - 故障严重程度（P0-P3）
   - 影响范围
   - 是否需要立即响应

3. 信息收集
   - 执行系统信息收集脚本
   - 检查关键日志
   - 收集配置信息

4. 假设生成
   - 基于症状分析可能原因
   - 列出所有可能原因
   - 按可能性排序

5. 逐步验证
   - 从最可能的原因开始验证
   - 使用排除法
   - 记录验证过程

6. 定位根本原因
   - 确认具体原因
   - 理解问题机制
   - 准备解决方案

7. 实施修复
   - 选择最安全的修复方案
   - 准备回滚方案
   - 执行修复

8. 验证效果
   - 确认问题解决
   - 检查是否有副作用
   - 监控系统状态

9. 文档记录
   - 记录故障原因
   - 记录解决方案
   - 更新知识库
```

### 解决方案

#### 快速修复 vs 根本修复

**快速修复（临时方案）**
- 重启服务
- 清理临时文件
- 调整配置参数
- 限制资源使用

**根本修复（永久方案）**
- 修复代码 Bug
- 升级软件版本
- 优化架构设计
- 增加资源容量

#### 修复优先级
```
P0（严重，立即处理）
- 服务完全不可用
- 数据丢失风险
- 安全漏洞

P1（高，尽快处理）
- 性能严重下降
- 部分功能不可用
- 影响大量用户

P2（中，按计划处理）
- 性能轻微下降
- 非核心功能问题
- 影响少量用户

P3（低，延后处理）
- UI/UX 问题
- 优化建议
- 文档更新
```

### 预防措施

#### 1. 监控告警
- 部署监控系统（Prometheus、Zabbix、Nagios）
- 设置关键指标告警
- 配置告警通知渠道

#### 2. 日志管理
- 集中日志收集（ELK、Graylog）
- 定期日志归档
- 日志分析和告警

#### 3. 备份策略
- 定期数据备份
- 备份验证
- 异地备份

#### 4. 容量规划
- 监控资源使用趋势
- 提前扩容
- 资源预留

#### 5. 变更管理
- 变更申请和审批
- 变更测试
- 变更回滚准备

#### 6. 文档维护
- 维护系统文档
- 更新故障知识库
- 定期演练

## 示例

### 示例 1：Web 服务响应慢

#### 问题
用户反馈 Web 服务响应变慢，页面加载时间超过 10 秒

#### 诊断流程
```bash
# 1. 系统状态
uptime
# 输出：load average: 8.5, 7.2, 6.8（负载过高）

# 2. CPU 使用
top -bn1 | head -20
# 发现：nginx worker 进程 CPU 使用率 90%+

# 3. 内存使用
free -h
# 内存使用正常

# 4. 磁盘 I/O
iostat -x 1 5
# I/O 等待时间正常

# 5. 网络连接
ss -tuln | grep :80
# 连接数：8000+（过多）
```

#### 根本原因
并发连接数过高，nginx 配置不合理

#### 解决方案
```bash
# 1. 调整 nginx 配置
worker_connections 增加到 4096

# 2. 启用连接复用
keepalive_timeout 调整为 30

# 3. 配置负载均衡
将请求分发到多个后端服务器

# 4. 重新加载配置
nginx -t
systemctl reload nginx
```

#### 验证
```bash
# 检查负载
uptime
# 负载降到 2.0 以下

# 测试响应
curl -w "@curl-format.txt" -o /dev/null -s http://example.com
# 响应时间降到 500ms 以下
```

### 示例 2：数据库连接失败

#### 问题
应用无法连接到数据库，日志显示 "Connection refused"

#### 诊断流程
```bash
# 1. 检查服务状态
systemctl status mysql
# 状态：inactive（dead）

# 2. 查看日志
journalctl -u mysql -n 50
# 错误：Out of memory, killed by OOM Killer

# 3. 检查内存
free -h
# 内存使用：95%

# 4. 检查 OOM 日志
dmesg | grep -i "killed process"
# 确认：mysql 被杀死
```

#### 根本原因
系统内存不足，OOM Killer 杀死了 MySQL 进程

#### 解决方案
```bash
# 1. 清理内存
sync; echo 3 > /proc/sys/vm/drop_caches

# 2. 启动 MySQL
systemctl start mysql

# 3. 限制 MySQL 内存使用
在 my.cnf 中设置：
innodb_buffer_pool_size = 1G

# 4. 监控内存使用
free -h
```

#### 预防措施
```bash
# 1. 增加 swap 空间
# 2. 配置 OOM 保护
echo -1000 > /proc/$(pidof mysql)/oom_score_adj
# 3. 部署内存监控
```

## 约束与注意事项

1. **先诊断后修复**：不要盲目重启，先定位根本原因
2. **保留现场**：故障发生时不要立即清理，先收集信息
3. **备份优先**：任何修复操作前先备份
4. **分步验证**：每次修改一个参数，验证效果
5. **记录过程**：详细记录诊断和修复过程
6. **预防为主**：建立监控和告警机制
