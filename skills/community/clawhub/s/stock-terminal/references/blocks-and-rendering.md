# Blocks and rendering

Implement these ten renderers for the afternoon core. The host maps validated AST nodes to native components. It never uses dynamic HTML, runtime component names, or model-selected JavaScript.

Read [canvas grammar](canvas-grammar.md) for parsing and data modes. Read [commands and data](commands-and-data.md) for the snapshot producer behind each `dataRef`.

## Shared component contract

Every renderer accepts `{ id, width, props }`; `narrative` and `callout` also accept `content`. A renderer receives a snapshot resolver from the host, not network credentials and not a general fetch function.

The host passes `snapshot.data` to the adapter only after removing the transport envelope. A bare array and direct object keep their documented shape. A preview envelope contributes its `data` member. A documents envelope contributes its `documents` array. This normalized API payload is adapter input. The adapter's projected `{columns, rows}` output is a separate public render model and must not be passed back through API field paths.

For a live block:

1. Resolve `props.dataRef` from the current surface snapshot store.
2. Confirm that the snapshot operation and normalized inputs match the slot expected by the component.
3. Render its explicit status before reading its value.
4. Show source date and fetch time separately when present.
5. Add a source link only when the normalized snapshot supplies a validated HTTP or HTTPS URL.

Snapshot metadata such as `status`, `sourceUrl`, source time, and fetch time belongs to the host snapshot store. It is never trusted from canvas XML. Run `validateLiveBlockBinding` after resolving an effective refresh binding and before projecting any value. Without a refresh binding, the snapshot id must equal `props.dataRef`. With one, pass the trusted effective snapshot id explicitly.

For an inline synthetic block, show a persistent `TEST DATA` label and its `asOf`. Never remove that label through CSS or a compact layout.

## Core catalog

| Type | Required props or content | Renderer job | Typical snapshot |
|---|---|---|---|
| `section-header` | `title`; optional `subtitle` | Introduce one bounded section | None |
| `narrative` | nonempty text content; optional `title` | Dated authored explanation | None |
| `callout` | `tone`, nonempty text; optional `title` | Emphasize neutral, bullish, bearish, or warning context | None |
| `table` | live `dataRef`, or synthetic `columns`, `rows`, `asOf` | Bounded generic rows with aligned numeric cells | Screener, comparison, disclosures |
| `metric-card` | `label`; live `dataRef` plus `field`, or synthetic `value` plus `asOf` | One labeled scalar | Quote or normalized metric |
| `price-chart` | `ticker`, `range`; live `dataRef`, or synthetic `points` plus `asOf` | One price series | Normalized chart points |
| `sentiment` | `ticker`; live `dataRef`, or synthetic `value` plus `asOf` | Polarity, Score, attention when present | Normalized metric snapshot |
| `news-feed` | `ticker`; live `dataRef`, or synthetic `items` plus `asOf` | Bounded story cards | Ticker story clusters |
| `watchlist` | `title`; live `dataRef`, or synthetic `items` plus `asOf` | Compact ticker rows | Batch prices or screen results |
| `market-mood` | live `dataRef`, or synthetic `score`, `phase`, `asOf` | Market composite and phase | Market mood snapshot |

The prop lists are enforced in [the JSON Schema](contracts/canvas.schema.json) and [runtime validator](runtime/canvas-validator.mjs). Do not add a prop in a component alone. Update all three layers and their fixtures together.

## Data states

Each data renderer implements the same five states.

| Status | Visible behavior |
|---|---|
| `loading` | Stable skeleton or short loading row; preserve panel dimensions |
| `ok` | Render normalized value, source date, and fetch time |
| `empty` | Say the requested window returned no rows; never display zero unless zero was returned |
| `error` | State the short failure kind, such as auth, rate limit, timeout, or coverage |
| `preview` | Render the supplied preview and label it `preview`; mention an upgrade only when truncation blocks the answer |

Keep the last good value during a manual refresh and mark it as refreshing. Replace it atomically after the new snapshot validates. On failure, keep the prior value visibly dated and show the new error beside it.

## Renderer details

### `section-header`

Use a compact title and optional muted subtitle. A heading establishes hierarchy but does not consume a large hero card. Ticker text uses tabular monospace styling.

### `narrative`

Render escaped plain text with paragraph breaks. Links are not inferred from text. The host may support a small safe markdown subset in a later contract, but version 2.0 content remains plain text. Keep the canvas creation date or a specific authored date visible near analysis that can go stale.

