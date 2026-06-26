# Research Patterns

Use these patterns to plan efficient web research and subagent delegation.

## Query ladder

1. **Landscape query:** broad terms to learn vocabulary and major sources.
2. **Primary-source query:** add `official docs`, `release notes`, `spec`, `site:vendor.com`, `github`, or exact project names.
3. **Version/date query:** include version numbers, year, or product edition.
4. **Problem query:** search the exact error, constraint, or use case.
5. **Contradiction query:** search for `limitations`, `deprecated`, `breaking changes`, `security`, `known issues`, or `comparison`.

Stop when additional searches repeat the same evidence and the answer is stable.

## Fast-moving topic pattern

Use for APIs, models, pricing, packages, frameworks, laws, security, and current events.

- Require date/version awareness.
- Prefer official pages and release notes.
- Check at least one recent secondary source only to discover context, not as final authority.
- Call out when information may change.

## Technical implementation pattern

Use when research will affect code or configuration.

- Find official docs and minimal examples.
- Identify supported versions and platform constraints.
- Extract exact commands/config keys/API shapes.
- After implementation, run a small verification gate: test, lint, build, dry-run, status command, or direct inspection.

## Comparative research pattern

Use when choosing between options.

- Define evaluation criteria first: cost, reliability, ecosystem, complexity, privacy, maintenance, performance.
- Gather evidence per option using the same criteria.
- Present a recommendation with tradeoffs, not a giant matrix unless asked.

## Multi-subagent pattern

Use when tracks are independent:

- **Retriever:** collect primary sources and key quotes.
- **Skeptic:** find limitations, risks, contradictions, recent changes.
- **Synthesizer:** merge findings into a recommendation.

Keep the main agent as the hub. Subagents should not coordinate with each other unless the environment explicitly supports it and the task needs it.

## Minimum final brief

Every useful research result should include:

- Direct answer.
- Evidence with URLs.
- Recommendation or next action.
- Risks/unknowns.
