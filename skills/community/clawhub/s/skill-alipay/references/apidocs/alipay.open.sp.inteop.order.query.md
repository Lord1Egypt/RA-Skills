# alipay.open.sp.inteop.order.query (服务商一体化开通作业查询业务开通单)

**接口用途**：服务商一体化开通作业查询业务开通单

**文档地址**：https://opendocs.alipay.com/isv/4308c1bb_alipay.open.sp.inteop.order.query

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

| 参数                | 类型     | 必填 | 说明           |
|-------------------|--------|----|--------------|
| `inteop_order_no` | string | 是  | 一体化作业业务开通主单号 |

### 公共响应参数

| 参数         | 类型     | 必填 | 说明      |
|------------|--------|----|---------|
| `code`     | string | 是  | 网关返回码   |
| `msg`      | string | 是  | 网关返回码描述 |
| `sub_code` | string | 否  | 业务返回码   |
| `sub_msg`  | string | 否  | 业务返回码描述 |
| `sign`     | string | 是  | 签名      |

### 业务响应参数

| 参数                       | 类型                          | 必填 | 说明               |
|--------------------------|-----------------------------|----|------------------|
| `inteop_order_no`        | string                      | 是  | 一体化作业主单号         |
| `inteop_order_status`    | string                      | 是  | 一体化作业主单状态，见枚举值   |
| `inteop_sub_order_infos` | array\<InteOpSubOrderInfo\> | 是  | 一体化作业子项信息，见下方子属性 |
| `merchant_oid`           | string                      | 否  | 商户号              |
| `wp_qr_code`             | string                      | 否  | 待办二维码跳转链接        |
| `wp_qr_code_img_url`     | string                      | 否  | 待办二维码图片链接        |
| `wp_web_link`            | string                      | 否  | 待办web页面链接        |

#### inteop_order_status（主单状态）枚举值

| 枚举名   | 枚举值                   |
|-------|-----------------------|
| 初始化   | INIT                  |
| 审核中   | AUDITING              |
| 审核完成  | AUDIT_PASS            |
| 审核未通过 | REJECT                |
| 待商户确认 | WAIT_MERCHANT_CONFIRM |
| 商户已确认 | MERCHANT_CONFIRMED    |
| 申请成功  | APPLY_SUCCESS         |
| 已取消   | APPLY_CANCEL          |

#### inteop_sub_order_infos（子项信息）子参数

| 参数                 | 类型                        | 必填 | 说明                                   |
|--------------------|---------------------------|----|--------------------------------------|
| `sub_order_no`     | string                    | 是  | 一体化作业子项单号                            |
| `type`             | string                    | 是  | 一体化作业子项类型：AUTH-授权、SIGN-签约、SETTLED-入驻 |
| `sub_order_status` | string                    | 是  | 一体化作业子项状态                            |
| `memo`             | string                    | 是  | 备注                                   |
| `shop_infos`       | array\<InteOpShopInfoVO\> | 否  | 一体化作业商户门店信息，见下方子属性                   |

#### shop_infos（门店信息）子参数

| 参数                   | 类型     | 必填 | 说明        |
|----------------------|--------|----|-----------|
| `shop_id`            | string | 否  | 门店id      |
| `merchant_oid`       | string | 否  | 商户号       |
| `wp_qr_code`         | string | 否  | 待办二维码跳转链接 |
| `wp_qr_code_img_url` | string | 否  | 待办二维码图片链接 |
| `wp_web_link`        | string | 否  | 待办web页面链接 |

### 错误码

| 错误码                         | 说明                          | 解决方案                                        |
|-----------------------------|-----------------------------|---------------------------------------------|
| `SYSTEM_ERROR`              | 系统繁忙                        | 服务器异常，可能发生了网络或者系统异常，导致服务调用失败，商户可以用同样的请求发起重试 |
| `INVALID_PARAMETER`         | 参数有误                        | 请根据接口返回的参数非法的具体错误信息，修改参数后进行重试               |
| `INTEOP_BIZ_ITEM_NOT_EXIST` | openapi一体化作业子项不存在           | openapi一体化作业子项不存在                           |
| `INTEOP_ORDER_NOT_EXIST`    | 根据inteop_order_no未查询到作业主单记录 | 请确认一体化作业主单是否正确                              |
| `INVALID_INTEOP_ORDER_NO`   | inteop_order_no参数无效         | inteop_order_no参数无效，未查到有效申请单记录              |
| `ISV_PID_INCONSISTENCY`     | 当前应用归属服务商pid和主单服务商pid不一致    | 请确认操作服务商pid信息                               |
| `SP_MERCHANT_INF_NO_FIND`   | 应用主体所属服务商PID格式无效            | 请检查服务商应用归属pid信息                             |

### 请求示例

```bash
curl 'https://openapi.alipay.com/gateway.do?charset=UTF-8&method=alipay.open.sp.inteop.order.query&format=json&sign=${sign}&app_id=${appid}&version=1.0&sign_type=RSA2&timestamp=${now}' \
 -F 'biz_content={
        "inteop_order_no":"2025073153331550"
}'
```

### 响应示例

```json
{
  "alipay_open_sp_inteop_order_query_response": {
    "code": "10000",
    "msg": "Success",
    "merchant_oid": "xxxxxx",
    "wp_qr_code": "alipays://platformapi/startapp?appId=2018090561299510&page=pages/wait-deal-p/index?batchNo=2025081654312412&query=principalId=1234721240914772",
    "wp_qr_code_img_url": "https://mobilecodec.alipay.com/show.htm?code=5dq0500nid6vko7cl64b&trans=false",
    "wp_web_link": "https://b.alipay.com/page/isv-merchant-workspace/wait-deal-p?batchNo=2025081654312412",
    "inteop_order_no": "2025080653727467",
    "inteop_order_status": "AUDITING",
    "inteop_sub_order_infos": [
      {
        "shop_infos": [
          {
            "shop_id": "XXX"
          }
        ],
        "sub_order_no": "2025071111661598",
        "type": "SETTLED_AND_AUTH",
        "sub_order_status": "AUDITING",
        "memo": "备注"
      }
    ]
  },
  "sign": "ERITJKEIJKJHKKKKKKKHJEREEEEEEEEEEE"
}
```

> 说明：本示例仅供参考。