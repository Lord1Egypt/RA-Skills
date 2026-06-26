## Description: <br>
Remix v2 data loading and mutations. Use when writing loaders, actions, deferred data, revalidation logic, or pending state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to choose and implement Remix v2 loaders, actions, deferred data, revalidation, and pending-state patterns while avoiding common v1-to-v2 migration mistakes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate for broad Remix loader or action discussions where project-specific Remix versions or adapters differ. <br>
Mitigation: Verify API details against the Remix version and runtime adapter used in the target project. <br>
Risk: Generated guidance may be copied into code paths that return sensitive loader data or suppress needed revalidation. <br>
Mitigation: Review generated changes before use, return safe DTOs from loaders, and keep default revalidation unless an opt-out is justified. <br>


## Reference(s): <br>
- [Loaders](references/loaders.md) <br>
- [Actions](references/actions.md) <br>
- [Defer & Await - Streaming Loader Data](references/defer-await.md) <br>
- [Revalidation & Pending State](references/revalidation.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code] <br>
**Output Format:** [Markdown guidance with TypeScript and TSX examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no executable code is included in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
