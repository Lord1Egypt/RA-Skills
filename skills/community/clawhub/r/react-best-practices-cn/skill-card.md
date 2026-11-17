## Description:

Chinese-language React and Next.js performance guidance for agents that write, review, or refactor components, pages, data fetching, bundle behavior, and rendering patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT

## Use Case:

Developers and AI coding agents use this skill to apply React and Next.js performance best practices during code generation, review, and refactoring. It focuses on avoiding waterfalls, reducing bundle size, improving server and client data access, and minimizing unnecessary rendering work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may apply performance examples without adapting them to application security requirements.

Mitigation: Review generated code before use and verify that authentication, authorization, tenant scoping, and data handling remain correct.

Risk: Caching examples can lead to exposure of user-specific records across requests or tenants.

Mitigation: Scope caches by request, user, and tenant where applicable, and avoid cross-request caching for sensitive data unless authorization boundaries are enforced.

Risk: Examples involving inline scripts, logging, or package-manager execution can introduce CSP, secret-handling, or supply-chain risk.

Mitigation: Avoid logging raw session cookies or tokens, control CSP and interpolation risks for inline scripts, and pin package-manager tooling before execution.

## Reference(s):

- [React documentation](https://react.dev)
- [Next.js documentation](https://nextjs.org)
- [SWR documentation](https://swr.vercel.app)
- [better-all](https://github.com/shuding/better-all)
- [node-lru-cache](https://github.com/isaacs/node-lru-cache)
- [How we optimized package imports in Next.js](https://vercel.com/blog/how-we-optimized-package-imports-in-next-js)
- [How we made the Vercel Dashboard twice as fast](https://vercel.com/blog/how-we-made-the-vercel-dashboard-twice-as-fast)
- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/skills/react-best-practices-cn)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code]

**Output Format:** [Markdown guidance with TypeScript and React examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language guidance organized as prioritized React and Next.js performance rules.]

## Skill Version(s):

1.0.0 (source: server release, artifact metadata, and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
