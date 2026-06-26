# ListAppReleaseStageRuns - 批量查询研发阶段执行记录

批量查询研发阶段执行记录。

| 适用版本 | 标准版 |
| --- | --- |

## 服务接入点与授权信息

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。
    
    | **产品** | **资源** | **所需权限** |
    | --- | --- | --- |
    | 应用交付 | 发布阶段 | 只读 |
    

## 请求语法

`GET https://{domain}/oapi/v1/appstack/organizations/{organizationId}/apps/{appName}/releaseWorkflows/{releaseWorkflowSn}/releaseStages/{releaseStageSn}/executions`

## 请求头

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## 请求参数

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| appName | string | path | 是 | 应用名。 | my-web-service |
| releaseWorkflowSn | string | path | 是 | 发布流程唯一序列号。 | 3f472a12b15d4f418ad6227bb85f787c |
| releaseStageSn | string | path | 是 | 发布流程阶段唯一序列号。 | 6b4c53eee9a842c6a11235b29d002a81 |
| pagination | string | query | 否 | 分页模式参数：keyset 表示键集分页，不传表示页码分页。 | keyset |
| perPage | number | query | 否 | 分页尺寸参数，决定一页最多返回多少对象。 | 20 |
| orderBy | string | query | 否 | 分页排序属性，决定根据何种属性进行记录排序；推荐在实现严格遍历时，使用 id 属性。 | id |
| sort | string | query | 否 | 分页排序升降序，asc 为升序，desc 为降序；推荐在实现严格遍历时，使用升序。 | asc |
| nextToken | string | query | 否 | 键集分页 token，获取第一页数据时无需传入，否则需要传入前一页查询结果中的 nextToken 字段。 | token |
| page | number | query | 否 | 页码分页时使用，用于获取下一页内容。 | 1 |
| organizationId | string | path | 是 | 组织 ID。 | ec766e63aee3437d9a51f334d6exe671 |

## 请求示例

`curl -X 'GET' \ 'https://test.rdc.aliyuncs.com/oapi/v1/appstack/organizations/ec766e63aee3437d9a51f334d6exe671/apps/my-web-service/releaseWorkflows/3f472a12b15d4f418ad6227bb85f787c/releaseStages/6b4c53eee9a842c6a11235b29d002a81/executions?pagination=keyset&perPage=20&orderBy=id&sort=asc&nextToken=token&page=1' \ -H 'accept: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## 返回参数

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object | 分页接口所返回的列表。 |  |
| current | number | 页码分页时存在该字段，表示当前页。 | 1 |
| data | array | 分页结果数据。 |  |
| \- | object | 阶段实例信息。 |  |
| endTime | string | 流水线执行结束时间。 | 2024-01-01 00:00:00 |
| number | string | 流水线执行编号。 | 123 |
| startTime | string | 流水线执行开始时间。 | 2024-01-01 00:00:00 |
| state | string | 流水线执行状态。 | SUCCESS |
| triggerMode | string | 触发方式：1人工触发，2定时触发，3代码提交触发，5流水线触发，6 WEBHOOK 触发。 | 1 |
| nextToken | string | 采用键值分页时存在该字段，用于传给分页接口，迭代获取下一页数据。 | token |
| pages | number | 页码分页时存在该字段，表示总页数。 | 10 |
| perPage | number | 页码分页时存在该字段，表示每页大小。 | 10 |
| total | number | 页码分页时存在该字段，表示结果总数。 | 100 |

## 返回示例

`{ "current": 1, "data": [ { "endTime": "2024-01-01 00:00:00", "number": "123", "startTime": "2024-01-01 00:00:00", "state": "SUCCESS", "triggerMode": "1" } ], "nextToken": "token", "pages": 10, "perPage": 10, "total": 100 }`

## 错误码

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。