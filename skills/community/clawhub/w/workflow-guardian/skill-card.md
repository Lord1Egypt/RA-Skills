## Description: <br>
Defines, enforces, and tracks structured workflows for any task type, including do/don't rules, execution sequences, hard gates, soft advisories, checkpoints, and violation detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyber-bye](https://clawhub.ai/user/cyber-bye) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to define repeatable task workflows, enforce ordered execution, check gates and checkpoints, and record violations for later review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad workflow enforcement can interrupt normal agent work or block progress at gates across unrelated tasks. <br>
Mitigation: Install only in workspaces where this control model is intended, and define narrow activation rules plus explicit owner override procedures. <br>
Risk: Persistent logs, memory state, workflow history, and violation entries may capture sensitive task details. <br>
Mitigation: Set clear write locations, redact secrets and personal data before logging, and review stored workflow artifacts regularly. <br>
Risk: Post-fix behavior can lead to autonomous corrective changes after violations. <br>
Mitigation: Require owner approval before autonomous fixes on confidential, destructive, or production-impacting tasks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cyber-bye/workflow-guardian) <br>
- [Publisher profile](https://clawhub.ai/user/cyber-bye) <br>
- [JSON Schema draft-07](http://json-schema.org/draft-07/schema#) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown workflow rules, hook instructions, templates, and JSON schema] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces persistent workflow, log, rules, memory, checkpoint, and violation structures for an agent workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
