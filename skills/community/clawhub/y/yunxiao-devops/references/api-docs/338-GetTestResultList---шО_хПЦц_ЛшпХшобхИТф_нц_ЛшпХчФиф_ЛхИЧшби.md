# GetTestResultList - 获取测试计划中测试用例列表

通过 OpenAPI 获取测试计划中测试用例列表。

| 适用版本 | 企业标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)，替换 API 请求语法中的 <domain>
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)
-   获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 测试管理 | 测试计划 | 只读 |

## **请求语法**

`POST https://{domain}/oapi/v1/testhub/organizations/{organizationId}/{testPlanIdentifier}/result/list/{directoryIdentifier}`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** |
| --- | --- | --- | --- | --- |
| organizationId | string | path | 是 | 组织 id |
| testPlanIdentifier | string | path | 是 | 测试计划 id |
| directoryIdentifier | string | path | 是 | 目录 id |

## **请求示例**

`curl -X 'POST' \ 'https://{domain}/oapi/v1/testhub/organizations/{organizationId}/{testPlanIdentifier}/result/list/{directoryIdentifier}' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | array |  |  |
| \- | object |  |  |
| assignedTo | object |  |  |
| id | string | 用户 id | user-id-xxx |
| name | string | 名称 | name-xxx |
| bugCount | integer | 测试执行结果关联缺陷数量 |  |
| customFields | object |  |  |
| fieldClassName | string | 字段类型 | int |
| fieldFormat | string | 字段格式 | input |
| fieldIdentifier | string | 字段 id | 943d20fe5e385a08fdd6b593fb |
| value | string | 字段值 |  |
| gmtCreate | string | 测试用例创建时间 |  |
| identifier | string | 测试用例 id，测试用例唯一标识 |  |
| spaceIdentifier | string | 测试用例所属的测试库 id |  |
| subject | string | 测试用例标题 |  |
| testResultExecutor | object |  |  |
| id | string | 用户 id | user-id-xxx |
| name | string | 名称 | name-xxx |
| testResultExecutorIdentifier | string | 测试计划执行人 id |  |
| testResultGmtCreate | string | 测试结果创建时间 |  |
| testResultGmtModified | string | 测试结果最后修改时间 |  |
| testResultIdentifier | string | 测试结果的 id |  |
| testResultStatus | string | 测试结果的状态，可选值为：  -   TODO：待测试 -   PASS：已通过 -   FAILURE：未通过 -   POSTPONE：暂缓 |  |

## **返回示例**

`[ { "assignedTo": { "id": "user-id-xxx", "name": "name-xxx" }, "bugCount": 0, "customFields": { "fieldClassName": "int", "fieldFormat": "input", "fieldIdentifier": "943d20fe5e385a08fdd6b593fb", "value": "" }, "gmtCreate": "", "identifier": "", "spaceIdentifier": "", "subject": "", "testResultExecutor": { "id": "user-id-xxx", "name": "name-xxx" }, "testResultExecutorIdentifier": "", "testResultGmtCreate": "", "testResultGmtModified": "", "testResultIdentifier": "", "testResultStatus": "" } ]`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。