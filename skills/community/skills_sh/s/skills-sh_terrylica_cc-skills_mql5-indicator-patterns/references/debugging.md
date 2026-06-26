**Skill**: [MQL5 Visual Indicator Patterns](../SKILL.md)

## Part 8: Debugging Checklist

When indicator not displaying correctly:

1. **Check scale**:
   - [ ] Added `IndicatorSetDouble(INDICATOR_MINIMUM/MAXIMUM)`?
   - [ ] Range appropriate for data values?

1. **Check buffers**:
   - [ ] `indicator_buffers` >= `indicator_plots`?
   - [ ] Hidden buffers for tracking old values?
   - [ ] `ArraySetAsSeries(buffer, false)` for all buffers?

1. **Check warmup**:
   - [ ] `PLOT_DRAW_BEGIN` calculated correctly?
   - [ ] Early bars initialized to `EMPTY_VALUE`?

1. **Check recalculation**:
   - [ ] Bar detection logic (`is_new_bar`)?
   - [ ] Old value subtraction before adding new?
   - [ ] `last_processed_bar` tracking working?

1. **Check data flow**:
   - [ ] Base indicator handle valid?
   - [ ] `CopyBuffer` returning expected count?
   - [ ] No `EMPTY_VALUE` in calculated range?
