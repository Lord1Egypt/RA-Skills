# alipay.open.agent.common.sign (代签约产品通用接口)

**接口用途**：三方应用代理签约产品，需要配合开启事务接口使用。

**文档地址**：https://opendocs.alipay.com/isv/234689cd_alipay.open.agent.common.sign

### 公共请求参数

| 参数               | 类型     | 必填 | 说明                             |
|------------------|--------|----|--------------------------------|
| `app_id`         | string | 是  | 支付宝分配给开发者的应用ID                 |
| `method`         | string | 是  | 接口名称                           |
| `format`         | string | 否  | 仅支持JSON                        |
| `charset`        | string | 是  | 请求使用的编码格式，如utf-8, gbk, gb2312等 |
| `sign_type`      | string | 是  | 签名算法类型：RSA2或RSA，推荐使用RSA2       |
| `sign`           | string | 是  | 商户请求参数的签名串                     |
| `timestamp`      | string | 是  | 发送请求的时间，格式yyyy-MM-dd HH:mm:ss  |
| `version`        | string | 是  | 接口版本，固定为1.0                    |
| `app_auth_token` | string | 否  | 应用授权令牌                         |

### 业务请求参数

| 参数                          | 类型              | 必填   | 说明                                                                         |
|-----------------------------|-----------------|------|----------------------------------------------------------------------------|
| `batch_no`                  | string          | 是    | 代商户操作事务编号，通过alipay.open.agent.create接口进行创建                                 |
| `mcc_code`                  | string          | 是    | 商家经营类目2.0中的"经营类目编码"                                                        |
| `product_code`              | string          | 是    | isv要代商户签约产品码，产品码是支付宝内部对产品的唯一标识                                             |
| `special_license_pic`       | byte[]          | 条件必填 | 企业特殊资质图片，文件最小5KB，最大5M，格式必须为png、bmp、gif、jpg、jpeg                            |
| `business_license_no`       | string          | 否    | 营业执照号码                                                                     |
| `business_license_pic`      | byte[]          | 否    | 营业执照图片，被代创建商户运营主体为个人账户必填，企业账户无需填写                                          |
| `business_license_auth_pic` | byte[]          | 否    | 营业执照授权函图片，个体工商户如果使用总公司或其他公司的营业执照认证需上传该授权函图片                                |
| `long_term`                 | boolean         | 否    | 营业期限是否长期有效                                                                 |
| `date_limitation`           | string          | 否    | 营业期限                                                                       |
| `alipay_life_name`          | string          | 否    | 支付宝生活号（原服务窗）名称                                                             |
| `special_license_type`      | string          | 否    | 合约特殊资质的类型，不传默认99（其他附件）                                                     |
| `rate`                      | string          | 否    | 服务费率（%），范围0.38~0.6                                                         |
| `life_app_id`               | string          | 否    | 被签约商户的支付宝生活号ID编号                                                           |
| `mini_app_id`               | string          | 条件必填 | 被签约商家下任意小程序APPID编号                                                         |
| `mini_app_name`             | string          | 条件必填 | 小程序名称                                                                      |
| `mini_app_screenshot`       | byte[]          | 条件必填 | 小程序截图信息                                                                    |
| `h_5_status`                | string          | 条件必填 | H5网站状态：ONLINE-已上线、OFFLINE-未上线                                              |
| `h_5_memo`                  | string          | 条件必填 | 网站扩展信息文本                                                                   |
| `h_5_extra_pic`             | byte[]          | 条件必填 | 网站备注图片                                                                     |
| `h_5_sites`                 | string          | 条件必填 | H5网站地址                                                                     |
| `h_5_home_screenshot`       | byte[]          | 条件必填 | H5网站首页截图                                                                   |
| `h_5_item_screenshot`       | byte[]          | 条件必填 | H5网站商品截图                                                                   |
| `h_5_pay_screenshot`        | byte[]          | 条件必填 | H5网站支付页截图                                                                  |
| `h_5_sites_loa`             | byte[]          | 条件必填 | H5网站授权函                                                                    |
| `app_item_screenshot`       | byte[]          | 条件必填 | 商品或服务页截图                                                                   |
| `app_test_account`          | string          | 条件必填 | 可以登录该应用的测试账户                                                               |
| `app_name`                  | string          | 条件必填 | 商户的APP应用名称                                                                 |
| `app_status`                | string          | 条件必填 | 应用状态：ONLINE-已上线、OFFLINE-未上线                                                |
| `app_market`                | string          | 条件必填 | 投放应用市场：苹果、应用宝、华为、360、小米、豌豆荚、其他                                             |
| `app_auth_pic`              | byte[]          | 条件必填 | APP授权函图片                                                                   |
| `download_link`             | string          | 条件必填 | 应用下载链接                                                                     |
| `app_home_screenshot`       | byte[]          | 条件必填 | 应用首页截图                                                                     |
| `app_pay_screenshot`        | byte[]          | 条件必填 | 应用内支付页截图                                                                   |
| `app_demo`                  | byte[]          | 条件必填 | APP demo（格式为.apk）或应用说明文档（格式为.doc、.docx、.pdf）                               |
| `app_test_account_password` | string          | 条件必填 | 可以登录此应用的账户的密码                                                              |
| `shop_scene_pic`            | byte[]          | 条件必填 | 店铺内景图片                                                                     |
| `shop_sign_board_pic`       | byte[]          | 条件必填 | 店铺门头照图片                                                                    |
| `shop_province_code`        | string          | 条件必填 | 门店所在省份                                                                     |
| `shop_city_code`            | string          | 条件必填 | 门店所在城市                                                                     |
| `shop_district_code`        | string          | 条件必填 | 门店所在区或县                                                                    |
| `shop_detail_address`       | string          | 条件必填 | 门店详细地址                                                                     |
| `shop_name`                 | string          | 条件必填 | 门店名称                                                                       |
| `web_sites`                 | array\<string\> | 条件必填 | 接入网址信息                                                                     |
| `web_sites_loa`             | byte[]          | 条件必填 | 接入网址的授权函                                                                   |
| `web_test_account`          | string          | 条件必填 | 可以登录此网站的测试账户                                                               |
| `web_test_account_password` | string          | 条件必填 | 可以登录此网站的账户的密码                                                              |
| `web_home_screenshot`       | byte[]          | 条件必填 | 网站首页截图                                                                     |
| `web_item_screenshot`       | byte[]          | 条件必填 | 网站商品页截图                                                                    |
| `web_pay_screenshot`        | byte[]          | 条件必填 | 网站支付页截图                                                                    |
| `web_status`                | string          | 条件必填 | 网站状态：ONLINE-已上线、OFFLINE-未上线                                                |
| `trade_scene`               | string          | 条件必填 | 交易场景：pc-电脑网站支付、mobile-手机网站支付、tiny_app-JSAPI、offline_store-线下场所、预授权支付时至少传一个 |
| `mobile_type`               | string          | 条件必填 | 移动设备类型：APP、H5                                                              |

