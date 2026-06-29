# ant-design-vue components — full reference (dashboard lens)

Every component in **ant-design-vue v4**, grouped as on antdv.com, with its globally-registered **`a-` tag**, the props you actually reach for, and **how it's used in a dashboard**. Components most central to dashboards are marked ⭐ and expanded with snippets.

Conventions:
- Two-way binding is `v-model:value` (inputs/selects/pickers), `v-model:checked` (switch/checkbox), `v-model:selectedKeys`/`v-model:openKeys` (menu), `v-model:open` (modal/drawer), `v-model:current` (steps).
- Render props become **named slots**; events are Vue events (`@change`, `@click`).

---

## Dashboard cheat-sheet (need → component)

| You need… | Use |
|---|---|
| App frame (nav + header + content) | `a-layout` + `a-layout-sider`/`-header`/`-content` ⭐ |
| Primary navigation | `a-menu` (inline sider) ⭐ |
| "You are here" path | `a-breadcrumb` |
| Page-level view switch | `a-tabs` or `a-segmented` |
| KPI number | `a-statistic` in an `a-card` ⭐ |
| Tabular data | `a-table` ⭐ |
| Key-value record summary | `a-descriptions` |
| Status / category label | `a-tag`, `a-badge` |
| Trend / distribution / gauge | `<v-chart>` (ECharts) — antd has no charts |
| Filters bar | `a-select` + `a-range-picker` + `a-input-search` in an `a-space`/`a-form` inline |
| Completion / quota | `a-progress` |
| Row actions | `a-dropdown` + `a-popconfirm` |
| Detail/edit without leaving page | `a-drawer` or `a-modal` |
| Loading / empty mock states | `a-skeleton`, `a-spin`, `a-empty` |
| User identity | `a-avatar`, `a-avatar-group` |
| Activity / audit log | `a-timeline`, `a-list` |

---

## General

| Component | Tag | Key props / slots | Dashboard use |
|---|---|---|---|
| Button ⭐ | `a-button` | `type` primary\|default\|dashed\|text\|link, `danger`, `size`, `loading`, `ghost`, `block`, `shape` round\|circle, `#icon` | Actions. **≤1 `primary` per region**; `text`/`link` for low-emphasis; `danger` for destructive. |
| FloatButton | `a-float-button`, `a-float-button-group`, `a-back-top` | `type`, `shape`, `tooltip`, `badge`, `#icon` | Persistent "＋ New", help, back-to-top on long pages. |
| Typography | `a-typography-title` (`:level`), `a-typography-text`, `a-typography-paragraph`, `a-typography-link` | `type` secondary\|success\|warning\|danger, `ellipsis`, `copyable`, `code`, `strong` | Section titles, truncating long IDs/URLs, inline code. |
| Icon | `<user-outlined/>`, `<dashboard-outlined/>`, … (from `@ant-design/icons-vue`) | three themes: `*Outlined`, `*Filled`, `*TwoTone`; styleable via `style`/`spin`/`rotate` | Menu items, button icons, statistic prefixes, status. Registered globally by `main.ts`. |

---

## Layout

⭐ **Layout** — the dashboard shell. `a-layout-sider` is collapsible and is where the menu lives.

```html
<a-layout style="height: 100%">
  <a-layout-sider v-model:collapsed="collapsed" collapsible :width="220" theme="dark">
    <div class="logo">Acme</div>
    <!-- a-menu here -->
  </a-layout-sider>
  <a-layout>
    <a-layout-header style="background:#fff; padding:0 16px">…top bar…</a-layout-header>
    <a-layout-content style="padding:16px; overflow:auto">…work area…</a-layout-content>
  </a-layout>
</a-layout>
```

