## Description:

React and Next.js performance optimization guidelines from Vercel Engineering, with 57 rules across 8 categories for writing, reviewing, and refactoring React code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill when writing, reviewing, refactoring, or optimizing React and Next.js applications for performance, bundle size, rendering behavior, data fetching, and server/client boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some examples involve session cookies or client-side storage and could expose sensitive data if copied without review.

Mitigation: Review examples before applying them, avoid logging raw session cookies, and keep authentication data scoped to the minimum required context.

Risk: Inline script examples can weaken XSS posture if adapted with untrusted values.

Mitigation: Use strict XSS and CSP guardrails, keep inline script data controlled, and avoid injecting unsanitized user input.

Risk: Cross-request cache examples can leak or reuse data across users or tenants if the cache key is too broad.

Mitigation: Scope caches by tenant, user, and authorization context, and use explicit TTLs and invalidation rules.

Risk: Mutable npx or GitHub install commands can fetch code that has not been reviewed.

Mitigation: Pin install commands to reviewed package versions, release tags, or commits before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wpank/skills/react-best-practices)
- [How We Optimized Package Imports in Next.js](https://vercel.com/blog/how-we-optimized-package-imports-in-next-js)
- [React cache Documentation](https://react.dev/reference/react/cache)
- [Next.js Authentication Guide](https://nextjs.org/docs/app/guides/authentication)
- [React: You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect#initializing-the-application)
- [better-all](https://github.com/shuding/better-all)
- [node-lru-cache](https://github.com/isaacs/node-lru-cache)
- [Vercel Fluid Compute](https://vercel.com/docs/fluid-compute)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with TypeScript, TSX, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Designed for agents to apply as review and refactoring guidance; examples require human review before use in production code.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
