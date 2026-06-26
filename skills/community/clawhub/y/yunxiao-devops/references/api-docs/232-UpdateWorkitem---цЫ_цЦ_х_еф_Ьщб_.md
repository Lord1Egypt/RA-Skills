# UpdateWorkitem - 更新工作项

通过 OpenAPI 更新工作项。body的格式为一个jsonobject,格式为:{"fieldId":"value"}，如果是多值格式为:{"fieldId":\["value1"\],"value2"\]}。例如: 更改标题： {"subject":"test-update-by-api"}， 更改状态： {"status":"statusId"}， 更改负责人： {"assignedTo":"userId"}， 更改优先级： {"priority":"priorityId"}， fieldId的可选值可以通过\\"获取工作项类型字段配置\\"这个接口获取，value为希望更新的值。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。
    
    | **产品** | **资源** | **所需权限** |
    | --- | --- | --- |
    | 项目协作 | 工作项 | 读写 |
    

## **请求语法**

`PUT https://{domain}/oapi/v1/projex/organizations/{organizationId}/workitems/{id}`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| id | string | path | 是 | 工作项ID。 | 9a2b\*\*\*\*5ef1 |
| organizationId | string | path | 是 | 企业ID。 | 5ebbc0228123212b59xxxxx |
| \- | object | body | 是 |  | 格式为一个jsonobject,格式为:{"fieldId":"value"}，如果是多值格式为:{"fieldId":\["value1"\],"value2"\]}。例如: 更改标题： {"subject":"test-update-by-api"}， 更改状态： {"status":"statusId"}， 更改负责人： {"assignedTo":"userId"}， 更改优先级： {"priority":"priorityId"}， fieldId的可选值可以通过\\"获取工作项类型字段配置\\"这个接口获取，value为希望更新的值。 |

## **请求示例**

`curl -X 'PUT' \ 'https://test.rdc.aliyuncs.com/oapi/v1/projex/organizations/{organizationId}/workitems/{id}' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "subject":"test-update-by-api" }'`

## **返回参数**

无

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。