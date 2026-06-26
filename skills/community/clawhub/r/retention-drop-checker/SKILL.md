---
name: retention-drop-checker
description: Diagnose why short-video retention drops and suggest practical fixes. Use when views start but audience leaves early.
---

# Retention Drop Checker

## Skill Card

- **Category:** Performance Diagnostics
- **Core problem:** Videos get impressions but lose viewers too early.
- **Best for:** Teams improving first-seconds retention and completion rate.
- **Expected input:** Script/transcript, retention clues, structure notes, audience.
- **Expected output:** Drop diagnosis + fix actions + next script skeleton.

## 先交互，再分析

开始时先确认：
1. 你现在有的是什么？
   - retention 曲线截图
   - 平台导出的 retention 数据
   - 脚本/逐字稿
   - 你自己的结构笔记
2. 你更想查的是：
   - 前 3 秒掉点
   - 中段流失
   - CTA 前流失
   - 完播率偏低
3. 你们平时有没有自己的 retention 分段逻辑？
4. 如果没有统一逻辑，是否接受我先给一个推荐诊断框架？

## Python analysis guidance

如果用户提供结构化 retention 数据（CSV / export / timestamped segments）：
- 生成 Python 分析脚本
- 先解释分析逻辑
- 再输出 drop map / segment diagnosis
- 最后返回可复用脚本

如果用户没有结构化数据：
- 先按脚本结构和可见线索做定性诊断
- 明确说明这是 heuristic analysis
- 不要伪装成精确 retention model

## Workflow

1. Clarify the available evidence and diagnosis goal.
2. Segment the video structure.
3. Identify likely drop moments.
4. Diagnose root causes.
5. Recommend practical fixes.
6. Provide next-version structure.
7. If structured data exists, return Python analysis script.

## Output format

1. Drop diagnosis map
2. Cause list
3. Fix actions
4. Next script skeleton
5. Optional Python script (when structured data exists)

## Quality and safety rules

- Tie diagnosis to specific segments.
- Keep fixes concrete and testable.
- Preserve core product story.
- Distinguish heuristic diagnosis from data-backed diagnosis.

## License

Copyright (c) 2026 **Razestar**.

This skill is provided under **CC BY-NC-SA 4.0** for non-commercial use.
You may reuse and adapt it with attribution to Razestar, and share derivatives
under the same license.

Commercial use requires a separate paid commercial license from **Razestar**.
No trademark rights are granted.
