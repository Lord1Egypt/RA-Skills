# GetChangeRequestTree - 查询合并请求的变更文件树

通过 OpenAPI 查询合并请求的变更文件树，包含变更行数信息。

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

`GET https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/changeRequests/{localId}/diffs/changeTree`

### **Region版**

```
GET https://{domain}/oapi/v1/codeup/repositories/{repositoryId}/changeRequests/{localId}/diffs/changeTree
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
| localId | integer | path | 是 | 局部 ID。 | 1 |
| fromPatchSetId | string | query | 是 | 合并目标对应的版本唯一 ID（from 和 to，是 git 的对比顺序，与通常的源分支和目标分支的顺序相反）。 | bf117304dfe44d5d9b1132f348edf92e |
| toPatchSetId | string | query | 是 | 合并源对应的版本唯一 ID（from 和 to，是 git 的对比顺序，与通常的源分支和目标分支的顺序相反）。 | 537367017a9841738ac4269fbf6aacbe |

## **请求示例**

### **中心版**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/changeRequests/1/diffs/changeTree?fromPatchSetId=bf117304dfe44d5d9b1132f348edf92e&toPatchSetId=537367017a9841738ac4269fbf6aacbe' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

### **Region版**

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/codeup/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/changeRequests/1/diffs/changeTree?fromPatchSetId=bf117304dfe44d5d9b1132f348edf92e&toPatchSetId=537367017a9841738ac4269fbf6aacbe' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object |  |  |
| changedTreeItems | array | 变更文件列表。 |  |
| \- | object |  |  |
| aMode | string | 旧文件模式。 | 100644 |
| addLines | integer | 新增行数。 | 1 |
| bMode | string | 新文件模式。 | 100644 |
| delLines | integer | 删除行数。 | 1 |
| deletedFile | string | 是否是删除文件。 | false |
| isBinary | boolean | 是否是二进制文件。 | false |
| newFile | boolean | 是否是新建文件。 | false |
| newObjectId | string | 新文件 git object id。 | 9cc84ea9b4d95453115d0c26488d6a78694e0bc6 |
| newPath | string | 新文件路径。 | src/test/main.java |
| oldObjectId | string | 旧文件 git object id。 | b573bb50d56e8c19282593cbf5b081e211923a83 |
| oldPath | string | 旧文件路径。 | src/test/main.java |
| renamedFile | string | 是否是重命名文件。 | false |
| count | integer | 总变更文件数。 | 1 |
| totalAddLines | integer | 总增加行数。 | 10 |
| totalDelLines | integer | 总删除行数。 | 10 |

## **返回示例**

`{ "changedTreeItems": [ { "aMode": "100644", "addLines": 1, "bMode": "100644", "delLines": 1, "deletedFile": "false", "isBinary": false, "newFile": false, "newObjectId": "9cc84ea9b4d95453115d0c26488d6a78694e0bc6", "newPath": "src/test/main.java", "oldObjectId": "b573bb50d56e8c19282593cbf5b081e211923a83", "oldPath": "src/test/main.java", "renamedFile": "false" } ], "count": 1, "totalAddLines": 10, "totalDelLines": 10 }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。