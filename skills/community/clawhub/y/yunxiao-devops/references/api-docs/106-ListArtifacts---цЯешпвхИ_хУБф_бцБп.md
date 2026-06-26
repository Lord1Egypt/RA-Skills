# ListArtifacts - 查询制品信息

通过 OpenAPI 查询制品信息。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。
    
    | **产品** | **资源** | **所需权限** |
    | --- | --- | --- |
    | 制品仓库 | 制品 | 只读 |
    

## **请求语法**

`GET https://{domain}/oapi/v1/packages/organizations/{organizationId}/repositories/{repoId}/artifacts`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## 请求参数

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | 是 | 企业 Id | xxxxxxxx |
| repoId | string | path | 是 | 仓库 Id | my-repo |
| repoType | string | query | 是 | 仓库类型，可选值 GENERIC/DOCKER/MAVEN/NPM/NUGET | MAVEN |
| page | integer | query | 否 | 当前页码 |  |
| perPage | integer | query | 否 | 每页数据量，默认值10 | 10 |
| search | string | query | 否 | 根据包名进行检索 | junit |
| orderBy | string | query | 否 | 按指定方式排序: latestUpdate：按最近更新时间排序; gmtDownload: 按最近下载时间排序。默认值：latestUpdate。 | latestUpdate |
| sort | string | query | 否 | 排序顺序: asc: 从小到大; desc: 从大到小。默认值：desc。 | desc |

## **请求示例**

`curl -X 'GET' \ 'https://test.rdc.aliyuncs.com/oapi/v1/packages/organizations/xxxxxxxx/repositories/my-repo/artifacts?repoType=MAVEN&page=&perPage=10&search=junit&orderBy=latestUpdate&sort=desc' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | array |  |  |
| \- | object | 模块信息。 |  |
| downloadCount | integer | 下载次数。 | 100 |
| gmtDownload | integer | 最近下载时间。 | 1728557118000 |
| id | integer | 制品 id。 | 123456 |
| latestUpdate | integer | 最近更新时间。 | 1728557118000 |
| module | string | 模块名。 | mypackage |
| organization | string | 组织信息。 | com.aliyun |
| repositoryId | string | 仓库 id。 | my\_repo |
| versions | array | 版本列表。 |  |
| \- | object |  |  |
| createTime | integer | 创建时间。 | 1728557118000 |
| creator | string | 创建人。 | xxxx |
| gmtDownload | integer | 最新下载时间。 | 1728557118000 |
| id | integer | 制品版本 id。 | 123456 |
| modifier | string | 修改人。 | xxx |
| updateTime | integer | 修改时间。 | 1728557118000 |
| version | string | 版本号。 | 1.4 |

## **返回示例**

`[ { "downloadCount": 100, "gmtDownload": 1728557118000, "id": 123456, "latestUpdate": 1728557118000, "module": "my package", "organization": "com.aliyun", "repositoryId": "my_repo", "versions": [ { "createTime": 1728557118000, "creator": "xxxx", "gmtDownload": 1728557118000, "id": 123456, "modifier": "xxx", "updateTime": 1728557118000, "version": "1.4" } ] } ]`

## 错误码

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。