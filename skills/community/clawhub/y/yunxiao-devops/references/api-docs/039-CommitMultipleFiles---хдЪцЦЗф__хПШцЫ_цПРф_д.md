# CommitMultipleFiles - 多文件变更提交

通过 OpenAPI 多文件变更提交。

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 代码管理 | 文件 |  |

## **请求语法**

### **中心版**

`POST https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/multipleFiles`

### **Region版**

```
POST https://{domain}/oapi/v1/codeup/repositories/{repositoryId}/multipleFiles
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
| actions | array | body | 否 |  |  |
| \- | object | body | 否 |  |  |
| action | string | body | 否 | 操作类型  -   create：创建文件 -   delete：删除文件 -   move：移动文件 -   update：更新文件  。 | create |
| content | string | body | 否 | 文件内容  > 注意：若是更新操作，则是完全覆盖，即传入的 content 内容，会直接覆盖原有的文件内容  。 | xxx |
| file\_path | string | body | 否 | 文件路径。 | src/test.java |
| previous\_path | string | body | 否 | 变更前的文件路径。 | src/main/test.java |
| branch | string | body | 否 | 分支名称。 | demo-branch |
| commit\_message | string | body | 否 | 提交信息，非空，不超过102400个字符。 | create a file with content |

## **请求示例**

### **中心版**

`curl -X 'POST' \ 'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/multipleFiles' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "actions": [ { "action": "create", "content": "xxx", "file_path": "src/test.java", "previous_path": "src/main/test.java" } ], "branch": "demo-branch", "commit_message": "create a file with content" }'`

### **Region版**

```
curl -X 'POST' \
  'https://{domain}/oapi/v1/codeup/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/multipleFiles' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \
  --data '
    {
        "actions": [
            {
                "action": "create",
                "content": "xxx",
                "file_path": "src/test.java",
                "previous_path": "src/main/test.java"
            }
        ],
        "branch": "demo-branch",
        "commit_message": "create a file with content"
    }'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
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

`{ "authorEmail": "username@example.com", "authorName": "codeup-name", "authoredDate": "2024-10-05T15:30:45Z", "committedDate": "2024-10-05T15:30:45Z", "committerEmail": "username@example.com", "committerName": "codeup-name", "id": "6da8c14b5a9102998148b7ea35f96507d5304f74", "message": "commit message detail", "parentIds": ["3fdaf119cf76539c1a47de0074ac02927ef4c8e1"], "shortId": "6da8c14b", "title": "commit msg title", "webUrl": "http://exmaple.com/example_repo/commit/commit_sha" }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。