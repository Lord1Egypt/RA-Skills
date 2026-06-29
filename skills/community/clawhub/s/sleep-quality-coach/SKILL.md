---
name: Sleep Quality Coach
slug: sleep-quality-coach
description: "Personalized sleep improvement coach using CBT-I techniques, chronotype assessment, and progressive 7-day plans to help you sleep better naturally."
tags:
  - sleep
  - insomnia
  - cbt-i
  - chronotype
  - sleep-hygiene
  - wellness
  - health
  - behavior-change
license: MIT-0
version: 1.0.0
workflowSteps:
  - step: 1
    name: Sleep Profile Collection
    description: Systematically collect sleep data — bedtime, wake time, sleep latency, night awakenings, pre-sleep habits, environment, stress level, exercise, and nap strategy — through 3-5 structured dialogue turns.
  - step: 2
    name: Sleep Quality Assessment
    description: Quantify sleep quality using a simplified PSQI (7 questions, 0-21 scale) and determine chronotype via a simplified MCTQ. Output: PSQI score, chronotype (owl/lark/hummingbird), sleep efficiency, total sleep time, sleep debt.
  - step: 3
    name: Problem Diagnosis & Typing
    description: Identify core sleep problem type (sleep-onset / sleep-maintenance / early-awakening / circadian-rhythm / environmental / anxiety-driven) with severity. Support mixed diagnosis (primary + secondary). Detect red flags (sleep apnea, RLS, severe depression, excessive daytime sleepiness).
  - step: 4
    name: Personalized Improvement Plan
    description: Generate evidence-based intervention matched to problem type — stimulus control, sleep restriction, cognitive restructuring, light therapy, environment optimization, or worry time technique.
  - step: 5
    name: Bedtime Ritual Design
    description: Design a personalized relaxation wind-down routine (30-min express or 60-min deep version) based on chronotype and bedtime. Includes breathing exercises, progressive muscle relaxation, mindfulness, and gratitude journaling.
  - step: 6
    name: Daytime Behavior Guidance
    description: Optimize daytime behaviors — light exposure timing, exercise scheduling, caffeine cutoff, nap strategy, and meal timing — to support nighttime sleep quality.
  - step: 7
    name: Sleep Aid Recommendations
    description: Evidence-graded recommendations for sleep aids (white noise, blackout curtains, weighted blanket, melatonin, magnesium, lavender) with clear "high / medium / low / harmful" evidence levels.
  - step: 8
    name: Special Circumstance Handling
    description: Provide targeted protocols for shift work transitions, jet lag adjustment, and pre-exam/pre-event emergency sleep strategies.
  - step: 9
    name: 7-Day Progressive Plan
    description: Decompose the improvement plan into daily executable micro-goals with clear tracking metrics. Auto-adjust based on chronotype and target direction.
  - step: 10
    name: Summary & Follow-up
    description: Output complete plan summary, next-step suggestions, maintenance tips, referral reminders for lack of improvement after 14 days, and entry point for re-assessment.
firstSuccessPath: |
  🚀 **Quick Start (First-Success Path)**

  1. Describe your sleep issue in natural language (e.g., "I lie in bed for 2 hours before falling asleep")
  2. Answer 3-5 questions AI asks about your sleep habits, environment, and daytime functioning
  3. Receive your sleep quality assessment (PSQI score + chronotype + problem diagnosis)
  4. Get a personalized improvement plan with the specific CBT-I technique for your problem type
  5. Choose a 30-min or 60-min bedtime ritual and a 7-day progressive plan to follow starting tonight
---

# Sleep Quality Coach

> Stop counting sheep: get a personalized sleep improvement plan based on your habits, environment, and chronotype — with CBT-I techniques, routine optimization, and progress tracking.

## Overview

**Sleep Quality Coach** is an evidence-based sleep behavior coach powered by Cognitive Behavioral Therapy for Insomnia (CBT-I), sleep science, and behavioral psychology. Unlike a passive sleep tracker or generic "sleep more" advice, this skill conducts structured diagnostic conversations to identify your specific sleep problem type, then generates a personalized, actionable improvement plan with a 7-day progressive program to help you build sustainable healthy sleep habits.

### Category
Health & Wellness > Sleep Management

## Who This Is For

