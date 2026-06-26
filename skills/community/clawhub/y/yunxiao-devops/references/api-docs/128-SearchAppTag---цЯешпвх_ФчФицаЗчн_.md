# SearchAppTag - 查询应用标签

通过OpenAPI查询应用标签。

| 适用版本 | 标准版 |
| --- | --- |

### **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/lingma/developer-reference/obtain-personal-access-token-1)。
-   获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 应用交付 | 应用标签 | 只读 |

### **请求语法**

`POST https://{domain}/oapi/v1/appstack/organizations/{organizationId}/appTags:search`

### **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

### **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | 是 | 组织 ID。 | ec766e63aee3437d9a51f334d6ex\*\*\*\* |
| current | integer | query | 否 | 页数，从1开始。默认值为1。 | 1 |
| pageSize | integer | query | 否 | 本页返回的数量，默认值为10。 | 10 |
| \- | object | body | 否 |  |  |
| orderBy | string | body | 否 | 排序方式，支持 name 和 id，默认为 id。 | name |
| search | string | body | 否 | 应用标签名称的模糊搜索。 | mytag |
| sort | string | body | 否 | 排序方式，支持 asc 和 desc，默认为 desc。 | desc |

### **请求示例**

`curl -X 'POST' \ 'https://{domain}/oapi/v1/appstack/organizations/ec766e63aee3437d9a51f334d6exe671/appTags:search?current=1&pageSize=10' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "orderBy": "name", "search": "mytag", "sort": "desc" }'`

### **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object |  |  |
| data | array | 返回的应用标签列表。 |  |
| \- | object |  |  |
| frontendStyle | string | 样式，目前仅含颜色。 | `{"color":"#66acab"}` |
| name | string | 应用标签名称。 | mytag |
| total | integer | 当前搜索条件下的总数。 | 1 |

### **返回示例**

`{ "data": [ { "frontendStyle": "{\"color\":\"#66acab\"}", "name": "mytag" } ], "total": 1 }`

### **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。