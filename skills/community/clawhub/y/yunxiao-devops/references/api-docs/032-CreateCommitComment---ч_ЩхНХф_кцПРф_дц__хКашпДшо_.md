# CreateCommitComment - 给单个提交添加评论

通过 OpenAPI 给单个提交添加评论。

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 代码管理 | 提交 | 读写 |

## **请求语法**

### **中心版**

`POST https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/commits/{sha}/comments`

### **Region版**

```
POST https://{domain}/oapi/v1/codeup/repositories/{repositoryId}/commits/{sha}/comments
```

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | -   是：中心版 -   否：Region版 | 组织 ID。 | 60de7a6852743a5162b5f957 |
| repositoryId | string | path | 是 | 代码库 ID 或者 URL-Encoder 编码的全路径。 | 2813489或者60de7a6852743a5162b5f957%2FDemoRepo |
| sha | string | path | 是 | 提交的 SHA 值。 | 2b4f8fc38bdf464359c3a05334654fa27e15a704 |
| \- | object | body | 否 | commit 的评论。 |  |
| content | string | body | 是 | commit 的评论内容。 | comment content |

## **请求示例**

### **中心版**

`curl -X 'POST' \ 'https://{domain}/oapi/v1/codeup/organizations/60de7a6852743a5162b5f957/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/commits/2b4f8fc38bdf464359c3a05334654fa27e15a704/comments' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "content": "comment content" }'`

### **Region版**

```
curl -X 'POST' \
  'https://{domain}/oapi/v1/codeup/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/commits/2b4f8fc38bdf464359c3a05334654fa27e15a704/comments' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \
  --data '
    {
        "content": "comment content"
    }'
```

## **返回参数**

无

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。