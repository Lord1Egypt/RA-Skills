# ant.merchant.expand.bizaccess.order.query (开通进度主动查询)

**接口用途**：用于服务商代商户开通进度主动查询，主要用于业务申请单流转状态查询，可以结合"消息通知"异步接口协同使用。

**核心状态说明：**

- 待确认（WAIT_TO_CONFIRM）：接口会额外返回待办小程序商家确认页链接，服务商可生成二维码提供商家反扫工具
- 成功完结（SUCCESS）：业务单据开通完成，服务商可进行业务开通结果表达或推进后续流程
- 失败完结（FAIL）：服务商可获取失败原因（fail_reasons）反馈错误原因来提示引导后续行动点或解决方案

**文档地址**：https://opendocs.alipay.com/isv/cc0c6699_ant.merchant.expand.bizaccess.order.query

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

| 参数         | 类型     | 必填  | 说明                                      |
|------------|--------|-----|-----------------------------------------|
| `order_id` | string | 二选一 | 服务商代商户开通业务申请单的主单号（必填，本期仅支持使用order_id查询） |
| `pid`      | string | 二选一 | 商户id（本期不支持使用pid查询）                      |

### 公共响应参数

| 参数         | 类型     | 必填 | 说明      |
|------------|--------|----|---------|
| `code`     | string | 是  | 网关返回码   |
| `msg`      | string | 是  | 网关返回码描述 |
| `sub_code` | string | 否  | 业务返回码   |
| `sub_msg`  | string | 否  | 业务返回码描述 |
| `sign`     | string | 是  | 签名      |

### 业务响应参数

| 参数                      | 类型                                 | 必填 | 说明          |
|-------------------------|------------------------------------|----|-------------|
| `order_status`          | string                             | 是  | 申请单状态，见枚举值  |
| `order_id`              | string                             | 是  | 业务开通主单号     |
| `merchant_pid`          | string                             | 是  | 商户号         |
| `fail_reasons`          | array\<IsvBizOpenOrderFailReason\> | 否  | 失败原因，见下方子属性 |
| `wait_process_task_url` | string                             | 否  | 待办url       |
| `sub_merchant_orders`   | array                              | 否  | 子单列表，见下方子属性 |
| `order_content`         | object                             | 否  | 订单信息，见下方子属性 |

#### order_status（申请单状态）枚举值

| 枚举名  | 枚举值             |
|------|-----------------|
| 初始化  | INIT            |
| 待审核  | WAIT_TO_AUDIT   |
| 待确认  | WAIT_TO_CONFIRM |
| 确认中  | CONFIRMING      |
| 成功完结 | SUCCESS         |
| 失败完结 | FAIL            |

#### fail_reasons（失败原因）子参数

| 参数           | 类型     | 必填 | 说明   |
|--------------|--------|----|------|
| `error_code` | string | 是  | 错误码  |
| `error_msg`  | string | 是  | 错误原因 |

#### sub_merchant_orders（子单列表）子参数

| 参数                 | 类型     | 必填 | 说明          |
|--------------------|--------|----|-------------|
| `m_order_id`       | string | 是  | 主申请单id      |
| `sub_order_type`   | string | 是  | 子单类型        |
| `sub_order_status` | string | 是  | 子单状态        |
| `order_content`    | object | 否  | 订单信息，见下方子属性 |

#### order_content（订单信息）子参数

