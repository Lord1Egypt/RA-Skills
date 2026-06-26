# GetVariableGroup - 获取变量组

通过 OpenAPI 获取变量组。

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 流水线 | 变量组 | 只读 |

## **请求语法**

### **中心版**

`GET https://{domain}/oapi/v1/flow/organizations/{organizationId}/variableGroups/{id}`

### **Region版**

```
GET https://{domain}/oapi/v1/flow/variableGroups/{id}
```

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | -   是：中心版 -   否：Region版 | 企业 Id。 | 5ebbc0228123212b59xxxxx |
| id | integer | path | 是 | 变量组 id。 | 123 |

## **请求示例**

### **中心版**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/flow/organizations/5ebbc0228123212b59xxxxx/variableGroups/123' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

### **Region版**

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/flow/variableGroups/123' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object |  |  |
| createTime | integer | 创建时间。 | 1586863220000 |
| creatorAccountId | string | 创建人阿里云账号 id。 | 1111111111111 |
| description | string | 变量组描述。 | 变量组描述 |
| id | integer | 变量组 id。 | 1234 |
| modifierAccountId | string | 更新人阿里云账号 id。 | 1111111111111 |
| name | string | 变量组名称。 | 主机组 |
| relatedPipelines | array |  |  |
| \- | object |  |  |
| id | integer | 关联的流水线 Id。 | 1586863220000 |
| name | string | 关联的流水线名称。 | 流水线 |
| updateTime | integer | 更新时间。 | 1586863220000 |
| variables | array |  |  |
| \- | object |  |  |
| isEncrypted | boolean | 是否加密。 | true |
| name | string | 变量名。 | name1 |
| value | string | 变量值。 | value1 |

## **返回示例**

`{ "createTime": 1586863220000, "creatorAccountId": "1111111111111", "description": "变量组描述", "id": 1234, "modifierAccountId": "1111111111111", "name": "主机组", "relatedPipelines": [ { "id": 1586863220000, "name": "流水线" } ], "updateTime": 1586863220000, "variables": [ { "isEncrypted": true, "name": "name1", "value": "value1" } ] }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。