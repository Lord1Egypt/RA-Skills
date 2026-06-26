# DeleteArtifactVersion - 删除单个制品版本

通过 OpenAPI 删除单个制品版本。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。
    
    | **产品** | **资源** | **所需权限** |
    | --- | --- | --- |
    | 制品仓库 | 制品 | 读写 |
    

## **请求语法**

`DELETE https://{domain}/oapi/v1/packages/organizations/{organizationId}/repositories/{repoId}/artifacts/{id}/{versionId}`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | 是 | 企业 Id。 | xxxxxxxx |
| repoId | string | path | 是 | 仓库 Id。 | my-repo |
| id | integer | path | 是 | 制品 Id，参考来源：ListArtifacts - 查询制品信息 api。 | 123456 |
| versionId | integer | path | 是 | 制品版本 id, 参考来源：GetArtifact - 查询单个制品信息 api。 | 123456 |
| repoType | string | query | 是 | 仓库类型，可选值 GENERIC/DOCKER/MAVEN/NPM/NUGET/PYPI。 | MAVEN |

## **请求示例**

`curl -X 'DELETE' \ 'https://test.rdc.aliyuncs.com/oapi/v1/packages/organizations/xxxxxxxx/repositories/my-repo/artifacts/123456/123456?repoType=MAVEN' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | boolean | 是否删除成功。 | true |

## **返回示例**

`true`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。