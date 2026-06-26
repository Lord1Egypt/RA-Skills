---
name: child-vaccine
description: Manage child vaccination schedules, track vaccinations, and get reminders for upcoming or overdue vaccines. Use when user mentions vaccines, immunizations, or vaccination records.
argument-hint: <operation_type: record/schedule/due/overdue/completed/reaction/reminder, e.g.: record Hep B dose 1 completed, schedule, due, reminder>
allowed-tools: Read, Write
schema: child-vaccine/schema.json
---

# Child Vaccination Skill

Child vaccination schedule management, including national immunization program and optional vaccines, providing vaccination reminders and missed dose warnings.

## Core Flow

```
User Input → Identify Operation Type → Read Child Information → Generate Vaccination Schedule/Record → Save Data
```

## Step 1: Parse User Input

### Operation Type Mapping

| Input | action | Description |
|------|--------|-------------|
| record | record | Log vaccination |
| schedule | schedule | View vaccination schedule |
| due | due | View upcoming vaccinations |
| overdue | overdue | View missed vaccinations |
| completed | completed | View completed vaccinations |
| reaction | reaction | Log adverse reactions |
| reminder | reminder | Vaccination reminders |

### Vaccine Name Mapping

| Input | vaccine_name | category |
|------|--------------|----------|
| Hep B, 乙肝, 乙肝疫苗 | 乙肝疫苗 | class_1 |
| BCG, 卡介苗 | 卡介苗 | class_1 |
| Polio, 脊灰, 小儿麻痹症 | 脊灰疫苗 | class_1 |
| DTP, 百白破 | 百白破疫苗 | class_1 |
| MMR, 麻腮风 | 麻腮风疫苗 | class_1 |
| JE, 乙脑 | 乙脑疫苗 | class_1 |
| Meningococcal A, 流脑, 流脑A群 | 流脑A群疫苗 | class_1 |
| Meningococcal A+C, 流脑A+C | 流脑A+C群疫苗 | class_1 |
| Hep A, 甲肝 | 甲肝疫苗 | class_1 |
| Varicella, 水痘 | 水痘疫苗 | class_2 |
| PCV13, 肺炎, 13价肺炎 | 13价肺炎疫苗 | class_2 |
| Pentavalent, 五联疫苗 | 五联疫苗 | class_2 |
| Rotavirus, 轮状病毒 | 轮状病毒疫苗 | class_2 |
| Flu, 流感, 流感疫苗 | 流感疫苗 | class_2 |
| Hib | Hib疫苗 | class_2 |
| EV71, 手足口 | EV71疫苗 | class_2 |

### Dose Recognition

| Input | dose |
|------|------|
| dose 1, 第1针, 1针, 第一针 | 第1针 |
| dose 2, 第2针, 2针, 第二针 | 第2针 |
| dose 3, 第3针, 3针, 第三针 | 第3针 |
| dose 4, 第4针, 4针, 第四针 | 第4针 |
| dose 5, 第5针, 5针, 第五针 | 第5针 |
| booster, 加强针, 加强 | 加强针 |

### Status Recognition

| Input | status |
|------|--------|
| completed, 已完成, 已接种 | completed |
| scheduled, 计划, 预约 | scheduled |
| missed, 漏种 | missed |

## Step 2: Check Information Completeness

### record Operation Required:
- Vaccine name
- Dose
- Vaccination status (defaults to completed)
- Vaccination date (defaults to today)

## Step 3: Determine Vaccination Schedule by Age

### National Immunization Program Vaccines (Class 1)

