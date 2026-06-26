# GetPipelineEmasArtifactUrl - 获取流水线 emas 构建产物临时下载地址

通过 OpenAPI 获取流水线 emas 构建产物临时下载地址。

| **适用版本** | **中心版** |
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

`GET https://{domain}/oapi/v1/flow/organizations/{organizationId}/pipelines/getEmasArtifactDownloadUrl`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | 是 | 企业 Id。 | 5ebbc0228123212b59xxxxx |
| emasJobInstanceId | string | query | 是 | emas 任务 id，可通过 API https://help.aliyun.com/document\_detail/460565.html。 | Psaxsa |
| md5 | string | query | 是 | emas 构建产物 md5，可通过 API https://help.aliyun.com/document\_detail/460565.html。 | assasas |
| pipelineId | integer | query | 是 | 流水线 Id, 可通过 API ListPipelines 获取。 | 1111 |
| pipelineRunId | integer | query | 是 | 流水线运行实例 id。 | 1 |
| serviceConnectionId | integer | query | 是 | 服务连接 id。 | 122 |

## **请求示例**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/flow/organizations/5ebbc0228123212b59xxxxx/pipelines/getEmasArtifactDownloadUrl?emasJobInstanceId=Psaxsa&md5=assasas&pipelineId=1111&pipelineRunId=1&serviceConnectionId=122' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | string | emas 构建产物临时下载地址，一个小时有效期。 | http://aliyun.com |

## **返回示例**

`http://aliyun.com`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。