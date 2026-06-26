## Description: <br>
Comprehensive iOS/SwiftUI code review with optional parallel agents <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review iOS and SwiftUI changes for correctness, architecture, concurrency, tests, security, performance, and framework-specific issues. It guides agents through scoped Swift file discovery, linter checks, technology detection, finding verification, and a consolidated Markdown review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects Swift source files and may run local lint, build, and test commands in the reviewed repository. <br>
Mitigation: Review command output before acting on findings, especially in sensitive or large projects. <br>
Risk: Code review findings can be incorrect or misleading if generated without enough source context. <br>
Mitigation: Use the skill's gates requiring scoped Swift files, linter checks, protocol loading, and re-reading code around Critical or Major findings. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown review report with severity-grouped findings, file and line references, good patterns, and a verdict] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local SwiftLint, build, and test commands for verification.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
