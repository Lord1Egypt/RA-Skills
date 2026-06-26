---
name: tongcheng-travel-assistant
description: 零配置即装即用｜酒店机票门票火车票全覆盖｜含预订链接和实时价格｜同程出行一键搞定
tags: [同程旅行, 酒店查询, 机票查询, 火车票查询, 景点门票, 汽车票, 度假线路, 旅行助手, tongcheng, travel]
tools:
  - name: tongcheng_hotel_search
    description: 搜索同程酒店，返回酒店列表含价格、评分、设施和预订链接
    primaryEnv: TONGCHENG_PROXY_URL
    env:
      - name: TONGCHENG_PROXY_URL
        description: 同程代理URL（自动配置，无需手动设置）
        required: false
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置，无需手动设置）
        required: false
    parameters:
      - name: destination
        type: string
        description: 目的地城市，如"上海"、"北京"
        required: true
      - name: extra
        type: string
        description: 补充信息，如"外滩附近 明天入住"或"五星级 含早餐"
        required: false
  - name: tongcheng_flight_search
    description: 搜索同程机票，返回航班列表含价格、时刻和航司信息
    parameters:
      - name: departure
        type: string
        description: 出发城市，如"北京"
        required: true
      - name: destination
        type: string
        description: 目的城市，如"上海"
        required: true
      - name: extra
        type: string
        description: 补充信息，如"明天"、"最早"、"直飞"
        required: false
  - name: tongcheng_train_search
    description: 搜索同程火车票，返回车次列表含余票、票价和坐席信息
    parameters:
      - name: departure
        type: string
        description: 出发城市，如"北京"
        required: true
      - name: destination
        type: string
        description: 目的城市，如"上海"
        required: true
      - name: extra
        type: string
        description: 补充信息，如"明天"、"高铁"、"最早"
        required: false
  - name: tongcheng_bus_search
    description: 搜索同程汽车票，返回班次列表含时间和价格
    parameters:
      - name: departure
        type: string
        description: 出发城市，如"上海"
        required: true
      - name: destination
        type: string
        description: 目的城市，如"苏州"
        required: true
      - name: extra
        type: string
        description: 补充信息，如"明天"、"最早"
        required: false
  - name: tongcheng_scenery_search
    description: 搜索同程景点门票，返回景点列表含价格和评分
    parameters:
      - name: destination
        type: string
        description: 目的地城市，如"上海"
        required: true
      - name: extra
        type: string
        description: 补充信息，如"亲子"、"自然风光"、"5A景区"
        required: false
  - name: tongcheng_traffic_search
    description: 查询同程综合交通方案，对比飞机/火车/汽车等多种出行方式
    parameters:
      - name: departure
        type: string
        description: 出发城市，如"北京"
        required: true
      - name: destination
        type: string
        description: 目的城市，如"上海"
        required: true
      - name: extra
        type: string
        description: 补充信息，如"明天"、"最便宜"、"最快"
        required: false
  - name: tongcheng_travel_search
    description: 搜索同程度假线路，返回旅游套餐/跟团游/自由行产品
    parameters:
      - name: destination
        type: string
        description: 目的地，如"三亚"、"云南"
        required: true
      - name: extra
        type: string
        description: 补充信息，如"5天4晚"、"跟团"、"亲子游"
        required: false
---

# 同程旅行助手

同程旅行全品类搜索技能，覆盖酒店、机票、火车票、汽车票、景点门票、综合交通、度假线路7大品类。数据来自同程旅行程心API，价格真实、信息准确、带预订链接。

## 能做什么

| 功能 | 说明 |
|------|------|
| 🏨 酒店搜索 | 按城市/区域/星级/价格查酒店，返回价格/评分/设施/预订链接 |
| ✈️ 机票搜索 | 查航班价格/时刻/航司，支持直飞/中转/特价筛选 |
| 🚄 火车票搜索 | 查车次余票/票价/坐席，支持高铁/动车/普速 |
| 🚌 汽车票搜索 | 查汽车班次时间和价格 |
| 🎫 景点门票 | 查景点价格/评分，带预订链接 |
| 🚗 综合交通 | 对比飞机/火车/汽车等多种出行方案 |
| 🏖 度假线路 | 搜索跟团游/自由行/旅游套餐 |

## 不能做什么

- 不支持在线下单/支付，预订链接跳转同程APP或网页完成
- 日期请用自然语言描述（如"明天""6月20日"），不支持时间戳格式

## 使用示例

1. "帮我查上海外滩附近的酒店"
2. "北京到上海明天的机票"
3. "广州到深圳的火车票"
4. "上海有什么好玩的景点"
5. "三亚5天4晚跟团游"

## 注意事项

- 价格实时变动，以实际预订页面为准
- 查询通过云端代理转发到同程旅行API，代理不存储用户数据

## 使用提示

- 酒店搜索支持补充区域、星级、设施偏好，如extra="外滩附近 五星级 含早餐"
- 火车票搜索可指定高铁/动车，如extra="明天 高铁"
- 机票搜索可筛选直飞/特价，如extra="明天 直飞"