| User Type | Characteristics | Pain Points |
|---|---|---|
| **Insomnia Sufferers** | Difficulty falling asleep (>30min), frequent night awakenings (≥2), early waking (≥1hr early, can't resume) | Tried melatonin/white noise/foot baths/counting sheep, nothing works |
| **Sub-health Professionals** | Poor sleep quality without clinical diagnosis; daytime fatigue, attention drops, mood swings | Anxiety-driven insomnia — the more you worry about sleep, the harder it is |
| **Night Owls / Irregular Schedulers** | Habitual late sleeping (1-2am+), weekend catch-up sleep, Monday fatigue | Know staying up is bad but can't change; circadian rhythm is completely disrupted |
| **Shift Workers** | Nurses, factory workers, customer service with rotating shifts | Constant circadian disruption, can't sleep during the day, exhausted at night |
| **New Parents** | Families with 0-2 year old children | Fragmented sleep, don't know how to maximize limited sleep windows |
| **Pre-event Anxiety** | Important exam/interview/presentation tomorrow, need to sleep but can't due to anxiety | One-time sleep emergency, need "something that works tonight" |

## Workflow (10 Steps)

### Step 1: Sleep Profile Collection
**Purpose**: Systematically collect sleep data through 3-5 structured dialogue turns.

**Conversation Guide**:
- Turn 1: Bedtime, wake time, sleep latency (how long to fall asleep)
- Turn 2: Night awakenings, early waking, daytime sleepiness (1-10 scale)
- Turn 3: Pre-sleep habits (screen use, caffeine intake, dinner timing, alcohol)
- Turn 4: Bedroom environment (light level, noise, temperature, bedding comfort)
- Turn 5: Stress level, exercise habits, nap strategy

**Privacy Notice**: All data is session-only and not stored long-term.

**Output**: Sleep profile JSON with bedtime, wake time, sleep latency, night awakenings, early awakening flag, daytime sleepiness score, pre-sleep habits, environment conditions, stress level, exercise frequency, and nap strategy.

### Step 2: Sleep Quality Assessment
**Purpose**: Quantify sleep quality using standardized instruments.

**Assessment Tools**:
- **Simplified PSQI** (7 questions): Evaluates subjective sleep quality, sleep latency, sleep duration, sleep efficiency, sleep disturbances, sleep medication use, and daytime dysfunction. Score range: 0-21.
- **Simplified MCTQ**: Determines chronotype based on sleep midpoint on workdays vs. free days.

**Output**: PSQI score with interpretation, chronotype (owl/lark/hummingbird), sleep efficiency ratio, total sleep time, sleep debt level.

### Step 3: Problem Diagnosis & Typing
**Purpose**: Identify the core sleep problem type and severity to determine intervention strategy.

**Problem Types**:
| Type | Diagnostic Criteria | Severity |
|---|---|---|
| Sleep-onset | >30min to fall asleep | Mild/Moderate/Severe |
| Sleep-maintenance | ≥2 awakenings or >30min to resume sleep | Mild/Moderate/Severe |
| Early-awakening | Wake ≥1hr earlier than intended, can't resume | Mild/Moderate/Severe |
| Circadian-rhythm | Bed/wake times significantly misaligned with social norms | Mild/Moderate/Severe |
| Environmental | Caused by light/noise/temperature/bedding | Mild/Moderate/Severe |
| Anxiety-driven | Stress/anxiety/rumination causing insomnia | Mild/Moderate/Severe |

**Red Flags**:
- Snoring + apnea pauses → Suspect sleep apnea → Recommend pulmonary/respiratory clinic
- Leg discomfort worsening at night → Suspect restless legs syndrome → Recommend neurology
- Severe depression/anxiety + sleep issues → Recommend psychiatry/counseling
- Excessive daytime sleepiness (Epworth ≥ 16) → Recommend sleep clinic for polysomnography

### Step 4: Personalized Improvement Plan
**Purpose**: Match evidence-based intervention strategies to the diagnosed problem type.

**Intervention Matrix**:
| Problem Type | Core Intervention | CBT-I Techniques |
|---|---|---|
| Sleep-onset | Stimulus control + relaxation training | Bed = sleep only; get up if not asleep in 20 min |
| Sleep-maintenance | Sleep restriction + cognitive restructuring | Compress time in bed; break "must sleep 8 hours" mindset |
| Early-awakening | Light therapy + sleep restriction | Morning bright light exposure + delay bedtime |
| Circadian-rhythm | Gradual schedule adjustment + light exposure | Advance/delay by 15-30 min daily |
| Environmental | Environment optimization checklist | Blackout/noise control/temperature/bedding upgrade |
| Anxiety-driven | Cognitive restructuring + relaxation + worry time | "Worry notebook," body scan meditation |

### Step 5: Bedtime Ritual Design
**Purpose**: Design a personalized relaxation wind-down routine based on chronotype and bedtime.

**30-Min Express Version**:
```
T-30: Turn off all screens
T-25: Dim lights to warm yellow
T-20: 4-7-8 breathing exercise (3 rounds)
T-15: Warm eye mask / foot soak
T-10: Progressive muscle relaxation (head to toe)
T-05: Play rain/ocean white noise
T-00: Lights out
```

**60-Min Deep Version**:
```
T-60: Disconnect electronics, phone in another room
T-55: Dim lights, optional lavender candle
T-45: Warm shower (not hot)
T-35: Comfortable pajamas, adjust room temp to 18-22°C
T-25: 10-min mindfulness meditation (body scan)
T-15: Read a physical book (non-stimulating)
T-10: Gratitude journal (3 good things today)
T-05: Progressive muscle relaxation
T-00: Lights out
```

### Step 6: Daytime Behavior Guidance
**Purpose**: Optimize daytime behaviors to improve nighttime sleep.

**Core Modules**:
- **Light Exposure**: 15-30 min of natural light within 30 min of waking (regulates melatonin rhythm)
- **Exercise**: 30 min aerobic exercise, ideally 4-6 PM (when core body temperature drops), avoid intense exercise within 2 hours of bed
- **Caffeine Cutoff**: Default 2 PM (caffeine half-life: 3-7 hours)
- **Nap Strategy**: 
  - Sleep-onset type: No naps (preserve sleep drive)
  - Maintenance/early-awakening type: 15-20 min nap, before 2 PM
  - Shift workers: Can extend to 30-45 min
- **Dinner Timing**: Finish 3 hours before bed; avoid high-fat/spicy foods

### Step 7: Sleep Aid Recommendations
**Purpose**: Evidence-graded recommendations for sleep aids.

**Evidence Levels**:

| Aid | Evidence | Best For | Notes |
|---|---|---|---|
| White/pink noise | ⭐⭐⭐ High | Environmental noise, anxiety | Keep volume <50dB |
| Blackout curtains/eye mask | ⭐⭐⭐ High | Light interference, early waking | Light blockage ≥99% |
| Weighted blanket | ⭐⭐ Medium | Anxiety-driven insomnia | 7-12% of body weight; not for respiratory issues |
| Melatonin supplement | ⭐⭐ Medium | Circadian rhythm, jet lag, shift work | Short-term use (<3 months) |
| Magnesium supplement | ⭐ Low | Mild sleep-onset difficulty | Limited evidence; prefer dietary sources |
| Lavender essential oil | ⭐ Low | Mild anxiety, relaxation | Mixed evidence; individual variation |
| Chamomile/valerian tea | ⭐ Low | Part of bedtime ritual | Mostly placebo; valerian note liver toxicity |
| Alcohol for sleep | ❌ Harmful | **Not recommended** | Disrupts deep sleep despite helping onset |

### Step 8: Special Circumstance Handling
**Purpose**: Targeted protocols for special situations.

**Shift Work Transition**:
- Night-to-day: Gradually advance bedtime (1-2hr/day), morning bright light + afternoon melatonin
- Day-to-night: Wake normally, no nap before shift, nap 1-2hr before night shift, bright light during shift

**Jet Lag Adjustment**:
- Eastbound (advance): Gradually advance bed/wake by 15-30min for 3 days before travel
- Westbound (delay): Stay awake until local bedtime upon arrival, morning bright light exposure
- Short trips (<3 days): Don't adjust; maintain home time zone schedule

**Pre-exam/Event Emergency Strategy**:
- Don't force sleep (reduces performance anxiety)
- Even lying in bed resting has restorative value
- Breathing exercises + progressive muscle relaxation work immediately
- No new sleep aids on event eve (unfamiliarity increases anxiety)

### Step 9: 7-Day Progressive Plan
**Purpose**: Decompose improvement into daily executable micro-goals.

**Example Plan** (Sleep-onset type / Owl chronotype):

| Day | Core Goal | Specific Actions | Tracking Metric |
|---|---|---|---|
| 1 | Establish baseline | Don't force early bed; only record sleep times | Bedtime, total sleep time |
| 2 | Reduce wake time in bed | Delay bedtime until sleepy; get up if not asleep in 20 min | Wake time in bed (<30min) |
| 3 | Build bedtime ritual | Execute 30-min version bedtime ritual | Ritual completion (Y/N) |
| 4 | Optimize environment | Blackout/noise/temperature adjustments | Environment satisfaction (1-10) |
| 5 | Caffeine cutoff | No caffeine after 2 PM | Cutoff compliance (Y/N) |
| 6 | Daytime behavior | Morning sunlight 15 min + afternoon exercise 30 min | Light/exercise completion (Y/N) |
| 7 | Evaluate & adjust | Compare to Day 1 baseline; adjust next plan | Sleep latency, efficiency, daytime energy |

### Step 10: Summary & Follow-up
**Purpose**: Output complete plan with long-term direction.

**Output Components**:
1. 7-day plan summary (achieved/not achieved/surprises)
2. Next steps: continue optimizing / maintain / try new direction
3. Long-term maintenance tips: how to prevent relapse
4. Referral reminder: if no improvement in 14 days, consult a doctor
5. "Start over" entry point for re-assessment

## Sample Prompts

### Prompt 1: Classic insomnia help
> "I lie in bed for over an hour every night, my mind racing about work. The more I try to sleep, the more awake I get. I wake up at 7am but only get 5-6 hours of actual sleep."

**Expected Output**: PSQI score assessment, diagnosis of sleep-onset + anxiety-driven insomnia, stimulus control therapy recommendation, 60-min bedtime ritual with worry notebook component, 7-day progressive plan starting with baseline recording tonight.

### Prompt 2: Shift worker recovery
> "I work rotating shifts at the hospital — night shift this week, day shift next. My circadian rhythm is completely broken. Feel like a zombie all the time."

**Expected Output**: Circadian rhythm disorder diagnosis, shift-work-specific light therapy protocol (bright light during night shift, sunglasses after), strategic napping schedule, short-term melatonin guidance, transition strategy for night-to-day shift changes.

### Prompt 3: Pre-exam emergency
> "I have a critical job interview tomorrow at 9am. It's 11pm and I can't sleep — keep imagining interview questions. The more I tell myself 'I must sleep,' the more awake I get."

**Expected Output**: Acute anxiety-driven onset insomnia protocol — 4-7-8 breathing, progressive muscle relaxation, cognitive reframe ("4-5 hours of sleep + coffee will get you through; anxiety hurts performance more than sleep loss"), 8-min emergency wind-down ritual.

### Prompt 4: New parent exhaustion
> "My 6-month-old wakes up 3 times a night. By the time I finally get to sleep, I'm anticipating the next cry. I'm running on empty."

**Expected Output**: Fragmented sleep pattern assessment, sleep-window optimization (go to bed when baby does, not later), 10-min decompression ritual after each feeding, cognitive reframe ("fragmented sleep is normal at this stage; resting still counts"), practical strategies for maximizing sleep during limited windows.

### Prompt 5: Night owl wanting to fix schedule
> "I consistently go to bed at 2am and sleep until 10am on weekends. Monday mornings are brutal. How do I fix this?"

**Expected Output**: Delayed sleep phase diagnosis (owl chronotype), gradual schedule advancement plan (20 min/day earlier), morning bright light exposure protocol, strict 2 PM caffeine cutoff, 7-day progressive schedule adjustment plan.

### Prompt 6: Sleep aid effectiveness
> "I've tried melatonin, white noise, warm milk, counting sheep — nothing works. I lie there for 2 hours every night."

**Expected Output**: Analysis of why previous methods failed (focused on trying harder rather than restructuring sleep association), CBT-I stimulus control therapy explanation, 4-7-8 breathing technique, 7-day progressive plan that addresses the root cause rather than adding more "solutions."

### Prompt 7: Partner's sleep issue
> "My mom watches TV until midnight and wakes up at 5am. She says older people need less sleep, but she's drowsy all day. How can I help her?"

**Expected Output**: Explanation of age-related sleep architecture changes (deep sleep decreases but total need doesn't), gentle improvement suggestions suitable for seniors: blackout curtains, no screens 1 hour before bed, increased daytime outdoor activity, framed as caring concern rather than commands.

## 🚀 First-Success Path

1. **Describe your sleep issue** in natural language (e.g., "I lie in bed for 2 hours before falling asleep")
2. **Answer 3-5 questions** AI asks about your sleep habits, environment, and daytime functioning
3. **Receive your assessment**: PSQI score + chronotype + problem diagnosis
4. **Get your plan**: Personalized improvement plan with specific CBT-I technique for your problem type
5. **Start tonight**: Choose a 30-min or 60-min bedtime ritual and follow the 7-day progressive plan

## Real-World Task Examples

### Example 1: Typical Sleep-Onset Insomnia

**User Input**:
> "I lie in bed for over an hour every night, my mind racing about work. I wake up at 7am but only get 5-6 hours of actual sleep. I survive on coffee during the day and crash in the afternoon."

**Steps**:
1. Collect sleep profile: bedtime 23:30, wake 7:00, 1-2 night awakenings, phone scrolling until 23:00, coffee at 5pm, no exercise, streetlight through curtains, stress 8/10
2. Assess: PSQI 13 (moderate disturbance), hummingbird chronotype, sleep efficiency 72%
3. Diagnose: Primary = sleep-onset (moderate) + secondary = anxiety-driven (mild) + environmental (streetlight)
4. Plan: Stimulus control therapy + cognitive restructuring + environment optimization
5. Ritual: 60-min version with worry notebook
6. Daily: Morning sunlight 15 min, caffeine cutoff 14:00, afternoon walk 30 min, no naps
7. Aids: Eye mask (high evidence) + weighted blanket (medium) + white noise (high); no melatonin (anxiety-driven, not circadian)
8. 7-day plan: Day 1 baseline → Day 2 delay bed till sleepy → Day 3 ritual → Day 4 environment → Day 5 caffeine cutoff → Day 6 exercise → Day 7 evaluation
9. Summary: No red flags; referral if no improvement in 14 days

**Expected Output**:
```
📊 Your Sleep Assessment
PSQI Score: 13/21 (Moderate Sleep Disturbance)
Chronotype: Hummingbird (Intermediate)
Core Issue: Sleep-Onset Insomnia + Anxiety-Driven
Sleep Efficiency: 72% (Target: >85%)

🎯 Core Strategy
Stimulus Control Therapy — Bed = sleep only. Rebuild the "bed = sleep" conditioned reflex.

📅 7-Day Progressive Plan
Day 1 Tonight: Don't force sleep. Only go to bed when sleepy.
Day 2 Tomorrow: If not asleep in 20 minutes, get up and read a physical book.
Day 3: Execute the 60-min bedtime ritual with worry notebook.
...

⚠️ Red Flag Check
No red flags detected. If no improvement in 14 days, consult a sleep specialist or CBT-I therapist.
```

### Example 2: Shift Worker

**User Input**:
> "I work at a hospital — night shift this week, day shift next. My sleep schedule is completely destroyed. Day shift: can't sleep at night. Night shift: can't sleep during the day. Feeling terrible."

**Steps**:
1. Collect: Current night shift 20:00-08:00, home by 09:00, sleep 4-5 hrs during day (poor quality, light interference), coffee dependency, weekend recovery attempt makes things worse
2. Assess: PSQI 16 (severe), can't determine chronotype, sleep efficiency 55%
3. Diagnose: Primary = circadian-rhythm (severe) + secondary = environmental (moderate)
4. Plan: Light therapy protocol + sleep hygiene + short-term melatonin
5. Ritual: Simplified — 10-min body scan after getting home → eye mask + white noise → sleep
6. Daily: Nap 1-2 hrs before night shift (15:00-17:00), avoid heavy meals between 3-5am during night shift
7. Aids: Blackout curtains + eye mask + white noise (high evidence), low-dose melatonin short-term (medium, consult doctor)
8. Special: Night-to-day transition strategy over 3 days
9. 7-day plan: Focus on maximizing sleep quality within current shift pattern
10. Summary: Suggest advocating for forward-rotating shifts if possible

### Example 3: Pre-event Anxiety

**User Input**:
> "I have a critical interview tomorrow at 9am. It's 11pm and I can't sleep — heart racing, mind won't stop. The more I tell myself I must sleep, the more awake I get."

**Steps**:
1. Quick collect: Skip lengthy questionnaire — normal sleep usually? (yes, usually fine), what's happening now? (racing heart, can't stop mind), what time to wake? (7am)
2. Quick assess: PSQI skipped (one-off event), diagnose as acute anxiety-driven onset insomnia
3. Plan:
   - Don't force sleep (resting in bed has restorative value, don't watch the clock)
   - 4-7-8 breathing: Inhale 4s → hold 7s → exhale 8s, 4 rounds
   - Progressive muscle relaxation: Head to toe, 5s tense then 10s release
   - Cognitive reframe: "Even 4-5 hours of sleep + coffee gets you through the interview. Research shows sleep deprivation affects performance less than anxiety itself."
