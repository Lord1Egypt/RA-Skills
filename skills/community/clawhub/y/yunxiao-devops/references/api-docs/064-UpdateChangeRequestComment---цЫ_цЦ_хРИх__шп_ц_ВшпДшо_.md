# UpdateChangeRequestComment - 更新合并请求评论

通过 OpenAPI 更新合并请求评论。

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 代码管理 | 合并请求 | 读写 |

## **请求语法**

### **中心版**

`PUT https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/changeRequests/{localId}/comments/{commentBizId}`

### **Region版**

```
PUT https://{domain}/oapi/v1/codeup/repositories/{repositoryId}/changeRequests/{localId}/comments/{commentBizId}
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
| localId | integer | path | 是 | 局部 ID，表示代码库中第几个合并请求。 | 1 |
| commentBizId | string | path | 是 | 评论 bizId。 | bf117304dfe44d5d9b1132f348edf92e |
| \- | object | body | 否 |  |  |
| content | string | body | 否 | 内容。 | your new comment |
| resolved | boolean | body | 否 | 是否已解决。 | false |

## **请求示例**

### **中心版**

`curl -X 'PUT' \ 'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/changeRequests/1/comments/bf117304dfe44d5d9b1132f348edf92e' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "content": "your new comment", "resolved": false }'`

### **Region版**

```
curl -X 'PUT' \
  'https://{domain}/oapi/v1/codeup/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/changeRequests/1/comments/bf117304dfe44d5d9b1132f348edf92e' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \
  --data '
    {
        "content": "your new comment",
        "resolved": false
    }'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object |  |  |
| result | boolean | 执行结果。 | true |

## **返回示例**

`{ "result": true }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。