### `callout`

Map `tone` to a restrained border and label. Directional colors are reserved for bullish and bearish meaning. `warning` uses an accessible warm color. `neutral` uses the normal border. A callout is explanatory text, never a clickable action.

### `table`

Pin the first column on narrow screens only when it improves identification. Right-align numeric cells, use tabular numerals, cap visible rows, and provide an internal scroll region for overflow. Never execute cell content or treat a string as markup. A live table derives columns and rows from the normalized snapshot adapter rather than evaluating object paths supplied by the model.

Use the shipped adapter in a host module beside the copied `runtime/` directory. Here `currentView`
is already looked up for the authorized thread and current artifact, so its bindings are not a global block-ID map:

```js
import {
  projectSnapshotTable,
  validateLiveBlockBinding,
} from './runtime/snapshot-adapters.mjs';

const binding = validateLiveBlockBinding(commands, snapshot, block, {
  effectiveSnapshotId: currentView.bindings.get(block.id) ?? block.props.dataRef,
});
if (!binding.ok) return renderDataError(binding.error);

const table = projectSnapshotTable(commands, snapshot);
if (!table.ok) return renderDataError(table.error);
return renderTable(table.columns, table.rows);
```

The default projection uses only the operation's allowlisted collection fields. A host can pass an explicit `fields` list of allowlisted keys to make a narrower table. It cannot supply object paths. All selected fields must come from one documented collection, and every cell must be a primitive or null. Missing and null stay missing; they never become zero or an empty string. The adapter caps rows at 25 by default, accepts an explicit limit from 1 to 100, caps table strings at 1,024 code units, and rejects duplicate fields, nested objects, arrays, non-finite numbers, and oversized strings.

Worked projections from normalized payloads:

| Operation | Normalized `snapshot.data` | Suggested field keys | Output row |
|---|---|---|---|
| `insider_trades` | `[{insiderName, transactionDate, transactionCode, transactionType, sharesTransacted, totalValue}]` | `insiderName`, `transactionCode`, `totalValue` | `{insiderName, transactionCode, totalValue}` |
| `analyst_actions` | `[{actionDate, firm, actionType, fromGrade, toGrade}]` | `actionDate`, `firm`, `toGrade` | `{actionDate, firm, toGrade}` |
| `institutional_holders` | `{reportDate, holders:[{filerName, shares, valueUsd, changeType, sharesChangePct}]}` | `filerName`, `shares`, `changeType`, `sharesChangePct` | `{filerName, shares, changeType, sharesChangePct}` |
| `screener_execute` | `{matched, results:[{ticker, sentiSenseScore7D, currentPrice, changePercent, analystTargetUpsidePct}]}` | `ticker`, `score7D`, `currentPrice`, `changePercent` | `{ticker, score7D, currentPrice, changePercent}` |

### `metric-card`

The live renderer reads the allowlisted `field` from the snapshot adapter for that operation. Do not apply an arbitrary dotted path. Format price, percentage, count, and date fields in the adapter. Keep the label and age visible. Two cards may share one snapshot without adding requests.

Call `getDisplayField(commands, snapshot, block.props.field)` after binding validation. A collection field is rejected rather than silently choosing the newest row. A missing or null field returns `{value: null, missing: true}`. A metric string is capped at 4,096 code units, and objects, arrays, non-finite numbers, and longer strings are rejected with a typed error.

`displayFields` in `contracts/commands.json` is the per-operation selector allowlist. Each entry has the public key a block may request, the path inside normalized `snapshot.data`, and its label. The list is deliberately nonexhaustive. Add a field to the manifest and its tests before a renderer can expose it.

### `price-chart`

Plot one line with a single data color. Show ticker, range, latest dated point, and delayed-data annotation. The binding validator checks both ticker and range against normalized snapshot inputs, so a requested `1Y` panel cannot silently display a cached `1M` response. Validate all values as finite numbers before they enter the chart library. Break gaps rather than interpolating across missing values. The basic renderer needs no technical indicators.

### `sentiment`

Sentiment is polarity in `[-1, 1]`; preserve its sign and do not remap it to 0 to 100. SentiSense Score is a separate unbounded value and must not be capped or normalized. Render the metrics carried by the snapshot and omit unavailable optional fields with an explicit reason.

### `news-feed`

