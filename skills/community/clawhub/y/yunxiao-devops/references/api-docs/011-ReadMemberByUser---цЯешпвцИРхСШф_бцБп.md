# ReadMemberByUser - 查询成员信息

通过 OpenAPI 查询成员信息。

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 组织管理 | 组织成员 | 只读 |

## **请求语法**

### **中心版**

`GET https://{domain}/oapi/v1/platform/organizations/{organizationId}/members:readByUser`

### **Region版**

```
GET https://{domain}/oapi/v1/platform/members:readByUser
```

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | -   是：中心版 -   否：Region版 | 组织 ID。 |  |
| userId | string | query | 是 | 用户 ID。 |  |

## **请求示例**

### **中心版**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/platform/organizations/{organizationId}/members:readByUser?userId={userId}' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

### **Region版**

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/platform/members:readByUser?userId={userId}' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object |  |  |
| deptIds | array\[string\] | 所属组织部门列表。 | \["99d1\*\*\*\*6124"\] |
| email | string | 邮箱。 | example@example.com |
| id | string | 成员 ID。 | 99d1\*\*\*\*6124 |
| joined | string | 加入时间。 | 2023-08-31T03:59:16.201Z |
| lastUpdated | string | 最后更新时间，等于数据库的更新时间。 | 2023-08-31T03:59:16.201Z |
| name | string | 成员名。 | 示例名 |
| organizationId | string | 组织 ID。 | 99d1\*\*\*\*6124 |
| roleIds | array\[string\] | 角色信息。 | \["99d1\*\*\*\*6124"\] |
| status | string | 成员状态，可选值：ENABLED,DISABLED,UNDELETED,DELETED,NORMAL\_USING,UNVISITED。 | ENABLED |
| userId | string | 用户 ID。 | 99d1\*\*\*\*6124 |
| visited | string | 最后访问时间。 | 2023-08-31T03:59:16.201Z |

## **返回示例**

`{ "deptIds": ["99d1****6124"], "email": "example@example.com", "id": "99d1****6124", "joined": "2023-08-31T03:59:16.201Z", "lastUpdated": "2023-08-31T03:59:16.201Z", "name": "示例名", "organizationId": "99d1****6124", "roleIds": ["99d1****6124"], "status": "ENABLED", "userId": "99d1****6124", "visited": "2023-08-31T03:59:16.201Z" }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。