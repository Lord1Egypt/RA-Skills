# ListChangeRequests - 查询合并请求列表

通过 OpenAPI 查询合并请求（新）列表，支持多条件筛选、分页以及排序。

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 代码管理 | 合并请求 | 只读 |

## **请求语法**

### **中心版**

`GET https://{domain}/oapi/v1/codeup/organizations/{organizationId}/changeRequests`

### **Region版**

```
GET https://{domain}/oapi/v1/codeup/changeRequests
```

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | -   是：中心版 -   否：Region版 | 组织 ID。 | 60d54f3daccf2bbd6659f3ad |
| page | integer | query | 否 | 页码。 | 1 |
| perPage | integer | query | 否 | 每页大小。 | 20 |
| projectIds | string | query | 否 | 代码库 ID 或者路径列表，多个以逗号分隔。 | 2813489,2813490 |
| authorIds | string | query | 否 | 创建者用户 ID 列表，多个以逗号分隔。 | 62c795xxxb468af8 |
| reviewerIds | string | query | 否 | 评审人用户 ID 列表，多个以逗号分隔。 | 62c795xxxb468af8 |
| state | string | query | 否 | 合并请求筛选状态：opened，merged，closed，默认为 null，即查询全部状态。 | opened |
| search | string | query | 否 | 标题关键字搜索。 | mr title |
| orderBy | string | query | 否 | 排序字段，仅支持：created\_at - 创建时间；updated\_at - 更新时间，默认排序字段。 | updated\_at |
| sort | string | query | 否 | 排序方式：asc - 升序；desc - 降序，默认排序方式。 | desc |
| createdBefore | string | query | 否 | 起始创建时间，时间格式为 ISO 8601。 | 2024-04-05T15:30:45Z |
| createdAfter | string | query | 否 | 截止创建时间，时间格式为 ISO 8601。 | 2024-04-05T15:30:45Z |

## **请求示例**

### **中心版**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/changeRequests?page=1&perPage=20&projectIds=2813489,2813490&authorIds=62c795xxxb468af8&reviewerIds=62c795xxxb468af8&state=opened&search=mr title&orderBy=updated_at&sort=desc&createdBefore=2024-04-05T15:30:45Z&createdAfter=2024-04-05T15:30:45Z' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

