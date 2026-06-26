# alipay.open.agent.commonsign.confirm (代商户签约，提交信息确认接口)

**接口用途**：三方应用代理签约产品，上传商户信息后，确认提交信息。可以配合开启事务接口使用。

**文档地址**：https://opendocs.alipay.com/isv/15287e8b_alipay.open.agent.commonsign.confirm

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

| 参数         | 类型     | 必填 | 说明                                                |
|------------|--------|----|---------------------------------------------------|
| `batch_no` | string | 是  | ISV代商户操作事务编号，通过事务开启接口alipay.open.agent.create调用返回 |

### 公共响应参数

| 参数         | 类型     | 必填 | 说明      |
|------------|--------|----|---------|
| `code`     | string | 是  | 网关返回码   |
| `msg`      | string | 是  | 网关返回码描述 |
| `sub_code` | string | 否  | 业务返回码   |
| `sub_msg`  | string | 否  | 业务返回码描述 |
| `sign`     | string | 是  | 签名      |

### 业务响应参数

| 参数         | 类型     | 必填 | 说明   |
|------------|--------|----|------|
| `order_no` | string | 是  | 签约单号 |

### 错误码

| 错误码                                  | 说明                 | 解决方案                                                        |
|--------------------------------------|--------------------|-------------------------------------------------------------|
| `SYSTEM_ERROR`                       | 系统繁忙               | 服务器异常，可能发生了网络或者系统异常，导致服务调用失败，商户可以用同样的请求发起重试                 |
| `INVALID_PARAMETER`                  | 参数有误               | 请根据接口返回的参数非法的具体错误信息，修改参数后进行重试                               |
| `ANT_PRODUCT_CONFLICT`               | 签约冲突               | 当前签约产品和已签约产品冲突，无法签约                                         |
| `BATCH_IS_EMPTY`                     | 事务中没有进行任何操作        | 不允许提交空事务，请先调用代签约等业务接口，再提交事务                                 |
| `BATCH_IS_NOT_EXIST`                 | 代商户操作事务编号不存在       | 请检查事务编号是否有效                                                 |
| `BATCH_STATUS_IS_FINAL`              | 事务已经达到终态           | 请确认事务状态是否是init状态，submit\|cancel\|timeout状态的都是终态，不允许继续进行接口调用 |
| `BIZ_ERROR`                          | 业务异常/签约失败          | 具体失败原因，请参考接口返回的错误信息                                         |
| `BUSINESS_LICENSE_NO_EMPTY`          | 营业执照号不能为空          | 请检查商户的营业执照号是否填写                                             |
| `FEERATE_NOT_INTERAVL`               | 费率不在区间内            | 具体的费率区间请参考接口返回的区间值                                          |
| `INVALID_BATCH_NO`                   | 事务编号batch_no不能为空   | 事务编号batch_no不能为空                                            |
| `MERCHANT_INTERFACE_INFO_ERR`        | 批量提交中产品经营信息不一致     | 确保批量提交的产品中需要一致的信息保证一致                                       |
| `MERCHANT_SIGN_PRODUCT_IN_AUDIT`     | 商户存在审核中的签约申请       | 取消之前的申请单，重新签约                                               |
| `NEW_LINK_CANNOT_BATCH_SIGN`         | 新链路不支持多产品批量签约      | 新链路的产品需逐个发起签约                                               |
| `NOT_MATCHED_SSU_OR_PS`              | 产品暂时无法签约           | 请确认商户所在行业是否可以签约该产品                                          |
| `NO_APP_PERMISSION`                  | APPID不匹配           | 请检查当前调用的appId和创建事务的appId是否匹配                                |
| `OPEN_API_SIGN_ISV_NOT_IN_WHITELIST` | isv不在白名单中          | 该接口暂未开放                                                     |
| `OPEN_API_SIGN_PRODUCT_NOT_SUPPORT`  | 产品码不在白名单中          | 暂不支持该产品码                                                    |
| `OPEN_API_SIGN_PRODUCT_NUM_TOO_BIG`  | 批量提交的产品超过限制数量      | 减少一次性批量提交的产品数量                                              |
| `ORDER_TYPE_NULL_ERROR`              | 产品订购类型为空           | 根据具体的返回的原因解决                                                |
| `PRODUCT_CANNOT_MIX_SIGN`            | 新老链路产品不可混签         | 新老链路的产品分别提交，暂不支持同批次提交                                       |
| `PRODUCT_NO_OPENABLE_PERMISSION_SET` | 当前签约产品不存在可开通的权限集   | 当前产品暂未开放任何可签约的权限集                                           |
| `PRODUCT_OPEN_FAIL`                  | 产品开通失败             | 请参照接口返回错误信息修改传参                                             |
| `RESTRICT_VALID_ERROR`               | 批量签约暂不支持产品批量信息补全操作 | 去掉其中需要补全的产品                                                 |
| `UNKNOWN_EXCEPTION`                  | 系统内部错误             | 请联系客服咨询具体原因                                                 |

### 请求示例

```bash
curl 'https://openapi.alipay.com/gateway.do?charset=UTF-8&method=alipay.open.agent.commonsign.confirm&format=json&sign=${sign}&app_id=${appid}&version=1.0&sign_type=RSA2&timestamp=${now}' \
 -F 'app_auth_token=${app_auth_token}' \
 -F 'biz_content={
        "batch_no":"2017110616474516400082883"
}'
```

### 响应示例

```json
{
  "alipay_open_agent_commonsign_confirm_response": {
    "code": "10000",
    "msg": "Success",
    "order_no": "20211102034000100000023843766649"
  },
  "sign": "ERITJKEIJKJHKKKKKKKHJEREEEEEEEEEEE"
}
```

> 说明：本示例仅供参考。