#### trade_scene（交易场景）枚举值

| 枚举名  | 枚举值           |
|------|---------------|
| 小程序  | tiny_app      |
| 移动设备 | mobile        |
| 线下场所 | offline_store |
| PC网站 | pc            |

#### mobile_type（移动设备类型）枚举值

| 枚举名 | 枚举值 |
|-----|-----|
| APP | APP |
| H5  | H5  |

#### app_status（应用状态）枚举值

| 枚举名 | 枚举值     |
|-----|---------|
| 已上线 | ONLINE  |
| 未上线 | OFFLINE |

#### h_5_status / web_status（H5网站状态/网站状态）枚举值

| 枚举名 | 枚举值     |
|-----|---------|
| 已上线 | ONLINE  |
| 未上线 | OFFLINE |

#### app_market（投放应用市场）枚举值

| 枚举名 | 枚举值 |
|-----|-----|
| 苹果  | 苹果  |
| 应用宝 | 应用宝 |
| 华为  | 华为  |
| 360 | 360 |
| 小米  | 小米  |
| 豌豆荚 | 豌豆荚 |
| 其他  | 其他  |

### 公共响应参数

| 参数         | 类型     | 必填 | 说明      |
|------------|--------|----|---------|
| `code`     | string | 是  | 网关返回码   |
| `msg`      | string | 是  | 网关返回码描述 |
| `sub_code` | string | 否  | 业务返回码   |
| `sub_msg`  | string | 否  | 业务返回码描述 |
| `sign`     | string | 是  | 签名      |

### 业务响应参数

无业务响应参数

### 错误码

