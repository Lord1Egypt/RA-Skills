# Phase 2: Explore

Deeply analyze the codebase to understand how the project works and how the requirement relates to existing code. This phase delegates exploration to three parallel subagents for efficiency.

## What to Communicate

After merging the three subagent results, present a unified picture covering:

- **Architecture** — how the project is organized
- **Relevant files** — each file's role and why it matters for this requirement
- **Existing patterns** — conventions and patterns the implementation should follow
- **Similar implementations** — precedent features and how they were done
- **Impact radius** — how many files and modules would be affected
- **Constraints discovered** — limitations from code structure, tech stack, or conventions

Merge and deduplicate the subagent findings. Keep the total under 500 words.

## Context to Preserve

Before finishing, make sure the conversation retains: the architecture style in brief, the top relevant file paths, the primary pattern to follow, the impact radius, and the most important constraints.

## Steps

1. TaskUpdate — set Phase 2 to `in_progress`.
2. Launch three parallel subagents using the Agent tool. Include the context summary in each prompt so they know what to explore.
3. After all three return, merge their findings into a unified summary. Remove redundant findings between subagents.
4. Preserve context for downstream phases.
5. TaskUpdate — set Phase 2 to `completed`.

### Subagent Assignments

**Explorer-1: Structure & Pattern**
Directory organization, module boundaries, entry points, build system, dependency management, architecture style (MVC, layered, hexagonal, event-driven), naming conventions, import/dependency patterns.

**Explorer-2: Impact & Convention**
Files and modules directly related to the requirement, their dependents, shared utilities or services involved, database models or schemas, error handling approach, logging, test structure, and configuration conventions.

**Explorer-3: Precedent**
Similar features previously implemented, patterns to follow for consistency, anti-patterns to avoid, reusable components or utilities.

### Subagent Guidelines

- Reference specific file paths, not vague descriptions
- Note patterns the implementation should follow for consistency
- Identify potential conflicts or constraints early
- If no relevant code is found, say so explicitly — the feature may be novel
- LSP tools (go to definition, find references) can improve exploration depth

## Rollback

If a later phase discovers insufficient exploration: set Phase 2 back to `pending`, specify additional focus areas.
