# Xiamen Tide Calculator v3.0 - New Features Guide

## Overview of Three New Features

### 1. Solar-to-Lunar Date Auto-Conversion ⭐
**Feature**: Supports direct input of solar dates (YYYY-MM-DD format) with automatic conversion to lunar dates

**Usage Examples**:
```bash
# Query tides for April 2, 2025
python scripts/tide_calculator.py --solar-date 2025-04-02

# Query beachcombing advice for April 2, 2025
python scripts/tide_calculator.py --solar-date 2025-04-02 --beach-mode
```

**Output Example**:
```
【Xiamen Beachcombing Advice · Lunar 2025/3/5】
🌊 Beachcombing Score: 7.4 (Recommended)
...
```

### 2. Current Date Auto-Detection ⭐
**Feature**: Use the --today parameter to automatically get the current date and convert it to lunar date

**Usage Examples**:
```bash
# Query today's tides
python scripts/tide_calculator.py --today

# Query today's beachcombing advice
python scripts/tide_calculator.py --today --beach-mode

# Smart tip: If no date parameter is provided, the current date is used automatically
python scripts/tide_calculator.py
# Output: Tip: No date provided, using current date
```

**Output Example**:
```
【Xiamen Beachcombing Advice · Lunar 2026/2/15】
🌊 Beachcombing Score: 6.4 (Recommended)
...
```

### 3. Leap Month Handling ⭐
**Feature**: Automatic leap month detection, annotation in output, and special tips

**Features**:
- Auto-detection: Uses `lunar_date.leap_month` property
- Output annotation: Displays "Leap X Month" instead of "Month X"
- Tide annotation: Displays "Spring Tide (Leap Month)" etc.
- Score adjustment: Extra +0.2 points during leap months
- Special tips: Beachcombing advice during leap months

**Leap Month Output Example**:
```
【Xiamen Beachcombing Advice · Lunar 2026 Leap 6/2】
🌊 Beachcombing Score: 6.0 (Recommended)
...
📍 Recommended Locations:
  - Suggest waiting for spring tide before beachcombing
  - Note: Tides may vary slightly during leap months
...
📊 Tide Information:
  - Tide Size: Spring Tide (Leap Month)
...
💡 Beachcombing Tips:
  - During leap months, tides may vary slightly, on-site observation recommended
```

---

## Summary of All Usage Methods

### Standard Mode (Tide Query)
```bash
# Use current date
python scripts/tide_calculator.py --today

# Use solar date
python scripts/tide_calculator.py --solar-date 2025-04-02

# Use lunar date
python scripts/tide_calculator.py --lunar-day 15 --lunar-month 3

# No parameters (auto-detect current date)
python scripts/tide_calculator.py
```

### Beachcombing Mode
```bash
# Current date beachcombing advice
python scripts/tide_calculator.py --today --beach-mode

# Solar date beachcombing advice
python scripts/tide_calculator.py --solar-date 2025-04-02 --beach-mode

# Lunar date beachcombing advice
python scripts/tide_calculator.py --lunar-day 2 --lunar-month 3 --beach-mode
```

### Multi-day Comparison
```bash
# Compare beachcombing scores over multiple days (supports leap month detection)
python scripts/compare_beach_days.py --lunar-month 3 --start-day 1 --days 10
```

---

## Common Use Cases

### Case 1: Check if today is good for beachcombing
```bash
python scripts/tide_calculator.py --today --beach-mode
```

### Case 2: Check tomorrow's beachcombing advice
```bash
# 1. Determine tomorrow's solar date
# 2. Query using the solar date
python scripts/tide_calculator.py --solar-date 2026-04-03 --beach-mode
```

### Case 3: Query tides for a specific date
```bash
# Using solar date (more convenient)
python scripts/tide_calculator.py --solar-date 2025-05-01

# Or using lunar date
python scripts/tide_calculator.py --lunar-day 1 --lunar-month 4
```

### Case 4: Which day in the next week is best for beachcombing
```bash
python scripts/compare_beach_days.py --lunar-month 3 --start-day 1 --days 7
```

### Case 5: Query beachcombing advice during leap months
```bash
# The system automatically detects leap months
python scripts/tide_calculator.py --lunar-day 2 --lunar-month 6 --beach-mode
# If it's a leap sixth month, it will be automatically annotated
```

