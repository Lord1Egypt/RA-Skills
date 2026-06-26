# User Basic Parameters Schema

Complete data structure definition for user basic medical parameters.

## Field Quick Reference

### Basic Information (basic_info)

| Field | Type | Description |
|-------|------|-------------|
| `gender` | enum | M=Male, F=Female |
| `height` | number | Height in centimeters, 50-250 |
| `weight` | number | Weight in kilograms, 2-300 |
| `birth_date` | string | Birth date in YYYY-MM-DD format |

### Calculated Indicators (calculated)

| Field | Type | Description |
|-------|------|-------------|
| `age` | integer | Age |
| `bmi` | number | BMI index |
| `bmi_status` | enum | Underweight/Normal/Overweight/Obese |
| `body_surface_area` | number | Body surface area in m² |

## BMI Classification

| Range | Status |
|-------|--------|
| < 18.5 | Underweight |
| 18.5 - 23.9 | Normal |
| 24 - 27.9 | Overweight |
| >= 28 | Obese |

## Calculation Formulas

**BMI:**
```
BMI = weight(kg) / height(m)²
```

**Body Surface Area (Mosteller):**
```
BSA = √(height_cm × weight_kg / 3600)
```

## Data Storage

- Location: `data/profile.json`
- Format: JSON object
