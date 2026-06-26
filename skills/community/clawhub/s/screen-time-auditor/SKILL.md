---
name: screen-time-auditor
description: Help a user manually audit screen habits, find trigger loops, identify the worst leakage zones, and run one week of realistic reduction experiments. Use when someone feels trapped by scrolling, checking, or rebound screen behavior. Chinese alias: 屏幕时间审计师.
version: v1.0.0
tags: digital-wellness, screen-time, productivity, habit-analysis
---

# Screen Time Auditor / 屏幕时间审计师

Use this skill when a user knows screen time feels too high but cannot yet see where the time goes, why it happens, or how to reduce it without a rebound.

## What it helps with
- Estimating screen time by device, app, and time band
- Separating functional use from unconscious drift and emotional escape
- Mapping trigger loops such as boredom, transitions, fatigue, procrastination, or social comparison
- Identifying the worst leakage zones, such as late-night scrolling or fragmented checking
- Recommending friction changes, replacement rituals, and protected phone-free windows
- Converting the audit into one realistic week of experiments

## Workflow
1. Ask the user to estimate or manually review screen time by device, app, and time band.
2. Separate functional screen use from drift and emotional escape.
3. Map the trigger loops behind the behavior.
4. Identify the worst leakage zones.
5. Recommend friction changes, replacement rituals, and phone-free windows.
6. Turn the audit into a one-week experiment.

## Output format
```markdown
# Screen Time Audit
## Current Pattern
- Main devices:
- Main drain apps or behaviors:
- Worst time bands:

## Trigger Map
- Trigger:
- Typical behavior:
- What it gives me:
- Better substitute:

## Reduction Plan
- Friction to add:
- Phone-free zone:
- Replacement action:
- Weekly target:
```

## Quality bar
- Move beyond shame into a specific pattern diagnosis.
- Distinguish useful use from compulsive drift.
- Include at least one friction change and one replacement behavior.
- Target one or two problem zones first instead of demanding perfection.

## Limits
- Some users need screens for work, caregiving, or study, so total reduction is not the right metric.
- Over-restriction can backfire if boredom or emotional need is ignored.
- Shared household devices can reduce data accuracy.
- Manual audit only, with no telemetry or app-blocker integration.


## Usage Scenarios

| # | User Input | Expected Output |
|---|---|---|
| 1 | "Audit my iPhone screen time report from the past 4 weeks." | Pattern breakdown: 3.2 hrs/day social media (peak at 10 PM-12 AM), 1.5 hrs gaming. Flags "doomscrolling" pattern: TikTok sessions over 30 min have 0 intentional opens. Attention-leak map. |
| 2 | "I want to cut my daily screen time from 5.5 hours to 3 hours. Design a graduated reduction plan." | 4-week plan: Week 1 → 4.5 hrs (remove 1 hr of bedtime scrolling), Week 2 → 4 hrs (app limits on top 3 apps), Week 3 → 3.5 hrs (grayscale mode during work hours), Week 4 → 3 hrs (replace gaming with offline hobby blocks). |
| 3 | "Compare my screen time with last quarter. Am I improving?" | Trend analysis: total screen time -18%, social media -32%, productivity apps +14%. Positive trajectory confirmed. Suggests maintaining current limits and adding focus-mode refinement. |


### Scenario 2: 刷抖音停不下来怎么办
**User input:** "我每天刷抖音2-3个小时，工作没效率晚上还熬夜。想戒但总是控制不住。怎么办？"
**Expected output:** 手机过度使用干预方案——第一步：量化基线（用手机系统自带的屏幕使用时间统计连续监测1周，知道平均每天用多久、什么时候用得多、什么App用最久）；第二步：环境设计（睡前1小时手机放在客厅不要带进卧室、抖音卸载重装但不开WiFi下载时不刷、设置抖音青少年模式强制15分钟后提醒）；第三步：替代行为（想刷手机时立刻起身倒杯水、做3个俯卧撑、看一页纸质书——任何打破条件反射的行为）；第四步：使用iPhone的"停用时间"功能或Android的"专注模式"（白天工作时间直接锁定娱乐App）。关键工具：Forest App（种树专注）+iOS Screen Time。
