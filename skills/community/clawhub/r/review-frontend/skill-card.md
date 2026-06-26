## Description: <br>
Comprehensive React/TypeScript frontend code review with per-area review skills, run in parallel where the agent supports subagents and sequentially otherwise. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review React and TypeScript frontend changes across routing, component, state, styling, testing, security, performance, and accessibility concerns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Post-fix verification commands execute npm scripts from the target repository. <br>
Mitigation: Use normal caution when running the verification step on untrusted projects. <br>
Risk: Incorrect review guidance can cause unnecessary or harmful code changes. <br>
Mitigation: The skill requires findings to be verified against actual files, references, and framework behavior before reporting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anderskev/review-frontend) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown review report with issue severity sections, file and line references, verdict, and post-fix verification commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The review output is a single consolidated pass with sequential issue numbering and a verdict based on Critical and Major findings.] <br>

## Skill Version(s): <br>
1.0.3 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
