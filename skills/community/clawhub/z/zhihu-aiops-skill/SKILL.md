---
name: zhihu-aiops
description: 智护运维平台 AIOps 集成技能。提供资产中心、CMDB 资产发现、监控告警、展示中心、VictoriaMetrics、Categraf SNMP 指标、操作系统监控添加和纳管设备智能巡检相关 API 参考与工作流。
version: 1.0.1
metadata:
  openclaw:
    requires:
      env:
        - ZHIHU_API_URL
        - ZHIHU_USER
        - ZHIHU_PASSWORD
        - VM_URL
      bins:
        - curl
        - python3
    primaryEnv: ZHIHU_API_URL
---

# 智护 AIOps Skill - 智护运维平台智能运维集成

> 当前版本: v1.0.1 | 最后更新: 2026-05-28 | 状态: 文档型 Skill，可注册安装，脚本执行能力将在下一阶段补充

智护 AIOps Skill 面向智护运维平台的智能问答、数字员工和 AIOps 场景，提供资产、监控、告警、CMDB 发现、纳管设备巡检、VictoriaMetrics 查询和 Categraf SNMP 指标查询的统一参考文档与操作流程。

本 Skill 适合用于：

- 查询智护平台资产中心数据，包括资产类型、资产模型、资产列表和纳管设备。
- 生成纳管设备巡检报告，覆盖安全设备、网络设备、终端设备、存储设备、数据库和操作系统。
- 查询展示中心和监控中心告警数据，包括告警总览、告警 TOP、告警列表和告警趋势。
- 查询 CMDB / 资产发现任务、扫描记录、扫描资产和 IP 使用率。
- 查询 VictoriaMetrics 中由 Categraf 写入的主机指标和 `snmp_*` SNMP 设备指标。
- 指导新增操作系统监控资产，包括登录、模型字段解析、连通性测试和资产创建。

## 配置

使用前请配置智护平台和 VictoriaMetrics 连接信息：

```bash
# 智护平台 API 地址，通常为当前部署环境内的后端服务地址
export ZHIHU_API_URL="http://zhihu-server:48080/admin-api"

# 智护平台登录账号
export ZHIHU_USER="admin"
export ZHIHU_PASSWORD="your-password"

# VictoriaMetrics 地址，Categraf 主机指标和 SNMP 指标统一写入该时序库
export VM_URL="http://zhihu-metric:9090"
```

不要在 Skill、脚本、提示词或文档中写死客户真实 IP、生产账号、生产密码或 API Key。跨环境部署时优先使用环境变量。

## 平台架构

```text
用户 / AI Agent
  |
  | 自然语言问题
  v
OpenClaw / ClawHub Skill
  |
  | 读取 SKILL.md 和 references/*.md
  v
智护平台 API
  |-- 资产中心: /cqt/asset-type、/cqt/asset-model、/cqt/asset-info
  |-- 监控中心: /monitor/*
  |-- 展示中心: /dashboard/*
  |-- CMDB 发现: /cmdb/*
  |
  v
智护数据

VictoriaMetrics
  ^
  |
Categraf
  |-- 主机 CPU / 内存 / 磁盘 / 网络指标
  |-- SNMP 网络设备 / 安全设备 / 存储设备指标，指标名前缀为 snmp_*
```

在智护当前架构中，网络设备、安全设备、存储设备等 SNMP 纳管设备不再依赖 Zabbix 查询，统一通过 Categraf 采集并写入 VictoriaMetrics。涉及交换机、路由器、防火墙、安全设备、存储设备、接口流量、SNMP 可达性时，应优先查询 `snmp_*` 指标。

## API 基础信息

- **Base URL**: `${ZHIHU_API_URL:-http://zhihu-server:48080/admin-api}`
- **请求方法**: 以 POST 为主，部分接口支持 GET
- **Content-Type**: `application/json`
- **认证方式**: 登录接口获取 Bearer Token
- **时序库**: `${VM_URL:-http://zhihu-metric:9090}`
- **时序查询协议**: Prometheus / VictoriaMetrics 兼容 API

