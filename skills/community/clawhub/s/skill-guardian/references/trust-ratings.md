# Trust Rating System

## How Trust Scores Are Calculated

### Base Score: 100

### Deductions

| Risk Factor | Deduction | Notes |
|-------------|-----------|-------|
| VirusTotal flag | -20 | Suspicious patterns detected |
| Network requests | -10 | External API calls |
| File system access | -10 | Broad file access |
| Eval/exec usage | -30 | Dynamic code execution |
| Crypto operations | -15 | Encryption/mining patterns |
| Obfuscated code | -25 | Hard to audit |

### Minimum Scores

- **< 50**: Blocked from auto-add (manual override required)
- **50-70**: Added with warnings
- **70+**: Added normally

## Source Trust Multipliers

| Source | Multiplier | Reasoning |
|--------|------------|-----------|
| clawhub | 1.0x | Moderated registry |
| github | 0.9x | User discretion needed |
| local | 0.8x | Unknown provenance |

## Review Schedule

- High trust (90+): Annual review
- Medium trust (70-89): Bi-annual review
- Low trust (<70): Quarterly review
