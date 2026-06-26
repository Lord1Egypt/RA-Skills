# ListEnvironments - 分页查找环境详情列表

通过 OpenAPI 页查找环境详情列表。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。
    
    | **产品** | **资源** | **所需权限** |
    | --- | --- | --- |
    | 应用交付 | 环境 | 只读 |
    

## **请求语法**

`GET https://{domain}/oapi/v1/appstack/organizations/{organizationId}/apps/{appName}/envs`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| appName | string | path | 是 | 应用名。 | my-web-service |
| pagination | string | query | 是 | 分页模式参数，目前只支持键集分页 keyset 模式。 | keyset |
| perPage | number | query | 否 | 分页尺寸参数，决定一页最多返回多少对象。 | 20 |
| orderBy | string | query | 是 | 分页排序属性，决定根据何种属性进行记录排序；推荐在实现严格遍历时，使用 id 属性。 | id |
| sort | string | query | 是 | 分页排序升降序，asc 为升序，desc 为降序；推荐在实现严格遍历时，使用升序。 | desc |
| nextToken | string | query | 否 | 键集分页 token，获取第一页数据时无需传入，否则需要传入前一页查询结果中的 nextToken 字段。 | token |
| page | number | query | 否 | 页码分页时使用，用于获取下一页内容。 | 1 |
| organizationId | string | path | 是 | 组织 ID。 | 99d1\*\*\*\*71d4 |

## **请求示例**

`curl -X 'GET' \ 'https://test.rdc.aliyuncs.com/oapi/v1/appstack/organizations/organization-id-xxx/apps/my-web-service/envs?pagination=keyset&perPage=20&orderBy=id&sort=desc&nextToken=token&page=1' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object | 分页接口所返回的列表。 |  |
| current | number | 页码分页时存在该字段，表示当前页。 | 1 |
| data | array | 分页结果数据。 |  |
| \- | object | AppStack 环境模型。 |  |
| appName | string | 环境所隶属的应用唯一名。 | my-web-service |
| creatorId | string | 环境创建者的用户 ID。 | bd9e3c6d-624f-4580-af7d-c5e26f1ed0f0 |
| deployGroupName | string | 部署组唯一名。 | k8s-dev |
| description | string | 环境描述。 | 这是一套用于展示的开发环境 |
| descriptiveName | string | 环境的展示名。 | 测试环境 |
| gmtCreate | string | 环境创建时间。 | 2024-09-01 00:00:00 |
| labelList | array | 标签列表。 |  |
| \- | object | AppStack 标签。 |  |
| displayName | string | 标签的展示名，用于描述性的场景，不参与标签匹配。 | 测试标签键 |
| displayValue | string | 标签的展示值，用于描述性的场景，不参与标签匹配。 | 测试标签值 |
| extraMap | object | 标签扩展属性 map，可在定义标签时用于存储自定义的扩展属性字段。 | map\[\] |
| name | string | 标签名，仅允许包含小写字母、中划线和数字，且开头、结尾均为小写字母或数字。 | demo-label |
| namespace | string | 标签命名空间，决定了标签的作用域。 | default |
| value | string | 标签值，仅允许包含小写字母、中划线和数字，且开头、结尾均为小写字母或数字。 | demo-label-value |
| lockBy | string | 当前正锁定环境的用户 ID。 | bd9e3c6d-624f-4580-af7d-c5e26f1ed0f0 |
| name | string | 环境的唯一名，仅允许包含小写字母、中划线和数字，且开头、结尾均为小写字母或数字。 | dev |
| replicasManagement | string | 副本托管模式。 | USER |
| resourcePoolName | string | 资源池唯一名。 | default |
| rolloutStrategies | array | 部署策略。 |  |
| \- | object | 部署策略。 |  |
| batchMode | string | 分批模式，可能的值：\[ConfirmFirstBatch Auto Manual\]。 | ConfirmFirstBatch |
| batchSteps | array | 分批详情列表。 |  |
| \- | object | 分批详情。 |  |
| type | string | 分批类型，可能的值：\[WEIGHT REPLICAS\]。 | WEIGHT |
| value | string | 分批值。 | 90 |
| batches | string | 分批数。 | 2 |
| deployType | string | 部署类型，可能的值：\[Rolling Batch Recreate\]。 | Batch |
| locator | string | 部署资源坐标。 | aaa.bbb.ccc |
| targetReplicas | number | 目标复本数量。 | 3 |
| timeOutMS | number | 超时时间。 | 60000 |
| state | string | 环境状态，可能的值：\[NEW DEPLOYING RUNNING ERROR\]。 | my-web-service |
| variableGroupName | string | 变量组唯一名。 | dev |
| variableGroups | array | 变量组。 |  |
| \- | object | 通用变量组模型。 |  |
| displayName | string | 变量组显示名。 | 开发变量组 |
| name | string | 变量组标识。 | dev |
| type | string | 变量组类型。 | GLOBAL |
| nextToken | string | 采用键值分页时存在该字段，用于传给分页接口，迭代获取下一页数据。 | token |
| pages | number | 页码分页时存在该字段，表示总页数。 | 10 |
| perPage | number | 页码分页时存在该字段，表示每页大小。 | 10 |
| total | number | 页码分页时存在该字段，表示结果总数。 | 100 |

## **返回示例**

`{ "current": 1, "data": [ { "appName": "my-web-service", "creatorId": "bd9e3c6d-624f-4580-af7d-c5e26f1ed0f0", "deployGroupName": "k8s-dev", "description": "这是一套用于展示的开发环境", "descriptiveName": "测试环境", "gmtCreate": "2024-09-01 00:00:00", "labelList": [ { "displayName": "测试标签键", "displayValue": "测试标签值", "extraMap": { }, "name": "demo-label", "namespace": "default", "value": "demo-label-value" } ], "lockBy": "bd9e3c6d-624f-4580-af7d-c5e26f1ed0f0", "name": "dev", "replicasManagement": "USER", "resourcePoolName": "default", "rolloutStrategies": [ { "batchMode": "ConfirmFirstBatch", "batchSteps": [ { "type": "WEIGHT", "value": "90" } ], "batches": "2", "deployType": "Batch", "locator": "aaa.bbb.ccc", "targetReplicas": 3, "timeOutMS": 60000 } ], "state": "my-web-service", "variableGroupName": "dev", "variableGroups": [ { "displayName": "开发变量组", "name": "dev", "type": "GLOBAL" } ] } ], "nextToken": "token", "pages": 10, "perPage": 10, "total": 100 }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。