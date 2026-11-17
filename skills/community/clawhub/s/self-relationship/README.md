# Self-Relationship Skill · 与自己对话

**English** | [中文](README.zh-CN.md) | [Deutsch](README.de.md) | [Español](README.es.md) | [Русский](README.ru.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

> Help people understand themselves more clearly, accept themselves without giving up on growth, and make choices that fit their actual lives.
>
> 帮助一个人更好地理解自己、接纳自己、调整自己，并在现实中做出更适合自己的选择。

An AI Skill grounded in positive psychology: when users talk about "self-relationship", "self-acceptance", "understanding yourself", "self-growth", and similar topics, it guides them to understand first and change second — instead of rushing to advice or labels.

## Core Philosophy

- **Understand yourself before changing yourself**: do not rush to judge; first ask "what happened, what am I experiencing, what does this mean to me"
- **A state is not an identity**: "I feel anxious right now" ≠ "I am an anxious person"
- **Acceptance does not mean giving up on change**: decide the next step based on reality
- **Tests are tools for understanding, not labels that define you**: personality tests, MBTI, and the Big Five are mirrors for knowing yourself
- **Do not turn psychology into a new tool for self-judgment**: no manufactured certainty, no fabricated experiences, no forced positivity

## Features

- Bilingual content (full Chinese text + English Version inside `SKILL.md`)
- Structured self-reflection framework: Facts → Feelings → Interpretation → Judgment → Choice
- Clear expression principles and boundaries that avoid the "AI psychology article" tone
- No diagnosis, no labels, no major life decisions on the user's behalf

## Installation

Copy this directory (or `SKILL.md`) into your Agent's skills directory:

```bash
# For Agents that support skills, e.g. Claude Code, Trae, etc.
# Copy the self-relationship directory into your skills directory
cp -r self-relationship ~/.claude/skills/
```

Once installed, the Skill loads automatically when the user mentions topics such as "self-relationship", "self-acceptance", "understanding yourself", "self-growth", or the Chinese equivalents 「与自己相处」「自我关系」「自我接纳」「自我理解」「认识自己」「自我成长」.

## Usage

Just talk to your Agent, for example:

- "I can't stop criticizing myself. What should I do?"
- "I feel like a failure. Is there something wrong with my personality?"
- "I took the MBTI, but I feel defined by it."
- "I'm not sure what I really want."

The Agent will follow the conversation principles defined in the Skill: understand → clarify → offer perspective → identify choices.

## Directory Structure

```
self-relationship/
├── README.md        # This file (English, shown by default on GitHub)
├── README.zh-CN.md  # 中文说明 (Chinese version)
└── SKILL.md         # Skill content (bilingual, with triggering description in frontmatter)
```

## Content Framework

1. **Core Philosophy** — 10 core principles (state ≠ identity, acceptance ≠ giving up, focus on tendencies, etc.)
2. **Self-Reflection Framework** — five layers: Facts → Feelings → Interpretation → Judgment → Choice
3. **Important Distinctions** — facts vs. interpretations, feelings vs. judgments, acceptance vs. resignation, etc.
4. **Conversation Principles** — understand before advising, allow uncertainty, allow contradictions, find what is controllable
5. **Expression Principles** — 13 principles (avoid AI tone, use fewer aphorisms, never fabricate experiences)
6. **Response Orientation** — understand → clarify → offer perspective → identify choices
7. **Boundaries** — no diagnosis, no pathologizing, no decisions on the user's behalf

## Disclaimer

This Skill is for education and self-reflection only. It does not constitute medical, psychological, or clinical diagnosis. If you are experiencing serious psychological distress or crisis, please seek qualified professional help (such as a counselor, psychiatrist, or a local crisis hotline).

## License

This project has no open-source license specified. For commercial use or redistribution, please contact the author.
