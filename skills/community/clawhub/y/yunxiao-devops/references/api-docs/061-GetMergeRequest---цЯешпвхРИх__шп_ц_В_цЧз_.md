# GetMergeRequest - 查询合并请求(旧)

通过 OpenAPI 查询单个合并请求(旧)。

| **适用版本** | **中心版** |
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

`GET https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/mergeRequests/{iid}`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | 是 | 组织 ID。 | 60d54f3daccf2bbd6659f3ad |
| repositoryId | integer | path | 是 | 代码库 ID 或者 URL-Encoder 编码的全路径。 | 2813489或者60de7a6852743a5162b5f957%2FDemoRepo |
| iid | integer | path | 是 | 库内合并请求 ID。 | 1 |

## **请求示例**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/mergeRequests/1' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object |  |  |
| acceptedRevision | string | 评审通过时的版本。 | 6da8c14b5a9102998148b7ea35f96507d5304f74 |
| ahead | integer | 源分支领先目标分支的 commit 数量。 | 1 |
| assignees | array | 评审人列表。 |  |
| \- | object |  |  |
| avatar | string | 头像地址。 | https://example/example/w/100/h/100 |
| email | string | 邮箱。 | username@example.com |
| id | integer | 数据库主键 ID（无业务意义）。 | 1 |
| name | string | 用户名称。 | codeup-name |
| state | string | 用户状态，包括{active、blocked}，一般为 active。 | active |
| status | string | 评审人的评审状态，包括：approved - 评审通过，pending - 待处理，comment - 发表过评论、点赞等。 | approved |
| userId | string | 云效用户 ID（在 codeup 的 OpenAPI 中涉及到用户 ID 之处，均应使用该用户 ID）。 | 62c795xxxb468af8 |
| username | string | 用户名称（登录名）。 | codeup-username |
| author | object | 用户信息。 |  |
| avatar | string | 头像地址。 | https://example/example/w/100/h/100 |
| email | string | 邮箱。 | username@example.com |
| id | integer | 数据库主键 ID（无业务意义）。 | 1 |
| name | string | 用户名称。 | codeup-name |
| state | string | 用户状态，包括{active、blocked}，一般为 active。 | active |
| userId | string | 云效用户 ID（在 codeup 的 OpenAPI 中涉及到用户 ID 之处，均应使用该用户 ID）。 | 62c795xxxb468af8 |
| username | string | 用户名称（登录名）。 | codeup-username |
| behind | integer | 目标分支领先源分支的 commit 数量。 | 1 |
| createdAt | string | 创建时间。 | 2024-10-05T15:30:45Z |
| creationMethod | string | 创建方式，包括：WEB、COMMAND，默认创建方式为 WEB。 | WEB |
| description | string | 合并请求描述信息。 | mr description |
| detailUrl | string | 合并请求详情地址。 | https://example.com/example/example\_demo/merge\_requests/1 |
| downvotes | integer | 不通过投票数。 | 1 |
| id | integer | 合并请求 ID。 | 1 |
| iid | integer | 库内合并请求 ID，表示属于代码库内的第几个合并请求 ID。 | 1 |
| isUsePushBlock | boolean | 是否开启推送拦截。 | false |
| labels | array\[string\] | 标签（label）列表。 | \["BUG"\] |
| mergeStatus | string | 合并请求合并状态，包括：unchecked-未检查，can\_be\_merged-待合并，cannot\_be\_merged-不可合并。 | can\_be\_merged |
| mergedRevision | string | 合并的版本。 | 6da8c14b5a9102998148b7ea35f96507d5304f74 |
| nameWithNamespace | string | 代码库的全名称（包含父路径）。 | 60de7a6852743a5162b5f957 / DemoRepo（斜杠两侧有空格） |
| projectId | integer | 代码库 ID。 | 2813489 |
| sourceBranch | string | 源分支。 | demo-branch |
| sourceProjectId | integer | 评审分支所在的代码库 ID。 | 2813489 |
| sourceProjectName | string | 源库名称。 | Codeup-Demo |
| sourceType | string | 合并源类型，包括：BRANCH、COMMIT。 | BRANCH |
| sshUrlToRepo | string | 仓库 SSH 克隆地址。 | git@example:example\_org/example.git |
| state | string | 合并请求状态：opened-已开启，closed-已关闭，merged-已合并，accepted-评审通过，reopened-重新打开，locked-合并中。 | opened |
| subscribers | array | 订阅人列表。 |  |
| \- | object | 用户信息。 |  |
| avatar | string | 头像地址。 | https://example/example/w/100/h/100 |
| email | string | 邮箱。 | username@example.com |
| id | integer | 数据库主键 ID（无业务意义）。 | 1 |
| name | string | 用户名称。 | codeup-name |
| state | string | 用户状态，包括{active、blocked}，一般为 active。 | active |
| userId | string | 云效用户 ID（在 codeup 的 OpenAPI 中涉及到用户 ID 之处，均应使用该用户 ID）。 | 62c795xxxb468af8 |
| username | string | 用户名称（登录名）。 | codeup-username |
| supportMergeFFOnly | boolean | 是否支持 ff-only 合并方式。 | true |
| targetBranch | string | 目标分支。 | master |
| targetProjectId | integer | 目标分支所在的代码库 ID。 | 2813489 |
| targetProjectName | string | 目标库名称。 | Codeup-Demo |
| targetType | string | 合并目标类型，包括：BRANCH、COMMIT。 | BRANCH |
| title | string | 合并请求标题。 | mr title |
| updatedAt | string | 更新时间。 | 2024-10-05T15:30:45Z |
| upvotes | integer | 通过投票数。 | 1 |
| webUrl | string | web 地址。 | https://example.com/example/example\_demo/merge\_requests/1 |
| workInProgress | boolean | WIP 标识，即合并请求还处于开发中。 | false |

