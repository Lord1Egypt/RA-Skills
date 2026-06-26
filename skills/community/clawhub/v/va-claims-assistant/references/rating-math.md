# VA Combined Rating Math

## The "Whole Person" Method

The VA does NOT add percentages together. Instead:

1. Sort disabilities highest to lowest
2. Apply largest rating to 100% whole person
3. Each subsequent rating applies to **remaining** whole person
4. Round result to nearest 10% (5+ rounds up, cap at 100%)

### Example: 70% + 30% + 20%
- Start: 100% whole person
- 70%: removes 70% → 30% remaining
- 30% of 30% = 9% → 21% remaining  
- 20% of 21% = 4.2% → 16.8% remaining
- Combined: 83.2% → rounds to **80%**

### Quick Script
```bash
python3 scripts/va_rating_calc.py 70 30 20
```

## Important Thresholds

| Rating | Significance |
|--------|-------------|
| 10-90% | Standard disability compensation |
| 100% | Full disability rate |
| 100% P&T | Permanent & Total — CHAMPVA, property tax, DEA |
| TDIU | 100% pay at lower rating (see below) |

## TDIU (Individual Unemployability)
Pay at 100% rate if:
- **Single condition ≥ 60%**, OR
- **Combined ≥ 70% with at least one condition ≥ 40%**
- Must be unable to maintain substantially gainful employment

## SMC (Special Monthly Compensation)
Additional monthly pay above 100% for:
- Loss of use of limb/organ
- Aid & Attendance (needs help with daily activities)
- Housebound status
- Combinations (SMC-L, S, etc.)
