## Description: <br>
Provides React and Next.js performance best-practice guidance for writing, reviewing, and refactoring application code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to guide React and Next.js component design, data fetching, rendering, server behavior, and bundle-size optimization. It is intended for code generation, code review, and refactoring tasks where performance patterns matter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says examples may steer agents toward unsafe inline scripts, auth-state handling, cookie logging, or shared user caches. <br>
Mitigation: Review generated React and Next.js changes before use, especially changes involving inline scripts, dangerouslySetInnerHTML, localStorage, cookies, logging, or server caches. <br>
Risk: Guidance involving auth behavior or shared server caches can create authorization or data-exposure issues if applied without context. <br>
Mitigation: Require server-side authorization checks, redaction for sensitive logs, and authorization-aware cache scoping for any generated implementation. <br>
Risk: Inline scripts and direct DOM or storage patterns may increase CSP or XSS exposure. <br>
Mitigation: Require explicit CSP and XSS protections when accepting generated changes that add inline scripts, dangerouslySetInnerHTML, or browser storage behavior. <br>


## Reference(s): <br>
- [React Documentation](https://react.dev) <br>
- [Next.js Documentation](https://nextjs.org) <br>
- [SWR Documentation](https://swr.vercel.app) <br>
- [better-all](https://github.com/shuding/better-all) <br>
- [node-lru-cache](https://github.com/isaacs/node-lru-cache) <br>
- [How We Optimized Package Imports in Next.js](https://vercel.com/blog/how-we-optimized-package-imports-in-next-js) <br>
- [How We Made the Vercel Dashboard Twice as Fast](https://vercel.com/blog/how-we-made-the-vercel-dashboard-twice-as-fast) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code] <br>
**Output Format:** [Markdown guidance with TypeScript and React examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language guidance derived from rule files and compiled agent documentation.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata, skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
