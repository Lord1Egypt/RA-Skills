---
name: male-menopause
description: Male menopause (hypogonadism) management including symptom tracking, testosterone monitoring, and TRT treatment records
argument-hint: <operation_type, e.g.: symptom decreased libido/testosterone 7.5/adam/trt start gel>
allowed-tools: Read, Write
schema: male-menopause/schema.json
---

# Male Menopause Management Skill

Male menopause (hypogonadism) tracking and management, including symptom assessment, testosterone monitoring, and TRT treatment records.

## Core Flow

```
User Input → Identify Operation Type → Parse Information → Check Completeness → Generate JSON → Save Data
                                     |
                              [Ask when information insufficient]
```

## Step 1: Parse User Input

### Operation Type Recognition

| Input Keywords | Operation |
|----------------|-----------|
| symptom | Record symptoms |
| testosterone | Record testosterone levels |
| adam | ADAM questionnaire assessment |
| trt | TRT treatment record |
| monitor | TRT monitoring indicators |
| status | View status |
| diagnosis | View diagnosis |

### Symptom Type Recognition

| Category | Keywords |
|----------|----------|
| Sexual symptoms | libido, erectile, morning erection |
| Physical symptoms | fatigue, weak, muscle, fat |
| Psychological symptoms | mood, depression, memory, concentration |

### Symptom Severity Recognition

| Severity | Keywords |
|----------|----------|
| Mild | mild |
| Moderate | moderate |
| Severe | severe |

### Testosterone Recognition

| Keywords | Extract |
|----------|---------|
| testosterone, total testosterone | Value + nmol/L |
| morning, 09:00, am | Measurement time |

## Step 2: Check Information Completeness

### Symptom Record (symptom)
- **Required**: Symptom type
- **Recommended**: Severity
- **Optional**: Duration, impact description

### Testosterone Test (testosterone)
- **Required**: Testosterone value
- **Recommended**: Measurement time
- **Optional**: Free testosterone, SHBG

### TRT Treatment (trt)
- **Required**: Operation type (start/stop/record)
- **Recommended**: Medication type, dosage
- **Optional**: Effectiveness, side effects

## Step 3: Interactive Prompts (If Needed)

### Question Scenarios

#### Scenario A: Symptom Record Missing Specific Information
```
What specific symptoms do you have?
For example: decreased libido, erectile dysfunction, easy fatigue, low mood, etc.
```

#### Scenario B: Missing Symptom Severity
```
How much do these symptoms affect your life?
• Mild: Occasional, doesn't affect life
• Moderate: Frequent, affects quality of life
• Severe: Persistent, severely affects life
```

## Step 4: Generate JSON

### Symptom Data Structure

```json
{
  "record_type": "symptom",
  "date": "2025-12-01",
  "symptoms": {
    "sexual": {
      "libido": {
        "present": true,
        "severity": "moderate",
        "impact": "noticeable"
      },
      "erectile_function": {
        "present": true,
        "severity": "mild",
        "morning_erection": "reduced"
      }
    },
    "physical": {
      "fatigue": {
        "present": true,
        "severity": "moderate",
        "impact_on_activities": "some"
      },
      "muscle_mass": {
        "present": true,
        "severity": "mild",
        "changes": "slight_decrease"
      }
    },
    "psychological": {
      "mood": {
        "present": true,
        "symptoms": ["depressed", "irritability"],
        "severity": "mild"
      }
    }
  }
}
```

### Testosterone Data Structure

```json
{
  "record_type": "testosterone_test",
  "date": "2025-06-15",
  "time": "09:00",
  "testosterone_levels": {
    "total_testosterone": {
      "value": 7.5,
      "reference": "10-35",
      "unit": "nmol/L",
      "result": "low",
      "confirmed": true,
      "repeat_count": 2
    },
    "free_testosterone": {
      "value": 0.18,
      "reference": "0.22-0.65",
      "unit": "nmol/L",
      "result": "low"
    },
    "shbg": {
      "value": 45,
      "reference": "20-50",
      "unit": "nmol/L",
      "result": "normal"
    }
  }
}
```

### ADAM Questionnaire Data Structure

```json
{
  "record_type": "adam_questionnaire",
  "date": "2025-06-20",
  "questions": [
    {"q1": "有性欲减退吗？", "answer": true, "score": 1},
    {"q2": "感到体力下降吗？", "answer": true, "score": 1},
    {"q3": "体力减退了吗？", "answer": true, "score": 1},
    {"q4": "身高变矮了吗？", "answer": false, "score": 0},
    {"q5": "生活乐趣减少了吗？", "answer": true, "score": 1},
    {"q6": "感到悲伤或脾气暴躁吗？", "answer": true, "score": 1},
    {"q7": "勃起能力下降了吗？", "answer": true, "score": 1},
    {"q8": "最近运动能力下降了吗？", "answer": false, "score": 0},
    {"q9": "饭后容易犯困吗？", "answer": false, "score": 0},
    {"q10": "最近工作表现下降了吗？", "answer": false, "score": 0}
  ],
  "total_score": 7,
  "positive": true,
  "interpretation": "Suggests possible male menopause"
}
```

