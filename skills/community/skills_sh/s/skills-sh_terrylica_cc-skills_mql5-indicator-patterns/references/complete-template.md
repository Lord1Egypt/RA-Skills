**Skill**: [MQL5 Visual Indicator Patterns](../SKILL.md)

## Part 7: Complete Example Template

```mql5
#property indicator_separate_window
#property indicator_buffers 2
#property indicator_plots   1

#property indicator_label1    "My Indicator"
#property indicator_type1     DRAW_LINE
#property indicator_color1    clrOrange
#property indicator_width1    2

input int InpPeriod = 20;
input int InpWindow = 30;

double BufVisible[];
double BufHidden[];
int hBase = INVALID_HANDLE;

int OnInit()
{
   // Buffers
   SetIndexBuffer(0, BufVisible, INDICATOR_DATA);
   SetIndexBuffer(1, BufHidden, INDICATOR_CALCULATIONS);

   // Warmup
   int StartCalcPosition = InpPeriod + InpWindow - 1;
   PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartCalcPosition);
   PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE);

   // Explicit scale for small values
   IndicatorSetDouble(INDICATOR_MINIMUM, 0.0);
   IndicatorSetDouble(INDICATOR_MAXIMUM, 1.0);

   // Base indicator
   hBase = iSomeIndicator(_Symbol, _Period, InpPeriod);
   if(hBase == INVALID_HANDLE) return INIT_FAILED;

   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   if(hBase != INVALID_HANDLE) IndicatorRelease(hBase);
}

int OnCalculate(const int rates_total,
                const int prev_calculated,
                const datetime &time[],
                ...)
{
   int StartCalcPosition = InpPeriod + InpWindow - 1;
   if(rates_total <= StartCalcPosition) return 0;

   // Get base data
   static double base[];
   ArrayResize(base, rates_total);
   ArraySetAsSeries(base, false);
   if(CopyBuffer(hBase, 0, 0, rates_total, base) < rates_total)
      return prev_calculated;

   // Set forward indexing
   ArraySetAsSeries(BufVisible, false);
   ArraySetAsSeries(BufHidden, false);

   // Start position
   int start = (prev_calculated == 0) ? StartCalcPosition : prev_calculated - 1;
   if(start < StartCalcPosition) start = StartCalcPosition;

   // Initialize early bars
   if(prev_calculated == 0)
   {
      for(int i = 0; i < start; i++)
      {
         BufVisible[i] = EMPTY_VALUE;
         BufHidden[i] = EMPTY_VALUE;
      }
   }

   // Rolling window state
   static double sum = 0.0;
   static int last_processed_bar = -1;

   // Prime window on first run
   if(prev_calculated == 0 || start == StartCalcPosition)
   {
      sum = 0.0;
      last_processed_bar = StartCalcPosition - 1;

      for(int j = start - InpWindow + 1; j <= start; j++)
         sum += base[j];
   }

   // Main loop
   for(int i = start; i < rates_total && !IsStopped(); i++)
   {
      bool is_new_bar = (i > last_processed_bar);

      // Slide window on new bar
      if(is_new_bar && i >= InpWindow)
      {
         int idx_out = i - InpWindow;
         sum -= base[idx_out];
      }

      double current = base[i];

      // Update sum
      if(is_new_bar)
      {
         sum += current;
      }
      else
      {
         if(i == last_processed_bar && BufHidden[i] != EMPTY_VALUE)
            sum -= BufHidden[i];
         sum += current;
      }

      last_processed_bar = i;

      // Calculate & store
      BufHidden[i] = current;
      BufVisible[i] = sum / InpWindow;
   }

   return rates_total;
}
```
