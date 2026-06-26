# GetBindInfo - 获取单个成员绑定信息

通过 OpenAPI 获取一个成员的所有绑定信息。

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

`GET https://{domain}/oapi/v1/platform/organizations/{organizationId}/members/{memberId}/binds`

### **Region版**

```
GET https://{domain}/oapi/v1/platform/members/{memberId}/binds
```

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | -   是：中心版 -   否：Region版 | 组织 ID。 |  |
| memberId | string | path | 是 | 成员 ID。 |  |

## **请求示例**

### **中心版**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/platform/organizations/{organizationId}/members/{memberId}/binds' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

### **Region版**

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/platform/members/{memberId}/binds' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object |  |  |
| binds | array | 绑定信息。 |  |
| \- | object |  |  |
| bindId | string | 绑定 ID。 | 99d1\*\*\*\*6124 |
| bindType | string | 绑定类型。 | saml |
| name | string | 绑定显示名称。 | name |
| memberId | string | 成员 ID。 | 99d1\*\*\*\*6124 |
| userId | string | 用户 ID。 | 99d1\*\*\*\*6124 |

## **返回示例**

`{ "binds": [ { "bindId": "99d1****6124", "bindType": "saml", "name": "name" } ], "memberId": "99d1****6124", "userId": "99d1****6124" }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。