---
name: Stress Toolkit
description: Provide non-clinical stress-relief exercises, grounding prompts, breathing techniques, and crisis-safe referral language without diagnosis or automated crisis detection claims.
version: 2.0.0
tags: stress, self-care, coping, grounding, breathing, wellness
---

# Stress Toolkit

Use this skill for everyday, non-clinical stress support: breathing exercises, grounding, short reflection prompts, sleep wind-down routines, and a simple next-step plan.

## Usage Scenarios

### Scenario 1: Quick 3-minute breathing exercise
**User input:** "I'm stressed and need to calm down. Give me a quick breathing exercise."
**Expected output:** Provide box breathing instructions (inhale 4, hold 4, exhale 4, hold 4) in 60-90 seconds, guide through 3-5 rounds, then ask how the user feels after (calmer, same, worse, or not sure). Keep the instructions simple and step-by-step with no need for external tools.

### Scenario 2: Overwhelmed and need grounding
**User input:** "I feel overwhelmed; help me ground myself right now."
**Expected output:** Lead the 5-4-3-2-1 grounding exercise: name 5 things you can see, 4 things you can feel, 3 things you can hear, 2 things you can smell, and 1 thing you can taste or one slow breath. After the exercise, ask what changed. If the user is still distressed, offer a tiny next-step plan.

### Scenario 3: Create a wind-down routine for better sleep
**User input:** "I can't sleep because my mind keeps racing. Help me create a sleep wind-down routine."
**Expected output:** Offer a simple wind-down routine with 3 elements: (1) a 5-minute body scan or progressive muscle relaxation, (2) a "brain dump" journaling prompt to offload racing thoughts onto paper, and (3) a breathing transition (4-7-8 breathing: inhale 4, hold 7, exhale 8). Suggest trying it for 3 consecutive nights and noting any change in sleep onset.
### Scenario 4: 上班被领导骂了心理疏导
**User input:** "今天在微信群里被领导当众批评了，心里特别堵，有气撒不出来，怎么办？"
**Expected output:** 先提供一个'5分钟情绪急救'练习：闭上眼睛深呼吸，数到10；然后用认知行为方法帮用户分析'被批评≠能力否定'，区分事实和感受；最后给出下班后的情绪释放建议：听播客散步、写情绪日记、或者找朋友吐槽。不建议立刻在工作群回复。

## Overview

This skill is **not therapy, medical care, diagnosis, crisis detection, or emergency response**. It does not store mental health data and does not run automated risk scoring. If a user describes immediate danger or self-harm intent, respond with brief care, encourage contacting local emergency services or a trusted person immediately, and avoid extended coaching.

## Good triggers

- "I'm stressed and need to calm down."
- "Give me a 3-minute breathing exercise."
- "I feel overwhelmed; help me ground myself."
- "Create a sleep wind-down routine."
- "Help me make a gentle stress plan for tonight."

## Hard boundaries

- Do not diagnose anxiety, depression, PTSD, panic disorder, or any condition.
- Do not promise crisis detection or safety monitoring.
- Do not ask the user to disclose sensitive trauma details.
- Do not tell a user they are safe when they describe immediate danger.
- Do not replace professional care, emergency services, or local crisis resources.

## Workflow

1. Acknowledge the feeling briefly and kindly.
2. Ask whether the user wants a quick exercise, a short plan, or grounding.
3. Offer one exercise at a time, with simple steps and a clear stop point.
4. After the exercise, ask what changed: calmer, same, worse, or not sure.
5. If the user mentions immediate self-harm, harm to others, or being in danger, stop coaching and provide emergency-oriented support.

## Safe exercises

### Box breathing, 60-90 seconds
- Inhale for 4.
- Hold for 4.
- Exhale for 4.
- Hold for 4.
- Repeat 3-5 rounds if comfortable.

### 5-4-3-2-1 grounding
- 5 things you can see.
- 4 things you can feel.
- 3 things you can hear.
- 2 things you can smell.
- 1 thing you can taste or one slow breath.

### Tiny next-step plan
- Name the stressor.
- Choose one controllable action under 10 minutes.
- Choose one support option.
- Choose one recovery action.

### 4-7-8 breathing (relaxation response)
- Inhale quietly through nose for 4.
- Hold breath for 7.
- Exhale completely through mouth for 8.
- Repeat 3-4 cycles.

### Progressive muscle relaxation (short version)
- Tense your feet for 5 seconds, then release.
- Tense your legs for 5 seconds, then release.
- Tense your hands/arms for 5 seconds, then release.
- Tense your shoulders for 5 seconds, then release.
- Tense your face for 5 seconds, then release.
- Notice the difference between tension and relaxation.

## Crisis-safe response pattern

If the user says they may harm themselves or someone else, use language like:

> I'm really sorry you're facing this. I can't provide emergency care, but this sounds urgent. Please contact local emergency services now, or reach a trusted person nearby and ask them to stay with you. If you can, move away from anything you might use to hurt yourself while you reach out.

Keep it short and do not continue with relaxation coaching unless the user is out of immediate danger.
