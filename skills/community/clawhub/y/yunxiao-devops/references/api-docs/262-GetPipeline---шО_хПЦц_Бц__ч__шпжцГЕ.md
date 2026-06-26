# GetPipeline - 获取流水线详情

通过 OpenAPI 获取流水线详情。

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

`GET https://{domain}/oapi/v1/flow/organizations/{organizationId}/pipelines/{pipelineId}`

### **Region版**

```
GET https://{domain}/oapi/v1/flow/pipelines/{pipelineId}
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

## **请求示例**

### **中心版**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/flow/organizations/5ebbc0228123212b59xxxxx/pipelines/123' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

### **Region版**

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/flow/pipelines/123' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object |  |  |
| createTime | integer | 创建时间。 | 1729178040000 |
| creatorAccountId | string | 创建人。 | 112222122 |
| envId | integer | 环境 id 0 日常环境 1预发环境 2正式环境。 | 0 |
| envName | string | 环境名称。 | 日常环境 |
| groupId | integer | 流水线分组 id。 | 1111 |
| modifierAccountId | string | 最后更新人。 | 112222122 |
| name | string | 流水线名称。 | 流水线 |
| pipelineConfig | object |  |  |
| flow | string | 流程配置。 | schema: tb pipeline: - name: 执行命令 stages: - driven: AUTO jobs: - displayName: 执行命令 task: execution-component-production@10 identifier: '10\_1626147407245' templateType: task templateSign: '' templateBatchUpdate: 'N' extraInfo: '' params: version1: pre-jdk1.62 steps: - name: 执行命令 stepType: exec-shell stepIdentifier: '10\_1626147407245\_\_11\_1626147407249' command: \| # input your command here echo hello,world! ARTIFACTS: '' JSONEncoding: true freeInTaskGroupModeFields: - ARTIFACTS source: 132504-sss\_ddd\_3mvJ ENGINE\_PIPELINE\_NAME: '\\${INPUTS.ENGINE\_PIPELINE\_NAME}' ENGINE\_PIPELINE\_ID: '\\${INPUTS.ENGINE\_PIPELINE\_ID}' ENGINE\_PIPELINE\_INST\_ID: '\\${INPUTS.ENGINE\_PIPELINE\_INST\_ID}' ENGINE\_PIPELINE\_INST\_NUMBER: '\\${INPUTS.ENGINE\_PIPELINE\_INST\_NUMBER}' buildNodeGroup: K8S-4 plugins: \[\] output: \[\] freeInTaskGroupModeFields: \[\] |
| settings | string | 流水线配置。 | {} |
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
| sign | string | 代码源标识。 | xxsxsxs |
| type | string | 代码源类型 aliyunGit 阿里云代码库 customGitlab 自建 git giteeGit 码云 codeup Codeup git 通用 git gitlab gitlab bitbucket bitbucket githubOAuth github。 | Codeup |
| tagList | array |  |  |
| \- | object |  |  |
| id | integer | 标签 id。 | 22 |
| name | string | 标签名称。 | 标签1 |
| updateTime | integer | 更新时间。 | 1729178040000 |

## **返回示例**

`{ "createTime": 1729178040000, "creatorAccountId": "112222122", "envId": 0, "envName": "日常环境", "groupId": 1111, "modifierAccountId": "112222122", "name": "流水线", "pipelineConfig": { "flow": "schema: tb pipeline: - name: 执行命令 stages: - driven: AUTO jobs: - displayName: 执行命令 task: execution-component-production@10 identifier: '10_1626147407245' templateType: task templateSign: '' templateBatchUpdate: 'N' extraInfo: '' params: version1: pre-jdk1.62 steps: - name: 执行命令 stepType: exec-shell stepIdentifier: '10_1626147407245__11_1626147407249' command: | # input your command here echo hello,world! ARTIFACTS: '' JSONEncoding: true freeInTaskGroupModeFields: - ARTIFACTS source: 132504-sss_ddd_3mvJ ENGINE_PIPELINE_NAME: '${INPUTS.ENGINE_PIPELINE_NAME}' ENGINE_PIPELINE_ID: '${INPUTS.ENGINE_PIPELINE_ID}' ENGINE_PIPELINE_INST_ID: '${INPUTS.ENGINE_PIPELINE_INST_ID}' ENGINE_PIPELINE_INST_NUMBER: '${INPUTS.ENGINE_PIPELINE_INST_NUMBER}' buildNodeGroup: K8S-4 plugins: [] output: [] freeInTaskGroupModeFields: []", "settings": "{}", "sources": [ { "data": { "branch": "master", "cloneDepth": 1, "credentialId": 222, "credentialLabel": "企业公钥", "credentialType": "region-ssh", "events": [ ], "isBranchMode": false, "isCloneDepth": true, "isSubmodule": false, "isTrigger": true, "label": "cdup/ss", "namespace": "asasasas", "repo": "https://codeup.aliyun.com/test.git", "serviceConnectionId": 12, "triggerFilter": ".*", "webhook": "https://flow.aliyun/webhook/asassasa" }, "sign": "xxsxsxs", "type": "Codeup" } ] }, "tagList": [ { "id": 22, "name": "标签1" } ], "updateTime": 1729178040000 }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。