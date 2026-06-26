# ListBindInfo - 列出组织成员特定类型的绑定信息

通过 OpenAPI 列出组织内所有成员的特定类型绑定信息。

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 组织管理 | 组织绑定 | 只读 |

## **请求语法**

### **中心版**

`GET https://{domain}/oapi/v1/platform/organizations/{organizationId}/members/binds/{bindType}`

### **Region版**

```
GET https://{domain}/oapi/v1/platform/members/binds/{bindType}
```

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | -   是：中心版 -   否：Region版 | 组织 ID。 |  |
| bindType | string | path | 是 | 绑定类型。 |  |
| page | integer | query | 否 | 当前页，默认1。 |  |
| perPage | integer | query | 否 | 每页数据条数，默认100。 |  |

## **请求示例**

### **中心版**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/platform/organizations/{organizationId}/members/binds/{bindType}?page={page}&perPage={perPage}' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

### **Region版**

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/platform/members/binds/{bindType}?page={page}&perPage={perPage}' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | array |  |  |
| \- | object |  |  |
| binds | array | 绑定信息。 |  |
| \- | object |  |  |
| bindId | string | 绑定 ID。 | 99d1\*\*\*\*6124 |
| bindType | string | 绑定类型。 | saml |
| name | string | 绑定显示名称。 | name |
| memberId | string | 成员 ID。 | 99d1\*\*\*\*6124 |
| userId | string | 用户 ID。 | 99d1\*\*\*\*6124 |

## **返回示例**

`[ { "binds": [ { "bindId": "99d1****6124", "bindType": "saml", "name": "name" } ], "memberId": "99d1****6124", "userId": "99d1****6124" } ]`

## **响应头**

| **参数** | **描述** | **示例值** |
| --- | --- | --- |
| x-next-page | 下一页。 |  |
| x-page | 当前页。 |  |
| x-per-page | 每页数据条数。 |  |
| x-prev-page | 上一页。 |  |
| x-total | 总数据量。 |  |
| x-total-pages | 总分页数。 |  |

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。