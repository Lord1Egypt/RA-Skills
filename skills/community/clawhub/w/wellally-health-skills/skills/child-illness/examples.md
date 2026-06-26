# Child Illness Management Examples

## Example 1: Record Illness

### User Input
```
/child-illness record fever cough runny nose
```

### System Output
```
Illness record saved

Illness Information:
Child: Xiaoming
Age: 2 years 5 months
Record Date: January 14, 2025

Illness: Acute upper respiratory infection
Type: Viral cold
Severity: Mild

Symptoms:
  Fever (peak 38.5)
  Cough (dry cough)
  Runny nose (clear discharge)

Home Care Recommendations:
  Use fever reducer when temperature > 38.5
  Drink plenty of water/milk
  Maintain indoor humidity

Use /child-illness fever to record temperature
Use /child-illness medicine to record medication

Data saved
```

## Example 2: Fever Management

### User Input
```
/child-illness fever 38.5
```

### System Output
```
Fever Management Record

Child: Xiaoming (2 years 5 months)
Record Time: 2025-01-14 20:00

Temperature: 38.5
Fever Level: Moderate fever

Management Recommendations:

Physical Cooling:
  Sponge bath with lukewarm water (focus on neck, armpits, groin)
  Reduce clothing, keep well-ventilated
  Drink plenty of warm water or milk

Medication for Fever:
  Use fever reducer when temperature >= 38.5
  Ibuprofen (>6 months): 5-10mg/kg, every 6-8 hours
  Acetaminophen (>3 months): 10-15mg/kg, every 4-6 hours

Warning Signs:
Seek immediate medical care if:
  Temperature >= 39 for 24 hours
  Poor mental state, lethargy
  Difficulty breathing

Data saved
```

## Example 3: Medication Record

### User Input
```
/child-illness medicine ibuprofen suspension 5ml
```

### System Output
```
Medication recorded

Medication Information:
Record Time: 2025-01-14 20:00
Current Illness: Acute upper respiratory infection

Medication: Ibuprofen suspension
Dosage: 5ml
Route: Oral

Dosing Instructions:
  Weight: 20.5kg, recommended dose: 5ml
  Interval: 6-8 hours
  Maximum daily: 4 times

Today's Medication Log:
08:00  Ibuprofen 5ml
14:00  Skipped (temperature below 38.5)
20:00  Ibuprofen 5ml

Next Dose:
Tomorrow 02:00 or when temperature >= 38.5

Data saved
```

## Example 4: Recovery Tracking

### User Input
```
/child-illness recovery
```

### System Output
```
Recovery Progress Tracking

Child: Xiaoming
Current Illness: Acute upper respiratory infection

Course Tracking:
Onset Date: 2025-01-12
Record Date: 2025-01-14
Day of Illness: Day 3

Symptom Changes:
        Fever    Cough    Runny Nose    Spirit
Day 1   38.2     ++       ++            Normal
Day 2   38.5     +++      ++            Slightly poor
Day 3   38.0     ++       +             Recovering

Recovery Assessment:
  Temperature decreasing, entering recovery phase
  Mental state improving
  Cough still needs monitoring

Expected Recovery:
Natural course of common cold: 7-10 days
Expected full recovery: Around January 19

Data saved
```
