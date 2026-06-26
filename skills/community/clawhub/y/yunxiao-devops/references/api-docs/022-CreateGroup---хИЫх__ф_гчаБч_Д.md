# CreateGroup - 创建代码组

通过 OpenAPI 创建代码组。

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 代码管理 | 代码组 | 读写 |

## **请求语法**

### **中心版**

`POST https://{domain}/oapi/v1/codeup/organizations/{organizationId}/groups`

### **Region版**

```
POST https://{domain}/oapi/v1/codeup/groups
```

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | -   是：中心版 -   否：Region版 | 组织 ID。 | 60d54f3daccf2bbd6659f3ad |
| \- | object | body | 否 |  |  |
| avatar | string | body | 否 | 代码组头像地址。 | https://example/example/w/100/h/100 |
| description | string | body | 否 | 代码组描述内容，最长不差过65535个字符。 | group description |
| name | string | body | 是 | 代码组名称。 | DemoGroup |
| parentId | integer | body | 否 | 代码组父路径 ID，若为空，则创建在组织路径下。 | 1 |
| path | string | body | 是 | 代码组路径。 | DemoGroup |
| visibility | string | body | 否 | 代码组的可见性，包括{private-私有，internal-组织内公开，public-公开}。 | private |

## **请求示例**

### **中心版**

`curl -X 'POST' \ 'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/groups' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "avatar": "https://example/example/w/100/h/100", "description": "group description", "name": "DemoGroup", "parentId": 1, "path": "DemoGroup", "visibility": "private" }'`

### **Region版**

```
curl -X 'POST' \
  'https://{domain}/oapi/v1/codeup/groups' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \
  --data '
    {
        "avatar": "https://example/example/w/100/h/100",
        "description": "group description",
        "name": "DemoGroup",
        "parentId": 1,
        "path": "DemoGroup",
        "visibility": "private"
    }'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object |  |  |
| avatarUrl | string | 头像地址。 | https://example/example/w/100/h/100 |
| description | string | 代码组描述信息。 | group description |
| id | integer | 代码组 ID，也可作为代码空间 ID 使用。 | 1 |
| name | string | 代码组名称。 | DemoRepo |
| nameWithNamespace | string | 代码组完整名称。 | 60de7a6852743a5162b5f957 / DemoRepo |
| ownerId | integer | 代码组创建者。 | null |
| parentId | integer | 上级路径的 ID。 | 2 |
| path | string | 代码组路径。 | DemoRepo |
| pathWithNamespace | string | 代码组完整路径。 | 60de7a6852743a5162b5f957/DemoRepo |
| visibility | string | 可见性,private 标识私有的，internal 标识组织内公开，public 表示全平台公开，可能的值：\[private internal public\]。 | private |
| webUrl | string | 页面访问时的 URL。 | http://example/60de7a6852743a5162b5f957/DemoRepo |

## **返回示例**

`{ "avatarUrl": "https://example/example/w/100/h/100", "description": "group description", "id": 1, "name": "DemoRepo", "nameWithNamespace": "60de7a6852743a5162b5f957 / DemoRepo", "ownerId": null, "parentId": 2, "path": "DemoRepo", "pathWithNamespace": "60de7a6852743a5162b5f957/DemoRepo", "visibility": "private", "webUrl": "http://example/60de7a6852743a5162b5f957/DemoRepo" }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。