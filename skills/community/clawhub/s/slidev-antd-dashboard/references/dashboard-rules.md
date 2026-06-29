# Dashboard composition rules

How to assemble ant-design-vue components into a dashboard that reads cleanly — and fits on a Slidev slide. Follow these in order; they resolve most layout decisions.

## 1. Anatomy: every admin dashboard is the same 4 regions

```
┌──────────┬───────────────────────────────────────────┐
│          │  Header: breadcrumb · search · user · bell │  ← a-layout-header
│  Sider   ├───────────────────────────────────────────┤
│  (menu)  │  Page title + primary action               │
│          │  Filter bar                                 │  ← a-layout-content
│  a-menu  │  Content grid (KPIs → charts → table)       │
│          │                                             │
└──────────┴───────────────────────────────────────────┘
```

- **Sider** (`a-layout-sider`, 200–240 px, `theme="dark"` is the classic look) holds the `a-menu`.
- **Header** (`a-layout-header`, ~56–64 px, white) holds breadcrumb on the left; search + notifications (`a-badge`) + user `a-avatar`/`a-dropdown` on the right.
- **Content** (`a-layout-content`, padding 16–24, `overflow:auto`) holds the page. Top of the page: an `<h2>`/`a-typography-title` + the single primary action button on the right (use `a-flex justify="space-between"`).
- Build the frame with **Layout**, never hand-rolled flexbox.

## 2. The grid is law

Everything in the content area lives in `a-row`/`a-col` (24 columns).

- **Gutter:** `:gutter="[16,16]"` (horizontal, vertical) is the default. 24 for airy executive dashboards.
- **KPI row:** 4 cards → `:span="6"`; 3 cards → `:span="8"`; 2 → `:span="12"`.
- **Charts row:** a big chart `:span="16"` next to a side panel `:span="8"`; or two `:span="12"`.
- **Full-width table:** `:span="24"`.
- **Responsive** (if the deck is viewed at odd sizes): `:xs="24" :sm="12" :lg="6"`.
- Never free-position with absolute CSS. If two things must align, they share a row.

## 3. Spacing: multiples of 8

| Token | px | Where |
|---|---|---|
| xs | 4 | icon↔text |
| sm | 8 | within a control cluster |
| md | 16 | card padding, default gutter, between filter fields |
| lg | 24 | between major sections / generous gutter |

Use `a-space :size="..."` and grid `:gutter`, not ad-hoc `margin`. Vertical rhythm between stacked rows: a wrapping `a-row` with `:gutter="[16,16]"` or `a-space direction="vertical" size="middle" style="width:100%"`.

## 4. Color is semantic, never decorative

- Pick **one** primary (brand) color via the theme token `colorPrimary`. It marks the **single most important action per view** — exactly one `type="primary"` button per region.
- Status palette, used only to encode meaning:
  - **success/up** → green (`#52c41a`), `a-tag color="green"`, `a-badge status="success"`, positive Statistic `valueStyle`.
  - **warning** → gold (`#faad14`).
  - **error/down** → red (`#ff4d4f`).
  - **processing/info** → blue (`#1677ff`), `a-badge status="processing"`.
  - **neutral/disabled** → grey (`color="default"`).
- Don't color things for variety. A wall of multicolored tags reads as noise. Greys + one accent + status colors.
- KPI deltas: green `<arrow-up-outlined/>` for good, red `<arrow-down-outlined/>` for bad — but remember "up" isn't always good (e.g. churn, latency); color by *sentiment*, not direction.

## 5. Typography & hierarchy

- Page title: `a-typography-title :level="4"` (or `<h2>`). Card titles via the card's `title` prop. Section labels: `a-typography-text type="secondary"` uppercase small.
- KPI value is the largest text on the card; its label is `type="secondary"` above it.
- Right-align numbers in tables (`align: 'right'` in the column) so digits line up; left-align text.
- Truncate long text with `a-typography-text :ellipsis` or column `ellipsis: true` + a Tooltip — never let it wrap a table row to 3 lines.

## 6. Density: make it compact

Dashboards are dense; default antd sizing is roomy. On slides:

- Set `componentSize="small"` (AntdThemeProvider `size="small"`) — shrinks tables, inputs, buttons together.
- Or apply `theme.compactAlgorithm` for an even tighter global rhythm.
- Tables: `size="small"`, hide row borders you don't need, cap columns at ~6 visible.
- Prefer `a-statistic` over sentences. Prefer `a-tag`/`a-badge` over prose status.