## 认证方式

智护平台 API 使用登录接口获取访问令牌：

```bash
curl -sS -X POST "${ZHIHU_API_URL}/system/auth/login" \
  -H "Content-Type: application/json" \
  --data '{
    "username": "'"${ZHIHU_USER}"'",
    "password": "'"${ZHIHU_PASSWORD}"'",
    "captchaVerification": ""
  }'
```

响应示例：

```json
{
  "code": 0,
  "data": {
    "accessToken": "token-value",
    "refreshToken": "refresh-token-value",
    "expiresTime": "2026-05-28 18:00:00"
  },
  "msg": ""
}
```

后续请求添加认证头：

```bash
-H "Authorization: Bearer ${TOKEN}"
```

如果目标环境使用的是裸 token 格式，请按实际环境调整，但默认建议使用 Bearer Token。

## 返回格式

智护平台接口通常返回：

```json
{
  "code": 0,
  "data": {},
  "msg": ""
}
```

字段说明：

- `code`: 状态码，`0` 通常表示成功。
- `data`: 业务数据。
- `msg`: 错误或提示信息。

VictoriaMetrics 接口通常返回：

```json
{
  "status": "success",
  "data": {
    "resultType": "vector",
    "result": []
  }
}
```

## API 模块索引

### 1. 资产中心 Asset

资产中心用于查询和维护资产类型、资产模型和资产实例。

| 能力 | 接口 | 说明 |
|------|------|------|
| 资产类型列表 | `/cqt/asset-type/page` | 查询硬件资产、软件资产等资产分类 |
| 资产模型列表 | `/cqt/asset-model/page` | 查询网络设备、数据库、操作系统等模型定义 |
| 资产信息列表 | `/cqt/asset-info/page` | 查询具体资产实例，通常需要传入 `modelId` |
| 资产信息创建 | `/cqt/asset-info/create` | 创建资产实例 |
| 资产信息更新 | `/cqt/asset-info/update` | 更新资产信息 |
| 资产信息删除 | `/cqt/asset-info/delete` | 删除资产 |

详细参数见：`references/api_asset.md`

### 2. 纳管设备智能巡检

智能巡检用于按模型查询智护平台当前纳管设备，并输出巡检报告。

常用模型：

| 类型 | modelId | modelCode | 说明 |
|------|---------|-----------|------|
| 安全设备 | `254` | `securitydevice` | 防火墙、安全网关等 |
| 网络设备 | `185` | `networkdevice` | 交换机、路由器等 |
| 终端设备 | `260` | `terminaldevice` | 摄像头、终端等 |
| 存储设备 | `261` | `storagedevice` | 存储类硬件 |
| 数据库 | `183` | `storagebase` | Oracle、MySQL、Redis 等 |
| 操作系统 | `195` | `operatesystem` | Linux、Windows 主机 |

巡检基础请求体示例：

```json
{
  "pageNo": 1,
  "pageSize": 10,
  "isManaged": null,
  "modelId": 185,
  "conditions": [],
  "status": 1,
  "modelCode": "networkdevice",
  "isMonitorAble": true,
  "groupIdList": []
}
```

详细流程见：`references/inspection-run.md`

### 3. 监控中心 Monitor

监控中心用于查询告警规则、告警概览、拨测任务和监控记录。

| 能力 | 接口 | 说明 |
|------|------|------|
| 告警规则列表 | `/monitor/alarm-rules-case/page` | 查询告警规则 |
| 告警规则状态修改 | `/monitor/alarm-rules-case/modify-status` | 启用或禁用规则 |
| 告警等级分布 | `/monitor/alarms/overview/priority` | 按告警等级统计 |
| 告警恢复统计 | `/monitor/alarms/overview/resolved` | 查看恢复趋势 |
| 告警分布 | `/monitor/alarms/overview/distribution` | 按资产类型统计 |
| 告警趋势 | `/monitor/alarms/overview/trend` | 查询时间趋势 |
| 拨测任务列表 | `/monitor/dialing-test-task/page` | 查询拨测任务 |

