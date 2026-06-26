# alipay.open.agent.create (开启代商户签约、创建应用事务)

**接口用途**：在ISV代商户进行应用创建、产品签约时，用于开启一个操作事务，必须是第一个调用的接口。

- 场景1：ISV代商户进行应用创建、产品签约，最后提交事务后需要商户确认才能完成流程
- 场景2：服务市场订购及授权，使用订单授权凭证order_ticket开启预授权模式，该模式下提交事务后无需商户确认

**文档地址**：https://opendocs.alipay.com/isv/e2e357b4_alipay.open.agent.create

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

| 参数             | 类型           | 必填 | 说明                                   |
|----------------|--------------|----|--------------------------------------|
| `account`      | string       | 是  | isv代操作的商户账号，可以是支付宝账号，也可以是pid（2088开头） |
| `contact_info` | ContactModel | 是  | 商户联系人信息，包含联系人名称、手机、邮箱信息，见下方子属性       |
| `order_ticket` | string       | 否  | 订单授权凭证，若传入本参数，则对应事务提交后进入预授权模式        |

#### contact_info（商户联系人信息）子参数

| 参数               | 类型     | 必填 | 说明      |
|------------------|--------|----|---------|
| `contact_name`   | string | 是  | 联系人名称   |
| `contact_mobile` | string | 是  | 联系人手机号码 |
| `contact_email`  | string | 否  | 联系人邮箱   |

### 公共响应参数

| 参数         | 类型     | 必填 | 说明      |
|------------|--------|----|---------|
| `code`     | string | 是  | 网关返回码   |
| `msg`      | string | 是  | 网关返回码描述 |
| `sub_code` | string | 否  | 业务返回码   |
| `sub_msg`  | string | 否  | 业务返回码描述 |
| `sign`     | string | 是  | 签名      |

### 业务响应参数

| 参数             | 类型     | 必填 | 说明                                                                                       |
|----------------|--------|----|------------------------------------------------------------------------------------------|
| `batch_no`     | string | 是  | 本次代商户操作的全局唯一事务编号，后续代商户创建小程序、代签约当面付等产品、提交事务等接口都需要传递该batch_no值，且要确认只有init状态的batch_no才能发起调用 |
| `batch_status` | string | 是  | ISV代商户操作事务状态，见枚举值                                                                        |

#### batch_status（事务状态）枚举值

| 枚举名     | 枚举值  | 说明                                                       |
|---------|------|----------------------------------------------------------|
| init    | 初始状态 | 本接口alipay.open.agent.create返回init状态，只有init状态允许进行各种业务接口调用 |
| submit  | 提交状态 | 事务已到达终态，调用alipay.open.agent.confirm接口可以提交init状态的事务       |
| cancel  | 取消状态 | 事务已到达终态，调用alipay.open.agent.cancel接口可以取消init状态的事务        |
| timeout | 超时状态 | 事务已到达终态，init状态的事务在1个小时后会自动超时                             |

> 注意：只有init状态才允许进行接口调用，其它状态都是终态，不允许继续进行接口调用。

### 错误码

| 错误码                                | 说明                  | 解决方案                        |
|------------------------------------|---------------------|-----------------------------|
| `INVALID_PARAMETER`                | 参数有误                | 检查必填参数是否为空，长度是否超限           |
| `APP_INFO_NOT_EXIST`               | 应用信息不存在             | 请检查sdk中配置的应用appId是否正确       |
| `NOT_ISV_APP_TYPE`                 | 不是第三方应用类型，不允许进行代理调用 | 请检查应用类型是否是第三方应用             |
| `MERCHANT_IS_NOT_EXIST`            | 商家支付宝账号不存在          | 请确认商家支付宝账号存在、正确且有效          |
| `MERCHANT_NOT_ACTIVED`             | 商家支付宝账号未激活          | 请确认商家支付宝账号存在、正确且有效          |
| `MERCHANT_CAN_NOT_LOGON`           | 商家支付宝账号被限制登录        | 请确认商家支付宝账号存在、正确且有效          |
| `MERCHANT_NOT_ENABLED`             | 商家支付宝账号被冻结或已注销      | 请确认商家支付宝账号存在、正确且有效          |
| `MERCHANT_NOT_CERTIFIED`           | 商家支付宝账号未实名认证        | 请确认商家支付宝账号存在、正确且有效          |
| `INVALID_CONTACT_NAME`             | 联系人名称为空或乱码          | 请填写正确的商户联系人姓名，最大长度20个字符     |
| `INVALID_CONTACT_MOBILE`           | 手机号码格式错误            | 请填写正确的11位手机号码               |
| `INVALID_CONTACT_EMAIL`            | 邮箱格式错误              | 请填写正确的邮箱                    |
| `PRE_AUTH_TICKET_NOT_EXIST`        | 订单授权凭证不存在           | 请检查订单授权凭证是否正确               |
| `PRE_AUTH_INVALID_AUTH_TICKET`     | 订单授权凭证状态失效或已过期      | 请商户重新订购生成新的订单授权凭证           |
| `PRE_AUTH_INVALID_AUTH_TOKEN`      | 订单授权凭证换取的令牌已失效      | 商户取消了授权或者令牌被刷新，需重新授权        |
| `PRE_AUTH_INVOKE_API_NOT_PERMITTE` | 订单授权凭证无权限调用该接口      | 无接口调用权限                     |
| `PRE_AUTH_INVALID_AUTH_APP_ID`     | 凭证对应应用与接口调用应用不一致    | 请将调用接口的应用id更换成订单授权凭证对应的应用id |
| `PRE_AUTH_INVALID_AUTH_USER_ID`    | 凭证对应授权者与代实施者不一致     | 请将商户账号更换成订单授权凭证对应授权者的账号     |
| `UNKNOWN_EXCEPTION`                | 系统内部错误              | 请联系客服咨询具体原因                 |

### 请求示例

```bash
curl 'https://openapi.alipay.com/gateway.do?charset=UTF-8&method=alipay.open.agent.create&format=json&sign=${sign}&app_id=${appid}&version=1.0&sign_type=RSA2&timestamp=${now}' \
 -F 'app_auth_token=${app_auth_token}' \
 -F 'biz_content={
        "account":"test@alipay.com",
        "contact_info":{
                "contact_name":"张三",
                "contact_mobile":"18866668888",
                "contact_email":"zhangsan@alipy.com"
        },
        "order_ticket":"00ee2d475f374ad097ee0f1ac223fX00"
}'
```

### 响应示例

```json
{
  "alipay_open_agent_create_response": {
    "code": "10000",
    "msg": "Success",
    "batch_no": "2017110616474516400082883",
    "batch_status": "init"
  },
  "sign": "ERITJKEIJKJHKKKKKKKHJEREEEEEEEEEEE"
}
```

> 说明：本示例仅供参考。