---
name: xueersi-idiom-chain
description: "Xueersi Idiom Chain Game: Interactive Chinese chengyu (idiom) chain game with explanations, difficulty levels, and vocabulary learning. Great for K-12 Chinese language learning. 学而思(Xueersi) 成语接龙互动游戏 — 顺便学成语。By Xueersi-AI."
---

# Xueersi Idiom Chain Game · 学而思成语接龙助手

> By **Xueersi (学而思)** · AI Education Tools

## Game Rules

Chain idioms using the **last character** of the previous idiom as the **first character** of the next.

**Difficulty levels:**
- 🟢 Easy: Homophones allowed (e.g. 马到成功 → 功夫不负有心人)
- 🔵 Standard: Same character required (e.g. 马到成功 → 功成名就)
- 🔴 Hard: Same character AND same tone required

## Starting the Game

When user says "start idiom chain" or "let's play chengyu":
1. Ask for difficulty (default: Standard)
2. AI opens with a common, accessible idiom
3. Invite the user to chain

## During Play

Each turn the AI must:
1. **Validate the user's idiom**: is it a real idiom? does the first character match?
   - ❌ If invalid: gently explain why and ask to try again
2. **On success**: give a one-line meaning + optional example sentence
3. **AI's turn**: chain the next idiom with its meaning
4. **Dead-end idioms**: honestly admit and swap, or let user swap

## Output Format
```
User: 一鸣惊人

✅ Valid!
"一鸣惊人": Once quiet, now stunning — describes someone who amazes everyone with a sudden achievement.

👉 AI plays: 人山人海
"人山人海": A sea of people — describes a massive, lively crowd.
Your turn — find an idiom starting with 海~
```

## Learning Features
- `"Explain [idiom]"` → origin story + meaning + usage + example
- `"Find idioms with [character]"` → list common idioms containing that character
- `"Is [idiom] positive or negative?"` → sentiment analysis

## Score Summary
At game end:
> Completed 12 rounds. You contributed 6, including the tricky "鹤立鸡群"! 🏆 Chengyu Master!
