# ant.merchant.expand.bizaccess.order.create (发起业务开通)

**接口用途**：用于服务商代商户发起业务开通，本期仅支持"安心付直连周期卡"产品。"安心付直连周期卡"
包含以下六项业务功能：芝麻信用服务开通、服务商代运营授权、服务商代调用授权、安心付协议、安心付业务开通、服务商分佣设置。

**文档地址**：https://opendocs.alipay.com/isv/26fe8b0d_ant.merchant.expand.bizaccess.order.create

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

| 参数                         | 类型                                | 必填   | 说明                                               |
|----------------------------|-----------------------------------|------|--------------------------------------------------|
| `merchant_name`            | string                            | 是    | 商户名称，对于企业和个体户，值为营业执照上的名称                         |
| `scene_biz_code`           | array\<string\>                   | 是    | 业务场景码，见枚举值                                       |
| `need_operation_auth`      | boolean                           | 是    | 是否需要代运营授权，默认为false                               |
| `need_interface_auth`      | boolean                           | 是    | 是否需要代开发授权，默认为false                               |
| `phone`                    | string                            | 条件必填 | 商户联系电话，scene_biz_code=AXF_MERCHANT_PERIOD_PAY时必传 |
| `isv_commission_info`      | array\<IsvCommissionInfo\>        | 条件必填 | 服务商抽佣信息，见下方子属性                                   |
| `price_infos`              | array\<MerchantPriceRelatedInfo\> | 条件必填 | 价格信息，scene_biz_code=AXF_MERCHANT_PERIOD_PAY时必传   |
| `mcc_code`                 | string                            | 否    | 商户二级类目code，为空时使用商户本身的mccCode                     |
| `qualifications`           | array                             | 否    | 商户上传资质详情                                         |
| `license_info`             | CommonMerchantLicenseInfo         | 否    | 主体证照信息，见下方子属性                                    |
| `merchant_logon_id`        | string                            | 否    | 商户登录号                                            |
| `optional_front_prod_code` | array\<string\>                   | 否    | 可选开通的前台产品                                        |
| `benefit_info`             | CertificateInfoForEntry           | 否    | 受益人证照，见下方子属性                                     |
| `legal_info`               | CertificateInfoForEntry           | 否    | 法人证照，见下方子属性                                      |
| `need_register_merchant`   | boolean                           | 否    | 是否需要代入驻                                          |
| `legal_person_logon_id`    | string                            | 否    | 法人登录号                                            |
| `merchant_type`            | string                            | 否    | 商户类型                                             |
| `external_id`              | string                            | 否    | 关联外部单号                                           |

#### scene_biz_code（业务场景码）枚举值

| 枚举名     | 枚举值                     |
|---------|-------------------------|
| 安心付周期卡  | AXF_MERCHANT_PERIOD_PAY |
| 服务市场代入驻 | FW_MARKET_ENTRY         |
| 代入驻     | ENTRY                   |

#### isv_commission_info（服务商抽佣信息）子参数

| 参数                           | 类型      | 必填   | 说明                                                                                                                                               |
|------------------------------|---------|------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| `commission_mode`            | string  | 是    | 抽佣模式：USER_UNIFORM_SCALE-用户统一比例、ITEM_UNIFORM_SCALE-商品统一比例                                                                                         |
| `commission_scene`           | string  | 是    | 抽佣场景：ANXINFU_PERIOD_CARD_AGENT-安心付周期卡代运营、ANXINFU_MONEY_CARD_AGENT-安心付金额卡代运营、ANXINFU_PERIOD_CARD_SAAS-安心付周期卡代开发、ANXINFU_MONEY_CARD_SAAS-安心付金额卡代开发 |
| `long_term`                  | boolean | 是    | 是否是长期模式场景，为true时不用传抽佣时间                                                                                                                          |
| `merchant_app_id`            | string  | 条件必填 | 商家应用appId，need_interface_auth为false时必填                                                                                                           |
| `isv_rate`                   | string  | 否    | 服务商抽佣比例，无单位，如0.0400表示4%                                                                                                                          |
| `commission_valid_time`      | string  | 否    | 抽佣开始时间                                                                                                                                           |
| `commission_invalid_time`    | string  | 否    | 抽佣结束时间                                                                                                                                           |
| `item_mode_commission_list`  | array   | 否    | 商品抽佣比例，见下方子属性                                                                                                                                    |
| `commission_first_role_list` | array   | 否    | 合作伙伴抽佣信息，见下方子属性                                                                                                                                  |

#### item_mode_commission_list（商品抽佣比例）子参数

