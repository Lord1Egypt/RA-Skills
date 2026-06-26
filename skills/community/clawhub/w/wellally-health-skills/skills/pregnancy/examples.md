# Pregnancy Skill Examples

## I. Start Pregnancy Record (start)

### Example 1: Basic Start
```
User: /pregnancy start 2025-01-01

System:
Pregnancy record created

Pregnancy Information:
Last Menstrual Period: January 1, 2025
Due Date: October 8, 2025
Current Week: 0 weeks
Trimester: First Trimester

Due Date Confidence: Medium (calculated based on LMP)

Next Prenatal Checkup:
12 weeks NT scan - March 25, 2025 (84 days remaining)
Preparation: Full bladder required

Prenatal Checkup Plan Overview:
12 weeks: NT scan
16 weeks: Triple Screen/NIPT
20 weeks: Anatomy Scan
24 weeks: Glucose Tolerance Test
28 weeks: Routine Checkup
32-36 weeks: Every 2 weeks
37-40 weeks: Every week

Nutrition Recommendations:
• Folic acid: 400-800 mcg/day (3 months before pregnancy to first trimester)
• Iron: Supplement in second and third trimesters
• Calcium: 1000-1200 mg/day
• DHA: 200-300 mg/day
```

### Example 2: Ultrasound Correction
```
User: /pregnancy start 2025-01-01 ultrasound May 15

System:
Pregnancy record created

Pregnancy Information:
Last Menstrual Period: January 1, 2025
Due Date: October 8, 2025
Ultrasound Correction: May 15, 2025
Adjusted Due Date: October 10, 2025

Due Date Confidence: High (based on ultrasound correction)
```

## II. Record Prenatal Checkup (checkup)

### Example 3: Normal NT Scan
```
User: /pregnancy checkup week 12 NT normal

System:
Prenatal checkup record updated

Checkup Information:
Gestational Week: 12 weeks
Check Type: NT scan
Date: March 25, 2025
Result: Normal (NT value 1.8mm)

This checkup completed

Next Prenatal Checkup:
16 weeks Triple Screen - April 22, 2025 (28 days remaining)
Preparation: Fasting blood draw
```

### Example 4: High-Risk Triple Screen
```
User: /pregnancy checkup 16weeks triple-screen high-risk

System:
Abnormal prenatal checkup result

Check Type: Triple Screen (16 weeks)
Result: High risk (Trisomy 21 risk 1:50)

Recommendations:
• Consult your prenatal care physician immediately
• Consider NIPT or amniocentesis
• Don't panic, high risk does not mean diagnosis

Next Prenatal Checkup:
Please confirm next checkup time with your doctor
```

### Example 5: Glucose Tolerance Test
```
User: /pregnancy checkup week 24 glucose-tolerance 7.5 8.2 6.8

System:
Prenatal checkup record updated

Glucose Tolerance Test Results:
Fasting Glucose: 5.3 mmol/L (normal <5.1)
1-Hour Glucose: 7.5 mmol/L (normal <10.0)
2-Hour Glucose: 6.8 mmol/L (normal <8.5)

Diagnosis: Gestational Diabetes

Recommendations:
• Consult a nutritionist immediately
• Control diet, monitor blood glucose
• Moderate exercise
• Record blood glucose values daily
```

### Example 6: Routine Checkup
```
User: /pregnancy checkup week 28 routine bp120/70 weight65kg

System:
Prenatal checkup record updated

Checkup Information:
Gestational Week: 28 weeks
Check Type: Routine Checkup
Blood Pressure: 120/70 mmHg (normal)
Weight: 65kg
Fundal Height: 26cm
Abdominal Circumference: 90cm
Fetal Heart Rate: 145 bpm (normal)

Next Prenatal Checkup:
30 weeks - 2 weeks later
```

## III. Record Symptoms (symptom)

### Example 7: Morning Sickness
```
User: /pregnancy symptom nausea moderate

System:
Symptom recorded

Symptom Information:
Type: Nausea
Severity: Moderate
Frequency: Daily

Current Gestational Week: 12 weeks (First Trimester)

Assessment:
Morning sickness is common in the first trimester, typically improves by 14-16 weeks.

Management Recommendations:
• Small, frequent meals (6-8 small meals per day)
• Eat soda crackers before getting out of bed
• Avoid empty stomach
• Stay hydrated

Important Note:
If vomiting is severe causing dehydration (reduced urination, dizziness), seek medical attention immediately.

Data synced to symptom records
```

