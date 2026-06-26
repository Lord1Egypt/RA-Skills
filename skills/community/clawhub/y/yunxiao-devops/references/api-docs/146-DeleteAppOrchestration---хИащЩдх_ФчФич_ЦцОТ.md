# DeleteAppOrchestration - 删除应用编排

通过 OpenAPI删除应用编排。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。
    
    | **产品** | **资源** | **所需权限** |
    | --- | --- | --- |
    | 应用交付 | 应用编排 | 读写 |
    

## **请求语法**

`DELETE https://{domain}/oapi/v1/appstack/organizations/{organizationId}/apps/{appName}/orchestrations/{sn}`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| appName | string | path | 是 | 应用名。 | my-web-service |
| sn | string | path | 是 | 应用编排唯一序列号。 | my-web-service@KUBERNETES |
| organizationId | string | path | 是 | 组织 ID。 | 99d1\*\*\*\*71d4 |

## **请求示例**

`curl -X 'DELETE' \ 'https://test.rdc.aliyuncs.com/oapi/v1/appstack/organizations/anyOrganizationId/apps/my-web-service/orchestrations/my-web-service@KUBERNETES' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | boolean | 调用是否成功。 | true |

## **返回示例**

`{ "success": true }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。