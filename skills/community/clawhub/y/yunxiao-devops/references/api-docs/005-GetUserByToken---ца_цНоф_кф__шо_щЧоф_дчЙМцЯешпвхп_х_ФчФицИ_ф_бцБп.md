# GetUserByToken - 根据个人访问令牌查询对应用户信息

通过 OpenAPI 根据个人访问令牌查询对应用户信息。

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 组织管理 | 用户 | 只读 |

## **请求语法**

### **中心版**

`GET https://{domain}/oapi/v1/platform/user`

### **Region版**

```
GET https://{domain}/oapi/v1/platform/user
```

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求示例**

### **中心版**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/platform/user' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

### **Region版**

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/platform/user' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object |  |  |
| createdAt | string | 创建时间。 | 2023-03-22T12:44:50.048Z |
| deletedAt | string | 删除时间。 | 2023-03-22T12:44:50.048Z |
| email | string | 邮箱。 | test\*\*\*\*@example.com |
| id | string | 用户 ID。 | 99d1\*\*\*\*6124 |
| lastOrganization | string | 上次登录组织。 | 99d1\*\*\*\*6124 |
| name | string | 显示名称。 | 示例用户名 |
| nickName | string | 昵称。 | 示例昵称 |
| staffId | string | 工号。 | 123\*\*\*\* |
| sysDeptIds | array\[string\] | 所属部门。 | \["99d1\*\*\*\*6124"\] |
| username | string | 登录账号名。 | demo\*\*username |

## **返回示例**

`{ "createdAt": "2023-03-22T12:44:50.048Z", "deletedAt": "2023-03-22T12:44:50.048Z", "email": "test****@example.com", "id": "99d1****6124", "lastOrganization": "99d1****6124", "name": "示例用户名", "nickName": "示例昵称", "staffId": "123****", "sysDeptIds": ["99d1****6124"], "username": "demo**username" }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。