# 数据统计模块

> 通用说明：所有接口响应均包含 `error` 字段（int），`0` = 成功，非 `0` = 失败（此时 `message` 包含错误描述）。下表不再重复列出
`error`。

| 接口     | 方法  | 路由                               | 用途            |
|--------|-----|----------------------------------|---------------|
| 待办事项   | GET | /statistics/overview/to-do       | 待发货、待付款等待办数量  |
| 运营数据   | GET | /statistics/overview/operational | 成交额、退款、订单数等   |
| 新增会员统计 | GET | /statistics/overview/new-member  | 各渠道新增会员折线     |
| 新增订单统计 | GET | /statistics/overview/new-order   | 各渠道新增订单折线     |
| 浏览量分析  | GET | /statistics/overview/view-data   | 各渠道 PV/UV     |
| 商品销量排行 | GET | /statistics/overview/goods-rank  | 各渠道商品销量、销售额排行 |
| 会员消费排行 | GET | /statistics/overview/member-rank | 各渠道会员消费排行     |
| 商品基础数据 | GET | /statistics/goods/basic          | 被浏览/加购/购买商品数  |

> **渠道字段说明**（多个接口共用）：`mall` = 综合商城（必返），`communityBuy` = 社区团购，`siteApp` = 智慧轻站，`promoter` =
> 推客带货。后三者仅在商城开启对应业务时返回。

---

## 待办事项数据

`GET /statistics/overview/to-do`

无请求参数。

**响应字段：**

| 字段                         | 类型  | 说明        |
|----------------------------|-----|-----------|
| data.wait_delivery_order   | int | 待发货订单数量   |
| data.wait_pay_order        | int | 待支付订单数量   |
| data.wait_after_sale_order | int | 待处理售后订单数量 |
| data.wait_replenish_goods  | int | 待补货商品数量   |
| data.wait_audit_member     | int | 待审核会员数量   |

```json
{
    "error": 0,
    "data": {
        "wait_delivery_order": 1737,
        "wait_pay_order": 943,
        "wait_after_sale_order": 83,
        "wait_replenish_goods": 35,
        "wait_audit_member": 0
    }
}
```

---

## 运营数据

`GET /statistics/overview/operational`

**请求参数：**

| 字段     | 类型     | 必传 | 说明                                                  |
|--------|--------|----|-----------------------------------------------------|
| period | string | 是  | `today` / `yesterday` / `week`(近7日) / `month`(近30日) |

**响应字段：**

| 字段                                      | 类型     | 说明                          |
|-----------------------------------------|--------|-----------------------------|
| data.order_pay_price                    | float  | 成交金额（元）                     |
| data.order_refund_price                 | float  | 退款金额（元）                     |
| data.order_pay                          | int    | 支付订单数（笔）                    |
| data.unit_price                         | float  | 笔单价（元）                      |
| data.guest_unit_price                   | int    | 客单价（元）                      |
| data.order_pay_member                   | int    | 支付人数                        |
| data.new_member_count                   | int    | 新会员数量                       |
| data.compare                            | object | 与昨日对比（仅 `period=today` 时返回） |
| data.compare.compare_order_pay_price    | int    | 较昨日成交金额比例(%)                |
| data.compare.compare_order_refund_price | int    | 较昨日退款金额比例(%)                |
| data.compare.compare_order_pay          | int    | 较昨日支付订单数比例(%)               |
| data.compare.compare_unit_price         | int    | 较昨日笔单价比例(%)                 |
| data.compare.compare_guest_unit_price   | int    | 较昨日客单价比例(%)                 |
| data.compare.compare_change             | int    | 较昨日支付人数比例(%)                |
| data.compare.compare_new_member_count   | int    | 较昨日新会员数量比例(%)               |

```json
{
    "error": 0,
    "data": {
        "order_pay_price": 139,
        "order_refund_price": 120.25,
        "order_pay": 2,
        "unit_price": 69.5,
        "guest_unit_price": 139,
        "order_pay_member": 1,
        "new_member_count": 0,
        "compare": {
            "compare_order_pay_price": 100,
            "compare_order_refund_price": 100,
            "compare_order_pay": 100,
            "compare_unit_price": 100,
            "compare_guest_unit_price": 100,
            "compare_change": 0,
            "compare_new_member_count": 100
        }
    }
}
```

---

## 新增会员统计

`GET /statistics/overview/new-member`

**请求参数：**

| 字段     | 类型     | 必传 | 说明                                       |
|--------|--------|----|------------------------------------------|
| period | string | 是  | `today` / `yesterday` / `week` / `month` |

**响应字段：** 按渠道返回时间序列数组，每个元素包含 `period`（时间点）和 `count`（数量）。

| 字段                  | 类型    | 说明         |
|---------------------|-------|------------|
| data.mall[]         | array | 综合商城（必返）   |
| data.communityBuy[] | array | 社区团购（有则返回） |
| data.siteApp[]      | array | 智慧轻站（有则返回） |
| data.promoter[]     | array | 推客带货（有则返回） |

```json
{
    "error": 0,
    "data": {
        "mall": [
            {
                "period": "00:00",
                "count": 0
            },
            {
                "period": "01:00",
                "count": 2
            },
            "... 每小时一个数据点，至 23:00"
        ],
        "communityBuy": [
            "... 同上结构"
        ],
        "siteApp": [
            "... 同上结构"
        ],
        "promoter": [
            "... 同上结构"
        ]
    }
}
```

---

## 新增订单统计

