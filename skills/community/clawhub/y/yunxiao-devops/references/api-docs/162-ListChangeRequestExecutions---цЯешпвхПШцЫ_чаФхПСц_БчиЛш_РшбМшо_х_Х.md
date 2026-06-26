# ListChangeRequestExecutions - 查询变更研发流程运行记录

通过OpenAPI查询变更研发流程运行记录。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 应用交付 | 变更 | 只读 |

## **请求语法**

`GET https://{domain}/oapi/v1/appstack/organizations/{organizationId}/apps/{appName}/changeRequests/{sn}/executions`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| appName | string | path | 是 | 应用名。 | my-web-service |
| sn | string | path | 是 | 变更标识符。 | eb4aee827214408e8d2dda49f0c0xxxx |
| perPage | number | query | 否 | 分页尺寸参数，决定一页最多返回多少对象。 | 20 |
| page | number | query | 否 | 页面分页时使用，用于获取下一页内容，默认第1页。 | 1 |
| orderBy | string | query | 否 | 分页排序属性，决定根据何种属性进行记录排序；推荐在实现严格遍历时，使用 id 属性。 | id |
| sort | string | query | 否 | 分页排序升降序，asc 为升序，desc 为降序；推荐在实现严格遍历时，使用升序。 | asc |
| releaseWorkflowSn | string | query | 是 | 流程唯一标识。 | eb4aee827214408e8d2dda49f0c0xxxx |
| releaseStageSn | string | query | 是 | 阶段唯一标识。 | eb4aee827214408e8d2dda49f0c0xxxx |
| organizationId | string | path | 是 | 组织 ID。 | ec766e63aee3437d9a51f334d6exxxxx |

## **请求示例**

`curl -X 'GET' \ 'https://test.rdc.aliyuncs.com/oapi/v1/appstack/organizations/ec766e63aee3437d9a51f334d6exxxxx/apps/my-web-service/changeRequests/sn-xxxx/executions?perPage=20&page=1&orderBy=id&sort=asc&releaseWorkflowSn=eb4aee827214408e8d2dda49f0c0xxxx&releaseStageSn=eb4aee827214408e8d2dda49f0c0xxxx' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object | 分页数据。 |  |
| current | number | 当前页数。 | 1 |
| pageSize | number | 每页大小。 | 10 |
| pages | number | 总页数。 | 10 |
| records | array | 数据列表。 |  |
| \- | object | 变更执行记录。 |  |
| commit | object | 变更执行记录版本。 |  |
| committedDate | string | 提交时间。 | 2024-09-01 00:00:00 |
| committerId | string | 提交人。 | 1c83bd48e254405fb27297ee1fb8xxxx |
| id | string | 变更执行记录版本 ID。 | id-xxx |
| runNumber | string | 运行序号。 | 123 |
| state | string | 阶段执行状态，可能的值：\[RUNNING SUCCESS FAILED CANCELED UNKNOWN\]。 | SUCCESS |
| total | number | 总数。 | 10 |

## **返回示例**

`{ "current": 1, "pageSize": 10, "pages": 10, "records": [ { "commit": { "committedDate": "2024-09-01 00:00:00", "committerId": "1c83bd48e254405fb27297ee1fb8xxxx", "id": "id-xxx" }, "runNumber": "123", "state": "SUCCESS" } ], "total": 10 }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。