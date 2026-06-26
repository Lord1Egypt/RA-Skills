# Writing Triadic State Contract — v2.9.1

This reference defines the durable handoff contract between Creator, Executor, Reader, and Evolution Analyst. Use it when a session has multiple modes enabled, when a long-form project resumes, or when Reader scoring includes SEO/style extensions.

## 1. Session State

Each writing session folder should contain `session-state.md`. Creator creates it after Phase 1 locks the task and updates it at every phase transition.

```markdown
# Session State

## Identity
- Session: YYYY-MM-DD_HHmm-topic
- Mode: full | instant | long-form | revision
- Template: [template name]
- Blend: none | [template A:70% + template B:30%]
- Public publishing: yes | no

## Active Modules
- Style clone: on | off | skipped
- SEO: on | off | skipped
- Long-form: on | off
- Multi-modal iteration: none | diff-modify | feature-synthesis | full-rewrite

## Phase Status
- Phase 0 memory read: pending | done | skipped
- Phase 0.5 style clone: pending | done | skipped
- Phase 1 intent lock: pending | done
- Phase 1.5 research: pending | done | skipped
- Phase 1.6 SEO: pending | done | skipped
- Phase 2 rules: pending | done
- Phase 3 drafts: pending | done
- Phase 4 reader review: pending | done | skipped
- Phase 5 user review: pending | done
- Phase 5.5 evolution: pending | done | skipped

## Decision Log
- [time] Decision: ...
- [time] User override: ...
- [time] Risk / fallback: ...
```

## 2. Required Artifacts

Creator must not call the next role until the required artifact for the current phase exists or the skip reason is written in `session-state.md`.

| Phase | Required artifact | Skip record |
|---|---|---|
| 0 | `MEMORY.md` read or initialized | `Phase 0 memory read: skipped` with reason |
| 1 | `需求分析.md` | never skip in full mode |
| 1.5 | `联网调研.md` | private topic, user says no search, or no network |
| 1.6 | `写作规则.md` contains `## SEO 约束` | non-public or non-SEO template |
| 2 | `写作规则.md` + `写作计划.md` | never skip in full mode |
| 3 | `初稿-v1.md` + `初稿-v2.md` | instant mode may use one final draft |
| 4 | `读者点评.md` | instant mode only |
| 5 | `终稿.md` + `用户反馈.md` | feedback may be empty |
| 5.5 | MEMORY update proposal or no-op note | user says trial only |

## 3. Handoff Checks

### Creator → Executor

Before spawning Executor, Creator must provide:

- intent summary from `需求分析.md`
- writing rules from `写作规则.md`
- writing plan from `写作计划.md`
- selected template skeleton and fatigue words
- active modules from `session-state.md`
- style fingerprint if enabled
- SEO constraints if enabled

If any required item is missing, Creator fixes the artifact first instead of asking Executor to infer it.

### Executor → Creator

Executor output must include:

- all requested drafts or the requested revision mode output
- version difference summary in full mode
- word count range status
- warnings for unmet constraints

Executor must not silently ignore SEO, style clone, word count, or historical taboo constraints. If a constraint conflicts with another constraint, report the conflict at the end.

### Creator → Reader

Before spawning Reader, Creator must provide:

- all draft versions
- target reader persona
- active scoring modules
- historical taboos and style fingerprint if available
- SEO checklist if SEO is enabled

Reader uses the adaptive 100-point scoring table from `reader-prompt.md`; optional modules redistribute weight instead of increasing the maximum score.

### Creator → Evolution Analyst

Creator must provide `session-state.md` and all artifacts generated in the session. Evolution Analyst returns structured update suggestions only; Creator is responsible for merging them into MEMORY.md without deleting historical records.

## 4. Failure Handling

- If network research fails, write the failure and continue with local knowledge.
- If MEMORY.md is missing, initialize it with empty global/type sections before Phase 1.
- If `知识库.md` is missing, create it before the first successful research sync.
- If Reader rejects all drafts below 70, Creator should ask the user whether to revise requirements or run Mode C full rewrite.
- If two active modules conflict, user instructions override module defaults, then historical preferences, then template defaults.
