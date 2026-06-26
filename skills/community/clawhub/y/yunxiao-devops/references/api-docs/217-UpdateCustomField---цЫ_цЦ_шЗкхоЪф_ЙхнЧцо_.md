# UpdateCustomField - 更新自定义字段

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 项目协作 | 自定义字段 | 读写 |

## **请求语法**

### **中心版**

`PUT https://{domain}/oapi/v1/projex/organizations/{organizationId}/customField/{id}`

### **Region版**

```
PUT https://{domain}/oapi/v1/projex/customField/{id}
```

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| id | string | path | 是 | 自定义字段 id。 |  |
| organizationId | string | path | -   是：中心版 -   否：Region版 | organizationId。 |  |
| \- | object | body | 否 |  |  |
| defaultValue | string | body | 否 | 默认值。 | test |
| description | string | body | 否 | 字段描述。 | test |
| disabledOptions | array\[string\] | body | 否 | 字段待选值，只有字段是全局字段且是列表类型时才有效。 | \["a"\] |
| name | string | body | 否 | 字段名称。 | test |
| nameEn | string | body | 否 | 字段英文名称。 | test |
| operatorId | string | body | 否 | 操作者的 useId，个人 token 时该参数无效。 | 操作者的 useId，个人 token 时该参数无效 |
| options | array\[string\] | body | 否 | 字段待选值，只有字段是列表类型时才有效。 | \["a","b","c"\] |

## **请求示例**

### **中心版**

`curl -X 'PUT' \ 'https://{domain}/oapi/v1/projex/organizations/{organizationId}/customField/{id}' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "defaultValue": "test", "description": "test", "disabledOptions": ["a"], "name": "test", "nameEn": "test", "operatorId": "操作者的useId，个人token时该参数无效", "options": ["a","b","c"] }'`

### **Region版**

```
curl -X 'PUT' \
  'https://{domain}/oapi/v1/projex/customField/{id}' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \
  --data '
    {
        "defaultValue": "test",
        "description": "test",
        "disabledOptions": ["a"],
        "name": "test",
        "nameEn": "test",
        "operatorId": "操作者的useId，个人token时该参数无效",
        "options": ["a","b","c"]
    }'
```

## **返回参数**

无

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。