| Age | Vaccines |
|-----|----------|
| Birth | Hep B (dose 1), BCG |
| 1 month | Hep B (dose 2) |
| 2 months | Polio (dose 1) |
| 3 months | Polio (dose 2), DTP (dose 1) |
| 4 months | Polio (dose 3), DTP (dose 2) |
| 5 months | DTP (dose 3) |
| 6 months | Hep B (dose 3), Meningococcal A (dose 1) |
| 8 months | MMR (dose 1), JE (dose 1) |
| 9 months | Meningococcal A (dose 2) |
| 18 months | DTP (dose 4), MMR (dose 2), Hep A |
| 2 years | JE (dose 2) |
| 3 years | Meningococcal A+C (dose 1) |
| 4 years | Polio (dose 4) |
| 6 years | DTP (dose 5), Meningococcal A+C (dose 2) |

### Optional Vaccines (Class 2 - Self-pay, Voluntary)

| Vaccine | Vaccination Time |
|---------|------------------|
| Varicella | 12 months, 4 years |
| PCV13 | 2, 4, 6 months + 12-15 months |
| Pentavalent | 2, 3, 4, 18 months |
| Rotavirus | 2, 3 months |
| Influenza | From 6 months, annually |
| Hib | 2, 3, 4, 18 months |
| EV71 | 6 months - 5 years |

## Step 4: Generate Vaccination Report

### Record Vaccination Example:
```
Vaccination recorded

Vaccine Information:
  Vaccine: Hepatitis B
  Dose: Dose 1
  Vaccination date: January 1, 2020
  Category: Class 1 vaccine

Vaccination Progress:
  Completed: 1/3 doses

Next Vaccination:
  February 1, 2020 (1 month later)
  Hepatitis B Dose 2

Important Notice:
This system is for vaccination recording only, cannot replace professional medical advice.

All vaccinations should be done at vaccination clinics.
Inform doctor of child's health status before vaccination.

Data saved
```

### View Vaccination Schedule Example:
```
Child Vaccination Schedule

Child Information:
  Name: Xiaoming
  Birth date: January 1, 2020
  Current age: 5 years 5 months

Class 1 Vaccination Schedule:

  2020-01-01 (Completed)
    Hepatitis B Dose 1
    BCG Dose 1

  2020-02-01 (Completed)
    Hepatitis B Dose 2

...

  2025-08-01 (42 days away)
    Meningococcal A Dose 1

Class 2 Vaccines (Recommended):

  Varicella
    12 months, 4 years
    Recommended

  PCV13
    2, 4, 6 months + 12-15 months
    Highly recommended

Data saved
```

## Step 5: Save Data

Save to `data/child-vaccine-tracker.json`, including:
- child_profile: Child basic information
- scheduled_vaccines: Scheduled vaccine list
- upcoming: Upcoming vaccinations
- overdue: Overdue vaccinations
- completed: Completed vaccinations
- reactions: Adverse reaction records
- statistics: Statistical information

## Adverse Reaction Grading

| Severity | Description |
|----------|-------------|
| Mild | Local redness/swelling, low fever, mild irritability |
| Moderate | Fever > 39, significant discomfort, affects activity |
| Severe | Severe allergic reaction, seizures, requires medical care |

## Vaccination Reminder Rules

| Advance Time | Reminder Type |
|--------------|---------------|
| Within 7 days | Upcoming vaccination |
| Overdue | Overdue vaccination |
| Severely overdue > 30 days | Urgent reminder |

## Execution Instructions

1. Read data/profile.json for child information
2. Calculate vaccination schedule based on birth date
3. Generate vaccination report or record vaccination
4. Save to data/child-vaccine-tracker.json

## Medical Safety Principles

### Safety Boundaries
- No specific vaccine brand recommendations
- No vaccination contraindication judgment
- No severe adverse reaction handling
- No substitute for vaccination clinics

### System Can
- Vaccination schedule management
- Vaccination reminders
- Missed dose warnings
- Adverse reaction recording

## Important Notice

This system is for vaccination recording and schedule management only, **cannot replace professional medical advice**.

All vaccinations should be done at vaccination clinics. **Inform doctor of child's health status** before vaccination.

If adverse reactions occur, **consult doctor promptly**.