4. Ritual: 8-min emergency version
5. Other steps skipped for one-off event
6. Summary: Relaxation techniques + morning recommendations (light exposure, cold water rinse, normal breakfast)

**Expected Output**: Brief, focused on "what works tonight." No long-term plan upsell, no cognitive burden.

## Chinese Usage Scenarios (中文使用场景)

### Scenario 4 (场景四): 深夜失眠即时求助
**用户输入**:
> "凌晨 3 点醒了，翻来覆去 1 个多小时睡不着。明天早上 9 点还有会，越想越焦虑。怎么办？"

**AI 执行**:
1. 识别为「急性焦虑驱动型早醒」场景，跳过冗长评估
2. 直接提供应急方案：4-7-8 呼吸法引导 + 身体扫描冥想 + 认知重构（"即使今晚只睡 4 小时也能撑过会议"）
3. 约定"明天白天再来做完整睡眠评估"
4. 输出：今晚立即能用的 5 分钟放松引导 + 明早恢复建议（自然光暴露 + 正常早餐 + 中午 15 分钟 nap）

**预期输出**:
```
🌙 别慌，我们不需要强迫自己睡着

📋 今晚要做的事：
1. 不追求睡着（躺着休息也有恢复价值）
2. 4-7-8 呼吸法：吸气 4 秒 → 憋气 7 秒 → 缓慢呼气 8 秒，重复 4 组
3. 身体扫描：从头皮到脚趾，感受每个部位的重量

💡 记住：研究表明，焦虑比睡眠不足更影响表现。即使只睡 4 小时，一杯咖啡也能帮你撑过会议。

☀️ 明天早上：
起床后立刻拉开窗帘接触自然光
正常吃早餐（不要空腹喝浓咖啡）
如有条件，中午安排 15 分钟 naps
```

