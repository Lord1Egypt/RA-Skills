# Canvas grammar and validation

Use this contract when a turn needs a durable visual artifact. Read [runtime and stream](runtime-and-stream.md) before connecting it to a provider, and [blocks and rendering](blocks-and-rendering.md) while implementing components.

The model proposes one complete XML canvas. The host parses it into an allowlisted AST, validates it, stores the source XML with the artifact record, and sends only the AST through the host event stream. Never render model XML directly. Never stream a partly parsed canvas.

## Root and layout

The required root attributes are `id`, `title`, `created`, and `schemaVersion="2.0"`. Optional root attributes are `author`, `tags`, `version`, and `template`. `created` is an ISO 8601 date-time. `tags` is a comma-separated list in XML and a string array in the AST.

```xml
<canvas id="turn.a17" title="Research screen" created="2026-01-15T16:00:00Z" schemaVersion="2.0" tags="research,ticker">
  <block id="heading" type="section-header" width="full" title="$DEMO" />
  <row>
    <block id="price" type="metric-card" width="half" label="Price" field="price" dataRef="dashboard.demo.quote" />
    <block id="tone" type="sentiment" width="half" ticker="$DEMO" dataRef="dashboard.demo.sentiment" />
  </row>
</canvas>
```

A canvas contains one to 48 rendered blocks. A top-level block has `width="full"`. A row contains exactly two `half` blocks or exactly three `third` blocks. Rows cannot nest and do not accept attributes. IDs are unique across the canvas root and every block.

The core block types are:

```text
section-header  narrative       callout          table
metric-card     price-chart     sentiment        news-feed
watchlist       market-mood
```

Unknown types fail validation. Adding a renderer requires a new contract version or a backward-compatible schema update shared by the producer, validator, and host.

## Text and escaping

Only `narrative` and `callout` carry text between opening and closing tags. Other blocks are self-closing and read values from attributes. Escape XML text and attributes with the five predefined entities: `&amp;`, `&lt;`, `&gt;`, `&quot;`, and `&apos;`. Valid numeric character references are also accepted.

The parser rejects declarations, DTDs, external entities, processing instructions, CDATA, comments, unknown entities, XML control characters, raw `<` inside attributes, and markup inside text. The canvas language does not accept HTML, scripts, styles, SVG, event handlers, executable actions, or URLs outside HTTP and HTTPS.

JSON held in an attribute must use the opposite quote style around the XML attribute:

```xml
<block id="rows" type="table" width="full"
  columns='["Ticker","Move"]'
  rows='[["$ALFA","+1.00%"]]'
  asOf="2026-01-15T15:45:00Z" synthetic="true" />
```

Inline arrays are bounded and shape-checked. A table row must match the column count. A price point has only `time` and a finite numeric `value`. A news item requires `title` and accepts only `source`, `url`, `publishedAt`, and `summary` in addition. A watchlist item requires `ticker` and accepts only `change`, `value`, and `label` in addition.

## Live snapshots and synthetic inline data

Every data block uses exactly one data mode.

In live mode, `dataRef` names a normalized host snapshot. The block may include selectors such as `field`, `ticker`, or `range`. The renderer resolves the ID from the same snapshot store used by `read_screen`; the model never chooses an object path against an arbitrary response.

The authored canvas cannot supply `status`, `sourceUrl`, `dataAsOf`, or `fetchedAt`. Those values are host-owned snapshot metadata and must be projected into renderer state only after the AST is validated. The canvas schema and parser reject an authored copy of any of those properties.

Structural canvas validation cannot prove that a live block's selectors match the operation behind its `dataRef`. After resolving the snapshot, run the snapshot adapter's `validateLiveBlockBinding(manifest, snapshot, block, { effectiveSnapshotId })` check before rendering. It verifies that the resolved snapshot is the intended binding and that a metric-card `field` is an operation-specific scalar listed in the manifest's `displayFields`. Reject an invalid binding instead of reading an arbitrary response path.

In inline mode, the block contains its bounded display data, `asOf`, and `synthetic="true"`. This mode exists for tests, previews, and explicitly labeled examples. It cannot represent a live answer. The validator rejects a block that mixes a live `dataRef` with any inline fields.

Snapshot entries keep these facts separate:

