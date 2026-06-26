# UpdateEffortRecord - 更新登记实际工时

通过 OpenAPI 更新登记实际工时。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。
    
    | **产品** | **资源** | **所需权限** |
    | --- | --- | --- |
    | 项目协作 | 实际工时 | 读写 |
    

## **请求语法**

`PUT https://{domain}/oapi/v1/projex/organizations/{organizationId}/workitems/{workitemId}/effortRecords/{id}`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | 是 | organizationId。 | 5ebbc0228123212b59xxxxx |
| workitemId | string | path | 是 | 工作项唯一标识。 |  |
| id | string | path | 是 | 工时记录是唯一标识。 |  |
| \- | object | body | 否 |  |  |
| actualTime | number | body | 是 | 实际工时。 | 1.5 |
| description | string | body | 否 | 工作描述。 | 描述内容 |
| gmtEnd | string | body | 是 | 工作开始结束日期。 |  |
| gmtStart | string | body | 是 | 工作开始日期。 |  |
| operatorId | string | body | 否 | 操作者的 useId，个人 token 时该参数无效。 | 操作者的 useId，个人 token 时该参数无效 |
| workType | string | body | 否 | 工作类型。 | 后端开发 |

## **请求示例**

`curl -X 'PUT' \ 'https://test.rdc.aliyuncs.com/oapi/v1/projex/organizations/{organizationId}/workitems/{workitemId}/effortRecords/{id}' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "actualTime": 1.5, "description": "描述内容", "gmtEnd": "", "gmtStart": "", "operatorId": "操作者的useId，个人token时该参数无效", "workType": "后端开发" }'`

## **返回参数**

无

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。