Render bounded story clusters with title, source, publication time, and safe source link when supplied. Do not render article HTML. Story detail is a user-selected follow-up and should reuse the command contract rather than prefetching every body. A ticker news block must bind to `ticker_stories` with the same normalized ticker input. The global `stories` operation has no ticker input, so use a table projection for that feed rather than inventing a ticker binding.

### `watchlist`

Render ticker, signed move, and one optional value or label. The block is a view, not a portfolio and not an order surface. A general screen result can use this renderer when each row remains compact; use `table` for richer columns.

### `market-mood`

Render the market score, phase, weekly change, and sub-signals only when those fields exist in the normalized snapshot. Keep sector data below the headline rather than creating a second giant hero. The current headline fields carry no top-level as-of, so say `source date not supplied`; do not borrow a history row date or the fetch time.

## Source time contract

Read the operation's `asOf` object in `contracts/commands.json`; do not infer a source time from a field name. `getSnapshotAsOf` returns a typed value only when the declared path and unit validate. Row-level contracts return `rowLevel: true` because one list-level date would misstate the evidence.

- `market-observation` dates the underlying quoted market value. For stock and ETF quotes this is optional `priceAsOf`. Their `timestamp` is response serve time and is never a substitute.
- `dataset-generation` dates a generated or refreshed dataset, such as analyst consensus, a company profile, a market summary, or the earnings calendar. It does not turn a reference price into a live quote.
- `market-session` names the trading session represented by end-of-day analytics.
- `state-computed` dates a computed state such as whether the market is open.
- `report-period` names the reporting quarter actually served. It is not a fetch time.
- `row-time` means each row carries an event, publication, generation, or observation date. Keep that date on its row.
- `none` means the operation supplies no defensible top-level source time. Display fetch time separately and label the source time as unavailable.

`fetchedAt` is always host metadata and only says when this application completed the read. It cannot fill an absent operation as-of. In particular, Market Mood and story lists have no top-level source date. Story rows use `cluster.clusteredAt`; a quote's `timestamp` is serve time; and a market summary's `lastUpdated` is serve time while `generatedAt` dates the analysis.

## Layout

Use a two-pane research layout on desktop: chat at roughly 42 percent and canvas in the remaining pane. Stack panes at narrow widths. Canvas rows switch to one column before a card clips; the AST width describes desktop intent, not an instruction to force narrow columns.

Recommended neutral tokens:

```css
:root {
  --bg: #0a0a0f;
  --surface: #0d1117;
  --border: #1c2230;
  --text: #f5f5f7;
  --muted: #8e8e93;
  --action: #f5f1e6;
  --data: #3182ce;
  --positive: #30d158;
  --negative: #ff453a;
  --panel-radius: 2px;
  --message-radius: 8px;
}
```

Use sans-serif for prose and monospace for tickers and tables. Set `font-variant-numeric: tabular-nums`. Keep data panels flat with one-pixel borders and compact spacing. Use short opacity transitions for loading and value replacement.

Avoid neon glow, rainbow charts, gradients behind data, oversized hero cards, heavy shadows inside the grid, decorative motion, and all-caps labels on every row. Screenshots used for QA should look like a research tool with dense readable evidence, not a product demo backdrop.

## Native component registry

Keep an explicit frozen map:

```js
const renderers = Object.freeze({
  'section-header': SectionHeader,
  narrative: Narrative,
  callout: Callout,
  table: DataTable,
  'metric-card': MetricCard,
  'price-chart': PriceChart,
  sentiment: SentimentPanel,
  'news-feed': NewsFeed,
  watchlist: Watchlist,
  'market-mood': MarketMood,
});
```

The validator rejects a type outside this registry. The renderer should also fail closed if its registry and contract somehow drift. Render a typed local error and retain the last good canvas.

## Acceptance checks

- All three valid XML fixtures render without console errors.
- Together, the fixtures exercise all ten core block types.
- Every fixture shows its synthetic label and fixed date.
- Loading, empty, error, preview, and refresh states preserve layout.
- Two-card and three-card rows stack before clipping.
- Keyboard focus reaches source links and scrollable tables.
- Text and colors meet accessible contrast at normal zoom.
- No raw XML or block content enters `innerHTML`.
- A bad block never blanks the last good canvas.
- `read_screen` returns the normalized values that the same components display.

These checks establish deterministic renderer behavior. Capture desktop and narrow screenshots during the separate fresh-builder exercise; fixture tests alone do not establish visual quality.