`GET /statistics/overview/new-order`

**请求参数：**

| 字段     | 类型     | 必传 | 说明                                       |
|--------|--------|----|------------------------------------------|
| period | string | 是  | `today` / `yesterday` / `week` / `month` |

**响应字段：** 结构与「新增会员统计」完全一致，按渠道返回 `{ period, count }` 时间序列。

```json
{
    "error": 0,
    "data": {
        "mall": [
            {
                "period": "00:00",
                "count": 0
            },
            "..."
        ],
        "communityBuy": [
            "..."
        ],
        "siteApp": [
            "..."
        ],
        "promoter": [
            "..."
        ]
    }
}
```

---

## 浏览量分析

`GET /statistics/overview/view-data`

**请求参数：**

| 字段     | 类型     | 必传 | 说明                                       |
|--------|--------|----|------------------------------------------|
| period | string | 是  | `today` / `yesterday` / `week` / `month` |

**响应字段：** 每个渠道包含 `viewData`（汇总 PV/UV）和 `detailData`（按时间点的明细）。

| 字段                         | 类型     | 说明                          |
|----------------------------|--------|-----------------------------|
| data.{channel}.viewData.pv | int    | 页面浏览量                       |
| data.{channel}.viewData.uv | int    | 独立访客数                       |
| data.{channel}.detailData  | object | 按时间点的 PV 明细，键为时间如 `"00:00"` |

> `{channel}` 可选值：`mall`（必返）、`communityBuy`、`siteApp`、`promoter`

```json
{
    "error": 0,
    "data": {
        "mall": {
            "viewData": {
                "pv": 126,
                "uv": 45
            },
            "detailData": {
                "00:00": {
                    "pv": 0
                },
                "01:00": {
                    "pv": 3
                },
                "...": "..."
            }
        },
        "communityBuy": {
            "viewData": {
                "pv": 0,
                "uv": 0
            },
            "detailData": {
                "...": "..."
            }
        },
        "siteApp": {
            "viewData": {
                "pv": 0,
                "uv": 0
            },
            "detailData": {
                "...": "..."
            }
        },
        "promoter": {
            "viewData": {
                "pv": 0,
                "uv": 0
            },
            "detailData": {
                "...": "..."
            }
        }
    }
}
```

---

## 商品销量排行榜

`GET /statistics/overview/goods-rank`

**请求参数：**

| 字段     | 类型     | 必传 | 说明                                       |
|--------|--------|----|------------------------------------------|
| period | string | 是  | `today` / `yesterday` / `week` / `month` |

**响应字段：** 按渠道返回商品排行数组。

| 字段                     | 类型     | 说明                     |
|------------------------|--------|------------------------|
| data.{channel}[].title | string | 商品标题                   |
| data.{channel}[].total | int    | 销售数量（promoter 渠道为带货数量） |
| data.{channel}[].price | float  | 销售额                    |

```json
{
    "error": 0,
    "data": {
        "mall": [
            {
                "id": "3326",
                "title": "示例商品名2",
                "total": "8",
                "price": "75.00"
            }
        ],
        "communityBuy": [],
        "promoter": [
            {
                "title": "示例商品名",
                "total": "5",
                "price": "199.00"
            }
        ]
    }
}
```

---

## 会员消费排行榜

`GET /statistics/overview/member-rank`

**请求参数：**

| 字段     | 类型     | 必传 | 说明                                       |
|--------|--------|----|------------------------------------------|
| period | string | 是  | `today` / `yesterday` / `week` / `month` |

**响应字段：** 按渠道返回会员消费排行数组。

| 字段                          | 类型     | 说明       |
|-----------------------------|--------|----------|
| data.mall[].id              | int    | 会员ID     |
| data.mall[].nickname        | string | 会员昵称     |
| data.mall[].order_money     | float  | 消费金额     |
| data.communityBuy[]         | array  | 结构同 mall |
| data.promoter[].id          | int    | 会员ID     |
| data.promoter[].nickname    | string | 会员昵称     |
| data.promoter[].total       | int    | 带货订单数量   |
| data.promoter[].order_money | float  | 带货订单金额   |

```json
{
    "error": 0,
    "data": {
        "mall": [
            {
                "id": "317",
                "nickname": "An",
                "mobile": "15888888888",
                "order_money": 11
            }
        ],
        "communityBuy": [
            {
                "id": "317",
                "nickname": "An",
                "order_money": 11
            }
        ],
        "promoter": [
            {
                "id": "9",
                "nickname": "som",
                "total": "0",
                "order_money": 0
            }
        ]
    }
}
```

---

## 获取商品基础数据统计

`GET /statistics/goods/basic`

**请求参数：**

| 字段         | 类型     | 必传 | 说明                                        |
|------------|--------|----|-------------------------------------------|
| start_time | string | 否  | 统计开始时间，不传默认为30天前，格式 `2026-01-01 00:00:00` |
| end_time   | string | 否  | 统计结束时间，不传默认为前一天，格式 `2026-02-01 00:00:00`  |

**响应字段：**

| 字段                    | 类型  | 说明         |
|-----------------------|-----|------------|
| data.goods_view_count | int | 被浏览商品数量（件） |
| data.cart_goods_count | int | 加购商品数量（件）  |
| data.pay_goods_count  | int | 购买商品数量（件）  |

```json
{
    "error": 0,
    "data": {
        "goods_view_count": 1,
        "cart_goods_count": 2,
        "pay_goods_count": 3
    }
}
```
