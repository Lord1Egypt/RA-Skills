# ListWebHooks - 查询 Webhook 列表

通过 OpenAPI 查询 Webhook 列表。

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 代码管理 | WebHook | 只读 |

## **请求语法**

### **中心版**

`GET https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/webhooks`

### **Region版**

```
GET https://{domain}/oapi/v1/codeup/repositories/{repositoryId}/webhooks
```

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | -   是：中心版 -   否：Region版 | 组织 ID。 | 60d54f3daccf2bbd6659f3ad |
| repositoryId | string | path | 是 | 代码库 ID 或者 URL-Encoder 编码的全路径。 | 2813489或者60de7a6852743a5162b5f957%2FDemoRepo |
| page | integer | query | 否 | 页码，默认从1开始，一般不要超过150页。 | 1 |
| perPage | integer | query | 否 | 每页大小，默认20，取值范围【1，100】。 | 20 |

## **请求示例**

### **中心版**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/webhooks?page=1&perPage=20' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

### **Region版**

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/codeup/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/webhooks?page=1&perPage=20' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object |  |  |
| createdAt | string | 创建时间。 | 2024-10-05T15:30:45Z |
| description | string | Webhook 描述信息。 | 描述内容 |
| enableSSLVerification | boolean | 是否开启 SSL 认证。 | false |
| id | integer | Webhook 主键 ID。 | 1 |
| mergeRequestEvents | boolean | 合并请求事件。 | true |
| noteEvents | boolean | 评论事件。 | true |
| pushEvents | boolean | 代码推送事件。 | true |
| repositoryId | integer | 代码库 ID。 | 1 |
| tagPushEvents | boolean | 标签推送事件。 | true |
| token | string | 用于验证身份的 token，用户自定义。 | xxx |
| updatedAt | string | 更新时间。 | 2024-10-05T15:30:45Z |
| url | string | Webhook 链接。 | http://example/example |

## **返回示例**

`{ "createdAt": "2024-10-05T15:30:45Z", "description": "描述内容", "enableSSLVerification": false, "id": 1, "mergeRequestEvents": true, "noteEvents": true, "pushEvents": true, "repositoryId": 1, "tagPushEvents": true, "token": "xxx", "updatedAt": "2024-10-05T15:30:45Z", "url": "http://example/example" }`

## **响应头**

| **参数** | **描述** | **示例值** |
| --- | --- | --- |
| x-next-page | 下一页。 | 3 |
| x-page | 当前页。 | 2 |
| x-per-page | 每页大小。 | 20 |
| x-prev-page | 前一页。 | 1 |
| x-request-id | 请求 ID。 | 37294673-00CA-5B8B-914F-A8B35511E90A |
| x-total | 总数。 | 50 |
| x-total-pages | 总分页数。 | 3 |

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。