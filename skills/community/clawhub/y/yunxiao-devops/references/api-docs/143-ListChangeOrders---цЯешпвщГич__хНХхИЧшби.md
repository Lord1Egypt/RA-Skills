# ListChangeOrders - 查询部署单列表

| **适用版本** | **企业标准版** |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/lingma/developer-reference/obtain-personal-access-token-1)。
-   获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 应用交付 | 部署单 | 只读 |

## **请求语法**

`POST https://{domain}/oapi/v1/appstack/organizations/{organizationId}/apps/{appName}/changeOrders/api`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| appName | string | path | 是 | 应用名。 | my-web-service |
| organizationId | string | path | 是 | 组织 ID。 | ec766e63aee3437d9a51f334d6exe671 |
| current | integer | query | 是 | 当前页号（从 1 开始，必须大于 0）。 | 1 |
| pageSize | integer | query | 是 | 分页记录数（最大 30 条）。 | 10 |
| \- | object | body | 否 | 查询部署单列表请求。 |  |
| creators | array\[string\] | body | 否 | 创建人 ID 列表。 | \[“666a5701100033a2c8e6ced5”, “5e9ee108424a50d98c7c8906”\] |
| states | array\[string\] | body | 否 | 部署单状态列表。 | \[“INIT”, “RUNNING”, “SUCCESS”, “FAILED”\] |
| types | array\[string\] | body | 否 | 部署单类型列表。 | \[“Deploy”, “Rollback”, “Scale”, “Destroy”\] |

## **请求示例**

`curl -X 'POST' \ 'https://{domain}/oapi/v1/appstack/organizations/ec766e63aee3437d9a51f334d6exe671/apps/my-web-service/changeOrders/api?current=1&pageSize=10' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "creators": ["666a5701100033a2c8e6ced5", "5e9ee108424a50d98c7c8906"], "states": ["INIT", "RUNNING", "SUCCESS", "FAILED"], "types": ["Deploy", "Rollback", "Scale", "Destroy"] }'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object | 分页部署单记录。 |  |
| current | integer | 当前页数。 |  |
| pageSize | integer | 每页大小。 |  |
| pages | integer | 总页数。 |  |
| records | array | 数据列表。 |  |
| \- | object | 部署单记录。 |  |
| appName | string | 应用名。 |  |
| appOrchestrationRevision | object | 应用编排版本信息。 |  |
| author | string | 作者。 |  |
| commitTime | string | 提交时间。 |  |
| message | string | 提交信息。 |  |
| sha | string | SHA 值。 |  |
| artifacts | object | 制品信息。 |  |
| changeOrderName | string | 部署单名称。 |  |
| changeOrderSn | string | 部署单编号。 |  |
| changeOrderVersion | string | 部署单版本。 |  |
| creator | string | 创建人。 |  |
| envDisplayName | string | 环境显示名。 |  |
| envName | string | 环境名。 |  |
| gmtCreate | string | 创建时间。 |  |
| name | string | 名称。 |  |
| profiles | array | 环境变量组列表。 |  |
| \- | object | 环境变量组。 |  |
| displayName | string | 显示名称。 |  |
| name | string | 名称。 |  |
| type | string | 类型。 |  |
| sn | string | 作业单号。 |  |
| snapshot | object | 快照信息。 |  |
| deployGroup | object | 部署组。 |  |
| appSelector | string | 应用选择器。 |  |
| claimList | array | 声明列表。 |  |
| \- | object | 声明。 |  |
| instanceName | string | 实例名称。 |  |
| itemSnList | array\[string\] | 项目编号列表。 |  |
| refId | string | 引用 ID。 |  |
| refType | string | 引用类型。 |  |
| sn | string | 编号。 |  |
| specMap | object | 规格映射。 |  |
| type | string | 类型。 |  |
| creator | string | 创建人。 |  |
| description | string | 描述。 |  |
| displayName | string | 显示名称。 |  |
| name | string | 名称。 |  |
| poolName | string | 资源池名称。 |  |
| source | string | 来源。 |  |
| state | string | 状态，可能的值：\[INIT PREPARING RUNNING SUSPENDED CANCELED SUCCESS FAILED\]。 | INIT |
| type | string | 类型，可能的值：\[Deploy Scale Rollback Destroy\]。 | Deploy |
| total | integer | 总数。 |  |

## **返回示例**

`{ "current": 0, "pageSize": 0, "pages": 0, "records": [ { "appName": "", "appOrchestrationRevision": { "author": "", "commitTime": "", "message": "", "sha": "" }, "artifacts": { }, "changeOrderName": "", "changeOrderSn": "", "changeOrderVersion": "", "creator": "", "envDisplayName": "", "envName": "", "gmtCreate": "", "name": "", "profiles": [ { "displayName": "", "name": "", "type": "" } ], "sn": "", "snapshot": { "deployGroup": { "appSelector": "", "claimList": [ { "instanceName": "", "itemSnList": [ ], "refId": "", "refType": "", "sn": "", "specMap": { }, "type": "" } ], "creator": "", "description": "", "displayName": "", "name": "", "poolName": "" } }, "source": "", "state": "INIT", "type": "Deploy" } ], "total": 0 }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。