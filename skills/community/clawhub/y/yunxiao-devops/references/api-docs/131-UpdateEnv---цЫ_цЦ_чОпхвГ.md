# UpdateEnv - 更新环境

通过 OpenAPI更新环境。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。
    
    | **产品** | **资源** | **所需权限** |
    | --- | --- | --- |
    | 代码管理 | 分支 | 读写 |
    

## **请求语法**

`PUT https://{domain}/oapi/v1/appstack/organizations/{organizationId}/apps/{appName}/envs/{envName}`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| appName | string | path | 是 | 应用名。 | my-web-service |
| envName | string | path | 是 | 环境名。 | dev |
| organizationId | string | path | 是 | 组织 ID。 | 99d1\*\*\*\*71d4 |
| \- | object | body | 否 | 更新环境请求。 |  |
| deployGroupName | string | body | 否 | 部署组名称。 | deploy-group-name |
| description | string | body | 否 | 环境描述。 | description |
| displayName | string | body | 否 | 环境显示名称。 | display-name |
| labelList | array | body | 否 | 标签列表。 |  |
| \- | object | body | 否 | AppStack 标签。 |  |
| displayName | string | body | 否 | 标签的展示名，用于描述性的场景，不参与标签匹配。 | 测试标签键 |
| displayValue | string | body | 否 | 标签的展示值，用于描述性的场景，不参与标签匹配。 | 测试标签值 |
| extraMap | object | body | 否 | 标签扩展属性 map，可在定义标签时用于存储自定义的扩展属性字段。 | map\[\] |
| name | string | body | 否 | 标签名，仅允许包含小写字母、中划线和数字，且开头、结尾均为小写字母或数字。 | demo-label |
| namespace | string | body | 否 | 标签命名空间，决定了标签的作用域。 | default |
| value | string | body | 否 | 标签值，仅允许包含小写字母、中划线和数字，且开头、结尾均为小写字母或数字。 | demo-label-value |
| orchestrationName | string | body | 否 | 环境编排名称。 | orchestration-name |
| profiles | array | body | 否 | 变量组列表。 |  |
| \- | object | body | 否 | 通用变量组模型。 |  |
| displayName | string | body | 否 | 变量组显示名。 | 开发变量组 |
| name | string | body | 否 | 变量组标识。 | dev |
| type | string | body | 否 | 变量组类型。 | GLOBAL |
| replicasManagement | string | body | 否 | 复本数管控模式，可能的值：\[SYSTEM USER\]。 | SYSTEM |
| resourceType | string | body | 是 | 资源类型，可能的值：\[KUBERNETES HOST BePending\]。 | KUBERNETES |
| rolloutStrategies | array | body | 否 | 部署策略列表。 |  |
| \- | object | body | 否 | 部署策略。 |  |
| batchMode | string | body | 否 | 分批模式，可能的值：\[ConfirmFirstBatch Auto Manual\]。 | ConfirmFirstBatch |
| batchSteps | array | body | 否 | 分批详情列表。 |  |
| \- | object | body | 否 | 分批详情。 |  |
| type | string | body | 是 | 分批类型，可能的值：\[WEIGHT REPLICAS\]。 | WEIGHT |
| value | string | body | 是 | 分批值。 | 90 |
| batches | string | body | 否 | 分批数。 | 2 |
| deployType | string | body | 否 | 部署类型，可能的值：\[Rolling Batch Recreate\]。 | Batch |
| locator | string | body | 是 | 部署资源坐标。 | aaa.bbb.ccc |
| targetReplicas | number | body | 否 | 目标复本数量。 | 3 |
| timeOutMS | number | body | 否 | 超时时间。 | 60000 |
| status | string | body | 否 | 状态。 | SUCCESS |

## **请求示例**

`curl -X 'PUT' \ 'https://test.rdc.aliyuncs.com/oapi/v1/appstack/organizations/organization-id-xxx/apps/my-web-service/envs/dev' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "deployGroupName": "deploy-group-name", "description": "description", "displayName": "display-name", "labelList": [ { "displayName": "测试标签键", "displayValue": "测试标签值", "extraMap": { }, "name": "demo-label", "namespace": "default", "value": "demo-label-value" } ], "orchestrationName": "orchestration-name", "profiles": [ { "displayName": "开发变量组", "name": "dev", "type": "GLOBAL" } ], "replicasManagement": "SYSTEM", "resourceType": "KUBERNETES", "rolloutStrategies": [ { "batchMode": "ConfirmFirstBatch", "batchSteps": [ { "type": "WEIGHT", "value": "90" } ], "batches": "2", "deployType": "Batch", "locator": "aaa.bbb.ccc", "targetReplicas": 3, "timeOutMS": 60000 } ], "status": "SUCCESS" }'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
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

## **返回示例**

`{ "appName": "my-web-service", "creatorId": "bd9e3c6d-624f-4580-af7d-c5e26f1ed0f0", "deployGroupName": "k8s-dev", "description": "这是一套用于展示的开发环境", "descriptiveName": "测试环境", "gmtCreate": "2024-09-01 00:00:00", "labelList": [ { "displayName": "测试标签键", "displayValue": "测试标签值", "extraMap": { }, "name": "demo-label", "namespace": "default", "value": "demo-label-value" } ], "lockBy": "bd9e3c6d-624f-4580-af7d-c5e26f1ed0f0", "name": "dev", "replicasManagement": "USER", "resourcePoolName": "default", "rolloutStrategies": [ { "batchMode": "ConfirmFirstBatch", "batchSteps": [ { "type": "WEIGHT", "value": "90" } ], "batches": "2", "deployType": "Batch", "locator": "aaa.bbb.ccc", "targetReplicas": 3, "timeOutMS": 60000 } ], "state": "my-web-service", "variableGroupName": "dev", "variableGroups": [ { "displayName": "开发变量组", "name": "dev", "type": "GLOBAL" } ] }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。