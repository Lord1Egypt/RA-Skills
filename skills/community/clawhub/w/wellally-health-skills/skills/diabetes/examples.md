# diabetes Skill Examples

## 1. Glucose Recording

### Example 1: Fasting Glucose Record
```
User: record fasting 6.5

AI: Blood glucose measurement recorded
Time: 2025-06-20 07:00
Type: Fasting blood glucose
Value: 6.5 mmol/L
Status: Within target range (4.4-7.0)

Recommendation: Continue maintaining good blood glucose control
```

### Example 2: Postprandial Glucose Record
```
User: record postprandial 8.2

AI: Blood glucose measurement recorded
Time: 2025-06-20 12:30
Type: 2-hour post-meal blood glucose
Value: 8.2 mmol/L
Status: Within target range (<10.0)

Recommendation: Post-meal blood glucose control is good
```

### Example 3: Bedtime Glucose Record
```
User: record bedtime 7.2

AI: Blood glucose measurement recorded
Time: 2025-06-20 22:00
Type: Bedtime blood glucose
Value: 7.2 mmol/L
Status: Within target range (6.0-9.0)

Recommendation: Bedtime blood glucose control is good, sleep well
```

## 2. HbA1c Recording

### Example 4: HbA1c Record
```
User: hba1c 6.8

AI: HbA1c test result recorded
Value: 6.8%
Target: <7.0%
Status: On target

Change from last: -0.3% (improved)

Recommendation: Test HbA1c every 3 months
```

### Example 5: HbA1c with Date
```
User: hba1c 7.2 2025-06-15

AI: HbA1c test result recorded
Date: 2025-06-15
Value: 7.2%
Target: <7.0%
Status: Not on target

Change from last: +0.4%

Recommendation: Blood glucose control needs improvement, consult doctor for treatment adjustment
```

## 3. Hypoglycemia Events

### Example 6: Mild Hypoglycemia
```
User: hypo 3.4 sweating

AI: Hypoglycemia event recorded
Time: 2025-06-18 15:30
Blood glucose: 3.4 mmol/L
Severity: Level 1 (mild)
Symptoms: Sweating

Hypoglycemia Management Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Immediately take 15g fast-acting glucose
   - 3-5 glucose tablets
   - 150ml juice or sugary drink

2. Re-check after 15 minutes

3. If still below 3.9 mmol/L, repeat step 1
```

### Example 7: Moderate Hypoglycemia
```
User: hypo 2.8 confusion took glucose

AI: Hypoglycemia event recorded
Time: 2025-06-18 16:00
Blood glucose: 2.8 mmol/L
Severity: Level 2 (moderate)
Symptoms: Confusion
Treatment: Took glucose

Status: Resolved

Recommendation: Analyze hypoglycemia cause, adjust medication or diet
```

## 4. Complications Screening

### Example 8: Retinopathy Screening
```
User: screening retina none

AI: Retinopathy screening recorded
Result: No retinopathy
Exam date: 2025-06-20
Next exam: 2026-06-20
```

### Example 9: Nephropathy Screening
```
User: screening kidney uacr 45 egfr 78

AI: Diabetic nephropathy screening recorded
Result: Microalbuminuria
UACR: 45 mg/g (30-300)
eGFR: 78 ml/min/1.73m²
CKD Stage: G2A2

Recommendation: Re-test every 3-6 months, control blood pressure and blood glucose
```

### Example 10: Neuropathy Screening
```
User: screening nerve normal

AI: Diabetic neuropathy screening recorded
Result: Normal
10g monofilament test: Normal
Exam date: 2025-06-20
```

### Example 11: Diabetic Foot Screening
```
User: screening foot normal

AI: Diabetic foot screening recorded
Result: Normal/Low risk
Dorsalis pedis pulse: Present
Ulcer: None
Wagner Grade: Grade 0
```

## 5. View Achievement Status

### Example 12: Achievement Overview
```
User: achievement

AI: Blood Glucose Achievement Report
━━━━━━━━━━━━━━━━━━━━━━━━━━
HbA1c: 6.8% (target <7.0%) ✓ On target

Past 7 days glucose:
- Fasting: Average 6.2 mmol/L (achievement rate 85.7%)
- Post-meal 2h: Average 8.5 mmol/L (achievement rate 71.4%)
- Bedtime: Average 7.1 mmol/L (achievement rate 100%)

TIR: 72% (target >70%) ✓ On target
Hypoglycemia events: 1 (level 1)

Control Evaluation: Good blood glucose control, continue
```

## 6. TIR Analysis

### Example 13: View TIR
```
User: tir

AI: Glucose Time in Range Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━
Analysis Period: Past 14 days

Target Range: 3.9-10.0 mmol/L
TIR: 72% ✓ On target (target >70%)
Above Range: 18% (<10%)
Below Range: 10% (<4%)

Time Distribution:
- In Range: 121 hours
- Above Range: 30 hours
- Below Range: 17 hours

Evaluation: TIR on target, low glucose time slightly high, pay attention to prevention
```

## 7. View Glucose Targets

### Example 14: View Targets
```
User: target

AI: Blood Glucose Management Targets
━━━━━━━━━━━━━━━━━━━━━━━━━━
Patient Type: General Adult

Blood Glucose Targets:
- Fasting/Pre-meal: 4.4-7.0 mmol/L
- 2-hour Post-meal: <10.0 mmol/L
- Bedtime: 6.0-9.0 mmol/L
- HbA1c: <7.0%
- TIR: >70%

Individualization Basis: General adult type 2 diabetes standard target
```

## 8. View Trends

### Example 15: Glucose Trends
```
User: trend

AI: Blood Glucose Trend Analysis (Past 7 Days)
━━━━━━━━━━━━━━━━━━━━━━━━━━
Fasting Glucose: Average 6.2 mmol/L (stable)
Post-meal Glucose: Average 8.5 mmol/L (stable)

Daily Fluctuation: Normal
Hypoglycemia Events: 1 (mild)

Trend: Blood glucose control stable, continue current treatment plan
```
