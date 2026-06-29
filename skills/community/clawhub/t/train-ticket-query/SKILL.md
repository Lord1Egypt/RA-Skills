---
name: train-ticket-query
display_name: 铁路12306火车票
description: 零配置即装即用，支持火车票查询含12306实时余票、去火车站交通方式查询和住宿推荐，多旅游平台数据直连。
tags: [火车票, 高铁, 动车, 12306余票, 火车票查询, 订火车票, 火车站交通, 住宿推荐, train, railway, ticket]
tools:
  - name: search_train
    description: 查询火车票/高铁票的余票、价格和时刻表，含12306实时余票信息
    parameters:
      - name: departure
        type: string
        description: 出发城市，如"上海"、"北京"
        required: true
      - name: destination
        type: string
        description: 到达城市，如"北京"、"成都"
        required: true
      - name: dep_date
        type: string
        description: 出发日期，支持"6月15日"、"6-15"、"明天"等灵活格式
        required: false
      - name: seat_class
        type: string
        description: 坐席类型筛选，如二等座、一等座、商务座、硬卧、硬座
        required: false
      - name: transport_no
        type: string
        description: 指定车次号，如G44、D312
        required: false
  - name: query_transport
    description: 查询从出发地到火车站的交通方式，包括打车预估费用和公交地铁路线
    parameters:
      - name: origin
        type: string
        description: 出发地名称，如"浦东机场"、"南京路100号"
        required: true
      - name: train_station
        type: string
        description: 火车站名，如"上海虹桥站"、"北京南站"
        required: true
      - name: city
        type: string
        description: 所在城市，如"上海"、"北京"
        required: true
  - name: recommend_hotel
    description: 用自然语言描述住宿需求，AI智能匹配高分酒店并返回推荐和预订链接
    parameters:
      - name: query
        type: string
        description: 住宿需求描述，如"北京住三里屯附近，400左右"
        required: true
---

# 12306火车票查询与预订 — 火车票查询含12306余票 + 去站交通 + 住宿推荐

> ⚡ **12306实时余票 · 灵活日期输入 · 去站交通 · 住宿推荐 · 零配置即装即用**

---

## 快速入门

**3个开场白示例，复制即用：**
1. "帮我查明天上海到北京的高铁票"
2. "从浦东机场怎么去上海虹桥站"
3. "北京住三里屯附近，400左右的酒店"

---

## 核心能力

1. **火车票查询**：查询高铁/动车/普快车次、票价、时刻表，自动补充12306各座席实时余票
2. **智能日期解析**：支持"6月15日"、"6-15"、"明天"、"后天"等多种日期格式
3. **直达/换乘分组**：直达车次、同站换乘、跨站换乘自动分组展示
4. **12306余票**：自动查询12306各座席余票信息（商务座/一等座/二等座/软卧/硬卧/硬座/无座）
5. **去站交通**：查询到火车站的打车预估费用、地铁/公交路线方案
6. **住宿推荐**：用自然语言描述需求，AI智能匹配酒店

## 能做什么

- 查询国内火车票实时票价和余票
- 按直达/换乘、座席类型、车次号等条件筛选
- 查询去火车站的打车、地铁、公交方案
- 推荐目的地住宿酒店

## 不能做什么

- 不支持直接购买火车票（提供预订链接，用户点击跳转购买）
- 不支持查询已购车票状态或办理退票
- 12306余票依赖12306官网接口，偶发不可用时仅显示票价参考

## 使用示例

1. "帮我查明天上海到北京的高铁票"
2. "广州到深圳6月20号的火车"
3. "从浦东机场怎么去上海虹桥站"
4. "北京住三里屯附近，400左右的酒店"

## 注意事项

- 12306余票信息来自12306官网，实时变动，以实际购票页面为准
- 票价为参考价，实际价格以预订页面为准
- 退票规则：开车前8天以上免手续费 | 48小时~8天扣5% | 24~48小时扣10% | 不足24小时扣20%
- 数据来源为多旅游平台直连，不存储用户数据

## 数据流向

用户输入 → 本技能 → 多旅游平台/12306 → 返回结果给用户
