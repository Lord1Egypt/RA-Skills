# Categraf SNMP 指标 API 参考

智护当前网络设备、安全设备、存储设备等 SNMP 纳管设备不再通过独立监控系统查询，统一由 Categraf 采集并写入 VictoriaMetrics。所有 SNMP 相关查询优先使用 `snmp_*` 指标。

## 连接信息

- **时序库地址**: `${VM_URL:-http://zhihu-metric:9090}`
- **即时查询**: `/api/v1/query`
- **范围查询**: `/api/v1/query_range`
- **序列发现**: `/api/v1/series`
- **指标名发现**: `/api/v1/label/__name__/values`

## 使用原则

1. 网络设备、交换机、路由器、防火墙、安全设备、存储设备的监控指标统一查 `snmp_*`。
2. 如果用户只说“网络设备状态”或“SNMP 状态”，优先发现可用 `snmp_*` 指标，再查询可达性或核心指标。
3. 如果用户询问接口流量，优先使用 octets 类指标，通过 `rate(...[5m]) * 8` 换算为 bits/s。
4. 如果用户询问设备数量或资产清单，优先使用智护平台资产接口 `/cqt/asset-info/page`，不要用指标序列数量直接等同资产数量。
5. 如果查询无数据，明确提示可能是 Categraf SNMP 采集未配置、标签不匹配、时间范围不正确或设备未产生指标。

## 常用标签

不同采集模板可能存在差异，优先尝试以下标签：

| 标签 | 说明 |
|------|------|
| `host_ip` | 设备 IP，智护默认优先使用 |
| `instance` | 采集实例，可能包含 `ip:port` |
| `agent_hostname` | Categraf Agent 主机名 |
| `ifName` | 接口名称 |
| `ifDescr` | 接口描述 |
| `ifIndex` | 接口索引 |
| `name` | 指标或设备名称 |

## 指标发现

### 发现所有 SNMP 序列

```bash
curl -G "${VM_URL:-http://zhihu-metric:9090}/api/v1/series" \
  --data-urlencode 'match[]={__name__=~"snmp_.*"}'
```

### 发现指定设备的 SNMP 序列

```bash
curl -G "${VM_URL:-http://zhihu-metric:9090}/api/v1/series" \
  --data-urlencode 'match[]={__name__=~"snmp_.*",host_ip="10.0.0.5"}'
```

### 查询所有指标名并过滤 SNMP

```bash
curl "${VM_URL:-http://zhihu-metric:9090}/api/v1/label/__name__/values" | \
  python3 -c 'import json,sys; print("\n".join([m for m in json.load(sys.stdin).get("data", []) if m.startswith("snmp_")]))'
```

## 常见查询示例

### 设备可达性

如果环境中存在 `snmp_up`：

```promql
snmp_up{host_ip="10.0.0.5"}
```

如果没有 `snmp_up`，先 discover 指标，再选择设备基础指标做可用性判断。

### 接口入方向流量

```promql
rate(snmp_ifHCInOctets{host_ip="10.0.0.5",ifName="GigabitEthernet0/1"}[5m]) * 8
```

### 接口出方向流量

```promql
rate(snmp_ifHCOutOctets{host_ip="10.0.0.5",ifName="GigabitEthernet0/1"}[5m]) * 8
```

### 接口错误包速率

```promql
rate(snmp_ifInErrors{host_ip="10.0.0.5"}[5m])
rate(snmp_ifOutErrors{host_ip="10.0.0.5"}[5m])
```

### 接口状态

```promql
snmp_ifOperStatus{host_ip="10.0.0.5"}
snmp_ifAdminStatus{host_ip="10.0.0.5"}
```

### Top 接口流量

```promql
topk(10, rate(snmp_ifHCInOctets[5m]) * 8)
```

## AI 工具调用建议

当用户询问 SNMP 或网络设备指标时，使用 `query_snmp_metrics`：

```json
{
  "action": "discover",
  "ip": "10.0.0.5",
  "limit": 50
}
```

```json
{
  "action": "range",
  "query": "rate(snmp_ifHCInOctets{host_ip=\"10.0.0.5\"}[5m]) * 8",
  "time_range": "1h",
  "step": "60s"
}
```

当用户询问普通主机 CPU、内存、磁盘、网络指标时，继续使用 `query_victoriametrics`。
