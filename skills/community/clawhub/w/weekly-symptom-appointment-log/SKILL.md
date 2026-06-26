---
name: Weekly Symptom Appointment Log
description: Prepare a clear seven-day symptom, trigger, question, and visit-note sheet before a clinician appointment.
version: "1.0.0"
type: prompt-flow
tags:
  - health-log
  - appointment-prep
  - symptom-tracking
  - clinician-visit
  - weekly-note
author: OpenClaw Skill Builder
---

# Weekly Symptom Appointment Log

## Overview

Weekly Symptom Appointment Log helps a user prepare a concise seven-day health note before a clinician visit. It organizes symptoms, timing, severity, possible triggers, impact, questions, and a visit summary.

This skill is not medical advice. It does not diagnose, recommend treatment, change medications, or tell the user to delay urgent care. If symptoms are severe, sudden, dangerous, or rapidly worsening, the user should seek urgent medical help or local emergency services.

## When to Use

Use this skill when the user wants to organize recent health observations before an appointment, such as:

- Weekly symptom tracking before a doctor visit
- Preparing notes for a specialist, therapist, physical therapist, or primary care clinician
- Summarizing symptom patterns clearly
- Making a question list for a visit
- Recording triggers, timing, and impact without self-diagnosing

**Trigger phrases:** "help me summarize symptoms for my appointment", "make a weekly symptom log", "doctor visit note", "track symptoms this week", "what should I tell my clinician".

## Urgent-Care Safety Check

Before routine logging, ask whether any urgent red flags are present. Keep this general and safety-focused.

Advise urgent care or emergency services now if the user reports severe, sudden, or potentially life-threatening symptoms, including but not limited to:

- Chest pain, pressure, trouble breathing, fainting, or signs of stroke
- Severe allergic reaction, swelling of face or throat, or trouble swallowing
- Severe injury, uncontrolled bleeding, or severe burns
- Sudden severe headache, confusion, seizure, or loss of consciousness
- Suicidal thoughts, intent to self-harm, or risk of harming others
- Severe abdominal pain, pregnancy-related emergency symptoms, or high fever with stiff neck
- Rapidly worsening symptoms or anything the user believes may be an emergency

If a red flag is present, do not continue routine logging as the main task. Encourage immediate professional help and offer to help create a brief emergency note only if safe.

## Deliverable

Produce a **Seven-Day Symptom Appointment Sheet** with:

1. Appointment snapshot
2. Symptoms being tracked
3. Seven-day log table
4. Possible triggers and patterns
5. Function and impact notes
6. Medication, treatment, and self-care notes for reporting only
7. Questions for the clinician
8. Concise visit summary
9. Items to bring

## Workflow

### Step 1 - Choose Symptoms to Track

Ask the user to choose up to five main symptoms for the week. For each symptom, capture:

- Plain-language name
- Location, if relevant
- Severity scale from 0 to 10, if useful
- Frequency or duration
- What makes it better or worse
- Impact on sleep, work, school, movement, appetite, mood, or daily activities

Avoid suggesting a diagnosis. Use the user's words where possible.

### Step 2 - Log Timing Across Seven Days

Create a simple seven-day structure. For each day, capture:

- Date or day label
- Symptom present or absent
- Start time and end time, if known
- Severity
- What was happening before it started
- Food, activity, stress, sleep, medication, environment, cycle, exposure, or other possible trigger, if relevant
- What helped or did not help
- Notes for clinician

If the user has incomplete data, mark it as "not recorded" rather than guessing.

### Step 3 - Note Patterns Without Diagnosing

Summarize observations carefully:

- Symptoms occurred more often at a certain time of day
- Symptoms followed a possible trigger
- Symptoms improved after rest, hydration, food, movement, medication, or another reported action
- Symptoms affected sleep, work, school, mood, or activity
- Symptoms are new, changing, persistent, or improving

Use language like "possible pattern" and "worth asking about". Do not claim cause and effect unless a clinician has confirmed it.

### Step 4 - Draft Questions

Help the user prepare concise appointment questions:

