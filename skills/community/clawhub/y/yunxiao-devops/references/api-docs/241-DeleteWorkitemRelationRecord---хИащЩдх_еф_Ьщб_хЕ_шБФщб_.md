# DeleteWorkitemRelationRecord - 删除工作项关联项

通过 OpenAPI 删除工作项关联项。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。
    
    | **产品** | **资源** | **所需权限** |
    | --- | --- | --- |
    | 项目协作 | 工作项相关项 | 读写 |
    

## **请求语法**

`DELETE https://{domain}/oapi/v1/projex/organizations/{organizationId}/workitems/{id}/relationRecords`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| id | string | path | 是 | 工作项唯一标识。 |  |
| organizationId | string | path | 是 | organizationId。 |  |
| \- | object | body | 否 |  |  |
| operatorId | string | body | 否 | 操作者的 useId，个人 token 时该参数无效。 | 操作者的 useId，个人 token 时该参数无效 |
| relationType | string | body | 否 | 关联类型，可选值为 PARENT、SUB、ASSOCIATED、DEPEND\_ON、DEPENDED\_BY 分别对应父项，子项，关联项、依赖项、支撑项。 | ASSOCIATED |
| workitemId | string | body | 否 | 关联的工作项 id。 | beda1775d1c3eca7dbdff5\*\*\*\* |

## **请求示例**

`curl -X 'DELETE' \ 'https://{domain}/oapi/v1/projex/organizations/{organizationId}/workitems/{id}/relationRecords' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "operatorId": "操作者的useId，个人token时该参数无效", "relationType": "ASSOCIATED", "workitemId": "beda1775d1c3eca7dbdff5****" }`

## **返回参数**

无

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。