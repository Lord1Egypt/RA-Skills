# Xerg

Reviewed CLI version: **0.35.2**.

This already-published CLI pin is reviewed independently of the skill's release version. New skill or package releases do not authorize an automatic pin change.

This skill uses the exact reviewed CLI version, including doctor-generated follow-up commands. Bare `xerg` examples below require an explicitly approved installation verified with `xerg --version` against that version. Stop on a mismatch; do not silently upgrade or substitute another version. The pin selects the top-level npm package, not its transitive dependencies or cryptographic integrity. Permission to install, inspect local data, or upload remains separate.

Remote OpenClaw collection is available through the reviewed CLI 0.35.2, which includes the remote-command and archive security corrections. Obtain explicit permission for the exact host or Railway service and evidence paths before connecting or copying data. Use existing operator-managed authentication; never request credential contents in chat. Run the pinned doctor with the approved remote selection, verify its version, and preserve its shell-safe audit recommendation unchanged. Remote access does not authorize configuration changes or hosted upload. Prefer an approved local export when remote access is unavailable.

Find wasted AI spend in OpenClaw, Hermes, QM, Claude Code, Cursor, and any framework that can export a JSON event payload.

Xerg is a local-first CLI for auditing AI spend in dollars, not raw token counts. It reads OpenClaw logs/transcripts or an independent sanitized trace capture, Hermes v0.17-v0.20.1 `state.db` with optional observer/certified trace enrichment, QM snapshots, Claude Code transcripts, and Cursor usage exports — plus event payloads from any framework via `xerg ingest` — separates three evidence-strict monetary findings from seven neutral signals, reports what each detector assessed, and lets you measure compatible fixes with `--compare`.

Everything runs locally by default. The CLI is publicly installable from npm as `@xerg/cli`, but it is not open source. No account is required for local audits. A Free hosted workspace keeps the last 30 days of pushed audits and groups related incremental snapshots into expandable series; hosted MCP is included with Team, Growth, Scale, and Enterprise.

Hosted pricing uses Monthly Audited Agent Spend from known spend in explicitly pushed runtime audits: Free through $2,000 per UTC month, Team at $99 through $10,000, Growth at $299 through $50,000, Scale at $799 through $250,000, and custom Enterprise above $250,000. Team, Growth, and Scale have identical capabilities. Historical imports, duplicate-review spend, and unpriced usage do not count toward MAAS.

The `npx @xerg/cli@0.35.2` path may fetch and execute the exact published npm package before running Xerg. After explicit approval, install it once with `npm install -g @xerg/cli@0.35.2` if you prefer a global installation.

## Installation and discovery

