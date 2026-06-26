# CreateCheckRun - 创建运行检查

通过 OpenAPI 创建或写入创建运行检查，但更新操作不能使用该接口。

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 代码管理 | 运行检查 | 读写 |

## **请求语法**

### **中心版**

`POST https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/checkRuns`

### **Region版**

```
POST https://{domain}/oapi/v1/codeup/repositories/{repositoryId}/checkRuns
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
| \- | object | body | 否 |  |  |
| annotations | array | body | 否 | 注解信息。 |  |
| \- | object | body | 否 |  |  |
| annotationLevel | string | body | 否 | 检查注解的等级：notice - 轻微；warning - 警告；failure - 严重。 | notice |
| endColumn | integer | body | 否 | 结束列，当且仅当 startLine=endLine 时，该字段值有效。 | 1 |
| endLine | integer | body | 否 | 结束行。 | 1 |
| message | string | body | 否 | 摘要信息。 | annotation message |
| path | string | body | 否 | 文件路径。 | src/test/main.java |
| rawDetails | string | body | 否 | 详情信息，限制64KB 以内。 | annotation raw details text |
| startColumn | integer | body | 否 | 起始列，当且仅当 startLine=endLine 时，该字段值有效。 | 1 |
| startLine | integer | body | 否 | 起始行，需要用户自行确认文件行数的有效性，否则无法展示，其余类似。 | 1 |
| title | string | body | 否 | 检查注解的标题。 | annotation title |
| completedAt | string | body | 否 | 三方检查的完结时间，格式为 ISO 8601，如2024-03-15T08:00:00Z。 | 2024-10-05T15:30:45Z |
| conclusion | string | body | 否 | 结论：cancelled - 已取消；failure - 失败；neutral - 中立状态，算作成功状态；success - 成功；skipped - 跳过，算作成功状态；timed\_out - 超时。 当直接写入 conclusion 时，status 自动设置为 completed。 | success |
| detailsUrl | string | body | 否 | 三方交互系统的详情地址，由用户自行决定，平台仅提供跳转能力。 | http://example.com |
| externalId | string | body | 否 | 外部系统的 ID，由用户自行决定写入的信息。 | 1 |
| headSha | string | body | 是 | 提交 ID，但需要确保该提交 ID 是某个新版合并请求的合并源。 | 6da8c14b5a9102998148b7ea35f96507d5304f74 |
| name | string | body | 是 | check run 的名称，长度限制在50以内。 | check run name |
| output | object | body | 否 |  |  |
| images | array | body | 否 | 可展示的图片，不超过3张。 |  |
| \- | object | body | 否 |  |  |
| alt | string | body | 否 | alt 文本信息。 | Test |
| caption | string | body | 否 | 图片信息的简要描述。 | Test Picture |
| imageUrl | string | body | 否 | 图片地址，须确保能够有效访问，否则页面无法加载。 | https://example/example/w/100/h/100 |
| summary | string | body | 否 | 摘要信息，支持 MarkDown 格式，最大字符长度为64KB，即65535个字符。 | check run output summary |
| text | string | body | 否 | 详情信息，支持 MarkDown 格式，最大字符长度为64KB，即65535个字符。 | check run output text |
| title | string | body | 否 | 标题。 | check run output title |
| startedAt | string | body | 否 | 三方检查的开始时间，格式为 ISO 8601，如2024-03-15T08:00:00Z。 | 2024-10-05T15:30:45Z |
| status | string | body | 否 | 状态：queued - 队列中；in\_progress - 运行中；completed - 已完成。当写入 completed 时，需要同时写入 conclusion。 | completed |

## **请求示例**

### **中心版**

`curl -X 'POST' \ 'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/checkRuns' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "annotations": [ { "annotationLevel": "notice", "endColumn": 1, "endLine": 1, "message": "annotation message", "path": "src/test/main.java", "rawDetails": "annotation raw details text", "startColumn": 1, "startLine": 1, "title": "annotation title" } ], "completedAt": "2024-10-05T15:30:45Z", "conclusion": "success", "detailsUrl": "http://example.com", "externalId": "1", "headSha": "6da8c14b5a9102998148b7ea35f96507d5304f74", "name": "check run name", "output": { "images": [ { "alt": "Test", "caption": "Test Picture", "imageUrl": "https://example/example/w/100/h/100" } ], "summary": "check run output summary", "text": "check run output text", "title": "check run output title" }, "startedAt": "2024-10-05T15:30:45Z", "status": "completed" }'`

### **Region版**

