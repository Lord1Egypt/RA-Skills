---
name: "trip-planner-generator"
description: "Generates structured travel plans for trip websites. Invoke when user wants to create a travel itinerary, plan a trip, or needs help organizing travel details."
---

# Trip Planner Generator

This skill helps generate structured, detailed travel plans through an interactive Q&A process.

## When to Invoke

Invoke this skill when:
- User wants to create a travel plan or itinerary
- User asks for help planning a trip
- User provides travel destination and wants a structured plan
- User mentions "旅行计划", "行程规划", "travel plan", "itinerary"
- User needs to organize travel details into a structured format

## Interactive Q&A Process

**IMPORTANT: Use the AskUserQuestion tool to guide users through the planning process.**

### Phase 1: Basic Information

Ask the following questions using AskUserQuestion:

```
Question 1: 目的地与主题
- Header: "目的地"
- Question: "请问您的旅行目的地是哪里？旅行主题是什么？"
- Options: 
  - "亲子游" (带孩子出行)
  - "情侣/夫妻游" (浪漫之旅)
  - "家庭游" (全家出行)
  - "朋友游" (结伴同行)
- Allow "Other" for custom destination input

Question 2: 出行时间
- Header: "时间"
- Question: "请问您的出行日期和天数？"
- Options:
  - "周末2天" (短途游)
  - "3-4天" (小长假)
  - "5-7天" (长假)
  - "7天以上" (深度游)
- Allow "Other" for specific dates

Question 3: 出行人数
- Header: "人数"
- Question: "请问出行人数和人员构成？"
- Options:
  - "2人" (情侣/夫妻)
  - "2大1小" (三口之家)
  - "2大2小" (四口之家)
  - "4人以上" (多人出行)
- Allow "Other" for specific composition (e.g., "2大1小(10岁)")

Question 4: 交通方式
- Header: "交通"
- Question: "请问您计划使用什么交通方式？"
- Options:
  - "高铁/火车" (铁路出行)
  - "飞机" (航空出行)
  - "自驾" (汽车出行)
  - "混合交通" (多种方式)
```

### Phase 2: Preferences & Budget

```
Question 5: 旅行偏好
- Header: "偏好"
- Question: "您更偏好哪种旅行风格？"
- Options:
  - "轻松休闲" (每天1-2个景点)
  - "深度体验" (慢慢逛，重质量)
  - "打卡观光" (多看几个景点)
  - "冒险探索" (尝试新体验)

Question 6: 预算范围
- Header: "预算"
- Question: "您的预算范围大概是多少？"
- Options:
  - "经济型" (人均1000-2000/天)
  - "舒适型" (人均2000-3000/天)
  - "品质型" (人均3000-5000/天)
  - "奢华型" (人均5000+/天)
```

### Phase 3: Special Requirements

```
Question 7: 特殊需求
- Header: "需求"
- Question: "是否有特殊需求需要考虑？"
- Options:
  - "有老人同行" (需要照顾老人)
  - "有小孩同行" (亲子友好)
  - "有饮食限制" (素食/过敏等)
  - "无特殊需求" (常规安排)
```

## Information Collection Summary

After Q&A, summarize collected information:

```markdown
📋 旅行计划信息确认

- 目的地：[目的地]
- 主题：[旅行主题]
- 日期：[开始日期] - [结束日期]
- 天数：[X天X夜]
- 人数：[人数构成]
- 交通：[交通方式]
- 偏好：[旅行风格]
- 预算：[预算范围]
- 特殊需求：[如有]

确认以上信息后，我将为您生成详细的旅行计划。
```

## Output Format

Generate travel plans in the following structured format:

```markdown
🚄 [旅行标题]

[日期范围] | [天数] | [人数]

[交通信息]

📅 D1 | [日期] [星期] — [当日主题]

住宿： [酒店名称]

时间 行程 备注

[时间] [活动] [详情]
...

💡 [当日贴士]

📅 D2 | ...

💰 预算（[人数]）

项目 费用

[项目名] [金额]
...

🎒 行前清单

🪪 证件
- [物品1]
- [物品2]

👕 衣物
- ...

☀️ 防晒驱蚊
- ...

💊 药品
- ...

📱 电子
- ...

⚠️ 注意事项

🔴 [重要事项]
🏨 [酒店相关]
☀️ [防暑防晒]
🦟 [防蚊措施]
🚶 [行程节奏]
🎒 [车程准备]
🍜 [饮食建议]
💰 [预算提醒]
```

