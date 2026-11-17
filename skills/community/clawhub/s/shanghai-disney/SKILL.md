---
name: shanghai-disney
display_name: 上海迪士尼游园助手
description: 上海迪士尼乐园游园助手，7项工具覆盖排队预估、路线规划、演出时间、餐厅推荐、门票价格，支持亲子/刺激/均衡多种路线风格。暑期迪士尼攻略、夏日夜场，带娃畅玩童话王国。暑期迪士尼攻略，夏日夜场畅玩指南
changelog: 优化技能描述，提升搜索匹配精度
version: 1.2.2
---
tools:
  - name: disney_schedule
    description: 查询上海迪士尼近期营业时间
    primaryEnv: PROXY_TOKEN
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置，无需手动设置）
        required: false
    parameters:
      - name: days
        type: integer
        description: 查询天数，默认7，最大14
        required: false
  - name: disney_ticket
    description: 查询上海迪士尼门票价格和购票建议
    parameters:
      - name: date
        type: string
        description: 游览日期，格式YYYY-MM-DD
        required: false
      - name: query
        type: string
        description: 筛选关键词
        required: false
  - name: disney_wait_estimate
    description: 查询游乐设施排队预估等待时间（基于历史数据估算，非实时）
    parameters:
      - name: query
        type: string
        description: 筛选条件，如"刺激""室内""亲子"
        required: false
  - name: disney_show_schedule
    description: 查询演出时间表与观赏建议
    parameters:
      - name: query
        type: string
        description: 筛选条件，如"必看""需预约"
        required: false
  - name: disney_smart_next
    description: 基于用户画像和排队预估推荐下一个项目
    parameters:
      - name: query
        type: string
        description: 自然语言描述，如"带5岁孩子""刺激路线"
        required: false
  - name: disney_route
    description: 输出完整一日游路线规划
    parameters:
      - name: query
        type: string
        description: 路线类型，如"亲子一日游""刺激路线"
        required: false
  - name: disney_dining
    description: 园区餐厅推荐
    parameters:
      - name: query
        type: string
        description: 筛选条件，如"梦幻世界餐厅""烧烤""便宜"
        required: false
---

# 上海迪士尼游园助手 — 排队预估+路线规划+演出时间，玩迪士尼不踩坑

> 7项工具覆盖排队预估、智能路线规划、演出时间表、餐厅推荐、门票价格，支持亲子/刺激/均衡多种风格。

🔥 **核心亮点：**
- **排队预估** — 基于历史数据和时段规律估算等待时间，帮助错峰游玩
- **智能路线规划** — 亲子/刺激/均衡三种风格，生成一日游完整路线
- **智能推荐下一个** — 基于同行人年龄、偏好和当前排队，推荐最适合的下一个项目
- **演出+餐厅** — 必看演出时间表+园区餐厅按区域/价格筛选
- **零配置** — 免申请Key，装上就能用

## 快速入门

**3个开场白示例，复制即用：**

1. "带5岁孩子去迪士尼，推荐下路线"
2. "现在排队大概多久"
3. "迪士尼有什么必看演出"

## 核心能力

1. **排队预估** — 根据历史数据和时段规律估算各设施等待时间，帮助错峰
2. **智能路线规划** — 生成亲子/刺激/均衡三种风格的一日游路线
3. **下一个推荐** — 基于用户画像和排队预估，智能推荐下一个项目
4. **演出时间表** — 查询必看演出场次、预约要求、最佳观赏位置
5. **营业时间** — 查询近14天开闭园时间（高德地图API实时数据）
6. **餐厅推荐** — 按区域/菜系/价格筛选园区餐厅
7. **门票价格** — 查询平日/高峰/早鸟票价和尊享卡价格

## 能做什么

- 预估各游乐设施排队等待时间
- 生成个性化一日游路线规划
- 查询演出时间表和观赏建议
- 查询营业时间和门票价格
- 推荐园区餐厅
- 根据同行人情况智能推荐下一个项目

## 不能做什么

- 不能获取实时排队数据（官方未开放API，排队为基于历史规律的预估值）
- 不能在线购票或预约（请通过上海迪士尼官方App购票）
- 不能查询酒店预订信息（可搭配酒店搜索技能使用）
- 排队预估可能与实际等待时间存在偏差，仅供参考

## 使用提示

- 排队预估在开园后2小时（9:30-10:30）和午后（13:00-14:00）偏差最小
- 疯狂动物城和创极速光轮全天排队较长，建议开园首冲或闭园前1小时
- 带小孩优先选"亲子路线"，避免排队超过40分钟的刺激项目
- 雨天室外项目可能关闭，可切换到室内项目（加勒比海盗、小熊维尼等）
- 演出需提前15-30分钟到场

## 🔗 搭配使用

- **酒店智能推荐** — 迪士尼玩完住哪里
- **高德地图全能版** — 导航到迪士尼+查周边
- **旅行美食指南** — 园区吃不够，园外美食补充

## 数据流向

营业时间查询通过云端代理到高德地图API，其余功能为本地内置数据。代理不存储用户数据。