| 错误码                                   | 说明                      | 解决方案                                                                   |
|---------------------------------------|-------------------------|------------------------------------------------------------------------|
| `SYSTEM_ERROR`                        | 系统繁忙                    | 服务器异常，可能发生了网络或者系统异常，导致服务调用失败，商户可以用同样的请求发起重试                            |
| `INVALID_PARAMETER`                   | 参数有误                    | 请根据接口返回的参数非法的具体错误信息，修改参数后进行重试                                          |
| `ADMIT_ORDER_NO_PASS`                 | 代商户签约预校验不通过             | 商户签约预校验不通过，该商户没有资质或存在签约中订单或该渠道没有面向该商家开放                                |
| `ANT_PRODUCT_CONFLICT`                | 您已签约此产品，或者同类产品          | 确保批量签约的产品没有冲突                                                          |
| `ANT_PRODUCT_DEPENDENCY_REQUIRED`     | 产品之间存在依赖                | 你还未签约支付宝支付产品（如电脑网站支付、手机网站支付、APP支付、当面付等），请签约后再开通本产品                     |
| `BATCH_IS_NOT_EXIST`                  | 代商户操作事务编号不存在            | 请检查事务编号是否有效                                                            |
| `BATCH_STATUS_IS_FINAL`               | 事务已经达到终态                | 请确认事务状态是否是init状态，submit/cancel/timeout状态的都是终态，不允许继续进行接口调用              |
| `BIZ_ERROR`                           | 业务异常                    | 具体失败原因，请参考接口返回的错误信息                                                    |
| `BUSINESS_LICENSE_PIC_RISK`           | 营业执照不合法                 | 请检查参数business_license_pic是否是营业执照；营业执照法人姓名是否一致；营业执照法人身份信息是否一致；营业执照是否已过期 |
| `CHECK_AGDS_SELLER_ACCESS_FAILED`     | 蚂蚁花呗专享认证不通过             | 请检查蚂蚁花呗专享是否认证通过                                                        |
| `CHECK_MERCHANT_ACCESS_CERT_PUNISHED` | 商户存在风险，禁止签约             | 商户存在风险，禁止签约，请更换账号签约                                                    |
| `FILE_FORMAT_IS_INVALID`              | 文件格式错误                  | 请检查文件类型的参数格式                                                           |
| `FILE_SIZE_MIN_LIMIT`                 | 文件大小低于范围                | 请检查文件类型的参数大小                                                           |
| `FILE_SIZE_OUT_LIMIT`                 | 文件大小超出范围                | 请检查文件类型的参数大小                                                           |
| `INVALID_BATCH_NO`                    | 事务编号batch_no不能为空        | 事务编号batch_no不能为空                                                       |
| `ISV_APP_NO_ORDER_PACKAGE`            | 第三方应用没有挂载该功能包           | 请挂载对应功能包                                                               |
| `ISV_APP_ORDER_PACKAGE_EMPTY`         | 第三方应用没有任何需要签约开通的功能包     | 请挂载对应功能包                                                               |
| `ISV_IDENTITY_NOT_SATISFY`            | 当前账户已入驻为服务商，不能签约收钱产品    | 请更换账号签约                                                                |
| `MERCHANT_NEED_FACE_CERTIFY`          | 需要商户完成身份证或人脸认证后，才能代商户签约 | 请联系代签约的商户先完成身份证或人脸认证后，再代商户签约                                           |
| `MERCHANT_SIGN_PRODUCT_IN_AUDIT`      | 签约审核中                   | 该商户签约审核中，暂时不能操作，请等签约审核结束后再试                                            |
| `MERCHANT_SIGN_PRODUCT_IN_FORBIDD`    | 无法进行签约                  | 该商户无法签约当前产品，存在产品签约冲突                                                   |
| `MERCHANT_STATE_NOT_SATISFY`          | 商户被清退或禁止续签，不允许签约        | 请检查商户状态，再重新签约                                                          |
| `NOT_MATCHED_SSU_OR_PS`               | 产品不支持当前类目               | 请检查商户的MCC类目以及填写的经营类目是否准确                                               |
| `NO_APP_PERMISSION`                   | APPID不匹配                | 请检查当前调用的appId和创建事务的appId是否匹配                                           |
| `OPEN_API_SIGN_ISV_NOT_IN_WHITELIST`  | isv不在白名单中               | 该接口暂未开放                                                                |
| `OPEN_API_SIGN_PRODUCT_NOT_SUPPORT`   | 不支持该产品签约                | 暂不支持该产品码，产品不在openapi签约渠道开放或者产品已下线                                      |
| `PRODUCT_NO_OPENABLE_PERMISSION_SET`  | 当前签约产品不存在可开通的权限集        | 当前产品暂未开放任何可签约的权限集                                                      |
| `RISK_ADVICE_ERROR`                   | 商户风险咨询校验失败              | 具体失败原因及解决方案，请参考接口返回的描述文案                                               |
| `SHOP_SIGN_BOARD_PIC_RISK`            | 门头照不合法                  | 请检查参数shop_sign_board_pic是否是门头照                                         |
| `UNKNOWN_EXCEPTION`                   | 系统内部错误                  | 请联系客服咨询具体原因                                                            |
| `UN_SUPPORT_ACCOUNT_CERTIFY_LEVEL`    | 账户未达到认证要求               | 请先联系商家完成账号认证，认证通过后重新签约                                                 |
| `UN_SUPPORT_ACCOUNT_TYPE`             | 不支持的签约账号类型              | 请检查代签约的商家账号类型                                                          |
| `USER_ACCOUNT_IS_BLOCK`               | 商户账号被冻结                 | 请检查商户账号是否可用                                                            |
| `USER_CARD_BALANCE_PAY_CLOSED`        | 账户余额支付功能已关闭             | 商家账户余额功能已关闭，请联系商家开启后重新签约                                               |

