## Description:

React and Next.js performance optimization guidelines from Vercel Engineering for writing, reviewing, and refactoring performance-sensitive applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[analsharqy](https://clawhub.ai/user/analsharqy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and code-review agents use this skill when writing, reviewing, or refactoring React and Next.js code for performance across data fetching, rendering, bundle size, caching, and re-render behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic application of performance guidance may introduce insecure React or Next.js patterns.

Mitigation: Review proposed changes before execution and apply the server-provided security guidance during code review.

Risk: Examples involving HTML injection, cookie handling, shell tools, or cross-request caching can be unsafe when copied without project-specific controls.

Mitigation: Use pinned or local dependencies, require CSP review for static HTML injection, avoid logging raw session cookies, and scope cross-request cache keys and data to the same authorization context.

## Reference(s):

- [React Documentation](https://react.dev)
- [Next.js Documentation](https://nextjs.org)
- [SWR Documentation](https://swr.vercel.app)
- [better-all](https://github.com/shuding/better-all)
- [node-lru-cache](https://github.com/isaacs/node-lru-cache)
- [How We Optimized Package Imports in Next.js](https://vercel.com/blog/how-we-optimized-package-imports-in-next-js)
- [How We Made the Vercel Dashboard Twice as Fast](https://vercel.com/blog/how-we-made-the-vercel-dashboard-twice-as-fast)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown guidance with TypeScript/TSX examples and occasional shell or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; output should be reviewed before automated code changes.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
