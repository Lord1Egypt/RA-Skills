# 校验规则管理 - 数据模型参考

## DTO 定义

### ValidateRuleDTO
校验规则DTO

| 字段 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| id | integer(int64) | 否 | 规则ID，更新时必填 | 1 |
| groupId | integer(int64) | 是 | 所属规则组ID | 1 |
| objectId | string | 是 | 校验对象 | Invoice |
| countryCode | string | 是 | 国家/地区代码，ISO 3166 | CN |
| ruleCode | string | 是 | 规则编码 | CN-SELLER-001 |
| ruleName | string | 是 | 规则名称 | 卖方名称必填校验 |
| description | string | 否 | 规则说明 | 校验卖方名称不能为空 |
| preconditions | string | 否 | 条件表达式 | countryCode == 'CN' |
| fieldKey | string | 否 | 字段key，非字段级校验不填 | sellerName |
| ruleType | string | 是 | 校验类型 | required |
| errorLevel | string | 是 | 错误级别：error/warn/info | error |
| errorCode | string | 否 | 对外暴露的错误码 | E10001 |
| errorMessage | string | 是 | 错误信息模板，支持{field}占位符 | {field}不能为空 |
| executionOrder | integer(int32) | 是 | 同规则组下规则的执行顺序 | 1 |
| status | string | 是 | 状态：draft/enabled/disabled | enabled |
| effectiveStart | string(date-time) | 否 | 生效日期 | 2024-01-01 |
| effectiveEnd | string(date-time) | 否 | 失效日期，NULL表示永久有效 | 2099-12-31 |
| extensions | object | 否 | 扩展属性 | {} |

---

### ValidateRuleGroupDTO
校验规则组DTO

| 字段 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| id | integer(int64) | 否 | 规则组ID，更新时必填 | 1 |
| parentId | integer(int64) | 否 | 父级ID | 0 |
| tenantId | integer(int64) | 否 | 所属租户 | 1 |
| groupName | string | 是 | 规则组名称 | 基础信息校验组 |
| description | string | 否 | 规则组说明 | 用于校验发票基础信息 |
| orderNum | integer(int32) | 是 | 顺序号 | 1 |

---

### ValidateSceneDTO
校验场景DTO

| 字段 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| id | integer(int64) | 否 | 场景ID，更新时必填 | 1 |
| sceneCode | string | 是 | 场景编码 | CN_VAT_SPECIAL |
| sceneName | string | 是 | 场景名称 | 中国增值税专票场景 |
| description | string | 否 | 场景说明 | 用于校验中国增值税专用发票 |
| status | string | 是 | 状态：draft/enabled/disabled | enabled |
| errorStrategy | string | 是 | 异常策略 | stop_on_error |
| extensions | object | 否 | 扩展属性 | {} |
| rules | array | 否 | 关联规则列表 | [] |

**errorStrategy 枚举值**:
- `stop_on_error`: 异常就结束
- `continue_all`: 执行所有

---

## QueryRequest 定义

### ValidateRuleQueryRequest
查询校验规则请求

| 字段 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| id | integer(int64) | 否 | 规则ID | 1 |
| groupId | integer(int64) | 否 | 所属规则组ID | 1 |
| objectId | string | 否 | 校验对象 | Invoice |
| countryCode | string | 否 | 国家/地区代码 | CN |
| ruleCode | string | 否 | 规则编码 | CN-SELLER-001 |
| ruleName | string | 否 | 规则名称 | 卖方名称必填校验 |
| fieldKey | string | 否 | 字段key | sellerName |
| ruleType | string | 否 | 校验类型 | required |
| status | string | 否 | 状态 | enabled |
| pageNum | integer(int32) | 是 | 当前页码 | 1 |
| pageSize | integer(int32) | 是 | 每页条数 | 10 |

---

### ValidateRuleGroupQueryRequest
查询校验规则组请求

