# ListProjectMembers - 获取项目成员列表

通过 OpenAPI 获取项目成员列表。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。
    
    | **产品** | **资源** | **所需权限** |
    | --- | --- | --- |
    | 项目协作 | 项目成员 | 只读 |
    

## **请求语法**

`GET https://{domain}/oapi/v1/projex/organizations/{organizationId}/projects/{id}/members`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| id | string | path | 是 | 项目唯一标识。 | 589c53d622cc8521793e08\*\*\*\* |
| name | string | query | 否 | 名称过滤。 | test |
| roleId | string | query | 否 | 角色 id 过滤，例如管理员的值为 project.admin。 | project.admin |
| organizationId | string | path | 是 | organizationId。 | 5ebbc0228123212b59xxxxx |

## **请求示例**

`curl -X 'GET' \ 'https://test.rdc.aliyuncs.com/oapi/v1/projex/organizations/{organizationId}/projects/589c53d622cc8521793e08****/members?name=test&roleId=project.admin' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | array |  |  |
| \- | object |  |  |
| roleId | string | 角色的唯一标识。 | project.admin |
| roleName | string | 角色名称。 | 管理员 |
| userAvatar | string | 用户头像地址。 | xxx |
| userId | string | 用户唯一标识。 | user-xxx |
| userName | string | 用户名称。 | user-test |

## **返回示例**

`[ { "roleId": "project.admin", "roleName": "管理员", "userAvatar": "xxx", "userId": "user-xxx", "userName": "user-test" } ]`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。