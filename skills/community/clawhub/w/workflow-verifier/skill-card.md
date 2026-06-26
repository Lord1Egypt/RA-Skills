## Description: <br>
工作流验证器 - 在执行前验证工作流的正确性、安全性和完整性。基于Karpathy法则，强调先思考、保持简单、目标驱动的原则。适用于代码审查、工作流执行、任务规划等场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and reviewers use this skill to check workflow assumptions, complexity, change scope, and validation steps before code generation, bug fixes, workflow execution, or PR review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate on broad safety or workflow-review phrases. <br>
Mitigation: Use it when a lightweight pre-execution review checklist is desired, and confirm the review context before relying on its decision. <br>
Risk: Private files, account data, or secrets could be exposed if intentionally supplied as review input. <br>
Mitigation: Provide only the workflow details needed for review; do not include secrets or unnecessary private data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/534422530/workflow-verifier) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown checklist with findings, suggestions, and an execution decision] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No code execution, credentials, persistence, or hidden data access reported by ClawHub security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
