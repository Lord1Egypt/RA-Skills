# alipay.open.sp.inteop.sync.notify (服务商一体化作业消息通知)

**接口用途**：服务商一体化作业消息通知，如：所有节点的审核结果汇总通知、商户确认通知、申请单结束通知

**文档地址**：https://opendocs.alipay.com/isv/aa5adc1e_alipay.open.sp.inteop.sync.notify

**说明**：本接口为支付宝消息推送接口，不是主动调用接口。开发者需要在开放平台控制台配置应用网关（NOTIFY_URL），支付宝会将通知
POST 到该地址。

---

### 通知公共参数

| 参数              | 类型     | 必填 | 说明                    |
|-----------------|--------|----|-----------------------|
| `notify_id`     | string | 是  | 通知ID                  |
| `utc_timestamp` | string | 是  | 消息发送时的服务端时间（毫秒时间戳）    |
| `msg_method`    | string | 是  | 消息接口名称                |
| `app_id`        | string | 是  | 消息接受方的应用id            |
| `version`       | string | 是  | 版本号，1.0或1.1（1.1为标准消息） |
| `biz_content`   | string | 是  | 消息报文，见消息属性            |
| `sign`          | string | 是  | 签名                    |
| `sign_type`     | string | 是  | 签名类型：RSA2             |
| `charset`       | string | 是  | 编码集，如UTF-8            |

---

### 消息属性（biz_content）

| 参数                | 类型                            | 必填 | 说明               |
|-------------------|-------------------------------|----|------------------|
| `inteop_order_no` | string                        | 是  | 一体化作业主单号         |
| `status`          | string                        | 是  | 一体化作业单状态，见枚举值    |
| `sub_order_infos` | array\<InteopSubOrderInfoVO\> | 否  | 一体化作业子单信息，见下方子属性 |

#### status（一体化作业单状态）枚举值

| 枚举名   | 枚举值                   |
|-------|-----------------------|
| 初始化   | INIT                  |
| 审核中   | AUDITING              |
| 审核完成  | AUDIT_PASS            |
| 审核驳回  | REJECT                |
| 待商户确认 | WAIT_MERCHANT_CONFIRM |
| 商户已确认 | MERCHANT_CONFIRMED    |
| 申请成功  | APPLY_SUCCESS         |
| 已取消   | APPLY_CANCEL          |

#### sub_order_infos（子单信息）子参数

| 参数                 | 类型     | 必填 | 说明                                           |
|--------------------|--------|----|----------------------------------------------|
| `type`             | string | 是  | 一体化作业子单类型：AUTH-授权、SIGN-签约、SIGN_AND_AUTH-签约授权 |
| `sub_order_no`     | string | 是  | 一体化作业子单号                                     |
| `sub_order_status` | string | 是  | 一体化作业子单状态                                    |
| `reason`           | string | 否  | 用于记录子单的原因信息                                  |

---

### 通知应答

服务商接收到通知后，需要返回应答报文告知支付宝是否处理成功：

| 应答报文      | 是否重试 | 说明                     |
|-----------|------|------------------------|
| `success` | 否    | 消息处理成功，支付宝停止投递         |
| `fail`    | 是    | 消息处理失败，支付宝根据投递重试策略重新发送 |

**投递重试策略**：一般情况下，25小时内完成8次通知，除了第一次是实时投递外，后续重试间隔为：2m、10m、10m、1h、2h、6h、15h。

---

### 消息示例

```bash
curl -X POST 'NOTIFY_URL' \
 --header 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' \
 --data-urlencode 'charset=UTF-8' \
 --data-urlencode 'biz_content={
        "inteop_order_no":"2025082154665410",
        "status":"APPLY_SUCCESS",
        "sub_order_infos":[
                {
                        "reason":"营业执照不符合规范",
                        "sub_order_status":"AUDITING",
                        "sub_order_no":"2025082154665410",
                        "type":"AUTH"
                }
        ]
}' \
 --data-urlencode 'utc_timestamp=${now}' \
 --data-urlencode 'sign=${sign}' \
 --data-urlencode 'app_id=${appid}' \
 --data-urlencode 'version=1.1' \
 --data-urlencode 'sign_type=RSA2' \
 --data-urlencode 'notify_id=${notify_id}' \
 --data-urlencode 'msg_method=alipay.open.sp.inteop.sync.notify'
```

> 说明：NOTIFY_URL是开发者在开放平台控制台上设置的应用网关地址。