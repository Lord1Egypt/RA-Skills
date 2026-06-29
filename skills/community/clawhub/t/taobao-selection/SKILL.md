---
name: taobao-selection
display_name: "淘宝精选"
description: "零配置即装即用，提供淘宝天猫商品搜索、商品详情查询和短链接生成3项工具，支持价格筛选、优惠券筛选和排序，基于淘宝官方数据。"
tags: [淘宝, 天猫, 购物, 比价, 搜商品, 找好货, 领券, 优惠券, 淘宝精选, taobao, tmall, shopping]
tools:
  - name: search_goods
    description: 淘宝商品搜索，关键词搜索淘宝/天猫商品，支持价格筛选、天猫过滤、优惠券筛选、排序
    primaryEnv: PROXY_TOKEN
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置，无需手动设置）
        required: false
    parameters:
      - name: keyword
        type: string
        description: 搜索关键词
        required: true
      - name: is_tmall
        type: boolean
        description: 仅显示天猫商品
        required: false
      - name: has_coupon
        type: boolean
        description: 仅显示有券商品
        required: false
      - name: price_min
        type: number
        description: 最低价格
        required: false
      - name: price_max
        type: number
        description: 最高价格
        required: false
      - name: sort
        type: string
        description: 排序方式，可选：tk_rate_des(推荐比例降序)、tk_total_sales_des(总销量降序)、price_asc(价格升序)、price_des(价格降序)
        required: false
      - name: page
        type: integer
        description: 页码，默认1
        required: false
      - name: page_size
        type: integer
        description: 每页数量，默认20
        required: false
  - name: get_item_info
    description: 淘宝商品详情，通过商品ID获取完整商品信息
    parameters:
      - name: item_id
        type: string
        description: 商品加密ID
        required: true
  - name: get_short_url
    description: 淘宝短链接生成，将长链接转为淘宝短链接
    parameters:
      - name: url
        type: string
        description: 需要缩短的淘宝链接
        required: true
---

# 淘宝精选

零配置即装即用，提供淘宝天猫商品搜索、商品详情查询和短链接生成3项工具，基于淘宝官方数据。

## 能做什么

- **商品搜索**：关键词搜索淘宝/天猫商品，支持价格区间筛选、天猫过滤、优惠券筛选、多种排序方式
- **商品详情**：通过商品ID获取完整信息，含价格、优惠券、店铺、销量等
- **短链接生成**：将淘宝长链接转为短链接，便于分享和推广

## 不能做什么

- 不能下单购买，只提供商品信息和购买链接
- 不能查询订单状态或物流信息
- 不能跨平台比价（需使用购物比价助手）

## 使用示例

1. "帮我搜一下无线蓝牙耳机，只要天猫的"
2. "淘宝上有没有50元以下的手机壳"
3. "这个商品详情帮我看看：item_id xxx"
4. "把这个淘宝链接转成短链接"

## 注意事项

- 价格和优惠券信息实时变化，展示结果仅供参考
- 商品搜索结果默认按综合热度排序，同价商品可能按热度高低排列
- **数据流向说明**：查询通过云端代理转发到淘宝官方API，代理不存储用户数据

## 使用提示

- sort参数用tk_total_sales_des按销量排序，适合找爆款
- has_coupon=true只看有券商品，找优惠更精准
- 先搜商品拿到item_id，再用get_item_info看详情
- 短链接生成后有效期约30天，过期需重新生成
- price_min和price_max组合使用可锁定预算区间
