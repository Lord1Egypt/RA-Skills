---
name: training-quiz
description: >
  Interactive product knowledge training and quiz system for retail staff.
  Tests employees on product specs, store policies, sales techniques, and FAQs
  through flashcards, multiple choice, and scenario-based questions.
  Tracks completion and scores per employee.
  Use when: a staff member wants to learn about products, take a quiz,
  test their knowledge, onboard to a new product line, or practice sales scripts.
  Triggers on: 考我, 测试, 培训, 学习产品, 练习, quiz me, test my knowledge,
  training, flashcard, product knowledge test, 我想学, 帮我复习, 新品学习.
metadata:
  openclaw:
    emoji: 🎓
---

# Training Quiz

## Overview

This skill turns the product knowledge base into an interactive learning system for staff.
It adapts difficulty, tracks progress, and celebrates improvement — making training
feel less like a chore and more like a game.

**Depends on:** `products[]` + `policy_entries[]` + `faqs[]` in knowledge base.

---

## Quiz Modes

| Mode | Trigger | Format | Best For |
|------|---------|--------|---------|
| Flashcard | "考我产品知识" | Q → reveal A | Quick daily review |
| Multiple Choice | "选择题模式" | Q + 4 options | Structured testing |
| Scenario | "情景练习" | Role-play customer scenario | Sales skill practice |
| Policy Drill | "考我政策" | Policy rule questions | Compliance training |
| New Product | "考我新品" | Focus on recently added items | New arrival onboarding |

Default mode: **Flashcard** (lowest friction).

---

## Session Flow

### Start
1. Greet the learner by name (if known from staff config)
2. Ask or confirm: mode, topic focus, number of questions (default 10)
3. Begin immediately — don't over-explain

### During Quiz
- Ask one question at a time
- Wait for answer before revealing correct response
- On correct: brief positive reinforcement ("✅ 答对了！") + optional fun fact
- On incorrect: show correct answer + brief explanation (2 sentences max)
- Track: correct / total, running accuracy %

### End of Session
```
🎓 本次练习结束！

结果：[correct]/[total] — [score]%
[评级: 优秀 ≥90% | 良好 70-89% | 需加强 <70%]

[If score < 70%]: 建议重点复习：[list weak categories]
[If score ≥ 90%]: 太棒了！你已经达到优秀水平 🏆

下次想练习什么？
```

**Reference:** [question-bank.md](references/question-bank.md) — question templates by type.

---

## Question Generation

Questions are auto-generated from the knowledge base. No manual authoring needed.

### From products:
- "这款[产品名]的[属性]是什么？" → answer from `description`/`variants`
- "下面哪个是[产品名]的正确价格？" → MCQ using real + nearby prices as distractors
- "[顾客描述] → 你会推荐哪款产品？" → scenario from `suitable_for`

### From policies:
- "退货政策中，[条件]，顾客可以享受什么？"
- "以下哪种情况不在退货政策范围内？" → MCQ with real exceptions as options

### From FAQs:
- Use `question` field directly
- Shuffle real FAQ answers as MCQ distractors

**Script:** `scripts/generate_questions.py` — generates a quiz set from the KB.

---

## Progress Tracking

Store per-employee progress in agent memory under `training_progress.<staff_id>`:

```json
{
  "staff_id": "zhang_san",
  "sessions": [
    {
      "date": "2024-07-15",
      "mode": "flashcard",
      "score": 8,
      "total": 10,
      "accuracy": 80,
      "weak_categories": ["policy", "pricing"]
    }
  ],
  "cumulative_accuracy": 82,
  "badges": ["first_quiz", "7day_streak", "policy_master"]
}
```

Report progress to manager on request:
> "张三本月完成 5 次练习，平均正确率 82%，政策类题目需加强。"

---

## Gamification

Keep it motivating:

| Achievement | Trigger |
|-------------|---------|
| 🌟 首次完成 | First quiz session |
| 🔥 连续挑战 | 3+ consecutive days |
| 📚 政策达人 | 5 policy quizzes with ≥90% |
| 🏆 产品专家 | Overall accuracy ≥90% over 10+ sessions |
| ⚡ 闪电手 | 10 consecutive correct answers |

Announce badges immediately when earned. Keep it brief and genuine.
