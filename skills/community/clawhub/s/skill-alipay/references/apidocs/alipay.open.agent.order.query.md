# alipay.open.agent.order.query (查询申请单状态)

**接口用途**：代签约产品提交后，查询对应申请单的情况。

**文档地址**：https://opendocs.alipay.com/isv/bd1943c2_alipay.open.agent.order.query

### 公共请求参数

| 参数               | 类型     | 必填 | 说明                               |
|------------------|--------|----|----------------------------------|
| `app_id`         | string | 是  | 支付宝分配给开发者的应用ID                   |
| `method`         | string | 是  | 接口名称                             |
| `format`         | string | 否  | 仅支持JSON                          |
| `charset`        | string | 是  | 请求使用的编码格式，如utf-8, gbk, gb2312等   |
| `sign_type`      | string | 是  | 签名算法类型：RSA2或RSA，推荐使用RSA2         |
| `sign`           | string | 是  | 商户请求参数的签名串                       |
| `timestamp`      | string | 是  | 发送请求的时间，格式yyyy-MM-dd HH:mm:ss    |
| `version`        | string | 是  | 接口版本，固定为1.0                      |
| `app_auth_token` | string | 否  | 应用授权令牌                           |
| `biz_content`    | string | 是  | 请求参数的集合，除公共参数外所有请求参数都必须放在这个参数中传递 |

### 业务请求参数

| 参数         | 类型     | 必填 | 说明                                                            |
|------------|--------|----|---------------------------------------------------------------|
| `batch_no` | string | 是  | ISV代商户操作事务编号，通过调用alipay.open.agent.create（开启代商户签约、创建应用事务）接口返回 |

### 公共响应参数

| 参数         | 类型     | 必填 | 说明      |
|------------|--------|----|---------|
| `code`     | string | 是  | 网关返回码   |
| `msg`      | string | 是  | 网关返回码描述 |
| `sub_code` | string | 否  | 业务返回码   |
| `sub_msg`  | string | 否  | 业务返回码描述 |
| `sign`     | string | 是  | 签名      |

### 业务响应参数

| 参数                           | 类型                              | 必填   | 说明                                       |
|------------------------------|---------------------------------|------|------------------------------------------|
| `order_status`               | string                          | 是    | 支付宝商户入驻申请单状态，见下方枚举值                      |
| `order_no`                   | string                          | 是    | 签约单号                                     |
| `merchant_pid`               | string                          | 是    | 商户pid                                    |
| `confirm_url`                | string                          | 特殊可选 | 商户确认签约链接，只有申请单状态在MERCHANT_CONFIRM状态下才会返回 |
| `agent_app_id`               | string                          | 特殊可选 | 代理创建的应用ID，商户确认成功后才返回应用ID                 |
| `reject_reason`              | string                          | 特殊可选 | 审核失败的拒绝原因，只有审核失败才会返回该值                   |
| `restrict_infos`             | array\<SignRestrictInfo\>       | 否    | 受限信息，见下方子属性                              |
| `product_agent_status_infos` | array\<ProductAgentStatusInfo\> | 否    | 申请单中每个产品的签约状态，见下方子属性                     |

#### order_status（申请单状态）枚举值

| 枚举名       | 枚举值                           | 说明                                        |
|-----------|-------------------------------|-------------------------------------------|
| 暂存        | MERCHANT_INFO_HOLD            | 提交事务出现业务校验异常时，会暂存申请单信息，可以调用业务接口修正参数，并重新提交 |
| 审核中       | MERCHANT_AUDITING             | 申请信息正在人工审核中                               |
| 待商户确认     | MERCHANT_CONFIRM              | 申请信息审核通过，等待联系人确认签约或授权                     |
| 商户确认成功    | MERCHANT_CONFIRM_SUCCESS      | 商户同意签约或授权                                 |
| 商户超时未确认   | MERCHANT_CONFIRM_TIME_OUT     | 商户受到确认信息15天内未确认，需要重新提交申请信息                |
| 审核失败或商户拒绝 | MERCHANT_APPLY_ORDER_CANCELED | 申请信息审核被驳回，或者商户选择拒绝签约或授权                   |

