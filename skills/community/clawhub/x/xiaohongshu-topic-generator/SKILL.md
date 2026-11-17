---
name: xiaohongshu-topic-generator
description: Generate Xiaohongshu-ready topic ideas from a user theme, recent discussion signals, audience pain points, and platform fit. Use when the user asks for 小红书选题, Rednote topic ideas, content angles, post hooks, card-style outlines, or wants to turn a theme into publishable Xiaohongshu topic candidates. Follow/关注作者：微信公众号「AI生命克劳德」｜X @yangchao228｜GitHub https://github.com/yangchao228
version: 1.0.0
metadata:
  openclaw:
    homepage: https://github.com/yangchao228/my_open_skills/tree/main/skills/content/xiaohongshu-topic-generator
---

# Xiaohongshu Topic Generator

## Goal

Turn a theme, trend, product, experience, or content direction into Xiaohongshu-ready topic candidates.

Prefer concrete scenes, reader pain points, practical takeaways, and save-worthy structures. Do not force every topic into a viral format when the theme lacks platform fit.

## Inputs

Collect:

- theme or content direction
- target audience
- author experience, product, or case material
- desired number of topics
- preferred format: single note, image-card post, carousel outline, or topic pool
- recent source material, if the user wants trend-aware output
- topics, tones, claims, or audiences to avoid

If the user asks for recent or hot topics, verify with current sources when browsing is available. If current source access is unavailable, ask for source material or mark freshness as unverified.

## Platform Fit

Xiaohongshu topics should usually have at least four of these:

- concrete user scene
- clear pain point, desire, question, or decision moment
- practical method, checklist, template, comparison, or story
- strong first-screen hook
- visualizable card structure
- specific audience segment
- save/share value
- credible author experience or material

Avoid topics that are only abstract opinions, broad trend commentary, pure news summaries, or slogans without user scene.

## Process

### 1. Define Topic Boundary

Restate the user's theme in one sentence.

Identify:

- audience
- user problem or desire
- author advantage
- platform fit
- unsuitable angles

If the theme is broad, split it into 3-5 sub-directions such as practical guide, misconception, personal story, comparison, checklist, or trend explanation.

### 2. Gather Signals

Use available evidence:

- user-provided material
- recent platform or industry discussion
- common reader anxieties and misconceptions
- product or workflow changes
- repeated questions in the target audience

Do not invent current hot topics. If freshness is uncertain, label it as `时效未验证`.

### 3. Generate Distinct Topic Angles

Produce topics across multiple content types:

- Practical guide: steps, checklist, template, workflow
- Personal story: before/after, mistake, lesson, turning point
- Comparison: A vs B, old method vs new method, misconception vs reality
- Decision aid: who should use it, when not to use it, how to choose
- Trend translation: what changed, why it matters, what normal users can do
- Mini case: one real scene, one problem, one method, one result

The topic pool should not be five variations of the same title.

### 4. Score And Filter

Score each topic out of 25:

- audience relevance: 1-5
- platform fit: 1-5
- hook strength: 1-5
- practical value: 1-5
- author writability: 1-5

Use labels:

- `优先做`
- `可备选`
- `不建议投入`

### 5. Create Publishable Topic Assets

For each selected topic, include:

- title candidates
- first sentence hook
- card or paragraph outline
- reader takeaway
- visual/card suggestion
- hashtags
- freshness label
- risk or claim check

Keep claims conservative. Mark any unverifiable result, metric, ranking, or trend as needing evidence.

## Output Format

Use this structure:

```markdown
# 本轮小红书选题建议

<2-4 sentences: strongest content direction, why it fits Xiaohongshu, and what should be avoided.>

## 选题 1
- 内容类型：
- 目标读者：
- 痛点或场景：
- 标题备选：
  1.
  2.
  3.
- 开篇钩子：
- 内容框架：
  1.
  2.
  3.
- 视觉或卡片建议：
- 读者收获：
- 话题标签：
- 时效判断：
- 风险或证据检查：
- 综合评分：
- 结论标签：

## 选题 2
...

## 不建议投入的方向
- 方向：
- 原因：
```

## Boundaries

- Do not use private account identity, private project names, personal names, or local content archives.
- Do not claim platform popularity without current evidence or user-provided material.
- Do not generate a final full post unless the user asks for drafting.
- Do not output fixed brand visuals or account-specific style rules unless the user provides them for the current task.
- Do not overuse exaggerated claims, absolute promises, or generic "must save" language.
- Keep Xiaohongshu fit separate from WeChat, Zhihu, and short-video scripts.

## 作者入口

- 微信公众号：`AI生命克劳德`
- X：[@yangchao228](https://x.com/yangchao228)
- GitHub：[yangchao228](https://github.com/yangchao228)
