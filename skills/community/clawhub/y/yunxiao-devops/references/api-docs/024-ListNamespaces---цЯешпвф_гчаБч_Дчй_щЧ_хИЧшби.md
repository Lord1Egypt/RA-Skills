# ListNamespaces - 查询代码组空间列表

通过 OpenAPI 查询代码组空间列表，有分页，无排序；可通过该接口来查询代码组列表。

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 代码管理 | 代码组 | 只读 |

## **请求语法**

### **中心版**

`GET https://{domain}/oapi/v1/codeup/organizations/{organizationId}/namespaces`

### **Region版**

```
GET https://{domain}/oapi/v1/codeup/namespaces
```

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | -   是：中心版 -   否：Region版 | 组织 ID。 | 60d54f3daccf2bbd6659f3ad |
| parentId | integer | query | 否 | 父组空间 ID，若是查询组织下当前用户的组空间列表，可设置为空。 | 1 |
| page | integer | query | 否 | 页码，默认从1开始，一般不要超过150页。 | 1 |
| perPage | integer | query | 否 | 每页大小，默认20，取值范围【1，100】。 | 20 |
| search | string | query | 否 | 搜索关键字。 | Test |
| orderBy | string | query | 否 | 排序字段，可选值包括 {created\_at, updated\_at}，默认值为 updated\_at。 | updated\_at |
| sort | string | query | 否 | 排序方式，可选值包括{asc, desc}，默认值为 desc。 | desc |

## **请求示例**

### **中心版**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/namespaces?parentId=1&page=1&perPage=20&search=Test&orderBy=updated_at&sort=desc' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

### **Region版**

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/codeup/namespaces?parentId=1&page=1&perPage=20&search=Test&orderBy=updated_at&sort=desc' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | array |  |  |
| \- | object |  |  |
| avatarUrl | string | 头像地址。 | https://example/example/w/100/h/100 |
| fullPath | string | 空间完整路径。 | 60de7a6852743a5162b5f957/DemoGroup |
| id | integer | ID。 | 1 |
| kind | string | 默认取值为 group。 | group |
| name | string | 名称。 | DemoGroup |
| nameWithNamespace | string | 完整名称。 | 60de7a6852743a5162b5f957 / DemoGroup |
| parentId | integer | 上级路径的 ID。 | 2 |
| path | string | 路径。 | DemoGroup |
| pathWithNamespace | string | 完整路径。 | 60de7a6852743a5162b5f957/DemoGroup |
| visibility | string | 可见性，包括{private-私有，internal-组织内公开，public-公开}，可能的值：\[private internal public\]。 | private |
| webUrl | string | 页面访问时的 URL。 | http://example.com/60de7a6852743a5162b5f957/DemoGroup |

## **返回示例**

`[ { "avatarUrl": "https://example/example/w/100/h/100", "fullPath": "60de7a6852743a5162b5f957/DemoGroup", "id": 1, "kind": "group", "name": "DemoGroup", "nameWithNamespace": "60de7a6852743a5162b5f957 / DemoGroup", "parentId": 2, "path": "DemoGroup", "pathWithNamespace": "60de7a6852743a5162b5f957/DemoGroup", "visibility": "private", "webUrl": "http://example.com/60de7a6852743a5162b5f957/DemoGroup" } ]`

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