| 参数          | 类型     | 必填 | 说明                   |
|-------------|--------|----|----------------------|
| `item_id`   | string | 是  | 商品id                 |
| `item_rate` | string | 是  | 抽佣比例，无单位，如0.0400表示4% |

#### commission_first_role_list（合作伙伴抽佣信息）子参数

| 参数                    | 类型     | 必填 | 说明                                                               |
|-----------------------|--------|----|------------------------------------------------------------------|
| `role_alipay_account` | string | 是  | 合作伙伴支付宝账号                                                        |
| `role_account_name`   | string | 是  | 合作伙伴支付宝账号名称                                                      |
| `role_type`           | string | 是  | 角色类型：SUPPLIER_ROLE-供应商、BRANCH_ROLE-分公司、CHANNEL_PROVIDER_ROLE-渠道商 |
| `role_rate`           | string | 是  | 角色抽佣比例，无单位，如0.0400表示4%                                           |

#### price_infos（价格信息）子参数

| 参数                  | 类型     | 必填 | 说明                                               |
|---------------------|--------|----|--------------------------------------------------|
| `back_product_code` | string | 否  | 后台产品码：I1140100001000001000-商家扣款（安心付直联版使用，间联版不需填） |
| `price_rate`        | string | 否  | 费率，最多两位小数，范围0.38～0.6，单位%                         |

#### qualifications（资质信息）子参数

| 参数               | 类型              | 必填 | 说明                                                                  |
|------------------|-----------------|----|---------------------------------------------------------------------|
| `type`           | string          | 是  | 资质类型                                                                |
| `cert_no`        | string          | 是  | 资质Code                                                              |
| `effective_date` | string          | 是  | 资质有效期，格式yyyy-MM-dd，长期有效传入9999-12-31                                 |
| `license_name`   | string          | 否  | 资质名称                                                                |
| `license_urls`   | array\<string\> | 否  | 凭证图片链接，通过ant.merchant.expand.indirect.image.upload接口返回的image_id作为参数 |

#### license_info（主体证照信息）子参数

| 参数               | 类型              | 必填 | 说明     |
|------------------|-----------------|----|--------|
| `type`           | string          | 是  | 资质类型   |
| `cert_no`        | string          | 是  | 资质Code |
| `effective_date` | string          | 是  | 资质有效期  |
| `license_name`   | string          | 否  | 资质名称   |
| `license_urls`   | array\<string\> | 否  | 凭证图片链接 |

#### benefit_info（受益人证照）子参数

| 参数                  | 类型              | 必填 | 说明                          |
|---------------------|-----------------|----|-----------------------------|
| `cert_no`           | string          | 是  | 证件号                         |
| `cert_type`         | string          | 是  | 证件类型                        |
| `cert_pic_url_type` | string          | 是  | 证件图片类型：ORIGINAL-原件、COPY-复印件 |
| `cert_pic_urls`     | array\<string\> | 是  | 证件图片地址                      |
| `cert_name`         | string          | 是  | 证件名称                        |
| `gmt_valid`         | string          | 否  | 生效时间                        |
| `gmt_invalid`       | string          | 否  | 失效时间                        |
| `business_scope`    | string          | 否  | 经营范围                        |
| `reg_capital`       | string          | 否  | 注册地址                        |

#### legal_info（法人证照）子参数

| 参数                  | 类型              | 必填 | 说明                          |
|---------------------|-----------------|----|-----------------------------|
| `cert_no`           | string          | 是  | 证件号                         |
| `cert_type`         | string          | 是  | 证件类型                        |
| `cert_pic_url_type` | string          | 是  | 证件图片类型：ORIGINAL-原件、COPY-复印件 |
| `cert_pic_urls`     | array\<string\> | 是  | 证件图片地址                      |
| `cert_name`         | string          | 是  | 证件名称                        |
| `gmt_valid`         | string          | 否  | 生效时间                        |
| `gmt_invalid`       | string          | 否  | 失效时间                        |
| `business_scope`    | string          | 否  | 经营范围                        |
| `reg_capital`       | string          | 否  | 注册地址                        |

### 公共响应参数

| 参数         | 类型     | 必填 | 说明      |
|------------|--------|----|---------|
| `code`     | string | 是  | 网关返回码   |
| `msg`      | string | 是  | 网关返回码描述 |
| `sub_code` | string | 否  | 业务返回码   |
| `sub_msg`  | string | 否  | 业务返回码描述 |
| `sign`     | string | 是  | 签名      |

### 业务响应参数

