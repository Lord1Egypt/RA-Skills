---
name: skill-autogenesis
description: Review completed work, summarize reusable procedures, identify recurring workflow patterns, and decide whether to create a skill, patch an existing skill, store a memory note, or do nothing. Built for agents that need structured procedural memory in Hermes, OpenClaw, or similar tool-using environments without confusing abstract rules with reusable procedures.
version: 1.3.2
author: Agent Skill Master
license: MIT
metadata:
  hermes:
    tags: [skills, automation, summarization, procedural-memory, openclaw, hermes]
    related_skills: [hermes-agent, plan, writing-plans]
---

# Skill Autogenesis

Turn repeated successful work into reusable procedural memory.

Default stance: evaluate first. Do not turn every solved task, preference, or policy note into a new skill.

This skill makes the agent do five things during normal task execution:
1. Analyze what was just done.
2. Summarize the reusable procedure if one actually exists.
3. Track whether the same procedure keeps recurring.
4. Apply `skill_manage`-style lifecycle rules for create, patch, edit, write_file, and remove_file behavior.
5. Choose the lightest correct persistence action: create a skill, patch an existing skill, store a compact memory note, or do nothing.

This skill is inspired by Hermes Agent's agent-managed skill behavior and its guidance to save complex or non-trivial workflows as skills. Source links are listed in `references/sources.md`.

## When to Use

Load this skill when the user wants the agent to:
- continuously summarize solved work into reusable knowledge
- build skills automatically instead of waiting for manual requests
- monitor repeated task patterns across a session or across past sessions
- bootstrap self-improving behavior in another agent such as OpenClaw
- convert high-frequency workflows into durable skill files

Load this skill early in a session if automatic skill creation is desired.

## Operating Contract

When this skill is active, treat every substantial task as a candidate for procedural learning, not as an automatic instruction to create a new skill.

A task becomes a skill candidate when at least one of these is true:
- the workflow required 5 or more meaningful tool calls
- the workflow involved debugging, retries, or correction before success
- the workflow is likely to recur for this user or project
- the same intent appears 3 or more times in the current session or in session history
- the user explicitly asks for automation, reuse, codification, or standardization

A skill candidate is only a review target. The default output of the review is a classification decision, not a file write.

Do not create a skill for trivial one-step work, ephemeral conversation-only advice, highly project-specific context that will not generalize, or abstract policy notes that are better stored in memory or prompts.

## Quick Reference

Use this decision rule after every meaningful success:

1. Summarize the solved workflow in 4 blocks:
   - trigger
   - inputs and prerequisites
   - exact procedure
   - verification
2. Decide what kind of knowledge was produced:
   - executable procedure
   - preference or policy note
   - one-off result with no reusable pattern
3. Classify the workflow:
   - one-off
   - reusable but not frequent yet
   - frequent and stable
4. Estimate recurrence evidence:
   - current-session repetition count
   - past-session repetition count if `session_search` exists
   - explicit user preference for reuse
5. If the result is an executable procedure and it is frequent and stable, create or patch a skill.
6. If the result is reusable but not frequent enough, store a compact memory note if memory exists.
7. If the result is a preference, boundary, or policy note, update memory or prompts instead of creating a skill.
8. If the workflow is not stable yet, wait and keep observing.

## Decision Matrix

Use this routing table before any persistence action:

- executable procedure + stable + verified + recurring -> create or patch a skill
- executable procedure + promising but not frequent yet -> store a compact memory note or keep observing
- user preference, approval boundary, naming convention, style rule, or governance note -> update memory or prompts, not a skill
- one-off result, temporary conclusion, or incomplete hypothesis -> no persistence yet

Hard stop rules:
- If `knowledge_type=preference`, never call `skill_manage(create)` or `skill_manage(edit)`.
- If `knowledge_type=policy`, never call `skill_manage(create)` unless the output also contains a complete executable procedure with trigger, ordered actions, and verification.
- If `recommended_action` is `memory`, `prompt`, or `none`, do not write or modify any skill files.
- When in doubt between procedure and policy, classify as non-skill first and require stronger evidence before writing files.

## Output Contract

Before creating or updating anything, produce an internal decision record with these fields:
- knowledge_type: procedure | preference | policy | one_off
- recurrence: none | possible | confirmed
- stability: low | medium | high
- verification: missing | partial | passed
- recommended_action: create | patch | memory | prompt | none

Use this exact template internally before any persistence action:

Classification:
- knowledge_type:
- recurrence:
- stability:
- verification:
- recommended_action:

Reason:
- why this is or is not an executable reusable procedure
- why the selected persistence layer is the lightest correct one

Only `recommended_action=create` or `recommended_action=patch` may lead to skill file updates.
If any field is missing, default to `recommended_action=none` until the classification is complete.

## Procedure

### Phase 1. Capture the solved pattern

