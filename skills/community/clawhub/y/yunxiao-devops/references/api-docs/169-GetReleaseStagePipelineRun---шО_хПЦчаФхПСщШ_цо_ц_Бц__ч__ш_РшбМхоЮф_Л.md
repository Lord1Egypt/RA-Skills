# GetReleaseStagePipelineRun - 获取研发阶段流水线运行实例

获取研发阶段流水线运行实例。

| 适用版本 | 标准版 |
| --- | --- |

## 服务接入点与授权信息

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。
    
    | **产品** | **资源** | **所需权限** |
    | --- | --- | --- |
    | 应用交付 | 发布阶段 | 只读 |
    

## 请求语法

`GET https://{domain}/oapi/v1/appstack/organizations/{organizationId}/apps/{appName}/releaseWorkflows/{releaseWorkflowSn}/releaseStages/{releaseStageSn}/executions/{executionNumber}:getPipelineRun`

## 请求头

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## 请求参数

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| appName | string | path | 是 | 应用名。 | my-web-service |
| releaseWorkflowSn | string | path | 是 | 发布流程唯一序列号。 | 3f472a12b15d4f418ad6227bb85f787c |
| releaseStageSn | string | path | 是 | 发布流程阶段唯一序列号。 | 6b4c53eee9a842c6a11235b29d002a81 |
| executionNumber | string | path | 是 | 流水线运行 ID，对应 ExecuteChangeRequestReleaseStage 返回中的 pipelineRunId。 | 123456 |
| organizationId | string | path | 是 | 组织 ID。 | ec766e63aee3437d9a51f334d6exe671 |

## 请求示例

`curl -X 'GET' \ 'https://test.rdc.aliyuncs.com/oapi/v1/appstack/organizations/ec766e63aee3437d9a51f334d6exe671/apps/my-web-service/releaseWorkflows/3f472a12b15d4f418ad6227bb85f787c/releaseStages/6b4c53eee9a842c6a11235b29d002a81/executions/123:getPipelineRun' \ -H 'accept: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## 返回参数

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object | 获取流水线运行实例结果。 |  |
| pipelineRun | object | 获取流水线运行实例信息。 |  |
| createTime | string | 创建时间。 | 2024-01-01 00:00:00 |
| creatorAccountId | string | 创建人账号。 | creator-account-id |
| modifierAccountId | string | 修改人账号。 | modifier-account-id |
| creator | string | 创建人云效账号 ID。 | 61c92a37ae805dbacc5b9f78 |
| modifier | string | 修改人云效账号 ID。 | 61c92a37ae805dbacc5b9f78 |
| pipelineId | string | 流水线 ID。 | 123 |
| pipelineRunId | string | 流水线运行 ID。 | 123456 |
| sources | array | 输入源信息。 |  |
| \- | object | 输入源。 |  |
| data | object | 输入源详细数据。 |  |
| branch | string | 分支。 | master |
| commit | string | 提交信息。 | commit |
| repo | string | 所属仓库。 | https://codeup.aliyun.com… |
| sign | string | 标识。 | sign |
| type | string | 类型。 | type |
| stageTopo | array | 流水线阶段串并行顺序分组（同一个 group 内的stage 并行，group 之间串行）。 |  |
| \- | array\[string\] | 阶段分组。 |  |
| stages | array | 阶段列表。 |  |
| \- | object | 阶段。 |  |
| index | string | stage对应stageTopo中的元素（用于识别stage串并行顺序）。 | Group0-Stage0 |
| name | string | 名称。 | stage-name |
| stageInfo | object | 阶段信息。 |  |
| endTime | number | 结束时间。 | 123 |
| jobs | array | 任务列表。 |  |
| \- | object | 任务。 |  |
| actions | array | 操作列表。 |  |
| \- | object | 操作。 |  |
| disable | boolean | 是否禁用。 | true |
| params | string | 其他参数。 | {} |
| type | string | 类型。 | type |
| endTime | number | 结束时间。 | 123456 |
| id | number | ID。 | 123 |
| name | string | 名称。 | job-name |
| params | string | 额外参数。 | {} |
| jobSign | string | 任务唯一标识。 | job-1 |
| result | string | 结果。 | {\\"data\\":{\\"RELEASE\_INFO\\":\\"\[\]\\",\\"ARTIFACTSV2\\":\\"\[\]\\",\\"ARTIFACTS\\":\\"\[\]\\"},\\"requestId\\":\\"8bf5e28c-a58b-498e-a205-1c0ff5465c3c\\",\\"successful\\":true} |
| startTime | number | 开始时间。 | 123456 |
| status | string | 状态。 | SUCCESS |
| name | string | 名称。 | stage-name |
| startTime | number | 开始时间。 | 123 |
| status | string | 状态。 | SUCCESS |
| status | string | 状态。 | SUCCESS |
| triggerMode | string | 触发方式。 | 1 |
| updateTime | string | 更新时间。 | 2024-01-01 00:00:00 |

## 返回示例

`{ "pipelineRun": { "createTime": "2024-01-01 00:00:00", "creatorAccountId": "creator-account-id", "modifierAccountId": "modifier-account-id", "creator":"61c92a37ae805dbacc5b9f78", "modifier":"61c92a37ae805dbacc5b9f78", "pipelineId": "123", "pipelineRunId": "123456", "sources": [ { "data": { "branch": "master", "commit": "commit", "repo": "https://codeup.aliyun.com..." }, "sign": "sign", "type": "type" } ], "stageTopo": [ [ ] ], "stages": [ { "index":"Group0-Stage0", "name": "stage-name", "stageInfo": { "endTime": 123, "jobs": [ { "actions": [ { "disable": true, "params": "{}", "type": "type" } ], "endTime": 123456, "id": 123, "jobSign": "job-1", "result": "{\"data\":{\"RELEASE_INFO\":\"[]\",\"ARTIFACTSV2\":\"[]\",\"ARTIFACTS\":\"[]\"},\"requestId\":\"8bf5e28c-a58b-498e-a205-1c0ff5465c3c\",\"successful\":true}", "name": "job-name", "params": "{}", "startTime": 123456, "status": "SUCCESS" } ], "name": "stage-name", "startTime": 123, "status": "SUCCESS" } } ], "status": "SUCCESS", "triggerMode": "1", "updateTime": "2024-01-01 00:00:00" } }`

## 错误码

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。