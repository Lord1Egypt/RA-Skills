# hypertension Skill Examples

## 1. Blood Pressure Recording

### Example 1: Basic BP Record
```
User: record 135/85

AI: Blood pressure measurement recorded
Time: 2025-01-02 08:00
Systolic: 135 mmHg
Diastolic: 85 mmHg
Classification: High-Normal

Target: <130/80 mmHg
Status: Not on target (elevated systolic)

Recommendation: Reduce sodium intake, exercise regularly, monitor regularly
```

### Example 2: BP Record with Pulse
```
User: record 130/80 pulse 78

AI: Blood pressure measurement recorded
Time: 2025-01-02 08:00
Systolic: 130 mmHg
Diastolic: 80 mmHg
Pulse: 78 bpm
Classification: High-Normal

Status: Approaching target
```

### Example 3: BP Record with Detailed Parameters
```
User: record 140/90 pulse 82 morning sitting left arm

AI: Blood pressure measurement recorded
Time: 2025-01-02 08:00
Systolic: 140 mmHg
Diastolic: 90 mmHg
Pulse: 82 bpm
Measurement Time: Morning
Position: Sitting
Arm: Left
Classification: Grade 1 Hypertension

Status: Not on target, recommend medical evaluation
```

## 2. View Blood Pressure Trends

### Example 4: BP Trend Analysis
```
User: trend

AI: Blood pressure trend analysis (past 7 days)
━━━━━━━━━━━━━━━━━━━━━━━━━━
Average BP: 132/83 mmHg
Morning average: 135/85 mmHg
Evening average: 128/80 mmHg

Circadian Rhythm: Dipper (normal)
Achievement Rate: 71.4%

Trend: BP control stable, morning BP slightly elevated

Recommendation: Continue monitoring, pay attention to morning BP control
```

### Example 5: 30-Day Trend
```
User: trend 30days

AI: Blood pressure trend analysis (past 30 days)
━━━━━━━━━━━━━━━━━━━━━━━━━━
Average BP: 128/81 mmHg
Achievement Rate: 73.3%

Trend: BP control improved, continue current treatment plan
```

## 3. Calculate Average BP

### Example 6: Calculate Average
```
User: average

AI: Blood pressure average (past 7 days)
━━━━━━━━━━━━━━━━━━━━━━━━━━
Home BP Average: 132/83 mmHg
Morning Average: 135/85 mmHg
Evening Average: 128/80 mmHg
Days on Target: 5/7 days

Evaluation: Control approaching target, keep working
```

## 4. View History Records

### Example 7: View History
```
User: history

AI: Blood pressure measurement history (last 10)
━━━━━━━━━━━━━━━━━━━━━━━━━━
Date        Time    Sys/Dia    Pulse  Target
2025-01-08  08:00   128/80     76     ✓
2025-01-08  20:00   125/78     72     ✓
2025-01-07  08:00   135/85     78     ✗
2025-01-07  20:00   130/82     75     ✗
...
```

## 5. View Achievement Status

### Example 8: Achievement Overview
```
User: status

AI: Blood Pressure Achievement Report
━━━━━━━━━━━━━━━━━━━━━━━━━━
BP Target: <130/80 mmHg

Past 7 days:
- Average BP: 132/83 mmHg
- Days on Target: 5/7 days (71.4%)
- Achievement Rate: 71.4%

Past 30 days:
- Average BP: 128/81 mmHg
- Days on Target: 22/30 days (73.3%)
- Achievement Rate: 73.3%

Control Evaluation: BP control approaching target, keep working
```

## 6. Cardiovascular Risk Assessment

### Example 9: Risk Assessment
```
User: risk

AI: Cardiovascular Risk Assessment
━━━━━━━━━━━━━━━━━━━━━━━━━━
10-Year ASCVD Risk: 12.5%
Risk Level: High Risk

Major Risk Factors:
- Hypertension (currently poorly controlled)
- Age > 55 years
- Elevated total cholesterol

Recommendations:
1. Strict BP control to target value
2. Consider statin therapy
3. Low-salt diet, regular exercise
4. Quit smoking, limit alcohol

Recommendation: Seek medical attention soon, consult doctor for treatment adjustment
```

## 7. Target Organ Assessment

### Example 10: Heart Assessment
```
User: heart echo normal

AI: Heart assessment recorded
Exam Type: Echocardiogram
Result: Normal
Left Ventricular Hypertrophy: None

Date: 2025-06-20
```

### Example 11: Kidney Assessment
```
User: kidney uacr 15 egfr 90

AI: Kidney assessment recorded
UACR: 15 mg/g (<30, normal)
eGFR: 90 ml/min/1.73m² (normal)
Microalbuminuria: Negative

Evaluation: Normal kidney function, no evidence of target organ damage
```

### Example 12: Retina Assessment
```
User: retina grade-0

AI: Retina assessment recorded
Grade: Grade 0
Result: No retinopathy

Exam Date: 2025-06-20
Next Exam: 2026-06-20
```

## 8. View BP Targets

### Example 13: View Targets
```
User: target

AI: Blood Pressure Management Targets
━━━━━━━━━━━━━━━━━━━━━━━━━━
Systolic Target: <130 mmHg
Diastolic Target: <80 mmHg

Target Basis: General adult standard

Recommendations:
- Limit sodium intake (<5g/day)
- Regular aerobic exercise (150 min/week)
- Control weight (BMI <24)
- Quit smoking, limit alcohol
```
