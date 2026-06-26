# Estimation Formulas

## Overview

This document provides complete formulas and calculation examples for test effort estimation.

## Base Time Standards

### Case Design Time

**Simple Features:**
- Range: 0.20-0.30 person-days
- Base: 0.25 person-days
- Formula: `base_time * complexity_factor`
  - Simple: 0.25 * 1.0 = 0.25
  - Medium: 0.25 * 1.4 = 0.35
  - Complex: 0.25 * 2.0 = 0.50

**Examples:**
- Gateway list (simple): 0.30 person-days
- Device details (medium): 0.40 person-days
- Add device (complex): 0.50 person-days

### First Run Time

**Simple Features:**
- Range: 0.15-0.20 person-days
- Base: 0.18 person-days
- Formula: `base_time * complexity_factor`
  - Simple: 0.18 * 1.0 = 0.18
  - Medium: 0.18 * 1.4 = 0.25
  - Complex: 0.18 * 1.7 = 0.30

**Examples:**
- Gateway list (simple): 0.20 person-days
- Device details (medium): 0.30 person-days
- Add device (complex): 0.40 person-days

### Retest Time

**Formula:**
- `first_run_time * retest_ratio`
- Ratio varies by complexity:
  - Simple: 40%-67% (0.08-0.13)
  - Medium: 33%-40% (0.08-0.12)
  - Complex: 33%-38% (0.10-0.15)
- Minimum: 0.10 person-days (after rounding)

**Calculation Examples:**
- Gateway list: 0.20 * 50% = 0.10 → round to 0.10
- Device details: 0.30 * 33% = 0.099 → round to 0.10
- Add device: 0.40 * 38% = 0.152 → round to 0.15

### Regression Time

**Formula:**
- `first_run_time * regression_ratio`
- Ratio varies by complexity:
  - Simple: 50%-67% (0.08-0.13)
  - Medium: 48%-50% (0.12-0.15)
  - Complex: 50% (0.15-0.20)
- Round to two decimals

**Calculation Examples:**
- Gateway list: 0.20 * 50% = 0.10
- Device details: 0.30 * 50% = 0.15
- Add device: 0.40 * 50% = 0.20

## Complete Calculation Example

### Example: Gateway List (Simple Feature)

**Input:**
- Feature: Gateway list display and navigation
- Complexity: Simple

**Calculations:**
1. Case Design: 0.30 person-days (simple upper bound)
2. First Run: 0.20 person-days (simple upper bound)
3. Retest: 0.20 * 50% = 0.10 person-days
4. Regression: 0.20 * 50% = 0.10 person-days
5. Total: 0.30 + 0.20 + 0.10 + 0.10 = 0.70 person-days

### Example: Add Device (Complex Feature)

**Input:**
- Feature: Online/offline device binding
- Complexity: Complex

**Calculations:**
1. Case Design: 0.50 person-days (complex standard)
2. First Run: 0.40 person-days (complex upper bound)
3. Retest: 0.40 * 38% = 0.152 → round to 0.15 person-days
4. Regression: 0.40 * 50% = 0.20 person-days
5. Total: 0.50 + 0.40 + 0.15 + 0.20 = 1.25 person-days

## Rounding Rules

### Standard Rounding
- Round to two decimal places
- Use Python `round(value, 2)` function
- Example: 0.152 → 0.15, 0.099 → 0.10

### Minimum Value Rule
- All time values must be >= 0.10 person-days
- If calculated value < 0.10, set to 0.10
- Example: 0.08 → 0.10, 0.099 → 0.10

## Validation Rules

### Total Error Constraint
- Total estimation error should be within 0.5 person-days of actual values
- Calculate: `abs(estimated_total - actual_total) <= 0.5`

### Consistency Check
- Simple features should not exceed 0.30 person-days for design
- Complex features should be at least 0.50 person-days for design
- Medium features should fall between 0.35-0.40 person-days for design
- Retest and regression times should be proportional to first run
