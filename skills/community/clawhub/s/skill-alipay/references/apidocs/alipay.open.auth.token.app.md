# alipay.open.auth.token.app (换取应用授权令牌)

**接口用途**：换取应用授权令牌。在应用授权的场景下，商户把名下应用授权给ISV后，支付宝会给ISV颁发应用授权码app_auth_code，ISV可通过获取到的app_auth_code换取app_auth_token。

**说明**：

- app_auth_code作为换取app_auth_token的票据，每次用户授权带上的app_auth_code将不一样
- app_auth_code只能使用一次，一天（从当前时间算起的24小时）未被使用自动过期
- 刷新应用授权令牌：ISV可通过获取到的refresh_token刷新app_auth_token，刷新后老的refresh_token会在一段时间后失效（失效时间为接口返回的re_expires_in）

**文档地址**：https://opendocs.alipay.com/isv/04h3uf

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

| 参数              | 类型     | 必填   | 说明                                                                                 |
|-----------------|--------|------|------------------------------------------------------------------------------------|
| `grant_type`    | string | 是    | 授权方式：authorization_code-使用应用授权码换取应用授权令牌、refresh_token-使用app_refresh_token刷新获取新授权令牌 |
| `code`          | string | 条件必填 | 应用授权码，grant_type为authorization_code时必填                                             |
| `refresh_token` | string | 条件必填 | 刷新令牌，grant_type为refresh_token时必填                                                   |

#### grant_type（授权方式）枚举值

| 枚举名                          | 枚举值                |
|------------------------------|--------------------|
| 使用应用授权码换取应用授权令牌              | authorization_code |
| 使用app_refresh_token刷新获取新授权令牌 | refresh_token      |

### 公共响应参数

| 参数         | 类型     | 必填 | 说明      |
|------------|--------|----|---------|
| `code`     | string | 是  | 网关返回码   |
| `msg`      | string | 是  | 网关返回码描述 |
| `sub_code` | string | 否  | 业务返回码   |
| `sub_msg`  | string | 否  | 业务返回码描述 |
| `sign`     | string | 是  | 签名      |

### 业务响应参数

| 参数                  | 类型     | 必填 | 说明                            |
|---------------------|--------|----|-------------------------------|
| `user_id`           | string | 是  | 授权商户的user_id                  |
| `auth_app_id`       | string | 是  | 授权商户的appid                    |
| `app_auth_token`    | string | 是  | 应用授权令牌                        |
| `app_refresh_token` | string | 是  | 刷新令牌                          |
| `expires_in`        | string | 是  | 该字段已作废，应用令牌长期有效，接入方不需要消费该字段   |
| `re_expires_in`     | string | 是  | 刷新令牌的有效时间（从接口调用时间作为起始时间），单位到秒 |

### 错误码

| 错误码                       | 说明                                             | 解决方案                                           |
|---------------------------|------------------------------------------------|------------------------------------------------|
| `APP_ID_NOT_CONSISTENT`   | 授权令牌授予的应用AppId与当前应用AppId不一致                    | 确认授权令牌和应用标识是否正确                                |
| `APP_NOT_ISV`             | 当前请求app_id非第三方应用，请求失败                          | 当前请求应用非第三方应用，请更改appid后重试                       |
| `AUTH_CODE_NOT_EXIST`     | auth_code不存在                                   | 更换存在的授权code                                    |
| `AUTH_CODE_NOT_VALID`     | 无效的auth_code                                   | 更换有效的授权码                                       |
| `AUTH_TOKEN_NOT_FOUND`    | 授权令牌不存在                                        | 一般不会出现该异常，如出现需要更换有效的授权码                        |
| `GRANT_TYPE_INVALID`      | grant_type必须是authorization_code或者refresh_token | grant_type必须是authorization_code或者refresh_token |
| `REFRESH_TOKEN_NOT_EXIST` | 刷新令牌不存在                                        | 更换存在的刷新令牌                                      |
| `REFRESH_TOKEN_NOT_VALID` | 无效的刷新令牌                                        | 更换有效的刷新令牌                                      |
| `REFRESH_TOKEN_TIME_OUT`  | 刷新令牌过期                                         | 更换有效的刷新令牌                                      |

### 请求示例

```bash
curl 'https://openapi.alipay.com/gateway.do?charset=UTF-8&method=alipay.open.auth.token.app&format=json&sign=${sign}&app_id=${appid}&version=1.0&sign_type=RSA2&timestamp=${now}' \
 -F 'app_auth_token=${app_auth_token}' \
 -F 'biz_content={
        "grant_type":"authorization_code",
        "code":"1cc19911172e4f8aaa509c8fb5d12F56",
        "refresh_token":"201509BBdcba1e3347de4e75ba3fed2c9abebE36"
}'
```

### 响应示例

```json
{
  "alipay_open_auth_token_app_response": {
    "code": "10000",
    "msg": "Success",
    "user_id": "2088102150527498",
    "auth_app_id": "2013121100055554",
    "app_auth_token": "201509BBeff9351ad1874306903e96b91d248A36",
    "app_refresh_token": "201509BBdcba1e3347de4e75ba3fed2c9abebE36",
    "expires_in": "123456",
    "re_expires_in": "123456"
  },
  "sign": "ERITJKEIJKJHKKKKKKKHJEREEEEEEEEEEE"
}
```

> 说明：本示例仅供参考。