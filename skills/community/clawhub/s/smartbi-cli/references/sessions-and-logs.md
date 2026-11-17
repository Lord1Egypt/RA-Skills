# Conversations, execution, and logs

Use this workflow when selected by `query-routing.md`: explicit Baize requests, existing-report questions using the built-in report Skill, or default complex insight tasks. Respect an explicit direct-query/local-analysis choice. Ordinary model retrieval and file conversion do not require conversations.

Resolve `<PYTHON>` to an available Python 3 interpreter and `<SKILL_DIR>` to this Skill's absolute directory. The wrapped commands below use POSIX `\` only for readability; on PowerShell pass the same arguments on one line or use PowerShell's continuation syntax. Do not assume the current working directory is the Skill directory.

## Existing-report questions

This is an optional server capability for an external agent, not an assumed AIChat runtime. Resolve the report through target-environment APIs and construct context from verified resource metadata and user/task parameters. Do not assume injected credentials, a preselected report list, browser filters or server sandbox files are available. An internal Skill package alone does not establish an externally callable contract.

For existing-report questions, first follow `report-query.md`. Use this conversation branch only when a deployed report-query Skill and externally callable conversation contract are verified; a direct report query/export does not require a conversation. Skill names differ by deployment: one verified environment exposes “数据模型或报表取数”, while other internal instructions call the report branch “报表数据查询”. Discover the actual accessible Skill identifier and compatible Agent in the target deployment; neither label alone proves a callable report workflow. Do not substitute model MQL merely because the question is simple. Preserve the report resource's actual type, parameters and relevant selection context; do not invent a Skill ID or label a report as a dataset.

The runner's `--skill` option forwards Skill values, but its current payload puts the same resource into both `selectedResources` and `datasets`. Report compatibility of that payload has not been verified: do not advertise the model-runner example below as a tested report workflow. Use a verified report conversation contract, then validate the actual report-tool execution, applied filters and returned data. Stream completion alone does not prove the report was queried. If the built-in capability is unavailable, report the limitation; model fallback requires sufficient evidence of equivalent report calculations and filters, not merely a model binding.

## Execution and result checks

The helper's `ok`, `stream_exit=0`, and round `NORMAL` describe execution/transport completion only. Likewise, `queryRpcSync` may return HTTP 200 and outer `success=true` while its inner result has `status=error`. Read the final answer and query-tool results before claiming success. A normally completed Agent may report a database connection error and produce no data. For file requests, require an actual file artifact, a successful download, and verified file contents; an empty artifact list does not pass file-delivery acceptance. Diagnose the recorded underlying error before changing prompts or creating another conversation.

## Discover IDs; do not hardcode them

Use these read APIs before the first run in a new environment:

```bash
smartbi describe aichat.getAgentItems --profile <PROFILE> --agent
smartbi describe aichat.getLlmConfigs --profile <PROFILE> --agent
smartbi describe aichat.queryTrainedSuccessResources --profile <PROFILE> --agent
```

Then call the relevant operation with `--profile <profile>` and a temporary request file. Use the exact Agent ID returned by `getAgentItems`; custom Agents normally appear as `customagent_<RAW_AGENT_ID>` in `queryRpc`, while internal Agent workflow APIs use the raw ID.

For the standard Baize data-insight workflow, the default Agent is `customagent_AGENT_DATA_INSIGHT_ASSISTANT` (`dataInsightAssistant`). The helper uses this ID when `--agent-id` is omitted. If it is unavailable, verify the deployment with `getAgentItems`; do not silently substitute another Agent.

## Request contracts and resource types

Describe each selected operation in the target environment. `queryRpc` uses the streaming request envelope `jsonRpcStreamReq`; The currently verified `queryRpcSync` contract requires `req`; recheck each target deployment. Do not switch endpoints while retaining the other envelope. The bundled runner supports streaming `queryRpc` only; it is not a synchronous runner.

Resolve selectedResources[].type and datasets[].type from the actual resource metadata and validate against the operation's accepted schema. Do not copy DATA_MODEL from a generic example as the resource type or assume all models are AUGMENTED_DATASET. The current generic JSON-RPC schema permits additional properties and does not itself prove downstream ResourceType acceptance; if metadata and examples conflict, inspect the applicable resource contract or report the unresolved mismatch. The runner requires --dataset-type explicitly; it passes that verified value unchanged and does not maintain a fixed resource-type map.

For new/old indicator-model questions, use `metric-model-query.md` to distinguish the catalog root from the queryable/AI-selectable resource. In one verified environment the AI resource list contains `AUGMENTED_DATASET` and `TABULAR_DATASET`, including a data model associated with an `MT_MODEL`, but not the `MT_MODEL` root itself. This is an observed mapping, not a ban on AI questions for new indicator models; verify the target deployment's accepted resource or dedicated entry point before invoking AI, and validate the answer against its executed query.

Step limits, tool concurrency, knowledge precedence and model selection belong to the deployed Agent's configuration. Reuse its current settings; do not hardcode values copied from a past graph into direct queries or other deployments. For behavior inspection read `insight-agent-behavior.md`.

## Recommended one-command run

From the skill directory:

