# GetApplication - 查找应用详情

通过OpenAPI查找应用详情。

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

`GET https://{domain}/oapi/v1/appstack/organizations/{organizationId}/apps/{appName}`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| appName | string | path | 是 | 应用名。 | my-web-service |
| organizationId | string | path | 是 | 组织 ID。 | ec766e63aee3437d9a51f334d6exxxxx |

## **请求示例**

`curl -X 'GET' \ 'https://test.rdc.aliyuncs.com/oapi/v1/appstack/organizations/anyOrganizationId/apps/my-web-service' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object | AppStack 应用模型。 |  |
| appTemplateDisplayName | string | 应用模板展示名称。 | app-template-display-name |
| appTemplateName | string | 应用模板名称。 | app-template-name |
| creatorId | string | 应用创建者 ID。 | bd9e3c6d-624f-4580-af7d-c5e26f1exxxx |
| description | string | 描述。 | description |
| gmtCreate | string | 创建时间。 | 2024-09-01 00:00:00 |
| name | string | 应用名。 | app-name |
| tags | array | 标签。 | \["java"\] |

## **返回示例**

`{ "appTemplateDisplayName": "app-template-display-name", "appTemplateName": "app-template-name", "creatorId": "bd9e3c6d-624f-4580-af7d-c5e26f1exxxx", "description": "description", "gmtCreate": "2024-09-01 00:00:00", "name": "app-name", "tags": ["Java"] }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。