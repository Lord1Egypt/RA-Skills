## Description: <br>
Reviews Remix v2 error-handling code for the unified ErrorBoundary, isRouteErrorResponse narrowing, throw-vs-return, root boundary scaffolding, and v1 holdovers (CatchBoundary, useCatch). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and code reviewers use this skill to review TypeScript Remix v2 route modules for correct error boundary behavior, thrown Response handling, root boundary scaffolding, and v1 migration holdovers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may read and search Remix project files during review. <br>
Mitigation: Use the skill in repositories where code review access is intended; the skill itself is documentation-only and does not request credentials or make changes. <br>
Risk: Review guidance may produce incorrect or overbroad findings if valid Remix v2 inheritance patterns are not checked. <br>
Mitigation: Require location evidence, exemption checks, and v1-vs-v2 marker checks before reporting findings. <br>


## Reference(s): <br>
- [Boundary Shape Reference](references/boundary-shape.md) <br>
- [Root Boundary Reference](references/root-boundary.md) <br>
- [Throw Response Reference](references/throw-response.md) <br>
- [V1 Holdovers Reference](references/v1-holdovers.md) <br>
- [Remix v2 ErrorBoundary Docs](https://remix.run/docs/en/main/route/error-boundary) <br>
- [Remix v2 Error Handling Guide](https://remix.run/docs/en/main/guides/errors) <br>
- [Remix v2 entry.server handleError Docs](https://remix.run/docs/en/main/file-conventions/entry.server) <br>
- [ClawHub Skill Page](https://clawhub.ai/anderskev/remix-v2-error-boundaries-review) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown review findings with code references and suggested fixes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings should include file location evidence, exemption checks, v1-vs-v2 marker checks, and severity labels before user-facing reporting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
