# ListApplications - 分页查找应用详情

通过OpenAPI分页查找应用详情。

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

`GET https://{domain}/oapi/v1/appstack/organizations/{organizationId}/apps:search`

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
| sort | string | query | 否 | 分页排序为升降序，asc 为升序，desc 为降序；推荐在实现严格遍历时，使用升序。 | asc |
| nextToken | string | query | 否 | 键集分页 token，获取第一页数据时无需传入，否则需要传入前一页查询结果中的 nextToken 字段。 | 0286da51e61e4cf9a7056ef1a4fexxxx |
| organizationId | string | path | 是 | 组织 ID。 | ec766e63aee3437d9a51f334d6exxxxx |
| tags | string | query | 否 | 应用标签，使用逗号隔开，每个标签名需要进行 urlencode。 | tag1,tag2,%E4%B8%AD%E6%96%87%E5%A3%B9%E5%8F%B7 |

## **请求示例**

`curl -X 'GET' \ 'https://test.rdc.aliyuncs.com/oapi/v1/appstack/organizations/organization-id-xxx/apps:search?pagination=keyset&orderBy=id&perPage=20&sort=asc&nextToken=token&tags=tag1,tag2,%E4%B8%AD%E6%96%87%E5%A3%B9%E5%8F%B7' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object | 分页接口所返回的列表。 |  |
| data | array | 分页结果数据。 |  |
| \- | object | AppStack 应用模型。 |  |
| appTemplateDisplayName | string | 应用模板展示名称。 | app-template-display-name |
| appTemplateName | string | 应用模板名称。 | app-template-name |
| creatorId | string | 应用创建者 ID。 | bd9e3c6d-624f-xxxx-af7d-c5e26f1ed0f0 |
| description | string | 描述。 | description |
| gmtCreate | string | 创建时间。 | 2024-09-01 00:00:00 |
| name | string | 应用名。 | app-name |
| nextToken | string | 采用键值分页时存在该字段，用于传给分页接口，迭代获取下一页数据。 | 0286da51e61e4cf9a7056ef1a4fexxxx |

## **返回示例**

`{ "data": [ { "appTemplateDisplayName": "app-template-display-name", "appTemplateName": "app-template-name", "creatorId": "bd9e3c6d-624f-xxxx-af7d-c5e26f1ed0f0", "description": "description", "gmtCreate": "2024-09-01 00:00:00", "name": "app-name" } ], "nextToken": "0286da51e61e4cf9a7056ef1a4fexxxx" }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。