```bash
<PYTHON> <SKILL_DIR>/scripts/baize_session.py run \
  --profile <PROFILE> \
  --agent-id customagent_AGENT_DATA_INSIGHT_ASSISTANT \
  --dataset-id <MODEL_ID> \
  --dataset-name '<MODEL_NAME>' \
  --dataset-type <RESOURCE_TYPE> \
  --question '<QUESTION>' \
  --out-dir <EVIDENCE_DIR>
```

Optional flags include `--llm-config-id`, repeated `--skill`, `--knowledge-file`, `--use-personal-knowledge`, `--need-inquiry`, and `--web-search`. `--agent-id` defaults to `customagent_AGENT_DATA_INSIGHT_ASSISTANT` and can be omitted for the standard data-insight Agent. The helper:

1. generates `convId`, JSON-RPC ID, and message ID;
2. calls `aichat.createConversation`;
3. runs `aichat.queryRpc` as SSE;
4. stores `stream.ndjson` and stderr;
5. calls `getConversationRounds` and `queryChatLogs`;
6. removes temporary request JSON files;
7. prints only an evidence summary.

The output directory contains a manifest and raw response evidence. Review it before committing; logs can contain business data and should normally stay outside source control.

## Parse and download file artifacts

`queryRpc` returns an SSE stream. The reusable helper
`scripts/artifact_io.py` extracts `result.kind == "artifact-update"` file parts;
it does not treat a server URI as a local file. Inspect a captured stream first:

```bash
<PYTHON> <SKILL_DIR>/scripts/artifact_io.py inspect <EVIDENCE_DIR>/stream.ndjson
```

Download the first advertised result file through the current binary endpoint,
then inspect its tabular contents:

```bash
<PYTHON> <SKILL_DIR>/scripts/artifact_io.py download <EVIDENCE_DIR>/stream.ndjson \
  --profile <PROFILE> \
  --output <EVIDENCE_DIR>/artifacts/result.xlsx

<PYTHON> <SKILL_DIR>/scripts/artifact_io.py read <EVIDENCE_DIR>/artifacts/result.xlsx
<PYTHON> <SKILL_DIR>/scripts/artifact_io.py read <EVIDENCE_DIR>/artifacts/result.xlsx --all-sheets
```

The default download request is `aichat.downloadQueryResult` with a
`filePath` body. For an installation exposing the S3 CGI endpoint, pass its
operation and request field explicitly (for example, `--request-field s3Uri`).
The reader uses pandas: the first Excel sheet is read by default, `--all-sheets`
returns sheet metadata for every sheet, and CSV/Parquet are read as one table.

The conversation runner leaves existing behavior unchanged. Add
`--download-artifacts` to `scripts/baize_session.py run` to automatically parse
the completed stream and download files into `<out-dir>/artifacts` (or the
directory supplied with `--artifact-dir`).

## Inspect an existing conversation

```bash
<PYTHON> <SKILL_DIR>/scripts/baize_session.py rounds \
  --profile <PROFILE> \
  --conv-id <CONV_ID> \
  --output <ROUNDS_JSON>

<PYTHON> <SKILL_DIR>/scripts/baize_session.py logs \
  --profile <PROFILE> \
  --conv-id <CONV_ID> \
  --query-id <OPTIONAL_ROUND_ID> \
  --output <LOGS_JSON>
```

Important round fields:

- `id`: round/query ID used to correlate logs;
- `status`: typically `NORMAL`, `RUNNING`, `ERROR`, or `INTERRUPTED`;
- `question`, `datasets`, and `queryType`: verify routing inputs;
- `duration` and `errorType`: execution evidence;
- `answer`, `result`, `agentLogContent`: outputs and embedded artifacts.

## Resume an interrupted stream

Do not create a second conversation simply because the SSE client disconnected:

```bash
<PYTHON> <SKILL_DIR>/scripts/baize_session.py resume \
  --profile <PROFILE> \
  --conv-id <CONV_ID> \
  --output <RESUMED_STREAM_NDJSON>
```

Use `aichat.stopStream` only when the user explicitly asks to stop a running task or a bounded monitoring policy has been exceeded.

### Truncated think streams and stuck RUNNING rounds

Think-heavy conversations can exhaust the client-side event cap while the server round remains `RUNNING` and `answer` is empty. Resume the same `convId` with a larger `--max-events`, then poll `getConversationRounds` until the status leaves `RUNNING`. Do not create a duplicate conversation.

### Extracting the final answer from round.answer

`round.answer` may be a JSON-encoded event array rather than plain text. Reconstruct the answer by merging text artifact parts according to their `append` flag, excluding reasoning parts such as `text/think` and intermediate tool logs such as `text/python` or `text/error`. Treat `kind == file` parts as deliverables and download them through `scripts/artifact_io.py`.

## Success criteria

Require both transport and business evidence:

- the stream reaches a final status, or a resumed stream does;
- `getConversationRounds` contains the expected round;
- the round status is `NORMAL` for success;
- the bound Agent and dataset are correct;
- expected nodes/artifacts are present;
- forbidden fallback paths are absent;
- logs and result tables agree with the claimed outcome.

For a governance gate, always run at least one admitted case and one rejected/clarification case. The latter must prove that SQL/MQL/Python/result-table nodes were not executed.