| 字段 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| id | integer(int64) | 否 | 规则组ID | 1 |
| parentId | integer(int64) | 否 | 父级ID | 0 |
| groupName | string | 否 | 规则组名称 | 基础信息校验组 |
| pageNum | integer(int32) | 是 | 当前页码 | 1 |
| pageSize | integer(int32) | 是 | 每页条数 | 10 |

---

### ValidateSceneQueryRequest
查询校验场景请求

| 字段 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| id | integer(int64) | 否 | 场景ID | 1 |
| sceneCode | string | 否 | 场景编码 | CN_VAT_SPECIAL |
| sceneName | string | 否 | 场景名称 | 中国增值税专票场景 |
| status | string | 否 | 状态 | enabled |
| pageNum | integer(int32) | 是 | 当前页码 | 1 |
| pageSize | integer(int32) | 是 | 每页条数 | 10 |

---

## 其他 DTO

### EntityPrimaryKeyDTO
实体主键DTO（用于详情查询、删除、启停）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | integer(int64) | 是 | 实体ID |

---

### SaveGroupOrdersRequest
保存组顺序请求

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| groupOrders | array | 是 | 组顺序列表 |

### GroupOrderDTO
组顺序DTO

| 字段 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| id | integer(int64) | 是 | 规则组ID | 1 |
| orderNum | integer(int32) | 是 | 顺序号 | 1 |

---

### ValidateEntitySchemasRequest
获取校验对象参数结构请求

| 字段 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| countryCode | string | 是 | 国家/地区代码 | CN |

---

## 响应结构

### BWJsonResultDto<T>
通用响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| requestId | string | 请求ID |
| success | boolean | 是否成功 |
| message | string | 消息 |
| errorCode | string | 错误码 |
| errorMsg | string | 错误信息 |
| total | integer | 总记录数（分页查询时） |
| data | T / array | 数据 |
| extInfo | object | 扩展信息 |
| kind | integer | 类型 |

---

## API 端点汇总

### 校验规则管理
| 接口 | 方法 | 说明 |
|------|------|------|
| /admin/validateRule/create | POST | 新增校验规则 |
| /admin/validateRule/update | POST | 更新校验规则 |
| /admin/validateRule/delete | POST | 删除校验规则 |
| /admin/validateRule/enable | POST | 启用校验规则 |
| /admin/validateRule/disable | POST | 禁用校验规则 |
| /admin/validateRule/queryPageList | POST | 分页查询校验规则 |
| /admin/validateRule/queryDetail | POST | 根据ID查询校验规则 |
| /admin/validateRule/validateEntitySchemas | POST | 获取校验对象参数结构 |

### 校验规则组管理
| 接口 | 方法 | 说明 |
|------|------|------|
| /admin/validateRuleGroup/create | POST | 新增校验规则组 |
| /admin/validateRuleGroup/update | POST | 更新校验规则组 |
| /admin/validateRuleGroup/delete | POST | 删除校验规则组 |
| /admin/validateRuleGroup/saveGroupOrders | POST | 更新校验规则组顺序 |
| /admin/validateRuleGroup/queryPageList | POST | 分页查询校验规则组 |
| /admin/validateRuleGroup/queryDetail | POST | 根据ID查询校验规则组 |

### 校验场景管理
| 接口 | 方法 | 说明 |
|------|------|------|
| /admin/validateScene/create | POST | 新增校验场景 |
| /admin/validateScene/update | POST | 更新校验场景 |
| /admin/validateScene/delete | POST | 删除校验场景 |
| /admin/validateScene/enable | POST | 启用校验场景 |
| /admin/validateScene/disable | POST | 禁用校验场景 |
| /admin/validateScene/queryPageList | POST | 分页查询校验场景 |
| /admin/validateScene/queryDetail | POST | 根据ID查询校验场景 |

### 校验执行
| 接口 | 方法 | 说明 |
|------|------|------|
| /api/validation/getSceneValidRules | POST | 获取场景校验规则 |
