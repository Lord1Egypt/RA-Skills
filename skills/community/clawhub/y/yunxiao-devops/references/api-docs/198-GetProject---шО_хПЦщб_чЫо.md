# GetProject - 获取项目

通过 OpenAPI 获取项目。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。
    
    | **产品** | **资源** | **所需权限** |
    | --- | --- | --- |
    | 项目协作 | 项目 | 只读 |
    

## **请求语法**

`GET https://{domain}/oapi/v1/projex/organizations/{organizationId}/projects/{id}`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| id | string | path | 是 | 项目ID。在项目详情的页面url中可以获取到，例如如下的urlhttps://devops.aliyun.com/projex/project/589c53d622cc8521793e08\*\*\*\*。 | 589c53d622cc8521793e08\*\*\*\* |
| organizationId | string | path | 是 | 组织ID，企业管理后台的页面url中可以获取到，例如如下的url: https://devops.aliyun.com/org-admin/6232xxxxxx42694c8cd/profile。 | 6232xxxxxx42694c8cd |

## **请求示例**

`curl -X 'GET' \ 'https://test.rdc.aliyuncs.com/oapi/v1/projex/organizations/{organizationId}/projects/589c53d622cc8521793e08****' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object |  |  |
| id | string | 项目的ID，是该项目的唯一标识。 | baef\*\*\*\*accd |
| name | string | 项目名称。 | project-test |
| description | string | 项目的描述。 | test |
| creator | object | 修改人。 |  |
| id | string | 修改人用户ID。 | 674d96abd497cd558d68\*\*\*\* |
| name | string | 修改人名称。 | user-name-xxx |
| modifier | object | 修改人。 |  |
| id | string | 修改人用户ID。 | 674d96abd497cd558d68\*\*\*\* |
| name | string | 修改人用户名。 | user-name-xxx |
| scope | string | 公开类型，枚举值为： public、private。 | public |
| status | object | 状态。 |  |
| id | string | 状态ID。 | 1111 |
| name | string | 状态名称。 | 进行中 |
| customCode | string | 编号。 | CCDD |
| customFieldValues | array(object) | 自定义字段值。 |  |
| fieldId | string | 自定义字段 ID。 | fieldId1 |
| fieldName | string | 自定义字段名称。 | field-test |
| values | array(object) |  |  |
| displayValue | string | 自定义值的显示名称。 | 111 |
| identifier | string | 自定义值的唯一标识。 | 111 |
| icon | string | icon，图标的 url。 | xxx |
| gmtCreate | string | 创建时间的时间戳。 | 1740018075 |
| gmtModified | string | 更新时间的时间戳。 | 1740018075 |

## **返回示例**

`{ "creator": { "id": "674d96abd497cd558d68****", "name": "user-name-xxx" }, "customCode": "CCDD", "customFieldValues": [ { "fieldId": "fieldId1", "fieldName": "field-test", "values": [ { "displayValue": "111", "identifier": "111" } ] } ], "description": "test", "gmtCreate": "1740018075", "gmtModified": "1740018075", "icon": "xxx", "id": "1111", "logicalStatus": "normal", "modifier": { "id": "674d96abd497cd558d68****", "name": "user-name-xxx" }, "name": "project-test", "scope": "public", "status": { "id": "1111", "name": "进行中" } }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。