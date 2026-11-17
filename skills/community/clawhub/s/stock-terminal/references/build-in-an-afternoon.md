# Build a local chat-and-canvas terminal

Build one useful local research app: chat thread on the left, a validated financial canvas on the right.
The intended four-hour sequence is a planning target, not a measured delivery guarantee.
Use the installed skill tree as the specification. No separate example product or private repository is needed.
Do not spend the afternoon reproducing every possible data widget.

## Deliverable and prerequisites

Deliver a runnable Electron/React app with home ticker entry, saved threads, one model provider,
the ten core canvas blocks, every public command in the manifest, manual data refresh, and Stop.
A screen explanation must read the same host snapshots the widgets display.
Keep an evidence record of commands, test results, screenshots, and limitations.

Use a supported local Node runtime with ESM, npm, a desktop session, and user-authorized dependency installation.
Pin application dependencies with `--save-exact` and retain the generated lockfile.
The [canvas validator](runtime/canvas-validator.mjs), [stream reducer](runtime/stream-reducer.mjs),
[request cache helper](runtime/request-cache.mjs), and [snapshot adapters](runtime/snapshot-adapters.mjs)
use standard JavaScript globals only. The [file inventory](inventory.json) lists reference files and checksums.
Their installation does not install Electron, React, a provider client, or a JSON Schema test library.
The canvas validator is a strict subset parser; use its supported grammar rather than adding an XML package implicitly.

Live data needs `SENTISENSE_API_KEY` in the main process environment.
A provider turn needs the user's chosen provider connection in that process as well.
Missing credentials must produce a setup state. Do not invent market data or prompt for a secret in chat.
The XML fixtures can run without any key and must remain labeled synthetic.

## 0:00-0:35: shell and first thread

Read [app-shell.md](app-shell.md), scaffold the app, and prove the renderer cannot read Node or credentials.
Use one home input. A ticker navigates to its compact view; a research question creates a thread.
Render a left conversation pane and right artifact pane with a saved-thread rail.
Wire typed IPC methods and a closeable per-turn subscription before adding a model.
Load [stock-snapshot.xml](fixtures/stock-snapshot.xml) through the validator as an explicit fixture mode.

Checkpoint: a running desktop app shows two panes and a synthetic dated screen, with no secret in renderer assets.
Do not begin with portfolios, brokerage setup, billing, a plugin manager, or four provider adapters.

## 0:35-1:15: one shared data read model

Read [commands-and-data.md](commands-and-data.md) and load [commands.json](contracts/commands.json).
Register only manifest operations, including the three host-local tools
`resolve_security`, `read_screen`, and `render_canvas`; do not register them a second time.
Name resolution is a data tool wrapping the documented entity search, not a ticker guess.
Implement the four-read compact ticker recipe and each response adapter it needs.
Use the [request cache helper](runtime/request-cache.mjs) before binding default time windows,
canonical operation/input keys, an in-flight promise map, and successful snapshot cache entries.
Keep explicit user windows exact; expire successful reads after five minutes and bypass them on manual refresh.
The compact view displays the ticker; company identity is an explicit optional fifth profile read.
Retain preview flags, source dates where supplied, fetch times, and typed failures.

Checkpoint: the ticker view displays a delayed quote, chart, Score, and stories from shared snapshots.
Widgets load independently. One failing read leaves the other three usable.
In deterministic mode all fixture values are visibly synthetic; missing live data never falls back silently to those values.

## 1:15-2:00: canvas grammar and native blocks

Read [canvas-grammar.md](canvas-grammar.md) and [blocks-and-rendering.md](blocks-and-rendering.md).
Copy the strict validator, then implement ten allowlisted React components against its AST.
Use operation `displayFields` and the snapshot adapters for live tables and metric selectors.
Resolve live bindings in the host before rendering; model-authored status, source links, and dates are rejected.
Register `render_canvas({xml})` in the host; it validates the whole XML before returning success.
Store source XML in the host, send only the AST to the renderer, and commit at most one successful artifact per turn.
Implement loading, empty, error, preview, and dated stale-narrative states before decorative styling.
Open the [comparison](fixtures/compare.xml) and [daily brief](fixtures/daily-brief.xml) fixtures.