Complete schema definition: see [schema.json](schema.json).

## Step 5: Save Data

1. Generate record ID: `andropause_YYYYMMDD_XXX`
2. Save to `data/更年期记录/YYYY-MM/YYYY-MM-DD_症状记录.json`
3. Update `data/andropause-tracker.json`

## Testosterone Level Assessment Standards

| Total Testosterone (nmol/L) | Assessment |
|----------------------------|------------|
| >= 10 | Normal |
| 8-10 | Possible hypogonadism |
| < 8 | Confirmed hypogonadism (repeat testing required)

**Testing Requirements:**
- Morning measurement (8-11am) most accurate
- At least 2 tests to confirm
- Interval > 1 week between tests

## ADAM Questionnaire Scoring Standards

**Positive Criteria:**
- Question 1 or 7 positive + any other question positive
- Or >= 3 questions positive

**Result Interpretation:**
- 0-2 questions "yes": Negative
- >= 3 questions "yes": Positive

## Hypogonadism Diagnostic Standards

- **Symptoms**: Typical symptoms present
- **Testosterone**: Total testosterone < 8 nmol/L (repeat testing)
- **Or**: Total testosterone 8-12 nmol/L + significant symptoms

**Diagnostic Criteria:**
- Morning (8-11am) testing
- At least 2 tests to confirm
- Exclude other diseases

## Execution Instructions

```
1. Identify operation type
2. Parse input parameters, extract all available information
3. Check required fields, ask user if missing
4. Judge results based on assessment standards
5. Generate JSON compliant with schema.json
6. Save to appropriate file path
7. Confirm save to user and display summary and recommendations
```

## Example Interactions

### Example 1: Record Symptoms
```
User: 更年期症状 性欲减退 容易疲劳
AI: 请问这些症状对您的生活影响有多大？
    轻度：偶尔有，不影响生活
    中度：经常有，影响生活质量
    重度：持续存在，严重影响生活

User: 中度吧
AI: ✅ 症状已记录

    Sexual symptoms: Decreased libido (moderate)
    Physical symptoms: Easy fatigue (moderate)

    Recommendation: Suggest testosterone level testing, complete ADAM questionnaire assessment

    Saved to: data/更年期记录/2025-12/2025-12-01_症状记录.json
```

### Example 2: Record Testosterone
```
User: 睾酮 7.5 早晨9点
AI: ✅ 睾酮检测已记录

    Total testosterone: 7.5 nmol/L ⚠️ (reference: 10-35)
    Free testosterone: 0.18 nmol/L ⚠️ (reference: 0.22-0.65)
    Measurement time: 09:00 ✓ (morning)

    Diagnosis: Hypogonadism (confirmed)

    TRT treatment recommendation: Symptoms + low testosterone = TRT treatment indication
    Suggest consulting endocrinology or urology for evaluation

    Saved to: data/更年期记录/2025-06/2025-06-15_睾酮检测.json
```

### Example 3: ADAM Questionnaire
```
User: ADAM问卷
AI: 请回答以下10个问题 (是/否):

    1. 有性欲减退吗？
    2. 感到体力下降吗？
    3. 体力减退了吗？
    4. 身高变矮了吗？
    5. 生活乐趣减少了吗？
    6. 感到悲伤或脾气暴躁吗？
    7. 勃起能力下降了吗？
    8. 最近运动能力下降了吗？
    9. 饭后容易犯困吗？
    10. 最近工作表现下降了吗？

    [User answers each question...]

    ✅ ADAM问卷已完成

    Total score: 7/10 questions positive
    Result: Positive ⚠️

    ADAM questionnaire positive, suggests possible male menopause (hypogonadism).

    Recommendation: Test testosterone levels, comprehensive assessment combining symptoms and testosterone

    Saved to: data/更年期记录/2025-06/2025-06-20_ADAM问卷.json
```

## Important Notice

- This system is for menopause health tracking only, cannot replace professional medical advice
- TRT treatment must be under doctor supervision
- Regular monitoring of side effects is very important
- Symptoms + low testosterone required for diagnosis
- Need to exclude other diseases

## Seek Immediate Medical Care For

- Hct > 54%
- PSA rapid elevation
- Breast lump
- Lower limb swelling and pain
