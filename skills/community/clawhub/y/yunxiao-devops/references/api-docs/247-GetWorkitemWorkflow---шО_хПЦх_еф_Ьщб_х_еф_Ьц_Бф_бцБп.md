# GetWorkitemWorkflow - 获取工作项工作流信息

通过 OpenAPI 获取工作项工作流信息。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。
    
    | **产品** | **资源** | **所需权限** |
    | --- | --- | --- |
    | 项目协作 | 工作项类型字段配置 | 只读 |
    

## **请求语法**

`GET https://{domain}/oapi/v1/projex/organizations/{organizationId}/projects/{projectId}/workitemTypes/{id}/workflows`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| organizationId | string | path | 是 | organizationId。 | 5ebbc0228123212b59xxxxx |
| projectId | string | path | 是 | 项目唯一标识。 |  |
| id | string | path | 是 | 工作项类型 id。 |  |

## **请求示例**

`curl -X 'GET' \ 'https://test.rdc.aliyuncs.com/oapi/v1/projex/organizations/{organizationId}/projects/{projectId}/workitemTypes/{id}/workflows' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object |  |  |
| defaultStatusId | string | 默认状态 id。 | TODO |
| id | string | 工作流 id。 | 89c213d622cc8521793e08\*\*\*\* |
| name | string | 工作流名称。 | test |
| statuses | array | 包含的状态列表。 |  |
| \- | object |  |  |
| displayName | string | 显示名称。 | 待处理 |
| id | string | id。 | id-xxx |
| name | string | 名称。 | 待处理 |
| nameEn | string | 英文名称。 | TODO |

## **返回示例**

`{ "defaultStatusId": "TODO", "id": "89c213d622cc8521793e08****", "name": "test", "statuses": [ { "displayName": "待处理", "id": "id-xxx", "name": "待处理", "nameEn": "TODO" } ] }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。