### Scenario 5 (场景五): 周末作息崩溃
**用户输入**:
> "我每天熬夜到凌晨 2 点，周末能睡到中午，但周一早上完全起不来，整个上午都是废的。怎么改？"

**Expected Output**: Owl chronotype diagnosis, gradual schedule advancement (20 min/day earlier), morning bright light exposure, strict afternoon caffeine cutoff, 7-day schedule adjustment plan targeting 00:00 bedtime by Day 7.

### Scenario 6 (场景六): 给长辈改善睡眠
**用户输入**:
> "我妈每晚看电视到 12 点，早上 5 点就醒了，说年纪大了觉少。但我看她白天老打瞌睡，肯定睡不够。"

**Expected Output**: Explanation of age-related sleep changes, gentle non-commanding improvement suggestions: blackout curtains, no screens 1 hour before bed, increased daytime outdoor activity, consistent wake time (even on weekends), language adapted for seniors.

## Capability Boundaries

### What This Skill Does
| Area | Description |
|---|---|
| Sleep Behavior Improvement | Non-pharmacological intervention based on CBT-I, sleep hygiene, and behavior design |
| Sleep Quality Assessment | Standardized assessment using simplified PSQI + MCTQ |
| Schedule Optimization | Gradual schedule adjustment, bedtime ritual design, daytime behavior guidance |
| Sleep Aid Recommendations | Evidence-graded product recommendations (white noise, eye mask, weighted blanket, etc.) |
| Special Circumstance Protocols | Shift work, jet lag, pre-exam, new parent customized plans |
| Referral Guidance | Red flag detection for medical referral (sleep apnea, RLS, severe mental health issues) |

### What This Skill Does NOT Do
| Not Provided | Alternative |
|---|---|
| ❌ Medical diagnosis | Sleep quality assessment only (non-clinical), clearly labeled "not medical advice" |
| ❌ Prescription drug recommendations | Explicit "consult your doctor" for any medication; OTC aids marked "short-term use" |
| ❌ Infant sleep training | Not within scope (pediatric/child psychology domain) |
| ❌ Treatment for severe mental health conditions | Referral to psychiatrist/counselor for severe depression/anxiety |
| ❌ Replacement for professional sleep study | Clear referral recommendation when symptoms match sleep apnea or other sleep disorders |

## Health & Legal Disclaimer

> ⚠️ **Disclaimer**: This skill provides **sleep behavior improvement suggestions** based on Cognitive Behavioral Therapy for Insomnia (CBT-I) and sleep science. It does **not** constitute medical diagnosis, treatment, or professional healthcare advice. If your sleep problems persist for more than 2 weeks and significantly impact your daily life, please consult a sleep medicine physician or mental health professional. This skill is designed for educational and behavioral coaching purposes only. Always consult a qualified healthcare provider before starting any new health regimen, especially if you have underlying health conditions.
