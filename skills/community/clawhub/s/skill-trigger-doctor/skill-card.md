## Description: <br>
Diagnose, fix, and prevent agent skill trigger failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thomaszhou22](https://clawhub.ai/user/thomaszhou22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to diagnose skill activation failures, audit skill descriptions, validate YAML frontmatter, manage trigger token budgets, and improve trigger accuracy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the included audit script with --fix can modify SKILL.md files in the selected skills directory. <br>
Mitigation: Review the generated changes before relying on the repaired metadata or deploying the edited skills. <br>
Risk: Trigger guidance or remediation suggestions can introduce incorrect or overly broad skill descriptions. <br>
Mitigation: Manually test repaired skills with representative natural-language triggers and review descriptions for false-positive activation. <br>


## Reference(s): <br>
- [Failure Pattern Reference](references/failure-patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/thomaszhou22/skill-trigger-doctor) <br>
- [Publisher Profile](https://clawhub.ai/user/thomaszhou22) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with bash commands and optional JSON audit reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or apply edits to skill metadata when the included audit script is run with --fix.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
