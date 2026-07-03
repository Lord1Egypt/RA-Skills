---
name: sheraton-hotel-booking
display_name: 喜来登酒店查询与预订
description: 搜索万豪集团旗下喜来登酒店，返回实时价格与预订链接，支持酒店详情查询和套餐优惠搜索，基于飞猪官方数据直连。暑期家庭出游首选，全球喜来登酒店查询
version: 1.1.3
tags: [喜来登, 酒店预订, 万豪集团, 商务酒店, 度假酒店]
tools:
  - name: search
    description: 搜索喜来登酒店，返回价格、星级、地址和预订链接
    primaryEnv: PROXY_TOKEN
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置，无需手动设置）
        required: false
    parameters:
      - name: dest_name
        type: string
        description: 目的地城市或区域
        required: true
      - name: check_in
        type: string
        description: 入住日期，格式YYYY-MM-DD
        required: false
      - name: check_out
        type: string
        description: 退房日期，格式YYYY-MM-DD
        required: false
      - name: keyword
        type: string
        description: 额外关键词，如"虹桥""度假"
        required: false
      - name: max_price
        type: integer
        description: 最高价格/晚
        required: false
      - name: sort
        type: string
        description: "排序方式：rate_desc/price_asc/price_desc/distance_asc"
        required: false
      - name: limit
        type: integer
        description: 返回数量，默认10
        required: false
  - name: detail
    description: 查询喜来登酒店详情，包括周边交通、设施、政策和房型
    parameters:
      - name: shid
        type: string
        description: 酒店ID，从搜索结果获取
        required: false
      - name: hotel_name
        type: string
        description: 酒店名称
        required: false
      - name: review_keyword
        type: string
        description: 评价关键词过滤
        required: false
  - name: packages
    description: 搜索喜来登酒店套餐优惠（含早/连住/门票等打包产品）
    parameters:
      - name: keyword
        type: string
        description: 搜索关键词
        required: false
      - name: hotel_name
        type: string
        description: 酒店名称
        required: false
      - name: province_or_city
        type: string
        description: 省份或城市
        required: false
      - name: sort
        type: string
        description: 排序方式
        required: false
      - name: limit
        type: integer
        description: 返回数量，默认10
        required: false
---

# 喜来登酒店查询与预订 — 万豪经典品牌，实时价格一键直达

> 万豪旗下全球分布最广的酒店品牌，搜索酒店/查详情/找套餐三步搞定，飞猪官方数据直连。

🔥 **核心亮点：**
- **品牌专属** — 专注喜来登，搜索结果100%精准匹配
- **飞猪官方数据** — 万豪专区数据源，价格真实可靠
- **详情查询** — 周边交通/景点/设施/房型/政策一网打尽
- **套餐优惠** — 含早/连住/门票等打包产品，通常比单订更优惠
- **零配置** — 免申请Key，装上就能用

## 快速入门

**3个开场白示例，复制即用：**

1. "上海有什么喜来登酒店"
2. "深圳喜来登800块以内的"
3. "三亚喜来登有什么优惠套餐"

## 核心能力

1. **酒店搜索** — 按城市搜索喜来登，返回价格/星级/地址/附近地标/预订链接
2. **酒店详情** — 查询某家喜来登的详细信息（周边交通/景点/美食/设施/房型/政策）
3. **套餐搜索** — 搜索含早/连住/门票等打包优惠套餐
4. **价格筛选** — 支持按最高价格/晚过滤，支持多种排序
5. **预订链接** — 每条结果附带飞猪预订链接，可直接跳转下单
6. **评价过滤** — 支持按评价关键词过滤详情

## 能做什么

- 搜索全国各城市的喜来登酒店
- 查询酒店详细信息（设施/房型/政策/周边交通美食）
- 搜索套餐优惠（含早/连住/门票等打包产品）
- 按价格/距离/评分排序筛选
- 返回实时价格和飞猪预订链接

## 不能做什么

- 不支持非喜来登品牌酒店搜索（其他万豪品牌请用对应品牌技能）
- 不支持直接在线下单（提供飞猪预订链接，需在飞猪平台完成预订）
- 不提供酒店实时房态查询（房态以飞猪页面为准）

## 使用提示

- 先搜索获取shid，再用shid查询详情，信息更完整
- 套餐通常比单订优惠10-30%，优先查看packages
- max_price筛选可排除高价酒店，配合sort=price_asc找到最优价
- 周末和节假日价格浮动大，建议指定check_in/check_out日期
- 价格和可用性以飞猪页面为准

## 🔗 搭配使用

- **酒店聪明订** — 多平台比价，确认最低价
- **威斯汀/丽思卡尔顿** — 同集团不同档次品牌对比
- **景点智能推荐** — 住哪玩哪一站规划

## 数据流向

用户输入 → 本技能 → 云端代理 → 飞猪平台API → 返回结果。代理不存储用户数据。
