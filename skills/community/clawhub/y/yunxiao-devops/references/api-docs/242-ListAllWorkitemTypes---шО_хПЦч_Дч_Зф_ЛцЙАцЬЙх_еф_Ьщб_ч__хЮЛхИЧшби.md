# ListAllWorkitemTypes - 获取组织下所有工作项类型列表

通过 OpenAPI 获取组织下所有工作项类型列表。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。
    
    | **产品** | **资源** | **所需权限** |
    | --- | --- | --- |
    | 项目协作 | 工作项类型 | 只读 |
    

## **请求语法**

`GET https://{domain}/oapi/v1/projex/organizations/{organizationId}/workitemTypes`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| categories | string | query | 否 | 工作项类型，可选值为 Req，Bug，Task 等。 |  |
| organizationId | string | path | 是 | organizationId。 | 5ebbc0228123212b59xxxxx |

## **请求示例**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/projex/organizations/{organizationId}/workitemTypes?categories={categories}' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | array |  |  |
| \- | object |  |  |
| addUser | object |  |  |
| id | string | 用户 id。 | 674d96abd497cd558d68\*\*\*\* |
| name | string | 名称。 | name-xxx |
| categoryId | string | 所属类别的唯一标识，例如 Req，Task，Bug 等。 | Req |
| creator | object |  |  |
| id | string | 用户 id。 | 674d96abd497cd558d68\*\*\*\* |
| name | string | 名称。 | name-xxx |
| defaultType | boolean | 是否默认类型。 | true |
| description | string | 类型描述。 | 类型描述 |
| enable | boolean | 是否启用。 | true |
| gmtAdd | string | 添加时间。 |  |
| gmtCreate | string | 创建时间。 |  |
| id | string | 工作项类型唯一标识。 | bca48ee2a0976d38f48\*\*\*\* |
| name | string | 类型名称。 | 技术需求 |
| nameEn | string | 类型英文名。 | Technical Requirements |
| systemDefault | boolean | 是否系统默认。 | true |

## **返回示例**

`[ { "addUser": { "id": "674d96abd497cd558d68****", "name": "name-xxx" }, "categoryId": "Req", "creator": { "id": "674d96abd497cd558d68****", "name": "name-xxx" }, "defaultType": true, "description": "类型描述", "enable": true, "gmtAdd": "", "gmtCreate": "", "id": "bca48ee2a0976d38f48****", "name": "技术需求", "nameEn": "Technical Requirements", "systemDefault": true } ]`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。