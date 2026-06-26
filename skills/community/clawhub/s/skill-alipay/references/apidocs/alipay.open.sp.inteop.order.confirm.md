# alipay.open.sp.inteop.order.confirm (服务商一体化开通作业子项合并提交)

**接口用途**：服务商一体化开通作业子项合并提交

**文档地址**：https://opendocs.alipay.com/isv/2e6e922b_alipay.open.sp.inteop.order.confirm

### 公共请求参数

| 参数            | 类型     | 必填 | 说明                               |
|---------------|--------|----|----------------------------------|
| `app_id`      | string | 是  | 支付宝分配给开发者的应用ID                   |
| `method`      | string | 是  | 接口名称                             |
| `format`      | string | 否  | 仅支持JSON                          |
| `charset`     | string | 是  | 请求使用的编码格式，如utf-8, gbk, gb2312等   |
| `sign_type`   | string | 是  | 签名算法类型：RSA2或RSA，推荐使用RSA2         |
| `sign`        | string | 是  | 商户请求参数的签名串                       |
| `timestamp`   | string | 是  | 发送请求的时间，格式yyyy-MM-dd HH:mm:ss    |
| `version`     | string | 是  | 接口版本，固定为1.0                      |
| `biz_content` | string | 是  | 请求参数的集合，除公共参数外所有请求参数都必须放在这个参数中传递 |

### 业务请求参数

| 参数                | 类型      | 必填 | 说明                                                   |
|-------------------|---------|----|------------------------------------------------------|
| `inteop_order_no` | string  | 是  | 服务商一体化作业主单号                                          |
| `async_submit`    | boolean | 否  | 选择异步提交，根据alipay.open.sp.inteop.order.query接口查询订单提交结果 |

### 公共响应参数

| 参数         | 类型     | 必填 | 说明      |
|------------|--------|----|---------|
| `code`     | string | 是  | 网关返回码   |
| `msg`      | string | 是  | 网关返回码描述 |
| `sub_code` | string | 否  | 业务返回码   |
| `sub_msg`  | string | 否  | 业务返回码描述 |
| `sign`     | string | 是  | 签名      |

### 业务响应参数

| 参数             | 类型                                 | 必填 | 说明                |
|----------------|------------------------------------|----|-------------------|
| `check_result` | array\<IntegratedOpenCheckInfoVO\> | 否  | 一体化作业的校验结果，见下方子属性 |

#### check_result（校验结果）子参数

| 参数             | 类型     | 必填 | 说明        |
|----------------|--------|----|-----------|
| `sub_order_no` | string | 否  | 作业子单号     |
| `memo`         | string | 否  | 作业预校验备注信息 |

### 错误码

| 错误码                         | 说明                         | 解决方案                                        |
|-----------------------------|----------------------------|---------------------------------------------|
| `SYSTEM_ERROR`              | 系统繁忙                       | 服务器异常，可能发生了网络或者系统异常，导致服务调用失败，商户可以用同样的请求发起重试 |
| `INVALID_PARAMETER`         | 参数有误                       | 请根据接口返回的参数非法的具体错误信息，修改参数后进行重试               |
| `INTEOP_BIZ_ITEM_NOT_EXIST` | 一体化作业子项不存在                 | 一体化作业子项不存在，请确认是否新建子项                        |
| `INTEOP_ORDER_NOT_EXIST`    | 一体化作业主单记录不存在               | 一体化作业主单记录不存在                                |
| `INTEOP_SETTLED_NOT_FINISH` | 一体化入驻流程未完成                 | openapi一体化作业中，入驻处理中，请稍后重试                   |
| `INVALID_INTEOP_ORDER_NO`   | 作业主单编号（inteop_order_no）无效  | 请更换inteop_order_no                          |
| `ISV_PID_INCONSISTENCY`     | 无操作权限，当前服务商pid和主单服务商pid不一致 | 无操作权限，当前服务商pid和主单服务商pid不一致                  |
| `MERCHANT_CAN_NOT_LOGON`    | 商家支付宝账号被限制登录               | 商家支付宝账号被限制登录，请先解除限制                         |
| `MERCHANT_IS_NOT_EXIST`     | 商户不存在                      | 商户支付宝不存在，请确认支付宝账号                           |
| `MERCHANT_NOT_ACTIVED`      | 商家支付宝账号未激活                 | 请激活商家支付宝账号                                  |
| `MERCHANT_NOT_CERTIFIED`    | 商家支付宝账号未实名认证               | 商家支付宝账号未实名认证                                |
| `MERCHANT_NOT_ENABLED`      | 商家支付宝账号被冻结或已注销             | 商家支付宝账号被冻结或已注销                              |
| `ORDER_CHECK_FAIL`          | 一体化作业订单检查失败，存在冲突配置或必填信息缺失  | 具体异常信息参考check_result结果中的memo查看具体失败原因        |
| `SP_MERCHANT_INF_NO_FIND`   | 服务商PID不存在                  | 服务商PID不存在                                   |

### 请求示例

```bash
curl 'https://openapi.alipay.com/gateway.do?charset=UTF-8&method=alipay.open.sp.inteop.order.confirm&format=json&sign=${sign}&app_id=${appid}&version=1.0&sign_type=RSA2&timestamp=${now}' \
 -F 'biz_content={
        "async_submit":true,
        "inteop_order_no":"2025061611646882"
}'
```

### 响应示例

```json
{
  "alipay_open_sp_inteop_order_confirm_response": {
    "code": "10000",
    "msg": "Success",
    "check_result": [
      {
        "sub_order_no": "2025071611667571",
        "memo": "备注信息"
      }
    ]
  },
  "sign": "ERITJKEIJKJHKKKKKKKHJEREEEEEEEEEEE"
}
```

> 说明：本示例仅供参考。