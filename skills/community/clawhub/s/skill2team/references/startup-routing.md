# Startup Routing

Skill2Team uses route and delivery selectors. Runtime is Codex-only in this build. Execution path is a separate selector.

## Selector order

1. **Execution path**: `direct-skill` by default, or `meta-team-first` when explicitly requested.
2. **Route**: `source-to-team`, `brief-to-team`, or `guided-to-team`.
3. **Delivery**: `design` or `package`.
4. **Runtime**: use `codex` whenever deployable artifacts are requested.
5. **Architecture method**: default to framework-neutral agent architecture relationship graph with profile-based agents.
6. **Model invocation policy**: default to OpenAI Codex runtime/custom-agent invocation; do not route actual model work through direct API calls unless the user explicitly chooses API-run role simulation or API-service follow-up.
7. **Human-interaction execution mode**: ask before source conversion starts. Default to `preserve_source_human_interaction_steps`; full automation requires explicit user choice and audit.

If source material is missing, ask for it before analyzing. If deployable artifacts are requested, set `Target runtime: codex` and use neutral placeholders such as `<SOURCE_SKILL_ZIP>`.

## Delivery mapping

| Old or informal request | Use |
|---|---|
| inspect / inventory / diagnose | `Delivery: design` |
| architecture report / team design / restructure plan | `Delivery: design` |
| validate / check packageability | Use the relevant internal gate: design quality gate inside `design`, or package release gate inside `package`. |
| generate files / create artifacts / runtime package | `Delivery: package` |
| install / register / replace agents | Provide post-package Codex registration/use prompt template; do not create a new delivery mode. |
| report / compare / benchmark / evaluate | Handle as design review or package quality review section; do not create a new delivery mode. |
| revise | Rerun the relevant delivery with previous output as source material. |
| restore / rehydrate | Treat the previous capsule/package as `source-to-team` source material and rerun `design` or `package`. |
| Hermes/OpenClaw conversion | Treat as a design-continuation prompt. Do not put this in package-end prompts. |
| API service in Codex workspace | Treat as a design-continuation or explicitly labeled API-run role simulation prompt. Do not put this in package-end prompts. |

## Route defaults

| User phrase | Route | Delivery |
|---|---|---|
| convert this skill into a team | `source-to-team` | `design` or `package` when artifacts are requested |
| redesign this old team | `source-to-team` | `design` |
| turn this brief into agents | `brief-to-team` | `design` |
| ask me questions first | `guided-to-team` | `design` |
| generate Codex agent files | `source-to-team` | `package` |
| register these generated agents | `source-to-team` | `package` plus post-package Codex registration/use template |
| compare old workflow and new team | `source-to-team` | `design` review or `package` release review |
| restore from Team2Skill capsule | `source-to-team` | `design` or `package` |

## Architecture/workflow routing rule

For `design` and `package`, keep these separate:

- Agent Architecture Map: who owns what, who routes, who reviews, who shares state, and why the agent count is justified.
- Workflow Orchestration Map: runtime sequence, branch, loop, gate, fan-out/fan-in, required user input node, human wait, checkpoint, resume, and terminal behavior.

Use framework-neutral agent profiles as the default representation. Do not require a specific multi-agent runtime unless a later API-service follow-up explicitly selects one.

## Count rule

Prefer 5-6 top-level agents. Ask for or provide a strong rationale for fewer or more.
