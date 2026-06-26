# ListGlobalVars - 查询全局变量组列表

查询全局变量组列表。

| 适用版本 | 标准版 |
| --- | --- |

## 服务接入点与授权信息

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。
    
    | **产品** | **资源** | **所需权限** |
    | --- | --- | --- |
    | 应用交付 | 全局变量组 | 只读 |
    

## 请求语法

`POST https://{domain}/oapi/v1/appstack/organizations/{organizationId}/globalVars:search`

## 请求头

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## 请求参数

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| current | long | query | 是 | 当前页码。 | 1 |
| pageSize | long | query | 是 | 每页大小。 | 10 |
| organizationId | string | path | 是 | 组织 ID。 | organization-id-xxx |
| \- | object | body | 否 | 查询全局变量组请求。 |  |
| search | string | body | 否 | 查询关键字。 | search-text |

## 请求示例

`curl -X 'POST' \ 'https://test.rdc.aliyuncs.com/oapi/v1/appstack/organizations/organization-id-xxx/globalVars:search?current=1&pageSize=10' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "search": "search-text" }'`

## 返回参数

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object | 分页数据。 |  |
| current | number | 当前页数。 | 1 |
| pageSize | number | 每页大小。 | 10 |
| pages | number | 总页数。 | 10 |
| records | array | 数据列表。 |  |
| \- | object | 全局变量信息。 |  |
| creatorId | string | 创建人。 | creator-id |
| displayName | string | 全局变量展示名称。 | display-name-xxx |
| gmtCreate | string | 创建时间。 | 2024-09-01 00:00:00 |
| gmtModified | string | 修改时间。 | 2024-09-01 00:00:00 |
| modifierId | string | 修改人。 | modifier-id |
| name | string | 全局变量名称。 | name-xxx |
| ownerId | string | 拥有者 ID。 | owner-id |
| usageReferences | array | 全局变量引用。 |  |
| \- | object | 全局变量引用。 |  |
| globalVarName | string | 全局变量名称。 | global-var-name |
| usageRefObject | object | 全局变量引用对象。 |  |
| usageRefType | string | 全局变量引用类型，可能的值：\[AppEnv AppTemplateWorkflowStage AppWorkflowStage AppTemplateEnv\]。 | AppEnv |
| total | number | 总数。 | 10 |

## 返回示例

`{ "current": 1, "pageSize": 10, "pages": 10, "records": [ { "creatorId": "creator-id", "displayName": "display-name-xxx", "gmtCreate": "2024-09-01 00:00:00", "gmtModified": "2024-09-01 00:00:00", "modifierId": "modifier-id", "name": "name-xxx", "ownerId": "owner-id", "usageReferences": [ { "globalVarName": "global-var-name", "usageRefObject": { }, "usageRefType": "AppEnv" } ] } ], "total": 10 }`

## 错误码

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。