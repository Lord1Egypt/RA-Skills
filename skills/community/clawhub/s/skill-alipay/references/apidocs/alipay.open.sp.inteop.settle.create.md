# alipay.open.sp.inteop.settle.create (服务商一体化开通作业添加入驻开通项)

**接口用途**：服务商一体化开通作业添加入驻开通项

**文档地址**：https://opendocs.alipay.com/isv/a8eff27a_alipay.open.sp.inteop.settle.create

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

| 参数                  | 类型                               | 必填 | 说明                                                       |
|---------------------|----------------------------------|----|----------------------------------------------------------|
| `operator_login_id` | string                           | 是  | 用于接收入驻待办通知的经办人支付宝登录账号                                    |
| `inteop_order_no`   | string                           | 是  | 业务开通主单号，用于一体化作业过程的申请单串联                                  |
| `merchant_type`     | string                           | 是  | 商户类型：01-普通企业、02-事业单位、04-社会组织、05-党政及国家机关、06-小微商户、07-个体工商户 |
| `license_info`      | BizOpenCommonMerchantLicenseInfo | 否  | 主体证照信息，见下方子属性                                            |
| `benefit_info`      | BizOpenCertificateInfoForEntry   | 否  | 受益人证照【废弃】，见下方子属性                                         |
| `legal_info`        | BizOpenCertificateInfoForEntry   | 否  | 法人证照，见下方子属性                                              |
| `benefit_infos`     | array                            | 否  | 多受益人证照信息，见下方子属性                                          |
| `bank_card_info`    | SettleBankCardInfo               | 否  | 银行账户信息，个体工商户、普通企业必填，见下方子属性                               |

#### license_info（主体证照信息）子参数

| 参数               | 类型              | 必填 | 说明                                                                  |
|------------------|-----------------|----|---------------------------------------------------------------------|
| `type`           | string          | 是  | 资质类型，如：201-全国法人营业执照、2011-统一社会信用代码证书等                                |
| `license_name`   | string          | 是  | 资质名称，如营业执照就是营业执照的名称                                                 |
| `cert_no`        | string          | 是  | 证件号，如统一社会信用代码                                                       |
| `effective_date` | string          | 是  | 资质有效期，格式yyyy-MM-dd，长期有效传入9999-12-31                                 |
| `business_scope` | string          | 否  | 经营范围                                                                |
| `reg_capital`    | string          | 否  | 注册地址                                                                |
| `license_pics`   | array\<string\> | 否  | 资质凭证图片，通过ant.merchant.expand.indirect.image.upload接口返回的image_id作为参数 |

#### benefit_info（受益人证照）【废弃】子参数

| 参数              | 类型              | 必填 | 说明                           |
|-----------------|-----------------|----|------------------------------|
| `cert_no`       | string          | 是  | 证件号                          |
| `cert_type`     | string          | 是  | 证件类型，如：100-中国大陆公民身份证、102-护照等 |
| `cert_name`     | string          | 是  | 证件名称                         |
| `gmt_invalid`   | string          | 是  | 失效时间                         |
| `gmt_valid`     | string          | 是  | 生效时间                         |
| `cert_pics`     | array\<string\> | 是  | 证件图片                         |
| `cert_pic_type` | string          | 是  | 证件图片类型：ORIGINAL-原件、COPY-复印件  |

#### legal_info（法人证照）子参数

| 参数              | 类型              | 必填 | 说明                           |
|-----------------|-----------------|----|------------------------------|
| `cert_no`       | string          | 是  | 证件号                          |
| `cert_type`     | string          | 是  | 证件类型，如：100-中国大陆公民身份证、102-护照等 |
| `cert_name`     | string          | 是  | 证件名称                         |
| `gmt_invalid`   | string          | 是  | 失效时间                         |
| `gmt_valid`     | string          | 是  | 生效时间                         |
| `cert_pics`     | array\<string\> | 是  | 证件图片                         |
| `cert_pic_type` | string          | 是  | 证件图片类型：ORIGINAL-原件、COPY-复印件  |

#### benefit_infos（多受益人证照）子参数

| 参数              | 类型              | 必填 | 说明                          |
|-----------------|-----------------|----|-----------------------------|
| `cert_no`       | string          | 是  | 证件号                         |
| `cert_type`     | string          | 是  | 证件类型                        |
| `cert_name`     | string          | 是  | 证件名称                        |
| `gmt_invalid`   | string          | 是  | 失效时间                        |
| `gmt_valid`     | string          | 是  | 生效时间                        |
| `cert_pics`     | array\<string\> | 是  | 证件图片                        |
| `cert_pic_type` | string          | 是  | 证件图片类型：ORIGINAL-原件、COPY-复印件 |

#### bank_card_info（银行账户信息）子参数

| 参数                      | 类型     | 必填 | 说明               |
|-------------------------|--------|----|------------------|
| `usage_type`            | string | 是  | 账户类型：01-对公，02-对私 |
| `account_holder_name`   | string | 是  | 开户名称             |
| `account_inst_name`     | string | 是  | 开户银行             |
| `bank_card_no`          | string | 是  | 银行账号             |
| `account_inst_province` | string | 否  | 开户行所在省           |
| `account_inst_city`     | string | 否  | 开户行所在市           |
| `account_branch_name`   | string | 否  | 银行支行名称           |
| `pbc_bank_code`         | string | 否  | 联行号              |

### 公共响应参数

| 参数         | 类型     | 必填 | 说明      |
|------------|--------|----|---------|
| `code`     | string | 是  | 网关返回码   |
| `msg`      | string | 是  | 网关返回码描述 |
| `sub_code` | string | 否  | 业务返回码   |
| `sub_msg`  | string | 否  | 业务返回码描述 |
| `sign`     | string | 是  | 签名      |

