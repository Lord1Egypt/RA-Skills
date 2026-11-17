# Workday `*.htmld` endpoints for fpx

Ready-to-run paths for `fpx get '<url>' -p workday`. All shapes are
live-verified in the repo (`src/client.ts`, `src/tools/*.ts`,
`docs/WORKDAY-API.md`) against a production tenant on `wd5.myworkday.com`
(cards 2026-06, the manager surfaces 2026-08). Replace
`wd5.myworkday.com`/`acme` with your own `$HOST`/`$TENANT`.

Every response is a `root` envelope: page chrome (`title`, `taskId`,
`tenant`, `currentUser`, `accountTasks`, `header` export links,
**`sessionSecureToken` — SECRET, never project this**) plus a `body`.
**`body` is NOT always `cardContentSections`** — Workday serves seven page
families (data card, `grid`, form/`fieldSet`, `compositeView` worker profile,
`hierarchyNavigator` org chart, `landingPage` hub, and report prompt forms),
so a page that looks empty under a `cardContentSections` filter usually is
not. **Always pipe through one of the filters below — never bare `jq '.'`.**

---

## 1. List your apps (the discovery entry point)

```
GET https://$HOST/$TENANT/quickaccess/fetch.htmld?shouldFetchUpcApps=true
```

```sh
fpx get "https://$HOST/$TENANT/quickaccess/fetch.htmld?shouldFetchUpcApps=true" -p workday \
  | jq '[.. | objects | select(.widget=="configuredAppsItem") | {label, taskId: .taskIid}] | unique_by(.label)'
```

A `widget/children` tree; leaf `configuredAppsItem` nodes carry `label` +
`taskIid`. Some apps share a generic launcher id (e.g. `2997$2151`) and open
to a near-empty page — for those, open the app in your browser and use its
page URL with endpoint 3 instead.

## 2. Task by id (constructable — no page-context token needed)

```
GET https://$HOST/$TENANT/task/<taskId>.htmld
```

`<taskId>` looks like `2998$43525` (from endpoint 1, or a prior response's
references). Returns clean JSON for any task id, but **container/launcher
tasks return a near-empty shell** (no `cardContentSections`) — rich data
needs endpoints 3+4 below.

```sh
fpx get "https://$HOST/$TENANT/task/2998\$43525.htmld" -p workday | jq '{
  title: (if (.title|type)=="object" then .title.text else .title end),
  fields: [.. | objects | select(.widget=="text") | {label, value}],
  refs:   [.. | objects | select(.widget=="moniker") | {text, instanceId}],
  relatedTasks: (.accountTasks // [])
}'
```

(Escape the literal `$` in a task id before the shell expands it, as shown.)

## 3. Task hub → data card crawl (rich data)

Container tasks (Benefits and Pay, etc.) delegate to child cards through two
opaque, page-context-bound tokens you can only get by loading the parent:

```
GET https://$HOST/$TENANT/inst/<pageCtx>/cacheable-task/<taskId>.htmld   # the hub
GET https://$HOST/$TENANT/card/all/<cardId>/<pageCtx>.htmld              # a child card (the real content)
```

