# GetLatestPipelineRun - 获取最近一次流水线运行信息

通过 OpenAPI 获取最近一次流水线运行信息。

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

`GET https://{domain}/oapi/v1/flow/organizations/{organizationId}/pipelines/{pipelineId}/runs/latestPipelineRun`

### **Region版**

```
GET https://{domain}/oapi/v1/flow/pipelines/{pipelineId}/runs/latestPipelineRun
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

## **请求示例**

### **中心版**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/flow/organizations/5ebbc0228123212b59xxxxx/pipelines/123/runs/latestPipelineRun' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

### **Region版**

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/flow/pipelines/123/runs/latestPipelineRun' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object |  |  |
| createTime | integer | 开始时间。 | 1590730400000 |
| creatorAccountId | string | 创建人。 | 1222222222 |
| globalParams | array |  |  |
| \- | object |  |  |
| encrypted | boolean | 是否加密。 | false |
| key | string | 参数 key。 | key |
| value | string | 参数值。 | value |
| groups | array |  |  |
| \- | object |  |  |
| id | integer | id。 | 1 |
| name | string | 名称。 | 执行命令 |
| modifierAccountId | string | 更新人。 | 1222222222 |
| pipelineId | integer | 流水线 id。 | 123 |
| pipelineRunId | integer | 流水线运行 id，可通过 API ListPipelineRuns 获取。 | 1 |
| pipelineType | string | 流水线类型。 | default |
| sources | array |  |  |
| \- | object |  |  |
| data | object |  |  |
| branch | string | 默认分支。 | master |
| cloneDepth | integer | 克隆深度。 | 1 |
| credentialId | integer | 服务证书 id。 | 222 |
| credentialLabel | string | 证书显示名称。 | 企业公钥 |
| credentialType | string | 证书类型。 | region-ssh |
| events | array\[string\] | 触发事件。 |  |
| isBranchMode | boolean | 触发过滤条件。 | false |
| isCloneDepth | boolean | 是否设置克隆深度。 | true |
| isSubmodule | boolean | 是否子模块。 | false |
| isTrigger | boolean | 是否开启提交触发。 | true |
| label | string | 展示名称。 | cdup/ss |
| namespace | string | github 命名空间。 | asasasas |
| repo | string | 仓库地址。 | https://codeup.aliyun.com/test.git |
| serviceConnectionId | integer | 服务连接 id。 | 12 |
| triggerFilter | string | 触发过滤条件。 | .\* |
| webhook | string | webhook 地址。 | https://flow.aliyun/webhook/asassasa |
| name | string | 代码源名称。 | 示例代码源 |
| sign | string | 代码源标识。 | assaaaaaasasasa |
| type | string | 代码源类型 aliyunGit 阿里云代码库 customGitlab 自建 git giteeGit 码云 codeup Codeup git 通用 git gitlab gitlab bitbucket bitbucket githubOAuth github。 | Codeup |
| stageGroup | array\[string\] |  |  |
| stages | array | 阶段详情。 |  |
| \- | object |  |  |
| index | string | 阶段序号。 | Group0-Stage0 |
| name | string | 阶段名称。 | Java 构建 |
| stageInfo | object |  |  |
| endTime | integer | 结束时间。 | 1729178040000 |
| jobs | array | 任务列表。 |  |
| \- | object |  |  |
| actions | array | 后续操作,具体参考文档 https://help.aliyun.com/document\_detail/2360596.html。 |  |
| \- | object |  |  |
| data | string | 数据。 |  |
| disable | boolean | 是否有权限调用,具体参考文档 https://help.aliyun.com/document\_detail/2360596.html。 | true |
| displayType | string | 显示类型。 | LOG |
| name | string | 名称。 | 构建日志 |
| order | integer | 顺序。 | 1 |
| params | object | 参数,具体参考文档 https://help.aliyun.com/document\_detail/2360596.html。 |  |
| key | string | 参数名称。 |  |
| title | string | 标题。 | 构建日志 |
| type | string | 后续操作类型,具体参考文档 https://help.aliyun.com/document\_detail/2360596.html。 | GetVMDeployOrder |
| endTime | integer | 结束时间。 | 1729178040000 |
| id | integer | 任务 id。 | 21212 |
| jobSign | string | 任务唯一标识。 | job-1 |
| name | string | 任务名称。 | Java 构建 |
| params | string | 运行参数。 | {} |
| result | string | 结果。 | {"data":{"RELEASE\_INFO":"\[\]","ARTIFACTSV2":"\[\]","ARTIFACTS":"\[\]"},"requestId":"8bf5e28c-a58b-498e-a205-1c0ff5465c3c","successful":true} |
| startTime | integer | 开始时间。 | 1729178040000 |
| status | string | 状态 FAIL 运行失败 SUCCESS 运行成功 RUNNING 运行中。 | RUNNING |
| name | string | 阶段名称。 | Java 构建 |
| startTime | integer | 开始时间。 | 1729178040000 |
| status | string | 状态 FAIL 运行失败 SUCCESS 运行成功 RUNNING 运行中。 | RUNNING |
| status | string | 状态 FAIL 运行失败 SUCCESS 运行成功 RUNNING 运行中。 | RUNNING |
| triggerMode | integer | 触发模式 1人工触发 2定时触发 3代码提交触发 5流水线触发6WEBHOOK 触发。 | 1 |
| updateTime | integer | 更新时间。 | 1590730400000 |

## **返回示例**

`{ "createTime": 1590730400000, "creatorAccountId": "1222222222", "globalParams": [ { "encrypted": false, "key": "key", "value": "value" } ], "groups": [ { "id": 1, "name": "执行命令" } ], "modifierAccountId": "1222222222", "pipelineId": 123, "pipelineRunId": 1, "pipelineType": "default", "sources": [ { "data": { "branch": "master", "cloneDepth": 1, "credentialId": 222, "credentialLabel": "企业公钥", "credentialType": "region-ssh", "events": [ ], "isBranchMode": false, "isCloneDepth": true, "isSubmodule": false, "isTrigger": true, "label": "cdup/ss", "namespace": "asasasas", "repo": "https://codeup.aliyun.com/test.git", "serviceConnectionId": 12, "triggerFilter": ".*", "webhook": "https://flow.aliyun/webhook/asassasa" }, "name": "示例代码源", "sign": "assaaaaaasasasa", "type": "Codeup" } ], "stageGroup": [ ], "stages": [ { "index": "Group0-Stage0", "name": "Java构建", "stageInfo": { "endTime": 1729178040000, "jobs": [ { "actions": [ { "data": "", "disable": true, "displayType": "LOG", "name": "构建日志", "order": 1, "params": { "key": "" }, "title": "构建日志", "type": "GetVMDeployOrder" } ], "endTime": 1729178040000, "id": 21212, "jobSign": "job-1", "name": "Java构建", "params": "{}", "result": "{"data":{"RELEASE_INFO":"[]","ARTIFACTSV2":"[]","ARTIFACTS":"[]"},"requestId":"8bf5e28c-a58b-498e-a205-1c0ff5465c3c","successful":true}", "startTime": 1729178040000, "status": "RUNNING" } ], "name": "Java构建", "startTime": 1729178040000, "status": "RUNNING" } } ], "status": "RUNNING", "triggerMode": 1, "updateTime": 1590730400000 }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。