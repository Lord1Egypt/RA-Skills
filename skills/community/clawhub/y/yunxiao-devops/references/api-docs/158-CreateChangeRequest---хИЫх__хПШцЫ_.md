# CreateChangeRequest - 创建变更

通过OpenAPI创建变更。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 应用交付 | 变更 | 读写 |

## **请求语法**

`POST https://{domain}/oapi/v1/appstack/organizations/{organizationId}/apps/{appName}/changeRequests`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| appName | string | path | 是 | 应用名。 | my-web-service |
| organizationId | string | path | 是 | 组织 ID。 | ec766e63aee3437d9a51f334d6exxxxx |
| \- | object | body | 否 | 创建变更请求。 |  |
| appCodeRepoSn | string | body | 是 | 应用代码仓库标识符。 | cebf021afe6848578c97a1f6a253xxxx |
| autoDeleteBranchWhenEnd | boolean | body | 是 | 变更结束时候是否自动删除分支。 | false |
| branchName | string | body | 是 | 应用代码分支名称。 | master |
| createBranch | boolean | body | 是 | 是否创建分支。 | false |
| ownerId | string | body | 否 | 变更负责人。 | 1c83bd48e254405fb27297ee1fb8xxxx |
| title | string | body | 是 | 变更标题。 | title-xxxx |

## **请求示例**

`curl -X 'POST' \ 'https://test.rdc.aliyuncs.com/oapi/v1/appstack/organizations/ec766e63aee3437d9a51f334d6exxxxx/apps/my-web-service/changeRequests' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "appCodeRepoSn": "cebf021afe6848578c97a1f6a253xxxx", "autoDeleteBranchWhenEnd": false, "branchName": "master", "createBranch": false, "ownerId": "1c83bd48e254405fb27297ee1fb8xxxx", "title": "title-xxxx" }'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object | 变更信息。 |  |
| appCodeRepoSn | string | 代码仓库唯一标识。 | cebf021afe6848578c97a1f6a253xxxx |
| appName | string | 应用名。 | my-web-service |
| autoDeleteBranchWhenEnd | boolean | 结束后是否自动删除分支。 | true |
| branch | string | 变更代码分支。 | master |
| creatorId | string | 创建者云效 id。 | creator-id-xxx |
| gmtCreate | string | 创建时间。 | 2024-09-01 00:00:00 |
| gmtModified | string | 修改时间。 | 2024-09-01 00:00:00 |
| name | string | 变更名称。 | name-xxx |
| originBranch | string | 代码分支源分支。 | master |
| originBranchRevisionSha | string | 代码分支源分支版本。 | c229f22024535638af41838daa43af1e6d46xxxx |
| ownerId | string | 拥有者 ID。 | 1c83bd48e254405fb27297ee1fb8xxxx |
| sn | string | 唯一标识符。 | eb4aee827214408e8d2dda49f0c0xxxx |
| state | string | 状态：INIT 初始化, WAIT 等待中, AUDITING 审核中, PASS 审核通过, FAILED 审核不通过, CANCELED 已取消, NO\_NEED 无需审核。 | INIT |
| type | string | 变更类型：APP。 | APP |

## **返回示例**

`{ "appCodeRepoSn": "cebf021afe6848578c97a1f6a253xxxx", "appName": "my-web-service", "autoDeleteBranchWhenEnd": true, "branch": "master", "creatorId": "creator-id-xxx", "gmtCreate": "2024-09-01 00:00:00", "gmtModified": "2024-09-01 00:00:00", "name": "name-xxx", "originBranch": "master", "originBranchRevisionSha": "c229f22024535638af41838daa43af1e6d46xxxx", "ownerId": "1c83bd48e254405fb27297ee1fb8xxxx", "sn": "eb4aee827214408e8d2dda49f0c0xxxx", "state": "INIT", "type": "APP" }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。