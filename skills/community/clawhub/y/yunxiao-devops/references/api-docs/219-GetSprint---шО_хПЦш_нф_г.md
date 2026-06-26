# GetSprint - 获取迭代

通过 OpenAPI 获取迭代。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。
    
    | **产品** | **资源** | **所需权限** |
    | --- | --- | --- |
    | 项目协作 | 迭代 | 只读 |
    

## **请求语法**

`GET https://{domain}/oapi/v1/projex/organizations/{organizationId}/projects/{projectId}/sprints/{id}`

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

## **请求示例**

`curl -X 'GET' \ 'https://test.rdc.aliyuncs.com/oapi/v1/projex/organizations/{organizationId}/projects/589c53d622cc8521793e08****/sprints/892153d622cc8521793e08****' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object |  |  |
| capacityHours | integer | 迭代工时容量（小时）。 | 100 |
| creator | object | 负责人。 |  |
| id | string | 用户 id。 | 674d96abd497cd558d68\*\*\*\* |
| name | string | 用户名。 | user-name-xxx |
| description | string | 描述。 | test |
| endDate | string | 结束日期。 | 1740018075 |
| gmtCreate | string | 创建时间的时间戳。 | 1740018075 |
| gmtModified | string | 更新时间的时间戳。 | 1740018075 |
| id | string | id。 | 1111 |
| locked | boolean | 是否被锁定。 | false |
| modifier | object | 负责人。 |  |
| id | string | 用户 id。 | 674d96abd497cd558d68\*\*\*\* |
| name | string | 用户名。 | user-name-xxx |
| name | string | 名称。 | sprint-test |
| owners | array | 负责人。 |  |
| \- | object | 负责人。 | \["user1","user2"\] |
| id | string | 用户 id。 | 674d96abd497cd558d68\*\*\*\* |
| name | string | 用户名。 | user-name-xxx |
| startDate | string | 开始日期。 | 1740018075 |
| status | string | 状态：TODO、DOING、ARCHIVED，分别对应未开始，进行中和已完成。 | TODO |

## **返回示例**

`{ "capacityHours": 100, "creator": { "id": "674d96abd497cd558d68****", "name": "user-name-xxx" }, "description": "test", "endDate": "1740018075", "gmtCreate": "1740018075", "gmtModified": "1740018075", "id": "1111", "locked": false, "modifier": { "id": "674d96abd497cd558d68****", "name": "user-name-xxx" }, "name": "sprint-test", "owners": [ { "id": "674d96abd497cd558d68****", "name": "user-name-xxx" } ], "startDate": "1740018075", "status": "TODO" }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。