| Host or surface | Installation or discovery path | Review boundary |
| --- | --- | --- |
| Terminal-capable agent | [Canonical skill](https://xerg.ai/skill.md) | Review fetched content before use; this mutable URL does not pin a revision or install it persistently. |
| Agent Skills hosts | [Public repository](https://github.com/xergai/skills), discoverable on [skills.sh](https://www.skills.sh/xergai/skills/xerg) | Use `skills@1.5.25` and an operator-reviewed full repository SHA; keep host and scope selection interactive. |
| OpenClaw | [ClawHub `@xerg/xerg`](https://clawhub.ai/xerg/skills/xerg) | Select and review an exact skill version and its files; never substitute the bare `xerg` slug. |
| Hermes | [Legacy discovery index](https://xerg.ai/.well-known/skills/index.json) or a reviewed raw GitHub Markdown URL | A full repository SHA in the raw URL fixes the source revision; the discovery index and hosted skill URL are mutable. |
| Local folder import | The Xerg `SKILL.md` bundled inside the approved npm CLI package | Review the bundled file independently; its instructions can differ from the current skill release. |

Installation, package download, local inspection, remote access, workspace connection, payload preview, and upload require their own applicable approvals. A listing or successful installation does not certify the skill, authorize execution, or establish current artifact identity.

The accepted package and skill release is **0.35.3**. Its instructions deliberately select the independently reviewed CLI **0.35.2**; the release version and executable review pin are separate identities.

## Install

Give a terminal-capable agent the universal cold-fetch prompt:

```text
set up https://xerg.ai/skill.md
```

The agent first reviews the fetched skill and summarizes the software it may install and the local sources it may inspect. Persistent skill installation, an npm download, local runtime inspection, workspace connection, payload preview, and upload are separate stages; each applicable stage requires its own approval.

For Agent Skills hosts (Claude Code, Codex, Cursor, and others), first obtain and review a specific **40-character hexadecimal commit SHA** from the public `xergai/skills` repository. After approving the installer download and skill installation, replace the placeholder below with that reviewed SHA. Do not run the placeholder or substitute a branch, tag, or automatically selected latest revision. The pinned installer requires Node 22.20 or newer (separate from the reviewed CLI's Node 22.15.0 minimum; Node 23 requires 23.8.0 or newer).

```bash
npx --yes --package=skills@1.5.25 skills add 'https://github.com/xergai/skills/tree/<REVIEWED_PUBLIC_REPO_FULL_SHA>/skills/xerg' --skill xerg
```

The command leaves agent selection and installation scope interactive; `npx --yes` only accepts the approved package download. The installer version and source revision are both explicit; this does not pin transitive dependencies or provide a cryptographic integrity guarantee. If no reviewed SHA is available, stop the installer step or import an already-reviewed local skill folder through your host's supported flow after permission. Current-session use of the fetched skill still requires its separate permissions and must not persist it implicitly. A CLI version pin does not establish that an older package's bundled skill is the corrected revision.

Then ask your agent to audit your AI spend. Installation does not authorize local inspection or upload; the agent asks separately and explains the findings.

Install the CLI directly:

```bash
npm install -g @xerg/cli@0.35.2
```

Or run without installing:

```bash
npx @xerg/cli@0.35.2 init
```

## Native host installation

The [native host installation guide](https://xerg.ai/docs/skill-bundle#native-host-installation) provides the reviewed-version OpenClaw command and full-SHA Hermes URL procedure. Installation and host discovery were exercised with OpenClaw **2026.9.4** on Node **24.16.0**, and Hermes **0.21.0** at commit `29112bef099274229cadff79cdff7bf7b99c4b77` on Python **3.12.14**. This does not certify model execution or other host revisions.

Use an already-approved host installation, review the selected skill's exact files, and keep native security checks and confirmation enabled. Stop on a blocked install. The skill version is separate from its reviewed CLI pin, and installation does not authorize running the CLI or inspecting runtime data. A mutable hosted URL is not equivalent to the guide's reviewed full-SHA source.

## What It Finds

- **Retry waste** from stable charged failed/aborted attempt chains ending in success
- **Tool-loop waste** from exact no-progress tool input/result/state repetitions
- **Cache churn** only when a cache lifecycle costs more than its uncached counterfactual
- Seven separate neutral signals for deep loops, context outliers/growth, fixed cadence, premium-model routine labels, cache-read concentration, and Max Mode concentration

Current JSON findings carry affected and avoidable spend, evidence and impact bases, and detector version. Signals carry bounded observed metrics plus optional associated spend and basis; associated spend is never classified as waste. Compare output reports monetary deltas only when active-finding coverage is compatible.

Claude Code streaming records are reconstructed before analysis. Repeated tool-name chains are reported as neutral argument-diversity evidence, with only SHA-256 input/result digests and byte counts retained locally. A high distinct-input ratio is consistent with fan-out, while a low ratio is a reason to inspect; neither creates avoidable spend. Use `xerg explain <item-id>` to inspect a saved finding, signal, or chain packet.

## Quick Start

Interactive first run (humans):

```bash
xerg init
xerg audit --compare
```

Non-interactive path (agents, scripts, CI): after the applicable permissions, verify that doctor's `cliVersion` is 0.35.2. Require its recommendation to select that exact version, preserve the complete shell-safe command, show it, and obtain audit approval before running it as printed. Stop on a version mismatch or mutable package reference. The subsequent examples require the verified installed CLI described above; they are not automatic follow-up actions.

```bash
npx --yes @xerg/cli@0.35.2 doctor --json
xerg audit --json
xerg audit --json --compare
xerg collect openclaw
xerg collect hermes --state-db "$HERMES_HOME/state.db"
xerg doctor --runtime qm
xerg audit --runtime qm --since 7d
xerg audit --otlp-file ./openclaw.capture.jsonl
```

Add `--runtime openclaw`, `--runtime hermes`, or `--runtime claude-code` when more than one local runtime is detected. QM is never auto-detected and always uses `--runtime qm` after administrator setup.

## Sources

- Local machine: OpenClaw, Hermes, and Claude Code (`xerg audit --runtime claude-code`)
- Explicit QM source: host-independent `qm-snapshot/v1`, strict view-only direct PostgreSQL, or the certified Fly-contained exporter
- Independent local OpenClaw traces: `xerg collect openclaw` or `xerg audit --otlp-file <capture.jsonl>`
- Certified local Hermes trace enrichment: `xerg collect hermes --state-db <path>` or `xerg audit --runtime hermes --state-db <path> --otlp-file <capture.jsonl>`
- Local Cursor usage export: `xerg audit --cursor-usage-csv ./cursor-usage.csv`
- Any framework's exported event payload: `xerg ingest --file payload.json`
- OpenClaw evidence exported from another host and supplied through an approved local path

If local defaults are empty, export the approved evidence to the local machine and pass an explicit local path.

When OpenClaw gateway logs and session transcripts both produce calls in the requested window, Xerg uses transcripts as the sole authority for totals and analysis and excludes gateway runs. This prevents additive accounting when the same activity is present in both formats. Transcripts preserve agent, lineage, and per-tool evidence, but can omit gateway-only activity; mixed reports therefore warn that activity and spend may be understated and findings may differ from a fully reconciled view. Gateway-only and transcript-only audits are unchanged. Use only `--log-file` or only `--sessions-dir` to select one local source kind explicitly.

Monetary and detector-coverage gates evaluate only that selected transcript evidence. Passing a gate does not certify omitted gateway-only activity.

## Optional Hosted Follow-Up

For skill-directed operation, inspect and approve each hosted stage separately:

```bash
XERG_SETUP_METHOD=skill XERG_AGENT_HOST=<host> npx --yes @xerg/cli@0.35.2 push --dry-run
XERG_SETUP_METHOD=skill XERG_AGENT_HOST=<host> npx --yes @xerg/cli@0.35.2 activate --connect-only
XERG_SETUP_METHOD=skill XERG_AGENT_HOST=<host> npx --yes @xerg/cli@0.35.2 push
```

The preview prints the intended payload and should be summarized locally rather than pasted into chat. Add `--organization-id <verified-org-id>` to the connection command only when that exact value is known. Use `push --file <path> --dry-run` and the same `--file` on upload for an explicitly selected prepared payload. Connection and upload require distinct approvals and must not be combined in skill-directed work. Human-operated CLI flows remain documented separately.

- `mcp-setup` prints or writes hosted MCP config for supported clients
- hosted Optimizations can copy a Fix with Xerg task; paid hosted MCP exposes `xerg_get_optimization({ optimization_id })` to retrieve the same content-free handoff without changing code or policy
- paid workspace admins can connect Linear and create one sanitized, one-way issue per Optimization; the integration does not synchronize issue status or change the Optimization automatically
- after an approved push, Fleet Overview leads with strictly validated seven-day before/after savings when available, keeps current waste separate, and can group identified-waste rates by department or runtime posture; runtime posture remains Not set until a workspace admin assigns `vpc`, `on-prem`, `saas`, `local`, `hybrid`, or `air-gap`, and is never inferred from audit evidence. Audit Detail adds daily Performance and detector-attributed Workflow economics, while Compare retains outcome evidence and Signal guidance remains explicitly non-monetary
- local audits and compare remain available if you skip hosted setup

## Restricted environments

Use an already installed or prefetched `@xerg/cli@0.35.2` when runtime package downloads are prohibited. Before a disconnected local audit, set `XERG_NO_UPDATE_CHECK=1` or `CI=1`, provide a dedicated writable XDG data directory for snapshots, and mount only the explicitly approved source files or directories read-only. Keep Xerg authentication outside the environment unless the user separately approves the applicable hosted operation. Pairing and upload are networked modes.

The registry's `dist.integrity` value can verify registry transport and cache bytes for the exact package, but it is not independent publisher provenance and does not cover the package's transitive dependency graph. The pushed payload contract is published in the MIT-licensed `@xerg/schemas` package; use `push --dry-run` to inspect the exact intended payload locally before separately approving an upload.

## Security And Data Flow

- Local audits read OpenClaw, Hermes, QM snapshots, Claude Code, Cursor usage, or ingest payload files and may write local JSON snapshots for `--compare`.
- Local commands remain telemetry-free. Explicit hosted pairing and push requests carry only a fixed, content-free execution-context envelope; the canonical skill sets a bounded `XERG_AGENT_HOST` hint on the same approved hosted command.
- Hermes uses `$HERMES_HOME/state.db` read-only by default and as its sole monetary authority. Optional observer telemetry and certified trace enrichment preserve authoritative token buckets and `economicAuditId`; analysis `auditId` changes when coverage/findings change. Push v7 includes content-free finding/signal coverage, daily pricing-coverage counts, and eligible evidence-strict results; detailed mechanics remain local.
- The reviewed CLI 0.35.2 includes the Hermes compatibility work documented in [Hermes analysis](https://xerg.ai/docs/hermes-analysis). Bounded live acceptance covered the exact v0.20.1, v0.20.6, and v0.21.0 pins, with partial lifecycle observation on the newer two pins and separately pinned OTLP acceptance. It can describe equivalent captured native starts as one logical request, with a local observed-start count and retry-inclusive latency, not per-provider-attempt detail. Missing native timing or conflicting evidence remains aggregate, including older captures. Usage absent from Hermes state accounting is absent from Xerg totals, not evidence of a zero provider charge. Newer package notices do not authorize changing the reviewed CLI pin or upgrading automatically.
- Xerg 0.24.2 certifies Hermes state schemas 16-25. A Hermes operator may separately install the optional observer described in [Hermes analysis](https://xerg.ai/docs/hermes-analysis). When present, Xerg reads its content-free events and bounded health state; this skill does not install, configure, start, restart, or modify observer state. Before new Xerg-directed Hermes activity, run `xerg doctor --runtime hermes --require-observer-live`; failed preflight exits `5`, and repairs cover only future activity. Existing aggregate audits remain available with their limitation before totals and conclusions.
- Hermes v0.20 terminal generated/truncated values may be conservative byte floors and render as “At least”; returned bytes remain exact, and Xerg never dereferences a Hermes spill path. Xerg 0.24.0 terminal mechanics were not certified for v0.20.x and could understate these values. Hermes v0.20.1 auxiliary tasks such as `title_generation` remain task-scoped aggregates when public request hooks do not expose them; their economics stay included and their sequence analysis stays explicitly unavailable.
- QM currently supports one-shot snapshot, strict direct, and Fly-contained collection. Strict direct mode uses a dedicated export-view-only reader. Fly Managed Postgres instead uses a disclosed one-shot process boundary inside QM core and does not claim database least privilege. Both use a backed-up identity key and HMAC raw IDs before persistence; content fields are not exported, and `openrouter/auto` placeholders remain unpriced. Offline QM Slack audits accept only an authorized pre-created snapshot. The CLI must be explicitly approved, provisioned, and version-verified by an operator in the administrator's private runtime; agents must not install it implicitly or initiate live collection. The runtime receives no database URL, identity key, Fly token, provider credential, or Xerg credential. Continuous follow capture, durable tool-history capture beyond QM's retention window, and live Slack-triggered collection are not currently supported.
- Both trace collectors bind only to loopback, sanitize before persistence, receive traces only, and never push automatically. `analysisCoverage`, `toolActivity`, and `workloadEconomics` remain local.
- Remote OpenClaw collection requires explicit permission for the target and evidence paths. Exporting to an approved local path remains an alternative; neither option authorizes hosted upload.
- Xerg Cloud sync only happens when you run `connect`, `audit --push`, or `push`.
- Push payloads include audit totals, rollups, findings, recommendations, comparison deltas, and source metadata. They exclude raw prompt and response content, local source file paths, local snapshot store paths, and internal finding details.
- Push v7 carries separate content-free findings, signals, per-detector coverage, and daily pricing coverage. Signals may include an optional human-readable workflow/run label; current producers also add an optional requested audit interval, detector-attributed workflow waste, detector-versioned comparison finding changes, observed immediate parent-to-child agent-delegation rollups, and comparison pricing availability. Delegation rows show spend that is already counted in the child row and the audit total; never add them again. Monetary comparison fields are usable only when `spendComparisonAvailable` is explicitly true; identified-waste deltas additionally require `wasteComparisonAvailable`. Older v7/v6 payloads remain valid without those additive fields. Push v6 remains accepted and meters identically from daily runtime spend. Evidence references and internal details stay local.
- Local snapshots may contain versioned diagnostic packets with digests, byte counts, local paths, and inspection guidance. Raw or truncated tool arguments/results are never stored, and diagnostics, digests, paths, and per-TTL cache buckets never cross Push v7.
- Runtime costs may be observed, locally estimated, or unpriced. They are not authoritative provider invoices; Xerg does not currently ingest provider bills, reconcile invoices, or convert runtime audits to FOCUS.

## CI And Automation

```bash
xerg audit --push --fail-above-waste-rate 0.25
xerg audit --fail-above-waste-usd 100
xerg audit --json
```

## Links

- Docs: [xerg.ai/docs](https://xerg.ai/docs)
- Service status: [status.xerg.ai](https://status.xerg.ai)
- Skill: [xerg.ai/skill.md](https://xerg.ai/skill.md)
- npm: [@xerg/cli](https://www.npmjs.com/package/@xerg/cli)
- Pricing: [xerg.ai/pricing](https://xerg.ai/pricing)
- Support: `hello@xerg.ai`

## Ownership

This skill is maintained by [Xerg](https://xerg.ai) and synced to the public [xergai/skills](https://github.com/xergai/skills) repo from the Xerg release train, versioned with `@xerg/cli`. The skill content is free to install and use with any agent; the Xerg CLI it drives is publicly installable from npm but not open source.
