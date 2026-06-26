# ant.merchant.expand.bizaccess.order.cancel (开通进度主动撤销)

**接口用途**：用于服务商代商户开通主动撤销。

**文档地址**：https://opendocs.alipay.com/isv/8913b5b3_ant.merchant.expand.bizaccess.order.cancel

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

| 参数         | 类型     | 必填 | 说明   |
|------------|--------|----|------|
| `order_id` | string | 是  | 主单id |

### 公共响应参数

| 参数         | 类型     | 必填 | 说明      |
|------------|--------|----|---------|
| `code`     | string | 是  | 网关返回码   |
| `msg`      | string | 是  | 网关返回码描述 |
| `sub_code` | string | 否  | 业务返回码   |
| `sub_msg`  | string | 否  | 业务返回码描述 |
| `sign`     | string | 是  | 签名      |

### 业务响应参数

无业务响应参数

### 错误码

| 错误码                    | 说明          | 解决方案                                        |
|------------------------|-------------|---------------------------------------------|
| `SYSTEM_ERROR`         | 系统繁忙        | 服务器异常，可能发生了网络或者系统异常，导致服务调用失败，商户可以用同样的请求发起重试 |
| `INVALID_PARAMETER`    | 参数有误        | 请根据接口返回的参数非法的具体错误信息，修改参数后进行重试               |
| `ORDER_STATUS_INVALID` | 当前申请单状态无法撤销 | 当前申请单状态无法撤销，请耐心等待                           |

### 请求示例

```bash
curl 'https://openapi.alipay.com/gateway.do?charset=UTF-8&method=ant.merchant.expand.bizaccess.order.cancel&format=json&sign=${sign}&app_id=${appid}&version=1.0&sign_type=RSA2&timestamp=${now}' \
 -F 'app_auth_token=${app_auth_token}' \
 -F 'biz_content={
        "order_id":"2024546y546754865"
}'
```

### 响应示例

```json
{
  "ant_merchant_expand_bizaccess_order_cancel_response": {
    "code": "10000",
    "msg": "Success"
  },
  "sign": "ERITJKEIJKJHKKKKKKKHJEREEEEEEEEEEE"
}
```

> 说明：本示例仅供参考。