```
curl -X 'POST' \
  'https://{domain}/oapi/v1/codeup/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/checkRuns' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \
  --data '
    {
        "annotations": [
            {
                "annotationLevel": "notice",
                "endColumn": 1,
                "endLine": 1,
                "message": "annotation message",
                "path": "src/test/main.java",
                "rawDetails": "annotation raw details text",
                "startColumn": 1,
                "startLine": 1,
                "title": "annotation title"
            }
        ],
        "completedAt": "2024-10-05T15:30:45Z",
        "conclusion": "success",
        "detailsUrl": "http://example.com",
        "externalId": "1",
        "headSha": "6da8c14b5a9102998148b7ea35f96507d5304f74",
        "name": "check run name",
        "output": {
            "images": [
                {
                    "alt": "Test",
                    "caption": "Test Picture",
                    "imageUrl": "https://example/example/w/100/h/100"
                }
            ],
            "summary": "check run output summary",
            "text": "check run output text",
            "title": "check run output title"
        },
        "startedAt": "2024-10-05T15:30:45Z",
        "status": "completed"
    }'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object |  |  |
| annotations | array | 注解信息。 |  |
| \- | object |  |  |
| annotationLevel | string | 检查注解的等级：notice - 轻微；warning - 警告；failure - 严重。 | notice |
| createdAt | string | 创建时间。 | 2024-10-05T15:30:45Z |
| endColumn | integer | 结束列，当且仅当 startLine=endLine 时，该字段值有效。 | 2 |
| endLine | integer | 结束行。 | 2 |
| id | integer | 检查注解 ID，唯一标识。 | 1 |
| message | string | 摘要信息。 | check run annotation message |
| path | string | 文件路径。 | src/test/main.java |
| rawDetails | string | 详情信息，限制64KB 以内。 | check run annotation raw details text |
| startColumn | integer | 起始列，当且仅当 startLine=endLine 时，该字段值有效。 | 1 |
| startLine | integer | 起始行，需要用户自行确认文件行数的有效性，否则无法展示，其余类似。 | 1 |
| title | string | 检查注解的标题。 | check run annotation title |
| updatedAt | string | 更新时间。 | 2024-10-05T15:30:45Z |
| checkSuite | object | 检查套件信息。 |  |
| id | integer | 唯一标识。 | 1 |
| completedAt | string | 三方检查的完成时间。 | 2024-10-05T15:30:45Z |
| conclusion | string | 结论：cancelled - 已取消；failure - 失败；neutral - 中立状态，算作成功状态；success - 成功；skipped - 跳过，算作成功状态；timed\_out - 超时。 | success |
| createdAt | string | 回写记录的创建时间。 | 2024-10-05T15:30:45Z |
| detailsUrl | string | 三方交互系统的链接地址，由用户自行决定，平台仅提供跳转能力。 | http://example.test |
| externalId | string | 外部系统 ID。 | 1 |
| headSha | string | 提交 ID。 | 6da8c14b5a9102998148b7ea35f96507d5304f74 |
| id | integer | 唯一标识。 | 1 |
| name | string | check run 的名称。 | Test Check Run |
| output | object | 页面展示信息。 |  |
| images | array | 可展示的图片，不超过3张。 |  |
| \- | object |  |  |
| alt | string | alt 文本信息。 | Test |
| caption | string | 图片信息的简要描述。 | alt caption |
| imageUrl | string | 图片地址，须确保能够有效访问，否则页面无法加载。 | https://example/example/w/100/h/100 |
| summary | string | 摘要信息，支持 MarkDown 格式，最大字符长度为64KB，即65535个字符。 | check run summary |
| text | string | 详情信息，支持 MarkDown 格式，最大字符长度为64KB，即65535个字符。 | check run markdown content text |
| title | string | 标题。 | check run title |
| startedAt | string | 三方检查的开始时间。 | 2024-10-05T15:30:45Z |
| status | string | 状态：queued - 队列中；in\_progress - 运行中；completed - 完成。 | completed |
| updatedAt | string | 回写记录的更新时间。 | 2024-10-05T15:30:45Z |
| writer | object | 写入人信息。 |  |
| id | string | 用户 ID。 | 62c795xxxb468af8 |
| logoUrl | string | 用户头像地址。 | https://example/example/w/100/h/100 |
| name | string | 用户名称。 | codeup-name |
| slug | string | 用户登录名。 | codeup-username |
| type | string | 写入人类型：User - 用户；Bot - 应用（暂无）。 | User |

## **返回示例**

`{ "annotations": [ { "annotationLevel": "notice", "createdAt": "2024-10-05T15:30:45Z", "endColumn": 2, "endLine": 2, "id": 1, "message": "check run annotation message", "path": "src/test/main.java", "rawDetails": "check run annotation raw details text", "startColumn": 1, "startLine": 1, "title": "check run annotation title", "updatedAt": "2024-10-05T15:30:45Z" } ], "checkSuite": { "id": 1 }, "completedAt": "2024-10-05T15:30:45Z", "conclusion": "success", "createdAt": "2024-10-05T15:30:45Z", "detailsUrl": "http://example.test", "externalId": "1", "headSha": "6da8c14b5a9102998148b7ea35f96507d5304f74", "id": 1, "name": "Test Check Run", "output": { "images": [ { "alt": "Test", "caption": "alt caption", "imageUrl": "https://example/example/w/100/h/100" } ], "summary": "check run summary", "text": "check run markdown content text", "title": "check run title" }, "startedAt": "2024-10-05T15:30:45Z", "status": "completed", "updatedAt": "2024-10-05T15:30:45Z", "writer": { "id": "62c795xxxb468af8", "logoUrl": "https://example/example/w/100/h/100", "name": "codeup-name", "slug": "codeup-username", "type": "User" } }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。