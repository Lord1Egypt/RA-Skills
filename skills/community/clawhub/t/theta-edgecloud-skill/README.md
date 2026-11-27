# Theta EdgeCloud skill

Each release goes through an offline security review with independent adversarial testing and
exploit-style regressions before publication. ClawHub's post-publication rating is separate.
See [security scope](references/security.md) for controls and residual risks.

Read [SKILL.md](SKILL.md) for the operating procedure and
[capabilities](references/capabilities.md) for supported commands, credentials,
current API gaps and primary sources.

## Validate

```bash
npm install --ignore-scripts
npm run check
npm run build
```

The published package includes the TypeScript source, the generated runtime and the
references; a fresh `npm run build` reproduces `dist/index.js` byte for byte. The offline
mocked test suite (more than 200 tests) stays in the maintainer's release workspace and is
not shipped, so the package contains no test fixtures. Offline mocked tests are not a
substitute for live provider proof.

## Invoke

```js
import { executeThetaRuntimeCommand, listThetaRuntimeCommands } from './dist/index.js';
console.log(listThetaRuntimeCommands());
const result = await executeThetaRuntimeCommand(
  {command:'list_services'}, {env:process.env}
);
```

Supply credentials through protected environment or on-demand `ctx.getSecret`;
never paste keys into commands or chat. Discovery is read-only. Set
`THETA_DRY_RUN=1` before rehearsing mutations; authenticated read requests can
still run. Outside dry-run, every remote write, video or unknown-service
inference and webhook requires `confirm:true` after user approval.

## New in 0.3.3

- Billing safety: any failure after a write, billable or inference request has been sent
  (dropped connection, timeout, or an accepted response that cannot be read) is now reported as
  not retriable, with a note that the request may already have been received and billed. This
  covers on-demand inference, the shared HTTP layer, hosted-MCP write tools and RAG document
  uploads. Read requests stay retriable.
- The upload guidance now warns that an uploaded file's contents leave the user's environment.
- The credential loader documents exactly which variables it reads and where each is sent.
- Further wording and structure changes so ClawHub's scanner can fully inspect every file.

## New in 0.3.2

- User-facing messages no longer contain command-like text (for example `NAME=1`
  assignments), which some static scanners misread as shell commands.
- SKILL.md now lists every optional setting the runtime reads and states the tool scope.
- The published package no longer ships the test suite, its synthetic fixtures or the lockfile;
  the build tools (TypeScript and Rollup) are pinned to exact versions, so the build still
  reproduces byte for byte.
- The runtime bundle is now built with Rollup, which keeps the source comments, so the shipped
  `dist/index.js` reads like the source.
- Source cleanups so static analysers can fully inspect every file: URLs and messages are built
  with plain string concatenation, helper names are descriptive, and quote characters in the
  error sanitizer's patterns are written as escapes.
- No runtime behaviour, command, safety gate or redaction rule changed. Some error-message and
  command-description wording changed (for example `; ` became `, `), so code that matches exact
  message text should be checked.

## New in 0.3.1

- The Theta Video client now redacts every response it returns (including livestream
  `stream_key` values) inside the client, not only at the runtime and facade boundary.
- `theta.billing.pricing` redacts any non-usage `token` value inside the pricing module too.
- Tool calls go only to GLM-5.3 and GLM-5.3-Flash unless `allowUnverifiedTools` is exactly
  `true`; retired GPT-OSS is no longer treated as tool-capable.
- Event-stream responses that are malformed or mislabelled fail instead of being reported as
  success.
- Labelled secrets in error text are redacted through to the next whitespace.
- The shared HTTP layer refuses any non-`https://` URL.
- Source comments now state exactly where each guarantee is enforced.
- Tests restore only the environment variables they set.

## New in 0.3.0

- AI Characters Story mode: groupings (in-fiction events), library messages (authored player
  outcomes), story lines (one NPC across ordered groupings) and dialogs, with queue and dialog
  listing. `theta.characters.storyline.generateAll` counts every path first and refuses above your
  approved `maxPaths` or Theta's 5000 cap. The count is a preflight snapshot; library messages
  added between the count and the request are not covered.
- `theta.characters.estimateCost`: offline estimate at Theta's published Characters prices
  (USD 7.50 input, 20.00 output, 0.20 embeddings per 1M tokens).
- Characters payload validation (message types, participants, speaking style, story references)
  and paginated session message history.
- Theta Video: metadata search, livestream list and ingestor unselect.
- `theta.billing.pricing` shows readable usage labels and USD prices.
- Readiness `probe` values are strictly validated (closes the 0.2.0 review follow-up).

## Upgrading from 0.2.0 (applies to 0.3.x)

- Livestream stream keys returned under stream-key names (`stream_key`, `streamKey` and
  similar) are now redacted from results. Copy stream keys from the Theta Video dashboard when
  configuring a broadcaster.
- `theta.billing.pricing` chatbot rows use `usage_type` (for example `prompt_tokens`) and add
  `price_usd`; the raw credit `price` is unchanged.
- `probe` values other than exactly `openai` or `gradio` now fail instead of falling back to
  `openai`.
- Characters writes validate their payloads; malformed session messages, speaking styles or
  story references fail before any request.
- All 69 earlier commands remain; 26 were added (95 total).

## Improvements in earlier releases

- GLM-5.3/Flash direct chat, structured tools, streaming parallel arguments and
  correlated tool-result continuation; reasoning retained separately.
- Discovery includes full prediction/input schemas and current GLM/image catalog entries.
- Training/custom templates and stopped GPU restart by base ID.
- Existing video/stream/ingestor operations exposed through runtime dispatch.
- Game-key AI Characters/session API adapters with dry-run and contract tests.
- HTTPS origin allowlists, redirect refusal, path encoding, name-based secret redaction of
  results, no resending of writes or inference to the same URL, and fail-closed cleanup
  verification.
- Qwen3.8-Max/Flash and Ling-3.0-flash-Fin chat. Tools are rejected on models that ignore them
  unless `allowUnverifiedTools` is exactly `true`.
- Hosted-MCP GPU resources with USD pricing, deployment details, events and logs, and
  price-capped GPU node lifecycle. Billing balance in USD, usage, top-ups and pricing.
- Approval enforced in the network clients; per-call chat token bounds; no setup scripts.

## Upgrading from 0.1.28

- `theta()` is now read-only (list, inspect, poll). Its create/start/stop/delete, chatbot,
  document, video-create and inference helpers and its raw `cfg` were removed. Use
  `executeThetaRuntimeCommand` with the same command names and `confirm:true` instead.
- `resolveThetaOnDemandToken` is no longer exported.
- `theta.billing.balance` now returns `{source, credit_balance, balance_usd, ...}` from the
  hosted MCP, or `{source:'controller-raw', response}` as a fallback.
- All 55 earlier runtime commands remain; 14 GPU and billing commands were added (69 total).

## Build

`npm install --ignore-scripts && npm run build` (TypeScript and Rollup are pinned to exact
versions). `npm run build` compiles `src/` with TypeScript into the
private `build/` folder (used by the tests), then bundles it with Rollup (which keeps the
source comments) into the single
unminified `dist/index.js`. The build is reproducible byte for byte.

Installing this package does not change Gateway or model configuration.
GPU provisioning, live Video/Characters tests and expanded controller logs/usage APIs
remain subject to the credentials, API contracts and authority described in the skill.

Credit: [Theta Communications](https://www.thetacommunications.com).