Checkpoint: all three fixtures render; invalid XML returns a typed repair hint while preserving the last good canvas.
Nested rows, unknown blocks, duplicate IDs, or markup must not become permissively rendered content.

## 2:00-2:45: provider loop and public events

Read [runtime-and-stream.md](runtime-and-stream.md) and use [stream-reducer.mjs](runtime/stream-reducer.mjs).
Implement one provider adapter with tool definitions, tool-result continuation, and cancellation where supported.
The provider SDK or HTTP transport is your app's dependency; choose it for the user's available connection and pin it.
The adapter produces internal progress. The host emits only the six versioned event types.
Choose text or canvas before deltas are visible; buffer narrative on canvas turns.
Expose short host-authored tool summaries, not raw tool arguments or partial JSON.

Implement `read_screen` over the same immutable snapshots the renderer uses.
A user asking "why is that chart down?" should get an explanation referencing its visible period and source date.
Let a typed canvas error trigger one bounded repair attempt within the existing turn budget.

Checkpoint: a follow-up reuses the visible evidence without silently replacing it or duplicating canvas prose in chat.
Stopping ends the local turn and discards late results, even when the provider cannot abort its request.

## 2:45-3:25: useful commands

Implement `open`, `compare`, and `daily brief` using manifest recipes and shared request accounting.
The full `open` has six reads; a compact home ticker has four. Do not conflate their budgets.
Expose all recipes marked `exposure: "command"` through the same registry and generic tables or text.
Generate help from those recipes; navigation and internal resolution remain separate.
Translate a natural screening request to a typed plan validated against the field catalog before execution.
If translation needs a model and no provider is connected, request setup rather than sending free text as `plan`.
Offer bounded company-resolution choices and selected-story detail navigation without extra automatic fan-out.
No command may refer to an unregistered operation. Composite requests count all selected legs.
Keep `news` useful with SentiSense story titles; external headline fetching is optional.

Checkpoint: ticker, comparison, brief, options, earnings, screening, and text-only help all route predictably.
A request for one price remains one price read and a short answer.
A missing sibling skill cannot prevent these inline recipes from working.

## 3:25-4:00: verify and hand back

Run [verification.md](verification.md). Capture screenshots of ticker, comparison, text, loading, preview, and error states.
Replay Stop followed by a late artifact and verify no canvas changes after the terminal event.
Refresh one data block; its snapshot fetch time changes while the authored narrative remains visibly dated.
Reopen a saved thread with its original artifact and dates; do not silently regenerate its history.
Audit a synthetic secret canary against renderer bundles, public events, logs, XML, and saved artifacts.
If an optional export feature is implemented, scan its output too; export is not required for this build.

Checkpoint: deliver start/build commands, a lockfile, deterministic checks, screenshots, and explicit unverified live checks.
Record actual elapsed time and any stage that exceeded the target. Do not claim the timing goal passed without measurement.

## Deliberately deferred

- Multiple providers: one working adapter proves the host boundary; more adapters multiply credential and streaming cases.
- Portfolio, brokerage, trading, local-file import, and skill editing: these add permissions and separate product responsibilities.
- Every technical indicator and specialized block: the ten core types plus generic tables answer the initial command surface.
- Deep auto-refresh and polling: manual refresh preserves a comprehensible relationship between new data and old narration.
- External social embeds: source links and cluster titles work without third-party scripts or arbitrary web fetching.
- HTML/PDF export: not needed to answer or reopen a turn; if added later, include its output in the canary sweep.
- Remote deployment and distribution: a working local app is the afternoon deliverable; publication is a separate user decision.
