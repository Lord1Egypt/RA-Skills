# Agent Independence Model

Skill2Team distinguishes between **logical independence** and **runtime independence**.

## Logical independence

Every recommended agent must have a canonical independence contract even if the target platform cannot create a fully separate runtime process.

Required fields:

| Field | Meaning |
|---|---|
| agent_id | Stable machine-readable id |
| display_name | Human-readable name |
| mission | One-sentence purpose |
| accountable_outputs | Outputs this agent owns |
| responsibilities | What the agent does |
| non_responsibilities | What the agent must not do |
| authority | What it can approve, reject, request, or escalate |
| owned_skills | Skills primarily owned by this agent |
| shared_skills | Skills this agent may use but does not own |
| restricted_or_forbidden_skills | Skills it cannot use or can only use through a gate |
| tools_policy | Allowed, denied, approval-required tools |
| memory_boundary | What state or memory it may read/write |
| input_contract | Required inputs |
| output_contract | Required outputs |
| handoff_contract | How it gives work to another agent |
| gates_owned | Validation or approval gates it owns |
| rerun_triggers | When it should rerun |
| execution_path | `direct-skill`, `meta-team-first`, or target-runtime artifact only |
| current_run_fanout_status | Whether the current run used direct-skill, registered real subagents, current-session real subagents, or was blocked because real Codex meta-team activation was not confirmed |
| target_subagent_fanout_supported | Whether Codex can run this role as a real subagent: `runtime-dependent` until runtime smoke tests pass, then runtime evidence may mark it usable. |
| execution_mode | `fanout`, `blocked`, or target-runtime artifact only |
| fallback_mode | What to do when the target platform or current runtime cannot run this role independently |

## Runtime independence

Runtime independence is Codex-dependent in this build. Skill2Team must not claim support for untested runtime profiles.

| Target | Concrete packaging |
|---|---|
| Codex | `.codex/agents/*.toml` custom agent files, `.codex/config.toml` with `multi_agent` and `enable_fanout`, `.codex/s2t-agent-registrations/<team_id>.json`, `AGENTS.md`, and usage/runtime contracts |

## Fan-out status rule

Runtime independence artifacts do not prove that the current Skill2Team run used real subagents. Every report and adapter package must state the selected execution path. If the run used default `direct-skill`, record `current_run_fanout_status: direct-skill-not-requested`. If Codex `meta-team-first` was selected, record `current_run_fanout_status: real_subagents` only after registered meta-agents actually ran and smoke-test evidence exists. If the running Codex thread cannot hot-load newly registered custom agents but real independent subagents execute the fixed S2T work orders, record `current_run_fanout_status: real_session_subagents` and keep registered meta-team smoke status pending. Otherwise record `blocked_no_real_codex_meta_team`, provide the reason, and stop instead of using a fallback run.

## Safety rule

If a platform offers persona/workspace separation but not sandboxing, say this explicitly and add tool or sandbox configuration recommendations where the platform supports them.
