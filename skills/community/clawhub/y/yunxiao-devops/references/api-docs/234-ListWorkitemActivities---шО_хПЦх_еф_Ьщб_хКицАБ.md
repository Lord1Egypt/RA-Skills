# ListWorkitemActivities - 获取工作项动态

通过 OpenAPI 获取工作项动态。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。
    
    | **产品** | **资源** | **所需权限** |
    | --- | --- | --- |
    | 项目协作 | 工作项 | 只读 |
    

## **请求语法**

`GET https://{domain}/oapi/v1/projex/organizations/{organizationId}/workitems/{id}/activities`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| id | string | path | 是 | 工作项唯一标识。 |  |
| organizationId | string | path | 是 | organizationId。 | 5ebbc0228123212b59xxxxx |

## **请求示例**

`curl -X 'GET' \ 'https://test.rdc.aliyuncs.com/oapi/v1/projex/organizations/{organizationId}/workitems/{id}/activities' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | array |  |  |
| \- | object |  |  |
| actionType | string | action 类型，可选值为: created, updated, delete, associate, unassociate 分别对应: 创建，更新，删除，关联和解除关联的 action。 |  |
| eventId | integer | 事件 id。 |  |
| eventTime | string | 事件发生时间。 |  |
| eventType | string | 事件类型，可选值为: workitem.created, workitem.updated, workitem.transitioned, workitem.association.changed， workitem.attachment.changed 分别对应工作项创建，工作项更新，工作项状态流转，工作项附件变更，工作项关联项变更。 |  |
| newValue | array | 更新后的值，可以为空。 |  |
| \- | object |  |  |
| displayValue | string | 显示的名称。 |  |
| identifier | string | 值的唯一标识。 |  |
| oldValue | array | 更新前的值，可以为空。 |  |
| \- | object |  |  |
| displayValue | string | 显示的名称。 |  |
| identifier | string | 值的唯一标识。 |  |
| operator | object |  |  |
| id | string | 用户 id。 | 674d96abd497cd558d68\*\*\*\* |
| name | string | 名称。 | name-xxx |
| parentEventId | integer | parentEventId。 |  |
| property | object |  |  |
| propertyId | string | 属性 id。 |  |
| propertyName | string | 属性名称。 |  |
| propertyType | string | 属性类型, 可选值为 Field，Relation 或是 null。 |  |
| relatedResource | object |  |  |
| resourceId | string | 资源 id，如果是工作项则是对应的工作项 id。 |  |
| resourceType | string | 资源对象，如果是工作项则是 Workitem。 |  |
| resourceId | string | 事件发生的资源对象 id，工作项则是对应的工作项 id。 |  |

## **返回示例**

`[ { "actionType": "", "eventId": 0, "eventTime": "", "eventType": "", "newValue": [ { "displayValue": "", "identifier": "" } ], "oldValue": [ { "displayValue": "", "identifier": "" } ], "operator": { "id": "674d96abd497cd558d68****", "name": "name-xxx" }, "parentEventId": 0, "property": { "propertyId": "", "propertyName": "", "propertyType": "" }, "relatedResource": { "resourceId": "", "resourceType": "" }, "resourceId": "" } ]`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。