# ListWorkitemAttachments - 获取工作项附件列表

通过 OpenAPI 获取工作项附件列表。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。
    
    | **产品** | **资源** | **所需权限** |
    | --- | --- | --- |
    | 项目协作 | 工作项附件 | 只读 |
    

## **请求语法**

`GET https://{domain}/oapi/v1/projex/organizations/{organizationId}/workitems/{id}/attachments`

### **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| id | string | path | 是 | 工作项唯一标识。 |  |
| organizationId | string | path | 是 | organizationId。 | 5ebbc0228123212b59xxxxx |

## **请求示例**

`curl -X 'GET' \ 'https://test.rdc.aliyuncs.com/oapi/v1/projex/organizations/{organizationId}/workitems/{id}/attachments' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | array |  |  |
| \- | object |  |  |
| creator | object |  |  |
| id | string | 用户 id。 | 674d96abd497cd558d68\*\*\*\* |
| name | string | 名称。 | name-xxx |
| fileId | string | 文件 id。 | 985353d622cc8521793e08\*\*\*\* |
| fileName | string | 文件名称。 | file-name-xxx |
| gmtCreate | string | 创建时间。 |  |
| gmtModified | string | 修改时间。 |  |
| id | string | id。 | id-xxx |
| modifier | object |  |  |
| id | string | 用户 id。 | 674d96abd497cd558d68\*\*\*\* |
| name | string | 名称。 | name-xxx |
| size | integer | 文件大小。 | 1024 |
| suffix | string | 文件后缀。 | .png |
| url | string | 文件下载地址，是个临时的下载地址，有时效性。 | https://xxx.test.com |

## **返回示例**

`[ { "creator": { "id": "674d96abd497cd558d68****", "name": "name-xxx" }, "fileId": "985353d622cc8521793e08****", "fileName": "file-name-xxx", "gmtCreate": "", "gmtModified": "", "id": "id-xxx", "modifier": { "id": "674d96abd497cd558d68****", "name": "name-xxx" }, "size": 1024, "suffix": ".png", "url": "https://xxx.test.com" } ]`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。