## Description: <br>
Venture Delegation helps an agent decompose opportunities, projects, and broad tasks into atomic work items with evals, dependency ordering, and model assignments for delegated execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dodge1218](https://clawhub.ai/user/dodge1218) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, founders, and project leads use this skill to turn new ideas, vague requests, or oversized tasks into a structured delegation plan with atomic outputs, machine-verifiable checks, model choices, and execution waves. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated eval commands or delegated work plans may be unsafe, incorrect, or unsuitable for the current workspace if executed without review. <br>
Mitigation: Review the delegation plan and each generated command before execution, and run commands only in an appropriate workspace. <br>
Risk: Task context may be routed through sub-agents or model providers and written into local plan or learning files. <br>
Mitigation: Avoid confidential tasks unless that routing and local recordkeeping are acceptable; redact sensitive details before delegation. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown plans, tables, prompts, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a delegation plan and append timing or pass-fail notes when the workflow is followed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
