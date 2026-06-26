# SearchWorkitems - 搜索工作项

通过 OpenAPI 搜索工作项，参数中 spaceId 为项目 id 或项目集 id，该接口不支持跨多个项目进行数据搜索。

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 项目协作 | 工作项 | 只读 |

## **请求语法**

### **中心版**

`POST https://{domain}/oapi/v1/projex/organizations/{organizationId}/workitems:search`

### **Region版**

```
POST https://{domain}/oapi/v1/projex/{organizationId}/workitems:search
```

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | -   是：中心版 -   否：Region版 | organizationId。 |  |
| \- | object | body | 否 |  |  |
| category | string | body | 是 | 搜索的工作项类型，例如 Req，多值用逗号隔开。 | Req |
| conditions | string | body | 否 | 过滤条件，是一个 json 串，格式为{"conditionGroups":\[\[filterObject,filterObject,...\]\]}， 每个字段如何拼接可参考需求列表页面过滤时请求的 ajax 接口: workitem/list. 可在页面上先选择好条件进行过滤，后直接取 workitem/list 接口中的 conditions 参数   几个常见的 filterObject:   标题包含 test 的条件：   {"fieldIdentifier": "subject","operator": "CONTAINS","value": \["test"\],"toValue": null,"className": "string","format": "input"},   状态包含指定状态的条件：   {"fieldIdentifier": "status","operator": "CONTAINS","value": \["28","30","32","100010"\],"toValue": null,"className": "status","format": "list"},   负责人包含用户 id 为5f2bfdacb69dd0f7311e2932的条件   {"fieldIdentifier": "assignedTo","operator": "CONTAINS","value": \["5f2bfdacb69dd0f7311e2932"\],"toValue": null,"className": "user","format": "list"}   创建人包含用户 id 为5f2bfdacb69dd0f7311e2932的条件   {"fieldIdentifier": "creator","operator": "CONTAINS","value": \["5f2bfdacb69dd0f7311e2932"\],"toValue": null,"className": "user","format": "list"}   包含标签 id 为1589a2b0ae967141c6929f1a78的条件   {"fieldIdentifier": "tag","operator": "CONTAINS","value": \["1589a2b0ae967141c6929f1a78"\],"toValue": null,"className": "tag","format": "multiList"}   更新时间介入的条件：   {"fieldIdentifier": "gmtCreate","operator": "BETWEEN","value": \["2022-04-01 00:00:00"\],"toValue": "2023-03-31 23:59:59","className": "dateTime","format": "input"}。 | {"conditionGroups":\[\[{"fieldIdentifier":"status","operator":"CONTAINS","value":\["100005","100010","154395"\],"toValue":null,"className":"status","format":"list"}\]\]} |
| orderBy | string | body | 否 | 排序字段，默认为 gmtCreate   gmtCreate：创建时间   name：名称。 | gmtCreate |
| page | integer | body | 否 | 分页参数，第几页。 | 1 |
| perPage | integer | body | 否 | 分页参数，每页大小，0-200，默认值20。 | 20 |
| sort | string | body | 否 | 排序方式，默认为 desc   desc：降序   asc：升序。 | desc |
| spaceId | string | body | 是 | 项目 id 或项目集 id。 |  |
| spaceType | string | body | 否 | 空间类型，Project（项目）或 Program（项目集），默认为 Project。 | Project |

## **请求示例**

### **中心版**

`curl -X 'POST' \ 'https://{domain}/oapi/v1/projex/organizations/{organizationId}/workitems:search' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "category": "Req", "conditions": "{"conditionGroups":[[{"fieldIdentifier":"status","operator":"CONTAINS","value":["100005","100010","154395"],"toValue":null,"className":"status","format":"list"}]]}", "orderBy": "gmtCreate", "page": 1, "perPage": 20, "sort": "desc", "spaceId": "", "spaceType": "Project" }'`

### **Region版**

