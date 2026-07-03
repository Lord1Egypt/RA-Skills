---
name: smart-poi
display_name: "景点智能推荐"
description: 6项工具覆盖景点、酒店、交通、美食、火车票、机票，含图片和预订链接，飞猪+高德数据直连，零配置即装即用。
tags: [景点推荐, 门票搜索, 景点酒店, 美食推荐, 交通出行]
tools:
  - name: poi_search
    description: 景点搜索，返回景点名称、等级、地址、图片和购票链接
    primaryEnv: FLIGGY_PROXY_URL
    env:
      - name: FLIGGY_PROXY_URL
        description: 飞猪代理URL（自动配置）
        required: false
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置）
        required: false
    parameters:
      - name: city
        type: string
        description: 城市名，如：深圳、杭州、北京
        required: true
      - name: keyword
        type: string
        description: 景点关键词，如：西湖、长城
        required: false
      - name: category
        type: string
        description: 景点类型，如：自然风光、主题乐园
        required: false
      - name: level
        type: integer
        description: 景区等级1-5（5=5A）
        required: false
  - name: poi_hotel
    description: 搜索景点附近酒店，返回酒店名称、评分、价格、图片和预订链接
    parameters:
      - name: query
        type: string
        description: 搜索需求，如：西湖附近酒店
        required: true
      - name: limit
        type: integer
        description: 返回数量，默认10
        required: false
  - name: poi_transport
    description: 查询到景点的交通方案，含打车、地铁、公交
    parameters:
      - name: origin
        type: string
        description: 出发地，如：上海虹桥站
        required: true
      - name: destination
        type: string
        description: 景点名称，如：故宫
        required: true
      - name: city
        type: string
        description: 城市名，如：北京
        required: true
  - name: poi_food
    description: 搜索景点附近餐厅美食，返回餐厅名称、菜系、评分和人均消费
    parameters:
      - name: location
        type: string
        description: 景点名称，如：故宫
        required: true
      - name: city
        type: string
        description: 城市名，如：北京
        required: true
      - name: keywords
        type: string
        description: 菜系关键词，如：火锅、粤菜
        required: false
      - name: radius
        type: integer
        description: 搜索半径(米)，默认3000
        required: false
      - name: limit
        type: integer
        description: 返回数量，默认10
        required: false
  - name: train_search
    description: 搜索火车票，返回车次、时间、票价和购票链接
    parameters:
      - name: origin
        type: string
        description: 出发城市，如：北京
        required: true
      - name: destination
        type: string
        description: 到达城市，如：杭州
        required: true
      - name: dep_date
        type: string
        description: 出发日期，格式YYYY-MM-DD
        required: false
  - name: flight_search
    description: 搜索机票，返回航班、时间、票价和购票链接
    parameters:
      - name: origin
        type: string
        description: 出发城市，如：北京
        required: true
      - name: destination
        type: string
        description: 到达城市，如：杭州
        required: true
      - name: dep_date
        type: string
        description: 出发日期，格式YYYY-MM-DD
        required: false
      - name: back_date
        type: string
        description: 返程日期，格式YYYY-MM-DD
        required: false
---

# 景点智能推荐 — 景点+酒店+交通+美食+火车票+机票，6个工具玩遍一座城

> 飞猪+高德双数据源，从搜景点到订门票、找酒店、查交通、寻美食、买车票机票，一站闭环。

🔥 **核心亮点：**
- **6项工具全覆盖** — 景点/酒店/交通/美食/火车票/机票，玩遍一座城只需一个技能
- **图片展示** — 景点和酒店搜索结果含图片，所见即所得
- **智能互推** — 每个工具自动推荐关联服务，搜景点→推酒店→推交通
- **预订链接** — 景点门票、火车票、机票均附带预订链接
- **零配置** — 免申请Key，装上就能用

## 快速入门

**3个开场白示例，复制即用：**

1. "杭州有什么好玩的景点"
2. "故宫附近酒店推荐"
3. "从虹桥到外滩怎么走"

## 核心能力

1. **景点搜索** — 按城市/关键词/类型/等级搜索，返回景点图片、门票和购票链接
2. **酒店搜索** — 搜索景点附近酒店，返回酒店图片、价格、评分和预订链接
3. **交通查询** — 查询到景点的打车/地铁/公交方案，含预估费用和时间
4. **美食推荐** — 搜索景点附近餐厅，返回菜系、评分和人均消费
5. **火车票查询** — 搜索火车票，返回车次、时间、票价和购票链接
6. **机票查询** — 搜索机票，返回航班、时间、票价和购票链接

## 能做什么

- 搜索全国各城市的景点门票，含图片、等级、价格
- 搜索景点周边酒店，含图片、评分、价格和预订链接
- 查询到景点的多种交通方案（打车/地铁/公交）
- 搜索景点附近餐厅美食，含菜系、评分和人均
- 查询火车票和机票，支持跨城行程规划

## 不能做什么

- 不支持在线下单（提供预订链接跳转平台完成）
- 仅覆盖国内景点（海外景点暂不支持）
- 交通和美食基于高德地图数据，部分小城市覆盖可能不完整

## 使用提示

- 景点搜索支持按等级筛选（如只看5A景区）
- 美食搜索可按菜系关键词过滤（如"火锅""粤菜"）
- 交通查询需同时提供出发地、目的地和城市名
- 每个工具末尾会提示其他可用服务，方便串联行程
- 价格实时变动，以预订页面为准

## 🔗 搭配使用

- **酒店聪明订** — 多平台比价找到最低价
- **旅行美食指南** — 更深入的城市美食推荐
- **高德地图全能版** — 更详细的路线规划和导航

## 数据流向

用户输入 → 本技能 → 云端代理 → 飞猪/高德API → 返回结果。代理不存储用户数据。
