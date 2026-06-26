# UpdateApplication - 更新应用

通过OpenAPI更新应用。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 应用交付 | 应用 | 读写 |

## **请求语法**

`PUT https://{domain}/oapi/v1/appstack/organizations/{organizationId}/apps/{appName}`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| appName | string | path | 是 | 应用名。 | my-web-service |
| organizationId | string | path | 是 | 组织 ID。 | ec766e63aee3437d9a51f334d6exxxxx |
| \- | object | body | 否 | 应用信息修改入参。 |  |
| ownerId | string | body | 否 | 应用 owner ID。 | bd9e3c6d-624f-xxxx-xxxx-c5e26f1ed0f0 |
| tags | array | body | 否 | 应用标签（覆盖式更新：如果不需要更新，调用该接口时可以不传该参数；空列表代表清空标签。） | \["后端服务", "Java"\] |
| description | string | body | 否 | 应用描述。 | 这是一个Java后端应用 |

## **请求示例**

`curl -X 'PUT' \ 'https://test.rdc.aliyuncs.com/oapi/v1/appstack/organizations/organization-id-xxx/apps/my-web-service' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "ownerId": "bd9e3c6d-624f-xxxx-xxxx-c5e26f1ed0f0", "tags":["Java"], "description"："这是一个Java后端应用" }'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object | AppStack 应用模型。 |  |
| appTemplateDisplayName | string | 应用模板展示名称。 | app-template-display-name |
| appTemplateName | string | 应用模板名称。 | app-template-name |
| creatorId | string | 应用创建者 ID。 | bd9e3c6d-624f-xxxx-xxxx-c5e26f1ed0f0 |
| description | string | 描述。 | description |
| gmtCreate | string | 创建时间。 | 2024-09-01 00:00:00 |
| name | string | 应用名。 | app-name |
| tags | array | 标签。 | \["java"\] |

## **返回示例**

`{ "appTemplateDisplayName": "app-template-display-name", "appTemplateName": "app-template-name", "creatorId": "bd9e3c6d-624f-xxxx-xxxx-c5e26f1ed0f0", "description": "description", "gmtCreate": "2024-09-01 00:00:00", "name": "app-name", "tags":["Java"] }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。