---
name: sheraton-hotel-booking
display_name: 喜来登酒店查询与预订
description: 零配置即装即用，提供3项喜来登酒店搜索工具，支持品牌酒店查询、详情和套餐优惠搜索，基于飞猪官方数据。
tags: [喜来登, Sheraton, 万豪, 酒店, 预订, 套餐, 酒店搜索, 品牌酒店, 万豪集团, 商务酒店, 度假酒店]
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
        description: 排序方式：rate_desc/price_asc/price_desc/distance_asc
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

# 喜来登酒店查询与预订

搜索万豪集团旗下喜来登酒店，返回真实价格和可预订链接，并支持查询酒店详情和套餐优惠。数据源为飞猪官方商品库万豪专区。

## 能做什么

- **酒店搜索**：按城市搜索喜来登酒店，返回价格、星级、地址、附近地标和预订链接
- **酒店详情**：查询某家喜来登的详细信息，包括周边交通/景点/美食、酒店设施、政策、房型
- **套餐搜索**：搜索含早/连住/门票等打包套餐，通常比单订更优惠

## 不能做什么

- 不支持非喜来登品牌酒店搜索（如需其他万豪品牌请使用对应品牌技能）
- 不支持直接在线下单（提供飞猪预订链接，需在飞猪平台完成预订）
- 不提供酒店实时房态查询（房态以飞猪页面为准）

## 使用示例

1. "上海有什么喜来登酒店"
2. "深圳喜来登800块以内的"
3. "上海虹口喜来登怎么样"（需先搜索获取shid）
4. "三亚喜来登有什么优惠套餐"

## 注意事项

- 触发条件：当用户明确要搜索或预订喜来登酒店时使用
- 价格和可用性以飞猪页面实时数据为准
- **数据流向**：查询通过云端代理转发到飞猪平台，代理不存储用户数据
- 搜索结果自动注入品牌关键词"喜来登"，用户只需提供城市即可

## 使用提示

- 先搜索获取shid，再用shid查询详情，信息更完整
- 套餐通常比单订优惠10-30%，优先查看packages
- max_price筛选可排除高价酒店，配合sort=price_asc找到最优价
- 周末和节假日价格浮动大，建议指定check_in/check_out日期