### Example 8: Edema
```
User: /pregnancy symptom edema feet mild

System:
Symptom recorded

Symptom Information:
Type: Edema
Severity: Mild
Location: Ankles

Current Gestational Week: 32 weeks (Third Trimester)

Assessment:
Mild edema is common in late pregnancy.

Management Recommendations:
• Elevate legs while resting
• Avoid prolonged standing or sitting
• Sleep on left side
• Moderate walking
• Reduce salt intake

Warning:
If sudden swelling occurs in face or hands, seek medical attention immediately to rule out preeclampsia.
```

## IV. Record Weight (weight)

### Example 9: Normal Weight Gain
```
User: /pregnancy weight 62.5

System:
Weight recorded

Weight Information:
Record Date: March 20, 2025
Current Gestational Week: 12 weeks

Current Weight: 62.5 kg
Pre-pregnancy Weight: 60.0 kg
Weight Gained: 2.5 kg
Current BMI: 23.1 (normal)

Weight Gain Assessment:
Recommended Total Pregnancy Weight Gain: 11.5-16 kg
Current Progress: Normal

Expected First Trimester Weight Gain: 1-2 kg
Current Weight Gain: 2.5 kg (slightly above)

Second and Third Trimester Recommendations:
Weekly Weight Gain: 0.35-0.50 kg

Nutrition Recommendations:
• Balanced diet, avoid "eating for two"
• Quality protein: Fish, poultry, eggs, dairy, legumes
• Complex carbs: Whole grains, tubers
• Fruits and vegetables: 500g or more daily
```

### Example 10: Excessive Weight Gain
```
User: /pregnancy weight 68

System:
Weight recorded

Weight Information:
Current Weight: 68.0 kg
Pre-pregnancy Weight: 60.0 kg
Weight Gained: 8.0 kg
Current Gestational Week: 20 weeks

Weight Gain Assessment:
Pregnancy Weight Gained: 8.0 kg
Recommended Weight Gain: About 5-6kg (at this stage)
Status: Excessive weight gain

Recommendations:
• Control high-sugar, high-fat foods
• Increase vegetable proportion
• Moderate exercise
• Reduce refined carbohydrates
```

## V. Record Vital Signs (vital)

### Example 11: Normal Blood Pressure
```
User: /pregnancy vital bp 115/75

System:
Blood pressure recorded

Blood Pressure Information:
Record Date: March 20, 2025
Current Gestational Week: 12 weeks

Blood Pressure: 115/75 mmHg
Classification: Normal

Mean Arterial Pressure: 88.3 mmHg

Recommendations:
Blood pressure is normal, keep it up!

Recommendations:
• Monitor blood pressure regularly
• Watch for headache, vision changes
• Seek medical attention if blood pressure rises
```

### Example 12: High Blood Pressure Warning
```
User: /pregnancy vital bp 145/95

System:
High blood pressure warning

Blood Pressure Information:
Blood Pressure: 145/95 mmHg
Classification: Stage 2 Hypertension

Risk Assessment:
Blood pressure is elevated, close monitoring needed.

Seek Medical Care Immediately:
• Check urine protein
• Assess liver and kidney function
• Check platelets
• Assess fetal status

Warning Symptoms (seek immediate care if present):
• Severe headache
• Blurred vision, flashing lights
• Upper abdominal pain (right upper quadrant)
• Nausea and vomiting
• Shortness of breath

Please contact your prenatal care physician or go to the emergency room immediately!
```

## VI. Multiple Pregnancy Setup (type)

### Example 13: Twin Pregnancy
```
User: /pregnancy type twins

System:
Multiple pregnancy type set

Pregnancy Type Information:
Type: Twin Pregnancy
Fetal Count: 2

Due Date Adjustment:
Original Due Date: October 8, 2025 (40 weeks)
Adjusted Due Date: September 17, 2025 (37 weeks)
Advance: 3 weeks

Important Notes:
Multiple pregnancy is high-risk, recommendations:

Prenatal Checkup Frequency Adjustment:
• From 28 weeks: Every 2 weeks
• From 32 weeks: Every week
• Add cervical length monitoring (starting at 16-18 weeks)
• Add fetal growth monitoring (every 4-6 weeks)

Special Monitoring:
• Fetal growth discordance
• Signs of Twin-Twin Transfusion Syndrome (TTTS)
• Cervical shortening

Recommended Weight Gain:
Total Recommended Gain: 16-24 kg
Second and Third Trimester Weekly Gain: 0.5-0.7 kg

Recommendations:
• Consult Maternal-Fetal Medicine (MFM) specialist
• Consider referral to tertiary hospital
• Create delivery plan (discuss at 32-34 weeks)

Fetal Profiles Created:
• Fetus A - Information to be completed
• Fetus B - Information to be completed
```

