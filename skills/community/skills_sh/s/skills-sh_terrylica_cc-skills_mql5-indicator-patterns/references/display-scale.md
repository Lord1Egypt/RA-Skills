**Skill**: [MQL5 Visual Indicator Patterns](../SKILL.md)

## Part 1: Display Scale Management

### Problem: Blank Indicator Window

**Symptom**: Indicator compiles successfully but shows blank/empty window on chart

**Root Cause**: MT5 auto-scaling fails for very small values (e.g., 0.00-0.05 range)

### Solution: Explicit Scale Setting

```mql5
int OnInit()
{
   // ... other initialization ...

   // FIX: Explicitly set scale range for small values
   IndicatorSetDouble(INDICATOR_MINIMUM, 0.0);
   IndicatorSetDouble(INDICATOR_MAXIMUM, 0.1);

   return INIT_SUCCEEDED;
}
```

**When to use**:

- Score/probability indicators (0.0-1.0 range)
- Normalized metrics with small variations
- Any values where range < 1.0

**Reference**: MQL5 forum threads 135340, 137233, 154523 document this limitation