---

## Output Interpretation

### Title Section
```
【Xiamen Beachcombing Advice · Lunar 2026/2/15】
                          ^^^^  Year  ^^Month ^^Day
                          If leap month, displays "Leap X Month"
```

### Beachcombing Score
```
🌊 Beachcombing Score: 6.4 (Recommended)
                        ^^^^  ^^^^^^^^^^  ^^^^^^
                        Score  Rec. Level
```
- **8.0-10.0**: Highly Recommended
- **6.0-7.9**: Recommended
- **4.0-5.9**: Fair
- **0.0-3.9**: Not Recommended
- **Leap Month**: Extra +0.2 points

### Tide Size Annotation
```
Tide Size: Spring Tide (Leap Month)
           ^^^^^^^^^^^^  ^^^^^^^^^^
           Size          Leap annotation (only shown during leap months)
```

### Time Format
```
High Tide 1: 12:00
High Tide 2: Next Day 00:24  ← Cross-day annotation
Low Tide 1: 05:48
Low Tide 2: 18:12
Low Tide 1: Previous Day 19:24  ← Cross-day annotation
```

---

## Command Line Parameter Reference

### tide_calculator.py Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `--lunar-day` | Lunar day (1-30) | `--lunar-day 15` |
| `--lunar-month` | Lunar month (1-12), default 1 | `--lunar-month 3` |
| `--solar-date` | Solar date (YYYY-MM-DD) ⭐ | `--solar-date 2025-04-02` |
| `--today` | Use current date ⭐ | `--today` |
| `--beach-mode` | Beachcombing mode | `--beach-mode` |

### compare_beach_days.py Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `--lunar-month` | Lunar month (1-12) | `--lunar-month 3` |
| `--start-day` | Starting lunar day (1-30) | `--start-day 1` |
| `--days` | Number of days to compare, default 7 | `--days 10` |

---

## Dependency Requirements

### Python Libraries
- **zhdate**: Lunar date conversion library (required)
  ```bash
  pip install zhdate
  ```

### Python Version
- Python 3.6+

---

## FAQ

### Q1: How do I know if a date falls in a leap month?
A: The system automatically detects it. If it's a leap month, the output will clearly display "Leap X Month".

### Q2: Can solar and lunar dates be used together?
A: It's recommended to use one method. If both are provided, the system will use the solar date.

### Q3: Do --today and --solar-date conflict?
A: Yes, the last provided parameter will be used. It's recommended to explicitly specify the desired parameter.

### Q4: Will beachcombing scores be higher during leap months?
A: Leap months receive an extra +0.2 points, but the main scoring factors are still based on tide size, time windows, etc.

### Q5: How to verify if the lunar conversion is correct?
A: You can compare with other lunar conversion tools or calendar software. The zhdate library is based on professional algorithms.

---

## Upgrade Notes

### Upgrading from v2.0 to v3.0

**New Features**:
1. ✅ Solar-to-lunar date auto-conversion
2. ✅ Current date auto-detection
3. ✅ Leap month handling

**Upgrade Steps**:
1. Install dependencies: `pip install zhdate`
2. Use the new skill file: `xiamen-tide-calculator.skill`
3. Review new feature usage

**Compatibility**: Fully backward compatible, original parameters continue to work.

---

## Quick Start

### First Time Use
```bash
# 1. Install dependencies
pip install zhdate

# 2. Query today's tides (using new features)
python scripts/tide_calculator.py --today --beach-mode

# 3. Review beachcombing advice
# All information is included in the output
```

### Most Common Commands
```bash
# Today's beachcombing advice (most common)
python scripts/tide_calculator.py --today --beach-mode

# Specific solar date beachcombing advice
python scripts/tide_calculator.py --solar-date 2025-04-02 --beach-mode

# Next week beachcombing comparison
python scripts/compare_beach_days.py --lunar-month 3 --start-day 1 --days 7
```

---

## Technical Support

### What to do if you encounter problems?
1. Check if zhdate is installed correctly: `pip list | grep zhdate`
2. Confirm Python version: `python --version`
3. View detailed error information: Check full output when running the script
4. Reference verification document: `Xiamen Tide Calculator - New Feature Verification Summary`

### Feature Suggestions and Feedback
If you have feature suggestions or find bugs, please contact the developer.
