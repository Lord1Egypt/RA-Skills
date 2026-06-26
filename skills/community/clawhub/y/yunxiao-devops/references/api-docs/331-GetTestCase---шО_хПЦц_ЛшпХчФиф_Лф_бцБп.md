# GetTestCase - 获取测试用例信息

通过 OpenAPI 获取测试用例信息。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。
    
    | **产品** | **资源** | **所需权限** |
    | --- | --- | --- |
    | 测试管理 | 测试用例 | 只读 |
    

## **请求语法**

`GET https://{domain}/oapi/v1/testhub/organizations/{organizationId}/testRepos/{testRepoId}/testcases/{id}`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | 是 | organizationId。 |  |
| testRepoId | string | path | 是 | 用例库唯一标识。 |  |
| id | string | path | 是 | 用例唯一标识。 |  |

## **请求示例**

`curl -X 'GET' \ 'https://test.rdc.aliyuncs.com/oapi/v1/testhub/organizations/{organizationId}/testRepos/{testRepoId}/testcases/{id}' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object |  |  |
| assignedTo | object |  |  |
| id | string | 用户 id。 | user-id-xxx |
| name | string | 名称。 | name-xxx |
| creator | object |  |  |
| id | string | 用户 id。 | user-id-xxx |
| name | string | 名称。 | name-xxx |
| customCode | string | 编号。 | DDDD-112 |
| customFieldValues | array | 自定义字段值。 |  |
| \- | object |  |  |
| fieldFormat | string | 字段类型。 | User |
| fieldId | string | 字段 id。 | field-id-xxx |
| fieldName | string | 字段名称。 | field-name-xxx |
| values | array | 字段值。 |  |
| \- | object |  |  |
| displayValue | string | 显示的名称。 |  |
| identifier | string | 值的唯一标识。 |  |
| directory | object |  |  |
| id | string | id。 | id-xxx |
| name | string | 名称。 | test |
| gmtCreate | string | 创建时间。 |  |
| gmtModified | string | 修改时间。 |  |
| id | string | id。 | id-xxx |
| labels | array | 标签。 |  |
| \- | object |  |  |
| color | string | 颜色。 | test |
| id | string | id。 | id-xxx |
| name | string | 名称。 | test |
| modifier | object |  |  |
| id | string | 用户 id。 | user-id-xxx |
| name | string | 名称。 | name-xxx |
| preCondition | string | 前置条件内容。 | test |
| preConditionFormat | string | 前置条件内容格式，可选值为 RICHTEXT 和 TEXT。 | RICHTEXT |
| subject | string | 标题。 | test |
| testRepo | object |  |  |
| id | string | id。 | id-xxx |
| name | string | 名称。 | test |
| testSteps | object |  |  |
| content | array | 当 contentType 为 TABLE 时，该字段描述了测试步骤的内容。 |  |
| \- | object |  |  |
| expected | string | 期望结果。 | 期望结果1 |
| step | string | 测试步骤。 | 测试步骤1 |
| contentType | string | 内容格式，可选值为 TABLE 和 TEXT。 | TEXT |
| expectedResult | string | 当 contentType 为 TEXT 时，该字段描述了期望结果的内容。 | 期望结果1 |
| stepContent | string | 当 contentType 为 TEXT 时，该字段描述了测试步骤的内容。 | 测试步骤1 |

## **返回示例**

`{ "assignedTo": { "id": "user-id-xxx", "name": "name-xxx" }, "creator": { "id": "user-id-xxx", "name": "name-xxx" }, "customCode": "DDDD-112", "customFieldValues": [ { "fieldFormat": "User", "fieldId": "field-id-xxx", "fieldName": "field-name-xxx", "values": [ { "displayValue": "", "identifier": "" } ] } ], "directory": { "id": "id-xxx", "name": "test" }, "gmtCreate": "", "gmtModified": "", "id": "id-xxx", "labels": [ { "color": "test", "id": "id-xxx", "name": "test" } ], "modifier": { "id": "user-id-xxx", "name": "name-xxx" }, "preCondition": "test", "preConditionFormat": "RICHTEXT", "subject": "test", "testRepo": { "id": "id-xxx", "name": "test" }, "testSteps": { "content": [ { "expected": "期望结果1", "step": "测试步骤1" } ], "contentType": "TEXT", "expectedResult": "期望结果1", "stepContent": "测试步骤1" } }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。