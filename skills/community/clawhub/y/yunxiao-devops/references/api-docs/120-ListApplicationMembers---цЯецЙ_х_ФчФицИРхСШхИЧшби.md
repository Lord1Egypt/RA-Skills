# ListApplicationMembers - 查找应用成员列表

通过OpenAPI查找应用成员列表。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 应用交付 | 应用 | 只读 |

## **请求语法**

`GET https://{domain}/oapi/v1/appstack/organizations/{organizationId}/apps/{appName}/members`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| appName | string | path | 是 | 应用名。 | my-demo-app |
| current | integer | query | 是 | 当前页号（从 1 开始，默认取 1）。 | 1 |
| pageSize | integer | query | 是 | 分页记录数（默认 10 条）。 | 10 |
| organizationId | string | path | 是 | 组织 ID。 | ec766e63aee3437d9a51f334d6exxxxx |

## **请求示例**

`curl -X 'GET' \ 'https://test.rdc.aliyuncs.com/oapi/v1/appstack/organizations/organization-id-xxx/apps/my-demo-app/members?current=1&pageSize=10' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object | 分页数据。 |  |
| current | number | 当前页数。 | 1 |
| pageSize | number | 每页大小。 | 10 |
| pages | number | 总页数。 | 10 |
| records | array | 数据列表。 |  |
| \- | object | 数据列表。 |  |
| avatar | string | 成员头像 URL。 | http://xxxxxxxxx |
| description | string | 成员描述。 | 示例描述 |
| displayName | string | 成员展示名。 | 示例成员名 |
| id | string | 成员 ID（如用户 ID），含义需要根据 type 字段确定。 | bd9e3c6d-624f-4580-af7d-c5e26f1ed0f0 |
| roleList | array | 成员所具有的角色列表。 |  |
| \- | object | 成员所具有的角色列表。 |  |
| displayName | string | 角色的展示名。 | 拥有者 |
| name | string | 角色的唯一标识名。 | owner |
| type | string | 成员类型，如用户（User）、组织（Org）等，用于辅助判断 id 字段的类型，可能的值：\[Member User Team Group Org\]。 | User |
| total | number | 总数。 | 10 |

## **返回示例**

`{ "current": 1, "pageSize": 10, "pages": 10, "records": [ { "avatar": "http://xxxxxxxxx", "description": "示例描述", "displayName": "示例成员名", "id": "bd9e3c6d-624f-4580-af7d-c5e26f1ed0f0", "roleList": [ { "displayName": "拥有者", "name": "owner" } ], "type": "User" } ], "total": 10 }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。