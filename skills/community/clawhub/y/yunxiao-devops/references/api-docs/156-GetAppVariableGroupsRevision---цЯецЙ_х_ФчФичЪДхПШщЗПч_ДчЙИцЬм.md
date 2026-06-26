# GetAppVariableGroupsRevision - 查找应用的变量组版本

通过OpenAPI查找应用的变量组版本。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 应用交付 | 变量组 | 只读 |

## **请求语法**

`GET https://{domain}/oapi/v1/appstack/organizations/{organizationId}/apps/{appName}/variableGroups:revision`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| appName | string | path | 是 | 应用名。 | my-web-service |
| organizationId | string | path | 是 | 组织 ID。 | c229f22024535638af41838daa43af1e6d46xxxx |

## **请求示例**

`curl -X 'GET' \ 'https://test.rdc.aliyuncs.com/oapi/v1/appstack/organizations/c229f22024535638af41838daa43af1e6d46xxxx/apps/my-web-service/variableGroups:revision' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object | 版本信息。 |  |
| author | string | 提交人。 | 1c83bd48e254405fb27297ee1fb8xxxx |
| commitTime | number | 提交时间。 | 1726301443290 |
| message | string | 版本提交信息。 | message-xxxx |
| refs | array\[string\] | 关联信息。 |  |
| repoMeta | object | 仓库信息。 |  |
| name | string | 仓库名称。 | my-repo |
| type | string | 仓库类型：VARIABLE。 | VARIABLE |
| sha | string | 版本 sha 值。 | c229f22024535638af41838daa43af1e6d46xxxx |

## **返回示例**

`{ "author": "1c83bd48e254405fb27297ee1fb8xxxx", "commitTime": 1726301443290, "message": "message-xxxx", "refs": [ ], "repoMeta": { "name": "my-repo", "type": "VARIABLE" }, "sha": "c229f22024535638af41838daa43af1e6d46xxxx" }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。