详细参数见：`references/api_monitor.md`

### 4. 展示中心 Dashboard

展示中心用于查询大屏、首页和告警统计数据。

| 能力 | 接口 | 说明 |
|------|------|------|
| 告警统计 | `/dashboard/alarms/summary` | 告警总数、未恢复、已恢复、等级分组 |
| 告警 TOP | `/dashboard/alarms/summary/top` | 告警次数最多的项目 |
| 告警列表 | `/dashboard/alarms/list` | 分页查询告警记录 |
| 资产分布 | `/dashboard/asset-monitor/summary` | 资产模型分布统计 |
| 资源告警 | `/dashboard/asset-alarms/summary` | 各资产类型告警数量 |
| 性能 TOP | `/dashboard/asset-metric/summary/top` | CPU、内存、磁盘使用率 TOP |

详细参数见：`references/api_dashboard.md`

### 5. CMDB / 资产发现

CMDB 模块用于扫描任务、扫描记录和扫描资产查询。

| 能力 | 接口 | 说明 |
|------|------|------|
| 扫描任务列表 | `/cmdb/scan-task/page` | 查询资产发现任务 |
| 扫描任务创建 | `/cmdb/scan-task/create` | 创建扫描任务 |
| 扫描任务更新 | `/cmdb/scan-task/update` | 更新扫描任务 |
| 扫描任务删除 | `/cmdb/scan-task/delete` | 删除扫描任务 |
| 扫描任务重启 | `/cmdb/scan-task/restart` | 重新执行扫描 |
| 扫描记录列表 | `/cmdb/scan-record/page` | 查询扫描历史 |
| 扫描资产列表 | `/cmdb/scan-record/asset/page` | 查询发现的资产 |
| IP 使用率 | `/cmdb/scan-record/asset/ip-usage` | 统计 IP 使用情况 |

详细参数见：`references/api_cmdb.md`

### 6. VictoriaMetrics

VictoriaMetrics 提供主机指标和 SNMP 指标查询能力。

| 接口 | 说明 |
|------|------|
| `/api/v1/query` | 即时查询 |
| `/api/v1/query_range` | 范围查询 |
| `/api/v1/series` | 序列发现，适合发现 `snmp_*` 指标 |
| `/api/v1/label/__name__/values` | 查询指标名称 |
| `/api/v1/label/{label}/values` | 查询标签值 |

详细参数见：`references/api_victoriametrics.md`

### 7. Categraf SNMP 指标

SNMP 设备指标统一使用 `snmp_*` 前缀。

常见查询：

```promql
# 发现 SNMP 指标序列
{__name__=~"snmp_.*"}

# 查询指定设备 SNMP 可达性，具体指标名以采集模板为准
snmp_up{host_ip="10.0.0.5"}

# 查询接口入方向流量，换算为 bits/s
rate(snmp_ifHCInOctets{host_ip="10.0.0.5"}[5m]) * 8

# 查询接口出方向流量，换算为 bits/s
rate(snmp_ifHCOutOctets{host_ip="10.0.0.5"}[5m]) * 8
```

详细说明见：`references/api_snmp_metrics.md`

### 8. 操作系统监控添加

当用户要求添加 Linux / Windows 主机监控时，需要收集以下信息：

| 参数 | 说明 | 示例 |
|------|------|------|
| `monitorIp` | 目标主机 IP | `192.0.2.10` |
| `monitorPort` | SSH 或 WinRM 端口 | `22` / `5985` |
| `userName` | 登录用户名 | `root` / `Administrator` |
| `password` | 登录密码 | `your-password` |
| `name` | 监控名称 | `web-server-01` |

执行流程：

1. 登录智护平台获取 Token。
2. 查询操作系统资产模型和字段映射。
3. 调用连通性测试接口。
4. 连通成功后创建操作系统资产。
5. 返回创建结果和后续监控建议。

