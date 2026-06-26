# ListTemplateRepositories - 查询模板代码库列表

通过 OpenAPI 查询模板代码库列表。

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 代码管理 | 代码仓库 | 只读 |

## **请求语法**

### **中心版**

`GET https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/templates`

### **Region版**

```
GET https://{domain}/oapi/v1/codeup/repositories/templates
```

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | -   是：中心版 -   否：Region版 | 组织 ID。 | 60d54f3daccf2bbd6659f3ad |
| page | integer | query | 否 | 页码，默认从1开始，一般不要超过150页。 | 1 |
| perPage | integer | query | 否 | 每页大小，默认20，取值范围【1，100】。 | 20 |
| templateType | integer | query | 是 | 模板类型，1-自定义模板库，2-系统内置模板库。 | 2 |

## **请求示例**

### **中心版**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/repositories/templates?page=1&perPage=20&templateType=2' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

### **Region版**

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/codeup/repositories/templates?page=1&perPage=20&templateType=2' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | array |  |  |
| \- | object |  |  |
| avatarUrl | string | 代码库头像链接。 | https://example/example/w/100/h/100 |
| description | string | 代码库描述内容。 | 模板库的描述内容 |
| name | string | 代码库名称。 | template-repo |
| path | string | 代码库全路径，但若是系统预置模板库，则该属性为 null。 | null |
| projectId | integer | 模板仓库 ID。 | 1 |

## **返回示例**

`[ { "avatarUrl": "https://example/example/w/100/h/100", "description": "模板库的描述内容", "name": "template-repo", "path": "null", "projectId": 1 } ]`

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