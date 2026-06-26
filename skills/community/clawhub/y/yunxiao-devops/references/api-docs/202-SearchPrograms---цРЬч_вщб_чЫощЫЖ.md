# SearchPrograms - 搜索项目集

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 项目协作 | 项目 | 只读 |

## **请求语法**

### **中心版**

`POST https://{domain}/oapi/v1/projex/organizations/{organizationId}/programs:search`

### **Region版**

```
POST https://{domain}/oapi/v1/projex/programs:search
```

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | -   是：中心版 -   否：Region版 | organizationId。 |  |
| \- | object | body | 否 |  |  |
| creator | string | body | 否 | 创建人标识符（支持多个，用逗号分隔）。 | 5e6f6c1403283833284f3a95 |
| gmtCreateEnd | string | body | 否 | 创建时间结束（格式：yyyy-MM-dd HH:mm:ss）。 | 2026-01-10 23:59:59 |
| gmtCreateStart | string | body | 否 | 创建时间开始（格式：yyyy-MM-dd HH:mm:ss）。 | 2025-12-01 00:00:00 |
| name | string | body | 否 | 名称搜索（模糊匹配）。 | dd |
| orderBy | string | body | 否 | 排序字段，目前只支持名称和创建时间，不填值则默认为 gmtCreate   gmtCreate：创建时间   name：名称，可能的值：\[gmtCreate name\]。 | gmtCreate |
| page | integer | body | 否 | 分页参数，第几页。 | 1 |
| perPage | integer | body | 否 | 分页参数，每页大小，0-200，默认值20。 | 20 |
| sort | string | body | 否 | 排序方式，默认为 desc   desc：降序   asc：升序，可能的值：\[asc desc\]。 | desc |
| status | string | body | 否 | 状态标识符（支持多个，用逗号分隔）。 | 8a4058a71159b682541b0864,cc961a18adf770c6e423ccc5 |
| users | string | body | 否 | 用户标识符（支持多个，用逗号分隔，用于 extraConditions）。 | 5e6f6c1403283833284f3a95 |

## **请求示例**

### **中心版**

`curl -X 'POST' \ 'https://{domain}/oapi/v1/projex/organizations/{organizationId}/programs:search' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "creator": "5e6f6c1403283833284f3a95", "gmtCreateEnd": "2026-01-10 23:59:59", "gmtCreateStart": "2025-12-01 00:00:00", "name": "dd", "orderBy": "gmtCreate", "page": 1, "perPage": 20, "sort": "desc", "status": "8a4058a71159b682541b0864,cc961a18adf770c6e423ccc5", "users": "5e6f6c1403283833284f3a95" }'`

### **Region版**

```
curl -X 'POST' \
  'https://{domain}/oapi/v1/projex/programs:search' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \
  --data '
    {
        "creator": "5e6f6c1403283833284f3a95",
        "gmtCreateEnd": "2026-01-10 23:59:59",
        "gmtCreateStart": "2025-12-01 00:00:00",
        "name": "dd",
        "orderBy": "gmtCreate",
        "page": 1,
        "perPage": 20,
        "sort": "desc",
        "status": "8a4058a71159b682541b0864,cc961a18adf770c6e423ccc5",
        "users": "5e6f6c1403283833284f3a95"
    }'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | array |  |  |
| \- | object |  |  |
| creator | object | 修改人。 |  |
| id | string | 用户 id。 | 674d96abd497cd558d68\*\*\*\* |
| name | string | 用户名。 | user-name-xxx |
| customCode | string | 编号。 | CCDD |
| customFieldValues | array | 自定义字段值。 |  |
| \- | object | 自定义字段值。 |  |
| fieldId | string | 字段 ID。 | fieldId1 |
| fieldName | string | 字段名称。 | field-test |
| values | array |  |  |
| \- | object |  |  |
| displayValue | string | 值的显示名称。 | 111 |
| identifier | string | 值的唯一标识。 | 111 |
| description | string | 描述。 | test |
| gmtCreate | string | 创建时间的时间戳。 |  |
| gmtModified | string | 更新时间的时间戳。 |  |
| icon | string | icon。 | xxx |
| id | string | id。 | 1111 |
| logicalStatus | string | 逻辑状态。 | normal |
| modifier | object | 修改人。 |  |
| id | string | 用户 id。 | 674d96abd497cd558d68\*\*\*\* |
| name | string | 用户名。 | user-name-xxx |
| name | string | 名称。 | project-test |
| scope | string | 公开类型，枚举值为： public、private。 | public |
| status | object | 状态。 |  |
| id | string | 状态 id。 | 1111 |
| name | string | 状态名称。 | 进行中 |

## **返回示例**

`[ { "creator": { "id": "674d96abd497cd558d68****", "name": "user-name-xxx" }, "customCode": "CCDD", "customFieldValues": [ { "fieldId": "fieldId1", "fieldName": "field-test", "values": [ { "displayValue": "111", "identifier": "111" } ] } ], "description": "test", "gmtCreate": "", "gmtModified": "", "icon": "xxx", "id": "1111", "logicalStatus": "normal", "modifier": { "id": "674d96abd497cd558d68****", "name": "user-name-xxx" }, "name": "project-test", "scope": "public", "status": { "id": "1111", "name": "进行中" } } ]`

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