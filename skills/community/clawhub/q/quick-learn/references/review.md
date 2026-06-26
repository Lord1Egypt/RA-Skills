# Forgetting Curve Review / 遗忘曲线复习

> Review cards match user's language. Technical concept names stay in English (e.g. "React Hooks" not translated).

## Review Nodes

| Review | Interval | Retention After |
|---|---|---|
| 1st / 第 1 次 | 1 day later | ~90% |
| 2nd / 第 2 次 | 3 days later | ~95% |
| 3rd / 第 3 次 | 7 days later | ~98% |

## Architecture

Review cron uses `sessionTarget: "isolated"` — ONLY pushes the card. Main session agent handles correct/wrong judgment and chain scheduling.

## Card Template (match user's language)

```
🔄 Review Reminder | {topic} · Day {n} Review
📌 One-line summary: {core}
🧠 Quick self-test (30 sec): {1 brief question}
💡 Hint: {small hint}
Reply with your answer / 回复你的答案 👇
```

## Answer Evaluation

**Correct / 答对:**
```
✅ Nice — you've got it! "{concept}" is locked in.
Quick ref: {1-sentence reinforcement}
No more review needed — it's internalized. / 已内化，无需再复习。
```

**Partially correct / 部分正确:**
```
Almost there! You nailed {correct part}, but: {gentle correction + 1 key detail}
I'll resend this card tomorrow for a quick refresh. / 明天再发一次巩固一下。
```

**Wrong / 答错:**
```
Not quite — that's why we're reviewing! Key point: {2-3 sentence explanation}
Think of it this way: {1-sentence analogy} / 换个角度想：{一句话类比}
I'll resend this tomorrow. / 明天重发一次。
```

**No response / "don't know":**
```
No worries — quick refresher: {2-3 sentence summary}
I'll resend this tomorrow. / 明天再发一次。
```

## Chain Scheduling

User replies in main chat → agent executes:
1. Read `learning-data/{slug}/review-state.json`
2. **Correct** → Next node: 1d→3d→7d progression / 进入下一节点
3. **Wrong** → Retry in 1 day, reset consecutive count / 1 天后重试，重置连续计数
4. **3 consecutive correct** → Mark "internalized", stop / 标记「已内化」，终止
5. **No response 24h** → Skip, next planned node still fires / 跳过，下一节点照常

## Review State

`learning-data/{slug}/review-state.json`:
```json
{
  "day_1": {
    "concept": "What is React Hooks",
    "reviews_completed": 0, "consecutive_correct": 0,
    "next_review_at": "2026-04-07T09:00:00", "status": "pending"
  }
}
```

Status flow: `pending` → `sent` → `correct`/`wrong` → `internalized`/`skipped`
