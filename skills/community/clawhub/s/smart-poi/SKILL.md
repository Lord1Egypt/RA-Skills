---
name: smart-poi
display_name: "景点智能推荐"
description: 零配置即装即用｜6项工具景点酒店交通美食火车票机票｜含图片和预订链接｜飞猪+高德数据直连
tags: [景点推荐, 门票搜索, 酒店搜索, 美食推荐, 交通出行, 火车票, 机票, 飞猪旅行, 高德地图, POI, travel, attraction]
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

# 景点智能推荐

零配置即装即用的景点旅行技能，6项工具覆盖景点搜索、酒店住宿、交通出行、美食推荐、火车票和机票查询，基于飞猪旅行+高德地图数据直连。

## 能做什么

- **景点搜索**：按城市、关键词、类型、等级搜索景点，返回景点图片、门票价格和购票链接
- **酒店搜索**：搜索景点附近酒店，返回酒店图片、价格、评分和预订链接
- **交通查询**：查询到景点的打车/地铁/公交方案，含预估费用和时间
- **美食推荐**：搜索景点附近餐厅，返回菜系、评分和人均消费
- **火车票查询**：搜索飞猪火车票，返回车次、时间、票价和购票链接
- **机票查询**：搜索飞猪机票，返回航班、时间、票价和购票链接

## 使用示例

1. "杭州西湖附近景点门票"
2. "故宫附近酒店推荐"
3. "从虹桥到外滩怎么走"
4. "西湖附近有什么好吃的"
5. "北京到杭州火车票"
6. "上海到三亚机票"

## 注意事项

- 价格实时变动，以实际预订页面为准
- 景点和酒店搜索通过飞猪结构化数据，含图片展示
- 交通和美食基于高德地图数据，自动定位周边
- 每个工具末尾会提示其他可用服务
