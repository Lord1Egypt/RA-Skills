# CreateWorkitem - 创建工作项

通过 OpenAPI 创建工作项。

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

`POST https://{domain}/oapi/v1/projex/organizations/{organizationId}/workitems`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | 是 | 组织 ID | 5ebbc0228123212b59\*\*\*\* |
| \- | object |  |  |  |  |
| assignedTo | string | body | 是 | 指派人 userId | 674d96abd497cd558d68\*\*\*\* |
| customFieldValues | object | body | 否 | 格式为：{“fieldId”:“value”}，多值 value 用逗号隔开，例如：{“fieldId”: “value1,value2”}。fieldId 的可选值为“工作项创建时需要的字段信息”接口返回的字段 type 值为 SystemCustomField 和 CustomField 的字段，value 为希望更新的值。 | {“priority”:“888853d622cc8eae793e085e27”} |
| description | string | body | 否 | 工作项描述 | 描述 test |
| labels | array\[string\] | body | 否 | 关联的标签 ID 列表 | f2f52de5cac7656371fba2\*\*\*\* |
| parentId | string | body | 否 | 父工作项 ID | beda1775d1c3eca7dbdff5\*\*\*\* |
| participants | array\[string\] | body | 否 | 参与人 userId 列表 | 674d96abd497cd558d68\*\*\*\* |
| spaceId | string | body | 是 | 空间 ID，如果是项目就是项目的 ID。 | bfbb5f44f3aaab11460cd1\*\*\*\* |
| sprint | string | body | 否 | 关联的迭代 ID | 1c0d8bc0115fdf76bc33ac\*\*\*\* |
| subject | string | body | 是 | 工作项标题 | 标题 test |
| trackers | array\[string\] | body | 否 | 抄送人 userId 列表 | 674d96abd497cd558d68\*\*\*\* |
| verifier | string | body | 否 | 验证人 userId | 674d96abd497cd558d68\*\*\*\* |
| versions | array\[string\] | body | 否 | 关联的版本 ID 列表 | bfbb5f44f3aaab11460cd1\*\*\*\* |
| workitemTypeId | string | body | 是 | 工作项类型 ID，可以从该接口获取：[ListWorkitemTypes - 获取工作项类型列表](https://help.aliyun.com/zh/yunxiao/developer-reference/listworkitemtypes)。 | bca48ee2a0976d38f48\*\*\*\* |

## **请求示例**

`curl -X 'POST' \ 'https://openapi-rdc.aliyuncs.com/oapi/v1/projex/organizations/{organizationId}/workitems' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "assignedTo": "67da65f8048beaa8b097****", "description": "描述test", "labels": ["f2f52de5cac7656371fba2****"], "participants": ["67da65f8048beaa8b097****"], "spaceId": "bfbb5f44f3aaab11460cd1****", "sprint": "1c0d8bc0115fdf76bc33ac****", "subject": "标题test", "trackers": ["67da65f8048beaa8b097****"], "workitemTypeId": "9uy29901re573f561d69****" }'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object |  |  |
| id | string | 工作项 ID | 7c6da1002a65113899df73\*\*\*\* |

## **返回示例**

`{"id":"7c6da1002a65113899df73****"}`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。