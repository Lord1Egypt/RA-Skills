# CreateBranch - 创建分支

通过 OpenAPI 创建分支。

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 代码管理 | 分支 | 读写 |

## **请求语法**

### **中心版**

`POST https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/branches`

### **Region版**

```
POST https://{domain}/oapi/v1/codeup/repositories/{repositoryId}/branches
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
| branch | string | query | 是 | 创建的分支名称。 | demo-branch |
| ref | string | query | 是 | 来源分支名称。 | master |

## **请求示例**

### **中心版**

`curl -X 'POST' \ 'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/branches?branch=demo-branch&ref=master' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

### **Region版**

```
curl -X 'POST' \
  'https://{domain}/oapi/v1/codeup/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/branches?branch=demo-branch&ref=master' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object |  |  |
| commit | object | 分支最近一次提交信息。 |  |
| authorEmail | string | 作者邮箱。 | username@example.com |
| authorName | string | 作者姓名。 | Codeup-Demo |
| authoredDate | string | 作者提交时间。 | 2024-04-05T15:30:45Z |
| committedDate | string | 提交者提交时间。 | 2024-04-05T15:30:45Z |
| committerEmail | string | 提交者邮箱。 | username@example.com |
| committerName | string | 提交者姓名。 | Codeup-Demo |
| id | string | 提交 ID。 | 45ede4680536406d793e0e629bc771cb9fcaa153 |
| message | string | 提交内容。 | commit message |
| parentIds | array\[string\] | 父提交 ID。 | \["3fdaf119cf76539c1a47de0074ac02927ef4c8e1"\] |
| shortId | string | 短 ID。 | 45ede468 |
| stats | object | 提交变更行统计。 |  |
| additions | integer | 增加行数。 | 10 |
| deletions | integer | 删除行数。 | 1 |
| total | integer | 总变动行数。 | 11 |
| title | string | 标题，提交的第一行内容。 | commit title |
| defaultBranch | boolean | 是否是默认分支。 | false |
| name | string | 分支名称。 | demo-branch |
| protected | boolean | 是否是保护分支。 | false |
| webUrl | string | 页面访问 URL。 | http://codeup.example.com/org-id/repo/demo-branch |

## **返回示例**

`{ "commit": { "authorEmail": "username@example.com", "authorName": "Codeup-Demo", "authoredDate": "2024-04-05T15:30:45Z", "committedDate": "2024-04-05T15:30:45Z", "committerEmail": "username@example.com", "committerName": "Codeup-Demo", "id": "45ede4680536406d793e0e629bc771cb9fcaa153", "message": "commit message", "parentIds": ["3fdaf119cf76539c1a47de0074ac02927ef4c8e1"], "shortId": "45ede468", "stats": { "additions": 10, "deletions": 1, "total": 11 }, "title": "commit title" }, "defaultBranch": false, "name": "demo-branch", "protected": false, "webUrl": "http://codeup.example.com/org-id/repo/demo-branch" }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。