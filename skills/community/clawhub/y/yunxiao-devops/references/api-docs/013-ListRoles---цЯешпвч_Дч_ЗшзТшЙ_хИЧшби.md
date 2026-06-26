# ListRoles - 查询组织角色列表

通过 OpenAPI 查询组织角色列表（本接口无需分页，组织角色个数是有限的）。

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 组织管理 | 组织角色 | 只读 |

## **请求语法**

### **中心版**

`GET https://{domain}/oapi/v1/platform/organizations/{organizationId}/roles`

### **Region版**

```
GET https://{domain}/oapi/v1/platform/roles
```

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | -   是：中心版 -   否：Region版 | 所属组织 ID。 |  |

## **请求示例**

### **中心版**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/platform/organizations/{organizationId}/roles' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

### **Region版**

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/platform/roles' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | array |  |  |
| \- | object |  |  |
| id | string | 角色 ID。 | 99d1\*\*\*\*6124 |
| name | string | 角色名称。 | 示例名 |
| organizationId | string | 组织 ID。 | 99d1\*\*\*\*6124 |
| permissions | array\[string\] | 角色权限列表。 | \["base\*\*\*\*\*\*"\] |

## **返回示例**

`[ { "id": "99d1****6124", "name": "示例名", "organizationId": "99d1****6124", "permissions": ["base******"] } ]`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。