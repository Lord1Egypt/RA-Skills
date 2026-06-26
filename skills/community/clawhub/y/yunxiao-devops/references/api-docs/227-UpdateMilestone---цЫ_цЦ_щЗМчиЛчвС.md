# UpdateMilestone - 更新里程碑

通过 OpenAPI 更新里程碑。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。
    
    | **产品** | **资源** | **所需权限** |
    | --- | --- | --- |
    | 项目协作 | 里程碑 | 读写 |
    

## **请求语法**

`PUT https://{domain}/oapi/v1/projex/organizations/{organizationId}/projects/{projectId}/milestones/{id}`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | 是 | organizationId。 | 5ebbc0228123212b59xxxxx |
| projectId | string | path | 是 | 项目唯一标识。 | project-id-xxx |
| id | string | path | 是 | 里程碑唯一标识。 |  |
| \- | object | body | 否 |  |  |
| actualEndDate | string | body | 否 | 实际完成时间，只有在状态改为已完成时才可以设置该值，格式是 yyyy-MM-dd。 |  |
| assignedTo | string | body | 否 | 负责人。 |  |
| description | string | body | 否 | 描述。 |  |
| operatorId | string | body | 否 | 操作者的 useId，个人 token 时该参数无效。 | 操作者的 useId，个人 token 时该参数无效 |
| planEndDate | string | body | 否 | 计划完成时间，格式是 yyyy-MM-dd。 |  |
| status | string | body | 否 | 状态。 |  |
| subject | string | body | 否 | 标题。 |  |

## **请求示例**

`curl -X 'PUT' \ 'https://test.rdc.aliyuncs.com/oapi/v1/projex/organizations/{organizationId}/projects/{projectId}/milestones/{id}' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "actualEndDate": "", "assignedTo": "", "description": "", "operatorId": "操作者的useId，个人token时该参数无效", "planEndDate": "", "status": "", "subject": "" }'`

## **返回参数**

无

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。