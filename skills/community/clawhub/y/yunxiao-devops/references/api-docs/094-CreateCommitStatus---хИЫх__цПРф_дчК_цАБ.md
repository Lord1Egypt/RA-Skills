# CreateCommitStatus - 创建提交状态

通过 OpenAPI 创建或写入提交状态，更新操作也使用该接口。

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 代码管理 | 提交状态 | 读写 |

## **请求语法**

### **中心版**

`POST https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/commits/{sha}/statuses`

### **Region版**

```
POST https://{domain}/oapi/v1/codeup/repositories/{repositoryId}/commits/{sha}/statuses
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
| sha | string | path | 是 | 提交 ID，即 Commit SHA。 | 6da8c14b5a9102998148b7ea35f96507d5304f74 |
| \- | object | body | 否 |  |  |
| context | string | body | 否 | 用于区分不同系统写入的字符串标识，会以标题的作用在 UI 页面展示，默认为 default，长度不超过50；该参数在卡点设置和合并请求联动中扮演重要的角色，正式使用时，切勿随意设置。 | default-context |
| description | string | body | 否 | 描述信息。 | commit status description |
| state | string | body | 是 | 写入状态，且仅能填入以下四个字符串：error - 异常；failure - 失败；pending - 运行中；success - 成功。 | success |
| targetUrl | string | body | 否 | 用户写入的跳转链接，代码平台仅提供跳转的 UI，一般可设置为三方系统首页的链接。 | http://example.com/example |

## **请求示例**

### **中心版**

`curl -X 'POST' \ 'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/commits/6da8c14b5a9102998148b7ea35f96507d5304f74/statuses' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "context": "default-context", "description": "commit status description", "state": "success", "targetUrl": "http://example.com/example" }'`

### **Region版**

```
curl -X 'POST' \
  'https://{domain}/oapi/v1/codeup/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/commits/6da8c14b5a9102998148b7ea35f96507d5304f74/statuses' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \
  --data '
    {
        "context": "default-context",
        "description": "commit status description",
        "state": "success",
        "targetUrl": "http://example.com/example"
    }'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object |  |  |
| author | object | 写入人信息。 |  |
| avatarUrl | string | 用户头像地址。 | https://example/example/w/100/h/100 |
| id | string | 用户 ID。 | 62c795xxxb468af8 |
| name | string | 用户名称。 | codeup-name |
| type | string | 写入人类型：User - 用户；Bot - 应用（暂无）。 | User |
| username | string | 用户登录名。 | codeup-username |
| context | string | 用于区分不同系统的字符串标识，会以标题的作用在相应的页面进行展示，长度不超过50；正式使用时，勿随意设置值。 | default-context |
| createdAt | string | 写入时间。 | 2024-10-05T15:30:45Z |
| description | string | 简要描述信息，且不超过3000个字符。 | commit status description |
| id | integer | 主键 ID，无业务实义。 | 1 |
| sha | string | 提交 ID，即 Commit SHA。 | 6da8c14b5a9102998148b7ea35f96507d5304f74 |
| state | string | 写入状态：error - 异常；failure - 失败；pending - 运行中；success - 成功。 | success |
| targetUrl | string | 用户写入的外部链接，代码平台提供跳转的 UI，一般可设置为三方系统的链接。 | http://example.com/example |
| updatedAt | string | 更新时间。 | 2024-10-05T15:30:45Z |

## **返回示例**

`{ "author": { "avatarUrl": "https://example/example/w/100/h/100", "id": "62c795xxxb468af8", "name": "codeup-name", "type": "User", "username": "codeup-username" }, "context": "default-context", "createdAt": "2024-10-05T15:30:45Z", "description": "commit status description", "id": 1, "sha": "6da8c14b5a9102998148b7ea35f96507d5304f74", "state": "success", "targetUrl": "http://example.com/example", "updatedAt": "2024-10-05T15:30:45Z" }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。