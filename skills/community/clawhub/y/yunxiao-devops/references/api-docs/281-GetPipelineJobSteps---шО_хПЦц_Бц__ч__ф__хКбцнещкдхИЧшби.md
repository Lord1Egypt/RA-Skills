# GetPipelineJobSteps - 获取流水线任务步骤列表

通过 OpenAPI 获取流水线任务步骤列表。

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 流水线 | 流水线运行任务 | 只读 |

## **请求语法**

### **中心版**

`GET https://{domain}/oapi/v1/flow/organizations/{organizationId}/pipelines/{pipelineId}/pipelineRuns/{pipelineRunId}/jobs/{jobId}/steps`

### **Region版**

```
GET https://{domain}/oapi/v1/flow/pipelines/{pipelineId}/pipelineRuns/{pipelineRunId}/jobs/{jobId}/steps
```

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | -   是：中心版 -   否：Region版 | 企业 Id。 | 5ebbc0228123212b59xxxxx |
| pipelineId | string | path | 是 | 流水线 Id。 | 123 |
| pipelineRunId | string | path | 是 | 流水线运行 Id，可通过 API ListPipelineRuns 获取。 | 1 |
| jobId | string | path | 是 | 流水线运行任务 Id，可通过 API GetPipelineRun 获取。 | 1 |

## **请求示例**

### **中心版**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/flow/organizations/5ebbc0228123212b59xxxxx/pipelines/123/pipelineRuns/1/jobs/1/steps' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

### **Region版**

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/flow/pipelines/123/pipelineRuns/1/jobs/1/steps' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object |  |  |
| actionCode | string | actionCode。 | EXECUTION\_COMPONENT\_BUILD |
| actionName | string | actionName。 | 构建 |
| buildId | integer |  | 1 |
| jobId | integer |  | 1 |
| steps | array |  |  |
| \- | object |  |  |
| finish | boolean | 是否完成。 | true |
| nodeIndex | integer | 步骤下标。 | true |
| nodeName | string | 步骤名称。 | 执行命令 |
| parentIndex | integer | 父节点下标。 | 0 |
| running | boolean | 运行中。 | false |
| status | string | 状态。 | success |
| stepApiVersion | string | 步骤版本。 | v2 |
| stepIndex | integer | 步骤下标。 | true |
| stepName | string | 步骤名称。 | 执行命令 |
| supportDebug | boolean | 是否支持调试。 | true |

## **返回示例**

`{ "actionCode": "EXECUTION_COMPONENT_BUILD", "actionName": "构建", "buildId": 1, "jobId": 1, "steps": [ { "finish": true, "nodeIndex": true, "nodeName": "执行命令", "parentIndex": 0, "running": false, "status": "success", "stepApiVersion": "v2", "stepIndex": true, "stepName": "执行命令", "supportDebug": true } ] }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。