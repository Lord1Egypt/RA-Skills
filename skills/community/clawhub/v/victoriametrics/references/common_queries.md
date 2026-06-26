# Common Monitoring Queries

This reference provides ready-to-use PromQL queries for common monitoring scenarios.
Queries are provided for both **node_exporter** and **categraf** metric formats.

## Table of Contents

- [CPU Monitoring](#cpu-monitoring)
- [Memory Monitoring](#memory-monitoring)
- [Disk Monitoring](#disk-monitoring)
- [Network Monitoring](#network-monitoring)
- [System Load](#system-load)
- [GPU Monitoring](#gpu-monitoring)
- [Service Health](#service-health)

---

## CPU Monitoring

### node_exporter

```promql
# CPU usage (percentage)
100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# CPU usage per mode
avg by (instance, mode) (irate(node_cpu_seconds_total[5m])) * 100

# CPU usage per core
avg by (instance, cpu) (irate(node_cpu_seconds_total{mode!="idle"}[5m])) * 100

# CPU iowait percentage
avg by (instance) (irate(node_cpu_seconds_total{mode="iowait"}[5m])) * 100
```

### categraf

```promql
# CPU usage (percentage)
cpu_usage_active{cpu="cpu-total"}

# CPU usage per core
cpu_usage_active{cpu!="cpu-total"}

# CPU idle percentage
cpu_usage_idle{cpu="cpu-total"}

# CPU iowait percentage
cpu_usage_iowait{cpu="cpu-total"}
```

---

## Memory Monitoring

### node_exporter

```promql
# Memory usage (percentage)
(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100

# Memory used (bytes)
node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes

# Memory available (bytes)
node_memory_MemAvailable_bytes

# Memory total (bytes)
node_memory_MemTotal_bytes

# Swap usage (percentage)
(node_memory_SwapTotal_bytes - node_memory_SwapFree_bytes) / node_memory_SwapTotal_bytes * 100
```

### categraf

```promql
# Memory usage (percentage)
mem_used_percent

# Memory used (bytes)
mem_used

# Memory available (bytes)
mem_available

# Memory total (bytes)
mem_total

# Memory available percentage
mem_available_percent
```

---

## Disk Monitoring

### node_exporter

```promql
# Disk usage (percentage)
100 - (node_filesystem_avail_bytes / node_filesystem_size_bytes * 100)

# Disk usage per mount point
100 - ((node_filesystem_avail_bytes{mountpoint="/"}) / (node_filesystem_size_bytes{mountpoint="/"}) * 100)

# Disk available (bytes)
node_filesystem_avail_bytes

# Disk total (bytes)
node_filesystem_size_bytes

# Disk read rate (bytes/s)
rate(node_disk_read_bytes_total[5m])

# Disk write rate (bytes/s)
rate(node_disk_written_bytes_total[5m])

# Disk I/O utilization
rate(node_disk_io_time_seconds_total[5m]) * 100
```

### categraf

```promql
# Disk usage (percentage)
disk_used_percent

# Disk used (bytes)
disk_used

# Disk total (bytes)
disk_total

# Disk free (bytes)
disk_free

# Disk read rate (bytes/s)
rate(diskio_read_bytes[5m])

# Disk write rate (bytes/s)
rate(diskio_write_bytes[5m])

# Disk I/O utilization (percentage)
diskio_io_util
```

---

## Network Monitoring

### node_exporter

```promql
# Network receive rate (bytes/s)
rate(node_network_receive_bytes_total[5m])

# Network transmit rate (bytes/s)
rate(node_network_transmit_bytes_total[5m])

# Network receive errors
rate(node_network_receive_errs_total[5m])

# Network transmit errors
rate(node_network_transmit_errs_total[5m])

# Network packets received
rate(node_network_receive_packets_total[5m])

# Network packets transmitted
rate(node_network_transmit_packets_total[5m])
```

### categraf

```promql
# Network receive rate (bytes/s)
rate(net_bytes_recv[5m])

# Network transmit rate (bytes/s)
rate(net_bytes_sent[5m])

# Network receive errors
rate(net_err_in[5m])

# Network transmit errors
rate(net_err_out[5m])

# Network packets received
rate(net_packets_recv[5m])

# Network packets transmitted
rate(net_packets_sent[5m])
```

---

## System Load

### node_exporter

```promql
# Load average (1 minute)
node_load1

# Load average (5 minutes)
node_load5

# Load average (15 minutes)
node_load15

# Normalized load (per CPU)
node_load1 / count(node_cpu_seconds_total{mode="idle"}) without (cpu, mode)
```

### categraf

```promql
# Load average (1 minute)
system_load1

# Load average (5 minutes)
system_load5

# Load average (15 minutes)
system_load15

# Normalized load (per CPU)
system_load_norm_1
system_load_norm_5
system_load_norm_15
```

---

## GPU Monitoring

### DCGM Exporter

```promql
# GPU memory usage (percentage)
DCGM_FI_DEV_FB_USED / (DCGM_FI_DEV_FB_FREE + DCGM_FI_DEV_FB_USED) * 100

# GPU temperature (Celsius)
DCGM_FI_DEV_GPU_TEMP

# GPU utilization (percentage)
DCGM_FI_DEV_GPU_UTIL

# GPU memory bandwidth utilization
DCGM_FI_DEV_MEM_COPY_UTIL

# GPU power usage (Watts)
DCGM_FI_DEV_POWER_USAGE

# GPU encoder utilization
DCGM_FI_DEV_ENC_UTIL

# GPU decoder utilization
DCGM_FI_DEV_DEC_UTIL
```

### NVIDIA SMI Exporter

```promql
# GPU memory used (bytes)
nvidia_gpu_memory_used_bytes

# GPU memory total (bytes)
nvidia_gpu_memory_total_bytes

# GPU memory usage (percentage)
nvidia_gpu_memory_used_bytes / nvidia_gpu_memory_total_bytes * 100

# GPU temperature (Celsius)
nvidia_gpu_temperature_celsius
```

---

## Service Health

### Universal

```promql
# Service up status
up

# Service up status (specific job)
up{job="prometheus"}

# Count of up services
count(up == 1)

# Count of down services
count(up == 0)
```

### Application-specific

```promql
# MySQL up status
mysql_up

# Redis up status
redis_up

# HTTP response time (ms)
http_response_response_time_ms

# HTTP response code
http_response_response_code
```

---

## Process Monitoring

### node_exporter

```promql
# Process count by state
processes_total

# Running processes
processes_running

# Sleeping processes
processes_sleeping

# Zombie processes
processes_zombies
```

### categraf

```promql
# Process count
processes_total

# Running processes
processes_running

# Sleeping processes
processes_sleeping

# Zombie processes
processes_zombies

# Process threads
processes_total_threads
```

---

## Network Connections

### node_exporter

```promql
# TCP connections by state
netstat_tcp_established
netstat_tcp_time_wait
netstat_tcp_close_wait

# Total TCP connections
sum(netstat_tcp_*)

# UDP connections
netstat_udp_socket
```

### categraf

```promql
# TCP connections by state
netstat_tcp_established
netstat_tcp_time_wait
netstat_tcp_close_wait

# Total sockets used
netstat_sockets_used

# UDP connections
netstat_udp_socket
```

---

## Quick Reference Table

| Metric Type | node_exporter | categraf |
|-------------|---------------|----------|
| CPU Usage % | `100 - avg(irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100` | `cpu_usage_active{cpu="cpu-total"}` |
| Memory Usage % | `(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100` | `mem_used_percent` |
| Disk Usage % | `100 - (node_filesystem_avail_bytes / node_filesystem_size_bytes * 100)` | `disk_used_percent` |
| Network RX | `rate(node_network_receive_bytes_total[5m])` | `rate(net_bytes_recv[5m])` |
| Network TX | `rate(node_network_transmit_bytes_total[5m])` | `rate(net_bytes_sent[5m])` |
| Load 1m | `node_load1` | `system_load1` |
| Uptime | `node_time_seconds - node_boot_time_seconds` | `system_uptime` |

---

## Tips

1. **Auto-detect metric format**: Query both formats and use the one that returns data
2. **Label differences**:
   - node_exporter: `instance="host:port"`
   - categraf: `instance="host"`, `agent_hostname="host"`
3. **Rate calculations**: Always use `rate()` or `irate()` for counter metrics
4. **Time ranges**: Use `[5m]` for short-term trends, `[1h]` for longer-term analysis

---

## Examples

### Universal CPU Query (works with both)

```bash
# Try categraf first, fallback to node_exporter
node scripts/cli.js query 'cpu_usage_active{cpu="cpu-total"} or (100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100))'
```

### Universal Memory Query

```bash
node scripts/cli.js query 'mem_used_percent or ((node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100)'
```

### Universal Disk Query

```bash
node scripts/cli.js query 'disk_used_percent or (100 - (node_filesystem_avail_bytes / node_filesystem_size_bytes * 100))'
```
