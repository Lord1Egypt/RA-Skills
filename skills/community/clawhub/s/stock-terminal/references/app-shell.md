# App shell and trust boundary

Keep credentials, HTTP, provider calls, and persistence in Electron's main process.
The renderer receives validated view data and six host events, not a general-purpose network or filesystem bridge.
This is an implementation recipe, not a prebuilt application.

## Small source layout

```text
app/
  package.json
  package-lock.json
  main/index.mjs
  main/preload.cjs
  main/operations.mjs
  main/provider.mjs
  main/turns.mjs
  main/snapshots.mjs
  main/history.mjs
  renderer/index.html
  renderer/main.jsx
  renderer/App.jsx
  renderer/blocks.jsx
  renderer/theme.css
  contracts/                 copy from this reference kit
  runtime/                   copy the shipped neutral modules
```

Use Vite for the React renderer, with explicit input and output paths and a relative production asset base.
Install Electron and Vite as development dependencies, React and ReactDOM as runtime dependencies;
use `npm install --save-exact` or `--save-dev --save-exact` as appropriate and retain the lockfile.
Configure `dev:renderer`, `dev:desktop`, `build:renderer`, `start`, and `test` scripts in the new app.
The production `start` must load the renderer's built local HTML without depending on a development server.

Launch Electron from a terminal that already has the authorized environment available:

```bash
npm run dev:renderer
# In another terminal inheriting SENTISENSE_API_KEY and the chosen provider environment:
npm run dev:desktop
```

A desktop icon launch may not inherit shell variables. Do not claim otherwise or paste keys into renderer configuration.
For the first local build, document terminal launch and a missing-key setup state.
A later packaged app can add OS credential storage as a separate deliberate implementation.

## BrowserWindow and preload

Use an absolute preload path computed from the main module's directory.
Set `contextIsolation: true`, `nodeIntegration: false`, `sandbox: true`, and `webSecurity: true`.
The renderer is local content; a development HTTP URL must be a fixed loopback origin controlled by the app.
Do not accept a model-supplied URL as the window location.
Deny new windows and navigation away from the fixed renderer location.
Open a validated public source URL in the system browser through a separate host allowlist method.
Never load a remote article into the privileged application window.

Expose a small bridge, shaped like this CommonJS preload:

```js
const { contextBridge, ipcRenderer } = require('electron');
contextBridge.exposeInMainWorld('terminal', {
  startTurn: input => ipcRenderer.invoke('terminal:start-turn', input),
  stopTurn: turnId => ipcRenderer.invoke('terminal:stop-turn', { turnId }),
  readView: input => ipcRenderer.invoke('terminal:read-view', input),
  refreshSnapshot: ({ threadId, snapshotId }) => ipcRenderer.invoke('terminal:refresh', { threadId, snapshotId }),
  listThreads: () => ipcRenderer.invoke('terminal:list-threads'),
  openThread: threadId => ipcRenderer.invoke('terminal:open-thread', { threadId }),
  onEvent: listener => {
    const handler = (_event, payload) => listener(payload);
    ipcRenderer.on('terminal:event', handler);
    return () => ipcRenderer.removeListener('terminal:event', handler);
  },
});
```

Validate each IPC input again in the main handler and verify its sender belongs to the expected window/main frame.
Emit only schema-validated host events to that owning frame. The renderer accepts events only for known turn IDs
in its active thread and disposes the subscription on thread change or unmount. Route concurrent turns by ID, not arrival order.
`readView` accepts a known view ID and validated ticker inputs, never an arbitrary REST path.
`refreshSnapshot({threadId, snapshotId})` accepts only a snapshot already belonging to that thread's current view.
The main handler looks up both IDs in host storage and checks membership against the current artifact
and its effective refresh bindings before any HTTP request. Reject unknown or cross-thread IDs with a controlled
error. A supplied thread ID is a selector, not proof of ownership; also verify the owning window/main frame.
Thread IDs are opaque values looked up in host storage, never path fragments.
Bound strings, input arrays, concurrent turns, and stored history size.
Do not expose `invoke(channel, args)`, SDK namespace reflection, shell commands, or a filesystem API.

## Host operation boundary

Keep one operation map from [commands.json](contracts/commands.json).
Validate a model tool's ID and arguments before matching it to that map.
Construct URLs from the fixed origin `https://app.sentisense.ai` and the operation's documented path/query.
Parse with `new URL()` and check HTTPS and the exact hostname before reading or attaching the API key.
Reject alternate origins, ports, userinfo, and redirects; the origin is not configurable through environment or input.
Encode path inputs as single path segments, validate time ranges, and cap list limits.
A caller cannot supply a scheme, hostname, headers, or credential value.

The HTTP helper reads `process.env.SENTISENSE_API_KEY` only inside the main process.
It adds `X-SentiSense-API-Key` and a runtime `User-Agent` containing `stock-terminal`.
Reject redirects on API reads so an allowed host cannot forward the credential elsewhere.
Use request timeouts and an abort signal, bounded response bodies, and controlled concurrency.
Parse JSON and normalize it with the operation-specific adapter before caching.
Keep upstream error bodies and transport objects host-local; emit a controlled failure code and short summary.
Never log request headers, raw model input, credentials, or provider response dumps.

This host-only request builder validates the destination before accessing the credential:

```js
const API_ORIGIN = 'https://app.sentisense.ai';
function sentisenseApiUrl(path, query = {}) {
  const url = new URL(path, API_ORIGIN);
  if (url.protocol !== 'https:' || url.hostname !== 'app.sentisense.ai' ||
      url.origin !== API_ORIGIN || url.port || url.username || url.password) {
    throw new Error('Unsupported API origin');
  }
  for (const [name, value] of Object.entries(query)) {
    if (value !== null && value !== undefined) url.searchParams.set(name, String(value));
  }
  return url;
}
function sentisenseRequest(path, query = {}) {
  const url = sentisenseApiUrl(path, query);
  const key = process.env.SENTISENSE_API_KEY;
  if (!key) throw new Error('SENTISENSE_API_KEY is not set');
  return {
    url,
    init: {
      headers: { 'X-SentiSense-API-Key': key, 'User-Agent': 'LocalTerminal/1.0 (stock-terminal)' },
      redirect: 'error',
    },
  };
}
```

Keep the returned request host-private. Add the registered operation's method, validated body, timeout,
and abort signal in the transport handler; never spread caller-supplied headers or redirect settings into it.

Use a public snapshot projection explicitly assembled from allowed values:

```js
function publicSnapshot(snapshot) {
  return {
    id: snapshot.id,
    operationId: snapshot.operationId,
    inputs: snapshot.safeInputs,
    fetchedAt: snapshot.fetchedAt,
    sourceDate: snapshot.sourceDate ?? null,
    status: snapshot.status,
    isPreview: snapshot.isPreview,
    previewReason: snapshot.previewReason ?? null,
    data: snapshot.validatedDisplayData,
  };
}
```

These are host read-model fields, not claims about API response field names.
`safeInputs` and `validatedDisplayData` must be allowlisted operation by operation before this projection.
Use each operation's `displayFields` and `asOf` contract plus [snapshot adapters](runtime/snapshot-adapters.mjs).
Populate a whole-snapshot `sourceDate` only from its non-row `asOf` contract, retaining the kind and meaning
in the displayed label. A report quarter, session date, computed state, and generation time mean different things.
A response serve timestamp is not a source as-of; a row event/report date stays on its row.
Keep `sourceDate: null` for undated snapshots and row-only dates; label the missing as-of explicitly.
In particular, quote `timestamp` is serve time, mood has no as-of, and story lists have per-story dates only.
The host supplies status, source links, and dates after resolving `dataRef`; the model cannot author those props.
Object spreading an upstream response into this object defeats the boundary.
Provider prompts receive the relevant public snapshots, not environment contents or raw headers.
A provider error is summarized by the host; it is not copied verbatim into a chip.

## Layout and navigation

Use a narrow saved-thread rail, a left chat pane around 42% of usable width, and a right canvas pane.
The home input supports ticker navigation and natural research questions without requiring command memorization.
A bare ticker opens the compact view. `open TICKER` is the richer six-read research command.
When a thread has no artifact, show a useful empty state; text turns do not manufacture empty canvases.
Tool chips live in the active assistant turn, with pending/success/error/interrupted states and short summaries.
A Stop control stays reachable during model and data work.
Rows stack on narrow windows before clipping. Give tables horizontal scrolling and charts a bounded minimum height.
See [blocks-and-rendering.md](blocks-and-rendering.md) for tokens and component states.

## History and refresh

Persist threads and artifacts atomically under the app's own user-data directory using generated IDs.
Store source XML only host-side, alongside the validated AST, contract version, artifact ID, source dates,
and the snapshot IDs needed to explain the saved screen. Never store credentials in this record.
Revalidate saved artifacts against their recorded version; display an explicit migration error for unsupported versions.
Do not evaluate code or HTML from saved content.

Use immutable snapshot versions: refresh creates a new snapshot ID for the same operation/input key.
Keep the AST and saved evidence byte-stable. For manual refresh, the host maintains an ephemeral view binding
from the current artifact ID and block ID to the new snapshot ID; do not edit `dataRef` inside the saved AST.
The renderer uses the effective binding and `read_screen` returns those same effective snapshot IDs.
A `refreshSnapshot` IPC reply carries the validated new snapshot and binding update, not a second turn artifact.
Clear ephemeral bindings on history reopen so the saved view starts with its original evidence.
Only an explicit new analysis turn can author a new persistent artifact. The narrative keeps its original date.
Show a small "data refreshed; analysis written at ..." label when those diverge.
Reopening history preserves its original narrative. Regeneration is an explicit new user turn.

## Provider seam

When no provider credential is available, keep deterministic commands and ticker navigation usable
if the SentiSense connection is available. For an open-ended model request, emit a short text setup turn:
"Model connection required for this request. Data commands are still available."
Do not start a provider call, fabricate a model answer, or ask for secrets in chat.
A missing SentiSense key separately blocks data reads; synthetic fixtures require an explicit test mode.
This is the first-build fallback behavior, not a claim that a model-assisted turn has passed verification.

Implement one adapter that accepts messages, registered tool definitions, and an abort signal,
and yields internal progress plus final tool requests/text.
Continue the provider turn only after each tool resolver completes; tool-input completion is not tool success.
Translate that progress into [the public host protocol](runtime-and-stream.md) inside the main process.
Bound the number of tool rounds, HTTP requests, canvas repairs, and elapsed time per turn.
Always clean up listeners and settle pending chips when a turn ends.
Stop discards later results even if abort is unsupported; do not promise provider billing stopped.

## Source links and optional embeds

The core app opens validated source links externally and renders returned story titles as text.
If adding external title lookup later, create a separate narrow fetcher with public-address DNS checks
before every request and redirect, byte/time limits, no ambient credentials, and no private/loopback/metadata destinations.
Do not expose an arbitrary browsing tool to the model.
Social embed HTML needs separate sandboxing and explicit provider allowlists; never inject it into the native canvas tree.
