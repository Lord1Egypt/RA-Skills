## Description: <br>
React and Next.js performance optimization guidelines from Vercel Engineering for writing, reviewing, and refactoring performant React and Next.js code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[analsharqy](https://clawhub.ai/user/analsharqy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill when creating, reviewing, or refactoring React and Next.js applications to apply performance patterns for data fetching, bundle size, server and client rendering, re-renders, and JavaScript hot paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some examples may encourage risky handling of session cookies, inline scripts, or cross-request user-data caching without enough guardrails. <br>
Mitigation: Review generated changes before use; do not log cookies or tokens, avoid caching full user records across requests without scoped keys and invalidation, and use inline scripts only when CSP and data handling are explicitly safe. <br>
Risk: Performance advice may be applied as if it were authoritative security guidance. <br>
Mitigation: Treat the skill as a performance-review aid and route security-sensitive changes through normal application security review. <br>


## Reference(s): <br>
- [React Documentation](https://react.dev) <br>
- [Next.js Documentation](https://nextjs.org) <br>
- [SWR Documentation](https://swr.vercel.app) <br>
- [better-all](https://github.com/shuding/better-all) <br>
- [node-lru-cache](https://github.com/isaacs/node-lru-cache) <br>
- [How we optimized package imports in Next.js](https://vercel.com/blog/how-we-optimized-package-imports-in-next-js) <br>
- [How we made the Vercel Dashboard twice as fast](https://vercel.com/blog/how-we-made-the-vercel-dashboard-twice-as-fast) <br>
- [ClawHub skill page](https://clawhub.ai/analsharqy/react-best-practices-2) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown guidance with TypeScript, React, Next.js, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are advisory and should be reviewed before code changes are applied.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