| 参数                         | 类型              | 必填 | 说明            |
|----------------------------|-----------------|----|---------------|
| `merchant_id`              | string          | 否  | 商户ID          |
| `phone`                    | string          | 否  | 商户联系电话        |
| `mcc_code`                 | string          | 否  | 商户二级类目code    |
| `need_operation_auth`      | boolean         | 否  | 是否需要代运营授权     |
| `need_interface_auth`      | boolean         | 否  | 是否需要代开发授权     |
| `merchant_name`            | string          | 否  | 商户名称          |
| `scene_biz_code`           | array\<string\> | 否  | 业务场景码         |
| `merchant_logon_id`        | string          | 否  | 商户登录号         |
| `need_register_merchant`   | boolean         | 否  | 是否需要代入驻       |
| `merchant_type`            | string          | 否  | 商户类型          |
| `optional_front_prod_code` | array\<string\> | 否  | 可选的前台产品       |
| `qualifications`           | array           | 否  | 资质信息，见下方子属性   |
| `license_info`             | object          | 否  | 主体证照信息，见下方子属性 |
| `isv_commission_info`      | array           | 否  | 抽佣信息，见下方子属性   |
| `price_infos`              | array           | 否  | 价格信息，见下方子属性   |
| `benefit_info`             | object          | 否  | 受益人证照         |
| `legal_info`               | object          | 否  | 法人证照          |

##### qualifications（资质信息）子参数

| 参数               | 类型              | 必填 | 说明                                  |
|------------------|-----------------|----|-------------------------------------|
| `type`           | string          | 是  | 资质类型                                |
| `cert_no`        | string          | 是  | 资质Code                              |
| `effective_date` | string          | 是  | 资质有效期，格式yyyy-MM-dd，长期有效传入9999-12-31 |
| `license_name`   | string          | 否  | 资质名称                                |
| `license_urls`   | array\<string\> | 否  | 凭证图片链接                              |

##### license_info（主体证照信息）子参数

| 参数               | 类型              | 必填 | 说明     |
|------------------|-----------------|----|--------|
| `type`           | string          | 是  | 资质类型   |
| `cert_no`        | string          | 是  | 资质Code |
| `effective_date` | string          | 是  | 资质有效期  |
| `license_name`   | string          | 否  | 资质名称   |
| `license_urls`   | array\<string\> | 否  | 凭证图片链接 |

##### isv_commission_info（抽佣信息）子参数

| 参数                           | 类型      | 必填   | 说明                                                       |
|------------------------------|---------|------|----------------------------------------------------------|
| `commission_mode`            | string  | 是    | 抽佣模式：USER_UNIFORM_SCALE-用户统一比例、ITEM_UNIFORM_SCALE-商品统一比例 |
| `commission_scene`           | string  | 是    | 抽佣场景                                                     |
| `long_term`                  | boolean | 是    | 是否是长期模式场景                                                |
| `merchant_app_id`            | string  | 条件必填 | 商家应用appId                                                |
| `isv_rate`                   | string  | 否    | 服务商抽佣比例，无单位，如0.0400表示4%                                  |
| `commission_valid_time`      | string  | 否    | 抽佣开始时间                                                   |
| `commission_invalid_time`    | string  | 否    | 抽佣结束时间                                                   |
| `item_mode_commission_list`  | array   | 否    | 商品抽佣比例                                                   |
| `commission_first_role_list` | array   | 否    | 合作伙伴抽佣信息                                                 |

##### price_infos（价格信息）子参数

| 参数                  | 类型     | 必填 | 说明                              |
|---------------------|--------|----|---------------------------------|
| `back_product_code` | string | 否  | 后台产品码：I1140100001000001000-商家扣款 |
| `price_rate`        | string | 否  | 费率，最多两位小数，范围0.38～0.6，单位%        |

### 错误码

| 错误码                 | 说明    | 解决方案                                        |
|---------------------|-------|---------------------------------------------|
| `SYSTEM_ERROR`      | 系统繁忙  | 服务器异常，可能发生了网络或者系统异常，导致服务调用失败，商户可以用同样的请求发起重试 |
| `INVALID_PARAMETER` | 参数有误  | 请根据接口返回的参数非法的具体错误信息，修改参数后进行重试               |
| `NO_PERMISSION`     | 数据无权限 | 请确保账号拥有正确的数据权限                              |

### 请求示例

```bash
curl 'https://openapi.alipay.com/gateway.do?charset=UTF-8&method=ant.merchant.expand.bizaccess.order.query&format=json&sign=${sign}&app_id=${appid}&version=1.0&sign_type=RSA2&timestamp=${now}' \
 -F 'app_auth_token=${app_auth_token}' \
 -F 'biz_content={
        "order_id":"2024111100502000000000000000",
        "pid":"208830189531XXXX"
}'
```

