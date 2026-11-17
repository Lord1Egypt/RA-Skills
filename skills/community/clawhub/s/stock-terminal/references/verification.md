# Verification and the fresh-builder exercise

Use deterministic checks first. They prove the kit's contracts, not a provider integration or a four-hour delivery claim.
Live API and provider checks are separate, use authorized credentials, and must be recorded as run or unrun.
Never present fixture-only success as live market validation.

## Validate the installed tree

All links in the installed `SKILL.md` and references must resolve locally.
Use [inventory.json](inventory.json) as the explicit reference receipt: each entry names a file and its SHA-256.
It lists reference payload files only, excluding itself and the separately required `SKILL.md`.
A directory listing is not a file. Do not infer completeness from an unexplained total.
Retain the directory structure when copying modules or sharing the kit with another builder.
If an installer fetches only `SKILL.md`, obtain the complete skill directory before attempting the build.
Availability of relative URLs alone does not prove an installer downloaded those resources.

From the installed skill directory, verify the receipt without fetching another repository:

```bash
node --input-type=module <<'JS'
import {readFileSync, readdirSync} from 'node:fs';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
const inventory = JSON.parse(readFileSync('references/inventory.json', 'utf8'));
assert.equal(inventory.schemaVersion, '2.0');
const walk = dir => readdirSync(dir, {withFileTypes:true}).flatMap(entry =>
  entry.isDirectory() ? walk(`${dir}/${entry.name}`) : [`${dir}/${entry.name}`]);
const actual = walk('references').filter(path => path !== 'references/inventory.json').sort();
assert.deepEqual(inventory.files.map(file => file.path).sort(), actual);
for (const file of inventory.files) {
  assert.equal(createHash('sha256').update(readFileSync(file.path)).digest('hex'), file.sha256, file.path);
}
assert.ok(readFileSync('SKILL.md').length > 0);
console.log(`PASS 1 SKILL.md entry point plus ${actual.length + 1} reference files, including inventory.json`);
JS
```

From the installed skill directory, run this dependency-free XML smoke check:

```bash
node --input-type=module <<'JS'
import {readFileSync} from 'node:fs';
import assert from 'node:assert/strict';
import {parseCanvasXml, validateCanvasAst} from './references/runtime/canvas-validator.mjs';
for (const name of ['stock-snapshot', 'compare', 'daily-brief']) {
  const result = parseCanvasXml(readFileSync(`references/fixtures/${name}.xml`, 'utf8'));
  assert.equal(result.ok, true, JSON.stringify(result.error));
  assert.equal(validateCanvasAst(result.canvas).ok, true);
  console.log(`PASS ${name}`);
}
JS
```

Run the invalid-input replay described in [canvas grammar](canvas-grammar.md)
and the turn replay described in [runtime and stream](runtime-and-stream.md).
Validate the JSON Schemas themselves with a Draft 2020-12 implementation when available.
The events schema references its sibling canvas schema; resolve that reference locally, never through a guessed network URL.
Schema validation supplements the semantic runtime checks for XML, duplicate IDs, and turn state.

## Contract checkpoints

| Case | Observable pass condition |
|---|---|
| Three valid XML fixtures | Parse to a valid AST and render without ignored blocks |
| Ten core block types | Every type has an allowlisted native renderer and required-prop handling |
| Unknown block, missing prop, duplicate ID, nested row | Typed validation failure; no partial artifact commit |
| DTD, external entity, script, unsafe link | Rejected; no network lookup or executable markup |
| Version mismatch | Explicit incompatible-version failure, not a silent fallback parser |
| Repair then success | Failed attempt leaves last good canvas intact; one final artifact commits |
| Two successful artifacts in one turn | Second artifact rejected; first remains visible |
| Text request | Only text in chat; no canvas artifact |
| Canvas request | Chips/status while buffering; one artifact, no duplicated narrative |
| Tool input deltas | Partial JSON stays host-local; no raw arguments in chips |
| Tool completion | Success is emitted only after actual resolver completion |
| Duplicate or stale active-turn sequence | Rejected with no state mutation; after terminal end, all events are ignored |
| Stop then late result or artifact | Turn remains stopped and prior canvas is unchanged |
| Provider cannot abort | UI stops and discards late output; no claim that provider billing stopped |
| Exhausted invalid-canvas repair | Concise text fallback, no malformed canvas and no duplicate prose |

## Data and command checkpoints

Count actual HTTP sends with a local recorder, including widget requests and retries.
Use the operation/input identities in [commands.json](contracts/commands.json), not a count of model tool invocations.

- Compact ticker: four cold requests, with profile adding one only if requested.
- Full `open`: six cold requests; `compare`: twelve for two distinct uncached tickers.
- Daily brief: five cold requests; indices use one batch-price request.
- Smart-money screen: three baseline reads; each deliberately widened empty bucket adds one.
- Holders: quarters before holders; a cached settled-quarter list removes one request.
- Warm identical requests: derive default windows with the shipped helper, then repeat at a different millisecond
  within the same bucket and TTL. Expect zero sends; cross a boundary, expire an entry, and force refresh separately.
  Explicit user windows retain their exact boundaries and therefore their own request identity.
