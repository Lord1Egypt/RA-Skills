# SearchProjects - 搜索项目

通过 OpenAPI 搜索项目。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。
    
    | **产品** | **资源** | **所需权限** |
    | --- | --- | --- |
    | 项目协作 | 项目 | 只读 |
    

## **请求语法**

`POST https://{domain}/oapi/v1/projex/organizations/{organizationId}/projects:search`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | 是 | 企业ID。 | 5ebbc0228123212b59xxxxx |
| \- | object | body | 否 |  |  |
| conditions | string | body | 否 | 过滤条件是一个 JSON 串，格式为{“conditionGroups”:\[\[filterObject,filterObject,…\]\]}， 目前支持 name,status,gmtCreate,creator,project.admin,logicalStatus 六个条件搜索，以下为一个完整的搜索条件(真实场景中可以按需选取对应的值){“conditionGroups”:\[\[{“className”:“status”,“fieldIdentifier”:“status”,“format”:“list”,“operator”:“CONTAINS”,“toValue”:null,“value”:\[“8a4058a71159b682541b0864”,“cc961a18adf770c6e423ccc5”,“faf4893ebf92851b6717511a9e”,“e22f2f8dcbffe9aa03eae7e8ba”\]},{“className”:“string”,“fieldIdentifier”:“name”,“format”:“input”,“operator”:“BETWEEN”,“toValue”:null,“value”:\[“ffffff”\]},{“className”:“date”,“fieldIdentifier”:“gmtCreate”,“format”:“input”,“operator”:“BETWEEN”,“toValue”:“2023-09-06 23:59:59”,“value”:\[“2023-08-03 00:00:00”\]},{“className”:“user”,“fieldIdentifier”:“creator”,“format”:“list”,“operator”:“CONTAINS”,“toValue”:null,“value”:\[“43578d02-c84c-4fef-8c34-50c05304809a”,“d222d052-4c0e-4a03-b961-bb3f5fd556a0”\]},{“className”:“user”,“fieldIdentifier”:“project.admin”,“format”:“multiList”,“operator”:“CONTAINS”,“toValue”:null,“value”:\[“d222d052-4c0e-4a03-b961-bb3f5fd556a0”,“bccd35ab-6380-4e03-b280-8b6f966e635c”\]},{“className”:“string”,“fieldIdentifier”:“logicalStatus”,“format”:“list”,“operator”:“CONTAINS”,“toValue”:null,“value”:\[“NORMAL”\]}\]\]}。 | {“conditionGroups”:\[\[{“className”:“string”,“fieldIdentifier”:“name”,“format”:“input”,“operator”:“BETWEEN”,“toValue”:null,“value”:\[“test”\]}\]\]} |
| extraConditions | string | body | 否 | 额外的过滤条件，该参数主要设定一个基础查询范围，例如我管理的、我参与的，我收藏的等。 可以参考页面的项目列表的 AJAX 接口 project/search/list 中的 extraConditions 参数。 |  |
| orderBy | string | body | 否 | 排序字段，目前只支持名称和创建时间，不填值则默认为 gmtCreate，gmtCreate：创建时间，name：名称。 | gmtCreate |
| page | integer | body | 否 | 分页参数，第几页。 | 1 |
| perPage | integer | body | 否 | 分页参数，每页大小，0-200，默认值20。 | 20 |
| sort | string | body | 否 | 排序方式，默认为 desc，desc 对应降序；asc 对应升序。 | desc |

## **请求示例**

`curl -X 'POST' \ 'https://test.rdc.aliyuncs.com/oapi/v1/projex/organizations/{organizationId}/projects:search' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "conditions": "{"conditionGroups":[[{"className":"string","fieldIdentifier":"name","format":"input","operator":"BETWEEN","toValue":null,"value":["test"]}]]}", "extraConditions": "", "orderBy": "gmtCreate", "page": 1, "perPage": 20, "sort": "desc" }'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | array(object) |  |  |
| creator | object | 修改人。 |  |
| id | string | 修改人 ID。 | 674d96abd497cd558d68\*\*\*\* |
| name | string | 修改人名称。 | user-name-xxx |
| customCode | string | 编号。 | CCDD |
| customFieldValues(object) | array | 自定义字段值。 |  |
| fieldId | string | 自定义字段 ID。 | fieldId1 |
| fieldName | string | 自定义字段名称。 | field-test |
| values | array(object) |  |  |
| identifier | string | 值的唯一标识。 | 111 |
| displayValue | string | 值的显示名称。 | 111 |
| description | string | 描述。 | test |
| gmtCreate | string | 创建时间的时间戳。 | 1740018075 |
| gmtModified | string | 更新时间的时间戳。 | 1740018075 |
| icon | string | icon。 | xxx |
| id | string | ID。 | 1111 |
| logicalStatus | string | 逻辑状态。 | normal |
| modifier | object | 修改人。 |  |
| id | string | 修改人 ID。 | 674d96abd497cd558d68\*\*\*\* |
| name | string | 修改人名称。 | user-name-xxx |
| name | string | 名称。 | project-test |
| scope | string | 公开类型，枚举值为： public、private。 | public |
| status | object | 状态。 |  |
| id | string | 状态 ID。 | 1111 |
| name | string | 状态名称。 | 进行中 |

## **返回示例**

`[ { "creator": { "id": "674d96abd497cd558d68****", "name": "user-name-xxx" }, "customCode": "CCDD", "customFieldValues": [ { "fieldId": "fieldId1", "fieldName": "field-test", "values": [ { "displayValue": "111", "identifier": "111" } ] } ], "description": "test", "gmtCreate": "", "gmtModified": "", "icon": "xxx", "id": "1111", "logicalStatus": "normal", "modifier": { "id": "674d96abd497cd558d68****", "name": "user-name-xxx" }, "name": "project-test", "scope": "public", "status": { "id": "1111", "name": "进行中" } } ]`

## **响应头**

| **参数** | **描述** | **示例值** |
| --- | --- | --- |
| x-next-page | 下一页。 | 2 |
| x-page | 当前页。 | 1 |
| x-per-page | 每页数据条数。 | 20 |
| x-prev-page | 上一页。 | 1 |
| x-total | 总数据量。 | 200 |
| x-total-pages | 总分页数。 | 10 |

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。