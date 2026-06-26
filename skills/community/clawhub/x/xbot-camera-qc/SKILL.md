---
name: xbot-camera-qc-pro
slug: xbot-camera-qc-pro  # 唯一标识，小写+短横线
version: 1.0.0           # 语义化版本
description: Professional visual inspection for xbot.coffee Lite, detecting drink volume, screen, table, robotic arm, dirt, environment and pests. Output structured English JSON for API automation.
tags: coffee, qc, vision, api, xbot
author: YourName
homepage: https://github.com/yourname/xbot-camera-qc-pro
---

# xbot.coffee Lite Camera QC (API Version)

## Detection Rules
1. drink_status: normal / insufficient / overflow / foreign_object / spill_outside
2. screen_status: normal / off
3. table_clean: normal / dirty
4. robot_arm: normal / abnormal
5. equipment_dirty: normal / dirty
6. environment_clean: normal / messy
7. pest: none / found

## Output JSON
{
"drink_status": "...",
"screen_status": "...",
"table_clean": "...",
"robot_arm": "...",
"equipment_dirty": "...",
"environment_clean": "...",
"pest": "...",
"has_anomaly": true/false,
"alert_msg": "..."
}