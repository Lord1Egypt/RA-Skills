# GetAppReleaseStageExecutionPipelineJobLog - 查询研发阶段流水线任务运行日志

查询研发阶段流水线任务运行日志。

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

`GET https://{domain}/oapi/v1/appstack/organizations/{organizationId}/apps/{appName}/releaseWorkflows/{releaseWorkflowSn}/releaseStages/{releaseStageSn}/executions/{executionNumber}:pipelineJobLog`

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
| executionNumber | string | path | 是 | 流水线运行ID，对应 ExecuteChangeRequestReleaseStage 返回的 pipelineRunId。 | 123456 |
| jobId | string | query | 是 | 任务 ID，可通过 GetReleaseStagePipelineRun 接口获取任务 ID。 | 123 |
| organizationId | string | path | 是 | 组织 ID。 | ec766e63aee3437d9a51f334d6exe671 |

## 请求示例

`curl -X 'GET' \ 'https://test.rdc.aliyuncs.com/oapi/v1/appstack/organizations/ec766e63aee3437d9a51f334d6exe671/apps/my-web-service/releaseWorkflows/3f472a12b15d4f418ad6227bb85f787c/releaseStages/6b4c53eee9a842c6a11235b29d002a81/executions/1:pipelineJobLog?jobId=123' \ -H 'accept: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## 返回参数

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object | 研发阶段执行流水线任务日志。 |  |
| content | string |  | xxxxxx |
| more | boolean |  | false |

## 返回示例

`{ "content": "", "more": false }`

## 错误码

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。