## 7. KPI cards

- 3–6 per row, equal `:span`. Each: secondary label → big `a-statistic` value → a delta (`+12% vs last mo`) and optionally a tiny sparkline (`<v-chart>` ~40 px tall).
- Keep them parallel: same metric grammar, same precision, same card height.
- `:bordered="false"` when the page background is tinted; bordered on white.

## 8. Tables

- Always set `row-key`. Always set `:scroll="{ y: <px> }"` on a slide so the table body scrolls instead of pushing the slide off-canvas. Use `:scroll="{ x }"` if columns are wide.
- Use `#bodyCell` to render status as `a-tag`/`a-badge`, money right-aligned, and an actions column (`a-space` of `a` links + `a-popconfirm`).
- Pagination: `:pagination="{ pageSize: 8, size: 'small' }"`, or `:pagination="false"` for a short fixed list.
- Bulk actions: `:rowSelection` + an action bar that appears above the table.
- Left-most column = the entity's name/identifier (often a link).

## 9. Charts (ECharts via `<v-chart>`)

- One idea per chart. Line = trend over time; Bar = compare categories; Pie/Donut = parts of a whole (≤5 slices); Gauge/Progress = single value vs target.
- **Always set an explicit height** (`style="height:240px"`). Give `grid` tight margins so it fills the card.
- Match the deck: pass a theme or set `colorPrimary`-aligned series colors; turn off chart junk (heavy gridlines, 3D, shadows).
- Put each chart in an `a-card` with a `title` and a Segmented/Select for its time range in `#extra`.

## 10. Fitting a dashboard onto a slide

A Slidev slide is a **fixed canvas**, default 980×552 px, scaled to the viewport. Desktop dashboards assume ~1440 px. Strategy, in order of preference:

1. **Raise the canvas** in headmatter: `canvasWidth: 1280` (or `1440`). The whole slide — at desktop density — scales down to fit. This is the main lever. Set it once for the deck.
2. **Compact components:** `componentSize="small"` / `compactAlgorithm` (§6).
3. **Per-slide `zoom`:** add `zoom: 0.85` to a single crowded slide's frontmatter.
4. **Scroll inside, not out:** give the content area `overflow:auto` and tables `:scroll`, so overflow scrolls within the panel rather than spilling off the slide.
5. **Use `layout: full`** so the dashboard uses the entire canvas (no slide padding/centering).

Don't shrink font-size by hand or `transform: scale()` ad hoc — it desyncs hit-targets and blurs text. Let `canvasWidth`/`zoom` do uniform scaling.

```yaml
---
layout: full
zoom: 0.9     # only if this specific slide is tight
---
```

## 11. States (especially for mockups)

A convincing dashboard mockup shows more than the happy path:

- **Loading:** wrap panels in `a-skeleton :loading="true" active` or `a-spin`.
- **Empty:** `a-empty` inside a card / as a table's empty slot.
- **Error/permission:** `a-result status="403|500"`.
- **Realistic data:** plausible names, dates, and numbers — never "Lorem ipsum" or `foo/bar`. Inconsistent or fake-looking data undermines the design.

## 12. Dark mode

AntdThemeProvider syncs antd to Slidev's dark mode automatically. Verify both: toggle dark in Slidev (the deck's dark toggle) and confirm cards/tables/charts remain legible. For charts, pass a dark-aware `backgroundColor: 'transparent'` and light text colors, or register an ECharts dark theme.

## Do / Don't

**Do**
- Start from an `examples/` skeleton and a Layout shell.
- One primary action per region; everything else secondary/tertiary.
- Align everything to the 24-grid and the 8 px spacing scale.
- Encode meaning with color/tags; keep the rest neutral.
- Show realistic data and at least one non-happy state.

**Don't**
- Use React `antd` or `@ant-design/charts` (React-only) — Vue equivalents only.
- Import `reset.css` globally (breaks Slidev typography).
- Free-position with absolute CSS or hand-rolled flex for the frame.
- Cram 10 KPIs and 6 charts on one slide — split across slides; one story per slide.
- Leave `<v-chart>` without a height, or a table without `row-key`/`:scroll`.
- Wire `a-menu` to Slidev's router — keep it on local state.