```
curl -X 'POST' \
  'https://{domain}/oapi/v1/projex/{organizationId}/workitems:search' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \
  --data '
    {
        "category": "Req",
        "conditions": "{"conditionGroups":[[{"fieldIdentifier":"status","operator":"CONTAINS","value":["100005","100010","154395"],"toValue":null,"className":"status","format":"list"}]]}",
        "orderBy": "gmtCreate",
        "page": 1,
        "perPage": 20,
        "sort": "desc",
        "spaceId": "",
        "spaceType": "Project"
    }'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | array |  |  |
| \- | object |  |  |
| assignedTo | object |  |  |
| id | string | 用户 id。 | 674d96abd497cd558d68\*\*\*\* |
| name | string | 名称。 | name-xxx |
| categoryId | string | 工作项分类 id。 | Req |
| creator | object |  |  |
| id | string | 用户 id。 | 674d96abd497cd558d68\*\*\*\* |
| name | string | 名称。 | name-xxx |
| customFieldValues | array | 自定义字段值。 |  |
| \- | object |  |  |
| fieldFormat | string | 字段类型。 | User |
| fieldId | string | 字段 id。 | 126553d622cc8521793e08\*\*\*\* |
| fieldName | string | 字段名称。 | field-name-xxx |
| values | array | 字段值。 |  |
| \- | object |  |  |
| displayValue | string | 显示的名称。 |  |
| identifier | string | 值的唯一标识。 |  |
| description | string | 描述。 | test |
| formatType | string | 描述的格式，目前支持 RICHTEXT 和 MARKDOWN。 | RICHTEXT |
| gmtCreate | string | 创建时间。 |  |
| gmtModified | string | 修改时间。 |  |
| id | string | 工作项 id。 | id-2 |
| idPath | string | 工作项 idPath。 | id-1,id-2 |
| labels | array | 标签。 |  |
| \- | object |  |  |
| color | string | 颜色。 | test |
| id | string | id。 | id-xxx |
| name | string | 名称。 | test |
| logicalStatus | string | 逻辑状态, normal 为正常状态， archived 为归档状态。 | normal |
| modifier | object |  |  |
| id | string | 用户 id。 | 674d96abd497cd558d68\*\*\*\* |
| name | string | 名称。 | name-xxx |
| parentId | string | 父工作项 id。 | id-1 |
| participants | array | 参与人。 |  |
| \- | object |  |  |
| id | string | 用户 id。 | 674d96abd497cd558d68\*\*\*\* |
| name | string | 名称。 | name-xxx |
| serialNumber | string | 编号。 | DSDD-123 |
| space | object |  |  |
| id | string | id。 | id-xxx |
| name | string | 名称。 | test |
| sprint | object |  |  |
| id | string | id。 | id-xxx |
| name | string | 名称。 | test |
| status | object |  |  |
| displayName | string | 显示名称。 | 待处理 |
| id | string | id。 | id-xxx |
| name | string | 名称。 | 待处理 |
| nameEn | string | 英文名称。 | TODO |
| statusStageId | string | 状态阶段 id。 | id-xxx |
| subject | string | 标题。 | test |
| trackers | array | 跟踪人。 |  |
| \- | object |  |  |
| id | string | 用户 id。 | 674d96abd497cd558d68\*\*\*\* |
| name | string | 名称。 | name-xxx |
| updateStatusAt | string | 状态更新时间。 |  |
| verifier | object |  |  |
| id | string | 用户 id。 | 674d96abd497cd558d68\*\*\*\* |
| name | string | 名称。 | name-xxx |
| versions | array | 版本。 |  |
| \- | object |  |  |
| id | string | id。 | id-xxx |
| name | string | 名称。 | test |
| workitemType | object |  |  |
| id | string | id。 | id-xxx |
| name | string | 名称。 | test |

## **返回示例**

`[ { "assignedTo": { "id": "674d96abd497cd558d68****", "name": "name-xxx" }, "categoryId": "Req", "creator": { "id": "674d96abd497cd558d68****", "name": "name-xxx" }, "customFieldValues": [ { "fieldFormat": "User", "fieldId": "126553d622cc8521793e08****", "fieldName": "field-name-xxx", "values": [ { "displayValue": "", "identifier": "" } ] } ], "description": "test", "formatType": "RICHTEXT", "gmtCreate": "", "gmtModified": "", "id": "id-2", "idPath": "id-1,id-2", "labels": [ { "color": "test", "id": "id-xxx", "name": "test" } ], "logicalStatus": "normal", "modifier": { "id": "674d96abd497cd558d68****", "name": "name-xxx" }, "parentId": "id-1", "participants": [ { "id": "674d96abd497cd558d68****", "name": "name-xxx" } ], "serialNumber": "DSDD-123", "space": { "id": "id-xxx", "name": "test" }, "sprint": { "id": "id-xxx", "name": "test" }, "status": { "displayName": "待处理", "id": "id-xxx", "name": "待处理", "nameEn": "TODO" }, "statusStageId": "id-xxx", "subject": "test", "trackers": [ { "id": "674d96abd497cd558d68****", "name": "name-xxx" } ], "updateStatusAt": "", "verifier": { "id": "674d96abd497cd558d68****", "name": "name-xxx" }, "versions": [ { "id": "id-xxx", "name": "test" } ], "workitemType": { "id": "id-xxx", "name": "test" } } ]`

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