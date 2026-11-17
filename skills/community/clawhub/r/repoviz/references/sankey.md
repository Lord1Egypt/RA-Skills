# Sankey Diagrams (`/draw?type=sankey`)

## When to Use

Weighted flows: data-pipeline volumes, dependency/bundle-size contributions, request routing distributions, traffic sources, cost attribution, funnel/conversion analysis. Use it when the user asks to *"trace data flow"*, *"show where the bytes/requests/money come from and go"*, or *"visualize dependencies by weight"*.

If edges have no meaningful weight, use `archmap` (topology) or `flowchart` (ordering) instead — Sankey without weights adds no signal.

## URL Schema & Encoding Rule

```
https://x-cmd.com/draw?type=sankey&labels=<n1,n2,...>&links=<A>B:<w>;<A>C:<w>;...[&title=][&unit=][&t=pipeline|fund][&scheme=][&w=][&h=]
```

- `labels=` — comma-separated node names. **Links reference nodes by these exact names**, so a multi-word node is declared `Hot%20Store` in `labels=` and written `Hot%20Store>Dashboard:32` in `links=` — encode it identically in both places.
- `links=` — semicolon-separated `From>To:weight` triplets. `>` and `:` stay literal; the `>` token separates source and target.
- `unit=` — caption suffix shown on values (e.g. `GB%2Fday`, `req%2Fs`; a literal `/` is safe, `%2F` is canonical).
- `t=` styles: `pipeline` (engineering/flow feel), `fund` (allocation feel); default `base`.
- Numeric-annotation param `num=` is ignored by sankey.

**JSON alternative (`?d=`)** for programmatic generation — URL-encode the whole JSON. Structure `{"labels":[...],"links":[{"from":"A","to":"B","value":30}]}` becomes:

```
https://x-cmd.com/draw?type=sankey&d=%7B%22labels%22%3A%5B%22A%22%2C%22B%22%5D%2C%22links%22%3A%5B%7B%22from%22%3A%22A%22%2C%22to%22%3A%22B%22%2C%22value%22%3A30%7D%5D%7D
```

## Minimal Working Example (3 nodes)

Raw definition:

```
labels=A,B,C
links=A>B:5;B>C:3
```

Final URL:

```
https://x-cmd.com/draw?type=sankey&labels=A,B,C&links=A>B:5;B>C:3&title=Minimal%20flow
```

## Production Repo Example

Multi-stage data pipeline: events collected into a stream, fanned out to hot/cold storage, then consumed by a dashboard and an ML pipeline (`t=pipeline`, unit caption, 7 nodes / 8 links):

```
https://x-cmd.com/draw?type=sankey&t=pipeline&labels=Events,Collector,Stream,Hot%20Store,Cold%20Store,Dashboard,ML%20Pipeline&links=Events>Collector:100;Collector>Stream:96;Stream>Hot%20Store:40;Stream>Cold%20Store:56;Hot%20Store>Dashboard:32;Hot%20Store>ML%20Pipeline:8;Cold%20Store>ML%20Pipeline:30;Cold%20Store>Dashboard:12&title=Data%20pipeline%20flow&unit=GB%2Fday
```

A second production shape — dependency weights, e.g. bundle-size contribution of top modules into entry chunks — uses the same grammar; derive the weights from file sizes (`du`/`stat`) or import counts during the scan.

## Anti-Patterns & Limits

- **Hard limits: ≤24 nodes, ≤60 links.** Fan out aggressively: keep the top ~8–12 flows and collapse the rest into an `Other` node.
- **Must be a DAG.** Cycles are rejected: `sankey links must form a DAG (no cycles); check links= for a loop`. Feedback loops belong in a `lifecycle` diagram.
- Weights must be ≥0 (negative = 400); decimals are fine.
- In/out totals per node need not match (the renderer normalizes band widths), but mismatches usually mean a missed flow — sanity-check conservation before shipping.
- `links=` referencing a name absent from `labels=` fails; typo-proof by generating both from one node list.
- More than ~10 nodes makes bands unreadable at README width (~800px) — prefer an overview Sankey plus per-pipeline detail charts.