| Component | Tag | Key props | Use |
|---|---|---|---|
| Layout ⭐ | `a-layout`, `a-layout-header`, `a-layout-sider`, `a-layout-content`, `a-layout-footer` | sider: `collapsible`, `v-model:collapsed`, `collapsedWidth`, `width`, `breakpoint`, `theme` dark\|light | App frame. One per dashboard. |
| Grid ⭐ | `a-row`, `a-col` | row: `:gutter="[h,v]"`, `justify`, `align`, `wrap`; col: `:span` (of 24), `:offset`, `:xs/:sm/:md/:lg/:xl/:xxl`, `flex` | The layout backbone — **all content sits here**. KPI cards `:span="6"` (4-up) or `:span="8"` (3-up). |
| Flex | `a-flex` | `vertical`, `justify`, `align`, `gap`, `wrap` | Quick 1-D rows/columns (toolbars, header clusters) without writing CSS. |
| Space | `a-space` | `:size`, `direction`, `wrap`, `align`, `#split` | Inline gaps between buttons/tags/filters — preferred over margins. |
| Divider | `a-divider` | `orientation`, `dashed`, `type` vertical, `#default` (text) | Separate sections or inline action groups. |

---

## Navigation

⭐ **Menu** — primary nav, almost always `mode="inline"` in the sider. See [navigation.md](navigation.md) for design rules. Slot form is most readable in slides:

```html
<a-menu v-model:selectedKeys="sel" v-model:openKeys="open" mode="inline" theme="dark">
  <a-menu-item key="dash"><dashboard-outlined /> Overview</a-menu-item>
  <a-sub-menu key="sales">
    <template #title><line-chart-outlined /> Sales</template>
    <a-menu-item key="orders">Orders</a-menu-item>
    <a-menu-item key="invoices">Invoices</a-menu-item>
  </a-sub-menu>
  <a-menu-item key="settings"><setting-outlined /> Settings</a-menu-item>
</a-menu>
```

