# ListAllReleaseStageBriefs - 查找研发流程下所有研发阶段摘要

通过 OpenAPI 查找研发流程下所有研发阶段摘要。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。
    
    | **产品** | **资源** | **所需权限** |
    | --- | --- | --- |
    | 应用交付 | 研发阶段 | 只读 |
    

## **请求语法**

`GET https://{domain}/oapi/v1/appstack/organizations/{organizationId}/apps/{appName}/releaseWorkflow/{releaseWorkflowSn}/releaseStageBriefs`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| appName | string | path | 是 | 应用名。 | my-app |
| releaseWorkflowSn | string | path | 是 | 研发流程唯一标识符。 | 3f472a12b15d4f418ad6227bb85f787c |
| organizationId | string | path | 是 | 组织 ID。 | ec766e63aee3437d9a51f334d6exe671 |

## **请求示例**

`curl -X 'GET' \ 'https://test.rdc.aliyuncs.com/oapi/v1/appstack/organizations/ec766e63aee3437d9a51f334d6exe671/apps/my-app/releaseWorkflow/3f472a12b15d4f418ad6227bb85f787c/releaseStageBriefs' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | array |  |  |
| \- | object |  |  |
| appName | string | 应用名。 | my-web-app |
| labels | array |  |  |
| \- | object | AppStack 标签。 |  |
| displayName | string | 标签的展示名，用于描述性的场景，不参与标签匹配。 | 测试标签键 |
| displayValue | string | 标签的展示值，用于描述性的场景，不参与标签匹配。 | 测试标签值 |
| extraMap | object | 标签扩展属性 map，可在定义标签时用于存储自定义的扩展属性字段。 | map\[\] |
| name | string | 标签名，仅允许包含小写字母、中划线和数字，且开头、结尾均为小写字母或数字。 | demo-label |
| namespace | string | 标签命名空间，决定了标签的作用域。 | default |
| value | string | 标签值，仅允许包含小写字母、中划线和数字，且开头、结尾均为小写字母或数字。 | demo-label-value |
| name | string | 名称。 | my-stage |
| order | string | 阶段顺序。 | 1 |
| processEngineSn | string | Flow pipeline id。 | 736548 |
| processEngineType | string | 可能的值：\[FlowV1 FlowV2 FlowAny\]。 | FlowV1 |
| releaseWorkflowSn | string | 所属的流程 sn。 | 1484e1facb5a4febbe1652607b2eb345 |
| sn | string | 唯一序列号。 | sn-xxxx |

## **返回示例**

`[ { "appName": "my-web-app", "labels": [ { "displayName": "测试标签键", "displayValue": "测试标签值", "extraMap": { }, "name": "demo-label", "namespace": "default", "value": "demo-label-value" } ], "name": "my-stage", "order": "1", "processEngineSn": "736548", "processEngineType": "FlowV1", "releaseWorkflowSn": "1484e1facb5a4febbe1652607b2eb345", "sn": "sn-xxxx" } ]`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。