After any meaningful success, extract:
- the user intent
- the exact tools used
- the ordered steps that actually worked
- failure modes encountered
- the verification signals that proved success

Write the summary in concise operational language, not narrative prose.

Before doing anything persistent, ask one discriminator question:
- Did this task produce an executable reusable procedure, or did it only produce a rule, preference, constraint, or one-off conclusion?

If it did not produce an executable reusable procedure, do not create a skill from it.

### Phase 2. Detect recurrence

Use the strongest evidence available.

Preferred sources, in order:
1. current session context
2. `session_search` results for similar tasks, intents, file types, services, or error patterns
3. memory entries about user habits, project conventions, or repeated workflows
4. direct user phrasing such as "we do this often", "make this reusable", or "use this in other agents"

Treat recurrence as confirmed when any of these rules match:
- the same or equivalent workflow appears 3 or more times across current and past sessions
- the user explicitly requests automatic reuse
- the workflow is long, stable, and clearly generic enough for future reuse

Recurrence alone is not enough. A repeated preference or governance note is still not a skill unless it defines a reusable executable procedure.

### Phase 3. Decide whether to create a skill

Run this checklist in order. All checks must pass before create or patch.

Checklist:
1. Is the result an executable procedure rather than a rule, preference, or policy statement?
2. Does it have a clear trigger condition?
3. Does it contain ordered actions another agent can actually execute?
4. Does it define at least one verification signal?
5. Is it stable enough to repeat without relying on accidental context?
6. Is it free of secrets, temporary identifiers, and mostly user-specific data?
7. Would storing it as memory or prompt guidance lose important procedural detail?

Create a skill only when all conditions hold:
- the result is an executable procedure, not merely a rule, preference, or policy statement
- the workflow has a clear trigger condition
- the steps are deterministic enough to be followed again
- verification criteria are known
- the procedure is not mostly user-specific secrets or temporary data
- the skill can be expressed as reusable instructions rather than raw transcript history

If the conditions are not met, do not force a skill.

Route non-skill outcomes to the right storage layer:
- user preference or communication style -> user memory
- durable environment fact or project convention -> memory
- agent governance or default behavior -> prompt or runtime config
- unfinished hypothesis or weak pattern -> no persistence yet

### Phase 4. Apply `skill_manage` lifecycle logic

When `skill_manage` or an equivalent skill API exists, use the same action-selection logic instead of treating every change as a new skill.

Action selection rules:
- use `create` when no related skill exists and the workflow is frequent, stable, reusable, and classified as `knowledge_type=procedure`
- use `patch` for targeted fixes, missing steps, corrected commands, improved verification, or recurring pitfalls in an existing procedural skill
- use `edit` only when the skill structure must be reorganized substantially and targeted patching is no longer clean
- use `write_file` to add or update supporting files such as references, templates, scripts, assets, and human-facing docs
- use `remove_file` to delete obsolete supporting files that would otherwise mislead later runs
- use `delete` only with explicit user approval, because deletion is destructive

Hard stop enforcement:
- never use `create` for preferences, policy notes, approval boundaries, style guidance, or naming conventions by themselves
- never use `patch` or `edit` to convert a non-procedural rule into a fake skill
- if the best destination is memory or prompt, stop the skill lifecycle here and use that destination instead

Default policy:
- prefer `patch` over `edit`
- prefer updating an existing related skill over creating a near-duplicate
- confirm with the user before destructive actions such as `delete`
- if a supporting file is large or structured, keep it outside `SKILL.md` and manage it through supporting-file actions

### Phase 5. Create the skill

If `skill_manage` exists, create a new skill only when the recurrence threshold is met, the workflow has passed verification, the active environment allows autonomous skill creation, and the decision record says `knowledge_type=procedure`.
If the environment uses a different skill API, map the same lifecycle actions semantically.
If no skill creation capability exists, produce a complete `SKILL.md` draft and `README.md` draft for the user or parent agent to save.

The created skill must contain:
- YAML frontmatter
- a sharp description of the problem solved
- target users
- key features
- trigger conditions
- numbered procedure steps
- pitfalls
- verification
- source links when factual claims depend on external references

When file support exists, also create or update:
- `README.md` for human-facing overview
- `references/` files for source links or API notes
- `templates/` files for reusable skill skeletons, prompts, or configs
- `scripts/` files when the workflow depends on repeatable helper automation
- `assets/` files only when the skill genuinely needs non-text resources

Hermes-specific implementation note:
- `skill_manage(action='write_file')` only supports supporting files under approved subdirectories such as `references/`, `templates/`, `scripts/`, and `assets/`
- a root-level `README.md` is not a supporting-file target for `skill_manage(action='write_file')`
- if the environment requires a root `README.md`, create or update it through ordinary file-writing tools or direct filesystem output instead of `skill_manage(action='write_file')`

### Phase 6. Name and place the skill

Use a concise kebab-case name.