## **返回示例**

`{ "acceptedRevision": "6da8c14b5a9102998148b7ea35f96507d5304f74", "ahead": 1, "assignees": [ { "avatar": "https://example/example/w/100/h/100", "email": "username@example.com", "id": 1, "name": "codeup-name", "state": "active", "status": "approved", "userId": "62c795xxxb468af8", "username": "codeup-username" } ], "author": { "avatar": "https://example/example/w/100/h/100", "email": "username@example.com", "id": 1, "name": "codeup-name", "state": "active", "userId": "62c795xxxb468af8", "username": "codeup-username" }, "behind": 1, "createdAt": "2024-10-05T15:30:45Z", "creationMethod": "WEB", "description": "mr description", "detailUrl": "https://example.com/example/example_demo/merge_requests/1", "downvotes": 1, "id": 1, "iid": 1, "isUsePushBlock": false, "labels": ["BUG"], "mergeStatus": "can_be_merged", "mergedRevision": "6da8c14b5a9102998148b7ea35f96507d5304f74", "nameWithNamespace": "60de7a6852743a5162b5f957 / DemoRepo（斜杠两侧有空格）", "projectId": 2813489, "sourceBranch": "demo-branch", "sourceProjectId": 2813489, "sourceProjectName": "Codeup-Demo", "sourceType": "BRANCH", "sshUrlToRepo": "git@example:example_org/example.git", "state": "opened", "subscribers": [ { "avatar": "https://example/example/w/100/h/100", "email": "username@example.com", "id": 1, "name": "codeup-name", "state": "active", "userId": "62c795xxxb468af8", "username": "codeup-username" } ], "supportMergeFFOnly": true, "targetBranch": "master", "targetProjectId": 2813489, "targetProjectName": "Codeup-Demo", "targetType": "BRANCH", "title": "mr title", "updatedAt": "2024-10-05T15:30:45Z", "upvotes": 1, "webUrl": "https://example.com/example/example_demo/merge_requests/1", "workInProgress": false }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。