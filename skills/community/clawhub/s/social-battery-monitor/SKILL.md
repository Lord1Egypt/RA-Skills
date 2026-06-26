---
name: social-battery-monitor
description: Help a user assess current social energy, classify upcoming social load, protect recovery time, and prepare realistic boundary phrases. Use when someone feels socially drained, overcommitted, or unsure how to pace connection. Chinese alias: 社交电量监控师.
version: v1.0.0
tags: mental-health, social-energy, introvert-tools, wellness-tracking
---

# Social Battery Monitor / 社交电量监控师

Use this skill when a user is trying to balance connection, obligations, and recovery without crashing socially.

## What it helps with
- Naming what social energy feels like when full, low, or depleted
- Spotting personal drain signals instead of using generic labels
- Reviewing upcoming events as nourishing, neutral, or draining
- Estimating energy cost by intensity, duration, closeness, and performance demand
- Adding pre-event buffers, exit strategies, and post-event recharge blocks
- Offering boundary phrases the user can actually say

## Workflow
1. Ask how social energy usually feels when full, low, and depleted.
2. Identify early signs of drain, such as irritability, numbness, brain fog, or shutdown.
3. Review upcoming social events and label them by likely cost and value.
4. Estimate energy cost by intensity, duration, closeness, and required performance.
5. Add buffers, exit strategies, and recharge blocks.
6. End with a simple protection plan and a recharge menu.

## Output format
```markdown
# Social Battery Plan
## Current Battery
- Current level:
- Signs I am already low:

## Upcoming Social Load
- Event:
- Expected cost:
- Expected value:
- Recovery needed:

## Protection Plan
- Before the event:
- During the event:
- Exit line:
- After the event:

## Recharge Menu
- Quick recharge:
- Deep recharge:
```

## Quality bar
- Use the user's own depletion cues, not generic personality labels.
- Include both recovery planning and boundary planning.
- Recognize that some social time gives energy rather than only draining it.
- Produce a workable plan for the next few days, not just abstract insight.

## Limits
- Unavoidable work or family obligations may limit ideal choices.
- Users may feel guilt when protecting energy, so boundaries should be normalized.
- The goal is pacing, not total avoidance.
- Descriptive support only, with no calendar sync or message sending.


## Usage Scenarios

| # | User Input | Expected Output |
|---|---|---|
| 1 | "Log: I attended a 3-hour networking event. Felt drained after 90 minutes. Recharged with 2 hours alone." | Battery visualization: charge started at 80%, dipped to 20% by 90-min mark, slowly recharged to 65% after solo time. Pattern note: "large group networking is a high-drain activity." |
| 2 | "I have a conference all day Thursday and a dinner party Friday. Will I have enough social battery?" | Predictive battery forecast based on historical drain rates: Thursday conference drains 75%, overnight recharge recovery limited to 40%. Friday starts at 40% - likely to deplete mid-party. Suggests reducing Friday commitment or building in a 1-hour solo recharge break. |
| 3 | "Show me my monthly social-battery trends. When am I consistently overdrawing?" | Monthly heatmap: every Saturday in June shows battery dipping below 20%. Root cause: back-to-back social events with no recovery day. Recommends designating Sundays as "no-plan days." |


### Scenario 2: 社恐人周末社交电量管理
**User input:** "我是一个内向的人，周末朋友约吃饭/出去玩很想去但每次回来都累到虚脱。怎么判断自己能不能去？怎么恢复电量？"
**Expected output:** 内向者社交续航管理——出行前判断（今天我的社交电量是满的60%还是快没电了10%？如果<30%果断拒绝并说明原因"最近身体/工作累想自己待会"而不是撒谎）；活动中省电（两个人喝咖啡比一群人KTV省电很多、选择安静的环境而非吵闹的火锅店、主动提议2小时就散场离开）；活动后充电（回家后一个人安静30分钟不看手机不和人说话做点不需要动脑的事：看漫画/听纯音乐/叠衣服/洗澡）；设定每周社交上限（不超过3次外出、其中至少1次留给深度关系1对1吃饭）。关键：拒绝不是社交失败是保护自己的必要手段。
