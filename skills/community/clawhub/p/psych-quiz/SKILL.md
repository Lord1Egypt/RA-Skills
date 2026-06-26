---
name: psych-quiz
description: Provide short, low-risk self-check quizzes for common mental wellness themes such as stress, sleep, and emotional overload. Results are for self-observation only.
version: 1.0.0
tags: quiz, mental-health, self-assessment, psychology, stress, wellness
---

# Psych Quiz

Provide short, structured self-check quizzes for everyday mental wellness reflection.

## Usage Scenarios

### Scenario 1: Stress-level self-check
**User input:** "帮我测测压力，看我现在的压力有多大。"
**Expected output:** Guide the user through 6 short questions about tension, racing thoughts, irritability, sleep quality, perceived load, and focus — each rated Never/Sometimes/Often/Almost always. Score the results into a band (manageable / building / elevated / high), give a brief interpretation ("你的压力信号在明显累积"), and offer 2-3 practical suggestions such as reducing one nonessential demand or doing a short grounding exercise.

### Scenario 2: Sleep quality reflection
**User input:** "最近睡得不好，帮我看看是不是太焦虑了。"
**Expected output:** Frame a sleep-focused mini-quiz with 5 questions on falling asleep, staying asleep, waking tired, daytime fatigue, and racing thoughts at bedtime. Score and interpret the pattern, distinguishing whether the sleep issue is stress-driven or may have other causes. Provide 1-2 immediate next steps (e.g., a simple wind-down routine, reducing screen time before bed).

### Scenario 3: General mental wellness check-in
**User input:** "给我一个 quick mental check-in，看看我最近状态怎么样。"
**Expected output:** Offer a concise 5-question mixed quiz covering mood, energy, focus, social engagement, and overall coping. Score into a light result band and provide a short, non-alarmist interpretation. Include a professional-support reminder if any answers indicate persistent strain. Keep the entire interaction under 5 exchanges, prioritizing quick reflection over depth.
### Scenario 4: 微信群里有人发了心理健康测试想做
**User input:** "朋友分享了一个公众号的心理健康测试说很准，做完显示中度抑郁，我该信吗？"
**Expected output:** 提醒用户：公众号的非专业心理测试不具备临床诊断效度，建议使用标准化工具（如SDS抑郁自评量表、GAD-7焦虑筛查量表，简单心理/壹心理App有官方版本）。如果非专业测试提示中度以上，建议去三甲医院心理科或精神科做专业评估，而不是自行判断。同时建议避免反复做不同在线测试造成'诊断色'。

## Core purpose

Use this skill to help the user:
- do a quick self-check on stress, sleep, burnout, or emotional strain
- turn vague unease into a simple, structured reflection
- get a lightweight result with practical next steps
- notice when a situation may need more support

This skill is for **self-observation and general reflection**. It is **not** diagnosis, psychotherapy, or medical advice.

## Use this skill for

Typical triggers include:
- "帮我测测压力"
- "我最近状态怎么样"
- "做个心理小测试"
- "我是不是压力太大了"
- "给我一个 quick mental check-in"
- "stress quiz"
- "burnout check"
- "sleep check"

## Do not use this skill as

Do not present this skill as:
- a clinical assessment
- a diagnosis tool
- professional psychological evaluation
- a substitute for therapy or psychiatry
- a definitive judgment about the user's condition

Avoid statements like:
- "你已经患有焦虑症/抑郁症"
- "这个结果证明你有问题"
- "只要做这个测试就能确定"

Prefer phrasing like:
- "自我观察参考"
- "初步整理"
- "一般性支持"
- "如果困扰持续，建议寻求专业帮助"

## Recommended quiz flow

Default flow:
1. brief framing and disclaimer
2. ask the user to answer based on the last 1-2 weeks
3. give 5-7 short questions
4. score into a light result band
5. provide a short interpretation
6. offer 1-3 practical next steps
7. add safety escalation if needed

## First supported quiz: Stress Check-In

Start with a **stress check-in** as the default MVP because it is:
- easy to understand
- broadly useful
- easy to structure and reuse
- relatively low-risk when framed properly

### Question format

Use four options per item:
- Never
- Sometimes
- Often
- Almost always

### Suggested stress questions

1. Lately, I often feel tense or unable to relax.
2. My mind keeps running and is hard to slow down.
3. I get irritated or impatient more easily than usual.
4. My sleep or rest has been worse, or I still feel tired after resting.
5. I feel like the things on my plate are close to my limit.
6. It has been harder to focus on what I need to do.

### Suggested scoring

- Never = 0
- Sometimes = 1
- Often = 2
- Almost always = 3

Suggested ranges:
- **0-4**: Stress looks relatively manageable
- **5-8**: Some stress is building
- **9-13**: Stress appears noticeably elevated
- **14-18**: Stress appears high and worth attention

## Result output pattern

Every result should include:
1. **Result level**
2. **Brief interpretation**
3. **1-3 practical suggestions**
4. **Professional-support reminder when appropriate**

### Example result: relatively manageable

> Your current stress level looks relatively manageable.
> That does not mean there is no pressure at all — it suggests you may still have some buffer right now.
> A good next step is to keep your basic rest rhythm and notice whether new stressors are starting to build.

### Example result: some stress is building

> You may already be carrying a noticeable amount of stress.
> It may not have fully overwhelmed you, but it is probably worth addressing before it grows heavier.
> A helpful next step is to reduce one nonessential demand, write down the top stressor, and make space for one real recovery break.

### Example result: noticeably elevated

> Your recent answers suggest stress may already be affecting your mood, attention, or rest.
> This can be a good time to shift from "push through" mode into "stabilize first" mode.
> Consider reducing one pressure source, talking to someone you trust, or getting more structured support if this keeps going.

### Example result: high and worth attention

> Your recent answers suggest your stress level may be quite high right now.
> If this is lasting, or if you are also dealing with sleep disruption, emotional worsening, or loss of daily functioning, it may be important to seek support in real life instead of carrying it alone.
> Right now, the priority is not to "push harder," but to help yourself stabilize and get support.

## Style rules

Prefer language that is:
- calm
- clear
- non-alarmist
- respectful
- practical

Avoid language that is:
- dramatic
- diagnostic
- preachy
- shame-based
- falsely certain

## Safety escalation

Stop the normal quiz flow and use a direct safety response if the user expresses:
- self-harm thoughts
- suicide thoughts
- intent to harm others
- inability to stay safe
- overwhelming despair that makes a quiz inappropriate

Use a response like:

> ⚠️ Important: this is not the right moment for a normal self-check quiz. If you may be at risk of harming yourself or someone else, or you cannot keep yourself safe right now, please contact a trusted person immediately and reach out to local emergency care, a crisis line, a hospital, or a licensed professional as soon as possible.

Then stay focused on immediate safety rather than continuing the quiz.

## Disclaimer

> ⚠️ **Disclaimer**: This tool provides general self-reflection support only. It does not provide diagnosis, psychotherapy, psychiatric evaluation, or medical advice. If you are experiencing severe distress, worsening hopelessness, thoughts of harming yourself or others, or a clear decline in daily functioning, please seek help from a licensed mental health professional, a doctor, or local emergency support resources.

## Minimal operating pattern

For most uses, prefer this pattern:
1. brief framing
2. 5-6 questions
3. simple scoring
4. short interpretation
5. one small next step
6. optional follow-up support

## Future expansion

After the stress MVP is stable, the same structure can be extended to:
- sleep check
- burnout check
- emotional overload check
- relationship strain check

Keep the same tone, same safety boundaries, and same non-diagnostic framing.
