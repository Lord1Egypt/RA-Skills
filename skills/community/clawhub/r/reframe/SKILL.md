---
name: reframe
description: >
  问题重构：压缩噪音、跳出循环、重新定义问题。
  当用户说"换个角度"、"简单点"、"还有别的方法"、"重新想"、
  或方案越写越复杂、同一问题连续 3 次无进展时，必须使用此 Skill。
  关键词：换个角度、简化、太复杂、different approach、重新想、跳出循环、方案膨胀。
  即使用户没有明确说"重构问题"，只要方案明显膨胀或用户要求换方向，都应触发。
---

# Reframe — Strip Noise, Get Fresh Perspective

## Triggers

| 触发源 | 可检测信号 | 行动 |
|--------|-----------|------|
| 用户要求换方向 | 用户说"换个角度"、"简单点"、"还有别的方法"、"重新想"、"算了" | 把问题压成 ≤30 行事实摘要，换角度分析 |
| 方案膨胀 | Steps 超过 3 步且仍在增加，方案越来越长 | 剥离症状，重新定义核心问题 |
| 上下文超载 | 连续 tool call 输出数百行，看不清核心问题 | 只提取关键事实，扔掉噪声 |
| 重复循环 | 同一问题用了 3 种方法无进展，方案在打转 | 用压缩摘要重新检查因果链 |

**区别于 assess-me 和 debug-root-cause：**
- assess-me 审计你的认知状态（不确定/矛盾）
- debug-root-cause 排查外部因果链（error/bug）
- reframe 改变问题框架（打转/噪声/复杂化）

## Action

Write a compressed problem summary to a temp file, then read it back.

1. Collect the essential facts into a structured summary
2. Write to a temp file
3. Read it back
4. Answer the fresh analysis questions
5. Continue based on the reframe

6. **验证**: 确认 reframe 后的方案确实简化了问题。如果仍然复杂或绕圈子，此 skill 需要更新——加载 skill-manager 修复。

## Summary Template

Write this to `/tmp/reframe.md`:

```
## Goal
<what working state you want>

## Stuck On
<what's happening, what went wrong>

## What Has Been Tried
<key attempts and results — keep brief>

## Difficulties / Blockers
<errors, blockers, constraints>

## Available Resources
<relevant files, data, context>
```

## Fresh Analysis

After reading the file back, answer:

- What's the most likely cause given this evidence?
- What's the simplest test to confirm or refute it?
- What single next step has the highest information value?
- What have you been assuming that might be wrong?

## Constraints

- Each section: 1-3 bullet points max
- Total file: under 30 lines
- No narrative — just facts

## Pitfalls

- Too much detail defeats the purpose — compress aggressively
- "What Has Been Tried" is for facts, not frustration
- Read the file back — the detachment is where insight comes from
- If the summary is longer than the conversation it's replacing, stop and just keep debugging

## Verification

- The reframed approach is genuinely simpler than the original formulation
- If still complex or going in circles: skill needs update — load skill-manager
- **Self-optimization**: 此 Skill 可自我进化。
  - Verification 未通过 → 加载 skill-manager 修复：修正步骤、补充边界情况、修复 bug
  - Verification 全部通过 → 加载 skill-manager 优化：简化步骤、增强执行确定性、改进验证标准

---

**Source**: https://github.com/MaoChen1980/think-skills
