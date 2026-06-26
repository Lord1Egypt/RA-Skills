# CreateTestCase - 创建测试用例

通过 OpenAPI 创建测试用例。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。
    
    | **产品** | **资源** | **所需权限** |
    | --- | --- | --- |
    | 测试管理 | 测试用例 | 读写 |
    

## **请求语法**

`POST https://{domain}/oapi/v1/testhub/organizations/{organizationId}/testRepos/{id}/testcases`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| id | string | path | 是 | 用例库唯一标识。 |  |
| organizationId | string | path | 是 | organizationId。 | 5ebbc0228123212b59xxxxx |
| \- | object | body | 否 |  |  |
| assignedTo | string | body | 否 | 负责人。 |  |
| customFieldValues | object | body | 否 | 自定义字段值，字段 key 可通过"获取获取测试用例字段配置接口"获得。 |  |
| directoryId | string | body | 否 | 目录 id。 |  |
| labels | array\[string\] | body | 否 | 标签 ids。 |  |
| preCondition | string | body | 否 | 前置条件。 |  |
| subject | string | body | 否 | 标题。 |  |
| testSteps | object | body | 否 |  |  |
| content | array | body | 否 | 当 contentType 为 TABLE 时，该字段描述了测试步骤的内容。 |  |
| \- | object | body | 否 |  |  |
| expected | string | body | 否 | 期望结果。 | 期望结果1 |
| step | string | body | 否 | 测试步骤。 | 测试步骤1 |
| contentType | string | body | 否 | 内容格式，可选值为 TABLE 和 TEXT。 | TEXT |
| expectedResult | string | body | 否 | 当 contentType 为 TEXT 时，该字段描述了期望结果的内容。 | 期望结果1 |
| stepContent | string | body | 否 | 当 contentType 为 TEXT 时，该字段描述了测试步骤的内容。 | 测试步骤1 |

## **请求示例**

`curl -X 'POST' \ 'https://test.rdc.aliyuncs.com/oapi/v1/testhub/organizations/{organizationId}/testRepos/{id}/testcases' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "assignedTo": "", "customFieldValues": { }, "directoryId": "", "labels": [ ], "preCondition": "", "subject": "", "testSteps": { "content": [ { "expected": "期望结果1", "step": "测试步骤1" } ], "contentType": "TEXT", "expectedResult": "期望结果1", "stepContent": "测试步骤1" } }'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object |  |  |
| id | string | id。 | id-xxx |

## **返回示例**

`{ "id": "id-xxx" }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。