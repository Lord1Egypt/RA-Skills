---
name: slidev-antd-dashboard
description: Build dashboard and admin-UI slides in Slidev using ant-design-vue (the Vue 3 implementation of Ant Design). Use when creating Slidev presentations that need dashboards, admin layouts, side menus, data tables, KPI/stat cards, charts, forms, or any Ant Design components. Covers full setup, every ant-design-vue component, composition rules, menu/navigation design specs, and ready-to-paste example slides.
---

# Slidev + Ant Design Dashboards

Build polished **dashboard / admin-console mockups inside Slidev slides** using **`ant-design-vue`**.

## Read this first (critical context)

1. **Slidev is Vue 3. Use `ant-design-vue`, NOT React `antd`.** The canonical `antd` package is React-only and cannot be dropped into Slidev. `ant-design-vue` is the official Ant Design implementation for Vue 3 — same design language, same component set, near-identical API. Every example here uses it.
2. **Globally-registered components use the `a-` prefix.** After `app.use(Antd)`, you write `<a-button>`, `<a-table>`, `<a-layout-sider>`, `<a-menu>`, `<a-statistic>`, etc. — not `<Button>`.
3. **ant-design-vue v4 uses CSS-in-JS.** Component styles auto-inject; you do **not** need (and should **avoid**) globally importing `ant-design-vue/dist/reset.css`, because its global preflight overrides Slidev's slide typography. Theme via `<a-config-provider>` instead.
4. **Ant Design ships no charts.** Use **ECharts (`vue-echarts`)** — see [setup.md](references/setup.md#charts). `@ant-design/charts` is React-only; do not suggest it for Slidev.
5. **A slide is a fixed canvas** (default 980×552 px). Real dashboards are designed for ~1440 px. Render at desktop density and let Slidev scale the slide down — set `canvasWidth` higher and/or use `componentSize`. See [dashboard-rules.md](references/dashboard-rules.md#fitting-a-dashboard-onto-a-slide).

## Quickstart

```bash
# in a Slidev project (npm init slidev@latest)
npm i ant-design-vue@^4.2.6 @ant-design/icons-vue
npm i echarts vue-echarts          # charts (recommended)
```

1. Copy `assets/main.ts` → `setup/main.ts` (registers antd, all icons, and `<v-chart>` globally).
2. Copy `assets/AntdThemeProvider.vue.md` → `components/AntdThemeProvider.vue.md` (ConfigProvider + dark-mode sync + sane tokens).
3. In `slides.md` headmatter, bump the canvas so dashboards aren't cramped:
   ```yaml
   ---
   canvasWidth: 1280
   ---
   ```
4. Wrap any dashboard slide content in `<AntdThemeProvider>` and use a `full` layout. Paste an example from `examples/` to start.

Full, annotated instructions: **[references/setup.md](references/setup.md)**.

## The 5 golden rules (details in dashboard-rules.md)

1. **One Layout shell per dashboard:** `a-layout` → `a-layout-sider` (nav) + `a-layout-header` (top bar) + `a-layout-content` (work area). Don't hand-roll flexbox for the frame.
2. **Everything sits on the 24-column grid** (`a-row`/`a-col` with `:gutter`). KPI cards = 4–6 across; never free-position.
3. **8 px spacing rhythm** — gutters and margins in multiples of 8 (8/16/24). Use `a-space` instead of margin hacks.
4. **Color is semantic, not decorative** — primary for the one main action per view; green/red/gold via `a-tag`/`a-badge`/Statistic only to encode meaning. ≤1 primary button per region.
5. **Show structure, not lorem** — realistic labels and numbers; use `a-skeleton`/`a-empty` for loading/empty states in mockups.

## What's in this skill

| File | Use it for |
|------|-----------|
| [references/setup.md](references/setup.md) | Install, `setup/main.ts`, theming, dark mode, scaling, charts, the React-antd→ant-design-vue translation table, pitfalls. |
| [references/components.md](references/components.md) | **Every** ant-design-vue component, grouped, with key props + "use-in-dashboard" guidance and the `a-` tag name. |
| [references/dashboard-rules.md](references/dashboard-rules.md) | Composition rules: layout, grid, spacing, color, density, KPI cards, tables, fitting onto a slide, do/don't. |
| [references/navigation.md](references/navigation.md) | Menu & navigation design spec: sider vs top nav, IA depth, Menu/Breadcrumb/Tabs/Steps patterns, responsive, do/don't. |
| [assets/](assets/) | Drop-in `main.ts`, `AntdThemeProvider.vue.md`, `styles.css`. |
| [examples/](examples/) | 4 complete copy-paste dashboard slides: admin shell, analytics overview, data-table page, detail+form page. |

## Workflow when asked to "make a dashboard slide"

1. Confirm the project is a Slidev project and the setup in `setup.md` is in place (or add it).
2. Pick the closest example in `examples/` as a skeleton.
3. Choose the navigation pattern from `navigation.md` (sider menu is the default for admin dashboards).
4. Lay out content on the grid per `dashboard-rules.md`; pick components from `components.md`.
5. Wrap in `<AntdThemeProvider>`, set the slide `layout: full`, verify it fits the canvas (`npm run dev`).
