# CreateApplicationSource - 创建应用源

通过OpenAPI创建应用源。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 应用交付 | 应用 | 读写 |

## **请求语法**

`POST https://{domain}/oapi/v1/appstack/organizations/{organizationId}/apps/{appName}/sources`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| appName | string | path | 是 | 应用名。 | my-web-service |
| organizationId | string | path | 是 | 组织 ID。 | organization-id-xxx |
| \- |  | body | 否 |  |  |
| connectionConfig | object | body | 是 | Flow 服务连接信息。 |  |
| connectionId | string | body | 是 | 服务连接 ID。 | 请使用Flow服务连接的id（Integer 类型），即 [ListServiceConnections - 获取服务连接列表](https://help.aliyun.com/zh/yunxiao/developer-reference/listserviceconnections)接口返回中的id。 |
| connectionType | string | body | 是 | 服务连接类型：FLOW （固定为FLOW） | FLOW |
| identifier | string | body | 是 | 代码仓库唯一标识。 | myrepo |
| name | string | body | 是 | 代码仓库名。 | 6489a6ad391bxxxxyyy/Codeup-Demo |
| repoContext | object | body | 是 | 代码仓库上下文。 |  |
| defaultBranch | string | body | 是 | 默认分支。 | branch-xxx |
| repoType | string | body | 是 | 代码仓库类型。 | CODEUP - Codeup代码库CUSTOM\_GITLAB - 自建GitlabGIT - 通用Git |
| repoUrl | string | body | 是 | 代码仓库地址。 | http://xxxxxxxxx.git |
| repoUrl | string | body | 是 | 代码仓库 URL。 | https://codeup.aliyun.com/6489a6ad391bxxxxyyy/Codeup-Demo.git |
| projectId | string | body | 是 | 项目ID | 183240 |
| type | string | body | 是 | 代码仓库类型：CODE\_REPO。 | CODE\_REPO |

## **请求示例**

`curl -X 'POST' \ 'https://test.rdc.aliyuncs.com/oapi/v1/appstack/organizations/ec766e63aee3437d9a51f334d6exe671/apps/my-web-service/sources' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "connectionConfig": { "connectionId": "connection-id", "connectionType": "FLOW" }, "identifier": "myrepo", "name": "6489a6ad391bxxxxyyy/Codeup-Demo", "repoContext": { "defaultBranch": "branch-xxx", "repoType": "CODEUP", "repoUrl": "http://xxxxxxxxx.git", "projectId": "183240" }, "repoUrl": "https://codeup.aliyun.com/6489a6ad391bxxxxyyy/Codeup-Demo.git", "type": "CODE_REPO" }'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- |  |  |  |
| appName | string | 代码仓库源所隶属的应用唯一名。 | my-web-service |
| connectionConfig | object | Flow 服务连接信息。 |  |
| connectionId | string | 服务连接 ID。 | connection-id |
| connectionType | string | 服务连接类型：FLOW （固定为FLOW）。 | FLOW |
| identifier | string | 代码服务提供方所使用的代码仓库唯一标识。 | my-web-service-repo |
| name | string | 代码仓库源名称。 | my-web-service-repo-git |
| repoContext | object | 代码仓库上下文。 |  |
| defaultBranch | string | 默认分支。 | branch-xxx |
| repoType | string | 代码仓库类型：CODEUP Codeup, CUSTOM\_GITLAB 自建GitLab, GIT 通用GIT。 | CODEUP |
| repoUrl | string | 代码仓库地址。 | http://xxxxxxxxx |
| repoUrl | string | 代码仓库 URL。 | https://codeup.aliyun.com/bd9e3c6d-624f-4580-af7d-c5e26f1ed0f0/my-web-service-repo.git |
| sn | string | 代码仓库源唯一序列号。 | 2e4bec5575244987a4f09ea4ca29e89f |
| type | string | 代码仓库类型：CODE\_REPO（固定为CODE\_REPO）。 | CODE\_REPO |

## **返回示例**

`{ "appName": "my-web-service", "connectionConfig": { "connectionId": "connection-id", "connectionType": "FLOW" }, "identifier": "my-web-service-repo", "name": "my-web-service-repo-git", "repoContext": { "defaultBranch": "branch-xxx", "repoType": "CODEUP", "repoUrl": "http://xxxxxxxxx" }, "repoUrl": "https://codeup.aliyun.com/bd9e3c6d-624f-4580-af7d-c5e26f1ed0f0/my-web-service-repo.git", "sn": "2e4bec5575244987a4f09ea4ca29e89f", "type": "" }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。