### **Region版**

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/codeup/changeRequests?page=1&perPage=20&projectIds=2813489,2813490&authorIds=62c795xxxb468af8&reviewerIds=62c795xxxb468af8&state=opened&search=mr title&orderBy=updated_at&sort=desc&createdBefore=2024-04-05T15:30:45Z&createdAfter=2024-04-05T15:30:45Z' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | array |  |  |
| \- | object |  |  |
| author | object | 用户信息。 |  |
| avatar | string | 用户头像地址。 | https://example/example/w/100/h/100 |
| email | string | 用户邮箱。 | username@example.com |
| name | string | 用户名称。 | codeup-name |
| state | string | 用户状态：active - 激活可用；blocked - 阻塞暂不可用。 | active |
| userId | string | 云效用户 ID。 | 62c795xxxb468af8 |
| username | string | 用户登录名。 | codeup-username |
| createdAt | string | 创建时间。 | 2024-10-05T15:30:45Z |
| creationMethod | string | 合并请求的创建方式：WEB - 页面创建；COMMAND\_LINE - 命令行创建。 | WEB |
| description | string | 描述。 | mr description |
| detailUrl | string | 合并请求详情地址。 | https://example.com/example/example\_demo/change/1 |
| hasConflict | boolean | 是否有冲突。 | false |
| localId | integer | 合并请求局部 ID，表示当前代码库中第几个合并请求 ID。 | 1 |
| mergedRevision | string | 合并版本（提交 ID），仅已合并状态才有值。 | 6da8c14b5a9102998148b7ea35f96507d5304f74 |
| projectId | integer | 代码库 ID。 | 2813489 |
| reviewers | array | 评审人列表。 |  |
| \- | object |  |  |
| avatar | string | 用户头像地址。 | https://example/example/w/100/h/100 |
| email | string | 用户邮箱。 | username@example.com |
| hasCommented | boolean | 是否已经评论过。 | true |
| hasReviewed | boolean | 是否评审过。 | true |
| name | string | 用户名称。 | codeup-name |
| reviewOpinionStatus | string | 评审意见：PASS - 通过；NOT\_PASS - 不通过。 | PASS |
| reviewTime | string | 评审时间。 | 2024-10-05T15:30:45Z |
| state | string | 用户状态：active - 激活可用；blocked - 阻塞暂不可用。 | active |
| userId | string | 云效用户 ID。 | 62c795xxxb468af8 |
| username | string | 用户登录名。 | codeup-username |
| sourceBranch | string | 源分支。 | demo-branch |
| sourceProjectId | integer | 评审分支所在的代码库 ID。 | 2813489 |
| sourceType | string | 评审分支类型：BRANCH、COMMIT。 | BRANCH |
| sshUrl | string | 仓库 SSH 克隆地址。 | git@example:example\_org/example.git |
| state | string | 合并请求状态：UNDER\_DEV - 开发中；UNDER\_REVIEW - 评审中；TO\_BE\_MERGED - 待合并；CLOSED - 已关闭；MERGED - 已合并。 | UNDER\_REVIEW |
| supportMergeFFOnly | boolean | 是否支持 fast-forward-only 合并方式。 | true |
| targetBranch | string | 目标分支。 | master |
| targetProjectId | integer | 目标分支所在的代码库 ID。 | 2813489 |
| targetType | string | 目标分支类型：BRANCH、COMMIT。 | BRANCH |
| title | string | 标题。 | mr title |
| totalCommentCount | integer | 总评论数。 | 10 |
| unResolvedCommentCount | integer | 未解决评论数。 | 1 |
| updatedAt | string | 更新时间。 | 2024-10-05T15:30:45Z |
| webUrl | string | Web 地址。 | https://example.com/example/example\_demo/change/1 |
| workInProgress | boolean | WIP 标识，即是否在开发中。 | false |

## **返回示例**

`[ { "author": { "avatar": "https://example/example/w/100/h/100", "email": "username@example.com", "name": "codeup-name", "state": "active", "userId": "62c795xxxb468af8", "username": "codeup-username" }, "createdAt": "2024-10-05T15:30:45Z", "creationMethod": "WEB", "description": "mr description", "detailUrl": "https://example.com/example/example_demo/change/1", "hasConflict": false, "localId": 1, "mergedRevision": "6da8c14b5a9102998148b7ea35f96507d5304f74", "projectId": 2813489, "reviewers": [ { "avatar": "https://example/example/w/100/h/100", "email": "username@example.com", "hasCommented": true, "hasReviewed": true, "name": "codeup-name", "reviewOpinionStatus": "PASS", "reviewTime": "2024-10-05T15:30:45Z", "state": "active", "userId": "62c795xxxb468af8", "username": "codeup-username" } ], "sourceBranch": "demo-branch", "sourceProjectId": 2813489, "sourceType": "BRANCH", "sshUrl": "git@example:example_org/example.git", "state": "UNDER_REVIEW", "supportMergeFFOnly": true, "targetBranch": "master", "targetProjectId": 2813489, "targetType": "BRANCH", "title": "mr title", "totalCommentCount": 10, "unResolvedCommentCount": 1, "updatedAt": "2024-10-05T15:30:45Z", "webUrl": "https://example.com/example/example_demo/change/1", "workInProgress": false } ]`

## **响应头**

| **参数** | **描述** | **示例值** |
| --- | --- | --- |
| x-next-page | 下一页。 | 3 |
| x-page | 当前页。 | 2 |
| x-per-page | 每页大小。 | 20 |
| x-prev-page | 前一页。 | 1 |
| x-request-id | 请求 ID。 | 37294673-00CA-5B8B-914F-A8B35511E90A |
| x-total | 总数。 | 20 |
| x-total-pages | 总分页数。 | 3 |

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。