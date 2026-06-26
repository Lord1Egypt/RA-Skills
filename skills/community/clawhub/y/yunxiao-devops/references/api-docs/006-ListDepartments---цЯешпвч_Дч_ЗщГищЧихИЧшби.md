# ListDepartments - 查询组织部门列表

通过 OpenAPI 查询组织部门列表。

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 组织管理 | 组织部门 | 只读 |

## **请求语法**

### **中心版**

`GET https://{domain}/oapi/v1/platform/organizations/{organizationId}/departments`

### **Region版**

```
GET https://{domain}/oapi/v1/platform/departments
```

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | -   是：中心版 -   否：Region版 | 所属组织 ID。 |  |
| parentId | string | query | 否 | 父部门 ID。 |  |
| page | integer | query | 否 | \[标准版不适用\]当前页，默认1。 |  |
| perPage | integer | query | 否 | \[标准版不适用\]每页数据条数，1<=perPage<=100，默认100。 |  |

## **请求示例**

### **中心版**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/platform/organizations/{organizationId}/departments?parentId={parentId}&page={page}&perPage={perPage}' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

### **Region版**

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/platform/departments?parentId={parentId}&page={page}&perPage={perPage}' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | array |  |  |
| \- | object |  |  |
| creatorId | string | 创建人 ID。 | 99d1\*\*\*\*6124 |
| hasSub | boolean | 是否有子部门。 | true |
| id | string | 部门 ID。 | 99d1\*\*\*\*6124 |
| name | string | 部门名称。 | 示例 |
| organizationId | string | 组织 ID。 | 99d1\*\*\*\*6124 |
| parentId | string | 父部门 ID。 | 99d1\*\*\*\*6124 |

## **返回示例**

`[ { "creatorId": "99d1****6124", "hasSub": true, "id": "99d1****6124", "name": "示例", "organizationId": "99d1****6124", "parentId": "99d1****6124" } ]`

## **响应头**

| **参数** | **描述** | **示例值** |
| --- | --- | --- |
| x-next-page | \[标准版不适用\]下一页。 |  |
| x-page | \[标准版不适用\]当前页。 |  |
| x-per-page | \[标准版不适用\]每页数据条数。 |  |
| x-prev-page | \[标准版不适用\]上一页。 |  |
| x-total | \[标准版不适用\]总数据量。 |  |
| x-total-pages | \[标准版不适用\]总分页数。 |  |

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。