| 参数             | 类型                                 | 必填 | 说明          |
|----------------|------------------------------------|----|-------------|
| `order_id`     | string                             | 是  | 业务开通主单号     |
| `fail_reasons` | array\<IsvBizOpenOrderFailReason\> | 否  | 失败原因，见下方子属性 |
| `merchant_pid` | string                             | 否  | 商户PID       |

#### fail_reasons（失败原因）子参数

| 参数           | 类型     | 必填 | 说明   |
|--------------|--------|----|------|
| `error_code` | string | 是  | 错误码  |
| `error_msg`  | string | 是  | 错误原因 |

### 错误码

| 错误码                 | 说明     | 解决方案                                        |
|---------------------|--------|---------------------------------------------|
| `SYSTEM_ERROR`      | 系统繁忙   | 服务器异常，可能发生了网络或者系统异常，导致服务调用失败，商户可以用同样的请求发起重试 |
| `INVALID_PARAMETER` | 参数有误   | 请根据接口返回的参数非法的具体错误信息，修改参数后进行重试               |
| `BIZ_OPEN_ERROR`    | 业务开通异常 | 业务开通异常，参考fail_reasons提供的解决方案再重试             |

### 请求示例

```bash
curl 'https://openapi.alipay.com/gateway.do?charset=UTF-8&method=ant.merchant.expand.bizaccess.order.create&format=json&sign=${sign}&app_id=${appid}&version=1.0&sign_type=RSA2&timestamp=${now}' \
 -F 'app_auth_token=${app_auth_token}' \
 -F 'biz_content={
        "phone":"15612345678",
        "mcc_code":"B0064",
        "qualifications":[{
                "license_name":"xx有限公司",
                "cert_no":"91350602MXXXXXXXXX",
                "effective_date":"2024-10-01",
                "type":"3128",
                "license_urls":["xxxxxxxxxxxx.jpg"]
        }],
        "license_info":{
                "license_name":"xx有限公司",
                "cert_no":"91350602MXXXXXXXXX",
                "effective_date":"2024-10-01",
                "type":"3128",
                "license_urls":["xxxxxxxxxxxx.jpg"]
        },
        "isv_commission_info":[{
                "isv_rate":"0.0400",
                "commission_valid_time":"2024-10-01",
                "item_mode_commission_list":[{"item_rate":"0.0400","item_id":"2023102522000XXXXXX000"}],
                "commission_scene":"ANXINFU_PERIOD_CARD_SAAS",
                "commission_invalid_time":"2024-10-01",
                "merchant_app_id":"201406060016XXXX",
                "commission_mode":"USER_UNIFORM_SCALE",
                "long_term":true,
                "commission_first_role_list":[{"role_type":"SUPPLIER_ROLE","role_account_name":"XXX有限公司","role_alipay_account":"zhangsancompanyXXX@163.com","role_rate":"0.0400"}]
        }],
        "merchant_name":"XXX有限公司",
        "merchant_logon_id":"zhangsancompanyXXX@163.com",
        "scene_biz_code":["AXF_MERCHANT_PERIOD_PAY"],
        "need_operation_auth":true,
        "need_interface_auth":true,
        "price_infos":[{"price_rate":"0.38","back_product_code":"I1140100001000001000"}],
        "optional_front_prod_code":["I1140100001000001000"],
        "benefit_info":{"business_scope":"零售","cert_type":"100","cert_name":"赵xx","cert_no":"3301000xxxxx222","cert_pic_url_type":"ORIGINAL","reg_capital":"杭州市xxx街道xxx室","gmt_invalid":"2024-1-1","cert_pic_urls":["key3432749273.jpg"],"gmt_valid":"2024-01-01"},
        "legal_info":{"business_scope":"零售","cert_type":"100","cert_name":"赵xx","cert_no":"3301000xxxxx222","cert_pic_url_type":"ORIGINAL","reg_capital":"杭州市xxx街道xxx室","gmt_invalid":"2024-1-1","cert_pic_urls":["key3432749273.jpg"],"gmt_valid":"2024-01-01"},
        "need_register_merchant":true,
        "legal_person_logon_id":"137xxxxxxxx",
        "merchant_type":"01",
        "external_id":"202543748329432432"
}'
```

### 响应示例

```json
{
  "ant_merchant_expand_bizaccess_order_create_response": {
    "code": "10000",
    "msg": "Success",
    "order_id": "202411110050200000000000XXXX",
    "fail_reasons": [
      {
        "error_code": "100",
        "error_msg": "错误原因"
      }
    ],
    "merchant_pid": "2088541042290000"
  },
  "sign": "ERITJKEIJKJHKKKKKKKHJEREEEEEEEEEEE"
}
```

> 说明：本示例仅供参考。