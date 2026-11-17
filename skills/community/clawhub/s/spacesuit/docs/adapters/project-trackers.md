# Project tracker adapters (v1)

Spacesuit supplies optional tracker normalization. Command Center supplies the
provider-independent, read-only project board and still works without Spacesuit.
**Live tracker synchronization is not configured by these commands.** No credentials
are read, stored, accepted as CLI flags, or copied into snapshots. The runnable CLI
imports explicit local provider exports. The transport-injection API is groundwork
for an authorized host connector, not an installed Linear/Jira integration.

## Outcomes rather than task lists

- Linear **projects** become `kind: project` cards.
- Jira **epics** become `kind: epic` cards. Configure native issue-type IDs explicitly;
  project containers, ordinary issues, and localized type names are not guessed.
- The native project ID, status ID, and status label survive normalization. Identity
  is `(sourceId, projectId)`; equal titles across trackers are separate outcomes.
- Native semantic categories map into inbox/planned/doing/done/canceled/unknown.
  `statusMap` overrides use native status IDs. Review is explicit; Jira's `done`
  category is not assumed to mean review or cancellation. Map canceled states by ID.
- Missing health and task aggregates remain unknown/null. We do not derive project
  completion from an incomplete issue page or silently use counts as weighted progress.
- Agent/session/dependency relationships come only from explicit `links` keyed by
  native project ID. No title matching, implicit cross-account joins, or task ownership
  inference. Configs and exports are private per-workspace bindings.
- Memory/knowledge/topic adapters remain independently composable. These adapters
  neither replace OpenClaw retrieval nor impose a memory backend on a flavor.

## Offline preview and apply

Use a new scratch workspace first. Copy `tests/fixtures/projects/config.json`,
`linear.json`, and `jira.json` into it. These are synthetic, intentionally old exports;
the board correctly marks their preserved observation time stale.

```bash
node scripts/projects.js preview --workspace /path/to/workspace --config config.json
node scripts/projects.js apply --workspace /path/to/workspace --config config.json
```

The workspace must be a real absolute directory, with no symlink ancestors. Config
and export paths are relative to it. Preview writes nothing; apply explicitly writes:

```text
state/command-center/project-sources.json
state/command-center/projects/<source-id>.json
```

Example config (no credentials):

```json
{
  "schemaVersion": 1,
  "profile": "",
  "agentId": "main",
  "sources": [
    {
      "id": "linear-example",
      "provider": "linear",
      "label": "Planning",
      "enabled": true,
      "input": "linear.json"
    },
    {
      "id": "jira-example",
      "provider": "jira",
      "label": "Delivery",
      "enabled": true,
      "input": "jira.json",
      "jiraEpicTypeIds": ["10000"],
      "jiraBaseUrl": "https://example.atlassian.net",
      "statusMap": { "10002": "review" }
    }
  ]
}
```

Each export is `{ "observedAt": "<ISO timestamp>", "pages": [<raw response>, ...] }`.
Linear pages contain `data.projects.nodes` and `pageInfo.hasNextPage/endCursor`;
Jira enhanced-search pages contain `issues`, `isLast`, and `nextPageToken` when more
pages exist. Preserve response order. Export timestamps are observation times, not
import times: importing an old file does not make the data fresh. Jira rich-text ADF
descriptions are omitted in v1 rather than rendered as HTML or guessed into summaries.

Set `enabled: false` and apply to disable a source. Disabled sources are not read and
their snapshot files are retained. Keep the prior config/export files to reverse
changes; this importer does not create automatic backups or delete snapshots.
One selected profile/agent per workspace is supported; a different identity cannot
overwrite existing selection or snapshots. Use distinct workspaces for isolation.

Missing exports produce `unavailable`; malformed/unsafe exports produce `error` for
that source without hiding healthy sources. On refresh failure, prior data and its
original observation time are retained with error/unavailable status—not fresh empty
success. Partial pagination is explicitly `partial`; unused export pages beyond the
200-project cap do not discard the collected projects. No provider error text is exposed.
Corrupt, unsafe, or foreign previous snapshots are never reused or overwritten: only
that source reports error, healthy sources continue, and apply reports `partial` plus
`skippedSources`. The requested source remains enabled so the dashboard can show its
error rather than silently hiding it. Inspect and repair the preserved file before
retrying. A mismatched identity in the shared selection remains a global refusal.

## Injected transport API

```js
const { collect } = require("./lib/projects/adapters");
const snapshot = await collect({
  source,
  profile: "",
  agentId: "main",
  request: authorizedHostRequest,
  maxPages: 10,
  maxProjects: 200,
  timeoutMs: 10000,
});
```

The injected request receives a fixed provider query descriptor plus an AbortSignal:

- Linear: `provider`, `method: POST`, `path: /graphql`, static read-only `query`,
  `variables: {first: 50, after}`.
- Jira: `provider`, `method: GET`, `path: /rest/api/3/search/jql`, `params` containing
  explicit fields, `maxResults: 50`, JQL, and optional `nextPageToken`.

It returns parsed provider JSON, not a Fetch Response. The host binds the intended
account/base URL, authorizes access, enforces response-body byte limits before JSON
parsing, supplies protected credentials and obeys cancellation. This library does not
construct credential headers, invoke arbitrary endpoints, or load executable adapters
from config. Jira JQL may be explicitly supplied in the private binding.

The collector enforces an independent total deadline even if the host ignores abort,
caps pages/projects, rejects looping/missing cursors, and marks truncated results
partial. It does not retry rate limits, silently continue GraphQL errors, or schedule
polling. The host must coalesce concurrent calls and apply its provider retry policy.

Limits: 8 sources, 200 projects/source, 1 MiB per local export or output snapshot,
64 KiB config, 10 imported pages. Reads reject symlinks and non-regular files (including
FIFOs); writes use private temporary files and rename. Apply has a workspace lock and
selection-change check. Atomicity is **per file**, not an all-source transaction. A
crashed apply can leave a mix of observation times; the UI must retain source freshness.
Do not concurrently replace workspace directories while importing. A stale import
lock requires operator inspection before removal.

## Provider references and limitations

Shapes and pagination follow [Linear GraphQL](https://linear.app/developers/graphql),
[Linear pagination](https://linear.app/developers/pagination), and
[Jira enhanced issue search](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-search/).
No real provider calls were made by the tests: a configured source pilot is still
required to verify account-specific permissions, schema availability, and issue types.
Asana, GitHub Issues, mutations, drag/drop transitions, live sync, and bidirectional
conflict resolution are future capabilities—not advertised as working in v1.
