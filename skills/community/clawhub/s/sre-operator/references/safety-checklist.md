# 安全检查清单

## 目录
- [执行前检查](#执行前检查)
- [命令风险评估](#命令风险评估)
- [数据备份确认](#数据备份确认)
- [回滚准备](#回滚准备)
- [执行后验证](#执行后验证)

## 概览
本文档提供执行任何破坏性操作前的安全检查清单。在执行可能影响系统稳定性的操作前，请务必完成所有相关检查项。

## 核心内容

### 执行前检查

#### 1. 环境确认
- [ ] 确认当前操作环境（测试/开发/生产）
- [ ] 确认系统类型和版本
  ```bash
  cat /etc/os-release
  uname -a
  ```
- [ ] 确认当前工作目录
  ```bash
  pwd
  ```
- [ ] 确认当前用户权限
  ```bash
  whoami
  id
  ```

#### 2. 影响范围评估
- [ ] 识别操作影响的系统组件
- [ ] 识别操作影响的用户和服务
- [ ] 识别操作影响的网络连接
- [ ] 评估操作对业务的影响程度
- [ ] 确认是否需要通知相关人员

#### 3. 资源状态检查
- [ ] 检查系统负载
  ```bash
  uptime
  ```
- [ ] 检查磁盘空间
  ```bash
  df -h
  ```
- [ ] 检查内存使用
  ```bash
  free -h
  ```
- [ ] 检查关键服务状态
  ```bash
  systemctl status service_name
  ```

#### 4. 配置文件确认
- [ ] 确认配置文件位置
- [ ] 查看当前配置内容
  ```bash
  cat /path/to/config
  ```
- [ ] 备份当前配置
  ```bash
  cp /path/to/config /path/to/config.bak.$(date +%Y%m%d_%H%M%S)
  ```
- [ ] 验证备份文件创建成功
  ```bash
  ls -lh /path/to/config.bak.*
  ```

### 命令风险评估

#### 1. 命令分类

**🔴 高风险命令**
- `rm` - 删除文件或目录
- `dd` - 直接磁盘操作
- `mkfs` - 创建文件系统
- `fdisk/parted` - 磁盘分区
- `iptables -F` - 清空防火墙规则
- `chmod 777` - 设置权限为完全开放
- `chown -R` - 递归修改所有者

**⚠️ 中风险命令**
- `systemctl stop/restart` - 停止/重启服务
- `kill -9` - 强制终止进程
- `apt/yum upgrade` - 升级软件包
- `reboot/shutdown` - 重启/关机
- `mount/umount` - 挂载/卸载文件系统
- `crontab -e` - 编辑定时任务

**✅ 低风险命令（只读）**
- `cat`, `less`, `more` - 查看文件
- `ls`, `find` - 列出文件
- `ps`, `top` - 查看进程
- `df`, `du` - 查看磁盘
- `netstat`, `ss` - 查看网络
- `grep`, `awk`, `sed`（不修改文件）

#### 2. 风险评估矩阵

| 操作 | 数据丢失风险 | 服务中断风险 | 系统稳定性风险 | 风险等级 |
|------|------------|------------|--------------|---------|
| 查看文件 | 无 | 无 | 无 | ✅ 低 |
| 删除日志文件 | 低 | 无 | 无 | ✅ 低 |
| 删除数据文件 | 高 | 无 | 无 | 🔴 高 |
| 重启应用服务 | 无 | 中 | 低 | ⚠️ 中 |
| 重启系统服务 | 无 | 高 | 中 | 🔴 高 |
| 删除系统文件 | 极高 | 极高 | 极高 | 🔴 高 |
| 修改防火墙规则 | 无 | 高 | 高 | 🔴 高 |
| 系统升级 | 中 | 高 | 高 | 🔴 高 |

#### 3. 命令验证流程

**步骤 1：理解命令**
- [ ] 阅读 `man` 手册
  ```bash
  man command_name
  ```
- [ ] 使用 `--help` 查看参数说明
  ```bash
  command_name --help
  ```
- [ ] 确认每个参数的作用

**步骤 2：模拟执行**
- [ ] 使用 `--dry-run` 参数（如果支持）
  ```bash
  apt-get install --dry-run package_name
  rsync --dry-run -av src/ dest/
  ```
- [ ] 使用 `echo` 预览完整命令
  ```bash
  echo "rm -rf /path/to/directory"
  ```
- [ ] 使用 `-n` 参数（如 rsync、make）

**步骤 3：小范围测试**
- [ ] 在测试环境执行
- [ ] 使用非关键数据测试
- [ ] 观察执行结果和影响

### 数据备份确认

#### 1. 识别需要备份的数据
- [ ] 配置文件
- [ ] 数据文件
- [ ] 日志文件
- [ ] 数据库
- [ ] 用户数据

#### 2. 备份方法

**文件备份**
```bash
# 创建带时间戳的备份
cp /path/to/file /path/to/file.bak.$(date +%Y%m%d_%H%M%S)

# 备份整个目录
cp -r /path/to/directory /path/to/directory.bak.$(date +%Y%m%d_%H%M%S)

# 使用 tar 打包备份
tar -czf backup_$(date +%Y%m%d_%H%M%S).tar.gz /path/to/directory
```

**数据库备份**
```bash
# MySQL 备份
mysqldump -u username -p database_name > backup_$(date +%Y%m%d_%H%M%S).sql

# PostgreSQL 备份
pg_dump -U username database_name > backup_$(date +%Y%m%d_%H%M%S).sql
```

**配置文件备份**
```bash
# 备份配置目录
tar -czf config_backup_$(date +%Y%m%d_%H%M%S).tar.gz /etc/nginx/

# 备份单个配置文件
cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak.$(date +%Y%m%d_%H%M%S)
```

#### 3. 备份验证
- [ ] 确认备份文件已创建
  ```bash
  ls -lh /path/to/backup*
  ```
- [ ] 验证备份文件完整性
  ```bash
  file backup_file.tar.gz
  tar -tzf backup_file.tar.gz | head
  ```
- [ ] 测试备份文件是否可恢复（非生产环境）

### 回滚准备

#### 1. 回滚方案设计
- [ ] 制定详细的回滚步骤
- [ ] 准备回滚命令
- [ ] 评估回滚操作的风险
- [ ] 设定回滚触发条件

#### 2. 回滚命令准备

**文件回滚**
```bash
# 从备份恢复
cp /path/to/file.bak.timestamp /path/to/file

# 使用 git 恢复（如果在版本控制下）
git checkout HEAD -- /path/to/file
```

**服务回滚**
```bash
# 重启服务
systemctl restart service_name

# 恢复配置后重启
systemctl reload service_name
```

**软件包回滚**
```bash
# Debian/Ubuntu
apt-get install package_name=version

# RHEL/CentOS
yum downgrade package_name
yum history undo transaction_id
```

#### 3. 回滚测试
- [ ] 在测试环境验证回滚方案
- [ ] 记录回滚所需时间
- [ ] 识别回滚可能遇到的问题

### 执行后验证

#### 1. 功能验证
- [ ] 验证操作目标是否达成
- [ ] 测试相关功能是否正常
- [ ] 验证服务是否正常运行
  ```bash
  systemctl status service_name
  ```

#### 2. 数据完整性检查
- [ ] 验证数据未丢失
- [ ] 验证数据未损坏
- [ ] 验证权限和所有权正确
  ```bash
  ls -l /path/to/file
  ```

#### 3. 系统状态检查
- [ ] 检查系统负载
  ```bash
  uptime
  ```
- [ ] 检查磁盘空间
  ```bash
  df -h
  ```
- [ ] 检查内存使用
  ```bash
  free -h
  ```
- [ ] 检查日志是否有错误
  ```bash
  journalctl -p err -n 50
  tail -n 50 /var/log/syslog
  ```

#### 4. 网络连接验证
- [ ] 测试网络连通性
  ```bash
  ping -c 4 target_ip
  ```
- [ ] 测试端口监听
  ```bash
  ss -tuln | grep port_number
  ```
- [ ] 测试服务可访问性
  ```bash
  curl -I http://localhost:port
  ```

#### 5. 文档更新
- [ ] 记录执行的命令
- [ ] 记录执行结果
- [ ] 记录执行时间
- [ ] 更新相关文档
- [ ] 记录遇到的问题和解决方案

## 示例

### 示例 1：重启 Nginx 服务前的检查清单

#### 执行前检查
```bash
# 1. 环境确认
whoami  # 确认用户
pwd     # 确认目录
cat /etc/os-release  # 确认系统

# 2. 配置文件备份
cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak.$(date +%Y%m%d_%H%M%S)

# 3. 配置文件验证
nginx -t

# 4. 当前状态
systemctl status nginx
```

#### 执行命令
```bash
systemctl reload nginx  # 优先使用 reload，平滑重载配置
# 或
systemctl restart nginx  # 如果需要重启
```

#### 执行后验证
```bash
# 1. 服务状态
systemctl status nginx

# 2. 端口监听
ss -tuln | grep :80

# 3. 功能测试
curl -I http://localhost

# 4. 日志检查
journalctl -u nginx -n 20
```

### 示例 2：删除文件前的检查清单

#### 执行前检查
```bash
# 1. 确认文件位置
pwd
ls -l /path/to/file

# 2. 确认文件内容（如果是配置文件）
cat /path/to/file

# 3. 确认文件未被使用
lsof /path/to/file

# 4. 创建备份
cp /path/to/file /path/to/file.bak.$(date +%Y%m%d_%H%M%S)
```

#### 执行命令
```bash
# 使用交互模式
rm -i /path/to/file

# 或先移动到临时目录
mv /path/to/file /tmp/deleted_$(date +%Y%m%d_%H%M%S)
```

#### 执行后验证
```bash
# 确认文件已删除
ls -l /path/to/file

# 验证系统正常运行
systemctl status related_service
```

### 示例 3：系统升级前的检查清单

#### 执行前检查
```bash
# 1. 系统信息
cat /etc/os-release
uname -a

# 2. 当前安装包状态
apt list --installed | grep package_name

# 3. 备份关键配置
tar -czf config_backup_$(date +%Y%m%d_%H%M%S).tar.gz /etc/

# 4. 数据库备份
mysqldump -u username -p database_name > db_backup_$(date +%Y%m%d_%H%M%S).sql

# 5. 检查可用更新
apt update
apt list --upgradable
```

#### 执行命令
```bash
# 先模拟执行
apt-get upgrade --dry-run

# 确认无误后执行
apt-get upgrade
```

#### 执行后验证
```bash
# 1. 服务状态
systemctl status critical_service

# 2. 系统负载
uptime

# 3. 日志检查
journalctl -p err -n 100

# 4. 功能测试
# 根据具体业务进行测试
```

## 约束与注意事项

1. **永远不要跳过执行前检查**
2. **高风险操作必须有备份**
3. **生产环境操作必须在低峰期进行**
4. **操作前必须通知相关人员**
5. **准备好回滚方案**
6. **执行过程中实时监控系统状态**
7. **执行后必须进行完整验证**
8. **记录所有操作和结果**

## 紧急情况处理

### 如果执行后发现错误
1. **立即停止操作**：按 `Ctrl+C` 中断正在执行的命令
2. **保留现场**：不要修改任何文件，记录错误信息
3. **收集日志**：
   ```bash
   journalctl -xe
   tail -n 100 /var/log/syslog
   ```
4. **评估影响**：确认哪些功能受到影响
5. **执行回滚**：按照准备的回滚方案恢复
6. **记录问题**：详细记录问题原因和解决方案