- Shared widget/tool reads: one in-flight send, with both consumers receiving the same snapshot identity.
- Name resolution: one additional search per unresolved company name; no fan-out after an ambiguous or empty match.
- News detail: one extra request only for the selected story, not every row in the list.
- Custom screen: catalog discovery plus execution when cold; read-only POST body retains the user's filters.
  Assert plan is an object, limit a number, and tickers an array or null after exact-token substitution.
- Live table: use the shipped snapshot adapters for insider, analyst, holders, and screener fixtures.
  Reject unsupported field keys and forged authored snapshot metadata; do not evaluate a model object path.
- As-of: quote serve time is not trade time, mood has no as-of, and story dates belong to individual rows.

Inject failures into the adapter rather than altering production data:

| Injected condition | Observable pass condition |
|---|---|
| No API key | Setup state before HTTP fan-out; no synthetic market fallback |
| No provider connection | Deterministic data commands still work with an API key; model requests get a text setup state and make no provider call |
| Cross-thread refresh ID | Main handler rejects before any HTTP request; only current-view snapshot IDs can refresh |
| 401 | Authentication failure and bounded stop, not repeated data calls |
| 429 with Retry-After | Delay within remaining budget or an explicit limit state |
| Uncovered ticker | Unsupported section labeled; no fabricated zero score |
| Empty data | Empty state distinct from transport error |
| Preview response | Visible slice and limitation; denominator not inferred from returned length |
| Null or omitted field | Unavailable label, never a coerced zero |
| Old generated insight | Source age visible alongside newer quote fetch time |
| Widget refresh | New snapshot and fetch time; authored narrative keeps its original evidence date |
| Saved thread reopen | Original dated artifact; no hidden regeneration |
| Wrong ticker/name | Resolution fails clearly; empty downstream rows are not misreported as no coverage |

## Public data boundary and synthetic canary

Generate an unmistakable noncredential canary in the test harness at runtime; do not use a real API or provider key.
Insert it into a fake host authorization header and a fake provider configuration, then exercise the transport.
Assert the mocked upstream receives it only in the intended authorization location.
Capture renderer-bound IPC, host events, diagnostic logs, XML, saved artifacts, and built renderer assets.
Export is deliberately deferred. If the app implements export, also capture and scan every exported format;
otherwise record "export not implemented, optional surface not applicable" without inventing an export feature.
Search those captures for the canary and require zero matches.
Also inject a canary into a rejected raw-arguments field to verify the reducer reports a typed error without echoing payloads.

This is a boundary test, not a general secret detector. The reducer cannot know every secret embedded in arbitrary valid text.
Host-authored summaries and explicit public projections are required; a redaction regex alone is insufficient.
Do not write actual environment values into logs merely to prove the scanner works.
A repo contract test of unknown fields does not prove a future app keeps credentials out of its renderer.
That final claim requires the built application's canary exercise.

## Fresh-builder exercise

Give a clean agent only one complete emitted `stock-terminal/` directory containing `SKILL.md` and `references/`.
Give it an empty project directory, this task, and any explicitly authorized credentials through the host environment.
Do not supply source code from another terminal or unstated architecture notes.
Start a wall-clock timer and record dependencies, environment, interruptions, and elapsed time.

Ask it to produce:

1. A runnable Electron/React app, a lockfile, and documented development and production launch commands.
2. Home ticker navigation, saved threads, left chat/right canvas, one provider adapter, ten native block renderers.
3. Every manifest recipe marked `exposure: "command"`, the compact navigation/internal resolution distinction,
   shared snapshots, and the three local tools `resolve_security`, `read_screen`, and `render_canvas`.
4. The versioned six-event protocol, bounded repair, tool chips, Stop/late-result handling, and manual refresh.
5. Deterministic test output, source-date/preview/error evidence, and canary results.
6. Screenshots of ticker, comparison, text-only, loading, preview, and error states at useful desktop and narrow widths.
7. A short evidence record with elapsed time, deviations, unsupported optional features, and unrun live checks.

Pass the build exercise only if a fresh local install builds and launches without hidden files,
the deterministic checks pass, the screenshots show readable complete views, and the canary stays host-side.
A live-data pass additionally requires dated returned values with the user's authorized API key.
A provider pass requires one real tool-assisted turn, one explanation of the visible screen, and a stopped turn.
A timing pass additionally requires the measured work to fit the stated four-hour target.
Report those four outcomes separately. A useful runnable app can pass the build while timing or live access remains unverified.

## Visual review

Inspect the screenshots rather than accepting a successful render command as visual evidence.
Text should be legible, numeric columns aligned, and source dates visible without dominating the screen.
Rows stack before clipping, long company/story labels wrap, and tables scroll rather than overlap.
Loading and error states retain their layout, so completing one widget does not move the whole page unexpectedly.
Use neutral dark surfaces and restrained accent colors; reject neon glow, rainbow data, decorative motion,
oversized empty hero cards, or gradients behind values.

## Before sharing an app or kit

Scan actual shipped bodies, references, contracts, fixtures, modules, manifests, and source maps.
Require no private repository paths, personal identity, internal project names, tracking IDs, or credential literals.
Synthetic fixtures must remain clearly labeled test data and must never act as runtime market-data fallbacks.
Local verification is not permission to publish, upload, deploy, or distribute the app or skill.
