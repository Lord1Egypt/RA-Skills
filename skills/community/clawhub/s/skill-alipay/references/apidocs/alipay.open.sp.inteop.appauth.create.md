# alipay.open.sp.inteop.appauth.create (服务商一体化开通作业添加代调用授权项)

**接口用途**：服务商一体化开通作业添加代调用授权项

**文档地址**：https://opendocs.alipay.com/isv/af483a46_alipay.open.sp.inteop.appauth.create

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

| 参数                | 类型     | 必填 | 说明                          |
|-------------------|--------|----|-----------------------------|
| `inteop_order_no` | string | 是  | 业务开通主单号                     |
| `isv_app_id`      | string | 是  | 申请授权的三方应用appid              |
| `out_biz_no`      | string | 否  | 外部关联单号，代调用授权成功之后会在授权通知里携带此值 |

### 公共响应参数

| 参数         | 类型     | 必填 | 说明      |
|------------|--------|----|---------|
| `code`     | string | 是  | 网关返回码   |
| `msg`      | string | 是  | 网关返回码描述 |
| `sub_code` | string | 否  | 业务返回码   |
| `sub_msg`  | string | 否  | 业务返回码描述 |
| `sign`     | string | 是  | 签名      |

### 业务响应参数

| 参数             | 类型     | 必填 | 说明  |
|----------------|--------|----|-----|
| `sub_order_no` | string | 是  | 子单号 |

### 错误码

| 错误码                             | 说明                         | 解决方案                               |
|---------------------------------|----------------------------|------------------------------------|
| `SYSTEM_ERROR`                  | 系统繁忙                       | 服务器异常，可能发生了网络或者系统异常，商户可以用同样的请求发起重试 |
| `INVALID_PARAMETER`             | 参数有误                       | 根据接口返回的参数非法的具体错误信息，修改参数后进行重试       |
| `EXIST_APP_AUTH_ORDER`          | 当前申请单下已经存在代调用开通项           | 取消已经存在的代调用授权子项或重新创建一个主单添加代调用授权子项   |
| `INTEOP_ORDER_NOT_EXIST`        | 作业主单记录不存在                  | 请检查作业主单是否存在                        |
| `INVALID_INTEOP_ORDER_NO`       | 作业主单 inteop_order_no必填     | 请在入参中赋值inteop_order_no             |
| `ISV_ORDER_STATUS_IS_FINAL`     | 主单状态非初始态，不可操作              | 重新创建一个新的作业主单                       |
| `ISV_PID_INCONSISTENCY`         | 无操作权限，当前服务商pid和主单服务商pid不一致 | 主单创建服务商需要和当前子单创建服务商是同一个人           |
| `NOT_MATCHED_VALIDATION_POLICY` | 请求数据不符合任何已配置的校验策略          | 请检查使用业务场景是否正确                      |
| `SP_MERCHANT_INF_NO_FIND`       | 服务商PID不存在                  | 服务商PID不存在                          |

### 请求示例

```bash
curl 'https://openapi.alipay.com/gateway.do?charset=UTF-8&method=alipay.open.sp.inteop.appauth.create&format=json&sign=${sign}&app_id=${appid}&version=1.0&sign_type=RSA2&timestamp=${now}' \
 -F 'app_auth_token=${app_auth_token}' \
 -F 'biz_content={
        "inteop_order_no":"2025071611667571",
        "isv_app_id":"2014072300007148",
        "out_biz_no":"2025xxxxxxx"
}'
```

### 响应示例

```json
{
  "alipay_open_sp_inteop_appauth_create_response": {
    "code": "10000",
    "msg": "Success",
    "sub_order_no": "2025071611667571"
  },
  "sign": "ERITJKEIJKJHKKKKKKKHJEREEEEEEEEEEE"
}
```

> 说明：本示例仅供参考。