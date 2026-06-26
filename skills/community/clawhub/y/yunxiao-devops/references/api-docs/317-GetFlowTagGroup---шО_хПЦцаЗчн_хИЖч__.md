# GetFlowTagGroup - 获取标签分类

通过 OpenAPI 获取标签分类。

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 流水线 | 标签 | 只读 |

## **请求语法**

### **中心版**

`GET https://{domain}/oapi/v1/flow/organizations/{organizationId}/tagGroups/{id}`

### **Region版**

```
GET https://{domain}/oapi/v1/flow/tagGroups/{id}
```

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | -   是：中心版 -   否：Region版 | 企业 Id。 | 5ebbc0228123212b59xxxxx |
| id | integer | path | 是 | 标签分类 id。 | 111 |

## **请求示例**

### **中心版**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/flow/organizations/5ebbc0228123212b59xxxxx/tagGroups/111' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

### **Region版**

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/flow/tagGroups/111' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object |  |  |
| creatorAccountId | string | 创建人。 | 1111111111111 |
| flowTagList | array |  |  |
| \- | object |  |  |
| color | string | 标签颜色。 | #1F9AEF |
| creatorAccountId | string | 创建人。 | 1111111111111 |
| id | integer | 标签 id。 | 111 |
| modifierAccountId | string | 更新人。 | 1111111111111 |
| name | string | 标签名称。 | 标签名称 |
| id | integer | 标签分类 id。 | 1111 |
| modifierAccountId | string | 更新人。 | 1111111111111 |
| name | string | 标签分类名称。 | 标签分类名称 |

## **返回示例**

`{ "creatorAccountId": "1111111111111", "flowTagList": [ { "color": "#1F9AEF", "creatorAccountId": "1111111111111", "id": 111, "modifierAccountId": "1111111111111", "name": "标签名称" } ], "id": 1111, "modifierAccountId": "1111111111111", "name": "标签分类名称" }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。