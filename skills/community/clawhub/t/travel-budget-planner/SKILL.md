---
name: travel-budget-planner
display_name: "旅行预算规划师"
description: "零配置即装即用，智能估算20+目的地旅行预算含机票签证保险，四档风格对比一人一价，支持多目的地性价比排名。"
tags: [旅行预算, 旅游费用, 出行规划, 旅行花费, 旅游攻略, travel budget, trip cost, budget planner, 旅行省钱, 自由行预算]
tools:
  - name: plan
    description: 生成目的地旅行预算规划，含日均消费分解、总预算汇总、不同风格对比和省钱建议
    parameters:
      - name: destination
        type: string
        description: 目的地城市名，如 东京、巴黎、三亚
        required: true
      - name: days
        type: integer
        description: 出行天数，默认5天
        required: false
      - name: style
        type: string
        description: 出行风格：穷游/经济/舒适/豪华，默认经济
        required: false
      - name: people
        type: integer
        description: 出行人数，默认1人
        required: false
  - name: compare
    description: 对比多个目的地的预算，帮你选最划算的目的地
    parameters:
      - name: destinations
        type: string
        description: 目的地列表，逗号分隔，如 东京,首尔,曼谷
        required: true
      - name: days
        type: integer
        description: 出行天数，默认5天
        required: false
      - name: style
        type: string
        description: 出行风格，默认经济
        required: false
---

# 旅行预算规划师

智能估算旅行预算，覆盖20+热门目的地，按穷游/经济/舒适/豪华四档给出日均消费分解，含机票、签证、保险费用，支持多目的地性价比对比。

## 能做什么

- **预算规划**：输入目的地+天数+风格，生成完整预算分解（住宿/餐饮/交通/景点/杂费）
- **机票估算**：自动估算中国出发往返机票费用，按四档风格区分
- **签证保险**：自动计入签证费和旅行保险费用
- **多目的地对比**：同时对比多个目的地的总预算，自动排名性价比
- **省钱建议**：每个目的地附带3条实测省钱技巧

## 不能做什么

- 不能查询实时机票价格，机票为历史均价估算
- 不能替代实际预订，汇率和价格随时波动
- 不含小众目的地，目前覆盖20+热门城市
- 住宿/餐饮价格为当地中等水平参考，淡旺季差异大

## 使用示例

1. "去东京5天大概要多少钱"
2. "两个人去巴厘岛7天舒适游预算"
3. "东京、首尔、曼谷5天哪个最便宜"
4. "三亚穷游4天要多少预算"
5. "巴黎经济游7天多少钱"

## 注意事项

- 所有金额为人民币估算参考，实际费用受季节/汇率/个人消费习惯影响
- 机票价格波动大，建议提前1-2月关注，旺季可能翻倍
- 淡旺季酒店价格可能差2-3倍，出行前再确认
- **数据流向**：所有数据为本地内置，不发送任何外部请求，不收集用户数据

## 使用提示

- 穷游=青旅+街头小吃+公交，经济=经济酒店+普通餐厅+公共交通，舒适=四星+特色餐厅+打车，豪华=五星+米其林+专车
- 东南亚目的地免签/落地签，签证费为0，总预算更划算
- 对比功能帮你在犹豫不决时快速选出性价比最高的目的地
- 日本消费税10%可免税，实际花费可能比估算低5-8%
- 长途旅行(7天+)可以考虑每周住宿费递减（长租折扣）
