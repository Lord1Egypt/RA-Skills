# ListPipelineRuns - 获取流水线运行实例列表

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 流水线 | 流水线运行实例 | 只读 |

## **请求语法**

### **中心版**

`GET https://{domain}/oapi/v1/flow/organizations/{organizationId}/pipelines/{pipelineId}/runs`

### **Region版**

```
GET https://{domain}/oapi/v1/flow/pipelines/{pipelineId}/runs
```

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | -   是：中心版 -   否：Region版 | 企业 Id。 | 5ebbc0228123212b59xxxxx |
| pipelineId | string | path | 是 | 流水线 id。 | 123 |
| perPage | integer | query | 否 | 每页数据条数，默认10，最大支持30。 | 10 |
| page | integer | query | 否 | 当前页，默认1。 | 1 |
| startTime | integer | query | 否 | 执行开始时间。 | 1729178040000 |
| endTme | integer | query | 否 | 执行结束时间。 | 1729178040000 |
| status | string | query | 否 | 运行状态，状态 FAIL 运行失败 SUCCESS 运行成功 RUNNING 运行中。 | FAIL |
| triggerMode | integer | query | 否 | 触发方式，1人工触发 2定时触发 3代码提交触发 5流水线触发 6WEBHOOK 触发。 | 1 |

## **请求示例**

### **中心版**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/flow/organizations/5ebbc0228123212b59xxxxx/pipelines/123/runs?perPage=10&page=1&startTime=1729178040000&endTme=1729178040000&status=FAIL&triggerMode=1' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

### **Region版**

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/flow/pipelines/123/runs?perPage=10&page=1&startTime=1729178040000&endTme=1729178040000&status=FAIL&triggerMode=1' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | array |  |  |
| \- | object |  |  |
| creatorAccountId | string | 创建人。 | 1222222222 |
| endTime | integer | 结束时间。 | 1729178040000 |
| pipelineId | integer | 流水线 id。 | 123 |
| pipelineRunId | integer | 流水线运行实例 id。 | 1 |
| startTime | integer | 开始时间。 | 1729178040000 |
| triggerMode | integer | 触发模式 1人工触发 2定时触发 3代码提交触发 5流水线触发 6 WEBHOOK 触发。 | 1 |

## **返回示例**

`[ { "creatorAccountId": "1222222222", "endTime": 1729178040000, "pipelineId": 123, "pipelineRunId": 1, "startTime": 1729178040000, "triggerMode": 1 } ]`

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