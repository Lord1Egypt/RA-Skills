# ListRepositories - 查看仓库信息

通过 OpenAPI 查看仓库信息。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。
    
    | **产品** | **资源** | **所需权限** |
    | --- | --- | --- |
    | 制品仓库 | 制品仓库 | 只读 |
    

## **请求语法**

`GET https://{domain}/oapi/v1/packages/organizations/{organizationId}/repositories`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## 请求参数

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | 是 | 企业 Id。 | xxxxxxxx |
| repoTypes | string | query | 否 | 仓库类型，可选值 GENERIC/DOCKER/MAVEN/NPM/NUGET,查询多个仓库类型可以以逗号分割。 | MAVEN |
| repoCategories | string | query | 否 | 仓库模式，可选值 Hybrid/Local/Proxy/ProxyCache/Group,查询多个模式可以以逗号分割。 | Hybrid |
| perPage | integer | query | 否 | 每页数据量，默认值8。 |  |
| page | integer | query | 否 | 当前页面。 |  |

## **请求示例**

`curl -X 'GET' \ 'https://test.rdc.aliyuncs.com/oapi/v1/packages/organizations/xxxxxxxx/repositories?repoTypes=MAVEN&repoCategories=Hybrid&perPage={perPage}&page={page}' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | array |  |  |
| \- | object | 制品仓库。 |  |
| accessLevel | string | 公开性, PRIVATE:私有仓库（仅仓库成员可访问），INTERNAL：组织内可见（组织内成员均可访问）。 | PRIVATE |
| latestUpdate | string | 最近更新时间。 | 1729064771000 |
| repoCategory | string | 仓库模式。 | Hybrid |
| repoDesc | string | 仓库描述。 | 流水线构建出的软件包制品 |
| repoDescriptor | string | 仓库描述文件。 | {“enableMaxVersionPerArtifact”:false,“hybridDescriptor”:{“cacheExpireTime”:-1,“fuseTime”:180000,“metaCacheExpireTime”:1800,“proxies”:\[\]},“isOverwriteArtifact”:“N”,“maxVersionPerArtifact”:-1,“versionStrategy”:“CUSTOM”} |
| repoId | string | 仓库 Id。 | flow\_generic\_repo |
| repoName | string | 仓库名称。 | 流水线软件包仓库 |
| repoType | string | 仓库类型。 | GENERIC |
| star | boolean | 是否收藏。 | false |

## **返回示例**

`[ { "accessLevel": "PRIVATE", "latestUpdate": "1729064771000", "repoCategory": "Hybrid", "repoDesc": "流水线构建出的软件包制品", "repoDescriptor": "{\"enableMaxVersionPerArtifact\":false,\"hybridDescriptor\":{\"cacheExpireTime\":-1,\"fuseTime\":180000,\"metaCacheExpireTime\":1800,\"proxies\":[]},\"isOverwriteArtifact\":\"N\",\"maxVersionPerArtifact\":-1,\"versionStrategy\":\"CUSTOM\"}", "repoId": "flow_generic_repo", "repoName": "流水线软件包仓库", "repoType": "GENERIC", "star": false } ]`

## 错误码

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。