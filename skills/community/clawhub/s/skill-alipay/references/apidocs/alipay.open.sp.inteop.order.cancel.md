# alipay.open.sp.inteop.order.cancel (服务商一体化作业取消业务开通单)

**接口用途**：服务商一体化作业取消业务开通单，商家确认之前都可以进行取消。

**文档地址**：https://opendocs.alipay.com/isv/a91d61cf_alipay.open.sp.inteop.order.cancel

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

| 参数                | 类型     | 必填 | 说明                            |
|-------------------|--------|----|-------------------------------|
| `inteop_order_no` | string | 是  | 一体化作业开通主单号，单号为服务商一体化作业主单创建返回值 |

### 公共响应参数

| 参数         | 类型     | 必填 | 说明      |
|------------|--------|----|---------|
| `code`     | string | 是  | 网关返回码   |
| `msg`      | string | 是  | 网关返回码描述 |
| `sub_code` | string | 否  | 业务返回码   |
| `sub_msg`  | string | 否  | 业务返回码描述 |
| `sign`     | string | 是  | 签名      |

### 业务响应参数

| 参数                  | 类型                             | 必填 | 说明                 |
|---------------------|--------------------------------|----|--------------------|
| `inteop_order_no`   | string                         | 否  | 一体化作业主单号           |
| `sub_task_op_infos` | array\<InteopSubTaskOpInfoVO\> | 否  | 一体化作业任务操作信息，见下方子属性 |

#### sub_task_op_infos（一体化作业任务操作信息）子参数

| 参数             | 类型     | 必填 | 说明           |
|----------------|--------|----|--------------|
| `sub_order_no` | string | 否  | 作业子单号        |
| `memo`         | string | 否  | 作业子单取消失败备注信息 |

### 错误码

| 错误码                       | 说明                         | 解决方案                                        |
|---------------------------|----------------------------|---------------------------------------------|
| `SYSTEM_ERROR`            | 系统繁忙                       | 服务器异常，可能发生了网络或者系统异常，导致服务调用失败，商户可以用同样的请求发起重试 |
| `INVALID_PARAMETER`       | 参数有误                       | 请根据接口返回的参数非法的具体错误信息，修改参数后进行重试               |
| `INTEOP_ORDER_NOT_EXIST`  | 作业主单记录不存在                  | 作业主单记录不存在                                   |
| `INVALID_INTEOP_ORDER_NO` | 作业主单 inteop_order_no不能为空   | 请对inteop_order_no赋值                         |
| `ISV_PID_INCONSISTENCY`   | 无操作权限，当前服务商pid和主单服务商pid不一致 | 无操作权限，当前服务商pid和主单服务商pid不一致                  |
| `ORDER_CANCEL_FAIL`       | 订单状态不可取消                   | 请稍后重试                                       |
| `ORDER_CANCEL_NOT_ALLOW`  | 订单不允许取消                    | 订单不允许取消，请检查当前订单状态                           |
| `SP_MERCHANT_INF_NO_FIND` | 服务商PID不存在                  | 服务商PID不存在                                   |

### 请求示例

```bash
curl 'https://openapi.alipay.com/gateway.do?charset=UTF-8&method=alipay.open.sp.inteop.order.cancel&format=json&sign=${sign}&app_id=${appid}&version=1.0&sign_type=RSA2&timestamp=${now}' \
 -F 'app_auth_token=${app_auth_token}' \
 -F 'biz_content={
        "inteop_order_no":"2025061211643563"
}'
```

### 响应示例

```json
{
  "alipay_open_sp_inteop_order_cancel_response": {
    "code": "10000",
    "msg": "Success",
    "inteop_order_no": "2025091911760795",
    "sub_task_op_infos": [
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