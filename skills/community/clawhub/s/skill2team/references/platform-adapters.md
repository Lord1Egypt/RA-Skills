# Platform Adapters

Skill2Team 1.9.2 generates Codex packages only.

## Codex package shape

```text
.codex/
  config.toml
  agents/
    <agent_id>.toml
  s2t-agent-registrations/
    <team_id>.json
profiles/
  <agent_id>.agent-profile.json
AGENTS.md
s2t-agent-registry.json
agent-profiles.json
design-intermediate-results.json
design-output.zip
design-output-manifest.json
entry-agent-startup-welcome.json
agent-architecture.map.json
workflow-orchestration.map.json
flow-control.contract.json
runtime-invocation-contract.json
register-readiness-contract.json
design-continuation-prompt-templates.json
post-package-prompt-templates.json
docs/
  design-intermediate-results.md
  design-output-archive.md
  entry-agent-startup-welcome.md
  agent-architecture-map.md
  workflow-orchestration-map.md
  flow-control-contract.md
  agent-profiles.md
  runtime-invocation-contract.md
  register-readiness-contract.md
  design-continuation-prompt-templates.md
  post-package-prompt-templates.md
  team-usage-guide.md
```

## Codex config requirements

Use `config_file`, not `path`, because Codex custom-agent loading expects the registered agent file through that key.

```toml
[features]
multi_agent = true
enable_fanout = true

[agents]
max_threads = 6
max_depth = 1

[agents.s2t-target-example-entry]
config_file = "./agents/s2t-target-example-entry.toml"
```

## Package-time manifest rules

At package time:

- `target_runtime = codex`;
- `architecture_method = framework-neutral agent architecture relationship graph with profile-based agents`;
- `model_invocation_policy.default_model_runner = OpenAI Codex`;
- `registration_status = not_registered`;
- `entry_agent_runnable = false`;
- `registered_files = []`;
- `planned_registered_files` covers every planned top-level agent and the registration manifest;
- `generated_target_team_agents` lists all target agents and functions;
- `agent_profiles` covers every planned top-level agent;
- `design_continuation_prompt_templates` covers design-to-package and optional non-Codex continuations as design-result material;
- `next_use_prompt_templates` and `package_end_prompt_templates` cover Codex package-use prompts only.

## Design-continuation and package-end registration/start guidance

Skill2Team design output should provide continuation prompts for package, Codex, API-service runners, Hermes, OpenClaw, and other selected frameworks. Skill2Team package output should provide manifest-scoped package-end Codex registration/start/use prompts only. It should not relabel registration or external conversion as a new Skill2Team delivery mode.

Every Codex package must include a team usage guide, entry-agent startup welcome page, and runtime invocation contract. They must distinguish unregistered package use from registered entry-agent use, rewrite source self-invocation prompts to the generated entry-agent contract, preserve required user input nodes by default, and end with Codex-only paste-ready prompt templates.

## API-service, Hermes, and OpenClaw adapters

Optional API-service, Hermes, OpenClaw, or other framework follow-ups can build a multi-agent runtime from the framework-neutral architecture relationship graph, `agent-profiles.json`, and `profiles/*.agent-profile.json`. These paths belong to design-continuation material and must state their model service mode:

- OpenAI Codex model service;
- API model service.

Only OpenAI Codex model-service paths can claim OpenAI Codex model execution. API-service follow-ups must label themselves as API-service follow-up or API-run role simulation.

## Codex target-team no-simulation rule

A generated target team registered in Codex should execute through the registered entry agent and real specialist handoffs. If the active thread cannot hot-load generated target-agent types, the package may execute through real current-session subagents only when the run records `target_run_fanout_status=real_session_target_subagents` and keeps registered smoke status pending. If the runtime cannot expose either registered handoff or real current-session fan-out, the entry agent must stop with `target-team execution blocked`; it must not claim Codex target-team execution while running a single-agent or sequential simulation.
