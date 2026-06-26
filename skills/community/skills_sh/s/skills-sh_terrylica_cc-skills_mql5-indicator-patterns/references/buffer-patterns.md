**Skill**: [MQL5 Visual Indicator Patterns](../SKILL.md)

## Part 2: Buffer Architecture Patterns

### Two-Buffer Pattern (Visible + Hidden)

Use when tracking previous values for recalculation:

```mql5
#property indicator_buffers 2  // Total buffers
#property indicator_plots   1  // Visible plots

double BufVisible[];  // Plot buffer
double BufHidden[];   // Tracking buffer

int OnInit()
{
   SetIndexBuffer(0, BufVisible, INDICATOR_DATA);        // Visible
   SetIndexBuffer(1, BufHidden, INDICATOR_CALCULATIONS); // Hidden

   return INIT_SUCCEEDED;
}
```

**Buffer Types**:

- `INDICATOR_DATA`: Visible plot (appears on chart)
- `INDICATOR_CALCULATIONS`: Hidden buffer (for internal calculations)

**Why use hidden buffers**:

- Store previous bar values for recalculation
- Track intermediate calculation steps
- Maintain rolling window state
