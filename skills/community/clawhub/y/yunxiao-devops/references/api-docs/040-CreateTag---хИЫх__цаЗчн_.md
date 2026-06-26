# CreateTag - 创建标签

通过 OpenAPI 创建代码库标签（Tag）。

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 代码管理 | 标签 | 读写 |

## **请求语法**

### **中心版**

`POST https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/tags`

### **Region版**

```
POST https://{domain}/oapi/v1/codeup/repositories/{repositoryId}/tags
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
| tagName | string | query | 是 | 标签名称（若包含特殊符号，需使用 URL-Encoder 进行编码处理）。 | v1.0 |
| ref | string | query | 是 | 来源，可为分支名称、另一个标签名称或者 CommitSHA。 | master |
| message | string | query | 否 | 描述信息。 | Tag 描述信息 |

## **请求示例**

### **中心版**

`curl -X 'POST' \ 'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/tags?tagName=v1.0&ref=master&message=Tag描述信息' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

### **Region版**

```
curl -X 'POST' \
  'https://{domain}/oapi/v1/codeup/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/tags?tagName=v1.0&ref=master&message=Tag描述信息' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object |  |  |
| commit | object | 提交信息。 |  |
| authorEmail | string | 作者邮箱。 | username@example.com |
| authorName | string | 作者姓名。 | codeup-name |
| authoredDate | string | 作者提交时间。 | 2024-10-05T15:30:45Z |
| committedDate | string | 提交者提交时间。 | 2024-10-05T15:30:45Z |
| committerEmail | string | 提交者邮箱。 | username@example.com |
| committerName | string | 提交者姓名。 | codeup-name |
| id | string | 提交 ID。 | de02b625ba8488f92eb204bcb3773a40c1b4ddac |
| message | string | 提交内容。 | Commit Message |
| parentIds | array\[string\] | 父提交 ID。 | \["3fdaf119cf76539c1a47de0074ac02927ef4c8e1"\] |
| shortId | string | 代码组路径。 | de02b625 |
| stats | object | 变更行数信息。 |  |
| additions | integer | 增加行数。 | 1 |
| deletions | integer | 删除行数。 | 1 |
| total | integer | 总变动行数。 | 2 |
| title | string | 标题，提交的第一行内容。 | Commit Title |
| webUrl | string | 页面访问地址。 | http://exmaple.com/example\_repo/commit/commit\_sha |
| id | string | 主键 ID。 | de02b625ba8488f92eb204bcb3773a40c1b4ddac |
| message | string | 标签描述信息。 | 描述内容 |
| name | string | 标签名。 | v1.0 |
| release | object | 发行版本信息。 |  |
| description | string | 描述信息。 | 描述内容 |
| tagName | string | 标签名。 | v1.0 |

## **返回示例**

`{ "commit": { "authorEmail": "username@example.com", "authorName": "codeup-name", "authoredDate": "2024-10-05T15:30:45Z", "committedDate": "2024-10-05T15:30:45Z", "committerEmail": "username@example.com", "committerName": "codeup-name", "id": "de02b625ba8488f92eb204bcb3773a40c1b4ddac", "message": "Commit Message", "parentIds": ["3fdaf119cf76539c1a47de0074ac02927ef4c8e1"], "shortId": "de02b625", "stats": { "additions": 1, "deletions": 1, "total": 2 }, "title": "Commit Title", "webUrl": "http://exmaple.com/example_repo/commit/commit_sha" }, "id": "de02b625ba8488f92eb204bcb3773a40c1b4ddac", "message": "描述内容", "name": "v1.0", "release": { "description": "描述内容", "tagName": "v1.0" } }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。