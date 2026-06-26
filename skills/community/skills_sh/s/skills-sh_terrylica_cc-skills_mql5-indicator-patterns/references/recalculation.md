**Skill**: [MQL5 Visual Indicator Patterns](../SKILL.md)

## Part 3: Bar Recalculation Pattern

### Problem: Rolling Window Drift

Current bar updates with each tick. Naive implementations double-count values, causing drift in rolling statistics.

### Solution: New Bar Detection + Value Replacement

```mql5
// Static variables preserve state between OnCalculate calls
static double sum = 0.0;
static int last_processed_bar = -1;

int OnCalculate(const int rates_total, const int prev_calculated, ...)
{
   for(int i = start; i < rates_total; i++)
   {
      // Detect if this is a NEW bar (not recalculation)
      bool is_new_bar = (i > last_processed_bar);

      double current_value = GetValue(i);

      if(is_new_bar)
      {
         // NEW BAR: Add to window, slide if needed
         if(i >= window_size)
         {
            int idx_out = i - window_size;
            sum -= BufHidden[idx_out];  // Remove oldest
         }
         sum += current_value;  // Add newest
      }
      else
      {
         // RECALCULATION: Replace old value with new value
         if(i == last_processed_bar && BufHidden[i] != EMPTY_VALUE)
         {
            sum -= BufHidden[i];        // Remove old contribution
         }
         sum += current_value;          // Add new value
      }

      // Store for next recalculation
      BufHidden[i] = current_value;
      last_processed_bar = i;

      // Calculate indicator using sum
      BufVisible[i] = sum / window_size;
   }

   return rates_total;
}
```

**Key points**:

- `is_new_bar` differentiates new bars from recalculation
- Hidden buffer stores old values for subtraction
- Static `last_processed_bar` tracks position
- Only slide window on NEW bars

---

## Part 4: Rolling Window State Management

### Pattern: Static Sum Variables

```mql5
static double sum = 0.0;
static double sum_squared = 0.0;
static int last_processed_bar = -1;

// Initialize sums on first run
if(prev_calculated == 0 || start == StartCalcPosition)
{
   sum = 0.0;
   sum_squared = 0.0;
   last_processed_bar = StartCalcPosition - 1;

   // Prime the window with initial values
   for(int j = start - window_size + 1; j <= start; j++)
   {
      double x = GetValue(j);
      sum += x;
      sum_squared += x * x;
   }
}
```

**Why static variables**:

- Preserve state between `OnCalculate()` calls
- Avoid recalculating entire window each tick
- Enable O(1) sliding window updates

**Initialization pattern**:

- Reset on first run (`prev_calculated == 0`)
- Prime window with initial N values
- Update incrementally thereafter
