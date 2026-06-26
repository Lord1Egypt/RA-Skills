# ListMilestones - 获取里程碑列表

通过 OpenAPI 获取里程碑列表。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。
    
    | **产品** | **资源** | **所需权限** |
    | --- | --- | --- |
    | 项目协作 | 里程碑 | 只读 |
    

## **请求语法**

`GET https://{domain}/oapi/v1/projex/organizations/{organizationId}/projects/{id}/milestones`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| id | string | path | 是 | 项目唯一标识。 | project-id-xxx |
| organizationId | string | path | 是 | organizationId。 | 5ebbc0228123212b59xxxxx |
| status | string | query | 否 | 状态列表，多个用逗号隔开。 |  |
| page | integer | query | 否 | 页码。 |  |
| perPage | integer | query | 否 | 每页数据条数。 |  |

## **请求示例**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/projex/organizations/{organizationId}/projects/{id}/milestones?status={status}&page={page}&perPage={perPage}' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | array |  |  |
| \- | object |  |  |
| actualEndDate | string | 实际完成时间。 |  |
| assignedTo | object |  |  |
| id | string | 用户 id。 | 674d96abd497cd558d68\*\*\*\* |
| name | string | 名称。 | name-xxx |
| creator | object |  |  |
| id | string | 用户 id。 | 674d96abd497cd558d68\*\*\*\* |
| name | string | 名称。 | name-xxx |
| description | string | 描述。 | test |
| gmtCreate | string | 创建时间。 |  |
| gmtModified | string | 修改时间。 |  |
| id | string | id。 | id-xxx |
| modifier | object |  |  |
| id | string | 用户 id。 | 674d96abd497cd558d68\*\*\*\* |
| name | string | 名称。 | name-xxx |
| planEndDate | string | 计划完成时间。 |  |
| status | object |  |  |
| displayName | string | 显示名称。 | 待处理 |
| id | string | id。 | id-xxx |
| name | string | 名称。 | 待处理 |
| nameEn | string | 英文名称。 | TODO |
| subject | string | 名称。 | test |

## **返回示例**

`[ { "actualEndDate": "", "assignedTo": { "id": "674d96abd497cd558d68****", "name": "name-xxx" }, "creator": { "id": "674d96abd497cd558d68****", "name": "name-xxx" }, "description": "test", "gmtCreate": "", "gmtModified": "", "id": "id-xxx", "modifier": { "id": "674d96abd497cd558d68****", "name": "name-xxx" }, "planEndDate": "", "status": { "displayName": "待处理", "id": "id-xxx", "name": "待处理", "nameEn": "TODO" }, "subject": "test" } ]`

## **响应头**

| **参数** | **描述** | **示例值** |
| --- | --- | --- |
| x-next-page | 下一页。 |  |
| x-page | 当前页。 |  |
| x-per-page | 每页数据条数。 |  |
| x-prev-page | 上一页。 |  |
| x-total | 总数据量。 |  |
| x-total-pages | 总分页数。 |  |

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。