# Security And Operations

Use this reference when a workflow needs security review, authentication design, or day-two operations.

## Security Model Summary

GitHub Agentic Workflows uses five named security layers that work together to contain a confused or compromised agent:

1. **Read-only tokens**: The agent receives a GitHub token scoped to read-only permissions. Even if the agent attempts to create a pull request, push code, or delete a file, the underlying token does not allow it.
2. **Zero secrets in the agent**: The agent process never receives write tokens, API keys, or other sensitive credentials. Those secrets exist only in separate, isolated jobs that run after the agent has finished and its output has passed review.
3. **Network firewall**: The agent runs inside an isolated container. The Agent Workflow Firewall (AWF) routes all outbound traffic through a Squid proxy that enforces an explicit domain allowlist. Traffic to any other destination is dropped at the kernel level.
4. **Safe outputs**: The agent cannot write to GitHub directly. It produces a structured artifact describing its intended actions. A separate job with scoped write permissions reads that artifact and applies only what the workflow explicitly permits.
5. **Agentic threat detection**: Before any output is applied, a dedicated threat detection job runs an AI-powered scan of the agent's proposed changes, checking for prompt injection, leaked credentials, and malicious code patterns.

Professional use starts by assuming prompts, tools, and repository content can be adversarial or misleading.

## Least-Privilege Defaults

Prefer these defaults unless the workflow has a concrete reason to differ:

1. `permissions: read-all` or explicit read permissions.
2. Safe outputs for issues, comments, labels, pull requests, reviews, dispatch, and agent assignment.
3. Minimal `toolsets:` rather than broad GitHub or shell access.
4. `strict: true`.
5. `network.allowed` with `defaults` plus the smallest extra ecosystem or custom domains set.

Avoid direct `contents: write`, `issues: write`, or `pull-requests: write` on the agentic execution path when a safe output can model the same outcome.

## Safe Outputs

Safe outputs are the core professional pattern for repository writes.

Key points:

1. The agent runs read-only and emits a structured artifact describing its intended actions.
2. Before any output is applied, a dedicated threat detection job runs an AI-powered scan of the agent's proposed changes. It checks for prompt injection attacks, leaked credentials, and malicious code patterns. If anything looks suspicious, the workflow fails immediately and nothing is written to the repository.
3. After the threat detection gate, a separate job with scoped write permissions applies only what the workflow explicitly permits: hard limits per operation (such as a maximum of one issue per run), required title prefixes, and label constraints. The agent requests; a gated job decides.
4. Common outputs include `create-issue`, `add-comment`, `add-labels`, `create-pull-request`, `dispatch-workflow`, `call-workflow`, `assign-to-agent`, and `create-agent-session`.
5. `noop`, `missing-tool`, and `missing-data` are critical truthfulness and reliability tools.
6. `staged: true` is the safest rollout mode for new write-heavy workflows.

Professional prompt rule:

```text
If no action is needed, the agent MUST call noop with a concise explanation.
```

Without an emitted safe output, a safe-output workflow can fail at runtime even when analysis was correct.

## Network Policy

Use `network:` as both an egress control and a content-sanitization allowlist.

Recommended pattern:

```yaml
network:
  allowed:
    - defaults
    - node
    - "api.example.com"
```

Guidance:

1. Prefer ecosystem identifiers such as `node`, `python`, `containers`, or `github`.
2. Add custom domains explicitly.
3. Use blocked domains when privacy or compliance requires it.
4. Treat `(redacted)` URLs as a signal that the allowlist is incomplete.
5. Keep the firewall enabled in production.
6. If the installed compiler rejects custom domains in strict mode, keep the firewall narrow and fetch the needed sources in deterministic setup steps so the agent reads local files instead of making ad hoc outbound requests.

## Authentication

Engine authentication:

1. Copilot: `COPILOT_GITHUB_TOKEN`.
2. Claude: `ANTHROPIC_API_KEY`.
3. Codex: `OPENAI_API_KEY`.
4. Gemini: `GEMINI_API_KEY`.

Additional authentication is usually required for:

1. Cross-repository reads or writes.
2. GitHub Projects operations.
3. Remote GitHub tool mode.
4. Assigning Copilot or creating advanced safe outputs.

Use a GitHub App when possible for short-lived, scoped tokens. Copilot engine authentication itself still requires a PAT.

## Public Repository Safety

Public repositories need extra care.

1. Keep GitHub lockdown mode enabled for workflows that inspect user-generated content unless the workflow is explicitly low-risk.
2. Use restrictive safe outputs and approval controls for anything that can modify repository state.
3. Keep network policy narrow.
4. Review threat-detection prompts or steps for code-changing workflows.

If lockdown is blocking legitimate external contributor scenarios, change the workflow design before disabling protection.

## Observability And Operations

Use the CLI to manage production quality:

```bash
gh aw status
gh aw logs <workflow>
gh aw audit <run-id>
gh aw health
```

Use these signals:

1. Success rate and trend.
2. Token usage and AI Credits (AIC) cost.
3. Firewall denials and blocked domains.
4. Tool usage and missing-tool events.
5. Threat-detection outcomes.
6. Safe-output previews versus actual writes.

Cost control starts with visibility: use `gh aw logs` and `gh aw audit` to find runs consuming the most time, tokens, and AI Credits, then tighten prompts, triggers, and model choices before spend drifts upward. Set `max-ai-credits:` in frontmatter to cap the AI Credits a single run may consume. See [https://github.github.com/gh-aw/reference/cost-management/](https://github.github.com/gh-aw/reference/cost-management/) for the full cost-management reference.

GH-AW supports OpenTelemetry export: workflow traces and token data can be exported to OTLP backends for dashboards, alerting, and spend analysis. See [https://github.github.com/gh-aw/reference/open-telemetry/](https://github.github.com/gh-aw/reference/open-telemetry/).

## Operational Hygiene

1. Keep workflows small and single-purpose.
2. Use shared imports only when reuse is real and maintained.
3. Pin or review CLI versions deliberately in controlled environments.
4. Use `gh aw update` for sourced workflows and `gh aw upgrade` for repository-wide modernization.
5. Treat `.lock.yml` files as build artifacts that must stay in sync with compile-time changes.
6. Re-run validation and verbose compile output after a CLI upgrade before concluding that a workflow shape is still valid.