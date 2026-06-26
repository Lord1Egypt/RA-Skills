# alipay.open.sp.inteop.product.create (服务商一体化开通作业添加产品开通项)

**接口用途**：服务商一体化开通作业添加产品开通项

**文档地址**：https://opendocs.alipay.com/isv/67ff59c4_alipay.open.sp.inteop.product.create

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

| 参数                             | 类型                        | 必填   | 说明                       |
|--------------------------------|---------------------------|------|--------------------------|
| `inteop_order_no`              | string                    | 是    | 业务开通单号                   |
| `product_code`                 | string                    | 是    | 产品编码，见枚举值                |
| `inteop_product_details`       | array                     | 否    | 产品开通明细信息，为空则默认开通产品下属所有明细 |
| `inteop_product_price_details` | array                     | 否    | 产品费率明细信息                 |
| `mcc_code`                     | string                    | 是    | 经营类目编码，详情参考商家经营类目2.0     |
| `trade_scene`                  | string                    | 条件必填 | 交易场景，根据产品不同必传不同值         |
| `mobile_type`                  | string                    | 条件必填 | 移动设备类型                   |
| `inteop_merchant_info`         | InteOpMerchantInfo        | 是    | 商户基本信息                   |
| `inteop_business_license_info` | InteOpBusinessLicenseInfo | 条件必填 | 商户营业执照信息                 |
| `inteop_shop_info`             | InteOpShopInfo            | 条件必填 | 店铺信息                     |
| `inteop_app_info`              | InteOpAppInfo             | 条件必填 | app信息                    |
| `inteop_web_site_info`         | InteOpWebSiteInfo         | 条件必填 | 网站信息                     |
| `inteop_mini_app_info`         | InteOpMiniAppInfo         | 条件必填 | 小程序信息                    |
| `inteop_h_5_info`              | InteOpHtmlFiveInfo        | 条件必填 | h5信息                     |
| `inteop_special_license_infos` | array                     | 否    | 特殊行业资质信息                 |
| `inteop_special_license_info`  | InteOpSpecialLicenseInfo  | 否    | 特殊行业资质信息【废弃】             |

#### product_code（产品编码）枚举值

| 枚举名     | 产品编码                 |
|---------|----------------------|
| JSAPI支付 | I1080300001000060370 |
| 预授权支付   | I1080300001000065324 |
| 手机网站支付  | I1080300001000041949 |
| 电脑网站支付  | I1080300001000041203 |
| 订单码支付   | I1080300001000068149 |
| 刷脸付     | I1080300001000045785 |
| 当面付     | I1080300001000041016 |
| APP支付   | I1080300001000041313 |
| 线下租赁交易  | I1080300001000151809 |
| 商家分账    | I1080300001000043489 |
| 小程序订单中心 | I1080300001000041605 |

#### trade_scene（交易场景）必填条件

| 开通产品         | 必传值                                      |
|--------------|------------------------------------------|
| 当面付          | offline_store                            |
| 电脑网站支付       | pc                                       |
| 手机网站支付、APP支付 | mobile                                   |
| JSAPI        | tiny_app                                 |
| 预授权支付        | tiny_app,mobile,offline_store（至少选一个，可多选） |

#### mobile_type（移动设备类型）必填条件

| 开通产品            | 必传值           |
|-----------------|---------------|
| 手机网站支付          | H5            |
| APP支付           | APP           |
| 预授权支付（mobile场景） | APP,H5（至少选一个） |

#### inteop_product_details（产品开通明细信息）子参数

| 参数                    | 类型     | 必填 | 说明       |
|-----------------------|--------|----|----------|
| `product_detail_code` | string | 是  | 产品开通明细编码 |

#### inteop_product_price_details（产品费率明细信息）子参数

| 参数                    | 类型     | 必填 | 说明                                     |
|-----------------------|--------|----|----------------------------------------|
| `product_detail_code` | string | 是  | 产品开通明细项编码                              |
| `price_rate`          | string | 是  | 产品开通明细项费率，单位小数不能填百分号，最多两位小数，范围0.38～1.0 |

#### inteop_merchant_info（商户基本信息）子参数

| 参数               | 类型     | 必填 | 说明       |
|------------------|--------|----|----------|
| `contact_name`   | string | 是  | 商户联系人姓名  |
| `contact_mobile` | string | 是  | 商户联系人手机号 |

#### inteop_business_license_info（商户营业执照信息）子参数

| 参数                        | 类型      | 必填 | 说明                                             |
|---------------------------|---------|----|------------------------------------------------|
| `business_license_no`     | string  | 是  | 商户营业执照号码                                       |
| `business_license_pic`    | string  | 是  | 营业执照图片，传入alipay.open.file.upload接口上传获取的file_id |
| `long_term`               | boolean | 否  | 营业执照是否长期有效                                     |
| `date_limitation`         | string  | 否  | 营业期限（非长期时需填）                                   |
| `business_license_mobile` | string  | 否  | 营业执照法人认证手机号                                    |

