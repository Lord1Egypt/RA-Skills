---
name: ai-health
description: AI-driven health analysis system including comprehensive analysis, risk prediction, intelligent Q&A, and report generation.
argument-hint: <operation_type(analysis/prediction/chat/report/status) [target] [options]>
allowed-tools: Read, Write
schema: ai-health/schema.json
---

# AI Health Assistant Skill

AI-driven comprehensive health analysis system providing intelligent health insights, risk prediction, and personalized recommendations.

## Core Flow

```
User Input -> Parse Operation Type -> [analyze] Read Data -> Multi-dimensional Analysis -> Generate Insights -> Output Report
                              -> [predict] Extract Risk Factors -> Calculate Risk -> Generate Recommendations
                              -> [chat] Parse Query -> Retrieve Data -> Analyze -> Reply
                              -> [report] Generate HTML Report
                              -> [status] Display Configuration Status
```

## Step 1: Parse Operation Type

| Input Keywords | Operation |
|----------------|-----------|
| analyze | analyze |
| predict | predict |
| chat | chat |
| report | report |
| status | status |

## Step 2: AI Comprehensive Analysis (analyze)

### Analysis Process

```
1. Read AI configuration and user profile
2. Read all health data sources
   - Basic indicators (profile.json)
   - Lifestyle data
   - Mental health data
   - Medical history data
3. Execute multi-dimensional analysis
   - Correlation analysis (Pearson, Spearman)
   - Trend analysis (linear regression, moving average)
   - Anomaly detection (CUSUM, Z-score)
4. Generate personalized recommendations (Level 1-3)
5. Output text report
6. Generate HTML report (optional)
```

### Time Range Parameters

| Parameter | Description |
|-----------|-------------|
| all | All data |
| last_month | Last month |
| last_quarter | Last quarter (default) |
| last_year | Last year |
| YYYY-MM-DD | From specified date to present |

## Step 3: Health Risk Prediction (predict)

### Supported Risk Types

| Type | Description | Model |
|------|-------------|-------|
| hypertension | Hypertension risk (10-year) | Framingham |
| diabetes | Diabetes risk (10-year) | ADA |
| cardiovascular | Cardiovascular risk (10-year) | Framingham |
| all | All risk predictions | Combined |

### Risk Calculation Process

```
1. Read user profile and related health data
2. Extract risk factors (age, BMI, blood pressure, blood sugar, family history, etc.)
3. Apply risk prediction models
4. Calculate risk probability and grade
5. Identify modifiable risk factors
6. Generate prevention recommendations
```

## Step 4: Intelligent Health Q&A (chat)

### Supported Query Types

**Data Query:**
```
What is my average sleep time?
What is my recent weight?
```

**Trend Analysis:**
```
How has my weight changed recently?
Has my sleep quality improved?
```

**Correlation Query:**
```
How does exercise affect my sleep?
Is there a relationship between diet and my weight?
```

**Recommendation Query:**
```
How can I improve my sleep quality?
Should I reduce my hypertension risk?
```

## Step 5: Generate AI Report (report)

### Report Types

| Type | Description |
|------|-------------|
| comprehensive | Comprehensive health report (default) |
| quick_summary | Quick summary |
| risk_assessment | Risk assessment report |
| trend_analysis | Trend analysis report |

### Report Generation Process

```
1. Read user data and AI configuration
2. Execute analysis based on report type
3. Call report generation script
4. Save to data/ai-reports/ directory
5. Display report file path
```

## Execution Instructions

```
1. Parse operation type and parameters
2. [analyze] Load data -> Multi-dimensional analysis -> Generate insights -> Output
3. [predict] Extract risk factors -> Apply models -> Calculate risk -> Output
4. [chat] Parse query -> Retrieve data -> Analyze and reply
5. [report] Determine type -> Generate HTML -> Save
6. [status] Read configuration -> Display status
```

## Example Interactions

### Comprehensive Analysis
```
User: AI analysis

Output:
AI Health Analysis Report
━━━━━━━━━━━━━━━━━━━━━━━━━━
Health Index: 72/100 (Good)
Improving: Sleep quality, Exercise level
Needs Attention: BMI, Medication adherence

🎯 Risk Prediction:
Hypertension Risk: 32% (Moderate Risk)
Diabetes Risk: 18% (Low Risk)
```

### Risk Prediction
```
User: AI predict hypertension risk

Output:
🎯 Hypertension Risk Prediction Report
Risk Probability: 32%
Risk Grade: 🟡 Moderate Risk

Major Risk Factors:
1. BMI: 24.9 (Approaching overweight)
2. Systolic BP: 128 mmHg (High-normal)
```

### Intelligent Q&A
```
User: What is my average sleep time?

Output:
Based on records from the past 90 days,
Your average sleep time is 6.8 hours.

Recommendation: Aim for 7-9 hours of sleep
```