#### restrict_infos（受限信息）子参数

| 参数                     | 类型     | 必填 | 说明                 |
|------------------------|--------|----|--------------------|
| `restrict_product`     | string | 是  | 产品码，支付宝定义的产品码      |
| `restrict_version`     | string | 否  | 受限版本：02-受限版、04-极速版 |
| `restrict_reason`      | string | 否  | 受限的原因              |
| `restrict_reason_code` | string | 否  | 受限原因编码             |

#### product_agent_status_infos（产品签约状态）子参数

| 参数              | 类型     | 必填 | 说明            |
|-----------------|--------|----|---------------|
| `product_name`  | string | 否  | 产品名称          |
| `product_code`  | string | 否  | 产品编码          |
| `status`        | string | 否  | 产品签约状态，见下方枚举值 |
| `reject_reason` | string | 否  | 产品被驳回的原因      |

#### product_agent_status_infos.status（产品签约状态）枚举值

| 枚举名             | 枚举值     | 说明                     |
|-----------------|---------|------------------------|
| none            | 未签约     | 还没有签约该产品               |
| valid           | 已生效     | 合约已经生效，不需要再签约          |
| restrictValid   | 受限生效    | 合约已经生效，但是资料不全，功能受限     |
| audit           | 审核中     | 已经有合约在审核中，请等待审核完成      |
| waitConfirm     | 待商户确认协议 | 合约已经审核通过，需要商户确认后合约才生效  |
| auditReject     | 审核未通过   | -                      |
| invalid         | 合约失效    | 曾经签过合约，但已经失效了，可以重新发起签约 |
| restrictInvalid | 受限失效    | 受限合约失效了                |

### 错误码

| 错误码                       | 说明               | 解决方案                         |
|---------------------------|------------------|------------------------------|
| `INVALID_BATCH_NO`        | 事务编号batch_no不能为空 | 事务编号参数batch_no不能为空           |
| `BATCH_IS_NOT_EXIST`      | 代商户操作事务编号不存在     | 请检查事务编号是否有效                  |
| `INVALID_PARAMETER`       | 参数有误             | 检查必填参数是否为空，长度是否超限            |
| `SYSTEM_ERROR`            | 系统繁忙             | 系统内部错误，请稍后重试                 |
| `NO_APP_PERMISSION`       | APPID不匹配         | 请检查当前调用的appId和创建事务的appId是否匹配 |
| `BATCH_STATUS_NOT_SUBMIT` | 事务没有正常提交         | 请先将对应的事务提交                   |

### 请求示例

```bash
curl 'https://openapi.alipay.com/gateway.do?charset=UTF-8&method=alipay.open.agent.order.query&format=json&sign=${sign}&app_id=${appid}&version=1.0&sign_type=RSA2&timestamp=${now}' \
 -F 'app_auth_token=${app_auth_token}' \
 -F 'biz_content={
        "batch_no":"2017110616474516400082883"
}'
```

### 响应示例

```json
{
  "alipay_open_agent_order_query_response": {
    "code": "10000",
    "msg": "Success",
    "order_status": "MERCHANT_INFO_HOLD",
    "confirm_url": "https://openhome.alipay.com/isv/settling/confirm.htm?orderNo=20180627015000000000009202531926",
    "order_no": "20211020034000100000027428505085",
    "agent_app_id": "2017111108241348",
    "reject_reason": "图片涉黄",
    "merchant_pid": "390284792319804",
    "restrict_infos": [
      {
        "restrict_product": "I1011000100000000001",
        "restrict_version": "02",
        "restrict_reason": "经营资质不符合要求",
        "restrict_reason_code": "001"
      }
    ],
    "product_agent_status_infos": [
      {
        "product_name": "当面付收单",
        "product_code": "FACE_TO_FACE_PAYMENT",
        "status": "none|valid|restrictValid...",
        "reject_reason": "请您在签约时上传与账户主体一致的证件。"
      }
    ]
  },
  "sign": "ERITJKEIJKJHKKKKKKKHJEREEEEEEEEEEE"
}
```

> 说明：本示例仅供参考。