# GetWorkitem - 获取工作项

通过 OpenAPI 获取工作项。

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

`GET https://{domain}/oapi/v1/projex/organizations/{organizationId}/workitems/{id}`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| id | string | path | 是 | 工作项唯一标识。 |  |
| organizationId | string | path | 是 | organizationId。 | 5ebbc0228123212b59xxxxx |

## **请求示例**

`curl -X 'GET' \ 'https://test.rdc.aliyuncs.com/oapi/v1/projex/organizations/{organizationId}/workitems/{id}' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object |  |  |
| assignedTo | object |  |  |
| id | string | 用户 id。 | 674d96abd497cd558d68\*\*\*\* |
| name | string | 名称。 | name-xxx |
| categoryId | string | 工作项分类 id。 | Req |
| creator | object |  |  |
| id | string | 用户 id。 | 674d96abd497cd558d68\*\*\*\* |
| name | string | 名称。 | name-xxx |
| customFieldValues | array | 自定义字段值。 |  |
| \- | object |  |  |
| fieldFormat | string | 字段类型。 | User |
| fieldId | string | 字段 id。 | 126553d622cc8521793e08\*\*\*\* |
| fieldName | string | 字段名称。 | field-name-xxx |
| values | array | 字段值。 |  |
| \- | object |  |  |
| displayValue | string | 显示的名称。 |  |
| identifier | string | 值的唯一标识。 |  |
| description | string | 描述。 | test |
| formatType | string | 描述的格式，目前支持 RICHTEXT 和 MARKDOWN。 | RICHTEXT |
| gmtCreate | string | 创建时间。 |  |
| gmtModified | string | 修改时间。 |  |
| id | string | 工作项 id。 | id-2 |
| idPath | string | 工作项 idPath。 | id-1,id-2 |
| labels | array | 标签。 |  |
| \- | object |  |  |
| color | string | 颜色。 | test |
| id | string | id。 | id-xxx |
| name | string | 名称。 | test |
| logicalStatus | string | 逻辑状态, normal 为正常状态， archived 为归档状态。 | normal |
| modifier | object |  |  |
| id | string | 用户 id。 | user-id-xxx |
| name | string | 名称。 | name-xxx |
| parentId | string | 父工作项 id。 | id-1 |
| participants | array | 参与人。 |  |
| \- | object |  |  |
| id | string | 用户 id。 | 674d96abd497cd558d68\*\*\*\* |
| name | string | 名称。 | name-xxx |
| serialNumber | string | 编号。 | DSDD-123 |
| space | object |  |  |
| id | string | id。 | id-xxx |
| name | string | 名称。 | test |
| sprint | object |  |  |
| id | string | id。 | id-xxx |
| name | string | 名称。 | test |
| status | object |  |  |
| displayName | string | 显示名称。 | 待处理 |
| id | string | id。 | id-xxx |
| name | string | 名称。 | 待处理 |
| nameEn | string | 英文名称。 | TODO |
| statusStageId | string | 状态阶段 id。 | id-xxx |
| subject | string | 标题。 | test |
| trackers | array | 跟踪人。 |  |
| \- | object |  |  |
| id | string | 用户 id。 | 674d96abd497cd558d68\*\*\*\* |
| name | string | 名称。 | name-xxx |
| updateStatusAt | string | 状态更新时间。 |  |
| verifier | object |  |  |
| id | string | 用户 id。 | 674d96abd497cd558d68\*\*\*\* |
| name | string | 名称。 | name-xxx |
| versions | array | 版本。 |  |
| \- | object |  |  |
| id | string | id。 | id-xxx |
| name | string | 名称。 | test |
| workitemType | object |  |  |
| id | string | id。 | id-xxx |
| name | string | 名称。 | test |

## **返回示例**

`{ "assignedTo": { "id": "674d96abd497cd558d68****", "name": "name-xxx" }, "categoryId": "Req", "creator": { "id": "674d96abd497cd558d68****", "name": "name-xxx" }, "customFieldValues": [ { "fieldFormat": "User", "fieldId": "674d96abd497cd558d68****", "fieldName": "field-name-xxx", "values": [ { "displayValue": "", "identifier": "" } ] } ], "description": "test", "formatType": "RICHTEXT", "gmtCreate": "", "gmtModified": "", "id": "id-2", "idPath": "id-1,id-2", "labels": [ { "color": "test", "id": "id-xxx", "name": "test" } ], "logicalStatus": "normal", "modifier": { "id": "674d96abd497cd558d68****", "name": "name-xxx" }, "parentId": "id-1", "participants": [ { "id": "674d96abd497cd558d68****", "name": "name-xxx" } ], "serialNumber": "DSDD-123", "space": { "id": "id-xxx", "name": "test" }, "sprint": { "id": "id-xxx", "name": "test" }, "status": { "displayName": "待处理", "id": "id-xxx", "name": "待处理", "nameEn": "TODO" }, "statusStageId": "id-xxx", "subject": "test", "trackers": [ { "id": "674d96abd497cd558d68****", "name": "name-xxx" } ], "updateStatusAt": "", "verifier": { "id": "674d96abd497cd558d68****", "name": "name-xxx" }, "versions": [ { "id": "id-xxx", "name": "test" } ], "workitemType": { "id": "id-xxx", "name": "test" } }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。