详细流程见：`references/add-os-monitor.md`

## 使用示例

### 查询告警统计

```bash
TOKEN=$(curl -sS -X POST "${ZHIHU_API_URL}/system/auth/login" \
  -H "Content-Type: application/json" \
  --data '{"username":"'"${ZHIHU_USER}"'","password":"'"${ZHIHU_PASSWORD}"'","captchaVerification":""}' \
  | python3 -c 'import sys,json; print((json.load(sys.stdin).get("data") or {}).get("accessToken", ""))')

curl -sS -X POST "${ZHIHU_API_URL}/dashboard/alarms/summary" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  --data '{}'
```

### 查询网络设备资产

```bash
curl -sS -X POST "${ZHIHU_API_URL}/cqt/asset-info/page" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  --data '{
    "pageNo": 1,
    "pageSize": 10,
    "isManaged": null,
    "modelId": 185,
    "conditions": [],
    "status": 1,
    "modelCode": "networkdevice",
    "isMonitorAble": true,
    "groupIdList": []
  }'
```

### 查询 SNMP 指标序列

```bash
curl -sS "${VM_URL}/api/v1/series?match%5B%5D=%7B__name__%3D~%5C%22snmp_.*%5C%22%7D"
```

### 查询任意 PromQL

```bash
curl -sG "${VM_URL}/api/v1/query" \
  --data-urlencode 'query=up'
```

## 参考文档

### 核心 API

- `references/api_asset.md` - 资产中心 API 详细参数
- `references/api_cmdb.md` - CMDB / 资产发现 API 详细参数
- `references/api_dashboard.md` - 展示中心 API 详细参数
- `references/api_monitor.md` - 监控中心 API 详细参数

### 指标与巡检

- `references/api_victoriametrics.md` - VictoriaMetrics API 参考
- `references/api_snmp_metrics.md` - Categraf SNMP 指标查询参考
- `references/inspection-run.md` - 纳管设备智能巡检工作流
- `references/add-os-monitor.md` - 新增操作系统监控工作流

## 注意事项

1. **认证 Token**: 智护平台 Token 有有效期，执行任务前建议重新登录获取。
2. **资产查询**: 资产实例查询优先使用 `/cqt/asset-info/page`，但通常需要先知道 `modelId`。
3. **模型与资产不同**: 资产模型是字段定义，资产信息才是具体设备或实例。
4. **SNMP 架构**: 当前 SNMP 设备指标统一通过 Categraf 写入 VictoriaMetrics，不再使用 Zabbix 查询链路。
5. **环境变量**: 不要把测试环境 IP、账号、密码写进 Skill，统一使用 `ZHIHU_API_URL`、`ZHIHU_USER`、`ZHIHU_PASSWORD`、`VM_URL`。
6. **安全边界**: 该 Skill 会指导访问用户配置的智护平台和 VictoriaMetrics 地址，不应访问无关外部系统。
7. **第一阶段限制**: 当前版本是文档型 Skill，能提供 API 参考和工作流指导；确定性 CLI 工具将在后续版本补充。

## 后续规划

下一阶段计划增加 `scripts/zhihu_cli.py`，提供可直接执行的命令：

```bash
python3 scripts/zhihu_cli.py login
python3 scripts/zhihu_cli.py alarm-summary
python3 scripts/zhihu_cli.py asset-page --model-code networkdevice
python3 scripts/zhihu_cli.py inspect-managed-assets --scope all
python3 scripts/zhihu_cli.py vm-query --query 'up'
python3 scripts/zhihu_cli.py snmp-discover
python3 scripts/zhihu_cli.py add-os-monitor --ip 192.0.2.10 --port 22 --username root --password your-password --name web-server-01
```

## 版本历史

- v1.0.1 (2026-05-28): 改为中文主页文档，补充智护架构、模块索引、使用示例、巡检模型、SNMP/VictoriaMetrics 说明。
- v1.0.0 (2026-05-28): 初始 ClawHub 注册版本，整理 `SKILL.md` 和 `references/`。
