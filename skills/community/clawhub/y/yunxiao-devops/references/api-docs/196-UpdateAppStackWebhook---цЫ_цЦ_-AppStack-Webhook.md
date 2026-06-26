# UpdateAppStackWebhook - 更新 AppStack Webhook

更新现有的 AppStack Webhook 配置。

| **适用版本** | **企业标准版** |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/lingma/developer-reference/obtain-personal-access-token-1)。
-   获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 应用交付 | Webhook | 读写 |

## **请求语法**

`POST https://{domain}/oapi/v1/appstack/organizations/{organizationId}/hook/{sn}/api`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | 是 | 组织 ID。 | ec766e6xxxxxxxxxx34d6exe671 |
| sn | string | path | 是 | Webhook 唯一标识。 | c263a6749757xxxxxxx842f45f2f80e |
| \- | object | body | 否 | 更新 AppStack Webhook 请求。 |  |
| description | string | body | 是 | Webhook 描述，长度不超过256字符。 | aa |
| events | array | body | 是 | 事件列表。 |  |
| \- | object | body | 否 |  |  |
| action | string | body | 是 | 事件动作，支持的动作类型：Create, Delete, Update, StatusUpdate。注意：不同事件类型支持的动作组合有限制，可能的值：\[Create Delete Update StatusUpdate\]。 | Create |
| event | string | body | 是 | 事件类型，支持的事件类型：AppOrchestration, ChangeOrder, ChangeRequest, Env, ReleaseStageExecution, VariableGroup, App，可能的值：\[AppOrchestration ChangeOrder ChangeRequest Env ReleaseStageExecution VariableGroup App\]。 | App |
| scopeId | string | body | 是 | 生效范围 ID。 | 企业 ID,应用名称 |
| scopeType | string | body | 是 | 生效范围类型，可能的值：\[ORGANIZATION APP\]。 | ORGANIZATION |
| sn | string | body | 是 | Webhook 唯一标识。 | c263a6749xxxxx2f45f2f80e |
| spec | object | body | 是 | Webhook 描述。 |  |
| token | string | body | 否 | Webhook 令牌，长度不超过128字符。 |  |
| type | string | body | 是 | 类型。 | WEBHOOK |
| url | string | body | 是 | Webhook URL，长度不超过1024字符。 | https://devops.aliyun.com/appstack/setting/webhooks |
| type | string | body | 是 | 类型。 | WEBHOOK |

## **请求示例**

`curl -X 'POST' \ 'https://{domain}/oapi/v1/appstack/organizations/ec766e6xxxxxxxxxx34d6exe671/hook/c263a6749757xxxxxxx842f45f2f80e/api' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "description": "aa", "events": [ { "action": "Create", "event": "App" } ], "scopeId": "企业ID,应用名称", "scopeType": "ORGANIZATION", "sn": "c263a6749xxxxx2f45f2f80e", "spec": { "token": "", "type": "WEBHOOK", "url": "https://devops.aliyun.com/appstack/setting/webhooks" }, "type": "WEBHOOK" }'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
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

`{ "description": "测试", "disabledExpired": "", "enabled": true, "events": [ { "action": "Create", "event": "App" } ], "scopeId": "企业ID,应用名称", "scopeType": "ORGANIZATION", "sn": "c263a6749757xxxxxx2f45f2f80e", "spec": { "token": "", "type": "WEBHOOK", "url": "https://devops.aliyun.com/appstack/setting/webhooks" }, "timeout": 3, "type": "WEBHOOK" }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。