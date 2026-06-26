# SearchTestCases - 搜索测试用例

通过 OpenAPI 搜索测试用例。

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

`POST https://{domain}/oapi/v1/testhub/organizations/{organizationId}/testRepos/{id}/testcases:search`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| id | string | path | 是 | 用例库唯一标识。 |  |
| organizationId | string | path | 是 | organizationId。 |  |
| \- | object | body | 否 |  |  |
| conditions | string | body | 否 | 过滤条件， 是一个 json 串，格式为{“conditionGroups”:\[\[filterObject,filterObject,…\]\]}， 每个字段如何拼接可参考测试用例列表页面过滤时请求的/testCase/listByDirectory 接口，以下为一个完整的搜索条件（真实场景中可以按需选取对应的值）{“conditionGroups”:\[\[{“fieldIdentifier”:“subject”,“operator”:“CONTAINS”,“value”:\[“ceshi”\],“toValue”:null,“className”:“string”,“format”:“input”}\]\]}。 | {“conditionGroups”:\[\[{“fieldIdentifier”:“subject”,“operator”:“CONTAINS”,“value”:\[“ceshi”\],“toValue”:null,“className”:“string”,“format”:“input”}\]\]} |
| directoryId | string | body | 否 | 目录 id | id-xxx |
| orderBy | string | body | 否 | 排序字段：  -   gmtCreate（默认）：创建时间 -   name：名称 | gmtCreate |
| page | integer | body | 否 | 分页参数，第几页。 | 1 |
| perPage | integer | body | 否 | 分页参数，每页大小，0-200，默认值20。 | 20 |
| sort | string | body | 否 | 排序方式：  -   desc（默认）：降序 -   asc：升序 | desc |

## **请求示例**

`curl -X 'POST' \ 'https://test.rdc.aliyuncs.com/oapi/v1/testhub/organizations/{organizationId}/testRepos/{id}/testcases:search' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "conditions": "{"conditionGroups":[[{"fieldIdentifier":"subject","operator":"CONTAINS","value":["ceshi"],"toValue":null,"className":"string","format":"input"}]]}", "directoryId": "", "orderBy": "gmtCreate", "page": 1, "perPage": 20, "sort": "desc" }'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | array |  |  |
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

`[ { "assignedTo": { "id": "user-id-xxx", "name": "name-xxx" }, "creator": { "id": "user-id-xxx", "name": "name-xxx" }, "customCode": "DDDD-112", "customFieldValues": [ { "fieldFormat": "User", "fieldId": "field-id-xxx", "fieldName": "field-name-xxx", "values": [ { "displayValue": "", "identifier": "" } ] } ], "directory": { "id": "id-xxx", "name": "test" }, "gmtCreate": "", "gmtModified": "", "id": "id-xxx", "labels": [ { "color": "test", "id": "id-xxx", "name": "test" } ], "modifier": { "id": "user-id-xxx", "name": "name-xxx" }, "preCondition": "test", "preConditionFormat": "RICHTEXT", "subject": "test", "testRepo": { "id": "id-xxx", "name": "test" }, "testSteps": { "content": [ { "expected": "期望结果1", "step": "测试步骤1" } ], "contentType": "TEXT", "expectedResult": "期望结果1", "stepContent": "测试步骤1" } } ]`

## **响应头**

| **参数** | **描述** | **示例值** |
| --- | --- | --- |
| x-next-page | 下一页。 |  |
| x-page | 当前页。 |  |
| x-per-page | 每页数据条数。 |  |
| x-prev-page | 上一页。 |  |
| x-total | 总数据量。 |  |
| x-total-pages | 总分页数。 |  |

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。