---
name: build-skill
description: Use when creating or rewriting a skill and you want one strong, workflow-conformant version built through failure analysis, review, and refinement instead of a multi-draft tournament.
---

# /build-skill

Build one strong skill draft on purpose.

This skill writes skills as operational briefs for capable senior engineers with no local context. Favor invariants, decision boundaries, evidence, and stop rules over shell choreography or ceremony.

## Args

The args string should include:

- the skill name
- what the skill does
- any modes, commands, or repo context that materially change the design

If the request is underspecified, ask one clarifying question before proceeding.

## Core principles

- Write for a capable senior engineer, not a shell automaton.
- Frontmatter descriptions are for discovery. They should say when to use the skill, not summarize the whole workflow.
- Use the smallest amount of process that still preserves quality.
- Review feedback should protect invariants or sharpen decision boundaries, not automatically reintroduce procedural clutter.
- Token efficiency matters. If detail is rarely needed, keep it out of the main body or load it on demand.

## Routing decisions

Before drafting, classify:

- **Scope**: user-level or project-level
- **Target path**: the exact `SKILL.md` destination implied by that scope
- **Rules encoding**: whether the skill primarily preserves governance, policy, or decision algebra rather than a normal workflow

If any of those remain ambiguous after one clarifying question, stop and escalate.

## RED phase

Establish the failing baseline before writing the skill.

The baseline-failure exercise is mandatory when:

- editing an existing skill
- writing a skill that enforces rules, discipline, or decision boundaries
- the request is motivated by observed agent failure, drift, or rationalization

For a brand-new workflow skill with a clear spec and no observed failure history, a lighter RED phase is acceptable: identify at least one plausible failure mode before drafting.

Capture:

- what goes wrong without the skill
- what a weak version of the skill would fail to prevent
- what rationalizations or shortcuts the skill needs to resist

## Build flow

1. **Orient**
   - extract the skill name and purpose
   - classify scope, target path, and rules encoding

2. **Isolate**
   - if already in a worktree, continue
   - otherwise use `/isolate` before writing files

3. **Design**
   - use `/brainstorming` if the skill shape is still unclear after the initial clarification
   - keep it short; the goal is clarity, not a long discovery phase

4. **Write a plan**
   - write `ai-workspace/plans/build-skill-<name>.md`
   - include the skill spec, the RED baseline, target path, and what “good” means for this skill

5. **Review the plan**
   - run `/plan-review`
   - teach reviewers how to evaluate a good skill:
     - clear objective
     - clear invariants
     - evidence to gather
     - safe automatic paths
     - explicit stop boundaries
     - no penalty for avoiding shell choreography

6. **Draft one skill**
   - write one deliberate draft in the target style
   - do not run a default three-draft tournament

7. **Review the draft**
   - review against the RED baseline, invariants, and rationalizations
   - accept feedback that protects an invariant or clarifies a decision boundary
   - discuss feedback that mainly adds procedure without improving safety or clarity

8. **Refine or escalate**
   - revise until the skill is concise, discoverable, and safe
   - escalate instead of polishing forever when:
     - the request remains underspecified after one clarifying question
     - review finds an unresolved invariant failure
     - review disagreement is really a policy choice that repo context cannot settle
     - repeated revisions add process without improving safety or clarity

9. **Verify**
   - if project-level, confirm the skill is discoverable in the repo’s skill surface
   - run the repo validation needed for the touched files

10. **Archive and ship**
   - archive the plan when the work is done
   - ship through the normal repo workflow

## Policy algebra

Use policy algebra only when the skill primarily encodes governance rules, policy invariants, or decision algebra that must survive later editing.

Do not invoke policy algebra for ordinary workflow or technique skills just because they contain a few guardrails.

If policy algebra applies:

- generate the frozen rule block before drafting
- ensure the draft carries it exactly where required
- verify the final skill against that block before shipping

## What good looks like

A good skill:

- is easy to discover
- tells the agent when to use it
- defines the objective quickly
- preserves the important invariants
- gathers the minimum evidence needed to act safely
- defines what can happen automatically
- defines when the agent must stop
- avoids ceremony that does not improve outcomes

## Keep / avoid

Keep:

- trigger-first descriptions
- failure-mode-first thinking
- concise operational language
- explicit invariants and stop rules

Avoid:

- workflow-summary descriptions
- shell-macro choreography unless exact syntax is the point
- default multi-draft tournaments
- review loops that confuse verbosity with quality
