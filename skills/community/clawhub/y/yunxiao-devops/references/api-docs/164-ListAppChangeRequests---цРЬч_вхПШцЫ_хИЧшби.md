# ListAppChangeRequests - 搜索变更列表

| **适用版本** | **中心版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 应用交付 | 变更 | 只读 |

## **请求语法**

### **中心版**

`POST https://{domain}/oapi/v1/appstack/organizations/{organizationId}/apps/{appName}/changeRequests:search`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| appName | string | path | 是 | 应用名。 | my-web-service |
| organizationId | string | path | 是 | 组织 ID。 | ec766e63aexxxxxxxxxxx334d6exe671 |
| \- | object | body | 否 | 搜索变更请求参数。 |  |
| current | integer | body | 否 | 当前页数。 | 1 |
| name | string | body | 否 | 变更名称。 | my-change-request |
| owner | array\[string\] | body | 否 | 负责人列表。 | \["5e9ee1084xxxxxxxxxxc8906"\] |
| pageSize | integer | body | 否 | 每页数量。 | 10 |
| state | array\[string\] | body | 否 | 变更状态列表。 | \["DEVELOPING", "INTEGRATING", "RELEASED"\] |

## **请求示例**

`curl -X 'POST' \ 'https://{domain}/oapi/v1/appstack/organizations/ec766e63aee3xxxxxxxxxd6exe671/apps/my-web-service/changeRequests:search' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "current": 1, "name": "my-change-request", "owner": ["5e9ee1xxxxx06"], "pageSize": 10, "state": ["DEVELOPING", "INTEGRATING", "RELEASED"] }'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object | 变更详情分页数据。 |  |
| current | number | 当前页数。 | 1 |
| pageSize | number | 每页大小。 | 10 |
| pages | number | 总页数。 | 1 |
| records | array | 数据列表。 |  |
| \- | object | 变更详情信息。 |  |
| appCodeRepo | object | 应用代码仓库信息。 |  |
| appName | string | 应用名。 | aaassa |
| connectionConfig | object | 连接配置信息。 |  |
| connectionId | string | 连接 ID。 | 708274 |
| connectionType | string | 连接类型。 | FLOW |
| identifier | string | 仓库标识。 | Codeup\_Demo |
| name | string | 仓库名称。 | Codeup-Demo |
| repoContext | object | 仓库上下文信息。 |  |
| defaultBranch | string | 默认分支。 | master |
| projectId | string | 项目 ID。 | 26420 |
| repoType | string | 仓库类型。 | CODEUP |
| repoUrl | string | 仓库地址。 | https://codeup.aliyun.com/xxxxxxxxxx/Codeup-Demo.git |
| repoUrl | string | 代码仓库地址。 | https://codeup.aliyun.com/xxxxxxxxxxx/Codeup-Demo.git |
| sn | string | 仓库标识符。 | xxxxxxxxxxxxxxxx |
| appCodeRepoSn | string | 应用代码仓库标识符。 | xxxxxxxxxxxxxx |
| appName | string | 应用名。 | aaassa |
| branch | string | 分支名称。 | feature/20251216\_dd |
| creatorId | string | 创建者 ID。 | xxxxxxxxxxxxxx |
| extInfo | object | 扩展信息。 |  |
| gmtCreate | string | 创建时间。 | 2025-12-16T08:14:56.000+00:00 |
| gmtModified | string | 修改时间。 | 2025-12-16T08:14:56.000+00:00 |
| name | string | 变更名称。 | aa |
| originBranch | string | 源分支。 | master |
| originBranchRevision | string | 源分支版本。 | xxxxxxxxxxxxxxxx |
| ownerId | string | 负责人 ID。 | xxxxxxxxxxxxx |
| sn | string | 变更标识符。 | xxxxxxxxxxxxxx |
| state | string | 变更状态，可能的值：\[DEVELOPING INTEGRATING RELEASED CLOSED\]。 | DEVELOPING |
| type | string | 变更类型。 | APP |
| total | number | 总数。 | 6 |

## **返回示例**

`{ "current": 1, "pageSize": 10, "pages": 1, "records": [ { "appCodeRepo": { "appName": "aaassa", "connectionConfig": { "connectionId": "xxxxx", "connectionType": "FLOW" }, "identifier": "Codeup_Demo", "name": "Codeup-Demo", "repoContext": { "defaultBranch": "master", "projectId": "26420", "repoType": "CODEUP", "repoUrl": "https://codeup.aliyun.com/xxxxxxxxxxxxxxx/Codeup-Demo.git" }, "repoUrl": "https://codeup.aliyun.com/xxxxxxxxxxxxxxx/Codeup-Demo.git", "sn": "xxxxxxxxxxxxxxx" }, "appCodeRepoSn": "xxxxxxxxxxxxxx", "appName": "aaassa", "branch": "feature/20251216_dd", "creatorId": "xxxxxxxxxxxxx", "extInfo": { }, "gmtCreate": "2025-12-16T08:14:56.000+00:00", "gmtModified": "2025-12-16T08:14:56.000+00:00", "name": "aa", "originBranch": "master", "originBranchRevision": "xxxxxxxxxxxxxxxxxx", "ownerId": "xxxxxxxxxxxxx", "sn": "xxxxxxxxxxx", "state": "DEVELOPING", "type": "APP" } ], "total": 6 }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。