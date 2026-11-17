---
name: thought-flow
description: >
  The 8-stage collaboration loop for working with the user: INTENT,
  CONSTRAINTS, PROPOSE, PRESS, PRACTICE, INVESTIGATE, CODIFY, BOUNDARY-CHECK.
  Use when starting a new task (state intent and constraints up front), when
  proposing a plan (include options + a recommendation), when the user pushes
  back on a proposal, when something fails or looks broken and needs
  investigation, or when deciding whether to codify knowledge into an AGENTS.md
  rule or a SKILL.md procedure.
---

# Thought-Flow — the Collaboration Loop

The architecture of how the user and the agent work together. It is not a rigid process — it is a loop that converges: practice again, refine again. Every stage below is a working example of the others.

```
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│  1. INTENT         ──  what do I want? state it plainly        │
│          │                                                     │
│  2. CONSTRAINTS    ──  what must not change? boundaries,       │
│                       tools, remotes, conventions, approvals   │
│          │                                                     │
│  3. PROPOSE        ──  agent drafts a plan + options +         │
│                       recommendation                           │
│          │                                                     │
│  4. PRESS          ──  I push back where it conflicts with     │
│                       my constraints; we negotiate             │
│          │                                                     │
│  5. PRACTICE       ──  approve, build, run, observe            │
│                       (real failures live here)                │
│          │                                                     │
│  6. INVESTIGATE    ──  when it fails, verify against the       │
│                       real system before blaming the tool      │
│          │                                                     │
│  7. CODIFY         ──  distill the practice into AGENTS.md     │
│                       rules and SKILL.md steps                 │
│          │                                                     │
│  8. BOUNDARY-CHECK ──  is this the right repo / worktree /     │
│                       scope for this knowledge? resize if not  │
│          │                                                     │
│          └────── loop ── practice again, refine again ──────┘  │
└────────────────────────────────────────────────────────────────┘
```

## The stages

1. **INTENT — what do I want?** State it plainly, up front. The quality of the outcome depends more on how the problem is described than on the model.
2. **CONSTRAINTS — what must not change?** Boundaries, tools, remotes, conventions, approvals. Intent and Constraints are the most expensive stages: spending ten minutes stating them saves an hour of rework.
3. **PROPOSE — draft a plan with options + a recommendation.** A plan with only one path is a demand, not a proposal. Always include the tradeoffs so the user can disagree meaningfully.
4. **PRESS — the user pushes back where it conflicts with their constraints.** Negotiate. Do not just argue and do not just agree — look for a third option that respects the real constraints. The best outcomes are neither the agent's first idea nor the user's, but a compromise that holds.
5. **PRACTICE — approve, build, run, observe.** This is where the loop is honest. No plan survives contact with the real system; the failures at this stage are the ones that teach.
6. **INVESTIGATE — when it fails, verify against the real system before blaming the tool.** Read the upstream source, call the API, check the live state. An error message is a clue, not a conclusion. This is what separates debugging from guessing.
7. **CODIFY — distill the practice into durable knowledge.** A procedure that works twice becomes a candidate for a SKILL.md. A rule true for a whole repo becomes an AGENTS.md entry. Skill for the procedure, AGENTS.md for the constitution.
8. **BOUNDARY-CHECK — is this the right scope?** Which repo, which worktree, which file. OpenCode loads skills only up to the git worktree root — a parent-level skill is invisible inside a sub-repo session, so put knowledge where the work happens. Too broad dilutes; too narrow fragments.

Then loop: practice again, refine again, until the system becomes boring and reliable.

## Working with the loop

- The user holds the constraints; the agent holds the system knowledge. The agent's proposal is a first draft of a decision, not the decision itself.
- The user writes their operating preferences into AGENTS.md so the agent never has to ask: minimalist, Linux only, command line preferred, approval before changes, commit only when asked.
- Prefer `gh` and the API for verification (`gh run watch`, `gh run view --log`, `gh api`, `curl` against live endpoints) over UI clicking. The API is the primary way to verify; a registry's or workflow's own report can be wrong (e.g. a success reported as `pending-publication` failure).
- Precision in, precision out. Vague intent produces guesswork; precise constraints produce exactly the automation the user wanted.

## Verification

- Intent and constraints were stated before any plan was drafted.
- Proposals carried at least two options plus a recommendation.
- Failures were investigated against the real system before concluding the tool or workflow was broken.
- Knowledge worth keeping was codified — into a SKILL.md for a procedure, an AGENTS.md entry for a repo-wide rule — at the worktree where the work happens.
