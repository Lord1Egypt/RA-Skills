## Description: <br>
Structured PR Review guides agents through layered GitHub pull request reviews and review-comment follow-up using the gh CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ggettert](https://clawhub.ai/user/ggettert) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review GitHub pull requests with security, correctness, conventions, infrastructure-as-code, and testing layers, then produce a structured verdict. They can also use it to address reviewer comments, update PRs, reply to threads, and resolve conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Addressing review feedback can commit changes, push branches, update PR descriptions, post replies, and resolve GitHub review threads. <br>
Mitigation: Use repository-scoped gh credentials, confirm write actions before execution, and prefer review-only mode when comments or branch updates are not needed. <br>
Risk: A structured review may still miss issues or assign the wrong severity to a finding. <br>
Mitigation: Have a human maintainer review the verdict before relying on it for merge approval or requested changes. <br>


## Reference(s): <br>
- [Review Layers](references/review-layers.md) <br>
- [Addressing Review Comments](references/addressing-workflow.md) <br>
- [Team Conventions](references/conventions.md) <br>
- [Infrastructure as Code Checklist](references/iac-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown review verdicts, issue notes, summaries, comment replies, and inline gh CLI commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses severity tiers: MUST FIX, SHOULD FIX, and SUGGESTION.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
