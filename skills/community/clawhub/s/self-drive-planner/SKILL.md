---
name: self-drive-planner
display_name: 自驾出行规划
description: 自驾出行规划助手，基于高德地图实时数据，支持路线规划与过路费估算、沿途加油站/充电桩/服务区搜索和天气查询，零配置即装即用。
tags: [自驾游, 路线规划, 过路费估算, 沿途加油站, 充电桩搜索]
tools:
  - name: plan_route
    description: 规划自驾路线，输出距离、时间、过路费、油耗估算和分段建议
    primaryEnv: PROXY_TOKEN
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置，无需手动设置）
        required: false
    parameters:
      - name: origin
        type: string
        description: 出发地（城市名或地名）
        required: true
      - name: destination
        type: string
        description: 目的地（城市名或地名）
        required: true
      - name: waypoints
        type: string
        description: 途经点，逗号分隔
        required: false
      - name: strategy
        type: integer
        description: 策略：0=速度优先，1=费用优先，2=距离优先
        required: false
  - name: search_poi_along
    description: 搜索沿途或指定位置周边的服务设施（加油站/充电桩/服务区/停车场/餐厅）
    parameters:
      - name: location
        type: string
        description: 位置（地名或城市名）
        required: true
      - name: poi_type
        type: string
        description: 设施类型：gas_station/charging/service_area/parking/restaurant
        required: true
      - name: radius
        type: integer
        description: 搜索半径（米），默认5000
        required: false
  - name: trip_weather
    description: 查询出发地、目的地及沿途城市的天气，给出驾驶天气建议
    parameters:
      - name: cities
        type: string
        description: 城市名列表，逗号分隔
        required: true
---

# 自驾出行规划 — 路线+过路费+油耗+沿途设施+天气，一站式规划

> 基于高德地图实时数据，智能规划自驾路线，自动估算过路费和油耗，搜索沿途加油站/充电桩/服务区。

🔥 **核心亮点：**
- **智能路线规划** — 速度/费用/距离三种策略，自动分段并插入休息建议
- **过路费+油耗估算** — 提前知道全程花费，方便预算规划
- **沿途设施搜索** — 加油站/充电桩/服务区/停车场/餐厅一键查找
- **天气预警** — 沿途城市天气查询，暴雨/大雪/大雾驾驶建议
- **零配置** — 装上就能用

## 快速入门

**3个开场白示例，复制即用：**

1. "从北京开车到上海怎么走，过路费多少"
2. "南京到杭州自驾，沿途加油站有哪些"
3. "北京到西安沿途天气怎么样"

## 核心能力

1. **路线规划** — 输出距离、时间、过路费、油耗/电费估算
2. **分段建议** — 每2-3小时自动插入休息建议，长途自动分段
3. **沿途搜索** — 加油站/充电桩/服务区/停车场/餐厅
4. **天气查询** — 沿途城市天气+恶劣天气驾驶建议
5. **疲劳提醒** — 连续驾驶超3小时自动提醒，夜间缩短间隔
6. **策略选择** — 速度优先/费用优先/距离优先三种模式

## 能做什么

- 规划自驾路线，输出距离、时间、过路费和油耗估算
- 搜索沿途加油站、充电桩、服务区、停车场、餐厅
- 查询沿途城市天气，给出驾驶天气建议
- 长途自驾自动分段并建议休息点

## 不能做什么

- 不提供实时路况导航（请使用高德/百度地图App）
- 不提供酒店住宿预订（可搭配酒店搜索技能使用）
- 油耗为标准公式估算，实际受车型和驾驶习惯影响

## 使用提示

- 超过500km长途建议分两天走，工具会自动分段并建议休息点
- strategy=1（费用优先）可避开部分收费路段，但时间会增加
- 新能源车重点关注充电桩搜索，部分高速服务区充电桩较少
- 暴雨/大雪天气建议优先选择高铁而非自驾
- 过路费和油耗为估算参考，实际以导航为准

## 🔗 搭配使用

- **高德地图全能版** — 更全面的地图和导航能力
- **旅行预算规划师** — 自驾旅行的整体预算规划
- **天气查询** — 目的地详细天气预报

## 数据流向

路线规划通过云端代理转发到高德地图API，代理服务不存储用户数据。
