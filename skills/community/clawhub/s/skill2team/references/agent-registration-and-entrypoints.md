# Agent Registration and Entrypoints

Skill2Team 1.9.2 produces Codex **packages**. It does not expose a separate registration delivery. The package must still contain enough manifest information and prompt templates for a later Codex-capable environment to register and use the generated target team safely.

## Entry-agent rule

Every generated target team must have exactly one user-facing entry agent.

The entry agent owns:

- user intake;
- state lookup;
- route/work-order setup;
- shallow specialist handoff;
- final synthesis;
- refusal to self-approve specialist outputs.

A package must not tell the user to invoke the entry agent as a registered runtime agent until Codex registration and smoke-test evidence exist. After registration, the entry agent must still block with `target-team execution blocked` if it cannot actually hand off to registered specialist agents and real current-session target subagents are unavailable.

## Package manifest requirements

Every package must include `s2t-agent-registry.json` and `.codex/s2t-agent-registrations/<team_id>.json` with:

```json
{
  "managed_by": "skill2team",
  "target_runtime": "codex",
  "model_invocation_policy": {
    "default_model_runner": "OpenAI Codex",
    "direct_model_api_calls_default": false
  },
  "team_id": "<team_id>",
  "entry_agent_id": "<entry_agent_id>",
  "registration_status": "not_registered",
  "entry_agent_runnable": false,
  "registered_target_team_smoke_status": "not_registered",
  "target_run_fanout_status": "not_started",
  "allowed_current_session_target_fanout_status": "real_session_target_subagents",
  "registered_files": [],
  "generated_target_team_agents": [
    {
      "agent_id": "<entry_agent_id>",
      "function": "User-facing intake, state lookup, routing, shallow handoff, and synthesis.",
      "entry": true,
      "artifact_path": ".codex/agents/<entry_agent_id>.toml"
    }
  ],
  "next_use_prompt_templates": {
    "design_to_package_prompt": "...",
    "design_continuation_codex_package_register_start_openai_codex": "...",
    "design_continuation_api_service_runner": "...",
    "design_continuation_hermes_openai_codex_profile": "...",
    "design_continuation_hermes_api_profile": "...",
    "design_continuation_openclaw_openai_codex_profile": "...",
    "design_continuation_openclaw_api_profile": "...",
    "package_end_codex_register_and_start_openai_codex": "...",
    "current_session_target_team_fanout_prompt": "..."
  }
,
  "target_team_execution_guard_policy": {
    "codex_target_team_execution_requires_real_registered_agents": true,
    "codex_target_team_execution_allows_real_session_subagents_when_registered_agents_unavailable": true,
    "session_subagent_success_status": "real_session_target_subagents",
    "block_status": "target-team execution blocked",
    "forbid_single_agent_or_sequential_simulation": true
  }
}
```

## Fixed S2T meta-team ids

For Codex, the fixed 1.9.2 meta-team agent ids are:

- `s2t-meta-entry`
- `s2t-meta-source-mapper`
- `s2t-meta-architecture-designer`
- `s2t-meta-workflow-orchestrator`
- `s2t-meta-runtime-adapter`
- `s2t-meta-evaluation-reviewer`

The last id is retained for compatibility, but its role is **Quality Reviewer** in this package-only model.

## Codex package layout

```text
.codex/
  config.toml
  agents/
    <agent_id>.toml
  s2t-agent-registrations/
    <team_id>.json
AGENTS.md
s2t-agent-registry.json
design-intermediate-results.json
design-output.zip
design-output-manifest.json
entry-agent-startup-welcome.json
runtime-invocation-contract.json
register-readiness-contract.json
design-continuation-prompt-templates.json
post-package-prompt-templates.json
```

## Design continuation and package-end guidance

After `Delivery: design`, provide continuation prompts for package, Codex, API-service runners, Hermes, OpenClaw, and other selected frameworks. When a user asks to register, replace, or use a shared generated target-team package, keep `Delivery: package` and provide package-end Codex register/start/use prompts only. The prompt must use placeholders such as `<SOURCE_SKILL_ZIP>`, `<GENERATED_TARGET_TEAM_PACKAGE>`, and `<CODEX_PROJECT_ROOT>` and must not hard-code a specific source task.

The registered entry agent must render or summarize `docs/entry-agent-startup-welcome.md` before entering the first real migrated workflow stage, collect required user input nodes, and default to preserving source human-interaction steps.

## Registered target-team execution rule

A generated target-team package must include this rule in its runtime invocation contract and generated agent instructions:

```text
If the registered entry agent cannot dispatch work to the named specialist agents through the Codex runtime, use real current-session target subagents only when independent Codex subagents can actually be launched for generated target profiles and the run records `target_run_fanout_status=real_session_target_subagents`. Otherwise stop with `target-team execution blocked`. Do not perform specialist work inside the entry agent while claiming multi-agent target-team execution.
```
