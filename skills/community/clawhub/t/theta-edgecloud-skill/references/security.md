# Security scope

This describes the current release. Offline regression tests use synthetic credentials and
mocked transports. They never make real attacks or real network calls.

## Controls

- Packaging: the runtime ships as one unminified bundle, `dist/index.js`, built from `src/` by
  `npm run build` (TypeScript, then esbuild). It exports only `executeThetaRuntimeCommand`,
  `listThetaRuntimeCommands`, `thetaRuntimeCommandSchemas`, `thetaCommandRequiresConfirm` and the
  read-only `theta()` facade; internal transports, configuration readers and policy lists are not
  exported from it. `src/` is included for review. Only `dist/index.js` is the supported runtime
  entry point.
- No runtime dependencies, shell execution, wallet or chain signing, local RPC adapters or local
  file reads. This package defines no install hooks. Development installs use
  `npm ci --ignore-scripts`.
- Origins:
  - On-demand accepts only `https://ondemand.thetaedgecloud.com`.
  - Dedicated inference accepts HTTPS subdomains of `thetaedgecloud.com` or
    `onthetaedgecloud.com`. The latter also hosts other customers' deployments, so configure
    only your own endpoint. A caller cannot replace the operator-configured endpoint, and Basic
    auth is never reused for a different origin.
  - The hosted MCP client uses one fixed origin, `https://controller.thetaedgecloud.com/mcp`.
  - Credentials, nonstandard ports, paths, queries and fragments in configured origins are
    rejected. Every transport refuses redirects.
- Approval: outside dry-run, `confirm` must be the boolean `true` for:
  - every create/update/start/stop/delete of deployments, GPU nodes, RAG agents and documents,
    video uploads, videos, streams and ingestor selection, and every AI Characters write
    (characters; session create, delete, context and message);
  - the four hosted-MCP write tools (create/start/stop/delete GPU node). Any other non-read MCP
    tool name is refused;
  - inference on any service not on the low-cost allowlist. The allowlist covers the live chat
    models, `stable_diffusion_xl_turbo`, `image_to_image`, `esrgan`, `blip`, `llava` and
    `whisper`. Video (for example `seedance_2_5`), retired, unknown and future services are gated
    by default;
  - any on-demand `webhook`/`callback` field, at any depth, which must also be `https`.
    Dedicated-endpoint chat rejects webhook/callback fields.
- Request bodies are copied once to plain JSON (running any getter or `toJSON`), then every check
  runs on that copy, and only that copy is sent.
- Spend bounds: on-demand chat, chat-shaped `infer` and dedicated-endpoint chat clamp
  `max_tokens` to 1..5000 and remove alternative length or fan-out fields
  (`max_completion_tokens`, `max_new_tokens`, `n`, `best_of` and similar). `wait` is 0..60.
- GPU node creation requires a positive `max_price_per_hour_usd` cap, which is sent to Theta. The
  MCP client looks up the resource's listed price first, and refuses when it is unknown or above
  the cap.
- Dry-run: blocks every write and inference. It still performs authenticated reads (HTTP GETs
  and read-only hosted-MCP `tools/call` POSTs). A caller-supplied environment can enable dry-run
  but cannot disable an operator-enabled dry-run.
- Credentials are not logged. Runtime results, facade results and previews replace values under
  names that mark secrets (password, token, secret, API key, authorization, credential) with
  `[redacted]`. Only numeric usage counts such as `prompt_tokens` are kept. `theta()` reports only which
  credential families are configured. Provider error text is sanitized and truncated.
- Tools are sent only to models that return structured tool calls (GLM-5.3 and GLM-5.3-Flash),
  unless the caller sets `allowUnverifiedTools` to exactly `true`. Then results carry no
  tool-call guarantee.
- Resource path components are encoded. Empty, dot and control-character IDs are rejected, and
  unknown command names (including prototype names) are rejected.
- Retries: only GET reads are retried. A write or inference request is never resent to the same
  URL. Deployment start/stop/delete try one alternate documented route (`/deployments/...`)
  only when the first route answers 404/405, meaning that route does not exist, so the action is
  not applied twice. Malformed or unterminated event streams fail rather than claim success.
- Disposable deployment validation returns `ok` only when create, readiness and verified cleanup
  succeed and, for the default `openai` probe, an inference smoke call (from `smokeMessage`)
  succeeds. `gradio` probes validate readiness and cleanup only. `smokeTested` reports whether
  inference was exercised. Unknown handles or list shapes never prove deletion.

## Trust and limits

`confirm:true` is supplied by the calling agent. It records, but cannot verify, that the user
approved the exact action. This is a trusted-operator API library, not a sandbox or a spending
firewall. Use least-privilege project and game keys, provider-side quotas and protected secret
storage.

Model-generated tool calls are returned as data and never executed; validate and authorize
their arguments independently.

Non-Theta destinations are opt-in:
- presigned cloud-storage upload URLs issued by Theta, to which the agent PUTs user-approved
  files;
- `https` webhooks you pass, to which Theta POSTs results. The runtime cannot verify that you own
  the URL; only pass your own.

Outputs can contain user content or signed media URLs. Treat them as private and untrusted.
Name-based redaction cannot catch secrets inside free text, so do not log complete
provider responses or publish customer inputs.

Automated scans, an independent adversarial review and exploit-style regression tests reduce
risk but cannot establish absolute security.
