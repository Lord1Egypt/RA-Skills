# UpdateAppTag - 更新应用标签

通过OpenAPI更新应用标签。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 应用交付 | 应用标签 | 读写 |

### **请求语法**

`PUT https://{domain}/oapi/v1/appstack/organizations/{organizationId}/appTags/updateTag`

### **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

### **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | 是 | 组织 ID。 | ec766e63aee3437d9a51f334d6ex\*\*\*\* |
| name | string | query | 是 | 应用标签名称。 | mytag |
| \- | object | body | 否 |  |  |
| color | string | body | 否 | 标签颜色，若不填写则保持原有颜色不变。  -   `#66acab`：蓝绿色 -   `#7b9ab4`：蓝灰色 -   `#698cd4`：明亮的蓝色 -   `#4676e5`：强烈的蓝色 -   `#5c68c1`：深蓝紫色 -   `#9f76dA`：紫色 -   `#6bAe3f`：绿色 -   `#ae9e6b`：土黄色 -   `#a7bc60`：浅绿 -   `#ae785e`：棕色 -   `#eb933e`：橙色 -   `#d75644`：红色 | #66acab |
| name | string | body | 是 | 要修改为的新的应用标签名称，如无需修改，请确保与原 name 相同。 | newName |

### **请求示例**

`curl -X 'PUT' \ 'https://{domain}/oapi/v1/appstack/organizations/ec766e63aee3437d9a51f334d6exe671/appTags/updateTag?name=mytag' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "color": "#66acab", "name": "newName" }'`

### **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object |  |  |
| frontendStyle | string | 样式，目前仅含颜色。 | `{"color":"#66acab"}` |
| name | string | 应用标签名称。 | mytag |

### **返回示例**

`{ "frontendStyle": "{\"color\":\"#66acab\"}", "name": "mytag" }`

### **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。