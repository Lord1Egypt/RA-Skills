# Troubleshooting by layer

Do not change prompts, Agent graphs, or query code until the failure layer is established.

## Registry cache permissions

CLI `UNKNOWN_ERROR` alone does not prove authentication or network failure. If diagnostics establish EPERM/EACCES when writing the CLI registry cache, use its supported `SMARTBI_CACHE_DIR` override to a permitted temporary/work directory for that execution; preserve the profile and TLS verification. This is CLI-managed API metadata, not a Skill model/result cache. Do not persist machine-specific paths in the Skill or delete another process's lock. Diagnose with the CLI runtime: a PowerShell TLS error does not establish that Node fails for the same reason.

## Direct-query latency

For direct MQL/SQL, compare total CLI wall time with the response `durationMs` before blaming the model. In the verified CLI, `durationMs` covers the final business HTTP request, response reading and parsing; it excludes process startup, registry discovery/refresh, and other command overhead. Registry requests can themselves use the network, so the difference is not purely CPU time.

If wall time is high but business HTTP time is low, inspect the CLI/registry layer with bounded diagnostics. A later fast call alone does not identify the earlier cause. Do not automatically add `--refresh`, delete cache/lock files, change global cache settings or repeatedly re-query to hide intermittent latency. Reuse confirmed contracts and metadata within the task; refresh when evidence shows they changed or are invalid. Native query execution, network latency and server processing require server tracing to separate.

A calling tool's wait timeout is not itself proof that the CLI request failed or succeeded. If the tool yielded a live process/session, resume or poll that same execution within a bounded wait instead of starting a duplicate query. If output was redirected to a file, check whether the original process has completed, then parse the complete CLI envelope and business status; file existence or partial bytes alone are not success. Only retry after the original outcome is known or it is safely established that no duplicate work will be issued. For an expected long query, choose a suitable CLI/tool timeout from the current task and observed behavior; do not force background execution, fixed multi-minute waits or a universal latency baseline. `durationMs` is final business HTTP time in the verified CLI, not total command wall time.

The sections below about conversations, rounds and Agent graphs apply only when that workflow was actually invoked; direct queries do not require creating a Baize session for diagnosis.

## Control-plane or authentication failure

Evidence:

- `createConversation` fails;
- `queryRpc` reports authentication failure;
- both rounds and chat logs are empty.

Check the selected profile, base URL, token/session validity, and permissions. This happened before an Agent round or sandbox was created; do not blame MQL, Python, or the workflow.

## Stream transport failure

Evidence:

- the SSE connection ends or times out;
- the conversation has a `RUNNING` round or later log activity.

Use `queryRpcResume` with the same `convId`. Do not create a duplicate conversation or repeat a potentially non-idempotent task.

## Agent graph failure

Evidence:

- the round exists;
- plan artifacts show a node failed, never started, or a finish node waits forever;
- a tool node returns `TOOL_EXECUTE_ERROR`.

Inspect the latest plan artifact, node/port/link IDs, mutually exclusive branches, Provider/Tool bindings, and tool HTTP status. A shared finish node can deadlock if it requires inputs from both mutually exclusive branches; use separate finish nodes or optional inputs supported by the runtime.

## Tool/OpenAPI failure

Evidence:

- Agent reaches the tool node;
- response is HTTP 4xx/5xx or the request body is empty/malformed.

Check Provider read-back, current Tool IDs, request parameter `id`/`name`, content type, actual serialized booleans, and the remote service log. Provider save success does not prove invocation compatibility.

## Sandbox or data-query failure

Evidence:

- rounds/logs exist;
- logs show `smartbi_cli`, SQL/MQL, Python, or Parquet operations failing.

Only now inspect the actual sandbox command, model/table/field names, filters, generated files, and row counts. Local `smartbi` controls conversations; `smartbi_cli` runs inside the Baize sandbox and is a different executable.

## Result or presentation failure

HTTP 200, round `NORMAL`, or a generated file does not prove correctness. Check result rows, business grain, totals, expected artifacts, and any visual/layout QA required by the task.

## Known query and stream symptoms

| Symptom | Likely layer | Response |
|---|---|---|
| SQL returns `DAO_ID_IS_NULL` for multiple valid query shapes | Sandbox/data-query | Check that `FROM` is a model logical table/view alias from current metadata, not a physical table name. |
| SQL cannot find `年`/`年季`/`年月` | Sandbox/data-query | Derive the semantic time level from a verified date column with DuckDB functions such as `year()`. |
| Stream ends at the event cap while round is `RUNNING` and answer is empty | Stream transport | Resume the same `convId` with a larger event cap and poll rounds; do not create a duplicate conversation. |
| `round.answer` appears to be opaque JSON | Result/presentation | Parse its event array, merge appended text artifacts, exclude reasoning/tool logs, and handle file parts separately. |

## Minimal diagnostic bundle

Collect without credentials:

- CLI version and named profile (not its contents);
- Agent ID and read-back SHA-256;
- conversation ID and round/query ID;
- round status, duration, and `errorType`;
- node plan names/states/durations;
- filtered logs around the failing query ID;
- Provider/Tool IDs and remote HTTP status;
- artifact filenames, sizes, and hashes where relevant.
