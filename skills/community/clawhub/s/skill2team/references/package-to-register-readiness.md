# Package-to-Register Readiness

`Delivery: package` is a Codex readiness contract, not a loose artifact dump.

Skill2Team 1.9.2 stops at package. A package must still be designed so that a later Codex-capable environment can safely register and use it through manifest-scoped steps.

## Hard runtime requirement

The registered entry agent and every registered specialist agent must actually be installable, invocable, handoff-capable, and gate-checkable in Codex before anyone describes the target team as runnable.

Generated files are not proof of runtime execution. Registered target-team execution must not fall back to sequential or single-agent simulation. If the active Codex thread cannot hot-load generated target-agent types, a target workflow may continue only through real current-session subagents with `target_run_fanout_status=real_session_target_subagents`; it must not be described as registered target-team execution.

## Required package contents

Every package that may later be used in Codex must include:

- runtime artifact for every planned top-level agent;
- exactly one user-facing entry-agent artifact;
- `design-intermediate-results.json` and `docs/design-intermediate-results.md`;
- `design-output.zip`, `design-output-manifest.json`, and `docs/design-output-archive.md`;
- `entry-agent-startup-welcome.json` and `docs/entry-agent-startup-welcome.md`;
- a generated target-team agents/functions list;
- `agent-profiles.json`, `profiles/*.agent-profile.json`, and `docs/agent-profiles.md`;
- `.codex/config.toml` with `config_file` entries;
- `s2t-agent-registry.json`;
- `.codex/s2t-agent-registrations/<team_id>.json`;
- `docs/runtime-invocation-contract.md`;
- `runtime-invocation-contract.json`;
- `design-package-conformance.contract.json` and `docs/design-package-conformance-contract.md`;
- `runtime-instruction-conformance.json` and `docs/runtime-instruction-conformance.md`;
- `meta-team-audit.contract.json` and `docs/meta-team-audit-contract.md`;
- `docs/register-readiness-contract.md`;
- `register-readiness-contract.json`;
- `docs/post-package-prompt-templates.md`;
- `post-package-prompt-templates.json`;
- `docs/team-usage-guide.md`.

## Package-time status

```yaml
registration_status: not_registered
entry_agent_runnable: false
registered_files: []
registered_target_team_smoke_status: not_registered
target_run_fanout_status: not_started
```

## Package release gate

The package release gate must check artifact completeness, entry-agent startup welcome presence, required user input node preservation, agent profile completeness, source-derived runtime constraint materialization, no hard-coded source example leakage, model invocation policy compliance, independent audit status, and design-output archive plus Codex-only package-end prompt coverage.

If `design-package-conformance.contract.json` or `runtime-instruction-conformance.json` reports `reexecution_required=true`, the package can be inspected but must not be registered for source-faithful execution until the named `reexecute_from` phase is rerun.

## Later Codex smoke tests

A later Codex registration/use workflow must collect evidence for:

1. **Entry invocation**: invoke the registered entry agent by runtime name and receive an intake/state-lookup response that renders or summarizes the startup welcome page.
2. **Specialist handoffs**: send shallow work orders to every non-entry specialist agent and receive structured results.
3. **Gate blocking**: show that an independent reviewer/verifier can block an incomplete or unsafe output.
4. **State/artifact handoff**: preserve a named artifact id or state key across at least one handoff.

If any check cannot be performed because generated target-agent types are not available in the active thread, the workflow may use real current-session target subagents only if they can actually be launched and tracked as separate roles. Otherwise the registered entry agent must stop with `target-team execution blocked`, explain the missing runtime capability or evidence, and give recovery steps. It must not continue as a single-agent or sequential simulation.

Skill2Team package output may include instructions and prompt templates for these checks, but must not claim the team is runnable until Codex runtime evidence exists.

## Later non-Codex continuations

Optional API-service, Hermes, OpenClaw, or other framework follow-ups belong to design-continuation material archived in `design-output.zip`. They must use the package's profile artifacts and framework-neutral agent relationship architecture map, clearly state the model service mode, and must not appear as package-end next actions or claim Codex custom-agent execution when using an API service.