| Component | Tag | Key props | Use |
|---|---|---|---|
| Menu ⭐ | `a-menu`, `a-menu-item`, `a-sub-menu`, `a-menu-item-group`, `a-menu-divider` | `mode` inline\|vertical\|horizontal, `theme`, `v-model:selectedKeys`, `v-model:openKeys`, `:items`, `inlineCollapsed` | Sider nav (inline) or top nav (horizontal). Keep on local state, not Slidev's router. |
| Breadcrumb | `a-breadcrumb`, `a-breadcrumb-item` | `:items`, `separator`, `#title` | Page location for ≥2-level IA; sits in/under the header. |
| Dropdown | `a-dropdown`, `a-dropdown-button` | `trigger` hover\|click, `placement`, `#overlay` (a-menu) | Row "⋯" actions, user-account menu, "More" buttons. |
| Pagination | `a-pagination` | `:total`, `v-model:current`, `:pageSize`, `showSizeChanger`, `showQuickJumper`, `simple` | Under tables/lists (often via the table's own `:pagination`). |
| Steps | `a-steps`, `a-step` | `v-model:current`, `status`, `direction`, `size`, `:percent`, `progressDot`, `type` navigation | Wizards, onboarding, pipeline/stage status. |
| Anchor | `a-anchor`, `a-anchor-link` | `:items`, `affix`, `direction` | In-page jump nav on long settings/detail pages. |

---

## Data Entry

A dashboard's **filter bar** is usually `a-input-search` + `a-select` + `a-range-picker` in an inline `a-form` or `a-space`.

```html
<a-form layout="inline">
  <a-form-item><a-input-search placeholder="Search…" style="width:220px" /></a-form-item>
  <a-form-item>
    <a-select v-model:value="status" style="width:140px" :options="statusOpts" placeholder="Status" />
  </a-form-item>
  <a-form-item><a-range-picker /></a-form-item>
  <a-form-item><a-button type="primary">Apply</a-button></a-form-item>
</a-form>
```

| Component | Tag | Key props | Use |
|---|---|---|---|
| Form | `a-form`, `a-form-item` | `layout` horizontal\|vertical\|inline, `:model`, `:rules`, `:labelCol`/`:wrapperCol`, `validateTrigger` | All forms; **inline** layout for filter bars, **vertical** for create/edit. |
| Input | `a-input`, `a-input-password`, `a-input-search`, `a-textarea`, `a-input-group` | `v-model:value`, `allowClear`, `#prefix`/`#suffix`, `:maxlength`, `size`, `addonBefore` | Text fields, search bars. |
| InputNumber | `a-input-number` | `:min`/`:max`/`:step`, `:formatter`/`:parser`, `addonAfter` | Thresholds, prices, quantities. |
| Select ⭐ | `a-select`, `a-select-option`, `a-select-opt-group` | `v-model:value`, `:options`, `mode` multiple\|tags, `showSearch`, `:loading`, `maxTagCount`, `allowClear` | The default filter control. |
| DatePicker ⭐ | `a-date-picker`, `a-range-picker`, `a-month-picker`, `a-week-picker` | `picker` date\|week\|month\|quarter\|year, `:presets`, `showTime`, `format`, `valueFormat` | **Date-range filter** — present on most dashboards. |
| TimePicker | `a-time-picker` | `format`, `use12Hours`, `:minuteStep` | Schedules, cutoffs. |
| Checkbox | `a-checkbox`, `a-checkbox-group` | `v-model:checked`, `:options`, `indeterminate` | Multi-filters, bulk-select headers, settings. |
| Radio | `a-radio`, `a-radio-group`, `a-radio-button` | `v-model:value`, `optionType` button, `:options`, `button-style` solid | Mutually-exclusive view toggles, small segmented choices. |
| Switch | `a-switch` | `v-model:checked`, `checkedChildren`/`unCheckedChildren`, `:loading`, `size` | Feature flags, on/off settings, table-row enable. |
| Slider | `a-slider` | `range`, `:marks`, `:min`/`:max`/`:step`, `:tooltip` | Threshold/range tuning, price filters. |
| Cascader | `a-cascader` | `:options`, `multiple`, `showSearch`, `changeOnSelect` | Region / category / org hierarchy pickers. |
| TreeSelect | `a-tree-select` | `:treeData`, `treeCheckable`, `multiple`, `showSearch`, `treeDefaultExpandAll` | Hierarchical filter (org units, nested categories). |
| AutoComplete | `a-auto-complete` | `:options`, `filterOption`, `backfill` | Search-with-suggestions. |
| Mentions | `a-mentions` | `:options`, `prefix`, `split` | @-mention comment boxes. |
| Rate | `a-rate` | `:count`, `allowHalf`, `:character` | Review/quality scores. |
| Transfer | `a-transfer` | `:dataSource`, `v-model:targetKeys`, `:titles`, `showSearch`, `#render` | Column choosers, role/permission assignment. |
| Upload | `a-upload`, `a-upload-dragger` | `listType` text\|picture\|picture-card, `v-model:fileList`, `:multiple`, `:beforeUpload` | Data import, attachments, avatars. |

---

## Data Display

⭐ **Statistic** in **Card** = the KPI tile, the heart of an overview dashboard.

```html
<a-card :bordered="false">
  <a-statistic title="MRR" :value="48230" :precision="0" prefix="$" :value-style="{ color:'#3f8600' }">
    <template #suffix><span style="font-size:14px"> <arrow-up-outlined /> 12%</span></template>
  </a-statistic>
</a-card>
```

⭐ **Table** — the data workhorse. Columns are a prop; custom cells use the `#bodyCell` slot.

```html
<a-table :columns="columns" :data-source="rows" row-key="id" size="small"
         :pagination="{ pageSize: 8 }" :scroll="{ y: 320 }">
  <template #bodyCell="{ column, record }">
    <template v-if="column.key === 'status'">
      <a-badge :status="record.ok ? 'success' : 'error'" :text="record.status" />
    </template>
    <template v-else-if="column.key === 'action'">
      <a-space>
        <a><edit-outlined /> Edit</a>
        <a-popconfirm title="Delete?"><a class="text-red-500"><delete-outlined /></a></a-popconfirm>
      </a-space>
    </template>
  </template>
</a-table>
```

| Component | Tag | Key props | Use |
|---|---|---|---|
| Card ⭐ | `a-card`, `a-card-grid`, `a-card-meta` | `title`, `#extra`, `:bordered`, `hoverable`, `:loading`, `size`, `:tabList`, `:actions` | Container for every panel — KPIs, charts, lists. `:bordered="false"` on tinted backgrounds. |
| Statistic ⭐ | `a-statistic`, `a-statistic-countdown` | `title`, `:value`, `:precision`, `prefix`/`suffix`, `:valueStyle` | KPI numbers; color the value to encode up/down. |
| Table ⭐ | `a-table`, `a-table-column`, `a-table-column-group` | `:columns`, `:data-source`, `row-key`, `:pagination`, `:rowSelection`, `:scroll`, `:expandable`, `:loading`, `sticky`, `#bodyCell`/`#headerCell`/`#summary` | Lists of records. Use `size="small"` + `:scroll` on slides. |
| Descriptions | `a-descriptions`, `a-descriptions-item` | `:column`, `bordered`, `size`, `layout`, `title` | Read-only key-value record summary (detail pages). |
| Tabs | `a-tabs`, `a-tab-pane` | `v-model:activeKey`, `type` line\|card\|editable-card, `tabPosition`, `size`, `centered`, `:items` | Segment a page into views without navigating away. |
| Segmented | `a-segmented` | `v-model:value`, `:options`, `block`, `size` | Compact view/time-range switch (Day/Week/Month). |
| Tag | `a-tag`, `a-check-tag` | `color` (preset name or hex), `closable`, `:bordered`, `#icon` | Status, categories, active filters. Preset colors carry meaning. |
| Badge | `a-badge`, `a-badge-ribbon` | `:count`, `dot`, `status` success\|processing\|error\|warning\|default, `color`, `:overflowCount` | Notification counts, status dots, "New" ribbons. |
| Avatar | `a-avatar`, `a-avatar-group` | `size`, `shape` circle\|square, `src`, `#icon`, `:maxCount` | User cells, headers, assignee stacks. |
| List | `a-list`, `a-list-item`, `a-list-item-meta` | `:dataSource`, `:grid`, `:pagination`, `:loadMore`, `size`, `#renderItem` | Activity feeds, item lists, card grids. |
| Timeline | `a-timeline`, `a-timeline-item` | `mode` left\|right\|alternate, `color`, `:pending`, `#label` | Audit logs, deployment/order history. |
| Collapse | `a-collapse`, `a-collapse-panel` | `v-model:activeKey`, `accordion`, `ghost`, `bordered` | Grouped/advanced filters, FAQ, foldable detail sections. |
| Tree | `a-tree`, `a-directory-tree` | `:treeData`, `checkable`, `draggable`, `v-model:expandedKeys`, `v-model:selectedKeys` | File browsers, org charts, category trees. |
| Tooltip | `a-tooltip` | `title`, `placement`, `color` | Hints on truncated text or icon-only buttons. |
| Popover | `a-popover` | `#content`, `title`, `trigger`, `placement` | Richer hover/click detail than a tooltip. |
| Statistic countdown | `a-statistic-countdown` | `:value` (timestamp), `format` | SLA timers, sale countdowns. |
| Calendar | `a-calendar` | `:fullscreen`, `#dateCellRender`, `v-model:value`, `mode` | Schedule / booking / heatmap views. |
| Image | `a-image`, `a-image-preview-group` | `:preview`, `:fallback`, `width` | Media thumbnails with zoom. |
| Carousel | `a-carousel` | `autoplay`, `dots`, `effect` | Rotating highlights (use sparingly). |
| Empty | `a-empty` | `:image`, `description`, `#default` | Empty states inside cards/tables. |
| QRCode | `a-qrcode` | `:value`, `:size`, `:icon`, `status` | Share links, mobile handoff. |
| Tour | `a-tour` | `v-model:open`, `:steps`, `v-model:current` | Feature onboarding overlays. |

---

## Feedback

| Component | Tag / API | Key props | Use |
|---|---|---|---|
| Progress ⭐ | `a-progress` | `type` line\|circle\|dashboard, `:percent`, `status` success\|exception\|active, `:steps`, `:strokeColor` | Quota usage, goal completion, gauges in KPI cards. |
| Alert | `a-alert` | `type` success\|info\|warning\|error, `banner`, `showIcon`, `closable`, `#action`, `description` | Inline status/announcement banners atop a page. |
| Skeleton ⭐ | `a-skeleton`, `a-skeleton-button`/`-input`/`-image`/`-avatar` | `active`, `:loading`, `:paragraph`, `:title`, `:avatar` | Loading placeholders — great for "loading state" mockups. |
| Spin | `a-spin` | `:spinning`, `tip`, `:delay`, `size`, `#indicator` | Wrap a panel to show it loading. |
| Result | `a-result` | `status` success\|error\|info\|warning\|403\|404\|500, `title`, `subTitle`, `#extra` | Empty/permission/error full-panel states. |
| Modal | `a-modal` + `Modal.confirm/info/success/error/warning` | `v-model:open`, `:width`, `:footer`, `:confirmLoading`, `centered` | Dialogs, confirmations, quick create/edit. |
| Drawer | `a-drawer` | `v-model:open`, `placement`, `:width`, `:mask`, `#extra` | Slide-in detail/edit panel, off-canvas filters. |
| Popconfirm | `a-popconfirm` | `title`, `okText`, `@confirm`, `#icon` | Inline confirm for destructive row actions. |
| Message | `message` API | `message.success/error/info/warning/loading()` | Transient toast feedback after an action. |
| Notification | `notification` API | `notification.open({ message, description, placement })` | System/async notices (top-right). |
| Watermark | `a-watermark` | `:content`, `:font`, `:gap` | Mark mockups "DEMO" / "Confidential". |

> `message`/`Modal`/`notification` are imperative. Wrap your root in `a-app` (AntdThemeProvider already does) so they pick up theme + context.

---

## Other / system

| Component | Tag / import | Purpose |
|---|---|---|
| ConfigProvider ⭐ | `a-config-provider` | Theming root: `:theme="{ token, algorithm, components }"`, `componentSize`, `locale`, `direction`, `:getPopupContainer`. Used by `AntdThemeProvider.vue`. |
| App | `a-app` | Provides context for `message`/`Modal`/`notification` and a base reset. Wrap dashboard root. |
| Theme tokens | `import { theme } from 'ant-design-vue'` | `theme.defaultAlgorithm` / `darkAlgorithm` / `compactAlgorithm`; `theme.useToken()` to read tokens in a component. Use `compactAlgorithm` for dense dashboards. |
| Affix | `a-affix` | `:offsetTop`, `:target` — pin a toolbar while scrolling (limited value on a fixed slide). |
| Grid breakpoints | `Grid.useBreakpoint()` | Reactive breakpoint map for responsive layout logic. |

---

## Picking among similar components

- **Tabs vs Segmented vs Radio.Group:** Tabs = switch *page content*; Segmented = compact in-card switch (time range, chart type); Radio.Group(button) = a form field with mutually-exclusive options.
- **Tag vs Badge:** Tag = a labeled chip (category/status with text); Badge = a count or a small status dot attached to something.
- **Card vs Descriptions vs Statistic:** Card = container; Descriptions = many key-value pairs; Statistic = one headline number.
- **Modal vs Drawer:** Modal = short, focused confirm/create; Drawer = larger detail/edit or many fields, keeps page context visible behind it.
- **Table vs List:** Table = comparable columns across rows; List = heterogeneous items / feed where columns don't align.
- **Dropdown vs Popover:** Dropdown = a menu of *actions*; Popover = arbitrary *content*.
