# ListProgramVersions - 获取项目集版本列表

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 项目协作 | 版本 | 只读 |

## **请求语法**

### **中心版**

`GET https://{domain}/oapi/v1/projex/organizations/{organizationId}/programs/{id}/versions`

### **Region版**

```
GET https://{domain}/oapi/v1/projex/programs/{id}/versions
```

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | -   是：中心版 -   否：Region版 | organizationId。 |  |
| id | string | path | 是 | 项目集唯一标识。 |  |
| status | array\[string\] | query | 否 | 过滤的状态，TODO,DOING,ARCHIVED，分别对应未开始，进行中，已完成。 |  |
| page | integer | query | 否 | 分页参数，第几页。 |  |
| perPage | integer | query | 否 | 分页参数，每页大小。 |  |

## **请求示例**

### **中心版**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/projex/organizations/{organizationId}/programs/{id}/versions?status={status}&name={name}&page={page}&perPage={perPage}' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

### **Region版**

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/projex/programs/{id}/versions?status={status}&name={name}&page={page}&perPage={perPage}' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | array |  |  |
| \- | object |  |  |
| creator | object | 负责人。 |  |
| id | string | 用户 id。 | 674d96abd497cd558d68\*\*\*\* |
| name | string | 用户名。 | user-name-xxx |
| gmtCreate | string | 创建时间的时间戳。 |  |
| gmtModified | string | 更新时间的时间戳。 |  |
| id | string | id。 | 1111 |
| locked | boolean | 是否被锁定。 | false |
| modifier | object | 负责人。 |  |
| id | string | 用户 id。 | 674d96abd497cd558d68\*\*\*\* |
| name | string | 用户名。 | user-name-xxx |
| name | string | 版本名称。 | 1111 |
| owners | array | 负责人。 |  |
| \- | object | 负责人。 |  |
| id | string | 用户 id。 | 674d96abd497cd558d68\*\*\*\* |
| name | string | 用户名。 | user-name-xxx |
| publishDate | string | 发布日期。 |  |
| startDate | string | 开始日期。 |  |
| status | string | 状态，未开始对应 TODO，进行中对应 DOING，已发布对应 ARCHIVED。 | TODO |

## **返回示例**

`[ { "creator": { "id": "674d96abd497cd558d68****", "name": "user-name-xxx" }, "gmtCreate": "", "gmtModified": "", "id": "1111", "locked": false, "modifier": { "id": "674d96abd497cd558d68****", "name": "user-name-xxx" }, "name": "1111", "owners": [ { "id": "674d96abd497cd558d68****", "name": "user-name-xxx" } ], "publishDate": "", "startDate": "", "status": "TODO" } ]`

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