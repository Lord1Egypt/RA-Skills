# CreateProject - 创建项目

通过 OpenAPI 创建项目。

| **适用版本** | 标准版 |
| --- | --- |

## **前提条件**

-   获取[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)，并在API **请求语法**中替换 `{domain}` 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取`organizationId`，请前往**组织管理后台**的**基本信息**页面获取**组织 ID** 。

## **授权信息**

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 项目协作 | 项目 | 读写 |

## **请求语法**

`POST https://{domain}/oapi/v1/projex/organizations/{organizationId}/projects`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | 是 | organizationId |  |
| \- | object | body | 否 |  |  |
| customCode | string | body | 是 | 项目编号，四到六位大写字母，组织下唯一。 | CCDD |
| customFieldValues | object | body | 否 | 格式为：`{"fieldId":"value"}`，多值 value 用`","`隔开，例如：`{"fieldId":"value1,value2"}`。例如： {“priority”:“888853d622cc8eae793e085e27”} fieldId 的可选值为"获取项目模板"接口返回的字段 type 值为 CustomField 的字段，value 为希望更新的值 | map\[priority:888853d622cc8eae793e085e27\] |
| description | string | body | 否 | 描述 | test |
| name | string | body | 是 | 项目名称 | project-test |
| operatorId | string | body | 否 | 操作者的 userId，个人 token 时该参数无效。 | user-xxx |
| scope | string | body | 是 | 公开性，public or private，可能的值：\[public, private\]。 | public |
| templateId | string | body | 是 | 模板 id，可以通过获取项目模板列表接口获取。 | template-test |

## **请求示例**

`curl -X 'POST' \ 'https://{domain}/oapi/v1/projex/organizations/{organizationId}/projects' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "customCode": "CCDD", "customFieldValues": { }, "description": "test", "name": "project-test", "operatorId": "user-xxx", "scope": "public", "templateId": "template-test" }'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object |  |  |
| id | string | id | 1111 |

## **返回示例**

`{ "id": "1111" }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。