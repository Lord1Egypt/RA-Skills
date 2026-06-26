# CreateRepository - 创建代码库

通过 OpenAPI 创建代码库。

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 代码管理 | 代码仓库 | 读写 |

## **请求语法**

### **中心版**

`POST https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories`

### **Region版**

```
POST https://{domain}/oapi/v1/codeup/repositories
```

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | -   是：中心版 -   否：Region版 | 组织 ID。 | 60d54f3daccf2bbd6659f3ad |
| createParentPath | boolean | query | 否 | 是否自动创建父路径。 | true |
| \- | object | body | 否 |  |  |
| avatarUrl | string | body | 否 | 代码库头像地址。 | https://example/example/w/100/h/100 |
| description | string | body | 否 | 代码库描述内容，最长不差过65535个字符。 | 描述内容 |
| name | string | body | 是 | 代码库名称。 | demo-repo |
| namespaceId | integer | body | 否 | 代码库父路径 ID，若为空，则创建在组织路径下。 | 2813489 |
| path | string | body | 是 | 代码库路径。 | demo-repo |
| readMeType | string | body | 否 | 自动创建 readme 类型: EMPTY - 空，USER\_GUIDE - 引导 readme 文件。 | USER\_GUIDE |
| templateProject | object | body | 否 |  |  |
| syncAllBranches | boolean | body | 否 | 是否导入模板库所有分支。 | true |
| templateProjectId | integer | body | 否 | 模板库 ID。 | 1 |
| templateType | integer | body | 否 | 模板类型，1-自定义模板，2-系统预置模板。 | 1 |
| visibility | string | body | 否 | 代码库的可见性: private - 私有，internal - 组织内公开，public：公开。 | private |

## **请求示例**

### **中心版**

`curl -X 'POST' \ 'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/repositories?createParentPath=true' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "avatarUrl": "https://example/example/w/100/h/100", "description": "描述内容", "name": "demo-repo", "namespaceId": 2813489, "path": "demo-repo", "readMeType": "USER_GUIDE", "templateProject": { "syncAllBranches": true, "templateProjectId": 1, "templateType": 1 }, "visibility": "private" }'`

### **Region版**

```
curl -X 'POST' \
  'https://{domain}/oapi/v1/codeup/repositories?createParentPath=true' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \
  --data '
    {
        "avatarUrl": "https://example/example/w/100/h/100",
        "description": "描述内容",
        "name": "demo-repo",
        "namespaceId": 2813489,
        "path": "demo-repo",
        "readMeType": "USER_GUIDE",
        "templateProject": {
            "syncAllBranches": true,
            "templateProjectId": 1,
            "templateType": 1
        },
        "visibility": "private"
    }'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object |  |  |
| accessLevel | integer | 当前用户在该代码库上的权限类型，可能的值：\[20 30 40\]。 | 40 |
| archived | boolean | 代码库是否归档。 | false |
| avatarUrl | string | 头像地址。 | https://example/example/w/100/h/100 |
| createdAt | string | 创建时间。 | 2024-10-05T15:30:45Z |
| creatorId | integer | 代码库创建者。 | 1 |
| demoProject | boolean | 是否是 demo 库。 | false |
| description | string | 代码库描述。 | demo repo |
| encrypted | boolean | 是否加密。 | false |
| id | integer | 代码库 ID。 | 2813489 |
| lastActivityAt | string | 最后活跃时间。 | 2024-10-05T15:30:45Z |
| name | string | 代码库名称。 | demo-repo |
| nameWithNamespace | string | 代码库完整名称（含完整组名称）。 | 60de7a6852743a5162b5f957 / DemoRepo |
| namespaceId | integer | 上级路径的 ID。 | 2813489 |
| path | string | 代码库路径。 | demo-repo |
| pathWithNamespace | string | 代码库完整路径（含完整组路径）。 | 60de7a6852743a5162b5f957/DemoRepo |
| repositorySize | string | 代码库大小(MB)。 | 1 |
| starCount | integer | 被收藏的数量。 | 1 |
| starred | boolean | 是否被当前用户收藏。 | false |
| updatedAt | string | 最近更新时间。 | 2024-10-05T15:30:45Z |
| visibility | string | 可见性,private 标识私有的，internal 标识组织内公开，public 表示全平台公开，可能的值：\[private internal public\]。 | private |
| webUrl | string | 页面访问时的 URL。 | http://example.com/org-demo/example-repo |

## **返回示例**

`{ "accessLevel": 40, "archived": false, "avatarUrl": "https://example/example/w/100/h/100", "createdAt": "2024-10-05T15:30:45Z", "creatorId": 1, "demoProject": false, "description": "demo repo", "encrypted": false, "id": 2813489, "lastActivityAt": "2024-10-05T15:30:45Z", "name": "demo-repo", "nameWithNamespace": "60de7a6852743a5162b5f957 / DemoRepo", "namespaceId": 2813489, "path": "demo-repo", "pathWithNamespace": "60de7a6852743a5162b5f957/DemoRepo", "repositorySize": "1", "starCount": 1, "starred": false, "updatedAt": "2024-10-05T15:30:45Z", "visibility": "private", "webUrl": "http://example.com/org-demo/example-repo" }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。