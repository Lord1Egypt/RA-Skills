---
name: zmg-storyboard-generator
description: Create shootable storyboard scripts for ZMGClaw internal demos. Use when the user asks to turn a news topic, campaign concept, documentary idea, short-video idea, public-service message, brand story, or creative outline into a scene-by-scene script with shots, narration, visuals, interview beats, rhythm, and production notes.
version: 1.0.0
user-invocable: true
---

# ZMG分镜脚本生成

## Purpose

Transform an idea into a production-facing storyboard script. Optimize for clarity: directors, editors, reporters, camera operators, and AI video/image tools should understand what to create.

## Inputs

Useful inputs:

- Story premise, news topic, campaign theme, or desired message.
- Duration and format: 15s, 30s, 60s, 3min, vertical, horizontal, TV package, short video, or explainer.
- Audience and platform.
- Style: documentary, warm human story, fast social edit, policy explainer, youth culture, cinematic, official, or investigative.
- Required facts, people, locations, slogans, products, or compliance constraints.

If duration is missing, assume 60-90 seconds for social video and state the assumption.

## Workflow

1. Restate the core story in one sentence.
2. Choose a narrative structure:
   - Hook -> context -> character/problem -> turning point -> resolution -> call to action.
   - Problem -> evidence -> explanation -> solution -> takeaway.
   - Before -> change -> after.
3. Divide the runtime into scenes or beats.
4. For each beat, specify image, shot type, motion, narration/dialogue, sound, text overlay, and material needs.
5. Add interview questions when human subjects are involved.
6. Add AI-generation prompts only when the user wants assets for image/video tools.
7. Check continuity: time, place, causality, character motivation, and tone.

## Output Format

Use this structure by default:

```markdown
## 创作定位
- 片名/暂定标题：
- 核心表达：
- 时长与比例：
- 风格：

## 分镜脚本
| 时间 | 镜号 | 画面/场景 | 景别/运动 | 旁白/对白 | 声音 | 字幕/包装 | 备注 |
|---|---:|---|---|---|---|---|---|

## 采访设计
- 采访对象：
- 关键问题：

## 素材清单
- 实拍：
- 资料：
- AI生成：
- 包装：

## 连贯性检查
- 逻辑：
- 人物：
- 节奏：
- 风险：
```

## Quality Rules

- Make every shot filmable or generatable.
- Avoid vague instructions like "beautiful picture"; name the visible subject, action, environment, composition, and mood.
- Keep narration speakable. Prefer short sentences.
- Do not invent factual claims for news or public-policy content.
- Flag missing source material when the script depends on unprovided facts, quotes, archive footage, or approvals.
