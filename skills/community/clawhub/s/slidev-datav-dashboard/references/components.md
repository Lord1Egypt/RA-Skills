# DataV (datav-vue3) Component Catalog

Package: **`@kjgl77/datav-vue3`** (v1.7.x) · Docs: https://datav-vue3.netlify.app ·
Live demos: https://datav-vue3-demo.netlify.app · It is a faithful Vue 3 port of
[DataV-Team/DataV](http://datav.jiaminghi.com/), so the original DataV docs/examples still apply.

## How registration & tags work

`app.use(DataVVue3)` registers every component **globally** as `Dv<Name>`. In templates **both**
forms resolve (Vue strips hyphens during resolution):

```html
<DvBorderBox13 />            <!-- PascalCase (recommended in Slidev markdown) -->
<dv-border-box-13 />         <!-- kebab-case -->
```

On-demand import also works: `import { BorderBox13 } from '@kjgl77/datav-vue3'`.

### Two universal rules

1. **Size it.** Every component fills its parent (`width/height: 100%`). If the parent has no
   height, it renders blank. Use `style="width:100%;height:100%"` inside a sized panel, or set px.
2. **Replace, don't mutate (for redraws).** Chart components watch their `config`/`option`
   *reference*. To update, reassign (`config.value = …` on a `reactive`, or replace the array).
   Mutating deeply nested data may not re-render; replacing the field does.

### Border content gotcha (important)

Per the official "边框组件注意事项": a border box renders default-slot children into an inner
`.border-box-content` container. **Wrap chart content placed inside a border in a *component*** (not
raw inline DOM) — slot-mounted DOM can report `width/height: 0` in `onMounted`, breaking charts that
measure themselves. This skill's `DashPanel.vue` does this wrapping for you. To force a box to
re-measure after its parent resizes, call its exposed `initWH()` method (via `ref`) instead of
re-keying it.

---

## 1) Border boxes — `DvBorderBox1` … `DvBorderBox13` (13)

Decorative animated frames. **Common props (all 13):**

| Prop | Type | Default | Notes |
| --- | --- | --- | --- |
| `color` | `string[]` | per box | Two colors: `[main, secondary]`. hex / rgb / rgba / keyword. |
| `backgroundColor` | `string` | `'transparent'` | Fill behind the content. |

```html
<DvBorderBox13 :color="['#1d5cff', '#37e1eb']" background-color="rgba(8,22,48,.55)">
  <YourPanelContent />
</DvBorderBox13>
```

**Per-box character & extras** (pick by vibe; numbers are stable across DataV):

| Tag | Look / use for | Extra props |
| --- | --- | --- |
| `DvBorderBox1` | Ornate corners + dotted frame; hero/title panels | — |
| `DvBorderBox2` | Simple thin rounded frame; dense grids | — |
| `DvBorderBox3` | Double-line techy frame | — |
| `DvBorderBox4` | Angular single-corner accent (asymmetric) | `reverse` (bool, mirror) |
| `DvBorderBox5` | Layered offset frame; medium panels | `reverse` (bool) |
| `DvBorderBox6` | Dotted nodes on corners; compact KPI cards | — |
| `DvBorderBox7` | Subtle thin border + corner ticks; secondary panels | — |
| `DvBorderBox8` | Animated running-light border; "live" panels | `reverse` (bool), `dur` (number, sec) |
| `DvBorderBox9` | Sci-fi cut corners + scanlines; charts | — |
| `DvBorderBox10` | Rounded glow frame; soft cards | — |
| `DvBorderBox11` | Frame **with a centered title bar** | `title` (string), `titleWidth` (number) |
| `DvBorderBox12` | Bracket corners; main content | — |
| `DvBorderBox13` | Clean header-line frame; **best default panel** | — |

Tip: use one "feature" box (1/8/9/11) for the hero/header and a calm box (2/7/12/13) for the rest —
don't mix many ornate frames on one screen.

---

## 2) Decorations — `DvDecoration1` … `DvDecoration12` (12)

Non-data flourishes: lines, dividers, rotating rings, scanning frames. **Common prop (all):**
`color: string[]`. Several add `reverse` (orientation) and/or `dur` (animation seconds); a few wrap
slot content. Always give them a size via `style`.

| Tag | Look / use for | Common props |
| --- | --- | --- |
| `DvDecoration1` | Dotted blocks + pulsing squares; corner accents | `color` |
| `DvDecoration2` | Animated travelling dot along a bar; section dividers | `color`, `reverse` (vertical), `dur` |
| `DvDecoration3` | Grid of blinking dots; texture/background fill | `color` |
| `DvDecoration4` | Thin animated scan line; vertical/horizontal separators | `color`, `reverse`, `dur` |
| `DvDecoration5` | Zig-zag pulse line (EKG-style); under titles | `color`, `dur` |
| `DvDecoration6` | Column of animated bars; ornamental sidebars | `color` |
| `DvDecoration7` | **Title wrapper** — side glyphs around centered slot text | `color` + default slot |
| `DvDecoration8` | Header underline with corner hook; section headers | `color`, `reverse` |
| `DvDecoration9` | **Rotating hexagon ring around slot** content (e.g., a % or icon) | `color`, `dur` + default slot |
| `DvDecoration10` | Horizontal animated travelling line; thin top/bottom rails | `color` |
| `DvDecoration11` | **Framed banner around slot** text; emphasized labels | `color` + default slot |
| `DvDecoration12` | Scanning radar/halo ring around slot; focal accents | `color`, `scanDur`, `haloDur` + slot |

```html
<!-- a centered section title -->
<DvDecoration7 :color="['#2f7cff', '#37e1eb']" style="width:300px;height:40px">运营总览</DvDecoration7>

<!-- a thin animated rail across the top -->
<DvDecoration10 style="width:100%;height:5px" />
```

> Exact extras can vary slightly by version — when in doubt, open the component's page on
> https://datav-vue3.netlify.app and use the "查看代码" demo as ground truth.

---

## 3) Data & chart components ("Other")

These carry data via a single **reactive** object: `:config="{…}"` (most) or `:option="{…}"`
(`DvCharts`). Shapes below are verified against the official demos.

### `DvDigitalFlop` — 数字翻牌器 (animated number)

KPI counters; the staple of any 大屏 header.

`:config` fields: `number: number[]` (required), `content: string` (template, `{nt}` = each number,
e.g. `'{nt} 个'`), `toFixed`, `textAlign` (`'center'|'left'|'right'`), `rowGap`,
`style` (CRender style: `{ fontSize, fill, stroke }`), `formatter(n) => string` (e.g. thousands
separators), `animationCurve`, `animationFrame`.

```html
<DvDigitalFlop :config="{
  number: [128430],
  content: '{nt}',
  formatter: (n) => n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ','),
  style: { fontSize: 42, fill: '#3de7c9' },
}" style="width:100%;height:60px" />
```

### `DvScrollBoard` — 轮播表 (auto-scrolling table)

Logs, alarms, event streams.

`:config` fields: `header: string[]`, `data: string[][]` (rows of cells, HTML allowed),
`rowNum` (visible rows, def 5), `headerBGC` (def `#00BAFF`), `oddRowBGC` (`#003B51`),
`evenRowBGC` (`#0A2732`), `waitTime` (ms, def 2000), `headerHeight` (def 35),
`columnWidth: number[]`, `align: ('left'|'center'|'right')[]`, `index` (show row #), `indexHeader`,
`carousel` (`'single'|'page'`), `hoverPause` (def true).
Events: `@click`, `@mouseover`, `@getFirstRow` → `{ row, ceil, rowIndex, columnIndex }`.

```html
<DvScrollBoard :config="{
  header: ['时间', '区域', '事件', '级别'],
  data: scrollRows,                         // string[][]
  index: true, columnWidth: [60, 140],
  align: ['center','center','left','center'],
}" style="width:100%;height:100%" @click="onRow" />
```

### `DvScrollRankingBoard` — 排名轮播表 (animated ranking bars)

Top-N leaderboards.

`:config` fields: `data: {name, value}[]`, `rowNum` (def 5), `waitTime` (def 2000),
`carousel` (`'single'|'page'`), `unit`, `sort` (auto-sort, def true),
`valueFormatter({name,value,percent,ranking}) => string`, `textColor` (def `#fff`),
`color` (bar+rank color, def `#1370fb`), `fontSize` (def 13).
`name` is rendered with `v-html` → you can pass HTML.

```html
<DvScrollRankingBoard :config="{ data: ranking, unit: '万元' }" style="width:100%;height:100%" />
```

### `DvCapsuleChart` — 胶囊柱图 (horizontal capsule bars)

Compact category comparison with an axis.

`:config` fields: `data: {name, value}[]`, `unit`, `colors: string[]`, `showValue` (bool),
`textColor` (def `#fff`), `fontSize` (def 12), `labelNum` (axis ticks, def 6).

```html
<DvCapsuleChart :config="{
  data: [{name:'南阳',value:167},{name:'郑州',value:75}],
  colors: ['#37a2da','#32c5e9','#67e0e3','#9fe6b8'], unit:'万元', showValue:true,
}" style="width:100%;height:100%" />
```

### `DvActiveRingChart` — 动态环图 (auto-rotating ring + center number)

Single highlighted ratio that cycles through items.

`:config` fields: `radius` (`'50%'`/px), `activeRadius` (`'55%'`/px), `data: {name,value}[]`,
`lineWidth` (def 20), `activeTimeGap` (ms, def 3000), `color: string[]`, `textColor`,
`digitalFlopStyle: { fontSize, fill }`, `digitalFlopToFixed`, `digitalFlopUnit`,
`showOriginValue` (show raw value vs percent), `animationCurve`, `animationFrame`.
Top-level prop `isDigitalFlop` (bool, def true).

```html
<DvActiveRingChart :config="{
  lineWidth: 24,
  data: [{name:'在线',value:980},{name:'离线',value:120}],
  digitalFlopStyle: { fontSize: 22, fill: '#3de7c9' },
}" style="width:100%;height:100%" />
```

### `DvWaterLevelPond` — 水位图 (animated water-level gauge)

Capacity / utilization / progress as a filling wave.

`:config` fields: `data: number[]` (one or more levels; shows the max), `shape`
(`'rect'|'roundRect'|'round'`, def `'rect'`), `colors: string[]` (gradient; repeat a color to
disable gradient; def `['#00BAFF','#3DE7C9']`), `waveNum` (def 3), `waveHeight` (def 40),
`waveOpacity` (def 0.4), `formatter` (def `'{value}%'`).

```html
<DvWaterLevelPond :config="{ data:[66], shape:'roundRect' }" style="width:120px;height:160px" />
```

### `DvPercentPond` — 进度池 (bordered progress bar)

Single 0–100 metric with a glowing border.

`:config` fields: `value` (0–100), `colors: string[]` (gradient; def `['#3DE7C9','#00BAFF']`),
`borderWidth` (def 3), `borderGap` (def 3), `lineDash: number[]` (def `[5,1]`), `textColor`
(def `#fff`), `borderRadius` (def 5), `localGradient` (bool), `formatter` (def `'{value}%'`).

```html
<DvPercentPond :config="{ value: 72 }" style="width:200px;height:60px" />
```

### `DvConicalColumnChart` — 锥形柱图 (conical columns, optional top images)

Ranked conical bars; can place a medal/icon image on top of each.

`:config` fields: `data: {name,value}[]`, `img: string[]` (top images, by rank), `fontSize`
(def 12), `imgSideLength` (def 30), `columnColor` (def `'rgba(0,194,255,0.4)'`), `textColor`
(def `#fff`), `showValue` (bool), `sort` (def true).

```html
<DvConicalColumnChart :config="{ data: ranking, showValue: true }" style="width:100%;height:100%" />
```

### `DvCharts` — 通用图表 (general chart, the workhorse)

A wrapper around [@jiaminghi/charts](http://charts.jiaminghi.com/) (an **ECharts-like but NOT
ECharts** lightweight engine). Pass **`:option`** (not `config`). Auto-resizes on window resize.
Use for line / bar / pie / gauge / radar / scatter / pictorialBar / funnel, etc.

⚠️ **Option dialect differs from ECharts.** Styling uses CRender keys: text color is
`style.fill`, lines use `style.stroke`. Quick reference:

```js
const option = reactive({
  title: { text: '流量趋势', style: { fill: '#fff' } },
  legend: { data: ['流入', '流出'], textStyle: { fill: '#c9e0ff' } },
  xAxis: {
    name: '时', data: ['00','04','08','12','16','20'],
    axisLine: { style: { stroke: '#2b4a6b' } },
    axisLabel: { style: { fill: '#7fa6cc' } },
  },
  yAxis: {
    name: '值', data: 'value',
    axisLine: { style: { stroke: '#2b4a6b' } },
    splitLine: { show: true, style: { stroke: '#16314e' } },
    axisLabel: { style: { fill: '#7fa6cc' } },
  },
  series: [
    { name: '流入', type: 'line', data: [120,180,150,260,230,170], smooth: true,
      lineArea: { show: true, gradient: ['rgba(0,186,255,.45)','rgba(0,186,255,0)'] },
      lineStyle: { stroke: '#00BAFF' } },
    { name: '流出', type: 'bar', data: [80,120,100,160,140,110], gradient: { color: ['#3de7c9','#1d9c87'] } },
  ],
})
```

Pie:
```js
const pie = reactive({
  series: [{ type: 'pie', radius: '55%', data: [{name:'A',value:40},{name:'B',value:30}],
    outsideLabel: { formatter: '{name} {percent}%', style: { fill: '#c9e0ff' } } }],
  color: ['#00BAFF','#3de7c9','#f7b500','#fb7293','#9b8bff'],
})
```

See full option docs: http://charts.jiaminghi.com/config/ · examples: http://charts.jiaminghi.com/example/

### `DvFlylineChart` / `DvFlylineChartEnhanced` — 飞线图 (flyline map)

Geo "flying lines" from points to a center over a **background map image**.

`:config` fields: `points: {name?, text?, position:[x,y], …}[]` (positions are **0–1 relative**
to the bg image), `lines: {source, target, …}[]` (Enhanced), `centerPoint: [x,y]`,
`bgImgUrl` (the map image — **required for a useful map**), `centerPointImg: {url}`,
`pointsImg: {url}`, plus `halo`, `text`, `line`, `k`, `curvature`. Set **`:dev="true"`** while
placing points — it shows coordinates so you can click to read positions.

```html
<DvFlylineChartEnhanced :config="flyConfig" style="width:100%;height:100%" />
```

> You must supply your own map image (`bgImgUrl`). If you have no map asset, use `DvCharts`
> (line/bar/pie/gauge) as the center visual instead — the example deck does this so it runs with
> zero binary assets. Swap in a flyline map when you have one.

### Utilities

| Tag | Purpose | Notes |
| --- | --- | --- |
| `DvLoading` | Loading spinner with text | Default slot = label: `<DvLoading>加载中…</DvLoading>` |
| `DvButton` | Sci-fi styled button (6 variants) | `:config` with `type`; mostly for interactive demos |
| `DvFullScreenContainer` | Scales a 1920×1080 app to fill `window` | ⚠️ **Standalone Vue apps only.** Do **not** use inside Slidev — it conflicts with Slidev's canvas scaling. In Slidev, use `canvasWidth: 1920` + `aspectRatio: '16/9'` instead. |

---

## Picking components by intent

| You want to show… | Use |
| --- | --- |
| A big KPI number that animates | `DvDigitalFlop` (or `DvActiveRingChart` for a ratio) |
| Top-N ranking | `DvScrollRankingBoard` or `DvConicalColumnChart` |
| A live event/alarm/log feed | `DvScrollBoard` |
| Category comparison (compact) | `DvCapsuleChart` |
| Trend over time / distribution | `DvCharts` (line / bar / pie / gauge / radar) |
| A single % / utilization | `DvPercentPond` (bar) or `DvWaterLevelPond` (tank) |
| A geographic map with flows | `DvFlylineChart` / `…Enhanced` (needs a map image) |
| A framed "panel" around any of the above | `DvBorderBox*` via this skill's `DashPanel` |
| Section titles / dividers / accents | `DvDecoration*` |
