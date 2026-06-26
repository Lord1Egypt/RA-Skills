# UpdateSprint - 更新迭代

通过 OpenAPI 更新迭代。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。
    
    | **产品** | **资源** | **所需权限** |
    | --- | --- | --- |
    | 项目协作 | 迭代 | 读写 |
    

## **请求语法**

`PUT https://{domain}/oapi/v1/projex/organizations/{organizationId}/projects/{projectId}/sprints/{id}`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| projectId | string | path | 是 | 项目唯一标识。 | 589c53d622cc8521793e08\*\*\*\* |
| id | string | path | 是 | 迭代唯一标识。 | 892153d622cc8521793e08\*\*\*\* |
| organizationId | string | path | 是 | organizationId。 | 5ebbc0228123212b59xxxxx |
| \- | object | body | 否 |  |  |
| capacityHours | integer | body | 否 | 迭代的工时容量（小时）。 | 100 |
| description | string | body | 否 | 迭代描述。 | 迭代信息 |
| endDate | string | body | 否 | 结束日期。 | 2025-02-20 |
| name | string | body | 是 | 迭代名称。 | test |
| operatorId | string | body | 否 | 操作者的 userId，个人 token 时该参数无效。 | 674d96abd497cd558d68\*\*\*\* |
| owners | array\[string\] | body | 否 | 迭代负责人列表。 | \["user1","user2"\] |
| startDate | string | body | 否 | 开始日期 应该是yyyy-MM-dd的格式。 | 2025-02-20 |

## **请求示例**

`curl -X 'PUT' \ 'https://test.rdc.aliyuncs.com/oapi/v1/projex/organizations/{organizationId}/projects/589c53d622cc8521793e08****/sprints/892153d622cc8521793e08****' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "capacityHours": 0, "description": "迭代信息", "endDate": "2025-02-20", "name": "test", "operatorId": "674d96abd497cd558d68****", "owners": [ "user1","user2" ], "startDate": "2025-02-20" }'`

## **返回参数**

无

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。