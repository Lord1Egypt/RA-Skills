# Analytics Explorer - JSX Template

## When to Use

- User wants an interactive analytics dashboard in JSX
- User needs filters, computed metrics, and dynamic views
- Static markdown or HTML would not satisfy interaction needs

## Required UI Blocks

1. Header with dashboard title and short context subtitle
2. Filter bar with at least:
   - time range selector
   - metric selector
   - segment selector (region/product/team/etc.)
3. KPI stats grid (3-5 cards) derived from active filter state
4. Primary trend visualization panel
5. Secondary breakdown visualization panel
6. Detail table synced with current filter state

## State and Interaction Contract

- Keep filter state in `useState` (or reducer for complex cases)
- Compute chart and stats data with `useMemo` from active filters
- Every visual panel must update from the same derived data source
- Trends in table rows must align with chart period and metric
- Use one theme accent strategy tied to selected segment if helpful

## Data Contract

- Input data should be structured by dimensions (time, metric, segment)
- Derived stats should include:
  - `total`
  - `average`
  - `peak`
  - optional `growth`
- For trend calculations, compute change from adjacent periods

## JSX Constraints

- Allowed imports only from `react` and `react-dom`
- No external charting packages
- Prefer SVG and CSS-driven visuals
- Respect reduced-motion user preference

## Scaffold Template

```jsx
import { useMemo, useState } from 'react'

export default function AnalyticsExplorer () {
  const [timeRange, setTimeRange] = useState('{default_time_range}')
  const [metric, setMetric] = useState('{default_metric}')
  const [segment, setSegment] = useState('{default_segment}')

  const chartData = useMemo(() => {
    // Derive dataset from current filters
    return { /* { series -> period -> value } */ }
  }, [timeRange, metric, segment])

  const stats = useMemo(() => {
    // Compute total/average/peak/growth from chartData
    return {
      total: 0,
      average: 0,
      peak: 0,
      growth: '{+0.0%}',
    }
  }, [chartData])

  return (
    <div>
      <header>
        <h1>{'{Dashboard Title}'}</h1>
        <p>{'{Short context subtitle}'}</p>
      </header>

      <section>
        {/* Filters: time range, metric, segment */}
      </section>

      <section>
        {/* KPI cards driven by stats */}
      </section>

      <section>
        {/* Primary chart (SVG) driven by chartData */}
      </section>

      <section>
        {/* Secondary chart (SVG/CSS) for breakdown */}
      </section>

      <section>
        {/* Detail table synchronized with active filters */}
      </section>
    </div>
  )
}
```

## Implementation Notes

- Keep styles local and consistent (inline object or scoped CSS block)
- Keep section responsibilities clear:
  - filters = control
  - charts = pattern/trend
  - table = exact values
- Avoid placeholder fake brands in final output

## Validation Checklist

- All controls are wired and affect output
- `useMemo` dependencies are complete and correct
- Derived values and table trends are numerically consistent
- No unsupported imports or runtime-only browser assumptions
- Generated JSX stays understandable and modifiable
