# Example dashboard slides

Four complete, copy-paste Slidev slides. Each is a real `layout: full` slide that renders a dashboard page.

## Prerequisites (one-time, per Slidev project)

1. `npm i ant-design-vue@^4.2.6 @ant-design/icons-vue echarts vue-echarts`
2. Copy these from `../assets/` into your project:
   - `main.ts` → `setup/main.ts`
   - `AntdThemeProvider.vue` → `components/AntdThemeProvider.vue`
   - `DashboardShell.vue` → `components/DashboardShell.vue`  *(the examples use this frame)*
3. In `slides.md` headmatter add `canvasWidth: 1280` so dashboards aren't cramped.

`DashboardShell.vue` already includes `AntdThemeProvider` (theme + dark-mode sync), the dark sider menu, and the header — so each example is just `<DashboardShell …>page content</DashboardShell>`.

## How to use an example

**Copy-paste:** open the file, copy its whole content, paste into `slides.md` as a new slide (the leading `---`/frontmatter starts a new slide).

**Or import** without copying — add a slide that pulls the file in:

```md
---
src: ./.claude/skills/slidev-antd-dashboard/examples/02-analytics-overview.md
---
```

(Adjust the path to where you keep the skill; Slidev merges the imported file's frontmatter and `<script setup>`.)

## The four examples

| File | Page | Demonstrates |
|---|---|---|
| `01-admin-layout.md` | Overview / app shell | `DashboardShell` frame (Layout + sider Menu + header), `a-alert`, `a-card`, `a-steps`, `a-badge` status list, `#actions` slot. The frame every other page sits in. |
| `02-analytics-overview.md` | Analytics overview | `a-row`/`a-col` grid, KPI `a-statistic` cards with colored deltas, **ECharts** line + donut via `<v-chart>`, `a-segmented` time range, `a-range-picker`, top-products `a-table` with `#bodyCell` tags/trends. |
| `03-data-table.md` | Orders management | Inline filter `a-form` (`a-input-search` + `a-select` + `a-range-picker`), `a-table` with `rowSelection`, `a-badge` status, `a-avatar` cells, bulk-action `a-alert`, `a-popconfirm` delete, paginator. |
| `04-detail-form.md` | Order detail + edit | `a-steps` progress, vertical `a-form` (Select, InputNumber, DatePicker, Segmented, Textarea, Switch) on the grid, `a-descriptions` summary, `a-timeline` activity. |

## Customizing

- **Change the active nav item / breadcrumb:** set `selected-key` and `:crumbs` on `<DashboardShell>`. To expand a different sub-menu, pass `open-key`.
- **Change the nav items themselves:** edit the menu inside `DashboardShell.vue`.
- **Density:** `<DashboardShell size="middle">` for roomier, default is `small`.
- **Real data / charts:** swap the arrays and ECharts `option` objects in each slide's `<script setup>`. Add ECharts modules you need to the `use([...])` list in `setup/main.ts`.
- **Dark mode:** toggle the deck's dark mode — `DashboardShell` re-themes antd and the chart surfaces automatically.

See `../references/` for the rules these examples follow (`dashboard-rules.md`, `navigation.md`) and every component (`components.md`).
