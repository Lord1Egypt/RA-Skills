# Theta EdgeCloud skill

Offline security review passed on 2026-10-03, including independent adversarial
testing and exploit-style regressions. ClawHub's post-publication rating is separate.
See [security scope](references/security.md) for controls and residual risks.

Read [SKILL.md](SKILL.md) for the operating procedure and
[capabilities](references/capabilities.md) for supported commands, credentials,
current API gaps and primary sources.

## Validate

```bash
npm ci --ignore-scripts
npm run check
npm test
```

The package includes source, generated runtime, tests and references. Four former
placeholder tests now exercise real contracts/safety gates. Offline mocked tests
are not a substitute for live provider proof.

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

## Improvements

- GLM-5.3/Flash direct chat, structured tools, streaming parallel arguments and
  correlated tool-result continuation; reasoning retained separately.
- Discovery includes full prediction/input schemas and current GLM/image catalog entries.
- Training/custom templates and stopped GPU restart by base ID.
- Existing video/stream/ingestor operations exposed through runtime dispatch.
- Twelve game-key AI Characters/session API adapters with dry-run and contract tests.
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

`npm ci --ignore-scripts && npm test`. `npm run build` compiles `src/` with TypeScript into the
private `build/` folder (used by the tests), then bundles it with esbuild into the single
unminified `dist/index.js`. The build is reproducible byte for byte.

Installing this package does not change Gateway or model configuration.
GPU provisioning, live Video/Characters tests and expanded controller logs/usage APIs
remain subject to the credentials, API contracts and authority described in the skill.

Credit: [Theta Communications](https://www.thetacommunications.com).
