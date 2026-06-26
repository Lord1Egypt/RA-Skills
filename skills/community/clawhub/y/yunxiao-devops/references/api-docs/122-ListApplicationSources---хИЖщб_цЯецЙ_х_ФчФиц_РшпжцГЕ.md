# ListApplicationSources - 分页查找应用源详情

通过OpenAPI分页查找应用源详情。

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

`GET https://{domain}/oapi/v1/appstack/organizations/{organizationId}/apps/{appName}/sources`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| appName | string | path | 是 | 应用名。 | my-web-service |
| pagination | string | query | 否 | 分页模式参数：keyset 表示键集分页，不传表示页码分页。 | keyset |
| perPage | number | query | 否 | 分页尺寸参数，决定一页最多返回多少对象。 | 20 |
| orderBy | string | query | 否 | 分页排序属性，决定根据何种属性进行记录排序；推荐在实现严格遍历时，使用 id 属性。 | id |
| sort | string | query | 否 | 分页排序升降序，asc 为升序，desc 为降序；推荐在实现严格遍历时，使用升序。 | asc |
| nextToken | string | query | 否 | 键集分页 token，获取第一页数据时无需传入，否则需要传入前一页查询结果中的 nextToken 字段。 | 0286da51e61e4cf9a7056ef1a4fexxxx |
| page | number | query | 否 | 页码分页时使用，用于获取下一页内容。 | 1 |
| organizationId | string | path | 是 | 组织 ID。 | ec766e63aee3437d9a51f334d6exxxxx |

## **请求示例**

`curl -X 'GET' \ 'https://test.rdc.aliyuncs.com/oapi/v1/appstack/organizations/organization-id-xxx/apps/my-web-service/sources?pagination=keyset&perPage=20&orderBy=id&sort=asc&nextToken=token&page=1' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object | 分页接口所返回的列表。 |  |
| current | number | 页码分页时存在该字段，表示当前页。 | 1 |
| data | array\[\] | 分页结果数据。 |  |
| appName | string | 代码仓库源所隶属的应用唯一名。 | my-web-service |
| connectionConfig | object | Flow 服务连接信息。 |  |
| connectionId | string | 服务连接 ID。 | connection-id |
| connectionType | string | 服务连接类型：FLOW 。 | FLOW |
| identifier | string | 代码服务提供方所使用的代码仓库唯一标识。 | my-web-service-repo |
| name | string | 代码仓库源名称。 | my-web-service-repo-git |
| repoContext | object | 代码仓库上下文。 |  |
| defaultBranch | string | 默认分支。 | branch-xxx |
| repoType | string | 代码仓库类型。 | CODE\_REPO |
| repoUrl | string | 代码仓库地址。 | http://xxxxxxxxx |
| repoUrl | string | 代码仓库 URL。 | https://codeup.aliyun.com/bd9e3c6d-xxxx-4580-xxxx-c5e26f1ed0f0/my-web-service-repo.git |
| sn | string | 代码仓库源唯一序列号。 | 2e4bec5575244987a4f09ea4ca29xxxx |
| type | string | 代码仓库类型：CODE\_REPO。 | CODE\_REPO |
| nextToken | string | 采用键值分页时存在该字段，用于传给分页接口，迭代获取下一页数据。 | 0286da51e61e4cf9a7056ef1a4fexxxx |
| pages | number | 页码分页时存在该字段，表示总页数。 | 10 |
| perPage | number | 页码分页时存在该字段，表示每页大小。 | 10 |
| total | number | 页码分页时存在该字段，表示结果总数。 | 100 |

## **返回示例**

`{ "current": 1, "data": [ { "appName": "my-web-service", "connectionConfig": { "connectionId": "connection-id", "connectionType": "FLOW" }, "identifier": "my-web-service-repo", "name": "my-web-service-repo-git", "repoContext": { "defaultBranch": "branch-xxx", "repoType": "CODE_REPO", "repoUrl": "http://xxxxxxxxx" }, "repoUrl": "https://codeup.aliyun.com/bd9e3c6d-624f-4580-af7d-c5e26f1ed0f0/my-web-service-repo.git", "sn": "2e4bec5575244987a4f09ea4ca29e89f", "type": "CODE_REPO" } ], "nextToken": "token", "pages": 10, "perPage": 10, "total": 100 }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。