## Description:

Provides React and Next.js performance optimization guidelines from Vercel Engineering for agents writing, reviewing, or refactoring applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iammarcellus](https://clawhub.ai/user/iammarcellus)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to apply React and Next.js performance patterns during code generation, review, and refactoring. It focuses on data fetching, bundle size, server-side behavior, client-side storage, rendering, and re-render optimization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may copy insecure example patterns into application code.

Mitigation: Review generated code before merging and require authentication, authorization, validation, and secret-handling checks for affected paths.

Risk: Examples involving cookies, tokens, local storage, or DOM reads may be misused as authority sources.

Mitigation: Do not log raw cookies or tokens, avoid storing sensitive data in client-side storage, and keep authorization decisions on trusted server-side paths.

Risk: Bare CLI examples such as npx can resolve different tool versions over time.

Mitigation: Pin CLI and package versions when turning examples into repeatable build or optimization commands.

Risk: Inline scripts used for hydration behavior can create security and maintainability risk if expanded beyond static bootstraps.

Mitigation: Restrict inline scripts to vetted static bootstraps, keep sensitive values out of them, and review them against the application's content security policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iammarcellus/skills/react-best-practices-3)
- [React documentation](https://react.dev)
- [Next.js documentation](https://nextjs.org)
- [SWR documentation](https://swr.vercel.app)
- [better-all](https://github.com/shuding/better-all)
- [node-lru-cache](https://github.com/isaacs/node-lru-cache)
- [How we optimized package imports in Next.js](https://vercel.com/blog/how-we-optimized-package-imports-in-next-js)
- [How we made the Vercel Dashboard twice as fast](https://vercel.com/blog/how-we-made-the-vercel-dashboard-twice-as-fast)
- [Next.js authentication guide](https://nextjs.org/docs/app/guides/authentication)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with TypeScript, TSX, shell, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance that agents may apply when proposing or editing React and Next.js application code.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter and metadata state 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
