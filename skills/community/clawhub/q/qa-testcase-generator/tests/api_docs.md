# 电商系统 API 接口文档

> 版本: v2.3 | 最后更新: 2026-06-15

---

## 1. 用户注册接口

**POST** `/api/v1/user/register`

**请求头**: `Content-Type: application/json`

**请求体**:
```json
{
  "username": "string, 3-20字符, 字母数字下划线",
  "password": "string, 8-20字符, 必须含大小写字母和数字",
  "email": "string, 合法邮箱格式",
  "phone": "string, 11位手机号, 选填",
  "invite_code": "string, 6位数字, 选填"
}
```

**成功响应** (201):
```json
{
  "code": 0,
  "message": "注册成功",
  "data": {
    "user_id": 100001,
    "token": "jwt_token_string"
  }
}
```

**错误码**:
| 错误码 | HTTP状态码 | 说明 |
|--------|-----------|------|
| 1001 | 400 | 用户名已存在 |
| 1002 | 400 | 邮箱已注册 |
| 1003 | 400 | 密码复杂度不足 |
| 1004 | 400 | 邀请码无效 |
| 1005 | 400 | 参数格式错误 |

---

## 2. 用户登录接口

**POST** `/api/v1/user/login`

**请求体**:
```json
{
  "login_type": "string, enum: password/sms/wechat",
  "account": "string, 邮箱或手机号",
  "password": "string, login_type=password时必填",
  "sms_code": "string, login_type=sms时必填,6位数字",
  "wechat_code": "string, login_type=wechat时必填"
}
```

**成功响应** (200):
```json
{
  "code": 0,
  "message": "登录成功",
  "data": {
    "token": "jwt_token_string",
    "expires_in": 7200,
    "user_info": {
      "user_id": 100001,
      "username": "testuser",
      "avatar_url": "https://cdn.example.com/avatar/default.png"
    }
  }
}
```

**错误码**:
| 错误码 | HTTP状态码 | 说明 |
|--------|-----------|------|
| 2001 | 401 | 账号或密码错误 |
| 2002 | 401 | 短信验证码错误或过期 |
| 2003 | 401 | 微信授权失败 |
| 2004 | 403 | 账号已被锁定，请30分钟后重试 |
| 2005 | 429 | 登录频率过高，请稍后再试 |

---

## 3. 商品搜索接口

**GET** `/api/v1/product/search`

**查询参数**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| keyword | string | 是 | 搜索关键词，1-50字符 |
| category_id | int | 否 | 分类ID，用于筛选 |
| page | int | 否 | 页码，默认1，≥1 |
| page_size | int | 否 | 每页条数，默认20，[1,100] |
| sort_by | string | 否 | 排序方式：price_asc/price_desc/sales/newest |
| min_price | float | 否 | 最低价格，≥0 |
| max_price | float | 否 | 最高价格，≥min_price |

