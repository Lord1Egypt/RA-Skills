# Security scope

This describes the current release. Offline regression tests use synthetic credentials and
mocked transports. They never make real attacks or real network calls.

## Controls

- Packaging: the runtime ships as one unminified bundle, `dist/index.js`, built from `src/` by
  `npm run build` (TypeScript, then Rollup, which keeps the source comments). It exports only `executeThetaRuntimeCommand`,
  `listThetaRuntimeCommands`, `thetaRuntimeCommandSchemas`, `thetaCommandRequiresConfirm` and the
  read-only `theta()` facade; internal transports, configuration readers and policy lists are not
  exported from it. `src/` is included for review. Only `dist/index.js` is the supported runtime
  entry point.
- No runtime dependencies, shell execution, wallet or chain signing, local RPC adapters or local
  file reads. This package defines no install hooks. Development installs run npm install with
  lifecycle scripts disabled (the exact command is in README.md). The build tools (TypeScript
  and Rollup) are pinned to exact versions.
- Origins:
  - On-demand accepts only `https://ondemand.thetaedgecloud.com`.
  - Dedicated inference accepts HTTPS subdomains of `thetaedgecloud.com` or
    `onthetaedgecloud.com`. The latter also hosts deployments of other customers, so configure
    only your own endpoint. A caller cannot replace the operator-configured endpoint (the runtime
    command handlers reject request-level overrides), and Basic auth is never reused for a
    different origin. Internally, disposable validation probes its own newly created endpoint
    with explicit auth.
  - The hosted MCP client uses one fixed origin, `https://controller.thetaedgecloud.com/mcp`.
  - Credentials, nonstandard ports, paths, queries and fragments in configured origins are
    rejected. Every transport refuses redirects.
- Approval: outside dry-run, `confirm` must be the boolean `true` for:
  - every create/update/start/stop/delete of deployments, GPU nodes, RAG agents and documents,
    video uploads, videos, streams, ingestor selection and unselection, and every AI Characters
    write (characters; session create, delete, context and message; Story mode groupings,
    library messages, story lines, dialogs, dialog recreation and story line generation);
  - the four hosted-MCP write tools (create/start/stop/delete GPU node). Any other non-read MCP
    tool name is refused;
  - inference on any service not on the low-cost allowlist. The allowlist covers the live chat
    models, `stable_diffusion_xl_turbo`, `image_to_image`, `esrgan`, `blip`, `llava` and
    `whisper`. Video (for example `seedance_2_5`), retired, unknown and future services are gated
    by default;
  - any on-demand `webhook`/`callback` field, at any depth, which must also be `https`.
    Dedicated-endpoint chat rejects webhook/callback fields.
- Validated request bodies (AI Characters payloads and on-demand/dedicated inference requests)
  are copied once to plain JSON (running any getter or `toJSON`), then every check runs on that
  copy, and only that copy is sent. Other bodies (for example Theta Video create/stream/select)
  are serialized once at the HTTP boundary without that pre-validation copy.
- Spend bounds: on-demand chat, chat-shaped `infer` and dedicated-endpoint chat clamp
  `max_tokens` to 1..5000 and remove alternative length or fan-out fields
  (`max_completion_tokens`, `max_new_tokens`, `n`, `best_of` and similar). `wait` is 0..60.
- Story line generation (`theta.characters.storyline.generateAll`) is a billable bulk action. It
  requires `confirm:true` and an integer `maxPaths` (1..5000) before any request. It then counts
  the paths with read requests (one library message per grouping, using the service's reported
  total when larger than the page) and refuses, with no write, when the count is above
  `maxPaths`, above Theta's 5000-path cap, zero, or cannot be read. Ambiguous, conflicting or
  malformed pagination totals and incomplete list pages also refuse, as do a `pagination` value
  that is not an object, unrecognised fields inside `pagination`, non-boolean
  `has_more`/`hasMore`, a non-zero `offset`, conflicting list fields and conflicting story line
  `grouping_ids`. The list response is read against an exact field allowlist: besides `body`,
  the one list field (`messages`, `library_messages` or `items`), `pagination` and the
  recognised paging fields, only plain (non-object) informational values are accepted (`status`,
  `message`, `code`, `success`, `error`, `request_id`, `id`, `grouping_id`, `storyline_id`,
  `npc_id`, `name`, `title`, `created_at`, `updated_at` and their camelCase forms). Any other
  field refuses, as does a list response that reports failure on the envelope or the body: `success`
  present and not `true`, a `status` of `err`, `error`, `errors`, `fail`, `failed` or `failure`
  (any letter case, surrounding spaces ignored) or an HTTP-style code of 400 or more, or an
  `error` value other than null, false or an empty string. A full page (as many items as a reported page size such as `per_page`, `limit`
  or `number`) refuses unless a total or `has_more:false` shows the list is complete. A list with
  no pagination metadata is treated as the complete list. The
  preflight count is a snapshot: library messages added between the count and the request are
  not covered; Theta's own 5000 cap still applies.