### 响应示例

```json
{
  "ant_merchant_expand_bizaccess_order_query_response": {
    "code": "10000",
    "msg": "Success",
    "order_status": "WAIT_TO_AUDIT",
    "order_id": "202411110050200000000000XXXX",
    "fail_reasons": [
      {
        "error_code": "100",
        "error_msg": "错误原因"
      }
    ],
    "wait_process_task_url": "alipays://platformapi/startapp?appId=2018090561299510&page=pages/wait-deal-common/index?orderId=2024112700502000000041130000",
    "sub_merchant_orders": [
      {
        "m_order_id": "2025040765435432432",
        "sub_order_type": "REGISTRATION",
        "sub_order_status": "SUCCESS"
      }
    ],
    "order_content": {
      "merchant_id": "20888826252",
      "phone": "15612345678",
      "mcc_code": "B0064",
      "need_operation_auth": true,
      "need_interface_auth": true,
      "merchant_name": "XXX有限公司",
      "scene_biz_code": [
        "AXF_MERCHANT_PERIOD_PAY"
      ],
      "merchant_logon_id": "zhangsancompanyXXX@163.com",
      "need_register_merchant": true,
      "merchant_type": "01",
      "optional_front_prod_code": [
        "I1140100001000001000"
      ],
      "qualifications": [
        {
          "type": "3128",
          "license_name": "xx有限公司",
          "cert_no": "91350602MXXXXXXXXX",
          "effective_date": "2024-10-01",
          "license_urls": [
            "xxxxxxxxxxxx.jpg"
          ]
        }
      ],
      "license_info": {
        "type": "3128",
        "license_name": "xx有限公司",
        "cert_no": "91350602MXXXXXXXXX",
        "effective_date": "2024-10-01",
        "license_urls": [
          "xxxxxxxxxxxx.jpg"
        ]
      },
      "isv_commission_info": [
        {
          "commission_mode": "USER_UNIFORM_SCALE",
          "commission_scene": "ANXINFU_PERIOD_CARD_SAAS",
          "merchant_app_id": "201406060016XXXX",
          "isv_rate": "0.0400",
          "commission_valid_time": "2024-10-01",
          "commission_invalid_time": "2024-10-01",
          "long_term": true,
          "item_mode_commission_list": [
            {
              "item_id": "2023102522000XXXXXX000",
              "item_rate": "0.0400"
            }
          ],
          "commission_first_role_list": [
            {
              "role_alipay_account": "zhangsancompanyXXX@163.com",
              "role_account_name": "XXX有限公司",
              "role_type": "SUPPLIER_ROLE",
              "role_rate": "0.0400"
            }
          ]
        }
      ],
      "price_infos": [
        {
          "back_product_code": "I1140100001000001000",
          "price_rate": "0.38"
        }
      ],
      "benefit_info": {
        "cert_no": "3301000xxxxx222",
        "cert_type": "100",
        "cert_pic_url_type": "ORIGINAL",
        "cert_pic_urls": [
          "key3432749273.jpg"
        ],
        "cert_name": "赵xx",
        "gmt_valid": "2024-01-01",
        "gmt_invalid": "2024-1-1",
        "business_scope": "零售",
        "reg_capital": "杭州市xxx街道xxx室"
      },
      "legal_info": {
        "cert_no": "3301000xxxxx222",
        "cert_type": "100",
        "cert_pic_url_type": "ORIGINAL",
        "cert_pic_urls": [
          "key3432749273.jpg"
        ],
        "cert_name": "赵xx",
        "gmt_valid": "2024-01-01",
        "gmt_invalid": "2024-1-1",
        "business_scope": "零售",
        "reg_capital": "杭州市xxx街道xxx室"
      }
    },
    "merchant_pid": "2088354xxxx"
  },
  "sign": "ERITJKEIJKJHKKKKKKKHJEREEEEEEEEEEE"
}
```

> 说明：本示例仅供参考。