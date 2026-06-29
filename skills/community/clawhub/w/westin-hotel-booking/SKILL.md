---
name: westin-hotel-booking
display_name: 威斯汀酒店查询与预订
description: 搜索万豪集团旗下威斯汀酒店并返回实时价格与预订链接，支持酒店详情查询和套餐优惠搜索，多旅游平台数据直连。
tags: [威斯汀, Westin, 万豪, 酒店预订, hotel]
tools:
  - name: search
    description: 搜索威斯汀酒店，返回价格、星级、地址和预订链接
    parameters:
      - name: dest_name
        type: string
        description: 目的地城市/区域，如"上海""深圳""三亚"
        required: true
      - name: keyword
        type: string
        description: 额外关键词，如"虹桥""度假"
        required: false
      - name: max_price
        type: integer
        description: 最高价格/晚
        required: false
  - name: detail
    description: 查询某家威斯汀酒店的详细信息，包括周边交通、设施、房型等
    parameters:
      - name: shid
        type: string
        description: 酒店ID，从搜索结果获取
        required: false
      - name: hotel_name
        type: string
        description: 酒店名称（备选定位方式）
        required: false
  - name: packages
    description: 搜索威斯汀酒店套餐优惠（含早/连住/门票等打包产品）
    parameters:
      - name: keyword
        type: string
        description: 搜索关键词，如"上海""三亚度假"
        required: false
      - name: hotel_name
        type: string
        description: 酒店名称
        required: false
---

# 威斯汀酒店查询与预订

搜索威斯汀（Westin）酒店，返回真实价格和可预订链接，支持酒店详情和套餐优惠查询。

## 使用场景

- 用户明确要**搜索或预订威斯汀酒店**时使用
- 用户说「帮我找上海的威斯汀」「深圳威斯汀多少钱」等
- 不在用户仅提及品牌名但无搜索意图时触发

## 能做什么

- 搜索威斯汀酒店，返回价格、星级、地址、附近地标和预订链接
- 查询某家威斯汀酒店的详情（周边交通/景点/设施/房型/政策）
- 搜索威斯汀酒店套餐优惠

## 不能做什么

- 不支持非威斯汀酒店搜索
- 不支持直接预订（提供预订链接，用户点击跳转）

## 🚫 绝对禁止

1. **禁止编造任何数据** — 酒店名称、价格、评分、星级必须100%来自脚本输出
2. **禁止添加脚本未返回的信息**
3. **禁止省略预订链接** — 脚本返回的detailUrl必须完整展示

## 使用示例

1. 「上海有什么威斯汀酒店」→ search
2. 「上海800块以内的威斯汀」→ search + max_price
3. 「上海威斯汀怎么样」→ detail
4. 「威斯汀有什么优惠套餐」→ packages

## 注意事项

- 价格实时变动，以实际预订页面为准
- 数据来源为多旅游平台直连，不存储用户数据

## 数据流向

用户输入（城市/日期/关键词）→ 本技能脚本 → 代理服务 → 旅游平台API → 返回结果给用户。查询参数（城市、日期、酒店名）会发送到代理服务以获取实时数据。
