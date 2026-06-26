# SearchAppTemplates - 搜索应用模板

通过 OpenAPI 搜索应用模板。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。
    
    | **产品** | **资源** | **所需权限** |
    | --- | --- | --- |
    | 应用交付 | 应用模板 | 只读 |
    

## **请求语法**

`GET https://{domain}/oapi/v1/appstack/organizations/{organizationId}/appTemplates:search`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| pagination | string | query | 是 | 分页模式参数，目前只支持键集分页 keyset 模式。 | keyset |
| perPage | number | query | 否 | 分页尺寸参数，决定一页最多返回多少对象。 | 20 |
| orderBy | string | query | 是 | 分页排序属性，决定根据何种属性进行记录排序；推荐在实现严格遍历时，使用 id 属性。 | id |
| sort | string | query | 否 | 分页排序升降序，asc 为升序，desc 为降序；推荐在实现严格遍历时，使用升序。 | asc |
| nextToken | string | query | 否 | 键集分页 token，获取第一页数据时无需传入，否则需要传入前一页查询结果中的 nextToken 字段。 | token |
| displayNameKeyword | string | query | 否 | 按展示名进行模糊搜索的关键字。 | my-app-template |
| page | number | query | 否 | 页码分页时使用，用于获取下一页内容。 | 1 |
| organizationId | string | path | 是 | 组织 ID。 | 99d1\*\*\*\*71d4 |

## **请求示例**

`curl -X 'GET' \ 'https://test.rdc.aliyuncs.com/oapi/v1/appstack/organizations/anyOrganizationId/appTemplates:search?pagination=keyset&perPage=20&orderBy=id&sort=asc&nextToken=token&displayNameKeyword=my-app-template' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object | 分页接口所返回的列表。 |  |
| current | number | 页码分页时存在该字段，表示当前页。 | 1 |
| data | array | 分页结果数据。 |  |
| \- | object | 应用模板。 |  |
| cover | string | 应用模板封面。 | http://xxxxxxx |
| creatorId | string | 应用模板创建人。 | xxxxxx |
| description | string | 应用模板描述。 | app-template-description-xxx |
| displayName | string | 应用模板展示名称。 | app-template-display-name-xxx |
| gmtCreate | string | 应用模板创建时间。 | 2024-09-01 00:00:00 |
| gmtModified | string | 应用模板修改时间。 | 2024-09-01 00:00:00 |
| modifierId | string | 应用模板修改人。 | xxxxxx |
| name | string | 应用模板名称。 | app-template-name-xxx |
| type | string | 应用模板类型。 | CUSTOMIZE |
| nextToken | string | 采用键值分页时存在该字段，用于传给分页接口，迭代获取下一页数据。 | token |
| pages | number | 页码分页时存在该字段，表示总页数。 | 10 |
| perPage | number | 页码分页时存在该字段，表示每页大小。 | 10 |
| total | number | 页码分页时存在该字段，表示结果总数。 | 100 |

## **返回示例**

`{ "current": 1, "data": [ { "cover": "http://xxxxxxx", "creatorId": "xxxxxx", "description": "app-template-description-xxx", "displayName": "app-template-display-name-xxx", "gmtCreate": "2024-09-01 00:00:00", "gmtModified": "2024-09-01 00:00:00", "modifierId": "xxxxxx", "name": "app-template-name-xxx", "type": "CUSTOMIZE" } ], "nextToken": "token", "pages": 10, "perPage": 10, "total": 100 }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。