### 业务响应参数

| 参数             | 类型     | 必填 | 说明          |
|----------------|--------|----|-------------|
| `sub_order_no` | string | 否  | 一体化作业子项申请单号 |

### 错误码

| 错误码                                 | 说明                    | 解决方案                               |
|-------------------------------------|-----------------------|------------------------------------|
| `SYSTEM_ERROR`                      | 系统繁忙                  | 服务器异常，可能发生了网络或者系统异常，商户可以用同样的请求发起重试 |
| `INVALID_PARAMETER`                 | 参数有误                  | 请根据接口返回的参数非法的具体错误信息，修改参数后进行重试      |
| `ABNORMAL_MERCHANT_INFORMATION`     | 企业名下账号数已达上限           | 咨询支付宝客服                            |
| `ACCOUNT_UNVERIFIED`                | 经办人账号未实名认证            | 请经办人通过支付宝APP完成实名认证                 |
| `BANK_INST_NOT_EXIST`               | 银行机构不存在               | 银行机构不存在，请核实更新后重试                   |
| `DATA_REVIEW_FAILED`                | 法人或企业信息资料审核不通过        | 请检查法人信息和企业信息是否正确                   |
| `EXCEED_PENDING_ORDER_LIMIT`        | 经办人在途申请单已达上限          | 请先完结经办人在途申请单                       |
| `EXIST_MERCHANT_PID`                | 主单已存在商户号              | 主单已经存在商户号，不能再添加入驻子项                |
| `EXIST_SETTLE_ORDER`                | 入驻子项已存在               | 同一个主单下面只能有一个入驻子项，请更换新的主单号          |
| `INFORMATION_CHECK_FAILED`          | 企业或法人信息校验失败           | 请检查法人信息和企业信息是否正确                   |
| `INTEOP_ORDER_NOT_EXIST`            | 一体化作业主单记录不存在          | 请更换新的有效一体化作业主单                     |
| `INVALID_INTEOP_ORDER_NO`           | 作业主单inteop_order_no无效 | 请输入正确的参数                           |
| `ISV_OPERATIONAL_PERMISSIONS`       | 服务商没有该功能的执行权限         | 找支付宝技术对服务商进行开白                     |
| `ISV_PID_INCONSISTENCY`             | 无操作权限                 | 当前服务商pid和主单服务商pid不一致               |
| `MERCHANT_TYPE_ILLEGAL`             | 商户类型非法                | 请检查商户类型是否正常                        |
| `MERCHANT_TYPE_INTERCEPT`           | 商户类型错误                | 禁止泛金融商户类型开通，更换经办人登录账号              |
| `OPERATOR_LOGIN_ACCOUNT_UNVERIFIED` | 经办人账号不是个人实名支付宝账号      | 更换经办人账号，提供个人支付宝的登录名                |
| `OPERATOR_LOGIN_ID_NOT_EXIST`       | 经办人账号未查询到对应的支付宝账号     | 更换经办人账号，提供个人支付宝的登录名                |
| `ORDER_ALREADY_EXISTS`              | 入驻申请单已存在              | 继续进行上一个申请单，或撤销上一个申请单               |
| `ORDER_CHECK_FAIL`                  | 一体化作业订单校验失败           | 具体明细参见check_result列表数据             |
| `SERCURITY_INTERCEPT`               | 请求频率过高或命中黑名单          | 30分钟后重试，如问题依旧请联系支付宝技术支持            |

### 请求示例

```bash
curl 'https://openapi.alipay.com/gateway.do?charset=UTF-8&method=alipay.open.sp.inteop.settle.create&format=json&sign=${sign}&app_id=${appid}&version=1.0&sign_type=RSA2&timestamp=${now}' \
 -F 'biz_content={
        "operator_login_id":"137XXXXXXXX",
        "inteop_order_no":"20250XXXXXX3563",
        "merchant_type":"01",
        "license_info":{
                "business_scope":"零售商",
                "license_name":"xx有限公司",
                "cert_no":"91350602MXXXXXXXXX",
                "effective_date":"2024-10-01",
                "reg_capital":"浙江省杭州市 xxxx",
                "license_pics":["xxxxxxxxxxxx.jpg"],
                "type":"201"
        },
        "legal_info":{
                "cert_pics":["xxxxxxxxxxx.jpg"],
                "cert_type":"100",
                "cert_name":"赵xx",
                "cert_pic_type":"ORIGINAL",
                "cert_no":"3301000xxxxx222",
                "gmt_invalid":"2024-1-1",
                "gmt_valid":"2024-01-01"
        },
        "benefit_infos":[{
                "cert_pics":["xxxxxxxxxxx.jpg"],
                "cert_type":"100",
                "cert_name":"赵xx",
                "cert_pic_type":"ORIGINAL",
                "cert_no":"3301000xxxxx222",
                "gmt_invalid":"2024-1-1",
                "gmt_valid":"2024-01-01"
        }],
        "bank_card_info":{
                "account_inst_name":"XXX银行",
                "usage_type":"01",
                "account_holder_name":"XXX",
                "pbc_bank_code":"XXX",
                "bank_card_no":"XXX",
                "account_inst_city":"XX市",
                "account_inst_province":"XX省",
                "account_branch_name":"XXX"
        }
}'
```

### 响应示例

```json
{
  "alipay_open_sp_inteop_settle_create_response": {
    "code": "10000",
    "msg": "Success",
    "sub_order_no": "202505XXXX"
  },
  "sign": "ERITJKEIJKJHKKKKKKKHJEREEEEEEEEEEE"
}
```

> 说明：本示例仅供参考。