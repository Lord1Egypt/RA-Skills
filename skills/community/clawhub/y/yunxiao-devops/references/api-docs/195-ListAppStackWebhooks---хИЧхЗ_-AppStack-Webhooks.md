# ListAppStackWebhooks - 列出 AppStack Webhooks

获取 AppStack Webhooks 列表。

| **适用版本** | **企业标准版** |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/lingma/developer-reference/obtain-personal-access-token-1)。
-   获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 应用交付 | Webhook | 只读 |

## **请求语法**

`GET https://{domain}/oapi/v1/appstack/organizations/{organizationId}/hook`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | 是 | 组织 ID。 | ec766e6xxxxxxxxxx34d6exe671 |
| scopeType | string | query | 是 | 生效范围类型。 | ORGANIZATION |
| scopeId | string | query | 是 | 生效范围 ID。 | 企业 ID,应用名称 |
| channelType | string | query | 是 | 资源类型。 | WEBHOOK |

## **请求示例**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/appstack/organizations/ec766e6xxxxxxxxxx34d6exe671/hook?scopeType=ORGANIZATION&scopeId=企业ID,应用名称&channelType=WEBHOOK' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | array |  |  |
| \- | object | AppStack Webhook 配置。 |  |
| description | string | Webhook 描述，长度不超过256字符。 | 测试 |
| disabledExpired | string | 禁用过期时间。 |  |
| enabled | boolean | 是否启用。 | true |
| events | array | 事件列表。 |  |
| \- | object |  |  |
| action | string | 事件动作。 | Create |
| event | string | 事件类型。 | App |
| scopeId | string | 生效范围 ID。 | 企业 ID,应用名称 |
| scopeType | string | 生效范围类型，可能的值：\[ORGANIZATION APP\]。 | ORGANIZATION |
| sn | string | Webhook 唯一标识。 | c263a6749757xxxxxx2f45f2f80e |
| spec | object | Webhook 详细描述。 |  |
| token | string | Webhook 令牌，长度不超过128字符。 |  |
| type | string | 类型。 | WEBHOOK |
| url | string | Webhook URL，长度不超过1024字符。 | https://devops.aliyun.com/appstack/setting/webhooks |
| timeout | integer | 超时时间(秒)。 | 3 |
| type | string | 类型。 | WEBHOOK |

## **返回示例**

`[ { "description": "测试", "disabledExpired": "", "enabled": true, "events": [ { "action": "Create", "event": "App" } ], "scopeId": "企业ID,应用名称", "scopeType": "ORGANIZATION", "sn": "c263a6749757xxxxxx2f45f2f80e", "spec": { "token": "", "type": "WEBHOOK", "url": "https://devops.aliyun.com/appstack/setting/webhooks" }, "timeout": 3, "type": "WEBHOOK" } ]`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。