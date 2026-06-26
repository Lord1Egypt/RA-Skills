# 计算类

## 产品参数

| 产品 | Namespace | Dimension Key | ID 格式 | 核心指标 |
|------|-----------|--------------|---------|---------|
| CVM 云服务器 | `QCE/CVM` | `InstanceId` | ins-xxx | CpuUsage, CpuLoadavg, MemUsage, CvmDiskUsage, LanIntraffic, LanOuttraffic, TcpCurrEstab, WanIntraffic, WanOuttraffic |
| Lighthouse 轻量应用 | `QCE/LIGHTHOUSE` | `InstanceId` | lhins-xxx | 同 CVM |
| CVM 内网监控 | `QCE/SDN_VM` | `unInstanceId` | ins-xxx | Vmconn, VmConnRatio |
| 专用宿主机 CDH | `QCE/HOST` | `lanip` + `hostid` | 宿主机IP+ID | LogicCpuUsage, MemUsage, MemAvailable, DiskAvailable, DiskReadTraffic, DiskWriteTraffic, Bond1Intraffic, Bond1Outtraffic |

## 指标决策表

| 问题现象 | 推荐指标 |
|----------|---------|
| CPU 高/卡顿/响应慢 | CpuUsage, CpuLoadavg, MemUsage, TcpCurrEstab |
| 内存不足/OOM | MemUsage, CpuUsage, CpuLoadavg |
| 磁盘满/IO 慢 | CvmDiskUsage, CpuUsage, CpuLoadavg, MemUsage |
| 网络异常/丢包 | WanIntraffic, WanOuttraffic, LanIntraffic, LanOuttraffic, TcpCurrEstab |
| 无法访问/宕机 | CpuUsage, MemUsage, CvmDiskUsage, LanIntraffic, LanOuttraffic, TcpCurrEstab |
| 笼统/不明确 | CpuUsage, MemUsage, CpuLoadavg, CvmDiskUsage, LanIntraffic, LanOuttraffic |

## 注意事项

- **CVM 自动关联 CBS**：脚本检测到 namespace=QCE/CVM 时，自动查询挂载的云硬盘并采集磁盘 IO 指标
- TAT 需实例已安装自动化助手 Agent（官方镜像默认已安装）

---

## OS 内部诊断（TAT 远程执行）

当监控数据发现异常需要定位根因（如 CPU>80% 需找进程）、或监控正常但用户反馈问题持续、或用户明确要求 OS 级排查时，**模型应主动触发** TAT 远程诊断。

**⚠️ 安全约束：TAT 只允许执行只读命令，严禁执行任何写入、修改、删除、重启、停止等变更操作。**

### 触发条件

以下情况应主动执行 OS 诊断，无需等用户指示：
- 监控数据发现异常（如 CPU > 80%），需定位具体进程
- 监控数据正常但用户反馈问题持续，需深入 OS 内部排查
- 用户要求"登录看看"、"查下进程"、"看下磁盘"等 OS 级排查

### 判断 OS 类型

prefetch.py 返回的 `instance_info.OsName` 中包含 `Windows` 则为 Windows，否则为 Linux。

### Linux 执行方式

使用 `prefetch.py --exec-tat` 一步完成（自动 base64 编码、执行、等待、解码输出）：

```bash
python3 scripts/prefetch.py \
  --instance-id <id> --product cvm --region <region> \
  --namespace QCE/CVM --dimension-key InstanceId \
  --exec-tat '<shell命令>'
```

返回 JSON 中 `output` 字段即为命令输出文本。可选 `--tat-timeout 120` 调整超时。

允许的命令：`top`、`ps`、`free`、`df`、`du`、`ss`、`netstat`、`ping`、`mtr`、`dig`、`cat`、`dmesg`、`journalctl`、`ip`、`last`、`uptime`、`iostat`、`vmstat` 等只读查询。
禁止的命令：`rm`、`kill`、`systemctl stop/restart`、`reboot`、`echo > file`、`iptables -A/-D/-F` 等变更命令。

### Linux 诊断命令决策表