**成功响应** (200):
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "total": 256,
    "page": 1,
    "page_size": 20,
    "total_pages": 13,
    "products": [
      {
        "product_id": 1001,
        "name": "商品名称",
        "price": 99.90,
        "original_price": 129.00,
        "sales_count": 1024,
        "stock": 500,
        "rating": 4.8,
        "image_url": "https://cdn.example.com/product/1001.jpg",
        "is_available": true
      }
    ]
  }
}
```

**错误码**:
| 错误码 | HTTP状态码 | 说明 |
|--------|-----------|------|
| 3001 | 400 | 搜索关键词为空 |
| 3002 | 400 | 价格区间不合法（min_price > max_price） |
| 3003 | 400 | 分类不存在 |
| 3004 | 400 | 分页参数超出范围 |

---

## 4. 商品详情接口

**GET** `/api/v1/product/{product_id}`

**路径参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| product_id | int | 商品ID，≥1 |

**成功响应** (200):
```json
{
  "code": 0,
  "data": {
    "product_id": 1001,
    "name": "无线蓝牙耳机",
    "category_id": 201,
    "category_name": "数码配件",
    "price": 99.90,
    "original_price": 129.00,
    "description": "高品质蓝牙5.3耳机，续航24小时",
    "specs": {"颜色": ["黑色","白色"], "版本": ["标准版","Pro版"]},
    "stock": 500,
    "sales_count": 1024,
    "rating": 4.8,
    "images": ["url1","url2"],
    "reviews_count": 356,
    "is_available": true,
    "delivery_info": {"free_shipping": true, "estimated_days": 2}
  }
}
```

**错误码**:
| 错误码 | HTTP状态码 | 说明 |
|--------|-----------|------|
| 3101 | 404 | 商品不存在 |
| 3102 | 400 | 商品已下架 |

---

## 5. 添加购物车接口

**POST** `/api/v1/cart/add`

**请求体**:
```json
{
  "product_id": "int, 必填",
  "sku_id": "int, 必填",
  "quantity": "int, 必填, 1-99",
  "selected": "bool, 选填, 默认true"
}
```

**成功响应** (200):
```json
{
  "code": 0,
  "message": "添加成功",
  "data": {
    "cart_item_id": 50001,
    "cart_total": 3
  }
}
```

**错误码**:
| 错误码 | HTTP状态码 | 说明 |
|--------|-----------|------|
| 4001 | 400 | 商品不存在 |
| 4002 | 400 | SKU不存在或已失效 |
| 4003 | 400 | 库存不足 |
| 4004 | 400 | 购物车商品已达上限（200种） |
| 4005 | 400 | 同一商品已达最大购买数量 |

---

## 6. 购物车列表接口

**GET** `/api/v1/cart/list`

**响应** (200):
```json
{
  "code": 0,
  "data": {
    "items": [
      {
        "cart_item_id": 50001,
        "product_id": 1001,
        "product_name": "无线蓝牙耳机",
        "sku_id": 20001,
        "sku_spec": "黑色/标准版",
        "price": 99.90,
        "quantity": 2,
        "selected": true,
        "stock": 500,
        "is_available": true
      }
    ],
    "total_price": 199.80,
    "selected_total": 199.80,
    "item_count": 1
  }
}
```

---

## 7. 更新购物车商品接口

**PUT** `/api/v1/cart/update`

**请求体**:
```json
{
  "cart_item_id": "int, 必填",
  "quantity": "int, 必填, 0-99（0=删除该商品）",
  "selected": "bool, 选填"
}
```

**错误码**:
| 错误码 | HTTP状态码 | 说明 |
|--------|-----------|------|
| 4101 | 400 | 购物车商品不存在 |
| 4102 | 400 | 更新后的数量超过库存 |

---

## 8. 下单接口

**POST** `/api/v1/order/create`

**请求体**:
```json
{
  "address_id": "int, 必填",
  "cart_item_ids": "int[], 必填, 至少1项, 最多200项",
  "coupon_id": "int, 选填",
  "remark": "string, 选填, 最多200字",
  "payment_method": "string, 必填, enum: wechat/alipay/balance",
  "invoice_type": "string, 选填, enum: personal/company/none"
}
```

**成功响应** (201):
```json
{
  "code": 0,
  "message": "下单成功",
  "data": {
    "order_id": "OD202606150001",
    "total_amount": 299.70,
    "discount_amount": 10.00,
    "final_amount": 289.70,
    "estimated_delivery": "2026-06-18",
    "payment_url": "https://pay.example.com/order/OD202606150001"
  }
}
```

**错误码**:
| 错误码 | HTTP状态码 | 说明 |
|--------|-----------|------|
| 5001 | 400 | 收货地址不存在 |
| 5002 | 400 | 商品信息已变更，请重新确认 |
| 5003 | 400 | 部分商品库存不足 |
| 5004 | 400 | 优惠券不可用或已过期 |
| 5005 | 400 | 订单金额低于起送金额 |
| 5006 | 400 | 购物车商品已变更 |

---

## 9. 订单列表接口

**GET** `/api/v1/order/list`

**查询参数**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| status | string | 否 | 筛选状态：pending/paid/shipped/completed/cancelled/refunded |
| page | int | 否 | 默认1 |
| page_size | int | 否 | 默认10, [1,50] |
| start_date | string | 否 | 开始日期, YYYY-MM-DD |
| end_date | string | 否 | 结束日期, ≥start_date |

**错误码**:
| 错误码 | HTTP状态码 | 说明 |
|--------|-----------|------|
| 6001 | 400 | 状态参数不合法 |
| 6002 | 400 | 日期范围超过90天 |

---

## 10. 订单详情接口

**GET** `/api/v1/order/{order_id}`

**路径参数**: `order_id` - 订单编号（OD开头+14位数字）

**成功响应** (200): 返回完整订单信息，包含商品明细、物流信息、支付记录、状态变更时间线

**错误码**:
| 错误码 | HTTP状态码 | 说明 |
|--------|-----------|------|
| 6101 | 404 | 订单不存在 |
| 6102 | 403 | 无权查看该订单 |

---

## 11. 取消订单接口

**POST** `/api/v1/order/cancel`

**请求体**:
```json
{
  "order_id": "string, 必填",
  "reason": "string, 必填, 10-200字",
  "cancel_type": "string, 必填, enum: buyer_initiated/system/timeout"
}
```

**错误码**:
| 错误码 | HTTP状态码 | 说明 |
|--------|-----------|------|
| 6201 | 400 | 订单状态不允许取消 |
| 6202 | 400 | 订单已发货，无法取消 |
| 6203 | 400 | 取消失败，请联系客服 |
| 6204 | 400 | 退款处理中，请勿重复操作 |

---

## 12. 支付回调接口

**POST** `/api/v1/payment/callback`

**请求头**: `Content-Type: application/x-www-form-urlencoded`

**参数**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| order_id | string | 是 | 商户订单号 |
| trade_no | string | 是 | 支付平台交易号 |
| total_amount | float | 是 | 支付金额 |
| payment_time | string | 是 | 支付时间, ISO8601格式 |
| sign | string | 是 | 签名 |
| trade_status | string | 是 | TRADE_SUCCESS / TRADE_FAILED / TRADE_CLOSED |

**成功响应** (200):
```
success
```

**失败响应** (200):
```
fail
```

**说明**: 支付回调必须幂等，同一 order_id 重复回调不重复处理。签名验证失败返回`fail`但不记录错误。

**错误码**: 无业务错误码，HTTP 200 + body "fail" 表示处理失败。