```text
operation and normalized input identity
status: loading | ok | empty | error | preview
normalized value
source date when the response supplies one
fetch time recorded by the host
validated source URL when one exists
```

Manual refresh creates a new snapshot and updates an ephemeral host view binding for the data block,
without editing the saved AST; see [app shell](app-shell.md). It does not rewrite authored narrative. Keep the narrative's original date visible so fresh widget data is not blended into old analysis.

## Parsed AST

The authoritative executable shape is [contracts/canvas.schema.json](contracts/canvas.schema.json). A parsed canvas has this form:

```json
{
  "schemaVersion": "2.0",
  "id": "turn.a17",
  "title": "Research screen",
  "created": "2026-01-15T16:00:00Z",
  "tags": ["research", "ticker"],
  "blocks": [
    {
      "id": "heading",
      "type": "section-header",
      "width": "full",
      "props": { "title": "$DEMO" }
    },
    {
      "type": "row",
      "blocks": [
        {
          "id": "price",
          "type": "metric-card",
          "width": "half",
          "props": { "label": "Price", "field": "price", "dataRef": "dashboard.demo.quote" }
        },
        {
          "id": "tone",
          "type": "sentiment",
          "width": "half",
          "props": { "ticker": "$DEMO", "dataRef": "dashboard.demo.sentiment" }
        }
      ]
    }
  ]
}
```

JSON Schema covers structure, allowed fields, per-type props, data modes, widths, sizes, and formats. Runtime validation additionally covers XML well-formedness, unique IDs, total nested block count, JSON-in-attribute shapes, safe URLs, forbidden markup, and row width rules. Run both contracts in tests.

## Host integration

Copy or adapt [runtime/canvas-validator.mjs](runtime/canvas-validator.mjs). It has no package dependency and exports:

```js
CANVAS_SCHEMA_VERSION
BLOCK_TYPES
parseCanvasXml(xml, options)
validateCanvasAst(canvas)
```

Both validation functions return one of:

```js
{ ok: true, canvas }
{ ok: false, error: { code, message, path? } }
```

Treat error codes as the stable programmatic interface and messages as repair context. Preserve the last good canvas when validation fails. Give the model one bounded repair attempt inside the same turn budget. A repaired turn still commits at most one successful artifact.

Reserve a host-generated artifact ID before asking the model for XML, and require that ID in the root.
The `render_canvas({xml})` resolver should:

1. Receive a complete XML string.
2. Enforce the byte limit before parsing.
3. Call `parseCanvasXml`.
4. Return the typed validation error to the agent when invalid.
5. On success, verify the root ID equals the reserved artifact ID, then save XML plus AST in host storage.
6. Emit one `artifact` event whose `body` is the validated AST.

If repair fails, end the canvas turn with a concise text fallback. Do not clear the last good artifact and do not emit a half-empty canvas.

## Deterministic replay

The three valid examples are [stock snapshot](fixtures/stock-snapshot.xml), [comparison](fixtures/compare.xml), and [daily brief](fixtures/daily-brief.xml). All observations are visibly synthetic. [Invalid canvases](fixtures/invalid-canvases.json) pairs each hostile or malformed XML string with its expected error code.

From the installed skill directory, change into `references/` and run the fixtures using only emitted files:

```bash
node --input-type=module <<'NODE'
import { readFileSync } from 'node:fs';
import { parseCanvasXml } from './runtime/canvas-validator.mjs';

for (const name of ['stock-snapshot.xml', 'compare.xml', 'daily-brief.xml']) {
  const xml = readFileSync(`./fixtures/${name}`, 'utf8');
  const result = parseCanvasXml(xml);
  if (!result.ok) throw new Error(`${name}: ${result.error.code}`);
}

const invalid = JSON.parse(readFileSync('./fixtures/invalid-canvases.json', 'utf8'));
for (const test of invalid) {
  const result = parseCanvasXml(test.xml);
  if (result.ok || result.error.code !== test.expectedCode) {
    throw new Error(`${test.name}: expected ${test.expectedCode}`);
  }
}
console.log('canvas fixtures: pass');
NODE
```

Fixture success proves the local contract and renderer inputs. It does not prove live API coverage, provider behavior, or the one-afternoon timing target.
