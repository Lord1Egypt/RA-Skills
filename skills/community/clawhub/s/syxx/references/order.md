# 订单查询管理模块

> 通用说明：所有接口响应均包含 `error` 字段（int），`0` = 成功，非 `0` = 失败（此时 `message` 包含错误描述）。下表不再重复列出
`error`。

| 接口     | 方法   | 路由                        | 用途               |
|--------|------|---------------------------|------------------|
| 订单列表   | GET  | /order/list/get           | 按编号/会员/状态/时间搜索订单 |
| 订单号查ID | GET  | /order/index/get-id-by-no | 通过订单编号获取订单ID     |
| 订单状态   | GET  | /order/index/get-status   | 查询订单当前状态         |
| 订单物流   | GET  | /order/index/get-express  | 查询订单物流轨迹         |
| 关闭订单   | POST | /order/operation/close    | ⚠️ 危险操作，需用户确认    |

> **订单状态码对照：** `-1` 已关闭 / `0` 待支付 / `10` 待发货 / `11` 部分发货 / `20` 待收货 / `21` 待自提 / `30` 已完成

---

## 获取订单列表

`GET /order/list/get`

根据会员ID、订单状态、下单时间、订单编号搜索订单信息。

**请求参数：**

| 字段                | 类型     | 必传 | 说明                               |
|-------------------|--------|----|----------------------------------|
| order_no          | string | 否  | 订单编号                             |
| create_time_start | string | 否  | 下单时间-开始，格式 `2026-02-02 00:00:00` |
| create_time_end   | string | 否  | 下单时间-结束，格式 `2026-02-04 23:59:59` |
| member_id         | int    | 否  | 指定会员ID                           |
| status            | int    | 否  | 订单状态（见上方状态码对照）                   |
| page              | int    | 否  | 页码（默认 1）                         |
| page_size         | int    | 否  | 每页数量（默认 6）                       |

**响应字段：**

| 字段                             | 类型     | 说明        |
|--------------------------------|--------|-----------|
| total                          | int    | 当前条件下的总数量 |
| page                           | int    | 当前页       |
| page_size                      | int    | 每页数量      |
| list[].id                      | int    | 订单ID      |
| list[].order_no                | string | 订单编号      |
| list[].pay_price               | float  | 实付金额      |
| list[].order_type              | int    | 订单类型码     |
| list[].activity_type           | int    | 活动类型码     |
| list[].status                  | int    | 订单状态码     |
| list[].create_time             | string | 下单时间      |
| list[].dispatch_type           | int    | 配送方式      |
| list[].buyer_name              | string | 收件人姓名     |
| list[].buyer_mobile            | string | 收件人手机号    |
| list[].buyer_remark            | string | 买家备注      |
| list[].member_id               | int    | 会员ID      |
| list[].member_nickname         | string | 会员昵称      |
| list[].member_realname         | string | 会员真实姓名    |
| list[].member_mobile           | string | 会员手机号     |
| list[].address                 | string | 收货地址      |
| list[].status_text             | string | 订单状态文字    |
| list[].order_type_text         | string | 订单类型文字    |
| list[].activity_type_text      | string | 订单活动类型文字  |
| list[].goods_info[]            | array  | 订单商品列表    |
| list[].goods_info[].title      | string | 商品标题      |
| list[].goods_info[].goods_id   | string | 商品ID      |
| list[].goods_info[].total      | string | 购买数量      |
| list[].goods_info[].price      | float  | 实付价       |
| list[].goods_info[].price_unit | string | 单价        |

```json
{
    "error": 0,
    "total": 1,
    "list": [
        {
            "id": "29057",
            "order_no": "1010260204182752364533",
            "pay_price": "1898.80",
            "order_type": "10",
            "activity_type": "22",
            "status": "11",
            "create_time": "2026-02-04 18:27:52",
            "goods_info": [
                {
                    "title": "大疆 DJI Pocket 2 全能套装",
                    "goods_id": "8588",
                    "total": "1",
                    "price": 1726.95,
                    "price_unit": "1788.00"
                }
            ],
            "dispatch_type": "10",
            "buyer_name": "收件人姓名",
            "buyer_mobile": "15888888888",
            "buyer_remark": "",
            "member_id": "317",
            "member_nickname": "An",
            "member_realname": "李可鑫",
            "member_mobile": "15888888888",
            "address": "浙江省 杭州市 淳安县 啦啦啦",
            "status_text": "部分发货",
            "order_type_text": "普通订单",
            "activity_type_text": null
        }
    ],
    "page": 1,
    "page_size": 20
}
```

---

## 通过订单编号获取订单ID

`GET /order/index/get-id-by-no`

**请求参数：**

| 字段       | 类型     | 必传 | 说明   |
|----------|--------|----|------|
| order_no | string | 是  | 订单编号 |

**响应字段：**

| 字段       | 类型  | 说明   |
|----------|-----|------|
| order_id | int | 订单ID |

```json
{
    "error": 0,
    "order_id": "31711"
}
```

---

## 获取订单状态

`GET /order/index/get-status`

根据订单编号或订单ID查询订单当前状态（后端自动识别传入的是编号还是ID）。

**请求参数：**

| 字段       | 类型     | 必传 | 说明                |
|----------|--------|----|-------------------|
| order_no | string | 是  | 订单编号或订单ID（后端自动识别） |

**响应字段：**

| 字段          | 类型     | 说明     |
|-------------|--------|--------|
| status      | int    | 订单状态码  |
| status_text | string | 订单状态文字 |

```json
{
    "error": 0,
    "status": "30",
    "status_text": "已完成"
}
```

---

## 获取订单物流信息

`GET /order/index/get-express`

根据订单编号或订单ID查询订单物流信息（后端自动识别传入的是编号还是ID）。

**请求参数：**

| 字段       | 类型     | 必传 | 说明                |
|----------|--------|----|-------------------|
| order_no | string | 是  | 订单编号或订单ID（后端自动识别） |

**响应字段：**

| 字段                            | 类型     | 说明     |
|-------------------------------|--------|--------|
| data.express.state            | int    | 物流状态码  |
| data.express.state_text       | string | 物流状态文字 |
| data.express.data[]           | array  | 物流轨迹列表 |
| data.express.data[].date_time | string | 时间     |
| data.express.data[].step      | string | 物流详情   |
| data.express_com              | string | 物流公司名称 |
| data.express_sn               | string | 物流单号   |
| data.address_detail           | string | 收货地址   |

```json
{
    "error": 0,
    "data": {
        "express": {
            "state": "2",
            "data": [
                {
                    "date_time": "2026-03-12 11:52:29",
                    "step": "【济南市】已离开 山东济南分拨交付中心；发往 山东潍坊分拨交付中心"
                },
                {
                    "date_time": "2026-03-11 16:18:16",
                    "step": "【南京市】江苏南京浦口区新城公司 已揽收"
                }
            ],
            "state_text": "疑难"
        },
        "express_com": "韵达快运",
        "express_sn": "315070238346274",
        "address_detail": "啦啦啦"
    }
}
```

---

## ⚠️ 关闭待支付订单

`POST /order/operation/close`

通过订单ID关闭待支付的订单。**此操作不可逆，执行前必须向用户确认。**

**请求参数：**

| 字段 | 类型  | 必传 | 说明   |
|----|-----|----|------|
| id | int | 是  | 订单ID |

**响应字段：**

| 字段      | 类型     | 说明                 |
|---------|--------|--------------------|
| message | string | 失败时返回错误信息，如"订单不存在" |

```json
{
    "error": 0
}
```
