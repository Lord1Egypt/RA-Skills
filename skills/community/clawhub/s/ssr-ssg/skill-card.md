## Description:

Deep workflow for SSR, SSG, ISR, and hybrid rendering that helps agents choose modes per route, plan data freshness and caching, handle streaming and hydration, and validate SEO, performance, and operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to guide SSR, SSG, ISR, edge, and hybrid rendering decisions for modern web applications. It helps agents produce route-level rendering strategies, caching plans, hydration boundary checks, and validation guidance for SEO, performance, and operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect SSR, SSG, ISR, cache, or edge-rendering changes can affect freshness, SEO, performance, or private-data caching.

Mitigation: Review proposed rendering and caching changes per route, with explicit freshness, authentication, cache-vary, invalidation, SEO, and performance checks before deployment.

Risk: Hydration or server-client boundary mistakes can duplicate work, expose server-only assumptions, or cause runtime mismatches.

Mitigation: Verify client islands, serialized state, environment-specific APIs, and hydration-sensitive values such as locale, random IDs, and time.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/codekungfu/skills/ssr-ssg)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with matrices, checklists, and implementation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include per-route rendering recommendations, cache and invalidation plans, streaming and hydration checks, and SEO/performance validation steps.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
