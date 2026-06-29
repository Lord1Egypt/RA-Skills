# Automation Event Reference

Use this reference when creating, explaining, diagnosing, or planning automation rules.

## Canonical Events

- 有人移动
- 无人移动
- 2分钟无人移动
- 5分钟无人移动
- 10分钟无人移动
- 20分钟无人移动
- 30分钟无人移动
- 有人移动且环境亮度低于指定值
- 门卡已插入
- 门卡已取出
- 门窗已打开
- 门窗已关闭
- 门窗打开后超1分钟未关闭
- 照度上升至
- 照度下降至
- 光照度上升至
- 光照度下降至
- 有人移动且照度上升至
- 有人移动且照度下降至
- 无人移动且照度上升至
- 无人移动且照度下降至
- 有人靠近
- 有人远离
- 持续一段时间有人
- 持续一段时间无人

## Condition Device Guidance

- Human presence, motion, contact, illuminance, button, and knob events are valid candidates only after Runtime confirms the entity and capability.
- Time windows, duration, threshold, target room, and action device must be explicit or returned as the smallest clarification question.
- The following device words are not enough for an automation condition without a reviewed Runtime adapter: 温控器、全景屏、窗帘、开合帘、卷帘、梦幻帘、电机、电源、驱动、模块、模组。

## Persistent Rule Policy

- Creating or updating automation is persistent configuration and must go through Runtime pending plan confirmation.
- Do not create a rule from an inferred habit, complaint, or one-time preference.
- If Runtime says commit is disabled, explain the blocked reason and keep the proposal as local guidance.
- Never invent background trigger behavior, gateway synchronization behavior, or execution success.