- AI Characters payloads are validated before any request: session message `type` and
  `participant_type`, character `speaking_style` values, story line `npc_id`/`grouping_ids`
  (1..20) and dialog `message_refs` (1..20). `session.messages` paging is bounded
  (`page` 1..10000, `number` 1..100). Action routes (`dialog.recreate`, `generate_all`) always
  send `{}` and ignore caller payloads.
- Video search filters are validated (1..10 keys matching `[A-Za-z0-9_][A-Za-z0-9_.-]{0,63}`,
  string values up to 256 characters); `page`, `number` and `operator` cannot be used as filter
  keys, and every value is URL-encoded.
- GPU node creation requires a positive `max_price_per_hour_usd` cap, which is sent to Theta. The
  MCP client looks up the resource's listed price first, and refuses when it is unknown or above
  the cap.
- Dry-run: blocks every write and inference. It still performs authenticated reads (HTTP GETs
  and read-only hosted-MCP `tools/call` POSTs). A caller-supplied environment can enable dry-run
  but cannot disable an operator-enabled dry-run.
- Credentials are not logged. Runtime results, facade results and previews replace values under
  names that mark secrets (password, token, secret, API key, authorization, credential, private
  key, mnemonic, livestream `stream_key`) with `[redacted]`; a name matches when it contains one
  of these words, so `sa_secret` or `game_api_key` match too. In plaintext error text, a label
  matched by the same rule (plus cookie, any `phrase` such as seed, recovery or pass phrase, seed
  words, access key and JWT), followed by `=`, `:`, `:=`,
  `=>` or a full-width colon or equals sign (U+FF1A, U+FF1D), has its value redacted as a whole unit (a quoted string, including typographic and
  back quotes and backslash-escaped quotes, a bracketed list or object, or an unquoted run up to
  whitespace, so commas, semicolons, `&` and closing brackets stay inside the value; a `Bearer`/`Basic` scheme word
  is kept). Unquoted mnemonic, phrase, seed-word and private key values, and any
  `-----BEGIN ...-----` key block (any letter case), are redacted to the end of the message. An unterminated quote or bracket redacts to the end of the message. Only
  the first 8 KB of an error body is examined, and the result is cut to 280 characters. Secrets in
  unlabelled free text, or under names that do not contain these words (such as a plain `key`
  field or a URL path), are not detected. `theta.billing.pricing` moves Theta's exact
  documented usage labels (`prompt_tokens`, `completion_tokens`, `embedding_tokens`) from
  `token` to `usage_type` so they stay readable; any other value under `token` is still redacted.
  Numeric values under `*_tokens` names (such as `prompt_tokens`) are kept as usage counts;
  this is a name-and-type rule, so a non-numeric value under such a name is redacted. `theta()` reports only which
  credential families are configured. Provider error text is sanitized and truncated.
- Tools are sent only to models that return structured tool calls (GLM-5.3 and GLM-5.3-Flash),
  unless the caller sets `allowUnverifiedTools` to exactly `true`. Then results carry no
  tool-call guarantee.
- Resource path components are encoded. Empty, dot and control-character IDs are rejected, and
  unknown command names (including prototype names) are rejected.
- Retries: only GET reads are retried. A write or inference request is never resent to the same
  URL. Deployment start/stop/delete try one alternate documented route (`/deployments/...`)
  only when the first route answers 404/405, meaning that route does not exist, so the action is
  not applied twice. Malformed or unterminated event streams fail rather than claim success: a stream must
  parse as JSON `data:` chunks and end with `[DONE]` or a reported `finish_reason`, and any
  non-JSON body sent as `text/event-stream` or containing `data:` lines that does not meet this
  fails with a non-retriable error (the request may already be billed, so it is never resent).
  Other successful non-JSON bodies are returned as `raw` text.
- Readiness `probe` must be exactly `openai` or `gradio` (default `openai`); anything else is
  refused before any request, in the runtime and in the internal command functions.
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
