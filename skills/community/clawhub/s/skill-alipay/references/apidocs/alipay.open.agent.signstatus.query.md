# alipay.open.agent.signstatus.query (查询商户某个产品的签约状态)

**接口用途**：主要用在isv代理商户签约场景，用来查询商户签约某个产品的签约状态，可以配合"第三方接入核心API"功能包里的接口使用

**文档地址**：https://opendocs.alipay.com/isv/319f304c_alipay.open.agent.signstatus.query

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

| 参数              | 类型              | 必填 | 说明                                                            |
|-----------------|-----------------|----|---------------------------------------------------------------|
| `pid`           | string          | 是  | isv要查询签约状态的商户账号，可以是支付宝账号pid（2088开头），也可以是商户的登录账号（邮箱或手机号）       |
| `product_codes` | array\<string\> | 是  | isv要查询商户签约状态的产品码，产品码是支付宝内部对产品的唯一标识，目前支持查询产品及产品码详情参见获取商家产品开通状态 |

### 公共响应参数

| 参数         | 类型     | 必填 | 说明      |
|------------|--------|----|---------|
| `code`     | string | 是  | 网关返回码   |
| `msg`      | string | 是  | 网关返回码描述 |
| `sub_code` | string | 否  | 业务返回码   |
| `sub_msg`  | string | 否  | 业务返回码描述 |
| `sign`     | string | 是  | 签名      |

### 业务响应参数

| 参数                 | 类型                             | 必填 | 说明                                   |
|--------------------|--------------------------------|----|--------------------------------------|
| `sign_status_list` | array\<ProductSignStatusInfo\> | 是  | 商户产品签约状态结果对象数组，返回本次查询的产品的签约状态，见下方子属性 |

#### sign_status_list（商户产品签约状态）子参数

| 参数             | 类型     | 必填 | 说明        |
|----------------|--------|----|-----------|
| `product_name` | string | 是  | 产品名称      |
| `product_code` | string | 是  | 产品编码      |
| `status`       | string | 是  | 签约状态，见枚举值 |

#### status（签约状态）枚举值

| 枚举名                       | 枚举值           |
|---------------------------|---------------|
| 未签约，表示还没有签约该产品            | none          |
| 已生效，表示合约已经生效，不需要再签约了      | valid         |
| 受限生效，表示合约已经生效，但是资料不全，功能受限 | restrictValid |

### 错误码

| 错误码                                | 说明                   | 解决方案                                                 |
|------------------------------------|----------------------|------------------------------------------------------|
| `SYSTEM_ERROR`                     | 系统繁忙                 | 服务器异常，可能发生了网络或者系统异常，导致服务调用失败，商户可以用同样的请求发起重试          |
| `INVALID_PARAMETER`                | 参数有误                 | 请根据接口返回的参数非法的具体错误信息，修改参数后进行重试                        |
| `MERCHANT_IS_NOT_EXIST`            | 商家支付宝账号不存在           | 请确认商家支付宝账号存在、正确且有效                                   |
| `QUERY_SIGN_STATUS_AUTH_NOT_MATCH` | 应用授权信息和要查询的商户信息不匹配   | 请检查应用授权token和要查询签约状态的商户是否匹配                          |
| `QUERY_SIGN_STATUS_NOT_AUTH`       | 接口自调用时不允许查询其它商户的签约状态 | 接口自调用时只能查询自己的签约状态，要查询其他商户的签约状态，请先让商户进行应用授权，再使用代理方式调用 |

### 请求示例

```bash
curl 'https://openapi.alipay.com/gateway.do?charset=UTF-8&method=alipay.open.agent.signstatus.query&format=json&sign=${sign}&app_id=${appid}&version=1.0&sign_type=RSA2&timestamp=${now}' \
 -F 'app_auth_token=${app_auth_token}' \
 -F 'biz_content={
        "pid":"支付宝账号：2088123451234543或手机号：13811111111或邮箱：123@xxx.com",
        "product_codes":[
                "I1011000100000000001"
        ]
}'
```

### 响应示例

```json
{
  "alipay_open_agent_signstatus_query_response": {
    "code": "10000",
    "msg": "Success",
    "sign_status_list": [
      {
        "product_name": "当面付收单",
        "product_code": "FACE_TO_FACE_PAYMENT",
        "status": "valid"
      }
    ]
  },
  "sign": "ERITJKEIJKJHKKKKKKKHJEREEEEEEEEEEE"
}
```

> 说明：本示例仅供参考。