# VictoriaMetrics API 参考

## 连接信息

- **地址**: `${VM_URL:-http://zhihu-metric:9090}`
- **查询接口**: `/api/v1/query`
- **范围查询**: `/api/v1/query_range`
- **标签查询**: `/api/v1/label/{label_name}/values`

---

## 即时查询

### /api/v1/query

执行 PromQL 即时查询。

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| query | string | 是 | PromQL 查询语句 |
| time | string | 否 | 查询时间 (RFC3339或Unix时间戳) |
| timeout | string | 否 | 超时时间 |

**响应格式**:

```json
{
  "status": "success",
  "data": {
    "resultType": "vector",
    "result": [
      {
        "metric": {
          "__name__": "cpu_usage_idle",
          "cpu": "cpu-total",
          "host_ip": "192.168.1.100"
        },
        "value": [1678888888, "85.5"]
      }
    ]
  }
}
```

---

## 范围查询

### /api/v1/query_range

执行 PromQL 范围查询。

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| query | string | 是 | PromQL 查询语句 |
| start | string | 是 | 开始时间 (RFC3339或Unix时间戳) |
| end | string | 是 | 结束时间 (RFC3339或Unix时间戳) |
| step | string | 是 | 步长 (如: 60s, 5m, 1h) |
| timeout | string | 否 | 超时时间 |

**响应格式**:

```json
{
  "status": "success",
  "data": {
    "resultType": "matrix",
    "result": [
      {
        "metric": {
          "__name__": "mem_used_percent",
          "host_ip": "192.168.1.100"
        },
        "values": [
          [1678888800, "45.2"],
          [1678889100, "46.1"],
          [1678889400, "44.8"]
        ]
      }
    ]
  }
}
```

---

## 标签查询

### /api/v1/label/{label_name}/values

查询标签的所有值。

**路径参数**:

| 参数名 | 类型 | 说明 |
|--------|------|------|
| label_name | string | 标签名 (如: __name__, host_ip) |

**响应格式**:

```json
{
  "status": "success",
  "data": ["value1", "value2", "value3"]
}
```

### 查询所有指标名

使用特殊标签 `__name__` 查询所有指标名称。

```bash
curl "${VM_URL:-http://zhihu-metric:9090}/api/v1/label/__name__/values"
```

---

## 常用 PromQL

### CPU 相关

```promql
# CPU 使用率 (100 - 空闲率)
100 - cpu_usage_idle{cpu="cpu-total"}

# 按主机分组的 CPU 使用率
100 - cpu_usage_idle{cpu="cpu-total"} by (host_ip)

# 系统负载
system_load1
system_load5
system_load15
```

### 内存相关

```promql
# 内存使用率
mem_used_percent

# 可用内存
mem_available

# 总内存
mem_total

# 交换分区使用率
(1 - mem_swap_free / mem_swap_total) * 100 and mem_swap_total > 0
```

### 磁盘相关

```promql
# 磁盘使用率
disk_used_percent

# 按挂载点分组
disk_used_percent by (host_ip, path)

# 磁盘IO使用率
rate(diskio_io_time[5m]) / 10
```

### 网络相关

```promql
# 接收速率 (bytes/sec)
rate(net_bytes_recv{interface!~"docker.*|br.*|veth.*"}[1m])

# 发送速率 (bytes/sec)
rate(net_bytes_sent{interface!~"docker.*|br.*|veth.*"}[1m])

# 接收速率 (bits/sec)
rate(net_bytes_recv{interface!~"docker.*|br.*|veth.*"}[1m]) * 8

# 错误包率
rate(net_err_in[1m])
rate(net_err_out[1m])
```

### 系统相关

```promql
# 系统运行时间
system_uptime

# 进程数
processes_total
processes_zombies
processes_running

# TCP 连接数
netstat_tcp_inuse
netstat_tcp_tw
```

### 聚合查询

```promql
# 统计主机数量
count(system_uptime) by (component_type)

# 平均 CPU 使用率
avg(cpu_usage_idle{cpu="cpu-total"})

# TOP 10 内存使用率
 topk(10, mem_used_percent)

# 磁盘使用率大于 80% 的主机
 disk_used_percent > 80
```

---

## 指标命名规范 (Categraf/Telegraf)

| 前缀 | 类别 | 常见指标 |
|------|------|---------|
| `cpu_` | CPU | `cpu_usage_idle`, `cpu_usage_user`, `cpu_usage_system`, `cpu_usage_iowait` |
| `mem_` | 内存 | `mem_used_percent`, `mem_total`, `mem_available`, `mem_used`, `mem_swap_*` |
| `disk_` | 磁盘 | `disk_used_percent`, `disk_total`, `disk_used`, `disk_free`, `disk_inodes_*` |
| `diskio_` | 磁盘IO | `diskio_io_time`, `diskio_reads`, `diskio_writes`, `diskio_read_bytes`, `diskio_write_bytes` |
| `net_` | 网络 | `net_bytes_recv`, `net_bytes_sent`, `net_packets_*`, `net_err_*`, `net_drop_*` |
| `netstat_` | TCP连接 | `netstat_tcp_inuse`, `netstat_tcp_tw`, `netstat_tcp_orphan`, `netstat_sockets_used` |
| `system_` | 系统 | `system_load1/5/15`, `system_uptime`, `system_n_cpus`, `system_n_users` |
| `processes_` | 进程 | `processes_total`, `processes_zombies`, `processes_running`, `processes_sleeping` |
| `kernel_` | 内核 | `kernel_context_switches`, `kernel_interrupts` |
| `snmp_` | SNMP设备 | 由 Categraf SNMP 插件采集，覆盖交换机、路由器、防火墙、安全设备、存储设备等 |

### SNMP 设备指标

智护当前已统一使用 Categraf + VictoriaMetrics 承载网络设备 SNMP 监控数据。查询网络设备、安全设备、存储设备时，优先查询 `snmp_*` 指标。

```promql
# 发现 SNMP 指标序列
{__name__=~"snmp_.*"}

# 指定设备可达性（如果采集模板提供 snmp_up）
snmp_up{host_ip="10.0.0.5"}

# 接口入方向流量 bits/s
rate(snmp_ifHCInOctets{host_ip="10.0.0.5"}[5m]) * 8

# 接口出方向流量 bits/s
rate(snmp_ifHCOutOctets{host_ip="10.0.0.5"}[5m]) * 8
```

---

## 常用标签

| 标签名 | 说明 |
|--------|------|
| `__name__` | 指标名称 |
| `host_ip` | 主机IP地址 |
| `agent_hostname` | Agent主机名 |
| `name` | 设备/接口名称 |
| `component_type` | 组件类型 (如: Linux, Windows) |
| `cpu` | CPU编号 (cpu-total, cpu0, cpu1...) |
| `path` | 挂载路径 |
| `interface` | 网络接口名 |
| `device` | 磁盘设备名 |

---

## 请求示例

### 即时查询

```bash
curl "${VM_URL:-http://zhihu-metric:9090}/api/v1/query?query=mem_used_percent"
```

### 范围查询

```bash
curl "${VM_URL:-http://zhihu-metric:9090}/api/v1/query_range?query=cpu_usage_idle{cpu=%22cpu-total%22}&start=1678888800&end=1678975200&step=300"
```

### 搜索指标

```bash
curl "${VM_URL:-http://zhihu-metric:9090}/api/v1/label/__name__/values" | \
  python3 -c "import json,sys; [print(m) for m in json.load(sys.stdin)['data'] if 'cpu' in m]"
```
