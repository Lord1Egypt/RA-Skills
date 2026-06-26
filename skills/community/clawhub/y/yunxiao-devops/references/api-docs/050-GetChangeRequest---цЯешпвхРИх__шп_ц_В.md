# GetChangeRequest - 查询合并请求

通过 OpenAPI 查询合并请求详情。

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

`GET https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/changeRequests/{localId}`

### **Region版**

```
GET https://{domain}/oapi/v1/codeup/repositories/{repositoryId}/changeRequests/{localId}
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

## **请求示例**

### **中心版**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/changeRequests/1' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

### **Region版**

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/codeup/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/changeRequests/1' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object |  |  |
| ahead | integer | 源分支领先目标分支的 commit 数量。 | 1 |
| allRequirementsPass | boolean | 是否所有卡点项通过。 | true |
| author | object | 用户信息。 |  |
| avatar | string | 用户头像地址。 | https://example/example/w/100/h/100 |
| email | string | 用户邮箱。 | username@example.com |
| name | string | 用户名称。 | codeup-name |
| state | string | 用户状态：active - 激活可用；blocked - 阻塞暂不可用。 | active |
| userId | string | 云效用户 ID。 | 62c795xxxb468af8 |
| username | string | 用户登录名。 | codeup-username |
| behind | integer | 目标分支领先源分支的 commit 数量。 | 1 |
| canRevertOrCherryPick | boolean | 是否能 Revert 或者 CherryPick。 | true |
| conflictCheckStatus | string | 冲突检测状态：CHECKING - 检测中；HAS\_CONFLICT - 有冲突；NO\_CONFLICT - 无冲突；FAILED - 检测失败。 | NO\_CONFLICT |
| createFrom | string | 创建来源：WEB - 页面创建；COMMAND\_LINE - 命令行创建。 | WEB |
| createTime | string | 创建时间。 | 2024-10-05T15:30:45Z |
| description | string | 描述。 | mr description |
| detailUrl | string | 合并请求详情地址。 | https://example.com/example/example\_demo/change/1 |
| hasReverted | boolean | 是否 Revert 过。 | false |
| localId | integer | 局部 ID。 | 1 |
| mergedRevision | string | 合并版本（提交 ID），仅已合并状态才有值。 | 6da8c14b5a9102998148b7ea35f96507d5304f74 |
| mrType | string | 合并请求类型：CODE\_REVIEW - 代码评审；REF\_REVIEW - 分支标签评审。 | CODE\_REVIEW |
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
| sourceProjectId | integer | 源库 ID。 | 2813489 |
| status | string | 合并请求状态：UNDER\_DEV - 开发中；UNDER\_REVIEW - 评审中；TO\_BE\_MERGED - 待合并；CLOSED - 已关闭；MERGED - 已合并。 | UNDER\_REVIEW |
| subscribers | array | 订阅人列表。 |  |
| \- | object | 用户信息。 |  |
| avatar | string | 用户头像地址。 | https://example/example/w/100/h/100 |
| email | string | 用户邮箱。 | username@example.com |
| name | string | 用户名称。 | codeup-name |
| state | string | 用户状态：active - 激活可用；blocked - 阻塞暂不可用。 | active |
| userId | string | 云效用户 ID。 | 62c795xxxb468af8 |
| username | string | 用户登录名。 | codeup-username |
| supportMergeFastForwardOnly | boolean | 是否支持 fast-forward-only。 | true |
| targetBranch | string | 目标分支。 | master |
| targetProjectId | integer | 目标库 ID。 | 2813489 |
| targetProjectNameWithNamespace | string | 目标库名称（含完整父路径）。 | 60de7a6852743a5162b5f957 / DemoRepo（斜杠两侧有空格） |
| targetProjectPathWithNamespace | string | 目标库路径（含完整父路径）。 | 60de7a6852743a5162b5f957/DemoRepo |
| title | string | 标题。 | mr title |
| totalCommentCount | integer | 总评论数。 | 1 |
| unResolvedCommentCount | integer | 未解决评论数。 | 1 |
| updateTime | string | 更新时间。 | 2024-10-05T15:30:45Z |
| webUrl | string | 页面地址。 | https://example.com/example/example\_demo/change/1 |

## **返回示例**

`{ "ahead": 1, "allRequirementsPass": true, "author": { "avatar": "https://example/example/w/100/h/100", "email": "username@example.com", "name": "codeup-name", "state": "active", "userId": "62c795xxxb468af8", "username": "codeup-username" }, "behind": 1, "canRevertOrCherryPick": true, "conflictCheckStatus": "NO_CONFLICT", "createFrom": "WEB", "createTime": "2024-10-05T15:30:45Z", "description": "mr description", "detailUrl": "https://example.com/example/example_demo/change/1", "hasReverted": false, "localId": 1, "mergedRevision": "6da8c14b5a9102998148b7ea35f96507d5304f74", "mrType": "CODE_REVIEW", "projectId": 2813489, "reviewers": [ { "avatar": "https://example/example/w/100/h/100", "email": "username@example.com", "hasCommented": true, "hasReviewed": true, "name": "codeup-name", "reviewOpinionStatus": "PASS", "reviewTime": "2024-10-05T15:30:45Z", "state": "active", "userId": "62c795xxxb468af8", "username": "codeup-username" } ], "sourceBranch": "demo-branch", "sourceProjectId": 2813489, "status": "UNDER_REVIEW", "subscribers": [ { "avatar": "https://example/example/w/100/h/100", "email": "username@example.com", "name": "codeup-name", "state": "active", "userId": "62c795xxxb468af8", "username": "codeup-username" } ], "supportMergeFastForwardOnly": true, "targetBranch": "master", "targetProjectId": 2813489, "targetProjectNameWithNamespace": "60de7a6852743a5162b5f957 / DemoRepo（斜杠两侧有空格）", "targetProjectPathWithNamespace": "60de7a6852743a5162b5f957/DemoRepo", "title": "mr title", "totalCommentCount": 1, "unResolvedCommentCount": 1, "updateTime": "2024-10-05T15:30:45Z", "webUrl": "https://example.com/example/example_demo/change/1" }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。