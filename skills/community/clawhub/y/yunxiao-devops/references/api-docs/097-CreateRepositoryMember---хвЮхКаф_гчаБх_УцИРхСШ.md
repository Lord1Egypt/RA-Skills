# CreateRepositoryMember - 增加代码库成员

通过 OpenAPI 增加代码库成员，可支持多个用户添加。

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 代码管理 | 成员 | 读写 |

## **请求语法**

### **中心版**

`POST https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/members`

### **Region版**

```
POST https://{domain}/oapi/v1/codeup/repositories/{repositoryId}/members
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
| accessLevel | integer | query | 是 | 访问权限：20-浏览者，30-开发者，40-库管理员。 | 40 |
| userId | string | query | 是 | 云效用户 ID（支持多个成员 ID，按英文逗号隔开）。 | \[62c795xxxb468af8\] |
| expiresAt | string | query | 否 | 到期时间，固定时间格式：yyyy-MM-dd。 | 2024-10-05 |

## **请求示例**

### **中心版**

`curl -X 'POST' \ 'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/members?accessLevel=40&userId=[62c795xxxb468af8]&expiresAt=2024-10-05' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

### **Region版**

```
curl -X 'POST' \
  'https://{domain}/oapi/v1/codeup/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/members?accessLevel=40&userId=[62c795xxxb468af8]&expiresAt=2024-10-05' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object |  |  |
| accessLevel | integer | 成员权限：20-浏览者，30-开发者，40-管理员。 | 30 |
| avatarUrl | string | 头像地址。 | https://example/example/w/100/h/100 |
| expiresAt | string | 过期时间。 | 2024-10-05T15:30:45Z |
| id | integer | 主键 ID（无实际业务意义）。 | 2813489 |
| name | string | 成员名称。 | codeup-demo |
| state | string | 状态：active-已激活, blocked-阻塞，暂无法使用。 | active |
| userId | string | 云效用户 ID（在 Codeup 提交的 OpenAPI 中涉及到用户 ID 之处，均应该使用该用户 ID）。 | 62c795xxxb468af8 |
| username | string | 用户名称。 | codeup-username |
| webUrl | string | 页面访问 URL。 | xxx |

## **返回示例**

`{ "accessLevel": 30, "avatarUrl": "https://example/example/w/100/h/100", "expiresAt": "2024-10-05T15:30:45Z", "id": 2813489, "name": "codeup-demo", "state": "active", "userId": "62c795xxxb468af8", "username": "codeup-username", "webUrl": "xxx" }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。