#### inteop_shop_info（店铺信息）子参数

| 参数                    | 类型     | 必填   | 说明                                  |
|-----------------------|--------|------|-------------------------------------|
| `shop_name`           | string | 条件必填 | 门店名称（offline_store场景必传）             |
| `shop_sign_board_pic` | string | 条件必填 | 门店门头照（offline_store场景必传）            |
| `shop_scene_pic`      | string | 条件必填 | 门店内景图片（offline_store场景必传）           |
| `shop_country_code`   | string | 条件必填 | 门店所在国家编码，中国默认156（offline_store场景必传） |
| `shop_province_code`  | string | 条件必填 | 门店所在省份编码（offline_store场景必传）         |
| `shop_city_code`      | string | 条件必填 | 门店城市编码（offline_store场景必传）           |
| `shop_district_code`  | string | 条件必填 | 门店所在区县编码（offline_store场景必传）         |
| `shop_detail_address` | string | 条件必填 | 门店详细地址（offline_store场景必传）           |

#### inteop_app_info（app信息）子参数

| 参数                          | 类型              | 必填   | 说明                              |
|-----------------------------|-----------------|------|---------------------------------|
| `app_name`                  | string          | 条件必填 | 商户的APP应用名称                      |
| `app_status`                | string          | 条件必填 | 应用状态：ONLINE-已上架、OFFLINE-未上架     |
| `app_market`                | array\<string\> | 条件必填 | 上架的服务市场：苹果、应用宝、华为、360、小米、豌豆荚、其他 |
| `app_type`                  | string          | 条件必填 | 应用类型：IOS、Android                |
| `app_home_screenshot`       | string          | 条件必填 | 应用首页截图file_id                   |
| `app_pay_screenshot`        | string          | 条件必填 | 应用支付页截图file_id                  |
| `app_item_screenshot`       | string          | 条件必填 | 商品或服务页截图file_id                 |
| `in_app_screenshot`         | string          | 条件必填 | 应用内截图file_id                    |
| `app_test_account`          | string          | 否    | 应用测试账号                          |
| `app_test_account_password` | string          | 否    | 应用测试账号密码                        |
| `app_auth_pic`              | string          | 否    | APP授权函图片file_id                 |
| `app_download_link`         | string          | 否    | 应用下载链接                          |

#### inteop_web_site_info（网站信息）子参数

| 参数                          | 类型     | 必填   | 说明                          |
|-----------------------------|--------|------|-----------------------------|
| `web_sites`                 | string | 条件必填 | 接入网址信息（pc场景必填）              |
| `web_home_screenshot`       | string | 条件必填 | 网站首页截图file_id               |
| `web_item_screenshot`       | string | 条件必填 | 网站商品页截图file_id              |
| `web_pay_screenshot`        | string | 条件必填 | 网站支付页截图file_id              |
| `web_status`                | string | 条件必填 | 网站状态：ONLINE-已上线、OFFLINE-未上线 |
| `web_sites_loa`             | string | 否    | 网址授权函file_id                |
| `web_test_account`          | string | 否    | 网站测试账号                      |
| `web_test_account_password` | string | 否    | 网站测试账号密码                    |

#### inteop_mini_app_info（小程序信息）子参数

| 参数                    | 类型     | 必填   | 说明                     |
|-----------------------|--------|------|------------------------|
| `mini_app_id`         | string | 条件必填 | 小程序APPID（tiny_app场景必填） |
| `mini_app_name`       | string | 否    | 小程序名称                  |
| `mini_app_screenshot` | string | 否    | 小程序截图file_id           |

#### inteop_h_5_info（h5信息）子参数

| 参数                          | 类型     | 必填   | 说明                            |
|-----------------------------|--------|------|-------------------------------|
| `h_5_status`                | string | 条件必填 | H5网站状态：ONLINE-已上线、OFFLINE-未上线 |
| `h_5_sites`                 | string | 条件必填 | H5网站地址                        |
| `h_5_home_screenshot`       | string | 条件必填 | H5首页截图file_id                 |
| `h_5_pay_screenshot`        | string | 条件必填 | H5支付页截图file_id                |
| `h_5_item_screenshot`       | string | 条件必填 | H5商品页截图file_id                |
| `h_5_sites_loa`             | string | 否    | H5网址授权函file_id                |
| `h_5_memo`                  | string | 否    | 网站信息文本                        |
| `h_5_extra_pic`             | string | 否    | 网站备注图片file_id                 |
| `h_5_test_account`          | string | 否    | H5网站测试账户                      |
| `h_5_test_account_password` | string | 否    | H5网站测试账户密码                    |