- What could explain this pattern?
- Are any tests, exams, or referrals appropriate?
- Which symptoms should prompt urgent care?
- Are current medications or supplements relevant?
- What should I track next week?
- What changes should I make or avoid before follow-up?

Include the user's top three priorities first.

### Step 5 - Create Visit Summary

Write a short summary the user can read or hand to a clinician:

- Main concern
- When it started
- Most frequent or severe symptoms
- Notable changes
- Possible triggers observed
- Impact on daily life
- Current medications, treatments, or self-care to report
- Top questions

Keep it factual, brief, and free of diagnosis claims.

## Output Template

```markdown
# Seven-Day Symptom Appointment Sheet

## Appointment Snapshot
- Clinician or clinic:
- Appointment date:
- Main concern:
- Week covered:
- Urgent red flags present today: Yes / No / Not asked

## Symptoms to Track
1. [Symptom] - location, severity range, frequency, impact
2. [Symptom] - location, severity range, frequency, impact

## Seven-Day Log
| Day | Symptoms and severity | Timing | Possible triggers or context | What helped or did not help | Impact | Notes for clinician |
|---|---|---|---|---|---|---|
| Day 1 |  |  |  |  |  |  |
| Day 2 |  |  |  |  |  |  |
| Day 3 |  |  |  |  |  |  |
| Day 4 |  |  |  |  |  |  |
| Day 5 |  |  |  |  |  |  |
| Day 6 |  |  |  |  |  |  |
| Day 7 |  |  |  |  |  |  |

## Possible Patterns to Discuss
- Timing:
- Triggers or context:
- What helped:
- What worsened:
- Changes over the week:
- Daily-life impact:

## Questions for the Clinician
1. [Top question]
2. [Second question]
3. [Third question]

## Visit Summary
[Brief factual paragraph using the user's words. No diagnosis claims.]

## Items to Bring
- Medication and supplement list
- Relevant measurements or home readings
- Photos, if relevant and appropriate
- Previous test results or discharge papers
- Insurance or referral paperwork, if needed
```

## Safety Boundaries

- Not medical advice, diagnosis, triage, or treatment planning.
- Do not recommend starting, stopping, or changing medication or treatment.
- Do not interpret test results as a clinician.
- Do not dismiss severe, sudden, dangerous, or rapidly worsening symptoms.
- If urgent red flags are present, advise urgent care or local emergency services instead of routine logging.
- Mental health crisis, self-harm risk, or harm-to-others risk requires immediate crisis or emergency support.
- Keep the log factual and based on the user's observations. Mark unknowns as unknown.

## Acceptance Criteria

1. Performs an urgent-care safety check before routine logging.
2. Lets the user choose symptoms and records timing, severity, frequency, and impact.
3. Creates a seven-day symptom log with triggers, context, what helped, and notes.
4. Summarizes possible patterns without diagnosing or claiming causation.
5. Drafts clinician questions with the user's top priorities first.
6. Creates a concise visit summary suitable for an appointment.
7. Avoids medical advice, treatment changes, and test interpretation.
8. Produces English-only prompt-flow content with no executable code.

## Example Prompts

Copy and paste one of these into your AI assistant with your details filled in:

1. **Doctor appointment next week:** "I have a doctor appointment next Tuesday and want to summarize headaches, fatigue, and nausea from the last seven days. Headaches are usually in the afternoon (severity 4-6), fatigue is worst in the morning, nausea comes and goes after meals. I've been sleeping poorly and skipping breakfast. Build me a seven-day symptom sheet to bring to the appointment."

2. **Tracking for a specialist:** "I'm seeing a neurologist in 5 days about recurring migraines. Over the past week I've had 3 migraine episodes — one on Monday (severe, with aura), one on Wednesday (moderate), and one on Saturday (mild). They seem worse after screen time and skipped meals. I also want to ask about a new medication option. Create a weekly log with trigger patterns and visit questions."

3. **Therapy appointment prep:** "I have therapy on Friday and want to track my mood and anxiety across the week. Monday was okay (3/10 anxiety), Tuesday was rough (8/10, couldn't focus at work), Wednesday was better after exercise, Thursday I had trouble sleeping. I also want to discuss whether my current coping strategies are helping. Make a simple weekly note."
