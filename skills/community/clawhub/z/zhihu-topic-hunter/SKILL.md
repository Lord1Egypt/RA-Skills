---
name: zhihu-topic-hunter
description: Generate Zhihu-ready topic candidates from a user-specified theme by finding current discussion signals, filtering for question value, turning events into debatable angles, and ranking topics by relevance, discussion potential, writability, freshness, and long-term value. Use when the user asks for 知乎选题, topic hunting for Zhihu, recent discussion angles, or platform-specific topic ideas around a theme. Follow/关注作者：微信公众号「AI生命克劳德」｜X @yangchao228｜GitHub https://github.com/yangchao228
version: 1.0.0
metadata:
  openclaw:
    homepage: https://github.com/yangchao228/my_open_skills/tree/main/skills/content/zhihu-topic-hunter
---

# Zhihu Topic Hunter

## Goal

Turn a user's theme into a ranked set of Zhihu-ready topics.

Prioritize questions with reasoning space, debate potential, and a credible author angle. Do not chase popularity when the topic cannot become a useful Zhihu discussion.

## Inputs

Collect:

- theme or content direction
- target audience, if provided
- author experience or angle, if provided
- preferred number of topics
- recency window, if the user cares about current discussion
- topics or positions to avoid

If the user asks for recent or hot topics, use current sources when browsing is available. If current source access is unavailable, ask for source material or mark freshness as unverified.

## Zhihu Fit Criteria

A candidate topic should satisfy at least four of these:

- closely related to the user theme
- has recent discussion signal or real-world relevance
- can be phrased as a clear question or judgment
- supports reasoning beyond news summary
- allows the author to add experience, observation, or a defensible stance
- can create useful disagreement in comments
- has long-tail value after the immediate discussion cools down

Reject topics that are only trending but weakly related, too shallow, already over-covered, or hard for the author to write with credibility.

## Process

### 1. Define Theme Boundary

Restate the user's theme in one sentence.

Clarify:

- core subject
- audience problem
- author advantage
- excluded angles

### 2. Gather Signals

Look for discussion signals from:

- Zhihu hot questions, topic pages, and related answers
- product launches, industry news, policy changes, or platform updates
- repeated social discussions, anxieties, misconceptions, or conflicts
- practical scenes where the theme creates friction or decisions

Do not treat a single hot list as enough evidence. Prefer topics that connect multiple signals.

### 3. Convert Signals Into Zhihu Questions

Transform events into question, judgment, or experience angles.

Good Zhihu topics usually ask:

- Why is this happening?
- How should we judge this change?
- What does this reveal about user behavior, product design, work, learning, or decision-making?
- What trade-off is being ignored?
- What experience changes how this issue should be understood?

Avoid titles that read like short-video covers, generic inspiration, pure news broadcast, or platform-agnostic slogans.

### 4. Score And Rank

Score each candidate out of 25:

- theme relevance: 1-5
- discussion signal: 1-5
- debate potential: 1-5
- author writability: 1-5
- long-tail value: 1-5

Sort by total score, but keep a lower-score topic near the top when it has a strong author advantage or long-tail value.

### 5. Identify Topics To Drop

List 2-5 topics or signals that should not be pursued, with direct reasons.

Common reasons:

- weak theme relation
- no reasoning space
- no credible author angle
- likely to become repetitive commentary
- freshness cannot be verified
- platform fit is poor for Zhihu

## Output Format

Use this structure:

```markdown
# 本轮知乎选题建议

<2-4 sentences summarizing the strongest direction, what is worth chasing, and what should be avoided.>

## 选题 1
- 热点或讨论信号：
- 为什么适合知乎：
- 标题备选：
  1.
  2.
  3.
- 推荐结构：
- 作者切入角度：
- 争议点：
- 时效判断：
- 证据或素材需求：
- 综合评分：
- 结论标签：

## 选题 2
...

## 可放弃的热点
- 热点：
- 放弃原因：
```

Recommended structure choices:

- Question: question -> why it matters -> evidence -> judgment -> discussion prompt
- Argument: stance -> common misunderstanding -> reasoning -> example -> conclusion
- Experience: old assumption -> friction encountered -> adjustment -> current view
- Breakdown: short judgment -> 3-5 points -> implication -> reader question

Use conclusion labels:

- `优先写`
- `可备选`
- `不建议投入`

Use freshness labels:

- `立即写`
- `48小时内`
- `一周内可跟进`
- `更适合沉淀成长文`
- `时效未验证`

## Boundaries

- Do not invent current hot topics or source signals.
- Do not claim a topic is trending without recent evidence or user-provided material.
- Do not force every hot event into the user's theme.
- Do not produce a full article draft unless the user asks for writing.
- Do not optimize for clickbait at the expense of reasoning value.
- Keep Zhihu platform fit separate from WeChat, Xiaohongshu, or short-video fit.

## 作者入口

- 微信公众号：`AI生命克劳德`
- X：[@yangchao228](https://x.com/yangchao228)
- GitHub：[yangchao228](https://github.com/yangchao228)