## Required Information Checklist

| Category | Required Fields |
|----------|-----------------|
| Basic | 目的地, 主题, 日期, 天数, 人数 |
| Transport | 出发地, 交通方式, 车次/航班 |
| Daily | 日期, 星期, 主题, 住宿, 时间线 |
| Budget | 交通, 住宿, 门票, 餐饮, 合计 |
| Prepare | 证件, 衣物, 防护, 药品, 电子 |
| Notes | 重要提醒, 注意事项 |

## Tips for Quality Plans

1. **Realistic Timing**
   - Include travel time between locations
   - Add buffer time for delays
   - Consider meal times
   - Account for rest breaks

2. **Child-Friendly** (if applicable)
   - Age-appropriate activities
   - Rest periods
   - Snack breaks
   - Interactive experiences

3. **Practical Details**
   - Booking requirements
   - Opening hours
   - Ticket prices
   - Transportation options

4. **Local Knowledge**
   - Best visiting times
   - Crowd avoidance tips
   - Local food recommendations
   - Free vs paid attractions

## Example Output

```markdown
🚄 广州深圳亲子游

2026.04.29 - 05.04 | 6天5夜 | 一大一小(10岁)

车次 D2431 温州南 08:16 → 广州南 16:51

📅 D1 | 4/29 周二 — 到达广州 大马戏之夜

住宿： 长隆香江酒店

时间 行程 备注

08:16 温州南站出发 D2431 约8.5h
16:51 到达广州南站，打车去长隆
17:30 入住香江酒店休整
19:30 长隆国际大马戏 ⭐ 700元两人套票 约1.5h
21:00 回酒店休息

💡 建议19:00到馆，中间区域最佳。节目：空中飞人+小丑+动物表演。全程不允许拍照录像。

💰 预算（一大一小）

项目 费用

高铁往返 1500-1800元
长隆香江 2晚 2500元（含门票）
长隆大马戏 700元（两人套票）
广州全季 1晚 250-350元
深圳全季 2晚 400-700元
小梅沙海洋世界 200-350元
餐饮（6天） 1500-2000元
市内交通 200-400元
合计 ≈7050-8800元

省钱贴士： 长隆门票含在酒店、大马戏套票省200、深圳湾+北京路免费、提前网购更便宜。

🎒 行前清单

🪪 证件
- 大人身份证
- 小朋友户口本
- 12306提前15天抢票

👕 衣物
- 换洗衣物6天
- 薄外套（晚间空调凉）
- 舒适运动鞋
- 防晒衣 冰袖 遮阳帽
- 玩水备用衣物

☀️ 防晒驱蚊
- 防晒霜SPF50+
- 驱蚊液 + 驱蚊贴
- 便携小风扇
- 湿巾 纸巾

💊 药品
- 晕车药
- 创可贴 + 碘伏棉棒
- 退烧药 + 肠胃药
- 儿童常用药

📱 电子
- 充电器 + 充电宝
- 提前下载动画片/游戏

⚠️ 注意事项

🔴 抢票 五一D2431和返程提前15天 定闹钟
🏨 酒店 长隆香江+全季尽早预订
☀️ 防暑 五月广深30-35度 避开11-15点暴晒
🦟 防蚊 长隆蚊虫多 长袖+驱蚊液
🚶 节奏 每天1-2个景点+午休 不赶场
🎒 车程 去8.5h 返5h 零食动画片备好
🍜 饮食 清淡为主 街边少吃生冷
💰 预算 约7050-8800 备少量现金
```

## Integration with trip-website-generator

The output format is designed to be easily parsed by the trip-website-generator skill. Key mappings:

| Plan Section | Website Page |
|--------------|--------------|
| Daily itinerary (📅) | index.html |
| Preparation checklist (🎒) | prepare.html |
| Important notes (⚠️) | notes.html |
| Budget (💰) | budget.html |

When a user has a generated plan, they can use trip-website-generator to create a beautiful website from it.
