## Description: <br>
Reviews Remix v2 route data-flow code for loader and action mistakes, validation gaps, leaked server fields, incorrect return helpers, v1 transition holdovers, revalidation issues, and defer/Await traps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review Remix v2 TypeScript route modules for data-flow mistakes in loaders, actions, revalidation, pending state, and defer/Await streaming before reporting code-review findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may lead an agent to inspect route modules that contain sensitive fields such as passwords, tokens, or API keys. <br>
Mitigation: Use it only in repositories where that level of code-review access is acceptable, and review findings before acting on them. <br>


## Reference(s): <br>
- [Action Review Reference](references/actions.md) <br>
- [Defer & Await Review Reference](references/defer-await.md) <br>
- [Loader Review Reference](references/loaders.md) <br>
- [Revalidation & Pending State Review Reference](references/revalidation.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown code-review findings and guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings are expected to include route locations, exemption checks, and verification context before user-facing reporting.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
