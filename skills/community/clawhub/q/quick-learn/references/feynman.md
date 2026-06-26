# Feynman Technique & Learning Style / 费曼技巧与学习风格

> **Language note**: Explanatory text matches user's language. Technical terms (State, Props, useEffect) stay in original English. Product names unchanged.

## Feynman Four Steps

1. **Study** → Push today's content (reading/audio/video) → 推送今日内容
2. **Explain** → User explains in their own words → 用户用自己的话解释
3. **Find Gaps** → Identify weak points, supplement → 发现漏洞，回补
4. **Simplify** → User re-explains in plain language/analogies, 3-5 sentences → 通俗语言/类比重新解释，3-5 句

**Agent role**: You're a curious student, NOT a teacher. User explains to YOU. → 你是好奇的学生，不是老师。

## Feynman Prompts by Type

| Type | Prompt (use user's language, keep tech terms in English) |
|---|---|
| **Technical / 技术** | EN: "In plain words, no code — what is it and what problem does it solve?" / ZH: "不用代码，用大白话告诉我它是什么、解决什么问题。" |
| **Process / 流程** | EN: "If you had to explain this process to a layperson, how would you do it?" / ZH: "如果让你把这个流程讲给一个外行听，你会怎么说？" |
| **Theory / 理论** | EN: "How does this theory differ from what you initially thought?" / ZH: "这个理论和你最开始的想法有什么不同？" |
| **System / 系统** | EN: "If you were to compare it to a real-life system, what would it be like?" / ZH: "如果用一个生活中的系统来类比，它像什么？" |
| **Business / 业务** | EN: "If you had 30 seconds in an elevator to explain it to your boss, what would you say?" / ZH: "如果要在电梯里用 30 秒给老板讲清楚，你会怎么说？" |

## Gap Types — How to Guide

| Gap | Manifestation | Guidance (match user's language) |
|---|---|---|
| **Confusing causation / 混淆因果** | Treating correlation as causation | ZH: "A 发生的时候 B 也发生了，一定是 A 导致 B 吗？" |
| **Over-simplification / 过度简化** | Missing preconditions | ZH: "这个规则有没有例外？什么时候不适用？" |
| **Jargon dependency / 术语依赖** | Can't explain without jargon | ZH: "不用「{term}」这个词，你会怎么描述？" |
| **Isolated understanding / 孤立理解** | No connection to known concepts | ZH: "这和你之前学的 xxx 有什么关联？" |

## Quality Scoring

| Stars | Criteria |
|---|---|
| ⭐ (1) | Wrong understanding, fundamental misconceptions / 理解错误，基本误解 |
| ⭐⭐ (2) | Partial, missing key concepts, jargon-heavy / 部分理解，遗漏关键，依赖术语 |
| ⭐⭐⭐ (3) | Correct, no analogies, somewhat technical / 理解正确，无类比，偏技术化 |
| ⭐⭐⭐⭐ (4) | Correct + good analogy, accessible to beginners / 理解正确 + 好类比，新手可懂 |
| ⭐⭐⭐⭐⭐ (5) | Exceptional, creative analogy, 3-5 sentences capture essence / 极佳，创意类比，3-5 句说清本质 |

## Learning Style Adaptation

First 2 days: balanced style. From day 3: auto-adjust based on behavior.

| Detected | Adjustment |
|---|---|
| "This diagram is clear" / 「这个图好清楚」 | More diagrams, Mermaid for complex concepts / 增加图解 |
| Digs into code details / 追问代码细节 | Add code examples, reduce text / 增加代码示例 |
| Excellent analogies / 类比特别好 | Include more analogies, reduce jargon / 更多类比 |
| "Too wordy" / 「太啰嗦」 | Trim to <300 words, key points only / 精简到 300 字以内 |
| "Tell me more" / 「再多讲讲」 | Add deep analysis + extended reading / 增加深度解析 |

**Store in path.json:**
```json
{
  "learning_style": {
    "visual_weight": "high", "code_weight": "medium", "analogy_weight": "high",
    "verbosity": "concise", "confidence": 0.75, "updated_at": "2026-04-08"
  }
}
```