### 请求示例

```
curl 'https://openapi.alipay.com/gateway.do?charset=UTF-8&method=alipay.open.agent.common.sign&format=json&sign=${sign}&app_id=${appid}&version=1.0&sign_type=RSA2&timestamp=${now}' \
 -F 'app_auth_token=${app_auth_token}' \
 -F 'batch_no=2020062409585609100024230' \
 -F 'mcc_code=A0001_B0001' \
 -F 'special_license_pic=@/home/admin/test.jpg' \
 -F 'business_license_no=1532501100006302' \
 -F 'business_license_pic=@/home/admin/test.jpg' \
 -F 'business_license_auth_pic=@/home/admin/test.jpg' \
 -F 'long_term=true' \
 -F 'date_limitation=2017-11-11' \
 -F 'product_code=FACE_TO_FACE_PAYMENT' \
 -F 'alipay_life_name=杭州xx报社' \
 -F 'special_license_type=99' \
 -F 'rate=0.38' \
 -F 'life_app_id=2030020837517348' \
 -F 'mini_app_id=2021003187665167' \
 -F 'mini_app_name=xxx小程序' \
 -F 'mini_app_screenshot=@/home/admin/test.jpg' \
 -F 'h_5_status=ONLINE' \
 -F 'h_5_memo=相关备注信息' \
 -F 'h_5_extra_pic=@/home/admin/test.jpg' \
 -F 'h_5_sites=www.h5.com' \
 -F 'h_5_home_screenshot=@/home/admin/test.jpg' \
 -F 'h_5_item_screenshot=@/home/admin/test.jpg' \
 -F 'h_5_pay_screenshot=@/home/admin/test.jpg' \
 -F 'h_5_sites_loa=@/home/admin/test.jpg' \
 -F 'app_item_screenshot=@/home/admin/test.jpg' \
 -F 'app_test_account=testAccount' \
 -F 'app_name=应用名称' \
 -F 'app_status=ONLINE' \
 -F 'app_market=豌豆荚' \
 -F 'app_auth_pic=@/home/admin/test.jpg' \
 -F 'download_link=http://demo.com/demo.apk' \
 -F 'app_home_screenshot=@/home/admin/test.jpg' \
 -F 'app_pay_screenshot=@/home/admin/test.jpg' \
 -F 'app_demo=@/home/admin/test.jpg' \
 -F 'app_test_account_password=testPassword' \
 -F 'shop_scene_pic=@/home/admin/test.jpg' \
 -F 'shop_sign_board_pic=@/home/admin/test.jpg' \
 -F 'shop_province_code=370000' \
 -F 'shop_city_code=370900' \
 -F 'shop_district_code=370902' \
 -F 'shop_detail_address=人民路10号' \
 -F 'shop_name=xxx门店' \
 -F 'web_sites=["www.web.com"]' \
 -F 'web_sites_loa=@/home/admin/test.jpg' \
 -F 'web_test_account=testAccount' \
 -F 'web_test_account_password=testPassword' \
 -F 'web_home_screenshot=@/home/admin/test.jpg' \
 -F 'web_item_screenshot=@/home/admin/test.jpg' \
 -F 'web_pay_screenshot=@/home/admin/test.jpg' \
 -F 'web_status=ONLINE' \
 -F 'trade_scene=tiny_app' \
 -F 'mobile_type=APP'
```

### 响应示例

```
{
  "alipay_open_agent_common_sign_response": {
    "code": "10000",
    "msg": "Success"
  },
  "sign": "ERITJKEIJKJHKKKKKKKHJEREEEEEEEEEEE"
}
```

> 说明：本示例仅供参考。