# 展示中心 API 详细参数

## 告警统计数据查询

**URL**: `/dashboard/alarms/summary`

**请求方式**: POST

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| alarmStatus | string | 否 | 告警状态 (0-告警中, 1-已恢复) |

**响应参数**:

| 参数名 | 类型 | 说明 |
|--------|------|------|
| totalCount | long | 告警总数 |
| firingCount | long | 未恢复总数 |
| resolvedCount | long | 已恢复总数 |
| priorityGroup | map | 告警等级分组统计 |

**响应示例**:

```json
{
  "code": 0,
  "data": {
    "totalCount": 41,
    "firingCount": 38,
    "resolvedCount": 3,
    "priorityGroup": {
      "紧急告警": 2,
      "重要告警": 18,
      "提示警告": 2,
      "次要告警": 17
    }
  },
  "msg": ""
}
```

---

## 告警TOP统计查询

**URL**: `/dashboard/alarms/summary/top`

**请求方式**: POST

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| topNum | int | 否 | 返回几条TOP数据 |
| alarmStatus | string | 否 | 告警状态 |

**响应参数**:

| 参数名 | 类型 | 说明 |
|--------|------|------|
| alarmTitle | string | 告警标题 |
| alarmCount | int | 告警次数 |

**响应示例**:

```json
{
  "code": 0,
  "data": [
    {
      "alarmTitle": "MySQL慢查询",
      "alarmCount": 293
    },
    {
      "alarmTitle": "MySQL实例down",
      "alarmCount": 51
    }
  ],
  "msg": ""
}
```

---

## 告警列表查询

**URL**: `/dashboard/alarms/list`

**请求方式**: POST

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| pageNo | int | 是 | 页码 |
| pageSize | int | 是 | 每页数量 |
| alarmStatus | string | 否 | 告警状态 (0-告警中, 1-已恢复) |

**响应参数**:

| 参数名 | 类型 | 说明 |
|--------|------|------|
| alarmId | long | 告警记录ID |
| alarmTitle | string | 告警标题 |
| alarmStartTime | string | 告警时间 (yyyy-MM-dd HH:mm:ss) |
| assetTypeName | string | 资产类型名称 |
| assetName | string | 资产名称 |
| alarmCount | int | 告警次数 |
| assetStatus | string | 告警状态 (0-告警中, 1-已恢复) |

**响应示例**:

```json
{
  "code": 0,
  "data": [
    {
      "alarmId": 25,
      "alarmTitle": "MySQL慢查询",
      "alarmStartTime": "2025-09-11 18:10:32",
      "assetTypeName": null,
      "assetName": "",
      "alarmCount": 293,
      "assetStatus": "1"
    }
  ],
  "msg": ""
}
```

---

## 资产分布统计

**URL**: `/dashboard/asset-monitor/summary`

**请求方式**: POST

**请求参数**: 无

**响应参数**:

| 参数名 | 类型 | 说明 |
|--------|------|------|
| modelId | long | 资产模型ID |
| modelName | string | 模型名称 |
| modelCode | string | 模型编号 |
| assetTotalCount | int | 资产总数 |
| monitorStatusCounts | array | 分状态数量列表 |
| status | string | 监控状态 |
| statusStr | string | 监控状态文本 |
| count | long | 资产数量 |

**响应示例**:

```json
{
  "code": 0,
  "data": [
    {
      "modelId": 185,
      "modelName": "网络设备",
      "modelCode": "networkdevice",
      "assetTotalCount": 3,
      "monitorStatusCounts": [
        {
          "status": "0",
          "statusStr": "未监控",
          "count": 10
        }
      ]
    }
  ],
  "msg": ""
}
```

---

## 资源告警总览

**URL**: `/dashboard/asset-alarms/summary`

**请求方式**: POST

**请求参数**: 无

**响应参数**:

| 参数名 | 类型 | 说明 |
|--------|------|------|
| assetModelId | long | 资产模型ID |
| assetModelName | string | 资产模型名称 |
| assetCount | int | 资产数量 |
| alarmCount | int | 告警数量 |

**响应示例**:

```json
{
  "code": 0,
  "data": [
    {
      "assetModelId": 195,
      "assetModelName": "操作系统",
      "assetCount": 1,
      "alarmCount": 0
    }
  ],
  "msg": ""
}
```

---

## 告警设备TOP

**URL**: `/dashboard/asset-alarms/summary/top`

**请求方式**: POST

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| topNum | int | 否 | 返回几条TOP数据 |

**响应参数**:

| 参数名 | 类型 | 说明 |
|--------|------|------|
| assetId | long | 资产ID |
| assetName | string | 资产名称 |
| alarmCount | int | 告警数量 |

---

## 设备性能TOP

**URL**: `/dashboard/asset-metric/summary/top`

**请求方式**: POST

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| topNum | int | 否 | 返回几条TOP数据 |
| metricType | string | 是 | 性能数据类型 (cpu_memory_rate/disk_capacity) |

**响应参数**:

| 参数名 | 类型 | 说明 |
|--------|------|------|
| assetId | long | 资产ID |
| assetName | string | 资产名称 |
| cpuUsedRate | double | CPU使用率 |
| cpuUsedRateStr | string | CPU使用率(带%) |
| memoryUsedRate | double | 内存使用率 |
| memoryUsedRateStr | string | 内存使用率(带%) |
| diskUsedCapacity | double | 磁盘使用量 |
| diskUsedCapacityStr | string | 磁盘使用量(带单位) |
| diskTotalCapacity | double | 磁盘总量 |
| diskTotalCapacityStr | string | 磁盘总量(带单位) |
| diskUsedRate | double | 磁盘使用率 |
| diskUsedRateStr | string | 磁盘使用率(带%) |
