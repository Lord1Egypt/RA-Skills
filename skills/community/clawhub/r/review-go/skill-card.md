## Description: <br>
Comprehensive Go backend code review with optional parallel review areas. Use when reviewing changed Go files; detects BubbleTea, Wish SSH, and Prometheus and loads the matching review skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review changed Go backend code and related test changes. It guides an agent to inspect diffs, load applicable Go review skills, verify findings, and report categorized issues with file-line references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local repository files and suggests normal Go verification commands that may be expensive or sensitive in large repositories. <br>
Mitigation: Review the proposed commands before running them and scope execution to the appropriate repository and environment. <br>
Risk: Code-review findings can be misleading if based only on diff context or incomplete reference checks. <br>
Mitigation: Use the skill's verification gates: re-read relevant code, search references for unused-code claims, and check callers or framework wiring before reporting blocking issues. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anderskev/review-go) <br>
- [Publisher profile](https://clawhub.ai/user/anderskev) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown review report with issue severities, file-line references, verification notes, and verdict.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include suggested Go verification commands such as go build, go vet, golangci-lint run, and go test -race.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
