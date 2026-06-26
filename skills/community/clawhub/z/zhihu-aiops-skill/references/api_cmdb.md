# CMDB 扫描 API 详细参数

## 扫描任务管理

### 扫描任务列表

**URL**: `/cmdb/scan-task/page`

**请求方式**: POST

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| pageNo | int | 是 | 页码 |
| pageSize | int | 是 | 每页数量 |
| taskName | string | 否 | 任务名称(搜索) |

### 创建扫描任务

**URL**: `/cmdb/scan-task/create`

**请求方式**: POST

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| taskName | string | 是 | 任务名称 |
| scanRange | string | 是 | 扫描范围 (IP段，如: 192.168.1.0/24) |
| scanType | string | 是 | 扫描类型 (ICMP/SNMP) |
| snmpCommunity | string | 否 | SNMP团体名 |
| snmpVersion | string | 否 | SNMP版本 |

### 更新扫描任务

**URL**: `/cmdb/scan-task/update`

**请求方式**: POST

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | int | 是 | 任务ID |
| taskName | string | 否 | 任务名称 |
| scanRange | string | 否 | 扫描范围 |
| ... | ... | 否 | 其他参数 |

### 删除扫描任务

**URL**: `/cmdb/scan-task/delete`

**请求方式**: POST

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | int | 是 | 任务ID |

### 重启扫描任务

**URL**: `/cmdb/scan-task/restart`

**请求方式**: POST

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | int | 是 | 任务ID |

---

## 扫描记录管理

### 扫描记录列表

**URL**: `/cmdb/scan-record/page`

**请求方式**: POST

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| pageNo | int | 是 | 页码 |
| pageSize | int | 是 | 每页数量 |
| taskId | int | 否 | 任务ID |

### 扫描资产列表

**URL**: `/cmdb/scan-record/asset/page`

**请求方式**: POST

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| pageNo | int | 是 | 页码 |
| pageSize | int | 是 | 每页数量 |
| recordId | int | 否 | 记录ID |

### 扫描资产导出

**URL**: `/cmdb/scan-record/asset/export`

**请求方式**: POST

**说明**: 导出扫描发现的资产数据

---

## IP 管理

### IP 使用率统计

**URL**: `/cmdb/scan-record/asset/ip-usage`

**请求方式**: POST

**说明**: 统计IP地址的使用情况

**响应示例**:

```json
{
  "code": 0,
  "data": {
    "total": 256,
    "used": 150,
    "unused": 106,
    "usageRate": "58.59%"
  },
  "msg": ""
}
```
