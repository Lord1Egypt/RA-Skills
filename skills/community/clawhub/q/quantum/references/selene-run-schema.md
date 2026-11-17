# `selene_run` v1 schema + `<SeleneRunView />`

A single Zod schema renders every Selene experiment in this repo. New demos should target it instead of bespoke React pages.

## Schema (v1)

`src/lib/selene-run-schema.ts` defines:

```ts
SeleneRun = {
  schemaVersion: 1,
  experiment: string,
  title: string,
  description: string,
  kernel: { snippet, qubits, shotsPerRow },
  verdict: { text, good },
  metrics: { name, value, unit?, good? }[],
  series: {
    id, kind: "histogram" | "bar" | "line",
    title, xLabel?, yLabel?,
    yKeys: string[],
    points: { label, values: Record<string, number> }[],
  }[],
  notes?: string,
  extras?: Record<string, unknown>,
}
```

Render with `<SeleneRunView run={...} />` (`src/components/selene/SeleneRun.tsx`). It reads `metrics` and `series` only — `extras` exists for non-rendering metadata.

## The "no `extras` escape hatch" rule

**If a new demo needs `extras` to render correctly, the schema is wrong — extend the schema instead.** This is the refutation criterion for the `json-ir-schema` frontier card; bypassing it via `extras` voids the v1 conformance claim.

The current 8/8 demos round-trip without `extras`. Keep it that way.

## Authoring a new demo

1. Run the Python driver, dump results to `src/data/demos/<name>.json` in whatever shape is natural.
2. Write a converter in `src/lib/selene-run-convert.ts`:
   ```ts
   export function convert<Name>ToSeleneRun(): SeleneRun {
     const raw = rawJson;
     return { schemaVersion: 1, experiment: "...", title: ..., metrics: [...], series: [...], ... };
   }
   ```
3. Add a route that does `SeleneRunSchema.parse(convert<Name>ToSeleneRun())` and renders `<SeleneRunView />`. Parsing at render time is the schema test.
4. Add the new demo to the conformance dashboard (`src/routes/nadarasa.schema-coverage.tsx`) so the count stays at N/N.

## When to extend the schema vs. add `extras`

| Need | Action |
| --- | --- |
| Another chart kind (e.g. heatmap, scatter) | extend `SeriesSchema.kind` enum |
| Per-series annotations (target curve overlay) | add an optional `overlay` field on `SeriesSchema` |
| Truly non-rendering metadata (timing, host info) | `extras` is fine |
| Anything the user is meant to see | extend the schema |

When in doubt: if `<SeleneRunView />` reads it, it belongs in `metrics` or `series`, not `extras`.
