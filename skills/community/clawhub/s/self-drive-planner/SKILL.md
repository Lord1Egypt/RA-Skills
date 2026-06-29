---
name: self-drive-planner
display_name: 自驾出行规划
description: 零配置即装即用，提供3项自驾规划工具，支持路线规划与过路费估算、沿途设施搜索和天气查询，基于高德地图实时数据。
tags: [自驾, 自驾游, 路线规划, 过路费, 油耗, 天气, 充电桩, 加油站, 高德, road trip, 驾驶, 旅行规划]
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

# 自驾出行规划

帮助用户规划自驾出行，提供基于高德地图实时数据的路线规划、费用估算、沿途服务设施和驾驶建议。

## 能做什么

- **路线规划**：输出距离、时间、过路费、油耗/电费估算，每2-3小时自动插入休息建议
- **沿途搜索**：查找加油站、充电桩、服务区、停车场、餐厅等设施
- **天气查询**：查询沿途城市天气，给出暴雨/大雪/大雾等恶劣天气驾驶建议
- **疲劳驾驶提醒**：连续驾驶超过3小时自动提醒休息，夜间驾驶缩短建议间隔

## 不能做什么

- 不提供实时路况导航（请使用高德/百度地图App导航）
- 不提供酒店或住宿预订（可搭配酒店搜索技能使用）
- 油耗估算为标准公式估算，实际油耗受车型和驾驶习惯影响
- 过路费以高德API返回值为准，实际费用可能有差异

## 使用示例

1. "从北京开车到上海怎么走，过路费多少"
2. "南京到杭州自驾，沿途加油站有哪些"
3. "北京到西安沿途天气怎么样"

## 注意事项

- 路线规划和过路费为高德API返回值，实际可能因路况调整
- **数据流向**：查询通过云端代理转发到高德地图API，代理不存储用户数据
- **佣金声明**：本技能路线规划结果不含商业排序，过路费和油耗为高德API返回值和标准公式估算。部分目的地搜索结果可能包含飞猪等平台的预订链接，同价时优先展示佣金较高的平台

## 使用提示

- 超过500km长途建议分两天走，工具会自动分段并建议休息点
- strategy=1（费用优先）可避开部分收费路段，但时间会增加
- 新能源车可关注充电桩搜索，部分高速服务区充电桩较少
- 暴雨/大雪天气建议优先选择高铁而非自驾