### Example 14: Triplet Pregnancy
```
User: /pregnancy type triplets

System:
Multiple pregnancy type set

Pregnancy Type Information:
Type: Triplet Pregnancy
Fetal Count: 3

Due Date Adjustment:
Original Due Date: 40 weeks
Adjusted Due Date: 35 weeks
Advance: 5 weeks

Special Considerations:
Triplet pregnancy is very high risk
Recommendations:
• Immediate referral to tertiary hospital MFM specialist
• Close monitoring (every 2 weeks)
• Early delivery planning (28-30 weeks)
```

## VII. Fetal Information (fetal)

### Example 15: Fetal Weight
```
User: /pregnancy fetal A weight 1200g

System:
Fetal information updated

Fetus A Information:
Weight: 1200g (45th percentile)
Gestational Week: 28 weeks

Assessment:
Fetal development is normal, weight within normal range.
```

### Example 16: Fetal Position
```
User: /pregnancy fetal A position cephalic

System:
Fetal information updated

Fetus A Information:
Position: Cephalic (head down)
Confirmed: June 20, 2025
Notes: Cephalic, fixed

Assessment:
Cephalic presentation is the most favorable position for delivery.
```

### Example 17: Fetal Heart Rate
```
User: /pregnancy fetal A heart 145

System:
Fetal information updated

Fetus A Information:
Heart Rate: 145 bpm (normal)
Variability: Normal

Assessment:
Heart rate within normal range (110-160 bpm).
```

## VIII. View Status (status)

### Example 18: Complete Status
```
User: /pregnancy status

System:
Current Pregnancy Status

Basic Information:
Last Menstrual Period: January 1, 2025
Due Date: October 8, 2025
Current Date: March 31, 2025

Pregnancy Progress:
Current Week: 12 weeks + 6 days
Trimester: First Trimester (1-13 weeks)
Days Passed: 89 days
Days Remaining: 191 days
Progress: 32%

Fetal Development:
Size: Plum size (about 5-6cm)
Weight: About 14g
Important Milestones:
✅ Organ development mostly complete
✅ Fingers and toes differentiated
✅ External genitalia beginning to form

Weight Tracking:
Pre-pregnancy Weight: 60.0 kg
Current Weight: 62.5 kg
Weight Gained: 2.5 kg
Recommended Weight Gain: 11.5-16 kg
Status: Normal

Recent Symptoms:
• Nausea (moderate) - Daily
• Fatigue (mild) - Frequent

Recent Blood Pressure:
March 20: 115/75 mmHg (normal)

Completed Checkups:
✅ 12 weeks NT scan - March 25 (normal)

Next Checkup:
16 weeks Triple Screen - April 22, 2025
22 days remaining

Preparation: Fasting blood draw

Focus This Week:
• Continue folic acid supplementation 400 mcg/day
• Seek immediate care if vaginal bleeding or abdominal pain
• Rest well, avoid strenuous exercise
```

## IX. Next Checkup Reminder (next-checkup)

### Example 19: Next Checkup
```
User: /pregnancy next-checkup

System:
Next prenatal checkup reminder

Next Checkup Information:
Check Type: Triple Screen (16 weeks)
Scheduled Date: April 22, 2025 (Tuesday)
22 days remaining (3 weeks)

Checkup Description:
Triple Screen (Down Syndrome Screening) uses blood tests to detect
certain markers in maternal serum, assessing the risk of chromosomal
abnormalities such as Down syndrome.

Preparation:
• Fast for 8+ hours
• Bring ID and insurance card
• Bring previous checkup records
• Schedule appointment in advance
```

## Trimester Divisions

| Trimester | Weeks | Duration |
|-----------|-------|----------|
| First Trimester | 1-13 weeks | About 3 months |
| Second Trimester | 14-27 weeks | About 3.5 months |
| Third Trimester | 28-42 weeks | About 3.5 months |

## Recommended Weight Gain (Based on IOM)

| Pre-pregnancy BMI | BMI Range | Total Gain | Second/Third Trimester Weekly Gain |
|-------------------|-----------|------------|------------------------------------|
| Underweight | <18.5 | 12.5-18 kg | 0.51 kg |
| Normal | 18.5-24.9 | 11.5-16 kg | 0.42 kg |
| Overweight | 25.0-29.9 | 7-11.5 kg | 0.28 kg |
| Obese | >=30.0 | 5-9 kg | 0.22 kg |
