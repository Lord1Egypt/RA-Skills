# ListProjectTemplates - 获取项目模板

通过 OpenAPI 获取项目模板。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。
    
    | **产品** | **资源** | **所需权限** |
    | --- | --- | --- |
    | 项目协作 | 项目模板 | 只读 |
    

## **请求语法**

`GET https://{domain}/oapi/v1/projex/organizations/{organizationId}/projectTemplates`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | 是 | organizationId。 | 5ebbc0228123212b59xxxxx |

## **请求示例**

`curl -X 'GET' \ 'https://test.rdc.aliyuncs.com/oapi/v1/projex/organizations/{organizationId}/projectTemplates' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | array |  |  |
| \- | object |  |  |
| creator | object | 修改人。 |  |
| id | string | 用户 id。 | 674d96abd497cd558d68\*\*\*\* |
| name | string | 用户名。 | user-name-xxx |
| description | string | 模板描述。 | 快速、有效的落地 Scrum，合理规划并形成交付节奏，持续提升敏捷交付能力 |
| gmtCreate | string | 创建时间的时间戳。 | 1740018075 |
| gmtModified | string | 更新时间的时间戳。 | 1740018075 |
| icon | string | 图标链接。 | test |
| id | string | id。 | 1111 |
| modifier | object | 修改人。 |  |
| id | string | 用户 id。 | 674d96abd497cd558d68\*\*\*\* |
| name | string | 用户名。 | user-name-xxx |
| name | string | 模板名。 | Scrum 敏捷交付空间 |
| type | integer | 模板类型 0-system/4-custom/16-instance。 | 0 |
| withControl | boolean | 是否是管控模板。 | true |

## **返回示例**

`[ { "creator": { "id": "674d96abd497cd558d68****", "name": "user-name-xxx" }, "description": "快速、有效的落地Scrum，合理规划并形成交付节奏，持续提升敏捷交付能力 ", "gmtCreate": "1740018075", "gmtModified": "1740018075", "icon": "test", "id": "1111", "modifier": { "id": "674d96abd497cd558d68****", "name": "user-name-xxx" }, "name": "Scrum敏捷交付空间", "type": 0, "withControl": true } ]`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。