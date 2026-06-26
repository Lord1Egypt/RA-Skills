---
name: sleep-wind-down-coach
description: Build a realistic evening wind-down plan with a ramp-down timeline, environment checklist, last stimulating action boundary, fallback version, and next-morning feedback prompts. Use when the user stays mentally on until bed and needs a gentler transition from stimulation to sleep.
version: v1.0.0
tags: sleep-health, evening-routine, habit-formation, wellness
---

# Sleep Wind-Down Coach

## Overview

Use this skill to create a clear transition from stimulation to rest. It helps the user define a bedtime target, build a 30, 60, or 90 minute wind-down ladder, reduce late-night stimulation, and keep a fallback version for imperfect nights.

This skill is descriptive wellness guidance only. It is not treatment for insomnia or a clinical sleep disorder.

## Trigger

Use this skill when the user wants to:
- stop working or scrolling right up to bedtime
- build a wind-down routine that starts before bed
- reduce mental activation late at night
- create a fallback routine for already-late evenings
- review how evening choices affect next-morning mood

### Example prompts
- "Help me build a 60 minute wind-down routine"
- "I stay mentally on until bed and sleep feels hard"
- "Make me a fallback bedtime routine for late nights"
- "I want to stop checking work email before sleep"

## Workflow

1. Identify the desired bedtime, current pattern, and drift points.
2. Choose a 30, 60, or 90 minute ramp-down ladder.
3. Sequence calming actions and one clear boundary for stimulating inputs.
4. Add environment adjustments for light, screens, temperature, and noise.
5. Create a fallback version for late nights.
6. Review the next morning how the plan affected sleep onset and mood.

## Inputs

The user can provide any mix of:
- desired bedtime
- actual bedtime or drift pattern
- late-night work or screen habits
- evening stimulation triggers
- hygiene, stretching, reading, or breathing preferences
- home constraints like children, noise, or irregular schedules
- how they usually feel on waking

## Outputs

Return a markdown wind-down plan with:
- sleep target and current pattern
- ramp-down timeline
- environment checklist
- fallback version
- morning feedback questions

## Safety

- Start before bedtime, not at bedtime.
- Include at least one behavioral and one environmental adjustment.
- Keep the routine realistic enough that it does not become a perfection ritual.
- Do not present the skill as diagnosis, medication advice, or treatment.

## Acceptance Criteria

- Return markdown text.
- Include a bedtime target, timeline, and boundary for stimulation.
- Include a fallback version for imperfect nights.
- Include next-morning feedback prompts.


## Usage Scenarios

| # | User Input | Expected Output |
|---|---|---|
| 1 | "I am a night owl who needs to wake up at 6:30 AM. Design a wind-down routine starting from my current 2 AM bedtime." | Progressive plan: Week 1 → screens off at 1 AM, Week 2 → 12:30 AM with 10-min journaling, Week 3 → midnight with chamomile tea ritual, Week 4 → 11:30 PM with 15-min reading. Each step shifts bedtime back 15-30 min. Includes stimulus-control rules (bed = sleep only). |
| 2 | "I followed the routine for 2 weeks but I am still lying awake for 45 minutes. Diagnose." | Sleep latency diagnosis: checking for caffeine after 2 PM, exercise within 3 hours of bed, room temperature (should be 65-68°F), and mental-rumination patterns. Suggests adding a "brain dump" exercise and progressive muscle relaxation audio. |
| 3 | "I travel to Tokyo next week (13-hour time difference). Adapt my wind-down routine for the trip and first 3 days there." | Travel-adapted plan: pre-flight light-exposure schedule shift, in-flight wind-down kit (eye mask, no alcohol, hydration), Day 1-3 Tokyo routine anchored to local 10 PM with morning-light exposure at 7 AM JST. |


### Scenario 2: 睡前刷手机越刷越精神
**User input:** "我每天11点上床但刷手机刷到1-2点才睡，第二天7点又要起。有没有睡前能帮大脑关机的程序？"
**Expected output:** 中国打工人睡前断电程序——第一步：睡前30分钟设手机关机闹钟（用iOS的"睡眠"模式或Android的"勿扰"模式，到点自动变灰屏）；第二步：执行"无蓝光15分钟"（打开暖色台灯+不看任何屏幕+做一件事：1.热水泡脚促进血液循环降低核心体温便于入睡 2.听一个10分钟的播客/有声书用网易云音乐/喜马拉雅搜ASMR睡眠 3.看纸质书不是电子书看任意一页）；第三步：建立"床=睡觉"的条件反射（不在床上玩手机/吃零食/办公，只睡觉和亲密关系）；第四步：如果躺了20分钟没睡着就起床去客厅坐会（打破"努力睡觉但睡不着"的焦虑循环）。关键工具：Sleep Cycle闹钟+褪黑素（偶尔用不要依赖）。
