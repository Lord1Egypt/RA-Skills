# ListPipelineGroupPipelines - 获取流水线分组下流水线列表

通过 OpenAPI 获取流水线分组下流水线列表。

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 流水线 | 流水线分组 | 只读 |

## **请求语法**

### **中心版**

`GET https://{domain}/oapi/v1/flow/organizations/{organizationId}/pipelineGroups/pipelines`

### **Region版**

```
GET https://{domain}/oapi/v1/flow/pipelineGroups/pipelines
```

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | -   是：中心版 -   否：Region版 | 企业 Id。 | 5ebbc0228123212b59xxxxx |
| groupId | integer | query | 是 | 流水线分组 id ,0 表示将流水线改为未分组。 | 111 |
| createStartTime | integer | query | 否 | 创建开始时间。 | 1729178040000 |
| createEndTime | integer | query | 否 | 创建结束时间。 | 1729178040000 |
| executeStartTime | integer | query | 否 | 执行开始时间。 | 1729178040000 |
| executeEndTime | integer | query | 否 | 执行结束时间。 | 1729178040000 |
| pipelineName | string | query | 否 | 流水线名称。 | 流水线 A |
| statusList | string | query | 否 | 流水线运行状态，多个逗号分割，SUCCESS,RUNNING,FAIL,CANCELED,WAITING。 | RUNNING,SUCCESS |
| perPage | integer | query | 否 | 每页数据条数，默认10，最大支持30。 | 10 |
| page | integer | query | 否 | 当前页，默认1。 | 1 |

## **请求示例**

### **中心版**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/flow/organizations/5ebbc0228123212b59xxxxx/pipelineGroups/pipelines?groupId=111&createStartTime=1729178040000&createEndTime=1729178040000&executeStartTime=1729178040000&executeEndTime=1729178040000&pipelineName=流水线A&statusList=RUNNING,SUCCESS&perPage=10&page=1' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

### **Region版**

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/flow/pipelineGroups/pipelines?groupId=111&createStartTime=1729178040000&createEndTime=1729178040000&executeStartTime=1729178040000&executeEndTime=1729178040000&pipelineName=流水线A&statusList=RUNNING,SUCCESS&perPage=10&page=1' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | array |  |  |
| \- | object |  |  |
| gmtCreate | integer | 创建时间。 | 1729178040000 |
| pipelineId | integer | 流水线 Id。 | 124 |
| pipelineName | string | 流水线名称。 | 流水线 |

## **返回示例**

`[ { "gmtCreate": 1729178040000, "pipelineId": 124, "pipelineName": "流水线" } ]`

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