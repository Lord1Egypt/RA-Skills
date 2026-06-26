# GetCompare - 查询代码比较内容

通过 OpenAPI 可获取 branch、commit 或者 tag 之间的比较内容；注意，from 和 to 的顺序为 git 命令行执行的顺序，与 UI 页面的顺序相反，再者，比较时应该确保是相同类型比较，例如 branch 与 branch，commit 与 commit。

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 代码管理 | 代码比较 | 只读 |

## **请求语法**

### **中心版**

`GET https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/compares`

### **Region版**

```
GET https://{domain}/oapi/v1/codeup/repositories/{repositoryId}/compares
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
| from | string | query | 是 | 可为 CommitSHA、分支名或者标签名。 | master |
| to | string | query | 是 | 可为 CommitSHA、分支名或者标签名。 | dev\_branch |
| sourceType | string | query | 否 | 可选值：branch、tag；若是 commit 比较，可不传；若是分支比较，则需传入：branch，亦可不传，但需要确保不存在分支或 Tag 重名的情况；若是 tag 比较，则需传入：tag；若是存在分支和标签同名的情况，则需要严格传入 branch 或者 tag。 | branch |
| targetType | string | query | 否 | 可选值：branch、tag；若是 commit 比较，可不传；若是分支比较，则需传入：branch，亦可不传，但需要确保不存在分支或 Tag 重名的情况；若是 tag 比较，则需传入：tag；若是存在分支和标签同名的情况，则需要严格传入 branch 或者 tag。 | branch |
| straight | string | query | 否 | 是否使用 Merge-Base：straight=false，表示使用 Merge-Base；straight=true，表示不使用 Merge-Base；默认为 false，即使用 Merge-Base。 | false |

## **请求示例**

### **中心版**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/compares?from=master&to=dev_branch&sourceType=branch&targetType=branch&straight=false' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

### **Region版**

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/codeup/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/compares?from=master&to=dev_branch&sourceType=branch&targetType=branch&straight=false' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object |  |  |
| commits | array | 差异提交列表。 |  |
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
| shortId | string | 提交短 ID。 | 6da8c14b |
| title | string | 标题，提交的第一行内容。 | commit msg title |
| webUrl | string | 页面访问地址。 | http://exmaple.com/example\_repo/commit/commit\_sha |
| diffs | array | 差异内容。 |  |
| \- | object |  |  |
| aMode | string | 旧文件的模式标识，包含文件类型、权限等信息。 | 0 |
| bMode | string | 新文件的模式标识，包含文件类型、权限等信息。 | 100644 |
| deletedFile | boolean | 是否是删除文件。 | false |
| diff | string | 比较内容。 | \--- /dev/null\\n+++ b/asda\\n@@ -0,0 +1 @@\\n+asdasd\\n\\ No newline at end of file\\n |
| isBinary | boolean | 是否是二进制文件。 | false |
| newFile | boolean | 是否是新增文件。 | true |
| newId | string | 新文件的 git object id。 | 9118d6c90d0d80f906e70baf6af04a50ff660d7b |
| newPath | string | 新文件路径。 | src/test/main.java |
| oldId | string | 旧文件的 git object id。 | 0000000000000000000000000000000000000000 |
| oldPath | string | 旧文件路径。 | src/test/main.java |
| renamedFile | boolean | 是否是重命名文件。 | false |

## **返回示例**

`{ "commits": [ { "authorEmail": "username@example.com", "authorName": "codeup-name", "authoredDate": "2024-10-05T15:30:45Z", "committedDate": "2024-10-05T15:30:45Z", "committerEmail": "username@example.com", "committerName": "codeup-name", "id": "6da8c14b5a9102998148b7ea35f96507d5304f74", "message": "commit message detail", "parentIds": ["3fdaf119cf76539c1a47de0074ac02927ef4c8e1"], "shortId": "6da8c14b", "title": "commit msg title", "webUrl": "http://exmaple.com/example_repo/commit/commit_sha" } ], "diffs": [ { "aMode": "0", "bMode": "100644", "deletedFile": false, "diff": "--- /dev/null\n+++ b/asda\n@@ -0,0 +1 @@\n+asdasd\n\\ No newline at end of file\n", "isBinary": false, "newFile": true, "newId": "9118d6c90d0d80f906e70baf6af04a50ff660d7b", "newPath": "src/test/main.java", "oldId": "0000000000000000000000000000000000000000", "oldPath": "src/test/main.java", "renamedFile": false } ] }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。