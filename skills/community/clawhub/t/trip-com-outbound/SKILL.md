---
display_name: Trip.com携程国际版
description: 出境游一站式助手，支持搜索全球酒店、查询国际机票、购买境外景点门票。数据来自Trip.com（携程国际版），预订链接自动携带联盟推广。面向中国出境游用户。
tools:
  - bash
env:
  - PROXY_URL
  - PROXY_TOKEN
---

# Trip.com携程国际版

## Description

面向中国出境游用户的一站式旅行助手，数据来自 Trip.com（携程国际版）。支持3大核心功能：

1. **海外酒店搜索** — 输入目的地，返回酒店名称、特色、每晚价格、评分和预订链接
2. **国际机票查询** — 输入出发城市和目的地，返回航班号、起降时间、价格和预订链接
3. **境外景点门票** — 输入景点或目的地，返回景点介绍、门票价格和购买链接

所有预订链接通过 Trip.com 联盟推广，支持全球200+国家和地区。

## When to Use

- 用户计划出境旅行，需要搜索海外酒店
- 查询国际航班（机票价格、航班时刻）
- 查找境外景点门票和一日游
- 比价不同平台酒店/机票价格
- 获取目的地旅行建议和攻略

关键词：出境游、海外酒店、国际机票、境外门票、Trip.com、携程国际、出国旅行、酒店预订、机票查询

## Execution

### Step 1: 判断用户需求类型

根据用户问题判断属于哪种模式：
- 涉及酒店/住宿 → `hotel`
- 涉及机票/航班 → `flight`
- 涉及景点/门票/活动 → `attraction`

### Step 2: 执行脚本

```bash
python scripts/trip_com.py <mode> "<查询内容>"
```

**酒店搜索：**
```bash
python scripts/trip_com.py hotel "东京新宿附近性价比高的酒店，预算500-800元"
```

**机票查询：**
```bash
python scripts/trip_com.py flight "7月15日上海飞东京成田的机票"
```

**景点门票：**
```bash
python scripts/trip_com.py attraction "大阪环球影城门票"
```

### Step 3: 展示结果

将 API 返回的结果直接展示给用户，包含：
- 名称/航班号
- 价格信息
- 评分/特色
- Trip.com 预订链接

## Examples

**用户：** "帮我找东京新宿附近的酒店"
```bash
python scripts/trip_com.py hotel "东京新宿附近的酒店，2晚，2人"
```

**用户：** "查一下上海到曼谷的机票"
```bash
python scripts/trip_com.py flight "上海飞曼谷的机票，经济舱"
```

**用户：** "大阪有什么好玩的？门票多少钱？"
```bash
python scripts/trip_com.py attraction "大阪热门景点和门票价格"
```

## Data Flow & Privacy

用户查询通过 HTTPS 发送至安全代理服务器（SCF），代理注入认证令牌后转发至 TripGenie API。代理不存储用户个人数据，所有通信均 HTTPS 加密。返回结果包含 Trip.com 联盟预订链接。

## Notes

- 数据来自 Trip.com（携程国际版），覆盖全球200+国家
- 返回的预订链接为 Trip.com 联盟链接
- 支持中文查询，返回中文结果
- 价格实时查询，以实际预订页面为准
