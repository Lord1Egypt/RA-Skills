# GetWorkitemTypeFieldConfig - 获取工作项类型字段配置

通过 OpenAPI 获取工作项类型字段配置。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。
    
    | **产品** | **资源** | **所需权限** |
    | --- | --- | --- |
    | 项目协作 | 工作项类型字段配置 | 只读 |
    

## **请求语法**

`GET https://{domain}/oapi/v1/projex/organizations/{organizationId}/projects/{projectId}/workitemTypes/{id}/fields`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| organizationId | string | path | 是 | organizationId。 | 5ebbc0228123212b59xxxxx |
| projectId | string | path | 是 | 项目唯一标识。 |  |
| id | string | path | 是 | 工作项类型 id。 |  |

## **请求示例**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/projex/organizations/{organizationId}/projects/{projectId}/workitemTypes/{id}/fields' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | array |  |  |
| \- | object |  |  |
| cascadingOptions | object |  |  |
| mustSelectLeaf | boolean | 是否必须选择叶子节点。 | true |
| optionsList | array | 选项列表。 | \[\] |
| \- | object |  |  |
| children | array\[string\] |  |  |
| defaultValue | string | 默认值。 | 12233 |
| description | string | 描述。 | 描述 |
| format | string | 字段格式，目前支持的有 list、multiList、date、dateTime、int、float、string、text、user、multiUser、cascading、file、 tag、sprint、version 分别对应 单选、多选、日期、时间、整型、浮点、单行文本、多行文本、用户、多选用户、层级字段、文件、标签、迭代、版本。 | list |
| id | string | 字段 id。 | 126553d622cc8521793e08\*\*\*\* |
| name | string | 名称。 | 名称 |
| options | array | 可选值。 |  |
| \- | object |  |  |
| displayValue | string | 可选值值显示值。 | 111 |
| id | string | 字段 id。 | 126553d622cc8521793e08\*\*\*\* |
| value | string | 可选值值。 | 111 |
| valueEn | string | 可选值值英文。 | 111 |
| required | boolean | 是否必填。 | true |
| showWhenCreate | boolean | 创建时是否展示。 | true |
| type | string | 字段类型,区分不同的类型，如系统字段：NativeField，用户自定义字段：CustomField。 | NativeField |

## **返回示例**

`[ { "cascadingOptions": { "mustSelectLeaf": true, "optionsList": [] }, "defaultValue": "12233", "description": "描述", "format": "list", "id": "126553d622cc8521793e08****", "name": "名称", "options": [ { "displayValue": "111", "id": "126553d622cc8521793e08****", "value": "111", "valueEn": "111" } ], "required": true, "showWhenCreate": true, "type": "NativeField" } ]`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。