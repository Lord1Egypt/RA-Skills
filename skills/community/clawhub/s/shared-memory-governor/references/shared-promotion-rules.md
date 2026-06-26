# Promotion Rules

## Quick map

- Purpose
- Shared scope validation rule
- Candidate evaluation categories
- Shared file boundaries
- Shared scan promotion template
- Source priority rule

## Purpose

Use this reference when running `run-shared-scan` or reviewing whether a local memory item may be promoted into shared memory.

## Shared scope validation rule

Treat shared-scope validation as a separate hard gate during shared promotion.

Default rule in v1:
- a candidate found in only one agent's approved local memory source should be skipped
- similarity or repetition across multiple participating agents should be treated as the primary promotion signal by default
- single-agent items should not be promoted merely because they look useful or shareable

Allow promotion from a single local source only when at least one of the following is true:
- the user explicitly designated the item as shared or global
- the item is clearly a shared-memory governance rule rather than an agent-local working habit
- the item is otherwise explicitly documented as globally applicable to all participating agents

Treat the following as the standard `promotionBasis` values:
- `explicit-user-designation`
- `multi-agent-corroboration`
- `shared-governance-rule`

If none of these bases can be justified clearly, skip the candidate.

### Practical interpretation

Use this default decision order:
1. Check whether substantially similar content appears across multiple participating agents
2. If not, check whether the user explicitly said the item should be shared
3. If not, check whether the item is a shared-memory governance rule
4. Otherwise skip the item

Do not treat "seems broadly useful" as a sufficient basis by itself.

## Candidate evaluation categories

Explicitly distinguish:
- `user-global` preferences and constraints
- `cross-agent` facts
- `shared-governance` rules
- agent-local workflow habits
- role-specific defaults
- project-specific context

Only the first three categories are promotable by default in v1.

## Shared file boundaries

### `shared-user.md`

Allowed examples:
- user timezone
- user communication preferences
- user delivery preferences that apply across multiple agents
- stable memory-collaboration preferences

Disallowed examples:
- one agent's private task defaults
- one agent's role-specific writing habits
- project-specific operating detail that applies only to one agent

### `shared-memory.md`

Allowed examples:
- cross-agent project facts
- durable environment facts
- shared-memory governance facts that are not merely file-placement rules

Disallowed examples:
- agent-specific project context
- one-off execution traces
- temporary debugging notes

### `shared-rules.md`

Allowed examples:
- read order rules
- attachment rules
- promotion rules
- schedule review rules

Disallowed examples:
- user preference content
- reusable project facts
- agent-local working defaults

## Shared scan promotion template

For each promoted item, record at minimum:
- `sourceAgents`
- `sourceFiles`
- `targetSharedFile`
- `scopeType` (`user-global` | `cross-agent` | `shared-governance`)
- `promotionBasis` (`explicit-user-designation` | `multi-agent-corroboration` | `shared-governance-rule`)
- `whyNotAgentLocal`
- `corroborationStatus`

## Source priority rule

`sourcePriority` controls candidate discovery order only. It does not authorize promotion by itself.
