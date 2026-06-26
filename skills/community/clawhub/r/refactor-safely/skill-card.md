## Description: <br>
Plans and executes safe refactors through scoped steps, tests, verification, and rollback planning without changing external behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangzhiming1999](https://clawhub.ai/user/wangzhiming1999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan and carry out behavior-preserving refactors, split changes into reviewable steps, verify each step, and keep rollback instructions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad refactoring requests can change behavior or exceed the intended scope. <br>
Mitigation: Confirm the refactoring scope, public behavior that must remain unchanged, and the proposed plan before accepting changes. <br>
Risk: Refactors without adequate verification can introduce regressions. <br>
Mitigation: Use version control, run or add tests for core paths, inspect diffs, and keep rollback notes for each step. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangzhiming1999/refactor-safely) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance] <br>
**Output Format:** [Markdown refactoring plan with scope, risk, validation, and rollback notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable code; recommendations should be reviewed before accepting code changes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
