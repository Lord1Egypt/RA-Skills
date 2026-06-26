# ListPipelineJobHistorys - 获取流水线任务的执行历史

通过 OpenAPI 获取流水线任务的执行历史。

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 流水线 | 流水线 | 只读 |

## **请求语法**

### **中心版**

`GET https://{domain}/oapi/v1/flow/organizations/{organizationId}/pipelines/getComponentsWithoutButtons`

### **Region版**

```
GET https://{domain}/oapi/v1/flow/pipelines/getComponentsWithoutButtons
```

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | -   是：中心版 -   否：Region版 | 企业 Id。 | 5ebbc0228123212b59xxxxx |
| pipelineId | string | query | 是 | 流水线 Id, 可通过 API ListPipelines 获取。 | 123 |
| category | string | query | 是 | 任务分类，暂时只支持 DEPLOY。 | DEPLOY |
| identifier | string | query | 是 | 任务标识。 | 10\_ssasasa |
| perPage | integer | query | 否 | 每页数据条数，默认10，最大支持30。 | 10 |
| page | integer | query | 否 | 当前页，默认1。 | 1 |

## **请求示例**

### **中心版**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/flow/organizations/5ebbc0228123212b59xxxxx/pipelines/getComponentsWithoutButtons?pipelineId=123&category=DEPLOY&identifier=10_ssasasa&perPage=10&page=1' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

### **Region版**

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/flow/pipelines/getComponentsWithoutButtons?pipelineId=123&category=DEPLOY&identifier=10_ssasasa&perPage=10&page=1' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | array |  |  |
| \- | object |  |  |
| executeNumber | integer | 任务第几次执行。 | 1 |
| identifier | string | 任务标识。 | 10\_xaxxsxa |
| jobId | integer | 任务 id。 | 123 |
| jobName | string | 任务名称。 | 任务名称 |
| operatorAccountId | string | 运行人 aliyunPK。 | ssaasssa |
| pipelineId | integer | 流水线 Id, 可通过 API ListPipelines 获取。 | 123 |
| pipelineRunId | integer | 流水线运行实例 id。 | 123 |
| sources | string | 任务运行的代码源信息。 | {} |
| status | string | 任务执行状态。 | SUCCESS |

## **返回示例**

`[ { "executeNumber": 1, "identifier": "10_xaxxsxa", "jobId": 123, "jobName": "任务名称", "operatorAccountId": "ssaasssa", "pipelineId": 123, "pipelineRunId": 123, "sources": "{}", "status": "SUCCESS" } ]`

## **响应头**

| **参数** | **描述** | **示例值** |
| --- | --- | --- |
| x-next-page | 下一页。 | 3 |
| x-page | 当前页。 | 2 |
| x-per-page | 每页数据条数。 | 10 |
| x-prev-page | 上一页。 | 1 |
| x-total | 总数据量。 | 100 |
| x-total-pages | 总分页数。 | 10 |

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。