| 问题现象 | 推荐命令 |
|----------|---------|
| **CPU/负载** | |
| CPU 高，需定位进程 | `top -bn1 -o %CPU \| head -20` |
| 负载高但 CPU 不高 | `uptime && ps -eo pid,stat,wchan,comm --sort=-vsz \| head -20` |
| **内存** | |
| 内存高/OOM | `free -h && echo '---' && ps aux --sort=-%mem \| head -15` |
| OOM 记录查询 | `dmesg -T \| grep -i 'oom\|killed' \| tail -20` |
| **磁盘/IO** | |
| 磁盘满 | `df -h && echo '---' && du -sh /* 2>/dev/null \| sort -rh \| head -15` |
| inode 耗尽 | `df -ih` |
| IO 高 | `iostat -xdm 1 3 2>/dev/null \|\| cat /proc/diskstats` |
| **网络互联** | |
| 网络不通/延迟高 | `ping -c 5 <目标IP> && echo '---' && mtr -rn -c 10 <目标IP>` |
| DNS 解析异常 | `dig <域名> && echo '---' && cat /etc/resolv.conf` |
| 端口连通性 | `curl -so /dev/null -w '%{http_code} %{time_total}s' http://<目标IP>:<端口>/ \|\| nc -zvw3 <目标IP> <端口>` |
| 路由/网卡状态 | `ip route show && echo '---' && ip addr show && echo '---' && ip -s link` |
| TCP 连接状态分布 | `ss -ant \| awk '{print $1}' \| sort \| uniq -c \| sort -rn` |
| 网络连接异常/丢包 | `ss -tunap \| head -30 && echo '---' && netstat -s \| grep -iE 'error\|drop\|retrans\|overflow'` |
| 防火墙/安全组规则 | `iptables -L -n --line-numbers 2>/dev/null && echo '---' && ip6tables -L -n 2>/dev/null` |
| **系统日志** | |
| 系统错误日志 | `dmesg -T \| tail -50` |
| 最近系统日志 | `journalctl --no-pager -n 50 --since '1 hour ago'` |
| 指定服务日志 | `journalctl --no-pager -u <服务名> -n 50` |
| 登录/安全日志 | `last -20 && echo '---' && lastb -10 2>/dev/null` |
| 内核/硬件错误 | `dmesg -T \| grep -iE 'error\|fail\|warn\|panic\|bug\|hardware' \| tail -30` |
| **进程/服务** | |
| 服务状态 | `systemctl list-units --state=failed` |
| 指定进程详情 | `ps -ef \| grep <进程名> && echo '---' && ls -l /proc/<PID>/fd 2>/dev/null \| wc -l` |
| 僵尸进程 | `ps aux \| awk '$8=="Z"'` |
| **综合巡检** | |
| 综合快速巡检 | `uptime && free -h && df -h && top -bn1 \| head -15` |
| 系统概况 | `uname -a && uptime && free -h && df -h && ip addr show \| grep 'inet ' && ss -ant \| wc -l` |

**注意**：`<目标IP>`、`<域名>`、`<端口>`、`<服务名>`、`<进程名>` 等占位符需根据用户描述替换为实际值。

### Windows 执行方式

Windows 不能用 `--exec-tat`，需手动执行 tccli（注意 `--CommandType POWERSHELL`）：

```bash
echo -n '<PowerShell命令>' | base64
tccli tat RunCommand --region <region> \
  --InstanceIds '["<instance-id>"]' \
  --CommandType POWERSHELL \
  --Content '<base64编码结果>' \
  --Timeout 60 --output json
```

### Windows 诊断命令决策表

| 问题现象 | PowerShell 命令 |
|----------|----------------|
| CPU/进程 | `Get-Process \| Sort-Object CPU -Descending \| Select-Object -First 15` |
| 内存 | `systeminfo \| Select-String 'Memory'` |
| 磁盘 | `Get-PSDrive -PSProvider FileSystem` |
| 网络连通性 | `Test-NetConnection -ComputerName <目标IP> -Port <端口>` |
| DNS 解析 | `Resolve-DnsName <域名>` |
| TCP 连接 | `Get-NetTCPConnection \| Group-Object State \| Sort-Object Count -Desc` |
| 系统日志 | `Get-EventLog -LogName System -Newest 30 -EntryType Error,Warning` |
| 服务状态 | `Get-Service \| Where-Object {$_.Status -ne 'Running' -and $_.StartType -eq 'Automatic'}` |
| 综合巡检 | `systeminfo \| Select-String 'OS Name,Total Physical,Available Physical,System Boot'; Get-PSDrive -PSProvider FileSystem` |
