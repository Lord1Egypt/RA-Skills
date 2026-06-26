# ListAppReleaseStageExecutionIntegratedMetadata - 查询研发阶段执行记录集成变更信息

查询研发阶段执行记录集成变更信息。

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

`GET https://{domain}/oapi/v1/appstack/organizations/{organizationId}/apps/{appName}/releaseWorkflows/{releaseWorkflowSn}/releaseStages/{releaseStageSn}/executions/{executionNumber}/integratedMetadata`

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
| executionNumber | integer | path | 是 | 流水线运行 ID，对应 ExecuteChangeRequestReleaseStage 返回中的 pipelineRunId。 | 1 |
| organizationId | string | path | 是 | 组织 ID。 | ec766e63aee3437d9a51f334d6exe671 |

## 请求示例

`curl -X 'GET' \ 'https://test.rdc.aliyuncs.com/oapi/v1/appstack/organizations/ec766e63aee3437d9a51f334d6exe671/apps/my-web-service/releaseWorkflows/3f472a12b15d4f418ad6227bb85f787c/releaseStages/6b4c53eee9a842c6a11235b29d002a81/executions/1/integratedMetadata' \ -H 'accept: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## 返回参数

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | array |  |  |
| \- | object | 发布阶段实例集成数据信息。 |  |
| changeRequests | array | 变更请求。 |  |
| \- | object | 变更请求集成数据信息。 |  |
| branchName | string | 变更请求分支。 | master |
| commitId | string | 变更请求 commitId。 | a80102ee37cca462a23865e7a3e66ac1ca032a5c |
| name | string | 变更请求名称。 | name-xxx |
| ownerId | string | 变更拥有者。 | 10df6011-2837-4fdb-ad92-356a679a60ca |
| sn | string | 变更请求编号。 | sn-xxx |
| releaseBranch | string | 发布分支。 | master |
| releaseRevision | string | 发布分支Git版本。 | a80102ee37cca462a23865e7a3e66ac1ca032a5c |
| repoType | string | 代码仓库类型。 | CODEUP |
| repoUrl | string | 代码仓库地址。 | https://codeup.aliyun.com… |

## 返回示例

`[ { "changeRequests": [ { "branchName": "master", "commitId": "a80102ee37cca462a23865e7a3e66ac1ca032a5c", "name": "name-xxx", "ownerId": "10df6011-2837-4fdb-ad92-356a679a60ca", "sn": "sn-xxx" } ], "releaseBranch": "master", "releaseRevision": "a80102ee37cca462a23865e7a3e66ac1ca032a5c", "repoType": "CODEUP", "repoUrl": "https://codeup.aliyun.com..." } ]`

## 错误码

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。