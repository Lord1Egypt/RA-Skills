# Profile Skill Examples

## 1. Set Parameters

### Example 1: Complete Setup
```
User: set F 175 70 1990-01-01

Save:
{
  "basic_info": {
    "gender": "F",
    "height": 175,
    "weight": 70,
    "birth_date": "1990-01-01"
  },
  "calculated": {
    "age": 35,
    "bmi": 22.9,
    "bmi_status": "Normal",
    "body_surface_area": 1.85
  }
}
```

### Example 2: Male Setup
```
User: set M 180 75 1985-06-15

Save:
{
  "basic_info": {
    "gender": "M",
    "height": 180,
    "weight": 75,
    "birth_date": "1985-06-15"
  },
  "calculated": {
    "age": 40,
    "bmi": 23.1,
    "bmi_status": "Normal",
    "body_surface_area": 1.94
  }
}
```

## 2. View Parameters

### Example 3: View Current Parameters
```
User: view

Output:
╔══════════════════════════════════════╗
║         👤 Personal Health Profile   ║
╠══════════════════════════════════════╣
║  Height:    ████ 175 cm              ║
║  Weight:    ██████ 70 kg             ║
║  Birth Date: 1990-01-01              ║
║  Age:       35 years                 ║
╠══════════════════════════════════════╣
║  BMI:       22.9 【Normal】          ║
║  BSA:       1.85 m²                  ║
╚══════════════════════════════════════╝
```

### Example 4: Data Not Set
```
User: view

Output:
⚠️ Data not set
Please use: /profile set 175 70 1990-01-01
```