#### inteop_special_license_infos（特殊行业资质信息）子参数

| 参数                     | 类型     | 必填 | 说明                |
|------------------------|--------|----|-------------------|
| `special_license_type` | string | 否  | 合约特殊资质的类型，默认可以传99 |
| `special_license_pic`  | string | 否  | 企业特殊资质图片file_id   |

### 公共响应参数

| 参数         | 类型     | 必填 | 说明      |
|------------|--------|----|---------|
| `code`     | string | 是  | 网关返回码   |
| `msg`      | string | 是  | 网关返回码描述 |
| `sub_code` | string | 否  | 业务返回码   |
| `sub_msg`  | string | 否  | 业务返回码描述 |
| `sign`     | string | 是  | 签名      |

### 业务响应参数

| 参数             | 类型              | 必填 | 说明           |
|----------------|-----------------|----|--------------|
| `sub_order_no` | string          | 是  | 一体化作业子项单号    |
| `memos`        | array\<string\> | 是  | 产品添加开通失败原因说明 |

### 错误码

| 错误码                             | 说明              | 解决方案                                                 |
|---------------------------------|-----------------|------------------------------------------------------|
| `SYSTEM_ERROR`                  | 系统繁忙            | 服务器异常，可能发生了网络或者系统异常，商户可以用同样的请求发起重试                   |
| `INVALID_PARAMETER`             | 参数有误            | 根据接口返回的参数非法的具体错误信息，修改参数后进行重试                         |
| `FILE_HANDLE_FAIL`              | 文件处理错误          | 检查上传图片ID或者重试                                         |
| `INTEOP_ORDER_NOT_EXIST`        | 作业主单记录不存在       | 先使用接口alipay.open.sp.inteop.order.create创建主单          |
| `INVALID_INTEOP_ORDER_NO`       | 作业主单号为空         | 请先通过alipay.open.sp.inteop.order.create创建主单号          |
| `ISV_PID_INCONSISTENCY`         | 无操作权限           | 当前服务商pid和主单服务商pid不一致，请使用对应的服务商应用进行调用                 |
| `MERCHANT_NOT_SETTLE`           | 商户还未入驻          | 请先代商户入驻或通过alipay.open.sp.inteop.settle.create先创建入驻子单 |
| `ORDER_COMMIT`                  | 主订单已进到下一阶段      | 请通过接口alipay.open.sp.inteop.order.query查询订单状态         |
| `PRODUCT_CHECK_FAIL`            | 产品开通业务逻辑检查失败    | 根据memos查询具体的原因                                       |
| `PRODUCT_EXIST_SOLUTION_RECORD` | 产品在解决方案申请单内已经存在 | 需要取消对应的解决方案申请子单                                      |
| `PRODUCT_EXIT_RECORD`           | 产品在当前申请单已经存在    | 请通过接口alipay.open.sp.inteop.order.query查询对应的子单记录      |
| `SP_MERCHANT_INF_NO_FIND`       | 服务商PID不存在       | 请先入驻成为服务商                                            |

### 请求示例

```bash
curl 'https://openapi.alipay.com/gateway.do?charset=UTF-8&method=alipay.open.sp.inteop.product.create&format=json&sign=${sign}&app_id=${appid}&version=1.0&sign_type=RSA2&timestamp=${now}' \
 -F 'app_auth_token=${app_auth_token}' \
 -F 'biz_content={
        "inteop_order_no":"2025111811880890",
        "product_code":"I1080300001000060370",
        "inteop_product_details":[{"product_detail_code":"I1140300001000013424"}],
        "inteop_product_price_details":[{"product_detail_code":"I1140300001000013424","price_rate":"0.38"}],
        "mcc_code":"A0001_B0001",
        "trade_scene":"tiny_app",
        "mobile_type":"APP",
        "inteop_merchant_info":{"contact_name":"张三","contact_mobile":"136xxxxxx12"},
        "inteop_app_info":{
                "app_name":"XXXX","app_type":"IOS","app_status":"ONLINE",
                "app_home_screenshot":"XXXX","app_item_screenshot":"XXXX","in_app_screenshot":"XXXX",
                "app_test_account":"account_1","app_test_account_password":"password123",
                "app_auth_pic":"XXXX","app_market":["小米"],"app_pay_screenshot":"XXXX","app_download_link":"XXXX"
        }
}'
```

### 响应示例

```json
{
  "alipay_open_sp_inteop_product_create_response": {
    "code": "10000",
    "msg": "Success",
    "sub_order_no": "2025061211645380",
    "memos": [
      "产品A:产品已全部开通或审核中"
    ]
  },
  "sign": "ERITJKEIJKJHKKKKKKKHJEREEEEEEEEEEE"
}
```

> 说明：本示例仅供参考。