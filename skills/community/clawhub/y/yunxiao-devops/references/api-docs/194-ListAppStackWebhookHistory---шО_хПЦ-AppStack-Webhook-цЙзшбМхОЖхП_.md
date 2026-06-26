# ListAppStackWebhookHistory - 获取 AppStack Webhook 执行历史

获取指定 Webhook 的历史执行历史列表。

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

`GET https://{domain}/oapi/v1/appstack/organizations/{organizationId}/hook/{sn}/logs/api`

## **请求语法**

```
GET https://{domain}/oapi/v1/appstack/organizations/{organizationId}/hook/{sn}/logs/api
```

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | 是 | 组织 ID。 | ec766e6xxxxxxxxxx34d6exe671 |
| sn | string | path | 是 | Webhook 唯一标识。 | c263a67497xxxxxxxxe842f45f2f80e |
| perPage | integer | query | 否 | 每页数量，可选参数。不为空时必须大于0且小于50。 | 10 |
| page | integer | query | 否 | 页码，可选参数。不为空时必须大于等于0。 | 1 |
| orderBy | string | query | 否 | 排序字段，可选参数。不为空时必须为 gmtCreate。 | gmtCreate |
| sort | string | query | 否 | 排序方向，可选参数。不为空时必须为 desc 或 asc。 | desc |

## **请求示例**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/appstack/organizations/ec766e6xxxxxxxxxx34d6exe671/hook/c263a67497xxxxxxxxe842f45f2f80e/logs/api?perPage=10&page=1&orderBy=gmtCreate&sort=desc' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object | AppStack Webhook 历史响应。 |  |
| current | integer | 当前页码。 | 1 |
| data | array | 历史数据列表。 |  |
| \- | object | AppStack Webhook 历史日志。 |  |
| action | string | 事件动作。 | Create |
| event | string | 事件类型。 | Env |
| eventData | object | 事件数据。 |  |
| headers | object | 请求头信息。 |  |
| payload | object | 事件数据。 |  |
| gmtEnd | string | 结束时间。 | 2025-09-19T06:05:18.000+00:00 |
| gmtEndLong | integer | 结束时间戳。 | 1758261917732 |
| gmtSend | string | 发送时间。 | 2025-09-19T06:05:18.000+00:00 |
| gmtSendLong | integer | 发送时间戳。 | 1758261917647 |
| refHookChannelSubscribeSn | string | 关联的 Webhook 订阅标识。 | aa1e7f6acxxxxxx830aa295fc66 |
| result | object | 执行结果。 |  |
| data | integer | HTTP 状态码。 | 302 |
| message | string | 结果消息。 | {“headers”:{“Connection”:“keep-alive”,“Content-Length”:“0”},“body”:"",“message”:“Found”} |
| success | boolean | 是否成功。 | false |
| sn | string | 日志唯一标识。 | ae321cxxxxxxxx087ffa612d5bc |
| state | integer | 执行状态。 | 2 |
| nextToken | string | 下一页令牌。 |  |
| pages | integer | 总页数。 | 1 |
| perPage | integer | 每页数量。 | 10 |
| total | integer | 总记录数。 | 6 |

## **返回示例**

`{ "current": 1, "data": [ { "action": "Create", "event": "Env", "eventData": { "headers": { }, "payload": { } }, "gmtEnd": "2025-09-19T06:05:18.000+00:00", "gmtEndLong": 1758261917732, "gmtSend": "2025-09-19T06:05:18.000+00:00", "gmtSendLong": 1758261917647, "refHookChannelSubscribeSn": "aa1e7f6acxxxxxx830aa295fc66", "result": { "data": 302, "message": "{"headers":{"Connection":"keep-alive","Content-Length":"0"},"body":"","message":"Found"}", "success": false }, "sn": "ae321cxxxxxxxx087ffa612d5bc", "state": 2 } ], "nextToken": "", "pages": 1, "perPage": 10, "total": 6 }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。