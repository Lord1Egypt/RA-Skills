# Design Continuation Prompt Templates

## Design to package

```text
Continue from the Skill2Team design result and generate a concrete Codex target-team package.
Use <SOURCE_SKILL_ZIP> as the source material and <GENERATED_TARGET_TEAM_PACKAGE> as the output package path.
Preserve the Agent Architecture Map, Workflow Orchestration Map, Control-Flow & Resume Contract, profile-based agents, design quality gate result, and no-hard-coding rule.
```

## Codex / OpenAI Codex continuation

```text
Use OpenAI Codex custom-agent/runtime invocation.
Register or run the profile-based target team from <GENERATED_TARGET_TEAM_PACKAGE> inside <CODEX_PROJECT_ROOT>.
Use package manifests as the source of truth and do not call direct model APIs.
```

## API-service runner continuation

```text
Build a framework-neutral API-service runner plan in <API_SERVICE_PROJECT_ROOT> from the target-team profiles in <GENERATED_TARGET_TEAM_PACKAGE>.
Use <API_MODEL_SERVICE_CONFIG> as the explicit API model service configuration.
Name a specific multi-agent framework only if the user explicitly selects one.
Label this as API-service follow-up, not Codex custom-agent execution.
```

## Hermes / OpenAI Codex profile conversion

```text
In <HERMES_WORKSPACE>, convert the Skill2Team design into Hermes profile-based agents.
Use OpenAI Codex for model execution.
Preserve profile ids, role boundaries, architecture/workflow separation, quality gates, and no-hard-coding rules.
```

## Hermes / API profile conversion

```text
In <HERMES_WORKSPACE>, convert the Skill2Team design into Hermes profile-based agents backed by <API_MODEL_SERVICE_CONFIG>.
Build a framework-neutral agent relationship graph and label the result as API-service follow-up.
```

## OpenClaw / OpenAI Codex profile conversion

```text
Create OpenClaw-compatible profile files from the Skill2Team design.
Use OpenAI Codex for model execution where model work is required.
Preserve global-skill metadata if publishing a skill, MIT-0/text-only constraints, architecture/workflow separation, independent review gate, and no-hard-coding rule.
```

## OpenClaw / API profile conversion

```text
Create OpenClaw-compatible profile files from the Skill2Team design and build execution as a framework-neutral agent relationship graph.
Use <API_MODEL_SERVICE_CONFIG> as the API model service configuration.
Label this as API-service follow-up.
Preserve MIT-0/text-only constraints, global-skill metadata, architecture/workflow separation, independent review gate, and no-hard-coding rule.
```
