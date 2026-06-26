# alipay.open.sp.inteop.order.create (服务商一体化作业主单创建)

**接口用途**：服务商一体化作业主单创建

**文档地址**：https://opendocs.alipay.com/isv/5106b36b_alipay.open.sp.inteop.order.create

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

| 参数                        | 类型     | 必填 | 说明                             |
|---------------------------|--------|----|--------------------------------|
| `account`                 | string | 否  | 商户支付宝账号。如果作业子项中包含代商户入驻，则不传递此参数 |
| `service_market_order_no` | string | 否  | 服务市场订单号                        |

### 公共响应参数

| 参数         | 类型     | 必填 | 说明      |
|------------|--------|----|---------|
| `code`     | string | 是  | 网关返回码   |
| `msg`      | string | 是  | 网关返回码描述 |
| `sub_code` | string | 否  | 业务返回码   |
| `sub_msg`  | string | 否  | 业务返回码描述 |
| `sign`     | string | 是  | 签名      |

### 业务响应参数

| 参数                | 类型     | 必填 | 说明         |
|-------------------|--------|----|------------|
| `inteop_order_no` | string | 是  | 一体化作业开通主单号 |

### 错误码

| 错误码                              | 说明                         | 解决方案                                    |
|----------------------------------|----------------------------|-----------------------------------------|
| `SYSTEM_ERROR`                   | 系统繁忙                       | 服务器异常，可能发生了网络或者系统异常，商户可以用同样的请求发起重试      |
| `INVALID_PARAMETER`              | 参数有误                       | 请根据接口返回的参数非法的具体错误信息，修改参数后进行重试           |
| `MARKET_ORDER_ITEM_NOT_EXIST`    | 服务市场订单商品信息不存在              | 服务市场订单商品信息不存在，请确认订单信息                   |
| `MERCHANT_CAN_NOT_LOGON`         | 商家支付宝账号被限制登录               | 商家支付宝账号被限制登录，请先解除限制                     |
| `MERCHANT_IS_NOT_EXIST`          | 商户不存在                      | 商户支付宝不存在，请确认支付宝账号                       |
| `MERCHANT_NOT_ACTIVED`           | 商家支付宝账号未激活                 | 请激活商家支付宝账号                              |
| `MERCHANT_NOT_CERTIFIED`         | 商家支付宝账号未实名认证               | 商家支付宝账号未实名认证                            |
| `MERCHANT_NOT_ENABLED`           | 商家支付宝账号被冻结或已注销             | 商家支付宝账号被冻结或已注销                          |
| `ORDER_ISV_PID_NOT_EQUAL`        | 服务市场订单服务商pid与当前登录服务商pid不一致 | 服务市场订单服务商pid与当前登录服务商pid不一致，请确认当前登录服务商信息 |
| `SAME_MERCHANT_CREATE_FREQUENT`  | 相同商户创建作业频繁                 | 相同商户创建作业过于频繁，请稍后重试                      |
| `SERVICE_MARKET_ORDER_NOT_EXIST` | 服务市场订单不存在                  | 服务市场订单不存在，请确认订单号是否正确                    |

### 请求示例

```bash
curl 'https://openapi.alipay.com/gateway.do?charset=UTF-8&method=alipay.open.sp.inteop.order.create&format=json&sign=${sign}&app_id=${appid}&version=1.0&sign_type=RSA2&timestamp=${now}' \
 -F 'app_auth_token=${app_auth_token}' \
 -F 'biz_content={
        "account":"1881579654267",
        "service_market_order_no":"202507140000000000219990"
}'
```

### 响应示例

```json
{
  "alipay_open_sp_inteop_order_create_response": {
    "code": "10000",
    "msg": "Success",
    "inteop_order_no": "2025052748926736"
  },
  "sign": "ERITJKEIJKJHKKKKKKKHJEREEEEEEEEEEE"
}
```

> 说明：本示例仅供参考。
