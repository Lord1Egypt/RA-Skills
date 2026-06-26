# CreateGlobalVar - 创建全局变量组

创建全局变量组。

| 适用版本 | 标准版 |
| --- | --- |

## 服务接入点与授权信息

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。
    
    | **产品** | **资源** | **所需权限** |
    | --- | --- | --- |
    | 应用交付 | 全局变量组 | 读写 |
    

## 请求语法

`POST https://{domain}/oapi/v1/appstack/organizations/{organizationId}/globalVars`

## 请求头

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## 请求参数

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | 是 | 组织 ID。 | organization-id-xxx |
| \- | object | body | 否 | 创建全局变量组请求。 |  |
| content | array | body | 否 | 变量列表。 |  |
| \- | object | body | 否 | 变量模型。 |  |
| description | string | body | 否 | 变量描述。 | 命名空间 |
| key | string | body | 否 | 变量键。 | namespace |
| value | string | body | 否 | 变量值。 | default |
| displayName | string | body | 否 | 全局变量组显示名称。 | my-display-name |
| message | string | body | 否 | 全局变量组信息。 | message-xxx |
| name | string | body | 否 | 全局变量组名称。 | my-global-var-group |
| ownerId | string | body | 否 | 全局变量组拥有者。 | owner-id-xxx |

## 请求示例

`curl -X 'POST' \ 'https://test.rdc.aliyuncs.com/oapi/v1/appstack/organizations/anyOrganizationId/globalVars' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "content": [ { "description": "命名空间", "key": "namespace", "value": "default" } ], "displayName": "my-display-name", "message": "message-xxx", "name": "my-global-var-group", "ownerId": "owner-id-xxx" }'`

## 返回参数

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object | 全局变量组。 |  |
| content | array | 全局变量组变量列表。 |  |
| \- | object | 变量模型。 |  |
| description | string | 变量描述。 | 命名空间 |
| key | string | 变量键。 | namespace |
| value | string | 变量值。 | default |
| creator | string | 全局变量组创建者。 | creator-id-xxx |
| displayName | string | 全局变量组显示名称。 | my-display-name |
| gmtCreate | string | 全局变量组创建时间。 | 2024-01-01 00:00:00 |
| gmtModified | string | 全局变量组修改时间。 | 2024-01-01 00:00:00 |
| modifier | string | 全局变量组修改者。 | modifier-id-xxx |
| name | string | 全局变量组名称。 | my-global-var-group |
| revision | object | 版本信息。 |  |
| author | string | 提交人。 | user-xxxx |
| commitTime | integer | 提交时间。 | 1722250824321 |
| message | string | 版本提交信息。 | message-xxxx |
| refs | array\[string\] | 关联信息。 |  |
| repoMeta | object | 仓库信息。 |  |
| name | string | 仓库名称。 | my-repo-name |
| type | string | 仓库类型。 | VARIABLE |
| sha | string | 版本 sha 值。 | sha-xxxxx |

## 返回示例

`{ "content": [ { "description": "命名空间", "key": "namespace", "value": "default" } ], "creator": "creator-id-xxx", "displayName": "my-display-name", "gmtCreate": "2024-01-01 00:00:00", "gmtModified": "2024-01-01 00:00:00", "modifier": "modifier-id-xxx", "name": "my-global-var-group", "revision": { "author": "user-xxxx", "commitTime": 1722250824321, "message": "message-xxxx", "refs": [ ], "repoMeta": { "name": "my-repo-name", "type": "VARIABLE" }, "sha": "sha-xxxxx" } }`

## 错误码

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。