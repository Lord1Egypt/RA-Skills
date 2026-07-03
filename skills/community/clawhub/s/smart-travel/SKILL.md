---
name: smart-travel
display_name: "全能旅行助手"
description: 一站式AI旅行助手，16项工具覆盖机票/酒店/火车票/景点/美食/天气全场景。飞猪+高德+同程+途牛多源数据直连，零配置即装即用。
tags: [旅行, 行程规划, 机票, 酒店, 火车票, 景点门票, 比价, 美食, 天气, 万豪, 打车]
tools:
  - name: travel_plan
    description: 智能行程规划，推荐行程方案
    primaryEnv: FLIGGY_PROXY_URL
    env:
      - name: FLIGGY_PROXY_URL
        description: 飞猪代理URL（自动配置）
        required: false
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置）
        required: false
    parameters:
      - name: params
        type: string
        description: 自然语言查询，如"3天2晚上海游"
        required: true
  - name: search_train
    description: 搜索火车票/高铁票
    parameters:
      - name: params
        type: string
        description: 自然语言查询，如"北京到上海明天的火车"
        required: true
  - name: search_flight
    description: 搜索国内航班机票
    parameters:
      - name: params
        type: string
        description: 自然语言查询，如"上海到三亚7月1号机票"
        required: true
  - name: search_hotel
    description: 搜索酒店，返回实时价格、星级、品牌、地址和预订链接
    parameters:
      - name: params
        type: string
        description: 自然语言查询，如"杭州西湖附近酒店"
        required: true
  - name: search_poi
    description: 搜索景点门票
    parameters:
      - name: params
        type: string
        description: 自然语言查询，如"上海迪士尼门票"
        required: true
  - name: search_marriott_hotel
    description: 搜索万豪集团酒店
    parameters:
      - name: params
        type: string
        description: 自然语言查询，如"上海万豪酒店"
        required: true
  - name: get_marriott_hotel_info
    description: 获取万豪酒店详情
    parameters:
      - name: params
        type: string
        description: 酒店名称或关键词
        required: true
  - name: search_marriott_package
    description: 搜索万豪酒店套餐
    parameters:
      - name: params
        type: string
        description: 自然语言查询，如"万豪含早套餐"
        required: true
  - name: search_food
    description: 搜索附近美食推荐
    parameters:
      - name: params
        type: string
        description: 自然语言查询，如"外滩附近美食"
        required: true
  - name: search_transport
    description: 查询市内交通方案
    parameters:
      - name: params
        type: string
        description: 自然语言查询，如"浦东机场到外滩（上海）"
        required: true
  - name: search_weather
    description: 查询目的地天气预报
    parameters:
      - name: params
        type: string
        description: 自然语言查询，如"三亚天气预报"
        required: true
  - name: take_taxi_link
    description: 生成高德一键打车链接
    parameters:
      - name: params
        type: string
        description: 自然语言查询，如"从浦东机场到外滩（上海）"
        required: true
  - name: bus_search
    description: 搜索长途汽车票和城际大巴班次
    parameters:
      - name: params
        type: string
        description: 自然语言查询，如"上海到苏州明天的汽车票"
        required: true
  - name: travel_search
    description: 搜索跟团游和自由行旅游产品
    parameters:
      - name: params
        type: string
        description: 自然语言查询，如"三亚跟团游"或"日本亲子游"
        required: true
  - name: cruise_search
    description: 搜索邮轮旅游产品，支持按航线查询
    parameters:
      - name: params
        type: string
        description: 自然语言查询，如"日本邮轮"或"东南亚航线"
        required: true
  - name: holiday_search
    description: 搜索度假旅游线路产品，支持按关键词和出发城市筛选
    parameters:
      - name: params
        type: string
        description: 自然语言查询，如"三亚度假"或"从上海出发去日本"
        required: true
---

# 全能旅行助手

> 你的AI旅行搭子 — 一句话搞定机酒火车景点美食，16项工具全包，装了就用。

🔥 **为什么选我？**
- **全** — 16项工具覆盖机票、酒店、火车票、景点门票、美食、天气、打车、万豪、汽车票、跟团游、邮轮、度假线路、行程规划、市内交通，一个技能替代十个
- **真** — 飞猪+高德+同程+途牛多平台实时数据，不是AI编的，价格都是真的
- **快** — 零配置，装了就能用，不用装CLI，不用配Key

🎯 **试试这样说：**
1. "帮我规划3天2晚的上海游"
2. "查明天北京到上海的机票"
3. "三亚亚特兰蒂斯酒店多少钱"

## 能做什么

- **行程规划**：智能推荐行程方案，涵盖景点+酒店+交通
- **火车票搜索**：查车次、票价、余票
- **机票搜索**：查航班价格、时刻、航司
- **酒店搜索**：按城市/区域/品牌查酒店，返回价格、星级、品牌、地址、地标、装修时间、预订链接和酒店图片
- **景点门票**：查景点门票价格和预订链接
- **万豪酒店**：搜索万豪集团旗下酒店详情和套餐
- **美食推荐**：搜索附近美食，含评分和距离
- **市内交通**：查询公交/地铁/驾车路线
- **天气查询**：查询目的地天气预报
- **打车链接**：生成高德一键打车链接
- **汽车票搜索**：查长途汽车票和城际大巴班次，显示发车时间、票价和余票
- **跟团游搜索**：搜跟团游和自由行产品，显示天数、价格和出发日期
- **邮轮搜索**：按港口和月份搜航线，显示航线、天数、价格和出发日期
- **度假线路**：按关键词和出发城市搜度假产品，显示亮点、天数和价格

## 使用示例

1. "帮我规划一个3天2晚的上海游"
2. "查北京到上海明天的火车票"
3. "三亚天气预报"
4. "上海万豪酒店有什么套餐"
5. "从浦东机场到外滩怎么走"
6. "上海到苏州明天的汽车票"
7. "日本亲子跟团游"
8. "日本邮轮航线"
9. "从上海出发去三亚度假"

## 注意事项

- 价格实时变动，以实际预订页面为准
- 查询通过云端代理转发到飞猪旅行+高德地图+同程旅行+途牛旅游API，代理不存储用户数据

## 🔗 专项比价工具

想要更精准的跨平台最低价对比？试试这些专项工具：
- **酒店比价** — 飞猪+途牛+同程+美团+RG 5源并发比价
- **机票比价** — 飞猪+途牛+同程+美团+RG 5平台直飞航班对比
- **景点门票比价** — 美团+飞猪+途牛 3平台门票最低价