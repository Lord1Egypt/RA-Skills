# 商品查询管理模块

> 通用说明：所有接口响应均包含 `error` 字段（int），`0` = 成功，非 `0` = 失败（此时 `message` 包含错误描述）。下表不再重复列出
`error`。

| 接口   | 方法   | 路由                         | 用途            |
|------|------|----------------------------|---------------|
| 商品列表 | GET  | /goods/list/get            | 按标题/编码/条码搜索商品 |
| 商品详情 | GET  | /goods/detail/get          | 按商品ID获取详情     |
| 下架商品 | POST | /goods/operation/put-store | ⚠️ 危险操作，需用户确认 |

---

## 获取商品列表

`GET /goods/list/get`

根据商品标题、商品编码、商品条码搜索商品信息。

**请求参数：**

| 字段        | 类型     | 必传 | 说明                                                                                                                                |
|-----------|--------|----|-----------------------------------------------------------------------------------------------------------------------------------|
| keywords  | string | 否  | 搜索关键字（可匹配商品标题、编码、条码）                                                                                                              |
| type      | int    | 否  | 商品类型：`0` 实体商品 / `1` 虚拟商品 / `2` 虚拟卡密 / `3` 预约到店 / `5` 计次时商品 / `8` 批发商品 / `9` 智慧药房 / `13` 海淘商品 / `20` 社区团购 / `21` 期刊商品 / `22` 供应链商品 |
| status    | int    | 否  | 商品状态：不传=全部 / `1` 上架 / `2` 售罄 / `3` 下架 / `4` 已删除                                                                                   |
| sort      | string | 否  | 排序字段：`real_sales` 真实销量 / `create_time` 创建时间                                                                                       |
| by        | string | 否  | 排序方式：`asc` 升序 / `desc` 降序                                                                                                         |
| page      | int    | 否  | 页码（默认 1）                                                                                                                          |
| page_size | int    | 否  | 每页数量（默认 6）                                                                                                                        |

**响应字段：**

| 字段                    | 类型     | 说明                  |
|-----------------------|--------|---------------------|
| total                 | int    | 当前条件下的总数量           |
| page                  | int    | 当前页                 |
| page_size             | int    | 每页数量                |
| list[].id             | int    | 商品ID                |
| list[].title          | string | 商品标题                |
| list[].sub_title      | string | 商品副标题               |
| list[].type           | int    | 商品类型                |
| list[].thumb          | string | 商品主图                |
| list[].unit           | string | 单位                  |
| list[].goods_code     | string | 编码                  |
| list[].bar_code       | string | 条码                  |
| list[].stock          | int    | 库存                  |
| list[].stock_warning  | int    | 库存告警值               |
| list[].real_sales     | int    | 真实销量                |
| list[].price          | float  | 商品价格                |
| list[].min_price      | float  | 多规格区间最低价            |
| list[].max_price      | float  | 多规格区间最高价            |
| list[].cost_price     | float  | 成本价                 |
| list[].original_price | float  | 划线价                 |
| list[].has_option     | int    | 是否多规格：`0` 否 / `1` 是 |
| list[].sales          | int    | 销量                  |
| list[].type_text      | string | 商品类型文字              |
| list[].status_text    | string | 商品状态文字              |

```json
{
    "error": 0,
    "total": 1307,
    "list": [
        {
            "id": "9842",
            "title": "按订单-一次性核销完成",
            "sub_title": "",
            "type": "5",
            "thumb": "image/25/2025/11/xxxx.jpg",
            "unit": "件",
            "goods_code": "",
            "bar_code": "",
            "stock": "3316",
            "stock_warning": "20",
            "real_sales": "16",
            "price": "10.00",
            "min_price": "10.00",
            "max_price": "12.00",
            "cost_price": "0.00",
            "original_price": "0.00",
            "has_option": "1",
            "status": "1",
            "sales": "16",
            "type_text": "计次时商品",
            "status_text": "上架"
        }
    ],
    "page": 1,
    "page_size": 6
}
```

---

## 获取商品详情

`GET /goods/detail/get`

根据商品ID获取商品详情。

**请求参数：**

| 字段 | 类型  | 必传 | 说明   |
|----|-----|----|------|
| id | int | 是  | 商品ID |

**响应字段：**

| 字段                   | 类型     | 说明                  |
|----------------------|--------|---------------------|
| goods.id             | int    | 商品ID                |
| goods.type           | int    | 商品类型                |
| goods.status         | int    | 商品状态                |
| goods.is_deleted     | int    | 是否删除：`0` 否 / `1` 是  |
| goods.title          | string | 商品标题                |
| goods.sub_title      | string | 商品副标题               |
| goods.unit           | string | 单位                  |
| goods.goods_code     | string | 编码                  |
| goods.bar_code       | string | 条码                  |
| goods.stock          | int    | 库存                  |
| goods.price          | float  | 商品价格                |
| goods.min_price      | float  | 多规格区间最低价            |
| goods.max_price      | float  | 多规格区间最高价            |
| goods.cost_price     | float  | 成本价                 |
| goods.original_price | float  | 划线价                 |
| goods.has_option     | int    | 是否多规格：`0` 否 / `1` 是 |
| goods.view_count     | int    | 浏览量                 |
| goods.sales          | int    | 销量                  |
| goods.thumb          | string | 主图                  |
| goods.type_text      | string | 商品类型文字              |
| goods.status_text    | string | 商品状态文字              |

```json
{
    "error": 0,
    "goods": {
        "id": "9842",
        "type": "5",
        "status": "1",
        "is_deleted": "0",
        "title": "按订单-一次性核销完成",
        "sub_title": "",
        "price": "10.00",
        "max_price": "12.00",
        "min_price": "10.00",
        "original_price": "0.00",
        "stock": "3316",
        "has_option": "1",
        "view_count": "27",
        "sales": "0",
        "thumb": "https://xxx.jpg",
        "goods_unit": "袋",
        "status_text": "上架",
        "type_text": "计次时商品"
    }
}
```

---

## ⚠️ 下架商品

`POST /goods/operation/put-store`

通过商品ID下架商品。**此操作影响前台展示，执行前必须向用户确认。**

**请求参数：**

| 字段 | 类型  | 必传 | 说明   |
|----|-----|----|------|
| id | int | 是  | 商品ID |

**响应字段：**

| 字段      | 类型     | 说明                 |
|---------|--------|--------------------|
| message | string | 失败时返回错误信息，如"商品不存在" |

```json
{
    "error": 0
}
```
