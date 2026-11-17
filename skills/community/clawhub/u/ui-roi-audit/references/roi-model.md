# ROI model

How to turn an audit finding into a number. The method follows Loveday & Niehaus (2008, ch. 2).
The worked example below uses invented figures; it is not taken from the book.

## The two formulas

```
Net gain = Revenue attributable to the change − Investment
ROI (%)  = Net gain ÷ Investment × 100
```

(Loveday & Niehaus 2008, ch. 2)

## The inputs

| Input | Where it comes from |
|---|---|
| Visits per month | Analytics |
| Conversion rate | Conversions ÷ visits, for the audited goal |
| Average value per conversion | Average order value, or average lead value × close rate |
| Investment | Design, content, and build cost of the fix |

Revenue per month = visits × conversion rate × average value. (ch. 2)

## Traffic versus conversion

The book's central argument: money spent on extra traffic buys a one-time gain, while money spent on
raising the conversion rate keeps paying on all traffic that follows, including traffic bought
later (ch. 2). Use this to answer "should we buy more ads or fix the page".

Compare the two options over the same period and the same spend:

1. **Buy traffic.** Extra visits × current conversion rate × average value, minus the spend. The
   gain stops when the spend stops.
2. **Improve conversion.** All visits × (new rate − old rate) × average value, for every month the
   improvement stays live, minus the one-time spend.

## Worked example (illustrative figures)

A lead-generation page: 40,000 visits a month, 1.5% conversion, 80 EUR average lead value.

- Baseline revenue: 40,000 × 0.015 × 80 = 48,000 EUR a month.
- Fix costs 12,000 EUR and lifts conversion to 1.65% (a 0.15 point gain).
- Extra revenue: 40,000 × 0.0015 × 80 = 4,800 EUR a month.
- Month 1: 4,800 − 12,000 = −7,200 EUR. The fix has not paid back yet.
- Month 12: 57,600 − 12,000 = 45,600 EUR net gain. ROI = 45,600 ÷ 12,000 = 380%.

The same lesson as in the book: a conversion fix can look poor in its first month and strong over a
year, so judge it over at least twelve months (ch. 2).

## Rules for estimates

- **Use ranges.** Give a low and a high conversion assumption, never a single point.
- **Stay conservative.** The authors describe conversion forecasting as closer to art than science
  and advise cautious estimates (ch. 2, ch. 3).
- **State what the model ignores.** Seasonality, traffic mix changes, and price changes are outside
  a simple model (ch. 3).
- **Annualize.** Report twelve-month figures alongside the payback month.
- **No data, no number.** If visits, conversion rate, or average value is unknown, say which input
  is missing and give a qualitative rating instead.
- **Use funnel data to find the page.** Analytics should show where visitors leave, not only how
  many pages were viewed (ch. 3).

## When the goal is not a sale

For software and internal tools, value shows up as cost avoided instead of revenue gained: less
development rework, fewer support contacts, shorter training, faster task completion. See
`usability-roi-module.md` for the benefit categories from Marcus (2004).
