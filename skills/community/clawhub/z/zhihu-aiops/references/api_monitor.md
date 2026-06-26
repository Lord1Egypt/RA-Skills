# 监控中心 API 详细参数

## 告警规则管理

### 告警规则列表

**URL**: `/monitor/alarm-rules-case/page`

**请求方式**: POST

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| pageNo | int | 是 | 页码 |
| pageSize | int | 是 | 每页数量 |
| ruleName | string | 否 | 规则名称(搜索) |

### 修改告警规则状态

**URL**: `/monitor/alarm-rules-case/modify-status`

**请求方式**: POST

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | int | 是 | 规则ID |
| status | int | 是 | 状态 (1-启用, 0-禁用) |

---

## 告警概览统计

### 告警等级分布

**URL**: `/monitor/alarms/overview/priority`

**请求方式**: POST

**说明**: 按告警等级分组统计

### 告警恢复统计

**URL**: `/monitor/alarms/overview/resolved`

**请求方式**: POST

**说明**: 告警恢复趋势统计

### 告警分布

**URL**: `/monitor/alarms/overview/distribution`

**请求方式**: POST

**说明**: 按资产类型统计告警分布

### 告警日报

**URL**: `/monitor/alarms/overview/daily`

**请求方式**: POST

**说明**: 每日告警数量统计

### 告警趋势

**URL**: `/monitor/alarms/overview/trend`

**请求方式**: POST

**说明**: 告警时间趋势分析

### 告警TOP

**URL**: `/monitor/alarms/overview/{type}/top`

**请求方式**: POST

**路径参数**:

| 参数名 | 类型 | 说明 |
|--------|------|------|
| type | string | 类型 (asset-资产, rule-规则) |

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| topNum | int | 否 | 返回数量 |

---

## 拨测任务管理

### 拨测任务列表

**URL**: `/monitor/dialing-test-task/page`

**请求方式**: POST

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| pageNo | int | 是 | 页码 |
| pageSize | int | 是 | 每页数量 |
| taskName | string | 否 | 任务名称(搜索) |

### 创建拨测任务

**URL**: `/monitor/dialing-test-task/create`

**请求方式**: POST

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| taskName | string | 是 | 任务名称 |
| taskType | string | 是 | 任务类型 (HTTP/TCP/PING) |
| taskParams | object | 是 | 任务参数 |
| alarmRules | array | 否 | 告警规则 |

**HTTP拨测参数示例**:

```json
{
  "taskName": "接口健康检查",
  "taskType": "HTTP",
  "taskParams": {
    "httpParams": {
      "requestUrl": "http://example.com/api/health",
      "requestMethod": "GET",
      "requestHeaders": [],
      "requestParams": [],
      "expectResponseCode": 200,
      "expectResponseBody": ""
    }
  }
}
```

### 更新拨测任务

**URL**: `/monitor/dialing-test-task/update`

**请求方式**: POST

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | int | 是 | 任务ID |
| ... | ... | 否 | 其他要更新的字段 |

### 删除拨测任务

**URL**: `/monitor/dialing-test-task/delete`

**请求方式**: POST

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | int | 是 | 任务ID |

### 拨测任务触发状态修改

**URL**: `/monitor/dialing-test-task/trigger-status`

**请求方式**: POST

### 拨测任务告警规则列表

**URL**: `/monitor/dialing-test-task/alarm-rules/list`

**请求方式**: POST

### 拨测任务关联资产列表

**URL**: `/monitor/dialing-test-task/asset/list`

**请求方式**: POST

---

## 拨测记录

### 拨测记录列表

**URL**: `/monitor/dialing-test-task/record/page`

**请求方式**: POST

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| pageNo | int | 是 | 页码 |
| pageSize | int | 是 | 每页数量 |
| taskId | int | 否 | 任务ID |

### 拨测指标查询

**URL**: `/monitor/dialing-test-task/record/metric`

**请求方式**: POST

---

## HTTP拨测测试

**URL**: `/monitor/dialing-test-task/http-test`

**请求方式**: POST

**请求参数**:

```json
{
  "taskType": "HTTP",
  "taskParams": {
    "httpParams": {
      "requestUrl": "http://example.com/api",
      "requestMethod": "POST",
      "requestHeaders": [],
      "requestParams": [],
      "expectResponseCode": 200
    }
  }
}
```
