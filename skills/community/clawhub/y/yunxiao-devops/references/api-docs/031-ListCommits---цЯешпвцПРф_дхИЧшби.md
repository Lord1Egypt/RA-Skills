# ListCommits - 查询提交列表

通过 OpenAPI 查询代码库提交（Commit）列表。

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 代码管理 | 提交 | 只读 |

## **请求语法**

### **中心版**

`GET https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/commits`

### **Region版**

```
GET https://{domain}/oapi/v1/codeup/repositories/{repositoryId}/commits
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
| refName | string | query | 是 | 分支名称、标签名称或提交版本，默认为代码库默认分支。 | master |
| since | string | query | 否 | 提交起始时间，格式：YYYY-MM-DDTHH:MM:SSZ。 | 2024-10-05T15:30:45Z |
| until | string | query | 否 | 提交截止时间，格式：YYYY-MM-DDTHH:MM:SSZ。 | 2024-10-05T15:30:45Z |
| page | integer | query | 否 | 页码。 | 1 |
| perPage | integer | query | 否 | 每页大小。 | 10 |
| path | string | query | 否 | 文件路径。 | src/test/main.java |
| search | string | query | 否 | 搜索关键字。 | Test |
| showSignature | boolean | query | 否 | 是否展示签名。 | false |
| committerIds | string | query | 否 | 提交人 ID 列表（多个 ID 以逗号隔开）。 | \[62c795xxxb468af8\] |

## **请求示例**

### **中心版**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/commits?refName=master&since=2024-10-05T15:30:45Z&until=2024-10-05T15:30:45Z&page=1&perPage=10&path=src/test/main.java&search=Test&showSignature=false&committerIds=[62c795xxxb468af8]' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

### **Region版**

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/codeup/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/commits?refName=master&since=2024-10-05T15:30:45Z&until=2024-10-05T15:30:45Z&page=1&perPage=10&path=src/test/main.java&search=Test&showSignature=false&committerIds=[62c795xxxb468af8]' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | array |  |  |
| \- | object |  |  |
| authorEmail | string | 作者邮箱。 | username@example.com |
| authorName | string | 作者姓名。 | codeup-name |
| authoredDate | string | 作者提交时间。 | 2024-10-05T15:30:45Z |
| committedDate | string | 提交者提交时间。 | 2024-10-05T15:30:45Z |
| committerEmail | string | 提交者邮箱。 | username@example.com |
| committerName | string | 提交者姓名。 | codeup-name |
| id | string | 提交 ID。 | 6da8c14b5a9102998148b7ea35f96507d5304f74 |
| message | string | 提交内容。 | commit message detail |
| parentIds | array\[string\] | 父提交 ID。 | \["3fdaf119cf76539c1a47de0074ac02927ef4c8e1"\] |
| shortId | string | 代码组路径。 | 6da8c14b |
| title | string | 标题，提交的第一行内容。 | commit msg title |
| webUrl | string | 页面访问地址。 | http://exmaple.com/example\_repo/commit/commit\_sha |

## **返回示例**

`[ { "authorEmail": "username@example.com", "authorName": "codeup-name", "authoredDate": "2024-10-05T15:30:45Z", "committedDate": "2024-10-05T15:30:45Z", "committerEmail": "username@example.com", "committerName": "codeup-name", "id": "6da8c14b5a9102998148b7ea35f96507d5304f74", "message": "commit message detail", "parentIds": ["3fdaf119cf76539c1a47de0074ac02927ef4c8e1"], "shortId": "6da8c14b", "title": "commit msg title", "webUrl": "http://exmaple.com/example_repo/commit/commit_sha" } ]`

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