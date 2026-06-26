# GetSSHKey - 查询 SSH Key

通过 OpenAPI 查询单个 SSH Key。

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 代码管理 | SSH密钥 | 只读 |

## **请求语法**

### **中心版**

`GET https://{domain}/oapi/v1/codeup/organizations/{organizationId}/keys/{keyId}`

### **Region版**

```
GET https://{domain}/oapi/v1/codeup/keys/{keyId}
```

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | -   是：中心版 -   否：Region版 | 组织 ID。 | 60d54f3daccf2bbd6659f3ad |
| keyId | integer | path | 是 | SSH Key 的主键 ID。 | 1 |

## **请求示例**

### **中心版**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/keys/1' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

### **Region版**

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/codeup/keys/1' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object |  |  |
| createdAt | string | 创建时间。 | 2024-10-05T15:30:45Z |
| expireTime | string | 过期时间。 | 2024-10-05T15:30:45Z |
| fingerPrint | string | 指纹信息。 | xxx |
| id | integer | SSH Key 的主键 ID。 | 1 |
| key | string | SSH Key 的公钥串。 | xxx |
| keyScope | string | 作用范围: ALL - 全部（读/写操作，包括 clone/pull/push），READ - 只读（仅支持 clone/pull）。 | ALL |
| lastUsedTime | string | 最后使用时间。 | 2024-10-05T15:30:45Z |
| title | string | SSH Key 的标题。 | username@example |
| updatedAt | string | 更新时间。 | 2024-10-05T15:30:45Z |

## **返回示例**

`{ "createdAt": "2024-10-05T15:30:45Z", "expireTime": "2024-10-05T15:30:45Z", "fingerPrint": "xxx", "id": 1, "key": "xxx", "keyScope": "ALL", "lastUsedTime": "2024-10-05T15:30:45Z", "title": "username@example", "updatedAt": "2024-10-05T15:30:45Z" }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。