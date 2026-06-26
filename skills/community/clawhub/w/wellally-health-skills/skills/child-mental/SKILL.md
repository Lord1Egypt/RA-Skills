---
name: child-mental
description: Child mental health screening, mood tracking, behavior assessment, anxiety and ADHD screening. Use when user mentions child emotions, behavior, attention, mood swings, or mental concerns.
argument-hint: <operation_type: record/mood/behavior/anxiety/adhd/report/history, e.g.: record happy mood, mood happy, behavior, anxiety, adhd>
allowed-tools: Read, Write
schema: child-mental/schema.json
---

# Child Mental Health Skill

Child mental health assessment, mood tracking and behavior problem screening, providing preliminary assessment for anxiety, attention and other areas.

## Core Flow

```
User Input → Identify Operation Type → Read Child Information → Determine Assessment Items by Age → Generate Assessment Report → Save Data
```

## Step 1: Parse User Input

### Operation Type Mapping

| Input | action | Description |
|------|--------|-------------|
| record | record | Log comprehensive assessment |
| mood | mood | Mood tracking |
| behavior | behavior | Behavior assessment |
| anxiety | anxiety | Anxiety screening |
| adhd | adhd | Attention screening (ADHD) |
| report | report | Comprehensive report |
| history | history | Historical records |

### Mood Keyword Mapping

| Input | mood |
|------|------|
| happy | happy |
| calm | calm |
| sad | sad |
| angry | angry |
| excited | excited |
| anxious | anxious |

## Step 2: Check Information Completeness

### Required (prompt to set if missing):
- Child name (from data/profile.json)
- Birth date (from data/profile.json)
- Gender (from data/profile.json)

## Step 3: Determine Assessment Items by Age

| Age | Assessment Focus |
|-----|------------------|
| 0-3 years | Emotional response, attachment, behavior patterns |
| 3-6 years | Emotional expression, social behavior, attention |
| 6-12 years | Emotional regulation, learning behavior, peer relationships |
| 12-18 years | Emotional management, self-awareness, stress coping |

## Step 4: Generate Assessment Report

### Mood State Assessment

| Overall Mood | Condition |
|--------------|------------|
| Stable | Appropriate emotional responses, self-regulation |
| Fluctuating | Rapid mood changes, unpredictable |
| Unstable | Difficulty self-soothing, frequent crying |

### Behavior Assessment Grading

| Assessment Result | Condition |
|-------------------|-----------|
| Normal | All behavior domains age-appropriate |
| Mild problems | 1-2 domains with mild difficulties |
| Significant problems | Multiple domains with significant difficulties |

### Normal Assessment Report Example:
```
Mental health assessment saved

Assessment Information:
Child: Xiaoming
Age: 2 years 5 months
Assessment date: January 14, 2025

Mood State:
  Overall mood: Stable
  Emotional expression: Rich and appropriate
  Emotional regulation: Good

Behavior Assessment:
  Overall behavior: Normal
  Activity level: Moderate
  Attention: Good
  Compliance: Good
  Aggressive behavior: None

Comprehensive Assessment:
  Normal mental development

Recommendations:
  Continue providing loving environment
  More companionship and interaction
  Establish regular daily routine

Data saved
```

## Step 5: Save Data

Save to `data/child-mental-tracker.json`, including:
- child_profile: Child basic information
- assessments: Assessment records
- mood_tracking: Mood tracking
- behavior_tracking: Behavior tracking
- statistics: Statistical information

## Anxiety Screening Items

### Separation Anxiety
- Crying when separated from parents
- Worrying parents won't return
- Refusing to go to school
- Physical symptoms when leaving home

### Social Anxiety
- Fear of unfamiliar environments
- Reluctance to interact with others
- Fear of being watched
- Avoiding social situations

### Generalized Anxiety
- Excessive worrying
- Muscle tension
- Sleep difficulties
- Easy fatigue

## ADHD Screening Scoring Standard

| Total Score | Assessment |
|-------------|------------|
| <20 points | Unlikely ADHD |
| 20-30 points | Possible ADHD, recommend assessment |
| >30 points | Highly suspected ADHD, recommend professional assessment |

## Mental Health Focus by Age

### 0-3 Years (Infancy)
- Focus: Attachment, emotional response, behavior patterns
- Common issues: Separation anxiety, sleep problems, feeding problems

### 3-6 Years (Preschool)
- Focus: Emotional expression, social behavior, self-care skills
- Common issues: Aggressive behavior, phobias, language problems

### 6-12 Years (School Age)
- Focus: Learning behavior, peer relationships, self-awareness
- Common issues: Learning difficulties, ADHD, anxiety

### 12-18 Years (Adolescence)
- Focus: Emotional management, self-identity, stress coping
- Common issues: Depression, anxiety, behavior problems

## Execution Instructions

1. Read data/profile.json for child information
2. Determine assessment items based on age and operation type
3. Generate assessment report
4. Save to data/child-mental-tracker.json

## Medical Safety Principles

### Safety Boundaries
- No mental disorder diagnosis
- No psychiatric medication recommendations
- No psychotherapy provision
- No crisis situation handling

### System Can
- Mental health assessment recording
- Symptom screening reference
- Mood tracking
- Trend analysis
- Medical consultation recommendations

## Important Notice

This system is for mental health recording and screening reference only, **cannot replace professional psychological assessment and diagnosis**.

If following conditions occur, **seek immediate professional help**:
- Thoughts or behaviors of harming self or others
- Extreme emotional outbursts
- Complete non-compliance with instructions
- Complete social withdrawal
- Severe changes in sleep or appetite
- Hallucinations or delusions

For emergencies, **immediately call 120 or go to nearest hospital**.
