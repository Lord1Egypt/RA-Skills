## Description:

React and Next.js performance optimization guidelines from Vercel Engineering for writing, reviewing, and refactoring code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mutsunico](https://clawhub.ai/user/mutsunico)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to apply React and Next.js performance practices while generating, reviewing, or refactoring application code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may copy unsafe guidance patterns into production code involving session cookies, inline scripts, or shared caches.

Mitigation: Review generated changes before use, avoid logging raw cookies or tokens, avoid dynamic `dangerouslySetInnerHTML`, and scope cross-request caches carefully.

Risk: Tooling examples that rely on floating commands can change behavior over time.

Mitigation: Use pinned or project-local tooling when applying this skill in a codebase.

## Reference(s):

- [React documentation](https://react.dev)
- [Next.js documentation](https://nextjs.org)
- [SWR documentation](https://swr.vercel.app)
- [better-all](https://github.com/shuding/better-all)
- [node-lru-cache](https://github.com/isaacs/node-lru-cache)
- [How we optimized package imports in Next.js](https://vercel.com/blog/how-we-optimized-package-imports-in-next-js)
- [How we made the Vercel Dashboard twice as fast](https://vercel.com/blog/how-we-made-the-vercel-dashboard-twice-as-fast)
- [ClawHub skill page](https://clawhub.ai/mutsunico/skills/react-best-practices-2-0-1-0)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown guidance with React and Next.js code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill guidance for agent-assisted code work.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
