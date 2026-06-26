# GetProjectTemplateFieldConfig - 获取项目模板字段配置

通过 OpenAPI 获取项目模板字段配置。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。
    
    | **产品** | **资源** | **所需权限** |
    | --- | --- | --- |
    | 项目协作 | 项目模板 | 只读 |
    

## **请求语法**

`GET https://{domain}/oapi/v1/projex/organizations/{organizationId}/projectTemplates/{id}/fields`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| id | string | path | 是 | 模板唯一标识。 | a5c253d622cc8521793e08\*\*\*\* |
| organizationId | string | path | 是 | organizationId。 | 5ebbc0228123212b59xxxxx |

## **请求示例**

`curl -X 'GET' \ 'https://test.rdc.aliyuncs.com/oapi/v1/projex/organizations/{organizationId}/projectTemplates/a5c253d622cc8521793e08****/fields' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | array |  |  |
| \- | object |  |  |
| defaultValue | string | 默认值。 | test |
| description | string | 描述。 | test |
| id | string | 字段 id。 | id |
| name | string | 名称。 | test |
| options | array | 可选值。 |  |
| \- | object | 可选值。 |  |
| displayValue | string | 可选值的显示值。 | 测试 |
| id | string | id。 | 1 |
| value | string | 可选值。 | 测试 |
| valueEn | string | 可选值的英文。 | test |
| required | boolean | 是否必填。 | true |
| type | string | 字段类型，区分不同的类型，如系统字段：NativeField，用户自定义字段：CustomField。 | NativeField |

## **返回示例**

`[ { "defaultValue": "test", "description": "test", "id": "id", "name": "test", "options": [ { "displayValue": "测试", "id": "1", "value": "测试", "valueEn": "test" } ], "required": true, "type": "NativeField" } ]`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。