`<pageCtx>` is NOT constructable — read it off the hub response's own
references/uris (or copy the child card's URL from your open browser tab).
The `cacheable-task` token is comparatively stable across loads; the
`card/all` child token rotates. Project the hub response the same way as
endpoint 2; the child card usually contains list-card rows (see below).

## 4. List-card rows (e.g. a benefits cost table)

A list/table section's `contentSectionItems[]` are ROW objects keyed by
clean column names (`label`, `value`, `secondaryValue`, `task`,
`onInstance`, …) rather than a flat `text` widget — key on the **column
name**, not `propertyName` (Workday's real propertyNames are namespaced,
`wd:Label`/`nyw:Value`, and are template noise here). Approximate the
row read with:

```sh
fpx get "https://$HOST/$TENANT/card/all/<cardId>/<pageCtx>.htmld" -p workday | jq '
  .body.cardContentSections[]? | {
    section: .contentSectionName,
    rows: [.contentSectionItems[]? | {
      label: (.label.value // .label.label // empty),
      value: ([.value.value, .secondaryValue.value] | map(select(. != null)) | join(" ")),
    }]
  }'
```

Drill-in references for a row come from its navigational columns only
(`task`, `onInstance`, `relatedTaskInstance`, `quicklinkItem` — `uxIcon`/
`image` monikerLists are decoration):

```sh
fpx get "https://$HOST/$TENANT/card/all/<cardId>/<pageCtx>.htmld" -p workday | jq '
  [.body.cardContentSections[]?.contentSectionItems[]?
   | (.task, .onInstance, .relatedTaskInstance, .quicklinkItem)?
   | select(. != null)
   | .. | objects | select(.widget=="moniker") | {text, instanceId}]'
```

## 5. Worker profile → the drill-in catalog (the manager surface)

```
GET https://$HOST/$TENANT/inst/<workerCtx>/<workerIid>.htmld
```

Returns "View Associate": a `compositeView` listing ~40 named, fetchable tasks
across 9 sections. `<workerCtx>` differs per tenant — read it off an org-chart
node's concrete profile uri (endpoint 6) rather than guessing.

```sh
fpx get "https://$HOST/$TENANT/inst/1\$715/247\$42.htmld" -p workday | jq '
  [.. | objects | select(.widget=="compositeViewSection")
   | {section: .label,
      tasks: [.taskNodes | .. | objects | select(.widget=="compositeViewTask")
              | {label, uri: (.uri + ".htmld")}]}]'
```

Then fetch any of those uris (**`.htmld` must be appended — the bare form 404s**):

```
GET https://$HOST/$TENANT/inst/<ctx>/rel-task/<taskId>.htmld
```

## 6. Org chart (the reporting chain)

```
GET https://$HOST/$TENANT/task/<orgChartTaskId>.htmld
```

Get `<orgChartTaskId>` from endpoint 1 (the app labelled "Org Chart").

```sh
fpx get "https://$HOST/$TENANT/task/2998\$2673.htmld" -p workday | jq '
  [.. | objects | select(.widget=="hierarchyNavigator")
   | {workerIid,
      chain: [.ancestors[]? | {
        name:  (.navigatorInstance.instances[0].text // null),
        profileUri: (.navigatorInstance.selfUriTemplate + ".htmld"),
        title: (.navigatorItems[0].detailOne // null),
        location: (.navigatorItems[0].detailTwo // null),
        reports: (.navigatorItems[0].detailThree // null)}]}]'
```

`selfUriTemplate` is already CONCRETE here (one uri per person) — this is where
the `<workerCtx>` for endpoint 5 comes from. Note the chain runs UPWARD only;
expanding DOWN to direct reports is a POST-only navigation and 404s on GET.

## 7. Grids (real tables)

Many pages return a `grid` rather than card sections. Cells are keyed by an
opaque `columnId`, so join to `columns[]`:

```sh
fpx get "https://$HOST/$TENANT/inst/<ctx>/rel-task/<taskId>.htmld" -p workday | jq '
  [.. | objects | select(.widget=="grid") | . as $g
   | ($g.columns | map({key: .columnId, value: .label}) | from_entries) as $cols
   | {label: $g.label, rows: $g.rowCount, total: $g.deepRowCount,
      chunkingUrl: $g.chunkingUrl,
      data: [$g.rows[]? | .cellsMap | with_entries(
               .key |= ($cols[.] // .)
             ) | map_values(.value // .instances[0].text // null)]}]'
```

**`deepRowCount > rowCount` means the grid is CHUNKED** — you have only the
first page, and `chunkingUrl` serves the rest. Don't report it as complete.

## 8. Healthcheck probe (tiny authenticated endpoint)

```
GET https://$HOST/$TENANT/get-global-prefs.htmld?feature=doNotShowMobileAd
```

```sh
fpx get "https://$HOST/$TENANT/get-global-prefs.htmld?feature=doNotShowMobileAd" -p workday | jq -r '
  if (type=="object") then "ok (\(. | length) top-level keys)" else "unexpected body" end'
```

Cheap way to confirm the bridge + tab + SSO session are all alive before a
bigger crawl — a non-JSON/HTML result here means the session expired (see
SKILL.md's session-expiry tell).

---

## SPA URL → data endpoint

If you copy a URL from your open Workday tab and it contains `/d/`
(`https://$HOST/$TENANT/d/inst/....htmld`), drop the `/d/` segment before
fetching — that path is the HTML app shell, not data:

```sh
url="https://wd5.myworkday.com/acme/d/inst/13102!ABC/cacheable-task/2998\$43525.htmld"
data_url="${url/\/d\///}"   # → .../acme/inst/13102!ABC/cacheable-task/2998$43525.htmld
fpx get "$data_url" -p workday | jq '...'
```

## Gotchas that cost real debugging time

- **Most uris arrive WITHOUT `.htmld` and 404 until you append it** — `inst`,
  `rel-task` and `task` paths alike.
- **`moniker.target` is the best navigation edge**: a URL-ENCODED ABSOLUTE url.
  Decode it and drop the `/d/` segment, then it fetches.
  `jq -r '.target | @uri "\(.)"'` won't do it — use
  `python3 -c 'import sys,urllib.parse; print(urllib.parse.unquote(sys.stdin.read()))'`.
- **Uri templates come in three dialects**: `{id}`, `[IID]`, and
  already-concrete. Substituting only `{id}` yields unfetchable uris.
- **A page with no `cardContentSections` is not empty** — it is probably a grid,
  a compositeView, a hierarchyNavigator, a landingPage, or a report PROMPT form
  (`monikerListInput` / `textInput` widgets, which need a POST of parameters).

## Verified NOT GET-able (don't burn time here)

- `/{tenant}/navigable/<iid>` and `/navigable/bundler` — org-chart expansion to
  direct reports. POST-only.
- `/{tenant}/worklet/<workletIid>`, `/{tenant}/print/navigable/...` — 404.
- `/{tenant}/search.htmld` — returns an empty `federatedSearchResults` shell;
  `q`, `st`, `searchText`, `query`, `text`, `keyword` and `s` were all tried and
  none is the query parameter.
- **GraphQL surface** (`/wday/pex/graphql/graphql?operation=...`, POST) — serves
  the inbox/"My Tasks" and search. Reachable, but no operation shape is captured
  in the repo, so it's left out here rather than guessed.
- **Writes** — none exist in workday-mcp (read-only); Workday writes are
  multi-step business processes, not single POSTs.
