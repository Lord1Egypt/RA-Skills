# Dashboard Layout Rules

## Grid
Use 12-column grid.
Use fixed row units for simple MVP placement.

## Default Widget Size
- `kpi`: `w=3`, `h=2`
- `line`: `w=6`, `h=4`
- `bar`: `w=6`, `h=4`
- `grouped_bar`: `w=6`, `h=4`
- `table`: `w=12`, `h=5`

## Placement
- Place widgets left-to-right, top-to-bottom.
- Wrap when `x + w > 12`.
- Keep `y` monotonic.

## Filter Panel
Keep global filters in right-side panel for scaffold UI.
Filter source priority:
1. Explicit metadata `filters`
2. inferred dimensions (excluding time)
