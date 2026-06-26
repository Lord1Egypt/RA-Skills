# 营销活动查询管理模块

> 通用说明：所有接口响应均包含 `error` 字段（int），`0` = 成功，非 `0` = 失败（此时 `message` 包含错误描述）。下表不再重复列出
`error`。

| 接口      | 方法   | 路由                        | 用途               |
|---------|------|---------------------------|------------------|
| 优惠券概览   | GET  | /sales/coupon/overview    | 各状态优惠券数量汇总       |
| 优惠券列表   | GET  | /sales/coupon/list        | 按名称/状态/领取方式搜索优惠券 |
| 停止发放优惠券 | POST | /sales/coupon/manual-stop | ⚠️ 危险操作，需用户确认    |
| 满额包邮设置  | GET  | /sales/full-free/get      | 获取当前满额包邮规则       |
| 关闭满额包邮  | POST | /sales/full-free/close    | ⚠️ 危险操作，需用户确认    |

---

## 获取优惠券概览

`GET /sales/coupon/overview`

获取优惠券各状态数量汇总。无请求参数。

**响应字段：**

| 字段                | 类型  | 说明       |
|-------------------|-----|----------|
| data.sending      | int | 发放中优惠券数量 |
| data.expired      | int | 已过期优惠券数量 |
| data.out_of_stock | int | 已领完优惠券数量 |
| data.used         | int | 已使用优惠券数量 |
| data.received     | int | 已领取优惠券数量 |

```json
{
    "error": 0,
    "data": {
        "sending": 29,
        "expired": 66,
        "out_of_stock": 6,
        "used": 523,
        "received": 18417
    }
}
```

---

## 获取优惠券列表

`GET /sales/coupon/list`

根据优惠券名称、状态、领取方式搜索优惠券信息。

**请求参数：**

| 字段               | 类型     | 必传 | 说明                                                                   |
|------------------|--------|----|----------------------------------------------------------------------|
| keywords         | string | 否  | 搜索优惠券名称                                                              |
| coupon_sale_type | int    | 否  | 优惠类型：`1` 立减 / `2` 折扣（不传=全部）                                          |
| status           | int    | 否  | 状态：`1` 发放中 / `2` 未发放 / `3` 已领完 / `4` 已过期（不传=全部）                      |
| pick_way         | int    | 否  | 领取方式：`1` 免费领取 / `2` 付费领取 / `3` 链接领取 / `4` 活动领取 / `5` 领券中心 / `6` 直播领取 |
| page             | int    | 否  | 页码（默认 1）                                                             |
| page_size        | int    | 否  | 每页数量（默认 6）                                                           |

**响应字段：**

| 字段                   | 类型     | 说明              |
|----------------------|--------|-----------------|
| total                | int    | 当前条件下的总数量       |
| page                 | int    | 当前页             |
| page_size            | int    | 每页数量            |
| list[].id            | int    | 优惠券ID           |
| list[].coupon_name   | string | 优惠券名称           |
| list[].stock         | int    | 优惠券库存           |
| list[].create_time   | string | 添加时间            |
| list[].content       | string | 优惠内容（如"满1减0.1"） |
| list[].pick_way_text | string | 领取类型文字          |
| list[].status_text   | string | 状态文字            |

```json
{
    "error": 0,
    "total": 1,
    "list": [
        {
            "id": "218",
            "coupon_name": "计次时",
            "coupon_sale_type": "1",
            "stock": "0",
            "create_time": "2025-11-25 15:24:33",
            "content": "满1减0.1",
            "pick_way": 2,
            "pick_way_text": "付费领取",
            "status": "4",
            "status_text": "已过期"
        }
    ],
    "page": 1,
    "page_size": 20
}
```

---

## ⚠️ 手动停止发放优惠券

`POST /sales/coupon/manual-stop`

根据优惠券ID停止发放指定的优惠券。**此操作立即生效，执行前必须向用户确认。**

**请求参数：**

| 字段 | 类型  | 必传 | 说明    |
|----|-----|----|-------|
| id | int | 是  | 优惠券ID |

**响应字段：**

| 字段      | 类型     | 说明                  |
|---------|--------|---------------------|
| message | string | 失败时返回错误信息，如"优惠券不存在" |

```json
{
    "error": 0
}
```

---

## 获取满额包邮设置

`GET /sales/full-free/get`

获取当前满额包邮规则。无请求参数。

**响应字段：**

| 字段                      | 类型     | 说明                                      |
|-------------------------|--------|-----------------------------------------|
| settings.state          | int    | 开启状态：`0` 关闭 / `1` 开启                    |
| settings.is_participate | string | 指定商品：`0` 以下商品不参与 / `1` 以下商品参与 / `2` 不限制 |
| settings.goods_ids      | array  | 指定商品的ID合集                               |
| settings.order_enough   | string | 单笔订单包邮金额                                |
| goods_list[]            | array  | 指定商品的列表                                 |
| goods_list[].id         | int    | 商品ID                                    |
| goods_list[].title      | string | 商品标题                                    |
| goods_list[].price      | float  | 商品价格                                    |
| no_support_areas        | string | 不参加包邮地区（为空则不限制）                         |

```json
{
    "error": 0,
    "settings": {
        "state": 0,
        "is_participate": "0",
        "goods_ids": [
            "9801"
        ],
        "order_enough": "3000.00"
    },
    "goods_list": [
        {
            "id": "9801",
            "title": "xzj多规格",
            "price": "120.00",
            "has_option": "1"
        }
    ],
    "no_support_areas": "北京市，山东省【青岛市(黄岛区)】"
}
```

---

## ⚠️ 关闭满额包邮设置

`POST /sales/full-free/close`

关闭满额包邮设置。无请求参数。**此操作立即生效，执行前必须向用户确认。**

**响应字段：**

| 字段      | 类型     | 说明                     |
|---------|--------|------------------------|
| message | string | 失败时返回错误信息，如"当前已经是关闭状态" |

```json
{
    "error": 0
}
```
