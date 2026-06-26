# DeleteHostListFromDeployGroup - 部署组移除主机

通过 OpenAPI 部署组移除主机。

| 适用版本 | 企业标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 应用交付 | 资源 | 读写 |

### **请求语法**

`PUT https://{domain}/oapi/v1/appstack/organizations/{organizationId}/pools/instances/{instanceName}/deployGroup/{groupName}/removeHostList`

### **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

### **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| instanceName | string | path | 是 | 主机集群名称（非主机集群显示名）。 | 主机集群1 |
| groupName | string | path | 是 | 部署组名称（非部署组显示名）。 | 部署组1 |
| organizationId | string | path | 是 | 组织 ID。 | ec766e63aee3437d9a51f334d6exe671 |
| \- | object | body | 否 |  |  |
| hostSns | array\[string\] | body | 是 | ecs 主机实例 id 列表（主机类型暂只支持 ecs）。 | \[“i-ssssssa”, “i-ssssssb”, “i-ssssssc”\] |

### **请求示例**

`curl -X 'PUT' \ 'https://{domain}/oapi/v1/appstack/organizations/ec766e63aee3437d9a51f334d6exe671/pools/instances/主机集群1/deployGroup/部署组1/removeHostList' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "hostSns": ["i-ssssssa", "i-ssssssb", "i-ssssssc"] }'`

### **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | boolean | 是否成功。 | true |

### **返回示例**

`true`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。