Naming rules:
- prefer action plus domain, such as `summarize-support-tickets` or `deploy-preview-app`
- avoid vague names such as `automation-skill` or `helper`
- if the skill is meta-behavior for agents, prefer names such as `skill-autogenesis`, `workflow-distillation`, or `agent-procedural-memory`

Prefer a category that matches the task domain.
If the skill applies across agents, place it in an agent or workflow category.

### Phase 7. Update existing skills instead of duplicating

Before creating a new skill, check whether a related skill already exists.
If one exists and the new workflow is a refinement, patch the existing skill instead of creating a duplicate.

Patch immediately when you discover:
- missing prerequisites
- wrong commands
- missing fallback logic
- a recurring pitfall
- a better verification step
- missing supporting files such as references, templates, or scripts

Use `edit` only if the whole skill needs structural reorganization.
Use `write_file` when the core logic is fine but the skill needs supporting files.
Use `remove_file` when a stale supporting file conflicts with the updated workflow.
Never use `delete` without explicit user approval.

## Skill Creation Template

When auto-creating a skill, follow this structure:

1. Frontmatter
   - `name`
   - `description`
   - `version`
   - `author`
   - `license`
   - `metadata.hermes.tags`
   - optional related skills
2. Body sections
   - title
   - purpose sentence
   - when to use
   - quick reference
   - procedure
   - pitfalls
   - verification
   - sources

## Auto-Creation Policy

Default thresholds:
- create immediately for workflows with 5 or more meaningful tool calls plus clear reuse potential
- create immediately after a difficult debugging workflow that ended in a reliable fix
- create after 3 confirmed repetitions of substantially the same workflow
- create immediately when the user explicitly asks for reusable cross-agent behavior

Hard gate before any create action:
- the outcome must be an executable reusable procedure with concrete steps, tools, and verification
- if the outcome is only a rule, preference, guardrail, naming convention, approval boundary, or abstract heuristic, do not create a new skill from it

Lifecycle policy:
- choose `create` only when no suitable skill exists yet
- choose `patch` as the default update action
- choose `edit` only for large structural rewrites
- choose `write_file` for README, references, templates, scripts, and other supporting files
- choose `remove_file` for obsolete supporting files
- choose `delete` only with explicit user approval

Default safety boundaries:
- do not auto-publish
- do not include secrets, tokens, personal data, or machine-specific absolute paths unless the skill is explicitly local-only and the user wants that
- do not encode temporary incident details as if they were general rules
- do not claim success without a verification step
- do not perform destructive skill deletion without user approval

## Fallback Behavior for Non-Hermes Agents

If running in OpenClaw or another agent framework:
- look for an equivalent to `skill_manage`, file tools, memory, and session search
- keep the same recurrence logic and output contract
- if tool names differ, map behavior semantically instead of abandoning the workflow
- map lifecycle actions explicitly: `create`, `patch`, `edit`, `write_file`, `remove_file`, and guarded `delete`
- use source resolution policy in this order: GitHub source, then `references/fallback/`, then mark the claim as `[UNVERIFIED]`
- if only file writing is available, generate the skill package directly as files
- if no persistence exists, return the draft skill and a short adoption note

## Pitfalls

- Do not confuse topic similarity with procedure identity. Similar requests can still require different workflows.
- Do not create a skill from an unfinished or partially verified process.
- Do not duplicate an existing skill just because the wording changed.
- Do not save raw conversation summaries as skills. Convert them into executable procedure.
- Do not overfit a skill to one repository, hostname, or credential set unless the user requested a local-only skill.
- Do not mistake a rule for a skill. A rule says what should be true. A skill says when to act, what to do, and how to verify it worked.
- Do not create a skill for user preferences, approval requirements, naming conventions, or communication style. Store those in memory or prompts.
- Do not use `skill_manage(create)` as a generic persistence tool. If the outcome is policy-like, preference-like, or one-off, creating a skill is the wrong action.

## Verification

A newly created or updated skill is considered valid only when all checks pass:
1. The trigger condition is explicit.
2. The procedure is ordered and actionable.
3. The skill contains at least one verification section.
4. The name is unique and descriptive.
5. The description explains problem solved, target user, key features, and when to use.
6. The content contains no secrets or temporary identifiers.
7. A README is generated alongside the skill package when file support exists.
8. Source links are attached when the skill references external behavior or framework semantics.
9. The internal classification record exists and ends with `recommended_action=create` or `recommended_action=patch`.
10. The checklist in Phase 3 passed completely.

## Sources

Use this source resolution policy:
1. Prefer the GitHub source listed in `references/sources.md`.
2. If the GitHub source is unavailable, use the matching local copy in `references/fallback/`.
3. If neither source is available, mark the statement as `[UNVERIFIED]`.

See `references/sources.md` for the primary references that informed this skill's logic and thresholds.
If GitHub links are unavailable, use the local fallback copies in `references/fallback/`.
